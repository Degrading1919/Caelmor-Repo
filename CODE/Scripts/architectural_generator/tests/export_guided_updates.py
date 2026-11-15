"""Export four revisions of one Blender building for the Unity update test."""
import json
import os
from pathlib import Path
import sys

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(Path(__file__).resolve().parent)]

from caelmor_architecture.blender_backend import export_building
from caelmor_architecture.guide_backend import GUIDE, SCHEDULE, anchor_of
from test_condition_export import read_glb
from test_opening_guides_blender import cottage, face, opening, select, setup_scene
from test_wall_feature_guides_blender import DAMP_OUTLINE, timber_edge


def export(collection, output, revision):
    folder = output / revision
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / 'cottage.glb'
    export_building(collection, str(path), construction_metadata=True)
    visual, _ = read_glb(path)
    collider, _ = read_glb(path.with_suffix('.collision.glb'))
    sidecar = json.loads(path.with_suffix('.caelmor.json').read_text(encoding='utf-8'))
    assert sidecar['source_validation']['valid']
    groups = [n['extras']['caelm_floor_group'] for n in visual['nodes'] if n.get('extras', {}).get('caelm_floor_group')]
    assert groups and len(groups) == len(set(groups))
    return dict(building=sidecar['floor_presentation']['building_id'],
                visual={n.get('extras', {}).get('caelm_buffer_id') for n in visual['nodes']} - {None},
                collision={n['name'] for n in collider['nodes']})


def main(output):
    scene, *_ = setup_scene()
    props = scene.caelmor_settings
    collection, _ = cottage(props, (5., -2., 1.675))
    baseline = export(collection, output, 'baseline')
    door = face(collection, 'Update test door', 'rear', [(1.25,.45),(2.35,.45),(2.35,2.59),(1.25,2.59)])
    door_id = opening(props, collection, door, 'DOOR', leaf=False)
    window = face(collection, 'Update test window', 'right', [(2.15,1.25),(3.35,1.25),(3.35,2.20),(2.15,2.20)])
    window_id = opening(props, collection, window, 'WINDOW')
    added = export(collection, output, 'added')
    first_schedule = json.loads(collection[SCHEDULE])
    door.location.x -= .22
    bpy.context.view_layer.update()
    coordinates = anchor_of(collection).matrix_world.inverted() @ window.matrix_world
    stretch = coordinates.inverted().to_3x3() @ Vector((0, .16, 0))
    for vertex in window.data.vertices:
        if (coordinates @ vertex.co).y > 3.:
            vertex.co += stretch
    window.data.update()
    select(window)
    assert bpy.ops.caelmor.opening_guide(action='REFRESH') == {'FINISHED'}
    assert door[GUIDE]['id'] == door_id and window[GUIDE]['id'] == window_id
    assert json.loads(collection[SCHEDULE]) != first_schedule
    edited = export(collection, output, 'edited')
    for source in (door, window):
        select(source)
        assert bpy.ops.caelmor.opening_guide(action='REMOVE') == {'FINISHED'}
    removed = export(collection, output, 'removed')

    assert len({r['building'] for r in (baseline, added, edited, removed)}) == 1
    assert baseline['visual'] == removed['visual'] and baseline['collision'] == removed['collision']
    assert added['visual'] == edited['visual'] and added['collision'] == edited['collision']
    assert baseline['visual'] < added['visual']
    assert added['collision'] - baseline['collision'] == {f'Collider Approach {door_id}'}
    post_id = opening(props, collection, timber_edge(collection,3.70), 'TIMBER_POST')
    loss = face(collection,'Update test splash damage','right',DAMP_OUTLINE)
    loss_id = opening(props, collection, loss, 'PLASTER_LOSS')
    features = export(collection,output,'features')
    assert features['building'] == baseline['building'] and features['collision'] == baseline['collision']
    extra = features['visual'] - baseline['visual']
    assert len(extra) == 2 and all(any(f'.guide.{id}.' in buffer for buffer in extra) for id in (post_id,loss_id))
    print('GUIDED_UPDATE_FIXTURES', len(baseline['visual']), len(added['visual']),
          len(baseline['collision']), len(added['collision']), len(features['visual']))


if __name__ == '__main__':
    main(Path(os.environ.get('CAELMOR_GUIDED_UPDATE_DIR', ROOT/'dist'/'guided_update_check')))
