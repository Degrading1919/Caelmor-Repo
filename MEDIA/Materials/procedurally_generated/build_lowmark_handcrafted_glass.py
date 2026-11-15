"""Build mouth-blown pane geometry, map exports and matched Cycles reviews."""

from argparse import ArgumentParser
from pathlib import Path
from collections import Counter
import json
import math
import sys

import bpy
import numpy as np
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from build_lowmark_structural_timber import grid_faces, plain, point, profile, ramp, surface_mesh

STEM = "Lowmark_Handcrafted_Window_Glass"
SEED = 70931
TILE = .36
NOMINAL = .00265
THICKNESS_RANGE = .004
FRONT_SPAN = .004
IOR = 1.515
ABSORPTION_COLOR = (.445,.794,.682)
ABSORPTION_DENSITY = 30.
CLEAR_WAVE = .40
CLEAR_SHAPE = "Clear | subdued waviness"
FINISHES = ("Clear","Lightly_Weathered","Obscured")
LABELS = ("Clear","Lightly Weathered","Obscured")
UP = Vector((0,0,1))


class DrawnGlass:
    """A gently bowed sheet with thickness structure independent of its bow."""

    def __init__(self,seed,wave):
        self.seed,self.wave = seed,wave

    def shape(self,x,y,*,clear=False):
        u,v = x/TILE,y/TILE
        seed = self.seed
        flow = u+.060*(profile(u,v,3,5,seed+1)-.5)
        flow += .033*np.sin(math.tau*(v+u))
        ribbon = profile(flow,v,9,3,seed+4)
        pull = profile(flow,v,14,7,seed+5)
        wrinkle = profile(flow,v,28,18,seed+7)
        body = profile(u,v,5,5,seed+10)
        bow = .00160*(body-.5)+.00051*(ribbon-.5)
        bow += .000108*(wrinkle-.5)
        change = .00069*(ribbon-.5)+.00057*(pull-.5)+.000095*(wrinkle-.5)
        change += .00027*(profile(u,v,17,14,seed+12)-.5)
        wave = self.wave*CLEAR_WAVE if clear else self.wave
        thickness = NOMINAL+wave*change
        bow *= wave
        return bow+(thickness-NOMINAL)/2, bow-(thickness+NOMINAL)/2, thickness

    def roughness(self,x,y):
        u,v = x/TILE,y/TILE
        fine = profile(u,v,61,54,self.seed+15)
        wash = profile(u+.018*(fine-.5),v,13,17,self.seed+17)
        pooled = (profile(u,v,4,6,self.seed+19)*.64+.36*wash)
        tide = ramp(.49,.76,pooled)
        freckles = ramp(.67,.89,fine)*ramp(.37,.71,wash)
        clear = .014+.013*wash+.007*fine
        weathered = clear+.042+.105*tide+.025*freckles
        obscure = .268+.071*wash+.047*tide+.010*fine
        return dict(zip(FINISHES,(clear,weathered,obscure)))


def path(channel):
    return ROOT/f"{STEM}_{channel}.exr"


def shape_maps(field,x,y,pitch,*,clear):
    front,_,thickness = field.shape(x,y,clear=clear)
    # Analytic surface samples at adjacent texel centers, including across wrap.
    sy = (field.shape(x,y+pitch,clear=clear)[0]-field.shape(x,y-pitch,clear=clear)[0])/(2*pitch)
    sx = (field.shape(x+pitch,y,clear=clear)[0]-field.shape(x-pitch,y,clear=clear)[0])/(2*pitch)
    n = np.stack((-sx,-sy,np.ones_like(sx)),axis=-1)
    n /= np.linalg.norm(n,axis=-1)[...,None]
    sigma = ABSORPTION_DENSITY*(1-np.asarray(ABSORPTION_COLOR))
    tint = np.exp(-thickness[...,None]*sigma)
    return {
        "normal":.5+.5*n,
        "height":.5+front/FRONT_SPAN,
        "thickness":thickness/THICKNESS_RANGE,
        "transmission_color":tint,
    }


def maps(field,size):
    pitch = TILE/size
    centers = (np.arange(size,dtype=float)+.5)*pitch
    x,y = np.meshgrid(centers,centers)
    out = shape_maps(field,x,y,pitch,clear=False)
    out.update({f"Clear_{key}":val for key,val in shape_maps(field,x,y,pitch,clear=True).items()})
    out.update({f"{finish}_rough":val for finish,val in field.roughness(x,y).items()})
    return {k:(np.repeat(v[:,:,None],3,axis=2) if v.ndim==2 else v).astype(np.float32)
            for k,v in out.items()}


def inspect(field,data,size):
    for key,val in data.items():
        if val.shape!=(size,size,3) or not np.isfinite(val).all() or not (0<=val.min()<=val.max()<=1):
            raise RuntimeError(f"Invalid {key} image")
        for axis in (0,1):
            seam = np.mean(np.abs(np.take(val,0,axis)-np.take(val,-1,axis)))
            cols = tuple(i for i in range(3) if i!=axis)
            internal = np.mean(np.abs(np.diff(val,axis=axis)),axis=cols)
            if seam>1.15*internal.max()+3e-4:
                raise RuntimeError(f"{key} jumps at repeat axis {axis}")
    for prefix in ("","Clear_"):
        inspect_shape(field,data,size,prefix)
    rough = [data[f"{finish}_rough"].mean() for finish in FINISHES]
    if not rough[0]<rough[1]<rough[2]:
        raise RuntimeError("Finish order does not increase scatter")
    print(f"Mean roughness {np.round(rough,3)} | channels and both seam axes passed",flush=True)


def inspect_shape(field,data,size,prefix):
    h = (data[prefix+"height"][:,:,0]-.5)*FRONT_SPAN
    gradients = [(np.roll(h,-1,axis)-np.roll(h,1,axis))/(2*TILE/size) for axis in (1,0)]
    n = data[prefix+"normal"]*2-1
    if np.max(np.abs(np.linalg.norm(n,axis=-1)-1))>.005:
        raise RuntimeError("Non-unit tangent normals")
    if field.wave:
        if min(np.corrcoef((-g).ravel(),n[:,:,i].ravel())[0,1] for i,g in enumerate(gradients))<.97:
            raise RuntimeError("Normal direction disagrees with the exported outward height")
    t = data[prefix+"thickness"][:,:,0]*THICKNESS_RANGE
    if not (.0017<t.min() and t.max()<.0037):
        raise RuntimeError(f"Unphysical pane thickness {t.min():.5f}–{t.max():.5f} m")
    sigma = ABSORPTION_DENSITY*(1-np.asarray(ABSORPTION_COLOR))
    np.testing.assert_allclose(data[prefix+"transmission_color"],np.exp(-t[...,None]*sigma),atol=.001)
    print(f"{prefix.rstrip('_') or 'Shared'} thickness {1000*t.min():.3f}–{1000*t.max():.3f} mm",flush=True)


def save_maps(scene,data):
    settings = scene.render.image_settings
    settings.file_format,settings.color_mode,settings.color_depth = "OPEN_EXR","RGB","16"
    settings.exr_codec = "ZIP"
    for key,val in data.items():
        size = val.shape[0]
        buf = np.ones((size,size,4),np.float32)
        buf[:,:,:3] = val
        image = bpy.data.images.new(key,size,size,alpha=False,float_buffer=True)
        image.colorspace_settings.name = "Non-Color"
        image.pixels.foreach_set(buf.ravel())
        image.save_render(str(path(key)),scene=scene)
        bpy.data.images.remove(image)


def reopen_maps(keys,field,size):
    out = {}
    for key in keys:
        im = bpy.data.images.load(str(path(key)))
        im.colorspace_settings.name = "Non-Color"
        channel = np.empty(len(im.pixels),np.float32)
        im.pixels.foreach_get(channel)
        out[key] = channel.reshape(size,size,4)[:,:,:3]
        bpy.data.images.remove(im)
    inspect(field,out,size)
    return out


def native_project(finish):
    # The standard Material Maker material is a map-review surface. Its opacity
    # input does not describe the transmission of a closed dielectric.
    prefix = "Clear_" if finish=="Clear" else ""
    defs = (
        ("Wave normals","image",-630,0,{"image":f"%PROJECT_PATH%/{path(prefix+'normal').name}","fix_ar":False}),
        ("Roughness","image",-630,390,{"image":f"%PROJECT_PATH%/{path(f'{finish}_rough').name}","fix_ar":False}),
        ("Outward height","image",-630,635,{"image":f"%PROJECT_PATH%/{path(prefix+'height').name}","fix_ar":False}),
        ("Components","decompose",-410,0,{}),("Native X","invert",-230,-115,{}),
        ("Native Z","invert",-230,164,{}),("Native normal","combine",-45,0,{}),
        ("Depth","invert",-210,590,{}),
        ("Material","material",200,176,{"size":10,"metallic":0.,"roughness":1.,"normal":1.,
                                       "depth_scale":FRONT_SPAN/TILE,"ao":1.}),
    )
    edges = (
        ("Wave normals",0,"Components",0),("Components",0,"Native X",0),
        ("Components",2,"Native Z",0),("Native X",0,"Native normal",0),
        ("Components",1,"Native normal",1),("Native Z",0,"Native normal",2),
        ("Native normal",0,"Material",4),("Roughness",0,"Material",2),
        ("Outward height",0,"Depth",0),("Depth",0,"Material",6),
    )
    nodes = [{"name":n,"type":t,"seed_int":0,"node_position":{"x":x,"y":y},"parameters":p}
             for n,t,x,y,p in defs]
    nodes[-1]["export_paths"] = {}
    graph = {"name":"Graph","type":"graph","label":f"Lowmark Glass Maps | {finish.replace('_',' ')}",
             "seed_int":0,"node_position":{"x":0,"y":0},"parameters":{},"nodes":nodes,
             "connections":[{"from":a,"from_port":b,"to":c,"to_port":d} for a,b,c,d in edges]}
    (ROOT/f"{STEM}_{finish}.ptex").write_text(json.dumps(graph,indent=2)+"\n",encoding="utf8")


def optical_material(finish):
    mat = bpy.data.materials.new(f"Lowmark Handcrafted Glass | {finish.replace('_',' ')}")
    mat.use_nodes = True
    mat["caelm_tile_metres"] = TILE
    mat["caelm_nominal_thickness_m"] = NOMINAL
    ns,links = mat.node_tree.nodes,mat.node_tree.links
    ns.clear()
    uv = ns.new("ShaderNodeUVMap")
    uv.uv_map,uv.location = "UV0_Metric",(-720,225)
    scale = ns.new("ShaderNodeVectorMath")
    scale.operation,scale.location = "SCALE",(-510,225)
    scale.inputs["Scale"].default_value = 1/TILE
    links.new(uv.outputs["UV"],scale.inputs[0])
    rough = ns.new("ShaderNodeTexImage")
    rough.image = bpy.data.images.load(str(path(f"{finish}_rough")),check_existing=True)
    rough.image.colorspace_settings.name = "Non-Color"
    rough.label,rough.location = "Weathering and microfacet spread",(-315,225)
    links.new(scale.outputs[0],rough.inputs["Vector"])

    glass = ns.new("ShaderNodeBsdfGlass")
    glass.distribution = "BECKMANN"
    glass.location = (-42,190)
    glass.inputs["Color"].default_value = (1,1,1,1)
    glass.inputs["IOR"].default_value = IOR
    links.new(rough.outputs["Color"],glass.inputs["Roughness"])
    tint = ns.new("ShaderNodeVolumeAbsorption")
    tint.label,tint.location = "Faint batch tint through real path length",(-45,-30)
    tint.inputs["Color"].default_value = (*ABSORPTION_COLOR,1)
    tint.inputs["Density"].default_value = ABSORPTION_DENSITY
    out = ns.new("ShaderNodeOutputMaterial")
    out.location = (217,166)
    links.new(glass.outputs[0],out.inputs["Surface"])
    links.new(tint.outputs[0],out.inputs["Volume"])
    return mat


def pane(name,field,width,height,origin,u,normal,phase,mat,pitch,*,clear=False,review_shape=False):
    nx,ny = math.ceil(width/pitch)+1,math.ceil(height/pitch)+1
    x,y = np.meshgrid(np.linspace(0,width,nx),np.linspace(0,height,ny))
    uv = np.column_stack((x.ravel()+phase[0],y.ravel()+phase[1]))
    flat = np.asarray(origin)+x.ravel()[:,None]*np.asarray(u)+y.ravel()[:,None]*np.asarray(UP)

    def sheet(clear):
        front,rear,_ = field.shape(x+phase[0],y+phase[1],clear=clear)
        return np.concatenate([flat+layer.ravel()[:,None]*np.asarray(normal) for layer in (front,rear)])

    points = sheet(clear)
    leading = grid_faces(nx,ny)
    count = nx*ny
    trailing = leading[:,::-1]+count
    boundary = np.r_[np.arange(nx),np.arange(1,ny)*nx+nx-1,
                     (ny-1)*nx+np.arange(nx-2,-1,-1),np.arange(ny-2,0,-1)*nx]
    following = np.roll(boundary,-1)
    sides = np.column_stack((following,boundary,boundary+count,following+count))
    faces = np.concatenate((leading,trailing,sides))
    obj = surface_mesh(name,points,faces)
    obj.data.materials.append(mat)
    layer = obj.data.uv_layers.new(name="UV0_Metric")
    layer.data.foreach_set("uv",uv[faces.ravel()%count].astype(np.float32).ravel())
    obj.data.polygons.foreach_set("use_smooth",np.r_[np.ones(2*len(leading),bool),np.zeros(len(sides),bool)])
    if review_shape:
        obj.shape_key_add(name="Shared formed sheet")
        key = obj.shape_key_add(name=CLEAR_SHAPE)
        key.data.foreach_set("co",sheet(True).astype(np.float32).ravel())
    return obj,points,faces


def verify_shell(points,faces,normal):
    if not np.isfinite(points).all():
        raise RuntimeError("Nonfinite pane mesh")
    edges = Counter(tuple(sorted((int(a),int(b)))) for f in faces for a,b in zip(f,np.roll(f,-1)))
    if set(edges.values())!={2}:
        raise RuntimeError("Open or nonmanifold pane")
    mid = len(points)//2
    thickness = (points[:mid]-points[mid:])@np.asarray(normal)
    if thickness.min()<=.0017:
        raise RuntimeError("Glass surfaces intersect")
    left = np.cross(points[faces[0,1]]-points[faces[0,0]],points[faces[0,3]]-points[faces[0,0]])
    if left@np.asarray(normal)<=0:
        raise RuntimeError("Swapped entrance and exit faces")


def write_library(field,materials):
    chips = set()
    for i,finish in enumerate(FINISHES):
        name = f"{LABELS[i]} sample pane (0.28 m × 0.34 m)"
        obj,points,faces = pane(name,field,.28,.34,Vector((i*.36,0,0)),
                               Vector((1,0,0)),Vector((0,-1,0)),
                               (.071,.114),materials[finish],.0036,clear=finish=="Clear")
        verify_shell(points,faces,Vector((0,-1,0)))
        chips.add(obj)
    bpy.data.libraries.write(str(ROOT/f"{STEM}.blend"),chips|set(materials.values()),
                             path_remap="RELATIVE_ALL",fake_user=True,compress=True)
    for obj in chips:
        mesh = obj.data
        bpy.data.objects.remove(obj,do_unlink=True)
        bpy.data.meshes.remove(mesh)


def fit_windows(scene,field,material,draft):
    # The native facade builds each opening as a separate eight-vertex prism.
    # Preserve its aperture and trim and replace the placeholder in this scene.
    boxes = []
    for obj in tuple(scene.objects):
        if obj.type!="MESH" or not obj.name.startswith("facade_windows"):
            continue
        obj.hide_render = True
        if len(obj.data.vertices)%8 or len(obj.data.polygons)*8!=len(obj.data.vertices)*6:
            raise RuntimeError(f"Unexpected native glazing topology in {obj.name}")
        points = np.asarray([tuple(obj.matrix_world@v.co) for v in obj.data.vertices])
        for box in points.reshape(-1,8,3):
            low,high = box.min(axis=0),box.max(axis=0)
            small = int(np.argmin((high-low)[:2]))
            if not np.isclose(high[small]-low[small],.018,atol=.001):
                raise RuntimeError("Unexpected pane placeholder thickness")
            center = (low+high)/2
            normal = Vector((0,0,0))
            normal[small] = 1.0 if center[small]>(4.1,2.8)[small] else -1.0
            u = UP.cross(normal)
            origin = Vector(center)-u*(high[1-small]-low[1-small])/2
            origin.z = low[2]
            boxes.append((Vector(center),origin,u,normal,
                          float(high[1-small]-low[1-small]),float(high[2]-low[2])))
    front = [b for b in boxes if b[0].y<.10 and b[0].x>4.5]
    if not front:
        raise RuntimeError("Actual front farmhouse aperture unavailable")
    target = min(front,key=lambda b:abs(b[0].x-6.15))
    rng = np.random.default_rng(field.seed+57)
    objects = []
    for index,(center,origin,u,n,width,height) in enumerate(boxes):
        # Extend the perimeter into the surrounding timber rebate so it
        # stays covered at oblique angles. Follow the native single sheet
        # behind the separate cross bars, whose ends stop inside the opening.
        lap_u,lap_v = .051,.058
        cut = origin-lap_u*u-lap_v*UP
        phase = tuple(rng.uniform(0,TILE,2)-np.array([lap_u,lap_v]))
        obj,points,faces = pane(f"Window {index+1} | formed glass sheet",
            field,width+2*lap_u,height+2*lap_v,cut,u,n,phase,material,.006 if draft else .0038,
            review_shape=True)
        if not objects or center==target[0]:
            verify_shell(points,faces,n)
        objects.append(obj)
    print(f"Fitted {len(objects)} closed panes to {len(boxes)} native windows | "
          f"front aperture {target[4]:.3f} × {target[5]:.3f} m at {tuple(target[0])}",flush=True)
    return target[0],objects


def block(name,location,scale,mat):
    bpy.ops.mesh.primitive_cube_add(size=1,location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    obj.data.materials.append(mat)
    return obj


def vessel(name,loc,section,mat):
    a = np.linspace(0,math.tau,96,endpoint=False)
    points = [(loc[0]+r*math.cos(t),loc[1]+r*math.sin(t),loc[2]+z)
              for z,r in section for t in a]
    i = np.arange(len(points)).reshape(len(section),len(a))
    j = np.roll(i,-1,axis=1)
    faces = np.stack((i[:-1],j[:-1],j[1:],i[1:]),axis=-1).reshape(-1,4)
    obj = surface_mesh(name,points,faces)
    obj.data.materials.append(mat)
    for face in obj.data.polygons:
        face.use_smooth = True
    rounded = obj.modifiers.new("Thrown clay curves","SUBSURF")
    rounded.levels = 1
    rounded.render_levels = 2
    return obj


def furnish(center):
    x,y,z = center
    wall = plain("Interior chalk plaster",(.41,.32,.223))
    timber = plain("Interior walnut shelf",(.159,.084,.044))
    indigo = plain("Muted blue glaze",(.044,.15,.167),.44)
    crock = plain("Warm earthenware",(.34,.143,.081),.58)
    cream = plain("Undyed ceramic",(.57,.443,.285),.49)
    linen = plain("Unbleached linen",(.384,.348,.269))
    block("Interior wall behind the glazing",(x,y+1.37,z-.1),(2.7,.075,2.18),wall)
    for dx in (-.48,.10,.58):
        block("Interior vertical framing",(x+dx,y+1.316,z-.04),(.045,.045,1.5),timber)
    block("Upper interior shelf",(x-.13,y+.97,z+.137),(1.50,.59,.043),timber)
    block("Lower work bench",(x+.035,y+.57,z-.367),(1.55,.70,.056),timber)
    block("Folded linen",(x+.195,y+.47,z-.311),(.36,.34,.043),linen)
    for i in range(2):
        block("Fold in linen",(x+.16+i*.074,y+.470,z-.283),(.023,.29,.016),linen)
    vessel("Blue cross-lit storage jug",(x-.213,y+.39,z-.341),
           ((0,.078),(.033,.111),(.14,.127),(.251,.094),(.284,.050),
            (.345,.035),(.354,.047),(.374,.047),(.378,.034),(.35,.031)),indigo)
    vessel("Terracotta crock",(x+.295,y+.79,z-.338),
           ((0,.083),(.048,.123),(.20,.131),(.236,.133),(.242,.119),(.205,.112)),crock)
    vessel("Light ceramic on the back shelf",(x+.12,y+1.035,z+.158),
           ((0,.063),(.034,.103),(.159,.106),(.226,.077),(.242,.077),(.247,.067),
            (.214,.064)),cream)
    # Real straight features at two depths make local refraction observable.
    block("Freestanding slatted tool rail",(x-.21,y+.79,z+.31),(.46,.031,.029),timber)
    for i in range(4):
        block("Hanging straight wood tool",(x-.39+i*.102,y+.781,z+.253),
              (.022,.028,.174-i*.017),timber)


def build_review(scene,field,materials,draft):
    from build_lowmark_lime_plaster import build_farmhouse, make_materials, set_material
    from build_lowmark_planked_oak import orient_and_phase
    from build_lowmark_forged_iron import area

    plaster = build_farmhouse(scene)
    lime = make_materials()["Maintained"]
    for obj in plaster:
        set_material(obj,lime)
    with bpy.data.libraries.load(str(ROOT/"Lowmark_Planked_Oak_Joinery.blend")) as (_,loaded):
        loaded.materials = ["Lowmark Planked Oak | Wood Weathered"]
    oak = loaded.materials[0]
    with bpy.data.libraries.load(str(ROOT/"Lowmark_Forged_Iron_Hardware.blend")) as (_,loaded):
        loaded.materials = ["Lowmark Forged Iron | Weathered"]
    iron = loaded.materials[0]
    for obj in tuple(scene.objects):
        if obj.type!="MESH":
            continue
        if obj.name.startswith(("facade_doors","facade_shutters")):
            set_material(obj,oak)
            orient_and_phase(obj)
        elif obj.name.startswith("facade_iron"):
            set_material(obj,iron)

    center,glass = fit_windows(scene,field,materials["Clear"],draft)
    x,y,z = center
    furnish(center)
    floor = plain("Neutral courtyard ground",(.167,.145,.119))
    block("Review ground",(4,3,-.14),(80,80,.20),floor)
    scene.world = bpy.data.worlds.new("Neutral daylight sky")
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (.66,.71,.78,1)
    bg.inputs["Strength"].default_value = .21
    bpy.ops.object.light_add(type="SUN",location=(x-4,-6,8))
    sun = bpy.context.object
    sun.data.energy,sun.data.angle = 1.40,.16
    point(sun,(x,0,z))
    area("Interior daylight key",(x-.76,y+.40,z+.58),(x,y+.94,z),44,.88,.57)
    area("Interior back wall bounce",(x+.66,y+.52,z+.48),(x,y+1.2,z),28,.75,.54)
    reflection = area("Tall exterior reflected light",(x-1.25,-2.15,z+.37),center,82,.36,1.12)
    bpy.ops.object.camera_add()
    camera = scene.camera = bpy.context.object
    camera.data.lens = 57
    camera.location = (x+.49,-2.60,z+.14)
    point(camera,center)
    return center,glass,camera,reflection


def render(scene,key,w,h):
    scene.render.resolution_x,scene.render.resolution_y = w,h
    scene.render.resolution_percentage = 100
    settings = scene.render.image_settings
    settings.file_format,settings.color_mode,settings.color_depth = "PNG","RGB","8"
    scene.render.filepath = str(ROOT/f"{STEM}_{key}.png")
    bpy.ops.render.render(write_still=True)


def review(scene,field,materials,draft):
    center,glass,camera,reflection = build_review(scene,field,materials,draft)
    w,h = (930,735) if draft else (1550,1190)
    for finish in ("Open",*FINISHES):
        for obj in glass:
            obj.hide_render = finish=="Open"
            if finish!="Open":
                set_glazing_finish(obj,materials,finish)
        scene.cycles.samples = (84 if draft else 216) if finish=="Obscured" else (28 if draft else 88)
        render(scene,finish.lower(),w,h)
    scene.cycles.samples = 28 if draft else 88

    for obj in glass:
        set_glazing_finish(obj,materials,"Clear")
    x,y,z = center
    reflection.location = (x-2.35,-2.03,z+.30)
    reflection.data.energy = 123
    point(reflection,center)
    camera.location = (x+1.26,-1.90,z+.16)
    camera.data.lens = 63
    point(camera,center)
    render(scene,"grazing",w,h)

    for obj in glass:
        set_glazing_finish(obj,materials,"Lightly_Weathered")
    camera.location = (x+5.9,-8.2,4.02)
    camera.data.lens = 45
    point(camera,(4.6,1.2,2.58))
    render(scene,"farmhouse",w,h)


def set_glazing_finish(obj,materials,finish):
    obj.data.materials[0] = materials[finish]
    obj.data.shape_keys.key_blocks[CLEAR_SHAPE].value = float(finish=="Clear")


def main():
    args = ArgumentParser()
    mode = args.add_mutually_exclusive_group()
    mode.add_argument("--maps-only",action="store_true")
    mode.add_argument("--render-only",action="store_true")
    args.add_argument("--draft",action="store_true")
    args.add_argument("--optix",action="store_true",help="Use an available NVIDIA OptiX device for the review renders.")
    args.add_argument("--seed",type=int,default=SEED)
    args.add_argument("--wave",type=float,default=1.)
    args.add_argument("--verify-repeat",action="store_true")
    cfg = args.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    if cfg.seed<0 or not 0<=cfg.wave<=1.25:
        args.error("Use a nonnegative seed and a wave scale between 0 and 1.25.")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    if cfg.optix:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "OPTIX"
        prefs.refresh_devices()
        if not any(d.type=="OPTIX" for d in prefs.devices):
            args.error("No Cycles OptiX device is available.")
        for device in prefs.devices:
            device.use = device.type=="OPTIX"
        scene.cycles.device = "GPU"
    scene.cycles.adaptive_threshold = .012
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 10
    scene.cycles.transmission_bounces = 8
    scene.view_settings.view_transform = "AgX"
    field = DrawnGlass(cfg.seed,cfg.wave)
    if not cfg.render_only:
        size = 512 if cfg.draft else 1024
        data = maps(field,size)
        inspect(field,data,size)
        if cfg.verify_repeat:
            independent = maps(DrawnGlass(cfg.seed,cfg.wave),size)
            for key in data:
                np.testing.assert_array_equal(data[key],independent[key])
            # Confirm the signed shape fields and finishes are periodic in metres.
            q = np.linspace(-.12,.53,107)
            x,y = np.meshgrid(q,q+.012)
            for clear in (False,True):
                for dx,dy in ((TILE,0),(0,-TILE),(TILE,TILE)):
                    shape = field.shape(x,y,clear=clear)
                    tiled = field.shape(x+dx,y+dy,clear=clear)
                    for left,right in zip(shape,tiled):
                        np.testing.assert_allclose(left,right,rtol=0,atol=1e-12)
            print(f"{len(data)} exports match independent regeneration pixel-for-pixel",flush=True)
        save_maps(scene,data)
        reopened = reopen_maps(data.keys(),field,size)
        for key in data:
            np.testing.assert_allclose(data[key],reopened[key],rtol=0,atol=5e-4)
        del reopened,data
    materials = {finish:optical_material(finish) for finish in FINISHES}
    if not cfg.render_only:
        write_library(field,materials)
        for finish in FINISHES:
            native_project(finish)
    if not cfg.maps_only:
        review(scene,field,materials,cfg.draft)


if __name__=="__main__":
    main()
