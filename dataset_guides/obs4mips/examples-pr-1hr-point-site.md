# Example: Hourly Point-Site Precipitation

This example writes `pr` from `obs4MIPs_A1hrPt.json` for a single in-situ site. It follows the bundled `demo-insitu` pattern but updates it to the current CV rules by using `grid_label = site` and `site_id = US-ARM-SGP`. The first two records of `demo/demo-insitu/sample_in-situ1.nc` are converted from `mm/hour` to `kg m-2 s-1`.

## Dataset JSON Used

```json
{
  "_AXIS_ENTRY_FILE": "obs4MIPs_coordinate.json",
  "_FORMULA_VAR_FILE": "obs4MIPs_formula_terms.json",
  "_controlled_vocabulary_file": "obs4MIPs_CV.json",
  "activity_id": "obs4MIPs",
  "calendar": "standard",
  "contact": "zhang40@llnl.gov, obs4mips-panel@wcrp-cmip.org",
  "grid": "site",
  "grid_label": "site",
  "has_aux_unc": "FALSE",
  "institution_id": "DOE-ARM",
  "license": "Data in this file is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License (https://creativecommons.org/licenses).",
  "nominal_resolution": "site",
  "outpath": "/private/tmp/obs4mips-guide/pr-1hr-point-site/out",
  "output_file_template": "<variable_id><frequency><source_id><variant_label><grid_label>",
  "output_path_template": "<activity_id><institution_id><source_id><frequency><variable_id><grid_label><version>",
  "processing_code_location": "dataset_guides/obs4mips/example-data-tools/generate_pr_1hr_point_site.py",
  "product": "site-observations",
  "references": "Xie, Shaocheng., and 16-coauthors, 2010: ARM climate modeling best estimate data, Bull. Amer. Meteor. Soc, 91, 13-20, doi:10.1175/2009BAMS2891.1.",
  "site_id": "US-ARM-SGP",
  "site_location": "ARM Southern Great Plains site- Lamont",
  "source_data_url": "https://arm.gov/data/science-data-products/vaps/armbe",
  "source_id": "ARMBE-atm-c1-1-8",
  "title": "ARMBE atmospheric point observations prepared for obs4MIPs",
  "variant_info": "Example subset prepared for the CMOR dataset guide",
  "variant_label": "CMORGuide"
}
```

## Variable And Coordinate Choices

- Table: `obs4MIPs_A1hrPt.json`
- Variable entry: `pr`
- Axes: `time`, `latitude1`, `longitude1`
- Site lookup: latitude and longitude are taken from `obs4MIPs_site_id.json` for `US-ARM-SGP`
- Time-axis note: the script passes time in `seconds since 2018-01-01`, but CMOR rewrites the output axis units to `days since 2018-01-01`
- Frequency note: the table name is `A1hrPt`, but the output `frequency` attribute is `1hr`

## Output File

```text
/private/tmp/obs4mips-guide/pr-1hr-point-site/out/obs4MIPs/DOE-ARM/ARMBE-atm-c1-1-8/1hr/pr/site/v20260506/pr_1hr_ARMBE-atm-c1-1-8_CMORGuide_site_201801010030-201801010130.nc
```

## Full `ncdump -h` Output

```text
netcdf pr_1hr_ARMBE-atm-c1-1-8_CMORGuide_site_201801010030-201801010130 {
dimensions:
	time = UNLIMITED ; // (2 currently)
	lat = 1 ;
	lon = 1 ;
	bnds = 2 ;
variables:
	double time(time) ;
		time:bounds = "time_bnds" ;
		time:units = "days since 2018-01-01" ;
		time:calendar = "standard" ;
		time:axis = "T" ;
		time:long_name = "time" ;
		time:standard_name = "time" ;
	double time_bnds(time, bnds) ;
	double lat(lat) ;
		lat:units = "degrees_north" ;
		lat:axis = "Y" ;
		lat:long_name = "Latitude" ;
		lat:standard_name = "latitude" ;
	double lon(lon) ;
		lon:units = "degrees_east" ;
		lon:axis = "X" ;
		lon:long_name = "Longitude" ;
		lon:standard_name = "longitude" ;
	float pr(time, lat, lon) ;
		pr:standard_name = "precipitation_flux" ;
		pr:long_name = "Precipitation" ;
		pr:comment = "includes both liquid and solid phases" ;
		pr:units = "kg m-2 s-1" ;
		pr:cell_methods = "area: time: mean" ;
		pr:cell_measures = "area: areacella" ;
		pr:missing_value = 1.e+20f ;
		pr:_FillValue = 1.e+20f ;

// global attributes:
		:Conventions = "CF-1.7 ODS-2.6" ;
		:activity_id = "obs4MIPs" ;
		:contact = "zhang40@llnl.gov, obs4mips-panel@wcrp-cmip.org" ;
		:creation_date = "2026-05-06T19:42:52Z" ;
		:data_specs_version = "2.6" ;
		:external_variables = "areacella" ;
		:frequency = "1hr" ;
		:grid = "site" ;
		:grid_label = "site" ;
		:has_aux_unc = "FALSE" ;
		:history = "2026-05-06T19:42:52Z ; CMOR rewrote data to be consistent with CMIP6, CF-1.7 ODS-2.6 and CF standards." ;
		:institution = "U.S. Department of Energy, Atmospheric Radiation Measurment Program" ;
		:institution_id = "DOE-ARM" ;
		:mip_era = "CMIP6" ;
		:nominal_resolution = "site" ;
		:processing_code_location = "dataset_guides/obs4mips/example-data-tools/generate_pr_1hr_point_site.py" ;
		:product = "site-observations" ;
		:realm = "atmos" ;
		:references = "Xie, Shaocheng., and 16-coauthors, 2010: ARM climate modeling best estimate data, Bull. Amer. Meteor. Soc, 91, 13-20, doi:10.1175/2009BAMS2891.1." ;
		:region = "north_america" ;
		:site_id = "US-ARM-SGP" ;
		:site_location = "ARM Southern Great Plains site- Lamont" ;
		:source = "ARMBE atm-c1-1-8 (2023): DOE ARM Best Estimate Data Products for Atmosphere and Cloud properties" ;
		:source_data_url = "https://arm.gov/data/science-data-products/vaps/armbe" ;
		:source_id = "ARMBE-atm-c1-1-8" ;
		:source_type = "insitu" ;
		:source_version_number = "atm-c1-1-8" ;
		:table_id = "obs4MIPs_A1hrPt" ;
		:table_info = "Creation Date:(18 November 2020) MD5:d1931a6ed68778081dacabfba94915fe" ;
		:title = "ARMBE atmospheric point observations prepared for obs4MIPs" ;
		:tracking_id = "9f95b5cb-e802-4086-8c63-9f00ce5f9abb" ;
		:variable_id = "pr" ;
		:variant_info = "Example subset prepared for the CMOR dataset guide" ;
		:variant_label = "CMORGuide" ;
		:license = "Data in this file is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License (https://creativecommons.org/licenses)." ;
		:cmor_version = "3.14.3" ;
}
```

