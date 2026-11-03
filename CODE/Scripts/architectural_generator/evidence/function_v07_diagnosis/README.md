# Functional presentation diagnosis — v0.7

This is a controlled presentation comparison for two existing buildings: Lowmark Smithy and Emberholt Gatehouse. It reuses the v0.6 geometry, settings, materials, neutral ground, render resolution, and established studio setup. The native geometry hash is checked against the corresponding v0.6 record before each diagnosis case is rendered.

## Comparison layout

The contact sheet has three treatment columns and four rows. Each case appears in clay and material views.

| Column | Controlled change |
|---|---|
| Baseline studio | Original v0.6 front view and studio lighting/material treatment. |
| Raking light only | Keeps the baseline front camera, target, scale, geometry, and materials; changes the lighting rig. |
| Lower frontage only | Keeps baseline lighting, geometry, materials, target, and scale; lowers the camera angle to inspect the frontage. |

Rows are Lowmark Smithy clay/material, followed by Emberholt Gatehouse clay/material. The diagnosis renders are retained in this folder; the baseline column references the original v0.6 front images. Composition reads and verifies those existing PNGs and writes `comparison.png` without rerendering.

## Interpretation and status

In these two controlled cases, raking light makes existing masonry relief and equipment edges read more clearly. The lower camera reveals the forge, while box-shaped equipment, uninterrupted roof forms, and the gatehouse’s flat frontage remain visible. These observations point to geometry as the main constraint in the two examples, with lighting as a secondary contributor. The clay-versus-material comparison changes the whole finish, so it does not isolate the contribution of individual shaders. This is not a universal finding about all 16 function/region combinations. No production material change is planned from this study.

Compose the contact sheet after the diagnosis manifest and all treatment images are complete:

```powershell
./tests/compose_function_diagnosis.ps1
```

The expected sheet is 3332 × 3080 pixels. The composer checks image hashes and 1024 × 704 dimensions before placing the images.
