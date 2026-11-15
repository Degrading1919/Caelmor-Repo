"""Place Lowmark sector artwork in Blender using the generated world offsets."""
import argparse
import csv
import math
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET

import bpy


TOOLS = Path(__file__).resolve().parent
GRIDS = TOOLS.parents[2] / "MEDIA/Maps/Lowmark_Blockout/grids"


def load_svg_reference(path, expected_size):
    """Rasterize the editable SVG's viewport with the same renderer as export."""
    launcher = ["py", "-3"] if os.name == "nt" else ["python3"]
    environment = os.environ.copy()
    dependencies = TOOLS / ".scratch/deps"
    environment["PYTHONPATH"] = str(dependencies)
    renderer = ("import sys; from resvg_py import svg_to_bytes; "
                "sys.stdout.buffer.write(svg_to_bytes(svg_path=sys.argv[1], background='#ffffff'))")
    rendered = subprocess.run([*launcher, "-c", renderer, str(path)], env=environment,
                              capture_output=True, check=False)
    if rendered.returncode:
        error = rendered.stderr.decode(errors="replace").strip()
        raise RuntimeError(f"Sector SVG render failed. Install the terrain tool dependencies first.\n{error}")
    scratch = TOOLS / ".scratch"
    scratch.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=scratch, prefix="sector-reference-") as folder:
        raster = Path(folder) / path.with_suffix(".png").name
        raster.write_bytes(rendered.stdout)
        image = bpy.data.images.load(str(raster))
        if tuple(image.size) != expected_size:
            bpy.data.images.remove(image)
            raise ValueError("The rendered SVG does not match the sector dimensions.")
        image.pack()
        image.name = f"{path.stem} SVG reference"
        return image


def place_sector(sector_id, *, z=0.0, source="png", opacity=0.75):
    """Return a north-up Blender image empty centred at its indexed XY position."""
    sector_id = sector_id.upper()
    with (GRIDS / "grid_index.csv").open(encoding="utf-8", newline="") as stream:
        row = next((item for item in csv.DictReader(stream) if item["sector_id"] == sector_id), None)
    if row is None:
        raise ValueError(f"Unknown Lowmark sector {sector_id!r}.")
    if source not in ("png", "svg") or not math.isfinite(z) or not 0 <= opacity <= 1:
        raise ValueError("Use PNG or SVG, a finite elevation, and opacity in the interval [0, 1].")
    width, height = int(row["width_m"]), int(row["height_m"])
    if width != height:
        raise ValueError("The sector reference must be square.")
    west, north = int(row["x_min_m"]), int(row["y_max_m"])
    center = (float(row["center_x_m"]), float(row["center_y_m"]), z)
    path = GRIDS / f"{sector_id}.{source}"
    name = f"Lowmark {sector_id} [{source.upper()}]"
    obj = bpy.data.objects.get(name)
    if obj is not None and obj.get("caelmor_sector_reference") != sector_id:
        raise ValueError(f"Blender object {name!r} already exists outside this tool.")
    if obj is None:
        if source == "svg":
            root = ET.parse(path).getroot()
            if [float(value) for value in root.get("viewBox", "").split()] != [west, -north, width, height]:
                raise ValueError("SVG viewport does not match the indexed world bounds.")
            image = load_svg_reference(path, (width, height))
        else:
            image = bpy.data.images.load(str(path), check_existing=True)
        if tuple(image.size) != (width, height):
            raise ValueError(f"Sector image {path.name} must be {width} × {height} pixels.")
        obj = bpy.data.objects.new(name, None)
        obj.empty_display_type = "IMAGE"
        obj.data = image
        bpy.context.collection.objects.link(obj)
        obj["caelmor_sector_reference"] = sector_id
    obj.location = center
    obj.rotation_euler = (0, 0, 0)
    obj.scale = (1, 1, 1)
    obj.empty_display_size = width
    obj.empty_image_offset = (-0.5, -0.5)
    obj.empty_image_depth = "FRONT"
    obj.show_empty_image_orthographic = True
    obj.show_empty_image_perspective = False
    obj.show_empty_image_only_axis_aligned = True
    obj.use_empty_image_alpha = True
    obj.color[3] = opacity
    return obj


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sector_ids", nargs="+")
    parser.add_argument("--source", choices=("png", "svg"), default="png")
    parser.add_argument("--z", type=float, default=0.0)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    for identity in args.sector_ids:
        place_sector(identity, z=args.z, source=args.source)
