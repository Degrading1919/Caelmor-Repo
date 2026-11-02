"""Caelmor Architectural Generator Blender add-on (Blender API loaded on registration)."""
bl_info = {
    "name": "Caelmor Architectural Generator",
    "author": "Caelmor",
    "version": (0, 2, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Caelmor",
    "description": "Generate editable, metre-scale Lowmark buildings",
    "category": "Add Mesh",
}

import json

# Keep this package importable by ordinary Python outside Blender.
bpy = None


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
    class CAELMOR_PG_Settings(b.types.PropertyGroup):
        caelm_seed: b.props.IntProperty(name="Seed", default=17, min=0, max=2147483647)
        caelm_function: b.props.EnumProperty(name="Building", items=[
            ('FARMHOUSE', "Farmhouse", "Rural dwelling"),
            ('BARN', "Barn", "Agricultural outbuilding"),
            ('GRAIN_STORE', "Grain Store", "Small rural grain store"),
            ('MILLER', "Miller", "Miller rural home and workplace"),
            ('INN', "Inn", "Small rural inn"),
        ], default='FARMHOUSE')
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
            box.prop(p, "caelm_footprint")
            col = box.column(align=True)
            col.prop(p, "caelm_width")
            col.prop(p, "caelm_depth")
            col.prop(p, "caelm_wing_width")
            col.prop(p, "caelm_wing_depth")
            col = box.column(align=True)
            col.prop(p, "caelm_floors")
            col.prop(p, "caelm_floor_height")
            col.prop(p, "caelm_pitch")
            col.prop(p, "caelm_overhang")
            box.prop(p, "caelm_detail")
            box.prop(p, "caelm_window_density")
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

    return (CAELMOR_PG_Settings, CAELMOR_OT_generate, CAELMOR_OT_load,
            CAELMOR_OT_regenerate, CAELMOR_OT_protect, CAELMOR_OT_export, CAELMOR_PT_main)


def _settings_from_json(data):
    from .model import Settings
    allowed = Settings.__dataclass_fields__.keys()
    return Settings(**{key: data[key] for key in allowed if key in data})


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


