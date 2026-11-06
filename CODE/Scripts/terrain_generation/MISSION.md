We have approved Lowmark Vale's geographical composition using the attached topographical planning map and thematic regional map. The placement and spatial relationships of settlements, landmarks, rivers, engineering works, and regional features are approved. The illustrated elevations, contour intervals, gradients, and scale have **not** been validated.

Your mission is to develop and demonstrate a deterministic mathematical terrain-generation methodology capable of reproducing this approved composition as a physically coherent, believable 3D landscape.

Inspect the current Caelmor repository, relevant canon, and existing tooling before selecting an approach.

**Primary objectives:**

- Preserve the approved geographical relationships and recognizable composition. Treat the illustrations as spatial design constraints, not surveyed elevation data.
- Establish a defensible coordinate system, world dimensions, terrain resolution, elevation constraints, and regional slope relationships. Evaluate scale against Caelmor's intended player traversal and world density rather than accepting the illustrated scale bar.
- Reconstruct plausible drainage basins, watersheds, river gradients, floodplains, wetlands, uplands, and waterfall transitions using mathematically constrained terrain synthesis.
- Explicitly validate the complete river system and engineered waterways, including Stillwater Fen, Hollow Lock, Relief Cut, Uphill Canal, Bramblelock Weir, and the main river's downstream course. Distinguish natural hydrology from engineered water control.
- Respect settlement requirements, including buildable terrain, flood exposure, access routes, and the surrounding landscape's narrative purpose.
- Prefer constrained elevation fields, drainage-aware mathematical modeling, authored control geometry, and deterministic refinement over unconstrained procedural noise.

**Implementation and verification:**

Develop the smallest working, reproducible offline prototype that demonstrates the method on Lowmark's major landforms. Produce inspectable terrain and hydrology visualizations, preferably including a comparison against the approved maps.

Verify drainage direction, elevation continuity, river connectivity, settlement suitability, and reproducibility. Record any remaining inconsistencies or necessary assumptions.

Use stable inputs and seeds so identical inputs reproduce identical outputs. Keep authored geographical constraints separate from generation algorithms so the terrain remains adjustable without redesigning the generator.

Do not modify the established architectural generator, importer, or gameplay runtime without a demonstrated dependency and explicit authorization. This is an offline world-authoring process, not runtime procedural world generation.

**Creative authority:**

Do not silently relocate approved settlements, landmarks, or major waterways to resolve mathematical conflicts. Make reasonable in-scope technical decisions independently, but present any unavoidable geographical compromises for Creative Director review.

The desired outcome is a working mathematical foundation for Lowmark terrain production, not merely a design proposal or an aesthetically similar noise-generated heightmap.

Commit reproducible project-owned work and verification evidence according to existing repository governance. Report the resulting terrain, validation findings, unresolved decisions, and next production step.

### Additional approved-map constraint: settlement capacity and terrain integration

The World & Quest design work has produced preliminary settlement capacity budgets. These are **proposed planning targets, not approved population canon or mandatory final building counts**.

Account for them while determining world dimensions, terrain resolution, local topography, buildable land, road corridors, and settlement envelopes.

| Settlement | Roofed buildings | NPC roster | Typical visible NPCs | Proposed built-up span |
|---|---:|---:|---:|---:|
| Brookhollow | 75–120 | 85–150 | 22–40 | 400–650 m |
| Crestbridge | 60–100 | 70–125 | 18–35 | 350–600 m |
| Ashenstead | 35–60 | 35–70 | 10–22 | 220–420 m |
| Greyharrow | 28–50 | 30–60 | 8–18 | 220–380 m |
| Reedmere | 12–24 | 15–32 | 5–12 | 130–250 m |
| Whisperflow Landing | 5–12 | 10–25 | 5–20 | 100–200 m |
| Drowsebank Mill | 4–10 | 5–14 | 2–7 | 70–160 m |

**Critical terrain requirement:**

Settlement terrain modification must be proportional to the settlement's function, density, and natural setting.

Large towns should have plausible, adequately sized developable areas supporting their anticipated building density, road networks, commercial functions, and civic infrastructure.

Small settlements and specialized worksites should adapt to existing landforms through localized grading, foundations, stilts, terraces, or limited earthworks. Do not create artificial flattened plateaus around every settlement.

Consider three distinct areas for each location:

1. Building footprints and developable land.
2. Settlement circulation and public-space envelope.
3. Surrounding working landscape and infrastructure.

Respect flood exposure, natural drainage, elevation changes, route access, and plausible medieval construction practices. Preserve recognizable surrounding geography.

For major river settlements, distinguish the waterfront working areas from safer residential and civic ground.

For agricultural communities, preserve extensive usable fields outside the concentrated village envelope.

For fen settlements, prioritize adaptation to existing waterways and marsh terrain rather than draining or flattening the landscape.

For mills and waterworks, derive terrain requirements from water levels, gradients, and engineering constraints.

**NPC implications:**

NPC roster figures represent assigned characters, not simultaneous active simulations. Visible-NPC targets are preliminary presentation and performance-planning estimates, not requirements to instantiate NPCs during terrain generation.

Use these estimates to anticipate public-space capacity, roads, markets, and circulation. Do not implement NPC simulation as part of this task.

**Validation:**

For each settlement, demonstrate that the resulting terrain can plausibly accommodate the proposed building range without excessive grading or damage to the approved regional composition.

Provide an inspectable settlement-capacity overlay showing candidate building areas, settlement envelopes, access corridors, surrounding working landscapes, slopes, and relevant flood exposure.

Identify locations where the proposed building capacity, footprint density, or built-up span appears incompatible with the approved geographical arrangement.

Treat such conflicts as matters for Creative Director review rather than silently changing approved placement.

Do not begin generating buildings or populating settlements. Establish and validate the terrain's capacity to support them first.