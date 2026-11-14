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


## Timber Study review candidate

Open [the editable Timber Study](Lowmark_Brookoak_RoofShingles_TimberStudy.ptex) in Material Maker 1.7. The native graph at revision 88 adds board-local longitudinal fibers and growth curvature, randomly selected knots with local fiber deflection, directional splits, broken wear on exposed butts, and separate warmer timber and pale exposed-wood colors. The lap and shifted edges remain the primary height structure. Normal derives from that same height and roughness blends the detail signal with the weathering field. The albedo reads the shared surface fields and adds no rendered lighting. Fasteners have been left out of this study.

The Remote Controls node groups riven grain, growth-ring influence, knot relief, split strength, butt chips, board variation, pale exposed wood, relief-driven roughness, lap relief and normal intensity. The two final color gradients set the timber and pale-weathered palettes. Knot selection is set by the dark-to-light threshold in Colorize 3. Scratches length, width and layers control the split mask. The native board fill supplies deterministic placement. Grain follows the length of each board. Changing the eight-course layout or board seed requires generator re-registration.

- [Matched Blender comparison](Lowmark_Brookoak_RoofShingles_TimberStudy_comparison.jpg) uses a neutral sphere, grazing-light plane and 6.4 × 3.55 m roof slope at the registered physical UV scale. Each pair shares camera, light, geometry density and a 33 mm displacement range. The roof slope is a controlled test surface at the add-on fixture’s approximate scale.
- [Channel comparison](Lowmark_Brookoak_RoofShingles_TimberStudy_channels.jpg), [2×2 repeat](Lowmark_Brookoak_RoofShingles_TimberStudy_repeat.jpg) and [1024px native sphere](Lowmark_Brookoak_RoofShingles_TimberStudy_native.png). The V repeat falls on a strong lap and the fixed board-tone cadence is visible over a broad surface. The edges continue across the U join.
- Native export produced 2048 × 2048 sRGB albedo, tangent +Y normal, linear roughness and linear height. A second export after saving matched all four SHA-256 digests. The exported albedo, downsampled to the native 1024 preview, averaged 0.27/255 absolute RGB difference. Normal directions agree with the signed height derivatives on both axes. The EXR roughness range is about 0.69–0.95. Strict validation passed with two catalog warnings for native gradient parameters on Fill to Gradient and Radial Gradient. Both gradients are serialized and render.
- Roof AutoComplete commit `0169d96` uses 1.28 m U, eight 0.30 m courses per V repeat, 38 measured side-joint centers, and an exact registered albedo hash. The study retains the course and perimeter warp settings and their seeds. A local peak check around the registered joints found a median shift of zero and maximum of three 1024-equivalent pixels. The new albedo changes the hash. The registered files remain in use pending visual acceptance and a coordinated registration change with 0%, 50% and 100% detail checks.
- The board-local wood subgraph sits upstream of lap and gap assembly. It is a practical starting point for a modeled-shingle companion. A standalone preview still needs local UV input and a material branch that excludes the roof field's perimeter and lap relief.
- The study improves wood identity and coordinated channel response. At grazing angles, some fibers remain too parallel and smooth, knots read as small pits more than open whorls, and butt wear is subtle. The reference's fractured edges, broad gouges and varied abrasion remain stronger. This is pending Creative Director visual review. No Unity or installed add-on test used the candidate.

The user-provided sphere and texture-map screenshot was used as a visual benchmark only. SHA-256 `b24cc8eedfb9bfb535176beec9bcbbf71131b4b2faa13e0643e747e4994673b03`. The screenshot is excluded from the repository. The graph and rendered outputs are original Caelmor procedural work.
