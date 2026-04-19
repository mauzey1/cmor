#!/usr/bin/env python

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

import common

cmor = common.cmor


def generate(workdir: Path) -> str:
    common.configure_dataset(workdir)
    cmor.load_table("CMIP7_atmos.json")
    lat_id, lon_id = common.lat_lon_axes()
    time_id = common.time_axis()

    data = np.array(
        [
            [1.0, 1.2, 1.4, 1.6],
            [0.8, 1.0, 1.2, 1.4],
            [0.6, 0.8, 1.0, 1.2],
            [1.1, 1.3, 1.5, 1.7],
            [0.9, 1.1, 1.3, 1.5],
            [0.7, 0.9, 1.1, 1.3],
        ],
        dtype="f",
    ).reshape((2, 3, 4))

    var_id = cmor.variable("prra_tavg-u-hxy-is", "kg m-2 s-1", [time_id, lat_id, lon_id])
    cmor.write(var_id, data)
    return common.close_dataset(var_id)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args()
    print(generate(Path(args.workdir)))


if __name__ == "__main__":
    main()
