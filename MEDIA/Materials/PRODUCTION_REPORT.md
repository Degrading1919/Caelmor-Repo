# Production report

## Delivered

- 100 uniquely ranked masters, 100 standalone grayscale PNGs, 100
  individually downloadable Procreate folders in ZIP form, and eight
  reusable Blender-generated OBJ templates.
- Each package has one indexed OBJ, a linked MTL, stable catalog metadata,
  and six 512 × 512 PNGs. The distributed 100 standalone masters are
  identical to their packaged `master.png`. There are 600 packaged PNG
  entries including those copies, of which 400 are linked in the MTLs.
- 21 palette choices across seven palette families, grouped and ranked
  contact sheets, a palette sheet, a repeat check and six native studio
  previews. All original baselines are procedural authoring starters.
- Versioned paint return, a Blender material builder, and a separate
  normal-from-height tool. [Authoring workflow](README.md) · [Painting checklist](PAINTING_CHECKLIST.md)

| Published deliverable | Count | Bytes |
| --- | ---: | ---: |
| Individual ZIPs | 100 | 43,871,404 |
| Standalone grayscale PNGs | 100 | 5,909,325 |
| Both delivery sets | 200 | 49,780,729 |

Source, templates and review evidence bring the full library to about
56 MB before Git compression. Optional higher-resolution variants and
working return copies are generated as needed. No production paint
returns, third-party extractions or dedicated Unity assets are bundled.

## Evidence and validation

| Gate | Observed result |
| --- | --- |
| Catalog and source links | 100 ranked IDs, declared physical U and V repeat, palette family, regions, per-master usage, sources and paint tasks. Repository paths verified. |
| Batch format | All 100 ZIPs passed member, material-ID, four MTL link, PNG dimensions/mode, nonconstant value/relief and repeat-boundary checks. All 100 grayscale files have distinct SHA-256 digests. |
| UVs | All 100 OBJ charts were checked against a complete one-to-one regular grid with positive-area faces. Each has 289 vertices and 256 quads. |
| Native pilot | Blender 5.0.1 imported and rendered six complete packages. One continuous chart per mesh with coverage 0 to 1, color sRGB and data Non-Color. Procreate-specific MTL links were checked and connected explicitly in Blender. |
| Reproduction | Six pilots and ten repaired masters rebuilt to byte-identical ZIPs. A fresh 1024-pixel shingle package and RGB normal regenerated from height were also verified. |
| Return to Blender | A synthetic chromatic PNG round trip created two revisions while preserving original and unselected maps. Tested occupied-slot protection, explicit assignment to a metric repeat surface, linked PBR inputs and packed image persistence after Blender reload. |
| Device and acceptance | Actual iPad Procreate import, painting and texture export await Creative Director testing. Hand-painting and production acceptance remain open. |

Machine-readable evidence is in [inventory.json](evidence/inventory.json),
[verification.json](evidence/verification.json), and
[roundtrip.json](evidence/roundtrip.json). A catalog audit moved weather,
soot, dye and similar finish-only entries out of the master count. The
repeat QA caught three basket-pattern boundaries and the texture pass
reworked thatch, bark shingles and joinery cues before delivery. Some
stock and weave baselines intentionally share methods and still benefit
from hand-painted tonal hierarchy and more natural irregularity.

## Research provenance and limits

- `Caelmor_Material_Research_Review.xlsx` sheets **Starter Library** and
  **Shared Surface Maps** informed the separation of physical stock,
  constructed patterns and reusable technical maps.
- `RS3_Material_Reuse_Research.xlsx` sheets **Named Fort References**,
  **Proposed Families** and **Shared Texture Maps** informed architectural
  and cross-category reuse priorities. Archived `material_usage_named.csv`
  and `texture_usage_named.csv` supply usage context. Assignment
  frequencies measure observed reuse, with no inference of canon supply.
- Phase 1 content strategy and the regional dossiers determine priority
  and plausible use. The architectural generator engine contract informs
  the Blender material handoff and the distinction between paint UVs
  and model-space UVs.
- The archived research tools were inspected at the inventory level.
  Existing workbook and metadata evidence sufficed for this mission.
  No live RSMV retrieval or use of Jagex image pixels was needed.
- Procreate import and export guidance comes from the
  [official 3D painting help](https://help.procreate.com/articles/Z0mATv-3d-painting)
  and [texture sharing handbook](https://help.procreate.com/procreate/handbook/3d-painting/share).

The current return accepts matching-size, non-interlaced 8-bit PNGs.
The library tests Blender authoring and source handling. Automatic
generator remapping, final glass transmission, and export baking of
procedural palette nodes remain production integration work.
