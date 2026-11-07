Continue development of Caelmor's Lowmark Vale terrain-generation system from the latest `main` commit (`3ec4003`).

**Objective:** Advance the verified deterministic regional terrain prototype into geographically believable, locally refined terrain capable of supporting Caelmor's settlements, roads, waterways, and eventual architectural generation.

You have already established the 6,144 × 4,992 m regional model, validated hydrology, deterministic generation, settlement capacity screens, and 3D terrain export. Preserve these accomplishments and build directly on the existing implementation.

### Primary work

**1. Local terrain refinement**

Develop appropriate 1–2 m local terrain refinement for Crestbridge, Greyharrow, Reedmere, and Drowsebank Mill.

Prioritize:
- Natural settlement foundations and believable building plots
- Road and cart access, terrain gradients, and river crossings
- Riverbanks, waterworks, flood exposure, and drainage
- Integration with surrounding terrain without artificial plateaus or visible tile seams

Use the existing regional terrain as the foundation. Do not recreate the generator or independently redesign approved regional geography.

**2. Crestbridge geographical review**

Give Crestbridge particular attention.

The current terrain places Crest Hall approximately 648 m from the settlement center and Hill Depot approximately 779 m away.

Review the Lowmark lore, narrative production bible, and POI requirements to determine whether these relationships support the intended fortified bridge town, granary operations, underground depot connections, and quest traversal.

Refine local geography and access where justified while preserving approved regional relationships. Do not silently relocate major narrative anchors or rewrite quest requirements.

**3. Remaining hydrological concerns**

Investigate and propose practical resolutions for:
- Western Whisperflow's ambiguous secondary waterway
- Stillwater Fen's natural outlet versus the authored quest-state closure
- Drowsebank's mill-race and its connection to the Relief Cut
- Reedmere's elevated settlement requirements under higher water
- The Uphill Canal's terrain and water-level relationships without inventing an explanation for its anomalous behavior

Distinguish technical corrections from decisions requiring Creative Director approval.

**4. Three-dimensional inspection**

Produce actual 3D inspection renders of the refined terrain, especially Crestbridge.

I want to evaluate the geography visually, not just through mathematical validation.

Include:
- A broad elevated view showing Crestbridge, Crest Hall, Hill Depot, and the surrounding valley
- A ground-level approach toward Crestbridge and its crossing
- A view demonstrating the relative elevations and distances between the bridge, granaries, Crest Hall, and Hill Depot
- Additional local settlement views where they reveal important design problems

Use Blender or existing supported visualization tools. Prioritize accurate terrain representation over decorative buildings. Simple massing proxies are acceptable when necessary to communicate scale, but distinguish them from generated architectural assets.

**5. Verification and integration**

Maintain deterministic reproducibility, drainage validation, and compatibility with the existing terrain-generation system.

Review relevant findings against the Caelmor Master Assistant Protocol, Phase 1 canon, Lowmark dossier, narrative and zone requirements, roadmap, File Manifest, and repository `AGENTS.md`.

Use the existing designated checkout and established output locations. Avoid duplicate pipelines, unnecessary scaffolding, unrelated architectural-generator modifications, or premature gameplay/runtime integration.

Exercise your delegated technical discretion. Investigate, implement, test, independently review, and correct issues without requiring approval for routine decisions. Escalate only foundational geographical changes, canon conflicts, or decisions outside your authority.

### Deliverables

Produce an inspectable, reproducible refinement milestone containing:

- Updated deterministic terrain outputs and validated local refinement
- Crestbridge 3D inspection renders, including ground-level and elevated perspectives
- Updated settlement capacity and access findings
- Verification evidence and any relevant performance measurements
- A concise record of unresolved Creative Director decisions
- Documentation explaining what is technically verified versus still conceptual

Commit and push verified project-owned changes directly to `main` under the repository's existing governance rules.

**Success condition:** I should be able to examine Crestbridge and the surrounding terrain in 3D, understand whether its settlement and quest geography physically works, and see that the same validated terrain can be regenerated deterministically.

The ultimate objective is terrain that supports the eventual construction of a believable, interconnected Lowmark Vale—not merely a mathematically valid heightmap.