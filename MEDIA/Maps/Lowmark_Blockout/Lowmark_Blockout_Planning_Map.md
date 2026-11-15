# Lowmark Blockout Planning Map: companion note

**Files:** `Lowmark_Blockout_Planning_Map.svg` (primary, editable), `Lowmark_Blockout_Planning_Map.png` (export of the same sheet). **Generator:** `CODE/Scripts/terrain_generation/build_blockout_planning_map.py`. Do not hand-edit the generated geometry as source. Change the controls or the script and regenerate: `python CODE/Scripts/terrain_generation/build_blockout_planning_map.py` (needs numpy, matplotlib, cairosvg).

**Status:** production planning sheet, 2026-11-15, built from repo head `c3b0e02`. It is not canon, and it does not rule D-5 (map placement), which is still open in the bible. It moves no anchor and resolves no conflict.

## 1. Sources used

| Source | What the map takes from it |
|---|---|
| `CODE/Scripts/terrain_generation/lowmark_controls.json` | World extent, origin and axes; every settlement and landmark anchor; all 33 water reaches (natural, backwater, engineered, anomalous) and their modelled widths; the 10 route traces; the fen and orchard polygons; settlement envelopes, working radii and building targets; the `unresolved` list |
| `MEDIA/Maps/Lowmark_Terrain/height_engineered.npy` | 5 m contours (25 m index) and the hillshade (8 m samples) |
| `MEDIA/Maps/Lowmark_Terrain/verification.json` | Unbuilt road/water crossing points and route lengths |
| `MEDIA/Maps/Lowmark_Terrain/candidate_plots.json` and `Local_Refinement/candidate_plots.json` | Terrain-capacity candidate centres. The local 2 m results are used for Crestbridge/Mill, Greyharrow and Reedmere |
| Terrain `README.md`, `LOCAL_README.md`, `MISSION.md`, `SOURCE_NOTES.md` | Capacity screens, scale status, coordinate conventions, building targets (the 2026-11-06 mission table) |
| `MEDIA/Maps/Lowmark_Planning_Map.png` (Director-approved composition) | Planning regions A–K, traced by eye; region letter positions; waterway and area label positions. It was also the visual style reference. No style image was attached to this request, so the existing planning map served as the reference. Its scale bar and contours were **not** used |
| `04_CONTENT_PRODUCTION/Zones/Caelmor_Lowmark_Terrain_Narrative_Conflict_Register.md` | TC-01 to TC-19, with their severities |
| `04_CONTENT_PRODUCTION/Zones/Caelmor_Lowmark_POI_and_Zone_Requirements.md`, `Quests/Caelmor_Lowmark_v1_Narrative_Production_Bible.md` (§3, §4), `LORE/Regions/Caelmor_Region1_LowmarkVale.md` (§IV–V) | POI slate, parent locations for sites that have no coordinates, D-4/D-5/D-10/CR-3 status |

## 2. Dimensions, grid and coordinates

- **Extent:** 6,144 m east–west by 4,992 m north–south (30.67 km²). This is the current working extent of the terrain foundation. No newer repo evidence supersedes it. Sol still describes it as "a working compromise for review", not approved world size.
- **Origin and axes:** the south-west frame corner is (0, 0). X runs east and Y runs north, in metres (`lowmark_controls.json` → `world.coordinate_system`). In Blender, X is east, Y north and Z up. In Unity, X is east, Y up and Z north. The terrain GLB uses X east, Y up, −Z north.
- **Grid:** 384 m sectors, 16 columns by 13 rows, each split into 192 m cells (2 × 2 per sector, 32 × 26 cells in all). Both divide the extent exactly. **No grid or tiling standard is recorded anywhere in the repo.** The terrain uses 8 m regional and 2 m local samples, and its local patch bounds are not on a 384 m lattice. The 384/192 m grid therefore comes from the Director's instruction for this sheet and is now recorded here.
- **IDs:** sector columns run **A–P west to east** and rows run **01–13 south to north**, so sector `H05` covers x 2688–3072 and y 1536–1920. A cell is its sector plus a quadrant: `H05.SW`, `.SE`, `.NW` or `.NE`. The numeric cell index is `i = floor(x/192)` (0–31) and `j = floor(y/192)` (0–25). The circled letters A–K on the map are the approved map's planning regions, not grid columns.
- **SVG units:** 1 user unit = 1 m. A world point (x, y) is drawn at SVG (x, −y), so the world origin is SVG (0, 0) and every path coordinate reads directly in metres. The layers are Inkscape layers (`L01`–`L14`) and can be toggled.
- **PNG:** 5292 × 4426 px at **2 m per pixel**. The map frame's north-west corner is at pixel (260, 380), and the frame is 3072 × 2496 px.

## 3. Confirmed, provisional, blocked

**Confirmed** means a feature is on the Director-approved composition from the 2026-11-06 terrain mission and has been traced as an anchor or alignment. Placement is approved; the metre values are approximate (about ±30–60 m). This covers the anchors of Brookhollow, Crestbridge, Ashenstead, Greyharrow, Reedmere, Hill Depot, Mantle Shrine, Circle of Unburnt Reeds, Veilwater Falls and the Whispering Door Farmhouse; the Hollow Lock and Bramblelock Weir positions; the river, Relief Cut and fen alignments; and the orchard field polygon. The Relief Cut and the Hollow Lock exist as canon only by CR-3. Their geometry is not ruled.

**Provisional** covers:
- every settlement envelope, working radius and building number
- the proposed access corridors (Crestbridge → Mill, → Hall → Depot)
- the Drowsebank Mill site (TC-06/07/08: the marker sits on the channel)
- the Uphill Canal line (TC-14: schematic steps; the mechanism is withheld)
- the western Whisperflow arm (backwater or meander, still unresolved)
- planning regions A–K (traced by eye)
- contour heights (technical proposals)
- every crossing (none is built)
- every TC row with severity "Degrades" or "scope"

**Blocked** (register severity "Blocks"; leave these as empty placeholders in blockout):
- **TC-01, Crest Hall.** The anchor is kept, but it is 640 m from the river, so the water-gate, Gate Landing, river-fed cistern and the Night Bridge north stair cannot be built as written.
- **TC-09, Relief Cut mouth.** The Cut mouth, the mill tail and Bramblelock share one node, so the MQ4 order (mouth → towpath → weir) has no length to build in.
- **TC-13, Whisperflow Landing.** The anchor is 490–520 m from any traced water, so the landing's water edge is unresolved.

**New finding, not in the register (NC-1):** the approved map puts the Whispering Door Farmhouse at [2108, 269], south-west on the Landing–Crestbridge road. POI §1/§6.1 (M01) places it on the Heartlands–Ashenstead edge, with a drain to the guide-line outfall under the Rebirth Fields, about 4 km away. It is drawn at the approved-map anchor and tagged for review.

Eighteen named sites have no approved XY: the granaries, the bridge structure, the Drowned Lamb, the bell tower, the Ember-Well, the Rebirth Fields, the Lantern Post, Widow's Step and others. They are **listed with their parent location and not drawn as points**.

## 4. Settlement footprints and building totals: assumptions

- **Building totals are estimates.** The only building numbers in the repo are the "proposed planning targets, not approved population canon" in the terrain `MISSION.md` table. The sheet shows them as written, for example Brookhollow 75–120 roofs, together with the terrain capacity screens that test them. Nothing here raises them to canon.
- **Envelopes** are the terrain model's own axis-aligned ellipses at the **upper** proposed span (`envelope_axes_m`, full E–W × N–S diameters). They are not plot plans. The model shows that smaller spans often cannot hold the lower building count.
- **Capacity dots** are terrain-screen candidate centres (about 120–160 m² roof screens on slope, freeboard and corridor checks). They show where buildable ground exists. **They are not building positions.** At Reedmere the dots are conditional stilt candidates; none of them is dry.
- **Crestbridge outworks:** Crest Hall and Hill Depot lie outside the 600 m core, and nobody has ruled whether the 60–100 roof target includes them (TC-19).
- **Whisperflow Landing** is a working crossing, not a village (D-4, CR-4). Its 5–12 roof target is kept as the mission's estimate.
- **Greyharrow** does not demonstrably reach 50 roofs (local screen 39), and the bible scopes it as a micro-settlement (TC-19).

## 5. Using the map for Blender blockout and PGS work

1. Import the SVG with File > Import > Scalable Vector Graphics. Select the `map_frame_6144x4992` rectangle and scale the whole import uniformly until the frame measures 6,144 m. Leave the frame's lower-left corner at (0, 0). Text is not imported, so read labels from the PNG.
2. As an alternative, set the PNG as a top-orthographic reference image at 2 m per pixel, offset so that the frame corner lands at the world origin.
3. Bring in `MEDIA/Maps/Lowmark_Terrain/terrain.glb` (regional) and the local GLBs on the same origin, with no offset. Contours on the sheet come from the same height array.
4. Place buildings inside settlement envelopes only. Keep clear of channels (drawn at modelled width), crossings and waterworks corridors. Do not build on the Drowsebank marker.
5. Leave BLOCKED features unbuilt and keep their footprints as placeholders. Amber items can be blocked out, but treat them as reversible.
6. Log every placed building with its world X/Y in metres and its sector/cell ID, for example `H05.NE`, so that a later D-5 ruling can be applied by coordinates.

## 6. Open items for the Director and Sol

- **D-5 (map placement):** rule whether the approved composition plus this sheet is the placement authority.
- **Grid:** confirm 384/192 m as the official blockout grid, since no repo document records it.
- **Sequence:** TC-01/02/03/05 (Crestbridge civic arrangement) is the next consequential ruling; then TC-09/06 (Cut mouth, towpath, weir and spur order); then TC-13 (the Landing's water and the western arm).
- **TC-15:** the extent of the Rebirth Fields.
- **TC-19:** settlement budget scope.
- **NC-1:** the Whispering Door Farmhouse placement.
- **D-10 (Mining):** still open. No mine site is shown.
