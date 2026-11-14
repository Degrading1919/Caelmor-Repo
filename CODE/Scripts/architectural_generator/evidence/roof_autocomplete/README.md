# Roof AutoComplete coverage verification

Blender 5.0.1 on a 6 × 4 m test shell assembled from existing Lowmark
wood-trimmed plaster modules, including a doorway and a window.

| Structural rise | 0% | 25% | 50% | 75% | 100% |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1.8 m | 1,096 | 2,222 | 2,960 | 3,414 | 3,540 |
| 3.0 m | 1,096 | 2,582 | 3,578 | 4,190 | 4,348 |

All counts include the permanent roof assembly. At 1.8 m the modeled
shingle counts are 0, 142, 284, 426 and 568. At 3.0 m they are 0, 194,
388, 582 and 776. Selection stays nested across the five settings.
The 0% selection generates no modeled cover boards and the 100% selection
generates no flat cover field. The projected top cover area stays 31.49 m²,
and XY bounds and ridge height agree within 2 mm across tested detail levels.

The test compares wall mesh coordinates and world transforms, checks slope
UV direction and phase on flat and modeled surfaces, exercises preview,
generation, update and saved bearing reload, and checks repeat cleanup.
The 100% 3 m [GLB](native_wallkit_roof.glb) reimports as 7 meshes and 4,348
triangles. Its primitives have normals and UVs. Brookoak keeps the base
color, normal and roughness maps. See the [native report](roof_autocomplete_report.json).

| Render | 0% | 50% | 100% |
| --- | --- | --- | --- |
| Warm key | [0%](warm_0.png) | [50%](warm_50.png) | [100%](warm_100.png) |
| Grazing key | [0%](grazing_0.png) | [50%](grazing_50.png) | [100%](grazing_100.png) |

These renders use a fixed 2.4 m rise, camera, seed and Brookoak export.
Within each lighting condition only shingle coverage varies. Shared PBR
and UVs hold the pattern in place. The modeled side joints approximate the
painted curves with straight edges. Small differences can show at close range.

The connected [wall-kit wing](compound_wing.png) has a 6 × 4 m main
rectangle and a 2 × 2 m projection. It generated two valley segments and
flashing, with 5,008 roof triangles at 50%. Its inferred compound outline
survived loading and updating through the panel.

The local 'test_scene.blend' candidate has diagonal wall cores. On the exterior
wall selection used for the check, the operator reports Plane.005, Plane.008,
Plane.009 and Plane.010 at approximately 45° off-axis. This selection cannot
be covered by the orthogonal wing tool. Whether it matches the Director’s
original selection remains unverified. Correlate those named walls with the
original layout before deciding if diagonal bearing support is needed.
Visible spacing at the eaves and plain tall gable infill remain finishing
observations. The 6 m rise report comes from the Director’s Blender session.

Run from the repo root with the local Lowmark kit available:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.0/blender.exe' --background --factory-startup --disable-autoexec --python-exit-code 1 --python CODE/Scripts/architectural_generator/tests/test_roof_autocomplete_blender.py
```

The original 0.17.0 render pair remains in this directory as historical evidence.
