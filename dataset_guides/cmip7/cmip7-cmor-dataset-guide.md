# CMIP7 Datasets With CMOR

## Purpose

This guide explains how CMOR in this repository turns CMIP7 user input into NetCDF datasets. It is written for application developers who need to decide which fields a driver must collect, which metadata CMOR derives from the CMIP7 tables and controlled vocabulary, and how coordinate or z-factor choices change the final file.

The worked examples are split into separate pages in this directory so each case can include:

- the user-facing dataset JSON
- the resolved output path
- the full `ncdump -h` header

All examples in this guide use the published CMIP7 controlled vocabulary file:

```text
cmip7-cmor-tables/tables-cvs/cmor-cvs.json
```

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
5. Write the data arrays.
6. Close the variable and let CMOR finalize the output path, filename, and derived global metadata.

Pseudocode for a driver looks like:

```text
collect dataset JSON
select CV + coordinate table + variable table
select branded variable entry
define required axes / grid / z-factors
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
- `drs_specs`, `grid_label`, `region`, `frequency`, and `outpath`

### Controlled Vocabulary

The CMIP7 controlled vocabulary does three main jobs:

- validates controlled values such as `activity_id`, `experiment_id`, `grid_label`, `institution_id`, `license_id`, and the RIPF indices
- expands identifiers into descriptive metadata such as `institution`, `source`, `experiment`, `description`, and `license`
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
| `drs_specs` | Yes | No default; examples use `MIP-DRS7` | Global attribute and DRS token |
| `mip_era` | Yes in this example set | Examples use `CMIP7` | Global attribute and DRS token |
| `grid_label` | Yes | No default; must be CV-valid | Global attribute and DRS token |
| `nominal_resolution` | Yes | No default; must be CV-valid | Global attribute |
| `region` | Yes | No default; examples use `glb` | Global attribute and DRS token |
| `license_id` | Yes | No default; must be CV-valid | Used to derive `license` |
| `outpath` | Yes | No default | Filesystem root where CMOR creates the DRS tree |

### Time, Tracking, and Override Inputs

| Input | Required? | Default or expected value | Use in output |
| --- | --- | --- | --- |
| `calendar` | Required for time-varying output | No default implied by this guide; examples use `360_day` | Time-axis metadata |
| `frequency` | Required for time-varying output | No general default; use `fx` for fixed fields | Global attribute and DRS token |
| `tracking_prefix` | Optional | No guide-level default; examples use `hdl:21.14107` | Prefix used when CMOR derives `tracking_id` |
| `Conventions` | Optional | If omitted, CMOR uses the table header; CMOR 3.15.0 also preserves an explicit CV-valid value such as `CF-1.13` | Global attribute override |
| `output_path_template` | Optional | If omitted, CMOR uses the CV directory template | Overrides the DRS directory layout |
| `output_file_template` | Optional | If omitted, CMOR uses the CV filename template | Overrides the DRS filename layout |
| `_history_template` | Optional | If omitted, CMOR writes its default history string | Overrides the global `history` format |

CMOR 3.15.0 can also derive `drs_specs` and `tracking_prefix` from root-level CV strings. The published CMIP7 CV in this repository still uses the existing array form for `drs_specs` and does not define `tracking_prefix`, so the validated examples continue to pass both fields explicitly.

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
| Monthly ocean field with parent metadata | Adds the required `branch_*` and `parent_*` lineage attributes | [Parented `piControl` `tos`](examples-tos-parent-picontrol.md) |
| Monthly ice-sheet rainfall flux | Shows a branded variable whose `area_label` and `realm` are not the simplest single-realm case | [Monthly ice-sheet `prra`](examples-prra-monthly-ice-sheet.md) |
| Fixed land field | Omits the time axis and uses `frequency = fx` | [Fixed `rootd`](examples-rootd-fixed.md) |
| Near-surface scalar height | Uses a singleton vertical coordinate written as a scalar `height` variable | [Scalar-height `tas`](examples-tas-height2m.md) |
| Pressure-level atmosphere field | Uses `plev19` and writes a length-19 pressure coordinate | [Pressure-level `ta`](examples-ta-plev19.md) |
| Hybrid-sigma atmosphere field | Adds z-factors and formula terms alongside the main variable | [Hybrid-sigma `hus`](examples-hus-hybrid-sigma.md) |

## Coordinate and Grid Patterns

### Native Latitude-Longitude Grids

The standard native-grid case uses:

- `latitude` with bounds
- `longitude` with bounds
- `time` with bounds for interval data

These become `lat`, `lon`, and `time` variables in the output.

### Singleton Vertical Coordinates

Some CMIP7 entries use a scalar vertical coordinate rather than a length-N dimension. Examples include `height2m` and `h100m`.

The `tas_tavg-h2m-hxy-u` example shows that CMOR writes a scalar `height` coordinate and attaches it through the variable `coordinates` attribute.

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

The CMIP7 tables in this repository also define rotated, projected, and unstructured horizontal grids. Those follow the same high-level pattern: the driver must define the grid and any auxiliary coordinates before writing the main variable. This example set focuses on native latitude-longitude output plus vertical-coordinate variation.

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

## Parent Metadata

Parent metadata is conditional. It depends on the experiment entry selected in the controlled vocabulary.

In the published CMIP7 CV used by these examples:

- `amip` has no parent experiment
- `piControl` names `piControl-spinup` as its parent

That means:

- the `amip` examples in this guide do not need `parent_*` or `branch_*` fields
- a dataset whose experiment entry names a parent must include the required lineage metadata
- [Parented `piControl` `tos`](examples-tos-parent-picontrol.md) shows the minimal monthly case with those attributes populated

## Practical Rules for Driver Authors

- Keep dataset JSON focused on dataset identity, output location, and explicit overrides.
- Use branded CMIP7 variable names from the tables rather than rebuilding CMIP7 labels manually.
- Set the CMIP7 file selections explicitly: `_controlled_vocabulary_file`, `_AXIS_ENTRY_FILE`, and `_FORMULA_VAR_FILE`.
- Use CV-valid identifiers for `institution_id`, `source_id`, `grid_label`, `license_id`, and `tracking_prefix`.
- Supply `frequency` for time-varying variables, and use `fx` when a fixed-field DRS is intended.
- Let the controlled vocabulary expand `institution`, `source`, `experiment`, and `license`.
- Read the coordinate entry carefully for hybrid or specialized vertical coordinates and create every required formula-term variable.
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
