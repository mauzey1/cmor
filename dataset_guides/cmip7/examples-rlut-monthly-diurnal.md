# Example: Monthly Diurnal With A `time3` Axis

## What This Example Demonstrates

This example writes `rlut_tclmdc-u-hxy-u`, a CMIP7 Monthly Diurnal variable that uses the `time3` coordinate entry. It demonstrates two CMOR 3.15.1 behaviors that matter for driver authors: CMOR writes climatology bounds as `climatology_bnds` while keeping `frequency = 1hr`, and an explicit user override of `Conventions = CF-1.13` is preserved in both the global attribute and the default `history` string.

## Dataset JSON Used

```json
{
  "Conventions": "CF-1.13",
  "_AXIS_ENTRY_FILE": "CMIP7_coordinate.json",
  "_FORMULA_VAR_FILE": "CMIP7_formula_terms.json",
  "_cmip7_option": 1,
  "_controlled_vocabulary_file": "cmip7-cmor-tables/tables-cvs/cmor-cvs.json",
  "activity_id": "CMIP",
  "calendar": "360_day",
  "experiment_id": "amip",
  "forcing_index": "f3",
  "frequency": "1hr",
  "grid_label": "g999",
  "initialization_index": "i1",
  "institution_id": "MOHC",
  "license_id": "CC-BY-4.0",
  "nominal_resolution": "100 km",
  "outpath": "/tmp/cmor-docs/rlut-diurnal/out",
  "physics_index": "p1",
  "realization_index": "r9",
  "region": "glb",
  "source_id": "DUMMY-MODEL"
}
```

## Variable and Coordinate Choices

- Table: `CMIP7_atmos.json`
- Variable entry: `rlut_tclmdc-u-hxy-u`
- Axes: `time3`, `latitude`, `longitude`
- Root-string CV note: the published `_controlled_vocabulary_file` supplies root-level `drs_specs = "MIP-DRS7"`, `tracking_prefix = "hdl:21.14107"`, and `mip_era = "CMIP7"`, so CMOR derives them instead of reading them from dataset JSON
- Time-axis note: CMOR writes the output coordinate as `time`, attaches `climatology = "climatology_bnds"`, and keeps `long_name = "Diurnal Mean"`
- Sampling note: this example writes two monthly diurnal cycles, so the output contains 48 hourly climatology bins spanning January and February
- Output-naming note: the resolved filename uses a monthly `197901-197903` time-range suffix without an extra climatology marker

## Resolved Output File

```text
/tmp/cmor-docs/rlut-diurnal/out/MIP-DRS7/CMIP7/CMIP/MOHC/DUMMY-MODEL/amip/r9i1p1f3/glb/1hr/rlut/tclmdc-u-hxy-u/g999/v20260520/rlut_tclmdc-u-hxy-u_1hr_glb_g999_DUMMY-MODEL_amip_r9i1p1f3_197901-197903.nc
```

## Full `ncdump -h` Output

```text
netcdf rlut_tclmdc-u-hxy-u_1hr_glb_g999_DUMMY-MODEL_amip_r9i1p1f3_197901-197903 {
dimensions:
	time = UNLIMITED ; // (48 currently)
	lat = 3 ;
	lon = 4 ;
	bnds = 2 ;
variables:
	double time(time) ;
		time:climatology = "climatology_bnds" ;
		time:units = "days since 1979-01-01" ;
		time:calendar = "360_day" ;
		time:axis = "T" ;
		time:long_name = "Diurnal Mean" ;
		time:standard_name = "time" ;
	double climatology_bnds(time, bnds) ;
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
	float rlut(time, lat, lon) ;
		rlut:standard_name = "toa_outgoing_longwave_flux" ;
		rlut:long_name = "TOA Outgoing Longwave Radiation" ;
		rlut:units = "W m-2" ;
		rlut:cell_methods = "area: mean time: mean within days time: mean over days" ;
		rlut:missing_value = 1.e+20f ;
		rlut:_FillValue = 1.e+20f ;

// global attributes:
		:Conventions = "CF-1.13" ;
		:activity_id = "CMIP" ;
		:area_label = "u" ;
		:branded_variable = "rlut_tclmdc-u-hxy-u" ;
		:branding_suffix = "tclmdc-u-hxy-u" ;
		:creation_date = "2026-05-20T19:15:08Z" ;
		:data_specs_version = "MIP-DS7.1.0.0" ;
		:description = "Simulation of the climate of the recent past with prescribed sea surface temperatures and sea ice concentrations." ;
		:drs_specs = "MIP-DRS7" ;
		:experiment = "Simulation of the climate of the recent past with prescribed sea surface temperatures and sea ice concentrations." ;
		:experiment_id = "amip" ;
		:forcing_index = "f3" ;
		:frequency = "1hr" ;
		:grid_label = "g999" ;
		:history = "2026-05-20T19:15:08Z ; CMOR rewrote data to be consistent with CF-1.13 and CMIP7 data requirements." ;
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
		:realm = "atmos" ;
		:region = "glb" ;
		:source = "DUMMY-MODEL: aerosol: Dummy Aerosol; atmosphere: Dummy Atmosphere; atmospheric_chemistry: Dummy Atmospheric Chemistry; land_surface: Dummy Land Surface; ocean: Dummy Ocean; ocean_biogeochemistry: Dummy Ocean Biogeochemistry; sea_ice: Dummy Sea Ice" ;
		:source_id = "DUMMY-MODEL" ;
		:table_info = "Name: CMIP7_atmos.json; Creation Date:(2026-04-21 15:01:29) MD5:6c425d5354e32ec5498084c927c982a9" ;
		:temporal_label = "tclmdc" ;
		:title = "DUMMY-MODEL output prepared for CMIP7" ;
		:tracking_id = "hdl:21.14107/073a42d6-fb5b-4dd6-bbbf-054572fc62bb" ;
		:variable_id = "rlut" ;
		:variant_label = "r9i1p1f3" ;
		:vertical_label = "u" ;
		:license = "CC-BY-4.0; CMIP7 data produced by MOHC is licensed under a Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0). Consult https://wcrp-cmip.github.io/cmip7-guidance/docs/CMIP7/Guidance_for_users/#2-terms-of-use-and-citations-requirements for terms of use governing CMIP7 output, including citation requirements and proper acknowledgment. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law." ;
		:cmor_version = "3.15.1" ;
}
```
