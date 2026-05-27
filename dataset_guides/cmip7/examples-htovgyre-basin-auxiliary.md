# Example: Monthly Ocean Transport With Basin Auxiliary Coordinate

## What This Example Demonstrates

This example writes `htovgyre_tavg-u-hyb-sea`, a monthly northward ocean heat transport variable whose table dimensions include `latitude`, `basin`, and `time`. The `basin` coordinate is a CMIP7 character coordinate, so CMOR writes a `sector(basin, strlen)` auxiliary coordinate and adds `coordinates = "sector"` to the main variable.

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
  "outpath": "/tmp/cmor-docs/htovgyre-basin/out",
  "physics_index": "p1",
  "realization_index": "r9",
  "region": "glb",
  "source_id": "DUMMY-MODEL"
}
```

## Variable and Coordinate Choices

- Table: `CMIP7_ocean.json`
- Variable entry: `htovgyre_tavg-u-hyb-sea`
- Axes passed to `cmor.variable(...)`: `time`, `basin`, `latitude`
- Character coordinate labels passed to the `basin` axis: `atlantic_arctic_ocean`, `indian_pacific_ocean`, `global_ocean`
- Output auxiliary coordinate: `sector(basin, strlen)`
- Root-string CV note: the published `_controlled_vocabulary_file` supplies root-level `drs_specs = "MIP-DRS7"`, `tracking_prefix = "hdl:21.14107"`, and `mip_era = "CMIP7"`, so CMOR derives them instead of reading them from dataset JSON

The key runtime pattern is:

```text
basin = cmor.axis("basin", units="", coord_vals=["atlantic_arctic_ocean", "indian_pacific_ocean", "global_ocean"])
variable = cmor.variable("htovgyre_tavg-u-hyb-sea", "W", [time, basin, latitude])
```

## Resolved Output File

```text
/tmp/cmor-docs/htovgyre-basin/out/MIP-DRS7/CMIP7/CMIP/MOHC/DUMMY-MODEL/amip/r9i1p1f3/glb/mon/htovgyre/tavg-u-hyb-sea/g999/v20260527/htovgyre_tavg-u-hyb-sea_mon_glb_g999_DUMMY-MODEL_amip_r9i1p1f3_197901-197902.nc
```

## Full `ncdump -h` Output

```text
netcdf htovgyre_tavg-u-hyb-sea_mon_glb_g999_DUMMY-MODEL_amip_r9i1p1f3_197901-197902 {
dimensions:
	time = UNLIMITED ; // (2 currently)
	basin = 3 ;
	lat = 3 ;
	bnds = 2 ;
	strlen = 21 ;
variables:
	double time(time) ;
		time:bounds = "time_bnds" ;
		time:units = "days since 1979-01-01" ;
		time:calendar = "360_day" ;
		time:axis = "T" ;
		time:long_name = "Time Intervals" ;
		time:standard_name = "time" ;
	double time_bnds(time, bnds) ;
	char sector(basin, strlen) ;
		sector:long_name = "Ocean Basin" ;
		sector:standard_name = "region" ;
	double lat(lat) ;
		lat:bounds = "lat_bnds" ;
		lat:units = "degrees_north" ;
		lat:axis = "Y" ;
		lat:long_name = "Latitude" ;
		lat:standard_name = "latitude" ;
	double lat_bnds(lat, bnds) ;
	float htovgyre(time, basin, lat) ;
		htovgyre:standard_name = "northward_ocean_heat_transport_due_to_gyre" ;
		htovgyre:long_name = "Northward Ocean Heat Transport Due to Gyre" ;
		htovgyre:units = "W" ;
		htovgyre:cell_methods = "depth: longitude: sum where sea (along a zig-zag grid path spanning a basin)  time: mean" ;
		htovgyre:missing_value = 1.e+20f ;
		htovgyre:_FillValue = 1.e+20f ;
		htovgyre:coordinates = "sector" ;

// global attributes:
		:Conventions = "CF-1.12" ;
		:activity_id = "CMIP" ;
		:area_label = "sea" ;
		:branded_variable = "htovgyre_tavg-u-hyb-sea" ;
		:branding_suffix = "tavg-u-hyb-sea" ;
		:creation_date = "2026-05-27T23:36:59Z" ;
		:data_specs_version = "MIP-DS7.1.0.0" ;
		:description = "Simulation of the climate of the recent past with prescribed sea surface temperatures and sea ice concentrations." ;
		:drs_specs = "MIP-DRS7" ;
		:experiment = "Simulation of the climate of the recent past with prescribed sea surface temperatures and sea ice concentrations." ;
		:experiment_id = "amip" ;
		:forcing_index = "f3" ;
		:frequency = "mon" ;
		:grid_label = "g999" ;
		:history = "2026-05-27T23:36:59Z ; CMOR rewrote data to be consistent with CF-1.12 and CMIP7 data requirements." ;
		:horizontal_label = "hyb" ;
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
		:tracking_id = "hdl:21.14107/145194c4-7cda-4100-abde-ad01056d52a1" ;
		:variable_id = "htovgyre" ;
		:variant_label = "r9i1p1f3" ;
		:vertical_label = "u" ;
		:license = "CC-BY-4.0; CMIP7 data produced by MOHC is licensed under a Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0). Consult https://wcrp-cmip.github.io/cmip7-guidance/docs/CMIP7/Guidance_for_users/#2-terms-of-use-and-citations-requirements for terms of use governing CMIP7 output, including citation requirements and proper acknowledgment. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law." ;
		:cmor_version = "3.15.1" ;
}
```
