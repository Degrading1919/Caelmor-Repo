# Lowmark local terrain and inspection milestone

Milestone date: **November 7, 2026**. Regional source baseline: `3ec4003`.

Three deterministic **2 m terrain patches** refine Crestbridge/Hall/Depot/Drowsebank jointly, Greyharrow and Reedmere, retaining the 6,144 × 4,992 m regional frame. They support site inspection and bounded terrain tests. They do not establish a finished settlement, compact civic layout, hydraulic operating model, architectural placement or quest/navigation implementation.

## Regenerate

From the designated checkout in PowerShell 7:

```powershell
./CODE/Scripts/terrain_generation/Generate-Lowmark.ps1 -Local
```

Use `-InstallDependencies` on the first run. Python 3.13, the pinned checkout-local packages and Blender 5.0.1 are used; `-Blender <executable>` selects another installation. `-InspectionSamples 24` increases render samples from the default 12. `-Local -SkipMesh` runs numerical generation/review without producing new Blender renders or GLBs.

The command reruns the regional checks, builds local arrays, executes local regressions and independent saved-array review, renders actual terrain in Blender, adds labelled captions and verifies every local GLB vertex against its saved array. Temporary work stays in the ignored `.scratch` directory. Author inputs are [local_controls.json](local_controls.json); the regional inputs remain separate. [LOCAL_REVIEW.md](LOCAL_REVIEW.md) records source-backed geographical conflicts and Director options.

## Inspect in 3D

These are actual Blender camera renders of the saved terrain, at **1:1 elevation scale**. Labels and captions identify fixed anchors, conceptual proxies and unresolved links; they do not replace terrain pixels.

| View | What to inspect |
|---|---|
| [Crestbridge elevated valley](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/Views/crestbridge_broad_elevated.png) | Crossing, fixed Hall/Depot positions and the surrounding valley together. |
| [Ground approach](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/Views/crestbridge_ground_approach.png) | Eye 1.75 m above the retained approach road, 140 m before its analytical river intersection. |
| [Civic relationships](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/Views/crestbridge_relationships.png) | True distances/elevations between crossing, conceptual granary example, Hall and Depot. |
| [Greyharrow](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/Views/greyharrow_local.png) | Side-branch banks, candidate access and sparse foundation tests. |
| [Reedmere](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/Views/reedmere_local.png) | Wet ground, natural access and conditional raised-floor tests. |
| [Reedmere floor detail](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/Views/reedmere_floor_detail.png) | Three neutral floor/pile tests; clearance is conditional, with ground left unfilled. |
| [Drowsebank](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/Views/drowsebank_local.png) | Race, working head and adjacent bank space. No building is placed on the mill marker's channel bed. |

Open the saved [Blender inspection scene](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/local_inspection.blend) to orbit the same geometry and cameras. Individual terrain-only meshes are [Crestbridge/Mill](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/crestbridge_mill.glb), [Greyharrow](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/greyharrow.glb) and [Reedmere](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/reedmere.glb). The GLBs contain neutral terrain, not the inspection boxes, bridge supports or architectural assets. The `.blend` additionally contains static reference water, road coverage and the clearly labelled proxies.

The bridge proxy follows the actual retained road/river intersection, approximately 60 m from the unchanged regional `crest` hydrology node. It is an unapproved scale/deck example. Other water-contact gaps remain unbuilt. The granary box has **no approved site XY** and is excluded from terrain grading and capacity. The Depot box is an entrance/area marker, not a surface depot building.

## Walk in the isolated Unity inspector

The Windows inspector was built and its automated player smoke passed. Run
`UNITY/Builds/TerrainInspection/CaelmorTerrainInspector.exe` in this checkout,
or regenerate/build it with `./UNITY/Inspect-Terrain.ps1 -Build`.
Build outputs stay ignored; the scene, baked payload and source are tracked.
[Executed native/build/player evidence](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/unity_validation.txt)
records four spawn checks, 168 interface probes, persistence, 3 m/s movement
at 60 and 10 FPS, and preservation of the technical fixture/build settings.

The native inspection scene is [LowmarkTerrainInspection.unity](../../../UNITY/Assets/_Project/World/TerrainInspection/LowmarkTerrainInspection.unity), in the existing `UNITY` project. Open that scene in Unity 6000.5.5f1 and press Play. It reads a baked inspection payload from the verified terrain; it is separate from the playable technical fixture and authored world scenes.

- WASD walks at **3 m/s**; Shift uses the optional 5.5 m/s inspection sprint.
- Hold right mouse to look; release it or Escape to release the cursor.
- `1` Crestbridge approach, `2` Greyharrow, `3` Reedmere, `4` Mill; Home returns to the approach.
- `5` places the inspector on the technical bridge deck. Its measured approach gap is **2.56 m**, exceeding the controller's 0.3 m step: ramps/crossing access are unresolved, so the deck is not claimed walkable from the road.

Native batch validation executed real terrain collision at four spawns, 168 interface probes, saved-scene reopening and a one-second CharacterController walk of **2.999933 m**. Existing technical-fixture files and configured build scenes remained unchanged. These checks establish native inspection geometry and movement, not a human playtest, quest traversal, swimming, navigation or the unresolved civic layout. The Unity eye height is 1.62 m; the Blender ground-view camera uses its separately recorded 1.75 m eye offset.

## Terrain, capacity and access findings

| Site | Proposed roofs | Normal-stage footprint candidates | +1.5 m scenario floor candidates | Interpretation |
|---|---:|---:|---:|---|
| Crestbridge | 60–100 | 114 | 114 | Core envelope can accommodate the proposed range in this screen; remote Hall/Depot functionality remains unresolved. |
| Greyharrow | 28–50 | 39 | 38 | Supports the lower/middle range under these assumptions; 50 is not demonstrated. |
| Drowsebank Mill | 4–10 | 5 | 5 | Lower end only; machinery, pond/wheel, spur and ancillary programme are not laid out. |
| Reedmere | 12–24 | 0 dry candidates | 0 dry candidates | 55 **conditional stilt** candidates; raised floors, piles, connected walks and evacuation still require design. |

These are postprojection complete-footprint tests on the actual local surface, not authored building counts. They use a different resolution/lattice from the regional screen, so the count differences are not a controlled terrain-improvement comparison. Only sparse foundation examples are graded; no buildings or final parcel plan are generated. The connected +1.5 m stage scenario and 0.3 m floor-clearance screen are planning assumptions, not flood-frequency or structural certification.

Road checks measure the final 2 m surface away from declared water-contact gaps. The retained approaches in the reviewed local run remain below the 10% cart-grade screen there; the largest reported grade is about 6.81%. This does not make the gaps into bridges or prove complete navigable routes. Reedmere retains its wet-ground/stilt policy.

Static centreline tests found no dry points on the reviewed local watercourses. The corrected Drowsebank leat still reaches only about **0.136 m minimum static depth**, below the 0.2 m target at its shallowest point. It is explicitly a remaining shallow reach, not proven barge draft or discharge capacity. The 0.95 m mill working head establishes a drainage relationship, not barge passage through the wheel race.

## Verification and artifact boundaries

The three patches contain 927,747 samples and 1,849,344 triangles. Their outer borders match the regional edges exactly in global coordinates. Crestbridge and Mill share one patch; independent patch ownership does not overlap. Bounded banks, roads, foundation tests and the dedicated inherited leat-bed correction preserve canonical junction samples, source stages and approved XY anchors. The separate composite records allowed interior regional-vertex changes; the original regional inputs are not overwritten by local refinement.

The reviewed local arrays have no interior sinks; their exits have checked continuations to the regional outlet. The composite conserves all 480,625 regional samples to that outlet. Surface checks use the published SWNE triangles rather than assuming bilinear interpolation has the same drainage. Scene rendering and GLB export read these persisted arrays. Numerical regeneration, mesh verification, batch engine execution and a human walking inspection are distinct evidence levels.

- [Actual capacity/exposure overlay](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/local_capacity.png) and [Crestbridge terrain sections](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/crestbridge_sections.png).
- [Local metrics](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/local_metrics.json): timings, budgets, routes, static depths and footprint outcomes.
- [Independent persisted-array review](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/local_verification.json).
- Mesh reviews: [Crestbridge/Mill](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/crestbridge_mill_mesh_verification.json), [Greyharrow](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/greyharrow_mesh_verification.json), [Reedmere](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/reedmere_mesh_verification.json).
- [Render metadata](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/render_metadata.json) and [image fingerprints](../../../MEDIA/Maps/Lowmark_Terrain/Local_Refinement/Views/image_verification.json).

Observed performance and sizes belong to the saved metrics/render metadata, not runtime frame-rate claims. Observed runs took about 16–19 s for local generation and 65–80 s for Blender export, seven 1600 × 1000 Cycles views at 12 samples and scene saving; the latest exact times are in the saved metadata. The three terrain GLBs total 44,461,836 bytes; the compressed inspection `.blend` is 54,251,761 bytes. Every local vertex and SWNE face was checked; maximum elevation error is below 0.00000382 m.

## What still requires a decision or production work

Crest Hall remains about 652 m from the town anchor and **640 m from the retained natural river**. A better approach road does not provide its authored direct water-gate or the bridge's nearby north stair. The Depot remains about 837 m from the river; roughly 4.14 m gross ground-to-water head across that distance does not establish the authored chute/high-bank exit. No canal, waterfront annex, long tunnel or moved anchor has been invented to conceal those conflicts.

The western Whisperflow topology, fen's natural outlet versus quest closure, distinct mill-to-Cut spur/navigation, Reedmere's raised access system and the Uphill Canal's local storage/levels remain explicit review items in [LOCAL_REVIEW.md](LOCAL_REVIEW.md). The canal's anomalous positive head is retained without an invented pump explanation.

**Ready for further terrain/site inspection and Director review.** The milestone is not a locked settlement-assembly plan or a complete quest geography. The next consequential ruling is Crestbridge's Hall/river/granary arrangement, informed by the true-scale views.
