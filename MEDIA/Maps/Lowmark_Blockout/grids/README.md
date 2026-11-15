# Lowmark 2D sector references

[Coordinate and feature index](grid_index.csv) · [Full-region master sheet](../Lowmark_Blockout_Planning_Map.md).

The 3,456 × 3,072 m frame contains 72 sectors, A–I west to east and 01–08 south to north. Each sector has a layered SVG and a **384 × 384 px, 1 m/px** PNG, with north up and the 192 m quadrant boundaries in place. The files carry the master map's contours, water, routes, settlement and planning overlays, anchor styles and conflict tags in the sector viewport.

## Placement

Use the indexed minimum X and Y as the sector's southwest offset. The indexed centre is the insertion point for a centred image. For image-page coordinates `(u, v)` measured east and down from the upper left, the world point is `(x_min_m + u, y_max_m − v)`. A pixel centre uses `u = column + 0.5`, `v = row + 0.5`. Landmarks are indexed by anchor, settlement areas and linework by visible overlap, and conflict tags by their displayed tag boxes.

In Blender use one Blender unit per metre. X is east, Y is north and Z is up. Import the [regional terrain GLB](../../Lowmark_Terrain/terrain.glb) and the [existing local refinements](../../Lowmark_Terrain/Local_Refinement/) at their original scale and origin. Blender's glTF importer gives them the expected XY basis. The images overlay those meshes in top orthographic view at the indexed global XY. Their Z is an adjustable reference display height.

In Blender's Python Console load the placement helper once, then call it for each sector you need:

```python
import runpy
place = runpy.run_path(r"C:/Users/CK/Documents/Caelmor-Repo/CODE/Scripts/terrain_generation/place_blockout_sector.py")["place_sector"]
place("D03")
place("E03", source="svg")
```

The helper creates north-up image empties at the exact indexed centres and accepts optional `z` and `opacity` values. The SVG option rasterizes the sector's actual viewport and packs the image into Blender. Keep work that needs editable layers in a vector editor. Curve import in Blender has limited support for SVG viewports, labels and paint styles.

For manual placement or PGS, set a centred square reference to **384 × 384 m** at `center_x_m, center_y_m`, or use `x_min_m, y_min_m` for a southwest-origin tool. For example, D03 spans X 1152–1536 and Y 768–1152, with its image centre at (1344, 960). SVG coordinates stay in the master basis `(X, −Y)`, with viewBox `x_min_m -y_max_m 384 384`. Crossing vector paths retain their source coordinates and continue to the sector viewport.

Labels at an edge are clipped with the artwork so adjoining sectors reassemble as drawn. Use the CSV for the full names and the master sheet for the legend and conflict explanations.

## Regenerate and check

From the designated checkout in PowerShell, with the pinned terrain tool dependencies installed:

```powershell
$env:PYTHONPATH = 'CODE/Scripts/terrain_generation/.scratch/deps'
py -3 -X utf8 CODE/Scripts/terrain_generation/build_blockout_planning_map.py --sectors-only
```

For a fresh dependency setup use `py -3 -m pip install --target CODE/Scripts/terrain_generation/.scratch/deps -r CODE/Scripts/terrain_generation/requirements.txt`. The normal `Generate-Lowmark.ps1 -Local` pipeline refreshes the master and all sectors together. The sector-only command checks the master against the current generated artwork and leaves the terrain files untouched.

The generator verifies SVG and PNG dimensions, quadrant lines, shared-edge source paths and the full-resolution PNG mosaic against the master frame. To repeat the separate native Blender placement test:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.0/blender.exe' --background --factory-startup --python-exit-code 1 --python CODE/Scripts/terrain_generation/tests/verify_blockout_blender.py
```

## Verification

- The 72 SVGs total **1,438,296 bytes**, the 72 PNGs **2,407,018 bytes**, and the 72-row CSV **13,139 bytes**.
- A second sector-only run reproduced all 145 generated files byte for byte.
- Independent readback checked each ID, viewport, centre, and PNG size. The **3,456 × 3,072 px** mosaic matched the master SVG's geographic frame at one pixel per metre, with zero differing RGB pixels. Its RGB pixel buffer has SHA-256 `54aa57dedc4077278d2ff4e0ea5a019ce0399de5c51dacbbd7369b4c5aa1d63d`.
- Across **127 shared edges**, 500 intersecting contour, waterway and route paths retained their original coordinates on both sides. Rendering each SVG on its own produced minor rasterization differences from the PNG crop, with at most 0.217% of pixels differing and a maximum mean error of 0.016 per 8-bit channel.
- **Native Blender 5.0.1** placed D03 from its PNG and E03 from its SVG. Both were 384 m square and met at **X = 1536 m** over the imported 8 m regional and 2 m Crestbridge–Drowsebank meshes. Terrain raycasts hit at both centres and the shared edge. Direct SVG-to-curve import applied its own scale and included paths outside the viewport, so the helper uses the viewport raster for placement.
