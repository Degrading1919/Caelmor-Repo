"""Render the actual verified GLBs in the same benchmark studio, no regeneration."""
import sys,json
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from render_world_evidence import _reset_scene,_aim
from render_architectural_benchmarks import CASE_SPECS,WIDTH,HEIGHT,SAMPLES,sha
out=ROOT/'evidence/materials_v09/roundtrip';out.mkdir(parents=True,exist_ok=True)
records=[]
for function in ('SMITHY','GATEHOUSE'):
    spec=CASE_SPECS[function];scene,camera=_reset_scene()
    scene.render.resolution_x=WIDTH;scene.render.resolution_y=HEIGHT;scene.eevee.taa_render_samples=SAMPLES
    bpy.data.objects['Neutral ground'].location.z=0.
    glb=out.parent/(function.lower()+'.glb');bpy.ops.import_scene.gltf(filepath=str(glb))
    for distance in ('normal','close'):
        target=spec['targets']['close_front' if function=='GATEHOUSE' and distance=='close' else distance]
        location=Vector(target)+Vector(spec['directions'][distance][0]).normalized()*spec['camera_distances'][distance]
        _aim(camera,location,target);camera.data.ortho_scale=spec['scales'][distance]
        image=out/(function.lower()+'_'+distance+'.png');scene.render.filepath=str(image)
        bpy.ops.render.render(write_still=True)
        records.append(dict(function=function,distance=distance,image=image.name,sha256=sha(image),
            glb_sha256=sha(glb),camera_location=list(location),camera_target=list(target),ortho_scale=camera.data.ortho_scale))
(out/'manifest.json').write_text(json.dumps(dict(blender=bpy.app.version_string,images=records),indent=2)+'\n')
print('MATERIAL_ROUNDTRIP_CAPTURE_PASS',len(records),flush=True)
