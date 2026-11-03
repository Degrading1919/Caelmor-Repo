"""Replay unique review settings, verify native ZIP and retained image hashes.

No Blender rerender or benchmark. Raw frames are optional outside the authoring
workspace; published composite hashes and exact settings remain in the report.
"""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from caelmor_architecture.engine import generate,geometry_hash,validate
from caelmor_architecture.model import Settings


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    out=ROOT/'evidence'
    names=['v05_final_cottage_clay_manifest.json','v05_final_cottage_pbr_manifest.json',
           'v05_condition_cottage_pbr_manifest.json','v05_craft_cottage_pbr_manifest.json']
    names += [f'v05_function_{function}_pbr_manifest.json' for function in ('farmhouse','inn','boathouse','smithy')]
    checked={}; frames=0;raw_checks=0;sources=[]
    current={p.name:digest(p) for p in (ROOT/'caelmor_architecture').glob('*.py')}
    for name in names:
        data=json.loads((out/name).read_text())
        sources.append({'manifest':name,'source_byte_agreement':all(current.get(k)==v for k,v in data['source_hashes'].items())})
        for row in data['records']:
            key=json.dumps(row['settings'],sort_keys=True)
            if key not in checked:
                plan,buffers=generate(Settings(**row['settings']))
                result=validate(plan,buffers)
                assert result['valid'],(name,result['errors'])
                checked[key]=geometry_hash(buffers)
            assert checked[key]==row['geometry_hash'],(name,row['settings'])
            path=out/'_household_frames'/row['image']
            if path.exists():
                assert digest(path)==row['image_sha256'],path
                raw_checks+=1
            frames+=1
    native=json.loads((out/'v05_installed_emberholt.caelmor.json').read_text())
    native_hash=geometry_hash(generate(Settings(**native['settings']))[1])
    assert native_hash==native['source_geometry_hash']
    old=json.loads((out/'expanded_installed_farmhouse.caelmor.json').read_text())
    legacy_hash=geometry_hash(generate(Settings(**old['settings']))[1])
    assert legacy_hash==old['source_geometry_hash'],'Legacy geometry changed'
    archive=ROOT/'dist/caelmor_architecture.zip'
    archive_hash=digest(archive)
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.namelist():
            path=ROOT/'caelmor_architecture'/member
            if not path.exists():path=ROOT/member
            assert bundle.read(member)==path.read_bytes(),member
        members=len(bundle.namelist())
    for name in ('v05_installed_extension.json','v05_installed_legacy.json'):
        assert json.loads((out/name).read_text())['archive_sha256']==archive_hash
    composites=[p for pattern in ('v05_final_*.png','v05_function_*.png','v05_condition_*.png','v05_craft_*.png')
                for p in out.glob(pattern)]
    report={'valid':True,'unique_render_settings':len(checked),'render_records':frames,
            'raw_frame_hashes_verified':raw_checks,'render_geometry_matches_final_source':True,
            'source_snapshots':sources,'final_addon_source_sha256':current,
            'archive_sha256':archive_hash,'archive_members_verified':members,
            'native_export_geometry_hash':native_hash,'legacy_baseline_geometry_unchanged':True,
            'composite_sha256':{p.name:digest(p) for p in composites},
            'scope':'Geometry replay does not establish pixel identity or human artistic acceptance.'}
    (out/'v05_evidence_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('composite_sha256','final_addon_source_sha256','source_snapshots')},indent=2))


if __name__=='__main__':main()
