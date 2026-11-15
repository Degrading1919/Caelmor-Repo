"""Resolve explicit material height and apply it to an authored surface field."""
from dataclasses import dataclass
from pathlib import Path
import math
import re

import bpy
from mathutils import Matrix, Vector
import numpy as np

from .relief_cage import GRID, cage

HEIGHT_IMAGE = 'caelm_height_image'
HEIGHT_SPAN = 'caelm_height_span'
HEIGHT_NEUTRAL = 'caelm_height_neutral'
HEIGHT_UV = 'CaelmorHeightUV'
MAX_TRIANGLES = 300_000
MAX_STRENGTH = .035


@dataclass
class Height:
    image: object
    uv: str
    transform: Matrix
    extension: str
    span: float
    neutral: float


def _upstream(socket):
    while socket and socket.is_linked:
        connection = socket.links[0]
        if connection.from_node.type != 'REROUTE':
            return connection.from_node, connection.from_socket
        socket = connection.from_node.inputs[0]
    return None, None


def _coordinates(texture, mesh):
    node, socket = _upstream(texture.inputs['Vector'])
    result = Matrix.Identity(3)
    while node and node.type == 'MAPPING':
        if node.vector_type != 'POINT' or any(node.inputs[n].is_linked for n in ('Location','Rotation','Scale')):
            raise ValueError('Height requires a constant UV mapping transform.')
        translation, rotation, scale = (node.inputs[n].default_value for n in ('Location','Rotation','Scale'))
        if (abs(rotation.x) + abs(rotation.y) > 1e-6
                or not all(math.isfinite(x) for x in (*translation, *rotation, *scale))
                or min(scale.x, scale.y) <= 0):
            raise ValueError('Height requires a planar, positively scaled UV transform.')
        c,s = math.cos(rotation.z),math.sin(rotation.z)
        result = result @ Matrix(((c*scale.x,-s*scale.y,translation.x),
                                  (s*scale.x,c*scale.y,translation.y),(0.,0.,1.)))
        node, socket = _upstream(node.inputs['Vector'])
    if node and not (node.type == 'UVMAP' or node.type == 'TEX_COORD' and socket.name == 'UV'):
        raise ValueError('Height requires image textures driven by UV coordinates.')
    render = next((layer.name for layer in mesh.uv_layers if layer.active_render), '')
    uv = (node.uv_map if node and node.type=='UVMAP' else '') or render
    if uv not in mesh.uv_layers:
        raise ValueError(f'Material refers to missing UV layer {uv!r}.')
    if texture.extension not in ('REPEAT','EXTEND'):
        raise ValueError('Height supports repeating or edge-clamped images.')
    return uv, result, texture.extension


def _image_node(socket):
    node, output = _upstream(socket)
    while node and node.type in ('NORMAL_MAP','SEPARATE_COLOR','SEPRGB'):
        node, output = _upstream(node.inputs[0] if node.type!='NORMAL_MAP' else node.inputs['Color'])
    return node if node and node.type=='TEX_IMAGE' and output.name=='Color' else None


def _companion(source):
    """Recognize a sibling height export with the same authored texture stem."""
    if source is None or not source.filepath:
        return None
    path = Path(bpy.path.abspath(source.filepath, library=source.library))
    prefix = re.sub(r'[_ .-](base_?color|albedo|color)$', '', path.stem, flags=re.I)
    if prefix == path.stem or not path.is_absolute():
        return None
    suffixes = {'.png','.exr','.tga','.tif','.tiff','.bmp'}
    names = {prefix.lower() + '_' + key for key in ('height','displace','displacement')}
    def matches(candidate):
        return candidate.parent==path.parent and candidate.stem.lower() in names and candidate.suffix.lower() in suffixes
    loaded = {Path(bpy.path.abspath(im.filepath,library=im.library)): im for im in bpy.data.images
              if im.filepath and im.packed_file
              and matches(Path(bpy.path.abspath(im.filepath,library=im.library)))
              and im.colorspace_settings.name=='Non-Color'}
    paths = set(loaded)
    if path.parent.is_dir():
        paths.update(candidate for candidate in path.parent.iterdir() if candidate.is_file() and matches(candidate))
    if len(paths)>1:
        raise ValueError('Multiple companion height images. Pick one in Materials.')
    if not paths:
        return None
    path = next(iter(paths))
    if path in loaded:
        return loaded[path]
    existing = next((im for im in bpy.data.images if im.filepath
                     and bpy.path.abspath(im.filepath, library=im.library) == str(path)
                     and im.colorspace_settings.name=='Non-Color'), None)
    if existing:
        return existing
    image = bpy.data.images.load(str(path), check_existing=False)
    image.colorspace_settings.name = 'Non-Color'
    return image


def resolve(material, mesh):
    if not material or not material.use_nodes or not material.node_tree:
        return None
    nodes = material.node_tree.nodes
    output = next((n for n in nodes if n.type=='OUTPUT_MATERIAL' and n.is_active_output), None)
    if output is None:
        return None
    shader, _ = _upstream(output.inputs['Surface'])
    color = _image_node(shader.inputs['Base Color']) if shader and shader.type=='BSDF_PRINCIPLED' else None
    displacement, _ = _upstream(output.inputs['Displacement'])
    if displacement and material.displacement_method != 'BUMP':
        raise ValueError('Use Bump Only in the shader before enabling modifier relief, to avoid applying height twice.')
    chosen = getattr(material,HEIGHT_IMAGE,None) or material.get(HEIGHT_IMAGE)
    height = None
    if displacement and chosen is None:
        if (displacement.type!='DISPLACEMENT' or displacement.space!='OBJECT'
                or any(displacement.inputs[key].is_linked for key in ('Midlevel','Scale','Normal'))):
            raise ValueError('Use an object-space Displacement node with constant scale and midlevel, or select a height image.')
        height = _image_node(displacement.inputs['Height'])
        if not height:
            raise ValueError('Connected displacement does not resolve to a scalar height image.')
    if not displacement and chosen is None:
        candidates = [node for node in nodes if node.type=='TEX_IMAGE' and node.image and
                      any(re.fullmatch(r'(sbsar_tx_)?(height|displacement)', label.strip(), re.I)
                          for label in (node.label,node.name))]
        if len(candidates)>1:
            raise ValueError('Multiple height nodes. Pick one image in Materials.')
        height = candidates[0] if candidates else None
    source = chosen or (height.image if height else _companion(color.image if color else None))
    if source is None:
        return None
    if (not isinstance(source,bpy.types.Image) or source.source not in ('FILE','GENERATED')
            or source.colorspace_settings.name!='Non-Color' or not source.size[0]):
        raise ValueError('Height must be a readable Non-Color image.')
    reference = height or color
    if reference is None:
        raise ValueError('Height image needs a UV-mapped material image as its coordinate reference.')
    uv, transform, extension = _coordinates(reference,mesh)
    if shader and shader.type=='BSDF_PRINCIPLED':
        for name in ('Base Color','Normal','Metallic','Roughness'):
            channel = _image_node(shader.inputs[name])
            if channel is not None and _coordinates(channel,mesh) != (uv,transform,extension):
                raise ValueError(f'Height and {name} use different coordinates or edge policies.')
    direct = bool(height and displacement)
    span = displacement.inputs['Scale'].default_value if direct else .025
    neutral = displacement.inputs['Midlevel'].default_value if direct else .5
    if hasattr(material,HEIGHT_SPAN) and material.is_property_set(HEIGHT_SPAN):
        span = getattr(material,HEIGHT_SPAN)
    else:
        span = material.get(HEIGHT_SPAN,span)
    if hasattr(material,HEIGHT_NEUTRAL) and material.is_property_set(HEIGHT_NEUTRAL):
        neutral = getattr(material,HEIGHT_NEUTRAL)
    else:
        neutral = material.get(HEIGHT_NEUTRAL,neutral)
    if (not isinstance(span,(int,float)) or not isinstance(neutral,(int,float))
            or not 0 < span <= 1 or not 0 <= neutral <= 1):
        raise ValueError('Use positive finite height strength in metres and a neutral value between 0 and 1.')
    return Height(source,uv,transform,extension,span,neutral)


def _validate_samples(image):
    if not image.is_float:
        return
    # A float image can contain out-of-range values. The depth limit assumes
    # unit-range scalar data so that surrounding structure remains clear.
    values = np.empty(len(image.pixels),dtype=np.float32)
    image.pixels.foreach_get(values)
    colors = values.reshape(-1,image.channels)[:, :3]
    if not np.isfinite(colors).all() or colors.min() < 0 or colors.max() > 1:
        raise ValueError('Float height must contain finite values from zero to one.')


def apply(obj, settings, validated_images):
    """Install modifiers on the stage's editable flat field. Return a UI status."""
    materials = obj.data.materials
    if len(materials)!=1:
        return 'Flat: relief requires one material per mapped section'
    material = materials[0]
    try:
        source = resolve(material,obj.data)
        if source is None:
            return 'Flat: material has no height image'
        if settings.relief_strength == 0:
            return 'Flat: material relief strength is zero'
        if source.image not in validated_images:
            _validate_samples(source.image)
            validated_images.add(source.image)
        levels = settings.relief_resolution
        if 2 * sum(p.area for p in obj.data.polygons) * 4**levels / GRID**2 > MAX_TRIANGLES:
            return 'Flat: reduce the relief resolution on this surface'
        mesh, weights = cage(obj.data,obj.data.uv_layers[source.uv])
    except (ValueError, OSError, RuntimeError) as exc:
        return f'Flat: {exc}'
    triangles = (sum(len(face.vertices) for face in mesh.polygons) * 2 * 4 ** (levels - 1)
                 if levels else sum(len(face.vertices) - 2 for face in mesh.polygons))
    if triangles > MAX_TRIANGLES:
        bpy.data.meshes.remove(mesh)
        return 'Flat: reduce the relief resolution on this surface'
    coords = mesh.uv_layers[source.uv]
    values = mesh.uv_layers[HEIGHT_UV]
    for index, loop in enumerate(coords.data):
        u,v = loop.uv
        values.data[index].uv = (source.transform @ Vector((u,v,1.)))[:2]
    old = obj.data
    if old.users == 1:
        name = old.name
        obj.data = mesh
        bpy.data.meshes.remove(old)
        mesh.name = name
    else:
        obj.data = mesh
    mask = obj.vertex_groups.new(name='Caelmor Relief Interior')
    for index, weight in enumerate(weights):
        if weight>0:
            mask.add([index], float(weight), 'REPLACE')
    subdivide = obj.modifiers.new('Caelmor Relief Sampling','SUBSURF')
    subdivide.subdivision_type = 'SIMPLE'
    subdivide.levels = subdivide.render_levels = levels
    subdivide.uv_smooth = 'NONE'
    modifier = obj.modifiers.new('Caelmor Material Height','DISPLACE')
    texture = next((tex for tex in bpy.data.textures if tex.type=='IMAGE' and tex.get('caelm_height_texture')
                    and tex.image==source.image and tex.extension==source.extension), None)
    if texture is None:
        texture = bpy.data.textures.new(f'Caelmor Height | {source.image.name}',type='IMAGE')
        texture.image,texture.extension = source.image,source.extension
        texture['caelm_height_texture'] = True
    modifier.texture = texture
    modifier.texture_coords = 'UV'
    modifier.uv_layer = HEIGHT_UV
    modifier.direction = 'NORMAL'
    modifier.vertex_group = mask.name
    modifier.mid_level = source.neutral
    modifier.strength = min(MAX_STRENGTH,source.span * settings.relief_strength)
    return f'Height: {source.image.name}'
