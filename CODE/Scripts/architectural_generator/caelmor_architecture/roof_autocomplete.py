"""Blender authoring for a detached roof over a confirmed modular wall bearing."""
from hashlib import sha256
import json
import math
from pathlib import Path
import uuid

import bpy
from mathutils import Matrix, Vector

from .blender_backend import _export_selection, _mesh_object, _remove_object
from .construction import Resolver
from .brookoak_courses import ALBEDO_SHA256, cover_buffers
from .geometry import MeshBuffer
from .model import Plan, Settings, rectangle_union_outline
from .roof import _line_span, build_roof, roof_faces
from .roof_selection import Bearing, infer_bearing


PREVIEW = 'caelm_roof_bearing_preview'
ROOF = 'caelm_autocomplete_roof'
MATERIALS = {'BROOKOAK': ('Brookoak Shingles', 'Lowmark_Brookoak_RoofShingles')}


def _roof_buffers(bearing, rise, detail, overhang, ridge, seed):
    values = (*bearing.center, bearing.width, bearing.depth, bearing.angle, rise, overhang)
    if not all(math.isfinite(v) for v in values) or not 1 <= min(bearing.width,bearing.depth) <= max(bearing.width,bearing.depth) <= 40:
        raise ValueError('Use a finite bearing rectangle with sides between 1 and 40 m')
    if not 0 <= detail <= 100 or not .15 <= overhang <= .8 or ridge not in ('AUTO','X','Y'):
        raise ValueError('Check detail, ridge axis and overhang (0.15–0.8 m)')
    ridge_setting = ridge
    if ridge == 'AUTO':
        ridge = 'X' if bearing.width >= bearing.depth - .0001 else 'Y'
    x, y = bearing.width/2, bearing.depth/2
    overrides = {'by_role': {'roof_cover': {'representation': 'HYBRID'}}}
    settings = Settings(seed=seed, detail='HIGH', geometry_mode='EFFICIENT', roof_style='GABLE',
                        overhang=overhang, construction_overrides=overrides)
    rects = list(bearing.rects) if bearing.rects else [(-x,-y,x,y,ridge)]
    if bearing.rects and ridge_setting != 'AUTO' and ridge != rects[0][4]:
        raise ValueError('Use the inferred ridge direction for a connected wing')
    plan = Plan(settings,rects)
    # Rise is specified for the main volume. The same pitch applies to the
    # wing, whose ridge elevation follows from its own horizontal run.
    main = rects[0]
    run = (main[3]-main[1])/2 if main[4]=='X' else (main[2]-main[0])/2
    pitch = math.degrees(math.atan2(rise,run))
    if not 15 <= pitch <= 65:
        raise ValueError(f'Roof rise gives a {pitch:.1f}° pitch. Use 15–65° for the main span')
    plan.slope = rise/run
    plan.settings.pitch = pitch
    plan.eave = .12  # Deck underside bears on the wall datum.
    plan.construction_resolver = Resolver(overrides, 'LOWMARK')
    plan.construction_zone = 'autocomplete'
    plan.cover_percent = detail
    plan.roof_cover_builder = cover_buffers
    buffers = build_roof(plan)
    infill = MeshBuffer('Gable infill', 'timber_light', 'roof')
    patches = roof_faces(plan)
    for start,end in plan.edges:
        axis = 0 if abs(start[0]-end[0])<1e-7 else 1
        along = 1-axis
        delta = end[along]-start[along]
        direction = ((-.13*math.copysign(1,delta),0,0) if axis==0
                     else (0,.13*math.copysign(1,delta),0))
        lo,hi = sorted((start[along],end[along]))
        for patch in patches:
            span = _line_span(patch.poly,axis,start[axis])
            if span is None:
                continue
            a,b = max(lo,span[0]),min(hi,span[1])
            if b-a < 1e-7:
                continue
            pa,pb = list(start),list(start)
            pa[along],pb[along] = a,b
            za,zb = max(0,patch.height(*pa)-.12),max(0,patch.height(*pb)-.12)
            if max(za,zb) > 1e-6:
                infill.extrude([(*pa,0),(*pb,0),(*pb,zb),(*pa,za)],direction)
    return plan, buffers+[infill]


def _field_material(paths):
    # Pack the authored maps into each saved Blender project. glTF can retain
    # albedo/normal PNG and will encode the linear roughness texture for ORM.
    key = json.dumps([(str(path), path.stat().st_mtime_ns) for path in paths])
    existing = next((m for m in bpy.data.materials if m.get('caelm_brookoak_maps') == key),None)
    if existing:
        return existing
    mat = bpy.data.materials.new('Brookoak Roof Field')
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    shader = nodes.get('Principled BSDF')
    uv = nodes.new('ShaderNodeUVMap')
    uv.uv_map = 'RoofUV'
    for path, socket in zip(paths, ('Base Color', 'Normal', 'Roughness')):
        image = bpy.data.images.load(str(path), check_existing=False)
        image.colorspace_settings.name = 'sRGB' if socket == 'Base Color' else 'Non-Color'
        image.pack()
        texture = nodes.new('ShaderNodeTexImage')
        texture.image = image
        links.new(uv.outputs['UV'], texture.inputs['Vector'])
        source = texture.outputs['Color']
        if socket == 'Normal':
            normal = nodes.new('ShaderNodeNormalMap')
            normal.uv_map = 'RoofUV'
            links.new(source, normal.inputs['Color'])
            source = normal.outputs['Normal']
        links.new(source, shader.inputs[socket])
    mat['caelm_brookoak_maps'] = key
    return mat


def _trim_material(key, field):
    token = field['caelm_brookoak_maps'] + key
    material = next((m for m in bpy.data.materials if m.get('caelm_brookoak_trim') == token),None)
    if material:
        return material
    # The atlas represents multiple irregular-width shingles. Derive a
    # pattern-free tone from the same albedo and let the physical laps shade.
    import numpy as np
    image = next(n.image for n in field.node_tree.nodes if n.type == 'TEX_IMAGE')
    pixels = np.empty(len(image.pixels),dtype=np.float32)
    image.pixels.foreach_get(pixels)
    # Blender's byte-backed image buffer supplies stored sRGB samples here.
    rgb = np.median(pixels.reshape(-1,4)[::32,:3],axis=0)
    color = np.where(rgb <= .04045, rgb/12.92, ((rgb+.055)/1.055)**2.4)
    factor = {'roof':1.0,'roof_dark':.72,'roof_worn':1.19,'roof_patch':1.08}[key]
    material = bpy.data.materials.new('Brookoak Solid '+key)
    material.use_nodes = True
    shader = material.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*[min(1,float(c)*factor) for c in color],1)
    material.diffuse_color = shader.inputs['Base Color'].default_value
    shader.inputs['Roughness'].default_value = .83
    material['caelm_brookoak_trim'] = token
    return material


def build_roof_collection(scene,bearing,*,rise,detail,material_directory,seed=17,overhang=.35,
                          ridge='AUTO',collection=None,material='BROOKOAK'):
    if collection is not None and (not collection.get(ROOF) or collection not in list(scene.collection.children)):
        raise ValueError('Select a Roof AutoComplete collection linked to this scene')
    try:
        _, stem = MATERIALS[material]
    except KeyError as error:
        raise ValueError('Unsupported roof material') from error
    directory = Path(bpy.path.abspath(str(material_directory))).resolve()
    paths = [directory / (stem+suffix) for suffix in ('_albedo.png','_normal.png','_rough.exr')]
    if not all(path.is_file() for path in paths):
        raise ValueError('Select the procedurally_generated folder containing the three Brookoak maps')
    if sha256(paths[0].read_bytes()).hexdigest() != ALBEDO_SHA256:
        raise ValueError("Brookoak albedo differs from the registered course layout. Select the approved export set.")
    plan,buffers = _roof_buffers(bearing,rise,detail,overhang,ridge,seed)
    field = _field_material(paths)
    stage = []
    build_id = uuid.uuid4().hex
    matrix = Matrix.Translation(Vector(bearing.center)) @ Matrix.Rotation(bearing.angle,4,'Z')
    cache = {}
    try:
        for buffer in buffers:
            obj = _mesh_object(buffer,cache,build_id,plan)
            stage.append(obj)
            obj.matrix_world = matrix
            obj['caelm_roof_part'] = True
            if buffer.field_family:
                obj.data.uv_layers['UV2_Surface'].name = 'RoofUV'
                obj.data.uv_layers.active = obj.data.uv_layers['RoofUV']
                obj.data.uv_layers['RoofUV'].active_render = True
                obj.data.materials[0] = field
            elif buffer.material.startswith('roof'):
                obj.data.materials[0] = _trim_material(buffer.material,field)
            obj.data.calc_loop_triangles()
        triangles = sum(len(o.data.loop_triangles) for o in stage)
        if collection is None:
            collection = bpy.data.collections.new('Caelmor AutoComplete Roof')
            scene.collection.children.link(collection)
        prior = [o for o in collection.objects if o.get('caelm_roof_part')]
        for obj in stage:
            collection.objects.link(obj)
        for obj in prior:
            _remove_object(obj)
    except Exception:
        for obj in stage:
            _remove_object(obj)
        raise
    collection[ROOF] = True
    collection['caelm_roof_triangles'] = triangles
    collection['caelm_roof_shingles'] = plan.modeled_units
    collection['caelm_roof_cover_units'] = plan.cover_units
    collection['caelm_roof_settings'] = json.dumps(dict(
        center=list(bearing.center),width=bearing.width,depth=bearing.depth,angle=bearing.angle,rects=list(bearing.rects),
        rise=rise,detail=detail,seed=seed,overhang=overhang,ridge=ridge,material=material,
        material_directory=str(directory)),sort_keys=True)
    return collection


def export_roof(collection, filepath):
    objects = [o for o in collection.objects if o.get('caelm_roof_part')] if collection else []
    if not objects:
        raise ValueError('Select a generated roof collection to export')
    _export_selection(filepath,objects,objects[0],'GLB')


def _bearing(props):
    rects = json.loads(props.rects)
    if rects:
        sx = props.width/(max(r[2] for r in rects)-min(r[0] for r in rects))
        sy = props.depth/(max(r[3] for r in rects)-min(r[1] for r in rects))
        rects = [(a*sx,b*sy,c*sx,d*sy,axis) for a,b,c,d,axis in rects]
    return Bearing(tuple(props.center),props.width,props.depth,props.angle,tuple(rects))


def _target_changed(props, context):
    props.ready = False


def _bearing_changed(props, context):
    props.ready = False


def _preview(scene, props):
    bearing = _bearing(props)
    rotation = Matrix.Rotation(bearing.angle,3,'Z')
    center = Vector(bearing.center)
    x,y = bearing.width/2,bearing.depth/2
    outline = rectangle_union_outline(bearing.rects) if bearing.rects else ((-x,-y),(x,-y),(x,y),(-x,y))
    vertices = [center + rotation @ Vector((a,b,.012)) for a,b in outline]
    for obj in list(scene.objects):
        if obj.get(PREVIEW):
            _remove_object(obj)
    mesh = bpy.data.meshes.new('Roof Bearing Outline')
    mesh.from_pydata(vertices,[(i,(i+1)%len(vertices)) for i in range(len(vertices))],[])
    obj = bpy.data.objects.new('Roof Bearing Outline',mesh)
    scene.collection.objects.link(obj)
    obj[PREVIEW] = True
    obj.hide_render = True
    obj.hide_select = True
    obj.show_in_front = True


class RoofSettings(bpy.types.PropertyGroup):
    center: bpy.props.FloatVectorProperty(name='Bearing Center XYZ', subtype='TRANSLATION',unit='LENGTH',update=_bearing_changed)
    width: bpy.props.FloatProperty(name='Width',min=1,max=40,default=6,unit='LENGTH',update=_bearing_changed)
    depth: bpy.props.FloatProperty(name='Depth',min=1,max=40,default=4,unit='LENGTH',update=_bearing_changed)
    angle: bpy.props.FloatProperty(name='Bearing Rotation',subtype='ANGLE',update=_bearing_changed)
    rects: bpy.props.StringProperty(default='[]')
    ready: bpy.props.BoolProperty(default=False)
    rise: bpy.props.FloatProperty(name='Roof Height',description='Ridge rise above the wall bearing, excluding cover thickness',
                                  min=.1,max=30,default=2,unit='LENGTH')
    detail: bpy.props.IntProperty(name='Experimental Modeled Shingles',subtype='PERCENTAGE',min=0,max=100,default=0,
                                  description='Zero uses a flat mapped covering. Positive values explicitly add legacy shingle geometry')
    material: bpy.props.EnumProperty(name='Roof Material',items=[
        (key,record[0],'') for key,record in MATERIALS.items()])
    material_directory: bpy.props.StringProperty(name='PBR Map Folder',subtype='DIR_PATH',
        default='C:/Users/CK/Documents/Caelmor-Repo/MEDIA/Materials/procedurally_generated')
    ridge: bpy.props.EnumProperty(name='Ridge Direction',items=[
        ('AUTO','Long Side',''),('X','Bearing X',''),('Y','Bearing Y','')])
    overhang: bpy.props.FloatProperty(name='Overhang',min=.15,max=.8,default=.35,unit='LENGTH')
    seed: bpy.props.IntProperty(name='Seed',min=0,max=2147483647,default=17)
    advanced: bpy.props.BoolProperty(name='Advanced')
    target: bpy.props.PointerProperty(name='Update Target',type=bpy.types.Collection,
                                      poll=lambda self,collection: bool(collection.get(ROOF)),
                                      update=_target_changed)


class CAELMOR_OT_roof_preview(bpy.types.Operator):
    bl_idname = 'caelmor.roof_preview'
    bl_label = 'Infer Wall Bearing'
    bl_options = {'REGISTER','UNDO'}
    infer: bpy.props.BoolProperty(default=True)

    def execute(self, context):
        props = context.scene.caelm_roof_settings
        try:
            if self.infer:
                b = infer_bearing(context.selected_objects,context.evaluated_depsgraph_get())
                props.center,props.width,props.depth,props.angle = b.center,b.width,b.depth,b.angle
                props.rects = json.dumps(b.rects)
                props.target = None
                props.detail = 0
            _preview(context.scene,props)
            props.ready = True
        except ValueError as error:
            if self.infer:
                props.ready = False
            self.report({'ERROR'},str(error))
            return {'CANCELLED'}
        return {'FINISHED'}


class CAELMOR_OT_roof_load(bpy.types.Operator):
    bl_idname = 'caelmor.roof_load'
    bl_label = 'Load Saved Bearing and Settings'
    bl_options = {'REGISTER','UNDO'}
    from_selection: bpy.props.BoolProperty(default=False,options={'HIDDEN'})

    def execute(self, context):
        props = context.scene.caelm_roof_settings
        if self.from_selection:
            active = context.view_layer.objects.active
            props.target = next((c for c in active.users_collection if c.get(ROOF)),None) if active else None
        if not props.target:
            return {'CANCELLED'}
        settings = json.loads(props.target['caelm_roof_settings'])
        props.rects = json.dumps(settings.pop('rects', []))
        for key,value in settings.items():
            setattr(props,key,value)
        _preview(context.scene,props)
        props.ready = True
        return {'FINISHED'}


class CAELMOR_OT_roof_generate(bpy.types.Operator):
    bl_idname = 'caelmor.roof_generate'
    bl_label = 'Generate / Update Roof'
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        props = context.scene.caelm_roof_settings
        if not props.ready:
            self.report({'ERROR'},'Preview and confirm the bearing first')
            return {'CANCELLED'}
        try:
            props.target = build_roof_collection(context.scene,_bearing(props),rise=props.rise,detail=props.detail,
                material_directory=props.material_directory,seed=props.seed,overhang=props.overhang,
                ridge=props.ridge,collection=props.target,material=props.material)
        except (ValueError,RuntimeError,OSError) as error:
            self.report({'ERROR'},str(error))
            return {'CANCELLED'}
        for obj in list(context.scene.objects):
            if obj.get(PREVIEW):
                _remove_object(obj)
        props.ready = True
        self.report({'INFO'},f"Roof: {props.target['caelm_roof_triangles']:,} triangles")
        return {'FINISHED'}


class CAELMOR_OT_roof_export(bpy.types.Operator):
    bl_idname = 'caelmor.roof_export'
    bl_label = 'Export Roof GLB'
    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    filter_glob: bpy.props.StringProperty(default='*.glb',options={'HIDDEN'})

    def invoke(self, context, event):
        self.filepath = bpy.path.ensure_ext(self.filepath or 'Caelmor Roof','.glb')
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        try:
            export_roof(context.scene.caelm_roof_settings.target,bpy.path.ensure_ext(self.filepath,'.glb'))
        except (ValueError,RuntimeError,OSError) as error:
            self.report({'ERROR'},str(error))
            return {'CANCELLED'}
        return {'FINISHED'}


def draw_roof(layout,context,selected=None):
    props = context.scene.caelm_roof_settings
    if context.mode!='OBJECT':
        layout.label(text='Switch to Object Mode to work on a roof.')
        return
    if selected and selected!=props.target:
        layout.label(text=selected.name,icon='HOME')
        layout.operator('caelmor.roof_load',text='Edit Selected Roof').from_selection = True
        return
    layout.operator('caelmor.roof_preview',text='Preview Wall Top',icon='MESH_GRID')
    layout.prop(props,'target',text='Existing Roof')
    if props.target:
        layout.operator('caelmor.roof_load',text='Load Roof Settings')
    for name in ('material','rise','overhang','advanced'):
        layout.prop(props,name)
    if props.advanced:
        for name in ('detail','material_directory','ridge','seed','center','width','depth','angle'):
            layout.prop(props,name)
        correction = layout.operator('caelmor.roof_preview',text='Preview Manual Bearing')
        correction.infer = False
    elif props.detail:
        layout.label(text='Saved experimental modeled shingles are enabled.',icon='INFO')
    if props.ready:
        shape = 'Main + wing' if props.rects != '[]' else 'Rectangle'
        layout.label(text=f'{shape} {props.width:.2f} × {props.depth:.2f} m')
        layout.operator('caelmor.roof_generate',icon='MOD_BUILD')
    if props.target:
        layout.operator('caelmor.roof_export',icon='EXPORT')


CLASSES = (RoofSettings,CAELMOR_OT_roof_preview,CAELMOR_OT_roof_load,
           CAELMOR_OT_roof_generate,CAELMOR_OT_roof_export)
