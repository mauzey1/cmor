# Example: Daily Tasmax With Grid And CRS Metadata

## What This Example Demonstrates

This example writes `tasmax` from `DRCDP_APday.json` using the separate grids workflow. It subsets the shipped `DataPreparationExamples/DEMO/MACA3-0/DRCDP-MACA3-0_demo_data.nc` file, loads `DRCDP_grids.json`, creates a grid with 2-D auxiliary latitude-longitude coordinates plus 4-corner vertices, and writes a `crs` variable with the WGS84 metadata copied from the demo file.

## Dataset JSON Used

```json
{
  "_AXIS_ENTRY_FILE": "DRCDP_coordinate.json",
  "_FORMULA_VAR_FILE": "DRCDP_formula_terms.json",
  "_controlled_vocabulary_file": "DRCDP_CV.json",
  "_history_template": "%s; CMOR rewrote data to be consistent with <activity_id>, CMIP6, CMIP6Plus and <Conventions> standards",
  "activity_id": "DRCDP",
  "driving_activity_id": "CMIP",
  "driving_experiment_id": "historical",
  "driving_mip_era": "CMIP6",
  "driving_source_id": "ACCESS-CM2",
  "driving_variant_label": "r1i1p1f1",
  "outpath": "/private/tmp/drcdp-guide/tasmax-grid-crs/out",
  "output_file_template": "<variable_id><region_id><institution_id><source_id><driving_mip_era><driving_experiment_id><driving_source_id><driving_variant_label><frequency>",
  "output_path_template": "<activity_id><region_id><institution_id><source_id><driving_mip_era><driving_activity_id><driving_experiment_id><driving_source_id><driving_variant_label><frequency><variable_id><version>",
  "source_id": "MACA3-0",
  "tracking_prefix": "hdl:21.14100"
}
```

## Variable And Coordinate Choices

- Variable table: `DRCDP_APday.json`
- Grid table: `DRCDP_grids.json`
- Variable entry: `tasmax`
- Axes passed to `cmor.variable(...)`: `time`, `gridId`
- Auxiliary grid coordinates: 2-D `latitude`, 2-D `longitude`, `vertices_latitude`, `vertices_longitude`
- CRS: `grid_mapping_name = latitude_longitude` with `semi_major_axis`, `inverse_flattening`, and `crs_wkt` copied from the demo file
- Longitude normalization: the example converts longitudes to `[0, 360]` because `DRCDP_grids.json` validates `longitude` and `vertices_longitude` against that range

## Resolved Output File

```text
/private/tmp/drcdp-guide/tasmax-grid-crs/out/DRCDP/NAM/UCM-ACSL/MACA3-0/CMIP6/CMIP/historical/ACCESS-CM2/r1i1p1f1/day/tasmax/v20260512/tasmax_NAM_UCM-ACSL_MACA3-0_CMIP6_historical_ACCESS-CM2_r1i1p1f1_day_20090101-20090102.nc
```

## Full `ncdump -h` Output

```text
netcdf tasmax_NAM_UCM-ACSL_MACA3-0_CMIP6_historical_ACCESS-CM2_r1i1p1f1_day_20090101-20090102 {
dimensions:
	time = UNLIMITED ; // (2 currently)
	lat = 4 ;
	lon = 5 ;
	bnds = 2 ;
	vertices = 4 ;
variables:
	double time(time) ;
		time:bounds = "time_bnds" ;
		time:units = "days since 1900-01-01" ;
		time:calendar = "gregorian" ;
		time:axis = "T" ;
		time:long_name = "time" ;
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
	int crs ;
		crs:grid_mapping_name = "latitude_longitude" ;
		crs:longitude_of_prime_meridian = 0. ;
		crs:semi_major_axis = 6378137. ;
		crs:inverse_flattening = 298.257223563 ;
		crs:crs_wkt = "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4326\"]]" ;
	double latitude(lat, lon) ;
		latitude:standard_name = "latitude" ;
		latitude:long_name = "latitude" ;
		latitude:units = "degrees_north" ;
		latitude:missing_value = 1.e+20 ;
		latitude:_FillValue = 1.e+20 ;
		latitude:bounds = "vertices_latitude" ;
	double longitude(lat, lon) ;
		longitude:standard_name = "longitude" ;
		longitude:long_name = "longitude" ;
		longitude:units = "degrees_east" ;
		longitude:missing_value = 1.e+20 ;
		longitude:_FillValue = 1.e+20 ;
		longitude:bounds = "vertices_longitude" ;
	double vertices_latitude(lat, lon, vertices) ;
		vertices_latitude:units = "degrees_north" ;
		vertices_latitude:missing_value = 1.e+20 ;
		vertices_latitude:_FillValue = 1.e+20 ;
	double vertices_longitude(lat, lon, vertices) ;
		vertices_longitude:units = "degrees_east" ;
		vertices_longitude:missing_value = 1.e+20 ;
		vertices_longitude:_FillValue = 1.e+20 ;
	double height ;
		height:units = "m" ;
		height:axis = "Z" ;
		height:positive = "up" ;
		height:long_name = "height" ;
		height:standard_name = "height" ;
	float tasmax(time, lat, lon) ;
		tasmax:standard_name = "air_temperature" ;
		tasmax:long_name = "Daily Maximum Near-Surface Air Temperature" ;
		tasmax:comment = "maximum near-surface (usually, 2 meter) air temperature (add cell_method attribute \'time: max\')" ;
		tasmax:units = "K" ;
		tasmax:cell_methods = "area: mean time: maximum" ;
		tasmax:cell_measures = "area: areacella" ;
		tasmax:history = "2026-05-12T23:11:30Z altered by CMOR: Treated scalar dimension: \'height\'." ;
		tasmax:coordinates = "height latitude longitude" ;
		tasmax:missing_value = 1.e+20f ;
		tasmax:_FillValue = 1.e+20f ;
		tasmax:grid_mapping = "crs" ;

// global attributes:
		:Conventions = "CF-1.7 CMIP-6.5" ;
		:activity_id = "DRCDP" ;
		:contact = "John T. Abatzoglou; jabatzoglou@ucmerced.edu" ;
		:creation_date = "2026-05-12T23:11:30Z" ;
		:data_specs_version = "6.5.0.0; mip-cmor-tables; f42386929a0057ed15e66a3bac045b8c00d33c0f" ;
		:driving_activity_id = "CMIP" ;
		:driving_experiment_id = "historical" ;
		:driving_mip_era = "CMIP6" ;
		:driving_source_id = "ACCESS-CM2" ;
		:driving_variant_label = "r1i1p1f1" ;
		:external_variables = "areacella" ;
		:frequency = "day" ;
		:further_info_url = "https://www.climatologylab.org/maca.html" ;
		:grid = "10 x 10 km latitude x longitude" ;
		:grid_label = "gn" ;
		:history = "2026-05-12T23:11:30Z; CMOR rewrote data to be consistent with DRCDP, CMIP6, CMIP6Plus and CF-1.7 CMIP-6.5 standards" ;
		:institution = "Applied Climate Science Laboratory, University of California, Merced, 5200 N. Lake Road, Merced, CA 95343, USA (ROR: 00d9ah105)" ;
		:institution_id = "UCM-ACSL" ;
		:license_id = "CC0 1.0" ;
		:license_url = "https://creativecommons.org/publicdomain/zero/1.0/" ;
		:nominal_resolution = "10 km" ;
		:product = "downscaled-statistical" ;
		:realm = "atmos" ;
		:reference = "Abatzoglou, John T., and Timothy J. Brown (2012) A comparison of statistical downscaling methods suited for wildfire applications. International Journal of Climatology, 32 (5), pp 772-780. https://doi.org/10.1002/joc.2312" ;
		:region = "north_america" ;
		:region_id = "NAM" ;
		:source = "MACA 3.0: Statistically-downscaled climate model projections based on CMIP6" ;
		:source_id = "MACA3-0" ;
		:source_name = "MACA" ;
		:source_version = "3.0" ;
		:table_id = "APday" ;
		:table_info = "Creation Date:(2025-09-03) MD5:9c77819bfbf9392f6157c58b38c2524f" ;
		:title = "MACA 3.0 dataset prepared for DRCDP" ;
		:tracking_id = "hdl:21.14100/991e1830-4c4a-464e-9bb4-3d11bf28681c" ;
		:variable_id = "tasmax" ;
		:license = "CC0 1.0; DRDCP data produced by UCM-ACSL is licensed under a Creative Commons CC0 1.0 Universal Public Domain Dedication License (https://creativecommons.org/publicdomain/zero/1.0/). Consult https://pcmdi.llnl.gov/CMIP6/TermsOfUse for terms of use governing DRDCP output, including citation requirements and proper acknowledgment. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law." ;
		:cmor_version = "3.15.1" ;
}
```
