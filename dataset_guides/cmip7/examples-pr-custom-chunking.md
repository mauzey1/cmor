# Example: Monthly Precipitation With Custom Chunking

## What This Example Demonstrates

This example writes `pr_tavg-u-hxy-u`, a monthly precipitation field on a native latitude-longitude grid, while overriding the data-variable chunk layout. It shows the supported CMIP7 pattern for chunking: create the CMOR variable, call `cmor.set_chunking(...)`, then stream the data one timestep at a time. The chunking choice is not part of the dataset JSON, so the chunk metadata is shown below with `ncdump -sh`.

The chunk shape in this example is chosen so the data-variable chunking itself is compatible with the size rule used by `cmip7_repack`'s `check_cmip7_packing` tool. In practice, that means keeping `time` and `time_bnds` to a single chunk or contiguous storage, and making each multi-chunk data-variable chunk at least about `4 MiB` uncompressed. A raw CMOR file may still fail that tool's separate consolidated-metadata check, which is outside the chunking controls demonstrated here.

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
  "outpath": "/tmp/cmor-docs/pr-chunking/out",
  "physics_index": "p1",
  "realization_index": "r9",
  "region": "glb",
  "source_id": "DUMMY-MODEL"
}
```

## Variable and Coordinate Choices

- Table: `CMIP7_atmos.json`
- Variable entry: `pr_tavg-u-hxy-u`
- Axes: `time`, `latitude`, `longitude`
- Root-string CV note: the published `_controlled_vocabulary_file` supplies root-level `drs_specs = "MIP-DRS7"`, `tracking_prefix = "hdl:21.14107"`, and `mip_era = "CMIP7"`, so CMOR derives them instead of reading them from dataset JSON
- Horizontal grid: `144 x 192`
- Runtime chunking call: `cmor.set_chunking(var_id, [38, 144, 192])`
- Write pattern: 40 monthly slices written one timestep at a time with `time_vals` and `time_bnds`

## Resolved Output File

```text
/tmp/cmor-docs/pr-chunking/out/MIP-DRS7/CMIP7/CMIP/MOHC/DUMMY-MODEL/amip/r9i1p1f3/glb/mon/pr/tavg-u-hxy-u/g999/v20260520/pr_tavg-u-hxy-u_mon_glb_g999_DUMMY-MODEL_amip_r9i1p1f3_197901-198204.nc
```

## Full `ncdump -h` Output

```text
netcdf pr_tavg-u-hxy-u_mon_glb_g999_DUMMY-MODEL_amip_r9i1p1f3_197901-198204 {
dimensions:
	time = UNLIMITED ; // (40 currently)
	lat = 144 ;
	lon = 192 ;
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
	float pr(time, lat, lon) ;
		pr:standard_name = "precipitation_flux" ;
		pr:long_name = "Precipitation" ;
		pr:units = "kg m-2 s-1" ;
		pr:cell_methods = "area: time: mean" ;
		pr:missing_value = 1.e+20f ;
		pr:_FillValue = 1.e+20f ;

// global attributes:
		:Conventions = "CF-1.12" ;
		:activity_id = "CMIP" ;
		:area_label = "u" ;
		:branded_variable = "pr_tavg-u-hxy-u" ;
		:branding_suffix = "tavg-u-hxy-u" ;
		:creation_date = "2026-05-20T18:58:19Z" ;
		:data_specs_version = "MIP-DS7.1.0.0" ;
		:description = "Simulation of the climate of the recent past with prescribed sea surface temperatures and sea ice concentrations." ;
		:drs_specs = "MIP-DRS7" ;
		:experiment = "Simulation of the climate of the recent past with prescribed sea surface temperatures and sea ice concentrations." ;
		:experiment_id = "amip" ;
		:forcing_index = "f3" ;
		:frequency = "mon" ;
		:grid_label = "g999" ;
		:history = "2026-05-20T18:58:19Z ; CMOR rewrote data to be consistent with CF-1.12 and CMIP7 data requirements." ;
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
		:temporal_label = "tavg" ;
		:title = "DUMMY-MODEL output prepared for CMIP7" ;
		:variable_id = "pr" ;
		:variant_label = "r9i1p1f3" ;
		:vertical_label = "u" ;
		:license = "CC-BY-4.0; CMIP7 data produced by MOHC is licensed under a Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0). Consult https://wcrp-cmip.github.io/cmip7-guidance/docs/CMIP7/Guidance_for_users/#2-terms-of-use-and-citations-requirements for terms of use governing CMIP7 output, including citation requirements and proper acknowledgment. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law." ;
		:cmor_version = "3.15.1" ;
		:tracking_id = "hdl:21.14107/9eeef70d-4eb2-48b3-a9a1-dd548491660b" ;
}
```

## Full `ncdump -sh` Output

```text
netcdf pr_tavg-u-hxy-u_mon_glb_g999_DUMMY-MODEL_amip_r9i1p1f3_197901-198204 {
dimensions:
	time = UNLIMITED ; // (40 currently)
	lat = 144 ;
	lon = 192 ;
	bnds = 2 ;
variables:
	double time(time) ;
		time:bounds = "time_bnds" ;
		time:units = "days since 1979-01-01" ;
		time:calendar = "360_day" ;
		time:axis = "T" ;
		time:long_name = "Time Intervals" ;
		time:standard_name = "time" ;
		time:_Storage = "chunked" ;
		time:_ChunkSizes = 512 ;
		time:_Endianness = "little" ;
	double time_bnds(time, bnds) ;
		time_bnds:_Storage = "chunked" ;
		time_bnds:_ChunkSizes = 512, 2 ;
		time_bnds:_DeflateLevel = 1 ;
		time_bnds:_Endianness = "little" ;
	double lat(lat) ;
		lat:bounds = "lat_bnds" ;
		lat:units = "degrees_north" ;
		lat:axis = "Y" ;
		lat:long_name = "Latitude" ;
		lat:standard_name = "latitude" ;
		lat:_Storage = "contiguous" ;
		lat:_Endianness = "little" ;
	double lat_bnds(lat, bnds) ;
		lat_bnds:_Storage = "chunked" ;
		lat_bnds:_ChunkSizes = 144, 2 ;
		lat_bnds:_DeflateLevel = 1 ;
		lat_bnds:_Endianness = "little" ;
	double lon(lon) ;
		lon:bounds = "lon_bnds" ;
		lon:units = "degrees_east" ;
		lon:axis = "X" ;
		lon:long_name = "Longitude" ;
		lon:standard_name = "longitude" ;
		lon:_Storage = "contiguous" ;
		lon:_Endianness = "little" ;
	double lon_bnds(lon, bnds) ;
		lon_bnds:_Storage = "chunked" ;
		lon_bnds:_ChunkSizes = 192, 2 ;
		lon_bnds:_DeflateLevel = 1 ;
		lon_bnds:_Endianness = "little" ;
	float pr(time, lat, lon) ;
		pr:standard_name = "precipitation_flux" ;
		pr:long_name = "Precipitation" ;
		pr:units = "kg m-2 s-1" ;
		pr:cell_methods = "area: time: mean" ;
		pr:missing_value = 1.e+20f ;
		pr:_FillValue = 1.e+20f ;
		pr:_Storage = "chunked" ;
		pr:_ChunkSizes = 38, 144, 192 ;
		pr:_DeflateLevel = 1 ;
		pr:_Endianness = "little" ;

// global attributes:
		:Conventions = "CF-1.12" ;
		:activity_id = "CMIP" ;
		:area_label = "u" ;
		:branded_variable = "pr_tavg-u-hxy-u" ;
		:branding_suffix = "tavg-u-hxy-u" ;
		:creation_date = "2026-05-20T18:58:19Z" ;
		:data_specs_version = "MIP-DS7.1.0.0" ;
		:description = "Simulation of the climate of the recent past with prescribed sea surface temperatures and sea ice concentrations." ;
		:drs_specs = "MIP-DRS7" ;
		:experiment = "Simulation of the climate of the recent past with prescribed sea surface temperatures and sea ice concentrations." ;
		:experiment_id = "amip" ;
		:forcing_index = "f3" ;
		:frequency = "mon" ;
		:grid_label = "g999" ;
		:history = "2026-05-20T18:58:19Z ; CMOR rewrote data to be consistent with CF-1.12 and CMIP7 data requirements." ;
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
		:temporal_label = "tavg" ;
		:title = "DUMMY-MODEL output prepared for CMIP7" ;
		:variable_id = "pr" ;
		:variant_label = "r9i1p1f3" ;
		:vertical_label = "u" ;
		:license = "CC-BY-4.0; CMIP7 data produced by MOHC is licensed under a Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0). Consult https://wcrp-cmip.github.io/cmip7-guidance/docs/CMIP7/Guidance_for_users/#2-terms-of-use-and-citations-requirements for terms of use governing CMIP7 output, including citation requirements and proper acknowledgment. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law." ;
		:cmor_version = "3.15.1" ;
		:tracking_id = "hdl:21.14107/9eeef70d-4eb2-48b3-a9a1-dd548491660b" ;
		:_NCProperties = "version=2,netcdf=4.10.0,hdf5=2.1.0" ;
		:_SuperblockVersion = 2 ;
		:_IsNetcdf4 = 1 ;
		:_Format = "netCDF-4 classic model" ;
}
```

This `ncdump -sh` output shows the part controlled by `cmor.set_chunking`: the `pr` data variable uses `_ChunkSizes = 38, 144, 192`, while the time coordinate variables keep CMOR's own chunking policy for streamed writes. With `float32` data, that data-chunk shape is about 4.20 MiB uncompressed, which satisfies the `cmip7_repack` data-chunk size rule without relying on the separate metadata-consolidation step.
