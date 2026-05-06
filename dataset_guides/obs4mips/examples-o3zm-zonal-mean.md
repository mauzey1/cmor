# Example: Monthly Zonal-Mean Ozone Profile

This example writes the `o3zm` table entry from `obs4MIPs_Amon.json` using a zonal-mean `latitude` plus `height` coordinate system. It subsets the bundled `demo-zonalmeans/BSVerticalOzone_MR_GPH_Tier1.3_v1.0.nc` file, converts the source `altitude` axis from kilometers to meters, and writes the current zonal-mean `grid_label = gnz`.

## Dataset JSON Used

```json
{
  "_AXIS_ENTRY_FILE": "obs4MIPs_coordinate.json",
  "_FORMULA_VAR_FILE": "obs4MIPs_formula_terms.json",
  "_controlled_vocabulary_file": "obs4MIPs_CV.json",
  "activity_id": "obs4MIPs",
  "calendar": "standard",
  "contact": "greg@bodekerscientific.com, submissions-obs4mips@wcrp-cmip.org",
  "grid": "5 degree latitude height zonal mean",
  "grid_label": "gnz",
  "has_aux_unc": "FALSE",
  "institution_id": "DLR-BIRA",
  "license": "Data in this file is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License (https://creativecommons.org/licenses).",
  "nominal_resolution": "500 km",
  "outpath": "/private/tmp/obs4mips-guide/o3zm-zonal-mean/out",
  "output_file_template": "<variable_id><frequency><source_id><variant_label><grid_label>",
  "output_path_template": "<activity_id><institution_id><source_id><frequency><variable_id><grid_label><version>",
  "processing_code_location": "dataset_guides/obs4mips/example-data-tools/generate_o3zm_zonal_mean.py",
  "product": "observations",
  "references": "Hassler, B., Kremser, S., Bodeker, G. E., Lewis, J., Nesbit, K., Davis, S. M., Chipperfield, M. P., Dhomse, S. S., and Dameris, M.: An updated version of a gap-free monthly mean zonal mean ozone database, Earth Syst. Sci. Data, 10, 1473-1490, https://doi.org/10.5194/essd-10-1473-2018, 2018.",
  "source_data_url": "http://www.bodekerscientific.com/data/monthly-mean-global-vertically-resolved-ozone",
  "source_id": "BSVertOzone-v1-0",
  "title": "Bodeker Scientific vertical ozone profile database",
  "variant_info": "Example subset prepared for the CMOR dataset guide",
  "variant_label": "CMORGuide"
}
```

## Variable And Coordinate Choices

- Table: `obs4MIPs_Amon.json`
- Variable entry: `o3zm`
- Output variable name: `o3`
- Axes: `time`, `height`, `latitude`
- Height-axis handling: source `altitude` is in kilometers; the example writes `height` in meters
- Grid-label note: the current CV accepts `gnz` for zonal-mean data; this guide uses that more specific label instead of generic `gn`

## Output File

```text
/private/tmp/obs4mips-guide/o3zm-zonal-mean/out/obs4MIPs/DLR-BIRA/BSVertOzone-v1-0/mon/o3/gnz/v20260506/o3_mon_BSVertOzone-v1-0_CMORGuide_gnz_197901-197902.nc
```

## Full `ncdump -h` Output

```text
netcdf o3_mon_BSVertOzone-v1-0_CMORGuide_gnz_197901-197902 {
dimensions:
	time = UNLIMITED ; // (2 currently)
	height = 3 ;
	lat = 4 ;
	bnds = 2 ;
variables:
	double time(time) ;
		time:bounds = "time_bnds" ;
		time:units = "days since 1950-01-01 00:00:00" ;
		time:calendar = "standard" ;
		time:axis = "T" ;
		time:long_name = "time" ;
		time:standard_name = "time" ;
	double time_bnds(time, bnds) ;
	double height(height) ;
		height:units = "m" ;
		height:axis = "Z" ;
		height:positive = "up" ;
		height:long_name = "height" ;
		height:standard_name = "height" ;
	double lat(lat) ;
		lat:bounds = "lat_bnds" ;
		lat:units = "degrees_north" ;
		lat:axis = "Y" ;
		lat:long_name = "Latitude" ;
		lat:standard_name = "latitude" ;
	double lat_bnds(lat, bnds) ;
	float o3(time, height, lat) ;
		o3:standard_name = "mole_fraction_of_ozone_in_air" ;
		o3:long_name = "Mole Fraction of O3" ;
		o3:comment = "Mole fraction is used in the construction mole_fraction_of_X_in_Y, where X is a material constituent of Y." ;
		o3:units = "mol mol-1" ;
		o3:cell_methods = "time: mean" ;
		o3:cell_measures = "area: areacella" ;
		o3:missing_value = 1.e+20f ;
		o3:_FillValue = 1.e+20f ;

// global attributes:
		:Conventions = "CF-1.12; ODS-2.6.1" ;
		:activity_id = "obs4MIPs" ;
		:contact = "greg@bodekerscientific.com, submissions-obs4mips@wcrp-cmip.org" ;
		:creation_date = "2026-05-06T19:42:52Z" ;
		:data_specs_version = "ODS-2.6.1" ;
		:external_variables = "areacella" ;
		:frequency = "mon" ;
		:grid = "5 degree latitude height zonal mean" ;
		:grid_label = "gnz" ;
		:has_aux_unc = "FALSE" ;
		:history = "2026-05-06T19:42:52Z ; CMOR rewrote data to be consistent with CMIP6, CF-1.12; ODS-2.6.1 and CF standards." ;
		:institution = "Deutsches Zentrum fur Luft- und Raumfahrt, Royal Belgian Institute for Space Aeronomy" ;
		:institution_id = "DLR-BIRA" ;
		:mip_era = "CMIP6" ;
		:nominal_resolution = "500 km" ;
		:processing_code_location = "dataset_guides/obs4mips/example-data-tools/generate_o3zm_zonal_mean.py" ;
		:product = "observations" ;
		:realm = "atmosChem" ;
		:references = "Hassler, B., Kremser, S., Bodeker, G. E., Lewis, J., Nesbit, K., Davis, S. M., Chipperfield, M. P., Dhomse, S. S., and Dameris, M.: An updated version of a gap-free monthly mean zonal mean ozone database, Earth Syst. Sci. Data, 10, 1473-1490, https://doi.org/10.5194/essd-10-1473-2018, 2018." ;
		:region = "global" ;
		:source = "BSVertOzone v1-0 (2018): Mole concentration of ozone in air" ;
		:source_data_url = "http://www.bodekerscientific.com/data/monthly-mean-global-vertically-resolved-ozone" ;
		:source_id = "BSVertOzone-v1-0" ;
		:source_type = "satellite_retrieval" ;
		:source_version_number = "v1-0" ;
		:table_id = "obs4MIPs_Amon" ;
		:table_info = "Creation Date:(18 November 2020) MD5:aa08a16dfef81dcf310b0fe2c4c02122" ;
		:title = "Bodeker Scientific vertical ozone profile database" ;
		:tracking_id = "cdcaaedd-b819-411b-b59b-99e9584e74a5" ;
		:variable_id = "o3" ;
		:variant_info = "Example subset prepared for the CMOR dataset guide" ;
		:variant_label = "CMORGuide" ;
		:license = "Data in this file is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License (https://creativecommons.org/licenses)." ;
		:cmor_version = "3.14.3" ;
}
```

