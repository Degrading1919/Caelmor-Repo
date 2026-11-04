"""Reproducible Blender-authoring geometry diagnostics; no runtime benchmark."""
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from caelmor_architecture.engine import compare_geometry_modes
from caelmor_architecture.model import Settings


def main():
    examples = (
        Settings(function='FARMHOUSE', region='LOWMARK', use_grammar=True, seed=17),
        Settings(function='WATCHTOWER', region='THORNFELL', context='PASSWATCH',
                 use_grammar=True, seed=23),
        Settings(function='SMITHY', region='EMBERHOLT', context='EMBERFORGES',
                 use_grammar=True, seed=41),
    )
    if '--world' in sys.argv:
        examples=tuple(Settings(function='COTTAGE',region=region,use_grammar=True,
                                world_aware=True,seed=91)
                       for region in ('LOWMARK','THORNFELL','MIRE','EMBERHOLT'))
    rows = []
    for settings in examples:
        for detail in ('LOW', 'MEDIUM', 'HIGH'):
            requested = replace(settings, detail=detail)
            measured = compare_geometry_modes(requested)
            assert all(measured[mode]['valid'] for mode in ('SOLID', 'EFFICIENT')), measured
            rows.append({'settings': asdict(requested), 'results': measured})
    report = {
        'scope': 'Authoring geometry counts and pure generation/validation time; no runtime measurements.',
        'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted((ROOT / 'caelmor_architecture').glob('*.py'))},
        'cases': rows,
    }
    target = ROOT / 'evidence' / ('world_geometry_diagnostics.json' if '--world' in sys.argv
                                 else 'geometry_mode_diagnostics.json')
    target.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    for row in rows:
        settings, result = row['settings'], row['results']
        print(settings['region'], settings['function'], settings['detail'],
              'triangles', result['SOLID']['triangles'], '->', result['EFFICIENT']['triangles'],
              f"({result['triangles_reduction_percent']:.2f}% reduction)")


if __name__ == '__main__':
    main()
