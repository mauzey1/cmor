#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

import cmor
import numpy as np


def parse_args(case_slug: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--drcdp-repo",
        default=os.environ.get("DRCDP_REPO"),
        help="Path to a local checkout of the PCMDI/DRCDP repository.",
    )
    parser.add_argument(
        "--workdir",
        default=f"/private/tmp/drcdp-guide/{case_slug}",
        help="Working directory where the script writes JSON and NetCDF output.",
    )
    args = parser.parse_args()
    if not args.drcdp_repo:
        parser.error("set --drcdp-repo or DRCDP_REPO to a local DRCDP checkout")
    return args


def ensure_clean_dir(path: Path) -> Path:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return path


def resolve_user_input(raw_user_input: dict, drcdp_repo: Path) -> dict:
    resolved = dict(raw_user_input)
    resolved["_AXIS_ENTRY_FILE"] = "DRCDP_coordinate.json"
    resolved["_FORMULA_VAR_FILE"] = "DRCDP_formula_terms.json"
    resolved["_controlled_vocabulary_file"] = "DRCDP_CV.json"
    resolved["_history_template"] = (
        "%s; CMOR rewrote data to be consistent with <activity_id>, "
        "CMIP6, CMIP6Plus and <Conventions> standards"
    )

    drs = load_json(drcdp_repo / "DRCDP_DRS.json")
    tracking = load_json(drcdp_repo / "DRCDP_tracking_id.json")
    resolved["output_file_template"] = drs["DRS"]["filename_template"]
    resolved["output_path_template"] = drs["DRS"]["directory_path_template"]
    resolved["tracking_prefix"] = tracking["tracking_id_prefix"][0]
    return resolved


def setup_case(
    *,
    case_slug: str,
    table_name: str,
    raw_user_input: dict,
    drcdp_repo: Path,
    workdir: Path,
) -> tuple[Path, Path, Path]:
    case_dir = ensure_clean_dir(workdir)
    outdir = case_dir / "out"
    outdir.mkdir(parents=True, exist_ok=True)

    raw_input = dict(raw_user_input)
    raw_input["outpath"] = str(outdir)

    raw_input_path = write_json(case_dir / "raw_user_input.json", raw_input)
    resolved_input = resolve_user_input(raw_input, drcdp_repo)
    resolved_input_path = write_json(case_dir / "user_input.json", resolved_input)

    tables_dir = drcdp_repo / "Tables"
    cmor.setup(inpath=str(tables_dir), netcdf_file_action=cmor.CMOR_REPLACE)
    if cmor.dataset_json(str(resolved_input_path)) != 0:
        raise RuntimeError(f"cmor.dataset_json failed for {case_slug}")
    cmor.load_table(str(tables_dir / table_name))
    return raw_input_path, resolved_input_path, outdir


def finalize_case(var_id: int) -> str:
    output_path = cmor.close(var_id, file_name=True)
    cmor.close()
    return output_path


def bounds_from_centers(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype="d")
    midpoints = (values[1:] + values[:-1]) / 2.0
    bounds = np.empty((values.size, 2), dtype="d")
    bounds[1:, 0] = midpoints
    bounds[:-1, 1] = midpoints
    bounds[0, 0] = values[0] - (midpoints[0] - values[0])
    bounds[-1, 1] = values[-1] + (values[-1] - midpoints[-1])
    return bounds


def ncdump_header(path: str | Path) -> str:
    return subprocess.check_output(["ncdump", "-h", str(path)], text=True)

