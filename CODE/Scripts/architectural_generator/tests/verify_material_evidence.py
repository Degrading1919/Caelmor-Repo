"""Deterministic bookkeeping for captures, bindings, package and historical data."""
from pathlib import Path
import hashlib,json,struct,zipfile
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/materials_v09'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def check_image(path,digest):
    assert sha(path)==digest,path
    data=path.read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n'
    return struct.unpack('>II',data[16:24])

capture=read(OUT/'final/manifest.json')
assert capture['source_unchanged_during_capture'] and capture['image_count']==44
assert len(capture['images'])==44
for name,digest in capture['source_hashes'].items():assert sha(ROOT/'caelmor_architecture'/name)==digest,name
variants={'reference','young','old','neglected','maintained','modest','affluent','rough','fine','modest_maintained','affluent_neglected'}
camera_error=0.
for function in ('SMITHY','GATEHOUSE'):
    rows=[r for r in capture['images'] if r['function']==function]
    assert len(rows)==22 and {r['variant'] for r in rows}==variants
    old=read(ROOT/'evidence/benchmarks_v08/after/cases'/(function.lower()+'.json'))
    assert all(r['geometry_hash']==old['geometry_hash'] for r in rows)
    assert all(r['geometry_settings']==old['settings'] for r in rows)
    for row in rows:
        assert check_image(OUT/'final'/row['image'],row['image_sha256'])==(1024,704)
        before=next(r for r in old['images'] if r['distance']==row['distance'] and r['finish']=='material' and r['view']==0)
        # v08 serialized mathutils float32 targets; v09 records the same Python
        # target tuple. Compare within float32 serialization tolerance.
        delta=max(abs(a-b) for field in ('camera_target','camera_location') for a,b in zip(row[field],before[field]))
        assert delta<2e-6,delta
        camera_error=max(camera_error,delta)
        assert row['ortho_scale']==before['ortho_scale']
    settings={r['variant']:r['surface_settings'] for r in rows}
    for a,b,fields in (('young','old',{'age'}),('neglected','maintained',{'maintenance'}),
                       ('modest','affluent',{'wealth'}),('rough','fine',{'craftsmanship'}),
                       ('modest_maintained','affluent_neglected',{'wealth','maintenance'})):
        assert {k for k in settings[a] if settings[a][k]!=settings[b][k]}==fields,(a,b)

sheets=read(OUT/'comparison/manifest.json')['sheets'];assert len(sheets)==6
for sheet in sheets:
    assert check_image(OUT/sheet['image'],sheet['sha256'])==(sheet['width'],sheet['height'])
    for item in sheet['inputs']:check_image(OUT/item['path'],item['sha256'])
native=read(OUT/'export_checks.json');assert native['source_unchanged_during_run']
for name,digest in native['source_sha256'].items():assert sha(ROOT/'caelmor_architecture'/name)==digest,name
assert native['png_payloads_equal_to_pre_context_fix']
for case in native['cases']:
    assert sha(OUT/(case['function'].lower()+'.glb'))==case['glb_sha256']
    assert case['uv2_exported_corner_values_checked']>0
    assert case['reimport']['reimported_pixel_map_checks']>0
assert native['cases'][0]['regeneration_protection_override']['roof_only_max_sample_error']<2.1/255
roundtrip=read(OUT/'roundtrip/manifest.json');assert len(roundtrip['images'])==4
for row in roundtrip['images']:
    assert sha(OUT/(row['function'].lower()+'.glb'))==row['glb_sha256']
    check_image(OUT/'roundtrip'/row['image'],row['sha256'])
assert read(OUT/'legacy_surface_check.json')['result']=='PASS'
assert read(OUT/'color_space_probe.json')['valid']
boundary=read(OUT/'range_check.json');assert boundary['valid']
assert boundary['settings']['detail']=='HIGH' and boundary['settings']['floors']==3
assert all(max(s['size'])<=4096 for s in boundary['surfaces'])

archive=ROOT/'dist/caelmor_architecture.zip';archive_hash=sha(archive)
for function in ('smithy','gatehouse'):
    install=read(OUT/('install_'+function+'.json'))
    assert install['archive_sha256']==archive_hash and install['native_install_and_generate']
with zipfile.ZipFile(archive) as z:
    for name in z.namelist():
        source=ROOT/'caelmor_architecture'/name
        if not source.exists():source=ROOT/name
        assert z.read(name)==source.read_bytes(),name
    members=len(z.namelist())
# Previously source-pinned images remain evidence, not regenerated baselines.
historical=0
for stage in ('before','after'):
    for function in ('smithy','gatehouse'):
        root=ROOT/'evidence/benchmarks_v08'/stage
        case=read(root/'cases'/(function+'.json'))
        for row in case['images']:
            check_image(root/row['image'],row['image_sha256']);historical+=1

diagnostics=[]
for function in ('SMITHY','GATEHOUSE'):
    ref=next(r for r in capture['images'] if r['function']==function and r['variant']=='reference')
    diagnostics.append(dict(function=function,geometry_hash=ref['geometry_hash'],
        atlas_banks=len(ref['surfaces']),atlas_maps=3*len(ref['surfaces']),
        atlas_texels=sum(r['size'][0]*r['size'][1] for r in ref['surfaces']),
        glb_bytes=(OUT/(function.lower()+'.glb')).stat().st_size,
        blend_bytes=(OUT/'final'/(function.lower()+'.blend')).stat().st_size))
report=dict(valid=True,source_revision=capture['source_revision'],images_verified=44,roundtrip_images=4,
    max_camera_metadata_delta_metres=camera_error,
    comparison_sheets=6,historical_benchmark_images_verified=historical,archive_sha256=archive_hash,
    archive_members=members,asset_diagnostics=diagnostics,
    scope='Source/image/archive correspondence and executed native reports; not final artistic acceptance or runtime performance.')
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print('MATERIAL_EVIDENCE_VERIFIED',json.dumps(report,sort_keys=True))
