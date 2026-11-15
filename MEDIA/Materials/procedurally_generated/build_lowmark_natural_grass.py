"""Generate Lowmark's metric vegetation meshes, foliage atlas and review scenes."""

from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
import math
import struct
import sys

import bpy
import numpy as np
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from build_lowmark_structural_timber import point, profile, ramp

STEM = "Lowmark_Natural_Grass_Wildflowers"
SEED = 49163
CELL = 256
ATLAS = 1024
GUTTER = 12
TAU = 2 * math.pi
UP = Vector((0, 0, 1))


@dataclass(frozen=True)
class Habitat:
    label: str
    moisture: float
    verge: float
    density: float


HABITATS = {
    "Short_Sward": Habitat("Short sward", .57, .69, 46),
    "Mixed_Verge": Habitat("Mixed verge", .63, .88, 29),
    "Dry_Roadside": Habitat("Dry roadside", .23, .94, 22),
    "Meadow_Seed": Habitat("Meadow seed heads", .45, .67, 9),
    "Ribbed_Rosette": Habitat("Ribbed rosettes", .53, .85, 12),
    "Wayside_Yarrow": Habitat("Cream wayside flowers", .39, .55, 6),
    "Selfheal": Habitat("Violet selfheal", .70, .46, 8),
}

# Colors are scene-linear plant tissue. Coordinates follow a leaf from its
# sheath or petiole towards its tip, so senescence and venation follow growth.
TISSUE = (
    ((.058, .093, .020), (.18, .245, .062), .56),  # fresh folded blade
    ((.067, .088, .023), (.21, .239, .074), .61),  # olive blade
    ((.083, .067, .026), (.31, .225, .098), .75),  # partly cured blade
    ((.123, .084, .033), (.39, .280, .133), .79),  # dry straw
    ((.030, .073, .021), (.102, .163, .050), .55), # ribbed plantain
    ((.033, .079, .032), (.104, .171, .061), .57), # selfheal leaf
    ((.040, .072, .027), (.133, .181, .071), .67), # yarrow foliage
    ((.046, .072, .025), (.148, .167, .052), .60), # living stems
    ((.093, .081, .029), (.246, .213, .086), .68), # green panicle
    ((.152, .092, .037), (.392, .287, .141), .80), # spent panicle
    ((.044, .032, .012), (.141, .101, .038), .76), # plantain spike
    ((.167, .079, .169), (.336, .203, .365), .60), # violet corolla
    ((.335, .290, .142), (.758, .721, .541), .64), # yarrow florets
    ((.102, .066, .024), (.271, .194, .080), .73), # dried umbels
    ((.335, .290, .142), (.758, .721, .541), .64), # cream corymb cutout
    ((.102, .066, .024), (.271, .194, .080), .73), # dried corymb cutout
)


def line_distance(x, y, start, end):
    ax, ay = start
    dx, dy = end[0] - ax, end[1] - ay
    t = np.clip(((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy), 0, 1)
    return np.hypot(x - ax - dx * t, y - ay - dy * t)


def panicle_alpha(x, y, index):
    """Cutout for an open, alternating fine-grass panicle; RGB extends to the gutter."""
    rng = np.random.default_rng(280 + index)
    shape = .0055 - line_distance(x, y, (.48, .018), (.53, .96))
    for level in range(6):
        start = (.48 + level * .007, .14 + level * .125)
        for sign in (-1, 1):
            span = (.42 - level * .045) * rng.uniform(.66, 1.)
            tip = (start[0] + sign * span, start[1] + rng.uniform(.085, .17))
            shape = np.maximum(shape, .0028 - line_distance(x, y, start, tip))
            for fraction in (.68, .97):
                joint = tuple(a + fraction * (b - a) for a, b in zip(start, tip))
                ending = (joint[0] + sign * .019, joint[1] + rng.uniform(.036, .060))
                shape = np.maximum(shape, rng.uniform(.0085, .012) - line_distance(x, y, joint, ending))
    return np.clip(.5 + shape * (CELL - 2 * GUTTER), 0, 1)


def corymb_alpha(x, y, index):
    shapes = np.full_like(x,-1.)
    rng = np.random.default_rng(7813 + index)
    for i in range(7):
        angle = i*2.4
        distance = .16+.19*math.sqrt(i/6)
        cx, cy = .5+math.cos(angle)*distance, .5+math.sin(angle)*distance
        for j in range(5):
            a = angle + j*TAU/5
            radius = rng.uniform(.045,.064)
            da, db = cx+math.cos(a)*.072, cy+math.sin(a)*.072
            shapes = np.maximum(shapes,radius-np.hypot(x-da,y-db))
    return np.clip(.5+shapes*(CELL-2*GUTTER),0,1)


def atlas_maps():
    channel = np.arange(CELL, dtype=np.float32)
    channel = np.clip((channel + .5 - GUTTER) / (CELL - GUTTER * 2), 0, 1)
    x, y = np.meshgrid(channel, channel)
    images = {key: np.ones((ATLAS, ATLAS, 4), dtype=np.float32)
              for key in ("albedo", "normal", "roughness")}
    for i, (base, tip, rough) in enumerate(TISSUE):
        grain = profile(x, y, 26, 4, 310 + i, periodic=False) - .5
        tissue = profile(x, y, 8, 8, 515 + i, periodic=False) - .5
        taper = ramp(.04, .94, y)
        midrib = np.exp(-((x - .5) / .032) ** 2) * (1 - .6 * taper)
        if i == 4:
            for ridge in (.23, .36, .64, .77):
                midrib += .50 * np.exp(-((x - ridge - .13 * (ridge - .5) * y) / .016) ** 2)
        if i in (0, 1, 2, 3, 4, 5, 6, 7):
            branch = np.cos((y - np.abs(x - .5) * .19) * TAU * 12)
            veins = .13 * np.maximum(branch, 0) ** 12 * ramp(.08, .35, np.abs(x - .5))
            veins *= 1. if i in (4, 5, 6) else .24
        else:
            midrib *= .08
            veins = 0.
        relief = .0028 * midrib + .0032 * grain + .0019 * tissue + .0024 * veins
        dy, dx = np.gradient(relief)
        direction = np.dstack((-dx * 135, -dy * 135, np.ones_like(dx)))
        normal = .5 + .5 * direction / np.linalg.norm(direction, axis=2, keepdims=True)
        color = np.asarray(base) + taper[:, :, None] * (np.asarray(tip) - base)
        color *= (1 + .18 * grain + .35 * tissue + .12 * midrib + .18 * veins)[:, :, None]
        if i in (1, 2, 3, 4, 5):
            speckle = ramp(.22, .43, profile(x, y, 36, 31, 189 + i, periodic=False) - .5)
            stress = speckle * ramp(.23, .79, y) * (.65 if i in (2, 3) else .26)
            color *= (1 - .57 * stress[:, :, None])
        col, row = i % 4, i // 4
        tile = np.s_[row * CELL:(row+1) * CELL, col * CELL:(col+1) * CELL]
        images["albedo"][tile][:, :, :3] = color
        if i in (8, 9):
            images["albedo"][tile][:, :, 3] = panicle_alpha(x, y, i)
        elif i in (14, 15):
            images["albedo"][tile][:, :, 3] = corymb_alpha(x, y, i)
        images["normal"][tile][:, :, :3] = normal
        gloss = np.clip(rough + .10 * tissue - .041 * midrib + .075 * taper, .44, .93)
        images["roughness"][tile][:, :, :3] = gloss[:, :, None]
    return images


def write_maps(scene, maps):
    settings = scene.render.image_settings
    settings.file_format = "PNG"
    settings.color_depth = "8"
    settings.color_management = "OVERRIDE"
    settings.view_settings.view_transform = "Standard"
    settings.view_settings.look = "None"
    for key, rgba in maps.items():
        color = key == "albedo"
        settings.color_mode = "RGBA" if color else "RGB"
        img = bpy.data.images.new(f"Foliage {key}", ATLAS, ATLAS, alpha=True, float_buffer=True)
        img.colorspace_settings.name = "Linear Rec.709" if color else "Non-Color"
        if color:
            # Blender's float image buffers use premultiplied alpha by default.
            # A straight buffer keeps colored padding under transparent panicle pixels.
            img.alpha_mode = "STRAIGHT"
        img.pixels.foreach_set(rgba.ravel())
        img.save_render(str(ROOT / f"{STEM}_{key}.png"), scene=scene)
        bpy.data.images.remove(img)
    settings.color_management = "FOLLOW_SCENE"


def foliage_material():
    mat = bpy.data.materials.new("Lowmark foliage atlas")
    mat.use_nodes = True
    mat.use_backface_culling = False
    mat.surface_render_method = "DITHERED"
    mat.diffuse_color = (.11, .17, .041, 1)
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    shader = nodes["Principled BSDF"]
    shader.inputs["Metallic"].default_value = 0
    shader.inputs["Subsurface Weight"].default_value = .08
    shader.inputs["Subsurface Scale"].default_value = .004
    tex = {}
    for i, key in enumerate(("albedo", "normal", "roughness")):
        node = nodes.new("ShaderNodeTexImage")
        node.label = key.title()
        node.location = (-620, 220 - 270 * i)
        node.image = bpy.data.images.load(str(ROOT / f"{STEM}_{key}.png"))
        node.image.colorspace_settings.name = "sRGB" if key == "albedo" else "Non-Color"
        tex[key] = node
    mask = nodes.new("ShaderNodeMath")
    mask.operation = "GREATER_THAN"
    mask.inputs[1].default_value = .48
    mask.location = (-280, 50)
    norm = nodes.new("ShaderNodeNormalMap")
    norm.inputs["Strength"].default_value = .70
    norm.location = (-280, -155)
    links.new(tex["albedo"].outputs["Color"], shader.inputs["Base Color"])
    links.new(tex["albedo"].outputs["Alpha"], mask.inputs[0])
    links.new(mask.outputs[0], shader.inputs["Alpha"])
    links.new(tex["normal"].outputs["Color"], norm.inputs["Color"])
    links.new(norm.outputs["Normal"], shader.inputs["Normal"])
    links.new(tex["roughness"].outputs["Color"], shader.inputs["Roughness"])
    return mat


def radial(angle):
    return Vector((math.cos(angle), math.sin(angle), 0))


class Mesh:
    def __init__(self, lod):
        self.lod = lod
        self.vertices = []
        self.faces = []
        self.uvs = []

    def add(self, points, faces, uv, tile):
        offset = len(self.vertices)
        self.vertices.extend(tuple(v) for v in points)
        self.faces.extend(tuple(i + offset for i in face) for face in faces)
        col, row = tile % 4, tile // 4
        extent = CELL - 2 * GUTTER
        self.uvs.extend(((col * CELL + GUTTER + u * extent) / ATLAS,
                         (row * CELL + GUTTER + v * extent) / ATLAS) for u, v in uv)

    def ribbon(self, root, heading, length, width, rise, reach, curl, twist, tile,
               *, broad=False, minimum=0., small=False):
        """Taper a living leaf along a bent midrib with an asymmetric cross section."""
        steps = ((3, 2, 1) if small else (6, 4, 2))[self.lod]
        multi = not small and (self.lod == 0 or broad and self.lod == 1)
        bands = (-1., 0., 1.) if multi else (-1., 1.)
        forward = radial(heading)
        points, uv, faces = [], [], []
        for j in range(steps):
            t = j / steps
            lateral = radial(heading + math.pi / 2 + twist * t)
            center = root + length * (forward * (reach * t ** 1.38) + UP * (rise * t - curl * t ** 3))
            center += lateral * length * twist * .18 * t ** 2
            width_curve = (.31 + .69 * math.sin(math.pi * t ** .62) ** .69) if broad else (1. - t) ** .57 * (.72 + .28 * min(t * 5, 1))
            edge = max(width * width_curve, minimum) * .5
            for side in bands:
                position = center + lateral * side * edge * (1 + .16 * t * side)
                position += UP * edge * (abs(side) * (.31 + twist * .19 * side))
                points.append(position)
                uv.append((.5 + side * .493, t))
        tip = root + length * (forward * reach + UP * (rise - curl))
        tip += radial(heading + math.pi / 2 + twist) * length * twist * .18
        k = len(bands)
        for j in range(steps-1):
            for i in range(k-1):
                a = j*k + i
                faces.append((a, a+k, a+k+1, a+1))
        for i in range(k-1):
            a = (steps-1)*k+i
            faces.append((a, len(points), a+1))
        self.add(points + [tip], faces, uv + [(.5, 1)], tile)

    def stem(self, start, end, radius, tile, bend=None):
        lateral = (end - start).cross(Vector((1, .03, 0))).normalized()
        second = (end - start).normalized().cross(lateral)
        centers = (start, bend, end) if bend is not None and self.lod < 2 else (start, end)
        sides = (4, 3, 2)[self.lod]
        points, faces, uv = [], [], []
        for j, center in enumerate(centers):
            t = j / (len(centers)-1)
            for i in range(sides):
                a = TAU*i/sides
                points.append(center + (lateral*math.cos(a) + second*math.sin(a))*radius*(1-.34*t))
                uv.append((.19 + .61*i/(sides-1), t))
        usable = sides if sides > 2 else 1
        for j in range(len(centers)-1):
            for i in range(usable):
                a, b = j*sides+i, j*sides+(i+1)%sides
                faces.append((a, b, b+sides, a+sides))
        self.add(points, faces, uv, tile)

    def spikelet(self, start, end, radius, tile, *, sides=4, profile_scale=1.):
        axis = (end-start).normalized()
        lateral = axis.cross(Vector((1, .03, .012))).normalized()
        second = axis.cross(lateral)
        middle = start.lerp(end, .46)
        points = [start, end]
        uv = [(.5, .06), (.55, .95)]
        for i in range(sides):
            a = TAU*i/sides
            points.append(middle + (lateral*math.cos(a) + second*math.sin(a)*profile_scale)*radius)
            uv.append((.5 + .41*math.cos(a), .56))
        faces = []
        for i in range(sides):
            a, b = 2+i, 2+(i+1)%sides
            faces.extend(((0,b,a), (a,b,1)))
        self.add(points, faces, uv, tile)

    def panicle_card(self, foot, tip, span, heading, tile):
        sideways = radial(heading) * span
        center = foot.lerp(tip, .52)
        points = (foot-sideways*.72, foot+sideways*.72, center+sideways, center-sideways,
                  tip+sideways*.62, tip-sideways*.62)
        self.add(points, ((0,1,2,3), (3,2,4,5)),
                 ((0.,0.), (1.,0.), (1.,.52), (0.,.52), (1.,1.), (0.,1.)), tile)

    def corymb_card(self, center, heading, radius, tile):
        forward, lateral = radial(heading)*radius, radial(heading+math.pi/2)*radius
        rise = UP*radius*.27
        corners = (center-forward-lateral-rise, center+forward-lateral-rise,
                   center+forward+lateral+rise, center-forward+lateral+rise)
        self.add(corners,((0,1,2,3),),((0.,0.),(1.,0.),(1.,1.),(0.,1.)),tile)

    def blossom(self, center, radius, heading, tile, petals):
        root = center - UP*radius*.23
        rim = [root + radial(heading + i*TAU/petals) * radius for i in range(petals)]
        for i in range(petals):
            rim[i].z += radius * (.26 if i % 2 else .59)
        points = [center] + rim
        faces = [(0, 1+i, 1+(i+1)%petals) for i in range(petals)]
        uv = [(.50, .44)] + [(.5 + .40*math.cos(i*TAU/petals), .55 + .41*math.sin(i*TAU/petals))
                             for i in range(petals)]
        self.add(points, faces, uv, tile)

    def object(self, name, mat):
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(self.vertices, [], self.faces)
        mesh.update()
        if mesh.validate(verbose=True):
            raise RuntimeError(f"Invalid topology in {name}")
        uv = mesh.uv_layers.new(name="UV0")
        uv.data.foreach_set("uv", np.asarray(self.uvs, np.float32)[[loop.vertex_index for loop in mesh.loops]].ravel())
        mesh.polygons.foreach_set("use_smooth", np.ones(len(mesh.polygons), bool))
        mesh.materials.append(mat)
        return bpy.data.objects.new(name, mesh)


def grass(mesh, family, rng, density, moisture, stage):
    count, low, high, width, radius = {
        "Short_Sward": (35, .046, .165, .0055, .065),
        "Mixed_Verge": (35, .090, .292, .009, .069),
        "Dry_Roadside": (26, .064, .257, .0057, .049),
        "Meadow_Seed": (17, .077, .245, .0068, .056),
    }[family]
    dry = family == "Dry_Roadside"
    seeds = rng.integers(0, 2**32, max(6, round(count * density) - stage * 2))
    occupied = round(len(seeds) * (1., .72, .46)[mesh.lod])
    share = rng.uniform(-math.pi, math.pi)
    buds = (Vector((0,0,0)), radial(share + 1.2) * radius*.65, radial(share - 1.5) * radius*.8)
    for i, seed in enumerate(seeds[:occupied]):
        r = np.random.default_rng(seed)
        aim = share + r.uniform(-math.pi, math.pi)
        root = buds[i % len(buds)] + radial(aim + r.uniform(-.8,.8))*radius*r.uniform(.05,.78)
        root.z = r.uniform(-.010, .005)
        juvenile = (i % 5 == 0)
        tall = r.uniform(low, high)*(1.0 if stage else .85)*(1.05 if juvenile else 1.)
        lean = r.uniform(.22, .83) if juvenile else r.uniform(.31, 1.16)
        erect = r.uniform(.59, 1.16) if not dry else r.uniform(.30, .89)
        hook = min(erect-.10,r.uniform(.07,.42 if not dry else .50))
        aging = (1-moisture)*1.04 + stage*.28 + r.uniform(-.56,.53) + (.86 if dry else -.27 if juvenile else 0)
        tile = 3 if aging > 1.36 else 2 if aging > .84 else 1 if aging > .35 else 0
        mesh.ribbon(root, aim, tall, width*r.uniform(.48,1.58), erect, lean, hook,
                    r.uniform(-.68,.68), tile, minimum=.0023 if mesh.lod == 2 else 0)
    if family != "Short_Sward":
        stems = {"Mixed_Verge": (0,1,2), "Dry_Roadside": (1,2,3), "Meadow_Seed": (3,4,5)}[family][stage]
        for index, seed in enumerate(rng.integers(0, 2**32, stems)):
            r = np.random.default_rng(seed)
            foot = buds[index % len(buds)]
            direction = share + r.uniform(-1.6, 1.6)
            panicle(mesh, r, foot, direction, r.uniform(.24, .47) if not dry else r.uniform(.17,.32),
                    dry or stage == 2)


def panicle(mesh, rng, root, aim, height, dry):
    reach = radial(aim)*height*rng.uniform(.09,.44)
    tip = root + UP*height + reach
    head = root.lerp(tip,.67)
    bend = root.lerp(head,.55) - reach*.12
    mesh.stem(root, head, height*.005, 2 if dry else 7, bend)
    tile = 9 if dry else 8
    width = height*rng.uniform(.085,.15)
    if mesh.lod == 2:
        for yaw in (aim, aim + math.pi/2):
            mesh.panicle_card(head, tip, width*.86, yaw, tile)
        return
    seed_tile = 3 if dry else 2
    mesh.stem(head, tip, height*.002, 2 if dry else 7)
    for j in range((6,4)[mesh.lod]):
        t = .075 + j*.145
        joint = head.lerp(tip, t)
        yaw = aim + j*2.40 + rng.uniform(-.38,.38)
        for offset in (0, math.pi*.91):
            direction = radial(yaw + offset)
            branch = joint + direction*width*(1-.71*t)*rng.uniform(.55,1.04) + UP*height*(.06+.018*t)
            mesh.stem(joint, branch, height*.00115, 2 if dry else 7)
            for fraction in ((.66,1.) if mesh.lod == 0 else (1.,)):
                base = joint.lerp(branch,fraction)
                spike_tip = base + UP*height*rng.uniform(.012,.028) + direction*height*.007
                mesh.spikelet(base,spike_tip,height*.0047,seed_tile,sides=(4,3)[mesh.lod],profile_scale=.73)


def rosette(mesh, rng, density, moisture, stage):
    leaves = max(5, round(8*density))
    yaw = rng.uniform(0, TAU)
    root = Vector((0,0,-.005))
    for i, seed in enumerate(rng.integers(0,2**32,leaves)):
        r = np.random.default_rng(seed)
        if i >= round(leaves*(1.,.85,.68)[mesh.lod]):
            continue
        angle = yaw + 2.40*i + r.uniform(-.29,.29)
        length = r.uniform(.116,.239)*(.76 if stage == 0 else 1.)
        aged = stage == 2 and i > leaves*.7 and moisture < .6
        mesh.ribbon(root,angle,length,r.uniform(.023,.048),r.uniform(.43,.83),r.uniform(.66,1.05),
                    r.uniform(.08,.25),r.uniform(-.47,.44),2 if aged else 4,broad=True)
    for i in range(stage):
        aim = radial(yaw+2.3*i)
        tip = aim*rng.uniform(.025,.090)+UP*rng.uniform(.18,.28)
        head = tip + UP*rng.uniform(.022,.034)
        mesh.stem(root,tip,.00155,7,bend=(root+tip)*.49-aim*.017)
        mesh.spikelet(tip,head,.0064,10,sides=(7,5,4)[mesh.lod])
        if stage == 1:
            for j in range((9,6,3)[mesh.lod]):
                pos = tip.lerp(head,.33) + radial(yaw+j*TAU/(9,6,3)[mesh.lod])*.008
                mesh.blossom(pos,.0028,yaw,12,4)


def yarrow_leaf(mesh, start, aim, length):
    forward = radial(aim)
    tip = start + length*(forward*.91+UP*.24)
    mesh.stem(start,tip,.0011,6)
    for i in range((8,5,3)[mesh.lod]):
        t = (i+.9)/(8,5,3)[mesh.lod]
        attachment = start.lerp(tip,t)
        span = length*.36*(.31+.69*math.sin(math.pi*t))*(1-.39*t)
        for direction in (-1,1):
            turn = aim + direction*1.09
            mesh.ribbon(attachment,turn,span,span*.26,.43,.91,.16,.15*direction,6,broad=True,small=True)
            if mesh.lod == 0 and .20<t<.85:
                leaflet = attachment + radial(turn)*span*.42 + UP*span*.12
                mesh.ribbon(leaflet,turn+direction*.64,span*.37,span*.081,.36,.86,.10,.08,6,small=True)


def yarrow(mesh, rng, density, stage):
    yaw = rng.uniform(0,TAU)
    root = Vector((0,0,-.009))
    shoots = max(1, round((2 if stage else 1)*density))
    for i, seed in enumerate(rng.integers(0,2**32,shoots)):
        r = np.random.default_rng(seed)
        direction = radial(yaw + i*2.24)
        length = r.uniform(.205,.334) if stage != 2 else r.uniform(.266,.423)
        apex = direction*length*.24 + UP*length
        bend = root.lerp(apex,.49)-direction*.014
        mesh.stem(root,apex,.0024,2 if stage==2 else 7,bend)
        for j in range((5,4,3)[mesh.lod]):
            t = (.18,.34,.57,.24,.68)[j]
            position = (root.lerp(bend,t/.49) if t < .49 else bend.lerp(apex,(t-.49)/.51))
            yarrow_leaf(mesh,position,yaw+i*2.24+j*2.40, length*(.31-.22*t))
        bloom_tiles = (12,12,13)
        branch_count = (6,4,3)[mesh.lod]
        for j, branch_seed in enumerate(r.integers(0,2**32,6)[:branch_count]):
            blossom_rng = np.random.default_rng(branch_seed)
            angle = yaw + j*2.40
            spread = (.008+.025*(j%3)*.65)*(1 if stage else .64)
            cap = apex+radial(angle)*spread+UP*blossom_rng.uniform(.010,.032)
            joint = apex - UP*(.033+(.006*j))
            mesh.stem(joint,cap,.0011,7)
            if mesh.lod == 2:
                mesh.corymb_card(cap,angle,blossom_rng.uniform(.011,.016),15 if stage==2 else 14)
                continue
            for k in range((5,3)[mesh.lod]):
                pos = cap+radial(angle+k*2.40)*blossom_rng.uniform(.002,.010)+UP*blossom_rng.uniform(-.002,.003)
                mesh.stem(cap - UP*.008,pos,.0006,7)
                mesh.blossom(pos,blossom_rng.uniform(.0030,.0048),angle+k,bloom_tiles[stage],8 if mesh.lod==0 else 5)


def selfheal(mesh, rng, density, stage):
    root = Vector((0,0,-.010))
    yaw = rng.uniform(0,TAU)
    for i, seed in enumerate(rng.integers(0,2**32,max(1,round((2+int(stage!=0))*density)))):
        r = np.random.default_rng(seed)
        direction = radial(yaw+i*2.40)
        bottom = root + direction*r.uniform(.025,.052)
        apex = bottom+UP*r.uniform(.137,.251)+direction*r.uniform(.017,.056)
        head = apex + UP*r.uniform(.036,.047)
        mesh.stem(bottom,apex,.0021,7,bend=(bottom+apex)*.49)
        for j in range((4,3,2)[mesh.lod]):
            t = (.28,.54,.13,.71)[j]
            for k in (0,1):
                angle = yaw+i*1.7+j*math.pi*.5+k*math.pi
                mesh.ribbon(bottom.lerp(apex,t),angle,r.uniform(.044,.070)*(1-.45*t),r.uniform(.015,.024),
                            .34,1.,.16,.16,5,broad=True)
        mesh.spikelet(apex,head,.010,10,sides=(7,5,4)[mesh.lod])
        for j in range(4 if mesh.lod==0 else 3):
            tier = apex.lerp(head,(j+.65)/4.8)
            petals = (5,4,3)[mesh.lod]
            for k in range(petals):
                angle = yaw+k*TAU/petals+j*.77
                outward = radial(angle)
                pos = tier+outward*(.009+.001*(j%2))
                mesh.blossom(pos,r.uniform(.0045,.0070),angle,11 if stage else 5,6)
                if mesh.lod == 0 and stage:
                    mesh.spikelet(tier,pos+UP*.003,.0028,11,sides=4)


def plant(family, variant, lod, opts):
    kind = tuple(HABITATS).index(family)
    rng = np.random.default_rng(np.random.SeedSequence((opts.seed,kind,variant)))
    mesh = Mesh(lod)
    if kind < 4:
        grass(mesh,family,rng,opts.density,opts.moisture,variant)
    elif family == "Ribbed_Rosette":
        rosette(mesh,rng,opts.density,opts.moisture,variant)
    elif family == "Wayside_Yarrow":
        yarrow(mesh,rng,opts.density,variant)
    else:
        selfheal(mesh,rng,opts.density,variant)
    mesh.vertices = [(x,y,z*opts.height) for x,y,z in mesh.vertices]
    return mesh


def library(scene, mat, opts):
    collection = bpy.data.collections.new("Lowmark Natural Grass and Wildflowers")
    scene.collection.children.link(collection)
    records, signature = {}, hashlib.sha256()
    for family, habitat in HABITATS.items():
        for i, stage in enumerate(("Young","Established","Late")):
            group = bpy.data.collections.new(f"{family}_{stage}")
            collection.children.link(group)
            variations = []
            for lod in range(3):
                name = f"LM_{family}_{stage}_LOD{lod}"
                source = plant(family,i,lod,opts)
                obj = source.object(name,mat)
                group.objects.link(obj)
                mesh = obj.data
                mesh.calc_loop_triangles()
                tris = len(mesh.loop_triangles)
                points = np.asarray(source.vertices)
                extent = np.ptp(points,axis=0)
                if not np.isfinite(points).all() or min(extent)<=0 or np.any(extent>1.1):
                    raise RuntimeError(f"Invalid metre dimensions for {name}: {extent}")
                if points[:,2].max() <= .025 or points[:,2].min() > .014:
                    raise RuntimeError(f"Invalid ground pivot for {name}")
                uv = np.asarray(source.uvs,dtype=np.float32)
                faces = np.asarray([i for face in source.faces for i in (*face,-1)],np.int32)
                packed = (points.astype("<f4").tobytes(), uv.astype("<f4").tobytes(), faces.astype("<i4").tobytes())
                signature.update(name.encode())
                for part in packed:
                    signature.update(part)
                if opts.verify_repeat:
                    check = plant(family,i,lod,opts)
                    if source.vertices != check.vertices or source.faces != check.faces or source.uvs != check.uvs:
                        raise RuntimeError(f"Independent generation differs for {name}")
                if any(f.area < 2e-10 for f in mesh.polygons) or not np.all((uv > 0)&(uv < 1)):
                    raise RuntimeError(f"Invalid triangles or atlas coordinates for {name}")
                metadata = {"asset_family":family,"growth_stage":stage,"lod":lod,"triangles":tris,
                            "height_m":float(points[:,2].max()),"footprint_m":[float(x) for x in extent[:2]],
                            "moisture_preference_01":habitat.moisture,"path_edge_affinity_01":habitat.verge,
                            "patch_density_per_m2":habitat.density,"source_seed":opts.seed,
                            "authoring_moisture_01":opts.moisture,"authoring_blade_density":opts.density}
                for key, value in metadata.items():
                    obj[key] = value
                if lod == 0:
                    obj.asset_mark()
                    obj.asset_data.description = f"{habitat.label}, {stage.lower()} growth. Metre units."
                    obj.asset_data.tags.new("Lowmark")
                    obj.asset_data.tags.new("Vegetation")
                variations.append(obj)
            budgets = [ob["triangles"] for ob in variations]
            if not 0 < budgets[2] < budgets[1] < budgets[0] < 3800:
                raise RuntimeError(f"Invalid LOD budgets for {family} {stage}: {budgets}")
            records[family,i] = variations
            print(f"{family:17} {stage:11} {str(budgets):20} H {variations[0]['height_m']:.3f} m",flush=True)
    print(f"Mesh/UV signature {signature.hexdigest()}", flush=True)
    return collection, records


def check_glb(path, records):
    with path.open("rb") as stream:
        magic, version, total = struct.unpack("<4sII",stream.read(12))
        length, kind = struct.unpack("<I4s",stream.read(8))
        if (magic,version,total,kind) != (b"glTF",2,path.stat().st_size,b"JSON"):
            raise RuntimeError("Invalid glTF container")
        document = json.loads(stream.read(length))
    nodes = {node["name"]:node for node in document["nodes"] if "mesh" in node}
    expected_names = {ob.name for variants in records.values() for ob in variants}
    if set(nodes)!=expected_names or len(document["materials"])!=1:
        raise RuntimeError("glTF mesh hierarchy or material count differs from source")
    for name, node in nodes.items():
        primitive, = document["meshes"][node["mesh"]]["primitives"]
        triangles = document["accessors"][primitive["indices"]]["count"]//3
        if triangles!=node["extras"]["triangles"] or not {"POSITION","NORMAL","TANGENT","TEXCOORD_0"}<=primitive["attributes"].keys():
            raise RuntimeError(f"glTF mesh channels or triangle count differ for {name}")
        if "translation" in node or "scale" in node:
            raise RuntimeError(f"Unbaked pivot or scale in {name}")
    mat, = document["materials"]
    pbr = mat["pbrMetallicRoughness"]
    if not (mat["alphaMode"]=="MASK" and abs(mat["alphaCutoff"]-.48)<.0001 and mat["doubleSided"]
            and pbr["metallicFactor"]==0 and "baseColorTexture" in pbr
            and "metallicRoughnessTexture" in pbr and "normalTexture" in mat):
        raise RuntimeError("glTF vegetation channel bindings differ from source")
    print(f"Verified {len(nodes)} glTF meshes, metre pivots and two-sided alpha-cutout PBR",flush=True)


def check_atlas(maps, mat):
    for key in maps:
        node = next(n for n in mat.node_tree.nodes if n.label==key.title())
        image = node.image
        pixels = np.empty(len(image.pixels), np.float32)
        image.pixels.foreach_get(pixels)
        pixels = pixels.reshape(ATLAS,ATLAS,4)
        expected = maps[key]
        if key == "albedo":
            np.testing.assert_allclose(pixels[:,:,3],expected[:,:,3],atol=.006,rtol=0)
            if np.min(pixels[2*CELL:3*CELL,:2*CELL,:3])<.005:
                raise RuntimeError("Panicle atlas lost colored padding under transparent texels")
        else:
            np.testing.assert_allclose(pixels[:,:,:3],expected[:,:,:3],atol=.006,rtol=0)
    print("Reopened 1024 px atlas maps with verified opacity, filtered padding and linear data",flush=True)


def setup_review(scene, opts):
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 28 if opts.draft else 70
    scene.cycles.use_denoising = True
    scene.cycles.adaptive_threshold = .012
    if opts.optix:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "OPTIX"
        prefs.refresh_devices()
        if not any(d.type=="OPTIX" for d in prefs.devices):
            raise RuntimeError("No Cycles OptiX device found")
        for device in prefs.devices:
            device.use = device.type=="OPTIX"
        scene.cycles.device = "GPU"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.world = bpy.data.worlds.new("Lowmark open sky")
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes["Background"]
    background.inputs["Color"].default_value = (.73,.84,1.,1.)
    background.inputs["Strength"].default_value = .44
    bpy.ops.object.light_add(type="SUN",location=(-1.8,-3.7,5.5))
    sun = bpy.context.object
    sun.name = "Afternoon sun"
    sun.data.energy = 2.30
    sun.data.color = (1.,.89,.72)
    sun.data.angle = math.radians(8.)
    point(sun,(.0,0,0))
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.image_settings.quality = 95
    scene.render.resolution_percentage = 100 if not opts.draft else 58
    return sun


def camera(scene, name, position, subject, *, lens=46, width=None):
    data = bpy.data.cameras.new(name)
    data.lens = lens
    if width is not None:
        data.type = "ORTHO"
        data.ortho_scale = width
    obj = bpy.data.objects.new(name,data)
    scene.collection.objects.link(obj)
    obj.location = position
    point(obj,subject)
    return obj


def render(scene, cam, label, size):
    scene.camera = cam
    scene.render.resolution_x, scene.render.resolution_y = size
    scene.render.filepath = str(ROOT/f"{STEM}_{label}.jpg")
    bpy.ops.render.render(write_still=True)


def instance(collection, template, position, yaw, size):
    ob = bpy.data.objects.new(template.name,template.data)
    collection.objects.link(ob)
    ob.location, ob.rotation_euler.z, ob.scale = position, yaw, size
    return ob


def specimen_review(scene, records):
    from build_lowmark_structural_timber import plain
    display = bpy.data.collections.new("Specimen and LOD comparison")
    scene.collection.children.link(display)
    for row, lod in enumerate((0,1,2)):
        for col, family in enumerate(HABITATS):
            x,y = (col-3)*.56,(1-row)*.67
            instance(display,records[family,1][lod],(x,y,0),.65+(col%3)*1.1,(1.,1.,1.))
    bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.016))
    table = bpy.context.object
    table.name = "Neutral specimen stage"
    table.data.materials.append(plain("Matte specimen stage",(.105,.103,.094),.94))
    cam = camera(scene,"Matched LODs",(0,-3.6,4.4),(0,0,.13),width=4.18)
    render(scene,cam,"specimens",(2000,1050))
    for ob in list(display.objects) + [table,cam]:
        bpy.data.objects.remove(ob,do_unlink=True)
    bpy.data.collections.remove(display)


# Fixed planting locations for the farmhouse demonstration. Each tuple describes
# an observed yard feature to dress, with its position, width and mix in metres.
S, M, D, E, R, Y, V = HABITATS
PLANTING = (
    # (along Y, signed verge offset, radii along/across, density, species mix)
    (-.20,  2.15, .56,1.8, 24, ((M,5),(S,3),(R,1))),
    (-.25, -1.89, .48,1.1, 28, ((D,4),(S,4),(R,1))),
    (-1.64,  1.43, .85,.53, 54, ((S,9),(R,2),(M,4),(Y,1))),
    (-2.58,  2.02, 1.2,.65, 34, ((M,11),(S,6),(E,2),(Y,1))),
    (-2.10, -1.83, .99,.57, 55, ((D,11),(M,7),(R,2),(Y,.6))),
    (-2.98, -2.81, 1.1,.86, 39, ((M,8),(D,6),(S,5),(E,3))),
    (-3.34,  1.11, .73,.47, 65, ((S,10),(R,4),(M,2),(V,.7))),
    (-3.36,  2.51, 1.2,.87, 49, ((M,11),(S,4),(E,4),(V,1.4))),
    (-4.60, -1.18, .86,.47, 56, ((S,11),(R,6),(M,7),(Y,1))),
    (-4.71,  1.59, .59,.63, 38, ((S,8),(D,4),(M,7),(R,2))),
    (-5.25, -2.18, 1.6,1.2, 37, ((M,12),(S,5),(D,5),(E,4),(Y,1.1),(V,1.3))),
    (-5.41,  3.53, 1.8,1.6, 33, ((M,9),(D,3),(S,4),(E,4),(Y,.7))),
    (-6.42,  1.22, 1.03,.52, 62, ((S,12),(M,6),(R,3),(V,1.9))),
    (-6.55,  2.24, 1.73,.89, 42, ((M,10),(S,4),(E,5),(V,1.2))),
    (-7.75, -1.55, 1.24,.71, 38, ((S,8),(M,5),(R,2),(D,5))),
    (-8.75, -3.60, 2.4,1.9, 27, ((M,7),(D,7),(S,6),(E,3))),
    (-9.10,  2.62, 2.1,1.3, 22, ((M,8),(S,3),(E,3))),
    (-3.40, -5.40, 3.4,1.8, 29, ((M,6),(D,6),(E,4),(Y,.7))),
    (-3.30,  5.22, 4.1,1.5, 29, ((M,8),(S,4),(V,.7),(E,4))),
    (-5.38,  1.19, .36,.25, 32, ((Y,5),(S,1))),
)


def plant_demo(scene, fixture, soil, records, opts):
    """Place the fixed specimen groups outside the approved soil tread."""
    centers, across, stations, _, bed = fixture
    group = bpy.data.collections.new("Farmhouse review planting")
    scene.collection.children.link(group)
    rng = np.random.default_rng(np.random.SeedSequence((opts.seed,79239)))
    count_by_family = dict.fromkeys(HABITATS,0)
    signature = hashlib.sha256()
    for along, verge, radius_u, radius_v, density, mix in PLANTING:
        count = math.ceil(math.pi*radius_u*radius_v*density*opts.density)
        radius = np.sqrt(rng.uniform(0,1,count))
        phase = rng.uniform(0,TAU,count)
        u = np.interp(along,centers[:,1],stations)+np.cos(phase)*radius*radius_u
        v = verge + np.sin(phase)*radius*radius_v
        path, margin = soil.shoulder(u,v)
        pockets = profile(u/4,v/3,13,11,opts.seed+89,periodic=False)
        taper = 1-.45*radius**2
        allowed = (.25+.60*ramp(.09,.70,pockets)+.26*margin)*taper
        allowed *= (1-path)**2*ramp(.50,1.09,np.abs(v))*ramp(.22,.53,np.abs(v-.03*opts.path_edge))
        allowed *= np.minimum(1.38,1. + opts.path_edge*.60 * margin)
        in_yard = (u<np.interp(-.06,centers[:,1],stations)) & (u>0)
        take = np.flatnonzero(in_yard & (path<.62) & (rng.random(count)<allowed))
        surf = np.column_stack([np.interp(u[take],stations,c) for c in centers.T])
        surf += v[take,None]*np.column_stack([np.interp(u[take],stations,c) for c in across.T])
        height = bed(u[take],v[take])-.003
        for j, index in enumerate(take):
            local_moisture = np.clip(opts.moisture+.42*(pockets[index]-.52),0,1)
            keys, weights = zip(*mix)
            weights = np.array([w * math.exp(-5*(HABITATS[k].moisture-local_moisture)**2)
                                * (1+opts.path_edge*margin[index]*HABITATS[k].verge)
                                for k,w in zip(keys,weights)])
            family = keys[rng.choice(len(keys),p=weights/weights.sum())]
            count_by_family[family] += 1
            stage = rng.choice(3,p=(.26,.57,.17))
            x,y = surf[j]
            # LOD placement is fixed to this one demonstration: the two review
            # cameras both retain the same objects, lighting and physical scale.
            lod = 0 if -7.5<y<-2.1 and abs(v[index])<3.8 else (1 if y>-8.5 else 2)
            size = rng.uniform(.69,1.22)
            stretch = size*rng.uniform(.79,1.16)
            yaw = rng.uniform(0,TAU)
            template = records[family,stage][lod]
            instance(group,template,(x,y,height[j]),yaw,(size,size,stretch))
            signature.update(template.name.encode())
            signature.update(struct.pack("<6f",x,y,height[j],size,stretch,yaw))
    print(f"Fixed farmhouse layout {count_by_family} | {signature.hexdigest()}",flush=True)
    return group


def farmhouse_review(scene, sun, records, opts):
    from build_lowmark_packed_earth import Soil, material, review_ground
    from build_lowmark_lime_plaster import build_farmhouse, make_materials, set_material
    from build_lowmark_planked_oak import orient_and_phase
    from build_lowmark_handcrafted_glass import fit_windows, DrawnGlass, optical_material

    plaster = build_farmhouse(scene)
    lime = make_materials()["Maintained"]
    for obj in plaster:
        set_material(obj,lime)
    with bpy.data.libraries.load(str(ROOT/"Lowmark_Planked_Oak_Joinery.blend")) as (_, loaded):
        loaded.materials = ["Lowmark Planked Oak | Wood Weathered"]
    oak, = loaded.materials
    with bpy.data.libraries.load(str(ROOT/"Lowmark_Forged_Iron_Hardware.blend")) as (_, loaded):
        loaded.materials = ["Lowmark Forged Iron | Weathered"]
    iron, = loaded.materials
    for obj in tuple(scene.objects):
        if obj.type=="MESH" and obj.name.startswith(("facade_doors","facade_shutters")):
            orient_and_phase(obj)
            set_material(obj,oak)
        elif obj.type=="MESH" and obj.name.startswith("facade_iron"):
            set_material(obj,iron)
    fit_windows(scene,DrawnGlass(70931,1.),optical_material("Lightly_Weathered"),opts.draft)
    ground_soil = Soil(81379,.82,.91,.56,.60,.77,.80)
    y = np.linspace(-18.,11.8,470)
    x = 3.79+.98*(1-np.cos(.28*np.maximum(-y-.38,0)))
    _, fixture = review_ground("Approved packed earth and worn approach",np.column_stack((x,y)),8.7,
                               ground_soil,material("Transition"),landing=True)
    planting = plant_demo(scene,fixture,ground_soil,records,opts)
    sun.rotation_euler = (.53,-.49,-.37)
    approach = camera(scene,"Gameplay-distance approach",(7.65,-10.67,2.51),(4.20,-.95,1.01),lens=34)
    close = camera(scene,"Verge close-up",(3.37,-7.01,.86),(3.00,-4.89,.11),lens=40)
    scene.camera = approach
    scene.render.resolution_x,scene.render.resolution_y = (1700,1080)
    scene.render.filepath = "//"+STEM+"_farmhouse.jpg"
    # Preserve a ready-to-open editable scene with both Cameras and the
    # linked-instance plant meshes. The atlas is beside the scene.
    if not opts.draft:
        bpy.context.preferences.filepaths.save_version = 0
        bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/f"{STEM}_Farmhouse.blend"),compress=True,relative_remap=True)
    render(scene,approach,"farmhouse",(1700,1080))
    render(scene,close,"verge",(1700,1050))
    planting.hide_render = True
    render(scene,close,"verge_bare",(1700,1050))
    planting.hide_render = False


def main():
    cli = ArgumentParser()
    cli.add_argument("--seed",type=int,default=SEED)
    cli.add_argument("--density",type=float,default=1.)
    cli.add_argument("--height",type=float,default=1.)
    cli.add_argument("--moisture",type=float,default=.56)
    cli.add_argument("--path-edge",type=float,default=.74)
    cli.add_argument("--assets-only",action="store_true")
    cli.add_argument("--draft",action="store_true")
    cli.add_argument("--optix",action="store_true")
    cli.add_argument("--verify-repeat",action="store_true")
    opts = cli.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    if not (opts.seed>=0 and .65<=opts.density<=1.35 and .72<=opts.height<=1.35
            and 0<=opts.moisture<=1 and 0<=opts.path_edge<=1):
        cli.error("Use a nonnegative seed, density .65–1.35, height .72–1.35 and moisture/path edge 0–1.")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    maps = atlas_maps()
    if opts.verify_repeat:
        for key, array in atlas_maps().items():
            np.testing.assert_array_equal(maps[key],array,err_msg=key)
    write_maps(scene,maps)
    mat = foliage_material()
    check_atlas(maps,mat)
    del maps
    collection, records = library(scene,mat,opts)
    if not opts.draft:
        path = ROOT/f"{STEM}.blend"
        bpy.data.libraries.write(str(path),{collection},path_remap="RELATIVE_ALL",fake_user=True,compress=True)
        path = ROOT/f"{STEM}.glb"
        bpy.ops.export_scene.gltf(filepath=str(path),export_format="GLB",export_extras=True,
                                  export_yup=True,export_cameras=False,export_lights=False,
                                  export_hierarchy_full_collections=True,export_tangents=True)
        check_glb(path,records)
    if opts.verify_repeat:
        print("Independent generation matched for all 63 source meshes and three atlases",flush=True)
    if not opts.assets_only:
        scene.collection.children.unlink(collection)
        sun = setup_review(scene,opts)
        specimen_review(scene,records)
        farmhouse_review(scene,sun,records,opts)


if __name__ == "__main__":
    main()
