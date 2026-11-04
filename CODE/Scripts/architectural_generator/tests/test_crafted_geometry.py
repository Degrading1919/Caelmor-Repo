from collections import Counter

from caelmor_architecture.crafted_geometry import (bevel_open_box_front, beveled_box,
                                                    replace_box_components)
from caelmor_architecture.geometry import MeshBuffer, cross, dot, sub


def signed_volume(buffer):
    volume = 0.0
    for face in buffer.faces:
        a = buffer.vertices[face[0]]
        for i in range(1, len(face) - 1):
            volume += dot(a, cross(buffer.vertices[face[i]], buffer.vertices[face[i + 1]])) / 6
    return volume


def edge_uses(buffer):
    uses = Counter()
    for face in buffer.faces:
        for a, b in zip(face, face[1:] + face[:1]):
            uses[tuple(sorted((a, b)))] += 1
    return uses


def test_beveled_box_is_closed_outward_and_compact():
    mesh = MeshBuffer('crafted')
    assert beveled_box(mesh, (1, 2, 3), (2, 1, 3), .035) is mesh
    assert len(mesh.vertices) == 24
    assert Counter(map(len, mesh.faces)) == {4: 18, 3: 8}
    assert set(edge_uses(mesh).values()) == {2}
    assert signed_volume(mesh) > 0
    assert all(len(set(face)) == len(face) for face in mesh.faces)
    assert all(dot(cross(sub(mesh.vertices[face[1]], mesh.vertices[face[0]]),
                         sub(mesh.vertices[face[2]], mesh.vertices[face[0]])),
                   tuple(sum(mesh.vertices[i][a] for i in face) / len(face) - (1, 2, 3)[a]
                         for a in range(3))) > 0 for face in mesh.faces)
    assert min(p[0] for p in mesh.vertices) >= 0
    assert max(p[0] for p in mesh.vertices) <= 2
    assert min(p[1] for p in mesh.vertices) >= 1.5
    assert max(p[1] for p in mesh.vertices) <= 2.5
    assert min(p[2] for p in mesh.vertices) >= 1.5
    assert max(p[2] for p in mesh.vertices) <= 4.5


def test_beveled_box_is_deterministic_and_clamps_for_thin_dimensions():
    meshes = [MeshBuffer('x') for _ in range(2)]
    for mesh in meshes:
        beveled_box(mesh, (0, 0, 0), (.04, 2, 1), bevel=10)
    assert meshes[0].vertices == meshes[1].vertices
    assert meshes[0].faces == meshes[1].faces
    assert signed_volume(meshes[0]) > 0
    assert set(edge_uses(meshes[0]).values()) == {2}


def test_replace_only_selected_closed_box_components_and_preserve_metadata():
    mesh = MeshBuffer('house', material='stone', layer='masonry', topology='SOLID',
                      structural_role='wall', roof_envelope={'keep': True},
                      support_surface={'also': 'keep'})
    mesh.box((0, 0, 0), (2, 1, 1))
    mesh.box((4, 0, 0), (2, 1, 1))
    before = len(mesh.faces)
    assert replace_box_components(mesh, bevel=.03,
                                  predicate=lambda _mesh, center, _size: center[0] < 1) == 1
    assert len(mesh.faces) == before + 20
    assert len(mesh.vertices) == 32
    assert mesh.name == 'house' and mesh.material == 'stone' and mesh.layer == 'masonry'
    assert mesh.topology == 'SOLID' and mesh.structural_role == 'wall'
    assert mesh.roof_envelope == {'keep': True} and mesh.support_surface == {'also': 'keep'}
    assert set(edge_uses(mesh).values()) == {2}


def test_replace_ignores_surface_triangle_skin():
    mesh = MeshBuffer('skin', topology='SURFACE')
    mesh.indexed([(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)],
                 [(0, 1, 2), (0, 1, 3), (1, 2, 3), (2, 0, 3)])
    vertices, faces = list(mesh.vertices), list(mesh.faces)
    assert replace_box_components(mesh) == 0
    assert mesh.vertices == vertices and mesh.faces == faces


def open_front_box(name='skin'):
    mesh = MeshBuffer(name, topology='SURFACE', material='stone', layer='skin')
    mesh.box((0, 0, 0), (2, 1, 1))
    mesh.faces = mesh.faces[:3] + mesh.faces[4:]  # remove x+ cap, retain x- open back
    return mesh


def test_bevel_open_box_front_keeps_back_open_and_inside_bounds():
    mesh = open_front_box()
    assert bevel_open_box_front(mesh, inset=.025, depth=.012) == 1
    assert len(mesh.vertices) == 12 and len(mesh.faces) == 9
    assert all(len(face) == 4 for face in mesh.faces)
    uses = edge_uses(mesh)
    assert Counter(uses.values()) == {1: 4, 2: 16}
    assert all(-1 <= p[0] <= 1 and -.5 <= p[1] <= .5 and -.5 <= p[2] <= .5
               for p in mesh.vertices)
    center = (0, 0, 0)
    for face in mesh.faces:
        a, b, c = (mesh.vertices[face[i]] for i in range(3))
        centroid = tuple(sum(mesh.vertices[i][axis] for i in face)/4 for axis in range(3))
        assert dot(cross(sub(b, a), sub(c, a)), sub(centroid, center)) > 0
    assert mesh.topology == 'SURFACE' and mesh.material == 'stone' and mesh.layer == 'skin'


def test_bevel_open_box_front_applies_predicate_per_component():
    mesh = open_front_box()
    mesh.box((4, 0, 0), (2, 1, 1))
    assert bevel_open_box_front(mesh, predicate=lambda _mesh, center, _size: center[0] < 1) == 1
    assert len(mesh.faces) == 15
    assert len(mesh.vertices) == 20


def test_bevel_open_box_front_skips_clipped_nonbox_component():
    mesh = open_front_box()
    mesh.vertices[0] = (-.9, -.4, -.4)
    before_vertices, before_faces = list(mesh.vertices), list(mesh.faces)
    assert bevel_open_box_front(mesh) == 0
    assert mesh.vertices == before_vertices and mesh.faces == before_faces
