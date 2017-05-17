"""
Steel model definition.
"""

from collections import OrderedDict


from leontief_model import (
    EfficiencyProcess,
    DirichletAllocationProcess as AllocationProcess,
    SinkProcess
)


def define_processes():

    # pylint: disable=unused-variable,invalid-name

    BF = EfficiencyProcess('Blast furnace', ['PI', 'L'])
    PI = AllocationProcess('Pig iron', ['OBF', 'OHF', 'EAF', 'IFC'])

    DR = EfficiencyProcess('Direct reduction', ['DRI', 'L'])
    DRI = AllocationProcess('Direct reduced iron', ['EAF'])

    SP = EfficiencyProcess('Scrap preparation', ['S', 'L'])
    S = AllocationProcess('Scrap', ['OBF', 'EAF'])

    L = SinkProcess('Loss')

    OBF = EfficiencyProcess('Oxygen blown furnace', ['OBFS', 'L'])
    OBFS = AllocationProcess('Oxygen blown furnace steel', ['CCS', 'CCBT', 'CCBM', 'IC'])

    OHF = EfficiencyProcess('Open hearth furnace', ['OHFS', 'L'])
    OHFS = AllocationProcess('Open hearth furnace steel', ['IC'])

    EAF = EfficiencyProcess('Electric arc furnace', ['EAFS', 'L'])
    EAFS = AllocationProcess('Electric arc furnace steel', ['CCBT', 'CCBM', 'IC', 'SPC'])

    IFC = EfficiencyProcess('Foundry iron casting', ['castiron', 'IFCL'])
    IFCL = AllocationProcess('Foundry iron casting loss/scrap', ['L', 'IFC'])

    SPC = EfficiencyProcess('Steel product casting', ['caststeel', 'SPCL'])
    SPCL = AllocationProcess('Steel product casting loss/scrap', ['L', 'SPC'])

    IC = EfficiencyProcess('Ingot casting', ['ingots', 'ICL'])
    ingots = AllocationProcess('Ingots', ['PRM', 'SPC'])
    ICL = AllocationProcess('Ingot casting loss/scrap', ['L', 'IC'])

    CCS = EfficiencyProcess('CC slab', ['slab', 'CCSL'])
    slab = AllocationProcess('Slab', ['HSM', 'PLM'])
    CCSL = AllocationProcess('CC slab loss/scrap', ['L', 'SP', 'CCS'])

    CCBT = EfficiencyProcess('CC billet', ['billet', 'CCBTL'])
    billet = AllocationProcess('Billet', ['HSM', 'RBM'])
    CCBTL = AllocationProcess('CC billet loss/scrap', ['L', 'SP', 'CCBT'])

    CCBM = EfficiencyProcess('CC bloom', ['bloom', 'CCBML'])
    bloom = AllocationProcess('Bloom', ['SEM'])
    CCBML = AllocationProcess('CC bloom loss/scrap', ['L', 'SP', 'CCBM'])

    PRM = EfficiencyProcess('Primary mill', ['PRMP', 'PRML'])
    PRMP = AllocationProcess('Primary mill products', ['SEM', 'RBM', 'PLM', 'HSM'])
    PRML = AllocationProcess('Primary mill loss/scrap', ['L', 'SP'])

    SEM = EfficiencyProcess('Section mill', ['SEMP', 'SEML'])
    SEMP = AllocationProcess('Section mill products', ['secheavy', 'seclight', 'secrail'])
    SEML = AllocationProcess('Section mill loss/scrap', ['L', 'SP'])

    RBM = EfficiencyProcess('Rod/bar mill', ['RBMP', 'RBML'])
    RBMP = AllocationProcess('Rod/bar mill products', ['STP', 'rodrebar', 'rodwire', 'rodbar'])
    RBML = AllocationProcess('Rod/bar mill loss/scrap', ['L', 'SP'])

    PLM = EfficiencyProcess('Plate mill', ['PLMP', 'PLML'])
    PLMP = AllocationProcess('Plate mill products', ['TWP', 'plate'])
    PLML = AllocationProcess('Plate mill loss/scrap', ['L', 'SP'])

    HSM = EfficiencyProcess('Hot strip mill', ['HSMP', 'HSML'])
    HSMP = AllocationProcess('Hot strip mill products', ['TWP', 'CRM', 'GP_HR', 'hrc', 'hrns'])
    HSML = AllocationProcess('Hot strip mill loss/scrap', ['L', 'SP'])

    STP = EfficiencyProcess('Seamless tube plant', ['seamlesstube', 'SP'])
    TWP = EfficiencyProcess('Tube welding plant', ['weldedtube', 'SP'])

    CRM = EfficiencyProcess('Cold rolling mill', ['CRMP', 'SP'])
    CRMP = AllocationProcess('Cold rolling mill products', ['elsheet', 'crc', 'GP_CR', 'TM'])

    GP_HR = EfficiencyProcess('Galvanising plant (HR)', ['hrcgalv', 'SP'])
    GP_CR = EfficiencyProcess('Galvanising plant (CR)', ['GPP_CR', 'SP'])
    GPP_CR = AllocationProcess('Galvanising (CR) products', ['crcgalv', 'OCP'])

    TM = EfficiencyProcess('Tinmill', ['crctinned', 'SP'])

    OCP = EfficiencyProcess('Organic coating plant', ['crccoated', 'SP'])

    secheavy = SinkProcess('Sections (heavy)')
    seclight = SinkProcess('Sections (light)')
    secrail = SinkProcess('Sections (rail)')
    rodrebar = SinkProcess('Rebar')
    rodwire = SinkProcess('Wire rod')
    rodbar = SinkProcess('HR bar')
    plate = SinkProcess('Plate')
    hrc = SinkProcess('HR coil')
    hrns = SinkProcess('HR narrow strip')
    seamlesstube = SinkProcess('Seamless tube')
    weldedtube = SinkProcess('Welded tube')
    elsheet = SinkProcess('Electical sheet')
    crc = SinkProcess('Cold rolled coil')
    crcgalv = SinkProcess('CRC galvanised')
    crctinned = SinkProcess('CRC tinned')
    crccoated = SinkProcess('CRC coated')
    hrcgalv = SinkProcess('HRC galvanised')

    castiron = SinkProcess('Cast iron')
    caststeel = SinkProcess('Cast steel')

    return OrderedDict((pid, process)
                       for pid, process in sorted(locals().items()))
