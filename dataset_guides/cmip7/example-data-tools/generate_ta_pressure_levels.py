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
    plev_id = common.plev19_axis()

    data = np.linspace(220.0, 280.0, 2 * 19 * 3 * 4, dtype="f").reshape((2, 19, 3, 4))
    var_id = cmor.variable(
        "ta_tavg-p19-hxy-air",
        "K",
        [time_id, plev_id, lat_id, lon_id],
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
