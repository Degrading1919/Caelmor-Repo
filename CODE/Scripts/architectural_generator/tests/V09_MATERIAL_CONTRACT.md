# Procedural surfaces and independent condition — 0.9

Mission: improve surfaces of the accepted-direction Lowmark Smithy and Thornfell
Gatehouse without redesigning their architecture. Follow the lessons-learned
procedural asset baseline: small causal comparisons, inexpensive numeric gates,
actual PBR/export inspection, independent critique, then release verification.
No new props, furniture, interiors, terrain, vegetation, building catalog or game
systems. Generation functions, mesh positions, topology and semantic functions
remain the 0.8 implementation.

## Independent causes

| Input | Surface meaning | Must not imply |
|---|---|---|
| Wealth | Grading/sorting of timber and stone, knot/outlier selection, regional material investment | Cleanliness or absence of age |
| Craftsmanship | Preparation relief, adze/plane work, dressed stone, burnished/oiled finish | Age or household wealth |
| Age | Material maturation, exposure, retained patina | Automatic ruin |
| Maintenance | Reduced accumulated dirt/corrosion; stressed shingle replacements, joint repointing and local limewash | Resetting an old building to new |

Environmental history uses building-local metres, host foundations/eaves, actual
facade apertures and generated fire/chimney roles. Moisture follows low contact,
exposed roof butts and sill drips. Grain follows each existing metric long-axis
projection. Connected pieces share stock variation across faces. No arbitrary
rectangular dirt/repair cohorts or fake masonry joints are painted over real
construction. Existing roof joints and masonry geometry provide the jointing.

Regional dossiers remain authority: Lowmark's agricultural/river-trade work,
Thornfell's exposed stone highlands, the Mire's wet raised settlements, and
Emberholt's volcanic craft industry. Exposure coefficients, one prevailing-rain
direction, maturation curves and finish recipes are reversible artistic
interpretations, not new canon, conservation advice or physical simulations.
Only the two benchmark families receive full new visual comparisons here;
numeric regional-pattern coverage does not approve all regional materials.

## Technical invariants

Keep editable metric and lightmap UVs; add a separate padded surface atlas.
Bake original albedo, tangent normal and packed roughness/metallic fields so the
finish survives actual GLB export. Albedo PNG is sRGB, normal/ORM linear, ORM G
roughness and B metallic; R is constant one, not computed ambient occlusion.
Follow the [Khronos glTF 2.0 material contract](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#materials).
No reference texture or external asset is copied. New code remains under the
existing GPL-3.0-or-later license. NumPy is bundled with Blender.

Cache by source geometry, metric UVs, settings, palette, context and atlas
revision. Reuse identical datablocks, preserve manual node edits and explicit
slot replacements, and never recoat protected pieces. Include retained fire
sources in condition context during full/protected/scoped regeneration. A scoped
atlas may repack; compare its bound surface appearance, not its bank name.

## Observable comparison and gates

Fixed seed91, established/standard, age35/upkeep0.7, medium/efficient, the same
two v08 reference meshes, cameras, lighting and image dimensions. Keep the
historical v08 material captures immutable. Use normal and close exterior
frontage views. The fixed-geometry surface sweeps explicitly isolate finishes;
normal production still applies its existing wealth/craft construction rules.

Pairs: ages5/120 with upkeep0.7; upkeep0.15/0.95 at age120; modest/affluent with
age35/upkeep0.7; rough/fine at age35/upkeep0.7; modest-maintained and
affluent-neglected at age120. Show both default before/after and control pairs.
Do not count a different texture hash as a legible artistic improvement.

Order: vector sampler and causal-field tests; small actual render inspection;
correct weak surfaces; matched final captures; geometry hash regressions;
native texture/UV/pixel export-reimport, regeneration/protection and saved reopen;
isolated package installation. Verify image/source/archive hashes at freeze.
No Unity/runtime testing or new performance benchmark is part of this mission.
