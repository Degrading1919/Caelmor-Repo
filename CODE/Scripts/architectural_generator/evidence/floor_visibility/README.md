# Floor-separated architectural presentation — v0.16

New buildings have independently hideable visual floor sections. Construction
families, source geometry, materials, functional programs and collision proxies
are retained. This is asset organization and client presentation, not an
interior-generation or navigation system.

## Visual evidence

- [Clay: full / ground-floor preview / restored](floor_clay.jpg)
- [Materials: full / ground-floor preview / restored](floor_material.jpg)
- [Three-storey floor progression](three_storey_progression.jpg)
- [Exact settings, volume elevations, measurements and render-source hashes](metrics.json)
- [Measured image differences](pixel_comparison.json)
- Individual 800×600 PNGs remain alongside the sheets, including unsplit
  `*_legacy.png` controls and every occupied upper-floor preview.

Matched captures hold seed, camera, lighting, materials and geometry settings
constant, using the existing world evidence studio. Three manual Lowmark
fixtures cover 1–3 storeys; the construction-library Smithy and Gatehouse cover
independent World volumes, curved construction and functional programs. World
programs retain their actual storey arrangements rather than inheriting manual
`floors` blindly. The control is the same source with separation disabled.

Root and independent review found the removal/restoration readable in both
clay and materials, with no obvious open cuts or assembled exterior seams at
these cameras. Image comparison and exterior ray checks support that limited
observation. Existing exterior shells remain empty where interiors do not exist.
The Smithy's lower stock-range roof can stay visible while previewing its taller
forge hall because it lies below that ceiling. Selecting the stock-range volume
uses its own cutoff. Gatehouse wings likewise retain their own elevations.

## Implementation and authoring

The adapter partitions finished Blender meshes after atlas/UV/material binding,
before the staged collection swap. Walls, posts, opening frames and details
crossing storey planes are clipped into real visual portions, not assigned by
origin. Closed solids receive caps; surface skins stay surfaces. Existing
UV0/atlas/detail UVs, colors, material indices and exterior normals interpolate;
UV1 lightmap charts are repacked. Semantic flues remain ALWAYS visible. Legacy
four-strip chimney walls can be split without filling their central void.
The final band above the last ceiling is unoccupied gable/attic geometry.

Roof layers, roof construction roles and independent zero-clearance flat
weather surfaces are separately controllable COVERING groups. Unhosted World
access assemblies, including Lowmark steps and Mire decks, retain their original
empty world-zone association and use render-only shared/ALWAYS ownership with
zero occupiable floors. No host or enterable area is fabricated.

In Blender, select a building, choose **Simulated floor** (-1 exterior, 0 ground)
and **Construction volume**, then **Apply Floor Preview**. This changes visual
hide flags only; Exterior restores prior states. Protected section edits and
manual material replacements survive regeneration. Source IDs remain available
alongside stable section IDs. Artist-transformed protected sections retain
their assigned visual ownership and need review if moved across floors.

Old saved settings without `floor_separation` explicitly load as False. To
migrate: Load Selected Settings, enable Floor-separated visuals, regenerate All
Layers. Switching representation with protected sections fails safely. Disabling
separation with section-specific material-slot overrides also fails instead of
silently merging/dropping artist finishes; restore those slots or keep separation.

## Export and client dependency

Hierarchy: persistent building root → volume → visibility/floor → construction
sections. Source/section/building IDs, roles, floor indices, bounds and schedules
survive GLB reimport. `floor_presentation` is an additive version-1 sidecar
extension. Collision is exported independently. Full visual exports remain
complete during interior preview, then restore mesh, parent and root hide flags.
The [packaged-install Lowmark demo](../../dist/floor_visibility_demo.glb), its
[sidecar](../../dist/floor_visibility_demo.caelmor.json) and separate collision
GLB are retained. This extra default-UI fixture includes shared access geometry.

Heights are building-local Blender Z metres, mapped to local Y by standard
Y-up GLB conversion. Unity components for each volume must share the common
building-root coordinate basis; importing extras requires an importer binding.

The Systems Engineer added opt-in `FloorVisibilityBuilding` and
`LocalFloorVisibilityPresentation` components under `UNITY/Assets/_Project/World/`.
With explicitly authored occupancy boxes and occupiable bands, the local camera
shows FLOOR sections starting below the selected ceiling, COVERING sections
wholly below it, and ALWAYS sections. Other building IDs are unaffected. Dwell
and hysteresis stabilize transitions. Per-render snapshots restore original and
externally changed renderer states, including during nested camera callbacks.
The code does not disable objects, collisions, interactions, simulation, network
state or persistence.

**Remaining dependency:** the current playable scene has no generated-building
metadata importer, authored enterable areas or multi-level player navigation.
Exports intentionally contain `occupancy_areas=[]`; footprint or elevation never
implies occupancy. Bind imported nodes to renderers and author actual interior
areas before connecting the adapter to a player. The scene remains untouched.
No end-to-end imported-building/player traversal, multiplayer client test,
rendered URP/camera-stack test or runtime-performance claim follows from the
isolated component validation.

## Asset measurements

| Fixture | Triangles before / after | Vertices before / after | Meshes = primitives before / after | GLB MB before / after | Materials |
| --- | ---: | ---: | ---: | ---: | ---: |
| lowmark_1f | 17,784 / 18,040 | 11,660 / 11,868 | 24 / 28 | 4.78 / 4.84 | 11 unchanged |
| lowmark_2f | 29,932 / 31,702 | 19,618 / 20,922 | 26 / 37 | 8.46 / 8.75 | 12 unchanged |
| lowmark_3f | 23,052 / 25,504 | 15,108 / 16,828 | 24 / 41 | 6.46 / 6.85 | 11 unchanged |
| smithy_wings | 14,483 / 14,959 | 11,369 / 11,821 | 77 / 83 | 4.82 / 4.96 | 14 unchanged |
| thornfell_gatehouse | 73,870 / 76,972 | 53,042 / 55,698 | 155 / 188 | 18.22 / 18.87 | 11 unchanged |

Primitive counts are glTF primitives, not measured draw calls. Splitting raises
renderer/primitive counts; triangles increase at real cut boundaries and caps.
Existing material and texture allocations are reused. These are asset costs,
not evidence of faster rendering. No arbitrary polygon budget was imposed.

## Verification and reproduction

See [verification](verification.json), [isolated installation](install.json) and
[isolated Unity component checks](unity_client_validation.txt).

From `CODE/Scripts/architectural_generator`, with Blender 5.0.1:

```text
python -m unittest discover -s tests -p test_floors.py
python -m unittest discover -s tests -p test_generator.py
python -m unittest discover -s tests -p test_architectural_benchmarks.py
blender --factory-startup -b --python-exit-code 1 --python tests/test_floor_blender.py -- --render
blender --factory-startup -b --python-exit-code 1 --python tests/test_floor_edges_blender.py
blender --factory-startup -b --python-exit-code 1 --python tests/test_construction_blender.py
blender --factory-startup -b --python-exit-code 1 --python tests/test_construction_depth_blender.py
python tests/compose_floor_visibility.py
python verify_install.py --region LOWMARK --function FARMHOUSE --report evidence/floor_visibility/install.json
```

Native checks cover five fixtures, 594 exterior rays each, floor bounds, stable
IDs, material/UV identity, unchanged collision, export while previewing and GLB
reimport, protected edits, slot overrides, scoped regeneration, safe migration,
the preview operator and saved `.blend` reopen. Targeted tests cover exact-plane
ownership, manifold post caps and normals, neutral cap colors, semantic
continuity, hybrid-roof UVs and material-override migration rejection. Historical
construction/depth lifecycle suites explicitly retain unsplit settings alongside
the new section-aware suites.

## Corrections, review and limits

Native testing caught empty clipped-part cleanup ordering. Installation caught
unhosted access geometry; it now has explicit shared ownership. Independent
review caught hidden parent groups not being restored after export; all export
ancestors are now snapshotted and tested. Client review corrected height-axis
mapping and per-render state restoration. A restore image differed by one
8-bit quantization step; checks record and tolerate that bound.

Cut caps sample adjacent construction UVs, not separately authored end-grain
artwork. Section boundaries can slightly alter texture interpolation at a small
number of pixels; see the measured record. Custom nonmanifold solids, modifiers
crossing storeys, artist-transformed groups and unusual imported hierarchies need
separate review. This bounded pass does not claim a twenty-type native matrix,
complete playable interiors or Creative Director artistic acceptance.

RSMV floor-separated exported models motivated this asset organization. They
are not evidence of RuneScape's internal visibility implementation. No RuneScape
meshes, textures or source were copied into this feature.
