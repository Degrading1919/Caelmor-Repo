"""Native Blender package import, PBR binding, chart checks, and studio previews.

Run from the repository root:
  blender --background --python MEDIA/Materials/verify_blender.py -- \
    --packages MEDIA/Materials/.pilot/packages \
    --evidence MEDIA/Materials/evidence

Accepts <id>.zip files and/or unpacked <id>/ package folders. For each package,
imports material.obj with Blender's default OBJ axes (the published assets are
Y-up), verifies material.mtl and its Procreate map directives, checks the UV
chart and six 512-square PNGs, binds PBR nodes explicitly, and renders the
imported mesh. Output is one PNG preview per package plus verification.json.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

import bpy
from mathutils import Vector


EXPECTED_MAPS = {
    "map_Kd": "color.png",
    "map_roughness": "roughness.png",
    "map_metallic": "metallic.png",
    "map_tangentSpaceNormal": "normal.png",
}
REQUIRED_IMAGES = ("master.png", "color.png", "height.png", "roughness.png", "metallic.png", "normal.png")
PILOT_IDS = (
    "split_oak_shingle",
    "coursed_fieldstone",
    "split_slate",
    "hewn_oak",
    "forged_iron",
    "plain_linen",
)


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parent
    parser.add_argument("--packages", type=Path, default=root / "packages")
    parser.add_argument("--evidence", type=Path, default=root / "evidence")
    parser.add_argument("--resolution", type=int, default=768)
    parser.add_argument("--samples", type=int, default=24)
    parser.add_argument("--all", action="store_true", help="Render all found packages instead of the pilot six")
    return parser.parse_args(argv)


def discover_packages(packages: Path) -> list[tuple[str, Path]]:
    found: dict[str, Path] = {}
    if not packages.is_dir():
        raise FileNotFoundError(f"Pilot package directory not found: {packages}")
    for folder in packages.iterdir():
        if folder.is_dir() and (folder / "material.obj").is_file():
            found[folder.name] = folder
    for archive in packages.glob("*.zip"):
        if archive.stem in found:
            continue
        found[archive.stem] = archive
    if not found:
        raise FileNotFoundError(f"No package folders or ZIPs in {packages}")
    # Preserve catalog order for known pilot IDs, then report any extras clearly.
    return sorted(found.items(), key=lambda row: (PILOT_IDS.index(row[0]) if row[0] in PILOT_IDS else 999, row[0]))


def safe_extract(archive: Path, destination: Path, package_id: str) -> Path:
    root = destination.resolve()
    with zipfile.ZipFile(archive) as zf:
        for item in zf.infolist():
            name = PurePosixPath(item.filename)
            if name.is_absolute() or ".." in name.parts:
                raise ValueError(f"Unsafe package path: {item.filename}")
            target = (destination / Path(*name.parts)).resolve()
            if target != root and root not in target.parents:
                raise ValueError(f"Unsafe package path: {item.filename}")
        zf.extractall(destination)
    candidate = destination / package_id
    if (candidate / "material.obj").is_file():
        return candidate
    if (destination / "material.obj").is_file():
        return destination
    raise FileNotFoundError(f"{archive}: expected {package_id}/material.obj")


def parse_mtl(path: Path) -> tuple[str, dict[str, str]]:
    material_name = None
    maps: dict[str, str] = {}
    for raw in path.read_text(encoding="ascii").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition(" ")
        if key == "newmtl":
            material_name = value.strip()
        elif key in EXPECTED_MAPS:
            maps[key] = value.strip()
    if material_name is None:
        raise ValueError(f"Missing newmtl in {path}")
    return material_name, maps


def validate_obj_links(obj_path: Path, material_name: str) -> None:
    text = obj_path.read_text(encoding="ascii")
    libraries = [line.split(maxsplit=1)[1].strip() for line in text.splitlines() if line.startswith("mtllib ")]
    materials = [line.split(maxsplit=1)[1].strip() for line in text.splitlines() if line.startswith("usemtl ")]
    if libraries != ["material.mtl"]:
        raise ValueError(f"Expected literal mtllib material.mtl in {obj_path.name}; got {libraries}")
    if materials != [material_name]:
        raise ValueError(f"OBJ material id does not match MTL {material_name!r}: {materials}")


def uv_chart_stats(mesh: bpy.types.Mesh) -> dict[str, float | int]:
    if len(mesh.uv_layers) != 1:
        raise ValueError(f"Expected one UV chart layer, found {len(mesh.uv_layers)}")
    uv_data = mesh.uv_layers.active.data
    uv = [tuple(item.uv) for item in uv_data]
    eps = 1e-6
    min_u, max_u = min(p[0] for p in uv), max(p[0] for p in uv)
    min_v, max_v = min(p[1] for p in uv), max(p[1] for p in uv)
    if min(min_u, min_v) < -eps or max(max_u, max_v) > 1.0 + eps:
        raise ValueError("UV chart extends outside normalized [0,1] range")
    if any(abs(value) > eps and abs(value - 1.0) > eps for value in (min_u, max_u, min_v, max_v)):
        raise ValueError("UV chart does not cover the full unit square")

    # Imported face UVs must be consistently oriented, nondegenerate, and tile
    # exactly one unit square. Combined with one connected manifold grid and
    # all coordinates in the square, this detects folds/overlapping raster area.
    area = 0.0
    for poly in mesh.polygons:
        points = [uv_data[loop_index].uv for loop_index in poly.loop_indices]
        signed = sum(points[i].x * points[(i + 1) % len(points)].y
                     - points[(i + 1) % len(points)].x * points[i].y
                     for i in range(len(points))) * 0.5
        if signed <= 1e-12:
            raise ValueError("Found degenerate or flipped UV face")
        area += signed
    if abs(area - 1.0) > 1e-5:
        raise ValueError(f"UV face area totals {area:.8f}, expected 1.0")

    edge_use: dict[tuple[int, int], int] = {}
    adjacency = {i: set() for i in range(len(mesh.polygons))}
    owners: dict[tuple[int, int], list[int]] = {}
    for poly in mesh.polygons:
        verts = list(poly.vertices)
        for a, b in zip(verts, verts[1:] + verts[:1]):
            key = tuple(sorted((a, b)))
            edge_use[key] = edge_use.get(key, 0) + 1
            owners.setdefault(key, []).append(poly.index)
    if any(count > 2 for count in edge_use.values()):
        raise ValueError("Mesh has a non-manifold edge")
    for faces in owners.values():
        if len(faces) == 2:
            adjacency[faces[0]].add(faces[1])
            adjacency[faces[1]].add(faces[0])
    reached, stack = set(), [0] if adjacency else []
    while stack:
        current = stack.pop()
        if current in reached:
            continue
        reached.add(current)
        stack.extend(adjacency[current] - reached)
    if len(reached) != len(mesh.polygons):
        raise ValueError("Mesh/UV chart is disconnected")
    boundary_edges = sum(count == 1 for count in edge_use.values())
    return {"uv_layers": 1, "uv_min": [min_u, min_v], "uv_max": [max_u, max_v],
            "uv_signed_area": area, "faces": len(mesh.polygons), "vertices": len(mesh.vertices),
            "boundary_edges": boundary_edges}


def load_images(package: Path) -> tuple[dict[str, bpy.types.Image], dict[str, dict]]:
    images, stats = {}, {}
    for filename in REQUIRED_IMAGES:
        path = package / filename
        if not path.is_file():
            raise FileNotFoundError(f"Missing required image: {filename}")
        image = bpy.data.images.load(str(path), check_existing=False)
        width, height = map(int, image.size)
        if (width, height) != (512, 512):
            raise ValueError(f"{filename} is {width}x{height}; expected 512x512")
        image.colorspace_settings.name = "sRGB" if filename == "color.png" else "Non-Color"
        if filename == "color.png" and image.colorspace_settings.name != "sRGB":
            raise ValueError("Color map did not retain sRGB color space")
        if filename != "color.png" and image.colorspace_settings.name != "Non-Color":
            raise ValueError(f"Data map {filename} is not Non-Color")
        images[filename.removesuffix(".png")] = image
        stats[filename] = {"width": width, "height": height, "color_space": image.colorspace_settings.name}
    return images, stats


def assign_material(obj: bpy.types.Object, name: str, images: dict[str, bpy.types.Image]) -> bpy.types.Material:
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (650, 80)
    shader = nodes.new("ShaderNodeBsdfPrincipled")
    shader.location = (380, 80)
    links.new(shader.outputs["BSDF"], output.inputs["Surface"])
    uv = nodes.new("ShaderNodeTexCoord")
    uv.location = (-850, 0)
    def texture(key: str, x: int, y: int):
        node = nodes.new("ShaderNodeTexImage")
        node.image = images[key]
        node.location = (x, y)
        links.new(uv.outputs["UV"], node.inputs["Vector"])
        return node

    color = texture("color", -400, 340)
    links.new(color.outputs["Color"], shader.inputs["Base Color"])
    rough = texture("roughness", -400, 100)
    links.new(rough.outputs["Color"], shader.inputs["Roughness"])
    metallic = texture("metallic", -400, -140)
    links.new(metallic.outputs["Color"], shader.inputs["Metallic"])
    normal = texture("normal", -400, -380)
    normal_map = nodes.new("ShaderNodeNormalMap")
    normal_map.location = (-80, -300)
    links.new(normal.outputs["Color"], normal_map.inputs["Color"])
    links.new(normal_map.outputs["Normal"], shader.inputs["Normal"])
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return mat


def render_preview(obj: bpy.types.Object, images: dict[str, bpy.types.Image], package: Path,
                   package_id: str, output: Path, resolution: int, samples: int,
                   material_name: str) -> None:
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = samples
    scene.render.resolution_x = resolution
    scene.render.resolution_y = resolution
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.view_settings.exposure = 0
    scene.view_settings.gamma = 1
    scene.render.image_settings.color_mode = "RGBA"

    # Do not alter imported mesh coordinates: camera/lighting pose around its
    # true bounds so each preview shows the actual package geometry.
    world = bpy.data.worlds.new(f"{package_id}_studio_world")
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.16, 0.16, 0.16, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.45
    bounds = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    center = sum(bounds, Vector()) / 8
    extent = max(max((p - center).length for p in bounds), 0.015)
    # Published charts are open sheets. The Y-facing studio camera makes the
    # face readable while its slight elevation exposes geometric relief.
    camera_data = bpy.data.cameras.new(f"{package_id}_camera")
    camera = bpy.data.objects.new(f"{package_id}_camera", camera_data)
    scene.collection.objects.link(camera)
    camera.location = center + Vector((0.36 * extent, -2.4 * extent, 2.8 * extent))
    direction = center - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = extent * 2.0
    camera_data.clip_start = max(.001,extent*.014)
    scene.camera = camera

    def area_light(name: str, offset: tuple[float, float, float], power: float, size: float):
        data = bpy.data.lights.new(name, "AREA")
        data.energy, data.shape, data.size = power*.22*(extent/1.2)**2, "DISK", size * extent
        light = bpy.data.objects.new(name, data)
        scene.collection.objects.link(light)
        light.location = center + Vector(offset) * extent
        light.rotation_euler = (center - light.location).to_track_quat("-Z", "Y").to_euler()

    area_light(f"{package_id}_key", (-2.0, -2.4, 3.0), 520, 2.0)
    area_light(f"{package_id}_fill", (2.4, -1.6, 0.6), 260, 2.5)
    area_light(f"{package_id}_rim", (0.3, 1.2, 2.5), 380, 1.5)

    # A compact studio floor provides contact/edge cues for this open geometry.
    bpy.ops.mesh.primitive_plane_add(size=extent * 7, location=(center.x, center.y + 0.35 * extent, center.z - 0.58 * extent))
    floor = bpy.context.object
    floor.name = f"{package_id}_studio_floor"
    floor_mat = bpy.data.materials.new(f"{package_id}_studio_floor_material")
    floor_mat.diffuse_color = (0.13, 0.13, 0.13, 1)
    floor_mat.use_nodes = True
    floor_mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.13, 0.13, 0.13, 1)
    floor_mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.82
    floor.data.materials.append(floor_mat)
    # Keep the imported face above the floor regardless of small vertical noise.
    floor.location.z = min((obj.matrix_world @ Vector(c)).z for c in obj.bound_box) - 0.04 * extent

    scene.render.filepath = str(output / f"{package_id}.png")
    bpy.ops.render.render(write_still=True)


def verify_one(package_id: str, source: Path, temp_root: Path, output: Path,
               resolution: int, samples: int) -> dict:
    temp = tempfile.TemporaryDirectory(prefix=f".{package_id}_", dir=temp_root)
    package = Path(temp.name)
    try:
        if source.is_file():
            package = safe_extract(source, package, package_id)
        else:
            package = source
        metadata_path = package / "metadata.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.is_file() else {}
        if metadata.get("id", package_id) != package_id:
            raise ValueError(f"metadata id does not match package name {package_id}")

        material_name, mtl_maps = parse_mtl(package / "material.mtl")
        if mtl_maps != EXPECTED_MAPS:
            raise ValueError(f"MTL map directives mismatch: {mtl_maps}")
        for filename in mtl_maps.values():
            if not (package / filename).is_file():
                raise FileNotFoundError(f"MTL references missing texture: {filename}")
        validate_obj_links(package / "material.obj", material_name)

        # Start each import from a clean scene so object bounds and images are
        # unambiguous. wm.obj_import defaults to Y-up OBJ -> Z-up Blender.
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete(use_global=False)
        for block in list(bpy.data.materials):
            if block.users == 0:
                bpy.data.materials.remove(block)
        before = set(bpy.data.objects)
        bpy.ops.wm.obj_import(filepath=str(package / "material.obj"))
        imported = [obj for obj in bpy.data.objects if obj not in before and obj.type == "MESH"]
        if len(imported) != 1:
            raise ValueError(f"Expected one imported mesh, found {len(imported)}")
        obj = imported[0]
        if not obj.data.polygons or not obj.data.vertices:
            raise ValueError("Imported OBJ mesh is empty")
        chart = uv_chart_stats(obj.data)
        images, image_stats = load_images(package)
        extents = [float(obj.dimensions[i]) for i in range(3)]
        if extents[2] <= 0 or max(extents) <= 0:
            raise ValueError(f"OBJ did not import as useful Z-up geometry: dimensions={extents}")
        assign_material(obj, material_name, images)
        output.mkdir(parents=True, exist_ok=True)
        render_preview(obj, images, package, package_id, output, resolution, samples, material_name)

        # Release loaded PNGs before temporary ZIP extraction is removed.
        for image in images.values():
            bpy.data.images.remove(image)
        result = {
            "id": package_id,
            "source": source.name,
            "status": "pass",
            "obj": "material.obj",
            "mtl_material": material_name,
            "mtl_maps": mtl_maps,
            "images": image_stats,
            "mesh": {"dimensions_blender_xyz": extents, **chart},
            "preview": f"{package_id}.png",
            "render": {"engine": "Cycles", "resolution": [resolution, resolution], "samples": samples},
        }
        print(f"PASS {package_id}: {len(obj.data.vertices)} vertices, {len(obj.data.polygons)} faces")
        return result
    finally:
        temp.cleanup()


def main() -> None:
    args = parse_args()
    packages = args.packages.resolve()
    evidence = args.evidence.resolve()
    # Scratch extraction is contained within MEDIA/Materials and is removed
    # after each package, including error paths.
    scratch_root = Path(__file__).resolve().parent
    results = []
    discovered = dict(discover_packages(packages))
    if not args.all:
        missing = set(PILOT_IDS)-discovered.keys()
        if missing:
            raise ValueError(f"Missing pilot packages: {', '.join(sorted(missing))}")
        discovered = {identity:discovered[identity] for identity in PILOT_IDS}
    for package_id, source in discovered.items():
        try:
            results.append(verify_one(package_id, source.resolve(), scratch_root, evidence, args.resolution, args.samples))
        except Exception as error:
            results.append({"id": package_id, "source": source.name, "status": "fail", "error": f"{type(error).__name__}: {error}"})
            print(f"FAIL {package_id}: {type(error).__name__}: {error}", file=sys.stderr)
    report = {"packages_dir": packages.name, "count": len(results),
              "passed": sum(item["status"] == "pass" for item in results),
              "failed": sum(item["status"] == "fail" for item in results), "packages": results}
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if report["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
