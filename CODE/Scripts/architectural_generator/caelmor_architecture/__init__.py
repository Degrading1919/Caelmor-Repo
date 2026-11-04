"""Caelmor Architectural Generator Blender add-on (Blender API loaded on registration)."""
bl_info = {
    "name": "Caelmor Architectural Generator",
    "author": "Caelmor",
    "version": (0, 12, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Caelmor",
    "description": "Generate editable regional Caelmor buildings",
    "category": "Add Mesh",
}

import json
from .profiles import REGIONS, TYPE_SPECS

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


def _bpy():
    global bpy
    if bpy is None:
        import bpy as _module
        bpy = _module
    return bpy


def _settings_from_props(props):
    from .model import Settings
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


def _active_build(context):
    obj = context.view_layer.objects.active
    if obj:
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


class CAELMOR_PG_Settings(_bpy().types.PropertyGroup if False else object):
    # Replaced with a Blender PropertyGroup class during register; this sentinel
    # prevents bpy from being imported at module import time.
    pass


def _make_classes(b):
    def context_items(self, context):
        region = getattr(self, "caelm_region", "LOWMARK")
        return _CONTEXT_ITEMS.get(region, _CONTEXT_ITEMS["LOWMARK"])

    def reset_context(self, context):
        # Context identifiers are region-scoped. A region change safely returns
        # to that region's default rather than leaving a stale enum identifier.
        self.caelm_context = "AUTO"

    class CAELMOR_PG_Settings(b.types.PropertyGroup):
        caelm_seed: b.props.IntProperty(name="Seed", default=17, min=0, max=2147483647)
        caelm_function: b.props.EnumProperty(name="Building", items=_TYPE_ITEMS, default='FARMHOUSE')
        caelm_region: b.props.EnumProperty(name="Region", items=_REGION_ITEMS, default='LOWMARK', update=reset_context)
        caelm_context: b.props.EnumProperty(name="Local Context", items=context_items, default=0)
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
        caelm_maintenance: b.props.FloatProperty(name="Maintenance", default=.7, min=0.0, max=1.0)
        caelm_age: b.props.FloatProperty(name="Age (years)", default=20.0, min=0.0, max=250.0)
        caelm_use_grammar: b.props.BoolProperty(name="Use Regional Grammar", default=True)
        caelm_world_aware: b.props.BoolProperty(
            name="World Construction Language", default=True,
            description="Arrange regional structural forms as roofed construction volumes")
        caelm_crafted_curves: b.props.BoolProperty(
            name="Crafted Curves", default=True,
            description="Allow swept Lowmark Smithy roofs and joinery, taller Thornfell gate vaults, and continuous Mire bow ribs")
        caelm_seed_massing: b.props.BoolProperty(
            name="Seed Changes Layout", default=True,
            description="Vary massing and roof forms by seed for the Lowmark Smithy and Thornfell Gatehouse")
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
        caelm_width: b.props.FloatProperty(name="Width", default=11.0, min=6.0, max=24.0, unit='LENGTH')
        caelm_depth: b.props.FloatProperty(name="Depth", default=7.0, min=4.0, max=16.0, unit='LENGTH')
        caelm_wing_width: b.props.FloatProperty(name="Wing Width", default=4.2, min=2.5, max=10.0, unit='LENGTH')
        caelm_wing_depth: b.props.FloatProperty(name="Wing Depth", default=4.5, min=2.5, max=12.0, unit='LENGTH')
        caelm_floors: b.props.IntProperty(name="Floors", default=2, min=1, max=3)
        caelm_floor_height: b.props.FloatProperty(name="Floor Height", default=2.65, min=2.4, max=3.8, unit='LENGTH')
        caelm_pitch: b.props.FloatProperty(name="Roof Pitch (degrees)", default=48.0, min=30.0, max=60.0)
        caelm_overhang: b.props.FloatProperty(name="Overhang", default=0.45, min=0.2, max=0.75, unit='LENGTH')
        caelm_detail: b.props.EnumProperty(name="Detail", items=[('LOW', "Low", "Fewer architectural details"), ('MEDIUM', "Medium", "Balanced detail"), ('HIGH', "High", "Full detail")], default='HIGH')
        caelm_window_density: b.props.FloatProperty(name="Window Density", default=1.0, min=0.4, max=1.5)

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
                from .blender_backend import build
                settings = _settings_from_props(context.scene.caelmor_settings)
                collection, metrics = build(settings, origin=context.scene.cursor.location.copy())
                self.report({'INFO'}, f"Generated {collection.name}: {metrics.get('vertices', 0):,} vertices")
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

    class CAELMOR_OT_export(b.types.Operator):
        bl_idname = "caelmor.export"
        bl_label = "Export Building"
        bl_options = {'REGISTER'}
        filepath: b.props.StringProperty(subtype='FILE_PATH')
        filter_glob: b.props.StringProperty(default="*.glb;*.gltf", options={'HIDDEN'})

        @classmethod
        def poll(cls, context):
            return _active_build(context) is not None

        def invoke(self, context, event):
            context.window_manager.fileselect_add(self)
            return {'RUNNING_MODAL'}

        def execute(self, context):
            try:
                from .blender_backend import export_building
                export_building(_active_build(context), self.filepath)
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
            box = layout.box()
            box.label(text="Building", icon='HOME')
            box.prop(p, "caelm_seed")
            box.prop(p, "caelm_function")
            regional = box.box()
            regional.label(text="Region and Household")
            regional.prop(p, "caelm_region")
            regional.prop(p, "caelm_context")
            row = regional.row(align=True)
            row.prop(p, "caelm_wealth")
            row.prop(p, "caelm_craftsmanship")
            regional.prop(p, "caelm_age")
            regional.prop(p, "caelm_maintenance")
            regional.prop(p, "caelm_use_grammar")
            regional.prop(p, "caelm_world_aware")
            curve_row = regional.row()
            curve_row.enabled = p.caelm_world_aware
            curve_row.prop(p, "caelm_crafted_curves")
            if p.caelm_world_aware and (p.caelm_region, p.caelm_function) in (
                    ('LOWMARK', 'SMITHY'), ('THORNFELL', 'GATEHOUSE')):
                regional.prop(p, "caelm_seed_massing")
            roof_row = regional.row()
            roof_row.enabled = not p.caelm_world_aware
            roof_row.prop(p, "caelm_roof_style")
            if p.caelm_world_aware:
                regional.label(text="Regional construction chooses roof forms")
            regional.prop(p, "caelm_geometry_mode")
            regional.operator("caelmor.apply_grammar", icon='FILE_REFRESH')
            box.label(text="Shape inputs" if p.caelm_world_aware else "Manual shape controls (used when grammar is off)")
            if p.caelm_world_aware:
                box.label(text="Regional construction adapts these inputs to its building form")
            col = box.column(align=True)
            col.enabled = not p.caelm_use_grammar
            footprint_row=col.row()
            footprint_row.enabled=not p.caelm_world_aware
            footprint_row.prop(p, "caelm_footprint")
            col.prop(p, "caelm_width")
            col.prop(p, "caelm_depth")
            wings=col.column()
            wings.enabled=not p.caelm_world_aware
            wings.prop(p, "caelm_wing_width")
            wings.prop(p, "caelm_wing_depth")
            col = box.column(align=True)
            col.enabled = not p.caelm_use_grammar
            col.prop(p, "caelm_floors")
            col.prop(p, "caelm_floor_height")
            pitch_row=col.row()
            pitch_row.enabled=not p.caelm_world_aware
            pitch_row.prop(p, "caelm_pitch")
            overhang_row=box.row()
            overhang_row.enabled=not p.caelm_world_aware
            overhang_row.prop(p, "caelm_overhang")
            box.prop(p, "caelm_detail")
            box.prop(p, "caelm_window_density")
            try:
                from .model import resolve_settings, style_for
                from .profiles import TYPE_SPECS, REGIONS
                requested = _settings_from_props(p)
                effective = resolve_settings(requested)
                style = style_for(effective)
                spec = TYPE_SPECS[effective.function]
                region_spec = REGIONS[effective.region]
                info = layout.box()
                info.label(text="World Construction Language" if requested.world_aware else
                           ("Effective Regional Plan" if requested.use_grammar else "Manual Plan"))
                info.label(text=f"{region_spec.label} / {effective.context} · {spec.category.replace('_',' ').title()}")
                if requested.world_aware:
                    descriptions = {
                        "LOWMARK": "Low, broad halls with roofed service ranges",
                        "THORNFELL": "Stepped stone masses with steep, sheltered roofs",
                        "MIRE": "Raised timber volumes with supported connections",
                        "EMBERHOLT": "Terraced masonry blocks with industrial massing",
                    }
                    info.label(text=descriptions.get(effective.region, "Regional roofed construction volumes"))
                    info.label(text="Final bounds and validation appear after generation")
                else:
                    info.label(text=f"{effective.width:.1f} × {effective.depth:.1f} m main block")
                    info.label(text=f"{style.foundation_height + effective.floors * effective.floor_height:.1f} m eaves · {effective.pitch:.0f}° {effective.roof_style.lower()}")
                    info.label(text=f"{style.foundation_mode} foundation · {style.construction} · {style.roof_cover}")
            except (ValueError, KeyError, AttributeError):
                pass
            layout.operator("caelmor.generate", icon='ADD')
            layout.operator("caelmor.protect_selected", icon='LOCKED', text="Protect / Unprotect Selected")
            layout.label(text="Protected buffers retain edits through regeneration.")
            row = layout.row(align=True)
            row.operator("caelmor.load_settings", icon='IMPORT')
            row.operator("caelmor.export", icon='EXPORT')
            layout.label(text="Regenerate generated layers")
            for scope, label in [('ALL', "All Layers"), ('ROOF', "Roof"), ('WINDOWS', "Windows"), ('DETAILS', "Details")]:
                op = layout.operator("caelmor.regenerate", text=label, icon='FILE_REFRESH')
                op.scope = scope
            collection = _active_build(context)
            if collection:
                from .blender_backend import collection_metrics
                m = collection_metrics(collection)
                layout.label(text=f"{m['vertices']:,} verts · {m['objects']} objects")
                layout.label(text=f"Bounds: {m['width']:.1f} × {m['depth']:.1f} × {m['height']:.1f} m")
                raw_diagnostics = collection.get("caelm_validation")
                if raw_diagnostics:
                    try:
                        diagnostics = json.loads(raw_diagnostics)
                        status = "Geometry checks passed" if diagnostics.get("valid") else "Geometry checks found issues"
                        layout.label(text=f"{status} · {diagnostics.get('triangles', 0):,} triangles",
                                     icon='CHECKMARK' if diagnostics.get("valid") else 'ERROR')
                        for issue in diagnostics.get("errors", ())[:2]:
                            layout.label(text=str(issue)[:72], icon='DOT')
                    except (ValueError, TypeError):
                        layout.label(text="Saved geometry diagnostics unavailable", icon='INFO')

    return (CAELMOR_PG_Settings, CAELMOR_OT_apply_grammar, CAELMOR_OT_generate, CAELMOR_OT_load,
            CAELMOR_OT_regenerate, CAELMOR_OT_protect, CAELMOR_OT_export, CAELMOR_PT_main)


def _settings_from_json(data):
    from .model import Settings
    allowed = Settings.__dataclass_fields__.keys()
    values = {key: data[key] for key in allowed if key in data}
    if "use_grammar" not in data: values["use_grammar"] = False
    if "region" not in data: values["region"] = "LOWMARK"
    if "geometry_mode" not in data: values["geometry_mode"] = "SOLID"
    if "roof_style" not in data: values["roof_style"] = "GABLE"
    if "world_aware" not in data: values["world_aware"] = False
    return Settings(**values)


_CLASSES = ()


def register():
    global _CLASSES
    b = _bpy()
    _CLASSES = _make_classes(b)
    for cls in _CLASSES:
        b.utils.register_class(cls)
    b.types.Scene.caelmor_settings = b.props.PointerProperty(type=_CLASSES[0])


def unregister():
    b = _bpy()
    if hasattr(b.types.Scene, "caelmor_settings"):
        del b.types.Scene.caelmor_settings
    for cls in reversed(_CLASSES):
        try:
            b.utils.unregister_class(cls)
        except RuntimeError:
            pass


if __name__ == "__main__":
    register()


