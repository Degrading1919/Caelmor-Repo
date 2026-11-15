"""Build the true-scale Lowmark blockout planning map (SVG primary, PNG export).

Reads only existing project sources:
  - lowmark_controls.json            (approved-map anchors, waterways, routes, envelopes)
  - MEDIA/Maps/Lowmark_Terrain/*      (height_engineered.npy, verification.json,
                                       candidate_plots.json, Local_Refinement/candidate_plots.json)
and writes the master sheet and its sector references under MEDIA/Maps/Lowmark_Blockout.

Coordinates: SVG user unit = 1 metre. World point (x east, y north) is drawn at
SVG (x, -y), so the world origin (south-west map corner) is SVG (0, 0) and the
map frame dimensions follow the regional controls. Nothing here creates canon or moves an
anchor; every placement and status is taken from, or cited to, a repo source.

Usage (from the checkout root):
  python CODE/Scripts/terrain_generation/build_blockout_planning_map.py [--png-scale 0.5 | --sectors-only]
Requires numpy, matplotlib (contour extraction) and resvg-py (PNG export).
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import math
from html import escape
from pathlib import Path

import numpy as np
from blockout_sectors import export_sectors

ROOT = Path(__file__).resolve().parents[3]
CONTROLS = ROOT / "CODE/Scripts/terrain_generation/lowmark_controls.json"
TERRAIN = ROOT / "MEDIA/Maps/Lowmark_Terrain"
OUT = ROOT / "MEDIA/Maps/Lowmark_Blockout"
STEM = "Lowmark_Blockout_Planning_Map"

WORLD = json.loads(CONTROLS.read_text(encoding="utf-8"))["world"]
W, H = WORLD["width_m"], WORLD["height_m"]
SECTOR, CELL = 384, 192
if W % SECTOR or H % SECTOR:
    raise ValueError("Blockout dimensions must align to complete sectors.")
COLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:W // SECTOR]
ROWS = H // SECTOR

# Layout of the sheet around the map frame (SVG units = metres).
ML, MT, MR = 520, 760, 260
PANEL_W = 3500
BOTTOM = 3500
VB_X, VB_Y = -ML, -(H + MT)
VB_W = ML + W + MR + PANEL_W + 160
VB_H = MT + H + BOTTOM

C_OK, C_PROV, C_BLOCK = "#1b1b1b", "#b86e00", "#c62828"
C_WATER, C_ENG, C_ANOM = "#3a86c8", "#1d4f91", "#7b3fa0"
FONT = "DejaVu Sans, Arial, Helvetica, sans-serif"

# Planning-map pixel -> normalized frame (lowmark_controls.json map_frame.pixel_to_normalized)
def px_to_m(px, py):
    return ((px - 6) / 1096 * W, (898 - py) / 892 * H)


def P(x, y):
    """World metres -> SVG coordinates."""
    return x, -y


def fmt(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def pts(points):
    return " ".join(f"{fmt(x)},{fmt(-y)}" for x, y in points)


class Svg:
    def __init__(self):
        self.parts: list[str] = []

    def add(self, s: str):
        self.parts.append(s)

    def layer(self, ident, label, hidden=False):
        style = ' style="display:none"' if hidden else ""
        self.add(f'<g id="{ident}" inkscape:groupmode="layer" inkscape:label="{escape(label)}"{style}>')

    def end(self):
        self.add("</g>")

    def text(self, x, y, s, size=60, anchor="start", weight="normal", fill=C_OK, italic=False,
             halo=True, ident=None, extra=""):
        """x, y are SVG coordinates (already flipped)."""
        style = "font-style:italic;" if italic else ""
        idattr = f' id="{ident}"' if ident else ""
        common = (f'x="{fmt(x)}" y="{fmt(y)}" font-size="{fmt(size)}" text-anchor="{anchor}" '
                  f'font-weight="{weight}" font-family="{FONT}" style="{style}"{extra}')
        if halo:
            # Separate halo element: renderers without paint-order support still draw a dark label.
            self.add(f'<g><text {common} fill="none" stroke="#ffffff" stroke-width="{fmt(size * 0.24)}" '
                     f'stroke-linejoin="round" stroke-opacity="0.9">{escape(s)}</text>'
                     f'<text{idattr} {common} fill="{fill}">{escape(s)}</text></g>')
        else:
            self.add(f'<text{idattr} {common} fill="{fill}">{escape(s)}</text>')


def m(xy):
    return xy[0] * W, xy[1] * H


def rdp(points, eps):
    if len(points) < 3:
        return points
    a, b = np.array(points[0]), np.array(points[-1])
    arr = np.array(points)
    ab = b - a
    n = np.hypot(*ab)
    if n == 0:
        d = np.hypot(*(arr - a).T)
    else:
        d = np.abs(ab[0] * (arr[:, 1] - a[1]) - ab[1] * (arr[:, 0] - a[0])) / n
    i = int(np.argmax(d))
    if d[i] > eps:
        left = rdp(points[: i + 1], eps)
        right = rdp(points[i:], eps)
        return left[:-1] + right
    return [points[0], points[-1]]


def hillshade_png(h, cell=8.0):
    gy, gx = np.gradient(h.astype(np.float64), cell)  # rows north, cols east
    slope = np.arctan(np.hypot(gx, gy) * 2.0)          # 2x vertical exaggeration for legibility only
    aspect = np.arctan2(-gx, gy)
    az, alt = math.radians(315), math.radians(45)
    shade = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
    img = np.clip(shade * 255, 0, 255).astype(np.uint8)[::-1]  # north-up rows
    from PIL import Image
    buf = io.BytesIO()
    Image.fromarray(img, "L").save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


def contour_paths(h, levels):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ny, nx = h.shape
    xs = np.linspace(0, W, nx)
    ys = np.linspace(0, H, ny)
    fig = plt.figure()
    cs = plt.contour(xs, ys, h, levels=levels)
    out = {}
    for lev, segs in zip(cs.levels, cs.allsegs):
        paths = []
        for seg in segs:
            if len(seg) < 6:
                continue
            simp = rdp([tuple(p) for p in seg], 3.0)
            if len(simp) >= 2:
                paths.append("M" + " L".join(f"{fmt(x)},{fmt(-y)}" for x, y in simp))
        out[float(lev)] = paths
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# Source-derived content tables. Status: "ok" confirmed/approved, "prov" provisional,
# "block" blocked by an unresolved terrain/narrative conflict (register severity Blocks).
# ---------------------------------------------------------------------------

# Planning regions A-K: dashed outlines of the approved planning map, traced by eye in
# its pixel frame (approx. +/-10 px = +/-60 m) and converted with map_frame.pixel_to_normalized.
REGIONS = [  # key, name, outline centre px, outline radii px, letter-circle px on the source map
    ("A", "Veilwater Uplands / Headwaters", (153, 152), (115, 93), (143, 113)),
    ("B", "Stillwater Fen Complex", (310, 360), (235, 118), (330, 367)),
    ("C", "Ashenstead Reclaimed Fields", (854, 262), (166, 102), (832, 213)),
    ("D", "Crestbridge Civic Corridor", (524, 575), (164, 58), (469, 548)),
    ("F", "Orchard and Weir Floodplain", (787, 642), (92, 58), (796, 613)),
    ("G", "Whisperflow Heartlands", (590, 782), (158, 88), (584, 774)),
    ("H", "Brookhollow Trade Reach", (852, 825), (120, 55), (865, 791)),
    ("I", "Greyharrow Side Branch", (1007, 685), (90, 80), (1060, 633)),
    ("J", "Brackenford Woods / Canal Verge", (987, 546), (92, 82), (996, 505)),
    ("K", "Drowsebank Mill Waterworks", (546, 656), (76, 44), (516, 675)),
]
E_LETTER_PX = (683, 456)
# E (Relief Cut Engineering Line) is linear on the source map; drawn as the Cut alignment.

# Settlement statuses and the register rows that qualify them.
SETTLEMENT_STATUS = {
    "brookhollow": ("ok", ["TC-19"]),
    "crestbridge": ("ok", ["TC-02", "TC-04", "TC-19"]),
    "ashenstead": ("prov", ["TC-15"]),
    "greyharrow": ("prov", ["TC-19"]),
    "reedmere": ("ok", ["TC-12"]),
    "whisperflow_landing": ("prov", ["TC-13"]),
    "drowsebank_mill": ("prov", ["TC-06", "TC-07", "TC-08"]),
}
LANDMARK_STATUS = {
    "crest_hall": ("block", ["TC-01", "TC-05"], "Crest Hall"),
    "hill_depot": ("prov", ["TC-03"], "Hill Depot"),
    "whispering_door_farmhouse": ("ok", ["NC-1"], "Whispering Door Farmhouse"),
    "floodplain_orchards": ("ok", [], None),
    "brackenford_woods": ("ok", [], None),
    "mantle_shrine": ("ok", ["TC-17"], "Mantle Shrine"),
    "circle_unburnt_reeds": ("ok", [], "Circle of Unburnt Reeds"),
    "veilwater_falls": ("ok", ["TC-16"], "Veilwater Falls"),
}

# Label placement offsets (metres, world axes) and text anchor; purely presentational.
LABEL_OFFSETS = {
    "brookhollow": (70, 60, "start"), "crestbridge": (-60, 70, "end"), "ashenstead": (80, 40, "start"),
    "greyharrow": (-90, 80, "end"), "reedmere": (90, -110, "start"),
    "whisperflow_landing": (0, -155, "middle"), "drowsebank_mill": (-65, -135, "end"),
    "crest_hall": (115, 28, "start"), "hill_depot": (100, 30, "start"),
    "whispering_door_farmhouse": (80, -40, "start"), "mantle_shrine": (0, 90, "middle"),
    "circle_unburnt_reeds": (0, 95, "middle"), "veilwater_falls": (-60, 70, "end"),
}

CONFLICTS = [
    # id, severity, short text and source anchor (where spatially defined)
    ("TC-01", "block", "Compact Hall site; direct water gate, cistern and bridge north stair remain unbuilt.", "crest_hall"),
    ("TC-02", "prov", "Granary and toll-facing yard have no approved placement.", None),
    ("TC-03", "prov", "Depot remains uphill. Chute and below-toll slack-water exit need a local layout.", "hill_depot"),
    ("TC-04", "prov", "Technical route crossing only. Bridge, stairs and transitions are unbuilt.", "bridge_crossing"),
    ("TC-05", "prov", "Hall-to-mouth alignment is a straight-distance diagnostic; towpath still unbuilt.", None),
    ("TC-06", "prov", "Tail race still meets the common outfall; separate wartime spur unresolved.", None),
    ("TC-07", "prov", "Static mill head does not establish draft, pulses or reverse flow.", None),
    ("TC-08", "prov", "Working yard offset from the race. Pond, wheel and gates remain unbuilt.", "drowsebank_mill"),
    ("TC-09", "block", "Cut mouth, mill tail and Bramblelock share weir_up; no length for MQ4 chase between them.", "weir_up"),
    ("TC-10", "prov", "The straight exceeds the 60–90 second quest beat. See route measurements.", "cut_corner"),
    ("TC-11", "prov", "The natural fen outlet remains open in the static baseline.", "fen_out"),
    ("TC-12", "prov", "Reedmere requires stilts; staging, causeways and evacuation remain unbuilt.", "reedmere"),
    ("TC-13", "prov", "Provisional landing envelope reaches main-river bank; crossing and road-head view untested.", "whisperflow_landing"),
    ("TC-14", "prov", "Regional uphill line is schematic; the quest's twenty-step site is unplaced.", "uphill_canal_foot"),
    ("TC-15", "prov", "Rebirth Fields extent and seepage remain unresolved.", "ashenstead"),
    ("TC-16", "prov", "Falls approach requires local switchbacks and Listening Steps.", "veilwater_falls"),
    ("TC-17", "prov", "Local fen-edge channel at Mantle Shrine remains untraced.", "mantle_shrine"),
    ("TC-18", "prov", "See updated route measurements for pacing and unbuilt crossings.", None),
    ("TC-19", "prov", "Greyharrow upper capacity and civic outworks budget remain unresolved.", "greyharrow"),
    ("NC-1", "prov", "Whispering Door map anchor and Rebirth Fields outfall relationship need review.", "whispering_door_farmhouse"),
    ("W-ARM", "prov", "Western arm retained as terminal backwater profile pending topology ruling.", "western_arm_terminal"),
]
TAG_POS = {  # tag offset from conflict location (world m), presentational only
    "TC-01": (200, -72), "TC-02": (0, 0), "TC-03": (180, 170), "TC-04": (-370, -85), "TC-06": (40, -120),
    "TC-08": (65, 170), "TC-09": (90, 110), "TC-10": (0, 0), "TC-11": (60, 40), "TC-12": (-200, -260),
    "TC-13": (-330, -40), "TC-14": (70, 0), "TC-15": (60, -150), "TC-16": (-320, -90), "TC-17": (-60, -200),
    "TC-19": (60, -210), "NC-1": (60, -140), "W-ARM": (-560, -60),
}

UNANCHORED = [
    ("P02", "Crestbridge granaries, tally room, undercroft, waiting wall", "Crestbridge (TC-02: no approved XY)"),
    ("P02", "Crestbridge bridge, south toll, forge under first arch", "Technical crossing shown above (TC-04)"),
    ("P18", "The Drowned Lamb (tavern) and cellar", "Brookhollow envelope (waterfront)"),
    ("P25", "Greyharrow silent bell tower", "Greyharrow envelope (overlooks side branch)"),
    ("P23", "Ashenstead Watergarden and Ember-Well", "Ashenstead envelope"),
    ("--", "Rebirth Fields", "Ashenstead working landscape (TC-15: extent untraced)"),
    ("P12", "The Drowned Pier", "Whisperflow Landing, downstream of footing (TC-13)"),
    ("P17", "Renewal coppice and household woods", "Near Landing (POI 6.1); Brackenford"),
    ("P19", "Ferry Camp at Greyharrow Reach", "Greyharrow Reach (lower branch)"),
    ("P15", "The Sluice Shelter", "Orchard floodplain, near Bramblelock"),
    ("P13", "Guide-Line Culvert", "Under Rebirth Fields (TC-15)"),
    ("P14", "Furrowed Plains trench line", "Ashenstead Fields / Ashen Flats"),
    ("P20", "Goblin camp at the burned barns", "Heartlands-Ashenstead edge"),
    ("P27", "The Twice-Burned Tree", "By the goblin path near P20"),
    ("P21", "Watchers' Lantern Post", "Fen edge, start of the far leg (R4)"),
    ("P22", "Widow's Step", "Embankment overlooking Reedmere's near edge"),
    ("P30", "Stillwater Fen interior [PROPOSED POI]", "Inside fen polygon"),
    ("--", "Veilwater Oasis / Warden's Hearth (hidden)", "Behind the Falls; never on normal maps"),
]


def build(png_scale: float, sectors_only: bool = False):
    ctrl = json.loads(CONTROLS.read_text(encoding="utf-8"))
    ver = json.loads((TERRAIN / "verification.json").read_text(encoding="utf-8"))
    cand = json.loads((TERRAIN / "candidate_plots.json").read_text(encoding="utf-8"))["sites"]
    lcand = json.loads((TERRAIN / "Local_Refinement/candidate_plots.json").read_text(encoding="utf-8"))
    h = np.load(TERRAIN / "height_engineered.npy")
    assert ctrl["world"]["width_m"] == W and ctrl["world"]["height_m"] == H

    nodes = {n["id"]: m(n["xy"]) for n in ctrl["hydrology"]["nodes"]}
    settlements = {s["id"]: s for s in ctrl["settlements"]}
    landmarks = {l["id"]: m(l["xy"]) for l in ctrl["landmark_anchors"]}
    metrics = json.loads((TERRAIN / "metrics.json").read_text(encoding="utf-8"))
    local_metrics = json.loads((TERRAIN / "Local_Refinement/local_metrics.json").read_text(encoding="utf-8"))
    regional_counts = {site["id"]: site for site in metrics["settlements"]}
    local_counts = {key: value for patch in local_metrics["patches"] for key, value in patch["plot_summary"].items()}
    local_verification = json.loads((TERRAIN / "Local_Refinement/local_verification.json").read_text(encoding="utf-8"))
    crossing = local_verification["anchors"]["bridge_crossing"]["xy_m"]
    conflict_positions = {**nodes, **landmarks, **{key: m(site["xy"]) for key, site in settlements.items()},
                          "bridge_crossing": crossing}
    if h.shape != (H // 8 + 1, W // 8 + 1) or (metrics["width_m"], metrics["height_m"]) != (W, H):
        raise ValueError("Regenerate the regional terrain before building the planning sheet.")

    s = Svg()
    s.add('<?xml version="1.0" encoding="UTF-8"?>')
    s.add(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
          f'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
          f'width="{VB_W}" height="{VB_H}" viewBox="{VB_X} {VB_Y} {VB_W} {VB_H}">')
    s.add("<title>Lowmark Vale blockout planning map (true scale, 1 SVG unit = 1 m)</title>")
    s.add('<desc>World origin = SVG (0,0) = south-west map corner; world (x east, y north) is drawn at SVG (x, -y). '
          f'Map frame {W} x {H} m. Grid: 384 m sectors (A-{COLS[-1]} x 01-{ROWS:02}), 192 m quadrants. '
          'Generated by CODE/Scripts/terrain_generation/build_blockout_planning_map.py from lowmark_controls.json '
          'and MEDIA/Maps/Lowmark_Terrain. Not canon; see the companion note for status rules.</desc>')
    s.add('<defs>'
          '<pattern id="fenHatch" patternUnits="userSpaceOnUse" width="60" height="60" patternTransform="rotate(30)">'
          '<rect width="60" height="60" fill="#cfe6ee"/><line x1="0" y1="0" x2="0" y2="60" stroke="#7fb6cf" stroke-width="8"/></pattern>'
          '<pattern id="orchHatch" patternUnits="userSpaceOnUse" width="70" height="70" patternTransform="rotate(-35)">'
          '<rect width="70" height="70" fill="#dbeccb"/><line x1="0" y1="0" x2="0" y2="70" stroke="#93bf72" stroke-width="7"/></pattern>'
          '<pattern id="blockHatch" patternUnits="userSpaceOnUse" width="40" height="40" patternTransform="rotate(45)">'
          '<line x1="0" y1="0" x2="0" y2="40" stroke="#c62828" stroke-width="6" stroke-opacity="0.55"/></pattern>'
          '</defs>')
    s.add(f'<rect x="{VB_X}" y="{VB_Y}" width="{VB_W}" height="{VB_H}" fill="#ffffff"/>')

    # --- base terrain -----------------------------------------------------
    s.layer("L01_terrain_base", "01 Terrain base (hillshade, contours)")
    s.add(f'<rect x="0" y="{-H}" width="{W}" height="{H}" fill="#f4f1e8"/>')
    shade = hillshade_png(h)
    half = 4  # 8 m samples on nodes: centre each image pixel on its sample
    s.add(f'<image x="{-half}" y="{-H - half}" width="{W + 2 * half}" height="{H + 2 * half}" '
          f'preserveAspectRatio="none" opacity="0.32" style="image-rendering:optimizeQuality" '
          f'xlink:href="data:image/png;base64,{shade}"/>')
    levels = np.arange(60, 231, 5)
    cps = contour_paths(h, levels)
    s.add('<g id="contours_5m" fill="none" stroke="#8a7a5c" stroke-linejoin="round">')
    for lev, paths in cps.items():
        index = abs(lev % 25) < 1e-6
        w_ = 3.2 if index else 1.4
        op = 0.75 if index else 0.45
        if paths:
            s.add(f'<path data-elev-m="{int(lev)}" stroke-width="{w_}" stroke-opacity="{op}" d="{" ".join(paths)}"/>')
    s.add("</g>")
    s.end()

    # --- planning regions -------------------------------------------------
    s.layer("L02_planning_regions", "02 Planning regions A-K (approved map, traced by eye)")
    for key, name, (cx, cy), (rx, ry), _lp in REGIONS:
        x, y = px_to_m(cx, cy)
        s.add(f'<ellipse id="region_{key}" cx="{fmt(x)}" cy="{fmt(-y)}" rx="{fmt(rx * W / 1096)}" '
              f'ry="{fmt(ry * H / 892)}" fill="none" stroke="#2e4a2e" stroke-width="7" stroke-dasharray="44 26" stroke-opacity="0.7">'
              f'<title>{escape(key + " " + name)}</title></ellipse>')
    s.end()

    # --- land-use areas ---------------------------------------------------
    s.layer("L03_landuse", "03 Fen, orchard floodplain")
    fen = ctrl["wetlands"][0]
    s.add(f'<polygon id="stillwater_fen" points="{pts([m(p) for p in fen["polygon"]])}" fill="url(#fenHatch)" '
          f'fill-opacity="0.75" stroke="#4f97b8" stroke-width="6"/>')
    fp = ctrl["floodplains"][0]
    s.add(f'<polygon id="floodplain_orchards" points="{pts([m(p) for p in fp["polygon"]])}" fill="url(#orchHatch)" '
          f'fill-opacity="0.8" stroke="#5f9a3e" stroke-width="6"/>')
    s.add(f'<polyline id="orchard_drainage_apron" points="{pts([m(p) for p in fp["drainage_corridor_points"]])}" '
          f'fill="none" stroke="#5f9a3e" stroke-width="4" stroke-dasharray="20 14"/>')
    s.end()

    # --- settlement envelopes & working landscape ------------------------
    s.layer("L04_envelopes", "04 Settlement envelopes and working landscape (proposed)")
    for sid, st in settlements.items():
        x, y = m(st["xy"])
        ax, ay = st["envelope_axes_m"]
        status = SETTLEMENT_STATUS[sid][0]
        col = C_BLOCK if status == "block" else C_PROV
        s.add(f'<circle id="working_{sid}" cx="{fmt(x)}" cy="{fmt(-y)}" r="{st["working_radius_m"]}" fill="none" '
              f'stroke="{C_PROV}" stroke-width="4" stroke-dasharray="6 18" stroke-linecap="round" stroke-opacity="0.8"/>')
        s.add(f'<ellipse id="envelope_{sid}" cx="{fmt(x)}" cy="{fmt(-y)}" rx="{ax / 2}" ry="{ay / 2}" '
              f'fill="{col}" fill-opacity="0.10" stroke="{col}" stroke-width="9" stroke-dasharray="36 18">'
              f'<title>{escape(st["name"])} envelope {ax} x {ay} m (upper proposed span)</title></ellipse>')
        if status == "block":
            s.add(f'<ellipse cx="{fmt(x)}" cy="{fmt(-y)}" rx="{ax / 2}" ry="{ay / 2}" fill="url(#blockHatch)"/>')
    s.end()

    # --- water -------------------------------------------------------------
    s.layer("L05_water", "05 Rivers and engineered water (true channel width)")
    for r in ctrl["hydrology"]["reaches"]:
        line = [m(p) for p in r["points"]]
        wdt = 2 * r["half_width_m"]
        if r["kind"] == "natural":
            s.add(f'<polyline id="reach_{r["id"]}" points="{pts(line)}" fill="none" stroke="{C_WATER}" '
                  f'stroke-width="{wdt}" stroke-linejoin="round" stroke-linecap="round"/>')
        elif r["kind"] == "backwater":
            s.add(f'<polyline id="reach_{r["id"]}" points="{pts(line)}" fill="none" stroke="{C_WATER}" '
                  f'stroke-width="{wdt}" stroke-opacity="0.55" stroke-linejoin="round" stroke-dasharray="70 30"/>')
        elif r["kind"] == "engineered":
            s.add(f'<polyline id="reach_{r["id"]}" points="{pts(line)}" fill="none" stroke="{C_ENG}" '
                  f'stroke-width="{max(wdt, 10) + 10}" stroke-linejoin="miter"/>')
            s.add(f'<polyline points="{pts(line)}" fill="none" stroke="#bfe0f5" stroke-width="{max(wdt, 10) - 2}" stroke-linejoin="miter"/>')
        else:  # anomalous_engineered
            s.add(f'<polyline id="reach_{r["id"]}" points="{pts(line)}" fill="none" stroke="{C_ANOM}" '
                  f'stroke-width="14" stroke-dasharray="40 16" stroke-linejoin="miter"/>')
    s.end()

    # --- roads ------------------------------------------------------------
    s.layer("L06_routes", "06 Routes and corridors (approved-map traces / proposed access)")
    for r in ctrl["routes"]:
        line = [m(p) for p in r["points"]]
        proposed = r["status"].startswith("Proposed")
        if proposed:
            s.add(f'<polyline id="route_{r["id"]}" points="{pts(line)}" fill="none" stroke="#6d6d6d" '
                  f'stroke-width="{r["width_m"]}" stroke-dasharray="30 18" stroke-linecap="round"/>')
        elif r["route_type"] == "cart":
            s.add(f'<polyline id="route_{r["id"]}" points="{pts(line)}" fill="none" stroke="#ffffff" '
                  f'stroke-width="{r["width_m"] + 10}" stroke-linejoin="round" stroke-linecap="round"/>')
            s.add(f'<polyline points="{pts(line)}" fill="none" stroke="#8b5a2b" stroke-width="{r["width_m"]}" '
                  f'stroke-linejoin="round" stroke-linecap="round"/>')
        else:
            s.add(f'<polyline id="route_{r["id"]}" points="{pts(line)}" fill="none" stroke="#8b5a2b" '
                  f'stroke-width="9" stroke-dasharray="4 22" stroke-linecap="round"/>')
    # unbuilt crossings from verification.json (route x water)
    s.add('<g id="crossings">')
    for r in ver["routes"]:
        crossings = r["crossings"] if isinstance(r["crossings"], list) else json.loads(r["crossings"])
        for c in crossings:
            x, y = c["xy_m"]
            s.add(f'<g><title>Unbuilt crossing: {escape(r["id"])} x {escape(c["reach"])}</title>'
                  f'<rect x="{fmt(x - 22)}" y="{fmt(-y - 22)}" width="44" height="44" fill="#ffffff" stroke="{C_PROV}" '
                  f'stroke-width="7" transform="rotate(45 {fmt(x)} {fmt(-y)})"/></g>')
    s.add("</g>")
    s.end()

    # --- capacity candidates -----------------------------------------------
    s.layer("L07_capacity", "07 Terrain-capacity candidate centres (not buildings)")
    local_ids = {"crestbridge", "greyharrow", "reedmere", "drowsebank_mill"}
    for sid, plist in cand.items():
        if sid in local_ids:
            continue
        for x, y, _z in plist:
            s.add(f'<circle cx="{fmt(x)}" cy="{fmt(-y)}" r="7" fill="#555"/>')
    for key, plist in lcand.items():
        for p_ in plist:
            x, y = p_["xy_m"]
            fill = "#555" if p_["settlement"] != "reedmere" else "#3a86c8"
            s.add(f'<circle cx="{fmt(x)}" cy="{fmt(-y)}" r="5" fill="{fill}"/>')
    s.end()

    # --- grid --------------------------------------------------------------
    s.layer("L08_grid", "08 Blockout grid (384 m sectors / 192 m cells)")
    g = []
    for x in range(CELL, W, CELL):
        if x % SECTOR:
            g.append(f"M{x},0 V{-H}")
    for y in range(CELL, H, CELL):
        if y % SECTOR:
            g.append(f"M0,{-y} H{W}")
    s.add(f'<path id="grid_cells_192m" d="{" ".join(g)}" stroke="#4b5a6a" stroke-width="2" stroke-opacity="0.35" '
          f'stroke-dasharray="10 10" fill="none"/>')
    g = [f"M{x},0 V{-H}" for x in range(SECTOR, W, SECTOR)] + [f"M0,{-y} H{W}" for y in range(SECTOR, H, SECTOR)]
    s.add(f'<path id="grid_sectors_384m" d="{" ".join(g)}" stroke="#2b3a4a" stroke-width="5" stroke-opacity="0.55" fill="none"/>')
    s.add('<g id="sector_ids">')
    for i in range(W // SECTOR):
        for j in range(H // SECTOR):
            s.text(i * SECTOR + 12, -(j + 1) * SECTOR + 40, f"{COLS[i]}{j + 1:02d}", size=32, fill="#2b3a4a",
                   halo=False, extra=' fill-opacity="0.75"')
    s.add("</g>")
    s.end()

    # --- waterworks structures ---------------------------------------------
    s.layer("L09_structures", "09 Waterworks and anchors (approved-map symbols)")

    def anchor(x, y, kind, status, title):
        col = {"ok": C_OK, "prov": C_PROV, "block": C_BLOCK}[status]
        fill = col if status == "ok" else "#ffffff"
        dash = ' stroke-dasharray="14 8"' if status == "prov" else ""
        X, Y = P(x, y)
        out = f'<g><title>{escape(title)}</title>'
        if kind == "settlement":
            out += f'<rect x="{fmt(X - 34)}" y="{fmt(Y - 34)}" width="68" height="68" fill="{fill}" stroke="{col}" stroke-width="10"{dash}/>'
        elif kind == "structure":
            out += f'<rect x="{fmt(X - 30)}" y="{fmt(Y - 18)}" width="60" height="36" fill="{fill}" stroke="{col}" stroke-width="9"{dash}/>'
        else:
            out += f'<circle cx="{fmt(X)}" cy="{fmt(Y)}" r="30" fill="{fill}" stroke="{col}" stroke-width="10"{dash}/>'
        if status == "block":
            out += (f'<circle cx="{fmt(X)}" cy="{fmt(Y)}" r="62" fill="none" stroke="{C_BLOCK}" stroke-width="8"/>'
                    f'<path d="M{fmt(X - 44)},{fmt(Y - 44)} L{fmt(X + 44)},{fmt(Y + 44)} M{fmt(X + 44)},{fmt(Y - 44)} L{fmt(X - 44)},{fmt(Y + 44)}" stroke="{C_BLOCK}" stroke-width="8"/>')
        out += "</g>"
        s.add(out)

    hl = ((nodes["hollow_lock_inlet"][0] + nodes["hollow_lock_tail"][0]) / 2, (nodes["hollow_lock_inlet"][1] + nodes["hollow_lock_tail"][1]) / 2)
    bw = ((nodes["weir_up"][0] + nodes["weir_down"][0]) / 2, (nodes["weir_up"][1] + nodes["weir_down"][1]) / 2)
    anchor(*hl, "structure", "ok", "Hollow Lock (CR-3 existence; approved-map position; 1.1 m static head proposal)")
    anchor(*bw, "structure", "ok", "Bramblelock Weir (approved-map position; 1.2 m head proposal)")
    anchor(*nodes["weir_up"], "point", "block", "Relief Cut mouth = common node weir_up (TC-09)")
    anchor(*nodes["mill_forebay"], "structure", "prov", "Drowsebank wheel drop (forebay->tailrace, 0.95 m head proposal)")
    anchor(*nodes["uphill_canal_foot"], "point", "prov", "Uphill Canal foot pool (TC-14)")
    anchor(*nodes["uphill_canal_cistern"], "point", "prov", "Uphill Canal cistern node at east frame edge (TC-14)")
    anchor(*crossing, "structure", "prov", "Technical road/river crossing (TC-04); not approved bridge centre")
    for sid, st in settlements.items():
        x, y = m(st["xy"])
        anchor(x, y, "settlement", SETTLEMENT_STATUS[sid][0], f'{st["name"]} anchor [{x:.0f}, {y:.0f}]')
    for lid, (x, y) in landmarks.items():
        status, refs, label = LANDMARK_STATUS[lid]
        if label is None:
            continue
        anchor(x, y, "point", status, f"{label} anchor [{x:.0f}, {y:.0f}]")
    s.end()

    # --- conflict tags -----------------------------------------------------
    s.layer("L10_conflicts", "10 Conflict / provisional tags (register ids)")
    for cid, sev, _txt, location in CONFLICTS:
        if location is None:
            continue
        loc = conflict_positions[location]
        dx, dy = TAG_POS.get(cid, (60, 60))
        col = C_BLOCK if sev == "block" else C_PROV
        x, y = loc[0] + dx * .55, loc[1] + dy * .55
        X, Y = P(x, y)
        wbox = 24 * len(cid) + 24
        s.add(f'<g id="tag_{cid}"><rect x="{fmt(X)}" y="{fmt(Y - 38)}" width="{wbox}" height="48" rx="8" '
              f'fill="{col}"/>')
        s.text(X + wbox / 2, Y, cid, size=34, anchor="middle", weight="bold", fill="#ffffff", halo=False)
        s.add("</g>")
    s.end()

    # --- labels ------------------------------------------------------------
    s.layer("L11_labels", "11 Labels")
    for key, name, _c, _r, (lx, ly) in REGIONS:
        X, Y = P(*px_to_m(lx, ly))
        s.add(f'<circle cx="{fmt(X)}" cy="{fmt(Y)}" r="58" fill="#2e4a2e"/>')
        s.text(X, Y + 22, key, size=66, anchor="middle", weight="bold", fill="#ffffff", halo=False)
    X, Y = P(*px_to_m(*E_LETTER_PX))
    s.add(f'<circle cx="{fmt(X)}" cy="{fmt(Y)}" r="58" fill="#2e4a2e"/>')
    s.text(X, Y + 22, "E", size=66, anchor="middle", weight="bold", fill="#ffffff", halo=False)

    def lab(x, y, txt, size=70, anchor_="start", **kw):
        X, Y = P(x, y)
        s.text(X, Y, txt, size=size * .66, anchor=anchor_, **kw)

    for sid, st in settlements.items():
        x, y = m(st["xy"])
        dx, dy, a = LABEL_OFFSETS[sid]
        status = SETTLEMENT_STATUS[sid][0]
        col = {"ok": C_OK, "prov": C_PROV, "block": C_BLOCK}[status]
        big = sid in ("brookhollow", "crestbridge", "ashenstead", "greyharrow")
        lab(x + dx, y + dy, st["name"], size=96 if big else 78, anchor_=a, weight="bold", fill=col)
    for lid, (x, y) in landmarks.items():
        status, refs, label = LANDMARK_STATUS[lid]
        if label is None:
            continue
        dx, dy, a = LABEL_OFFSETS[lid]
        col = {"ok": C_OK, "prov": C_PROV, "block": C_BLOCK}[status]
        lab(x + dx, y + dy, label, size=62, anchor_=a, fill=col, weight="bold")
    lab(hl[0] - 40, hl[1] + 70, "Hollow Lock", size=62, anchor_="end", weight="bold")
    lab(bw[0] + 48, bw[1] - 82, "Bramblelock Weir", size=62, weight="bold")
    # area / waterway names (italic). Positions from the approved planning map labels where noted.
    for (px, py), txt, size, col in [
        ((350, 318), "Stillwater Fen", 120, "#1e5f7f"),
        ((568, 762), "Whisperflow Run", 92, "#1e5f7f"),
        ((785, 655), "Floodplain Orchards", 64, "#3c6b28"),
        ((995, 560), "Brackenford Woods", 76, "#2e4a2e"),
        ((968, 728), "Greyharrow Reach", 58, "#1e5f7f"),
        ((912, 445), "Uphill Canal", 64, C_ANOM),
        ((583, 428), "Relief Cut", 76, C_ENG),
        ((657, 282), "Path of Unburnt Reeds", 58, "#8b5a2b"),
        ((120, 95), "Veilwater headwaters", 58, "#1e5f7f"),
        ((240, 490), "river (fen outlet)", 46, "#1e5f7f"),
    ]:
        x, y = px_to_m(px, py)
        lab(x, y, txt, size=size, anchor_="middle", fill=col, italic=True, weight="bold")
    s.end()

    # --- frame, ticks, north arrow, scale -----------------------------------
    s.layer("L12_frame", "12 Frame, coordinates, north arrow, scale bar")
    s.add(f'<rect id="map_frame_{W}x{H}" x="0" y="{-H}" width="{W}" height="{H}" fill="none" stroke="#000" stroke-width="10"/>')
    for x in range(0, W + 1, CELL):
        major = x % SECTOR == 0
        L = 60 if major else 30
        s.add(f'<path d="M{x},0 V{L} M{x},{-H} V{-H - L}" stroke="#000" stroke-width="{5 if major else 3}"/>')
        if major:
            s.text(x, 140, f"{x}", size=46, anchor="middle", halo=False)
    for y in range(0, H + 1, CELL):
        major = y % SECTOR == 0
        L = 60 if major else 30
        s.add(f'<path d="M0,{-y} H{-L} M{W},{-y} H{W + L}" stroke="#000" stroke-width="{5 if major else 3}"/>')
        if major:
            s.text(-80, -y + 16, f"{y}", size=46, anchor="end", halo=False)
    for i in range(W // SECTOR):
        cx = i * SECTOR + SECTOR / 2
        s.text(cx, 260, COLS[i], size=72, anchor="middle", weight="bold", halo=False)
        s.text(cx, -H - 90, COLS[i], size=72, anchor="middle", weight="bold", halo=False)
    for j in range(H // SECTOR):
        cy = -(j * SECTOR + SECTOR / 2)
        s.text(-330, cy + 25, f"{j + 1:02d}", size=72, anchor="middle", weight="bold", halo=False)
        s.text(W + 160, cy + 25, f"{j + 1:02d}", size=72, anchor="middle", weight="bold", halo=False)
    s.text(W / 2, 360, f"Easting X (m) from south-west origin · sector columns A–{COLS[-1]}", size=52, anchor="middle", halo=False)
    s.add(f'<text x="-430" y="{-H / 2}" font-size="52" font-family="{FONT}" text-anchor="middle" '
          f'transform="rotate(-90 -430 {-H / 2})">Northing Y (m) from south-west origin · sector rows 01–{ROWS:02}</text>')
    s.add(f'<circle cx="0" cy="0" r="22" fill="{C_BLOCK}"/>')
    s.text(30, 230, "ORIGIN (0, 0)", size=44, weight="bold", fill=C_BLOCK, halo=False)
    # title strip above the map
    s.text(0, -H - 470, "LOWMARK VALE — BLOCKOUT PLANNING MAP (TRUE SCALE)", size=106, weight="bold", halo=False)
    s.text(0, -H - 330, f"1 SVG unit = 1 m · {W:,} × {H:,} m · {len(COLS) * ROWS} sectors of 384 m · 192 m quadrants", size=62, halo=False)
    s.text(0, -H - 240, "Sources: Lowmark terrain controls, regenerated regional and local surfaces, Director reference maps and conflict register",
           size=38, fill="#444", halo=False)
    # north arrow (grid north = +Y)
    nx, ny = W - 330, -H + 380
    s.add(f'<g id="north_arrow"><path d="M{nx},{ny - 230} L{nx + 90},{ny + 90} L{nx},{ny + 30} L{nx - 90},{ny + 90} Z" '
          f'fill="#000" stroke="#fff" stroke-width="10"/>')
    s.text(nx, ny - 260, "N", size=110, anchor="middle", weight="bold")
    s.text(nx, ny + 180, "grid north = +Y", size=44, anchor="middle")
    s.add("</g>")
    s.end()

    def scale_bar(sx, sy):
        s.add('<g id="scale_bar">')
        s.add(f'<rect x="{sx - 60}" y="{sy - 170}" width="2240" height="320" fill="#ffffff" fill-opacity="0.9" stroke="none"/>')
        for k in range(4):
            fill = "#000" if k % 2 == 0 else "#fff"
            s.add(f'<rect x="{sx + k * 500}" y="{sy - 40}" width="500" height="40" fill="{fill}" stroke="#000" stroke-width="4"/>')
        for k in range(5):
            s.text(sx + k * 500, sy - 60, f"{k * 500}", size=46, anchor="middle", halo=False)
        s.text(sx + 2060, sy - 60, "m", size=46, halo=False)
        for k in range(int(2048 / CELL) + 0):
            fill = "#2b3a4a" if (k // 2) % 2 == 0 else "#fff"
            s.add(f'<rect x="{sx + k * CELL}" y="{sy + 20}" width="{CELL}" height="30" fill="{fill}" stroke="#2b3a4a" stroke-width="3"/>')
        s.text(sx, sy + 110, "sector 384 m = 2 cells of 192 m · bars are true length", size=44, halo=False)
        s.add("</g>")

    # --- right panel: declaration and legend --------------------------------
    s.layer("L13_legend", "13 Legend and declarations")
    px0 = W + MR + 120
    y = -H - 40
    s.add(f'<g transform="translate({px0} {-H}) scale(.67) translate({-px0} {H})">')
    s.add(f'<rect x="{px0 - 60}" y="{-H - 120}" width="{PANEL_W}" height="4790" fill="#fafafa" stroke="#000" stroke-width="5"/>')

    def ptxt(t, size=50, weight="normal", fill=C_OK, dy=None, x=None, italic=False):
        nonlocal y
        y += dy if dy is not None else size * 1.35
        s.text(px0 if x is None else x, y, t, size=size, weight=weight, fill=fill, halo=False, italic=italic)

    ptxt("MAP DECLARATION", 70, "bold", dy=40)
    for t in [
        f"Director-approved working extent: {W:,} m E–W × {H:,} m N–S ({W * H / 1e6:.6f} km²).",
        "Origin: south-west frame corner = (0, 0). X east, Y north, metres.",
        "  Blender: X east / Y north / Z up.  Unity: X east / Y up / Z north.",
        "  GLB terrain: X east / Y up / −Z north (terrain README).",
        "SVG: world (x, y) is drawn at (x, −y); import puts origin at (0, 0).",
        f"Grid: 384 m sectors, columns A–{COLS[-1]} west to east, rows 01–{ROWS:02} south to north.",
        "  Sector ID e.g. H05 = x 2688–3072, y 1536–1920.",
        "  192 m cells = sector quadrant: H05.SW / .SE / .NW / .NE.",
        f"  Quadrant index i = floor(x/192) 0–{W//CELL-1}, j = floor(y/192) 0–{H//CELL-1}.",
        "Terrain: 8 m height_engineered.npy; contours 5 m (25 m index);",
        "  hillshade 2× exaggerated for reading only. Heights are technical",
        "  proposals, not surveyed or approved.",
        "Positions follow the approved composition. Amber anchors include",
        "  provisional compact site adjustments. The grid indexes placement.",
    ]:
        ptxt(t, 44)

    ptxt("STATUS KEY", 70, "bold", dy=110)
    rows = [
        (C_OK, "solid", "CONFIRMED — on the Director-approved composition (anchor"),
        (None, None, "  or traced alignment); placement approved, metres approximate."),
        (C_PROV, "dash", "PROVISIONAL — technical proposal, estimate, or MAP"),
        (None, None, "  VERIFICATION REQUIRED item (envelopes, budgets, corridors)."),
        (C_BLOCK, "block", "BLOCKED — register severity 'Blocks': do not block out the"),
        (None, None, "  dependent feature until the Director / Sol rules."),
    ]
    for col, kind, t in rows:
        y += 62
        if col:
            if kind == "solid":
                s.add(f'<circle cx="{px0 + 30}" cy="{y - 16}" r="24" fill="{col}"/>')
            elif kind == "dash":
                s.add(f'<circle cx="{px0 + 30}" cy="{y - 16}" r="24" fill="#fff" stroke="{col}" stroke-width="8" stroke-dasharray="12 7"/>')
            else:
                s.add(f'<circle cx="{px0 + 30}" cy="{y - 16}" r="24" fill="#fff" stroke="{col}" stroke-width="8"/>'
                      f'<circle cx="{px0 + 30}" cy="{y - 16}" r="40" fill="none" stroke="{col}" stroke-width="6"/>')
        s.text(px0 + 90, y, t, size=44, halo=False, weight="bold" if col else "normal",
               fill=col if col else C_OK)

    ptxt("LEGEND", 70, "bold", dy=110)
    items = [
        ("sq", C_OK, "Settlement anchor (approved-map symbol centre)"),
        ("ci", C_OK, "Landmark / named site anchor"),
        ("st", C_OK, "Waterworks structure (lock, weir, wheel drop, crossing)"),
        ("river", C_WATER, "Natural river, drawn at modelled width (36 / 28 / 16 m)"),
        ("back", C_WATER, "Western Whisperflow arm — topology unresolved"),
        ("eng", C_ENG, "Engineered channel: Relief Cut, Hollow Lock, mill leat/race"),
        ("anom", C_ANOM, "Uphill Canal (anomalous authored line; schematic steps)"),
        ("fen", None, "Stillwater Fen (approved composition; stage technical)"),
        ("orch", None, "Floodplain Orchards field polygon; dashed = drainage apron"),
        ("cart", None, "Cart road, 12 m corridor (approved-map trace)"),
        ("foot", None, "Foot path, 5 m (Path of Unburnt Reeds, Reedmere path)"),
        ("acc", None, "Proposed technical access (Mill, Hall, Depot) — not approved"),
        ("x", C_PROV, "Unbuilt road/water crossing (verification.json)"),
        ("env", C_PROV, "Settlement envelope = upper proposed span (ellipse)"),
        ("work", C_PROV, "Working landscape radius (fields, approaches, waterfront)"),
        ("reg", None, "Planning region A–K (approved map, traced by eye ±60 m)"),
        ("cand", None, "Terrain-capacity candidate centre (NOT a building)"),
        ("tag", C_BLOCK, "Conflict tag (red = Blocks, amber = Degrades/scope)"),
        ("grid", None, "Sector 384 m (solid) / cell 192 m (dashed)"),
    ]
    for kind, col, t in items:
        y += 76
        cx, cy = px0 + 70, y - 16
        if kind == "sq":
            s.add(f'<rect x="{cx - 26}" y="{cy - 26}" width="52" height="52" fill="{col}"/>')
        elif kind == "ci":
            s.add(f'<circle cx="{cx}" cy="{cy}" r="24" fill="{col}"/>')
        elif kind == "st":
            s.add(f'<rect x="{cx - 30}" y="{cy - 18}" width="60" height="36" fill="{col}"/>')
        elif kind == "river":
            s.add(f'<path d="M{cx - 60},{cy} H{cx + 60}" stroke="{col}" stroke-width="30"/>')
        elif kind == "back":
            s.add(f'<path d="M{cx - 60},{cy} H{cx + 60}" stroke="{col}" stroke-width="26" stroke-opacity="0.55" stroke-dasharray="40 14"/>')
        elif kind == "eng":
            s.add(f'<path d="M{cx - 60},{cy} H{cx + 60}" stroke="{C_ENG}" stroke-width="26"/><path d="M{cx - 60},{cy} H{cx + 60}" stroke="#bfe0f5" stroke-width="14"/>')
        elif kind == "anom":
            s.add(f'<path d="M{cx - 60},{cy} H{cx + 60}" stroke="{col}" stroke-width="14" stroke-dasharray="30 12"/>')
        elif kind == "fen":
            s.add(f'<rect x="{cx - 60}" y="{cy - 26}" width="120" height="52" fill="url(#fenHatch)" stroke="#4f97b8" stroke-width="5"/>')
        elif kind == "orch":
            s.add(f'<rect x="{cx - 60}" y="{cy - 26}" width="120" height="52" fill="url(#orchHatch)" stroke="#5f9a3e" stroke-width="5"/>')
        elif kind == "cart":
            s.add(f'<path d="M{cx - 60},{cy} H{cx + 60}" stroke="#8b5a2b" stroke-width="14"/>')
        elif kind == "foot":
            s.add(f'<path d="M{cx - 60},{cy} H{cx + 60}" stroke="#8b5a2b" stroke-width="9" stroke-dasharray="4 18" stroke-linecap="round"/>')
        elif kind == "acc":
            s.add(f'<path d="M{cx - 60},{cy} H{cx + 60}" stroke="#6d6d6d" stroke-width="10" stroke-dasharray="26 14"/>')
        elif kind == "x":
            s.add(f'<rect x="{cx - 20}" y="{cy - 20}" width="40" height="40" fill="#fff" stroke="{col}" stroke-width="7" transform="rotate(45 {cx} {cy})"/>')
        elif kind == "env":
            s.add(f'<ellipse cx="{cx}" cy="{cy}" rx="60" ry="28" fill="{col}" fill-opacity="0.12" stroke="{col}" stroke-width="7" stroke-dasharray="22 10"/>')
        elif kind == "work":
            s.add(f'<ellipse cx="{cx}" cy="{cy}" rx="60" ry="28" fill="none" stroke="{col}" stroke-width="4" stroke-dasharray="5 12"/>')
        elif kind == "reg":
            s.add(f'<ellipse cx="{cx}" cy="{cy}" rx="60" ry="28" fill="none" stroke="#2e4a2e" stroke-width="5" stroke-dasharray="26 14"/>')
        elif kind == "cand":
            for k in range(-2, 3):
                s.add(f'<circle cx="{cx + k * 24}" cy="{cy}" r="7" fill="#555"/>')
        elif kind == "tag":
            s.add(f'<rect x="{cx - 64}" y="{cy - 26}" width="60" height="52" rx="10" fill="{C_BLOCK}"/><rect x="{cx + 4}" y="{cy - 26}" width="60" height="52" rx="10" fill="{C_PROV}"/>')
        elif kind == "grid":
            s.add(f'<path d="M{cx - 60},{cy - 22} H{cx + 60}" stroke="#2b3a4a" stroke-width="5"/><path d="M{cx - 60},{cy + 14} H{cx + 60}" stroke="#4b5a6a" stroke-width="3" stroke-dasharray="10 10"/>')
        s.text(px0 + 170, y, t, size=44, halo=False)

    ptxt("PLANNING REGIONS (approved-map letters)", 56, "bold", dy=110)
    for key, name, *_ in REGIONS[:4] + [("E", "Relief Cut Engineering Line (linear; drawn as the Cut)")] + REGIONS[4:]:
        ptxt(f"{key}  {name}", 44, dy=58)

    ptxt("SCALE", 70, "bold", dy=120)
    scale_bar(px0 + 40, y + 190)
    y += 330

    ptxt("BLENDER / PGS USE", 70, "bold", dy=110)
    for t in [
        f"1. Import the SVG. Use map_frame_{W}x{H} to check a width of {W:,} m.",
        "   The frame's lower-left corner is world (0, 0); keep it there.",
        f"2. Or use the PNG as a top-ortho reference: {1 / png_scale:g} m per pixel; map frame",
        f"   NW corner at pixel ({ML * png_scale:g}, {MT * png_scale:g}) from the image's top-left.",
        "3. Align terrain.glb / local GLBs on the same origin (no offsets).",
        "4. Place buildings only inside envelopes, off channels and crossings;",
        "   leave BLOCKED features (red) as empty placeholders.",
        "5. Record any new building position in world metres + sector ID.",
    ]:
        ptxt(t, 44)
    s.add("</g>")
    s.end()

    # --- bottom panel: settlement table, conflicts, unanchored sites ---------
    s.layer("L14_tables", "14 Settlement guidance, conflicts, unanchored sites")
    by0 = 520
    s.add(f'<rect x="-460" y="{by0 - 80}" width="{W + MR + PANEL_W + 40}" height="{BOTTOM - 520}" fill="#fafafa" stroke="#000" stroke-width="5"/>')
    yy = by0
    s.text(-400, yy, "SETTLEMENT BLOCKOUT GUIDANCE (building totals are ESTIMATES: proposed planning targets from the 2026-11-06 terrain mission, not canon)",
           size=56, weight="bold", halo=False)
    cols_x = [-400, 380, 1200, 1840, 2420, 3000, 4060]
    heads = ["Settlement / anchor (m)", "Roofs (target)", "Regional screen", "Local 2 m screen", "Envelope (m)", "Status", "Blockout note"]
    yy += 80
    for cx_, t in zip(cols_x, heads):
        s.text(cx_, yy, t, size=42, weight="bold", halo=False)
    notes = {
        "brookhollow": "Waterfront flood zoning still required.",
        "crestbridge": "Compact Hall and Depot positions are provisional (TC-01–05).",
        "ashenstead": "Lower shoulder core; Rebirth Fields remain untraced.",
        "greyharrow": "Side-branch settlement; upper count unproven.",
        "reedmere": "Conditional stilt sites. Causeways and staging unbuilt.",
        "whisperflow_landing": "Working crossing envelope reaches main river (TC-13).",
        "drowsebank_mill": "Offset yard candidate; hydraulic and machinery layout open.",
    }
    for sid, st in settlements.items():
        yy += 62
        x, y_ = m(st["xy"])
        status = SETTLEMENT_STATUS[sid][0]
        col = {"ok": C_OK, "prov": C_PROV, "block": C_BLOCK}[status]
        b = st["buildings"]
        lc = local_counts.get(sid)
        rg = regional_counts[sid]
        local_display = (f'{lc["conditional_stilts"]} stilt (0 dry)' if sid == "reedmere"
                         else f'{lc["normal_candidates"]} / {lc["scenario_floor_candidates"]}' if lc else "—")
        row = [f'{st["name"]} [{x:.0f}, {y_:.0f}]', f"{b[0]}–{b[1]} (est.)", f'{rg["screened_roof_capacity"]} / {rg["flood_scenario_safe_capacity"]}',
               local_display,
               f'{st["envelope_axes_m"][0]} × {st["envelope_axes_m"][1]}',
               {"ok": "anchor confirmed", "prov": "provisional", "block": "BLOCKED"}[status] + " " + ",".join(SETTLEMENT_STATUS[sid][1]),
               notes[sid]]
        for i, (cx_, t) in enumerate(zip(cols_x, row)):
            s.text(cx_, yy, t, size=38, halo=False, fill=col if i == 5 else C_OK)
    yy += 62
    s.text(-400, yy, "Regional screen = normal-stage / outside +1.5 m scenario candidate count (terrain README); local = 2 m normal / scenario floor (LOCAL_README). "
           "Screens assume 120–160 m² mean roofs; they are capacity checks, not plot plans. Envelope axes are E–W × N–S full diameters.",
           size=36, fill="#444", halo=False)
    yy += 52
    s.text(-400, yy, "Hall and Depot use provisional compact positions. The civic budget and functional interfaces still require local design.",
           size=36, fill="#444", halo=False)

    # conflicts
    yy += 110
    s.text(-400, yy, "CONFLICTS AND PROVISIONAL ITEMS (Lowmark Terrain / Narrative Conflict Register TC-xx; NC = new, found while building this sheet)",
           size=56, weight="bold", halo=False)
    for k, (cid, sev, txt, _loc) in enumerate(CONFLICTS):
        yrow = yy + 70 + k * 56
        col = C_BLOCK if sev == "block" else C_PROV
        s.add(f'<rect x="-400" y="{yrow - 40}" width="190" height="50" rx="10" fill="{col}"/>')
        s.text(-305, yrow, cid, size=34, anchor="middle", weight="bold", fill="#fff", halo=False)
        s.text(-180, yrow, ("BLOCKS · " if sev == "block" else "") + txt, size=34, halo=False,
               fill=C_BLOCK if sev == "block" else C_OK)
    yy = yy + 70 + len(CONFLICTS) * 56 + 60

    # unanchored sites
    s.text(-400, yy, "NAMED SITES WITH NO APPROVED XY — not drawn as points; block out only inside the stated parent once D-5 / the TC row is ruled",
           size=56, weight="bold", halo=False)
    column_rows = (len(UNANCHORED) + 1) // 2
    for k, (pid, name, parent) in enumerate(UNANCHORED):
        colx = [-400, 3050][k // column_rows]
        yrow = yy + 70 + (k % column_rows) * 56
        s.text(colx, yrow, f"{pid}  {name} → {parent}", size=34, halo=False)
    s.end()
    s.add("</svg>")

    sheet = "\n".join(s.parts)
    svg_path = OUT / f"{STEM}.svg"
    if sectors_only and svg_path.read_text(encoding="utf-8") != sheet:
        raise ValueError("The master sheet differs from the current terrain. Run without --sectors-only to update both.")
    export_sectors(sheet, ctrl, ver, REGIONS, LANDMARK_STATUS, OUT / "grids", SECTOR, CELL)
    if sectors_only:
        return

    OUT.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(sheet, encoding="utf-8")
    from resvg_py import svg_to_bytes
    png_path = OUT / f"{STEM}.png"
    png_path.write_bytes(svg_to_bytes(svg_path=str(svg_path), zoom=png_scale, background="#ffffff"))
    frame_px = ((0 - VB_X) * png_scale, (-H - VB_Y) * png_scale)
    print(f"SVG {svg_path} ({svg_path.stat().st_size:,} bytes)")
    print(f"PNG {png_path} ({png_path.stat().st_size:,} bytes) {int(VB_W * png_scale)}x{int(VB_H * png_scale)} px, "
          f"{1 / png_scale:g} m/px; map frame NW corner at px {frame_px}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--png-scale", type=float, default=0.5, help="PNG pixels per metre (default 0.5 = 2 m/px)")
    ap.add_argument("--sectors-only", action="store_true", help="Write sectors from existing verified terrain without rewriting the master sheet")
    args = ap.parse_args()
    build(args.png_scale, args.sectors_only)
