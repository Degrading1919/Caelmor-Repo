"""Muted Lowmark materials with deterministic, tileable procedural surface maps."""
import math

PALETTE = {
    "stone": ((.31,.29,.25,1),.88,0), "stone_light": ((.48,.44,.37,1),.86,0),
    "plaster": ((.66,.59,.47,1),.92,0), "plaster_patch": ((.53,.47,.38,1),.94,0),
    "timber": ((.18,.105,.055,1),.82,0), "timber_light": ((.31,.21,.12,1),.78,0),
    "roof": ((.105,.12,.115,1),.9,0), "roof_dark": ((.085,.098,.095,1),.94,0),
    "roof_worn": ((.117,.125,.116,1),.94,0), "roof_patch": ((.12,.125,.112,1),.94,0),
    "iron": ((.09,.105,.10,1),.52,.55), "glass": ((.16,.25,.26,1),.22,.08),
    "mortar": ((.39,.35,.29,1),.97,0),
}

SIZE = 128
SURFACE_REVISION = 2
FAMILIES = {
    "timber": "wood", "timber_light": "wood",
    "roof": "roof", "roof_dark": "roof", "roof_worn": "roof", "roof_patch": "roof",
    "stone": "stone", "stone_light": "stone", "mortar": "stone",
    "plaster": "plaster", "plaster_patch": "plaster",
}


def _fade(t):
    return t * t * (3.0 - 2.0 * t)


def _hash2(ix, iy, seed=0):
    """Stable scalar hash; integer lattice coordinates wrap for seamless tiles."""
    n = (ix * 374761393 + iy * 668265263 + seed * 1442695041) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    n ^= n >> 16
    return n / 2147483647.5 - 1.0


def _noise(u, v, cells_u, cells_v, seed=0):
    """Periodic, smooth value noise in [-1, 1], with exact integer tile periods."""
    x, y = (u % 1.0) * cells_u, (v % 1.0) * cells_v
    ix, iy = math.floor(x), math.floor(y)
    fx, fy = _fade(x - ix), _fade(y - iy)
    x0, x1 = ix % cells_u, (ix + 1) % cells_u
    y0, y1 = iy % cells_v, (iy + 1) % cells_v
    a = _hash2(x0, y0, seed) * (1.0 - fx) + _hash2(x1, y0, seed) * fx
    b = _hash2(x0, y1, seed) * (1.0 - fx) + _hash2(x1, y1, seed) * fx
    return a * (1.0 - fy) + b * fy


def _fbm(u, v, seed=0):
    return (.56 * _noise(u,v,4,4,seed) + .29 * _noise(u,v,8,8,seed+1)
            + .15 * _noise(u,v,16,16,seed+2))


def _wood_height(u, v):
    # UV0 follows each board's long axis: narrow warped ridges run down the grain.
    warp = .014 * _noise(u, v, 5, 3, 11) + .006 * _noise(u, v, 11, 7, 12)
    crossgrain = v + warp
    broad = _noise(u, crossgrain, 5, 13, 21)
    fine = _noise(u, crossgrain, 9, 29, 22)
    ridges = math.sin(math.tau * (19.0 * crossgrain + .8 * broad))
    height = .43 * ridges + .24 * broad + .13 * fine + .10 * _noise(u,v,4,5,23)
    # Two subtle, periodic knots per tile. Their elongated rings disturb the grain,
    # while a dark centre and short checks keep the board from reading as plastic.
    for ku, kv, seed in ((.27,.31,31),(.73,.76,32)):
        du = min(abs((u-ku+.5)%1.0-.5), .5)
        dv = min(abs((v-kv+.5)%1.0-.5), .5)
        rx, ry = du/.115, dv/.047
        r = math.sqrt(rx*rx + ry*ry)
        if r < 3.4:
            envelope = max(0.0, 1.0-r/3.4)
            rings = math.cos(math.tau * r * 1.22 + .3 * _noise(u,v,8,8,seed))
            height += .11 * envelope * rings - .10 * math.exp(-r*r*2.1)
            # Fine splits emerge from each knot and remain aligned with the grain.
            check = max(0.0, 1.0-abs(dv - .004*math.sin(du*120.0))/.0018)
            if du < .09:
                height -= .075 * check * envelope
    return height


def _periodic_height(family, u, v):
    if family == "wood":
        return _wood_height(u, v)
    if family == "roof":
        # Irregular split shingles: broad mineral weathering with fine broken grain.
        seam = math.sin(math.tau * (8.0*v + .18*_noise(u,v,5,4,41)))
        course = math.sin(math.tau * (7.0*u + .35*_noise(u,v,4,6,42)))
        return .42*_fbm(u,v,43) + .25*_noise(u,v,13,11,44) + .20*seam*course + .13*_noise(u,v,27,23,45)
    if family == "stone":
        return .52*_fbm(u,v,51) + .31*_noise(u,v,11,9,52) + .17*_noise(u,v,25,21,53)
    # Limewash with restrained aggregate flecks, soft trowel variation and pitting.
    aggregate = _noise(u,v,25,23,61)
    pits = _noise(u,v,39,37,62)
    return .55*_fbm(u,v,63) + .24*_noise(u,v,11,8,64) + .13*aggregate + .08*pits


def _srgb(value):
    value = max(0.0, min(1.0, value))
    return 12.92 * value if value <= .0031308 else 1.055 * value ** (1/2.4) - .055


def _images(family, base):
    import bpy
    root = f"Caelmor Original {family.title()} Surface{SURFACE_REVISION}"
    color = bpy.data.images.get(root + " Color")
    normal = bpy.data.images.get(root + " Normal")
    roughness = bpy.data.images.get(root + " Roughness")
    if color is not None and normal is not None and roughness is not None:
        return color, normal, roughness
    color = bpy.data.images.new(root + " Color", width=SIZE, height=SIZE, alpha=True, float_buffer=False)
    normal = bpy.data.images.new(root + " Normal", width=SIZE, height=SIZE, alpha=True, float_buffer=False)
    roughness = bpy.data.images.new(root + " Roughness", width=SIZE, height=SIZE, alpha=True, float_buffer=False)
    color.colorspace_settings.name = 'sRGB'
    normal.colorspace_settings.name = 'Non-Color'
    roughness.colorspace_settings.name = 'Non-Color'
    h = [[_periodic_height(family, x/SIZE, y/SIZE) for x in range(SIZE)] for y in range(SIZE)]
    pixels = [0.0] * (SIZE * SIZE * 4)
    normal_pixels = [0.0] * (SIZE * SIZE * 4)
    rough_pixels = [0.0] * (SIZE * SIZE * 4)
    relief = {"wood": .0011, "roof": .00055, "stone": .0021, "plaster": .00085}[family]
    rough_base = {"wood": .84, "roof": .92, "stone": .90, "plaster": .94}[family]
    for y in range(SIZE):
        ym, yp = (y-1) % SIZE, (y+1) % SIZE
        for x in range(SIZE):
            xm, xp = (x-1) % SIZE, (x+1) % SIZE
            i = (y * SIZE + x) * 4
            height = h[y][x]
            # Family-specific albedo range keeps limewash and stone visibly mineral
            # without pushing the restrained wood and roof surfaces into noisy contrast.
            u, v = x/SIZE, y/SIZE
            albedo_amp = {"wood":.12, "roof":.13, "stone":.23, "plaster":.25}[family]
            cloud_amp = {"wood":.010, "roof":.012, "stone":.045, "plaster":.055}[family]
            cloud = _noise(u, v, 2, 2, 75) if family in ("stone", "plaster") else 0.0
            fine = _noise(u, v, 7, 7, 71)
            variation = max(.72, min(1.08, .97 + albedo_amp*height + cloud_amp*cloud + .012*fine))
            pixels[i:i+4] = [_srgb(variation)] * 3 + [1.0]
            du = (h[y][xp] - h[y][xm]) * .5 * SIZE * relief
            dv = (h[yp][x] - h[ym][x]) * .5 * SIZE * relief
            nx, ny, nz = -du, -dv, 1.0
            inv = 1.0 / math.sqrt(nx*nx + ny*ny + nz*nz)
            normal_pixels[i:i+4] = [nx*inv*.5+.5, ny*inv*.5+.5, nz*inv*.5+.5, 1.0]
            rough = max(.68, min(.99, rough_base + .035*_fbm(x/SIZE,y/SIZE,73) + .014*height))
            rough_pixels[i:i+4] = [rough, rough, rough, 1.0]
    color.pixels.foreach_set(pixels)
    normal.pixels.foreach_set(normal_pixels)
    roughness.pixels.foreach_set(rough_pixels)
    color.pack(); normal.pack(); roughness.pack()
    for image in (color, normal, roughness):
        image["caelm_original"] = True
        image["caelm_surface_revision"] = SURFACE_REVISION
    return color, normal, roughness


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
    color_image, normal_image, rough_image = _images(family, base)
    uv = nodes.new('ShaderNodeUVMap'); uv.uv_map = "UV0_Metric"; uv.label = "Metric UV0"
    color_tex = nodes.new('ShaderNodeTexImage'); color_tex.image = color_image
    color_tex.extension = 'REPEAT'; color_tex.label = "Caelmor tileable albedo variation"
    tint = nodes.new('ShaderNodeMix'); tint.data_type = 'RGBA'; tint.blend_type = 'MULTIPLY'
    tint.inputs['Factor'].default_value = 1.0
    tint.inputs['A'].default_value = base
    tint.label = "Palette × original surface variation"
    vertex = nodes.new('ShaderNodeVertexColor'); vertex.layer_name = "CaelmorTint"
    vertex.label = "Exported building weathering (COLOR_0)"
    vertex_mix = nodes.new('ShaderNodeMix'); vertex_mix.data_type = 'RGBA'; vertex_mix.blend_type = 'MULTIPLY'
    vertex_mix.inputs['Factor'].default_value = 1.0
    vertex_mix.label = "Surface weathering tint"
    normal_tex = nodes.new('ShaderNodeTexImage'); normal_tex.image = normal_image
    normal_tex.extension = 'REPEAT'; normal_tex.label = "Caelmor tangent normal"
    normal_tex.image.colorspace_settings.name = 'Non-Color'
    normal_node = nodes.new('ShaderNodeNormalMap'); normal_node.space = 'TANGENT'; normal_node.inputs['Strength'].default_value = .32
    rough_tex = nodes.new('ShaderNodeTexImage'); rough_tex.image = rough_image
    rough_tex.extension = 'REPEAT'; rough_tex.label = "Caelmor roughness variation"
    rough_tex.image.colorspace_settings.name = 'Non-Color'
    links.new(uv.outputs['UV'], color_tex.inputs['Vector'])
    links.new(color_tex.outputs['Color'], tint.inputs['B'])
    links.new(tint.outputs['Result'], vertex_mix.inputs['A'])
    links.new(vertex.outputs['Color'], vertex_mix.inputs['B'])
    links.new(vertex_mix.outputs['Result'], shader.inputs['Base Color'])
    links.new(uv.outputs['UV'], normal_tex.inputs['Vector'])
    links.new(normal_tex.outputs['Color'], normal_node.inputs['Color'])
    links.new(normal_node.outputs['Normal'], shader.inputs['Normal'])
    links.new(uv.outputs['UV'], rough_tex.inputs['Vector'])
    links.new(rough_tex.outputs['Color'], shader.inputs['Roughness'])
    mat["caelm_texture_family"] = family


def get_material(name, cache=None):
    """Return current shared material without replacing edits or legacy datablocks."""
    import bpy
    key = name if name in PALETTE else "timber"
    if cache is not None and key in cache:
        return cache[key]
    base_name = "Caelmor | " + key.replace("_", " ").title()
    # Reuse by semantic key + surface revision first, even if the user renamed it.
    mat = next((candidate for candidate in bpy.data.materials
                if candidate.get("caelm_material") == key
                and candidate.get("caelm_surface_revision") == SURFACE_REVISION), None)
    if mat is None:
        legacy = bpy.data.materials.get(base_name)
        # Keep an existing pre-revision material and every manual edit intact.
        # New scenes retain friendly names; legacy scenes get an explicit revision suffix.
        mat_name = base_name if legacy is None else f"{base_name} [Surface{SURFACE_REVISION}]"
        suffix = 2
        while bpy.data.materials.get(mat_name) is not None:
            mat_name = f"{base_name} [Surface{SURFACE_REVISION}.{suffix}]"
            suffix += 1
        mat = bpy.data.materials.new(mat_name)
        _configure_new_material(mat, key, *PALETTE[key])
        mat["caelm_surface_revision"] = SURFACE_REVISION
    if cache is not None:
        cache[key] = mat
    return mat


def _smoothstep(edge0, edge1, value):
    t = max(0.0, min(1.0, (value-edge0) / max(edge1-edge0, 1e-9)))
    return t*t*(3.0-2.0*t)


def _sill_runoff(position, normal, plan):
    """Return a small deterministic wall stain directly below known openings."""
    if plan is None or abs(normal[2]) > .38 or math.hypot(normal[0],normal[1]) < .45:
        return 0.0
    try:
        from .facade import _openings_for_edge, _edge_frame
        strongest = 0.0
        for edge_index, edge in enumerate(plan.edges):
            a, b, tx, ty, outward, length = _edge_frame(plan, edge_index, edge)
            # Only the exterior face receives rain streaks.
            if normal[0]*outward[0] + normal[1]*outward[1] < .35:
                continue
            along = (position[0]-a[0])*tx + (position[1]-a[1])*ty
            across = (position[0]-a[0])*outward[0] + (position[1]-a[1])*outward[1]
            if across < -.08 or across > .42 or not 0.0 <= along <= length:
                continue
            for opening in _openings_for_edge(plan, edge_index, edge):
                if opening["kind"] not in ("window", "vent"):
                    continue
                center = (opening["s0"] + opening["s1"]) * .5
                sill = opening["z0"]
                dx = abs(along-center)
                down = sill-position[2]
                # Wall meshes are deliberately coarse between openings. A broad,
                # soft mask at sill corners interpolates into a narrow central drip.
                if -.02 <= down <= .72 and dx <= .48 + .08*down:
                    taper = (1.0-_smoothstep(.48,.74,down)) * (1.0-_smoothstep(.38+.025*down,.62+.04*down,dx))
                    # Subtle irregular edge avoids a graphic, perfectly uniform stripe.
                    irregular = .82 + .18*_noise(position[0]*.37,position[1]*.37,7,7,81)
                    strongest = max(strongest, taper*irregular)
        return strongest
    except (AttributeError, TypeError, ValueError):
        return 0.0


def surface_tint(position, normal, material, plan=None):
    """Bounded linear-RGB multiplier for baked per-corner environmental weathering.

    This helper has no Blender dependency, so masks can be inspected or unit-tested
    against the pure geometry plan. Position and normal are local metre coordinates.
    """
    key = str(material).lower()
    x,y,z = (float(v) for v in position)
    nx,ny,nz = (float(v) for v in normal)
    nlen = math.sqrt(nx*nx+ny*ny+nz*nz) or 1.0
    nx,ny,nz = nx/nlen,ny/nlen,nz/nlen
    factor = 1.0
    is_masonry = key in {"stone","stone_light","mortar","plaster","plaster_patch"}
    is_roof = key.startswith("roof") or key == "timber" and z > (getattr(plan,"eave",2.8)-.2)
    if is_masonry:
        damp = (1.0-_smoothstep(.10,.62,z)) * max(0.0, min(1.0, abs(nz)*.25 + .75))
        factor *= 1.0 - .14*damp
        factor *= 1.0 - .105*_sill_runoff((x,y,z),(nx,ny,nz),plan)
        if plan is not None and abs(nz) < .38:
            # Broad, sheltered-wall discoloration starts at the eaves and fades
            # downward over about a metre, with no isolated random blotches.
            eave = float(getattr(plan,"eave",z))
            below_eave = eave-z
            eave_band = _smoothstep(-.04,.05,below_eave) * (1.0-_smoothstep(.42,1.15,below_eave))
            eave_variation = .94 + .06*_noise(x*.31,y*.31,3,3,83)
            factor *= 1.0 - .095*eave_band*eave_variation
    # Orientation-weighted sun and wind exposure gently lifts exposed upper surfaces.
    toward_sun = max(0.0, nx*(-.48) + ny*(-.38) + nz*.79)
    elevation = _smoothstep(.55,1.4,z)
    exposure = toward_sun * elevation
    if is_masonry or is_roof or key.startswith("timber"):
        factor *= 1.0 + .045*exposure
    # Chimney soot is localized to the roof surrounding the known domestic stack.
    if is_roof and plan is not None and str(getattr(getattr(plan,"settings",None),"function","")).upper() in ("FARMHOUSE","MILLER","INN"):
        rect = max(plan.rects, key=lambda r:(r[2]-r[0])*(r[3]-r[1]))
        x0,y0,x1,y1,_axis = rect
        cx,cy = x0+(x1-x0)*.78, y0+(y1-y0)*.76
        distance = math.hypot(x-cx,y-cy)
        soot = (1.0-_smoothstep(.28,1.65,distance)) * _smoothstep(plan.eave-.25,plan.eave+.2,z)
        factor *= 1.0 - .11*soot
    # glTF COLOR_0 is normalized [0, 1]. Clamp here so Blender preview and
    # exported vertex data use the same standards-valid weathering values.
    factor = max(0.0, min(1.0, factor))
    return (factor, factor, factor, 1.0)
