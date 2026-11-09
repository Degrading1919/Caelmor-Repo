# Mire of Fallen Banners: Encounter and Enemy Requirements

**Status (2026-11-09):** review-state content. Gameplay Designer requirement set, **Batch 4** of the Mire production plan (bible §12). It brings every enemy family, variant, boss, miniboss, elite, fauna fight and hazard authored in the Mire narrative packages into one implementation reference. Everything here is **[NEW]** authored content and is not canon until the Creative Director promotes it (MD-16). Items marked **[PROPOSAL — DIRECTOR]** are consequential rules the content depends on; items marked **[PROPOSAL — Gameplay Designer]** are placements or values this file adds. Numbers are **framing targets** (fight length, HP remaining, telegraph duration), not balance values. Health, damage, armour and XP values belong to the tuning pass after a playable build exists. This file is **documented dependencies only**: no schema, JSON or C# is authored or implied (bible §11.12).

**This file is canonical for cross-package combat values.** Where two Mire packages give different numbers or kits for the same creature, telegraph, status or rule, the value in §13 (shared canonical register C-1 to C-12 and resolutions I-1 to I-24) is the implementation value. The quest-package edits listed in §13.3 were **applied** in the Batch 4 encounter alignment review (2026-11-09), so the three acts and four side-quest files now carry these values; the bible rows in §13.3 are with the bible owner. Where any text still differs, implementation follows this file.

**Director rulings (2026-11-03, binding):** `Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md`. **CDR-1:** every enemy is defeated at **0 HP**; no health-threshold yield, retreat, break-off, scatter or drive-off; scripted survival only for the named exceptions in its §4 register, and **the Mire has none** (bible §3 "SX proposal: none"). **CDR-2:** Ranged is a core combat skill; every fight accepts melee or ranged and none requires ranged. **CDR-3:** the Mire is an internal milestone of the complete game. **CDR-4:** standard RPG systems over bespoke simulation; this file lists only genuinely necessary new runtime needs (§9.4).

**Open Director decisions this file is built around:** **MD-7** (Hollowfoot as enemies) is **OPEN**: every Hollowfoot entry is tagged `[MD-7]`, is optional, carries nothing evidentiary, is never the only route, and has a non-combat alternative recorded beside it (§5.7, §11.1). **MD-3** (first-light crossing) and **MD-4** (staged drainage, no breath meter) are recommendations awaiting sign-off; dependent rows are tagged. **MD-8** (the General as a revisitable night encounter) is a recommendation; the Night Count is tagged.

**Sources read (current state, 2026-11-09):** `Quests/Caelmor_Mire_Narrative_Production_Bible.md` (§1.1, §2.4, §2.6, §3, §4.2, §9, §10, §10.1, §11, §11.1, §11.2); `Quests/Caelmor_Mire_Main_Act_I.md` (§A7, §A7.1, §A9, §B7, §B7.1, §B9); `_Act_II.md` (§A7, §A9, §B7, §B8.1, §B9, §B12); `_Act_III.md` (§7, §7.1, §7.2, §9.1, §11, §12, §14.1, §E.9); `Quests/Caelmor_Mire_Side_Quests_Names_and_Lanterns.md`, `_Cloth_and_Memory.md`, `_Work_and_Skills.md`, `_Settlements_and_Combat.md` (every encounters-and-hazards table, step table and integration table). The format follows `Enemies/Caelmor_Thornfell_Encounter_and_Enemy_Requirements.md`.

**Source state.** The three main acts were reviewed and committed before this file was written. The four side-quest files are **under concurrent independent review**; this file was built from their working-tree state on 2026-11-09, which already includes that review's fixes to MNK-E3 (mudcutters lie as edge mounds and rise on the Call or on approach), MRH (the first-thinned patch darkens back to rust so the stop loop cannot run dry) and MFH `S05` (objective now "Defeat the dogs at the racks"). §16 says what to re-check when those reviews land.

**Companions:** `Zones/Caelmor_Mire_POI_and_Zone_Requirements.md` (arenas, lanes, lit-post radii, channel crossings, water stages) and `Quests/Caelmor_Mire_Integration_Requirements.md` (both Batch 4). Arena geometry stated here is repeated there as level-design requirements; §13's shared register is stated in the same words in both.

**Ownership:** the Gameplay Designer owns this file. The Schema & Content Engineer owns creature data schema and naming (Roadmap 33.7). The Systems Engineer owns spawn rules, hazard volumes, status effects and the re-form state model. Animation, VFX and audio own the tells.

---

## 0. How to use this file

| You are | Read |
|---|---|
| Building creature definitions | §4 roster, §5 family specs, §6 fauna, §7 bosses, minibosses and elite |
| Building spawn and encounter data | §11 encounter register; §10 earth-memory rules and re-form sites |
| Building hazards, the Chapel light system and the count | §3 telegraph grammar, §9 hazard register |
| Building combat runtime support | §1 constraints, §8 defeat (CDR-1), §9.4 runtime needs |
| Tuning after the first playable build | §2 bands and universal targets; the band notes in §5 |
| Editing a Mire quest package | §13.3 package edits needed |
| Reviewing for the Director | §13 canonical register and issues, §14 questions |

**Id convention.** Mire packages prefix every encounter with the three-letter quest code (`MNS-E1`, `MRH-E2`), so no id collides with Lowmark (`MQ…`, two-letter side codes) or Thornfell (`T…`). Hazards use `<CODE>-H<n>`. Hazards the packages describe without an id get one here, marked **[NEW id]**. World pockets outside any quest use `MW-<nn>` (§11.3). Canonical register rows are `C-n`; issues found between packages are `I-n`.

---

## 1. Runtime constraints that shape every encounter

These are the Lowmark and Thornfell constraints (Thornfell encounter file §1), unchanged, plus the Mire-specific lines.

| Constraint (source) | What it means for encounter design |
|---|---|
| **Click-to-move on a host NavMesh; Shift sprint; no jump** (Unity README; Phase 1.3 §1) | Every dodge is "click a floor point and walk there". No counter needs a jump, dash, roll or precise input timing. "Move on two" (the count) is a walk out of a lane or ring, never a timed input. |
| **Agility triggers approved, not built** | No encounter may need an agility trigger. Every Mire shortcut into an arena (walkway gaps, palisade climbs, the MRH stump vault, the MCF bale step) has a walkable fallback, and every cover object (pole frames, stumps, the drum of the Chapel posts) is NavMesh-reachable. |
| **10 Hz authoritative tick; intents enqueue for T+1** (Stage 6.1.1) | **Minimum telegraphs (carried from Lowmark and Thornfell, canonical here as C-1):** light hits ≥ 0.8 s; moderate or heavy hits ≥ 1.0 s; any hit at or above 25% max HP, any displacement (push, pull, knockback, knockdown) and any instant area effect ≥ 1.5 s. Several package values sat below these; §13 I-9 to I-12 raise them. |
| **Auto-attack on interval; specials on cooldown; no stamina** (Phase 1.3 §2) | Fights are about position, target priority and **ground** (which lane, which patch, which lit post), not input speed. |
| **AI roles Passive / Aggressive / Defensive; enemies never flee** (Phase 1.3 §2) | Matches CDR-1: every Mire enemy, human, animal or earth-memory, fights until defeated at 0 HP (§8). Leash/reset stays. Earth-memory enemies re-form by place condition, which is not a retreat (§10). |
| **Combat states; Incapacitated "does not imply death"** (Stage 6.1.2) | Not required by Mire content. The Mire registers no scripted exception (bible §3); no quest on-defeat hook plays a surrender. |
| **Interaction needs reach and line of sight** | Channels under attack (lift a pole, fold a banner, pin logs, light a post, open a sluice board, pull or seat a stake, hold the gap stone) need a clear standing pad facing the object. Channel progress is kept when interrupted (bible §11.1). |
| **Player camera only** | Telegraphs must read at default zoom from any angle **at night and in fog**, which is most Mire combat. The **ground** carries the primary tell (ripple, swell, reed-ripple, silt line, ironbloom colour, lane furrow lips); the body pose and audio are its required twins (§3). |
| **Deep water is non-walkable; no swimming, no drowning, no breath meter** (bible §11.1, MD-4) | No push, pull or knockback can move a player into deep or Sour water. Ditch shallows, island edges and mud are walkable slow ground. Every edge that meets deep water is a hard NavMesh stop. |
| **Solo-first; per-player state** (bible §9) | Every encounter is solo-clearable at its band. Co-op scales health per participant, shares world creatures and gives step credit to all participants on the step. Channel states, standards' risen/folded state, Chapel water stage (host-led, §11.1), the count, circle arrivals and choices are per player with the host fallback. |
| **Combat never reveals evidence; no defeated enemy speaks** (bible §11.3) | No creature drop advances an investigation. Testimony comes from living witnesses (Edris, Dunstan, Oswin, Bran, Halsey, Annot), registers, household books, ledgers read in place, and objects. Phenomena (Wraiths, Echoes, the General, the Shades, the glass, the moss) prove nothing and identify nobody. |
| **Earth-memory stays bounded** (bible §2.4) | Banner Wraiths exist only where a standard is **risen**. Earthen Echoes exist only where their **condition** holds (fog on the Blackwater, a disturbed camp, an unfinished ring, the ridge's count). Chapel Shades exist only inside the Sunken Chapel and are a hazard. The General exists only on Bannerline. The Sorrowback is **not** a Mire encounter (trail only, MDS07). |

---

## 2. Progression bands and universal solo targets

Bible MD-10 sets the framing: no quest prerequisite; MR-M1–M2 **Competent**, MR-M3–M5 **Advanced**. Exact levels belong to tuning.

| Band | Content | Equipment assumption | Combat role |
|---|---|---|---|
| **Competent (early)** | MR-M1; side quests unlocked after MR-M1 (MRS, MFT, MFH, MSG, MLL, MNK) | Post-Thornfell identity (production framing only; no Thornfell requirement) | First Mire fights: Griefbit Beetles, the first Banner Wraith, Bog Hounds, Reedlurkers, the first Earthen Echoes (MLL), Mud-Clad Raiders and the Mud-Boss (MNK, upper end). |
| **Competent (late)** | MR-M2; side quests unlocked after MR-M2 (MBS, MMR, MWS, MHG, MBO, MRH; MCF after MBS) | As above, toward Advanced | Bearers and the Risen Colour; the Rust Hart (upper end); Rootshadow cutters (MCF reaches into Advanced). |
| **Advanced** | MR-M3, MR-M4, MR-M5; side quests after MR-M3 (MFW, MRW, MBA chain; MLW after MR-M4; MLD after MLW) | Advanced identity, cooked food | Echoes from the boat, the Chapel by light, the count, Echo files, the General. |
| **Post-arc** | After MR-M5 | Toward the next milestone | The Night Count `[MD-8]` (MW-01), world pockets (§11.3). |

**Universal targets (all bands; Lowmark and Thornfell values kept)**

| Rule | Target |
|---|---|
| Standard fight length | 20–90 s per group; set pieces 2–5 min with phases or waves (MR-M2 standards, MCS-E3, MLL-E2, the Bannerline road); minibosses **3–4.5 min**; the elite **2.5–3.5 min**; the Act III boss **6–8 min** (Act III §7.1.5, canonical, C-11) |
| HP after a first-attempt standard fight | 50–85% remaining (per-pocket values in §11 govern) |
| Largest single non-boss hit | ≤ 30% of band max HP, telegraphed ≥ 1.5 s |
| Hazards | **Cannot kill a player above 25% HP** (C-2). No hazard, push, pull or knockback can move a player into deep water, off the causeway into Sour water, overboard, or off the ridge. Every displacement goes to a defined safe side (the road, the island's dry centre, inside the boat, a lit post, up-lane). |
| Group size | 1–4 hostiles active outside set pieces; set pieces cap at 5 standing at once (MBR-E5 counts its re-formed Wraiths inside the cap) |
| Death | Respawn at the named safe point with step, flags, carry-state progress and completed segments intact; the pocket resets as its row in §11 says |
| Toughness framing | **fragile** (swarm, echo, reed-slinger) · **standard** · **sturdy** (carapace, gnawer, snapper, bearer, stalker, rutting stalker) · **elite** (~3–5× standard: the Mud-Boss) · **miniboss/boss** (fight-length driven: the Risen Colour, the Rust Hart, the General) |

---

## 3. Telegraph grammar (ground first)

The Mire's readable system is **ground** (bible §1.1). Every telegraph has a **ground or water tell** and a **body or audio twin**. Durations are canonical; where packages differ, §13 gives the reconciliation (†).

| Shape | What the player sees / hears | Canonical duration | Counter | Used by |
|---|---|---|---|---|
| **Swell (forming)** | Mud bulges and darkens; a column or hump rises; a standard's cloth lifts or cracks with no wind | **1.5 s** (Echo stand-up); **3.0 s** (Wraith forming and standard pulse) | Strike the hump (free hit) or step clear of where it stands | Earthen Echoes, Banner Wraiths, the Risen Colour's pulse |
| **Ripple (water)** | A line of reeds parts toward the player; the ripple stops when a head lifts clear | **1.2 s** lunge (**1.5 s** first-appearance pockets†); **1.0 s** spit | Step back from the water's edge; sidestep the lobbed spit | Reedlurkers, Silt Crawler burst (a silt line, 1.5 s) |
| **The count** | Ground pulse two soft beats then a deep third; ripple ring from the muster post, heavy ripple down the lanes on three | **1.2 s per beat** (3.6 s count); **0.9 s** in the General's P3 | **Move on two.** Every count attack lands on a third beat and is shown at least one beat earlier (two beats in P3, C-7) | Echo files, the General, MBL bearers, the gap |
| **Raise** | A standard-shape lifted high and held; cloth ripples | **2.0 s** (bearer), **2.5 s** (the Colour's Rally) | Any hit during the raise interrupts it | Bearer, the Risen Colour |
| **Stamp (charge)** | Two forefoot stamps throwing red dust; head up then down | **1.5 s** minimum† | Sidestep; behind a stump the charger hits it and staggers 2 s | Tarnish Stalkers, the Rust Hart; the carapace's butt uses the same minimum |
| **Wind-up (human)** | Weapon drawn back through mud or across the body; a sling arm whirls; a blade dipped in a hip pot | **1.0 s** melee†, **1.2 s** sling and throw† | Step back or aside; break line of sight to throwers | Mud-Clad Raiders, Rootshadow Cutters, Hollowfoot `[MD-7]` |
| **Recoat / drink** | A kneeling figure scooping mud onto its chest | **2.0 s** | Any hit interrupts | The Mud-Boss |
| **Lean (Chapel)** | The hand lantern's flame leans away from the thick dark and shrinks | **~2 s** (S06: same lean, presses every ~2 s) | Get into a lit post's radius | Chapel Shades (hazard, §9.2) |
| **Gutter** | A post's flame shrinks and smokes | **1.5 s** | Relight (~2 s) or run to the next lit post | The draught (MCS-H2) |
| **Ironbloom** | Patch colour (deep rust → rust → orange → pale) and sign (licked soil, scrape) | Not timed (read before the fight) | Stand on the patch it will stop at | The Rust Hart |

**Four rules for every telegraph.**
1. **Ground and body twins.** A player looking away or in fog still gets it. No tell is colour alone: every colour tell (ironbloom, the gap ripple brightening, the poisoner's green-black drip) also has a shape or motion. Audio is a third carrier where the source has one; the count additionally carries an optional caption ("one… two… THREE") and optional rumble (Act III §7.1.2).
2. **The environment names the safe space**, not UI: the road beside the ditch, the turf strips between lanes, the stump behind the Hart, a lit post's circle, the inside of the boat, the dry centre of the reed island.
3. **Every heavy attack has a punish window** (the Hart's lick, the Colour's Advance recovery, the General's plates sloughing for ~4 counts, the Mud-Boss's recoat).
4. **Interruptible wind-ups are tools both ways.** A raise, recoat or shout that buffs, heals or calls help is always interruptible by any hit, melee or ranged (bearer Raise, Colour Rally, Mud-Boss recoat, Hollowfoot shouter `[MD-7]`). This is the Mire's priority-target lesson, taught in MBR-E2.

---

## 4. Roster and Phase 1.5 count check

### 4.1 Families (bible §10; Phase 1.5 §4.1: 3 low, 4 mid, 2 high)

| Tier | Family | Default AI role | Standard variants | Elite | Variants counted |
|---|---|---|---|---|---|
| Low | **Bog Hounds** (wildlife) | Aggressive pack on peat paths and planks; some prop-targeting | runner, gnawer | — (wildlife) | 2 |
| Low | **Reedlurkers** (wildlife) | Aggressive ambush, leashed to shallows | lurker, snapper | — (wildlife) | 2 |
| Low | **Griefbit Beetles** (vermin) | Aggressive swarm; drawn by fear | swarm, carapace | — (vermin) | 2 |
| Mid | **Mud-Clad Raiders** | Aggressive ambushers at bad crossings | mudcutter, reed-slinger | **Mud-Boss** (MNK-E3) | 3 |
| Mid | **Rootshadow Cutters** | Aggressive cloth-strippers with poisoned blades [CANON poisons] | cutter, poisoner | — (recorded deviation, bible §10) | 2 |
| Mid | **Tarnish Stalkers** | Aggressive stop-and-charge elk on ironbloom ground | stalker, rutting stalker (unplaced; §11.3 MW-03) | **the Rust Hart** (side miniboss, MRH-E1) | 3 |
| Mid | **Hollowfoot** `[MD-7]` (human) | Passive drifters; Aggressive on entry or nearby combat | wanderer, shouter | — (recorded deviation; no Hollowfoot person is made a boss) | 2 |
| High | **Banner Wraiths** (earth-memory) | Lane-walking impressions tied to a risen standard | wraith, bearer | **the Risen Colour** (MR-M2 miniboss phenomenon; never named in UI) | 3 |
| High | **Earthen Echoes** (earth-memory) | Slow walkers repeating a motion; collapse when struck; re-form by condition | echo, file | **the General Who Wouldn't Fall** (Act III boss) | 3 |

**Variant total:** 18 standard + 4 elite-slot (Mud-Boss, Rust Hart, Risen Colour, the General) = **22**, matching bible §10 and inside Phase 1.5 §4.2's ~20–22. **Bosses:** 1 Act III boss (the General) and 2 minibosses (the Risen Colour, the Rust Hart), matching bible §10 and Phase 1.5 §4.3. The Mud-Boss is the one true elite. As in Thornfell (I-15, I-16), the General and the Risen Colour fill their families' elite slots; they are counted as boss and miniboss, not as separate elites.

**Under MD-7's alternative** (Hollowfoot as non-combatant survivors only), the Hollowfoot family leaves the roster: **20 variants** (16 standard + 4), still inside ~20–22. Nothing else in the count moves.

**Sub-forms, not variants:** the **weak file** of 2 echoes (MBL-E1 practice lane); the **Shades** (hazard, not creatures); fauna in a provoked state (§6).

**Placement gap.** One counted variant, the **rutting stalker**, appears in no package. §11.3 MW-03 proposes a world placement; cutting it drops the count to 21 (20 under the MD-7 alternative is then 19, still near range).

### 4.2 Fauna (Hunting fauna and vermin; not counted; fight only when provoked)

Marsh Rats (ambient vermin), mire boars, fenny does, **Silt Crawlers** (stirred by the Chapel draining, MCS-E2/E3), marrow herons, tarnish serpents (bask on iron soil), fen fowl. Full behaviour in §6.

### 4.3 First appearance and recurrence

| Family | First possible appearance | Main-line first | Recurs in |
|---|---|---|---|
| Griefbit Beetles | MNS-E1 (MR-M1) | MR-M1 | MWS-E1, MLD-E1 |
| Banner Wraiths | MNS-E2 (MR-M1) | MR-M1 | MBR-E1/E2/E3/E5, MBL-E5 |
| Bog Hounds | **MFH-E1** (after MR-M1) | — | MBO-E1 |
| Reedlurkers | **MRS-E1 or MLL-E1 or MSG-E1** (all after MR-M1) (§13 I-3) | MBR-E4 (MR-M2) | MRC-E1, MCS-E1/E3 |
| Mud-Clad Raiders | MNK-E1 (after MR-M1) | — | MNK-E2/E3 only |
| Earthen Echoes | **MLL-E2** (after MR-M1) or MMR (after MR-M2) (§13 I-4) | MRC-E2 (MR-M3) | MBL-E1/E2/E4/E6/E7; MW-01 |
| Tarnish Stalkers | MRH-E2 (after MR-M2) | — | MW-03 (proposal) |
| Rootshadow Cutters | MCF-E1 (after MBS) | — (MR-M2 shows signs only) | MCF-E2/E3 only |
| Hollowfoot `[MD-7]` | MBL-E3 (MR-M5) | MR-M5 (optional) | Never anywhere else |

---

## 5. Family specifications

Each table lists the variant kit with canonical telegraphs. "Band notes" gives the role the family plays, not numbers. Telegraph values marked † were reconciled from differing or below-minimum package values (§13).

### 5.1 Griefbit Beetles (low; vermin)

**Ecology.** Black beetles that boil out of rotten timber and grave-wet peat where fear rises (bible §10). They are drawn to a frightened person nearby and thin when that person is calmed. The draw is ecology and presentation, never evidence of anything about the person.

**AI role.** Aggressive. Swarms surge at people and carts; the carapace guards a swarm's flank. **Fear add (canonical, C-12):** while a named frightened NPC is in the pocket and not yet calmed, **one** extra swarm gathers visibly (~3 s over the source) once per fight after the pocket's timer (MNS-E1: 40 s; MWS-E1: 30 s); calming the NPC first cancels the pending add.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Swarm** | One combined creature (a cloud of beetles) with one health pool; surges along a short line; can spread into a bite circle | **Surge:** the cloud tightens, click-hum rises in pitch (**1.0 s**), then rolls 3 m along a line (light). **Spread:** the cloud flattens onto the ground (**1.5 s**†), then bites in a 2 m circle (light) | Sidestep the surge line; leave the circle | Competent (all) |
| **Carapace** | Guards the swarm's flank; charge-butt | Rears and clicks its wing-cases (**1.5 s**†), then a straight charge-butt with a small knockback toward open ground (never off a walkway edge) | Sidestep; punish the recovery | Competent |

**Band notes.** MNS-E1 is the first Mire fight (60–90 s, 60–80% HP) and teaches that fear draws them by showing the wave thin when Edris calms the reed-cutter. MWS-E1 repeats the lesson with Maddy. MLD-E1 is optional and trivial, with a calm option (§11.2). Swarm **fragile**, carapace **sturdy**.

**Defeat / loot.** Defeated at 0 HP with the ordinary defeat presentation. On MLD's calm path the swarm is never engaged: it stays in its ditch under an ordinary leash and aggro-on-enter/attack, with no settle state (Names MLD.6). That is scenery, not a health outcome. Loot: nothing, or ordinary vermin material per the economy pass. Nothing advances a quest.

### 5.2 Bog Hounds (low; wildlife)

**Ecology.** Hungry feral packs on peat paths, plank rows and old drill ground, drawn to smoke racks and anything carried that smells of food. Starving, like everyone this season (MFH Gwenna's line); that is presentation, not mercy logic.

**AI role.** Aggressive pack. Runners circle and dart; the gnawer holds a lane or goes for a prop (MFH racks: tears an eel down every ~6 s it is left alone, cosmetic, racks refill). On the Dry Muster's furrows the pack runs the furrow as a line (MBO-E1).

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Runner** | Circles and darts; in furrows, runs the line behind a lead runner and breaks out to flank | **Dart:** head drops, hackles lift (**0.9 s**†), then a short lunge (light). **Furrow run:** the lead runner barks once (**1.0 s**), then the line runs the furrow toward the player | Sidestep; step across the furrow lip and catch runners as they break out | Competent |
| **Gnawer** | Holds the lane ahead or works a prop; heavy bite | Stands square, lips back (**1.2 s**†), then a heavy bite (moderate-heavy; **no bleed**†, §13 I-8) | Step out; interrupt its prop work by attacking it | Competent |

**Band notes.** MFH-E1 is the first appearance (45–60 s); planks are narrow, so ranged players have the row's length and melee players the rack posts. MBO-E1's furrows are straight lanes: ranged can shoot down a furrow. Runner **standard**, gnawer **sturdy**.

**Defeat / loot.** Defeated at 0 HP; no flee. Harvestable where the economy allows; hides belong to the economy pass. Nothing advances a quest.

### 5.3 Reedlurkers (low; wildlife)

**Ecology.** Amphibious ambushers in shallows, sumps and bay pools, telegraphing by reed-ripple (bible §10). Leashed to water: a player who steps back onto firm ground beyond reach ends the lurker's lunge range.

**AI role.** Aggressive ambush. **Canonical kit (C-5; §13 I-1):** the **lurker** waits submerged and lunges from the water's edge; the **snapper** hangs back in deeper water and spits, and clamps if a player closes to melee on its bank. MBR-E4's swapped kit (lurker spits, snapper clamps only) is reconciled to this.

**Reach (CDR-2, C-5).** "Deeper water" for a snapper always means **wadeable** water (knee-deep, standard slow) within a few metres of the bank or sump lip, never non-walkable deep water, so a melee player can always reach it. A lurker that takes damage from an attacker it cannot reach (beyond its 3 m lunge) for ~5 s submerges and resets to full at its spot (ordinary leash/evade), so firm ground beyond the lunge is not a safe firing position; ranged players fight at the edge, sidestepping lunges, and the snapper's spit covers the bank.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Lurker** | Submerged beside a gather node, floating fowl, lantern post or vent; lunges 3 m from the water; may climb a vent lip (MSG) | **Reed-ripple:** a line of reeds bends toward the player (**1.2 s**; **1.5 s** in the first-appearance pockets MRS-E1, MLL-E1 and MBR-E4†), then a straight lunge-bite (light-moderate). **Grab** (on a connected lunge): a short hold (**root 1.5 s**) the player breaks early by attacking the lurker. **Vent climb** (MSG only): claws on the shaft lip (**1.0 s**), then it knocks a vent plank shut (puzzle state only, no damage) | Step back from the edge; attack to break a grab; reopen the vent | Competent–Advanced |
| **Snapper** | Holds deeper water or a bank; spits; clamps in melee | **Spit:** head rises clear of the water, throat swells and the ripple stops (**1.0 s**), then a lobbed gob (light) that leaves a short-lived slick where it lands (standard slow while standing in it; visible before entry). **Clamp** (melee range): jaws open with a wet clack (**1.0 s**), then a clamp (moderate) with **root 1.5 s** | Sidestep the spit; keep out of the slick; close behind the bank cover and punish after a clamp | Competent–Advanced |

**Band notes.** Reedlurkers give ranged players a ranged enemy to answer and melee players a bank to close behind (bible §10). They are the "familiar threat" that opens MR-M4 (MCS-E1) and the pressure on MSG's puzzle lulls. Lurker **standard**, snapper **sturdy**.

**Defeat / loot.** Defeated at 0 HP; they do not re-form (MSG.6). Harvestable where the economy allows. Nothing advances a quest.

### 5.4 Mud-Clad Raiders (mid)

**Ecology.** Camouflaged bandits at bad crossings who pull or move stakes so travellers cross Sour (MNK). They lie in the shallows as mud mounds that breathe steam. Human. Appear only at Nine Stakes (by design; no world pocket, §11.3).

**AI role.** Aggressive ambush. Mudcutters rise from mounds when a player wades within ~6 m; reed-slingers hold hummocks and crossfire.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Mudcutter** | Lies as a mud mound; rises and cleaves | **Rise:** the mound's steam thickens and it shifts (**1.2 s**). **Cleave:** weapon dragged back through the mud (**1.0 s**†), then a cleave (moderate) | Watch for breathing mounds; step aside of the cleave | Competent (upper) |
| **Reed-slinger** | Holds a hummock in the reeds; slings clods | Arm whirls twice (**1.2 s**†), then a clod along a line (light; **no blind**†, §13 I-8) | Strafe; use the reed path screened from one slinger, or trade across the water with Ranged | Competent (upper) |
| **Mud-Boss** (elite) | §7.4 | §7.4 | §7.4 | Competent (upper), MNK-E3 |

**Band notes.** MNK is the first combat challenge most players meet (after MR-M1, Competent upper end): E1 45–60 s, E2 50–70 s, E3 2.5–3.5 min. Mudcutter **standard**, reed-slinger **fragile**, Mud-Boss **elite**.

**Defeat / loot.** Defeated at 0 HP with the ordinary defeat presentation (§8). No dialogue after defeat; Halsey's one sober line from the bank ("That's the last of them.") is the only comment. Stolen goods under hides are ordinary loot plus the ferry family's cart goods as a **carry-state bundle** for Halsey. The history of the crossing comes from the **ferry book** (`MNK-D3`), never from a raider.

### 5.5 Rootshadow Cutters (mid)

**Ecology.** Syndicate cloth-strippers who cut cloth from risen standards to sell as "commemorative goods" (MD-12). Fragmented and avoiding large conflict [CANON]; no leader is named. Their go-between, **Gethin Scarth**, never fights, is never present at the Reed Hide and is never targetable. Human. Appear only in MCF (by design; no world pocket).

**AI role.** Aggressive; leashed to their stage of the Hide (mouth, frames, stack bay). Poisoners are Defensive at range.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Cutter** | Closes in pairs; uses stripping frames to flank; may cut a frame lashing | **Hook-slash:** reed-hook drawn back across the body (**1.0 s**†), then a wide slash in a 2.5 m arc (moderate). **Frame cut** (MCF-E2): slashes a lashing, the rope creaks (**1.5 s**†), and a bare pole swings down along a 2 m line (moderate; a line area effect) | Step back from the arc; step out of the pole's line | Competent (late)–Advanced |
| **Poisoner** | Holds a platform, a far frame or the stack top; throws poisoned blades; two poisoners alternate (MCF-E3) | Dips the blade in the hip pot, green-black drip visible (**1.2 s**), then a thrown blade (light) that applies **standard poison** (damage over time, ~8 s; ordinary antidote cures) | Sidestep or break line of sight behind a frame; read both poisoners' dips in E3 | Competent (late)–Advanced |

**Band notes.** MCF is the Cloth and Colour combat core (~55% combat). Frames are cover for both sides; ranged players clear the stack top, melee players climb the low bale step (walkable fallback: a bale ramp). The Hide-mouth lookout platform (MCF-E1) has a walkable stair or ramp on the NavMesh, so melee reaches its poisoner without an agility trigger (MAP VERIFICATION REQUIRED). Cutter **standard**, poisoner **standard**.

**Defeat / loot.** Defeated at 0 HP with the ordinary defeat presentation. Nothing a cutter drops advances the quest: the evidence is **Gethin's ledger**, read in place at the jetty, and the cloth itself (carry-state bales). Hob (crew track) stops at the Hide's edge and never fights.

### 5.6 Tarnish Stalkers (mid)

**Ecology.** Erratic iron-antlered elk of the ironbloom ground (MP27). Their paths zigzag; their stops do not: they always stop on thick ironbloom (deep rust or rust) to lick iron-rich soil, never on orange or pale. **Iron soil and the old iron in it are inspectable, never collectable** (battlefield metal is evidence, not feedstock, MD-11).

**AI role.** Aggressive. **Stop-and-charge:** run erratically to the nearest thick patch, stop, then charge the nearest two-legged target.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Stalker** | Smaller; stop-and-charge like the Hart; called by its bellow (MRH-E2) | **Stamp:** two forefoot stamps throwing red dust (**1.5 s**†), then a straight charge (heavy, knockdown) | Sidestep; stumps stop the charge (2 s stagger) | Competent (late) |
| **Rutting stalker** (unplaced; MW-03) | A stalker that defends a patch at dusk: it stops, then charges anyone who enters the patch's edge | As stalker; plus **Antler toss** at a stop: head swings low (**1.5 s**), a short sweep that knocks the player back off the patch toward bare ground | Stay off its patch; sidestep the charge | Competent (late) / post-arc |
| **The Rust Hart** (miniboss) | §7.3 | §7.3 | §7.3 | Competent (upper), MRH-E1 |

**Band notes.** MRH is the reference "read the ground before the fight" encounter. Stalker **sturdy**, rutting stalker **sturdy**.

**Defeat / loot.** Defeated at 0 HP. Harvestable per the economy pass (antler, hide, meat). The Hart's antlers are a quest choice (`MRH_ANTLER`: Rootrest's bonecarvers or Annot's wall), not loot. The **old arrowhead** in the antler base is an inspect, not an item. Nothing advances an investigation.

### 5.7 Hollowfoot `[MD-7]` (mid; human)

**[PROPOSAL — DIRECTOR] MD-7 is OPEN.** The bible's recommendation (Hollowfoot as an ordinary human enemy family under CDR-1) is built here; the **alternative** (non-combatant survivors only) is recorded in full below and in §11.1, and swapping to it touches only the rows tagged `[MD-7]`.

**Ecology (canon, dossier §IX).** Humans driven half-mad by war trauma; they wander without awareness of time and react violently to loud noise and bright banners. They appear as enemies **only where the General's count drives them** (MR-M5, the Bannerline road's Rag Bend) and nowhere else in the Mire.

**Dignity rules (binding on every Hollowfoot row).** No named or known person is ever among them. No NPC treats a fight as a cure. Lysa's settled Hollowfoot (Jory Wick and the Fenward residents) are non-combatant NPCs, never targetable, under either ruling. Hollowfoot carry nothing evidentiary. No Hollowfoot fight is required or the only route. "Bright cloth" is flavour (standard aggro and assist radius), never a gear-visibility system (Act III open decision 5; CDR-4).

**AI role.** Passive drifters in their hollow; Aggressive on entry or on combat within assist radius; the shouter calls the others when struck.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Wanderer** | Drifts; rushes when roused | Hunches, shoulders forward (**1.0 s**), then a short rush (moderate; no knockback) | Sidestep | Advanced |
| **Shouter** | Drifts; when struck, shouts and pulls the others to him | Throws head back (**1.2 s**), then a shout that pulls the other two to him | Interrupt the throw-back with any hit | Advanced |

**Band notes.** MBL-E3 only: optional, 40–60 s if engaged, avoidable entirely by keeping to the road. Wanderer **standard**, shouter **standard**.

**Defeat / loot.** Defeated at 0 HP with the ordinary human defeat presentation; ordinary loot only; no yield, flight or downed state; at most one sober ally line.

**MD-7 non-combat alternative (one line):** the Rag Bend's three drifters sit among the rags rocking to the count, non-hostile and never targetable; the player can pass on the road or **sit with them** (interact ~3 s), after which they walk down to the wardens' brazier and a Griefwatch carer takes them to Lysa; no XP, loot or flag (Act III §14.1). Under that ruling the Hollowfoot creature definitions are not built.

### 5.8 Banner Wraiths (high; earth-memory)

**Author truth (bible §2.4, C15).** Minor, place-bound impressions tied to **risen** standards. Not ghosts, not souls, never undead. They repeat a motion (a walk across the road, a cut, a shove). They dissipate when their banner is properly honoured or retired. **Combat disperses, conditions decide** (§10).

**AI role.** Each Wraith walks a fixed lane tied to its standard and engages anything that enters it. Slow and readable. Wraiths never target or engage non-combatants (Calwen, Mara, Corra, Dunstan; MBR rules).

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Wraith** | Walks its lane; cuts and shoves | **Forming:** the standard's cloth lifts or cracks with no wind and the peat at its foot darkens and swells (**3.0 s**). **Cut / sweep:** blade-shape or cloth arm drawn back over the shoulder (**1.0 s**), then a slow wide arc (moderate). **Press:** leans forward behind its standard-shape (**1.5 s**), then a two-step shove along its lane (one step of knockback; may put the player in the ditch shallows: slowed, never drowned) | Step out of the lane; wait out a pass; strike to collapse it (it re-forms by condition) | Competent–Advanced |
| **Bearer** | Hangs back by its standard; buffs | **Raise:** lifts its standard-shape high and holds (**2.0 s**, cloth ripples); if not interrupted, Wraiths within **8 m** attack faster for **10 s** (C-4). Any hit during the raise cancels it. **Plant** (MBL-E5 only, on the count): grounds its pole on a third beat; a 3 m shock ring decal shows from **beat 1** (~2.4 s)†, then the ring lands (moderate, small knockback outward) | Interrupt the raise (priority target); leave the ring on two | Competent (late)–Advanced |
| **The Risen Colour** (miniboss phenomenon) | §7.2 | §7.2 | §7.2 | Competent (late), MBR-E5 |

**Band notes.** MNS-E2 shows one Wraith that can be waited out (~20 s) or fought (30–45 s). MR-M2 is the family's quest: three standards (E1–E3) under escalating pressure, then the Colour. MBL-E5 retires the ridge's standards under the count. Wraith **standard**, bearer **sturdy**.

**Presentation rules.** Blank target frame (health bar, no name), no nameplate, no face, no colours that read as a side, no unit mark, no voiced line (C-9). No NPC calls them souls or the dead; Calwen and the crews call them "the risen".

**Defeat / loot.** Defeated at 0 HP; collapses into mud at or toward its standard. Re-forms only by its standard's condition (C-3). **No loot.** Never evidence: at MR-M1's second reading the Wraith is explicitly refused as a hold.

### 5.9 Earthen Echoes (high; earth-memory)

**Author truth (bible §2.4, §2.6).** Mud figures that repeat motions (a man bracing a pole, a woman hauling a rope, someone kneeling, lifting a pail). Not ghosts, never undead, never identify anyone. They collapse into mud when struck and re-form while their **condition** lasts: the grey on the Blackwater (MRC), a disturbed camp (MMR), an unfinished mourning ring (MLL), the ridge's count while the Bannerline circle is open (MBL).

**AI role.** Slow, relentless walkers along a straight line or lane, toward a target the place gives them (the boat's gunwale, a survey string, the speaking Haddow, a lane segment). Files move only in lanes and only on the count.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Echo** | Stands up out of mud and walks its line repeating its motion; swings when it reaches something | **Stand-up:** a hump of mud rises and holds (**1.5 s**; a ranged shot during the hold is a free hit). **Swing:** stops, both arms lift dripping mud (**1.2 s**), then a 2 m downward swing (moderate; **no knockback**†, §13 I-6). MLL: a swing that sweeps a carried or set lantern knocks it out (relight). MRC: two mud hands on the gunwale halt the ride while any Echo is at the boat (presentation, no damage) | Strike the hump; step out of the swing; clear the gunwale | Competent–Advanced |
| **File** | A line of 3 echoes (2 in the weak practice form) that moves one lane segment per third beat and strikes its own segment on arrival | Arms rise on **beat 2** (~1.2 s) before each step; in the General's P3, on **beat 1**† (C-7). Arrival strike: moderate damage, **1 s knockdown**. MMR-E2 (no count): the ground ripples on each step and the file thrusts on its third step (**1.0 s** wind-up, 3 m line, moderate) | Be out of the file's next segment on two; or defeat all its echoes (it re-forms at its lane head on the next third beat while the condition lasts) | Competent (MMR preview)–Advanced |
| **The General Who Wouldn't Fall** (boss) | §7.1 | §7.1 | §7.1 | Advanced, MBL-E6; post-arc MW-01 `[MD-8]` |

**Band notes.** MLL-E2 and MMR teach that Echoes come back by place; MRC-E2 teaches them from the boat; MBL teaches the count with a weak file (MBL-E1 cannot drop the player below 70% HP), then uses files as the region's capstone pressure. Echo **fragile**, file **standard** per echo.

**Presentation rules.** Blank target frame, no nameplate, face, unit mark or colours; no voiced line (Act II §A7; C-9). Belief barks ("the drowned getting up") are answered only by Rowan's "Mud." Nobody treats the Echoes as people.

**Defeat / loot.** Defeated at 0 HP; collapses into mud. Re-forms only by condition (C-3). **No loot.** Never evidence.

---

## 6. Fauna combat behaviour (Hunting fauna and vermin; not counted)

| Animal | Default role | Provoked / scripted state | Telegraph | Counter | Appears |
|---|---|---|---|---|---|
| **Silt Crawlers** | Passive (buried in silt) | **Stirred** by the Chapel draining: burst from fresh silt near the player and close. **Hard front shell** (reduced damage from the front; full from sides and back) | **Burst:** silt bubbles in a line toward the player (**1.5 s**), then it erupts at the line's end. **Pinch:** shell clatters, claws rise (**1.0 s**), then a pinch (moderate). **Turn:** a visible shuffle (**1.5 s**) to face a player who steps round | Step off the burst line; step round for the flank (melee) or reposition for an angle (Ranged). If directional armour is not built, the shell is replaced by more health (§9.4 R-9) | MCS-E2, MCS-E3 (stirred); otherwise Passive Hunting fauna |
| **Fenny does** | Passive grazers | **Warning tell:** lift heads together, freeze ~1 s, bolt away from a disturbance 4–6 s before Echoes stand (MMR) | — | Read the warning | MMR (every disturbance); Drowned Encampment ambient |
| **Fen fowl** | Passive | Hunting interaction only (shoot or net from Hob's hide; retrieve from the shallows) | — | — | MRS, MFT |
| **Mire boars** | Passive | Aggressive only if struck or cornered; defeated at 0 HP like any creature | Head down, front-foot paw (**1.5 s**), then a short charge | Sidestep | Marshfall Edge ambient |
| **Tarnish serpents** | Passive, bask on iron soil (MDS06) | Bite only if stepped on or struck | Coil lifts (**1.0 s**), strike | Step off the red ground | Iron Bend and crown of Bannerline; Rust Hollow edges |
| **Marrow herons** | Passive scenery | Never hostile | — | — | Meres, fords (MFW roost) |
| **Marsh Rats** | Ambient vermin | Never a pocket | — | — | Settlement edges |

**Rules.** Fauna in a fight are defeated at 0 HP (CDR-1); none flees on health. The does' bolt is a **warning presentation outside combat** (they are never engaged), not a health retreat. Quest-spawned fauna (MRS fowl, MCS crawlers) is one instance per player. Hunting yields come only through Hunting interactions or harvest after defeat, per the economy pass.

---

## 7. Bosses, minibosses and elite (consolidated)

### 7.1 The General Who Wouldn't Fall — Act III boss (MR-M5, `MBL-E6`)

Source: Act III §7, §7.1 (committed); bible §10.1. Summary for creature building; **the Act III spec is authoritative** and this table matches it (canonical values C-7, C-11).

| Field | Spec |
|---|---|
| What it is | The field's command, fear and obedience pressed into one coherent imprint when the last Memorywardens grounded the battle (FT-02c, C15). It repeats the pressure and form of command ("Hold." "Close up." "No one leaves."). Not a returned commander. Names no unit, battle, person, place or date; answers no question (Hewin's included). No Memorykeeper or Tender calls it a ghost. |
| Read | ~2.5× human height; peat, old iron (blades, stakes, buckles) and banner rags; an outline that never settles (a crest, a pole, shoulders, a cloak that is a flag); a standard pole with no readable cloth; a layered voice like several people saying one word; no face. |
| Arena | The crown of Bannerline (C2–C4), ~30 × 35 m (zone tune): the **muster post** (anchor), the palisade arc above (solid), **three lanes** (Stake, Post, Ring; ~3 m wide, four segments each) separated by ~4 m **turf strips** (safe from files, not from the General), the **twelve-stone circle** below (outside the arena: the General never enters the ring). Night; lanterns on the palisade stakes and at the road stone. No fall possible. **Leash:** if no player has been inside the arena for ~5 s, it returns to the post and its health returns to the top of the current phase (removes the ring as a safe firing position without a new rule). |
| **The count** | Beat 1 and 2: soft thud, thin ripple from the post. Beat 3: deep thud, heavy ripple down all lanes. **1.2 s per beat** (P1–P2), **0.9 s** (P3). On three, files step, the order is spoken (captioned), and any attack shown on beat 2 lands. **Move on two.** |
| **Files** | Form at lane heads on a third beat; arms rise on beat 2 (beat 1 in P3, C-7); arrival strike moderate + 1 s knockdown in the segment. Counter: out of the next segment by three, or defeat the file. |
| **Hold** (P1 shield) | Mud plates across its front, clods spraying when struck; while any file holds a lane, damage to it is heavily reduced (GD; suggested 80%). With no file standing, the plates slough off for ~4 counts (~14 s). |
| **Planted Standard** (all) | Beat 2 (beat 1 in P3): lifts the pole high, ~5 m ring decal at its feet. Beat 3: drives it down; heavy damage + knockback in the ring. Counter: out of the ring on two. |
| **Close up** (P2) | Beat 1: mud ridges along the edges of the targeted player's lane or strip. Beat 2: steps into that lane's head, lowers the pole. Beat 3: sweep down the whole lane (heavy, **~35% max HP**, the one sanctioned exception to the 30% cap, shown ~2.4 s ahead), except within ~2 m of its flanks ("inside the turn"). Counter: change lane on two (Ranged) or step inside the turn (melee). |
| **Converge** (P2) | Files in other lanes turn their heads toward the targeted lane on beat 2; on 3 they step diagonally toward it. Turf strips stay safe from files. |
| **No one leaves** (P3) | Banner rags thicken at the arena edge (visual only; no wall, no damage). Count quickens to 0.9 s per beat; every P3 attack is shown on beat 1 (~1.8 s ahead). Strikes leave 3 m mud patches: **standard slow 30%, 3 s**, lasting two counts. One file only (Post Lane). |
| Phases | **P1 "Hold"** 100–65% → re-muster at the post (~8 s, invulnerable; the asker beat plays, sets `MBL_ASKER`) → **P2 "Close up"** 65–30% → plants at the Post Lane head → **P3 "No one leaves"** 30–0%. |
| Defeat | **0 HP**: collapses into the ground; its mud slides down the Post Lane into the gap; the count continues softer (the condition, the open circle, is still there). `S05_general` completes on defeat + `MBL-D6.20`. It would re-form at the next night while the circle stands open, which is why the rite (`S06_circle`) follows at once. After `S06`, the story General does not re-form. |
| Targets | Solo **6–8 min**, Advanced identity with cooked food; a player who moves on two ends at 30–60% HP. No single hit above 30% max HP except the in-lane sweep (~35%). |
| Ranged parity | P1: files walk every lane, so ranged players still cross and clear them. P2: the sweep covers a whole lane, so lane ends are not safe. Leash removes the ring. Neither style has a spot it cannot reach. |
| Death / logout / co-op | Wake at Griefwatch's vigil hall with the quest Active; a warden walks the player back to the palisade checkpoint; fight resets to the **top of the phase died in** (100 / 65 / 30%). Logout restarts at 100%. Shared boss for partners on `S05`; health scales; Close up rotates targets; the asker beat is resolved by whichever partner acts first (fallback: host). |
| Loot | No loot that identifies anything. **No battlefield iron** (MD-11, §13 I-21): any drop is an ordinary non-metal material set by the economy pass. |
| Presentation | **Boss health bar with no name shown** (C-9; §14 Q4). The captioned orders are its only words. |
| Night Count `[MD-8]` | Post-story, struck from the muster post at night: §11.3 MW-01. |

### 7.2 The Risen Colour — miniboss phenomenon (MR-M2, `MBR-E5`)

Source: Act I §B6 Beat 5, §B7 (committed). **Design name only: never shown in UI, never said in dialogue.**

| Field | Spec |
|---|---|
| What it is | The standard at the field's centre (turnout platform, N5) and the Wraith that holds its ground. Banner Wraith family; the family's elite slot. |
| Arena | The turnout platform at dusk; black water beside it (non-walkable); the road behind (respawn at the causeway head N6). |
| Escort | 2 bearers, 2 wraiths at start; **after the lift begins, 1 wraith per pulse** until the standard is folded. Cap: 5 standing at once. |
| **Pulse** (the standard) | Cloth cracks out stiff, a ripple runs through the mud from its foot (**3.0 s**); every ~30 s (Act I `S05_colour` note). Re-forms defeated members, and the Colour itself if the standard still stands. |
| **Dip** | Lowers its standard-shape forward (**1.5 s**), then a wide sweeping arc in front (heavy). Counter: behind or to the side. |
| **Advance** | Plants and rears its pole-shape upright (**2.0 s**, cloth cracks), then strides four paces down its lane striking anything in it (heavy, push one step along the lane toward the road, never toward the black water). Counter: step out of the lane; punish the stand after. |
| **Rally** (below half, once per life) | Raises the shape high (**2.5 s**); if not interrupted, re-forms any defeated bearer at once. Any hit interrupts. |
| Bearer / wraith | As §5.8. |
| End | The quest ends the fight by **condition plus defeat**: lift (3 segments) + fold (3 correct) stops new forming; every enemy still standing fights on to **0 HP** (no enemy is "cleared" by the condition ending). `S05_colour` completes on lift + fold + all on the platform defeated. |
| Targets | 3–4.5 min including the lift and fold; ends at 40–60% HP. |
| Persistence | Death: respawn at the causeway head; step stays at dusk on return (re-pinned); lift and fold progress kept; the Colour and escort reset to full (ordinary leash reset). |
| Co-op | Shared fight. The pulse follows the host's standard state; each partner's lift and fold progress is their own. |
| Rules | Blank target frame; no nameplate, face, side colours or unit mark; no voice. Melee or ranged: the road gives ranged length, and the pulse brings back whatever was out-ranged, so kiting is valid and bounded. |

### 7.3 The Rust Hart — side miniboss (MRH, `MRH-E1` + `MRH-E2`)

Source: Settlements and Combat MRH.7.1 (working tree 2026-11-09, including the review fix for patch regrowth).

| Field | Spec |
|---|---|
| Read | A huge iron-grey stag, flanks streaked rust-red, antlers stained black at the base and rust at the tips, wide as a cart; moves in jerks. An animal. |
| Arena | The Hollow's heart (H6): a red bowl with **five ironbloom patches** (deep rust, rust, orange, orange, pale), **stumps** for cover (a charge into a stump staggers it 2 s), old iron half in the peat (inspectable, never collectable). Stump-line vault is an optional shortcut with a walkable fallback. Fog drifts in and out. |
| Pre-fight | `S01_path` to `S04_wait` (tracking): the player reads four stop sites (sign + fungus), predicts the unvisited deep-rust patch, and waits downwind at dusk. The fight starts with the strange moment (MRH.8): the Hart arrives, licks, looks, stamps. |
| **The stop** (core) | Runs to the **nearest thick patch** (deep rust or rust), stops, licks (**2.5 s**, completely still: the heavy-hit window), then fixes on the nearest two-legged target. A patch thins to orange after two licks (visible colour change). When no thick patch is left, the first-thinned patch darkens back to rust (the loop never runs dry). |
| **Charge** (all) | After every stop: head up, **two forefoot stamps** throwing red dust (**1.5 s**†), then a straight charge across the bowl; heavy + knockdown. Behind a stump: it hits the stump, 2 s stagger. |
| **Erratic run** (all) | Zigzags at speed between stops; contact deals moderate damage; destination is always the nearest thick patch. |
| **Antler rake** (P2, ≤70%) | At a stop, instead of licking, rakes the patch (**1.6 s**, head swinging low): a clearly bounded rust-coloured **spore cloud** fills the patch for 8 s; standing in it applies **standard damage over time** (the same poison/DoT status as MCF, presented as spores; C-6). |
| **Bellow** (P2, at 50%) | Head up, neck stretched, breath plume (**2.0 s**); two stalkers (**MRH-E2**) come out of the fog from the Hollow's edge (stamp 1.5 s†, charge). Interrupting the bellow is not offered (it is a phase transition, not a buff). |
| **Iron run** (P3, <25%) | Lick shortens to **1.5 s**; after each charge it runs straight to the next patch with no zigzag. |
| Phases | P1 100–70%; P2 70–25% (rake from 70%, bellow at 50%); P3 <25%. No enrage. |
| End | At **0 HP** it goes down on the red ground. `S06_antlers`: Hunting harvest (~3 s) or Annot does it; antler-base inspect (the old arrowhead); `MRH_ANTLER` choice. |
| Targets | 3–4 min, Competent identity upper end (MRS-level Hunting gate ~[GD: low-mid] on accept). |
| Ranged / melee | Ranged shoots during the lick and from behind stumps; the charge closes any distance. Melee stands on the patch it will stop at. Neither trivialises it. |
| Reset / co-op | Leaving H6 or dying resets it to full; stop sites read earlier stay read; patches regrow. Respawn at Annot's blind. Shared creature; charges target the nearest two-legged player. |

### 7.4 The Mud-Boss — elite (MNK, `MNK-E3`)

Source: Settlements and Combat MNK.7.1 (working tree 2026-11-09, including the review fix for the mudcutter mounds).

| Ability | Telegraph | Effect | Counter |
|---|---|---|---|
| Read | A big man in a coat of dried mud plates over oilcloth; a long hooked stake-puller and a short blade. Human. | — | — |
| **Hook pull** (all) | Sets the hook low and leans back (**1.5 s**†) | Straight pull that drags a player within 5 m toward him, ending in the island-edge shallows (slow on landing); never into deep water | Step out of the 5 m line or behind a pole-frame upright |
| **Mud plate** (below each third: ~66% and ~33%) | Wades into the shallows, kneels and scoops mud onto his chest (**2.0 s**) | A frontal damage-reduction plate (wet grey plates; uses the same conditional damage-reduction buff as the General's Hold, §9.4) | Any hit during the recoat interrupts it, melee or ranged |
| **Call** (at 60%) | Shouts once (**1.0 s**) | E3's two mudcutters still lying as edge mounds rise; if both already rose (a player waded within ~6 m) or were defeated, nothing comes | Clear the mounds early, or be ready |
| **Sweep** (below 30%) | Pole held level and drawn back (**1.6 s**) | Full-circle swing: knockdown inside 4 m; cadence ~10 s | Leave 4 m on the draw |
| Arena | The reed island (N4): dry centre, shallow edges (slow), reed screen, two pole-frame uprights (cover against any surviving slinger) | — | — |
| Defeat | At **0 HP** he falls; ordinary defeat presentation. Halsey from the bank: "That's the last of them." No dialogue after defeat; nothing he carries is evidence | — | — |
| Reset | Leaving the island resets him and any living mudcutters (mounds re-lie); E1/E2 stay defeated. He is leashed to the island: if no player has been on it for ~5 s he resets, so the banks across the water are not a firing position (same rule as the General's ring). Respawn at Halsey's post | — | — |
| Target | 2.5–3.5 min with 2 mudcutters | — | — |

---

## 8. Defeat (CDR-1)

**Rule.** Every Mire enemy, human (Mud-Clad Raiders, the Mud-Boss, Rootshadow Cutters, Hollowfoot `[MD-7]`), animal (Bog Hounds, Reedlurkers, Griefbit Beetles, Tarnish Stalkers, the Rust Hart, stirred fauna) or earth-memory (Banner Wraiths, the Risen Colour, Earthen Echoes, files, the General), fights until defeated at **0 HP**. No health threshold ends a fight early; nothing yields, kneels, breaks off, scatters, flees, is driven off or limps away because of its health. **Leash/reset** stays standard RPG behaviour. Earth-memory enemies **re-form while their condition lasts** (a place rule, §10). XP, loot and co-op credit are awarded at defeat. Every step that completes on a fight completes **on defeat** (`MBL-E6 defeated (0 HP)`, `MRH Rust Hart defeated (0 HP)`, `MNK-E3 defeated`, and so on).

**No Mire exception.** The Mire registers no scripted surrender, mercy or survival outcome (bible §3; CDR rulings §4 lists SX-1 to SX-3 only, none in the Mire). No quest on-defeat hook plays an alternative presentation for a Mire creature.

**Defeated humans.** Ordinary defeat presentation: the enemy falls and fades after the standard corpse time, with ordinary loot (§12). No tied or bound props, no downed state, no dialogue with a defeated enemy, no ally comment on mercy. One short, sober ally line is enough (Halsey's "That's the last of them.").

**Earth-memory defeat presentation.** The figure collapses into mud (Wraiths toward their standard; the General down the Post Lane into the gap). It leaves no body, no loot and no inspectable object.

**Non-combatants (never targetable; no attack resolves on them).** Gethin Scarth (MCF go-between), Oswin Garvey, every claimant and witness, Calwen, Mara, Corra, Dunstan, Edris, Lysa, the Haddows and Prue (MLL), Lenna (MMR), Ned (MSG), Halsey and Annot, Hob (stops at the Hide's edge), Jory Wick and every settled Hollowfoot at Fenward and Griefwatch, every child (MLD), Hewin, Ysolde and every circle attendee. **Allies** in MBL (Marshwardens, the Thornfell Ridge Warden pair with `TH_STANDING`, the Bannerbearers) fight beside the player and are **standard invulnerable ally NPCs** (never defeated).

**MLL protection rule (not a health rule).** An Echo that reaches a speaking Haddow stops and repeats its motion beside them; the speaker pauses (progress paused, not lost) until the player clears it. No speaker can be harmed.

**Runtime need (Systems Engineer).** None beyond standard defeat at 0 HP and the drift-site re-form model (§10, §9.4 R-1). No yield event, CombatIncapacitated use, hostile-to-neutral swap or quest on-defeat surrender hook is needed for any Mire creature. Ordinary "on defeat" step triggers (MNK `S03_boss`, MRH `S05_fight`, MBL `S05_general`) use the standard quest event for a named creature's defeat, which Thornfell and Lowmark already require.

---

## 9. Hazard register

Hazards are environmental. They have no health, no target frame and no AI. All obey C-2: **cannot kill a player above 25% HP**, never move anyone into deep water, and deep water is a hard non-walkable edge.

### 9.1 Water, ground and route hazards

| Id | Hazard | Where | Tell | Effect | Safe space | Source |
|---|---|---|---|---|---|---|
| **MNS-H1** [NEW id] | Running or Sour shallows | Every crossing off-state (C1, C4, C6 in MR-M1; all crossings by schedule) | Stake water at pale (Running) or black band / stake leaning (Sour) | **Non-walkable**; the player stops at the edge with a bark; no damage | Wait (keep watch) for Slack | Act I §A7; bible §9.2 |
| **MNS-H2** [NEW id] | Ditch shallows | Along the Standards Causeway | Reed-fringed water beside the logs | Walkable, **standard slow** while wading; no drowning | The road | Act I §A7, §B7 |
| **MNS-H3** [NEW id] | The dark line | Causeway C5, `S04_walk_back` | The cart wheel sinks | Harmless stop; a two-segment heave | — | Act I §A7 |
| **MBR-H1** [NEW id] | Loose logs | Causeway where a pole has come out | Logs shift underfoot | Walkable, standard slow, until pinned | Pinned logs | Act I §B7 |
| **MBR-H2** [NEW id] | The black water | Beside the turnout platform (N5) | Black, still surface | Non-walkable | The platform | Act I §B7 |
| **MRS-H1** | Deep water | Mere beyond the retrieve marker | Water darkens past a line of reed floats | Non-walkable boundary | The shallows | Work MRS.6 |
| **MFH-H1** | Mud at the punt | Blackwater Landing H1 at Slack/Sour | Wet mud sheen | Slow zone; no damage | The plank row | Work MFH.6 |
| **MWS-H1** | Sunk planks | Marshfall row P3 before `S02` | Planks dip into water | Slow zone | Driven piles | Work MWS.5 |
| **MFT-H1** [NEW id] | Flood stage | Fenward hut floors (W5) | Water at the step | Presentation slow on hut floors; no damage | Shelf slots | Work MFT.6 |
| **MHG-H1** [NEW id] | Under the store at Running | Hushed Granary stilts | Water over the ladder foot | Non-walkable; the hatch step pins Slack on keep watch | — | Work MHG.5 |
| **MNK-H1** [NEW id] | Island-edge shallows | Nine Stakes reed island (N4) | Mud lip, reed screen | Walkable slow (also where the Hook pull lands) | Dry centre | Settlements MNK.7.1 |
| **MSG-H1** [NEW id] | Trench gust | The Singing Trench bays | Reeds above flatten and a rising whistle (**~3 s**) | During a gust, vent planks are pinned by the draft (cannot be worked); **no damage, no push** | Wait for the lull | Cloth MSG Beat 1–3, MSG.11 |
| **MCF-H1** [NEW id] | Frame cut (cutter-triggered prop) | Reed Hide stripping frames (MCF-E2) | Rope creaks as a cutter slashes a lashing (**1.5 s**†) | A bare pole swings down along a 2 m line, moderate damage. **Fallback:** remove; E2 gets one more cutter (MCF.11) | Out of the pole's line | Cloth MCF.6 |
| **MCS (water stages)** | Chapel nave water | The Sunken Chapel, stages 0–3 `[MD-4]` | Water line at each stage | Deep water non-walkable at every stage; walkable ground grows as each sluice board drops the nave | Lit, dry ground | Act II §B7, bible N-3 |

### 9.2 The Chapel: Shades and the draught `[MD-4]` (light-gated hazards; never creatures)

| Field | Spec |
|---|---|
| Ids | **MCS-H1** Chapel Shades (all dark ground inside the chapel, `S02`–`S06`); **MCS-H2** the draught (`S06_out`) |
| What Shades are | Impressions in the dark of the Sunken Chapel (C15): thickening dark at the edge of the player's light. **A hazard, not a combat family.** No HP, untargetable, no name, no face, no voice, no unit mark, no word. No NPC calls them souls or ghosts; Mabyn calls them "the press" or "the shades", "only dark that's heavy". Enemies are not affected by Shades. |
| Dark ground | Walkable ground outside every lit post's radius (**~6 m**). After **~6 s** continuous in dark ground (`S06`: ~3 s), Shades form at the edge of the hand lantern's light. |
| Hand lantern | Mabyn's carry-state lantern with three looks (**bright** ~3 m radius, **low**, **ember**): presentation of one dark-ground timer (presses 0–2). No meter, no bar, no fuel, no stored light stat; the timer resets on entering a lit post's radius (flame recovers over ~2 s). A log line on each change. |
| **Lean → press** | Tell: the flame leans away from the thickest dark and the light shrinks (**~2 s**). Press: the lantern drops one state. Every **~4 s** in dark ground (`S06`: ~2 s). |
| **Push** | At ember, the next press pushes the player back to the nearest lit post: edges dim, the player staggers (~2 s, no control), then stands in the post's light. **No damage.** |
| **The draught (MCS-H2)** | After the crypt is opened, each post gutters **once**, in a wave from the floor upward: gutter tell (**1.5 s**, flame shrinks and smokes) then out. Shades form faster (~3 s) and press more often (~2 s). Relight a guttered post (~2 s) or run between lit ones. 2–3 min. |
| Fights in the light | Every MCS encounter spawns at or next to lit ground once its stage's first post is lit; a player can always draw enemies into light. |
| Death / co-op | Respawn in Mabyn's loft (before `S02`) or at the gallery post (after); water stage, boards, lit posts and reads persist; Shades reset; in `S06` relit posts stay lit. Water stage follows the **host** for all present. |
| Rules | Never anywhere but inside the Sunken Chapel. Never used to date, identify or prove anything. Bible N-2 (light-gated hazard volumes) with the fallback of pre-authored lit/dark zones flipped at each drainage stage. |

### 9.3 Bannerline hazards (MR-M5)

| Id | Hazard | Where | Tell | Effect | Source |
|---|---|---|---|---|---|
| **MBL-H1** [NEW id] | The third beat | Any lane, `S02`–`S06` | Beat 2 (~1.2 s; beat 1 in P3) | The count itself never damages; only things in a file's segment or an attack's decal are hit | Act III §7.2 |
| **MBL-H2** [NEW id] | Mud patches | Crown, P3 only | A patch appears where a strike lands | Standard slow 30% for 3 s; lasts two counts | Act III §7.2 |
| **MBL-H3** [NEW id] | Gap step-off | The circle's gap, `S06_circle` | Gap ripple brightens on beat 2 of an arrival count (~1.2 s) | ~15% max HP and knockback (back toward the gap stone, never down the slope) if held through beat 3; never costs rite progress | Act III §7.2 |
| **MBL-H4** [NEW id] | Iron soil | The Iron Bend, the crown | Red ground | None; tarnish serpents bask here (fauna, §6) | Act III §7.2 |
| — | Dark | The road and crown at night | — | None; lanterns at each held bend and on the palisade. **No light-gated mechanics on Bannerline** (those are the Chapel's) | Act III §7.2 |

### 9.4 Status and runtime needs (documented dependencies; nothing implemented)

CDR-4 test: every row says whether the need is **standard** (already required by Lowmark or Thornfell, or ordinary RPG) or **new**. Only R-12 to R-14 are new to the Mire, and two of them come from the bible's own §11.2 with fallbacks. Avoided needs are listed at the end.

| # | Need | Used by | Status | Recommendation |
|---|---|---|---|---|
| R-1 | **Re-form by condition** (spawn point + condition flag + re-form trigger: timer, pulse event or beat event) | Wraiths, the Colour, Echoes, files, the General | Standard (Lowmark drift-site model; Thornfell lane re-form) | One state model: each earth-memory spawn point reads a condition (standard risen, ring unfinished, grey pinned, stake standing, circle open) and a re-form trigger (C-3) |
| R-2 | **Push / pull toward a defined safe side**, clamped so no deep-water edge is crossed | Wraith press, Colour Advance, carapace butt, Planted Standard, Mud-Boss hook pull (a pull is a push with the source as direction), gap step-off, Shade push | Standard (Thornfell push-to-safe-side) | Direction source (volume tag or source position) + edge clamp |
| R-3 | **Knockdown** (timed movement block) | File arrival (1 s), Hart and stalker charge, Mud-Boss sweep | Standard (Lowmark I-18 / Thornfell §9.4) | Same ruling |
| R-4 | **Slow** | Ditch shallows, loose logs, island shallows, snapper slick, General mud patches (30%, 3 s) | Standard | One slow status; durations per source |
| R-5 | **Root** (short hold, breakable by attacking the holder) | Lurker grab, snapper clamp (1.5 s) | Standard | One root status with an optional "break on hit to source" flag |
| R-6 | **Poison / damage over time** with ordinary antidote | Poisoner blades; the Hart's spore cloud (same status, spore presentation) | Standard (canon poisons; MCF.11 "standard status effect") | One DoT status; the spore cloud is a bounded ground volume that applies it |
| R-7 | **Ally attack-speed buff on an interruptible wind-up** | Bearer Raise (8 m, 10 s) | Standard (Thornfell hornman Gather) | Same buff and interruptible-windup flag |
| R-8 | **Conditional damage reduction** | General's Hold (while any file stands), Mud-Boss mud plate (until broken by damage or the next phase) | Standard buff with a condition | One damage-reduction buff whose removal is driven by an encounter condition |
| R-9 | **Directional armour** (reduced damage from the front) | Silt Crawler shell | **Optional** | If not available, replace with more health and keep the slow turn as presentation (§6). Not built for the Mire alone |
| R-10 | **Hazard clamp** (cannot reduce below 25%) | Every hazard (§9.1, §9.3) | Standard (Thornfell C-2) | One clamp parameter |
| R-11 | **Invulnerable ally NPCs; untargetable non-combatants** | MBL allies; every non-combatant | Standard | — |
| R-12 | **The count**: a boss-timeline beat event (beat index 1/2/3, tempo per phase) that listeners read | General, files, MBL bearers, gap step-off, ripple decals, caption and rumble | **New (Mire), smallest form** | A scripted encounter metronome broadcasting `count_beat(n)`; every listener schedules its tell on beat 1 or 2 and its hit on 3. This is ordinary boss scripting; it is listed because several systems read it |
| R-13 | **Light-gated hazard volumes** (bible N-2) | Chapel Shades, the draught | **New (bible §11.2)** | Spawn gating by a lantern post's lit state (~6 m) + the dark-ground timer on the carried lantern + a scripted push to the nearest lit post. **Fallback:** pre-authored lit/dark zones flipped at each drainage stage |
| R-14 | **Channel-state schedule** (bible N-1) | Every encounter on a crossing (MNK, MNS, MBR shallows, MRS, MFH) | **New (bible §11.2)**, not combat-specific | Per-crossing state table keyed to the presentation hour. **Fallback:** quest-pinned states per step |

**Avoided (not needed; do not build for the Mire):** **bleed** (gnawer; §13 I-8), **blind** (reed-slinger clod; I-8), facing-based armour unless R-9 already exists elsewhere, any breath or air meter, swimming, drowning, per-tile mud physics, a gear-brightness visibility system for Hollowfoot, a yield or surrender event, a hostile-to-neutral swap, a tide simulation, a fear meter for Griefbit adds (C-12 uses a timer and the existing calm dialogue event).

---

## 10. Earth-memory rules and re-form sites

### 10.1 Binding rules (bible §2.4, §2.6, §11.3)

1. **Earth-memory never identifies anyone.** No nameplate, no name, no face, no side colours, no unit or clan mark, no voiced identity. Target frames are blank (C-9). No UI, NPC, bark, inspect or document names a Wraith, Echo or the General after a real person, unit or side. Belief barks are answered only by plain words ("Mud.").
2. **They prove nothing.** No hold, register entry or choice rests on a Wraith, an Echo, the General, a Shade, the glass or the moss. At MR-M1's second reading the Wraith is explicitly refused as a hold.
3. **Combat disperses, conditions decide.** Striking collapses a figure; it re-forms while its condition lasts (C-3) and stops forming when the condition ends; those still standing fight on to 0 HP. No quest cures earth-memory by combat.
4. **Bounded to their places.** Wraiths only at risen standards; Echoes only at their condition sites; Shades only inside the Chapel; the General only on Bannerline. Never in a settlement interior.
5. **Readable and slow.** Wraiths walk lanes; Echoes walk straight lines; files move only on the count. Out-ranging them never ends a fight on its own, because they re-form; the place's condition does.
6. **No loot from earth-memory.** Ever.

### 10.2 Re-form sites

| Site | Place | Condition (re-forms while…) | Re-form trigger in an active encounter | Ends when | State after |
|---|---|---|---|---|---|
| `wraith.roadside_c2` | Causeway C2 roadside works (MP08) | The crew's standard stands risen (MR-M1) | At the next dusk, at the standard (it walks its pass repeatedly until struck) | MR-M2 lifts and folds it (`MR_CAUSEWAY = reset`) | Quiet after MR-M2 |
| `wraith.causeway_std1–3` | Causeway standards 1–3 (MP08) | Standard risen and unfolded | Forming tell 3.0 s at the standard, after a defeated Wraith's collapse | Third correct fold of that standard | Folded; quiet |
| `wraith.turnout_colour` | Turnout platform N5 (MP07) | Standard risen and unfolded | The **pulse** (~30 s) re-forms defeated members and the Colour | Lift + fold | Quiet; `MR_BANNERS` decides the field's props |
| `wraith.palisade_std1–3` | Palisade heads C1 (MP12) | Standard risen | On a third beat, near the freed pole | Fold of that standard | Quiet |
| `echo.encampment_cut` | Drowned Encampment cut C3 (MP09), from the boat | The grey (pinned `[MD-3]`) and the boat in that stretch | **~10 s** after defeat (boat-pacing value, kept) | The boat leaves the stretch | Quest-local |
| `echo.encampment_survey` | Drowned Encampment landward side (MP09) | Lenna's survey stakes standing (the disturbance) | **6 s** (C-3 default) | All six stakes pulled (`S04_stakes`) | Quiet; strange moment plays |
| `echo.stillgrave_ring` | Stillgrave Hollow ring (MP11) | The Haddows' ring unfinished | **6 s**, at the water's edge | Dob's stake (`MLL-D4.30`): every Echo folds into mud at once | Quiet; the ring's light lies straight with `MR_LANTERN_LINE` |
| `echo.bannerline_count` | Bannerline road bends and crown (MP12, MP17) | The circle open (the ridge's count) | Next **third beat**, at the lane head | `S06_circle` completes | Ridge quiet; the Night Count is a separate, called encounter (MW-01) |

---

## 11. Encounter register by quest

**Persistence tags** (Lowmark/Thornfell set). **STEP**: spawns on step entry; gone when the step completes. **ONCE**: never respawns for that player. **→WORLD**: after its step, the area keeps an ordinary population of the same family (§11.3). **COND**: earth-memory; governed by §10.2. **OPT**: optional pocket. Solo targets are the package values (§2 targets apply where none is given). All POIs are bible §4.2 ids; placements are relative and **MAP VERIFICATION REQUIRED** throughout (zones package).

### 11.1 Main quests (committed packages)

| Id | Step | Place (POI) | Families / variants | Band | Solo target | Persistence / respawn | Source |
|---|---|---|---|---|---|---|---|
| MNS-E1 | `S02b_station` | Edris's old station on the causeway (MP08) | W1: 2 swarm, 1 carapace (+1 swarm fear add after ~40 s unless Edris has calmed the man); W2: 1 swarm, 1 carapace | Competent | 60–90 s; 60–80% HP | ONCE (defeated beetles stay defeated). Respawn: Edris's station | Act I §A7 |
| MNS-E2 | `S04_walk_back` | Roadside works C2, night (MP08) | 1 wraith (fight or wait out, `MNS_WRAITH`) | Competent | 30–45 s fought; ~20 s to wait out | COND (`wraith.roadside_c2`). Respawn: last stake passed, cart waiting | Act I §A7 |
| MBR-E1 | `S03_standards` (std 1) | Causeway standard 1, road (MP08) | 2 wraith | Competent (late) | 60–90 s lift to fold; 60–80% HP | COND until folded. Respawn: causeway head N6; folds, pins, segments kept | Act I §B7 |
| MBR-E2 | `S03_standards` (std 2) | Standard 2 (MP08) | 2 wraith, 1 bearer | Competent (late) | 90–120 s; 50–70% HP | COND | Act I §B7 |
| MBR-E3 | `S03_standards` (std 3) | Standard 3, embankment slope (MP08) | 3 wraith, 1 bearer | Competent (late) | 100–140 s; 50–70% HP | COND | Act I §B7 |
| MBR-E4 | `S04_chest` | Ditch at the embankment foot (MP07/MP08 edge) | 2 lurker, 1 snapper (kit per C-5; 1.5 s first-appearance ripple) | Competent (late) | 45–70 s | ONCE | Act I §B7 |
| MBR-E5 | `S05_colour` | Turnout platform N5, dusk (MP07) | **The Risen Colour**, 2 bearer, 2 wraith; +1 wraith per pulse until folded | Competent (late) | 3–4.5 min; 40–60% HP | COND (`wraith.turnout_colour`); step re-pins dusk | Act I §B7, §7.2 here |
| MRC-E1 | `S02_prepare` (moss task; skipped by the crew alternative `MRC_MOSS_CREW`) | Stillgrave's near edge, stilt-stump shallows S2, night (MP11) | 2 lurker, 1 snapper | Advanced | 60–90 s; 65–80% HP | ONCE. Respawn: Blackwater Landing (moss kept) | Act II §A7 |
| MRC-E2 | `S05_crossing` `[MD-3]` | Drowned Encampment cut C3, from the boat (MP09) | Echoes, 2 per bank per stretch × 3 stretches | Advanced | 2–3 min; 55–70% HP | COND (`echo.encampment_cut`); restarts at stretch 1 on death. Respawn: aboard at the last passed junction | Act II §A7 |
| MCS-E1 | `S01_roofline` | Chapel roof lower slope T2, around the two lowest posts (MP13) | 2 lurker, 1 snapper | Advanced | 60–90 s; 65–80% HP | ONCE. Respawn: Mabyn's loft | Act II §B7 |
| MCS-E2 | `S03_drain` (stage 1) `[MD-4]` | Upper aisle walk N1 (MP13) | 4 Silt Crawler, two waves of two (stirred fauna) | Advanced | 60–90 s per wave; 60–75% HP after both | ONCE. Respawn: gallery post G6 | Act II §B7 |
| MCS-E3 | `S03_drain` (stage 2) `[MD-4]` | Lower bays N2 (MP13) | 2 lurker (bay pools), 1 snapper, 2 Silt Crawler | Advanced | 2–3 min; 55–70% HP | ONCE | Act II §B7 |
| MCS-H1 | `S02`–`S06` | All dark ground in the chapel (MP13) | Chapel Shades (hazard) | Advanced | — | Hazard; resets on death | Act II §B7, §B8.1 |
| MCS-H2 | `S06_out` | Floor to hatch (MP13) | The draught (hazard) | Advanced | 2–3 min | STEP; relit posts stay lit | Act II §B7 |
| MBL-E1 | `S02_count` | Practice lane B2 by Bran's watchpost (MP17) | Weak file of 2 echoes | Advanced | Under 60 s; cannot drop the player below 70% HP | COND (re-forms on the next third beat); `S02` also completes on 3 clean counts | Act III §7 |
| MBL-E2 | `S03_road` | The Low Bend R1 (MP12 road) | 2 files of 3 (one per lane) | Advanced | 60–90 s; 75–90% HP | COND (`echo.bannerline_count`). Checkpoint: closure gate → watchpost | Act III §7 |
| **MBL-E3** `[MD-7]` OPT | `S03_road` | The Rag Bend hollow R2, below the road (MP12) | 2 Hollowfoot wanderer, 1 shouter | Advanced | 40–60 s if engaged; avoidable by keeping to the road | ONCE if fought. **MD-7 alternative:** survivor beat (sit with them, ~3 s; they walk down to the wardens' brazier and are taken to Lysa; no XP, loot or flag) | Act III §7, §14.1 |
| MBL-E4 | `S03_road` | The Iron Bend R3 (MP12) | 2 files of 3, staggered one count, across three lanes; allies hold the flank | Advanced | 90–120 s; 65–85% HP | COND. Checkpoint: Iron Bend | Act III §7 |
| MBL-E5 | `S04_standards` | Palisade heads C1 (MP12) | Per standard: 2 wraith (1st); 2 wraith + 1 bearer (2nd, 3rd); `MR_BANNERS = restored`: +2 wraith at the 3rd | Advanced | ~2–3 min for all three | COND per standard; once folded, the remainder fight to 0 HP and do not re-form. Checkpoint: palisade | Act III §7 |
| MBL-E6 | `S05_general` | The crown C2–C4 (MP12) | **The General**; files per phase | Advanced | 6–8 min; ends 30–60% HP | Phase checkpoints 100/65/30%; logout restarts 100%; after `S06` the story General does not re-form | Act III §7.1, §7.1 here |
| MBL-E7 | `S06_circle` | The lanes and the gap during the rite C3–C4 (MP12) | 1 file of 3 (Post Lane); segment 3 adds 1 file of 3 (Stake Lane) | Advanced | Rite ~6–8 min of hold in all | COND; hold progress persists through death, logout and walking away. Checkpoint: road stone C4 | Act III §7 |

**MD-7 summary for main quests.** MR-M1 to MR-M4 have **no Hollowfoot enemy** under either ruling (Act I §A7.1, §B7.1; Act II §A7, §B7). MR-M5 has one: MBL-E3, optional, off the required route, carrying nothing evidentiary. Swapping to the alternative removes the Hollowfoot creature definitions and changes no step, flag or evidence.

### 11.2 Side quests (working-tree state, 2026-11-09)

| Id | Step | Place (POI) | Families / variants | Band | Solo target | Persistence / respawn | Source |
|---|---|---|---|---|---|---|---|
| MRS-E1 | `S06_flight` (first retrieve) | Retrieve shallows F4, Fowling Meres (MP26) | 1 lurker (1.5 s first-appearance ripple; grab) | Competent | 30–45 s; low damage | ONCE (resets to its spot on death). Respawn: Hob's hide | Work MRS.6 |
| MFH-E1 | `S05_hounds` ("Defeat the dogs at the racks") | Smoke racks H3, plank row, Blackwater Landing (MP06) | 2 runner, 1 gnawer | Competent | 45–60 s | STEP (hounds reset on death). Respawn: the Tolley bench | Work MFH.6 |
| MWS-E1 | `S01_burdens` | Maddy's step P2, Marshfall row (MP02) | 2 swarm, 1 carapace (+1 swarm fear add after ~30 s while Maddy is frightened) | Competent (late) | 40–60 s | ONCE. Respawn: the row's head | Work MWS.5 |
| MLL-E1 OPT | `S02_moss` | Far posts of Stillgrave's near edge (MP11) | 2 lurker, 1 snapper (1.5 s first-appearance ripple) | Competent | 30–45 s; 70–90% HP | ONCE; avoidable by gathering near | Names MLL.6 |
| MLL-E2 | `S06_finish` | Stillgrave ring at the water's edge (MP11) | Echoes: W1 2; W2 3; W3 3 + 1 that walks to Dob's lantern | Competent | ~2.5–3.5 min; 50–70% HP | COND (`echo.stillgrave_ring`); completed speeches kept. Respawn: memorial gardens | Names MLL.6 |
| MLD-E1 OPT | `S04_walk` (fight **or** calm the child) | Ditch below the centre turnout, Standards Causeway (MP08) | 2 swarm, leashed to the ditch; never reach the road | Advanced (trivial) | 20–35 s; 80–95% HP | STEP. Calm option: the swarm stays in the ditch, never engaged (ordinary leash; no settle state; scenery, not a health outcome) | Names MLD.6 |
| MCF-E1 | `S03_mouth` | Lookout platform and reed screen, Reed Hide mouth (MP23) | 2 cutter, 1 poisoner | Competent (late)–Advanced | 40–60 s; 60–80% HP | ONCE; cleared stages kept. Respawn: Marshfall | Cloth MCF.6 |
| MCF-E2 | `S04_frames` | Stripping frames, narrow bay (MP23) | 3 cutter, 1 poisoner; frame cut (MCF-H1) | Competent (late)–Advanced | 60–80 s; 50–70% HP | ONCE | Cloth MCF.6 |
| MCF-E3 | `S05_stack` | The stack bay (MP23) | 2 cutter, 2 poisoner (alternating) | Competent (late)–Advanced | 70–100 s; 40–65% HP | ONCE | Cloth MCF.6 |
| MMR-E1 | `S01_strings` | Survey strings, Drowned Encampment landward side (MP09) | 3 echo (does bolt 4–6 s before) | Competent (late) | 40–60 s; 70–85% HP | COND (`echo.encampment_survey`) | Cloth MMR.6 |
| MMR-E2 | `S02_track` | The loop path (MP09) | 1 file (no count; thrust on its third step), 2 echo | Competent (late) | 50–70 s; 60–80% HP | COND | Cloth MMR.6 |
| MMR-E3 | `S04_stakes` | Remaining strings (MP09) | 4 echo, 2 at a time; re-form 6 s while their string's stake stands | Competent (late) | 60–90 s; 50–75% HP | COND; ends when all stakes are pulled | Cloth MMR.6 |
| MSG-E1 | `S03_hold` (lulls) | Flooded sumps, bays 1 and 3, the Singing Trench (MP19) | L1: 2 lurker; L2: 1 lurker, 1 snapper; L3: 2 lurker, 1 snapper (vent climb) | Competent | 25–40 s per lull; ends 55–75% HP | Per lull, ONCE; gust count persists. Respawn: the trench mouth | Cloth MSG.6 |
| MBO-E1 | `S05_round` | Drill furrows D1, between posts 2 and 3, the Dry Muster (MP24) | 3 runner, 1 gnawer | Competent (late) | 50–70 s | STEP (hounds reset on death; lit posts and rung turns stay). Respawn: Tibb's bench | Settlements MBO.7 |
| MNK-E1 | `S02_clear` | Near reed bed N3 west, Nine Stakes (MP21) | 2 mudcutter, 1 reed-slinger | Competent (upper) | 45–60 s | ONCE. Respawn: Halsey's post | Settlements MNK.7 |
| MNK-E2 | `S02_clear` | Far reed bed N3 east (MP21) | 1 mudcutter, 2 reed-slinger (crossfire) | Competent (upper) | 50–70 s | ONCE | Settlements MNK.7 |
| MNK-E3 | `S03_boss` | Reed island N4 (MP21) | **Mud-Boss** + 2 mudcutter (edge mounds; rise on the Call or on approach) | Competent (upper) | 2.5–3.5 min | ONCE; leaving the island resets him and living mudcutters | Settlements MNK.7.1, §7.4 here |
| MRH-E1 | `S05_fight` | The Hollow's heart H6, the Rust Hollow (MP27) | **The Rust Hart** | Competent (upper) | 3–4 min | ONCE; resets on leaving H6 or death. Respawn: Annot's blind | Settlements MRH.7.1, §7.3 here |
| MRH-E2 | `S05_fight` (at 50%) | From the Hollow's fog edge (MP27) | 2 stalker | Competent (upper) | — (phase pressure) | Part of MRH-E1 | Settlements MRH.7 |

**No-combat quests (checked):** MSS, MBA, MEP, MLW, MBS, MFW (the figure at the ford is never hostile and never answers), MFT (flood stage is presentation), MHG, MRW; micro-events MME01–MME10 and discoveries MDS01–MDS10 (no encounters; MDS07 is the Sorrowback **trail** only, never followed). **No Hollowfoot** appears in any side quest, micro-event or discovery (each package's MD-7 note: "no change").

### 11.3 World pockets and proposed placements [PROPOSAL — Gameplay Designer]

| Id | Place | Unlock / condition | Content | Band | Respawn |
|---|---|---|---|---|---|
| **MW-01 The Night Count** `[MD-8]` [PROPOSAL — DIRECTOR] | Bannerline crown (MP12) | After MR-M5 Completed; night (player hour); the player strikes the muster post ("Strike the post. The count will answer."). With `tended`, the vigil keeper steps off the gap first | MBL-E6 without story beats (no asker, no rite); same phases, tells and count; tuning may be raised | Post-arc | Called only; defeat at 0 HP collapses it into the post's foot and the count stops on its own (the circle is complete). Respawn: Griefwatch. `MR_BANNERLINE` changes props and lines, not access. Ordinary combat rewards; any unique drop belongs to the item pass (no battlefield iron) (Act III §E.9) |
| MW-02 Bog Hounds | Marshfall Edge peat paths; Rootrest's outer paths (MAP VERIFICATION REQUIRED) | After MR-M1 | Runner pairs, occasionally a gnawer | Competent | WORLD |
| **MW-03 Rutting stalker** | The Rust Hollow's outer patches (MP27), not H6 | After MRH Completed; dusk | 1 rutting stalker + 1–2 stalkers defending thick patches | Competent (late) / post-arc | WORLD (long timer). Places the counted but unplaced variant (§4.1); cut it to drop the count to 21 |
| MW-04 Reedlurkers | Fowling Meres edges, Stillgrave's near edge, Blackwater banks by the landing | After MR-M1 | Lurker pairs, occasional snapper | Competent–Advanced | WORLD |
| MW-05 Griefbit Beetles | Grave-wet ground at the Field's edge and the Sodden Pyres (MP20) | Any | Ambient swarms; Passive unless a fear event or the player disturbs the timber | Competent | WORLD |
| MW-06 Tarnish stalkers | The Rust Hollow (MP27), outside H6 | After MRH Completed | 1–2 stalkers | Competent (late) | WORLD |

**No world pocket, by design:** Mud-Clad Raiders (Nine Stakes is safe after MNK; the crossing tells the truth), Rootshadow Cutters (the Reed Hide is empty after MCF), Hollowfoot (never a world enemy under either MD-7 ruling), Banner Wraiths and Earthen Echoes outside a live condition (§10.2), Chapel Shades outside the Chapel, the Sorrowback (not a Mire encounter). **Never anywhere:** a Wraith at a retired or folded standard; an Echo at a site whose condition has ended; the story General after `S06`.

---

## 12. Loot and drop notes

| Rule | Detail |
|---|---|
| **No new quest items** | The Mire budget is four (`MNS_name_tape`, `MBR_unit_logs`, `MCS_warden_leaves`, `MBL_names_roll`; bible §9.4); **none comes from a creature**. The tape is carried from Mara's find, the logs from the levered chest, the leaves from under the altar, the roll from Ysolde's table. Side quests use carry-state objects and read-in-place records only. |
| **Combat drops nothing evidentiary** | No ledger, roll, tape, log, token or mark is carried by an enemy. Gethin's ledger is read at the jetty; the ferry book at Nine Stakes; the ration board in the cookhouse; the vestry log in place. |
| **Defeated humans drop ordinary loot only** | Mud-Clad Raiders, the Mud-Boss, Rootshadow Cutters, Hollowfoot `[MD-7]`: ordinary drops per the economy pass. MNK's stolen goods are ordinary loot plus Halsey's carry-state bundle. Cloth recovered in MCF is carry-state bales, never loot. Coin rewards in the packages come from NPCs, not corpses. |
| **Earth-memory drops nothing** | Wraiths, the Colour, Echoes, files: no loot. The General: ordinary non-metal material only (§7.1; §13 I-21). |
| **Battlefield metal is evidence, not feedstock** (MD-11) | Old iron in the Rust Hollow, on the Iron Bend and on the crown is inspectable and never collectable; no creature drops it. |
| **Animals** | Hides, antler, meat and feathers are economy-pass items (reed shafts, fen fowl and griefroot are proposals, not catalog items). The Rust Hart's antlers go by the `MRH_ANTLER` choice. Fen fowl come through Hunting interactions, not combat kills. |

---

## 13. Cross-package canonical register and issues

### 13.1 Shared canonical register (canonical for implementation; packages defer to it)

The Mire Batch 4 handoffs (this file, Zones, Integration) state these values in the same words. Where a quest package gives a different number or kit, the package value is superseded for implementation; the package edits in §13.3 have been applied.

| # | Topic | Canonical value |
|---|---|---|
| **C-1** | Telegraph minimums | Light ≥ 0.8 s; moderate or heavy ≥ 1.0 s; any hit ≥ 25% max HP, any displacement (push, pull, knockback, knockdown) and any instant area effect ≥ 1.5 s. Lingering ground patches (snapper slick, mud patches, spore cloud) are visible before entry and follow the tell of the attack that creates them. Charges with knockdown use **1.5 s** (stamp). |
| **C-2** | Hazards and water | No hazard can kill a player above **25% HP**. Deep or Sour water is non-walkable everywhere; no swimming, drowning or breath meter (MD-4). No push, pull or knockback can move a player into deep water, overboard, off the causeway into Sour water or off the ridge. |
| **C-3** | Defeat and re-form | Every enemy is defeated at **0 HP** (CDR-1); no Mire SX. Earth-memory re-forms only by condition, in two layers: **in an active encounter**, on the site's trigger (Echo spot timer **6 s** default; MRC-E2 keeps **~10 s** as boat pacing; Wraiths on their standard's forming tell or the Colour's **~30 s pulse**; files and MBL Wraiths on the **next third beat**); **outside an encounter**, a site whose condition still holds repopulates at the **next dusk** (Wraiths) or the next time its condition is presented (Echoes). When the condition ends, nothing new forms and anything still standing fights on to 0 HP. |
| **C-4** | Bearer | **Raise 2.0 s**; Wraiths within **8 m** attack faster for **10 s**; any hit during the raise cancels it. In MBL-E5 the bearer also has **Plant** on the count (3 m ring, decal from beat 1). |
| **C-5** | Reedlurkers | **Lurker** lunges (reed-ripple **1.2 s**; **1.5 s** in MRS-E1, MLL-E1 and MBR-E4) and may grab (root 1.5 s, broken by attacking it). **Snapper** spits from deeper water (**1.0 s**; slowing slick) and clamps in melee (**1.0 s**, root 1.5 s). They do not re-form. A snapper holds wadeable water only; a lurker hit from beyond its reach for ~5 s submerges and resets (no safe firing spot; §5.3). |
| **C-6** | Statuses | Standard slow (General patches 30%, 3 s; shallows while wading); root 1.5 s; knockdown 1 s (file) or per source; **standard poison/DoT** (~8 s, antidote) for poisoners and the Hart's spore cloud. **No bleed, no blind.** |
| **C-7** | The count | **1.2 s per beat** (3.6 s per count); **0.9 s** in the General's P3. Every count attack lands on a third beat and is shown on beat 2 at the latest; in P3 **every** count attack (Planted Standard, file arrival, Close up ridges) is shown on **beat 1**. The count itself never damages. Carriers: positional audio, ground ripple decal, optional rumble, optional caption. |
| **C-8** | Ranged (CDR-2) | Ranged is first-class in every fight and never required; every counter that names Ranged has a melee answer. No fight is trivialised by range: earth-memory re-forms by condition; the General's leash removes the ring; the Mud-Boss's island leash removes the banks; Reedlurkers reset when hit from beyond reach; the Hart's charge closes any distance; frames and stumps serve both styles. Every raised or water-bound enemy (snapper, slinger hummock, poisoner platform or stack) is reachable on foot. Weapon, ammunition and XP values belong to the item and systems specialists. |
| **C-9** | Earth-memory presentation | Wraiths, the Colour, Echoes and files: **blank target frame** (health bar, no name), no nameplate, face, side colours, unit mark or voice. The General: a **boss health bar with no name shown**; its captioned orders are its only words. Design names such as "the Risen Colour" never appear in UI or dialogue. |
| **C-10** | Hollowfoot `[MD-7]` | Optional, avoidable, never evidence, never the only route, never a known person, never a boss, never a world enemy; ordinary human defeat at 0 HP under the recommendation; the survivor-beat alternative (§5.7) under the other ruling. Fenward and Griefwatch Hollowfoot are always non-combatants. |
| **C-11** | Boss and miniboss framing | The General: Act III §7.1 is authoritative (phases 100/65/30%, 6–8 min, ~35% in-lane sweep as the one sanctioned exception). Minibosses 3–4.5 min (the Colour), 3–4 min (the Hart); elite 2.5–3.5 min (the Mud-Boss). |
| **C-12** | Griefbit fear add | One extra swarm, **once per fight**, gathers visibly (~3 s) after the pocket's timer (MNS-E1 40 s; MWS-E1 30 s) while the frightened NPC is not yet calmed; calming first cancels it. No fear meter. |

### 13.2 Issues found between packages and their resolutions

| # | Issue | Packages | Resolution (canonical here) |
|---|---|---|---|
| **I-1** | **Reedlurker kit swapped.** MBR-E4 gives the **lurker** a spit and the **snapper** a root clamp; MRC-E1, MCS-E1/E3, MLL-E1 and MSG-E1 give the **snapper** the spit and the lurker the lunge. | Act I; Act II; Names; Cloth | **C-5:** lurker lunges (+ grab), snapper spits and clamps in melee. MBR-E4 keeps its numbers and its purpose (a ranged answer to a ranged enemy); only which variant spits changes. |
| **I-2** | **Reed-ripple lunge length**: 1.5 s (MBR-E4) vs 1.2 s (MRC, MCS, MLL, MSG, MRS). MRS-E1 calls 1.2 s "the family's MR-M2 length", which is wrong. | Act I; Work; others | **1.2 s** standard; **1.5 s** first-appearance tell in MRS-E1, MLL-E1 and MBR-E4 (the pockets a player can meet first). |
| **I-3** | **Reedlurkers' first appearance**: bible §10 says "MR-M2 ditch"; MRS, MLL and MSG all unlock after MR-M1 and use Reedlurkers (MLL even says it "teaches the reed-ripple before MR-M2"). | Bible; Work; Names; Cloth | First appearance is **MRS-E1, MLL-E1 or MSG-E1** (whichever is taken first); main-line first MBR-E4. Bible "First seen" should read "MRS / MLL / MSG (after MR-M1); main line MR-M2 ditch". |
| **I-4** | **Earthen Echoes' first appearance**: bible §10 says MR-M3; MLL-E2 (after MR-M1) and MMR (after MR-M2) come earlier. | Bible; Names; Cloth | First appearance is **MLL-E2 or MMR**; main-line first MRC-E2. Bible text only. |
| **I-5** | **Earth-memory re-form timing** differs: 6 s (MMR, MLL), ~10 s (MRC), next third beat (MBL), ~30 s pulse (MBR-E5), "next dusk" (bible §2.6, MNS-E2). | Bible; all earth-memory packages | **C-3** two-layer rule: in-encounter triggers as authored (6 s default; MRC 10 s kept), next dusk outside an encounter. Bible §2.6 should add the in-encounter layer in one sentence. No package numbers change. |
| **I-6** | **Echo swing knockback**: MRC-E2's slap has a "short knockback within the boat" on a 1.2 s tell (displacement below 1.5 s). | Act II | **No knockback** on the echo swing (moderate damage only). Removes the overboard-adjacent displacement too. |
| **I-7** | **Bearer buff model**: MBR-E2 has an interruptible 2.0 s Raise (faster cuts for ~10 s); MBL-E5 has a passive aura "while its standard is risen" plus a Plant ring on beat 3 told only on beat 2 (~1.2 s; an area effect below 1.5 s). | Act I; Act III | **C-4:** Raise everywhere (interruptible, 8 m, 10 s); the MBL Plant keeps its ring but its decal shows from **beat 1** (~2.4 s). |
| **I-8** | **New statuses**: Bog Hound gnawer **bleed** (MBO, MFH); reed-slinger clod **blind** (MNK). Neither is used elsewhere; both are new runtime statuses (CDR-4). | Settlements; Work | **Remove both.** Gnawer bite is a heavier hit; the clod is light damage only. If Systems already has bleed or blind for other content, either may be restored without changing the pockets. |
| **I-9** | **Bog Hound tells**: runner dart 0.8 s (MBO) vs 0.9 s (MFH); gnawer 1.0 s (MBO) vs 1.2 s (MFH). | Settlements; Work | **Dart 0.9 s; gnawer 1.2 s.** Numbers only. |
| **I-10** | **Below-minimum human wind-ups**: mudcutter cleave 0.9 s, Rootshadow hook-slash 0.9 s (moderate hits); reed-slinger whirl 1.4 s vs Thornfell slinger 1.2 s. | Settlements; Cloth | **Melee wind-ups 1.0 s; sling 1.2 s.** |
| **I-11** | **Below-minimum displacement and charges**: Mud-Boss hook pull 1.3 s; Rust Hart charge stamps 1.4 s; stalker stamp 1.0 s; Griefbit carapace charge-butt with knockback 1.2 s. | Settlements; Act I; Work | **1.5 s** for every pull, charge and knockback (C-1). |
| **I-12** | **Below-minimum area effects**: MLD swarm "spread" 2 m bite circle 1.0 s; MCF frame cut (2 m line) 1.0 s; file arrival in the General's P3 told on beat 2 at 0.9 s with a knockdown. | Names; Cloth; Act III | Spread **1.5 s**; frame cut **1.5 s**; in P3, file arms rise on **beat 1** (C-7), matching what Act III already does for the Planted Standard. |
| **I-13** | **Griefbit fear add** stated two ways (MNS 40 s third swarm "gathers over the cart", joins if wave 1 not cleared; MWS "one extra swarm if the fight lasts past 30 s"). | Act I; Work | **C-12:** once per fight, pocket timers kept, cancelled by calming. Text consistent; no number change. |
| **I-14** | **Silt Crawlers**: bible §10 lists them as uncounted Hunting fauna; MCS uses them as required encounters with a **directional shell** (a facing-based damage rule no other Mire creature uses). | Bible; Act II | Keep them as **stirred fauna** (not counted). Directional armour is **optional** (R-9); fallback is more health with the slow turn kept as presentation. |
| **I-15** | **Unplaced variant**: the **rutting stalker** appears in no package. | Bible §10 | World placement **MW-03** (§11.3), or cut it (count 21). |
| **I-16** | **Elite gaps**: Rootshadow Cutters and Hollowfoot have no elite (Phase 1.5 §4.2 asks one per non-wildlife family). | Bible §10 | Recorded deviation kept (canon: Rootshadow avoids large conflict; MD-7: no Hollowfoot person is made a boss). Under MD-7's alternative the Hollowfoot family leaves the roster (count 20). |
| **I-17** | **Boss phase thresholds and length**: bible §10.1 names the phases without thresholds; Act III sets 100/65/30% and 6–8 min, longer than the Thornfell/Lowmark universal Act III boss target (5–7 min). | Bible; Act III | **Act III is canonical (C-11).** The longer target fits the re-muster beat and the rite that follows; the tuning pass may shorten it. Bible §10.1 needs no edit. |
| **I-18** | **Earth-memory target frames**: Act II says Echo frames show no name; Act I says the Colour is never named in UI; nothing states it for ordinary Wraiths, files or the General. | Act I; Act II; Act III | **C-9:** blank frames for all earth-memory; the General's boss bar shows no name (§14 Q4). |
| **I-19** | **"Bright cloth" reaction** for Hollowfoot (dossier) could imply a gear-visibility system. | Act III open decision 5 | Flavour only (standard aggro and assist radius), as Act III recommends (C-10; CDR-4). No package edit. |
| **I-20** | **MLD calm option**: the first draft's dialogue-driven "settle" read as a drive-off. | Names MLD.6 | Already fixed in the Batch 3 review (e98147e): ordinary ditch leash and aggro-on-enter/attack, no settle state; the calm dialogue is the step. On the calm path the swarm is never engaged, so it is scenery (CDR rulings §3.1.4). |
| **I-21** | **General loot**: Act III allows "ordinary material drops only (economy pass)"; MD-11 says battlefield metal is evidence, not feedstock, and the General is made of old iron. | Act III; bible MD-11 | Ordinary **non-metal** material only; no battlefield iron. One clause in Act III §7.1.5 and §E.9. |
| **I-22** | **Hazard clamp** is unstated in every Mire package; the only damaging hazard (MBL gap step-off ~15% max HP) and boss-adjacent patches could stack. | Act III | **C-2** (25% clamp) applies to every Mire hazard. Text only. |
| **I-23** | **MCF frame cut** is a cutter-triggered prop hazard with a fallback in MCF.11 but no id. | Cloth | Id **MCF-H1** [NEW id]; tell 1.5 s (I-12); fallback kept. |
| **I-24** | **MFH `S05` drive-off wording** ("Drive the dogs off the racks") contradicted CDR-1. | Work | **Already fixed** in the concurrent review (now "Defeat the dogs at the racks"); recorded here so the Zones and Integration handoffs use the new text. |

### 13.3 Package edits (number and text changes only, no id, step or flag renames)

**Status (2026-11-09):** every quest-package row below was **applied** in the Batch 4 encounter alignment review (each package's review log has the row). The **bible** row is with the bible owner (suggested text in that review's report).

| Package | Edits |
|---|---|
| **Bible** (`Quests/Caelmor_Mire_Narrative_Production_Bible.md`) | §10 "First seen": Reedlurkers → "MRS / MLL / MSG (after MR-M1); main line MR-M2 ditch" (I-3); Earthen Echoes → "MLL / MMR; main line MR-M3" (I-4). §2.6: add the in-encounter re-form layer in one sentence (I-5). §10 note: the rutting stalker is placed by the Enemies package as MW-03 or cut (I-15). |
| **Act I** (`Quests/Caelmor_Mire_Main_Act_I.md`) | §B7 MBR-E4: move the spit from the lurker to the snapper; the snapper also clamps in melee (I-1). §A7 MNS-E1 carapace charge-butt tell ~1.2 s → **1.5 s** (I-11). |
| **Act II** (`Quests/Caelmor_Mire_Main_Act_II.md`) | §A7 MRC-E2 swing: remove "short knockback within the boat" (I-6). §B7 MCS-E2: note that the front shell is optional with the more-health fallback (I-14). |
| **Act III** (`Quests/Caelmor_Mire_Main_Act_III.md`) | §7 MBL-E5 bearer: replace the passive aura with the Raise (2.0 s, interruptible, 8 m, 10 s) and show the Plant ring decal from beat 1 (I-7). §7.1.3 Files and No one leaves: in P3 the file arms rise on beat 1 (I-12). §7.1.5 "Never" row and §E.9 Rewards: "ordinary non-metal material only; no battlefield iron" (I-21). §7.2: add "no hazard can kill above 25% HP" (I-22). §7.1.5: boss bar shows no name (I-18). |
| **Names and Lanterns** (`Quests/Caelmor_Mire_Side_Quests_Names_and_Lanterns.md`) | MLL.6 MLL-E1 reed-ripple ~1.2 s → **1.5 s** (first appearance) (I-2). MLD.6 MLD-E1 spread ~1.0 s → **1.5 s** (I-12). |
| **Cloth and Memory** (`Quests/Caelmor_Mire_Side_Quests_Cloth_and_Memory.md`) | MCF.6 cutter hook-slash ~0.9 s → **1.0 s** (I-10); frame cut ~1.0 s → **1.5 s** and id MCF-H1 (I-12, I-23). |
| **Work and Skills** (`Quests/Caelmor_Mire_Side_Quests_Work_and_Skills.md`) | MRS.6 MRS-E1: replace "(~1.2 s, the family's MR-M2 length)" with "(~1.5 s, the family's first-appearance length)" (I-2). MFH.6 MFH-E1: gnawer bite "inflicts a short bleed" → "a heavy bite" (I-8). MWS.5 MWS-E1 carapace butt ~1.2 s → **1.5 s** (same kit as MNS-E1, with knockback) (I-11). |
| **Settlements and Combat** (`Quests/Caelmor_Mire_Side_Quests_Settlements_and_Combat.md`) | MBO.7 MBO-E1: runner dart ~0.8 s → **0.9 s**; gnawer ~1.0 s → **1.2 s**, remove "short bleed" (I-8, I-9). MNK.7 MNK-E1: cleave ~0.9 s → **1.0 s**; sling ~1.4 s → **1.2 s**, remove "blinds briefly on hit (standard short blind)" (I-8, I-10). MNK.7.1 Hook pull 1.3 s → **1.5 s** (I-11). MRH.7.1 Charge 1.4 s → **1.5 s**; MRH-E2 stamp ~1.0 s → **1.5 s** (I-11). |

---

## 14. Director-level questions (consequential only)

1. **MD-7 (Hollowfoot):** keep Hollowfoot as an optional human enemy group at the Rag Bend (MBL-E3), or adopt the survivor beat? Everything is built so either choice touches only `[MD-7]` rows; the roster drops to 20 under the alternative.
2. **MD-8 (the Night Count, MW-01):** approve the General as a revisitable night encounter struck from the muster post?
3. **Rutting stalker (I-15):** place it as MW-03 or cut it (count 21)?
4. **The General's name in UI (C-9, I-18):** approve a boss health bar with **no name**, consistent with "never named in UI" for the Risen Colour and blank Echo frames? (Recommendation: yes. The folk name "the General Who Wouldn't Fall" stays in people's mouths, not on the frame.)

MD-3 and MD-4 are already with the Director through the bible; nothing in this file adds to them.

## 15. Hand-offs (documented dependencies; nothing implemented)

| To | What |
|---|---|
| Schema & Content Engineer (33.7) | Creature definitions for 22 counted variants (18 standard; the Mud-Boss elite; the Risen Colour, the Rust Hart, the General) + sub-forms (weak file) + fauna (Silt Crawlers stirred state, mire boars, tarnish serpents, fenny does presentation, fen fowl) + the Hollowfoot pair behind `[MD-7]`; pocket data from §11; hazard ids including the [NEW id]s in §9; re-form sites from §10.2 |
| Systems Engineer | §9.4 R-1 to R-14 (only R-12 to R-14 new; R-13 and R-14 with fallbacks); standard defeat at 0 HP with no exception hook; push/pull with edge clamp; conditional damage reduction; DoT; root; avoided list (no bleed, no blind) |
| Animation / VFX / Audio | §3 grammar and canonical tells; ground-first tells readable at night and in fog; blank earth-memory presentation; the count's audio, decal, rumble and caption; the Shades' lean and the lantern's three looks |
| Level design (Zones file) | Arenas: the crown with lanes, turf strips and leash volume; turnout platform; reed island with uprights; Rust Hollow H6 with five patches and stumps; Reed Hide stages; Chapel stages with lit-post radii; Stillgrave ring; the boat's cut stretches; deep-water hard edges everywhere |
| Quest package authors | §13.3 number and text edits (applied 2026-11-09; keep them on later edits) |
| Bible owner | §13.3 bible rows (I-3, I-4, I-5, I-15) |

## 16. Review log

| Check | Result |
|---|---|
| Coverage | Every encounter id in the three main acts and four side-quest files is in §11 (MNS-E1/E2; MBR-E1–E5; MRC-E1/E2; MCS-E1–E3, MCS-H1/H2; MBL-E1–E7; MRS-E1; MFH-E1; MWS-E1; MLL-E1/E2; MLD-E1; MCF-E1–E3; MMR-E1–E3; MSG-E1; MBO-E1; MNK-E1–E3; MRH-E1/E2). Package hazard ids (MRS-H1, MFH-H1, MWS-H1, MCS-H1/H2) are in §9; hazards described without ids carry [NEW id]s. Quests with no combat are listed in §11.2. |
| Binding rules | CDR-1: every enemy to 0 HP; no yield, retreat, break-off, scatter, drive-off; no Mire SX; re-form is a place rule. CDR-2: every pocket accepts melee or ranged; none requires ranged; no position the General, the Hart or a re-forming figure cannot answer. CDR-3: milestone language only. CDR-4: three new needs, two from the bible with fallbacks; bleed and blind avoided. Combat reveals nothing; no creature carries a quest item. |
| MD tags | `[MD-7]` on every Hollowfoot row with the non-combat alternative stated (§5.7, §11.1, C-10); `[MD-3]` on MRC-E2; `[MD-4]` on the Chapel rows; `[MD-8]` on MW-01. |
| Canon | Shades are a hazard; the Sorrowback is not an encounter; earth-memory never identifies anyone; Memorywardens unnamed; no casualty counts; no route to another region; battlefield metal never loot. |
| Click-to-move | No counter needs a jump or timed input; every shortcut has a walkable fallback; every displacement is clamped to a safe side and away from deep water. |
| Telegraph minimums | After §13 reconciliation, every tell meets 0.8 / 1.0 / 1.5 s (C-1). |
| Scope | No schema, JSON or C#; no edits to other files; integration needs documented only. |
| Reconciliation | Re-checked 2026-11-09 against the side-quest files as committed in e98147e (unchanged since): §9.1 and §11.2 rows, I-1, I-2, I-8 to I-13, I-23 and I-24 hold; I-20 updated (the MLD settle state was removed in that review). |
| Batch 4 encounter alignment review, 2026-11-09 | Independent review. **Fixed here (6):** Reedlurker reach rule added (snapper only in wadeable water; a lurker hit from beyond its lunge submerges and resets), closing an unreachable-snapper melee gap and a free ranged firing line (§5.3, C-5, C-8); Mud-Boss island leash so the banks are not a firing position (§7.4); MCF-E1 lookout platform reachable on foot (§5.5); MLD calm path restated as ordinary leash with no settle state, matching the e98147e fix (§5.1, §11.2, I-20); Stillgrave child renamed Pim → Dob per the Batch 3 rename (§10.2, §11.2); status lines updated now that §13.3 is applied. **Applied** every §13.3 quest-package row (Acts I–III, four side-quest files). Re-grep clean for yield, break off, flee, scatter, drive off, retreat, release, v1, bleed, blind and "the Muster" (remaining hits are rule statements, canon myth, place names such as the Dry Muster, or the muster post). |
