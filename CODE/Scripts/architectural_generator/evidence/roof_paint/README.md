# Roof paint at gameplay distance

[Three-way comparison](comparison.png) · [Render and verification record](manifest.json)

The Smithy's roof should read as split timber shelter over an open working bay. The Gatehouse roof should read as cleft mineral stock while leaving the stone passage as the main cue on the road approach. Both are art proposals for the existing Caelmor buildings and use the same seed 91 studio gameplay view as the [painted material baseline](../painted_materials/README.md). The reference for the regional brief is the [Lowmark dossier](../../../../../LORE/Regions/Caelmor_Region1_LowmarkVale.md) and [Thornfell dossier](../../../../../LORE/Regions/Caelmor_Region2_ThornfellMarches.md).

The private Fort Forinthry Workshop slate diffuse makes broad groups of cool tiles and light course lips visible before any lighting is applied. Its luminance changes about 2.7 times as much vertically as horizontally between adjacent texels in the sampled texture. Its repeating UVs and normal map support the same direction. The useful lesson is to compose broad values and let a selective edge signal explain the lap. Caelmor's roof covering already has modeled courses, repairs, and separate roughness and normals. The study uses those existing construction cues and original colors. The published evidence contains only Caelmor imagery.

| Treatment | Lowmark Smithy | Thornfell Gatehouse |
| --- | --- | --- |
| Baseline | The roof reads as a broad tan mass. The shingles recede into the surface. | The cool roof separates from the wall. The dark faces read almost as continuous slabs. |
| Strong painted pigment | Warm and weathered tones break up the field. Pigment follows the fall, though uninterrupted streaks can make adjacent shingles read as a single surface. | Broad cool and grey groups make the slate legible in the shaded roof while keeping the roof planes quiet enough for the gate to lead. |
| Pigment with tile and edge treatment | Bounded stock and row variation, with warm exposed butts, makes the lap readable. The main roof looks more like assembled split timber. This is the stronger Smithy candidate. | Tile contrast creates a checkerboard on the high gable, and the added light lips compete with the hip and ridge. Prefer pigment alone here. |

The first candidate combines a broad field with directional marks. Lowmark uses longer marks down the fall and warm wood tones. Thornfell uses cross-course marks and cool mineral tones. The second candidate adds tile stock and course variation. It only adds the edge accent when the top face has an edge on the generator's actual course start. This leaves clip boundaries and concealed bedding outside the accent. The color still goes through the existing condition fields and atlas.

Both materials benefit from a visibly stronger base-color treatment. The Smithy's improvement is in the way the roof reads as built. For the Gatehouse, the roof becomes more legible, but stronger tile accents pull attention away from the entrance. Its large flanking masses and plain wall returns still set the limit on the building's silhouette. Further texture contrast will not change those relationships. If a later pass needs a stronger Gatehouse read, compare one massing or entrance change in clay with the selected roof finish held fixed.

Blender 5.0.1 reused the existing controls and produced four new frames, one per treatment and building. It built each case once and recoated the roof only. Geometry hashes and camera transforms matched the controls. Both treatments exported with the same texture bindings, normal and roughness/metallic payloads, and image count. The course treatment's reimport passed pixel and UV binding checks. A local check verified deterministic pigment and confirmed that moving a clipped face off a course start disables the edge accent.

| GLB bytes | Baseline | Pigment | Pigment with courses |
| --- | ---: | ---: | ---: |
| Smithy | 4,262,100 | 4,304,960 | 4,316,960 |
| Gatehouse | 16,508,572 | 16,599,300 | 16,607,840 |

The experimental finish modes are selectable through the study script and surface bake API. They are not generation defaults. **Pass** for the controlled technical study. **Evidence needed** for Creative Director acceptance and a second seed before broader use. The [procedural asset baseline](https://github.com/Degrading1919/lessons-learned/pull/3) guided the scope of rendering and verification.
