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
    num_lat = 144
    num_lon = 192
    lat_bnds = np.linspace(-90.0, 90.0, num_lat + 1, dtype="d")
    lat = (lat_bnds[:-1] + lat_bnds[1:]) / 2.0
    lon_bnds = np.linspace(0.0, 360.0, num_lon + 1, dtype="d")
    lon = (lon_bnds[:-1] + lon_bnds[1:]) / 2.0
    lat_id = cmor.axis(
        table_entry="latitude",
        units="degrees_north",
        coord_vals=lat,
        cell_bounds=lat_bnds,
    )
    lon_id = cmor.axis(
        table_entry="longitude",
        units="degrees_east",
        coord_vals=lon,
        cell_bounds=lon_bnds,
    )
    time_id = cmor.axis(
        table_entry="time",
        units="days since 1979-01-01",
    )

    num_times = 40
    time_vals = np.arange(num_times, dtype="d") * 30.0 + 15.0
    time_bnds = np.arange(num_times + 1, dtype="d") * 30.0

    var_id = cmor.variable("pr_tavg-u-hxy-u", "kg m-2 s-1", [time_id, lat_id, lon_id])
    # Use full horizontal slices and a large enough time chunk to satisfy
    # cmip7_repack/check_cmip7_packing without further rechunking.
    cmor.set_chunking(var_id, [38, num_lat, num_lon])

    for index in range(num_times):
        base = np.add.outer(
            np.linspace(0.8, 1.2, num_lat, dtype="f"),
            np.linspace(0.0, 0.4, num_lon, dtype="f"),
        )
        data = base + np.float32(index) * np.float32(0.01)
        cmor.write(
            var_id,
            data,
            time_vals=time_vals[index],
            time_bnds=time_bnds[index:index + 2],
        )

    return common.close_dataset(var_id)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args()
    print(generate(Path(args.workdir)))


if __name__ == "__main__":
    main()
