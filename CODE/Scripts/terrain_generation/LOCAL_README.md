# Lowmark local terrain and walking inspection

Three **2 m** patches refine the 8 m regional surface in the approved **3,456 × 3,072 m** frame. Run `Generate-Lowmark.ps1 -Local` from this tool directory or follow the [full procedure](README.md) from the checkout root.

| Patch | East / north bounds (m) | Grid (east × north) | Scope |
| --- | --- | --- | --- |
| Crestbridge–Drowsebank | 1104–2208 / 552–1440 | 553 × 445 | Crossing, provisional Hall and Depot, race and yard |
| Greyharrow | 2800–3376 / 520–1040 | 289 × 261 | Side-branch settlement and approaches |
| Reedmere | 56–536 / 1456–1944 | 241 × 245 | Wet fen shore and conditional raised floors |

The 2 m source meshes share their parent elevations at the outer edges. Local edit budgets and actual post-edit terrain, candidate footprint clearance and road grades are checked independently. At the exact mesh triangles, the sampled Drowsebank leat stays wet with a minimum static centreline depth of **0.651 m**; wheel head remains **0.95 m**. Neither value establishes barge draft or pulses. All nine tested local route/patch combinations meet the 10% ground-grade screen on the eligible portions outside water gaps. Regional grades and crossing requirements are recorded separately.

| Site | Regional normal / +1.5 m ground capacity | Local normal / scenario floor candidates |
| --- | ---: | ---: |
| Crestbridge | 84 / 79 | 107 / 107 |
| Drowsebank | 5 / 5 | 7 / 7 |
| Greyharrow | 18 / 15 | 29 / 27 |
| Reedmere | 25 / 0 | 0 dry / 33 conditional stilts |

The 2 m pass uses a different footprint lattice and checks all samples within each footprint, so these columns are feasibility screens with different methods. Reedmere retains wet ground. Its three 10 × 8 m inspection floors are raised above the normal reference stage plus 1.5 m and 0.3 m clearance. Connected boardwalks and evacuation remain unbuilt.

## Inspect

- [Blender scene](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/local_inspection.blend), [Crestbridge relationships](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/Views/crestbridge_relationships.png), [Drowsebank](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/Views/drowsebank_local.png), [local capacity](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/local_capacity.png).
- [Local metrics](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/local_metrics.json), [independent saved-data verification](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/local_verification.json), [walking inspector validation](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/unity_validation.txt).
- Build and smoke-test with `./UNITY/Inspect-Terrain.ps1 -Build`, or open `UNITY/Assets/_Project/World/TerrainInspection/LowmarkTerrainInspection.unity` and press Play. WASD and the mouse walk and look, Shift sprints, and 1–4 select the four starts. Walk speed is 3 m/s in this technical fixture.

The inspector uses the separately owned composite and 2 m grids. It validates terrain mesh collision at four starts and 168 patch-interface probes. The technical bridge deck has a 2.67 m maximum approach gap. Separate structure and approach design is required. The inspector's water strips indicate reference stages visually. It does not feed the gameplay scene.
