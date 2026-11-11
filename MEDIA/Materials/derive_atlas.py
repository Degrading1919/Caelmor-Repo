"""Generate linear Height and +Y tangent-space Normal for painted UV atlases."""
from argparse import ArgumentParser
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

import numpy as np
from PIL import Image

from derive_height import _blur
from paint_map_io import write_map


ROOT = Path(__file__).resolve().parent


def _islands(uv, vertices, winding):
    """Connect UV-continuous mesh edges with the same handedness."""
    parents = list(range(len(uv)))

    def root(index):
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    edges = {}
    for index, (triangle, corners) in enumerate(zip(uv, vertices)):
        for a, b in ((0, 1), (1, 2), (2, 0)):
            pair = sorted(((corners[a], *triangle[a]), (corners[b], *triangle[b])))
            key = (winding[index] > 0, *pair)
            other = edges.setdefault(key, index)
            left, right = sorted((root(index), root(other)))
            parents[right] = left
    return np.array([root(i) for i in range(len(uv))])


def _triangle_pixels(corners, shape):
    """Sample texel centres with half-open edges for shared triangle sides."""
    height, width = shape
    points = corners * (width, -height) + (0, height)
    start = np.maximum(0, np.ceil(points.min(axis=0) - 0.5).astype(int))
    end = np.minimum((width, height), np.floor(points.max(axis=0) - 0.5).astype(int) + 1)
    x0, y0 = start
    x1, y1 = end
    y, x = np.ogrid[y0:y1, x0:x1]
    inside = np.ones((y1 - y0, x1 - x0), dtype=bool)
    for a, b in zip(points, np.roll(points, -1, axis=0)):
        dx, dy = b - a
        side = dx * (y + 0.5 - a[1]) - dy * (x + 0.5 - a[0])
        include_edge = dy < 0 or (dy == 0 and dx > 0)
        inside &= (side > 1e-9) | ((abs(side) <= 1e-9) & include_edge)
    rows, cols = np.nonzero(inside)
    return rows + y0, cols + x0


def rasterize(uv, xyz, vertices, shape, allow_stacked=False):
    """Return island labels, triangle indices and local (U, shear, V) metrics."""
    if not np.isfinite(uv).all() or not np.isfinite(xyz).all() or np.any((uv < 0) | (uv > 1)):
        raise ValueError('Expected finite geometry and a single UV atlas inside 0–1')
    delta_uv = uv[:, 1:] - uv[:, :1]
    winding = np.linalg.det(delta_uv)
    if np.any(abs(winding) < 1e-12):
        raise ValueError('UV atlas contains a degenerate triangle')
    du, dv = np.linalg.solve(delta_uv, xyz[:, 1:] - xyz[:, :1]).transpose(1, 0, 2)
    length_u = np.linalg.norm(du, axis=1)
    if np.any(length_u <= 1e-9):
        raise ValueError('UV atlas contains a degenerate surface')
    shear = np.sum(du * dv, axis=1) / length_u
    length_v = np.linalg.norm(dv - du * (shear / length_u)[:, None], axis=1)
    if np.any(length_v <= 1e-9):
        raise ValueError('UV atlas contains a degenerate surface')
    metrics = np.column_stack((length_u, shear, length_v))
    islands = _islands(uv, vertices, winding)
    labels = np.zeros(shape, dtype=np.int32)
    triangles = np.full(shape, -1, dtype=np.int32)
    areas = {}
    order = np.argsort(islands, kind='stable')
    groups = np.split(order, np.flatnonzero(np.diff(islands[order])) + 1)
    for group in groups:
        samples = [_triangle_pixels(uv[i] if winding[i] < 0 else uv[i, [0, 2, 1]], shape)
                   for i in group]
        rows = np.concatenate([p[0] for p in samples])
        cols = np.concatenate([p[1] for p in samples])
        indices = np.repeat(group, [len(p[0]) for p in samples])
        if rows.size == 0:
            raise ValueError('An island covers no texel centres at this resolution')
        duplicate_count = rows.size - np.unique(rows * shape[1] + cols).size
        if duplicate_count:
            raise ValueError(f'UV island starting at triangle {group[0]} overlaps itself '
                             f'at {duplicate_count} texel samples')
        owners = labels[rows, cols]
        if np.any(owners):
            owner = int(owners[0])
            exact_stack = owner in areas and np.all(owners == owner) and areas[owner] == rows.size
            if not allow_stacked or not exact_stack:
                raise ValueError('Overlapping UV islands require an explicitly allowed full stack')
            if not np.allclose(metrics[triangles[rows, cols]], metrics[indices], rtol=1e-4, atol=1e-7):
                raise ValueError('Stacked UV islands have incompatible physical metrics')
            continue
        label = int(islands[group[0]]) + 1
        labels[rows, cols] = label
        triangles[rows, cols] = indices
        areas[label] = rows.size
    return labels, triangles, metrics


def _lab(rgb):
    """sRGB to CIE Lab relative to D65, scaled by 100."""
    linear = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    xyz = linear @ np.array([[.4124564, .3575761, .1804375],
                             [.2126729, .7151522, .0721750],
                             [.0193339, .1191920, .9503041]], dtype=np.float32).T
    xyz /= (.95047, 1, 1.08883)
    f = np.where(xyz > (6 / 29) ** 3, np.cbrt(xyz), xyz / (3 * (6 / 29) ** 2) + 4 / 29)
    x, y, z = f.transpose(2, 0, 1)
    return 1.16 * y - .16, 5 * (x - y), 2 * (y - z)


def _offset(array, dy, dx, fill):
    shifted = np.full_like(array, fill)
    h, w = array.shape[:2]
    y, x = slice(max(0, dy), min(h, h + dy)), slice(max(0, dx), min(w, w + dx))
    src_y, src_x = slice(max(0, -dy), min(h, h - dy)), slice(max(0, -dx), min(w, w - dx))
    shifted[y, x] = array[src_y, src_x]
    return shifted


SIDES = ((0, -1), (0, 1), (-1, 0), (1, 0))


def _auto_height(rgb, mask, radius, edge_fade):
    # Zero padding and normalized convolution isolate this island, including
    # holes and narrow strips. Pad beyond the three box passes' support.
    first = np.flatnonzero(mask)[0]

    def average(values, r, weights):
        # The band differences are invariant to a constant offset. Centering
        # first keeps constant paint at exactly the neutral Height code.
        values = values - values.flat[first]
        margin = 3 * r
        blurred = _blur(np.pad(values * mask, margin), r, 'stretch')
        return blurred[margin:-margin, margin:-margin] / weights

    weights = {}
    for r in dict.fromkeys(radius):
        margin = 3 * r
        blurred = _blur(np.pad(mask.astype(np.float32), margin), r, 'stretch')
        weights[r] = np.maximum(blurred[margin:-margin, margin:-margin], 1e-8)
    fine, medium, wide = radius
    light, a, b = _lab(rgb)
    fine_l = average(light, fine, weights[fine])
    mid_l = average(light, medium, weights[medium])
    wide_l = average(light, wide, weights[wide])
    chroma = np.hypot(*(average(c, fine, weights[fine]) - average(c, medium, weights[medium])
                        for c in (a, b)))
    grain = (.65 * (mid_l - wide_l) + .35 * (fine_l - mid_l)) / (1 + (chroma / .035) ** 2)
    # Fade inferred relief near UV cuts and narrow modeled bevel strips.
    fade = np.zeros_like(grain) if edge_fade else mask.astype(np.float32)
    interior = mask
    for _ in range(edge_fade):
        interior = interior & np.logical_and.reduce([_offset(interior, *d, False) for d in SIDES])
        fade += interior / edge_fade
    return .16 * np.tanh(grain / .1) * fade


def _slope(height, labels, axis):
    d = (0, 1) if axis == 1 else (1, 0)
    prev = _offset(height, *d, 0)
    next_value = _offset(height, -d[0], -d[1], 0)
    has_prev = _offset(labels, *d, 0) == labels
    has_next = _offset(labels, -d[0], -d[1], 0) == labels
    delta = np.where(has_prev, height - prev, 0) + np.where(has_next, next_value - height, 0)
    return delta / np.maximum(1, has_prev.astype(int) + has_next)


def pad_maps(labels, pixels, distance):
    """Extend whole texels through empty gutters with stable ties and no mixing."""
    labels = labels.copy()
    pixels = pixels.copy()
    directions = SIDES + ((-1, -1), (-1, 1), (1, -1), (1, 1))
    for _ in range(distance):
        previous = labels.copy()
        # Only pixels from the preceding ring are eligible as donors.
        for dy, dx in directions:
            owners = _offset(previous, dy, dx, 0)
            take = (labels == 0) & (owners != 0)
            if take.any():
                y, x = np.nonzero(take)
                pixels[y, x] = pixels[y - dy, x - dx]
                labels[y, x] = owners[y, x]
    return labels, pixels


def derive(rgb, labels, triangle_ids, metrics, relief_m, *, intensity=1, smoothing=1,
           padding=4, edge_fade=3, depth=None, cracks=None, detail=None):
    if not 0 <= intensity <= 2 or not .25 <= smoothing <= 4:
        raise ValueError('Intensity must be 0–2 and smoothing must be 0.25–4')
    if not np.isfinite(relief_m) or relief_m <= 0 or not 0 <= padding <= 32 or not 0 <= edge_fade <= 32:
        raise ValueError('Use positive finite relief and padding/edge fade between 0 and 32 texels')
    occupied = labels > 0
    if not occupied.any():
        raise ValueError('Atlas has no occupied texels')
    radius = [max(1, round(r * min(labels.shape) / 512 * smoothing)) for r in (1, 4, 16)]
    height = np.full(labels.shape, .5, dtype=np.float32)
    if intensity:
        rows, cols = np.nonzero(occupied)
        owner = labels[rows, cols]
        order = np.argsort(owner, kind='stable')
        for group in np.split(order, np.flatnonzero(np.diff(owner[order])) + 1):
            y, x = rows[group], cols[group]
            box = np.s_[y.min():y.max() + 1, x.min():x.max() + 1]
            mask = labels[box] == owner[group[0]]
            signal = _auto_height(rgb[box], mask, radius, edge_fade)
            if detail is not None:
                signal *= detail[box]
            height[box][mask] += intensity * signal[mask]
    if depth is not None:
        height[occupied] += depth[occupied]
    if cracks is not None:
        height[occupied] -= .20 * cracks[occupied]
    np.clip(height, 0, 1, out=height)
    with np.errstate(over='raise', invalid='raise', divide='raise'):
        u, shear, v = np.asarray(metrics)[triangle_ids[occupied]].T
        sx = _slope(height, labels, 1)[occupied] * labels.shape[1] * relief_m / u
        # PNG rows descend while Blender V ascends.
        sy = (-_slope(height, labels, 0)[occupied] * labels.shape[0] * relief_m - shear * sx) / v
        normal = np.column_stack((-sx, -sy, np.ones_like(sx)))
        normal /= np.linalg.norm(normal, axis=1, keepdims=True)
    pixels = np.zeros((*labels.shape, 4), dtype=np.uint16)
    pixels[:, :, 0] = np.rint(height * 65535).astype(np.uint16)
    pixels[:, :, 1:] = (128, 128, 255)
    pixels[occupied, 1:] = np.rint((normal * .5 + .5) * 255).astype(np.uint8)
    _, padded = pad_maps(labels, pixels, padding)
    return padded[:, :, 0].copy(), padded[:, :, 1:].astype(np.uint8)


def _png(path, shape=None, scalar=False):
    with Image.open(path) as image:
        if image.format != 'PNG' or (shape is not None and image.size != shape[::-1]):
            raise ValueError(f'{path}: expected a PNG matching the atlas dimensions')
        if scalar:
            if image.mode not in ('L', 'I', 'I;16', 'I;16B') or 'transparency' in image.info:
                raise ValueError(f'{path}: expected an opaque grayscale data PNG')
            return np.array(image)
        rgba = np.array(image.convert('RGBA'))
        return rgba[:, :, :3].astype(np.float32) / 255, rgba[:, :, 3]


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--albedo', type=Path, required=True, help='sRGB painted atlas PNG')
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--blend', type=Path, help='Saved Blender scene containing the target mesh')
    source.add_argument('--island-mask', type=Path, help='Grayscale integer labels, 0 outside islands')
    parser.add_argument('--object', help='Mesh object name in the Blender scene')
    parser.add_argument('--uv-map', help='Blender UV map name (defaults to active map)')
    parser.add_argument('--blender', default='blender', help='Blender executable')
    parser.add_argument('--allow-stacked', action='store_true')
    parser.add_argument('--size-m', nargs=2, type=float, metavar=('U', 'V'),
                        help='Physical coverage of the full mask (default 1 m by 1 m)')
    parser.add_argument('--height', type=Path, required=True, help='Fresh 16-bit Height PNG')
    parser.add_argument('--normal', type=Path, required=True, help='Fresh RGB Normal PNG')
    parser.add_argument('--relief-m', type=float, default=.002, help='Metres per full Height range')
    parser.add_argument('--intensity', type=float, default=1)
    parser.add_argument('--smoothing', type=float, default=1)
    parser.add_argument('--padding', type=int, default=4)
    parser.add_argument('--edge-fade', type=int, default=3)
    parser.add_argument('--depth', type=Path, help='Signed depth override, 8-bit 128 or 16-bit 32768 is neutral')
    parser.add_argument('--cracks', type=Path, help='White cuts up to 20 percent of full relief range')
    parser.add_argument('--detail-mask', type=Path, help='Black suppresses inferred relief on modeled details')
    args = parser.parse_args()
    try:
        paths = (args.height, args.normal)
        if paths[0].resolve() == paths[1].resolve() or any(p.exists() or p.suffix.lower() != '.png' for p in paths):
            raise ValueError('Choose two distinct fresh .png output paths')
        if any(not p.parent.is_dir() for p in paths):
            raise ValueError('Output parent directories must exist')
        rgb, alpha = _png(args.albedo)
        shape = rgb.shape[:2]
        if args.blend:
            if not args.object or args.size_m is not None:
                raise ValueError('Blender input needs --object and obtains scale from the mesh')
            with TemporaryDirectory(dir=ROOT) as scratch:
                target = Path(scratch) / 'triangles.npz'
                subprocess.run([args.blender, '--background', '--factory-startup', str(args.blend.resolve()),
                                '--python-exit-code', '1', '--python', str(ROOT / 'blender_atlas_uv.py'),
                                '--', '--object', args.object, '--output', str(target)] +
                               (['--uv-map', args.uv_map] if args.uv_map else []), check=True)
                with np.load(target) as geometry:
                    labels, triangles, metrics = rasterize(geometry['uv'], geometry['xyz'],
                                                          geometry['vertices'], shape, args.allow_stacked)
        else:
            labels = _png(args.island_mask, shape, scalar=True)
            u, v = args.size_m or (1., 1.)
            if not all(np.isfinite(m) and m > 0 for m in (u, v)):
                raise ValueError('Mask dimensions in metres must be positive and finite')
            if args.object or args.uv_map or args.allow_stacked:
                raise ValueError('Object, UV map and stack validation require Blender input')
            triangles = np.zeros(shape, dtype=np.int32)
            metrics = np.array([[u, 0., v]])
        if np.any(alpha[labels > 0] != 255):
            raise ValueError('Albedo must be opaque within all occupied texels')

        def scalar(path, signed=False):
            if path is None:
                return None
            data = _png(path, shape, scalar=True)
            maximum = 255 if data.dtype == np.uint8 else 65535
            return (data.astype(np.float32) - (maximum + 1) // 2) / maximum if signed else data / maximum

        height, normal = derive(rgb, labels, triangles, metrics, args.relief_m, intensity=args.intensity,
                                smoothing=args.smoothing, padding=args.padding, edge_fade=args.edge_fade,
                                depth=scalar(args.depth, signed=True), cracks=scalar(args.cracks),
                                detail=scalar(args.detail_mask))
        write_map(args.height, height)
        try:
            write_map(args.normal, normal)
        except OSError:
            args.height.unlink()
            raise
    except (OSError, ValueError, FloatingPointError, subprocess.CalledProcessError) as error:
        parser.error(str(error))
    print(f'{shape[1]} x {shape[0]}, {np.count_nonzero(np.unique(labels))} occupied UV regions')


if __name__ == '__main__':
    main()
