"""Derive a tangent-space +Y normal from a grayscale Height PNG."""
from argparse import ArgumentParser
from pathlib import Path

import numpy as np

from paint_map_io import material_record, read_grayscale_png, write_map


def normal_pixels(height, size_m, relief_m, edge='repeat'):
    width, depth = size_m
    if any(not np.isfinite(value) or value <= 0 for value in (width, depth, relief_m)):
        raise ValueError('Surface dimensions and relief must be positive and finite')
    h, w = height.shape
    with np.errstate(over='raise', divide='raise', invalid='raise'):
        if edge == 'repeat':
            dx = (np.roll(height, -1, 1) - np.roll(height, 1, 1)) * w * relief_m / (2 * width)
            dy = (np.roll(height, -1, 0) - np.roll(height, 1, 0)) * h * relief_m / (2 * depth)
        else:
            # One-sided differences at the outermost pixels preserve a constant
            # slope without looking across the image or flattening the border.
            dy, dx = np.gradient(height.astype(np.float64))
            dx *= w * relief_m / width
            dy *= h * relief_m / depth
        normal = np.stack((-dx, dy, np.ones_like(dx)), axis=-1)
        normal /= np.linalg.norm(normal, axis=-1, keepdims=True)
    return np.round((normal * .5 + .5) * 255).astype(np.uint8)


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--id',required=True,help='Catalog material ID')
    parser.add_argument('--height',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--relief-m',type=float,required=True,
                        help='Height in metres represented by the full scalar range')
    parser.add_argument('--edge', choices=('repeat', 'stretch'), default='repeat')
    parser.add_argument('--size-m', type=float, nargs=2, metavar=('U', 'V'),
                        help='Metres covered by the image along U and V (defaults to catalog scale_m)')
    args=parser.parse_args()
    try:
        record = material_record(args.id)
        height = read_grayscale_png(args.height)
        pixels = normal_pixels(height, args.size_m or record['scale_m'], args.relief_m, args.edge)
        write_map(args.output, pixels)
    except (OSError, ValueError, FloatingPointError) as error:
        parser.error(str(error))


if __name__=='__main__':
    main()
