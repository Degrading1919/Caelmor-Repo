# 0.7 construction-quality review

The Creative Director rejected the simplicity of the 0.6 four-function set,
despite its improved functional organization and passing technical gates.
This pass preserves the function-first approach and tests construction quality
in Smithy, Market Hall, Stable and Gatehouse. It does not expand the catalog,
change canon, generate general interiors or test Unity.

## Diagnosis before implementation

`render_function_diagnosis.py` reuses the existing native backend and studio.
Two original native geometry hashes are replayed: Lowmark Smithy and Emberholt
Gatehouse. Original front views are reused, then each mesh is rendered in clay
and materials under (a) changed light with the original camera, and (b) a lower
camera with original light. The eight new images and four original images are
composed without additional geometry generation into
`evidence/function_v07_diagnosis/comparison.png`.

Raking light reveals masonry relief; the lower view exposes more forge equipment.
The broad roof, box-like equipment and flat defended frontage remain in both
finishes. Geometry is the principal constraint in these two controlled examples.
The whole-finish clay/material change does not isolate individual shader effects.
No production shader or studio change is justified by this experiment alone.
The diagnostic runner initially stopped on missing per-row source metadata in an
older manifest; it was corrected to use that manifest's header revision and
resumed the existing four images before completing the second case.

## Acceptance and execution record

The observable construction requirements are in `FUNCTIONAL_PROGRAMS.md`.
The source revision and image/archive fingerprints are recorded in the final
gallery manifests and `verification.json`. The standard studio, seed, medium
detail, established wealth and standard craftsmanship are held constant. Each
native build supplies clay/material views from both opposing cameras.

Integration corrected issues that passed narrower checks: a moved Mire market
connector crossed framing; shrinking that connector left an unusable 35cm strip;
the tower resize displaced a bridge route; a center ray passed through a window
where a doorway was required. The final layout reserves a 1.35m transverse market
aisle before stalls, creates a real secondary watchtower door, and opens the
bridge rail at that supported landing. Permanent checks require public route
width, actual door records, multi-height/body-width rays, and a clear portal
head across the complete arch/lintel section.

The wall correction builds mitred infill solids at both faces and handles tapered
zero-height ends without degenerate faces. It applies to the four functional
programs; the other sixteen programs retain their recorded geometry. The
negative regression raises a real high-wall corner through the roof and verifies
that the wall gate rejects it. Glazing BVH checks include detail-layer functional
fixtures, not only structural buffers; circulation probes also approach the
declared top of their clear volume. These remain sampled clearance checks, not
exhaustive collision proofs.

Final commands/results are recorded in the gallery README alongside the retained
execution logs. Artistic acceptance remains pending Creative Director review.

## Limits and efficiency

The study samples two cases, not every region or wealth tier. It cannot establish
thermal, structural-engineering, terrain or runtime safety. Machine gates can
falsify geometric clearance claims but cannot approve art quality. Final artistic
acceptance belongs to the Creative Director.

Bounded Luna High workers own the two function modules and their focused tests;
the integration owner retains diagnosis, shared constraints and final review.
Luna Medium adapts existing evidence bookkeeping. One native mesh is reused for
both finishes and opposing views. This records a workflow, not a model ranking
or a measured reduction in subscription allowance, tokens, API dollars or total
wall-clock cost; those measurements are unavailable.
