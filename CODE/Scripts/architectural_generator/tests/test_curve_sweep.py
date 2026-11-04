"""Focused checks for the reusable planar tapered-member sweep."""

import unittest
from collections import Counter

from caelmor_architecture.curve_sweep import sweep_member
from caelmor_architecture.geometry import MeshBuffer


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


class CurveSweepTests(unittest.TestCase):
    def setUp(self):
        self.centers = ((0, 0, 0), (1, 0, 0.4), (2, 0, 1.2))
        self.widths = (0.8, 0.6, 0.4)
        self.depths = (0.5, 0.45, 0.3)

    def make_member(self):
        mesh = MeshBuffer("curved_brace")
        sweep_member(mesh, self.centers, (0, 1, 0), self.widths, self.depths)
        return mesh

    def test_tapered_sections_are_centered_at_the_requested_points(self):
        mesh = self.make_member()
        self.assertEqual(len(mesh.vertices), 8 * len(self.centers))
        for i, center in enumerate(self.centers):
            ring = mesh.vertices[i * 8:(i + 1) * 8]
            for axis in range(3):
                self.assertAlmostEqual(sum(p[axis] for p in ring) / 8, center[axis])
            if i == 0:
                tangent = (self.centers[1][0] - center[0], 0,
                           self.centers[1][2] - center[2])
            elif i == len(self.centers) - 1:
                tangent = (center[0] - self.centers[i - 1][0], 0,
                           center[2] - self.centers[i - 1][2])
            else:
                tangent = (self.centers[i + 1][0] - self.centers[i - 1][0], 0,
                           self.centers[i + 1][2] - self.centers[i - 1][2])
            length = sum(component ** 2 for component in tangent) ** .5
            tangent = tuple(component / length for component in tangent)
            depth_axis = (tangent[2], 0, -tangent[0])
            projections = [sum((p[k] - center[k]) * depth_axis[k] for k in range(3))
                           for p in ring]
            self.assertAlmostEqual(max(p[1] for p in ring) - min(p[1] for p in ring),
                                   self.widths[i])
            self.assertAlmostEqual(max(projections) - min(projections), self.depths[i])

    def test_topology_is_deterministic_and_closed_outward(self):
        first, second = self.make_member(), self.make_member()
        self.assertEqual(first.vertices, second.vertices)
        self.assertEqual(first.faces, second.faces)
        self.assertEqual(len(first.faces), 8 * (len(self.centers) - 1) + 2)
        self.assertTrue(all(count == 2 for count in edge_use_counts(first).values()))
        self.assertGreater(signed_volume(first), 0)

    def test_straight_member_has_exact_section_bounds(self):
        mesh = MeshBuffer("straight_brace")
        centers = ((0, 0, 0), (0, 0, 2))
        sweep_member(mesh, centers, (1, 0, 0), (0.6, 0.6), (0.4, 0.4))
        self.assertAlmostEqual(min(v[0] for v in mesh.vertices), -0.3)
        self.assertAlmostEqual(max(v[0] for v in mesh.vertices), 0.3)
        self.assertAlmostEqual(min(v[1] for v in mesh.vertices), -0.2)
        self.assertAlmostEqual(max(v[1] for v in mesh.vertices), 0.2)
        self.assertAlmostEqual(min(v[2] for v in mesh.vertices), 0)
        self.assertAlmostEqual(max(v[2] for v in mesh.vertices), 2)

    def test_rejects_invalid_section_and_path_data(self):
        cases = (
            ((), (0, 1, 0), (), (), .12),
            (self.centers, (0, 0, 0), self.widths, self.depths, .12),
            (self.centers, (0, 1, 0), (1, 1), self.depths, .12),
            (self.centers, (0, 1, 0), (1, 0, 1), self.depths, .12),
            (self.centers, (0, 1, 0), self.widths, self.depths, 0),
            (((0, 0, 0), (1, 1, 0)), (0, 1, 0), (1, 1), (1, 1), .12),
            (((0, 0, 0), (0, 0, 0)), (0, 1, 0), (1, 1), (1, 1), .12),
        )
        for centers, side, widths, depths, chamfer in cases:
            with self.subTest(centers=centers, chamfer=chamfer):
                with self.assertRaises(ValueError):
                    sweep_member(MeshBuffer("invalid"), centers, side, widths, depths, chamfer)


if __name__ == "__main__":
    unittest.main()
