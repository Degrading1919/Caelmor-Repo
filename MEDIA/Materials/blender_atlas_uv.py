"""Extract evaluated UV triangles and metre-space edges for derive_atlas.py."""
from argparse import ArgumentParser
import sys

import bpy
import numpy as np


def mesh_triangles(obj, uv_map=None):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
    try:
        layer = mesh.uv_layers.get(uv_map) if uv_map else mesh.uv_layers.active
        if layer is None:
            raise ValueError(f'{obj.name} has no requested UV map')
        mesh.calc_loop_triangles()
        uv = []
        xyz = []
        vertices = []
        scale = bpy.context.scene.unit_settings.scale_length
        # Translation has no effect on tangent derivatives.
        transform = evaluated.matrix_world.to_3x3()
        for triangle in mesh.loop_triangles:
            uv.append([tuple(layer.uv[loop].vector) for loop in triangle.loops])
            xyz.append([tuple((transform @ mesh.vertices[i].co) * scale)
                        for i in triangle.vertices])
            vertices.append(tuple(triangle.vertices))
        if not uv:
            raise ValueError(f'{obj.name} has no mesh triangles')
        return np.asarray(uv), np.asarray(xyz), np.asarray(vertices)
    finally:
        evaluated.to_mesh_clear()


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--object', required=True)
    parser.add_argument('--uv-map')
    parser.add_argument('--output', required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    obj = bpy.context.scene.objects.get(args.object)
    if obj is None or obj.type != 'MESH':
        raise ValueError(f'No mesh named {args.object!r} in the active scene')
    uv, xyz, vertices = mesh_triangles(obj, args.uv_map)
    np.savez(args.output, uv=uv, xyz=xyz, vertices=vertices)


if __name__ == '__main__':
    main()
