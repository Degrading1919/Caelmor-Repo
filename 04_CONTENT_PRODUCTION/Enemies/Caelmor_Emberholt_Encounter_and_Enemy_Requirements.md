# Emberholt Heights: Encounter and Enemy Requirements

**Status (2026-11-15):** review-state content. Gameplay Designer requirement set, **Batch 4** of the Emberholt production plan (bible §12). It brings every enemy family, variant, boss, miniboss, elite, encounter and hazard authored in the Emberholt act packages and side-quest files into one implementation reference. Everything here is **[NEW]** authored content and is not canon until the Creative Director promotes it (bible ED-19). Items marked **[PROPOSAL — DIRECTOR]** are consequential rules the content depends on; items marked **[PROPOSAL — Gameplay Designer]** are placements or values this file adds. Numbers are **framing targets** (fight length, HP remaining, telegraph duration), not balance values. Health, damage, armour and XP values belong to the tuning pass after a playable build exists. This file is **documented dependencies only**: no schema, JSON or C# is authored or implied (bible scope guard; §11.12).

**This file is canonical for cross-package combat values.** Where two Emberholt packages give different numbers or kits for the same creature, telegraph, status or rule, the value in §16 (shared canonical register C-1 to C-13 and resolutions I-1 to I-23) is the implementation value. §17 lists every package edit (file, id, old text, new text). **PE-1 to PE-15 and PE-18 to PE-20 were applied to the packages on 2026-11-15** (Batch 4 encounter alignment review); PE-16 and PE-17 wait on the Director (§18 Q1). Where a package still differs, implementation follows this file.

**Director rulings (binding):** `Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md`. **CDR-1:** every enemy is defeated at **0 HP**; no health-threshold yield, retreat, break-off, scatter or drive-off; scripted survival only for the named exceptions in its §4 register, and **Emberholt has none** (bible §3 "SX proposal: none"). **CDR-2:** Ranged is a core combat skill; every fight accepts melee or ranged and none requires ranged. **CDR-3:** Emberholt is an internal milestone of the complete game. **CDR-4:** standard RPG systems over bespoke simulation; this file lists only genuinely necessary runtime needs (§15). **CDR-6 (2026-11-14) and rulings §3.7:** every step, boss and reward is completable solo; co-op is optional assistance; partner credit only when the partner's own active step consumes it; personal choices and flags independent; no co-op-only mechanics.

**Bible decisions this file builds on (recommendations, not rulings):** **ED-2** (Ember-Fused workers and flaring children are never combatants; their flares are hazards ended by containment). **ED-6** (heat is ordinary hazard volumes with periodic damage, timed vents, cooling niches and a three-state schedule; no heat meter, no stamina, no stealth or detection; "heat-pressure traps" are pressure plates with visible primed tells). **ED-8** (bosses are constructs or animals: the Draw Sentinel, the Hollow Revenant, Old Plate; no named anchor is ever fought). **ED-10** (EH-M1–M2 Advanced, EH-M3–M6 Expert). Dependent rows are tagged `[ED-n]`. Decisions **D-E2**, **D-S1** and ED-3 (the initiate is Iven Calder), all ruled 2026-11-15, and the reserved D-3, C07 and the "invaders" wording touch no encounter: no fight, kit, drop or spawn depends on them.

**Authored tuning requirements, not approved rules.** C-1 (telegraph minimums, including **1.5 s for any displacement**) and C-2 (hazard protection, including the **25% clamp**) are adopted from the Mire's framing as **authored tuning requirements pending Gameplay Designer review**. They are not approved universal rules. Every row that depends on them says so.

**Sources read (current state, 2026-11-15):** `Quests/Caelmor_Emberholt_Narrative_Production_Bible.md` (§1.1, §1.2, §2.4, §2.6, §2.7, §3 ED-2/ED-6/ED-8/ED-10, §4.2, §9, §10, §10.1, §11, §11.1, §11.2); `Quests/Caelmor_Emberholt_Main_Act_I.md` (Act I conventions; §A7, §A11, §A12; §B7, §B11; §C7, §C8.1, §C9, §C11, §C12); `_Act_II.md` (Act II conventions incl. pressure plates; §A7, §A8, §A9, §A11; §B7, §B11; cross-check); `_Act_III.md` (§6 Beat 6, §7, §7.1, §7.2, §9, §11, §12); `Quests/Caelmor_Emberholt_Side_Quests_Combat_and_Discovery.md` (§0.5; EOP, EFD, EAD, ECC §6 and §10; §7, §8); `_Commons_and_Wards.md` (EWA, ECN, EFC, EBL, ESR §6, §7, §10); `_Unburnt_and_Names.md` (EST, ETB, EMS, ENW, EGT §6–§10); `_Work_and_Skills.md` (ESK, EOM, EFS, EWQ, ESP, ESH §6, §7, §10); the rulings file (CDR-1 to CDR-6, §3.1–§3.7, §4). Format follows `Enemies/Caelmor_Mire_Encounter_and_Enemy_Requirements.md`.

**Source state.** Acts I–III were independently reviewed on 2026-11-14; the four side-quest files on 2026-11-15. All are in review awaiting the Director. This file was built from their state on 2026-11-15; the alignment review the same day applied §17's unconditional edits to them.

**Companions:** the Emberholt Zones and Integration handoffs (Batch 4, written concurrently). Arena geometry stated here (reach rules, niches, ledges, leash volumes) is a level-design requirement there; runtime needs in §15 roll up into the Integration handoff. Where either handoff states a combat value differently, this file governs; §20 records the alignment check still owed.

**Ownership:** the Gameplay Designer owns this file. The Schema & Content Engineer owns creature data schema and naming (Roadmap 33.7). The Systems Engineer owns spawn rules, hazard volumes, statuses and the re-form state model. Animation, VFX and audio own the tells.

---

## 0. How to use this file

| You are | Read |
|---|---|
| Building creature definitions | §4 roster, §5 family specs, §6 bosses, minibosses and elite |
| Building spawn and encounter data | §10 encounter register; §9 resonance conditions and re-form sites; §11 world pockets |
| Building hazards and heat terrain | §3 telegraph grammar; §8 hazard register; C-2, C-3 |
| Building combat runtime support | §1 constraints; §7 defeat; §15 runtime needs |
| Tuning after the first playable build | §2 bands and universal targets; band notes in §5 |
| Editing an Emberholt package | §17 package edits needed |
| Reviewing for the Director or Gameplay Designer | §16 canonical register and issues; §18 questions |

**Id convention.** Emberholt packages prefix every encounter with the three-letter E quest code (`ECW-E1`, `EOP-E3`), so no id collides with Lowmark (`MQ…`, two-letter codes), Thornfell (`T…`) or the Mire (`M…`). Hazards use `<CODE>-H<n>`. Hazards the packages describe without an id get one here, marked **[NEW id]**. World pockets outside any quest use `EW-<nn>` (§11). Canonical register rows are `C-n`; issues are `I-n`; runtime needs are `R-n`; package edits are `PE-n`.

---

## 1. Runtime constraints that shape every encounter

These are the Lowmark, Thornfell and Mire constraints, unchanged, plus the Emberholt-specific lines.

| Constraint (source) | What it means for encounter design |
|---|---|
| **Click-to-move on a host NavMesh; Shift sprint; no jump** (Unity README; Phase 1.3 §1) | Every dodge is "click a floor point and walk there". No counter needs a jump, dash, roll or precise timing. "Step off the wheel while the tell is red" and "stand between lines" are walks. |
| **Agility triggers approved, not built** | No encounter needs an agility trigger. The Act I duct ledge (U2) and drain culvert step have walkable fallbacks (Act I §A12, §C12). Every ledge an enemy stands on is reached on foot (§12); in today's flat navigation that access is a ramp, a NavMesh slope or an at-grade position (Zones §5A ML-05, ML-10, ML-12, ML-29, ML-34 to ML-36). |
| **10 Hz authoritative tick; intents enqueue for T+1** (Stage 6.1.1) | Telegraph minimums C-1 (pending GD). Several package values sit below them; §16 I-1 to I-10 raise them. |
| **Auto-attack on interval; specials on cooldown; no stamina** (Phase 1.3 §2; ED-6) | Fights are about position, target priority and **heat** (which niche, which tell, which line), not input speed. |
| **AI roles Passive / Aggressive / Defensive; enemies never flee** (Phase 1.3 §2; CDR-1) | Every Emberholt enemy fights to 0 HP (§7). Leash/reset stays. Resonance forms re-form by a place condition, which is not a retreat (§9). |
| **Interaction needs reach and line of sight** | Channels under attack (bleed a cock, bleed the pocket valve, shut a collar, douse a brazier, shut a gate, cap a wallow) need a clear standing pad facing the object. Channel progress is kept when interrupted (bible §11.1). |
| **Player camera only; dark interiors** | Most Emberholt fights are in ducts, galleries and chambers lit by tells, seams and lamps. Every telegraph is a body pose, a tell change or a ground glow readable in that light (§3). |
| **Heat is terrain, never a stat** (bible §1.1, ED-6) | Working and Surging zones deal periodic damage; cooling niches stop it; waiting in a niche always turns a zone. No meter, no cold damage, no frost damage (Act III §7.2). |
| **No falls** | No Emberholt arena has a fall, ledge drop, open shaft or deep water a player can be moved into. Every displacement ends on walkable floor (C-2). |
| **Solo-first; per-player state** (bible §9; CDR-6) | Every encounter is solo-clearable at its band. Tells, cocks, braziers, valves, collars, plates, ring sectors, wallows and caps are per-player props. A shared enemy that reads a per-player prop (§13) is a presentation question for Sol and never changes a solo fight. |
| **Combat never reveals evidence; no defeated enemy speaks** (bible §11.3; rulings §3.2) | No drop advances an investigation. Testimony comes from living witnesses, registers, books read in place and objects. Phenomena (the Embermind Echo, the sob, the lanterns, the frost lines) prove nothing and identify nobody. |
| **People are never enemies** (ED-2, ED-12; bible §2.7) | No Volkhari, Ember-Fused worker, child or civic official is ever targetable. A person's flare is a hazard volume around a non-targetable NPC, ended by containment (C-11). |

---

## 2. Progression bands and universal solo targets

Bible ED-10 sets the framing: no quest prerequisite for EH-M1; EH-M1–M2 **Advanced**, EH-M3–M6 **Expert**. Exact levels belong to tuning (`[GD]`).

| Band | Content | Equipment assumption | Combat role |
|---|---|---|---|
| **Advanced** | EH-M1, EH-M2; side quests unlocked after EH-M1 (EWA, EFS, EWQ, ESK, ESP, ESH, EBL, ESR) or EH-M2 (ECN, EOP, EFD, EOM, EST) | Post-Mire identity (production framing only; no Mire requirement before EH-M3) | Cinder Rats, Slag Beetles, the first Cinder Wraiths, Emberback Boars, Dross Scavengers (ECN), Forge Saboteurs and the Saboteur Captain (EOM), Old Plate (EOP, upper end) |
| **Expert** | EH-M3 to EH-M6; side quests unlocked after EH-M3 (EAD, ENW, EMS) or later (ECC, ETB, EGT) | Expert identity, cooked food | Deepbrand Crews, Ashfall Revenants and the Hollow Revenant, Emberdeep Sentinels and the warden-frame, Wraiths in the sleep rooms, the night of the main and the Draw Sentinel |
| **Post-arc** | After EH-M6 | Toward the next milestone | World pockets (§11); the EFD vigil re-offer with `EFD_TELL = bare` |

**Universal targets (all bands; Lowmark, Thornfell and Mire values kept)**

| Rule | Target |
|---|---|
| Standard fight length | 20–90 s per group (packages run to 100–120 s for set groups: per-pocket values in §10 govern); set pieces 2.5–4 min (ECW-E3, ESS-E1, EAC-E3, EFD-E1); minibosses **3–4.5 min** (the Hollow Revenant, including the valve), **3–4 min** (Old Plate); the elite **2.5–3.5 min** (the Saboteur Captain); the Act III boss **6–8 min** (Act III §7.1.4, canonical, C-9) |
| HP after a first-attempt standard fight | 50–90% remaining (per-pocket values in §10 govern) |
| Largest single hit | ≤ 30% of band max HP, telegraphed ≥ 1.5 s. **Emberholt has no exception**: the heaviest authored hit is the Draw Sentinel's Lock-step (~25%) |
| Hazards | C-2 (pending GD): no single hazard event takes a player from above 25% max HP to 0. Periodic heat can still defeat a player who stays in a Surging zone below 25%, which is the deterrent the packages describe. Every displacement ends on walkable floor, never in a slag pool or on a primed plate. |
| Group size | 1–4 hostiles active outside set pieces; set pieces cap at **5 standing at once** (C-12; EGH-E3 counts the Call's glasswalkers inside the cap) |
| Death | Respawn at the named safe point with step, flags, carry-states and channel progress intact; the pocket resets as its row in §10 says. EH-M6: a beaten player always wakes at the warming house (bible §10.1). |
| Toughness framing | **fragile** (scurrier, sprayer, slinger, thrower, flare, glasswalker) · **standard** (biter, boar, scavenger, crossbow, wraith, revenant) · **sturdy** (crawler, tusker, guard, wrecker, sentinel, warden-frame) · **elite** (~3–5× standard: the Saboteur Captain) · **miniboss/boss** (fight-length driven: the Hollow Revenant, Old Plate, the Draw Sentinel) |

---

## 3. Telegraph grammar (heat first)

Emberholt's readable system is **heat** (bible §1.1): tells, vent breath, cooling niches, flarecap. Every telegraph has a **heat tell** (a glow, a tell change, ash lifting, seams brightening) and a **body or audio twin**. Durations are canonical; values marked † were raised from package values (§16). All values are seconds.

| Shape | What the player sees / hears | Canonical duration | Counter | Used by |
|---|---|---|---|---|
| **Ash lift (vent breath)** | Ash lifts off a grate, a kiln lip or a pit grate; a rising hiss | **1.5 s** (vents everywhere); **2.0 s** (Draw Sentinel P2 Seal clock) | Walk off the grate or out of the mouth's line | Every timed vent; ECW-E3 and EFD-E1 re-form trigger; EOM kiln mouth; the Seal |
| **Tell change** | An emberglass bead goes amber, then **red with a crazed skin** (colour **and** texture) | Collar Pulse **2.0 s**; Vent Lines **2.0 s amber + 1.0 s red**; ring sectors **~2 s amber + ~6 s red**; brazier flare **1.5 s** | Step off the wheel, out of the line or off the sector while it is red | Draw Sentinel, the proving ring, ESS braziers |
| **Primed state (standing tell)** | A plate or zone already shows red-crazed before the player steps on or in | Shown before entry (no timer) | Step round; wait for it to vent and go clear | Pressure plates (EAC-H1), Surging zones, red cocks, orange flarecap |
| **Pulse ring** | Light runs out along the floor cracks from a pocket vent | **3.0 s** | Stand in the frame's lee or beyond the current reach | EGH-E3 pocket pulse |
| **Glow wind-up (beast)** | Fur flares orange; plates glow along the neck; abdomen swells red; forefoot scrape and snort | **0.8–1.2 s** light and moderate hits; **1.5 s** charges and butts† | Sidestep; step out of the line; use an outcrop | Rats, beetles, boars, Old Plate |
| **Wind-up (human)** | A pole drawn to the hip; a shield set; a sledge lifted; a sling whirling a glowing pellet; a pot swung behind the shoulder | **1.0 s** melee†; **1.2 s** throws†; **1.4 s** sling; **1.5 s** any pull, shove, stagger or slam† | Step back or aside; break line of sight to shooters | Dross Scavengers, Forge Saboteurs, Deepbrand Crews |
| **Seam brightening (construct)** | Seams brighten down an arm; chest plates part and glow; the eye-slit brightens and it plants | **1.2 s** sweep; **1.5 s** cone, charge† and Brand | Step out of the arc, cone or line; it never turns mid-charge | Emberdeep Sentinels, the warden-frame, the Draw Sentinel |
| **Flare (resonance)** | A body brightens and hums; arms flare white; a fireball swells between hands; glass glows under it | **1.0 s** grasp; **1.2 s** toss, rake, shard throw; **1.5 s** flash, shriek; **2.0 s** shatter | Sidestep; leave the ring or line | Cinder Wraiths, Ashfall Revenants, the Hollow Revenant |
| **Interruptible call** | Arms sunk into the glass | **2.5 s** | Any hit, melee or ranged, cancels it | Hollow Revenant Call |
| **Ground tremor** | Dust lifts off the glass all over the bowl; a rumble | **2.0 s** | Get clear of open ground; outcrops stop charges | Old Plate's resonance spike |

**Four rules for every telegraph.**
1. **Heat and body twins.** A player looking away still gets it. No tell is colour alone: every red tell also crazes (texture), every glow is paired with a pose or motion, and audio carries where the source has one.
2. **The environment names the safe space**, not UI: a blue-washed niche, the frame's lee, a glass outcrop, the wedge between vent lines, the rim of the proving ring, a clear sector, the unplated ribs.
3. **Every heavy attack has a punish window**: crossbow and slinger reloads, Lock-step's ~3 s recovery, Old Plate's roll and outcrop stagger, the re-seat after the fourth collar.
4. **Interruptible wind-ups are tools both ways.** A call that brings help is always interruptible by any hit, melee or ranged (Hollow Revenant Call). Damage-reduction states (Tusker Brace, Old Plate's plate glow, the warden-frame's Draw, the Draw Sentinel's Draw) are visible and end by a place rule or a timer, never by a meter.

---

## 4. Roster and Phase 1.5 count check

### 4.1 Families (bible §10: 4 low, 3 mid, 2 high)

| Tier | Family | Default AI role | Standard variants | Elite | Variants counted |
|---|---|---|---|---|---|
| Low | **Cinder Rats** (vermin) | Aggressive in ducts and cellars; drop from brackets, run walls | scurrier, biter | — (vermin) | 2 |
| Low | **Slag Beetles** (wildlife) | Aggressive guards on vents and slag; sprayers hold vent lips | crawler, sprayer | — (wildlife) | 2 |
| Low | **Emberback Boars** (wildlife) | Aggressive on open ridge ground; charge on resonance spikes | boar, tusker | **Old Plate** (side miniboss, EOP-E3) | 3 |
| Low | **Dross Scavengers** (human) | Aggressive pipe-strippers holding doors, cuts and yards | scavenger, slinger | — (recorded deviation: no scavenger is made a boss) | 2 |
| Mid | **Forge Saboteurs** (human) [CANON smuggler band; NEW crew] | Aggressive; throwers hold ledges | wrecker, thrower | **Saboteur Captain** (EOM-E2) | 3 |
| Mid | **Deepbrand Crews** (human) | Defensive holders of a line; crossbows on raised steps | guard, crossbow | — (recorded deviation: Deepbrand's commander is reserved) | 2 |
| Mid | **Cinder Wraiths** (resonance) | Aggressive surge silhouettes; re-form while the condition lasts | wraith, flare | — (recorded deviation: phenomena) | 2 |
| High | **Ashfall Revenants** (resonance construct) | Aggressive; glasswalkers patrol glass | revenant (**unplaced**, I-13), glasswalker | **the Hollow Revenant** (EH-M3 miniboss, EGH-E3) | 3 |
| High | **Emberdeep Sentinels** (construct) | Patrol and hold; the warden-frame keeps a floor | sentinel, warden-frame | **the Draw Sentinel** (EH-M6 boss, EGA-E4) | 3 |

**Variant total:** 18 standard + 4 elite-slot (Old Plate, Saboteur Captain, Hollow Revenant, Draw Sentinel) = **22**, matching bible §10 and inside Phase 1.5 §4.2's ~20–22. **Bosses:** 1 Act III boss (the Draw Sentinel, a construct) and 2 minibosses (the Hollow Revenant, a resonance construct; Old Plate, an animal), matching bible §10, ED-8 and Phase 1.5 §4.3. The Saboteur Captain is the one true human elite; ED-8 governs bosses only, and the Captain is not a boss. As in the Mire, the bosses and minibosses fill their families' elite slots and are not counted twice.

**Placement gap.** One counted variant, the Ashfall **revenant** (plain form), appears in no package. §16 I-13 gives three options (place it on the EH-M3 crossing, a conditioned world pocket, or cut it to a count of **21**, still inside range). §18 Q1.

**Sub-forms, not variants:** none authored. The EOP-E2 boars, EGA-E3 waves and the Call's glasswalkers are ordinary variants.

### 4.2 Ambient fauna (not counted; never hostile)

**Magma larks** (scatter at a footstep; feathers are gathered in EWQ as pickups, never killed) and **ridge goats** (steading stock; never targetable) are ambient (bible §10). Hunting in Emberholt is the Emberback Boar family; no other huntable fauna is authored. A later economy pass may add wild ridge goats as Hunting fauna; nothing here needs them.

### 4.3 First appearance and recurrence

| Family | First possible appearance | Main-line first | Recurs in |
|---|---|---|---|
| Cinder Rats | ECW-E1 (EH-M1) | EH-M1 | EEH-E1, EWA-E1; EW-01 |
| Slag Beetles | ECW-E2 (EH-M1, long way only) or EFS-E1 (after EH-M1) | EH-M1 (optional route) | EGA-E2, EGA-E3, EAD-E1; EW-02 |
| Cinder Wraiths | ECW-E3 (EH-M1) | EH-M1 | ESS-E1, EFD-E1 (optional) |
| Emberback Boars | EWQ-E1 (after EH-M1) | — | EOP-E1, EOP-E2, EOP-E3 (Old Plate); EW-03 |
| Dross Scavengers | ECN-E1 (after EWA and EH-M2) | EGA-E1 (EH-M6) | ECN-E2, ECC-E1 (optional); EW-04 |
| Forge Saboteurs | EOM-E1 (after ESK and EH-M2) | — | EOM-E2 only |
| Deepbrand Crews | EGH-E1 (EH-M3) | EH-M3 | EAC-E1, EAC-E3 |
| Ashfall Revenants | EGH-E2 (EH-M3) | EH-M3 | EGH-E3; EW-05 (proposal, I-13) |
| Emberdeep Sentinels | EAC-E2 (EH-M4) | EH-M4 | EAC-E3, EGA-E4 |

Bible §10 "First seen" rows all hold (Boars "EWQ / EOP"; Scavengers "ECN; EH-M6"). No bible edit is needed for first appearance.

---

## 5. Family specifications

Each table lists the variant kit with canonical telegraphs. Band notes give the role, not numbers. † marks a value raised from a package (§16, §17).

### 5.1 Cinder Rats (low; vermin)

**Ecology.** Duct vermin that nest by warm pipe and sense heat (canon: the Cinder Rat has "sensed one particular sobbing ember for years"; the vermin are ordinary animals and never carry that meaning). **AI role.** Aggressive. Scurriers run brackets and walls; biters hold a ladder or a nest mouth.

| Variant | Toughness | Kit (tell → effect) | Notes |
|---|---|---|---|
| **scurrier** | fragile | **Drop:** fur flares orange on the bracket overhead (**1.0 s**) → drops on the spot below, light damage, no displacement (ECW-E1, EWA-E1). **Dash** (EEH-E1 variant of the same move): fur flares on the wall (**1.0 s**) → dash along the wall and a leap at the player, light damage. | The drop spot is under the glowing bracket: the tell is also the decal. |
| **biter** | standard | **Lunge:** crouches, back fur glowing (**0.8 s**) → short straight lunge-bite, light damage. | Holds ladders and nest mouths. |
| *Nest flare* (EEH-E1 only) | — | When the cellar duct vent exhales (ash lift **1.5 s**), every rat's fur flares and they press for ~3 s (attack interval shortened; no new attack). | A presentation of vent breath under light pressure. |

**Defeat:** fur goes dark; ordinary corpse; harvest per economy. **Band:** Advanced; pockets end at 70–90% HP.

### 5.2 Slag Beetles (low; wildlife)

**Ecology.** Armoured beetles on slag and vents that burst into sparks when killed [CANON]. **AI role.** Aggressive guards: crawlers hold vents and trench mouths; sprayers sit on vent lips (a step up, always reachable on foot).

| Variant | Toughness | Kit (tell → effect) | Notes |
|---|---|---|---|
| **crawler** | sturdy | **Butt:** lowers its head, plates glowing (**1.5 s**†) → short charge-butt, moderate damage, **one-step knock-back** toward open floor. | Act I ECW-E2 and EFS-E1 had 1.2 s (I-1). |
| **sprayer** | fragile | **Spit:** rears, abdomen swelling red (**1.0 s**) → a slag gob (light to moderate) that leaves a **burning patch ~4 s**. | The ranged-answer target in every beetle fight. The patch is visible flame before entry. |
| *Burst* (both, on defeat) | — | At 0 HP the beetle glows (**1.5 s**†) → sparks in a **1-pace ring**, light damage. | Packages had ~0.5 s (I-2). The burst follows defeat; the beetle is already defeated and is not "cleared" by it. |

**Band:** Advanced (ECW-E2, EFS-E1) and Expert (EGA-E2/E3, EAD-E1). Pockets end at 55–85% HP.

### 5.3 Emberback Boars (low; wildlife)

**Ecology.** Ridge boars with heated plate hide that **charge during resonance spikes** [CANON]. **AI role.** Aggressive on open ground; a glass outcrop, shrub or wall stops a charge.

| Variant | Toughness | Kit (tell → effect) | Notes |
|---|---|---|---|
| **boar** | standard | **Charge:** forefoot scrape and snort, or head lowered with back plates glowing (**1.5 s**) → straight charge ~6 paces, moderate damage and **one-step knock-back**; an outcrop or shrub in the line stops it. | EOP and EWQ agree on 1.5 s. |
| **tusker** | sturdy | **Gore:** head drops, plates glow along the neck (EOP **1.2 s**) or paws the stones twice (EWQ **1.5 s**) → hooking tusk sweep in a front arc, moderate damage, **no displacement**† (I-6). **Brace** (EOP-E1): stops, plates flare amber (**1.0 s**) → reduced damage for ~4 s, visible glow; wait it out or hit the boars. | EWQ's tusker uses Gore only; Brace is optional per pocket. |
| *Resonance spike* | — | When a nearby vent exhales (ash lift **1.5 s**), every boar's plates flare and its next action is a Charge (EWQ-E1). Old Plate's fight has one scripted spike (§6.3). | Canon behaviour as an ordinary scripted trigger. |

**Elite:** Old Plate (§6.3). **Defeat:** lies down on its side; the plate glow goes out; harvestable (rulings §3.1.4). **Band:** Advanced.

### 5.4 Dross Scavengers (low; human)

**Ecology.** Human pipe-strippers from the Dross tips [CANON group; NEW detail]. **AI role.** Aggressive holders of a door, a cut or a yard; slingers stand on something low and climbable.

| Variant | Toughness | Kit (tell → effect) | Notes |
|---|---|---|---|
| **scavenger** | standard | **Bar:** lifts the pry-bar overhead (**1.0 s**) → overhead strike, moderate. **Shove:** shoulder dips, feet set (**1.5 s**) → shove, light damage and **one-step knock-back** (may end on a vent grate; never inside a slag pool, C-2†, I-11). | EGA-E1, ECN-E1/E2 and ECC-E1 share the kit. |
| **slinger** | fragile | **Whirl:** sling whirls with a glowing slag pellet (**1.4 s**) → a shot that leaves a **burning patch ~4 s**. **Reload:** ~2.5 s visible (the window to close). | 1.4 s is above the 1.2 s throw minimum; kept as authored in all four pockets. |

**No elite** (recorded deviation, bible §10). **Defeat:** ordinary human defeat; no dialogue after; ordinary loot (§14). **Band:** Advanced (ECN) and Expert (EGA, ECC).

### 5.5 Forge Saboteurs (mid; human)

**Ecology.** A smuggler band that targets emberwork [CANON]; in EOM a crew Durnan once dismissed, working from a ridge kiln [NEW]. **AI role.** Aggressive; throwers hold the kiln's rim ledge (two ramps).

| Variant | Toughness | Kit (tell → effect) | Notes |
|---|---|---|---|
| **wrecker** | sturdy | **Overhead:** lifts a sledge two-handed, head glowing from the kiln (**1.5 s**) → slam with a 1-pace shock and **one-step knock-back**. **Bar Sweep:** draws a bar back low (**1.0 s**†) → sweeping front arc, moderate. | Package Bar Sweep 0.9 s (I-8). |
| **thrower** | fragile | **Coal Pot:** swings a smoking pot behind the shoulder (**1.2 s**†) → lob; the pot's landing spot glows during flight; bursts in a **2-pace burning patch ~3 s**. | Package 1.0 s (I-9). Crate walls give cover. |

**Elite:** the Saboteur Captain (§6.4). **Placement:** EOM only. **No world pocket** (the kiln is cold after EOM: five aprons on pegs). **Band:** Advanced.

### 5.6 Deepbrand Crews (mid; human)

**Ecology.** Deep-works guards and hands; "doesn't rescue you; retrieves what's left" [CANON]; their public standing as a contractor is [NEW]. **AI role.** Defensive: guards hold a chalk line or a landing with shields and hooked poles; crossbows cover from a raised step reached by a ramp or stairs.

| Variant | Toughness | Kit (tell → effect) | Notes |
|---|---|---|---|
| **guard** | sturdy | **Hook:** draws the pole back to the hip (**1.5 s**†) → hooking sweep that **pulls the player one step** toward him. **Shield bash:** sets his feet, shield up (**1.5 s**†) → bash, moderate damage and a **short stagger** (~0.5 s movement block; counted as displacement under C-1). | Packages: Hook 1.2 s, bash 1.0 s (I-3, I-4). |
| **crossbow** | standard | **Aimed shot:** red glint on the bolt-tip, steadied stance (**1.5 s**) → heavy bolt (≤ ~20% max HP framing); sidestep or break line of sight. **Reload:** ~3 s visible (the window to close). | Always on a raised step reachable on foot (§12). |

**No elite** (recorded deviation: the commander is reserved for later content). **Defeat:** ordinary human defeat; one sober ally bark at most (Darven, `EGH-B2.4`); **no paper is ever found on a body** (§14). **Band:** Expert.

### 5.7 Cinder Wraiths (mid; resonance)

**Ecology.** Blazing silhouettes caused by emotional surges in ember veins; not undead, not conscious, never ghosts [CANON]. They form where a vein surges and re-form while it surges (bible §2.4, §2.7). **AI role.** Aggressive. Wraiths go for whoever is working the condition (at the manifold, carrying the ewer); flares hover over a vent, brazier or pit and throw.

| Variant | Toughness | Kit (tell → effect) | Notes |
|---|---|---|---|
| **wraith** | standard | **Grasp:** arms flare white (**1.0 s**) → two-handed lunge, moderate, no displacement. **Flash:** body brightens and hums (**1.5 s**) → heat burst in a **2-pace ring**, moderate. | Same kit in ECW-E3, ESS-E1, EFD-E1. |
| **flare** | fragile | **Toss:** a ball of fire swells between its hands (**1.2 s**) → arcing throw; landing spot glows during flight; **burning patch ~4 s**. | Hovers **no higher than ~2 m above its vent, brazier or pit lip**, so melee can strike it from the floor or the pit steps (C-7; I-19). |

**No elite** (recorded deviation: phenomena). **Defeat:** collapses into ash at its grate or brazier; no body, no loot, no inspectable object. **Re-form:** §9. **Presentation:** target frame shows the family name only; no face, voice or word (C-8). **Band:** Advanced (ECW, EFD) and Expert (ESS).

### 5.8 Ashfall Revenants (high; resonance construct)

**Ecology.** Resonance constructs formed from intense trauma and uncontrolled embercraft [CANON]. Not the initiate and not any person (bible §2.4). **AI role.** Aggressive; glasswalkers patrol the safe line between tells and engage on sight.

| Variant | Toughness | Kit (tell → effect) | Notes |
|---|---|---|---|
| **glasswalker** | fragile | **Crack step** (presence tell, not an attack): each step stars the glass white with a crunch, so a real one is told apart from the Embermind Echo. **Shard throw:** pulls a shard up out of the floor (**1.2 s**) → thrown in a line, moderate. **Slide:** crouches, glass hissing (**1.0 s**) → short slide and swipe, moderate, no displacement. | EGH-E2, EGH-E3. |
| **revenant** (unplaced; kit [PROPOSAL — Gameplay Designer]) | standard | **Rake:** draws an arm back, ash streaming (**1.2 s**) → wide raking arc in front, moderate. **Shriek:** body contracts and brightens (**1.5 s**) → pressure shriek, **one-step knock-back ring** (2 paces). | The plain form of the Hollow Revenant's kit (§6.2). Placement: I-13. |

**Elite:** the Hollow Revenant (§6.2). **Defeat:** collapses into ash. **Re-form:** only in EGH-E3 while the pocket pulses; glasswalkers on the crossing (no condition) never re-form. **Presentation:** family name only on frames (C-8). **Band:** Expert.

### 5.9 Emberdeep Sentinels (high; construct)

**Ecology.** Constructs made by Remnant engineers to patrol sealed chambers [CANON]. Machines. **AI role.** Patrol on a fixed route and engage on sight (sentinel); hold a floor (warden-frame).

| Variant | Toughness | Kit (tell → effect) | Notes |
|---|---|---|---|
| **sentinel** | sturdy | **Sweep:** draws one arm back, seams brightening (**1.2 s**) → wide horizontal sweep, moderate; duck behind a door jamb or step out. **Vent:** chest plates part, glow inside (**1.5 s**) → short cone of heat ahead, moderate. **Lock-step:** eye-slit brightens and it plants (**1.5 s**†) → straight charge to the point it faced and a skid stop; heavy damage and one step aside to anyone in the path. | Package EAC-E2 Lock-step 1.0 s; Act III uses 1.5 s (I-5). |
| **warden-frame** | sturdy | **Draw (place condition):** while it stands on a red sector its seams glow white and it takes heavily reduced damage [GD]; on clear or amber iron it takes full damage. **Stride:** crouches, seams flicking toward the nearest red sector (**1.0 s**, a movement tell) → strides there. **Clamp:** both arms open wide (**1.2 s**) → two-armed clamp in front, heavy, no displacement. **Brand:** plants a foot, the sector under it flares amber early (**1.5 s**) → that sector vents early (leave it). | EAC-E3 only. The Draw never heals it and never re-forms it. If its target stands off the sunken floor (rim or gallery) it leaves the sectors and follows by the ramps and the gallery access, with no Draw off the sectors (I-24). Clamp is heavy but framed below 25% max HP, so 1.2 s meets C-1. |

**Elite:** the Draw Sentinel (§6.1). **Defeat:** **destroyed at 0 HP**: seizes, plates go dark, cools, stays down; never re-forms; drops nothing. **Band:** Expert.

---

## 6. Bosses, minibosses and elite (consolidated)

### 6.1 The Draw Sentinel — Act III boss (EH-M6 `S06_sentinel`, `EGA-E4`)

Source: Act III §7.1 (reviewed); bible §10.1. Summary for creature building; **the Act III spec is authoritative** and this table matches it (C-9). Nothing here changes it.

| Field | Spec |
|---|---|
| What it is | An Emberdeep Sentinel built to keep a junction: embersteel plates over ember-vein seams, a valve-wheel in its chest coupled to the draw valve. A machine. Never speaks, never carries a proper name, never yields evidence. |
| Read | ~3.5 m, square-shouldered, plates scorched dark, a turning wheel in its chest, a single bar of light for an eye-slit. While it draws, glowing lines run from each open collar along the floor channels to its feet. |
| Arena | Round domed chamber ~26 m (zone tune; MAP VERIFICATION REQUIRED): central plinth and draw valve, four splice collars on the wall, two niches (L, R) with seal plates, one floor vent, eight plate lines that stop ~2 m short of the niches. Solid walls; no fall, ledge or raised firing spot. **Leash (standard):** no player in the chamber for ~5 s → returns to the plinth, health to the top of the current phase, **shut collars stay shut**. |
| Dormant start | Spawns untargetable and inert on the plinth; wakes when the player touches the draw valve (`S05` → `S06`). |
| **P1 "Draw"** 100–65% | Damage reduction per open collar (suggested ~20% each [GD]); **cannot be brought below 65% while any collar is open** (an ordinary phase gate; nothing yields). **Shut collar:** 3-segment channel (~3 s each), hit interrupts the segment, completed segments kept. **Collar Pulse:** collar tell red-crazed **2.0 s** → 3 m half-ring heat burst, moderate, one-step knock-back; at most once per ~10 s per collar. **Sweep** 1.2 s (~4 m arc, moderate, no displacement). **Lock-step** 1.5 s (heavy ~25% max HP, push aside one step; ~3 s recovery = the solo window for a collar segment). Room Working. |
| Re-seat | On the **fourth collar shut** (at 65% or above): climbs onto the plinth, ~6 s invulnerable; both seal plates slam, one lifts; room goes Surging. |
| **P2 "Seal"** to 30% | **Seal** every ~20 s: floor-vent ash lifts **2.0 s** and the open niche's tell goes red-crazed for the full 2.0 s → the open niche's plate drops (anyone inside pushed one step out, light damage), the other lifts. Exactly one niche open. **Stride** (1.0 s movement tell) to the open niche's mouth. **Vent Cone** 1.5 s (6 m cone, moderate + ~3 s burning patch; reaches into a niche mouth). Sweep, Lock-step. Crossing ~20 m (~4 s run) through Surging costs no more than ~10–15% max HP. |
| Plant | At 30%: plants on the plinth, ~4 s invulnerable; both seal plates jam open; room drops to Working. |
| **P3 "Vent"** 30–0% | **Vent Lines** every ~7 s: a line's tells amber **2.0 s**, red **1.0 s** → heat sheet along the whole spoke, heavy, one-step knock-back to the side. Two opposite lines above 15%; three below 15%, never two adjacent, so a safe wedge is always open. **Spill:** arm cocks toward the farthest player (**1.5 s**) → 3 m burning patch ~4 s where they stood. Sweep at the plinth's edge. |
| Defeat | **0 HP**: a last line vents short; plates go dark from the edges in; it locks mid-turn. **Destroyed.** Then the draw-valve channel (3 × ~4 s, no enemies remain). Post-quest it stands cold with a wardens' chalk mark (Act III epilogue). |
| Targets | Solo **6–8 min**, Expert identity with cooked food; ends 30–60% HP. Heaviest hit ~25% (Lock-step). |
| Ranged parity | P1: collars are shut by hand on the wall, so every style crosses the room; Pulse hits a channeller of either style; Lock-step crosses the room. P2: niches close every ~20 s and Vent Cone reaches the open niche's mouth: no niche is a perch. P3: lines run plinth to wall; Spill hits the farthest player. **No position it cannot reach** (C-7). |
| Death / logout | Wake at the warming house (W2), quest Active; a line hand at the stair head offers travel to the last checkpoint (walking is the fallback). Fight resets to the **top of the phase died in** (100 / 65 / 30%); **every collar already shut stays shut** (`EGA_COLLARS`, 0–4, persisted). Logout restores the same checkpoint. |
| Co-op | Shared boss for partners on their own `S06`; health scales per participant, solo tuning is the baseline and is never raised (C-10). A collar shut during the shared fight counts for every present partner on their own `S06` and persists in each one's `EGA_COLLARS`, so no partner shuts it again (CDR-6 §3.7 item 2a); a partner not on `S06` is not credited (§13; supersedes the playability audit CO-04 wording). EGA-E4 spawns from each partner's own `S06`, whatever the host's quest state (CO-02). Which partner's kept collars the shared Sentinel starts with is a presentation question for Sol (§13). The draw-valve channel is a per-player prop; channelled together, it credits every present partner on `S06` (§3.7 item 2a). |
| Presentation | Health bar reads the **family name, "Emberdeep Sentinel"**; "the Draw Sentinel" is a production label and never appears in UI or dialogue (C-8). |
| Loot | None. |

### 6.2 The Hollow Revenant — miniboss phenomenon (EH-M3 `S06_circle`, `EGH-E3`)

Source: Act I §C7 (reviewed), Beat 6. Act I is authoritative; this table consolidates it.

| Field | Spec |
|---|---|
| What it is | An Ashfall Revenant (elite) bound to the heat pocket at the ritual circle: a shape of ash and heat that is never the same height twice. Not the initiate, not any person, never a witness. |
| Arena | The circle (H4, EP07): the frame (the **lee** behind it is safe from the pulse), the rim with its iron rings, the pocket vent and the crew's **bleed valve** (red handle) on the far side. MAP VERIFICATION REQUIRED. |
| **Pocket pulse** (the condition) | Light runs out along the cracks from the pocket vent (**3.0 s**) → heat wave across the floor to the current reach. Every ~30 s. On the pulse, defeated party members re-form at the frame, **the Revenant included**, up to the cap (C-12). |
| The valve | 3-segment channel (~4 s each), interrupted by hits, progress kept. Each segment shrinks the pulse's reach by a third; the **third** ends the condition (`EGH_POCKET_BLED`). Nothing re-forms after; anything standing fights on to 0 HP. |
| Kit | **Rake** 1.2 s (wide arc, moderate). **Shatter:** raises both arms, glass glowing (**2.0 s**) → shards burst in a straight line, heavy (step out of the line). **Shriek** 1.5 s → two-step knock-back ring. **Call** (below 50%, once per life of the Revenant): arms sunk in the glass (**2.5 s**); **any hit interrupts**; otherwise two glasswalkers rise at the rim **up to the cap of 5 standing** (C-12; I-18). |
| Adds | 2 glasswalkers screen the rim (§5.8). |
| Solo approach | Clear the glasswalkers, put the Revenant down, and bleed a segment (or two) in the up-to-30 s before the next pulse brings them back. The Revenant advances on whoever is at the valve, so a solo player alternates fighting and channelling. |
| Targets | Solo **3–4.5 min** including the valve; ends 40–60% HP. |
| Ranged parity | Ranged players can thin glasswalkers from the frame's lee but must cross to the valve; the pulse brings back what was out-ranged; Shatter and the advance close distance. Out-ranging never ends the fight; only the valve does. |
| Death / logout | Respawn at the crew camp (G7). Valve segments kept and reach stays shrunk; the Revenant and its glasswalkers reset to full (ordinary leash reset). Site inspects kept. |
| Co-op | Shared fight; the valve is a per-player prop, but segments bled during the shared fight credit every present partner whose own active step consumes them, so no partner bleeds it again (CDR-6 §3.7 item 2a); a partner not on that step bleeds it when they reach it. Which partner's valve drives the shared pulse is a presentation question for Sol (§13). |
| Presentation | Boss health bar with the **family name, "Ashfall Revenant"**; "the Hollow Revenant" is a production label (C-8). The Embermind Echo (EGH-H5) keeps its cycle and never syncs with the pulse. |
| Loot | None. |

### 6.3 Old Plate — side miniboss (EOP `S05_old_plate`, `EOP-E3`)

Source: `Side_Quests_Combat_and_Discovery.md` EOP.6.1 (reviewed). Authoritative except Spark-shake (†).

| Field | Spec |
|---|---|
| What it is | An old emberback sow the size of a cart, plates grey and thick as slag, muzzle white, left tusk broken to a stump. An animal. Fights to 0 HP; harvestable. |
| Arena | The wallow bowl (M3, EP08): three wallows on a ~25 s bead cycle (W-A → W-B → W-C), three glass outcrops, walkable rim and slope. She follows onto the rim: no ledge, roof or rim point out of her reach. |
| **Plate heat** | After every wallow her plates glow amber and she takes heavily reduced damage [GD]; the glow cools from the centre over ~12 s (~9 s below 25%). Grey plates take full damage. |
| **Wallow** | With grey plates she trots to the amber wallow and rolls **3.0 s** (the opening; plates still grey). Standing in the wallow ring: light heat (EOP-H1). |
| **Capping** | A damping sod (carry; ~2 s cap) greys a bead for ~45 s; she snorts (1.0 s) and trots to the next. All capped: she roots a cold wallow (4.0 s roll, no plate heat). The loop never stalls; the sod stack never runs out; capping is never required. |
| **Charge** | Forefoot scrape and grunt (**1.5 s**) → straight charge, heavy damage and **knockdown** (~1 s). An outcrop in her line stops her: she **staggers 2 s**. With glowing plates the charge leaves burning hoofprints ~3 s (EOP-H2). |
| **Tusk hook** | Head drops and swings to her right (**1.0 s**) → wide hook, moderate, no displacement. Her left (stump side) has none. |
| **Spark-shake** (≤60%) | Plants and shakes, plates rattling (**1.5 s**†) → burning slag flakes in a 3-pace ring; patches ~4 s. Package 1.2 s (I-7). |
| **Resonance spike** (once, at 50%) | Ground tremor (**2.0 s**); every bead red for 6 s (no wallow usable); two boars (EOP-E2) charge in; she charges with them. An ordinary health-triggered event; nothing ends early. |
| **Old legs** (≤25%) | Chains two charges; glow cools faster (~9 s). |
| Targets | Solo **3–4 min**, Advanced identity; caps help both styles equally. |
| Ranged parity | Ranged shoots during rolls and staggers; the charge closes any distance; outcrops are cover for both. Melee stands on her stump side. |
| Death / reset | Leaving the bowl or dying resets her to full and clears caps; the step returns to `S04_dusk` (she comes again at the next dusk; keep watch at the blind). Signs read, the lesson and EOP-E1 stay done. Respawn at the blind (M2). |
| Co-op | Shared fight; wallows, beads and caps are per-player props, but a wallow capped during the shared fight counts for every present partner on their own active `S05`, so no partner caps it again (CDR-6 §3.7 item 2a); a partner not on `S05` is not credited. Solo-tuned. |
| Presentation | Health bar reads **"Old Plate"**, the name Teodor uses (a folk name for an animal, not a design label; C-8; GD to confirm). |
| Loot | Ordinary emberback harvest per economy; the plate-hide stays a prop by `EOP_PLATE` (ECD-01). |

### 6.4 The Saboteur Captain — elite (EOM `S04_kiln`, `EOM-E2`)

Source: `Side_Quests_Work_and_Skills.md` EOM.6 (reviewed). Authoritative except Close (†).

| Field | Spec |
|---|---|
| What he is | The leader of a crew Durnan once dismissed. A human elite (~3–5× standard). Identified only by the ledger read in place and Durnan reading the crew's marks, never by a drop or a word after the fight. |
| Arena | The kiln mouth (M9, EP17) with one wrecker on his flank; the mouth's breath is EOM-H1. |
| Kit | **Hot Bar:** pulls a glowing bar from the mouth, tip brightening white (**1.2 s**) → wide arc swing, moderate-heavy (below 25% max HP, so 1.2 s meets C-1). **Quench Steam:** hooks a bucket with his foot (**1.5 s**, the bucket lifts) → kicks it across a hot brick: steam cone in front, damage, **no blinding**. **Door** (~50%): kicks the kiln door wide (1.0 s, not an attack; the hinge glows) → from then the mouth breathes every ~9 s instead of ~12 s (ash lift 1.5 s; 3-pace line; damage and one-step knock-back). **Close:** if the player stays beyond ~6 m for ~6 s, plants a foot (**1.5 s**†) → head-down charge to melee range, moderate, no displacement. Package 0.8 s (I-10). |
| Targets | Solo **2.5–3.5 min**, Advanced identity; ends 45–65% HP. |
| Ranged parity | Close stops pure range-kiting without making ranged weaker than melee; the rim throwers in EOM-E1 are reachable by two ramps. |
| Death / reset | Respawn at the steadings fire (M6). EOM-E1 stays defeated; the Captain and his wrecker reset on leash (an ordinary reset, not a retreat); the Door phase resets with him. |
| Presentation | Target frame **"Saboteur Captain"** (a role, not a name). No line after the fight. |
| Loot | Ordinary loot per economy; never evidence. |

---

## 7. Defeat (CDR-1)

**Rule.** Every Emberholt enemy, human (Dross Scavengers, Forge Saboteurs and the Captain, Deepbrand Crews), animal (Cinder Rats, Slag Beetles, Emberback Boars, Old Plate), resonance (Cinder Wraiths, Ashfall Revenants, the Hollow Revenant) or construct (Emberdeep Sentinels, the warden-frame, the Draw Sentinel), fights until defeated at **0 HP**. No health threshold ends a fight early. Health-triggered **phase events** (the Revenant's Call, Old Plate's spike and old legs, the Captain's Door, the Draw Sentinel's 65% floor while collars are open) change the fight and never end it. **Leash/reset** stays standard. XP, loot and co-op credit are awarded at defeat. Every step that completes on a fight completes **on defeat** (`EGA-E4 destroyed`, `EOP-E3 defeated`, `ECW-E3 every enemy defeated`).

**No Emberholt exception.** No scripted surrender, mercy or survival outcome (bible §3; rulings §4 lists none for Emberholt). No quest on-defeat hook plays an alternative presentation.

**Condition end (resonance; C-4).** When a resonance condition ends (third cock bled, third brazier doused, pocket bled, vigil song over), nothing more forms. Forms in combat with any player **fight on to 0 HP**. In a required encounter (ECW-E3, ESS-E1, EGH-E3) every standing form is set to engage the player when the condition ends, so the step can always complete. Only in the optional EFD-E1 does the end of the vigil song end the condition as a **place rule** (bible §2.7): no more form, a form already fighting a player carries on to 0 HP, and a form fighting nobody goes with its condition and collapses into ash at the grate. Nothing defeats it and no XP, credit or loot follows; it is not a drive-off, break-off or health outcome (I-12; §18 Q2).

**Defeat presentation by family.** Rats: fur goes dark. Beetles: glow and burst into sparks. Boars: lie down, plate glow fades; harvestable. Humans: fall and fade after the standard corpse time; no tied or downed state, no dialogue with a defeated enemy; at most one sober ally bark. Wraiths and Revenants: collapse into ash at their grate, brazier or frame; no body, no loot, no inspect. Sentinels: seize, cool, stay down.

**Non-combatants (never targetable; no attack resolves on them; enemies never path to them).** Veska Dunmor, Yorven Khelt, Hennet Ulm, Odile Prace, Aubin Harl, Ralenne Kharveil, Sarne Ardane, Jessa Ostry, Tavi, Idra Callow, every student and teacher, Theryn Dalewright, Selice Morra, Hesper Tolk, Darven Mott, Kaevren Thalos, Marenya Silvertide, Maeryn Vall, Seredh Embercarver, Dahrin Vosk, Asera, Thennek Vorren, Thalan Veyr, Kaelith (emberlight only; never reachable), Seralynd Hearthveil, Saelia Verithe, Serix Arden, Vael Trossen, the Cinder Rat, the Flameward Speaker, the EH-M6 line hands, healer and fused smelter-hand, Durnan Volkryst, Quint, Myr Adalrek, Dalia Vret and her tap-hands, Sereth Vorn, Teodor Marsk and every herder and burner, Ivett and every pilgrim, Elyndra the Cinderseer (EFD, EP20; D-EL, ruled 2026-11-15), Haelric Stormvein and every warden, the carter and the rope-store keeper, Grisel Tamm, Ilsa and her diggers, Kaelen Veyr'un, Ondine, Breck Krell, Ryl Danner, Brisa Teglan, Lenk, Imra Brask, Perrin, Glassmoth and her customers, Benno and every child, Tessaly Varn, every Volkhari, every Ember-Fused worker and every civic official. **Emberholt has no fighting allies:** every companion waits in a niche, behind a corner or outside a grille during fights (Act I §A7, §C7; Act II §A7; Act III §7).

**Runtime need (Systems Engineer).** None beyond standard defeat at 0 HP, a phase gate, and the drift-site re-form model (§9; §15 R-1). No yield event, CombatIncapacitated use, hostile-to-neutral swap or on-defeat surrender hook.

---

## 8. Hazard register

Hazards are environmental: no health, no target frame, no AI. All obey **C-2 (pending GD)**: no single hazard event takes a player from above 25% max HP to 0; displacement ends on walkable floor, never in a slag pool or on a primed plate; no falls exist. Heat values follow **C-3 (pending GD)**. Ids marked [NEW id] are assigned here.

### 8.1 Heat terms (shared by every package)

| Term | Effect | Safe space | Tell |
|---|---|---|---|
| **Cool** | None | — | Clear bead |
| **Working** | Light periodic heat damage outside niches | Cooling niche | Amber bead |
| **Surging** | Heavy periodic heat damage outside niches; walkable; never a wall | Cooling niche; a wait in a niche always turns it | Red, crazed bead; heat shimmer |
| **Vent grate** | Timed exhale over the grate: damage and one-step knock-back | Any floor off the grate | Ash lift 1.5 s before each exhale |
| **Burning patch** | Damage per second while stood in; no status after leaving | Anywhere outside the flame | Visible flame, ~3–4 s |
| **Refusal** | A red cock, a red forge or brazier, a hot diverter, an amber face: the interaction is refused, sometimes with a scald and one step of knock-back; **nothing resets** | Step back | Red or amber tell |
| **Frost** (EH-M6) | **None.** Presentation only | — | — |

### 8.2 Main quests

| Id | Hazard | Where (POI) | Tell | Effect | Source |
|---|---|---|---|---|---|
| **ECW-H1** [NEW id] | Working zones | Undercroft U2, U3 after keep watch (EP15) | Amber | Light periodic | Act I §A7 |
| **ECW-H2** [NEW id] | Surging zones | U3 short way before keep watch; U5 during the surge | Red-crazed; shimmer | Heavy periodic; Veska's bark | Act I §A7, §A11 |
| **ECW-H3** [NEW id] | Vent grates | U2, U3, U5 (~10 s ducts, ~12 s junction) | Ash lift 1.5 s | Exhale; ECW-E3's re-form trigger | Act I §A7, §A12 |
| **ECW-H4** [NEW id] | Red cocks | U5 manifold | Red-crazed cock | Refusal: scald and one step of knock-back; never a reset | Act I §A7, §A11 |
| **ECW-H5** [NEW id] | Burning patches | From sprayers and flares | Flame | ~4 s | Act I §A7 |
| **EEH-H1** [NEW id] `[ED-2]` | Tavi's flare | Practice court (EP04), `S03` | Lanterns and hood tell | ~4-pace zone round a non-targetable child; periodic heat; shrinks a third per containment part; ends when she reaches the niche | Act I §B7 |
| **EEH-H2** [NEW id] | The cellar | Academy heat cellar M2, `S05` | Amber | Working; niche by the ladder | Act I §B7 |
| **EEH-H3** [NEW id] | Court floor vent | Practice court | Ash lift 1.5 s | Working outside the test; feeds the flare until its damper is shut | Act I §B7 |
| **EGH-H1** [NEW id] | Flarecap stretches | Darven's Gallery G4, G5 (EP10) | Orange cap | Surging; a struck orange seam bursts (moderate, knock-back); player-triggered | Act I §C7 |
| **EGH-H2** [NEW id] | Drain heat rooms | G6 | Amber | Working; timed vents; a niche each | Act I §C7 |
| **EGH-H3** [NEW id] | Glass vents | Crossing H2, circle H4 (EP07) | Amber breathing; red-crazed surging | Timed exhale; red = heavy (do not cross) | Act I §C7 |
| **EGH-H4** [NEW id] | Pocket pulse | Circle H4, `S06` | Light ring 3.0 s | Heat wave to current reach; re-form trigger (§6.2) | Act I §C7 |
| **EGH-H5** [NEW id] | The Embermind Echo | H2, H4 | Walls brighten, roar 1.5 s | **Overlay only** (~8 s): no collision, no damage, no effect on any volume or AI; reduced-overlay accessibility option | Act I §C8.1 |
| **EAC-H1** [NEW id] `[ED-6]` | Pressure plates | Plate run K4 (EP13) | Primed red-crazed (standing tell); spent clear ~8 s; re-priming amber ~2 s | Stepping on a primed plate vents a column ~0.6 s later: damage and one step of knock-back. Never resets anything, no alarm | Act II conventions, §A7, §A11 |
| **EAC-H2** [NEW id] | Heat rooms | K4a, K4b | Red-crazed on arrival | Surging until Asera's breaths or a wait, then Working | Act II §A7 |
| **EAC-H3** [NEW id] | Shaft vents | K2 | Ash lift 1.5 s | Timed exhale | Act II §A7 |
| **EAC-H4** [NEW id] | Flarecap seams | K2, K5 | Orange cap | Striking or bracing bursts (moderate, knock-back) | Act II §A7 |
| **EAC-H5** [NEW id] | The hand (ring sectors) | Proving ring R1 (EP16) | Amber ~2 s → red-crazed ~6 s | A sheet of heat across the sector, damage and knock-back toward the rim; clockwise, about two hot at once; the rim is always safe; keeps turning after the fight until the frame stops drawing | Act II §A7 |
| **ESS-H1** [NEW id] | Duct and wall vents | Rat's duct (B5.3); record-room wall vent L4 (EP22) | Ash lift 1.5 s | Timed exhale | Act II §B7 |
| **ESS-H2** [NEW id] | The duct's Working stretch | Rat's duct | Amber | Light periodic | Act II §B7 |
| **ESS-H3** [NEW id] | Record room Surging | L4 | Red-crazed | Heavy periodic until the damper is shut | Act II §B7 |
| **ESS-H4** [NEW id] | Brazier flare | Sleep rooms L3a–c, `S04` | Flame stands up white, tell crazes red 1.5 s | ~2-pace heat ring round the brazier; re-form trigger (~10 s per brazier, staggered) | Act II §B7 |
| **ESS-H5** [NEW id] | Burning patches | From flares | Flame | ~4 s | Act II §B7 |
| **EGA-H1** [NEW id] | Working zones | Stages A, B after their cocks; C after the relief; U10 in P1 and P3 | Amber | Light periodic | Act III §7.2 |
| **EGA-H2** [NEW id] | Surging zones | U5 before cock A; stage B before its cock; U8 before the relief; U9 until held; U10 in P2 | Red-crazed; shimmer | Heavy periodic; a niche always turns it | Act III §7.2 |
| **EGA-H3** [NEW id] | Vent grates | U2, U3, U7 (fast, ~8 s), U8, U10 | Ash lift 1.5 s (U10 2.0 s in P2) | Exhale | Act III §7.2 |
| **EGA-H4** [NEW id] | Burning patches | Slingers, sprayers, Vent Cone, Spill | Flame | ~3–4 s | Act III §7.2 |
| **EGA-H5** [NEW id] `[ED-2]` | The fused worker's zone | Warming house W2, `S01` | Veins brighten; blanket smoulders | Working heat in ~2 m round a non-targetable man; never spreads; ends with containment | Act III §7.2 |
| **EGA-H6** [NEW id] | Frost | Cinderwall, upper Undercroft, `S00`–`S06` | — | **None** | Act III §7.2 |

### 8.3 Side quests

| Id | Hazard | Where (POI) | Tell | Effect | Source |
|---|---|---|---|---|---|
| **EWA-H1** | Floor grates | Commons branch C3 | Ash lift 1.5 s (~10 s) | Exhale | EWA.6 |
| **EWA-H2** | The hot diverter | C5 | Key will not seat | Refusal: scald, one step of knock-back | EWA.6 |
| **ECN-H1** | Slag pools | Pits mouth N6, cache basin N7 (EP18) | Dull glow under the crust | Heavy periodic inside; **no knock-back ends inside one** (C-2†; I-11) | ECN.6 |
| **ECN-H2** | Vent grates in the slag | N6 | Ash lift 1.5 s (~12 s) | Exhale | ECN.6 |
| **EBL-H1** | Relief spur | Cinderwall streets, the spur | Amber | Working; the only way to die in EBL is to linger | EBL.6 |
| **EBL-H2** | Outer notch | The relief valve | Red | Refusal: scald if forced, one step of knock-back | EBL.6 |
| **ESR-H1** | Culvert walk | Bridge of Seven Repairs (EP27) | Amber | Working; niches; touch water | ESR.6 |
| **EOP-H1** | Amber wallow | Wallow bowl M3 (EP08) | Amber bead; shimmer | Light periodic inside the ring | EOP.6 |
| **EOP-H2** | Burning hoofprints | Behind Old Plate's charge while her plates glow | Flame | ~3 s, light | EOP.6 |
| **EFD-H1** | The pit vent | Shrine pit E2 (EP20) | Ash lift 1.5 s (~10 s; ~6 s during the song) | Exhale; EFD-E1's re-form trigger | EFD.6 |
| **EFD-H2** | Surging pit (no bead) | E2 during the song | **Heat shimmer only** (deliberately no bead; shimmer is the shape tell) | Heavy periodic in the pit; lower terrace Working; upper terrace cool | EFD.6 |
| **EFD-H3** | The crawl | E3 | Amber bead at the mouth | Light periodic; jar niche halfway | EFD.6 |
| **EAD-H1** `[ED-2]` | Myr's zone | Tap cut T3 (EP19), ~2 m round him | Veins brighten; stone glows | Surging until the gate is shut, then Working; never spreads; beetles never enter it and sprayers never target into it | EAD.6 |
| **EAD-H2** | Wall vents | T2 | Ash lift 1.5 s (~8 s) | Exhale | EAD.6 |
| **EAD-H3** | Flarecap walls | T2 | Orange | **Nothing** if struck by an attack (no trap); a bark teaches the rule | EAD.6 |
| **EOM-H1** | Kiln mouth breath | Kiln mouth M9 (EP17) | Ash lift 1.5 s (~12 s; ~9 s after the Door) | 3-pace line; damage and one-step knock-back | EOM.6 |
| **EFS-H1** | Orange-cap Surging zones | Ridge Workings R3 (EP14) | Red-crazed edge tells; orange cap | Surging (pinned) | EFS.6 |
| **EFS-H2** | Amber face | R5 | Ore-point tell amber (~15 s) | Strike refused: steam, small damage | EFS.6 |
| **EWQ-H1** | Vent bath and range vent | Ash Roads Q4 centre, Q3 corner (EP09) | Ash lift 1.5 s (~12 s) | Exhale; EWQ-E1's resonance spike trigger | EWQ.6 |
| **ESK-H1** [NEW id] | The hearth | Guild yard (EP25) | Fire | Touching it: small burn and a step back. Quench steam is harmless | ESK.6 |
| **ESP-H1** [NEW id] | Yard vent grate | Cooling House yard (EP02) | Ash lift 1.5 s | Small damage and knock-back on the exhale | ESP.6 |
| **ESH-H1** [NEW id] | Test vent on a bare hand | Brisa's tannery (EP03) | Ash lift | Small damage | ESH.6 |
| **ESH-H2** [NEW id] | Soot loft | Tannery loft | Amber | Working away from the bucket | ESH.6 |
| **ESH-H3** [NEW id] | Duct grates | The fitting duct | Ash lift 1.5 s | Exhale (as Act I) | ESH.6 |
| **EST-H1** [NEW id] `[ED-2]` | Kaelen's flare zone | Maeryn's back room (EP03), `S04` | Stove hood tell red-crazed → amber → clear | Periodic heat [GD: light] in ~3 paces round a non-targetable youth; shrinks by a quarter per part; never moves; ends on the fourth part | EST.6 |
| **EMS-H1** [NEW id] | Vent stretch | Ash Roads to the Cold Seam (EP09, EP21) | Ash lift 1.5 s (~8 s) | Light damage and one-step knock-back | EMS.6 |
| **EMS-H2** [NEW id] | Working stretch | Same road | Red-crazed on arrival | Surging until one keep-watch turn, then Working; three niches | EMS.6 |

**No hazard:** EFC (the hearth's red state is a refusal, no damage), ETB, ENW (a red forge only says *Too hot. Let it cool.*), EGT (the red brazier scorches syrup, no damage), ECC.

**Hazard-to-encounter rule.** No hazard ever spawns, buffs or heals an enemy except as a named condition (ECW-H3, ESS-H4, EFD-H1, EGH-H4, EAC-H5 for the warden-frame's Draw, the Draw Sentinel's collars), and every such condition is visible and ended by the player's own channel or by a timed place rule.

---

## 9. Resonance conditions, re-form sites and constructs

### 9.1 Binding rules (bible §2.4, §2.7; rulings §3.1.2)

1. **Combat disperses, conditions decide.** Wraiths and Revenants are defeated at 0 HP and collapse into ash; they re-form **only** while their site's condition lasts and **only** on the site's trigger, up to a cap.
2. **The condition, never health or time-in-fight, decides.** No re-form is tied to the player's or the enemy's health.
3. **Outside an active encounter**, a resonance form exists only when a quest next presents its condition (bible §2.7, **pending Gameplay Designer confirmation**, as in the Mire). No world pocket spawns Wraiths or Revenants without a quest-presented condition (§11).
4. **Condition end:** C-4 (§7).
5. **Constructs never re-form.** Emberdeep Sentinels, the warden-frame and the Draw Sentinel are destroyed at 0 HP. The warden-frame's Draw and the Draw Sentinel's Draw are damage-reduction place rules, not re-forms or heals.
6. **Phenomena identify nobody.** No form has a face, voice, unit mark or word; no form is a person (C-8).

### 9.2 Re-form sites

| Encounter | Site | Condition | Trigger | Cap | Condition ends | Source |
|---|---|---|---|---|---|---|
| ECW-E3 | Cinderwall junction vents (U5) | Unbled cocks | Vent exhale (ash lift 1.5 s) | 3 / 2 / 1 / 0 by cocks bled | Third cock bled | Act I §A7, §A12 |
| ESS-E1 | Three braziers L3a–c | Lit braziers | Brazier flare (1.5 s tell; ~10 s cycle each, staggered) | 3 / 2 / 1 / 0 by braziers doused | Third brazier doused | Act II §B7 |
| EFD-E1 (optional) | The pit grate E2 | The vigil song | Pit exhale (~6 s during the song) | 2 | Song ends | EFD.6 |
| EGH-E3 | The frame in the circle H4 | The pocket pulsing | Pocket pulse (~30 s; 3.0 s tell) | Party of the Revenant + 2 glasswalkers, within C-12 | Third valve segment | Act I §C7 |
| EGH-E2 | The crossing H2 | **None** | — | — | Glasswalkers never re-form | Act I §C7 |

**Live forms are unaffected by cap changes** and fight to 0 HP (Act I §A12).

**Post-quest.** ECW junction, ESS sleep rooms and the EGH circle are quiet after their quests (conditions ended). EFD with `EFD_TELL = bare`: a post-quest vigil may present the surge and re-offer EFD-E1 as written; with `fitted`, the bead goes red, Ivett stops the song and the Wraith moment is rare. These are quest-presented conditions under rule 3.

---

## 10. Encounter register by quest

**Persistence tags** (Lowmark/Thornfell/Mire set). **ONCE**: never respawns for that player. **COND**: resonance; governed by §9.2. **RESET**: resets to full on death or leash. **OPT**: optional pocket. **→WORLD**: after its step, the area keeps an ordinary population of the same family (§11). Solo targets are the package values (§2 targets apply where none is given). All POIs are bible §4.2 ids; placements are relative and **MAP VERIFICATION REQUIRED** throughout (Zones handoff).

### 10.1 Main quests

| Id | Step | Place (POI) | Families / variants | Band | Solo target | Persistence / respawn | Source |
|---|---|---|---|---|---|---|---|
| ECW-E1 | `S01_line` | Undercroft duct run U2 (EP15) | 3 scurrier, 2 biter | Advanced | 45–70 s; 70–85% HP | ONCE →WORLD (EW-01). Respawn: stair niche U1 | Act I §A7 |
| ECW-E2 OPT (route) | `S01_line`, long way only | Side duct of the vent gallery U3 (EP15) | 2 crawler, 1 sprayer | Advanced | 50–80 s; 60–80% HP | ONCE; skipped by waiting at the fork niche. Respawn: U1 | Act I §A7 |
| ECW-E3 | `S06_surge` | Cinderwall junction U5 (EP15) | Wraith and flare forms, open 2 wraith + 1 flare, cap 3 → 2 → 1 | Advanced | 3–4 min wheel to last Wraith; 50–70% HP | COND. Respawn: U1; bled cocks and lowered cap kept; live Wraiths reset; Veska re-opens the wheel on return | Act I §A7 |
| EEH-E1 | `S05_annex` | Academy heat cellar M2 (EP04) | 3 scurrier, 2 biter (nest flare) | Advanced | 45–70 s; 70–85% HP | ONCE. Respawn: practice court rail M1 | Act I §B7 |
| EEH-H1 | `S03_test` | Practice court (EP04) | Tavi's flare (hazard; never a fight) | Advanced | — | Hazard; containment parts kept; zone resumes at its shrunk size | Act I §B7 |
| EGH-E1 | `S02_mouth` | Sealed mouth G2 (EP10) | 2 guard, 1 crossbow (ledge by a short ramp) | Expert | 70–100 s; 55–75% HP | ONCE. Respawn: old works approach G1 | Act I §C7 |
| EGH-E2 | `S05_hollow` | Hollow crossing H2 (EP07) | 2 glasswalker (I-13 option a: 1 glasswalker + 1 revenant) | Expert | 50–80 s; 60–80% HP | ONCE (no condition). Respawn: crew camp G7 | Act I §C7 |
| EGH-E3 | `S06_circle` | The circle H4 (EP07) | **The Hollow Revenant**, 2 glasswalker (+2 on Call, within cap) | Expert | 3–4.5 min incl. valve; 40–60% HP | COND. Respawn: G7; valve segments kept; party resets | Act I §C7; §6.2 |
| EAC-E1 | `S03_warrens` | Deepbrand landing K3 (EP13) | 2 guard, 1 crossbow (raised step, three stairs) | Expert | 70–100 s; 55–75% HP | ONCE. Respawn: shaft foot K2 | Act II §A7 |
| EAC-E2 | `S04_sigils` | Sigil gallery tier-2 landing K5 (EP13) | 1 sentinel (first in Emberholt) | Expert | 60–90 s; 60–80% HP | ONCE. Respawn: K2 | Act II §A7 |
| EAC-E3 | `S05_chamber` | Proving ring R1 and gallery (EP16) | 1 warden-frame, 2 guard, 1 crossbow (gallery by a stair) | Expert | 3–4 min; 40–60% HP | Humans ONCE; warden-frame RESET to full on death; the hand keeps turning. Respawn: ring edge niche | Act II §A7 |
| ESS-E1 | `S04_sleep_rooms` | Sleep-room corridor and rooms L3 (EP22) | Wraith and flare forms, open 2 wraith + 1 flare, cap 3 → 2 → 1 | Expert | 2.5–3.5 min; 50–70% HP | COND. Respawn: vigil hall; doused braziers and lowered cap kept; a carried ewer set down full; live Wraiths reset | Act II §B7 |
| EGA-E1 | `S02_descent` (stage A) | Junction door U4 (EP15) | 3 scavenger, 1 slinger (on the sack, four steps) | Expert | 60–90 s; 60–80% HP | ONCE. Wake: warming house W2; line-hand travel to checkpoint | Act III §7 |
| EGA-E2 | `S02_descent` (stage B) | Old conduits U7 (EP15) | 2 crawler, 2 sprayer, fast vents | Expert | 60–90 s; 60–80% HP | ONCE | Act III §7 |
| EGA-E3 | `S03_bleed` | Bleed house U8 (EP15) | Wave 1: 2 crawler, 1 sprayer; wave 2 (~20 s): 1 crawler, 1 sprayer | Expert | 70–100 s; 55–75% HP | ONCE; the same fight in all three relief choices | Act III §7 |
| EGA-E4 | `S06_sentinel` | Splice junction U10 (EP15) | **The Draw Sentinel** | Expert | 6–8 min; 30–60% HP | Phase checkpoints 100/65/30%; shut collars persist; destroyed, never re-forms | Act III §7.1; §6.1 |

### 10.2 Side quests

| Id | Step | Place (POI) | Families / variants | Band | Solo target | Persistence / respawn | Source |
|---|---|---|---|---|---|---|---|
| EWA-E1 | `S02_trace` | The dead leg C4 (Commons branch; EP02/EP15) | 3 scurrier, 2 biter | Advanced | 45–60 s; 75–90% HP | ONCE (nest prop clears). Respawn: wash-house niche C2 | EWA.6 |
| ECN-E1 | `S04_pits` (fightable earlier; defeats kept) | Pits mouth N6 (EP18) | 3 scavenger, 1 slinger (lean-to roof, ladder) | Advanced | 60–90 s; 65–85% HP | ONCE →WORLD (EW-04). Respawn: Slagside bench N5 | ECN.6 |
| ECN-E2 | `S04_pits` | Cache basin N7 (EP18) | 2 scavenger, 2 slinger (one per ledge; ramps ~4 steps) | Advanced | 90–120 s; 55–75% HP | ONCE. Respawn: N5 | ECN.6 |
| EOP-E1 | `S02_edge` | Molten Scars' edge M1 (EP08) | 2 boar, 1 tusker | Advanced | 50–80 s; 65–85% HP | ONCE →WORLD (EW-03). Respawn: the blind M2 | EOP.6 |
| EOP-E2 | `S05_old_plate` (at 50%) | Wallow bowl M3 (EP08) | 2 boar | Advanced | Inside EOP-E3 | Returns with each retry of EOP-E3 | EOP.6 |
| EOP-E3 | `S05_old_plate` | Wallow bowl M3 (EP08) | **Old Plate** | Advanced | 3–4 min | RESET; step returns to `S04_dusk`. Respawn: M2 | EOP.6.1; §6.3 |
| EFD-E1 OPT | `S02_vigil` | Shrine pit E2 and lower terrace (EP20) | Wraith and flare forms, open 1 wraith + 1 flare, cap 2 | Advanced | 2–3 min if fought through the song; 60–80% HP | COND; re-offered at later vigils with `bare`. Respawn: water-jar niche E1 | EFD.6 |
| EAD-E1 | `S04_cut` | Tap cut T2 (EP19) | Wave 1: 2 crawler, 1 sprayer; wave 2 (~20 s after wave 1 is half down): 1 crawler, 1 sprayer | Expert | 70–100 s; 55–75% HP | ONCE. Respawn: quench barrel T1 | EAD.6 |
| ECC-E1 OPT | `S06_room` | Rope-store yard G5 (EP01) | 2 scavenger, 1 slinger (coil stack, two steps) | Expert | 60–90 s; 60–80% HP | ONCE if fought; avoidable by the alley side-gate. Respawn: wardens' post G1 | ECC.6 |
| EOM-E1 | `S04_kiln` | Kiln yard M8 (EP17) | 2 wrecker, 2 thrower (rim ledge, two ramps) | Advanced | 70–100 s; 55–75% HP | ONCE. Respawn: steadings fire M6 | EOM.6 |
| EOM-E2 | `S04_kiln` | Kiln mouth M9 (EP17) | **Saboteur Captain**, 1 wrecker | Advanced | 2.5–3.5 min; 45–65% HP | RESET on leash or death (Door phase too). Respawn: M6 | EOM.6; §6.4 |
| EFS-E1 | `S03_stope` | Slag fan R4 (EP14) | 3 crawler, 1 sprayer (crest, walkable) | Advanced | 50–75 s; 65–85% HP | ONCE →WORLD (EW-02). Respawn: Workings head R1 | EFS.6 |
| EWQ-E1 | `S06_boars` | The range Q3 on the Ash Roads (EP09) | 2 boar, 1 tusker | Advanced | 50–80 s; 60–80% HP | ONCE →WORLD (EW-03). Respawn: range bench Q3 | EWQ.6 |

**Hazard-only quests** (no encounter id): EEH (EEH-H1 to H3 beside its one fight), EST (EST-H1), EMS (EMS-H1, H2), EBL (EBL-H1, H2), ESR (ESR-H1), ESK (ESK-H1), ESP (ESP-H1), ESH (ESH-H1 to H3). **No combat and no hazard:** EFC, ETB, ENW, EGT.

**Coverage check.** Every encounter id in every Emberholt package appears above: ECW-E1–E3, EEH-E1, EGH-E1–E3, EAC-E1–E3, ESS-E1, EGA-E1–E4 (main, 15); EWA-E1, ECN-E1–E2, EOP-E1–E3, EFD-E1, EAD-E1, ECC-E1, EOM-E1–E2, EFS-E1, EWQ-E1 (side, 14). Total **29**.

---

## 11. World pockets and proposed placements [PROPOSAL — Gameplay Designer]

| Id | Place | Unlock / condition | Content | Band | Respawn |
|---|---|---|---|---|---|
| EW-01 Cinder Rats | Undercroft upper line (EP15) side ducts; not the junction | After EH-M1 | Pairs of scurriers, an occasional biter | Advanced | WORLD |
| EW-02 Slag Beetles | Ridge Workings upper galleries (EP14); the Dross tips by Slagside (EP06/EP18 edge); the Undercroft vent gallery U3 (EP15; Act III §E.9 warden's round) | After EFS (Workings); any (tips); after EH-M6 (U3) | Crawler pairs, an occasional sprayer on a vent lip | Advanced | WORLD |
| EW-03 Emberback Boars | Molten Scars (EP08) round the steadings; Ash Roads beyond the range (EP09) | Ash Roads pocket: after EH-M1 (the Hunting source `EOP-D1.30` points to, so the EOP accept is reachable without EWQ; playability audit ES-04). Molten Scars pocket: after EWQ or EOP | Boar pairs, an occasional tusker; ordinary boars still come to the wallows at dusk (EOP.8) | Advanced | WORLD; Hunting staged here (bible §4.2) |
| EW-04 Dross Scavengers | Dross Scavenger Pits (EP18), outside the Commons cache basin | After ECN Completed | 1–2 scavengers, an occasional slinger, stripping scrap | Advanced | WORLD (long timer). Never at Slagside (a settlement) |
| **EW-05 Ashfall revenant** (only if I-13 option b is chosen) | The Glassed Hollow's outer glass (EP07), reached through the gallery under Kaevren's post | After EH-M3; **only while a quest presents a red-crazed outer-glass vent** (bible §2.7 rule 3) | 1 revenant + 1 glasswalker | Expert | COND. Needs a quest to present the condition; see I-13 |

**No world pocket, by design:** Forge Saboteurs (the kiln is cold after EOM), Deepbrand Crews (the Warrens are closed beyond the mouth by a per-player turn-back volume, Zones EP13; the gallery mouth is under an Emberguard post; the far doors are barred from the far side), Emberdeep Sentinels (no patrol is left reachable; the Draw Sentinel stands cold), Cinder Wraiths outside a quest-presented condition (§9.1 rule 3), Old Plate and the Saboteur Captain (one each). **Never anywhere:** an enemy in a Cooling House, warming house, clinic, shop, academy court or civic hall; any Volkhari, Ember-Fused worker, child or official as an enemy.

---

## 12. Ranged reach register (CDR-2: viable everywhere, never required, no unreachable safe spot)

**Rules.** (1) Every enemy standing above floor level stands on something a player can walk to. In today's flat navigation (no jump, no agility, no ladder form yet) that is a ramp, a NavMesh slope or an at-grade position; a stair or ladder counts only once Zones §5A builds it (ML-05, ML-10, ML-12, ML-29, ML-34 to ML-36; Zones EZ-7). The "Melee reach" column below names the authored access, subject to that rule. (2) Every hovering form (flare) hovers no higher than ~2 m above its vent, brazier or pit lip, so melee can strike it from the floor or the pit steps. (3) Every point a player can attack from is a point an enemy can reach or answer (by pathing, a throw, a charge, Close, Spill or a leash). (4) Every counter that names Ranged has a melee answer. (5) Out-ranging never ends a condition fight; only the player's channel does.

| Encounter | Raised or ranged element | Melee reach | How a ranged player is answered |
|---|---|---|---|
| ECW-E2, EGA-E2/E3, EAD-E1, EFS-E1 | Sprayers on vent lips / the fan crest | A step up; the crest is walkable | Crawlers close; sprayers spit |
| ECW-E3, ESS-E1, EFD-E1 | Flares over vents, braziers, the pit | ≤ ~2 m hover | Wraiths path to the player; flares throw; EFD: Wraiths climb the steps and rail, the toss reaches the upper terrace's front edge, and **beyond the front edge no target is in line of sight** (Zones requirement; I-23) |
| EGH-E1, EAC-E1 | Crossbow on a ledge / raised step | Short ramp / three stairs | Aimed shot; guards Hook a player in |
| EAC-E3 | Crossbow on the gallery; warden-frame on the floor | Gallery stair (ramp in a flat build, ML-12) | The hand turns, so a rim shooter must move round the rim; guards press; crossbow covers the rim; the warden-frame follows a target onto the rim or the gallery, with no Draw off the sectors (I-24) |
| EGH-E3 | — | — | Pulse re-forms what was out-ranged; Shatter and the advance close distance; the valve must be bled by hand |
| EGA-E1, ECN-E1, ECN-E2, ECC-E1 | Slinger on a sack, roof, ledges, coil stack | Four steps; ladder; ramps ~4 steps; two steps | Sling; ECC: the slinger covers the outside stair |
| EOM-E1, EOM-E2 | Throwers on the rim ledge; the Captain | Two ramps | Coal pots; crate walls give cover both ways; the Captain's Close |
| EOP-E1/E3, EWQ-E1 | — | — | Charges close any distance; Old Plate follows onto the rim; outcrops are cover for both |
| EGA-E4 | — | — | No raised spot; niches close and Vent Cone reaches into a mouth; Spill hits the farthest player; leash ~5 s |

---

## 13. Solo completion and co-op (CDR-6; rulings §3.7)

**Solo test (every encounter and boss passes as authored).** No encounter needs two simultaneous holds, a partner on the other side of a door, or a role only another player can fill. Every channel under pressure (cocks, braziers, the pocket valve, collars, Myr's gate, caps) has a solo window: a recovery (Lock-step ~3 s), a reload (crossbows ~3 s, slingers ~2.5 s), a re-form gap (the pulse every ~30 s; brazier and vent cycles), or the condition simply waiting (channels keep progress). Solo targets are in §10.

**Co-op (optional; never compromises solo).** Health scales per participant from the solo baseline, which is **never raised for groups** (C-10). Creatures are shared. A defeat credits each partner **whose own active step consumes it**. Props, choices and flags are per player, but shared work is not repeated (CDR-6 §3.7 item 2a): bleeding a cock, dousing a brazier, bleeding the pocket valve, shutting a collar, capping a wallow or shutting Myr's gate during shared play credits every present partner whose own active step consumes it. A partner not on that step (absent, earlier or later) does it through their own play when they reach it, the prop presented from their own state. Choices, readings and personal flags never transfer. A partner who leaves never blocks the other; the remaining player finishes alone from their own persisted step.

**Presentation questions for Sol (not prerequisites for solo).** A shared enemy that reads a per-player prop needs one presentation when partners' props differ: the ECW-E3 Wraith cap (cocks), the ESS-E1 cap (braziers), the EGH-E3 pulse reach (valve), the EAC-E3 sector cycle (the hand), the EGA-E4 starting collars, Old Plate's wallow targets (beads and caps). Each package records this; none changes a solo fight (I-20). **Predicate note (playability audit CO-03):** where a step requires "all defeated" (ECW `S06_surge`, EGH `S06_circle`, ESS `S04_sleep_rooms`), this is a predicate question, not only presentation: the encounter clears for every present partner on that step (cocks, valve segments or braziers done together count for each of them); per player it is met once their own condition has ended and no form is engaged with them, so a partner's unfinished cocks, valve or braziers never hold another player's completion; a partner on a different step is not held by it and is not credited.

---

## 14. Loot and drop notes

| Rule | Detail |
|---|---|
| **No quest item comes from a creature** | The Emberholt budget is five (`EEH_ledger`, `EGH_roll`, `EAC_sigil_stone`, `ESS_letters`, `EGA_junction_book`; bible §9.4). Each is found, signed out or handed over; none drops. |
| **Combat drops nothing evidentiary** | No ledger, order, letter, roll, tag or mark on a body. Deepbrand guards carry ordinary loot and no paper. The EGA scavengers' sack of brass and a cock handle is a world object, never loot. ECN's Commons brass is a cache found by directions and a bead in the crust, never loot. The EOM crew is identified by a ledger read in place. |
| **Humans** | Dross Scavengers, Forge Saboteurs and the Captain, Deepbrand Crews: ordinary drops per the economy pass. |
| **Animals** | Rats, beetles and boars: harvest where the economy allows (rulings §3.1.4). Old Plate: ordinary emberback harvest; the plate-hide stays a prop by `EOP_PLATE` (ECD-01). Lark feathers come from EWQ pickups, not kills. |
| **Resonance and constructs** | Wraiths, Revenants, the Hollow Revenant: nothing. Sentinels, the warden-frame, the Draw Sentinel: nothing. |
| **Legacy materials** | Ember shards, emberglass, ashsteel, conduction plates and Volkhari Ash are not catalog items (ED-11); no creature drops them. |

---

## 15. Runtime needs (documented dependencies; nothing implemented)

CDR-4 test: every row says whether the need is **standard** (already required by Lowmark, Thornfell or the Mire, or ordinary RPG) or **new**. **This file adds no new runtime need of its own**, but two rows rest on capabilities current source does not demonstrate (playability audit TD-01, TD-05): re-arming hazards (R-9, R-11) and mobile pursuit (R-15). Both are listed as **NEW requirements**, not existing capability. The only Emberholt needs beyond standard are the bible's own two (R-13, R-14), both used in their fallback forms by every package.

| # | Need | Used by | Status | Recommendation / fallback |
|---|---|---|---|---|
| R-1 | **Re-form by condition with a cap** (spawn point + condition flag + trigger + cap; live forms unaffected by cap changes; condition-end engage or collapse per C-4) | ECW-E3, ESS-E1, EFD-E1, EGH-E3 | Standard (Lowmark drift-site model; Mire R-1; Mire MBR-E5 pulse) | One state model; triggers are vent exhale, brazier flare, pit exhale, pocket pulse |
| R-2 | **Push / pull one step toward a defined side, clamped** so it never ends in a slag pool or on a primed plate | Vent exhales, crawler butt, boar charge, Hook, Shove, wrecker Overhead, Shriek, Collar Pulse, Lock-step, Seal, Vent Lines, ring sectors, plates | Standard (Thornfell/Mire push-to-safe-side) | Direction source + edge clamp tagged on slag pools and plates |
| R-3 | **Knockdown / stagger** (timed movement block) | Shield bash (~0.5 s), Old Plate charge (~1 s) | Standard (Lowmark I-18; Mire R-3) | Same ruling |
| R-4 | **Ground damage volumes** (burning patches, wallow ring, hoofprints) | Sprayers, slingers, flares, throwers, Vent Cone, Spill, Old Plate | Standard | Volume with lifetime; **no burn status after leaving** |
| R-5 | **Conditional damage reduction** | Tusker Brace (timer), Old Plate plate glow (timer), warden-frame Draw (sector state), Draw Sentinel Draw (open-collar count) | Standard (Mire R-8) | One buff whose strength or removal is driven by a timer or an encounter condition |
| R-6 | **Phase gate** (health floor while a condition holds) | Draw Sentinel 65% while any collar is open | Standard boss scripting | Ordinary phase gate; nothing yields |
| R-7 | **Health-triggered encounter events** | Revenant Call (<50%), Old Plate spike (50%) and old legs (25%), Captain Door (~50%) | Standard | Ordinary boss scripting; add-spawn respects the cap (C-12) |
| R-8 | **Interruptible wind-up** | Hollow Revenant Call | Standard (Thornfell hornman; Mire bearer) | Any hit cancels |
| R-9 | **Hazard volumes with periodic damage and safe niche volumes; timed vents** | Every heat zone | **NEW requirement: ext LM (re-arm)** (playability audit TD-01). Current hazards fire once, bound to a target, and never re-arm; there is no periodic area damage or safe niche volume | Per C-3. Minimum for Sol: one extension so the existing hazard re-arms on a cooldown (periodic ticks, cyclic vents); niches safe by sitting outside the radii. Sol owns the form |
| R-10 | **Hazard clamp** (no single event from above 25% to 0) | Every hazard | Standard (Thornfell/Mire C-2) | One clamp parameter (pending GD) |
| R-11 | **Step-triggered state hazards** (primed / spent / re-priming) and **sequenced line hazards** | Pressure plates; ring sectors; Vent Lines; Seal plates | **NEW requirement: ext LM (re-arm)** (playability audit TD-01; same extension as R-9) | Tell prop states drive the volumes |
| R-12 | **Untargetable non-combatants; containment hazard round a non-targetable NPC** | Every non-combatant; EEH-H1, EST-H1, EAD-H1, EGA-H5 | Standard (Act III §12 containment pattern) | — |
| R-13 | **Heat-state schedule per zone** (bible **EI-HT-01**) | Every heat zone | **Bible §11.2 (new), fallback in use** | **Fallback:** quest-pinned states per step. Every Emberholt package already uses the fallback; nothing waits on the schedule |
| R-14 | **Staged pressure** (bible **EI-PR-01**) | EH-M6 stages, U10 phases | **Bible §11.2, fallback form** | Per-player environment-variant swap (Mire MI-WL-01); Act III uses only this form |
| R-15 | **Mobile pursuit** (Wraiths path to the player; the EAC-E3 warden-frame and Old Plate follow onto the rim or gallery; Revenant advances; charges close distance) | §6.2, §6.3, §12 (I-24), EOP, EAC-E3 | **Not demonstrated** (`UNITY/README.md`: enemy bodies are anchored; mobile pursuit is remaining work). = LM / MR (build once) (playability audit TD-05) | **Fallback:** anchored enemies whose range covers the arena with no rim spot outside it; charges as re-arming line hazards from the anchor (R-9 extension) |

**Possible need outside combat (not added here):** the EH-M3 compound prerequisite (Act I §C12, derived-flag fallback) and the sigil-stone world-volume read (Act II, per-door inspect fallback). Neither affects an encounter.

**Avoided (do not build for Emberholt):** a heat, temperature or cold meter; stamina; stealth, detection or alarms; cold or frost damage; a burn, bleed, blind or poison status (Captain's steam explicitly does not blind; patches deal damage only while stood in); directional armour; falls or drowning; a yield, surrender or downed state; a hostile-to-neutral swap; a gear-brightness or fear system; any co-op-only mechanic.

---

## 16. Cross-package canonical register and issues

### 16.1 Shared canonical register (canonical for implementation; packages defer to it)

| # | Topic | Canonical value |
|---|---|---|
| **C-1** | Telegraph minimums (**authored tuning requirement, pending Gameplay Designer review**; same framing as the Mire and Act III §7) | Light ≥ **0.8 s**; moderate or heavy ≥ **1.0 s**; thrown or lobbed projectiles ≥ **1.2 s** with the landing spot visible in flight; any hit ≥ 25% max HP, **any displacement (push, pull, knock-back, knockdown, stagger)** and any instant area effect ≥ **1.5 s**. A hazard whose dangerous state is shown before the player enters or steps (primed plate, red cock, Surging zone, orange cap) is told by that standing state. Lingering patches are visible before entry. |
| **C-2** | Hazard protection (**authored tuning requirement, pending Gameplay Designer review**) | No single hazard event (heat tick, exhale, plate, patch, scald, burst, seam) takes a player from above **25% max HP** to 0. Below 25%, staying in a Surging zone can defeat a player. No displacement ends inside a slag pool or on a primed plate (stops at the edge). No falls exist. Zones EK-7 adds the placement rule that no displacement crosses a level change. Frost and cold are never damage. |
| **C-3** | Heat terrain (ED-6; values pending GD) | Working = light periodic; Surging = heavy periodic, tuned so a ~4 s crossing costs ~10–15% max HP (Act III §7.1.4); Working about a third of Surging. A cooling niche stops it; waiting in a niche always turns a zone; no meter. |
| **C-4** | Defeat, re-form and condition end | Every enemy to **0 HP** (CDR-1); no Emberholt SX. Resonance re-forms only on its site's trigger while its condition lasts, up to its cap (§9.2). At condition end: forms in combat fight on to 0 HP; in required encounters every standing form engages; only in optional EFD-E1, when the song ends the condition (a place rule, not a drive-off), does a form fighting nobody collapse at the grate; no XP, credit or loot. Outside encounters, re-form only when a quest presents the condition (pending GD). Constructs never re-form. |
| **C-5** | Kit values raised from packages | Crawler Butt **1.5 s**; beetle burst glow **1.5 s**; Deepbrand Hook **1.5 s** and Shield bash **1.5 s**; Sentinel Lock-step **1.5 s**; tusker Gore **no displacement**; Old Plate Spark-shake **1.5 s**; wrecker Bar Sweep **1.0 s**; thrower Coal Pot **1.2 s**; Captain Close **1.5 s**. Kept as authored: slinger Whirl 1.4 s, biter Lunge 0.8 s, Wraith Grasp 1.0 s, glasswalker Slide 1.0 s, Old Plate Tusk hook 1.0 s. |
| **C-6** | Statuses | One-step knock-back; one-step pull; stagger ~0.5 s; knockdown ~1 s (Old Plate's charge); conditional damage reduction. **No slow, root, burn, bleed, blind or poison status.** |
| **C-7** | Ranged and reach (CDR-2) | §12 rules: every raised enemy reachable on foot (in a flat build by a ramp or at grade, Zones EK-8); hovering flares ≤ ~2 m above their lip; every attack point answered; ranged never required; out-ranging never ends a condition fight. Weapon, ammunition and XP values belong to the item and systems specialists. |
| **C-8** | Frames and names | Target frames show the **family name** only ("Cinder Wraith", "Ashfall Revenant", "Emberdeep Sentinel"); no face, voice, unit mark or word on resonance forms. Production labels ("the Draw Sentinel", "the Hollow Revenant") never appear in UI or dialogue. Exceptions: Old Plate's bar reads **"Old Plate"** (Teodor's folk name); the elite's frame reads **"Saboteur Captain"** (a role). GD to confirm (§18 G2). |
| **C-9** | Boss, miniboss and elite framing | The Draw Sentinel: **Act III §7.1 authoritative** (phases 100/65/30%, 6–8 min, no hit above 30%; heaviest ~25%). The Hollow Revenant 3–4.5 min incl. the valve; Old Plate 3–4 min; the Saboteur Captain 2.5–3.5 min. ED-8 holds: every boss and miniboss is a construct or an animal; no named anchor is fought. |
| **C-10** | Solo and co-op (CDR-6) | Every encounter and boss solo-clearable at its band as authored. Co-op health scaling is optional, from the solo baseline, never raised for groups. Credit through a partner's own active step, including shared kills and shared channels they took part in; nobody repeats identical shared work (§3.7 item 2a). Props, choices and flags per player. Shared presentation is a fallback only (bible §9; MI-CO-06 pattern). |
| **C-11** | Non-combatants and person flares (ED-2) | §7 list never targetable; enemies never path to them. A person's flare is a hazard volume round a non-targetable NPC, ended by containment; enemies never enter it or target into it (EAD-H1 rule applies to all). |
| **C-12** | Set-piece cap | No more than **5 hostiles standing at once** in any set piece. Re-forms and add-spawns (Revenant Call, EGA-E3 wave 2, EAD-E1 wave 2) fill only up to the cap. |
| **C-13** | Evidence and loot | Combat never reveals evidence; no defeated enemy speaks; no quest item from a creature; resonance and constructs drop nothing (§14). |

### 16.2 Issues found between packages and their resolutions

| # | Issue | Packages | Resolution (canonical here) |
|---|---|---|---|
| **I-1** | **Crawler Butt** with knock-back at ~1.2 s (ECW-E2, EFS-E1) vs ~1.5 s (EGA-E2, EAD-E1). Displacement below 1.5 s. | Act I; Work and Skills | **1.5 s** everywhere (C-5). PE-1, PE-11. |
| **I-2** | **Beetle burst** on defeat: ~0.5 s glow before a 1-pace area hit (instant area effect below 1.5 s). | Act I; Act III; Combat and Discovery; Work and Skills | Glow **1.5 s**. PE-2, PE-8, PE-9, PE-11. |
| **I-3** | **Deepbrand Hook** pull at ~1.2 s. | Act I; Act II | **1.5 s**. PE-4, PE-6. EAC-E3's guards inherit ("as EAC-E1"). |
| **I-4** | **Shield bash** stagger at ~1.0 s. A stagger is a movement block (displacement class). | Act I; Act II | **1.5 s** (C-1 pending GD; if GD rules stagger is not displacement, revert to 1.0 s). PE-5, PE-6. |
| **I-5** | **Sentinel Lock-step**: EAC-E2 ~1.0 s vs the Draw Sentinel's ~1.5 s for the same family move with push-aside. | Act II; Act III | **1.5 s**. PE-7. |
| **I-6** | **Tusker Gore** kits differ: EOP-E1 1.2 s, no displacement; EWQ-E1 1.5 s, small knock-back. | Combat and Discovery; Work and Skills | Family kit: **no displacement**; tell length per pocket (both ≥ 1.2 s). PE-14. |
| **I-7** | **Old Plate Spark-shake**: 3-pace ring at 1.2 s. | Combat and Discovery | **1.5 s**. PE-10. |
| **I-8** | **Wrecker Bar Sweep** at ~0.9 s (moderate hit below 1.0 s). | Work and Skills | **1.0 s**. PE-12. |
| **I-9** | **Thrower Coal Pot** at ~1.0 s (a lob that bursts in a 2-pace patch; below the 1.2 s throw minimum used by the Wraith flare and the Mire slinger). | Work and Skills | **1.2 s**, landing spot visible in flight. PE-12. |
| **I-10** | **Captain Close** charge at ~0.8 s. | Work and Skills | **1.5 s**; moderate, no displacement. PE-13. |
| **I-11** | **Shoves into slag pools**: ECN-E1's shove goes "toward a pool"; ECN-H1 says knock-backs can push into pools (heavy periodic damage). | Commons and Wards | **C-2:** no displacement ends inside a slag pool; it stops at the crust edge. The pools stay terrain to fight round. PE-15. |
| **I-12** | **Condition end**: Acts I–III say no enemy is cleared by the condition ending; EFD says an unengaged Wraith collapses when the song ends. | Acts I–III; Combat and Discovery | Both hold under **C-4**: the EFD rule is a place rule ending the condition in an optional pocket; required encounters engage every standing form. EFD text reworded to that framing (PE-19). §18 Q2. |
| **I-13** | **Unplaced variant**: the Ashfall **revenant** (plain form) appears in no package. | Bible §10 | Options: **(a)** EGH-E2 becomes 1 glasswalker + 1 revenant (same size; teaches the plain kit before the elite; conditional PE-16); **(b)** world pocket EW-05, which needs a quest-presented condition (bible §2.7 rule 3) that no package provides; **(c)** cut it (count **21**, inside range; bible §10 note, PE-17). Recommendation: **(a)**. §18 Q1. |
| **I-14** | **Hazard clamp** unstated in every Emberholt package; packages describe death by lingering in Surging zones. | All | **C-2** applies; consistent with lingering deaths below 25%. No edit; the register governs. |
| **I-15** | **"Downed"** wording: Act I §B11 "Player is downed in Tavi's flare" (bible §11.5: no downed state). | Act I | "beaten". PE-3. |
| **I-16** | **Frame names** unstated for the Revenant, Old Plate and the Captain; Act III sets the family name for the Sentinel. | Acts I, III; side files | **C-8**. No edit. |
| **I-17** | **Act III boss length** 6–8 min vs the Lowmark/Thornfell universal 5–7 min. | Act III | **Act III canonical** (C-9), as the Mire. The tuning pass may shorten it. |
| **I-18** | **Revenant Call** can stack with pulse re-forms beyond 5 standing. | Act I | **C-12** cap. Clause added to Act I EGH-E3 Call (PE-20). |
| **I-19** | **Flare hover height** unstated (ECW-E3, ESS-E1, EFD-E1). | Acts I, II; Combat and Discovery | **C-7**: ≤ ~2 m above the lip. Zones requirement; no edit. |
| **I-20** | **Shared enemies reading per-player props** in co-op. | Acts I–III; EOP | Sol presentation questions (§13); solo unaffected. The three "all defeated" predicates are also a predicate question: per-player reading added to §13 (playability audit CO-03). |
| **I-21** | **Pressure plates** vent ~0.6 s after the step with knock-back (below 1.5 s if read as an attack). | Act II | Compliant under C-1's standing-state clause: the primed tell shows before the step. No edit. |
| **I-22** | **Displacement onto plates or sectors**: Hook, Shove and vents could chain a player onto a primed plate. | Act II | **C-2**: no displacement ends on a primed plate. Ring sectors are the arena itself and stay legal (their tell runs ~8 s). No edit. |
| **I-23** | **EFD upper terrace**: Wraiths do not path beyond its front edge; the package also says every attack point is answered. | Combat and Discovery | Zones requirement: from beyond the front edge there is no line of sight into the pit. No edit. |
| **I-24** | **EAC-E3 gallery safe spot**: the warden-frame "holds the floor"; once the gallery crossbow is down, a ranged player on the gallery (or a rim station) could shoot a frame that never leaves the sectors (CDR-2: a place the enemy cannot reach). | Act II | The frame follows a target off the sunken floor by the ramps and gallery access, with no Draw off the sectors. PE-18 (applied). |
| **I-25** | **Post-story Undercroft beetles**: Act III §E.9 put Slag Beetles in a vent gallery "on the day's schedule"; no world pocket covered the Undercroft and the schedule may never be built. | Act III | EW-02 extended to the U3 vent gallery after EH-M6; Act III §E.9 cites EW-01 and EW-02 and the Zones §6.1 defaults (applied). |

---

## 17. Package edits (number and text only; no id, step or flag renames)

**Status (2026-11-15, Batch 4 encounter alignment review): PE-1 to PE-15 and PE-18 to PE-20 applied**, each old string asserted to occur once and replaced as written, with a review-log row in each package. **PE-16 and PE-17 not applied** (Director, §18 Q1). Each row gives the exact text replaced. Inherited rows ("as EAC-E1", "as EGA-E2", "as Act I `ECW-E2`") change with their source and need no separate edit except where the text is repeated (EFS-E1).

| # | File | Id / section | Old text | New text | Issue |
|---|---|---|---|---|---|
| **PE-1** | `Quests/Caelmor_Emberholt_Main_Act_I.md` | §A7 ECW-E2 | `lowers its head and its plates glow (~1.2 s)` | `lowers its head and its plates glow (~1.5 s)` | I-1 |
| **PE-2** | `Quests/Caelmor_Emberholt_Main_Act_I.md` | §A7 ECW-E2 | `(~0.5 s glow first; light damage)` | `(~1.5 s glow first; light damage)` | I-2 |
| **PE-3** | `Quests/Caelmor_Emberholt_Main_Act_I.md` | §B11 | `Player is downed in Tavi's flare` | `Player is beaten in Tavi's flare` | I-15 |
| **PE-4** | `Quests/Caelmor_Emberholt_Main_Act_I.md` | §C7 EGH-E1 | `draws the pole back to the hip (~1.2 s)` | `draws the pole back to the hip (~1.5 s)` | I-3 |
| **PE-5** | `Quests/Caelmor_Emberholt_Main_Act_I.md` | §C7 EGH-E1 | `sets his feet, shield up (~1.0 s)` | `sets his feet, shield up (~1.5 s)` | I-4 |
| **PE-6** | `Quests/Caelmor_Emberholt_Main_Act_II.md` | §A7 EAC-E1 (EAC-E3 inherits) | `draws the pole back to the hip (~1.2 s)`; `feet set, shield up (~1.0 s)` | `(~1.5 s)` in both | I-3, I-4 |
| **PE-7** | `Quests/Caelmor_Emberholt_Main_Act_II.md` | §A7 EAC-E2 | `plants (~1.0 s), then a straight charge` | `plants (~1.5 s), then a straight charge` | I-5 |
| **PE-8** | `Quests/Caelmor_Emberholt_Main_Act_III.md` | §7 EGA-E2 (EGA-E3 inherits) | `on defeat, ~0.5 s glow` | `on defeat, ~1.5 s glow` | I-2 |
| **PE-9** | `Quests/Caelmor_Emberholt_Side_Quests_Combat_and_Discovery.md` | EAD.6 EAD-E1 | `on defeat, ~0.5 s glow` | `on defeat, ~1.5 s glow` | I-2 |
| **PE-10** | `Quests/Caelmor_Emberholt_Side_Quests_Combat_and_Discovery.md` | EOP.6.1 Spark-shake | `She plants and shakes (**1.2 s**` | `She plants and shakes (**1.5 s**` | I-7 |
| **PE-11** | `Quests/Caelmor_Emberholt_Side_Quests_Work_and_Skills.md` | EFS.6 EFS-E1 | `plates glowing ~1.2 s`; `~0.5 s glow, sparks in a 1-pace ring` | `plates glowing ~1.5 s`; `~1.5 s glow, sparks in a 1-pace ring` | I-1, I-2 |
| **PE-12** | `Quests/Caelmor_Emberholt_Side_Quests_Work_and_Skills.md` | EOM.6 EOM-E1 | `draws a bar back low (~0.9 s)`; `behind the shoulder (~1.0 s)` | `draws a bar back low (~1.0 s)`; `behind the shoulder (~1.2 s)` | I-8, I-9 |
| **PE-13** | `Quests/Caelmor_Emberholt_Side_Quests_Work_and_Skills.md` | EOM.6 EOM-E2 Close | `charges (~0.8 s, head down)` | `charges (~1.5 s, head down)` | I-10 |
| **PE-14** | `Quests/Caelmor_Emberholt_Side_Quests_Work_and_Skills.md` | EWQ.6 EWQ-E1 Tusker Gore | `front arc with a small knock-back` | `front arc (no displacement)` | I-6 |
| **PE-15** | `Quests/Caelmor_Emberholt_Side_Quests_Commons_and_Wards.md` | ECN.6 ECN-E1 Shove; ECN-H1 | `(toward a pool if one is near: watch the glow)`; `Terrain; knock-backs can push into them` | `(it stops at a pool's crust edge, never inside: watch the glow)`; `Terrain; no knock-back ends inside one` | I-11 |
| **PE-16** *(conditional: only if §18 Q1 chooses option a)* | `Quests/Caelmor_Emberholt_Main_Act_I.md` | §C7 EGH-E2 | `2 × Ashfall Revenant **glasswalker**` | `1 × Ashfall Revenant **glasswalker**, 1 × **revenant**` (kit per this file §5.8; solo target unchanged). The Call cap clause moved to PE-20 | I-13 |
| **PE-17** *(bible owner; conditional on Q1)* | `Quests/Caelmor_Emberholt_Narrative_Production_Bible.md` | §10 count note | `**Count:** 18 standard variants + 4 elites` | Option a: add "the plain revenant first appears on the EH-M3 crossing". Option c: "17 standard variants + 4 elites = 21 (the plain revenant is cut)" | I-13 |
| **PE-18** *(applied)* | `Quests/Caelmor_Emberholt_Main_Act_II.md` | §A7 EAC-E3 AI role | `Warden-frame holds the floor and moves toward primed sectors;` | `… primed sectors; if its target stands off the sunken floor (rim or gallery) it follows by the ring's ramps and the gallery access and has no Draw off the sectors, so neither is a safe firing spot;` | I-24 |
| **PE-19** *(applied)* | `Quests/Caelmor_Emberholt_Side_Quests_Combat_and_Discovery.md` | EFD.6 Rules; EFD combat compliance | `A Wraith that is not engaged when the song ends collapses at the grate …` | The song's end is a place rule ending the condition: forms already fighting carry on to 0 HP; forms fighting nobody collapse at the grate with no XP, credit or loot; not a drive-off | I-12 |
| **PE-20** *(applied)* | `Quests/Caelmor_Emberholt_Main_Act_I.md` | §C7 EGH-E3 Call | `two glasswalkers rise at the rim at once.` | `… at once, never more than five hostiles standing (Enemies C-12).` | I-18 |

**Count: 18 unconditional edits (PE-1 to PE-15, PE-18 to PE-20) across six package files, all applied 2026-11-15; 2 conditional (PE-16, PE-17) open.** No edit changes an id, step, flag, line, choice or geography.

---

## 18. Questions (consequential only)

**Director**
1. **Q1 — The unplaced Ashfall revenant (I-13).** Place it on the EH-M3 crossing (recommended; PE-16), give it a conditioned world pocket that a later quest presents (EW-05), or cut it (count 21)?
2. **Q2 — Condition end in optional pockets (C-4, I-12).** Confirm that a resonance form in combat with nobody may collapse when its condition ends (EFD-E1 only) as a bible §2.7 place rule rather than a CDR-1 drive-off. Recommendation: yes; required encounters already engage every standing form.

**Gameplay Designer**
1. **G1 — C-1 and C-2** are adopted as authored tuning requirements, not approved rules. In particular: is a ~0.5 s **stagger** displacement under C-1? PE-5 and PE-6 depend on it (if not, the shield bash stays at 1.0 s).
2. **G2 — Frame names (C-8).** Family names on resonance and construct frames and boss bars (following Act III's "Emberdeep Sentinel"), with "Old Plate" and "Saboteur Captain" as the two exceptions?
3. **G3 — Outside-encounter re-form (§9.1 rule 3).** Confirm, as pending in bible §2.7 and the Mire.

---

## 19. Hand-offs (documented dependencies; nothing implemented)

| To | What |
|---|---|
| Schema & Content Engineer (33.7) | Creature definitions for 22 counted variants (18 standard + Old Plate, the Saboteur Captain, the Hollow Revenant, the Draw Sentinel), or 21 under Q1 option c; pocket data from §10; hazard ids including the [NEW id]s in §8; re-form sites from §9.2; frame names per C-8 |
| Systems Engineer | §15 R-1 to R-14 (no new need from this file; R-13 and R-14 in fallback form); standard defeat at 0 HP with no exception hook; push/pull with edge clamp on slag pools and plates; conditional damage reduction; phase gate; avoided list |
| Animation / VFX / Audio | §3 grammar; every red tell crazes (texture twin); ash lift on every vent; landing glow on every lob; flare hover height; the Embermind Echo's reduced-overlay option; family-name frames |
| Level design (Zones handoff) | Arenas: U5 junction with manifold and niches; the circle with the frame's lee and valve; the proving ring with rim and gallery stair; the sleep rooms and cistern niche; U10 with plinth, collars, niches, seal plates and spoke lines; the wallow bowl with outcrops; the kiln yard and mouth with two ramps; the pits basin ramps; the shrine terraces with the front-edge sight line (I-23); every raised enemy position reachable on foot (§12); slag-pool and plate edge tags for the push clamp |
| Integration handoff | §15 rows; Sol presentation questions in §13 |
| Quest package authors | §17 PE-1 to PE-15 and PE-18 to PE-20 applied 2026-11-15; PE-16/PE-17 on the Director's answer to Q1 |

---

## 20. Review log

| Review | Findings and revisions |
|---|---|
| Authored, 2026-11-15 (Batch 4, encounters) | Built from the bible, Acts I–III and the four side-quest files in their reviewed state, and the rulings file (CDR-1 to CDR-6, §3.7). Authored walkthrough only; nothing was played; no build exists. Every encounter id in every Emberholt package registered (29: 15 main, 14 side); 56 hazards registered (37 with new ids). Roster count 22 holds with one unplaced variant (I-13). Bosses checked against ED-8 (construct, resonance construct, animal; no anchor fought). Every encounter and boss checked solo-clearable (CDR-6) and ranged-viable without a safe spot (CDR-2). C-1 and C-2 adopted as authored tuning requirements pending GD, not approved rules. 23 issues found; 15 unconditional package edits listed, none applied; no id, step, flag, line or geography changed. **Owed:** alignment of C-1 to C-13 with the concurrently written Zones and Integration handoffs; re-check §17 after the packages' Director review lands. |
| Batch 4 encounter alignment review, 2026-11-15 | Re-checked against CDR-1 to CDR-6 (§3.7), every package encounter id, step, loot and predicate, and the concurrent Zones (EK-1 to EK-11, ML-34 to ML-36) and Integration (EQ-03 to EQ-05, EQ-09, EQ-13) handoffs. **Applied** PE-1 to PE-15 to the six packages as written (none disputed) and added PE-18 to PE-20. **Defects fixed here:** EAC-E3 gallery and rim were a ranged safe spot against a frame that held the floor (I-24); §1 and §12 counted stairs and ladders as melee reach in a flat build (now ramp or at grade, Zones EZ-7); the EFD-E1 condition end now reads as a place rule ending the condition, with no XP, credit or loot, and never a drive-off (C-4, §7); warden-frame Clamp and Captain Hot Bar framed below 25% max HP so their 1.2 s meets C-1; post-story Undercroft beetles had no world pocket (EW-02 extended, I-25); C-2 cross-references Zones EK-7. C-1 and C-2 stay authored tuning pending GD. Not applied: PE-16, PE-17 (Director Q1). |
| Emberholt character rulings, 2026-11-15 | D-E2, D-S1, ED-3 recorded as ruled in the header (no encounter depended on them; `[INITIATE]` placeholder replaced). Elyndra the Cinderseer added to the non-combatant list (met in EFD at EP20, D-EL). No kit, spawn, drop or value changed. |
| Playability audit fixes, 2026-11-15 | Playability audit fixes, 2026-11-15: CO-02 (rule), CO-03 (§13 predicate note, I-20), CO-04, ES-04, TD-01, TD-05, CO-01 (world-pocket note). |
| CDR-6 shared-credit clarification (§3.7 item 2a), 2026-11-15 | §6.1 Draw Sentinel co-op (collars and draw valve credit every present partner on `S06`; supersedes CO-04 wording), §6.2 EGH-E3 valve, §6.3 Old Plate caps, §13 co-op rule and predicate note, C-10: shared kills, channels and hazard clears credit every present partner whose active step consumes them; no partner repeats identical shared work. Choices and personal flags stay per player. |
