# Example: Monthly Ocean Field With Parent Metadata

This example writes `tos_tavg-u-hxy-sea` for the `piControl` experiment and includes the parent-lineage attributes required by the current CMIP7 controlled vocabulary. It shows the simplest parented case in this guide: the same native latitude-longitude monthly ocean field as the basic `tos` example, but with `branch_*` and `parent_*` metadata present in both the dataset JSON and the output file.

## Dataset JSON Used

```json
{
  "_AXIS_ENTRY_FILE": "CMIP7_coordinate.json",
  "_FORMULA_VAR_FILE": "CMIP7_formula_terms.json",
  "_cmip7_option": 1,
  "_controlled_vocabulary_file": "cmip7-cmor-tables/tables-cvs/cmor-cvs.json",
  "activity_id": "CMIP",
  "branch_time_in_child": 30.0,
  "branch_time_in_parent": 10800.0,
  "calendar": "360_day",
  "drs_specs": "MIP-DRS7",
  "experiment_id": "piControl",
  "forcing_index": "f3",
  "frequency": "mon",
  "grid_label": "g999",
  "initialization_index": "i1",
  "institution_id": "MOHC",
  "license_id": "CC-BY-4.0",
  "mip_era": "CMIP7",
  "nominal_resolution": "100 km",
  "outpath": "/tmp/cmor-docs/tos-parent/out",
  "parent_activity_id": "CMIP",
  "parent_experiment_id": "piControl-spinup",
  "parent_mip_era": "CMIP7",
  "parent_source_id": "DUMMY-MODEL",
  "parent_time_units": "days since 1850-01-01",
  "parent_variant_label": "r9i1p1f3",
  "physics_index": "p1",
  "realization_index": "r9",
  "region": "glb",
  "source_id": "DUMMY-MODEL",
  "tracking_prefix": "hdl:21.14107"
}
```

## Variable and Coordinate Choices

- Table: `CMIP7_ocean.json`
- Variable entry: `tos_tavg-u-hxy-sea`
- Axes: `time`, `latitude`, `longitude`
- Parent chain required by the current CV: `piControl -> piControl-spinup`

## Output File

```text
/tmp/cmor-docs/tos-parent/out/MIP-DRS7/CMIP7/CMIP/MOHC/DUMMY-MODEL/piControl/r9i1p1f3/glb/mon/tos/tavg-u-hxy-sea/g999/v20260501/tos_tavg-u-hxy-sea_mon_glb_g999_DUMMY-MODEL_piControl_r9i1p1f3_197901-197902.nc
```

## Full `ncdump -h` Output

```text
netcdf tos_tavg-u-hxy-sea_mon_glb_g999_DUMMY-MODEL_piControl_r9i1p1f3_197901-197902 {
dimensions:
	time = UNLIMITED ; // (2 currently)
	lat = 3 ;
	lon = 4 ;
	bnds = 2 ;
variables:
	double time(time) ;
		time:bounds = "time_bnds" ;
		time:units = "days since 1979-01-01" ;
		time:calendar = "360_day" ;
		time:axis = "T" ;
		time:long_name = "Time Intervals" ;
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
	float tos(time, lat, lon) ;
		tos:standard_name = "sea_surface_temperature" ;
		tos:long_name = "Sea Surface Temperature" ;
		tos:units = "degC" ;
		tos:cell_methods = "area: mean where sea time: mean" ;
		tos:missing_value = 1.e+20f ;
		tos:_FillValue = 1.e+20f ;

// global attributes:
		:Conventions = "CF-1.12" ;
		:activity_id = "CMIP" ;
		:area_label = "sea" ;
		:branch_time_in_child = 30. ;
		:branch_time_in_parent = 10800. ;
		:branded_variable = "tos_tavg-u-hxy-sea" ;
		:branding_suffix = "tavg-u-hxy-sea" ;
		:creation_date = "2026-05-02T01:18:57Z" ;
		:data_specs_version = "MIP-DS7.1.0.0" ;
		:description = "Pre-industrial control simulation with prescribed carbon dioxide concentrations (for prescribed carbon dioxide emissions, see `esm-piControl`). Used to characterise natural variability and unforced behaviour." ;
		:drs_specs = "MIP-DRS7" ;
		:experiment = "Pre-industrial control simulation with prescribed carbon dioxide concentrations (for prescribed carbon dioxide emissions, see `esm-piControl`). Used to characterise natural variability and unforced behaviour." ;
		:experiment_id = "piControl" ;
		:forcing_index = "f3" ;
		:frequency = "mon" ;
		:grid_label = "g999" ;
		:history = "2026-05-02T01:18:57Z ; CMOR rewrote data to be consistent with CMIP7, CF-1.12 and CF standards." ;
		:horizontal_label = "hxy" ;
		:initialization_index = "i1" ;
		:institution = "Met Office Hadley Centre" ;
		:institution_id = "MOHC" ;
		:license_id = "CC-BY-4.0" ;
		:mip_era = "CMIP7" ;
		:nominal_resolution = "100 km" ;
		:parent_activity_id = "CMIP" ;
		:parent_experiment_id = "piControl-spinup" ;
		:parent_mip_era = "CMIP7" ;
		:parent_source_id = "DUMMY-MODEL" ;
		:parent_time_units = "days since 1850-01-01" ;
		:parent_variant_label = "r9i1p1f3" ;
		:physics_index = "p1" ;
		:product = "model-output" ;
		:realization_index = "r9" ;
		:realm = "ocean" ;
		:region = "glb" ;
		:source = "DUMMY-MODEL: aerosol: Dummy Aerosol; atmosphere: Dummy Atmosphere; atmospheric_chemistry: Dummy Atmospheric Chemistry; land_surface: Dummy Land Surface; ocean: Dummy Ocean; ocean_biogeochemistry: Dummy Ocean Biogeochemistry; sea_ice: Dummy Sea Ice" ;
		:source_id = "DUMMY-MODEL" ;
		:table_info = "Creation Date:(2026-04-21 15:01:29) MD5:a66e0fc7ab41aafa94f1ba3223e0c9fe" ;
		:temporal_label = "tavg" ;
		:title = "DUMMY-MODEL output prepared for CMIP7" ;
		:tracking_id = "hdl:21.14107/f1c08434-80e2-47cd-94bf-d8d6dc8daf89" ;
		:variable_id = "tos" ;
		:variant_label = "r9i1p1f3" ;
		:vertical_label = "u" ;
		:license = "CC-BY-4.0; CMIP7 data produced by MOHC is licensed under a Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0). Consult https://wcrp-cmip.github.io/cmip7-guidance/docs/CMIP7/Guidance_for_users/#2-terms-of-use-and-citations-requirements for terms of use governing CMIP7 output, including citation requirements and proper acknowledgment. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law." ;
		:cmor_version = "3.14.3" ;
}
```
