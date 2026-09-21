# Creative Director balance decision package

**Decision status:** the **skill-cap, progression-milestone, non-combat fixed-base-XP architecture, anti-monotony progression guardrail, generalized-exponential curve family, final curve coefficients A = 8 and K = 15, milestone-time targets, 5,000,000 XP level-99 display scale, resulting 1–99 cumulative threshold table, Lowmark gathering-output randomness model, and selective layered cross-tier reuse model are closed for analytical design**. Final non-combat activity XP values, XP/hour, action cadence, catalog-volume ceiling, and runtime implementation remain open. The checked-in `balance_config.json`, generated legacy XP curve, SQLite progression bands, and all 60-level calculations below remain a **legacy provisional analytical baseline**, not approved balance and not runtime canon. No runtime, schema, JSON, SQLite, calculator-code, or C# cutover is authorized by this document.

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

---

## Closed progression design — XP curve and time-to-milestone philosophy

This section closes the remaining **level-progression design gaps**. It establishes tuning targets, not runtime rates. "Engaged skill hours" means ideal time actively progressing that discipline; it is not elapsed account time and excludes travel, downtime, market activity, inventory friction, quests, combat interruptions, social play, and other non-training activity.

### Mastery horizon

Caelmor targets a **long-form 99 journey of approximately 135–150 engaged skill hours**, with **145 hours as the nominal analytical target**.

The purpose is not to reproduce RuneScape's XP table or grind length. The purpose is to preserve the emotional qualities that make long-term skill progression memorable: recurring personal goals, attachment to training places and methods, visible permanent progress, knowledge-driven efficiency, and a final achievement that can become part of the character's identity.

The 99 journey must feel like a long relationship with a discipline rather than a mandatory wall blocking normal play.

### Nominal milestone timing targets

| Milestone | Identity | Nominal engaged time from level 1 | Acceptable early tuning envelope | Design meaning |
|---|---|---:|---:|---|
| **30** | Novice complete | **~11 h** | ~10–12 h | Basic loop learned; player is a confident apprentice rather than a beginner. |
| **50** | Competent complete | **~31 h** | ~28–34 h | Skill is dependable; player has meaningful personal routines and choices. |
| **70** | Advanced complete | **~63 h** | ~58–68 h | Knowledge and efficiency clearly distinguish experienced players. |
| **80** | Practical mastery | **~90 h** | ~85–92 h | Most practical functionality is available; the player should feel almost mastered. |
| **99** | Cap / Completion | **~145 h** | ~135–150 h | Long-term dedication, identity, and commemoration. |

Nominal incremental commitment is therefore approximately:

- levels 1–30: **11 h**
- levels 31–50: **20 h**
- levels 51–70: **32 h**
- levels 71–80: **27 h**
- levels 81–99: **55 h**

This places practical mastery at roughly **62% of the full nominal journey**, leaving about **38%** after level 80. That late tail is intentional: practical mastery and numerical completion are different achievements.

### Closed curve formula, coefficients, XP scale, and threshold table

Use the **RuneScape-like generalized exponential curve family**, independently tuned for Caelmor rather than copying OSRS or RS3 XP totals.

The authoritative formula is:

```text
Weight(L) = L + 8 × 2^(L / 15)

RawXP(L) = Σ Weight(i), for i = 1 to L-1

RequiredXP(L)
    = round(
        5,000,000 × RawXP(L) / RawXP(99)
      )
```

Closed parameters:

```text
A = 8
K = 15
XP99 = 5,000,000
```

The authoritative threshold table is:

```text
03_CORE_SYSTEMS/Skills & XP v1/Caelmor_XP_Threshold_Table.csv
```

Selected closed thresholds:

| Level | Cumulative XP | Share of level-99 XP |
|---:|---:|---:|
| 30 | 221,617 | 4.43234% |
| 50 | 652,858 | 13.05716% |
| 70 | 1,549,627 | 30.99254% |
| 80 | 2,324,814 | 46.49628% |
| 90 | 3,475,278 | 69.50556% |
| 99 | 5,000,000 | 100.00000% |

The table has monotonic XP-to-next-level growth from **2,224 XP for level 1→2** to **198,978 XP for level 98→99**. There are no flat or reversed level-cost jumps and no special final-level multiplier.

The curve remains subordinate to the already-closed pacing philosophy: representative fixed-XP activities and believable methods must still reproduce the approved milestone-time envelopes without hidden player-level XP scaling.

### Closed non-combat fixed-base-XP architecture

For authored non-combat skilling/economy activities:

- the same authored action under the same conditions has the same base XP regardless of player level;
- player level itself does not invisibly multiply the action's base XP;
- higher-level activities may award higher fixed base XP when they are genuinely different activities;
- better methods, tools, routes, resources, access, preparation, knowledge, and separately authorized modifiers may increase XP/hour;
- target XP/hour is an analytical result or diagnostic, not an automatic generator of per-action XP.

This preserves stable activity identity. An iron-mining action does not become worth more base XP merely because the player reached a higher Mining level.

This architecture is limited to non-combat skilling/economy XP. It does not define Melee, Ranged, combat encounter XP, quest XP, or other future XP-source models.

Derived milestone times must still satisfy the closed Creative Director pacing envelopes. If they do not, tune representative activity rewards, access, method composition, tools, or other explicit gameplay factors without introducing hidden player-level XP scaling.

### Closed anti-monotony progression guardrail

**REPETITION MAY BE FAMILIAR, BUT PROGRESSION MUST NOT BE MERELY RESKINNED REPETITION.**

Caelmor welcomes relaxing, familiar skilling loops, but a higher-level activity is not a meaningful progression beat merely because it changes resource name, level requirement, XP reward, action duration, yield, visual model, or required tool tier.

Meaningful progression should deepen appropriate combinations of player knowledge, route and location choices, resource distributions, preparation, tool or station decisions, processing and cross-skill relationships, economic purpose, world or quest context, environmental constraints, risk/reward choices, alternate methods, efficiency discoveries, and decisions about what to gather, make, keep, process, or sell. Interaction structure may change occasionally where justified, but complexity must not be added merely for novelty.

This guardrail preserves Caelmor's existing rules: **slow but rewarding, never slow and empty**; repetition is acceptable when purposeful; no filler resources or recipes; fewer, deeper systems; knowledge-driven efficiency; meaningful world attachment; and RuneScape-inspired feeling without copying RuneScape implementation.

Representative-method calibration must pass **both** numerical pacing and experiential progression. A method set is rejected even if it perfectly reaches the 11 / 31 / 63 / 90 / 145-hour targets when long stretches are dominated by mechanically interchangeable tier replacements.

**Validation question:** Does this progression band materially change what the player learns, chooses, routes around, prepares for, connects to, or values — or is it primarily the same action with a different unlock?

If it is primarily the latter, revise the content or method structure rather than adding another resource tier.

### Progress-pulse rule

Ordinary level-ups are valid rewards even when they unlock no new object or action. The permanent number increase, visible approach to a self-selected goal, and increasing mastery are themselves part of the progression loop.

Authored unlock density should therefore be **lower than numerical level density**. Selected milestone levels should carry mechanical, world, efficiency, or identity meaning; intervening levels may exist primarily as satisfying progress pulses.

### Method-discovery rule

The 135–150 hour completion target is **not** permission to force every player to progress at one fixed rate. Caelmor should preserve room for knowledge-driven efficiency.

A player who learns better routes, preparation, resource relationships, tool choices, processing chains, or other legitimate skill-specific efficiencies should be able to outperform a less-informed player without bypassing the identity of the journey. Future XP/hour tuning should therefore define a reasonable baseline method and a meaningful but controlled efficiency ceiling rather than one universal rate.

### Practical-mastery boundary

By approximately level 80:

- the player should possess most core practical functionality;
- the skill should feel complete enough to use confidently across ordinary high-level play;
- remaining unlocks should be specialist, prestigious, unusually efficient, or otherwise exceptional;
- no fundamental feature necessary to understand or enjoy the discipline should be withheld merely to populate levels 81–98.

This protects the 80–99 tail from becoming compulsory grind while preserving a strong voluntary long-term goal.

### What remains deliberately unresolved

This closed design direction does **not** yet define:

- baseline or optimal XP/hour;
- action durations;
- final XP per gather/craft/completion;
- success or failure probabilities outside the closed Lowmark Hunting and Woodcutting output model;
- resource yield rates;
- exact unlock levels inside each identity band;
- runtime formulas or implementation.

Those values must be derived later from the approved milestone timing targets and playtested against actual travel, input supply, world friction, economy throughput, and skill-specific activity structure.

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

2. **XP curve / coefficients / scale / threshold table / milestone pacing — CLOSED.** Use the selected RuneScape-like generalized exponential family with **A = 8**, **K = 15**, and **5,000,000 XP at level 99**. `Caelmor_XP_Threshold_Table.csv` is the authoritative 1–99 threshold table. Nominal cumulative engaged-time targets remain approximately level 30 = 11 h, level 50 = 31 h, level 70 = 63 h, level 80 = 90 h, and level 99 = 145 h, with the approved envelopes retained. Final per-action XP, baseline XP/hour, and optimal XP/hour remain downstream calibration values derived from representative fixed-XP activities and believable methods.

3. **Band / unlock-spacing philosophy — PARTIALLY CLOSED; anti-monotony criterion CLOSED.** Broad identity bands are fixed by the approved milestone structure. Ordinary levels may be progress pulses and do not require an action, recipe, item, or new mechanic. Exact authored unlock positions remain open and should be determined skill-by-skill from mechanical purpose, world logic, cross-skill dependencies, memorable milestone density, and the closed anti-monotony guardrail rather than a requirement to populate every numerical level. Mechanically interchangeable tier replacements do not by themselves justify major progression beats. Existing six 10-level analytical bands are not approved progression bands for the 99-level model.

4. **Gather/craft cadence — OPEN.** Hold XP/hour fixed and multiply all current legacy action durations: **responsive 0.75×** gives band-1/6 gathering 3/6.75 s (1,200/533 one-unit yields/h) and crafting 2.25/4.125 s (1,600/873 completions/h); **current 1×** gives 4/9 s (900/400) and 3/5.5 s (1,200/655); **deliberate 1.25×** gives 5/11.25 s (720/320) and 3.75/6.875 s (960/524). **Data:** adjust action XP inversely and recheck source/sink throughput; this does not decide animation timings. **Later runtime:** interaction feel, animation lock, latency, and resource depletion must be tested separately.

5. **Lowmark gathering randomness — CLOSED.** Hunting HM1–HM8 and Woodcutting WM1–WM8 use deterministic primary outputs, no random gathering-failure roll, and no random bonus-output roll. Invalid opportunities, player execution failures, deliberate refusals, readable world-condition losses, closures, and nonproductive work can still produce no material because they are authored states or consequences rather than chance failures. Raw hide and tannin-rich bark remain source-conditional guaranteed outputs. Fixed authored-action XP, approved cadence, and approved throughput remain unchanged. This ruling does not authorize the legacy 102-item catalog or silently decide randomness for unrelated future systems.

6. **Cross-tier reuse strength — CLOSED: SELECTIVE LAYERED REUSE.** Processed construction, fuel, fitting, lining, and maintenance goods retain direct late demand when aspirational construction or repair physically consumes them. Source goods may remain indirectly relevant through legitimate conversion without being forced into late recipes. Ordinary wood retains direct civic and ordinary-market relevance plus indirect Smithing relevance through charcoal. Early Hunting and woodland areas remain useful through dense source-to-process relationships. Universal capstone inputs, prestige material tiers, filler sinks, and reuse-percentage quotas are rejected.

7. **Lowmark v1 catalog-volume ceiling — READY FOR CREATIVE DIRECTOR APPROVAL.** Recommend a target of **40–55 player-facing item identities** and **24–36 player-facing recipe or service identities**, with hard planning ceilings of **64 items** and **48 recipes/services**. Counts are separate. Workshop-only states, provenance, condition, relationship placeholders, and internal process steps do not become catalog entries. Exceeding either ceiling requires a demonstrated missing function, the purpose/source/sink/progression/non-redundancy test, implementation-capacity review, and explicit Creative Director approval. The legacy 102-item catalog is reference material only and supplies no target.

**Next decision order:** (1) approve or revise the Lowmark v1 catalog-volume ceiling; (2) define the minimum Cooking catalog and exact equipment/tool forms inside the approved envelope; (3) validate recipe quantities, repair frequency, source/sink throughput, and implementation burden before runtime promotion.

*Method:* Counts and region/connection facts are SQL queries against `caelmor_economy.sqlite`; legacy 60-level XP thresholds, scenario curves, expected action rates, and weighted-bonus examples use `CODE/Scripts/caelmor_progression_calculator.py` and the checked-in provisional configuration. The approved 99-level cap, milestone identities, fixed-base-XP architecture, anti-monotony progression guardrail, generalized-exponential family, coefficients `A = 8` / `K = 15`, 5,000,000 XP scale, and authoritative 1–99 threshold table are Creative Director progression decisions. The 145-hour nominal mastery horizon and milestone timing targets remain analytical acceptance constraints rather than a per-action reward formula.
