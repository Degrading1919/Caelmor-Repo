"""Read-only artifact/source/camera/package checks for the two art benchmarks."""
import hashlib
import json
from pathlib import Path
import struct
import zipfile
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/benchmarks_v08'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def image(p,expected,size):
    assert sha(p)==expected,p
    data=p.read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n',p
    assert struct.unpack('>II',data[16:24])==tuple(size),p

def main():
    counts=0;geometry={};cost=[];revisions={}
    for function,region in (('SMITHY','LOWMARK'),('GATEHOUSE','THORNFELL')):
        key=function.lower();pair={}
        for stage in ('before','after'):
            record=read(OUT/stage/'cases'/f'{key}.json');pair[stage]=record
            assert record['function']==function and record['region']==region
            assert record['pure_validation']['valid'] and record['native_validation']['valid']
            assert record['geometry_hash']==record['pure_geometry_hash']
            assert record['image_count']==len(record['images'])==12
            views={(v['distance'],v['finish'],v['view']):v for v in record['images']}
            assert set(views)=={(d,f,v) for d in ('normal','distant','close') for f in ('clay','material') for v in (0,1)}
            for v in views.values():
                image(OUT/stage/v['image'],v['image_sha256'],(1024,704));counts+=1
                if v['distance']!='close':assert v['framing_check']['valid']
            if stage=='after':
                for name,digest in record['generator_source_sha256'].items():
                    assert sha(ROOT/'caelmor_architecture'/name)==digest,('stale source',name)
                for name,digest in record['render_source_sha256'].items():
                    assert sha(ROOT/'tests'/name)==digest,('stale renderer',name)
            assert record['render_source_sha256']['render_world_evidence.py']==sha(ROOT/'tests/render_world_evidence.py')
            revisions[stage]=record['source_revision']
        assert pair['before']['settings']==pair['after']['settings']
        before_views={(v['distance'],v['finish'],v['view']):v for v in pair['before']['images']}
        for v in pair['after']['images']:
            old=before_views[v['distance'],v['finish'],v['view']]
            for name in ('camera_target','camera_location','camera_direction','ortho_scale','width','height','samples'):
                assert v[name]==old[name],(function,name)
        original=read(ROOT/'evidence/function_v07/manifests'/f'{key}.json')
        old=next(r for r in original['records'] if r['region']==region)
        assert old['geometry_hash']==pair['before']['geometry_hash'],'Before is not the published 0.7 model'
        geometry[function]=pair['after']['geometry_hash']
        cost.append({'function':function,'region':region,**{
            stage:{k:pair[stage]['pure_validation'][k] for k in ('vertices','triangles','objects')}
            for stage in ('before','after')}})
    composition=read(OUT/'comparison/manifest.json');assert len(composition['sheets'])==6
    for sheet in composition['sheets']:
        image(OUT/sheet['image'],sheet['image_sha256'],(sheet['width'],sheet['height']))
        assert len(sheet['inputs'])==8
    mesh=read(OUT/'mesh_checks.json')
    targeted=read(OUT/'benchmark_mesh_checks.json')
    changes={name for name,value in targeted['source_sha256'].items()
             if mesh['source_sha256'].get(name)!=value}
    assert changes<= {'benchmark_gatehouse.py'},('Unclassified late native source change',changes)
    native={r['function']:r['source_geometry_hash'] for r in targeted['cases']
        if (r['function'],r['region']) in (('SMITHY','LOWMARK'),('GATEHOUSE','THORNFELL'))}
    assert native==geometry
    lifecycle=read(OUT/'lifecycle.json');assert len(lifecycle['cases'])==2
    for row in lifecycle['cases']:
        assert row['geometry_hash']==geometry[row['function']]
        assert all(row[k] for k in ('protected_edit_retained','unprotected_regeneration_restored','saved_reopen','export_reimport'))
        assert sha(OUT/(row['function'].lower()+'.glb'))==row['glb_sha256']
    archive=ROOT/'dist/caelmor_architecture.zip';archive_hash=sha(archive)
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.namelist():
            p=ROOT/'caelmor_architecture'/member
            if not p.is_file():p=ROOT/member
            assert p.read_bytes()==bundle.read(member),('stale package',member)
        members=len(bundle.namelist())
    for name in ('installed_smithy.json','installed_gatehouse.json','installed_legacy.json'):
        assert read(OUT/name)['archive_sha256']==archive_hash
    report={'valid':True,'source_revisions':revisions,'images_verified':counts,'comparison_sheets':6,
        'geometry_costs':cost,'geometry_hashes':geometry,'archive_sha256':archive_hash,'archive_members':members,
        'native_integration_cases':len(mesh['cases']),'targeted_final_native_cases':len(targeted['cases']),
        'late_native_source_changes':sorted(changes),
        'scope':'Fixed-camera matched imagery, actual mesh gate correspondence, two lifecycle checks and final archive identity. Technical evidence; Creative Director art acceptance remains pending.'}
    (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
