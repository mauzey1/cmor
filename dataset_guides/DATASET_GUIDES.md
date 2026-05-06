# Creating or updating a CMOR dataset guide

## Task inputs

This task assumes the coding agent is given:

* `PROJECT_REPO`: the target CMOR-table repository, either as a local path or a Git URL
* `PROJECT_NAME`: a short project name if it cannot be inferred cleanly from the repo
* `OUTPUT_DIR`: the folder to create in this repo for the new docs
* optionally, an instruction to update an existing guide in place rather than creating a new one

This task file lives under the repository's `dataset_guides/` directory. Generated guides should also live under `dataset_guides/` as sibling project directories.

If `OUTPUT_DIR` is not provided, derive it from the project name or repo slug by lowercasing it, replacing non-alphanumeric characters with underscores, and placing it under `dataset_guides/`.

Example:

* `DRCDP` -> `dataset_guides/drcdp`
* `CMIP7` -> `dataset_guides/cmip7`

## Overview

We want to create or update a project-specific dataset guide for a CMOR-table project. The output should be a self-contained documentation directory with:

* one main guide page
* several example pages, one per representative dataset pattern
* an `example-data-tools` directory containing the runnable scripts used to generate those examples

If the target guide directory already exists, update it in place rather than creating a duplicate directory elsewhere. Reuse and revise the existing guide files when they remain useful.

If this repository happens to contain older dataset-guide material, it may be used as reference material. The task must still remain executable if no pre-existing dataset-guide directory or markdown files are present.

Using the CMOR source code in this repository, the target project repo, and any example code or documentation in that repo, create examples of user-provided input and the NetCDF output that CMOR generates. Cover representative dimension types, grids, vertical coordinates, z-factors, and other project-specific patterns that are actually supported by the target project.

This guide should help an application developer understand what input a CMOR driver must collect to produce datasets for that project.

## Guidance on source material and setup

* Treat this task file as the primary specification for document structure and scope.
* If `OUTPUT_DIR` already exists, inspect its current contents first and decide whether each file should be kept, revised, replaced, or removed.
* If there are existing dataset-guide docs elsewhere in this repo, especially under `dataset_guides/cmip7/`, you may inspect them for tone or layout ideas, but the task must remain executable when no such docs exist.
* Inspect the target project repo for:
  * controlled vocabulary files
  * variable tables
  * coordinate, grid, and formula-term tables
  * example scripts, notebooks, or docs that show intended usage
* Use `python3 -m venv` to create the `cmor-test-env` environment if it does not exist.
```bash
python3 -m venv cmor-test-env
source cmor-test-env/bin/activate
pip install cmor netcdf4 pyfive hdf5plugin --extra-index-url https://pcmdi.github.io/cmor
```
* Install extra dependencies only if the target project repo requires them to generate representative outputs.
* If the target repo is only available as a remote URL, clone it into a temporary or scratch location outside the output directory and treat it as read-only.
* If cloning or dependency installation requires network access or elevated permissions, request approval rather than working around it.
* Create Python programs for each example that use CMOR to create a file.
* Use either NetCDF4 in Python or `ncdump -h ...` in the CLI to capture header data from files.
* Validate every statement in the guide against the target repo and actual generated output. Do not guess field names, defaults, or naming rules.

## Objectives

* Create a guide directory named `OUTPUT_DIR` if it does not already exist.
* Treat `OUTPUT_DIR` as a path under the repository root, typically `dataset_guides/<project_slug>`.
* Add or update a main guide markdown file in that directory. Prefer the name `<project_slug>-cmor-dataset-guide.md`.
* Add or update separate example pages in the same directory and link them from the main guide.
* Add or update code used to create example files under `OUTPUT_DIR/example-data-tools`.
* Use this document structure for the main guide unless the target project strongly justifies a small adjustment:
  * title and purpose
  * CMORization workflow
  * where metadata comes from
  * user input reference
  * dataset families covered by the examples
  * coordinate, grid, and vertical-pattern notes that apply to the target project
  * output naming rules
  * links to the example pages
* Use this structure for each example page unless the target project strongly justifies a small adjustment:
  * short title naming the dataset pattern
  * brief explanation of what the example demonstrates
  * dataset JSON or equivalent input
  * variable and coordinate choices
  * resolved output file
  * full `ncdump -h` output
* In the main guide:
  * explain the CMORization workflow for the target project
  * identify where metadata comes from: driver JSON or user input, target project CV, variable table entries, coordinate or grid definitions, formula terms, and CMOR-derived values
  * provide a list of user inputs with brief descriptions, whether they are required, optional, or conditional, and any verified defaults
  * summarize the main dataset families covered by the examples
  * explain output naming rules and show resolved path or filename patterns when possible
* In each example page:
  * show the dataset JSON or equivalent driver input actually used
  * identify the selected table, variable, axes, grid, and z-factors or formula terms when relevant
  * show the resolved output file path
  * include the full `ncdump -h` header
  * briefly explain what the example demonstrates
* Choose example cases that are representative of the target project. If the project does not support a CMIP7-style feature set, document the features it actually supports instead of forcing a one-to-one match with any prior docs.
* When updating an existing guide, preserve useful structure and filenames where practical so existing links remain stable.

## Rules

* Only write documentation files to `OUTPUT_DIR`, and code used to create example files to `OUTPUT_DIR/example-data-tools`. Do not edit the rest of the CMOR repo or the target project repo.
* The task must succeed whether `OUTPUT_DIR` already exists or not.
* Existing docs in `OUTPUT_DIR` may be edited when the task is to update that guide. Existing docs outside `OUTPUT_DIR` are reference material only unless the user explicitly asks otherwise.
* The generated docs must stand on their own and must not depend on cross-links to pre-existing pages outside `OUTPUT_DIR`.
* The new docs may use any existing dataset guide in this repo as a style reference, but the content must be based on the target project and must use that project's actual terminology, file names, CV fields, table names, and workflow.
* Do not carry CMIP7-specific wording into the generated docs unless the target project explicitly reuses the same concept or identifier.
* Do not assume the target project uses CMIP7-specific inputs such as `_cmip7_option`, `branding_suffix`, or the same DRS templates. Include only fields and behavior that are verified for the target project.
* If the target project lacks some concepts entirely, such as parent lineage, hybrid sigma coordinates, branded variable suffixes, or multiple grid families, say so plainly and omit those sections or mark them not applicable.
* Keep the docs technology-agnostic beyond JSON and NetCDF files. There is no need to include code in the docs beyond short pseudocode. Store runnable examples in `OUTPUT_DIR/example-data-tools`.
* Prefer a small set of high-value examples that collectively cover the real variation in the target tables over a large set of repetitive cases.

## Example parameterization

For the repo `https://github.com/PCMDI/DRCDP`:

* `PROJECT_REPO=https://github.com/PCMDI/DRCDP`
* `PROJECT_NAME=DRCDP`
* `OUTPUT_DIR=dataset_guides/drcdp`

The resulting directory should look roughly like:

```text
dataset_guides/drcdp/
  drcdp-cmor-dataset-guide.md
  examples-<case-1>.md
  examples-<case-2>.md
  ...
  example-data-tools/
    <scripts used to generate the example files>
```

For updating the existing CMIP7 guide in this repo:

* `PROJECT_REPO=cmip7-cmor-tables`
* `PROJECT_NAME=CMIP7`
* `OUTPUT_DIR=dataset_guides/cmip7`

In that case, update the existing files in `dataset_guides/cmip7/` in place instead of creating a new directory.
