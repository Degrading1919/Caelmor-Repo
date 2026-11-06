"""Blender batch-only export of the full authoritative terrain grid, not a building.

blender -b --factory-startup --python-exit-code 1 --python export_blender.py -- --arrays terrain_arrays.npz --output terrain.glb
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import bpy
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arrays", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(sys.argv[sys.argv.index("--")+1:])
    with np.load(args.arrays, allow_pickle=False) as data:
        z = data["height_engineered"].astype(np.float32)
        x, y = data["x"].astype(np.float32), data["y"].astype(np.float32)
    if not np.isfinite(z).all():
        raise ValueError("Terrain elevation must be finite")
    ny, nx = z.shape
    if z.shape != (len(y), len(x)):
        raise ValueError("Terrain grid dimensions do not match coordinates")
    xx, yy = np.meshgrid(x, y)
    coordinates = np.column_stack((xx.ravel(), yy.ravel(), z.ravel())).astype(np.float32)
    corners = (np.arange(ny-1)[:, None] * nx + np.arange(nx-1)[None, :]).ravel().astype(np.int32)
    quads = np.column_stack((corners, corners+1, corners+nx+1, corners+nx)).astype(np.int32)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    mesh = bpy.data.meshes.new("Lowmark full 8m mathematical terrain")
    mesh.vertices.add(len(coordinates)); mesh.vertices.foreach_set("co", coordinates.ravel())
    mesh.loops.add(quads.size); mesh.loops.foreach_set("vertex_index", quads.ravel())
    mesh.polygons.add(len(quads))
    mesh.polygons.foreach_set("loop_start", np.arange(len(quads), dtype=np.int32)*4)
    mesh.polygons.foreach_set("loop_total", np.full(len(quads),4,dtype=np.int32))
    mesh.polygons.foreach_set("use_smooth", np.ones(len(quads), dtype=bool))
    mesh.update(calc_edges=True)
    obj = bpy.data.objects.new("Lowmark / offline mathematical terrain / provisional open works", mesh)
    bpy.context.collection.objects.link(obj)
    obj["purpose"] = "Full-resolution offline terrain prototype; not a production world scene or building export"
    obj["axes_blender"] = "east X / north Y / elevation Z, metres, south-west origin"
    obj["glb_axes"] = "east X / elevation Y / minus north Z, right-handed glTF"
    obj["grid_spacing_m"] = float(x[1]-x[0])
    obj["grid_shape"] = [int(ny), int(nx)]
    obj["height_float32_sha256"] = hashlib.sha256(z.astype("<f4").tobytes()).hexdigest()
    obj["hydraulic_boundary"] = "Static terrain only. Gates/water stages/anomalous lift are separate authored constraints."
    material = bpy.data.materials.new("Neutral technical terrain / no finished artwork")
    material.use_nodes = True
    material.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (.42,.49,.34,1)
    material.node_tree.nodes.get("Principled BSDF").inputs["Roughness"].default_value = .9
    mesh.materials.append(material)
    bpy.context.view_layer.objects.active = obj; obj.select_set(True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=str(args.output.resolve()), export_format="GLB", use_selection=True,
                              export_yup=True, export_extras=True, export_normals=True, export_texcoords=False)
    print("CAELMOR_TERRAIN_GLB_EXPORTED " + json.dumps({"vertices":len(coordinates), "triangles":2*len(quads),
          "bytes":args.output.stat().st_size, "height_float32_sha256":obj["height_float32_sha256"]}))


if __name__ == "__main__": main()
