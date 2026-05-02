# Example: Hybrid-Sigma Specific Humidity

This example writes `hus_tavg-al-hxy-u`, a monthly model-level specific-humidity field on a standard hybrid-sigma coordinate. It shows the most complex case in this set: a vertical axis with formula terms, z-factors, and a surface-pressure field stored with the main variable.

Generator script: [example-data-tools/generate_hus_hybrid_sigma.py](example-data-tools/generate_hus_hybrid_sigma.py)

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
  "outpath": "/tmp/cmor-docs/hus-hybrid/out",
  "physics_index": "p1",
  "realization_index": "r9",
  "region": "glb",
  "source_id": "DUMMY-MODEL",
  "tracking_prefix": "hdl:21.14107"
}
```

## Variable and Coordinate Choices

- Table: `CMIP7_atmos.json`
- Variable entry: `hus_tavg-al-hxy-u`
- Axes: `time`, `standard_hybrid_sigma`, `latitude`, `longitude`
- Z-factors written: `a`, `b`, `p0`, `ps`, `a_bnds`, `b_bnds`

## Output File

```text
/tmp/cmor-docs/hus-hybrid/out/MIP-DRS7/CMIP7/CMIP/MOHC/DUMMY-MODEL/amip/r9i1p1f3/glb/mon/hus/tavg-al-hxy-u/g999/v20260501/hus_tavg-al-hxy-u_mon_glb_g999_DUMMY-MODEL_amip_r9i1p1f3_197901-197902.nc
```

## Full `ncdump -h` Output

```text
netcdf hus_tavg-al-hxy-u_mon_glb_g999_DUMMY-MODEL_amip_r9i1p1f3_197901-197902 {
dimensions:
	time = UNLIMITED ; // (2 currently)
	lev = 5 ;
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
	double lev(lev) ;
		lev:bounds = "lev_bnds" ;
		lev:units = "1" ;
		lev:axis = "Z" ;
		lev:positive = "down" ;
		lev:long_name = "hybrid sigma pressure coordinate" ;
		lev:standard_name = "atmosphere_hybrid_sigma_pressure_coordinate" ;
		lev:formula = "p = a*p0 + b*ps" ;
		lev:formula_terms = "p0: p0 a: a b: b ps: ps" ;
	double lev_bnds(lev, bnds) ;
		lev_bnds:formula = "p = a*p0 + b*ps" ;
		lev_bnds:standard_name = "atmosphere_hybrid_sigma_pressure_coordinate" ;
		lev_bnds:units = "1" ;
		lev_bnds:formula_terms = "p0: p0 a: a_bnds b: b_bnds ps: ps" ;
	double p0 ;
		p0:standard_name = "reference_air_pressure_for_atmosphere_vertical_coordinate" ;
		p0:long_name = "vertical coordinate formula term: reference pressure" ;
		p0:units = "Pa" ;
	double a(lev) ;
		a:long_name = "vertical coordinate formula term: a" ;
	double b(lev) ;
		b:long_name = "vertical coordinate formula term: b" ;
	float ps(time, lat, lon) ;
		ps:standard_name = "air_pressure" ;
		ps:long_name = "Surface Air Pressure" ;
		ps:units = "Pa" ;
	double a_bnds(lev, bnds) ;
		a_bnds:long_name = "vertical coordinate formula term: a(k+1/2)" ;
	double b_bnds(lev, bnds) ;
		b_bnds:long_name = "vertical coordinate formula term: b(k+1/2)" ;
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
	float hus(time, lev, lat, lon) ;
		hus:standard_name = "specific_humidity" ;
		hus:long_name = "Specific Humidity" ;
		hus:units = "1" ;
		hus:cell_methods = "area: time: mean" ;
		hus:missing_value = 1.e+20f ;
		hus:_FillValue = 1.e+20f ;

// global attributes:
		:Conventions = "CF-1.12" ;
		:activity_id = "CMIP" ;
		:area_label = "u" ;
		:branded_variable = "hus_tavg-al-hxy-u" ;
		:branding_suffix = "tavg-al-hxy-u" ;
		:creation_date = "2026-05-02T01:03:57Z" ;
		:data_specs_version = "MIP-DS7.1.0.0" ;
		:description = "Simulation of the climate of the recent past with prescribed sea surface temperatures and sea ice concentrations." ;
		:drs_specs = "MIP-DRS7" ;
		:experiment = "Simulation of the climate of the recent past with prescribed sea surface temperatures and sea ice concentrations." ;
		:experiment_id = "amip" ;
		:forcing_index = "f3" ;
		:frequency = "mon" ;
		:grid_label = "g999" ;
		:history = "2026-05-02T01:03:57Z ; CMOR rewrote data to be consistent with CMIP7, CF-1.12 and CF standards." ;
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
		:table_info = "Creation Date:(2026-04-21 15:01:29) MD5:6c425d5354e32ec5498084c927c982a9" ;
		:temporal_label = "tavg" ;
		:title = "DUMMY-MODEL output prepared for CMIP7" ;
		:variable_id = "hus" ;
		:variant_label = "r9i1p1f3" ;
		:vertical_label = "al" ;
		:license = "CC-BY-4.0; CMIP7 data produced by MOHC is licensed under a Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0). Consult https://wcrp-cmip.github.io/cmip7-guidance/docs/CMIP7/Guidance_for_users/#2-terms-of-use-and-citations-requirements for terms of use governing CMIP7 output, including citation requirements and proper acknowledgment. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law." ;
		:cmor_version = "3.14.3" ;
		:tracking_id = "hdl:21.14107/0b39b326-d6fc-4d39-8946-3a3766762b8f" ;
}
```
