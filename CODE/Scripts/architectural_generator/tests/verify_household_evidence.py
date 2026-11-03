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


def verify_archetypes():
    """Verify gallery coverage/provenance/files, without generating more geometry."""
    import struct
    from caelmor_architecture.profiles import TYPE_SPECS,REGIONS
    out=ROOT/'evidence'/'archetypes_v05'
    baseline=json.loads((ROOT/'evidence'/'v05_evidence_verification.json').read_text())
    current={p.name:digest(p) for p in (ROOT/'caelmor_architecture').glob('*.py')}
    assert current==baseline['final_addon_source_sha256'],'Generator source changed since v0.5 delivery'
    assert digest(ROOT/'dist'/'caelmor_architecture.zip')==baseline['archive_sha256'],'Installable add-on changed'
    sheet_manifest=json.loads((out/'contact_sheets'/'manifest.json').read_text(encoding='utf-8-sig'))
    sheets={r['function']:r for r in sheet_manifest['sheets']}
    assert len(sheets)==len(TYPE_SPECS)==20
    assert set(sheets)==set(TYPE_SPECS)
    records=[];images=set();problems=[];sheet_hashes={};manifest_hashes={}
    revision=None;directions={}
    def image_check(relative,expected,size=None):
        path=out/relative
        assert digest(path)==expected,relative
        data=path.read_bytes()
        assert data[:8]==b'\x89PNG\r\n\x1a\n',relative
        dimensions=struct.unpack('>II',data[16:24])
        if size:assert dimensions==size,(relative,dimensions)
        return dimensions
    for function in TYPE_SPECS:
        path=out/'manifests'/f'{function.lower()}.json'
        manifest=json.loads(path.read_text())
        manifest_hashes[path.name]=digest(path)
        if revision is None:revision=manifest['source_revision']
        assert manifest['source_revision']==revision
        for name,expected in manifest['source_sha256'].items():
            assert digest(ROOT/'caelmor_architecture'/name)==expected,name
        for name,expected in manifest['render_source_sha256'].items():
            assert digest(ROOT/'tests'/name)==expected,name
        assert len(manifest['records'])==4
        assert {r['region'] for r in manifest['records']}==set(REGIONS)
        scales=[]
        for row in manifest['records']:
            settings=row['settings']
            assert row['function']==settings['function']==function
            assert row['region']==settings['region']
            assert {k:v for k,v in settings.items() if k not in ('region','function')}==manifest['settings_contract']
            assert (settings['seed'],settings['wealth'],settings['craftsmanship'],settings['age'],
                    settings['maintenance'],settings['detail'],settings['geometry_mode'])==(91,'ESTABLISHED','STANDARD',35,.7,'MEDIUM','EFFICIENT')
            assert settings['world_aware'] and settings['use_grammar'] and settings['context']=='AUTO'
            records.append(row)
            if row['status']!='rendered':
                problems.append({'function':function,'region':row['region'],'status':row['status'],'error':row.get('error')})
                continue
            assert row['validation']['valid'] and row['geometry_hash']
            assert len(row['views'])==4
            views={(v['mode'],v['view']):v for v in row['views']}
            assert set(views)=={(m,v) for m in ('clay','material') for v in (0,1)}
            for view in row['views']:
                assert view['image'] not in images
                images.add(view['image'])
                image_check(view['image'],view['image_sha256'],(1024,704))
                scales.append(view['ortho_scale'])
                direction=tuple(view['camera_direction'])
                assert directions.setdefault(view['view'],direction)==direction,'Inconsistent view direction'
            for view in (0,1):
                a,b=views['clay',view],views['material',view]
                assert a['camera_location']==b['camera_location'] and a['camera_target']==b['camera_target']
                assert a['image_sha256']!=b['image_sha256'],'Identical clay/material images'
            assert views['clay',0]['image_sha256']!=views['clay',1]['image_sha256']
            front,rear=views['clay',0]['camera_direction'],views['clay',1]['camera_direction']
            assert all(abs(front[i]+rear[i])<1e-8 for i in (0,1)) and front[2]>0 and rear[2]>0,'Views are not opposed exterior angles'
        assert not scales or max(scales)-min(scales)<1e-8,'Unmatched cross-region scale'
        sheet=sheets[function]
        assert sheet['source_revision']==revision
        dimensions=image_check(sheet['contact_sheet'],sheet['contact_sheet_sha256'])
        assert dimensions[0]>=4096 and dimensions[1]>=2816
        assert len(sheet['source_individuals'])==16
        for view in sheet['source_individuals']:
            if view['result']=='included':
                assert view['image'] in images
                assert view['declared_sha256']==view['actual_sha256']==digest(out/view['image'])
            else:assert problems,('Unexpected contact sheet placeholder',function,view)
        sheet_hashes[sheet['contact_sheet']]=sheet['contact_sheet_sha256']
    assert len(records)==80
    assert len(list((out/'individual').glob('*/*.png')))==len(images),'Unindexed individual render'
    report={'valid':True,'source_revision':revision,'generator_source_unchanged':True,'addon_archive_unchanged':True,
            'archetypes':20,'regions':4,'configurations':len(records),
            'rendered_configurations':sum(r['status']=='rendered' for r in records),
            'individual_images_verified':len(images),'contact_sheets_verified':len(sheets),
            'unsupported_or_failed_combinations':problems,'archetype_manifest_sha256':manifest_hashes,
            'contact_sheet_sha256':sheet_hashes,
            'verification_source_sha256':digest(Path(__file__)),
            'composition_source_sha256':digest(ROOT/'tests'/'compose_archetype_gallery.ps1'),
            'scope':'Coverage, file hashes/dimensions, unchanged generator source and matched settings/cameras. Native build validated each configuration once; no new regression suite, package/export or target-engine tests. Human artistic assessment remains pending.'}
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if not k.endswith('_sha256')},indent=2))


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


if __name__=='__main__':
    if '--archetype-gallery' in sys.argv:verify_archetypes()
    else:main()
