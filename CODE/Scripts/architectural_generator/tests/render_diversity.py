"""Five-seed study using the established benchmark studio."""
import argparse
from dataclasses import asdict, replace
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(Path(__file__).resolve().parent)]

import bpy
from render_polish_benchmarks import capture, settings
from render_architectural_benchmarks import source_hashes
from render_world_evidence import _reset_scene
from caelmor_architecture.blender_backend import build

SEEDS = (7, 17, 19, 91, 408)
FUNCTIONS = ('SMITHY', 'GATEHOUSE')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=('before', 'after'))
    parser.add_argument('revision')
    parser.add_argument('--rear', action='store_true')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    out = ROOT / 'evidence' / 'diversity_v12' / args.stage
    if (out / 'manifest.json').exists():
        raise ValueError('Capture already completed')
    sources = source_hashes()
    records = []
    for seed in SEEDS:
        for function in FUNCTIONS:
            s = replace(settings(function), seed=seed, crafted_curves=True)
            if args.stage == 'after':
                s = replace(s, seed_massing=True)
            _reset_scene()
            bpy.data.objects['Neutral ground'].location.z = 0.
            collection, metrics = build(s)
            images = capture(collection, out / str(seed), function,
                             distances=('normal',), views=(0, 1) if args.rear else (0,),
                             vertex_framing=True)
            for row in images:
                row['image'] = f"{seed}/{row['image']}"
            validation = json.loads(collection['caelm_source_validation'])
            records.append(dict(settings=asdict(s), images=images, metrics=metrics,
                                validation=validation,
                                geometry_hash=collection['caelm_geometry_hash']))
            print('DIVERSITY_CAPTURE', args.stage, seed, function, flush=True)
    assert sources == source_hashes(), 'Source changed during capture'
    (out / 'manifest.json').write_text(json.dumps(dict(
        revision=args.revision, blender=bpy.app.version_string,
        generator_sha256=sources, cases=records), indent=2)+'\n')


if __name__ == '__main__':
    main()
