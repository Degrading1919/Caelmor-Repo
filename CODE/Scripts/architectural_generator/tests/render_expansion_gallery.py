"""Re-render only type cards with camera framing derived from actual mesh bounds."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_expansion_evidence import (
    FRAMES, HEIGHT, OUT, WIDTH, build_rows, configurations, frame_for, initialize,
)


def main():
    OUT.mkdir(exist_ok=True)
    FRAMES.mkdir(exist_ok=True)
    scene, camera, sun, fill, ground = initialize()
    rows = build_rows(configurations(False))
    timings = []
    for index, row in enumerate(rows):
        for other in rows:
            visible = other is row
            for obj in other["objects"]:
                obj.hide_render = not visible
        timings.append(frame_for(
            scene, camera, sun, fill, ground, row,
            FRAMES / f"item_{index:02d}.png", WIDTH, 1.12,
        ))
    manifest_path = OUT / "expansion_evidence_manifest.json"
    report = json.loads(manifest_path.read_text(encoding="utf-8"))
    report["renders"]["gallery"] = {
        "items": len(rows),
        "frame_resolution": [WIDTH, HEIGHT],
        "seconds": round(sum(timings), 3),
        "camera_fit": "projected actual mesh bounds with 12% margin plus 2 m",
    }
    manifest_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"EXPANSION_GALLERY_READY={OUT / 'expanded_type_gallery.png'}", flush=True)


if __name__ == "__main__":
    main()
