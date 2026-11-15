"""Reproduce the matched native displacement pilot in Blender 5."""
import hashlib
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_world_evidence import ROOT, _aim, _bounds, _materials, _neutral_material, _reset_scene
from test_condition_export import read_glb
from test_construction_depth import case
from caelmor_architecture.blender_backend import _settings_dict, build, export_building
from material_relief_pilot import height_image, install
from caelmor_architecture.model import Settings
from caelmor_architecture.engine import generate
from caelmor_architecture.surface_atlas import _field_pattern

OUT = ROOT / 'evidence' / 'material_relief'
SCRATCH = ROOT / 'dist' / 'material_relief_pilot'
FRAMES = SCRATCH / 'frames'


def settings_for(label, representation):
    if label == 'masonry':
        return case('GATEHOUSE', None if representation == 'MODELED' else representation)
    return Settings(function='COTTAGE', region='LOWMARK', footprint='RECT', floors=1,
                    width=8., depth=5.8, fit_blockout=True, seed=91, detail='MEDIUM',
                    use_grammar=False, world_aware=True, geometry_mode='EFFICIENT',
                    construction_overrides={'by_role': {'roof_cover': {'representation': representation}}})


def visual_metrics(collection):
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    rows = {}
    for obj in collection.objects:
        if obj.type != 'MESH' or obj.get('caelm_collider'):
            continue
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        try:
            mesh.calc_loop_triangles()
            rows[obj['caelm_buffer_id']] = [len(mesh.vertices), len(mesh.loop_triangles)]
        finally:
            evaluated.to_mesh_clear()
    return rows


def exported(path):
    doc, _ = read_glb(path)
    nodes = {n['name']: n for n in doc['nodes']}
    primitives = [p for n in nodes.values() if 'mesh' in n
                  for p in doc['meshes'][n['mesh']]['primitives']]
    return ({'bytes': path.stat().st_size, 'triangles': sum(
                doc['accessors'][p['indices']]['count'] // 3 for p in primitives),
             'vertex_records': sum(doc['accessors'][p['attributes']['POSITION']]['count'] for p in primitives),
             'renderers': sum('mesh' in n for n in nodes.values()), 'primitives': len(primitives),
             'materials': len(doc['materials']), 'textures': len(doc['textures']), 'images': len(doc['images'])},
            {n['name']: (n.get('extras', {}).get('caelm_buffer_id'),
                         tuple(nodes_name['name'] for nodes_name in (doc['nodes'][i] for i in n.get('children', []))))
             for n in nodes.values()})


def field_sample(obj):
    bpy.context.view_layer.update()
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = evaluated.data
    points = np.empty(len(mesh.vertices) * 3, dtype=np.float32)
    mesh.vertices.foreach_get('co', points)
    uvs = np.empty(len(mesh.loops) * 2, dtype=np.float32)
    mesh.uv_layers['UV2_Surface'].data.foreach_get('uv', uvs)
    edges = np.empty(len(mesh.loops), dtype=np.int32)
    mesh.loops.foreach_get('edge_index', edges)
    counts = np.bincount(edges, minlength=len(mesh.edges))
    boundary = {i for edge in mesh.edges if counts[edge.index] == 1 for i in edge.vertices}
    return points.reshape(-1, 3), uvs, sorted(boundary)


def check_relief(obj):
    moving, uv_after, boundary = field_sample(obj)
    modifier = obj.modifiers['Caelmor Material Height']
    strength = modifier.strength
    try:
        modifier.strength = 0.
        flat, uv_before, _ = field_sample(obj)
    finally:
        modifier.strength = strength
    lift = np.linalg.norm(moving - flat, axis=1)
    assert np.isfinite(moving).all() and .005 < lift.max() <= strength + 1e-5
    uv_drift = float(np.max(np.abs(uv_before - uv_after)))
    assert np.isfinite(uv_drift) and uv_drift < 2e-6, (obj.name, uv_drift)
    assert boundary and lift[boundary].max() < 2e-6
    return {'lift_mm': float(lift.max() * 1000), 'pinned_boundary_vertices': len(boundary),
            'max_uv_drift': uv_drift,
            'evaluated_position_sha256': hashlib.sha256(moving.tobytes()).hexdigest()}


def check_external_image(obj, path=None):
    # An exported scalar image exercises the same input as a baked Substance
    # height output. Use the original repository image without saving to it.
    if path is None:
        directory = ROOT.parents[2] / 'MEDIA' / 'Materials' / 'procedurally_generated'
        path = directory / 'Lowmark_Brookoak_RoofShingles_displace.exr'
    image = bpy.data.images.load(str(path))
    image.colorspace_settings.name = 'Non-Color'
    texture = obj.modifiers['Caelmor Material Height'].texture
    original = texture.image
    try:
        texture.image = image
        return {'size': list(image.size), **check_relief(obj)}
    finally:
        texture.image = original
        bpy.data.images.remove(image)


def shot(scene, camera, target, direction, scale, path):
    _aim(camera, target + Vector(direction).normalized() * 24, target)
    camera.data.ortho_scale = scale
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def capture(label, *, render=True):
    scene, camera = _reset_scene()
    scene.render.resolution_x, scene.render.resolution_y = 960, 640
    scene.eevee.taa_render_samples = 24
    sun = next(o for o in scene.objects if o.type == 'LIGHT' and o.data.type == 'SUN')
    sun.rotation_euler = Vector((.94, -.22, .25)).to_track_quat('Z', 'Y').to_euler()
    sun.data.angle = .045
    settings = settings_for(label, 'TEXTURE')
    plan, _ = generate(settings)
    hosts = {zone.key: zone.plan for zone in plan.world_zones}
    collection, _ = build(settings, placement=((0., 0., 0.), 0.) if settings.fit_blockout else None)
    fields = [o for o in collection.objects if o.get('caelm_field_family')]
    if label == 'masonry':
        fields = [o for o in fields if o['caelm_world_zone'] == 'gatehouse_east_watchtower'
                  and o.get('caelm_floor_index') == 0]
    assert fields
    bounds = _bounds(collection)
    center = Vector([(a+b)/2 for a, b in bounds])
    span = max(b-a for a, b in bounds[:2])
    roof_face = max(fields[0].data.polygons, key=lambda p: -p.normal.y)
    focus = (fields[0].matrix_world @ roof_face.center if label == 'roof' else Vector((13.1, -2.56, 2.0)))
    views = {'gameplay': (center, (1., -1.6, 1.55), span * 1.50),
             'detail': (focus, (.55, -1., .62) if label == 'roof' else (.50, -1., .24),
                        4.3 if label == 'roof' else 5.)}
    directory = SCRATCH / label
    original = {o: tuple(o.data.materials) for o in collection.objects if o.type == 'MESH'}
    clay = _neutral_material()
    metrics = {'settings': _settings_dict(settings),
               'cameras': {name: {'target': list(target), 'direction': list(direction), 'scale': scale}
                           for name, (target, direction, scale) in views.items()}}
    for variant, levels in [('texture', None), ('relief_low', 0), ('relief', 1)]:
        if levels is not None:
            for obj in fields:
                if variant == 'relief_low':
                    material = obj.data.materials[0]
                    _, _, craft, weather = _field_pattern(obj, hosts[obj['caelm_world_zone']], settings)
                    install(obj, height_image(material, craft, weather),
                            strength=.04, levels=levels)
                else:
                    obj.modifiers[0].levels = obj.modifiers[0].render_levels = levels
        checks = {obj['caelm_buffer_id']: check_relief(obj) for obj in fields} if levels is not None else {}
        rows = visual_metrics(collection)
        metrics[variant] = {'vertices': sum(v for v, _ in rows.values()),
                            'triangles': sum(t for _, t in rows.values()),
                            'fields': {obj['caelm_buffer_id']: rows[obj['caelm_buffer_id']] for obj in fields},
                            'displacement_checks': checks}
        if variant in ('texture', 'relief'):
            path = directory / variant / 'building.glb'
            path.parent.mkdir(parents=True, exist_ok=True)
            export_building(collection, str(path), construction_metadata=True)
            data, hierarchy = exported(path)
            metrics[variant]['glb'] = data
            collision = hashlib.sha256(path.with_suffix('.collision.glb').read_bytes()).hexdigest()
            if variant == 'texture':
                baseline = hierarchy, collision
            else:
                assert baseline == (hierarchy, collision), (label, 'hierarchy or collision changed')
                assert data['triangles'] == metrics[variant]['triangles'], (data, metrics[variant])
        print('MATERIAL_RELIEF_METRICS', label, variant, metrics[variant], flush=True)
        if render:
            for finish in ('material', 'clay'):
                if finish == 'clay':
                    _materials(collection, clay)
                for view, arguments in views.items():
                    if variant == 'relief_low' and (view != 'detail' or finish != 'clay'):
                        continue
                    shot(scene, camera, *arguments, FRAMES / f'{label}_{view}_{finish}_{variant}.png')
            for obj, materials in original.items():
                obj.data.materials.clear()
                for material in materials:
                    obj.data.materials.append(material)
    if label == 'roof':
        name = fields[0].name
        metrics['relief']['external_image_check'] = check_external_image(fields[0])
        bpy.ops.wm.save_as_mainfile(filepath=str(directory / 'relief.blend'), copy=True)
        bpy.ops.wm.open_mainfile(filepath=str(directory / 'relief.blend'))
        reopened = bpy.data.objects[name]
        assert check_relief(reopened) == metrics['relief']['displacement_checks'][name]
        assert bpy.data.meshes[reopened.data.name + ' (undisplaced input)'].use_fake_user
        scene, camera = bpy.context.scene, bpy.context.scene.camera
        collection = next(c for c in bpy.data.collections if c.get('caelm_build'))
        metrics['relief']['saved_reopen_verified'] = True
    for obj in collection.objects:
        obj.hide_render = True
    for mode in ('MODELED', 'HYBRID'):
        fixture, _ = build(settings_for(label, mode),
                           placement=((0., 0., 0.), 0.) if settings.fit_blockout else None)
        rows = visual_metrics(fixture)
        metrics[mode.lower()] = {'vertices': sum(v for v, _ in rows.values()),
                                 'triangles': sum(t for _, t in rows.values())}
        if render:
            shot(scene, camera, *views['gameplay'], FRAMES / f'{label}_gameplay_material_{mode.lower()}.png')
        for obj in fixture.objects:
            obj.hide_render = True
    before = set(scene.objects)
    bpy.ops.import_scene.gltf(filepath=str(directory / 'relief' / 'building.glb'))
    imported = [o for o in scene.objects if o not in before and o.type == 'MESH']
    by_name = {obj.get('caelm_buffer_id'): obj for obj in imported}
    assert sum(len(o.data.polygons) for o in imported) == metrics['relief']['triangles']
    for name in metrics['relief']['fields']:
        assert len(by_name[name].data.uv_layers) >= 3
    metrics['relief']['reimported_meshes'] = len(imported)
    return metrics


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    FRAMES.mkdir(parents=True, exist_ok=True)
    labels = [label for label in ('roof', 'masonry') if '--'+label in sys.argv] or ['roof', 'masonry']
    report = {label: capture(label, render='--metrics-only' not in sys.argv) for label in labels}
    if len(labels) == 2:
        (OUT / 'measurements.json').write_text(json.dumps({
            'blender': bpy.app.version_string, 'cases': report}, indent=2) + '\n')
    print('MATERIAL_RELIEF_PILOT_PASS', flush=True)
