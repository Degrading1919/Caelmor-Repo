# Caelmor analytical economy data model

The SQLite file is an analytical design artifact, not a runtime replacement. Its source of truth is the schema-validated JSON batches in `interchange/` plus `balance_config.json`. Only `CODE/Scripts/caelmor_economy_builder.py` writes the canonical database; workers contribute batches. Stable keys and foreign keys make the relationships queryable.

## Relational spine

`gathering_nodes` owns world identity and region. Each node references one `gathering_action`; many nodes may share that action. The action owns skill, exact unlock level, rate/XP math, optional compatible tool items, and one or more `gathering_action_outputs`. Each output references an `item`. The item owns stable item identity/category/form, while `recipes` connect one or more item inputs to outputs with quantities, skill, region, station tag, and exact unlock. The builder derives `item_sources` from gathering outputs, recipes, and explicit external acquisition; `item_sinks` from recipe input consumption and explicit external `consumption` only.

`item_uses` is deliberately separate. Equipping, trading, tool requirements, tool use, and other non-consuming demand never increase sink counts. A recipe input is a modeled removal; an authored `external_sinks` `consumption` relation represents removal on use. Authored `external_uses` are non-consuming. `item_metrics.sink_count` therefore means consuming pathways, while `use_count` means non-consuming demand. Terminal equipment and tools may have zero true sinks without being orphaned; consumables and ammunition carry explicit consumption sinks. No generic external-use entry should duplicate a concrete recipe input.

`economy_skill_scope` separates the seven Phase 1.3 v1 skills (`v1_core`) from seven later Stage 3.1 skills (`economy_extension`). Phase 1.3 is the higher-authority v1 scope source. Extension rows are post-v1 analytical economy planning, not automatically authorized v1 runtime content. All 14 included skills retain gathering/crafting classification and covered/uncovered status. `skill_metrics` contains action/recipe/item/band counts for every included skill, including fully absent ones. Uncovered skills produce validation warnings; they are never omitted from the audit.

`progression_bands` and `xp_levels` are derived from the provisional `balance_config.json` using `CODE/Scripts/caelmor_progression_calculator.py`. Exact unlocks are `required_level` on actions/recipes and must lie in their bands. Gathering expected output/hour is deterministic attempts/hour × success × output quantity × skill yield multiplier; crafting output/hour is attempts/hour × recipe output quantity. Weighted output pools require an explicit rationale; conditional outputs without a calculable condition remain unresolved rather than guessed. The current authored catalog uses no RNG.

## Main query surfaces

| Question | View/table |
|---|---|
| Where does an item come from? | `v_item_origins`, `item_sources` |
| What can it become? | `v_item_transformations`, `recipe_inputs`, `recipe_outputs` |
| Which skills and regions connect? | `v_item_connections`, `v_item_origins`, `item_uses` |
| How long is it relevant? | `v_item_relevance` (`consuming_band_span` for removal; `relevance_band_span` also includes source/use horizon; `open_ended_demand` flags uses without an end level) |
| What unlocks at a level? | `v_level_unlocks`, `xp_levels` |
| Which items lack sources/consuming sinks? | `v_item_health` |
| Which materials may be redundant? | `validation_findings` plus source/sink neighborhoods |
| Expected XP/hour and yield/hour? | `v_activity_rates`, `gathering_action_outputs`, `recipes` |
| Which skills are uncovered? | `economy_skill_scope`, `skill_metrics`, `validation_findings` |

`validation_findings` records design-quality checks (orphans, dead ends, weak sinks, redundant signatures, progression gaps, tool/input gating, cycles). Schema/reference violations fail before a DB is published. The builder writes to a temporary sibling file, checks foreign keys and integrity, and replaces the canonical SQLite file only after a successful build.

## Rebuild

From repository root:

```powershell
py -3 CODE\Scripts\caelmor_economy_builder.py --input '04_CONTENT_PRODUCTION\Economy\interchange' --output '04_CONTENT_PRODUCTION\Economy\caelmor_economy.sqlite' --schema 'CODE\Scripts\caelmor_worker_interchange.schema.json' --progression-config '04_CONTENT_PRODUCTION\Economy\balance_config.json' --audit '04_CONTENT_PRODUCTION\Economy\ECONOMY_AUDIT.md'
py -3 -m unittest discover -s CODE\Scripts\tests -q
```

The baseline's XP, timings, success, and yields are provisional modeling parameters—not Caelmor canon and not runtime tuning. Runtime C# remains unchanged.
