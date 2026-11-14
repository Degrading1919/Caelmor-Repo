# Caelmor: Mire Playability Audit

**Date:** 2026-11-13 (updated 2026-11-14 for CDR-6, solo completion; section 5.0 and the fix log)
**Audience:** Collin (Creative Director), Sol (systems and Unity), Gameplay Designer (GD)
**Package audited:** the Mire quest package at checkpoint `98f24f3`, read on `main` at `eb38636`. No file under `04_CONTENT_PRODUCTION/` changed between those two commits; the commits in between are texture-painting and material-atlas work under `MEDIA/Materials/`.

## 0. What this document is

**This is an authored-content and systems-contract walkthrough. Nothing in it was played or tested.** The Mire is not implemented in Unity. Every statement about "playable" below means "logically playable on paper": the step predicates, flags, items, routes, death and logout rules and co-op rules can be followed from start to finish without contradiction, and the runtime capabilities they assume are named. Whether any of it plays well can only be learned from a build (section 7).

### Scope

All Mire content files under `04_CONTENT_PRODUCTION/`:

| Short name | File |
|---|---|
| Bible | `Quests/Caelmor_Mire_Narrative_Production_Bible.md` |
| Act I, Act II, Act III | `Quests/Caelmor_Mire_Main_Act_I.md`, `_Act_II.md`, `_Act_III.md` |
| Act I/II/III dialogue | `Dialogue & Narrative/Caelmor_Mire_Main_Act_I_Dialogue.md` (and II, III) |
| Names, Cloth, Work, Sett | `Quests/Caelmor_Mire_Side_Quests_Names_and_Lanterns.md`, `_Cloth_and_Memory.md`, `_Work_and_Skills.md`, `_Settlements_and_Combat.md` (micro-events MME and discoveries MDS are in Sett) |
| Enemies | `Enemies/Caelmor_Mire_Encounter_and_Enemy_Requirements.md` |
| Zones | `Zones/Caelmor_Mire_POI_and_Zone_Requirements.md` |
| Integration | `Quests/Caelmor_Mire_Integration_Requirements.md` |

Reference sources: `Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md` (CDR-1 to CDR-5: three quest states, no fail paths, walk-away and resume), `UNITY/README.md`, `UNITY/ARCHITECTURE_PIPELINE.md`, `Quests/LowmarkGameplay_Integration.md`, `Quests/Caelmor_Lowmark_v1_Integration_Requirements.md` (§8.1 co-op crediting), `Quests/Caelmor_Thornfell_Integration_Requirements.md` (TI-CO-06, Q-06), `Zones/Caelmor_Lowmark_Terrain_Narrative_Conflict_Register.md`, `MEDIA/Materials/README.md`, and a source grep of `UNITY/` and `CODE/`.

### Method

1. **Solo pass, main line.** A fresh character with no Lowmark or Thornfell history was traced through MR-M1 to MR-M5 and the post-story content: prerequisites, step transitions, access, equipment, quest items, skill gates and their time-cost alternatives, travel and crossing states, death and logout, repeated interactions, softlocks and rewards. Finding ids `SM-01` to `SM-30`.
2. **Solo pass, optional content.** The same check for the twenty side quests, micro-events (MME), discoveries (MDS) and post-story world content (MW). Finding ids `SS-01` to `SS-28`.
3. **Co-op pass.** Two characters progressing independently, walked as five pairings at different quest stages (section 5). Finding ids `CO-01` to `CO-21`.
4. **Technical-dependency pass.** Every runtime need in the Mire packages was compared with what current source demonstrates. Finding ids `TD-01` to `TD-22`.
5. **Bounded fixes.** Only objectively demonstrable narrative and cross-document errors were corrected, in place, with no id renames and no new quests, characters, lore, systems or geography. Consequential design alternatives were preserved for approval.
6. **Independent review.** A separate reviewer checked the whole fix diff against the findings and the repository files. It fixed a further set of defects in place: the name echo above, two leftover "next dusk" re-form rules, MLD's band in the Enemies file, host-state rows that were not yet marked provisional or that gated movement, and a credit rule that contradicted shared-progress rows (now Director items D-13 and D-14). Where a report and a file disagreed, the file was taken as the truth.

Duplicates found by more than one pass are merged below and cross-referenced by their original ids.

### Status labels

| Label | Meaning |
|---|---|
| **Fixed 2026-11-13** | Text corrected in the named files in this audit. |
| **Fallback added** | A content fallback for Sol was added beside the primary design; the primary design is unchanged. |
| **Pending GD / Director / Sol** | Marked in the files as open; no option was chosen. |
| **Open: owner** | Not changed; the named owner decides. |
| **Untestable** | Cannot be assessed until a playable Unity build exists. |

Severity: **High** (softlock, blocked progression, broken predicate, or a contradiction a player would hit), **Medium**, **Low**.

### Boundaries kept in this audit

- **Collin's positions are recommendations pending his approval and are not promoted to canon.** These are: MD-7 prefer the noncombatant Hollowfoot alternative; MD-3 accept the first-light crossing; MD-4 accept staged Chapel drainage; MD-8 retain the optional Night Count refight without reversing the resolved story; the Bannerline road accessible before MR-M5 with story interactions gated; Stillgrave war-washing only as explicitly uncertain local folklore; the rutting stalker omitted unless it has a distinct gameplay purpose. Every file that mentions them still marks them as open.
- **MI-CO-06 is a provisional presentation fallback only.** The host's personal quest state is never authoritative over another player's progression. This audit did not choose a networking architecture. Where shared state affects navigation or gameplay, the conflict and the possible solution families are recorded for Sol (section 5 and Integration §5.2 Q-18).
- **Enemies C-1 (1.5-second telegraph minimum for displacement) and C-2 (25% hazard protection)** are treated as authored encounter-tuning requirements pending Gameplay Designer review, not approved universal combat rules. The files now say so wherever they appear.
- **No geography was changed.** The Lowmark terrain conflicts and every Mire MAP VERIFICATION REQUIRED flag are kept (section 8).
- **No art, material, texture or colour was modified or prescribed.**

---

## 1. Summary

### Verdict

**Solo: logically playable after the fixes.** A fresh character can reach every main-line and side-quest completion and the post-story content without a softlock in the authored content. Every skill step on the main line has a time-cost crew alternative, so no Lowmark or Thornfell skill is required. Every step has a death respawn and a logout restore, and no quest can fail. The remaining solo risks are runtime capabilities that the content assumes and Unity does not yet demonstrate: above all, multi-level navigation for the Chapel (MR-M4), the keep-watch and presentation-hour system, runtime walkability changes, escort and boat movement, and mobile enemies. MR-M4 cannot be built until multi-level navigation exists, and it has no authored fallback because its progression is the floor descending.

**Co-op: optional assistance under CDR-6 (2026-11-14); it never gates solo completion.** The solo walkthrough above is the completion standard for every Mire quest. CDR-6 also decided the two co-op Director items (D-13 shared-task credit, D-14 the asker beat and junction calls): a partner is credited only when their own active step consumes the work, and personal flags and decisions stay independent. With partners at the same step the packages are coherent; with partners at different steps the shared-world conflicts below remain presentation questions for Sol and can strand only the co-op presentation, never a player's ability to finish alone. Before this audit, several package rules let the host's quest state decide a partner's navigation, interactions and credit. That wording has been removed: each player's own state now decides their own navigation, objectives, credit and completion in every file. What remains open is how a shared world presents state that differs between partners when that state is walkable ground or a gate (causeway crossings, Chapel water stages, standards, the crown and closure gate, walkways, presentation hour). Those are recorded with solution families for Sol and are not decided here.

### Top eight issues, in priority order

| # | Issue | Category | Status |
|---|---|---|---|
| 1 | **The Chapel (MR-M4) assumes multi-level navigation, ladders, stacked floors and runtime walkability swaps.** Current Unity has a flat navigation scene with no multi-level or off-mesh traversal. Every required MCS step depends on it, and no flattening workaround applies (SM-05, TD-01; section 4.1). | C | Open: Sol. Two content fallbacks added for push targeting and Mabyn's movement. |
| 2 | **Shared environmental state in co-op.** Partners at different steps need different crossing states, water stages, standards, crown props and hours in one shared space. One player's state can strand or block the other (CO-07 to CO-11, CO-15). | C | Downgraded by CDR-6 (2026-11-14): a presentation question for Sol (Q-18, families F1 to F5), not a prerequisite for solo completion; any family, including the lightest (F4 or F5), is acceptable. Host authority removed from text. |
| 3 | **Host-driven credit and completion in co-op.** Partners were credited for boards, posts and the MR-M5 gap hold they did not perform, and MI-CO-06 let host state drive walkable state (CO-01, CO-03, CO-04, CO-06). | A, High | Fixed 2026-11-13. |
| 4 | **Keep watch, the presentation hour and per-player walkability are not demonstrated in source.** Nearly every Mire step reads the hour or a crossing state (TD-09, TD-02, SM-24). | C | Open: Sol. |
| 5 | **Escort, boat ride and mobile enemies are required on the main path and listed as remaining work in Unity** (SM-06, SM-07, TD-07, TD-08). | C | Open: Sol. One fallback added for the harness haul. |
| 6 | **MR-M2 dusk and night steps sent the player across a causeway crossing that was Running at dusk and night,** and the crossing register broke its own one-turn rule (SM-01, SM-02). | A, High | Fixed 2026-11-13. |
| 7 | **The festival side quest MLD could only start after MR-M5 had auto-activated,** placing festival banners and a dry-weather pin inside the crisis, while the text claimed it was playable before MR-M5 (SS-02). Separately, MMR's required Echo fights could re-form in a loop (SS-01). | A, High | Fixed 2026-11-13 (SS-02 option (a); option (b) preserved for the Director). |
| 8 | **Displacement attacks told at 1.2 s conflict with the 1.5 s C-1 requirement,** while the Enemies file claimed full compliance (SM-04). | A, Medium | Pending GD. Rows marked; both options recorded. |

### What was fixed

Fifty-five source findings were applied in full or in part, or marked pending, across twelve files (section 9). The fixes correct crossing pins, step restore points, rewards that promised nothing, bible text that contradicted the acts, flag-writer and acceptance-test wording, re-form conditions, reversed stake readings, renamed-character leftovers, name collisions, side-quest prerequisites and timing, the lantern-debt contradiction, and every co-op rule that gave the host authority over another player's progression, credit or completion. Content fallbacks for Sol were added beside, not instead of, three primary designs. No step, flag, line or encounter id was renamed. No MAP VERIFICATION REQUIRED flag was removed (the count in the changed files rose from 98 to 101).

---

## 2. A. Definite authored-content contradictions

Merged across passes. "Fixed" means the contradiction is gone from every named file; the files carry a review-log row "Playability audit fixes, 2026-11-13".

| ID | Sev. | Location | Problem | Resolution |
|---|---|---|---|---|
| **A-01** (SM-01) | High | Act I MBR `S03` to `S06`, §B7 death, §B11; Zones X01/X02; Integration MI-CH-02, MI-CK-02 | MBR `S05` waits for dusk at the sanctuary and `S06` returns at night, but crossings C1 and C4 were Running at those hours and MBR pinned nothing. A death in MBR-E5 respawned the player behind a Running C1. This contradicted "Act I pins every state it needs" and AT-02. | Fixed 2026-11-13. X01 and X02 are pinned Slack for the pinning player from MBR `S03` to `S06` end, in Act I, Zones and Integration. |
| **A-02** (SM-02) | Medium | Zones §6.2 X01 and rules line; Integration AT-02 | The rule says a default never blocks travel for more than one keep-watch turn, but X01, on the only route between Sorrowmere and Marshfall, was Running at dusk and at night. | Fixed 2026-11-13. X01 default is now Slack / Slack / Slack / Running. The crossing table keeps its [PROPOSAL — DIRECTOR] label, so the Director may still rule otherwise. |
| **A-03** (SM-03) | Medium | Act I MBR `S04b` predicate, §B11 logout | The required `causeway.shard_moss` event fires only near Dunstan at the causeway head, but logout restored the player to the register room, past the trigger, with no objective sending them back. | Fixed 2026-11-13. Logout restores to the causeway head until `MBR_SHARD_MOMENT` is set, and a journal sub-objective "Carry the shard home by the causeway head" is shown. |
| **A-04** (SM-04) | Medium | Act III §7, §7.1.2 and §7.1.3, §7.2; Enemies C-1, C-7, §5.9, §7.1, §9.3 MBL-H3, compliance summary; Integration AT-07, MC-2 | C-1 asks for 1.5 s on any displacement, but five displacement attacks (file arrival, Planted Standard, gap step-off and related rows) are told on beat 2, about 1.2 s. The Enemies file claimed full compliance. | **Pending GD.** The five rows are marked "C-1 pending GD" and the compliance claim is corrected. Options recorded, none chosen: (a) show every displacement attack on beat 1 in all phases; (b) record count-carried attacks as a stated exception to C-1. |
| **A-05** (SM-16, CO-12) | Medium | Integration MI-EN-10; Act III §E.9; Enemies MW-01 | MI-EN-10 let any player start the Night Count at the muster post with no quest gate, and the refight and the story General shared one encounter id, so a refight defeat could satisfy a partner's MBL `S05` without the asker beat. | Fixed 2026-11-13. MI-EN-10 is gated on MR-M5 Completed. The refight is a separate encounter instance whose defeat never completes `S05`. Whether the two may run at one crown at the same time is open for Sol (section 5, conflict K-06). |
| **A-06** (SM-11) | Low | Act III §14.1; Act III dialogue `MBL-D2b.10`, `.11`, `MBL-B3.4` | §14.1 said the drifter lines stand as written under the MD-7 noncombatant branch, but three tagged lines describe hostile drifters. | Fixed 2026-11-13. §14.1 now states the swap variants (cut `.11` and half of `.10`; `MBL-B3.4` becomes "They're in the rags."). Both MD-7 branches are kept. |
| **A-07** (SM-12) | Low | Act II §A10, ferryman's pole | The reward promised "a key for post-story ferry content" that no file authors. | Fixed 2026-11-13. Phrase deleted. (Integration EM-01 never contained it.) |
| **A-08** (SM-13) | Low | Bible §6 table and §6.1 vs Act I `S01`, `S03`, `S04b` | The bible had Dunstan read the Hayle book itself and Ysolde ask for the original care leaf, which would make the Marshfall sub-objective pointless; Act I has a Memorykeeper's copy and the leaf read where it is kept. | Fixed 2026-11-13. Bible aligned to Act I. |
| **A-09** (SM-14) | Low | Act I Beat 4 and §A7; Enemies C-3, §10.2; Zones §7; Integration MC-4 | Act I and Enemies said the C2 standard's Wraith re-forms at every dusk outside quests; Zones said standards are presentation only outside quests. | Fixed 2026-11-13, **pending GD.** All files now use the simpler rule: the Wraith re-forms when a quest next presents its condition. |
| **A-10** (SM-15) | Low | Act I Beat 2 item 4; Act I dialogue `MNS-D5` | The tape hold was offered "now or later" during `S02`, but its dialogue was headed `S03` only. | Fixed 2026-11-13. `MNS-D5` is available from `S02`. |
| **A-11** (SM-17) | Low | Integration AT-11 | "All 12 `MR_` flags have one writer" ignored the documented second writer of `MR_ROWAN_TRUST`. | Fixed 2026-11-13. Exception named. |
| **A-12** (SS-01) | High | Cloth MMR.3, `S01`, `S02`, MMR.11; Enemies §10.2, §11.2; Integration MC-5; Zones; bible §7 MMR row | Three different re-form conditions. As written, MMR-E1 and E2 re-formed while the survey stakes stood, which covered the very steps that ask the player to defeat them. | Fixed 2026-11-13. MMR-E1 and E2 do not re-form. The stake-string Echoes re-form only while `S04` is active and stakes remain. All files, including the bible row, agree. |
| **A-13** (SS-02) | High | Names MLD.2, MLD.3; MLW; Act III MR-M5 auto-start; bible §7.1; Act I header and §B10 | MLD required MLW, which requires MR-M4, so MLD could only start after MR-M5 had auto-activated. "Playable before or after MR-M5" was false, and the festival's banners, dry pin and NPC placements collided with the crisis. | Fixed 2026-11-13 with **option (a)**: MLD needs MLL and MR-M2; the MLW keeper line is an optional read; MLD is not offered while MR-M5 is Active. **Option (b)** (MLD only after MR-M5 Completed, and Act III's dependency on MLD deleted) is preserved in MLD's open decisions for the Director (section 6). |
| **A-14** (SS-03) | Medium | Work MHG.1, .2, Beat 6, MHG.8, `MHG-D5`, `MHG-D6`, open decision 1; vs Names `MSS-D6.30`, bible MD-5, §7.2 | MHG made lantern debt a price that is called in ("owes a lantern-walk when asked", a grain call-in), contradicting the bible's "never a price" and MSS. | Fixed 2026-11-13. Wystan chooses to acknowledge Tilda's walk unasked; no call-in. Line ids unchanged (the speaker of `MHG-D5.01` is now Wystan). MHG stays [PROPOSAL — DIRECTOR]. |
| **A-15** (SS-04) | Medium | Zones §6.2 X10; Integration MI-CH-04 | Both reversed the stake grammar ("reach at Slack, wade at Running") against bible §1.1 and MWS. | Fixed 2026-11-13. "Wade at Slack, reach at Running." |
| **A-16** (SS-05) | Medium | Names MEP Beat 2 (two places), `MEP-I2.01`, `MEP-I2.02` | The deduction clue still read "Keel, J." after Jem was renamed Lew. | Fixed 2026-11-13. "Keel, L." in all four places. |
| **A-17** (SS-08) | Low | Sett MRW `S02`; Zones X14; Integration MI-CH-02 | MRW gated a presentation-only stake and misread Running. | Fixed 2026-11-13. Keep-watch line deleted; MRW removed from MI-CH-02 consumers. |
| **A-18** (SS-09) | Low | Zones §3 R4 | R4 was "first used MR-M3", but side content uses it from MR-M1. | Fixed 2026-11-13. First used at MR-M1 by side content; never gated. |
| **A-19** (SS-10) | Low | Act I §B9.2 `MBR_PINS`; Integration §3.2 | Act I promised an Oswin line in MLD that MLD does not author. | Fixed 2026-11-13. The reader is the existing `MLD-I1.02` inspect; no line was authored. |
| **A-20** (SS-11) | Low | Names MLW Beat 3 | "The player knows the stitch" is false when `MLL_HOOD = crew`. | Fixed 2026-11-13. Phrase deleted. |
| **A-21** (SS-12) | Low | Enemies §11.2 MSG-E1 | The row still described the replaced gust cycle. | Fixed 2026-11-13. Row uses MSG's wave logic. |
| **A-22** (SS-13) | Low | Sett MBO; Cloth MBS | Two Ridge Wardens at Griefwatch with different stays could read as one person. | Fixed 2026-11-13. One line in each file states they are two people (MBO's Warden is role-named to match Act III, so the stays do not reconcile). |
| **A-23** (SS-14) | Low | Sett MNK `S05`, `S06` | `S06` required the ninth stake "reseated", but nothing lifted it first. | Fixed 2026-11-13. `S06` lifts the ninth and tries it in the side socket first. |
| **A-24** (SS-15) | Low | Work MHG; Sett MRW; Names MLL | Near-duplicate names: Briony Jessop and Bryony Haddow; Corwin Tey and Corin Haddow. | Fixed 2026-11-13. Avis Jessop and Godwin Tey, collision-checked (the first replacement, Merryn, was changed in review because it echoed Lowmark's Merrin family) across Lowmark, Thornfell and Mire. |
| **A-25** (SS-16) | Low | Sett MRH | An arrowhead "grown into the base of one antler" for years, though antlers shed yearly. | Fixed 2026-11-13. Skull at the antler base. |
| **A-26** (SS-27) | Low | Names MEP ferry book; Cloth MFW; Zones X04, X06 | Both texts imply a ferry from Blackwater Landing to the Rootrest side that the crossing register does not show. | **Open: map owner.** MAP VERIFICATION REQUIRED notes added in Zones §6.2, MEP open decisions and MFW.4. No geography changed. |
| **A-27** (CO-01) | High | Integration MI-CO-06; bible §9 and §9.2; Zones §0.1 and §6; side-file co-op bullets | MI-CO-06 let the host's state drive channel states, water stages, standards, lit posts and the gap stone. Those are walkable ground, interaction targets and hazard gates, so the host decided other players' navigation and completion. | Fixed 2026-11-13. MI-CO-06 is now a provisional presentation fallback pending Director review that never decides another player's walkable ground, interactions, step, credit or choice. New Integration Q-18 records the conflicts and families F1 to F5. D-6 and Q-08 updated. |
| **A-28** (CO-02) | Medium | Integration MI-CO-06; bible §9 | Cited Thornfell and Lowmark as precedent for host state; neither adopted it (Thornfell recorded three styles and recommended "first choice in the shard"; Lowmark §8.1 "first player's result shows for all"). | Fixed 2026-11-13. Precedent stated accurately; no region has an approved shard-level rule. |
| **A-29** (CO-03) | High | Act II §A7, §B7; Integration MI-CO-01; Sett MRH.13 | "All present are credited", including partners at an earlier step who were credited for boards and posts they did not do, against Lowmark §8.1 ("credits every participant whose own active step consumes it"). | Fixed 2026-11-13. Credit only from each partner's own active step. |
| **A-30** (CO-04) | High | Act III §11; Integration MI-CO-01 | The host's hold drove the arrivals and every partner present was credited per gap segment, so a partner could complete MR-M5's central rite without holding. | Fixed 2026-11-13. Each partner's segments count only from their own hold. |
| **A-31** (CO-05) | Medium | Act II §B12 custody row vs §B7, §B11; Integration Q-08 | Two different fallbacks for the same custody props. | Fixed 2026-11-13. One wording: per player; provisional presentation fallback per MI-CO-06. |
| **A-32** (CO-06) | Medium | Integration AT-03, AT-13; Act II §B7, §B12 N-3; Enemies §1, §9.2 | The provisional host fallback was written as acceptance tests and as the Chapel water-stage rule. | Fixed 2026-11-13. Tests now require that no partner's walkable ground, interaction or credit depends on another partner's state; the water stage is per player and its co-op presentation is unresolved (Q-18). |
| **A-33** (CO-17) | Medium | Act III §7; Integration MI-CT-01; Enemies §1 | Shared count versus per-player count; a partner not on MBL could be struck without tells. | Fixed 2026-11-13. The count is the encounter's timer; every player who can be struck receives its tells. Mechanism is Sol's. |
| **A-34** (CO-21) | Medium | Act III §11 vs Zones §6.4, Integration Q-10, Sett MBO.4 | Act III said other players see a closed road before MR-M5; Zones, Q-10 and MBO say the gate is open. | Fixed 2026-11-13. Each player sees their own state; the road-open position stays a pending Director recommendation. |
| **A-35** (TD-19) | Low | Integration MI-WL-01, MI-PP-06 | Cited Lowmark G14 (drift-site state) for per-player environment variants; the correct rows are G16 and M44. | Fixed 2026-11-13. Citation corrected; walkability noted as a Mire extension beyond G16. |

---

## 3. B. Likely gameplay or pacing problems

| ID | Sev. | Location | Problem | Resolution |
|---|---|---|---|---|
| **B-01** (SM-18) | Medium | Act II MR-M3 `S02` to `S05` | A player using every crew alternative and asking Rowan could need seven to nine identical keep-watch clicks in a 35 to 45 minute quest. | Fixed 2026-11-13 (simplification, no new feature): one wait completes every crew alternative commissioned before it, and the objective text tells players Sennic's sittings advance on any turned hour. Remains the main line's weakest stretch (see verdict). |
| **B-02** (SM-20) | Medium (possible) | Bible MD-10, §11.6; all main packages ("Skill XP: action only") | A player who goes straight down the main line earns XP only from actions and a modest amount of combat. Whether they reach the "Advanced" band by MCS-E3 and the General depends on side content. No level gate exists, so this can stall but not block. | Open: GD. Confirm level bands against the main line's own yield. |
| **B-03** (SM-21) | Low | Act II MRC to MCS (continuous) | A player low on food after MRC-E2 had no restock before the act's densest fight. | Fixed 2026-11-13. Mabyn's peat stove is a cooking spot and she offers food. |
| **B-04** (SM-22) | Low | Act I MR-M1 to MR-M2 | No journal lead pointed to MR-M2's offer. | Fixed 2026-11-13. "Calwen is asking for the witness." |
| **B-05** (SM-23) | Low | Act III §7.1.5, §11; Enemies §7.1, §11.1 | Logout restarted the boss at 100% while death restarted the phase, so dying was cheaper than logging out. | Fixed 2026-11-13. Logout restores the same phase checkpoint as death. |
| **B-06** (SS-06) | Medium | Work MRS and MFH accept gates; bible §7.2 | Hunting and Woodcutting gates pointed to levels earned in Lowmark or Thornfell, but the play order is free and no in-region training to those levels was found. | Partly fixed: "already learned in Lowmark" deleted from the bible; the twelve gates read "[GD: entry level, reachable in the Mire]". **Open: GD** sets the numbers. |
| **B-07** (SS-07) | Medium | Sett MBO; Names MSS; Cloth MBS; Act III §11 | A first visit to Griefwatch after MR-M4 fired the MBO bark about an open gate at the moment MR-M5 shut it; MSS and MBS scenes used the hall MR-M5 occupies. | Fixed 2026-11-13. The MBO bark is suppressed while MR-M5 is Active; MSS and MBS hall scenes wait until MR-M5 `S03` is complete. |
| **B-08** (SS-17) | Low | Sett MNK.1 | An unanswered "Want next: who Stakeman Varne was" hook. | Fixed 2026-11-13. Deleted. |
| **B-09** (SS-18) | Low | Cloth MCF | Bare poles stayed leaning after completion, and the "day assault" could happen at night. | Fixed 2026-11-13. Poles are laid on completion; `S03` to `S05` pinned to day. |
| **B-10** (CO-14) | Medium | Names MLD.10, MEP.10; Act I §A7, §A11 | Escorts fell back to following the host, who might not be on that quest, leaving an escort with no owner. | Fixed 2026-11-13. An escort follows its own quest owner. Overlapping causeway set pieces remain a Sol conflict (section 5, K-01). |
| **B-11** (TD-06) | Low (possible) | Act II §B5.2 G3; Zones MP13 | The agility gap's walkable fallback goes "back round through the loft", but only one loft-to-gallery link is described. If there is no second link, Windlass C sits behind an agility trigger, against Zones §0.1. | Open: zone pass. MAP VERIFICATION REQUIRED for the Chapel interior; no geometry chosen here. |

SM-19 (the hidden `MRC-L-ROWAN` window) and SS-19 (five thin side quests) are pacing problems whose remedy is a Director choice; they are listed in section 6.

### Pacing verdict

The walkthrough judged pacing from the authored steps only. Feel, length and difficulty need a build.

- **Act I (MR-M1, MR-M2): the strongest RuneScape-style stretch.** MR-M1 is a real investigation: travel across a route that changes with the channel, evidence gathered in any order from four keepers, a skill step with a time alternative, an escort, and a hold board where the player reasons with objects. MR-M2 makes labour the gameplay (lift, pin, fold under attack, lever) and ends with a miniboss beaten by bringing a standard down. Weak spot: the three standards in MR-M2 `S03` are the same four-part job three times; the escalation (bearer, slope, seams) carries it, but only just.
- **Act II: split.** MR-M4 (the Chapel) is a genuine dungeon: read the building, an order puzzle with a guaranteed hint, light-against-dark pressure and a timed escape. MR-M3 is the main line's weakest quest: four preparation chores and three hour-gated sittings joined by keep-watch waits. The fix in B-01 removes the worst repetition; the waiting theme remains. Its first-light crossing is good once it starts.
- **Act III: a full capstone.** A records task, a taught rhythm used to move, then fight, then hold still; a three-phase boss; a played rite. Weak spots: the `S01` roll is a three-match show-evidence task that is light for a capstone opener, and the six-to-eight-minute gap hold in `S06` risks becoming a waiting exercise.
- **Side content.** The strongest optional quests use real verbs and make good use of the stake and keep-watch reading: MRS, MFH, MFT, MNK, MRH, MCF, MSG, MLL, MBO and MWS. The weakest are strings of scripted interactions: MHG (talk, inspect and walk only), MFW (watch, read, ask), and the MBA, MSS and MBS inspect chains, which are mostly dialogue gates (SS-19, section 6).
- **Co-op.** Before the fixes, co-op degraded into one player playing and the other being credited. The text now requires each partner to do their own work; whether that is achievable depends on Sol's answer to section 5.

**Weakest spots overall:** MR-M3 `S02` wait chain; MBL `S06` hold length; MBR `S03` repetition; MHG and MFW as side quests.

---

## 4. C. Technical dependencies requiring Sol

Status against current source (`UNITY/README.md` and a grep of `UNITY/` and `CODE/`): **Demonstrated**, **Partly**, **Not demonstrated**. Current Unity facts used: click-to-move on a host NavMesh; "The current flat navigation scene has no multi-level or off-mesh traversal"; remaining production work includes "mobile enemy pursuit", "complete NPC lifecycle/escort and inspection walks", "authored water-state scheduling", "walk-away resume prompts" and "co-op behavior"; "Enemy bodies are anchored greybox encounters"; "Death restores health at the crew fire and retains progress/items"; checkpoints are a local file and "World position, multiplayer membership and wall-clock simulation are not persisted"; `LocalFloorVisibilityPresentation` is opt-in, "not wired into the playable scene", and its "Unity scene integration and rendered multi-camera behavior remain unvalidated".

### 4.1 Multi-level navigation and the Chapel (MR-M4)

**Status: Not demonstrated.** Source grep finds only `NavMesh.CalculatePath(..., NavMesh.AllAreas, ...)` and no NavMesh links, off-mesh links, obstacles or area masks. The Lowmark precedent replaced the Flood Kitchen loft stairs with flat access markers because multi-level traversal is unfinished (`LowmarkGameplay_Integration.md`). That workaround cannot apply to the Chapel, because MCS progression is the floor descending. Integration MI-AG-02 is a MUST with no fallback for the Chapel, and the Chapel is the only route to R08's custodians.

**What each step assumes (all required unless noted):**

| Step | Assumed capability |
|---|---|
| MRC `S06`, MCS `S00`, `S08` | Boat to roof landing stage transfer at the end or start of a ride spline (off-mesh or scripted transfer). |
| MCS `S01` | Sloped roof ridge; two posts in knee-deep shallows; a Reedlurker fight at the slope edge (slope plus wade slow). |
| `S02` | Hatch ladder roof to bell loft, second ladder loft to gallery (interaction-driven vertical moves); Mabyn climbs down to G6 (NPC ladder traversal); the first scripted Shade push. |
| `S03` | Windlass A in the loft and B and C on the gallery, worked B, C, A, so the player crosses the ladder repeatedly; the gallery agility gap and its fallback round through the loft (B-11); a stair G6 to N1; **three runtime walkability swaps** as the water drops, with the player standing in the space; the aisle walk N1 lies directly under the gallery (stacked floors: click picking, camera occlusion, floor visibility); Crawlers and Reedlurkers must path across stages. |
| `S04` | Vestry door off N2 (ordinary once N2 exists). |
| `S05` | Slab lift opens a crypt stair below the nave floor (another stacked layer). |
| `S06` | Timed ascent from floor to bays to aisle to gallery (stair) to loft (ladder) to hatch (ladder) while posts gutter; the Shade push target must be computed along the walkable route, not straight-line, or it can drop the player onto another floor; Mabyn pulls the player up through the hatch (scripted vertical transfer). |
| `S07` altar outcome | The player and Mabyn go back down the whole line to the crypt (NPC following across stairs and two ladders). |
| Post-quest revisit | All of the above at the final stage. |

**Floor visibility.** The adapter that exists builds floors from generator-manifest volumes in horizontal bands. The Chapel is a hand-authored landmark whose nave is a double-height void with a perimeter gallery and changing water. Whether the adapter fits is unknown (TD-04).

**Authored fallbacks (added beside the primary design; Sol may accept them; no design change):**
- Shade push: to the nearest lit post reachable on the walkable route, never across a level change (Act II Beat 9, §B8.1, §B12 N-2; Integration MI-LT-04). Sol fallback: the last lit post on the player's own level or the stair head above it.
- Mabyn across levels: Sol fallback has Mabyn wait at G6 in the altar outcome rather than following (Act II §B12; Integration MI-AG-02). Placement sets (MI-PP-04) can stand her at G6 and in the crypt.

**What cannot be avoided:** per-stage NavMesh variants or area toggling with agent re-snap on swap, ladders as scripted moves, and visibility and click picking for stacked floors. These are hard prerequisites for MR-M4.

**Other required multi-level spots (SM-09, Medium; Partly).** MR-M1 `S03` and `S04b` stilt-house steps and the Ferrow house on taller piles; MR-M3 `S00` to `S01` stair or ramp down to Blackwater Landing; MR-M5 `S02` Bran's watchpost platform. Low risk if built as ramps. **Fallback added:** the MBL `S02` furrow inspect may sit on a ground-level pad at the watchpost; the platform is presentation (Act III §5.2, Beat 2; Zones MP17, with MAP VERIFICATION for the pad's sightline; Integration MI-AG-02).

### 4.2 Per-player walkable and environment state

| ID | Sev. | Need | Status | Depends on it | Fallback |
|---|---|---|---|---|---|
| TD-02 | High | Runtime walkable-segment switching (crossings, water stages, walkway, closure gate), per player or per instance | **Partly** for persistent one-way water presentation (the Lowmark waterline survives reload). **Not demonstrated** for any state change that alters walkable ground, or for per-player walkability on one host NavMesh. `Build.ps1` does not rebake navigation. Lowmark G16 asked only for per-player presentation. | MNS `S02`, `S04`; MBR `S03` to `S06`; MRC; MCS `S03`; MWS walkway; MBL gate; every co-op conflict in section 5 | None for walkability. The integration rows now note that "per player" here includes walkability. |
| SM-24 | Medium | Agent re-snap when a segment closes under or near the player | Not demonstrated | MNS `S04` turns stakes Sour behind the cart, close to the player | None |
| TD-17 | Medium | Lit radius, post states, hand lantern, Shade push and draught (MI-LT-01 to 05) | Not demonstrated (push alone is Partly, flat only) | MCS `S02` to `S07` | "Pre-authored lit and dark zones flipped at each drainage stage" still needs per-player zone switching, so it inherits TD-02. |

### 4.3 Escort, ride and NPC movement

| ID | Sev. | Need | Status | Depends on it | Fallback |
|---|---|---|---|---|---|
| SM-06, TD-07 | High | Cart follow, halt and re-park; boat ride on a spline with stops, halts, combat from a moving boat, mid-ride disembark and re-board; wardens following and holding bends in MR-M5; ~20 NPC arrivals | Not demonstrated ("complete NPC lifecycle/escort" is remaining work; Lowmark still needs Tamsin's escort movement). No escort key in the schema. | MNS `S04`; MRC `S03`, `S05`; MCS `S08`; MBL `S03`, `S05`, `S06`; MLD, MEP, MLW, MFT, MHG escorts | Existing: MI-ES-02 halt fallback; MI-ES-04 bark-only asker; Act III arrivals spawned at their marks with a fade. **Added:** the MRC harness haul may run as three channel segments at a fixed bank pad beside the grounded boat (Act II §A12; Integration MI-ES-02). The follow and ride themselves have no fallback. |
| TD-03 | Medium | NPC ladder traversal and scripted player transition through the hatch | Not demonstrated | MCS `S02`, `S06`, `S07` | Mabyn waits at G6 (4.1). |
| TD-15 | Low | Respawn "aboard at the last passed junction" of a moving boat | Partly (conditional respawn regions exist; a moving anchor does not) | MRC `S03`, `S05` | None |

### 4.4 Mobile enemy pursuit

| ID | Sev. | Need | Status | Depends on it |
|---|---|---|---|---|
| SM-07, TD-08 | High | Wraiths advancing and shoving down a road lane; the Colour's four-pace Advance; Echoes wading about 6 s to the boat (MRC-E2's "the cut always ends" depends on this timing); Crawlers bursting and closing; Reedlurker lunges; the General moving into a player's lane; Bog Hounds | Partly: telegraphs, windups and movement dodges are demonstrated; moving enemies are not ("mobile enemy pursuit" is remaining work). File and lane-Wraith patrols are probably the smallest part. | Required fights in MR-M2, MR-M3, MR-M4 and the MR-M5 boss |
| SS-22 | Low | MRS scripted dusk flight and heron; MRH patch-seeking Hart; MFH rowing crossing | Not demonstrated | Side quests only |

### 4.5 Keep watch and the presentation hour

| ID | Sev. | Need | Status | Depends on it |
|---|---|---|---|---|
| TD-09 | High | Keep watch, per-player presentation hour, hour pins, hour-keyed props, quest weather (MI-CK-01 to 04, MI-DG-06) | Not demonstrated. No keep-watch, presentation-hour or weather code in `UNITY/` or `CODE/`. | Almost every main step: dusk and night pins, Slack turns, the grey, Sennic's sittings, Rowan's asks, the MBL night pin, the MCS buttress schedule, the Night Count. This is the largest single dependency after co-op. |

### 4.6 Channel schedule and pins

| ID | Sev. | Need | Status | Notes |
|---|---|---|---|---|
| SM-08 | Medium | Pin lifetime | Text fixed 2026-11-13 | Integration MI-CH-02 and MI-CK-02, Act I §A12 and Zones now say pins are step-scoped and release to the Zones default at step end, and quest completion releases all. Without this, MNS `S04`'s Sour pins could have closed the causeway after MR-M1. MBR `S05`/`S06` and MCS `S03` rows were added to MI-CK-02. |
| SS-20 | Medium | Discoveries (MDS01, MDS10) read crossing states but have no quest to pin them | Open: Sol | Define a pin rule for discoveries, or require each discovery to read correctly in any state. |
| (scheduling) | High (part of TD-09) | Per-crossing schedule MI-CH-01 | Not demonstrated ("authored water-state scheduling" is remaining work) | Rides on TD-09 and TD-02. |

### 4.7 Other runtime needs

| ID | Sev. | Need | Status | Note |
|---|---|---|---|---|
| TD-10 | Medium | Resume hooks, sub-progress, logout restore to the step's location and hour | Partly: flags, stages, choices, inventory persist; position by step, hour, kept segments, resume prompts and autosave do not ("Reload starts at the road head"). | Every logout row in the Mire assumes step-located restore. |
| TD-11 | Medium | Kept-progress channels and ordered sequences with reset | Partly: timed, interruptible channels exist; segments kept across interrupt, death or logout, and order-check reset, do not. | The MBL gap hold and the MCS windlasses depend on it. |
| TD-12 | Medium | Boss phase checkpoints, invulnerable transitions, per-participant scaling | Partly: enemy leash exists; phases do not. | MBR-E5, the General, MNK and MRH bosses. |
| TD-16 | Medium | Deep-water edge stop with bark; shallows slow; status effects; the 25% hazard clamp | Partly: collision-validated push and closed ground exist; slow and clamp do not. | Labels fixed 2026-11-13: MI-EN-07, both MC-9 rows and Enemies C-1 and C-2 are "authored tuning requirement, pending Gameplay Designer review". Values unchanged. |
| TD-04 | Medium | Floor visibility for stacked interiors | Not demonstrated (adapter exists, unwired and unvalidated) | Question for Sol: can the adapter serve a hand-authored interior with a gallery over an open nave, or does the Chapel need another approach? |
| TD-05 | Medium | Push target across levels | Partly (push demonstrated on flat ground) | Wording fixed 2026-11-13 (4.1). |
| TD-13 | Low | Carry states and deposits | Demonstrated (carry objects never enter inventory; collectable again after death or reload). "Cannot be dropped by a hit" is not shown. | None. |
| TD-14 | Low | Flag-gated dialogue, evidence choices, persistent choices | Demonstrated. Paged document views (MI-DG-03) and hour-gated dialogue (MI-DG-06) are not. | Sol for MI-DG-03. |
| TD-20 | Low | Chapel glass emissive state, nave water | Not demonstrated through the import pipeline ("Transparent/emissive materials ... are rejected"). Consistent with the Chapel being a hand-authored landmark. | Recorded so nobody expects these from the generator. No art direction implied. |
| TD-21 | Low | Zones §10 tool-status statements | Accurate against current READMEs, with one understatement: exports already carry floor metadata and an unwired floor adapter exists. | Optional wording update in Zones §10; not applied. |

---

## 5. Co-op

### 5.0 CDR-6: co-op is optional assistance (2026-11-14)

Collin ruled CDR-6 on 2026-11-14 (`Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md`, §1 and §3.7). For the Mire this audit now reads as follows.

- **The solo walkthrough stands as the completion standard.** Every Mire quest, main and side, was walked logically solo (section 1) and that walk is the test of completion. No co-op or shared-state solution is a prerequisite for finishing the solo questline.
- **Co-op is evaluated only as optional assistance.** Sections 5.1 to 5.3 are kept as recorded. The conflicts K-01 to K-10 stay documented for Sol as shared-world presentation and networking questions; they can affect how partners at different steps see one world, not whether either can finish alone. Integration Q-18 and AT-13 were downgraded accordingly, and no new runtime requirement is created only to support elaborate co-op mechanics.
- **Credit and personal state (D-13, D-14 resolved).** A partner receives shared encounter or task credit only when their own active step consumes it. MRC mending and gathering, MMR stakes, MBA spine, MCF count and MSG vents now say so; an MRC task a partner finished counts for the other as that task's crew path, and the "mended it yourself" pole and lines go only to the player who mended. Each partner's `MBL_ASKER` comes only from their own action (default `wardens`, as in solo), and MRC junction calls count only for the caller's own `MRC_WRONG_CALLS`.
- **MI-CO-06 (D-08)** is a presentation fallback only, governed by CDR-6; every "pending Director review" qualifier on it in the packages now reads so.
- **Leaving never blocks.** MI-CO-08 now states that a partner who leaves, disconnects or is ahead never blocks the other; the remaining player finishes alone from their own persisted step.
- **Bosses checked solo.** The General (MBL-E6; solo 6 to 8 min, Act III §7.1.5), MCS-E3 (solo 2 to 3 min), the Mud-Boss (MNK-E3) and the Rust Hart (MRH-E1) are authored with solo targets and no group tuning; co-op only scales health up from the solo baseline (MI-CO-04). The gap hold in MR-M5 `S06` is held by the one player while NPCs fill the ring; no second holder is needed. The Night Count (MW-01, `[MD-8]`) may be tuned higher than the story fight but now states it stays solo-achievable.

### 5.1 Principle now written into the packages

Each player's own quest state decides that player's own navigation, objectives, interaction availability, credit, choices and completion. A partner is credited for a defeat or action only when their own active step consumes it (Lowmark §8.1). Each partner's own flags drive their barks, dialogue and epilogue. An escort follows its own quest owner. No partner's keep watch or pin advances another partner's hour-gated step. A host leaving is treated as a logout for every partner, who then restores from their own persisted state by their own step's logout rule (Integration MI-CO-08).

**Host-driven presentation is provisional.** MI-CO-06 now reads: where the runtime cannot show different props to partners, one shared visual state may be shown; it never decides another player's walkable ground, interaction availability, step, credit or choice. It is pending Director review (Integration D-6) and is not an approved universal co-op rule. **Superseded 2026-11-14:** CDR-6 now governs it as a presentation fallback only (section 5.0).

Some side-file and Enemies rows still say "(fallback: host)" for props (MRW.13 NPC table placement, MNK.13, MRH.13 prop, MWS.10, MCF, Enemies §7.2 Colour pulse). They were left as authored and now sit under the file-level provisional qualifier. The Enemies §7.2 Colour pulse row should be read with Act I §B7, which now lists the pulse source as an open Q-18 item.

### 5.2 Pairings walked

| # | Partner 1 (host) | Partner 2 | What the walk found |
|---|---|---|---|
| P1 | MR-M4, in the Chapel | MR-M1 | P2 cannot reach the Chapel on their own state (Rowan's route opens after MRC). Nothing says whether Rowan ferries a partner who has not done MRC. If ferried, P2 stands in the host's water stage without a hand lantern and, before the fix, was credited for boards and posts. At the causeway, P2's crossings followed the host's channel states and hour. |
| P2 | MR-M5 Completed (Night Count unlocked) | Starting MR-M5 | The host's quieted or tended crown props and open gate replace P2's risen lane-head standards and shut gate. Before the fix, the Night Count and P2's story General were the same encounter id. P2 could be struck by files without seeing the count. |
| P3 | MR-M3, one outcome | MR-M3, the opposite outcome | `MR_ROWAN_TRUST` stays per player (sound). One Rowan and one boat serve two steps. Junction calls go to whoever answers first. Mending credit gave P2 the "mended it yourself" pole and lines. |
| P4 | Main-line set piece | A side quest in the same space | MLD `S04` (children's line, every stake Slack) against MNS `S04` (cart, crossings turning Sour behind it) on the same causeway; MLW on the Chapel roof against MCS `S01`; MWS walkway in Marshfall against MNS `S03`. |
| P5 | Disconnect and host departure | Any | Every logout rule covered only the player's own logout. Nothing covered the host leaving while P2 rides the boat, stands on the host's stage-3 floor, or is in the host's arrivals. |

### 5.3 Shared-state conflicts that affect navigation or progression

**Solution families for Sol** (recorded in Integration §5.2 Q-18; **none is chosen here, and this audit does not propose a networking architecture**):

- **F1. Per-player phased set piece.** Each player at a stateful step gets their own copy of the set piece; partners share only when their states match.
- **F2. Per-viewer props and walkability.** Props, environment variants and walkable segments resolve from each viewer's own state, with per-player path checks on the host. The heaviest option; Lowmark G16 asked only for the presentation half.
- **F3. Shared presentation that never gates navigation or credit.** One shared visual state may show, but each player's walkability, interactions and credit are checked against that player's own state. If visuals and rules disagree, the rules use the player's own state.
- **F4. Compatibility gate on entry.** A stateful set piece can be entered together only at the same step and state; otherwise the further-ahead partner joins in the other's state as a helper who makes no progress.
- **F5. Defer to solo.** The stateful step pauses in co-op and resumes alone or with a same-step partner; the partner sees a neutral state.

| ID | Sev. | Conflict | Families that fit | Fixed in text meanwhile |
|---|---|---|---|---|
| **K-01** (CO-07, CO-14) | High | **Causeway crossings.** P2 on MNS `S02` must keep watch to turn X01 Slack; P2's keep watch cannot move the host's state, so under host presentation P2 could never cross. If the host runs MNS `S04` at the same time, the host's cart turns X02 Sour behind it and cuts off P2 on MNS `S03`. MLD `S04` and MNS `S04` need opposite stake states on X01 and X02. AT-02's one-turn guarantee held only for the host. | F3 (walkability from each player's own pin; the stake prop shows any state), F2, F5 | Escorts follow their own owner; host cart fallback deleted. |
| **K-02** (CO-08) | High | **Presentation hour.** The hour is per player, but partners in one shard share lighting and fauna. Channel defaults, hour-gated asks and sittings, dusk Wraiths, the MBL night pin, the MCS dusk Slack and the Night Count all read it. One player's keep watch could move the other's gates, or the hour diverges in a shared space. | F3 (each player's hour drives only their own pins, gates and spawns; shared lighting is presentation), F1 for pinned set pieces, F5 for hour-gated steps | Q-18 states that no partner's keep watch or pin advances another partner's hour-gated step. |
| **K-03** (CO-09) | High | **Chapel water stage and lit posts.** A partner at an earlier stage, or with no MCS, walks host-stage ground (N1 to N3) that does not exist in their own state; when the host leaves, that ground becomes deep water. The partner may have no hand lantern, but the dark-ground timer runs on the carried lantern. The stage-3 glass moment is once per player. | F1 (per-player Chapel instance) or F4, plus F3 for lit posts | Water stage is per player in Act II, Enemies and Integration; co-op presentation unresolved. **Open GD question:** how Shades treat a partner without the hand lantern. |
| **K-04** (CO-10) | High | **Roadside and field standards (MBR).** If the host has completed MBR, the standards are removed or folded, so P2 on MBR `S03` or `S05` has nothing to lift, pin or fold. In reverse, P2 has folded but the host's standard is risen, so Wraiths keep re-forming for P2. | F1, F2, F4 | "On the host's props" deleted from Act I §B7 and §B11; the Colour's pulse source is an open Q-18 item. |
| **K-05** (CO-11) | High | **The crown and the closure gate (MBL).** If the host is quieted or tended, P2 at MBL `S04` has no risen lane-head standard to cut, lift or fold. The host's open gate lets P2 walk up to a crown that is quiet in P2's view. In reverse, a host in MBL `S00` to `S03` (gate shut) blocks a partner who has not reached MR-M5 from road content that exists before MR-M5 (Integration Q-10; MAP VERIFICATION REQUIRED for whether MSS's spoon lies past the gate). | F1 (per-player crown for `S02` to `S07`), F4, F5; F3 for the gate | Each player sees their own road state (A-34). Collin's road-open recommendation fits F3 for the gate but stays a recommendation. |
| **K-06** (CO-12) | High | **Night Count beside a story General.** P1 may strike the muster post while P2's story fight or unretired standards are at the same crown. | F1, F4, F5 | The refight is a separate instance that never completes `S05` (A-05). Coexistence is Sol's. MD-8 itself stays a Director decision. |
| **K-07** (CO-15) | Medium | **Walkways and stakes as route geometry.** Before MWS, P2 has a sunk section and the root run; under host presentation P2 walks the host's repaired walkway, then stands on geometry their own state lacks when the host leaves. MNK seats stakes against the host's socket states. | F3 or F2 | Rows sit under the provisional qualifier. |
| **K-08** (CO-13) | Medium | **Single named NPCs and vehicles.** One Rowan and one boat serve P1's crossing and P2's practice runs; one Mabyn serves MCS `S02` and MLW; one Ysolde stands at the landing (MCS `S08`) and the register table (MRC `S00`). The partner's required speaker can be elsewhere. | F2 (per-player NPC instances or phasing), F4 (shared ride only at the same step), F5 | None; no content change proposed. |
| **K-09** (SS-21) | Medium | **Weather and festival pins.** MLD festival banners and dry pin, MLW rain pin, MSG storm pin and the MR-M5 ochre pin differ by quest state. | F3, F2, or the provisional host presentation as long as it never gates anything | MLD is no longer offered while MR-M5 is Active (A-13), which removes the solo version of this clash. |
| **K-10** (CO-18, CO-19) | High | **Disconnect, reconnect and host departure.** A partner who dies or reconnects during the shared boat ride respawns "aboard" a boat that has moved on. A partner reconnecting into a host world at another water stage or crown state may have a respawn anchor on ground that is not walkable in that variant. Where a non-host partner's flags, sub-progress and items persist after play in the host's session is undefined; current Unity persists a local checkpoint file and not multiplayer membership. | F1 or F4; or F5 (an out-of-step partner respawns at their own step anchor in their own state) | MI-CO-08: host departure is a logout for every partner. Persistence ownership is Sol's and untestable until a co-op build exists. |

Two co-op items are Director decisions rather than Sol conflicts (CO-16 shared-task credit and CO-20 one partner's action setting another's choice flag); they are in section 6 and were resolved by CDR-6 on 2026-11-14 (D-13, D-14).

**Co-op verdict.** With partners at the same step, the packages are now coherent: shared enemies, individual credit, per-player choices and per-player epilogues. With partners at different steps, K-01 to K-05 and K-10 can strand or block a partner's co-op session until Sol picks a family per set piece. MR-M4 and MR-M5 are the hardest cases. **Under CDR-6 (section 5.0) these are presentation questions for co-op only: none prevents either player from finishing alone from their own step.**

---

## 6. D. Director-level decisions

Nothing in this section has been approved by this audit. "Recommendation" means Collin's current recommendation, pending his explicit approval.

| ID | Decision | Collin's recommendation (pending) | What the audit found | Alternatives preserved |
|---|---|---|---|---|
| D-01 (SM-27) | **MD-7** Hollowfoot drifters at the Rag Bend | Prefer the noncombatant alternative | Playable either way. MBL-E3 is optional, off route and carries nothing; no main step, flag or evidence depends on it. The swap needed text variants, now stated in Act III §14.1 (A-06). | Both branches kept in Act III §14.1, the dialogue and Enemies. |
| D-02 (SM-25) | **MD-3** First-light crossing | Accept | Playable: every crossing hour is pinned, and logout returns to the landing at morning. No content change needed. | The alternative remains in the bible MD-3 record. |
| D-03 (SM-26) | **MD-4** Staged Chapel drainage | Accept | Logically playable: the hint ladder guarantees the order, Running blocks, and the stage never regresses. Wholly dependent on multi-level navigation and runtime walkability swaps (section 4.1). | Kept in the bible MD-4 record. |
| D-04 (SM-28) | **MD-8** Night Count boss refight | Retain, optional, without reversing the story | Playable post-story: it starts only by striking the post at night after MR-M5, and stops on its own after defeat, so the resolved story is not reversed. The gate and separate-instance fixes (A-05) are needed whichever way the road decision goes. No crown keep-watch bench is specified; the player keeps watch at Griefwatch and walks up, which is acceptable. | If declined, Integration MI-EN-10 says "delete the interact". |
| D-05 (SM-29, SS-25) | **Bannerline road** before MR-M5 | Accessible, with story-specific interactions gated | The authored content already treats it this way (MBO W1, MSS spoon, MDS07 path, MDS06 after MR-M5). The main line is unaffected either way: pre-MR-M5 standards are presentation with no Wraiths. Zones Q-3 is still open. | Gate-shut alternative in Zones Q-3. MAP VERIFICATION flags kept. |
| D-06 (SS-23) | **Stillgrave war-washing** | Retain only as explicitly uncertain local folklore | MLL-D3.03 already complied; MLL.1, Area D, Beat 4 and Ebba's `MLL-D3.01` leaned toward fact. They have been hedged to read as uncertain local Tender belief. It is not canon and was not removed. | The removal option already authored as an MLL open decision. |
| D-07 (SS-24) | **Rutting stalker** (MW-03) | Omit unless it has a distinct gameplay purpose | No distinct purpose found: MW-06 already gives post-MRH stalkers, MRH-E2 uses the stalker kit, and the antler toss and dusk patch defence duplicate the Hart. MW-03 is marked "omission recommended, pending Director" and kept. | If omitted, the variant count in bible §10 and Enemies §4.1 becomes 17. |
| D-08 (CO-01, CO-02) | **MI-CO-06** co-op presentation | **Decided by CDR-6 (2026-11-14):** presentation fallback only, governed by CDR-6 | Rewritten as a provisional presentation fallback that never decides navigation, interaction, credit or completion (A-27). Navigation-affecting conflicts are for Sol (section 5). | Integration D-6 open; Q-08 records the superseded wording and how to revert. |
| D-09 (SM-10) | **Route from Sorrowmere to Griefwatch and Rootrest** | None recorded | No package states it (Zones Q-1). Act III says "No channel crossing is required in MR-M5". If the map pass routes Griefwatch through the causeway, X01 and X02 apply to MR-M5's start and end. | Whatever route Q-1 selects must have no crossing that is non-walkable at morning, or MR-M5 `S00` and `S08` need a Slack pin like A-01. MAP VERIFICATION REQUIRED kept; no geography changed. |
| D-10 (SM-19) | **`MRC-L-ROWAN` upgrade window** | None recorded | The window ("until MR-M5 becomes Active") is in practice a few minutes at the landing after MCS, with keep watches between asks, and nothing tells the player it exists. | Act II §A14.5 already offers both: cut `MRC-L-ROWAN` (flag final at MRC completion; the audit's preference, as a simplification) or extend the window. |
| D-11 (SS-02) | **MLD timing** | None recorded | Option (a) applied as the minimal fix (A-13). Still uncovered: an MLD accepted before MR-M5 starts can be Active during the crisis; no text says which presentation wins (same pattern as the MBO/MSS/MBS rule in Act III §11). | **Option (b):** MLD only after MR-M5 Completed, and Act III's read of MLD Completed for Oswin's placement deleted. Recorded in MLD's open decisions. |
| D-12 (SS-19) | **Thin side quests** (MHG, MFW, MBA, MSS, MBS) | None recorded | Five of twenty side quests are strings of talk, inspect and walk with no RuneScape-style verb. | Using existing verbs only: make an existing skill node on their route a required gather or craft step, or trim them and accept them as short lore quests. Director and GD choose. |
| D-13 (CO-16) | **Shared-task credit** (MRC mending and gathering; MMR stakes; MBA spine; MCF count; MSG vents) | **Resolved by CDR-6 (2026-11-14):** credit only when the partner's own active step consumes it; personal rewards and lines from the player's own action. Applied in Int MI-CO-03, II §A11, Clo, Nam. | A partner could receive the "mended it yourself" pole and lines for work they did not do, against Lowmark §8.1. | Bounded option: shared-task credit only for a partner whose own active step consumes it, with reward lines keyed to the player's own action. Shared crewing kept only if approved. |
| D-14 (CO-20) | **Asker beat and junction calls in co-op** | **Resolved by CDR-6 (2026-11-14):** each partner's `MBL_ASKER` and `MRC_WRONG_CALLS` come only from their own action (default `wardens`). Applied in Int MI-CO-05, II §A7, III §7.1.5, Ene §7.1. | One partner's action sets another partner's `MBL_ASKER` ("fallback: host", Act III §7.1.5, Enemies §11.1) and junction calls go to whoever answers first. Presentation only, so Low. | Keep one shared beat, or make it per player (a partner who did not act gets the default `wardens`). |
| D-15 (SS-26) | **MWS marker purpose** | None recorded | Still [PROPOSAL — DIRECTOR]. Not a playability blocker. MHG also remains [PROPOSAL — DIRECTOR]. | As authored. |

### Gameplay Designer items (primary entries in sections 2 and 3)

- **SM-04 (A-04):** C-1 versus 1.2 s displacement tells. Options (a) beat 1 everywhere, (b) stated exception. Pending GD.
- **SM-14 (A-09):** the dusk Wraith re-forms only when a quest next presents its condition. Applied, pending GD confirmation.
- **SM-20 (B-02):** level bands against main-line XP yield.
- **SS-06 (B-06):** entry levels for the MRS and MFH gates, reachable in the Mire.
- **C-1 (1.5 s) and C-2 (25%):** authored tuning requirements pending GD review in every file that states them (TD-16).
- **K-03:** how Shades treat a co-op partner without the hand lantern.

### Carried over from Lowmark and Thornfell (still open; not touched by the Mire)

- **Maelin's knowledge.**
- **The river hands / Lock men.**
- **The knot-per-bearer custom.**

A grep of the Mire files found no reference to any of them, and no fix in this audit touched them. Rowan's knots and the Hayle three-knot charm are unrelated local markers and do not bear on the knot-per-bearer question.

---

## 7. E. Areas that cannot be assessed until a playable Unity build exists

None of the following can be judged from text. They are listed so that nobody reads this audit as evidence about them.

| # | Area | Source ids |
|---|---|---|
| E-01 | Whether the 1.2 s and 0.9 s count, its tells and the step-off window read fairly with click-to-move and the host's 100 ms tick (MBL). | SM-30, TD-22 |
| E-02 | Whether the six-to-eight-minute gap hold with step-offs (MBL `S06`) stays engaging. | SM-30 |
| E-03 | Whether MRC-E2's halt and wade timing really ends the cut, and whether the boat-ride halt rule keeps the fight fair for melee from the bow. | SM-30, TD-22 |
| E-04 | Shade push feel, the draught's difficulty, stage-swap readability (about 15 s transitions), and whether post spacing keeps paths inside lit radii (MCS). | SM-30, TD-22 |
| E-05 | Camera readability of the stacked Chapel and of crown lanes at night. | TD-22 |
| E-06 | Readability of stakes, knots, moss posts and banner states as world markers at game camera distance. | SM-30 |
| E-07 | Cart, boat and side-quest escort pacing (MLW, MFT). | SM-30, SS-28 |
| E-08 | Puzzle readability (MNK, MWS), slack-seam and heron cues (MRS), MSG waves, and Night Count tuning. | SS-28 |
| E-09 | Whether the main-line length targets hold (MNS and MBR 40 to 55 min, MRC 35 to 45, MCS 55 to 70, MBL 60 to 75) and the level curve (B-02). | SM-30 |
| E-10 | Every co-op behaviour: credit, reconnection, host departure, partner persistence, per-viewer presentation. No per-viewer presentation, per-player walkability, partner credit or partner persistence exists to test against. | TD-18, TD-22 |
| E-11 | Performance of four nave environment variants and per-player prop sets. No draw-call or memory budget is established (`UNITY/ARCHITECTURE_PIPELINE.md`). | TD-22 |
| E-12 | Whether C-1 (1.5 s) and C-2 (25%) are the right values at all. They remain authored tuning requirements pending GD. | SS-28 |

---

## 8. Preserved constraints

- **Lowmark terrain conflicts.** TC-01 to TC-19 in `Zones/Caelmor_Lowmark_Terrain_Narrative_Conflict_Register.md` remain recorded and unsolved. This audit did not touch that register. The Mire Zones file's terrain early-check register (§9, MT-01 to MT-18), which names Mire distance and water dependencies on the Lowmark pattern, is unchanged.
- **Mire map verification.** Every MAP VERIFICATION REQUIRED flag is kept. Counted per file before and after the fixes: no file lost a flag, and Zones rose from 39 to 42 because the SM-09 pad sightline and SS-27 ferry notes added flags. Map-dependent findings (A-26 ferry, B-11 Chapel gallery link, D-09 Griefwatch route, K-05 spoon location) were recorded as questions, not solved by moving anything.
- **Materials.** The recent `main` work under `MEDIA/Materials/` (painted-atlas relief within UV islands, height and normals derived from painted maps, shared UVs on mirrored walls, and the documented approved oak shingle, Hewn Oak and lime plaster finishes) was read before this section was written. A grep of the Mire packages found no material, texture, shader, atlas, palette or finish prescription; Zones states its architectural notes name "no material, colour, palette or finish". The stake colour words (pale, ochre, black) are gameplay states in the channel grammar, not art direction. This audit modifies and prescribes no art.

---

## 9. Fix log

Files: **I, II, III** = Act I/II/III quest files; **I-dlg** = Act I dialogue; **Bible**; **Int** = Integration; **Zon** = Zones; **Ene** = Enemies; **Nam, Clo, Wrk, Set** = side-quest files. Every changed file carries a review-log row dated 2026-11-13. Act II and Act III dialogue were not changed. What each fix changed is stated in the Resolution column of sections 2 and 3 and in section 4; this log records status and files only.

**Applied in full**

| Files | IDs |
|---|---|
| I | SM-03, SM-22 |
| I-dlg | SM-15 |
| II | SM-12, SM-18, SM-21, CO-05 |
| III | SM-11, CO-21 |
| Bible | SM-13 |
| Int | SM-16, SM-17, CO-18 (one row, MI-CO-08), TD-19 |
| Zon | SM-02 (proposal table), SS-09 |
| Ene | SS-12 |
| Nam | SS-05, SS-11, SS-23 (hedging only) |
| Wrk | SS-03 |
| Set | SS-14, SS-16, SS-17 |
| Several | SM-01 (I, Int, Zon); SM-08 (I, Int, Zon); SM-23 (III, Ene); SS-01 (Clo, Ene, Int, Zon, Bible); SS-02 option (a) (Nam, Bible, I); SS-04 (Zon, Int); SS-07 (III, Set, Nam, Clo); SS-08 (Set, Int); SS-10 (I, Int); SS-13 two-people line (Set, Clo); SS-15 (Wrk, Set); SS-18 (Clo, Int, Zon); CO-01 (Int, Bible, Zon, Nam, Clo, Wrk); CO-02 (Int, Bible); CO-03 (II, Int, Set); CO-04 (III, Int); CO-06 (II, Int, Ene); CO-12 predicate (III, Int, Ene); CO-14 (I, Nam); CO-17 (III, Int, Ene); TD-05 (II, Int) |

**Applied with a pending label, as a fallback, or in part**

| ID | Status | Files |
|---|---|---|
| SM-04 | Rows marked "C-1 pending GD"; claim corrected; no option chosen | III, Ene, Int, Zon |
| SM-14 | Applied, pending GD confirmation | I, Ene, Int, Zon |
| TD-16 | Labels only; values unchanged | III, Int, Zon, Ene |
| SM-05 | Fallbacks added beside primary design | II, Int |
| SM-06 | Fallback added | II, Int |
| SM-09 | Fallback added (ground pad) | III, Zon, Int |
| SS-06 | Partly: gates are GD placeholders | Wrk, Bible |
| SS-24 | Marked "omission recommended, pending Director"; MW-03 kept | Ene |
| SS-27 | MAP VERIFICATION notes only | Zon, Nam, Clo |
| CO-10 | Partly: "on the host's props" deleted; conflict open (K-04) | I |

**Not applied (owner decides)**

| IDs | Owner |
|---|---|
| SM-07, SM-24, SS-20, SS-21, SS-22, CO-07, CO-08, CO-09, CO-11, CO-13, CO-15, CO-19, TD-01 to TD-04, TD-06 to TD-15, TD-17, TD-18, TD-20, TD-21 | Sol (sections 4 and 5) |
| SM-10, SM-19, SS-19, SS-25, SS-26; SM-25 to SM-29 (status notes) | Director (section 6) |
| SM-20 | Gameplay Designer |
| SM-30, SS-28, TD-22 | Untestable (section 7) |

**CDR-6 solo-completion sweep, 2026-11-14**

Collin's CDR-6 (solo completion; co-op optional) decided D-08, D-13 and D-14 and downgraded every co-op shared-state item to a presentation question for Sol. Text only; no id, step, flag, line or geography changed; Sol's conflicts K-01 to K-10 kept and reframed.

| ID | Status | Files |
|---|---|---|
| CO-16 (D-13) | Applied: credit only from the partner's own active step; MRC personal pole and lines from the player's own work | Int, II, Clo, Nam |
| CO-20 (D-14) | Applied: `MBL_ASKER` and junction calls per player from their own action | Int, II, III, Ene |
| D-08 (MI-CO-06) | Presentation fallback only, governed by CDR-6; package qualifiers restated | Int, Bible, I, II, III, Clo, Nam, Set, Wrk, Zon, Ene |
| Q-18, AT-13, MI-CO-04, MI-CO-08 | Q-18 a presentation question, not a solo prerequisite; AT-13 optional (co-op build only); bosses tuned solo first; leaving never blocks | Int |
| Night Count, extra ferry punt | Night Count stays solo-achievable; the punt for a large party is optional co-op presentation | III, Ene, II |

## 10. Counts

Source findings: 101 ids across four passes (SM 30, SS 28, CO 21, TD 22). After merging duplicates and moving status notes into the decision list, the audit records the following.

| Category | High | Medium | Low | Total | Fixed or fallback added | Open |
|---|---|---|---|---|---|---|
| A. Definite authored-content contradictions | 6 | 12 | 17 | 35 | 33 | 2 (A-04 GD; A-26 map owner) |
| B. Likely gameplay or pacing problems | 0 | 5 | 6 | 11 | 8, plus B-06 partly | 3 (B-02 GD, B-06 GD numbers, B-11 zone pass) |
| C. Technical dependencies for Sol (section 4) | 5 | 12 | 6 | 23 | Text or fallback on 6 (SM-05, SM-06, SM-08, SM-09, TD-05, TD-16) | All capabilities open for Sol |
| C. Co-op shared-state conflicts for Sol (section 5, K-01 to K-10) | 7 | 3 | 0 | 10 | Host authority removed from text in all ten | All ten open for Sol as presentation questions; none blocks solo completion (CDR-6) |
| D. Director-level decisions | 0 | 5 | 10 | 15 | 3 decided by CDR-6 (D-08, D-13, D-14) | 12, plus GD items and 3 carried-over Lowmark/Thornfell questions |
| E. Untestable until a playable build | — | — | — | 12 areas | — | 12 |

High-severity items still open after this audit are all technical or co-op dependencies for Sol: the Chapel's multi-level navigation, per-player walkability, escort and ride, mobile enemies, keep watch and the presentation hour, and the seven High co-op conflicts, which under CDR-6 affect co-op presentation only and do not block solo completion. No High authored-content contradiction remains open.
