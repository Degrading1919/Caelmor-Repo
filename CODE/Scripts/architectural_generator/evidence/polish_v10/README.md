# Architectural polish in v0.10

The reference builds use generator source `ae0ec03`. The controls are the packed v0.9 benchmark scenes published through `c2da894`. Both captures use seed 91, established wealth, standard workmanship, age 35, maintenance 0.7, MEDIUM detail and EFFICIENT geometry. Each sheet pairs clay and material views and includes images rendered from the actual reimported GLB.

| Building | Distant | Gameplay distance | Close inspection |
|---|---|---|---|
| Lowmark Smithy | [Sheet](comparison/smithy_distant.png) | [Sheet](comparison/smithy_normal.png) | [Sheet](comparison/smithy_close.png) |
| Thornfell Gatehouse | [Sheet](comparison/gatehouse_distant.png) | [Sheet](comparison/gatehouse_normal.png) | [Sheet](comparison/gatehouse_close.png) |

The [controlled experiment](comparison/experiment_normal.png) shows the v0.9 control, the new material on the old mesh, and the first crafted geometry pass. The [control manifest](before/manifest.json) and [release manifest](after/manifest.json) record settings, camera transforms, geometry and image digests. There are 48 matched native frames and 12 GLB reimport frames across the three distances and two angles. The [Smithy Blender scene](after/smithy.blend), [Gatehouse Blender scene](after/gatehouse.blend), [Smithy GLB](after/smithy.glb), [Gatehouse GLB](after/gatehouse.glb) and [extension ZIP](../../dist/caelmor_architecture.zip) are included.

## Visual decisions

Photos 1, 2, 3 and 5 supplied by the Creative Director guided the study. The reference cues were substantial timber profiles, layered eaves, distinct values for roofing and walls, and masonry that carries through the threshold. The same cues appear in the environment art and game screenshots from Fort Forinthry. Caelmor uses split timber roofing in Lowmark and cool slate over local stone in Thornfell. These are art interpretations of the existing regional directions. The generator uses original procedural geometry and maps. [Anouk Debruyne’s Fort Forinthry environment work](https://anoukdebruyne.artstation.com/projects/Xg3P93) · [Jagex workshop screenshot](https://cdn.runescape.com/assets/img/external/news/2023/07/deadandburied/ranger3.png)

Material separation made the largest difference at normal distance in the first experiment. Darker framing carries across the Smithy front. Cool slate, dressed surrounds and a darker wall field make the Gatehouse entrance easier to find. The first bevel pass added masonry scale but made the Smithy chimney look heavily banded. The final pass reduces those arrises to 10 mm. The Smithy's heavier posts, ties and hewn knees give the work bay a visible bearing frame.

The Gatehouse has worked stone faces within the original wall envelopes. Four staggered courses over continuous bedding replace each blank battered wedge. Flagstone approaches bear on masonry and follow the established ramp grades. These changes give the plinth and threshold a material relationship to the arch. The passage, guard access and work-bay functions retain their existing layouts and clearance contracts.

The reference comparisons still expose straight roof courses, regular masonry bonds, restrained weathering and plain secondary elevations, especially the Smithy rear wall. The pass improves primary material hierarchy and the weight of the assemblies. The Creative Director still owns judgment about the desired RS3 level of finish. No external reference meshes or textures are bundled.

## Geometry and texture cost

| Fixture | Vertices v0.9 → v0.10 | Triangles v0.9 → v0.10 | GLB v0.9 → v0.10 | Embedded images v0.9 → v0.10 |
|---|---:|---:|---:|---:|
| Smithy | 8,136 → 9,320 | 9,352 → 11,704 | 11.84 → 3.78 MB | 10.55 → 1.95 MB |
| Gatehouse | 34,996 → 46,432 | 42,006 → 64,562 | 50.40 → 16.02 MB | 44.86 → 6.34 MB |

The Gatehouse spends 22,556 extra triangles on worked arrises and visibly bonded base construction. Its GLB is about 68% smaller. The largest texture saving comes from replacing unique face normals with shared 256² normal tiles. These repeat every two metres, giving 128 normal texels per metre before filtering. Per-piece metric phases align the normals with albedo grain and vary their placement. Albedo densities are selected by material family. The packed roughness and metallic map uses a 2× area filter on each axis. Fine relief comes from the reusable normal texture, while local condition remains in albedo and roughness/metallicity. The two inputs use separate map-bound UVs. Editable Blender scenes keep both original metric and lightmap UVs.

Exact whole-bank deduplication offered no savings on the nine original Gatehouse banks. The old GLB stored 18.76 MB albedo, 15.58 MB normal and 10.53 MB ORM PNG payloads. The revised Gatehouse stores 4.92 MB albedo, 0.059 MB normals and 1.36 MB ORM. These are authoring and export measurements. The native importer can reindex UV sets and omit unused sets. Verification follows each texture's actual binding.

## Executed verification

- Seven pure geometry utility checks covered winding, bounds, closed beveled boxes, open backs and clipped component rejection. Twelve detail and condition tests covered periodicity, slope continuity, grain direction and causal controls. Six benchmark regressions passed, covering deterministic seeds, geometry modes, openings and unchanged geometry hashes for the other 78 combinations.
- Blender 5.0.1 passed [native geometry checks](benchmark_mesh_checks.json) for both fixtures. The run checked 51 clearance rays, 32 stair headroom rays, 15 exhaust rays and actual glass/structure overlap.
- [Native export and lifecycle checks](export_checks.json) matched 468,942 map-bound UV values across both fixtures and compared 96 decoded pixel maps. Smithy checks covered edit protection, explicit material replacement, cached shader edits, save/reopen, deterministic textures and scoped regeneration with retained heat context. The maximum UV serialization delta was about 0.00000012. Native export and the gallery GLBs contain matching embedded PNG payloads.
- The [legacy farmhouse smoke](legacy_surface_check.json) and isolated [Smithy](install_smithy.json) and [Gatehouse](install_gatehouse.json) installations passed. [Evidence verification](verification.json) records the archive hash, all 33 package members, image digests, camera correspondence and GLB byte counts.

Luna High supplied the crafted geometry utilities, periodic detail sampler, export-test changes and independent first-pass visual critique. The lead handled integration, final corrections and final native execution after both workers hit their usage limit. The initial UV check used rounded set membership and rejected a valid serialization boundary. The final check compares the actual coordinates within 2e-6 and verifies the imported map bindings. The material and geometry experiment guided the changes before the full capture.
