"""Regression tests for the painted Height and Normal workflow."""
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import numpy as np
from PIL import Image

from derive_height import height_pixels
from derive_normal import normal_pixels
from paint_map_io import material_record, read_grayscale_png
from return_paint import return_paint


ROOT = Path(__file__).resolve().parent


class PaintMaps(unittest.TestCase):
    def setUp(self):
        scratch = TemporaryDirectory(dir=ROOT)
        self.addCleanup(scratch.cleanup)
        self.scratch = Path(scratch.name)

    def cli(self, tool, *args):
        return subprocess.run([sys.executable, str(ROOT / tool), *map(str, args)],
                              capture_output=True, text=True, encoding='utf-8', errors='replace')

    def test_flat_paint_stays_flat(self):
        paint = np.full((32, 32), 0.22, dtype=np.float32)
        for edge in ('repeat', 'stretch'):
            height = height_pixels(paint, edge=edge)
            self.assertTrue(np.all(height == 128))
            normal = normal_pixels(height / 255, (1, 4), 0.006, edge)
            self.assertTrue(np.all(normal == [128, 128, 255]))

    def test_wash_is_suppressed_and_directional_grain_survives(self):
        y = np.arange(512)[:, None]
        wash = np.broadcast_to(0.5 + 0.22 * np.cos(2 * np.pi * y / 512), (512, 512))
        paint = wash + 0.12 * np.sin(2 * np.pi * y / 16)
        flat = height_pixels(wash, edge='stretch')
        grain = height_pixels(paint, edge='stretch')
        strong = height_pixels(paint, intensity=2, edge='stretch')
        smoothed = height_pixels(paint, smoothing=4, edge='stretch')
        self.assertLess(np.std(flat), 1.5)
        self.assertGreater(np.std(grain), 4 * np.std(flat))
        self.assertGreater(np.std(strong), 1.8 * np.std(grain))
        self.assertLess(np.std(smoothed[128:-128]), np.std(grain[128:-128]))
        self.assertTrue(np.all(grain == grain[:, :1]))
        self.assertLess(np.ptp(grain), 60)

    def test_repeat_filter_is_centered_and_wraps(self):
        paint = np.full((256, 256), 0.5)
        paint[128, 0] = 0.05
        height = height_pixels(paint)
        self.assertEqual(np.unravel_index(height.argmin(), height.shape), (128, 0))
        self.assertEqual(height[128, 1], height[128, -1])
        self.assertLess(height[128, -1], 128)
        shifted = height_pixels(np.roll(paint, 47, axis=1))
        np.testing.assert_array_equal(shifted, np.roll(height, 47, axis=1))

    def test_stretch_filter_does_not_sample_opposite_edge(self):
        paint = np.full((256, 256), 0.5)
        paint[:, :16] = 0.1
        self.assertTrue(np.all(height_pixels(paint, edge='stretch')[:, -1] == 128))
        self.assertTrue(np.any(height_pixels(paint)[:, -1] != 128))

    def test_stretched_normal_preserves_slope_at_edges(self):
        y, x = np.indices((32, 32))
        height = (2 * x + y).astype(np.float32) / 96
        normal = normal_pixels(height, (0.15, 0.6), 0.05, 'stretch')
        self.assertTrue(np.all(normal == normal[10, 10]))
        self.assertLess(normal[0, 0, 0], 128)
        self.assertGreater(normal[0, 0, 1], 128)
        wide = normal_pixels(height, (0.6, 0.6), 0.05, 'stretch')
        self.assertGreater(wide[0, 0, 0], normal[0, 0, 0])
        self.assertNotEqual(normal_pixels(height, (0.15, 0.6), 0.05)[0, 0, 0],
                            normal[0, 0, 0])

    def test_repeat_normal_matches_existing_equation(self):
        height = np.random.default_rng(4).random((16, 16), dtype=np.float32)
        width, depth = material_record('split_oak_shingle')['scale_m']
        dx = (np.roll(height, -1, 1) - np.roll(height, 1, 1)) * 16 * 0.025 / (2 * width)
        dy = (np.roll(height, -1, 0) - np.roll(height, 1, 0)) * 16 * 0.025 / (2 * depth)
        old = np.stack((-dx, dy, np.ones_like(height)), axis=-1)
        old /= np.linalg.norm(old, axis=-1, keepdims=True)
        np.testing.assert_array_equal(normal_pixels(height, (width, depth), 0.025),
                                      np.round((old * 0.5 + 0.5) * 255).astype(np.uint8))

    def test_cli_output_round_trips_into_paint_package(self):
        rows = np.broadcast_to(np.rint(128 + 18 * np.sin(np.arange(512)[:, None] / 3)),
                               (512, 512)).astype(np.uint8)
        paint = self.scratch / 'paint.png'
        Image.fromarray(rows).convert('RGBA').save(paint)
        original = paint.read_bytes()
        height, normal = (self.scratch / name for name in ('height.png', 'normal.png'))
        args = ('--id', 'hewn_oak', '--input', paint, '--output', height, '--edge', 'stretch')
        result = self.cli('derive_height.py', *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.cli('derive_normal.py', '--id', 'hewn_oak', '--height', height,
                          '--output', normal, '--relief-m', 0.006, '--edge', 'stretch',
                          '--size-m', 4, 1)
        self.assertEqual(result.returncode, 0, result.stderr)
        for path, mode in ((height, 'L'), (normal, 'RGB')):
            with Image.open(path) as image:
                self.assertEqual((image.mode, image.size), (mode, (512, 512)))
        revision = return_paint(ROOT / 'packages/hewn_oak.zip',
                                [('height', height), ('normal', normal)],
                                self.scratch / 'returns', catalog=ROOT / 'catalog.json')
        self.assertEqual((revision / 'height.png').read_bytes(), height.read_bytes())
        self.assertEqual((revision / 'normal.png').read_bytes(), normal.read_bytes())
        self.assertNotEqual(self.cli('derive_height.py', *args).returncode, 0)
        self.assertEqual(paint.read_bytes(), original)

    def test_invalid_input_and_settings_are_rejected(self):
        png = self.scratch / 'bad.png'
        for mode, size, color in (('RGB', (4, 4), (1, 2, 3)),
                                  ('RGBA', (4, 4), (1, 1, 1, 0)),
                                  ('L', (3, 4), 128), ('L', (1, 1), 128)):
            Image.new(mode, size, color).save(png)
            with self.subTest(mode=mode, size=size), self.assertRaises(ValueError):
                read_grayscale_png(png)
        Image.new('L', (4, 4), 128).save(png, format='JPEG')
        with self.assertRaises(ValueError):
            read_grayscale_png(png)
        with self.assertRaisesRegex(ValueError, 'Unknown catalog'):
            material_record('missing')
        with self.assertRaises(ValueError):
            height_pixels(np.zeros((4, 4)), intensity=float('nan'))
        with self.assertRaises(ValueError):
            normal_pixels(np.zeros((4, 4)), (0, 1), 0.006)

    def test_16_bit_height_input(self):
        source = self.scratch / 'height16.png'
        Image.fromarray(np.array([[0, 1024], [32768, 65535]], dtype=np.uint16)).save(source)
        np.testing.assert_allclose(read_grayscale_png(source),
                                   [[0, 1024 / 65535], [32768 / 65535, 1]])


if __name__ == '__main__':
    unittest.main()
