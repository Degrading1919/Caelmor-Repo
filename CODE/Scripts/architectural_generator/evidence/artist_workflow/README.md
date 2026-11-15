# Artist workflow verification

The new Caelmor sidebar routes from the actual selected object. Creation uses one dialog for starting style and sizing. Edits begin from the selected building's saved inputs. The selected part or group supplies the scope of material and construction changes. An optional advanced draft is bound to a building and expires when its saved choices change.

## Executed checks

- Blender 5.0.1 artist workflow. Recommended Cottage creation, manual Thornfell dimensions, a rotated Lowmark proxy, and a Mire proxy fitted to its raised floor datum. Changed the Lowmark roof to hip, set pitch and overhang, and chose slate. Applied a window finish to a section and a roof finish to its construction group. Checked protected mesh coordinates, rejected a stale edit, added/moved/removed a window guide, and verified that save/reopen and regeneration replayed the correct material and roof choices.
- The material-only export retained its visual node identities, floor metadata, and byte-identical collision GLB. The separate Unity 6000.5.5f1 guided update regression passed 2,186 Editor checks with current Blender export fixtures, including retained native asset identities and authored overrides.
- Native blockout, opening, timber/plaster guide, and standalone roof regressions passed. The standalone test exercises selection-based load, rectangle and compound bearing, diagonal rejection, progressive shingles, and GLB round-trip. Diagonal rejection now uses a controlled wall fixture. The mutable local artist scene is recorded as a diagnostic.
- Twelve direct geometry checks respected manual main dimensions across Lowmark, Thornfell, Mire, and Emberholt. The matrix used hip Cottages, Market Halls, and Stables. The extension archive passed Blender validation.
- The broader `test_world.py` run reports three Thornfell Gatehouse gallery-deck failures for Modest, Established, and Affluent. All three failures reproduce on the initial `91a7a68` sources.

The new hip-roof workflow exposed chimney flashing that crossed two roof planes as a single warped solid. The corrected apron follows each actual roof plane. Adjoining volumes still have to clear each other when an artist changes a roof or envelope.

The focused workflow is verified through native Blender operators and contextual layout checks. The cases cover one upright box per fitted main volume. The forge and gate passage keep their own working bay sizes. Wall feature placement remains available on box-fitted Lowmark Cottages.

```powershell
Set-Location CODE/Scripts/architectural_generator
$blender = 'C:/Program Files/Blender Foundation/Blender 5.0/blender.exe'
& $blender -b --factory-startup --python-exit-code 1 --python tests/test_artist_workflow_blender.py
```
