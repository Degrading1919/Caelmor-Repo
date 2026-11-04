# Internal implementation contract

Offline Blender tool, original Python geometry, no production game schemas or C#.
Units metres, Z up, footprint CCW. All mesh faces outward.

`model.py`: `Settings(seed=17, function='FARMHOUSE', footprint='L', width=11.0,
depth=7.0, wing_width=4.2, wing_depth=4.5, floors=2, floor_height=2.65,
pitch=48.0, overhang=0.45, detail='HIGH', window_density=1.0)` dataclass,
`make_plan(settings) -> Plan`. `Plan.settings`, `Plan.outline` [(x,y)],
`Plan.rects` rectangles `(x0,y0,x1,y1,axis)` where axis 'X'/'Y' is ridge direction,
`Plan.eave` (0.45+floors*floor_height), `Plan.roof_height(x,y)`,
`Plan.edges` pairs of exterior endpoints, `Plan.rng(label)` stable Random.
Footprints RECT/L/T/U. Main rectangle (0,0,width,depth); wings extend toward negative Y.

`geometry.py`: `MeshBuffer(name, material='timber', layer='structure')` contains
`vertices`, `faces`. `.box(center, size)` closed cuboid; `.beam(a,b,width,depth=None)`
oriented closed cuboid; `.prism(poly_xy,z0,z1)` convex polygon extrusion;
`.extrude(poly_xyz,vector)` convex polygon extrusion; `.cylinder(a,b,radius,segments=8)`.
`.face(points)` adds a polygon. All components closed solids unless stated.
`clip(poly,a,b,c)` returns convex XY polygon satisfying a*x+b*y+c>=0;
`area(poly)`, `lerp(a,b,t)`, `stable_seed(seed,label)`.

`facade.py`: `build_facades(plan) -> list[MeshBuffer]`. Author walls with real depth,
hole subdivisions (no blank wall behind windows), foundation, timber frame avoiding
openings, glazing/lead, shutters, planked door, chimney, details. Group buffers by
material and semantic layer. Legal layers foundation/walls/structure/windows/doors/details.
Plinth 0..0.45. Exterior wall frame follows outline; outward normal (dy,-dx)/length.
Nonenterable exterior only in this release. Root implements roofs, gable infill can
be in facade using roof_height along boundary. Labels material palette:
stone,stone_light,plaster,plaster_patch,timber,timber_light,roof,roof_patch,iron,glass,mortar.

`roof.py`: `build_roof(plan) -> list[MeshBuffer]`, root owner. Clipped analytic
upper envelope of intersecting gables, continuous skin, clipped tile courses,
ridge/valley/flashing and supporting rafters.

`engine.py`: `generate(settings) -> (plan,buffers)`; `validate(plan,buffers) -> dict`
raises ValueError on bad input. `geometry_hash(buffers) -> str`.

`blender_backend.py` agent owner: `build(settings, collection=None, layers=None)`
creates/replaces tagged buffers only in target collection. Shared PBR palette,
UV0 metric projection, UV1 packed lightmap, flat meshes, material tags, custom props.
`export_building(collection, filepath)` glTF + manifest/optional FBX; no claim of Unity validation.
`__init__.py` registration and sidebar UI (Generate New, Regenerate Selected with
layer scope, preserve manual untagged objects). Save settings in collection.
Root package imports bpy lazily so pure unittest imports work outside Blender.

Tests agent owns tests/, evidence render driver, README.md, THIRD_PARTY.md.
Do not publish git from subagents. Do not modify other agents' files.

## Construction treatments — proposal for Creative Director review

This section proposes an interface for the offline generator. The Director approved the seven treatment families below. The IDs, component mapping, defaults and export rules are proposed. The delivery checkout contains the Lowmark-only generator. The separate `Caelmor-Architecture` checkout contains the 0.12.2 reference used here, including `REGIONAL_GRAMMAR.md`, `WORLD_IMPLEMENTATION_CONTRACT.md` and the Thornfell Gatehouse export in `evidence/painted_materials`. The proposal uses the richer checkout as design evidence and treats the delivery checkout as an older compatibility case.

### Taxonomy

| Treatment ID | Eligible component roles | Construction cues and material constraints |
| --- | --- | --- |
| `stone_masonry` | `wall_body`, `plinth`, `arch_ring`, `vault` | Stone laid in bonded rubble or courses, with believable bedding, staggered joints and corner returns. An arch uses radial joints. |
| `dressed_stone` | `wall_body`, `plinth`, `arch_ring`, `vault`, `opening_trim` | Worked stone with fitted beds and controlled faces and arrises. Use shaped voussoirs at arches and fitted jambs or sills at openings. The same stone stock may serve both masonry treatments. |
| `structural_timber` | `frame_member`, `roof_support` | Wood posts, beams, braces or rafters with legible sections, bearing and joinery. Grain follows the member. |
| `wooden_boarding` | `wall_infill`, `boarding`, `roof_deck` | Wood boards with readable edges, seams and a local joint or overlap pattern. Examples include siding, floor boards, gate leaves and shutters. Use for a deck when it actually represents boards. |
| `wooden_shingles` | `roof_cover` | Split wood units in staggered, overlapping courses with legible eaves and ridges. |
| `slate_tile_roofing` | `roof_cover` | Slate or fired-clay units in lapped courses. Stock determines the section and edge profile, so flat slate and shaped clay can share placement rules. |
| `plaster_limewash` | `wall_infill`, `wall_surface` | Render infill or a plaster/limewash layer over a compatible host. Render can have thickness and chipped edges. Limewash follows the host and adds negligible relief. |

### Authoring and resolution

The planner supplies a stable component ID and `component_role` before a geometry or surface builder chooses a treatment. A function can request a wall, arch, beam, boarded leaf or roof assembly and constrain its dimensions, support and clearances. Every function uses the same treatment resolver. A roof declares separate support, deck and cover roles. A plastered masonry wall has a masonry body and a separate surface linked to that body. Mortar, flashing, hardware, glazing, anchors and collision proxies retain their existing handling. The existing layer, `semantic`, `structural_role` and `functional_role` retain their current meanings. In the reference Gatehouse export, `structural_role` defaults to `framing` for most objects, including stone pieces.

| Independent input | Proposed contract |
| --- | --- |
| Substrate and surface family | Resolve `substrate` as physical stock and `surface_family` as a compatible reusable shading family. Slate and clay both use `slate_tile_roofing`. A coating records its own lime/earthen stock or limewash and references the host component. Keep existing palette slots such as `stone_light`, `roof` and `roof_patch` for material binding. |
| Construction | Resolve one `treatment` per participating component. The treatment governs assembly and geometry cues. A mixed assembly is a set of components with their own roles and treatments. |
| Region and practice | Reuse region/context IDs and `AUTO` resolution. Local practice supplies candidate treatments, stock and details such as bond, board layout or lap. Regional defaults can differ by role within a single building. |
| Craft and preparation | Keep `craftsmanship` and `wealth`. Preparation controls hewing, dressing, stock sorting and tolerances within a selected treatment. Existing wealth/craftsmanship-driven style choices can supply defaults. An explicit compatible treatment remains selected when preparation or wealth changes. |
| Condition | Keep age and maintenance independent. Derive exposure from local practice and component orientation/shelter. Resolve repair locally, such as a replacement shingle cohort or repointed joints. Repairs inherit role and treatment unless a compatible change is explicitly authored. |
| Artistic finish | An optional `finish` reference selects the existing procedural/baked look or a compatible artist-authored surface. Finish changes affect shading or maps and their required UVs. They leave the assembly, support, aperture profile and physical condition inputs intact. |

Proposed settings shape is an optional `construction_overrides` object with optional `by_component` and `by_role` maps, keyed by stable component ID and the role IDs above. Each map value is an object with any of `treatment`, `substrate`, `surface_family` or `finish` as registered string IDs. Missing fields inherit. An empty `construction_overrides` opts in with defaults. Omit the object to keep the legacy path. This uses the current settings store and adds no external preset file. For opted-in components, resolve each authored field in this order.

1. Use an explicit component override, then an explicit role override scoped to the building. Omission inherits from the next level.
2. Use compatible defaults from the resolved local context, then the region. The existing regional style and function-specific requirements can narrow the candidates, such as a minimum bearing width at a passage or a continuous weather envelope at a roof.
3. Use an equivalent existing role/assembly default where one is known and supported. Otherwise retain the existing path for unclassified components or report an unsupported treatment request. An explicit incompatible value is an error and never falls through to a different treatment.

Resolve treatment and stock together against role, host and geometry constraints, then apply preparation, condition and finish. Use stable component IDs and named seed streams so a paint or patina change cannot reroll the assembly or layout. Keep `use_grammar`, manual dimensions, `world_aware`, roof style, `crafted_curves`, `seed_massing`, detail and `SOLID`/`EFFICIENT` behavior on the paths that already support them.

### Regional defaults and review fixtures

These are mappings of working art direction against the four dossiers. They do not establish material supply, trade or new regional canon.

| Region | Proposed role mapping and reference |
| --- | --- |
| Lowmark Vale | First review fixture. Use masonry for the plinth or smithy stack, timber for the frame, plaster for infill, boards for stock-range cladding and wooden shingles for the roof cover. Check a shared timber or roof role across two functions. The river and farm context supports practical materials and local repairs. |
| Thornfell Marches | Use the existing Gatehouse as a comparison fixture. Map the curtain and battered plinth to masonry, the fitted portal ring, jambs and vault to dressed stone, the wooden gate leaf to boarding and `SLATE` cover to slate/tile roofing. Keep the clear passage and arch profile, vault support and slate roof envelope. The reference's mixed stone stock and painted bevels are preparation and finish evidence. |
| Mire of Fallen Banners | Keep raised access and flood clearance from the stilt/risen-bank grammar. Timber support and boarding fit the raised construction. Preserve existing `REED` cover on its legacy path outside this initial taxonomy. Where the existing grammar selects `SHINGLE`, use wooden shingles. |
| Emberholt Heights | Use masonry or dressed stone for volcanic-stone walls and terrace edges, with fired clay under slate/tile roofing where existing practice selects `CLAY`. Keep forge exposure and soot local to the relevant components. |

The dossier sources are `LORE/Regions/Caelmor_Region1_LowmarkVale.md`, `Caelmor_Region2_ThornfellMarches.md`, `Caelmor_Region3_MireOfFallenBanners.md` and `Caelmor_Region4_EmberholtHeights.md`. Phase 1 and roadmap Stage 33 put the Lowmark slice first. The *Caelmor Material Research Review* sheets **Starter Library** and **Shared Surface Maps**, alongside `material_usage_named.csv`, support reuse of surface families across assemblies and finish variants. The scan measures material assignments and shared maps. It cannot establish construction geometry or Caelmor regional availability. All treatment IDs and stock references belong to the Caelmor authoring tool.

### Validation and compatibility

- Before geometry generation, reject unknown fields, unknown explicit IDs, invalid region/context pairs, incompatible role/treatment/stock or host combinations, unresolvable finish references and unsupported builders. A role override must be compatible with each matched component after applying component overrides. Identify the component, rejected field and allowed choices. Check existing numeric ranges and validate the candidate geometry before replacing the collection, including aperture clearance, bearing, cover continuity and the existing topology rules for the selected mode. A rejected request leaves the collection intact.
- Acceptance checks for a future implementation include repeatability at fixed settings and seed, a shared role resolving consistently across functions, the same stock in masonry and dressed stone, and slate and clay resolving under the same roof treatment. A finish-only change preserves vertex positions, faces and component identity. A repair-only change stays local. Check a Lowmark legacy farmhouse and the reference Gatehouse, and confirm the Mire reed path survives.
- Existing saved settings without the `construction_overrides` object resolve through their original compatibility path. Keep existing controls, material slots, UV conventions, datablocks and override behavior. Compare normalized settings for scoped regeneration, preserving the distinction between legacy and opted-in settings. Changes affecting multiple layers or support/cover geometry require full regeneration. Preserve protected buffers and artist overrides by stable buffer identity. Flag protected components that conflict with the new plan for manual reconciliation.
- Keep `CaelmorBuildingExport` format 1, existing field meanings and sidecar naming. For treatment-aware exports, propose optional per-object `component_role`, `treatment`, `substrate` and `surface_family` fields. Record resolved values from the generated object, including for protected pieces with known provenance. Omit values for unclassified or protected pieces whose classification is unknown. Emit a single classification only when it describes the whole object. Preserve existing grouping and omit ambiguous tags for mixed buffers. The source geometry hash still describes generated source geometry. Verify reader tolerance before emitting optional fields by default and retain the existing export shape for strict readers.

This section is the proposed authoring contract. Settings are Blender collection data and the sidecar is offline export metadata. No JSON Schema change is required for this proposal. The gameplay schemas and the economy worker interchange schema govern separate inputs.
