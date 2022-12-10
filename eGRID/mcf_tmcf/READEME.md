#### To get the mcf file. Run `python mcf_template` at upper level dir.
#### PS:
- The format for the gas_node can be changed in `GAS_MCF_TEMPLATE`
- The format for the gas_sv can be changed in `SV_MCF_TEMPLATE`
- Need to talk with Data Commons team about the exact format they want. For example: Does `emissionSourceType`, `typeOf` or `name` is needed (epa ghgrp don't have `name` but do have `emissionSourceType` [see here](https://github.com/datacommonsorg/data/blob/master/scripts/us_epa/ghgrp/gas.py)).
- For the generation and emission rate in eGRID data may need different format.
- May need to change `process.py` for each column name.(For example: In `process.py`, I used 'plantAnnualNOxEmissions' format as the column name. But Data Commons may want 'plant Annual NOx Emissions' as the name.)
- For the `tmcf` file, from my understand it should follow the format: (property: C:the_name_of_node->column_name_of_corresponding_property)