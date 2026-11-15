"""Task-oriented building authoring. Dialogs edit the selected building's saved inputs."""
from dataclasses import replace
import json

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty

from . import _REGION_ITEMS, _TYPE_ITEMS, _active_build, _report_error, _settings_from_json
from .blender_backend import build, load_settings
from .construction_library import ASSEMBLIES, FINISH_ROLES, edit_finish, enum_items, replace_choice, selected
from .model import Settings, resolve_settings, supports_wall_guides
from .profiles import TYPE_SPECS


_ROOF = (('AUTO','Recommended','Use this volume’s original roof form'),
         ('GABLE','Gable','Two slopes meeting at a ridge'),
         ('HIP','Hip','Slopes on all sides'))
_MANUAL = ('SMITHY','GATEHOUSE')
_ASSEMBLIES = tuple(key for key in ASSEMBLIES if not key.endswith('_depth'))
_GROUPS = tuple((key,*label,index) for index,(key,label) in enumerate(FINISH_ROLES.items()))
_TIMBER = ASSEMBLIES['supports'][2]


def _dimensions(layout, state, *, fitted=False, one_storey=False):
    if not fitted:
        row = layout.row(align=True)
        row.prop(state,'width')
        row.prop(state,'depth')
    row = layout.row(align=True)
    if not one_storey:
        row.prop(state,'floors')
    if not fitted:
        row.prop(state,'floor_height')


def _select(context,obj):
    if obj and obj.visible_get():
        for prior in context.selected_objects:
            prior.select_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj


def _part(context):
    active = context.view_layer.objects.active
    return active if (active and active.select_get() and active.type=='MESH' and active.get('caelm_generated')
                      and not active.get('caelm_collider')) else None


def _selection(context):
    active = context.view_layer.objects.active
    return _active_build(context) if active and active.select_get() else None


def _profiles(collection, settings):
    profiles = json.loads(collection.get('caelm_editable_volumes','{}'))
    if settings.world_aware and not profiles:
        # Existing scenes gain the current effective values on first edit.
        from .engine import generate
        from .guide_backend import collect
        guides, _ = collect(collection,settings,load_settings(collection))
        plan,_ = generate(settings, finish_names=bpy.data.materials.keys(), opening_guides=guides)
        profiles = {z.key: dict(width=z.width,depth=z.depth,floors=z.plan.settings.floors,
            floor_height=z.plan.settings.floor_height,style=z.plan.roof_mode,pitch=z.plan.settings.pitch,
            recommended_style=z.plan.recommended_roof_mode,
            overhang=z.plan.settings.overhang) for z in plan.world_zones}
    return profiles


def _groups(operator,context):
    collection = bpy.data.collections.get(operator.target) if operator.target else _selection(context)
    roles = _roles(collection) if collection else ()
    return tuple(item for item in _GROUPS if item[0] in roles)


class CAELMOR_OT_create_building(bpy.types.Operator):
    bl_idname = 'caelmor.create_building'
    bl_label = 'Create Building'
    bl_description = 'Start with a building type and regional defaults, a box, or dimensions you enter'
    bl_options = {'REGISTER','UNDO'}

    function: EnumProperty(name='Building Type',items=_TYPE_ITEMS,default='COTTAGE')
    region: EnumProperty(name='Starting Style',items=_REGION_ITEMS,default='LOWMARK',
                         description='Suggest construction and appearance. You can edit the building after creation')
    method: EnumProperty(name='Size',items=[
        ('RECOMMENDED','Recommended','Start with a size appropriate to this building and region'),
        ('MANUAL','Enter Dimensions','Set the main building dimensions while keeping regional construction'),
        ('BOX','Selected Box','Fit the main volume to the selected upright rectangular box')])
    width: FloatProperty(name='Width',unit='LENGTH',default=8.,min=6.,max=24.)
    depth: FloatProperty(name='Depth',unit='LENGTH',default=6.,min=4.,max=16.)
    floors: IntProperty(name='Storeys',default=1,min=1,max=3)
    floor_height: FloatProperty(name='Storey Height',unit='LENGTH',default=2.8,min=2.4,max=3.8)

    @classmethod
    def poll(cls,context):
        return context.mode=='OBJECT'

    def invoke(self,context,event):
        active = context.view_layer.objects.active
        if not _selection(context) and _box_candidate(active) and active.select_get():
            self.method = 'BOX'
        return context.window_manager.invoke_props_dialog(self,width=365,confirm_text='Generate')

    def draw(self,context):
        self.layout.prop(self,'function')
        self.layout.prop(self,'region')
        self.layout.prop(self,'method')
        if self.method=='BOX':
            if self.function not in _MANUAL:
                if self.function not in ('STABLE','MARKET_HALL'):
                    self.layout.prop(self,'floors')
                self.layout.label(text='The top of the box sets the eaves.')
            else:
                self.layout.label(text='The working layout sets its bay sizes.',icon='INFO')
        elif self.method=='MANUAL':
            if self.function in _MANUAL:
                self.layout.label(text='The working layout sets its bay sizes.',icon='INFO')
            else:
                _dimensions(self.layout,self,one_storey=self.function in ('STABLE','MARKET_HALL'))

    def execute(self,context):
        try:
            settings = Settings(function=self.function,region=self.region,use_grammar=True,world_aware=True,
                                construction_overrides={},geometry_mode='EFFICIENT',detail='MEDIUM',
                                crafted_curves=True,seed_massing=True)
            if self.method=='BOX':
                from .blockout import fit
                source = context.view_layer.objects.active
                context.view_layer.update()
                floors = 1 if self.function in ('STABLE','MARKET_HALL') else self.floors
                fitted,placement = fit(replace(settings,floors=floors),source)
                collection,_ = build(fitted,placement=placement)
                collection['caelm_blockout_source'] = source
                if supports_wall_guides(fitted):
                    context.scene.caelmor_settings.caelm_guide_target = collection
            else:
                if self.method=='MANUAL':
                    settings = replace(settings,manual_shape=True,width=self.width,depth=self.depth,
                                       floors=1 if self.function in ('STABLE','MARKET_HALL') else self.floors,
                                       floor_height=self.floor_height)
                collection,_ = build(settings,origin=context.scene.cursor.location.copy())
            collection.name = TYPE_SPECS[self.function].label
            return {'FINISHED'}
        except Exception as exc:
            return _report_error(self,exc)


class CAELMOR_OT_edit_building(bpy.types.Operator):
    bl_idname = 'caelmor.edit_building'
    bl_label = 'Edit Building'
    bl_description = 'Open the selected building’s current values. Apply rebuilds compatible generated parts'
    bl_options = {'REGISTER','UNDO'}

    action: EnumProperty(items=[(s,s.title(),'') for s in
                               ('SHAPE','ROOF','MATERIAL','CONSTRUCTION','CONDITION','REBUILD')])
    target: StringProperty(options={'HIDDEN','SKIP_SAVE'})
    snapshot: StringProperty(options={'HIDDEN','SKIP_SAVE'})
    part: StringProperty(options={'HIDDEN','SKIP_SAVE'})
    zone: StringProperty(options={'HIDDEN','SKIP_SAVE'})
    recommended_roof: StringProperty(options={'HIDDEN','SKIP_SAVE'})
    recommend: BoolProperty(name='Recommended Dimensions',
                            description='Let the building type and starting style choose the main envelope')
    width: FloatProperty(name='Width',unit='LENGTH',min=6,max=24,default=8)
    depth: FloatProperty(name='Depth',unit='LENGTH',min=4,max=16,default=6)
    floors: IntProperty(name='Storeys',min=1,max=4,default=1)
    floor_height: FloatProperty(name='Storey Height',unit='LENGTH',min=2.4,max=3.8,default=2.8)
    footprint: EnumProperty(name='Footprint',items=[(key,label,'') for key,label in
                           (('RECT','Rectangle'),('L','L'),('T','T'),('U','U'))])
    wing_width: FloatProperty(name='Wing Width',unit='LENGTH',min=2.5,max=10,default=4.2)
    wing_depth: FloatProperty(name='Wing Depth',unit='LENGTH',min=2.5,max=12,default=4.5)
    style: EnumProperty(name='Roof Form',items=_ROOF)
    custom_pitch: BoolProperty(name='Set Pitch',description='Use a specific slope angle for this roof')
    pitch: FloatProperty(name='Pitch (degrees)',min=10,max=60,default=35)
    custom_overhang: BoolProperty(name='Set Overhang',description='Use a specific distance beyond the wall')
    overhang: FloatProperty(name='Overhang',unit='LENGTH',min=.04,max=.8,default=.42)
    match_group: BoolProperty(name='Apply to Matching Group',
                              description='Use the material on this construction group across the building. Keep individual material overrides')
    group: EnumProperty(name='Group',items=_groups)
    material: StringProperty(name='Scene Material',description='Choose a material loaded into this Blender file')
    clear_material: BoolProperty(name='Restore Default Material',
                                description='Remove this assignment and use the next applicable building or regional material')
    orient: EnumProperty(name='Texture Rotation',items=[
        ('AUTO','Automatic','Follow the generated coordinates'),('90','90°',''),('180','180°',''),('270','270°','')])
    age: FloatProperty(name='Age (years)',min=0,max=250)
    maintenance: FloatProperty(name='Maintenance',min=0,max=1)
    craftsmanship: EnumProperty(name='Craftsmanship',items=[
        ('ROUGH','Rough','Coarser stock and workmanship'),('STANDARD','Standard','Everyday workmanship'),
        ('FINE','Fine','Careful preparation and joinery')])

    @classmethod
    def poll(cls,context):
        return context.mode=='OBJECT' and _selection(context) is not None

    @classmethod
    def description(cls,context,properties):
        return {
            'SHAPE':'Change the main dimensions or refit its source box',
            'ROOF':'Change the selected volume’s roof form, pitch and overhang',
            'MATERIAL':'Apply or restore a material on this part or its matching group',
            'CONSTRUCTION':'Choose the assembly or timber profile for this selection',
            'CONDITION':'Adjust age, upkeep and workmanship for this building',
            'REBUILD':'Rebuild this building using its saved choices and protected meshes',
        }.get(properties.action,cls.bl_description)

    def _lookup(self,context):
        collection = bpy.data.collections.get(self.target) if self.target else _selection(context)
        if not collection or collection not in list(context.scene.collection.children_recursive):
            raise ValueError('Select a building in this scene.')
        if self.target and collection.get('caelm_settings')!=self.snapshot:
            raise ValueError('The building changed while this dialog was open. Reopen the edit.')
        if self.part:
            obj = next((o for o in collection.objects if o.get('caelm_buffer_id')==self.part),None)
            if obj is None:
                raise ValueError('The selected part changed while this dialog was open. Select it again.')
        else:
            obj = None if self.target else _part(context)
        return collection,_settings_from_json(load_settings(collection)),obj

    def invoke(self,context,event):
        try:
            collection,settings,obj = self._lookup(context)
            self.target,self.snapshot = collection.name,collection['caelm_settings']
            self.part = obj.get('caelm_buffer_id','') if obj else ''
            if self.action=='REBUILD':
                return self.execute(context)
            role = obj.get('caelm_component_role') if obj else None
            if self.action in ('SHAPE','ROOF'):
                profiles = _profiles(collection,settings)
                main = next(iter(profiles),'')
                self.zone = (obj.get('caelm_world_zone') or main) if obj and self.action=='ROOF' else main
                current = profiles.get(self.zone,{})
                display = settings if current else resolve_settings(settings)
                self.recommend = settings.use_grammar and not settings.manual_shape and not settings.fit_blockout
                for name in ('width','depth','floors','floor_height','pitch','overhang'):
                    setattr(self,name,current.get(name,getattr(display,name)))
                self.footprint,self.wing_width,self.wing_depth = display.footprint,display.wing_width,display.wing_depth
                inputs = (settings.roof_overrides or {}).get(self.zone or 'main',{})
                self.style = inputs.get('style','AUTO') if settings.world_aware else inputs.get('style',settings.roof_style)
                self.recommended_roof = current.get('recommended_style',current.get('style',''))
                self.custom_pitch = 'pitch' in inputs
                self.custom_overhang = 'overhang' in inputs
            elif self.action=='CONDITION':
                self.age,self.maintenance,self.craftsmanship = settings.age,settings.maintenance,settings.craftsmanship
            elif self.action=='MATERIAL':
                roles = _roles(collection)
                self.match_group = obj is None
                if role in FINISH_ROLES or roles:
                    self.group = role if role in FINISH_ROLES else roles[0]
                if obj and obj.data.materials and obj.data.materials[0]:
                    self.material = obj.data.materials[0].name
                self.orient = obj.get('caelm_uv_rotation','AUTO') if obj else 'AUTO'
            elif self.action=='CONSTRUCTION':
                by_role = (settings.construction_overrides or {}).get('by_role',{})
                for key in _ASSEMBLIES:
                    group,_,options = ASSEMBLIES[key]
                    setattr(self,key,selected(options,by_role.get(group,{})))
                self.timber = obj.get('caelm_variant','AUTO') if obj else 'AUTO'
            return context.window_manager.invoke_props_dialog(self,width=385,confirm_text='Apply')
        except Exception as exc:
            return _report_error(self,exc)

    def draw(self,context):
        layout = self.layout
        try:
            collection,settings,obj = self._lookup(context)
        except ValueError as exc:
            layout.label(text=str(exc),icon='ERROR')
            return
        if self.action=='SHAPE':
            if settings.fit_blockout:
                source = collection.get('caelm_blockout_source')
                layout.label(text=f'Source box: {source.name}' if source else 'Source box is unavailable')
                layout.label(text='Move or resize the box, then apply to refit.')
                _dimensions(layout,self,fitted=True,one_storey=settings.function in ('STABLE','MARKET_HALL'))
            elif settings.world_aware and settings.function in _MANUAL:
                layout.label(text='The forge or passage sets its own bay sizes.',icon='INFO')
            else:
                layout.prop(self,'recommend')
                if not self.recommend:
                    if settings.world_aware:
                        layout.label(text='Main volume dimensions')
                    _dimensions(layout,self,one_storey=settings.world_aware and settings.function in ('STABLE','MARKET_HALL'))
                    if not settings.world_aware:
                        layout.prop(self,'footprint')
                        if self.footprint!='RECT':
                            layout.prop(self,'wing_width')
                            layout.prop(self,'wing_depth')
        elif self.action=='ROOF':
            if self.zone:
                layout.label(text=_volume_label(self.zone))
            layout.prop(self,'style')
            form = self.recommended_roof if self.style=='AUTO' else self.style
            for name in ('pitch','overhang'):
                if form=='TERRACE' or name=='pitch' and form=='BOW':
                    continue
                layout.prop(self,'custom_'+name)
                if getattr(self,'custom_'+name):
                    layout.prop(self,name)
        elif self.action=='MATERIAL':
            if obj:
                layout.prop(self,'match_group')
            if not obj or self.match_group and obj.get('caelm_component_role') in FINISH_ROLES:
                layout.prop(self,'group')
            elif obj and self.match_group:
                layout.label(text='Matching '+_part_label(obj).lower())
            elif obj:
                layout.label(text=_part_label(obj))
            layout.prop(self,'clear_material')
            if not self.clear_material:
                layout.prop_search(self,'material',bpy.data,'materials')
                if obj and obj.get('caelm_component_id') and not self.match_group:
                    layout.prop(self,'orient')
        elif self.action=='CONDITION':
            for name in ('age','maintenance','craftsmanship'):
                layout.prop(self,name)
        elif self.action=='CONSTRUCTION':
            keys = _assembly_choices(collection,obj)
            for name in keys:
                layout.prop(self,name)
            if obj and obj.get('caelm_treatment')=='structural_timber':
                layout.prop(self,'timber')

    def execute(self,context):
        try:
            collection,settings,obj = self._lookup(context)
            part = obj.get('caelm_buffer_id') if obj else None
            source = None
            placement = None
            materials = None
            if self.action=='SHAPE':
                if settings.fit_blockout:
                    from .blockout import fit
                    source = collection.get('caelm_blockout_source')
                    if not source or context.scene.objects.get(source.name)!=source:
                        raise ValueError('The source box must be in this scene before refitting.')
                    context.view_layer.update()
                    settings,placement = fit(replace(settings,floors=self.floors),source)
                elif self.recommend:
                    settings = replace(settings,manual_shape=False,use_grammar=True)
                else:
                    shape = dict(width=self.width,depth=self.depth,floors=self.floors,floor_height=self.floor_height)
                    if settings.world_aware and settings.function in ('STABLE','MARKET_HALL'):
                        shape['floors'] = 1
                    if not settings.world_aware:
                        shape.update(footprint=self.footprint,wing_width=self.wing_width,wing_depth=self.wing_depth)
                    settings = replace(settings,manual_shape=True,**shape)
            elif self.action=='ROOF':
                zone = self.zone or (obj.get('caelm_world_zone') if obj else None)
                zone = (zone or next(iter(_profiles(collection,settings)),None)) if settings.world_aware else 'main'
                if not zone:
                    raise ValueError('Select a roof volume.')
                edits = dict(settings.roof_overrides or {})
                values = {}
                if self.style!='AUTO':
                    values['style'] = self.style
                form = self.recommended_roof if self.style=='AUTO' else self.style
                for name in ('pitch','overhang'):
                    if (getattr(self,'custom_'+name) and form!='TERRACE'
                            and not (name=='pitch' and form=='BOW')):
                        values[name] = getattr(self,name)
                if values:
                    edits[zone] = values
                else:
                    edits.pop(zone,None)
                settings = replace(settings,roof_overrides=edits or None)
            elif self.action=='MATERIAL':
                settings,materials = _material_edit(self,collection,settings,obj)
            elif self.action=='CONDITION':
                settings = replace(settings,age=self.age,maintenance=self.maintenance,
                                   craftsmanship=self.craftsmanship)
            elif self.action=='CONSTRUCTION':
                settings = _construction_edit(self,collection,settings,obj)
            build(settings,collection=collection,placement=placement,section_materials=materials)
            if part:
                _select(context,next((o for o in collection.objects if o.get('caelm_buffer_id')==part),None))
            return {'FINISHED'}
        except Exception as exc:
            if 'Weather roofs cross:' in str(exc):
                exc = ValueError('The edited roof crosses an adjoining roof. Try a smaller overhang or another form.')
            return _report_error(self,exc)


for _key in _ASSEMBLIES:
    _,_label,_options = ASSEMBLIES[_key]
    CAELMOR_OT_edit_building.__annotations__[_key] = EnumProperty(name=_label,items=enum_items(_options))
CAELMOR_OT_edit_building.__annotations__['timber'] = EnumProperty(name='Selected Timber Profile',items=[
    ('AUTO','Inherit group','Use the group or regional profile'),
    *[(preset['variant'],label,help_text) for _,label,help_text,preset in _TIMBER]])


def _roles(collection):
    return tuple(dict.fromkeys(o['caelm_component_role'] for o in collection.objects
                               if o.get('caelm_component_role') in FINISH_ROLES))


def _material_edit(operator,collection,settings,obj):
    material = None if operator.clear_material else bpy.data.materials.get(operator.material)
    if not operator.clear_material and not material:
        raise ValueError('Choose a material loaded in this Blender file.')
    role_edit = operator.match_group or not obj
    component = obj.get('caelm_component_id') if obj else None
    if obj and not role_edit and (obj.get('caelm_protected') or len(obj.data.materials)!=1):
        raise ValueError('Unlock this part to rebuild it. For multiple slots, edit the individual Blender material slots.')
    if not role_edit and not component:
        return settings,{obj['caelm_buffer_id']:material}
    if role_edit and obj and obj.get('caelm_component_role') not in FINISH_ROLES:
        parts = [part for part in collection.objects if part.type=='MESH' and not part.get('caelm_protected')
                 and not part.get('caelm_collider') and len(part.data.materials)==1
                 and all(part.get(key)==obj.get(key) for key in ('caelm_layer','caelm_material'))]
        return settings,{part['caelm_buffer_id']:material for part in parts}
    if role_edit and operator.group not in _roles(collection):
        raise ValueError('Choose a group present in this building.')
    before = settings.construction_overrides or {}
    assignments = edit_finish(before,'by_role' if role_edit else 'by_component',
                              operator.group if role_edit else component,
                              material.name if material else None,operator.orient)
    overrides = before.get('by_component',{})
    changed = {}
    for part in collection.objects:
        key = part.get('caelm_component_id')
        if not key or part.get('caelm_protected'):
            continue
        if role_edit:
            matches = part.get('caelm_component_role')==operator.group and 'finish' not in overrides.get(key,{})
        else:
            matches = key==component
        if matches:
            changed[part['caelm_buffer_id']] = None
    return replace(settings,construction_overrides=assignments),changed


def _assembly_choices(collection,obj):
    roles = _roles(collection)
    role = obj.get('caelm_component_role') if obj else None
    if role in {ASSEMBLIES[key][0] for key in _ASSEMBLIES}:
        return [key for key in _ASSEMBLIES if ASSEMBLIES[key][0]==role]
    if obj and obj.get('caelm_layer')=='roof':
        zone = obj.get('caelm_world_zone')
        profiles = json.loads(collection.get('caelm_editable_volumes','{}'))
        if profiles.get(zone,{}).get('style') in ('GABLE','HIP','BOW','SHED'):
            return ['cover']
    if obj and obj.get('caelm_layer') in ('windows','doors'):
        return []
    return [key for key in _ASSEMBLIES if ASSEMBLIES[key][0] in roles]


def _construction_edit(operator,collection,settings,obj):
    overrides = json.loads(json.dumps(settings.construction_overrides or {}))
    roles = overrides.setdefault('by_role',{})
    for key in _assembly_choices(collection,obj):
        role,_,options = ASSEMBLIES[key]
        choice = getattr(operator,key)
        if choice!=selected(options,roles.get(role,{})):
            replace_choice(roles,role,options,choice)
    if not roles:
        overrides.pop('by_role')
    if obj and obj.get('caelm_treatment')=='structural_timber':
        key = obj['caelm_component_id']
        components = overrides.setdefault('by_component',{})
        fields = components.setdefault(key,{})
        if operator.timber=='AUTO':
            fields.pop('variant',None)
        else:
            fields['variant'] = operator.timber
        if not fields:
            components.pop(key)
        if not components:
            overrides.pop('by_component')
    return replace(settings,construction_overrides=overrides)


def _volume_label(zone):
    prefix,_,rest = zone.partition('_')
    return (rest if prefix in ('lowmark','thornfell','mire','emberholt') else zone).replace('_',' ').title()


def _part_label(obj):
    group = FINISH_ROLES.get(obj.get('caelm_component_role'))
    if group:
        return group[0]
    return {'windows':'Window Parts','doors':'Door Parts','roof':'Roof Part','walls':'Wall Part',
            'structure':'Structure','foundation':'Foundation'}.get(obj.get('caelm_layer'),'Building Detail')


def _box_candidate(obj):
    return obj and obj.type=='MESH' and len(obj.data.vertices)==8 and len(obj.data.polygons)==6


def _task(layout,action,label,icon):
    layout.operator('caelmor.edit_building',text=label,icon=icon).action = action


def draw(layout,context):
    from .roof_autocomplete import ROOF, draw_roof
    props = context.scene.caelmor_settings
    active = context.view_layer.objects.active
    collection = _selection(context)
    standalone = (next((c for c in active.users_collection if c.get(ROOF)),None)
                  if active and active.select_get() else None)
    if not collection:
        layout.prop(props,'caelm_authoring_tool',expand=True)
    if not collection and (props.caelm_authoring_tool=='ROOF' or standalone and props.caelm_authoring_tool=='AUTO'):
        draw_roof(layout,context,standalone)
        return
    if not collection:
        layout.operator('caelmor.create_building',icon='ADD')
        if active and active.type=='MESH' and not _box_candidate(active) and context.mode=='OBJECT':
            _draw_feature(layout,context,None)
        return

    saved = load_settings(collection)
    obj = _part(context)
    bind = active.get('caelm_guide') if active else None
    layout.label(text='Edit Selected Building',icon='HOME')
    layout.label(text=f"{TYPE_SPECS[saved['function']].label} · {dict((k,v) for k,v,_ in _REGION_ITEMS).get(saved.get('region'),'Lowmark Vale')}")
    if obj:
        layout.label(text=_part_label(obj),icon='MESH_DATA')
    row = layout.row(align=True)
    if not saved.get('world_aware') or saved['function'] not in _MANUAL:
        _task(row,'SHAPE','Refit Box' if saved.get('fit_blockout') else 'Shape','MESH_CUBE')
    _task(row,'ROOF','Roof' if obj and obj.get('caelm_layer')=='roof' else 'Edit Roof','MOD_BUILD')
    if not bind:
        row = layout.row(align=True)
        if obj or _roles(collection):
            _task(row,'MATERIAL','Assign Material','MATERIAL')
        if _assembly_choices(collection,obj):
            _task(row,'CONSTRUCTION','Construction','TOOL_SETTINGS')
    if bind or supports_wall_guides(_settings_from_json(saved)):
        _draw_feature(layout,context,collection)
    row = layout.row(align=True)
    _task(row,'CONDITION','Condition','TIME')
    _task(row,'REBUILD','Regenerate','FILE_REFRESH')
    if obj:
        locked = obj.get('caelm_protected',False)
        layout.operator('caelmor.protect_selected',text='Unlock Mesh Edits' if locked else 'Protect Mesh Edits',
                        icon='LOCKED' if locked else 'UNLOCKED')
    conflicts = json.loads(collection.get('caelm_construction_conflicts','[]'))
    if conflicts:
        layout.label(text=f'{len(conflicts)} protected parts need review',icon='ERROR')
    layout.separator()
    layout.operator('caelmor.create_building',text='Create Another Building',icon='ADD')


def _draw_feature(layout,context,collection):
    active = context.view_layer.objects.active
    if active and active.get('caelm_guide'):
        binding = active['caelm_guide']
        layout.label(text=f"{binding['kind'].replace('_',' ').title()} on {binding['side']} wall")
        row = layout.row(align=True)
        row.operator('caelmor.opening_guide',text='Update Feature').action = 'REFRESH'
        row.operator('caelmor.opening_guide',text='Remove',icon='X').action = 'REMOVE'
        layout.operator('caelmor.edit_feature',text='Change Feature Type')
    elif collection:
        if _source_guide(context,collection,active):
            layout.operator('caelmor.select_feature_guide',icon='RESTRICT_SELECT_OFF')
        if any(o.get('caelm_guide_host')==collection for o in context.scene.objects):
            layout.operator('caelmor.opening_guide',text='Update Wall Features',icon='FILE_REFRESH').action = 'REFRESH'
        layout.label(text='Select a guide face or edge to add a feature.')
    elif active and active.type=='MESH' and len(active.data.polygons)<=1:
        from . import _fitted_collection
        if any(_fitted_collection(None,c) for c in context.scene.collection.children_recursive):
            layout.operator('caelmor.edit_feature',text='Add Wall Feature',icon='MESH_PLANE')


class CAELMOR_OT_edit_feature(bpy.types.Operator):
    bl_idname = 'caelmor.edit_feature'
    bl_label = 'Wall Feature'
    bl_description = 'Use the selected face or edge to add or change an opening, post or plaster loss'
    bl_options = {'REGISTER','UNDO'}

    def invoke(self,context,event):
        props = context.scene.caelmor_settings
        obj = context.view_layer.objects.active
        binding = obj.get('caelm_guide') if obj else None
        if binding:
            props.caelm_guide_kind = binding['kind']
            props.caelm_guide_leaf = binding['leaf']
        return context.window_manager.invoke_props_dialog(self,width=340,confirm_text='Apply')

    def draw(self,context):
        obj = context.view_layer.objects.active
        props = context.scene.caelmor_settings
        if not obj or not obj.get('caelm_guide'):
            self.layout.prop(props,'caelm_guide_target',text='Building')
        self.layout.prop(props,'caelm_guide_kind',text='Feature')
        if props.caelm_guide_kind in ('DOOR','ROUND_DOOR'):
            self.layout.prop(props,'caelm_guide_leaf',text='Include Closed Door')

    def execute(self,context):
        return bpy.ops.caelmor.opening_guide(action='APPLY')


def _source_guide(context,collection,obj):
    identity = obj.get('caelm_buffer_id','') if obj else ''
    if '.guide.' not in identity:
        return None
    identifier = identity.split('.guide.',1)[1].split('.',1)[0]
    return next((source for source in context.scene.objects if source.get('caelm_guide_host')==collection
                 and source.get('caelm_guide',{}).get('id')==identifier),None)


class CAELMOR_OT_select_feature_guide(bpy.types.Operator):
    bl_idname = 'caelmor.select_feature_guide'
    bl_label = 'Select Feature Guide'
    bl_description = 'Select the editable shape that places this generated feature'
    bl_options = {'REGISTER','UNDO'}

    def execute(self,context):
        source = _source_guide(context,_selection(context),_part(context))
        if not source or not source.visible_get():
            return _report_error(self,ValueError('Show the source guide in the Outliner first.'))
        _select(context,source)
        return {'FINISHED'}


CLASSES = (CAELMOR_OT_create_building,CAELMOR_OT_edit_building,CAELMOR_OT_edit_feature,
           CAELMOR_OT_select_feature_guide)
