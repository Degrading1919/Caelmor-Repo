"""Construct and bake a periodic Lowmark rubble wall in Blender 5.0.1.

Run with Blender --background --python build_lowmark_fieldstone.py.
Use -- --draft for clay-only look development, or -- --verify-repeat for release QA.
The wall is constructed in XY, with +Z toward the exposed face.
"""
from argparse import ArgumentParser
import csv
from pathlib import Path
import sys

import bpy
from mathutils import Matrix, Vector
import numpy as np

ROOT = Path(__file__).resolve().parent
NAME = "Lowmark_Fieldstone_Masonry"
U, V = 2.40, 1.80
RELIEF = .096
SEED = 41492
ROCKS = np.array([
    [.230, .213, .177], [.176, .174, .151], [.301, .272, .220],
    [.206, .187, .157], [.275, .240, .203], [.142, .153, .144],
    [.220, .185, .149], [.267, .256, .229],
])


def smooth(lo, hi, x):
    t = np.clip((x - lo) / (hi - lo), 0, 1)
    return t * t * (3 - 2 * t)


def field(x, y, seed, period=None):
    i, j = np.floor(x), np.floor(y)
    a, b = smooth(0, 1, x - i), smooth(0, 1, y - j)

    def at(dx, dy):
        a, b = i+dx, j+dy
        if period is not None:
            a, b = a % period[0], b % period[1]
        value = np.sin(a*127.1 + b*311.7 + seed*19.27) * 43758.5453
        return value - np.floor(value)

    return (1-b)*((1-a)*at(0,0)+a*at(1,0)) + b*((1-a)*at(0,1)+a*at(1,1))


def clipped(poly, axis, limit):
    """Intersect a convex cell with a half plane."""
    if not len(poly):
        return poly
    dist = poly @ axis - limit
    result = []
    for i, b in enumerate(poly):
        a = poly[i-1]
        p, q = dist[i-1], dist[i]
        if (p < 0) != (q < 0):
            result.append(a + (b-a) * p/(p-q))
        if q <= 0:
            result.append(b)
    return np.asarray(result)


def layout():
    # Loose bed heights. Vary the rise and stagger, then fit individual
    # stones with a periodic power diagram instead of continuous mortar rails.
    beds = [
        (.09, [.02, .21, .37, .54, .72, .91]),
        (.24, [.12, .31, .49, .64, .82]),
        (.40, [.01, .18, .36, .58, .75, .94]),
        (.57, [.11, .26, .43, .62, .84]),
        (.74, [.00, .20, .38, .55, .70, .92]),
        (.90, [.09, .29, .46, .64, .83]),
    ]
    rng = np.random.default_rng(SEED)
    positions = []
    for y, xs in beds:
        for x in xs:
            positions.append(((x*U+rng.uniform(-.074,.074))%U,
                              (y*V+rng.uniform(-.077,.077))%V))
    centers = np.asarray(positions)
    weights = rng.uniform(-.020,.031,len(centers))
    scale = np.array([.77,1.])
    period = np.array([U,V])
    copies = [(centers+period*(i,j))*scale for i in (-1,0,1) for j in (-1,0,1)]
    all_centers = np.concatenate(copies)
    all_weights = np.tile(weights,9)
    stones = []
    for ident,(center,weight) in enumerate(zip(centers*scale,weights)):
        poly = center + np.array([[-1,-1],[1,-1],[1,1],[-1,1]])*period
        for other, w in zip(all_centers,all_weights):
            delta = other-center
            if np.dot(delta,delta) < 1e-10:
                continue
            cut = np.dot(delta,(other+center)*.5) + (weight-w)*.5
            poly = clipped(poly,delta,cut)
        if len(poly) < 3:
            raise RuntimeError(f"Stone cell {ident} vanished")
        poly = poly/scale
        # A subset has a separate thin pinning stone against its shoulder.
        if ident in (2, 5, 10, 14, 18, 23, 28, 31):
            axis = np.array([rng.uniform(-.8,.8),rng.choice([-1.,1.])])
            support = poly @ axis
            mark = np.quantile(support,.72)
            main = clipped(poly,axis,mark)
            pin = clipped(poly,-axis,-mark)
            if min(len(main),len(pin)) >= 3:
                stones.append((main,"fieldstone"))
                stones.append((pin,"pinning stone"))
                continue
        stones.append((poly,"fieldstone"))
    return stones


def stone_mesh(poly, role, ident):
    rng = np.random.default_rng(SEED+1009*(ident+1))
    center = poly.mean(axis=0)
    footprint = poly-center
    angles = np.linspace(0,2*np.pi,112,endpoint=False)
    directions = np.column_stack((np.cos(angles),np.sin(angles)))
    edges = np.roll(footprint,-1,axis=0)-footprint
    normals = np.column_stack((edges[:,1],-edges[:,0]))
    limits = np.einsum("ij,ij->i",normals,footprint)
    denom = directions @ normals.T
    ratios = np.divide(limits,denom,out=np.full_like(denom,np.inf),where=denom>1e-9)
    radius = np.min(ratios,axis=1)
    rolling = (np.roll(radius,4)+np.roll(radius,-4))*.5
    radius = np.minimum(radius,radius*rng.uniform(.78,.94)+rolling*.15)
    radius -= rng.uniform(.006,.014) + .004*np.sin(5*angles+rng.uniform(0,7))
    radius += .004*np.sin(11*angles+rng.uniform(0,7))
    radius = np.maximum(.012,radius)
    busted = rng.uniform(0,2*np.pi)
    radial_loss = np.maximum(np.cos(angles-busted),0)**20*rng.uniform(.004,.031)
    radius = np.maximum(.010,radius-radial_loss)
    outline = directions*radius[:,None]
    fractions = np.r_[np.linspace(.004,.85,32),[.89,.92,.945,.964,.983,1.]]
    f = fractions[:,None]
    xy = center+f[:,:,None]*outline[None,:,:]
    x,y = (xy-center).transpose(2,0,1)
    base = rng.uniform(.041,.076) if role=="fieldstone" else rng.uniform(.027,.044)
    facet = base + rng.uniform(-.094,.094)*x + rng.uniform(-.11,.11)*y
    for _ in range(5):
        direction = rng.uniform(0,2*np.pi)
        axis = np.cos(direction)*x + np.sin(direction)*y
        limit = base + rng.uniform(.014,.035) - rng.uniform(.14,.29)*axis
        facet = np.minimum(facet,limit)
    fracture_axis = rng.uniform(-1.4,1.4)
    along = x*np.cos(fracture_axis)+y*np.sin(fracture_axis)
    cross = -x*np.sin(fracture_axis)+y*np.cos(fracture_axis)
    run = field(along*12,cross*38,ident+11)
    strata = smooth(.37,.53,run)-.60*smooth(.70,.87,run)
    cleft = np.zeros_like(x)
    if rng.random()<.65:
        line = cross-rng.uniform(-.06,.062)-.13*along
        crooked = (field(along*25,np.zeros_like(along),ident+5)-.5)*.014
        cut_width = rng.uniform(.003,.009)
        active = 1-smooth(.045,.14,np.abs(along-rng.uniform(-.07,.07)))
        cleft = (1-smooth(.20,1,np.abs(line+crooked)/cut_width))*active
        facet -= rng.uniform(.006,.019)*cleft
    pitted = smooth(.63,.87,field(x*95,y*95,ident+19))
    broken = field(x*34,y*31,ident+23)
    bedding = rng.uniform(.0014,.0105)
    facet += bedding*(strata-.35)+rng.uniform(.003,.009)*(broken-.50)-.0046*pitted
    shoulder = smooth(rng.uniform(.67,.86),1,f)
    bed = .006 + .004*field(x*34,y*32,ident+7)
    z = facet*(1-shoulder) + bed*shoulder
    z += np.sin(angles*7+ident)[None,:]*.004*shoulder*(1-shoulder)
    z = np.clip(z,.003,.094)
    hue = ROCKS[rng.integers(len(ROCKS))]*rng.uniform(.87,1.10)
    vein = smooth(.47,.56,run)*(1-smooth(.57,.73,run))
    hue_field = hue[None,None,:]*(.88+.21*broken+.115*vein-.16*pitted-.08*cleft)[:,:,None]
    stain = smooth(.59,.81,field(x*8.8,y*12.7,ident+69))*(.25+.75*broken)
    age_hue = np.array([.165,.154,.112])
    hue_field = hue_field*(1-stain[:,:,None]*.38)+age_hue*stain[:,:,None]*.38
    rough = np.clip(.72 + .098*pitted + .105*broken - .11*vein + .04*stain,.59,.96)
    local = xy-center
    points = np.dstack((xy,z))
    sample = np.dstack((local+np.array([ident*2.31,ident*.51]),z))
    return points,hue_field,rough,sample,center+outline


def mortar_signals(u,v):
    su,sv = 2*np.pi*u/U,2*np.pi*v/V
    broad=field(u/U*43,v/V*33,86,(43,33))
    sand=field(u/U*135,v/V*97,92,(135,97))
    wiped=field(u/U*31,v/V*89,162,(31,89))
    bumps = .85*(broad-.5)+.40*(sand-.5)+.18*(wiped-.5)
    daub = .57*broad+.26*wiped+.17*sand
    hue = np.array([.256,.235,.203])*(.82+.31*daub)[...,None]
    height = .008 + .0036*bumps
    rough = np.clip(.86+.08*bumps,.71,.98)
    coord = np.stack(((U/(2*np.pi))*np.sin(su),(U/(2*np.pi))*np.cos(su),
                      (V/(2*np.pi))*np.sin(sv)),axis=-1)
    return height,hue,rough,coord


def wall():
    vertices, faces, pigment, rough, coords, sample_w, mortar = [], [], [], [], [], [], []
    layout_records = []
    offset = 0

    def append(points, color, r, sample, weight, wrap=False):
        nonlocal offset
        rows,cols = points.shape[:2]
        vertices.append(points.reshape(-1,3).astype(np.float32))
        pigment.append(np.column_stack((color.reshape(-1,3),np.ones(rows*cols))).astype(np.float32))
        rough.append(r.ravel().astype(np.float32))
        coords.append(sample.reshape(-1,3).astype(np.float32))
        w = (V/(2*np.pi))*np.cos(points[:,:,1]*(2*np.pi/V)) if weight else np.zeros((rows,cols))
        sample_w.append(w.ravel().astype(np.float32))
        mortar.append(np.full(rows*cols,weight,np.float32))
        columns = cols if wrap else cols-1
        start = np.arange((rows-1)*cols).reshape(rows-1,cols)[:,:columns]
        nxt = np.roll(np.arange(cols),-1)[:columns]+(start//cols)*cols
        face = np.stack((start,nxt,nxt+cols,start+cols),axis=-1)
        if wrap:
            face=face[:,:,::-1] # center-to-edge rings have the opposite winding
        faces.append(face.reshape(-1,4).astype(np.int32)+offset)
        offset += rows*cols

    # Bed samples repeat at an exact integer grid interval. Mortar rises
    # selectively where a trowel has packed it against a stone's rim.
    spacing = U/360
    x,y = np.meshgrid(np.arange(-15,376)*spacing,np.arange(-15,286)*spacing)
    z,mortar_hue,mortar_rough,mortar_coord = mortar_signals(x,y)
    shoulder_field = np.zeros_like(z)
    for ident,(poly,role) in enumerate(layout()):
        pos,hue,r,coord,outline = stone_mesh(poly,role,ident)
        center = poly.mean(axis=0)
        layout_records.append((ident,role,*center,float(np.max(pos[:,:,2])),outline))
        for ix in (-1,0,1):
            for iy in (-1,0,1):
                displacement = (ix*U,iy*V,0)
                current = pos+displacement
                if (current[:,:,0].max() < -.052 or current[:,:,0].min() > U+.052
                    or current[:,:,1].max() < -.052 or current[:,:,1].min() > V+.052):
                    continue
                append(current,hue,r,coord,0,True)
                rim = outline+(ix*U,iy*V)
                mask = ((x>rim[:,0].min()-.039)&(x<rim[:,0].max()+.039)
                        &(y>rim[:,1].min()-.039)&(y<rim[:,1].max()+.039))
                if mask.any():
                    patch=np.column_stack((x[mask],y[mask]))
                    distance=np.full(len(patch),np.inf)
                    for a,b in zip(rim,np.roll(rim,-1,axis=0)):
                        vec=b-a
                        projection=np.clip(((patch-a)@vec)/max(vec@vec,1e-10),0,1)
                        distance=np.minimum(distance,np.linalg.norm(patch-a-projection[:,None]*vec,axis=1))
                    lift=(1-smooth(.008,.037,distance))*(.004+.009*field(
                          (x[mask]-ix*U)*17,(y[mask]-iy*V)*21,ident+87))
                    shoulder_field[mask]=np.maximum(shoulder_field[mask],lift)
    append(np.dstack((x,y,z+shoulder_field)),mortar_hue,mortar_rough,mortar_coord,1)
    points, quads, rgb, matte, uvw, w, masks = map(np.concatenate,(vertices,faces,pigment,rough,coords,sample_w,mortar))
    mesh=bpy.data.meshes.new("Shaped stones with continuous mortar bedding")
    mesh.vertices.add(len(points))
    mesh.vertices.foreach_set("co",points.ravel())
    mesh.loops.add(quads.size)
    mesh.loops.foreach_set("vertex_index",quads.ravel())
    mesh.polygons.add(len(quads))
    mesh.polygons.foreach_set("loop_start",np.arange(0,quads.size,4,dtype=np.int32))
    mesh.polygons.foreach_set("use_smooth",np.ones(len(quads),bool))
    mesh.color_attributes.new(name="Stone Reflectance",type="FLOAT_COLOR",domain="POINT").data.foreach_set("color",rgb.ravel())
    for name, kind, attr, data in (("Surface Roughness","FLOAT","value",matte),
                                   ("Mineral Sample","FLOAT_VECTOR","vector",uvw),
                                   ("Sample W","FLOAT","value",w),
                                   ("Mortar Coverage","FLOAT","value",masks)):
        mesh.attributes.new(name=name,type=kind,domain="POINT").data.foreach_set(attr,data.ravel())
    mesh.update(calc_edges=True)
    obj=bpy.data.objects.new("Lowmark Fieldstone source",mesh)
    bpy.context.collection.objects.link(obj)
    return obj,layout_records

def surface(name, baked_source):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes,links = material.node_tree.nodes,material.node_tree.links
    bsdf = nodes.get("Principled BSDF")

    def attr(label,output):
        node=nodes.new("ShaderNodeAttribute")
        node.attribute_name=label
        return node.outputs[output]

    def noise(vector, scale, detail):
        node=nodes.new("ShaderNodeTexNoise")
        node.inputs["Scale"].default_value=scale
        node.inputs["Detail"].default_value=detail
        links.new(vector,node.inputs["Vector"])
        if baked_source:
            node.noise_dimensions="4D"
            links.new(attr("Sample W","Fac"),node.inputs["W"])
        return node.outputs["Fac"]

    if baked_source:
        uv = attr("Mineral Sample","Vector")
        base = nodes.new("ShaderNodeVertexColor")
        base.layer_name="Stone Reflectance"
        color = base.outputs["Color"]
        rough = attr("Surface Roughness","Fac")
        mask = attr("Mortar Coverage","Fac")
    else:
        uv=nodes.new("ShaderNodeTexCoord").outputs["Object"]
        mineral=nodes.new("ShaderNodeValToRGB")
        ramps = mineral.color_ramp
        ramps.elements[0].color=(*ROCKS[5],1)
        ramps.elements[1].color=(*ROCKS[2],1)
        ramps.elements.new(.38).color=(*ROCKS[1],1)
        ramps.elements.new(.64).color=(*ROCKS[4],1)
        random=nodes.new("ShaderNodeObjectInfo")
        links.new(random.outputs["Random"],mineral.inputs[0])
        color=mineral.outputs[0]
        rough_map=nodes.new("ShaderNodeMapRange")
        rough_map.inputs["To Min"].default_value=.68
        rough_map.inputs["To Max"].default_value=.93
        links.new(noise(uv,40,2),rough_map.inputs["Value"])
        rough=rough_map.outputs[0]
        mask=None

    islands = noise(uv,73,3)
    grain = noise(uv,335,2)
    tone=nodes.new("ShaderNodeValToRGB")
    tone.color_ramp.elements[0].position=.17
    tone.color_ramp.elements[0].color=(.41,.43,.44,1)
    tone.color_ramp.elements[1].position=.81
    tone.color_ramp.elements[1].color=(1.49,1.43,1.34,1)
    links.new(islands,tone.inputs[0])
    tint=nodes.new("ShaderNodeMixRGB")
    tint.blend_type="MULTIPLY"
    tint.inputs[0].default_value=.53
    links.new(color,tint.inputs[1])
    links.new(tone.outputs[0],tint.inputs[2])
    links.new(tint.outputs[0],bsdf.inputs["Base Color"])
    links.new(rough,bsdf.inputs["Roughness"])
    fine=nodes.new("ShaderNodeBump")
    fine.inputs["Strength"].default_value=.66
    fine.inputs["Distance"].default_value=.0014
    links.new(grain,fine.inputs["Height"])
    chip=nodes.new("ShaderNodeBump")
    chip.inputs["Strength"].default_value=.48
    chip.inputs["Distance"].default_value=.0026
    links.new(islands,chip.inputs["Height"])
    links.new(fine.outputs[0],chip.inputs["Normal"])
    links.new(chip.outputs[0],bsdf.inputs["Normal"])
    return material,tint.outputs[0],mask


def tile_plane(width=U, height=V, repeats=(1.,1.)):
    mesh=bpy.data.meshes.new("Metric fieldstone UV")
    mesh.from_pydata([(0,0,0),(width,0,0),(width,height,0),(0,height,0)],[],[(0,1,2,3)])
    uv=mesh.uv_layers.new(name="UV0_Metric")
    for i,(u,v) in enumerate(((0,0),(1,0),(1,1),(0,1))):
        uv.data[i].uv=(u*repeats[0],v*repeats[1])
    obj=bpy.data.objects.new("Fieldstone surface",mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def pixels(image):
    p=np.empty(len(image.pixels),np.float32)
    image.pixels.foreach_get(p)
    return p.reshape(image.size[1],image.size[0],4)


def bake(scene, wall_obj, source, size):
    mat, color, mask = source
    plate=tile_plane()
    target_mat=bpy.data.materials.new("Bake receiver")
    target_mat.use_nodes=True
    plate.data.materials.append(target_mat)
    target=target_mat.node_tree.nodes.new("ShaderNodeTexImage")
    bpy.ops.object.select_all(action="DESELECT")
    plate.select_set(True)
    wall_obj.select_set(True)
    bpy.context.view_layer.objects.active=plate
    nodes,links=mat.node_tree.nodes,mat.node_tree.links
    output=nodes.get("Material Output").inputs["Surface"]
    principled=nodes.get("Principled BSDF").outputs[0]
    height=nodes.new("ShaderNodeSeparateXYZ")
    links.new(nodes.new("ShaderNodeNewGeometry").outputs["Position"],height.inputs[0])
    height_normalized=nodes.new("ShaderNodeMath")
    height_normalized.operation="DIVIDE"
    height_normalized.inputs[1].default_value=RELIEF
    links.new(height.outputs["Z"],height_normalized.inputs[0])
    emit=nodes.new("ShaderNodeEmission")
    results={}
    channels=(("albedo","EMIT",color),("normal","NORMAL",None),("rough","ROUGHNESS",None),
              ("height","EMIT",height_normalized.outputs[0]),("mortar","EMIT",mask))
    for label,kind,signal in channels:
        links.new(principled,output)
        if signal is not None:
            links.new(signal,emit.inputs[0])
            links.new(emit.outputs[0],output)
        img=bpy.data.images.new(label,size,size,alpha=False,float_buffer=True)
        img.colorspace_settings.name="Linear Rec.709" if label=="albedo" else "Non-Color"
        target.image=img
        target_mat.node_tree.nodes.active=target
        bpy.ops.object.bake(type=kind,use_selected_to_active=True,cage_extrusion=.132,
                           max_ray_distance=.20,normal_space="TANGENT",margin=0)
        results[label]=img
        print("Baked",label,flush=True)
    links.new(principled,output)
    for node in (emit,height_normalized,height):
        nodes.remove(node)
    bpy.data.objects.remove(plate,do_unlink=True)
    return results


def check(images, repeat=None):
    for label,im in images.items():
        a=pixels(im)[:,:,:3]
        if repeat is not None:
            np.testing.assert_array_equal(a,pixels(repeat[label])[:,:,:3],err_msg=label)
        if not np.all(np.isfinite(a)):
            raise RuntimeError(f"Non-finite pixels in {label}")
        if label=="normal":
            length=np.linalg.norm(a*2-1,axis=2)
            if np.max(np.abs(length-1))>.025:
                raise RuntimeError("Normal bake has missing or invalid samples")
        else:
            if a.min() < -.001 or a.max() > 1.001:
                raise RuntimeError(f"Out-of-range {label}")
        jumps=[]
        for axis in (0,1):
            seam=float(np.abs(np.take(a,0,axis)-np.take(a,-1,axis)).mean())
            body=np.abs(np.diff(a,axis=axis)).mean(axis=tuple(i for i in range(3) if i!=axis))
            jumps.append((round(seam,4),round(float(np.percentile(body,95)),4),
                          round(float(body.max()),4)))
            if seam>max(float(body.max())*1.35,.006):
                raise RuntimeError(f"{label} has a wrap discontinuity on axis {axis}")
        print(label,"seam / interior p95 / interior max",jumps,flush=True)
    z=pixels(images["height"])[:,:,0]
    n=pixels(images["normal"])[:,:,:3]*2-1
    for channel,axis in enumerate((1,0)):
        signed=-np.roll(z,-1,axis=axis)+np.roll(z,1,axis=axis)
        score=np.corrcoef(signed.ravel(),n[:,:,channel].ravel())[0,1]
        if score<.20:
            raise RuntimeError(f"Normal and height disagree on axis {axis}: {score}")
        print("Signed normal-height alignment",axis,round(float(score),3),flush=True)
    print("Mortar coverage",round(float(pixels(images["mortar"])[:,:,0].mean()),3),flush=True)


def path(label):
    suffix="exr" if label in {"rough","height"} else "png"
    return ROOT/f"{NAME}_{label}.{suffix}"


def publish(scene, images):
    settings=scene.render.image_settings
    for label,im in images.items():
        settings.color_mode="RGB"
        if label=="albedo":
            scene.view_settings.view_transform="Standard"
            scene.view_settings.look="None"
            settings.file_format="PNG"
            settings.color_depth="8"
            im.save_render(str(path(label)),scene=scene)
            scene.view_settings.view_transform="AgX"
        elif label in {"normal","mortar"}:
            im.filepath_raw=str(path(label))
            im.file_format="PNG"
            im.save()
        else:
            settings.file_format="OPEN_EXR"
            settings.color_depth="16"
            settings.exr_codec="ZIP"
            im.save_render(str(path(label)),scene=scene)


def attach_bake(obj):
    mat=bpy.data.materials.new("Lowmark fieldstone wall bake")
    mat.use_nodes=True
    obj.data.materials.append(mat)
    nodes,links=mat.node_tree.nodes,mat.node_tree.links
    bsdf=nodes.get("Principled BSDF")
    for key,socket in (("albedo","Base Color"),("normal","Normal"),("rough","Roughness")):
        image=bpy.data.images.load(str(path(key)),check_existing=True)
        image.colorspace_settings.name="sRGB" if key=="albedo" else "Non-Color"
        tex=nodes.new("ShaderNodeTexImage")
        tex.image=image
        tex.extension="REPEAT"
        if key=="normal":
            nor=nodes.new("ShaderNodeNormalMap")
            nor.uv_map="UV0_Metric"
            links.new(tex.outputs["Color"],nor.inputs["Color"])
            links.new(nor.outputs[0],bsdf.inputs[socket])
        else:
            links.new(tex.outputs["Color"],bsdf.inputs[socket])


def aim(obj,location,target):
    obj.location=location
    back=(obj.location-Vector(target)).normalized()
    right=Vector((0,1,0)).cross(back).normalized()
    up=back.cross(right)
    obj.rotation_euler=Matrix((right,up,back)).transposed().to_euler()


def review(scene,obj,draft=False):
    world=scene.world=bpy.data.worlds.new("Neutral review environment")
    world.use_nodes=True
    bg=world.node_tree.nodes["Background"]
    bg.inputs[0].default_value=(.76,.82,.91,1)
    bg.inputs[1].default_value=.37
    bpy.ops.object.camera_add()
    camera=scene.camera=bpy.context.object
    camera.data.type="ORTHO"
    bpy.ops.object.light_add(type="SUN")
    light=bpy.context.object
    light.data.energy=2.9
    light.data.angle=.16
    scene.cycles.samples=16 if draft else 32
    scene.cycles.use_denoising=True
    scene.render.resolution_percentage=100
    scene.render.resolution_x=1200
    scene.render.resolution_y=945
    scene.render.image_settings.file_format="PNG"
    scene.render.image_settings.color_mode="RGB"
    scene.render.image_settings.color_depth="8"
    aim(camera,(1.63,-.42,3.34),(1.20,.90,.03))
    aim(light,(-3,1,3),(0,0,0))
    camera.data.ortho_scale=1.75
    source=obj.data.materials[0]
    clay=bpy.data.materials.new("Geometry review clay")
    clay.diffuse_color=(.42,.42,.42,1)
    obj.data.materials[0]=clay

    def capture(label):
        scene.render.filepath=str(path(label))
        bpy.ops.render.render(write_still=True)

    capture("clay")
    if draft:
        return
    aim(light,(3,-1,2.5),(0,0,0))
    capture("clay_reverse")
    obj.data.materials[0]=source
    aim(light,(-3,1,3),(0,0,0))
    capture("close")
    obj.hide_render=True
    panel=tile_plane()
    attach_bake(panel)
    capture("flat")
    panel.hide_render=True

    repeat=tile_plane(2*U,2*V,(2.,2.))
    attach_bake(repeat)
    aim(camera,(U,V,7),(U,V,0))
    camera.data.ortho_scale=2*U
    scene.render.resolution_x=1440
    scene.render.resolution_y=1080
    settings=scene.render.image_settings
    settings.file_format="JPEG"
    settings.quality=94
    scene.render.filepath=str(ROOT/f"{NAME}_repeat.jpg")
    bpy.ops.render.render(write_still=True)
    settings.file_format="PNG"
    scene.render.resolution_x=1200
    repeat.hide_render=True

    # A 5.6 m framed building elevation with a 1.05 m fieldstone plinth.
    def context_mat(name, rgb):
        ma=bpy.data.materials.new(name)
        ma.use_nodes=True
        shader=ma.node_tree.nodes.get("Principled BSDF")
        shader.inputs["Base Color"].default_value=(*rgb,1)
        shader.inputs["Roughness"].default_value=.92
        return ma

    def beam(location, dimensions, material):
        bpy.ops.mesh.primitive_cube_add(size=1,location=location)
        obj=bpy.context.object
        obj.dimensions=dimensions
        obj.data.materials.append(material)

    plaster=context_mat("Context lime plaster",(.54,.47,.37))
    timber=context_mat("Context oak sill",(.109,.063,.032))
    beam((2.8,1.32,-.14),(5.6,2.64,.24),plaster)
    beam((2.8,1.10,.026),(5.60,.17,.12),timber)
    for x in (.095,2.80,5.505):
        beam((x,1.88,.023),(.18,1.49,.105),timber)
    plinth=tile_plane(5.6,1.05,(5.6/U,1.05/V))
    attach_bake(plinth)
    plinth.location.z=.003
    beam((2.80,-.20,-.11),(6.5,.40,.60),context_mat("Context earth",(.20,.166,.122)))
    aim(camera,(4.25,1.95,8.1),(2.8,1.20,0))
    camera.data.ortho_scale=6.6
    aim(light,(-4,1,3),(0,0,0))
    scene.render.resolution_y=690
    capture("foundation")


def layout_csv(layout_records):
    # Store canonical unwrapped outlines. Translating by integer tile counts
    # gives the neighbor copies. IDs and order are stable for the given seed.
    with (ROOT/f"{NAME}_layout.csv").open("w",newline="",encoding="utf-8") as stream:
        writer=csv.writer(stream,lineterminator="\n")
        writer.writerow(("stone_id","role","center_u_m","center_v_m","face_peak_m",
                         "outline_index","outline_u_m","outline_v_m"))
        for ident,role,u,v,peak,outline in layout_records:
            for i,(x,y) in enumerate(outline):
                writer.writerow((ident,role,f"{u:.6f}",f"{v:.6f}",f"{peak:.6f}",
                                 i,f"{x:.6f}",f"{y:.6f}"))


def main():
    parser=ArgumentParser()
    parser.add_argument("--draft",action="store_true",help="Render neutral geometry only")
    parser.add_argument("--verify-repeat",action="store_true")
    parser.add_argument("--size",type=int,default=2048)
    args=parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene
    scene.render.engine="CYCLES"
    scene.cycles.samples=1
    scene.cycles.device="CPU"
    scene.view_settings.view_transform="AgX"
    obj,records=wall()
    source=surface("Fieldstone and lime mortar",True)
    obj.data.materials.append(source[0])
    print(f"Constructed {len(records)} stones and {len(obj.data.polygons)} faces",flush=True)
    if not args.draft:
        images=bake(scene,obj,source,args.size)
        repeat=bake(scene,obj,source,args.size) if args.verify_repeat else None
        check(images,repeat)
        if repeat:
            print("All five repeat bakes identical",flush=True)
        publish(scene,images)
        layout_csv(records)
        stone_only,_,_=surface("Lowmark Fieldstone | Stone Only",False)
        stone_only.use_fake_user=True
        bpy.data.libraries.write(str(ROOT/f"{NAME}_stone.blend"),{stone_only},
                                 fake_user=True,compress=True)
    review(scene,obj,args.draft)


if __name__=="__main__":
    main()
