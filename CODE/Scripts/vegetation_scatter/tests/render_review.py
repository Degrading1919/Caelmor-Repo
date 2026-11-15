"""Matched Cycles evidence on the approved farmhouse and a 50 × 38 m meadow."""

from argparse import ArgumentParser
from pathlib import Path
import csv
import sys
import time

import bpy
import numpy as np

TOOL = Path(__file__).resolve().parents[1]
REPO = TOOL.parents[2]
MATERIALS = REPO / "MEDIA" / "Materials" / "procedurally_generated"
sys.path[:0] = [str(TOOL), str(MATERIALS)]

from caelmor_vegetation import PRESETS, configure, register
from caelmor_vegetation import blender_backend as backend
from caelmor_vegetation.distribution import FAMILY_WEIGHTS, guide_fields, wall_fields
from build_lowmark_packed_earth import Soil, UV, material, mesh_with_uv
from build_lowmark_structural_timber import grid_faces, point, profile, ramp


def collection(scene, name):
    group = bpy.data.collections.new(name)
    scene.collection.children.link(group)
    return group


def guide(group, name, points, half_width, verge):
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions = "3D"
    spline = data.splines.new("POLY")
    spline.points.add(len(points)-1)
    spline.points.foreach_set("co", np.column_stack((points, np.ones(len(points)))).astype(np.float32).ravel())
    obj = bpy.data.objects.new(name, data)
    group.objects.link(obj)
    obj.hide_render = True
    obj["cv_path_half_width"] = half_width
    obj["cv_verge_width"] = verge
    return obj


def footprint(group, name, corners):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([(x, y, 0.) for x, y in corners], [], [(0, 1, 2, 3)])
    obj = bpy.data.objects.new(name, mesh)
    group.objects.link(obj)
    obj.hide_render = True
    obj.display_type = "WIRE"
    return obj


def paint(obj, name, values):
    attribute = obj.data.attributes.new(name, "FLOAT", "POINT")
    attribute.data.foreach_set("value", np.clip(values, 0, 1).astype(np.float32).ravel())


def farmhouse():
    original = MATERIALS / "Lowmark_Natural_Grass_Wildflowers_Farmhouse.blend"
    bpy.ops.wm.open_mainfile(filepath=str(original))
    scene = bpy.context.scene
    ground = bpy.data.objects["Approved packed earth and worn approach"]
    for name in ("Farmhouse review planting", "Farmhouse filler batches (2.5 m cells)"):
        old = bpy.data.collections[name]
        scene.collection.children.unlink(old)
    y = np.linspace(-18., 11.8, 470)
    x = 3.79+.98*(1-np.cos(.28*np.maximum(-y-.38, 0)))
    paths = collection(scene, "Test guide · Footpath centerline")
    guide(paths, "Farmhouse approach guide", np.column_stack((x, y, np.zeros_like(y))), .69, .90)
    buildings = collection(scene, "Test footprint · Farmhouse")
    footprint(buildings, "Farmhouse bearing", ((-.015, -.08), (8.20, -.08), (8.20, 5.67), (-.015, 5.67)))
    footprint(buildings, "Front steps", ((3.20, -.91), (4.37, -.91), (4.37, -.08), (3.20, -.08)))

    verts = np.empty(3*len(ground.data.vertices), np.float32)
    ground.data.vertices.foreach_get("co", verts)
    x, y, _ = verts.reshape(-1, 3).T
    side = x-(3.79+.98*(1-np.cos(.28*np.maximum(-y-.38, 0))))
    drainage = .24*np.exp(-((x-2.65)/1.05)**2-((y+3.1)/4.1)**2)
    dry = .26*np.exp(-((x-6.85)/2.2)**2-((y+3.6)/3.0)**2)
    paint(ground, "cv_moisture", .49+drainage-dry)
    yard = (1-ramp(5.25, 7.1, np.abs(side)))*ramp(-14.4, -11.4, y)*(1-ramp(-.06, 1.3, y))
    disturbed = .48*np.exp(-((x-6.04)/.73)**2-((y+1.1)/1.4)**2)
    paint(ground, "cv_density", yard*(1-disturbed))
    scene.camera = bpy.data.objects["Gameplay-distance approach"]
    point(scene.camera, (4.20, -.95, .57))
    return scene, ground, paths, buildings


def meadow():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    y = np.linspace(-11., 39., 191)
    x = 2.80*np.sin(.105*y+.37)+.18*np.sin(.24*y)
    centers = np.column_stack((x, y))
    lengths = np.r_[0, np.cumsum(np.linalg.norm(np.diff(centers, axis=0), axis=1))]
    direction = np.gradient(centers, axis=0)
    direction /= np.linalg.norm(direction, axis=1, keepdims=True)
    side = np.column_stack((-direction[:, 1], direction[:, 0]))
    along, across = np.meshgrid(lengths, np.linspace(-19., 19., 153))
    coords = centers[None]+across[:, :, None]*side[None]
    xx, yy = coords.transpose(2, 0, 1)
    soil = Soil(81379, .82, .91, .56, .60, .77, .80)
    track, _ = soil.shoulder(along, across)
    z = (.65*np.sin(xx*.16-.57)*np.sin(yy*.147+.12)+.27*np.cos(yy*.29+xx*.17)
         +.056*np.sin(xx*1.34+yy*1.17)+.032*np.cos(xx*2.21-yy*.72)-.04*track)
    z += 1.07*np.exp(-((xx-6.9)/7.3)**2-((yy-17.2)/6.9)**2)+.028*yy
    terrain = mesh_with_uv("Lowmark rolling meadow", np.column_stack((xx.ravel(), yy.ravel(), z.ravel())),
                           grid_faces(len(y), len(across)), np.column_stack((along.ravel(), across.ravel())),
                           material("Transition"))
    assert terrain.data.uv_layers.get(UV) is not None
    meadow_soil = .76+.32*profile(xx/18, yy/18, 4, 4, 678, periodic=False)
    grazed = .57*np.exp(-((xx+10.4)/5.)**2-((yy-3.4)/4.6)**2)
    moist_ditch = .41*np.exp(-((xx+.24*yy-7.1)/2.35)**2)
    paint(terrain, "cv_density", meadow_soil*(1-grazed))
    paint(terrain, "cv_moisture", .30+moist_ditch+.21*profile(xx/18, yy/18, 3, 3, 891, periodic=False))
    paths = collection(scene, "Test guide · Meadow curve")
    guide(paths, "Meadow footpath centerline", np.column_stack((x, y, np.zeros_like(y))), .68, 1.42)

    world = bpy.data.worlds.new("Lowmark clear daylight")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (.76, .86, 1., 1.)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = .43
    scene.world = world
    sun_data = bpy.data.lights.new("Midmorning sun", "SUN")
    sun_data.energy = 2.35
    sun_data.angle = .14
    sun_data.color = (1., .93, .82)
    sun = bpy.data.objects.new("Midmorning sun", sun_data)
    scene.collection.objects.link(sun)
    sun.location = (7.5, -10.6, 8.)
    point(sun, (1., 7., 0.))
    camera_data = bpy.data.cameras.new("Meadow approach")
    camera_data.lens = 36.
    camera = bpy.data.objects.new("Meadow approach", camera_data)
    scene.collection.objects.link(camera)
    camera.location = (5.6, -10.2, 3.1)
    point(camera, (.25, 8.7, .28))
    scene.camera = camera
    return scene, terrain, paths, None


def configure_render(scene, parsed):
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 24 if parsed.draft else 62
    scene.cycles.use_denoising = True
    scene.cycles.adaptive_threshold = .018
    if parsed.optix:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "OPTIX"
        prefs.refresh_devices()
        if not any(device.type == "OPTIX" for device in prefs.devices):
            raise RuntimeError("No OptiX device is available.")
        for device in prefs.devices:
            device.use = device.type == "OPTIX"
        scene.cycles.device = "GPU"
    else:
        scene.cycles.device = "CPU"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.image_settings.quality = 94
    scene.render.resolution_x = 1550
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 58 if parsed.draft else 100


def review(fixture, parsed):
    scene, terrain, paths, structures = (farmhouse if fixture == "farmhouse" else meadow)()
    bpy.context.view_layer.update()
    options = scene.caelmor_vegetation
    options.library = str(MATERIALS / backend.LIBRARY_FILE)
    options.layer = "Review planting"
    options.seed = 19387 if fixture == "farmhouse" else 67791
    options.patch_size = 1.92 if fixture == "farmhouse" else 3.65
    options.filler = .91 if fixture == "farmhouse" else .81
    options.clustering = .95 if fixture == "farmhouse" else .96
    options.density_boost = .95 if fixture == "farmhouse" else .72
    options.moisture = .54 if fixture == "farmhouse" else .62
    options.scale_min, options.scale_max = (.82, 1.28) if fixture == "farmhouse" else (.91, 1.49)
    options.height = 1.03 if fixture == "farmhouse" else 1.16
    options.lod_near, options.lod_far = (7.5, 16.0) if fixture == "farmhouse" else (9.0, 22.0)
    options.tile_size = 4. if fixture == "farmhouse" else 6.
    options.max_samples = 365000 if fixture == "meadow" else 300000
    options.max_instances = 23500 if fixture == "farmhouse" else 127000
    options.max_triangles = 820000 if fixture == "farmhouse" else 2420000
    options.paths = paths
    options.structures = structures
    for family, value in FAMILY_WEIGHTS.items():
        setattr(options.species, family, value)
    if fixture == "meadow":
        options.species.Meadow_Seed = .59
        options.species.Mixed_Verge = 1.08
    mix = {family: getattr(options.species, family) for family in FAMILY_WEIGHTS}
    catalog = backend.load_catalog(options.library)
    configure_render(scene, parsed)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    rows = []
    for preset, density in PRESETS.items():
        options.density = density
        settings = configure(bpy.context)
        start = time.perf_counter()
        output, population = backend.generate(scene, depsgraph, [terrain], catalog, settings,
                                              layer=options.layer, path_collection=paths,
                                              structures=structures, weights=mix)
        duration = time.perf_counter()-start
        bpy.context.view_layer.update()
        repeated, check = backend.generate(scene, depsgraph, [terrain], catalog, settings,
                                          layer=options.layer, path_collection=paths,
                                          structures=structures, weights=mix)
        assert population.signature == check.signature
        assert len(check.xyz) <= options.max_instances and check.cost.sum() <= options.max_triangles
        roots = check.xyz[:, :2]
        guides = backend.guides_for(paths, scene, depsgraph, .62, .9)
        tread, verge = guide_fields(roots, guides, 1.1)
        walls = wall_fields(roots, backend.footprints_for(structures, depsgraph), 1.8)
        assert (tread >= 0).all() and (walls >= 0).all()
        rows.append((fixture, preset.title(), density, check.candidates, check.requested_samples,
                     len(check.xyz), int(check.cost.sum()), len(repeated.objects), *repeated["lod_counts"],
                     int(np.count_nonzero(verge > .1)), round(duration, 3), check.signature))
        print(rows[-1], flush=True)
        scene.render.filepath = str(parsed.output/f"{fixture}_{preset.lower()}.jpg")
        bpy.ops.render.render(write_still=True)
        if fixture == "farmhouse" and preset == "MODERATE" and not parsed.draft:
            approach = scene.camera
            scene.camera = bpy.data.objects["Verge close-up"]
            scene.render.filepath = str(parsed.output/"farmhouse_verge.jpg")
            bpy.ops.render.render(write_still=True)
            scene.camera = approach
    return rows


def main():
    cli = ArgumentParser()
    cli.add_argument("--optix", action="store_true")
    cli.add_argument("--draft", action="store_true")
    cli.add_argument("--output", type=Path, default=TOOL/"evidence")
    args = cli.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    register()
    rows = review("farmhouse", args)+review("meadow", args)
    with (args.output/"counts.csv").open("w", newline="", encoding="utf8") as file:
        writer = csv.writer(file)
        writer.writerow(("Scene", "Preset", "Density", "Candidates", "Requested", "Instances", "Triangles",
                         "Batches", "LOD0", "LOD1", "LOD2", "Verge roots", "Generate seconds", "Placement SHA256"))
        writer.writerows(rows)


if __name__ == "__main__":
    main()
