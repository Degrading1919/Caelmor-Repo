"""Build or render the bounded stone atlas verification fixture."""
from pathlib import Path
import sys

import bpy
from mathutils import Vector


WIDTH, HEIGHT = 384, 256
FRONTS = ((20, 40, 100, 140), (101, 40, 181, 140), (220, 40, 300, 140))


def build(directory):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    vertices, faces, uv_faces = [], [], []

    def add_face(indices, bounds, mirror=False):
        x0, y0, x1, y1 = bounds
        corners = [(x / WIDTH, 1 - y / HEIGHT) for x, y in
                   ((x0, y1), (x1, y1), (x1, y0), (x0, y0))]
        faces.append(indices)
        uv_faces.append([corners[i] for i in (1, 0, 3, 2)] if mirror else corners)

    for index, (cx, cy, chart) in enumerate(((-.66, .55, 0), (.66, .55, 1),
                                            (-.66, -.55, 2), (.66, -.55, 0))):
        start = len(vertices)
        for w, h, z in ((.55, .425, .08), (.62, .49, 0)):
            vertices.extend((cx + x, cy + y, z) for x, y in
                            ((-w, -h), (w, -h), (w, h), (-w, h)))
        add_face(tuple(range(start, start + 4)), FRONTS[chart], mirror=index == 3)
        for side in range(4):
            a, b = start + side, start + (side + 1) % 4
            row = 165 + (index * 4 + side) * 5
            add_face((b, a, a + 4, b + 4), (20, row, 105, row + 2))

    mesh = bpy.data.meshes.new('Stone fronts and modeled bevels')
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    layer = mesh.uv_layers.new(name='Paint')
    for face, corners in zip(mesh.polygons, uv_faces):
        for loop, uv in zip(face.loop_indices, corners):
            layer.uv[loop].vector = uv
    obj = bpy.data.objects.new('Atlas Stones', mesh)
    bpy.context.collection.objects.link(obj)
    bpy.ops.wm.save_as_mainfile(filepath=str(directory / 'fixture.blend'))


def render(directory):
    scene = bpy.context.scene
    obj = scene.objects['Atlas Stones']
    material = bpy.data.materials.new('Painted stone verification')
    material.use_nodes = True
    obj.data.materials.append(material)
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    shader = nodes.get('Principled BSDF')
    shader.inputs['Roughness'].default_value = .86
    uv = nodes.new('ShaderNodeUVMap')
    uv.uv_map = 'Paint'
    for name in ('albedo', 'normal'):
        tex = nodes.new('ShaderNodeTexImage')
        tex.image = bpy.data.images.load(str(directory / f'{name}.png'))
        tex.extension = 'EXTEND'
        links.new(uv.outputs['UV'], tex.inputs['Vector'])
        if name == 'albedo':
            links.new(tex.outputs['Color'], shader.inputs['Base Color'])
        else:
            tex.image.colorspace_settings.name = 'Non-Color'
            normal = nodes.new('ShaderNodeNormalMap')
            normal.uv_map = 'Paint'
            links.new(tex.outputs['Color'], normal.inputs['Color'])
            links.new(normal.outputs['Normal'], shader.inputs['Normal'])

    bpy.ops.object.camera_add(location=(.6, -1.4, 5.6))
    camera = bpy.context.object
    camera.rotation_euler = (-camera.location).to_track_quat('-Z', 'Y').to_euler()
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = 3.55
    scene.camera = camera
    bpy.ops.object.light_add(type='SUN')
    light = bpy.context.object
    light.data.energy = 2.25
    scene.world = bpy.data.worlds.new('Fixture ambient')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (.12, .12, .12, 1)
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 8
    scene.cycles.use_denoising = False
    scene.render.resolution_x, scene.render.resolution_y = 600, 520
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    for name, direction in (('high', (-.6, -.35, 1.5)), ('raking', (.4, -1.5, .55))):
        light.rotation_euler = (-Vector(direction)).to_track_quat('-Z', 'Y').to_euler()
        for mode, strength in (('paint', 0), ('relief', 1)):
            normal.inputs['Strength'].default_value = strength
            scene.render.filepath = str(directory / f'{name}_{mode}.png')
            bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    mode, folder = sys.argv[sys.argv.index('--') + 1:]
    (build if mode == 'build' else render)(Path(folder))
