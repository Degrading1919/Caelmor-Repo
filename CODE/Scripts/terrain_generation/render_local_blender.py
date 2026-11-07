"""Render the saved local terrain in Blender batch mode at true metre scale.

No architecture generator, authored scene, artistic texture, or gameplay is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_blender import create_grid
from terrain import project_polyline
from local_refinement import stage_geometry


def material(name, color, roughness=.9):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def cube(name, xy, base, dimensions, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(*xy, base+dimensions[2]/2))
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    obj["ownership"] = "Disposable inspection proxy; not an architectural asset or approved building placement"
    return obj


def sample(data, point, field="height"):
    x, y, z = data["x"], data["y"], data[field]
    px = np.clip((point[0]-x[0])/(x[1]-x[0]), 0, len(x)-1)
    py = np.clip((point[1]-y[0])/(y[1]-y[0]), 0, len(y)-1)
    c, r = int(px), int(py)
    c1, r1 = min(c+1,len(x)-1), min(r+1,len(y)-1)
    tx, ty = px-c, py-r
    return float(z[r,c]*(1-tx)*(1-ty)+z[r,c1]*tx*(1-ty)+z[r1,c]*(1-tx)*ty+z[r1,c1]*tx*ty)


def covers(data, point):
    return data["x"][0] <= point[0] <= data["x"][-1] and data["y"][0] <= point[1] <= data["y"][-1]


def clipped_water(terrain_obj, data, regional_controls, mat):
    """Intersect static water with the actual Blender terrain triangles.

    Whole-cell wet masks omit narrow diagonal water and create false visual
    breaks. Clip each intersected triangle instead of hiding that geometry.
    """
    xx,yy=np.meshgrid(data["x"],data["y"])
    potential, reference, _=stage_geometry(regional_controls,xx,yy,np.full(xx.shape,-1e6))
    domain=np.where(np.isfinite(potential),-1.,1.).ravel()
    stage=np.where(np.isfinite(potential),potential,reference).ravel()
    ground=data["height"].ravel()
    mesh=terrain_obj.data
    mesh.calc_loop_triangles()
    triangles=np.empty(len(mesh.loop_triangles)*3,dtype=np.int32)
    mesh.loop_triangles.foreach_get("vertices",triangles)
    triangles=triangles.reshape(-1,3)
    selected=(np.min(domain[triangles],axis=1)<0)&(np.min(ground[triangles]-stage[triangles],axis=1)<0)
    coordinates=np.column_stack((xx.ravel(),yy.ravel(),stage+.005,ground-stage,domain))
    vertices=[]; faces=[]
    def clip(poly, index):
        result=[]
        for first,second in zip(poly,poly[1:]+poly[:1]):
            inside0,inside1=first[index]<=0,second[index]<=0
            if inside0: result.append(first)
            if inside0!=inside1:
                result.append(first+(second-first)*(first[index]/(first[index]-second[index])))
        return result
    for ids in triangles[selected]:
        poly=clip(clip([coordinates[index] for index in ids],3),4)
        if len(poly)<3: continue
        start=len(vertices)
        vertices.extend(tuple(point[:3]) for point in poly)
        faces.extend((start,start+i,start+i+1) for i in range(1,len(poly)-1))
    if not vertices: return
    water_mesh=bpy.data.meshes.new(terrain_obj.name+" / clipped static water")
    water_mesh.from_pydata(vertices,[],faces)
    water_mesh.update()
    obj=bpy.data.objects.new(water_mesh.name,water_mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    obj["display_lift_m"]=.005
    obj["scope"]="Static source water surfaces intersected with actual saved terrain; not simulated flow"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--regional", type=Path, required=True)
    parser.add_argument("--controls", type=Path, required=True)
    parser.add_argument("--local", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--samples", type=int, default=12)
    parser.add_argument("--view", default="", help="Render one camera for iteration; default renders every view")
    args = parser.parse_args(sys.argv[sys.argv.index("--")+1:])
    started = time.perf_counter()
    controls = json.loads(args.controls.read_text(encoding="utf-8-sig"))
    regional_controls=json.loads(Path(controls["regional_controls"]).read_text(encoding="utf-8-sig"))
    args.output.mkdir(parents=True, exist_ok=True)
    args.raw.mkdir(parents=True, exist_ok=True)
    with np.load(args.regional, allow_pickle=False) as source:
        regional = {k: source[k] for k in ("x", "y", "height_engineered", "water_level")}
    regional["height"] = np.load(args.local/"composite_regional_height.npy", allow_pickle=False)
    patches = []
    for spec in controls["patches"]:
        with np.load(args.local/(spec["id"]+".npz"), allow_pickle=False) as source:
            patches.append((spec, {k: source[k] for k in source.files}))
    def ground(point):
        return sample(next((d for _, d in patches if covers(d,point)), regional),point)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    scene = bpy.context.scene
    bpy.context.preferences.filepaths.save_version = 0
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = args.samples
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 3
    scene.render.use_persistent_data = True
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (.65,.75,.84,1)
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = .5
    bpy.ops.object.light_add(type="SUN", location=(2500,1000,1000))
    sun = bpy.context.object
    sun.rotation_euler = (math.radians(37),math.radians(-23),math.radians(-30))
    sun.data.energy = 2.3
    sun.data.angle = math.radians(8)
    terrain_mat = material("Shared neutral terrain inspection", (.35,.43,.26))
    water_mat = material("Reference water surface / static", (.055,.24,.32), .28)
    proxy_mat = material("Neutral scale proxies / not architecture", (.55,.54,.49))
    hall_mat = material("Hall anchor proxy", (.43,.32,.22))
    depot_mat = material("Underground depot entrance marker", (.54,.30,.19))
    deck_mat = material("Conditional raised floor test", (.43,.47,.51))
    # Remove all coarse faces owned by a local patch. This prevents double
    # surfaces in the shared Crestbridge/Mill area and preserves world coordinates.
    xx, yy = np.meshgrid(regional["x"][:-1], regional["y"][:-1])
    keep = np.ones(xx.shape,dtype=bool)
    for _, data in patches:
        keep &= ~((xx>=data["x"][0]) & (xx<data["x"][-1]) & (yy>=data["y"][0]) & (yy<data["y"][-1]))
    coarse = create_grid(regional["x"],regional["y"],regional["height"],"Regional surroundings / 8m",keep)
    coarse.data.materials.append(terrain_mat)
    mesh_reports = []
    for spec, data in patches:
        obj = create_grid(data["x"],data["y"],data["height"],spec["id"]+" / saved 2m terrain",triangulate=True)
        obj.data.materials.append(terrain_mat)
        obj["source_npz_sha256"] = hashlib.sha256((args.local/(spec["id"]+".npz")).read_bytes()).hexdigest()
        obj["vertical_exaggeration"] = 1.0
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        path = args.output/(spec["id"]+".glb")
        staged=args.raw/(spec["id"]+".staged.glb")
        bpy.ops.export_scene.gltf(filepath=str(staged.resolve()),export_format="GLB",use_selection=True,
                                  export_yup=True,export_extras=True,export_normals=True,export_texcoords=False)
        staged.replace(path)
        mesh_reports.append({"id":spec["id"],"vertices":len(obj.data.vertices),"triangles":len(obj.data.polygons),
                             "glb_bytes":path.stat().st_size,"source_npz_sha256":obj["source_npz_sha256"]})
        clipped_water(obj,data,regional_controls,water_mat)
        # road_mask includes the grading blend. Display the declared travel lane
        # instead of making every earthwork shoulder appear to be a wide road.
        lane=np.zeros(data["height"].shape,dtype=float)
        tx,ty=np.meshgrid(data["x"],data["y"])
        for route in regional_controls["routes"]:
            if route["id"] not in spec["route_ids"]: continue
            points=np.asarray(route["points"])*[regional_controls["world"]["width_m"],regional_controls["world"]["height_m"]]
            distance,_=project_polyline(points,tx,ty)
            lane=np.maximum(lane,np.clip((controls["roads"]["half_width_m"]+.25-distance)/.5,0,1))
        coverage=lane*data["road_mask"]*~data["river_mask"]
        attribute=obj.data.attributes.new("inspection_road_coverage","FLOAT","POINT")
        attribute.data.foreach_set("value",coverage.astype(np.float32).ravel())
    # Color existing terrain instead of floating road polygons, which can make
    # sampled edges cast false sawtooth shadows in the eye-level inspection.
    tree=terrain_mat.node_tree
    attribute=tree.nodes.new("ShaderNodeAttribute")
    attribute.attribute_name="inspection_road_coverage"
    mix=tree.nodes.new("ShaderNodeMixRGB")
    mix.inputs[1].default_value=(.35,.43,.26,1)
    mix.inputs[2].default_value=(.43,.32,.20,1)
    tree.links.new(attribute.outputs["Fac"],mix.inputs[0])
    tree.links.new(mix.outputs["Color"],tree.nodes.get("Principled BSDF").inputs["Base Color"])
    anchors = {a["id"]:a for a in controls["inspection"]["anchors"]}
    labels = []
    for item in controls["inspection"]["proxies"]:
        if item["type"] == "bridge_deck":
            endpoints = np.asarray(item["endpoints_xy_m"])
            center = endpoints.mean(axis=0)
            direction = endpoints[1]-endpoints[0]
            length = float(np.linalg.norm(direction))
            base = item["deck_top_m"]-item["deck_thickness_m"]
            obj = cube(item["id"],center,base,(item["width_m"],length,item["deck_thickness_m"]),proxy_mat)
            obj.rotation_euler.z = -math.atan2(direction[0],direction[1])
            labels.append({"id":"bridge_proxy","point":[*center,item["deck_top_m"]+1],"text":"Crossing: technical deck proxy"})
            for endpoint in endpoints:
                z=ground(endpoint)
                cube("Uncertified bridge support proxy",endpoint,z,(2,2,max(.2,base-z)),proxy_mat)
        elif item["type"] == "box":
            point = item.get("xy_m",anchors.get(item.get("anchor_id"),{}).get("xy_m"))
            z = ground(point)
            mat = hall_mat if "hall" in item["id"] else depot_mat if "depot" in item["id"] else proxy_mat
            cube(item["id"],point,z,(*item["footprint_m"],item["height_m"]),mat)
            texts={"crest_hall_scale_proxy":"Crest Hall: fixed anchor / size proxy",
                   "depot_area_marker":"Hill Depot: underground area marker",
                   "granary_yard_concept":"Granary concept ONLY: no approved XY"}
            labels.append({"id":item["id"],"point":[*point,z+item["height_m"]+2],"text":texts.get(item["id"],item["id"]),"ground_m":z})
    # A few conditional Reedmere floor tests communicate elevation, not a hamlet.
    # Only explicitly declared technical floor tests become proxies; capacity
    # centers are not automatically converted into buildings or a hamlet.
    for point in controls["inspection"].get("reedmere_floor_test_xy_m",[]):
        z=ground(point)
        normal=sample(regional,point,"water_level")
        if not np.isfinite(normal): continue
        corners=np.array([[point[0]+dx,point[1]+dy] for dx in (-5,5) for dy in (-4,4)])
        _,reference,_=stage_geometry(regional_controls,corners[:,0],corners[:,1],np.array([ground(q) for q in corners]))
        normal=float(reference.max())
        floor=normal+1.5+.3
        cube("Conditional raised floor / no building",point,floor-.2,(10,8,.2),deck_mat)
        for dx in (-4,4):
            for dy in (-3,3):
                base=ground((point[0]+dx,point[1]+dy))
                cube("Conditional pile / geotechnics unresolved",(point[0]+dx,point[1]+dy),base,(.3,.3,max(.2,floor-.2-base)),proxy_mat)
    cameras=list(controls["inspection"]["cameras"])
    cameras.extend([
        {"id":"greyharrow_local","position_xy_m":[5100,850],"eye_height_above_ground_m":230,
         "target_xy_m":[5450,1250],"target_height_above_ground_m":2,"lens_mm":43},
        {"id":"reedmere_local","position_xy_m":[850,2370],"eye_height_above_ground_m":150,
         "target_xy_m":[440,2770],"target_height_above_ground_m":1,"lens_mm":43},
        {"id":"reedmere_floor_detail","position_xy_m":[400,2700],"eye_height_above_ground_m":4,
         "target_xy_m":[416,2744],"target_height_above_ground_m":1.4,"lens_mm":35},
        {"id":"drowsebank_local","position_xy_m":[2770,1000],"eye_height_above_ground_m":170,
         "target_xy_m":[3040,1250],"target_height_above_ground_m":2,"lens_mm":42}])
    bpy.context.view_layer.update()
    views=[]
    for camera_spec in cameras:
        camera_data=bpy.data.cameras.new(camera_spec["id"])
        camera=bpy.data.objects.new(camera_spec["id"],camera_data)
        scene.collection.objects.link(camera)
        point=camera_spec["position_xy_m"]
        eye=ground(point)+camera_spec["eye_height_above_ground_m"]
        camera.location=(*point,eye)
        target=camera_spec["target_xy_m"]
        target_z=ground(target)+camera_spec["target_height_above_ground_m"]
        camera.rotation_euler=(Vector((*target,target_z))-camera.location).to_track_quat("-Z","Y").to_euler()
        camera_data.lens=camera_spec["lens_mm"]
        camera_data.clip_end=20000
        camera_data.clip_start=.1
        scene.camera=camera
        bpy.context.view_layer.update()
        if camera_spec["id"] in ("crestbridge_broad_elevated","crestbridge_relationships"):
            for _ in range(24):
                projected=[world_to_camera_view(scene,camera,Vector(label["point"])) for label in labels]
                if all(p.z>0 and .07<p.x<.93 and .08<p.y<.92 for p in projected): break
                camera_data.lens*=.94
                bpy.context.view_layer.update()
            else:
                raise AssertionError("Required Crestbridge relationship markers do not fit the camera")
        view_labels=[]
        for label in labels:
            projected=world_to_camera_view(scene,camera,Vector(label["point"]))
            if projected.z>0 and 0<projected.x<1 and 0<projected.y<1:
                view_labels.append({**label,"normalized_pixel_xy":[projected.x,1-projected.y]})
        view={"id":camera_spec["id"],"position_east_north_up_m":list(camera.location),
              "eye_height_above_sampled_ground_m":camera_spec["eye_height_above_ground_m"],
              "target_east_north_up_m":[*target,target_z],"lens_mm":camera_data.lens,
              "vertical_scale":1,"labels":view_labels,"raw_path":str((args.raw/(camera_spec["id"]+".png")).resolve())}
        if not args.view or args.view==camera_spec["id"]:
            frame_start=time.perf_counter()
            scene.render.filepath=view["raw_path"]
            bpy.ops.render.render(write_still=True)
            view["render_seconds"]=time.perf_counter()-frame_start
        views.append(view)
    scene["purpose"]="Offline inspection only; true metre scale; neutral scale proxies; no authored world scene"
    scene["parent_main"]="3ec4003"
    scene["vertical_scale"]=1.0
    bpy.ops.wm.save_as_mainfile(filepath=str((args.output/"local_inspection.blend").resolve()),compress=True)
    report={"blender":bpy.app.version_string,"blender_hash":bpy.app.build_hash.decode(),
            "render_engine":scene.render.engine,"samples":args.samples,"resolution":[1600,1000],
            "vertical_scale":1,"meshes":mesh_reports,"views":views,
            "scope":"Actual saved 2m terrain, static water, candidate roads and explicitly conceptual scale proxies. No architecture assets or runtime validation.",
            "total_seconds":time.perf_counter()-started}
    (args.output/"render_metadata.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("CAELMOR_LOCAL_3D_INSPECTION "+json.dumps({"meshes":len(mesh_reports),"views":len(views),"seconds":report["total_seconds"]}))


if __name__=="__main__": main()
