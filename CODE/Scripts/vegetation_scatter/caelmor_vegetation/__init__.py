"""Caelmor Vegetation Scatter, a Blender 5.0 authoring extension."""

from dataclasses import replace

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty, StringProperty
from mathutils import Matrix

from . import blender_backend as backend
from .distribution import FAMILY_WEIGHTS, MASKS, Settings


PRESETS = {"SPARSE": 30., "MODERATE": 90., "DENSE": 165.}
DEFAULTS = Settings()
FAMILIES = tuple((family, family.replace("_", " "), "") for family in FAMILY_WEIGHTS)
MASK_LABELS = {"cv_density": "Density", "cv_exclude": "Exclusion", "cv_moisture": "Moisture", "cv_verge": "Verge"}


class CV_Species(bpy.types.PropertyGroup):
    pass


CV_Species.__annotations__ = {
    family: FloatProperty(name=family.replace("_", " "), min=0., max=4., default=weight)
    for family, weight in FAMILY_WEIGHTS.items()
}


class CV_Settings(bpy.types.PropertyGroup):
    library: StringProperty(name="Vegetation Library", subtype="FILE_PATH")
    layer: StringProperty(name="Output Layer", default="Lowmark")
    density: FloatProperty(name="Candidates per m²", min=0, max=1000, default=DEFAULTS.density,
                           description="Candidate density before habitat, masks and budgets are applied")
    seed: IntProperty(name="Seed", min=0, default=DEFAULTS.seed)
    filler: FloatProperty(name="Filler Share", min=0, max=1, default=DEFAULTS.filler, subtype="FACTOR")
    scale_min: FloatProperty(name="Minimum Scale", min=.02, max=6, default=DEFAULTS.scale[0])
    scale_max: FloatProperty(name="Maximum Scale", min=.02, max=6, default=DEFAULTS.scale[1])
    height: FloatProperty(name="Height Multiplier", min=.03, max=8, default=DEFAULTS.height)
    heading: FloatProperty(name="Heading", subtype="ANGLE", default=DEFAULTS.heading)
    rotation: FloatProperty(name="Rotation Spread", min=0, max=3.141593, subtype="ANGLE", default=DEFAULTS.rotation)
    align: FloatProperty(name="Follow Slope", min=0, max=1, default=DEFAULTS.align, subtype="FACTOR")
    clustering: FloatProperty(name="Clustering", min=0, max=1, default=DEFAULTS.clustering, subtype="FACTOR")
    patch_size: FloatProperty(name="Patch Size", min=.12, max=100., default=DEFAULTS.patch_size, subtype="DISTANCE")
    moisture: FloatProperty(name="Soil Moisture", min=0, max=1, default=DEFAULTS.moisture, subtype="FACTOR")
    slope_limit: FloatProperty(name="Maximum Slope (°)", min=1, max=89, default=DEFAULTS.slope_limit)
    elevation_limit: BoolProperty(name="Limit Elevation")
    elevation_min: FloatProperty(name="Minimum Elevation", subtype="DISTANCE", default=-10.)
    elevation_max: FloatProperty(name="Maximum Elevation", subtype="DISTANCE", default=100.)
    paths: PointerProperty(name="Path Guides", type=bpy.types.Collection,
                           description="Unbeveled curves, edge-only meshes or Grease Pencil strokes")
    path_half_width: FloatProperty(name="Tread Half Width", min=0, default=.65, subtype="DISTANCE")
    verge_width: FloatProperty(name="Verge Width", min=0, default=.86, subtype="DISTANCE")
    structures: PointerProperty(name="Structure Footprints", type=bpy.types.Collection,
                                description="Oriented bounds of these proxies exclude interiors and shape wall-base growth")
    wall_gap: FloatProperty(name="Wall Clearance", min=0, default=DEFAULTS.wall_gap, subtype="DISTANCE")
    wall_verge: FloatProperty(name="Wall Base Width", min=0, default=DEFAULTS.wall_verge, subtype="DISTANCE")
    density_boost: FloatProperty(name="Verge and Wall Boost", min=0, max=1.8, default=DEFAULTS.density_boost)
    protected: PointerProperty(name="Protected Objects", type=bpy.types.Collection,
                               description="Optional existing hand-placed objects whose roots should be avoided")
    manual_spacing: FloatProperty(name="Protected Root Radius", min=.0, max=4., default=.20, subtype="DISTANCE")
    manual_family: EnumProperty(name="Manual Plant", items=FAMILIES, default="Mixed_Verge")
    mask: EnumProperty(name="Paint Group", items=tuple((key, label, "") for key, label in MASK_LABELS.items()))
    lod_anchor: PointerProperty(name="LOD Anchor", type=bpy.types.Object)
    lod_near: FloatProperty(name="LOD0 Range", min=0, default=DEFAULTS.lod_distances[0], subtype="DISTANCE")
    lod_far: FloatProperty(name="LOD1 Range", min=0, default=DEFAULTS.lod_distances[1], subtype="DISTANCE")
    tile_size: FloatProperty(name="Batch Size", min=.5, max=1000., default=DEFAULTS.tile_size, subtype="DISTANCE")
    max_samples: IntProperty(name="Candidate Limit", min=1, max=2000000, default=DEFAULTS.max_samples)
    max_instances: IntProperty(name="Instance Limit", min=0, max=2000000, default=DEFAULTS.max_instances)
    max_triangles: IntProperty(name="Triangle Limit", min=0, max=50000000, default=DEFAULTS.max_triangles)
    species: PointerProperty(type=CV_Species)
    show_species: BoolProperty(name="Species Mix")
    show_habitat: BoolProperty(name="Habitat and Guides", default=True)
    show_transform: BoolProperty(name="Plant Transforms")
    show_budget: BoolProperty(name="LOD and Budget")


def configure(context):
    ui = context.scene.caelmor_vegetation
    anchor = ui.lod_anchor or context.scene.camera
    return replace(DEFAULTS, seed=ui.seed, density=ui.density, filler=ui.filler, density_boost=ui.density_boost,
                   clustering=ui.clustering, patch_size=ui.patch_size, moisture=ui.moisture,
                   slope_limit=ui.slope_limit, align=ui.align,
                   elevation=(ui.elevation_min, ui.elevation_max) if ui.elevation_limit else None,
                   wall_gap=ui.wall_gap, wall_verge=ui.wall_verge, scale=(ui.scale_min, ui.scale_max),
                   height=ui.height, heading=ui.heading, rotation=ui.rotation,
                   lod_origin=tuple(anchor.matrix_world.translation) if anchor else None,
                   lod_distances=(ui.lod_near, ui.lod_far), tile_size=ui.tile_size,
                   max_samples=ui.max_samples, max_instances=ui.max_instances, max_triangles=ui.max_triangles)


class CV_OT_Preset(bpy.types.Operator):
    bl_idname = "caelmor.vegetation_preset"
    bl_label = "Set Vegetation Density"
    bl_options = {"UNDO"}

    density: EnumProperty(items=tuple((key, key.title(), "") for key in PRESETS))

    def execute(self, context):
        context.scene.caelmor_vegetation.density = PRESETS[self.density]
        return {"FINISHED"}


class CV_OT_Generate(bpy.types.Operator):
    bl_idname = "caelmor.vegetation_generate"
    bl_label = "Generate / Regenerate"
    bl_description = "Rebuild the named layer on selected terrain and retain protected placements"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT" and any(obj.type == "MESH" for obj in context.selected_objects)

    def execute(self, context):
        opts = context.scene.caelmor_vegetation
        roles = set()
        for group in (opts.paths, opts.structures, opts.protected, backend.layer_collection(context.scene, opts.layer.strip(), backend.MANUAL)):
            if group is not None:
                roles.update(group.all_objects)
        terrain = [obj for obj in context.selected_objects if obj.type == "MESH" and obj not in roles
                   and not obj.get(backend.BATCH) and not obj.get("cv_pinned_source")]
        try:
            catalog = backend.load_catalog(opts.library)
            collection, placement = backend.generate(
                context.scene, context.evaluated_depsgraph_get(), terrain, catalog, configure(context),
                layer=opts.layer, path_collection=opts.paths, path_half_width=opts.path_half_width,
                verge_width=opts.verge_width, structures=opts.structures, protected=opts.protected,
                spacing=opts.manual_spacing, weights={family: getattr(opts.species, family) for family in FAMILY_WEIGHTS},
            )
        except (ValueError, RuntimeError, KeyError, OSError) as error:
            self.report({"ERROR"}, str(error))
            return {"CANCELLED"}
        if not opts.library:
            opts.library = bpy.path.relpath(catalog.path) if bpy.data.filepath else catalog.path
        self.report({"INFO"}, f"{len(placement.xyz):,} instances, {collection['triangles']:,} triangles")
        return {"FINISHED"}


class CV_OT_Mask(bpy.types.Operator):
    bl_idname = "caelmor.vegetation_mask"
    bl_label = "Prepare Selected Paint Group"
    bl_description = "Create or select the active terrain's mask for Blender Weight Paint"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return context.mode in {"OBJECT", "PAINT_WEIGHT"} and obj and obj.type == "MESH" and not obj.get(backend.BATCH)

    def execute(self, context):
        obj = context.active_object
        mask = context.scene.caelmor_vegetation.mask
        group = obj.vertex_groups.get(mask)
        if group is None:
            attr = obj.data.attributes.get(mask)
            if attr is not None:
                self.report({"INFO"}, "The named mesh attribute already supplies this mask.")
                return {"FINISHED"}
            group = obj.vertex_groups.new(name=mask)
            if MASKS[mask]:
                group.add(list(range(len(obj.data.vertices))), MASKS[mask], "REPLACE")
        obj.vertex_groups.active_index = group.index
        self.report({"INFO"}, f"{group.name} is active for Weight Paint")
        return {"FINISHED"}


class CV_OT_Pin(bpy.types.Operator):
    bl_idname = "caelmor.vegetation_pin"
    bl_label = "Pin Selected Points"
    bl_description = "Move selected points to protected, individually editable plant objects"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH" and context.active_object and context.active_object.get(backend.BATCH)

    def execute(self, context):
        try:
            count = backend.pin_points(context, context.active_object, context.scene.caelmor_vegetation.manual_spacing)
        except (ValueError, RuntimeError) as error:
            self.report({"ERROR"}, str(error))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Pinned {count} plants")
        return {"FINISHED"}


class CV_OT_Protect(bpy.types.Operator):
    bl_idname = "caelmor.vegetation_protect"
    bl_label = "Protect Selected Plants"
    bl_description = "Reserve selected hand-placed roots when regenerating this layer"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT" and any(obj.type == "MESH" and not obj.get(backend.BATCH)
                                                for obj in context.selected_objects)

    def execute(self, context):
        opts = context.scene.caelmor_vegetation
        group = backend.manual_collection(context.scene, opts.layer.strip() or "Lowmark")
        for obj in context.selected_objects:
            if obj.type == "MESH" and not obj.get(backend.BATCH) and obj not in group.objects.values():
                group.objects.link(obj)
        return {"FINISHED"}


class CV_OT_Place(bpy.types.Operator):
    bl_idname = "caelmor.vegetation_place"
    bl_label = "Place Protected Plant at Cursor"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        opts = context.scene.caelmor_vegetation
        try:
            catalog = backend.load_catalog(opts.library)
            source = next(item for item in catalog.variants if item.family == opts.manual_family and item.stage == "Established")
            matrix = Matrix.Translation(context.scene.cursor.location) @ Matrix.Rotation(opts.heading, 4, "Z")
            backend.place_manual(context.scene, opts.layer.strip() or "Lowmark", catalog.objects[source.indices[0]],
                                 matrix, opts.manual_spacing)
        except (ValueError, RuntimeError, StopIteration, KeyError, OSError) as error:
            self.report({"ERROR"}, str(error) or "Chosen plant was absent from the approved library.")
            return {"CANCELLED"}
        return {"FINISHED"}


class CV_PT_Panel(bpy.types.Panel):
    bl_label = "Vegetation Scatter"
    bl_idname = "CV_PT_vegetation_scatter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Caelmor"

    def draw(self, context):
        layout, opts = self.layout, context.scene.caelmor_vegetation
        if context.mode == "EDIT_MESH" and context.active_object and context.active_object.get(backend.BATCH):
            layout.operator(CV_OT_Pin.bl_idname)
            return
        layout.prop(opts, "library")
        layout.prop(opts, "layer")
        row = layout.row(align=True)
        for preset in PRESETS:
            row.operator(CV_OT_Preset.bl_idname, text=preset.title()).density = preset
        row = layout.row(align=True)
        row.prop(opts, "density")
        row.prop(opts, "seed")
        layout.prop(opts, "filler")
        layout.operator(CV_OT_Generate.bl_idname, icon="OUTLINER_OB_POINTCLOUD")
        group = backend.layer_collection(context.scene, opts.layer.strip(), backend.LAYER)
        if group is not None:
            layout.label(text=f"{group.get('instances', 0):,} instances · {group.get('triangles', 0):,} triangles")
            if group.get("requested_samples", 0) > group.get("candidates", 0):
                layout.label(text="Candidate limit reached", icon="INFO")
        self.section(layout, opts, "show_transform", opts,
                     ("scale_min", "scale_max", "height", "heading", "rotation", "align"))
        self.section(layout, opts, "show_species", opts.species, FAMILY_WEIGHTS)
        habitat = self.section(layout, opts, "show_habitat", opts,
                               ("clustering", "patch_size", "moisture", "slope_limit", "elevation_limit"))
        if habitat:
            if opts.elevation_limit:
                habitat.prop(opts, "elevation_min")
                habitat.prop(opts, "elevation_max")
            for name in ("paths", "path_half_width", "verge_width", "structures", "wall_gap", "wall_verge", "density_boost"):
                habitat.prop(opts, name)
            habitat.prop(opts, "mask")
            habitat.operator(CV_OT_Mask.bl_idname)
        self.section(layout, opts, "show_budget", opts,
                     ("lod_anchor", "lod_near", "lod_far", "tile_size", "max_samples", "max_instances", "max_triangles"))
        box = layout.box()
        box.prop(opts, "protected")
        box.prop(opts, "manual_spacing")
        box.operator(CV_OT_Protect.bl_idname)
        box.prop(opts, "manual_family")
        box.operator(CV_OT_Place.bl_idname)

    @staticmethod
    def section(layout, opts, toggle, values, fields):
        box = layout.box()
        opened = getattr(opts, toggle)
        box.prop(opts, toggle, icon="TRIA_DOWN" if opened else "TRIA_RIGHT", emboss=False)
        if not opened:
            return None
        for name in fields:
            box.prop(values, name)
        return box


CLASSES = (CV_Species, CV_Settings, CV_OT_Preset, CV_OT_Generate, CV_OT_Mask,
           CV_OT_Pin, CV_OT_Protect, CV_OT_Place, CV_PT_Panel)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.caelmor_vegetation = PointerProperty(type=CV_Settings)


def unregister():
    del bpy.types.Scene.caelmor_vegetation
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
