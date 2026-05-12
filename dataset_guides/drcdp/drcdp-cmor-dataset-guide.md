# DRCDP Datasets With CMOR

## Purpose

This guide explains how CMOR in this repository writes DRCDP-compliant NetCDF files from the published `PCMDI/DRCDP` tables and CV files. It is written for application developers who need to know which values a driver must collect, which metadata DRCDP derives from `source_id` and the variable tables, and when a driver must switch from plain `lat`/`lon` axes to the separate grids workflow.

The validated examples in this directory use:

- `Tables/DRCDP_CV.json`
- `DRCDP_DRS.json`
- `Tables/DRCDP_AP1hr.json`
- `Tables/DRCDP_APday.json`
- `Tables/DRCDP_grids.json`
- the helper logic in `src/DRCDPLib.py:writeUserJson`

The runnable scripts are stored under `example-data-tools/`. Each script writes a real DRCDP file, prints the resolved output path, and leaves the exact `user_input.json` used by CMOR in its work directory under `/private/tmp/drcdp-guide/<case>/`.

Run-specific values such as `creation_date`, `tracking_id`, and the `vYYYYMMDD` version directory vary between runs. The structural behavior shown by the examples does not.

## CMORization Workflow

DRCDP in its current published form uses a small driver input plus a larger amount of CV-managed metadata.

1. Collect the minimal driver input: `activity_id`, `source_id`, the four `driving_*` fields, and `outpath`.
2. Apply the same augmentation that `DRCDPLib.writeUserJson` performs:
   `DRCDP_coordinate.json`, `DRCDP_formula_terms.json`, `DRCDP_CV.json`, the DRCDP DRS templates, `tracking_prefix`, and the DRCDP history template are added to the JSON that CMOR actually reads.
3. Initialize CMOR with the DRCDP `Tables/` directory.
4. Load either `DRCDP_AP1hr.json` or `DRCDP_APday.json`.
5. Define either:
   plain `time` + `latitude` + `longitude` axes, or
   a grid via `DRCDP_grids.json` plus `cmor.grid(...)` and `cmor.set_crs(...)`.
6. Write the variable data and close the file. CMOR resolves the DRS directory, filename, time range suffix, and derived global metadata.

Pseudocode for the validated workflow is:

```text
collect minimal DRCDP driver input
expand it with DRCDP helper defaults
cmor.setup(inpath=<DRCDP Tables>)
cmor.dataset_json(<resolved user_input.json>)
load variable table
optionally load DRCDP_grids.json and define grid + CRS
define axes or grid
write data
close file and record the CMOR-generated path
```

## Where Metadata Comes From

### Driver Input

The minimal driver input is much smaller than the final global metadata set. In the validated examples, the driver directly supplies only:

- `activity_id`
- `source_id`
- `driving_activity_id`
- `driving_experiment_id`
- `driving_mip_era`
- `driving_source_id`
- `driving_variant_label`
- `outpath`

### DRCDP Helper Logic

`src/DRCDPLib.py:writeUserJson` injects these fields before CMOR reads the JSON:

- `_AXIS_ENTRY_FILE = DRCDP_coordinate.json`
- `_FORMULA_VAR_FILE = DRCDP_formula_terms.json`
- `_controlled_vocabulary_file = DRCDP_CV.json`
- `tracking_prefix = hdl:21.14100`
- `output_path_template`
- `output_file_template`
- `_history_template`

The scripts in `example-data-tools/` reimplement this exact augmentation locally so they can run against any DRCDP checkout without importing DRCDP Python modules.

### DRCDP Controlled Vocabulary

`Tables/DRCDP_CV.json` expands `source_id` into most dataset identity fields. The validated outputs show these fields coming from the `source_id` record rather than the minimal driver JSON:

- `calendar`
- `contact`
- `further_info_url`
- `grid`
- `grid_label`
- `institution` and `institution_id`
- `license`, `license_id`, and `license_url`
- `nominal_resolution`
- `product`
- `reference`
- `region` and `region_id`
- `source`, `source_name`, and `source_version`
- `title`

The current published `source_id` values in the CV are:

- `EDDE2-0`
- `LOCA2-0`
- `LOCA2-1`
- `MACA3-0`
- `STAR-ESDM1-0`

### Variable And Grid Tables

The variable tables provide the per-variable structure:

- `frequency`
- `realm`
- `table_id`
- `variable_id`
- `units`
- `cell_methods`
- `cell_measures`
- required coordinate names such as `height2m`

`DRCDP_grids.json` is only needed when the driver writes a grid-aware field. In that case it defines:

- auxiliary 2-D `latitude` and `longitude`
- `vertices_latitude` and `vertices_longitude`
- the `crs` variable schema used by `cmor.set_crs`

### CMOR-Derived Fields

CMOR itself resolves or finalizes:

- `Conventions`
- `creation_date`
- `history`
- `tracking_id`
- the version directory token such as `v20260512`
- the filename time range suffix

For the validated DRCDP surface-height variables, CMOR also writes the scalar `height` coordinate automatically from the table metadata. The driver examples only pass `time`, `latitude`, and `longitude` axes for `tasmax`, yet the output contains `height`.

## User Input Reference

### Minimal Driver Inputs

| Input | Required? | Verified behavior |
| --- | --- | --- |
| `activity_id` | Yes | Current DRCDP CV only validates `DRCDP` |
| `source_id` | Yes | Must match a `source_id` entry in `DRCDP_CV.json`; this drives most identity metadata |
| `driving_activity_id` | Yes | Used in the DRS directory path and global metadata |
| `driving_experiment_id` | Yes | Used in the DRS directory path, filename, and global metadata |
| `driving_mip_era` | Yes | Used in the DRS directory path, filename, and global metadata |
| `driving_source_id` | Yes | Used in the DRS directory path, filename, and global metadata |
| `driving_variant_label` | Yes | Used in the DRS directory path, filename, and global metadata |
| `outpath` | Yes | Filesystem root where CMOR creates the DRCDP tree |

### Helper-Managed Inputs

| Input | Required? | Verified behavior |
| --- | --- | --- |
| `_AXIS_ENTRY_FILE` | Conditional | Required by CMOR, but the validated DRCDP workflow injects `DRCDP_coordinate.json` automatically |
| `_FORMULA_VAR_FILE` | Conditional | Injected as `DRCDP_formula_terms.json` even though the published `AP1hr` and `APday` variables in this guide do not use z-factors |
| `_controlled_vocabulary_file` | Conditional | Injected as `DRCDP_CV.json` |
| `output_path_template` | Conditional | Injected from `DRCDP_DRS.json` |
| `output_file_template` | Conditional | Injected from `DRCDP_DRS.json` |
| `tracking_prefix` | Conditional | Injected from `DRCDP_tracking_id.json` as `hdl:21.14100` |
| `_history_template` | Conditional | Injected by the DRCDP helper so CMOR writes the DRCDP-specific history string |

### Fields The Driver Does Not Need To Repeat

When the validated helper workflow is used, these are derived from the DRCDP CV rather than typed into the driver JSON:

- `calendar`
- `contact`
- `further_info_url`
- `grid`
- `grid_label`
- `institution_id`
- `license_id`
- `license_url`
- `nominal_resolution`
- `product`
- `reference`
- `region`
- `region_id`
- `source`
- `source_name`
- `source_version`
- `title`

The validated runs also showed CMOR replacing the short `license` string from the CV with the longer templated DRCDP license statement. That replacement emits a warning, but the file is still created correctly.

## Dataset Families Covered By The Examples

| Example family | What changes in the output | Link |
| --- | --- | --- |
| Hourly precipitation on a rectilinear grid | Uses `DRCDP_AP1hr.json` with plain `time`, `lat`, and `lon` axes | [Hourly `pr` on rectilinear `lat`/`lon`](examples-pr-ap1hr-regular-grid.md) |
| Daily tasmax with implicit surface height | Uses `DRCDP_APday.json`; CMOR writes scalar `height` even though the driver only passes `time`, `lat`, and `lon` | [Daily `tasmax` with implicit `height2m`](examples-tasmax-height2m.md) |
| Daily tasmax with grid metadata and CRS | Adds `DRCDP_grids.json`, 2-D auxiliary `latitude`/`longitude`, 4-corner vertices, and a `crs` variable | [Daily `tasmax` with grid and CRS metadata](examples-tasmax-grid-crs.md) |

## Coordinate, Grid, And Vertical Notes

### Rectilinear Latitude-Longitude Cases

The simplest DRCDP cases in the current tables use:

- `time` with bounds
- `latitude` with bounds
- `longitude` with bounds

This is enough for the `AP1hr` `pr` example and for the plain `APday` `tasmax` example.

### Scalar Surface Heights

The current `APday` table includes `height2m` and `height10m` variables such as `tasmax`, `tasmin`, `hursmax`, `hursmin`, `sfcWind`, `uas`, and `vas`.

The validated `tasmax` runs showed:

- the driver can pass only `time`, `latitude`, and `longitude`
- CMOR still writes a scalar `height` coordinate
- the output variable records `coordinates = "height"`

In other words, the table metadata is sufficient for the scalar near-surface height in this workflow.

### Grid-Aware Outputs

When the driver needs auxiliary 2-D latitude-longitude coordinates and CRS metadata, the validated workflow is:

1. Load `DRCDP_grids.json`
2. Define 1-D `latitude` and `longitude` axes with bounds
3. Build 2-D `latitude` and `longitude` arrays for the grid
4. Build 4-corner `vertices_latitude` and `vertices_longitude`
5. Call `cmor.grid(...)`
6. Call `cmor.set_crs(...)`
7. Create the main variable with `[time, gridId]`

The resulting file still has `lat` and `lon` dimensions, but it also contains:

- `crs`
- 2-D `latitude(lat, lon)`
- 2-D `longitude(lat, lon)`
- `vertices_latitude(lat, lon, vertices)`
- `vertices_longitude(lat, lon, vertices)`

### Formula Terms And Z-Factors

`DRCDP_formula_terms.json` ships with the repository and is injected by the helper workflow, but the currently published `DRCDP_AP1hr.json` and `DRCDP_APday.json` examples in this guide do not require:

- z-factors
- hybrid coordinates
- pressure levels
- depth coordinates

For the current DRCDP public tables, a guide focused on surface atmosphere fields is more accurate than forcing CMIP-style vertical examples that the tables do not use.

## Output Naming Rules

DRCDP stores its DRS rules in `DRCDP_DRS.json`.

Verified directory template:

```text
<activity_id>/<region_id>/<institution_id>/<source_id>/<driving_mip_era>/<driving_activity_id>/<driving_experiment_id>/<driving_source_id>/<driving_variant_label>/<frequency>/<variable_id>/<version>
```

Verified filename template:

```text
<variable_id>_<region_id>_<institution_id>_<source_id>_<driving_mip_era>_<driving_experiment_id>_<driving_source_id>_<driving_variant_label>_<frequency>_<time-range>.nc
```

The raw template in `DRCDP_DRS.json` is stored without literal separators between tokens. The validated runs show that CMOR resolves those tokens into path segments for the directory tree and underscores for the filename body.

Examples from this guide:

- Hourly `pr`:
  `/private/tmp/drcdp-guide/pr-ap1hr-regular-grid/out/DRCDP/NAM/EPA/EDDE2-0/CMIP6/CMIP/historical/ACCESS-CM2/r1i1p1f1/1hr/pr/v20260512/pr_NAM_EPA_EDDE2-0_CMIP6_historical_ACCESS-CM2_r1i1p1f1_1hr_200812312330-200901010030.nc`
- Daily `tasmax`:
  `/private/tmp/drcdp-guide/tasmax-height2m/out/DRCDP/NAM/UCSD-SIO/LOCA2-1/CMIP6/CMIP/historical/ACCESS-CM2/r1i1p1f1/day/tasmax/v20260512/tasmax_NAM_UCSD-SIO_LOCA2-1_CMIP6_historical_ACCESS-CM2_r1i1p1f1_day_20081231-20090101.nc`

## Example Pages

- [Hourly `pr` on rectilinear `lat`/`lon`](examples-pr-ap1hr-regular-grid.md)
- [Daily `tasmax` with implicit `height2m`](examples-tasmax-height2m.md)
- [Daily `tasmax` with grid and CRS metadata](examples-tasmax-grid-crs.md)
