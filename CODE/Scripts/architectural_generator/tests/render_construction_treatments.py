"""Matched construction captures using the established benchmark studio."""
from dataclasses import replace
import json
from pathlib import Path

import sys
import bpy
sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_polish_benchmarks import CASE_SPECS, capture, settings, source_hashes
from render_world_evidence import _reset_scene
from caelmor_architecture.blender_backend import _settings_dict, build
from caelmor_architecture.engine import generate, validate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'evidence'/'construction_treatments'


def record(function, fixture, variant, distances):
    scene, _ = _reset_scene()
    bpy.data.objects['Neutral ground'].location.z = 0.
    sun = next(o for o in scene.objects if o.type=='LIGHT' and o.data.type=='SUN')
    sun.rotation_euler = (.88,.57,-.23)
    sun.data.angle = .07
    fill = next(o for o in scene.objects if o.type=='LIGHT' and o.data.type=='AREA')
    fill.data.energy = 750
    plan, buffers = generate(fixture)
    checks = validate(plan, buffers)
    assert checks['valid'], checks['errors']
    collection, _ = build(fixture)
    assert collection['caelm_geometry_hash'] == checks['geometry_hash']
    images = capture(collection, OUT/variant, function, distances=distances,
                     views=(0,), vertex_framing=True)
    for item in images:
        item['image'] = f"{variant}/{item['image']}"
    return dict(function=fixture.function, region=fixture.region, variant=variant,
                settings=_settings_dict(fixture), triangles=checks['triangles'],
                geometry_hash=checks['geometry_hash'], images=images,
                treatments=sorted({b.construction.treatment for b in buffers if b.construction}))


def main():
    records = []
    for function in ('SMITHY', 'GATEHOUSE'):
        fixture = replace(settings(function), crafted_curves=True, seed_massing=True)
        if function == 'GATEHOUSE':
            _, buffers = generate(fixture)
            wall = next(b for b in buffers if b.name.endswith('curtain_return.east'))
            right = max(v[0] for v in wall.vertices)
            CASE_SPECS[function]['targets']['close_front'] = (right-1.8,-.35,1.8)
            CASE_SPECS[function]['scales']['close'] = 7.7
            CASE_SPECS[function]['scales']['normal'] = 32.
        else:
            CASE_SPECS[function]['targets']['close'] = (6.5,1.05,2.25)
            CASE_SPECS[function]['scales']['close'] = 10.2
            CASE_SPECS[function]['directions']['close'] = ((1.16,-.78,.57),(-.8,-1.2,.4))
        before = record(function, fixture, 'before', ('normal','close'))
        after = record(function, replace(fixture, construction_overrides={}), 'after', ('normal','close'))
        for a, b in zip(before['images'], after['images'], strict=True):
            for key in ('camera_location', 'camera_target', 'ortho_scale'):
                assert a[key] == b[key]
        records.extend((before, after))
    # Capture the established Lowmark roof/frame/plinth vocabulary on a second
    # working program using the same studio and its existing benchmark camera.
    CASE_SPECS['STABLE'] = dict(CASE_SPECS['SMITHY'],
        targets={'normal':(8.7,3.,2.7)}, scales={'normal':31.})
    stable = replace(settings('STABLE'), construction_overrides={})
    records.append(record('STABLE', stable, 'reuse', ('normal',)))
    (OUT/'manifest.json').write_text(json.dumps(dict(blender=bpy.app.version_string,
                                                   control_revision='abfa9f0', source_sha256=source_hashes(),
                                                   cases=records), indent=2)+'\n')


def joinery_detail():
    function = 'SMITHY'
    spec = CASE_SPECS[function]
    spec['targets']['close'] = (2.8,.24,3.35)
    spec['scales']['close'] = 7.3
    spec['directions']['close'] = ((.36,-1.2,.19),(-.8,-1.2,.4))
    fixture = replace(settings(function), crafted_curves=True, seed_massing=True)
    before = record(function, fixture, 'joinery/before', ('close',))
    after = record(function, replace(fixture, construction_overrides={}), 'joinery/after', ('close',))
    for a, b in zip(before['images'], after['images'], strict=True):
        for key in ('camera_location','camera_target','ortho_scale'):
            assert a[key] == b[key]
    (OUT/'joinery'/'manifest.json').write_text(json.dumps(dict(
        blender=bpy.app.version_string, source_sha256=source_hashes(),
        cases=[before, after]),indent=2)+'\n')


if __name__ == '__main__':
    if '--joinery' in sys.argv:
        joinery_detail()
    else:
        main()

