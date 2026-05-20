# Example: Daily Tasmax With An Implicit `height2m` Coordinate

## What This Example Demonstrates

This example writes `tasmax` from `DRCDP_APday.json` using only `time`, `latitude`, and `longitude` axes. It demonstrates that the near-surface `height2m` requirement is resolved by CMOR from the table metadata, so the output contains a scalar `height` coordinate even though the driver never calls `cmor.axis("height2m", ...)`.

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
  "outpath": "/private/tmp/drcdp-guide/tasmax-height2m/out",
  "output_file_template": "<variable_id><region_id><institution_id><source_id><driving_mip_era><driving_experiment_id><driving_source_id><driving_variant_label><frequency>",
  "output_path_template": "<activity_id><region_id><institution_id><source_id><driving_mip_era><driving_activity_id><driving_experiment_id><driving_source_id><driving_variant_label><frequency><variable_id><version>",
  "source_id": "LOCA2-1",
  "tracking_prefix": "hdl:21.14100"
}
```

## Variable And Coordinate Choices

- Table: `DRCDP_APday.json`
- Variable entry: `tasmax`
- Axes passed by the driver: `time`, `latitude`, `longitude`
- Implicit vertical coordinate: `height2m` from the table becomes scalar `height` in the output
- Source-driven metadata: the `LOCA2-1` CV entry supplies `institution_id = UCSD-SIO`, `region_id = NAM`, `nominal_resolution = 5 km`, and the title and contact metadata

## Resolved Output File

```text
/private/tmp/drcdp-guide/tasmax-height2m/out/DRCDP/NAM/UCSD-SIO/LOCA2-1/CMIP6/CMIP/historical/ACCESS-CM2/r1i1p1f1/day/tasmax/v20260512/tasmax_NAM_UCSD-SIO_LOCA2-1_CMIP6_historical_ACCESS-CM2_r1i1p1f1_day_20081231-20090101.nc
```

## Full `ncdump -h` Output

```text
netcdf tasmax_NAM_UCSD-SIO_LOCA2-1_CMIP6_historical_ACCESS-CM2_r1i1p1f1_day_20081231-20090101 {
dimensions:
	time = UNLIMITED ; // (2 currently)
	lat = 3 ;
	lon = 4 ;
	bnds = 2 ;
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
		tasmax:history = "2026-05-12T23:11:31Z altered by CMOR: Treated scalar dimension: \'height\'." ;
		tasmax:coordinates = "height" ;
		tasmax:missing_value = 1.e+20f ;
		tasmax:_FillValue = 1.e+20f ;

// global attributes:
		:Conventions = "CF-1.7 CMIP-6.5" ;
		:activity_id = "DRCDP" ;
		:contact = "Daniel Feldman; DRFeldman@lbl.gov" ;
		:creation_date = "2026-05-12T23:11:31Z" ;
		:data_specs_version = "6.5.0.0; mip-cmor-tables; f42386929a0057ed15e66a3bac045b8c00d33c0f" ;
		:driving_activity_id = "CMIP" ;
		:driving_experiment_id = "historical" ;
		:driving_mip_era = "CMIP6" ;
		:driving_source_id = "ACCESS-CM2" ;
		:driving_variant_label = "r1i1p1f1" ;
		:external_variables = "areacella" ;
		:frequency = "day" ;
		:further_info_url = "https://loca.ucsd.edu/" ;
		:grid = "5 x 5 km latitude x longitude" ;
		:grid_label = "gn" ;
		:history = "2026-05-12T23:11:31Z; CMOR rewrote data to be consistent with DRCDP, CMIP6, CMIP6Plus and CF-1.7 CMIP-6.5 standards" ;
		:institution = "Scripps Institution of Oceanography, University of California, San Diego, 9500 Gilman Drive, La Jolla, CA 92093, USA (ROR: 04v7hvq31)" ;
		:institution_id = "UCSD-SIO" ;
		:license_id = "CC BY 4.0" ;
		:license_url = "https://creativecommons.org/licenses/by/4.0/" ;
		:nominal_resolution = "5 km" ;
		:product = "downscaled-statistical" ;
		:realm = "atmos" ;
		:reference = "Pierce, David W., Daniel R. Cayan, and Bridget L. Thrasher (2014) Statistical downscaling using Localized Constructed Analogs (LOCA). Journal of Hydrometeorology, 15 (6), pp 2558-2585. https://doi.org/10.1175/JHM-D-14-0082.1" ;
		:region = "north_america" ;
		:region_id = "NAM" ;
		:source = "LOCA 2.1: Statistically-downscaled climate model projections based on CMIP6" ;
		:source_id = "LOCA2-1" ;
		:source_name = "LOCA" ;
		:source_version = "2.1" ;
		:table_id = "APday" ;
		:table_info = "Creation Date:(2025-09-03) MD5:9c77819bfbf9392f6157c58b38c2524f" ;
		:title = "LOCA 2.1 dataset prepared for DRCDP" ;
		:tracking_id = "hdl:21.14100/f639caed-cef7-4156-a6c1-c9699e354079" ;
		:variable_id = "tasmax" ;
		:license = "CC BY 4.0; DRDCP data produced by UCSD-SIO is licensed under a Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/). Consult https://pcmdi.llnl.gov/CMIP6/TermsOfUse for terms of use governing DRDCP output, including citation requirements and proper acknowledgment. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law." ;
		:cmor_version = "3.15.1" ;
}
```
