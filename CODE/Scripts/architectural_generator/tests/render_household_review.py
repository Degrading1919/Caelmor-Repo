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
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
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
