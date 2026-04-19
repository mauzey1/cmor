# Example: Hybrid-Sigma Specific Humidity

This example writes `hus_tavg-al-hxy-u`, a monthly model-level specific-humidity field on a standard hybrid-sigma coordinate. It shows the most complex case in this set: a vertical axis with formula terms, z-factors, and a surface-pressure field stored with the main variable.

Generator script: [example-data-tools/generate_hus_hybrid_sigma.py](example-data-tools/generate_hus_hybrid_sigma.py)

## Dataset JSON Used

The generated dataset JSON points at a local copy of the controlled vocabulary because this example adds the CMIP7 vertical-label token `al` for atmosphere model levels.

```json
{
  "_AXIS_ENTRY_FILE": "CMIP7_coordinate.json",
  "_FORMULA_VAR_FILE": "CMIP7_formula_terms.json",
  "_cmip7_option": 1,
  "_controlled_vocabulary_file": "CMIP7_CV_with_model_levels.json",
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
  "outpath": "/tmp/cmor-docs/hus-hybrid/out",
  "physics_index": "p1",
  "realization_index": "r009",
  "region": "glb",
  "source_id": "PCMDI-test-1-0",
  "tracking_prefix": "hdl:21.14100"
}
```

## Additional Controlled-Vocabulary Entry Used

```json
{
  "CV": {
    "vertical_label": {
      "al": "atmosphere model levels"
    }
  }
}
```

## Variable and Coordinate Choices

- Table: `CMIP7_atmos.json`
- Variable entry: `hus_tavg-al-hxy-u`
- Axes: `time`, `standard_hybrid_sigma`, `latitude`, `longitude`
- Z-factors written: `a`, `b`, `p0`, `ps`, `a_bnds`, `b_bnds`

## Output File

```text
/tmp/cmor-docs/hus-hybrid/out/CMIP7/CMIP/PCMDI-test-1-0/glb/mon/piControl/r009i000001dp1f30/hus/tavg-al-hxy-u/gn/v20260419/hus_tavg-al-hxy-u_mon_glb_gn_PCMDI-test-1-0_piControl_r009i000001dp1f30_201801-201802.nc
```

## Full `ncdump -h` Output

```text
netcdf hus_tavg-al-hxy-u_mon_glb_gn_PCMDI-test-1-0_piControl_r009i000001dp1f30_201801-201802 {
dimensions:
	time = UNLIMITED ; // (2 currently)
	lev = 5 ;
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
		:archive_id = "WCRP" ;
		:area_label = "u" ;
		:branded_variable = "hus_tavg-al-hxy-u" ;
		:branding_suffix = "tavg-al-hxy-u" ;
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
		:variable_id = "hus" ;
		:variant_label = "r009i000001dp1f30" ;
		:vertical_label = "al" ;
		:license = "CC BY 4.0; CMIP7 data produced by PCMDI is licensed under a Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/). Consult https://wcrp-cmip.github.io/cmip7-guidance/docs/CMIP7/Guidance_for_users for terms of use governing CMIP7 output, including citation requirements and proper acknowledgment. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law." ;
		:cmor_version = "3.14.1" ;
		:tracking_id = "hdl:21.14100/5ea144a4-6c22-407f-81a4-70a0d1c082e6" ;
}
```
