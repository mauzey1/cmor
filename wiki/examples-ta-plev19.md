# Example: Pressure-Level Air Temperature

This example writes `ta_tavg-p19-hxy-air`, a monthly air-temperature field on the standard 19 pressure levels. It shows the pressure-level case where the driver must supply the coordinate values requested by `plev19`.

Generator script: [example-data-tools/generate_ta_pressure_levels.py](example-data-tools/generate_ta_pressure_levels.py)

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
  "outpath": "/tmp/cmor-docs/ta-p19/out",
  "physics_index": "p1",
  "realization_index": "r009",
  "region": "glb",
  "source_id": "PCMDI-test-1-0",
  "tracking_prefix": "hdl:21.14100"
}
```

## Variable and Coordinate Choices

- Table: `CMIP7_atmos.json`
- Variable entry: `ta_tavg-p19-hxy-air`
- Axes: `time`, `plev19`, `latitude`, `longitude`

## Output File

```text
/tmp/cmor-docs/ta-p19/out/CMIP7/CMIP/PCMDI-test-1-0/glb/mon/piControl/r009i000001dp1f30/ta/tavg-p19-hxy-air/gn/v20260419/ta_tavg-p19-hxy-air_mon_glb_gn_PCMDI-test-1-0_piControl_r009i000001dp1f30_201801-201802.nc
```

## Full `ncdump -h` Output

```text
netcdf ta_tavg-p19-hxy-air_mon_glb_gn_PCMDI-test-1-0_piControl_r009i000001dp1f30_201801-201802 {
dimensions:
	time = UNLIMITED ; // (2 currently)
	plev = 19 ;
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
	double plev(plev) ;
		plev:units = "Pa" ;
		plev:axis = "Z" ;
		plev:positive = "down" ;
		plev:long_name = "Pressure Levels (19)" ;
		plev:standard_name = "air_pressure" ;
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
	float ta(time, plev, lat, lon) ;
		ta:standard_name = "air_temperature" ;
		ta:long_name = "Air Temperature" ;
		ta:units = "K" ;
		ta:cell_methods = "area: time: mean where air" ;
		ta:missing_value = 1.e+20f ;
		ta:_FillValue = 1.e+20f ;

// global attributes:
		:Conventions = "CF-1.12" ;
		:activity_id = "CMIP" ;
		:archive_id = "WCRP" ;
		:area_label = "air" ;
		:branded_variable = "ta_tavg-p19-hxy-air" ;
		:branding_suffix = "tavg-p19-hxy-air" ;
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
		:realm = "atmos" ;
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
		:table_info = "Creation Date:(2026-03-11 08:29:00) MD5:2f9a4e8dc61b12a4346dcc3bd83414b5" ;
		:temporal_label = "tavg" ;
		:title = "PCMDI-test-1-0 output prepared for CMIP7" ;
		:tracking_id = "hdl:21.14100/f6af3d29-24f0-483d-b490-ed1d1f6e519f" ;
		:variable_id = "ta" ;
		:variant_label = "r009i000001dp1f30" ;
		:vertical_label = "p19" ;
		:license = "CC BY 4.0; CMIP7 data produced by PCMDI is licensed under a Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/). Consult https://wcrp-cmip.github.io/cmip7-guidance/docs/CMIP7/Guidance_for_users for terms of use governing CMIP7 output, including citation requirements and proper acknowledgment. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law." ;
		:cmor_version = "3.14.1" ;
}
```
