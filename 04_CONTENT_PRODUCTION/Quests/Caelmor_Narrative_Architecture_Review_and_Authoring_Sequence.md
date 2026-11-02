# Caelmor Narrative Architecture — Consistency Review, Director Decisions, and Authoring Sequence

**Status:** Proposal package for Creative Director milestone review (2026-11-02). Part of the package indexed in `Caelmor_Narrative_Architecture.md`. This file covers **deliverable 6** (consistency review: contradictions, missing causal links, excessive dependencies, gameplay opportunities) and **deliverable 7** (recommended sequence for later detailed quest authoring). §5 consolidates every decision reserved for the Creative Director. §6 records the independent review.

---

## 1. Scope of the review

Reviewed against the package: Phase 1.1–1.5; the reconciled `LORE/` Timeline, War History, Factions, four regional dossiers, merged overview, and character anchors; the Part 2–6 proposals and ledgers, the Director decision sheet, the canon reconciliation audit, and the final lore lock review in `00_ADMIN/Reference/`; the complete Lowmark v1 package; Stage 15/27 quest runtime documents and `CODE/Systems/QuestRuntimeSystem.cs`; and the RuneScape structural study.

---

## 2. Contradictions found in existing sources

None of these were silently fixed. Each has a recommendation.

| # | Contradiction | Sources | Effect on narrative | Recommendation | Owner |
|---|---|---|---|---|---|
| 1 | **Quest failure states.** The Creative Director's rule is three states (Inactive, Active, Completed). Stage 27 and `QuestRuntimeSystem.cs` define `Failed`; Stage 15.2 defines `Uninitialized` and terminal `Abandoned`. | Director instruction (this mission); Stage 15.2, Stage 27; `QuestRuntimeSystem.cs`; `Caelmor_Lowmark_v1_Integration_Requirements.md` §1.1, G04, I-13, D-INT-7, and the re-offer section (which plans to adopt 15.2's `Abandoned` and states "All Lowmark quests may be abandoned") | No authored quest can fail, but the Lowmark integration handoff currently recommends the opposite of the Director's rule. | Retire `Failed` and `Abandoned` from the narrative contract; revise G04, I-13, D-INT-7 and the re-offer rule so a dropped quest simply stays Active (or returns to Inactive before any step is taken, if the Director prefers); Systems Engineer change with Director sign-off before Stage 24.1 runtime work. | Director → Systems Engineer |
| 2 | **The Flameward Speaker's knowledge.** The Emberholt dossier makes him secretly aligned with personal ambition and hidden beliefs. Factions §5 says several Council members act under Hearthveil dream influence, and §VII.A calls him a "compliant Remnant instrument". | `Caelmor_Region4_EmberholtHeights.md` §IV, §XVII; `Caelmor_Factions.md` §5, §VII.A | Decides whether EH-M5 exposes a villain or a victim. | He is a **knowing** ally for his own ambition **and** dream-seeded: his anchor says he receives Hearthveil visions "sincerely believing them divine" and believes he guides a renaissance. The wrong readings are "wholly puppet" and "wholly mastermind". "Compliant" describes his relationship to the Ashfall Authority. Some councillors are dream-influenced. The character ledger's limit stands: he lacks the Ashfall endgame. | Director (light ruling) |
| 3 | **"Invading forces" from the east.** Thornfell is "the eastern barrier against invading forces"; the Mire "buffered Lowmark and Thornfell from eastern incursions". The war was among Caelmor's four regions; no fifth power exists in canon. | Thornfell dossier §II; Mire dossier §II; Timeline §V | Players could infer an outside invader. | Do not pick an invasion vector here (Part 4 map audit: it "cannot silently pick one"); add no fifth power and give the precursor no military command while C03 is open. Resolve in the map and canon pass. | Director (canon pass) |
| 4 | **Thornfell institution names.** Factions has "Cliffward Sentinels"; the dossier has "Ridge Wardens". The Assembly appears as Stonewake Assembly, March-Assembly Hall, and Thornfell Assembly. The merged overview lists Highridge Hold and Redbanner Camp, absent from the dossier (which lists Stonewake and Highsteads). | Factions §16; Thornfell dossier §III, §VI; merged overview §II | Naming drift when Thornfell production starts. | Treat Cliffward Sentinels as a ridge-patrol corps within the Ridge Wardens; use "Stonewake Assembly" for the body and "Assembly Hall at Stonewake" for the place; treat Highridge Hold and Redbanner Camp as unplaced names until the map pass. | Thornfell bible |
| 5 | **Mire place names.** The merged overview lists Reedsward; the dossier's settlements are Sorrowmere, Marshfall, Griefwatch, Rootrest. | Merged overview §III; Mire dossier §VII | Minor. | Treat Reedsward as an unplaced name until the map pass. | Mire bible |
| 6 | **Character-creation origins.** Each dossier has "starting faction flavor" for characters originating there; the v1 recommendation (D-3) is an origin-neutral wanderer. | Regional dossiers §XII/§XIII; bible §3 D-3 | Affects how future regions greet a player. | Keep the origin-neutral wanderer (the architecture assumes it). If origins are added later, each regional arc gets one optional line per origin, never a branch. | Director (already open as D-3) |
| 7 | **"End their suffering."** The Emberholt dossier's *Ash-Stained Chains* offers to free, aid, or end the suffering of the captive Volkhari. | Emberholt dossier §XIX.3 | Killing Thalan would reduce a Volkhari person to a plot outcome and close Volkhari threads. | Offer free or aid-in-place only (decision D-E2). | Director |
| 8 | **Perfect Flame as spectacle.** The dossier's capstone uncovers "ritual plans for a city-wide ignition" and the Remnant's goal of a "Fire Titan–class vessel". | Emberholt dossier §IX, §XIX.5 | Risk of high-fantasy spectacle. | Ground it (FT-04): a transmissible-mastery attempt that depends on a conditioned crowd, whose failure mode is a second Glassed Hollow under a district. Move its climax to the convergence. | Director (FT-04) |
| 9 | **Part 2 spine and the "Stopping".** Part 2 places Shatterfall in Year 2 and uses "the Stopping" for the first three postwar years. | `Caelmor_Part2_War_and_Postwar_Proposal.md` | FT-02 uses "the Stopping" for the end of the war and puts Thornfell's stop in the final year. | FT-02b is written to fit either a Year-2 Shatterfall or no spine. "The Stopping" names the cessation season and the first postwar years together. Both remain optional proposals. | Director (with FT-02) |
| 10 | **"Kaldren Stone-Echo".** A stale name in the Part 3 cross-region custodians table. | `Caelmor_Part3_Cross_Region_Continuity_Proposal.md` | Minor. | Use Kaldren Deepdelver everywhere. | Next canon pass |

---

## 3. Missing causal links (and how the package closes them)

| Gap in existing canon | Why it matters | Closure | Status |
|---|---|---|---|
| **How the war ended.** Canon says no clean victory and no explanation every region accepts, but not what stopped it. | Without it, the peace has no shape and the endgame has no question. | It wore out; inside that, four uncoordinated withdrawals at different times, some feeding others; no treaty (FT-02). | Approved (§5.0) |
| **Why prewar interdependence failed.** Canon describes the inspection problem but no institution. | Gives the endgame something to remake. | The Crossing Concord (FT-01). | Approved (§5.0) |
| **Who bought Lowmark's stolen grain.** v1 leaves a placeholder for "the cross-region pass". | The first cross-region thread. | A Thornfell Blood-Oath splinter's unsanctioned reserve (FT-03). | Approved (§5.0) |
| **Why the Remnant has waited thirty years.** | Prevents an idle-villain problem. | It needs a conditioned generation, its Titan template is bound and unstable, and Thalan's research is slow (C.1). | Proposal |
| **Why the Fire Titan has not destroyed anything since.** | Canon says Deepbrand fears its re-emergence. | Canon already answers it: Remnant bindings hold it, and they are degrading. The Remnant keeps it bound because it is the template it studies (FT-05). | Canon plus proposal |
| **Why a wanderer is trusted across four regions.** | Avoids a chosen-one premise. | Earned standing per region; the convergence requires all four, because only someone who has seen each region's hidden cost can carry it to the others. | Proposal |
| **Why the player leaves Lowmark.** | Organic travel motive. | Being sent with a caravan once trusted; optional pursuit of the bill's buyer. | Proposal |
| **What the Riverwardens do after v1.** | They should not vanish or rule. | They teach Braid tending to many hands; Long Horizon. | Proposal |
| **Why Thornfell and Emberholt tension is rising now.** | Canon gives the history but not the trigger. | Mutual misreading: Emberholt's dense-city food stockpiles and drills, Thornfell's splinter stores and horn, and rumors Durell seeds in both (FT-04 for Durell's role). | Proposal + FT-04 |

---

## 4. Dependency, scope, and gameplay review

### 4.1 Excessive dependencies

| Risk | Finding | Mitigation adopted |
|---|---|---|
| Convergence breadth | Four regional standings are required (3 direct parents: LR-M1, MR-M5, EH-M6; 29 transitive milestones, all regional main arcs plus LR-M1). This is the single breadth gate. | No side quest or optional series is ever required; regional order is free and no region's entry needs another region; each region's spine stays inside its region (RuneScape study: deep spines plus bounded convergence, rejecting quest-point walls and flat 30-plus lists). |
| Emberholt Hollow gate | EH-M3 asks for TF-M3 or MR-M2 (two or three quests elsewhere). | Either satisfies it; EH-M1–M2 are open to any player, so release order stays flexible. |
| Hidden gates | None. Every prerequisite is a visible milestone in the three-state model (study: no hidden partial-progress gates). | — |
| Skill walls | None on main milestones. | Hard skill gates only on optional shortcuts, master commissions, and Long Horizon content. |
| Lowmark return | Requires Thornfell; required before the convergence because it owns Lowmark's stop. | Lowmark v1 remains complete without it; it is optional for all regional play. |

### 4.2 Canon and tone risks

| Risk | Guardrail |
|---|---|
| Conspiracy creep (everything becomes the Remnant). | Faction C.1 bounded-reach clause; rule 4 in arcs §1.3; R15 recontextualizes the Remnant as feeding existing fears. |
| Spectacle creep in the endgame. | Arcs §5.2 "must never become" rule; FT-04 grounding; the decisive acts are refusal, testimony, shared work, and a binding rather than a kill. |
| Anchor biography creep. | All shared-character edges must pass the Part 4 character ledger; Brynjar is not made the splinter's leader; Maelin is not made a refusing crew member; Kaldren is not made the log's author. |
| Supernatural witnesses. | Rule B.3.4; every revelation has two human or material custodians. |
| Lowmark resolution undermined. | The return arc adds Lowmark's wartime responsibility; it does not reverse v1's present-day truths (Part 5 Thread 1 owner rule). |
| Magic power fantasy. | No milestone requires player spellcasting; any future system sits under the Concord's witness rules. |

### 4.3 Opportunities for more memorable gameplay

1. **One readable system per region.** Lowmark reads water and marker stones; Thornfell reads sound (horn codes, echo timing, null-points); the Mire reads shifting ground and channel states; Emberholt reads heat. Each is learned knowledge (Pillar A), and the convergence asks the player to use all four in one descent.
2. **Distinct climaxes.** The evidence-chip hearing is the climax only once, in Lowmark MQ10. Every later capstone is physical and dangerous: holding a closing pass in a blizzard (TF-M5), facing the General on Bannerline (MR-M5), a diving descent to the drowned convoy (LR-M1), a descent through a failing heat main (EH-M6), rebuilding an old Concord crossing in storm (CV-M3), and the Last Binding (CV-M4). Only TF-M5 and CV-M4 have a human trigger; EH-M6's cause is systemic and CV-M3's is weather. Evidence chips shape only short aftermath scenes.
3. **Post-story access.** Each capstone turns its climax site into revisitable content (study principle 13): Shatterfall in storms, Bannerline at night, the Emberdeep after EH-M6.
4. **Regional deeds layer.** A per-region, non-failing completion lattice (quests, places, encounters) that pays out traversal or utility, following the diary pattern in the study. Gameplay Designer proposal; no schema assumed.
5. **The Sorrowback as the world's alarm.** A large, readable earth-memory encounter that rises when the regions mobilize and recedes when the player calms the Second Road; its presence is a visible world-state signal.
6. **The four tools as party-free co-op texture.** In co-op, partners with different regional standings read different systems at the Mirebone crossing and in the Last Binding, without syncing progression (Pillar D).

---

## 5. Decisions reserved for the Creative Director

### 5.0 Creative Director rulings (2026-11-02)

The Creative Director (Collin) reviewed the refined architecture and ruled as follows. These rulings supersede the recommendation columns in §5.1 and §5.2 wherever they differ. Items not listed here remain open on their recommendation.

| Id | Ruling | What it settles | What stays open |
|---|---|---|---|
| **FT-01** | **Approved.** The Crossing Concord was an informal prewar custom of mutual witness, not a centralized government. | It existed; it was custom (access, testimony, the shame of refusal), with no army, court, seat, or ruler; it failed on the Road to War. | Which regional refusal came first; the exact form of each region's surviving custom. Each region's part in the failure (H08) stays a proposal until its arc is authored. |
| **FT-02** | **Approved.** The Great War ended through exhaustion, hunger, desertion, local truces, and staggered regional withdrawals. Preserve the revised regional accounts (02a–02d), the relative chronology, and the prolonged cessation. | No treaty; the four withdrawals happened at different times, Thornfell's sealing earliest and slowest, Lowmark's crews' refusal over a season or more after the Fourteenth Lot, Emberholt's Glassed Hollow sudden in the final year, the Mire's grounding of the last great battle; raids continued for a time after ("the Stopping"). | Year numbers; casualty counts; who blew the Shatterfall horn; who gave the Fourteenth Lot order (owned by LR-M1). The optional Part 2 campaign spine stays optional. |
| **FT-03** | **Approved.** The buyer of Lowmark's stolen grain was a Thornfell Blood-Oath splinter acting independently. Do not invent unverified trade routes. | The bill's account is a Thornfell store-house used by a splinter acting without its clans or the Assembly. The v1 placeholder is now filled with a neutral account name, the **Whinstone Store**, that does not name a region in v1. | The route the grain took (river, road, or transfer) stays open until the map pass. Who in the splinter authorized purchase beyond the factor stays withheld (R05). |
| **FT-04** | **Approved.** Perfect Flame is the Remnant's attempt to make advanced embercraft reproducible through conditioning and controlled knowledge. Its influence beyond Emberholt must remain specific and bounded. | The definition; that it depends on a conditioned population and restricted knowledge; that outside Emberholt the Remnant only exploits, never causes, other regions' crises. | Each specific outside operation (Durell's informants, seeded rumors) must be authored as a discrete, discoverable act and reviewed; none is canon until authored. |
| **FT-05** | **Narrative direction approved.** The Fire Titan is a suffering transformed initiate. The Last Binding is an earned, dangerous confrontation ending in containment rather than a conventional kill. | The Titan is a person the war made, not a monster to slay; the convergence climax ends in a binding, not a kill. | The precise magical mechanics (how the bindings degrade, what a rest-binding is made of, the quench cisterns, the spoken name) remain **subject to later consistency review**. No Stonebound role. |
| **D-C03** | Adopt **limited personnel continuity** between the wartime precursor and the formal Remnant. Do not invent an approved precursor name or an extensive surviving leadership roster. | Some individuals of the precursor survived and helped form the formal Remnant (recommendation (a), narrowed). | The precursor's name; the transition date; who the surviving individuals were. Selvara stays bounded by her ledger row. Any named survivor needs a separate ruling. |
| **D-C06** | Keep the Volkhari population **unnumbered** and their surviving communities **unresolved**. | Content depicts individuals only. | Population, community form, location. |
| **D-CV1** | The Titan is **bound to rest**. Whether eventual release is possible remains an **open late-game question**. | The CV-M4 outcome is a rest-binding. | The Long Horizon release option is neither approved nor ruled out. |
| **D-R1** | **Prefer Thornfell → Mire → Emberholt** as the future **production** order. | Authoring order for regional bibles. | It is not a mandatory player progression order and not an approved release schedule. Only Lowmark is approved for release. |
| **Convergence location** | **Approve the concept** of rebuilding a historically significant crossing. Keep **Mirebone Crossing's suitability provisional** until geographic verification. | CV-M3 is a crossing rebuild at an old Concord crossing. | Which crossing. "Mirebone" stays a provisional working name in all documents. |
| **D-Q1** | **Quest lifecycle: Inactive, Active, Completed only.** The Systems Engineer has already published the contract reconciliation (commit a1c71ea). | Closed. | — |

Still open and unchanged by these rulings: D-E2 (Thalan's fates), D-S1 (the Speaker), contradictions 3 (eastern "invaders"), 4–5 (place-name drift, now handled by each regional bible), 6 (origins), 10 (stale name), D-L1 (all Lowmark bible §3 decisions, including D-11 canon promotion of v1 [NEW] material), and C07.

Each decision below had a recommendation. The tables are kept as the record of what was proposed.

### 5.1 Foundational truths

| Id | Decision | Recommendation | Alternatives | If replaced | Blocks |
|---|---|---|---|---|---|
| **FT-01** | Adopt the **Crossing Concord**, a prewar custom of mutual witness at crossings and passes that failed on the Road to War. | Approve. | No named institution (the endgame then creates something wholly new); a formal treaty body (more governmental, less grounded). | CV-M1 and CV-M3 framing; R16 seeds. | Convergence outline |
| **FT-02** | Adopt **a war that wore out, with four hidden withdrawals and no treaty**. Exhaustion, hunger, desertion, and local truces did most of the work over the last years; inside that collapse each region made one uncoordinated withdrawal at a different time, for its own reasons, some feeding others: 02b Thornfell's slow sealing of the passes (earliest), 02a Lowmark crews' spreading refusal after the Fourteenth Lot, 02d the Glassed Hollow as Emberholt's sudden collapse, 02c the Memorywardens' grounding of the last great battle (forming the General). Raids continued for a time after (Part 2's "the Stopping"). | Approve the frame; approve 02a–02d individually, and the relative order. | Keep the frame but change the order or a regional withdrawal; keep "no single explanation" without specifying. | Each region's capstone revelation; R06, R08, R09, R13, R17. | Each regional bible (its own sub-truth); convergence |
| **FT-03** | The **outside buyer** on the Lowmark bill is a Thornfell store-house supplying a Blood-Oath splinter's unsanctioned war reserve. | Approve; fill the v1 placeholder with a neutral store-house name once approved. | An Emberholt merchant house (risks the "Emberholt is always the villain" read the Part 3 caution warns against); a rival Lowmark house (keeps it local). | TF-M2 hook; v1 bill name only. | Thornfell bible |
| **FT-04** | **Perfect Flame** defined as transmissible mastery depending on a conditioned crowd, with Durell's interregional operations bounded and discoverable. | Approve. | The dossier's city-wide ignition (spectacle risk). | EH-M5, CV-M2, CV-M4. | Emberholt bible; convergence |
| **FT-05** | The **Fire Titan** is the transformed precursor initiate: a person still suffering inside a fire that cannot go out [Thalan's canon sense of suffering], held beneath Emberholt by Remnant bindings that are degrading [CANON]. It cannot be killed by force without spreading its fire, or freed without burning the city. In CV-M4 the Remnant's draw breaks the old bindings; the player earns a new **rest-binding**, made by Emberholt fire wardens and individual consenting Volkhari from pieces the player gathers as testimony and objects, that holds the Titan without using it. A dangerous multi-phase encounter, but no kill. The Stonebound play no part (the earlier C11 expansion is withdrawn). | Approve. | A conventional boss kill (loses the tragedy; contradicts the spreading-fire lesson); the Titan freed (city burns); containment by the deep works (withdrawn: it stretched C11 and made the ending passive). | CV-M4; R19. | Convergence |

### 5.2 Other decisions

| Id | Decision | Recommendation | Blocks |
|---|---|---|---|
| **D-C03** | Precursor name and continuity (canon C03). | Options: (a) partial continuity, a wartime fire-research cadre whose few survivors helped found the formal Remnant; (b) no personnel continuity, the formal Remnant inherited only records; (c) continuity of records and one patron family. Selvara stays bounded by her ledger row (sheltered during the war; no war role) in every option. Recommendation (a), name chosen in the Emberholt bible. | EH-M3 outline |
| **D-C06** | Volkhari population (canon C06). | Keep unnumbered; depict individuals only. | Nothing; recommended before EH-M4 |
| **D-E2** | Thalan's possible fates in EH-M4. | Free, or aid in place; no option to end his life. | EH-M4 |
| **D-CV1** | The Titan after CV-M4. | Bound to rest, still a person lost rather than a monster slain; the player chooses whether its name is restored to the public record. Option for the Long Horizon: a slow, tended release over years until the fire is spent and the initiate can die, kept by Emberholt wardens, with any Volkhari involvement limited to consenting individuals (C06 stays open). | CV-M4; Long Horizon |
| **D-R1** | Release order after Thornfell. | Mire before Emberholt: the Mire teaches testimony before Emberholt tests it, and Glassed Hollow's displaced civilians reach Mire care first. Either order works structurally. | Production planning |
| **D-Q1** | Retire `Failed`/`Abandoned` from the quest contract (contradiction 1), which also reverses the Lowmark integration handoff's D-INT-7 recommendation. | Approve and hand to the Systems Engineer before Stage 24.1. | Quest runtime |
| **D-S1** | Speaker's knowledge (contradiction 2). | Knowing ally who is also dream-seeded. | EH-M5 |
| **D-L1** | Existing Lowmark open decisions (bible §3: antagonist, Field-Mage, Riverwarden contact, backwater, yield state, and the rest). | Unchanged; the architecture assumes the current recommendations but does not depend on any of them except that the bill has a buyer and the Fourteenth Lot exists. | — |
| **D-P1** | Canon promotion. | Promote nothing from this package until the FT rulings; then promote approved FTs into `LORE/` in a separate canon pass. | — |

---

### 5.3 Controlled canon-promotion pass (2026-11-02)

Rule applied: promote only what a ruling explicitly approves; keep everything else as proposal; reconcile references without overwriting unrelated canon. Each promoted passage in `LORE/` is marked with its ruling id so it can be traced.

| File | Change | Ruling |
|---|---|---|
| `LORE/Timeline/Caelmor_Timeline.md` | §IV: the Crossing Concord as an informal custom that failed. §IV, §VI: limited precursor continuity, name still unresolved. §V: how the war wore out, the four staggered withdrawals in relative order, the prolonged cessation, and a note that regional "armistice" speech names the cessation, not an agreement. §VIII: the present Blood-Oath splinter as buyer of Lowmark's stolen grain. | FT-01, FT-02, FT-03, D-C03 |
| `LORE/Worldbuilding Docs/Caelmor_War_History.md` | §III: the Concord. §V: the Glassed Hollow as Emberholt's war-ending gamble. §VI: the shape of the end, keeping the existing "no single explanation every region accepted" as public truth. §IX: limited continuity. | FT-01, FT-02, D-C03 |
| `LORE/Factions/Caelmor_Factions.md` | Remnant origin line (limited continuity); Ashfall long-term goal (Perfect Flame defined, bounded reach); §13 Fire Titan (suffering initiate; containment, not a kill; mechanics open; release open); §16 Thornfell (the splinter); §VIII Canon Alignment summary (D-C03, FT-04). |
| `LORE/Worldbuilding Docs/Caelmor_War_History.md` §III, `LORE/Regions/Caelmor_Region_Merged.md`, `Caelmor_Region4_EmberholtHeights.md`, `LORE/Characters/Caelmor_Characters_Region4_Emberholt.txt` (Selvara) | "Personnel continuity unresolved" lines reconciled to limited continuity; Selvara's existing canon role is unchanged. | D-C03 | D-C03, FT-04, FT-05, D-CV1, FT-03 |
| `LORE/Regions/Caelmor_Region2_ThornfellMarches.md` | §IV: the independent Blood-Oath splinter beside the existing Blood-Oath/Hearthguard tension. | FT-03 |
| Architecture package | Status lines; World Truth Part A stale "in its final year each region stopped" sentence corrected to the approved staggered account; H07, H09, H15–H19, H25 and C.1 relabelled **[APPROVED]**; Mirebone marked provisional in Arcs §5.2; index and §7 step 0–1 marked done. | All |
| Lowmark v1 | `NF_bill_of_lading` placeholder filled with "the Whinstone Store" (Act I dialogue; Act I and Act III open-decision rows updated). No other v1 change. | FT-03 |

**Not promoted (kept as proposals):** each region's specific part in the Concord's failure (H08), the Riverwarden-withdrawal interpretation of Oriel's line, the "rest-binding" ingredients and the CV-M4 mechanics, Durell's specific operations, the Lowmark v1 [NEW] material (Relief Cut, Hollow Lock, House Marrick and the rest; D-11 is still open; FT-02a promotes the convoy loss, its name (the Fourteenth Lot), its place (Stillwater Fen, already canon) and the crews' refusal as history; it does not promote the Relief Cut or Hollow Lock as named works), every milestone, and all Thornfell production content, which will be authored in the Thornfell package in review state.

## 6. Independent review log

An independent reviewer read all six package files against `AGENTS.md`, the Master Protocol, `LORE/`, the Part 4–6 ledgers, the decision sheet, the reconciliation audit, the lore lock review, and the Lowmark bible (2026-11-02). It reported 20 findings (2 high, 9 medium, 9 low). All were accepted and fixed in this revision.

| # | Severity | Finding | Fix applied |
|---|---|---|---|
| 1 | High | Lowmark's stop (FT-02a) was owned by optional LR-M1, yet CV-M1 assembled all four stops with only standings as gates: either a hidden gate or a reveal out of order. | LR-M1 is now a hard parent of CV-M1 (`LR_STANDING`), optional for regional play. Longest chain 33. Arcs §1.2, §5, §6.2–6.3; Ledger R13, R17; §4.1 updated. |
| 2 | High | CV-M4 gave Kaldren travel to Emberholt, which the character ledger forbids. | Allies replaced by the player's learned practice and unnamed local hands. |
| 3 | Medium | Kaldren listed as a Summit custodian (ledger: cannot validate a Summit account). | R07 custodians are now the horn-trial record and a Ridge Warden log. |
| 4 | Medium | FT-05 gave the Stonebound a purpose ("made for") and active containment. | Rewritten as a physical settling of heat and pressure; flagged as a C11 expansion in FT-05. |
| 5 | Medium | Spectacle drift: Crest Hall siege repeating MQ10, a Titan fight, a fail-worded stake. | One act of sabotage; environmental survival sequence with no Titan fight; stake reworded under the three-state rule. |
| 6 | Medium | Speaker reading ignored his dream-seeded anchor. | Knowing ally **and** dream-seeded; wrong readings are "wholly puppet / wholly mastermind". |
| 7 | Medium | D-C03 gave Selvara a war role. | D-C03 now offers three options; Selvara bounded by her ledger row in each. |
| 8 | Medium | Darven Mott used as the guaranteed witness to the wartime ritual. | Guaranteed path is site evidence plus a provenanced record; Darven only guides. |
| 9 | Medium | Index and graph misstated the Emberholt gate. | Index corrected; gate drawn solid. |
| 10 | Medium | Several revelations lacked guaranteed paths; optional owners unacknowledged; R05 omitted the Lowmark link. | Paths added for R05, R10–R13, R15, R18, R19; optional-series owners exempted explicitly (R14). |
| 11 | Medium | Hearthveil reach beyond Emberholt not flagged. | Kept to Emberholt delegates and travellers; any direct reach folded into FT-04. |
| 12–20 | Low | E-M3/E-M4 codes; "Four causes" listing three; this placeholder; Contradiction 3 picking an invasion vector; "controlling plan" before approval; study edge vocabulary reading as a schema; contradiction 1 missing the Lowmark integration handoff's `Abandoned` plan (G04, I-13, D-INT-7); Kaelith "freed by accident"; FT-03 route assuming a map link. | All corrected; the integration-handoff conflict is now part of contradiction 1 and D-Q1. |

The reviewer confirmed clean: status labels, the Mire's two non-undead major threats, one chapel with three names, postwar Dreamers, the precursor kept distinct from the formal Remnant with C03, C06 and C07 open, no player spellcasting, no quest that can fail or be abandoned, and no reproduced RuneScape content.

### 6.1 Director refinement pass (2026-11-02)

The Creative Director reviewed the package, kept the overall direction, and asked for five targeted corrections before canon promotion. Changes made, without rewriting the architecture or starting regional quests:

| Request | Change |
|---|---|
| Fewer repeated civic-hearing finales; distinct climaxes with exploration, danger, discovery, action. | The hearing is the climax only in Lowmark MQ10. TF-M5 is now holding a closing pass in a blizzard, with Thornfell's stop found cut into the sealing works. EH-M6 is a descent through a failing heat main that exposes the Remnant's draw lines. CV-M3 is rebuilding an old Concord crossing in storm with a four-region crew, away from MQ10's Crestbridge. A second review pass removed early drafts that repeated MQ10's archive fire and location. CV-M4 is the Last Binding. MR-M5 and LR-M1 were already physical. Chips now shape short aftermath scenes only. |
| Reevaluate Lowmark MQ12 before every regional arc. | No region's entry milestone has a quest prerequisite. Cross-region gates remain only at consequential intersections: EH-M3 (TF-M3 or MR-M2), LR-M1 (Lowmark and Thornfell), and the convergence (all four regions). The FT-03 grain link became a non-ordered connection. |
| FT-02 believable, not four synchronized stops. | The war wore out over its last years through exhaustion, hunger, desertion, and local truces; the four withdrawals happen at different times, in a causal chain (Thornfell's slow sealing → Lowmark's spreading refusal → Emberholt's gamble → the last battle in the Mire), and raids continue for a time after. |
| FT-05 must keep the Titan a transformed person and a dangerous tragedy, with an earned resolution. | The Stonebound containment is withdrawn. The Titan is the initiate, suffering, held by canon Remnant bindings that are degrading. CV-M4 has the player gather the pieces of a new rest-binding from the people who hold them, then survive a multi-phase encounter in which the Titan can only be driven back, never killed, until it is bound to rest by name. Binders are Emberholt fire wardens and individual consenting Volkhari only (C06 kept open). |
| Keep FT-01, FT-03, FT-04 as preferred candidates. | Unchanged; still pending formal rulings (ruled 2026-11-02, §5.0). |

An independent review of this pass confirmed requests 2–4 were met and found blocking issues, all fixed: Volkhari had been written as a group institution (now individual, consenting binders only, C06 kept open); EH-M6 and the first CV-M3 draft repeated Lowmark MQ10's archive fire and Crestbridge location (replaced as above); three capstones shared one sabotage template (EH-M6 now systemic, CV-M3 weather-driven); the FT-02 chain was too neat (now "some fed others", with canon's fractured command and escalation); the FT-03 "stolen" link had become missable (now an exempt two-halves connection); plus stale Stonebound, "final-year", hearing, Thalan-capture, Asera, and graph references.


---

## 7. Recommended sequence for detailed quest authoring

The order follows dependency, not release dates. Each step names its output and what it waits on.

| Step | Work | Output (proposed location) | Waits on |
|---|---|---|---|
| 0 | **Done 2026-11-02.** Director rulings on FT-01–05, D-Q1, D-R1, D-C03, D-C06, D-CV1 and the convergence location. | Recorded in §5.0, the canon pass in §5.3, and project memory. | This package |
| 1 | **Done 2026-11-02.** Lowmark v1 follow-through: fill the bill's buyer name (the Whinstone Store, FT-03); no other v1 change. Runtime and schema work continues independently (Roadmap 24, 31). | Edit to the Act I package placeholder. | FT-03 |
| 2 | **In production (2026-11-02).** **Thornfell bible** in the Lowmark bible's format: author truth, cast, five milestones, side slate (at least half self-contained), POIs, flags, encounter families. Then milestone packages before side quests. | `04_CONTENT_PRODUCTION/Quests/Caelmor_Thornfell_Narrative_Production_Bible.md` and its packages (file map in that bible once committed) | Steps 0–1; map pass for Thornfell |
| 3 | **Shared civilian ledger** for the Register of the Unreturned: choose three to five cases, their custodians, and which region owns each resolution. Writing this before the Mire prevents later continuity drift. | A section in the Mire bible, or an appendix to this package | Step 2 |
| 4 | **Mire bible** (D-R1: preferred production order). | `…/Caelmor_Mire_Narrative_Production_Bible.md` (proposed) | Steps 2–3 |
| 5 | **C03 and C06 rulings**, then the **Emberholt bible**. | `…/Caelmor_Emberholt_Narrative_Production_Bible.md` (proposed) | D-C03, D-E2, D-S1 |
| 6 | **Lowmark return** (*The Fourteenth Lot*): one milestone and two or three side stories. | Addendum to the Lowmark bible | Thornfell bible (the second custodian) |
| 7 | **Convergence bible**: CV-M1–M4, world-event structures, the CV-M3 terms-scene chip table drawn from all arcs. | `…/Caelmor_Convergence_Narrative_Production_Bible.md` (proposed) | All four regional bibles |
| 8 | **Long Horizon** stewardship structures and deep-works exploration briefs. | Brief in the convergence bible | Step 7; any approved practice or faction system |

**Within every regional bible, author in this order** (working backward from revelations, then forward through discovery):

1. The region's owned revelations from the ledger, each with its two custodians.
2. The capstone, then the act turn, then the entry milestone.
3. Seeds and evidence placement across the remaining milestones.
4. Side stories that carry seeds, then self-contained side stories (at least half of the slate).
5. Micro-events and environmental discoveries (three-layer framework).
6. Independent review against this package, the character ledger, and the map audit.

### 7.1 The quest contribution contract

Every future quest, however small, declares five things in its summary card. This is how a self-contained quest still contributes to a larger, consistent world.

| Field | Question | Example answer |
|---|---|---|
| **Anchor** | Which faction, place, or community does it deepen? | Thornfell Cairn-Keepers |
| **World-truth row** | Which history row (H01–H25) or present pressure does it touch, if any? | H16, or "none (present-day only)" |
| **Revelation role** | Does it plant, support, or own a revelation (R01–R20), or is it self-contained? | Plants R06 (a cairn with no body) |
| **Recurring evidence** | Does any object, record, or person recur, and with which independent custodian? | None |
| **State compliance** | How does it stay within Inactive/Active/Completed? | Choice recorded in `TH_…` outcome flag (Thornfell region flags use `TH_` because Lowmark MQ6 already uses `TF_` for quest-local flags); no fail path |

A quest that answers "self-contained" to the revelation field is welcome. Part 5's rule stands: Caelmor needs many stories that end where they begin.
