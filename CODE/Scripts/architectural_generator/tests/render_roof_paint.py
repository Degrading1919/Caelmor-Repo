"""Render two roof-only treatments against the existing fixed-camera baseline."""
from dataclasses import asdict, replace
from pathlib import Path
import json
import sys
import tempfile

import bpy
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render_masonry_stock import mapped_payloads
from render_polish_benchmarks import build,capture,export_building,settings
from render_world_evidence import _reset_scene
from render_architectural_benchmarks import source_hashes
from test_condition_export import assert_glb_materials,check_reimport,linked_image,read_glb
from caelmor_architecture.engine import generate,geometry_hash
from caelmor_architecture.surface_atlas import FAMILY,apply_surfaces

OUT=ROOT/'evidence'/'roof_paint'
CONTROL=ROOT/'evidence'/'painted_materials'


def snapshots(objects):
    result={}
    for mat in {obj.data.materials[0] for obj in objects}:
        result[mat.name]={}
        for socket in ('Base Color','Normal','Roughness','Metallic'):
            image=linked_image(mat,socket)
            pixels=np.empty(len(image.pixels),dtype=np.float32)
            image.pixels.foreach_get(pixels)
            stride=max(4,len(pixels)//1024//4*4)
            result[mat.name][socket]=dict(size=tuple(image.size),signature=image.name,
                                         pixel_count=len(pixels),
                                         samples=[(i,float(pixels[i])) for i in range(0,len(pixels),stride)])
    return result


def compare_maps(previous,current,roof_ids):
    assert previous.keys()==current.keys()
    changed=[name for name in current if current[name]!=previous[name]]
    assert changed and set(changed)<=roof_ids, changed
    assert all(current[n]['normal']==previous[n]['normal']
               and current[n]['orm']==previous[n]['orm']
               and current[n]['base'][0]==previous[n]['base'][0] for n in current)
    return changed


def run_case(function,baseline,scratch):
    s=replace(settings(function),crafted_curves=True,seed_massing=True)
    prior=next(row for row in baseline['cases'] if row['settings']==asdict(s))
    before=next(frame for frame in prior['after'] if frame['view']==0)
    _reset_scene()
    bpy.data.objects['Neutral ground'].location.z=0.
    collection,_=build(s)
    plan,buffers=generate(s)
    assert geometry_hash(buffers)==collection['caelm_geometry_hash']==prior['geometry_hash']
    objects=[obj for obj in collection.objects if obj.type=='MESH' and not obj.get('caelm_collider')]
    roof=[obj for obj in objects if FAMILY.get(obj.get('caelm_material'))=='roof']
    roof_ids={obj.name for obj in roof}
    assert roof
    original=[tuple(obj.data.materials) for obj in objects if obj not in roof]
    baseline_glb=CONTROL/(function.lower()+'.glb')
    if not baseline_glb.exists():
        baseline_glb=scratch/(function.lower()+'_baseline.glb')
        export_building(collection,str(baseline_glb))
    previous=mapped_payloads(baseline_glb)
    treatments={}
    for mode in ('PIGMENT','COURSES'):
        apply_surfaces(roof,plan,s,context_objects=objects,roof_finish=mode)
        frames=capture(collection,OUT/mode.lower(),function,('material',),('normal',),
                       views=(0,),vertex_framing=True)
        frame=frames[0]
        assert all(frame[k]==before[k] for k in ('camera_location','camera_target','ortho_scale'))
        assert original==[tuple(obj.data.materials) for obj in objects if obj not in roof]
        path=scratch/f'{function.lower()}_{mode.lower()}.glb'
        export_building(collection,str(path))
        doc,binary=read_glb(path)
        current=mapped_payloads(path)
        assert len(doc['images'])==prior['material_export']['embedded_image_count']
        changed=compare_maps(previous,current,roof_ids)
        treatments[mode]=dict(frame=frame,changed_bindings=changed,glb_bytes=path.stat().st_size,
                              image_count=len(doc['images']))
        if mode=='COURSES':
            compare_maps(pigment,current,roof_ids)
            export=assert_glb_materials(doc,binary)
            images=snapshots(roof)
            reimport=check_reimport(path,images)
            assert reimport['reimported_pixel_map_checks']==4*len(images)
            treatments[mode].update(material_export=export,reimport=reimport)
        else:
            pigment=current
    return dict(settings=asdict(s),geometry_hash=prior['geometry_hash'],
                baseline=before,baseline_glb_bytes=baseline_glb.stat().st_size,treatments=treatments)


def main():
    if (OUT/'manifest.json').exists():
        raise ValueError('Roof comparison already completed')
    baseline=json.loads((CONTROL/'manifest.json').read_text())
    source=source_hashes()
    with tempfile.TemporaryDirectory(prefix='caelmor_roof_') as temp:
        cases=[run_case(f,baseline,Path(temp)) for f in ('SMITHY','GATEHOUSE')]
    assert source==source_hashes()
    (OUT/'manifest.json').write_text(json.dumps(dict(
        blender=bpy.app.version_string,baseline_revision='2a260e9',
        source_sha256=source,cases=cases),indent=2)+'\n')
    print('ROOF_PAINT_PASS',len(cases))


if __name__=='__main__':
    main()
