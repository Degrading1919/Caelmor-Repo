# Caelmor Architectural Generator — Evidence-Based Research and Implementation Brief

**Research date:** November 2, 2026  
**Purpose:** Guide development of a Blender add-on that procedurally **constructs** distinctive, richly modeled, medieval buildings for Caelmor—rather than requiring the developer to manually assemble a preset structural asset kit.  
**Game assumption:** The majority of buildings have complete exterior geometry; **selected** inns, workshops, homes, quest buildings and landmarks have explorable interiors (RuneScape-style selective access).  
**Scope:** Offline Blender art-authoring tool only. Generated assets are human-reviewed, baked/exported, and placed in a handcrafted Unity game world. No runtime world generation is proposed.  
**Evidence standard:** Software documentation and source repositories establish features/implementation existence, **not** independent proof of art quality or successful execution in Caelmor. No Blender runtime or Unity benchmark was executed as part of this research.

## Executive recommendation

**Build an architectural grammar engine with procedural geometry outputs**, not an AI-mesh generator and not a prefab assembler. The highest value strategy is:

1. **Python coordinator and semantic building plan** → footprints, floors, massing, roof logic, framing layout, functional volumes, per-part seeds.
2. **2D geometry kernel** → clean polygons, offsets, intersections, openings, roof boundaries.
3. **BMesh-created load-bearing structure** → foundation, timber posts, lintels, beams, floors, chimneys, wall framing, accurate gable/intersection geometry.
4. **Geometry Nodes detail system** → repeated tiles, roof shingles, decorative ironwork, moss, nails, stones, surface wear. Components can generate parametric primitives rather than drawing from a kit.
5. **Regional design grammar + physical aging model** → building function constrains silhouette/material/repair choices; generated history supports environmental storytelling.
6. **Selective interior solver** → only buildings designated enterable receive coherent rooms, stairs, wall thickness, collision and nav clearance; non-enterable buildings retain complete exterior shape and blocked windows/doors as appropriate.
7. **Game-export compiler** → semantic mesh grouping, shared material sets, efficient UVs, LOD tiers, simplified colliders, export records, Unity inspection.

**Core integration shortlist:** Building Tools (MIT); Blender BMesh + Geometry Nodes; Shapely or equivalent geometry kernel; a straight-skeleton algorithm for applicable roofs; xatlas (MIT), meshoptimizer (MIT) and trimesh for secondary UVs, LOD and QA. Introduce OR-Tools only when the selected-interior milestone needs it. Avoid adopting GPL/commercial libraries silently.

## Why this is feasible, and what 'fully fledged' means

A building generator can algorithmically construct posts, beams, complex roofs, masonry partitions and ornaments from dimensions and rules; it need not store prebuilt wall/roof meshes. A small **vocabulary of shapes and rules**, authored once, is unavoidable—geometry has to follow a language—but this is different from manually building a kit and assembling each structure. Detailed exteriors and plausible interiors are achievable for a bounded grammar; 'any building from any prompt, perfectly furnished and game-ready with no review' is not realistic.

The quality bar is not 'more texture on a rectangle'. Each model must display meaningful architecture: irregular footprint or intelligible growth history; structurally consistent roof, rafters and supports; openings tied to facade logic; physical masonry/timber details that survive close inspection; coherent material scaling; and believable repaired or worn surfaces. Every detail must also have an appropriate optimization path.

## Proposed engine layers and rules (concept, NOT approved JSON schema)

| Layer | Output and rules | Preferred implementation | Common failure to detect |
| --- | --- | --- | --- |
| 0. Input/seed | Region, building function, footprint mode, interior mode, detail tier, style restrictions, parent seed | Blender Python UI + persistent properties | Same seed produces different building after reopening |
| 1. Footprint | Valid outline, optional wings/courtyard, terrain attachment and foundations | Shapely/Clipper2 + deterministic grammar | Self-crossing contours or zero-width edges |
| 2. Massing | Floors, towers, bays, jetty, annexes, volumes and intended roof relationships | Semantic Python graph + rule engine | Unsupported overhangs or impossible circulation |
| 3. Architectural structure | Sills, posts, studs, braces, wall infill, headers, lintels, joists, chimney shafts | BMesh/curves + parametric profile lofts | Unsupported openings, disconnected frames |
| 4. Roof | Gables, hips, half-hips, side wings, valleys, soffits, rafters, shingles | Straight skeleton where useful + custom roof templates and intersection solver | Gaps/leaks, inverted slopes, accidental intersections |
| 5. Openings | Doors/windows aligned to room function, structural bays, roof and facade grammar | Offset/intersection constraints + BMesh | Floating doors, window cut through brace or stairs |
| 6. Surface geometry | Stone courses, timber grain relief, plaster cracks, tiles, wrought metal and distinctive joinery | Geometry Nodes, procedural profile and material masks | High-poly uniform repetition, texture swimming |
| 7. Age/history | Repairs, additions, smoke/rain staining, roof replacement and war marks | Event-driven grammar + masks linked to geometry | Random decals unrelated to water/gravity/use |
| 8. Selective interior | Room graph, corridor/door connectivity, stairs, accessible floors, interior structure | Recursive splits/constraint solver and BMesh | Blocked doors, unreachable stairs, clipping ceilings |
| 9. Export/QA | Mesh partition, UV/trim strategy, LOD0–2, collider meshes, render/metrics and Unity import | Export compiler + meshoptimizer/xatlas/trimesh + in-engine QA | Excess renderers, unsupported materials, missing floor collider |

### Generator design principles

- **Semantic-first, mesh-second:** A `post` should be a known element attached to a wall span and floor, not a random unidentified mesh.
- **Deterministic local seeds:** Derive stable per-component seeds (footprint, roof, facade, wear, interior) from a parent seed; changing roof tile color must not shuffle window positions.
- **Rules over randomness:** Function, ecology, wealth, age and region constrain probabilities and geometry; do not use purely global noise for weathering.
- **Editable components:** Store tags for foundation, walls, roof, openings, interior shell, trim and detail; support a "regenerate only roof" control.
- **Geometry hierarchy:** Generate structural/high-silhouette elements as mesh; lower-impact details become normal/roughness/decals or sparse instancing.
- **Safe regeneration:** Keep human edits in a protected override layer rather than rewriting edited vertices silently.
- **Headless reproducibility:** A generated building should be reproducible from input + tool revision + materials manifest, not a saved random viewport state.
- **Never mix up scene complexity and runtime complexity:** Very detailed procedural source assets may need aggressive bake, instancing, mesh joining and lightmap/collider prep for Unity.

## Technique decisions in implementation order

### 1. Footprint/massing grammars — adopt immediately

Start with orthogonal L, T and U footprints and controlled protrusions; support user-drawn polygon after sanitizing. Generate shape branches from functions (e.g. inn common room, detached/street-front store, attached service wing) rather than uniform weighted choices. Store volumes with adjacency. **Do not start with arbitrary concave footprint polygons** until the orthogonal test suite passes. Use dimensional constraints for door and stair sizes; reserve space before adding trim.

### 2. Roof construction — separate a dedicated subsystem

For a simple gable: construct two pitched planes from a ridge/plate solution. For a hip: straight-skeleton partitions are an excellent candidate. For cross-gables, dormers, stepped roof masses or variable slopes: build explicit roof sub-volumes with ridge relationships and resolve their valleys/intersections; skeletons are an aid, not a magic one-size-fit-all solver. Generate load-bearing rafters and fascia from roof geometry, then distribute tiles/shingles with orientation aligned to local slope.

### 3. Structural framing — fully generated geometry

Treat every facade as constrained wall spans between corners/floor intersections. Place corner posts and structural headers first; generate windows/doors **within legal free spans**; then studs, braces, noggins, panel infill, sill and trim. Masonry styles should generate coarse actual stone blocks at corners/sills/arches, while broad walls use tileable or baked materials. Use repeatable cross-section profiles along curves (not arbitrary object scaling that distorts grain).

### 4. Deterioration — causal rather than random

Generate changes as chronological building events: original core → attached wing → roof repair → reinforcement → staining → neglect. A chimney stains surfaces below the flue and roof downwind; moisture affects sill/plinth more than attic ridge; patches use distinct material cohorts. Deformation must preserve doorway clearance, roof weather envelope, colliders and gameplay traversal.

### 5. Interiors — constrain only the minority of buildings

An exterior-complete building contains believable openings and facade relationships but does not need expensive rooms/props. Functional buildings allocate room adjacency from use: inn common room to kitchen/service, stairs to rented bedrooms; workshop forge to ventilation/storage; selected homes to living/sleeping spaces. Generate walkability and logical stairs before furniture. For major narrative sites, expose override surfaces for the World & Quest Designer rather than attempting to generate signature story geometry automatically.

### 6. Unity-ready output — a release gate, not later cleanup

Use shared regional trim/tileable texture banks; separate only special textures that cannot be tiled. Avoid assuming all individual roof tiles must be actual meshes in every LOD. Build close view detailed geometry and bake/merge distant tiers; use simple colliders, keep doors as distinct interactivity anchors if enterable, test lighting and normal-map conventions in Unity. The reported URP metallic/occlusion/smoothness packed map is shader-specific; first verify Caelmor's renderer. **Do not adopt character triangle budgets for buildings.** Building targets should be empirically derived from a representative Lowmark Unity scene and measured frame-time/draw calls over an actual visible settlement.

## Existing tools — recommendation matrix

| Candidate | Status/terms verified | Recommendation | Rationale |
| --- | --- | --- | --- |
| Building Tools | MIT source; basic functions documented | **Study or fork first** | Existing Blender Python building operations, but not entire semantic architecture engine |
| BMesh + Geometry Nodes | Blender official built-in APIs | **Foundation** | Precise solid geometry plus efficient repetitive detailing |
| Shapely | BSD family; official docs/PyPI | **Prototype dependency** | Solid, familiar 2D footprint and boundary operations; binary packaging test necessary |
| bpypolyskel | GPL-3.0 source; author tests only | **Algorithm benchmark** | Strong hip roof starting point; GPL obligations if directly integrated |
| CGAL | GPL/LGPL/commercial varies by package | **Research reference** | More robust generalized skeletons; heavier dependency and licensing |
| Clipper2 | Open-source free commercial use | **Alternative geometry kernel** | Very good polygon offset/clipping; native library packaging harder |
| Sverchok | Procedural node ecosystem | **Methods reference** | Extensive geometry patterns; avoid required node-framework dependency |
| Bonsai/IFC | Semantic building modeling | **Semantic reference** | Walls/windows/doors/rooms are typed structural elements |
| Archipack | Free old and paid new tiers | **UX/reference only** | Mature parametric architecture features but code not universally reusable |
| Blender Level Architect | GPL-3.0; early project | **Experimental interior reference** | Promising room/door/stair solver claims but no QA evidence |
| Medieval Village Kit | CC0; recent source | **Style/export reference** | Code-generated assets but kit-based and painterly rather than Caelmor tone |
| xatlas + meshoptimizer | MIT | **Later exporter** | UVs, LOD simplification and mesh efficiency after geometric correctness |
| OR-Tools | Apache-2.0 | **Deferred** | Powerful for functional room layouts; overhead unnecessary for exteriors |
| WFC | Open source | **Optional, deferred** | Tiling/decor patterns, not building plans or roof logic |
| Material Maker + CC0 sources | Open-source authoring; site-level asset licenses | **Material pipeline** | Regional PBR consistency without training a unique texture AI model |

## Prototype sequence and completion gates

**Milestone A — proof of original geometry (highest priority):** A Blender installable add-on generates **one complete detailed, exterior-only Lowmark building** with an L-shaped footprint, real wall depth, exposed framing, doors/windows, gable/cross-gable roof, chimney, foundation, UV-ready meshes, and individually regenerable roof/window/detail layers. No manual prefab assembly. Demonstrate two substantially different seeds and an edited footprint. Clean roof intersections are the hardest acceptance test.

**Milestone B — ten-building diversity test:** Generate ten Lowmark exteriors from five functional classes (farmhouse, barn, grain store, miller dwelling, roadside inn). Check each in four fixed camera angles and a standardized Unity viewer scene; inspect silhouette similarity and close-up construction logic. For the selected inn, do **not** build interior yet; verify exterior grammar first.

**Milestone C — game-readiness:** Export a test street of ten buildings with source and optimized LOD meshes, colliders, UVs and material conversion. Benchmark actual frame time, draw calls, memory, shading/texture consistency, and light/shadow behavior. Record per-building metrics and export errors. Set budgets based on measured scene, not guessed triangle caps.

**Milestone D — selective interiors:** Add a functional inn, workshop and house with room connectivity, stairs, floors, doorway colliders, simple logical furniture zoning and in-engine player traversal. Require rooms to remain valid under at least five seeds and two footprint variations.

**Milestone E — Caelmor storytelling:** Add Lowmark history-specific construction rules and damage/repair cohorts; later expand to other regions only after Lowmark export and interiors are reliable. Important or story-critical landmarks remain artist-refined.

**Milestone acceptance record** should include seed, input settings, Blender build, generation time, geometry counts and material count, tests executed, four-view screenshots, collision results, mesh repair minutes, Unity render and profiler results, source licensing manifest, and any human intervention.

### Suggested quality checks

1. Repeatability: bytewise or geometry-hash equivalence under same seed/settings/build.
2. Geometry validity: non-self-crossing outer footprint; roof and wall seams within tolerance; no negative-area/zero-length faces; expected normal winding.
3. Semantic correctness: valid openings, legal structural clearances, no floating beam/unsupported porch, no chimney passing through stairs/window.
4. Interior correctness (only functional mode): connected rooms, traversable doors, stairs to actual floors, valid collider clearance.
5. Material quality: valid PBR map import, no obvious UV stretch, coherent texel density, region-consistent palette.
6. Unity quality: no missing textures, sensible pivot/scale, LOD transitions acceptable, colliders gameplay-sensible, playable frame-time within measured target.
7. Art direction: no procedural sameness across the ten-building set; low-fantasy grounded silhouette; visible, causally motivated repairs.

## Explicit constraints and unresolved decisions

- **Canon:** Phase 1.1 prohibits procedural generation for the initial release. A Blender-only offline authoring tool with reviewed, baked output is proposed to preserve *handcrafted world placement*, but this interpretation requires **Creative Director ratification**; do not silently rewrite canon.
- **Roles:** This report is Creative Director support research, not an approved gameplay schema, production JSON, Unity C# source, nor implemented Blender add-on. Systems Engineer exclusively owns C#; Schema & Content Engineer owns production schemas/JSON.
- **File location:** The live Caelmor repo's File Manifest was inspected. Related research resides in `00_ADMIN/Reference/`. This research is delivered as a standalone artifact and was **not committed to GitHub**. Do not invent additional folder paths or rename locked files without approval.
- **Dependencies:** Install/build wheels for the actual Blender bundled Python version and Windows environment. Keep optional external geometry/solver libraries behind adapters; ensure the add-on can report missing dependencies and still run a basic rectangular/gable test mode.
- **Licensing:** Verify the exact branch/source files before copying code. **An idea or algorithm is not a grant to copy someone else's source implementation.** GPL and commercial restrictions may affect redistribution of add-on code; Blender-generated model output is a separate question. This is engineering guidance, not legal advice.
- **Evidence limitation:** The sources below were researched via official web pages, repositories, research records and vendor descriptions. No independent visual quality benchmarking, headless Blender execution or Unity profiler run was performed, and early project claims are identified as such.

## Source register — annotated websites

**Evidence categories:** *Research* = academic method; *Official* = developer documentation; *Source* = repository showing actual code and license; *Demo/vendor* = promotional or community demonstration, not independent validation; *Heritage* = construction accuracy and lived-in detail. Each entry is a reviewed web resource and states exactly how to use it.

### Architecture grammar

1. **[ACM SIGGRAPH: Procedural Modeling of Buildings (Müller et al., 2006)](https://doi.org/10.1145/1141911.1141931)** — *Established research*. **Technique:** Context-sensitive CGA shape rules subdivide and transform volumes and facades into detailed buildings. **Caelmor implementation:** Use hierarchical plan → massing → faces → openings → details with constrained rule choices. **Limitation:** Research algorithm, not a drop-in software package; reproduce principles, not proprietary CityEngine syntax.

2. **[Arizona State University research record](https://asu.elsevierpure.com/en/publications/procedural-modeling-of-buildings-2/)** — *Research provenance*. **Technique:** Independent institutional record of the same CGA architecture work and publication context. **Caelmor implementation:** Trace peer-reviewed methods and definitions for shape rules and volumetric operations. **Limitation:** Not a second independently tested generation technique; provenance only.

3. **[Esri CityEngine CGA rule modeling](https://doc.arcgis.com/en/cityengine/latest/get-started/get-started-rule-based-modeling.htm)** — *Mature commercial implementation*. **Technique:** A shape receives rules; attributes guide generation of geometry and massing. **Caelmor implementation:** Copy the concept of named building grammars, attribute sets, and repeatable generation—not proprietary code. **Limitation:** CityEngine proprietary; cannot copy code or assume rules directly run in Blender.

4. **[MDPI: Procedural modeling of building layouts and roofs](https://www.mdpi.com/2073-431X/8/2/38)** — *Published research; access was rate-limited*. **Technique:** Study polygon and roof/floor-plan modeling methods for atypical footprints. **Caelmor implementation:** Use as a literature reference for distinguishing building footprint, room layout and roof generation. **Limitation:** Paper page was rate-limited on direct fetch; verify full article before citing an algorithm implementation.

5. **[Epic Games PCG framework](https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-in-unreal-engine)** — *Mature comparison, different engine*. **Technique:** Graph-driven hierarchical procedural content generation and partitioning. **Caelmor implementation:** Borrow orchestration concepts: staged graph, deterministic seeds, context-scoped generation. **Limitation:** Unreal-specific; do not adopt engine runtime or plugin as a Unity dependency.

6. **[COMPAS computational architecture](https://compas.dev/compas/2.0.4/userguide/introduction.html)** — *Established research-oriented Python framework*. **Technique:** Architecture/engineering algorithms, geometry, meshes, CAD adapters including Blender. **Caelmor implementation:** Potential intermediate geometry data model and algorithm reference beyond raw Blender operators. **Limitation:** Large dependency; investigate Blender Python packaging and license before use.

7. **[FreeCAD parametric CAD ecosystem](https://www.freecad.org/addons.php?lang=en)** — *Mature CAD comparison*. **Technique:** Constraint-driven sketches, history, architectural/fabrication modeling ecosystem. **Caelmor implementation:** Learn dependency-graph and regeneration concepts; do not require FreeCAD to operate generator. **Limitation:** Secondary workflow, not an art-ready medieval building solution.

8. **[libfive implicit solid modeling](https://libfive.com/)** — *Established parametric solid-modeling library*. **Technique:** Functional shape representations, constructive solid geometry, warps and smooth composition. **Caelmor implementation:** Possible later implementation for detailed arches/organic masonry profiles; keep off critical path. **Limitation:** Mesh conversion, materials/UVs, packaging and mixed MPL/GPL licensing demand review.

9. **[TopoTopo headless procedural geometry](https://topotopo.dev/)** — *Emerging project; vendor claims*. **Technique:** Reproducible graph with CLI, JSON and purported Blender export. **Caelmor implementation:** Evaluate architectural graph/export patterns and deterministic headless testing. **Limitation:** Not independently validated for medieval buildings; avoid foundation dependency until tested.

### Blender generators

10. **[Building Tools: primary code reference](https://github.com/ranjian0/building_tools)** — *Source available; MIT license verified*. **Technique:** Blender add-on for floors, roofs, doors, windows, stairs, balconies, multigroup facade operations. **Caelmor implementation:** Study or fork architecture primitives; replace box-oriented structure with an explicit building grammar. **Limitation:** Repository README mentions Blender 4.0 compatibility; test on target Blender, performance and repair quality.

11. **[Building Tools developer documentation](https://ranjian0.github.io/building_tools/)** — *Project documentation*. **Technique:** Add-on surface, supported modeling operators, interactions. **Caelmor implementation:** Reproduce artist-friendly controls and operations, not necessarily its authoring UI. **Limitation:** Version-specific docs; verify against the branch selected for integration.

12. **[Blender official BMesh Python API](https://docs.blender.org/api/main/bmesh.html)** — *Authoritative production API*. **Technique:** Editable topology operators and mesh connectivity, split/dissolve/face manipulation. **Caelmor implementation:** Use Python+BMesh for deterministic walls, openings, roof intersections, beams, stairs and structure. **Limitation:** Blender API changes require pinning an LTS build and regression testing.

13. **[Blender Geometry Nodes official manual](https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/introduction.html)** — *Authoritative production API*. **Technique:** Procedural mesh/curve/instance generation as modifiers or node groups. **Caelmor implementation:** Use for repeating roof tiles, nails, shingles, stone accents, braces, vegetation scatter. **Limitation:** Keep structural rules out of single giant node graph; realize instances only at export as necessary.

14. **[Sverchok geometry node catalog](https://nortikin.github.io/sverchok/docs/nodes.html)** — *Established open-source project*. **Technique:** Broad procedural geometry nodes for CAD, offsetting, solids, curves, meshes. **Caelmor implementation:** Reference node recipes and algorithms for ornamental geometry and polygon operations. **Limitation:** Large node framework, packaging/plugin interoperability concerns.

15. **[Bonsai IFC model authoring](https://docs-unstable.bonsaibim.org/guides/authoring/index.html)** — *Production-oriented IFC/BIM add-on*. **Technique:** Walls, rooms, openings, stairs, roofs, materials are semantic model elements. **Caelmor implementation:** Adopt the *separation of semantic entities from rendered geometry* for functional interiors. **Limitation:** BIM-heavy, no need to use IFC directly for Caelmor.

16. **[Archipack feature matrix](https://blender-archipack.org/features)** — *Established, partly commercial*. **Technique:** Parametric walls, roof, truss, beams, windows, stairs, moldings, auto-edits. **Caelmor implementation:** Study scope and UX of mature architecture tools. **Limitation:** Paid features/code not reusable without permission; confirm legacy/free component licenses.

17. **[Archipack historical open documentation](https://blender-archipack.gitlab.io/user%20guide.html)** — *Version-sensitive documentation*. **Technique:** Editable walls and roofs, reference paths, independent architectural objects. **Caelmor implementation:** Reference object parameter interactions and roof adjustment mechanisms. **Limitation:** Older documentation/version; validate compatibility before any direct dependency.

18. **[Archimesh overview](https://iblender.org/add-ons/archimesh/)** — *Legacy Blender extension*. **Technique:** Walls, stairs, doors/windows from architectural parameters. **Caelmor implementation:** Reference simple shape construction and UI controls for architectural objects. **Limitation:** Historical compatibility; insufficient detailed procedural output by itself.

19. **[Blender Level Architect](https://github.com/dottyboy/BlenderLevelArchitect)** — *Recent code; GPL-3.0; unproven production*. **Technique:** Author claims room/corridor/stair planning and WFC-style building plans for Blender. **Caelmor implementation:** Read solver structures for functional buildings, doors and connectivity. **Limitation:** Very young project with limited independent testing; GPL code-reuse implications.

20. **[Medieval Village Kit](https://github.com/danielgruginski/MedievalVillageKit)** — *Recent CC0 source example*. **Technique:** Python-generated medieval buildings, terrain and elements aimed at Unity. **Caelmor implementation:** Inspect geometry/scene-script patterns and game export habits. **Limitation:** Actually a modular kit, stylized WoW direction, not direct substitute for original geometry generation.

21. **[Blenderesse cottage/castle procedural releases](https://www.cgchannel.com/2024/10/jesse-miettinen-makes-all-of-the-blenderesse-blender-plugins-available-free/)** — *Independent industry coverage*. **Technique:** Catalog of freely distributed Geometry Nodes cottage and castle tools. **Caelmor implementation:** Download and benchmark controls and roofs as architectural reference. **Limitation:** Free-to-download does not imply permissive code license; compatibility old.

22. **[Medieval House Generator commercial listing](https://www.artstation.com/marketplace/p/P2mKa/medieval-house-generator-procedural-geometry-nodes-for-blender)** — *Seller demonstration; not independently tested*. **Technique:** Seller describes L-shaped forms, timber framing, hip roofs, tiles, dormers and aging. **Caelmor implementation:** Use visible scope as a baseline for parity tests and UX expectations. **Limitation:** Commercial license; advertised features do not prove game readiness or correctness.

23. **[Superhive Medieval House Generator documentation](https://superhivemarket.com/products/medieval-house-generator/docs)** — *Seller documentation*. **Technique:** Documented Geometry Nodes medieval generator based on instanced modular kit. **Caelmor implementation:** Study property/seed controls, contrast with true generated beams/roof geometry. **Limitation:** Explicitly kit-based; fails the no-hand-built-asset-kit principle as core solution.

24. **[Itch.io stylized medieval village generator](https://nico-hartl.itch.io/stylized-medieval-village)** — *Seller documentation*. **Technique:** 104 modules; snap grid; LODs; material/UV standards; slider-based house generator. **Caelmor implementation:** Excellent benchmark for final exported game assets and packaging, NOT generator geometry. **Limitation:** Commercial product, visually stylized, uses prefabs as construction basis.

25. **[Blender Artists procedural house experiment](https://blenderartists.org/t/home-2-0-procedural-house-generator-geometry-nodes/1656233)** — *Artist community demonstration*. **Technique:** User-configured footprints, roof types and structure through Geometry Nodes. **Caelmor implementation:** Study practical user-supplied footprint and roof editing workflow. **Limitation:** Claim/demo—not verified complete medieval game asset system.

26. **[CG Cookie BCITY training](https://www.cgcookie.com/courses/bcity-building-a-procedural-city-generator-with-geometry-nodes)** — *Training course, proved workflow concept*. **Technique:** Parametric footprints, instanced facades and street layouts with Geometry Nodes. **Caelmor implementation:** Use for generator UI and batching patterns, perhaps settlement placement later. **Limitation:** Course uses modular building pieces, so not the core generation method.

27. **[SideFX Labs procedural tool catalog](https://www.sidefx.com/docs/houdini/labs/)** — *Mature industry tool ecosystem*. **Technique:** Game-dev procedural techniques and exporter/asset prep patterns. **Caelmor implementation:** Benchmark technical architecture, batch processing, LOD and baking ideas. **Limitation:** Houdini dependency and asset-based construction; reference rather than transplant.

### Polygon and roofs

28. **[CGAL straight skeleton](https://doc.cgal.org/latest/Straight_skeleton_2/index.html)** — *Established computational geometry*. **Technique:** Straight skeleton from polygon edges, including holes, used for roof-style interior partitions. **Caelmor implementation:** Investigate pitched roof division on nonrectangular outlines, valleys and ridges. **Limitation:** Straight skeleton does not solve every gable/cross-gable aesthetic; GPL/commercial for portions.

29. **[CGAL licenses](https://www.cgal.org/license.html)** — *Primary license terms*. **Technique:** CGAL GPL/LGPL/commercial dual licensing, package-dependent. **Caelmor implementation:** Gate whether to import library vs reimplement algorithm from research. **Limitation:** Do not assume LGPL applies to straight-skeleton package.

30. **[bpypolyskel source](https://github.com/prochitecture/bpypolyskel)** — *Open Blender implementation, GPL-3.0*. **Technique:** `polygonize` derives hip-roof faces from footprint and an adjusted straight skeleton. **Caelmor implementation:** Ideal technical reference and test oracle for concave roofs. **Limitation:** GPL-3.0; authored 99.99% OSM success statistic is unverified, and geometry may be cleaned/non-mathematical skeleton.

31. **[Shapely geometry manual](https://shapely.readthedocs.io/en/stable/manual.html)** — *Mature Python geometry library*. **Technique:** Polygon buffering, clipping, intersections, validity, affine transforms and spatial queries. **Caelmor implementation:** Use for robust footprint cleanup, wall thickness, openings and courtyard subtraction. **Limitation:** Python wheels/GEOS must be compatible with Blender-bundled Python; avoid runtime dependency if packaging hard.

32. **[Clipper2 polygon geometry](https://www.angusj.com/clipper2/Docs/Overview.htm)** — *Established geometry library*. **Technique:** Robust clipping, offsetting and triangulation of polygons, integer-friendly. **Caelmor implementation:** Alternative to Shapely for foundations, wall-ring offsets and polygon Boolean operations. **Limitation:** Native C++/C# builds require wrappers; license and redistribution review.

33. **[Mapbox Earcut triangulation](https://mapbox.github.io/earcut/)** — *Widely used polygon triangulator*. **Technique:** Fast triangle generation from polygon rings and holes. **Caelmor implementation:** Triangulate verified 2D floor/roof plates as needed. **Limitation:** Author explicitly warns invalid or overlapping rings can produce incorrect output; validate first.

34. **[OpenStreetMap Simple 3D Buildings](https://wiki.openstreetmap.org/wiki/Simple_3D_Buildings)** — *Common building representation vocabulary*. **Technique:** Roof form, height, levels, material, parts and building attributes. **Caelmor implementation:** Borrow semantic labels and roof families for architecture configuration. **Limitation:** Real-world GIS convention is not medieval design logic or a software generator.

35. **[OSM2World generator](https://osm2world.org/)** — *Working map-to-3D renderer*. **Technique:** Outputs glTF and multiple LODs with building and roof interpretation from OSM tags. **Caelmor implementation:** Reference scalable map building representation and export strategy. **Limitation:** Modern geographic massing usually lacks fine medieval structural geometry.

36. **[COMPAS IFC geometry kernels](https://compas.dev/compas_ifc/latest/architecture.html)** — *Emerging integrated CAD implementation*. **Technique:** Unified mesh, extrusion, BRep and boolean representations with property validation. **Caelmor implementation:** Borrow architecture of semantic solids → mesh conversion, not complete BIM stack. **Limitation:** Integration complexity high for a Blender-first solo project.

### Interiors and detail

37. **[Google OR-Tools CP-SAT](https://developers.google.com/optimization/cp/cp_solver)** — *Mature constraint optimizer*. **Technique:** Integer decision solver for placement/capacity/adjacency constraints. **Caelmor implementation:** Later: solve room dimensions, stair alignment, service passage access, door clearances. **Limitation:** Do not add OR-Tools for MVP exterior generation; solver does not create architectural aesthetics.

38. **[Wave Function Collapse canonical repository](https://github.com/mxgmn/WaveFunctionCollapse)** — *Established tile-adjacency algorithm*. **Technique:** Constraint propagation across compatible tiles/patterns. **Caelmor implementation:** For interior furnishings, secondary facade accent placement, paving patterns. **Limitation:** WFC alone does not understand architectural load paths, room semantics or circulation.

39. **[English Heritage medieval architecture](https://www.english-heritage.org.uk/learn/story-of-england/medieval/architecture/)** — *Institutional historic source*. **Technique:** Period architectural context and styles beyond generic fantasy tropes. **Caelmor implementation:** Anchor styles in plausible timber, stone, roof and window design. **Limitation:** Historical reference, not generator code. Caelmor canon overrides direct historical imitation.

40. **[Society for Protection of Ancient Buildings: timber frames](https://www.spab.org.uk/advice/timber-frames)** — *Specialist conservation guidance*. **Technique:** How structural timber ages, shifts, decays and can be repaired. **Caelmor implementation:** Model causal wear: sill rot, scarf repair, substituted braces, damp staining, bowed elements. **Limitation:** Avoid random structural sag that violates support/geometry intersections.

41. **[Historic England: farm-building repair guide](https://historicengland.org.uk/images-books/publications/maintenance-repair-trad-farm-buildings/heag157-maintenance-repair-traditional-farm-buildings/)** — *Institutional historic source; PDF*. **Technique:** Farm architecture, materials, repairs and historical changes of use. **Caelmor implementation:** Excellent Lowmark barn/mill/storehouse design grammar and believable deterioration. **Limitation:** PDF requires page screenshot for visual analysis; not a code implementation source.

42. **[Material Maker](https://www.materialmaker.org/)** — *Established open-source material tool*. **Technique:** Graph-generated PBR surfaces that export for Unity. **Caelmor implementation:** Author cohesive Lowmark stone, timber, plaster, tile, thatch material families. **Limitation:** Baked maps and texture conversion still need integration; code-license review.

43. **[Poly Haven asset license](https://polyhaven.com/license)** — *Primary CC0 license*. **Technique:** Freely licensed PBR textures, HDRIs and models. **Caelmor implementation:** Source high-quality measured materials and establish a reference material bank. **Limitation:** Per-asset scale/color must be normalized; do not assume textured mesh has correct texel density.

44. **[ambientCG material collection](https://ambientcg.com/)** — *Established CC0 material provider*. **Technique:** Photogrammetric and PBR surfaces, including stone/wood/plaster/ground materials. **Caelmor implementation:** Alternative/complement to procedural low-frequency texture generator. **Limitation:** Material visual differences must be curated by region and age.

45. **[TextureCan license](https://www.texturecan.com/terms/)** — *Primary CC0 site terms*. **Technique:** PBR textures available for commercial integration and redistribution with projects. **Caelmor implementation:** Reference material inputs for handmade stone, roof tiles and timber. **Limitation:** Brands, logos, copyrighted graphics not automatically cleared by CC0 site terms.

46. **[Adobe Substance 3D Designer documentation](https://experienceleague.adobe.com/en/docs/substance-3d-designer/using/getting-started/overview/overview)** — *Mature paid industry benchmark*. **Technique:** Procedural material authoring and maps for reusable surfaces. **Caelmor implementation:** Reference advanced wear/dirt/masks methodology; not a mandatory dependency. **Limitation:** Adobe paid ecosystem and license; avoid reliance if no-cost is preferred.

### Game-ready export

47. **[xatlas UV parameterization](https://github.com/jpcy/xatlas)** — *Established MIT source*. **Technique:** UV chart generation, UV unwrapping and packing. **Caelmor implementation:** Use for secondary unique UVs/lightmap UVs or special mesh parts; prefer tileables/trim sheets for much architecture. **Limitation:** Automated charts can create numerous seams; Python binding/build friction possible.

48. **[meshoptimizer mesh and LOD library](https://github.com/zeux/meshoptimizer)** — *Established MIT source*. **Technique:** Mesh index optimization, overdraw/cache improvement, simplification. **Caelmor implementation:** Produce silhouette-preserving LODs and efficient export geometry; test walls/windows/roof tiles. **Limitation:** Naive simplification can destroy architectural edges, openings and alpha details; use grouped semantic decimation.

49. **[trimesh mesh QA and processing](https://trimesh.org/)** — *Mature Python mesh processing*. **Technique:** Topology checks, bounding boxes, ray tests, watertightness on closed solids. **Caelmor implementation:** Automated post-export checks, self-intersection tests where supported, mesh statistics. **Limitation:** Full assembled building shell may intentionally not be watertight: validate solids/components rather than global object.

50. **[Khronos glTF PBR specification](https://www.khronos.org/gltf/pbr/)** — *Open interoperability standard*. **Technique:** Material metallic/roughness convention, texture semantics and portability. **Caelmor implementation:** Use `.glb` as experimental portable artifact and standard PBR reference. **Limitation:** Unity may use FBX for particular import workflows; material remapping still required.

51. **[Unity URP channel packed material mapping](https://docs.unity.com/en-us/engine/6000.6/manual/materials-and-shaders/built-in/shaders-in-universalrp/channel-packed-texture)** — *Official engine documentation*. **Technique:** URP Lit packed map: R metallic, G occlusion, B unused, A smoothness. **Caelmor implementation:** Adapt roughness maps to inverted smoothness if using this shader; unit-test imported materials. **Limitation:** Check Caelmor project render pipeline and Unity version first; custom shader conventions may differ.

52. **[Unity LOD Group documentation](https://docs.unity.com/en-us/engine/6000.6/manual/analysis/graphics-performance-profiling/lod/lod-group/class-lodgroup)** — *Official engine documentation*. **Technique:** LOD thresholds, renderer groups and cross fades. **Caelmor implementation:** Generate LOD0, LOD1, LOD2 and optional distant shell for each building, and measure in Unity. **Limitation:** Do not infer good frame rates from raw triangle count alone; materials, overdraw, batches and shadows matter.

53. **[Unity FBX model import](https://docs.unity.com/en-us/engine/6000.0/manual/assets-and-media/asset-types/models/importing/fbximporter-model)** — *Official engine documentation*. **Technique:** Mesh import, axis/unit, normals, material extraction, animation and collision choices. **Caelmor implementation:** Define exporter coordinate check and prefab QA for building classes. **Limitation:** Documentation is version-dependent; inspect actual project before hard-coding assumptions.

54. **[GNU GPL FAQ](https://www.gnu.org/licenses/gpl-faq.en.html)** — *Primary licensing source*. **Technique:** Distinguishes program distribution requirements and output-license considerations. **Caelmor implementation:** Audit license obligations before vendoring GPL roof or Blender add-on code. **Limitation:** Not legal advice; source-code copying is different from borrowing published algorithm ideas.

55. **[Creative Commons CC0](https://creativecommons.org/public-domain/cc0/)** — *Primary license framework*. **Technique:** CC0 rights waiver enabling commercial reuse of compatible materials. **Caelmor implementation:** Standardize provenance tracking for exterior surface art and textures. **Limitation:** CC0 does not guarantee no privacy, trademark or publicity rights.

56. **[PyPI Shapely release and license](https://pypi.org/project/shapely/)** — *Package metadata*. **Technique:** Shapely Python packaging and version/OS compatibility. **Caelmor implementation:** Research how to vendor a tested geometry engine into Blender Python on Windows. **Limitation:** Dependency on prebuilt binary wheels varies with Blender embedded Python.

57. **[Blender Foundation GPL FAQ](https://www.blender.org/about/license/)** — *Blender licensing documentation*. **Technique:** Blender GPL and how scripts/add-ons may interact with it. **Caelmor implementation:** Include a real licensing review before distributing an add-on; output 3D files generally are not forced GPL by Blender. **Limitation:** Web endpoint sometimes blocks indexing; verify primary text before commercial distribution.

---

**Research count:** 57 individually listed source pages, 47 distinct hostnames and 45 distinct site domains (treating independently administered GitHub Pages/ReadTheDocs subdomains as separate sites). The catalog deliberately distinguishes mature platforms from recent unverified demos.
