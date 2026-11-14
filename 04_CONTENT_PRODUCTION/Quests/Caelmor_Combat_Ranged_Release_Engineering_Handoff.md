# Caelmor — Engineering Handoff: Combat, Ranged and Release Rulings (for Sol)

**Date:** 2026-11-03. **Author:** Creative Production (narrative). **For:** Sol (Systems Engineer / Technical Director) and the Schema & Content Engineer, when available.
**Source rulings:** `Caelmor_Director_Rulings_Combat_Ranged_Release.md` (CDR-1 to CDR-5).
**What this is:** the technical consequences of the rulings, written down so engineering can integrate them later. **Nothing here was implemented.** No C#, runtime contract, schema or production JSON was changed by the narrative pass.

---

## 1. Summary for engineering

| Area | Before (content asked for) | Now (rulings) | Net engineering effect |
|---|---|---|---|
| Human defeat | Health-threshold yield (20% Sallow/Ingrith/Foreman, 0% others), downed state, hostile→neutral NPC swap, tied/bound props, encounter-level surrender trigger | Every creature is defeated at 0 HP with the ordinary defeat flow | **Removes** a planned runtime mechanism (Lowmark EV08 `creature.yielded`, M18; Thornfell TI-EN-01/02/03). Simpler. |
| Animal low-health behaviour | Ridge wolves break off at 30% and count as defeat; Greymantle lies down at 10% | Fight to 0 HP | **Removes** break-off AI and a lie-down threshold event. |
| Named story exceptions | (part of the yield mechanism) | Three named creatures (SX-1 Joss Garrow, SX-2 Gideon Sallow, SX-3 Ingrith Scarrow) run a quest-scripted outcome **on defeat** | **One small hook** (§2). |
| Ranged | Optional, hedged on S01 | Core combat skill alongside melee | Ranged combat, Fletching and ammunition become required systems for the full game (§3). Content never *requires* ranged to finish a quest. |
| Release | Lowmark-only "v1", Thornfell "v1.5" | One public beta with the complete planned game | Roadmap / build-pipeline framing only (§5). |
| Quest lifecycle | Inactive / Active / Completed | Unchanged | None. |

The approved combat contract (Stage 6.1: CombatIncapacitated "does not imply death") is **not** changed. Content simply no longer depends on incapacitation for humans.

## 2. The one new hook: quest-scripted defeat outcome

**Need.** A creature definition (or a quest step bound to a specific creature instance) can declare **`on_defeat → quest event`**. When that creature reaches 0 HP:

1. Its combat participation ends as for any defeat (XP, co-op credit as normal; loot per its table).
2. Instead of the ordinary death presentation and corpse despawn, the quest plays a short scripted presentation (an animation pose plus one bark) and **spawns a non-hostile NPC** of the same person at that spot with a dialogue entry point.
3. The quest event fires (e.g., `cr.sallow_yield` for SX-2), advancing the step.
4. If the player dies or leaves before step completion, the creature resets per the encounter's normal reset rule.

**Users (complete list):** SX-1 Joss Garrow (Lowmark OL), SX-2 Gideon Sallow (Lowmark MQ10), SX-3 Ingrith Scarrow (Thornfell TF-M5). Phase checkpoints on these fights stay as authored.

**Implementation note (suggestion only).** This is ordinary quest scripting (quest listens for a defeat event of a tagged creature instance, then swaps it for an NPC). It should not be a general combat state. It can likely reuse the existing quest-event and NPC spawn paths once quest step tracking exists (Roadmap 31.2/31.3/31.5).

**Non-combatants** (Bersi Coldbrook in TIW, Eyvind Stall in TSH) never enter combat; their "give up" beats are quest scripts triggered by *other* creatures' defeat or by an interaction. They need no combat support.

## 3. Ranged (CDR-2)

| Need | Owner | Notes |
|---|---|---|
| Ranged as a core combat skill with its own progression | Systems Engineer, Gameplay Designer | Phase 1.3 §5 already lists Ranged ("bow/crossbow combat, stat-driven accuracy"). |
| Ranged attack resolution on the 10 Hz tick (range, line of sight, ammunition consumption) | Systems Engineer | Combat implementation and balance stay with specialists. Content assumes ordinary RPG ranged rules: equip bow, have ammunition, attack at range. |
| Fletching outputs (bows, arrows) and ammunition items | Schema & Content Engineer, economy pass | Stage 3.2 "Ranged weapon cores" class exists. Thornfell stormwood and Lowmark short-bow names in content are **proposals**; derive real items through the economy pipeline. |
| Enemy behaviour against ranged players | Gameplay Designer | Content rule: no fight can be trivialised by shooting from a spot the enemy cannot reach (ordinary leash/reset handles this). |
| Teaching content | (authored) | Thornfell *Stormwood* (TST): cut → shape/string → fletch → shoot. Lowmark *The Wrong Culprit* (WC): optional borrowed short bow. |

## 4. Runtime needs removed from content handoffs

| Removed need | Was in | Replaced by |
|---|---|---|
| Health-threshold yield event (EV08 `creature.yielded`, M18; Sallow 20%, Ingrith ~20%, Brigand Foreman 20%) | Lowmark integration G20/EV08/M18; Thornfell TI-EN-01, TI-EN-03 | Ordinary defeat at 0 HP. EV08 is renamed **`creature.scripted_defeat`** and used only by SX-1/SX-2/SX-3 (§2). |
| Downed state, hostile→neutral swap for ordinary enemies, `CombatIncapacitated` dependency for humans | Lowmark encounter §8, integration EV07 outcomes `downed`/`yielded` | Ordinary defeat presentation. |
| Tied / bound props and custody presentation | Lowmark MQ4, MQ6, NT; Thornfell TPW, TIW, TSH, TSW, TBC | None. |
| Encounter-level surrender trigger (first yield, ~60 s timer, proximity to a non-combatant) and the TIW surrender timer | Thornfell TI-EN-02, TI-CK-05 | Bersi's give-up is a quest predicate on "all TIW-E5 crew defeated". |
| Wolf break-off at 30% (and "disperse"/"scatter" at low health for wolves, crows, goblins, hawks "driven off") | Thornfell C-5, I-6, TI-EN-06, TSN-E1, TSW-E1, TTH, TSM, TNR, TSL-E2; Lowmark TB | Fight to 0 HP. Standard leash/reset kept. |
| Greymantle 10% lie-down and "untargetable until S06" | Thornfell TGM | Defeat at 0 HP; body kept as a per-player prop until `S06_choice` (fallback: authored body prop). |
| Serpent "drive off" outcome (EV07 `driven_off`, `SV_SERPENT_DRIVEN`) | Lowmark MQ11 | Defeat at 0 HP. The flag id is kept but never set. |
| Group rout (TB goblins) | Lowmark TB | Each goblin defeated at 0 HP. |

**Small predicate changes (ordinary quest tracking, no new system):** Lowmark MQ4 `S09_rusk` is now an inspect predicate (Rusk's slate); `LM_LOCK_STATE` is written by the smash/chain interaction completions rather than bark lines; Thornfell TSG `S04`/`S05` start on the Foreman's defeat; TPW gains a cut-badge inspect prop. Lowmark *The Wrong Culprit* needs a dialogue item **loan and return** (give/take a short bow and arrows).

## 5. Release and roadmap framing (CDR-3)

- No partial public release. Stage 42.4 "External Beta Build" should require the complete planned game (all regional milestones plus convergence per the approved architecture).
- Regional content milestones are internal; place them as roadmap stages in dependency order (Lowmark → Thornfell → Mire → Emberholt; Lowmark return; convergence). Owners: Sol / Technical Director.
- Networking stages in Phase 1.3 ("v1 host-authoritative → v1.5 dedicated → v2.0 shards") are technical architecture stages, not releases; suggest relabelling. Flagged in the rulings §5 (G-2, G-6); not edited.
- `v1_core` tags in economy/skills data are content tiers, not releases; no change.

## 6. Change log from the reconciliation pass

Applied 2026-11-03 to all Lowmark and Thornfell production packages (quests, dialogue, bibles, encounters, zones, integration) and the narrative architecture. Each file carries its own "Director rulings reconciliation (2026-11-03)" log row. Line ids that were cut are kept in place as "(removed: CDR-1)" so references do not dangle: Lowmark `NF-B4.3`, `NF-D6.04`, `NF-D7.01–.40` (`NF-D7` is now the slate inspect), `NF-D8.01/.03`; Thornfell `TPW-B3.5`, `TIW-B6.2`, `TIW-B9.4`, `TSW-B3.7`, `TSW-B4.8`, `TWG-D2.*`, `TAS-D4.*`, `TSG-D2.01/.10/.20`. New lines: Lowmark `NF-D9.05/.06/.50`, `WC-D6.11–.13`; Thornfell `TST` steps `S06b_fletch`, optional `TST-E2`, barks `TST-B5.07–.13`, `TST-B7.08–.09`.

**Ranged needs added by content (Thornfell TST, Integration EC-05..EC-08):** Ranged skill, a bow, bowstring, arrows, Fletching recipes, a stringing channel, a shootable target set (the Stonewake butts as a public practice station). Optional in TST: wind drift on arrows (fallback: authored hit chance) and a per-arrow quality check. Ranged is never required outside TST's teaching step, and TST keeps a non-ranged alternative path.

## 7. Simplification candidates (CDR-4) for Director / Gameplay review

Collected by the reconciliation workers. **Not removed**: each has a fallback or is bounded content. Listed so Gameplay and engineering can replace them with standard RPG systems where cheaper.

| Region | Candidate | Standard alternative |
|---|---|---|
| Lowmark | MQ11 follower trance state machine (four states) | Escort follower with one "stopped" state |
| Lowmark | The Muster's tether with per-stone "reading" flags | Fixed safe stones per phase |
| Lowmark | MQ10 per-bundle smoulder/singe timers; Sallow's rope-cut and relight lanterns | One fire timer; static lighting |
| Lowmark | MQ6 band-counter brace with plank lift-out physics | Channelled interaction |
| Lowmark | Joss's Wade (path ring check toward the deep side) | Plain phase-3 move set |
| Lowmark | Per-player presentation hour (MQ4), per-player Lock prop state, per-player dream layer (TB), observation volumes ("stops when watched", WD/UC) | Shared world state with quest-phased props |
| Lowmark | NT cart-targeting thieves, lantern-lit pathing block, immune slow-aura allies | Defend-the-point encounter |
| Lowmark | "Hunting resolution, not a combat kill" (FK, WC) | Defeat then harvest |
| Thornfell | Close-count quest clock with held final pip; TSW forced shelter holding the storm; five-window storm state (TES, three-window fallback exists); TES-E4 break-gap timers | Ordinary timed objective |
| Thornfell | Per-player Narrows bridge state machine N0–N4; per-player gate state; three co-op prop fallback styles (Q-06) | Quest-phased bridge props |
| Thornfell | TIW haul advancing only while the player is in zone | Ordinary timer |
| Thornfell | Held-note breath bar and the new `call-blown` completion type (TTH/TWG); hornman Rest-cancel window | Standard interaction with a success check |
| Thornfell | TGM null-point UI/audio mute, dust-curtain occlusion, pillar-stun collision | Visual-only telegraphs with UI intact |
| Thornfell | TST wind-drift arrows and tillering-board curve UI | Standard ranged hit roll; single craft action |
| Thornfell | TSM wolf "snatch the carry"; TSL lightning hazard with 10% HP floor; TSL-E2 brace input; TWC colour-bearing carry state with sail push | Ordinary hazards and a carry item |
| Thornfell | TSG cutter work bars that pause when engaged; terrace drop gated on three Answers; TBC chalk-board load planner | Simple progress interactions |

## 8. Solo completion (CDR-6, 2026-11-14)

The Creative Director ruled that every quest is fully completable by one player; co-op is optional assistance (rulings CDR-6, §3.7). For engineering this means:

- **No multiplayer system is a prerequisite of quest completion.** Quest tracking, flags, choices and rewards are per player. A partner's progress, presence, disconnection or host role never decides another player's step.
- **Shared credit** is ordinary: an encounter or task credits a partner only when their own active step consumes it.
- **Shared-world presentation** (partners at different steps seeing different crossing states, water stages or props) stays documented as presentation questions for Sol (Mire Integration Q-18, Thornfell Q-06, Lowmark §8.1). These are not blockers for building the solo questline, and content will not add runtime needs only to support elaborate co-op mechanics.
- **Bosses** are tuned for solo completion; any optional multiplayer scaling must not compromise it.

The per-region solo-completion sweep (2026-11-14) is logged in the rulings file §7 and in each package's review log.
