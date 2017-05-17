import numpy as np

from leontief_model import DirichletAllocationProcess
dir_prior = DirichletAllocationProcess.prior


def logit(x):
    return -np.log(1/x - 1)


def logit_range_sd(a, b):
    return (logit(b) - logit (a)) / 4


param_defs = {
    ##### REDUCTION & SCRAP
    'BF':    (logit(0.993), logit_range_sd(0.99, 0.998)),  # BF eff -- Cullen flow [4]
    'DR':    (logit(0.993), logit_range_sd(0.99, 0.998)),  # DR eff -- Cullen flow [1] (assumes equal to BF eff)
    'SP':    (logit(0.85), logit_range_sd(0.75, 0.9)),     # SP eff -- ????

    ##### STEELMAKING
    'OBF':   (logit(0.871), logit_range_sd(0.80, 0.90)),   # OBF eff -- Cullen flow [16] -- range made up, could do better
    'OHF':   (logit(0.871), logit_range_sd(0.80, 0.90)),   # OHF eff -- Cullen flow [20] (same as OBF [16])
                'EAF':   (logit(0.889), logit_range_sd(0.86, 0.96)),   # EAF eff -- Cullen flow [13], range 86%-96%, centre 88.9%

    ##### CASTING
    'CCBM':  (logit(0.955), logit_range_sd(0.93, 0.98)),   # CCBM eff -- Cullen flow [28] -- range made up
    'CCBT':  (logit(0.975), logit_range_sd(0.96, 0.99)),   # CCBT eff -- Cullen flow [34] -- range made up
    'CCS':   (logit(0.965), logit_range_sd(0.955, 0.985)), # CCS eff -- Cullen flow [39] -- range made up
    'CCBML': dir_prior([13, 16, 71], with_stddev=(2, 10)), # CCBML alloc (L, SP, CCBM) -- Cullen flows [30-32] -- range made up
    'CCBTL': dir_prior([13, 16, 71], with_stddev=(2, 10)), # CCBTL alloc (L, SP, CCBT) -- Cullen flows [36-38], same as [30-32]
    'CCSL':  dir_prior([13, 16, 71], with_stddev=(2, 10)), # CCSL alloc (L, SP, CCS) -- Cullen flows [41-43], same as [30-32]
    'IC':    (logit(0.98), logit_range_sd(0.97, 0.99)),    # IC eff -- Cullen flow [44] -- range made up
    'ICL':   dir_prior([25, 75], with_stddev=(0, 20)),     # ICL alloc (L, IC) -- Cullen flows [47-48] -- range made up

    'PRM':   (logit(0.925), logit_range_sd(0.915, 0.935)), # PRM eff -- Cullen flow [61] -- range?
    'PRML':  dir_prior([1, 99], with_stddev=(0, 5)),       # PRML alloc (L, SP) -- Cullen flows [62-63]

    'IFC':   (logit(0.66), logit_range_sd(0.64, 0.68)),    # IFC eff -- Cullen flow [56] -- range made up
    'IFCL':  dir_prior([25, 75], with_stddev=(0, 20)),     # same as ICL -- Cullen flow [58]
    'SPC':   (logit(0.522), logit_range_sd(0.50, 0.54)),   # SPC eff -- Cullen flow [52] -- range made up
    'SPCL':  dir_prior([25, 75], with_stddev=(0, 20)),     # same as ICL -- Cullen flow [53]

    ##### ROLLING

    'SEM':   (logit(0.90), logit_range_sd(0.88, 0.92)),    # SEM yield -- Cullen flow [29] -- range made up
    'SEML':  dir_prior([1.5, 98.5], with_stddev=(0, 5)),   # SEML alloc (L, SP) -- Cullen flow [67]

    'RBM':   (logit(0.94), logit_range_sd(0.80, 0.96)),    # RBM yield -- solved by Cullen [68] as 94%. Unlikely to be 97%.
    'RBML':  dir_prior([1.5, 98.5], with_stddev=(0, 5)),   # RBML alloc (L, SP) -- Cullen flow [72]

    'PLM':   (logit(0.90), logit_range_sd(0.88, 0.92)),    # PLM yield -- Cullen flow [73] -- range made up
    'PLML':  dir_prior([1.15, 98.85], with_stddev=(0, 5)), # PLML alloc (L, SP) -- Cullen flow [77]

    'HSM':   (logit(0.96), logit_range_sd(0.94, 0.97)),    # HSM yield -- Cullen flow [78] (solved) -- range made up
    'HSML':  dir_prior([1, 99], with_stddev=(0, 5)),       # HSML alloc (L, SP) -- Cullen flow [83]

    ##### OTHER

    'STP':   (logit(0.90), logit_range_sd(0.80, 0.99)),    # STP yield -- Cullen solved [84] -- broad range made up
    'TWP':   (logit(0.90), logit_range_sd(0.80, 0.98)),    # TWP yield -- Cullen solved [87] -- broad range made up
    'CRM':   (logit(0.951), logit_range_sd(0.94, 0.96)),   # CRM yield -- Cullen flow [91] -- narrow range made up
    'GP_HR': (logit(0.975), logit_range_sd(0.97, 0.98)),   # GP_HR yield -- Cullen flow [94] -- narrow range made up
    'GP_CR': (logit(0.975), logit_range_sd(0.97, 0.98)),   # GP_HR yield -- Cullen flow [94] -- narrow range made up
    'TM':    (logit(0.935), logit_range_sd(0.93, 0.94)),   # TM yield -- Cullen flow [99] -- narrow range made up
    'OCP':   (logit(0.980), logit_range_sd(0.97, 0.99)),   # OCP yield -- Cullen flow [102] -- narrow range made up
}
