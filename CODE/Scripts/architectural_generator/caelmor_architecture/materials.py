"""Muted Lowmark materials and original, periodic micro-surface images."""
import math

PALETTE = {
    "stone": ((.31,.29,.25,1),.88,0), "stone_light": ((.48,.44,.37,1),.86,0),
    "plaster": ((.66,.59,.47,1),.92,0), "plaster_patch": ((.53,.47,.38,1),.94,0),
    "timber": ((.18,.105,.055,1),.82,0), "timber_light": ((.31,.21,.12,1),.78,0),
    "roof": ((.105,.12,.115,1),.9,0), "roof_patch": ((.16,.17,.15,1),.92,0),
    "iron": ((.09,.105,.10,1),.52,.55), "glass": ((.16,.25,.26,1),.22,.08),
    "mortar": ((.39,.35,.29,1),.97,0),
}

SIZE = 128
FAMILIES = {"timber": "wood", "timber_light": "wood", "roof": "roof",
            "roof_patch": "roof", "stone": "stone", "stone_light": "stone",
            "mortar": "stone", "plaster": "plaster", "plaster_patch": "plaster"}


def _periodic_height(family, u, v):
    tau = math.tau
    if family == "wood":
        grain = math.sin(tau * (13 * v + .04 * math.sin(tau * 3 * u) + .012 * math.sin(tau * 9 * u)))
        fine = math.sin(tau * (31 * v + .02 * math.sin(tau * 5 * u)))
        return .72 * grain + .20 * fine + .08 * math.sin(tau * (2*u + 3*v))
    if family == "roof":
        return (.56 * math.sin(tau * 11 * u) * math.sin(tau * 7 * v)
                + .28 * math.cos(tau * 19 * u + tau * 3 * v)
                + .16 * math.sin(tau * 29 * v))
    if family == "stone":
        return (.44 * math.sin(tau * 5 * u) * math.cos(tau * 7 * v)
                + .33 * math.sin(tau * 13 * u + tau * 11 * v)
                + .23 * math.cos(tau * 23 * u - tau * 17 * v))
    return (.42 * math.sin(tau * 17 * u) * math.cos(tau * 13 * v)
            + .34 * math.sin(tau * 29 * u + tau * 23 * v)
            + .24 * math.cos(tau * 37 * u - tau * 31 * v))


def _srgb(value):
    value = max(0.0, min(1.0, value))
    return 12.92 * value if value <= .0031308 else 1.055 * value ** (1/2.4) - .055


def _images(family, base):
    import bpy
    base_name = f"Caelmor Original {family.title()} Tile"
    normal_name = f"Caelmor Original {family.title()} Normal"
    color = bpy.data.images.get(base_name)
    normal = bpy.data.images.get(normal_name)
    if color is not None and normal is not None:
        return color, normal
    color = bpy.data.images.new(base_name, width=SIZE, height=SIZE, alpha=True, float_buffer=False)
    normal = bpy.data.images.new(normal_name, width=SIZE, height=SIZE, alpha=True, float_buffer=False)
    color.colorspace_settings.name = 'sRGB'
    normal.colorspace_settings.name = 'Non-Color'
    h = [[_periodic_height(family, x/SIZE, y/SIZE) for x in range(SIZE)] for y in range(SIZE)]
    pixels = [0.0] * (SIZE * SIZE * 4)
    normal_pixels = [0.0] * (SIZE * SIZE * 4)
    relief = {"wood": .00075, "roof": .00035, "stone": .00165, "plaster": .00045}[family]
    for y in range(SIZE):
        ym, yp = (y-1) % SIZE, (y+1) % SIZE
        for x in range(SIZE):
            xm, xp = (x-1) % SIZE, (x+1) % SIZE
            i = (y * SIZE + x) * 4
            height = h[y][x]
            # Preserve the palette hue, adding restrained natural color variation.
            variation = .97 + .025 * height + .008 * math.sin(math.tau * (7*x/SIZE + 5*y/SIZE))
            pixels[i:i+4] = [_srgb(variation)] * 3 + [1.0]
            du = (h[y][xp] - h[y][xm]) * .5 * SIZE * relief
            dv = (h[yp][x] - h[ym][x]) * .5 * SIZE * relief
            nx, ny, nz = -du, -dv, 1.0
            inv = 1.0 / math.sqrt(nx*nx + ny*ny + nz*nz)
            normal_pixels[i:i+4] = [nx*inv*.5+.5, ny*inv*.5+.5, nz*inv*.5+.5, 1.0]
    color.pixels.foreach_set(pixels)
    normal.pixels.foreach_set(normal_pixels)
    color.pack(); normal.pack()
    color["caelm_original"] = True; normal["caelm_original"] = True
    return color, normal


def _configure_new_material(mat, key, base, roughness, metallic):
    family = FAMILIES.get(key)
    mat.diffuse_color = base
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    shader = next((node for node in nodes if node.type == 'BSDF_PRINCIPLED'), None)
    if shader is None: shader = nodes.new('ShaderNodeBsdfPrincipled')
    shader.inputs['Base Color'].default_value = base
    shader.inputs['Roughness'].default_value = roughness
    shader.inputs['Metallic'].default_value = metallic
    mat["caelm_material"] = key
    mat["caelm_palette"] = "Lowmark muted PBR"
    if family is None:
        return
    color_image, normal_image = _images(family, base)
    uv = nodes.new('ShaderNodeUVMap'); uv.uv_map = "UV0_Metric"; uv.label = "Metric UV0"
    color_tex = nodes.new('ShaderNodeTexImage'); color_tex.image = color_image
    color_tex.extension = 'REPEAT'; color_tex.label = "Caelmor tileable base color"
    tint = nodes.new('ShaderNodeMixRGB'); tint.blend_type = 'MULTIPLY'
    tint.inputs['Fac'].default_value = 1.0
    tint.inputs['Color1'].default_value = base
    tint.label = "Palette tint × original surface variation"
    normal_tex = nodes.new('ShaderNodeTexImage'); normal_tex.image = normal_image
    normal_tex.extension = 'REPEAT'; normal_tex.label = "Caelmor tangent normal"
    normal_tex.image.colorspace_settings.name = 'Non-Color'
    normal_node = nodes.new('ShaderNodeNormalMap'); normal_node.space = 'TANGENT'; normal_node.inputs['Strength'].default_value = .32
    links.new(uv.outputs['UV'], color_tex.inputs['Vector'])
    links.new(color_tex.outputs['Color'], tint.inputs['Color2'])
    links.new(tint.outputs['Color'], shader.inputs['Base Color'])
    links.new(uv.outputs['UV'], normal_tex.inputs['Vector'])
    links.new(normal_tex.outputs['Color'], normal_node.inputs['Color'])
    links.new(normal_node.outputs['Normal'], shader.inputs['Normal'])
    mat["caelm_texture_family"] = family


def get_material(name, cache=None):
    """Return shared Principled material; preserve an existing user's edits."""
    import bpy
    key = name if name in PALETTE else "timber"
    if cache is not None and key in cache:
        return cache[key]
    mat_name = "Caelmor | " + key.replace("_", " ").title()
    mat = bpy.data.materials.get(mat_name)
    is_new = mat is None
    if is_new:
        mat = bpy.data.materials.new(mat_name)
        _configure_new_material(mat, key, *PALETTE[key])
    if cache is not None:
        cache[key] = mat
    return mat
