"""Controlled surface-only sweeps using the existing v08 cameras and studio.

No mesh generation occurs between condition variants. Actual production build
still uses all normal grammar controls; this diagnostic isolates their finishes.
"""
import argparse
from dataclasses import asdict,replace
import hashlib,json,sys,time
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from render_architectural_benchmarks import CASE_SPECS,WIDTH,HEIGHT,SAMPLES,source_hashes,sha,frame_test
from render_world_evidence import _reset_scene,_aim,_bounds
from caelmor_architecture.model import Settings
from caelmor_architecture.engine import generate,geometry_hash
from caelmor_architecture.blender_backend import build,TAG
from caelmor_architecture.surface_atlas import apply_surfaces

VARIANTS={
    'reference':{},
    'young':{'age':5},'old':{'age':120},
    'neglected':{'age':120,'maintenance':.15},'maintained':{'age':120,'maintenance':.95},
    'modest':{'wealth':'MODEST'},'affluent':{'wealth':'AFFLUENT'},
    'rough':{'craftsmanship':'ROUGH'},'fine':{'craftsmanship':'FINE'},
    'modest_maintained':{'age':120,'maintenance':.95,'wealth':'MODEST'},
    'affluent_neglected':{'age':120,'maintenance':.15,'wealth':'AFFLUENT'},
}


def unused_maps():
    # This fresh evidence scene has no user work. Remove only unused generated
    # maps/banks between variants; never run global orphan purge in production.
    for mat in list(bpy.data.materials):
        if mat.users==0 and (mat.get('caelm_surface_fingerprint') or mat.get('caelm_material')):
            bpy.data.materials.remove(mat)
    for image in list(bpy.data.images):
        if image.users==0 and (image.get('caelm_atlas_revision') or image.get('caelm_original')):
            bpy.data.images.remove(image)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--stage',default='pilot')
    parser.add_argument('--source-revision',default='development')
    parser.add_argument('--cases',nargs='+',default=list(CASE_SPECS),choices=list(CASE_SPECS))
    parser.add_argument('--variants',nargs='+',default=list(VARIANTS),choices=list(VARIANTS))
    parser.add_argument('--distances',nargs='+',default=['normal','close'],choices=['normal','close'])
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=ROOT/'evidence/materials_v09'/args.stage;out.mkdir(parents=True,exist_ok=True)
    sources=source_hashes();records=[]
    previous=json.loads((ROOT/'evidence/benchmarks_v08/after/manifest.json').read_text())
    hashes={c['function']:c['geometry_hash'] for c in previous['cases']}
    for function in args.cases:
        spec=CASE_SPECS[function]
        settings=Settings(function=function,region=spec['region'],seed=91,world_aware=True,use_grammar=True,
            detail='MEDIUM',geometry_mode='EFFICIENT',wealth='ESTABLISHED',craftsmanship='STANDARD',age=35,maintenance=.7)
        scene,camera=_reset_scene();scene.render.resolution_x=WIDTH;scene.render.resolution_y=HEIGHT
        scene.eevee.taa_render_samples=SAMPLES;bpy.data.objects['Neutral ground'].location.z=0.
        plan,buffers=generate(settings);assert geometry_hash(buffers)==hashes[function]
        started=time.perf_counter();collection,_=build(settings)
        print('MATERIAL_BUILD',function,round(time.perf_counter()-started,3),flush=True)
        objects=[o for o in collection.objects if o.get(TAG) and not o.get('caelm_collider')]
        bpy.context.view_layer.update();bounds=_bounds(collection)
        for variant in args.variants:
            finish=replace(settings,**VARIANTS[variant])
            started=time.perf_counter();diagnostics=apply_surfaces(objects,plan,finish);unused_maps()
            print('MATERIAL_FINISH',function,variant,round(time.perf_counter()-started,3),flush=True)
            for distance in args.distances:
                target=spec['targets']['close_front' if function=='GATEHOUSE' and distance=='close' else distance]
                direction=Vector(spec['directions'][distance][0]).normalized()
                location=Vector(target)+direction*spec['camera_distances'][distance]
                _aim(camera,location,target);camera.data.ortho_scale=spec['scales'][distance]
                if distance=='normal':assert frame_test(camera,bounds,target)['valid']
                path=out/function.lower()/f'{variant}_{distance}.png';path.parent.mkdir(exist_ok=True)
                scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
                records.append(dict(function=function,variant=variant,distance=distance,image=path.relative_to(out).as_posix(),
                    image_sha256=sha(path),geometry_settings=asdict(settings),surface_settings=asdict(finish),
                    geometry_hash=hashes[function],camera_target=list(target),camera_location=list(location),
                    ortho_scale=camera.data.ortho_scale,resolution=[WIDTH,HEIGHT],surfaces=diagnostics))
            if variant=='reference' and args.stage=='final':
                bpy.ops.wm.save_as_mainfile(filepath=str(out/(function.lower()+'.blend')))
        print('MATERIAL_CASE_COMPLETE',function,flush=True)
    unchanged=sources==source_hashes()
    if args.stage=='final':assert unchanged,'Source changed during capture'
    manifest=dict(source_revision=args.source_revision,source_hashes=sources,source_unchanged_during_capture=unchanged,blender=bpy.app.version_string,
        scope='Surface-only diagnostic; fixed generated v08 geometry; production grammar still honors all controls.',
        studio='render_world_evidence._reset_scene, ground z=0 as v08 benchmark capture',
        image_count=len(records),images=records)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('MATERIAL_CAPTURE_COMPLETE',len(records),flush=True)

if __name__=='__main__':main()
