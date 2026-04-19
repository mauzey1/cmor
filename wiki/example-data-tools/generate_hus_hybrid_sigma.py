#!/usr/bin/env python

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import numpy as np

import common

cmor = common.cmor


def generate(workdir: Path) -> str:
    workdir.mkdir(parents=True, exist_ok=True)
    derived_cv = workdir / "CMIP7_CV_with_model_levels.json"
    cv = json.loads(common.CV_PATH.read_text())
    cv["CV"]["vertical_label"]["al"] = "atmosphere model levels"
    derived_cv.write_text(json.dumps(cv, indent=2, sort_keys=True))

    old_cwd = Path.cwd()
    os.chdir(workdir)
    try:
        common.configure_dataset(
            workdir,
            overrides={"_controlled_vocabulary_file": derived_cv.name},
        )
        cmor.load_table("CMIP7_atmos.json")
        lat_id, lon_id = common.lat_lon_axes()
        time_id = common.time_axis()
        lev_id, _a_vals, _b_vals, _p0_val, ps_vals = common.standard_hybrid_sigma_axis()

        ps_var_id = cmor.zfactor(
            zaxis_id=lev_id,
            zfactor_name="ps",
            axis_ids=[time_id, lat_id, lon_id],
            units="Pa",
        )

        data = np.linspace(0.001, 0.020, 2 * 5 * 3 * 4, dtype="f").reshape((2, 5, 3, 4))
        var_id = cmor.variable(
            "hus_tavg-al-hxy-u",
            "1",
            [time_id, lev_id, lat_id, lon_id],
        )
        cmor.write(var_id, data)
        cmor.write(ps_var_id, ps_vals, store_with=var_id)
        return common.close_dataset(var_id)
    finally:
        os.chdir(old_cwd)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args()
    print(generate(Path(args.workdir)))


if __name__ == "__main__":
    main()
