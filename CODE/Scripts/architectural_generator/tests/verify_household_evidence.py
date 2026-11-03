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


def verify_functional_gallery():
    """Verify the v0.6 function gallery and preserve the v0.5 image baseline."""
    import struct
    out=ROOT/'evidence'/'function_v06'
    function_names=('smithy','market_hall','stable','gatehouse')
    regions=('LOWMARK','THORNFELL','MIRE','EMBERHOLT')
    expected_settings={'seed':91,'wealth':'ESTABLISHED','craftsmanship':'STANDARD','age':35,
                       'maintenance':.7,'detail':'MEDIUM','geometry_mode':'EFFICIENT',
                       'world_aware':True,'use_grammar':True,'context':'AUTO'}
    def png_check(path,expected_hash,size=None):
        assert path.is_file(),f'Missing PNG: {path}'
        assert digest(path)==expected_hash,f'PNG SHA-256 mismatch: {path}'
        data=path.read_bytes()
        assert data[:8]==b'\x89PNG\r\n\x1a\n',f'Invalid PNG signature: {path}'
        dimensions=struct.unpack('>II',data[16:24])
        if size:assert dimensions==size,(path,dimensions,size)
        return dimensions

    source_current={p.name:digest(p) for p in (ROOT/'caelmor_architecture').glob('*.py')}
    functions={name:name.upper() for name in function_names}
    manifests={}; manifest_hashes={}; records_by_function={}; all_images=set(); image_count=0
    revision_values=set(); settings_by_function={}; camera_by_function={}; function_source_snapshots={}
    for name in function_names:
        function=functions[name]
        path=out/'manifests'/f'{name}.json'
        manifest=json.loads(path.read_text(encoding='utf-8-sig'))
        manifests[name]=manifest
        manifest_hashes[path.name]=digest(path)
        revision_values.add(manifest['source_revision'])
        assert len(manifest['records'])==4,(name,'expected four regional records')
        assert {row['region'] for row in manifest['records']}==set(regions),(name,'regional coverage mismatch')
        source_snapshot={}
        for source_name,expected_hash in manifest['source_sha256'].items():
            source_path=ROOT/'caelmor_architecture'/source_name
            assert source_path.is_file() and digest(source_path)==expected_hash,(name,source_name,'addon source snapshot mismatch')
            source_snapshot[source_name]=expected_hash
        render_snapshot={}
        for helper_name,expected_hash in manifest['render_source_sha256'].items():
            helper_path=ROOT/'tests'/helper_name
            assert helper_path.is_file() and digest(helper_path)==expected_hash,(name,helper_name,'render helper snapshot mismatch')
            render_snapshot[helper_name]=expected_hash
        function_source_snapshots[name]={'addon_source_sha256':source_snapshot,'render_source_sha256':render_snapshot}
        seen_regions=set(); scales=[]; directions={}; per_function_records=[]
        for row in manifest['records']:
            settings=row['settings']; region=row['region']
            assert row['function']==settings['function']==function,(name,region,'function metadata mismatch')
            assert row['region']==settings['region'] and region in regions,(name,region,'region metadata mismatch')
            assert {key:value for key,value in settings.items() if key not in ('region','function')}==manifest['settings_contract'],(name,region,'settings contract mismatch')
            seen_regions.add(region)
            for key,expected in expected_settings.items():assert settings.get(key)==expected,(name,region,key,settings.get(key))
            assert row.get('functional_program') and row['functional_program'].get('function')==function,(name,region,'missing or mismatched functional_program')
            assert row['functional_program'].get('region')==region,(name,region,'functional_program region mismatch')
            assert row['status']=='rendered',(name,region,'non-rendered record')
            assert row['validation']['valid'] and row['geometry_hash'],(name,region,'invalid build record')
            views={(view['mode'],int(view['view'])):view for view in row['views']}
            assert len(row['views'])==4 and set(views)=={(mode,view) for mode in ('clay','material') for view in (0,1)},(name,region,'view coverage mismatch')
            for view in row['views']:
                relative=view['image']
                assert relative not in all_images,('duplicate image path',relative)
                all_images.add(relative); image_count+=1
                assert (view.get('width'),view.get('height'))==(1024,704),(name,region,relative,'manifest dimensions mismatch')
                png_check(out/relative,view['image_sha256'],(1024,704))
                scales.append(float(view['ortho_scale']))
                direction=tuple(view['camera_direction'])
                assert directions.setdefault(int(view['view']),direction)==direction,(name,'camera direction differs across regions/modes')
            for view_index in (0,1):
                clay=views['clay',view_index]; material=views['material',view_index]
                assert clay['camera_location']==material['camera_location'] and clay['camera_target']==material['camera_target'],(name,region,'clay/material camera mismatch')
                assert clay['camera_direction']==material['camera_direction'] and clay['ortho_scale']==material['ortho_scale'],(name,region,'clay/material view framing mismatch')
                assert clay['image_sha256']!=material['image_sha256'],(name,region,'clay/material images identical')
            front=views['clay',0]['camera_direction']; rear=views['clay',1]['camera_direction']
            assert all(abs(front[i]+rear[i])<1e-8 for i in (0,1)) and front[2]>0 and rear[2]>0,(name,region,'front/rear angles are not opposed')
            per_function_records.append(row)
        assert seen_regions==set(regions),(name,'not all regions represented')
        assert max(scales)-min(scales)<1e-8,(name,'scale is not common across regions/views')
        settings_by_function[name]=manifest['settings_contract']
        camera_by_function[name]={'directions':{str(key):value for key,value in directions.items()},'ortho_scale':scales[0]}
        records_by_function[name]=per_function_records
    assert len(revision_values)==1,('per-function source revisions differ',revision_values)
    assert image_count==64 and len(all_images)==64,('expected 64 unique individual images',image_count)
    actual_images={p.relative_to(out).as_posix() for p in (out/'individual').glob('*/*.png')}
    assert actual_images==all_images,('unindexed or missing individual images',actual_images.symmetric_difference(all_images))

    sheet_manifest=json.loads((out/'contact_sheets'/'manifest.json').read_text(encoding='utf-8-sig'))
    sheets=sheet_manifest['sheets']
    if isinstance(sheets,dict):sheets_by_function={str(key).upper():value for key,value in sheets.items()}
    else:sheets_by_function={str(row.get('function',row.get('name'))).upper():row for row in sheets}
    assert set(sheets_by_function)==set(functions.values()),('contact sheet functions mismatch',set(sheets_by_function))
    sheet_hashes={}
    for name in function_names:
        function=functions[name]; sheet=sheets_by_function[function]
        assert str(sheet.get('function',name)).lower()==name,(name,'sheet metadata function mismatch')
        expected_revision=manifests[name]['source_revision']
        sheet_revision=sheet.get('source_revision',sheet_manifest.get('source_revision'))
        if isinstance(sheet_revision,(list,tuple)):
            assert expected_revision in sheet_revision,(name,'sheet source revision mismatch')
        else:assert sheet_revision==expected_revision,(name,'sheet source revision mismatch')
        sheet_path=out/sheet['contact_sheet']
        dimensions=png_check(sheet_path,sheet['contact_sheet_sha256'],(4316,3080))
        assert dimensions==(sheet.get('contact_sheet_width'),sheet.get('contact_sheet_height')),(name,'sheet dimension metadata mismatch')
        source_individuals=sheet['source_individuals']
        assert len(source_individuals)==16,(name,'expected 16 source images per sheet')
        expected={(row['region'],mode,view) for row in records_by_function[name] for mode in ('clay','material') for view in (0,1)}
        included=set()
        for item in source_individuals:
            assert item['function']==function,(name,'sheet contains substituted function metadata')
            key=(item['region'],item['mode'],int(item['view']))
            assert key in expected and key not in included,(name,'unexpected or duplicate source image',key)
            included.add(key)
            assert item['result']=='included' and item.get('reason') is None,(name,'sheet has placeholder or substitution',item)
            assert item['image'] in all_images,(name,'sheet references an unindexed image',item['image'])
            observed=digest(out/item['image'])
            assert item['declared_sha256']==item['actual_sha256']==observed,(name,'sheet image hash mismatch',item['image'])
        assert included==expected,(name,'contact sheet image coverage mismatch')
        sheet_hashes[sheet['contact_sheet']]=sheet['contact_sheet_sha256']
    assert len(sheet_hashes)==4

    # These Blender BVH checks are reported separately from current source
    # snapshots: yard fixtures were checked before a shared-capital correction
    # which affected only Thornfell Smithy/Market Hall bearing geometry.
    mesh_check_names=('mesh_checks_stable_gatehouse.json','mesh_checks_smithy_market_hall.json')
    mesh_case_hashes={}
    mesh_check_provenance={}
    for check_name in mesh_check_names:
        check_path=out/check_name
        check=json.loads(check_path.read_text(encoding='utf-8-sig'))
        check_source=dict(check.get('source_sha256',{}))
        assert check_source,(check_name,'native geometry check lacks source provenance')
        mesh_check_provenance[check_name]={'check_file_sha256':digest(check_path),'source_sha256_at_check':check_source,'blender':check.get('blender')}
        for case in check['cases']:
            key=(case['function'],case['region'])
            assert key not in mesh_case_hashes,('duplicate native geometry gate case',key)
            mesh_case_hashes[key]=case['source_geometry_hash']
    expected_mesh_cases={(function.upper(),region) for function in function_names for region in regions}
    assert set(mesh_case_hashes)==expected_mesh_cases,('native geometry gate coverage mismatch',set(mesh_case_hashes)^expected_mesh_cases)
    for name in function_names:
        for row in records_by_function[name]:
            key=(row['function'],row['region'])
            assert mesh_case_hashes[key]==row['geometry_hash'],('native geometry gate is stale or for different geometry',key)

    # Confirm the historical v0.5 gallery still matches its own retained manifests
    # and verification record. This is file/hash validation only; no geometry replay.
    old=ROOT/'evidence'/'archetypes_v05'
    old_report=json.loads((old/'verification.json').read_text(encoding='utf-8-sig'))
    old_sheet_manifest=json.loads((old/'contact_sheets'/'manifest.json').read_text(encoding='utf-8-sig'))
    old_sheets=old_sheet_manifest['sheets']
    if isinstance(old_sheets,dict):old_sheets_by_function={str(key).upper():value for key,value in old_sheets.items()}
    else:old_sheets_by_function={str(row['function']).upper():row for row in old_sheets}
    assert {s['contact_sheet'] for s in old_sheets_by_function.values()}==set(old_report['contact_sheet_sha256']) and len(old_sheets_by_function)==20
    old_manifest_hashes=old_report['archetype_manifest_sha256']; old_images=set(); old_sheet_hashes={}
    old_manifests=list((old/'manifests').glob('*.json'))
    assert len(old_manifests)==20
    for manifest_path in old_manifests:
        assert digest(manifest_path)==old_manifest_hashes[manifest_path.name],('historical manifest changed',manifest_path.name)
        old_manifest=json.loads(manifest_path.read_text(encoding='utf-8-sig'))
        assert len(old_manifest['records'])==4
        for row in old_manifest['records']:
            for view in row['views']:
                relative=view['image']
                assert relative not in old_images,('duplicate historical image',relative)
                old_images.add(relative)
                png_check(old/relative,view['image_sha256'],(1024,704))
    assert len(old_images)==320 and len(list((old/'individual').glob('*/*.png')))==320
    for function,sheet in old_sheets_by_function.items():
        relative=sheet['contact_sheet']
        expected=old_report['contact_sheet_sha256'][relative]
        assert expected==sheet['contact_sheet_sha256'],('historical sheet manifest hash mismatch',relative)
        png_check(old/relative,expected)
        old_sheet_hashes[relative]=expected
    assert len(old_sheet_hashes)==20

    # Validate the final installable archive and the two package reports created
    # by the packaging step. Compare every zip member to its workspace source.
    archive=ROOT/'dist'/'caelmor_architecture.zip'
    archive_hash=digest(archive); archive_members=[]
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.namelist():
            path=ROOT/'caelmor_architecture'/member
            if not path.is_file():path=ROOT/member
            assert path.is_file() and bundle.read(member)==path.read_bytes(),('archive member differs from workspace',member)
            archive_members.append(member)
    package_reports={}
    for report_name in ('installed_extension.json','installed_legacy.json'):
        report_path=out/report_name
        report=json.loads(report_path.read_text(encoding='utf-8-sig'))
        assert report['archive_sha256']==archive_hash,(report_name,'archive SHA-256 mismatch')
        package_reports[report_name]=digest(report_path)

    report={
        'valid':True,
        'source_revision':next(iter(revision_values)),
        'functions':list(functions.values()),'regions':list(regions),
        'configurations':16,'rendered_configurations':16,
        'native_build_validation_records':16,
        'individual_images_verified':image_count,'contact_sheets_verified':len(sheet_hashes),
        'functional_manifest_sha256':manifest_hashes,'functional_source_snapshots':function_source_snapshots,
        'contact_sheet_sha256':sheet_hashes,'functional_settings_contracts':settings_by_function,
        'camera_contracts':camera_by_function,
        'native_geometry_gate_cases':len(mesh_case_hashes),'native_geometry_gate_provenance':mesh_check_provenance,
        'historical_v05_preserved':True,'historical_v05_individual_images_verified':len(old_images),
        'historical_v05_contact_sheets_verified':len(old_sheet_hashes),
        'historical_v05_manifest_sha256':old_manifest_hashes,'historical_v05_contact_sheet_sha256':old_sheet_hashes,
        'addon_source_sha256':source_current,'archive_sha256':archive_hash,
        'archive_members_verified':len(archive_members),'package_report_sha256':package_reports,
        'verification_source_sha256':digest(Path(__file__)),
        'composition_source_sha256':digest(ROOT/'tests'/'compose_archetype_gallery.ps1'),
        'scope':'Manifest/file hash and dimension verification, regional function metadata, settings/camera matching, recorded native build validation, Blender BVH gate geometry-hash correspondence, retained historical v0.5 evidence, and final archive/package-report identity. No geometry replay, rendering, regression suite, Unity runtime check, or final art acceptance was performed.'
    }
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if not k.endswith('_sha256') and 'sha256' not in k},indent=2))


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
    if '--functional-gallery' in sys.argv:verify_functional_gallery()
    elif '--archetype-gallery' in sys.argv:verify_archetypes()
    else:main()
