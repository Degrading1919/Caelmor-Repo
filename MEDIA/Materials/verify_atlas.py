"""Generate the original stone fixture, verify the CLI, and render its comparison."""
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
FRONTS = ((20, 40, 100, 140), (101, 40, 181, 140), (220, 40, 300, 140))


def make_paint(directory):
    albedo = np.full((256, 384, 3), 52, dtype=np.uint8)
    cracks = np.zeros(albedo.shape[:2], dtype=np.uint8)
    for index, ((x0, y0, x1, y1), color) in enumerate(zip(
            FRONTS, ((142, 122, 103), (118, 140, 133), (130, 127, 149)))):
        y, x = np.mgrid[:y1-y0, :x1-x0]
        broad = 16 * np.cos(x / 32 + index)
        fine = 4 * np.sin(.8 * x + .38 * y) * np.sin(.29 * x - .54 * y)
        fissure = abs(x - (19 + .31 * y + 2.4 * np.sin(y / 8))) < .8
        pigment = (x > 49)[:, :, None] * (5, -4, 3)
        stone = np.asarray(color) + (broad + fine - 16 * fissure)[:, :, None] + pigment
        albedo[y0:y1, x0:x1] = stone.clip(0, 255).astype(np.uint8)
        cracks[y0:y1, x0:x1] = fissure * 255
    for i in range(16):
        row = 165 + i * 5
        albedo[row:row+2, 20:105] = (98 + (i % 4) * 5, 93 + (i % 4) * 5, 88 + (i % 4) * 5)
        albedo[row:row+2, 54:56] += 35
    # Representative color padding for bilinear sampling at the model boundary.
    for x0, y0, x1, y1 in FRONTS:
        albedo[y0-1:y1+1, x0-1:x1+1] = np.pad(albedo[y0:y1,x0:x1], ((1,1),(1,1),(0,0)), mode='edge')
    Image.fromarray(albedo).save(directory / 'albedo.png')
    Image.fromarray(cracks).save(directory / 'cracks.png')


def verify(blender, output):
    with TemporaryDirectory(dir=ROOT) as tmp:
        directory = Path(tmp)
        make_paint(directory)
        base = [blender, '--background', '--factory-startup']
        fixture = ['--python-exit-code', '1', '--python', str(ROOT / 'blender_atlas_fixture.py'), '--']
        subprocess.run(base + fixture + ['build', tmp], check=True)
        command = [sys.executable, str(ROOT / 'derive_atlas.py'), '--blend', str(directory / 'fixture.blend'),
                   '--object', 'Atlas Stones', '--uv-map', 'Paint', '--allow-stacked', '--blender', blender,
                   '--albedo', str(directory / 'albedo.png'), '--cracks', str(directory / 'cracks.png'),
                   '--relief-m', '.006']
        for prefix in ('', 'repeat_'):
            subprocess.run(command + ['--height', str(directory / f'{prefix}height.png'),
                                      '--normal', str(directory / f'{prefix}normal.png')], check=True)
        for name in ('height', 'normal'):
            data = (directory / f'{name}.png').read_bytes()
            assert data == (directory / f'repeat_{name}.png').read_bytes()
            print(f'{name} SHA-256 {sha256(data).hexdigest()}', flush=True)
        height = np.array(Image.open(directory / 'height.png'))
        normal = np.array(Image.open(directory / 'normal.png'))
        assert height.shape == (256, 384) and normal.shape == (256, 384, 3)
        for i in range(16):
            y = 165 + i * 5
            assert np.all(height[y:y+2, 20:105] == 32768)
            assert np.all(normal[y:y+2, 20:105] == (128, 128, 255))
        cracks = np.array(Image.open(directory / 'cracks.png')) > 0
        print(f'Atlas Height {height.min()} to {height.max()}, median crack Height {np.median(height[cracks]):.0f}')
        slopes = normal.astype(float) / 255 * 2 - 1
        degrees = np.degrees(np.arctan2(np.linalg.norm(slopes[:,:,:2], axis=-1), slopes[:,:,2]))
        front_degrees = np.concatenate([degrees[y0:y1,x0:x1].ravel() for x0,y0,x1,y1 in FRONTS])
        print(f'Front normal tilt p95 {np.quantile(front_degrees,.95):.2f} deg, max {front_degrees.max():.2f} deg')
        subprocess.run(base + [str(directory / 'fixture.blend')] + fixture + ['render', tmp], check=True)
        sheet = Image.new('RGB', (1200, 1104), (33, 35, 39))
        draw = ImageDraw.Draw(sheet)
        for row, name in enumerate(('high', 'raking')):
            baseline = None
            for col, mode in enumerate(('paint', 'relief')):
                image = Image.open(directory / f'{name}_{mode}.png').convert('RGB')
                draw.text((col * 600 + 12, row * 552 + 9),
                          f'{name.title()} light / {"paint only" if col == 0 else "paint + generated Normal"}',
                          fill='white')
                sheet.paste(image, (col * 600, row * 552 + 32))
                if baseline is None:
                    baseline = np.array(image, dtype=np.int16)
                else:
                    change = np.abs(np.asarray(image) - baseline)
                    print(f'{name} light pixels changing by >2 RGB levels: {np.any(change > 2, axis=-1).sum()}')
                    changed = np.any(change > 2, axis=-1).sum()
                    assert changed > (100 if name == 'raking' else 0)
        sheet.save(output, quality=93)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--blender', default='blender')
    parser.add_argument('--output', type=Path, default=ROOT / 'evidence/stone_atlas_relief.jpg')
    args = parser.parse_args()
    verify(args.blender, args.output)
