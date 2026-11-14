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
from mathutils.geometry import delaunay_2d_cdt
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
# Muted siltstones, ferruginous sandstones, and pale quartz-rich blocks.
MASONRY_ROCKS = np.array([
    [[.117,.119,.106], [.171,.170,.149], [.144,.150,.139]],
    [[.228,.177,.127], [.197,.159,.119], [.258,.207,.154]],
    [[.232,.215,.179], [.293,.257,.202], [.238,.230,.205]],
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


def outline_distance(points, outline):
    distance = np.full(points.shape[:-1],np.inf)
    for a,b in zip(outline,np.roll(outline,-1,axis=0)):
        edge = b-a
        to_point = points-a
        projection = np.clip((to_point@edge)/max(edge@edge,1e-10),0,1)
        distance = np.minimum(distance,np.linalg.norm(to_point-projection[...,None]*edge,axis=-1))
    return distance


def face_mesh(outline):
    # Constrain a uniform metric grid to the irregular perimeter. Independent
    # triangles sample fissures consistently even across the largest stones.
    spacing = .0037
    low = np.floor(outline.min(axis=0)/spacing).astype(int)
    high = np.ceil(outline.max(axis=0)/spacing).astype(int)
    x,y = np.meshgrid(np.arange(low[0],high[0]),np.arange(low[1],high[1]))
    grid = spacing*np.column_stack((x.ravel(),y.ravel()))
    grid = grid[outline_distance(grid,outline)>.0015]
    points = np.vstack((outline,grid))
    border = [list(range(len(outline)))]
    coords,_,faces,_,_,_ = delaunay_2d_cdt([Vector(p) for p in points],[],border,1,.00007,False)
    face = np.asarray(faces,dtype=np.int32)
    xy = np.asarray(coords,dtype=np.float32)
    used,lookup = np.unique(face,return_inverse=True)
    return xy[used],lookup.reshape(-1,3).astype(np.int32)


def layout():
    # Broken beds shared by adjacent courses. Each head joint is staggered,
    # and its two ends can lean or step without changing the neighboring fit.
    heads = (
        (.025,.162,.342,.484,.625,.857),
        (.096,.251,.411,.614,.788),
        (.025,.193,.321,.467,.706,.842),
        (.113,.285,.449,.676,.907),
        (.004,.162,.346,.531,.721,.861),
        (.099,.250,.428,.606,.794),
    )
    levels = (0.,.267,.605,.862,1.176,1.472,V)
    ridge_u = U*np.array([0,.091,.206,.298,.393,.500,.613,.724,.842,.926])
    rng = np.random.default_rng(SEED)
    ridge_v = rng.uniform(-.052,.052,(len(heads),len(ridge_u)))
    ridge_v[::2,1::3] *= .35
    ridge_max = np.roll(ridge_v,-1,axis=1)
    # A low shelf between adjacent rise points leaves broad bearing lengths.
    bed_u = np.r_[np.column_stack((ridge_u,ridge_u+.50*np.diff(np.r_[ridge_u,U]))).ravel(),U]
    ridges = np.column_stack((ridge_v,.86*ridge_v+.14*ridge_max)).reshape(len(heads),-1)
    beds = np.column_stack((ridges,ridges[:,0]))
    stages = np.array([0,.34,.71,1.])
    # Each pair shares only the two junctions needed for a taller stone.
    anchors = {(0,3): ((1,2), (.454,.618)), (3,2): ((4,3), (.498,.695))}
    pin_sites = {2,5,10,14,18,23,28,31}
    slab_pairs = {15,30}

    def bed(course,x):
        return levels[course]+np.interp(x,bed_u,beds[course%len(heads)],period=U)

    def bearing(course,left,right):
        knots = np.sort(np.concatenate((bed_u-U,bed_u,bed_u+U)))
        between = knots[(knots>left+1e-6)&(knots<right-1e-6)]
        x = np.r_[left,np.unique(between),right]
        return np.column_stack((x,bed(course,x)))

    joint_paths = []
    for offsets in heads:
        offsets = U*np.asarray(offsets)
        lean = rng.uniform(-.069,.069,len(offsets))
        jog = rng.uniform(-.025,.025,len(offsets))
        paths = offsets[:,None]+lean[:,None]*(stages-.5)
        paths[:,1:3] += jog[:,None]*np.array([.76,-.46])
        joint_paths.append(paths)
    for (row,col),((upper,upper_col),junctions) in anchors.items():
        x = U*np.asarray(junctions)
        joint_paths[row][col:col+2,-1] = x
        joint_paths[upper][upper_col:upper_col+2,0] = x

    cells = {}
    for course,paths in enumerate(joint_paths):
        loop = np.concatenate((paths,paths[:1]+U))
        for col,(left,right) in enumerate(zip(loop,loop[1:])):
            bottom = bearing(course,left[0],right[0])
            top = bearing(course+1,left[-1],right[-1])

            def side(x):
                lower,upper = bed(course,x),bed(course+1,x)
                return np.column_stack((x,lower+stages*(upper-lower)))[1:-1]

            cells[course,col] = bottom,side(right),top,side(left)

    stones = []
    covered = {upper for upper,_ in anchors.values()}
    for block,(key,(bottom,right,top,left)) in enumerate(cells.items()):
        if key in covered:
            continue
        if key in anchors:
            upper, _ = anchors[key]
            _,right_above,top_above,left_above = cells[upper]
            right = np.vstack((right,top[-1],right_above))
            left = np.vstack((left,top[0],left_above))
            top = top_above
        poly = np.vstack((bottom,right,top[::-1],left[::-1]))
        if block in pin_sites:
            # Only cut a short wedge from the bedding corner, leaving
            # the long bearing surface supported by the course below.
            nx = rng.uniform(.46,.92)*(-1 if block%2==0 else 1)
            ny = rng.uniform(.78,1.30)*(-1 if block%3 else 1)
            axis = np.array([nx,ny])
            support = poly@axis
            cut = support.max()-np.ptp(support)*rng.uniform(.24,.32)
            stones.extend(((clipped(poly,axis,cut),"fieldstone"),
                           (clipped(poly,-axis,-cut),"pinning stone")))
        elif block in slab_pairs:
            axis = np.array([rng.uniform(-.35,.35),1.])
            cut = float(np.mean(poly@axis))
            stones.extend(((clipped(poly,axis,cut),"fieldstone"),
                           (clipped(poly,-axis,-cut),"fieldstone")))
        else:
            stones.append((poly,"fieldstone"))
    return stones


def stone_mesh(poly, role, ident):
    rng = np.random.default_rng(SEED+1009*(ident+1))
    mineral_rng = np.random.default_rng(SEED+82+17*ident)
    kind = int(mineral_rng.integers(len(MASONRY_ROCKS)))
    # Choose a few real corner losses. A half-plane yields a strike face
    # instead of a rounded radius reduction between samples.
    center = (poly.max(axis=0)+poly.min(axis=0))*.5
    if role=="pinning stone":
        center = poly.mean(axis=0)
    for _ in range(2):
        angle = rng.uniform(0,2*np.pi)
        axis = np.array((np.cos(angle),np.sin(angle)))
        values = poly@axis
        loss = rng.uniform(.007,.030) if role=="fieldstone" else rng.uniform(.003,.010)
        poly = clipped(poly,axis,values.max()-loss)

    angles = np.linspace(0,2*np.pi,224,endpoint=False)
    directions = np.column_stack((np.cos(angles),np.sin(angles)))
    start = poly-center
    edges = np.roll(start,-1,axis=0)-start
    # Use finite ray/edge intersections. The shared beds can jog inward.
    across = directions[:,0,None]*edges[None,:,1]-directions[:,1,None]*edges[None,:,0]
    numerator = start[:,0]*edges[:,1]-start[:,1]*edges[:,0]
    with np.errstate(divide="ignore",invalid="ignore"):
        ray = numerator/across
        edge = (start[None,:,0]*directions[:,1,None]-start[None,:,1]*directions[:,0,None])/across
    hits = (ray>0)&(edge>=-1e-9)&(edge<=1+1e-9)&np.isfinite(ray)
    radius = np.min(np.where(hits,ray,np.inf),axis=1)
    if not np.isfinite(radius).all():
        raise RuntimeError(f"Stone {ident} has an invalid footprint")
    profile = field(directions[:,0]*3.2,directions[:,1]*3.2,ident+43)
    radius = np.maximum(.0025,radius*.985-.0032-.0035*profile)
    outline = directions*radius[:,None]
    local,faces = face_mesh(outline)
    x,y = local.T
    base = rng.uniform(.048,.069) if role=="fieldstone" else rng.uniform(.036,.050)
    span = np.maximum(np.abs(outline).max(axis=0),.04)
    face_x,face_y = x/span[0],y/span[1]
    facet = base + rng.uniform(-.011,.011)*face_x + rng.uniform(-.013,.013)*face_y
    for _ in range(4):
        direction = rng.uniform(0,2*np.pi)
        axis = np.cos(direction)*face_x + np.sin(direction)*face_y
        limit = base + rng.uniform(.007,.027) - rng.uniform(.012,.032)*axis
        facet = np.minimum(facet,limit)
    fracture_axis = rng.uniform(-1.15,1.15)
    along = x*np.cos(fracture_axis)+y*np.sin(fracture_axis)
    cross = -x*np.sin(fracture_axis)+y*np.cos(fracture_axis)
    run = field(along*(8,12,13)[kind],cross*(40,23,21)[kind],ident+11)
    strata = smooth(.42,.57,run)-.60*smooth(.67,.82,run)
    cleft = np.zeros_like(x)
    if rng.random()<.61:
        line = cross-rng.uniform(-.060,.063)-.13*along
        crooked = (field(along*26,np.zeros_like(along),ident+5)-.5)*.014
        cut_width = rng.uniform(.0045,.009)
        active = 1-smooth(.039,.15,np.abs(along-rng.uniform(-.06,.06)))
        cleft = (1-smooth(.18,1,np.abs(line+crooked)/cut_width))*active
        facet -= rng.uniform(.005,.015)*cleft
    pitted = smooth(.62,.88,field(x*93,y*91,ident+19))
    broken = field(x*33,y*34,ident+23)
    bedding = rng.uniform(.0017,.0082)*(1.12,.69,.45)[kind]
    facet += bedding*(strata-.35)+rng.uniform(.001,.006)*(broken-.50)-.0035*pitted
    # Traced shoulders alternate between steep split faces and localized
    # spalls. Their widths are in metres rather than a share of stone size.
    shoulder_width = rng.uniform(.007,.016)+.016*field(x*18,y*18,ident+43)
    distance = outline_distance(local,outline)
    shoulder = np.interp(distance/shoulder_width,(0,.23,.77,1), (0,.16,.85,1))
    back = .012+.003*field(x*34,y*32,ident+7)
    z = facet*shoulder + back*(1-shoulder)
    z = np.clip(z,.010,.094)
    swatches = MASONRY_ROCKS[kind]
    hue = swatches[mineral_rng.integers(len(swatches))]*mineral_rng.uniform(.89,1.11)
    mineral = field(x*16.5,y*18.1,ident+67)
    vein = (smooth(.52,.58,run)-smooth(.62,.70,run))*smooth(.40,.73,mineral)
    hue_field = hue*(.84+.25*mineral+.30*vein-.15*pitted-.055*cleft)[:,None]
    # Oxidation gathers in coherent patches and is strongest in sandstone.
    stain = smooth(.54,.81,field(x*8.8,y*12.7,ident+69))*(.25+.75*broken)
    stain *= (.21,.51,.27)[kind]
    oxidized = np.array([.207,.154,.105])
    hue_field += stain[:,None]*(oxidized-hue_field)
    rough = np.clip((.69,.75,.72)[kind] + .098*pitted + .105*broken - .095*vein + .06*stain,.59,.96)
    points = np.column_stack((center+local,z))
    sample = np.column_stack((local+np.array([ident*2.31,ident*.51]),z))
    return points,faces,hue_field,rough,sample,center+outline



def mortar_signals(u,v):
    su,sv = 2*np.pi*u/U,2*np.pi*v/V
    broad=field(u/U*43,v/V*33,86,(43,33))
    sand=field(u/U*135,v/V*97,92,(135,97))
    wiped=field(u/U*31,v/V*89,162,(31,89))
    bumps = .85*(broad-.5)+.40*(sand-.5)+.18*(wiped-.5)
    daub = .57*broad+.26*wiped+.17*sand
    hue = np.array([.144,.132,.113])*(.85+.29*daub)[...,None]
    height = .016 + .0032*bumps
    rough = np.clip(.86+.08*bumps,.71,.98)
    coord = np.stack(((U/(2*np.pi))*np.sin(su),(U/(2*np.pi))*np.cos(su),
                      (V/(2*np.pi))*np.sin(sv)),axis=-1)
    return height,hue,rough,coord


def wall():
    vertices, faces, pigment, rough, coords, sample_w, mortar = [], [], [], [], [], [], []
    layout_records = []
    offset = 0

    def append(points, triangles, color, r, sample, weight):
        nonlocal offset
        count = len(points)
        vertices.append(points.astype(np.float32))
        pigment.append(np.column_stack((color,np.ones(count))).astype(np.float32))
        rough.append(r.ravel().astype(np.float32))
        coords.append(sample.astype(np.float32))
        w = (V/(2*np.pi))*np.cos(points[:,1]*(2*np.pi/V)) if weight else np.zeros(count)
        sample_w.append(w.astype(np.float32))
        mortar.append(np.full(count,weight,np.float32))
        faces.append(triangles.astype(np.int32)+offset)
        offset += count

    # Bed samples repeat at an exact integer grid interval. Mortar rises
    # selectively where a trowel has packed it against a stone's rim.
    spacing = U/360
    x,y = np.meshgrid(np.arange(-15,376)*spacing,np.arange(-15,286)*spacing)
    z,mortar_hue,mortar_rough,mortar_coord = mortar_signals(x,y)
    shoulder_field = np.zeros_like(z)
    for ident,(poly,role) in enumerate(layout()):
        pos,triangles,hue,r,coord,outline = stone_mesh(poly,role,ident)
        center = poly.mean(axis=0)
        layout_records.append((ident,role,*center,float(np.max(pos[:,2])),outline[::2]))
        for ix in (-1,0,1):
            for iy in (-1,0,1):
                displacement = (ix*U,iy*V,0)
                current = pos+displacement
                if (current[:,0].max() < -.052 or current[:,0].min() > U+.052
                    or current[:,1].max() < -.052 or current[:,1].min() > V+.052):
                    continue
                append(current,triangles,hue,r,coord,0)
                rim = outline+(ix*U,iy*V)
                mask = ((x>rim[:,0].min()-.039)&(x<rim[:,0].max()+.039)
                        &(y>rim[:,1].min()-.039)&(y<rim[:,1].max()+.039))
                if mask.any():
                    patch=np.column_stack((x[mask],y[mask]))
                    distance = outline_distance(patch,rim)
                    lift=(1-smooth(.003,.020,distance))*(.001+.005*field(
                          (x[mask]-ix*U)*17,(y[mask]-iy*V)*21,ident+87))
                    shoulder_field[mask]=np.maximum(shoulder_field[mask],lift)
    rows,cols = x.shape
    grid = np.arange(rows*cols).reshape(rows,cols)
    a,b,c,d = grid[:-1,:-1],grid[:-1,1:],grid[1:,1:],grid[1:,:-1]
    triangles = np.stack((a,b,c,a,c,d),axis=-1).reshape(-1,3)
    append(np.column_stack((x.ravel(),y.ravel(),(z+shoulder_field).ravel())),triangles,
           mortar_hue.reshape(-1,3),mortar_rough.ravel(),mortar_coord.reshape(-1,3),1)
    points, tris, rgb, matte, uvw, w, masks = map(np.concatenate,(vertices,faces,pigment,rough,coords,sample_w,mortar))
    mesh=bpy.data.meshes.new("Shaped stones with continuous mortar bedding")
    mesh.vertices.add(len(points))
    mesh.vertices.foreach_set("co",points.ravel())
    mesh.loops.add(tris.size)
    mesh.loops.foreach_set("vertex_index",tris.ravel())
    mesh.polygons.add(len(tris))
    mesh.polygons.foreach_set("loop_start",np.arange(0,tris.size,3,dtype=np.int32))
    mesh.polygons.foreach_set("use_smooth",np.ones(len(tris),bool))
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


def display_sphere(scene):
    # Two repeats around the equator keep the front sample near wall scale.
    radius=U/np.pi
    bpy.ops.mesh.primitive_uv_sphere_add(segments=640,ring_count=384,radius=radius)
    sphere=bpy.context.object
    mesh=sphere.data
    base=np.empty(len(mesh.vertices)*3,np.float32)
    mesh.vertices.foreach_get("co",base)
    base=base.reshape(-1,3)
    radial=base/radius
    loop_vertex=np.empty(len(mesh.loops),np.int32)
    mesh.loops.foreach_get("vertex_index",loop_vertex)
    uv=mesh.uv_layers.active
    uv.name="UV0_Metric"
    mapped=np.empty((len(mesh.loops),2),np.float32)
    uv.data.foreach_get("uv",mapped.ravel())
    mapped *= (2,U/V)
    mapped += (.13,.19)
    uv.data.foreach_set("uv",mapped.ravel())
    coord=np.empty((len(mesh.vertices),2),np.float32)
    coord[loop_vertex]=mapped
    image=bpy.data.images.load(str(path("height")))
    image.colorspace_settings.name="Non-Color"
    height=pixels(image)[:,:,0]
    h,w=height.shape
    sample=coord*(w,h)-.5
    cells=np.floor(sample).astype(int)
    u,v=cells.T
    fu,fv=(sample-cells).T
    top=(1-fu)*height[v%h,u%w]+fu*height[v%h,(u+1)%w]
    bottom=(1-fu)*height[(v+1)%h,u%w]+fu*height[(v+1)%h,(u+1)%w]
    depth=(1-fv)*top+fv*bottom
    # Fade geometry near the poles where longitude converges. Use radial
    # shading normals so the tangent bake supplies slopes only once.
    fade=1-smooth(.90,.999,np.abs(radial[:,2]))
    displaced=(base+radial*((depth-.36)*RELIEF*fade)[:,None]).astype(np.float32)
    mesh.vertices.foreach_set("co",displaced.ravel())
    mesh.polygons.foreach_set("use_smooth",np.ones(len(mesh.polygons),bool))
    mesh.update()
    mesh.normals_split_custom_set_from_vertices(radial.tolist())
    attach_bake(sphere)

    world=scene.world=bpy.data.worlds.new("Neutral sphere studio")
    world.use_nodes=True
    background=world.node_tree.nodes["Background"]
    background.inputs[0].default_value=(.56,.56,.56,1)
    background.inputs[1].default_value=.47
    bpy.ops.object.camera_add(location=(.22,-4.7,.33))
    scene.camera=bpy.context.object
    scene.camera.rotation_euler=(-scene.camera.location).to_track_quat("-Z","Y").to_euler()
    scene.camera.data.lens=91
    bpy.ops.object.light_add(type="AREA",location=(-2.8,-3.4,3.4))
    key=bpy.context.object
    key.rotation_euler=(-key.location).to_track_quat("-Z","Y").to_euler()
    key.data.energy=760
    key.data.shape="DISK"
    key.data.size=2.7
    scene.cycles.samples=48
    scene.cycles.use_denoising=True
    scene.render.resolution_x=scene.render.resolution_y=1400
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.image_settings.color_mode="RGB"
    scene.render.filepath=str(path("sphere"))
    bpy.ops.render.render(write_still=True)


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
        aim(camera,(U/2,V/2,3.6),(U/2,V/2,.03))
        camera.data.ortho_scale=U
        scene.render.resolution_y=900
        capture("clay_wall")
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
    aim(camera,(U/2,V/2,3.6),(U/2,V/2,.03))
    camera.data.ortho_scale=U
    scene.render.resolution_y=900
    capture("straight_wall")
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
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument("--draft",action="store_true",help="Render neutral geometry only")
    mode.add_argument("--sphere-only",action="store_true",help="Render a display sphere from existing maps")
    parser.add_argument("--verify-repeat",action="store_true")
    parser.add_argument("--size",type=int,default=2048)
    args=parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene
    scene.render.engine="CYCLES"
    scene.cycles.samples=1
    scene.cycles.device="CPU"
    scene.view_settings.view_transform="AgX"
    if args.sphere_only:
        display_sphere(scene)
        return
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
