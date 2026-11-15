"""Actual authoring-scene material relief, regeneration, and export check.

Supply a matching baked PBR and height set from the three SBSARs. The original
scene is loaded as a library. All writes go to the controlled fixture folder.
"""
import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_world_evidence import ROOT, _aim, _materials, _neutral_material, _reset_scene
from render_material_relief import exported, visual_metrics
from caelmor_architecture import register, _set_props, _settings_from_props
from caelmor_architecture.blender_backend import build, export_building, load_settings
from caelmor_architecture.material_relief import HEIGHT_UV
from caelmor_architecture.model import Settings

ROOF = 'medieval_wood_shingle_roof'
PLANKS = 'worn_wood_planks'
BIRCH = 'aged_birch_wood'
NAMES = (ROOF, PLANKS, BIRCH)
MODIFIER = 'Caelmor Material Height'
OUTPUT = ROOT / 'dist' / 'assigned_relief' / 'exports'


def assign(settings, wall):
    return replace(settings, construction_overrides={'by_role': {
        'roof_cover': {'finish': 'material:' + ROOF},
        'wall_infill': {'treatment': 'wooden_boarding', 'finish': 'material:' + wall}}})


def sections(collection):
    return [o for o in collection.objects if o.get('caelm_field_family') == 'artist']


def load_materials(source, directory, *, matched):
    with bpy.data.libraries.load(str(source)) as (library, loaded):
        assert set(NAMES) <= set(library.materials)
        loaded.materials = list(NAMES)
    spans = {ROOF: (.035,.45), PLANKS: (.01877,.80), BIRCH: (.035,.50)}
    for material in loaded.materials:
        if matched:
            for node in material.node_tree.nodes:
                if node.type=='TEX_IMAGE' and node.image:
                    channel = node.name.rsplit('_',1)[-1].lower()
                    path, = directory.glob(f'{material.name}*_{channel}.png')
                    space = node.image.colorspace_settings.name
                    node.image = bpy.data.images.load(str(path))
                    node.image.colorspace_settings.name = space
        else:
            for node in material.node_tree.nodes:
                if node.type=='TEX_IMAGE' and node.image:
                    name = node.image.filepath.replace('\\','/').rsplit('/',1)[-1]
                    path, = (source.parent/'substance tx').glob(f'*/{name}')
                    node.image.filepath = str(path)
                    node.image.reload()
        for node in material.node_tree.nodes:
            if node.type=='TEX_IMAGE' and node.image:
                assert tuple(node.image.size)==(1024,1024),(material.name,node.image.filepath)
        # Let the resolver discover the matching height sibling automatically.
        # A per-material authored span and neutral datum remain optional.
        material.caelm_height_span, material.caelm_height_neutral = spans[material.name]
        material.use_fake_user = True


def evaluate(obj):
    bpy.context.view_layer.update()
    mesh = obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
    points = np.empty(3 * len(mesh.vertices),np.float32)
    mesh.vertices.foreach_get('co',points)
    edges = np.empty(len(mesh.loops),np.int32)
    mesh.loops.foreach_get('edge_index',edges)
    count = np.bincount(edges,minlength=len(mesh.edges))
    border = sorted({index for e in mesh.edges if count[e.index]==1 for index in e.vertices})
    uv = {}
    for name in ('UV0_Metric',HEIGHT_UV):
        coordinates = np.empty(2 * len(mesh.loops),np.float32)
        mesh.uv_layers[name].data.foreach_get('uv',coordinates)
        uv[name] = coordinates
    return points.reshape(-1,3),border,uv


def check(obj):
    displacement = obj.modifiers[MODIFIER]
    strength = displacement.strength
    moving,border,uv = evaluate(obj)
    try:
        displacement.strength = 0.
        flat,_,_ = evaluate(obj)
    finally:
        displacement.strength = strength
    lift = np.linalg.norm(moving-flat,axis=1)
    material = obj.data.materials[0].name
    scale = .46 if material==PLANKS else 1.
    uv_error = float(np.max(np.abs(uv[HEIGHT_UV] - scale * uv['UV0_Metric'])))
    assert uv_error < 2e-6, (obj.name,uv_error)
    assert border and float(lift[border].max()) < 2e-6,obj.name
    assert float(lift.max()) > .0001 and np.isfinite(moving).all(),obj.name
    image = displacement.texture.image
    assert image.filepath.lower().rsplit('_',1)[-1].startswith('height.')
    values = np.empty(len(image.pixels),dtype=np.float32)
    image.pixels.foreach_get(values)
    height = values[::image.channels]
    limit = max(abs(float(height.min())-displacement.mid_level),
                abs(float(height.max())-displacement.mid_level))*strength
    assert float(lift.max()) <= limit + 2e-6,(obj.name,float(lift.max()),limit)
    return {'material':material,'resolution':list(image.size),'height_hash':hashlib.sha256(
            Path(bpy.path.abspath(image.filepath)).read_bytes()).hexdigest(),
            'max_lift_mm':float(lift.max()*1000),'boundary_vertices':len(border),
            'max_uv_error':uv_error,'uv_repeat_per_metre':scale,
            'mesh_hash':hashlib.sha256(moving.tobytes()).hexdigest()}


def capture(scene, camera, collection, directory, state, roof_target=None):
    directory.mkdir(parents=True,exist_ok=True)
    scene.render.resolution_x,scene.render.resolution_y = 960,640
    scene.eevee.taa_render_samples = 24
    lamp = next(obj for obj in scene.objects if obj.type=='LIGHT' and obj.data.type=='SUN')
    lamp.rotation_euler = Vector((.75,-.42,.33)).to_track_quat('Z','Y').to_euler()
    fields = sections(collection)
    roof = next(o for o in fields if o.get('caelm_layer')=='roof')
    face = max(roof.data.polygons,key=lambda p:-p.normal.y)
    if roof_target is None:
        roof_target = roof.matrix_world @ face.center
    views = {'gameplay': ((4,2.6,2.4),(1.,-1.8,1.65),14.2),
             'roof': (roof_target,(.35,-1,.48),3.4),
             'wall': ((4.15,0.,1.65),(.38,-1,.18),4.4)}
    original = {o:tuple(o.data.materials) for o in collection.objects if o.type=='MESH'}
    for finish in ('material','clay'):
        if state.startswith('original') and finish=='clay':
            continue
        if finish=='clay':
            _materials(collection,_neutral_material())
        for view,(target,direction,scale) in views.items():
            target = Vector(target)
            _aim(camera,target+Vector(direction).normalized()*22,target)
            camera.data.ortho_scale = scale
            scene.render.filepath = str(directory/f'{state}_{view}_{finish}.png')
            bpy.ops.render.render(write_still=True)
    for obj,materials in original.items():
        obj.data.materials.clear()
        for material in materials:
            obj.data.materials.append(material)
    return roof_target


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source',type=Path)
    parser.add_argument('bakes',type=Path)
    parser.add_argument('--render',action='store_true')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    source,bakes = args.source.resolve(strict=True),args.bakes.resolve(strict=True)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    settings = Settings(function='COTTAGE',region='LOWMARK',footprint='RECT',
                        width=8.,depth=5.8,floors=1,detail='MEDIUM',world_aware=True,
                        geometry_mode='EFFICIENT',fit_blockout=True,material_relief=True,
                        relief_resolution=1)
    placement = ((0.,0.,0.),0.)
    frames = OUTPUT.parent/'frames'
    if args.render:
        scene,camera = _reset_scene()
        register()
        load_materials(source,bakes,matched=False)
        collection,_ = build(assign(settings,PLANKS),placement=placement)
        assert all(not o.modifiers and 'no height' in o['caelm_relief_status'] for o in sections(collection))
        capture(scene,camera,collection,frames,'original')
        collection,_ = build(assign(settings,BIRCH),collection=collection)
        assert all(not o.modifiers and 'no height' in o['caelm_relief_status'] for o in sections(collection))
        capture(scene,camera,collection,frames,'original_birch')
    scene,camera = _reset_scene()
    if not hasattr(bpy.types.Scene,'caelmor_settings'):
        register()
    load_materials(source,bakes,matched=True)
    props = scene.caelmor_settings
    _set_props(props,assign(settings,PLANKS))
    authored = _settings_from_props(props)
    flat = replace(authored,relief_strength=0.)
    props.caelm_finish_role = 'wall_infill'
    props.caelm_finish_material = bpy.data.materials[BIRCH]
    assert bpy.ops.caelmor.stage_finish()=={'FINISHED'}
    remapped = _settings_from_props(props)
    collection,_ = build(flat,placement=placement)
    report = {'scene_sha256':digest,'blender':bpy.app.version_string,'cases':{}}
    first = None
    roof_target = None
    for label,current in (('flat',flat),('relief',authored),
                          ('remapped',remapped)):
        collection,_ = build(current,collection=collection)
        fields = sections(collection)
        assert len(fields)>=2
        checks = {o['caelm_buffer_id']:check(o) for o in fields} if label!='flat' else {}
        assert label!='flat' or all(not o.modifiers for o in fields)
        assert label!='remapped' or BIRCH in {r['material'] for r in checks.values()}
        path = OUTPUT / label / 'cottage.glb'
        path.parent.mkdir(parents=True,exist_ok=True)
        export_building(collection,str(path))
        metrics,hierarchy = exported(path)
        rows = visual_metrics(collection)
        assert metrics['triangles']==sum(r[1] for r in rows.values())
        collision = hashlib.sha256(path.with_suffix('.collision.glb').read_bytes()).hexdigest()
        if first is None:
            first = hierarchy,collision,metrics['renderers']
        assert first==(hierarchy,collision,metrics['renderers']),label
        report['cases'][label] = {'fields':checks,'glb':metrics,'collision_sha256':collision}
        if args.render:
            roof_target = capture(scene,camera,collection,frames,label,roof_target)
    if args.render:
        mods = [obj.modifiers[MODIFIER] for obj in sections(collection)]
        strengths = [mod.strength for mod in mods]
        for mod in mods:
            mod.strength = 0.
        capture(scene,camera,collection,frames,'birch_flat',roof_target)
        for mod,strength in zip(mods,strengths):
            mod.strength = strength

    prior = {o['caelm_buffer_id']:evaluate(o)[0] for o in sections(collection)}
    # Bind the three automatically discovered images to the review library
    # copies so they can be appended without an external bake directory.
    for name in NAMES:
        path, = bakes.glob(f'{name}*_height.png')
        image = next(im for im in bpy.data.images if im.filepath and
                     Path(bpy.path.abspath(im.filepath))==path and im.colorspace_settings.name=='Non-Color')
        bpy.data.materials[name].caelm_height_image = image
    bpy.ops.file.pack_all()
    _set_props(scene.caelmor_settings,assign(settings,BIRCH))
    preview = OUTPUT.parent/'material_relief_review.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(preview),copy=True)
    bpy.ops.wm.open_mainfile(filepath=str(preview))
    collection = next(c for c in bpy.data.collections if c.get('caelm_build'))
    restored = Settings(**load_settings(collection))
    assert restored.relief_resolution==1 and restored.material_relief
    fields = sections(collection)
    assert {o.data.materials[0].name for o in fields}=={ROOF,BIRCH}
    collection,_ = build(restored,collection=collection)
    replay_delta = {}
    for obj in sections(collection):
        key = obj['caelm_buffer_id']
        actual = check(obj)
        expected = report['cases']['remapped']['fields'][key]
        assert actual['height_hash']==expected['height_hash'] and actual['material']==expected['material']
        delta = float(np.max(np.abs(evaluate(obj)[0]-prior[key])))
        assert delta < 1e-5, (key,delta,actual,expected)
        replay_delta[key] = delta
    before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=str(OUTPUT/'remapped'/'cottage.glb'))
    objects = [o for o in bpy.context.scene.objects if o not in before and o.type=='MESH']
    assert sum(len(o.data.polygons) for o in objects)==report['cases']['remapped']['glb']['triangles']
    imports = {o.get('caelm_buffer_id'):o for o in objects}
    for key in report['cases']['remapped']['fields']:
        assert len(imports[key].data.uv_layers)==4
    assert hashlib.sha256(source.read_bytes()).hexdigest()==digest
    report['save_reopen_regenerate_and_reimport'] = True
    report['max_replay_delta_metres'] = replay_delta
    (OUTPUT.parent/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('CAELMOR_ASSIGNED_RELIEF_PASS',flush=True)


if __name__=='__main__':
    main()
