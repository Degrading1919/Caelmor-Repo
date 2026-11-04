# Expanded exterior implementation contract

Scope stays in this tool directory, no Unity/C#/game JSON/canon edits. Worktree:
`C:/Users/CK/Documents/Caelmor-Architecture`. No subagent Git writes.

## Profile/model owner

Own `profiles.py`, `model.py`, `REGIONAL_GRAMMAR.md`. Read current four regional
dossiers fully. Distinguish explicit facts from authored architectural inference.

Keep original Settings fields/API. Add region LOWMARK/THORNFELL/MIRE/EMBERHOLT;
context AUTO plus compatible named-local-context choices; wealth MODEST/ESTABLISHED/
AFFLUENT; craftsmanship ROUGH/STANDARD/FINE; maintenance float0..1; age years0..250;
use_grammar bool defaultFalse (legacy manual dimensions); roof_style GABLE/HIP/AUTO;
geometry_mode SOLID/EFFICIENT. Defaults preserve Lowmark manual API behaviour.
UI will start grammar mode for new buildings; old stored snapshots normalize to
legacy manual/SOLID defaults and preserve protected objects/material edits.

`profiles.REGIONS` maps codes to frozen region specs with label/context labels and
source references. `profiles.TYPE_SPECS` maps the following supported type IDs to
specs: original FARMHOUSE/BARN/GRAIN_STORE/MILLER/INN plus COTTAGE/TOWNHOUSE/
MERCHANT_HOUSE/LONGHOUSE/SHOP/WAREHOUSE/MARKET_HALL/STABLE/SMITHY/WORKSHOP/
ASSEMBLY_HALL/WATCHTOWER/GATEHOUSE/BARRACKS/BOATHOUSE. Specs expose category,
label,family, default dimensions/floors/footprint/roof_style and feature tuple.
Region/type/context/wealth change meaningful massing defaults in grammar mode.

`resolve_settings(requested)->Settings` returns effective dimensions, pitch,
roof_style etc in grammar mode, preserves manual dimensions otherwise.
`style_for(settings)->Style` exposes region,context,foundation_height,
foundation_mode PLINTH/PIERS, wall_material plaster/stone/timber_light,
construction TIMBER_INFILL/RUBBLE/ASHLAR/BOARD, roof_cover SHINGLE/SLATE/CLAY/REED,
frame_visibility 0..1, palette(dict semantic material->RGBA), weather_exposure.
Style is context/wealth/quality aware with conservative natural palettes.
All semantic material keys remain familiar (roof,roof_dark,plaster,timber,etc).

Plan.settings = effective Settings; Plan.requested_settings = original;
Plan.style = style_for(effective); Plan.type_spec=TYPE_SPECS[function];
Plan.foundation_height = style.foundation_height; Plan.eave=foundation_height+
floors*floor_height. Existing rects/outline/edges/rng/roof_height remain.
root owns roof_sources HIP implementation; Plan.roof_height HIP uses min of all
four distances to rectangle edges; GABLE keeps existing axis-distance formula.

## Facade/detail owner

Own facade.py and optional details.py. Consume plan.style/type_spec. Fix confirmed
window-to-beam collisions: reserve COMPLETE casing/shutter assembly, not just
aperture, against posts/braces/continuous floor plates/top plate/gable members.
Clamp/move windows into legal per-floor bands; keep sensible sizes/door height.
Expose assembly bounds and semantic members for independent tests. Mesh geometry
must agree with records. Protect roof-penetration fix. Foundation height replaces
hardcoded .45 throughout. PIERS: actual piles/deck and exterior access steps;
PLINTH existing closed stone base. Region construction changes walls/framing.
Type-specific parametric geometry must visibly convey purpose: storefront,
stable doors, warehouse loading hatch/hoist, forge stack/hood, civic porch,
watchtower/guard gallery, gatehouse passage, boathouse waterside door, etc.
No arbitrary prefab meshes or interiors. Every family needs a meaningful exterior
form/detail; conservative placement with semantic clearance, no random ornaments.
Use stable material keys; optional return extra buffers by type in details.py.

## Material/UI/backend owner

Own materials.py, blender_backend.py, __init__.py, blender_manifest.toml.
Expose all Settings controls plus apply grammar/profile, compatible context
selection, socioeconomic controls, effective plan dimensions/diagnostics.
Region/style palette plus age/maintenance/quality must alter real surfaces and
preserve natural family likeness. Texture banks original and shared by family;
contextual material keys include region/wealth/style revision, not one per asset.
Preserve old/manual materials, keep GLB palettes/roughness/normal/COLOR_0 valid.
`get_material(name,cache=None,style=None,settings=None)` extended compatibly;
backend passes plan.style, plan.settings. Material lookup/cache includes palette
context, so different regions in ONE scene do not silently share wrong colors.
Normalize old saved Settings through a model helper; preserve regeneration,
selection safety, anchors, protected edits, source hash labels, both UVs.
Root adds MeshBuffer.topology SOLID/SURFACE. Tag/export topology explicitly;
nonclosed shingle detail allowed only as SURFACE, closed structural core mandatory.
Version 0.3.0. Root handles generate/validate diagnostics + roof optimization.

## Root owner

Own roof.py, geometry.py, engine.py, optimization diagnostics, integration fixes.
Add correct clipped hip planes, and EFFICIENT roof surface mode removing hidden
undersides/headlap geometry while preserving closed deck + visible shingle relief.
Provide reproducible before/after counts and comparative Blender renders. No
guessed runtime polygon budget or Unity work.

## Verification owner (after implementation slot frees)

Own tests/, render evidence, README updates. Independent negative intersection
regressions, region/context/type/wealth matrix, old snapshot/manual protection,
headless Blender tests + comparative renders with explicit input/source hashes.
Do not claim simulation/Unity/structural certification. Wait for source READY
before heavy tests/renders. One Blender process at a time.
