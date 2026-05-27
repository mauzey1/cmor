#!/usr/bin/env python

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

import common

cmor = common.cmor


def generate(workdir: Path) -> str:
    common.configure_dataset(workdir)

    grid_table = cmor.load_table("CMIP7_grids.json")
    cmor.set_table(grid_table)

    rlat = np.array([-1.0, 0.0, 1.0], dtype="d")
    rlat_bnds = np.array([-1.5, -0.5, 0.5, 1.5], dtype="d")
    rlon = np.array([0.0, 1.0, 2.0, 3.0], dtype="d")
    rlon_bnds = np.array([-0.5, 0.5, 1.5, 2.5, 3.5], dtype="d")

    rlat_id = cmor.axis(
        table_entry="grid_latitude",
        units="degrees",
        coord_vals=rlat,
        cell_bounds=rlat_bnds,
    )
    rlon_id = cmor.axis(
        table_entry="grid_longitude",
        units="degrees",
        coord_vals=rlon,
        cell_bounds=rlon_bnds,
    )

    rlat_2d, rlon_2d = np.meshgrid(rlat, rlon, indexing="ij")
    latitude = 35.0 + rlat_2d + 0.05 * rlon_2d
    longitude = np.mod(210.0 + 1.4 * rlon_2d + 0.08 * rlat_2d, 360.0)

    lat_vertices = np.empty((rlat.size, rlon.size, 4), dtype="d")
    lon_vertices = np.empty((rlat.size, rlon.size, 4), dtype="d")
    for j in range(rlat.size):
        for i in range(rlon.size):
            cell_rlat = np.array(
                [rlat_bnds[j], rlat_bnds[j], rlat_bnds[j + 1], rlat_bnds[j + 1]],
                dtype="d",
            )
            cell_rlon = np.array(
                [rlon_bnds[i], rlon_bnds[i + 1], rlon_bnds[i + 1], rlon_bnds[i]],
                dtype="d",
            )
            lat_vertices[j, i, :] = 35.0 + cell_rlat + 0.05 * cell_rlon
            lon_vertices[j, i, :] = np.mod(210.0 + 1.4 * cell_rlon + 0.08 * cell_rlat, 360.0)

    grid_id = cmor.grid(
        axis_ids=[rlat_id, rlon_id],
        latitude=latitude,
        longitude=longitude,
        latitude_vertices=lat_vertices,
        longitude_vertices=lon_vertices,
    )

    cmor.load_table("CMIP7_ocean.json")
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

    var_id = cmor.variable("tos_tavg-u-hxy-sea", "degC", [time_id, grid_id])
    cmor.write(var_id, data)
    return common.close_dataset(var_id)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args()
    print(generate(Path(args.workdir)))


if __name__ == "__main__":
    main()
