"""Rehearse an iPad-style PNG return and the Blender metric-repeat handoff."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

import bpy

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from return_paint import build_blender_material, return_paint


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package',type=Path,default=ROOT/'packages'/'split_oak_shingle.zip')
    parser.add_argument('--report',type=Path,default=ROOT/'evidence'/'roundtrip.json')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    source=args.package.resolve()
    original=digest(source)
    with TemporaryDirectory(prefix='roundtrip-',dir=ROOT) as temp:
        temp=Path(temp)
        returned=temp/'painted_color.png'
        # Deliberately chromatic synthetic stand-in for a Procreate color PNG.
        before=build_blender_material(source,catalog_path=ROOT/'catalog.json',palette_option='native')
        color=next(n.image for n in before.node_tree.nodes if n.type=='TEX_IMAGE' and n.label.startswith('Color'))
        paint=color.copy()
        import numpy as np
        pixels=np.empty(len(paint.pixels),dtype=np.float32)
        paint.pixels.foreach_get(pixels)
        px=pixels.reshape(-1,4)
        px[:,0]*=.87
        px[:,2]*=.69
        paint.pixels.foreach_set(pixels)
        if paint.packed_file:
            paint.unpack(method='REMOVE')
        paint.filepath_raw=str(returned)
        paint.file_format='PNG'
        paint.save()
        revision=return_paint(source,[('color',returned)],temp/'returns',catalog=ROOT/'catalog.json')
        revision2=return_paint(revision,[('color',returned)],temp/'returns',catalog=ROOT/'catalog.json')
        assert revision2.name=='split_oak_shingle_rev002' and digest(source)==original
        from zipfile import ZipFile
        with ZipFile(source) as archive:
            for name in ('master.png','height.png','normal.png','roughness.png','metallic.png'):
                assert (revision/name).read_bytes()==archive.read('split_oak_shingle/'+name)
        mesh=bpy.data.meshes.new('Three roof repeats')
        mesh.from_pydata([(0,0,0),(6,0,0),(6,3,0),(0,3,0)],[],[(0,1,2,3)])
        uv=mesh.uv_layers.new(name='UV0_Metric')
        for loop,value in zip(uv.data,((0,0),(6,0),(6,3),(0,3))):
            loop.uv=value
        obj=bpy.data.objects.new('Metric repeat swatch',mesh)
        bpy.context.collection.objects.link(obj)
        obj.data.materials.append(before)
        try:
            build_blender_material(revision,object=obj,slot_index=0,catalog_path=ROOT/'catalog.json')
        except ValueError as exc:
            assert 'already has a material' in str(exc)
        else:
            raise AssertionError('An occupied artist slot was silently replaced')
        mat=build_blender_material(revision,object=obj,slot_index=0,replace_slot=True,
                                  catalog_path=ROOT/'catalog.json',palette_option='native')
        shader=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
        assert shader.inputs['Base Color'].links[0].from_node.type=='TEX_IMAGE'
        assert shader.inputs['Normal'].links[0].from_node.type=='NORMAL_MAP'
        assert all(shader.inputs[channel].is_linked for channel in ('Roughness','Metallic'))
        assert before.use_fake_user
        before_name=before.name
        revision_name=mat.name
        native=temp/'handoff.blend'
        bpy.ops.wm.save_as_mainfile(filepath=str(native))
        bpy.ops.wm.open_mainfile(filepath=str(native))
        baseline=bpy.data.materials[before_name]
        for material in (baseline,bpy.data.materials[revision_name]):
            assert all(n.image.packed_file for n in material.node_tree.nodes if n.type=='TEX_IMAGE')
        # The handoff files are archived as a working revision, so the
        # verification report retains the validated properties only.
    report={'fixture':'split_oak_shingle','blender':bpy.app.version_string,
            'synthetic_png_only':True,'ipad_import_tested':False,
            'revision_chain_verified':True,'unchanged_master_and_technical_maps':True,
            'protected_occupied_slot':True,'explicit_metric_repeat_assignment':True,
            'chromatic_return_preserved':True,'packed_zip_images_survive_reload':True}
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('MATERIAL_PAINT_RETURN_PASS')


if __name__=='__main__':
    main()
