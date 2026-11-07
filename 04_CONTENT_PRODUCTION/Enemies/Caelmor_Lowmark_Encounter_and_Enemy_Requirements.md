# Lowmark v1 — Encounter and Enemy Requirements

**Status:** Gameplay Designer requirement set (Master Assistant Protocol §4.4), Batch 4 of the Lowmark v1 production plan (bible §12; "Lowmark v1" is the label of the first internal production milestone, not a release, CDR-3). It consolidates every enemy, wildlife fight, boss, drift site and encounter pocket authored in the Lowmark narrative packages into one implementation reference. Everything here is **[NEW]** authored content and not canon until the Director promotes it. Items marked **[PROPOSAL — DIRECTOR]** are consequential rules the content depends on. Numbers given are **framing targets** (fight length, HP remaining, telegraph duration), not balance values. Health, damage, armour and XP values belong to the tuning pass after a playable build exists.

**Sources read:** `Quests/Caelmor_Lowmark_v1_Narrative_Production_Bible.md` (whole; §4, §9, §10 binding); `Quests/Caelmor_Lowmark_Quest_The_True_Line.md`; `Quests/Caelmor_Lowmark_Main_Act_I.md`, `_Act_II.md`, `_Act_III.md`; the three side-quest files; Phase 1.5 §2–4 and §10; Phase 1.3 §1–3 and §6; `DESIGNS/Combat Design/Stage 6.1.1 — Combat Action Intents.md` and `Stage 6.1.2 — Combat State Model.md`; `UNITY/README.md`.

**Companion:** `04_CONTENT_PRODUCTION/Zones/Caelmor_Lowmark_POI_and_Zone_Requirements.md` (places, arenas, adjacency). Arena geometry requirements listed here are repeated there as level-design requirements.

**Ownership:** this file is the Gameplay Designer's. Creature data schema and naming belong to the Schema & Content Engineer (Roadmap 33.7). Spawn rules, drift-site state and status effects belong to the Systems Engineer. Nothing here is JSON or code.

---

## 0. How to use this file

| You are | Read |
|---|---|
| Building creature definitions | §4 roster, §5 family specs, §6 wildlife, §7 bosses |
| Building spawn and encounter data | §10 drift-site register, §11 encounter-pocket index |
| Building combat runtime support | §1 constraints, §3 telegraph grammar, §8 defeat (CDR-1), §9 status and runtime needs |
| Tuning after the first playable build | §2 bands and universal targets, per-family band tables |
| Reviewing for the Director | §12 inconsistencies and resolutions, §13 questions |

**Id convention used below [PROPOSAL — DIRECTOR, for the Schema & Content Engineer].** Packages reuse bare ids (`E1`–`E4` appear in The True Line, MQ10, MQ11 and most side quests). This file prefixes every encounter id with its quest code: `TL-E1`, `CR-E1`, `SV-E1`, `UL-E1`, and so on. Packages that already prefix (`SM-`, `HW-`, `NF-`, `GL-`, `TF-`, `DK-`, `MN-`, `BF-`) keep their ids. Hazards keep `H` ids with the same prefix (`BW-H1`). Drift sites use `drift.<slug>`.

---

## 1. Runtime constraints that shape every encounter

| Constraint (source) | What it means for encounter design |
|---|---|
| **Click-to-move on a host NavMesh; Shift sprint; no jump** (Unity README; Phase 1.3 §1) | Every dodge is "click a floor point and walk there". Every counter must be reachable by walking a short distance on navigable ground. No counter may need a jump, a dash, a roll or precise input timing. |
| **Agility triggers approved but not built; no multi-level traversal or off-mesh links yet** (README) | No encounter may require an agility trigger. Raised "safe footing" (Marking-Stone plinths, post footings, serpent stakes) must be NavMesh-walkable by ramp or step height, not by trigger. |
| **10 Hz authoritative tick; intents enqueue for T+1** (Stage 6.1.1) | A player's reaction costs 1–2 ticks of latency on top of human reaction. Telegraph durations below are given in seconds and ticks. **Minimum telegraphs:** light hits ≥ 0.8 s (8 ticks); moderate or heavy hits ≥ 1.0 s (10 ticks); any hit at or above 25% max HP, any displacement toward a hazard, and any area effect ≥ 1.5 s (15 ticks). |
| **Auto-attack on weapon interval; specials on cooldown; no stamina** (Phase 1.3 §2) | Fights are about position and target priority, not input speed. "Punish windows" are when the enemy is exposed and the player's auto-attack and specials land freely. |
| **AI roles: Passive, Aggressive, Defensive; enemies never flee** (Phase 1.3 §2; CDR-1) | Every creature below has one role and is defeated at 0 HP. "Re-forming" drift, "sinking" serpents and "scattering" goblin crews (a bark after all members are defeated) are all specified so that nothing runs away at low HP during a fight. |
| **Combat states: Idle, Engaged, Acting, Defending, Restricted, Incapacitated; Incapacitated "does not imply death"** (Stage 6.1.2) | Human enemies take the **ordinary defeat** at 0 HP (§8, CDR-1); content no longer depends on CombatIncapacitated. The two scripted exceptions (SX-1 Joss, SX-2 Sallow) use the quest's **on-defeat hook**. Short staggers and knockdowns need a ruling (§9). |
| **Ranged is a core combat skill** (CDR-2) | Every Lowmark encounter can be fought with **melee or ranged**; none requires ranged and none is trivialised by it (no boss the player can shoot from a spot the boss cannot reach). Arena edges, deep sides and ledges must not give a ranged player a safe unreachable perch. Lowmark stays melee-led; WC has one optional borrowed short bow (§11.2). |
| **Interaction needs reach and line of sight** (README) | Channelled interactions under attack (cranks, levers, withies, boards) need clear sightlines from the safe standing spot to the object. |
| **Player-controlled camera and zoom only** (Phase 1.3 §1) | Telegraphs must read from the default zoom at any orbit angle. Ground decals and audio tells carry the load; no telegraph may depend on a camera angle. |
| **Solo-first; per-player state** (bible §9; Pillar D) | Every encounter is solo-clearable at its band. Co-op scales health per participant (tuning pass), shares world creatures, and gives step credit to every participant on the step. |
| **Combat never reveals evidence** (bible §11.3) | No creature drop advances any investigation. Loot is ordinary loot only. |

---

## 2. Progression bands and universal solo targets

Bible §6 level framing defines the bands. Exact levels belong to tuning.

| Band | Main quests | Equipment assumption | Combat role in the arc |
|---|---|---|---|
| **Novice** | MQ1–MQ4; side quests gated after MQ1–MQ3 | Starter weapon, no armour, rising to **Milestone 1** "dependable field equipment" by MQ4 (BP light protection, HS blade) | Learn telegraphs, leashes, the ground, and target priority. First elite (Sack-King). First humans. |
| **Competent** | MQ5–MQ9; side quests gated after MQ4–MQ5 | **Milestone 2** identity | Mixed groups, set-piece defence, an optional high-tier preview (Deep-Pool Serpent). Combat valley in MQ8–MQ9 by design. |
| **Advanced** | MQ10–MQ11 | **Milestone 3** specialist equipment | Siege, miniboss, the gate holds, the Muster. |
| **Post-arc** | MQ12 onward | Working toward **Milestone 4** | Residual drift sites, world elites, revisitable dungeons. |

**Universal targets (all bands)**

| Rule | Target |
|---|---|
| Standard fight length | 20–60 s per group; set pieces 2–6 min split into waves; minibosses 2.5–4 min; the Muster 6–8 min |
| HP after a first-attempt standard fight | 50–85% remaining |
| Largest single non-boss hit | ≤ 30% of a band-appropriate player's max HP, always telegraphed ≥ 1.5 s |
| Hazards and traps | Cannot kill a player above 25% HP (BW, HS, SB, SM rules unified) |
| Group size | 1–4 hostiles active at once outside set pieces (Phase 1.5 §10.1: "small, readable clusters"); set pieces cap at 4–5 active |
| Death penalty | Respawn at the named safe point with step, flags, quest items and completed segments intact; encounter resets as specified per pocket |
| Toughness framing | Use five health tiers relative to the band's standard: **fragile** (vermin, swarm members) · **standard** · **sturdy** (pole-man, runner pack leader, stalker) · **elite** (~3–5× standard) · **miniboss/boss** (fight-length driven). Tuning picks the multipliers. |

---

## 3. Telegraph grammar (shared language for every family)

Lowmark uses eight telegraph shapes. Each family draws from this list so players learn one vocabulary. Durations are canonical; package text that differs is reconciled in §12.

| Shape | What the player sees/hears | Canonical duration | Counter |
|---|---|---|---|
| **Line** | A straight mark on the ground or water: ripple line, flattened reeds, frost line, wet streak | 0.8 s (light) · 1.2 s (moderate) · 1.5–2.0 s (heavy) | Step off the line (1–2 m) |
| **Cone / arc** | Weapon drawn back across the body; a light cone or rustling arc on the ground | 1.2–1.5 s | Step behind or outside the arc |
| **Ring / circle** | A ring of bubbles, mist, shadow or light settling on the ground | 1.5–2.0 s | Walk out of the ring |
| **Charge** | Pawing, head lowered, boot scrape; a straight lane implied by facing | 1.5 s | Sidestep; the charger overruns and stands exposed 1.5–2 s |
| **Pull / tether** | A pale line drawn from the enemy to the player; current lines on water | 1.5–2.0 s | Step onto marked firm ground, or land two hits (the leech-latch rule) |
| **Latch** | Creature rears from the water | 1.2 s | Step onto dry ground or land two hits to break |
| **Cloud** | Body shake; grey cloud expands | 1.5 s build | Walk out of the cloud |
| **Count** | Audible count ("one… two… three"), one beat per ~1.0–1.2 s, with a visible marker per beat | 3–4.8 s total | Move once per beat; be on safe ground at the last beat |

**Three rules for every telegraph.** (1) Every tell has an **audio and a visual component**, so a player looking elsewhere still gets it. (2) Every heavy tell names its **safe space by the environment** (dry stone, stake disc, post footing, Marking Stone, berm) rather than by UI. (3) Every heavy attack has a **punish window** after it.

---

## 4. Roster and Phase 1.5 count check

### 4.1 Families (Phase 1.5 §4.1: 4 low, 3 mid, 2 high)

| Tier | Family | AI role (default) | Standard variants | Elite | Count |
|---|---|---|---|---|---|
| Low | **Shallows vermin** | Aggressive, leashed to water | swarm (Silt Swimmer / River Skitter presentations), latcher (River Leech) | none (vermin; bible §10) | 2 |
| Low | **Field Goblins** | Aggressive in their camp volume | scrapper, trapper | Sack-King | 3 |
| Low | **Ash Hounds** | Aggressive pack | runner, ash-shaker | Den Mother | 3 |
| Low | **Mud Pipers** | Aggressive once the player enters reeds; lure first | piper, bog-diver | Chorus-Piper | 3 |
| Mid | **Smugglers** (Sallow's crews, opportunists) | Aggressive; some prop-targeting | pole-man, cutter | **crew boss** (Rusk, Brack) **[PROPOSAL — DIRECTOR]** | 3 |
| Mid | **Reed Stalkers** | Aggressive ambush, leashed to reeds | stalker, lurker | Old Mud | 3 |
| Mid | **Water Wraiths** (drift) | Place-bound Aggressive; re-form | drift, lantern-drift | (slot filled by Joss Garrow per bible; see §7.2) | 2 (+1) |
| High | **Stillwater Serpents** | Aggressive, pool-bound | serpent | Deep-Pool Serpent | 2 |
| High | **Wraith Lords** | Boss | — | The Muster (boss) | 1 (boss) |

**Variant total:** 21 standard and elite variants (excluding Joss and the Muster), inside Phase 1.5 §4.2's ~20–22. **Bosses:** 1 Act III boss (the Muster) and 2 minibosses (Gideon Sallow, Joss Garrow), matching §4.3. Sub-forms that are **not** variants: small drift and wisp (MQ8 split), heap-boss (post-SM Sack-King replacement), named crew bosses as instances of one elite variant.

**Phase 1.5 under-count noted:** Serpents have one standard variant and Wraith Lords none, against "2 standard variants each". The total is in range and high-tier families are deliberately rare. No new variant is proposed.

### 4.2 Wildlife (Hunting fauna; not counted; fight when provoked)

Furrow Boar (incl. sow), Marsh Fen Goose, Bog-Touched Elk. Full behaviour in §6.

### 4.3 First appearance and recurrence (summary)

| Family | First possible appearance | Main-line first | Recurs in |
|---|---|---|---|
| Shallows vermin | TL-E2 (MQ1) | MQ1 | TL-E3, GL-E1/E2/E4a, TF-E1, BF-E1, BW-E1, FK-E2, BP-E1, UL-E3, UC-E1, WD-E4, FC-E1 |
| Field Goblins | SM-E1 (MQ2) | SM-E1 (MQ2) | SM-E2–E5, WC-E1 (after MQ2), GL-E4c, UR-E1, TB-E1; P20 and P07 world |
| Ash Hounds | HW-E2 (MQ3) | MQ3 | HW-E3 (burned-culvert den: MQ3 only), GL-E4b (plot-scrub den, not the culvert); Ashen Flats world |
| Mud Pipers | DK-E1 (MQ7) | MQ7 | DK-E2, SV-E1b; Chorus-Piper world elite (proposal) |
| Smugglers | NF-E1 (MQ4) **or** NT-E1 (after MQ2) | MQ4 | NF-E2–E4, TF-E2/E3a, CR-E1–E4, UL-E1/E2, NT-E1–E4 |
| Reed Stalkers | **NB-E1 (after MQ2): canonical first appearance** | GL-E3 (MQ5) | NB-E2/E3, FW-E1/E2, SV-E2; Old Mud world elite (proposal) |
| Water Wraiths | HW-E1 or HW-E4 (MQ3) | MQ3 | NF-E4, TF-E3b, DK-E2, MN-E1/E2, SV-E1/E3/E4, WD-E1–E3, CN-E1/E1b, OL-E1/E3, ME10 |
| Stillwater Serpents | FW-E3 (FW unlocks after MQ5) | SV-E3 (MQ11) | — |
| Wraith Lords | SV-E5 (MQ11) | MQ11 | — |

---

## 5. Family specifications

Each table lists the variant kit with canonical telegraphs. "Band tuning" gives the role the family plays in each band, not numbers.

### 5.1 Shallows vermin (low)

**Ecology.** Small river animals of the shallows, culverts and drains: silt-coloured swimmers in open river shallows (Silt Swimmer), chitinous scuttlers in culverts, drains and backwaters (River Skitter), and slow fat leeches in still deep pockets (River Leech). They live only in water and never leave it. They are the Vale's "your feet are wet" tax.

**AI role.** Aggressive inside a **water volume**; hard-leashed to it. Stepping onto dry ground, a ledge or drawing-steps ends contact.

| Variant | Presentations | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|---|
| **Swarm** | Silt Swimmer (river shallows: TL, FC, VK ambient); River Skitter (culverts, drains, backwaters, race, plunge pool: GL, TF, BF, BW, BP, UL, UC, WD) | Groups of 2–5; quick nips; bunch then rush | **Line**: ripple line or ripple fan toward the player, with a chitter/hiss (**0.8 s / 8 ticks**) | Step out of the line; step onto dry ground | Novice (core), Competent (filler), Advanced (filler only) |
| **Latcher** | River Leech | Slow; rears and latches; latched player is slowed | **Latch**: rears from the water (**1.2 s / 12 ticks**) | Latch breaks on stepping onto dry ground **or** landing two hits (canonical "leech-latch rule", reused by Joss's rope and the Muster's drag) | Novice–Competent |

**Band tuning.** Novice: the teaching family; first fight TL-E2 ends at 50–75% HP, death only by ignoring every telegraph. Competent: corridor spacing (GL-E2), never the main threat. Advanced: absent from set pieces. Swarms are **fragile**; latchers **standard**.

**Ambient rule.** Swarms in debris rafts and decorative shallows (VK boom, Whisperflow ME01) are Passive ambient and do not engage.

### 5.2 Field Goblins (low)

**Ecology.** Small, quick tunnel raiders nesting in old grain pits, burned barns and wartime depots, building traps and nests from broken farm tools and stolen sacks. They watch farms closely and copy what they see (WC.4: goblin field with a marker-height notch). They are thieves, not killers, but they fight to defeat once engaged.

**AI role.** Aggressive within the camp or tunnel volume. Raiders may **target props** (tool pile GL-E4c, tree branches TB-E1, sacks SM-E1) until engaged.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Scrapper** | Melee with hoe, broken tool or sickle; drops sacks to engage; ambushes from holes | Tool raised overhead (**1.0 s**), then a chop. Ambush: dirt trickles from the hole (**1.0 s**) | Step aside; watch the holes | Novice |
| **Trapper** | Keeps distance; sets **rake traps** (visible tines, small mound; **2.0 s** set, crouch-and-scrape); throws a sickle (**1.2 s** windup, short range); keeps scrappers between itself and the player | Set: kneel and scrape. Throw: arm back | Kill it first or stay off the straw/ash; traps are always visible once set | Novice–Competent |
| **Sack-King** (elite) | Flail melee; summons; room hazard. Full kit in Act I §A7 | Threshing: flail spin with rising whistle (**1.5 s**), front cone. Call the heaps (75%, 40%): pot-lid bang (**1.0 s**), 2 scrappers from sack nests. Bin pull (50%): grain ring trickles (**2.0 s**), slow ground + light DoT ~6 s, persists | Move to his side or back; clear adds; stay out of the grain | Novice (MQ2 only) |

**Traps (one generic definition, four presentations; Act I §A12).** Rake bed (light damage, 1 s stagger), twine scythe (1.2 s creak, moderate), harrow (1.5 s creak and dust, heavy on the shadow strip), pan alarm (no damage; wakes a group). Root trap variant (UR-E1: roots 2 s with a small hit). All visible to a player who looks; none can kill above 25% HP.

**Band tuning.** Novice core; Competent filler (GL-E4c, TB-E1). Scrappers **fragile-standard**; trappers **standard**; Sack-King **elite**, 60–90 s, first attempt ends at 30–60% HP.

**Respawn.** After SM S06 the depot is a revisitable dungeon; goblins respawn as world creatures and the Sack-King is replaced by a non-elite **heap-boss** scrapper (crown passes on). **Scatter rule:** goblin crews "scatter" only after all members are defeated (TB-E1), as a group bark. This is not fleeing.

### 5.3 Ash Hounds (low)

**Ecology.** Lean, ash-grey pack dogs denning in burned culverts and trench lines on the Ashen Flats. Their coats hold lung-irritant ash (dossier §VIII). They foul water by dragging carcasses into dens (HW site B), which is the ordinary cause the evidence rule needs.

**AI role.** Aggressive pack. Runners circle before lunging; shakers hang back.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Runner** | Flanks, circles, lunges | Low crouch (**0.8 s**), then a lunge (light) | Step aside; keep runners in front | Novice–Competent |
| **Ash-shaker** | Holds back; makes area denial | **Cloud**: whole-body shake (**1.5 s**); grey cloud **3 m radius, 4 s** | Walk out. Effect: **light damage over time while inside** (canonical; see §12 I-6) | Novice–Competent |
| **Den Mother** (elite) | Guards the den; heavier cloud; charge | **Charge**: scrapes twice (**1.5 s**), straight charge. **Ash storm**: larger cloud (5 m) with a **2.0 s** build | Sidestep the charge; leave the storm | Novice (optional only) |

**Band tuning.** Novice teaching family for area denial (HW-E2, 45–60 s). Competent repeat on the plot fix (GL-E4b, ~60 s; a scrub den, not the burned culvert). **Canonical ruling:** the burned-culvert den (P14 B3) belongs to MQ3 only; Unreplanted does not use Ash Hounds. Den Mother optional at Novice (60–90 s, avoidable), **one-time** (`HW_DEN_CLEARED` keeps the den empty).

### 5.4 Mud Pipers (low)

**Ecology.** Squat amphibious reed-dwellers with throat sacs that **mimic voices** heard near water (Bryn's in MQ7, a cutter's in MQ11). They lure prey into reeds, then dive and come up under it. Mimicry is animal behaviour; they repeat sounds, not meaning (evidence rule).

**AI role.** Lure first (positional bark away from the real person), then Aggressive once the player is in the reeds; fight to defeat once engaged (DK-E1). Never flee.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Piper** | Calls in a borrowed voice from inside reeds; spit or lunge | Puffed throat and a rising reed note (**1.0 s**) | Trust the real person's position (DK-D5 "I won't shout"); step aside | Competent |
| **Bog-diver** | Submerges in ditches and margins and surfaces under the player or an NPC | Reed tremor and gurgle (**1.0 s**) before the dive; on approach a **V of ripples** (**2.0 s**) | Intercept the V; step off the surfacing point | Competent–Advanced |
| **Chorus-Piper** (elite) **[NEW placement proposal]** | Calls in **several** voices at once from different points in a reed bed; surfaces among them; summons 1–2 pipers | Each call point marks with a reed tremor (**1.5 s**); its own dive uses the bog-diver tell at **1.5 s** | Find the one tremor that moves; ignore the stationary calls | Competent (world elite) |

**Band tuning.** Competent family. DK-E1 is the first meeting (~40 s). DK-E2 wave 2 is the signature. MQ11 Far Racks pair is optional. **Chorus-Piper is unplaced in every package**; proposed placement in §11.3 (W-01).

### 5.5 Smugglers (mid)

**Ecology.** People: Sallow's Lock crews (rope-burned palms, hooded lanterns, superstitious habits copied from Sallow), the Drowned Lamb cellar crew, and Greyharrow Reach opportunists. They fight for pay and fear the fen more than the keepers.

**AI role.** Aggressive. Several patterns **target props first**: carts (NT thieves), lanterns (NT dousers), the near crank pawl (TF pry-men), the barge lines (CR-E3), record piles (CR-E2). Defeated at 0 HP with the ordinary defeat presentation (§8, CDR-1).

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Pole-man** | Holds paths; long reach sweeps; works props (cranks, barge) until engaged | **Cone**: plants the pole and leans back (**1.2 s**), wide sweep with **2 m push** (never into deep water). Advanced variant (CR-E3): pole set low (**1.2 s**), **trip** knockdown 1 s. Pry (TF): crouch with bar glint (**2.5 s**) | Step out of reach or behind; interrupt pries with any hit | Novice (NF, UL, NT) → Advanced (CR) |
| **Cutter** | Flanks, harries, double cuts; thieves and torch-bearers | Shoulder drop, blade low, or knife hand drawn back (**0.9–1.0 s**), then two quick cuts (moderate). Torch swing (**1.2 s**) leaves a short fire patch (CR-E2). Douser: raised wet sack while running (**1.5 s**) | Step aside; catch thieves during the 2 s rummage | Novice → Advanced |
| **Crew boss** (elite) **[PROPOSAL — DIRECTOR]** | Named crew leaders built on a standard base with more health and one signature move. **Rusk** (NF-E3, pole-man base): **double sweep**, two plants and leans (1.2 s each), second reversed. **Brack** (NT-E3b, cutter base, ~2× health): laughs and steps back (**1.0 s**) then a long lunge; once per fight throws a lantern: **ring** of fire shown (**1.2 s**), burning oil 3 m for 3 s | Read the second sweep; leave the ring | Novice (Rusk, Brack) |

**Band tuning.** Novice: NF-E1 is the "first humans" lesson: wider telegraphs, smarter spacing, 40–60 s, 60–80% HP remaining. UL and NT play at Milestone 1. Competent: TF juggle (priorities over damage). Advanced: CR siege (heat zones, trips, barge race; E3 ends at 55–75% HP). Pole-men **sturdy**; cutters **standard**; crew bosses **elite**.

**Proposal rationale.** Bible §10 lists Gideon Sallow as the family's elite. Phase 1.5 counts minibosses separately from elites. Rusk and Brack are already authored as tougher named leaders; formalising them as the elite variant frees Sallow to be a pure miniboss and keeps the variant count honest. Nothing in any package changes.

### 5.6 Reed Stalkers (mid)

**Ecology.** Long-limbed ambush predators that wait inside reed curtains and reed islands, with a throat sac that swells before a sticky tongue-lash. Lurkers lie submerged at reed edges. They nest in woven reed mats wedged in stone (Crestbridge piers). Drawn to quiet water near people.

**AI role.** Aggressive ambush, leashed to reed volumes; lurkers Defensive in edge water. Some **target props or NPCs** (FW withies, FW and SV crews).

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Stalker** | Leaps from reeds; tongue-lash pulls toward water | **Line**: reeds part in a straight line toward the player with a low croak (**1.2 s**; Advanced **1.0 s**), then a leap. **Pull**: throat swells with a gurgle (**1.0 s**), tongue-lash pulls **3 m toward water** | Step off the line; stand on stone footing (the pull breaks on firm stone) | Novice (NB, low density) → Advanced |
| **Lurker** | Submerged; surfaces to grab players standing in deep or edge water | **Ring/line**: bubbles in a ring or line toward the player (**1.5 s**), surfacing grab | Stay on dry stones; step off the bubbles | Novice–Advanced |
| **Old Mud** (elite) **[NEW placement proposal]** | An old, heavy stalker with a mud-caked hide; tongue-lash pulls 4 m and holds 2 s; summons no adds; leaps twice in a row | Double line: reeds part twice in sequence (**1.5 s** then **1.0 s**). Hold: throat swells and stays swollen (**1.5 s**) | Stand on stone; second leap lands where the first line pointed | Competent–Advanced (world elite) |

**Prop/NPC targeting.** Withy grip and throat-swell (**1.5 s**) before a withy is pulled (FW-E2). Nest pulse: mats shiver (**2.0 s**) before a new stalker drops (NB-E2); `cut_nest` (3 s) stops it.

**Band tuning.** **Canonical ruling: Reed Stalkers first appear in Night Bridge** (after MQ2). Every NB pocket has **at most 2 stalker-family creatures active at once**, and NB uses the **longer telegraphs** (leap line 1.5 s, tongue-lash 1.2 s, lurker bubbles 1.8 s). Competent core (GL-E3 45–70 s; FW-E1/E2). Advanced pressure on crews (SV-E2 ~60 s). **Old Mud is unplaced in every package**; proposed placement in §11.3 (W-02).

### 5.7 Water Wraiths, "drift" (mid)

**Ecology (author truth, bible §2.3, §2.5).** Imprints of heavy water, not souls. They form where grief-heavy water is trapped or churned (sluices, races, pools, drains, outfalls, the fen) and repeat shapes: a wet sheet over a person, an arm of water, a lantern held out. They never speak, never identify anyone and never carry anything.

**AI role.** **Place-bound Aggressive**: leashed to their water body plus ~3 m. **Re-form** about **20 s** after dispersal while the site condition holds. Never flee; dispersal is not death and re-forming is not respawning. They **will not path into banner-thistle smoke** (~4 m ring). **Changing the condition quiets the site** (D-6).

| Variant | Behaviour | Telegraph (canonical) | Counter | Bands |
|---|---|---|---|---|
| **Drift** | Lashes in a line; grasps nearby with cold that slows | **Formation** (not an attack): the water goes glass-flat and "stands up" (**1.5 s**); a cold-mist ring on the ground marks its reach. **Lash**: an arm of water rises (**1.0 s**), then lashes in a **line**. **Cold grasp**: the water around it rises in a ring (**1.2 s**); inside, a short "heavy water" slow | Stand outside the mist ring; step off the line; leave the pool water | Novice → Advanced |
| **Lantern-drift** | A drift with a cold light at its core; its light is its tell; pulse ring | **Lash**: the core light pulses twice (**1.2 s**) before the lash. **Pulse ring**: a ring of light on the ground (**1.5 s**), erupts | Watch the light; step out of the ring | Novice (NF-E4) → Advanced |
| *Small drift* (sub-form) | 60% size; MQ8 demonstration only | As drift, faster and fainter | — | Competent |
| *Wisp* (sub-form) | Harmless visible mist; never engages | — | — | Competent |

**Drift rules (from HW §B7, D-6, MQ8).**
1. **Disperse vs quiet:** dispersal opens a ~20 s **window** (pool slack and wrinkled, softmoss briefly lightens) in which work can be done. Damage cancels channels. The site's fix stops re-forming.
2. **Split (MQ8 only):** dispersing a drift at a flagged site spawns two small drifts at linked downstream points; dispersing one of those spawns two wisps; depth capped at 2.
3. **Tended state (post-MQ11):** tended drift are **Passive**; they drift like slow lanterns and engage only if attacked.
4. **Smoke:** a set-down smoke-pot or lit smoke stake makes a ~4 m volume drift AI will not enter. Lanterns lit in NT do not affect drift; in WD a dark lantern corner lets drift reach the door faster (presentation and pathing weight only).

**Band tuning.** Novice: the loop lesson (HW-E1: each dispersal 15–20 s; whole sequence 3–4 min; 50–70% HP). Competent: set-piece weather (TF, DK, WD, CN). Advanced: pressure and lanes (SV). Drift **standard**; lantern-drift **sturdy**.

### 5.8 Stillwater Serpents (high)

**Ecology.** Barrel-thick serpents of the deep fen pools, drawn to Wraith-choked water (dossier §VIII). Only head and forebody are ever fully visible; movement shows first in water and reeds. Silent above water.

**AI role.** Aggressive, **pool-bound** (sill, staging edge). They **submerge and resurface** as part of their pattern; that is not fleeing. On defeat they sink.

| Variant | Behaviour | Telegraph | Counter | Bands |
|---|---|---|---|---|
| **Serpent** (standard; SV-E3) | Breaches through the Long Sill; jams the gate and pushes progress back while at the sill | **Coil-rise** (line): body lifts (**1.5 s**), straight lunge 6 m. **Tail sweep** (arc): water bulges on its flank (**1.2 s → canonical 1.5 s**, see §12 I-5), arc behind it. **Submerge**: sinks; a swirl marks the resurfacing point (**2.0 s**) | Step off the line; leave the flank; stand clear of the swirl | Advanced |
| **Deep-Pool Serpent** (elite; FW-E3) | Arena elite with zone rules (stakes, soft mat, shallows, kerb). Full kit in Settlements file §FW.4.1: Strike (1.5 s line), Tail sweep (1.5 s arc, 3 m push into shallows), Coil-slam (P2+, 2.0 s shadow circle; none on a stake), Sound and breach (66%/33%, 2.5 s bubble ring), Drag (P3, 2.0 s, mat tilts toward kerb; stakes immune) | As listed | Stand on the stake discs; never thrown into deep water (kerb) | Competent (gated, §12 I-2) |

**Band tuning.** Deep-Pool Serpent: 3–4 min solo at Competent; Novice "possible but punishing" is **not** an acceptable first-time experience, hence the gate in §12 I-2. MQ11 Serpent: 2–3 min, ends at 50–70% HP, within a crew-defence set piece.

### 5.9 Wraith Lords (high)

One authored instance: **the Muster** (§7.3). No standard variant.

---

## 6. Wildlife combat behaviour

Wildlife are Hunting fauna (Hunting portfolio alert-and-movement framework, F2/F3/F4). They are **not counted** as families and have **no elite**. Default AI role is **Passive** or **Defensive**; each has one authored provoked state.

| Animal | Default role | Provoked / scripted states | Telegraph | Counter and punish | Appears |
|---|---|---|---|---|---|
| **Furrow Boar** | **Passive** (neutral) in fields and reed mats | **Crop-aggressive**: targets a grain stack or crop prop until engaged (TL-E4). **Territorial**: a sow alerted at close range (WC-E2) or a boar disturbed within 5 m of a dragged hurdle (FC-E2) turns Aggressive | **Charge**: paws the ground and lowers its head (**1.5 s**), straight-line charge; sow bristles and snorts (**1.2 s**) | Sidestep; it overruns and stands exposed (**~2 s**; sow 1.5 s). A player who stands still can lose TL-E4 | TL-E4 (required climax, 45–75 s), WC-E2 (optional), FC-E2 (optional); Hunting harvest afterwards |
| **Marsh Fen Goose** | **Defensive**: engages inside nest radius; never pursues past the reed edge or rag stakes | Nest defence only | Neck stretch and hiss (**1.0 s**) before a wing-beat (light; <5% HP per hit at Novice) | Back off: leaving the radius ends the fight. Avoidance is legitimate | TL-E1 (avoidable), FK-E1 (closed nesting ground; avoidable); FK flock is a Hunting resolve, not combat |
| **Bog-Touched Elk** | **Passive with alert/flight**: alert radius ~8 m (head snap, ears flat); flees directly away from the player | **Provoked** (attacked): fights to defeat with a lowered-head charge (**1.5 s**). **Flood-driven** (scripted, DK wave 3): runs a path down the orchard rows and charges along the dike crown at an NPC; hitting it once redirects it to the player | Charge as boar: sidestep, it overruns and stands exposed (~2 s) | MN S04 (herding test; killing it ends the test with `MN_ELK_KILLED`, not a failure); DK-E2 wave 3 (required, set piece) |

**Rules.** Wildlife never flee at low HP once fighting (Phase 1.3). Hunting resolution of fowl (FK) is a Hunting interaction, not a combat kill. Quest-spawned wildlife (MN elk) is one instance per player.

---

## 7. Bosses and minibosses (consolidated)

### 7.1 Gideon Sallow — miniboss (MQ10, `CR-E4`) `[ANTAGONIST]`

Source of truth: Act III §10.6.1. MQ4 shows him across the chamber with **no combat definition** (Act I §C7); that stands.

| Element | Consolidated spec |
|---|---|
| Arena | Gate Landing (Crest Hall area G), ~14 × 8 m stone stage; water on the long side, wade-depth basin with steps at each end; 2 bollards; 3 lanterns on ropes, one per third |
| Weapon | Boat-hook, 3 m reach, slow |
| **Hook Sweep** | Cone: hook drawn back, shoulders turn, wet-leather creak (**1.2 s**); 160° arc at 3 m. Most frequent |
| **Rope Cut** (P2+) | Looks up, flicks the hook; the lantern sways first (**1.5 s**); that third goes dim. In dim light he **whistles before every swing**. **Relight** the fallen lantern (2 s). Never more than two down |
| **The Shove** | Charge: plants the hook's butt, lowers shoulder, boot scrape (**1.8 s**); wet streak marks the line; 5 m charge, 3 m knockback. Over the edge = no damage, 6–8 s wade back. Bollard behind you stops it |
| **Chain Touch** | At 66% and 33%: backs to the gate chain, 2 s open hand, one superstitious line. Free opening; characterisation |
| Phases | P1 100–66% Sweep, Shove · P2 66–33% + Rope Cut, 2 pole-men one at a time up the far steps · P3 33–0% cadence +25%, one Rope Cut on entry |
| **Defeat** | Defeated at **0 HP**. **SX-2** (§8): on defeat the quest plays his scripted surrender (drops the hook into the basin, grips the chain) and spawns him non-hostile; event `cr.sallow_yield` fires on defeat → `CR-D6` |
| Solo target (Advanced) | 2.5–4 min; ends at 40–70% HP |
| Death | Respawn at the Keepers' Yard; barge stays secured, fire-lines stay cut; Sallow resets to full |
| Co-op | Shared; health scales per participant; Shove targets the farthest player |

**Reconciled:** the bible's "shove toward the water" and the global "never into deep water" rule are compatible because the basin is **wade-depth**; this is a zone requirement. Act III §10.13's yield mechanism is superseded by CDR-1: Sallow is defeated at 0 HP and his surrender is the quest's scripted on-defeat outcome (SX-2), shared only with Joss (SX-1).

### 7.2 Joss Garrow, "Old Lantern" — miniboss (OL, `OL-E2`)

Source of truth: Settlements file §OL.4.1.

| Element | Consolidated spec |
|---|---|
| Classification | **Human miniboss** with Wraith-adjacent mechanics. Bible §10 lists him in the Water Wraith elite slot; he is a **living man**, never "dispersed". Keep the bible's slot for counting; implement him as a human creature defeated at 0 HP, with the SX-1 scripted outcome on defeat (§8) |
| Arena | The willow bend (Old Lantern's bend): 4 raised stone **post footings** (ramped landward side), a heavy-water ford across the middle, deep side behind reeds (unreachable) |
| **Lantern sweep** | Cone of light settles (**1.5 s**); moderate. If the cone touches the ford, a **lantern-drift** forms there 3 s later (max 2). Fight him on the bank |
| **Rope cast** | Bark "Hold the line!"; pale line drawn to the player (**1.5 s**); snare drags 3 m toward him. Break: step onto a footing or land two hits |
| **Count the stroke** (P2+) | "One… two… three", 1 per second (**3 s**). On three, a cold pulse **7 m** from the ford, heavy unless on a footing |
| **Wade** (P3, < 25%) | "End of leg."; walks toward the deep side; a ring marks a spot on his path for the whole wade. Stand in it to stop him; if he reaches the reeds he fights knee-deep and drift keep forming |
| Player tool | Banner-thistle smoke at any footing once per phase (2 s): 10 s cloud; lantern-drift take extra damage; his sweep and rope tells +0.5 s; one lucid fragment |
| Phases | P1 100–60% sweep, rope · P2 60–25% + count · P3 < 25% + wade, count cadence ~14 s. No enrage |
| **Defeat** | Defeated at **0 HP**. **SX-1** (§8): on defeat the quest plays his scripted surrender (one knee, lantern set down, still lit) and spawns him non-hostile for the OL choice |
| Solo target | Milestone 1 dependable to early Competent: 3–4 min |
| Reset | Leaving the bend or dying resets him to full and his patrol walk; his drift disperse |

**Zone requirement (load-bearing):** every walkable point of the arena must be within **one count** (3 s of walking, minus 2 ticks of latency) of a post footing, and footings must be NavMesh-reachable by ramp. With unknown walk speed, author footings so no point is more than ~4 m from one; verify in the build.

### 7.3 The Muster — Act III boss (MQ11, `SV-E5`)

Source of truth: Act III §11.6. Bible §6.1 brief and §10 agree with it.

| Element | Consolidated spec |
|---|---|
| Read | Tall standing mass of fog and moving water carrying a dozen lantern-lights in a ragged line at shoulder heights; a hollow oar-knock sounds inside it when it counts. No face, voice or name |
| Arena | Heart pool: ~30 m circle, ankle-deep over firm bottom; **8 Marking Stones** on low plinths at ~11 m radius (walkable by click; no jump); 3 Braid inflows; centre 5 m "deep" over the convoy holes; barge ribs on the north side (block lantern-lines); exit via the Lantern Sluice (leaving does not reset for 20 s) |
| **Lantern-line** | 3–5 lanterns hang in a row; amber → white, water frosts (**2.0 s**); cold surge: moderate damage + **chilled** (slow, 4 s). Step 2 m aside or behind a rib |
| **Stroke-call** | Count of four (P3: three), one knock per ~**1.2 s**; a 2 m ripple ring under each player each knock erupts on the next knock (light); final knock lights the 6 m muster circle (heavy, ~30%) |
| **The drag** (P2+) | Lanterns swing to one player (**2.0 s**); current lines; tether pulls toward the centre at ~1.2 m/s. **Step onto a Marking Stone that reads true** (the 3 nearest moving inflows show water standing in the notch). Snaps the drag; the Muster **staggers 3 s** (bonus damage) |
| **Pulled under** | Reaching the centre: 35% max HP, spat out by a random stone. Never instant death |
| Phases | P1 100–70% lines (~12 s), stroke-call of four (~20 s) · transition: sinks to waist, 2 lantern-drift adds at dry stones · P2 70–35% + drag (~25 s); living adds add a second lane · P3 35–0% count of three, two crossing lanes 0.6 s apart, drag ~18 s, no adds |
| Defeat | **Disperses**: lanterns go out outermost first; no loot; nothing evidentiary. Then `S07_heart_stone` (seat the post) is the change of conditions |
| Solo target (Advanced, with cooked food) | 6–8 min; a reader of counts and stones ends at 25–60% HP; a first-timer may die once or twice |
| Death | Respawn at the Lantern Sluice landing; resets to the top of the phase died in (100/70/35%); gates stay open; evacuees stay safe |
| Co-op | Shared; health scales; drag rotates targets, never two at once; rings under every player; each seats their own post |

**Reconciled / flagged.**
- The drag's counter needs **per-stone "reading" state** keyed to inflow proximity, a **tether** status and a **stagger** state (§9).
- Distance budget: from any point in the ring a reading stone must be reachable inside the drag's effective window. The 3 reading stones are fixed by inflow position, so the worst case is a player on the far side from all three inflows. **Zone requirement:** place the three inflows so no arena point is more than ~10 m (walking, against a 1.2 m/s pull) from a reading stone; verify in the build.
- Fight length (Act III open decision 1): **keep 6–8 min**; phase checkpoints make it fair.
- The count of four is taught at the evacuation (SV `S02` trance warning) and foreshadowed by Joss's count of three; Muster P3 drops to three. Consistent; no change.

---

## 8. Defeat (CDR-1, binding 2026-11-03)

This section replaces the former "Non-lethal human defeat [PROPOSAL — DIRECTOR]" rule, which is **superseded by CDR-1** (`Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md` §1, §3.1, §4).

**Rule.** Every hostile creature in Lowmark, human, animal, monster or spirit, is defeated at **0 HP**. No health threshold ends a fight early; no creature yields, flees, limps away or breaks off because of its health. Leash/reset is ordinary RPG behaviour and stays. Drift re-forming while its site condition holds is a place rule (§5.7, §10), not a disengagement.

| Element | Rule |
|---|---|
| Threshold | None. Every creature is defeated at 0 HP |
| Presentation | **Ordinary defeat presentation** for every human (Smugglers variants, crew bosses): falls, fades after the standard corpse time. No downed state, no tied props, no dialogue with a defeated ordinary enemy, no body in later visits. Drift disperse; serpents sink; animals are defeated and can be harvested where the economy allows |
| Combat state | Ordinary defeat. Content no longer requires **CombatIncapacitated** for any human (rulings §5 G-8) |
| XP, loot, co-op | Combat XP and ordinary loot at defeat, as for any enemy; nothing evidentiary drops. Shared world state; every participant on the step gets credit |
| Step completion | Any step that completed "on yield" completes **on defeat** |
| Allies | One short, sober ally line after a human fight is enough where an old "they'll live" beat stood. Allies do not comment on mercy |
| Non-combatants | Never targetable (unchanged) |
| Testimony | Combat never reveals evidence. Facts once given by a defeated ordinary enemy are re-sourced (rulings §3.2). MQ4: Maelin names Sallow at dawn (T-1); Rusk fights to 0 HP |

**Scripted story exceptions (quest events, not combat rules).** Two Lowmark creatures have a quest-scripted outcome **on defeat**. Each is defeated at 0 HP like any other creature; the quest's on-defeat hook then plays a scripted outcome instead of the ordinary defeat presentation and spawns the person as a non-hostile NPC for the next beat.

| Id | Creature | Quest / encounter | Outcome on defeat |
|---|---|---|---|
| **SX-1** | Joss Garrow, "Old Lantern" | OL `S04_joss` (`OL-E2`) | When Joss is defeated, the quest plays his surrender: he goes down to one knee and sets the lantern down, still lit; the drift-hold on him breaks. The OL choice (bring him in alive / bring back only his lantern) follows unchanged |
| **SX-2** | Gideon Sallow | CR `S06_sallow` (`CR-E4`) | When Sallow is defeated, the quest plays his surrender: he drops the hook into the basin and grips the gate chain ("Enough. I'm done."). `cr.sallow_yield` fires on defeat; `CR-D6` follows unchanged |

**Runtime need (Systems Engineer).** One small need replaces the former health-threshold defeat event: a **quest on-defeat hook for named creatures** (used only by SX-1 and SX-2) that plays a scripted outcome and spawns the NPC non-hostile. No threshold parameter, downed state, tied prop or hostile→neutral swap for ordinary enemies. See `Quests/Caelmor_Combat_Ranged_Release_Engineering_Handoff.md`.

---

## 9. Status effects and runtime needs

| Effect | Used by | Behaviour | Combat-state note |
|---|---|---|---|
| **Slow (movement)** | heavy water (drift cold grasp), leech latch, grain pile, ford, shallows, Muster "chilled", flooded circle | Movement speed reduced for a duration or while in volume | No state change; a movement modifier |
| **Damage-over-time zone** | ash cloud, Den Mother storm, grain pile, burning oil, CR heat zones, fire patches | Ticks damage while inside a volume | Volume rule |
| **Push / knockback** | pole sweep (2 m), tail sweep (3 m), Shove (3 m), jam swing, H2 tree fall, quench shard | Server-side forced move along a vector; never into deep water | Brief; no state |
| **Knockdown (≤ 1 s)** | CR-E3 trip | Cannot act or move for ~1 s | **Ruling needed:** CombatRestricted allows movement. Either add a timed movement block inside Restricted or use Incapacitated with an authoritative timed recovery. Recommend the first |
| **Stagger (≤ 1 s)** | rake bed (1 s), Muster stagger (enemy, 3 s) | Player: interrupts channels, blocks attacks briefly. Enemy: exposed, takes bonus damage | Player: CombatRestricted. Enemy: a vulnerability flag |
| **Root (≤ 2 s)** | UR rake-tine trap | Cannot move; can attack | Movement block only |
| **Pull / tether** | stalker tongue-lash (3 m snap), Joss rope (3 m drag), Muster drag (continuous), FW drag (mat tilt) | Forced movement toward a point; broken by entering a tagged safe volume or by two hits (rope/latch) | Needs **safe-ground volume tags** (stone footing, stake, reading stone) |
| **Smoke avoidance** | banner-thistle pot, Watcher smoke | Volume that drift pathing will not enter | Pathing rule |
| **Re-form** | all drift | On dispersal: despawn, timer (~20 s), respawn at site anchor while site condition is false | Spawn rule keyed to drift-site state |
| **Split** | MQ8 drift | On dispersal at flagged site: spawn N smaller at linked points, depth ≤ 2 | Spawn rule |
| **Prop targeting** | goblins (tools, branches), smugglers (carts, lanterns, pawl, barge, records), stalkers (withies), elk (Bryn) | AI selects a world object as target until engaged | AI behaviour |
| **NPC protection with slip** | DK Bryn, TF Imber, SV crews, FW cutters | Hostile hit or lunge-end within 2 m triggers a slip/pause event; NPC is invulnerable | NPC state |
| **Invulnerable allies** | Teague and Dace (NT), Lessa (FW), Orrin, Hesketh, Sedge | Cannot be targeted or downed; may slow enemies (NT lanes) | NPC flag |
| **Zone-tagged damage multipliers** | FW stakes/mat/shallows, Muster stones, Joss footings | Per-volume immunity or multipliers for named attacks | Volume tags |

---

## 10. Drift-site register

**State model (D-6, bible §9.2).** **Active**: drift spawn on the site's condition. **Quieted**: no spawn. **Tended** (post-MQ11, Tend/Shared only): rare Passive drift that engages only if attacked; Watchers patrol. **Closed** (MQ11 Seal): area behind a Keeper boundary; heavy water gone outside it. **Step-scoped**: drift that exist only during a quest step and leave no world state. **Presentation-only**: heavy-water signs (cold mist, glassy water, rotting softmoss) with no hostile spawn. All state is per player.

**Conditions:** *dusk* (dusk window), *flush* (flush nights; only before MQ4 completion), *backwater* (backwater nights; MQ4 completion → MQ11 completion; Act II §A2.2), *night*, *step* (only during the named step).

| Site id | POI / area | Spawn conditions while active | Encounters | State change (quest/step) | After MQ11: **Seal** | **Tend** | **Shared** |
|---|---|---|---|---|---|---|---|
| `drift.orchard_pool` | P16 A3 root pool | dusk, while sluice shut | HW-E1 | → quieted at HW `S02a_drain` (first quieted site) | quieted | quieted | quieted |
| `drift.flats_ditch` | P14 edge B2 ditch | flush, backwater: **presentation-only** (ditch runs back; uphill ripples); no hostile spawn | — | → quieted at SV `sv.fen_holds` **[resolution, §12 I-10]** | quieted | quieted | quieted |
| `drift.widows_step` | P22 C2–C3 causeway and bend | dusk, flush, backwater | HW-E4; SV lane pockets nearby | Stays active through Act I–II; MQ11 sets ending state | quieted | **tended** | **tended** |
| `drift.reed_lantern_bend` **[NEW id]** | Bend between P21 and P22 (ME10 "heavy bend below the Post"; names the bible §4.1 place "Reed-Lantern Bend") | dusk, from MQ3 completion | ME10 optional drift (1) | MQ11 sets ending state | quieted | **tended** | **tended** |
| `drift.bramblelock_pool` | P08 W1 weir pool | flush: **presentation-only** gathering (MQ4 Beat 2, non-engaging) | — | → quieted at NF `S11_dawn` (either `LM_LOCK_STATE`) | quieted | quieted | quieted |
| `drift.hollow_lock_chamber` **[NEW id]** | P09 L2 lock chamber | **step-scoped** (NF `S08_crank` while gates churn) | NF-E4 | Sinks at third crank segment; no world state | — | — | — |
| `drift.drowsebank_race` | P11 C race | **step-scoped** to TF `S08_hold` (forms only during the hold) | TF-E3b | → quieted at TF `S10_close` | quieted | quieted | quieted |
| `drift.orchard_dike` | P16 C Long Bank and far ditches | backwater | DK-E2 (waves 1, 3) | Stays active after MQ7; → quieted at MN `S00_book` (Sedge, unsigned) | quieted | quieted | quieted |
| `drift.heartlands_field_ditch` **[NEW id]** | A Heartlands field ditch (MN area B; see Zones M-sites) | dusk, backwater: **presentation-only** (cold mist, darkened softmoss) | — | → quieted at MN `S00_book` | quieted | quieted | quieted |
| `drift.unburnt_circle_pool` **[NEW id]** | P26 pool | dusk, backwater: **presentation-only** (no spawn: ME06 child inside the circle) | — | → quieted at MN `S00_book` | quieted | quieted | quieted |
| `drift.mantle_channel` | P24 E heavy pool and G lower pools | always (heavy pool) | MN-E1, MN-E2 (split) | → quieted at MN `S07_demo` (Sedge's quieting) | quieted | quieted | quieted |
| `drift.whispering_door_cellar` | Whispering Door farmhouse yard drain (M01) | night, from MQ4 completion | WD-E1–E3 | → quieted at WD `S07_quiet` | **as left** **[resolution, §12 I-11]** | as left | as left |
| `drift.watergarden_outlet` | P23 E outfall pool | always (heavy, turning); from game start | CN-E1, CN-E1b | → quieted at CN `S04_boat` | as left | as left; if CN completed → **tended** | as left; if CN completed → **tended** |
| `drift.old_lantern_bend` | Old Lantern's bend (M05 D) | night (Joss's lantern) | OL-E1 (shelter), Joss's lantern-drift | → quieted at OL `S07_book` | as left (active if OL not done) | as left | as left |
| `drift.far_leg` **[NEW id; replaces Old Lantern's bend as the residual]** | Two pockets on the far leg return path (M05 E) | Before MQ11: wakes only for a lit lantern carried past (OL lantern-only branch). **After MQ11: active at dusk** | OL-E3; post-MQ11 world pockets | MQ11 completion → active (residual) | **active** | **active** | **active** |
| `drift.stillwater_deep` | P30 heart pool and deep holes | Presentation "worse" from MQ4 dawn; hostile spawns **step-scoped** to SV `S06` | SV-E5 (Muster) | MQ11 choice | **closed** | **tended** | **closed** |
| `drift.stillwater_margins` | P30 lanes, Braid gates, near margins, remembrance channel | Step-scoped during SV `S02`–`S05` | SV-E1, E3, E4 | MQ11 choice | quieted | **tended** | **tended** |
| `drift.residual_a` / `_b` | Per ending (Act III §E.1.2): Seal = 2 outer reed-pools at the boundary; Tend = 2 far-margin pockets beyond the channel; Shared = 1 at the boundary, 1 far margin | dusk | Post-arc world pockets (2–3 drift, 1 lantern-drift) | Created at MQ11 completion | **active** | **active** | **active** |

**Residual count check (bible §9.2, Act III §E.1.2).** Every ending keeps **three** active heavy-water sites for progression: `drift.far_leg` plus the two residual pockets. If the player never completes OL, `drift.old_lantern_bend` is also active, which is a fourth site for that player only; acceptable (it is optional content they have not done).

**Sites that are not drift sites (checked):** Whisperflow dead spot and ME08 lagging pool (presentation only, no state); FK hush (a flush event; no drift); NT boil (river mechanics); MQ5 culvert (vermin and predator only; Act II §A2.7); Listening Steps (stillest water in the Vale); Crest Hall water-gate (the MQ10 stilling is sound only).

---

## 11. Encounter-pocket index

**Respawn rules.** **STEP**: spawns on step entry; only authored waves/re-forms during the step; gone when the step completes. **→WORLD**: after its step, the area keeps an ordinary population of the same families on the standard world timer. **ONCE**: never respawns for that player. **SITE**: governed by the drift-site register. **OPT**: optional pocket (still follows its respawn rule).

### 11.1 Main quests

| Id | Step gate | Place | Families / variants | Band | Respawn |
|---|---|---|---|---|---|
| TL-E1 | TL `S03_find_old_post` | P04 F reed walk, goose nest | 2 Marsh Fen Goose | Novice | OPT; nest remains (Defensive wildlife) |
| TL-E2 | TL `S04_clear_footing` | P04 G old footing shallows | 3 swarm (Silt Swimmer), 1 latcher | Novice | STEP → WORLD |
| TL-E3 | TL `S04b_wreck` | P04 H / P12 wreck shallows | 1 latcher, 2 swarm | Novice | OPT; STEP → WORLD |
| TL-E4 | TL `S08_high_ground` (3rd sack) | P04 field edge → J high landing | 1 Furrow Boar (crop-aggressive) | Novice | STEP → WORLD (Passive boar) |
| SM-E1 | SM `S02_descend` | P02/P07 D hill passage | 2 scrapper | Novice | STEP → WORLD |
| SM-E2 | SM `S03_sorting_hall` | P07 E Sorting Hall + rake beds | 1 trapper, 2 scrapper | Novice | STEP → WORLD; disarmed traps persist per player |
| SM-E3 | SM `S04_warren` | P07 G bin route side holes | 2 + 2 scrapper (ambush pairs) | Novice | STEP → WORLD (root route skips one pair) |
| SM-E4 | SM `S06_sack_king` | P07 J throne room | Sack-King + 2 scrapper (+2 called) | Novice | ONCE; heap-boss → WORLD |
| SM-E5 | SM `S04_warren` | P07 H Larder | 1 trapper, 1 scrapper, rake bed | Novice | OPT; → WORLD |
| HW-E1 | HW `S02a_dusk` / `S02a_first_drift` | P16 A3 root pool | 2 drift | Novice | SITE `orchard_pool` |
| HW-E2 | HW `S02b_den` | P14 B3 burned culvert mouth | 2 runner, 1 ash-shaker | Novice | STEP → WORLD (Flats packs); den area ONCE if HW-E3 cleared |
| HW-E3 | HW `S02b_den` (optional) | P14 B3 inner chamber | Den Mother + 1 runner | Novice | OPT; ONCE |
| HW-E4 | HW `S02c_smoke` / `S02c_walk_out` | P22 C2–C3 causeway, bend | waves 2/2/3 drift | Novice | SITE `widows_step` |
| NF-E1 | NF `S04_lookouts` | P10 T3 Cut mouth towpath | 1 pole-man, 1 cutter | Novice (M1) | ONCE |
| NF-E2 | NF `S06_yard` | P09 L1 yard | A: 2 pole-man + 1 cutter; B: 2 cutter (shed ambush) | Novice (M1) | ONCE |
| NF-E3 | NF `S07_winding_floor` | P09 L3 winding floor | **Rusk** (crew boss) + 2 cutter | Novice (M1) | ONCE |
| NF-E4 | NF `S08_crank` | P09 L2–L3 crank platform | W1 2 cutter; W2 2 lantern-drift; W3 2 pole-man + re-form | Novice (M1) | ONCE (humans); SITE `hollow_lock_chamber` (step-scoped) |
| GL-E1 | GL `S04_dig` (dig 3) | P03 Rebirth Fields hedge, shaft mouth | 2 swarm (Skitter) | Competent | STEP → WORLD |
| GL-E2 | GL `S05_culvert` | P13 I2 long run | 3 swarm + 1 latcher | Competent | STEP → WORLD |
| GL-I3 | GL `S05_culvert` | P13 I3 low run | Skitter stragglers | Competent | → WORLD |
| GL-E3 | GL `S05_culvert` | P13 I5 reed shaft | 1 stalker, 1 lurker | Competent | ONCE (stalker does not respawn) |
| GL-E4a | GL `S07_fix_circle` | P13 I6 grate chamber | 2 swarm | Competent | STEP |
| GL-E4b | GL `S07_fix_plot` | M-site Joric's plot scrub (beside P20) | 2 runner, 1 ash-shaker | Competent | STEP |
| GL-E4c | GL `S07_fix_dike` (night) | P03 field hut tool pile | 2 scrapper, 1 trapper | Competent | STEP |
| TF-E1 | TF `S03_repair` | P11 C race shallows at footbridge | 2 swarm | Competent | STEP → WORLD |
| TF-E2 | TF `S04b_fight` (optional) | P11 B mill floor, night | 1 pole-man, 1 cutter | Competent | OPT; ONCE |
| TF-E3a | TF `S08_hold` | P11 C gate, footbridge, G far bank | 3 pole-man (2 pry, 1 far crank), 1 cutter | Competent | ONCE |
| TF-E3b | TF `S08_hold` | P11 C race | 1–4 drift (one per band reached, min 1) | Competent | SITE `drowsebank_race` |
| DK-E1 | DK `S02c_stakes` | P16 G reed margin | 2 piper | Competent | STEP → WORLD (pipers in margin) |
| DK-E2 | DK `S05_defend` | P16 C Long Bank, G reeds, ditch | W1 2 drift; W2 2 piper + 1 bog-diver; W3 1 elk (flood-driven) + 1 drift | Competent | STEP; drift via SITE `orchard_dike` |
| MN-elk | MN `S04_elk` | P24 E heavy pool | 1 Bog-Touched Elk (quest instance) | Competent | ONCE |
| MN-E1 | MN `S07_demo` | P24 E heavy pool | 1 drift | Competent | SITE `mantle_channel` |
| MN-E2 | MN `S07_demo` (optional) | P24 G lower pools | 2 small drift → wisps | Competent | STEP |
| BF-E1 | BF `S02_climb` (fallback ford only) | P29 B plunge-pool ford | 2 swarm | Competent | OPT; → WORLD |
| CR-E1 | CR `S03_firelines` | P02 Crest Hall D undercroft aisle | 2 cutter | Advanced | ONCE |
| CR-E2 | CR `S04_records` | P02 Crest Hall D record room | 2 cutter (torch-bearers) | Advanced | ONCE |
| CR-E3 | CR `S05_water_gate` | P02 Crest Hall F water-gate hall | 3 pole-man, 2 cutter | Advanced | ONCE |
| CR-E4 | CR `S06_sallow` | P02 Crest Hall G gate landing | **Gideon Sallow** + 2 pole-man (P2) | Advanced | ONCE (resets on death) |
| SV-E1 | SV `S02_evacuate` | P30 Cutters' Causeway, lanes, huts; trance pockets | 5 pockets × 2–3 drift; 1 lantern-line hazard per lane | Advanced | SITE `stillwater_margins` (step-scoped) |
| SV-E1b | SV `S02_evacuate` | P06 B Far Racks | 2 piper | Advanced | OPT; STEP |
| SV-E2 | SV `S03_gate1` | P30 E Reedmere Weir | 2 stalker, 1 lurker | Advanced | STEP |
| SV-E3 | SV `S04_gate2` | P30 F Long Sill | drift wave; 1 Stillwater Serpent | Advanced | STEP (drift); ONCE (serpent) |
| SV-E4 | SV `S05_gate3` | P30 G Lantern Sluice | 2 drift waves, 2 lantern-drift | Advanced | STEP |
| SV-E5 | SV `S06_muster` | P30 H heart pool | **the Muster** (+2 lantern-drift at 70%) | Advanced | ONCE (phase checkpoints on death) |

MQ12 has no combat. MQ8 and MQ9 are the designed combat valley.

### 11.2 Side quests and micro-events

| Id | Step gate | Place | Families / variants | Band | Respawn |
|---|---|---|---|---|---|
| WC-E1 | WC `S03_barns` (WC unlocks after MQ2) | P20 burned barn row (two barns), Heartlands–Ashenstead edge | 3 scrapper, 1 trapper (melee, or the optional borrowed hunter's short bow; CDR-2) | Novice | STEP → WORLD (P20 goblin camp until UR changes it) |
| WC-E2 | WC `S06a_hunt` (if sow taken) | M03 scrub margin bed | 1 Furrow Boar sow (territorial) | Novice | OPT; ONCE (Hunting opportunity state) |
| BW-E1 | BW `S02_free_jam` | M04 scour pool | 5 swarm (Skitter) | Novice | STEP → WORLD |
| BW-H1/H2 | BW `S02` / `S04` | M04 jam swing; leaner fall | hazards | Novice | ONCE |
| FK-E1 | FK `S02_fowl` (closed ground) | P01 D reed margin nesting section | 2 Marsh Fen Goose | Novice | OPT; nest remains |
| FK-E2 | FK `S02_fowl` (optional) | P01 E recovery shallows, deep end | 1 latcher | Novice | OPT; → WORLD |
| BP-E1 | BP `S01_backwater` | P01 tan-yard E backwater | 4 swarm (Skitter) | Novice | STEP → WORLD |
| HS-H1 | HS `S03_crack` | P02 forge quench trough | hazard (shard lane) | Novice | Repeatable presentation |
| SB-H1/H2 | SB climb | P25 second landing; joist route | rotten boards; pigeon burst | Novice | ONCE per board |
| UL-E1 | UL `S01_way_in` (force) | P18 C stair alcove | 1 pole-man (door-man), 1 cutter | Novice (M1) | OPT; ONCE |
| UL-E2 | UL `S01`/`S04` (force, cellar attack, or ledger up the stair) | P18 D cellar market | 1 pole-man, 2 cutter | Novice (M1) | OPT; ONCE |
| UL-E3 | UL river door outside the skiff window | P18 F tunnel water | 2 latcher, 1 swarm | Novice | OPT; → WORLD |
| NB-E1 | NB `S02_war_face` | P02 underside D pier 2 reed island | 1 stalker + 1 lurker (max 2 active; family intro, long tells) | Novice | STEP → WORLD (reduced) |
| NB-E2 | NB `S04_cramp_face` | P02 underside F pier 3 + nest | stalkers from the nest, **never more than 2 active**, until `cut_nest` | Novice | STEP; nest ONCE |
| NB-E3 | NB platform fallback (pier 2→3 ride) | P02 underside hanging platform | 2 stalker | Novice | STEP |
| UR-E1 | UR `S02_nest` | M-site Joric's plot D burrow | 3 scrapper, 1 trapper (root traps) | Novice–Competent | ONCE |
| UR-E2 | UR `S03` (revised) | M-site Joric's plot E corner culvert | **Not Ash Hounds** (ruling: the culvert den is MQ3's). Recommended: 1 Field Goblin trapper + 2 scrapper lookout crew from the P20 camp, or as the revised UR package specifies | Novice–Competent | ONCE |
| NT-E1 | NT `S02_first_watch` | P19 B cart ring → D reed edge | 3 cutter thieves, one at a time | Novice (M1) | ONCE |
| NT-E2 | NT `S03_second_watch` (cut mooring) | P19 C dark landing | 2 pole-man | Novice (M1) | OPT; ONCE |
| NT-E3a | NT `S04_third_watch` wave 1 | P19 B dark lanes | 2 cutter (dousers), 1 pole-man | Novice (M1) | ONCE |
| NT-E3b | NT `S04_third_watch` wave 2 | P19 B dark lanes | 2 pole-man + **Brack** (crew boss) | Novice (M1) | ONCE |
| NT-E4 | NT `S02b_bluff` (optional) | P19 E bluff camp | 2 cutter, 1 pole-man (Defensive) | Novice (M1) | OPT; camp → WORLD (2–3 opportunists, Defensive) |
| FW-E1 | FW `S02_cutters` (group 3) | P06 E cutters' places | 2 stalker, 1 lurker | Competent | STEP → WORLD |
| FW-E2 | FW `S03_hold` | P06 B withy line | W1 3 stalker; W2 3 stalker + 1 lurker | Competent | STEP (waves repeat with one fewer if < 3 withies) |
| FW-E3 | FW `S04_serpent` | P06 F the staging | **Deep-Pool Serpent** (elite) | Competent | ONCE (resets if unengaged 30 s) |
| OL-E1 | OL `S02_shelter` | M05 C reed shelter | 2 lantern-drift | Novice–Competent | ONCE (first pass) |
| OL-E2 | OL `S04_joss` | M05 D willow bend | **Joss Garrow** (+≤2 lantern-drift from the ford) | Novice (M1)–Competent | ONCE (resets on leave/death) |
| OL-E3 | OL `S06_home` (lantern-only) | M05 E far leg return path | 2 drift (one per pocket) | Novice–Competent | SITE `far_leg` |
| UC-E1 | UC culvert step (drained) | P28 H Hazel Culvert puddles | 4 swarm (Skitter), 1 latcher | Competent | STEP → WORLD |
| TB-E1 | TB `S01_goblins` (dusk) | P27 tree, B goblin path | 2 trapper, 1 scrapper | Competent | ONCE |
| WD-E1 | WD `S03_defend` wave 1 | M01 Whispering Door farmhouse yard drain | 2 drift | Competent | SITE `hobb_cellar` |
| WD-E2 | WD `S03_defend` wave 2 | M01 drain, pump trough | 3 drift (one targets a lantern pole) | Competent | SITE `hobb_cellar` |
| WD-E3 | WD `S03_defend` wave 3 | M01 yard | 2 drift, 1 lantern-drift | Competent | SITE `hobb_cellar` |
| WD-E4 | WD `S05_drain` | M01 drain silt pools, valve | 3 swarm, 1 latcher | Competent | ONCE (drain closed after S06) |
| CN-E1 | CN `S03_boards` | P23 E outfall pool → D outfall head | 2 drift, re-forming (max 2) | Novice–Competent | SITE `watergarden_outlet` |
| CN-E1b | CN `S03_boards` (2nd board) | P23 D | 1 lantern-drift | Novice–Competent | SITE |
| FC-E1 | FC `S01_clear` | M02 Lark low field standing pools | 2 swarm (Silt Swimmer), 1 latcher | Novice–Competent | ONCE |
| FC-E2 | FC `S01_clear` (optional) | M02 reed mats | 1 Furrow Boar (territorial within 5 m of a dragged hurdle) | Novice | OPT; → WORLD wildlife |
| ME10 | ME10 at dusk (after MQ3) | Reed-Lantern Bend | 1 drift (optional; Watchers can smoke it) | Novice | SITE `reed_lantern_bend` |

SB, VK and the other micro-events have no hostile encounters (VK raft Silt Swimmers are Passive ambient).

### 11.3 World pockets and proposed elite placements **[PROPOSAL — Gameplay Designer]**

| Id | Place | Unlock | Content | Band | Respawn |
|---|---|---|---|---|---|
| W-01 **Chorus-Piper** | P16 G reed margin between orchards and river | MQ7 completed; dusk | Chorus-Piper + 2 piper | Competent | WORLD elite (long timer) |
| W-02 **Old Mud** | P06 Reedmere cutting grounds edge (Hookreed side), off the evacuation lane | MQ11 completed (before that the area is an evacuation route) | Old Mud + 1 lurker | Advanced / post-arc | WORLD elite (long timer) |
| W-03 heap-boss | P07 J throne room | SM completed | heap-boss scrapper + 2 scrapper, traps reset | Novice | WORLD |
| W-04 Flats packs | P14 trench line and Ashen Flats | MQ3 completed | 2 runner + 1 shaker packs | Novice–Competent | WORLD |
| W-05 Barn goblins | P20 burned barn row | MQ2 completed (WC) | scrapper/trapper crews | Novice | WORLD until UR completion, then thinned (one crew) |
| W-06 Residual drift | `drift.far_leg`, `drift.residual_a/_b` | MQ11 completed | 2–3 drift, 1 lantern-drift per pocket, dusk | Post-arc | SITE |
| W-07 Shallows | Whisperflow shallows, Brookhollow backwaters, culverts | any | swarms and latchers | Novice | WORLD |

---

## 12. Inconsistencies found and resolutions

| # | Inconsistency | Packages | Resolution |
|---|---|---|---|
| I-1 | **Reed Stalkers' first appearance.** Bible §10 says MQ5; NB (after MQ2) and FW (after MQ3) use them. | Bible; Settlements NB.4, FW.4 | **Canonical ruling (review pass): first appearance is Night Bridge** (after MQ2), with **at most 2 active at once** and longer telegraphs (§5.6). FW moves behind MQ5 (I-2). Bible §10 "First seen" should read "NB". NB-E1 and NB-E2 bodies reduced accordingly (§11.2). |
| I-2 | **FW serpent tuning vs unlock gate.** FW unlocked after MQ3 (Novice) but its elite is tuned for Competent (Milestone 2). | Settlements FW.1, FW.4.1, FW.11 | **Canonical ruling: FW unlocks after MQ5.** After MQ3, Lessa's warning-post bark may hint at it without starting it. The elite-before-standard order is kept deliberately: the Deep-Pool Serpent is an arena-controlled preview with an ally calling tells and safe stakes; the MQ11 standard is harder in context (crew defence, no stakes). |
| I-3 | **Field Goblins' first appearance.** Bible says MQ2; WC (after MQ1) claimed "first goblin fight". | Bible §10; Work & Skills WC.5; Act I SM-E1 | **Canonical ruling: WC unlocks after MQ2** at the Heartlands–Ashenstead edge, so SM-E1 is always the first goblin fight and WC-E1 is a repeat that adds ground-trap reading. |
| I-4 | **Drift telegraph language** varies: "arm rises ~1.0 s" (HW), "glassy stillness ~1.5 s" (TF, MN), "stands up ~1.5 s + lunge ~1 s" (WD, CN), "water rises in a ring ~1 s" (SV). Lantern-drift: "core pulses twice ~1.2 s" (NF), "brightens and leans ~1.2 s" (OL), "ground ring ~1.5 s" (WD, CN). | Act I, II, III; Discovery; Settlements | Canonical drift grammar in §5.7: **formation** (glassy/stands up, 1.5 s, not an attack) + **lash** (arm rises, 1.0 s, line) + **cold grasp** (ring, 1.2 s, slow). Lantern-drift: **lash** (core pulses twice, 1.2 s; "brightens and leans" is the same tell) + **pulse ring** (1.5 s). Each package's wording maps to one of these; animation and VFX build one set. SV's "ring ~1 s" is raised to 1.2 s. |
| I-5 | **Serpent tail sweep** is 1.2 s in MQ11 and 1.5 s in FW, for a moderate hit with 3 m knockback. | Act III §11.5; FW.4.1 | Canonical **1.5 s** for both (displacement rule in §1). |
| I-6 | **Ash-shaker cloud** effect differs: attack speed reduced (HW), minor DoT (GL), hurts while inside 3 m (UR); radius 4 m (HW) vs 3 m (UR). | Act I HW-E2; Act II GL-E4b; Settlements UR-E2 | Canonical: **light damage over time while inside, 3 m radius, 4 s**. Drop the attack-speed modifier (it needs a new status type and teaches the same lesson). HW text "coughs (attack speed reduced)" becomes "coughs (takes light damage while inside)". Den Mother storm 5 m. |
| I-7 | **Encounter id collisions.** Bare `E1`–`E5` reused by TL, MQ10, MQ11 and most side quests. | All | Prefix rule in §0 (`TL-E1`, `CR-E1`, `SV-E1`, `UL-E1`…). Schema & Content Engineer to adopt or replace. |
| I-8 | **Non-lethal defeat implemented three ways with two thresholds**: Act I "yield", Settlements "downed" + "Joss yields at 0 HP", Act III "Sallow yields at 20%". | Act I §C7/C12; Settlements §0.3, OL; Act III §10.6, §10.13 | **Resolved by CDR-1 (2026-11-03).** No non-lethal defeat: every creature is defeated at 0 HP (§8). Only SX-1 Joss and SX-2 Sallow keep a scripted outcome on defeat via the quest's on-defeat hook. |
| I-9 | **Old Lantern's bend**: OL quiets it on completion; Act III ending matrix keeps it **active by design** as one of three residual sites in every ending. | Settlements OL.6–OL.7; Act III §E.1.2 | OL's quieting stands (it is the quest's promise: "the drift was gathering to the lantern"). The third residual site becomes **`drift.far_leg`** (the two return-path pockets OL already authors), active at dusk after MQ11 in all endings. Count of three preserved. Act III §E.1.2 row needs that edit. |
| I-10 | **Flats ditch has no quieting step.** Act I says it stays active until "Act II/III changes its conditions"; no Act II quest touches it; the ending matrix shows it quieted in all endings. | Act I header; Act III §E.1.2 | It quiets at MQ11 `sv.fen_holds` (the Braids take the pressure). It is presentation-only throughout (no hostile spawn is authored there). |
| I-11 | **Whispering Door farmhouse cellar after MQ11.** The matrix says "as left; if active, quieted", which would remove WD's drift if WD is played after MQ11; WD itself says the cause is local. | Act III §E.1.2; Discovery WD.8 | **"As left"** in every ending: the site stays active until WD `S07`. WD remains playable after MQ11. Act III §E.1.2 row needs that edit. |
| I-12 | **Unplaced elites.** Chorus-Piper (Mud Pipers) and Old Mud (Reed Stalkers) exist only in bible §10. | Bible | Proposed world placements W-01, W-02 (§11.3). If the Director prefers fewer world elites, both can be cut; the variant count drops to 19, still near range. |
| I-13 | **Smugglers' elite.** Bible lists Gideon Sallow as the family elite; Phase 1.5 counts minibosses separately. | Bible §10; Phase 1.5 §4.2–4.3 | Formalise **crew boss** (Rusk, Brack) as the elite variant **[PROPOSAL — DIRECTOR]**; Sallow is the miniboss only. |
| I-14 | **Joss in the Wraith elite slot** although he is a living man. | Bible §10; OL.4.1 | Keep the bible's slot for counting; implement as a human defeated at 0 HP (SX-1 on defeat) with Wraith-adjacent abilities (lantern-drift spawning). Flagged for Director awareness only. |
| I-15 | **Ashenstead and Riverglass tiers vs early gates.** Bible §4.1 puts Ashenstead Fields at mid tier and Riverglass Banks at mid–high; WC (after MQ2), UR and CN (after MQ3), MQ3 Widow's Step, MQ4 Hollow Lock and OL (after MQ3) all play there at Novice. | Bible §4.1; Work & Skills Q3 | Each subzone gets a **near band and a far band** (Zones file §2): Ashenstead's Heartlands margin (WC smallholding, P20, Joric's plot, P23 village) is Novice; its interior (Rebirth Fields culvert, Path of Unburnt Reeds) is Competent; FW now sits after MQ5. Riverglass's fen edge (P21, P22, P06, P10, P09, far leg) is Novice–Competent; deep fen (P30, FW done stretch) is Advanced. |
| I-16 | **Elk behaviour** is alert/flight (MN) and charge-at-NPC (DK). | Act II MN, DK | Two authored states of one creature (§6): Passive alert/flight by default, scripted flood-driven charge in DK. |
| I-17 | **Smuggler sweep displacement** varies: "a step", "2 m", "trip knockdown 1 s". | Act I NF; Settlements UL/NT; Act III CR | Canonical 2 m push; the CR trip knockdown is the Advanced-band upgrade of the same tell. |
| I-18 | **Knockdown and stagger** vs Stage 6.1.2 (CombatRestricted allows movement). | Act III CR-E3; Act I SM rake bed | Ruling needed from Systems (§9): timed movement block within Restricted (recommended). |
| I-19 | **Minimum telegraphs under click-to-move.** Several light tells are 0.8 s; Phase 1.3 has no tick-latency allowance. | All | §1 minimums (0.8 s light, 1.0 s moderate, 1.5 s heavy/area/displacement). All authored tells already comply after I-4/I-5. |
| I-20 | **Arena "safe ground" is raised** (Muster plinths, Joss footings, FW stakes) while the Unity fixture has no multi-level traversal and agility triggers are unbuilt. | Act III §11.6.1; OL.4.1; FW.4.1; README | Safe ground must be NavMesh-walkable (ramp or within step height) and tagged as volumes. Repeated in the Zones file as a level-design requirement. |
| I-21 | **Ash Hound burned-culvert den reused** by UR (UR-E2) after MQ3 used it (HW-E2/E3, `HW_DEN_CLEARED` keeps it empty). | Act I HW; Settlements UR.4 | **Canonical ruling: the burned-culvert den belongs to MQ3 only.** UR-E2 uses a different threat (§11.2). |
| I-22 | **Old Lantern's bend permanence.** | Settlements OL; Act III §E.1.2 | **Canonical ruling: OL permanently quiets `drift.old_lantern_bend`** in every ending (I-9 resolution confirmed). |
| I-23 | **Farmhouse naming.** WD's farm is being renamed by the review pass. | Discovery WD, ME07 | Referred to throughout as **the Whispering Door farmhouse**; drift id `drift.whispering_door_cellar`. |

---

## 13. Director-level questions

1. ~~Non-lethal human defeat (§8)~~ **Resolved 2026-11-03 by CDR-1:** every enemy is defeated at 0 HP; SX-1 Joss and SX-2 Sallow are scripted outcomes on defeat.
2. **Crew boss as the Smugglers elite (I-13)** and **Joss kept in the Wraith elite slot (I-14):** approve the counting?
3. **World elites Chorus-Piper and Old Mud (I-12):** place them as proposed, or cut both?
4. **Ending-matrix edits (I-9, I-11):** `drift.far_leg` replaces Old Lantern's bend as the residual site; the Whispering Door farmhouse cellar is "as left". These touch Act III §E.1.2.

## 14. Hand-offs

| To | What |
|---|---|
| Schema & Content Engineer (33.7) | Creature definitions for 21 variants + 2 sub-forms + heap-boss + 3 wildlife + 2 minibosses + 1 boss; encounter-pocket data from §11; drift-site ids from §10; encounter id prefix rule |
| Systems Engineer | §8 quest on-defeat hook (SX-1, SX-2 only; see `Quests/Caelmor_Combat_Ranged_Release_Engineering_Handoff.md`); §9 status list; drift-site state and re-form/split spawn rules; safe-ground volume tags; prop-targeting AI; knockdown ruling |
| Animation / VFX / Audio | §3 telegraph grammar and §5 canonical tells (one drift set, one lantern-drift set) |
| Level design (Zones file) | Arena distance budgets (§7.2, §7.3), wade-depth basin (§7.1), walkable safe ground (I-20) |
| Act III author | §E.1.2 row edits (I-9, I-11) |
| Side-quest author | FW unlock after MQ5 (ruling); WC unlock after MQ2 (ruling); UR-E2 threat (ruling); NB stalker cap (ruling); HW ash-shaker text (I-6) |

---

## Director rulings reconciliation (2026-11-03)

Applied `Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md`. §8 rewritten: the non-lethal human defeat proposal is superseded by CDR-1; every creature is defeated at 0 HP with the ordinary defeat presentation; SX-1 Joss Garrow and SX-2 Gideon Sallow are quest-scripted outcomes on defeat through one on-defeat hook. §7.1 Sallow (20% yield → defeat at 0 HP, P3 now 33–0%), §7.2 Joss, §5.5 Smugglers, §1 constraint rows, NF-E1 "(downed)", I-8, I-14 and §13 question 1 updated. Ranged (CDR-2) added to §1 as a first-class, never-required option; WC-E1 notes the optional borrowed short bow. Release wording clarified (CDR-3). Encounter ids, steps and fight structure unchanged.
