"""Build Lowmark's shared ground material fields and Blender review scenes."""

from argparse import ArgumentParser
from pathlib import Path
import json
import math
import sys

import bpy
import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from build_lowmark_structural_timber import blend, grid_faces, pixels, plain, point, profile, ramp, surface_mesh

STEM = "Lowmark_Packed_Earth_Worn_Footpaths"
SEED = 81379
LENGTH,SPAN = 3.60,2.40
RELIEF = .082
FINISHES = ("Packed_Earth","Worn_Footpath")
CHANNELS = ("albedo","rough","normal","height")
PATH_BLEND = "path_blend"
VERGE = "verge"
UV = "UV0_Metric"


def map_path(key):
    extension = "png" if key.endswith("albedo") else "exr"
    return ROOT/f"{STEM}_{key}.{extension}"


def metric_grid(size):
    width,height = size
    return np.meshgrid((np.arange(width)+.5)*LENGTH/width,
                       (np.arange(height)+.5)*SPAN/height)


def neighbourhood(size,cx,cy,reach):
    """Visit the same texel centers when a feature crosses a tile boundary."""
    w,h = size
    sx,sy = LENGTH/w,SPAN/h
    x = np.arange(math.floor((cx-reach)/sx),math.ceil((cx+reach)/sx))
    y = np.arange(math.floor((cy-reach)/sy),math.ceil((cy+reach)/sy))
    return np.ix_(y%h,x%w),(x[None,:]+.5)*sx-cx,(y[:,None]+.5)*sy-cy


class Soil:
    def __init__(self,seed,compaction,gravel,moisture,traces,erosion,verge):
        self.seed = seed
        self.compaction,self.moisture,self.traces = compaction,moisture,traces
        self.erosion,self.verge = erosion,verge
        rng = np.random.default_rng(seed)
        self.stones = []
        centers = ((.39,.63),(1.18,1.94),(2.72,.48),(3.26,1.62),(.11,2.38),
                   (2.18,1.38),(1.44,.24),(3.48,.79),(1.06,1.26),(2.60,2.11))
        palettes = ((.268,.230,.185),(.234,.232,.201),(.311,.276,.220),(.192,.164,.131),
                    (.318,.326,.295),(.258,.204,.153))
        for count,r0,r1,scale in ((805,.0065,.026,.52),(1150,.0024,.0078,.49),(52,.022,.055,.66)):
            for i in range(round(count*gravel)):
                if i%3:
                    x,y = rng.uniform(0,LENGTH),rng.uniform(0,SPAN)
                else:
                    cx,cy = centers[int(rng.integers(len(centers)))]
                    x,y = cx+rng.normal(0,.16),cy+rng.normal(0,.115)
                a = r0+(r1-r0)*rng.random()**2.45
                b = a*rng.uniform(.52,1.07)
                ang = rng.uniform(-math.pi,math.pi)
                count_faces = int(rng.integers(5,9))
                angles = (np.arange(count_faces)+rng.uniform(-.25,.25,count_faces))*math.tau/count_faces
                radius = rng.uniform(.76,1.21,count_faces)
                fac = tuple(zip(np.cos(angles)/radius,np.sin(angles)/radius))
                tilt = rng.uniform(-.40,.40,2)
                clr = np.array(palettes[int(rng.integers(len(palettes)))])*rng.uniform(.68,1.18)
                self.stones.append((x%LENGTH,y%SPAN,a,b,ang,fac,tilt,clr,a*scale*rng.uniform(.50,1.24)))
        self.stones.sort(key=lambda v:v[-1])
        rng = np.random.default_rng(seed+41)
        self.prints = [(x,y,rng.uniform(-.36,.37)+(math.pi if i%4==1 else 0),
                        rng.uniform(.84,1.18),rng.uniform(.0015,.0045),rng.uniform(.48,1.))
                       for i,(x,y) in enumerate(((.26,.54),(.69,1.03),(1.42,1.65),(1.81,.76),
                                                 (2.28,1.36),(2.83,.41),(3.15,1.84),(3.52,1.11)))]
        self.channels = [(x,y,rng.uniform(.20,.54),rng.uniform(.009,.026),
                          rng.uniform(-.36,.36),rng.uniform(.0013,.0044),rng.uniform(-.079,.079))
                         for x,y in ((.18,.17),(.42,1.35),(.88,.54),(1.12,2.08),(1.47,.92),
                                     (1.88,1.76),(2.26,.36),(2.62,1.21),(3.05,2.29),(3.31,.72))]

    def shoulder(self,x,side):
        """Centerline-distance masks, sampled with relative U and signed V in metres."""
        u = x/LENGTH
        v = side/SPAN+.5
        seed = self.seed
        edge = np.abs(side+.082*(profile(u,v,7,6,seed+29)-.5)
                      +.12*(profile(u,v,4,4,seed+30)-.5))
        irregular = .156*(profile(u,v,12,10,seed+31)-.5)
        path = 1-ramp(.47+irregular,.99+irregular,edge)
        patches = profile(u,v,13,19,seed+35)
        shelter = .62*profile(u,v,6,9,seed+34)+.38*patches
        fringe = ramp(.52,.89,edge)*(1-ramp(.94,1.194,edge))
        verge = np.clip(1.55*self.verge*fringe*ramp(.35,.76,shelter),0,1)
        verge *= 1-ramp(1.105,1.19,np.abs(side))
        path *= 1-.34*verge
        path *= 1-ramp(1.05,1.17,np.abs(side))
        return path,verge

    def drainage(self,size):
        cuts = np.zeros(size[::-1],np.float32)
        for i,(cx,cy,length,width,slant,depth,bow) in enumerate(self.channels):
            patch,x,y = neighbourhood(size,cx,cy,length+.075)
            f = x/length
            offset = slant*x+bow*(f*f-.26)+.007*np.sin(12*x+i)
            taper = (1-ramp(.22,1.,np.abs(f)))*(.49+.51*(.5+.5*np.cos(16*x+i/2)))
            cut = depth*taper*(1-ramp(.14,1.,np.abs(y-offset)/(width*(.57+.43*taper))))
            cuts[patch] = np.maximum(cuts[patch],cut)
        return cuts

    def footmarks(self,size):
        dents = np.zeros(size[::-1],np.float32)
        torn = np.zeros_like(dents)
        for i,(cx,cy,angle,scale,depth,broken) in enumerate(self.prints):
            patch,x,y = neighbourhood(size,cx,cy,.16)
            cs,sn = math.cos(angle),math.sin(angle)
            along = (cs*x+sn*y)/scale
            across = (-sn*x+cs*y)/scale
            toe = 1-ramp(.40,1.,np.hypot((along-.047)/.063,(across-.005)/.033))
            heel = 1-ramp(.36,1.,np.hypot((along+.064)/.041,(across+.004)/.026))
            middle = (1-ramp(.38,1.,np.hypot((along+.015)/.054,(across+.005)/.021)))*.31
            track = np.maximum.reduce((toe,heel,middle))
            shredded = profile((x+cx)/LENGTH,(y+cy)/SPAN,225,168,self.seed+i+46)
            partial = ramp(.20,.63,.63*shredded+.37*(1-broken*np.sin(14*along+i)**2))
            pressed = depth*track*partial
            rim = ramp(.05,.29,track)*(1-ramp(.31,.58,track))*partial
            dents[patch] = np.maximum(dents[patch],pressed)
            torn[patch] = np.maximum(torn[patch],rim)
        return dents*self.traces,torn*self.traces

    def aggregate(self,size,height,color,rough,moisture,sediment,worn):
        raised = np.zeros_like(height)
        coverage = np.zeros_like(height)
        for x,y,a,b,angle,facets,tilt,stone_rgb,thickness in self.stones:
            patch,dx,dy = neighbourhood(size,x,y,max(a,b)*2.24)
            cs,sn = math.cos(angle),math.sin(angle)
            u = (cs*dx+sn*dy)/a
            v = (-sn*dx+cs*dy)/b
            limit = np.maximum.reduce([u*nx+v*ny for nx,ny in facets])
            rim = 1-ramp(.57,1.06,limit)
            face = .74+.18*np.minimum(-.20*u+.31*v,.48*u-.12*v)+tilt[0]*u*.39+tilt[1]*v*.39
            dome = rim*np.clip(face,.26,1.19)
            soil = sediment[patch]
            exposure = np.clip(.96-.44*soil-.15*worn,0,1)
            h = thickness*dome*exposure*(1-.14*worn)
            top = h>raised[patch]
            if not top.any():
                continue
            blend_mask = np.where(top,ramp(.19,.72,rim)*exposure,0)
            raised[patch] = np.maximum(raised[patch],h)
            coverage[patch] = np.maximum(coverage[patch],blend_mask)
            rgb = stone_rgb*(.88-.21*moisture[patch][...,None])
            rgb *= (1+.17*(soil[...,None]-.50)+.16*(dome[...,None]-.38))
            color[patch] = blend(color[patch],rgb,blend_mask)
            rough[patch] = rough[patch]*(1-blend_mask)+(.74-.15*moisture[patch])*blend_mask
        return height+raised,coverage

    def raster(self,size,worn):
        x,y = metric_grid(size)
        u,v = x/LENGTH,y/SPAN
        seed = self.seed
        coarse = profile(u,v,5,4,seed)
        pocket = profile(u,v,11,9,seed+2)
        clod = profile(u,v,43,30,seed+4)
        sharp = profile(u+.007*(clod-.5),v,89,69,seed+5)
        grit = .63*profile(u+.009*(sharp-.5),v+.011*(clod-.5),310,228,seed+8)
        grit += .37*profile(u,v,157,163,seed+120)
        powder = profile(u,v,607,407,seed+9)
        thin = profile(u,v,88,193,seed+12)
        wet = self.moisture*ramp(.24,.75,.61*pocket+.26*coarse+.13*clod)
        clay = ramp(.20,.77,.47*coarse+.37*pocket+.16*clod)
        sediment = ramp(.33,.71,.43*pocket+.32*sharp+.25*grit)
        compact = self.compaction*(.30 if not worn else .91)
        bound = ramp(.36,.75,.44*clod+.39*sharp+.17*grit)
        surface = .023*(coarse-.49)*(1-.69*compact)
        surface += .011*(pocket-.53)*(1-.52*compact)
        surface += .0094*(bound-.45)*(1-.91*compact)
        surface += .00225*(grit-.50)*(1-.58*compact)+.00060*(powder-.47)
        surface += (.0021+.0015*worn)*(sediment-.5)
        surface -= .0095*compact
        cuts = self.drainage(size)*self.erosion*(.31 if not worn else .88)
        dents,rims = self.footmarks(size) if worn else (0.,0.)
        surface -= cuts+dents
        surface += .00155*rims

        dry = blend(np.array((.114,.071,.038)),np.array((.178,.121,.066)),clay)
        dry = blend(dry,np.array((.222,.155,.088)),.38*worn+.22*sediment)
        dark = blend(np.array((.063,.042,.022)),np.array((.097,.073,.048)),clay)
        color = blend(dry,dark,wet*(.52 if worn else .79))
        color *= (.87+.18*clod+.14*sharp+.062*grit+.043*powder)[...,None]
        compression = np.clip(dents/.0033,0,1)
        color *= (1-.13*np.clip(cuts/.003,0,1)-.12*compression)[...,None]
        color = blend(color,np.array((.221,.164,.106)),.24*rims if worn else np.zeros_like(surface))
        rough = np.clip(.855+.073*(bound-.40)+.032*(powder-.5)-.177*wet-.052*compact
                        -.055*compression,.61,.96)
        height,stone = self.aggregate(size,surface,color,rough,wet,sediment,worn)

        # Thin, low growth in sheltered soil, kept below the height of gravel.
        growth = ramp(.50,.82,profile(u,v,18,15,seed+66))
        growth *= ramp(.49,.82,.71*clod+.29*thin)*(1-stone)
        green = np.clip(growth*self.verge*(.42 if worn else 1.15),0,1)
        olive = blend(np.array((.127,.113,.048)),np.array((.078,.090,.039)),thin)
        color = blend(color,olive,green*.81)
        height += .0018*green
        return height,color,rough,stone


def normals(height,size):
    w,h = size
    du = (np.roll(height,-1,axis=1)-np.roll(height,1,axis=1))/(2*LENGTH/w)
    dv = (np.roll(height,-1,axis=0)-np.roll(height,1,axis=0))/(2*SPAN/h)
    n = np.stack((-du,-dv,np.ones_like(du)),axis=-1)
    return .5+.5*n/np.linalg.norm(n,axis=-1)[...,None]


def maps(soil,size):
    data = {}
    for finish,worn in zip(FINISHES,(False,True)):
        height,color,rough,stone = soil.raster(size,worn)
        data.update({f"{finish}_albedo":color,f"{finish}_rough":rough,f"{finish}_normal":normals(height,size),
                     f"{finish}_height":.5+height/RELIEF})
        print(f"{finish} | gravel visible {np.mean(stone>.32):.1%} | relief "
              f"{height.min()*1000:.1f}–{height.max()*1000:.1f} mm",flush=True)
    xu,yv = metric_grid(size)
    data[PATH_BLEND],data[VERGE] = soil.shoulder(xu,yv-SPAN/2)
    return {key:((np.repeat(value[:,:,None],3,axis=2) if value.ndim==2 else value).astype(np.float32))
            for key,value in data.items()}


def verify(data,size,reopened=False):
    w,h = size
    for key,value in data.items():
        if value.shape!=(h,w,3) or not np.isfinite(value).all() or not (0<=value.min()<=value.max()<=1):
            raise RuntimeError(f"Unusable {key} map")
        for axis in (0,1):
            seam = np.abs(np.take(value,0,axis)-np.take(value,-1,axis)).mean()
            internal = np.abs(np.diff(value,axis=axis)).mean(axis=tuple(i for i in range(3) if i!=axis))
            if seam>internal.max()*1.30+.0003:
                raise RuntimeError(f"{key} discontinuity across tile axis {axis}")
    for finish in FINISHES:
        field = (data[f"{finish}_height"][:,:,0]-.5)*RELIEF
        expected = normals(field,size)
        actual = data[f"{finish}_normal"]
        if np.max(np.abs(np.linalg.norm(2*actual-1,axis=-1)-1))>.003:
            raise RuntimeError(f"{finish} contains non-unit normals")
        if np.quantile(np.linalg.norm(actual-expected,axis=-1),.99)>(.012 if reopened else .00001):
            raise RuntimeError(f"{finish} normals disagree with signed height")
    for key in (PATH_BLEND,VERGE):
        if np.max(data[key][[0,-1]])>0:
            raise RuntimeError(f"{key} fails to close at the outer boundary")
    if np.min(data[PATH_BLEND][h//2,:,0])<.9:
        raise RuntimeError("Inconsistent walking surface at the path center")
    print(f"{'Reopened' if reopened else 'Generated'} maps passed channel, metric relief and seam checks",flush=True)


def export(scene,data):
    settings = scene.render.image_settings
    settings.color_mode = "RGB"
    for key,value in data.items():
        h,w = value.shape[:2]
        rgba = np.ones((h,w,4),np.float32)
        rgba[:,:,:3] = value
        img = bpy.data.images.new(key,w,h,alpha=False,float_buffer=True)
        if key.endswith("albedo"):
            img.colorspace_settings.name = "Linear Rec.709"
            scene.view_settings.view_transform = "Standard"
            scene.view_settings.look = "None"
            settings.file_format,settings.color_depth = "PNG","8"
        else:
            img.colorspace_settings.name = "Non-Color"
            scene.view_settings.view_transform = "AgX"
            settings.file_format,settings.color_depth = "OPEN_EXR","16"
            settings.exr_codec = "ZIP"
        img.pixels.foreach_set(rgba.ravel())
        img.save_render(str(map_path(key)),scene=scene)
        bpy.data.images.remove(img)
    scene.view_settings.view_transform = "AgX"


def reopen(size):
    data = {}
    for key in [*(f"{finish}_{channel}" for finish in FINISHES for channel in CHANNELS),PATH_BLEND,VERGE]:
        im = bpy.data.images.load(str(map_path(key)))
        im.colorspace_settings.name = "sRGB" if key.endswith("albedo") else "Non-Color"
        data[key] = pixels(im)[:,:,:3]
        bpy.data.images.remove(im)
    verify(data,size,reopened=True)


def material(finish):
    mixed = finish=="Transition"
    name = "Lowmark Ground | "+finish.replace("_"," ")
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat["caelm_tile_metres"] = (LENGTH,SPAN)
    mat["caelm_height_range_metres"] = RELIEF
    ns,links = mat.node_tree.nodes,mat.node_tree.links

    def place(node,x,y,label=None):
        n = ns.new(node)
        n.location = (x,y)
        if label:
            n.label = label
        return n

    uv = place("ShaderNodeUVMap",-1220,340,"U distance along, V signed across")
    uv.uv_map = UV
    transform = place("ShaderNodeMapping",-980,335,"3.60 × 2.40 m surface repeat")
    transform.inputs["Scale"].default_value = (1/LENGTH,1/SPAN,1)
    transform.inputs["Location"].default_value = (0,.5,0)
    links.new(uv.outputs["UV"],transform.inputs["Vector"])

    def texture(key,x,y,coord):
        tex = place("ShaderNodeTexImage",x,y,key.replace("_"," "))
        tex.image = bpy.data.images.load(str(map_path(key)),check_existing=True)
        tex.image.colorspace_settings.name = "sRGB" if key.endswith("albedo") else "Non-Color"
        links.new(coord,tex.inputs["Vector"])
        return tex

    if mixed:
        raw = place("ShaderNodeSeparateXYZ",-955,-190)
        links.new(uv.outputs["UV"],raw.inputs[0])
        normalized = place("ShaderNodeSeparateXYZ",-760,-40)
        links.new(transform.outputs[0],normalized.inputs[0])
        across = place("ShaderNodeMath",-760,-265,"Path mask span in metres")
        across.operation = "DIVIDE"
        across.inputs[1].default_value = SPAN
        links.new(raw.outputs["Y"],across.inputs[0])
        across_centered = place("ShaderNodeMath",-560,-240)
        across_centered.operation = "ADD"
        across_centered.use_clamp = True
        across_centered.inputs[1].default_value = .5
        links.new(across.outputs[0],across_centered.inputs[0])
        coord = place("ShaderNodeCombineXYZ",-360,-130,"Metric edge coordinates")
        links.new(normalized.outputs["X"],coord.inputs["X"])
        links.new(across_centered.outputs[0],coord.inputs["Y"])
        mask = texture(PATH_BLEND,-155,-130,coord.outputs[0])

    bsdf = ns.get("Principled BSDF")
    bsdf.location = (475,300)
    ns.get("Material Output").location = (780,310)
    for i,(channel,socket) in enumerate((("albedo","Base Color"),("rough","Roughness"),("normal","Normal"))):
        y = 660+i*285
        sources = [texture(f"{style}_{channel}",-710 if j==0 else -390,y,transform.outputs[0]).outputs["Color"]
                   for j,style in enumerate(FINISHES if mixed else (finish,))]
        signal = sources[0]
        if mixed:
            mix = place("ShaderNodeMixRGB",135,y,channel)
            links.new(mask.outputs["Color"],mix.inputs[0])
            links.new(sources[0],mix.inputs[1])
            links.new(sources[1],mix.inputs[2])
            signal = mix.outputs[0]
        if channel=="normal":
            normal = place("ShaderNodeNormalMap",285,y)
            normal.uv_map = UV
            links.new(signal,normal.inputs["Color"])
            signal = normal.outputs["Normal"]
        links.new(signal,bsdf.inputs[socket])
    return mat


def native_project(finish):
    defs = [(key,"image",-670,230*i,
             {"image":f"%PROJECT_PATH%/{map_path(f'{finish}_{key}').name}","fix_ar":False})
            for i,key in enumerate(CHANNELS)]
    defs.extend((("Channels","decompose",-440,390,{}),("Native X","invert",-240,325,{}),
                 ("Native Z","invert",-240,560,{}),("Native normal","combine",-45,400,{}),
                 ("Depth","invert",-250,745,{}),
                 ("Material","material",185,220,{"size":10,"metallic":0.,"roughness":1.,
                                                "normal":1.,"depth_scale":RELIEF/LENGTH,"ao":1.})))
    nodes = [{"name":n,"type":k,"seed_int":0,"node_position":{"x":x,"y":y},"parameters":p}
             for n,k,x,y,p in defs]
    nodes[-1]["export_paths"] = {}
    edges = (("albedo",0,"Material",0),("rough",0,"Material",2),("height",0,"Depth",0),
             ("Depth",0,"Material",6),("normal",0,"Channels",0),("Channels",0,"Native X",0),
             ("Channels",2,"Native Z",0),("Native X",0,"Native normal",0),
             ("Channels",1,"Native normal",1),("Native Z",0,"Native normal",2),
             ("Native normal",0,"Material",4))
    graph = {"name":"Graph","type":"graph","label":f"Lowmark Ground | {finish.replace('_',' ')}",
             "seed_int":0,"node_position":{"x":0,"y":0},"parameters":{},"nodes":nodes,
             "connections":[{"from":a,"from_port":b,"to":c,"to_port":d} for a,b,c,d in edges]}
    (ROOT/f"{STEM}_{finish}.ptex").write_text(json.dumps(graph,indent=2)+"\n",encoding="utf8")


def mesh_with_uv(name,points,faces,uv,mat):
    obj = surface_mesh(name,points,faces)
    obj.data.materials.append(mat)
    obj.data.polygons.foreach_set("use_smooth",np.ones(len(faces),bool))
    layer = obj.data.uv_layers.new(name=UV)
    layer.data.foreach_set("uv",uv[faces.ravel()].astype(np.float32).ravel())
    return obj


def review_ground(name,centers,half_width,soil,mat,*,landing=False):
    # Fixed review fixtures. The centerline stations carry metre UVs through
    # the bend. A future generator can supply these coordinates on its mesh.
    tangents = np.gradient(centers,axis=0)
    tangents /= np.linalg.norm(tangents,axis=-1)[:,None]
    cross = np.column_stack((-tangents[:,1],tangents[:,0]))
    stations = np.r_[0,np.cumsum(np.linalg.norm(np.diff(centers,axis=0),axis=1))]
    sides = np.linspace(-half_width,half_width,math.ceil(2*half_width/.065)+1)
    u,v = np.meshgrid(stations,sides)
    xy = centers[None,:,:]+v[:,:,None]*cross[None,:,:]

    def bed(u,v):
        path,_ = soil.shoulder(u,v)
        undulation = .025*np.sin(.66*u+.50*v)+.016*np.sin(1.53*u-.97*v)
        bank = .070*(1-np.exp(-(.54*v)**2))
        height = -.031+undulation+bank-.020*path
        if landing:
            along = np.interp(u,stations,centers[:,1])
            approach = (1-ramp(.30,1.45,np.abs(along+.42)))*(1-ramp(.47,1.16,np.abs(v)))
            height += np.maximum(0.,-.004-height)*approach
        return height

    xyz = np.column_stack((xy.reshape(-1,2),bed(u,v).ravel()))
    uv = np.column_stack((u.ravel(),v.ravel()))
    faces = grid_faces(len(stations),len(sides))
    ground = mesh_with_uv(name,xyz,faces,uv,mat)
    center = len(sides)//2*len(stations)
    center_vertices = xyz[center:center+len(stations),:2]
    uv_distance = np.diff(uv[center:center+len(stations),0])
    world_distance = np.linalg.norm(np.diff(center_vertices,axis=0),axis=1)
    np.testing.assert_allclose(uv_distance,world_distance,atol=1e-10)
    if min(face.normal.z for face in ground.data.polygons)<.4:
        raise RuntimeError(f"Folded surface or inverted tangent frame in {name}")
    print(f"{name} | {stations[-1]:.2f} m along X in UV | {2*half_width:.2f} m across Y in UV",flush=True)
    return ground,(centers,cross,stations,half_width,bed)


def sprigs(fixture,soil,seed,density):
    centers,cross,stations,width,bed = fixture
    rng = np.random.default_rng(seed)
    n = math.ceil(2*width*stations[-1]*density)
    u = rng.uniform(.07,stations[-1]-.07,n)
    v = rng.uniform(-width+.04,width-.04,n)
    path,verge = soil.shoulder(u,v)
    fertile = profile(u/8.,v/6.,10,9,seed+10,periodic=False)
    grass = ramp(.28,.67,fertile)*ramp(.77,1.52,np.abs(v))
    chance = (.70*grass+.48*verge)*(1-path)**2
    # Rare little plants within the eroding shoulder. The center of the
    # tread stays open and its minor growth remains part of the baked soil.
    use = rng.random(n)<chance
    u,v = u[use],v[use]
    sampled_centers = np.column_stack([np.interp(u,stations,c) for c in centers.T])
    sampled_cross = np.column_stack([np.interp(u,stations,c) for c in cross.T])
    xy = sampled_centers+v[:,None]*sampled_cross
    z = bed(u,v)-.006
    points,faces,ids = [],[],[]
    for (x,y),base,distance in zip(xy,z,np.abs(v)):
        size = rng.uniform(.055,.225)*(.58+.42*ramp(.76,1.56,distance))
        for _ in range(int(rng.integers(4,9))):
            angle = rng.uniform(0,math.tau)
            dx,dy = math.cos(angle),math.sin(angle)
            x0,y0 = x+rng.uniform(-.029,.029),y+rng.uniform(-.029,.029)
            length = size*rng.uniform(.62,1.30)
            bend = length*rng.uniform(.28,.73)
            w = rng.uniform(.003,.0095)
            start = len(points)
            for t in (0.,.53,1.):
                px,py = x0+dx*bend*t*t,y0+dy*bend*t*t
                pz = base+length*(t-.17*t*t)
                spread = w*(1.-.94*t)
                points.extend(((px-dy*spread,py+dx*spread,pz),(px+dy*spread,py-dx*spread,pz)))
            faces.extend(((start,start+1,start+3,start+2),(start+2,start+3,start+5,start+4)))
            tone = int(rng.integers(4))
            ids.extend((tone,tone))
    obj = surface_mesh("Lowmark yard review | loose verge grass",points,np.asarray(faces))
    colors = ((.101,.122,.040),(.076,.103,.033),(.152,.156,.062),(.185,.159,.064))
    for i,color in enumerate(colors):
        name = f"Review verge grass {i+1}"
        mat = bpy.data.materials.get(name) or plain(name,color,.87)
        obj.data.materials.append(mat)
    obj.data.polygons.foreach_set("material_index",np.asarray(ids,dtype=np.int32))
    print(f"{fixture[2][-1]:.2f} m fixture | {len(u)} attached verge clumps",flush=True)
    return obj


def remove(obj):
    mesh = obj.data
    bpy.data.objects.remove(obj,do_unlink=True)
    bpy.data.meshes.remove(mesh)


def render(scene,name,width,height):
    scene.render.resolution_x,scene.render.resolution_y = width,height
    scene.render.resolution_percentage = 100
    settings = scene.render.image_settings
    settings.file_format,settings.color_mode,settings.color_depth = "PNG","RGB","8"
    scene.render.filepath = str(ROOT/f"{STEM}_{name}.png")
    bpy.ops.render.render(write_still=True)


def swatches(scene,materials,camera,draft):
    x,y = np.meshgrid(np.linspace(0,2.22,62),np.linspace(-.78,.78,44))
    uv = np.column_stack((x.ravel()+.40,y.ravel()+.20))
    points = np.column_stack((x.ravel(),y.ravel(),np.zeros(x.size)))
    surface = mesh_with_uv("Matched ground swatch",points,grid_faces(x.shape[1],x.shape[0]),
                           uv,materials[FINISHES[0]])
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = 2.62
    camera.location = (1.38,-1.78,2.22)
    point(camera,(1.11,0,0))
    for finish in FINISHES:
        surface.data.materials[0] = materials[finish]
        render(scene,finish.lower(),1000 if draft else 1536,660 if draft else 1010)
    remove(surface)


def route_studies(scene,soil,material,camera,draft):
    straight = np.column_stack((np.zeros(104),np.linspace(-2.8,3.2,104)))
    angle = np.linspace(-.75,.69,118)
    curved = np.column_stack((4.2*(1-np.cos(angle)),4.2*np.sin(angle)))
    size = (1000,680) if draft else (1536,1050)
    for i,(name,points) in enumerate((("straight",straight),("curved",curved))):
        ground,fixture = review_ground(name,points,2.,soil,material)
        grass = sprigs(fixture,soil,soil.seed+10+i,75)
        camera.data.type = "ORTHO"
        camera.data.ortho_scale = 6.60
        camera.location = (2.38,-4.18,5.08)
        point(camera,(.28,.09,0))
        render(scene,name,*size)
        remove(grass)
        remove(ground)


def farmhouse(scene,soil,material,camera,sun,draft):
    from build_lowmark_lime_plaster import build_farmhouse, make_materials, set_material
    from build_lowmark_planked_oak import orient_and_phase
    from build_lowmark_handcrafted_glass import fit_windows, DrawnGlass, optical_material

    plaster_objs = build_farmhouse(scene)
    lime = make_materials()["Maintained"]
    for obj in plaster_objs:
        set_material(obj,lime)
    with bpy.data.libraries.load(str(ROOT/"Lowmark_Planked_Oak_Joinery.blend")) as (_,loaded):
        loaded.materials = ["Lowmark Planked Oak | Wood Weathered"]
    oak = loaded.materials[0]
    with bpy.data.libraries.load(str(ROOT/"Lowmark_Forged_Iron_Hardware.blend")) as (_,loaded):
        loaded.materials = ["Lowmark Forged Iron | Weathered"]
    iron = loaded.materials[0]
    for obj in tuple(scene.objects):
        if obj.type=="MESH" and obj.name.startswith(("facade_doors","facade_shutters")):
            orient_and_phase(obj)
            set_material(obj,oak)
        elif obj.type=="MESH" and obj.name.startswith("facade_iron"):
            set_material(obj,iron)
    fit_windows(scene,DrawnGlass(70931,1.),optical_material("Lightly_Weathered"),draft)
    y = np.linspace(-18.,11.8,470)
    entrance = np.maximum(-y-.38,0)
    x = 3.79+.98*(1-np.cos(.28*entrance))
    ground,fixture = review_ground("Lowmark farmhouse walk and yard",np.column_stack((x,y)),8.7,
                                   soil,material,landing=True)
    sprigs(fixture,soil,soil.seed+68,48)
    sun.data.energy = 2.40
    sun.location = (-3.9,-4.9,10.)
    point(sun,(4.5,1.2,0))
    camera.data.type = "PERSP"
    camera.data.lens = 34
    camera.location = (5.85,-6.90,2.56)
    point(camera,(3.92,-.80,.62))
    render(scene,"farmhouse",1120 if draft else 1700,800 if draft else 1140)


def review(scene,soil,materials,draft):
    from build_lowmark_forged_iron import area
    scene.world = bpy.data.worlds.new("Lowmark earth review daylight")
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes["Background"]
    background.inputs["Color"].default_value = (.76,.80,.86,1)
    background.inputs["Strength"].default_value = .27
    bpy.ops.object.camera_add()
    camera = scene.camera = bpy.context.object
    key = area("Neutral raking comparison light",(.19,-.99,1.04),(1.11,0,0),60,1.20,.54)
    swatches(scene,materials,camera,draft)
    bpy.data.objects.remove(key,do_unlink=True)
    bpy.ops.object.light_add(type="SUN",location=(1.0,-3.2,5.))
    sun = bpy.context.object
    sun.data.energy,sun.data.angle = 2.15,.16
    point(sun,(0,0,0))
    route_studies(scene,soil,materials["Transition"],camera,draft)
    farmhouse(scene,soil,materials["Transition"],camera,sun,draft)


def main():
    cli = ArgumentParser()
    modes = cli.add_mutually_exclusive_group()
    modes.add_argument("--maps-only",action="store_true")
    modes.add_argument("--render-only",action="store_true")
    cli.add_argument("--draft",action="store_true")
    cli.add_argument("--optix",action="store_true")
    cli.add_argument("--verify-repeat",action="store_true")
    cli.add_argument("--seed",type=int,default=SEED)
    cli.add_argument("--compaction",type=float,default=.82)
    cli.add_argument("--gravel",type=float,default=.91)
    cli.add_argument("--moisture",type=float,default=.56)
    cli.add_argument("--traces",type=float,default=.60)
    cli.add_argument("--erosion",type=float,default=.77)
    cli.add_argument("--verge",type=float,default=.80)
    opts = cli.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    controls = (opts.compaction,opts.gravel,opts.moisture,opts.traces,opts.erosion,opts.verge)
    if opts.seed<0 or not all(0<=value<=1 for value in controls):
        cli.error("Use a nonnegative seed and surface controls from 0 to 1.")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    if opts.optix:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "OPTIX"
        prefs.refresh_devices()
        if not any(d.type=="OPTIX" for d in prefs.devices):
            cli.error("No Cycles OptiX device is available.")
        for device in prefs.devices:
            device.use = device.type=="OPTIX"
        scene.cycles.device = "GPU"
    else:
        scene.cycles.device = "CPU"
    scene.cycles.samples = 28 if opts.draft else 72
    scene.cycles.use_denoising = True
    scene.cycles.adaptive_threshold = .014
    scene.view_settings.view_transform = "AgX"
    soil = Soil(opts.seed,*controls)
    if not opts.render_only:
        size = (1080,720) if opts.draft else (2160,1440)
        data = maps(soil,size)
        verify(data,size)
        if opts.verify_repeat:
            regenerated = maps(Soil(opts.seed,*controls),size)
            for key,image in data.items():
                np.testing.assert_array_equal(image,regenerated[key],err_msg=key)
            del regenerated
            print(f"{len(data)} exports match independent regeneration pixel-for-pixel",flush=True)
        export(scene,data)
        del data
        reopen(size)
    materials = {finish:material(finish) for finish in (*FINISHES,"Transition")}
    if not opts.render_only:
        bpy.data.libraries.write(str(ROOT/f"{STEM}.blend"),set(materials.values()),
                                 path_remap="RELATIVE_ALL",fake_user=True,compress=True)
        for finish in FINISHES:
            native_project(finish)
    if not opts.maps_only:
        review(scene,soil,materials,opts.draft)


if __name__=="__main__":
    main()
