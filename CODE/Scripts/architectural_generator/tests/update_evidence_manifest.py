"""Add full settings and pure geometry diagnostics to an existing render record."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from caelmor_architecture.engine import generate, validate
from caelmor_architecture.model import Settings


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "evidence" / "evidence_manifest.json"


def settings_for(row):
    if 'settings' in row:
        return Settings(**row['settings'])
    values = {key: row[key] for key in ("function", "seed", "footprint", "width", "depth", "floors")}
    if row["function"] == "BARN":
        values["pitch"] = 42.0
    if row["function"] == "INN":
        values.update(wing_width=4.5, wing_depth=6.0)
    if row["function"] == "FARMHOUSE" and row["seed"] == 43:
        values.update(wing_width=4.0, wing_depth=5.2)
    if row["seed"] == 43:
        values["window_density"] = 1.2
    return Settings(**values)


def update():
    report = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for row in report["buildings"]:
        settings = settings_for(row)
        plan, buffers = generate(settings)
        diagnostics = validate(plan, buffers)
        if not diagnostics["valid"]:
            raise ValueError(f"Invalid evidence geometry: {row['function']} seed {row['seed']}: {diagnostics['errors']}")
        if diagnostics["geometry_hash"] != row["geometry_hash"]:
            raise ValueError(f"Geometry hash differs for {row['function']} seed {row['seed']}")
        if diagnostics["objects"] != row["mesh_objects"]:
            raise ValueError(f"Mesh count differs for {row['function']} seed {row['seed']}")
        if diagnostics["vertices"] != row["vertices"]:
            raise ValueError(f"Vertex count differs for {row['function']} seed {row['seed']}")
        row["settings"] = settings.__dict__
        row["validation"] = diagnostics
    MANIFEST.write_text(json.dumps(report, indent=2), encoding="utf-8")
    total_vertices = sum(row["vertices"] for row in report["buildings"])
    print(f"EVIDENCE_MANIFEST_VERIFIED buildings={len(report['buildings'])} vertices={total_vertices}")


if __name__ == "__main__":
    update()
