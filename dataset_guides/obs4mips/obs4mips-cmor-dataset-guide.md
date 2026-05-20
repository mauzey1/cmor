# obs4MIPs Datasets With CMOR

## Purpose

This guide explains how CMOR in this repository writes obs4MIPs-compliant NetCDF files from the published `PCMDI/obs4MIPs-cmor-tables` tables and controlled vocabularies. It is written for application developers who need to know which fields an obs4MIPs driver must collect directly, which metadata CMOR derives from the obs4MIPs CV and table files, and how the required input changes between regular gridded data, point-site data, and zonal-mean profile data.

The validated examples in this directory use:

- `Tables/obs4MIPs_CV.json`
- `Tables/obs4MIPs_formula_terms.json`
- `obs4MIPs_source_id.json`
- `obs4MIPs_institution_id.json`
- `obs4MIPs_site_id.json`
- `Tables/obs4MIPs_Amon.json`
- `Tables/obs4MIPs_A1hrPt.json`
- `Tables/obs4MIPs_coordinate.json`

The runnable scripts are stored under `example-data-tools/`. Each script writes a real obs4MIPs file, prints the resolved output path, and leaves the exact `user_input.json` used by CMOR in its work directory under `/private/tmp/obs4mips-guide/<case>/`.

Run-specific values such as `creation_date`, `tracking_id`, and the `vYYYYMMDD` version directory vary between runs. The structural behavior shown by the examples does not.

## CMORization Workflow

There is no repository helper that expands a minimal JSON before CMOR reads it. A driver is expected to provide the core obs4MIPs metadata itself, then let CMOR fill the pieces that come from the CV and table headers.

The validated workflow is:

1. Build a dataset JSON with the obs4MIPs file selectors plus the user-managed metadata:
   `contact`, `grid`, `grid_label`, `institution_id`, `license`, `nominal_resolution`, `product`, `references`, `source_data_url`, `source_id`, `variant_label`, and the output templates.
2. Initialize CMOR with the obs4MIPs `Tables/` directory.
3. Load the target table such as `obs4MIPs_Amon.json` or `obs4MIPs_A1hrPt.json`.
4. Define the axes required by the selected table entry.
5. If a required current-dataset attribute such as `processing_code_location` is not already in the JSON, set it before writing data.
6. Write the data and close the file. CMOR resolves the final path, filename, and the CV-derived metadata.

Pseudocode for the validated examples is:

```text
collect obs4MIPs dataset JSON
cmor.setup(inpath=<obs4MIPs Tables>)
cmor.dataset_json(<user_input.json>)
cmor.load_table(<target table>)
define required axes
write data
close file and record the CMOR-generated path
```

## Where Metadata Comes From

### User Input JSON

obs4MIPs expects the driver JSON to carry most of the human-facing dataset metadata directly. The validated examples all provide:

- `_AXIS_ENTRY_FILE`
- `_FORMULA_VAR_FILE`
- `_controlled_vocabulary_file`
- `activity_id`
- `calendar`
- `contact`
- `grid`
- `grid_label`
- `has_aux_unc`
- `institution_id`
- `license`
- `nominal_resolution`
- `outpath`
- `output_file_template`
- `output_path_template`
- `processing_code_location`
- `product`
- `references`
- `source_data_url`
- `source_id`
- `title`
- `variant_info`
- `variant_label`

The point-site example adds:

- `site_id`
- `site_location`

### Source Registry

`obs4MIPs_source_id.json` and the merged `Tables/obs4MIPs_CV.json` supply source-specific metadata. The validated runs show CMOR deriving these fields from `source_id` when they are omitted from the user JSON:

- `region`
- `source`
- `source_type`
- `source_version_number`

Examples in this guide use:

- `CMAP-V1902`
- `ARMBE-atm-c1-1-8`
- `BSVertOzone-v1-0`

### Institution Registry

`institution_id` must still be present in the user JSON. CMOR does not infer it from `source_id` in the current obs4MIPs workflow.

Once `institution_id` is present, CMOR derives:

- `institution`

from `obs4MIPs_institution_id.json`.

### Site Registry

Point-site workflows use `obs4MIPs_site_id.json` outside the variable tables. In the validated point example:

- `site_id = US-ARM`
- the driver uses the site registry to obtain latitude and longitude
- `site_location` is carried as explicit JSON metadata

### Variable, Coordinate, And Formula-Term Tables

The table entry defines the variable-specific part of the file:

- `frequency`
- `realm`
- `variable_id`
- `units`
- `cell_methods`
- `cell_measures`
- dimensions such as `longitude latitude time`, `longitude1 latitude1 time`, or `latitude height time`

The coordinate table defines the available axes and whether bounds are required:

- `latitude` and `longitude` require bounds
- `latitude1` and `longitude1` do not require bounds
- `height` does not require bounds in the validated zonal-mean profile case

`obs4MIPs_formula_terms.json` is also part of the validated dataset JSON. The selected example variables do not need z-factors, but the file remains part of the documented obs4MIPs input contract for cases that do.

### CMOR-Derived Fields

CMOR itself resolves or finalizes:

- `Conventions`
- `creation_date`
- `data_specs_version`
- `frequency`
- `history`
- `mip_era`
- `realm`
- `table_id`
- `tracking_id`
- `variable_id`

Two validated details are worth calling out:

- The `A1hrPt` point table still writes `frequency = 1hr` in the output.
- The `o3zm` table entry writes an output variable named `o3`, so both the filename and the `variable_id` global attribute use `o3`.

## Current-CV Notes

Some older demo JSON files in the target repository no longer match the current CV exactly.

The validated runs in this guide showed:

- the old `CMAP-V1902` demo JSON uses `institution_id = NOAA-ESRL-PSD`, but the current `source_id` registry maps `CMAP-V1902` to `NOAA-NCEI`
- the old in-situ demo uses `grid_label = ARM-SGP`, but that value fails current CV validation
- the current published CV also rejects `grid_label = site` for the point-site table
- the validated point-site example works with `grid = site`, `grid_label = gn`, and `site_id = US-ARM`

All three validated runs also emit the same non-fatal table-load warnings from CMOR 3.15.1:

```text
Warning: Attribute "activity_id" must be an array or object
Warning: Attribute "license" must be an array or object
```

The files are still created successfully, and the `license` global attribute is written from the user JSON.

## User Input Reference

### Core CMOR File Selectors

| Input | Required? | Verified behavior |
| --- | --- | --- |
| `_AXIS_ENTRY_FILE` | Yes | Examples use `obs4MIPs_coordinate.json` |
| `_FORMULA_VAR_FILE` | Conditional | Examples use `obs4MIPs_formula_terms.json`; not exercised by the selected variables but expected in obs4MIPs input JSONs |
| `_controlled_vocabulary_file` | Yes | Examples use `obs4MIPs_CV.json` |

### Core Dataset Metadata

| Input | Required? | Verified behavior |
| --- | --- | --- |
| `activity_id` | Yes | Current obs4MIPs CV validates `obs4MIPs` |
| `calendar` | Required for time-varying output | Examples use `standard` |
| `contact` | Yes | Passed through to the output |
| `grid` | Yes | User-facing grid description; examples use `1x1 degree latitude x longitude`, `site`, and `5 degree latitude height zonal mean` |
| `grid_label` | Yes | Must be CV-valid; examples use `gn` and `gnz` |
| `has_aux_unc` | Yes | Examples use `FALSE` |
| `institution_id` | Yes | Must be provided explicitly; CMOR then derives `institution` |
| `license` | Yes | Passed through to the output; current CMOR emits a non-fatal validation warning while loading the obs4MIPs CV |
| `nominal_resolution` | Yes | Must be CV-valid; examples use `250 km`, `site`, and `500 km` |
| `outpath` | Yes | Filesystem root where CMOR creates the obs4MIPs tree |
| `output_file_template` | Yes in this guide | Examples use `<variable_id><frequency><source_id><variant_label><grid_label>` |
| `output_path_template` | Yes in this guide | Examples use `<activity_id><institution_id><source_id><frequency><variable_id><grid_label><version>` |
| `processing_code_location` | Yes | Required global attribute in the current CV; examples set it to the local example script path |
| `product` | Yes | Examples use `observations` or `site-observations` |
| `references` | Yes | Passed through to the output |
| `source_data_url` | Yes | Passed through to the output |
| `source_id` | Yes | Must be CV-valid and drives several derived fields |
| `variant_label` | Yes | Used in the output filename |

### Common Optional Fields Used By The Examples

| Input | Required? | Verified behavior |
| --- | --- | --- |
| `title` | Optional but recommended | Passed through to the output |
| `variant_info` | Optional | Passed through to the output |

### Conditional Point-Site Fields

| Input | Required? | Verified behavior |
| --- | --- | --- |
| `site_id` | Conditional | Used for point-site datasets; example uses `US-ARM` |
| `site_location` | Optional but useful | Passed through to the output in the point-site case |

## Metadata obs4MIPs Derives

The validated examples showed that a driver can omit these fields and still get them in the output:

- `institution`
- `region`
- `source`
- `source_type`
- `source_version_number`
- `data_specs_version`
- `Conventions`
- `frequency`
- `mip_era`
- `realm`
- `table_id`
- `tracking_id`
- `variable_id`

The most important limitation is that `institution_id` is not one of the derived fields. It must be present in the user JSON even though the `source_id` registry also records it.

## Dataset Families Covered By The Examples

| Example family | What changes in the output | Link |
| --- | --- | --- |
| Monthly gridded atmosphere field | Standard `time` + `lat` + `lon` case on a regular latitude-longitude grid | [Monthly gridded `pr`](examples-pr-mon-global-grid.md) |
| Hourly in-situ point field | Uses `latitude1` and `longitude1`, keeps `grid = site`, and carries point-site metadata such as `site_id` while using `grid_label = gn` | [Hourly point-site `pr`](examples-pr-1hr-point-site.md) |
| Monthly zonal-mean vertical profile | Uses `time` + `height` + `lat`, `grid_label = gnz`, and the `o3zm` table entry that writes `o3` | [Monthly zonal-mean `o3zm`](examples-o3zm-zonal-mean.md) |

## Coordinate, Grid, And Vertical Notes

### Regular Latitude-Longitude Grids

The gridded precipitation example uses:

- `time` with bounds
- `latitude` with bounds
- `longitude` with bounds

This is the baseline obs4MIPs pattern for regular gridded products in tables such as `Amon`, `Aday`, and `A1hr`.

### Point-Site Data

The point-site example uses:

- `latitude1`
- `longitude1`
- `time` with bounds

Two current-CV details matter:

- `latitude1` and `longitude1` do not require bounds
- the current CV does not accept `grid_label = site` or the older demo value `ARM-SGP`; the validated point example uses `grid_label = gn`

The validated point output also shows that CMOR rewrites the time axis units to `days since 2018-01-01` even though the example script passes `seconds since 2018-01-01`.

### Zonal-Mean Vertical Profiles

The zonal-mean ozone example uses:

- `time` with bounds
- `height` without bounds
- `latitude` with bounds

The current `grid_label` vocabulary includes `gnz` for zonal-mean data, and that label works with the validated `o3zm` example.

### Grids And Formula Terms Not Exercised Here

The target repository also ships:

- `Tables/obs4MIPs_grids.json`
- `Tables/obs4MIPs_formula_terms.json`

The official demos bundled with the target repo, and the three high-value examples validated here, do not require:

- `cmor.grid(...)`
- `cmor.set_crs(...)`
- z-factors
- hybrid coordinates

Those features exist in the repository, but they are not needed for the representative obs4MIPs workflows covered by this guide.

## Output Naming Rules

The validated examples use:

```text
output_file_template:
<variable_id><frequency><source_id><variant_label><grid_label>

output_path_template:
<activity_id><institution_id><source_id><frequency><variable_id><grid_label><version>
```

Even though the templates are written without literal separators, CMOR resolves them into:

- path segments in the directory tree
- underscores in the filename body

With CMOR 3.15.1, this token-only `output_path_template` form produces the intended directory tree. The older slash-separated template shown in some legacy obs4MIPs demos produces doubled separators in validation runs with the current environment.

Resolved examples from this guide:

- Monthly gridded `pr`:
  `/private/tmp/obs4mips-guide/pr-mon-global-grid/out/obs4MIPs/NOAA-NCEI/CMAP-V1902/mon/pr/gn/v20260512/pr_mon_CMAP-V1902_CMORGuide_gn_197901-197902.nc`
- Hourly point-site `pr`:
  `/private/tmp/obs4mips-guide/pr-1hr-point-site/out/obs4MIPs/DOE-ARM/ARMBE-atm-c1-1-8/1hr/pr/gn/v20260512/pr_1hr_ARMBE-atm-c1-1-8_CMORGuide_gn_201801010030-201801010130.nc`
- Monthly zonal-mean `o3`:
  `/private/tmp/obs4mips-guide/o3zm-zonal-mean/out/obs4MIPs/DLR-BIRA/BSVertOzone-v1-0/mon/o3/gnz/v20260512/o3_mon_BSVertOzone-v1-0_CMORGuide_gnz_197901-197902.nc`

## Example Pages

Runnable scripts for these cases live under `example-data-tools/`.

- [Monthly gridded `pr`](examples-pr-mon-global-grid.md)
- [Hourly point-site `pr`](examples-pr-1hr-point-site.md)
- [Monthly zonal-mean `o3zm`](examples-o3zm-zonal-mean.md)
