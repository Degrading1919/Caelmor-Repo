"""Build and bake the registered Brookoak roof tile in Blender 5.0.

blender --background --python build_brookoak.py -- --size 2048
Set --size 768 for a quick review. Outputs sit beside this script.
"""
import argparse
import ast
from pathlib import Path
import sys

import bpy
from mathutils import Vector
import numpy as np


ROOT = Path(__file__).resolve().parent
STEM = "Lowmark_Brookoak_RoofShingles_RivenBake"
COURSE_SOURCE = ROOT.parents[2] / "CODE/Scripts/architectural_generator/caelmor_architecture/brookoak_courses.py"
COURSES = next(ast.literal_eval(node.value) for node in ast.parse(
    COURSE_SOURCE.read_text(encoding="utf-8")).body if isinstance(node, ast.Assign)
    and any(getattr(target, "id", "") == "JOINTS" for target in node.targets))
WIDTH, LENGTH, EXPOSURE = 1.28, 2.40, .30
HEIGHT_RANGE = .050


def noise(x, y, seed):
    """Smooth deterministic lattice noise, continuous across sample grids."""
    i, j = np.floor(x), np.floor(y)
    a, b = x-i, y-j
    a, b = a*a*(3-2*a), b*b*(3-2*b)

    def corner(ix, iy):
        k = np.sin(ix*127.1+iy*311.7+seed*19.37)*43758.5453123
        return k-np.floor(k)

    return (1-b)*((1-a)*corner(i,j)+a*corner(i+1,j)) + b*((1-a)*corner(i,j+1)+a*corner(i+1,j+1))


def smooth(lo, hi, v):
    t = np.clip((v-lo)/(hi-lo), 0, 1)
    return t*t*(3-2*t)


def shingle(width, seed, detail):
    rng = np.random.default_rng(seed)
    nx, ny = detail, detail+25
    gx = np.linspace(0, 1, nx+1)
    # Sample the steep, curved end more densely than the main face.
    gy = np.r_[[-.012, -.006, -.003, 0, .004, .009, .016, .024], np.linspace(.035, 1, ny+1)]
    x, t = np.meshgrid(gx, gy)
    y = np.maximum(t, 0)
    j = rng.uniform(0, 100)
    kx, ky = rng.uniform(.25,.77), rng.uniform(.31,.82)
    has_knot = rng.random() < .35
    # Map fibers around a pocket in the timber. The core and surrounding
    # fibers are sampled from the same shifted longitudinal coordinate.
    dx, dy = (x-kx), (y-ky)*.76
    kr = rng.uniform(.023,.056)
    radius = np.sqrt(dx*dx+dy*dy)
    # Split boards mostly follow long grain. Reserve strong curvature for a
    # minority of boards and the local flow around a knot.
    figure = .057 if j < 25 else .027
    shear = x + figure*(noise(x*2.2+j,y*1.8,seed)-.5)
    shear += rng.uniform(-.12,.12)*(y-.5) + .011*np.sin(5*y+j)
    if has_knot:
        pinch = dx*(kr*kr/(radius*radius+kr*kr*.55))*np.exp(-radius/.18)
        shear -= 1.9*pinch
    core = (1-smooth(kr*.35,kr*1.12,radius)) if has_knot else np.zeros_like(x)

    bundles = noise(shear*rng.uniform(7.,13.)+j,y*3.5,seed+1)
    cleavage = smooth(.32,.52,bundles) - .48*smooth(.65,.83,bundles)
    long_fiber = noise(shear*rng.uniform(34,58)+j,y*3.8,seed+2)
    earlywood = (1-smooth(.22,.46,long_fiber)) * (.35+.65*noise(shear*13,y*4.1,seed+3))
    fine = noise(shear*112+j,y*17,seed+4)
    pores = smooth(.63,.84,noise(shear*140+j,y*39,seed+5))

    fissures = np.zeros_like(x)
    torn_flank = np.zeros_like(x)
    fracture_rng = np.random.default_rng(seed+8719)
    for _ in range(fracture_rng.integers(3,8)):
        sx, sy = fracture_rng.uniform(.08,.94), fracture_rng.uniform(.08,.77)
        span = fracture_rng.uniform(.09,.40)
        throat = fracture_rng.uniform(.0035,.013) * smooth(0,.14,y)
        run = np.maximum(1-np.abs(y-sy)/span,0)**.68
        across = shear - sx - .010*np.sin(y*13+j+sx*17)
        cut = (1-smooth(.16,1,np.abs(across)/(throat*run+.0008)))*run
        cut *= .34+.66*noise(shear*12+j,y*13,seed+24)
        fissures = np.maximum(fissures,cut)
        flank = (1-smooth(.7,2.2,np.abs(across)/(throat*run+.0008)))*run
        torn_flank = np.maximum(torn_flank,np.maximum(flank-cut,0))

    distress = np.zeros_like(x)
    # End checks open at the butt and taper along crooked longitudinal fibers.
    for _ in range(rng.choice([0,1,2],p=[.27,.52,.21])):
        cx, extent, opening = rng.uniform(.12,.88), rng.uniform(.13,.58), rng.uniform(.008,.028)
        line = cx + rng.uniform(-.09,.09)*y
        line += .018*(noise(y*7+j,cx*11,seed+10)-.5)
        taper = np.maximum(1-y/extent,0)
        crack = (1-smooth(.18,1,np.abs(x-line)/(opening*taper+.00065)))*taper**.65
        distress = np.maximum(distress, crack)

    edge_noise = noise(x*9+j,0,seed+12)
    retreat = rng.uniform(-.0045,.0055) + .005*(edge_noise-.5)
    for _ in range(rng.choice([0,1,2],p=[.22,.57,.21])):
        cx = rng.choice([rng.uniform(.025,.15),rng.uniform(.84,.975),rng.uniform(.20,.80)])
        notch = np.maximum(1-np.abs(x-cx)/rng.uniform(.025,.11),0)
        retreat += notch**1.35*rng.uniform(.005,.022)
    retreat += distress*.003
    edge = (1-smooth(0,.15,np.minimum(x,1-x)))
    worn = np.maximum((1-smooth(0,.13,y))*(.28+.72*edge_noise), edge*.28)
    abrasion = smooth(.55,.79,noise(x*5+j,y*6,seed+13)) * (.25+.75*noise(shear*12,y*5,seed+14))
    tool_mark = np.zeros_like(x)
    if rng.random()<.52:
        tx, ty = rng.uniform(.2,.8), rng.uniform(.13,.52)
        footprint = (1-smooth(.45,1,np.abs(x-tx)/rng.uniform(.09,.24)))
        stroke = y-ty-.15*(x-tx)
        tool_mark = footprint*(1-smooth(.001,.013,np.abs(stroke))) * rng.uniform(.35,1)

    thickness = rng.uniform(.079,.128)*EXPOSURE
    crown = (1-(2*x-1)**2)*rng.uniform(.0017,.0045)
    cup = rng.uniform(-.004,.005)*(2*x-1)**2*(1-.78*y)
    twist = rng.uniform(-.009,.009)*(x-.5)*(1-y)**1.8
    ridge = .0029*(cleavage-.36) + .0015*(bundles-.5)
    wood_height = ridge - .0019*earlywood + .0012*(fine-.5) - .0006*pores - .0023*fissures
    damage = .0061*distress + .0040*core + .0033*tool_mark
    face = thickness * (1-.85*y) + (crown+wood_height)*(1-.45*y) + cup + twist - damage
    face -= (1-smooth(0,.027,np.minimum(x,1-x)))*.0026
    # One rounded arris, followed by a steep exposed end surface.
    bevel = 1-smooth(0,.031,y)
    face -= bevel*(.0036+.0019*edge_noise)
    end = t<=0
    face = np.where(end, np.maximum(.001,face*(1+t/.012)),face)
    actual_y = t*.369 + retreat*(1-smooth(0,.18,y))
    gap = rng.uniform(.0011,.0026)
    actual_x = gap + x*(width-2*gap)
    actual_x += .0017*(noise(x*5+j,y*4,seed+7)-.5)
    actual_x += (.0010+.0020*edge)*np.sin(y*4.7+j)

    base = np.array(rng.choice([
        [.275,.122,.052],[.313,.152,.065],[.222,.124,.070],
        [.230,.102,.050],[.294,.170,.095],[.160,.084,.040],
        [.270,.162,.105],[.208,.113,.066]], p=[.15,.17,.15,.12,.12,.08,.11,.10]))
    tone = .83+.23*bundles+.30*(long_fiber-.5)+.14*(fine-.5)-.22*earlywood-.145*pores
    rgb = base[None,None,:]*tone[:,:,None]
    greywood = np.array([.26,.200,.137])
    age = abrasion*rng.uniform(.12,.33)
    rgb = rgb*(1-age[:,:,None])+greywood*age[:,:,None]
    pale = np.array([.38,.231,.115])
    exposed = np.clip(worn*.66 + .44*tool_mark + .21*torn_flank + (.30+.14*edge_noise)*end,0,.86)
    rgb = rgb*(1-exposed[:,:,None])+pale*exposed[:,:,None]*(.70+.50*fine[:,:,None])
    endgrain = noise(shear*63+j,(face/.006),seed+30)
    rgb *= np.where(end,.70+.51*endgrain,1)[:,:,None]
    rgb *= (1-.56*distress-.35*core-.28*fissures)[:,:,None]
    latewood = smooth(.55,.76,long_fiber) * (1-smooth(.76,.92,long_fiber))
    rgb *= (.94 + .16*latewood + .12*(bundles-.5))[:,:,None]
    rough = np.clip(.70 + .17*earlywood + .10*pores+.11*abrasion-.15*worn+.10*distress+.09*fissures-.10*torn_flank-.07*tool_mark,.48,.94)
    xyz=np.stack((actual_x,actual_y,face),axis=-1)
    local=np.stack((shear*width+j*.034,actual_y+j*.028,face),axis=-1)
    # Sample both sidewalls. The slight outward slope is visible to a
    # top-down projection and preserves a narrow physical side joint.
    left,right=xyz[:,0:1].copy(),xyz[:,-1:].copy()
    left[:,:,0]-=.00075
    right[:,:,0]+=.00075
    left[:,:,2]=right[:,:,2]=.001
    xyz=np.concatenate((left,xyz,right),axis=1)
    rgb=np.concatenate((rgb[:,0:1]*.77,rgb,rgb[:,-1:]*.77),axis=1)
    rough=np.concatenate((rough[:,0:1],rough,rough[:,-1:]),axis=1)
    local=np.concatenate((local[:,0:1],local,local[:,-1:]),axis=1)
    return xyz,rgb,rough,local


def roof_mesh(detail, spherical=False):
    xyz, colors, roughness, fiber_coords, polygons = [], [], [], [], []
    offset = 0
    for row in (range(1,9) if spherical else range(10)):
        starts = COURSES[-1-row%8]
        spans = [(j, starts[(i+1)%len(starts)]+(1024 if i+1==len(starts) else 0))
                 for i,j in enumerate(starts)]
        for index,(begin,end) in enumerate(spans):
            vertices, rgb, rough, local = shingle((end-begin)/1024*WIDTH, 7001+(row%8)*103+index*17, detail)
            rows,cols = vertices.shape[:2]
            for repeat in ((0,1,2) if spherical else (-1,0,1)):
                start_x = (begin/1024+repeat)*WIDTH
                if not spherical and (start_x > WIDTH+.028 or start_x+(end-begin)/1024*WIDTH < -.010):
                    continue
                coords = vertices + (start_x, (row-1)*EXPOSURE, 0)
                if spherical:
                    lon=coords[:,:,0]*(2*np.pi/(WIDTH*3))
                    lat=(np.clip(coords[:,:,1]/LENGTH,.001,.999)-.5)*np.pi
                    radius=.71+coords[:,:,2]
                    coords=np.stack((radius*np.cos(lat)*np.cos(lon),
                                     radius*np.cos(lat)*np.sin(lon),
                                     radius*np.sin(lat)),axis=-1)
                xyz.append(coords.reshape(-1,3).astype(np.float32))
                colors.append(np.column_stack((rgb.reshape(-1,3),np.ones(rows*cols))).astype(np.float32))
                roughness.append(rough.ravel().astype(np.float32))
                fiber_coords.append(local.reshape(-1,3).astype(np.float32))
                quads = np.arange((rows-1)*cols,dtype=np.int32).reshape(rows-1,cols)[:,:-1].ravel()+offset
                polygons.append(np.column_stack((quads,quads+1,quads+cols+1,quads+cols)))
                offset += rows*cols

    # The roof deck is visible only through joints. Include it in the bake
    # so that gaps do not pick up a zero normal or show daylight in the source.
    if not spherical:
        xyz.append(np.array([(-.10,-.40,.0005),(WIDTH+.10,-.40,.0005),
                             (WIDTH+.10,LENGTH+.40,.0005),(-.10,LENGTH+.40,.0005)],np.float32))
        polygons.append(np.array([[offset,offset+1,offset+2,offset+3]],np.int32))
        colors.append(np.tile([.041,.024,.011,1.],(4,1)).astype(np.float32))
        roughness.append(np.full(4,.86,np.float32))
        fiber_coords.append(np.zeros((4,3),np.float32))
    xyz,polygons,colors,roughness,fiber_coords = map(np.concatenate,(xyz,polygons,colors,roughness,fiber_coords))
    mesh = bpy.data.meshes.new("Registered overlapping riven boards")
    mesh.vertices.add(len(xyz))
    mesh.vertices.foreach_set("co",xyz.ravel())
    mesh.loops.add(polygons.size)
    mesh.loops.foreach_set("vertex_index",polygons.ravel())
    mesh.polygons.add(len(polygons))
    mesh.polygons.foreach_set("loop_start",np.arange(0,polygons.size,4,dtype=np.int32))
    mesh.polygons.foreach_set("use_smooth",np.ones(len(polygons),bool))
    c = mesh.color_attributes.new(name="Timber reflectance",type="FLOAT_COLOR",domain="POINT")
    c.data.foreach_set("color",colors.ravel())
    r = mesh.attributes.new(name="Timber roughness",type="FLOAT",domain="POINT")
    r.data.foreach_set("value",roughness)
    f = mesh.attributes.new(name="Fiber coordinates",type="FLOAT_VECTOR",domain="POINT")
    f.data.foreach_set("vector",fiber_coords.ravel())
    mesh.update(calc_edges=True)
    obj = bpy.data.objects.new("Riven Brookoak bake source",mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def shader(obj):
    mat = bpy.data.materials.new("Brookoak timber")
    mat.use_nodes=True
    obj.data.materials.append(mat)
    n,l = mat.node_tree.nodes, mat.node_tree.links
    bsdf = n.get("Principled BSDF")
    pigment = n.new("ShaderNodeVertexColor")
    pigment.layer_name = "Timber reflectance"
    rough = n.new("ShaderNodeAttribute")
    rough.attribute_name="Timber roughness"
    # Board-local shallow fibers retain sub-mesh detail in the tangent bake.
    # They follow the board's length. A separate coordinate stretch across
    # the end grain limits continuous stripes on the end face.
    coord = n.new("ShaderNodeAttribute")
    coord.attribute_name="Fiber coordinates"
    stretch = n.new("ShaderNodeVectorMath")
    stretch.operation = "MULTIPLY"
    stretch.inputs[1].default_value = (360, 24, 118)
    l.new(coord.outputs["Vector"], stretch.inputs[0])
    fibers = n.new("ShaderNodeTexNoise")
    fibers.inputs["Scale"].default_value = 1
    fibers.inputs["Detail"].default_value = 2.3
    l.new(stretch.outputs[0], fibers.inputs["Vector"])
    bump = n.new("ShaderNodeBump")
    bump.inputs["Distance"].default_value = .00085
    bump.inputs["Strength"].default_value = .60
    l.new(fibers.outputs["Fac"], bump.inputs["Height"])
    l.new(bump.outputs[0], bsdf.inputs["Normal"])
    tint = n.new("ShaderNodeMixRGB")
    tint.blend_type="MULTIPLY"
    tint.inputs[0].default_value=.31
    l.new(pigment.outputs["Color"],tint.inputs[1])
    l.new(fibers.outputs["Fac"],tint.inputs[2])
    l.new(tint.outputs[0],bsdf.inputs["Base Color"])
    l.new(rough.outputs["Fac"],bsdf.inputs["Roughness"])
    return n,l,bsdf,tint


def plane():
    mesh=bpy.data.meshes.new("1.28 m by 2.40 m roof UV tile")
    mesh.from_pydata([(0,0,0),(WIDTH,0,0),(WIDTH,LENGTH,0),(0,LENGTH,0)],[],[(0,1,2,3)])
    uv=mesh.uv_layers.new(name="RoofUV")
    for i,coord in enumerate(((0,0),(1,0),(1,1),(0,1))):
        uv.data[i].uv=coord
    obj=bpy.data.objects.new("Bake target",mesh)
    bpy.context.collection.objects.link(obj)
    mat=bpy.data.materials.new("Bake target")
    mat.use_nodes=True
    obj.data.materials.append(mat)
    return obj,mat.node_tree.nodes.new("ShaderNodeTexImage")


def bake(scene, hi, source, size):
    lo,target = plane()
    bpy.ops.object.select_all(action="DESELECT")
    hi.select_set(True)
    lo.select_set(True)
    bpy.context.view_layer.objects.active=lo
    n,l,bsdf,pigment=source
    out=n.get("Material Output")
    emit=n.new("ShaderNodeEmission")
    pos=n.new("ShaderNodeNewGeometry")
    sep=n.new("ShaderNodeSeparateXYZ")
    l.new(pos.outputs["Position"],sep.inputs[0])
    remap=n.new("ShaderNodeMath")
    remap.operation="DIVIDE"
    remap.inputs[1].default_value=HEIGHT_RANGE
    l.new(sep.outputs["Z"],remap.inputs[0])
    texture = {}
    for label, kind in (("albedo","EMIT"),("normal","NORMAL"),("rough","ROUGHNESS"),("displace","EMIT")):
        l.new(bsdf.outputs[0],out.inputs[0])
        if label in ("albedo","displace"):
            signal=pigment.outputs[0] if label=="albedo" else remap.outputs[0]
            l.new(signal,emit.inputs["Color"])
            l.new(emit.outputs[0],out.inputs[0])
        im=bpy.data.images.new(label,width=size,height=size,alpha=False,float_buffer=True)
        im.colorspace_settings.name="Linear Rec.709" if label=="albedo" else "Non-Color"
        target.image=im
        lo.active_material.node_tree.nodes.active=target
        bpy.ops.object.bake(type=kind,use_selected_to_active=True,cage_extrusion=.085,
                           max_ray_distance=.13,normal_space="TANGENT",margin=0)
        texture[label]=im
        print("Baked",label,flush=True)
    l.new(bsdf.outputs[0],out.inputs[0])
    bpy.data.objects.remove(lo,do_unlink=True)
    return texture


def raw(im):
    data=np.empty(len(im.pixels),np.float32)
    im.pixels.foreach_get(data)
    return data.reshape(im.size[1],im.size[0],4)


def publish(scene, images):
    settings=scene.render.image_settings
    for label,im in images.items():
        if label=="normal":
            # Uncovered side joints represent a flat, recessed undercourse.
            pix=raw(im)
            holes=np.max(pix[:,:,:3],axis=-1)<.1
            pix[holes,:3]=(.5,.5,1)
            im.pixels.foreach_set(pix.ravel())
        if label=="albedo":
            pix=raw(im)
            holes=np.max(pix[:,:,:3],axis=-1)<.001
            pix[holes,:3]=(.045,.025,.012)
            im.pixels.foreach_set(pix.ravel())
        if label=="rough":
            pix=raw(im)
            holes=pix[:,:,0]<.05
            pix[holes,:3]=.87
            im.pixels.foreach_set(pix.ravel())
        suffix="png" if label in ("albedo","normal") else "exr"
        dest=ROOT/f"{STEM}_{label}.{suffix}"
        if label=="albedo":
            scene.view_settings.view_transform="Standard"
            scene.view_settings.look="None"
            scene.render.image_settings.file_format="PNG"
            scene.render.image_settings.color_depth="8"
            im.save_render(str(dest),scene=scene)
            scene.view_settings.view_transform="AgX"
        elif label=="normal":
            im.filepath_raw=str(dest)
            im.file_format="PNG"
            im.save()
        else:
            settings.file_format="OPEN_EXR"
            settings.color_mode="RGB"
            settings.color_depth="16"
            settings.exr_codec="ZIP"
            im.save_render(str(dest),scene=scene)


def aim(obj,loc,target):
    obj.location=loc
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat("-Z","Y").to_euler()


def review(scene,hi,source):
    world=scene.world=bpy.data.worlds.new("Neutral sky")
    world.use_nodes=True
    world.node_tree.nodes["Background"].inputs[0].default_value=(.49,.58,.69,1)
    world.node_tree.nodes["Background"].inputs[1].default_value=.33
    bpy.ops.object.camera_add()
    cam=scene.camera=bpy.context.object
    cam.data.type="ORTHO"
    bpy.ops.object.light_add(type="SUN")
    sun=bpy.context.object
    sun.data.energy=3.15
    sun.data.angle=.09
    _,l,bsdf,pigment=source
    scene.cycles.samples=24
    scene.cycles.use_denoising=True
    scene.render.resolution_x=1100
    scene.render.resolution_y=900
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.image_settings.color_mode="RGB"
    scene.render.image_settings.color_depth="8"
    target=(.65,1.18,.01)
    aim(cam,(1.51,-.92,1.92),target)
    cam.data.ortho_scale=1.55
    aim(sun,(-3,-4,3.2),(0,0,0))
    scene.render.filepath=str(ROOT/f"{STEM}_close.png")
    bpy.ops.render.render(write_still=True)
    node=bsdf.inputs["Base Color"]
    l.remove(node.links[0])
    node.default_value=(.32,.32,.32,1)
    scene.render.filepath=str(ROOT/f"{STEM}_clay.png")
    bpy.ops.render.render(write_still=True)
    aim(sun,(3,-1.7,2.3),(0,0,0))
    scene.render.filepath=str(ROOT/f"{STEM}_clay_reversed.png")
    bpy.ops.render.render(write_still=True)
    l.new(pigment.outputs[0],node)
    hi.hide_render=True
    flat,_=plane()
    mat=flat.active_material
    n,l=mat.node_tree.nodes,mat.node_tree.links
    bsdf=n.get("Principled BSDF")
    uv=n.new("ShaderNodeUVMap")
    uv.uv_map="RoofUV"
    for key,suffix,fac in (("albedo","png","Base Color"),("rough","exr","Roughness"),("normal","png","Normal")):
        im=bpy.data.images.load(str(ROOT/f"{STEM}_{key}.{suffix}"),check_existing=False)
        im.colorspace_settings.name="sRGB" if key=="albedo" else "Non-Color"
        tex=n.new("ShaderNodeTexImage")
        tex.image=im
        tex.extension="REPEAT"
        l.new(uv.outputs["UV"],tex.inputs["Vector"])
        if key=="normal":
            nm=n.new("ShaderNodeNormalMap")
            nm.uv_map="RoofUV"
            l.new(tex.outputs["Color"],nm.inputs["Color"])
            l.new(nm.outputs["Normal"],bsdf.inputs[fac])
        else:
            l.new(tex.outputs["Color"],bsdf.inputs[fac])
    aim(sun,(-3,-4,3.2),(0,0,0))
    scene.render.filepath=str(ROOT/f"{STEM}_flat.png")
    bpy.ops.render.render(write_still=True)
    flat.hide_render=True

    def attach(obj):
        obj.data.materials.append(mat)
        obj.data.uv_layers.active.name="RoofUV"

    bpy.ops.mesh.primitive_plane_add(size=1)
    obj=bpy.context.object
    attach(obj)
    obj.scale=(6.4,3.55,1)
    obj.rotation_euler.x=.45
    for loop in obj.data.uv_layers.active.data:
        loop.uv.x *= 6.4/WIDTH
        loop.uv.y *= 3.55/LENGTH
    aim(cam,(3.8,-11,5.7),(0,0,0))
    cam.data.ortho_scale=8.2
    scene.render.resolution_y=650
    scene.render.filepath=str(ROOT/f"{STEM}_roof.png")
    bpy.ops.render.render(write_still=True)
    obj.hide_render=True

    bpy.ops.mesh.primitive_uv_sphere_add(segments=512,ring_count=384,radius=.71)
    obj=bpy.context.object
    attach(obj)
    for polygon in obj.data.polygons:
        polygon.use_smooth=True
    # Sample height along sphere UVs for a diagnostic displaced material sphere.
    # This single continuous sphere has the same projection limits as a flat field.
    depth=bpy.data.images.load(str(ROOT/f"{STEM}_displace.exr"),check_existing=False)
    pixels=raw(depth)[:,:,0]
    coordinate=np.zeros((len(obj.data.vertices),2),np.float64)
    vertex_index=np.empty(len(obj.data.loops),np.int32)
    obj.data.loops.foreach_get("vertex_index",vertex_index)
    uvs=np.empty(len(vertex_index)*2,np.float32)
    uv_data=obj.data.uv_layers.active.data
    uv_data.foreach_get("uv",uvs)
    uvs=uvs.reshape(-1,2)
    uvs[:,0]*=3
    uv_data.foreach_set("uv",uvs.ravel())
    coordinate[vertex_index]=uvs
    samples=coordinate*np.array([depth.size[0],depth.size[1]])-.5
    cells=np.floor(samples).astype(int)
    u,v=cells.T
    tx,ty=(samples-cells).T
    h,w=pixels.shape
    top=(1-tx)*pixels[v%h,u%w]+tx*pixels[v%h,(u+1)%w]
    bottom=(1-tx)*pixels[(v+1)%h,u%w]+tx*pixels[(v+1)%h,(u+1)%w]
    z=((1-ty)*top+ty*bottom)*HEIGHT_RANGE
    coordinates=np.empty(len(obj.data.vertices)*3,np.float32)
    obj.data.vertices.foreach_get("co",coordinates)
    coordinates=coordinates.reshape(-1,3)
    coordinates *= (1+z/.71)[:,None]
    obj.data.vertices.foreach_set("co",coordinates.ravel())
    obj.data.update()
    nm.inputs["Strength"].default_value=.48
    aim(cam,(.11,-3.2,.75),(0,0,0))
    cam.data.ortho_scale=1.64
    aim(sun,(4,-4,5),(0,0,0))
    scene.render.resolution_x=900
    scene.render.resolution_y=900
    scene.render.filepath=str(ROOT/f"{STEM}_sphere.png")
    bpy.ops.render.render(write_still=True)
    obj.hide_render=True
    modeled_sphere(scene,cam,sun)


def modeled_sphere(scene,cam,sun):
    shell=roof_mesh(64,spherical=True)
    shader(shell)
    aim(cam,(.11,-3.2,.75),(0,0,0))
    cam.data.ortho_scale=1.64
    aim(sun,(4,-4,5),(0,0,0))
    scene.render.resolution_x=1000
    scene.render.resolution_y=1000
    scene.cycles.samples=32
    scene.cycles.use_denoising=True
    scene.render.filepath=str(ROOT/f"{STEM}_sphere_modeled.png")
    bpy.ops.render.render(write_still=True)



def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--size",type=int,default=2048)
    parser.add_argument("--mesh-detail",type=int,default=112)
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument("--bake-only",action="store_true")
    mode.add_argument("--sphere-only",action="store_true")
    parser.add_argument("--verify-repeat",action="store_true",help="Rebake and check pixel equality before publishing")
    args=parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc=bpy.context.scene
    sc.render.engine="CYCLES"
    sc.cycles.device="CPU"
    sc.cycles.samples=1
    sc.view_settings.view_transform="AgX"
    if args.sphere_only:
        world=sc.world=bpy.data.worlds.new("Neutral sky")
        world.use_nodes=True
        bg=world.node_tree.nodes["Background"]
        bg.inputs[0].default_value=(.49,.58,.69,1)
        bg.inputs[1].default_value=.33
        bpy.ops.object.camera_add()
        cam=sc.camera=bpy.context.object
        cam.data.type="ORTHO"
        bpy.ops.object.light_add(type="SUN")
        sun=bpy.context.object
        sun.data.energy=3.15
        sun.data.angle=.09
        sc.render.resolution_percentage=100
        sc.render.image_settings.file_format="PNG"
        modeled_sphere(sc,cam,sun)
        return
    hi=roof_mesh(args.mesh_detail)
    nodes=shader(hi)
    print("Bake source faces",len(hi.data.polygons),flush=True)
    maps=bake(sc,hi,nodes,args.size)
    if args.verify_repeat:
        repeat=bake(sc,hi,nodes,args.size)
        for key,value in maps.items():
            a,b=raw(value),raw(repeat[key])
            if not np.array_equal(a,b):
                raise RuntimeError(f"{key} bake changed on repeat (max delta {np.max(np.abs(a-b))})")
            print("Repeat bake matches pixels:",key,flush=True)
            bpy.data.images.remove(repeat[key])
    publish(sc,maps)
    if not args.bake_only:
        review(sc,hi,nodes)


if __name__=="__main__":
    main()
