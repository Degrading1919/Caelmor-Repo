"""Compose the material relief pilot using the construction evidence layout."""
import compose_construction_library as layout


def main():
    layout.ROOT = layout.EVIDENCE / 'material_relief'
    frames = layout.EVIDENCE.parent / 'dist' / 'material_relief_pilot' / 'frames'
    for fixture in ('roof', 'masonry'):
        rows = []
        for view, finish, caption in (('gameplay', 'material', 'Elevated material'),
                                      ('gameplay', 'clay', 'Elevated clay'),
                                      ('detail', 'material', 'Close material'),
                                      ('detail', 'clay', 'Close clay')):
            rows.append((caption, [frames / f'{fixture}_{view}_{finish}_{variant}.png'
                                   for variant in ('texture', 'relief')]))
        layout.sheet(f'{fixture}.jpg', ('Mapped baseline', 'Height displacement'), rows, width=710)
        layout.sheet(f'{fixture}_alternatives.jpg',
                     ('Modeled', 'Hybrid', 'Texture dominant', 'Height displacement'),
                     [('Elevated material', [frames / f'{fixture}_gameplay_material_{variant}.png'
                                             for variant in ('modeled', 'hybrid', 'texture', 'relief')])],
                     width=600)
        layout.sheet(f'{fixture}_sampling.jpg', ('Mapped baseline', '10 cm', '5 cm'),
                     [('Close clay', [frames / f'{fixture}_detail_clay_{variant}.png'
                                      for variant in ('texture', 'relief_low', 'relief')])], width=600)


if __name__ == '__main__':
    main()
