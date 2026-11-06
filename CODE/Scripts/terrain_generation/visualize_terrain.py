"""Inspectable scientific figures for the offline Lowmark terrain prototype."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, ListedColormap, LogNorm, LinearSegmentedColormap
from matplotlib.patches import Ellipse, Patch
import numpy as np
from PIL import Image

import terrain

REPOSITORY = Path(__file__).resolve().parents[3]
COLORS = {"natural": "#147eac", "engineered": "#d07b20", "anomalous_engineered": "#ad3258", "backwater": "#7764a0"}
GROUND = LinearSegmentedColormap.from_list("ground_only", ["#c5d69e", "#aebd86", "#c9b788", "#b7987c", "#e0d4bf", "#f4f0e8"])


def xy(points, controls):
    return np.asarray(points) * [controls["world"]["width_m"], controls["world"]["height_m"]]


def save(fig, output, name):
    fig.savefig(output / f"{name}.png", dpi=165, facecolor=fig.get_facecolor())
    plt.close(fig)


def setup(ax, controls, title):
    ax.set(xlim=(0, controls["world"]["width_m"]), ylim=(0, controls["world"]["height_m"]),
           xlabel="East from map origin (m)", ylabel="North (m)", title=title, aspect="equal")
    ax.tick_params(labelsize=8)


def background(ax, result, controls, engineered=False):
    z = result.height_engineered if engineered else result.height
    step = result.x[1] - result.x[0]
    rgb = LightSource(315, 40).shade(z, cmap=GROUND, vert_exag=1,
                                      dx=step, dy=step, blend_mode="soft")
    extent = [0, result.x[-1], 0, result.y[-1]]
    ax.imshow(rgb, origin="lower", extent=extent)
    ax.contour(result.x, result.y, z, levels=np.arange(60, 261, 20), colors="#536550", linewidths=.35, alpha=.55)
    # A fen stage is not proof of submergence: only show water where terrain is below it.
    wet = np.isfinite(result.water_level) & (z <= result.water_level)
    ax.imshow(np.ma.masked_where(~wet, wet), origin="lower", extent=extent,
              cmap=ListedColormap(["#76b9d1"]), alpha=.65, interpolation="nearest")


def reaches(ax, controls, labels=False):
    for reach in controls["hydrology"]["reaches"]:
        pts = xy(reach["points"], controls)
        kind = reach.get("kind", "natural")
        color = COLORS.get(kind, COLORS["engineered"])
        ax.plot(pts[:, 0], pts[:, 1], color=color, lw=1.6 if kind == "natural" else 1.35,
                ls="--" if kind in ("anomalous_engineered", "backwater") else "-", zorder=5)
        if labels and kind != "natural":
            mid = pts[len(pts)//2]
            ax.annotate(reach["id"].replace("_", " "), mid, fontsize=6, color=color)


def settlements(ax, controls, envelopes=False, labels=True):
    for item in controls["settlements"]:
        point = xy(item["xy"], controls)
        ax.scatter(*point, s=22, c="white", edgecolors="#202c32", zorder=10)
        if envelopes:
            axes = item["envelope_axes_m"]
            ax.add_patch(Ellipse(point, *axes, facecolor="none", edgecolor="#f5f6ef", lw=1.2, zorder=9))
        if labels:
            ax.annotate(item["id"].replace("_", " "), point, xytext=(5, 5), textcoords="offset points", fontsize=7,
                        bbox=dict(fc="white", ec="none", alpha=.72, pad=1), zorder=11)


def landmarks(ax, controls):
    for item in controls.get("landmark_anchors",[]):
        point=xy(item["xy"],controls)
        ax.scatter(*point,s=18,c="#30352b",marker="+",zorder=12)
        ax.annotate(item["id"].replace("_"," "),point,xytext=(4,4),textcoords="offset points",fontsize=6,
                    bbox=dict(fc="white",ec="none",alpha=.65,pad=.7),zorder=12)


def comparison(result, controls, output):
    fig, axes = plt.subplots(1, 2, figsize=(17, 8.2), constrained_layout=True)
    source = Image.open(REPOSITORY / "MEDIA/Maps/Lowmark_Planning_Map.png")
    crop = controls["map_frame"]["topographical_crop_px"]
    source = source.crop((crop["x0"], crop["y0"], crop["x1"], crop["y1"]))
    axes[0].imshow(source, extent=[0, result.x[-1], 0, result.y[-1]], origin="upper")
    setup(axes[0], controls, "Approved composition / traced anchors\nIllustrated heights and scale are NOT terrain measurements")
    settlements(axes[0], controls, True, False)
    background(axes[1], result, controls)
    reaches(axes[1], controls)
    settlements(axes[1], controls, True)
    landmarks(axes[1], controls)
    setup(axes[1], controls, "Constrained terrain / same horizontal frame\n8 m regional DEM; elevations are a technical scenario")
    fig.suptitle("LOWMARK VALE  |  Map composition preserved; vertical model independently constructed", fontsize=15, fontweight="bold")
    save(fig, output, "composition_comparison")


def hydrology(result, controls, output):
    fig, axes = plt.subplots(1, 2, figsize=(17, 8.3), constrained_layout=True)
    background(axes[0], result, controls)
    reaches(axes[0], controls)
    settlements(axes[0], controls, False)
    for route in controls.get("routes", []):
        p = xy(route["points"], controls)
        axes[0].plot(*p.T, color="#71583d", ls=":", lw=.9, alpha=.8)
    setup(axes[0], controls, "Authored water network and water-covered terrain\nBlue natural / orange controlled / magenta anomalous / purple unresolved arm")
    field = np.ma.masked_where(result.accumulation < 12, result.accumulation)
    axes[1].imshow(terrain.slope_degrees(result.height, result.x[1]-result.x[0]), origin="lower",
                   extent=[0, result.x[-1], 0, result.y[-1]], cmap="Greys", vmin=0, vmax=15, alpha=.35)
    image = axes[1].imshow(field, origin="lower", extent=[0, result.x[-1], 0, result.y[-1]],
                           cmap="viridis", norm=LogNorm(12, result.height.size))
    reaches(axes[1], controls)
    setup(axes[1], controls, "Independently tested steepest-descent D8 accumulation\nBaseline gated terrain; sample count, not discharge or flood probability")
    fig.colorbar(image, ax=axes[1], shrink=.7, label="Upslope contributing grid samples (log)")
    fig.suptitle("DRAINAGE AND CONTROLLED WATER  |  Stream profiles are constraints; raster routing is tested separately", fontsize=14)
    save(fig, output, "hydrology_and_routing")


def profiles(result, controls, output):
    fig, axes = plt.subplots(3, 1, figsize=(14, 11), constrained_layout=True)
    nodes = {n["id"]: n for n in controls["hydrology"]["nodes"]}
    main = [r for r in controls["hydrology"]["reaches"] if r.get("kind", "natural") == "natural" and not any(s in r["id"] for s in ("braid", "greyharrow"))]
    # Connected stationing follows the declared main chain, not dictionary order.
    outgoing = {}
    for reach in main:
        outgoing.setdefault(reach["from"], []).append(reach)
    current = next(n["id"] for n in controls["hydrology"]["nodes"] if n["id"] == "headwaters") if "headwaters" in nodes else main[0]["from"]
    station = 0
    visited = set()
    while current in outgoing:
        reach = outgoing[current][0]
        if reach["id"] in visited: break
        visited.add(reach["id"])
        points = xy(reach["points"], controls)
        length = float(np.linalg.norm(np.diff(points, axis=0), axis=1).sum())
        s, z = terrain.reach_profile(reach, nodes, length)
        axes[0].plot(station+s, z, color="#556756", lw=1.7)
        axes[0].plot(station+s, z+reach.get("water_depth_m", 1.2), color=COLORS["natural"], lw=2)
        axes[0].annotate(reach["to"].replace("_", " "), (station+length, z[-1]), xytext=(0, 7),
                         textcoords="offset points", fontsize=7, rotation=25)
        station += length; current = reach["to"]
    axes[0].set(title="Natural main-stem bed and reference water surface (fall is a localized 83.6 m transition)", xlabel="Downstream station (m)", ylabel="Provisional elevation (m)")
    for axis, selector, title in ((axes[1], lambda r: r.get("kind") == "engineered" and any(k in r["id"] for k in ("hollow", "relief_cut")), "Hollow Lock / Relief Cut: engineered head and invert controls"),
                                  (axes[2], lambda r: "uphill" in r["id"], "Uphill Canal: rising authored bed; +18.1 m lift is NOT passive gravity flow")):
        station = 0
        for reach in controls["hydrology"]["reaches"]:
            if not selector(reach): continue
            points = xy(reach["points"], controls)
            length = float(np.linalg.norm(np.diff(points, axis=0), axis=1).sum())
            s, z = terrain.reach_profile(reach, nodes, length)
            color = COLORS.get(reach.get("kind"), COLORS["engineered"])
            axis.plot(station+s, z, c="#6a6559", lw=1)
            source = reach.get("upstream_level_m", nodes[reach["from"]].get("water_level_m", z[0]))
            tail = reach.get("downstream_level_m", nodes[reach["to"]].get("water_level_m", z[-1]))
            axis.plot([station, station+length], [source, tail], color=color, lw=2, ls="--" if reach.get("kind") == "anomalous_engineered" else "-")
            axis.annotate(reach["id"].replace("_", " "), (station+length/2, (source+tail)/2), xytext=(0, 10),
                          textcoords="offset points", fontsize=7, rotation=12)
            station += length
        axis.set(title=title, xlabel="Sequential reach station (m); branch ordering is schematic", ylabel="Provisional elevation (m)")
    for ax in axes: ax.grid(alpha=.22)
    save(fig, output, "water_profiles")


def capacity(result, controls, output):
    fig, axes = plt.subplots(2, 4, figsize=(20, 11), constrained_layout=True)
    reports = {r["id"]: r for r in result.metrics["settlements"]}
    for ax, item in zip(axes.ravel(), controls["settlements"]):
        background(ax, result, controls, engineered=True)
        point = xy(item["xy"], controls)
        radius = item["working_radius_m"]
        masks = result.settlement_masks[item["id"]]
        overlay = np.zeros((*result.height.shape, 4))
        overlay[masks["working"]] = [.85, .7, .32, .18]
        overlay[masks["envelope"]] = [.1, .3, .45, .12]
        overlay[masks["candidate"]] = [.12, .66, .38, .58]
        overlay[masks["adaptation"]] = [.85, .35, .2, .3]
        ax.imshow(overlay, extent=[0, result.x[-1], 0, result.y[-1]], origin="lower", interpolation="nearest")
        exposed=masks.get("scenario_exposed")
        if exposed is not None and exposed.any():
            hatch=ax.contourf(result.x,result.y,exposed.astype(float),levels=[.5,1.5],colors="none",hatches=["///"])
            hatch.set_edgecolor("#467a9e"); hatch.set_linewidth(0)
        slope_lines=ax.contour(result.x,result.y,masks["slope_deg"],levels=[3,5,10,20],colors="#70533d",linewidths=.45,alpha=.8)
        ax.clabel(slope_lines,inline=True,fontsize=5,fmt=lambda value:f"{value:g}°")
        reaches(ax, controls)
        ax.add_patch(Ellipse(point, *item["envelope_axes_m"], fc="none", ec="white", lw=1.5))
        sites = np.asarray(result.plot_sites[item["id"]])
        if sites.size:
            ax.scatter(sites[:,0], sites[:,1], s=8, c="#133b24", marker="+", lw=.8)
        for route in controls.get("routes", []):
            p = xy(route["points"], controls); ax.plot(*p.T, color="#513e30", ls=":", lw=1.3)
        report = reports[item["id"]]
        ax.set(xlim=(max(0,point[0]-radius), min(result.x[-1],point[0]+radius)),
               ylim=(max(0,point[1]-radius),min(result.y[-1],point[1]+radius)), aspect="equal",
               title=f"{item['id'].replace('_',' ').title()}\nNormal {report['screened_roof_capacity']} / +1.5m {report['flood_scenario_safe_capacity']} | proposed {item['buildings'][0]}–{item['buildings'][1]}")
        ax.tick_params(labelsize=7)
    ax=axes.ravel()[-1]; ax.axis("off")
    ax.text(.03,.96,"CAPACITY SCREEN, NOT A BUILDING PLAN\n\nGreen: normal-stage candidate ground\nWhite ellipse: circulation / public envelope\nAmber: surrounding working landscape\nRust: slope / exposure / works constraint\nBlue hatch: connected +1.5m stage exposure\nBrown lines/numbers: ground slope in degrees\nBrown dots: access corridors\nCrosses: spaced terrain-fit centers; no buildings\n\nAll counts and spans are proposed targets.\nNo town-wide flattening or NPC population.\nExposure is a static planning scenario,\nnot a calibrated flood/return-period forecast.\n\n8 m grid is a conservative regional screen;\nlocal foundations and grading need refinement.", transform=ax.transAxes, va="top", fontsize=10, linespacing=1.45)
    fig.suptitle("SETTLEMENT CAPACITY  |  Building land, circulation and working landscape remain distinct", fontsize=16)
    save(fig, output, "settlement_capacity")


def perspective(result, controls, output):
    fig=plt.figure(figsize=(15,10), constrained_layout=True); ax=fig.add_subplot(projection="3d")
    step=4; xx,yy=np.meshgrid(result.x[::step],result.y[::step]); z=result.height_engineered[::step,::step]
    face=GROUND((z-result.height.min())/(result.height.max()-result.height.min()))
    ax.plot_surface(xx,yy,z,facecolors=face,rstride=1,cstride=1,linewidth=0,antialiased=False,shade=True)
    ax.set(xlabel="East (m)",ylabel="North (m)",zlabel="Elevation (m)",title="Lowmark mathematical terrain — 32 m display sampling, authoritative grid 8 m\nVertical display exaggeration ×6 for inspection; heights are provisional, not map-derived")
    ax.set_box_aspect((result.x[-1],result.y[-1],6*(result.height.max()-result.height.min())))
    ax.view_init(elev=33,azim=-128)
    save(fig,output,"terrain_perspective")


def watershed_figure(result,controls,output):
    if not hasattr(result,"watershed_labels"): return
    fig,axes=plt.subplots(1,2,figsize=(17,8),constrained_layout=True)
    background(axes[0],result,controls)
    basin_colors=plt.get_cmap("Set2",len(result.watershed_names))
    axes[0].imshow(result.watershed_labels,origin="lower",extent=[0,result.x[-1],0,result.y[-1]],
                   cmap=basin_colors,alpha=.55,vmin=0,vmax=max(1,len(result.watershed_names)-1))
    axes[0].legend(handles=[Patch(facecolor=basin_colors(i),label=name.replace("_"," "),alpha=.55)
                           for i,name in enumerate(result.watershed_names)],loc="lower left",fontsize=7)
    reaches(axes[0],controls); settlements(axes[0],controls,False)
    setup(axes[0],controls,"Model-derived subcatchments / first downstream gauge\n"+", ".join(result.watershed_names))
    slopes=terrain.slope_degrees(result.height_engineered,result.x[1]-result.x[0])
    image=axes[1].imshow(slopes,origin="lower",extent=[0,result.x[-1],0,result.y[-1]],cmap="YlOrBr",vmin=0,vmax=15)
    reaches(axes[1],controls); settlements(axes[1],controls,True)
    setup(axes[1],controls,"Actual open-terrain slope / values over15° saturated\nNo automatic road, foundation or buildability claim")
    fig.colorbar(image,ax=axes[1],shrink=.72,label="Ground slope (degrees)")
    fig.suptitle("WATERSHEDS AND SLOPES  |  Derived from the verified DEM, not illustrated contours",fontsize=15)
    save(fig,output,"watersheds_and_slopes")


def floodplain_figure(result, controls, output):
    if not result.floodplain_masks: return
    fig, axes = plt.subplots(1, 2, figsize=(14, 7), constrained_layout=True)
    for name, data in result.floodplain_masks.items():
        rows, cols = np.where(data["mask"])
        bounds = (result.x[cols.min()]-160, result.x[cols.max()]+160,
                  result.y[rows.min()]-160, result.y[rows.max()]+160)
        for ax, flooded, title in zip(axes, (data["normal_water"], data["scenario_exposed"]),
                                     ("Normal connected water", "Connected +1.5 m stage scenario")):
            background(ax, result, controls, engineered=True)
            ax.contour(result.x, result.y, data["mask"], levels=[.5], colors="#657a35", linewidths=1.5)
            ax.contour(result.x, result.y, data["berm"], levels=[.5], colors="#b17d30", linewidths=.7)
            ax.imshow(np.ma.masked_where(~flooded, flooded), origin="lower",
                      extent=[0,result.x[-1],0,result.y[-1]], cmap=ListedColormap(["#3f95c7"]), alpha=.8)
            reaches(ax, controls)
            ax.set(xlim=bounds[:2], ylim=bounds[2:], aspect="equal", title=title,
                   xlabel="East (m)", ylabel="North (m)")
    fig.suptitle("ORCHARD FLOODPLAIN  |  Green boundary / amber proposed berms / blue connected water\n"
                 "Terrain-fit scenario, not a flood-frequency forecast; no trees or field parcels generated", fontsize=13)
    save(fig, output, "orchard_floodplain")


def render(result, controls, output):
    output=Path(output); output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"axes.titlesize":11,"figure.facecolor":"#f7f5ed","axes.facecolor":"#f7f5ed"})
    comparison(result,controls,output); hydrology(result,controls,output); profiles(result,controls,output)
    capacity(result,controls,output); perspective(result,controls,output); watershed_figure(result,controls,output)
    floodplain_figure(result,controls,output)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--controls",type=Path,default=Path(__file__).with_name("lowmark_controls.json"))
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args(); controls=json.loads(args.controls.read_text(encoding="utf-8-sig"))
    result=terrain.generate(controls,8); terrain.export(result,args.output); render(result,controls,args.output)


if __name__=="__main__": main()
