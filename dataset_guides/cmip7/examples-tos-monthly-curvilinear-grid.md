# Example: Monthly Curvilinear-Grid Ocean Surface Field

## What This Example Demonstrates

This example writes `tos_tavg-u-hxy-sea`, a monthly sea-surface temperature field on a curvilinear horizontal grid. Unlike the native latitude-longitude example, the driver loads `CMIP7_grids.json`, defines `grid_latitude` and `grid_longitude` axes, creates a CMOR grid with `cmor.grid(...)`, and passes that grid id to `cmor.variable(...)`.

The generated file keeps `time` as the leading data dimension, writes `rlat` and `rlon` as the grid axes, and attaches 2-D auxiliary `latitude` and `longitude` variables with 4-corner vertex bounds.

## Dataset JSON Used

```json
{
  "_AXIS_ENTRY_FILE": "CMIP7_coordinate.json",
  "_FORMULA_VAR_FILE": "CMIP7_formula_terms.json",
  "_cmip7_option": 1,
  "_controlled_vocabulary_file": "cmip7-cmor-tables/tables-cvs/cmor-cvs.json",
  "activity_id": "CMIP",
  "calendar": "360_day",
  "experiment_id": "amip",
  "forcing_index": "f3",
  "frequency": "mon",
  "grid_label": "g999",
  "initialization_index": "i1",
  "institution_id": "MOHC",
  "license_id": "CC-BY-4.0",
  "nominal_resolution": "100 km",
  "outpath": "/tmp/cmor-docs/tos-curvilinear/out",
  "physics_index": "p1",
  "realization_index": "r9",
  "region": "glb",
  "source_id": "DUMMY-MODEL"
}
```

## Variable and Coordinate Choices

- Variable table: `CMIP7_ocean.json`
- Grid table: `CMIP7_grids.json`
- Variable entry: `tos_tavg-u-hxy-sea`
- Axes passed to `cmor.variable(...)`: `time`, plus the grid id returned by `cmor.grid(...)`
- Axes used to create the grid: `grid_latitude`, `grid_longitude`
- Auxiliary grid coordinates: 2-D `latitude`, 2-D `longitude`, `vertices_latitude`, `vertices_longitude`
- Root-string CV note: the published `_controlled_vocabulary_file` supplies root-level `drs_specs = "MIP-DRS7"`, `tracking_prefix = "hdl:21.14107"`, and `mip_era = "CMIP7"`, so CMOR derives them instead of reading them from dataset JSON

The relevant runtime pattern is:

```text
load CMIP7_grids.json
create grid_latitude and grid_longitude axes
call cmor.grid(axis_ids=[grid_latitude, grid_longitude], latitude=..., longitude=..., latitude_vertices=..., longitude_vertices=...)
load CMIP7_ocean.json
create the time axis
call cmor.variable("tos_tavg-u-hxy-sea", "degC", [time, grid])
```

## Resolved Output File

```text
/tmp/cmor-docs/tos-curvilinear/out/MIP-DRS7/CMIP7/CMIP/MOHC/DUMMY-MODEL/amip/r9i1p1f3/glb/mon/tos/tavg-u-hxy-sea/g999/v20260527/tos_tavg-u-hxy-sea_mon_glb_g999_DUMMY-MODEL_amip_r9i1p1f3_197901-197902.nc
```

## Full `ncdump -h` Output

```text
netcdf tos_tavg-u-hxy-sea_mon_glb_g999_DUMMY-MODEL_amip_r9i1p1f3_197901-197902 {
dimensions:
	time = UNLIMITED ; // (2 currently)
	rlat = 3 ;
	rlon = 4 ;
	bnds = 2 ;
	vertices = 4 ;
variables:
	double time(time) ;
		time:bounds = "time_bnds" ;
		time:units = "days since 1979-01-01" ;
		time:calendar = "360_day" ;
		time:axis = "T" ;
		time:long_name = "Time Intervals" ;
		time:standard_name = "time" ;
	double time_bnds(time, bnds) ;
	double rlat(rlat) ;
		rlat:bounds = "rlat_bnds" ;
		rlat:units = "degrees" ;
		rlat:axis = "Y" ;
		rlat:long_name = "latitude in rotated pole grid" ;
		rlat:standard_name = "grid_latitude" ;
	double rlat_bnds(rlat, bnds) ;
	double rlon(rlon) ;
		rlon:bounds = "rlon_bnds" ;
		rlon:units = "degrees" ;
		rlon:axis = "X" ;
		rlon:long_name = "longitude in rotated pole grid" ;
		rlon:standard_name = "grid_longitude" ;
	double rlon_bnds(rlon, bnds) ;
	double latitude(rlat, rlon) ;
		latitude:standard_name = "latitude" ;
		latitude:long_name = "latitude" ;
		latitude:units = "degrees_north" ;
		latitude:missing_value = 1.e+20 ;
		latitude:_FillValue = 1.e+20 ;
		latitude:bounds = "vertices_latitude" ;
	double longitude(rlat, rlon) ;
		longitude:standard_name = "longitude" ;
		longitude:long_name = "longitude" ;
		longitude:units = "degrees_east" ;
		longitude:missing_value = 1.e+20 ;
		longitude:_FillValue = 1.e+20 ;
		longitude:bounds = "vertices_longitude" ;
	double vertices_latitude(rlat, rlon, vertices) ;
		vertices_latitude:units = "degrees_north" ;
		vertices_latitude:missing_value = 1.e+20 ;
		vertices_latitude:_FillValue = 1.e+20 ;
	double vertices_longitude(rlat, rlon, vertices) ;
		vertices_longitude:units = "degrees_east" ;
		vertices_longitude:missing_value = 1.e+20 ;
		vertices_longitude:_FillValue = 1.e+20 ;
	float tos(time, rlat, rlon) ;
		tos:standard_name = "sea_surface_temperature" ;
		tos:long_name = "Sea Surface Temperature" ;
		tos:units = "degC" ;
		tos:cell_methods = "area: mean where sea time: mean" ;
		tos:missing_value = 1.e+20f ;
		tos:_FillValue = 1.e+20f ;
		tos:coordinates = "latitude longitude" ;

// global attributes:
		:Conventions = "CF-1.12" ;
		:activity_id = "CMIP" ;
		:area_label = "sea" ;
		:branded_variable = "tos_tavg-u-hxy-sea" ;
		:branding_suffix = "tavg-u-hxy-sea" ;
		:creation_date = "2026-05-27T23:19:26Z" ;
		:data_specs_version = "MIP-DS7.1.0.0" ;
		:description = "Simulation of the climate of the recent past with prescribed sea surface temperatures and sea ice concentrations." ;
		:drs_specs = "MIP-DRS7" ;
		:experiment = "Simulation of the climate of the recent past with prescribed sea surface temperatures and sea ice concentrations." ;
		:experiment_id = "amip" ;
		:forcing_index = "f3" ;
		:frequency = "mon" ;
		:grid_label = "g999" ;
		:history = "2026-05-27T23:19:26Z ; CMOR rewrote data to be consistent with CF-1.12 and CMIP7 data requirements." ;
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
		:realm = "ocean" ;
		:region = "glb" ;
		:source = "DUMMY-MODEL: aerosol: Dummy Aerosol; atmosphere: Dummy Atmosphere; atmospheric_chemistry: Dummy Atmospheric Chemistry; land_surface: Dummy Land Surface; ocean: Dummy Ocean; ocean_biogeochemistry: Dummy Ocean Biogeochemistry; sea_ice: Dummy Sea Ice" ;
		:source_id = "DUMMY-MODEL" ;
		:table_info = "Name: CMIP7_ocean.json; Creation Date:(2026-04-21 15:01:29) MD5:a66e0fc7ab41aafa94f1ba3223e0c9fe" ;
		:temporal_label = "tavg" ;
		:title = "DUMMY-MODEL output prepared for CMIP7" ;
		:tracking_id = "hdl:21.14107/44125134-fb5c-47a1-a877-cccfa10466a4" ;
		:variable_id = "tos" ;
		:variant_label = "r9i1p1f3" ;
		:vertical_label = "u" ;
		:license = "CC-BY-4.0; CMIP7 data produced by MOHC is licensed under a Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0). Consult https://wcrp-cmip.github.io/cmip7-guidance/docs/CMIP7/Guidance_for_users/#2-terms-of-use-and-citations-requirements for terms of use governing CMIP7 output, including citation requirements and proper acknowledgment. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law." ;
		:cmor_version = "3.15.1" ;
}
```
