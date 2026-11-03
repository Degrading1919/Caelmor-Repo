"""Small matched household study, common scale per region across wealth tiers.

blender --background --python tests/render_household_review.py -- --stage study1
Use --regions MIRE to refresh an affected region; --pbr retains real materials.
"""
import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import sys
import time

import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render_world_evidence import _reset_scene, _materials, _neutral_material, _aim
from caelmor_architecture.engine import generate,validate,geometry_hash
from caelmor_architecture.model import Settings
from caelmor_architecture.blender_backend import build

REGIONS=('LOWMARK','THORNFELL','MIRE','EMBERHOLT')
TIERS=('MODEST','ESTABLISHED','AFFLUENT')
VIEWS=((.85,-1.2,.68),(-.85,1.2,.68))


def archetype_gallery(args):
    """Evidence-only matrix: build once, reuse native geometry for both finishes.

    Reuses this module's existing studio, opposing views and camera-fit math.
    All four native collections share one scene per archetype, hidden in turn.
    """
    from caelmor_architecture.profiles import TYPE_SPECS
    from caelmor_architecture.model import resolve_settings
    from caelmor_architecture import engine
    from render_world_evidence import _bounds
    import traceback

    if Path(args.gallery_output).name!=args.gallery_output:
        raise ValueError('Gallery output must be a single evidence folder name')
    out=ROOT/'evidence'/args.gallery_output
    (out/'manifests').mkdir(parents=True,exist_ok=True)
    files=list((ROOT/'caelmor_architecture').glob('*.py'))
    selected_functions=set(args.gallery_functions or TYPE_SPECS)
    unused=set()
    if not selected_functions.intersection(('SMITHY','MARKET_HALL')):unused.add('function_work.py')
    if not selected_functions.intersection(('STABLE','GATEHOUSE')):unused.add('function_yard.py')
    files=[p for p in files if p.name not in unused]
    files += [ROOT/'caelmor_architecture'/'blender_manifest.toml']
    def source_hashes():
        return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    source=source_hashes()
    render_source={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in (Path(__file__),Path(__file__).with_name('render_world_evidence.py'))}
    contract=asdict(Settings(seed=91,wealth='ESTABLISHED',craftsmanship='STANDARD',
                    age=35,maintenance=.7,detail='MEDIUM',geometry_mode='EFFICIENT',
                    use_grammar=True,world_aware=True))
    contract.pop('function');contract.pop('region')
    functions=args.gallery_functions or tuple(TYPE_SPECS)
    for function in functions:
        if function not in TYPE_SPECS:raise ValueError('Unsupported archetype '+function)
        manifest_path=out/'manifests'/f'{function.lower()}.json'
        retained=[]
        if args.gallery_refresh and manifest_path.exists():
            old=json.loads(manifest_path.read_text())
            if old['settings_contract']!=contract:raise RuntimeError('Refresh settings changed: '+function)
            for row in old['records']:
                if row['region'] in args.regions:continue
                row.setdefault('source_revision',old['source_revision'])
                row.setdefault('source_sha256',old['source_sha256'])
                row.setdefault('render_source_sha256',old['render_source_sha256'])
                # Retain only exact geometry. Original render provenance stays
                # attached to the row; this is not a pixel identity assertion.
                retained_plan,retained_buffers=generate(Settings(**row['settings']))
                if geometry_hash(retained_buffers)!=row['geometry_hash']:
                    raise RuntimeError('Retained geometry changed; include region: '+row['region'])
                retained.append(row)
        if args.gallery_resume and manifest_path.exists():
            old=json.loads(manifest_path.read_text())
            if (old['source_sha256']!=source or old['render_source_sha256']!=render_source
                    or old['source_revision']!=args.source_revision or old['settings_contract']!=contract):
                raise RuntimeError('Resume source/settings mismatch: '+function)
            if {r['region'] for r in old['records']}==set(args.regions) and all(r['status']=='rendered' and len(r['views'])==4
                    and all((out/v['image']).exists() and hashlib.sha256((out/v['image']).read_bytes()).hexdigest()==v['image_sha256']
                            for v in r['views']) for r in old['records']):
                print('ARCHETYPE_GALLERY_REUSED',function,flush=True)
                continue
        scene,camera=_reset_scene()
        scene.render.resolution_x=1024;scene.render.resolution_y=704
        scene.eevee.taa_render_samples=32
        bpy.data.objects['Neutral ground'].location.z=0.
        records=[];cases=[]
        for region in args.regions:
            settings=Settings(function=function,region=region,**contract)
            row={'function':function,'region':region,'label':TYPE_SPECS[function].label,
                 'source_revision':args.source_revision,'source_sha256':source,
                 'render_source_sha256':render_source,
                 'settings':asdict(settings),'resolved_context':resolve_settings(settings).context,
                 'status':'pending','views':[]}
            records.append(row)
            try:
                started=time.perf_counter()
                collection,metrics=build(settings)
                bpy.context.view_layer.update()
                row['build_seconds']=round(time.perf_counter()-started,4)
                row['geometry_hash']=collection['caelm_geometry_hash']
                row['validation']=json.loads(collection['caelm_validation'])
                row['backend']=metrics
                row['functional_program']=json.loads(collection.get('caelm_functional_program','null'))
                if not row['validation']['valid']:raise RuntimeError('Backend accepted invalid geometry')
                bounds=_bounds(collection)
                center=Vector(tuple((a+b)*.5 for a,b in bounds))
                corners=[Vector((x,y,z)) for x in bounds[0] for y in bounds[1] for z in bounds[2]]
                row['bounds']=bounds
                collection.hide_render=True
                cases.append((row,collection,center,corners))
            except Exception as error:
                row['status']='invalid' if 'validation failed' in str(error).lower() else 'failed'
                row['error']=str(error);row['traceback']=traceback.format_exc()
        # Fixed scale across all four regions and both opposing views of a type.
        scale=0.;aspect=1024/704
        retained_bounds=[]
        for row in retained:
            bounds=row['bounds'];center=Vector(tuple((a+b)*.5 for a,b in bounds))
            corners=[Vector((x,y,z)) for x in bounds[0] for y in bounds[1] for z in bounds[2]]
            retained_bounds.append((None,None,center,corners))
        for _,_,center,corners in cases+retained_bounds:
            for direction in VIEWS:
                inverse=(-Vector(direction).normalized()).to_track_quat('-Z','Y').inverted()
                points=[inverse@(v-center) for v in corners]
                scale=max(scale,max(p.x for p in points)-min(p.x for p in points),
                          (max(p.y for p in points)-min(p.y for p in points))*aspect)
        scale*=1.10
        for row in retained:
            if any(abs(v['ortho_scale']-scale)>1e-6 for v in row['views']):
                raise RuntimeError('Common framing changed; refresh all regions for '+function)
        clay=_neutral_material()
        for row,collection,center,corners in cases:
            collection.hide_render=False
            original=[(o,tuple(o.data.materials)) for o in collection.objects if o.type=='MESH']
            try:
                for mode in ('clay','material'):
                    if mode=='clay':_materials(collection,clay)
                    else:
                        for obj,materials in original:
                            obj.data.materials.clear()
                            for material in materials:obj.data.materials.append(material)
                    for view,direction in enumerate(VIEWS):
                        started=time.perf_counter()
                        _aim(camera,center+Vector(direction).normalized()*90,center)
                        camera.data.ortho_scale=scale
                        path=out/'individual'/function.lower()/f'{row["region"].lower()}_{mode}_{view}.png'
                        path.parent.mkdir(parents=True,exist_ok=True)
                        scene.render.filepath=str(path)
                        bpy.ops.render.render(write_still=True)
                        row['views'].append({'mode':mode,'view':view,
                            'image':path.relative_to(out).as_posix(),
                            'image_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                            'width':1024,'height':704,'camera_direction':direction,
                            'camera_location':list(camera.location),'camera_target':list(center),
                            'ortho_scale':scale,'elapsed_seconds':round(time.perf_counter()-started,4)})
                assert collection['caelm_geometry_hash']==row['geometry_hash']
                row['status']='rendered'
            except Exception as error:
                row['status']='failed';row['error']=str(error);row['traceback']=traceback.format_exc()
            finally:
                collection.hide_render=True
            print('ARCHETYPE_CONFIG_COMPLETE',function,row['region'],row['status'],flush=True)
        if source_hashes()!=source:raise RuntimeError('Generator source changed during gallery')
        manifest={'source_revision':args.source_revision,'generator_version':engine.TOOL_REVISION,
                  'source_sha256':source,'render_source_sha256':render_source,
                  'settings_contract':contract,'renderer':bpy.app.version_string,
                  'engine':scene.render.engine,'samples':32,'studio':'render_world_evidence._reset_scene, ground at grade',
                  'scale_policy':'Common projected orthographic scale per archetype across four regions and both views; different archetypes fitted independently.',
                  'geometry_generation':'One native backend build/validation per configuration; same objects reused for clay and material.',
                  'records':sorted(retained+records,key=lambda r:REGIONS.index(r['region']))}
        temporary=manifest_path.with_suffix('.tmp')
        temporary.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
        temporary.replace(manifest_path)
        print('ARCHETYPE_GALLERY_COMPLETE',function,flush=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--stage',default='study1')
    parser.add_argument('--regions',nargs='+',choices=REGIONS,default=REGIONS)
    parser.add_argument('--function',default='COTTAGE')
    parser.add_argument('--pbr',action='store_true')
    parser.add_argument('--condition',action='store_true')
    parser.add_argument('--craft-study',action='store_true')
    parser.add_argument('--tiers',nargs='+',choices=TIERS,default=TIERS)
    parser.add_argument('--front-only',action='store_true')
    parser.add_argument('--archetype-gallery',action='store_true',help='Current 20-type/four-region reference gallery; no generator changes')
    parser.add_argument('--gallery-functions',nargs='+',help='Optional bounded subset of archetype IDs')
    parser.add_argument('--gallery-resume',action='store_true',help='Reuse complete image/hash/source-verified archetypes')
    parser.add_argument('--gallery-output',default='archetypes_v05',help='Separate evidence folder; preserve historical galleries')
    parser.add_argument('--gallery-refresh',action='store_true',help='Refresh selected regions, retaining verified geometry/framing and original per-record provenance')
    parser.add_argument('--source-revision',help='Pinned generator commit for the archetype gallery')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if args.archetype_gallery:
        if not args.source_revision:parser.error('--source-revision is required for the archetype gallery')
        if args.gallery_refresh and args.gallery_output=='archetypes_v05':
            parser.error('Historical v0.5 gallery is immutable; choose a new output folder')
        archetype_gallery(args)
        return
    mode='pbr' if args.pbr else 'clay'
    stem=f'v05_{args.stage}_{args.function.lower()}_{mode}'
    out=ROOT/'evidence'
    frames=out/'_household_frames'
    frames.mkdir(parents=True,exist_ok=True)
    regional_files={'LOWMARK':'world_lowmark_thornfell.py','THORNFELL':'world_lowmark_thornfell.py',
                    'MIRE':'world_mire.py','EMBERHOLT':'world_emberholt.py'}
    dependencies={'geometry.py','model.py','profiles.py','facade.py','roof.py','world.py',
                  'engine.py','materials.py','blender_backend.py','__init__.py'}
    dependencies.update(regional_files[r] for r in args.regions)
    def hashes():
        return {name:hashlib.sha256((ROOT/'caelmor_architecture'/name).read_bytes()).hexdigest()
                for name in sorted(dependencies)}
    source=hashes()
    records=[]
    for region in args.regions:
        cases=[]
        for tier in args.tiers:
            settings=Settings(seed=91,function=args.function,region=region,wealth=tier,
                              detail='MEDIUM',geometry_mode='EFFICIENT',use_grammar=True,
                              world_aware=True,craftsmanship='STANDARD',maintenance=.7,age=35)
            if args.condition:
                from dataclasses import replace
                settings=replace(settings,wealth='ESTABLISHED',
                                 age={'MODEST':15,'ESTABLISHED':85,'AFFLUENT':120}[tier],
                                 maintenance={'MODEST':.9,'ESTABLISHED':.7,'AFFLUENT':.3}[tier])
            if args.craft_study:
                from dataclasses import replace
                settings=replace(settings,wealth='ESTABLISHED',
                                 craftsmanship={'MODEST':'ROUGH','ESTABLISHED':'STANDARD','AFFLUENT':'FINE'}[tier])
            plan,buffers=generate(settings)
            metrics=validate(plan,buffers)
            if not metrics['valid']:raise RuntimeError((region,tier,metrics['errors'][:5]))
            vertices=[Vector(v) for b in buffers for v in b.vertices]
            bounds=[(min(v[i] for v in vertices),max(v[i] for v in vertices)) for i in range(3)]
            center=Vector(tuple((a+b)*.5 for a,b in bounds))
            corners=[Vector((x,y,z)) for x in bounds[0] for y in bounds[1] for z in bounds[2]]
            cases.append((settings,metrics,geometry_hash(buffers),center,corners,tier))
        # Fit the union of projected bounds; never resize an individual tier.
        scale=0.
        aspect=640/440
        for _,_,_,center,corners,_ in cases:
            for direction in VIEWS:
                d=Vector(direction).normalized()
                inverse=(-d).to_track_quat('-Z','Y').inverted()
                points=[inverse@(v-center) for v in corners]
                scale=max(scale,max(p.x for p in points)-min(p.x for p in points),
                          (max(p.y for p in points)-min(p.y for p in points))*aspect)
        scale*=1.10
        for settings,metrics,gh,center,corners,tier in cases:
            scene,camera=_reset_scene()
            scene.render.resolution_x=640; scene.render.resolution_y=440
            scene.eevee.taa_render_samples=16
            # Studio ground is at true grade, avoiding the previous floating
            # appearance caused by a small render-only ground offset.
            bpy.data.objects['Neutral ground'].location.z=0.
            start=time.perf_counter()
            collection,backend=build(settings)
            if collection.get('caelm_geometry_hash')!=gh:raise RuntimeError('Backend source mismatch')
            if not args.pbr:_materials(collection,_neutral_material())
            for view,direction in enumerate(VIEWS):
                if args.front_only and view:continue
                _aim(camera,center+Vector(direction).normalized()*70,center)
                camera.data.ortho_scale=scale
                path=frames/f'{stem}_{region.lower()}_{tier.lower()}_{view}.png'
                scene.render.filepath=str(path)
                bpy.ops.render.render(write_still=True)
                records.append({'settings':asdict(settings),'slot':tier,'view':view,
                                'geometry_hash':gh,'validation':metrics,'backend':backend,
                                'image':path.name,'image_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                                'ortho_scale':scale,'camera_direction':direction,
                                'elapsed_seconds':round(time.perf_counter()-start,3)})
            if region=='EMBERHOLT' and tier=='AFFLUENT' and args.pbr:
                bpy.ops.wm.save_as_mainfile(filepath=str(out/f'{stem}_emberholt_editable.blend'),compress=True)
        print('HOUSEHOLD_REGION_COMPLETE',region,mode,flush=True)
    after=hashes()
    if source!=after:raise RuntimeError('Source changed during rendering; discard this mixed-source batch')
    manifest={'renderer':bpy.app.version_string,'source_hashes':source,'records':records,
              'study':'craft' if args.craft_study else 'condition' if args.condition else 'wealth',
              'view_selection':'front-only' if args.front_only else 'two opposed views',
              'scope':'Matched parameters, common projected orthographic scale per region; see records for view selection.'}
    path=out/f'{stem}_manifest.json'
    if path.exists():
        old=json.loads(path.read_text())
        manifest['records']= [r for r in old['records'] if r['settings']['region'] not in args.regions]+records
        manifest['prior_source_snapshots']=old.get('prior_source_snapshots',[])+[old['source_hashes']]
    path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('HOUSEHOLD_REVIEW_PASS',len(records),path,flush=True)


if __name__=='__main__':main()
