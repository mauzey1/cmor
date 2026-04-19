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
    lat_id, lon_id = common.lat_lon_axes()
    time_id = common.time_axis()

    data = np.array(
        [
            [27.0, 27.1, 27.2, 27.3],
            [26.8, 26.9, 27.0, 27.1],
            [26.6, 26.7, 26.8, 26.9],
            [27.2, 27.3, 27.4, 27.5],
            [27.0, 27.1, 27.2, 27.3],
            [26.8, 26.9, 27.0, 27.1],
        ],
        dtype="f",
    ).reshape((2, 3, 4))

    var_id = cmor.variable("tos_tavg-u-hxy-sea", "degC", [time_id, lat_id, lon_id])
    cmor.write(var_id, data)
    return common.close_dataset(var_id)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args()
    print(generate(Path(args.workdir)))


if __name__ == "__main__":
    main()
