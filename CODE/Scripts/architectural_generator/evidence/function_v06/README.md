# Function-first architectural study — v0.6

This README indexes the focused v0.6 study of four building functions across Caelmor’s four regions. The linked standard sheets are intended to compare each selected function in Lowmark, Thornfell, the Mire, and Emberholt using clay front/rear and material front/rear views. These exterior studies are for reading function and regional treatment; they do not establish interior completion, gameplay readiness, player experience, or final art approval.

## Selected function sheets

| Function | v0.6 sheet | Historical v0.5 comparison |
|---|---|---|
| Smithy | [PNG](https://github.com/Degrading1919/Caelmor-Repo/blob/codex/architectural-generator/CODE/Scripts/architectural_generator/evidence/function_v06/contact_sheets/smithy.png) | [v0.5 Smithy](https://github.com/Degrading1919/Caelmor-Repo/blob/codex/architectural-generator/CODE/Scripts/architectural_generator/evidence/archetypes_v05/contact_sheets/smithy.png) |
| Market Hall | [PNG](https://github.com/Degrading1919/Caelmor-Repo/blob/codex/architectural-generator/CODE/Scripts/architectural_generator/evidence/function_v06/contact_sheets/market_hall.png) | [v0.5 Market Hall](https://github.com/Degrading1919/Caelmor-Repo/blob/codex/architectural-generator/CODE/Scripts/architectural_generator/evidence/archetypes_v05/contact_sheets/market_hall.png) |
| Stable | [PNG](https://github.com/Degrading1919/Caelmor-Repo/blob/codex/architectural-generator/CODE/Scripts/architectural_generator/evidence/function_v06/contact_sheets/stable.png) | [v0.5 Stable](https://github.com/Degrading1919/Caelmor-Repo/blob/codex/architectural-generator/CODE/Scripts/architectural_generator/evidence/archetypes_v05/contact_sheets/stable.png) |
| Gatehouse | [PNG](https://github.com/Degrading1919/Caelmor-Repo/blob/codex/architectural-generator/CODE/Scripts/architectural_generator/evidence/function_v06/contact_sheets/gatehouse.png) | [v0.5 Gatehouse](https://github.com/Degrading1919/Caelmor-Repo/blob/codex/architectural-generator/CODE/Scripts/architectural_generator/evidence/archetypes_v05/contact_sheets/gatehouse.png) |

## Compact regional proof sheet

The planned initial functional proof sheet selects one regionally anchored example per function: Lowmark Smithy, Thornfell Market Hall, Mire Stable, and Emberholt Gatehouse. Each column is titled with its function and region; rows show clay front/rear and material front/rear.

[Functional proof PNG](https://github.com/Degrading1919/Caelmor-Repo/blob/codex/architectural-generator/CODE/Scripts/architectural_generator/evidence/function_v06_pilot/contact_sheets/functional_proof.png)

The pilot uses source revision metadata from its per-function manifests (base revision `fa0597a` with the `v06-pilot` suffix). The contact sheet is a compact initial study, not a second rendering pipeline.

## Comparison settings and provenance

The fixed comparison settings are seed 91, ESTABLISHED wealth, STANDARD craftsmanship, age 35, maintenance 0.7, MEDIUM detail, EFFICIENT geometry, World construction and Regional Grammar on, and context AUTO. The standard gallery shows all four regional settings for each selected function. The proof sheet shows the four function/region pairs listed above. Context resolves from each manifest’s region setting.

Individual renders remain under each gallery’s `individual/<function>/` folder. Per-function manifests record source revision and hashes, settings, geometry and validation metadata, and view metadata. Contact sheet manifests record included image hashes and dimensions. A missing, failed, invalid, hash-mismatched, or wrongly sized view is represented as a labeled placeholder rather than substituted.

The completed comparison contains **16 configurations, 64 individual PNGs and four
4316 × 3080 contact sheets**, with no invalid combinations or substitutions.
The clay pass is for reading massing and silhouette; the material pass exposes
regional surface treatment. These are flat studio previews, not settlement or
terrain presentations. Final Creative Director art acceptance remains separate.

## Validation and retained history

See [verification.json](verification.json) and
[the executed validation record](../../tests/V06_VALIDATION.md). All 16 native
Blender mesh-gate geometry hashes agree with the comparison records. The complete
historical v0.5 gallery remains unchanged: 320 individual images and 20 sheets
verified against its retained manifests. It was not rerendered.

The first integrated source is `905e97b`; the later Thornfell forge and access
corrections are `1286d07`. Only the five affected configurations (20 frames)
were refreshed. The other eleven retain their original 44 image files, camera
scale and render source snapshots. Per-record source metadata takes precedence
over a manifest's latest refresh header. Eleven retained settings
were replayed against current geometry; material and studio sources are unchanged.
This establishes geometry correspondence, not pixel identity across source revisions.

Independent visual review first rejected the hidden Thornfell forge and then
confirmed its hearth, hood, anvil and outside flue were exposed after correction.
The [rejected Thornfell views](../function_v06_rejected_thornfell/) and the initial
pilot remain historical comparisons. Early pilots used working-tree snapshots
based on `fa0597a`, whose hashes are recorded; they are not falsely described as
committed source trees. Only the final comparison uses the two committed revisions
above.

To verify the recorded delivery without rendering or rebuilding the old gallery:

```powershell
py -3 tests/verify_household_evidence.py --functional-gallery
```

To reproduce the four-function study in a separate folder, from the generator
directory with Blender 5.0.1 and the current v0.6 source:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.0\blender.exe' --factory-startup --background --python-exit-code 1 --python tests/render_household_review.py -- --archetype-gallery --gallery-functions SMITHY MARKET_HALL STABLE GATEHOUSE --gallery-output function_v06_reproduction --source-revision 1286d07
./tests/compose_archetype_gallery.ps1 -Gallery function_v06_reproduction -Functions @('SMITHY','MARKET_HALL','STABLE','GATEHOUSE')
```
