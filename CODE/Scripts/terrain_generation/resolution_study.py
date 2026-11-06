"""Execute actual controls at candidate resolutions, retaining honest rejections."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import time

import numpy as np

from terrain import generate


def study(controls, resolutions=(32, 16, 8)):
    reports = []
    for resolution in resolutions:
        started = time.perf_counter()
        try:
            result = generate(controls, resolution)
        except ValueError as error:
            reports.append({"resolution_m": resolution, "status": "rejected", "reason": str(error),
                            "seconds_to_rejection": time.perf_counter() - started})
            continue
        reports.append({"resolution_m": resolution, "status": "generated", "cells": result.metrics["cells"],
                        "model_seconds": result.metrics["seconds"], "height_sha256": result.metrics["height_sha256"],
                        "unintended_sinks": result.metrics["unintended_sinks"],
                        "all_cells_reach_outlet": result.metrics["all_cells_reach_outlet"],
                        "conditioning_raise_max_m": result.metrics["conditioning_raise_max_m"],
                        "natural_sampled_uphill_segments": sum(reach["sampled_uphill_segments"] for reach in result.metrics["natural_reaches"]),
                        "fen_wet_fraction": result.metrics["fen"]["wet_ground_fraction"],
                        "settlement_screened_capacity": {item["id"]: item["screened_roof_capacity"] for item in result.metrics["settlements"]}})
    return reports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--controls", type=Path, default=Path(__file__).with_name("lowmark_controls.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    controls = json.loads(args.controls.read_text(encoding="utf-8-sig"))
    reports = {"python": platform.python_version(), "numpy": np.__version__,
               "controls_sha256": hashlib.sha256(args.controls.read_bytes()).hexdigest(),
               "results": study(controls)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(reports, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(reports, indent=2))


if __name__ == "__main__":
    main()
