"""Render a linear colour beside two byte-image encoding candidates."""
import bpy,json,sys
from pathlib import Path
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene;scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=192;scene.render.resolution_y=64;scene.render.resolution_percentage=100
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0
for j,value in enumerate((None,.25,1.055*.25**(1/2.4)-.055)):
    bpy.ops.mesh.primitive_plane_add(size=1.9,location=((j-1)*2.,0,0))
    obj=bpy.context.object;mat=bpy.data.materials.new(str(value));mat.use_nodes=True
    obj.data.materials.append(mat);nodes=mat.node_tree.nodes;nodes.clear()
    output=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value=(.25,.25,.25,1.)
    mat.node_tree.links.new(em.outputs[0],output.inputs['Surface'])
    if value is not None:
        image=bpy.data.images.new(str(value),width=4,height=4,alpha=True,float_buffer=False)
        image.colorspace_settings.name='sRGB';image.pixels.foreach_set([value,value,value,1.]*16);image.pack()
        tex=nodes.new('ShaderNodeTexImage');tex.image=image
        mat.node_tree.links.new(tex.outputs['Color'],em.inputs['Color'])
bpy.ops.object.camera_add(location=(0,0,5))
cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=6.
cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();scene.camera=cam
out=Path(__file__).resolve().parents[1]/'evidence/materials_v09/color_space_probe.png'
out.parent.mkdir(exist_ok=True,parents=True);scene.render.filepath=str(out);bpy.ops.render.render(write_still=True)
im=bpy.data.images.load(str(out),check_existing=False);px=list(im.pixels)
samples=[px[(32*192+x)*4:(32*192+x)*4+3] for x in (32,96,160)]
report=dict(direct=samples[0],raw_image=samples[1],srgb_encoded_image=samples[2])
assert max(abs(a-b) for a,b in zip(samples[0],samples[2]))<=2./255
assert min(abs(a-b) for a,b in zip(samples[0],samples[1]))>.1
report['valid']=True
(out.parent/'color_space_probe.json').write_text(json.dumps(report,indent=2))
print('COLOR_SPACE_PROBE',report,flush=True)
