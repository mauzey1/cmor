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
    height_id = common.height2m_axis()

    data = np.linspace(280.0, 286.0, 24, dtype="f").reshape((4, 3, 2, 1))
    var_id = cmor.variable(
        "tas_tavg-h2m-hxy-u",
        "K",
        [lon_id, lat_id, time_id, height_id],
    )
    cmor.write(var_id, data)
    return common.close_dataset(var_id)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args()
    print(generate(Path(args.workdir)))


if __name__ == "__main__":
    main()
