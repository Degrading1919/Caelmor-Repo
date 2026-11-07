"""Review persisted local terrain and plot its actual capacity/access surfaces."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, Normalize, ListedColormap
from matplotlib.patches import Ellipse
import numpy as np

import terrain
from build_prototype import source_digest
from local_refinement import stage_geometry, sample_local
from tests.test_hydrology_review import independent_d8, review_routing
from tests.test_local_review import review_local_drainage, review_seam, review_overlap
from visualize_terrain import GROUND

ROOT=Path(__file__).resolve().parents[3]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--local",type=Path,required=True)
    p.add_argument("--controls",type=Path,required=True)
    a=p.parse_args()
    local=json.loads(a.controls.read_text(encoding="utf-8-sig"))
    controls=json.loads((ROOT/local["regional_controls"]).read_text(encoding="utf-8-sig"))
    sources=local["source_refs"]+[local["inspection"]["reedmere_floor_test_source"]]
    for source in sources:
        if source_digest(ROOT/source["path"],source["hash_mode"])!=source["sha256"]:
            raise AssertionError("Local source changed without review: "+source["path"])
    with np.load(ROOT/local["regional_source"],allow_pickle=False) as parent:
        regional={name:parent[name] for name in ("x","y","height_engineered")}
    composite=np.load(a.local/"composite_regional_height.npy",allow_pickle=False)
    metrics=json.loads((a.local/"local_metrics.json").read_text(encoding="utf-8"))
    plots=json.loads((a.local/"candidate_plots.json").read_text(encoding="utf-8"))
    receiver,accumulation=independent_d8(composite,8,metrics["regional_outlet_cell"])
    global_review=review_routing(composite,receiver,accumulation,8,[metrics["regional_outlet_cell"]])
    patches={}; reviews=[]
    for spec in local["patches"]:
        with np.load(a.local/(spec["id"]+".npz"),allow_pickle=False) as data:
            patch=SimpleNamespace(**{name:data[name] for name in data.files})
        review_seam(patch,regional["height_engineered"],regional["x"],regional["y"])
        review=review_local_drainage(patch)
        review.update(id=spec["id"],height_sha256=hashlib.sha256(patch.height.astype("<f8").tobytes()).hexdigest(),
                      npz_bytes=(a.local/(spec["id"]+".npz")).stat().st_size)
        expected=next(item["height_sha256"] for item in metrics["patches"] if item["id"]==spec["id"])
        if review["height_sha256"]!=expected: raise AssertionError("Saved height does not match its generated evidence")
        patches[spec["id"]]=patch; reviews.append(review)
    values=list(patches.values())
    for i,first in enumerate(values):
        for second in values[i+1:]: review_overlap(first,second)
    def at(point):
        for patch in values:
            if patch.x[0]<=point[0]<=patch.x[-1] and patch.y[0]<=point[1]<=patch.y[-1]:
                return float(sample_local(patch.height,patch.x,patch.y,np.asarray([point]))[0])
        raise AssertionError("Inspection anchor not covered by refined terrain")
    anchors={item["id"]:{**item,"ground_m":at(item["xy_m"])} for item in local["inspection"]["anchors"]}
    floor_tests=[]
    for point in local["inspection"].get("reedmere_floor_test_xy_m",[]):
        patch=patches["reedmere"]
        corners=np.array([[point[0]+dx,point[1]+dy] for dx in (-5,5) for dy in (-4,4)])
        _,reference,_=stage_geometry(controls,corners[:,0],corners[:,1],np.array([at(q) for q in corners]))
        stage=float(reference.max())
        top=stage+1.5+.3
        floor_tests.append({"xy_m":point,"normal_reference_m":stage,"floor_m":top,
                            "corner_support_range_m":[top-max(at(q) for q in corners),top-min(at(q) for q in corners)],
                            "status":"Conditional static stage/floor test; no pile bearing or connected safe route proven."})
    report={"verified_on":"2026-11-07","baseline_main":"3ec4003","source_fingerprints_checked":len(sources),
            "saved_composite_independent_review":global_review,"saved_patch_reviews":reviews,
            "seams":"Every owned outer-border sample equals the parent edge in the same global coordinates; three disjoint owners; Crestbridge/Mill share one surface.",
            "surface_contract":"Explicit SWNE triangles at two metres; parent adaptive triangulation preserves coarse drainage before bounded edits.",
            "anchors":anchors,"reedmere_floor_tests":floor_tests,
            "capacity_scope":"Postprojection complete-footprint tests, not generated buildings or guaranteed final count. Different lattice/resolution from the regional screen; counts are not a controlled terrain-improvement comparison.",
            "scope":"Saved arrays independently reviewed. Render/mesh evidence is produced separately. No Unity or player validation claimed."}
    (a.local/"local_verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"figure.facecolor":"#f5f3ec"})
    fig,axes=plt.subplots(2,2,figsize=(15,13),constrained_layout=True)
    summaries={}
    for patch_metric in metrics["patches"]:
        summaries.update(patch_metric["plot_summary"])
    for ax,site_id in zip(axes.ravel(),("crestbridge","greyharrow","reedmere","drowsebank_mill")):
        site=next(item for item in controls["settlements"] if item["id"]==site_id)
        patch_id=next(item["id"] for item in local["patches"] if site_id in item["settlement_ids"])
        patch=patches[patch_id]
        extent=[patch.x[0],patch.x[-1],patch.y[0],patch.y[-1]]
        rgb=LightSource(315,35).shade(patch.height,cmap=GROUND,norm=Normalize(57.6,230.6),dx=2,dy=2,blend_mode="soft")
        ax.imshow(rgb,origin="lower",extent=extent)
        xx,yy=np.meshgrid(patch.x,patch.y)
        _,reference,_=stage_geometry(controls,xx,yy,patch.height)
        exposure=terrain.connected_stage_screen(patch.height,reference,patch.water_level,1.5)
        if exposure.any():
            hatches=ax.contourf(patch.x,patch.y,exposure.astype(float),levels=[.5,1.5],colors="none",hatches=["///"])
            hatches.set_edgecolor("#64889b"); hatches.set_linewidth(0)
        wet=np.isfinite(patch.water_level)
        ax.imshow(np.ma.masked_where(~wet,wet),origin="lower",extent=extent,cmap=ListedColormap(["#378cad"]),alpha=.8)
        ax.contour(patch.x,patch.y,patch.height,levels=np.arange(np.floor(patch.height.min()),np.ceil(patch.height.max())+1),colors="#625b42",linewidths=.4,alpha=.55)
        for route in controls["routes"]:
            if route["id"] not in next(item["route_ids"] for item in local["patches"] if item["id"]==patch_id): continue
            points=np.asarray(route["points"])*[controls["world"]["width_m"],controls["world"]["height_m"]]
            ax.plot(*points.T,ls=":",lw=1.1,color="#8c4f28")
        for plot in plots[patch_id]:
            if plot["settlement"]!=site_id: continue
            status=plot["status"]
            color="#713a9a" if status=="conditional_stilts" else "#d27824" if status=="flood_adaptation_required" else "#23834c" if status in ("graded_foundation_test","bounded_foundation_candidate") else "#696960"
            marker="s" if plot["foundation_applied"] else "+"
            ax.scatter(*plot["xy_m"],c=color,s=16,marker=marker,lw=.8,zorder=8)
        centre=np.asarray(site["xy"])*[controls["world"]["width_m"],controls["world"]["height_m"]]
        ax.add_patch(Ellipse(centre,*site["envelope_axes_m"],fc="none",ec="white",lw=1.5))
        radius=max(site["envelope_axes_m"])*.78
        summary=summaries[site_id]
        ax.set(xlim=(max(patch.x[0],centre[0]-radius),min(patch.x[-1],centre[0]+radius)),
               ylim=(max(patch.y[0],centre[1]-radius),min(patch.y[-1],centre[1]+radius)),aspect="equal",
               title=f"{site_id.replace('_',' ').title()} | normal {summary['normal_candidates']} / conditional stilts {summary['conditional_stilts']}\n"
                     f"Scenario floor screen {summary['scenario_floor_candidates']} | proposed roofs {site['buildings'][0]}–{site['buildings'][1]}",
               xlabel="East (m)",ylabel="North (m)")
    fig.suptitle("ACTUAL 2 m LOCAL TERRAIN / POSTPROJECTION FOOTPRINT SCREEN\nGreen: candidate floors; purple: conditional stilts; orange: flood adaptation; grey: review; squares: tested grading\nWhite: settlement envelope; dotted brown: retained access; blue hatch: connected +1.5m stage screen, not flood forecast",fontsize=12)
    fig.savefig(a.local/"local_capacity.png",dpi=150);plt.close(fig)
    # Direct surface transects expose the unapproved remote-civic relationship.
    fig,axes=plt.subplots(2,1,figsize=(13,7),constrained_layout=True)
    pairs=[("bridge_crossing","crest_hall"),("crest_hall","hill_depot")]
    for ax,(first,second) in zip(axes,pairs):
        start,end=np.array(anchors[first]["xy_m"]),np.array(anchors[second]["xy_m"])
        length=float(np.linalg.norm(end-start)); station=np.linspace(0,length,int(length)+1)
        points=start+(end-start)*(station/length)[:,None]
        heights=np.array([at(point) for point in points])
        ax.plot(station,heights,color="#5b6f3c",lw=2)
        ax.fill_between(station,heights,55,color="#c8d1b1",alpha=.6)
        ax.set(title=f"{first.replace('_',' ')} → {second.replace('_',' ')} / {length:.1f} m straight diagnostic",xlabel="Straight horizontal distance (m)",ylabel="True elevation (m)",ylim=(60,74))
        ax.grid(alpha=.2)
    fig.suptitle("CIVIC TERRAIN SECTIONS / NO VERTICAL EXAGGERATION IN THE 3D RENDERS\nThese straight diagnostics are not proposed tunnels, roads or an invented water-gate connection.",fontsize=12)
    fig.savefig(a.local/"crestbridge_sections.png",dpi=150);plt.close(fig)
    print("CAELMOR_SAVED_LOCAL_TERRAIN_VERIFIED "+json.dumps({"patches":len(reviews),"samples":sum(i["owned_samples"] for i in reviews),"sources":len(sources)}))


if __name__=="__main__": main()
