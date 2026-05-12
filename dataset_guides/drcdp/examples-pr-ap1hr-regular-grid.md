# Example: Hourly Precipitation On A Rectilinear Latitude-Longitude Grid

This example writes `pr` from `DRCDP_AP1hr.json` using plain `time`, `latitude`, and `longitude` axes. It demonstrates the smallest validated DRCDP workflow and shows that `frequency = 1hr` comes from the table entry rather than from the driver JSON.

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
  "outpath": "/private/tmp/drcdp-guide/pr-ap1hr-regular-grid/out",
  "output_file_template": "<variable_id><region_id><institution_id><source_id><driving_mip_era><driving_experiment_id><driving_source_id><driving_variant_label><frequency>",
  "output_path_template": "<activity_id><region_id><institution_id><source_id><driving_mip_era><driving_activity_id><driving_experiment_id><driving_source_id><driving_variant_label><frequency><variable_id><version>",
  "source_id": "EDDE2-0",
  "tracking_prefix": "hdl:21.14100"
}
```

## Variable And Coordinate Choices

- Table: `DRCDP_AP1hr.json`
- Variable entry: `pr`
- Axes: `time`, `latitude`, `longitude`
- Frequency: derived by CMOR from the `AP1hr` table entry
- Source-driven metadata: the `EDDE2-0` CV entry supplies `institution_id = EPA`, `region_id = NAM`, `grid = 10 x 10 km latitude x longitude`, and the license fields

## Output File

```text
/private/tmp/drcdp-guide/pr-ap1hr-regular-grid/out/DRCDP/NAM/EPA/EDDE2-0/CMIP6/CMIP/historical/ACCESS-CM2/r1i1p1f1/1hr/pr/v20260512/pr_NAM_EPA_EDDE2-0_CMIP6_historical_ACCESS-CM2_r1i1p1f1_1hr_200812312330-200901010030.nc
```

## Full `ncdump -h` Output

```text
netcdf pr_NAM_EPA_EDDE2-0_CMIP6_historical_ACCESS-CM2_r1i1p1f1_1hr_200812312330-200901010030 {
dimensions:
	time = UNLIMITED ; // (2 currently)
	lat = 2 ;
	lon = 3 ;
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
	float pr(time, lat, lon) ;
		pr:standard_name = "precipitation_flux" ;
		pr:long_name = "Precipitation" ;
		pr:comment = "includes both liquid and solid phases" ;
		pr:units = "kg m-2 s-1" ;
		pr:cell_methods = "area: time: mean" ;
		pr:cell_measures = "area: areacella" ;
		pr:missing_value = 1.e+20f ;
		pr:_FillValue = 1.e+20f ;

// global attributes:
		:Conventions = "CF-1.7 CMIP-6.5" ;
		:activity_id = "DRCDP" ;
		:contact = "Megan Mallard; Mallard.Megan@epa.gov" ;
		:creation_date = "2026-05-12T23:11:30Z" ;
		:data_specs_version = "6.5.0.0; mip-cmor-tables; f42386929a0057ed15e66a3bac045b8c00d33c0f" ;
		:driving_activity_id = "CMIP" ;
		:driving_experiment_id = "historical" ;
		:driving_mip_era = "CMIP6" ;
		:driving_source_id = "ACCESS-CM2" ;
		:driving_variant_label = "r1i1p1f1" ;
		:external_variables = "areacella" ;
		:frequency = "1hr" ;
		:grid = "10 x 10 km latitude x longitude" ;
		:grid_label = "gn" ;
		:history = "2026-05-12T23:11:30Z; CMOR rewrote data to be consistent with DRCDP, CMIP6, CMIP6Plus and CF-1.7 CMIP-6.5 standards" ;
		:institution = "United States Environmental Protection Agency, National Exposure Research Laboratory (NERL), Systems Exposure Division, 109 T.W. Alexander Drive, Durham, NC 27709, USA (ROR: 03tns0030)" ;
		:institution_id = "EPA" ;
		:license_id = "CC BY 4.0" ;
		:license_url = "https://creativecommons.org/licenses/by/4.0/" ;
		:nominal_resolution = "10 km" ;
		:product = "downscaled-statistical" ;
		:realm = "atmos" ;
		:reference = "Nolte, Christopher G., Tanya L. Spero, Jared H. Bowden, Marcus C. Sarofim, Jeremy Martinich, Megan S. Mallard (2021) Regional temperature-ozone relationships across the U.S. under multiple climate and emissions scenarios. Journal of the Air & Waste Management Association 74 (10), pp 1251-1264. https://doi.org/10.1080/10962247.2021.1970048" ;
		:region = "north_america" ;
		:region_id = "NAM" ;
		:source = "EDDE 2.0: EPA Dynamically Downscaled Ensemble based on CMIP5" ;
		:source_id = "EDDE2-0" ;
		:source_name = "EDDE" ;
		:source_version = "2.0" ;
		:table_id = "AP1hr" ;
		:table_info = "Creation Date:(2025-09-03) MD5:1dcb9c887cc3909e984b64655b17e21e" ;
		:title = "EDDE 2.0 dataset prepared for DRCDP" ;
		:tracking_id = "hdl:21.14100/778e9856-1fbe-4fd9-b530-16bb78b5cf32" ;
		:variable_id = "pr" ;
		:license = "CC BY 4.0; DRDCP data produced by EPA is licensed under a Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/). Consult https://pcmdi.llnl.gov/CMIP6/TermsOfUse for terms of use governing DRDCP output, including citation requirements and proper acknowledgment. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law." ;
		:cmor_version = "3.15.0" ;
}
```

