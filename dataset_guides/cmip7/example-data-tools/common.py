#!/usr/bin/env python

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[3]
try:
    import cmor  # noqa: E402
except ImportError:  # pragma: no cover - fallback for local source-tree runs
    BUILD_DIRS = sorted(REPO_ROOT.glob("build/lib.*"))
    if not BUILD_DIRS:
        raise RuntimeError(
            "Could not import cmor from the active environment and could not "
            "find a built CMOR Python package under build/lib.*"
        )
    sys.path.insert(0, str(BUILD_DIRS[0]))
    import cmor  # noqa: E402

TABLES_PATH = REPO_ROOT / "cmip7-cmor-tables" / "tables"
CV_PATH = REPO_ROOT / "cmip7-cmor-tables" / "tables-cvs" / "cmor-cvs.json"
CV_PATH_REL = str(CV_PATH.relative_to(REPO_ROOT))

BASE_USER_INPUT = {
    "_AXIS_ENTRY_FILE": "CMIP7_coordinate.json",
    "_FORMULA_VAR_FILE": "CMIP7_formula_terms.json",
    "_cmip7_option": 1,
    "activity_id": "CMIP",
    "calendar": "360_day",
    "experiment_id": "amip",
    "forcing_index": "f3",
    "frequency": "mon",
    "grid_label": "g999",
    "initialization_index": "i1",
    "institution_id": "MOHC",
    "license_id": "CC-BY-4.0",
    "nominal_resolution": "100 km",
    "physics_index": "p1",
    "realization_index": "r9",
    "region": "glb",
    "source_id": "DUMMY-MODEL",
}


def cmor_version() -> str:
    return ".".join(
        str(part)
        for part in (
            cmor.CMOR_VERSION_MAJOR,
            cmor.CMOR_VERSION_MINOR,
            cmor.CMOR_VERSION_PATCH,
        )
    )


def configure_dataset(
    workdir: Path,
    overrides: dict | None = None,
    removed_keys: list[str] | None = None,
) -> Path:
    workdir.mkdir(parents=True, exist_ok=True)
    outdir = workdir / "out"
    outdir.mkdir(parents=True, exist_ok=True)

    user_input = dict(BASE_USER_INPUT)
    user_input["_controlled_vocabulary_file"] = CV_PATH_REL
    user_input["outpath"] = str(outdir)
    if removed_keys:
        for key in removed_keys:
            user_input.pop(key, None)
    if overrides:
        user_input.update(overrides)

    input_path = workdir / "input.json"
    input_path.write_text(json.dumps(user_input, indent=2, sort_keys=True))

    cmor.setup(inpath=str(TABLES_PATH), netcdf_file_action=cmor.CMOR_REPLACE)
    if cmor.dataset_json(str(input_path)) != 0:
        raise RuntimeError("cmor.dataset_json failed")
    return input_path


def close_dataset(var_id: int) -> str:
    file_path = cmor.close(var_id, file_name=True)
    cmor.close()
    return file_path


def lat_lon_axes() -> tuple[int, int]:
    lat = np.array([10.0, 20.0, 30.0], dtype="d")
    lat_bnds = np.array([5.0, 15.0, 25.0, 35.0], dtype="d")
    lon = np.array([0.0, 90.0, 180.0, 270.0], dtype="d")
    lon_bnds = np.array([-45.0, 45.0, 135.0, 225.0, 315.0], dtype="d")

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
    return lat_id, lon_id


def time_axis() -> int:
    time = np.array([15.0, 45.0], dtype="d")
    time_bnds = np.array([0.0, 30.0, 60.0], dtype="d")
    return cmor.axis(
        table_entry="time",
        units="days since 1979-01-01",
        coord_vals=time,
        cell_bounds=time_bnds,
    )


def time2_axis() -> int:
    time = np.array([15.0, 45.0], dtype="d")
    time_bnds = np.array([[0.0, 30.0], [30.0, 60.0]], dtype="d")
    return cmor.axis(
        table_entry="time2",
        units="days since 1979-01-01",
        coord_vals=time,
        cell_bounds=time_bnds,
    )


def time3_axis(months: int = 2) -> int:
    points: list[float] = []
    bounds: list[list[float]] = []
    for month_index in range(months):
        month_start = month_index * 30.0
        for hour in range(24):
            lower = month_start + hour / 24.0
            upper = month_start + 30.0 + (hour + 1) / 24.0
            points.append((lower + upper) / 2.0)
            bounds.append([lower, upper])
    return cmor.axis(
        table_entry="time3",
        units="days since 1979-01-01",
        coord_vals=np.array(points, dtype="d"),
        cell_bounds=np.array(bounds, dtype="d"),
    )


def height2m_axis() -> int:
    return cmor.axis(
        table_entry="height2m",
        units="m",
        coord_vals=np.array((2.0,), dtype="d"),
    )


def plev19_axis() -> int:
    plev19 = np.array(
        [
            100000.0,
            92500.0,
            85000.0,
            70000.0,
            60000.0,
            50000.0,
            40000.0,
            30000.0,
            25000.0,
            20000.0,
            15000.0,
            10000.0,
            7000.0,
            5000.0,
            3000.0,
            2000.0,
            1000.0,
            500.0,
            100.0,
        ],
        dtype="d",
    )
    return cmor.axis(table_entry="plev19", units="Pa", coord_vals=plev19)


def standard_hybrid_sigma_axis() -> tuple[int, np.ndarray, np.ndarray, float, np.ndarray]:
    lev = np.array([0.92, 0.72, 0.50, 0.30, 0.10], dtype="d")
    lev_bnds = np.array([1.00, 0.83, 0.61, 0.40, 0.20, 0.00], dtype="d")
    a_vals = np.array([0.12, 0.22, 0.30, 0.20, 0.10], dtype="d")
    b_vals = np.array([0.80, 0.50, 0.20, 0.10, 0.00], dtype="d")
    p0_val = 100000.0
    ps_vals = np.array(
        [
            [
                [97000.0, 97400.0, 97800.0, 98200.0],
                [98600.0, 99000.0, 99400.0, 99800.0],
                [100200.0, 100600.0, 101000.0, 101400.0],
            ],
            [
                [97100.0, 97500.0, 97900.0, 98300.0],
                [98700.0, 99100.0, 99500.0, 99900.0],
                [100300.0, 100700.0, 101100.0, 101500.0],
            ],
        ],
        dtype="f",
    )

    lev_id = cmor.axis(
        table_entry="standard_hybrid_sigma",
        units="1",
        coord_vals=lev,
        cell_bounds=lev_bnds,
    )
    a_bnds = np.array([0.06, 0.18, 0.26, 0.25, 0.15, 0.00], dtype="d")
    b_bnds = np.array([0.94, 0.65, 0.35, 0.15, 0.05, 0.00], dtype="d")

    _ = cmor.zfactor(
        zaxis_id=lev_id,
        zfactor_name="a",
        axis_ids=[lev_id],
        zfactor_values=a_vals,
        zfactor_bounds=a_bnds,
    )
    _ = cmor.zfactor(
        zaxis_id=lev_id,
        zfactor_name="b",
        axis_ids=[lev_id],
        zfactor_values=b_vals,
        zfactor_bounds=b_bnds,
    )
    _ = cmor.zfactor(
        zaxis_id=lev_id,
        zfactor_name="p0",
        units="Pa",
        zfactor_values=p0_val,
    )
    return lev_id, a_vals, b_vals, p0_val, ps_vals
