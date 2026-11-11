"""Regression checks for UV ownership, relief isolation and tangent slopes."""
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import numpy as np
from PIL import Image

from derive_atlas import derive, pad_maps, rasterize


ROOT = Path(__file__).resolve().parent


def quad(left, right, reverse=False, scale=1, vertex_start=0):
    uv = np.array([[left, 0], [right, 0], [right, 1], [left, 1]])
    xyz = np.array([[0, 0, 0], [scale, 0, 0], [scale, 1, 0], [0, 1, 0]])
    if reverse:
        uv = uv[[1, 0, 3, 2]]
    faces = np.array([[0, 1, 2], [0, 2, 3]])
    return uv[faces], xyz[faces], faces + vertex_start


class AtlasRelief(unittest.TestCase):
    def test_mirror_stack_uses_one_texture_footprint(self):
        first = quad(0, .5)
        second = quad(0, .5, reverse=True, vertex_start=4)
        stack = [np.concatenate(pair) for pair in zip(first, second)]
        with self.assertRaisesRegex(ValueError, 'allowed full stack'):
            rasterize(*stack, (32, 48))
        labels, triangles, metrics = rasterize(*stack, (32, 48), allow_stacked=True)
        self.assertEqual(np.count_nonzero(labels), 32 * 24)
        self.assertEqual(np.unique(labels).tolist(), [0, 1])
        self.assertTrue(np.all(triangles[labels > 0] < 2))
        np.testing.assert_allclose(metrics, [[2, 0, 1]] * 4)

    def test_partial_and_incompatible_stacks_fail(self):
        first = quad(0, .5)
        for second, error in ((quad(.25, .75, vertex_start=4), 'allowed full stack'),
                              (quad(0, .5, reverse=True, scale=2, vertex_start=4), 'incompatible')):
            stack = [np.concatenate(pair) for pair in zip(first, second)]
            with self.assertRaisesRegex(ValueError, error):
                rasterize(*stack, (32, 48), allow_stacked=True)

    def test_internal_overlap_is_not_treated_as_a_stack(self):
        uv, xyz, vertices = quad(0, .5)
        duplicate = [np.concatenate((a, a[:1])) for a in (uv, xyz, vertices)]
        with self.assertRaisesRegex(ValueError, 'triangle 0 overlaps itself'):
            rasterize(*duplicate, (32, 48), allow_stacked=True)
        expected = rasterize(uv, xyz, vertices, (32, 48))
        shared = rasterize(*duplicate, (32, 48), shared_uv=True)
        for actual, original in zip(shared[:2], expected[:2]):
            np.testing.assert_array_equal(actual, original)

    def test_shared_uv_preserves_the_first_reference_on_partial_mirrors(self):
        front = quad(0, .5)
        back = quad(.25, .75, reverse=True, scale=2, vertex_start=4)
        stack = [np.concatenate(pair) for pair in zip(front, back)]
        labels, triangles, _ = rasterize(*stack, (32, 48), shared_uv=True)
        self.assertTrue(np.all(labels[:, :24] == 1))
        self.assertTrue(np.all(labels[:, 24:36] == 3))
        self.assertTrue(np.all(labels[:, 36:] == 0))
        self.assertTrue(np.all(triangles[:, :24] < 2))

    def test_tilt_limit_keeps_distorted_shared_uv_texels_near_flat(self):
        labels = np.ones((8, 8), dtype=np.uint8)
        depth = np.broadcast_to(np.linspace(-.2, .2, 8), labels.shape)
        _, normal = derive(np.zeros((*labels.shape, 3)), labels, np.zeros_like(labels),
                           [[.001, 0, 1]], 1, intensity=0, depth=depth, max_tilt=15)
        xyz = normal.astype(float) / 127.5 - 1
        tilt = np.degrees(np.arctan2(np.linalg.norm(xyz[..., :2], axis=-1), xyz[..., 2]))
        self.assertTrue(np.all((tilt > 14.7) & (tilt < 15.3)))

    def test_filter_and_derivative_are_isolated(self):
        labels = np.ones((48, 72), dtype=np.uint16)
        labels[:, 36:] = 2
        rgb = np.full((*labels.shape, 3), .5, dtype=np.float32)
        triangles = np.zeros_like(labels)
        depth = np.zeros_like(labels, dtype=np.float32)
        kwargs = dict(relief_m=.01, edge_fade=0, padding=0)
        expected = derive(rgb, labels, triangles, [[1, 0, 1]], **kwargs)
        rng = np.random.default_rng(1919)
        rgb[:, 36:] = rng.random((48, 36, 3))
        depth[:, 36:] = .2
        actual = derive(rgb, labels, triangles, [[1, 0, 1]], depth=depth, **kwargs)
        for a, b in zip(actual, expected):
            np.testing.assert_array_equal(a[:, :36], b[:, :36])
        self.assertTrue(np.all(actual[0][:, :36] == 32768))
        self.assertTrue(np.all(actual[1][:, :36] == (128, 128, 255)))

    def test_padding_copies_one_owner_and_never_rewrites_interiors(self):
        labels = np.array([[1, 0, 2, 0, 0]])
        data = np.array([[13, 0, 91, 0, 0]])
        owners, values = pad_maps(labels, data, 2)
        np.testing.assert_array_equal(owners, [[1, 2, 2, 2, 2]])
        np.testing.assert_array_equal(values, [[13, 91, 91, 91, 91]])

    def test_chroma_only_boundary_and_narrow_bevel_stay_flat(self):
        labels = np.ones((64, 128), dtype=np.uint8)
        labels[-2:] = 2
        linear_to_srgb = lambda x: 1.055 * x ** (1 / 2.4) - .055
        rgb = np.zeros((*labels.shape, 3), dtype=np.float32)
        rgb[:, :64, 0] = linear_to_srgb(.25)
        rgb[:, 64:, 1] = linear_to_srgb(.25 * .2126729 / .7151522)
        rgb[-2:, :64] = .2
        rgb[-2:, 64:] = .9
        height, normal = derive(rgb, labels, np.zeros_like(labels), [[1, 0, 1]], .01)
        self.assertTrue(np.max(abs(height.astype(int) - 32768)) <= 1)
        self.assertTrue(np.all(normal[-2:] == (128, 128, 255)))

    def test_tangent_metric_shear_and_v_sign(self):
        labels = np.ones((24, 36), dtype=np.uint8)
        y, x = np.indices(labels.shape)
        depth = .3 * x / 36 - .1 * y / 24
        _, normal = derive(np.zeros((*labels.shape, 3)), labels, np.zeros_like(labels),
                           [[2, 1, 3]], 1, intensity=0, depth=depth)
        expected = np.array([-.15, .05 / 3, 1])
        expected /= np.linalg.norm(expected)
        pixels = np.rint((expected * .5 + .5) * 255)
        self.assertTrue(np.all(normal == pixels))

    def test_mask_cli_accepts_rectangular_paint_and_authored_overrides(self):
        with TemporaryDirectory(dir=ROOT) as tmp:
            folder = Path(tmp)
            mask = np.full((20, 32), 7, dtype=np.uint16)
            rgba = np.full((20, 32, 4), 255, dtype=np.uint8)
            rgba[:, :, 0] = 130
            rgba[:, :, 1] = 97
            depth = np.full(mask.shape, 128, dtype=np.uint8)
            depth[:, 4] = 156
            cracks = np.zeros(mask.shape, dtype=np.uint8)
            cracks[10] = 255
            for name, data in (('albedo', rgba), ('mask', mask), ('depth', depth), ('cracks', cracks)):
                Image.fromarray(data).save(folder / f'{name}.png')
            command = [sys.executable, str(ROOT / 'derive_atlas.py'), '--albedo', str(folder / 'albedo.png'),
                       '--island-mask', str(folder / 'mask.png'), '--depth', str(folder / 'depth.png'),
                       '--cracks', str(folder / 'cracks.png'), '--height', str(folder / 'height.png'),
                       '--normal', str(folder / 'normal.png')]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(folder / 'height.png') as output:
                height = np.array(output)
            self.assertEqual(height.shape, (20, 32))
            self.assertEqual(height[4, 1], 32768)
            self.assertGreater(height[4, 4], 32768)
            self.assertLess(height[10, 1], 32768)
            with Image.open(folder / 'normal.png') as output:
                self.assertEqual((output.size, output.mode), ((32, 20), 'RGB'))
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)


if __name__ == '__main__':
    unittest.main()
