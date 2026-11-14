"""Construct and bake Lowmark structural timber in Blender 5.0.1.

U follows the member. The side is a periodic planar projection in metres.
The end is a cross-section and is mapped once per exposed cap.
"""
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
import sys

import bpy
from mathutils import Vector
import numpy as np

ROOT = Path(__file__).resolve().parent
STEM = "Lowmark_Structural_Timber"
SEED = 61573
SIDE_SIZE = (4., 1.)
END_SIZE = (.36, .36)
SIDE_RELIEF = .022
END_RELIEF = .012


def ramp(a, b, x):
    t = np.clip((x-a)/(b-a), 0, 1)
    return t*t*(3-2*t)


def blend(a, b, weight):
    return a + (b-a)*weight[..., None]


def profile(u, v, nx, ny, seed, periodic=True):
    """Smooth value noise on a rectangular lattice, with optional wrap."""
    x, y = u*nx, v*ny
    i, j = np.floor(x), np.floor(y)
    fx, fy = ramp(0, 1, x-i), ramp(0, 1, y-j)

    def lattice(a, b):
        if periodic:
            a, b = a%nx, b%ny
        value = np.sin(a*127.1+b*311.7+seed*19.27)*43758.5453123
        return value-np.floor(value)

    low = (1-fx)*lattice(i,j)+fx*lattice(i+1,j)
    high = (1-fx)*lattice(i,j+1)+fx*lattice(i+1,j+1)
    return (1-fy)*low+fy*high


def around(value, center, span):
    return (value-center+span/2)%span-span/2


@dataclass(frozen=True)
class Wood:
    height: np.ndarray
    color: np.ndarray
    roughness: np.ndarray


class Timber:
    def __init__(self, seed, age):
        self.seed, self.age = seed, age
        rng = np.random.default_rng(seed)
        # Each mark has physical dimensions. Origins are spread across the
        # whole timber face, with room for quieter sections between clusters.
        knot_origins = ((.13,.34),(.44,.17),(.64,.71),(1.10,.43),(1.44,.87),
                        (1.76,.56),(2.03,.20),(2.40,.37),(2.65,.79),(3.04,.11),
                        (3.31,.62),(3.52,.41),(3.76,.94))
        self.knots = [(x+rng.uniform(-.08,.08), y+rng.uniform(-.025,.025),
                       rng.uniform(.024,.065),rng.uniform(.011,.032),
                       rng.uniform(-.14,.14),rng.uniform(.50,1.0))
                      for x,y in knot_origins]
        check_origins = ((.05,.51),(.31,.20),(.70,.42),(1.19,.67),(1.48,.27),
                         (1.83,.52),(2.14,.14),(2.62,.77),(2.91,.34),
                         (3.18,.57),(3.68,.90),(3.83,.32))
        self.checks = [(x,y,rng.uniform(.13,.53),rng.uniform(.0024,.0076),
                        rng.uniform(.0038,.0101),rng.uniform(-.036,.036))
                       for x,y in check_origins]
        self.adze = []
        for x,y,angle,count in ((.34,.46,.42,4),(1.17,.11,-.28,3),
                                (1.88,.71,.53,5),(2.54,.36,-.21,3),
                                (3.38,.61,.39,5),(3.78,.22,.61,3)):
            for i in range(count):
                self.adze.append((x+i*rng.uniform(.036,.070),y+rng.uniform(-.044,.044),
                                  angle+rng.uniform(-.22,.22),rng.uniform(.055,.116),
                                  rng.uniform(.016,.041),rng.uniform(.0012,.0048)))

    def side(self,x,y):
        u,v = x/SIDE_SIZE[0],y/SIDE_SIZE[1]
        seed,age = self.seed,self.age
        sweep = .087*(profile(u,v,6,4,seed+3)-.5)
        sweep += .017*(profile(u,v,19,23,seed+8)-.5)
        sweep += .0037*(profile(u,v,67,71,seed+9)-.5)
        warped = y+sweep
        eye, collar, knot_rings = (np.zeros_like(warped) for _ in range(3))
        knot_noise = .09*(profile(u,v,141,204,seed+17)-.5)
        for kx,ky,length,width,tilt,hardness in self.knots:
            dx,dy = around(x,kx,4),around(y,ky,1)
            dy -= tilt*dx
            axial = dx/length
            across = dy/width
            # The surrounding annual rings fan around the embedded branch,
            # and the branch has its own tight, irregular rings.
            falloff = np.exp(-.74*(axial*.42)**2-.48*(across*.37)**2)
            warped += (width*.96+.018)*(across/np.sqrt(.65+across*across))*falloff
            r = np.sqrt(axial*axial+across*across)
            r += knot_noise
            eye = np.maximum(eye,(1-ramp(.32,.91,r))*hardness)
            collar = np.maximum(collar,ramp(.82,1.07,r)*(1-ramp(1.12,1.94,r)))
            knots = (.5+.5*np.cos(2*np.pi*(r*3.2+.07*np.sin(9*axial))))**5
            knot_rings = np.maximum(knot_rings,knots*(1-ramp(.30,1.52,r)))
        across = warped/SIDE_SIZE[1]
        grain_phase = 84*across + 2.6*profile(u,across,14,36,seed+14)
        ring = .5+.5*np.sin(2*np.pi*grain_phase)
        latewood = ring**7
        ribbon = profile(u,across,16,111,seed+22)
        fibril = profile(u,across,87,377,seed+27)
        vessels = ramp(.59,.89,profile(u,across,197,419,seed+31))
        bands = profile(u,across,11,29,seed+36)
        torn = ramp(.54,.81,profile(u,across,23,120,seed+42))
        coat = profile(u,v,6,8,seed+41)
        exposure = age*ramp(.27,.75,.66*coat+.34*bands)
        patina = exposure*ramp(.41,.69,.66*profile(u,v,16,19,seed+58)+.34*ribbon)
        abrasion = ramp(.61,.90,profile(u,across,39,67,seed+63))*exposure
        torn *= ramp(.28,.69,.61*bands+.39*coat)
        hewn = .0049*(profile(u,across,9,18,seed+62)-.5)
        hewn += .0028*(profile(u,v,12,11,seed+65)-.5)
        checks, chipped, scoops = (np.zeros_like(warped) for _ in range(3))
        for i,(cx,cy,length,width,depth,tilt) in enumerate(self.checks):
            dx = around(x,cx,4)
            t = dx/length
            dy = around(warped,cy,1)-tilt*dx
            dy += .004*(profile(u,v,47,15,seed+i+90)-.5)
            taper = (1-ramp(.10,1,np.abs(t)))
            taper *= .75+.25*profile(u,v,88,16,seed+i+120)
            notch = np.maximum(width*(.26+.74*taper),.001)
            signed = dy/notch
            cut = (1-ramp(.13,1,np.abs(signed)))*taper
            if i%3==0:
                fork = np.abs(dy-.047*np.maximum(dx,0))/notch
                cut = np.maximum(cut,.57*(1-ramp(.12,.80,fork))*taper*ramp(.04,.16,dx))
            checks = np.maximum(checks,depth*cut)
            shoulder = ramp(.54,1.15,np.abs(signed))*(1-ramp(1.25,3.4,np.abs(signed)))
            chipped = np.maximum(chipped,shoulder*taper*depth/.0078)
        for hx,hy,angle,length,width,depth in self.adze:
            dx,dy = around(x,hx,4),around(y,hy,1)
            a = (dx*np.cos(angle)+dy*np.sin(angle))/length
            b = (dy*np.cos(angle)-dx*np.sin(angle))/width
            s = a+.38*b*b
            # Tool entry is a narrow shoulder above a shallow scooped bed.
            sweep = ramp(-.74,-.48,s)*(1-ramp(-.36,.94,s))
            mark = sweep*(1-ramp(.17,1,np.abs(b)))
            scoops = np.maximum(scoops,depth*mark)
        relief = .0140+hewn
        relief += (.00085+.00092*exposure)*(ribbon-.46)
        relief += .0011*(fibril-.47)-.00061*vessels-latewood*(.00032+.00068*bands)
        relief -= .00145*abrasion
        relief += .00150*collar-.0051*eye-.00145*knot_rings
        relief -= .0032*torn+checks*(.63+.37*age)+scoops
        relief += .00125*chipped*(fibril-.31)
        relief = np.maximum(relief,.0009)
        hue = blend(np.array([.170,.094,.049]),np.array([.124,.106,.085]),exposure)
        hue *= (.68+.32*bands+.22*ribbon+.105*fibril-.17*latewood-.23*vessels-.28*torn)[...,None]
        hue = blend(hue,np.array([.080,.073,.058]),.52*patina)
        hue = blend(hue,np.array([.197,.159,.115]),.43*abrasion)
        hue = blend(hue,np.array([.072,.036,.016]),np.clip(.76*eye+.32*knot_rings,0,1))
        hue = blend(hue,np.array([.058,.034,.021]),ramp(.0006,.0060,checks)*.76)
        hue = blend(hue,np.array([.226,.143,.077]),np.clip(92*scoops+.36*chipped,0,.40))
        # Small pressure-polished areas beside weathered, porous fibers.
        rough = .67+.12*exposure+.07*vessels+.07*torn+.10*ramp(.001,.006,checks)+.06*patina
        rough -= .095*eye+.05*ramp(.0002,.0029,scoops)
        rough += .035*(fibril-.5)
        return Wood(relief,hue,np.clip(rough,.54,.93))

    def end(self,x,y):
        u,v = x/END_SIZE[0],y/END_SIZE[1]
        seed = self.seed
        dx,dy = x-.137,y-.198
        a = np.arctan2(dy,dx)
        r = np.hypot(dx*1.13,dy*.92)
        r *= 1+.085*np.sin(3*a+.8)+.054*np.cos(5*a-1.3)
        r += .0034*(profile(u,v,13,12,seed+8,False)-.5)
        phase = 139*r+1.54*profile(u,v,8,9,seed+71,False)+.32*np.sin(r*96+1.2)
        earlywood = (.5+.5*np.sin(2*np.pi*phase))**7
        pores = ramp(.51,.88,profile(u,v,188,193,seed+9,False))*(.25+.75*earlywood)
        rays = (.5+.5*np.sin(81*a+9*r+.61*np.sin(7*a)))**12*ramp(.01,.08,r)
        rays *= profile(u,v,36,38,seed+2,False)
        color_var = profile(u,v,10,11,seed+11,False)
        face_check = np.zeros_like(r)
        for bearing,start,end,width,depth in ((-.43,.032,.21,.0034,.0045),
               (1.62,.063,.16,.0029,.0037),(2.82,.094,.18,.0030,.0035),
               (-1.68,.078,.15,.0026,.0030),(.63,.006,.079,.0022,.0029)):
            rel = (a-bearing+np.pi)%(2*np.pi)-np.pi
            drift = .005*(profile(u,v,41,32,seed+int((bearing+4)*30),False)-.5)
            distance = np.abs(r*np.sin(rel)+drift)
            span = ramp(start,start+.020,r)*(1-ramp(end-.018,end,r))
            cut = (1-ramp(.0007,width,distance))*span*(np.cos(rel)>0)
            face_check = np.maximum(face_check,cut*depth)
        z = .0068-.00062*earlywood-.00072*pores+.00025*rays-face_check
        z += .0010*(profile(u,v,35,18,seed+16,False)-.5)
        tint = blend(np.array([.231,.136,.072]),np.array([.164,.122,.084]),
                     .65*self.age*color_var)
        tint *= (.86+.25*color_var-.17*earlywood-.20*pores+.08*rays)[...,None]
        tint = blend(tint,np.array([.079,.044,.022]),ramp(.0007,.0045,face_check)*.75)
        return Wood(z,tint,np.clip(.72+.10*pores+.10*ramp(0,.0045,face_check),.58,.94))


def surface_mesh(name,points,faces):
    mesh = bpy.data.meshes.new(name)
    mesh.vertices.add(len(points))
    mesh.vertices.foreach_set("co",np.asarray(points,dtype=np.float32).ravel())
    mesh.loops.add(faces.size)
    mesh.loops.foreach_set("vertex_index",np.asarray(faces,dtype=np.int32).ravel())
    mesh.polygons.add(len(faces))
    mesh.polygons.foreach_set("loop_start",np.arange(0,faces.size,faces.shape[1],dtype=np.int32))
    mesh.update(calc_edges=True)
    obj = bpy.data.objects.new(name,mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def grid_faces(nx,ny):
    i = np.arange(nx*ny,dtype=np.int32).reshape(ny,nx)
    return np.stack((i[:-1,:-1],i[:-1,1:],i[1:,1:],i[1:,:-1]),axis=-1).reshape(-1,4)


def attrs(obj,wood):
    mesh = obj.data
    rgba = np.column_stack((wood.color.reshape(-1,3),np.ones(len(mesh.vertices))))
    mesh.color_attributes.new(name="Wood color",type="FLOAT_COLOR",domain="POINT").data.foreach_set(
        "color",rgba.astype(np.float32).ravel())
    mesh.attributes.new(name="Wood roughness",type="FLOAT",domain="POINT").data.foreach_set(
        "value",wood.roughness.astype(np.float32).ravel())


def source_material():
    mat = bpy.data.materials.new("Structural timber | authoring")
    mat.use_nodes = True
    nodes,links = mat.node_tree.nodes,mat.node_tree.links
    color = nodes.new("ShaderNodeVertexColor")
    color.layer_name = "Wood color"
    rough = nodes.new("ShaderNodeAttribute")
    rough.attribute_name = "Wood roughness"
    bsdf = nodes.get("Principled BSDF")
    links.new(color.outputs["Color"],bsdf.inputs["Base Color"])
    links.new(rough.outputs["Fac"],bsdf.inputs["Roughness"])
    return mat,color.outputs["Color"]


def bake_source(bounds, relief_fn, sampling=512):
    # Padding is sampled from the same surface. Opposite tile edges see the
    # same tangent geometry and smooth vertex normals inside the bake cage.
    width,height = bounds
    dx,dy = width/(sampling*int(round(width/height))),height/sampling
    x,y = np.meshgrid(np.arange(-2,round(width/dx)+3)*dx,np.arange(-2,sampling+3)*dy)
    wood = relief_fn(x,y)
    points = np.column_stack((x.ravel(),y.ravel(),wood.height.ravel()))
    obj = surface_mesh("Hewn surface | bake source",points,grid_faces(x.shape[1],x.shape[0]))
    obj.data.polygons.foreach_set("use_smooth",np.ones(len(obj.data.polygons),bool))
    attrs(obj,wood)
    return obj


def image_path(channel, section="side"):
    suffix = "exr" if channel in {"rough","height"} else "png"
    stem = STEM if section=="side" else STEM+"_end"
    return ROOT/f"{stem}_{channel}.{suffix}"


def pixels(image):
    data = np.empty(len(image.pixels),np.float32)
    image.pixels.foreach_get(data)
    return data.reshape(image.size[1],image.size[0],4)


def bake(bounds, section, high, material, color, size, height_range):
    w,h = bounds
    plate = surface_mesh("Texture receiving plane",[(0,0,0),(w,0,0),(w,h,0),(0,h,0)],
                         np.array([[0,1,2,3]]))
    uv = plate.data.uv_layers.new(name="UV0_Metric")
    uv.data.foreach_set("uv",[0,0,1,0,1,1,0,1])
    target = bpy.data.materials.new("Bake target")
    target.use_nodes = True
    plate.data.materials.append(target)
    image_node = target.node_tree.nodes.new("ShaderNodeTexImage")
    target.node_tree.nodes.active = image_node
    selected = bpy.context.view_layer.objects
    bpy.ops.object.select_all(action="DESELECT")
    high.select_set(True)
    plate.select_set(True)
    selected.active = plate
    nodes,links = material.node_tree.nodes,material.node_tree.links
    surface = nodes.get("Material Output").inputs["Surface"]
    shader = nodes.get("Principled BSDF").outputs[0]
    emit = nodes.new("ShaderNodeEmission")
    geop = nodes.new("ShaderNodeNewGeometry")
    axis = nodes.new("ShaderNodeSeparateXYZ")
    div = nodes.new("ShaderNodeMath")
    div.operation = "DIVIDE"
    div.inputs[1].default_value = height_range
    links.new(geop.outputs["Position"],axis.inputs[0])
    links.new(axis.outputs["Z"],div.inputs[0])
    outputs = {}
    for channel,kind,signal in (("albedo","EMIT",color),("normal","NORMAL",None),
                                 ("rough","ROUGHNESS",None),("height","EMIT",div.outputs[0])):
        if signal is not None:
            links.new(signal,emit.inputs[0])
            links.new(emit.outputs[0],surface)
        else:
            links.new(shader,surface)
        image = bpy.data.images.new(f"{section} {channel}",*size,alpha=False,float_buffer=True)
        image.colorspace_settings.name = "Linear Rec.709" if channel=="albedo" else "Non-Color"
        image_node.image = image
        bpy.ops.object.bake(type=kind,use_selected_to_active=True,cage_extrusion=.036,
                           max_ray_distance=.065,normal_space="TANGENT",margin=0)
        print("Baked",section,channel,tuple(size),flush=True)
        outputs[channel] = image
    links.new(shader,surface)
    for node in (emit,div,axis,geop):
        nodes.remove(node)
    bpy.data.objects.remove(plate,do_unlink=True)
    bpy.data.materials.remove(target)
    return outputs


def check(section, images, bounds, relief, repeat=None):
    channels = {}
    for key,image in images.items():
        data = channels[key] = pixels(image)[:,:,:3]
        if repeat is not None:
            np.testing.assert_array_equal(data,pixels(repeat[key])[:,:,:3],err_msg=f"{section} {key}")
        if not np.isfinite(data).all() or data.min()<-.0001 or data.max()>1.0001:
            raise ValueError(f"Invalid values in {section} {key}: {(data.min(),data.max())}")
        if section=="side":
            for axis in (0,1):
                seam = np.abs(np.take(data,0,axis)-np.take(data,-1,axis)).mean()
                jumps = np.abs(np.diff(data,axis=axis)).mean(axis=tuple(i for i in range(3) if i!=axis))
                if seam>np.max(jumps)*1.20+.0002:
                    raise ValueError(f"Wrap discontinuity in {key} along axis {axis}")
                print(f"Seam {key} axis {axis}: {seam:.5f}, internal transitions up to {jumps.max():.5f}")
    normal = channels["normal"]*2-1
    if np.abs(np.linalg.norm(normal,axis=2)-1).max()>.025:
        raise ValueError(f"Invalid tangent normal in {section}")
    height = channels["height"][:,:,0]*relief
    dv,du = np.gradient(height,bounds[1]/height.shape[0],bounds[0]/height.shape[1])
    for i,derivative in enumerate((du,dv)):
        corr = np.corrcoef((-derivative).ravel(),normal[:,:,i].ravel())[0,1]
        if corr<.66:
            raise ValueError(f"Normal and height disagree in {section} axis {i}: {corr}")
        print(f"{section} normal-height alignment axis {i}: {corr:.3f}",flush=True)
    if section=="side":
        longitudinal_bias = float(dv.std()/du.std())
        if longitudinal_bias<1.6:
            raise ValueError(f"Grain is not longitudinal: {longitudinal_bias:.2f}")
        print(f"Side cross-grain / longitudinal slope: {longitudinal_bias:.2f}",flush=True)
    if repeat is not None:
        print(f"All four {section} repeat bakes match pixel-for-pixel",flush=True)


def publish(scene,images,section):
    settings = scene.render.image_settings
    settings.color_mode = "RGB"
    for key,image in images.items():
        out = str(image_path(key,section))
        if key=="albedo":
            scene.view_settings.view_transform = "Standard"
            scene.view_settings.look = "None"
            settings.file_format = "PNG"
            settings.color_depth = "8"
            image.save_render(out,scene=scene)
            scene.view_settings.view_transform = "AgX"
        elif key=="normal":
            image.filepath_raw = out
            image.file_format = "PNG"
            image.save()
        else:
            settings.file_format = "OPEN_EXR"
            settings.color_depth = "16"
            settings.exr_codec = "ZIP"
            image.save_render(out,scene=scene)


def mapped_material(name, bounds, paths, *, uv_offset=(0,0), repeat=True):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes,links = mat.node_tree.nodes,mat.node_tree.links
    uv = nodes.new("ShaderNodeUVMap")
    uv.uv_map = "UV0_Metric"
    mapping = nodes.new("ShaderNodeMapping")
    mapping.inputs["Scale"].default_value = (1/bounds[0],1/bounds[1],1)
    mapping.inputs["Location"].default_value = (uv_offset[0]/bounds[0],uv_offset[1]/bounds[1],0)
    links.new(uv.outputs["UV"],mapping.inputs["Vector"])
    bsdf = nodes.get("Principled BSDF")
    for key,socket in (("albedo","Base Color"),("normal","Normal"),("rough","Roughness")):
        image = bpy.data.images.load(str(paths(key)),check_existing=True)
        image.colorspace_settings.name = "sRGB" if key=="albedo" else "Non-Color"
        tex = nodes.new("ShaderNodeTexImage")
        tex.extension = "REPEAT" if repeat else "EXTEND"
        tex.image = image
        links.new(mapping.outputs["Vector"],tex.inputs["Vector"])
        signal = tex.outputs["Color"]
        if key=="normal":
            normal = nodes.new("ShaderNodeNormalMap")
            normal.uv_map = uv.uv_map
            links.new(signal,normal.inputs["Color"])
            signal = normal.outputs["Normal"]
        links.new(signal,bsdf.inputs[socket])
    return mat


def timber_materials():
    side = mapped_material("Lowmark Structural Timber | Longitudinal",SIDE_SIZE,image_path)
    end = mapped_material("Lowmark Structural Timber | Crosscut",END_SIZE,
                          lambda key: image_path(key,"end"),repeat=False)
    return side,end


def write_material_library(materials):
    out = ROOT/f"{STEM}.blend"
    for mat in materials:
        mat.use_fake_user = True
    bpy.data.libraries.write(str(out),set(materials),path_remap="RELATIVE_ALL",
                             fake_user=True,compress=True)


def timber_section(x,y,z,length,half_width,half_depth):
    # Squared hewn section with asymmetric wane and isolated corner loss.
    diagonal = np.abs(y/half_width)+np.abs(z/half_depth)
    nick = .20*np.exp(-((x-.17*length)/.036)**2)*(z>0)*(y<0)
    nick += .17*np.exp(-((x-.87*length)/.025)**2)*(y>0)*(z>0)
    lip = .039+.020*np.sin(12*x+1.7)+.018*np.sin(21*x+.5+.4*np.sign(y))
    shrink = np.minimum(1,(2-lip-nick)/np.maximum(.5,diagonal))
    return y*shrink+.0026*np.sin(4.7*x+1.15),z*shrink+.0023*np.sin(6.1*x+.6)


def skew_cut(x,y,z,length):
    return x+(.052*y-.028*z)*(1-ramp(0,.09,np.minimum(x,length-x)))


def beam(timber, length, width, depth, offset, location, *, high, materials):
    vertices,faces,uvs,attribs = [],[],[],[]
    w,d = width/2,depth/2
    corners = np.array([[-w,-d],[-w,d],[w,d],[w,-d]])
    longitudinal = np.linspace(0,length,round(length/(.0026 if high else .024))+1)
    point_count = 0

    def append(point, uv, wood):
        nonlocal point_count
        ny,nx = point.shape[:2]
        vertices.append(point.reshape(-1,3))
        uvs.append(uv.reshape(-1,2))
        faces.append(grid_faces(nx,ny)+point_count)
        if wood is not None:
            attribs.append(wood)
        point_count += nx*ny

    v0 = offset[1]
    for start,stop in zip(corners,np.roll(corners,-1,axis=0)):
        edge = stop-start
        span = np.linalg.norm(edge)
        cross = np.linspace(0,span,round(span/(.0022 if high else .016))+1)
        x,t = np.meshgrid(longitudinal,cross)
        base = start+t[...,None]/span*edge
        y,z = timber_section(x,base[...,0],base[...,1],length,w,d)
        u,v = x+offset[0],t+v0
        wood = timber.side(u,v) if high else None
        if wood is not None:
            normal = np.array([-edge[1],edge[0]])/span
            end_fade = ramp(0,.015,np.minimum(x,length-x))
            side_fade = ramp(0,.010,np.minimum(t,span-t))
            h = (wood.height-.014)*side_fade*end_fade
            y,z = y+normal[0]*h,z+normal[1]*h
        append(np.stack((skew_cut(x,base[...,0],base[...,1],length),y,z),axis=-1),
               np.stack((u,v),axis=-1),wood)
        v0 += span

    side_count = sum(len(face) for face in faces)
    for sign in (-1,1):
        span = np.linspace(-w,w,round(width/(.0018 if high else .014))+1)
        tv = np.linspace(-d,d,round(depth/(.0018 if high else .014))+1)
        y,z = np.meshgrid(sign*span,tv)
        x = np.full_like(y,0 if sign<0 else length)
        angle = .40*np.sin(offset[0]*2.7)-.25
        gen_u = sign*y*np.cos(angle)-z*np.sin(angle)+END_SIZE[0]/2
        gen_v = sign*y*np.sin(angle)+z*np.cos(angle)+END_SIZE[1]/2
        wood = timber.end(gen_u,gen_v) if high else None
        yz = timber_section(x,y,z,length,w,d)
        x = skew_cut(x,y,z,length)
        if wood is not None:
            at_edge = np.minimum(w-np.abs(y),d-np.abs(z))
            x += sign*(wood.height-.0068)*ramp(0,.007,at_edge)
        append(np.stack((x,*yz),axis=-1),np.stack((gen_u,gen_v),axis=-1),wood)
    all_faces = np.concatenate(faces)
    obj = surface_mesh("Hewn timber | modeled" if high else "Hewn timber | baked",
                       np.concatenate(vertices),all_faces)
    uv = obj.data.uv_layers.new(name="UV0_Metric")
    uv.data.foreach_set("uv",np.concatenate(uvs)[all_faces.ravel()].astype(np.float32).ravel())
    obj.data.polygons.foreach_set("use_smooth",np.ones(len(all_faces),bool))
    obj.location = location
    for material in materials:
        obj.data.materials.append(material)
    if high:
        color = np.concatenate([part.color.reshape(-1,3) for part in attribs])
        rough = np.concatenate([part.roughness.ravel() for part in attribs])
        attrs(obj,Wood(np.empty(0),color,rough))
    else:
        slot = np.zeros(len(all_faces),np.int32)
        slot[side_count:] = 1
        obj.data.polygons.foreach_set("material_index",slot)
    return obj


def plain(name,rgb,roughness=.82):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*rgb,1)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*rgb,1)
    shader.inputs["Roughness"].default_value = roughness
    return mat


def point(obj,target):
    obj.rotation_euler = (Vector(target)-obj.location).to_track_quat("-Z","Y").to_euler()


def studio(scene):
    scene.world = bpy.data.worlds.new("Neutral timber review")
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes.get("Background")
    bg.inputs[0].default_value = (.69,.73,.79,1)
    bg.inputs[1].default_value = .43
    scene.cycles.samples = 30
    scene.cycles.use_denoising = True
    bpy.ops.object.camera_add()
    camera = scene.camera = bpy.context.object
    camera.data.type = "ORTHO"
    bpy.ops.object.light_add(type="AREA",location=(-.70,-2.90,3.60))
    key = bpy.context.object
    key.data.shape = "DISK"
    key.data.size = 3.0
    key.data.energy = 440
    point(key,(.6,0,.2))
    return camera,key


def render(scene,label,width,height):
    scene.render.resolution_x,scene.render.resolution_y = width,height
    scene.render.resolution_percentage = 100
    image = scene.render.image_settings
    image.file_format = "PNG"
    image.color_mode = "RGB"
    image.color_depth = "8"
    scene.render.filepath = str(ROOT/f"{STEM}_{label}.png")
    bpy.ops.render.render(write_still=True)


def panels(scene, timber, authored, baked_materials):
    camera,key = studio(scene)
    specimens = ((1.64,.272,.258,(.25,.27),(0,0,.14)),
                 (1.32,.205,.197,(1.43,.483),(.18,.49,.107)))
    high = [beam(timber,*spec,high=True,materials=(authored,)) for spec in specimens]
    camera.location = (3.0,-3.8,2.48)
    target = (.78,.16,.20)
    point(camera,target)
    camera.data.ortho_scale = 1.88
    ground = surface_mesh("Studio floor",[(-20,-20,0),(20,-20,0),(20,20,0),(-20,20,0)],
                          np.array([[0,1,2,3]]))
    ground.data.materials.append(plain("Studio gray",(.23,.235,.23)))
    bpy.ops.object.light_add(type="AREA",location=(3.3,-1.05,1.80))
    fill = bpy.context.object
    fill.data.energy = 100
    fill.data.size = 1.75
    point(fill,(1.52,.06,.16))
    clay = plain("Neutral review clay",(.44,.44,.44))
    for obj in high:
        obj.data.materials[0] = clay
    render(scene,"clay",1320,800)
    for obj in high:
        obj.data.materials[0] = authored
    render(scene,"modeled",1320,800)
    if baked_materials is None:
        return

    for obj in high:
        bpy.data.objects.remove(obj,do_unlink=True)
    side,end = baked_materials
    low = [beam(timber,*spec,high=False,materials=(side,end)) for spec in specimens]
    render(scene,"baked",1320,800)
    camera.location = (3.2,-1.06,1.03)
    point(camera,(1.49,-.036,.19))
    camera.data.ortho_scale = .61
    render(scene,"crosscut",1050,850)

    for obj in low:
        bpy.data.objects.remove(obj,do_unlink=True)
    bpy.data.objects.remove(ground,do_unlink=True)
    bpy.data.objects.remove(fill,do_unlink=True)
    # Face-on repeat of the square-metre-scaled side texture.
    w,h = np.array(SIDE_SIZE)*2
    chart = surface_mesh("Two-by-two wood repeat",[(0,0,0),(w,0,0),(w,h,0),(0,h,0)],
                         np.array([[0,1,2,3]]))
    chart.data.materials.append(side)
    uv = chart.data.uv_layers.new(name="UV0_Metric")
    uv.data.foreach_set("uv",[0,0,w,0,w,h,0,h])
    camera.location = (w/2,h/2,8)
    point(camera,(w/2,h/2,0))
    camera.data.ortho_scale = w
    key.location = (2.6,-1.9,3.2)
    key.data.energy = 750
    point(key,(w/2,h/2,0))
    render(scene,"repeat",2000,500)
    bpy.data.objects.remove(chart,do_unlink=True)
    farmhouse(scene,camera,key,side)


def orientation_probe(obj):
    mesh = obj.data
    uv = mesh.uv_layers.get("UV0_Metric")
    if uv is None:
        raise ValueError(f"{obj.name}: generated timber lacks metric UV0")
    results = {"vertical":0,"horizontal":0,"diagonal":0}
    for f in mesh.polygons:
        loops = list(f.loop_indices)
        verts = [mesh.vertices[mesh.loops[i].vertex_index].co for i in loops]
        edges = [verts[(i+1)%len(verts)]-verts[i] for i in range(len(verts))]
        j = max(range(len(edges)),key=lambda k: edges[k].length)
        if edges[j].length<.33:
            continue
        delta = uv.data[loops[(j+1)%len(loops)]].uv-uv.data[loops[j]].uv
        if abs(delta.y)>.001 or abs(abs(delta.x)-edges[j].length)>.002:
            raise ValueError(f"{obj.name}: U is not metric along a timber face")
        vertical = abs(edges[j].normalized().z)
        key = "vertical" if vertical>.98 else "horizontal" if vertical<.02 else "diagonal"
        results[key] += 1
    return results


def farmhouse(scene,camera,key,side):
    generator = ROOT.parents[2]/"CODE"/"Scripts"/"architectural_generator"
    sys.path.insert(0,str(generator))
    from caelmor_architecture.blender_backend import build
    from caelmor_architecture.model import Settings

    collection,_ = build(Settings(footprint="RECT",width=8.2,depth=5.6,floors=1,
                                  floor_height=2.75,detail="MEDIUM",seed=17))
    candidates = [obj for obj in collection.all_objects if obj.type=="MESH"
                  and obj.get("caelm_material") in {"timber","timber_light"}
                  and obj.get("caelm_layer") in {"structure","walls","roof"}
                  and not obj.get("caelm_collider")]
    counts = {"vertical":0,"horizontal":0,"diagonal":0}
    for obj in candidates:
        for key_name,val in orientation_probe(obj).items():
            counts[key_name] += val
    if not all(counts.values()):
        raise RuntimeError(f"Farmhouse doesn't cover all member directions: {counts}")
    print(f"Farmhouse material probe: {len(candidates)} timber buffers, faces {counts}",flush=True)

    # Preview-only phase offsets per buffer. Geometry and UVs come directly
    # from the installed generator. The candidate replaces slots in memory.
    offsets = ((.33,.23),(1.79,.417),(3.17,.684),(2.55,.832))
    variations = [side]+[mapped_material(f"Timber display phase {i}",SIDE_SIZE,image_path,
                                        uv_offset=offset) for i,offset in enumerate(offsets)]
    for i,obj in enumerate(sorted(candidates,key=lambda item:item.name)):
        obj.data.materials.clear()
        obj.data.materials.append(variations[i%len(variations)])
    for obj in collection.all_objects:
        if obj.get("caelm_collider"):
            obj.hide_render = True
    ground = surface_mesh("Farmhouse studio floor",[(x,y,-.055) for x,y in
                         ((-35,-35),(35,-35),(35,35),(-35,35))],np.array([[0,1,2,3]]))
    ground.data.materials.append(plain("Neutral earth",(.20,.184,.152)))
    bpy.ops.object.light_add(type="SUN",location=(-6,-9,12))
    sun = bpy.context.object
    sun.data.energy = 2.4
    sun.data.angle = .20
    point(sun,(0,0,0))
    key.hide_render = True
    coords = [obj.matrix_world@Vector(p) for obj in collection.all_objects
              if obj.type=="MESH" and not obj.hide_render for p in obj.bound_box]
    low = Vector(tuple(min(p[i] for p in coords) for i in range(3)))
    high = Vector(tuple(max(p[i] for p in coords) for i in range(3)))
    center = (high+low)/2
    camera.location = center+Vector((7.8,-15.6,4.3))
    point(camera,center)
    camera.data.ortho_scale = 12.45
    render(scene,"farmhouse",1540,1100)
    detail = Vector((center.x,low.y+.44,1.66))
    camera.location = detail+Vector((3.5,-10,1.45))
    point(camera,detail)
    camera.data.ortho_scale = 5.4
    render(scene,"framing",1320,820)


def main():
    parser = ArgumentParser()
    parser.add_argument("--draft",action="store_true",help="Render modeled and clay beams without baking")
    parser.add_argument("--verify-repeat",action="store_true",help="Repeat both bakes and compare every pixel")
    parser.add_argument("--bake-only",action="store_true",help="Skip studio and farmhouse renders")
    parser.add_argument("--side-short",type=int,default=1024,help="Pixels along side map V")
    parser.add_argument("--end-size",type=int,default=1024)
    parser.add_argument("--seed",type=int,default=SEED)
    parser.add_argument("--age",type=float,default=.79)
    args = parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    if min(args.side_short,args.end_size)<128 or not 0<=args.age<=1:
        parser.error("Bake dimensions must be at least 128 and age must be in [0, 1]")
    if args.draft and args.bake_only:
        parser.error("--draft and --bake-only are mutually exclusive")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 1
    scene.cycles.device = "CPU"
    scene.view_settings.view_transform = "AgX"
    timber = Timber(args.seed,args.age)
    authored,color = source_material()
    materials = None
    if not args.draft:
        for section,bounds,relief_fn,height_ref,short in (
            ("side",SIDE_SIZE,timber.side,SIDE_RELIEF,args.side_short),
            ("end",END_SIZE,timber.end,END_RELIEF,args.end_size),
        ):
            sample = min(640,max(196,short*5//8)) if section=="side" else min(480,max(196,short//2))
            source = bake_source(bounds,relief_fn,sample)
            source.data.materials.append(authored)
            size = (short*round(bounds[0]/bounds[1]),short)
            images = bake(bounds,section,source,authored,color,size,height_ref)
            repeat = bake(bounds,section,source,authored,color,size,height_ref) if args.verify_repeat else None
            check(section,images,bounds,height_ref,repeat)
            publish(scene,images,section)
            for image in list(images.values())+list((repeat or {}).values()):
                bpy.data.images.remove(image)
            bpy.data.objects.remove(source,do_unlink=True)
        materials = timber_materials()
        write_material_library(materials)
    if not args.bake_only:
        panels(scene,timber,authored,materials)


if __name__ == "__main__":
    main()
