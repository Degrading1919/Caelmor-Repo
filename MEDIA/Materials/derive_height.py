"""Derive restrained linear Height from a hand-painted grayscale PNG."""
from argparse import ArgumentParser
from pathlib import Path

import numpy as np

from paint_map_io import material_record, read_grayscale_png, write_map


def _blur(values, radius, edge):
    """Three separable box passes approximate a Gaussian in float precision."""
    for _ in range(3):
        for axis in (0, 1):
            rows = np.moveaxis(values, axis, -1)
            # The extra leading sample supplies the first prefix difference.
            pad = [(0, 0), (radius + 1, radius)]
            padded = np.pad(rows, pad, mode='wrap' if edge == 'repeat' else 'reflect')
            sums = np.cumsum(padded, axis=-1, dtype=np.float64)
            width = 2 * radius + 1
            means = (sums[:, width:] - sums[:, :-width]) / width
            values = np.moveaxis(means.astype(np.float32), -1, axis)
    return values


def height_pixels(values, intensity=1.0, smoothing=1.0, edge='repeat'):
    """Blend local grain bands around a flat midpoint with a soft relief limit."""
    if not 0 <= intensity <= 2 or not 0.25 <= smoothing <= 4:
        raise ValueError('Intensity must be 0–2 and smoothing must be 0.25–4')

    def radius(at_512):
        return max(1, round(at_512 * smoothing * values.shape[0] / 512))

    fine = _blur(values, radius(1), edge)
    medium = _blur(fine, radius(4), edge)
    wash = _blur(medium, radius(16), edge)
    grain = 0.65 * (medium - wash) + 0.35 * (fine - medium)
    height = 0.5 + 0.22 * intensity * np.tanh(grain / 0.1)
    return np.rint(height * 255).astype(np.uint8)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--id', required=True, help='Catalog material ID')
    parser.add_argument('--input', type=Path, required=True, help='Grayscale Base Color PNG')
    parser.add_argument('--output', type=Path, required=True, help='Fresh Height PNG path')
    parser.add_argument('--edge', choices=('repeat', 'stretch'), default='repeat')
    parser.add_argument('--intensity', type=float, default=1.0, help='Relief amplitude, 0–2')
    parser.add_argument('--smoothing', type=float, default=1.0, help='Filter scale, 0.25–4')
    args = parser.parse_args()
    try:
        material_record(args.id)
        values = read_grayscale_png(args.input)
        pixels = height_pixels(values, args.intensity, args.smoothing, args.edge)
        write_map(args.output, pixels)
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
