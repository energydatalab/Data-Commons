import os
import sys

import numpy as np
import pandas as pd
import pandas.api.types as pd_types

# current_dir is the path to where this code is running from.
current_dir = os.path.dirname(__file__)

# For import util.county_to_dcid
import county_to_dcid


def name_convert(value):
    if value == '':
        return ''
    return f'\"{value}\"'


def code_to_str(code):
    if pd_types.is_number(code):
        # Specify 0 decimal places in the float->str conversion
        return f'{code:.0f}'
    return code


def plant_code_to_dcid(plant_code):
    return f'eia/pp/{code_to_str(plant_code)}'


def plant_owner_id_to_dcid(plant_owner_id, prefix_dcid=False):
    dcid = f'eia/u/{code_to_str(plant_owner_id)}'
    if prefix_dcid:
        return f'dcid:{dcid}'
    return dcid


def utility_id_to_dcid(utility_id, prefix_dcid=False):
    dcid = f'eia/u/{code_to_str(utility_id)}'
    if prefix_dcid:
        return f'dcid:{dcid}'
    return dcid


# Balancing Authority Name
def balancing_name_convert(bal_name):
    if bal_name == 'No balancing authority':
        bal_name = ''
    return name_convert(bal_name)


def county_dcid(df):
    for i, countyfips in enumerate(df['Plant FIPS county code']):
        if countyfips == '':
            df.at[i, 'CountyDcid'] = ''
        else:
            statefips = df.loc[i]['Plant FIPS state code']
            df.at[i, 'CountyDcid'] = 'geoId/' + statefips + countyfips
    return df


def count_dcid_prefix(countydcid):
    if countydcid == '':
        return ''
    else:
        return 'dcid:' + countydcid


def county_name_from_dict(df):
    for i, countydcid in enumerate(df['CountyDcid']):
        for k, v in county_to_dcid.COUNTY_MAP.items():
            for name, id in v.items():
                if id == countydcid:
                    df.at[i, 'County'] = name
    return df
