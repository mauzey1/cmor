#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

import cmor
import numpy as np
from netCDF4 import Dataset

from common import (
    DEFAULT_OUTPUT_FILE_TEMPLATE,
    DEFAULT_OUTPUT_PATH_TEMPLATE,
    bounds_from_centers,
    finalize_case,
    month_bounds_for_count,
    parse_args,
    prepare_case,
    processing_code_location,
)


CASE_SLUG = "pr-mon-global-grid"


def main() -> None:
    args = parse_args(CASE_SLUG)
    obs4mips_repo = Path(args.obs4mips_repo).resolve()

    user_input = {
        "_AXIS_ENTRY_FILE": "obs4MIPs_coordinate.json",
        "_FORMULA_VAR_FILE": "obs4MIPs_formula_terms.json",
        "_controlled_vocabulary_file": "obs4MIPs_CV.json",
        "activity_id": "obs4MIPs",
        "calendar": "standard",
        "contact": "pingping.Xie@noaa.gov, obs4mips-panel@wcrp-cmip.org",
        "grid": "1x1 degree latitude x longitude",
        "grid_label": "gn",
        "has_aux_unc": "FALSE",
        "institution_id": "NOAA-NCEI",
        "license": (
            "Data in this file is licensed under a Creative Commons "
            "Attribution-ShareAlike 4.0 International License "
            "(https://creativecommons.org/licenses)."
        ),
        "nominal_resolution": "250 km",
        "output_file_template": DEFAULT_OUTPUT_FILE_TEMPLATE,
        "output_path_template": DEFAULT_OUTPUT_PATH_TEMPLATE,
        "processing_code_location": processing_code_location(Path(__file__)),
        "product": "observations",
        "references": (
            "Xie, P., and P.A. Arkin, 1997: Global precipitation: A 17-year "
            "monthly analysis based on gauge observations, satellite estimates, "
            "and numerical model outputs. Bull. Amer. Meteor. Soc., 78, 2539-2558."
        ),
        "source_data_url": "https://www.psl.noaa.gov/data/gridded/data.cmap.html",
        "source_id": "CMAP-V1902",
        "title": "CMAP V1902 precipitation prepared for obs4MIPs",
        "variant_info": "Example subset prepared for the CMOR dataset guide",
        "variant_label": "CMORGuide",
    }

    prepare_case(
        case_slug=CASE_SLUG,
        table_name="obs4MIPs_Amon.json",
        user_input=user_input,
        obs4mips_repo=obs4mips_repo,
        workdir=Path(args.workdir),
    )

    source_path = obs4mips_repo / "demo" / "demo-global2D" / "precip.mon.mean.nc"
    with Dataset(source_path) as source:
        lat = np.asarray(source.variables["lat"][-3:], dtype="d")[::-1]
        lon = np.asarray(source.variables["lon"][:3], dtype="d")
        raw = np.asarray(source.variables["precip"][:2, -3:, :3], dtype="f")[:, ::-1, :]

    lat_bounds = bounds_from_centers(lat)
    lon_bounds = bounds_from_centers(lon)
    time_vals, time_bounds = month_bounds_for_count(
        start_year=1979,
        start_month=1,
        count=2,
        units="hours since 1800-01-01 00:00:0.0",
    )

    axis_ids = [
        cmor.axis(
            "time",
            coord_vals=time_vals,
            cell_bounds=time_bounds,
            units="hours since 1800-01-01 00:00:0.0",
        ),
        cmor.axis(
            "latitude",
            coord_vals=lat,
            cell_bounds=lat_bounds,
            units="degrees_north",
        ),
        cmor.axis(
            "longitude",
            coord_vals=lon,
            cell_bounds=lon_bounds,
            units="degrees_east",
        ),
    ]

    values = np.where(np.isnan(raw), 1.0e20, raw / 86400.0).astype("f4")
    var_id = cmor.variable("pr", "kg m-2 s-1", axis_ids, missing_value=1.0e20)
    cmor.write(var_id, values, ntimes_passed=values.shape[0])
    print(finalize_case(var_id))


if __name__ == "__main__":
    main()
