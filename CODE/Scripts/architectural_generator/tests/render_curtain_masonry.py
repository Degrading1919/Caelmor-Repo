"""Compare one Thornfell curtain return with the fixed Gatehouse controls."""
from dataclasses import replace
from pathlib import Path
import json
import sys
import tempfile
from unittest.mock import patch

import bpy

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render_polish_benchmarks import build,capture,export_building,settings
from render_architectural_benchmarks import source_hashes
from render_world_evidence import _reset_scene
from render_roof_paint import snapshots
from test_condition_export import assert_glb_materials,check_reimport,read_glb
from caelmor_architecture import benchmark_gatehouse
from caelmor_architecture.blender_backend import _settings_dict
from caelmor_architecture.blender_backend import _colliders
from caelmor_architecture.curtain_masonry import dressed_curtain_return
from caelmor_architecture.engine import generate,geometry_hash,validate

OUT=ROOT/'evidence'/'curtain_masonry'
BASE=ROOT/'evidence'/'painted_materials'
CLAY=ROOT/'evidence'/'diversity_v12'


def collision_signature(objects):
    return sorted((obj['caelm_world_zone'],tuple(tuple(v.co) for v in obj.data.vertices),
                   tuple(tuple(p.vertices) for p in obj.data.polygons)) for obj in objects)


def main():
    if (OUT/'manifest.json').exists():
        raise ValueError('Curtain study already captured')
    s=replace(settings('GATEHOUSE'),crafted_curves=True,seed_massing=True)
    source=source_hashes()
    existing=json.loads((BASE/'manifest.json').read_text())
    clay=json.loads((CLAY/'after/manifest.json').read_text())
    controls={finish:next(im for row in record['cases'] if row['settings']==_settings_dict(s)
                          for im in row[key] if im['finish']==finish and im['view']==0)
              for finish,record,key in (('clay',clay,'images'),('material',existing,'after'))}
    baseline_plan,baseline_buffers=generate(s)
    baseline_hash=geometry_hash(baseline_buffers)
    assert any(row['settings']==_settings_dict(s) and row['geometry_hash']==baseline_hash
               for row in existing['cases'])
    original=benchmark_gatehouse._curtain_return

    def candidate(wall,start,end,station,base):
        if wall.name.endswith('curtain_return.east'):
            dressed_curtain_return(wall,start,end,station,base,s.seed)
        else:
            original(wall,start,end,station,base)

    _reset_scene()
    bpy.data.objects['Neutral ground'].location.z=0.
    proxies=_colliders(baseline_plan,'curtain_study')
    baseline_collision=collision_signature(proxies)
    for obj in proxies:
        mesh=obj.data
        bpy.data.objects.remove(obj)
        bpy.data.meshes.remove(mesh)
    with patch.object(benchmark_gatehouse,'_curtain_return',candidate):
        plan,buffers=generate(s)
        collection,_=build(s)
    assert collision_signature(obj for obj in collection.objects
                               if obj.get('caelm_collider'))==baseline_collision
    assert plan.functional_program==baseline_plan.functional_program
    assert collection['caelm_geometry_hash']==geometry_hash(buffers)
    assert len(baseline_buffers)==len(buffers)
    changed=[b.name for a,b in zip(baseline_buffers,buffers,strict=True)
             if geometry_hash([a])!=geometry_hash([b])]
    assert len(changed)==1 and changed[0].endswith('curtain_return.east')
    wall=next(b for b in buffers if b.name==changed[0])
    old_wall=next(b for b in baseline_buffers if b.name==changed[0])
    assert wall.material==old_wall.material
    bounds=[(min(p[i] for p in wall.vertices),max(p[i] for p in wall.vertices)) for i in range(3)]
    for route in plan.functional_program['routes']:
        b=route['bounds']
        assert any(hi<=b[i] or lo>=b[i+3] for i,(lo,hi) in enumerate(bounds)),route['key']
    original_mesh=validate(baseline_plan,baseline_buffers)
    candidate_mesh=validate(plan,buffers)
    assert candidate_mesh['valid'],candidate_mesh['errors']
    assert 0<candidate_mesh['triangles']-original_mesh['triangles']<=700
    frames=capture(collection,OUT/'after','GATEHOUSE',('clay','material'),('normal',),
                   views=(0,),vertex_framing=True)
    for frame in frames:
        before=controls[frame['finish']]
        assert all(before[key]==frame[key] for key in ('camera_location','camera_target','ortho_scale'))
    with tempfile.TemporaryDirectory(prefix='caelmor_curtain_') as temp:
        path=Path(temp)/'gatehouse.glb'
        meshes=[obj for obj in collection.objects if obj.get('caelm_buffer_id')==wall.name]
        material_snapshots=snapshots(meshes)
        export_building(collection,str(path))
        doc,binary=read_glb(path)
        export=assert_glb_materials(doc,binary)
        size=path.stat().st_size
        reimport=check_reimport(path,material_snapshots)
        assert reimport['reimported_pixel_map_checks']==4
        imported=next(obj for obj in bpy.context.scene.objects if obj.name==wall.name)
        imported.data.calc_loop_triangles()
        assert len(imported.data.loop_triangles)==sum(len(face)-2 for face in wall.faces)
    assert source==source_hashes()
    (OUT/'manifest.json').write_text(json.dumps(dict(
        blender=bpy.app.version_string,source_sha256=source,settings=_settings_dict(s),
        material_control_revision='2a260e9',clay_control_revision=clay['revision'],
        geometry_hashes=[baseline_hash,candidate_mesh['geometry_hash']],
        triangles=[original_mesh['triangles'],candidate_mesh['triangles']],
        changed_buffers=changed,candidate_wall_bounds=bounds,
        unchanged_collision_proxies=len(baseline_collision),
        clear_route_bounds=len(plan.functional_program['routes']),
        baseline=controls,after=frames,glb_bytes=size,material_export=export,reimport=reimport),
        indent=2)+'\n')
    print('CURTAIN_MASONRY_PASS',candidate_mesh['triangles']-original_mesh['triangles'],reimport)


if __name__=='__main__':
    main()
