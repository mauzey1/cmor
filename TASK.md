# Making a doc on how CMOR makes CMIP7 datasets with CMOR

## Overview

We want to create a document that shows the different kinds of CMIP7 datasets that CMOR can create given the required and optional input by the user.

Using the CMOR source code, example code, and cmip7-cmor-tables, create examples of user-provided input and the output that it generates. This should range across different dimension types, grids, zfactors, etc.

This document will help guide a developer in making an application that will make similar datasets with similar input.

## Guidance on creating example files

* Use the `python3 -m venv` to create the 'cmor-test-env' environment if it doesn't exist.
```
python3 -m venv cmor-test-env
source cmor-test-env/bin/activate
pip install cmor netcdf4 pyfive hdf5plugin --extra-index-url https://pcmdi.github.io/cmor
```
* Create Python programs for each example that uses CMOR to create a file.
* Use either NetCDF4 in Python or `ncdump -h ...` in CLI to get header data from files.

## Objectives

* Create a wiki-like document that gives an overview on the process of "CMORizing" files.
* Explain how parts of CMIP7's controlled vocabulary (CV) are used in creating a dataset.
* Provide a list of user input with brief descriptions of how they are used in dataset, whether they are required or optional, and any expected default values.
* Provide examples of the diffrent kinds of NetCDF files that can be created with CMOR. These examples should contain the full header output of these files.
* Examples should be in separate files that can be accessed by links in the main document.

## Rules

* Only write document files to the `wiki` directory, and code used to create example files to `wiki/example-data-tools`. Do not edit the rest of the CMOR repo or its submodules.
* This work is to be based on the CMIP7 project and any project that could be derived from it. It ignore things specific to CMIP6 and other projects. Avoid mentioning CMIP6 and other projects in the document.
* The doc should be technology-agnostic beyond JSON and NetCDF files. There is no need to include code beyond possible pseudocode.