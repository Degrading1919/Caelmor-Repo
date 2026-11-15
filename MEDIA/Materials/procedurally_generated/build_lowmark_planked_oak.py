"""Mill, assemble, and bake Lowmark worked oak in Blender 5.0.1."""

from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
import json
import math
import sys

import bpy
import numpy as np
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from build_lowmark_structural_timber import (
    Wood, around, bake, bake_source, blend, grid_faces, mapped_material, pixels, plain,
    point, profile, ramp, source_material, surface_mesh,
)

STEM = "Lowmark_Planked_Oak_Joinery"
WIDTH, DEPTH = BOUNDS = (2.88, 1.20)
HEIGHT_RANGE = .012
SEED = 37951
STATES = ("Maintained", "Weathered", "Heavily_Aged")
SURFACES = ("Wood", "Planks")
CHANNELS = ("albedo", "normal", "rough", "height")
ROWS = (.183, .218, .166, .239, .197, .197)


class OakStock:
    """Periodic longitudinal oak grain cut through a small set of log figures."""

    def __init__(self, seed, tooling):
        self.seed = seed
        self.tooling = tooling
        rng = np.random.default_rng(seed)
        self.figures = (
            (.57,.28,.52,.117,.032), (1.62,.77,.49,.145,-.042),
            (2.49,1.03,.47,.093,.040), (.18,.09,.45,.128,-.023),
            (1.24,.51,.58,.14,.026), (2.18,.45,.44,.087,-.027),
        )
        self.knots = tuple(
            (x+rng.uniform(-.075,.075), y+rng.uniform(-.029,.029),
             rng.uniform(.027,.081), rng.uniform(.012,.031), rng.uniform(-.22,.22),
             rng.uniform(.40,1.))
            for x,y in ((.22,.27),(.91,.13),(1.49,.34),(2.22,.10),(2.65,.33),
                        (.46,.84),(1.31,.67),(2.02,.63),(2.37,.95),(1.06,1.10))
        )
        self.checks = tuple(
            (x+rng.uniform(-.082,.082), y+rng.uniform(-.03,.03), rng.uniform(.049,.21),
             rng.uniform(.0013,.0049), rng.uniform(.00070,.0031), rng.uniform(-.04,.04))
            for x,y in ((.35,.18),(.73,.39),(1.18,.07),(1.43,.32),(2.36,.19),(2.66,.47),
                        (.59,.63),(1.24,.77),(1.69,.84),(2.25,.93),(2.72,1.13),(.26,1.01))
        )
        self.saw_groups = []
        for cx,cy,heading,count in ((.18,.14,-.19,5),(.48,.69,-.24,5),(.85,.38,.21,6),
                                    (1.36,.23,-.32,4),(1.57,.92,.32,5),(1.91,.60,-.17,7),
                                    (2.34,.84,-.14,5),(2.52,.33,.27,6),(2.73,1.03,.35,3)):
            marks = []
            x = -.045
            for _ in range(count):
                x += rng.uniform(.009,.025)
                marks.append((x,rng.uniform(-.023,.023),heading+rng.uniform(-.115,.115),
                              rng.uniform(.0014,.0031),rng.uniform(.014,.055),
                              rng.uniform(.00009,.00024)))
            self.saw_groups.append((cx,cy,marks))

    def tool_marks(self,x,y):
        saw = np.zeros_like(x)
        for cx,cy,marks in self.saw_groups:
            dx,dy = around(x,cx,WIDTH),around(y,cy,DEPTH)
            patch = (np.abs(dx)<.17)&(np.abs(dy)<.11)
            sx,sy = dx[patch],dy[patch]
            cut = np.zeros_like(sx)
            for x0,y0,incline,span,length,depth in marks:
                t = (sy-y0)/length
                edge = sx-x0-incline*(sy-y0)+.0032*t*t
                fade = 1-ramp(.19,1,np.abs(t))
                width = span*(.34+.66*fade)
                mark = depth*fade*(1-ramp(.12,1,np.abs(edge)/width))
                cut = np.maximum(cut,mark)
            saw[patch] = np.maximum(saw[patch],cut)
        return saw

    def __call__(self, x, y, age):
        u, v = x/WIDTH, y/DEPTH
        seed = self.seed
        waviness = .025*(profile(u,v,6,6,seed+1)-.5)
        waviness += .007*(profile(u,v,13,25,seed+2)-.5)
        waviness += .0019*(profile(u,v,26,53,seed+3)-.5)
        figure = np.zeros_like(x)
        for cx,cy,length,span,amount in self.figures:
            dx,dy = around(x,cx,WIDTH)/length, around(y,cy,DEPTH)/span
            # The face passes through two sides of an arched annual-ring figure.
            bend = dy - .59*(dx*dx-.42)
            weight = np.exp(-1.35*dx**2-1.0*dy**2)
            waviness += 1.37*amount*weight*np.tanh(2.8*bend)
            figure += weight*(1-ramp(.18,1.05,np.abs(bend)))
        warped = y+waviness
        eye, collar, whorl, knot_split = (np.zeros_like(x) for _ in range(4))
        knot_tear = profile(u,v,113,149,seed+5)-.5
        for cx,cy,length,span,tilt,weight in self.knots:
            dx = around(x,cx,WIDTH)
            dy = around(y,cy,DEPTH)-dx*tilt
            a,b = dx/length,dy/span
            warp = np.exp(-.15*a*a-.11*b*b)
            warped += span*1.16*(b/np.sqrt(.52+b*b))*warp
            radius = np.hypot(a,b)+.16*knot_tear
            eye = np.maximum(eye,weight*(1-ramp(.20,.88,radius)))
            collar = np.maximum(collar,ramp(.62,1.07,radius)*(1-ramp(1.08,1.67,radius)))
            whorl = np.maximum(whorl,
                (.5+.5*np.cos(math.tau*(radius*2.45+.055*np.sin(a*6))))**5*
                (1-ramp(.12,1.45,radius)))
            relief_tail = weight*(1-ramp(.38,2.8,np.abs(a)))*ramp(.25,.70,np.abs(a))
            split_line = np.abs(b-.16*np.sin(1.3*a))/(.07+.12*relief_tail)
            knot_split = np.maximum(knot_split,relief_tail*(1-ramp(.14,1.,split_line)))

        grain = warped/DEPTH
        rays_coord = (warped+.016*np.sin(math.tau*(3*u+v)))/DEPTH
        ring_spacing = .020*(profile(u,grain,9,14,seed+7)-.5)
        phase = 192*(warped+ring_spacing)/DEPTH + .63*profile(u,grain,27,51,seed+8)
        wave = .5+.5*np.sin(math.tau*phase)
        summer = wave**4
        annual = (.5+.5*np.sin(math.tau*(phase+.27)))**2.4
        fibers = profile(u,grain,42,192,seed+9)
        line = profile(u,grain,57,326,seed+11)
        band = profile(u,grain,9,35,seed+12)
        pore = ramp(.47,.83,profile(u,grain,206,339,seed+13))*(.21+.79*summer)
        ray = ramp(.72,.91,profile(u,rays_coord,101,125,seed+15))
        ray *= ramp(.31,.68,figure+.14*band)*(1-.61*summer)

        shelter = profile(u,v,8,12,seed+17)
        exposure = ramp(.26,.75,.79*shelter+.21*band)
        patina = age*(.22+.78*exposure)
        burnish = ramp(.48,.73,.65*profile(u,v,14,19,seed+16)+.35*band)
        burnish *= 1-.71*patina
        lifted = patina*ramp(.48,.83,.55*fibers+.45*band)
        # Shallow, intermittent plane tracks and occasional oblique saw traces.
        plane = ramp(.57,.86,profile(u,grain,26,109,seed+20))
        plane *= ramp(.30,.75,profile(u,v,16,14,seed+19))
        saw = self.tool_marks(x,y)*(1-.38*patina)
        tool = self.tooling*(.00021*plane+saw)

        split = np.zeros_like(x)
        flank = np.zeros_like(x)
        for index,(cx,cy,length,span,depth,tilt) in enumerate(self.checks):
            dx = around(x,cx,WIDTH)
            taper = 1-ramp(.11,1,np.abs(dx)/(length*(.60+.55*age)))
            dy = around(y+.52*waviness,cy,DEPTH)-tilt*dx
            dy += .0025*(profile(u,v,31,13,seed+34+index)-.5)
            half = span*(.29+.71*taper)*(.46+.70*age)
            domain = taper*(.21+.79*age)
            groove = (1-ramp(.19,1.0,np.abs(dy)/half))*domain
            if index%4==1:
                fork = np.abs(dy+.043*np.maximum(dx,0))/half
                groove = np.maximum(groove,.58*(1-ramp(.05,.76,fork))*domain*ramp(.02,.08,dx))
            split = np.maximum(split,depth*groove)
            shoulder = ramp(.47,1.09,np.abs(dy)/half)*(1-ramp(1.14,2.65,np.abs(dy)/half))
            flank = np.maximum(flank,shoulder*domain)

        sheet = profile(u,v,13,15,seed+26)
        height = .0045+.00049*(sheet-.5)+.00031*(band-.5)
        height += (.00039+.00060*patina)*(fibers-.47)+.00028*(line-.52)
        height -= (.00025+.00024*patina)*summer + .00030*pore + tool
        height += .00030*collar+.00013*ray-.00161*eye-.00047*whorl
        height -= (.00033+.00177*patina)*knot_split
        height -= split+.00037*lifted
        height += .00025*flank*(line-.21)

        wood = blend(np.array((.197,.107,.045)),np.array((.288,.176,.096)),band)
        oxidized = blend(np.array((.083,.062,.048)),np.array((.188,.174,.153)),exposure)
        color = blend(wood,oxidized,patina)
        growth = .76+.29*band+.31*fibers+.145*line-.18*summer-.30*pore
        tool_color = self.tooling/.82
        growth += -.12*annual-.12*plane*tool_color+.18*ray-.055*saw/.00024*tool_color
        branch = (1-.46*eye)*(1-.29*whorl)*(1-.35*knot_split)
        color *= (np.maximum(.22,growth)*branch)[...,None]
        color = blend(color,np.array((.053,.037,.023)),np.clip(split/.0029,0,.76))
        color = blend(color,np.array((.280,.181,.091)),.17*flank+.067*burnish)
        rough = .50+.28*patina + .09*(fibers-.5)+.08*pore
        rough += .18*split/.0026+.075*lifted+.071*eye-.15*burnish
        return Wood(height,color,np.clip(rough,.34,.92))


@dataclass(frozen=True)
class Board:
    index: int
    start: float
    length: float
    grade: float
    crown: float
    face: float
    drift: float
    offset: tuple[float,float]
    chips: tuple[tuple[float,float,float,float],...]


class Assembly:
    """Six fitted courses with independently cut, stagger-jointed stock."""

    def __init__(self, stock, seed):
        self.stock = stock
        self.bottoms = np.r_[0.,np.cumsum(ROWS)]
        rng = np.random.default_rng(seed+39)
        self.rows = []
        for index,(start,length) in enumerate(((.20,1.28),(.76,1.63),(1.06,1.44),
                                               (.47,1.28),(1.19,1.58),(.58,1.51))):
            row = []
            for i,(begin,end) in enumerate(((start,start+length),(start+length,start+WIDTH))):
                chips = tuple((rng.uniform(.07,.92), rng.choice((0.,1.)), rng.uniform(.014,.059),
                               rng.uniform(.0018,.010)) for _ in range(2+(index+i)%3))
                row.append(Board(index*2+i,begin,end-begin,rng.uniform(-.19,.17),
                                 rng.uniform(-.00155,.0021), rng.uniform(-.00094,.00083),
                                 rng.uniform(-.0034,.0034), (rng.uniform(.1,2.6),rng.uniform(.08,1.16)),chips))
            self.rows.append(tuple(row))

    def __call__(self, x, y, age):
        seed = self.stock.seed
        u,v = x/WIDTH,y/DEPTH
        bed = y+.0017*(profile(u,v,9,7,seed+79)-.5)+.0011*np.sin(math.tau*(2*u+v))
        bed = bed%DEPTH
        height = np.empty_like(x)
        rough = np.empty_like(x)
        color = np.empty((*x.shape,3))
        for index,row in enumerate(self.rows):
            low,high = self.bottoms[index:index+2]
            belongs = (bed>=low)&(bed<high)
            yy = (bed[belongs]-low)/(high-low)
            if not yy.size:
                continue
            xx = x[belongs]
            seam = .0048*(yy-.5)+.00115*np.sin(math.tau*(yy+.37*index))
            progress = (xx+seam-row[0].start)%WIDTH
            hh,rr = np.empty_like(xx),np.empty_like(xx)
            cc = np.empty((len(xx),3))
            for j,board in enumerate(row):
                region = progress<row[0].length if j==0 else progress>=row[0].length
                t = (progress[region]-(row[0].length if j else 0.))/board.length
                across = yy[region]
                xx_board = xx[region]+board.offset[0]
                yy_board = (high-low)*across + board.offset[1] + board.drift*(t-.5)
                local_age = float(np.clip(age*(1.+.28*board.grade)+.18*board.grade,0,1))
                stock = self.stock(xx_board,yy_board,local_age)

                edge = np.minimum(across,1-across)*(high-low)
                end = np.minimum(t,1-t)*board.length
                chip = np.zeros_like(t)
                for at,side,reach,depth in board.chips:
                    distance = np.abs(t-at)*board.length/reach
                    edge_side = np.abs(across-side)*(high-low)
                    distress = (1-ramp(.04,1,distance))*(1-ramp(.001,depth*2.8,edge_side))
                    chip = np.maximum(chip,depth*distress)
                # End grain is vulnerable where an end cut approaches a tipped edge.
                fractured = (1-ramp(.0007,.028,end))*(1-ramp(.0003,.015,edge))
                chipped_edge = np.minimum(edge-chip*(.14+.83*age),end-.0058*age*fractured)
                gap = .00091+.00069*age
                shoulder = ramp(gap, gap+.00305+.0013*age,chipped_edge)
                hue = np.array((1.16,1.05,.86)) if board.index%4==0 else np.array((1.,1.,1.05))
                color_face = stock.color*(1.0+board.grade)*hue
                worn = (1-ramp(.004,.014+.004*age,edge))*shoulder
                worn *= ramp(.38,.78,profile(t,across,18,5,seed+85+board.index,periodic=False))
                loss = np.clip(115*chip+.58*fractured,0,1)*age
                color_face = blend(color_face,np.array((.270,.181,.102)),.27*worn+.38*loss*shoulder)
                end_fibers = profile(t,across,24,62,seed+19+board.index,periodic=False)
                joint = color_face*(.48+.14*end_fibers[...,None])
                crown = board.crown*(.46+.61*age)*(1-(2*across-1)**2)
                bow = .00084*np.sin(math.tau*(.67*t+.16*board.index))*(.46+.65*age)
                dressing = (1-ramp(.002,.059,end))*ramp(.44,.81,end_fibers)
                dressing *= (.51+.49*np.abs(across-.5)*2)*age
                top = .0034+stock.height+board.face+crown+bow-.25*chip*age-.00043*dressing
                color_face *= 1-.16*dressing[...,None]
                hh[region] = .00165 + (top-.00165)*shoulder
                cc[region] = blend(joint,color_face,ramp(.05,.86,shoulder))
                rr[region] = np.clip(.88*(1-shoulder)+shoulder*(stock.roughness-.085*worn+.12*loss),.34,.94)
            height[belongs], color[belongs], rough[belongs] = hh,cc,rr
        return Wood(height,color,rough)


def map_path(surface, finish, channel):
    suffix = "exr" if channel in ("rough","height") else "png"
    return ROOT/f"{STEM}_{surface}_{finish}_{channel}.{suffix}"


def verify_field(field, age):
    x,y = np.meshgrid(np.linspace(-.5,3.2,113),np.linspace(-.3,1.6,93))
    expected = vars(field(x,y,age))
    for dx,dy in ((WIDTH,0),(0,DEPTH),(-WIDTH,-DEPTH)):
        moved = vars(field(x+dx,y+dy,age))
        for key,array in moved.items():
            np.testing.assert_allclose(array,expected[key],rtol=0,atol=3e-10,err_msg=key)


def check_maps(surface, finish, maps, repeat=None):
    title = f"{surface} {finish}"
    data = {key:pixels(image)[:,:,:3] for key,image in maps.items()}
    for key,values in data.items():
        if repeat is not None:
            np.testing.assert_array_equal(values,pixels(repeat[key])[:,:,:3],err_msg=f"{title} {key}")
        if not np.isfinite(values).all() or values.min()<-.0001 or values.max()>1.0001:
            raise RuntimeError(f"Invalid {title} {key} range {values.min()}–{values.max()}")
        for axis in (0,1):
            seam = np.mean(np.abs(np.take(values,0,axis)-np.take(values,-1,axis)))
            lines = tuple(i for i in range(3) if i!=axis)
            internal = np.abs(np.diff(values,axis=axis)).mean(axis=lines).max()
            # The plank tile can cross a real longitudinal joint at V=0.
            if seam>1.65*internal+.0004:
                raise RuntimeError(f"{title} {key} border jump on axis {axis}: {seam} vs {internal}")
    n = data["normal"]*2-1
    if np.max(np.abs(np.linalg.norm(n,axis=-1)-1))>.026:
        raise RuntimeError(f"Invalid {title} normals")
    h = HEIGHT_RANGE*data["height"][:,:,0]
    dy,dx = np.gradient(h,DEPTH/h.shape[0],WIDTH/h.shape[1])
    match = [np.corrcoef((-v).ravel(),n[:,:,i].ravel())[0,1] for i,v in enumerate((dx,dy))]
    if min(match)<.68:
        raise RuntimeError(f"{title} normal and height mismatch: {match}")
    bias = np.median(np.abs(dy))/np.median(np.abs(dx))
    if bias<1.45:
        raise RuntimeError(f"{title} grain on wrong axis: {bias:.2f}")
    print(f"{title} | normal/height {np.round(match,3)} | across/along slope {bias:.2f}"
          f" | median roughness {np.median(data['rough'][:,:,0]):.3f}"
          f" | wrap OK | independent pixels {'match' if repeat is not None else 'unchecked'}",flush=True)
    return float(np.median(data["rough"][:,:,0]))


def save_maps(scene, surface, finish, maps):
    settings = scene.render.image_settings
    for channel,img in maps.items():
        path = str(map_path(surface,finish,channel))
        if channel=="normal":
            img.filepath_raw = path
            img.file_format = "PNG"
            img.save()
        elif channel=="albedo":
            scene.view_settings.view_transform = "Standard"
            scene.view_settings.look = "None"
            settings.file_format,settings.color_mode,settings.color_depth = "PNG","RGB","8"
            img.save_render(path,scene=scene)
            scene.view_settings.view_transform = "AgX"
        else:
            settings.file_format,settings.color_mode,settings.color_depth = "OPEN_EXR","RGB","16"
            settings.exr_codec = "ZIP"
            img.save_render(path,scene=scene)


def forget(obj):
    mesh = obj.data
    bpy.data.objects.remove(obj,do_unlink=True)
    bpy.data.meshes.remove(mesh)


def run_bakes(scene, fields, ages, size, depth_samples, verify):
    material,color = source_material()
    material.name = "Lowmark oak | wood stock bake"
    for surface,field in fields.items():
        roughness = []
        for finish,age in zip(STATES,ages):
            verify_field(field,age)
            runs = []
            for _ in range(2 if verify else 1):
                mesh = bake_source(BOUNDS,lambda x,y:field(x,y,age),sampling=depth_samples)
                mesh.name = f"{surface} {finish} | physical relief"
                mesh.data.materials.append(material)
                runs.append(bake(BOUNDS,f"{surface} {finish}",mesh,material,color,size,HEIGHT_RANGE))
                forget(mesh)
            roughness.append(check_maps(surface,finish,runs[0],runs[1] if verify else None))
            save_maps(scene,surface,finish,runs[0])
            for maps in runs:
                for image in maps.values():
                    bpy.data.images.remove(image)
        if sorted(roughness)!=roughness:
            raise RuntimeError(f"Condition does not increase median {surface} roughness: {roughness}")
    bpy.data.materials.remove(material)


def material_maker(surface, finish):
    # Native Material Maker's X and Z normal signs differ from its Blender
    # profile. Its height input is depth measured inward from the face.
    definitions = []
    for i,channel in enumerate(CHANNELS):
        definitions.append((channel,"image",-590,i*225,{
            "image":f"%PROJECT_PATH%/{map_path(surface,finish,channel).name}",
            "fix_ar":False,"clamp":False,
        }))
    definitions.extend((
        ("normal_components","decompose",-375,230,{}),
        ("native_x","invert",-169,173,{}),
        ("native_z","invert",-169,400,{}),
        ("native_normal","combine",36,250,{}),
        ("depth_from_height","invert",-169,690,{}),
        ("Material","material",252,215,{"size":10,"metallic":0.,"roughness":1.,
                                       "normal":1.,"depth_scale":HEIGHT_RANGE/WIDTH,"ao":1.}),
    ))
    nodes = [{"name":name,"type":node_type,"seed_int":0,"node_position":{"x":x,"y":y},
              "parameters":parameters} for name,node_type,x,y,parameters in definitions]
    nodes[-1]["export_paths"] = {}
    connections = [
        ("albedo",0,"Material",0), ("rough",0,"Material",2),
        ("normal",0,"normal_components",0), ("normal_components",0,"native_x",0),
        ("normal_components",2,"native_z",0), ("native_x",0,"native_normal",0),
        ("normal_components",1,"native_normal",1), ("native_z",0,"native_normal",2),
        ("native_normal",0,"Material",4), ("height",0,"depth_from_height",0),
        ("depth_from_height",0,"Material",6),
    ]
    project = {"name":"Graph","type":"graph","label":f"Lowmark Oak | {surface} {finish.replace('_',' ')}",
               "seed_int":0,"node_position":{"x":0,"y":0},"parameters":{},"nodes":nodes,
               "connections":[{"from":a,"from_port":b,"to":c,"to_port":d} for a,b,c,d in connections]}
    path = ROOT/f"{STEM}_{surface}_{finish}.ptex"
    path.write_text(json.dumps(project,indent=2)+"\n",encoding="utf-8")


def library(write):
    materials = {}
    for surface in SURFACES:
        for finish in STATES:
            name = f"Lowmark Planked Oak | {surface} {finish.replace('_',' ')}"
            mat = mapped_material(name,BOUNDS,lambda key:map_path(surface,finish,key))
            mat.node_tree.nodes.get("Principled BSDF").inputs["Specular IOR Level"].default_value = .37
            mat["caelm_repeat_metres"] = BOUNDS
            mat["caelm_height_range_m"] = HEIGHT_RANGE
            materials[surface,finish] = mat
            if write:
                material_maker(surface,finish)
    if write:
        bpy.data.libraries.write(str(ROOT/f"{STEM}.blend"),set(materials.values()),
                                 path_remap="RELATIVE_ALL",fake_user=True,compress=True)
    return materials


def uv_surface(name, u, v, z, material, phase=(0.,0.)):
    xyz = np.column_stack((u.ravel(),v.ravel(),np.broadcast_to(z,u.shape).ravel()))
    faces = grid_faces(u.shape[1],u.shape[0])
    obj = surface_mesh(name,xyz,faces)
    obj.data.materials.append(material)
    obj.data.polygons.foreach_set("use_smooth",np.ones(len(faces),bool))
    uv = obj.data.uv_layers.new(name="UV0_Metric")
    uv_coord = xyz[:,:2]+phase
    uv.data.foreach_set("uv",uv_coord[faces.ravel()].astype(np.float32).ravel())
    return obj


def slab(name, size, material, *, at=(0.,0.,0.), phase=(0.,0.), relief=None, thickness=.024):
    width,depth = size
    sx = max(2,int(width/.0035)) if relief else 2
    sy = max(2,int(depth/.0035)) if relief else 2
    x,y = np.meshgrid(np.linspace(0,width,sx),np.linspace(0,depth,sy))
    z = relief(x+phase[0],y+phase[1]) if relief else 0.
    obj = uv_surface(name,x,y,z,material,phase)
    obj.location = at
    if thickness:
        edge = obj.modifiers.new("Section thickness","SOLIDIFY")
        edge.thickness = thickness
        edge.use_quality_normals = True
    return obj


def individual_board(name, length, width, location, material, phase, index):
    # Board ends remain separate mesh edges. A small chip has a real silhouette.
    a,b = np.meshgrid(np.linspace(0,1,148),np.linspace(0,1,25))
    x = length*a
    y = width*b + .0025*np.sin(math.tau*(.67*a+.21*index))
    scar = 1-ramp(.007,.032,np.abs(x-length*(.24+.16*(index%3))))
    y += .0051*scar*(1-b)**5 + (a-.5)*(.006*(index-1))
    z = (.0009+.0004*index)*np.sin(math.pi*b) + .0009*np.sin(math.tau*(a+.22*index))
    board = uv_surface(name,x,y,z,material,phase)
    board.location = location
    section = board.modifiers.new("24 mm plank section","SOLIDIFY")
    section.thickness = .024
    section.use_quality_normals = True
    rounded = board.modifiers.new("Worked corners","BEVEL")
    rounded.width = .003
    rounded.segments = 3
    rounded.limit_method = "ANGLE"
    return board


def render(scene, label, width, height):
    scene.render.resolution_x,scene.render.resolution_y = width,height
    scene.render.resolution_percentage = 100
    settings = scene.render.image_settings
    settings.file_format,settings.color_mode,settings.color_depth = "PNG","RGB","8"
    scene.render.filepath = str(ROOT/f"{STEM}_{label}.png")
    bpy.ops.render.render(write_still=True)


def frame(camera, target, offset, scale):
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = scale
    camera.location = Vector(target)+Vector(offset)
    point(camera,target)


def studio(scene, draft):
    from build_lowmark_forged_iron import area
    scene.world = bpy.data.worlds.new("Joiner's neutral studio")
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (.55,.55,.55,1)
    background.inputs["Strength"].default_value = .21
    scene.cycles.use_denoising = True
    scene.cycles.samples = 18 if draft else 48
    bpy.ops.object.camera_add()
    camera = scene.camera = bpy.context.object
    key = area("Window key",(-.42,.78,1.16),(.8,.42,0),61,.92,.53)
    fill = area("Neutral fill",(1.75,-1.62,2.25),(.8,.42,0),33,2.1,1.35)
    ground = slab("Studio bench",(200,200),plain("Warm studio gray",(.144,.143,.139)),
                  at=(-100,-100,-.041),thickness=0.)
    return camera,key,fill,ground


def review_detail(scene, mats, camera, key, fill, draft):
    target = (.455,.257,0.)
    sample = slab("Heavily aged joint detail",(.91,.52),mats["Planks","Heavily_Aged"],
                  phase=(1.04,.263))
    key.location = (-.16,.73,.51)
    key.data.energy = 32
    key.data.size,key.data.size_y = .49,.24
    point(key,target)
    fill.data.energy = 18
    frame(camera,target,(.13,-.67,.91),1.13)
    render(scene,"detail",960 if draft else 1570,620 if draft else 1050)
    forget(sample)


def review_surfaces(scene, oak, ages, mats, camera, key, fill, draft):
    width,height = (960,550) if draft else (1570,865)
    clay = plain("Neutral oak clay",(.38,.38,.38),.66)
    phase = (.39,.118)
    frame(camera,(1.03,.424,0),(.48,-1.34,2.13),2.37)
    sample = slab("Cut boards and recessed bedding (high geometry)",(2.05,.86),clay,phase=phase,
                  relief=lambda x,y:oak(x,y,ages[1]).height)
    render(scene,"clay",width,height)
    forget(sample)

    sample = slab("Plank bake across one receiver",(2.05,.86),mats["Planks","Weathered"],phase=phase)
    for finish in STATES:
        sample.data.materials[0] = mats["Planks",finish]
        render(scene,finish.lower(),width,height)
    forget(sample)

    from build_lowmark_forged_iron import area
    side = area("Wood fiber raking light",(.21,.86,.50),(.72,.30,0),19,.62,.22)
    key.data.energy = 38
    frame(camera,(.73,.347,0),(.56,-.98,1.38),1.85)
    sources = (
        individual_board("Planed show face",1.40,.198,(0,0,0),mats["Wood","Maintained"],(.13,.15),0),
        individual_board("Weathered joinery stock",1.25,.225,(.095,.219,0),mats["Wood","Weathered"],(.91,.59),1),
        individual_board("Aged stock",1.46,.200,(-.035,.470,0),mats["Wood","Heavily_Aged"],(.36,.12),2),
    )
    render(scene,"wood_stock",width,height)
    for obj in sources:
        forget(obj)
    bpy.data.objects.remove(side,do_unlink=True)

    # The lit swatch presents four complete tiles. The broad floor repeats at
    # the same density as the smaller samples.
    sample = slab("2 by 2 repeat",(2*WIDTH,2*DEPTH),mats["Planks","Weathered"],thickness=0.)
    key.data.energy = 270
    key.location = (1.13,1.15,2.91)
    point(key,(2.60,1.13,0))
    fill.data.energy = 75
    frame(camera,(WIDTH,DEPTH,0),(0,0,5),2*WIDTH)
    render(scene,"repeat",1200 if draft else 1728,500 if draft else 720)
    sample.data.materials[0] = mats["Wood","Weathered"]
    render(scene,"wood_repeat",1200 if draft else 1728,500 if draft else 720)
    forget(sample)

    floor = slab("Lowmark boarded floor specimen",(4.62,3.15),mats["Planks","Maintained"],
                 at=(0,0,.047),phase=(.41,.17),thickness=.073)
    key.data.energy = 267
    key.location = (-.94,.38,2.92)
    point(key,(2.,1.82,0))
    frame(camera,(2.27,1.59,0),(2.3,-3.6,3.8),6.6)
    render(scene,"floor",width,height)
    forget(floor)


def orient_and_phase(obj):
    """Vary stock per physical board in a review copy of the native buffer."""
    mesh = obj.data
    layer = mesh.uv_layers.get("UV0_Metric")
    if layer is None:
        raise RuntimeError(f"{obj.name} has no native metric UV")
    parent = list(range(len(mesh.vertices)))

    def component(vertex):
        while parent[vertex]!=vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in mesh.edges:
        a,b = edge.vertices
        parent[component(b)] = component(a)
    components = {}
    counts = {"vertical":0,"horizontal":0}
    rng = np.random.default_rng(709+len(mesh.vertices))
    for face in mesh.polygons:
        loops = tuple(face.loop_indices)
        xyz = [mesh.vertices[mesh.loops[li].vertex_index].co for li in loops]
        edges = [xyz[(j+1)%len(loops)]-p for j,p in enumerate(xyz)]
        longest = max(range(len(edges)),key=lambda j:edges[j].length_squared)
        edge = edges[longest]
        if edge.length>.12:
            step = layer.data[loops[(longest+1)%len(loops)]].uv-layer.data[loops[longest]].uv
            if abs(step.y)>.002 or abs(abs(step.x)-edge.length)>.002:
                raise RuntimeError(f"{obj.name} long edge disagrees with U in the generator")
            counts["vertical" if abs(edge.z)>.95*edge.length else "horizontal"] += 1
        index = component(face.vertices[0])
        if index not in components:
            components[index] = Vector((rng.uniform(0,WIDTH),rng.uniform(0,DEPTH)))
        phase = components[index]
        for li in loops:
            layer.data[li].uv += phase
    print(f"{obj.name} | {len(components)} pieces | face grain {counts}",flush=True)
    if not counts["vertical"] or not counts["horizontal"]:
        raise RuntimeError(f"Expected both face orientations in {obj.name}")


def farmhouse(scene, materials, camera, key, fill, draft):
    from build_lowmark_forged_iron import area
    from build_lowmark_lime_plaster import build_farmhouse, make_materials, set_material
    plaster = build_farmhouse(scene)
    lime = make_materials()["Maintained"]
    for obj in plaster:
        set_material(obj,lime)
    with bpy.data.libraries.load(str(ROOT/"Lowmark_Forged_Iron_Hardware.blend")) as (_,loaded):
        loaded.materials = ["Lowmark Forged Iron | Weathered"]
    iron = loaded.materials[0]
    if iron is None:
        raise RuntimeError("Approved forged iron missing")
    parts = {"doors":[], "shutters":[]}
    for obj in tuple(scene.objects):
        if obj.type!="MESH":
            continue
        if obj.name.startswith("facade_iron"):
            set_material(obj,iron)
        for part,buffers in parts.items():
            if obj.name.startswith(f"facade_{part}"):
                set_material(obj,materials["Wood","Weathered"])
                orient_and_phase(obj)
                buffers.append(obj)
    if not all(parts.values()):
        raise RuntimeError("No native door or shutter review buffer")
    key.hide_render = True
    fill.hide_render = True
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = .49
    bpy.ops.object.light_add(type="SUN",location=(-4,-5,7))
    sun = bpy.context.object
    sun.data.energy = 2.05
    sun.data.angle = .21
    point(sun,(4.8,.92,0))
    camera.data.type = "PERSP"
    camera.data.lens = 51
    camera.location = (8.80,-7.95,3.24)
    point(camera,(4.44,.04,2.11))
    width,height = (1030,745) if draft else (1640,1170)
    render(scene,"farmhouse",width,height)
    area("Soft doorway bounce",(4.83,-2.05,2.71),(3.78,0,1.45),27,1.67,.95)
    camera.data.lens = 47
    camera.location = (4.14,-2.60,1.62)
    point(camera,(3.78,.015,1.47))
    render(scene,"door",width,height)

    # Find the right-hand window's two shutter leaves in the native front buffer.
    points = [obj.matrix_world@v.co for obj in parts["shutters"] for v in obj.data.vertices]
    front = [p for p in points if 4.74<p.x<8.16 and -.27<p.y<.07 and .9<p.z<2.65]
    if not front:
        raise RuntimeError("Could not locate native front shutter pair")
    center = .5*(min(p.x for p in front)+max(p.x for p in front))
    middle_z = .5*(min(p.z for p in front)+max(p.z for p in front))
    camera.location = (center+.69,-2.36,middle_z+.25)
    camera.data.lens = 53
    point(camera,(center,.03,middle_z))
    render(scene,"shutters",width,height)


def main():
    parser = ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--bake-only",action="store_true")
    mode.add_argument("--render-only",action="store_true")
    parser.add_argument("--draft",action="store_true")
    parser.add_argument("--verify-repeat",action="store_true")
    parser.add_argument("--verify-exports",action="store_true")
    parser.add_argument("--seed",type=int,default=SEED)
    parser.add_argument("--tooling",type=float,default=.82)
    parser.add_argument("--maintained",type=float,default=.11)
    parser.add_argument("--weathered",type=float,default=.49)
    parser.add_argument("--heavily-aged",type=float,default=.87)
    args = parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    ages = (args.maintained,args.weathered,args.heavily_aged)
    if args.seed<0:
        parser.error("Use a nonnegative seed.")
    if not (0<=ages[0]<ages[1]<ages[2]<=1 and 0<=args.tooling<=1):
        parser.error("Use three strictly ascending conditions in [0,1] and tooling in [0,1].")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 1
    scene.cycles.device = "CPU"
    scene.view_settings.view_transform = "AgX"
    stock = OakStock(args.seed,args.tooling)
    assembly = Assembly(stock,args.seed)
    size = (1008,420) if args.draft else (2400,1000)
    if args.verify_exports:
        for surface in SURFACES:
            for finish in STATES:
                maps = {}
                for channel in CHANNELS:
                    img = bpy.data.images.load(str(map_path(surface,finish,channel)))
                    img.colorspace_settings.name = "sRGB" if channel=="albedo" else "Non-Color"
                    if tuple(img.size)!=size:
                        raise RuntimeError(f"{img.filepath} was not exported at {size}")
                    maps[channel] = img
                check_maps(surface,finish,maps)
                for img in maps.values():
                    bpy.data.images.remove(img)
        return
    if not args.render_only:
        run_bakes(scene,{"Wood":stock,"Planks":assembly},ages,size,624 if args.draft else 1050,
                  args.verify_repeat)
    materials = library(write=not args.render_only)
    if not args.bake_only:
        camera,key,fill,_ = studio(scene,args.draft)
        review_surfaces(scene,assembly,ages,materials,camera,key,fill,args.draft)
        review_detail(scene,materials,camera,key,fill,args.draft)
        farmhouse(scene,materials,camera,key,fill,args.draft)


if __name__=="__main__":
    main()
