# Creative Director balance decision package

**Decision status:** the **skill-cap and progression-milestone philosophy is Creative Director approved and closed**. Decisions about XP curve shape, XP/hour, action cadence, RNG, cross-tier reuse, and catalog expansion remain open. The checked-in `balance_config.json`, generated XP curve, SQLite progression bands, and all 60-level calculations below remain a **legacy provisional analytical baseline**, not approved balance and not runtime canon. No runtime, schema, JSON, or C# cutover is authorized by this document.

Phase 1.3's seven `v1_core` skills and Lowmark-only v1 geography remain distinct from the seven `economy_extension` skills and later-region analytical planning.

## Closed Creative Director decision — skill cap and milestone philosophy

### Approved cap

- **Skill cap: 99.**
- RuneScape / OSRS / RS3 are emotional and structural reference points, not implementation templates. Caelmor intentionally uses a 99-level horizon for long-term attachment and recognizable progression tradition, while retaining its own progression bands, content density, pacing, economy, world structure, and mastery philosophy.
- A high numerical cap does **not** imply one authored resource, recipe, tool, tier, or other unlock per level.

### Approved progression identities

| Levels | Identity | Intended player feeling |
|---|---|---|
| 1–30 | **Novice** | "I am learning this discipline and discovering what it contains." |
| 31–50 | **Competent** | "I can depend on this skill and make informed choices." |
| 51–70 | **Advanced** | "I understand this discipline; knowledge and efficiency distinguish me." |
| 71–98 | **Masterful** | "I have substantial command of this discipline and am refining it." |
| ~80 | **Practical mastery point** | The player should feel almost mastered in practical terms. |
| 99 | **Cap / Completion** | "I completed something that became part of my character's identity." |

These are progression identities, not declarations that every skill must place identical content at identical individual levels.

### Mechanical meaning of the stages

**NOVICE — levels 1–30**

The player learns the discipline, discovers its basic loop, becomes increasingly useful, and forms early memories around locations, materials, tools, and routines. Novice does not mean helpless. The broad internal emotional movement is orientation → familiarity → confident apprenticeship.

**COMPETENT — levels 31–50**

The player can rely on the discipline for useful independence and make informed choices about where, why, and how to train or produce. This band should support personal routines and preferences rather than a single prescribed route.

**ADVANCED — levels 51–70**

Knowledge, routing, preparation, cross-skill understanding, and efficiency increasingly distinguish experienced players from beginners. Advanced progression should deepen system connections rather than depend on endlessly replacing early materials with disposable higher-tier equivalents.

**MASTERFUL — levels 71–98**

Mastery begins before the numerical cap. By approximately **level 80**, the player should feel that they practically know the discipline. Most core practical skill functionality should be available by this point or by the broader masterful stage.

Levels above the practical mastery point should emphasize **refinement, specialization, exceptional opportunities, personal goals, and dedication**. A small number of post-80 functions may be extremely rewarding, but they should be **specialist capabilities**, not missing essentials required for the discipline to feel complete.

The intended distinction is:

- **~80:** "I have mastered the practical discipline."
- **80–98:** "I can pursue things even many masters do not."
- **99:** "I completed the journey."

**CAP / COMPLETION — level 99**

Level 99 is primarily an **identity and commemorative achievement**, not a mandatory final power spike. Cap recognition should eventually make the achievement memorable and personally significant without forcing ordinary practical completeness to remain locked behind the final level.

### Level-density rule

**A level does not require an unlock. A milestone requires meaning.**

Ordinary levels are allowed to function as **satisfying progress pulses**. Selected levels and broader stage transitions carry the authored mechanical, world, efficiency, and identity beats. This rule exists to preserve a long progression horizon without creating filler resources, filler recipes, dead catalog growth, or solo-developer content burden merely to populate 99 numerical rungs.

### Expansion rule

Future skill-cap increases remain a legitimate expansion tool. If a skill later rises beyond 99, reaching 99 must retain its historical and emotional significance rather than being retroactively treated as "not actually mastery." A later increase should read as a **new chapter beyond an established mastery landmark**, not as invalidation of the player's previous completion.

### Downstream balance consequence

The next progression decision pass must rebuild XP-curve and time-to-milestone analysis around this approved structure. No approved conclusions about hours-to-30, hours-to-50, hours-to-70, hours-to-80, or hours-to-99 exist yet.

Do **not** remap content, regenerate XP tables, alter `max_level`, change action timing, tune XP/hour, change RNG, or alter runtime systems solely from this decision. Those are separate downstream tasks.

---

## Legacy analytical baseline — what the current numbers produce

The current calculator still uses a 60-level power curve (exponent 2.4, 1,000,000 XP at level 60). Every included skill has the same XP/hour target in a given band: the seven configured core skill profiles have no modifiers, and extension skills use the calculator's default 1.0 multipliers. Gathering awards XP on success; crafting awards XP per attempt. Success is 100%, all 63 gathering outputs are guaranteed, and weighted bonus chance is zero.

**These values are retained only so the existing analytical economy remains reproducible until the approved 99-level progression is deliberately retuned. They must not be interpreted as the new cap, milestone timing, or approved mastery duration.**

| Band / levels | XP/hour, every skill | Ideal hours through band | Gather seconds / attempts per hour | Craft seconds / completions per hour | New actions / recipes |
|---|---:|---:|---:|---:|---:|
| 1 / 1–10 | 1,412 | 10.00 (to 11) | 4 / 900 | 3 / 1,200 | 6 / 20 |
| 2 / 11–20 | 6,042 | 10.00 (to 21) | 5 / 720 | 3.5 / 1,029 | 6 / 13 |
| 3 / 21–30 | 12,272 | 10.00 (to 31) | 6 / 600 | 4 / 900 | 6 / 13 |
| 4 / 31–40 | 19,620 | 10.00 (to 41) | 7 / 514 | 4.5 / 800 | 6 / 10 |
| 5 / 41–50 | 27,872 | 10.00 (to 51) | 8 / 450 | 5 / 720 | 6 / 9 |
| 6 / 51–60 | 32,782 | 10.00 (to 60) | 9 / 400 | 5.5 / 655 | 6 / 12 |

Selected time-to-level from level 1: **10: 7.77 h; 20: 18.57 h; 21: 20.00 h; 30: 28.75 h; 40: 38.82 h; 41: 40.00 h; 50: 48.86 h; 60: 60.00 h.** These are ideal active-action hours, not elapsed play time: travel, inventory, node contention, inputs, stations, selling, and failure are not modeled. Seven core skills at 60 ideal hours apiece imply 420 single-skill training hours if all seven are mastered independently; this is not a player completion-time forecast and is now obsolete as a mastery model because 99 is the approved cap.

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

## Remaining Creative Director decisions

The old 60-level shorthand of "competent = entering band 3; advanced = entering band 5; masterful = cap" is **retired**. Approved identities are now Novice 1–30, Competent 31–50, Advanced 51–70, Masterful 71–98, practical mastery around 80, and Cap 99. Existing 60-level time comparisons below are legacy scenario arithmetic only and cannot answer the new milestone-timing questions.

1. **Skill cap and milestone philosophy — CLOSED.** Cap 99. Novice 1–30; Competent 31–50; Advanced 51–70; Masterful 71–98; practical mastery around 80; Cap/Completion 99. Most practical functionality is available by practical mastery. Post-80 rewards are specialist opportunities. Cap is primarily identity/commemoration. Future cap increases remain permissible while preserving 99 as a historical mastery landmark. Ordinary levels are satisfying progress pulses and do not each require authored unlocks.

2. **XP curve / hours to competence, advancement, practical mastery, and cap — OPEN.** The former 60-level scenarios (15/30/45 h focused, 20/40/60 h current, 30/60/90 h deliberate at old band boundaries) are now historical comparison points only. The next pass must decide curve shape and desired active time to levels 30, 50, 70, ~80, and 99 before deriving XP/hour targets.

3. **Band / unlock-spacing philosophy — PARTIALLY CLOSED.** Broad identity bands are now fixed by the approved milestone structure, but exact authored unlock spacing inside those bands remains open. The governing rule is that ordinary levels may be progress pulses; not every level needs an action, recipe, or item unlock. Existing six 10-level analytical bands are not approved progression bands for the 99-level model.

4. **Gather/craft cadence — OPEN.** Hold XP/hour fixed and multiply all current legacy action durations: **responsive 0.75×** gives band-1/6 gathering 3/6.75 s (1,200/533 one-unit yields/h) and crafting 2.25/4.125 s (1,600/873 completions/h); **current 1×** gives 4/9 s (900/400) and 3/5.5 s (1,200/655); **deliberate 1.25×** gives 5/11.25 s (720/320) and 3.75/6.875 s (960/524). **Data:** adjust action XP inversely and recheck source/sink throughput; this does not decide animation timings. **Later runtime:** interaction feel, animation lock, latency, and resource depletion must be tested separately.

5. **Randomness — OPEN.** **Deterministic (current):** 100% success, 63/63 guaranteed outputs, no bonus roll. **90% gather success:** one-unit yield falls from 900/400 to 810/360 per hour in legacy bands 1/6; to retain XP/hour under success-only awards, XP per success rises to 1.743/91.061 from 1.569/81.955. **5% optional one-unit bonus:** if an explicitly justified single-entry weighted pool is authored, one-unit expected yield becomes 945/420 per hour; current data have no such pool, so setting the chance alone changes nothing. **Data:** success/weights require explicit probability and reason, not rarity-label inference. **Later runtime:** failure/bonus feedback and player trust need playtest; no RNG is being added now.

6. **Cross-tier reuse strength — OPEN.** Of ten legacy band-1 raw materials, **retain current selective direct reuse (5/10 with band-4+ inputs)**; **strengthen to 7/10 (+2 materials)**; or **near-universal 9/10 (+4)**. Nine already have *downstream* band-4+ reachability, so the choice concerns direct continuing demand rather than whether their processing chains survive. **Data:** stronger options require meaningful later recipe inputs/sinks, not generic external-use labels or filler items. **Later runtime:** supply pressure and early-zone return value would change only after recipes and gathering are implemented and tested.

7. **Catalog size versus RuneScape-style depth — OPEN.** **Hold 102 items** and seek depth from the existing 77 transformations and many-to-many sources/sinks; **modest +25% planning envelope** is 128 items (+26), about 96 recipes/185 sources/246 consuming sinks if today's densities are maintained; **broader +50% envelope** is 153 items (+51), about 116 recipes/222 sources/296 sinks. These are arithmetic workload envelopes, *not* an authorization to add items and not a claim of volume parity with RuneScape. **Data:** any expansion must pass purpose, source, sink, overlap, and redundancy audits. **Later runtime:** every new item also carries asset, inventory, crafting, persistence, localization, and QA cost.

**Next decision order:** (1) XP curve shape and desired time to 30/50/70/~80/99; (2) exact unlock spacing inside the approved identity bands; (3) action cadence and sustainable throughput; (4) randomness; (5) cross-tier direct reuse; (6) catalog-volume ceiling. Recalculate only after the relevant Creative Director choice, then playtest before promoting derived rates to runtime.

*Method:* Counts and region/connection facts are SQL queries against `caelmor_economy.sqlite`; current legacy XP thresholds, scenario curves, expected action rates, and weighted-bonus examples use `CODE/Scripts/caelmor_progression_calculator.py` and the checked-in provisional configuration. The approved 99-level cap and milestone identities are Creative Director design decisions; no replacement XP table or rate model has yet been authored.
