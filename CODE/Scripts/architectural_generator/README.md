# Caelmor Architectural Generator

Version 0.9.0 is an offline Blender add-on for editable, metre-scale buildings. It combines twenty building types, regional working grammars, an optional world-aware construction language, manual orthogonal massing, procedural facades and roofs, original material maps, and semantic export metadata. It does not alter Caelmor runtime generation policy, Unity code, game schemas, or regional canon.

The 0.9 surface pass preserves the 0.8 procedural geometry. Standard exported
PBR maps now carry preparation, material sorting and environmental history.
Wealth sorts natural stock; craftsmanship controls preparation/tool marks and
finish; age accumulates patina; maintenance reduces deterioration and supplies
localized replacements, repointing and limewash. Wealth does not set cleanliness.
The Lowmark Smithy and Thornfell Gatehouse are the controlled visual fixtures;
see `evidence/materials_v09` for surface-only comparisons and actual GLB
round-trip diagnostics. These isolate finishes on identical geometry; normal
generation continues to honor wealth/craftsmanship's existing construction rules.

Surface maps are original packed albedo, tangent-normal and ORM PNGs connected
directly to Principled BSDF, with no renderer-only procedural shader dependency.
`UV2_Surface` supplements `UV0_Metric` and `UV1_Lightmap`; mesh vertices/faces
are unchanged. CaelmorTint is neutral for these baked materials to avoid double
weathering on export. Detail controls map density (wood receives twice the base
density); individual face charts are capped at 256 pixels and atlases at 4096
per dimension. This is an authoring resolution policy, not a runtime budget.
Blender's bundled NumPy evaluates the maps; no external textures or packages are
downloaded. Atlas revision 1 is separate from the retained legacy surface bank.
Unchanged geometry/settings reuse their material datablocks, preserving shader
edits. Explicit material-slot overrides and protected objects survive regeneration.
Changing condition inputs creates a new finish bank instead of overwriting a
material an artist may have edited. Old manually edited surfaces can remain on
protected objects; condition changes do not forcibly replace them.

The 0.8 art benchmarks revise **Lowmark Smithy** and **Thornfell Gatehouse** in
World mode. The smithy has a primary gabled forge and a lower boarded stock
range, with fire screening, coursed stack, pegged bents and repair equipment.
The gatehouse has broad hipped flanks, an actual vaulted archway, courtyard
entries, defensive slots and a guard hall. These are procedural construction
rules for every seed of the selected pair, with fixed-camera before/after
comparisons under `evidence/benchmarks_v08`. Artistic acceptance is pending;
the other 78 region/function combinations retain their existing geometry.

In World mode, Smithy, Market Hall, Stable and Gatehouse now allocate functional
spaces before their regional construction shell. Integral work equipment,
trading bays, animal stalls and guarding/access arrangements are limited to
those programs; this is not a general interior generator. Program rooms,
stations, clearances and approaches are included in the export sidecar. Other
functions retain their existing regional builders, and legacy/manual mode
remains available. See [FUNCTIONAL_PROGRAMS.md](FUNCTIONAL_PROGRAMS.md) for the
construction contract, inference boundaries and small visual acceptance set.

The 0.7 construction pass gives these programs shaped working equipment,
framed selling bays and open hall trusses, constructed stall gates and feeding
troughs, and deep defended portals with masonry arches and battered tower
buttresses. Lowmark and Thornfell market ridges now follow the public aisle;
Mire keeps its raised crowned shelter and Emberholt its mineral terrace.
Sloping wall infill is cut across its full thickness beneath the roof. These
are geometry changes, with the existing studio and material system retained
for comparison; they remain subject to Creative Director artistic acceptance.

The regional mappings and exact architectural choices are reversible visual interpretations of the four regional dossiers, not new canon. See [REGIONAL_GRAMMAR.md](REGIONAL_GRAMMAR.md) for the source cues, context IDs, type grammar, and boundaries of those interpretations. [WORLD_ARCHITECTURAL_LANGUAGES.md](WORLD_ARCHITECTURAL_LANGUAGES.md) records the broader structural art direction; its proposals are visual interpretations, not canon or approved material catalogs.

The 0.5 household pass makes investment change usable construction: Lowmark
work/store/private-room compounds; calm Thornfell domestic roofs and sheltered
room ranges; Mire compact landings versus roofed work decks/private links; and
Emberholt hearth halls, narrow artisan bodies, lower work ranges and private
courts. Craftsmanship and condition remain separate controls. Emberholt work
roofs use lapped iron sheets, household windows have enclosed domestic
proportions, and soot follows generated hearths. See
[ARTISTIC_REFINEMENT.md](ARTISTIC_REFINEMENT.md) for the matched comparison brief,
research and limits. These are reviewable art improvements, not production-art
approval.

## Requirements and installation

- Blender 5.0.1 is the tested target. The extension manifest declares Blender 4.2 as its minimum; other Blender releases have not been validated.
- Install `dist/caelmor_architecture.zip` using **Edit → Preferences → Get Extensions → Install from Disk**, then enable **Caelmor Architectural Generator**.
- Open a 3D View and find the **Caelmor** tab in the N-panel.
- Rebuild the distributable with `py -3 package_addon.py` from this directory. The ZIP contains the add-on source, full GPL license, third-party notices, research reference, architecture references and household comparison brief.

## Generate a building

Choose a building type, region, compatible local context, household wealth, craftsmanship, age, maintenance, geometry mode, detail, and seed. New panel settings start with regional grammar enabled. **Generate New** builds the effective plan and records the requested settings and validation summary on the Caelmor Building collection.

### Regions and contexts

The region selector offers Lowmark Vale, Thornfell Marches, Mire of Fallen Banners, and Emberholt Heights. The local-context menu is limited to stable IDs for the selected region; **Regional Default** uses that region's default context. Context shifts affect grammar-mode massing and the resolved regional style. Regional palette and construction choices stay grounded in ordinary local stone, timber, plaster, and roof materials; hidden ancient cultures and magical motifs are not applied as general neighborhood decoration.

### Twenty building types

The twenty parametric archetypes cover these broad uses:

- **Residential:** Farmhouse, Cottage, Townhouse, Longhouse.
- **Agricultural:** Barn, Grain Store, Stable.
- **Commercial:** Miller, Inn, Merchant House, Shop, Warehouse, Market Hall.
- **Industrial and craft:** Smithy, Workshop.
- **Civic:** Assembly Hall.
- **Defensive:** Watchtower, Gatehouse, Barracks.
- **Waterfront:** Boathouse.

Each type has its own default plan proportions and exterior features such as stalls, loading openings, forge stacks, public porches, watch galleries, gate passages, or waterside access. These are parametric exterior forms, not prefab meshes.

### Grammar and manual shape

With **Use Regional Grammar** on, type, region, context, wealth, and craftsmanship resolve a constraint-checked footprint, dimensions, floor count and height, pitch, roof preference, foundation, construction, and cover. The manual width, depth, wing, footprint, floor, floor-height, and pitch values are not consumed in this mode; overhang remains an explicit user-controlled roof setting. **Apply Grammar to Shape Controls** copies the resolved dimensions into those controls; switch grammar off to edit the resulting shape manually.

With **World Construction Language** on (the default for new Blender settings), region, function and household investment create multiple roofed volumes where appropriate. Lowmark pairs halls with working/storage/private-room ranges; Thornfell households use calm stone gables and sheltered courts while public/defensive functions can justify towers; the Mire combines raised timber halls with working decks and private links; Emberholt uses deep masonry, hearth flues, narrow domestic bodies, terraced courts, lower iron-roofed work ranges and civic/industrial ironwalks. These forms can change the footprint and number of volumes, so shape values are profile inputs rather than promises of exact final dimensions. Generated bounds and validation report the actual result. Regional construction chooses roof forms and eaves, so manual roof style and overhang are disabled in this mode.

Turn **World Construction Language** off to use the single-plan regional generator. This retains the prior manual and grammar workflows for compatibility.

With both World Construction Language and grammar off, manual dimensions and footprint are used directly. Roof style remains an independent control: **Regional / Type Default** selects the type's preference; Gable and Hip explicitly choose a roof. This keeps manual shaping available without silently applying archetype dimensions.

The supported footprints are RECT, L, T, and U. L wings may mirror, T wings may shift, and U wings may have unequal depths according to the seed. The guardrails require width 6–24 m, depth 4–16 m, 1–3 floors, and wing widths of at least 2.5 m. Non-rectangular wings must fit the main body, and U footprints retain at least 2 m of courtyard clearance.

### Household finish and condition

Wealth (Modest, Established, Affluent) changes household capacity, work/storage space and private-room/access arrangements in World mode, as well as grammar-mode scale and local finish assumptions. Craftsmanship (Rough, Standard, Fine) affects proportions, masonry selection, joinery and surface finish. Age and Maintenance are separate inputs: older maintained buildings retain patina and repair history, while neglected buildings accumulate exposure-specific deterioration. Wealth does not determine upkeep. These are authoring controls, not economic simulation or canonical social classes. The legacy material revision 4 bank remains readable; the current atlas bank uses separate fingerprints and datablocks. Saved settings remain readable; exact older World output and finishes require their original version. Protected pieces remain intact and can require manual reconciliation with a changed room arrangement.

### Detail and geometry modes

**High**, **Medium**, and **Low** alter architectural detailing and roof-course density. They do not represent runtime quality settings.

- **Solid** is the default, with a closed roof deck and closed structural components.
- **Efficient** reduces hidden roof layering and headlap geometry, and uses surface topology for physical cladding skins. The closed roof deck and structural core remain; exposed shingle relief, selected roof bedding, and optimized construction skins are tagged as `SURFACE` and are intentionally open surface geometry. This trades fully solid decorative layers for lower geometry counts; it is not a fully watertight building mesh.

The add-on reports effective plan dimensions and the latest geometry validation result in the panel.

## Regeneration and export

**Load Selected Settings** restores saved settings. **Regenerate Selected** replaces all generated layers or a selected roof, windows/doors, or details layer. Untagged objects are preserved. Use **Protect / Unprotect Selected** to retain an edited generated mesh through regeneration; protected meshes are included in exports.

Exports write GLB or glTF, a separate approximate collision GLB when proxies exist, and a `.caelmor.json` sidecar. The sidecar records settings, architecture mode, construction-zone bounds and validation counts, geometry hash, semantic layers, each object's world-zone, material and topology, structural role, roof-envelope/support-surface diagnostics, and protected state. World-aware collision proxies are generated for each construction zone and use its own foundation and eave heights; legacy proxies retain their prior layout. Collision proxies are approximate static wall and footprint shapes; they have not been tested for traversal or in Unity.

Generated meshes include metric UV0, packed UV1 lightmap coordinates, material factors, and normalized `COLOR_0` weathering. Original tileable 128×128 color, tangent-normal, and roughness maps are generated for shared wood, stone, plaster, and roof material families and packed into the Blender file. Region/context/wealth/craftsmanship palettes are cached independently of seed; small seed variation is baked per building. GLB embeds supported material images. Review material behavior in the target pipeline before production use.

## Python API

With Blender's Python environment and the add-on on `sys.path`:

```python
from caelmor_architecture.model import Settings, make_plan, resolve_settings
from caelmor_architecture.engine import generate, validate
from caelmor_architecture.blender_backend import build, export_building

settings = Settings(
    seed=17, function="BOATHOUSE", region="MIRE", context="SORROWMERE",
    use_grammar=True, wealth="ESTABLISHED", craftsmanship="STANDARD",
    geometry_mode="SOLID", world_aware=True,
)
effective = resolve_settings(settings)
plan, buffers = generate(settings)
report = validate(plan, buffers)
collection, metrics = build(settings)
sidecar_path = export_building(collection, r"C:\temp\boathouse.glb")
```

`generate` and `validate` are pure Python. `build` creates or replaces Blender objects; `export_building` writes the interchange files. The `Settings` API defaults `world_aware=False` so existing scripts keep the legacy path; new Blender UI settings default it on. Snapshots without `world_aware` load with it off, preserving the prior geometry path and manual settings. Snapshots without the other regional additions continue to load as manual Lowmark SOLID buildings with a Gable roof.

## Development checks

Use Python 3.11+ (or Blender's bundled Python) for pure geometry checks and Blender 5.0.1 for scene and export integration:

```powershell
py -3 -m unittest discover -s tests -p "test_generator.py" -v
py -3 -m unittest discover -s tests -p "test_geometry.py" -v
py -3 -m unittest discover -s tests -p "test_expansion.py" -v
py -3 -m unittest discover -s tests -p "test_facade_raycast.py" -v
py -3 tests/test_world.py
py -3 tests/stress_world.py
py -3 tests/measure_geometry_modes.py --world
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --factory-startup --background --python tests/test_world_blender.py
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --factory-startup --background --python tests/render_world_evidence.py -- --matrix
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --factory-startup --background --python tests/render_world_feature_heroes.py
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python tests/test_blender.py
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python tests/test_roof_clearance.py
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python tests/test_glass_timber_bvh.py
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python tests/test_profiles_blender.py
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python tests/smoke_surface_export.py
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python tests/render_expansion_evidence.py
./tests/compose_expansion_evidence.ps1
py -3 verify_install.py
```

See [tests/V05_VALIDATION.md](tests/V05_VALIDATION.md) for current household verification, [tests/WORLD_VALIDATION.md](tests/WORLD_VALIDATION.md) for the retained v0.4 record and [tests/VALIDATION.md](tests/VALIDATION.md) for v0.3/v0.2. Validation is generator and Blender authoring evidence, not target-engine compatibility or player experience.

## Scope limits

This is an exterior generator for orthogonal RECT/L/T/U footprints. It does not create arbitrary drawn polygons, interiors, enterable room layouts, or a complete settlement. Weathering, materials, and condition are procedural art, not measured simulation. Exported material behavior, collision, lighting, traversal, and performance still need review in any target engine.

World construction derives mass placement and roof shapes from the region; unused legacy footprint/wing/pitch/eave controls are disabled. Shared opening details, repeated surface patterns and some broad masonry faces still need artistic refinement. Protected manual edits remain intact but are outside the procedural geometry checks; changing a building's architectural language can require manual reconciliation of those edits. No interior load analysis or terrain fitting is claimed.

## License and original assets

The add-on source is GPL-3.0-or-later; the complete license is included as `caelmor_architecture/LICENSE`. Redistributing or modifying the add-on source requires following the GPL terms and preserving the applicable notices. Procedural material maps and generated geometry are original project assets created by this tool; no downloaded textures, prefab library, or third-party mesh assets are included. Generated GLB/glTF files and manifests are output artifacts and do not contain the add-on source code.
