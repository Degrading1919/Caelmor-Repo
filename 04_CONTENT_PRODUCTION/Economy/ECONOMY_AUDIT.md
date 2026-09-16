# Caelmor Economy Database Audit

## Row counts

| Relation | Rows |
|---|---:|
| `items` | 102 |
| `gathering_actions` | 36 |
| `gathering_nodes` | 51 |
| `gathering_action_outputs` | 63 |
| `recipes` | 77 |
| `recipe_inputs` | 171 |
| `recipe_outputs` | 77 |
| `item_sources` | 148 |
| `item_sinks` | 197 |
| `item_uses` | 75 |
| `canon_skill_scope` | 14 |
| `validation_findings` | 0 |

## Coverage and graph health

- Canon skills covered: 14/14; uncovered: 0.
- Items without a modeled source: 0.
- Items without a consuming sink: 25 (reusable equipment/tools may intentionally have none).
- Non-guaranteed gathering outputs: 0; unresolved yield rates: 0.
- Balance status: PROVISIONAL_ANALYTICAL_BASELINE_NOT_RUNTIME_CANON.

## Validation findings

Consuming sinks count recipe-input removal and explicit item `consumption` only. Trade, equipment/tool use, tool requirements, and other non-consuming demand are counted separately in `item_uses`.

- Errors: 0
- Warnings: 0
- Informational: 0

## Most connected items

| Item | Sources | Consuming sinks | Uses/demand | Skills | Consuming band span | Relevance band span | Open-ended demand |
|---|---:|---:|---:|---:|---:|---:|---:|
| `common_timber` | 3 | 14 | 0 | 5 | 5 | 5 | no |
| `animal_fat` | 5 | 8 | 0 | 4 | 5 | 5 | no |
| `sinew_cord` | 1 | 12 | 0 | 4 | 5 | 5 | no |
| `ashsteel_pickaxe` | 1 | 0 | 10 | 3 | None | 0 | yes |
| `game_meat` | 6 | 5 | 0 | 2 | 5 | 5 | no |
| `iron_fasteners` | 1 | 10 | 0 | 5 | 5 | 5 | no |
| `cured_leather` | 1 | 9 | 0 | 2 | 5 | 5 | no |
| `fletching_feathers` | 2 | 7 | 0 | 2 | 6 | 6 | no |
| `leather_strap` | 1 | 8 | 0 | 2 | 5 | 5 | no |
| `sinew` | 6 | 3 | 0 | 3 | 5 | 5 | no |
| `steel_knife` | 1 | 0 | 8 | 4 | None | 4 | yes |
| `steel_pickaxe` | 1 | 0 | 8 | 3 | None | 2 | yes |
| `ashsteel_bar` | 1 | 6 | 1 | 3 | 1 | 1 | yes |
| `common_shafts` | 1 | 7 | 0 | 1 | 5 | 5 | no |
| `salvaged_ironwork` | 5 | 3 | 0 | 2 | 4 | 5 | no |

## Detailed findings

No validation findings.

## Canon skill scope

All 14 canonical non-combat skills are represented. `primary` is the original seven-skill request; `extension` is the full-economy continuation. `uncovered` is a validation warning, not an omitted row.

| Skill | Kind | Target | Status | Actions | Recipes | Items | Bands |
|---|---|---|---|---:|---:|---:|---:|
| `adornment` | crafting | extension | covered | 0 | 6 | 16 | 6 |
| `alchemy` | crafting | extension | covered | 0 | 9 | 18 | 6 |
| `angling` | gathering | extension | covered | 6 | 0 | 2 | 6 |
| `cooking` | crafting | primary | covered | 0 | 8 | 10 | 6 |
| `fabrication` | crafting | extension | covered | 0 | 6 | 19 | 6 |
| `fletching` | crafting | primary | covered | 0 | 14 | 24 | 6 |
| `foraging` | gathering | extension | covered | 6 | 0 | 6 | 6 |
| `hunting` | gathering | primary | covered | 6 | 0 | 8 | 6 |
| `leatherworking` | crafting | primary | covered | 0 | 11 | 17 | 6 |
| `mechanisms` | crafting | extension | covered | 0 | 6 | 13 | 6 |
| `mining` | gathering | primary | covered | 6 | 0 | 3 | 6 |
| `scavenging` | gathering | extension | covered | 6 | 0 | 2 | 6 |
| `smithing` | crafting | primary | covered | 0 | 17 | 21 | 6 |
| `woodcutting` | gathering | primary | covered | 6 | 0 | 3 | 6 |

## Analytical entry points

Use `v_item_origins`, `v_item_transformations`, `v_item_connections`, `v_item_health`, `v_item_relevance`, `v_level_unlocks`, `v_activity_rates`, and `v_tool_progression` for the primary design questions.