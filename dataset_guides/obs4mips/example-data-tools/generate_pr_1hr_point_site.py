#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path

import cmor
import numpy as np
from netCDF4 import Dataset

from common import (
    DEFAULT_OUTPUT_FILE_TEMPLATE,
    DEFAULT_OUTPUT_PATH_TEMPLATE,
    finalize_case,
    parse_args,
    prepare_case,
    processing_code_location,
)


CASE_SLUG = "pr-1hr-point-site"


def main() -> None:
    args = parse_args(CASE_SLUG)
    obs4mips_repo = Path(args.obs4mips_repo).resolve()

    sites = json.loads((obs4mips_repo / "obs4MIPs_site_id.json").read_text())["site_id"]
    site_id = "US-ARM"
    site = sites[site_id]
    lat = float(site["latitude"])
    lon = float(site["longitude"]) % 360.0

    user_input = {
        "_AXIS_ENTRY_FILE": "obs4MIPs_coordinate.json",
        "_FORMULA_VAR_FILE": "obs4MIPs_formula_terms.json",
        "_controlled_vocabulary_file": "obs4MIPs_CV.json",
        "activity_id": "obs4MIPs",
        "calendar": "standard",
        "contact": "zhang40@llnl.gov, obs4mips-panel@wcrp-cmip.org",
        "grid": "site",
        "grid_label": "gn",
        "has_aux_unc": "FALSE",
        "institution_id": "DOE-ARM",
        "license": (
            "Data in this file is licensed under a Creative Commons "
            "Attribution-ShareAlike 4.0 International License "
            "(https://creativecommons.org/licenses)."
        ),
        "nominal_resolution": "site",
        "output_file_template": DEFAULT_OUTPUT_FILE_TEMPLATE,
        "output_path_template": DEFAULT_OUTPUT_PATH_TEMPLATE,
        "processing_code_location": processing_code_location(Path(__file__)),
        "product": "site-observations",
        "references": (
            "Xie, Shaocheng., and 16-coauthors, 2010: ARM climate modeling "
            "best estimate data, Bull. Amer. Meteor. Soc, 91, 13-20, "
            "doi:10.1175/2009BAMS2891.1."
        ),
        "site_id": site_id,
        "site_location": site["location"],
        "source_data_url": "https://arm.gov/data/science-data-products/vaps/armbe",
        "source_id": "ARMBE-atm-c1-1-8",
        "title": "ARMBE atmospheric point observations prepared for obs4MIPs",
        "variant_info": "Example subset prepared for the CMOR dataset guide",
        "variant_label": "CMORGuide",
    }

    prepare_case(
        case_slug=CASE_SLUG,
        table_name="obs4MIPs_A1hrPt.json",
        user_input=user_input,
        obs4mips_repo=obs4mips_repo,
        workdir=Path(args.workdir),
    )

    source_path = obs4mips_repo / "demo" / "demo-insitu" / "sample_in-situ1.nc"
    with Dataset(source_path) as source:
        raw_time = np.asarray(source.variables["time"][:2], dtype="d")
        raw = np.asarray(source.variables["precip_rate_sfc"][:2], dtype="f")

    time_bounds = np.array([[0.0, 3600.0], [3600.0, 7200.0]], dtype="d")
    axis_ids = [
        cmor.axis(
            "time",
            coord_vals=raw_time,
            cell_bounds=time_bounds,
            units="seconds since 2018-01-01",
        ),
        cmor.axis("latitude1", coord_vals=np.array([lat], dtype="d"), units="degrees_north"),
        cmor.axis("longitude1", coord_vals=np.array([lon], dtype="d"), units="degrees_east"),
    ]

    values = np.where(np.isnan(raw), 1.0e20, raw / 3600.0).astype("f4").reshape(2, 1)
    var_id = cmor.variable("pr", "kg m-2 s-1", axis_ids, missing_value=1.0e20)
    cmor.write(var_id, values, ntimes_passed=values.shape[0])
    print(finalize_case(var_id))


if __name__ == "__main__":
    main()
