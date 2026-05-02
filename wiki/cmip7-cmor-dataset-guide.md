# CMIP7 Datasets With CMOR

## Purpose

This guide describes how CMOR in this repository turns CMIP7 user input into NetCDF datasets. It is aimed at application developers who need to build a driver that produces CMIP7 output while keeping most logic in JSON metadata, table selection, coordinate definitions, and array writes.

The worked examples in `wiki/` use the published CMIP7 controlled vocabulary file:

```text
cmip7-cmor-tables/tables-cvs/cmor-cvs.json
```

The example pages in this guide were regenerated on 2026-05-02 with `cmor 3.14.3` from conda-forge. Run-specific values such as `creation_date`, `tracking_id`, and the `v20260501` directory token reflect that generation run.

## Example Environment

The CMIP7 examples in this guide were run from a `cmor-test-env` conda environment created from the task instructions and updated to `cmor 3.14.3`:

```text
conda create -n cmor-test-env -c conda-forge python=3.13 pyfive udunits2 hdf5plugin cmor=3.14.3 netcdf4
conda activate cmor-test-env
```

With that environment and the current CMIP7 tables in this repository, the example runs below complete cleanly and write the documented files without the earlier CV warnings.

## Mental Model

CMOR builds a CMIP7 file from four inputs:

1. Dataset JSON supplied by the driver
2. The CMIP7 controlled vocabulary
3. A CMIP7 variable table entry
4. Coordinate, grid, z-factor, and data arrays supplied at runtime

The typical sequence is:

1. Initialize CMOR with the CMIP7 table directory.
2. Load dataset JSON.
3. Load one CMIP7 variable table such as `CMIP7_ocean.json`, `CMIP7_atmos.json`, or `CMIP7_land.json`.
4. Define the axes, and define a grid or z-factors when the chosen variable requires them.
5. Define the variable using its branded CMIP7 table entry.
6. Write the data arrays.
7. Close the variable and let CMOR finalize the output path, filename, and global metadata.

## How Metadata Is Derived

### Dataset JSON

The dataset JSON is where the driver declares dataset identity, output location, and any template or metadata overrides. Important examples are:

- CMIP7 mode selection with `_cmip7_option`
- the controlled vocabulary, coordinate, and formula-term files
- dataset identity such as `activity_id`, `experiment_id`, `institution_id`, and `source_id`
- the RIPF components used to build `variant_label`
- `drs_specs`, `grid_label`, `region`, `frequency`, and `outpath`

### Controlled Vocabulary

The CMIP7 controlled vocabulary does three main jobs:

- validates controlled values such as `activity_id`, `experiment_id`, `grid_label`, `institution_id`, `license_id`, and the RIPF indices
- expands identifiers into descriptive metadata such as `institution`, `source`, `experiment`, `description`, and `license`
- provides the DRS directory and filename templates used to build the final output path

The directory template in the published CMIP7 CV is:

```text
<drs_specs><mip_era><activity_id><institution_id><source_id><experiment_id><variant_label><region><frequency><variable_id><branding_suffix><grid_label><version>
```

The filename template is:

```text
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

That is why the driver normally supplies the branded table entry once rather than setting each label attribute manually.

## User Input Reference

The table below summarizes the main inputs used by the examples in this guide.

| Input | Use in output | Required? | Notes |
| --- | --- | --- | --- |
| `_cmip7_option` | Enables CMIP7 metadata handling | Yes | Use `1` for the CMIP7 workflow in this repository |
| `_controlled_vocabulary_file` | Selects the CMIP7 controlled vocabulary JSON | Yes | The examples use `cmip7-cmor-tables/tables-cvs/cmor-cvs.json` |
| `_AXIS_ENTRY_FILE` | Selects the coordinate table | Yes | Use `CMIP7_coordinate.json` |
| `_FORMULA_VAR_FILE` | Selects the formula-term table | Required when formula terms are needed | Use `CMIP7_formula_terms.json` |
| `activity_id` | Global attribute and DRS token | Yes | Must exist in the CV |
| `experiment_id` | Global attribute and DRS token | Yes | The examples use `amip` because it does not require parent metadata |
| `institution_id` | Global attribute and DRS token | Yes | Must exist in the CV |
| `source_id` | Global attribute and DRS token | Yes | Must exist in the CV |
| `realization_index` | Part of `variant_label` | Yes | Example value: `r9` |
| `initialization_index` | Part of `variant_label` | Yes | Example value: `i1` |
| `physics_index` | Part of `variant_label` | Yes | Example value: `p1` |
| `forcing_index` | Part of `variant_label` | Yes | Example value: `f3` |
| `drs_specs` | Global attribute and DRS token | Yes | The examples use `MIP-DRS7` |
| `mip_era` | Global attribute and DRS token | Yes for the example set | The examples use `CMIP7` |
| `grid_label` | Global attribute and DRS token | Yes | The published demo CV currently accepts values such as `g999` |
| `nominal_resolution` | Global attribute | Yes | Must exist in the CV |
| `region` | Global attribute and DRS token | Yes | The examples use `glb` |
| `license_id` | Used to build `license` | Yes | The published demo CV uses values such as `CC-BY-4.0` |
| `calendar` | Time-axis metadata | Required for time-varying output | Examples use `360_day` |
| `frequency` | Global attribute and DRS token | Required for time-varying output | Use `fx` for fixed fields |
| `outpath` | Filesystem root for output | Yes | CMOR creates the rest of the DRS path under this location |
| `tracking_prefix` | Prefix for `tracking_id` | Optional but typically set | The examples use `hdl:21.14107` because it matches the published CV regex |
| `output_path_template` | Overrides the CV directory template | No | Use only when a custom path is required |
| `output_file_template` | Overrides the CV filename template | No | Use only when a custom filename is required |
| `_history_template` | Overrides default history text | No | Usually not needed |
| `branch_time_in_child` | Parent-lineage metadata | Conditional | Required when the selected experiment names a parent |
| `branch_time_in_parent` | Parent-lineage metadata | Conditional | Required when the selected experiment names a parent |
| `parent_activity_id` | Parent-lineage metadata | Conditional | Required when the selected experiment names a parent |
| `parent_experiment_id` | Parent-lineage metadata | Conditional | Required when the selected experiment names a parent |
| `parent_source_id` | Parent-lineage metadata | Conditional | Required when the selected experiment names a parent |
| `parent_time_units` | Parent-lineage metadata | Conditional | Required when the selected experiment names a parent |
| `parent_variant_label` | Parent-lineage metadata | Conditional | Required when the selected experiment names a parent |
| `parent_mip_era` | Parent-lineage metadata | Conditional | Use `CMIP7` for CMIP7 parent datasets |

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
- `Conventions`
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

With the example inputs used here:

```text
r9 + i1 + p1 + f3 -> r9i1p1f3
```

## Coordinate and Grid Families

The CMIP7 coordinate tables used in this repository cover several common dataset shapes.

### Latitude and Longitude

The standard native-grid case uses:

- `latitude` with bounds
- `longitude` with bounds
- `time` with bounds for interval data

These become `lat`, `lon`, and `time` variables in the output.

### Singleton Vertical Coordinates

Some CMIP7 entries use a scalar vertical coordinate rather than a length-N dimension. Examples include:

- `height2m`
- `h100m`

The `tas_tavg-h2m-hxy-u` example shows that CMOR writes a scalar `height` coordinate and attaches it through the variable `coordinates` attribute.

### Pressure Levels

Pressure-level variables use coordinate entries such as `plev19`. The driver must supply the requested coordinate values, and CMOR writes the output pressure coordinate metadata from the table definition.

### Hybrid Sigma Coordinates

Hybrid coordinates require both a vertical axis and the formula-term variables named by the coordinate definition.

For `standard_hybrid_sigma`, the output depends on:

- the hybrid coordinate values
- `a`
- `b`
- `p0`
- `ps`
- the corresponding bounds variables for `a` and `b`

### Rotated, Projected, and Unstructured Grids

The CMIP7 grid tables also support:

- rotated-pole coordinates
- projected `x` and `y` coordinates
- indexed unstructured grids
- mapping metadata through mapping entries

Those cases require the driver to define the grid and its auxiliary coordinates before the main variable is written.

## Output Naming Rules

CMOR uses the directory and filename templates from the published CMIP7 controlled vocabulary unless the driver overrides them.

With the example monthly inputs used here, a monthly ocean surface field resolves to:

```text
directory:
MIP-DRS7/CMIP7/CMIP/MOHC/DUMMY-MODEL/amip/r9i1p1f3/glb/mon/tos/tavg-u-hxy-sea/g999/vYYYYMMDD/

filename:
tos_tavg-u-hxy-sea_mon_glb_g999_DUMMY-MODEL_amip_r9i1p1f3_YYYYMM-YYYYMM.nc
```

For fixed fields, `frequency = fx` produces an explicit fixed-field DRS path and filename:

```text
MIP-DRS7/CMIP7/CMIP/MOHC/DUMMY-MODEL/amip/r9i1p1f3/glb/fx/rootd/ti-u-hxy-lnd/g999/vYYYYMMDD/
rootd_ti-u-hxy-lnd_fx_glb_g999_DUMMY-MODEL_amip_r9i1p1f3.nc
```

## Example Pages

The full worked examples are kept in separate files so each case can include the complete NetCDF header.

| Example | What it shows | Link |
| --- | --- | --- |
| Monthly native-grid ocean field | Basic lat/lon/time dataset on a native grid | [Monthly native-grid `tos`](examples-tos-monthly-native-grid.md) |
| Monthly ice-sheet rainfall flux | Multi-realm branding and a masked area label | [Monthly ice-sheet `prra`](examples-prra-monthly-ice-sheet.md) |
| Fixed land field | Time-independent output with `frequency = fx` | [Fixed `rootd`](examples-rootd-fixed.md) |
| Near-surface scalar height | Singleton vertical coordinate written as a scalar `height` variable | [Scalar-height `tas`](examples-tas-height2m.md) |
| Pressure-level atmosphere field | Standard pressure-level coordinate with `plev19` | [Pressure-level `ta`](examples-ta-plev19.md) |
| Hybrid-sigma atmosphere field | Hybrid axis plus z-factors and formula terms | [Hybrid-sigma `hus`](examples-hus-hybrid-sigma.md) |

## Parent Metadata

Parent metadata is conditional. It depends on the experiment entry selected in the controlled vocabulary.

In the published CMIP7 CV used by these examples:

- `amip` has no parent experiment
- `piControl` names `piControl-spinup` as its parent

That means:

- the `amip` examples in this guide do not need `parent_*` or `branch_*` fields
- a dataset whose experiment entry names a parent must include the required lineage metadata

## Practical Rules for Driver Authors

- Keep dataset JSON focused on dataset identity, output location, and explicit overrides.
- Use branded CMIP7 variable names from the tables rather than rebuilding CMIP7 labels by hand.
- Set the CMIP7 file selections explicitly: `_controlled_vocabulary_file`, `_AXIS_ENTRY_FILE`, and `_FORMULA_VAR_FILE`.
- Use CV-valid identifiers for `institution_id`, `source_id`, `grid_label`, `license_id`, and `tracking_prefix`.
- Supply `frequency` for time-varying variables, and use `fx` when a fixed-field DRS is intended.
- Let the controlled vocabulary expand `institution`, `source`, `experiment`, and `license` instead of copying those strings into the driver.
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
