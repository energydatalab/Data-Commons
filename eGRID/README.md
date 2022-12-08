# To Develop code for eGRID data ingestion
## Columns
- 'Data Year' -- 'Year'(int)
- 'Plant name' -- 'Name'(str)
- 'DOE/EIA ORIS plant or facility code' -- 'Dcid'
    (For the plant code, follow the `eia/pp/` format consistent with eia-860; however, there are some inconsistency. For examples: [AES Warrior Run Cogeneration Facility]{https://datacommons.org/browser/dc/0pm96qyg3x0wd} and [AES LAWAI SOLAR Hybrid]{https://datacommons.org/browser/eia/pp/61068}. The name of 'AES Warrior Run Cogeneration Facility' in the eGrid is just 'AES Warrior Run' and the dicd followed different format('dc/0pm96qyg3x0wd'), but it's `powerPlantCode` property is consistent with eGrid data. And the `owns` property of 'AES Warrior Run' is the 'Utility name' in eGrid data, and is the `isPartOf` property of the eia-860.(see AES LAWAI))
- 'Plant transmission or distribution system owner name' -- 'OwnerName' (new property)
- 'Plant transmission or distribution system owner ID' -- 'OwnerId' (new property with `egrid/owner/` format)
- 'Utility name' -- 'UtilityName'
- 'Utility ID' -- 'UtilityDcid' (`eia/u/` format, consistent with eia-860)
- 'Plant-level sector' -- 'powerPlantSector' (consistent with eia-860)
- 'Balancing Authority Name' -- 'BalancingAuthorityName' (new property)
- 'Balancing Authority Code' -- 'BalancingAuthorityCode' (new property, str )
- 'NERC region acronym' -- 'NERCRegionAcronym' (new property, str)
- 'eGRID subregion acronym' -- 'eGRIDSubregionAcronym' (new property, str)
- 'eGRID subregion name' -- 'eGRIDSubregionName' (new property)
- 'Plant associated ISO/RTO Territory ' -- 'PlantAssociatedISORTOTerritory' (new property, str)
- 'Plant county name' -- 'County' (add `CountyDcid`)
    (For the county generate Dcid based on the state and county FIPS, and then get the key from `county_to_dcid`(from [Data Commons repo]{https://github.com/datacommonsorg/data/blob/master/util/county_to_dcid.py}) as the County Name to match the existing name in Data Commons.)
- 'Plant latitude' -- 'Latitude'
- 'Plant longitude' -- 'Longitude'
- 'Number of units' -- 'NumberOfUnits' (new property)
- 'Number of generators' -- 'NumberOfGenerators' (new property)
- 'Plant primary fuel' -- 'generatorTechnology'
    (For each primary fuel, use [EnergySourceEnum]{https://datacommons.org/browser/EnergySourceEnum} and special case MWH use from [primeMover]{https://datacommons.org/browser/PrimeMoverEnum} as[EnergyStorageBattery]{https://datacommons.org/browser/EnergyStorageBattery}; )
- 'Plant primary fuel category' -- 'NAICSEnum' (use [NAICSEnum]{https://datacommons.org/browser/NAICSEnum})
- 'Plant capacity factor' -- 'PlantCapacityFactor' (new property)
- 'Plant nameplate capacity (MW)' -- 'nameplateCapacity'
    (However, eia-860 data don't have `nameplateCapacity` property, but other data do. For example: [AES Warrior Run Cogeneration Facility]{https://datacommons.org/browser/dc/hs2qdfn18lws2} as `PowerPlantUnit` do have `nameplateCapacity`.)
