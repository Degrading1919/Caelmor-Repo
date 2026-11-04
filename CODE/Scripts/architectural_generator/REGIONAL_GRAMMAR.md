# Caelmor regional working art grammar

This offline exterior generator treats region and building type as art direction for a parametric tool. The source dossiers establish broad regional cues; the palettes, construction mappings, exact roof covers, wealth tiers, and dimensions below are reversible visual inferences. They are not additional locked canon or claims about every resident. Ancient and hidden cultures are not used as the defaults for modern neighborhoods.

## Canon cues and bounded interpretation

| Region | Dossier cues used | Working exterior grammar |
| --- | --- | --- |
| Lowmark Vale | Fertile river crossroads, rebuilt fields, farms, mills, grain stores, barges and practical trade; practical water practices are ordinary, but hidden Riverwarden customs are not common civic knowledge. | Restrained plaster and timber infill, modest plinths, shingle roofs, practical porches and work openings. Brookhollow/Crestbridge favor wider fronts; rural holdings remain compact. |
| Thornfell Marches | Ridge and cliff communities, hewn-stone watchposts, longhouse clusters, stoneworking, harsh exposure, rope and chain bridges. | Hewn/rubble stone walls, compact ridge forms, slate working-cover assumption, small protected openings, sturdy exposed frames and watch galleries. |
| Mire of Fallen Banners | Homes on stilts or risen banks, elevated walkways, flood-resistant longhouses, reeds, peat, root and timber craft. Modern residents do not know Memorywarden magic. | Piers/decks and raised access, board/timber-light walls, reed-cover assumption, narrow raised forms, weathered restrained palette. |
| Emberholt Heights | Volcanic stone terraces, civic and artisan districts, forges, heat vents, emberglass and public embercraft. | Volcanic masonry, ashlar/rubble tiers, warm muted masonry and clay-cover assumption, forge stacks and vented work forms. The generator does not imply that every building uses magic. |

## Type grammar

`TYPE_SPECS` contains 20 immutable, purpose-led archetypes. Each records category, label, family, default plan dimensions, floors, footprint, roof preference and semantic features. Implemented features distinguish public entries, stable stalls, loading/hoist openings, forge stacks, civic porches, watch galleries, gate passages and waterside access through parametric construction. The feature tuples also retain future design hints; they are not a guarantee that every listed feature has a geometry consumer. For example, a mill wheel, barn lean-to, market open arcade, workshop tool ledge and stable side ramp are not implemented. Every archetype remains an exterior massing recipe.

## Regional contexts

Contexts are compatible region-specific stable IDs. `AUTO` resolves to each region's broad default. Lowmark offers Brookhollow, Crestbridge, Ashenstead, Greyharrow and rural holdings; Thornfell offers Stonewake, Highsteads, Passwatch and ridge; Mire offers Sorrowmere, Marshfall, Griefwatch and Rootrest; Emberholt offers Emberhold, Emberforges, Cinderweave and Ashspire. Context tweaks are deliberately small: massing changes apply in grammar mode; exposure and foundation style remain available in manual mode.

## Socioeconomic and condition controls

Wealth changes plan scale and selected finish assumptions; craftsmanship changes floor proportions and finish. Load-bearing masonry omits the exposed timber skeleton used by infill and board construction; maintenance and age drive conservative surface desaturation and exposure-related wear; Mire foundation clearance follows local flood context. These controls are art-tool parameters, not simulation or statements about canonical social classes. Natural region palettes preserve semantic keys such as `roof`, `roof_dark`, `plaster`, `timber`, `stone`, `glass`, and `metal`.

`Settings.use_grammar=False` preserves legacy manual dimensions. `resolve_settings()` normalizes legacy-compatible settings and produces a constraint-safe effective grammar plan. Plans keep both requested and effective settings, plus resolved style and type spec. `SOLID` remains the backwards-compatible geometry default; `EFFICIENT` is an additive surface optimization for roof covering and construction skins.

## Sources

- `LORE/Regions/Caelmor_Region1_LowmarkVale.md`
- `LORE/Regions/Caelmor_Region2_ThornfellMarches.md`
- `LORE/Regions/Caelmor_Region3_MireOfFallenBanners.md`
- `LORE/Regions/Caelmor_Region4_EmberholtHeights.md`
- `01_PRE-PRODUCTION/1.1 Core Vision/Caelmor_Phase1_1_Core_Vision.md`
- `01_PRE-PRODUCTION/1.2 Pillars & Tenets/Caelmor_Phase1_2_Pillars_and_Tenets.md`
- `CODE/Scripts/architectural_generator/Caelmor_Architectural_Generator_Research.md`
