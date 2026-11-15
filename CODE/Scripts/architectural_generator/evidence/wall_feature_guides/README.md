# Wall feature guides and Unity asset updates

[Editable cottage](wall-features.blend) · [Existing façade](wall-before.jpg) · [Guided post and plaster loss](wall-directed.jpg) · [Clay reveal detail](plaster-reveal-clay.jpg)

On the same cottage and camera, an edge relocates the principal post at one
bay. The revised frame schedule seats the bearing member between the sole and
roof plate and feeds both frame supports and diagonal bracing. The retained
window limits available framing stations. An irregular face defines lower
wall render loss and exposes sound earthen infill. The existing PBR treatment
uses a continuous finish across the cut coat, keeping clipped stock pieces
from reading as triangles. The depth comes from the wall cross-section and
the chip outline comes from the source face.

The examples use documented timber frame and infill principles. Repeated
wetting can loosen render or infill, and sound backing can survive local
finish damage. The visual interpretation here keeps that backing intact. See
[Historic England on timber framed walls and infill](https://historicengland.org.uk/advice/your-home/maintain-repair/walls/),
[Historic England on repair and finish detachment](https://historicengland.org.uk/advice/technical-advice/flooding-and-historic-buildings/repair-and-emergency-works/repair/),
and the [National Trust’s recorded timber frame](https://heritagerecords.nationaltrust.org.uk/HBSMR/MonRecord.aspx?uid=MNA118411).

## Verification

- Blender 5.0.1 verified guide placement, a conflicting post edit, variant
  selection, reversible plaster movement, stable guide IDs and unrelated
  geometry, save/reopen, removal and GLB round-trip. Measured near-normal
  rays hit the exposed daub about 20 mm behind the plaster face. The guided
  wall export retained five collision objects, including the floor.
- The original Opening Guides lifecycle and the five native floor-visibility
  cases passed. The Python generator and construction library suites passed
  20 tests. The packaged add-on passed an isolated Blender install.
- Unity 6000.5.5f1 completed 2,186 assertions in an independent Editor run.
  The same key went through 29 → 36 → 36 → 29 renderers as the window and
  doorway were added, edited and removed. Collision went 5 → 6 → 6 → 5.
  The post and plaster phase added two renderers and kept five colliders.
  The test checked actual retained Unity GUIDs and fileIDs, live and reopened
  scene placement, artist material overrides and guard rejections. It also
  verified retained identity after a legacy-suffix, guide-free refresh and
  byte/content stability on identical reimport. Existing scene files were
  unchanged.

Keep shared materials and textures available across iterations because authored
placements can reference them. They remain in the ownership ledger even when a
new renderer revision stops using them. Renderers and colliders above are asset
diagnostics. The [executed settlement benchmark](../lowmark_settlement/PERFORMANCE.md)
measured submissions and memory separately from geometry density.

## Reproduction

Run from the checkout in PowerShell. The export script produces revisions of
one building in `dist/guided_update_check`, including the two wall features.
The Unity regression uses a disposable prefab variant and placed scene.

```powershell
$blender = 'C:/Program Files/Blender Foundation/Blender 5.0/blender.exe'
$unity = 'C:/Program Files/Unity/Hub/Editor/6000.5.5f1/Editor/Unity.exe'
& $blender -b --factory-startup --python-exit-code 1 --python CODE/Scripts/architectural_generator/tests/export_guided_updates.py
& $blender -b --factory-startup --python-exit-code 1 --python CODE/Scripts/architectural_generator/tests/test_wall_feature_guides_blender.py
& $unity -batchmode -nographics -quit -projectPath (Join-Path $PWD 'UNITY') -executeMethod Caelmor.Unity.Editor.ArchitectureValidation.ValidateGuidedOpeningUpdates -logFile (Join-Path $PWD 'UNITY/Logs/architecture-guided-editor.log')
```

## Limits

The guide host is a fitted Lowmark Cottage. The structural edge describes a
vertical, sole-to-plate post. Plaster loss reveals sound daub in a rendered
timber bay. Masonry render loss, detached laths, arbitrary curves and genuine
structural damage remain outside this pilot. Unity compatibility covers guided
updates of a retained building structure. Existing artists’ references to
parts being removed must be moved or cleared before reimport. The checks use
the Unity Editor and do not establish player traversal or a frame-time result.
