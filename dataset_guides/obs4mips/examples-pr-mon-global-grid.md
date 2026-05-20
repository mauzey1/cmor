# Example: Monthly Gridded Precipitation On A Regular Latitude-Longitude Grid

## What This Example Demonstrates

This example writes `pr` from `obs4MIPs_Amon.json` on a regular `lat`/`lon` grid. It uses a small subset of the bundled `demo-global2D/precip.mon.mean.nc` file, converts the source units from `mm/day` to `kg m-2 s-1`, and validates the current `CMAP-V1902` source metadata against the published obs4MIPs CV.

## Dataset JSON Used

```json
{
  "_AXIS_ENTRY_FILE": "obs4MIPs_coordinate.json",
  "_FORMULA_VAR_FILE": "obs4MIPs_formula_terms.json",
  "_controlled_vocabulary_file": "obs4MIPs_CV.json",
  "activity_id": "obs4MIPs",
  "calendar": "standard",
  "contact": "pingping.Xie@noaa.gov, obs4mips-panel@wcrp-cmip.org",
  "grid": "1x1 degree latitude x longitude",
  "grid_label": "gn",
  "has_aux_unc": "FALSE",
  "institution_id": "NOAA-NCEI",
  "license": "Data in this file is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License (https://creativecommons.org/licenses).",
  "nominal_resolution": "250 km",
  "outpath": "/private/tmp/obs4mips-guide/pr-mon-global-grid/out",
  "output_file_template": "<variable_id><frequency><source_id><variant_label><grid_label>",
  "output_path_template": "<activity_id><institution_id><source_id><frequency><variable_id><grid_label><version>",
  "processing_code_location": "dataset_guides/obs4mips/example-data-tools/generate_pr_mon_global_grid.py",
  "product": "observations",
  "references": "Xie, P., and P.A. Arkin, 1997: Global precipitation: A 17-year monthly analysis based on gauge observations, satellite estimates, and numerical model outputs. Bull. Amer. Meteor. Soc., 78, 2539-2558.",
  "source_data_url": "https://www.psl.noaa.gov/data/gridded/data.cmap.html",
  "source_id": "CMAP-V1902",
  "title": "CMAP V1902 precipitation prepared for obs4MIPs",
  "variant_info": "Example subset prepared for the CMOR dataset guide",
  "variant_label": "CMORGuide"
}
```

## Variable And Coordinate Choices

- Table: `obs4MIPs_Amon.json`
- Variable entry: `pr`
- Axes: `time`, `latitude`, `longitude`
- Source file pattern: `demo/demo-global2D/precip.mon.mean.nc`
- Unit conversion: `mm/day` to `kg m-2 s-1` by dividing by `86400`
- CV-derived metadata in the output: `institution`, `region`, `source`, `source_type`, `source_version_number`, `frequency`, `realm`, `table_id`, and `variable_id`

## Resolved Output File

```text
/private/tmp/obs4mips-guide/pr-mon-global-grid/out/obs4MIPs/NOAA-NCEI/CMAP-V1902/mon/pr/gn/v20260512/pr_mon_CMAP-V1902_CMORGuide_gn_197901-197902.nc
```

## Full `ncdump -h` Output

```text
netcdf pr_mon_CMAP-V1902_CMORGuide_gn_197901-197902 {
dimensions:
	time = UNLIMITED ; // (2 currently)
	lat = 3 ;
	lon = 3 ;
	bnds = 2 ;
variables:
	double time(time) ;
		time:bounds = "time_bnds" ;
		time:units = "days since 1800-01-01 00:00:0.0" ;
		time:calendar = "standard" ;
		time:axis = "T" ;
		time:long_name = "time" ;
		time:standard_name = "time" ;
	double time_bnds(time, bnds) ;
	double lat(lat) ;
		lat:bounds = "lat_bnds" ;
		lat:units = "degrees_north" ;
		lat:axis = "Y" ;
		lat:long_name = "Latitude" ;
		lat:standard_name = "latitude" ;
	double lat_bnds(lat, bnds) ;
	double lon(lon) ;
		lon:bounds = "lon_bnds" ;
		lon:units = "degrees_east" ;
		lon:axis = "X" ;
		lon:long_name = "Longitude" ;
		lon:standard_name = "longitude" ;
	double lon_bnds(lon, bnds) ;
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
		:Conventions = "CF-1.11; ODS-2.5" ;
		:activity_id = "obs4MIPs" ;
		:contact = "pingping.Xie@noaa.gov, obs4mips-panel@wcrp-cmip.org" ;
		:creation_date = "2026-05-12T23:11:31Z" ;
		:data_specs_version = "ODS-2.5" ;
		:external_variables = "areacella" ;
		:frequency = "mon" ;
		:grid = "1x1 degree latitude x longitude" ;
		:grid_label = "gn" ;
		:has_aux_unc = "FALSE" ;
		:history = "2026-05-12T23:11:31Z ; CMOR rewrote data to be consistent with CMIP6, CF-1.11; ODS-2.5 and CF standards." ;
		:institution = "NOAA National Centers for Environmental Information, Asheville, NC 28801, USA" ;
		:institution_id = "NOAA-NCEI" ;
		:mip_era = "CMIP6" ;
		:nominal_resolution = "250 km" ;
		:processing_code_location = "dataset_guides/obs4mips/example-data-tools/generate_pr_mon_global_grid.py" ;
		:product = "observations" ;
		:realm = "atmos" ;
		:references = "Xie, P., and P.A. Arkin, 1997: Global precipitation: A 17-year monthly analysis based on gauge observations, satellite estimates, and numerical model outputs. Bull. Amer. Meteor. Soc., 78, 2539-2558." ;
		:region = "global" ;
		:source = "CMAP V1902 (N/A): CMAP Precipitation" ;
		:source_data_url = "https://www.psl.noaa.gov/data/gridded/data.cmap.html" ;
		:source_id = "CMAP-V1902" ;
		:source_type = "satellite_blended" ;
		:source_version_number = "V1902" ;
		:table_id = "obs4MIPs_Amon" ;
		:table_info = "Creation Date:(18 November 2020) MD5:2326922a1c50fd765f82110ed5c3675e" ;
		:title = "CMAP V1902 precipitation prepared for obs4MIPs" ;
		:tracking_id = "95fa32d2-e653-4fc8-b2d2-36e816185994" ;
		:variable_id = "pr" ;
		:variant_info = "Example subset prepared for the CMOR dataset guide" ;
		:variant_label = "CMORGuide" ;
		:license = "Data in this file is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License (https://creativecommons.org/licenses)." ;
		:cmor_version = "3.15.1" ;
}
```
