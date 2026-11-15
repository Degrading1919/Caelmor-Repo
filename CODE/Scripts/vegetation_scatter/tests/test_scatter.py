"""Native integration checks. Run with Blender 5.0.1 and --python-exit-code 1."""

from dataclasses import replace
from pathlib import Path
import math
import sys
import unittest

import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import caelmor_vegetation as addon
from caelmor_vegetation import blender_backend as backend
from caelmor_vegetation.distribution import Guide, Placement, Settings, guide_fields, manual_fields, scatter, wall_fields


def mesh_object(name, vertices, faces, edges=()):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, edges, faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def terrain(name, center=(0, 0, 0)):
    obj = mesh_object(name, [(i, j, 0.) for j in range(-5, 6) for i in range(-6, 7)],
                      [(y*13+x, y*13+x+1, (y+1)*13+x+1, (y+1)*13+x) for y in range(10) for x in range(12)])
    obj.location = center
    return obj


class VegetationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        addon.register()
        cls.catalog = backend.load_catalog(backend.default_library())

    def setUp(self):
        self.scene = bpy.context.scene
        for obj in tuple(self.scene.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        for cid in tuple(self.scene.collection.children):
            bpy.data.collections.remove(cid)
        self.ground = terrain("Test ground")
        bpy.context.view_layer.update()
        self.depsgraph = bpy.context.evaluated_depsgraph_get()
        self.settings = Settings(density=80., seed=13, lod_origin=(0., -6., 2.))

    def selected(self, obj):
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

    def test_mask_presets_and_seeded_surface(self):
        self.assertEqual(len(self.catalog.objects), 93)
        self.assertEqual(len(self.catalog.variants), 31)
        self.assertTrue(all(obj.library for obj in self.catalog.objects))
        self.selected(self.ground)
        options = self.scene.caelmor_vegetation
        options.library = self.catalog.path
        options.mask = "cv_density"
        self.assertEqual(bpy.ops.caelmor.vegetation_mask(), {"FINISHED"})
        weights = self.ground.vertex_groups["cv_density"]
        weights.add([v.index for v in self.ground.data.vertices if v.co.x <= 0], 0., "REPLACE")
        exclude = self.ground.data.attributes.new("cv_exclude", "FLOAT", "POINT")
        exclude.data.foreach_set("value", np.array([float(v.co.y >= 3) for v in self.ground.data.vertices], np.float32))
        bpy.context.view_layer.update()
        surface = backend.surface(self.ground, self.depsgraph)
        results = scatter([surface], self.catalog.variants, self.settings)
        again = scatter([surface], self.catalog.variants, self.settings)
        self.assertEqual(results.signature, again.signature)
        self.assertGreater(len(results.xyz), 200)
        self.assertTrue(np.all(results.xyz[:, 0] > -1.))
        self.assertTrue(np.all(results.xyz[:, 1] < 3.))
        edited = scatter([surface], self.catalog.variants, replace(self.settings, seed=14, density=28.))
        self.assertNotEqual(results.signature, edited.signature)
        self.assertLess(len(edited.xyz), len(results.xyz))
        self.assertEqual(bpy.ops.caelmor.vegetation_preset(density="SPARSE"), {"FINISHED"})
        self.assertEqual(options.density, addon.PRESETS["SPARSE"])

    def test_masks_path_footprints_scale_mix_and_budget(self):
        blocked = np.array([(-4., -2.), (-2., -2.), (-2., 2.), (-4., 2.)])
        guide = Guide(np.asarray([((-6., 0.), (6., 0.))]), .68, 1.25)
        pins = np.array([[2., 2., .42]])
        surface = backend.surface(self.ground, self.depsgraph)
        settings = replace(self.settings, density=170., max_triangles=9000, max_instances=550,
                           lod_distances=(.8, 5.), rotation=0., heading=.36, height=.56,
                           scale=(.80, .80), elevation=(-.05, .05))
        result = scatter([surface], self.catalog.variants, settings, guides=(guide,),
                         footprints=(blocked,), protected=pins, weights={"Mixed_Verge": 1.})
        self.assertGreater(len(result.xyz), 10)
        self.assertLessEqual(len(result.xyz), 550)
        self.assertLessEqual(result.cost.sum(), 9000)
        np.testing.assert_allclose(result.euler[:, 2], .36)
        np.testing.assert_allclose(result.scale[:, :2], .80)
        self.assertTrue(np.all(result.scale[:, 2] < .52))
        footprints = {}
        for item in self.catalog.variants:
            for index in item.indices:
                footprints[index] = item.radius
        radius = np.asarray([footprints[i] for i in result.assets])*.8
        xy = result.xyz[:, :2]
        self.assertTrue(np.all(guide_fields(xy, (guide,), 2.)[0] >= radius))
        self.assertTrue(np.all(wall_fields(xy, (blocked,), 3.) >= radius+settings.wall_gap))
        self.assertTrue(np.all(manual_fields(xy, pins, 3.) >= radius))
        self.assertTrue(all(self.catalog.objects[i]["asset_family"] == "Mixed_Verge" for i in result.assets))

    def test_slope_elevation_and_multiple_terrain(self):
        far = terrain("High shelf", (22, 0, 4))
        steep = terrain("Steep face", (40, 0, 0))
        steep.rotation_euler.y = math.radians(67)
        bpy.context.view_layer.update()
        surfaces = [backend.surface(obj, self.depsgraph) for obj in (far, steep, self.ground)]
        result = scatter(surfaces, self.catalog.variants, self.settings)
        self.assertTrue(np.all(result.xyz[:, 0] < 29))
        self.assertGreater(np.count_nonzero(result.xyz[:, 2] > 3), 200)
        low = scatter(surfaces, self.catalog.variants, replace(self.settings, elevation=(-.5, 1.), max_samples=1333))
        self.assertEqual(low.candidates, 1333)
        self.assertGreater(low.requested_samples, low.candidates)
        self.assertTrue(np.all(low.xyz[:, 2] < 1.))
        self.assertEqual(low.signature, scatter(list(reversed(surfaces)), self.catalog.variants,
                                                replace(self.settings, elevation=(-.5, 1.), max_samples=1333)).signature)

    def test_native_curve_grease_pencil_and_footprint_inputs(self):
        path = bpy.data.collections.new("Guide collection")
        self.scene.collection.children.link(path)
        spline_data = bpy.data.curves.new("Curve guide", "CURVE")
        spline = spline_data.splines.new("BEZIER")
        spline.bezier_points.add(2)
        for point, xyz in zip(spline.bezier_points, ((-4., -3., 0), (0., -2., 0), (4., -3., 0))):
            point.co = xyz
            point.handle_left_type = point.handle_right_type = "AUTO"
        curve = bpy.data.objects.new("Bezier guide", spline_data)
        path.objects.link(curve)
        curve["cv_path_half_width"] = .42
        gpd = bpy.data.grease_pencils.new("Ink guide")
        layer = gpd.layers.new("Walk", set_active=True)
        drawing = layer.frames.new(1).drawing
        drawing.add_strokes([3])
        for pt, coords in zip(drawing.strokes[0].points, ((-4., 3., 0), (0., 2., 0), (4., 3., 0))):
            pt.position = coords
        ink = bpy.data.objects.new("Ink guide", gpd)
        path.objects.link(ink)
        ink.location.x = .24
        self.scene.frame_set(1)
        bpy.context.view_layer.update()
        guides = backend.guides_for(path, self.scene, self.depsgraph, .72, .48)
        self.assertEqual([guide.half_width for guide in guides], [.42, .72])
        self.assertGreater(len(guides[0].segments), 8)
        self.assertEqual(len(guides[1].segments), 2)
        self.assertAlmostEqual(guides[1].segments[0, 0, 0], -3.76, places=5)
        proxy = mesh_object("Footprint", [(-2, -1, 0), (2, -1, 0), (2, 1, 0), (-2, 1, 0)], [(0, 1, 2, 3)])
        proxy.rotation_euler.z = .53
        structures = bpy.data.collections.new("Structures")
        self.scene.collection.children.link(structures)
        structures.objects.link(proxy)
        bpy.context.view_layer.update()
        polygons = backend.footprints_for(structures, self.depsgraph)
        self.assertEqual(len(polygons), 1)
        self.assertLess(wall_fields(np.array([[0., 0.]]), polygons, 1.)[0], -.98)

    def test_instances_evaluate_and_pick_the_approved_mesh(self):
        names = {obj.name: i for i, obj in enumerate(self.catalog.objects)}
        wanted = [names["LM_Dry_Stems_Established_LOD2"], names["LM_Selfheal_Established_LOD0"]]
        points = np.array([[1., 1., 0.], [3., 1., 0.]])
        placement = Placement(points, np.zeros((2, 3)), np.ones((2, 3)), np.array(wanted), np.array([2, 0]),
                              np.array([self.catalog.objects[i]["triangles"] for i in wanted]))
        collection = backend.apply_placement(self.scene, "Instance test", self.catalog, self.settings, placement)
        batch, = collection.objects
        modifier = batch.modifiers[0]
        original = modifier.node_group
        proof = original.copy()
        try:
            modifier.node_group = proof
            output = proof.nodes.get("Group Output")
            realize = proof.nodes.new("GeometryNodeRealizeInstances")
            proof.links.new(proof.nodes.get("Instance on Points").outputs["Instances"], realize.inputs["Geometry"])
            proof.links.new(realize.outputs["Geometry"], output.inputs["Geometry"])
            bpy.context.view_layer.update()
            obj = batch.evaluated_get(self.depsgraph)
            mesh = obj.to_mesh()
            mesh.calc_loop_triangles()
            parts = [sum((mesh.vertices[t.vertices[0]].co.x < 2.) == left for t in mesh.loop_triangles)
                     for left in (True, False)]
            self.assertEqual(parts, placement.cost.tolist())
            obj.to_mesh_clear()
        finally:
            modifier.node_group = original
            bpy.data.node_groups.remove(proof)

    def test_operators_pin_regenerate_and_keep_external_edits(self):
        options = self.scene.caelmor_vegetation
        options.layer = "Edit proof"
        options.library = self.catalog.path
        options.density = 30.
        self.selected(self.ground)
        self.assertEqual(bpy.ops.caelmor.vegetation_generate(), {"FINISHED"})
        output = backend.layer_collection(self.scene, options.layer, backend.LAYER)
        pre_signature = output["signature"]
        batch = next(iter(output.objects))
        self.selected(batch)
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode="OBJECT")
        index = min(2, len(batch.data.vertices)-1)
        batch.data.vertices[index].select = True
        original_root = np.asarray(batch.matrix_world @ batch.data.vertices[index].co)
        old_count = len(batch.data.vertices)
        bpy.ops.object.mode_set(mode="EDIT")
        self.assertEqual(bpy.ops.caelmor.vegetation_pin(), {"FINISHED"})
        bpy.ops.object.mode_set(mode="OBJECT")
        self.assertEqual(len(batch.data.vertices), old_count-1)
        manual = backend.layer_collection(self.scene, options.layer, backend.MANUAL)
        pinned, = manual.objects
        pinned.location = (0., -2., .026)
        pinned.scale *= 1.3
        marker = mesh_object("Artist hand edit", [(0, 0, 0)], [])
        marker.location = (2., .5, 0.)
        output.objects.link(marker)
        self.selected(self.ground)
        self.assertEqual(bpy.ops.caelmor.vegetation_generate(), {"FINISHED"})
        new = backend.layer_collection(self.scene, options.layer, backend.LAYER)
        self.assertNotEqual(new["signature"], pre_signature)
        self.assertIn(pinned, manual.objects.values())
        self.assertIn(marker, manual.objects.values())
        self.assertAlmostEqual(pinned.location.z, .026, places=5)
        self.assertEqual(tuple(pinned.location)[:2], (0., -2.))
        roots = np.array([tuple(obj.matrix_world @ vertex.co) for obj in new.objects for vertex in obj.data.vertices])
        self.assertGreater(np.linalg.norm(roots[:, :2]-original_root[:2], axis=1).min(), .014)
        stable = new["signature"]
        self.assertEqual(bpy.ops.caelmor.vegetation_generate(), {"FINISHED"})
        self.assertEqual(backend.layer_collection(self.scene, options.layer, backend.LAYER)["signature"], stable)
        self.assertEqual(len(manual.objects), 2)

    def test_failed_build_and_empty_build_do_not_touch_protected_objects(self):
        output, _ = backend.generate(self.scene, self.depsgraph, [self.ground], self.catalog,
                                     self.settings, layer="Protected proof")
        pin = backend.place_manual(self.scene, "Protected proof", self.catalog.objects[0],
                                   self.ground.matrix_world, .25)
        with self.assertRaisesRegex(ValueError, "ascending order"):
            backend.generate(self.scene, self.depsgraph, [self.ground], self.catalog,
                             replace(self.settings, scale=(1.5, .7)), layer="Protected proof")
        self.assertIs(output, backend.layer_collection(self.scene, "Protected proof", backend.LAYER))
        empty, result = backend.generate(self.scene, self.depsgraph, [self.ground], self.catalog,
                                          replace(self.settings, density=0), layer="Protected proof")
        self.assertEqual(len(result.xyz), 0)
        self.assertEqual(len(empty.objects), 0)
        self.assertIn(pin, backend.layer_collection(self.scene, "Protected proof", backend.MANUAL).objects.values())


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(VegetationTests))
    if not result.wasSuccessful():
        raise RuntimeError("Vegetation validation failed")
