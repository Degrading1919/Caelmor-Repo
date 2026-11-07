# Caelmor — Creative Director Rulings: Combat, Ranged and Release Strategy

**Ruled by:** Collin (Creative Director), 2026-11-03.
**Status:** **BINDING.** These rulings supersede conflicting assumptions in every production document, including the Lowmark v1 bible (D-13), the Thornfell bible (TD-7, TD-13 ranged hedge), both encounter packages (§8 non-lethal defeat, Thornfell C-5 and C-8), both integration handoffs, and the long-form narrative architecture.
**Scope of this file:** the ruling text, the Thornfell decisions resolved at the same time, the reconciliation rules every content package follows, the register of scripted story exceptions, the governing-document flags, and the engineering handoff pointer.
**Engineering handoff:** `Caelmor_Combat_Ranged_Release_Engineering_Handoff.md` (same folder). Sol is unavailable; nothing here changes C#, runtime contracts or schemas.

---

## 1. The rulings

| Id | Ruling | Effect on content |
|---|---|---|
| **CDR-1** | **Combat follows the RuneScape defeat model.** Ordinary enemies (humans, animals, monsters) fight until defeated at **0 HP**. No automatic retreat, disengagement or surrender based on remaining health. No universal non-lethal system for human opponents. Bosses ordinarily follow the same model. Individual quests may feature **scripted** surrender, mercy or survival outcomes where narratively justified, as exceptional story events, not general combat rules. | Lowmark D-13 and Thornfell TD-7 are **superseded**. Thornfell's wolf break-off (C-5, I-6) is **removed**. Health-threshold yields (Sallow 20%, Ingrith ~20%, Brigand Foreman 20%, Greymantle 10%) are **removed**. The encounter-level surrender trigger (Thornfell TI-EN-02) is **removed**. See §3 and §4. |
| **CDR-1a** | Keep the approved **three-state quest lifecycle**: Inactive, Active, Completed. | Unchanged. No quest fails because an enemy dies. |
| **CDR-2** | **Ranged is a core combat skill (S01 resolved: included).** Caelmor supports meaningful melee and ranged progression. Woodcutting, Fletching, Hunting, Smithing, Leatherworking and equipment production stay interconnected. Restore Thornfell's intended bow and archery content where appropriate. Ranged is a legitimate approach, **not mandatory** for completing any quest. Combat implementation, balance, items and schemas stay with their specialists. | Thornfell TST teaches the bow for real; "while S01 is open" hedges are removed; Lowmark gains an optional bow beat inside existing hunting content (§3.4). |
| **CDR-3** | **No partial public release.** Caelmor is privately developed and playtested until the complete intended game is implemented. The first public beta contains the complete planned game; the beta is for feedback, problems, balance and refinement. No Lowmark-only launch, no separate regional releases. Regional milestones are **internal production tools**, not release boundaries. Work stays sequential by dependency and roadmap. Do not expand scope or invent content to redefine completeness. | "v1", "v1.5", "ships", "launch" and "release" wording in production files is reconciled to internal-milestone language (§3.5). Governing documents that say otherwise are **flagged** for authoritative revision (§5); they are not rewritten here. |
| **CDR-4** | **RuneScape is the primary structural reference** for interconnected, independently enjoyable questlines; meaningful skill requirements; combat/gathering/crafting/equipment/economy interdependence; memorable quests (exploration, puzzles, unusual characters, danger, discoveries); persistent completion and unlocks; optional activities and side stories. Not copying RuneScape quests, not abandoning Caelmor's atmosphere, grounded combat or canon. **Avoid new mechanics added only for narrative realism when standard RPG systems do the job.** | Applied as a simplification test during reconciliation (§3.6) and in all Mire production. |
| **CDR-5** | Continue production: record the rulings, reconcile content and handoffs, preserve approved lore, quest structure and review work, do not touch C#, authoritative runtime contracts or schemas, document technical changes for Sol. | This file, the reconciliation pass, the engineering handoff, then the Mire foundation. |

**Guiding principle (Director's words):** build Caelmor as a complete, interconnected RuneScape-inspired RPG with its own distinctive world, not as a collection of increasingly elaborate systems that make familiar RPG gameplay unnecessarily complicated.

---

## 2. Thornfell decisions resolved (2026-11-03)

| Thornfell item | Ruling | Status in content |
|---|---|---|
| **TD-7** Human enemies yield | **Superseded by CDR-1.** | Humans fight to 0 HP; Ingrith is the one scripted exception (SX-3). |
| **TD-8** Gatefall sealing works | **Approved:** mechanical deadfalls ordered by horn calls, **without resonance**. FT-02b is narrowed at this one site only. | Promote to approved for Thornfell content (label `[APPROVED — CDR 2026-11-03]`). |
| **Two calendars** | **Approved:** the storekeepers' weeks-to-First-Smoke and the Ridge Wardens' frost-count are separate local reckonings. | Approved. |
| **Thaw** | **Approved:** quest-local presentation state `TSW_THAW`; `TH_SEASON` keeps two values (autumn, snow). | Approved (Encounter C-7 stands). |
| **Open stone** (TWN) | **Approved** as a newly emerging memorial custom. | Approved. |
| **Walking a banner home** (TWC) | **Approved** as **Old Torvek's local tradition** (not a Thornfell-wide custom). | Approved; text says it is Torvek's practice that others are starting to follow, never "the Marchers have always". |
| **S01 ranged scope** (TST bow held as proposal) | **Resolved by CDR-2.** | TST teaches stringing and shooting the stormwood bow. |
| **C-5** Wolves break off at 30% | **Removed by CDR-1.** | Wolves fight to 0 HP. |
| Everything else listed for review in the Thornfell bible §3 and the Batch 2–4 open-decision lists (TGM den UI mute, placement of world elites, TD-1/2/5/9–14, canon promotion) | **Stays in review.** | Unchanged. Nothing else is promoted. |

---

## 3. Reconciliation rules (apply to every Lowmark, Thornfell and future-region package)

### 3.1 Defeat

1. Every hostile creature, human, animal, monster or spirit, is defeated at **0 HP**. No health threshold ends a fight early. No creature flees, limps away, scatters out of the fight, sits down or yields because of its health.
2. **Leash/reset is standard RPG behaviour and stays**: an enemy that is pulled out of its area returns and resets (that is not a retreat). Spirit enemies (Lowmark drift, Thornfell horn-echo figures) still **re-form while their condition lasts**; that is a place rule, not a disengagement.
3. **Presentation of a defeated human:** the ordinary defeat presentation (falls, fades after the standard corpse time, drops ordinary loot). No gore, no lingering bodies in later visits, no "tied" props, no "downed" state, no dialogue with a defeated ordinary enemy. Allies do not comment on mercy. One short, sober ally line after a human fight is enough where the old text had a "they'll live" beat.
4. **Animals** are defeated at 0 HP and can be harvested where the economy allows. **Ambient flocks** (crows, hawks) are ordinary enemies: each bird is defeated at 0 HP; a flock that is not engaged is scenery.
5. **XP, loot and co-op credit** are awarded at defeat exactly as before.
6. **The player can never kill a non-combatant.** Non-hostile NPCs are never targetable. A non-combatant who gives up when their guards are defeated is a quest script, not a combat state (see SX-N below).
7. **Quests cannot fail** because an enemy died (CDR-1a). Every step that previously completed on "yield" now completes on **defeat** (or on the scripted exception event in §4).

### 3.2 Testimony that came from a defeated enemy

The evidence rule stays: **combat never reveals evidence.** Where a story beat used an ordinary enemy's words after a yield, re-source it, smallest change first:

| Pattern | Use when | Example |
|---|---|---|
| **T-1 Ally recognition** | An ally present can plausibly say it | MQ4: Maelin (or Hollis) names the man in the good coat across the chamber: Gideon Sallow, the factor. Rusk fights to 0 HP. |
| **T-2 In-place inspection** | The fact can be read from the place (board, ledger, pay chits on a peg, a cut badge) | Thornfell TPW: the Corner-Boss's cut badge is on the overturned cart; inspecting it gives the "deserter in a Warden's coat" line. |
| **T-3 Non-combatant witness** | A non-fighter is already in the scene (clerk, hornwright, hostage, peddler) | TIW: Bersi (never fights) still gives testimony after his crews are defeated. |
| **T-4 Cut it** | The line was flavour only (TWG lookout, TSG Foreman, TBC bandit) | Drop the line; nothing depends on it. |

Never move evidence into loot. A beat that cannot be re-sourced without changing what the player learns is escalated, not rewritten.

### 3.3 Dialogue

Change **conclusions and lines, not quests.** Keep beats, steps, flags and objectives wherever the only thing that changes is how a fight ends. Rename step objectives only where they promise a capture ("Make them yield" → "Defeat the crew"). Keep step ids. Remove lines that say enemies are tied, walked down, held or spared, unless they belong to a §4 exception. Where an epilogue said crews were "walked down to Passwatch", say the pass is clear.

### 3.4 Ranged (CDR-2)

1. Every encounter can be fought with **melee or ranged**. Never require ranged. Never design a fight that ranged trivialises (e.g., a ledge slinger the player can only answer with arrows is fine; a boss the player can shoot from a place the boss cannot reach is not).
2. Remove every "S01 open", "Ranged only if S01 allows" and "while S01 is open" hedge. Former "ranged optional, melee alternative" counters stay; ranged is now a **first-class** option in them, not a fallback.
3. **Thornfell TST (Stormwood)** teaches Woodcutting → Fletching → Ranged as a real loop: select and cut stormwood, shape and string a stave, fletch a bundle of arrows, shoot at the bowyer's marks. The racked unstrung stave stops being the default; it stays only as the bowyer's own display piece. Item names and stats remain proposals for the economy and item specialists (TD-13 unchanged on catalog authority).
4. **Lowmark** stays melee-led as the introductory region but must not exclude ranged: Lowmark encounters accept ranged, and one **optional** bow beat is added inside existing hunting content: *The Wrong Culprit* (WC, the Hunting intro) lets the player borrow the household eldest's short bow for the optional sow hunt (`WC-D6.12`, returned at `WC-D7.12`), as an alternative to melee. No new quest, no new region flag, no required ranged step.
5. Fletching and Ranged XP values, ammunition rules, weapon catalog, accuracy formula: **not authored here** (Gameplay Designer, Schema & Content Engineer, Systems Engineer).

### 3.5 Release terminology (CDR-3)

| Old wording | Replace with |
|---|---|
| "v1" as a release ("in v1", "ships in v1", "v1 has no …") | "Lowmark" / "the Lowmark milestone" / "in Lowmark content", or "the game" when the sentence is about the whole game |
| "v1.5" as Thornfell's release | "the Thornfell milestone" |
| "launch", "release", "ship", "shippable" for a region | "milestone", "playable", "complete" |
| "post-v1 geography" / "future release" | "later-milestone regions" |
| "Not authored in Thornfell v1.5" | "Not authored in Thornfell content" |

**Do not rename files or ids.** "Lowmark v1" in file names, flags and codes is a historical production label meaning *the first internal production milestone*; it carries no release meaning. `LM_*`, `TH_*`, codes and step ids are unchanged. Economy/Skills documents that use "v1" for catalog tiers (`v1_core`) keep it: that is a content-tier tag, not a release.

### 3.6 Simplification test (CDR-4)

During reconciliation, any runtime need that exists only to stage non-lethal combat is **removed** (yield thresholds, downed state, encounter-level surrender, break-off, hostile→neutral swap for ordinary enemies, tied props). Other elaborate mechanics are **listed, not removed**, in the engineering handoff §4 as simplification candidates for Director/Gameplay review; production content does not depend on removing them.

---

## 4. Register of scripted story exceptions

An exception is **a quest event, not a combat rule.** The creature is defeated at **0 HP** like any other; the quest's defeat hook then plays a scripted outcome instead of the ordinary defeat presentation, and spawns the person as a non-hostile NPC for the following beat. No threshold, no partial-health stop, no general "yield" state. Each one is listed here so the count stays small and visible.

| Id | Who | Quest | Why the story needs it | Outcome at 0 HP |
|---|---|---|---|---|
| **SX-1** | **Joss Garrow, "Old Lantern"** (human miniboss) | Lowmark *Old Lantern* (OL) | The quest is about bringing a lost, half-drowned old Watcher home. He is a victim, not a villain; the choice "bring Joss in alive / bring back only his lantern" is the quest. | He goes down to one knee and sets the lantern down, still lit; the drift-hold on him breaks. The OL choice follows unchanged. |
| **SX-2** | **Gideon Sallow** (human miniboss, `[ANTAGONIST]`) | Lowmark MQ10 *The Crest Hall Reckoning* | He is the human face of the Relief Cut and a witness at the hearing the next morning; his surrender terms, `CR_SALLOW_ACCOUNT` and his MQ12 lock-up exchange are the Act III payoff. | He drops the hook into the basin and grips the gate chain: "Enough. I'm done." `cr.sallow_yield` fires **on defeat**; `CR-D6` follows unchanged. |
| **SX-3** | **Ingrith Scarrow** (human boss, `[SPLINTER]`) | Thornfell TF-M5 *Stonewake* | The Assembly, the closure account and her clan's tribunal at thaw are the region's ending; the hunger-winter truth needs her alive to date her own hunger. | She plants the spear and sits on the drum frame, still counting under her breath. `TSW-D5` follows unchanged. |

**Scripted non-combatant outcomes (SX-N, not exceptions to CDR-1 because these people never fight):**

| Id | Who | Quest | Rule |
|---|---|---|---|
| SX-N1 | **Bersi Coldbrook** (clerk) | Thornfell TF-M2 *Iron Winter* (TIW) | Never fights. When the last crew member in the counting room is defeated, he gives up (scripted) and testifies. The crews fight to 0 HP; no encounter-level surrender. |
| SX-N2 | **Eyvind Stall** (hornwright) | Thornfell TF-M4 *The Summit Hall* (TSH) | Never fights; stopped by the *Take the horn* interaction (unchanged). |
| SX-N3 | Crews who stop because a **story action** ended their task (TSW "cut the pull-line": the haul ends, the crew sit down) | TF-M5 | A puzzle outcome, not a health outcome. Kept. |

**Mercy without an exception.** *Greymantle* (Thornfell TGM) fights to 0 HP and dies. The quest's End/Sleep choice is kept as a choice about **how the old bear is left**: seal the den as his resting place (three stones and Yrsa's stormflower net, "so the wind can't reach him") or leave it to the trappers. Same steps and flags; the 10% lie-down is removed.

Adding an exception later requires the same justification and an entry here.

---

## 5. Governing documents flagged for authoritative revision (not edited)

These are Phase 1 or governance sources. The Master Protocol reserves their revision to the Creative Director, so they are **flagged** with the exact conflict and suggested replacement wording. Until revised, **these rulings govern** wherever they disagree.

| # | Document | Conflict | Suggested revision |
|---|---|---|---|
| G-1 | `01_PRE-PRODUCTION/1.1 Core Vision/Caelmor_Phase1_1_Core_Vision.md` §8 "Scope Constraints for v1" | "No ranged combat or spell systems"; the heading frames scope as a v1 release. | "No player spell system." Remove the ranged exclusion (CDR-2). Retitle §8 "Scope Constraints" (CDR-3). |
| G-2 | `01_PRE-PRODUCTION/1.3 Feature Set & Scope/Caelmor_Phase1_3_FeatureSet_and_Scope_Boundaries.md` §6 (lines ~240–241), Section B "V1.5 Feature Expansion", networking "v1 → v1.5 → v2.0" | "v1 includes ONLY Lowmark Vale … Thornfell Marches becomes v1.5 content." | Lowmark is the introductory region and first internal milestone; the first public beta contains the complete planned game (CDR-3). Networking versions can stay as technical stages if relabelled "architecture stage", not release. §2 "Enemies never flee at low HP" already matches CDR-1 and stays. Ranged (§5) already included; matches CDR-2. |
| G-3 | `01_PRE-PRODUCTION/1.5 Content Strategy/Caelmor_Phase1_5_Content_Strategy.md` header and §1 | "v1 Content Minimums for a Complete, Shippable Core Experience"; "Scope: v1 (Lowmark Vale only)"; "the only region shipping in v1"; "v1 releases with: 1 full region". | Restate as **Lowmark milestone content minimums** (an internal production target). Add a line that the complete game is the sum of the regional milestones plus Convergence per the approved narrative architecture; per-region counts are reused as production targets, not release scope. Do not add counts. |
| G-4 | `00_ADMIN/Reference/Caelmor_Project_Instructions.txt` (development order) | "post-v1 geography". | "later-milestone geography"; keep the priority on a playable Lowmark vertical slice as an internal milestone. |
| G-5 | `00_ADMIN/Reference/Caelmor_Master_Assistant_Protocol.md` §(approval boundaries) | "release scope" is a protected category; no text currently states the CDR-3 release strategy. | Add CDR-3 as the release strategy of record. |
| G-6 | `00_ADMIN/Roadmaps/Caelmor_Roadmap.md` Stages 33–34, 42–43 | "Lowmark Vertical Slice" and "Playable Beta" stages read as if the beta could be Lowmark-only; Thornfell/Mire/Emberholt/Convergence content stages are absent. | State that Stage 42.4 "External Beta Build" requires the complete planned game; add regional content milestones as internal stages ordered by D-R1 (Thornfell → Mire → Emberholt) and Convergence. Technical owners (Sol) to place them. |
| G-7 | Lore-pass audits in `00_ADMIN/Reference/` (Canon Reconciliation Audit, Stage A Contradiction Register S01, Part 6 ledgers, Final Lore Foundation Lock Review, Part 2 Gap Audit) | "Lowmark-only v1", "S01 open". | Historical records; leave as written. Add one note to the Contradiction Register: **S01 resolved 2026-11-03 by CDR-2 (Ranged included).** |
| G-8 | `00_ADMIN/Milestones/Stage 6.1 — Combat Architecture Snapshot.md` (CombatIncapacitated "does not imply death") | Not a conflict: the contract still allows incapacitation for future scripted use. Content no longer *requires* it for humans. | None. Flag only so Sol knows the content dependency is gone. |

---

## 6. Where each ruling was applied

| Ruling | Lowmark | Thornfell | Architecture |
|---|---|---|---|
| CDR-1 | Bible D-13 resolved; encounter §8 rewritten as "Defeat (CDR-1)"; MQ4 Rusk to 0 HP, Maelin names Sallow at dawn (`NF-D9.05`), `S09_rusk` is a slate inspect; MQ6/MQ10 crews to 0 HP; MQ10 Sallow SX-2; MQ11 serpent to 0 HP; NT, UL, TB to 0 HP; OL Joss SX-1 | Bible TD-7 superseded; encounter §8 rewritten; TPW, TIW, TSH, TSW, TWG, TAS, TBC, TSG humans to 0 HP; Bersi SX-N1, Eyvind SX-N2, cut pull-line SX-N3, Ingrith SX-3; wolf break-off and all low-health disperse/scatter removed; Greymantle to 0 HP with the choice reframed | Review §5.0 addendum; §7.1 contract gains a sixth field, Combat compliance |
| CDR-2 | Ranged accepted everywhere; WC optional borrowed short bow; Fletching not taught in Lowmark | TST restored as Woodcutting → Fletching → Ranged; all S01 hedges removed; C-8 rewritten | Contract field |
| CDR-3 | Terminology note in the bible; "v1" release wording replaced across 14 files | "v1.5", "ships", "initial release" replaced; Integration §7 "Milestone scope" | Index §5.3 rewritten; Arcs layer table; D-R1 wording |
| Thornfell decisions | — | TD-8, two calendars, `TSW_THAW`, TWN open stone, TWC banner walk (Old Torvek's way) labelled `[APPROVED — CDR 2026-11-03]`; bible §3.2 settled-items table | Review §5.0 addendum |

## 7. Reconciliation log

| Pass | Result |
|---|---|
| Reconciliation (2026-11-03) | 33 production files reconciled with targeted edits; no file, step, flag or encounter id renamed. Engineering consequences in `Caelmor_Combat_Ranged_Release_Engineering_Handoff.md`. |
| Calls made under delegated authority (Director may revisit) | (1) Lowmark MQ10: Sallow's surrender terms now cover his **river hands**, bargemen taken up by the keepers who never fought, so `CR_CREW_LENIENCY` keeps meaning. (2) Thornfell TSG: Gerrit's two former crewmen die in the fight; the ledge choice keeps its flags and now turns on Gerrit standing surety for his remaining crew. (3) MQ4 `S09_rusk` kept as a slate inspect rather than retired. (4) TWC knot-per-bearer stays in review (only the banner walk was approved). (5) Non-combatants who run at the first blow (TIW clanless hires) and story-triggered bird lifts (TSH-E1, TIW-E3) kept: they are not health outcomes. |
| Independent review (2026-11-07) | Two independent reviewers, one per region, re-grepped every Lowmark and Thornfell file in full against CDR-1/2/3 and checked cross-file coherence. **Lowmark:** 9 defects fixed (WC bow attached to the sow hunt encounter WC-E2 in every file; serpent `driven_off` and goblin group scatter removed from the handoffs; two leftover "v1" phrases; EV08 label; Act I removed-id note; Rusk cast note; TB objective "Stop the goblins"; young pole-man's line now varies with `CR_CREW_LENIENCY`). **Thornfell:** 7 defects fixed (TPW wolves "driven off"; cut-badge inspect text; TSW Beat 4 now states her crew fight on and `TSW-D5` opens when the floor is clear; TGM zone state and Yrsa's bark no longer assume a live bear; TST verbs; one voice repeat). No high-severity defect. Left open for the Director: Maelin now knows Sallow's pay arrangements and the Lamb back room (within her limits?); "Lock men" now means unfought river hands; TWC-D2.03 calls the knot-per-bearer "the old way" while that custom is in review; TBC-B5.04 "I wasn't going to cut it. Much." kept as mid-fight banter. |
