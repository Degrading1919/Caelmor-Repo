"""Bake verified terrain samples for the isolated Unity walking inspector."""
import argparse
import hashlib
import json
from pathlib import Path
import struct

import numpy as np

import terrain


def text(stream, value):
    encoded = str(value).encode("utf-8")
    length = len(encoded)
    while length >= 128:
        stream.write(bytes([(length & 127) | 128])); length >>= 7
    stream.write(bytes([length])); stream.write(encoded)


def main():
    root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--regional", type=Path, default=root / "MEDIA/Maps/Lowmark_Terrain/terrain_arrays.npz")
    parser.add_argument("--locals", type=Path, default=root / "MEDIA/Maps/Lowmark_Terrain/Local_Refinement")
    parser.add_argument("--controls", type=Path, default=Path(__file__).with_name("lowmark_controls.json"))
    parser.add_argument("--local-controls", type=Path, default=Path(__file__).with_name("local_controls.json"))
    parser.add_argument("--output", type=Path, default=root / "UNITY/Assets/_Project/World/TerrainInspection/LowmarkTerrain.bytes")
    args = parser.parse_args()
    if not args.output.resolve().is_relative_to(root): raise ValueError("Keep inspection assets in the designated checkout.")
    controls = json.loads(args.controls.read_text(encoding="utf-8-sig"))
    local = json.loads(args.local_controls.read_text(encoding="utf-8-sig"))
    metrics = json.loads((args.locals / "local_metrics.json").read_text())
    if metrics["composite_sink_count"] or any(p["interior_sink_count"] for p in metrics["patches"]):
        raise ValueError("Only verified local terrain may be baked for inspection.")
    grids = []
    with np.load(args.regional, allow_pickle=False) as source:
        regional = np.load(args.locals / "composite_regional_height.npy", allow_pickle=False)
        grids.append(dict(id="regional", x=source["x"], y=source["y"], height=regional,
                          road=np.zeros(regional.shape, dtype=np.uint8), exclusions=[patch["bounds_m"] for patch in local["patches"]]))
    plots = json.loads((args.locals / "candidate_plots.json").read_text())
    for specification in local["patches"]:
        with np.load(args.locals / (specification["id"] + ".npz"), allow_pickle=False) as saved:
            grids.append(dict(id=specification["id"], x=saved["x"], y=saved["y"], height=saved["height"],
                              road=saved["road_mask"].astype(np.uint8), exclusions=[]))
    def sample(x, y):
        for grid in grids[::-1]:
            if grid["x"][0] <= x <= grid["x"][-1] and grid["y"][0] <= y <= grid["y"][-1]:
                xx, yy = grid["x"], grid["y"]
                col = min(int((x - xx[0]) / (xx[1] - xx[0])), len(xx) - 2)
                row = min(int((y - yy[0]) / (yy[1] - yy[0])), len(yy) - 2)
                u, v = (x - xx[col]) / (xx[1] - xx[0]), (y - yy[row]) / (yy[1] - yy[0])
                a,b,c,d=grid["height"][row,col],grid["height"][row,col+1],grid["height"][row+1,col],grid["height"][row+1,col+1]
                return float(a+(b-a)*u+(d-b)*v if v<=u else a+(d-c)*u+(c-a)*v)
        raise ValueError("Point outside terrain.")
    spawns = []
    approach = next(camera for camera in local["inspection"]["cameras"] if camera["id"] == "crestbridge_ground_approach")
    spawns.append(("Crestbridge approach", *approach["position_xy_m"], *approach["target_xy_m"]))
    for site_id in ("greyharrow", "reedmere", "drowsebank_mill"):
        site = next(site for site in controls["settlements"] if site["id"] == site_id)
        center = np.asarray(site["xy"]) * [controls["world"]["width_m"], controls["world"]["height_m"]]
        candidates = [plot for group in plots.values() for plot in group if plot["settlement"] == site_id
                      and plot.get("normal_stage_status") in ("graded_foundation_test", "bounded_foundation_candidate", "conditional_stilts")]
        point = min(candidates, key=lambda plot: np.linalg.norm(np.asarray(plot["xy_m"]) - center))["xy_m"] if candidates else center
        spawns.append((site.get("name", site_id), *point, float(center[0]), float(center[1] + 20)))
    labels = [(anchor["id"].replace("_", " "), *anchor["xy_m"]) for anchor in local["inspection"]["anchors"]]
    for site in controls["settlements"]:
        point = np.asarray(site["xy"]) * [controls["world"]["width_m"], controls["world"]["height_m"]]
        labels.append((site.get("name", site["id"]), *point))
    bridges = [proxy for proxy in local["inspection"]["proxies"] if proxy["type"] == "bridge_deck"]
    nodes = {node["id"]: node for node in controls["hydrology"]["nodes"]}
    strips = []
    for reach in controls["hydrology"]["reaches"]:
        points = np.asarray(reach["points"]) * [controls["world"]["width_m"], controls["world"]["height_m"]]
        samples, stations, breaks = terrain.polyline_samples(points, 4)
        ps, pz = terrain.reach_profile(reach, nodes, breaks[-1])
        stage = np.interp(stations, ps, pz) + reach.get("water_depth_m", 1.2)
        strips.append((reach["id"], samples, stage, reach.get("half_width_m", 4)))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("wb") as output:
        output.write(b"CLTRN001")
        text(output, metrics["composite_sha256"])
        output.write(struct.pack("<i", len(grids)))
        for grid in grids:
            text(output, grid["id"])
            output.write(struct.pack("<iifff", len(grid["x"]), len(grid["y"]), grid["x"][0], grid["y"][0], grid["x"][1] - grid["x"][0]))
            output.write(grid["height"].astype("<f4").tobytes())
            output.write(grid["road"].tobytes())
            output.write(struct.pack("<i", len(grid["exclusions"])))
            for rectangle in grid["exclusions"]: output.write(struct.pack("<4f", *rectangle))
        output.write(struct.pack("<i", len(strips)))
        for name, samples, stage, width in strips:
            text(output, name); output.write(struct.pack("<if", len(samples), width))
            for point, level in zip(samples, stage): output.write(struct.pack("<3f", point[0], point[1], level))
        output.write(struct.pack("<i", len(spawns)))
        for name, x, y, tx, ty in spawns:
            text(output, name); output.write(struct.pack("<4f", x, y, tx, ty))
        output.write(struct.pack("<i", len(labels)))
        for name, x, y in labels:
            text(output, name); output.write(struct.pack("<2f", x, y))
        output.write(struct.pack("<i", len(bridges)))
        for bridge in bridges:
            text(output, bridge["id"])
            output.write(struct.pack("<7f", *bridge["endpoints_xy_m"][0], *bridge["endpoints_xy_m"][1], bridge["width_m"], bridge["deck_top_m"], bridge["deck_thickness_m"]))
    summary = {"payload_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(), "payload_bytes": args.output.stat().st_size,
               "composite_source_sha256": metrics["composite_sha256"], "grids": [{"id":g["id"],"shape":list(g["height"].shape)} for g in grids],
               "spawn_points": [{"name":name,"east_m":x,"north_m":y,"ground_m":sample(x,y)} for name,x,y,_,_ in spawns],
               "bridge_approaches": [{"id":bridge["id"],"terrain_end_heights_m":[sample(*point) for point in bridge["endpoints_xy_m"]],
                                     "deck_top_m":bridge["deck_top_m"],"status":"No ramps generated; measured step gaps remain explicit."} for bridge in bridges],
               "basis": "Unity east X / elevation Y / north Z; arrays are baked, not regenerated during walking.",
               "water": "Source-profile strips at existing stages; inspection cue, no hydraulic simulation or collision.",
               "rights": "Caelmor project-generated terrain and Creative Director-authored control geometry; no third-party landscape assets."}
    args.output.with_suffix(".json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__": main()
