"""Legacy pilot fixtures using the shared relief cage."""
import math

import bpy
import numpy as np

from caelmor_architecture.relief_cage import cage

FIELD_UV = 'UV2_Surface'
MAX_TRIANGLES = 300_000


def height_image(material, craft, weather):
    """Recover the original metres-valued relief behind a Caelmor normal map."""
    from caelmor_architecture.construction_relief import field_maps
    family = material['caelm_shared_field']
    name = f'Caelmor Height {family} {craft} {weather:.2f}'
    if name not in bpy.data.images:
        *_, height = field_maps(family, craft, weather, (.5, .5, .5), include_height=True)
        size = height.shape[0]
        image = bpy.data.images.new(name, size, size, alpha=False, float_buffer=True)
        image.colorspace_settings.name = 'Non-Color'
        rgba = np.ones((size, size, 4), dtype=np.float32)
        rgba[:, :, :3] = height[:, :, None] / .04
        image.pixels.foreach_set(rgba.ravel())
        image.file_format = 'OPEN_EXR'
        image.pack()
    return bpy.data.images[name]


def install(obj, image, *, strength=.025, levels=1, uv=FIELD_UV, repeat=True):
    """Build an editable cage and native modifiers on a generated field only."""
    if obj.type != 'MESH' or not obj.get('caelm_field_family') or obj.get('caelm_collider'):
        raise ValueError('Select a mapped roof or masonry construction field.')
    if obj.get('caelm_protected') or obj.modifiers or obj.vertex_groups:
        raise ValueError('Material relief cannot replace protected geometry, vertex groups or an existing modifier stack.')
    if image.colorspace_settings.name != 'Non-Color' or uv not in obj.data.uv_layers:
        raise ValueError('Use a Non-Color height image and an existing UV layer shared with the material.')
    if not math.isfinite(strength) or not 0 < strength <= .04 or levels not in (0, 1, 2):
        raise ValueError('Choose strength above zero and up to 0.04 m and subdivision level 0–2.')
    source = obj.data
    mesh, weights = cage(source)
    triangles = (sum(len(face.vertices) for face in mesh.polygons) * 2 * 4 ** (levels - 1)
                 if levels else sum(len(face.vertices) - 2 for face in mesh.polygons))
    if triangles > MAX_TRIANGLES:
        bpy.data.meshes.remove(mesh)
        raise ValueError(f'The requested subdivision exceeds {MAX_TRIANGLES:,} triangles on this field. Lower the resolution.')
    obj.data = mesh
    original_name = source.name
    source.name += ' (undisplaced input)'
    source.use_fake_user = True
    mesh.name = original_name
    mask = obj.vertex_groups.new(name='Caelmor Relief Interior')
    for i, weight in enumerate(weights):
        if weight > 0:
            mask.add([i], float(weight), 'REPLACE')
    subdivide = obj.modifiers.new('Caelmor Relief Sampling', 'SUBSURF')
    subdivide.subdivision_type = 'SIMPLE'
    subdivide.levels = subdivide.render_levels = levels
    subdivide.uv_smooth = 'NONE'
    displacement = obj.modifiers.new('Caelmor Material Height', 'DISPLACE')
    texture = bpy.data.textures.new(image.name, type='IMAGE')
    texture.image = image
    texture.extension = 'REPEAT' if repeat else 'EXTEND'
    displacement.texture = texture
    displacement.texture_coords = 'UV'
    displacement.uv_layer = uv
    displacement.direction = 'NORMAL'
    displacement.vertex_group = mask.name
    displacement.mid_level = 0.
    displacement.strength = strength
    return source
