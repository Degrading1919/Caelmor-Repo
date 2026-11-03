# Caelmor Architectural Generator

Version 0.3.0 is an offline Blender add-on for editable, metre-scale exterior buildings. It combines regional working grammars, twenty purpose-led building types, manual orthogonal massing, procedural facades and roofs, original material maps, and semantic export metadata. It does not alter Caelmor runtime generation policy, Unity code, game schemas, or regional canon.

The regional mappings and exact architectural choices are reversible visual interpretations of the four regional dossiers, not new canon. See [REGIONAL_GRAMMAR.md](REGIONAL_GRAMMAR.md) for the source cues, context IDs, type grammar, and boundaries of those interpretations.

## Requirements and installation

- Blender 5.0.1 is the tested target. The extension manifest declares Blender 4.2 as its minimum; other Blender releases have not been validated.
- Install `dist/caelmor_architecture.zip` using **Edit → Preferences → Get Extensions → Install from Disk**, then enable **Caelmor Architectural Generator**.
- Open a 3D View and find the **Caelmor** tab in the N-panel.
- Rebuild the distributable with `py -3 package_addon.py` from this directory. The ZIP contains the add-on source, full GPL license, third-party notices, research reference, and regional grammar reference.

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

With grammar off, the manual dimensions and footprint are used directly. Roof style remains an independent control: **Regional / Type Default** selects the type's preference; Gable and Hip explicitly choose a roof. This keeps manual shaping available without silently applying archetype dimensions.

The supported footprints are RECT, L, T, and U. L wings may mirror, T wings may shift, and U wings may have unequal depths according to the seed. The guardrails require width 6–24 m, depth 4–16 m, 1–3 floors, and wing widths of at least 2.5 m. Non-rectangular wings must fit the main body, and U footprints retain at least 2 m of courtyard clearance.

### Household finish and condition

Wealth (Modest, Established, Affluent) affects grammar-mode scale and local finish assumptions. Craftsmanship (Rough, Standard, Fine) affects proportions, masonry selection, and surface finish. Age and Maintenance are separate condition inputs: older maintained buildings can remain cared for, and neglected buildings can be young. Condition changes subdued material wear; wealth does not automatically determine upkeep. These are art-authoring controls, not economic simulation or claims about canonical social classes.

### Detail and geometry modes

**High**, **Medium**, and **Low** alter architectural detailing and roof-course density. They do not represent runtime quality settings.

- **Solid** is the default, with a closed roof deck and closed structural components.
- **Efficient** reduces hidden roof layering and headlap geometry, and uses surface topology for physical cladding skins. The closed roof deck and structural core remain; exposed shingle relief, selected roof bedding, and optimized construction skins are tagged as `SURFACE` and are intentionally open surface geometry. This trades fully solid decorative layers for lower geometry counts; it is not a fully watertight building mesh.

The add-on reports effective plan dimensions and the latest geometry validation result in the panel.

## Regeneration and export

**Load Selected Settings** restores saved settings. **Regenerate Selected** replaces all generated layers or a selected roof, windows/doors, or details layer. Untagged objects are preserved. Use **Protect / Unprotect Selected** to retain an edited generated mesh through regeneration; protected meshes are included in exports.

Exports write GLB or glTF, a separate approximate collision GLB when proxies exist, and a `.caelmor.json` sidecar. The sidecar records settings, geometry hash, semantic layers, per-object material and topology, structural role, roof-envelope/support-surface diagnostics, and protected state. Collision proxies are approximate static wall and footprint shapes; they have not been tested for traversal or in Unity.

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
    geometry_mode="SOLID",
)
effective = resolve_settings(settings)
plan, buffers = generate(settings)
report = validate(plan, buffers)
collection, metrics = build(settings)
sidecar_path = export_building(collection, r"C:\temp\boathouse.glb")
```

`generate` and `validate` are pure Python. `build` creates or replaces Blender objects; `export_building` writes the interchange files. The API preserves the original manual `Settings` fields and adds the regional controls. Snapshots from version 0.2 that lack the new fields load as manual Lowmark SOLID buildings with a Gable roof, preserving the previous roof interpretation during scoped regeneration.

## Development checks

Use Python 3.11+ (or Blender's bundled Python) for pure geometry checks and Blender 5.0.1 for scene and export integration:

```powershell
py -3 -m unittest discover -s tests -p "test_generator.py" -v
py -3 -m unittest discover -s tests -p "test_geometry.py" -v
py -3 -m unittest discover -s tests -p "test_expansion.py" -v
py -3 -m unittest discover -s tests -p "test_facade_raycast.py" -v
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python tests/test_blender.py
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python tests/test_roof_clearance.py
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python tests/test_glass_timber_bvh.py
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python tests/test_profiles_blender.py
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python tests/smoke_surface_export.py
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python tests/render_expansion_evidence.py
./tests/compose_expansion_evidence.ps1
py -3 verify_install.py
```

See [tests/VALIDATION.md](tests/VALIDATION.md) for the current executed checks and evidence. Validation is generator and Blender authoring evidence; it is not a Unity compatibility check or a player-experience test.

## Scope limits

This is an exterior generator for orthogonal RECT/L/T/U footprints. It does not create arbitrary drawn polygons, interiors, enterable room layouts, or a complete settlement. Weathering, materials, and condition are procedural art, not measured simulation. Exported material behavior, collision, lighting, traversal, and performance still need review in any target engine.

## License and original assets

The add-on source is GPL-3.0-or-later; the complete license is included as `caelmor_architecture/LICENSE`. Redistributing or modifying the add-on source requires following the GPL terms and preserving the applicable notices. Procedural material maps and generated geometry are original project assets created by this tool; no downloaded textures, prefab library, or third-party mesh assets are included. Generated GLB/glTF files and manifests are output artifacts and do not contain the add-on source code.
