import os

current_dir = os.path.dirname(__file__)

COLUMNS_TO_NAME = {
    'plantAnnualNOxEmissions': 'NOx',
    'plantAnnualSO2Emissions': 'SO2',
    'plantAnnualCO2Emissions': 'CO2',
    'plantAnnualCH4Emissions': 'CH4',
    'plantAnnualN2OEmissions': 'N20',
    'plantAnnualCO2EquivalentEmissions': 'CO2Equivalent'
}

GAS_MCF_TEMPLATE = """
Node: dcid:{gas_dcid}
typeOf: dcs:GreenhouseGas
name: "{gas_name}"
"""

SV_MCF_TEMPLATE = """
Node: dcid:{sv_dcid}
typeOf: dcs:StatisticalVariable
populationType: dcs:Emissions
measuredProperty: dcs:amount
statType: dcs:measuredValue
measurementQualifier: dcs:Annual
emittedThing: dcs:{gas_dcid}
rangeIncludes: Quantity
"""


def is_gas_col(col):
    return col.strip() in COLUMNS_TO_NAME


def col_to_dcid(col):
    return COLUMNS_TO_NAME[col]


def append_gas_mcf(fp):
    for gas_col, gas_name in COLUMNS_TO_NAME.items():
        if not gas_name:
            continue
        fp.write(
            GAS_MCF_TEMPLATE.format(gas_dcid=col_to_dcid(gas_col),
                                    gas_name=gas_name))


def col_to_sv(col):
    if not is_gas_col(col):
        return None
    sv_dcid = col.strip()
    return f'{sv_dcid}'


def append_sv_mcf(fp):
    for col, name in COLUMNS_TO_NAME.items():
        sv_dcid = col_to_sv(col)
        if name:
            gas_dcid = col_to_dcid(col)
        fp.write(SV_MCF_TEMPLATE.format(sv_dcid=sv_dcid, gas_dcid=gas_dcid))


if __name__ == '__main__':
    with open(os.path.join(current_dir, 'mcf_tmcf/gas_node.mcf'), 'w') as fp:
        append_gas_mcf(fp)
    with open(os.path.join(current_dir, 'mcf_tmcf/gas_sv.mcf'), 'w') as fp:
        append_sv_mcf(fp)