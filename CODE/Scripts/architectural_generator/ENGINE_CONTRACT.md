# Architectural generator engine contract

## Current offline implementation

The designated `main` checkout is the development and delivery baseline. [PR #85](https://github.com/Degrading1919/Caelmor-Repo/pull/85) and `22e4185` (tool revision 0.12.2) are historical references, including the bounded Thornfell curtain return study. Phase 1, the four regional dossiers and the roadmap govern project scope. This add-on authors offline Blender assets in metres with Z up. The glTF exporter emits Y up.

| Interface | Current contract |
| --- | --- |
| Planning | `model.py` validates `Settings` and resolves regional/manual dimensions and style. `profiles.py` provides region and context IDs, type specs and initial construction/cover choices. `world.py` builds optional multi-zone construction. Functional programs reserve workspaces, routes, openings and support before the regional shell. See [regional grammar](REGIONAL_GRAMMAR.md), [world interface](WORLD_IMPLEMENTATION_CONTRACT.md) and [functional programs](FUNCTIONAL_PROGRAMS.md). |
| Geometry and validation | `engine.generate(settings)` returns plan and buffers. `MeshBuffer` carries vertices, faces, material, layer and topology, with role, zone and support metadata where authored. Structural cores use closed geometry. Efficient skins may use `SURFACE` topology. Keep existing aperture, route, bearing, weather-envelope and collision-proxy checks. `validate(plan, buffers)` reports validity and source diagnostics. Roof support, deck, cover and trim remain distinct. |
| Surface | `materials.py` provides palette keys, reusable families and a readable legacy material bank. `surface_atlas.py` supplies fingerprinted packed albedo, normal and ORM, with condition and pigments evaluated from the actual host plan. Keep metric UV0, lightmap UV1 and `UV2_Surface` on the atlas path. Retain shader edits on reused datablocks and explicit artist material-slot replacements keyed by `caelm_buffer_id`. |
| Regeneration | `blender_backend.build` validates before staging and replaces selected generated layers in the target collection. It preserves untagged objects, skips protected generated buffers and reapplies explicit slot overrides. Scoped regeneration requires equivalent normalized saved settings. Settings that change the plan require all layers. |
| Export | `export_building` writes GLB or glTF and the existing `.caelmor.json` sidecar, with a separate collision GLB when proxies exist. Format 1 includes requested settings, architecture mode, construction zones, source validation and hash, and per-object material, layer, world zone, topology, semantic/role, roof and support diagnostics and protected state. Source validation describes generated geometry. Protected edits and Unity traversal require separate review. |

### Compatibility for older Blender scenes

The original manual Lowmark interface used orthogonal RECT/L/T/U plans, intersecting gables, exterior shells, roof and facade buffers, and named seed streams. These concepts survive in the current single-plan path. Normalize old snapshots to manual Lowmark, gable and `SOLID` where their corresponding fields are absent. Older snapshots omit `world_aware`, `crafted_curves` and `seed_massing` and keep those switches off. New Blender UI defaults and direct `Settings` defaults differ. Preserve that distinction. Exact historical geometry and material reproduction can require the original tool revision.

Keep full-section roof clearance, bearing and aperture checks in force when extending the surviving path. For timber this includes the projected section, deck underside and supporting fascia plane. For roof cover retain valid overlap/headlap and valley/ridge clearance in each topology mode. The earlier revision-specific dimensions, material revisions and test tolerances are available in Git history.

## Construction treatments

The Director approved the seven treatment families below. The implementation uses the following IDs, component mapping and settings. This section carries forward the contract changes from `4ae1d62`. See [the consolidation record](../../../00_ADMIN/Reference/Caelmor_Repository_Consolidation.md) for provenance and recovery refs.

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

The planner supplies a stable component ID and `component_role` before a geometry or surface builder chooses a treatment. Use existing zone/member keys where they identify a single component. Never derive a role from a Blender name, palette key or broad export layer. A function can request a wall, arch, beam, boarded leaf or roof assembly and constrain its dimensions, support and clearances. Every function uses the same treatment resolver. A roof declares separate support, deck and cover roles. A plastered masonry wall has a masonry body and a separate surface linked to that body. Mortar, flashing, hardware, glazing, anchors and collision proxies retain their existing handling. The existing layer, `semantic`, `structural_role` and `functional_role` retain their current meanings. In the reference Gatehouse export, `structural_role` defaults to `framing` for most objects, including stone pieces.

| Independent input | Proposed contract |
| --- | --- |
| Substrate and surface family | Resolve `substrate` as physical stock and `surface_family` as a compatible reusable shading family. Slate and clay both use `slate_tile_roofing`. A coating records its own lime/earthen stock or limewash and references the host component. Keep existing palette slots such as `stone_light`, `roof` and `roof_patch` for material binding. |
| Construction | Resolve one `treatment` per participating component. The treatment governs assembly and geometry cues. A mixed assembly is a set of components with their own roles and treatments. |
| Region and practice | Reuse region/context IDs and `AUTO` resolution. Local practice supplies candidate treatments, stock and details such as bond, board layout or lap. Regional defaults can differ by role within a single building. |
| Craft and preparation | Keep `craftsmanship` and `wealth`. Preparation controls hewing, dressing, stock sorting and tolerances within a selected treatment. Existing wealth/craftsmanship-driven style choices can supply defaults. An explicit compatible treatment remains selected when preparation or wealth changes. |
| Condition | Keep age and maintenance independent. Derive exposure from local practice and component orientation/shelter. Resolve repair locally, such as a replacement shingle cohort or repointed joints. Repairs inherit role and treatment unless a compatible change is explicitly authored. |
| Artistic finish | An optional `finish` reference selects the existing procedural/baked look or a compatible artist-authored surface. Bind it after construction and condition resolve. Finish changes affect shading or maps and their required UVs. They leave the assembly, support, aperture profile and physical condition inputs intact. An existing explicit slot override still wins at Blender binding. |

The settings shape is an optional `construction_overrides` object with optional `by_component` and `by_role` maps, keyed by stable component ID and the role IDs above. Each map value is an object with any of `treatment`, `substrate`, `surface_family`, `finish` or `variant` as registered string IDs. Missing fields inherit. An empty `construction_overrides` opts in with defaults. Omit the object to keep the legacy path. This uses the current settings store and adds no external preset file. For opted-in components, resolve each authored field in this order.

1. Use an explicit component override, then an explicit role override scoped to the building. Omission inherits from the next level.
2. Use compatible defaults from the resolved local context, then the region. Translate current style choices where they apply (`RUBBLE`, `ASHLAR`, `BOARD`, `TIMBER_INFILL`, `SHINGLE`, `SLATE`, `CLAY`). A composite style such as `TIMBER_INFILL` supplies separate frame and infill choices. World zones can carry distinct local assembly choices. Requirements such as passage bearing width or a continuous roof envelope constrain selection.
3. Use an equivalent existing role/assembly default where one is known and supported. Otherwise retain the existing path for unclassified components or report an unsupported treatment request. An explicit incompatible value is an error and never falls through to a different treatment.

Resolve treatment and stock together against role, host and geometry constraints, then apply preparation, condition and finish. Use stable component IDs and named seed streams so a paint or patina change cannot reroll the assembly or layout. Keep `use_grammar`, manual dimensions, `world_aware`, roof style, `crafted_curves`, `seed_massing`, detail and `SOLID`/`EFFICIENT` behavior on the paths that already support them. In World mode, preserve the zone's control of roof form and eaves.

### Regional defaults and review fixtures

These are mappings of working art direction against the four dossiers. They do not establish material supply, trade or new regional canon.

| Region | Proposed role mapping and reference |
| --- | --- |
| Lowmark Vale | First review fixture. Use masonry for the plinth or smithy stack, timber for the frame, plaster for infill, boards for stock-range cladding and wooden shingles for the roof cover. Check a shared timber or roof role across two functions. The river and farm context supports practical materials and local repairs. |
| Thornfell Marches | Use the seed 91 Gatehouse as a comparison fixture. Map the ordinary curtain and battered plinth to masonry, the fitted portal ring, jambs and vault to dressed stone, the wooden gate leaf to boarding and `SLATE` cover to slate/tile roofing. Keep the clear passage and arch profile, vault support and slate roof envelope. Compare the [bounded dressed curtain study](evidence/curtain_masonry/README.md) as an optional treatment precedent. Mixed stone stock and painted bevels are preparation and finish evidence. |
| Mire of Fallen Banners | Keep raised access and flood clearance from the stilt/risen-bank grammar. Timber support and boarding fit the raised construction. Preserve existing `REED` cover on its legacy path outside this initial taxonomy. Where the existing grammar selects `SHINGLE`, use wooden shingles. |
| Emberholt Heights | Use masonry or dressed stone for volcanic-stone walls and terrace edges, with fired clay under slate/tile roofing where existing practice selects `CLAY`. Preserve the existing iron-roofed work-range path outside these seven treatments. Keep forge exposure and soot local to the relevant components. |

The dossier sources are `LORE/Regions/Caelmor_Region1_LowmarkVale.md`, `Caelmor_Region2_ThornfellMarches.md`, `Caelmor_Region3_MireOfFallenBanners.md` and `Caelmor_Region4_EmberholtHeights.md`. Phase 1 and roadmap Stage 33 put the Lowmark slice first. The *Caelmor Material Research Review* sheets **Starter Library** and **Shared Surface Maps**, alongside `material_usage_named.csv`, support reuse of surface families across assemblies and finish variants. The scan measures material assignments and shared maps. It cannot establish construction geometry or Caelmor regional availability. All treatment IDs and stock references belong to the Caelmor authoring tool.

### Validation and compatibility

- Before geometry generation, reject unknown fields, unknown explicit IDs, invalid region/context pairs, incompatible role/treatment/stock or host combinations, unresolvable finish references and unsupported builders. A role override must be compatible with each matched component after applying component overrides. Identify the component, rejected field and allowed choices. Check existing numeric ranges and validate the candidate geometry before replacing the collection, including aperture clearance, bearing, cover continuity and the existing topology rules for the selected mode. A rejected request leaves the collection intact.
- Acceptance checks include repeatability at fixed settings and seed, a shared role resolving consistently across functions, the same stock in masonry and dressed stone, and slate and clay resolving under the same roof treatment. A finish-only change preserves vertex positions, faces and component identity. A repair-only change stays local. Check a Lowmark legacy farmhouse and the reference Gatehouse, and confirm the Mire reed path survives.
- Existing saved settings without the `construction_overrides` object resolve through their original compatibility path. Keep existing controls, material slots, UV conventions, datablocks and override behavior. Compare normalized settings for scoped regeneration, preserving the distinction between legacy and opted-in settings. Changes affecting multiple layers or support/cover geometry require full regeneration. Preserve protected buffers and artist overrides by stable buffer identity. Flag protected components that conflict with the new plan for manual reconciliation.
- Keep `CaelmorBuildingExport` format 1, existing field meanings and sidecar naming. For treatment-aware exports, support optional per-object `component_role`, `treatment`, `substrate` and `surface_family` fields. Record the resolved construction provenance from the object, including for protected pieces with known provenance. These fields describe the assembly and its selected source family even if an artist replaces the displayed material. Omit values for unclassified or protected pieces whose classification is unknown. Emit a single classification only when it describes the whole object. Preserve existing grouping and omit ambiguous tags for mixed buffers. The source geometry hash still describes generated source geometry. The exporter defaults to the existing field set for strict readers. Enable Construction Metadata (or pass `construction_metadata=True`) for both optional settings and object fields.

Settings are Blender collection data and the sidecar is offline export metadata. No JSON Schema change is required. The gameplay schemas and the economy worker interchange schema govern separate inputs.


### Implemented bindings and limits

Component IDs use `zone/slot`, with `main` for the single-plan path. See
`construction.py` for registered stock IDs and role constraints. Existing
regional grammar selects the initial assembly and roof forms before the
resolver runs. The initial builders classify participating wall bodies, plinths,
infill, optional coatings, opening trim, principal frames, board leaves and
decks, pitched roof support and covers, and the Thornfell Gatehouse portal and
vault. Boards can replace plaster in compatible framed bays. Masonry stock
can carry either rubble or dressed work. A mineral cover can use flat slate or
fired clay under the same treatment ID. An explicit request that targets no
supported component is an error.

Masonry relief and render use continuous backing solids. Stone faces preserve
aperture cuts and leave recessed beds, with profile variation concentrated at
headers and footing. The curtain returns preserve site connection planes and
the route envelope. Board decks share the existing roof surface with a thin
underlay, and cover still uses the established valley, ridge and headlap
placement. Reed, iron and terrace systems retain their specialized paths.
Legacy and unclassified pieces can coexist with treated pieces, with treatment
provenance omitted on the former. A named Blender finish reuses the author
material datablock and does not build a new procedural atlas for that component.


### Construction library authoring

The 0.14.0 authoring panel presents a curated set of presets for plinths,
supports, masonry bodies, framed infill, roof supports, and roof cover. It
projects selectors into the existing role override map and retains
per-component and unrepresented fields. Existing scene property data and
saved settings use the same representation. The new optional `variant`
refines a treatment and role without changing its stock or finish. The first
registered variants are `broken_course` and `level_course` for masonry walls
and plinths, and `hewn_pegged` and `squared_housed` for timber frame members and
roof supports. An absent variant uses the role's established preparation.
Incompatible variants report the component and field. The optional provenance
sidecar records `variant` where present. Strict format-1 exports retain the
old field set.

The Lowmark Smithy and Stable are the two authoring fixtures. The Smithy
retains its existing workfront and stock lanes and uses a raised visible
firebed with a seated ash opening and a higher hood mouth. Stable stall
frontage, handling route and hay access remain specific to its work. The
Thornfell curtain refinement seats both faces into a continuous bed and
bridges it at alternate headers. Function-specific assemblies and specialized
regional systems continue to reserve bearing, passage and roof shape.

Metal framing remains a proposed taxonomy extension. Its separate stock,
section, connections, host bearing, corrosion and validation would need
authoring review before registration. The current structural selection is
timber. Iron roofs and fixtures continue on their existing paths.
