"""Author and bake Lowmark's reusable forged iron in Blender 5.0.1."""
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
import json
import math
import sys

import bpy
from mathutils import Vector
import numpy as np

ROOT = Path(__file__).resolve().parent
STEM = "Lowmark_Forged_Iron_Hardware"
sys.path.insert(0,str(ROOT))
from build_lowmark_structural_timber import (
    around, blend, grid_faces, pixels, plain, point, profile, ramp, surface_mesh,
)

TILE = .384
RELIEF = .004
SEED = 28747
FINISHES = ("Maintained","Weathered","Corroded")
CHANNELS = ("albedo","normal","rough","metallic","height")
CONTACT = "Forge Contact"
CLEAN_IRON = (.505,.51,.511,1)


@dataclass(frozen=True)
class Iron:
    height: np.ndarray
    color: np.ndarray
    roughness: np.ndarray
    metallic: np.ndarray


class Forge:
    def __init__(self,seed,hammer,blackening):
        self.seed = seed
        self.hammer = hammer
        self.blackening = blackening
        rng = np.random.default_rng(seed)
        self.blows = []
        for u,v,heading,count in ((.055,.036,.43,5),(.161,.068,.04,6),
                                   (.278,.042,-.09,5),(.073,.158,.7,6),
                                   (.222,.164,.42,7),(.337,.192,-.15,6),
                                   (.094,.267,-.36,5),(.205,.304,.13,7),
                                   (.334,.330,-.26,5)):
            for j in range(count):
                along = (j-(count-1)/2)*rng.uniform(.012,.023)
                self.blows.append((u+along+rng.uniform(-.012,.012),
                                   v+.35*along+rng.uniform(-.034,.034),
                                   heading+rng.uniform(-.54,.54),
                                   rng.uniform(.012,.028),rng.uniform(.007,.018),
                                   rng.uniform(.000095,.00033)))
        self.pockets = tuple((x+rng.uniform(-.016,.016),y+rng.uniform(-.016,.016),a,b,angle)
                             for x,y,a,b,angle in (
            (.064,.096,.033,.021,-.7),(.156,.231,.045,.028,.3),
            (.256,.058,.031,.022,.58),(.333,.258,.047,.029,.95),
            (.281,.326,.023,.020,-.56),(.012,.342,.036,.019,.25)
        ))

    def sample(self,x,y,condition):
        u,v = x/TILE,y/TILE
        seed = self.seed
        warp = profile(u,v,18,19,seed+1)
        smelt = profile(u+.018*(warp-.5),v,12,25,seed+3)
        fold = profile(u,v,7,8,seed+4)
        tooth = profile(u,v,251,237,seed+6)
        sockets = profile(u,v,117,131,seed+8)
        scale = profile(u,v,30,28,seed+11)
        pits = ramp(.55,.89,sockets)*ramp(.25,.76,smelt)
        strikes = np.zeros_like(x)
        strike_polish = np.zeros_like(x)
        for cx,cy,angle,rx,ry,depth in self.blows:
            dx,dy = around(x,cx,TILE),around(y,cy,TILE)
            c,s = math.cos(angle),math.sin(angle)
            a,b = (c*dx+s*dy)/rx,(-s*dx+c*dy)/ry
            r = np.sqrt(a*a+b*b)+.16*(warp-.5)
            contact = 1-ramp(.22,1.08,r)
            strikes = np.maximum(strikes,depth*contact)
            strike_polish = np.maximum(strike_polish,contact*depth/.00033)
        damp = np.zeros_like(x)
        for cx,cy,rx,ry,angle in self.pockets:
            dx,dy = around(x,cx,TILE),around(y,cy,TILE)
            c,s = math.cos(angle),math.sin(angle)
            r = np.hypot((c*dx+s*dy)/rx,(-s*dx+c*dy)/ry)
            damp = np.maximum(damp,1-ramp(.08,1.54,r))
        retention = .58*damp+.25*scale+.17*sockets
        retention += .09*strike_polish+.07*(warp-.5)
        boundary = .88-.56*condition
        rust = ramp(boundary,boundary+.14,retention)
        # Thin black finish colors the iron reflection. Separate thick
        # oxide and rust from the conducting surface with coverage masks.
        crust = ramp(.66,.90,scale)*ramp(.38,.80,sockets)*(.27+.53*condition)
        metallic = (1-rust)*(1-crust)
        strip = ramp(.18,.82,strike_polish)*(.19-.11*condition)
        dark = self.blackening*(.945+.066*smelt+.056*(scale-.5))-.12*strip
        black = np.array([.027,.030,.033])
        base = blend(np.array(CLEAN_IRON[:3]),black,np.clip(dark,0,1))
        base *= (.90+.22*smelt+.073*(tooth-.5))[...,None]
        base = blend(base,np.array([.048,.044,.039]),crust)
        rust_color = blend(np.array([.063,.028,.015]),np.array([.160,.070,.030]),
                           ramp(.28,.78,.56*tooth+.44*sockets))
        base = blend(base,rust_color,rust)
        rough = .365+.135*smelt+.080*pits-.090*strip+.061*condition
        rough += .016*(tooth-.5)+.105*crust
        rough = rough*(1-rust)+(.760+.153*tooth)*rust
        depth = .00228+.00073*(fold-.5)+.00026*(smelt-.5)
        depth -= self.hammer*strikes+.00024*pits
        depth += .000091*(tooth-.5)
        depth -= rust*(.00007+.00049*pits)
        depth += rust*.00027*(tooth-.29)
        return Iron(depth,base,np.clip(rough,.30,.95),np.clip(metallic,0,1))


def image_path(finish,key):
    extension = "exr" if key in {"height","rough"} else "png"
    return ROOT/f"{STEM}_{finish}_{key}.{extension}"


def delete_mesh(obj):
    mesh = obj.data
    bpy.data.objects.remove(obj,do_unlink=True)
    if mesh.users==0:
        bpy.data.meshes.remove(mesh)


def projection_plate(width,height):
    obj = surface_mesh("Iron receiver",[(0,0,0),(width,0,0),(width,height,0),(0,height,0)],
                       np.array([[0,1,2,3]],np.int32))
    uv = obj.data.uv_layers.new(name="UV0_Metric")
    return obj,uv


def source_geometry(forge,condition,detail):
    pitch = TILE/detail
    u,v = np.meshgrid(np.arange(-2,detail+3)*pitch,np.arange(-2,detail+3)*pitch)
    material = forge.sample(u,v,condition)
    points = np.column_stack((u.ravel(),v.ravel(),material.height.ravel()))
    source = surface_mesh("Forged relief",points,grid_faces(u.shape[1],u.shape[0]))
    mesh = source.data
    mesh.polygons.foreach_set("use_smooth",np.ones(len(mesh.polygons),bool))
    rgba = np.column_stack((material.color.reshape(-1,3),np.ones(len(points))))
    mesh.color_attributes.new(name="Iron reflectance",type="FLOAT_COLOR",domain="POINT").data.foreach_set(
        "color",rgba.astype(np.float32).ravel())
    for key,data in (("Iron roughness",material.roughness),("Iron metallic",material.metallic)):
        mesh.attributes.new(name=key,type="FLOAT",domain="POINT").data.foreach_set(
            "value",data.astype(np.float32).ravel())
    return source


def bake_maps(forge,finish,condition,size):
    source = source_geometry(forge,condition,min(1056,max(300,size)))
    mat = bpy.data.materials.new("Forged iron bake source")
    mat.use_nodes = True
    source.data.materials.append(mat)
    nodes,links = mat.node_tree.nodes,mat.node_tree.links
    surface = nodes.get("Material Output").inputs["Surface"]
    shader = nodes.get("Principled BSDF")
    color = nodes.new("ShaderNodeVertexColor")
    color.layer_name = "Iron reflectance"
    rough = nodes.new("ShaderNodeAttribute")
    rough.attribute_name = "Iron roughness"
    metal = nodes.new("ShaderNodeAttribute")
    metal.attribute_name = "Iron metallic"
    links.new(color.outputs["Color"],shader.inputs["Base Color"])
    links.new(rough.outputs["Fac"],shader.inputs["Roughness"])
    links.new(metal.outputs["Fac"],shader.inputs["Metallic"])
    geo = nodes.new("ShaderNodeNewGeometry")
    axis = nodes.new("ShaderNodeSeparateXYZ")
    links.new(geo.outputs["Position"],axis.inputs[0])
    scale = nodes.new("ShaderNodeMath")
    scale.operation = "DIVIDE"
    scale.inputs[1].default_value = RELIEF
    links.new(axis.outputs["Z"],scale.inputs[0])
    emit = nodes.new("ShaderNodeEmission")
    target_obj,uv = projection_plate(TILE,TILE)
    uv.data.foreach_set("uv",[0,0,1,0,1,1,0,1])
    target = bpy.data.materials.new("Iron bake target")
    target.use_nodes = True
    target_obj.data.materials.append(target)
    tex = target.node_tree.nodes.new("ShaderNodeTexImage")
    target.node_tree.nodes.active = tex
    bpy.ops.object.select_all(action="DESELECT")
    source.select_set(True)
    target_obj.select_set(True)
    bpy.context.view_layer.objects.active = target_obj
    outputs = {}
    for key,method,signal in (
        ("albedo","EMIT",color.outputs["Color"]),("normal","NORMAL",None),
        ("rough","ROUGHNESS",None),("metallic","EMIT",metal.outputs["Fac"]),
        ("height","EMIT",scale.outputs[0]),
    ):
        if signal is None:
            links.new(shader.outputs[0],surface)
        else:
            links.new(signal,emit.inputs[0])
            links.new(emit.outputs[0],surface)
        image = bpy.data.images.new(f"{finish} {key}",size,size,alpha=False,float_buffer=True)
        image.colorspace_settings.name = "Linear Rec.709" if key=="albedo" else "Non-Color"
        tex.image = image
        bpy.ops.object.bake(type=method,use_selected_to_active=True,cage_extrusion=.008,
                           max_ray_distance=.017,normal_space="TANGENT",margin=0)
        outputs[key] = image
        print("Baked",finish,key,flush=True)
    delete_mesh(target_obj)
    delete_mesh(source)
    bpy.data.materials.remove(target)
    bpy.data.materials.remove(mat)
    return outputs


def verify_maps(finish,outputs,repeat):
    data = {}
    for key,img in outputs.items():
        values = data[key] = pixels(img)[:,:,:3]
        if repeat is not None:
            np.testing.assert_array_equal(values,pixels(repeat[key])[:,:,:3],
                                          err_msg=f"{finish} {key}")
        if not np.isfinite(values).all() or values.min()<-.001 or values.max()>1.001:
            raise RuntimeError(f"Invalid {finish} {key} pixels: {values.min()}–{values.max()}")
        wrap = []
        for axis in (0,1):
            seam = np.abs(np.take(values,0,axis)-np.take(values,-1,axis)).mean()
            inside = np.abs(np.diff(values,axis=axis)).mean(
                axis=tuple(i for i in range(3) if i!=axis))
            if seam>1.25*inside.max()+.0001:
                raise RuntimeError(f"Visible {finish} {key} seam on axis {axis}")
            wrap.append((round(float(seam),5),round(float(inside.max()),5)))
        print(finish,key,"wrap vs interior max",wrap,flush=True)
    normal = data["normal"]*2-1
    if np.abs(np.linalg.norm(normal,axis=2)-1).max()>.025:
        raise RuntimeError(f"Invalid tangent normals in {finish}")
    v,u = np.gradient(data["height"][:,:,0])
    corr = [np.corrcoef(-g.ravel(),normal[:,:,i].ravel())[0,1] for i,g in enumerate((u,v))]
    if min(corr)<.77:
        raise RuntimeError(f"Normal and height mismatch in {finish}: {corr}")
    metal = data["metallic"][:,:,0]
    rough = data["rough"][:,:,0]
    coverage = float(np.mean(metal<.50))
    if coverage>.0005 and np.median(rough[metal<.50])<=np.median(rough[metal>.85]):
        raise RuntimeError(f"Corrosion roughness is inconsistent in {finish}")
    print(finish,"normal-height alignment",np.round(corr,3),
          f"dielectric-dominant pixels {coverage:.2%}",flush=True)
    if repeat is not None:
        print(f"All five independently rebuilt {finish} maps match pixel-for-pixel",flush=True)
    return coverage


def save_maps(scene,finish,outputs):
    settings = scene.render.image_settings
    settings.color_mode = "RGB"
    for key,img in outputs.items():
        path = str(image_path(finish,key))
        if key=="albedo":
            scene.view_settings.view_transform = "Standard"
            scene.view_settings.look = "None"
            settings.file_format = "PNG"
            settings.color_depth = "8"
            img.save_render(path,scene=scene)
            scene.view_settings.view_transform = "AgX"
        elif key in {"normal","metallic"}:
            img.filepath_raw = path
            img.file_format = "PNG"
            img.save()
        else:
            settings.file_format = "OPEN_EXR"
            settings.color_depth = "16"
            settings.exr_codec = "ZIP"
            img.save_render(path,scene=scene)


def material_maker_projects():
    # Native 1.7 Image nodes read the same maps as the Blender library.
    # The native depth port measures inward from the face, so invert height.
    # The native normal port uses the opposite X and Z signs to the Blender profile.
    for finish in FINISHES:
        nodes = []
        links = []
        ports = {"albedo":0,"metallic":1,"rough":2}
        for i,key in enumerate(CHANNELS):
            nodes.append({"name":key,"type":"image","seed_int":0,
                          "node_position":{"x":-570,"y":i*228},
                          "parameters":{"image":f"%PROJECT_PATH%/{image_path(finish,key).name}",
                                        "fix_ar":False,"clamp":False}})
        for name,node_type,x,y in (
            ("normal_components","decompose",-340,200),
            ("native_x","invert",-160,155),
            ("native_z","invert",-160,405),
            ("native_normal","combine",15,225),
            ("depth_from_height","invert",-200,4*228),
        ):
            nodes.append({"name":name,"type":node_type,"seed_int":0,
                          "node_position":{"x":x,"y":y},"parameters":{}})
        connections = [(key,0,"Material",port) for key,port in ports.items()]
        connections.extend((
            ("normal",0,"normal_components",0),
            ("normal_components",0,"native_x",0),
            ("normal_components",2,"native_z",0),
            ("native_x",0,"native_normal",0),
            ("normal_components",1,"native_normal",1),
            ("native_z",0,"native_normal",2),
            ("native_normal",0,"Material",4),
            ("height",0,"depth_from_height",0),
            ("depth_from_height",0,"Material",6),
        ))
        for source,output,target,input_port in connections:
            links.append({"from":source,"from_port":output,"to":target,"to_port":input_port})
        nodes.append({"name":"Material","type":"material","seed_int":0,"export_paths":{},
                      "node_position":{"x":250,"y":215},
                      "parameters":{"size":10,"metallic":1.,"roughness":1.,"normal":1.,
                                    "depth_scale":RELIEF/TILE,"ao":1.}})
        project = {"type":"graph","name":"Graph","label":f"Lowmark Forged Iron | {finish}",
                   "node_position":{"x":0,"y":0},"parameters":{},"seed_int":0,
                   "nodes":nodes,"connections":links}
        (ROOT/f"{STEM}_{finish}.ptex").write_text(json.dumps(project,indent=2)+"\n",encoding="utf-8")


def shader_library():
    mats = {}
    for finish in (*FINISHES,"Adjustable"):
        adjustable = finish=="Adjustable"
        mat = mats[finish] = bpy.data.materials.new(f"Lowmark Forged Iron | {finish}")
        mat.use_nodes = True
        mat.use_fake_user = True
        mat["caelm_repeat_metres"] = (TILE,TILE)
        mat["caelm_height_range_m"] = RELIEF
        nodes,links = mat.node_tree.nodes,mat.node_tree.links
        uv = nodes.new("ShaderNodeUVMap")
        uv.uv_map = "UV0_Metric"
        uv.location = (-1430,270)
        mapping = nodes.new("ShaderNodeVectorMath")
        mapping.operation = "SCALE"
        mapping.inputs["Scale"].default_value = 1/TILE
        mapping.location = (-1210,270)
        links.new(uv.outputs["UV"],mapping.inputs[0])

        def value(label,amount,x,y):
            node = nodes.new("ShaderNodeValue")
            node.label = label
            node.outputs[0].default_value = amount
            node.location = (x,y)
            return node.outputs[0]

        def mix(weight,first,second,label,x,y):
            node = nodes.new("ShaderNodeMixRGB")
            node.label = label
            node.location = (x,y)
            links.new(weight,node.inputs[0])
            for socket,signal in zip(node.inputs[1:],(first,second)):
                if isinstance(signal,tuple):
                    socket.default_value = signal
                else:
                    links.new(signal,socket)
            return node.outputs[0]

        def operation(op,source,factor,x,y):
            n = nodes.new("ShaderNodeMath")
            n.operation = op
            n.use_clamp = True
            n.location = (x,y)
            links.new(source,n.inputs[0])
            n.inputs[1].default_value = factor
            return n.outputs[0]

        attribute = nodes.new("ShaderNodeAttribute")
        attribute.attribute_name = CONTACT
        attribute.label = "Optional mesh contact mask"
        attribute.location = (-1110,680)
        amount = value("Contact polish strength",.45,-1100,840)
        contact = nodes.new("ShaderNodeMath")
        contact.operation = "MULTIPLY"
        contact.use_clamp = True
        contact.location = (-860,710)
        links.new(attribute.outputs["Fac"],contact.inputs[0])
        links.new(amount,contact.inputs[1])
        polished = contact.outputs[0]

        if adjustable:
            age = value("Exposure 0 maintained | 0.5 weathered | 1 corroded",.50,-1430,1010)
            first = operation("MULTIPLY",age,2.,-1180,1030)
            upper = operation("SUBTRACT",age,.5,-1180,1210)
            second = operation("MULTIPLY",upper,2.,-950,1040)

        bsdf = nodes.get("Principled BSDF")
        bsdf.location = (260,360)
        nodes.get("Material Output").location = (555,360)
        for i,(key,socket,target) in enumerate((
            ("albedo","Base Color",CLEAN_IRON),("normal","Normal",None),
            ("rough","Roughness",(.33,.33,.33,1)),("metallic","Metallic",(1,1,1,1)),
        )):
            y = 350-i*360
            textures = []
            for j,state in enumerate(FINISHES if adjustable else (finish,)):
                texture = nodes.new("ShaderNodeTexImage")
                texture.label = f"{state} {key}"
                texture.image = bpy.data.images.load(str(image_path(state,key)),check_existing=True)
                texture.image.colorspace_settings.name = "sRGB" if key=="albedo" else "Non-Color"
                texture.extension = "REPEAT"
                texture.location = (-940,y-j*105)
                texture.hide = adjustable
                links.new(mapping.outputs[0],texture.inputs["Vector"])
                textures.append(texture.outputs["Color"])
            signal = textures[0]
            if adjustable:
                lower = mix(first,signal,textures[1],"Maintained to weathered",-655,y)
                signal = mix(second,lower,textures[2],"Weathered to corroded",-430,y)
            if target is not None:
                signal = mix(polished,signal,target,"Contact polish",-210,y)
            if key=="normal":
                normal = nodes.new("ShaderNodeNormalMap")
                normal.uv_map = uv.uv_map
                normal.location = (-60,y)
                links.new(signal,normal.inputs["Color"])
                signal = normal.outputs["Normal"]
            links.new(signal,bsdf.inputs[socket])
    return mats


def uv_faces(obj,coords,faces):
    uv = obj.data.uv_layers.new(name="UV0_Metric")
    uv.data.foreach_set("uv",np.asarray(coords,dtype=np.float32)[faces.ravel()].ravel())
    return obj


def contact_attribute(obj,weight):
    data = obj.data.attributes.new(name=CONTACT,type="FLOAT",domain="POINT")
    data.data.foreach_set("value",np.asarray(weight,dtype=np.float32).ravel())


def strap(forge,condition,mat,*,high):
    nx,ny = (436,72) if high else (154,39)
    x,t = np.meshgrid(np.linspace(0,.326,nx),np.linspace(-1,1,ny))
    u = x/.326
    width = np.interp(u,[0,.14,.47,.78,.88,.93,.975,1],[.024,.025,.020,.0154,.015,.020,.017,.008])
    width += .00064*np.sin(78*x+.4)+.00054*np.sin(171*x)
    y = width*t+.00135*np.sin(x*13)
    bevel = ramp(.86,1,np.abs(t))
    crown = .00085*(1-t*t)+.00051*np.sin(24*x)+.00029*np.cos(48*x+.57)
    z = .009+crown-.0016*bevel*(1-.75*ramp(.971,1,u))-.00108*ramp(.968,1,u)-.0022*u
    tile_x,tile_y = x+.029,y+.095
    if high:
        h = forge.sample(tile_x,tile_y,condition).height-.00228
        z += h
    x += .0011*ramp(.92,1,u)*np.sin(2.8*t+.38)
    points = np.stack((x,y,z),axis=-1).reshape(-1,3)
    faces = grid_faces(nx,ny)
    mesh = uv_faces(surface_mesh("Drawn hinge strap",points,faces),
                    np.stack((tile_x,tile_y),axis=-1).reshape(-1,2),faces)
    mesh.data.materials.append(mat)
    mesh.data.polygons.foreach_set("use_smooth",np.ones(len(faces),bool))
    mask = bevel*(.49+.51*ramp(.12,.82,.5+.5*np.sin(x*44+.5*np.sign(t))))
    contact_attribute(mesh,mask)
    shell = mesh.modifiers.new("Forged plate thickness","SOLIDIFY")
    shell.thickness = .0058
    shell.offset = -1
    return mesh


def lathe(name,center,axis,profile_points,phase,material,polished):
    axis = Vector(axis).normalized()
    shoulder = Vector((0,0,1)) if abs(axis.z)<.9 else Vector((1,0,0))
    radial_x = shoulder.cross(axis).normalized()
    radial_y = axis.cross(radial_x).normalized()
    theta = np.linspace(0,2*np.pi,97)
    radii = np.array([r for a,r in profile_points])
    length = np.array([a for a,r in profile_points])
    a,r = np.meshgrid(theta,radii)
    axis_pos = length[:,None] + .00023*np.sin(5*a+phase)*ramp(0,.005,r)
    r = r*(1+.026*np.sin(5*a+phase)+.018*np.cos(3*a-1.8))
    center = np.array(center)
    points = center + axis_pos[...,None]*np.array(axis)
    points += (np.cos(a)*r)[...,None]*np.array(radial_x)
    points += (np.sin(a)*r)[...,None]*np.array(radial_y)
    faces = grid_faces(len(theta),len(length))
    # Each lathe profile runs from the lower end up the outer face.
    start = .052+.069*phase
    across = np.r_[0,np.cumsum(np.linalg.norm(np.diff(profile_points,axis=0),axis=1))]
    texcoords = np.stack((a*max(radii)+start,
                          np.broadcast_to(across[:,None]+.209+.025*phase,a.shape)),axis=-1)
    obj = uv_faces(surface_mesh(name,points.reshape(-1,3),faces),texcoords.reshape(-1,2),faces)
    obj.data.materials.append(material)
    obj.data.polygons.foreach_set("use_smooth",np.ones(len(faces),bool))
    polished = np.asarray(polished)[:,None]*(.59+.41*(.5+.5*np.sin(3*a+phase)))
    contact_attribute(obj,polished)
    return obj


def ringpull(mat):
    theta = np.linspace(0,2*np.pi,145)
    section = np.linspace(0,2*np.pi,25)
    t,s = np.meshgrid(theta,section)
    center = (.208,-.089,.0047)
    main = .039*(1+.034*np.cos(3*t+.8))
    rod = .0041*(1+.14*np.sin(3*t-.3)+.095*np.sin(5*t))
    radial = main+rod*np.cos(s)
    x = center[0]+radial*np.cos(t)
    y = center[1]+radial*np.sin(t)
    z = center[2]+rod*np.sin(s)+.00042*np.cos(t+.5)
    coords = np.stack((.053+main*t,.279+.0041*s),axis=-1)
    faces = grid_faces(len(theta),len(section))
    obj = uv_faces(surface_mesh("Worn forged pull ring",np.stack((x,y,z),axis=-1).reshape(-1,3),
                                faces),coords.reshape(-1,2),faces)
    obj.data.materials.append(mat)
    obj.data.polygons.foreach_set("use_smooth",np.ones(len(faces),bool))
    weight = ramp(.24,.90,-np.sin(t))*(.23+.77*ramp(.49,.91,np.cos(s)))
    contact_attribute(obj,weight)
    return obj


def specimens(forge,condition,material,high=False):
    items = [strap(forge,condition,material,high=high),ringpull(material)]
    eye = ((-.021,.0068),(-.021,.0103),(-.019,.0109),(.019,.0109),
           (.021,.0103),(.021,.0068),(-.021,.0068))
    items.append(lathe("Rolled hinge eye",(-.005,.001,.012),(0,1,0),eye,.77,material,
                       (.30,.67,.28,.18,.41,.56,.35)))
    pin = ((-.028,0),(-.028,.0061),(-.026,.0067),(.024,.0062),(.026,.0061),(.026,0))
    items.append(lathe("Tapered hinge pin",(-.005,.001,.012),(0,1,0),pin,1.68,material,
                       (0,.36,.39,.56,.61,.70)))
    for j,x in enumerate((.047,.159,.301)):
        y = (.0004,-.00095,.0015)[j]
        head = ((-.0031,0),(-.0031,.0052),(.0015,.0056),(.0019,.0090),
                (.0035,.0082),(.0051,.0059),(.0056,.0032),(.0056,0))
        items.append(lathe("Uneven forged fastener",(x,y,.009),(0,0,1),head,.53+j*.78,material,
                           (0,.08,.13,.46,.51,.47,.46,.43)))
    nail = ((-.002,0),(-.002,.0041),(.0012,.0043),(.0023,.0100),(.004,.008),(.005,0))
    items.append(lathe("Loose nail head",(.078,-.073,.0021),(0,0,1),nail,1.39,material,
                       (0,.04,.14,.26,.39,.50)))
    return items


def render(scene,label,width,height):
    scene.render.resolution_x,scene.render.resolution_y = width,height
    scene.render.resolution_percentage = 100
    settings = scene.render.image_settings
    settings.file_format = "PNG"
    settings.color_mode = "RGB"
    settings.color_depth = "8"
    scene.render.filepath = str(ROOT/f"{STEM}_{label}.png")
    bpy.ops.render.render(write_still=True)


def area(name,location,target,watts,size,width):
    bpy.ops.object.light_add(type="AREA",location=location)
    lamp = bpy.context.object
    lamp.name = name
    lamp.data.energy = watts
    lamp.data.shape = "RECTANGLE"
    lamp.data.size = size
    lamp.data.size_y = width
    point(lamp,target)
    return lamp


def studio(scene):
    scene.world = bpy.data.worlds.new("Neutral hardware studio")
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (.55,.55,.55,1)
    background.inputs["Strength"].default_value = .34
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    bpy.ops.object.camera_add()
    cam = scene.camera = bpy.context.object
    cam.data.type = "ORTHO"
    target = (.145,-.042,.004)
    cam.location = (.268,-.288,.244)
    point(cam,target)
    cam.data.ortho_scale = .421
    key = area("Broad white reflection card",(-.054,.170,.236),target,.84,.175,.092)
    fill = area("Soft front fill",(-.078,-.193,.218),target,.35,.249,.198)
    floor,_ = projection_plate(6,6)
    floor.location = (-3,-3,-.0004)
    floor.data.materials.append(plain("Studio graphite",(.158,.154,.149)))
    return cam,key,fill,floor


def repeat_view(scene,cam,key,fill,materials):
    width = TILE*2
    plane,uv = projection_plate(width,width)
    uv.data.foreach_set("uv",[0,0,width,0,width,width,0,width])
    plane.data.materials.append(materials["Corroded"])
    center = (TILE,TILE,0)
    cam.location = (TILE,TILE,.82)
    point(cam,center)
    cam.data.ortho_scale = width
    key.location = (.28,.36,.68)
    key.data.energy = 7.8
    key.data.size = .74
    key.data.size_y = .57
    point(key,center)
    fill.hide_render = True
    render(scene,"repeat",1440,1440)
    delete_mesh(plane)


def farmhouse(scene,cam,key,fill,material):
    from build_lowmark_lime_plaster import build_farmhouse, make_materials, set_material
    plaster = build_farmhouse(scene)
    lime = make_materials()["Maintained"]
    for obj in plaster:
        set_material(obj,lime)
    count = 0
    used = 0
    for obj in tuple(scene.objects):
        if obj.type!="MESH" or not obj.name.startswith("facade_iron"):
            continue
        uv = obj.data.uv_layers.get("UV0_Metric")
        if uv is None:
            raise RuntimeError(f"{obj.name} has no metric hardware UV")
        set_material(obj,material)
        # Only the portion of the native pull ring where a hand bears on
        # it receives polish. Its mask is an in-memory artist override.
        co = np.array([tuple(obj.matrix_world@v.co) for v in obj.data.vertices])
        x,y,z = co.T
        door = (x>3.28)&(x<4.32)&(y<.06)&(y>-.24)&(z>.55)&(z<2.54)
        pull = ((x>3.93)&(x<4.24)&(z>1.33)&(z<1.49)&door).astype(float)
        contact_attribute(obj,pull*.52)
        count += int(np.count_nonzero(door))
        used += 1
    if not count:
        raise RuntimeError("The native Lowmark door had no iron to review")
    print(f"Applied weathered iron to {used} native fixture buffers, "
          f"including {count} front door hardware vertices",flush=True)
    floor,_ = projection_plate(300,300)
    floor.location = (-150,-150,-.035)
    floor.data.materials.append(plain("Farmhouse ground",(.19,.172,.147)))
    key.hide_render = True
    fill.hide_render = True
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = .49
    bpy.ops.object.light_add(type="SUN",location=(-3,-8,10))
    sun = bpy.context.object
    sun.data.energy = 2.44
    sun.data.angle = .15
    point(sun,(4,2.5,0))
    cam.data.type = "PERSP"
    cam.data.lens = 48
    cam.location = (12.8,-12.0,8.4)
    point(cam,(4.1,2.6,2.98))
    render(scene,"farmhouse",1500,1060)
    cam.data.lens = 44
    target = (3.79,-.036,1.46)
    cam.location = (4.18,-2.75,1.63)
    point(cam,target)
    area("Neutral doorway reflection",(4.68,-1.96,2.57),target,15,1.10,.63)
    render(scene,"door",1470,1140)


def review(scene,forge,conditions,materials):
    cam,key,fill,floor = studio(scene)
    clay = plain("Hardware neutral clay",(.44,.44,.44),.53)
    modeled = specimens(forge,conditions[1],clay,high=True)
    render(scene,"clay",1440,900)
    for obj in modeled:
        delete_mesh(obj)
    if materials is None:
        return
    items = specimens(forge,conditions[1],materials["Weathered"])
    for finish in FINISHES:
        for obj in items:
            obj.data.materials[0] = materials[finish]
        render(scene,finish.lower(),1440,900)
    for obj in items:
        obj.data.materials[0] = materials["Weathered"]
    key.location = (.39,.152,.168)
    key.data.energy = .64
    key.data.size = .165
    key.data.size_y = .118
    point(key,(.138,-.026,.005))
    render(scene,"reflection",1440,900)
    for obj in items:
        delete_mesh(obj)
    delete_mesh(floor)
    repeat_view(scene,cam,key,fill,materials)
    farmhouse(scene,cam,key,fill,materials["Weathered"])


def main():
    parser = ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--clay-only",action="store_true")
    mode.add_argument("--bake-only",action="store_true")
    mode.add_argument("--render-only",action="store_true")
    parser.add_argument("--size",type=int,default=1536)
    parser.add_argument("--seed",type=int,default=SEED)
    parser.add_argument("--hammer",type=float,default=.94)
    parser.add_argument("--blackening",type=float,default=.98)
    parser.add_argument("--maintained",type=float,default=.13)
    parser.add_argument("--weathered",type=float,default=.52)
    parser.add_argument("--corroded",type=float,default=.87)
    parser.add_argument("--verify-repeat",action="store_true")
    args = parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    conditions = (args.maintained,args.weathered,args.corroded)
    if (args.size<256 or not all(0<=x<=1 for x in (args.hammer,args.blackening,*conditions))
            or not args.maintained<args.weathered<args.corroded):
        parser.error("Use 256 pixels or more and ascending condition values in [0, 1].")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 1
    scene.cycles.device = "CPU"
    scene.view_settings.view_transform = "AgX"
    forge = Forge(args.seed,args.hammer,args.blackening)
    if args.clay_only:
        review(scene,forge,conditions,None)
        return
    if not args.render_only:
        coverages = []
        for finish,condition in zip(FINISHES,conditions):
            outputs = bake_maps(forge,finish,condition,args.size)
            repeat = bake_maps(forge,finish,condition,args.size) if args.verify_repeat else None
            coverages.append(verify_maps(finish,outputs,repeat))
            save_maps(scene,finish,outputs)
            for img in list(outputs.values())+list((repeat or {}).values()):
                bpy.data.images.remove(img)
        if coverages!=sorted(coverages):
            raise RuntimeError(f"Finish corrosion coverage out of order: {coverages}")
    materials = shader_library()
    if not args.render_only:
        bpy.data.libraries.write(str(ROOT/f"{STEM}.blend"),set(materials.values()),
                                 path_remap="RELATIVE_ALL",fake_user=True,compress=True)
        material_maker_projects()
    if not args.bake_only:
        review(scene,forge,conditions,materials)


if __name__=="__main__":
    main()
