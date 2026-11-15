"""Reduce fixed-camera standalone samples into a reviewable CSV."""
import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import median

TIMES = ("frame_ms", "cpu_ms", "gpu_ms")
COUNTERS = ("batches", "draw_calls", "standard_draw_calls", "instanced_draw_calls", "setpass", "triangles", "allocated_bytes", "scene_texture_bytes",
            "scene_mesh_bytes", "streaming_current_bytes", "material_count", "common_material_count")
GROUP = ("configuration", "view", "roof_case", "foliage")


def summarize(inputs, output):
    groups = defaultdict(list)
    for path in inputs:
        with path.open(newline="", encoding="utf-8-sig") as stream:
            for row in csv.DictReader(stream):
                groups[tuple(row[key] for key in GROUP)].append(row)
    if not groups:
        raise ValueError("No completed samples")
    columns = (*GROUP, "samples", *(m + "_median" for m in TIMES + COUNTERS),
               "frame_ms_p95", "cpu_sample_count", "gpu_sample_count")
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(columns)
        for keys, rows in sorted(groups.items()):
            values = {m: sorted(float(row[m]) for row in rows if row.get(m, "") != "") for m in TIMES + COUNTERS}
            frame = values["frame_ms"]
            writer.writerow((*keys, len(rows), *(round(median(values[m]), 4) if values[m] else "" for m in TIMES + COUNTERS),
                             frame[(95 * len(frame) + 99)//100 - 1], len(values["cpu_ms"]), len(values["gpu_ms"])))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summarize(args.inputs, args.output)
