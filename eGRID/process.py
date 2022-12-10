import csv
import os
import sys

import pandas as pd
import numpy as np

_RAW_PATH = 'raw_data'
_IN_FILE = '/egrid2020_data.xlsx'
_OUT_FILE = '/egrid2020_data.csv'

# module_dir_ is the path to where this code is running from.
current_dir = os.path.dirname(__file__)

import utils

RAW_COLUMNS = [
    'Data Year',
    'Plant name',
    'DOE/EIA ORIS plant or facility code',
    'Plant transmission or distribution system owner name',
    'Plant transmission or distribution system owner ID',
    'Utility name',
    'Utility ID',
    'Plant-level sector',
    'Balancing Authority Name',
    'Balancing Authority Code',
    'NERC region acronym',
    'eGRID subregion acronym',
    'eGRID subregion name',
    'Plant associated ISO/RTO Territory ',
    'Plant FIPS state code',
    'Plant FIPS county code',
    'Plant county name',
    'Plant latitude',
    'Plant longitude',
    'Number of units',
    'Number of generators',
    'Plant primary fuel',
    'Plant primary fuel category',
    'Plant capacity factor',
    'Plant nameplate capacity (MW)',
    'Plant annual net generation (MWh)',
    'Plant annual NOx emissions (tons)',
    'Plant annual SO2 emissions (tons)',
    'Plant annual CO2 emissions (tons)',
    'Plant annual CH4 emissions (lbs)',
    'Plant annual N2O emissions (lbs)',
    'Plant annual CO2 equivalent emissions (tons)',
    'Plant annual NOx total output emission rate (lb/MWh)',
    'Plant ozone season NOx total output emission rate (lb/MWh)',
    'Plant annual SO2 total output emission rate (lb/MWh)',
    'Plant annual CO2 total output emission rate (lb/MWh)',
    'Plant annual CH4 total output emission rate (lb/MWh)',
    'Plant annual N2O total output emission rate (lb/MWh)',
    'Plant annual CO2 equivalent total output emission rate (lb/MWh)',
    'Plant annual coal net generation (MWh)',
    'Plant annual oil net generation (MWh)',
    'Plant annual gas net generation (MWh)',
    'Plant annual nuclear net generation (MWh)',
    'Plant annual hydro net generation (MWh)',
    'Plant annual biomass net generation (MWh)',
    'Plant annual wind net generation (MWh)',
    'Plant annual solar net generation (MWh)',
    'Plant annual geothermal net generation (MWh)',
    'Plant annual other fossil net generation (MWh)',
    'Plant annual other unknown/ purchased fuel net generation (MWh)',
    'Plant annual total nonrenewables net generation (MWh)',
    'Plant annual total renewables net generation (MWh)',
    'Plant annual total nonhydro renewables net generation (MWh)',
    'Plant annual total combustion net generation (MWh)',
    'Plant annual total noncombustion net generation (MWh)',
]

IMPORT_COLUMNS = [
    'Year', 'Name', 'Dcid', 'OwnerName', 'OwnerId', 'UtilityName',
    'UtilityDcid', 'PowerPlantSector', 'BalancingAuthorityName',
    'BalancingAuthorityCode', 'NERCRegionAcronym', 'eGRIDSubregionAcronym',
    'eGRIDSubregionName', 'PlantAssociatedISORTOTerritory', 'County',
    'CountyDcid', 'Latitude', 'Longitude', 'NumberOfUnits',
    'NumberOfGenerators', 'generatorTechnology', 'NAICSEnum',
    'PlantCapacityFactor', 'nameplateCapacity', 'plantAnnualNetGeneration',
    'plantAnnualNOxEmissions', 'plantAnnualSO2Emissions',
    'plantAnnualCO2Emissions', 'plantAnnualCH4Emissions',
    'plantAnnualN2OEmissions', 'plantAnnualCO2EquivalentEmissions',
    'plantAnnualNOxTypeTotalOutputEmissionRate',
    'plantAnnualOzoneSeasonNOxTotalOutputEmissionRate',
    'plantAnnualSO2TotalOutputEmissionRate',
    'plantAnnualCO2TotalOutputEmissionRate',
    'plantAnnualCH4TotalOutputEmissionRate',
    'plantAnnualN2OTotalOutputEmissionRate',
    'plantAnnualCO2EquivalentTotalOutputEmissionRate',
    'plantAnnualTotalCoalNetGeneration', 'plantAnnualTotalOilNetGeneration',
    'plantAnnualTotalGasNetGeneration', 'plantAnnualTotalNuclearNetGeneration',
    'plantAnnualTotalHydroNetGeneration',
    'plantAnnualTotalBiomassNetGeneration',
    'plantAnnualTotalWindNetGeneration', 'plantAnnualTotalSolarNetGeneration',
    'plantAnnualTotalGeothermalNetGeneration',
    'plantAnnualTotalOtherFossilNetGeneration',
    'plantAnnualTotalUnknownOrPurchasedFuelNetGeneration',
    'plantAnnualTotalNonrenewablesNetGeneration',
    'plantAnnualTotalRenewablesNetGeneration',
    'plantAnnualTotalNonhydroRenewablesNetGeneration',
    'plantAnnualTotalCombustionNetGeneration',
    'plantAnnualTotalNoncombustionNetGeneration'
]

SECTOR_CODE_ENUM = {
    'Electric Utility': 'dcid:EIA_ElectricUtility',
    'IPP Non-CHP': 'dcid:EIA_IndependentPowerProducer_NonCombinedHeatPower',
    'IPP CHP': 'dcid:EIA_IndependentPowerProducer_CombinedHeatPower',
    'Commercial Non-CHP': 'dcid:EIA_Commercial_NonCombinedHeatPower',
    'Commercial CHP': 'dcid:EIA_Commercial_CombinedHeatPower',
    'Industrial Non-CHP': 'dcid:EIA_Industrial_NonCombinedHeatPower',
    'Industrial CHP': 'dcid:EIA_Industrial_CombinedHeatPower',
}

ENERGY_SOURCE_ENUM = {
    'SUN': 'Solar',
    'NG': 'EIA_NaturalGas',
    'WAT': 'EIA_Water',
    'WND': 'EIA_Wind',
    'DFO': 'EIA_DistillateFuelOil',
    'LFG': 'MunicipalWaste',  ##
    'MWH': 'EnergyStorageBattery',  ##
    'BIT': 'EIA_BituminousCoal',
    'WDS': 'WoodAndWoodDerivedFuels',
    'SUB': 'EIA_SubbituminousCoal',
    'OBG': 'OtherBiomass',
    'GEO': 'Geothermal',
    'BLQ': 'BlackLiquor',  ##dcid:BlackLiquor
    'MSW': 'MunicipalWaste',  ##dcid: MunicipalWaste
    'NUC': 'Nuclear',
    'RC': 'EIA_RefinedCoal',
    'WH': 'Waste heat',  ##
    'RFO': 'EIA_ResidualFuelOil',
    'PRG': 'Process gas',  ##
    'KER': 'EIA_Kerosene',
    'OG': 'EIA_OtherGas',
    'WC': 'EIA_Waste_OtherCoal',
    'PC': 'EIA_PetroleumCoke',
    'LIG': 'EIA_LigniteCoal',
    'AB': 'AnimalWaste',  ##
    'OTH': 'OtherGases',  ##
    'PUR': 'OtherGases',  ##
    'WO': 'EIA_Waste_OtherOil',
    'BFG': 'EIA_BlastFurnaceGas',
    'COG': 'CokeOvenGas',  ##dcid: CokeOvenGas
    'OBS': 'OtherBiomass',  ##
    'WDL': 'WoodAndWoodDerivedFuels',  ####
    'OBL': 'OtherBiomass',  ##
    'JF': 'EIA_JetFuel',
    'SGC': 'EIA_CoalDerivedSynthesisGas',
    'PG': 'EIA_GaseousPropane'
}

ENERGY_SCOURCE_TYPE_ENUM = {
    'SOLAR': 'dcid: NAICS/221114',  #Solar electric power generation
    'GAS': 'dcid: NAICS/221112',
    'HYDRO': 'dcid: NAICS/221111',  #Hydroelectric power generation
    'WIND': 'dcid: NAICS/221115',  #Wind electric power generation
    'OIL': 'dcid: NAICS/221112',
    'BIOMASS': 'dcid: NAICS/221117',  #Biomass electric power generation
    'COAL': 'dcid: NAICS/221112',
    'OTHF': 'dcid: NAICS/221118',
    'GEOTHERMAL': 'dcid: NAICS/221116',  #Geothermal electric power generation
    'NUCLEAR': 'dcid: NAICS/221113',  #Nuclear electric power generation
    'OFSL': 'dcid: NAICS/221112'
}


def _to_enum(value, enum):
    dcid = enum.get(value, None)
    assert enum is not None, f'code "{value}" not found in {enum}'
    return dcid


def update_frame(df):
    df_new = pd.DataFrame()
    df = df.replace(np.nan, '')
    df_new['Year'] = df['Data Year'].astype(int)
    df_new['Name'] = df['Plant name'].apply(utils.name_convert)
    df_new['Dcid'] = df['DOE/EIA ORIS plant or facility code'].apply(
        utils.plant_code_to_dcid)
    df_new['OwnerName'] = df[
        'Plant transmission or distribution system owner name'].apply(
            utils.name_convert)
    df_new['OwnerId'] = df[
        'Plant transmission or distribution system owner ID'].apply(
            utils.plant_owner_id_to_dcid, prefix_dcid=True)
    df_new['UtilityName'] = df['Utility name'].apply(utils.name_convert)
    df_new['UtilityDcid'] = df['Utility ID'].apply(utils.utility_id_to_dcid,
                                                   prefix_dcid=True)
    df_new['PowerPlantSector'] = df['Plant-level sector'].apply(
        _to_enum, enum=SECTOR_CODE_ENUM)
    df_new['BalancingAuthorityName'] = df['Balancing Authority Name'].apply(
        utils.balancing_name_convert)
    df_new['BalancingAuthorityCode'] = df['Balancing Authority Code'].apply(
        utils.name_convert)
    df_new['NERCRegionAcronym'] = df['NERC region acronym'].apply(
        utils.name_convert)
    df_new['eGRIDSubregionAcronym'] = df['eGRID subregion acronym'].apply(
        utils.name_convert)
    df_new['eGRIDSubregionName'] = df['eGRID subregion name'].apply(
        utils.name_convert)
    df_new['PlantAssociatedISORTOTerritory'] = df[
        'Plant associated ISO/RTO Territory '].apply(utils.name_convert)
    utils.county_dcid(df)
    utils.county_name_from_dict(df)
    df_new['County'] = df['County']
    df_new['CountyDcid'] = df['CountyDcid'].apply(utils.count_dcid_prefix)
    df_new['Latitude'] = df['Plant latitude']
    df_new['Longitude'] = df['Plant longitude']
    df_new['NumberOfUnits'] = df['Number of units']
    df_new['NumberOfGenerators'] = df['Number of generators']
    df_new['generatorTechnology'] = df['Plant primary fuel'].apply(
        _to_enum, enum=ENERGY_SOURCE_ENUM)
    df_new['NAICSEnum'] = df['Plant primary fuel category'].apply(
        _to_enum, enum=ENERGY_SCOURCE_TYPE_ENUM)
    df_new['PlantCapacityFactor'] = df['Plant capacity factor']
    df_new['nameplateCapacity'] = df['Plant nameplate capacity (MW)']
    df_new['plantAnnualNetGeneration'] = df[
        'Plant annual net generation (MWh)']
    df_new['plantAnnualNOxEmissions'] = df['Plant annual NOx emissions (tons)']
    df_new['plantAnnualSO2Emissions'] = df['Plant annual SO2 emissions (tons)']
    df_new['plantAnnualCO2Emissions'] = df['Plant annual CO2 emissions (tons)']
    df_new['plantAnnualCH4Emissions'] = df['Plant annual CH4 emissions (lbs)']
    df_new['plantAnnualN2OEmissions'] = df['Plant annual N2O emissions (lbs)']
    df_new['plantAnnualCO2EquivalentEmissions'] = df[
        'Plant annual CO2 equivalent emissions (tons)']
    df_new['plantAnnualNOxTypeTotalOutputEmissionRate'] = df[
        'Plant annual NOx total output emission rate (lb/MWh)']
    df_new['plantAnnualOzoneSeasonNOxTotalOutputEmissionRate'] = df[
        'Plant ozone season NOx total output emission rate (lb/MWh)']
    df_new['plantAnnualSO2TotalOutputEmissionRate'] = df[
        'Plant annual SO2 total output emission rate (lb/MWh)']
    df_new['plantAnnualCO2TotalOutputEmissionRate'] = df[
        'Plant annual CO2 total output emission rate (lb/MWh)']
    df_new['plantAnnualCH4TotalOutputEmissionRate'] = df[
        'Plant annual CH4 total output emission rate (lb/MWh)']
    df_new['plantAnnualN2OTotalOutputEmissionRate'] = df[
        'Plant annual N2O total output emission rate (lb/MWh)']
    df_new['plantAnnualCO2EquivalentTotalOutputEmissionRate'] = df[
        'Plant annual CO2 equivalent total output emission rate (lb/MWh)']
    df_new['plantAnnualTotalCoalNetGeneration'] = df[
        'Plant annual coal net generation (MWh)']
    df_new['plantAnnualTotalOilNetGeneration'] = df[
        'Plant annual oil net generation (MWh)']
    df_new['plantAnnualTotalGasNetGeneration'] = df[
        'Plant annual gas net generation (MWh)']
    df_new['plantAnnualTotalNuclearNetGeneration'] = df[
        'Plant annual nuclear net generation (MWh)']
    df_new['plantAnnualTotalHydroNetGeneration'] = df[
        'Plant annual hydro net generation (MWh)']
    df_new['plantAnnualTotalBiomassNetGeneration'] = df[
        'Plant annual biomass net generation (MWh)']
    df_new['plantAnnualTotalWindNetGeneration'] = df[
        'Plant annual wind net generation (MWh)']
    df_new['plantAnnualTotalSolarNetGeneration'] = df[
        'Plant annual solar net generation (MWh)']
    df_new['plantAnnualTotalGeothermalNetGeneration'] = df[
        'Plant annual geothermal net generation (MWh)']
    df_new['plantAnnualTotalOtherFossilNetGeneration'] = df[
        'Plant annual other fossil net generation (MWh)']
    df_new['plantAnnualTotalUnknownOrPurchasedFuelNetGeneration'] = df[
        'Plant annual other unknown/ purchased fuel net generation (MWh)']
    df_new['plantAnnualTotalNonrenewablesNetGeneration'] = df[
        'Plant annual total nonrenewables net generation (MWh)']
    df_new['plantAnnualTotalRenewablesNetGeneration'] = df[
        'Plant annual total renewables net generation (MWh)']
    df_new['plantAnnualTotalNonhydroRenewablesNetGeneration'] = df[
        'Plant annual total nonhydro renewables net generation (MWh)']
    df_new['plantAnnualTotalCombustionNetGeneration'] = df[
        'Plant annual total combustion net generation (MWh)']
    df_new['plantAnnualTotalNoncombustionNetGeneration'] = df[
        'Plant annual total noncombustion net generation (MWh)']
    return df_new


def process(in_path, out_path):
    """Read data from excel and create CSV required for DC import"""
    raw_df = pd.read_excel(in_path,
                           sheet_name="PLNT20").drop(0).reset_index(drop=True)
    df_need = update_frame(raw_df)
    df_need.to_csv(out_path, columns=IMPORT_COLUMNS)


if __name__ == '__main__':
    in_path = os.path.join(current_dir, _RAW_PATH + _IN_FILE)
    out_path = os.path.join(current_dir, _RAW_PATH + _OUT_FILE)
    process(in_path, out_path)