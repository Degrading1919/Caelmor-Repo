# Lowmark mathematical terrain foundation

The Director approved a **3,456 × 3,072 m working frame (10.616832 km²)**. The regional grid remains **8 m**, with **433 × 385 samples** from the southwest origin. Three **2 m** refinements cover the Crestbridge–Drowsebank corridor, Greyharrow and Reedmere. The 384 m sectors and 192 m quadrants are a planning overlay. Terrain generation produces a continuous region and the same three local patches.

## Regenerate

Run from the designated checkout with PowerShell 7, Python 3.13, Blender 5.0.1 and Unity 6000.5.5f1.

```powershell
./CODE/Scripts/terrain_generation/Generate-Lowmark.ps1 -Local -InstallDependencies
./UNITY/Inspect-Terrain.ps1 -Build
```

Omit `-InstallDependencies` after the first run. The pinned tools install into the ignored checkout-local scratch directory. Use `-Blender <executable>` to select an installation. The full offline run includes regional and local tests, repeat generation, independent inspection, Blender GLB exports and all seven local renders, and the main planning SVG/PNG. The Unity command bakes the verified grids into the isolated inspector, validates its saved scene, builds the Windows inspector and runs the standalone walk smoke test.

Edit [regional controls](lowmark_controls.json) and [local controls](local_controls.json), then regenerate. The original [planning map](../../../MEDIA/Maps/Lowmark_Planning_Map.png) and [thematic map](../../../MEDIA/Maps/Lowmark_Thematic_Map.png) retain their original pixels and hashes. [Source notes](SOURCE_NOTES.md) explain the working offsets, the headwater radius changes and the authority of the maps.

## Outputs and checks

| Output | Current geometry or result |
| --- | --- |
| Regional natural and open-bed heightfields, watershed labels, contours, 16-bit PNG and 32 m OBJ preview | One metric frame, X east and Y north. Float arrays are the hydrology authority. |
| Regional terrain GLB | 166,705 vertices, 331,776 triangles. Every vertex matched to the source grid, with maximum vertical error below 0.000008 m. |
| Regional independent drainage | Natural, engineered-open and saved float32 open surfaces each route all 166,705 samples to the single declared outlet. Boundary-weighted watershed area is 10,616,832 m². |
| Conditioning and static flood screen | Maximum raise 7.343 m against the unchanged 12 m limit. Stillwater Fen retains wet and dry surfaces. The orchard scenario connects 45.8% of the field to the river at +1.5 m, with 72.3% of the berm area outside the case. |
| Local GLBs, heightfields, candidate plots, views and Unity payload | 380,559 owned 2 m samples across three patches. Exact parent seams, checked outflow and composite drainage. See [local details](LOCAL_README.md). |

[Planning sheet](../../../MEDIA/Maps/Lowmark_Blockout/Lowmark_Blockout_Planning_Map.md) · [Hydrology and routes](../../../MEDIA/Maps/Lowmark_Terrain/hydrology_and_routing.png) · [Regional verification](../../../MEDIA/Maps/Lowmark_Terrain/verification.json) · [Mesh verification](../../../MEDIA/Maps/Lowmark_Terrain/mesh_verification.json) · [Execution log](../../../MEDIA/Maps/Lowmark_Terrain/execution.txt).

The source arrays increase east by column and north by row. Blender uses X east, Y north, Z up. The terrain GLB uses X east, Y up, −Z north, and the Unity inspector uses X east, Y up, Z north. The 16-bit PNG has a 2.57 mm quantization step and loses some strict dry-bed D8 routes. Preserve the float arrays and validate any future resampling or tiling.

The original Caelmor synthesis uses authored channels as immutable conditioning seeds and a priority queue to raise trapped terrain within a budget. The conditioning approach draws on Priority-Flood. [Barnes, Lehman and Mulla (2014)](https://rbarnes.org/sci/2014_depressions.pdf)

The 8 m screens distinguish footprint eligibility, wet ground, engineered corridors and normal/+1.5 m exposure. They are approximate capacity checks. The default footprint sizes, development thresholds and population targets remain planning assumptions. Route grades measure the ground profile before structure design. The static water model preserves the natural fen outlet and separately marks the Uphill Canal's authored positive-head exception. It does not simulate pulses, draft or operating gates.

The [local geography review](LOCAL_REVIEW.md) and [conflict register](../../../04_CONTENT_PRODUCTION/Zones/Caelmor_Lowmark_Terrain_Narrative_Conflict_Register.md) record the distances and unresolved quest requirements for the compact layout.
