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


CASE_SLUG = "o3zm-zonal-mean"


def main() -> None:
    args = parse_args(CASE_SLUG)
    obs4mips_repo = Path(args.obs4mips_repo).resolve()

    user_input = {
        "_AXIS_ENTRY_FILE": "obs4MIPs_coordinate.json",
        "_FORMULA_VAR_FILE": "obs4MIPs_formula_terms.json",
        "_controlled_vocabulary_file": "obs4MIPs_CV.json",
        "activity_id": "obs4MIPs",
        "calendar": "standard",
        "contact": "greg@bodekerscientific.com, submissions-obs4mips@wcrp-cmip.org",
        "grid": "5 degree latitude height zonal mean",
        "grid_label": "gnz",
        "has_aux_unc": "FALSE",
        "institution_id": "DLR-BIRA",
        "license": (
            "Data in this file is licensed under a Creative Commons "
            "Attribution-ShareAlike 4.0 International License "
            "(https://creativecommons.org/licenses)."
        ),
        "nominal_resolution": "500 km",
        "output_file_template": DEFAULT_OUTPUT_FILE_TEMPLATE,
        "output_path_template": DEFAULT_OUTPUT_PATH_TEMPLATE,
        "processing_code_location": processing_code_location(Path(__file__)),
        "product": "observations",
        "references": (
            "Hassler, B., Kremser, S., Bodeker, G. E., Lewis, J., Nesbit, K., "
            "Davis, S. M., Chipperfield, M. P., Dhomse, S. S., and Dameris, M.: "
            "An updated version of a gap-free monthly mean zonal mean ozone "
            "database, Earth Syst. Sci. Data, 10, 1473-1490, "
            "https://doi.org/10.5194/essd-10-1473-2018, 2018."
        ),
        "source_data_url": (
            "http://www.bodekerscientific.com/data/"
            "monthly-mean-global-vertically-resolved-ozone"
        ),
        "source_id": "BSVertOzone-v1-0",
        "title": "Bodeker Scientific vertical ozone profile database",
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

    source_path = (
        obs4mips_repo / "demo" / "demo-zonalmeans" / "BSVerticalOzone_MR_GPH_Tier1.3_v1.0.nc"
    )
    with Dataset(source_path) as source:
        lat = np.asarray(source.variables["latitude"][:4], dtype="d")
        height = np.asarray(source.variables["altitude"][:3], dtype="d") * 1000.0
        raw = np.asarray(source.variables["O3"][:2, :4, :3], dtype="f")

    time_vals, time_bounds = month_bounds_for_count(
        start_year=1979,
        start_month=1,
        count=2,
        units="days since 1950-01-01 00:00:00",
    )
    lat_bounds = bounds_from_centers(lat)
    values = np.transpose(raw, (0, 2, 1))

    axis_ids = [
        cmor.axis(
            "time",
            coord_vals=time_vals,
            cell_bounds=time_bounds,
            units="days since 1950-01-01 00:00:00",
        ),
        cmor.axis("height", coord_vals=height, units="m"),
        cmor.axis(
            "latitude",
            coord_vals=lat,
            cell_bounds=lat_bounds,
            units="degrees_north",
        ),
    ]

    var_id = cmor.variable("o3zm", "mol mol-1", axis_ids, missing_value=1.0e20)
    cmor.write(var_id, values.astype("f4"), ntimes_passed=values.shape[0])
    print(finalize_case(var_id))


if __name__ == "__main__":
    main()
