#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

import numpy as np
from netCDF4 import Dataset

from common import bounds_from_centers, finalize_case, parse_args, setup_case
import cmor


CASE_SLUG = "tasmax-grid-crs"


def main() -> None:
    args = parse_args(CASE_SLUG)
    drcdp_repo = Path(args.drcdp_repo).resolve()

    raw_user_input = {
        "activity_id": "DRCDP",
        "source_id": "MACA3-0",
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

    grid_table = cmor.load_table(str(drcdp_repo / "Tables" / "DRCDP_grids.json"))
    cmor.set_table(grid_table)

    source_path = (
        drcdp_repo
        / "DataPreparationExamples"
        / "DEMO"
        / "MACA3-0"
        / "DRCDP-MACA3-0_demo_data.nc"
    )
    with Dataset(source_path) as source:
        lat = np.asarray(source.variables["lat"][:4], dtype="d")
        lon = np.asarray(source.variables["lon"][:5], dtype="d")
        time = np.asarray(source.variables["time"][:2], dtype="d")
        raw = source.variables["tasmax"][:2, :4, :5]
        fill_value = getattr(source.variables["tasmax"], "_FillValue")
        scale_factor = getattr(source.variables["tasmax"], "scale_factor", 1.0)
        add_offset = getattr(source.variables["tasmax"], "add_offset", 0.0)
        values = np.where(raw == fill_value, np.nan, raw.astype("f8"))
        values = (values * scale_factor + add_offset + 273.15).astype("f4")

        crs_var = source.variables["crs"]
        crs_params = {
            key: getattr(crs_var, key)
            for key in crs_var.ncattrs()
            if key not in {"GeoTransform", "long_name"}
        }

    lat_bounds = bounds_from_centers(lat)
    lon_bounds = bounds_from_centers(lon)
    lat_grid, lon_grid = np.broadcast_arrays(np.expand_dims(lat, 0), np.expand_dims(lon, 1))
    lon_grid = np.mod(lon_grid, 360.0)

    lat_vertices = np.concatenate((np.flip(lat_bounds, axis=1), lat_bounds), axis=1)
    lon_vertices = np.repeat(lon_bounds, 2, axis=1)
    lat_vertices_grid, lon_vertices_grid = np.broadcast_arrays(
        np.expand_dims(lat_vertices, 0),
        np.expand_dims(lon_vertices, 1),
    )
    lon_vertices_grid = np.mod(lon_vertices_grid, 360.0)

    crs_params["crs_wkt"] = crs_params.pop("spatial_ref")
    for key, value in list(crs_params.items()):
        if isinstance(value, np.floating):
            crs_params[key] = (float(value), "")

    lat_id = cmor.axis(
        "latitude",
        coord_vals=lat,
        cell_bounds=lat_bounds,
        units="degrees_north",
    )
    lon_id = cmor.axis(
        "longitude",
        coord_vals=np.mod(lon, 360.0),
        cell_bounds=np.mod(lon_bounds, 360.0),
        units="degrees_east",
    )
    grid_id = cmor.grid(
        axis_ids=[lat_id, lon_id],
        latitude=lat_grid,
        longitude=lon_grid,
        latitude_vertices=lat_vertices_grid,
        longitude_vertices=lon_vertices_grid,
    )

    cmor.load_table(str(drcdp_repo / "Tables" / "DRCDP_APday.json"))
    time_bounds = np.array([[time[0] - 0.5, time[0] + 0.5], [time[1] - 0.5, time[1] + 0.5]], dtype="d")
    time_id = cmor.axis(
        "time",
        coord_vals=time,
        cell_bounds=time_bounds,
        units="days since 1900-01-01",
    )
    cmor.set_crs(
        grid_id=grid_id,
        mapping_name=crs_params["grid_mapping_name"],
        parameter_names=crs_params,
    )

    var_id = cmor.variable("tasmax", "K", [time_id, grid_id], missing_value=1.0e20)
    cmor.write(var_id, values, ntimes_passed=values.shape[0])
    print(finalize_case(var_id))


if __name__ == "__main__":
    main()
