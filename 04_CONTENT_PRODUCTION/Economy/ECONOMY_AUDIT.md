# Caelmor Economy Database Audit

## Row counts

| Relation | Rows |
|---|---:|
| `items` | 63 |
| `gathering_actions` | 18 |
| `gathering_nodes` | 28 |
| `gathering_action_outputs` | 43 |
| `recipes` | 48 |
| `recipe_inputs` | 99 |
| `recipe_outputs` | 48 |
| `item_sources` | 95 |
| `item_sinks` | 171 |
| `validation_findings` | 1 |

## Validation findings

- Errors: 0
- Warnings: 1
- Informational: 0

## Most connected items

| Item | Sources | Sinks | Skills | Band span |
|---|---:|---:|---:|---:|
| `common_timber` | 3 | 10 | 3 | 5 |
| `animal_fat` | 5 | 6 | 3 | 5 |
| `game_meat` | 6 | 5 | 2 | 5 |
| `sinew_cord` | 1 | 10 | 2 | 5 |
| `fletching_feathers` | 2 | 8 | 2 | 6 |
| `ashsteel_pickaxe` | 1 | 7 | 2 | 0 |
| `common_shafts` | 1 | 7 | 1 | 5 |
| `cured_leather` | 1 | 7 | 1 | 5 |
| `leather_strap` | 1 | 7 | 1 | 5 |
| `sinew` | 6 | 2 | 2 | 5 |
| `iron_bar` | 1 | 6 | 1 | 5 |
| `steel_bar` | 1 | 6 | 1 | 4 |
| `steel_pickaxe` | 1 | 6 | 2 | 2 |
| `ashsteel_bar` | 1 | 5 | 1 | 1 |
| `dense_bone` | 5 | 1 | 2 | 0 |

## Detailed findings

- **WARNING `weak_sink`** — item `emberstone_shard`: Persistent non-terminal item has only one modeled sink.

## Skill coverage

| Skill | Actions | Recipes | Items | Bands |
|---|---:|---:|---:|---:|
| `cooking` | 0 | 6 | 8 | 6 |
| `fletching` | 0 | 14 | 24 | 6 |
| `hunting` | 6 | 0 | 8 | 6 |
| `leatherworking` | 0 | 11 | 17 | 6 |
| `mining` | 6 | 0 | 3 | 6 |
| `smithing` | 0 | 17 | 21 | 6 |
| `woodcutting` | 6 | 0 | 3 | 6 |

## Analytical entry points

Use `v_item_origins`, `v_item_transformations`, `v_item_connections`, `v_item_health`, `v_level_unlocks`, `v_activity_rates`, and `v_tool_progression` for the primary design questions.