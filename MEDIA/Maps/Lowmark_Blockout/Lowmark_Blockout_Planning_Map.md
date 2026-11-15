# Lowmark blockout planning map

[Editable SVG](Lowmark_Blockout_Planning_Map.svg) · [PNG reference](Lowmark_Blockout_Planning_Map.png) · [Terrain and regeneration instructions](../../../CODE/Scripts/terrain_generation/README.md).

The Director approved the **3,456 × 3,072 m** working extent. The sheet overlays the approved composition, current provisional site offsets, and regenerated terrain, water, route and capacity evidence. The original planning and thematic maps are preserved as composition references. Final placement under D-5 remains open.

## Frame and grid

| Property | Value |
| --- | --- |
| Extent | 3,456 m east–west × 3,072 m north–south, 10.616832 km² |
| Sector grid | 384 m, columns A–I west to east and rows 01–08 south to north, 72 sectors |
| Quadrants | 192 m, four per sector, 18 × 16 indices overall |
| Origin | Southwest corner at world (0, 0). In Blender X is east, Y north, Z up. In Unity X is east, Y up, Z north. The terrain GLB uses −Z north. |
| SVG | 1 unit = 1 m, plotted as (x, −y). The frame is `map_frame_3456x3072`. |
| PNG | 3948 × 3666 px at 2 m per pixel. The frame starts at pixel (260, 380) and spans 1728 × 1536 px. |
| Surface | 8 m regional samples, 5 m contours with 25 m index lines. Separate 2 m patches at the same origin. |

Use sector and quadrant IDs such as `H05.NE`. Sector H05 spans X 2688–3072 and Y 1536–1920. The overall quadrant indices are `floor(x/192)` (0–17) and `floor(y/192)` (0–15) on the half-open frame. The circled A–K letters inside the map are the planning regions from the Director's reference. Select a sector in the [coordinate index](grids/grid_index.csv) and see [Blender placement and PGS alignment](grids/README.md).

## Using the sheet

1. Import the SVG in Blender and check that the frame is 3,456 m wide with the southwest corner at the world origin. Use the PNG for labels, or position it as a top-view reference using its metric scale and frame corner above.
2. Align the regional GLB and local meshes using the shared origin. The terrain and water layers represent computed profiles, while working envelopes and capacity dots show feasible areas for later manual layout.
3. Keep channels, crossing gaps and proposed infrastructure corridors available for local design. Read the red tags before blockout. Amber identifies provisional anchor shifts, access corridors and conflict details.
4. Record new positions in world metres and sector/quadrant IDs. This sheet is the master reference. The sector files show the same geographic artwork clipped to each 384 m square.

The compact layout brings Hall and Depot closer to the civic crossing, offsets the Drowsebank working yard from its race and gives Whisperflow Landing a provisional main-river edge. The Hall water gate and stair, Depot outlet, separated Cut mouth and spur, and Landing approaches remain open. See the [conflict register](../../../04_CONTENT_PRODUCTION/Zones/Caelmor_Lowmark_Terrain_Narrative_Conflict_Register.md) and [measured geography review](../../../CODE/Scripts/terrain_generation/LOCAL_REVIEW.md).

The same [generator](../../../CODE/Scripts/terrain_generation/build_blockout_planning_map.py) renders the master and its sector files from the current controls, contours, crossings and capacity reports. It uses resvg-py 0.3.3 for the PNGs. The script runs at the end of `Generate-Lowmark.ps1 -Local`.
