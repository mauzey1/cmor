# CMIP7 Datasets With CMOR

## Purpose

This guide explains how CMOR in this repository turns CMIP7 user input into NetCDF datasets. It is written for application developers who need to decide which fields a driver must collect, which metadata CMOR derives from the CMIP7 tables and controlled vocabulary, and how coordinate, z-factor, or chunking choices change the final file.

The worked examples are split into separate pages in this directory so each case can include:

- the user-facing dataset JSON
- the resolved output path
- the full `ncdump -h` header

All examples in this guide use the published CMIP7 controlled vocabulary file:

```text
cmip7-cmor-tables/tables-cvs/cmor-cvs.json
```

The updated published CMIP7 CV now exposes `mip_era = "CMIP7"`, `drs_specs = "MIP-DRS7"`, and `tracking_prefix = "hdl:21.14107"` as root-level strings. As a result, all validated CMIP7 examples in this guide point directly at that published CV and demonstrate CMOR 3.15.1 deriving `drs_specs`, `tracking_id`, and `mip_era` from the CV instead of from user input.

Run-specific fields such as `creation_date`, `tracking_id`, and the `vYYYYMMDD` version token vary between runs. The structural behavior shown by the examples does not.

## CMORization Workflow

CMOR builds a CMIP7 file from four inputs:

1. Dataset JSON supplied by the driver
2. The CMIP7 controlled vocabulary
3. A CMIP7 variable table entry
4. Coordinate, grid, z-factor, and data arrays supplied at runtime

The typical sequence is:

1. Initialize CMOR with the CMIP7 table directory.
2. Load dataset JSON.
3. Load the CMIP7 variable table that contains the branded variable.
4. Define the axes, grid, and z-factors required by that table entry.
5. Optionally set storage controls such as chunking on the CMOR variable before the first write.
6. Write the data arrays.
7. Close the variable and let CMOR finalize the output path, filename, and derived global metadata.

Pseudocode for a driver looks like:

```text
collect dataset JSON
select CV + coordinate table + variable table
select branded variable entry
define required axes / grid / z-factors
optionally set variable chunking
write data arrays
close output and record the CMOR-generated path
```

## Where Metadata Comes From

### Dataset JSON

The dataset JSON is where the driver declares dataset identity, output location, and any explicit overrides. Typical examples are:

- CMIP7 mode selection with `_cmip7_option`
- file selections such as `_controlled_vocabulary_file`, `_AXIS_ENTRY_FILE`, and `_FORMULA_VAR_FILE`
- dataset identity such as `activity_id`, `experiment_id`, `institution_id`, and `source_id`
- the RIPF components used to build `variant_label`
- `grid_label`, `region`, `frequency`, and `outpath`
- optional pass-through metadata such as `archive_id`, `host_collection`, or `cv_version` when a project wants them preserved in the output

Runtime storage controls such as chunking are not dataset-JSON fields in these examples. When a driver needs a non-default chunk layout, it sets that on the CMOR variable after `cmor.variable(...)` and before the first `cmor.write(...)`.

With CMOR 3.15.1, the published CMIP7 CV used by these examples contributes root-level `mip_era = CMIP7`, `drs_specs = MIP-DRS7`, and `tracking_prefix = hdl:21.14107`, so the example JSON files in this guide no longer pass any of those fields explicitly.

### Controlled Vocabulary

The CMIP7 controlled vocabulary does three main jobs:

- validates controlled values such as `activity_id`, `experiment_id`, `grid_label`, `institution_id`, `license_id`, and the RIPF indices
- expands identifiers into descriptive metadata such as `institution`, `source`, `experiment`, `description`, and `license`
- provides root-level string metadata such as `mip_era` and `data_specs_version`
- provides the DRS directory and filename templates used to build the final output path

The published CMIP7 CV in this repository uses:

```text
directory template:
<drs_specs><mip_era><activity_id><institution_id><source_id><experiment_id><variant_label><region><frequency><variable_id><branding_suffix><grid_label><version>

filename template:
<variable_id><branding_suffix><frequency><region><grid_label><source_id><experiment_id><variant_label>
```

### Variable Table Entry

The selected table entry defines the variable-specific part of the file:

- branded variable name
- dimensions
- units
- cell methods
- standard name and long name
- realm

For example, the branded variable name `tos_tavg-u-hxy-sea` is split by CMOR into:

- `variable_id = tos`
- `temporal_label = tavg`
- `vertical_label = u`
- `horizontal_label = hxy`
- `area_label = sea`
- `branding_suffix = tavg-u-hxy-sea`

That is why a driver normally supplies the branded table entry once rather than rebuilding those labels by hand.

### Coordinate, Grid, And Formula Tables

The CMIP7 coordinate and formula-term files determine which runtime objects a driver must create around the main variable:

- `CMIP7_coordinate.json` defines axis metadata such as units, bounds requirements, and entries like `height2m` or `plev19`
- `CMIP7_formula_terms.json` defines the z-factor variables and formula-term metadata needed by hybrid-coordinate outputs
- grid-aware cases still depend on runtime driver choices for auxiliary coordinates and, when relevant, CRS metadata before the main variable is written

These files do not usually add new dataset-identity fields, but they do control whether a driver must create scalar coordinates, pressure axes, hybrid z-factors, or a separate grid definition.

## User Input Reference

The tables below summarize the inputs used by the examples in this guide.

### Core CMIP7 File Selections

| Input | Required? | Default or expected value | Use in output |
| --- | --- | --- | --- |
| `_cmip7_option` | Yes | Use `1` for the CMIP7 workflow in this repository | Enables CMIP7-specific handling |
| `_controlled_vocabulary_file` | Yes | No implicit default in this guide; examples use `cmip7-cmor-tables/tables-cvs/cmor-cvs.json` | Selects the CMIP7 controlled vocabulary |
| `_AXIS_ENTRY_FILE` | Yes | No implicit default in this guide; examples use `CMIP7_coordinate.json` | Selects the coordinate definitions |
| `_FORMULA_VAR_FILE` | Conditional | No implicit default; required only when formula terms are needed | Selects the z-factor and formula-term definitions |

### Dataset Identity and DRS Inputs

| Input | Required? | Default or expected value | Use in output |
| --- | --- | --- | --- |
| `activity_id` | Yes | No default; must exist in the CV | Global attribute and DRS token |
| `experiment_id` | Yes | No default; examples mainly use `amip` | Global attribute, DRS token, and parent-lineage rules |
| `institution_id` | Yes | No default; must exist in the CV | Global attribute and DRS token |
| `source_id` | Yes | No default; must exist in the CV | Global attribute and DRS token |
| `realization_index` | Yes | No default | Builds `variant_label` |
| `initialization_index` | Yes | No default | Builds `variant_label` |
| `physics_index` | Yes | No default | Builds `variant_label` |
| `forcing_index` | Yes | No default | Builds `variant_label` |
| `drs_specs` | Optional in CMOR 3.15.1 | The validated examples omit it from dataset JSON and let the published CMIP7 CV supply `MIP-DRS7` | Global attribute and DRS token |
| `mip_era` | Optional in CMOR 3.15.1 | If omitted, the published CMIP7 CV supplies `CMIP7` from its root-level string entry | Global attribute and DRS token |
| `grid_label` | Yes | No default; must be CV-valid | Global attribute and DRS token |
| `nominal_resolution` | Yes | No default; must be CV-valid | Global attribute |
| `region` | Yes | No default; examples use `glb` | Global attribute and DRS token |
| `license_id` | Yes | No default; must be CV-valid | Used to derive `license` |
| `outpath` | Yes | No default | Filesystem root where CMOR creates the DRS tree |

### Common Optional Pass-Through Inputs

| Input | Required? | Default or expected value | Use in output |
| --- | --- | --- | --- |
| `archive_id` | Optional | Current CMIP7 unit tests use `WCRP` | Preserved as a global attribute when supplied |
| `host_collection` | Optional | Current CMIP7 unit tests use `CMIP7` | Preserved as a global attribute when supplied |
| `cv_version` | Optional | No guide-level default | Preserved as a global attribute when supplied |

### Time, Tracking, and Override Inputs

| Input | Required? | Default or expected value | Use in output |
| --- | --- | --- | --- |
| `calendar` | Required for time-varying output | No default implied by this guide; examples use `360_day` | Time-axis metadata |
| `frequency` | Required for time-varying output | No general default; use `fx` for fixed fields | Global attribute and DRS token |
| `tracking_prefix` | Optional | The validated examples omit it from dataset JSON and let the published CMIP7 CV supply `hdl:21.14107` | Prefix used when CMOR derives `tracking_id` |
| `Conventions` | Optional | If omitted, CMOR uses the table header; CMOR 3.15.1 also preserves an explicit CV-valid value such as `CF-1.13` | Global attribute override |
| `output_path_template` | Optional | If omitted, CMOR uses the CV directory template | Overrides the DRS directory layout |
| `output_file_template` | Optional | If omitted, CMOR uses the CV filename template | Overrides the DRS filename layout |
| `_history_template` | Optional | If omitted, CMOR writes its default history string | Overrides the global `history` format |

CMOR 3.15.1 derives `mip_era`, `drs_specs`, and `tracking_prefix` from the published CMIP7 CV root strings used by these examples, so all three fields can be omitted from dataset JSON when that CV is selected.

When a driver supplies `Conventions`, CMOR 3.15.1 uses that explicit value both for the global `Conventions` attribute and in the default `history` message.

### Conditional Parent-Lineage Inputs

| Input | Required? | Default or expected value | Use in output |
| --- | --- | --- | --- |
| `branch_time_in_child` | Conditional | No default | Parent-lineage metadata |
| `branch_time_in_parent` | Conditional | No default | Parent-lineage metadata |
| `parent_activity_id` | Conditional | No default | Parent-lineage metadata |
| `parent_experiment_id` | Conditional | No default | Parent-lineage metadata |
| `parent_source_id` | Conditional | No default | Parent-lineage metadata |
| `parent_time_units` | Conditional | No default | Parent-lineage metadata |
| `parent_variant_label` | Conditional | No default | Parent-lineage metadata |
| `parent_mip_era` | Conditional | No default implied by CMOR; CMIP7 examples use `CMIP7` | Parent-lineage metadata |

## Metadata CMOR Usually Derives

Drivers normally do not need to set these fields directly:

- `branded_variable`
- `branding_suffix`
- `temporal_label`
- `vertical_label`
- `horizontal_label`
- `area_label`
- `variant_label`
- `institution`
- `source`
- `realm`
- `product`
- `mip_era` when the root-level CMIP7 CV provides it, as in the published `cmor-cvs.json`
- `Conventions` unless the driver supplies an explicit CV-valid override
- `creation_date`
- `tracking_id`
- `variable_id`
- `license`
- `title`
- `version`

The most important derived identifier is `variant_label`, which is built from:

```text
realization_index + initialization_index + physics_index + forcing_index
```

For example:

```text
r9 + i1 + p1 + f3 -> r9i1p1f3
```

## Dataset Families Covered By The Examples

The linked examples below show the main dataset shapes covered by this guide.

| Example family | What changes in the output | Link |
| --- | --- | --- |
| Monthly native-grid ocean field | Standard `time` + `lat` + `lon` case on a native grid | [Monthly native-grid `tos`](examples-tos-monthly-native-grid.md) |
| Monthly curvilinear-grid ocean field | Uses `CMIP7_grids.json` and `cmor.grid(...)` to write `rlat`, `rlon`, 2-D auxiliary `latitude`/`longitude`, and vertex bounds | [Monthly curvilinear-grid `tos`](examples-tos-monthly-curvilinear-grid.md) |
| Monthly ocean field with parent metadata | Adds the required `branch_*` and `parent_*` lineage attributes | [Parented `piControl` `tos`](examples-tos-parent-picontrol.md) |
| Monthly Diurnal climatology with explicit `Conventions` override | Uses `time3`, writes `climatology_bnds`, keeps `frequency = 1hr`, and preserves `Conventions = CF-1.13` in both the global attribute and default `history` string | [Monthly Diurnal `rlut`](examples-rlut-monthly-diurnal.md) |
| Monthly ice-sheet rainfall flux | Shows a branded variable whose `area_label` and `realm` are not the simplest single-realm case | [Monthly ice-sheet `prra`](examples-prra-monthly-ice-sheet.md) |
| Monthly ocean transport by basin | Uses the character `basin` coordinate and writes `sector(basin, strlen)` as an auxiliary coordinate | [Basin auxiliary-coordinate `htovgyre`](examples-htovgyre-basin-auxiliary.md) |
| Fixed land field | Omits the time axis and uses `frequency = fx` | [Fixed `rootd`](examples-rootd-fixed.md) |
| Near-surface scalar height | Uses a singleton vertical coordinate written as a scalar `height` variable | [Scalar-height `tas`](examples-tas-height2m.md) |
| Pressure-level atmosphere field | Uses `plev19` and writes a length-19 pressure coordinate | [Pressure-level `ta`](examples-ta-plev19.md) |
| Hybrid-sigma atmosphere field | Adds z-factors and formula terms alongside the main variable | [Hybrid-sigma `hus`](examples-hus-hybrid-sigma.md) |
| Custom chunking on streamed writes | Uses `cmor.set_chunking` before writing 40 monthly slices on a `144 x 192` grid with a repack-compatible data chunk | [Custom-chunked `pr`](examples-pr-custom-chunking.md) |

## Coordinate and Grid Patterns

### Native Latitude-Longitude Grids

The standard native-grid case uses:

- `latitude` with bounds
- `longitude` with bounds
- `time` with bounds for interval data

These become `lat`, `lon`, and `time` variables in the output.

### Curvilinear Grids

Curvilinear-grid cases use `CMIP7_grids.json` and `cmor.grid(...)` when the model's horizontal grid is not represented by independent 1-D latitude and longitude axes.

The `tos_tavg-u-hxy-sea` curvilinear example uses:

- `grid_latitude` and `grid_longitude` axes from `CMIP7_grids.json`
- 2-D auxiliary `latitude` and `longitude` arrays
- 4-corner `vertices_latitude` and `vertices_longitude` arrays
- a grid id returned by `cmor.grid(...)`, passed with the time axis to `cmor.variable(...)`

In the verified output, the main data variable is written as `tos(time, rlat, rlon)` and has `coordinates = "latitude longitude"`.

### Auxiliary Character Coordinates

Some CMIP7 dimensions are character coordinates rather than numeric axes. The `htovgyre_tavg-u-hyb-sea` example uses the `basin` coordinate with three labels:

- `atlantic_arctic_ocean`
- `indian_pacific_ocean`
- `global_ocean`

CMOR writes those labels as the auxiliary coordinate `sector(basin, strlen)` and adds `coordinates = "sector"` to the main `htovgyre` variable.

### Singleton Vertical Coordinates

Some CMIP7 entries use a scalar vertical coordinate rather than a length-N dimension. Examples include `height2m` and `h100m`.

The `tas_tavg-h2m-hxy-u` example shows that CMOR writes a scalar `height` coordinate and attaches it through the variable `coordinates` attribute.

### Climatology Time Axes

CMOR 3.15.1 also supports CMIP7 climatology variables that use the `time3` coordinate entry for Monthly Diurnal output.

In that pattern:

- the driver supplies climatology bounds on `time3`
- CMOR writes the output time variable as `time`
- the output time variable carries `climatology = "climatology_bnds"`
- the output time variable keeps `long_name = "Diurnal Mean"`
- the output reports `frequency = 1hr`
- the resolved filename uses a monthly `YYYYMM-YYYYMM` time-range suffix without an extra climatology marker

### Pressure Levels

Pressure-level variables use coordinate entries such as `plev19`. The driver supplies the requested level values, and CMOR writes the pressure-coordinate metadata defined by the CMIP7 table.

### Hybrid Sigma Coordinates

Hybrid coordinates require both a vertical axis and the formula-term variables named by the coordinate definition.

For `standard_hybrid_sigma`, the output depends on:

- the hybrid coordinate values
- `a`
- `b`
- `p0`
- `ps`
- the corresponding bounds variables for `a` and `b`

### Other Grid Families

The CMIP7 tables in this repository also define rotated, projected, and unstructured horizontal grids. Those follow the same high-level pattern shown by the curvilinear `tos` example: the driver must define the grid and any auxiliary coordinates before writing the main variable.

### Chunking And Streaming Writes

Chunking is controlled at runtime on the CMOR variable, not in the dataset JSON.

The supported Python pattern is:

- create the variable with `cmor.variable(...)`
- call `cmor.set_chunking(var_id, [...])` before the first write
- write the data, including one-timestep-at-a-time streaming writes if needed

For CMIP7-style files, the practical chunking constraints are:

- time coordinate variables such as `time` and `time_bnds` should remain a single chunk or contiguous, which CMOR manages in these examples
- if a data variable has multiple chunks, target at least about `4 MiB` uncompressed per chunk
- the size rule is evaluated on the data variable chunk itself; consolidated internal metadata is a separate file-layout concern outside CMOR's chunking API
- use `ncdump -sh` when you need to show `_Storage` and `_ChunkSizes` in the generated file

The chunking example in this guide shows a custom data-variable layout of `[38, 144, 192]` for a `(time, lat, lon)` precipitation field on a `144 x 192` grid. In the verified output, the `pr` variable uses that requested chunking while `time` and `time_bnds` keep CMOR-managed coordinate chunking.

## Output Naming Rules

CMOR uses the directory and filename templates from the CMIP7 controlled vocabulary unless the driver overrides them.

With the monthly `tos` example inputs, a time-varying ocean surface field resolves to:

```text
directory:
MIP-DRS7/CMIP7/CMIP/MOHC/DUMMY-MODEL/amip/r9i1p1f3/glb/mon/tos/tavg-u-hxy-sea/g999/vYYYYMMDD/

filename:
tos_tavg-u-hxy-sea_mon_glb_g999_DUMMY-MODEL_amip_r9i1p1f3_YYYYMM-YYYYMM.nc
```

For fixed fields, `frequency = fx` produces a fixed-field DRS path and filename:

```text
MIP-DRS7/CMIP7/CMIP/MOHC/DUMMY-MODEL/amip/r9i1p1f3/glb/fx/rootd/ti-u-hxy-lnd/g999/vYYYYMMDD/
rootd_ti-u-hxy-lnd_fx_glb_g999_DUMMY-MODEL_amip_r9i1p1f3.nc
```

For CMIP7 Monthly Diurnal variables on `time3`, CMOR 3.15.1 formats the time range with the same monthly `YYYYMM-YYYYMM` suffix style used by other climatology outputs. The climatology semantics are carried by the `time:climatology` attribute, `long_name = "Diurnal Mean"`, and the branded variable's `tclmdc` temporal label rather than by an extra filename suffix.

## Parent Metadata

Parent metadata is conditional. It depends on the experiment entry selected in the controlled vocabulary.

In the published CMIP7 CV used by these examples:

- `amip` has no parent experiment
- `piControl` names `piControl-spinup` as its parent

That means:

- the `amip` examples in this guide do not need `parent_*` or `branch_*` fields
- a dataset whose experiment entry names a parent must include the required lineage metadata
- [Parented `piControl` `tos`](examples-tos-parent-picontrol.md) shows the minimal monthly case with those attributes populated

## Example Pages

Runnable scripts for these cases live under `example-data-tools/`.

- [Monthly native-grid `tos`](examples-tos-monthly-native-grid.md)
- [Monthly curvilinear-grid `tos`](examples-tos-monthly-curvilinear-grid.md)
- [Parented `piControl` `tos`](examples-tos-parent-picontrol.md)
- [Monthly Diurnal `rlut`](examples-rlut-monthly-diurnal.md)
- [Monthly ice-sheet `prra`](examples-prra-monthly-ice-sheet.md)
- [Basin auxiliary-coordinate `htovgyre`](examples-htovgyre-basin-auxiliary.md)
- [Fixed `rootd`](examples-rootd-fixed.md)
- [Scalar-height `tas`](examples-tas-height2m.md)
- [Pressure-level `ta`](examples-ta-plev19.md)
- [Hybrid-sigma `hus`](examples-hus-hybrid-sigma.md)
- [Custom-chunked `pr`](examples-pr-custom-chunking.md)

## Practical Rules for Driver Authors

- Keep dataset JSON focused on dataset identity, output location, and explicit overrides.
- Use branded CMIP7 variable names from the tables rather than rebuilding CMIP7 labels manually.
- Set the CMIP7 file selections explicitly: `_controlled_vocabulary_file`, `_AXIS_ENTRY_FILE`, and `_FORMULA_VAR_FILE`.
- Use CV-valid identifiers for `institution_id`, `source_id`, `grid_label`, and `license_id`.
- Because the published CMIP7 CV in this repository now exposes `mip_era`, `drs_specs`, and `tracking_prefix` as root-level strings, drivers can omit those inputs and let CMOR derive them from the CV. All validated examples in this guide now use that path.
- Supply `frequency` for time-varying variables, and use `fx` when a fixed-field DRS is intended.
- Let the controlled vocabulary expand `institution`, `source`, `experiment`, `license`, and the root-level `mip_era` when the CV provides it.
- Read the coordinate entry carefully for hybrid or specialized vertical coordinates and create every required formula-term variable.
- Treat chunking as a runtime write option. If a driver needs a non-default layout, call `cmor.set_chunking` on the variable before the first `cmor.write`.
- If a driver overrides `Conventions`, expect the same value to appear in both the global `Conventions` attribute and the default CMOR `history` string.
- Treat the final NetCDF path and filename as CMOR output, not driver-formatted strings.

## Summary

In this repository, a CMIP7 dataset is produced by combining:

- dataset JSON supplied by the driver
- CMIP7 controlled-vocabulary validation and metadata expansion
- CMIP7 table-driven variable definitions
- runtime axis, grid, z-factor, and data arrays

For most application builders, the shortest reliable strategy is:

1. Build a clean dataset JSON schema around the required metadata listed above.
2. Select a branded variable from the correct CMIP7 table.
3. Define exactly the axes, grids, and z-factors required by that table entry.
4. Let CMOR derive the final metadata, path, and filename.
