# Lowmark Cottage authoring pilot

[Editable Blender sample](blockout-cottage.blend) · [Regional defaults](cottage-default.jpg) · [Artist-directed finish and joinery](cottage-directed.jpg)

Both images use the same orthographic camera, lighting, seed 17 and Lowmark
Brookhollow settings. The source is a single upright box with an 8.31 × 6.25 m
footprint, 3.35 m height and 0.41 rad heading. The second view uses a role-wide
foundation finish, a selected framing component's oak finish with rotated
metric UVs, and a selected roof support's timber profile. The finish images
are generated for the fixture. The Blender scene is saved after translating,
rotating and widening the source box to 8.81 m and refitting.

## Verification

- Blender 5.0.1 verified the box fit and source preservation, rejected a tilted
  source, replayed role and component inputs through full and scoped regeneration,
  checked deterministic source geometry and protected window retention, and tested
  that a conflicting resize left the prior building in place.
- The saved Blender scene retained the source link and the component edits.
  The GLB round trip checked world bounds, UV0, diffuse and normal image
  bindings, floor metadata, and the absence of the source box. The visual GLB
  was about 4.3 MB with a separate five-mesh collision export.
- Unity 6000.5.5f1 imported the exported fixture through the existing architecture
  editor importer under a disposable asset key. Its import record contained
  29 renderers, 5 colliders, 13 materials, 27 textures and 19,080 rendered mesh
  triangles. This exercised Editor import and prefab creation. Player runtime
  behavior and a live Substance graph were outside the verification fixture.
- The extension installed with isolated Blender preferences. The Python
  generator and construction-library suites passed (20 tests). Native
  construction-library and floor lifecycle tests passed. Roof AutoComplete's
  rectangular geometry and export checks and its synthetic two-volume valley
  case passed. Its optional local `test_scene.blend` failed the expected diagonal
  rejection assertion in unchanged roof selection and test code.
- The wider Python World suite reported three Thornfell Gatehouse gallery-deck
  failures, one per wealth tier. The same three failures reproduced using the
  starting revision `51a7f33`.

## Reproduce

From the repository root in PowerShell, run the native check. Set
`CAELMOR_BLOCKOUT_CHECK_DIR` to an empty scratch destination inside the
checkout to retain the scene and GLBs, and set `CAELMOR_BLOCKOUT_RENDER=1` to
also render the matched views. With neither variable, the check uses and
removes a temporary directory under `dist`.

```powershell
$blender = 'C:/Program Files/Blender Foundation/Blender 5.0/blender.exe'
& $blender -b --factory-startup --python-exit-code 1 --python CODE/Scripts/architectural_generator/tests/test_blockout_authoring_blender.py
```

## Geometry and runtime boundary

Modeled, hybrid and texture-dominant construction remain authoring choices.
The [executed settlement benchmark](../lowmark_settlement/PERFORMANCE.md)
measured a 2.1% difference in wide-view submitted triangles between minimum
and maximum roof detail, with no consistent timing gain. Submission grouping
showed a larger timing benefit, while BC compression reduced referenced
texture memory. A future semantic LOD representation would need to preserve
silhouette edges, compatible material sharing, stable floor and visibility
grouping, and independent collision. Optional displacement would require
predictable UVs and a mesh density and boundary policy. The pilot uses the
existing geometry and PBR representations.
