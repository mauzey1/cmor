#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

import numpy as np

from common import finalize_case, parse_args, setup_case
import cmor


CASE_SLUG = "tasmax-height2m"


def main() -> None:
    args = parse_args(CASE_SLUG)
    drcdp_repo = Path(args.drcdp_repo).resolve()

    raw_user_input = {
        "activity_id": "DRCDP",
        "source_id": "LOCA2-1",
        "driving_activity_id": "CMIP",
        "driving_experiment_id": "historical",
        "driving_mip_era": "CMIP6",
        "driving_source_id": "ACCESS-CM2",
        "driving_variant_label": "r1i1p1f1",
    }

    _, _, _ = setup_case(
        case_slug=CASE_SLUG,
        table_name="DRCDP_APday.json",
        raw_user_input=raw_user_input,
        drcdp_repo=drcdp_repo,
        workdir=Path(args.workdir),
    )

    time = np.array([39811.0, 39812.0], dtype="d")
    time_bounds = np.array([[39810.5, 39811.5], [39811.5, 39812.5]], dtype="d")
    lat = np.array([32.0, 33.0, 34.0], dtype="d")
    lat_bounds = np.array([[31.5, 32.5], [32.5, 33.5], [33.5, 34.5]], dtype="d")
    lon = np.array([240.0, 241.0, 242.0, 243.0], dtype="d")
    lon_bounds = np.array(
        [[239.5, 240.5], [240.5, 241.5], [241.5, 242.5], [242.5, 243.5]],
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

    values = np.arange(2 * 3 * 4, dtype="f").reshape(2, 3, 4) + 273.15
    var_id = cmor.variable("tasmax", "K", axis_ids, missing_value=1.0e20)
    cmor.write(var_id, values, ntimes_passed=values.shape[0])
    print(finalize_case(var_id))


if __name__ == "__main__":
    main()
