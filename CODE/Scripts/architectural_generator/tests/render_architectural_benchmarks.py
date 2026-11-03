"""Capture staged, fixed-camera architectural function benchmarks in Blender.

Example:
  blender --background --python tests/render_architectural_benchmarks.py -- \
    --stage before --source-revision 39f2e6c
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render_world_evidence import _reset_scene,_materials,_neutral_material,_aim,_bounds
from caelmor_architecture.blender_backend import build
from caelmor_architecture.engine import generate,validate,geometry_hash
from caelmor_architecture.model import Settings

CASE_SPECS={
    'SMITHY':{
        'region':'LOWMARK','targets':{'normal':(4,1.6,3.2),'distant':(4,1.6,3.2),'close':(2.6,1.3,1.7)},
        'scales':{'normal':18.0,'distant':32.0,'close':7.5},
        'camera_distances':{'normal':40.0,'distant':64.0,'close':18.0},
        'directions':{'normal':((.85,-1.2,.68),(-.85,1.2,.68)),
                      'distant':((.85,-1.2,.68),(-.85,1.2,.68)),
                      'close':((.65,-1.2,.40),(-.8,-1.2,.4))},
        'view_names':{'normal':('front','rear'),'distant':('front','rear'),
                      'close':('workfront_a','workfront_b')}
    },
    'GATEHOUSE':{
        'region':'THORNFELL','targets':{'normal':(7.9,3,6.8),'distant':(7.9,3,6.8),
                                         'close_front':(7.9,.4,2.9),'close_rear':(7.9,8.0,2.9)},
        'scales':{'normal':38.0,'distant':64.0,'close':9.0},
        'camera_distances':{'normal':58.0,'distant':96.0,'close':24.0},
        'directions':{'normal':((.85,-1.2,.68),(-.85,1.2,.68)),
                      'distant':((.85,-1.2,.68),(-.85,1.2,.68)),
                      'close':((.85,-1.2,.68),(-.85,1.2,.68))},
        'view_names':{'normal':('front','rear'),'distant':('front','rear'),
                      'close':('front','rear')}
    }
}
DISTANCES=('normal','distant','close')
FINISHES=('clay','material')
VIEWS=(0,1)
WIDTH=1024; HEIGHT=704; SAMPLES=32


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def source_hashes():
    base=ROOT/'caelmor_architecture'
    return {p.relative_to(base).as_posix():sha(p) for p in sorted(base.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}

def frame_test(camera,bounds,target):
    aspect=WIDTH/HEIGHT
    q=camera.rotation_euler.to_quaternion()
    inverse=q.inverted()
    projected=[inverse@(Vector((x,y,z))-Vector(target)) for x in bounds[0]
               for y in bounds[1] for z in bounds[2]]
    half_width=camera.data.ortho_scale*.5
    half_height=half_width/aspect
    pad=.985
    minx=min(p.x for p in projected); maxx=max(p.x for p in projected)
    miny=min(p.y for p in projected); maxy=max(p.y for p in projected)
    ok=(minx>=-half_width*pad and maxx<=half_width*pad and
        miny>=-half_height*pad and maxy<=half_height*pad)
    return {'valid':ok,'projected_bounds':{'x':[minx,maxx],'y':[miny,maxy]},
            'frame_bounds':{'x':[-half_width,half_width],'y':[-half_height,half_height]},
            'safety_margin_fraction':1-pad}

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('--stage',choices=('before','pilot1','pilot2','after'),required=True)
    parser.add_argument('--source-revision',required=True)
    parser.add_argument('--cases',nargs='*',choices=tuple(CASE_SPECS),default=list(CASE_SPECS))
    parser.add_argument('--distances',nargs='+',choices=DISTANCES,default=DISTANCES)
    return parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])

def main():
    args=parse_args(); out=ROOT/'evidence'/'benchmarks_v08'/args.stage
    if args.stage=='before' and (out/'manifest.json').exists():
        previous=json.loads((out/'manifest.json').read_text())
        if previous.get('case_count')==2 and previous.get('image_count')==24:
            raise RuntimeError('The completed before baseline is immutable')
    out.mkdir(parents=True,exist_ok=True)
    (out/'individual').mkdir(exist_ok=True)
    (out/'cases').mkdir(exist_ok=True)
    source_before=source_hashes()
    render_sources={p.name:sha(p) for p in (Path(__file__),Path(__file__).with_name('render_world_evidence.py'))}
    all_case_records=[]
    for function in args.cases:
        spec=CASE_SPECS[function]; region=spec['region']
        settings=Settings(seed=91,function=function,region=region,wealth='ESTABLISHED',
                          craftsmanship='STANDARD',age=35,maintenance=.7,detail='MEDIUM',
                          geometry_mode='EFFICIENT',world_aware=True,use_grammar=True,context='AUTO')
        started=time.perf_counter()
        plan,buffers=generate(settings); validation=validate(plan,buffers)
        if not validation['valid']:
            raise RuntimeError(f'{function} {region} pure validation failed: {validation["errors"]}')
        scene,camera=_reset_scene()
        scene.render.resolution_x=WIDTH;scene.render.resolution_y=HEIGHT
        scene.render.resolution_percentage=100;scene.eevee.taa_render_samples=SAMPLES
        bpy.data.objects['Neutral ground'].location.z=0.
        collection,backend_metrics=build(settings)
        bpy.context.view_layer.update()
        native_bounds=_bounds(collection)
        native_hash=collection.get('caelm_geometry_hash')
        pure_hash=geometry_hash(buffers)
        if native_hash and native_hash!=pure_hash:
            raise RuntimeError(f'{function} backend/pure geometry hashes differ: {native_hash} != {pure_hash}')
        native_validation=json.loads(collection.get('caelm_validation','{}'))
        if native_validation and not native_validation.get('valid',False):
            raise RuntimeError(f'{function} native backend validation failed: {native_validation}')
        original_materials=[(obj,tuple(obj.data.materials)) for obj in collection.objects if obj.type=='MESH']
        collection.hide_render=False
        clay=_neutral_material()
        render_records=[]
        # Group finishes as in the established gallery: swapping material slots
        # for every angle repeatedly invalidates Eevee's material draw caches.
        for finish in FINISHES:
            if finish=='clay':_materials(collection,clay)
            else:
                for obj,materials in original_materials:
                    obj.data.materials.clear()
                    for material in materials:obj.data.materials.append(material)
            for distance in args.distances:
              for view,direction in enumerate(spec['directions'][distance]):
                target_key=('close_front' if function=='GATEHOUSE' and distance=='close' and view==0 else
                            'close_rear' if function=='GATEHOUSE' and distance=='close' else distance)
                target=spec['targets'][target_key]
                camera_distance=spec['camera_distances'][distance]
                direction_vec=Vector(direction).normalized()
                camera_target=Vector(target)
                camera_location=camera_target+direction_vec*camera_distance
                _aim(camera,camera_location,camera_target)
                camera.data.ortho_scale=spec['scales'][distance]
                framing=(frame_test(camera,native_bounds,target) if distance in ('normal','distant')
                         else {'valid':None,'note':'Intentional close crop; full building bounds are not required.'})
                if distance in ('normal','distant') and not framing['valid']:
                    raise RuntimeError(f'{function} {distance} view {view} crops fixed full-building frame: {framing}')
                view_name=spec['view_names'][distance][view]
                relative=f'individual/{function.lower()}/{distance}_{finish}_{view_name}.png'
                image_path=out/relative;image_path.parent.mkdir(parents=True,exist_ok=True)
                scene.render.filepath=str(image_path)
                bpy.ops.render.render(write_still=True)
                render_records.append({'distance':distance,'finish':finish,'view':view,
                    'view_name':view_name,'image':relative,'image_sha256':sha(image_path),
                    'width':WIDTH,'height':HEIGHT,'samples':SAMPLES,
                    'camera_target':list(camera_target),'camera_direction':list(direction),
                    'camera_location':list(camera_location),'ortho_scale':spec['scales'][distance],
                    'framing_check':framing})
        record={'function':function,'region':region,'settings':asdict(settings),
                'source_revision':args.source_revision,'generator_source_sha256':source_before,
                'render_source_sha256':render_sources,'geometry_hash':native_hash or pure_hash,
                'pure_geometry_hash':pure_hash,'bounds':native_bounds,
                'pure_validation':validation,'native_validation':native_validation,
                'backend_metrics':backend_metrics,'build_seconds':round(time.perf_counter()-started,4),
                'renderer':bpy.app.version_string,'engine':scene.render.engine,
                'resolution':[WIDTH,HEIGHT],'samples':SAMPLES,
                'studio':'render_world_evidence._reset_scene; unchanged neutral studio',
                'images':render_records,'image_count':len(render_records)}
        case_path=out/'cases'/f'{function.lower()}.json'
        case_path.write_text(json.dumps(record,indent=2),encoding='utf-8')
        if args.stage=='after':
            bpy.ops.wm.save_as_mainfile(filepath=str(out/f'{function.lower()}.blend'))
        all_case_records.append({'function':function,'region':region,'manifest':case_path.relative_to(out).as_posix(),
                                 'manifest_sha256':sha(case_path),'image_count':len(render_records),
                                 'geometry_hash':record['geometry_hash']})
        print(f'BENCHMARK_CASE_COMPLETE={function} images={len(render_records)}',flush=True)
        bpy.ops.wm.read_factory_settings(use_empty=True)
    # Include unselected cases already captured in this stage only after checking
    # their provenance and every retained image hash. This supports the bounded
    # one-case Gatehouse framing correction without rerendering Smithy.
    for function in CASE_SPECS:
        if function in args.cases:continue
        case_path=out/'cases'/f'{function.lower()}.json'
        if not case_path.exists():continue
        retained=json.loads(case_path.read_text(encoding='utf-8'))
        if retained['source_revision']!=args.source_revision or retained['generator_source_sha256']!=source_before:
            raise RuntimeError(f'Retained case source mismatch: {function}')
        for image in retained['images']:
            image_path=out/image['image']
            if not image_path.is_file() or sha(image_path)!=image['image_sha256']:
                raise RuntimeError(f'Retained image missing/hash mismatch: {function} {image["image"]}')
        all_case_records.append({'function':function,'region':retained['region'],
            'manifest':case_path.relative_to(out).as_posix(),'manifest_sha256':sha(case_path),
            'image_count':len(retained['images']),'geometry_hash':retained['geometry_hash'],
            'reused_existing_verified_case':True})
    source_after=source_hashes()
    if source_after!=source_before:raise RuntimeError('Generator source changed during benchmark capture')
    all_case_records=sorted(all_case_records,key=lambda row:tuple(CASE_SPECS).index(row['function']))
    render_hashes={row['function']:json.loads((out/row['manifest']).read_text(encoding='utf-8'))['render_source_sha256'] for row in all_case_records}
    stage_record={'stage':args.stage,'source_revision':args.source_revision,
                  'generator_source_sha256':source_before,'render_source_sha256_by_case':render_hashes,
                  'cases':all_case_records,'case_count':len(all_case_records),
                  'image_count':sum(x['image_count'] for x in all_case_records),
                  'source_unchanged_during_capture':True}
    (out/'manifest.json').write_text(json.dumps(stage_record,indent=2),encoding='utf-8')
    print(f'BENCHMARK_STAGE_COMPLETE={args.stage} cases={len(all_case_records)} images={stage_record["image_count"]}',flush=True)

if __name__=='__main__':main()
