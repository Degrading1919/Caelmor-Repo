# Roof AutoComplete verification

Blender 5.0.1. The target is a substitute 6 × 4 m shell assembled from the
existing Lowmark `wood_trimmed_plaster` modules in the working art directory.
The fixture includes a doorway, a side window and trimmed modules. It does
not use the Director's assembled farmhouse. The test appends the source
meshes to a temporary scene in memory.

| Structural rise | Detail 0% | Detail 50% | Detail 100% |
| --- | ---: | ---: | ---: |
| 1.8 m | 1,413 | 1,695 | 2,318 |
| 3.0 m | 1,416 | 1,696 | 2,309 |

Counts are Blender mesh triangles at generation. The roof field keeps its
slope-aligned UVs and eight-course texture repeat while more courses become
physical geometry at the eaves. The GLB sample is the 3 m rise, 100% tier.
Blender reimport recovered 11 meshes and 2,309 triangles. The export retained
normals, UVs and base color, normal and roughness texture bindings.

- [Warm key](roof_warm_key.png) and [grazing key](roof_cool_key.png) show the
  2.4 m rise and 50% tier under the same camera.
- [Sample GLB](native_wallkit_roof.glb) and [executed report](roof_autocomplete_report.json).

From the repo root, with the local Lowmark wall kit available:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.0/blender.exe' --background --factory-startup --disable-autoexec --python-exit-code 1 --python CODE/Scripts/architectural_generator/tests/test_roof_autocomplete_blender.py
```

An in-memory roof-backend probe added a perpendicular 3 m wing overlapping
the main 6 × 4 m block. It produced 13 roof patches, two valley segments,
flashing and complete mapped-field UVs. This probe did not exercise wall
inference, wing gable infill, or a wing export. The operator accepts one
rectangle. A future wing workflow needs an explicit bearing and junction
check before the operator can generate it.
