"""v10 controlled art experiment and release evidence; reuse v08 studio/cameras."""
import argparse,json,sys,time
from dataclasses import asdict, replace
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from render_architectural_benchmarks import CASE_SPECS,WIDTH,HEIGHT,SAMPLES,sha,source_hashes,frame_test
from render_world_evidence import _reset_scene,_aim,_materials,_neutral_material,_bounds
from caelmor_architecture.blender_backend import build,export_building,TAG
from caelmor_architecture.model import Settings
from caelmor_architecture.engine import generate,geometry_hash,validate


def settings(function):
    return Settings(function=function,region=CASE_SPECS[function]['region'],seed=91,world_aware=True,
                    use_grammar=True,detail='MEDIUM',geometry_mode='EFFICIENT',age=35,maintenance=.7)


def capture(collection,out,function,finishes=('clay','material'),distances=('distant','normal','close'),views=(0,1)):
    scene=bpy.context.scene;camera=scene.camera;spec=CASE_SPECS[function]
    scene.render.resolution_x=WIDTH;scene.render.resolution_y=HEIGHT;scene.render.resolution_percentage=100
    scene.eevee.taa_render_samples=SAMPLES
    bpy.context.view_layer.update();bounds=_bounds(collection)
    original=[(o,tuple(o.data.materials)) for o in collection.objects if o.type=='MESH']
    clay=_neutral_material();records=[]
    for finish in finishes:
        if finish=='clay':_materials(collection,clay)
        else:
            for o,mats in original:
                o.data.materials.clear()
                for m in mats:o.data.materials.append(m)
        for distance in distances:
            for view in views:
                target_key=('close_front' if view==0 else 'close_rear') if function=='GATEHOUSE' and distance=='close' else distance
                target=Vector(spec['targets'][target_key]);direction=Vector(spec['directions'][distance][view]).normalized()
                location=target+direction*spec['camera_distances'][distance]
                _aim(camera,location,target);camera.data.ortho_scale=spec['scales'][distance]
                framing=frame_test(camera,bounds,target) if distance!='close' else {'valid':None,'note':'intentional close crop'}
                if distance!='close':assert framing['valid'],framing
                path=out/function.lower()/f'{distance}_{finish}_{view}.png';path.parent.mkdir(parents=True,exist_ok=True)
                scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
                records.append(dict(function=function,distance=distance,finish=finish,view=view,
                    image=path.relative_to(out).as_posix(),sha256=sha(path),camera_location=list(location),
                    camera_target=list(target),ortho_scale=camera.data.ortho_scale,framing=framing))
    for o,mats in original:
        o.data.materials.clear()
        for m in mats:o.data.materials.append(m)
    return records


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['before','pilot','after'],required=True)
    parser.add_argument('--source-revision',required=True)
    parser.add_argument('--label')
    parser.add_argument('--seed',type=int,default=91)
    parser.add_argument('--curves',action='store_true',help='Capture the crafted-curves comparison')
    parser.add_argument('--cases',nargs='+',default=list(CASE_SPECS),choices=list(CASE_SPECS))
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if args.seed != 91 and (not args.curves or args.stage != 'pilot' or not args.label):
        parser.error('Alternate seeds require a named crafted-curves pilot')
    if args.curves and args.stage=='before':
        parser.error('Crafted curves reuse the immutable v10 after capture as their control')
    folder='curves_v11' if args.curves else 'polish_v10'
    out=ROOT/'evidence'/folder/(args.label or args.stage)
    out.mkdir(parents=True,exist_ok=True)
    if args.stage=='before' and (out/'manifest.json').exists():raise RuntimeError('Completed control capture is immutable')
    sources=source_hashes();records=[];cases=[]
    for function in args.cases:
        s=settings(function)
        if args.stage in ('before','pilot') and not args.curves:
            old=ROOT/'evidence/materials_v09/final'/(function.lower()+'.blend')
            bpy.ops.wm.open_mainfile(filepath=str(old))
            collection=next(c for c in bpy.data.collections if c.get('caelm_build'))
            cases.append(dict(function=function,settings=json.loads(collection['caelm_settings']),
                geometry_hash=collection['caelm_geometry_hash'],input_blend_sha256=sha(old),input_source_revision='094eb8c'))
            if args.stage=='before':records+=capture(collection,out,function);continue
            # Material-only diagnostic on the immutable old geometry.
            from caelmor_architecture.surface_atlas import apply_surfaces
            plan,_=generate(s)
            objects=[o for o in collection.objects if o.get(TAG) and not o.get('caelm_collider')]
            apply_surfaces(objects,plan,s)
            material_records=capture(collection,out/'material_only',function,('material',),('normal',),(0,))
            for row in material_records:row['image']='material_only/'+row['image'];row['variant']='material_only'
            records+=material_records
        if args.curves:
            s=replace(s,crafted_curves=True,seed=args.seed)
        _reset_scene();bpy.data.objects['Neutral ground'].location.z=0.
        started=time.perf_counter();collection,metrics=build(s)
        plan,buffers=generate(s);checks=validate(plan,buffers);assert checks['valid'],checks['errors']
        assert geometry_hash(buffers)==collection['caelm_geometry_hash']
        if args.curves and args.stage=='pilot':
            cases.append(dict(function=function,settings=asdict(s),metrics=metrics,
                              geometry_hash=geometry_hash(buffers)))
        dest=out/'crafted' if args.stage=='pilot' else out
        generated_records=capture(collection,dest,function,('clay','material'),('normal',) if args.stage=='pilot' else ('distant','normal','close'),(0,) if args.stage=='pilot' else (0,1))
        if args.stage=='pilot':
            for row in generated_records:row['image']='crafted/'+row['image'];row['variant']='crafted'
        records+=generated_records
        if args.stage=='after':
            bpy.ops.wm.save_as_mainfile(filepath=str(out/(function.lower()+'.blend')))
            export=out/(function.lower()+'.glb');export_building(collection,str(export))
            cases.append(dict(function=function,settings=asdict(s),geometry_hash=geometry_hash(buffers),
                validation=checks,metrics=metrics,surfaces=json.loads(collection['caelm_surface_diagnostics']),
                export_sha256=sha(export),native_blend_sha256=sha(out/(function.lower()+'.blend')),
                authoring_seconds=round(time.perf_counter()-started,3)))
            # The imported asset is rendered with the exact same studio/cameras.
            _reset_scene();bpy.data.objects['Neutral ground'].location.z=0.
            before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(export))
            imported=[o for o in bpy.context.scene.objects if o not in before]
            imported_collection=bpy.data.collections.new('GLB appearance');bpy.context.scene.collection.children.link(imported_collection)
            for o in imported:imported_collection.objects.link(o)
            imported_records=capture(imported_collection,out/'exported',function,('material',),('distant','normal','close'),(0,1))
            for row in imported_records:row['image']='exported/'+row['image'];row['finish']='exported_material'
            records+=imported_records
        print('POLISH_CASE_COMPLETE',args.stage,function,flush=True)
    unchanged=sources==source_hashes()
    if args.stage=='after':assert unchanged,'Source changed during final capture'
    (out/'manifest.json').write_text(json.dumps(dict(stage=args.stage,source_revision=args.source_revision,
        control='polish_v10/after/manifest.json' if args.curves else None,
        generator_sha256=sources,source_unchanged_during_capture=unchanged,blender=bpy.app.version_string,
        render_script_sha256=sha(__file__),cases=cases,images=records,image_count=len(records)),indent=2)+'\n')
    print('POLISH_CAPTURE_PASS',args.stage,len(records),flush=True)

if __name__=='__main__':main()
