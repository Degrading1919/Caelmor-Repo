"""Controlled native, export and render evidence for construction depth."""
from collections import defaultdict
from dataclasses import replace
import json
from pathlib import Path
import struct
import sys
from tempfile import TemporaryDirectory

import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_construction_treatments as studio
from test_condition_export import assert_glb_materials, image_payload, read_glb
from test_construction_library import overrides
from caelmor_architecture.blender_backend import build, export_building, _settings_dict
from caelmor_architecture.engine import generate, validate

OUT=studio.ROOT/'evidence'/'construction_depth'
MODES=('MODELED','HYBRID','TEXTURE')


def settings_for(function,mode):
    opts=overrides('timber_shingle') if function=='SMITHY' else {'by_role':{}}
    role='roof_cover' if function=='SMITHY' else 'wall_body'
    if mode!='MODELED':
        opts['by_role'].setdefault(role,{})['representation']=mode
    return replace(studio.settings(function),crafted_curves=True,seed_massing=True,
                   construction_overrides=opts)


def image_bytes_with_mips(width,height):
    size=0
    while True:
        size+=width*height*4
        if width==height==1:
            return size
        width,height=max(1,width//2),max(1,height//2)


def export_metrics(path):
    doc,binary=read_glb(path)
    checked=assert_glb_materials(doc,binary)
    prims=[primitive for node in doc['nodes'] if 'mesh' in node
           for primitive in doc['meshes'][node['mesh']]['primitives']]
    images=[]
    for info in doc['images']:
        png=image_payload(doc,binary,info)
        width,height=struct.unpack_from('>II',png,16)
        images.append({'name':info.get('name',''),'width':width,'height':height,
                       'png_bytes':len(png),'rgba8_mipped_bytes':image_bytes_with_mips(width,height)})
    field_materials=[]
    for mat in doc['materials']:
        base=mat.get('pbrMetallicRoughness',{}).get('baseColorTexture')
        if base is None:
            continue
        tex=doc['textures'][base['index']]
        if not images[tex['source']]['name'].startswith('Caelmor Field '):
            continue
        field_materials.append(mat['name'])
        for info in (base,mat['normalTexture'],mat['pbrMetallicRoughness']['metallicRoughnessTexture']):
            tex=doc['textures'][info['index']]
            sampler=doc.get('samplers',[])[tex['sampler']] if 'sampler' in tex else {}
            assert sampler.get('wrapS',10497)==10497 and sampler.get('wrapT',10497)==10497
        assert mat['normalTexture'].get('texCoord',0)==base.get('texCoord',0)
    return {'bytes':path.stat().st_size,'materials':len(doc['materials']),
            'textures':len(doc['textures']),'images':images,
            'rgba8_mipped_bytes':sum(i['rgba8_mipped_bytes'] for i in images),
            'primitives':len(prims),'blended_primitives':sum(
                doc['materials'][p['material']].get('alphaMode')=='BLEND' for p in prims if 'material' in p),
            'vertex_records':sum(doc['accessors'][p['attributes']['POSITION']]['count'] for p in prims),
            'mapped_materials':checked['materials_with_maps'],'shared_field_materials':field_materials}


def capture_case(function,mode):
    settings=settings_for(function,mode)
    scene,_=studio._reset_scene()
    bpy.data.objects['Neutral ground'].location.z=0.
    sun=next(o for o in scene.objects if o.type=='LIGHT' and o.data.type=='SUN')
    sun.rotation_euler=(.88,.57,-.23)
    sun.data.angle=.07
    fill=next(o for o in scene.objects if o.type=='LIGHT' and o.data.type=='AREA')
    fill.data.energy=750
    plan,buffers=generate(settings)
    report=validate(plan,buffers)
    assert report['valid'],report['errors']
    collection,_=build(settings)
    assert collection['caelm_source_geometry_hash']==report['geometry_hash']
    frames=studio.capture(collection,OUT/mode.lower(),function,distances=('normal','close'),
                          views=(0,),vertex_framing=True)
    for frame in frames:
        frame['image']=mode.lower()+'/'+frame['image']
    with TemporaryDirectory(prefix='depth_bench_',dir=studio.ROOT/'dist') as temp:
        path=Path(temp)/(function.lower()+'.glb')
        export_building(collection,str(path),construction_metadata=True)
        export=export_metrics(path)
        assert bool(export['shared_field_materials'])==(mode!='MODELED')
        if mode=='HYBRID':
            # Exercise the actual exported node/UV configuration and retain
            # one visual round trip per fixture under the same studio.
            for obj in list(collection.objects):
                if obj.type=='MESH':
                    obj.hide_render=True
            bpy.ops.import_scene.gltf(filepath=str(path))
            imported=bpy.context.selected_objects
            proxy=bpy.data.collections.new('Export review')
            scene.collection.children.link(proxy)
            for obj in imported:
                proxy.objects.link(obj)
            meshes=[o for o in proxy.objects if o.type=='MESH']
            assert meshes and any(len(o.data.uv_layers)>=3 for o in meshes)
            glb=studio.capture(proxy,OUT/'glb',function,finishes=('material',),distances=('normal',),
                               views=(0,),vertex_framing=True)
            for frame in glb:
                frame['image']='glb/'+frame['image']
            frames.extend(glb)
    layers=defaultdict(lambda:{'vertices':0,'triangles':0,'buffers':0})
    for b in buffers:
        layer=layers[b.layer]
        layer['vertices']+=len(b.vertices)
        layer['triangles']+=sum(len(face)-2 for face in b.faces)
        layer['buffers']+=1
    return {'function':function,'representation':mode,'settings':_settings_dict(settings),
            'geometry_hash':report['geometry_hash'],'triangles':report['triangles'],
            'vertices':report['vertices'],'layers':dict(layers),'frames':frames,'export':export}


def main():
    specs=studio.CASE_SPECS
    specs['SMITHY']['targets']['close']=(4.25,2.1,3.85)
    specs['SMITHY']['scales']['close']=9.5
    specs['SMITHY']['directions']['close']=((.95,-.86,.75),(-.8,-1.2,.4))
    specs['GATEHOUSE']['targets']['close_front']=(12.7,1.7,3.7)
    specs['GATEHOUSE']['scales']['normal']=32.
    specs['GATEHOUSE']['scales']['close']=11.
    results=[]
    for function in ('SMITHY','GATEHOUSE'):
        rows=[capture_case(function,mode) for mode in MODES]
        reference=rows[0]['frames']
        for row in rows[1:]:
            for a,b in zip(reference,row['frames'][:len(reference)],strict=True):
                assert all(a[k]==b[k] for k in ('camera_location','camera_target','ortho_scale'))
        results.extend(rows)
    (OUT/'manifest.json').write_text(json.dumps(dict(blender=bpy.app.version_string,
        source_sha256=studio.source_hashes(),baseline_commit='414bd97',cases=results),indent=2)+'\n')


if __name__=='__main__':
    main()
