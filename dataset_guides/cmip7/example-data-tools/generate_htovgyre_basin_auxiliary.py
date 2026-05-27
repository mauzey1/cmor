#!/usr/bin/env python

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

import common

cmor = common.cmor


def generate(workdir: Path) -> str:
    common.configure_dataset(workdir)
    cmor.load_table("CMIP7_ocean.json")

    lat = np.array([10.0, 20.0, 30.0], dtype="d")
    lat_bnds = np.array([5.0, 15.0, 25.0, 35.0], dtype="d")
    lat_id = cmor.axis(
        table_entry="latitude",
        units="degrees_north",
        coord_vals=lat,
        cell_bounds=lat_bnds,
    )

    basin_id = cmor.axis(
        table_entry="basin",
        units="",
        coord_vals=[
            "atlantic_arctic_ocean",
            "indian_pacific_ocean",
            "global_ocean",
        ],
    )
    time_id = common.time_axis()

    data = np.array(
        [
            [-80.0, -84.0, -88.0],
            [-100.0, -104.0, -76.0],
            [-120.0, -92.0, -96.0],
            [-79.0, -83.0, -87.0],
            [-99.0, -103.0, -75.0],
            [-107.0, -111.0, -115.0],
        ],
        dtype="f",
    ).reshape((2, 3, 3))

    var_id = cmor.variable("htovgyre_tavg-u-hyb-sea", "W", [time_id, basin_id, lat_id])
    cmor.write(var_id, data)
    return common.close_dataset(var_id)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args()
    print(generate(Path(args.workdir)))


if __name__ == "__main__":
    main()
