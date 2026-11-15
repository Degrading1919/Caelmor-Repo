"""Generate, inspect, and independently verify Lowmark's offline terrain foundation."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

import numpy as np

import terrain
import resolution_study
import visualize_terrain
from tests.test_hydrology_review import independent_d8, review_routing

ROOT = Path(__file__).resolve().parents[3]


def source_digest(path,mode):
    if mode=="utf8_lf":
        text=Path(path).read_text(encoding="utf-8-sig").replace("\r\n","\n").replace("\r","\n")
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sample_grid(field, points, cell=8):
    px=np.clip(points[:,0]/cell,0,field.shape[1]-1); py=np.clip(points[:,1]/cell,0,field.shape[0]-1)
    x0=np.floor(px).astype(int); y0=np.floor(py).astype(int)
    x1=np.minimum(x0+1,field.shape[1]-1); y1=np.minimum(y0+1,field.shape[0]-1)
    tx=px-x0; ty=py-y0
    return field[y0,x0]*(1-tx)*(1-ty)+field[y0,x1]*tx*(1-ty)+field[y1,x0]*(1-tx)*ty+field[y1,x1]*tx*ty


def crossing_points(route, watercourses):
    results=[]
    cross=lambda a,b: a[0]*b[1]-a[1]*b[0]
    for name,water in watercourses:
        for a,b in zip(route[:-1],route[1:]):
            for c,d in zip(water[:-1],water[1:]):
                v=b-a; u=d-c; denominator=cross(v,u)
                if abs(denominator)<1e-9: continue
                t=cross(c-a,u)/denominator; s=cross(c-a,v)/denominator
                # Independently traced routes and reaches round normalized
                # coordinates separately, including at shared endpoints.
                if -1e-7<=t<=1+1e-7 and -1e-7<=s<=1+1e-7:
                    p=a+np.clip(t,0,1)*v
                    if not any(np.linalg.norm(p-np.array(item["xy_m"]))<24 for item in results):
                        results.append({"reach":name,"xy_m":p.tolist(),"status":"Requires a reviewed crossing/structure; no bridge generated."})
    return results


def traversal(controls, result):
    w = controls["world"]
    output = []
    watercourses=[(r["id"],np.asarray(r["points"])*[w["width_m"],w["height_m"]]) for r in controls["hydrology"]["reaches"]]
    for route in controls["routes"]:
        p = np.asarray(route["points"]) * [w["width_m"], w["height_m"]]
        length = float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum())
        points,station,_=terrain.polyline_samples(p,4)
        elevations=sample_grid(result.height_engineered,points)
        grade=np.abs(np.diff(elevations))/np.diff(station)
        crossings=crossing_points(p,watercourses)
        away=np.ones(len(grade),dtype=bool)
        for crossing in crossings:
            away &= np.linalg.norm(points[:-1]-np.asarray(crossing["xy_m"]),axis=1)>50
        output.append({"id": route["id"], "length_m": length,
                       "walk_minutes_at_technical_3mps": length / 180,
                       "sprint_minutes_at_technical_5_5mps": length / 330,
                       "unengineered_ground_grade_max":float(grade.max()),
                       "unengineered_ground_grade_p95":float(np.percentile(grade,95)),
                       "grade_max_away_from_50m_water_crossings":float(grade[away].max()) if away.any() else None,
                       "declared_grade_budget":route["max_grade"],
                       "fraction_above_grade_budget":float((grade>route["max_grade"]).mean()),
                       "crossings":crossings,
                       "note": "Unengineered ground profile; bridge decks, switchbacks, steps and grade slowdown are not built or simulated."})
    return output


def landmarks(controls,result):
    w=controls["world"]; output=[]; slope=terrain.slope_degrees(result.height_engineered,8)
    for landmark in controls.get("landmark_anchors",[]):
        point=np.array(landmark["xy"])*[w["width_m"],w["height_m"]]
        nearest=min(controls["settlements"],key=lambda s:np.linalg.norm(point-np.array(s["xy"])*[w["width_m"],w["height_m"]]))
        distance=float(np.linalg.norm(point-np.array(nearest["xy"])*[w["width_m"],w["height_m"]]))
        output.append({"id":landmark["id"],"xy_m":point.tolist(),"ground_m":float(sample_grid(result.height_engineered,point[None,:])[0]),
             "slope_deg":float(sample_grid(slope,point[None,:])[0]),"nearest_settlement":nearest["id"],
             "distance_to_core_anchor_m":distance,"status":"Anchor/site screen, not built landmark or approved local foundation."})
    return output


def spatial_review(controls, result):
    """Measure retained quest relationships against the current terrain controls."""
    scale = np.array([result.x[-1], result.y[-1]])
    sites = {site["id"]: np.asarray(site["xy"])*scale
             for site in controls["settlements"] + controls["landmark_anchors"]}
    nodes = {node["id"]: node for node in controls["hydrology"]["nodes"]}
    reaches = {reach["id"]: reach for reach in controls["hydrology"]["reaches"]}
    courses = {key: np.asarray(reach["points"])*scale for key, reach in reaches.items()}
    lengths = {key: float(np.linalg.norm(np.diff(points, axis=0), axis=1).sum())
               for key, points in courses.items()}

    def point(identity):
        return sites[identity] if identity in sites else np.asarray(nodes[identity]["xy"])*scale

    def nearest_water(identity, reach_ids):
        xy = point(identity)
        samples = [xy.reshape(1, 2)[:, axis] for axis in range(2)]
        options = [(key, *terrain.project_polyline(courses[key], *samples)) for key in reach_ids]
        key, distance, station = min(options, key=lambda item: item[1][0])
        reach = reaches[key]
        profile_at, profile_z = terrain.reach_profile(reach, nodes, lengths[key])
        width = reach["half_width_m"]
        return {"reach":key, "centreline_distance_m":float(distance[0]),
                "nominal_bank_distance_m":max(0.0,float(distance[0])-width),
                "nearest_reference_stage_m":float(np.interp(station,profile_at,profile_z)[0] + reach.get("water_depth_m",1.2)),
                "anchor_ground_m":float(sample_grid(result.height_engineered,xy[None,:])[0])}

    natural = [key for key, reach in reaches.items() if reach["kind"] == "natural"]
    water_tests = {
        "crest_hall_to_river":("crest_hall",natural),
        "hill_depot_to_river":("hill_depot",natural),
        "drowsebank_yard_to_race":("drowsebank_mill",["drowsebank_mill_leat","drowsebank_wheel_drop","drowsebank_tailrace"]),
        "landing_to_main_river":("whisperflow_landing",["weir_to_whisperflow","whisperflow_eastern_hairpin","lowerbend_to_brookhollow"]),
        "landing_to_western_arm":("whisperflow_landing",["western_whisperflow_arm"]),
        "orchards_to_lower_cut":("floodplain_orchards",["relief_cut_downstream"]),
        "reedmere_to_western_braid":("reedmere",["fen_western_braid"]),
        "mantle_shrine_to_channel":("mantle_shrine",natural),
        "greyharrow_to_branch":("greyharrow",["greyharrow_upper_branch","greyharrow_town_branch","greyharrow_lower_branch"]),
    }
    pairs = [
        ("crestbridge","crest_hall"), ("crest_hall","hill_depot"), ("hill_depot","mill_intake"),
        ("crest_hall","weir_up"), ("drowsebank_mill","weir_up"), ("weir_up","weir_down"),
        ("weir_down","whisperflow_landing"), ("whisperflow_landing","brookhollow"),
        ("ashenstead","cut_corner"), ("whispering_door_farmhouse","ashenstead"),
    ]
    return {"straight_distance_m":{f"{a}_to_{b}":float(np.linalg.norm(point(a)-point(b))) for a,b in pairs},
            "anchor_water_tests":{key:nearest_water(*test) for key,test in water_tests.items()},
            "traced_water_length_m":lengths,
            "scope":"Anchor-to-centreline measurements and nominal width only. No surveyed shore, site access, or quest state is implied."}


def watersheds(controls,result):
    """Model-derived subbasins with boundary-weighted physical area, not rainfall."""
    z=result.height; ny,nx=z.shape; nodes={n["id"]:n for n in controls["hydrology"]["nodes"]}
    weight=np.ones(z.shape,dtype=float)*64
    weight[[0,-1],:]*=.5; weight[:,[0,-1]]*=.5
    weighted=weight.ravel().copy(); receiver=result.receiver.ravel()
    for i in np.argsort(z.ravel(),kind="stable")[::-1]:
        if receiver[i]>=0: weighted[receiver[i]]+=weighted[i]
    expected=controls["world"]["width_m"]*controls["world"]["height_m"]
    if weighted[result.metrics["outlet_cell"]]!=expected: raise AssertionError("Metric catchment area conservation")
    gauges={}; names=["direct_lower_catchment"]
    # Choose a computed main-flow sample inside 40m of each retained anchor, not
    # an invented relocated landscape feature. Nested gauges define first-entry units.
    for name in ("fen_out", "crest", "grey_lower", "weir_down"):
        if name not in nodes: continue
        point=np.asarray(nodes[name]["xy"])*[result.x[-1],result.y[-1]]
        row,col=np.rint(point/8).astype(int)[::-1]
        rr,cc=np.mgrid[max(0,row-5):min(ny,row+6),max(0,col-5):min(nx,col+6)]
        valid=np.hypot(result.x[cc]-point[0],result.y[rr]-point[1])<=40
        cells=(rr*nx+cc)[valid]
        gauge=int(cells[np.argmax(result.accumulation.ravel()[cells])])
        if gauge not in gauges: names.append(name); gauges[gauge]=len(names)-1
    labels=np.zeros(z.size,dtype=np.uint8)
    for i in np.argsort(z.ravel(),kind="stable"):
        labels[i]=gauges[i] if i in gauges else labels[receiver[i]] if receiver[i]>=0 else 0
    areas=[float(weight.ravel()[labels==i].sum()) for i in range(len(names))]
    if sum(areas)!=expected: raise AssertionError("Subbasin partition area conservation")
    result.watershed_labels=labels.reshape(z.shape); result.watershed_names=names
    return {"physical_total_area_m2":expected,"boundary_weighting":"Interior64m², edge32m², corner16m² on the nodal8mgrid",
            "subbasins":[{"id":name,"area_m2":areas[i]} for i,name in enumerate(names)],
            "gauges":[{"id":names[label],"derived_cell":cell,"upstream_area_m2":float(weighted[cell]),"within_authored_anchor_m":40} for cell,label in gauges.items()],
            "interpretation":"Derived D8 subcatchments on the constrained terrain; no surveyed watershed, precipitation or discharge claim."}


def planning_sensitivity(controls, result):
    """Vary declared capacity assumptions without changing a metre of terrain."""
    xx, yy = np.meshgrid(result.x, result.y)
    reports = []
    for identity in ("greyharrow", "drowsebank_mill"):
        for footprint, coverage, slope in ((120, .40, 5), (90, .40, 5), (90, .45, 6)):
            scenario = copy.deepcopy(controls)
            item = next(x for x in scenario["settlements"] if x["id"] == identity)
            item.update(footprint_m2=footprint, plot_coverage=coverage, max_building_slope_deg=slope)
            _, metrics, _ = terrain.settlement_capacity(scenario, xx, yy, result.height_engineered, result.water_level,
                         8, result.reference_stage, result.channel_distance, result.engineered_mask)
            metric = next(x for x in metrics if x["id"] == identity)
            reports.append({"settlement":identity, "average_roof_footprint_m2":footprint,
                            "plot_coverage":coverage,"maximum_site_slope_deg":slope,
                            "normal_stage_capacity":metric["screened_roof_capacity"],
                            "plus_1_5m_scenario_capacity":metric["flood_scenario_safe_capacity"],
                            "status":"Sensitivity only: no building program, grading, anchor relocation or canon promotion."})
    reed = next(x for x in controls["settlements"] if x["id"] == "reedmere")
    requirements = []
    for x, y, z in result.plot_sites["reedmere"]:
        row = min(len(result.y)-1, round(y/8)); col = min(len(result.x)-1, round(x/8))
        requirements.append(max(0, result.reference_stage[row,col] + 1.5 + reed["min_freeboard_m"] - z))
    return {"density_and_foundation_assumptions":reports,
            "reedmere_raised_floor_scenario":{"normal_stage_candidate_centres":len(requirements),
               "plus_1_5m_stage_and_0_3m_freeboard_required_raise_m":
                  [float(min(requirements)),float(max(requirements))] if requirements else [],
               "status":"Conditional raised-floor envelope only. No piles, platforms, boardwalks or geotechnical design generated."}}


def scale_study(controls):
    reports=[]
    for factor, cell in ((2/3,4),(1,8),(4/3,8)):
        c=copy.deepcopy(controls); w=c["world"]
        w["width_m"] = round(w["width_m"]*factor); w["height_m"]=round(w["height_m"]*factor)
        for land in c.get("landforms",[]): land["radius_m"]*=factor
        for corridor in c.get("lowland_corridors",[]):
            # Keep engineering widths physical; this only scales the broad natural-landform envelope.
            for key in ("core_half_width_m","blend_width_m"):
                if key in corridor: corridor[key]*=factor
        item={"width_m":w["width_m"],"height_m":w["height_m"],"resolution_m":cell,
              "area_km2":w["width_m"]*w["height_m"]/1e6,
              "straight_width_walk_minutes":w["width_m"]/180,
              "straight_width_sprint_minutes":w["width_m"]/330}
        try:
            r=terrain.generate(c,cell)
            item.update(status="generated",height_sha256=r.metrics["height_sha256"],
                        normal_capacities={s["id"]:s["screened_roof_capacity"] for s in r.metrics["settlements"]},
                        scenario_capacities={s["id"]:s["flood_scenario_safe_capacity"] for s in r.metrics["settlements"]})
        except (ValueError,AssertionError) as error:
            item.update(status="rejected",reason=str(error))
        reports.append(item)
    return {"scenarios":reports,"interpretation":"Scale comparison, not approved world dimensions. Normalized map anchors fixed; settlement spans and footprint assumptions remain in metres. Broad landform radii scale with extent; water/engineering widths remain physical. Different valid sampling is explicit."}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--controls",type=Path,default=Path(__file__).with_name("lowmark_controls.json"))
    parser.add_argument("--output",type=Path,default=ROOT/"MEDIA/Maps/Lowmark_Terrain")
    args=parser.parse_args(); output=args.output.resolve()
    if not output.is_relative_to(ROOT): raise ValueError("Outputs must remain in the designated checkout")
    c=json.loads(args.controls.read_text(encoding="utf-8-sig"))
    for source in c.get("sources",[]):
        if source_digest(ROOT/source["path"],source.get("hash_mode","raw")) != source["sha256"]:
            raise ValueError("Authored source revision changed; review controls: "+source["path"])
    start=time.perf_counter(); r=terrain.generate(c,8)
    natural=review_routing(r.height,r.receiver,r.accumulation,8,[r.metrics["outlet_cell"]])
    open_rec,open_acc=independent_d8(r.height_engineered,8,r.metrics["outlet_cell"])
    constructed=review_routing(r.height_engineered,open_rec,open_acc,8,[r.metrics["outlet_cell"]])
    repeat=terrain.generate(c,8)
    for field in ("height","height_engineered","receiver","accumulation"):
        if not np.array_equal(getattr(r,field),getattr(repeat,field)):
            raise AssertionError("Determinism failure: "+field)
    controls_hash=source_digest(args.controls,"utf8_lf")
    r.metrics["controls_sha256"]=controls_hash
    basins=watersheds(c,r)
    terrain.export(r,output)
    np.save(output/"height_engineered.npy",r.height_engineered.astype("<f4"),allow_pickle=False)
    np.save(output/"watershed_labels.npy",r.watershed_labels,allow_pickle=False)
    # The exact float authority is preserved; PNG quantization is separately disclosed.
    f32=np.load(output/"height_engineered.npy",allow_pickle=False).astype(float)
    f32rec,f32acc=independent_d8(f32,8,r.metrics["outlet_cell"])
    saved=review_routing(f32,f32rec,f32acc,8,[r.metrics["outlet_cell"]])
    low,high=r.height.min(),r.height.max()
    quantized=np.rint((r.height-low)/(high-low)*65535)/65535*(high-low)+low
    qrec,_=independent_d8(quantized,8,r.metrics["outlet_cell"])
    quantization={"height_png_step_m":float((high-low)/65535),
                  "flat_or_undeclared_terminals_after_16bit_quantization":int(np.sum(qrec==-2)),
                  "authority":"Float32 NPY and full-resolution GLB; 16-bit PNG/32m OBJ are authoring/display exports, not independent hydrological authorities."}
    report={"fixture_source_main":c["authority"]["baseline_commit"],
            "python":platform.python_version(),"numpy":np.__version__,"controls_sha256":controls_hash,
            "natural_dem_independent_review":natural,"open_dem_independent_review":constructed,
            "saved_float32_open_dem_independent_review":saved,"determinism":"Exact same height/open-height/receiver/accumulation arrays on a second full generation",
            "quantization":quantization,"watersheds":basins,"routes":traversal(c,r),"landmark_site_screen":landmarks(c,r),"spatial_review":spatial_review(c,r),"capacity_sensitivity":planning_sensitivity(c,r),
            "world_scale_study":scale_study(c),"resolution_study":resolution_study.study(c),
            "scope":"Offline authoring prototype only; no C#, runtime, buildings, NPCs, production settlement layout or architectural tool changes.",
            "seed_policy":"Current solver uses deterministic authored geometry and analytic refinement; seed is reserved provenance, no unconstrained stochastic noise.",
            "performance_note":"Wall times are observations and intentionally excluded from deterministic geometry hashes.",
            "pipeline_seconds_before_figures":time.perf_counter()-start}
    (output/"verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    visualize_terrain.render(r,c,output)
    print("CAELMOR_TERRAIN_PROTOTYPE_VERIFIED "+json.dumps({"cells":r.height.size,"height_sha256":r.metrics["height_sha256"],"output":str(output)}))


if __name__=="__main__": main()
