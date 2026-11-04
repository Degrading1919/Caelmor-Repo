"""Build lightweight, paint-ready Caelmor material templates in Blender.

Usage (PowerShell):
  blender --background --python MEDIA/Materials/build_templates.py -- --output-dir MEDIA/Materials/templates

The output is one deterministic Wavefront OBJ per template. Each OBJ uses a
single connected, open surface with one square UV chart spanning [0, 1] in both
axes. The intentional open back lets Procreate artists paint the useful face
without wasting the canvas on hidden geometry. A consuming package can replace
the shared `CaelmorMaterial` identifier while retaining the required MTL link.
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import bpy


TEMPLATE_KEYS = (
    "roof",
    "wall",
    "beam",
    "board",
    "metal",
    "fabric",
    "terrain",
    "organic",
)


def surface_height(kind: str, u: float, v: float) -> float:
    """Small structural relief in the local paint surface (not texture detail)."""
    x = 2.0 * u - 1.0
    y = 2.0 * v - 1.0
    if kind == "roof":
        return 0.18 * y + 0.035 * math.sin(math.pi * u)
    if kind == "wall":
        return 0.025 * math.sin(2.0 * math.pi * u) * math.sin(math.pi * v)
    if kind == "beam":
        # Crown the broad face, with narrow chamfer-like shoulders.
        edge = abs(x)
        return 0.075 * (1.0 - x * x) + 0.025 * max(0.0, (edge - 0.78) / 0.22)
    if kind == "board":
        return 0.035 * math.cos(2.0 * math.pi * x) + 0.012 * math.sin(math.pi * y)
    if kind == "metal":
        return 0.10 * max(0.0, 1.0 - 0.68 * (x * x + y * y))
    if kind == "fabric":
        return -0.16 * (1.0 - y * y) + 0.025 * math.sin(3.0 * math.pi * u + y)
    if kind == "terrain":
        return (0.13 * math.exp(-3.2 * (x * x + y * y))
                + 0.028 * math.sin(2.2 * math.pi * u) * math.sin(1.6 * math.pi * v))
    if kind == "organic":
        return 0.11 * (1.0 - abs(x)) + 0.025 * math.sin(2.0 * math.pi * v)
    raise ValueError(f"Unknown template key: {kind}")


def surface_xy(kind: str, u: float, v: float) -> tuple[float, float]:
    """Return a gentle silhouette while keeping a regular, non-overlapping UV grid."""
    x = 2.0 * u - 1.0
    y = 2.0 * v - 1.0
    if kind == "organic":
        # Narrow rounded leaf/pelt form; endpoints remain small and paintable.
        width = 0.18 + 0.82 * (math.sin(math.pi * v) ** 0.7)
        x *= width
    if kind == "metal":
        # Rounded plate outline with a little margin at each corner.
        x *= 0.94 - 0.12 * abs(y)
        y *= 0.94 - 0.12 * abs(x)
    return x, y


def build_mesh(kind: str, segments: int) -> bpy.types.Object:
    """Create a native Blender grid and its one-to-one square UV chart."""
    verts: list[tuple[float, float, float]] = []
    uvs: list[tuple[float, float]] = []
    for j in range(segments + 1):
        v = j / segments
        for i in range(segments + 1):
            u = i / segments
            x, y = surface_xy(kind, u, v)
            verts.append((x, y, surface_height(kind, u, v)))
            uvs.append((u, v))

    faces: list[tuple[int, int, int, int]] = []
    row = segments + 1
    for j in range(segments):
        for i in range(segments):
            a = j * row + i
            faces.append((a, a + 1, a + row + 1, a + row))

    mesh = bpy.data.meshes.new(f"{kind}_surface")
    mesh.from_pydata(verts, [], faces)
    mesh.update(calc_edges=True)
    uv_layer = mesh.uv_layers.new(name="PaintUV")
    for polygon in mesh.polygons:
        for loop_index in polygon.loop_indices:
            vertex_index = mesh.loops[loop_index].vertex_index
            uv_layer.data[loop_index].uv = uvs[vertex_index]
    mesh.update()

    obj = bpy.data.objects.new(kind, mesh)
    bpy.context.collection.objects.link(obj)
    # The chart is an open surface by design. Recalculation preserves the
    # regular grid's consistent outward/top-facing winding and provides usable
    # vertex normals for Blender and downstream importers.
    mesh.update()
    mesh.calc_loop_triangles()
    return obj


def normalized_vertices(obj: bpy.types.Object) -> list[tuple[float, float, float]]:
    """Center and scale each template so its largest extent is exactly one."""
    coords = [tuple(v.co) for v in obj.data.vertices]
    mins = [min(p[k] for p in coords) for k in range(3)]
    maxs = [max(p[k] for p in coords) for k in range(3)]
    center = [(mins[k] + maxs[k]) * 0.5 for k in range(3)]
    scale = max(maxs[k] - mins[k] for k in range(3))
    if scale <= 1e-8:
        raise RuntimeError(f"Degenerate template geometry: {obj.name}")
    return [tuple((p[k] - center[k]) / scale for k in range(3)) for p in coords]


def write_obj(obj: bpy.types.Object, path: Path) -> None:
    """Serialize stable vertex, UV, and quad records without exporter drift."""
    mesh = obj.data
    vertices = normalized_vertices(obj)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii", newline="\n") as out:
        out.write(f"# Caelmor paint template: {obj.name}\n")
        out.write("# Generated by MEDIA/Materials/build_templates.py\n")
        out.write("mtllib material.mtl\n")
        out.write(f"o {obj.name}\n")
        for x, y, z in vertices:
            out.write(f"v {x:.9f} {y:.9f} {z:.9f}\n")
        # Every mesh vertex maps to the same-index UV point; this yields one
        # continuous chart and avoids seams or overlapping islands.
        # Segment count is recovered robustly from the square grid size.
        for loop in mesh.vertices:
            segments = round(math.sqrt(len(vertices))) - 1
            i = loop.index % (segments + 1)
            j = loop.index // (segments + 1)
            out.write(f"vt {i / segments:.9f} {j / segments:.9f}\n")
        out.write("usemtl CaelmorMaterial\n")
        for poly in mesh.polygons:
            refs = [f"{idx + 1}/{idx + 1}" for idx in poly.vertices]
            out.write("f " + " ".join(refs) + "\n")


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path,
        default=Path(__file__).resolve().parent / "templates",
        help="directory for the eight OBJ files (default: MEDIA/Materials/templates)",
    )
    parser.add_argument(
        "--segments", type=int, default=16,
        help="quad subdivisions per UV axis (8-64; default: 16)",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args()
    if not 8 <= args.segments <= 64:
        raise SystemExit("--segments must be between 8 and 64")
    output_dir = args.output_dir.resolve()
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials):
        for datablock in list(datablocks):
            if datablock.users == 0:
                datablocks.remove(datablock)

    material = bpy.data.materials.new("CaelmorMaterial")
    material.diffuse_color = (0.55, 0.42, 0.29, 1.0)
    for key in TEMPLATE_KEYS:
        obj = build_mesh(key, args.segments)
        obj.data.materials.append(material)
        write_obj(obj, output_dir / f"{key}.obj")
        mesh = obj.data
        bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.meshes.remove(mesh)
    print(f"Wrote {len(TEMPLATE_KEYS)} normalized paint templates to {output_dir}")


if __name__ == "__main__":
    main()
