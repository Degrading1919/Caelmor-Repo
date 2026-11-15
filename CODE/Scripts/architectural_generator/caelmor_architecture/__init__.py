"""Caelmor Architectural Generator Blender add-on (Blender API loaded on registration)."""
bl_info = {
    "name": "Caelmor Architectural Generator",
    "author": "Caelmor",
    "version": (0, 19, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Caelmor",
    "description": "Generate editable regional Caelmor buildings",
    "category": "Add Mesh",
}

import json
from dataclasses import replace
from .profiles import REGIONS, TYPE_SPECS
from .construction_library import ASSEMBLIES, FINISH_ROLES, authored_overrides, edit_finish, enum_items, selected

# Keep this package importable by ordinary Python outside Blender.
bpy = None

# Blender enum callbacks keep their strings alive for the lifetime of the
# registered properties. Region/type choices are stable static enums; local
# contexts are region-scoped dynamic enums backed by these persistent tuples.
_TYPE_ITEMS = tuple(
    (code, spec.label,
     f"{getattr(spec, 'building_category', spec.category).replace('_', ' ').title()} · {spec.family.replace('_', ' ')}")
    for code, spec in TYPE_SPECS.items())
_REGION_ITEMS = (
    ('LOWMARK', "Lowmark Vale", "Lowmark Vale regional architecture"),
    ('THORNFELL', "Thornfell Marches", "Thornfell Marches regional architecture"),
    ('MIRE', "Mire of Fallen Banners", "Mire regional architecture"),
    ('EMBERHOLT', "Emberholt Heights", "Emberholt regional architecture"),
)
_CONTEXT_ITEMS = {
    code: (("AUTO", "Regional Default", "Use the region's default local context"),) + tuple(
        (context, label, f"{label} local architectural context")
        for context, label in region.contexts.items())
    for code, region in REGIONS.items()
}
_FLOOR_VOLUMES = [('AUTO', 'First volume', 'Use the first construction volume')]
_FLOOR_VOLUME_CACHE = {}


def _bpy():
    global bpy
    if bpy is None:
        import bpy as _module
        bpy = _module
    return bpy


def _settings_from_props(props):
    from .model import Settings
    overrides = json.loads(props.caelm_construction_overrides or '{}') if props.caelm_construction else None
    if overrides is not None:
        overrides = authored_overrides(props, overrides)
    return Settings(
        seed=props.caelm_seed,
        function=props.caelm_function,
        footprint=props.caelm_footprint,
        width=props.caelm_width,
        depth=props.caelm_depth,
        wing_width=props.caelm_wing_width,
        wing_depth=props.caelm_wing_depth,
        floors=props.caelm_floors,
        floor_height=props.caelm_floor_height,
        floor_separation=props.caelm_floor_separation,
        pitch=props.caelm_pitch,
        overhang=props.caelm_overhang,
        detail=props.caelm_detail,
        window_density=props.caelm_window_density,
        region=props.caelm_region,
        context=props.caelm_context,
        wealth=props.caelm_wealth,
        craftsmanship=props.caelm_craftsmanship,
        maintenance=props.caelm_maintenance,
        age=props.caelm_age,
        use_grammar=props.caelm_use_grammar,
        roof_style=props.caelm_roof_style,
        geometry_mode=props.caelm_geometry_mode,
        world_aware=props.caelm_world_aware,
        crafted_curves=props.caelm_crafted_curves,
        seed_massing=props.caelm_seed_massing,
        construction_overrides=overrides,
        fit_blockout=props.caelm_fit_blockout,
    )


def _set_props(props, settings):
    props.caelm_seed = settings.seed
    props.caelm_function = settings.function
    props.caelm_footprint = settings.footprint
    props.caelm_width = settings.width
    props.caelm_depth = settings.depth
    props.caelm_wing_width = settings.wing_width
    props.caelm_wing_depth = settings.wing_depth
    props.caelm_floors = settings.floors
    props.caelm_floor_height = settings.floor_height
    props.caelm_floor_separation = settings.floor_separation
    props.caelm_pitch = settings.pitch
    props.caelm_overhang = settings.overhang
    props.caelm_detail = settings.detail
    props.caelm_window_density = settings.window_density
    props.caelm_region = settings.region
    props.caelm_context = settings.context
    props.caelm_wealth = settings.wealth
    props.caelm_craftsmanship = settings.craftsmanship
    props.caelm_maintenance = settings.maintenance
    props.caelm_age = settings.age
    props.caelm_use_grammar = settings.use_grammar
    props.caelm_roof_style = settings.roof_style
    props.caelm_geometry_mode = settings.geometry_mode
    props.caelm_world_aware = settings.world_aware
    props.caelm_crafted_curves = settings.crafted_curves
    props.caelm_seed_massing = settings.seed_massing
    props.caelm_fit_blockout = settings.fit_blockout
    props.caelm_construction = settings.construction_overrides is not None
    original = settings.construction_overrides or {}
    props.caelm_construction_overrides = json.dumps(original, sort_keys=True)
    roles = original.get('by_role',{})
    for name,(role,_,options) in ASSEMBLIES.items():
        setattr(props, 'caelm_assembly_'+name, selected(options,roles.get(role,{})))
    props.caelm_edit_finish = False
    props.caelm_finish_material = None
    props.caelm_finish_rotation = 'AUTO'


def _active_build(context):
    obj = context.view_layer.objects.active
    if obj:
        guide_host = obj.get('caelm_guide_host')
        if guide_host is not None and guide_host.get('caelm_build'):
            return guide_host
        for collection in obj.users_collection:
            if collection.get("caelm_build"):
                return collection
        # A manual or unrelated selected object must never redirect an operation
        # to some other Caelmor collection in the scene.
        return None
    builds = [c for c in context.scene.collection.children if c.get("caelm_build")]
    if len(builds) == 1:
        return builds[0]
    return None


def _report_error(operator, exc):
    operator.report({'ERROR'}, str(exc))
    return {'CANCELLED'}


def _active_component(context):
    obj = context.view_layer.objects.active
    if obj and obj.get('caelm_generated') and not obj.get('caelm_collider') and _active_build(context):
        return obj.get('caelm_component_id')
    return None


def _fitted_collection(_self, collection):
    return bool(collection.get('caelm_build') and collection.get('caelm_blockout_source'))


class CAELMOR_PG_Settings(_bpy().types.PropertyGroup if False else object):
    # Replaced with a Blender PropertyGroup class during register; this sentinel
    # prevents bpy from being imported at module import time.
    pass


def _make_classes(b):
    def floor_volume_items(self, context):
        collection = _active_build(context) if context else None
        schedule = []
        if collection and collection.get('caelm_floor_schedule'):
            schedule = [(v['volume'], v['count']) for v in json.loads(collection['caelm_floor_schedule']) if v['count'] > 0]
        key = tuple(schedule)
        if key not in _FLOOR_VOLUME_CACHE:
            _FLOOR_VOLUME_CACHE[key] = _FLOOR_VOLUMES+[(volume,volume,f'Floors 0–{count-1}') for volume,count in schedule]
        return _FLOOR_VOLUME_CACHE[key]

    def context_items(self, context):
        region = getattr(self, "caelm_region", "LOWMARK")
        return _CONTEXT_ITEMS.get(region, _CONTEXT_ITEMS["LOWMARK"])

    def reset_context(self, context):
        # Context identifiers are region-scoped. A region change safely returns
        # to that region's default rather than leaving a stale enum identifier.
        self.caelm_context = "AUTO"

    class CAELMOR_PG_Settings(b.types.PropertyGroup):
        caelm_seed: b.props.IntProperty(name="Seed", default=17, min=0, max=2147483647,
            description="Reproduce construction details and variation for the same inputs")
        caelm_function: b.props.EnumProperty(name="Building", items=_TYPE_ITEMS, default='FARMHOUSE',
            description="Choose the building's function and its corresponding construction program")
        caelm_region: b.props.EnumProperty(name="Region", items=_REGION_ITEMS, default='LOWMARK', update=reset_context,
            description="Set the regional construction, surface and roof defaults")
        caelm_context: b.props.EnumProperty(name="Local Context", items=context_items, default=0,
            description="Use the regional default or a specific local building tradition")
        caelm_wealth: b.props.EnumProperty(name="Wealth", items=[
            ('MODEST', "Modest", "Multipurpose household space and restrained local investment"),
            ('ESTABLISHED', "Established", "Investment in working space, storage and household capacity"),
            ('AFFLUENT', "Affluent", "Investment in private rooms, service spaces and sheltered access; craftsmanship is separate"),
        ], default='ESTABLISHED')
        caelm_craftsmanship: b.props.EnumProperty(name="Craftsmanship", items=[
            ('ROUGH', "Rough", "Rough-cut and irregular workmanship"),
            ('STANDARD', "Standard", "Competent everyday workmanship"),
            ('FINE', "Fine", "Careful joinery and finish"),
        ], default='STANDARD')
        caelm_maintenance: b.props.FloatProperty(name="Maintenance", default=.7, min=0.0, max=1.0,
            description="How well the building has been kept and repaired")
        caelm_age: b.props.FloatProperty(name="Age (years)", default=20.0, min=0.0, max=250.0,
            description="Years of exposure for weathering and appropriate construction details")
        caelm_use_grammar: b.props.BoolProperty(name="Use Regional Dimensions", default=True,
            description="Choose initial dimensions and floor count from the region and function")
        caelm_world_aware: b.props.BoolProperty(
            name="World Construction Language", default=True,
            description="Arrange regional structural forms as roofed construction volumes")
        caelm_crafted_curves: b.props.BoolProperty(
            name="Crafted Curves", default=True,
            description="Allow swept Lowmark Smithy roofs and joinery, taller Thornfell gate vaults, and continuous Mire bow ribs")
        caelm_seed_massing: b.props.BoolProperty(
            name="Seed Changes Layout", default=True,
            description="Vary massing and roof forms by seed for the Lowmark Smithy and Thornfell Gatehouse")
        caelm_construction: b.props.BoolProperty(
            name="Construction Treatments", default=True,
            description="Resolve construction by component role; legacy buildings load with this off")
        caelm_construction_overrides: b.props.StringProperty(
            name="Saved Construction Overrides", default="{}", options={'HIDDEN'})
        caelm_fit_blockout: b.props.BoolProperty(options={'HIDDEN'})
        caelm_edit_finish: b.props.BoolProperty(name="Set a finish on this role", options={'HIDDEN'})
        caelm_finish_scope: b.props.EnumProperty(name="Apply To", items=[
            ('ROLE', 'Construction role', 'Use the finish across all components of that role'),
            ('COMPONENT', 'Selected component', 'Use the finish on the selected semantic component across its floor sections'),
        ])
        caelm_finish_role: b.props.EnumProperty(name="Construction Role", items=[
            (role, *label_help) for role, label_help in FINISH_ROLES.items()])
        caelm_finish_material: b.props.PointerProperty(name="Scene Material", type=b.types.Material,
            description="Use a Blender material already loaded in this scene, including materials created by Substance")
        caelm_finish_rotation: b.props.EnumProperty(name='Metric UV Rotation', items=[
            ('AUTO', 'Automatic', 'Use the component’s generated UV orientation'),
            ('90', '90°', 'Rotate UV0 for this component’s scene material'),
            ('180', '180°', 'Reverse UV0 for this component’s scene material'),
            ('270', '270°', 'Rotate UV0 in the opposite direction'),
        ])
        caelm_component_joinery: b.props.EnumProperty(name='Timber Profile', items=[
            ('AUTO', 'Inherit', 'Use the role override or regional default for this component'),
            ('hewn_pegged', 'Hewn and pegged', 'Use worked timber and pegged intersections'),
            ('squared_housed', 'Squared and housed', 'Use straighter members with housed bearing shoulders'),
        ])
        caelm_guide_target: b.props.PointerProperty(name='Target Cottage', type=b.types.Collection,
            poll=_fitted_collection, description='Choose the box-fitted cottage whose wall will receive the active face')
        caelm_guide_kind: b.props.EnumProperty(name='Opening Type', items=[
            ('DOOR', 'Door', 'Ground-floor rectangular door with jambs, head and a stepped approach'),
            ('WINDOW', 'Window', 'Rectangular opening with casing, drained sill, shutters and glazing'),
            ('ROUND_DOOR', 'Rounded Door', 'Arched wall cut shaped from a rectangle or a symmetric curved face'),
        ])
        caelm_guide_leaf: b.props.BoolProperty(name='Closed Leaf', default=True,
            description='Generate a closed planked leaf and keep this static passage closed in collision')
        caelm_roof_style: b.props.EnumProperty(name="Roof Style", items=[
            ('AUTO', "Regional / Type Default", "Select a suitable roof by type and region"),
            ('GABLE', "Gable", "Gabled roof"), ('HIP', "Hip", "Hipped roof")], default='AUTO')
        caelm_geometry_mode: b.props.EnumProperty(name="Geometry", items=[
            ('SOLID', "Solid", "Closed solids with full roof construction"),
            ('EFFICIENT', "Efficient", "Reduced hidden roof geometry")], default='SOLID')
        caelm_footprint: b.props.EnumProperty(name="Footprint", items=[
            ('RECT', "Rectangular", "Single rectangle"), ('L', "L", "Two joined wings"),
            ('T', "T", "Three joined wings"), ('U', "U", "Three sides around a court"),
        ], default='L')
        caelm_width: b.props.FloatProperty(name="Width", default=11.0, min=6.0, max=24.0, unit='LENGTH',
            description="Main body span along its frontage, before ornament and roof overhang")
        caelm_depth: b.props.FloatProperty(name="Depth", default=7.0, min=4.0, max=16.0, unit='LENGTH',
            description="Main body depth from the front wall to the back wall")
        caelm_wing_width: b.props.FloatProperty(name="Wing Width", default=4.2, min=2.5, max=10.0, unit='LENGTH')
        caelm_wing_depth: b.props.FloatProperty(name="Wing Depth", default=4.5, min=2.5, max=12.0, unit='LENGTH')
        caelm_floors: b.props.IntProperty(name="Floors", default=2, min=1, max=3,
            description="Choose the floor count before fitting a box. The fit divides usable wall height into that many floors")
        caelm_floor_separation: b.props.BoolProperty(name="Floor-separated visuals", default=True,
            description="Partition visual meshes by volume and floor; leave collision independent")
        caelm_preview_floor: b.props.IntProperty(name="Simulated floor (-1 = exterior)", default=-1, min=-1, max=2)
        caelm_preview_volume: b.props.EnumProperty(name="Construction volume", items=floor_volume_items)
        caelm_floor_height: b.props.FloatProperty(name="Floor Height", default=2.65, min=2.4, max=3.8, unit='LENGTH',
            description="Storey height above the foundation. Box fitting derives it from the top of the source box")
        caelm_pitch: b.props.FloatProperty(name="Roof Pitch (degrees)", default=48.0, min=30.0, max=60.0)
        caelm_overhang: b.props.FloatProperty(name="Overhang", default=0.45, min=0.2, max=0.75, unit='LENGTH')
        caelm_detail: b.props.EnumProperty(name="Detail", items=[('LOW', "Low", "Fewer architectural details"), ('MEDIUM', "Medium", "Balanced detail"), ('HIGH', "High", "Full detail")], default='HIGH')
        caelm_window_density: b.props.FloatProperty(name="Window Density", default=1.0, min=0.4, max=1.5)

    for name,(_,label,options) in ASSEMBLIES.items():
        CAELMOR_PG_Settings.__annotations__['caelm_assembly_'+name] = b.props.EnumProperty(
            name=label, items=([('AUTO','Modeled','Use the established modeled construction'),
                                *enum_items(options)[1:]] if name.endswith('_depth')
                               else enum_items(options)), default='AUTO')

    class CAELMOR_OT_apply_grammar(b.types.Operator):
        bl_idname = "caelmor.apply_grammar"
        bl_label = "Apply Grammar to Shape Controls"
        bl_options = {'REGISTER', 'UNDO'}

        def execute(self, context):
            try:
                from .model import resolve_settings
                props = context.scene.caelmor_settings
                effective = resolve_settings(_settings_from_props(props))
                _set_props(props, effective)
                self.report({'INFO'}, "Applied regional massing to shape controls")
                return {'FINISHED'}
            except Exception as exc:
                return _report_error(self, exc)

    class CAELMOR_OT_generate(b.types.Operator):
        bl_idname = "caelmor.generate"
        bl_label = "Generate New"
        bl_options = {'REGISTER', 'UNDO'}

        def execute(self, context):
            try:
                from .blender_backend import build, load_settings
                props = context.scene.caelmor_settings
                settings = replace(_settings_from_props(props), fit_blockout=False)
                collection, metrics = build(settings, origin=context.scene.cursor.location.copy())
                _set_props(props, _settings_from_json(load_settings(collection)))
                self.report({'INFO'}, f"Generated {collection.name}: {metrics.get('vertices', 0):,} vertices")
                return {'FINISHED'}
            except Exception as exc:
                return _report_error(self, exc)

    class CAELMOR_OT_fit_blockout(b.types.Operator):
        bl_idname = 'caelmor.fit_blockout'
        bl_label = 'Generate from Selected Box'
        bl_description = 'Fit a Lowmark Cottage to the selected box, using its top as eave height and local −Y as frontage'
        bl_options = {'REGISTER', 'UNDO'}
        refit: b.props.BoolProperty(default=False, options={'HIDDEN'})

        def execute(self, context):
            try:
                from .blockout import fit
                from .blender_backend import build, load_settings
                props = context.scene.caelmor_settings
                collection = _active_build(context) if self.refit else None
                if self.refit:
                    source = collection.get('caelm_blockout_source') if collection else None
                    if source is None or context.scene.objects.get(source.name) != source:
                        raise ValueError('Select a building whose source box is in this scene')
                    settings = _settings_from_json(load_settings(collection))
                else:
                    settings = _settings_from_props(props)
                    source = context.view_layer.objects.active
                context.view_layer.update()
                fitted, placement = fit(settings, source)
                collection, _ = build(fitted, collection=collection, placement=placement)
                collection['caelm_blockout_source'] = source
                _set_props(props, _settings_from_json(load_settings(collection)))
                props.caelm_guide_target = collection
                self.report({'INFO'}, f'{collection.name} fitted to {source.name}')
                return {'FINISHED'}
            except Exception as exc:
                return _report_error(self, exc)

    class CAELMOR_OT_stage_finish(b.types.Operator):
        bl_idname = 'caelmor.stage_finish'
        bl_label = 'Stage Finish'
        bl_description = 'Save this finish choice in the panel settings, ready for Generate or Regenerate All'
        bl_options = {'REGISTER', 'UNDO'}
        clear: b.props.BoolProperty(default=False, options={'HIDDEN'})

        def execute(self, context):
            try:
                props = context.scene.caelmor_settings
                if not props.caelm_construction:
                    raise ValueError('Enable construction treatments to assign scene materials')
                scope = 'by_role'
                key = props.caelm_finish_role
                if props.caelm_finish_scope == 'COMPONENT':
                    scope = 'by_component'
                    key = _active_component(context)
                    if key is None:
                        raise ValueError('Select a generated construction component')
                material = props.caelm_finish_material
                if not self.clear and material is None:
                    raise ValueError('Choose a scene material before staging its finish')
                current = _settings_from_props(props).construction_overrides
                draft = edit_finish(current, scope, key, None if self.clear else material.name,
                                    props.caelm_finish_rotation)
                props.caelm_construction_overrides = json.dumps(draft, sort_keys=True)
                props.caelm_edit_finish = False
                self.report({'INFO'}, 'Finish change staged. Generate or Regenerate All to apply.')
                return {'FINISHED'}
            except Exception as exc:
                return _report_error(self, exc)

    class CAELMOR_OT_stage_joinery(b.types.Operator):
        bl_idname = 'caelmor.stage_joinery'
        bl_label = 'Stage Timber Profile'
        bl_description = 'Store the selected structural timber profile as a component input for Regenerate All'
        bl_options = {'REGISTER', 'UNDO'}

        @classmethod
        def poll(cls, context):
            obj = context.view_layer.objects.active
            return bool(_active_component(context) and obj.get('caelm_treatment') == 'structural_timber'
                        and context.scene.caelmor_settings.caelm_construction)

        def execute(self, context):
            try:
                props = context.scene.caelmor_settings
                draft = _settings_from_props(props).construction_overrides
                key = _active_component(context)
                entries = draft.setdefault('by_component', {})
                fields = entries.setdefault(key, {})
                choice = props.caelm_component_joinery
                if choice == 'AUTO':
                    fields.pop('variant', None)
                else:
                    fields['variant'] = choice
                if not fields:
                    entries.pop(key)
                if not entries:
                    draft.pop('by_component')
                props.caelm_construction_overrides = json.dumps(draft, sort_keys=True)
                props.caelm_edit_finish = False
                self.report({'INFO'}, 'Timber profile staged. Regenerate All to apply.')
                return {'FINISHED'}
            except Exception as exc:
                return _report_error(self, exc)

    class CAELMOR_OT_load(b.types.Operator):
        bl_idname = "caelmor.load_settings"
        bl_label = "Load Selected Settings"
        bl_options = {'REGISTER', 'UNDO'}

        @classmethod
        def poll(cls, context):
            return _active_build(context) is not None

        def execute(self, context):
            try:
                from .blender_backend import load_settings
                data = load_settings(_active_build(context))
                settings = _settings_from_json(data)
                _set_props(context.scene.caelmor_settings, settings)
                self.report({'INFO'}, "Loaded building settings")
                return {'FINISHED'}
            except Exception as exc:
                return _report_error(self, exc)

    class CAELMOR_OT_regenerate(b.types.Operator):
        bl_idname = "caelmor.regenerate"
        bl_label = "Regenerate Selected"
        bl_options = {'REGISTER', 'UNDO'}
        scope: b.props.EnumProperty(name="Scope", items=[
            ('ALL', "All", "Replace all generated layers"),
            ('ROOF', "Roof", "Replace roof layer"),
            ('WINDOWS', "Windows", "Replace windows and doors"),
            ('DETAILS', "Details", "Replace architectural details"),
        ], default='ALL')

        @classmethod
        def poll(cls, context):
            return _active_build(context) is not None

        def execute(self, context):
            try:
                from .blender_backend import build
                settings = _settings_from_props(context.scene.caelmor_settings)
                collection = _active_build(context)
                _, metrics = build(settings, collection=collection,
                                   layers=None if self.scope == 'ALL' else self.scope)
                if settings.fit_blockout:
                    from .blender_backend import load_settings
                    props = context.scene.caelmor_settings
                    saved = load_settings(collection).get('construction_overrides')
                    if saved != settings.construction_overrides:
                        props.caelm_construction_overrides = json.dumps(saved or {}, sort_keys=True)
                        props.caelm_edit_finish = False
                self.report({'INFO'}, f"Regenerated {self.scope.lower()}: {metrics.get('vertices', 0):,} vertices")
                return {'FINISHED'}
            except Exception as exc:
                return _report_error(self, exc)

    class CAELMOR_OT_protect(b.types.Operator):
        bl_idname = "caelmor.protect_selected"
        bl_label = "Protect Selected"
        bl_description = "Keep this generated object through future regeneration and include it in export"
        bl_options = {'REGISTER', 'UNDO'}

        @classmethod
        def poll(cls, context):
            obj = context.view_layer.objects.active
            return bool(obj and obj.get("caelm_generated") and not obj.get("caelm_collider"))

        def execute(self, context):
            obj = context.view_layer.objects.active
            obj["caelm_protected"] = not obj.get("caelm_protected", False)
            state = "protected from" if obj["caelm_protected"] else "available to"
            self.report({'INFO'}, f"{obj.name} is now {state} regeneration")
            return {'FINISHED'}

    class CAELMOR_OT_opening_guide(b.types.Operator):
        bl_idname = 'caelmor.opening_guide'
        bl_label = 'Apply Opening Guide'
        bl_description = 'Use a single planar face to rebuild the host opening, adjacent framing and collision'
        bl_options = {'REGISTER', 'UNDO'}
        action: b.props.EnumProperty(items=[
            ('APPLY', 'Apply', 'Attach the selected face or change its type'),
            ('REFRESH', 'Refresh', 'Use the current positions and outlines of this building’s guides'),
            ('REMOVE', 'Remove', 'Detach the selected guide and restore the generated wall'),
        ])

        def execute(self, context):
            try:
                from .blender_backend import build, load_settings
                from .guide_backend import HOST, apply_binding, propose
                props = context.scene.caelmor_settings
                source = context.view_layer.objects.active
                host = source.get(HOST) if source else None
                collection = host or (_active_build(context) if self.action == 'REFRESH' else props.caelm_guide_target)
                if not collection or not collection.get('caelm_build'):
                    raise ValueError('Choose the fitted cottage in Target Cottage or select one of its attached guides')
                if not any(c == collection for c in context.scene.collection.children_recursive):
                    raise ValueError('The target cottage must be in the current scene')
                settings = _settings_from_json(load_settings(collection))
                if not settings.fit_blockout:
                    raise ValueError('Opening guides require a box-fitted Lowmark Cottage')
                context.view_layer.update()
                edit = None
                if self.action == 'APPLY':
                    if source is None or not source.select_get():
                        raise ValueError('Select the source face in Object Mode')
                    edit = (source, propose(collection, source, settings, props.caelm_guide_kind, props.caelm_guide_leaf))
                elif self.action == 'REMOVE':
                    if host is None:
                        raise ValueError('Select an attached guide to remove it')
                    edit = (source, None)
                build(settings, collection=collection, guide_edit=edit, guide_refresh=True)
                if edit:
                    apply_binding(collection, *edit)
                # Guide operations use the target's applied settings. Retire
                # only inputs for removed assemblies without discarding the
                # artist's other staged changes in the panel.
                prior = (settings.construction_overrides or {}).get('by_component', {})
                saved = (load_settings(collection).get('construction_overrides') or {}).get('by_component', {})
                retired = prior.keys() - saved.keys()
                if retired:
                    draft = json.loads(props.caelm_construction_overrides or '{}')
                    if 'by_component' in draft:
                        for key in retired:
                            draft['by_component'].pop(key, None)
                        if not draft['by_component']:
                            draft.pop('by_component')
                        props.caelm_construction_overrides = json.dumps(draft, sort_keys=True)
                props.caelm_guide_target = collection
                if source and (edit or host) and source.visible_get():
                    for obj in context.selected_objects:
                        obj.select_set(False)
                    source.select_set(True)
                    context.view_layer.objects.active = source
                self.report({'INFO'}, 'Applied wall opening guides')
                return {'FINISHED'}
            except Exception as exc:
                return _report_error(self, exc)

    class CAELMOR_OT_floor_preview(b.types.Operator):
        bl_idname = 'caelmor.floor_preview'
        bl_label = 'Apply Floor Preview'
        bl_options = {'REGISTER', 'UNDO'}

        @classmethod
        def poll(cls, context):
            collection = _active_build(context)
            return bool(collection and collection.get('caelm_floor_contract'))

        def execute(self, context):
            try:
                from .floor_backend import preview
                props = context.scene.caelmor_settings
                preview(_active_build(context), props.caelm_preview_floor,
                        None if props.caelm_preview_volume == 'AUTO' else props.caelm_preview_volume)
                return {'FINISHED'}
            except Exception as exc:
                return _report_error(self, exc)

    class CAELMOR_OT_export(b.types.Operator):
        bl_idname = "caelmor.export"
        bl_label = "Export Building"
        bl_description = "Export visual geometry, collision and metadata. Scene materials need glTF-compatible PBR inputs"
        bl_options = {'REGISTER'}
        filepath: b.props.StringProperty(subtype='FILE_PATH')
        filter_glob: b.props.StringProperty(default="*.glb;*.gltf", options={'HIDDEN'})
        construction_metadata: b.props.BoolProperty(
            name="Construction Metadata", default=False,
            description="Add optional construction settings and per-object provenance to the sidecar")

        def draw(self, context):
            self.layout.prop(self, "construction_metadata")

        @classmethod
        def poll(cls, context):
            return _active_build(context) is not None

        def invoke(self, context, event):
            context.window_manager.fileselect_add(self)
            return {'RUNNING_MODAL'}

        def execute(self, context):
            try:
                from .blender_backend import export_building
                export_building(_active_build(context), self.filepath,
                                construction_metadata=self.construction_metadata)
                self.report({'INFO'}, "Exported building and metadata manifest")
                return {'FINISHED'}
            except Exception as exc:
                return _report_error(self, exc)

    class CAELMOR_PT_main(b.types.Panel):
        bl_label = "Caelmor Architecture"
        bl_idname = "CAELMOR_PT_main"
        bl_space_type = 'VIEW_3D'
        bl_region_type = 'UI'
        bl_category = "Caelmor"

        def draw(self, context):
            layout = self.layout
            p = context.scene.caelmor_settings
            collection = _active_build(context)
            source = collection.get('caelm_blockout_source') if collection else None

            def section(name, icon, *, collapsed=False):
                header, body = layout.panel('caelmor_' + name.lower(), default_closed=collapsed)
                header.label(text=name, icon=icon)
                return body

            if building := section('Building', 'HOME'):
                for key in ('function', 'region', 'context', 'seed', 'wealth'):
                    building.prop(p, 'caelm_' + key)
                building.operator('caelmor.generate', icon='ADD')
                if collection:
                    building.operator('caelmor.load_settings', icon='IMPORT')
                    building.operator('caelmor.regenerate', text='Regenerate All', icon='FILE_REFRESH')

            if shape := section('Shape', 'MESH_CUBE'):
                if (p.caelm_region, p.caelm_function) == ('LOWMARK', 'COTTAGE'):
                    shape.operator('caelmor.fit_blockout', icon='MESH_CUBE')
                    shape.label(text='Box top = eaves · local −Y = frontage')
                    if p.caelm_use_grammar and not p.caelm_fit_blockout:
                        shape.prop(p, 'caelm_floors', text='Floors for Box Fit')
                if source:
                    shape.label(text=f'Source box: {source.name}')
                    shape.operator('caelmor.fit_blockout', text='Refit from Source Box',
                                   icon='FILE_REFRESH').refit = True
                fitted = p.caelm_fit_blockout
                modes = shape.column()
                modes.enabled = not fitted
                modes.prop(p, 'caelm_use_grammar')
                modes.prop(p, 'caelm_world_aware')
                modes.operator('caelmor.apply_grammar', icon='FILE_REFRESH')
                if fitted:
                    shape.label(text='Dimensions come from the source box')
                dimensions = shape.column(align=True)
                dimensions.enabled = not (p.caelm_use_grammar or fitted)
                for key in ('width', 'depth', 'floors', 'floor_height'):
                    dimensions.prop(p, 'caelm_' + key)
                if not p.caelm_world_aware:
                    dimensions.prop(p, 'caelm_footprint')
                    if p.caelm_footprint != 'RECT':
                        dimensions.prop(p, 'caelm_wing_width')
                        dimensions.prop(p, 'caelm_wing_depth')
                    dimensions.prop(p, 'caelm_pitch')
                    shape.prop(p, 'caelm_roof_style')
                    shape.prop(p, 'caelm_overhang')
                else:
                    shape.label(text='Regional construction chooses roof forms')
                    shape.prop(p, 'caelm_crafted_curves')
                    if (p.caelm_region, p.caelm_function) in (('LOWMARK', 'SMITHY'), ('THORNFELL', 'GATEHOUSE')):
                        shape.prop(p, 'caelm_seed_massing')

            if construction := section('Construction', 'MOD_BUILD', collapsed=True):
                construction.prop(p, 'caelm_construction')
                if p.caelm_construction:
                    for name in ASSEMBLIES:
                        if not name.endswith('_depth'):
                            construction.prop(p, 'caelm_assembly_' + name)
                    construction.prop(p, 'caelm_craftsmanship')

            if materials := section('Materials', 'MATERIAL'):
                if p.caelm_construction:
                    materials.prop(p, 'caelm_finish_scope')
                    if p.caelm_finish_scope == 'ROLE':
                        materials.prop(p, 'caelm_finish_role')
                        scope, key = 'by_role', p.caelm_finish_role
                    else:
                        scope, key = 'by_component', _active_component(context)
                        materials.label(text=key or 'Select a generated component')
                        materials.prop(p, 'caelm_finish_rotation')
                    materials.prop(p, 'caelm_finish_material')
                    saved = json.loads(p.caelm_construction_overrides or '{}')
                    fields = saved.get(scope, {}).get(key, {})
                    finish = fields.get('finish', '')
                    if finish:
                        turn = fields.get('uv_rotation')
                        caption = finish.removeprefix('material:')
                        materials.label(text=f'Panel choice: {caption}' + (f' · {turn}°' if turn else ''))
                    row = materials.row(align=True)
                    row.enabled = key is not None
                    stage = row.row()
                    stage.enabled = p.caelm_finish_material is not None
                    stage.operator('caelmor.stage_finish', icon='CHECKMARK')
                    clear = row.row()
                    clear.enabled = bool(finish)
                    clear.operator('caelmor.stage_finish', text='Clear Override').clear = True
                    materials.label(text='Generate or Regenerate All to apply')
                else:
                    materials.label(text='Enable Construction Treatments for scene finishes')

            if components := section('Components', 'OBJECT_DATA', collapsed=True):
                components.prop(p, 'caelm_window_density')
                if collection:
                    active = context.view_layer.objects.active
                    key = _active_component(context)
                    if key and active.get('caelm_treatment') == 'structural_timber' and p.caelm_construction:
                        saved = json.loads(p.caelm_construction_overrides or '{}')
                        variant = saved.get('by_component', {}).get(key, {}).get('variant')
                        components.label(text=f'Selected: {key}')
                        if variant:
                            components.label(text=f'Panel choice: {variant.replace("_", " ").capitalize()}')
                        components.prop(p, 'caelm_component_joinery')
                        components.operator('caelmor.stage_joinery')
                    components.operator('caelmor.protect_selected', icon='LOCKED',
                                        text='Protect / Unprotect Selected')
                    row = components.row(align=True)
                    for scope, label in [('ROOF', 'Roof'), ('WINDOWS', 'Openings'), ('DETAILS', 'Details')]:
                        row.operator('caelmor.regenerate', text=label, icon='FILE_REFRESH').scope = scope
                    conflicts = json.loads(collection.get('caelm_construction_conflicts', '[]'))
                    if conflicts:
                        components.label(text=f'{len(conflicts)} protected sections need review', icon='ERROR')

            if openings := section('Opening Guides', 'MESH_PLANE', collapsed=True):
                active = context.view_layer.objects.active
                binding = active.get('caelm_guide') if active else None
                if binding:
                    openings.label(text=f"Attached to {binding['side']} wall · {binding['kind'].replace('_', ' ').title()}")
                else:
                    openings.prop(p, 'caelm_guide_target')
                openings.prop(p, 'caelm_guide_kind')
                if p.caelm_guide_kind != 'WINDOW':
                    openings.prop(p, 'caelm_guide_leaf')
                openings.operator('caelmor.opening_guide', icon='MOD_BUILD').action = 'APPLY'
                if collection:
                    openings.operator('caelmor.opening_guide', text='Regenerate Guides', icon='FILE_REFRESH').action = 'REFRESH'
                if binding:
                    openings.operator('caelmor.opening_guide', text='Remove Guide', icon='X').action = 'REMOVE'

            if condition := section('Condition', 'TIME', collapsed=True):
                condition.prop(p, 'caelm_age')
                condition.prop(p, 'caelm_maintenance')

            if geometry := section('Geometry', 'MESH_DATA', collapsed=True):
                geometry.prop(p, 'caelm_geometry_mode')
                geometry.prop(p, 'caelm_detail')
                if p.caelm_construction:
                    depth = geometry.column()
                    depth.enabled = p.caelm_geometry_mode == 'EFFICIENT'
                    depth.prop(p, 'caelm_assembly_roof_depth')
                    depth.prop(p, 'caelm_assembly_wall_depth')
                geometry.prop(p, 'caelm_floor_separation')
                if collection and collection.get('caelm_floor_contract'):
                    box = geometry.box()
                    box.label(text='Visual floor preview · collision unchanged')
                    box.prop(p, 'caelm_preview_volume')
                    box.prop(p, 'caelm_preview_floor')
                    for host in json.loads(collection['caelm_floor_schedule']):
                        box.label(text=f"{host['volume']}: floors 0–{host['count']-1}" if host['count']
                                  else f"{host['volume']}: exterior access (always visible)")
                    box.operator('caelmor.floor_preview')

            if export := section('Export', 'EXPORT', collapsed=True):
                export.operator('caelmor.export', icon='EXPORT')
                if collection:
                    from .blender_backend import collection_metrics
                    metrics = collection_metrics(collection)
                    export.label(text=f"{metrics['vertices']:,} verts · {metrics['objects']} objects")
                    export.label(text=f"Bounds: {metrics['width']:.1f} × {metrics['depth']:.1f} × {metrics['height']:.1f} m")
                    diagnostics = json.loads(collection.get('caelm_validation', '{}'))
                    if diagnostics:
                        status = 'Geometry checks passed' if diagnostics.get('valid') else 'Geometry issues found'
                        export.label(text=f"{status} · {diagnostics.get('triangles', 0):,} triangles",
                                     icon='CHECKMARK' if diagnostics.get('valid') else 'ERROR')
                        for issue in diagnostics.get('errors', ())[:2]:
                            export.label(text=str(issue)[:72], icon='DOT')

    return (CAELMOR_PG_Settings, CAELMOR_OT_apply_grammar, CAELMOR_OT_generate, CAELMOR_OT_load,
            CAELMOR_OT_regenerate, CAELMOR_OT_protect, CAELMOR_OT_floor_preview, CAELMOR_OT_export,
            CAELMOR_OT_fit_blockout, CAELMOR_OT_stage_finish, CAELMOR_OT_stage_joinery, CAELMOR_OT_opening_guide, CAELMOR_PT_main)


def _settings_from_json(data):
    from .model import Settings
    allowed = Settings.__dataclass_fields__.keys()
    values = {key: data[key] for key in allowed if key in data}
    if "use_grammar" not in data: values["use_grammar"] = False
    if "region" not in data: values["region"] = "LOWMARK"
    if "geometry_mode" not in data: values["geometry_mode"] = "SOLID"
    if "roof_style" not in data: values["roof_style"] = "GABLE"
    if "world_aware" not in data: values["world_aware"] = False
    if 'floor_separation' not in data: values['floor_separation'] = False
    return Settings(**values)


_CLASSES = ()


def register():
    global _CLASSES
    b = _bpy()
    from .roof_autocomplete import CLASSES, RoofSettings
    _CLASSES = _make_classes(b) + CLASSES
    for cls in _CLASSES:
        b.utils.register_class(cls)
    b.types.Scene.caelmor_settings = b.props.PointerProperty(type=_CLASSES[0])
    b.types.Scene.caelm_roof_settings = b.props.PointerProperty(type=RoofSettings)


def unregister():
    b = _bpy()
    if hasattr(b.types.Scene, 'caelm_roof_settings'):
        del b.types.Scene.caelm_roof_settings
    if hasattr(b.types.Scene, "caelmor_settings"):
        del b.types.Scene.caelmor_settings
    for cls in reversed(_CLASSES):
        try:
            b.utils.unregister_class(cls)
        except RuntimeError:
            pass


if __name__ == "__main__":
    register()


