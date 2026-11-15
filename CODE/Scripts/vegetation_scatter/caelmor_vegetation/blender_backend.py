"""Blender inputs, approved asset links, and owned Geometry Nodes point batches."""

from dataclasses import dataclass
from pathlib import Path
import math

import bpy
import numpy as np
from mathutils import Euler, Matrix, Vector
from mathutils.geometry import convex_hull_2d

from .distribution import Guide, MASKS, Settings, Surface, Variant, group_tiles, scatter


LIBRARY_FILE = "Lowmark_Natural_Grass_Wildflowers.blend"
LAYER = "cv_generated_layer"
MANUAL = "cv_manual_layer"
SOURCE = "cv_asset_library"
BATCH = "cv_scatter_batch"
ASSET = "cv_asset"
ROTATION = "cv_rotation"
SCALE = "cv_scale"


@dataclass(frozen=True)
class Catalog:
    objects: tuple
    variants: tuple
    path: str


def default_library(scene_path=None):
    starts = [Path(__file__).resolve().parent]
    if scene_path or bpy.data.filepath:
        starts.insert(0, Path(scene_path or bpy.data.filepath).resolve().parent)
    for start in starts:
        for parent in (start, *start.parents):
            path = parent / "MEDIA" / "Materials" / "procedurally_generated" / LIBRARY_FILE
            if path.is_file():
                return str(path)
    return ""


def load_catalog(filepath):
    path = Path(bpy.path.abspath(filepath)).resolve() if filepath else Path(default_library())
    if not path.is_file() or path.suffix.lower() != ".blend":
        raise ValueError("Select the approved Lowmark vegetation .blend library.")
    matching = {lib for lib in bpy.data.libraries if Path(bpy.path.abspath(lib.filepath)).resolve() == path}
    known = {obj.name: obj for obj in bpy.data.objects if obj.library in matching and obj.name.startswith("LM_")}
    with bpy.data.libraries.load(str(path), link=True) as (available, output):
        names = sorted(name for name in available.objects if name.startswith("LM_"))
        missing = [name for name in names if name not in known]
        output.objects = list(missing)
    known.update(zip(missing, output.objects))
    if not names or any(known[name] is None for name in names):
        raise ValueError("The selected file has no readable Lowmark vegetation objects.")
    objects = tuple(known[name] for name in names)
    variants = {}
    for index, obj in enumerate(objects):
        if obj.type != "MESH" or "asset_family" not in obj or "lod" not in obj:
            raise ValueError(f"Missing approved vegetation metadata on {obj.name}.")
        key = obj["asset_family"], obj["growth_stage"]
        lod = obj["lod"]
        entries = variants.setdefault(key, {})
        if lod not in (0, 1, 2) or lod in entries or obj["triangles"] <= 0:
            raise ValueError(f"Invalid LOD metadata on {obj.name}.")
        entries[lod] = index
    result = []
    for (family, stage), lods in sorted(variants.items()):
        if set(lods) != {0, 1, 2}:
            raise ValueError(f"{family} {stage} is missing a required LOD.")
        ids = tuple(lods[lod] for lod in range(3))
        sources = [objects[i] for i in ids]
        triangles = tuple(obj["triangles"] for obj in sources)
        if not triangles[0] > triangles[1] > triangles[2] > 0:
            raise ValueError(f"{family} {stage} must have decreasing LOD triangle counts.")
        radius = max(math.hypot(corner[0], corner[1]) for obj in sources for corner in obj.bound_box)
        height = max(abs(corner[2]) for obj in sources for corner in obj.bound_box)
        head = sources[0]
        result.append(Variant(family, stage, ids, triangles, radius,
                              height, head["moisture_preference_01"], head["path_edge_affinity_01"],
                              head["patch_density_per_m2"], head["placement_layer"] == "filler"))
    return Catalog(objects, tuple(result), str(path))


def world_points(points, matrix):
    transform = np.asarray(matrix, dtype=np.float64)
    return np.asarray(points, dtype=np.float64) @ transform[:3, :3].T+transform[:3, 3]


def surface(obj, depsgraph):
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
    try:
        mesh.calc_loop_triangles()
        verts = np.empty(len(mesh.vertices)*3, np.float32)
        mesh.vertices.foreach_get("co", verts)
        coords = world_points(verts.reshape(-1, 3), evaluated.matrix_world)
        triangles = np.empty(len(mesh.loop_triangles)*3, np.int32)
        mesh.loop_triangles.foreach_get("vertices", triangles)
        corners = triangles.reshape(-1, 3)
        if not len(corners):
            raise ValueError(f"Terrain {obj.name} has no evaluated faces.")
        mask_values = np.empty((len(verts)//3, len(MASKS)), np.float64)
        groups = {}
        for column, (name, default) in enumerate(MASKS.items()):
            group = evaluated.vertex_groups.get(name)
            if group is None:
                mask_values[:, column] = default
            else:
                mask_values[:, column] = 0
                groups[group.index] = column
            attribute = mesh.attributes.get(name)
            if group is None and attribute is not None and attribute.domain == "POINT" and attribute.data_type == "FLOAT":
                values = np.empty(len(mesh.vertices), np.float32)
                attribute.data.foreach_get("value", values)
                mask_values[:, column] = values
        if groups:
            for vertex in mesh.vertices:
                for weight in vertex.groups:
                    if weight.group in groups:
                        mask_values[vertex.index, groups[weight.group]] = weight.weight
        return Surface(obj.name_full, coords[corners], np.clip(mask_values[corners], 0, 1))
    finally:
        evaluated.to_mesh_clear()


def stroke_segments(points, cyclic=False):
    points = np.asarray(points, dtype=np.float64)[:, :2]
    if cyclic:
        points = np.vstack((points, points[:1]))
    return np.stack((points[:-1], points[1:]), axis=1)


def path_segments(obj, scene, depsgraph):
    evaluated = obj.evaluated_get(depsgraph)
    if obj.type == "GREASEPENCIL":
        pieces = []
        for layer in evaluated.data.layers:
            if layer.hide:
                continue
            frames = [frame for frame in layer.frames if frame.frame_number <= scene.frame_current]
            if not frames:
                continue
            drawing = max(frames, key=lambda frame: frame.frame_number).drawing
            for stroke in drawing.strokes:
                if len(stroke.points) >= 2:
                    coords = [tuple(point.position) for point in stroke.points]
                    points = world_points(coords, evaluated.matrix_world @ layer.matrix_local)
                    pieces.append(stroke_segments(points, stroke.cyclic))
        return np.concatenate(pieces) if pieces else np.empty((0, 2, 2))
    if obj.type not in {"CURVE", "MESH"}:
        return np.empty((0, 2, 2))
    mesh = evaluated.to_mesh()
    try:
        if mesh.polygons:
            raise ValueError(f"Path guide {obj.name} must be an unbeveled curve or an edge-only mesh.")
        coords = [tuple(vertex.co) for vertex in mesh.vertices]
        edges = np.array([tuple(edge.vertices) for edge in mesh.edges], np.int32).reshape(-1, 2)
        if not len(edges):
            return np.empty((0, 2, 2))
        return world_points(coords, evaluated.matrix_world)[edges, :2]
    finally:
        evaluated.to_mesh_clear()


def guides_for(collection, scene, depsgraph, half_width, verge):
    if collection is None:
        return ()
    guides = []
    for obj in sorted(collection.all_objects, key=lambda item: item.name_full):
        segments = path_segments(obj, scene, depsgraph)
        length = np.linalg.norm(segments[:, 1]-segments[:, 0], axis=1)
        if (length > 1.e-8).any():
            guides.append(Guide(segments[length > 1.e-8], max(0., float(obj.get("cv_path_half_width", half_width))),
                                max(0., float(obj.get("cv_verge_width", verge)))))
    return tuple(guides)


def footprints_for(collection, depsgraph):
    if collection is None:
        return ()
    result = []
    for obj in sorted(collection.all_objects, key=lambda item: item.name_full):
        if obj.type not in {"MESH", "CURVE"}:
            continue
        evaluated = obj.evaluated_get(depsgraph)
        corners = np.unique(world_points(evaluated.bound_box, evaluated.matrix_world)[:, :2], axis=0)
        if len(corners) < 3:
            continue
        polygon = corners[convex_hull_2d([Vector(v) for v in corners])]
        if len(polygon) < 3:
            continue
        x, y = polygon.T
        area = x @ np.roll(y, -1)-y @ np.roll(x, -1)
        if abs(area) > 1.e-8:
            result.append(polygon if area > 0 else polygon[::-1])
    return tuple(result)


def layer_collection(scene, layer, tag):
    return next((col for col in scene.collection.children if col.get(tag) == layer), None)


def manual_collection(scene, layer):
    collection = layer_collection(scene, layer, MANUAL)
    if collection is None:
        collection = bpy.data.collections.new(f"Vegetation · {layer} · Protected")
        collection[MANUAL] = layer
        scene.collection.children.link(collection)
    return collection


def protected_roots(scene, layer, extra, default_spacing, previous=None):
    collection = layer_collection(scene, layer, MANUAL)
    objects = set()
    for group in (collection, extra):
        if group is not None:
            objects.update(group.all_objects)
    if previous is not None:
        objects.update(obj for obj in previous.all_objects if not obj.get(BATCH))
    roots = []
    for obj in sorted(objects, key=lambda item: item.name_full):
        if obj.get(BATCH):
            continue
        roots.append((*obj.matrix_world.translation[:2], max(0., float(obj.get("cv_clearance", default_spacing)))))
        if "cv_pin_origin" in obj:
            roots.append((*obj["cv_pin_origin"], .015))
    return roots


def node_tree(catalog):
    existing = next((tree for tree in bpy.data.node_groups if tree.get(SOURCE) == catalog.path), None)
    if existing is not None:
        return existing
    # The source collection is referenced by the modifier and never linked to
    # the view layer. The linked originals therefore stay at their own pivots.
    assets = bpy.data.collections.new("Lowmark vegetation · Linked source")
    for obj in catalog.objects:
        assets.objects.link(obj)
    tree = bpy.data.node_groups.new("Caelmor · Vegetation instances", "GeometryNodeTree")
    tree[SOURCE] = catalog.path
    for direction in ("INPUT", "OUTPUT"):
        tree.interface.new_socket(name="Geometry", in_out=direction, socket_type="NodeSocketGeometry")
    nodes, links = tree.nodes, tree.links
    start = nodes.new("NodeGroupInput")
    start.location = (-550, 200)
    info = nodes.new("GeometryNodeCollectionInfo")
    info.location = (-550, 0)
    info.inputs["Collection"].default_value = assets
    info.inputs["Separate Children"].default_value = True
    info.inputs["Reset Children"].default_value = True
    instances = nodes.new("GeometryNodeInstanceOnPoints")
    instances.location = (220, 200)
    instances.inputs["Pick Instance"].default_value = True
    output = nodes.new("NodeGroupOutput")
    output.location = (480, 200)
    links.new(start.outputs["Geometry"], instances.inputs["Points"])
    links.new(info.outputs["Instances"], instances.inputs["Instance"])
    for row, (name, kind, socket) in enumerate(((ASSET, "INT", "Instance Index"),
                                                (ROTATION, "FLOAT_VECTOR", "Rotation"),
                                                (SCALE, "FLOAT_VECTOR", "Scale"))):
        attribute = nodes.new("GeometryNodeInputNamedAttribute")
        attribute.data_type = kind
        attribute.inputs["Name"].default_value = name
        attribute.location = (-550, -235-180*row)
        value = attribute.outputs["Attribute"]
        if name == ROTATION:
            euler = nodes.new("FunctionNodeEulerToRotation")
            euler.location = (-230, -430)
            links.new(value, euler.inputs["Euler"])
            value = euler.outputs["Rotation"]
        links.new(value, instances.inputs[socket])
    links.new(instances.outputs["Instances"], output.inputs["Geometry"])
    return tree


def batch_object(collection, tree, placements, ids, cell, size):
    offset = np.array((cell[0]*size, cell[1]*size, 0.))
    name = f"Scatter {cell[0]:+d}, {cell[1]:+d}"
    mesh = bpy.data.meshes.new(name)
    mesh.vertices.add(len(ids))
    mesh.vertices.foreach_set("co", (placements.xyz[ids]-offset).astype(np.float32).ravel())
    for name_attr, kind, prop, values in ((ASSET, "INT", "value", placements.assets),
                                          (ROTATION, "FLOAT_VECTOR", "vector", placements.euler),
                                          (SCALE, "FLOAT_VECTOR", "vector", placements.scale)):
        attr = mesh.attributes.new(name_attr, kind, "POINT")
        attr.data.foreach_set(prop, values[ids].astype(np.int32 if kind == "INT" else np.float32).ravel())
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = tuple(offset)
    obj[BATCH] = True
    collection.objects.link(obj)
    modifier = obj.modifiers.new("Vegetation instances", "NODES")
    modifier.node_group = tree
    modifier.show_in_editmode = False


def discard_batches(collection):
    for obj in tuple(collection.objects):
        if obj.get(BATCH) and len(obj.users_collection) == 1:
            mesh = obj.data
            bpy.data.objects.remove(obj, do_unlink=True)
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)
    bpy.data.collections.remove(collection)


def apply_placement(scene, layer, catalog, settings, placements):
    old = layer_collection(scene, layer, LAYER)
    new = bpy.data.collections.new(f"Vegetation · {layer}")
    new[LAYER] = layer
    try:
        if len(placements.xyz):
            tree = node_tree(catalog)
            for cell, ids in group_tiles(placements.xyz[:, :2], settings.tile_size):
                batch_object(new, tree, placements, ids, cell, settings.tile_size)
        new["instances"] = len(placements.xyz)
        new["triangles"] = int(placements.cost.sum())
        new["lod_counts"] = np.bincount(placements.lod, minlength=3).tolist()
        new["signature"] = placements.signature
        new["candidates"] = placements.candidates
        new["requested_samples"] = placements.requested_samples
        new["habitat_count"] = placements.habitat_count
        scene.collection.children.link(new)
    except Exception:
        discard_batches(new)
        raise
    if old is not None:
        if old.users > 1:
            scene.collection.children.unlink(old)
        else:
            extras = [obj for obj in old.objects if not obj.get(BATCH)]
            if extras:
                target = manual_collection(scene, layer)
                for obj in extras:
                    if obj not in target.objects.values():
                        target.objects.link(obj)
            for child in tuple(old.children):
                if child not in scene.collection.children.values():
                    scene.collection.children.link(child)
            discard_batches(old)
        new.name = f"Vegetation · {layer}"
    return new


def generate(scene, depsgraph, terrain, catalog, settings, *, layer, path_collection=None,
             path_half_width=.65, verge_width=.86, structures=None, protected=None, spacing=.20, weights=None):
    if not terrain:
        raise ValueError("Select at least one terrain mesh in Object Mode.")
    if any(obj.type != "MESH" or obj.get(BATCH) or obj.get("cv_pinned_source") for obj in terrain):
        raise ValueError("Scatter targets must be terrain meshes.")
    if settings.scale[0] > settings.scale[1] or settings.lod_distances[0] > settings.lod_distances[1]:
        raise ValueError("Scale and LOD range values must be in ascending order.")
    if settings.elevation is not None and settings.elevation[0] > settings.elevation[1]:
        raise ValueError("Minimum elevation must be below maximum elevation.")
    layer = layer.strip()
    if not layer:
        raise ValueError("Give the output layer a name.")
    surfaces = [surface(obj, depsgraph) for obj in terrain]
    guides = guides_for(path_collection, scene, depsgraph, path_half_width, verge_width)
    footprints = footprints_for(structures, depsgraph)
    old = layer_collection(scene, layer, LAYER)
    roots = protected_roots(scene, layer, protected, spacing, old)
    placements = scatter(surfaces, catalog.variants, settings, guides=guides, footprints=footprints,
                         protected=roots, weights=weights)
    return apply_placement(scene, layer, catalog, settings, placements), placements


def place_manual(scene, layer, source, matrix, clearance):
    group = manual_collection(scene, layer)
    obj = bpy.data.objects.new(f"Pinned · {source.name}", source.data)
    obj["cv_pinned_source"] = source.name
    obj["cv_clearance"] = clearance
    group.objects.link(obj)
    obj.matrix_world = matrix
    return obj


def pin_points(context, obj, clearance):
    if not obj.get(BATCH) or obj.mode != "EDIT":
        raise ValueError("Select vertices in one generated point batch in Edit Mode.")
    if len(context.objects_in_mode) != 1:
        raise ValueError("Pin points from one batch at a time.")
    owner = next((group for group in obj.users_collection if LAYER in group), None)
    if owner is None or owner not in context.scene.collection.children.values():
        raise ValueError("The selected batch does not belong to this scene.")
    if owner.users > 1:
        raise ValueError("Regenerate this layer in the current scene before pinning a shared batch.")
    linked = obj.modifiers[0].node_group.nodes.get("Collection Info").inputs["Collection"].default_value
    sources = sorted(linked.objects, key=lambda source: source.name)
    bpy.ops.object.mode_set(mode="OBJECT")
    try:
        selected = [v.index for v in obj.data.vertices if v.select and not v.hide]
        if not selected:
            return 0
        if obj.data.users > 1:
            obj.data = obj.data.copy()
        triangles = 0
        lod_counts = list(owner["lod_counts"])
        for index in selected:
            mesh = obj.data
            source = sources[mesh.attributes[ASSET].data[index].value]
            rotation = Euler(mesh.attributes[ROTATION].data[index].vector).to_quaternion()
            scale = mesh.attributes[SCALE].data[index].vector
            matrix = obj.matrix_world @ Matrix.LocRotScale(mesh.vertices[index].co, rotation, scale)
            pinned = place_manual(context.scene, owner[LAYER], source, matrix, clearance)
            pinned["cv_pin_origin"] = tuple(matrix.translation[:2])
            triangles += source["triangles"]
            lod_counts[source["lod"]] -= 1
    finally:
        bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.delete(type="VERT")
    owner["instances"] -= len(selected)
    owner["triangles"] -= triangles
    owner["lod_counts"] = lod_counts
    return len(selected)
