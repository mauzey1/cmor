#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

import numpy as np

from common import finalize_case, parse_args, setup_case
import cmor


CASE_SLUG = "pr-ap1hr-regular-grid"


def main() -> None:
    args = parse_args(CASE_SLUG)
    drcdp_repo = Path(args.drcdp_repo).resolve()

    raw_user_input = {
        "activity_id": "DRCDP",
        "source_id": "EDDE2-0",
        "driving_activity_id": "CMIP",
        "driving_experiment_id": "historical",
        "driving_mip_era": "CMIP6",
        "driving_source_id": "ACCESS-CM2",
        "driving_variant_label": "r1i1p1f1",
    }

    _, _, _ = setup_case(
        case_slug=CASE_SLUG,
        table_name="DRCDP_AP1hr.json",
        raw_user_input=raw_user_input,
        drcdp_repo=drcdp_repo,
        workdir=Path(args.workdir),
    )

    time_bounds = np.array(
        [
            [39811.9583333333, 39812.0],
            [39812.0, 39812.0416666667],
        ],
        dtype="d",
    )
    time = time_bounds.mean(axis=1)
    lat = np.array([35.0, 36.0], dtype="d")
    lat_bounds = np.array([[34.5, 35.5], [35.5, 36.5]], dtype="d")
    lon = np.array([250.0, 251.0, 252.0], dtype="d")
    lon_bounds = np.array(
        [[249.5, 250.5], [250.5, 251.5], [251.5, 252.5]],
        dtype="d",
    )

    axis_ids = [
        cmor.axis(
            "time",
            coord_vals=time,
            cell_bounds=time_bounds,
            units="days since 1900-01-01",
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

    values = (np.arange(2 * 2 * 3, dtype="f").reshape(2, 2, 3) + 1.0) / 3600.0
    var_id = cmor.variable("pr", "kg m-2 s-1", axis_ids, missing_value=1.0e20)
    cmor.write(var_id, values, ntimes_passed=values.shape[0])
    print(finalize_case(var_id))


if __name__ == "__main__":
    main()
