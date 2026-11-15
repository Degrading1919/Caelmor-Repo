"""Build the Lowmark settlement showcase from the released tools and material libraries."""

from argparse import ArgumentParser
from collections import Counter
from dataclasses import replace
from pathlib import Path
import hashlib
import json
import math
import sys

import bpy
import numpy as np
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Matrix, Vector

HERE = Path(__file__).resolve().parent
ARCH = HERE.parents[1]
REPO = ARCH.parents[2]
MEDIA = REPO / "MEDIA" / "Materials" / "procedurally_generated"
sys.path[:0] = [str(ARCH), str(ARCH.parent / "vegetation_scatter"), str(MEDIA)]

from caelmor_architecture.blender_backend import build
from caelmor_architecture.model import Settings, make_plan
from caelmor_architecture.roof_autocomplete import build_roof_collection
from caelmor_architecture.roof_selection import Bearing
from caelmor_vegetation import blender_backend as vegetation
from caelmor_vegetation.distribution import FAMILY_WEIGHTS, Settings as ScatterSettings, guide_fields, wall_fields
from build_lowmark_handcrafted_glass import DrawnGlass, TILE as GLASS_TILE, pane, verify_shell
from build_lowmark_lime_plaster import approved_context_materials, set_material
from build_lowmark_packed_earth import LENGTH, UV, Soil, material as ground_material, mesh_with_uv
from build_lowmark_planked_oak import orient_and_phase
from build_lowmark_structural_timber import grid_faces, point, profile, ramp


UP = Vector((0., 0., 1.))
STUDIES = {
    "Farmhouse": (Settings(seed=39, function="FARMHOUSE", footprint="L", width=10.7, depth=6.8,
                           wing_width=4.85, wing_depth=3.15, floors=2, floor_height=2.48, pitch=40,
                           overhang=.52, age=27, maintenance=.73, detail="HIGH", crafted_curves=True),
                   (-6.45, 8.35), -5.5, 86, "Maintained", "Weathered", "Maintained", "Clear"),
    "Cottage": (Settings(seed=64, function="COTTAGE", footprint="RECT", width=7.60, depth=4.85,
                         floors=1, floor_height=2.40, pitch=49, overhang=.42, wealth="MODEST",
                         age=64, maintenance=.48, detail="HIGH", crafted_curves=True, window_density=.80),
                 (-15.50, -.12), 15.5, 95, "Aged", "Heavily Aged", "Weathered", "Lightly Weathered"),
    "Workshop": (Settings(seed=92, function="WORKSHOP", footprint="RECT", width=10.65, depth=5.55,
                          floors=1, floor_height=2.68, pitch=34, overhang=.63, wealth="ESTABLISHED",
                          age=41, maintenance=.54, detail="HIGH", crafted_curves=True, window_density=1.20),
                  (7.75, 1.40), -15.5, 82, "Aged", "Maintained", "Corroded", "Obscured"),
}


def group(scene, name):
    collection = bpy.data.collections.new(name)
    scene.collection.children.link(collection)
    return collection


def move_to(obj, collection):
    if obj not in collection.objects.values():
        collection.objects.link(obj)
    for current in tuple(obj.users_collection):
        if current != collection:
            current.objects.unlink(obj)


def take_materials(file, names):
    with bpy.data.libraries.load(str(MEDIA / file)) as (source, output):
        if not set(names) <= set(source.materials):
            raise RuntimeError(f"Missing approved finish in {file}: {set(names)-set(source.materials)}")
        output.materials = list(names)
    return dict(zip(names, output.materials))


def approved_finishes():
    timber, masonry, stone = approved_context_materials()
    finishes = {"Timber": timber, "Masonry": masonry, "Stone": stone}
    requests = (
        ("Lowmark_Lime_Plaster_Whitewash.blend", "Lowmark Lime Plaster", "Plaster", ("Maintained", "Aged")),
        ("Lowmark_Planked_Oak_Joinery.blend", "Lowmark Planked Oak", "Oak", ("Wood Maintained", "Wood Weathered", "Wood Heavily Aged")),
        ("Lowmark_Forged_Iron_Hardware.blend", "Lowmark Forged Iron", "Iron", ("Maintained", "Weathered", "Corroded")),
        ("Lowmark_Handcrafted_Window_Glass.blend", "Lowmark Handcrafted Glass", "Glass", ("Clear", "Lightly Weathered", "Obscured")),
        ("Lowmark_Structural_Timber.blend", "Lowmark Structural Timber", "Crosscut", ("Crosscut",)),
    )
    for file, prefix, key, finish_list in requests:
        obtained = take_materials(file, tuple(f"{prefix} | {name}" for name in finish_list))
        for label in finish_list:
            finishes[key, label.removeprefix("Wood ")] = obtained[f"{prefix} | {label}"]
    return finishes


def base_height(x, y):
    return (.39*np.sin(x*.16+.5)*np.cos(y*.17+.4) + .22*np.sin(y*.17+x*.11)
            + .034*np.sin(x*1.43+y*.93) + .039*np.sin(y*1.87-x*.68) + .020*y
            + 7.9*np.exp(-((y-42.)/17.)**2-((x+10.)/31.)**2)
            + 6.1*np.exp(-((y-52.)/18.)**2-((x-35.)/23.)**2)
            + 3.1*np.exp(-((y-20.)/29.)**2-((x+39.)/12.)**2))


def phase_uv(obj, offset):
    uv = obj.data.uv_layers.get("UV0_Metric")
    if uv is None:
        raise RuntimeError(f"{obj.name} is missing UV0_Metric")
    data = np.empty(2*len(uv.data), np.float32)
    uv.data.foreach_get("uv", data)
    data.reshape(-1, 2)[:] += offset
    uv.data.foreach_set("uv", data)


def bevel(obj, width):
    modifier = obj.modifiers.new("Showcase edge rounding", "BEVEL")
    modifier.width = width
    modifier.segments = 2
    modifier.angle_limit = math.radians(34)


def face_glass(scene, body, plan, transform, finish, output, draft):
    field = DrawnGlass(70931+plan.settings.seed, 1.)
    rng = np.random.default_rng(9081+plan.settings.seed)
    count = 0
    for obj in tuple(body.all_objects):
        key = obj.get("caelm_buffer_id", "")
        if obj.type != "MESH" or not key.startswith("facade_windows"):
            continue
        coords = np.asarray([tuple(v.co) for v in obj.data.vertices])
        if len(coords) % 8 or len(obj.data.polygons)*8 != len(coords)*6:
            raise RuntimeError(f"Unexpected glazing topology in {key}")
        for box in coords.reshape(-1, 8, 3):
            low, high = box.min(axis=0), box.max(axis=0)
            center = Vector((low+high)*.5)
            small = int(np.argmin((high-low)[:2]))
            if not np.isclose(high[small]-low[small], .018, atol=.001):
                raise RuntimeError(f"Unexpected glazing placeholder thickness in {key}")
            candidates = []
            for a, b in plan.edges:
                if abs(a[small]-b[small]) < 1e-8 and min(a[1-small], b[1-small])-.001 <= center[1-small] <= max(a[1-small], b[1-small])+.001:
                    n = Vector((b[1]-a[1], a[0]-b[0], 0.)).normalized()
                    candidates.append((abs(center[small]-a[small]), n))
            _, normal = min(candidates, key=lambda candidate: candidate[0])
            u = UP.cross(normal)
            width, height = float(high[1-small]-low[1-small]), float(high[2]-low[2])
            start = center-u*(.5*width+.051)
            start.z = low[2]-.058
            ux, nx = transform.to_3x3() @ u, transform.to_3x3() @ normal
            phase = tuple(rng.uniform(0, GLASS_TILE, 2))
            glass, points, faces = pane(f"Drawn glass {count+1:02d}", field, width+.102, height+.116,
                                        transform @ start, ux, nx, phase, finish, .020 if draft else .012,
                                        clear=finish.name.endswith("Clear"))
            if count == 0:
                verify_shell(points, faces, nx)
            move_to(glass, output)
            glass["showcase_material"] = finish.name
            count += 1
        obj.hide_render = True
        obj.hide_set(True)
    if not count:
        raise RuntimeError(f"{body.name} has no fitted panes")
    return count


def bind_riven(field):
    material = field.copy()
    material.name = "Lowmark Brookoak | Riven Bake on registered roof UVs"
    del material["caelm_brookoak_maps"]
    checks = {}
    for texture in (node for node in material.node_tree.nodes if node.type == "TEX_IMAGE"):
        path = Path(texture.image.filepath)
        suffix = path.name.removeprefix("Lowmark_Brookoak_RoofShingles")
        source = MEDIA / f"Lowmark_Brookoak_RoofShingles_RivenBake{suffix}"
        colorspace = texture.image.colorspace_settings.name
        texture.image = bpy.data.images.load(str(source), check_existing=True)
        texture.image.colorspace_settings.name = colorspace
        checks[suffix] = hashlib.sha256(source.read_bytes()).hexdigest()
    material["showcase_source_maps_sha256"] = json.dumps(checks, sort_keys=True)
    return material


def building(scene, name, spec, finishes, roofs, draft):
    settings, location, heading, detail, plaster_finish, oak_finish, iron_finish, glass_finish = spec
    plan = make_plan(settings)
    angle = math.radians(heading)
    z = float(base_height(*location))
    transform = Matrix.Translation(Vector((*location, z))) @ Matrix.Rotation(angle, 4, "Z")
    compound = group(scene, name)
    body, _ = build(settings, origin=(*location, z))
    body.name = f"{name} · Generator body"
    compound.children.link(body)
    if body in scene.collection.children.values():
        scene.collection.children.unlink(body)
    anchors = [ob for ob in body.objects if ob.type == "EMPTY" and ob.get("caelm_build_anchor")]
    if not anchors:
        anchors = [ob for ob in body.objects if ob.type == "EMPTY" and ob.parent is None]
    anchor, = anchors
    anchor.rotation_euler.z = angle
    bpy.context.view_layer.update()
    phase = np.random.default_rng(settings.seed+3814)
    classifications = Counter()
    unseen = []
    entrance = None
    post_feet = []
    for obj in tuple(body.all_objects):
        key = obj.get("caelm_buffer_id", "")
        if obj.type != "MESH":
            continue
        layer = obj.get("caelm_layer", "")
        role = obj.get("caelm_material", "")
        if obj.get("caelm_collider") or layer == "roof" or key.startswith(("facade_stone", "facade_mortar")):
            obj.hide_render = True
            obj.hide_set(True)
            continue
        if key.startswith("facade_windows"):
            continue
        if key.startswith("facade_porch::floor"):
            for upright in np.asarray([tuple(v.co) for v in obj.data.vertices]).reshape(-1,8,3):
                low,high=upright.min(axis=0),upright.max(axis=0)
                if high[2]-low[2]>1.25 and max(high[:2]-low[:2])<.35:
                    post_feet.append(transform @ Vector((*(.5*(low[:2]+high[:2])),low[2])))
        if key.startswith("facade_details") and name in {"Farmhouse","Cottage"}:
            # The generated soot marker is an opaque rectangular decal proxy.
            obj.hide_render=True
            obj.hide_set(True)
            continue
        edge_round = 0.
        if key.startswith(("facade_doors", "facade_shutters")):
            label, finish, edge_round = "Planked Oak", finishes["Oak", oak_finish], .008
            orient_and_phase(obj)
            if key.startswith("facade_doors"):
                bb = np.asarray([tuple(v.co) for v in obj.data.vertices])
                center = (bb.min(axis=0)+bb.max(axis=0))*.5
                entrance = (center[0], 0.)
        elif role in {"timber", "timber_light"}:
            label, finish, edge_round = "Structural Timber", finishes["Timber"], .011
        elif role.startswith("plaster"):
            label, finish = "Lime Plaster", finishes["Plaster", plaster_finish]
        elif key.startswith("facade_flashing") or role in {"iron", "metal"}:
            label, finish, edge_round = "Forged Iron", finishes["Iron", iron_finish], .003
        elif key.startswith(("facade_steps", "facade_quoins", "facade_chimney_cap")):
            label, finish, edge_round = "Stone Only", finishes["Stone"], .022
        elif role.startswith("stone") or role == "mortar":
            label, finish = "Fieldstone", finishes["Masonry"]
        else:
            unseen.append((key, role))
            continue
        set_material(obj, finish)
        obj["showcase_material"] = finish.name
        classifications[label] += 1
        if obj.data.uv_layers.get("UV0_Metric") and label != "Stone Only":
            phase_uv(obj, phase.uniform((0, 0), (2.7, 1.8)))
        if edge_round:
            bevel(obj, edge_round)
    if unseen or entrance is None:
        raise RuntimeError(f"{name} binding or entrance unresolved: {unseen}")
    x0, y0, x1, y1, ridge = plan.rects[0]
    mid_x, mid_y = (x0+x1)*.5, (y0+y1)*.5
    roof_center = transform @ Vector((mid_x, mid_y, plan.eave-.12))
    rects = tuple((a-mid_x,b-mid_y,c-mid_x,d-mid_y,direction) for a,b,c,d,direction in plan.rects)
    roof = build_roof_collection(scene, Bearing(tuple(roof_center), x1-x0, y1-y0, angle, rects),
                                 rise=plan.slope*(y1-y0)/2, detail=detail, material_directory=MEDIA,
                                 seed=settings.seed, overhang=settings.overhang)
    roof.name = f"{name} · Roof AutoComplete"
    compound.children.link(roof)
    scene.collection.children.unlink(roof)
    for obj in roof.objects:
        role = obj.get("caelm_material", "")
        if "RoofUV" in obj.data.uv_layers:
            roofs.append(obj)
            classifications["Brookoak field"] += 1
        elif obj.name.startswith("Gable infill"):
            obj.hide_render = True
            obj.hide_set(True)
        elif role in {"timber", "timber_light"} or obj.name.startswith("Overlapping ridge caps"):
            set_material(obj, finishes["Timber"])
            obj["showcase_material"] = finishes["Timber"].name
            classifications["Structural Timber"] += 1
        elif role in {"iron", "metal"}:
            set_material(obj, finishes["Iron", iron_finish])
            obj["showcase_material"] = finishes["Iron", iron_finish].name
            classifications["Forged Iron"] += 1
        else:
            obj["showcase_material"] = "Brookoak tone from Roof AutoComplete"
            classifications["Brookoak trim"] += 1
    glass_group = bpy.data.collections.new(f"{name} · Handcrafted glazing")
    compound.children.link(glass_group)
    classifications["Handcrafted Glass"] = face_glass(scene, body, plan, transform,
                                                       finishes["Glass", glass_finish], glass_group, draft)
    hulls = [np.asarray([tuple((transform @ Vector((x,y,0)))[:2]) for x,y in ((a,b),(c,b),(c,d),(a,d))])
             for a,b,c,d,_ in plan.rects]
    step = lambda y: np.asarray((transform @ Vector((entrance[0], y, 0.)))[:2])
    report = {"seed": settings.seed, "shape": settings.footprint, "body_hash": body["caelm_geometry_hash"],
              "modeled_shingles": roof["caelm_roof_shingles"], "roof_pitch": settings.pitch,
              "bindings": dict(classifications), "wall_condition": plaster_finish,
              "joinery_condition": oak_finish, "glass_finish": glass_finish}
    print(name, report, flush=True)
    return {"name":name, "collection":compound, "transform":transform, "plan":plan, "hulls":hulls, "z":z,
            "door":step(-.86), "approach":step(-2.05), "report":report,"post_feet":post_feet}


def walk_line(control):
    controls = np.asarray(control, dtype=float)
    padded = np.vstack((controls[0], controls, controls[-1]))
    points = []
    for p0, p1, p2, p3 in zip(padded, padded[1:], padded[2:], padded[3:]):
        steps = max(4, math.ceil(np.linalg.norm(p2-p1)/.26))
        t = (np.arange(steps)/steps)[:, None]
        points.append(.5*(2*p1+(p2-p0)*t+(2*p0-5*p1+4*p2-p3)*t*t+(3*p1-p0-3*p2+p3)*t*t*t))
    return np.vstack((*points, controls[-1]))


def walks(sites):
    farm, cottage, workshop = sites
    return [
        ("Main walk to farmhouse", .79, 1.20, walk_line(((4.2,-45),(2.2,-26),(1.1,-16),(.48,-8.6),(.20,-4.7),(.66,1.6),
                                                         farm["approach"],farm["door"]))),
        ("Cottage track", .59, .91, walk_line(((.32,-6.8),(-3.2,-5.1),(-6.5,-3.6),(-9.3,-2.6),
                                               cottage["approach"],cottage["door"]))),
        ("Workshop access", .81, 1.24, walk_line(((.44,-7.35),(4.7,-5.9),(8.4,-5.2),(10.5,-4.5),
                                                  workshop["approach"],workshop["door"]))),
    ]


def ground_height(x, y, sites):
    x,y = np.broadcast_arrays(x,y)
    z = base_height(x,y)
    xy = np.column_stack((x.ravel(),y.ravel()))
    for site in sites:
        distance = wall_fields(xy, site["hulls"], 2.45).reshape(x.shape)
        weight = 1-ramp(.30,2.27,distance)
        z = z*(1-weight)+(site["z"]+.018)*weight
    return z


def route_uv(xy, routes):
    # Ground tissue has continuous world metric UVs; only the approved path
    # mask reads the closest walk's arclength and signed shoulder coordinate.
    best = np.full(len(xy), np.inf)
    uv = np.column_stack((np.zeros(len(xy)),np.full(len(xy),5.)))
    for _,half_width,_,points in routes:
        start, end = points[:-1], points[1:]
        direction = end-start
        spans = np.linalg.norm(direction,axis=1)
        station = np.r_[0., np.cumsum(spans)]
        for i,(a,b) in enumerate(zip(start,end)):
            reach = 2.2*half_width
            box = np.all((xy>=np.minimum(a,b)-reach)&(xy<=np.maximum(a,b)+reach),axis=1)
            ids = np.flatnonzero(box)
            if not len(ids):
                continue
            delta = xy[ids]-a
            fraction = np.clip(delta@direction[i]/spans[i]**2,0,1)
            off = delta-fraction[:,None]*direction[i]
            signed = np.sign(direction[i,0]*off[:,1]-direction[i,1]*off[:,0])
            dist = np.linalg.norm(off,axis=1)
            ratio = dist/half_width
            take = ratio < best[ids]
            target = ids[take]
            best[target] = ratio[take]
            uv[target,0] = station[i]+fraction[take]*spans[i]
            uv[target,1] = signed[take]*ratio[take]*.85
    return uv


def route_material():
    mat = ground_material("Transition")
    nodes,links = mat.node_tree.nodes,mat.node_tree.links
    mask = next(node for node in nodes if node.type == "TEX_IMAGE" and node.label == "path blend")
    coords = mask.inputs["Vector"].links[0].from_node
    center = coords.inputs["Y"].links[0].from_node
    across = center.inputs[0].links[0].from_node
    raw = across.inputs[0].links[0].from_node
    path = nodes.new("ShaderNodeUVMap")
    path.label = "Local coordinate along the authored walks"
    path.uv_map = "PathUV_Metric"
    path.location = (-1290,-230)
    phase = nodes.new("ShaderNodeMath")
    phase.operation = "DIVIDE"
    phase.inputs[1].default_value = LENGTH
    phase.location = (-780,-80)
    links.new(path.outputs["UV"],raw.inputs[0])
    links.new(raw.outputs["X"],phase.inputs[0])
    links.new(phase.outputs[0],coords.inputs["X"])
    mat["showcase_binding"] = "Approved Blend and Surface maps. PathUV drives mask. UV0 drives continuous material scale."
    return mat


def terrain_patch(name, x, y, sites, routes, mat, target):
    xx, yy = np.meshgrid(x,y)
    z = ground_height(xx,yy,sites)
    xy = np.column_stack((xx.ravel(), yy.ravel()))
    faces = grid_faces(len(x),len(y))
    obj = mesh_with_uv(name, np.column_stack((xy,z.ravel())), faces, xy, mat)
    layer = obj.data.uv_layers.new(name="PathUV_Metric")
    uv = route_uv(xy,routes)
    layer.data.foreach_set("uv",uv[faces.ravel()].astype(np.float32).ravel())
    obj.data.uv_layers.active = obj.data.uv_layers[UV]
    obj.data.uv_layers[UV].active_render = True
    all_hulls = [p for site in sites for p in site["hulls"]]
    soil = Soil(81379,.82,.91,.56,.60,.77,.80)
    _, native_verge = soil.shoulder(uv[:,0],uv[:,1])
    shelter = profile(xx/12, yy/12, 5, 5, 5119, periodic=False)
    grazed = .41*np.exp(-(xx/6.8)**2-((yy+.5)/4.55)**2)
    close = wall_fields(xy,all_hulls,2.1).reshape(z.shape)
    moist = .35+.25*shelter+.22*(1-ramp(.0,1.85,close))
    outer = np.exp(-((xx-1.)/29.)**2-((yy-3.)/29.)**2)
    values = {"cv_density": np.clip((.87+.31*shelter)*(1-grazed)*(.15+.85*outer),0,1),
              "cv_moisture":np.clip(moist,0,1),"cv_verge":native_verge}
    for key, data in values.items():
        field = obj.data.attributes.new(key,"FLOAT","POINT")
        field.data.foreach_set("value",np.asarray(data,dtype=np.float32).ravel())
    move_to(obj,target)
    return obj


def distant_landscape(scene):
    horizon = group(scene,"Ground · Distant pasture folds")
    x,y = np.meshgrid(np.linspace(-435.,435.,251),np.linspace(-435.,435.,251))
    radius,aspect = np.hypot(.94*x,y),np.arctan2(y,x)
    near_fold = 132.+18.*np.sin(3*aspect+.81)+9.*np.cos(5*aspect-.78)
    far_fold = 232.+37.*np.cos(2*aspect+.3)+15.*np.sin(5*aspect)
    first = np.exp(-((radius-near_fold)/28.)**2)*(17.8+5.*np.sin(4*aspect)+3.6*np.cos(7*aspect-.7))
    second = np.exp(-((radius-far_fold)/56.)**2)*(38.+9.*np.cos(4*aspect-1.)+5.*np.sin(8*aspect))
    outside = ramp(66.,114.,radius)
    creases = .43*np.sin(x*.123+y*.135)*np.cos(x*.082-y*.176)
    height = -3.8+outside*(first+second+creases)
    xy = np.column_stack((x.ravel(),y.ravel()))
    faces = grid_faces(x.shape[1],x.shape[0])
    mat = ground_material("Packed_Earth")
    soften_distant_repeat(mat)
    uv = np.column_stack(((x+3.0*np.sin(y*.071+x*.112)).ravel()*1.76,
                          (y+2.8*np.sin(x*.063-y*.115)).ravel()*1.68))
    land=mesh_with_uv("Far grazing landscape",np.column_stack((xy,height.ravel())),faces,uv,mat)
    move_to(land,horizon)


def soften_distant_repeat(material):
    """Converge subpixel terrain repeats toward the approved map's average."""
    nodes,links = material.node_tree.nodes,material.node_tree.links
    shader = nodes.get("Principled BSDF")
    source = shader.inputs["Base Color"].links[0].from_socket
    image = source.node.image
    samples = np.empty(len(image.pixels),dtype=np.float32)
    image.pixels.foreach_get(samples)
    srgb = samples.reshape(-1,4)[::41,:3]
    linear = np.where(srgb<=.04045,srgb/12.92,((srgb+.055)/1.055)**2.4)
    average = linear.mean(axis=0)
    blend = nodes.new("ShaderNodeMixRGB")
    blend.label = "Subpixel albedo · approved packed earth average"
    blend.inputs[0].default_value = .93
    blend.inputs[2].default_value = (*average,1.)
    links.new(source,blend.inputs[1])
    geometry = nodes.new("ShaderNodeNewGeometry")
    grain = nodes.new("ShaderNodeTexNoise")
    grain.label = "Broad pasture variation"
    grain.inputs["Scale"].default_value = .036
    grain.inputs["Detail"].default_value = 3.0
    links.new(geometry.outputs["Position"],grain.inputs["Vector"])
    values = nodes.new("ShaderNodeMapRange")
    values.inputs["To Min"].default_value = .62
    values.inputs["To Max"].default_value = 1.19
    links.new(grain.outputs["Fac"],values.inputs["Value"])
    color = nodes.new("ShaderNodeVectorMath")
    color.operation = "SCALE"
    links.new(blend.outputs["Color"],color.inputs[0])
    links.new(values.outputs["Result"],color.inputs["Scale"])
    links.new(color.outputs["Vector"],shader.inputs["Base Color"])
    normal = next(node for node in nodes if node.type == "NORMAL_MAP")
    normal.inputs["Strength"].default_value = .04


def site_inputs(scene, sites, routes, borders):
    guides = group(scene,"Inputs · Walk centerlines")
    for name,half_width,verge,points in routes:
        curve = bpy.data.curves.new(name,"CURVE")
        curve.dimensions = "3D"
        spline = curve.splines.new("POLY")
        spline.points.add(len(points)-1)
        locations = np.column_stack((points,ground_height(*points.T,sites),np.ones(len(points))))
        spline.points.foreach_set("co",locations.astype(np.float32).ravel())
        obj = bpy.data.objects.new(name,curve)
        guides.objects.link(obj)
        obj.hide_render = True
        obj["cv_path_half_width"],obj["cv_verge_width"] = half_width,verge
    structure = group(scene,"Inputs · Planting clearances")
    for site in sites:
        pad = site["door"]-site["approach"]
        across = np.array((-pad[1],pad[0]))/np.linalg.norm(pad)
        center = site["door"]+pad*.34
        d = across*(.97 if site["name"] == "Workshop" else .77)
        stair = np.stack((center-d-pad*.42,center+d-pad*.42,center+d+pad*.42,center-d+pad*.42))
        for i, polygon in enumerate((*site["hulls"],stair)):
            proxy_mesh(structure,f"{site['name']} clearance {i+1}",polygon)
    for i, (a,b,width) in enumerate(borders):
        vector = np.asarray(b)-a
        side = np.array((-vector[1],vector[0]))*.5*width/np.linalg.norm(vector)
        proxy_mesh(structure,f"Boundary wall clearance {i+1}",np.stack((a-side,b-side,b+side,a+side)))
    return guides,structure


def proxy_mesh(collection, name, polygon):
    polygon = np.asarray(polygon,dtype=float)
    axis = polygon[1]-polygon[0]
    angle = math.atan2(axis[1],axis[0])
    rotation = np.array(((math.cos(angle),-math.sin(angle)),(math.sin(angle),math.cos(angle))))
    center = polygon.mean(axis=0)
    local = (polygon-center) @ rotation
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([(x,y,0) for x,y in local],[],[tuple(range(len(local)))])
    obj = bpy.data.objects.new(name,mesh)
    collection.objects.link(obj)
    obj.location = (*center,0.)
    obj.rotation_euler.z = angle
    obj.hide_render = True
    obj.display_type = "WIRE"


def custom_mesh(name, vertices, faces, mats, collection, loop_uv=None):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices,[],faces)
    mesh.update()
    for mat in mats:
        mesh.materials.append(mat)
    if loop_uv is not None:
        uv = mesh.uv_layers.new(name="UV0_Metric")
        uv.data.foreach_set("uv",np.asarray(loop_uv,np.float32).ravel())
    obj = bpy.data.objects.new(name,mesh)
    collection.objects.link(obj)
    return obj


def stock(name, origin, length, width, height, angle, material, collection, seed, trim=.009):
    rng = np.random.default_rng(seed)
    off = rng.uniform(0,2.4,2)
    vertices = [(i*length,j*width*.5,k*height*.5) for i in (0,1) for j in (-1,1) for k in (-1,1)]
    faces = [(0,2,6,4),(1,5,7,3),(0,4,5,1),(2,3,7,6),(0,1,3,2),(4,6,7,5)]
    uv = [(vertices[idx][0]+off[0],(vertices[idx][1] if i<2 else vertices[idx][2])+off[1])
          if i<4 else (vertices[idx][1]+off[0],vertices[idx][2]+off[1])
          for i, face in enumerate(faces) for idx in face]
    obj = custom_mesh(name,vertices,faces,[material],collection,uv)
    obj.location = origin
    obj.rotation_euler.z = angle
    if trim:
        bevel(obj,trim)
    return obj


def billet(name, origin, length, radius, angle, tilt, timber, crosscut, collection, rng):
    sides = 11
    radial = np.linspace(0,math.tau,sides,endpoint=False)
    stretch = rng.uniform(.85,1.15,sides)
    vertices = [(x,radius*scale*s*math.cos(a)+x*.028,radius*scale*s*math.sin(a))
                for x,scale in ((0,1.),(length,.88)) for a,s in zip(radial,stretch)]
    sides_faces = [(i,(i+1)%sides,(i+1)%sides+sides,i+sides) for i in range(sides)]
    faces = sides_faces+[tuple(reversed(range(sides))),tuple(range(sides,2*sides))]
    phase = rng.uniform(0,1.1,2)
    uv = []
    for i,face in enumerate(faces):
        for j,index in enumerate(face):
            x,y,z = vertices[index]
            uv.append((x+phase[0],.04+radius*(radial[i]+(math.tau/sides if j in (1,2) else 0))) if i<sides
                      else (y+.26,z+.25))
    obj = custom_mesh(name,vertices,faces,[timber,crosscut],collection,uv)
    for poly in obj.data.polygons[-2:]:
        poly.material_index = 1
    obj.location = origin
    obj.rotation_euler = (0,tilt,angle)
    bevel(obj,.007)
    return obj


def rubble(name, xy, z, bounds, angle, mat, collection, rng):
    length,depth,height = bounds
    contour = np.array([(-.50,-.25),(-.30,-.50),(.30,-.50),(.50,-.27),
                        (.50,.29),(.31,.50),(-.28,.50),(-.49,.26)])
    contour += rng.uniform(-.075,.075,contour.shape)
    rings=[]
    for scale, level in ((.79,0), (1,.22), (.90,.81), (.71,1.)):
        skew = rng.uniform(-.070,.070,2)
        rings.extend((x*length,y*depth,height*(level+rng.uniform(-.09,.09))) for x,y in contour*scale+skew)
    n=len(contour)
    faces=[tuple(range(n-1,-1,-1))]
    for row in range(3):
        for i in range(n):
            a,b=row*n+i,row*n+(i+1)%n
            faces.append((a,b,b+n,a+n))
    faces.append(tuple(range(3*n,4*n)))
    obj = custom_mesh(name,rings,faces,[mat],collection)
    obj.location = (*xy,z)
    obj.rotation_euler.z = angle
    bevel(obj,.016 if height>.15 else .008)
    return obj


def dressing(scene, sites, finishes):
    rubble_group = group(scene,"Dressing · Stone boundaries and landings")
    wood_group = group(scene,"Dressing · Split fuel, stock and workbench")
    rng = np.random.default_rng(59217)
    borders = [((-16.8,-7.7),(-9.5,-9.8),.65),((-26.,3.4),(-18.,1.35),.62),
               ((9.0,-13.9),(18.6,-10.8),.66),((19.7,-6.9),(23.6,-.55),.67),
               ((-13.0,14.4),(-5.6,17.0),.61),((12.2,14.1),(23.0,15.2),.69)]
    for number,(start,end,width) in enumerate(borders):
        a,b=np.array(start),np.array(end)
        segment=b-a
        length = np.linalg.norm(segment)
        side=segment/length
        angle=math.atan2(side[1],side[0])
        normal=np.array((-side[1],side[0]))
        for course in range(3):
            u=rng.uniform(-.16,.19)+course*.10
            while u<length-.26:
                span=min(length-u,rng.uniform(.34,.79))
                mid=a+side*(u+span*.5)+normal*rng.uniform(-.048,.048)
                base=float(ground_height(*mid,sites))
                if course<2 or rng.random()>.06:
                    rubble(f"Wall {number+1} · rubble {course+1}",mid,base-.108+course*.21+rng.uniform(-.035,.035),
                           (span+.018,width*(1-course*.12)*rng.uniform(.86,1.14),rng.uniform(.205,.289)),
                           angle+rng.uniform(-.13,.13),finishes["Stone"],rubble_group,rng)
                u+=span*rng.uniform(.93,1.01)
    for site in sites:
        out = site["approach"]-site["door"]
        axis = out/np.linalg.norm(out)
        side=np.array((-axis[1],axis[0]))
        angle=math.atan2(side[1],side[0])
        for i in range(3):
            for j in range(2 if site["name"]!="Workshop" else 3):
                mid=site["door"]+axis*(.24+i*.38)+side*(j-(.5 if site["name"]!="Workshop" else 1))*.45
                base=float(ground_height(*mid,sites))
                rubble(f"{site['name']} threshold flag",mid,base-.056,(rng.uniform(.36,.52),rng.uniform(.28,.43),.09),
                       angle+rng.uniform(-.15,.15),finishes["Stone"],rubble_group,rng)
        for i, foot in enumerate(site["post_feet"]):
            base=float(ground_height(*foot[:2],sites))-.026
            if foot.z>base+.09:
                rubble(f"{site['name']} · seated porch pier {i+1}",foot[:2],base,
                       (.257,.254,foot.z-base+.033),site["transform"].to_euler().z,finishes["Stone"],rubble_group,rng)

    timber, oak = finishes["Timber"], finishes["Oak","Weathered"]
    for site in sites:
        transform = site["transform"]
        angle = transform.to_euler().z
        height = site["z"]
        crosscut = finishes["Crosscut","Crosscut"]
        if site["name"] == "Cottage":
            # The render exposed open slots above the native exterior fascia.
            # Tuck a backing board into the eaves below the deck in this scene.
            plan = site["plan"]
            w,d = plan.settings.width,plan.settings.depth
            o = plan.settings.overhang
            z = plan.eave-plan.slope*o-.131
            for j,y in enumerate((-o+.045,d+o-.045)):
                start = transform @ Vector((-.20,y,z))
                stock("Cottage · fitted eave backing",start,w+.40,.092,.171,angle,timber,wood_group,391+j)
        if site["name"] == "Workshop":
            bench_xy = transform @ Vector((7.2,-.90,0.))
            height = float(ground_height(*bench_xy[:2],sites))
            for s in range(3):
                p = transform @ Vector((7.0,-.71-s*.16,.80))
                stock("Workshop bench · planed top",(*p[:2],height+.81),2.15,.157,.076,angle,oak,wood_group,99+s)
            for x in (7.13,8.92):
                for y in (-.79,-1.04):
                    p = transform @ Vector((x,y,.37))
                    obj = stock("Bench trestle leg",(*p[:2],height+.014),.79,.104,.135,angle,timber,wood_group,
                                712+round(x*20+y*50))
                    obj.rotation_euler.y = -math.pi/2
            p=transform @ Vector((7.18,-.93,.25))
            stock("Bench longitudinal stretcher",(*p[:2],height+.26),1.92,.092,.116,angle,timber,wood_group,711)
            for j in range(9):
                p=transform @ Vector((7.4+rng.uniform(-.15,.15),-1.85+(j%3)*.19,0))
                z = float(ground_height(*p[:2],sites))+.074+(j//3)*.074
                stock("Workshop seasoning stock",(*p[:2],z),rng.uniform(1.65,2.42),.17,.061,
                      angle+rng.uniform(-.035,.037),oak,wood_group,908+j)
        else:
            lx,ly = (9.25,-.38) if site["name"]=="Farmhouse" else (5.38,-.63)
            for j in range(21 if site["name"]=="Farmhouse" else 14):
                p=transform @ Vector((lx+(j%7)*.17,ly+rng.uniform(-.045,.052),0.))
                base=float(ground_height(*p[:2],sites))
                z=base+.075+(j//7)*.135
                billet("Sheltered firewood",(*p[:2],z),rng.uniform(.29,.48),rng.uniform(.062,.105),
                       angle+math.pi/2+rng.uniform(-.11,.11),rng.uniform(-.08,.07),timber,crosscut,wood_group,rng)
    return borders


def scrub_boundaries(scene, sites, kit, timber):
    """Assemble distant scrub from the approved leaflet cards and woody shoots."""
    output = group(scene,"Dressing · Pasture scrub and hedgerows")
    leaf = next(obj for obj in kit.objects if obj.name == "LM_Low_Weeds_Established_LOD1").data
    source = np.array([tuple(v.co) for v in leaf.vertices])
    uv = [tuple(item.uv) for item in leaf.uv_layers.active.data]
    polygons = [tuple(f.vertices) for f in leaf.polygons]
    rng = np.random.default_rng(98164)
    templates=[]
    for template in range(6):
        host = bpy.data.collections.new(f"Scrub cluster source {template+1}")
        verts,faces,loops=[],[],[]
        for branch in range(8):
            azimuth = branch*2.399+rng.uniform(-.34,.32)
            heading = np.array((math.cos(azimuth),math.sin(azimuth)))
            length = rng.uniform(.30,.83)
            anchor=np.array((*(heading*length),rng.uniform(.50,1.29)))
            fork=np.array((*(heading*length*.26),anchor[2]*.58))
            dead=anchor+np.array((*(heading*.07),.24))
            for j,(a,b) in enumerate(((np.array((0.,0.,-.03)),fork),(fork,dead))):
                delta=b-a
                stalk=stock("Scrub woody shoot",a,float(np.linalg.norm(delta)),.033-j*.014,.029-j*.013,
                            math.atan2(delta[1],delta[0]),timber,host,1100+branch+j+template*39,trim=0)
                stalk.rotation_euler.y=-math.atan2(delta[2],math.hypot(*delta[:2]))
            crown = np.array((rng.uniform(.33,.51),rng.uniform(.31,.52),rng.uniform(.33,.51)))
            for _ in range(96):
                sample = rng.normal(0,1,3)
                sample *= rng.random()**.36/np.linalg.norm(sample)
                p = anchor+sample*crown
                spin = Matrix.Rotation(rng.uniform(0,math.tau),3,"Z") @ Matrix.Rotation(rng.uniform(-1.2,1.2),3,"X")
                points = source @ np.asarray(spin).T*rng.uniform(.74,1.37)+p
                first = len(verts)
                verts.extend(points.tolist())
                loops.extend(uv)
                faces.extend(tuple(first+i for i in face) for face in polygons)
        custom_mesh("Layered Lowmark broadleaf cutouts",verts,faces,[leaf.materials[0]],host,loops)
        templates.append(host)
    lines = (
        ((-29.0,10.8),(-17.3,12.6),10),
        ((-14.4,16.7),(-7.7,19.3),6),
        ((-3.2,19.3),(12.8,21.3),11),
        ((20.4,12.3),(30.3,17.4),8),
        ((-20.6,27.1),(-8.9,30.2),7),
        ((15.3,31.5),(22.1,28.4),6),
    )
    count=0
    for a,b,num in lines:
        for t in np.linspace(0,1,num):
            xy=np.asarray(a)+(np.asarray(b)-a)*t+rng.uniform(-.63,.63,2)
            obj=bpy.data.objects.new("Irregular scrub mass",None)
            output.objects.link(obj)
            obj.instance_type="COLLECTION"
            obj.instance_collection=templates[count%len(templates)]
            obj.location=(*xy,float(ground_height(*xy,sites)))
            scale=rng.uniform(.83,1.63)
            obj.scale=(scale*rng.uniform(.80,1.19),scale,scale*rng.uniform(.85,1.10))
            obj.rotation_euler.z=rng.uniform(0,math.tau)
            count+=1
    return count


def camera(scene, label, position, target, focal, fstop=0):
    lens = bpy.data.cameras.new(label)
    lens.lens = focal
    lens.clip_end = 520.
    lens.dof.use_dof = bool(fstop)
    if fstop:
        lens.dof.focus_distance = math.dist(position,target)
        lens.dof.aperture_fstop = fstop
    obj = bpy.data.objects.new(label,lens)
    scene.collection.objects.link(obj)
    obj.location=position
    point(obj,target)
    return obj


def daylight(scene):
    # The sky and key share a sun direction. The atmospheric sky provides
    # scattered fill while the small angular disk casts actual shadows.
    azimuth = math.radians(-123.)
    elevation = math.radians(34.)
    incoming = (math.cos(azimuth)*math.cos(elevation),math.sin(azimuth)*math.cos(elevation),math.sin(elevation))
    world = bpy.data.worlds.new("Lowmark clear late-morning sky")
    world.use_nodes = True
    nodes = world.node_tree.nodes
    sky = nodes.new("ShaderNodeTexSky")
    sky.sky_type = "MULTIPLE_SCATTERING"
    sky.sun_disc = False
    sky.sun_elevation = elevation
    sky.sun_rotation = azimuth % math.tau
    sky.altitude = .14
    sky.air_density = 1.12
    sky.aerosol_density = .73
    sky.ozone_density = 1.
    tint = nodes.new("ShaderNodeHueSaturation")
    tint.inputs["Saturation"].default_value = .53
    nodes["Background"].inputs["Strength"].default_value = .19
    world.node_tree.links.new(sky.outputs["Color"],tint.inputs["Color"])
    world.node_tree.links.new(tint.outputs["Color"],nodes["Background"].inputs["Color"])
    scene.world = world
    lamp = bpy.data.lights.new("Sun through light atmospheric haze", "SUN")
    lamp.energy = 2.62
    lamp.angle = math.radians(2.9)
    lamp.color = (1.,.922,.82)
    sun = bpy.data.objects.new(lamp.name,lamp)
    scene.collection.objects.link(sun)
    sun.location = Vector(incoming)*35
    point(sun,(0,0,0))


def render_config(scene, opts):
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 28 if opts.draft else 112
    scene.cycles.use_denoising = True
    scene.cycles.adaptive_threshold = .015 if opts.draft else .009
    scene.cycles.max_bounces = 10
    scene.cycles.transmission_bounces = 8
    if opts.optix:
        prefs=bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type="OPTIX"
        prefs.refresh_devices()
        if not any(device.type=="OPTIX" for device in prefs.devices):
            raise RuntimeError("No OptiX device is available")
        for device in prefs.devices:
            device.use = device.type=="OPTIX"
        scene.cycles.device="GPU"
    else:
        scene.cycles.device="CPU"
    scene.view_settings.view_transform="AgX"
    scene.view_settings.look="AgX - Medium High Contrast"
    scene.view_settings.exposure=-.30
    scene.render.image_settings.file_format="PNG"
    scene.render.image_settings.color_mode="RGB"
    scene.render.resolution_percentage = 38 if opts.draft else 100


SHOTS = {
    "Settlement": ((8.0,-35.4,6.80),(.38,6.45,2.7),29.0,(3000,1710)),
    "Farmhouse": ((3.80,-6.25,4.90),(-.95,8.30,3.70),36.,(2520,1720)),
    "Cottage": ((-3.01,-5.48,3.6),(-12.46,2.65,2.20),39.,(2520,1720)),
    "Workshop": ((1.0,-9.7,3.80),(12.2,2.8,2.25),37.,(2520,1720)),
    "Materials": ((-10.04,-3.88,2.02),(-12.67,.60,1.34),46.,(2350,1530)),
}


def frame_whole_buildings(scene, sites):
    bounds = {}
    for site in sites:
        parts = []
        for obj in site["collection"].all_objects:
            if obj.type == "MESH" and not obj.hide_render:
                coords = np.empty(3*len(obj.data.vertices),dtype=np.float32)
                obj.data.vertices.foreach_get("co",coords)
                parts.append(vegetation.world_points(coords.reshape(-1,3),obj.matrix_world))
        bounds[site["name"]] = np.concatenate(parts)
    measurements = {}
    for name in ("Settlement", "Farmhouse", "Cottage", "Workshop"):
        scene.render.resolution_x,scene.render.resolution_y=SHOTS[name][3]
        cam = bpy.data.objects[name]
        world_points = np.concatenate(tuple(bounds.values())) if name == "Settlement" else bounds[name]
        loc = vegetation.world_points(world_points,cam.matrix_world.inverted())
        if np.any(loc[:,2]>=0):
            raise RuntimeError(f"{name} contains architecture behind its camera")
        projected = -loc[:,:2]/loc[:,2,None]
        extrema = np.r_[projected.argmin(axis=0),projected.argmax(axis=0)]
        points = [Vector(world_points[index]) for index in extrema]
        screen = np.asarray([tuple(world_to_camera_view(scene,cam,point)) for point in points])
        wanted = np.abs(screen[:,:2]-.5).max()
        if wanted>.473:
            cam.data.lens *= .471/wanted
            screen = np.asarray([tuple(world_to_camera_view(scene,cam,point)) for point in points])
        measurements[name] = {"minimum_xy":screen[:,:2].min(axis=0).tolist(),
                              "maximum_xy":screen[:,:2].max(axis=0).tolist(),"lens_mm":cam.data.lens}
    return measurements


def plant_site(scene, terrain, guide_group, clearances, kit):
    mix = dict(FAMILY_WEIGHTS)
    mix.update({"Short_Sward":1.30, "Mixed_Verge":.85, "Meadow_Seed":.31, "Wayside_Yarrow":.028,
                "Selfheal":.041, "Dry_Stems":.36, "Stubble":1.48})
    settings = ScatterSettings(seed=53721,density=130, filler=.93, density_boost=.95, clustering=.954,
                               patch_size=3.72, moisture=.63, scale=(.84,1.35), height=1.12,
                               lod_origin=(.6,-8.,2.0), lod_distances=(14.,34.),tile_size=6.2,
                               max_samples=1460000, max_instances=242000,max_triangles=5600000)
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    layer, placed = vegetation.generate(scene,depsgraph,[terrain],kit,settings,layer="Settlement verges and pasture",
                                        path_collection=guide_group,structures=clearances,weights=mix)
    guides = vegetation.guides_for(guide_group,scene,depsgraph,.75,1.10)
    tread,_ = guide_fields(placed.xyz[:,:2],guides,1.)
    if len(kit.objects)!=93 or not len(placed.xyz) or np.any(tread < 0):
        raise RuntimeError("Vegetation does not meet the approved library or tread contract")
    data = {"instances":len(placed.xyz),"triangles":int(placed.cost.sum()),"batches":len(layer.objects),
            "lod_counts":list(layer["lod_counts"]),"placement_sha256":placed.signature,
            "path_centers_occupied":int(np.count_nonzero(tread<0))}
    print("Vegetation",data,flush=True)
    return data


def check_scene(scene, sites, scatter_stats):
    tag_prefixes = ("Lowmark", "Approved Lowmark", "Brookoak")
    bad = []
    for obj in scene.objects:
        if obj.type != "MESH" or obj.hide_render or obj.get(vegetation.BATCH):
            continue
        for material in obj.data.materials:
            if material is None or not material.name.startswith(tag_prefixes):
                bad.append((obj.name, material.name if material else None))
        if not obj.data.materials:
            bad.append((obj.name,None))
    if bad:
        raise RuntimeError(f"Unbound visible surfaces {bad[:12]}")
    linked_files = set()
    for image in bpy.data.images:
        if image.source == "FILE" and image.users and not image.packed_file:
            file = Path(bpy.path.abspath(image.filepath,library=image.library))
            if not file.is_file():
                raise RuntimeError(f"Missing referenced image {image.name}: {file}")
            linked_files.add(file.name)
    return {"buildings": {site["name"]:site["report"] for site in sites},"vegetation":scatter_stats,
            "visible_meshes":sum(obj.type=="MESH" and not obj.hide_render for obj in scene.objects),
            "bound_external_images":sorted(linked_files)}


def build_scene(opts):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = "Lowmark · Rural settlement"
    scene.unit_settings.system = "METRIC"
    finishes = approved_finishes()
    roofs = []
    sites = [building(scene,name,spec,finishes,roofs,opts.draft) for name,spec in STUDIES.items()]
    riven = bind_riven(roofs[0].data.materials[0])
    for obj in roofs:
        set_material(obj,riven)
        obj["showcase_material"] = riven.name
    routes = walks(sites)
    borders = dressing(scene,sites,finishes)
    guide_group, clearances = site_inputs(scene,sites,routes,borders)
    landscape = group(scene,"Ground · Packed earth and worn paths")
    x = np.unique(np.round(np.r_[np.linspace(-60,-24,56),np.linspace(-24,25,326),np.linspace(25,64,61)],5))
    y = np.unique(np.round(np.r_[np.linspace(-46,-20,46),np.linspace(-20,22,281),np.linspace(22,73,100)],5))
    ground = terrain_patch("Lowmark surveyed ground",x,y,sites,routes,route_material(),landscape)
    distant_landscape(scene)
    print("Terrain walk mesh",len(ground.data.vertices),"vertices",flush=True)
    kit=vegetation.load_catalog(str(MEDIA/vegetation.LIBRARY_FILE))
    shrub_count=scrub_boundaries(scene,sites,kit,finishes["Timber"])
    daylight(scene)
    for name,(position,target,focal,_) in SHOTS.items():
        camera(scene,name,position,target,focal,7.1 if name=="Materials" else 0)
    scene.camera = bpy.data.objects["Settlement"]
    bpy.context.view_layer.update()
    framing=frame_whole_buildings(scene,sites)
    stats = plant_site(scene,ground,guide_group,clearances,kit)
    # Orphan generator materials are unused after scene bindings. Remove them
    # before the file audit so dormant placeholder maps do not ship as dependencies.
    bpy.data.orphans_purge(do_recursive=True,do_linked_ids=False)
    result = check_scene(scene,sites,stats)
    result["scrub_boundary_instances"]=shrub_count
    result["camera_framing"]=framing
    scene["showcase_verification"] = json.dumps(result,sort_keys=True)
    return scene,result


def main():
    parser = ArgumentParser()
    parser.add_argument("--draft",action="store_true")
    parser.add_argument("--optix",action="store_true")
    parser.add_argument("--from-scene",type=Path)
    parser.add_argument("--shots",nargs="+",choices=tuple(SHOTS),default=list(SHOTS))
    opts = parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    prefix = ".draft_" if opts.draft else "Lowmark_"
    if opts.from_scene:
        bpy.ops.wm.open_mainfile(filepath=str(opts.from_scene.resolve()))
        scene = bpy.context.scene
        result = json.loads(scene["showcase_verification"])
    else:
        scene,result = build_scene(opts)
    render_config(scene,opts)
    scene.camera = bpy.data.objects["Settlement"]
    scene.render.resolution_x,scene.render.resolution_y=SHOTS["Settlement"][3]
    scene.render.filepath = "//"+prefix+"Settlement.png"
    if not opts.from_scene:
        bpy.context.preferences.filepaths.save_version = 0
        bpy.ops.wm.save_as_mainfile(filepath=str(HERE/f"{prefix}Settlement.blend"),compress=True,relative_remap=True)
    if not opts.draft:
        (HERE/"verification.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    for name in opts.shots:
        scene.camera = bpy.data.objects[name]
        scene.render.resolution_x,scene.render.resolution_y=SHOTS[name][3]
        scene.render.filepath = str(HERE/f"{prefix}{name}.png")
        bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
