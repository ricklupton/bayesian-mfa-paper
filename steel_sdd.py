"""Sankey diagram definition for simple steel model"""

import attr

from floweaver import ProcessGroup, Waypoint, Bundle, Elsewhere, SankeyDefinition, Partition

def diagram():
    nodes = {
        'BF': ProcessGroup(selection=['BF', 'PI']),
        'CCBM': ProcessGroup(selection=['CCBM', 'CCBML', 'bloom']),
        'CCBT': ProcessGroup(selection=['CCBT', 'CCBTL', 'billet']),
        'CCS': ProcessGroup(selection=['CCS', 'CCSL', 'slab']),
        'CRM': ProcessGroup(selection=['CRM', 'CRMP']),
        'DR': ProcessGroup(selection=['DR', 'DRI']),
        'EAF': ProcessGroup(selection=['EAF', 'EAFS']),
        'GP': ProcessGroup(selection=['GP_CR', 'GP_HR', 'GPP_CR']),
        'HSM': ProcessGroup(selection=['HSM', 'HSML', 'HSMP']),
        'IC': ProcessGroup(selection=['IC', 'ICL', 'ingots']),
        'IFC': ProcessGroup(selection=['IFC', 'IFCL']),
        'OBF': ProcessGroup(selection=['OBF', 'OBFS']),
        'OCP': ProcessGroup(selection=['OCP']),
        'OHF': ProcessGroup(selection=['OHF', 'OHFS']),
        'PLM': ProcessGroup(selection=['PLM', 'PLML', 'PLMP']),
        'PRM': ProcessGroup(selection=['PRM', 'PRML', 'PRMP']),
        'RBM': ProcessGroup(selection=['RBM', 'RBML', 'RBMP']),
        'SEM': ProcessGroup(selection=['SEM', 'SEML', 'SEMP']),
        'SP': ProcessGroup(selection=['SP', 'S']),
        'SPC': ProcessGroup(selection=['SPC', 'SPCL']),
        'STP': ProcessGroup(selection=['STP']),
        'TM': ProcessGroup(selection=['TM']),
        'TWP': ProcessGroup(selection=['TWP']),
        'crc': ProcessGroup(selection=['crc']),
        'crccoated': ProcessGroup(selection=['crccoated']),
        'crcgalv': ProcessGroup(selection=['crcgalv']),
        'crctinned': ProcessGroup(selection=['crctinned']),
        'elsheet': ProcessGroup(selection=['elsheet']),
        'hrc': ProcessGroup(selection=['hrc']),
        'hrcgalv': ProcessGroup(selection=['hrcgalv']),
        'hrns': ProcessGroup(selection=['hrns']),
        'plate': ProcessGroup(selection=['plate']),
        'rodbar': ProcessGroup(selection=['rodbar']),
        'rodrebar': ProcessGroup(selection=['rodrebar']),
        'rodwire': ProcessGroup(selection=['rodwire']),
        'seamlesstube': ProcessGroup(selection=['seamlesstube']),
        'secheavy': ProcessGroup(selection=['secheavy']),
        'seclight': ProcessGroup(selection=['seclight']),
        'secrail': ProcessGroup(selection=['secrail']),
        'weldedtube': ProcessGroup(selection=['weldedtube']),
        'castiron': ProcessGroup(selection=['castiron']),
        'caststeel': ProcessGroup(selection=['caststeel']),
        'loss1': Waypoint(title=''),
        'loss2': Waypoint(title=''),
        'loss3': Waypoint(title=''),
        'loss4': Waypoint(title=''),
        'loss5': Waypoint(title=''),
        'scrap1': Waypoint(title='', direction='L'),
        'scrap2': Waypoint(title='', direction='L'),
        'scrap3': Waypoint(title='', direction='L'),
        'scrap4': Waypoint(title='', direction='L'),
        'scrap5': Waypoint(title='', direction='L'),
        'scrap6': Waypoint(title='', direction='L'),

        'sections': Waypoint(),
        'rods': Waypoint(),
        'tubes': Waypoint(),
        'cr': Waypoint(title=''),
        'hr1': Waypoint(title=''),
        'hr2': Waypoint(title=''),
        'pi2casting': Waypoint(title=''),
        'slab': Waypoint(title=''),
        'billet': Waypoint(title=''),
        'bloom': Waypoint(title=''),
    }

    bundles = [
        Bundle('BF', 'OBF'),
        Bundle('BF', 'OHF'),
        Bundle('BF', 'EAF'),
        Bundle('BF', 'IFC', waypoints=('pi2casting',)),
        Bundle('DR', 'EAF'),

        Bundle('OBF', 'CCS'),
        Bundle('OBF', 'CCBT'),
        Bundle('OBF', 'CCBM'),
        Bundle('OBF', 'IC'),
        Bundle('OHF', 'IC'),
        Bundle('EAF', 'CCBT'),
        Bundle('EAF', 'CCBM'),
        Bundle('EAF', 'IC'),
        Bundle('EAF', 'SPC'),

        Bundle('CCBM', 'SEM', waypoints=('bloom',)),
        Bundle('CCBM', 'SP', waypoints=('scrap1',)),
        Bundle('CCBM', 'CCBM', flow_selection='source == "CCBML" and target == "CCBM"'),
        Bundle('CCBT', 'HSM', waypoints=('billet',)),
        Bundle('CCBT', 'RBM', waypoints=('billet',)),
        Bundle('CCBT', 'CCBT', flow_selection='source == "CCBTL" and target == "CCBT"'),
        Bundle('CCBT', 'SP', waypoints=('scrap1',)),
        Bundle('CCS', 'HSM', waypoints=('slab',)),
        Bundle('CCS', 'PLM', waypoints=('slab',)),
        Bundle('CCS', 'CCS', flow_selection='source == "CCSL" and target == "CCS"'),
        Bundle('CCS', 'SP', waypoints=('scrap1',)),
        Bundle('IC', 'IC', flow_selection='source == "ICL" and target == "IC"'),
        Bundle('IC', 'PRM'),
        Bundle('IC', 'SPC'),
        Bundle('SPC', 'SPC', flow_selection='source == "SPCL" and target == "SPC"'),
        Bundle('IFC', 'IFC', flow_selection='source == "IFCL" and target == "IFC"'),
        Bundle('SPC', 'caststeel'),
        Bundle('IFC', 'castiron'),

        Bundle('PRM', 'SP', waypoints=('scrap2', 'scrap1')),
        Bundle('PRM', 'SEM'),
        Bundle('PRM', 'RBM'),
        Bundle('PRM', 'PLM'),
        Bundle('PRM', 'HSM'),

        Bundle('HSM', 'SP', waypoints=('scrap3', 'scrap2', 'scrap1')),
        Bundle('HSM', 'TWP'),
        Bundle('HSM', 'CRM'),
        Bundle('HSM', 'GP'),
        Bundle('HSM', 'hrc', waypoints=('hr1', 'hr2')),
        Bundle('HSM', 'hrns', waypoints=('hr1', 'hr2')),
        Bundle('PLM', 'SP', waypoints=('scrap3', 'scrap2', 'scrap1')),
        Bundle('PLM', 'TWP'),
        Bundle('PLM', 'plate'),
        Bundle('RBM', 'SP', waypoints=('scrap3', 'scrap2', 'scrap1')),
        Bundle('RBM', 'STP'),
        Bundle('RBM', 'rodrebar', waypoints=('rods',)),
        Bundle('RBM', 'rodwire', waypoints=('rods',)),
        Bundle('RBM', 'rodbar', waypoints=('rods',)),
        Bundle('SEM', 'SP', waypoints=('scrap3', 'scrap2', 'scrap1')),
        Bundle('SEM', 'secheavy', waypoints=('sections',)),
        Bundle('SEM', 'seclight', waypoints=('sections',)),
        Bundle('SEM', 'secrail', waypoints=('sections',)),

        Bundle('CRM', 'SP', waypoints=('scrap4', 'scrap3', 'scrap2', 'scrap1')),
        Bundle('CRM', 'elsheet', waypoints=('cr',)),
        Bundle('CRM', 'crc', waypoints=('cr',)),
        Bundle('CRM', 'GP'),
        Bundle('CRM', 'TM'),

        Bundle('STP', 'seamlesstube', waypoints=('tubes',)),
        Bundle('STP', 'SP', waypoints=('scrap4', 'scrap3', 'scrap2', 'scrap1')),
        Bundle('TWP', 'weldedtube', waypoints=('tubes',)),
        Bundle('TWP', 'SP', waypoints=('scrap4', 'scrap3', 'scrap2', 'scrap1')),

        Bundle('TM', 'crctinned'),
        Bundle('TM', 'SP', waypoints=('scrap5', 'scrap4', 'scrap3', 'scrap2', 'scrap1')),
        Bundle('GP', 'crcgalv'),
        Bundle('GP', 'OCP'),
        Bundle('GP', 'hrcgalv'),
        Bundle('GP', 'SP', waypoints=('scrap5', 'scrap4', 'scrap3', 'scrap2', 'scrap1')),
        Bundle('OCP', 'crccoated'),
        Bundle('OCP', 'SP', waypoints=('scrap6', 'scrap5', 'scrap4', 'scrap3', 'scrap2', 'scrap1')),

        Bundle('SP', 'OBF'),
        Bundle('SP', 'EAF'),

        Bundle('BF', Elsewhere, waypoints=('loss1',)),
        Bundle('DR', Elsewhere, waypoints=('loss1',)),
        Bundle('SP', Elsewhere, waypoints=('loss1',)),
        Bundle('OBF', Elsewhere, waypoints=('loss2',)),
        Bundle('OHF', Elsewhere, waypoints=('loss2',)),
        Bundle('EAF', Elsewhere, waypoints=('loss2',)),
        Bundle('CCS', Elsewhere, waypoints=('loss3',)),
        Bundle('IC', Elsewhere, waypoints=('loss3',)),
        Bundle('CCBT', Elsewhere, waypoints=('loss3',)),
        Bundle('CCBM', Elsewhere, waypoints=('loss3',)),
        Bundle('SPC', Elsewhere, waypoints=('loss4',)),
        Bundle('IFC', Elsewhere, waypoints=('loss4',)),
        Bundle('PRM', Elsewhere, waypoints=('loss4',)),
        Bundle('SEM', Elsewhere, waypoints=('loss5',)),
        Bundle('RBM', Elsewhere, waypoints=('loss5',)),
        Bundle('PLM', Elsewhere, waypoints=('loss5',)),
        Bundle('HSM', Elsewhere, waypoints=('loss5',)),
    ]

    ordering = [
        # [['inputs'], [], []],
        [['BF', 'DR', 'SP'], [], []],
        [['OBF', 'OHF', 'EAF', 'pi2casting'], ['loss1'], []],
        [['CCS', 'IC', 'CCBT', 'CCBM'], ['loss2'], ['scrap1']],
        [['slab', 'PRM', 'billet', 'bloom', 'SPC', 'IFC'], ['loss3'], ['scrap2']],
        [['HSM', 'PLM', 'RBM', 'SEM'], ['loss4'], ['scrap3']],
        [['CRM', 'hr1', 'TWP', 'STP'], ['loss5'], ['scrap4']],
        [['GP', 'TM', 'cr'], [], ['scrap5']],
        [['OCP', 'hr2', 'tubes', 'rods', 'sections'], [], ['scrap6']],
        [['hrcgalv', 'crcgalv', 'crccoated', 'crctinned', 'crc', 'elsheet', 'hrc', 'hrns',
          'plate', 'weldedtube', 'seamlesstube', 'rodrebar', 'rodwire', 'rodbar',
          'secrail', 'seclight', 'secheavy', 'caststeel', 'castiron'], [], []],
    ]

    flow_partition = Partition.Simple('target', ['SP', 'L'])

    sdd = SankeyDefinition(nodes, bundles, ordering, flow_partition=flow_partition)

    return sdd


def diagram_with_stocks(processes):
    bundle_ids = [
        (pid, [x for x in process.outputs if x != 'L'])
         for pid, process in processes.items()
    ]
    # bundle_ids = [('CCBM', ['CCBM', 'SM', 'SP']),
    #               ('DR', ['DRI']),
    #               ('DRI', ['EAF']),
    #               ('OBF', ['OBFS']),
    #               ('OBFS', ['CCS', 'CCBM', 'CCBT', 'IC']),
    #               ('PRM', ['HSM', 'RBM', 'SP', 'SM', 'PLM']),
    #               ('BF', ['PI']),
    #               ('PI', ['OBF', 'IFC', 'EAF', 'OHF']),
    #               ('IC', ['PRM', 'SPC', 'SP', 'IC']),
    #               ('CCS', ['HSM', 'CCS', 'SP', 'PLM']),
    #               ('CCBT', ['HSM', 'RBM', 'SP', 'CCBT']),
    #               ('SP', ['S']),
    #               ('S', ['OBF', 'EAF']),
    #               ('EAF', ['EAFS']),
    #               ('EAFS', ['CCBM', 'CCBT', 'SPC', 'IC']),
    #               ('OHF', ['OHFS']),
    #               ('OHFS', ['IC']),
    # ]

    process_ids = tuple(processes.keys())
    # process_ids = ('BF', 'DR', 'DRI', 'PI', 'SP', 'S', 'OBF', 'OBFS', 'OHF', 'OHFS', 'EAF', 'EAFS', 'CCS', 'CCBT', 'CCBM',
    #             'IC', 'SPC', 'IFC', 'PRM', 'HSM', 'PLM', 'RBM', 'SM', 'L')

    possible_input_ids = ['BF', 'DR', 'SP']

    extra_processes = {
        # 'OBF': ['OBFS'],
        # 'OHF': ['OHFS'],
        # 'EAF': ['EAFS'],
    }

    nodes = {k: ProcessGroup([k] + extra_processes.get(k, []))
             for k in process_ids if k != 'L'}
    nodes['scrap1'] = Waypoint(direction='L')
    nodes['scrap2'] = Waypoint(direction='L')
    nodes['scrap3'] = Waypoint(direction='L')
    nodes['scrap4'] = Waypoint(direction='L')
    nodes['scrap5'] = Waypoint(direction='L')
    nodes['scrap6'] = Waypoint(direction='L')
    nodes['loss1'] = Waypoint(direction='R')
    nodes['loss2'] = Waypoint(direction='R')
    nodes['loss3'] = Waypoint(direction='R')
    nodes['loss4'] = Waypoint(direction='R')

    bundles = [
        Bundle(k, k2) for k, dests in bundle_ids for k2 in dests
    ] + [
    #     Bundle('inputs', k) for k in possible_input_ids
    # ] + [
        Bundle(x, Elsewhere, waypoints=('loss1', ), ) for x in ['BF', 'DR', 'SP']
    ] + [
        Bundle(x, Elsewhere, waypoints=('loss2', ))
        for x in ['OBF', 'OHF', 'EAF']
    ] + [
        Bundle(x, Elsewhere, waypoints=('loss3', ))
        for x in ['CCSL', 'ICL', 'CCBTL', 'CCBML', 'SPC', 'IFC']
    ] + [
        Bundle(x, Elsewhere, waypoints=('loss4', )) for x in ['PRML']
    ]

    ordering = [
        # [['inputs'], [], []],
        [['BF', 'DR', 'SP'], [], []],
        [['PI', 'DRI', 'S'], ['loss1'], []],
        [['OBF', 'OHF', 'EAF'], [], []],
        [['OBFS', 'OHFS', 'EAFS'], ['loss2'], []],
        [['IFC', 'CCS', 'IC', 'CCBT', 'CCBM'], [], []],
        [['IFCL', 'slab', 'CCSL', 'ingots', 'ICL', 'billet', 'CCBTL', 'bloom', 'CCBML'], [], ['scrap1']],
        [['PRM', 'SPC'], ['loss3'], []],
        [['PRMP', 'PRML', 'SPCL'], [], ['scrap2']],
        [['HSM', 'PLM', 'RBM', 'SEM'], ['loss4'], []],
        [['HSMP', 'HSML', 'PLMP', 'PLML', 'RBMP', 'RBML', 'SEMP', 'SEML'], [], ['scrap3']],
        [['CRM', 'TWP', 'STP'], [], ['scrap4']],
        [['CRMP'], [], []],
        [['GP_HR', 'GP_CR', 'TM'], [], ['scrap5']],
        [['OCP', 'GPP_CR'], [], ['scrap6']],
        [['crc', 'crccoated', 'crcgalv', 'crctinned', 'elsheet', 'hrcgalv', 'hrc', 'hrns',
          'plate', 'weldedtube', 'seamlesstube', 'rodrebar', 'rodwire', 'rodbar',
          'secrail', 'seclight', 'secheavy', 'caststeel', 'castiron'], [], []],
    ]

    bundles = [
        attr.assoc(b, waypoints=('scrap1', ))
        if b.target == 'SP' and b.source in ordering[5][0] else b for b in bundles
    ]
    bundles = [
        attr.assoc(b, waypoints=('scrap2', 'scrap1'))
        if b.target == 'SP' and b.source in ordering[7][0] else b for b in bundles
    ]
    bundles = [
        attr.assoc(b, waypoints=('scrap3', 'scrap2', 'scrap1'))
        if b.target == 'SP' and b.source in ordering[9][0] else b for b in bundles
    ]
    bundles = [
        attr.assoc(b, waypoints=('scrap4', 'scrap3', 'scrap2', 'scrap1'))
        if b.target == 'SP' and b.source in ordering[10][0] else b for b in bundles
    ]
    bundles = [
        attr.assoc(b, waypoints=('scrap5', 'scrap4', 'scrap3', 'scrap2', 'scrap1'))
        if b.target == 'SP' and b.source in ordering[12][0] else b for b in bundles
    ]
    bundles = [
        attr.assoc(b, waypoints=('scrap6', 'scrap5', 'scrap4', 'scrap3', 'scrap2', 'scrap1'))
        if b.target == 'SP' and b.source in ordering[13][0] else b for b in bundles
    ]

    sdd = SankeyDefinition(nodes, bundles, ordering)

    return sdd

# from steel_processes_theano_full2 import define_processes
# processes = define_processes()

sdd = diagram()
# sdd_with_stocks = diagram_with_stocks(processes)
