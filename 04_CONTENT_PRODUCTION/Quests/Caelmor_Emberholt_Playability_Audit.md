# Caelmor: Emberholt Playability Audit

**Date:** 2026-11-15
**Audience:** Collin (Creative Director), Sol (systems and Unity), Gameplay Designer (GD)
**Package audited:** the Emberholt quest package at commit `fb83110` (the independent-review fixes for the 2026-11-15 Emberholt character rulings), read on `main` at `e1c8ea8`. No file under `04_CONTENT_PRODUCTION/` and no gameplay source under `CODE/Systems/Gameplay/` changed between those two commits; the commit in between is Lowmark asset benchmarking under `UNITY/` and `CODE/Scripts/architectural_generator/`.

## 0. What this document is

**This is an authored-content and systems-contract walkthrough. Nothing in it was played or tested.** Emberholt is not implemented in Unity. "Playable" below means "logically playable on paper": the step predicates, flags, items, routes, death and logout rules and co-op rules can be followed from start to finish without contradiction, and the runtime capabilities they assume are named. Whether any of it plays well can only be learned from a build (section 7).

The walkthrough was made after the 2026-11-15 Emberholt character rulings (D-E2, D-S1, D-EL, ED-3; Review §5.0) had been applied, so it reads the package in its post-rulings state.

### Scope

All Emberholt content files under `04_CONTENT_PRODUCTION/`:

| Short name | File |
|---|---|
| Bible | `Quests/Caelmor_Emberholt_Narrative_Production_Bible.md` |
| Act I, Act II, Act III | `Quests/Caelmor_Emberholt_Main_Act_I.md`, `_Act_II.md`, `_Act_III.md` (EH-M1 to EH-M6: ECW, EEH, EGH, EAC, ESS, EGA) |
| Act I/II/III dialogue | `Dialogue & Narrative/Caelmor_Emberholt_Main_Act_I_Dialogue.md` (and II, III) |
| Unburnt, Commons, Work, Combat | `Quests/Caelmor_Emberholt_Side_Quests_Unburnt_and_Names.md`, `_Commons_and_Wards.md`, `_Work_and_Skills.md`, `_Combat_and_Discovery.md` (micro-events EME and discoveries EDS are in Combat) |
| Enemies | `Enemies/Caelmor_Emberholt_Encounter_and_Enemy_Requirements.md` |
| Zones | `Zones/Caelmor_Emberholt_POI_and_Zone_Requirements.md` |
| Integration | `Quests/Caelmor_Emberholt_Integration_Requirements.md` |

Reference sources: `Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md` (CDR-1 to CDR-6, §3.7 solo completion), `Quests/Caelmor_Narrative_Architecture_Review_and_Authoring_Sequence.md` §5.0, `00_ADMIN/Reference/Caelmor_Part4_Character_Family_Continuity_Ledger.md`, `UNITY/README.md`, `Quests/LowmarkGameplay_Integration.md`, `Quests/Caelmor_Lowmark_v1_Integration_Requirements.md`, the Thornfell and Mire integration files, the Mire playability audit, and a read of `CODE/Systems/Gameplay/GameplayContent.cs` and `GameplaySession.cs`.

### Method

1. **Solo pass, main line.** One solo player traced step by step through EH-M1 to EH-M6 and their dialogue, with the bible, Enemies, Zones and Integration rows they use: unlock predicates and flags, walk-away and resume, escort and multi-level dependencies, ranged safe spots, hazards, skill levels, the item budget, the EAC single-outcome path, ESS-D12, revelation ownership and post-completion dead ends. Finding ids `EM-01` to `EM-16`.
2. **Solo pass, side content.** The same check for the twenty side quests (EME01 to EME10 and EDS01 to EDS10 are the micro-events and discoveries in the Combat file). Finding ids `ES-01` to `ES-17`.
3. **Co-op pass.** Two characters progressing independently, walked as six pairings at different quest stages, under CDR-6 (section 5). Finding ids `CO-01` to `CO-09`.
4. **Technical-dependency pass.** Every runtime need in the packages compared with what current source and `UNITY/README.md` demonstrate. Finding ids `TD-01` to `TD-14`.
5. **Verification of High findings.** Each High finding was re-checked against the repository files before inclusion (see the note under section 1).
6. **No fixes in this pass.** Findings are recorded with a proposed bounded fix. Fixes follow in a separate pass (section 9).

Every finding keeps its original id. Exact duplicates found by more than one pass are merged and both ids are kept; one merge was made (CO-01 and TD-12). Related but distinct findings are cross-referenced, not merged.

### Status labels

| Label | Meaning |
|---|---|
| **Resolved** | The bounded fix (or a later ruling) is in the files and was checked against them (status column, 2026-11-15). |
| **Partly resolved** | The text side is done; what remains and its owner are named. |
| **Open** | Recorded; no file changed. (At first issue every finding was Open; see the status column and §1 "Status at 2026-11-15".) |
| **Open: Sol / Director / GD** | The named owner decides; no option chosen. |
| **Untestable** | Cannot be assessed until a playable Unity build exists. |

Severity: **High** (softlock, blocked progression, broken predicate, or a contradiction a player would hit), **Medium**, **Low**. Categories: **A** definite authored-content contradiction; **B** likely gameplay or pacing problem; **C** technical dependency for Sol; **D** Director-level decision; **E** cannot be assessed until a playable build exists.

### Boundaries kept in this audit

- **Enemies C-1 (1.5-second telegraph minimum for displacement) and C-2 (25% hazard protection) are authored tuning requirements pending Gameplay Designer review**, not approved universal combat rules. Where this audit says a telegraph "meets the 1.5 s figure", that is a check against a pending requirement.
- **The Mire MI-CO-06 pattern (Integration EI-CO-06 here) is a presentation fallback only.** The host's personal quest state is never authoritative over another player's progression. This audit chooses no networking architecture.
- **No geography was changed or proposed.** Every MAP VERIFICATION REQUIRED flag is kept (section 8). Map-dependent questions are recorded as questions.
- **No art, material, texture or colour is prescribed.**
- **No new feature, quest, character or lore is proposed.** Proposed fixes delete or simplify where they can.
- **Open Director items stay open:** ED-15, ED-7, ED-20, EDI-1 to EDI-4 and geographic placement (section 6).

---

## 1. Summary

### Status at 2026-11-15

The 55 findings reconciled against the two fix passes (`cce3031`, section 9), the CDR-6 shared-credit revision (§3.7 item 2a, `b45b809`) and the Director decisions of 2026-11-15. Each row in sections 2 to 7 now carries a status; every **Resolved** High and Medium finding was re-checked against the file text. Sections 1 to 8 otherwise keep the audit as written.

| Owner | Resolved | Partly resolved | Open | Total |
|---|---|---|---|---|
| Fixed in content (no owner left) | 28 | — | — | 28 |
| Sol | — | 10 | 6 | 16 |
| Director | — | — | 3 | 3 |
| Gameplay Designer | — | — | 1 | 1 |
| Playable build | — | — | 7 | 7 |
| **Total** | **28** | **10** | **17** | **55** |

High findings: ES-01, CO-01 and CO-03 Resolved; TD-01 and CO-02 Partly resolved (Sol). The two 2026-11-15 rulings follow-ups (Elyndra's shrine, the name "Iven") and the Hallam Drost rename are Resolved by the Director.

**Outstanding, by owner**

- **Sol (partly resolved, text side done):** TD-01 the repeating heat hazard and zone state (High; not designed here); CO-02 the deep-main family for the post-EGA Sentinel (High, co-op only); EM-07 confirm EI-QS-11 as MUST for EGA `S06`; TD-03 multi-level form; TD-04 "place at anchor" effect; TD-05 mobile pursuit; TD-06 escort-follow; TD-07 NPC lifecycle; TD-11 logout placement; TD-13 adopt the simplified forms.
- **Sol (open):** TD-02 channel cancel on heat ticks; TD-08 keep-watch build form; TD-09 sequence ends as flags; CO-06 heat state in co-op; CO-07 per-player NPC copies; CO-08 per-player hour and frost.
- **Director (open):** EM-13 (ED-7, the EH-M3 gate); EM-14 R09 by inference; ES-10 ESK hook direction; the EM-07 respawn alternative. Carried, not approved, alternatives kept: ED-7, ED-15, ED-20, EDI-1 to EDI-4. Geographic placement: map owner.
- **Gameplay Designer (open):** EM-08 EAC Option B length; also C-1 and C-2 and the EM-06 `[GD]` levels as ordinary tuning.
- **Playable build (open):** EM-15, EM-16, ES-14, ES-15, ES-16, ES-17, TD-14.

### Verdict

**Solo: logically playable as authored, with one region-wide stall and a heat system that does not yet exist.** A fresh character can reach every main-line completion on paper. The unlock chain is honest and visible, every `EH_*` flag the main line sets has one writer that runs before its readers, the quest-item budget is five of five, every required step has a time-cost route, ranged is never required, and the EAC single outcome is clean. No authored softlock was found on the main line. The worst solo problem is in how the main line meets the side content: once EH-M5 is Completed, the next Cinderwall entry auto-starts EH-M6 and pins the player's single presentation hour, so every side step that needs a keep watch stalls until EH-M6 is finished (ES-01). The largest risk is technical: the heat system, which is nearly every required route, is filed as an existing standard capability, but current source has only once-only, target-bound hazards (TD-01).

**Co-op: optional assistance under CDR-6; it never gates solo completion.** With partners at the same step, the packages are coherent apart from three text contradictions about credit (CO-04, CO-05, CO-09). With partners at different steps, quest-state barricades, the post-EGA Sentinel and the "all defeated" predicates of three resonance fights can strand or stall the co-op session (CO-01, CO-02, CO-03). These affect co-op presentation and pacing only; leaving the session clears each one.

### Top issues, in priority order

| # | Issue | Category | Status |
|---|---|---|---|
| 1 | **Heat is filed as an existing standard capability but is not demonstrated.** Current hazards fire once, bound to a target, and never re-arm; there is no periodic area damage, safe niche volume, zone state or repeating vent, plate or ring-sector cycle. Build order step 2 assumes it exists (TD-01). | C, High | Partly resolved: relabelled; runtime Open: Sol |
| 2 | **The EH-M6 frost pins the player's only presentation hour,** so every side step that needs a keep watch, a dusk, a night or a morning stops until EH-M6 is finished. Only EME01, EME02 and EME05 exclude the frost; EGT cannot be met as written (ES-01, ES-02, related ES-06). | B, High | Resolved |
| 3 | **"Carry-state" has two contradictory definitions.** Under "walk, cannot attack", two required fights (ECN `S04`, EAD `S04`) start with a carry-state held and the EWQ crossbow cannot be fired; implemented as Lowmark carries, documents and tokens would be lost on reload (ES-03, TD-10). | A, Medium | Resolved |
| 4 | **Thalan's escort after `EAC-D9.42` resumes in the wrong place.** Logout and death send the player back to the ring niche with Thalan beside them after he has left; under the fixed-recovery-point fallback he would rejoin above the shaft he never climbs (EM-02, EM-03). | A and C, Medium | Resolved |
| 5 | **Co-op shared state can strand a partner:** quest-state barricades are movement blockers (CO-01, merged TD-12); a completed host shows an inert Sentinel to a partner who must fight it (CO-02); "all defeated" predicates can never be met while a partner's condition keeps forms re-forming (CO-03). | C and B, High (co-op only) | CO-01 and CO-03 Resolved; CO-02 Partly resolved, Open: Sol |
| 6 | **Cross-quest flags missing from the persistence list** (Integration §3.2), including `EGH_INITIATE_JOURNAL`, which CV-M4 needs for R19 (EM-05). | A, Medium | Resolved |
| 7 | **A dialogue-chosen skill route has no stated rule for a player below the level,** a possible softlock (EM-06). | B, Medium | Resolved |
| 8 | **Multi-level, NPC movement and mobile pursuit** are assumed on required beats: the EH-M4 shaft, the Tavi, Veska, Darven and Yorven walks, and enemies that follow onto the rim (TD-03, TD-04, TD-05, EM-04). Fallbacks exist or are proposed for each. | C, Medium | EM-04 Resolved; TD-03, TD-04, TD-05 Partly resolved, Open: Sol |

### High findings: verification

All five High findings were re-checked against the repository files. None was wrong; none was dropped.

- **ES-01** holds: Act III §9.3 (l.487) pins "this player's presentation hour at dusk … at night from `S02` to the `S06` keep-watch"; Act I l.80 defines one per-player hour; Integration EI-HT-02 scopes zone pins to a step but no rule scopes the EGA hour pin to EGA's own areas. Note: the stall lasts until EH-M6 is finished, so it is blocked progression, not a permanent softlock.
- **CO-01** holds: Act I l.1138 and l.1160, Act II l.285, l.404 and l.443, Zones l.215 and l.283, and Integration EI-PP-03 ("= LM", MUST) all describe barricades that close routes by quest state; Zones ML-07 confirms the bypass and the annex street door serve EGH `S07`.
- **CO-02** holds: Act III §E (l.670) and §12 (l.569) as quoted.
- **CO-03** holds: Act I l.340 and l.1078 and Act II l.738 require "all defeated"; Enemies I-20 treats the shared re-form source as presentation only. Marked "possible" in effect: it depends on how Sol drives the shared re-form condition.
- **TD-01** holds: `HazardDefinition { id, target, once; all, none; windup, damage; radius, pushDistance }` (`GameplayContent.cs` l.98), and `Hazards()` (`GameplaySession.cs` l.268 to l.285) skips a hazard whose `once` flag is set and adds that flag when it fires. Integration EI-HT-03 and EI-HT-05 are marked "= LM" and Integration R-9 and R-11 "Standard".

---

## 2. A. Definite authored-content contradictions

Format per row: ID, severity, location, evidence, problem, proposed bounded fix, status at 2026-11-15.

| ID | Sev. | Location | Evidence | Problem | Proposed bounded fix | Status (2026-11-15) |
|---|---|---|---|---|---|---|
| **EM-01** | Medium | Zones §6.1 HZ-09, HZ-10; Zones §5A ML-05b; Integration EI-HT-07 | HZ-09 "EH-M3 **S03** Cool or Surging by the flarecap"; HZ-10 "EH-M3 **S04** Working"; ML-05b "EH-M3 **S04** Option B"; EI-HT-07 "G4 by the flarecap … EGH **S03**". Act I §C9.1 puts the flarecap pin in `S02_mouth` ("G4 pinned Cool/Surging by cap") and the drain in `S03_fall`. | Zones §6.1 says it is "canonical for implementation; quest packages defer to this register". Followed as written, G4 sits at its default (Cool) during the flarecap lesson in `S02`, so "follow the pale" has no Surging stretches to teach, and the pin lands one step late. | Change HZ-09 and EI-HT-07 to `S02` (the G4 pin), and HZ-10 and ML-05b to `S03` (the drain). Step numbers only. | **Resolved** (`cce3031`, Fixer 2; HZ-09 and EI-HT-07 read `S02`, HZ-10 and ML-05b read `S03`; verified) |
| **EM-02** | Medium | Act II §A11 Logout row and §A7 Death row; Zones §6.6 EH-M4 | §A11: "the ring's edge niche (`S05`–`S07` before the climb). A player who logs out during the walk resumes at the edge niche with Thalan beside them." At `EAC-D9.40` to `.42` Thennek takes Thalan into the side cut at the shaft foot, before the climb. | A logout or death between `EAC-D9.42` and the top of the shaft sends the player back to the ring with Thalan beside them after he has left. That contradicts the scene and repeats the escort. | After `EAC-D9.42`, set the logout and respawn point to the shaft-foot niche (or Maeryn's shop), with no Thalan. | **Resolved** (`cce3031`, Fixers 1 and 2; Act II §A7/§A11 and Zones §6.6 respawn at the shaft-foot niche after `EAC-D9.42`, no Thalan; verified) |
| **EM-05** | Medium | Integration §3.2 (and EI-FL-02 "must survive completion"); Act I §A9.2 | §3.2 omits these main-line cross-quest reads: `ECW_RAT_SEEN` (`ESS-D5.03`); `EGH_WORK_ORDER` and `EGH_ORDER_SHOWN` (`ESS-D4.03`/`.04`); `EGH_SHEET_READ` (`EAC-D2.10`; §3.2 lists only ENW); `EGH_STONE_HEARD` (`EAC-D1`; §3.2 lists only EMS); `EGH_KEEP_SEEN` (`EGA-I23`); `EAC_SLATE_READ` (`EGA-I22`); `ESS_LETTER_READ` (`EGA-I33`); `EEH_TAVI_STRUCK` (`EGA-D11.30`); `EGH_INITIATE_JOURNAL` (CV-M4 binding, R19). Separately, `ECW_SOB_HEARD` is listed as "Deliberately read by none" (Act I §A9.2 says the same), yet the Act II header and ESS `S03` state that the Rat's price reads it. | If the implementer persists only what §3.2 lists, every line Acts II and III promise drops silently, and the Iven Calder journal flag CV-M4 needs may not persist. `ESS-D5.07` was checked: the option is not flag-gated, so nothing softlocks. | Add the rows to §3.2. Correct the `ECW_SOB_HEARD` "read by none" note in Integration §3.2 and Act I §A9.2. | **Resolved** (`cce3031`, Fixers 1 and 2; §3.2 rows added incl. `EGH_INITIATE_JOURNAL`; `ECW_SOB_HEARD` read by ESS; verified) |
| **EM-09** | Low | `ESS-D12.01` to `.40` | `ESS_ELYNDRA_HEARD` is set only at `ESS-D12.40`. The node is reached only by prose ("→ ESS-D12.01 options, then ESS-D12.40"). The only explicit exit from the option list is "Another time → END (no flag)". | The flag and her closing line may be unreachable as written. Nothing gates on it, so the impact is flavour and the once-per-player rule. | Add an explicit option "(Leave her to the vent.) → ESS-D12.40" once any question has been asked. | **Resolved** (`cce3031`, Fixer 1; "(Leave her to the vent.)" option; verified) |
| **EM-10** | Low | Integration EI-IT-01 Notes | "Reappears in EH-M6 and CV-M4 from the strongbox." Act I header: "never granted again as an item". Act III §9.5: Yorven lays it on the board's ledge as a prop. | Could be read as a re-grant, which would put the item budget over five. | Change the note to "shown as a world prop in EH-M6 (inspect only); never re-granted". | **Resolved** (`cce3031`, Fixer 2; world prop only, never re-granted; verified) |
| **EM-11** | Low | Integration EI-KW-01, EI-KW-02 consumers | EI-KW-01 lists ECW `S01`, EAC `S03`, EGA `S06`, EMS and ETB. It omits ECW `S05` Option B (Cooling House bench), EEH `S02` Option B (Maeryn's stool) and `S03` (morning), EAC `S02` (dusk for Asera), and ESS `S01`/`S05`/`S06` (dusk, and the anteroom overnight). | Each is a required wait on a solo path. If keep watch is built against the listed consumers only, they break. | Add the consumers. Text only. | **Resolved** (`cce3031`, Fixer 2; consumers added; verified) |
| **EM-12** | Low | Zones §6.6 EH-M2 row vs Act I §B7 Death | Zones: "M1 practice court". Act I: the practice court during `S01`, `S03`, `S05`, `S06`, `S07`, and "at the Cooling House otherwise" (`S00`, `S02`, `S04`). | The registers disagree. If `S02`/`S04` deaths respawn at the court, the walk back to the Cinderweave workshops is longer. | Align Zones §6.6 to Act I §B7. | **Resolved** (`cce3031`, Fixer 2; verified) |
| **ES-02** | Medium | Unburnt EGT.3 unlock, EGT.4 A, `S01_batch` | Unlock is "EH-M5 Completed"; the stall is "[NEW sub-site of EP02, under an arch in the slag lanes]" (Cinderwall); `S01`: "Help Glassmoth make up a batch **before dusk**." | The first time the player can reach the stall after EH-M5 is the entry that starts the frost night, pinned at dusk. EGT can only be played inside the frost or after EGA `S07`, and "before dusk" cannot be met in the frost. Consequence of ES-01. | Offer EGT from `EGA_THAW_SEEN`, or hold it under the ES-01 rule. Delete "before dusk" from `S01`. | **Resolved** (`cce3031`, Fixer 2; held to `EGA_THAW_SEEN`; "before dusk" deleted; verified) |
| **ES-03** | Medium | Integration EI-CA-04; Act III `S01` blankets; EFC `S03`; ESK `S03`; ESP `S04`; EFS `S04`; EOP `S03`; ECN `S01` to `S05`; EAD `S01` to `S05`; EWQ EWS-09, `S05` to `S06`; EMS `S03` | EI-CA-04: carry-states "(blocks climb, agility and sprint)". Act III, EFC, ESP, EFS, EOP: "walk, cannot attack". ECN: the stamped cock and "Carry-state: the complaint" are held through `S04_pits` (ECN-E1/E2). EAD: "The wrap is carry-state and stays wet until used", held through `S04_cut` (EAD-E1). EWQ: "lent warden crossbow (carry-state, returned)", shot in `S05` and carried through the `S06` boar fight. EMS: receipt stub "carry-state, kept" with no end. | The two definitions contradict each other. Under "cannot attack", two required fights (ECN `S04`, EAD `S04`) start while the player holds carry-states, and the EWQ crossbow cannot be fired. No set-down point is named. Related: TD-10 (the technical side). | Define two classes in EI-CA-04. **Bulky** (crate, sod, cart, stone, blanket bundle, case, bucket): walk, cannot attack. **Small** (paper, cock, wrap, string, rubbing, lens): no movement limit. Make the EWQ crossbow a "lent tool" (the Work file already uses that term). Make the EMS stub the existing `EMS_RECEIPT` flag only. | **Resolved** (`cce3031`, Fixer 2; EI-CA-04 bulky and small classes, lent tool, class note in each side file; verified) |
| **ES-04** | Medium | Combat EOP §0.1, `EOP-D1.30`; Enemies §11 EW-03 | `EOP-D1.30`: "Boars come down the Ash Roads to the warm stones most dusks. Learn on them." EW-03, the only world boars, is gated "After EWQ or EOP" (Enemies l.509, l.518: EOP-E1 and EWQ-E1 are "ONCE →WORLD (EW-03)"). | EOP's accept needs Hunting `[GD: low–mid]`, and boars are the only Hunting source named. A player who has not done EWQ finds no boars, so EOP is quietly gated on EWQ. | Open EW-03's Ash Roads pocket after EH-M1 (drop "After EWQ or EOP" for that half). Alternative, more text: `EOP-D1.30` points to Ryl's range (EWQ). | **Resolved** (`cce3031`, Fixer 2; EW-03 Ash Roads pocket after EH-M1; verified) |
| **ES-07** | Low | Zones §7 item 2 vs Commons ECN `S05_court` | Zones: "ECN N8 at night". ECN: "the presentation hour moves to **dusk** if earlier". | Two different hour pins for the same step. | Align Zones to dusk. | **Resolved** (`cce3031`, Fixer 2; verified) |
| **ES-08** | Low | Bible §8.1 R09 and R12 "Seeds before payoff" | R09 seeds list "*The Half-Name Wall*"; R12 lists "*Glassmoth's Tonic*". | ENW unlocks after EH-M3 (R09's payoff) and EGT after EH-M5 (R12's payoff), so neither can seed before the payoff. Both package files correctly say "Supports". | Bible text only: move both to a "deepens after payoff" note. | **Resolved** (`cce3031`, Fixer 1; verified) |
| **ES-09** | Low | Bible §6 "Skill hooks"; ED-11 | "Smithing carries the hook in three milestones and **two side quests**." | The side files put Smithing hooks in ESR, ETB, ENW, ECC and EOM, plus the ESK intro and EWQ's optional heads. | Bible text: "and several side quests (ESK, EOM, ESR, ETB, ENW, ECC)". | **Resolved** (`cce3031`, Fixer 1; verified) |
| **ES-13** | Low (possible) | Unburnt EST.3 "Revelation role" | "One line carries the canon R19 shadow (Kaelen's dream of being called from below) … (bible §8.2)". | Bible §8.2's R19 seed list does not include it (checked: §8.2 R19 row). | Drop the "(bible §8.2)" citation, or add the line to §8.2 if the Director wants it as a seed. | **Resolved** (`cce3031`, Fixer 2; citation dropped; verified) |
| **CO-04** | Medium | Act III §7.1.4 (l.396); Enemies §6.1 (l.282), against Enemies §13 (l.562) and Integration EI-CO-01 | "A collar shut during a shared fight … is recorded as kept for each partner whose own active step is `S06`" against "shutting a collar … advances only the acting player's step" and "Every … collar … counts only for the partner who performs it". | Direct contradiction, partly inside the Enemies file. The first rule gives a partner persisted `EGA_COLLARS` progress through another player's action (§3.7.2). | Delete the "recorded as kept for each partner" sentence in Act III §7.1.4 and Enemies §6.1. Live collar state in a shared fight is presentation; `EGA_COLLARS` persists only the acting player's own shuts. | **Resolved** (`cce3031` removed the contradiction; the 2026-11-15 shared-credit revision, `b45b809`, then replaced the per-player wording under CDR-6 §3.7 item 2a: a collar shut in the shared fight counts for every present partner on `S06` and persists in each one's `EGA_COLLARS`; Act III §7.1.4, Enemies §6.1 and §13, EI-CO-01 agree; verified) |
| **CO-05** | Medium | Unburnt §0.6 (l.112); EST.10 (l.283); ETB.10 (l.617); ENW.10 (l.1237); EGT.10 (l.1520) | §0.6 gives "their own instance of every quest NPC scene (phased), every prop that a step reads", then says "A partner may help with a shared task (smother cloth, pump a bellows, brush a wall)". EST.10: "A partner in the back room may lay cloths and pull the damper; each part credits only a player whose own active `S04` consumes it." | Ambiguous whether a partner's cloth counts toward the other player's EST `S04` parts. If it does, it conflicts with §0.6's own "never completes another player's step", with EI-CO-01, and with Work and Skills ("a partner's stitching never completes the player's step"). It also contradicts per-player phased props. | Align with EI-CO-01: a partner's actions count only toward their own step in their own instance. Delete the five credit sentences ("may lay cloths / pump the bellows / hold the stock / brush beside / carry crates or hold the blank"), or mark them as flavour with no effect. | **Resolved** (`cce3031`; reworded by the shared-credit revision, `b45b809`: Unburnt §0.6 follows §3.7 item 2a, shared tasks done together credit every present partner on that step, lessons, carries, readings and choices stay personal; package rows read "Per §0.6"; verified) |
| **CO-09** | Low | Act I §A11 (l.396) | "A partner who has completed EH-M1 is addressed as 'warden's hand' in the other's `S07` and stands at the end table." | Partner-aware dialogue and placement that exists only for co-op; a runtime need for co-op flavour only (§3.7.6). | Delete the sentence. The address variant already follows each player's own `S06` completion. | **Resolved** (`cce3031`, Fixer 1; verified) |

---

## 3. B. Likely gameplay or pacing problems

| ID | Sev. | Location | Evidence | Problem | Proposed bounded fix | Status (2026-11-15) |
|---|---|---|---|---|---|---|
| **ES-01** | **High** | Act III §6 `S00_frost` trigger and §9.3; Act II "Unlocks across Act II"; side files §0.5/§0.6 ("Waiting … at a keep-watch bench is always available"); Combat EME01/EME05 | Act III §9.3: `EGA_FROST` "pins this player's presentation hour at **dusk** until `S01` … at **night** from `S02` to the `S06` keep-watch". EH-M6 auto-starts on the next Cinderwall entry after EH-M5. Act I defines a single per-player hour. Every Ridge quest leaves by "Cinderwall's working gate". | Once EH-M5 is Completed, the first Cinderwall entry freezes the player's hour. Every side step that needs an hour change stops until EGA `S07`: Option B "keep watch until morning" in EWA, ECN, EBL, ESR, EST, ETB, ENW, EOM, ESH and others; EBL night and morning; ETB morning; ESK, ESR and EOP dusk. No side file mentions this. Only EME01, EME02 and EME05 exclude the frost. A player who saves side content for after EH-M5 hits a keep watch that does nothing; progression is blocked until EH-M6 is finished. | One shared rule (each side file §0.5, Act III §9.3, Zones §7): the EGA hour pin governs only EGA steps and the frost-variant areas (W1 to W4, upper Undercroft). Side steps placed there are held while `EGA_FROST` is set and resume at `EGA_THAW_SEEN`, as EME01 and EME05 already do. Keep watch elsewhere advances normally. EDI-3 stays open. Related: ES-02, ES-06, CO-08. | **Resolved** (`cce3031`, Fixers 1 and 2; hour-pin scope rule in Act III §9.3, the four side files and Zones §7; verified. EDI-3 stays Open: Director) |
| **CO-03** | **High** (co-op stall; leaving clears it; solo unaffected) | Act I `S06_circle` (l.1078) "EGH-E3 all defeated + valve bled"; `S06_surge` (l.340) "Three cocks bled + every ECW-E3 enemy defeated"; Act II `S04_sleep_rooms` (l.738) "ESS-E1 all defeated and `ESS_BRAZIERS_OUT`"; Enemies §13 (presentation questions: ECW-E3 cap, ESS-E1 cap, EGH-E3 pulse) | The packages treat a shared enemy that reads a per-player prop as presentation only that "never changes a solo fight". The step predicates require "all defeated". | If the shared re-form condition follows a partner whose valve, cocks or braziers are unfinished, forms keep re-forming, and a player who has finished their own condition can never meet "all defeated" while paired. A partner's state then decides this player's completion, against §3.7.3. | For each of the three predicates: "all defeated" counts for a player once their own condition has ended and no form is engaged with them. Otherwise the predicate needs Sol's F1, F4 or F5. Add a note to Enemies I-20 that this is a predicate question, not only presentation. | **Resolved** (`cce3031`; reworded by the shared-credit revision, `b45b809`: the encounter clears for every present partner on that step, a partner on another step is never held; verified in Act I l.340, l.1078, Act II l.738. Shared re-form presentation stays a Sol presentation question, Enemies §13) |
| **EM-06** | Medium (possible softlock) | `ECW-D7.03` (Option A/B as dialogue options); `EAC-D9.01`; Integration EI-SK-01/04 | The skill route is chosen by a dialogue option ("I'll make it" → `ECW-D7.10`; "(Forge a drift…)" → `EAC-D9.05`). No node returns to the choice, and no rule states what happens to a player below the `[GD]` Smithing level. EI-SK-04 covers only side-quest starts. | A player who picks the skill route without the level may be unable to forge, with no authored way back to the time-cost route. Depends on implementation; not stated anywhere. EEH `S02`, EGH `S03`, ESS `S04` and EGA `S03` choose by action and are unaffected. | One rule in Integration §2.15: a skill-route option is shown only when the level is met (with a decline line), or the choice node is re-offered at Veska or Asera. No new content. | **Resolved** (`cce3031`, Fixer 2; EI-SK-05; verified. Level values are ordinary `[GD]` tuning) |
| **EM-07** | Medium | Act III §7 Rules (Death), §7.1.4; Integration EI-QS-11 (COULD) | "A beaten player always wakes at the warming house (W2)". Quest travel to the U10 door niche is "COULD. Fallback: walking". | Each Draw Sentinel retry (a 6 to 8 minute fight) costs a walk from W2 through U1, U5, U7, U8 and U9 to U10. Walk-away and resume prompts are remaining work. A pacing drag at the capstone. | Raise EI-QS-11 to MUST for `S06` only (Sol). The alternative, a U10 door-niche respawn, conflicts with bible §10.1, so that option is the Director's. **Note:** TD-13 proposes cutting EI-QS-11; the two fixes conflict. Recommended reconciliation: keep EI-QS-11 for EGA `S06` only and cut it elsewhere. | **Partly resolved:** EI-QS-11 scoped to EGA `S06` (`cce3031`); Sol confirms it as MUST (**Open: Sol**); the U10 respawn alternative stays the Director's (§6.1) |
| **EM-08** | Low | Act II §A6 Beat 6 table; `EAC-D9.01` | Option A: heat ~4 s, shape 2×3 s, quench, drive 3×4 s (about 25 s plus walking between hearth and frame). Option B: two cool phases of a ~40 s cycle (about 80 s). | The time-cost route costs about a minute more, so the Smithing hook adds little play choice at the act's emotional peak. Not a contradiction. | GD tuning, for example Option B takes three cycles. No content change. | **Open: Gameplay Designer** |
| **ES-11** | Low | Commons EBL `S01`, `S04` Option B, `S05`, `S06` | Night (`S01`) → morning (`S04` B) → night peak (`S05`) → "At the post at morning" (`S06`). | Up to four keep-watch hour jumps in a 25 to 35 minute quest; most of its length is waiting. | Delete the morning requirement from `S06`: the decision is made at the spur straight after `S05`, with Veska present. | **Resolved** (`cce3031`, Fixer 2; verified) |
| **ES-12** | Low (possible) | Commons ESR `S02_marks` matches 3 and 4 | Match 3 is "A carters' elder at the gate yard (`ESR-B2.03`)"; match 4 is "A Cinderweave glasswright **buying at the gate market** (`ESR-B2.04`)". `S02` needs six matches. | Both matches come from barks by NPCs with no stated placement or hours. If either is absent the step cannot complete. | State that both stand at the gate yard at every hour while `S02` is Active. | **Resolved** (`cce3031`, Fixer 2; both at the gate yard every hour while `S02` is Active; verified) |

### Pacing verdict

Judged from the authored steps only. Feel, length and difficulty need a build.

**Mostly meaningful RuneScape-style play, not a string of scripted interactions, provided heat is built as authored.** The heat system is taught in EH-M1, used again as plates and a ring clock in EH-M4, and brought back at full scale in EH-M6. Each milestone has one real skill hook with an honest time-cost route, and fights end by reading the place: cocks, a valve, braziers, collars. About half the side slate uses real verbs: EOP (a miniboss built on reading wallows and capping them), EOM (sabotage reading, then the kiln and its elite), ECN (trail, pits, slag cache), EFS (strike rhythm set by the tells), EWQ (a full fletching loop ending at the range), ESK (the ring-twice craft rule), EAD (search, fight, containment, escort) and EST (four-part containment).

The risk is technical. Heat (TD-01) is the gameplay. If it slips while the other fallbacks are taken (keep-watch channels, sequence-end flags, NPCs placed at stops, per-flight climb interactions), the region collapses toward scripted interactions.

**Weakest spots:**
1. **EH-M2:** about 5% combat. Class chores, a mitts errand, carrying a lens to Selice and an inspect-heavy annex: a fetch-and-read chain before the Tavi set piece.
2. **EH-M5 `S01` to `S03`:** inspect windows, a script, a slip, intercepts, a crawl and two document reads before the only fight. Long reading with little agency; as flag channels (TD-08, TD-09) the rehearsals become stand-and-wait.
3. **EH-M6 `S07` to `S08` after the boss:** dawn keep watch, thaw lines, the warming-house scene, the board, plates, the attendance roll, a choice, a reading scene and a letter, all scripted in sequence; the boss retry walk (EM-07) adds to the drag.

Also weak: the EAC Smithing hook carries almost no time trade-off (EM-08); the side quests EGT (almost all dialogue, and colliding with the frost), ESR (seven inspect-and-match checks, then two waits) and EFC (gather, carry, sit and watch); and the many keep-watch hour jumps (EBL, ESR). Keep watch is the time-cost alternative in about 16 of the 20 side quests, and is the main thing flattening their pacing.

---

## 4. C. Technical dependencies requiring Sol

Status against current source: **Demonstrated**, **Partly**, **Not demonstrated**. Current Unity facts used (`UNITY/README.md`): click-to-move on a host NavMesh; a flat navigation scene with no multi-level or off-mesh traversal; mobile enemy pursuit, NPC lifecycle and escort, walk-away resume prompts and co-op behaviour are remaining work; "Enemy bodies are anchored"; death restores at a recovery point and keeps progress and items; "World position … not persisted", reload at the road head. Code evidence (`CODE/Systems/Gameplay/`):

- `HazardDefinition { id, target, once; all, none; windup, damage; radius, pushDistance }`. `Hazards()` adds the `once` flag when the hazard fires and never re-arms it.
- `EnemyDefinition` has `target, range, leash, boundaryTarget/Radius` and no movement field.
- `presentationEvents` validate only `kind == "waterRise"`.
- `RespawnRegion { target, x, z, radius, all, none }` exists.
- `StageDefinition` and `ActionDefinition` support `any` and `anyCount`; `QuestDefinition` availability is `all` only.
- A hazard hit sets `draft.channel = -1`.

### 4.1 Heat system

| ID | Sev. | Location | Evidence | Status and problem | Fallback / bounded fix | Status (2026-11-15) |
|---|---|---|---|---|---|---|
| **TD-01** | **High** | Integration EI-HT-02/03/05 ("= LM (hazard volume)", "= LM (telegraphed environmental damage)"), EK-1, EK-3, EK-4; Integration R-9, R-11 "Standard"; Enemies; Zones §6 | Hazards are once-only, target-bound telegraphs (above). No periodic area damage, no safe niche volume, no zone state, no repeating vent, plate or ring-sector cycle. Predicates read heat state: EAC `S03` "both heat rooms Working"; EGA `S02` to `S03` stage and relief gates. | **Not demonstrated.** The core of the region (heat on nearly every required route, vents, plates, ring sectors, Vent Lines) is filed as an existing standard capability. Build order §7.1 step 2 assumes it exists. | Re-label these rows "ext LM (new: re-arm)". Minimum for Sol: (a) zone state as quest-local flags, with pins as flag set and clear; (b) one extension to the existing hazard so it re-arms on a cooldown, which gives cyclic vents, plates, sectors and periodic heat ticks; niche safety by placing niches outside the radii. Predicates then read flags. Sol owns the form. | **Partly resolved:** rows relabelled "ext LM (new: re-arm)" as a new requirement (`cce3031`). The repeating heat hazard, zone state and their runtime form stay **Open: Sol**; not designed here |
| TD-02 | Low | EI-CA-03, EQ-08, EK-10 | `draft.channel = -1` on hazard damage | **Confirmed.** Heat ticks would cancel channels. | The standard fallback (pads in or touching niche volumes) works under TD-01 if pads stay outside every hazard radius. Keep the request to Sol as is. See also EM-15. | **Open: Sol** (request kept as is) |
| ES-06 | Low | Per-player presentation hour (Act I conventions); step pins in EBL `S01` (night), ETB `S07` (morning), ESR `S04` (dusk), EST `S01`/`S03` (dusk), EOP `S04` (dusk); Integration EI-HT-02 | Each step "pins" an hour, and there is one hour per player. | Nothing says which pin wins when two Active quests pin different hours (e.g. EBL `S01` and ETB `S07` both Active). | For Sol (EI-HT-02): an hour pin applies only to keep watch inside that quest's step volume; elsewhere keep watch advances normally. Same shape as the ES-01 rule. | **Resolved** (`cce3031`, Fixer 2; hour pin applies only inside the quest's step volume; built on TD-08) |

### 4.2 Multi-level navigation

| ID | Sev. | Location | Evidence | Status and problem | Fallback / bounded fix | Status (2026-11-15) |
|---|---|---|---|---|---|---|
| TD-03 | Medium | Zones §5A (13 required rows); EI-AG-02 "= ext MR MI-AG-02" | README: the flat navigation scene "has no multi-level or off-mesh traversal". Several fallbacks offer "a zone transition into a flat interior" (ML-01b, ML-14, ML-15, ML-26, ML-09 alt.). | **Not demonstrated.** Scene and zone transitions are not demonstrated either: the build is one scene with connected hub paths. | Prefer the slope or flattened variant on every required row (ML-01a, ML-03, ML-07, ML-11, ML-14 bore, ML-15 ramp, ML-16, ML-20, ML-24, ML-26 sloped passage, ML-32). These need only NavMesh slopes, which exist. Build once with Mire MI-AG-02. | **Partly resolved:** slope or flattened fallback recommended in Zones §5A (`cce3031`); the multi-level form stays **Open: Sol** |
| TD-04 | Medium | Zones ML-09; Integration EQ-10, EDI-4; EI-ES-03 | The fallback "uses only the placement-to-a-named-anchor that respawn already needs … adds no runtime need". Code has `RespawnRegion` placement on death only. | **Partly.** An interaction that places the player at an anchor is a new, small action effect. Thennek and Asera on the ladders need EI-ES-03's fade fallback. | Ask Sol for one generic "place at anchor" action effect (reusing host-validated respawn placement), or EDI-4's ramp. Correct "adds no runtime need" to "one small action effect". | **Partly resolved:** "adds no runtime need" corrected (`cce3031`); the "place at anchor" effect stays **Open: Sol** (EDI-4 ramp: Director) |
| ES-05 | Medium | Commons EBL `S04_stay` (both options); Zones §5A ML-21 | Option A: "**fit** it at the headstock from the post's ladder". Option B: "fit the stay he brings (the same 2-segment fit)". ML-21 covers only the grate-hatch ladder. | A required ladder climb on both paths, with no ML row and no fallback. | Add an ML row. Fallback: an interaction-driven climb to a named anchor (ML-09 pattern), or the fit as a standing interaction at the post's foot. | **Resolved** (`cce3031`, Fixer 2; ML-37 with a standing-interaction fallback; verified) |

### 4.3 Escort, follow and NPC movement

| ID | Sev. | Location | Evidence | Status and problem | Fallback / bounded fix | Status (2026-11-15) |
|---|---|---|---|---|---|---|
| EM-03 | Medium | Integration EI-QS-06 fallback; Act II §A11 ("During `S07`, Thalan rejoins the player at the respawn point"); Zones ML-09 ("Thalan never climbs") | EI-QS-06 fallback: "the region's Cooling House for every step" (today's build has a single fixed recovery point). | Under that fallback, a death during the escort makes Thalan rejoin at Cinderwall, above the shaft he must never climb; the escort could not resume where the story needs it. Related: EM-02, TD-11. | Add one line to EI-QS-06 / EI-ES-01: under the fallback, Thalan waits at the last escort stop (the ring edge niche or the gallery), and escort-follow resumes when the player returns there. | **Resolved** (`cce3031`, Fixer 2; EI-ES-01 and EI-QS-06; verified) |
| EM-04 | Medium | Integration §2.10 EI-ES-01 to EI-ES-03; Zones §5A | The register lists only EAC `S07` (Thalan), EAD, ESH, the EGA crew, Thennek and Asera. It misses: Act I Beat 3, EEH `S03`: Tavi "escort-follow, short; she walks with the player and stops when they stop" (Act II calls it "the EH-M2 escort-follow"); ECW `S01`: Veska "stands in the next niche"; EGH `S02`/`S03`: Darven walks to G1 and on the drain route "goes first through the crawl … and waits at each niche"; EGH `S06`/`S07`: Yorven leads the player up the bypass (ML-07). | NPC lifecycle, escort and inspection walks are remaining work. These required beats have no stated fallback. Tavi's walk to the niche is a required containment part (`S03` completion). | Add these rows to EI-ES-01/02 with the existing fallbacks. Tavi: the "take her hand" interaction places her in the niche. The others: the NPC appears at each stop. Sol only. | **Resolved** (`cce3031`, Fixer 2; rows and fallbacks added to EI-ES-01/02; verified. The escort runtime is TD-06) |
| TD-06 | Low | EI-ES-01 (Thalan EAC `S07`, Myr EAD `S06`, Lenk ESH `S04`); EAD `S06_walk` "Escort arrives at H1 volume"; Act II §A11 "escort-follow resumes" | README: escort is remaining work; Lowmark's Tamsin escort is also pending (`LowmarkGameplay_Integration.md`). | **Not demonstrated.** A per-stop placement fallback exists, and flag-conditioned NPC representation is shown by Nan in the Flood Kitchen. | Merge with Mire MI-ES-01 and the Lowmark escort work. Write the fallback predicate as "player enters H1; Myr is placed there", and the same for Thalan at the shaft foot. | **Partly resolved:** fallback predicate written (`cce3031`); escort-follow runtime stays **Open: Sol** (with Lowmark and Mire) |
| TD-07 | Low | EI-ES-02, EI-PP-02 (tally-board crowd), Asera at dusk, crew in niches, Thennek at the shaft foot | README: "does not establish complete NPC lifecycle" | **Partly** (flag-conditioned representation only). | Place NPCs by step or flag only. Hour placement collapses into the keep-watch flag (TD-08). Merge with Lowmark and Mire. | **Partly resolved:** placement by step or flag recorded (`cce3031`); NPC lifecycle stays **Open: Sol** |

### 4.4 Mobile enemy pursuit

| ID | Sev. | Location | Evidence | Status and problem | Fallback / bounded fix | Status (2026-11-15) |
|---|---|---|---|---|---|---|
| TD-05 | Medium | Enemies §12 (Wraiths "path to the player"; warden-frame "follows a target onto the rim or the gallery", I-24; Old Plate "follows onto the rim"; "charges close any distance"); §6.2 Revenant "advances"; §15 "This file adds no new runtime need" | README: "mobile enemy pursuit/physical boar charge" are remaining work; "Enemy bodies are anchored". `EnemyDefinition` has no movement field. | **Not demonstrated.** The CDR-2 parity answers (the I-24 safe-spot fix, Old Plate's "never trivial") depend on pursuit, which is missing from R-1 to R-14. | Add an R-row "mobile pursuit = LM/MR (build once)". Fallback: anchored enemies whose range covers the arena with no rim spot outside it, and charges as re-arming line hazards from the anchor (TD-01). | **Partly resolved:** R-15 mobile pursuit added with an anchored fallback (`cce3031`); pursuit runtime stays **Open: Sol** |

### 4.5 Keep watch and the presentation hour

| ID | Sev. | Location | Evidence | Status and problem | Fallback / bounded fix | Status (2026-11-15) |
|---|---|---|---|---|---|---|
| TD-08 | Medium | EI-KW-01/02; predicates "Dusk reached" (EOP `S04`, EFD `S02`); dusk pins (ESS `S01`, `S05`; EAC `S02` Asera; ETB `S04`); EGA `S06` "dawn keep-watch"; EEH `S03` morning | README: choice props "do not claim a real day-cycle simulation"; Mire TD-09 | **Not demonstrated.** | Use the Integration fallback as the build form: keep watch is a timed channel that sets an hour flag, and predicates read the flag. Build once with Mire MI-KW-01. See also EM-11 (missing consumers), ES-01, ES-06. | **Open: Sol** (keep-watch build form; build once with Mire MI-KW-01) |

The frost hour (ES-01) and the frost variant (EI-WV-01, CO-08) ride on this capability.

### 4.6 Scripted sequences and presentation events

| ID | Sev. | Location | Evidence | Status and problem | Fallback / bounded fix | Status (2026-11-15) |
|---|---|---|---|---|---|---|
| TD-09 | Medium | EFD `S02` "vigil song end" (Wraiths re-form while it lasts); EOP `S04` "EOP.5 sequence end"; ESS `S01` "windows re-offer per run", `S05` `ess.breath_carried`; EGA `S07` `cinderwall.thaw_lines`; EAD `S05` "EAD.5"; ESK hammerfall; Integration §4.1 (15 events) | `presentationEvents` accept only `waterRise` | **Partly** (one generic timed event type). Six required predicates wait on a sequence ending. | Each sequence becomes a timed channel or dialogue node that sets the predicate's flag. The vigil's re-form window is a condition flag set at channel start and cleared at its end. Rehearsal window inspects stay available for the whole pinned step. Visuals are an upgrade. | **Open: Sol** (sequence ends as flags or channels) |

### 4.7 Carry-state

| ID | Sev. | Location | Evidence | Status and problem | Fallback / bounded fix | Status (2026-11-15) |
|---|---|---|---|---|---|---|
| TD-10 | Medium | Act I l.89 "a held prop and a quest-state flag"; §A11 "Carry-state bundle … persist" on death; Unburnt §0.6 "returned to their source if the player logs out"; several held at once (order copy + cut page; tags + order; plates 1→3); EI-CA-04 "EMS stone (blocks climb, agility and sprint)" | Lowmark carries are transient loads, need empty hands, are cleared on reload and are "collected again after death"; sprint is allowed "including while carrying" (README). | **Partly, with different meanings.** Documents and tokens kept across steps, deaths and logouts are not Lowmark carries. Implemented as carries they would be lost on reload, could not be stacked, and would need re-collect walks. The content-side contradiction is ES-03. | Split them: documents and tokens become possession flags (dialogue already gates on flags, EI-DG-02). Only physical loads (the EMS stone, ewer, pails, blankets, sack, sod, the ECC case) use the Lowmark carry with re-collect at the source. Drop the EMS "blocks sprint" clause to match the existing carry. | **Resolved** (`cce3031`, Fixers 1 and 2; documents and tokens are possession flags, only bulky loads use the Lowmark carry; verified in EI-CA-04) |

### 4.8 Other runtime needs

| ID | Sev. | Location | Evidence | Status and problem | Fallback / bounded fix | Status (2026-11-15) |
|---|---|---|---|---|---|---|
| TD-11 | Low | EI-QS-06 "Today's build restores at one fixed point"; EI-QS-07 logout restore by step | `RespawnRegion` with `all/none` flag conditions; README "World position … not persisted", reload at the road head | Respawn by step is **Partly** demonstrated, so the Integration text is out of date. Logout restore by position is **Not demonstrated**. The walk back from Cinderwall to U8 to U10 or the Warrens is long, because EI-QS-11 travel is only COULD (EM-07). | Update EI-QS-06 to cite respawn regions (this also eases EM-03). For logout, the resume-hook location needs load-time placement through the same respawn-region mechanism; otherwise accept a region-entry reload. | **Partly resolved:** EI-QS-06 cites respawn regions (`cce3031`); logout placement stays **Open: Sol** |
| TD-13 | Low | Integration items to drop or merge (CDR-4) | See fix column | Each adds scope with no gameplay gain. | **EI-QS-08, EI-FL-04, EQ-06:** gate the EGH offer action with `any`/`anyCount = 1` over the TF-M3 and MR-M2 completion flags, which `ActionDefinition` already supports; no derived flag or world rule (quest availability itself is `all` only). **EI-SG-01:** per-door inspect. **EI-HT-01:** the Zones §6.1 defaults. **EI-HT-08:** presentation only. **EI-CA-02:** a fixed-duration channel. **EI-DG-05:** a dialogue option. **EI-QS-11 and EI-QS-12:** cut (but see EM-07: keep EI-QS-11 for EGA `S06`). **EI-WV-01:** barks and props. **EI-HT-06:** three fixed-target hazards swapped by flag, merged into EI-HT-03 (every flaring NPC stands still). **EI-QS-03:** resume hooks as dialogue lines conditioned on quest stage, so no prompt system is needed. **EI-QS-04:** activation by flags through an entry action, the Lowmark pattern. | **Partly resolved:** simplified forms recorded in Integration (`cce3031`); adopting them stays **Open: Sol** (EI-QS-11 kept for EGA `S06`, EM-07) |

TD-12 (barricades by quest state are not demonstrated as movement blockers) is merged into CO-01 (section 5).

---

## 5. Co-op

### 5.0 CDR-6: co-op is optional assistance

Collin ruled CDR-6 on 2026-11-14 (`Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md`, §1 and §3.7). For Emberholt this audit reads as follows.

- **The solo walkthrough is the completion standard.** Every Emberholt quest, main and side, was walked logically solo (sections 1 to 3). No co-op or shared-state solution is a prerequisite for finishing alone.
- **Co-op is evaluated only as optional assistance.** Today's build is single-host and single-player ("Inactive players receive no gameplay execution"; co-op is remaining work), so every CO finding concerns a future co-op build. None affects solo completion. No new runtime requirement should be created only to support co-op mechanics (§3.7.6).
- **Credit and personal state.** A partner is credited only when their own active step consumes the work (EI-CO-01). Personal choices and flags are per player: the EAC approach and frame work (Act II §A11); `EH_SPEAKER` (§B11); `EFD_TELL` (EFD.10); `ESS_ELYNDRA_HEARD`, once per player and flavour only; EGA relief ("A partner's relief never moves another player's `EH_HEAT_MAIN`", Act III §11); the EOM vote, the EOP plate, the EAD book and ECC `EH_RIVERGLASS`. CO-04, CO-05 and CO-09 were the three places where the text contradicted this; all three are now Resolved, and since 2026-11-15 shared work done together credits every present partner on that step (CDR-6 §3.7 item 2a).
- **EI-CO-06 is a presentation fallback only** (the Mire MI-CO-06 pattern). One shared visual state may be shown; it never decides another player's walkable ground, hazard damage, interaction availability, step, credit or choice. The host's quest state is never authoritative over another player's progression.
- **Leaving never blocks** (EI-CO-05, Enemies §13, the §0 co-op bullet of each side file).
- **Bosses are solo-tuned** with group scaling only up from the solo baseline (EI-EN-08, Enemies C-10): the Draw Sentinel, the Hollow Revenant, Old Plate and the Captain.
- **No co-op-only content** (Enemies §15 "Avoided"; Work and Skills "second hand is always an NPC"), except CO-09.

### 5.1 Pairings walked

| # | Partner 1 (host) | Partner 2 | What the walk found |
|---|---|---|---|
| P1 | EAC Completed | EAC `S03` to `S07` in the Warrens | Post-quest barricade beyond the Warrens' mouth; Thalan already gone (CO-01, CO-07) |
| P2 | EGH `S06` to `S07` | EGH `S02` to `S05` | Mouth barricade closes P2's way in; shared pocket pulse (CO-01, CO-03) |
| P3 | EGA Completed | EGA `S03` to `S06` | Inert Sentinel prop, cut splices, locked relief wheels (CO-02) |
| P4 | EGA `S00` to `S06` (frost night, stage variants) | ECW `S01`/`S06`, or EWA, ESP, ESH in U2 to U5 | Conflicting heat pins, stages, hour and frost variant in the hub (CO-06, CO-08) |
| P5 | Same step | Same step | Collar credit (CO-04); shared-task help in Unburnt side quests (CO-05); re-form predicates (CO-03) |
| P6 | Host leaves mid-escort or mid-deep-main | Any | Logout rule holds; walk-back cost only (TD-11) |

### 5.2 Shared-state conflicts

**Solution families for Sol** (Mire Q-18, Integration EQ-12). **None is chosen here, and this audit proposes no networking architecture.**

- **F1. Per-player phased set piece.** Each player at a stateful step gets their own copy; partners share only when their states match.
- **F2. Per-viewer props and walkability.** Props, variants and walkable segments resolve from each viewer's own state, with per-player path checks on the host. The heaviest option.
- **F3. Shared presentation that never gates.** One shared visual state may show; walkability, hazard damage, interactions and credit use each player's own state.
- **F4. Compatibility gate on entry.** A stateful set piece can be entered together only at the same step and state; otherwise the further-ahead partner joins as a helper who makes no progress.
- **F5. Defer to solo.** The stateful step pauses in co-op and resumes alone or with a same-step partner.

| ID | Sev. | Location | Evidence | Conflict | Options for Sol (no architecture chosen) | Status (2026-11-15) |
|---|---|---|---|---|---|---|
| **CO-01** (merged with **TD-12**) | **High** (co-op only; solo unaffected) | Integration EI-PP-03; Act I §C11 l.1138 and l.1160; Act II l.285, l.404, l.443; Zones EP07 l.215, EP13 l.283 | "The mouth route back is closed for `S06`–`S07` (a Deepbrand barricade prop…)"; "past the mouth a new Deepbrand **barricade** (non-interactive prop) closes the Warrens"; EI-PP-03 is "= LM, MUST" and not marked presentation-only. EGH epilogue: "the gallery is walkable to the crew camp and the outer glass". TD-12: barricades are **not demonstrated** as movement blockers (the Mire audit grep found no NavMesh obstacles, links or area masks; Lowmark persistent props are visual). | Quest-state props that block movement. Under shared or host presentation: P2 at EGH `S02` to `S05` cannot enter by the mouth while the host is at `S06` to `S07`; P2 inside the Warrens at EAC `S03` to `S07` can be shut in when the host completes EAC. Possible: the EGH post-quest limit "walkable to … outer glass" may also close H3 to H4 to a partner at `S05` to `S06` (the text does not say what stops the player). EI-CO-06 forbids shared state from deciding walkable ground, yet these rows are the walkability. | Bounded content fix (simplifies, and removes a runtime need): delete the EGH `S06`–`S07` mouth barricade, since the bypass and the annex street door already serve `S07` (Zones ML-07) and no beat depends on it; make the post-EAC barricade a turn-back bark volume checked against each player's own EAC state. Otherwise F2, F4 or F5. | **Resolved** (`cce3031`, Fixers 1 and 2; EGH mouth barricade deleted; post-EAC barricade is a turn-back bark volume on each player's own EAC state; verified in Act I l.1138, Act II l.285 and l.443, EI-PP-03, Zones) |
| **CO-02** | **High** (co-op only) | Act III §E l.670 ("The **Sentinel** stands where it locked… inert prop; never re-forms"; splices "with their clamps cut off… stacked in the bleed house"); Act III §12 l.569 relief wheels ("turning one … locks the other two"); Enemies §6.1 co-op row | When the host has completed EGA, U9 and U10 show cut splices and an inert Sentinel. | A partner at their own `S04` has nothing to shut. At `S06` they need a live, targetable boss in the same spot. A partner at `S03` sees locked relief wheels and cannot choose. The Mire Night Count and crown class of conflict (Mire K-05, K-06). | F1 (a per-player deep-main instance for `S02` to `S06`), F4 or F5. Rule to state: EGA-E4 spawns from the partner's own `S06`, whatever the host's state. No content change proposed. | **Partly resolved:** rule stated, EGA-E4 spawns from each partner's own `S06` (`cce3031`); the deep-main family (F1, F4 or F5) stays **Open: Sol** |
| CO-06 | Medium | Integration EI-CO-03, EI-CO-06, EQ-12; Zones §0.1 per-player row, §7 item 4; Act II `S03_warrens` predicate "both heat rooms Working"; Act III §6.3 stages | EI-CO-06: shared presentation "never decides … hazard damage". U2 to U5 carries ECW `S01`/`S06` pins, EGA stage variants and EWA, EBL, ESP and ESH routes at once. | To honour EI-CO-06 the host must apply each player's own heat state for damage and for the "rooms Working" predicates, while the shared tell may show another player's state. That breaks the "readable system" for the partner and is a runtime need created only for co-op (§3.7.6). | F3 (damage and predicates from each player's own state, visuals shared) or F4/F5 for pinned heat steps. Record that under F3 a partner's tell may disagree with their own damage. | **Open: Sol** |
| CO-07 | Medium | Unburnt §0.6 ("own instance of every quest NPC scene (phased)"); Act II l.312 and §A11 ("Each partner sees their own Thalan"); Act I l.640 ("each partner's Tavi is their own"); l.1143 (Seredh); EAD.10 ("each player walks their own Myr home"); ESH.10 (Lenk); Integration EI-CO-04 | Per-player copies of single named NPCs (Thalan, Tavi, Seredh, Myr, Lenk, Asera, Serix) need NPC phasing. The build has no NPC lifecycle. | The Mire K-08 class. | F2 (per-player NPC instances), F4 (shared scene only at the same step) or F5. Solo unaffected. Keep the existing "a partner whose own step is not `S06` waits at the chamber door" wording as the F4 form. | **Open: Sol** |
| CO-08 | Medium | Integration EI-KW-02, EI-WV-01; Zones §7 items 2 and 3; Act III `S00_frost` | Per-player hour pins (EGA dusk, night, dawn and morning; ESS, EFD, EOP and ETB at dusk; ECN at night) and the EGA frost variant over the hub W1 to W4, where every partner passes. | Two players in one space need different hours and weather. Lighting is shared. | F3: each player's hour and frost drive only their own pins, gates and spawns; shared lighting and frost are presentation. Matches Mire K-02 and K-09. No content change. | **Open: Sol** |

CO-03 (B, High), CO-04, CO-05 and CO-09 (A) are text findings and sit in sections 2 and 3.

**Co-op verdict.** With partners at the same step, the packages are coherent once CO-04, CO-05 and CO-09 are corrected. With partners at different steps, CO-01, CO-02 and CO-03 can strand or stall a co-op session until Sol picks a family per set piece or the bounded text fixes are applied. EH-M4 (the Warrens) and EH-M6 (the deep main) are the hardest cases. Under CDR-6 these are co-op presentation and pacing questions only: none prevents either player from finishing alone from their own step.

---

## 6. D. Director-level decisions

Nothing in this section is decided by this audit.

### 6.1 Findings from this audit

| ID | Sev. | Decision | Location and evidence | What the audit found | Options preserved | Status (2026-11-15) |
|---|---|---|---|---|---|---|
| EM-13 (ED-7) | Medium | **EH-M3 gate** | Bible ED-7; Act I §C4, §C11. EH-M3 needs EH-M2 and (TF-M3 or MR-M2). | A solo player who enters Emberholt first stops after EH-M2 at a visible locked entry. The gate is honest and visible but blocks the main line on another region. Implementation note: TD-13 shows the "either region" gate needs no derived flag. | No change proposed. ED-7 stays open. | **Open: Director** (ED-7; not approved, options kept) |
| EM-14 | Low | **R09 inference** | Act I §C14.5. R09's "an initiate became the Fire Titan" is reached by inference after the second-sheet cut. | Already recorded for the Director. Listed so the main-line R09 path is not read as complete without that ruling. | As recorded in Act I §C14.5. | **Open: Director** |
| ES-10 | Low | **ESK hook direction** | Work ESK.13 item 1 vs bible §7.1 ESK row. Bible: "Durnan has heard of a forge that refuses salvage." Package: "a deliberate deviation … a **player** line answered by Durnan". | The package deliberately departs from the bible row, and the bible was not updated. | Director confirms; then edit the bible row (text only). | **Open: Director** |
| EM-07 (part) | — | **Draw Sentinel respawn point** | Act III §7; bible §10.1 | A U10 door-niche respawn would cut the retry walk but conflicts with bible §10.1. | Primary fix is Sol's EI-QS-11 (section 3); the respawn alternative is the Director's. | **Open: Director** (the respawn alternative; counted under EM-07, section 3) |

### 6.2 Open Director items carried (not changed by this audit)

| Item | Subject | Status and what the audit found |
|---|---|---|
| **ED-7** ● | EH-M3 gate on TF-M3 or MR-M2 | **Open: Director** (not approved; alternatives kept). Open (EM-13). |
| **ED-15** ● | Fog and Riverglass act (ECC) | **Open: Director** (not approved; alternatives kept). Held in review. ECC is playable as authored; the alternative (cut ECC and leave the series to CV-M2) is preserved in the bible. No playability finding depends on the choice. |
| **ED-20** ● | EH-M2 prerequisite (Arcs §3.3 prose vs §6 graph) | **Open: Director** (not approved; alternatives kept). Open. The main line follows the graph (EH-M2 requires EH-M1). If the prose wins, EH-M2's offer must not use "warden's hand" (bible ED-20). |
| **EDI-1** | Heat-zone defaults (Zones §6.1, ZQ-2) | **Open: Director** (not approved; alternatives kept). Open. Bears on TD-01 and EM-01: the defaults are what heat falls back to after every pin releases. |
| **EDI-2** | Red-Lit annex placement `[C14.2]` (Zones ZQ-1) | **Open: Director** (not approved; alternatives kept). Open. ML-07 and the CO-01 fix depend on the annex having a lower stacks door the bypass can reach and a street door. MAP VERIFICATION REQUIRED kept. |
| **EDI-3** | EH-M6 auto-activation (EQ-04) | **Open: Director** (not approved; alternatives kept). Open. ES-01's fix works under either auto-start or offer. |
| **EDI-4** | The EH-M4 shaft (EQ-10, Zones ZQ-5) | **Open: Director** (not approved; alternatives kept). Open. Relevant to TD-04: steep spiral ramp, or hold EH-M4, only if no ladder form is possible. |
| **Geographic placement** | Relative route order and every MAP VERIFICATION REQUIRED item | **Open: map owner.** Open for the map owner. No finding was solved by moving anything. |

### 6.3 Follow-ups from the 2026-11-15 character rulings

| Item | Evidence | Question for the Director | Status (2026-11-15) |
|---|---|---|---|
| **Elyndra's shrine: "abandoned" vs a kept shrine** | Canon character file `LORE/Characters/Caelmor_Characters_Region4_Emberholt.txt` l.1183: "Lives in near-isolation at an abandoned vent shrine"; Part 4 continuity ledger l.40: "An abandoned vent shrine on the Ridge" with D-EL "canon background, manner and shrine unchanged". The package has a keeper and pilgrims there: EFD (Combat l.416, l.429) "**Ivett Quarle** has kept it for most of her life", Zones l.356 "Ivett Quarle (keeper); pilgrims", bible EP20 and EDS05. | Is the shrine abandoned (Ivett and the pilgrims then contradict canon), or is "abandoned" read as "abandoned by the city, kept by one keeper" (a ledger and character-file note only)? No content change proposed until ruled. | **Resolved** (Director, 2026-11-15; applied in `b45b809`): the shrine is officially abandoned and the city does not maintain it; Ivett Quarle tends it independently; pilgrims visit occasionally; Elyndra lives there in relative isolation. EFD, bible EP20/ED-21/EDS05, Zones EP20 and LORE §37 aligned; verified in Combat EFD and Zones EP20. |
| **Given name "Iven" used twice** | ED-3 names the precursor initiate **Iven Calder** (Review §5.0; ledger l.41: "no relation to any other character sharing the given name"). Thornfell has **Iven Ridgeborne**, a canon-anchor high-path scout with dialogue in Acts II and III (Thornfell bible l.91, l.212; TF-M4 offer). | The ledger already states no relation. Confirm the overlap is acceptable, given that R19 at CV-M4 will put Iven Calder's name in front of players who know Iven Ridgeborne, or rule otherwise. No rename proposed here. | **Resolved** (Director, 2026-11-15; `b45b809`): Iven Ridgeborne keeps his name and is unrelated to Iven Calder; note added to the Part 4 ledger Iven Calder row. |
| **ESR elder renamed Hallam Drost** | Commons review pass 2026-11-15: Hallam Calder renamed so no Emberholt NPC shares a surname with Iven Calder (ED-3). | Accept the rename? | **Resolved** (Director, 2026-11-15: accepted; recorded in the Commons review log, `b45b809`). |

### Gameplay Designer items (primary entries above)

- **C-1 (1.5 s) and C-2 (25%):** authored tuning requirements pending GD review wherever they appear. Every main-line displacement meets the 1.5 s figure (pending GD); plates count as a standing tell (EK-4).
- **EM-08:** EAC Option B length against Option A.
- **EM-06:** the `[GD]` Smithing levels behind the dialogue-chosen skill routes.
- **ES-04:** the EOP Hunting accept level `[GD: low–mid]`, reachable without EWQ.
- **EM-16:** verify the P2 Seal crossing and the 6 s rehearsal windows against C-1 and C-2 once a build exists.

### Carried over from Lowmark and Thornfell

The open Lowmark and Thornfell questions recorded in the Mire audit (Maelin's knowledge; the river hands / Lock men; the knot-per-bearer custom) remain open and were not touched by this audit.

---

## 7. E. Areas that cannot be assessed until a playable Unity build exists

None of the following can be judged from text.

| ID | Sev. | Area | Location | Note | Status (2026-11-15) |
|---|---|---|---|---|---|
| EM-15 | Medium | Whether patrol tells stay readable through the Echo overlay (~8 s every ~25 s), and whether heat ticks cancel channel segments in the valve-under-pressure set pieces. | EGH `S05`; ECW `S06` and EGA `S06` channels in heat (EI-CA-03); EEH `S03` breath channel synced to an NPC count | Today's build interrupts timed work on a hit (TD-02). Keep the EI-CA-03 niche-pad fallback as the default. | **Open: playable build** |
| EM-16 | Medium | Whether a solo click-to-move player can make the P2 Seal crossing (~20 m in ~4 s at a run, through Surging heat, on a ~20 s cycle), hit the ESS `S01` 6 s rehearsal inspect windows, and bait the EAC-E3 warden-frame. | Act III §7.1.3; Act II ESS `S01`; EAC-E3 | Depends on click-to-move, Shift sprint and inspect latency at the 10 Hz tick. GD to verify against C-1/C-2 (pending GD). | **Open: playable build** (then GD against C-1/C-2) |
| ES-14 | — | Whether ETB `S07`'s 60 read-and-sound prompts ("Twenty children … each needs three chimes … No timer") drag or feel trivial. | Unburnt ETB `S07_lesson` | | **Open: playable build** |
| ES-15 | — | Whether Old Plate's wallow-seeking AI, ~25 s bead cycle, ~45 s caps and 3 to 4 minute solo target read and pace well with click-to-move. | Combat EOP-E3 (Enemies §6.3) | Depends on TD-05. | **Open: playable build** |
| ES-16 | — | Whether the ~3 minute EFD vigil song is dead time for a player who skips the optional Wraiths. | Combat EFD `S02_vigil` | | **Open: playable build** |
| ES-17 | — | Whether bubble correction "on the crew's call", crossbow marks and walking the stair with students work as interactions on click-to-move. | ESR `S03` Option B; EWQ `S05`; EME04 | | **Open: playable build** |
| TD-14 | Low | Whether the fallbacks (heat readability, flattened vertical spaces, anchored enemies) still read and play well. | Sections 4.1 to 4.4 | | **Open: playable build** |

Also untestable: every co-op behaviour (credit, reconnection, host departure, partner persistence, per-viewer presentation), and whether C-1 (1.5 s) and C-2 (25%) are the right values at all; they remain authored tuning requirements pending GD.

---

## 8. Preserved constraints

- **Map verification.** Every MAP VERIFICATION REQUIRED flag in the Emberholt package is kept. Count at `fb83110`: bible 8, Act I 12, Act II 11, Act III 7, Act III dialogue 2, Unburnt 8, Commons 7, Work 7, Combat 8, Zones 32, Enemies 3 (105 in total). This audit changed no file, so the count is unchanged. Map-dependent points (EDI-2 annex placement for ML-07 and CO-01, Elyndra's sleeping place at EP20, relative route order) are recorded as questions, not solved by moving anything.
- **Lowmark terrain conflicts.** TC-01 to TC-19 in `Zones/Caelmor_Lowmark_Terrain_Narrative_Conflict_Register.md` remain recorded and unsolved. This audit did not touch that register.
- **Geography.** No route, POI or connection was changed or proposed. Every fix above is a step number, a rule, a flag row, a deleted sentence or a fallback.
- **Art.** No material, texture, shader, palette, colour or finish was modified or prescribed. Heat states (Cool, Working, Surging) and tell states are gameplay states, not art direction.
- **Tuning.** C-1 (1.5 s) and C-2 (25%) are authored tuning requirements pending Gameplay Designer review. No value was changed.
- **Director rulings.** CDR-1 to CDR-6 and the 2026-11-15 character rulings (D-E2, D-S1, D-EL, ED-3) were read as binding. The EAC single outcome, ESS-D12's non-gating consult, R09 to R12 ownership by Emberholt and R19 owned by CV-M4 (seeded only; Iven Calder spoken nowhere in Emberholt) were checked and hold.

---

## 9. Fix log

Bounded fixes applied 2026-11-15 in two passes split by file ownership (Fixer 1: Acts I–III, their dialogue and the bible; Fixer 2: the four side-quest files, Enemies, Zones and Integration). A finding split across both owners appears in both tables. D and E items, and C items needing an architecture choice by Sol, were not applied and stay open. Each changed file carries a review-log row "Playability audit fixes, 2026-11-15".

**Fixer 1 (main acts, dialogue, bible)**

| ID | Status | Files | What changed or why skipped |
|---|---|---|---|
| EM-02 | applied | Act II | §A7 Death and §A11 Death/Logout: after `EAC-D9.42` respawn/logout at the shaft-foot niche (K2) with no Thalan; Thalan rejoins only before `.42`. |
| EM-05 | partly | Act I | §A9.2 `ECW_SOB_HEARD` "None (deliberately)" corrected to EH-M5 `ESS-D5`. Integration §3.2 rows are Fixer 2's. |
| EM-09 | applied | Act II Dialogue | `ESS-D12.01` gains `[ESS-D12.10 or ESS-D12.20 heard] "(Leave her to the vent.)" → ESS-D12.40`. |
| ES-08 | applied | Bible | §8.1 R09/R12 seed cells drop *The Half-Name Wall* / *Glassmoth's Tonic*; "Deepens after payoff" note added under the table. |
| ES-09 | applied | Bible | §6 Skill hooks and ED-11: "two side quests" -> "several side quests (ESK, EOM, ESR, ETB, ENW, ECC)". |
| CO-04 | partly | Act III | §7.1.4 co-op row: "recorded as kept for each partner" sentence replaced; collar counts only for the shutter, `EGA_COLLARS` persists own shuts only. Enemies §6.1 is Fixer 2's. |
| CO-09 | applied | Act I | §A11 co-op row: "warden's hand ... end table" sentence deleted. |
| ES-01 | partly | Act III | §9.3: hour-pin scope rule added (EGA pin governs only EGA steps and frost-variant areas; side steps there held until `EGA_THAW_SEEN`; keep watch elsewhere advances; EDI-3 open). Side files §0.5 and Zones §7 are Fixer 2's. |
| CO-03 | partly | Act I, Act II | `S06_surge`, `S06_circle`, `S04_sleep_rooms` "all defeated" made per player (own condition ended, no form engaged). Enemies I-20 note is Fixer 2's. |
| CO-01 | partly | Act I, Act II | Act I: EGH `S06`-`S07` mouth barricade prop deleted (and its §C runtime row); Yorven bark kept as a bark volume on the player's own step. Act II: post-EAC barricade is a turn-back volume (`EAC-B9.5`) on each player's own EAC state, never a blocker for a partner; prop presentation only. Zones EP07/EP13 and Integration EI-PP-03 are Fixer 2's. |
| TD-10 | partly | Act I | Conventions "Carry-state objects": documents and tokens are possession flags (kept across death/logout, no movement or attack limit; EI-CA-04 small class). Integration EI-CA-04 is Fixer 2's. |
| ES-03 | skipped | — | Checked my files: Act III blankets and Act II ewer are bulky "walk, cannot attack", consistent with the proposed classes; the fix lives in EI-CA-04 (Fixer 2). |
| ES-13 | skipped | — | Fix is in Unburnt (drop citation); adding the line to Bible §8.2 is the Director's option. |
| EM-07 | skipped | — | Sol (EI-QS-11) / Director (respawn alternative). |
| EM-08 | skipped | — | GD tuning; audit proposes no content change. |

**Fixer 2 (side quests, Enemies, Zones, Integration)**

| ID | Status | Files | What changed or why skipped |
|---|---|---|---|
| EM-01 | applied | Zones, Integration | HZ-09/EI-HT-07 -> S02 (G4 pin); HZ-10/ML-05b -> S03 (drain); verified against Act I S02_mouth/S03_fall table. |
| EM-02 | applied (my part) | Zones | §6.6 EH-M4 row: after EAC-D9.42 respawn/logout at shaft-foot niche, no Thalan. Act II part is Fixer 1. |
| EM-03 | applied | Integration | EI-ES-01 + EI-QS-06: under fixed-point fallback Thalan waits at last escort stop; no rejoin after D9.42. |
| EM-04 | applied | Integration | Tavi (EEH S03) added to EI-ES-01 with take-hand fallback; Veska ECW S01, Darven EGH S02-S03, Yorven EGH S06-S07 added to EI-ES-02. |
| EM-05 | applied (my part) | Integration | §3.2 rows added (ECW_RAT_SEEN, ECW_SOB_HEARD, EGH_WORK_ORDER/ORDER_SHOWN/KEEP_SEEN/INITIATE_JOURNAL, EAC_SLATE_READ, ESS_LETTER_READ, EEH_TAVI_STRUCK; EAC readers on SHEET/STONE); ECW_SOB_HEARD removed from "read by none". Act I §A9.2 note is Fixer 1. |
| EM-06 | applied | Integration | New EI-SK-05 below-level rule (option shown only at level; decline line; time-cost stays). |
| EM-07 | partly | Integration | EI-QS-11 scope note: keep for EGA S06 only, proposed MUST for Sol to confirm; priority not changed (Sol); respawn alternative is Director. |
| EM-08 | skipped | - | GD tuning, no content change proposed. |
| EM-09 | skipped | - | Act II dialogue, Fixer 1's file. |
| EM-10 | applied | Integration | EI-IT-01 note: world prop in EH-M6 (inspect only), never re-granted. |
| EM-11 | applied | Integration | EI-KW-01 consumers added. |
| EM-12 | applied | Zones | §6.6 EH-M2 aligned to Act I §B7. |
| ES-01 | applied (my part) | 4 side files, Zones §7, Integration EI-KW-02 | Shared frost rule: EGA pin scoped to EGA steps/frost areas; side steps there held to EGA_THAW_SEEN; EDI-3 open. Act III §9.3 is Fixer 1. |
| ES-02 | applied | Unburnt | EGT held under frost rule (opens at EGA_THAW_SEEN; unlock predicate unchanged to match Act II); "before dusk" deleted from S01 (2 places). |
| ES-03 | applied (my part) | Integration, 4 side files, Zones | EI-CA-04 bulky/small classes + lent tool; EWQ crossbow = lent tool; EMS stub = EMS_RECEIPT flag only; class note in each side file's rules. |
| ES-04 | applied | Enemies | EW-03 Ash Roads pocket opens after EH-M1. |
| ES-05 | applied | Zones, Integration | New ML-37 (EBL S04 post ladder) with standing-interaction fallback; §5A and EI-AG-02 counts updated (38 rows, 14 required). |
| ES-06 | applied | Integration EI-KW-02, Zones §7, side-file rule | Hour pin applies only inside the quest's step volume. |
| ES-07 | applied | Zones | §7 ECN N8 -> dusk. |
| ES-10 | skipped | - | D. |
| ES-11 | applied | Commons | EBL S06 no longer waits for morning (beat text + EBL-D5.01 stage note). |
| ES-12 | applied | Commons | ESR S02: elder and glasswright at gate yard every hour while S02 Active. |
| ES-13 | applied | Unburnt | EST.3 "(bible §8.2)" citation dropped. |
| CO-01 | applied (my part) | Integration EI-PP-03, Zones EP07/EP13/§6.5, Enemies l.536 | EGH mouth barricade deleted; post-EAC barricade -> per-player turn-back bark volume. Act I/II parts Fixer 1. |
| CO-02 | applied (rule only) | Enemies §6.1 | EGA-E4 spawns from each partner's own S06; family choice left to Sol. |
| CO-03 | applied (my part) | Enemies §13, I-20 | Per-player "all defeated" reading noted as predicate question. Act I/II predicates Fixer 1. |
| CO-04 | applied (my part) | Enemies §6.1 | "recorded as kept for each partner" sentence replaced; EGA_COLLARS acting player only. Act III part Fixer 1. |
| CO-05 | applied | Unburnt | §0.6 shared-task credit sentence and EST/ETB/ENW/EGT credit sentences deleted. |
| CO-09 | skipped | - | Act I, Fixer 1's file. |
| TD-01 | applied | Integration, Enemies | EI-HT-03/05, R-9, R-11 relabelled "ext LM (new: re-arm)" as NEW requirement; header and build order step 2 note; form left to Sol. |
| TD-02 | skipped | - | No change proposed (keep request as is). |
| TD-03 | applied | Zones §5A | Recommended slope/flattened fallback note; Sol's choice stands. |
| TD-04 | applied (text) | Zones ML-09/ML-17, Integration EI-AG-02 | "adds no runtime need" -> one small "place at anchor" action effect. Sol ask itself not decided. |
| TD-05 | applied | Enemies §15, Integration crosswalk | New R-15 mobile pursuit, not demonstrated, with anchored fallback. |
| TD-06 | applied | Integration EI-ES-01, Combat EAD S06 | Escort fallback predicate "player enters H1; Myr placed". |
| TD-07 | applied | Integration EI-ES-02 | Placement by step or flag only. |
| TD-10 | applied | Integration EI-CA-04, Unburnt, Zones | Documents/tokens as possession flags; EMS "blocks sprint" dropped. |
| TD-11 | applied (respawn part) | Integration EI-QS-06 | Cites RespawnRegion; logout placement left to Sol. |
| TD-13 | applied | Integration | Recommended simplified forms added to EI-QS-03/04/08/11/12, EI-FL-04, EI-DG-05, EI-HT-01/06/08, EI-CA-02, EI-WV-01, EI-SG-01, EQ-06; no priority labels changed; ED-7 stays open. |
| TD-14 | skipped | - | E. |

**CDR-6 shared-credit revision (2026-11-15, `b45b809`).** The Director clarified CDR-6 as §3.7 item 2a: shared work done together credits every present partner whose own active step consumes it, and nobody repeats an identical kill, repair or task. The per-player wording the fix passes had added for CO-03, CO-04 and CO-05 (and the matching EI-CO-01 and Enemies §13 rows) was replaced: the "all defeated" encounters clear for every present partner on that step; a collar shut in the shared fight persists in each present partner's `EGA_COLLARS`; Unburnt §0.6 credits shared tasks done together; cocks, valves, braziers, dampers, splices, caps, the EWA diverter and the EBL notch follow the same rule. Personal choices, flags, readings and rewards stay per player; solo completion and the leaving rule are unchanged. CO-01 (the per-player turn-back volume) and CO-09 were not affected. An independent review the same day added the EGA `S01` blanket carries and hood damper (Act III). Record: `Caelmor_Director_Rulings_Combat_Ranged_Release.md` §7.

**Director decisions (2026-11-15, `b45b809`).** Elyndra's shrine: officially abandoned, independently tended by Ivett Quarle, the city does not maintain it (§6.3, Resolved). Iven Ridgeborne keeps his name, unrelated to Iven Calder (§6.3, Resolved). Hallam Drost rename accepted (§6.3, Resolved).

**Status reconciliation (2026-11-15).** Every finding in sections 2 to 7 now has a status column (section 1, "Status at 2026-11-15"; counts in section 10). Each Resolved High and Medium finding was re-checked against the file text. ED-7, ED-15, ED-20 and EDI-1 to EDI-4 are not approved and stay Open: Director with their alternatives. TD-01 and the related runtime questions stay with Sol.

---

## 10. Counts

Source findings: 56 ids across four passes (EM 16, ES 17, CO 9, TD 14). One exact duplicate was merged (TD-12 into CO-01), leaving 55 findings. At first issue all were Open; status at 2026-11-15 is in the second table.

| Category | High | Medium | Low | Unrated | Total | IDs |
|---|---|---|---|---|---|---|
| A. Definite authored-content contradictions | 0 | 8 | 9 | — | 17 | EM-01, 02, 05, 09, 10, 11, 12; ES-02, 03, 04, 07, 08, 09, 13; CO-04, 05, 09 |
| B. Likely gameplay or pacing problems | 2 | 2 | 3 | — | 7 | ES-01, CO-03 (High); EM-06, 07; EM-08, ES-11, 12 |
| C. Technical dependencies for Sol (section 4) | 1 | 9 | 6 | — | 16 | TD-01 (High); EM-03, 04, ES-05, TD-03, 04, 05, 08, 09, 10; ES-06, TD-02, 06, 07, 11, 13 |
| C. Co-op shared-state conflicts for Sol (section 5) | 2 | 3 | 0 | — | 5 | CO-01 (+TD-12), CO-02 (High); CO-06, 07, 08 |
| D. Director-level decisions | 0 | 1 | 2 | — | 3 | EM-13, EM-14, ES-10; plus 8 carried open items (ED-7, ED-15, ED-20, EDI-1 to EDI-4, geographic placement) and 2 rulings follow-ups |
| E. Untestable until a playable build | 0 | 2 | 1 | 4 | 7 | EM-15, EM-16, TD-14; ES-14 to ES-17 |
| **Total** | **5** | **25** | **21** | **4** | **55** | |

All five High findings were verified against the repository files and stand. One is a solo problem in the authored content (ES-01, the frost hour stall), one is the core technical dependency (TD-01, heat), and three affect co-op only (CO-01, CO-02, CO-03), which under CDR-6 never block solo completion. No High authored-content contradiction (category A) was found.

**Status at 2026-11-15** (after `cce3031`, `b45b809` and the Director decisions of 2026-11-15)

| Category | Resolved | Partly resolved | Open | Open owner |
|---|---|---|---|---|
| A. Definite authored-content contradictions | 17 | 0 | 0 | — |
| B. Likely gameplay or pacing problems | 5 | 1 (EM-07, Sol) | 1 (EM-08) | Gameplay Designer |
| C. Technical dependencies for Sol (section 4) | 5 | 8 (TD-01, 03, 04, 05, 06, 07, 11, 13) | 3 (TD-02, 08, 09) | Sol |
| C. Co-op shared-state conflicts for Sol (section 5) | 1 | 1 (CO-02) | 3 (CO-06, 07, 08) | Sol |
| D. Director-level decisions | 0 | 0 | 3 (EM-13, EM-14, ES-10) | Director |
| E. Untestable until a playable build | 0 | 0 | 7 | Playable build |
| **Total** | **28** | **10** | **17** | |

By owner of what remains: Sol 16 (10 partly resolved, 6 open), Director 3, Gameplay Designer 1, playable build 7. Of the five High findings, ES-01, CO-01 and CO-03 are Resolved; TD-01 and CO-02 are Partly resolved with Sol. Outside the 55: ED-7, ED-15, ED-20 and EDI-1 to EDI-4 stay Open: Director (not approved; alternatives kept); geographic placement stays with the map owner; the two rulings follow-ups and the Hallam Drost rename are Resolved.
