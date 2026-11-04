"""Independent checks of the dependency-free geometry primitives."""

import unittest
from collections import Counter

from caelmor_architecture.engine import generate
from caelmor_architecture.geometry import MeshBuffer, area, clip
from caelmor_architecture.model import Settings


def edge_use_counts(buffer):
    counts = Counter()
    for face in buffer.faces:
        for a, b in zip(face, face[1:] + face[:1]):
            counts[tuple(sorted((a, b)))] += 1
    return counts


def signed_volume(buffer):
    total = 0.0
    for face in buffer.faces:
        a = buffer.vertices[face[0]]
        for i in range(1, len(face) - 1):
            b, c = buffer.vertices[face[i]], buffer.vertices[face[i + 1]]
            total += (a[0] * (b[1] * c[2] - b[2] * c[1])
                      + a[1] * (b[2] * c[0] - b[0] * c[2])
                      + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0
    return total


class GeometryPrimitiveTests(unittest.TestCase):
    def assertClosedOutward(self, buffer):
        self.assertTrue(buffer.faces)
        self.assertTrue(all(count == 2 for count in edge_use_counts(buffer).values()))
        self.assertGreater(signed_volume(buffer), 0.0)

    def test_box_beam_prism_and_cylinder_are_closed_outward_solids(self):
        primitives = []
        box = MeshBuffer("box")
        box.box((1, 2, 3), (2, 3, 4))
        primitives.append(box)
        beam = MeshBuffer("beam")
        beam.beam((0, 0, 0), (1, 2, 3), .2, .3)
        primitives.append(beam)
        chamfered = MeshBuffer("chamfered_beam")
        chamfered.chamfered_beam((0, 0, 0), (1, 2, 3), .2, .3, .02)
        primitives.append(chamfered)
        prism = MeshBuffer("prism")
        prism.prism([(0, 0), (2, 0), (2, 1), (0, 1)], 0, 2)
        primitives.append(prism)
        cylinder = MeshBuffer("cylinder")
        cylinder.cylinder((0, 0, 0), (0, 0, 2), .5, segments=12)
        primitives.append(cylinder)
        for buffer in primitives:
            with self.subTest(primitive=buffer.name):
                self.assertClosedOutward(buffer)

    def test_half_plane_clip_retains_only_points_in_the_requested_side(self):
        square = [(0, 0), (4, 0), (4, 3), (0, 3)]
        clipped = clip(square, 1, 0, -2)
        self.assertAlmostEqual(area(clipped), 6.0)
        self.assertTrue(all(x >= 2.0 - 1e-8 for x, _ in clipped))

    def test_generated_mesh_buffers_are_closed_and_outward_wound(self):
        _plan, buffers = generate(Settings(seed=29))
        self.assertTrue(buffers)
        for buffer in buffers:
            with self.subTest(buffer=buffer.name):
                self.assertTrue(all(count == 2 for count in edge_use_counts(buffer).values()))
                self.assertGreater(signed_volume(buffer), 0.0)


if __name__ == "__main__":
    unittest.main()
