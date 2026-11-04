"""Blender-only triangle overlap diagnostic for exterior roof/wall seams."""
import json
import sys
from pathlib import Path

import bpy
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from caelmor_architecture.blender_backend import TAG, build
from caelmor_architecture.model import Settings, make_plan


def world_geometry(obj):
    matrix = obj.matrix_world
    vertices = [tuple(matrix @ vertex.co) for vertex in obj.data.vertices]
    polygons = []
    for poly in obj.data.polygons:
        ids = tuple(poly.vertices)
        polygons.extend((ids[0], ids[i], ids[i+1]) for i in range(1, len(ids)-1))
    return vertices, polygons


def bounds(vertices):
    return tuple(min(v[i] for v in vertices) for i in range(3)), tuple(max(v[i] for v in vertices) for i in range(3))


def aabb_overlaps(a, b, pad=1e-6):
    alo, ahi = a
    blo, bhi = b
    return all(alo[i] <= bhi[i] + pad and blo[i] <= ahi[i] + pad for i in range(3))


def sub(a, b):
    return tuple(a[i]-b[i] for i in range(3))


def dot(a, b):
    return sum(a[i]*b[i] for i in range(3))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def segment_triangle(p0, p1, tri, eps=1e-8):
    direction = sub(p1, p0)
    edge1, edge2 = sub(tri[1], tri[0]), sub(tri[2], tri[0])
    h = cross(direction, edge2)
    det = dot(edge1, h)
    if abs(det) < eps:
        return None
    inv = 1.0/det
    s = sub(p0, tri[0])
    u = inv*dot(s, h)
    if u < -eps or u > 1.0+eps:
        return None
    q = cross(s, edge1)
    v = inv*dot(direction, q)
    if v < -eps or u+v > 1.0+eps:
        return None
    t = inv*dot(edge2, q)
    if t < -eps or t > 1.0+eps:
        return None
    return tuple(p0[i] + t*direction[i] for i in range(3))


def triangle_intersections(a, b):
    hits = []
    for tri, other in ((a, b), (b, a)):
        for i in range(3):
            point = segment_triangle(tri[i], tri[(i+1)%3], other)
            if point is not None and not any(sum((point[k]-q[k])**2 for k in range(3)) < 1e-12 for q in hits):
                hits.append(point)
    return hits


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    settings = Settings(seed=17, function="FARMHOUSE", footprint="L", width=11.0,
                        depth=7.0, floors=2, detail="HIGH", window_density=1.0)
    plan = make_plan(settings)
    collection, metrics = build(settings)
    objects = [obj for obj in collection.objects if obj.get(TAG) and obj.type == "MESH"
               and not obj.get("caelm_collider")]
    geometry = {obj.name: world_geometry(obj) for obj in objects}
    tree_data = {}
    for obj in objects:
        vertices, polygons = geometry[obj.name]
        bbox = bounds(vertices)
        tree = BVHTree.FromPolygons(vertices, polygons, all_triangles=True, epsilon=0.0)
        tree_data[obj.name] = (tree, bbox, vertices, polygons)

    walls = [obj for obj in objects if obj.get("caelm_buffer_id") == "facade_walls"]
    timber = [obj for obj in objects if obj.get("caelm_buffer_id") == "facade_timber"]
    roofs = [obj for obj in objects if obj.get("caelm_layer") == "roof"]
    envelope_excess = []
    for obj in objects:
        if obj.get("caelm_layer") == "roof":
            continue
        vertices, _ = geometry[obj.name]
        for index, (x, y, z) in enumerate(vertices):
            roof_z = plan.roof_height(x, y)
            if roof_z == roof_z and abs(roof_z) < 1e9:
                excess = z-roof_z
                if excess > .01:
                    envelope_excess.append((excess, obj.get("caelm_buffer_id"), index, x, y, z, roof_z))
    rows = []
    for wall in walls:
        for roof in roofs:
            wtree, wb, wverts, wfaces = tree_data[wall.name]
            rtree, rb, rverts, rfaces = tree_data[roof.name]
            if not aabb_overlaps(wb, rb):
                continue
            pairs = wtree.overlap(rtree)
            if not pairs:
                continue
            actual_pairs = 0
            hits = []
            for wi, ri in pairs:
                wt = [wverts[i] for i in wfaces[wi]]
                rt = [rverts[i] for i in rfaces[ri]]
                pair_hits = triangle_intersections(wt, rt)
                if pair_hits:
                    actual_pairs += 1
                    for point in pair_hits:
                        if not any(sum((point[k]-q[k])**2 for k in range(3)) < 1e-10 for q in hits):
                            hits.append(point)
            rows.append({"wall": wall.get("caelm_buffer_id"),
                         "roof": roof.get("caelm_buffer_id"), "roof_name": roof.name,
                         "material": roof.get("caelm_material"),
                         "bvh_candidate_pairs": len(pairs), "triangle_intersections": actual_pairs,
                         "unique_hit_points": len(hits),
                         "hit_bounds": [[round(min(p[i] for p in hits), 5) for i in range(3)],
                                        [round(max(p[i] for p in hits), 5) for i in range(3)]] if hits else None,
                         "examples": [tuple(round(v, 5) for v in p) for p in hits[:12]]})
    print(json.dumps({"metrics": metrics,
                      "non_roof_vertices_above_roof_envelope": {
                          "count_over_1cm": len(envelope_excess),
                          "max_excess": max((row[0] for row in envelope_excess), default=0.0),
                          "by_buffer": {key: sum(1 for row in envelope_excess if row[1] == key)
                                        for key in sorted({row[1] for row in envelope_excess})},
                          "max_by_buffer": {key: round(max(row[0] for row in envelope_excess if row[1] == key), 5)
                                            for key in sorted({row[1] for row in envelope_excess})},
                          "timber_examples": [(round(row[0], 5), row[2],
                                               *(round(v, 5) for v in row[3:]))
                                              for row in sorted((r for r in envelope_excess if r[1] == "facade_timber"), reverse=True)[:20]],
                          "examples": [(round(row[0], 5), row[1], row[2],
                                        *(round(v, 5) for v in row[3:]))
                                       for row in sorted(envelope_excess, reverse=True)[:20]],
                      },
                      "wall_roof_intersections": rows}, indent=2), flush=True)


if __name__ == "__main__":
    main()
