# Selectable openings and flat PBR finishes

| Blender comparison | What to inspect |
| --- | --- |
| [Window fit](window_fit.jpg) | The ordinary Cottage sash from `cc72e49` and the corrected assembly at identical scale, plus a narrower guided window. The front, oblique and reverse clay views expose the previous head, sill and side gaps independently of the glass shader. |
| [Independent placement](opening_move.jpg) | One ordinary window moves 0.50 m in the same wall. Its neighbor keeps its position. The guide window on the return is also editable. |
| [Mapped PBR finishes](mapped_finishes.jpg) | Flat roof covering, wall finish and plinth in clay and with assigned PBR maps. The posts, jamb studs, sash, sill, shutters, fascia and roof deck retain thickness. |

The proxy was 8.40 × 6.25 m with its eaves at 3.35 m, on the Lowmark Cottage's ground floor, seed 17 and the normal Medium detail setting. The test assigned the existing Caelmor Brookoak RivenBake shingles, maintained lime plaster, maintained oak and fieldstone PBR channels from the repository. Their albedo maps are 2048 × 2048, 2048 × 2048, 2400 × 1000 and 2048 × 2048 respectively. The movable window also has a separate weathered oak sash. The artist's materials are loaded into the test, and the masters are unchanged.

Blender 5.0.1 exercised native selection, placement, conflict rejection, wall ray checks, individual materials, regeneration and save/reopen. There were zero unobstructed rays across a 21 × 21 grid from each side of each assembled opening, sampled over 98% of its width and height. A separate ray check hit the rebuilt wall at the old edge of the moved aperture and found clear passage through its new edge in the visual wall mesh. The other ordinary window retained its generated Blender objects. Guided placement updated the existing source and preserved its ID.

The fixture had 114 authoring meshes and exported 27 visual nodes with 28 material primitives before and after the moves. The extra primitive accommodates the distinct sash material. The GLB was reimported with the same visual section identities and UVs. Floor groups and collision remain separate. The Unity 6000.5.5f1 Editor test passed 1,862 checks with current production Blender exports, covering guide additions, guide and ordinary-window position edits, removals, native IDs, placed prefab identity and unrelated overrides.

The geometry comparison for the recommended Lowmark Cottage produced 10,210 triangles against 22,043 with the legacy representation on the same seed and Medium settings. Nine pairs across four regions passed geometry validation, including the Cottage, functional Lowmark buildings, the Thornfell Gatehouse, and Mire and Emberholt cases. The standalone Roof AutoComplete regression checks the default flat cover and explicitly requested legacy percentages on the authored wall kit.

The contextual placement tool supports ordinary domestic openings and the existing guided Lowmark Cottage workflow. Functional passages remain fixed by their program. Direct viewport placement for posts and braces is outside this milestone. Old saves retain their current association and representation. A legacy-to-production conversion is a deliberate new asset and may require reconciling an authored Unity placement. Deliberate changes to a consolidated renderer's material-slot layout remain subject to the Unity importer's compatibility checks.

## Reproduce

```powershell
$root = 'CODE/Scripts/architectural_generator'
$blender = 'C:/Program Files/Blender Foundation/Blender 5.0/blender.exe'
$env:CAELMOR_COMPONENT_VIEWS = '1'
& $blender -b --factory-startup --python-exit-code 1 --python "$root/tests/test_selectable_openings_blender.py"
py -3 "$root/tests/compose_selectable_openings.py"
$env:CAELMOR_GUIDED_PRODUCTION = '1'
& $blender -b --factory-startup --python-exit-code 1 --python "$root/tests/export_guided_updates.py"
```

Run the existing [Unity Editor guided-update verification](../wall_feature_guides/README.md#reproduction) against those Blender revisions.
