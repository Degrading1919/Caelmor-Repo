"""Controlled v0.6 study: existing geometry, separate lighting and view changes.

Reuses the established studio/native backend. No production material changes.
"""
import hashlib
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from render_world_evidence import _reset_scene,_aim,_materials,_neutral_material
from caelmor_architecture.blender_backend import build
from caelmor_architecture.model import Settings

OUT=ROOT/'evidence'/'function_v07_diagnosis'

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    records=[]
    for function,region in (('SMITHY','LOWMARK'),('GATEHOUSE','EMBERHOLT')):
        old=json.loads((ROOT/'evidence/function_v06/manifests'/f'{function.lower()}.json').read_text())
        source=next(r for r in old['records'] if r['region']==region)
        front=next(v for v in source['views'] if v['mode']=='clay' and v['view']==0)
        scene,camera=_reset_scene()
        scene.render.resolution_x=1024;scene.render.resolution_y=704
        scene.eevee.taa_render_samples=32
        bpy.data.objects['Neutral ground'].location.z=0
        collection,_=build(Settings(**source['settings']))
        assert collection['caelm_geometry_hash']==source['geometry_hash'], 'Baseline changed'
        original=[(o,tuple(o.data.materials)) for o in collection.objects if o.type=='MESH']
        clay=_neutral_material()
        row={'function':function,'region':region,'settings':source['settings'],
             'geometry_hash':source['geometry_hash'],'source_revision':source.get('source_revision',old['source_revision']),
             'baseline_views':[v for v in source['views'] if v['view']==0],'views':[]}
        for treatment in ('raking_light','lower_frontage'):
            # Light-only treatment retains baseline camera/scale and materials.
            sun=next(o for o in scene.objects if o.type=='LIGHT' and o.data.type=='SUN')
            if treatment=='raking_light':
                _aim(sun,(-15,-20,12),(0,0,0));sun.data.energy=3.0;sun.data.angle=.055
                scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.22
                next(o for o in scene.objects if o.type=='LIGHT' and o.data.type=='AREA').data.energy=650
                location=front['camera_location']
            else:
                sun.rotation_euler=(.45,-.42,-.45);sun.data.energy=2.1;sun.data.angle=.12
                scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.7
                next(o for o in scene.objects if o.type=='LIGHT' and o.data.type=='AREA').data.energy=1500
                location=Vector(front['camera_target'])+Vector((.85,-1.2,.30)).normalized()*90
            _aim(camera,location,front['camera_target']);camera.data.ortho_scale=front['ortho_scale']
            for mode in ('clay','material'):
                if mode=='clay':_materials(collection,clay)
                else:
                    for obj,mats in original:
                        obj.data.materials.clear()
                        for mat in mats:obj.data.materials.append(mat)
                path=OUT/f'{function.lower()}_{region.lower()}_{treatment}_{mode}.png'
                # Resume this immutable diagnostic only while baseline geometry
                # matches; avoids repeating frames after metadata-only fixes.
                if not path.exists():
                    scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
                row['views'].append({'treatment':treatment,'mode':mode,'image':path.name,
                    'camera_location':list(camera.location),'camera_target':front['camera_target'],
                    'ortho_scale':camera.data.ortho_scale,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        records.append(row)
    (OUT/'manifest.json').write_text(json.dumps({'records':records,'design':
        'Geometry/native hash and settings held constant. Baseline studio reused from v0.6; light-only and camera-only treatments. No production shader edits.'},indent=2)+'\n')

if __name__=='__main__':main()
