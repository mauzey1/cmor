# Example: Monthly Native-Grid Ocean Surface Field

This example writes `tos_tavg-u-hxy-sea`, a monthly sea-surface temperature field on a native latitude-longitude grid. It is the simplest complete CMIP7 case in this set: one time axis, one latitude axis, one longitude axis, and no extra grid or formula-term variables.

Generator script: [example-data-tools/generate_tos_monthly_native_grid.py](example-data-tools/generate_tos_monthly_native_grid.py)

## Dataset JSON Used

```json
{
  "_AXIS_ENTRY_FILE": "CMIP7_coordinate.json",
  "_FORMULA_VAR_FILE": "CMIP7_formula_terms.json",
  "_cmip7_option": 1,
  "_controlled_vocabulary_file": "TestTables/CMIP7_CV.json",
  "activity_id": "CMIP",
  "archive_id": "WCRP",
  "calendar": "360_day",
  "cv_version": "6.2.19.0",
  "drs_specs": "MIP-DRS7",
  "experiment_id": "piControl",
  "forcing_index": "f30",
  "frequency": "mon",
  "grid_label": "gn",
  "host_collection": "CMIP7",
  "initialization_index": "i000001d",
  "institution_id": "PCMDI",
  "license_id": "CC BY 4.0",
  "nominal_resolution": "250 km",
  "outpath": "/tmp/cmor-docs/tos/out",
  "physics_index": "p1",
  "realization_index": "r009",
  "region": "glb",
  "source_id": "PCMDI-test-1-0",
  "tracking_prefix": "hdl:21.14100"
}
```

## Variable and Coordinate Choices

- Table: `CMIP7_ocean.json`
- Variable entry: `tos_tavg-u-hxy-sea`
- Axes: `time`, `latitude`, `longitude`

## Output File

```text
/tmp/cmor-docs/tos/out/CMIP7/CMIP/PCMDI-test-1-0/glb/mon/piControl/r009i000001dp1f30/tos/tavg-u-hxy-sea/gn/v20260419/tos_tavg-u-hxy-sea_mon_glb_gn_PCMDI-test-1-0_piControl_r009i000001dp1f30_201801-201802.nc
```

## Full `ncdump -h` Output

```text
netcdf tos_tavg-u-hxy-sea_mon_glb_gn_PCMDI-test-1-0_piControl_r009i000001dp1f30_201801-201802 {
dimensions:
	time = UNLIMITED ; // (2 currently)
	lat = 3 ;
	lon = 4 ;
	bnds = 2 ;
variables:
	double time(time) ;
		time:bounds = "time_bnds" ;
		time:units = "days since 2018" ;
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
		:archive_id = "WCRP" ;
		:area_label = "sea" ;
		:branded_variable = "tos_tavg-u-hxy-sea" ;
		:branding_suffix = "tavg-u-hxy-sea" ;
		:creation_date = "2026-04-19T22:33:29Z" ;
		:cv_version = "6.2.19.0" ;
		:data_specs_version = "CMIP-7.0.0.0" ;
		:description = "DECK: pre-industrial control simulation (TODO: add details)" ;
		:drs_specs = "MIP-DRS7" ;
		:experiment = "Simulation of the pre-industrial climate" ;
		:experiment_id = "piControl" ;
		:forcing_index = "f30" ;
		:frequency = "mon" ;
		:grid_label = "gn" ;
		:history = "2026-04-19T22:33:29Z ; CMOR rewrote data to be consistent with CMIP7, CF-1.12 and CF standards." ;
		:horizontal_label = "hxy" ;
		:host_collection = "CMIP7" ;
		:initialization_index = "i000001d" ;
		:institution = "Program for Climate Model Diagnosis and Intercomparison, Lawrence Livermore National Laboratory, Livermore, CA 94550, USA" ;
		:institution_id = "PCMDI" ;
		:label = "PCMDI-test 1.0" ;
		:label_extended = "PCMDI-test 1.0 (This entry is free text for users to contribute verbose information)" ;
		:license_id = "CC BY 4.0" ;
		:mip_era = "CMIP7" ;
		:nominal_resolution = "250 km" ;
		:physics_index = "p1" ;
		:product = "model-output" ;
		:realization_index = "r009" ;
		:realm = "ocean" ;
		:region = "glb" ;
		:release_year = "1989" ;
		:source = "PCMDI-test 1.0 (1989): \n",
			"aerosol: none\n",
			"atmos: Earth1.0-gettingHotter (360 x 180 longitude/latitude; 50 levels; top level 0.1 mb)\n",
			"atmosChem: none\n",
			"land: Earth1.0\n",
			"landIce: none\n",
			"ocean: BlueMarble1.0-warming (360 x 180 longitude/latitude; 50 levels; top grid cell 0-10 m)\n",
			"ocnBgchem: none\n",
			"seaIce: Declining1.0-warming (360 x 180 longitude/latitude)" ;
		:source_id = "PCMDI-test-1-0" ;
		:table_info = "Creation Date:(2026-03-11 08:29:00) MD5:981269c887d0715575860a82a0a34189" ;
		:temporal_label = "tavg" ;
		:title = "PCMDI-test-1-0 output prepared for CMIP7" ;
		:tracking_id = "hdl:21.14100/78dc94e1-9fa2-4e42-b3cf-2aa82c844a7f" ;
		:variable_id = "tos" ;
		:variant_label = "r009i000001dp1f30" ;
		:vertical_label = "u" ;
		:license = "CC BY 4.0; CMIP7 data produced by PCMDI is licensed under a Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/). Consult https://wcrp-cmip.github.io/cmip7-guidance/docs/CMIP7/Guidance_for_users for terms of use governing CMIP7 output, including citation requirements and proper acknowledgment. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law." ;
		:cmor_version = "3.14.1" ;
}
```
