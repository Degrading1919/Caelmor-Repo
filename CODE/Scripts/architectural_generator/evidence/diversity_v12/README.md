# Five-seed construction study

## Matched comparisons

| Function | Five-seed sheet |
| --- | --- |
| Lowmark Smithy | [Before and after](smithy.png) |
| Thornfell Gatehouse | [Before and after](gatehouse.png) |

The columns are seeds 7, 17, 19, 91 and 408. Each column shows the same seed and camera in clay and material. The other inputs stay fixed at established wealth, standard craftsmanship, age 35, maintenance 0.7, medium detail, Efficient geometry and Crafted Curves enabled. Both stages use Blender 5.0.1 and the existing benchmark studio. The [before manifest](before/manifest.json) pins the v0.11 source and exact settings. The [after manifest](after/manifest.json) records the revised source, settings, individual front and rear renders, construction zone diagnostics and hashes. The [sheet manifest](sheets.json) identifies each input frame.

## Baseline and changes

The v0.11 Smithies all share the same forge hall and side shed. The five Gatehouses all share the same portal and paired hipped towers. Seed changes are visible in finishes and small details, with little difference in massing or roof hierarchy.

**Smithy.** Site width and weather change the forge hall span, height, pitch and whether its gable is swept. Growth changes stock depth and frontage setback. Storage demand governs the stock bay width, whether it has an independent cross-gable or a simpler shed, and whether it needs an intermediate bent. The ramp terminates at the resulting entrance and the handling lane follows the bay. The hearth and exterior exhaust retain their working arrangement.

**Gatehouse.** Road width sizes the actual vault, iron grille, paving, thresholds and portal shoulders together. The guard wings can share a low skyline or raise one forward lookout above its neighbor. Hipped and gabled roofs and the direction of the central ridge change the silhouette. The early Blender pass exposed crossing roof planes, projecting corner stones and gallery openings that lost headroom as the wings got lower. Party-wall roofs now maintain their height order, corner courses follow the full roof soffit, and guard wings retain enough height for their openings and casing.

| Seed | Smithy profile | Gatehouse profile |
| ---: | --- | --- |
| 7 | Swept forge and set-back shed | Forward west lookout and low east hip |
| 17 | Straight, steeper forge and narrow shed | Paired gabled wings and hipped portal |
| 19 | Broad swept forge and deepest frontage setback | Broad vault and paired hips below a longitudinal ridge |
| 91 | Narrow straight forge and broad cross-gabled stock bay | Forward east lookout with tall gable |
| 408 | Swept forge and cross-gabled stock bay | Paired low hips beneath a transverse central roof |

All ten layouts have different construction signatures within their respective five-seed cohorts. The Smithy variants still read as siblings with a shared working front. The largest differences are the profile of the forge and the shape and setback of the stock bay. For the Gatehouse, the shift between a paired skyline and an offset lookout is the strongest difference. The core layouts remain recognizable in both clay and material.

**Compatibility.** The new **Seed Changes Layout** control applies to the world-aware Lowmark Smithy and Thornfell Gatehouse. New Blender scenes enable it by default. Older saved building settings and direct Python calls that omit the field retain the previous layout. Changing the option on an existing building calls for full regeneration so walls, roofs, routes and collision proxies are rebuilt together.

The comparison measures construction diversity within two architectural families. The material pass uses the existing palette and surface pipeline. Creative Director review determines artistic acceptance.

## Verification

- Thirteen Python tests passed across the seed-massing, construction curves and architectural benchmark suites. They verify deterministic replay, roof arrangement, the straight Solid alternatives, support and clearance constraints, and exact legacy geometry hashes for all ten controls and 78 earlier regional fixtures.
- [Native mesh checks](benchmark_mesh_checks.json) passed on all ten revised buildings with the atlas bake skipped for the geometry-only test. Actual Blender BVHs recorded 270 clearance rays, 160 stair headroom rays, 20 arch probes, 75 exhaust probes and zero glazing overlaps. Material renders and export checks use the full pipeline.
- The seed 91 variants passed [GLB and texture round trips](export_validation/export_checks.json). The Smithy also passed save/reopen, protected-edit retention, material override retention and scoped regeneration. An [isolated Blender install](install_check.json) generated a new Smithy with both layout and curve controls enabled.
- The five new Smithies range from 9,308 to 11,482 authoring vertices. The five Gatehouses range from 42,896 to 48,448. These are Blender-side counts.

## Reproduce

Run the renderer inside Blender using the source for the desired stage. The published baseline is immutable. The command below captures both front and rear views for the revised generator. The compositor verifies source images, paired camera transforms and matching settings.

```powershell
blender --background --factory-startup --python-exit-code 1 --python tests/render_diversity.py -- after <source-revision> --rear
./tests/compose_diversity.ps1
```
