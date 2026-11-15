"""Model and bake low vegetation over the accepted Lowmark Packed Earth fields."""

from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
import math
import sys

import bpy
import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from build_lowmark_packed_earth import LENGTH, RELIEF, SEED, SPAN, UV, Soil, normals
from build_lowmark_structural_timber import grid_faces, pixels, plain, point, surface_mesh

STEM = "Lowmark_Sparse_Vegetation_Ground"
GROWTH_SEED = 40581
SIZE = (2160, 1440)
PERIOD = np.array((LENGTH, SPAN))


def path(name, suffix):
    return ROOT / f"{STEM}_{name}.{suffix}"


def sample(field, x, y):
    """Bilinear evaluation at metre coordinates, including across the repeat."""
    h, w = field.shape[:2]
    px, py = x * w / LENGTH - .5, y * h / SPAN - .5
    ix, iy = np.floor(px).astype(int), np.floor(py).astype(int)
    fx, fy = px - ix, py - iy
    if field.ndim == 3:
        fx, fy = fx[..., None], fy[..., None]
    a = field[iy % h, ix % w] * (1 - fx) + field[iy % h, (ix + 1) % w] * fx
    b = field[(iy + 1) % h, ix % w] * (1 - fx) + field[(iy + 1) % h, (ix + 1) % w] * fx
    return a * (1 - fy) + b * fy


class Growth:
    def __init__(self, ground, rocks, seed):
        self.ground, self.rocks = ground, rocks
        self.rng = np.random.default_rng(seed)
        self.surfaces = []
        self.counts = dict(grass=0, weeds=0, roots=0, flowers=0)

    def ribbon(self, start, angle, length, width, lift, sweep, base, tip, rough, *,
               leaf=False, suspended=0., phase=0., dry=False):
        """Tapered, folded blade, elliptical leaf, or narrow stem in metres."""
        t = np.linspace(0., 1., 12 if leaf else 8)
        direction = np.array((math.cos(angle), math.sin(angle)))
        side = np.array((-direction[1], direction[0]))
        drift = sweep * t**1.4 + .10 * abs(sweep) * np.sin(8*t + phase)*t
        xy = start + length * t[:, None] * direction + drift[:, None] * side
        floor = sample(self.ground, *xy.T)
        root_height = sample(self.ground, *start)
        z = np.maximum(floor + .0007, root_height + suspended
                       + lift * (1.85*t - .99*t*t) + .12*lift*np.sin(math.pi*t))
        if leaf:
            taper = .10 + .90 * np.maximum(np.sin(math.pi*t**1.45), 0)**.69
            taper[0], taper[-1] = .14, .015
            taper *= 1 + .14*np.sin(33*t+phase) + .12*np.sin(15*t-phase)
        else:
            taper = (1-t)**.60 * (.49+.51*np.sin(.27+2.45*t))
            taper[-1] = .02
        cross = np.array((-1., 0., 1.))
        verts_xy = xy[:, None, :] + (width*taper[:, None]*cross/2)[..., None]*side
        fold = width * taper * (.17 if leaf else .23)
        verts_z = z[:, None] - fold[:, None]*np.abs(cross)
        verts_z += (width*taper*np.sin(phase+3*t)*.19)[:, None]*cross
        vertices = np.concatenate((verts_xy, verts_z[..., None]), axis=-1).reshape(-1, 3)
        colors = np.array(base)[None, :]*(1-t[:, None]) + np.array(tip)[None, :]*t[:, None]
        colors = colors[:, None, :]*np.array((.78, 1.17 if leaf else 1.08, .91))[None, :, None]
        colors *= (1+.11*np.sin(36*t+phase)+.045*np.sin(91*t+phase))[:, None, None]
        if dry:
            colors *= np.array((1.07, .98, .85))
        faces = grid_faces(3, len(t))
        self.surfaces.append((vertices, colors.reshape(-1, 3), faces, rough))

    def allowed(self, xy, limit=.24):
        return sample(self.rocks, *xy) < limit

    def grass(self, xy, direction, condition):
        self.counts["grass"] += 1
        rng = self.rng
        size = rng.uniform(.67, 1.45)
        for _ in range(rng.integers(7, 15)):
            dry = rng.random() < condition
            shade = rng.uniform(.63, 1.37)
            rgb = np.array((.094, .071, .033) if dry else (.032, .050, .017))*shade
            tip = rgb*np.array((1.52, 1.34, 1.12))
            self.ribbon(xy+rng.normal(0,.009,2), direction+rng.normal(0,1.32),
                        rng.uniform(.019, .109)*size, rng.uniform(.0021, .0052)*size,
                        rng.uniform(.003, .024)*size, rng.uniform(-.044, .044)*size,
                        rgb*.70, tip, .80 if dry else .63,
                        phase=rng.uniform(0, math.tau), dry=dry)

    def rosette(self, xy, kind):
        self.counts["weeds"] += 1
        rng = self.rng
        broad = kind == 0
        scale = rng.uniform(.61, 1.20)
        count = rng.integers(4, 10)
        heading = rng.uniform(0, math.tau)
        for leaf in range(count):
            angle = heading + leaf * 2.39996 + rng.uniform(-.46, .46)
            rgb = np.array((.041, .060, .018) if broad else (.027, .052, .021))
            rgb *= rng.uniform(.76, 1.28)
            self.ribbon(xy, angle, rng.uniform(.027, .102)*scale,
                        rng.uniform(.012, .025)*scale*(1. if broad else .59),
                        rng.uniform(.007, .028)*scale, rng.uniform(-.019, .019),
                        rgb*.83, rgb*1.17, rng.uniform(.52,.69), leaf=True,
                        phase=rng.uniform(0, math.tau))

    def runner(self, xy, angle):
        rng = self.rng
        length = rng.uniform(.041,.104)
        direction = np.array((math.cos(angle),math.sin(angle)))
        rgb = np.array((.036,.056,.019))*rng.uniform(.74,1.2)
        self.ribbon(xy, angle, length, .0021, .0025, 0., rgb*.77, rgb, .74)
        for pair in range(rng.integers(2,5)):
            for side in (-1,1):
                x = xy+length*(.18+.17*pair)*direction
                self.ribbon(x, angle+side*rng.uniform(.65,1.37), rng.uniform(.009,.027),
                            rng.uniform(.004,.011), rng.uniform(.003,.009), .0,
                            rgb*.85, rgb*1.13, .67, leaf=True)
        self.counts["weeds"] += 1

    def root(self, xy):
        self.counts["roots"] += 1
        rng = self.rng
        angle = rng.uniform(0, math.tau)
        vector = np.array((math.cos(angle), math.sin(angle)))
        length = rng.uniform(.042,.129)
        rgb = np.array((.105,.075,.041))*rng.uniform(.77,1.20)
        self.ribbon(xy, angle, length, rng.uniform(.0019,.0044), .0013,
                    rng.uniform(-.028,.028), rgb*.77, rgb, .87, phase=4.)
        for fraction in (.28,.53):
            x = xy + length*fraction*vector
            self.ribbon(x, angle+rng.choice((-1,1))*rng.uniform(.46,1.15),
                        rng.uniform(.018,.040), .0017, .001, rng.uniform(-.013,.013),
                        rgb, rgb*.8, .88, phase=1.)

    def flower(self, xy, index):
        self.counts["flowers"] += 1
        rng = self.rng
        angle = rng.uniform(0, math.tau)
        head = xy + .031*np.array((math.cos(angle), math.sin(angle)))
        self.ribbon(xy, angle, .032, .00165, .019, 0.,
                    (.047,.064,.024), (.067,.084,.031), .70)
        self.ribbon(xy, angle+.55, .022, .007, .012, .003,
                    (.043,.066,.023), (.051,.074,.028), .67, leaf=True)
        cream = np.array((.54,.473,.332) if index != 2 else (.47,.310,.108))
        for i in range(5):
            self.ribbon(head, i*math.tau/5+angle, rng.uniform(.0041,.0063),
                        .0049, .0017, 0., cream*.65, cream, .73, leaf=True, suspended=.019)
        self.ribbon(head+(.001,0), angle, .0033, .0036, .001, 0.,
                    (.29,.186,.041), (.35,.23,.053), .78, leaf=True, suspended=.021)

    def populate(self, cluster):
        rng = self.rng
        seeds = []
        while len(seeds) < 24:
            p = rng.random(2)*PERIOD
            if all(np.linalg.norm((p-other+PERIOD/2)%PERIOD-PERIOD/2) > .30 for other in seeds):
                seeds.append(p)
        for patch, center in enumerate(seeds):
            direction = rng.uniform(0, math.tau)
            axis = np.array((math.cos(direction), math.sin(direction)))
            side = np.array((-axis[1], axis[0]))
            count = rng.integers(6, 23) if patch%3==0 else rng.integers(20, 45)
            span = rng.uniform(.10, .27)
            condition = rng.uniform(.06, .29)
            for _ in range(count):
                u, v = rng.normal(size=2)
                tight = center + span*u*axis + span*.32*(v+.36*u*u)*side
                diffuse = center + .32*u*axis + .25*v*side
                p = (tight*cluster + diffuse*(1-cluster)) % PERIOD
                if self.allowed(p):
                    self.grass(p, direction + rng.normal(0, .65), condition)
            if patch % 8 != 5 and self.allowed(center):
                self.rosette(center, patch % 3)
            if patch % 3 != 1:
                for i in range(rng.integers(2,5)):
                    p = center + rng.normal(0,.10,2)
                    if self.allowed(p):
                        self.runner(p,direction+i*2.4)
            if patch % 5 == 3 and self.allowed(center):
                self.flower(center + .043*side, (patch//5)%3)
            if patch % 2 == 0 and self.allowed(center):
                self.root(center + .042*axis)
        for _ in range(20):
            p = rng.random(2)*PERIOD
            if self.allowed(p, .16):
                self.grass(p, rng.uniform(0, math.tau), .40)


def bake(growth, size):
    """Top-down, periodic 4×4 subpixel rasterization of the modeled surfaces."""
    w, h = size
    n = 4
    density = np.array((n*w, n*h))/PERIOD
    zbuffer = np.full((n*h, n*w), -np.inf, np.float32)
    # 16-bit buffers are sufficient for the supersamples. Resolve in float32.
    rgb = np.zeros((n*h, n*w, 3), np.float16)
    nxy = np.zeros((n*h, n*w, 2), np.float16)
    rough = np.zeros((n*h, n*w), np.float16)
    for verts, colors, faces, finish in growth.surfaces:
        for a, b, c, d in faces:
            for tri in ((a,b,c), (a,c,d)):
                xyz = verts[list(tri)]
                uv = xyz[:, :2]*density-.5
                low, high = np.ceil(uv.min(0)).astype(int), np.floor(uv.max(0)).astype(int)
                if (low > high).any():
                    continue
                dx, dy = uv[1]-uv[0], uv[2]-uv[0]
                det = dx[0]*dy[1]-dx[1]*dy[0]
                if abs(det) < 1e-9:
                    continue
                xx = np.arange(low[0], high[0]+1)[None, :]
                yy = np.arange(low[1], high[1]+1)[:, None]
                tx, ty = xx-uv[0,0], yy-uv[0,1]
                u, v = (tx*dy[1]-ty*dy[0])/det, (ty*dx[0]-tx*dx[1])/det
                z = xyz[0,2]+u*(xyz[1,2]-xyz[0,2])+v*(xyz[2,2]-xyz[0,2])
                iy, ix = yy % (n*h), xx % (n*w)
                mask = (u>=0) & (v>=0) & (u+v<=1) & (z>zbuffer[iy,ix])
                if not mask.any():
                    continue
                iy, ix = np.broadcast_arrays(iy, ix)
                selected = iy[mask], ix[mask]
                zbuffer[selected] = z[mask]
                palette = colors[list(tri)]
                rgb[selected] = palette[0]+u[mask,None]*(palette[1]-palette[0])+v[mask,None]*(palette[2]-palette[0])
                normal = np.cross(xyz[1]-xyz[0], xyz[2]-xyz[0])
                normal *= (1 if normal[2]>=0 else -1)/np.linalg.norm(normal)
                nxy[selected] = normal[:2]*.81
                rough[selected] = finish
    hit = np.isfinite(zbuffer)

    def resolve(data):
        return data.reshape(h,n,w,n,*data.shape[2:]).sum(axis=(1,3), dtype=np.float32)

    count = resolve(hit)
    zbuffer[~hit] = 0.
    floor = growth.ground
    z = resolve(zbuffer)/np.maximum(1,count)
    rel = np.where(count>0, np.maximum(.0,z-floor), 0.)
    albedo = resolve(rgb)/np.maximum(1,count)[...,None]
    normals_xy = resolve(nxy)/np.maximum(1,count)[...,None]
    surface = np.dstack((normals_xy, np.sqrt(1.-np.sum(normals_xy**2, axis=-1))))
    finish = resolve(rough)/np.maximum(1,count)
    # Extend straight-color PBR below the mask for texture filtering.
    # Height stays premultiplied so a covered sample attenuates exactly once.
    valid = count>0
    for _ in range(4):
        previous = valid.copy()
        for axis in (0, 1):
            for step in (-1, 1):
                take = ~valid & np.roll(previous, step, axis=axis)
                if take.any():
                    for field in (albedo, surface, finish):
                        field[take] = np.roll(field, step, axis=axis)[take]
                    valid[take] = True
    coverage = count/(n*n)
    return albedo, .5+.5*surface, coverage, finish, rel*coverage


def build(size, seed, cluster):
    soil = Soil(SEED, .82, .91, .56, .60, .77, 0.)
    height, color, rough, rock = soil.raster(size, False)
    growth = Growth(height, rock, seed)
    growth.populate(cluster)
    albedo, normal, alpha, finish, relief = bake(growth, size)
    fields = {
        "Soil_albedo": color, "Soil_normal": normals(height, size),
        "Soil_rough": rough, "Soil_height": .5+height/RELIEF,
        "Growth_albedo": albedo, "Growth_normal": normal,
        "Growth_data": np.dstack((alpha, finish, relief/RELIEF)),
    }
    return {key: value.astype(np.float32) for key,value in fields.items()}, height, growth


def verify(fields, height, growth, size, seeds, cluster):
    assert all(np.isfinite(value).all() for value in fields.values())
    data = fields["Growth_data"]
    mask, rough, raise_height = data.transpose(2,0,1)
    assert .025 < mask.mean() < .18
    assert not np.any(raise_height[mask==0]) and raise_height.max()*RELIEF <= .07
    for channel, plant in (("albedo", fields["Growth_albedo"]), ("normal", fields["Growth_normal"]),
                           ("rough", rough)):
        base = fields[f"Soil_{channel}"]
        for control in (0., np.zeros_like(mask)):
            amount = mask*control
            if base.ndim==3:
                amount = np.broadcast_to(amount, mask.shape)[...,None]
            assert np.array_equal(base + (plant-base)*amount, base)
    np.testing.assert_array_equal(height + raise_height*RELIEF*0., height)
    paint = np.linspace(0,1,9,dtype=np.float32)
    weight = paint[:,None,None]*mask
    assert np.all(np.diff(weight,axis=0)>=0)
    np.testing.assert_array_equal(weight[-1],mask)
    for field in fields.values():
        u = np.array((-.024,.003,LENGTH-.006))
        v = np.array((.003,SPAN-.009,-.013))
        np.testing.assert_allclose(sample(field,u,v), sample(field,u+LENGTH,v+SPAN), atol=1e-6, rtol=0)
    digest = sha256()
    for array in fields.values():
        digest.update(array.tobytes())
    if seeds:
        duplicate = Growth(height, growth.rocks, seeds[0])
        duplicate.populate(cluster)
        again = bake(duplicate, size)
        for original, rebuilt in zip((fields["Growth_albedo"], fields["Growth_normal"], mask, rough,
                                      raise_height*RELIEF), again):
            np.testing.assert_allclose(original, rebuilt, atol=4e-8, rtol=0)
        alternate = Growth(height, growth.rocks, seeds[0]+1)
        alternate.populate(cluster)
        assert not np.array_equal(duplicate.surfaces[0][0], alternate.surfaces[0][0])
    print(f"{size} | {growth.counts} | projected foliage {mask.mean():.2%} | "
          f"effective raised leaf top {raise_height.max()*RELIEF*1000:.1f} mm | {digest.hexdigest()}",
          flush=True)


def extension(key):
    return "png" if key.endswith("albedo") else "exr"


def export(scene, fields):
    settings = scene.render.image_settings
    settings.color_mode = "RGB"
    scene.view_settings.look = "None"
    for key, value in fields.items():
        h,w = value.shape[:2]
        rgba = np.ones((h,w,4), np.float32)
        rgba[:,:,:3] = value if value.ndim==3 else value[:,:,None]
        image = bpy.data.images.new(key,w,h,alpha=False,float_buffer=True)
        if extension(key)=="png":
            image.colorspace_settings.name = "Linear Rec.709"
            scene.view_settings.view_transform = "Standard"
            settings.file_format,settings.color_depth = "PNG","8"
        else:
            image.colorspace_settings.name = "Non-Color"
            settings.file_format,settings.color_depth = "OPEN_EXR","16"
            settings.exr_codec = "ZIP"
        image.pixels.foreach_set(rgba.ravel())
        image.save_render(str(path(key,extension(key))),scene=scene)
        bpy.data.images.remove(image)
        # Reopen saved data to catch color conversion and channel packing errors.
        reloaded = bpy.data.images.load(str(path(key,extension(key))))
        reloaded.colorspace_settings.name = "sRGB" if extension(key)=="png" else "Non-Color"
        decoded = pixels(reloaded)[:,:,:3]
        if extension(key)=="png":
            encoded = np.where(value<=.0031308,12.92*value,1.055*value**(1/2.4)-.055)
            assert np.max(np.abs(decoded-encoded)) <= 1.1/255
        else:
            target = value if value.ndim==3 else value[:,:,None]
            assert np.max(np.abs(decoded-target)) <= .00049
        bpy.data.images.remove(reloaded)
    scene.view_settings.view_transform = "AgX"


def material_group():
    graph = bpy.data.node_groups.new("Lowmark | Soil + Sparse Growth","ShaderNodeTree")
    ns, links = graph.nodes, graph.links

    def node(kind, at, label):
        n = ns.new(kind)
        n.location, n.label = at, label
        return n

    for name, default in (("Coverage",1.), ("Painted Mask",1.), ("Use cv_density",0.)):
        plug = graph.interface.new_socket(name=name,in_out="INPUT",socket_type="NodeSocketFloat")
        plug.min_value,plug.max_value,plug.default_value = 0.,1.,default
    graph.interface.new_socket(name="Surface",in_out="OUTPUT",socket_type="NodeSocketShader")
    graph.interface.new_socket(name="Height",in_out="OUTPUT",socket_type="NodeSocketFloat")
    graph.interface.new_socket(name="Growth Weight",in_out="OUTPUT",socket_type="NodeSocketFloat")
    controls = node("NodeGroupInput",(-1280,560),"Growth only")
    output = node("NodeGroupOutput",(810,300),"")
    uv = node("ShaderNodeUVMap",(-1280,40),"Metric coordinates")
    uv.uv_map = UV
    scale = node("ShaderNodeMapping",(-1080,40),"3.60 × 2.40 m repeat")
    scale.inputs["Scale"].default_value = (1/LENGTH,1/SPAN,1.)
    links.new(uv.outputs["UV"], scale.inputs["Vector"])
    attr = node("ShaderNodeAttribute",(-1280,330),"Shared Vegetation Scatter weight")
    attr.attribute_name = "cv_density"
    select = node("ShaderNodeMix",(-1040,440),"Enable painted POINT attribute when present")
    select.data_type = "FLOAT"
    links.new(controls.outputs["Use cv_density"],select.inputs[0])
    select.inputs[2].default_value = 1.
    links.new(attr.outputs["Fac"],select.inputs[3])

    def math_node(op, label, at, a, b, clamp=False):
        n = node("ShaderNodeMath",at,label)
        n.operation,n.use_clamp = op,clamp
        for i, src in enumerate((a,b)):
            if isinstance(src, (float,int)):
                n.inputs[i].default_value = src
            else:
                links.new(src,n.inputs[i])
        return n.outputs[0]

    cov = math_node("MULTIPLY","Coverage × paint",(-815,605),controls.outputs["Coverage"],
                    controls.outputs["Painted Mask"],True)
    cov = math_node("MULTIPLY","Include shared attribute",(-615,605),cov,select.outputs[0],True)

    def texture(key, at):
        tex = node("ShaderNodeTexImage",at,key.replace("_"," "))
        tex.image = bpy.data.images.load(str(path(key,extension(key))),check_existing=True)
        tex.image.colorspace_settings.name = "sRGB" if extension(key)=="png" else "Non-Color"
        links.new(scale.outputs[0],tex.inputs[0])
        return tex.outputs["Color"]

    data = node("ShaderNodeSeparateColor",(-570,365),"R coverage · G roughness · B height / .082 m")
    links.new(texture("Growth_data",(-815,350)),data.inputs[0])
    alpha = math_node("MULTIPLY","Visible coverage",(-275,590),cov,data.outputs[0])
    links.new(alpha,output.inputs["Growth Weight"])

    def mix(label, at, a, b):
        blend = node("ShaderNodeMixRGB",at,label)
        for src, slot in zip((alpha,a,b),blend.inputs):
            links.new(src,slot)
        return blend.outputs[0]

    color = mix("Linear albedo blend",(-40,280),texture("Soil_albedo",(-815,-10)),
                texture("Growth_albedo",(-550,-30)))
    rough = mix("Wood and foliage microfinish",(-40,60),texture("Soil_rough",(-815,-315)),data.outputs[1])
    normal_color = mix("Tangent normals",(-40,-165),texture("Soil_normal",(-815,-615)),
                       texture("Growth_normal",(-550,-615)))
    normal = node("ShaderNodeNormalMap",(190,-130),"OpenGL +Y")
    normal.uv_map = UV
    links.new(normal_color,normal.inputs["Color"])
    delta = math_node("MULTIPLY","Premultiplied leaf height",(-270,-420),cov,data.outputs[2])
    height = math_node("ADD","Soil + growth",(190,-380),texture("Soil_height",(-815,-925)),delta)
    shader = node("ShaderNodeBsdfPrincipled",(390,270),"Dry earth and low foliage")
    links.new(color,shader.inputs["Base Color"])
    links.new(rough,shader.inputs["Roughness"])
    links.new(normal.outputs[0],shader.inputs["Normal"])
    links.new(shader.outputs[0],output.inputs["Surface"])
    links.new(height,output.inputs["Height"])
    return graph


def material(group, name, cover):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat["caelm_tile_metres"] = tuple(PERIOD)
    mat["caelm_height_range_metres"] = RELIEF
    n = mat.node_tree.nodes
    n.remove(n.get("Principled BSDF"))
    instance = n.new("ShaderNodeGroup")
    instance.node_tree = group
    instance.label = "Coverage and paint affect growth only"
    instance.location = (-270, 300)
    instance.width = 255
    instance.inputs["Coverage"].default_value = cover
    mat.node_tree.links.new(instance.outputs["Surface"],n["Material Output"].inputs["Surface"])
    return mat


def authored_mesh(growth):
    collection = bpy.data.collections.new("Source · modeled blades, leaves, roots and flowers")
    bpy.context.scene.collection.children.link(collection)
    vertices, faces, colors = [], [], []
    for xyz, rgb, quads, _ in growth.surfaces:
        shift = np.floor(xyz[0,:2]/PERIOD)*PERIOD
        xyz = xyz.copy()
        xyz[:,:2] -= shift
        faces.extend(np.array(quads,dtype=int)+len(vertices))
        vertices.extend(xyz)
        colors.extend(np.column_stack((rgb,np.ones(len(rgb)))))
    model = surface_mesh("Growth bake source, open collection to inspect",vertices,np.asarray(faces))
    attr = model.data.color_attributes.new("Leaf Color","FLOAT_COLOR","POINT")
    attr.data.foreach_set("color",np.asarray(colors,np.float32).ravel())
    mat = plain("Modeled growth | source colors",(.11,.20,.05))
    color = mat.node_tree.nodes.new("ShaderNodeVertexColor")
    color.layer_name = attr.name
    mat.node_tree.links.new(color.outputs[0],mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"])
    model.data.materials.append(mat)
    bpy.context.scene.collection.objects.unlink(model)
    collection.objects.link(model)
    collection.hide_render = collection.hide_viewport = True


def mapped_mesh(name, xyz, faces, uv):
    obj = surface_mesh(name,xyz,faces)
    mapping = obj.data.uv_layers.new(name=UV)
    indices = np.zeros(len(obj.data.loops),dtype=np.int32)
    obj.data.loops.foreach_get("vertex_index",indices)
    mapping.data.foreach_set("uv",uv.reshape(-1,2)[indices].astype(np.float32).ravel())
    obj.data.polygons.foreach_set("use_smooth",np.ones(len(obj.data.polygons),dtype=bool))
    return obj


def flat(field, tiled=False):
    width, depth = (7.2,4.8) if tiled else (3.15,2.25)
    nx,ny = (721,481) if tiled else (526,342)
    x,y = np.meshgrid(np.linspace(-width/2,width/2,nx), np.linspace(-depth/2,depth/2,ny))
    u,v = (x+LENGTH,y+SPAN) if tiled else (x+1.76,y+1.18)
    h = sample(field,u,v)
    return mapped_mesh("Flat ground · metric UV",np.stack((x,y,h),axis=-1).reshape(-1,3),
                       grid_faces(nx,ny),np.stack((u,v),axis=-1))


def sphere(field):
    count, rings = 640, 329
    angle,t = np.meshgrid(np.linspace(0,math.tau,count+1), np.linspace(.001,math.pi-.001,rings))
    u,v = angle*LENGTH/math.tau-1.0, (t/math.pi)*SPAN
    radius = .60+sample(field,u,v)
    xyz = np.stack((np.cos(angle)*np.sin(t)*radius,np.sin(angle)*np.sin(t)*radius,-np.cos(t)*radius),axis=-1)
    obj = mapped_mesh("Material sphere · displaced from packed earth",xyz.reshape(-1,3),
                      grid_faces(count+1,rings),np.stack((u,v),axis=-1))
    # Weld the physical seam while keeping each loop's own UV.
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.remove_doubles(threshold=.00003)
    bpy.ops.object.mode_set(mode="OBJECT")
    obj.select_set(False)
    return obj


def set_lighting(scene):
    scene.world = bpy.data.worlds.new("Neutral review studio")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (.30,.33,.37,1.)
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = .46
    for name, pos, power, size, color in (
        ("Broad raking key",(-2.3,-1.6,2.75),220,2.6,(1.,.94,.86)),
        ("Sky fill",(1.6,-2.1,1.3),85,3.0,(.91,.95,1.)),
    ):
        light = bpy.data.lights.new(name,"AREA")
        light.energy,light.shape,light.size,light.color = power,"DISK",size,color
        obj = bpy.data.objects.new(name,light)
        scene.collection.objects.link(obj)
        obj.location = pos
        point(obj,(0,0,0))

    light = bpy.data.lights.new("Repeat · even daylight","SUN")
    light.energy,light.angle = 1.65,.17
    repeat_light = bpy.data.objects.new(light.name,light)
    scene.collection.objects.link(repeat_light)
    repeat_light.location = (-3,-3,6)
    point(repeat_light,(0,0,0))
    repeat_light.hide_render = True


def comparison(scene, fields, earth, bare, sparse, draft, render):
    few = fields["Growth_data"][:,:,2]*RELIEF
    # A cool, dark neutral world background keeps the silhouette easy to inspect.
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.render.resolution_percentage = 100
    objects = []
    for label, maker, position, target, scale, dimensions, states in (
        ("Sphere",sphere,(.12,-2.40,.17),(0,0,0),1.43,(980,980),("Bare","Sparse")),
        ("Ground",flat,(.15,-2.50,2.90),(0,0,0),2.06,(1330,900),("Bare","Sparse")),
        ("Detail",flat,(-.16,-1.15,1.07),(-.20,.16,0),.97,(1330,900),("Bare","Sparse")),
        ("Repeat",lambda field:flat(field,tiled=True),(0,0,8),(0,0,0),
         7.50,(1500,1010),("Sparse",)),
    ):
        camera = bpy.data.objects.new(label,bpy.data.cameras.new(label))
        scene.collection.objects.link(camera)
        scene.camera = camera
        camera.data.type = "ORTHO"
        camera.location = position
        point(camera,target)
        camera.data.ortho_scale = scale
        for light in (obj for obj in scene.objects if obj.type=="LIGHT"):
            light.hide_render = (label=="Repeat") != (light.data.type=="SUN")
        for name in states:
            mat, field = (bare,earth*.78) if name=="Bare" else (sparse,earth*.78+few*.48)
            if label=="Detail":
                obj = objects[2 if name=="Bare" else 3]
            else:
                obj = maker(field)
                obj.name = f"{label} · {name}"
                obj.data.materials.append(mat)
                objects.append(obj)
            obj.hide_render = obj.hide_viewport = False
            if render:
                scene.render.resolution_x,scene.render.resolution_y = dimensions
                scene.render.resolution_percentage = 58 if draft else 100
                scene.render.filepath = str(path(f"{label}_{name}","png"))
                bpy.ops.render.render(write_still=True)
            obj.hide_render = obj.hide_viewport = True
    # Save a ready-to-inspect material scene on the sparse flat comparison.
    scene.camera = bpy.data.objects["Ground"]
    for light in (obj for obj in scene.objects if obj.type=="LIGHT"):
        light.hide_render = light.data.type=="SUN"
    obj = objects[3]
    obj.hide_render = obj.hide_viewport = False
    scene.render.resolution_percentage = 100
    scene.render.resolution_x, scene.render.resolution_y = 1330,900


def main():
    cli = ArgumentParser()
    cli.add_argument("--seed",type=int,default=GROWTH_SEED)
    cli.add_argument("--cluster",type=float,default=.88)
    cli.add_argument("--draft",action="store_true")
    cli.add_argument("--skip-render",action="store_true")
    cli.add_argument("--verify-repeat",action="store_true")
    cli.add_argument("--optix",action="store_true")
    opts = cli.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    if opts.seed<0 or not 0<=opts.cluster<=1:
        cli.error("Use a nonnegative seed and cluster from zero to one.")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = "Lowmark Sparse Vegetation Ground"
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
    scene.cycles.samples = 24 if opts.draft else 64
    scene.cycles.use_denoising = True
    scene.cycles.adaptive_threshold = .012
    size = tuple(n//2 for n in SIZE) if opts.draft else SIZE
    fields, earth, growth = build(size, opts.seed, opts.cluster)
    verify(fields,earth,growth,size,(opts.seed,) if opts.verify_repeat else (),opts.cluster)
    export(scene, fields)
    group = material_group()
    bare = material(group,"Lowmark Ground | Bare Foundation",0.)
    sparse = material(group,"Lowmark Ground | Sparse Vegetation",1.)
    for mat in (bare,sparse):
        mat.use_fake_user = True
    authored_mesh(growth)
    set_lighting(scene)
    comparison(scene,fields,earth,bare,sparse,opts.draft,not opts.skip_render)
    scene["caelm_growth_seed"] = opts.seed
    scene["caelm_growth_cluster"] = opts.cluster
    scene["caelm_tile_metres"] = tuple(PERIOD)
    scene.render.filepath = "//"
    for image in bpy.data.images:
        if image.source=="FILE":
            image.filepath = f"//{Path(image.filepath).name}"
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/f"{STEM}.blend"),relative_remap=False,compress=True)


if __name__ == "__main__":
    main()
