# Example: Monthly Ice-Sheet Rainfall Flux

This example writes `prra_tavg-u-hxy-is`, a monthly rainfall flux over ice-sheet area. It shows that the branded variable controls both the area label and the multi-realm `realm` attribute.

Generator script: [example-data-tools/generate_prra_monthly_ice_sheet.py](example-data-tools/generate_prra_monthly_ice_sheet.py)

## Dataset JSON Used

```json
{
  "_AXIS_ENTRY_FILE": "CMIP7_coordinate.json",
  "_FORMULA_VAR_FILE": "CMIP7_formula_terms.json",
  "_cmip7_option": 1,
  "_controlled_vocabulary_file": "cmip7-cmor-tables/tables-cvs/cmor-cvs.json",
  "activity_id": "CMIP",
  "calendar": "360_day",
  "drs_specs": "MIP-DRS7",
  "experiment_id": "amip",
  "forcing_index": "f3",
  "frequency": "mon",
  "grid_label": "g999",
  "initialization_index": "i1",
  "institution_id": "MOHC",
  "license_id": "CC-BY-4.0",
  "mip_era": "CMIP7",
  "nominal_resolution": "100 km",
  "outpath": "/tmp/cmor-docs/prra/out",
  "physics_index": "p1",
  "realization_index": "r9",
  "region": "glb",
  "source_id": "DUMMY-MODEL",
  "tracking_prefix": "hdl:21.14107"
}
```

## Variable and Coordinate Choices

- Table: `CMIP7_atmos.json`
- Variable entry: `prra_tavg-u-hxy-is`
- Axes: `time`, `latitude`, `longitude`

## Output File

```text
/tmp/cmor-docs/prra/out/MIP-DRS7/CMIP7/CMIP/MOHC/DUMMY-MODEL/amip/r9i1p1f3/glb/mon/prra/tavg-u-hxy-is/g999/v20260419/prra_tavg-u-hxy-is_mon_glb_g999_DUMMY-MODEL_amip_r9i1p1f3_197901-197902.nc
```

## Full `ncdump -h` Output

```text
netcdf prra_tavg-u-hxy-is_mon_glb_g999_DUMMY-MODEL_amip_r9i1p1f3_197901-197902 {
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
	float prra(time, lat, lon) ;
		prra:standard_name = "rainfall_flux" ;
		prra:long_name = "Ice Sheet Rainfall Flux" ;
		prra:units = "kg m-2 s-1" ;
		prra:cell_methods = "area: time: mean where ice_sheet" ;
		prra:missing_value = 1.e+20f ;
		prra:_FillValue = 1.e+20f ;

// global attributes:
		:Conventions = "CF-1.12" ;
		:activity_id = "CMIP" ;
		:area_label = "is" ;
		:branded_variable = "prra_tavg-u-hxy-is" ;
		:branding_suffix = "tavg-u-hxy-is" ;
		:creation_date = "2026-04-19T23:52:24Z" ;
		:data_specs_version = "MIP-DS7.1.0.0" ;
		:description = "Simulation of the climate of the recent past with prescribed sea surface temperatures and sea ice concentrations." ;
		:drs_specs = "MIP-DRS7" ;
		:experiment = "Simulation of the climate of the recent past with prescribed sea surface temperatures and sea ice concentrations." ;
		:experiment_id = "amip" ;
		:forcing_index = "f3" ;
		:frequency = "mon" ;
		:grid_label = "g999" ;
		:history = "2026-04-19T23:52:24Z ; CMOR rewrote data to be consistent with CMIP7, CF-1.12 and CF standards." ;
		:horizontal_label = "hxy" ;
		:initialization_index = "i1" ;
		:institution = "Met Office Hadley Centre" ;
		:institution_id = "MOHC" ;
		:license_id = "CC-BY-4.0" ;
		:mip_era = "CMIP7" ;
		:nominal_resolution = "100 km" ;
		:physics_index = "p1" ;
		:product = "model-output" ;
		:realization_index = "r9" ;
		:realm = "atmos land landIce" ;
		:region = "glb" ;
		:source = "DUMMY-MODEL: aerosol: Dummy Aerosol; atmosphere: Dummy Atmosphere; atmospheric_chemistry: Dummy Atmospheric Chemistry; land_surface: Dummy Land Surface; ocean: Dummy Ocean; ocean_biogeochemistry: Dummy Ocean Biogeochemistry; sea_ice: Dummy Sea Ice" ;
		:source_id = "DUMMY-MODEL" ;
		:table_info = "Creation Date:(2026-03-11 08:29:00) MD5:2f9a4e8dc61b12a4346dcc3bd83414b5" ;
		:temporal_label = "tavg" ;
		:title = "DUMMY-MODEL output prepared for CMIP7" ;
		:tracking_id = "hdl:21.14107/50415a95-e0c0-49e4-95d0-5116e69d7b31" ;
		:variable_id = "prra" ;
		:variant_label = "r9i1p1f3" ;
		:vertical_label = "u" ;
		:license = "CC-BY-4.0; CMIP7 data produced by MOHC is licensed under a Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0). Consult https://wcrp-cmip.github.io/cmip7-guidance/docs/CMIP7/Guidance_for_users/#2-terms-of-use-and-citations-requirements for terms of use governing CMIP7 output, including citation requirements and proper acknowledgment. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law." ;
		:cmor_version = "3.14.1" ;
}
```
