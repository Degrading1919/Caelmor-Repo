# Creative Director balance decision package

**Decision status:** none of the options below is approved balance or canon. This is a read-only analysis of `caelmor_economy.sqlite` and the `PROVISIONAL_ANALYTICAL_BASELINE_NOT_RUNTIME_CANON` configuration. Phase 1.3's seven `v1_core` skills and Lowmark-only v1 geography remain distinct from the seven `economy_extension` skills and later-region analytical planning. No option here authorizes a runtime change.

## What the current numbers produce

The calculator uses a 60-level power curve (exponent 2.4, 1,000,000 XP at level 60). Every included skill has the same XP/hour target in a given band: the seven configured core skill profiles have no modifiers, and extension skills use the calculator's default 1.0 multipliers. Gathering awards XP on success; crafting awards XP per attempt. Success is 100%, all 63 gathering outputs are guaranteed, and weighted bonus chance is zero.

| Band / levels | XP/hour, every skill | Ideal hours through band | Gather seconds / attempts per hour | Craft seconds / completions per hour | New actions / recipes |
|---|---:|---:|---:|---:|---:|
| 1 / 1–10 | 1,412 | 10.00 (to 11) | 4 / 900 | 3 / 1,200 | 6 / 20 |
| 2 / 11–20 | 6,042 | 10.00 (to 21) | 5 / 720 | 3.5 / 1,029 | 6 / 13 |
| 3 / 21–30 | 12,272 | 10.00 (to 31) | 6 / 600 | 4 / 900 | 6 / 13 |
| 4 / 31–40 | 19,620 | 10.00 (to 41) | 7 / 514 | 4.5 / 800 | 6 / 10 |
| 5 / 41–50 | 27,872 | 10.00 (to 51) | 8 / 450 | 5 / 720 | 6 / 9 |
| 6 / 51–60 | 32,782 | 10.00 (to 60) | 9 / 400 | 5.5 / 655 | 6 / 12 |

Selected time-to-level from level 1: **10: 7.77 h; 20: 18.57 h; 21: 20.00 h; 30: 28.75 h; 40: 38.82 h; 41: 40.00 h; 50: 48.86 h; 60: 60.00 h.** These are ideal active-action hours, not elapsed play time: travel, inventory, node contention, inputs, stations, selling, and failure are not modeled. Seven core skills at 60 ideal hours apiece imply 420 single-skill training hours if all seven are mastered independently; this is not a player completion-time forecast.

**Pacing flags.** The equal 10-hour bands conceal uneven levels: levels 1→6 take 1.90 h, while 6→11 take 8.11 h. Every gathering skill gets exactly one new action at levels 1/11/21/31/41/51, so one action must carry most of each 10-hour band. Thirty of 60 levels unlock no action or recipe; levels 46–50 unlock neither. Recipe unlocks taper from 20 in band 1 to 9 in band 5. To hold increasing XP/hour as cadence slows, gathering XP per success rises from 1.569 in band 1 to 81.955 in band 6; crafting XP per completion rises from 1.177 to 50.084. These are calculator outputs, not tuned rewards.

Expected yield for a **one-unit** guaranteed gathering output is 900→400 units/hour from bands 1→6; multi-output action bundles range from 900–4,500 units/hour in band 1 and 400–2,400 in band 6. Crafting completes 1,200→655 recipes/hour; output quantity makes finished units range from 655 to 18,000/hour across recipes. Those figures assume unlimited material supply and uninterrupted station access. They are production ceilings, not proven sustainable economy throughput.

## Economy depth and regional load

The graph has **102 items, 36 gathering actions, 51 node placements, 77 recipes, 148 source links, 197 true consuming sink links, and 75 non-consuming use links**—1.45 sources and 1.93 consuming sinks per item on average. Median item has one source, one consuming sink, and two connected skills. No item lacks a source. The 25 zero-sink items are all reusable tools (13) or equipment (12), not concealed trade/tool-use sinks. Fifty-two items touch at least two skills, 17 touch at least three, and 47 have at least two origin-region labels (which may include `cross_region`).

Ten raw materials first appear in band 1. Five have **direct** recipe demand in band 4 or later (four in band 6); nine reach band 4 or later through downstream transformations. Thus strong *chain longevity* does not imply direct late demand for the original ore/hide/sinew. The database's `cross_tier_reuse_count` follows reachable recipe descendants; use direct `item_sinks` when deciding whether an early raw item itself remains a late-tier input.

| Region tag | Nodes (core / extension) | Recipes (core / extension) | Item region tags | Content observation |
|---|---:|---:|---:|---|
| Lowmark | 12 (6 / 6) | 21 (14 / 7) | 35 | Only region authorized by Phase 1.3 for v1; five node placements are band 1. |
| Thornfell | 13 (10 / 3) | 32 (23 / 9) | 44 | Largest recipe/item association; no band-6 node placement. |
| Mire | 14 (5 / 9) | 19 (10 / 9) | 33 | Most nodes, extension-heavy; only one band-1 node. |
| Emberholt | 12 (7 / 5) | 22 (15 / 7) | 34 | No node placement before band 3. |

Recipe and item region tags overlap; the regional counts must not be summed as unique content. Another 34 recipes carry `cross_region`. Later-region placements, including those for core skills, are analytical planning rather than v1 runtime authorization.

## Decisions to make (illustrative options, not selections)

For time comparisons, **competent = entering band 3; advanced = entering band 5; masterful = cap**. These labels are decision aids, not existing game promises. Scenario arithmetic uses the current `xp_table` and `derive_action_math` formulas with explicitly stated parameter changes; no source database or config was edited.

1. **Skill cap.** Keep all six content bands and the 1,000,000-XP endpoint, redistribute band widths as evenly as possible, and retain current XP/hour targets. **40 levels:** bands of 7/7/7/7/6/6 levels; competent 15 at 22.95 h, advanced 29 at 45.90 h, cap 40 at 64.07 h. **50 levels:** 9/9/8/8/8/8; competent 19 at 24.26 h, advanced 35 at 44.76 h, cap 50 at 64.05 h. **60 levels (current):** six 10-level bands; 21 at 20.00 h, 41 at 40.00 h, cap 60 at 60.00 h. A lower cap does *not* automatically shorten mastery when endpoint XP is held fixed. **Data:** 40/50 require remapping every exact action/recipe unlock and band assignment, not deleting extension content. **Later runtime:** UI, level gates, persistence, and content eligibility would need reconciliation; no cutover is authorized.

2. **Hours to competence / advancement / mastery.** With the current 60-level curve and band boundaries, scale all XP/hour targets uniformly: **focused** at 4/3× gives 15/30/45 h (band-1/6 rates 1,883/43,709 XP/h); **current** gives 20/40/60 h (1,412/32,782); **deliberate** at 2/3× gives 30/60/90 h (941/21,855). **Data:** recalculate action XP and rate tables, then check recipe/input supply against the new hours; the item graph need not change. **Later runtime:** actual play time must be calibrated with travel, downtime, and inventory loops before any rate is shipped.

3. **Band philosophy.** **Three broad 20-level chapters** group current unlocks into 12 actions plus 33/23/21 recipes per chapter and about 20 ideal hours each. **Six 10-level bands (current)** give six actions and 20/13/13/10/9/12 recipes per roughly 10-hour band. **Twelve 5-level micro-bands** yield six half-bands with *no* gathering unlocks; the 46–50 block has no action or recipe unlock at all. **Data:** broad bands mainly change grouping; micro-bands need deliberate re-spacing of existing unlocks or acceptance of empty beats. **Later runtime:** gate presentation and feedback cadence change, but the SQLite grouping alone changes no gameplay.

4. **Gather/craft cadence.** Hold XP/hour fixed and multiply all action durations: **responsive 0.75×** gives band-1/6 gathering 3/6.75 s (1,200/533 one-unit yields/h) and crafting 2.25/4.125 s (1,600/873 completions/h); **current 1×** gives 4/9 s (900/400) and 3/5.5 s (1,200/655); **deliberate 1.25×** gives 5/11.25 s (720/320) and 3.75/6.875 s (960/524). **Data:** adjust action XP inversely and recheck source/sink throughput; this does not decide animation timings. **Later runtime:** interaction feel, animation lock, latency, and resource depletion must be tested separately.

5. **Randomness.** **Deterministic (current):** 100% success, 63/63 guaranteed outputs, no bonus roll. **90% gather success:** one-unit yield falls from 900/400 to 810/360 per hour in bands 1/6; to retain XP/hour under success-only awards, XP per success rises to 1.743/91.061 from 1.569/81.955. **5% optional one-unit bonus:** if an explicitly justified single-entry weighted pool is authored, one-unit expected yield becomes 945/420 per hour; current data have no such pool, so setting the chance alone changes nothing. **Data:** success/weights require explicit probability and reason, not rarity-label inference. **Later runtime:** failure/bonus feedback and player trust need playtest; no RNG is being added now.

6. **Cross-tier reuse strength.** Of ten band-1 raw materials, **retain current selective direct reuse (5/10 with band-4+ inputs)**; **strengthen to 7/10 (+2 materials)**; or **near-universal 9/10 (+4)**. Nine already have *downstream* band-4+ reachability, so the choice concerns direct continuing demand rather than whether their processing chains survive. **Data:** stronger options require meaningful later recipe inputs/sinks, not generic external-use labels or filler items. **Later runtime:** supply pressure and early-zone return value would change only after recipes and gathering are implemented and tested.

7. **Catalog size versus RuneScape-style depth.** **Hold 102 items** and seek depth from the existing 77 transformations and many-to-many sources/sinks; **modest +25% planning envelope** is 128 items (+26), about 96 recipes/185 sources/246 consuming sinks if today's densities are maintained; **broader +50% envelope** is 153 items (+51), about 116 recipes/222 sources/296 sinks. These are arithmetic workload envelopes, *not* an authorization to add items and not a claim of volume parity with RuneScape. **Data:** any expansion must pass purpose, source, sink, overlap, and redundancy audits. **Later runtime:** every new item also carries asset, inventory, crafting, persistence, localization, and QA cost.

**Recommended decision order:** (1) cap and milestone definitions together; (2) desired active hours; (3) band philosophy and unlock spacing; (4) action cadence and sustainable throughput; (5) randomness; (6) cross-tier direct reuse; (7) catalog-volume ceiling. Recalculate after each choice, then playtest before promoting any number to runtime or canon. The current database remains an analytical model throughout.

*Method:* Counts and region/connection facts are SQL queries against `caelmor_economy.sqlite`; XP thresholds, scenario curves, expected action rates, and weighted-bonus examples use `CODE/Scripts/caelmor_progression_calculator.py` with copied in-memory configurations. Hours sum each level's `xp_to_next / target_xp_per_hour` at that level's band. Display values are rounded; the checked-in balance configuration is unchanged.
