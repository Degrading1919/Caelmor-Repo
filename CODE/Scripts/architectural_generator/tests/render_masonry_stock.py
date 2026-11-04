"""Capture the one-seed Thornfell masonry stock study and verify its GLB."""
from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path
import sys

import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_polish_benchmarks import build, capture, settings, export_building
from caelmor_architecture.blender_backend import _settings_dict
from render_world_evidence import _reset_scene
from render_architectural_benchmarks import source_hashes
from test_condition_export import (assert_glb_materials, check_reimport, image_payload,
                                   linked_image, pixel_signature, read_glb, texcoord)

OUT = ROOT / 'evidence' / 'masonry_stock'
BASE = ROOT / 'evidence' / 'diversity_v12'


def mapped_payloads(path):
    doc, binary = read_glb(path)
    materials = {}
    for node in doc['nodes']:
        if 'mesh' not in node:
            continue
        prim = doc['meshes'][node['mesh']]['primitives'][0]
        mat = doc['materials'][prim['material']]
        pbr = mat.get('pbrMetallicRoughness', {})
        if 'baseColorTexture' not in pbr:
            continue
        row = {}
        for key, binding in (('base', pbr['baseColorTexture']), ('normal', mat['normalTexture']),
                             ('orm', pbr['metallicRoughnessTexture'])):
            img = doc['images'][doc['textures'][binding['index']]['source']]
            row[key] = (texcoord(binding), sha256(image_payload(doc,binary,img)).hexdigest())
        materials[node['name']] = row
    return materials


def main():
    baseline = json.loads((BASE/'after/manifest.json').read_text())
    control = next(row for row in baseline['cases']
                   if row['settings']['function']=='GATEHOUSE' and row['settings']['seed']==91)
    before = [r for r in control['images'] if r['finish']=='material']
    s = replace(settings('GATEHOUSE'), crafted_curves=True, seed_massing=True)
    assert _settings_dict(s)==control['settings']
    _reset_scene()
    bpy.data.objects['Neutral ground'].location.z=0.
    collection, metrics = build(s)
    assert collection['caelm_geometry_hash']==control['geometry_hash']
    images = capture(collection, OUT/'after', 'GATEHOUSE', ('material',), ('normal',),
                     vertex_framing=True)
    for a,b in zip(before,images,strict=True):
        assert all(a[key]==b[key] for key in ('camera_location','camera_target','ortho_scale'))
    wall = {o.data.materials[0] for o in collection.objects
            if o.type=='MESH' and '.facade_masonry_skin' in o.get('caelm_buffer_id','')}
    assert len(wall)==1
    material=next(iter(wall))
    snapshots={}
    for socket in ('Base Color','Normal','Roughness','Metallic'):
        im=linked_image(material,socket)
        pixels=np.empty(len(im.pixels),dtype=np.float32)
        im.pixels.foreach_get(pixels)
        stride=max(4,len(pixels)//2048//4*4)
        snapshots[socket]=dict(size=tuple(im.size),signature=pixel_signature(im),
                               pixel_count=len(pixels),
                               samples=[(i,float(pixels[i])) for i in range(0,len(pixels),stride)])
    path=OUT/'gatehouse.glb'
    export_building(collection,str(path))
    doc,binary=read_glb(path)
    checks=assert_glb_materials(doc,binary)
    new=mapped_payloads(path)
    old_path=BASE/'export_validation/gatehouse.glb'
    changes=None
    if old_path.is_file():
        old=mapped_payloads(old_path)
        assert old.keys()==new.keys()
        changes=[name for name in new if new[name]!=old[name]]
        assert changes and all('.facade_masonry_skin' in name for name in changes)
        assert all(new[n]['normal']==old[n]['normal'] and new[n]['orm']==old[n]['orm']
                   and new[n]['base'][0]==old[n]['base'][0] for n in new)
    reimport=check_reimport(path,{material.name:snapshots})
    (OUT/'comparison.json').write_text(json.dumps(dict(
        baseline_revision=baseline['revision'], source_sha256=source_hashes(),
        blender=bpy.app.version_string, settings=_settings_dict(s), metrics=metrics,
        geometry_hash=control['geometry_hash'], before=before, after=images,
        mapped_meshes=len(new),changed_meshes=changes,
        glb_bytes=path.stat().st_size, baseline_glb_bytes=old_path.stat().st_size if old_path.exists() else None,
        material_export=checks,reimport=reimport),indent=2)+'\n')
    print('MASONRY_STOCK_PASS',changes,reimport)


if __name__=='__main__':
    main()
