"""Model machinery.

Copied from 4. Bayesian - Leontief models/leontief_model.py
2016-12-19
"""

import numpy as np
import pandas as pd
import theano.tensor as T
from theano.tensor.nlinalg import matrix_inverse
import pymc3 as pm


from floweaver import Dataset, weave


def inputs_flows_as_dataframe(processes, possible_inputs, inputs, flows):
    """Turn inputs & flows vectors into dataframe of flows"""
    flows = []
    num_processes = flows.shape[0]  # pylint: disable=no-member
    for target, value in zip(possible_inputs, inputs):
        if value > 0:
            flows.append(('inputs', target, '?', value))

    # lookup process id to index
    process_ids = list(processes.keys())
    for i in range(num_processes):
        for j in range(num_processes):
            if flows[i, j] > 0:
                flows.append((process_ids[i], process_ids[j], '?', flows[i, j]))
    return pd.DataFrame.from_records(flows, columns=('source', 'target', 'material', 'value'))



class SplitParamModel:
    """Flow model with different types of prior for different process sub-models.
    """
    def __init__(self, processes, input_defs, param_defs, flow_observations=None,
                 input_observations=None, inflow_observations=None):
        self.processes = processes
        self.possible_inputs = possible_inputs = sorted(list(input_defs.keys()))
        input_max = [input_defs[k] for k in possible_inputs]
        self.param_defs = param_defs

        with pm.Model() as self.model:
            # Inputs
            # Lognormal seems too biased towards very small inputs; try half-Cauchy or similar?
            inputs = pm.Uniform('inputs', lower=np.zeros_like(input_max),
                                upper=input_max, shape=len(input_max))

            # Params for each process
            # params = pm.Normal('params', mu=param_means, sd=param_stds, shape=len(param_means))
            process_params = {
                pid: process.param_rv(pid, param_defs.get(pid))
                for pid, process in processes.items()
            }

            # transfer_coeffs
            transfer_coeffs, all_inputs = self._build_matrices(process_params, inputs)
            transfer_coeffs = pm.Deterministic('TCs_coeffs', transfer_coeffs)
            process_throughputs = pm.Deterministic(
                'X', T.dot(matrix_inverse(T.eye(len(processes)) - transfer_coeffs), all_inputs))

            # Flows
            flows = pm.Deterministic('F', transfer_coeffs.T * process_throughputs[:, None])

            # Observations - flows
            if flow_observations is not None:
                flow_obs, flow_data, flow_stds = self._flow_observations(flow_observations)
                Fobs = pm.Deterministic('Fobs', T.tensordot(flow_obs, flows, 2))
                pm.Normal('FD', mu=Fobs, sd=flow_stds, observed=flow_data)

            # Observations - inputs
            if input_observations is not None:
                input_obs, input_data, input_stds = self._input_observations(input_observations)
                Iobs = pm.Deterministic('Iobs', T.dot(input_obs, all_inputs))
                pm.Normal('ID', mu=Iobs, sd=input_stds, observed=input_data)

            # Observations - ratios
            if inflow_observations is not None:
                inflow_obs, inflow_data, inflow_stds = self._flow_observations(inflow_observations)
                inflow_fractions = flows / process_throughputs[None, :]
                Iratioobs = pm.Deterministic('IFobs', T.tensordot(inflow_obs, inflow_fractions, 2))
                pm.Normal('IFD', mu=Iratioobs, sd=inflow_stds, observed=inflow_data)

    def _build_matrices(self, process_params, inputs):
        Np = len(self.processes)
        transfer_coeffs = T.zeros((Np, Np))

        # lookup process id to index
        pids = {k: i for i, k in enumerate(self.processes)}

        for pid, process in self.processes.items():
            if not process_params.get(pid):
                continue
            params = process_params[pid]
            process_tcs = process.transfer_functions(params)
            if process.outputs:
                dest_idx = [pids[dest_id] for dest_id in process.outputs]
                transfer_coeffs = T.set_subtensor(transfer_coeffs[dest_idx, pids[pid]], process_tcs)

        possible_inputs_idx = [pids[k] for k in self.possible_inputs]
        all_inputs = T.zeros(Np)
        all_inputs = T.set_subtensor(all_inputs[possible_inputs_idx], inputs)

        return transfer_coeffs, all_inputs

    def _flow_observations(self, observations):
        Np = len(self.processes)
        No = len(observations)
        flow_obs = np.zeros((No, Np, Np))
        flow_data = np.zeros(No)
        flow_stds = np.zeros(No)
        pids = {k: i for i, k in enumerate(self.processes)}
        for i, (sources, targets, value, std) in enumerate(observations):
            flow_obs[i, [pids[k] for k in sources], [pids[k] for k in targets]] = 1
            flow_data[i] = value
            flow_stds[i] = std
        return flow_obs, flow_data, flow_stds

    def _input_observations(self, observations):
        Np = len(self.processes)
        No = len(observations)
        input_obs = np.zeros((No, Np))
        input_data = np.zeros(No)
        input_stds = np.zeros(No)
        pids = {k: i for i, k in enumerate(self.processes)}
        for i, (targets, value, std) in enumerate(observations):
            input_obs[i, [pids[k] for k in targets]] = 1
            input_data[i] = value
            input_stds[i] = std
        return input_obs, input_data, input_stds

    def get_flow(self, trace, source, target):
        """Pick out flow from trace."""
        pids = {k: i for i, k in enumerate(self.processes)}
        return trace['flows'][:, pids[source], pids[target]]

    def show_point(self, point, sdd):
        """Show Sankey diagram for trace point."""
        all_inputs = self.model.deterministics[0].eval({
            v: point[str(v)] for v in self.model.vars if str(v) == 'inputs_interval_'})
        flows = self.model.flows.eval({
            self.model.inputs_interval_: point['inputs_interval_'],
            self.model.params: point['params']})
        dataset = Dataset(
            inputs_flows_as_dataframe(self.processes, self.possible_inputs, all_inputs, flows))
        return weave(sdd, dataset).to_widget( width=900, height=400,
                                              margins=dict(left=bg50, right=100, top=10, bottom=10))


class EfficiencyProcess:
    nparams = 1

    def __init__(self, name, outputs):
        assert len(outputs) == 2
        self.name = name
        self.outputs = outputs

    @staticmethod
    def transfer_functions(params):
        # logistic efficiency
        eff = T.exp(params[0]) / (1 + T.exp(params[0]))
        return T.stack([eff, 1 - eff])

    def param_rv(self, pid, defs):
        if defs:
            # Normal dist about given mean & sd
            means, stds = (np.atleast_1d(xx) for xx in defs)
            return pm.Normal('param_{}'.format(pid), mu=means, sd=stds, shape=len(means))
        else:
            # Uniform distribution
            return pm.Uniform('param_{}'.format(pid), shape=self.nparams)

class DirichletAllocationProcess:
    def __init__(self, name, outputs):
        assert len(outputs) >= 1
        self.name = name
        self.outputs = outputs
        self.nparams = len(outputs)

    @staticmethod
    def transfer_functions(params):
        return params

    @staticmethod
    def prior(shares, concentration=None, with_stddev=None):
        if (concentration is not None and with_stddev is not None) or \
           (concentration is None and with_stddev is None):
            raise ValueError('Specify either concentration or stddev')

        # normalise
        factor = sum(shares)
        shares = np.array(shares) / factor

        if with_stddev is not None:
            i, stddev = with_stddev
            stddev /= factor
            mi = shares[i]
            limit = np.sqrt(mi * (1 - mi) / (1 + len(shares)))
            if stddev > limit:
                raise ValueError('stddev is too high (%.2g > %.2g)' % (stddev, limit))
            concentration = mi * (1 - mi) / stddev**2 - 1
            if not np.isfinite(concentration):
                concentration = 1e10
        else:
            concentration = len(shares) * concentration

        return concentration * shares

    def param_rv(self, pid, defs):
        if defs is None:
            defs = np.ones(self.nparams)
        assert len(defs) == self.nparams
        if len(defs) > 1:
            return pm.Dirichlet('param_{}'.format(pid), defs)
        else:
            return pm.Deterministic('param_{}'.format(pid), T.ones((1,)))

class NormalisedUniformAllocationProcess:
    def __init__(self, name, outputs):
        assert len(outputs) >= 1
        self.name = name
        self.outputs = outputs
        self.nparams = len(outputs)

    @staticmethod
    def transfer_functions(params):
        return params

    def param_rv(self, pid, defs):
        if defs is not None:
            raise ValueError('no parameters')
        uniforms = pm.Uniform('param_{}'.format(pid), 0, 1, shape=self.nparams)
        result = uniforms / uniforms.sum()
        return result


class SymlogAllocationProcess:
    def __init__(self, name, outputs):
        assert len(outputs) >= 1
        self.name = name
        self.outputs = outputs
        self.nparams = len(outputs)

    def default_param_prior(self):
        # broad prior
        mean = np.zeros(self.nparams)
        std = 2.0 * np.ones(self.nparams)
        return mean, std

    @staticmethod
    def transfer_functions(params):
        x = T.exp(params)
        return x / x.sum()

    def param_rv(self, pid, defs):
        if defs:
            # Normal dist about given mean & sd
            means, stds = (np.atleast_1d(xx) for xx in defs)
            return pm.Normal('param_{}'.format(pid), mu=means, sd=stds, shape=len(means))
        else:
            # Uniform distribution
            return pm.Uniform('param_{}'.format(pid), shape=self.nparams)


class SoftmaxAllocationProcess:
    def __init__(self, name, outputs):
        assert len(outputs) >= 1
        self.name = name
        self.outputs = outputs
        self.nparams = len(outputs)

    def default_param_prior(self):
        # broad prior
        mean = np.zeros(self.nparams)
        std = 2.0 * np.ones(self.nparams)
        return mean, std

    @staticmethod
    def transfer_functions(params):
        return T.nnet.softmax(params)[0]

    def param_rv(self, pid, defs):
        if defs:
            # Normal dist about given mean & sd
            means, stds = (np.atleast_1d(xx) for xx in defs)
            return pm.Normal('param_{}'.format(pid), mu=means, sd=stds, shape=len(means))
        else:
            # Uniform distribution
            return pm.Uniform('param_{}'.format(pid), shape=self.nparams)


class SinkProcess:
    def __init__(self, name):
        self.name = name
        self.outputs = []
        self.nparams = 0

    @staticmethod
    def transfer_functions(params):
        return T.dvector()

    def param_rv(self, pid, defs):
        return None
