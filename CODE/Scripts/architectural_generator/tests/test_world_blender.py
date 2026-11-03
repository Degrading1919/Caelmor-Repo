"""Blender-runtime checks on assembled world-aware meshes and export behavior."""
import json
import os
import struct
import sys
import tempfile
import unittest
from pathlib import Path

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from caelmor_architecture.engine import generate, validate
from caelmor_architecture.model import Settings
from caelmor_architecture.blender_backend import TAG, build, export_building

REGIONS=("LOWMARK","THORNFELL","MIRE","EMBERHOLT")


def object_bvh(obj,depsgraph):
    evaluated=obj.evaluated_get(depsgraph)
    mesh=evaluated.to_mesh()
    try:
        mesh.calc_loop_triangles()
        vertices=[evaluated.matrix_world @ v.co for v in mesh.vertices]
        polygons=[tuple(t.vertices) for t in mesh.loop_triangles]
        return BVHTree.FromPolygons(vertices,polygons,all_triangles=True,epsilon=1e-6)
    finally:
        evaluated.to_mesh_clear()


def _reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


class WorldBlenderTests(unittest.TestCase):
    def setUp(self):
        _reset()

    def test_actual_world_windows_are_open_glazed_and_clear_of_frame(self):
        for region in REGIONS:
            with self.subTest(region=region):
                settings=Settings(seed=91,function="COTTAGE",region=region,
                    detail="LOW",use_grammar=True,world_aware=True)
                plan,buffers=generate(settings)
                report=validate(plan,buffers)
                self.assertTrue(report["valid"],report["errors"][:8])
                collection,_metrics=build(settings)
                bpy.context.view_layer.update()
                depsgraph=bpy.context.evaluated_depsgraph_get()
                objects=[o for o in collection.objects if o.get(TAG) and not o.get("caelm_collider")]
                by_id={o.get("caelm_buffer_id"):o for o in objects}
                glass_objs=[o for o in objects if o.get("caelm_material")=="glass"]
                self.assertTrue(glass_objs,region)

                frame_objs=[o for o in objects if o.get("caelm_layer")=="structure"
                    and str(o.get("caelm_material","")).startswith("timber")]
                frame_trees=[(o,object_bvh(o,depsgraph)) for o in frame_objs]
                glass_trees=[(o,object_bvh(o,depsgraph)) for o in glass_objs]
                overlaps=[]
                for glass_obj,glass_tree in glass_trees:
                    for frame_obj,frame_tree in frame_trees:
                        pairs=glass_tree.overlap(frame_tree)
                        if pairs:
                            overlaps.append((glass_obj.name,frame_obj.name,len(pairs)))
                self.assertFalse(overlaps,overlaps[:8])

                # Ray cast the actual Blender meshes through each window center.
                # The nearest visible surface must be glass; any joined wing or
                # neighboring mass that closes the opening wins this comparison.
                scene_bvhs=[]
                for obj in objects:
                    tree=object_bvh(obj,depsgraph)
                    scene_bvhs.append((obj,tree))
                rays=0
                for record in plan.facade_records:
                    a,b=plan.edges[record["edge_index"]]
                    dx,dy=b[0]-a[0],b[1]-a[1]
                    length=(dx*dx+dy*dy)**.5
                    tx,ty=dx/length,dy/length
                    nx,ny=ty,-tx
                    for aperture in record["openings"]:
                        if aperture["kind"]!="window":continue
                        s=(aperture["s0"]+aperture["s1"])*.5
                        z=(aperture["z0"]+aperture["z1"])*.5
                        origin=Vector((a[0]+tx*s-nx*.45,a[1]+ty*s-ny*.45,z))
                        direction=Vector((nx,ny,0))
                        hits=[]
                        for obj,tree in scene_bvhs:
                            location,normal,index,distance=tree.ray_cast(origin,direction,1.0)
                            if location is not None:
                                hits.append((distance,obj))
                        self.assertTrue(hits,(region,record["construction_zone"],aperture))
                        nearest=min(hits,key=lambda item:item[0])[1]
                        self.assertEqual(nearest.get("caelm_material"),"glass",
                            f"{region}/{record['construction_zone']} window occluded by {nearest.name} "
                            f"({nearest.get('caelm_material')})")
                        rays+=1
                self.assertGreater(rays,0)
                _reset()

    def test_world_regeneration_retains_protected_mesh_and_exports_settings(self):
        settings=Settings(seed=91,function="FARMHOUSE",region="THORNFELL",
            wealth="ESTABLISHED",use_grammar=True,world_aware=True)
        collection,_=build(settings)
        saved=json.loads(collection["caelm_settings"])
        self.assertTrue(saved["world_aware"])
        protected=next(o for o in collection.objects if o.get(TAG)
                       and not o.get("caelm_collider") and o.get("caelm_layer")=="walls")
        protected["caelm_protected"]=True
        protected.data.vertices[0].co.x+=.123
        protected.data.update()
        edited=tuple(protected.data.vertices[0].co)
        build(settings,collection=collection)
        retained=[o for o in collection.objects if o.get(TAG)
                  and o.get("caelm_buffer_id")==protected.get("caelm_buffer_id")]
        self.assertEqual(len(retained),1)
        self.assertIs(retained[0],protected)
        self.assertEqual(tuple(protected.data.vertices[0].co),edited)
        self.assertTrue(json.loads(collection["caelm_settings"])["world_aware"])

        with tempfile.TemporaryDirectory(prefix="caelmor_world_") as tmp:
            filepath=os.path.join(tmp,"world_build.glb")
            sidecar=export_building(collection,filepath)
            self.assertTrue(os.path.isfile(filepath))
            self.assertTrue(os.path.isfile(sidecar))
            with open(filepath,"rb") as stream:
                self.assertEqual(stream.read(4),b"glTF")
            with open(sidecar,encoding="utf-8") as stream:
                manifest=json.load(stream)
            self.assertEqual(manifest["format"],"CaelmorBuildingExport")
            self.assertEqual(manifest["settings"]["world_aware"],True)
            self.assertTrue(manifest["source_geometry_hash"])
            self.assertTrue(manifest["objects"])


if __name__=="__main__":
    sys.argv=[sys.argv[0]]
    unittest.main(verbosity=2)
