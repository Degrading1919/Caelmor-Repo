"""Export disposable Unity benchmark inputs from the saved showcase."""
import collections
import json
import shutil
import struct
from pathlib import Path
import sys
import tempfile
import bpy
from mathutils import Euler, Matrix, Vector

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from caelmor_architecture.blender_backend import export_building, TAG
from caelmor_architecture.roof_autocomplete import build_roof_collection
from caelmor_architecture.roof_selection import Bearing

DEST=HERE/".perf"
DEST.mkdir(exist_ok=True)
OUT=Path(tempfile.mkdtemp(prefix="export-",dir=DEST))
OUT.mkdir(exist_ok=True)
report={}
for name in ("Farmhouse","Cottage","Workshop"):
    body=bpy.data.collections[f"{name} · Generator body"]
    roof=bpy.data.collections[f"{name} · Roof AutoComplete"]
    anchor=next(o for o in body.objects if o.get("caelm_anchor"))
    original=json.loads(roof["caelm_roof_settings"])
    field=next(o.data.materials[0] for o in roof.objects if "RoofUV" in o.data.uv_layers)
    for obj in list(body.objects):
        if obj.type=="MESH" and obj.hide_render and not obj.get("caelm_collider"):
            body.objects.unlink(obj)
    settings=original.copy()
    center,width,depth,angle,rects=(settings.pop(k) for k in ("center","width","depth","angle","rects"))
    settings["material_directory"]=str(HERE.parents[4]/"MEDIA/Materials/procedurally_generated")
    # Resolve generated alternatives with the exact same roof bearing and native UV generator.
    for detail in dict.fromkeys((original["detail"],0,50,100)):
        if detail!=original["detail"] or f"{name.lower()}_{detail}.glb" in report:
            settings["detail"]=detail
            active=build_roof_collection(bpy.context.scene,Bearing(tuple(center),width,depth,angle,tuple(map(tuple,rects))),**settings)
        else:
            active=roof
        linked=[]
        for obj in active.objects:
            if obj.hide_render or obj.name.startswith("Gable infill"): continue
            if "RoofUV" in obj.data.uv_layers:
                obj.data.materials[0]=field
            world=obj.matrix_world.copy()
            obj.parent=anchor
            obj.matrix_world=world
            obj[TAG]=True
            obj["caelm_layer"]="roof"
            body.objects.link(obj)
            linked.append(obj)
        path=OUT/f"{name.lower()}_{detail}.glb"
        export_building(body,str(path),construction_metadata=True)
        report[path.name]={"shingles":active["caelm_roof_shingles"],"roof_triangles":active["caelm_roof_triangles"],"source_detail":original["detail"]}
        for obj in linked: body.objects.unlink(obj)
        if active!=roof:
            for obj in list(active.objects): bpy.data.objects.remove(obj,do_unlink=True)
            bpy.data.collections.remove(active)
    report[name.lower()]={"detail":original["detail"],"glass_panes":len(bpy.data.collections[f"{name} · Handcrafted glazing"].objects)}




def adapt_specular(path):
    """Record the showcase's dielectric PBR approximation for this fixture."""
    import struct
    raw=path.read_bytes()
    size=struct.unpack_from("<I",raw,12)[0]
    document=json.loads(raw[20:20+size])
    factors={}
    for material in document["materials"]:
        extensions=material.get("extensions",{})
        specular=extensions.pop("KHR_materials_specular",None)
        if specular is not None:
            if set(specular)!={"specularFactor"}:
                raise ValueError("Unreviewed specular extension")
            factors[material["name"]]=specular["specularFactor"]
        if not extensions: material.pop("extensions",None)
    for key in ("extensionsUsed","extensionsRequired"):
        if key in document:
            document[key]=[value for value in document[key] if value!="KHR_materials_specular"]
    body=json.dumps(document,separators=(",",":")).encode()
    body+=b" "*(-len(body)%4)
    binary=raw[20+size:]
    staging=path.parent/"import"/path.name
    staging.write_bytes(struct.pack("<III",0x46546c67,2,20+len(body)+len(binary))
                     +struct.pack("<II",len(body),0x4e4f534a)+body+binary)
    for suffix in (".caelmor.json",".collision.glb"):
        shutil.copyfile(path.with_suffix(suffix), staging.with_suffix(suffix))
    return factors

(OUT/"import").mkdir()
for key,value in report.items():
    if key.endswith(".glb"):
        value["approximated_specular_factors"]=adapt_specular(OUT/key)
scene=bpy.context.scene
camera_report={}
for obj in scene.objects:
    if obj.type=="CAMERA":
        forward=obj.matrix_world.to_quaternion() @ Vector((0,0,-1))
        camera_report[obj.name]={"position":list(obj.matrix_world.translation),"forward":list(forward),"horizontal_fov":obj.data.angle_x*180/3.141592653589793}
report["cameras"]=camera_report



DEST=OUT/"import"


# Use the showcase's actual scattered roots and linked specimens.
import collections
import struct
from mathutils import Euler, Matrix
scatter=bpy.data.collections["Vegetation · Settlement verges and pasture"]
batch=next(iter(scatter.objects))
source=next(n for n in batch.modifiers[0].node_group.nodes if n.type=="COLLECTION_INFO").inputs["Collection"].default_value
specimens=list(source.objects)
groups=collections.defaultdict(list)
basis=Matrix(((-1,0,0,0),(0,0,1,0),(0,-1,0,0),(0,0,0,1)))
for batch in sorted(scatter.objects,key=lambda ob:ob.name):
    mesh=batch.data
    for vertex, asset, rotation, scale in zip(mesh.vertices,mesh.attributes["cv_asset"].data,
                                              mesh.attributes["cv_rotation"].data,mesh.attributes["cv_scale"].data):
        local=Matrix.LocRotScale(vertex.co,Euler(rotation.vector),Vector(scale.vector))
        matrix=basis @ batch.matrix_world @ local @ basis.inverted()
        groups[batch.name,asset.value].append(matrix)
with (DEST/"scatter.bytes").open("wb") as stream:
    blocks=[(index,poses[start:start+1023]) for (_,index),poses in groups.items() for start in range(0,len(poses),1023)]
    stream.write(struct.pack("<i",len(blocks)))
    for index,poses in blocks:
        stream.write(struct.pack("<ii",index,len(poses)))
        for matrix in poses: stream.write(struct.pack("<16f",*(v for row in matrix for v in row)))
bpy.ops.object.select_all(action="DESELECT")
for index,specimen in enumerate(specimens):
    obj=bpy.data.objects.new(f"specimen_{index}",specimen.data)
    bpy.context.scene.collection.objects.link(obj)
    obj.select_set(True)
target=DEST/"plants.stage.glb"
bpy.ops.export_scene.gltf(filepath=str(target),export_format="GLB",use_selection=True,export_yup=True)
target.replace(DEST/"plants.glb")





lookup={specimen.name:index for index,specimen in enumerate(specimens)}
(DEST/"lod.json").write_text(json.dumps([lookup[specimen.name.rsplit("LOD",1)[0]+"LOD2"] for specimen in specimens]),encoding="utf-8")

bpy.ops.object.select_all(action="DESELECT")
for collection in bpy.data.collections:
    if collection.name.endswith(" · Handcrafted glazing"):
        for pane in collection.objects:
            pane.select_set(True)
probe=OUT/"glass-probe.glb"
bpy.ops.export_scene.gltf(filepath=str(probe),export_format="GLB",use_selection=True)
with probe.open("rb") as stream:
    header=stream.read(20)
    glas=json.loads(stream.read(struct.unpack_from("<I",header,12)[0]))
report["glass_probe"]={
    "panes":len(glas["nodes"]),
    "triangles":sum(glas["accessors"][p["indices"]]["count"]//3
                    for m in glas["meshes"] for p in m["primitives"]),
    "extensions":glas.get("extensionsUsed",[]),
    "exported_materials":glas["materials"],
}
report["foliage"]={"instances":sum(len(poses) for _,poses in blocks),"groups":len(blocks),
                   "specimens":len(specimens),"blender_triangles":scatter["triangles"],
                   "blender_lod_counts":list(scatter["lod_counts"])}
bpy.ops.object.select_all(action="DESELECT")
for collection in bpy.data.collections:
    if collection.name.startswith("Ground ·"):
        for obj in collection.objects:
            if obj.type == "MESH": obj.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(DEST/"ground.glb"),export_format="GLB",
                         use_selection=True,export_materials="NONE",export_yup=True)
(DEST/"export.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print("CAELMOR_PERF_EXPORT",DEST,flush=True)
