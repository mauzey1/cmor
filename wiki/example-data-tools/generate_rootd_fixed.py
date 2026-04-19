#!/usr/bin/env python

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

import common

cmor = common.cmor


def generate(workdir: Path) -> str:
    common.configure_dataset(workdir, overrides={"frequency": "fx"})
    cmor.load_table("CMIP7_land.json")
    lat_id, lon_id = common.lat_lon_axes()

    data = np.array(
        [
            [0.5, 0.6, 0.7, 0.8],
            [0.9, 1.0, 1.1, 1.2],
            [1.3, 1.4, 1.5, 1.6],
        ],
        dtype="f",
    )

    var_id = cmor.variable("rootd_ti-u-hxy-lnd", "m", [lat_id, lon_id])
    cmor.write(var_id, data)
    return common.close_dataset(var_id)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args()
    print(generate(Path(args.workdir)))


if __name__ == "__main__":
    main()
