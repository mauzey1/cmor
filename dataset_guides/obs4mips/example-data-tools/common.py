#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

import cmor
import numpy as np
from netCDF4 import date2num


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_FILE_TEMPLATE = "<variable_id><frequency><source_id><variant_label><grid_label>"
DEFAULT_OUTPUT_PATH_TEMPLATE = (
    "<activity_id><institution_id><source_id><frequency><variable_id><grid_label><version>"
)


def parse_args(case_slug: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--obs4mips-repo",
        default=None,
        help="Path to a local checkout of PCMDI/obs4MIPs-cmor-tables.",
    )
    parser.add_argument(
        "--workdir",
        default=f"/private/tmp/obs4mips-guide/{case_slug}",
        help="Working directory where the script writes JSON and NetCDF output.",
    )
    args = parser.parse_args()
    if not args.obs4mips_repo:
        parser.error("set --obs4mips-repo to a local obs4MIPs-cmor-tables checkout")
    return args


def ensure_clean_dir(path: Path) -> Path:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def processing_code_location(script_path: Path) -> str:
    return str(script_path.resolve().relative_to(REPO_ROOT))


def write_json(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return path


def prepare_case(
    *,
    case_slug: str,
    table_name: str,
    user_input: dict,
    obs4mips_repo: Path,
    workdir: Path,
) -> tuple[Path, Path]:
    case_dir = ensure_clean_dir(workdir)
    outdir = case_dir / "out"
    outdir.mkdir(parents=True, exist_ok=True)

    payload = dict(user_input)
    payload["outpath"] = str(outdir)
    input_path = write_json(case_dir / "user_input.json", payload)

    tables_dir = obs4mips_repo / "Tables"
    cmor.setup(inpath=str(tables_dir), netcdf_file_action=cmor.CMOR_REPLACE)
    if cmor.dataset_json(str(input_path)) != 0:
        raise RuntimeError(f"cmor.dataset_json failed for {case_slug}")
    cmor.load_table(str(tables_dir / table_name))
    return input_path, outdir


def finalize_case(var_id: int) -> str:
    output_path = cmor.close(var_id, file_name=True)
    cmor.close()
    return output_path


def month_bounds_for_count(
    *,
    start_year: int,
    start_month: int,
    count: int,
    units: str,
    calendar: str = "standard",
) -> tuple[np.ndarray, np.ndarray]:
    month_starts: list[datetime] = []
    year = start_year
    month = start_month
    for _ in range(count + 1):
        month_starts.append(datetime(year, month, 1))
        month += 1
        if month == 13:
            month = 1
            year += 1

    bounds = np.array(
        [
            [
                date2num(month_starts[index], units=units, calendar=calendar),
                date2num(month_starts[index + 1], units=units, calendar=calendar),
            ]
            for index in range(count)
        ],
        dtype="d",
    )
    time_vals = bounds.mean(axis=1)
    return time_vals, bounds


def bounds_from_centers(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype="d")
    midpoints = (values[1:] + values[:-1]) / 2.0
    bounds = np.empty((values.size, 2), dtype="d")
    bounds[1:, 0] = midpoints
    bounds[:-1, 1] = midpoints
    bounds[0, 0] = values[0] - (midpoints[0] - values[0])
    bounds[-1, 1] = values[-1] + (values[-1] - midpoints[-1])
    return bounds
