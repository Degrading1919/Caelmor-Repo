# Lowmark Brookoak Roof Shingles

An editable Material Maker 1.7 roof-field study for Lowmark. Open `Lowmark_Brookoak_RoofShingles.ptex` and use the Remote Controls node at the left. Revision 76 is the reviewed native MaterialPilot graph.

| Control | Starting value | Effect |
| --- | ---: | --- |
| Course count | 8 | Number of courses in a V repeat |
| Minimum shingle width | 0.115 | Minimum width as a fraction of a U repeat |
| Side / butt edge irregularity | 0.012 / 0.017 | Horizontal joint wander and variation in exposed butt position |
| Riven grain strength | 0.32 | Amount of per-board directional wavelet grain |
| Lap relief | 0.37 | Weight of the down-course height ramp |
| Board color variation | 0.35 | Amount of per-board tone variation before the albedo ramp |
| Weathering scale across / down roof | 12 / 8 | Roughness patch scale and the noise driving the side-edge warp |
| Split strength | 0.28 | Weight of the sparse directional split marks |

Change the main Colorize gradient for regional palettes. The second Colorize gradient controls the roughness range. Keep the course count integral and check U/V repetition after changing controls or seeds.

## Deliverables and checks

- MaterialPilot exported 1024px base color and tangent-space +Y normal as PNG, and linear roughness and height as EXR. The Blender-profile export converts Material Maker depth into physical height, with higher values on raised faces. Actual roughness spans about 0.77–0.92. The normal directions were checked against both height gradients.
- `_iteration.png` shows the early 512px native plane. `_preview.png` is the delivered 1024px native plane. `_repeat.png` is a 2×2 albedo repeat. `_raking_light.png` uses the same four exports on a 2×2 Blender surface with a 3.5 cm height range under angled light.
- The courses and board faces continue across the repeat. The V boundary lies at a course transition, where a stronger lip remains visible under grazing light. The repeat cadence is visible across a large roof field.
- Strict MaterialPilot validation passed with one warning. The bridge catalog omits the native `grad` parameter on Fill to Gradient. That native gradient renders and is present in the source.
- For Unity, use the albedo as sRGB, import the normal via the Normal Map importer, and treat the scalar maps as linear. Smoothness is one minus roughness. The Blender displacement preview is an authoring check. Material binding, displacement support, and the gameplay-distance appearance on a Lowmark roof still need Unity verification.
- The material now has varied butts, wood grain, relief, and splits. Distinct knot whorls, chipped silhouettes, and localized ochre weathering from the reference remain future art work. Creative Director review is pending.

## Reproduction and reference

Use one live graph writer. Inspect the bridge capabilities and current revision, plan the node transaction, apply against the checked revision, and inspect a native 512px preview. Validate all channels, render a 1024px preview, and export only under this directory. MaterialPilot derives its save/export roots from its server working directory. For this pass a directory-scoped session shared the running native bridge while enforcing this directory as the write root.

The attached roof screenshot informed the lap, butt offsets, fiber direction, and weathering. User-supplied visual reference SHA-256 `97fa5c1f652a9e169672f69063a98246e4ac0f482f105b2eab5b31f6cb241929`. Distribution rights for the screenshot are unverified, so it is omitted from the repo and supplies no pixels to the asset. The graph and exports are original Caelmor procedural work. The [Split Oak Shingle working palette](../README.md#split-oak-shingle--recolorable-roof-working-test) is the repo reference for muted oak tones.
