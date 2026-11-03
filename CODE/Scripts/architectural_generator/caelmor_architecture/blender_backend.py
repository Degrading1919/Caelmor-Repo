"""Blender scene, UV, material, and export adapter for the pure geometry engine."""
import json, math, os, uuid
import bpy
from mathutils import Vector, Matrix
from .engine import generate, validate, geometry_hash, TOOL_REVISION
from .materials import get_material, surface_tint

TAG = "caelm_generated"
COLLECTION_TAG = "caelm_build"
SETTINGS_KEY = "caelm_settings"
LAYER_ORDER = ("foundation", "walls", "structure", "windows", "doors", "details", "roof")
SCOPE_LAYERS = {"ROOF": {"roof"}, "WINDOWS": {"windows", "doors"}, "DETAILS": {"details"}}


def _settings_dict(settings):
    if hasattr(settings, "__dataclass_fields__"):
        return {name: getattr(settings, name) for name in settings.__dataclass_fields__}
    return dict(settings)


def load_settings(collection):
    raw = collection.get(SETTINGS_KEY)
    if not raw:
        raise ValueError("Selected collection has no saved Caelmor settings")
    return json.loads(raw)


def _normalize_settings_data(data):
    """Additive migration: old snapshots remain manual Lowmark SOLID plans."""
    from .model import Settings
    allowed = Settings.__dataclass_fields__.keys()
    values = {key: data[key] for key in allowed if key in data}
    # Version 0.2 only generated gables, so its snapshots must not inherit the
    # newer AUTO type roof when partially replacing just one visual layer.
    values.setdefault("region", "LOWMARK")
    values.setdefault("use_grammar", False)
    values.setdefault("world_aware", False)
    values.setdefault("geometry_mode", "SOLID")
    values.setdefault("roof_style", "GABLE")
    normalized = Settings(**values)
    return {key: getattr(normalized, key) for key in allowed}


def _project(p, axis):
    return (p.y, p.z) if axis == 0 else ((p.x, p.z) if axis == 1 else (p.x, p.y))


def _metric_uv(mesh, material):
    layer = mesh.uv_layers.new(name="UV0_Metric")
    follow_edge = material in {"timber", "timber_light"} or material.startswith('roof')
    for poly in mesh.polygons:
        vertices = [mesh.vertices[mesh.loops[i].vertex_index].co.copy() for i in poly.loop_indices]
        if follow_edge and len(vertices) >= 3:
            edge = max((vertices[(i+1) % len(vertices)] - vertices[i] for i in range(len(vertices))), key=lambda v: v.length)
            normal = poly.normal.normalized()
            tangent = (edge - normal * edge.dot(normal)).normalized()
            bitangent = normal.cross(tangent).normalized()
            center = sum(vertices, Vector()) / len(vertices)
            for li, vertex in zip(poly.loop_indices, vertices):
                delta = vertex - center
                layer.data[li].uv = (delta.dot(tangent), delta.dot(bitangent))
        else:
            axis = max(range(3), key=lambda i: abs(poly.normal[i]))
            for li, vertex in zip(poly.loop_indices, vertices):
                layer.data[li].uv = _project(vertex, axis)
    return layer


def _lightmap_uv(mesh):
    layer = mesh.uv_layers.new(name="UV1_Lightmap")
    count = max(1, len(mesh.polygons)); cols = max(1, math.ceil(math.sqrt(count)))
    rows = max(1, math.ceil(count / cols)); pad = .10
    for fi, poly in enumerate(mesh.polygons):
        col, row = fi % cols, fi // cols
        axis = max(range(3), key=lambda i: abs(poly.normal[i]))
        pts = [_project(mesh.vertices[mesh.loops[i].vertex_index].co, axis) for i in poly.loop_indices]
        u0, u1 = min(p[0] for p in pts), max(p[0] for p in pts)
        v0, v1 = min(p[1] for p in pts), max(p[1] for p in pts)
        su, sv = max(u1-u0, 1e-6), max(v1-v0, 1e-6)
        scale = min((1-2*pad)/su, (1-2*pad)/sv)
        ou, ov = (1-su*scale)/2, (1-sv*scale)/2
        for li, (u, v) in zip(poly.loop_indices, pts):
            x = pad + ou + (u-u0)*scale
            y = pad + ov + (v-v0)*scale
            layer.data[li].uv = ((col+x*(1-2*pad))/cols, (row+y*(1-2*pad))/rows)


def _layer_for(buffer):
    layer = getattr(buffer, "layer", "structure")
    return layer if layer in LAYER_ORDER else "structure"


def _mesh_object(buffer, cache, build_id, plan=None):
    mesh = bpy.data.meshes.new(buffer.name + "Mesh")
    mesh.from_pydata(buffer.vertices, [], buffer.faces); mesh.update(calc_edges=True)
    if not mesh.polygons:
        bpy.data.meshes.remove(mesh); return None
    for face in mesh.polygons: face.use_smooth = False
    material = getattr(buffer, "material", "timber")
    style = getattr(plan, "style", None)
    settings = getattr(plan, "settings", None)
    mesh.materials.append(get_material(material, cache, style=style, settings=settings))
    uv0 = _metric_uv(mesh, material)
    _lightmap_uv(mesh)
    # COLOR_0 carries deterministic environmental weathering into glTF/GLB.
    # Corner colors let adjacent faces retain their own exposure without changing geometry.
    tint_layer = mesh.color_attributes.new(name="CaelmorTint", type='FLOAT_COLOR', domain='CORNER')
    for poly in mesh.polygons:
        normal = tuple(poly.normal)
        for loop_index in poly.loop_indices:
            vertex = mesh.vertices[mesh.loops[loop_index].vertex_index].co
            tint_layer.data[loop_index].color = surface_tint(tuple(vertex), normal, material, plan, style, settings)
    mesh.uv_layers.active_index = 0
    # Set the single render-layer index last, using a fresh RNA reference after
    # adding UV1. Clearing another layer can clear the shared render flag.
    mesh.uv_layers[0].active_render = True
    obj = bpy.data.objects.new(buffer.name, mesh)
    obj[TAG] = True; obj["caelm_layer"] = _layer_for(buffer)
    obj["caelm_buffer_id"] = buffer.name
    obj["caelm_material"] = material; obj["caelm_semantic"] = _layer_for(buffer)
    obj["caelm_world_zone"] = str(getattr(buffer, "world_zone", None) or "")
    obj["caelm_build_id"] = build_id
    topology = str(getattr(buffer, "topology", "SOLID")).upper()
    obj["caelm_topology"] = topology if topology in ("SOLID", "SURFACE") else "SOLID"
    obj["caelm_structural_role"] = str(getattr(buffer, "structural_role", "framing"))
    for attr, tag in (("roof_envelope", "caelm_roof_envelope"),
                      ("support_surface", "caelm_support_surface")):
        value = getattr(buffer, attr, None)
        if value is not None:
            obj[tag] = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return obj


def _collider_object(name, vertices, faces, build_id, world_zone=None):
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(vertices, [], faces); mesh.update(calc_edges=True)
    obj = bpy.data.objects.new(name, mesh)
    obj["caelm_collider"] = True; obj["caelm_generated"] = True
    obj["caelm_layer"] = "collider"; obj["caelm_semantic"] = "collider"
    obj["caelm_build_id"] = build_id
    obj["caelm_world_zone"] = str(world_zone or "")
    obj.hide_render = True
    return obj


def _colliders(plan, build_id):
    """Make simple, closed collision proxies per outer wall and footprint wing."""
    out = []
    half = .09
    zones = getattr(plan, "world_zones", None)
    if zones:
        # A world plan may contain separated or stepped masses. Keep each
        # collision proxy attached to its actual zone bounds and base height.
        for zone_index, mass in enumerate(zones, 1):
            for index, edge in enumerate(mass.plan.edges, 1):
                a, b = Vector((edge[0][0], edge[0][1], mass.base)), Vector((edge[1][0], edge[1][1], mass.base))
                direction = b - a
                length = math.hypot(direction.x, direction.y)
                if length < 1e-5: continue
                normal = Vector((-direction.y / length, direction.x / length, 0)) * half
                bottom = [a - normal, b - normal, b + normal, a + normal]
                top = [Vector((v.x, v.y, mass.eave)) for v in bottom]
                verts = [tuple(v) for v in bottom + top]
                faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
                         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
                out.append(_collider_object(
                    f"Collider Wall {zone_index:02d}-{index:02d}", verts, faces, build_id, mass.key))
            for index, rect in enumerate(mass.plan.rects, 1):
                x0, y0, x1, y1, _axis = rect
                z0, z1 = mass.base-.16, mass.base
                verts = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
                         (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
                faces = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
                out.append(_collider_object(
                    f"Collider Floor {zone_index:02d}-{index:02d}", verts, faces, build_id, mass.key))
    else:
        # Preserve legacy collider geometry and names for snapshots and manual mode.
        eave = plan.eave
        for index, edge in enumerate(plan.edges):
            a, b = Vector((edge[0][0], edge[0][1], 0)), Vector((edge[1][0], edge[1][1], 0))
            direction = b - a
            length = math.hypot(direction.x, direction.y)
            if length < 1e-5: continue
            normal = Vector((-direction.y / length, direction.x / length, 0)) * half
            bottom = [a - normal, b - normal, b + normal, a + normal]
            top = [v + Vector((0, 0, eave)) for v in bottom]
            verts = [tuple(v) for v in bottom + top]
            faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
                     (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
            out.append(_collider_object(f"Collider Wall {index+1:02d}", verts, faces, build_id))
        for index, rect in enumerate(plan.rects):
            x0, y0, x1, y1, _axis = rect
            z0, z1 = 0.0, .2
            verts = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
                     (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
            faces = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
            out.append(_collider_object(f"Collider Floor {index+1:02d}", verts, faces, build_id))
    return out


def _new_collection(name):
    coll = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(coll)
    coll[COLLECTION_TAG] = True
    return coll


def _cleanup_stage(stage):
    if stage is None: return
    for obj in list(stage.objects): _remove_object(obj)
    if stage.name in bpy.data.collections: bpy.data.collections.remove(stage)


def _remove_object(obj):
    data = obj.data if obj.type == 'MESH' else None
    bpy.data.objects.remove(obj, do_unlink=True)
    if data is not None and data.users == 0:
        bpy.data.meshes.remove(data)


def _focus_collection(collection):
    visual = [obj for obj in collection.objects if obj.get(TAG) and not obj.get("caelm_collider")]
    if not visual: return
    for obj in bpy.context.selected_objects: obj.select_set(False)
    visual[0].select_set(True)
    bpy.context.view_layer.objects.active = visual[0]


def _ensure_anchor(collection, origin=None):
    anchor = next((obj for obj in collection.objects if obj.get("caelm_anchor")), None)
    if anchor is None:
        anchor = bpy.data.objects.new("Caelmor Building Root", None)
        anchor.empty_display_type = 'PLAIN_AXES'
        anchor.empty_display_size = 1.2
        anchor["caelm_anchor"] = True
        anchor["caelm_semantic"] = "building_root"
        anchor.location = origin if origin is not None else bpy.context.scene.cursor.location
        collection.objects.link(anchor)
    return anchor


def _parent_to_anchor(obj, anchor):
    obj.parent = anchor
    obj.matrix_parent_inverse = Matrix.Identity(4)


def build(settings, collection=None, layers=None, origin=None):
    """Build off-scene, then swap generated objects in requested layers only."""
    if collection is not None and not collection.get(COLLECTION_TAG):
        raise ValueError("Selected collection is not a Caelmor generated building")
    plan, buffers = generate(settings)
    validation = validate(plan, buffers)
    if isinstance(validation, dict) and not validation.get("valid", False):
        raise ValueError("Geometry validation failed; existing building was left unchanged")
    setting_data = _settings_dict(settings)
    scope = None
    if isinstance(layers, str) and layers.upper() != "ALL":
        scope = SCOPE_LAYERS.get(layers.upper())
        if scope is None: raise ValueError(f"Unknown regeneration scope: {layers}")
    elif layers is not None and not isinstance(layers, str): scope = set(layers)
    if collection and scope is not None:
        if _normalize_settings_data(load_settings(collection)) != _normalize_settings_data(setting_data):
            raise ValueError("Settings differ from this building. Load its saved settings or regenerate All Layers first.")
        present = {o.get("caelm_layer") for o in collection.objects if o.get(TAG)}
        if scope - present: raise ValueError("Cannot partially regenerate missing layers: " + ", ".join(sorted(scope-present)))
    protected_ids = {o.get("caelm_buffer_id") for o in (collection.objects if collection else ())
                     if o.get(TAG) and o.get("caelm_protected")}
    build_id = uuid.uuid4().hex; stage = _new_collection("__CAELMOR_STAGE__" + build_id[:8])
    try:
        cache = {}
        for buffer in buffers:
            if buffer.name not in protected_ids and (scope is None or _layer_for(buffer) in scope):
                # Finish/wear uses the actual host volume's roof, apertures and
                # hearths. A world building may contain multiple eave heights.
                mesh_plan=plan
                if hasattr(plan,'world_zones'):
                    host=next((m for m in plan.world_zones
                               if m.key==getattr(buffer,'world_zone',None)),None)
                    if host is not None:mesh_plan=host.plan
                obj = _mesh_object(buffer, cache, build_id, mesh_plan)
                if obj: stage.objects.link(obj)
        if scope is None:
            for obj in _colliders(plan, build_id):
                stage.objects.link(obj); obj.hide_set(True)
        if collection is None: collection = _new_collection("Caelmor Building")
        anchor = _ensure_anchor(collection, origin)
        old_generated = [obj for obj in collection.objects if obj.get(TAG) and not obj.get("caelm_protected")
                         and (scope is None or obj.get("caelm_layer") in scope)]
        staged = list(stage.objects)
        for obj in staged:
            _parent_to_anchor(obj, anchor)
            collection.objects.link(obj)
        for obj in old_generated: _remove_object(obj)
        for obj in staged: stage.objects.unlink(obj)
        _cleanup_stage(stage); stage = None
        collection[COLLECTION_TAG] = True
        collection[SETTINGS_KEY] = json.dumps(setting_data, sort_keys=True)
        collection["caelm_geometry_hash"] = geometry_hash(buffers)
        collection["caelm_source_geometry_hash"] = geometry_hash(buffers)
        collection["caelm_architecture"] = validation.get("architecture", "WORLD" if settings.world_aware else "LEGACY")
        construction_zones = validation.get("construction_zones", [])
        collection["caelm_construction_zones"] = json.dumps(construction_zones, sort_keys=True)
        collection["caelm_source_validation"] = json.dumps({
            "valid": bool(validation.get("valid", False)),
            "source_objects": int(validation.get("objects", len(buffers))),
            "source_vertices": int(validation.get("vertices", 0)),
            "source_triangles": int(validation.get("triangles", 0)),
            "construction_zones": construction_zones,
        }, sort_keys=True)
        collection["caelm_generator_version"] = TOOL_REVISION; collection["caelm_units"] = "metres"
        collection["caelm_validation"] = json.dumps({
            "valid": bool(validation.get("valid", False)) if isinstance(validation, dict) else True,
            "errors": list(validation.get("errors", ())) if isinstance(validation, dict) else [],
            "triangles": int(validation.get("triangles", 0)) if isinstance(validation, dict) else 0,
            "objects": int(validation.get("objects", len(buffers))) if isinstance(validation, dict) else len(buffers),
            "architecture": validation.get("architecture", "WORLD" if settings.world_aware else "LEGACY"),
            "source_objects": int(validation.get("objects", len(buffers))),
            "source_vertices": int(validation.get("vertices", 0)),
            "source_triangles": int(validation.get("triangles", 0)),
            "construction_zones": construction_zones,
        }, sort_keys=True)
        _focus_collection(collection)
        return collection, collection_metrics(collection)
    except Exception:
        _cleanup_stage(stage); raise


def collection_metrics(collection):
    objects = [o for o in collection.objects if o.get(TAG) and not o.get("caelm_collider")]
    points = [o.matrix_world @ Vector(c) for o in objects for c in o.bound_box]
    if points:
        dims = [max(p[i] for p in points)-min(p[i] for p in points) for i in range(3)]
    else: dims = [0.0, 0.0, 0.0]
    return {"objects": len(objects), "vertices": sum(len(o.data.vertices) for o in objects),
            "width": dims[0], "depth": dims[1], "height": dims[2],
            "layers": sorted({o.get("caelm_layer", "") for o in objects})}


def _export_selection(filepath, objects, anchor, export_format):
    view_layer = bpy.context.view_layer
    prior_selected = list(bpy.context.selected_objects)
    prior_active = view_layer.objects.active
    hidden_state = {obj: obj.hide_get() for obj in objects if obj.get("caelm_collider")}
    try:
        for obj in prior_selected: obj.select_set(False)
        for obj in objects:
            if obj.get("caelm_collider"): obj.hide_set(False)
            obj.select_set(True)
        anchor.select_set(True)
        view_layer.objects.active = anchor
        bpy.ops.export_scene.gltf(filepath=filepath, export_format=export_format, use_selection=True,
                                  export_apply=True, export_extras=True, export_yup=True)
    finally:
        for obj in list(bpy.context.selected_objects): obj.select_set(False)
        for obj in objects:
            if obj.get("caelm_collider"):
                obj.hide_set(hidden_state.get(obj, True))
        for obj in prior_selected:
            try: obj.select_set(True)
            except ReferenceError: pass
        try: view_layer.objects.active = prior_active
        except ReferenceError: view_layer.objects.active = None


def export_building(collection, filepath):
    """Export the generated collection to glTF/GLB plus a semantic JSON sidecar."""
    if not collection or not collection.get(COLLECTION_TAG): raise ValueError("No Caelmor generated building is selected")
    objects = [o for o in collection.objects if o.get(TAG) and not o.get("caelm_collider")]
    if not objects: raise ValueError("Building collection contains no generated geometry")
    anchor = next((obj for obj in collection.objects if obj.get("caelm_anchor")), None)
    if anchor is None: raise ValueError("Building root anchor is missing")
    fmt = 'GLB' if os.path.splitext(filepath)[1].lower() == '.glb' else 'GLTF_SEPARATE'
    _export_selection(filepath, objects, anchor, fmt)
    colliders = [o for o in collection.objects if o.get("caelm_collider")]
    if colliders:
        collider_path = os.path.splitext(filepath)[0] + ".collision.glb"
        _export_selection(collider_path, colliders, anchor, 'GLB')
    manifest = {"format": "CaelmorBuildingExport", "version": 1, "generator_version": TOOL_REVISION,
                "settings": load_settings(collection),
                "architecture": collection.get("caelm_architecture", "LEGACY"),
                "construction_zones": json.loads(collection.get("caelm_construction_zones", "[]")),
                "source_validation": json.loads(collection.get("caelm_source_validation", "{}")),
                "source_geometry_hash": collection.get("caelm_source_geometry_hash", ""),
                "has_protected_buffers": any(o.get("caelm_protected") for o in objects),
                "protected_buffer_count": sum(1 for o in objects if o.get("caelm_protected")),
                "units": "metres", "up_axis": "Y",
                "collision": {"file": os.path.basename(os.path.splitext(filepath)[0] + ".collision.glb") if colliders else None,
                              "object_count": len(colliders),
                              "wall_proxy_count": sum(1 for o in colliders if o.name.startswith("Collider Wall ")),
                              "floor_proxy_count": sum(1 for o in colliders if o.name.startswith("Collider Floor ")),
                              "note": "Approximate static outer-wall and footprint proxies; not tested for traversal."},
                "anchor": {"name": anchor.name, "location": list(anchor.location),
                           "rotation_euler": list(anchor.rotation_euler), "scale": list(anchor.scale)},
                "layers": collection_metrics(collection)["layers"],
                "objects": [{"name": o.name, "layer": o.get("caelm_layer"), "material": o.get("caelm_material"),
                             "world_zone": str(o.get("caelm_world_zone", "")),
                             "semantic": o.get("caelm_semantic"), "protected": bool(o.get("caelm_protected")),
                             "topology": o.get("caelm_topology", "SOLID"),
                             "structural_role": o.get("caelm_structural_role", "framing"),
                             "roof_envelope": json.loads(o["caelm_roof_envelope"]) if o.get("caelm_roof_envelope") else None,
                             "support_surface": json.loads(o["caelm_support_surface"]) if o.get("caelm_support_surface") else None}
                            for o in objects]}
    sidecar = os.path.splitext(filepath)[0] + ".caelmor.json"
    with open(sidecar, "w", encoding="utf-8") as f: json.dump(manifest, f, indent=2)
    return sidecar
