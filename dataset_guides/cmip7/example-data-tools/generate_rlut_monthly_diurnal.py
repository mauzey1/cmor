#!/usr/bin/env python

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

import common

cmor = common.cmor


def generate(workdir: Path) -> str:
    common.configure_dataset(
        workdir,
        overrides={"Conventions": "CF-1.13", "frequency": "1hr"},
    )
    cmor.load_table("CMIP7_atmos.json")
    time_id = common.time3_axis()
    lat_id, lon_id = common.lat_lon_axes()

    data = np.linspace(180.0, 220.0, num=48 * 3 * 4, dtype="f").reshape(48, 3, 4)
    var_id = cmor.variable(
        "rlut_tclmdc-u-hxy-u",
        "W m-2",
        [time_id, lat_id, lon_id],
        positive="up",
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
