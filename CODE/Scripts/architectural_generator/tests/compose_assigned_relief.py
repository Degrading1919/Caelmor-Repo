"""Compose private review frames with the existing construction sheet layout."""
from pathlib import Path
import sys

import compose_construction_library as layout


def main(directory):
    layout.ROOT = directory
    frames = layout.EVIDENCE.parent / 'dist' / 'assigned_relief' / 'frames'
    for name, detail, original, flat, displaced in (
            ('Shingles', 'roof', 'original', 'flat', 'relief'),
            ('Planks', 'wall', 'original', 'flat', 'relief'),
            ('Birch', 'wall', 'original_birch', 'birch_flat', 'remapped')):
        layout.sheet(f'Material Relief - {name}.jpg',
                     ('Flat', 'Material height'),
                     [(caption,[frames/f'{variant}_{view}_{finish}.png'
                                for variant in (flat,displaced)])
                      for caption,view,finish in (
                          ('Elevated gameplay material','gameplay','material'),
                          ('Close material','roof' if detail=='roof' else 'wall','material'),
                          ('Close clay',detail,'clay'))], width=780)
        layout.sheet(f'Material Source - {name}.jpg',
                     ('Original cached shader', 'Matched SBSAR bake'),
                     [('Close flat material',[frames/f'{variant}_{detail}_material.png'
                                              for variant in (original,flat)])],width=780)


if __name__=='__main__':
    main(Path(sys.argv[1]).resolve(strict=True))
