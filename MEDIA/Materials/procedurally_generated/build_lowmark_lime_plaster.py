"""Build and bake Lowmark lime plaster and whitewash with Blender 5.0.1.

The reusable tile is entirely plaster. Wall panels, framing and splash zones
are architectural context rather than outlines embedded in the texture.
"""
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
import math
import sys

import bpy
from mathutils import Vector
import numpy as np

ROOT = Path(__file__).resolve().parent
STEM = "Lowmark_Lime_Plaster_Whitewash"
sys.path.insert(0,str(ROOT))
from build_lowmark_structural_timber import (
    around, bake, bake_source, blend, mapped_material,
    pixels, plain, point, profile, ramp, source_material, surface_mesh,
)

TILE = 2.4
BOUNDS = (TILE,TILE)
RELIEF = .016
SEED = 82731
VARIANTS = ("Maintained","Aged")


@dataclass(frozen=True)
class Coat:
    height: np.ndarray
    color: np.ndarray
    roughness: np.ndarray


@dataclass(frozen=True)
class FloatPass:
    u: float
    v: float
    angle: float
    length: float
    width: float
    lift: float
    curve: float


@dataclass(frozen=True)
class WeakSpot:
    u: float
    v: float
    width: float
    height: float
    angle: float
    depth: float
    threshold: float


class Plaster:
    def __init__(self,seed,weathering,trowel):
        self.seed = seed
        self.weathering = weathering
        self.trowel = trowel
        rng = np.random.default_rng(seed)
        self.float_passes = []
        # Strokes overlap in local groups with turns of the float. Their
        # different centres and arcs prevent a grid of repeated semicircles.
        for x,y,angle in ((.23,.33,.37),(.52,1.23,-.55),(.30,1.91,.15),
                          (1.02,.72,.71),(1.27,1.72,-.27),(1.92,.43,.98),
                          (1.98,1.06,.31),(2.08,2.05,-.63),(.08,2.30,.22)):
            for step in range(3):
                self.float_passes.append(FloatPass(
                    x+.048*step+rng.uniform(-.058,.058),
                    y+.034*step+rng.uniform(-.086,.086),
                    angle+rng.uniform(-.46,.46),rng.uniform(.14,.28),
                    rng.uniform(.070,.129),rng.uniform(.00048,.00129),
                    rng.uniform(.35,.81)))
        self.spots = tuple(WeakSpot(x+rng.uniform(-.035,.035),y+rng.uniform(-.033,.033),
                                    width,height,angle,depth,threshold)
                           for x,y,width,height,angle,depth,threshold in (
            (.68,.65,.144,.093,-.55,.0035,.34),
            (.81,.716,.068,.035,.30,.0025,.45),
            (1.93,1.21,.103,.071,.32,.0030,.38),
            (1.845,1.284,.043,.037,-.30,.0021,.46),
            (1.34,.19,.076,.048,-.17,.0027,.43),
            (.33,1.79,.057,.105,.27,.0021,.48),
            (2.33,2.09,.076,.046,.43,.0024,.44),
        ))
        # Settling and drying traces. Branches begin on a parent path or
        # run out from the shoulder of a weak spot.
        self.fissures = (
            ((.68,.65),[(-.22,-.057),(-.154,-.054),(-.087,-.027),(-.047,-.033),
                         (.015,-.079),(.087,-.125),(.147,-.14)],.0025,.0010,.31),
            ((.68,.65),[(-.087,-.027),(-.092,.054),(-.124,.098),(-.130,.152)],.0017,.0008,.36),
            ((.68,.65),[(.015,-.079),(.003,-.133),(.038,-.197)],.0014,.00065,.45),
            ((1.93,1.21),[(-.13,.194),(-.116,.135),(-.066,.073),(-.05,.006),
                            (.015,-.055),(.055,-.118),(.085,-.136)],.0022,.00086,.40),
            ((1.93,1.21),[(-.066,.073),(-.118,.052),(-.161,.089),(-.220,.090)],.0015,.00064,.45),
            ((1.34,.19),[(-.18,.05),(-.095,.029),(-.027,.01),(.064,.023),(.14,.058)],.0016,.0008,.44),
            ((.33,1.79),[(-.11,-.17),(-.086,-.093),(-.036,-.053),
                           (-.01,.016),(.058,.064),(.076,.152)],.0016,.0008,.44),
            ((2.33,2.09),[(-.16,-.06),(-.091,-.05),(-.029,-.018),(.040,-.049),(.143,-.025)],
                          .0018,.00077,.46),
        )

    def float_marks(self,x,y,bend):
        relief = np.zeros_like(x)
        polished = np.zeros_like(x)
        for stroke in self.float_passes:
            dx,dy = around(x,stroke.u,TILE),around(y,stroke.v,TILE)
            c,s = math.cos(stroke.angle),math.sin(stroke.angle)
            along = (c*dx+s*dy)/stroke.length
            cross = (-s*dx+c*dy)/stroke.width
            # Curved nose of the blade, feathered sides and low toe where
            # the worker completed the stroke.
            tip = along+stroke.curve*cross*cross+bend
            body = ramp(-.95,-.53,tip)*(1-ramp(.20,.73,tip))
            side = 1-ramp(.43,1.01,np.abs(cross))
            lip = ramp(.03,.105,tip)*(1-ramp(.105,.24,tip))
            ridge = ramp(.27,.315,tip)*(1-ramp(.315,.39,tip))
            relief += stroke.lift*(.58*body+.64*lip+.21*ridge)*side
            polished = np.maximum(polished,.90*body*side)
        return relief*self.trowel,polished*self.trowel

    def wear(self,x,y,age,ragged,granular):
        exposure = np.zeros_like(x)
        spall = np.zeros_like(x)
        depth = np.zeros_like(x)
        crack = np.zeros_like(x)
        crack_depth = np.zeros_like(x)
        for spot in self.spots:
            dx,dy = around(x,spot.u,TILE),around(y,spot.v,TILE)
            c,s = math.cos(spot.angle),math.sin(spot.angle)
            a = (dx*c+dy*s)/spot.width
            b = (-dx*s+dy*c)/spot.height
            distance = np.sqrt(a*a+b*b)
            exposure = np.maximum(exposure,(1-ramp(.68,2.72,distance))*
                                  ramp(.1,.73,age))
            activation = ramp(spot.threshold,spot.threshold+.27,age)
            border = distance+.55*(ragged-.49)+.14*(granular-.47)
            lost = 1-ramp(.80,.935,border+.76*(1-activation))
            lost *= activation
            spall = np.maximum(spall,lost)
            depth = np.maximum(depth,lost*spot.depth)
        for (cx,cy),vertices,width,drop,start in self.fissures:
            activity = ramp(start-.13,start+.27,age)
            if activity == 0:
                continue
            dx,dy = around(x,cx,TILE),around(y,cy,TILE)
            z = np.zeros_like(x)
            for i,((ax,ay),(bx,by)) in enumerate(zip(vertices,vertices[1:])):
                abx,aby = bx-ax,by-ay
                h = np.clip(((dx-ax)*abx+(dy-ay)*aby)/(abx*abx+aby*aby),0,1)
                gap = np.hypot(dx-ax-h*abx,dy-ay-h*aby)
                t = (i+h)/(len(vertices)-1)
                taper = .39+.61*ramp(0,.19,t)*(1-ramp(.79,1,t))
                local_width = 1.24*width*taper*(.59+.81*ragged)
                z = np.maximum(z,(1-ramp(.12,1.22,gap/local_width))*taper)
            crack = np.maximum(crack,z*activity)
            crack_depth = np.maximum(crack_depth,z*activity*drop)
        return exposure,spall,depth,crack,crack_depth

    def sample(self,x,y,condition):
        u,v = x/TILE,y/TILE
        seed = self.seed
        shade = profile(u,v,6,5,seed+1)
        warp = profile(u,v,13,14,seed+2)
        work,polished = self.float_marks(x,y,.19*(warp-.5))
        open_pores = ramp(.53,.84,profile(u,v,312,279,seed+3))
        freckles = ramp(.69,.93,profile(u,v,492,513,seed+4))
        grains = profile(u,v,184,194,seed+5)
        grit = profile(u,v,345,327,seed+6)
        ragged = profile(u,v,51,67,seed+7)
        exposure,spall,lost,trace,fissure = self.wear(x,y,condition,ragged,grit)
        # Large forms are millimetre-scale float compaction and slight
        # waviness in the backing. Fine pores increase where the finish coat
        # eroded. The same loss and moisture fields drive the other channels.
        depth = .0083+.0028*(shade-.5)+.00073*(warp-.5)+work
        depth += .00027*(grains-.5)+.00017*(grit-.5)
        depth -= .00025*open_pores+.00021*freckles+lost+1.15*fissure
        depth += spall*(.00062*(grit-.5)-.00066*open_pores)
        brush = profile(u+.005*(warp-.5),v,28,8,seed+13)
        cloud = profile(u,v,9,8,seed+15)
        patch = profile(u,v,28,27,seed+16)
        patina = condition*self.weathering*(.36*ramp(.36,.74,.64*cloud+.36*shade)+.58*exposure)
        patina *= .71+.29*patch
        opacity = .91-.12*condition+.060*(cloud-.5)+.064*(brush-.5)-.31*patina
        lime = np.array([.821,.771,.648])
        sand = np.array([.491,.424,.322])
        hue = blend(sand,lime,np.clip(opacity,0,1))
        hue *= (1+.049*(patch-.5)+.020*(grains-.5)-.076*open_pores
                -.115*freckles+.027*polished)[...,None]
        hue = blend(hue,np.array([.475,.424,.338]),np.clip(.60*patina,0,.62))
        basecoat = np.array([.565,.497,.382])*(.82+.26*grit-.114*open_pores)[...,None]
        hue = blend(hue,basecoat,spall*.84)
        hue = blend(hue,np.array([.526,.442,.343]),trace*.64)
        roughness = .867+.051*open_pores+.030*patina+.048*spall+.018*(grit-.5)
        roughness -= .039*polished
        return Coat(depth,hue,np.clip(roughness,.80,.98))


def image_path(variant,channel):
    suffix = "exr" if channel in {"rough","height"} else "png"
    return ROOT/f"{STEM}_{variant}_{channel}.{suffix}"


def export(scene,variant,bakes):
    settings = scene.render.image_settings
    settings.color_mode = "RGB"
    for key,image in bakes.items():
        path = str(image_path(variant,key))
        if key=="albedo":
            scene.view_settings.view_transform = "Standard"
            scene.view_settings.look = "None"
            settings.file_format = "PNG"
            settings.color_depth = "8"
            image.save_render(path,scene=scene)
            scene.view_settings.view_transform = "AgX"
        elif key=="normal":
            image.filepath_raw = path
            image.file_format = "PNG"
            image.save()
        else:
            settings.file_format = "OPEN_EXR"
            settings.color_depth = "16"
            settings.exr_codec = "ZIP"
            image.save_render(path,scene=scene)


def verify_bake(variant,bakes,repeat):
    arrays = {}
    for label,image in bakes.items():
        array = arrays[label] = pixels(image)[:,:,:3]
        if repeat:
            np.testing.assert_array_equal(array,pixels(repeat[label])[:,:,:3],
                                          err_msg=f"{variant} {label}")
        if not np.isfinite(array).all() or array.min()<-.0002 or array.max()>1.0002:
            raise RuntimeError(f"Invalid {variant} {label} bake")
        seams = []
        for axis in (0,1):
            seam = np.abs(np.take(array,0,axis)-np.take(array,-1,axis)).mean()
            interior = np.abs(np.diff(array,axis=axis)).mean(
                axis=tuple(i for i in range(3) if i!=axis))
            if seam>1.20*interior.max()+.0001:
                raise ValueError(f"Visible wrap jump in {variant} {label} axis {axis}")
            seams.append((round(float(seam),5),round(float(interior.max()),5)))
        print(variant,label,"wrap / interior max",seams,flush=True)
    normal = arrays["normal"]*2-1
    if np.abs(np.linalg.norm(normal,axis=2)-1).max()>.025:
        raise RuntimeError(f"Invalid unit normals in {variant}")
    height = arrays["height"][:,:,0]*RELIEF
    dv,du = np.gradient(height)
    scores = [float(np.corrcoef((-grad).ravel(),normal[:,:,i].ravel())[0,1])
              for i,grad in enumerate((du,dv))]
    if min(scores)<.72:
        raise RuntimeError(f"Normal and height orientation disagree in {variant}: {scores}")
    print(variant,"normal-height alignment",np.round(scores,3),
          "surface relief in mm",np.round([height.min()*1000,height.max()*1000],3),flush=True)
    if repeat:
        print(f"{variant}: all four independent bakes match pixel-for-pixel",flush=True)


def make_materials():
    materials = {}
    for variant in VARIANTS:
        materials[variant] = mapped_material(
            f"Lowmark Lime Plaster | {variant}",BOUNDS,
            lambda key,variant=variant: image_path(variant,key))
        materials[variant]["caelm_repeat_metres"] = BOUNDS
        materials[variant]["caelm_height_range_m"] = RELIEF
    mat = bpy.data.materials.new("Lowmark Lime Plaster | Adjustable")
    mat.use_nodes = True
    nodes,links = mat.node_tree.nodes,mat.node_tree.links
    source = nodes.new("ShaderNodeUVMap")
    source.uv_map = "UV0_Metric"
    source.location = (-1040,180)
    mapping = nodes.new("ShaderNodeVectorMath")
    mapping.operation = "SCALE"
    mapping.location = (-830,180)
    mapping.inputs["Scale"].default_value = 1/TILE
    links.new(source.outputs["UV"],mapping.inputs[0])
    condition = nodes.new("ShaderNodeValue")
    condition.label = "Condition mix (0 maintained, 1 aged)"
    condition.outputs[0].default_value = .42
    condition.location = (-810,410)
    bsdf = nodes.get("Principled BSDF")
    bsdf.location = (120,320)
    nodes.get("Material Output").location = (420,320)
    for i,(key,socket) in enumerate((("albedo","Base Color"),("normal","Normal"),
                                      ("rough","Roughness"))):
        y = 260-i*465
        mix = nodes.new("ShaderNodeMixRGB")
        mix.label = f"{key.capitalize()} | condition"
        mix.location = (-290,y)
        links.new(condition.outputs[0],mix.inputs[0])
        for j,variant in enumerate(VARIANTS):
            texture = nodes.new("ShaderNodeTexImage")
            texture.image = bpy.data.images.load(str(image_path(variant,key)),check_existing=True)
            texture.image.colorspace_settings.name = "sRGB" if key=="albedo" else "Non-Color"
            texture.extension = "REPEAT"
            texture.location = (-565,y-j*230)
            links.new(mapping.outputs[0],texture.inputs["Vector"])
            links.new(texture.outputs["Color"],mix.inputs[j+1])
        signal = mix.outputs[0]
        if key=="normal":
            normal = nodes.new("ShaderNodeNormalMap")
            normal.location = (-60,y)
            normal.uv_map = source.uv_map
            links.new(signal,normal.inputs["Color"])
            signal = normal.outputs["Normal"]
        links.new(signal,bsdf.inputs[socket])
    materials["Adjustable"] = mat
    return materials


def write_library(materials):
    for mat in materials.values():
        mat.use_fake_user = True
    bpy.data.libraries.write(str(ROOT/f"{STEM}.blend"),set(materials.values()),
                             path_remap="RELATIVE_ALL",fake_user=True,compress=True)


def delete_mesh(obj):
    mesh = obj.data
    bpy.data.objects.remove(obj,do_unlink=True)
    if mesh.users==0:
        bpy.data.meshes.remove(mesh)


def plate(label,width,height,material):
    obj = surface_mesh(label,[(0,0,0),(width,0,0),(width,height,0),(0,height,0)],
                       np.array([[0,1,2,3]],np.int32))
    uv = obj.data.uv_layers.new(name="UV0_Metric")
    uv.data.foreach_set("uv",[0,0,width,0,width,height,0,height])
    obj.data.materials.append(material)
    return obj


def render(scene,label,width,height):
    scene.render.resolution_x,scene.render.resolution_y = width,height
    scene.render.resolution_percentage = 100
    settings = scene.render.image_settings
    settings.file_format = "PNG"
    settings.color_mode = "RGB"
    settings.color_depth = "8"
    scene.render.filepath = str(ROOT/f"{STEM}_{label}.png")
    bpy.ops.render.render(write_still=True)


def studio(scene):
    scene.world = bpy.data.worlds.new("Neutral plaster review")
    scene.world.use_nodes = True
    world = scene.world.node_tree.nodes.get("Background")
    world.inputs["Color"].default_value = (.76,.80,.84,1)
    world.inputs["Strength"].default_value = .43
    scene.cycles.samples = 26
    scene.cycles.use_denoising = True
    bpy.ops.object.camera_add()
    cam = scene.camera = bpy.context.object
    cam.data.type = "ORTHO"
    bpy.ops.object.light_add(type="SUN")
    sun = bpy.context.object
    sun.data.energy = 2.68
    sun.data.angle = .17
    return cam,sun


def clay_view(scene,camera,sun,original,condition):
    geometry = bake_source(BOUNDS,lambda x,y:original.sample(x,y,condition),600)
    geometry.data.materials.append(plain("Neutral plaster clay",(.47,.47,.47)))
    target = Vector((.87,.80,.008))
    camera.location = target+Vector((.21,-.54,2.3))
    point(camera,target)
    camera.data.ortho_scale = 1.30
    sun.location = (-3.9,-1.6,1.62)
    point(sun,(0,0,0))
    render(scene,"clay",1120,880)
    delete_mesh(geometry)


def swatches(scene,camera,sun,materials):
    target = Vector((.87,.80,0))
    camera.location = target+Vector((.21,-.54,2.3))
    point(camera,target)
    camera.data.ortho_scale = 1.30
    for name in VARIANTS:
        obj = plate("Plaster review patch",TILE,TILE,materials[name])
        render(scene,f"{name.lower()}_swatch",1120,880)
        delete_mesh(obj)
    width = 2*TILE
    obj = plate("Plaster 2x2",width,width,materials["Aged"])
    camera.location = (TILE,TILE,6)
    point(camera,(TILE,TILE,0))
    camera.data.ortho_scale = width
    sun.location = (-4,-2,3)
    point(sun,(0,0,0))
    render(scene,"repeat",1560,1560)
    delete_mesh(obj)


def set_material(obj,mat):
    if not obj.data.materials:
        obj.data.materials.append(mat)
    else:
        for i in range(len(obj.data.materials)):
            obj.data.materials[i] = mat


def approved_context_materials():
    timber_stem = "Lowmark_Structural_Timber"
    stone_stem = "Lowmark_Fieldstone_Masonry"

    def source(stem,key):
        ext = "exr" if key=="rough" else "png"
        return ROOT/f"{stem}_{key}.{ext}"

    timber = mapped_material("Approved Lowmark Structural Timber",(4.,1.),
                             lambda key:source(timber_stem,key),uv_offset=(.33,.23))
    stone = mapped_material("Approved Lowmark Fieldstone",(2.4,1.8),
                             lambda key:source(stone_stem,key))
    with bpy.data.libraries.load(str(ROOT/f"{stone_stem}_stone.blend")) as (source_lib,loaded):
        name = "Lowmark Fieldstone | Stone Only"
        if name not in source_lib.materials:
            raise RuntimeError("Approved fieldstone library is missing its stone surface")
        loaded.materials = [name]
    return timber,stone,loaded.materials[0]


def build_farmhouse(scene):
    generator = ROOT.parents[2]/"CODE"/"Scripts"/"architectural_generator"
    sys.path.insert(0,str(generator))
    from caelmor_architecture.blender_backend import build
    from caelmor_architecture.engine import generate
    from caelmor_architecture.model import Settings
    from caelmor_architecture.roof_autocomplete import build_roof_collection
    from caelmor_architecture.roof_selection import Bearing

    settings = Settings(footprint="RECT",width=8.2,depth=5.6,floors=1,
                        floor_height=2.75,detail="MEDIUM",seed=17)
    plan,_ = generate(settings)
    body,_ = build(settings)
    print("Built the Lowmark farmhouse review geometry",flush=True)
    x0,y0,x1,y1,ridge = plan.rects[0]
    # Roof AutoComplete offsets its local deck datum by 120 mm. Match the
    # farmhouse's eave and rise and keep the original gable wall and framing.
    bearing = Bearing(((x0+x1)/2,(y0+y1)/2,plan.eave-.12),x1-x0,y1-y0,0)
    roof = build_roof_collection(
        scene,bearing,rise=plan.slope*(y1-y0)/2,detail=60,
        material_directory=str(ROOT),overhang=settings.overhang,ridge=ridge,seed=settings.seed)
    print("Built the registered Brookoak roof on the farmhouse bearing",flush=True)
    timber,stone,cut_stone = approved_context_materials()
    plaster = []
    timber_count = 0
    fieldstone_count = 0
    body_meshes = tuple(body.all_objects)
    roof_meshes = tuple(roof.objects)
    for obj in body_meshes:
        if obj.type!="MESH":
            continue
        role = obj.get("caelm_material","")
        layer = obj.get("caelm_layer","")
        name = obj.name
        stock_facing = layer=="foundation" and any(
            name.startswith(s) for s in ("facade_stone","facade_mortar"))
        if obj.get("caelm_collider") or layer=="roof" or stock_facing:
            obj.hide_render = True
        elif role in {"plaster","plaster_patch"}:
            if "UV0_Metric" not in obj.data.uv_layers:
                raise RuntimeError(f"{name} is missing metric UV0")
            plaster.append(obj)
        elif role in {"timber","timber_light"}:
            set_material(obj,timber)
            timber_count += 1
        elif name.startswith(("facade_foundation_core","facade_chimney")):
            set_material(obj,stone)
            fieldstone_count += 1
        elif name.startswith(("facade_quoins","facade_steps")):
            set_material(obj,cut_stone)
            fieldstone_count += 1
    roof_surfaces = 0
    for obj in roof_meshes:
        if obj.name.startswith("Gable infill"):
            obj.hide_render = True
        elif "RoofUV" in obj.data.uv_layers:
            assert obj.data.materials[0].get("caelm_brookoak_maps")
            roof_surfaces += 1
        elif obj.get("caelm_material") in {"timber","timber_light"}:
            set_material(obj,timber)
            timber_count += 1
    if not plaster or not timber_count or not fieldstone_count or not roof_surfaces:
        raise RuntimeError("Farmhouse material binding incomplete")
    print(f"Actual farmhouse: {len(plaster)} plaster sections, {timber_count} approved "
          f"timber buffers, {fieldstone_count} approved fieldstone buffers, "
          f"{roof_surfaces} registered Brookoak roof surfaces, "
          f"{roof['caelm_roof_shingles']} dimensional shingles",flush=True)
    return plaster


def farmhouse(scene,camera,sun,materials):
    plaster = build_farmhouse(scene)
    floor = plate("Farmhouse review ground",1.,1.,plain("Muted earth",(.218,.196,.166)))
    floor.location = (-150,-150,-.032)
    floor.scale = (300,300,1)
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = .47
    sun.location = (-5,-8,10)
    point(sun,(4,2.5,0))
    sun.data.energy = 2.36
    sun.data.angle = .20
    camera.data.type = "PERSP"
    for name in VARIANTS:
        for obj in plaster:
            set_material(obj,materials[name])
        print(f"Reviewing {name} on {len(plaster)} farmhouse plaster sections",flush=True)
        target = Vector((4.1,2.58,2.97))
        camera.location = target+Vector((9.1,-16.7,6.7))
        point(camera,target)
        camera.data.lens = 47
        render(scene,f"{name.lower()}_farmhouse",1600,1120)
        target = Vector((1.88,-.10,1.46))
        camera.location = target+Vector((1.62,-5.10,1.04))
        point(camera,target)
        camera.data.lens = 47
        render(scene,f"{name.lower()}_detail",1440,1080)


def main():
    parser = ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--bake-only",action="store_true")
    mode.add_argument("--render-only",action="store_true",help="Review the existing exports")
    mode.add_argument("--clay-only",action="store_true")
    parser.add_argument("--size",type=int,default=2048)
    parser.add_argument("--seed",type=int,default=SEED)
    parser.add_argument("--maintained-condition",type=float,default=.13)
    parser.add_argument("--aged-condition",type=float,default=.77)
    parser.add_argument("--weathering",type=float,default=.82)
    parser.add_argument("--trowel",type=float,default=.83)
    parser.add_argument("--verify-repeat",action="store_true")
    args = parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    controls = (args.maintained_condition,args.aged_condition,args.weathering,args.trowel)
    if args.size<256 or not all(0<=x<=1 for x in controls):
        parser.error("Resolution must be at least 256. All finish controls are in [0, 1].")
    if args.maintained_condition>=args.aged_condition:
        parser.error("Aged condition must exceed maintained condition.")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 1
    scene.view_settings.view_transform = "AgX"
    original = Plaster(args.seed,args.weathering,args.trowel)
    if args.clay_only:
        cam,sun = studio(scene)
        clay_view(scene,cam,sun,original,args.aged_condition)
        return
    if not args.render_only:
        authored,color = source_material()
        authored.name = "Lime plaster high surface"
        sample = min(1024,max(256,args.size//2))

        def bake_condition(variant,condition):
            # Each verification pass re-creates the geometry and all finish
            # attributes, then bakes through the same native Blender cage.
            source = bake_source(BOUNDS,lambda x,y:original.sample(x,y,condition),sample)
            source.data.materials.append(authored)
            baked = bake(BOUNDS,variant,source,authored,color,(args.size,args.size),RELIEF)
            delete_mesh(source)
            return baked

        for variant,condition in zip(VARIANTS,(args.maintained_condition,args.aged_condition)):
            outputs = bake_condition(variant,condition)
            repeated = bake_condition(variant,condition) if args.verify_repeat else None
            verify_bake(variant,outputs,repeated)
            export(scene,variant,outputs)
            for image in list(outputs.values())+list((repeated or {}).values()):
                bpy.data.images.remove(image)
    materials = make_materials()
    if not args.render_only:
        write_library(materials)
    if not args.bake_only:
        camera,sun = studio(scene)
        clay_view(scene,camera,sun,original,args.aged_condition)
        swatches(scene,camera,sun,materials)
        farmhouse(scene,camera,sun,materials)


if __name__ == "__main__":
    main()
