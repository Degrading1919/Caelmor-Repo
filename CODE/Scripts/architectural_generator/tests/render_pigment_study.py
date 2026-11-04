"""One seed per material family, using the existing studio and GLB checks."""
from dataclasses import replace
from pathlib import Path
import json
import sys

import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render_masonry_stock import mapped_payloads
from render_polish_benchmarks import build,capture,export_building,settings
from render_world_evidence import _reset_scene
from render_architectural_benchmarks import source_hashes
from test_condition_export import assert_glb_materials,check_reimport,linked_image,read_glb
from caelmor_architecture.blender_backend import _settings_dict
from caelmor_architecture.benchmark_finish import uses_hewn_pigment,uses_masonry_stock

OUT=ROOT/'evidence/painted_materials'
BASE=ROOT/'evidence/diversity_v12'
MASONRY=ROOT/'evidence/masonry_stock'


def run_case(function, baseline):
    s=replace(settings(function),crafted_curves=True,seed_massing=True)
    row=next(case for case in baseline['cases'] if case['settings']==_settings_dict(s))
    if function=='SMITHY':
        before_dir=BASE/'after'
        before=[img for img in row['images'] if img['finish']=='material']
        old_glb=BASE/'export_validation/smithy.glb'
        scoped=uses_hewn_pigment
    else:
        previous=json.loads((MASONRY/'comparison.json').read_text())
        before_dir=MASONRY/'after'
        before=previous['after']
        old_glb=MASONRY/'gatehouse.glb'
        scoped=uses_masonry_stock
    _reset_scene()
    bpy.data.objects['Neutral ground'].location.z=0.
    collection,metrics=build(s)
    assert collection['caelm_geometry_hash']==row['geometry_hash']
    after=capture(collection,OUT/'after',function,('material',),('normal',),vertex_framing=True)
    for old,new in zip(before,after,strict=True):
        assert all(old[k]==new[k] for k in ('camera_location','camera_target','ortho_scale'))

    materials={o.data.materials[0] for o in collection.objects if o.type=='MESH'
               and scoped(o.get('caelm_buffer_id',''),s)}
    assert materials
    samples={}
    for mat in materials:
        snapshots={}
        for socket in ('Base Color','Normal','Roughness','Metallic'):
            im=linked_image(mat,socket)
            pixels=np.empty(len(im.pixels),dtype=np.float32)
            im.pixels.foreach_get(pixels)
            stride=max(4,len(pixels)//2048//4*4)
            snapshots[socket]=dict(size=tuple(im.size),signature=im.name,
                                   pixel_count=len(pixels),
                                   samples=[(i,float(pixels[i])) for i in range(0,len(pixels),stride)])
        samples[mat.name]=snapshots
    path=OUT/(function.lower()+'.glb')
    export_building(collection,str(path))
    doc,binary=read_glb(path)
    export=assert_glb_materials(doc,binary)
    new=mapped_payloads(path)
    changed=None
    if old_glb.is_file():
        old=mapped_payloads(old_glb)
        assert old.keys()==new.keys()
        changed=[name for name in new if new[name]!=old[name]]
        assert changed and any(scoped(name,s) for name in changed)
        assert all(new[n]['normal']==old[n]['normal'] and new[n]['orm']==old[n]['orm']
                   and new[n]['base'][0]==old[n]['base'][0] for n in new)
        if function=='GATEHOUSE':
            assert all(scoped(name,s) for name in changed)
    reimport=check_reimport(path,samples)
    assert reimport['reimported_pixel_map_checks']==len(materials)*4
    return dict(settings=_settings_dict(s),geometry_hash=row['geometry_hash'],metrics=metrics,
                before_directory=before_dir.relative_to(ROOT).as_posix(),before=before,after=after,
                mapped_meshes=len(new),changed_basecolor_bindings=changed,material_export=export,
                glb_bytes=path.stat().st_size,baseline_glb_bytes=old_glb.stat().st_size if old_glb.is_file() else None,
                reimport=reimport)


def main():
    baseline=json.loads((BASE/'after/manifest.json').read_text())
    source=source_hashes()
    cases=[run_case(function,baseline) for function in ('SMITHY','GATEHOUSE')]
    assert source==source_hashes()
    (OUT/'manifest.json').write_text(json.dumps(dict(
        blender=bpy.app.version_string,source_sha256=source,
        smithy_baseline_revision=baseline['revision'],gatehouse_baseline_revision='8bb4dd7',
        cases=cases),indent=2)+'\n')
    print('PAINTED_MATERIALS_PASS',[(c['settings']['function'],c['reimport']) for c in cases])


if __name__=='__main__':
    main()
