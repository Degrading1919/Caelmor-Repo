# Caelmor Narrative Architecture

**Status (updated 2026-11-02 after Creative Director rulings):** The Creative Director approved the direction of this package and ruled on FT-01 to FT-05 and D-C03, D-C06, D-CV1, D-R1 and the convergence-location concept (Review §5.0). It is now the **controlling plan for narrative work after Lowmark v1**, and the quest contribution contract (Review §7.1) is mandatory. Approved foundational truths have been promoted into `LORE/` by a controlled canon pass (Review §5.3); everything not named in a ruling remains a proposal. It sets the major history, faction motives, linked arcs, pivotal quests, revelations, and payoffs that later quests build toward. It does not replace the Lowmark v1 package, changes `LORE/` only through the logged canon pass in Review §5.3, does not commit future regions to production or release, and creates no schemas, JSON, or C#. Foundational truths FT-01 to FT-05 are now ruled (Review §5.0); the precise magical mechanics of FT-05 remain subject to a later consistency review.

**Authority used:** Phase 1.1–1.5; `00_ADMIN/Reference/Caelmor_Master_Assistant_Protocol.md` §5.4–5.6; the reconciled `LORE/` Timeline, War History, Factions, regional dossiers, merged overview, and character anchors; the Part 2–6 proposals, ledgers, decision sheet, reconciliation audit, and lore lock review in `00_ADMIN/Reference/`; `Caelmor_Lowmark_v1_Narrative_Production_Bible.md` and its packages; `00_ADMIN/Roadmaps/Caelmor_Roadmap.md`; the File Manifest.

---

## 1. Package map

| File | Deliverable |
|---|---|
| **This file** | Index, canon baseline, the two perspectives, the three orders, RuneScape principles adopted. |
| `Caelmor_Narrative_Architecture_Factions_and_World_Truth.md` | 1. Faction histories, relationships, long-term motivations. 2. Consolidated historical-event and world-truth framework. |
| `Caelmor_Narrative_Architecture_Arcs_and_Milestones.md` | 3. Regional and cross-regional arcs through the envisioned endgame. 4. Milestone quests and the dependency graph. |
| `Caelmor_Narrative_Architecture_Revelation_Ledger.md` | 5. Revelations and foreshadowing: how each discovery is earned. |
| `Caelmor_Narrative_Architecture_Review_and_Authoring_Sequence.md` | 6. Consistency review and Director decisions. 7. Recommended authoring sequence and the quest contribution contract. |
| `00_ADMIN/Reference/Caelmor_RuneScape_Quest_Architecture_Study.md` | Comparative structural research (supporting). |

All five architecture files sit beside the Lowmark bible in `04_CONTENT_PRODUCTION/Quests/`, the Manifest folder for quest design. The study sits with the other deep-research references.

---

## 2. The backbone in one page

**The central question.** Thirty years after a war nobody ended, can Caelmor's four regions make the peace they never made, before the same pressures start the next war?

**Historical truth.** Before the Great War, the regions depended on one another without any shared way to inspect dangerous practice or accept one another's witness; the custom that tried, the Crossing Concord, failed (FT-01). The war wore out without a treaty: exhaustion did most of the work, and inside that collapse each region made one withdrawal, at a different time and for its own reasons, and hid its cost behind a proud story (FT-02). Lowmark fed every side and its crews refused to run after a convoy was drowned; Thornfell's horns killed its own and its sealing stranded refugees; the Mire's last Memorywardens broke themselves to ground the battlefield and left the General behind; Emberholt's war ended in the Glassed Hollow, hidden as a forge collapse. Today hoarding, closures, drills, and a patient hidden faction are reproducing the road to war.

**Player discovery.** The player arrives as an ordinary wanderer and saves Lowmark's water (v1, complete). In each later region they solve a present local crisis and, while doing so, discover that region's hidden cost of the war and earn one civic tool: many hands (Lowmark), an honest closure (Thornfell), testimony that holds (the Mire), accountable power (Emberholt). With standing in all four, the player assembles the four stops, holds the Second Road, brings four regions to one table at an old Concord crossing, and breaks the Remnant's Perfect Flame beneath Emberholt, where they must bind the Fire Titan, a person the war made, to rest rather than kill it. The Long Horizon follows: keeping the peace, and deep places that explain much and never the Forgotten God.

**Not one conspiracy.** Every regional crisis has its own human cause. The Remnant is central only in Emberholt and in the convergence, where its operations are specific and bounded. What links the regions is a shared wound, not a shared villain.

---

## 3. Canon baseline (task 1)

### 3.1 Established and usable now

| Area | Established | Source |
|---|---|---|
| Chronology | Mythic Age, withdrawal, rediscovery, Road to War, a 5–10-year Great War ending about thirty years ago, postwar restraint, thirty years of recovery. | Timeline; War History; D01 |
| Magic | Four traditions; spirit is not an element; postwar regional restrictions with no universal ban; Lowmark's layered farm practice; combat water practice only with the Last Field-Mage; no v1 player spellcasting. | Timeline; Factions; D02, C09 |
| Supernatural limits | Stonebound passive; Dreamers postwar; two major non-undead Mire threats; one Mire chapel with three names; no phenomenon is a witness. | C08, C11, C14, C15 |
| Glassed Hollow core | Precursor abuse of Volkhari; initiate Titan; Kaelith free; Thalan sole captive; "forge collapse" false. | Factions; Emberholt dossier |
| Regions | Each region's civic obligation and ordinary life; cross-region ties for every pair; two-custodian rule. | D03, D04 |
| Lowmark v1 | A complete main arc, side slate, encounters, POIs, and integration handoff, with open director decisions in bible §3. | Lowmark package |
| Controls | Author truth, public belief, evidence, wrong reading, reveal owner; character ledger limits; map audit; three-layer discovery. | D06; Part 4–5 |

### 3.2 Unresolved, and kept unresolved

C03 precursor name, transition and survivor identities (limited continuity approved), C06 Volkhari population (kept unnumbered), C07 Founder roster, the Forgotten God, the Echohewn disappearance, the origin of "Sinking Star", map geometry, and constitutional powers. The architecture uses neutral wording for each and names the milestone, if any, that will need a ruling (World Truth §B.2).

### 3.3 Threads that can carry long-term questlines

| Thread | Existing basis | Used as |
|---|---|---|
| How the war ended | "No single explanation" (War History §VI); Part 2 "Cessation without settlement". | The convergence question (FT-02). |
| The inspection gap | Timeline §IV; Part 4 event 5. | The Crossing Concord (FT-01). |
| Lowmark's stolen grain and the Fourteenth Lot | v1 bill ("the Whinstone Store"); Bramblelock stones; Fenmere ledgers. | Thornfell entry (FT-03); Lowmark return. |
| Thornfell's forced resonance | Shatterfall scar; Ressa's forbidden calls; Brynjar's boast. | Thornfell arc. |
| Memorywardens' downfall | Mire dossier §IV; Sennic's memories; chapel relic rumor. | Mire arc (FT-02c). |
| Glassed Hollow and Volkhari | Directed core. | Emberholt arc. |
| One person in several records | Part 4 braids 4, 8, 12; Part 5 Thread 2. | Register of the Unreturned series. |
| Remnant's Perfect Flame | Emberholt dossier §IX–X. | Convergence climax (FT-04). |
| The Fire Titan and its degrading bindings | Factions §13, §18; Emberholt anchors (Varos Keln, Meryndis, Dahrin, Thalan). | Convergence climax (FT-05). |

---

## 4. Comparative principles from RuneScape (task 2)

The study verified that the public `parsed-osrs` extraction holds quest requirement strings, series labels, rewards, and walkthroughs, but flattens requirement depth and holds **no** narrative graph: no character, faction, location, event, or revelation links. The Creative Director's local copy was not reachable from this session; the limitation is recorded in the study. Caelmor's narrative graph is therefore authored natively in this package.

| RuneScape pattern (structural) | Caelmor decision |
|---|---|
| Low-requirement entry quest per region; many standalone quests. | **Adopted.** No region's entry milestone has a quest prerequisite; the only mid-arc cross-region gate is EH-M3 (TF-M3 or MR-M2); at least half of each side slate is self-contained. |
| Keystone quests that many later quests reuse. | **Adopted.** Each regional entry milestone teaches its readable system and is reused by later content. |
| Series membership separate from thematic "related" links. | **Adopted** as typed edges (arcs §6.1). |
| Deep spines for series finales; wide convergence for grandmaster capstones. | **Adapted.** Regional spines stay inside their region; the one convergence gate has three direct parents (Lowmark return, Mire capstone, Emberholt capstone) covering all four regions, and no side-quest or point requirements. |
| Quest-point totals, flat 30-plus requirement lists, broad skill walls. | **Rejected.** Standing flags name specific regions; skill gates only on optional content. |
| Story progress unlocks access and repeatable encounters. | **Adopted.** Routes, regions, and post-story climax sites. |
| Diary-style regional completion layers. | **Adapted** as a proposed regional deeds layer (Gameplay Designer). |
| Recurring mentor characters travelling across regions. | **Adapted.** Recurrence travels through records, trade, and route workers, and the player; anchors do not gain travel the character ledger forbids. |
| Completion badges revoked when new quests ship; autocompleted story content; placeholder finales; hidden partial gates. | **Rejected.** Badges are per region; no autocomplete; each regional arc is planned to completion before release; every gate is a visible milestone. |
| Fail states and abandonment. | **Rejected** by the three-state rule. |

---

## 5. The three orders (kept separate)

### 5.1 Historical chronology

Mythic Age → Quiet Withdrawal → Rediscovery (Riverwardens, Echohewn, Memorywardens, Emberholt fire, Volkhari inheritance) → Road to War (the Crossing Concord fails) → Great War (Lowmark breadbasket and Relief Cut; Thornfell forced horns; Mire battlefield; Emberholt weaponization) → late war (the Fourteenth Lot) → final year (four stops: crews' refusal, Thornfell sealing, Memorywarden grounding, Glassed Hollow) → the Stopping (no treaty) → postwar restraint, Dreamers, formal Remnant → thirty years of recovery → present (Lowmark's water; the Second Road). Full table: World Truth §B.1.

### 5.2 Player quest order (one plausible path; any regional order is allowed; Lowmark is the starting region, and EH-M3 asking for TF-M3 or MR-M2)

Lowmark v1 (12 main quests) → Thornfell (5) → Lowmark return (1; optional for regional play, required before the convergence) → Mire (5) → Emberholt (6) → convergence (4) → Long Horizon. Optional series run alongside. Players meet history out of chronological order by design: they learn the war's end (each region's stop) before they learn the prewar Concord, and Lowmark's own wartime shame last among the regions.

### 5.3 Future production and release (only Lowmark is approved for release)

v1 Lowmark → v1.5 Thornfell (the Phase 1.3 direction) → Mire → Emberholt (D-R1 ruled: preferred **production** order, not a player order or release schedule) → Lowmark return as an update alongside Thornfell or later → convergence once all four regions exist → Long Horizon. Only Lowmark is approved for release; Phase 1.3 names Thornfell as the v1.5 direction.

---

## 6. Using this package

- **Before writing any future quest:** check the World Truth rows it touches, the revelation it plants or owns (or declare it self-contained), the character ledger, and the quest contribution contract (Review §7.1). The contract is mandatory for Thornfell and later regional content (the Director directed production "using the approved narrative architecture", 2026-11-02).
- **Before starting a regional bible:** check the FT rulings it depends on (Review §5.0) and follow the authoring order (Review §7). The Thornfell bible is the first regional bible under this plan (`Caelmor_Thornfell_Narrative_Production_Bible.md`, in production).
- **When the Director rules:** record the ruling in Review §5.0 and project memory; then run a controlled canon pass (Review §5.3 is the first) to promote only what was approved into `LORE/`.
