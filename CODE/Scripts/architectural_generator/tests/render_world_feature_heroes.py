"""Render three feature focused world architecture examples in Blender."""
from __future__ import annotations

import bpy
import hashlib
import json
import math
import sys
import time
from dataclasses import asdict
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence"
sys.path.insert(0, str(ROOT))

from caelmor_architecture.model import Settings
from caelmor_architecture.engine import generate, validate, geometry_hash
from caelmor_architecture.blender_backend import build


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_hashes():
    from caelmor_architecture import engine, model, facade, roof, world
    from caelmor_architecture import world_lowmark_thornfell, world_mire, world_emberholt, blender_backend
    paths = (engine.__file__, model.__file__, facade.__file__, roof.__file__, world.__file__,
             world_lowmark_thornfell.__file__, world_mire.__file__, world_emberholt.__file__,
             blender_backend.__file__, __file__)
    return {Path(p).name: digest(p) for p in paths}


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x, scene.render.resolution_y = 1400, 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.view_settings.exposure = .7
    scene.world = bpy.data.worlds.new("World feature studio")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes.get("Background").inputs["Color"].default_value = (.32,.32,.31,1)
    scene.world.node_tree.nodes.get("Background").inputs["Strength"].default_value = .7
    bpy.ops.mesh.primitive_plane_add(size=300, location=(0,0,-.08))
    ground=bpy.context.object
    ground.name="Hero render ground"
    material=bpy.data.materials.new("Hero render ground material")
    material.diffuse_color=(.28,.29,.27,1)
    material.use_nodes=True
    material.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value=(.28,.29,.27,1)
    material.node_tree.nodes.get("Principled BSDF").inputs["Roughness"].default_value=.9
    ground.data.materials.append(material)
    bpy.ops.object.light_add(type="SUN", location=(-15,-18,28))
    sun=bpy.context.object
    sun.data.energy=2.1; sun.data.angle=.12
    sun.rotation_euler=(.45,-.42,-.45)
    bpy.ops.object.light_add(type="AREA", location=(5,-14,13))
    fill=bpy.context.object
    fill.data.energy=1700; fill.data.shape="DISK"; fill.data.size=14
    bpy.ops.object.camera_add()
    camera=bpy.context.object; camera.data.type="ORTHO"; scene.camera=camera
    return scene,camera


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    cases=(
      ("LOWMARK","MILLER",(-1.0,-.38,.72),"world_lowmark_miller_high.png",True),
      ("MIRE","BOATHOUSE",(.05,-1.0,.62),"world_mire_boathouse_high.png",True),
      ("EMBERHOLT","SMITHY",(.82,.78,.68),"world_emberholt_smithy_high_pbr.png",False),
    )
    records=[]
    for region,function,direction,image_name,clay in cases:
        settings=Settings(seed=91,function=function,region=region,wealth="ESTABLISHED",
                          detail="HIGH",craftsmanship="STANDARD",use_grammar=True,world_aware=True)
        start=time.perf_counter()
        scene,camera=reset_scene()
        plan,buffers=generate(settings)
        metrics=validate(plan,buffers)
        if not metrics.get("valid"):
            raise RuntimeError(f"Invalid feature hero geometry: {region}/{function}: {metrics}")
        gh=geometry_hash(buffers)
        build_start=time.perf_counter()
        collection,backend_metrics=build(settings)
        build_seconds=time.perf_counter()-build_start
        if collection.get("caelm_geometry_hash") != gh:
            raise RuntimeError(f"Engine and Blender hashes differ for {region}/{function}")
        collection.name=f"world_{region.lower()}_{function.lower()}_hero"
        points=[obj.matrix_world @ Vector(c) for obj in collection.objects if obj.type=="MESH"
                and not obj.hide_render and not obj.get("caelm_collider") for c in obj.bound_box]
        bounds=tuple((min(p[i] for p in points),max(p[i] for p in points)) for i in range(3))
        center=tuple((lo+hi)*.5 for lo,hi in bounds)
        span=tuple(hi-lo for lo,hi in bounds)
        distance=max(span[0],span[1])
        target=(center[0],center[1],center[2]*.78)
        d=Vector(direction).normalized()
        camera.location=Vector(center)+d*distance*1.85
        camera.rotation_euler=(Vector(target)-camera.location).to_track_quat("-Z","Y").to_euler()
        camera.data.ortho_scale=max(span[0]*1.52,span[1]*1.52,span[2]*1.42,12)*1.35
        camera.data.lens=48
        # Original renderer materials are retained for Emberholt; the other two
        # use the same neutral clay treatment as the comparison galleries.
        if clay:
            mat=bpy.data.materials.new("Neutral clay feature review")
            mat.diffuse_color=(.48,.48,.46,1); mat.use_nodes=True
            shader=mat.node_tree.nodes.get("Principled BSDF")
            shader.inputs["Base Color"].default_value=(.48,.48,.46,1)
            shader.inputs["Roughness"].default_value=.92
            for obj in collection.objects:
                if obj.type=="MESH": obj.data.materials.clear(); obj.data.materials.append(mat)
        filepath=OUT/image_name
        scene.render.filepath=str(filepath)
        render_start=time.perf_counter()
        bpy.ops.render.render(write_still=True)
        render_seconds=time.perf_counter()-render_start
        record={"settings":asdict(settings),"geometry_hash":gh,"validation":metrics,
                "backend_metrics":backend_metrics,"bounds":bounds,"camera_direction":direction,
                "neutral_clay":clay,"image":str(filepath.relative_to(ROOT)),
                "image_sha256":digest(filepath),"build_seconds":round(build_seconds,4),
                "render_seconds":round(render_seconds,4),
                "elapsed_seconds":round(time.perf_counter()-start,4),
                "blender_version":bpy.app.version_string}
        if region=="EMBERHOLT":
            blend=OUT/"world_emberholt_smithy_pbr.blend"
            bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True)
            record["blend"] = str(blend.relative_to(ROOT))
            record["blend_sha256"] = digest(blend)
            record["blend_bytes"] = blend.stat().st_size
        records.append(record)
    manifest={"schema":"world-feature-heroes-v1","source_hashes":source_hashes(),
              "blender_version":bpy.app.version_string,"records":records,
              "notes":"Miller and Boathouse are neutral clay to expose geometry. Emberholt Smithy keeps backend materials; its editable compressed Blender scene is included."}
    (OUT/"world_feature_heroes_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print("WORLD FEATURE HEROES",json.dumps(manifest,indent=2))


if __name__=="__main__": main()
