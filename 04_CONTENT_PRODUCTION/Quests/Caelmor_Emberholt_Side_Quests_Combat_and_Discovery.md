# Emberholt Side Quests: Combat and Discovery

**Status (2026-11-15):** Authored production content for Creative Director milestone review (Emberholt bible §12, Batch 3, part D). Four side quests from `Caelmor_Emberholt_Narrative_Production_Bible.md` §7.2 and §7.3: **EOP** *Old Plate* (Hunting; the side miniboss), **EFD** *The Flame That Would Not Die* (environmental), **EAD** *The Vein-Touched Man* (settlement and care) and **ECC** *The Commissioner's Cargo* (mystery, `[ED-15]`); the ten micro-events **EME01–EME10** (bible §7.4) and the ten discoveries **EDS01–EDS10** (bible §7.5). File map confirmed against bible §12 (Batch 3, `…_Side_Quests_Combat_and_Discovery.md`). Everything here is **[NEW]** unless marked **[CANON]** or **[APPROVED — id]**. Choices that rest on an open bible §3 recommendation are marked **[PROPOSAL — DIRECTOR]** or carry the decision's tag. Markdown only: no schema, production JSON or C#. Dialogue sits inline in each package (§x.13) in the node format `NODE SPEAKER: "Line." (stage note)`, `> [condition] "Option." → NEXT {effect}`, with node ids `<CODE>-D<n>.<nn>`, barks `<CODE>-B<n>.<nn>` and inspect texts `<CODE>-I<n>`. Voice follows bible §5.3.

**Binding rulings:** `Caelmor_Director_Rulings_Combat_Ranged_Release.md`: CDR-1 (every enemy defeated at 0 HP; no yield, retreat, break-off, scatter or drive-off; Emberholt registers no SX exception), CDR-2 (ranged first-class in every fight, required in none, trivial in none), CDR-3 (Emberholt is an internal production milestone of the complete game), CDR-4 (standard RPG systems before bespoke simulation), CDR-6 (every step, encounter, boss and reward completable solo; co-op is optional assistance; partner credit only when the partner's own active step consumes it; personal choices and flags independent; no co-op-only mechanics).

**Sources used:** the Emberholt bible (binding: §1.1, §2, §3 ED-2, ED-10, ED-11, ED-12, ED-15, ED-16, §4, §5, §7.2–7.5, §9, §10, §11); `Caelmor_Emberholt_Main_Act_I.md`, `_Act_II.md`, `_Act_III.md` and their dialogue files (tells, vents, niches, the plaque inspect, the Red Door clinic, EH-M6's containment pattern `EGA-D3`, beetle and scavenger kits, EME/EDS presentations in passing, `EEH_TAVI_LAUGHED`, `EGA_BOARD_BALANCED`); the sister file `Caelmor_Emberholt_Side_Quests_Commons_and_Wards.md` (shared conventions); the Emberholt dossier (`LORE/Regions/Caelmor_Region4_EmberholtHeights.md`: Emberback Boars, Magma Larks, Flarecap, Ember-Fused Workers, Volkhari Ash, *The Flame That Would Not Die*, the Ash Roads, the Molten Scars, backlash zones, Cinderreach Spire); `LORE/Characters/Caelmor_Characters_Region4_Emberholt.txt` (Oren Falx, Haelric Stormvein, Dalia Vret, Sereth Vorn, Myr Adalrek, Elyndra); the Part 4 character ledger (Oren Falx row: commercial pressure is not proof of Remnant command; Joren Vale row: maps are possible custodians, not truth sources); the Revelation Ledger (R09, R10, R15, R19); the format model `Caelmor_Mire_Side_Quests_Settlements_and_Combat.md` (quest packages, micro-event cards, three-layer discoveries); Lowmark *Under the Lamb* (`UL_LEDGER_GIVEN` / `UL_LEDGER_TAKEN`, read for one flavour option only).

**Scope guard.** Nothing here grows scope or adds a system. Every technical need is listed in each package's integration section and in §7 for the Emberholt integration handoff (bible §12, Batch 4). **No Emberholt terrain exists:** every placement is relative and marked **MAP VERIFICATION REQUIRED** where geometry, distance or heat matters. No route or direction to another region is stated or implied. Embergate is "the gate"; nothing names where its road goes.

**Not in this file.** The Heat Commons series, EBL and ESR (`…_Commons_and_Wards.md`); the Unburnt series, ENW and EGT (`…_Unburnt_and_Names.md`); ESK, EOM, EFS, EWQ, ESP and ESH (`…_Work_and_Skills.md`). This file sets none of their flags, uses none of their quest-givers as quest-givers, and does not resolve the Half-Name Wall, the Cold Seam's memory-stone, Maeryn's shop or EWQ's feather gathering. Where a micro-event or discovery stands at a place another package owns (EDS07, EDS09, EME08), the card here is the standing world version and the other package's lines take precedence while its step is active.

---

## 0. Purpose and shared rules

The main line teaches the player to read heat in a city. These four quests take that reading outside the civic story: onto the Ridge, where an old animal follows warm ash; to a shrine where a flame stands on nothing; to an illegal vein where a hurt man sits because it calls him; and back to the gate, where one sealed case is colder than everything around it. The micro-events and discoveries are the city and the Ridge being themselves while nobody is asking the player for anything.

### 0.1 Unlock gates and placement

| Code | Quest | Type (bible §7.2) | Core verb (primary first) | Unlock (quest state) | Skill hook (CDR-4) | Where (bible §4.2) | Length |
|---|---|---|---|---|---|---|---|
| **EOP** | Old Plate | Skill quest (Hunting); side miniboss | **track**, hunt, decide | EH-M2 Completed (`emberholt.main.02_ember_in_every_hand`) | **Hunting ~[GD: low–mid]**, checked on accept (Mire MRH precedent); reading sign and harvest | The Ridge Steadings (EP05); the Molten Scars (EP08) | 35–45 min |
| **EFD** | The Flame That Would Not Die | Environmental | **tend**, observe, decide | EH-M2 Completed | **Mining ~[GD: low]**: break out the fused throat; alternative: keep watch one turn while the keeper bars it out | Elyndra's Vent Shrine (EP20) | 25–35 min |
| **EAD** | The Vein-Touched Man | Settlement / care | **find**, contain, carry | EH-M3 Completed (`emberholt.main.03_hollow_that_should_not_burn`) | **Leatherworking ~[GD: low]**: soak, cut and lace a wet-hide wrap; alternative: keep watch one turn for the Red Door's loan wrap | Sereth's healing house (EP02 sub-site); the Ash Roads (EP09); the Embervein Tap (EP19) | 30–40 min |
| **ECC** | The Commissioner's Cargo `[ED-15]` | Mystery | **inspect**, trace, decide | EH-M4 Completed (`emberholt.main.04_ash_stained_chains`) | **Smithing ~[GD: low–mid]**: drift and replace a case's hinge pins; alternative: keep watch one turn for the wardens' farrier | Embergate yards (EP01): the Border-Wardens' post, the bonded shed, the Commission house, a counting room | 30–40 min |

All four are optional, solo-clearable, cannot fail and give no lump quest XP (skill XP from actions; bible §11.6). Inactive, Active or Completed only. **No quest items** (bible §9.4: the budget of five is spent by the milestones). Only **ECC** sets a region flag (`EH_RIVERGLASS`, bible §9.1). EAD and ECC wait on the EH-M3 cross-region gate (ED-7) through their main-line unlocks; EOP and EFD do not.

**Skill requirements.** Only EOP gates its accept on a skill (Hunting, as the bible slate names it a Hunting skill quest). Every other hook sits inside a step and has a time-cost alternative that is still play. `[GD]` levels are placeholders for the Gameplay Designer.

**Level framing (ED-10).** EOP and EFD sit at EH-M2's Advanced identity; EAD and ECC at Expert. Exact levels are Gameplay Designer calls.

### 0.2 Skill coverage

```text
EOP  Hunting (requirement + reads): three sign reads give the animal's age, sex and broken tusk; harvest after
     Carry: damping sods from the burners' stack to cap wallows (in the fight and before it)
     Melee or Ranged: Emberback Boars (EOP-E1, EOP-E2) and Old Plate (EOP-E3)
EFD  Tending (no skill): sweep, garland, lift offerings out of the bowl
     Mining (hook): break a fused crust of scree and offering stones out of the vent's throat (ECD-04)
     Melee or Ranged (optional): Cinder Wraiths at the vigil surge (EFD-E1)
EAD  Leatherworking (hook): soak a rawhide, cut and lace a wet wrap (ECD-02)
     Containment (no skill, ED-2): shut a feed gate, settle the wrap, count a man down
     Melee or Ranged: Slag Beetles in the tap cut (EAD-E1); escort a slow walker home
ECC  Reading in place: the gate manifest, the case, the timetables, a rent book
     Smithing (hook): drift two hinge pins, forge two new ones (ECD-03)
     Melee or Ranged (optional): Dross Scavengers in the rope-store yard (ECC-E1)
```

Ranged is viable in every fight here and required in none. Hunting carries EOP; Mining, Leatherworking and Smithing each carry one hook. Woodcutting does not appear (ED-11: timber is imported).

### 0.3 Economy-pass dependencies (ED-11)

**ECD-01 to ECD-04 are this file's proposal labels for the economy pass, not catalog ids or item names.** Legacy materials (ember shards, emberglass as a catalog item, ashsteel, conduction plates) are not used. Volkhari Ash appears only as a word on a seizure notice (EDS10).

| Id | Working name | Used by | Nearest approved state | What the economy pass must decide |
|---|---|---|---|---|
| **ECD-01** | **Old Plate's plate-hide** | EOP (harvest; the choice decides where it goes) | Hide (Hunting harvest) | Whether a plated emberback hide is a distinct hide state. Until defined, the harvest gives the ordinary boar harvest and the plate-hide is a quest prop. |
| **ECD-02** | **rawhide for a wet wrap** (from Sereth's store) | EAD (Leatherworking input) | Rawhide / untanned hide | The wrap recipe (soak, cut, lace). The wrap stays at Sereth's house after the quest; not kept by the player. |
| **ECD-03** | **iron bar for hinge pins** (from the farrier's rack) | ECC (Smithing input) | Iron bar | The pin recipe (heat, draw, cut). Pins are fitted in place; nothing is kept. |
| **ECD-04** | **fused scree crust** | EFD (Mining node, quest-local) | Ore rock (nearest Mining node) | A breakable node with no yield in this quest. |

### 0.4 Distinctness check

| Quest | What the player physically does | Wonder or unease | Not the same as |
|---|---|---|---|
| EOP | Reads three sign sites; learns three wallows by their beads; carries damping sods; fights an old sow who re-hardens her plates in warm ash, denying her wallows | **Wonder:** magma larks settle in a ring round her wallow and lift together when she rises | Mire MRH (patches thin by licking; here the player caps wallows); EWQ (boars as fletching quarry) |
| EFD | Tends a shrine's flame; stays for a dusk vigil; crawls to a vent throat and breaks it clear; decides whether a warden's bead goes in a holy flame | **Wonder:** at the last verse the flame goes out for three heartbeats and relights itself from below | EBL (a warden's valve on a bell); EH-M1 (bleeding a junction) |
| EAD | Follows a man by warm handprints; clears beetles from a tap cut; shuts a smuggler's gate; wraps and counts a fused man down; walks him home on an arm | **Unease:** the flarecap dims with his breath, and after he is still the vein pulses once on its own | EH-M6 `S01` (a fused worker in a warm room; here at a live vein, after a search, with a walk home) |
| ECC | Reads a manifest; opens a sealed case by its hinges without breaking the seal; reads a river's hours nobody can place; finds an empty counting room; decides who holds the copy | **Unease:** in a city where every stone is warm, the case is cold | ESS (letters with a sender); ECN (a case that reaches a court) |

### 0.5 Shared rules for all four packages

- **Address.** Cinderwall people and anyone who saw the ward reopened say "warden's hand" (bible §5.3 rule 8); Ridge herders, pilgrims, tap-hands and gate clerks say "traveller". Origin-neutral (D-3).
- **Tells and heat.** `EH_TELLS` is always true here (EH-M1 precedes every unlock). Each step pins the heat states it needs (bible §9.2; EI-HT-01 fallback). Waiting in a niche or at a keep-watch bench is always available. Frost and cold are never damage.
- **Combat.** Every enemy is defeated at 0 HP with the ordinary defeat presentation (CDR-1). Animals and beetles may be harvested where the economy allows; Cinder Wraiths collapse into ash and re-form only while their condition lasts (bible §2.7); humans fall and fade. No yield, flee, scatter, break-off or drive-off; no SX. Every fight accepts melee or ranged and requires neither; every point a player can attack from is a point the enemy can reach or answer (no unreachable safe spots). Every fight is solo-tuned (CDR-6).
- **Telegraphs.** Any attack that displaces the player is shown at least ~1.5 s before it lands (Act III's authored C-1 requirement, pending Gameplay Designer review). All telegraph times are in seconds.
- **Non-combatants.** Every named person in this file, every pilgrim, tap-hand, herder, clerk and carter is never targetable and never engaged. **Myr Adalrek is never an enemy** (ED-2): his flare is a hazard zone ended by containment.
- **Evidence.** Combat never reveals evidence and no defeated enemy speaks (rulings §3.2). Facts come from people who are alive and willing (Teodor, Ivett, Sereth, Dalia, Myr, Haelric, the carter, the rope-store keeper), records (the gate manifest, the rent book, the clinic book, notices, a survey sheet) and objects read in place (sign, wallows, a throat, a case). Phenomena (the larks, the flame going out, the vein's pulse, the cold case) identify nobody and prove nothing.
- **Reserved decisions.** No node depends on D-E2, D-S1, `[INITIATE]`, D-3, C07 or the "invaders" wording; nothing here mentions Thalan, the Speaker's knowledge or the initiate. No Volkhari person appears; no Volkhari number or community form is stated (D-C06, ED-12). No precursor name, roster or count (D-C03). The Fire Titan is never named; the Ash-Clad Giant is a legend in chalk (EDS04). ECC's nodes are tagged `[ED-15]`.
- **Time.** No calendar dates; the past is dated by events ("the cold-ward nights", "the winter the pens froze", "since the gate was rebuilt").
- **No failure.** Inactive / Active / Completed only. Death respawns at each quest's named safe point with step, flags and kept progress intact; logout restores the last persisted step and returns a dropped carry-state object to its source; walking away keeps the quest Active with the named resume hook; missed moments (a dusk, a vigil) re-offer on the next keep watch.
- **Co-op (CDR-6).** Each player's own quest state decides their own heat zones, wallows, caps, throat, gate, wrap, case and choices. Shared enemies credit a partner only when the partner's own active step consumes the defeat. A partner who leaves or is ahead never blocks the other. Shared prop presentation is a fallback only (bible §9; MI-CO-06 pattern). No step needs two players, and nothing is faster only with two.

### 0.6 Flags set and read

All flags set here are quest-local (`EOP_…`, `EFD_…`, `EAD_…`, `ECC_…`), micro-event (`EME##_…`) or discovery (`EDS##_SEEN` / `EDS##_READ`), except **`EH_RIVERGLASS`** (bible §9.1, set by ECC). Every flag has exactly one writer.

| Flag | Values | Set by (one writer) | Read by |
|---|---|---|---|
| `EOP_TRACKED` | bool | EOP `S01_sign` (third sign read) | `EOP-D2` options |
| `EOP_PLATE` | tannery / gate | EOP `S06_plate` | Steading pen gate prop; Brisa's tannery wall prop; barks |
| `EFD_THROAT` | self / keeper | EFD `S03_throat` | `EFD-D4.02` |
| `EFD_TELL` | fitted / bare | EFD `S04_bead` | Shrine bowl prop; vigil barks; EDS05 reading variant |
| `EAD_WRAP` | self / loan | EAD `S01_wrap` | `EAD-D5.12` |
| `EAD_BOOK` | named / unnamed | EAD `S07_book` | Sereth's clinic book prop; healing-house barks |
| `ECC_PINS` | self / farrier | ECC `S03_hinges` | `ECC-D4.01` |
| **`EH_RIVERGLASS`** `[ED-15]` | reported / held | **ECC** `S07_decide` | CV-M2 (request; bible §9.1). Nothing in Emberholt gates on it. |
| `EME##_…` | per card | Each micro-event | That micro-event only |
| `EDS##_SEEN` / `EDS##_READ` | bool, persistent | Each discovery's surface volume or inspect / reading interaction (the one interaction is the writer wherever it is presented: EDS09's surface inspect is presented in EH-M1 `S01`; EDS02's surface volume is crossed in EOP `S02`) | That discovery's later presentation |
| *(read)* `EH_TELLS` | bool | EH-M1 | Every tell inspect here |
| *(read)* EH-M2, EH-M3, EH-M4 Completed | quest state | Main line | EOP, EFD, EAD, ECC unlocks; EME09 (EH-M2); EDS10 reading variant (EH-M3) |
| *(read)* `EEH_TAVI_LAUGHED` | bool | EH-M2 `EEH-D6.41` | EME09 (Act I B9.2 names EME09 as a reader) |
| *(read)* `EGA_BOARD_BALANCED` | bool | EH-M6 `EGA-I28` | EME10 balanced state (Act III §9.2 names EME10 as a reader) |
| *(read)* `EH_HOLLOW_TRUTH` | told / kept / unset | EH-M3 | EDS09 surface variant (the chalk) |
| *(read)* `EH_HALF_NAME` | named / held / unset | ENW (sister file) | EDS09 reading variant only (bible §7.5: "one is chalked over later (ENW)"); ENW owns the prop |
| *(read)* `UL_LEDGER_GIVEN` / `UL_LEDGER_TAKEN` | bool (Lowmark *Under the Lamb*) | Lowmark UL `UL-D4.30` / `UL-D4.40` | ECC `ECC-D4.20` (one optional player option; flavour only; no transaction matched) |

No other region flag is read. No Thornfell or Mire flag is read. `EH_RIVERGLASS` is the only `EH_` flag written.

---
---

## EOP — Old Plate

### EOP.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `emberholt.side.old_plate` |
| Type | Skill quest (Hunting); side miniboss (bible §7.2, §10). |
| Unlock | EH-M2 Completed. **Hunting ~[GD: low–mid]** checked on accept. Offered by Teodor Marsk at his pen gate in the Ridge Steadings (`EOP-D1`); a herder's bark at the Ridge working gate points the way (`EOP-B0.1`). Below the level, Teodor talks and asks the player back (`EOP-D1.30`); no other content is locked. |
| Resume hook | Teodor at the pen gate or the blind: `EOP-D1.00` "She's still out there. So are you. Good." pins the step. |
| Skills | Hunting (requirement, sign reads, harvest); Melee or Ranged |
| Combat share | ~40% (boars at the Scars' edge; Old Plate) |
| Choice | Where the plate-hide goes (`EOP_PLATE` = tannery / gate); text and props only |
| Unlocks | Teodor's blind as a keep-watch point on the Scars' rim; the wallow bowl as a revisitable site (ordinary Emberback Boars come to the wallows at dusk) |
| **Anchor** (§7.1) | The Ridge Steadings (Teodor Marsk; herders and charcoal burners) |
| **World-truth row** | H13 (by place only: the Molten Scars are ground Emberholt's battle embercraft melted; nothing here says so in words; EDS02 owns the reading) |
| **Revelation role** | None (self-contained). The route crosses EDS02's surface volume. |
| **Recurring evidence** | None. |
| **State compliance** | Inactive / Active / Completed. No fail path: Old Plate comes to the wallows every dusk until defeated (missed dusks re-offer); signs read, sods carried and practice caps are kept; the choice is text and props only. |
| **Combat compliance** | Emberback Boars (EOP-E1, EOP-E2) and Old Plate (EOP-E3, elite) defeated at 0 HP; animals, harvestable. Melee or ranged; ranged never required and never trivial (her charge closes any distance; glass outcrops cover both styles; she can reach every point of the bowl and its rim). Solo-tuned miniboss, 3–4 minutes (CDR-6); a partner's kills credit them only if their own active step consumes the defeat. No SX. |

**In one paragraph.** Someone has been breaking the steading pens on the Ridge and taking kids and young goats. **Teodor Marsk** knows who before the player does: an emberback sow so old her plates have gone grey and thick as slag, whom he calls **Old Plate**. He knew her as a striped shoat who broke out of his father's pen the winter the pens froze; she has lived on the Ridge longer than most of the herders. Her teeth are worn and she can no longer root in the glass, so she takes what is penned. The player reads her sign at the pen, the burners' clamp and the path into the Molten Scars, clears the boars feeding at the Scars' edge, and learns her wallows from Teodor's blind: three ash wallows on vents, each with an emberglass bead Teodor traded a ham for, and she goes to whichever bead is amber, because warm ash sets her plates hard. The burners' damping sods cap a wallow. At dusk she comes. Teodor wants it done and is sorry about it, and when it is done he asks the traveller where her plate should go.

### EOP.2 Selection record and canon grounding

Selected shape: pen damage → three sign reads (Hunting) → boars at the edge → learn the wallows and the cap → dusk → miniboss built on reading tells → a small choice about what she leaves.

| Element | Source | Status |
|---|---|---|
| Emberback Boars: tough boars with ember-hardened plates; charge during resonance spikes | Dossier §XIII | [CANON] |
| Magma Larks: nest near heat vents; feathers shimmer | Dossier §XIII; bible EME08 | [CANON] |
| The Molten Scars; the Ash Roads; the Ridge Steadings (herders and charcoal burners) | Dossier §VI, §XX; bible EP05, EP08, EP09 | [CANON] / [NEW] |
| Old Plate, Teodor Marsk ("talks to animals more kindly than to people") | Bible §5.2, §7.2, §10 | [NEW] |
| Tells (clear, amber, red and crazed) | Bible §1.1; Act I | [NEW], consistent |
| Charcoal burners' damping sods; Teodor's traded beads; the wallow bowl | This package | [NEW] |

### EOP.3 The places [MAP VERIFICATION REQUIRED]

Outside the walls through the Ridge working gate on Cinderwall's side; the steadings and the Molten Scars lie along the Ash Roads (bible §4.2 route order). Relative order only.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **R1. The Ridge working gate** | Bark (`EOP-B0.1`) | A plain iron gate in Cinderwall's outer wall; herders with goats on ropes; ash on the road. |
| **P1. Teodor's steading** (EP05) | Offer; first sign; choice | Low stone pens against a warm slope; ridge goats; a smoke-house. One pen gate hangs off its post. A **keep-watch bench** under the eaves (respawn for `S00`, `S01`, `S06`). |
| **P2. The burners' clamp** | Second sign | A charcoal clamp under a skin of turf **damping sods**, smoking. One side rooted open, sods torn and scattered. A stack of cut sods beside it. |
| **P3. The Scars path** | Third sign | A spur off the Ash Road dropping toward the glass. Ash in the prints. |
| **M1. The Scars' edge** (EP08) | Boars (EOP-E1) | Where the glass begins: cinderleaf shrubs in the cracks, rooted over. Entering the edge's view volume sets `EDS02_SEEN`. |
| **M2. Teodor's blind** | Wallow lesson; dusk wait; respawn for `S02`–`S05` | A ring of glass rubble and a goat-hide awning on the bowl's rim. A burners' **sod stack** (sods cut and brought up by the burners for their clamps on this side). Keep-watch point. |
| **M3. The wallow bowl** | Old Plate (EOP-E3) | A shallow bowl of black glass. Three **ash wallows** sit on small vents (W-A near the rim, W-B at the centre, W-C under an overhang), each with an emberglass **bead** wedged in a stone at its lip. Three **glass outcrops** stand up like broken teeth. A walkable slope back to the blind; the rim is walkable all round. |

### EOP.4 Beats

**Beat 0: The Pens (`S00_offer`).** *Objective: Talk to the herder at the broken pen.* The bark at the working gate (`EOP-B0.1`) sends the warden's hand up the Ash Road. Teodor is mending the pen gate (`EOP-D1`). Two young goats gone in a fortnight; the herders want him to set a trap. He will not set a trap for her. On accept, the Hunting check.

**Beat 1: Sign (`S01_sign`).** *Objective: Read the sign at the pen, the clamp and the path.* Three reads in any order (Hunting reads; with the level met, each inspect gives its conclusion line):
- **The pen post** (`EOP-I1`): tusk gouges on one side of the post only, high; flakes of grey slag in the splinters, which plates shed when they rub.
- **The clamp** (`EOP-I2`): rooted into the warm side of the clamp; singed hair; prints deep and splayed: heavy, old, a sow.
- **The path** (`EOP-I3`): a shed plate the size of a hand, worn smooth on its inner face; in one print, the mark of a tusk broken off short, dragging on her left.
On the third read, sets `EOP_TRACKED`. Teodor, at the pen (`EOP-D2`), hears it and tells the story of the shoat that broke out of his father's pen.

**Beat 2: The Edge (`S02_edge`).** *Objective: Follow her path to the edge of the Molten Scars.* At the Scars' edge (M1), three Emberback Boars are rooting the cinderleaf (**EOP-E1**). They hold the path down. Harvest is optional. Teodor arrives after the fight and leads up to the blind (`EOP-B2.1`). Crossing M1 sets `EDS02_SEEN` in passing.

**Beat 3: The Wallows (`S03_wallows`).** *Objective: Learn her wallows from the blind.* At the blind (`EOP-D3`), Teodor shows the three wallows and their beads. "She goes where the bead's amber. Warm ash sets her plates hard as a griddle." Inspect the three wallows (`EOP-I4`; with `EH_TELLS` the bead state is read). **Keep watch one turn** at the blind: the beads change, one amber at a time, W-A to W-B to W-C (the vents' schedule, pinned for this quest). Then the cap: take a **damping sod** from the stack (carry-state; the player can walk but not attack while carrying), carry it to the amber wallow and **cap it** (interaction ~2 s). The sod smokes, the bead greys under it, and after ~45 s it burns through and the bead shows again. Teodor: "That's the trick. Not for long. Long enough." (`EOP-D3.20`).

**Beat 4: Dusk (`S04_dusk`).** *Objective: Wait for her at the blind.* If it is not dusk, keep watch at the blind until dusk. The strange moment plays (EOP.5). The objective changes when she rises from the wallow.

**Beat 5: Old Plate (`S05_old_plate`).** *Objective: Bring her down.* **EOP-E3** (spec EOP.6.1), with **EOP-E2** at the resonance spike. Teodor stays at the blind and calls the beads (`EOP-B5.*`); he never fights and is never engaged.

**Beat 6: Her Plate (`S06_plate`).** *Objective: Talk to Teodor.* He comes down the slope, kneels by her and puts a hand on her snout (`EOP-D5`). Harvest is offered (Hunting harvest; ordinary boar harvest per economy; the plate-hide is a quest prop, ECD-01). Then the choice (EOP.8). Sets `EOP_PLATE`. Small payment. **Quest Completed.**

### EOP.5 The larks (presentation spec: wonder)

| Time | Element | Spec |
|---|---|---|
| Dusk | **Shimmer** | The bowl's vents breathe; heat shimmer over the glass. One bead (W-B, pinned) shows amber. Magma larks bathe in the shimmer at the far side and scatter if the player moves on the rim (EME08 behaviour). |
| 0–4 s | **Her** | Old Plate comes down the far slope at a walk, not a run. She is huge and grey; her plates are dull; one tusk is a stump. |
| 4–10 s | **The ring** | She steps into W-B. The larks do not scatter. They come down out of the shimmer and settle on the glass in a ring round the wallow, all facing her, feathers shimmering amber. |
| 10–14 s | **The roll** | She rolls in the warm ash. Her plates take the heat and glow amber from the edges inward, like a griddle on a fire. |
| 14–16 s | **Lift** | She stands. Every lark lifts at once, one sound like a sheet shaken out. She looks up at the blind. |
| 16 s | **Begin** | A forefoot scrape; the fight begins (objective appears only now). |
| After | Teodor, if asked (`EOP-D5.20`) | "They do that for her. Only her. Forty years and I've never known why." |
| Meaning | None stated. Her wallow is the warmest place in the bowl at dusk, and larks bathe in heat. It proves nothing. |

### EOP.6 Encounters and hazards

Tuned for EH-M2's Advanced identity (ED-10). Ridge animals: defeated at 0 HP; harvestable.

| Id | Enemies / hazard | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **EOP-E1** | 2 × Emberback Boar **boar**, 1 × **tusker** | The Scars' edge (M1) among rooted cinderleaf | Boars charge from open glass; the tusker holds the path and braces | **Boar, Charge:** forefoot scrape and snort (~1.5 s), then a straight charge, damage and one-step knock-back; a shrub or outcrop stops it. **Tusker, Gore:** head drops, plates glow along the neck (~1.2 s), then a hooking gore (no displacement). **Tusker, Brace:** stops, plates flare amber (~1.0 s), takes reduced damage for ~4 s (visible glow; wait it out or hit the boars). | First animal fight on the Ridge; teaches "glowing plates take less" before the miniboss | 50–80 s; 65–85% HP |
| **EOP-E2** | 2 × Emberback Boar **boar** | Run in from the bowl's far slope at the resonance spike (EOP-E3 at 50%) | As EOP-E1 boars | As EOP-E1 | Phase pressure; canon "charge during resonance spikes" | — |
| **EOP-E3** | **Old Plate** (Emberback Boar elite) | The wallow bowl (M3) | Side miniboss; spec EOP.6.1 | EOP.6.1 | Required | 3–4 min |
| **EOP-H1** | Amber wallow | M3, whichever wallow is amber | Hazard | Amber bead; heat shimmer | Light periodic heat inside the wallow ring; outside it, none | — |
| **EOP-H2** | Burning hoofprints | Behind her charge while her plates glow | Hazard | Visible flame | ~3 s, light damage | — |

#### EOP.6.1 Miniboss spec: Old Plate (EOP-E3)

| Field | Spec |
|---|---|
| Family | Emberback Boars, elite (bible §10). An animal; fights to 0 HP (CDR-1); harvestable. |
| Read | An old sow the size of a cart, plates grey and thick as slag, muzzle white, the left tusk broken to a stump. Slow to start; very fast once moving. |
| **Plate heat** (core pattern) | After every wallow her plates **glow amber** and she takes **reduced damage** ([GD]; heavy reduction) while the glow lasts. The glow cools from the centre outward over **~12 s**, visible as the amber shrinking to the plate edges and going grey. Grey plates take full damage. |
| **Wallow** (core pattern) | When her plates are grey she trots to the wallow whose bead is **amber** (one at a time; the beads cycle W-A → W-B → W-C on a fixed ~25 s schedule, readable from anywhere in the bowl) and **rolls** for **3.0 s**: the opening for heavy hits, since her plates are still grey while she rolls. Standing in the wallow ring deals light heat (EOP-H1). |
| **Capping** | A **damping sod** from the stack at the blind (carry, ~2 s cap interaction) on an amber wallow greys its bead for ~45 s. She will not roll in a capped wallow: she stops at it, snorts (~1.0 s), and trots to the next bead in the cycle. If every wallow is capped or grey she roots a **cold wallow** in bare ash (4.0 s roll, no plate heat). The loop never stalls: caps burn through on their own, and the next bead always comes. The sod stack never runs out. Capping is never required: a player who never caps fights through more glow. |
| **Charge** (all phases) | Forefoot scrape and a low grunt (**1.5 s**), then a straight charge across the bowl: heavy damage and knockdown. A **glass outcrop** in her line stops her: she hits it and **staggers for 2 s** (free hits). While her plates glow, the charge leaves burning hoofprints (EOP-H2). |
| **Tusk hook** (all phases, close) | Head drops and swings to her **right**, the side with the whole tusk (**1.0 s**), a wide hook; no displacement. Her left, the stump side, has no hook: a reader stands on her left. |
| **Spark-shake** (P2, 60% and below) | She plants and shakes (**1.2 s**, plates rattling and glowing at the seams), throwing burning slag flakes in a 3-pace ring; patches burn ~4 s. |
| **Resonance spike** (once, at 50%) | The ground rumbles (**2.0 s**, dust lifting off the glass all over the bowl); every bead flares red for 6 s (no wallow usable); two Emberback Boars (EOP-E2) charge in off the far slope. She charges with them. |
| **Old legs** (P3, below 25%) | She chains two charges before she needs to turn, and the plate glow cools faster (~9 s) because she is tiring. |
| Arena | The bowl (M3): three wallows, three outcrops, the walkable rim and slope. No ledge, roof or rim point she cannot reach; she follows onto the rim. |
| Ranged and melee (CDR-2) | Ranged players shoot during the roll and the outcrop stagger; the charge closes any distance, and outcrops are cover for both. Melee players stand on her stump side and hit during rolls and staggers. Caps help both styles equally. Neither style trivialises her. |
| End | At 0 HP she lies down in the ash on her side; the glow goes out of her plates. Harvestable. |
| Reset | Leaving the bowl or dying resets her to full and clears caps; signs read and the blind lesson stay done. She comes again at the next dusk. |

**Rules.** All animals to 0 HP with the ordinary defeat presentation. Nothing dropped or harvested advances the quest beyond `S05`. **Death:** respawn at the blind (M2) for `S02`–`S05`; at the steading bench for the rest. Defeated EOP-E1 boars stay defeated; Old Plate resets and the quest returns to `S04_dusk` ("Wait for her at the blind"), with the strange moment shortened to the walk-in on repeat.

### EOP.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to the herder at the broken pen. | `EOP-D1` accept (Hunting check) | Yes | `EOP-B0.1` at the working gate points the way |
| `S01_sign` | Read the sign at the pen, the clamp and the path. | `EOP-I1` + `EOP-I2` + `EOP-I3` + `EOP-D2` end | Yes | Sets `EOP_TRACKED` on the third read |
| `S02_edge` | Follow her path to the edge of the Molten Scars. | EOP-E1 defeated + enter blind volume (M2) | Yes | Sets `EDS02_SEEN` in passing |
| `S03_wallows` | Learn her wallows from the blind. | 3 wallow inspects + one keep watch + one cap placed + `EOP-D3.20` | Yes | Beads pinned to the lesson cycle |
| `S04_dusk` | Wait for her at the blind. | Dusk reached (keep watch) + EOP.5 sequence end | Yes | Re-offers each dusk |
| `S05_old_plate` | Bring her down. | EOP-E3 defeated | Yes | EOP-E2 at 50% |
| `S06_plate` | Talk to Teodor. | `EOP-D5` choice + `EOP-D5.40` end | Yes (→ **Completed**) | Sets `EOP_PLATE`; harvest offered first |

| Flag | Set by | Read by |
|---|---|---|
| `EOP_TRACKED` | `S01` | `EOP-D2` options |
| `EOP_PLATE` = tannery / gate | `S06` | Pen gate prop; tannery wall prop; barks |
| *(set in passing)* `EDS02_SEEN` | `S02` (M1 volume) | EDS02 |

### EOP.8 Choices and consequences

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **To the tannery** (`tannery`): *"Brisa Teglan can make gloves of that. Somebody's hands stay whole."* | Teodor and a burner carry the plate-hide down to Brisa's tannery in the Cinderweave Quarter. | The steadings think it a little shameful to sell an old neighbour's skin; Teodor says nothing, which is worse. | Brisa hangs the plate on her tannery wall while it cures: "Thickest I've seen. Hide first, heat second." Barks at the tannery. |
| **Over the gate** (`gate`): *"Hang it over your pen gate. Let the young ones know the smell."* | Teodor nails one plate over his mended pen gate, as herders do with a boar that troubled them. | No gear comes of her; Brisa grumbles when she hears ("Good hide on a gate.") | The plate over the gate (prop). Herders' barks: pens with a sow's plate are left alone, they say. Nobody can prove it. |

No option is wrong. The pens are safe in both; ordinary boars still come to the wallows at dusk.

### EOP.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| Small payment | Currency | From Teodor's purse and the burners' ([GD]). |
| Harvest | Hunting | Ordinary emberback harvest per economy; the plate-hide stays a prop (ECD-01). |
| The blind | Access | A keep-watch point on the Scars' rim. |
| Hunting, Melee or Ranged XP | Action XP only [GD] | No lump quest XP. |

### EOP.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Hunting below the level | Teodor talks (`EOP-D1.30`) and asks the player back; the quest stays Inactive; nothing else is locked. |
| Misses dusk / leaves before she comes | `S04` re-offers at the next dusk; keep watch at the blind. |
| Death in the bowl | Respawn at the blind; she resets; caps clear; the step returns to `S04`. Signs, the lesson and EOP-E1 stay done. |
| Logout | Restore to the step: the steading (`S00`, `S01`, `S06`), the blind (`S02`–`S05`). A carried sod returns to the stack. |
| Walking away | Stays Active; resume at Teodor (`EOP-D1.00`). |
| Co-op | Shared fights; a defeat credits each partner whose own active `S02` or `S05` consumes it (CDR-6). Wallows, beads and caps are per player props; a partner's cap does not cap your wallow (shared presentation fallback only). Each player makes their own plate choice and sets their own `EOP_PLATE`. Old Plate is solo-tuned; nothing is co-op-only. |

### EOP.11 Integration needs

Standard: quest-start skill check (Mire MRH pattern); Hunting sign inspects gated by level; carry-state sod; a cap interaction that greys a bead prop for ~45 s per player; three bead props on a fixed per-player cycle (EI-HT-01 quest-pinned fallback); boss AI that moves to the tagged amber wallow and treats capped wallows as unavailable (Mire MRH patch-seeking loop); plate-glow timer with a damage-reduction buff; outcrop stagger on charge collision; the lark ring as a scripted flock event (dusk, first time; shortened on repeat); pen gate and tannery wall prop variants by `EOP_PLATE`. No new system.

### EOP.12 Mystery ledger entry

| Field | Entry |
|---|---|
| Author truth | Larks bathe in heat; her wallow at dusk is the warmest place in the bowl. Nothing more is decided. |
| Public belief | "The larks know her." |
| Observable | The ring of larks; the lift. |
| Wrong reading | She is something more than a sow. (She is an old sow.) |
| Withheld | Nothing that matters. |

### EOP.13 Dialogue

#### Cast notes

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Teodor Marsk** [NEW, bible §5.2], ridge-steading hunter | Old Plate since she was a shoat; her wallows; the beads; the burners' sods. | Why the larks come to her. | Talks to animals more kindly than to people. Short sentences to people; long, soft ones to goats. |
| **Herder** (role) | That Teodor's pens are broken. | — | Ridge plain. |
| **Charcoal burner** (role) | The sods; that she rooted the clamp. | — | Smoky, cheerful. |
| **Brisa Teglan** [NEW, bible §5.2] (post-quest bark only, `tannery`) | Hide. | — | "Hide first, heat second." |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| `EOP-B0.1` | HERDER | Ridge working gate; EH-M2 Completed; EOP Inactive | "If you're going up the road, Marsk's pens are broken. He won't set a trap. Ask him why. Go on." |
| `EOP-B1.1` | CHARCOAL BURNER | At the clamp, `S01` | "Rooted it while it was smoking. Didn't care. That's an old one, that's got no fear left." |
| `EOP-B2.1` | TEODOR | After EOP-E1 | (to a dead boar) "Sorry, lad." (to the player) "Up. The blind's this way." |
| `EOP-B5.1` | TEODOR (from the blind) | A bead turns amber | "Near one's warm!" / "Middle!" / "Under the hang!" |
| `EOP-B5.2` | TEODOR | A cap placed | "That's it. Make her walk." |
| `EOP-B5.3` | TEODOR | Her plates glowing | "She's hot. Let her cool. Don't waste yourself on plate." |
| `EOP-B5.4` | TEODOR | Resonance spike | "Ground's up! Boars'll come with it!" |
| `EOP-B5.5` | TEODOR | She staggers on an outcrop | "Now!" |
| `EOP-B6.1` | BRISA | Tannery, `tannery` | "Thickest plate I've seen. Hide first, heat second. This one's both." |
| `EOP-B6.2` | HERDER | Steading, `gate` | "Marsk's got her over the gate. Nothing's broke a pen with a plate on it. Not that I've seen." |
| `EOP-B6.3` | TEODOR | Post-quest, steading | (to a goat) "There. Nobody's coming. Nobody's coming tonight." |

#### Nodes

```
EOP-D1.00 [quest Active, returning] TEODOR: "She's still out there. So are you. Good." (pins step)  → end
EOP-D1.01 TEODOR: (driving a peg into the pen gate; not looking up) "If you've come about the pens, they're broken. If you've come about anything else, they're still broken."
EOP-D1.02 TEODOR: "Two kids in a fortnight. The others want a pit and a stake." (beat) "I'm not digging a pit for her."
  > "For who?"                                                      → EOP-D1.03
  > "What do you want done?"                                        → EOP-D1.05
EOP-D1.03 TEODOR: "Read the post and tell me. If you can't read a post, you can't help me."   → EOP-D1.05
EOP-D1.05 TEODOR: "Read her sign. Pen, the burners' clamp, the path down to the Scars. Then come back and tell me what you saw. Not what you think."
  > [Hunting ≥ GD] "All right."                                      {event: accept → S01_sign}  → end
  > [Hunting < GD] "All right."                                      → EOP-D1.30
EOP-D1.30 TEODOR: (looks at the player's hands, then their boots) "You'd walk past her prints and call them weather. Come back when you can read a print." (beat) "No offence. She'd take none either."   → end
```

```
EOP-D2.01 TEODOR: "Well?"
  > [EOP_TRACKED] "Old. Heavy. A sow. One tusk broken short on her left. Her plates are shedding."   → EOP-D2.02
  > "I haven't read it all."                                        → end
EOP-D2.02 TEODOR: (puts the mallet down) "Old Plate."
EOP-D2.03 TEODOR: "Winter the pens froze, my father had a sow farrow in the end pen. One shoat came out striped and screaming and went over the wall before her eyes were properly open. My father laughed till he coughed."
EOP-D2.04 TEODOR: "That's her. Forty years on the Ridge. Longer than most of us."
  > "Why is she taking stock now?"                                  → EOP-D2.05
  > "You're sorry about it."                                        → EOP-D2.07
EOP-D2.05 TEODOR: "Teeth. Look at the plate you found. Worn smooth. She can't root in the glass any more. Pens are easy. Pens don't run."   → EOP-D2.09
EOP-D2.07 TEODOR: "I'm sorry about most things that come to my pens hungry." (beat) "Doesn't stop me."   → EOP-D2.09
EOP-D2.09 TEODOR: "Follow her down to the edge. Boars feed there; they'll not let you by. I'll come up behind you to the blind."   {event: S01 complete}  → end
```

```
EOP-D3.01 TEODOR: (at the blind, on his heels) "There. Three wallows. Ash on vents. See the beads?"
EOP-D3.02 TEODOR: "Warden's beads. Traded a ham for them off a line hand who'd had a drink. Best ham I ever spent."
EOP-D3.03 TEODOR: "She goes where the bead's amber. Warm ash sets her plates hard as a griddle. Hit her then and you're hitting the griddle."
  > [EH_TELLS] "Clear, amber, red. Same as the city."               → EOP-D3.05
  > "How do I stop her?"                                            → EOP-D3.07
EOP-D3.05 TEODOR: "Same beads. Different animal." (beat) "City folk read them for pipes. I read them for her."   → EOP-D3.07
EOP-D3.07 TEODOR: "Watch them turn. Then I'll show you the trick."   {event: keep-watch prompt}  → end
EOP-D3.10 [after keep watch] TEODOR: "See? One at a time. Near, middle, under the hang. Round again."
EOP-D3.11 TEODOR: "Burners' sods. They damp the clamps with them. Throw one on a warm wallow and she can't use it. Go on. The warm one."   {event: cap prompt}  → end
EOP-D3.20 [after cap] TEODOR: "That's the trick. Not for long. Long enough." (looks at the sky) "She comes at dusk. She always has."   {event: S03 complete}  → end
```

```
EOP-D5.01 TEODOR: (kneels by her; puts his hand flat on her snout) "There, old girl. There."
EOP-D5.02 TEODOR: (to her, quietly) "You went over the wall. I remember."
EOP-D5.03 TEODOR: (to the player, after a while; standing) "Take what's yours of her. That's fair."   {harvest prompt}
EOP-D5.04 TEODOR: "Her plate's the thing. Thick as a hearthstone. Somebody'll want it. Where?"
  > "Brisa Teglan can make gloves of that. Somebody's hands stay whole."   → EOP-D5.10
  > "Hang it over your pen gate. Let the young ones know the smell."      → EOP-D5.30
  > "What do the herders do?"                                       → EOP-D5.06
EOP-D5.06 TEODOR: "Over the gate, mostly. Tanners pay, though. Gloves are gloves." (beat) "Your call. You brought her down."   → EOP-D5.04 options
EOP-D5.10 TEODOR: "Gloves." (beat) "She'd have liked that, being warm on somebody." (he does not sound sure)
      {set EOP_PLATE = tannery}  → EOP-D5.40
EOP-D5.30 TEODOR: "Over the gate." (beat) "She'll look down at the kids every morning. Fair enough. She looked at them long enough from outside."
      {set EOP_PLATE = gate}  → EOP-D5.40
EOP-D5.20 [after S05, asked about the larks] TEODOR: "They do that for her. Only her. Forty years and I've never known why."   → end
EOP-D5.40 TEODOR: (pays from a goat-leather purse) "For the pens. The burners put in too." (beat) "Come up any dusk. The blind's yours."
      {event: EOP-D5 end → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| `EOP-I1` | The pen post | "Tusk gouges, all on one side, high up. Flakes of grey slag caught in the splinters." / [Hunting] "+ Plates shed like that when they rub. Something big, and only one good tusk." |
| `EOP-I2` | The rooted clamp | "Rooted into the warm side while it smoked. Singed hair on the turf. Deep prints, toes splayed." / [Hunting] "+ Heavy and old. A sow; the hind prints sit inside the fore." |
| `EOP-I3` | The path | "A plate the size of your hand, worn smooth on the inside. In one print, a drag mark." / [Hunting] "+ The drag is a tusk broken off short, on her left. Her teeth are worn; she isn't rooting much." |
| `EOP-I4` | A wallow | "Grey ash on a small vent. An emberglass bead wedged in a stone at the lip." / [`EH_TELLS`] "+ Clear: cold. Amber: warm ash. Red: don't." |
| `EOP-I5` | A capped wallow | "A damping sod over the ash, smoking. The bead under it has gone grey." |
| `EOP-I6` | The plate over the gate (`gate`) | "One plate, nailed up. It has a goat's attention already." |

### EOP.14 Open decisions

1. **Quest-start Hunting requirement.** Follows the bible's "Skill quest (Hunting)" and the Mire MRH precedent. If the Gameplay Designer prefers no gate, the sign reads keep their conclusion lines at any level and `EOP-D1.30` is cut; nothing else changes.
2. **Teodor's "forty years".** A herder's way of saying a long time, not a date. Emberback lifespans are not canon; the economy and creature passes may prefer "longer than most of us" only (`EOP-D2.04` already carries that).

### EOP.15 Review log

| Check | Result |
|---|---|
| CDR-1 | Boars and Old Plate to 0 HP; the resonance-spike boars arrive and fight to 0 HP; nothing flees or breaks off. Reset on leaving is ordinary leash. |
| CDR-2 | Ranged and melee both viable; the charge closes distance; outcrops and the stump side reward reading, not a style; no point in the bowl or on the rim is out of her reach. |
| CDR-6 | Solo-tuned (3–4 min); caps are optional; no two-person mechanic. |
| Evidence | The story comes from Teodor and from sign; she carries nothing. |
| Sorry about it | Teodor kneels; the choice is about what she leaves, not whether she dies. |

---
---

## EFD — The Flame That Would Not Die

### EFD.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `emberholt.side.flame_that_would_not_die` |
| Type | Environmental (bible §7.2). |
| Unlock | EH-M2 Completed. A note on the Cooling House board (EH-M1 W2): *"The keeper at Elyndra's shrine asks a warden's hand to look at the flame. Bread and a bench."* Reading it (`EFD-I1`) or Hennet's bark (`EFD-B0.1`) starts the quest at `S00`; the offer completes with Ivett Quarle at the shrine (`EFD-D1`). |
| Resume hook | Ivett at the flame bowl: `EFD-D1.00` "It's still standing on nothing. Where had you got to?" |
| Skills | Mining ~[GD: low] (hook; keeper alternative); Melee or Ranged (optional) |
| Combat share | ~10%, optional (Cinder Wraiths at the vigil surge) |
| Choice | Whether a warden's bead goes in the flame bowl's lip (`EFD_TELL` = fitted / bare) |
| Unlocks | The shrine's water-jar niche as a keep-watch point; the dusk vigil as a repeatable world moment; EDS05's reading variant |
| **Anchor** (§7.1) | Shrine keepers and pilgrims (Ivett Quarle) |
| **World-truth row** | H01 (belief only: a shrine's faith and custom; nothing reliable is claimed) |
| **Revelation role** | None. Elyndra stays unproven (bible §7.2). |
| **Recurring evidence** | None. |
| **State compliance** | Inactive / Active / Completed. No fail path: the vigil re-offers at every dusk; the Mining hook has a keeper alternative; the bead choice is props and lines only. |
| **Combat compliance** | Cinder Wraiths (EFD-E1) at the vigil surge, **optional**: defeated at 0 HP, collapse into ash and re-form at each exhale only while the vigil surge lasts (bible §2.7). Melee or ranged; every spot a player can attack from is inside the Wraiths' reach. Solo; partner credit only via the partner's own active step. Pilgrims and Ivett are never targetable and never engaged. No SX. |

**In one paragraph.** Out on the Ridge, past the steadings, a flame stands in a basalt bowl at **Elyndra's Vent Shrine**. **Ivett Quarle** has kept it for most of her life and has never found its fuel: no wick, no oil, no coal. Pilgrims call it Elyndra's flame and tell the old story of the fire that burned through a storm. Lately it gutters and then leaps, and the pilgrims say Elyndra is angry. Ivett does not want it explained away; she wants it looked at. The player tends the flame with her, stays for the dusk vigil, when the pilgrims sing and the flame climbs with every verse and Cinder Wraiths rise out of the pit below the terrace, and at the last verse the flame goes out for three heartbeats and lights itself again from underneath. Through the keeper's crawl the player finds the vent that feeds it, half-choked with fallen scree and years of offering stones that pilgrims pushed into the bowl, and an iron ring someone set in the rock long ago so the draught would rise straight. The player clears the throat (or holds the lamp while Ivett bars it out), and then Ivett asks whether the shrine should have a warden's bead in its lip.

### EFD.2 Selection record and canon grounding

Selected shape: tend → observe the vigil → the flame goes out and returns → find the vent (Mining or keeper) → a choice between telling and keeping, carried by one bead. Rejected: proving Elyndra false (the bible keeps belief as belief); a boss in the pit (the bible gives Wraiths at a surge, optional).

| Element | Source | Status |
|---|---|---|
| *The Flame That Would Not Die*: a fire that burned through a storm; truth: a vein surged with nearby emotion | Dossier §XV.1 | [CANON] legend; told here by pilgrims as the shrine's story, attributed, never confirmed |
| Elyndra's Vent Shrine; Elyndra myth only, no appearance, no proof | Bible EP20, §5.1, §7.2, EDS05 | [CANON myth]; see EFD.14 item 1 on the canon character file |
| Ashvine garlands; emberbloom | Dossier §XIII | [CANON] |
| Heat follows the room; tells; vent breath; Cinder Wraiths | Bible §1.1, §2.4, §10 | [NEW] / [CANON] |
| Ivett Quarle, the vigil song, the keeper's crawl, the iron throat ring | This package | [NEW] |

### EFD.3 The places [MAP VERIFICATION REQUIRED]

Further out on the Ridge than the steadings, along the Ash Roads (bible §4.2). Relative order only.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **E1. The shrine terrace** (EP20) | Offer; tending; the vigil; the choice | A flat terrace of old paving on the ridge flank. On a basalt plinth, a wide **flame bowl** with a flame in it, waist-high, the colour of a forge. Offering stones heaped round the plinth, ashvine garlands, dried emberbloom. Pilgrims' benches. A **water-jar niche** in the rock (cooling niche; keep-watch; respawn). |
| **E2. The lower terrace and the pit** | The vigil surge; EFD-E1 | Steps down from E1 to a lower terrace round a railed pit. A **vent grate** at the pit's floor breathes; the pit has no tell (nobody ever set one). The steps and the pit floor are walkable; the rail is waist-high. |
| **E3. The keeper's cellar and crawl** | Route to the throat | A trapdoor behind the plinth; a cellar with brooms and a bar; a stooped **crawl** that runs back under the bowl (Working heat; one jar niche halfway). |
| **E4. The throat** | The Mining hook; the iron ring | Where the crawl meets the vent's neck under the bowl. A crust of fused scree and old offering stones half closes the neck; air comes up in coughs. In the rock above, an **iron ring** collars the throat. |

### EFD.4 Beats

**Beat 0: The Note (`S00_offer`).** *Objective: Find the keeper at Elyndra's shrine.* From the Cooling House board or Hennet's bark, out through the Ridge working gate and along the Ash Road past the steadings. Ivett at the bowl (`EFD-D1`).

**Beat 1: Tending (`S01_tend`).** *Objective: Tend the flame with the keeper.* Ivett's morning round, in any order: **sweep** the ash off the bowl's lip (interaction ~2 s); carry fresh **ashvine** from the garland basket to the plinth (carry-state, one trip); **lift three offering stones** out of the bowl's mouth where pilgrims push them (interaction each, ~1 s; the flame leans away from the hand). Then **inspect the bowl** (`EFD-I2`): no wick, no oil, no coal; a hole in the bowl's base the width of a wrist; a warm draught on the back of the hand. Ivett (`EFD-D2`): it gutters and leaps; she is afraid it will go out in front of the pilgrims, or leap at a child.

**Beat 2: The Vigil (`S02_vigil`).** *Objective: Stay for the dusk vigil.* Keep watch at the niche until dusk if needed. Pilgrims gather; Ivett leads a three-verse song. **Heat follows the room:** with each verse the flame climbs a hand higher and the pit's vent breathes harder; the pit is pinned **Surging** for the song (~3 minutes). Cinder Wraiths form at the pit grate on each exhale (**EFD-E1**, optional; the pilgrims sing on, unengaged, on the upper terrace). At the last verse the strange moment (EFD.5). The step completes when the song ends, whether or not the player fought.

**Beat 3: The Throat (`S03_throat`).** *Objective: Find what feeds the flame.* Ivett gives the trapdoor (`EFD-D3`). Down the crawl (Working; touch water at the jar niche) to the throat. **Inspect the crust** (`EFD-I5`) and **the iron ring** (`EFD-I6`). Then:
- **Option A (skill): break it out** (**Mining ~[GD: low]**). The crust is a quest-local Mining node (ECD-04): three strikes; each strike widens the neck and the cough becomes a breath. Sets `EFD_THROAT = self`.
- **Option B (time-cost): the keeper's bar.** "I've a bar. I've a back. Mine's older than yours." Keep watch one turn in the jar niche while Ivett and a pilgrim lever the crust out; the player holds the lamp (a held interaction, leave and resume). Sets `EFD_THROAT = keeper`.
On clearing, the throat breathes evenly; from above, through the crawl, the pilgrims' murmur changes: the flame has steadied.

**Beat 4: The Bead (`S04_bead`).** *Objective: Tell the keeper what you found.* At the bowl (`EFD-D4`). Ivett has a warden's bead somebody left at the shrine years ago and she never set. The choice (EFD.8). Sets `EFD_TELL`. Bread, a bench, Ivett's thanks. **Quest Completed.**

### EFD.5 The flame goes out (presentation spec: wonder)

| Time | Element | Spec |
|---|---|---|
| Last verse | **Height** | The flame stands twice its morning height, white at the root, swaying with the song. |
| 0–1 s | **Out** | On the verse's last word the flame goes out. Not down: out. The bowl is a dark stone mouth. The terrace is suddenly cold enough that every pilgrim feels it. |
| 1–4 s | **Dark** | Three heartbeats of silence (audible: the player's own heartbeat, three times). The pit's vent stops breathing. Ivett does not move. |
| 4–5 s | **Thump** | A soft thump from under the plinth, felt in the feet. The flame comes back from below, low and blue, then forge-coloured, then its morning height. |
| 5–8 s | **Breath** | The pilgrims breathe out together. One says "She breathed." The pit's vent breathes again, slowly. |
| After | Ivett (`EFD-D2.20`) | "It's done that four times this season. Never used to." |
| Meaning | Physical: a choked throat that stalls and re-fires. Belief: Elyndra breathed. Neither is denied. Nothing is proved about Elyndra. |

### EFD.6 Encounters and hazards

Tuned for EH-M2's Advanced identity. Cinder Wraiths are resonance distortions (bible §2.4); the condition is the vigil surge in the pit.

| Id | Enemies / hazard | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **EFD-E1** (optional) | Cinder **wraith** and **flare** forms at the pit grate; cap 2 at a time (opening mix 1 × wraith, 1 × flare) | The pit (E2) and the lower terrace; they climb the steps and the rail, and the flare throws to the upper terrace's front edge | Wraiths go for the nearest player; flares hang over the pit and throw | **Vent exhale (the condition):** ash lifts off the grate (~1.5 s), then the exhale (damage, one-step knock-back over the grate); a defeated Wraith re-forms in the exhale if under the cap. **Wraith, Grasp:** arms flare white (~1.0 s), then a two-handed lunge (sidestep). **Wraith, Flash:** body brightens and hums (~1.5 s), then a 2-pace heat ring. **Flare, Toss:** a ball of fire swells between its hands (~1.2 s), then an arcing throw leaving a burning patch ~4 s. | Optional fight while watching the vigil; the shrine's heat at its wildest | 2–3 min if fought through the song; 60–80% HP |
| **EFD-H1** | The pit vent | E2 | Timed hazard | Ash lift ~1.5 s (~10 s cycle); ~6 s during the song | Damage and one-step knock-back over the grate | — |
| **EFD-H2** | Surging pit (no tell) | E2 during the song | Hazard | **Heat shimmer only** (there is no bead: reading it without one is the point) | Heavy periodic heat in the pit; the lower terrace is Working; the upper terrace is cool | — |
| **EFD-H3** | The crawl | E3 | Hazard | Amber bead at the crawl mouth (Ivett's one concession: "That one came with the trapdoor.") | Light periodic heat; jar niche halfway | — |

**Rules.** Wraiths defeated at 0 HP collapse into ash at the grate. While the song lasts they re-form at each exhale up to the cap; the song's end ends the condition and **no more form**. A Wraith in combat when the song ends **fights on** to 0 HP. A Wraith that is not engaged when the song ends collapses at the grate (the condition has ended; bible §2.7: outside an active encounter a resonance form exists only while a quest presents its condition), which is a place rule, not a health outcome. **Every point a player can attack from is within the Wraiths' reach:** they climb the steps and the rail, and the flare's throw reaches the upper terrace's front edge, so a ranged player at the rail is answered. Out-ranging never ends the vigil; only the song does. Melee or ranged; nothing requires ranged. **Pilgrims and Ivett are never engaged;** Wraiths do not path onto the upper terrace beyond its front edge. **Death:** respawn at the water-jar niche (E1); the vigil, if still running, continues; if it ended, `S02` is complete. Bark `EFD-B2.3`.

### EFD.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Find the keeper at Elyndra's shrine. | `EFD-D1` end | Yes | Board note `EFD-I1` or `EFD-B0.1` makes the quest Active at `S00` |
| `S01_tend` | Tend the flame with the keeper. | Sweep + garland + 3 stones + `EFD-I2` + `EFD-D2.10` | Yes | — |
| `S02_vigil` | Stay for the dusk vigil. | Dusk reached + vigil song end (EFD.5 played) | Yes | Pit pinned Surging for the song; EFD-E1 optional; re-offers each dusk if the player leaves mid-song |
| `S03_throat` | Find what feeds the flame. | `EFD-I5` + `EFD-I6` + crust cleared (Option A) **or** keep watch + held lamp (Option B) | Yes | Sets `EFD_THROAT`; the vent's schedule drops from three states to Cool/Working after this step |
| `S04_bead` | Tell the keeper what you found. | `EFD-D4` choice + `EFD-D4.40` end | Yes (→ **Completed**) | Sets `EFD_TELL` |

| Flag | Set by | Read by |
|---|---|---|
| `EFD_THROAT` = self / keeper | `S03` | `EFD-D4.02` |
| `EFD_TELL` = fitted / bare | `S04` | Bowl prop; vigil barks; EDS05 reading variant |

### EFD.8 Choices and consequences

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Set the bead** (`fitted`): *"Set it in the lip. Anyone who's been to school can read a bead."* | Ivett sets the warden's bead in the bowl's lip. It shows amber at the vigil, clear at night. Everyone raised in Emberholt reads it; the vent is no longer a secret from anyone who looks. | A warden's bead in Elyndra's flame. Some pilgrims stop coming ("It's a pipe now."). Ivett: "She'd laugh, or she'd not." | Vigil barks: pilgrims check the bead before they sing. If the pit surges post-quest, the bead goes red and Ivett stops the song; the optional Wraith moment is rare. |
| **Leave it bare** (`bare`): *"Keep the bead in your pocket. You know what's under it. That's enough."* | No bead. Ivett keeps the throat clear herself each season with her bar. The shrine says nothing; the keeper knows. | Surges come unannounced. At a post-quest vigil the pit sometimes surges and Wraiths form (a re-offered optional fight, EFD-E1 as written). | Vigil barks: pilgrims sing as they always have. Ivett nods to the warden's hand at the gate. |

**Both:** the flame stands steady after `S03`, the pilgrims keep coming, nobody says Elyndra is or is not, and the dusk vigil runs as a world moment.

### EFD.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| Bread and a bench | Access | The water-jar niche as a keep-watch point on the far Ridge. |
| The vigil | World moment | Repeatable at dusk; watch or join the song (no reward). |
| Small payment | Currency | From the offering box, at Ivett's insistence ("Pilgrims would want it.") [GD]. |
| Mining, Melee or Ranged XP | Action XP only [GD] | No Mining XP on the keeper path. No lump quest XP. |

### EFD.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Leaves during the vigil | `S02` re-offers at the next dusk. |
| Will not or cannot Mine | Option B; never blocked. |
| Death | Respawn at the water-jar niche; tending and throat progress kept; strikes on the crust kept. |
| Logout | Restore to the step: the terrace (`S00`–`S02`, `S04`); the jar niche in the crawl (`S03`). A carried garland returns to the basket. |
| Walking away | Stays Active; resume at Ivett (`EFD-D1.00`). |
| Co-op | The vigil, the throat and the bead are per player (each player's vigil plays in their own state; a partner may stand at another's vigil and fight its Wraiths; a defeat credits a partner only if their own `S02` is active). The flame-out sequence and the bowl prop are per player; shared presentation is a fallback only (CDR-6). Each player chooses their own `EFD_TELL`. |

### EFD.11 Integration needs

Standard: a board-note inspect that starts a quest; tending interactions (sweep, carry, lift); a scripted vigil (NPC song, three verses, ~3 min) that pins the pit Surging and drives the flame height prop; a flame-out sequence (prop off for ~3 s, relight VFX, audio thump, per player); Wraith re-forming on the pit's exhale with a cap (Act I ECW-E3 pattern); a quest-local Mining node; a held lamp interaction during a keep watch; a bowl-lip bead prop by `EFD_TELL`; the vent's schedule switching after `S03` (EI-HT-01 fallback: quest-pinned). No new system.

### EFD.12 Mystery ledger entry

| Field | Entry |
|---|---|
| Author truth | A vent feeds the flame; scree and offerings choked its throat; someone long ago set an iron ring so the draught would rise straight. Who set it is not decided. |
| Public belief | Elyndra's flame; it breathes; it came up from the fire that burned through a storm. |
| Observable | No fuel; a warm draught; the flame-out at the last verse; the iron ring. |
| Wrong reading | The vent proves there was never an Elyndra; or the flame-out proves there was. Neither follows. |
| Withheld | Who Elyndra is; who set the ring. |

### EFD.13 Dialogue

#### Cast notes

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Ivett Quarle** [NEW], keeper of Elyndra's Vent Shrine | The flame's habits; every pilgrim's name; the trapdoor. | What is under the bowl; who set the ring; whether Elyndra lived or lives. | Dry, devout without fuss. "I keep it. That's the job. Believing's the pilgrims' job." |
| **Pilgrim** (role) | The story. | — | Hushed; one line each. |
| **Hennet Ulm** [NEW, bible §5.2] (bark) | Ivett's note. | — | Feeds first. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| `EFD-B0.1` | HENNET | Cooling House, EH-M2 Completed, EFD Inactive | "Note on the board from Ivett Quarle. Keeps Elyndra's shrine out on the Ridge. She doesn't ask for things. Go and see what she's asking for." |
| `EFD-B1.1` | PILGRIM | Terrace, any | "It came up from the fire that burned through the storm. She carried it here in a pot. That's what my mother said." |
| `EFD-B1.2` | PILGRIM | Terrace, `S01` | "Don't put your hand in the bowl. Put a stone." |
| `EFD-B2.1` | IVETT | Vigil, verse one | (to the pilgrims) "Same as always. Not loud. She doesn't need loud." |
| `EFD-B2.2` | PILGRIM | Wraiths form | "Don't look down. Sing." |
| `EFD-B2.3` | IVETT | Player respawns during the vigil | "Water first. Then whatever you were doing down there." |
| `EFD-B4.1` | PILGRIM | Post-quest vigil, `fitted` | "Amber. We can sing." |
| `EFD-B4.2` | IVETT | Post-quest vigil, `fitted`, bead red | "Red. That'll do for tonight. Go home warm." |
| `EFD-B4.3` | PILGRIM | Post-quest, `bare` | "She hasn't gone out since the warden's hand came. Not once." |

#### Nodes

```
EFD-D1.00 [quest Active, returning] IVETT: "It's still standing on nothing. Where had you got to?" (pins step)  → end
EFD-D1.01 IVETT: (sweeping ash off the plinth's foot) "You're the warden's hand. You came. Good."
EFD-D1.02 IVETT: "I've kept this flame since I could hold a broom. I've never fed it. Not a coal. Not a drop of oil."
EFD-D1.03 IVETT: "This season it gutters, then it leaps. The pilgrims say she's angry." (beat) "I don't want it explained away. I want it looked at. Those are different."
  > "Whose flame is it?"                                            → EFD-D1.04
  > "Show me how you keep it."                                      → EFD-D1.06
EFD-D1.04 IVETT: "Elyndra's, they say. I've never seen her. I've met people who say they have. They're all very sure and none of them agree."   → EFD-D1.06
EFD-D1.06 IVETT: "Sweep the lip. Garland on the plinth. Take the stones out of its mouth; they push them in. Then look at it properly."   {event: S00 complete → S01_tend}  → end
```

```
EFD-D2.01 IVETT: "Well? What's it burning?"
  > [EFD-I2 read] "Nothing in the bowl. There's a hole in the bottom, and warm air coming up."   → EFD-D2.02
  > "I haven't looked yet."                                         → end
EFD-D2.02 IVETT: "I know about the hole. I've always known about the hole." (beat) "I never put my hand over it. That felt rude."
EFD-D2.03 IVETT: "Stay for the vigil. Dusk. Watch what it does when they sing. Then you'll know what I'm afraid of."
EFD-D2.10 IVETT: "There's a bench. There's water. There's bread if you're polite."   {event: S01 complete}  → end
EFD-D2.20 [after S02] IVETT: (still looking at the bowl) "It's done that four times this season. Never used to." (beat) "Under the bowl there's a trapdoor. I don't go down there much. Go down."   → EFD-D3.01
```

```
EFD-D3.01 IVETT: "Cellar, then a crawl. Hot. There's a jar halfway; drink at it, the wardens' way."
EFD-D3.02 IVETT: "If you find a little door with a little woman in it, come back up and tell me first."   (dry)   {event: S02 complete → S03_throat}  → end
EFD-D3.10 [at the throat, Option B offered] IVETT: (from behind, with a bar and a pilgrim) "I've a bar. I've a back. Mine's older than yours. Hold the lamp."   → end
EFD-D3.11 [Option B complete] IVETT: (leaning on the bar, breathing hard) "Forty years of stones." (beat) "They meant well."   → end
```

```
EFD-D4.01 IVETT: (at the bowl; the flame stands still and straight) "Look at her. Like a candle in a church."
EFD-D4.02 [EFD_THROAT = self] IVETT: "You broke it out. I heard you through the floor." / [= keeper] IVETT: "My back's going to say something about that tomorrow."
  > "There's a vent under the bowl. The offerings choked it. Someone set an iron ring in the rock, a long time ago."   → EFD-D4.03
EFD-D4.03 IVETT: "A ring." (beat) "Somebody wanted it to burn straight." (she looks at the pilgrims' benches) "That could be her. That could be a smith. It could be both."
EFD-D4.04 IVETT: (takes a bead out of her apron: emberglass in a little iron cup) "A warden left this here years back. Said it'd tell me when the flame's going wrong. I never set it."
EFD-D4.05 IVETT: "You read them. I don't, not well. Do I set it?"
  > "Set it in the lip. Anyone who's been to school can read a bead."   → EFD-D4.10
  > "Keep it in your pocket. You know what's under it. That's enough."   → EFD-D4.30
  > "What would the pilgrims want?"                                 → EFD-D4.06
EFD-D4.06 IVETT: "Half of them would want to know. Half would stop coming if they did. The other half would come more." (beat) "That's three halves. That's pilgrims."   → EFD-D4.05 options
EFD-D4.10 IVETT: (presses the bead into the soft rim mortar; it shows clear, then a faint amber) "There." (beat) "She'd laugh, or she'd not."
      {set EFD_TELL = fitted}  → EFD-D4.40
EFD-D4.30 IVETT: (puts the bead back in her apron) "Mine to know, then. I'll keep the throat clear every thaw. With the bar."
      {set EFD_TELL = bare}  → EFD-D4.40
EFD-D4.40 IVETT: (bread from a cloth; a few coins from the offering box) "Pilgrims would want you to have it. I asked none of them." (beat) "Come to a vigil. Sing or don't."
      {event: EFD-D4 end → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| `EFD-I1` | Cooling House board note | "*The keeper at Elyndra's shrine asks a warden's hand to look at the flame. Bread and a bench. I. Quarle.*" Starts the quest. |
| `EFD-I2` | The flame bowl | "No wick. No oil. No coal. A hole in the bowl's base, wide as a wrist. Warm air on the back of your hand. The flame stands on nothing you can see." |
| `EFD-I3` | Offering stones | "Smooth stones from every road. Some have names scratched on them. Some have only a mark." |
| `EFD-I4` | The pit (no tell) | "A vent grate at the bottom of a railed pit. Nobody has ever set a bead here. You read the shimmer instead." |
| `EFD-I5` | The throat's crust | "Scree, glass, and offering stones fused into a crust across the neck. The air comes up in coughs." |
| `EFD-I6` | The iron ring | "An iron ring set in the rock round the throat, so the draught rises straight up into the bowl. Old. No maker's mark. Older than any warden pattern you've seen." |
| `EFD-I7` | The bead in the lip (`fitted`) | [`EH_TELLS`] "Clear. Cool." / "Amber. Working." / "Red, crazed. Surging." |

### EFD.14 Open decisions

1. **Elyndra in canon vs the bible [Director].** `LORE/Characters/Caelmor_Characters_Region4_Emberholt.txt` §37 makes Elyndra the Cinderseer a living seer at "an abandoned vent shrine"; the bible keeps her myth only (§5.1, EDS05). This package never shows, places, dates or kills her: Ivett has never seen her and pilgrims disagree, and this shrine is kept, not abandoned. A later appearance at another, abandoned shrine stays possible. EDS05's withheld layer is reworded accordingly (§6).
2. The flame-out "four times this season" is a keeper's count of an event, not a date.

### EFD.15 Review log

| Check | Result |
|---|---|
| Belief kept | Ivett's "That could be her. That could be a smith. It could be both." Nothing denies or proves Elyndra. |
| Combat | Optional; Wraiths re-form only by the song's condition; standing engaged Wraiths fight on; no unreachable safe spot (the rail is in reach). |
| Evidence | The ring and the throat are objects read in place; they prove nothing about anyone. |
| Player spellcasting | None: the player sweeps, carries, breaks rock, holds a lamp. |

---
---

## EAD — The Vein-Touched Man

### EAD.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `emberholt.side.vein_touched_man` |
| Type | Settlement / care (bible §7.2). |
| Unlock | EH-M3 Completed. Offered by Sereth Vorn at his healing house in Cinderwall, inside the Ridge working gate (`EAD-D1`); the Red Door healer's bark sends the warden's hand there (`EAD-B0.1`). |
| Resume hook | Sereth at his door: `EAD-D1.00` "He's still out there, or he's on my cot. Which?" |
| Skills | Leatherworking ~[GD: low] (hook; loan alternative); Melee or Ranged |
| Combat share | ~15% (Slag Beetles in the tap cut) |
| Choice | How Myr is written in Sereth's book (`EAD_BOOK` = named / unnamed) |
| Unlocks | Sereth's healing house as a respawn and recovery point (Sereth can damp "low-level backlash" [CANON]: a full heal at his cot, no buff); Dalia's camp as a quench barrel and keep-watch point |
| **Anchor** (§7.1) | Ember-Fused workers; Sereth Vorn; the lower tiers Dalia Vret protects |
| **World-truth row** | H22 (the postwar city: how people hurt by its veins are cared for, and who asks after them) |
| **Revelation role** | None. Myr's "heartbeat below" is his own phrase [CANON voice]; nothing confirms or explains it, and it is not counted as a seed. |
| **Recurring evidence** | Sereth's clinic book (custodian: Sereth Vorn). |
| **State compliance** | Inactive / Active / Completed. Containment cannot fail (ED-2): segments interrupted are kept; the escort waits; the hook has a loan alternative; re-offers on return. |
| **Combat compliance** | Slag Beetles (EAD-E1) defeated at 0 HP, bursting into sparks. Myr Adalrek, Dalia Vret and the tap-hands are never targetable and never engaged (ED-2; beetles path round Myr's zone). Melee or ranged; ranged never required. Solo; partner credit only via the partner's own active step. No SX. |

**In one paragraph.** **Myr Adalrek** fell into a shallow ember fissure in a small quake, lived through what should have killed him, and has cracks in his skin that pulse when he is near a live vein. **Sereth Vorn**, the healer who keeps a small healing house by the Ridge gate, has been caring for him. Before dawn Myr walked out. A tap-hand saw him on the Ash Road, going toward the **Embervein Tap**, where **Ashfinger Dalia Vret**'s people cut a trench down to an exposed vein and draw from it without anyone's leave. Sereth cannot leave his other patients. He teaches the warden's hand his way ("his heat first, then cover him wet, then count him down; never his arms"), and the player makes a wet-hide wrap or borrows one, follows Myr's warm handprints up the road, and finds him sitting on the lip of the vein with the tap's bead red and beetles coming up the cut. Dalia's people will not go near. Dalia will not fight anyone, and will let the player shut her feed gate, though it costs her a night's draw. The player clears the beetles, shuts the gate, settles the wrap, counts him down, and walks him home on an arm. At Sereth's, the clinic book is open and an Emberguard notice is pinned to the door: *for evaluation*. How Myr is written in the book is the last thing to decide.

### EAD.2 Selection record and canon grounding

Selected shape: a care errand with a search (warm signs), a fight that is not about him, a containment that is the set piece, and an escort that is slow on purpose. Rejected: a protect-or-surrender choice (canon hook; surrendering a frightened, non-hostile man to an evaluation is outside this quest's care framing, and the Remnant's interest in him is withheld here); Myr as a combatant (ED-2).

| Element | Source | Status |
|---|---|---|
| Myr Adalrek: fell into a fissure; cracks that pulse; one eye like a coal near veins; "heartbeat below"; fled the Emberguard's "evaluation"; at risk of flares | Characters §36 | [CANON] |
| Sereth Vorn: healer, modest healing house, controlled emberheat, can dampen low-level backlash, quietly stubborn about the dignity of the wounded | Characters §35 | [CANON]; the house's place is [NEW] |
| Dalia Vret, "Ashfinger": Embervein Traffickers; illegal tapping; protective of the lower tiers; lost a brother in a Deepbrand-labelled "accident" | Characters §27 | [CANON]; the Embervein Tap camp is [NEW place on CANON anchor] (bible EP19) |
| Ember-Fused workers: never combatants; containment interaction | Bible ED-2; Act III `S01` pattern | [PROPOSAL — DIRECTOR] ED-2 |
| Flarecap glows orange near live veins | Dossier §XIII; bible §1.1 | [CANON] |
| The Red Door clinic and its healer (role) | Act I W4 | [NEW], consistent |
| The wet-hide wrap, the feed gate, the evaluation notice wording | This package | [NEW] |

### EAD.3 The places [MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **H1. Sereth's healing house** [NEW sub-site of EP02, inside the Ridge working gate] | Offer; wrap; the book | Two rooms. Cots under clean sheets; a quench trough; jars; a workbench with soaking tubs and rawhide. The **clinic book** on a shelf by the door. On the door, an **Emberguard notice** (from `S07`). Respawn for `S00`, `S01`, `S07`. |
| **H2. The Red Door clinic** (Act I W4) | Loan alternative | As Act I. The healer is dressing a burn. |
| **R1. The Ridge working gate** | Pass | As EOP R1. |
| **R2. The Ash Road** (EP09) | Myr's signs | Cracked road, burnt engravings in the kerbs (EDS01). Warm waymark stones. A culvert where flarecap grows. |
| **T1. Dalia's camp** (EP19) | Dalia; respawn for `S02`–`S06` | Tents of ember-thread canvas, a handcart, a **quench barrel** (cooling niche; keep-watch). Tap-hands with blackened fingers. Lamps hooded. |
| **T2. The tap cut** | EAD-E1; the feed gate | A trench cut down into the rock. **Flarecap** bright orange along both walls. Two **vents** in the walls. At its head, Dalia's **feed gate**: an iron slide across a channel, with a **bead** above it. |
| **T3. The vein lip** | Myr; containment | The trench ends at a lip over an exposed vein: a crack of orange light in the floor. Myr sits on the lip with his knees up. |

### EAD.4 Beats

**Beat 0: Sereth (`S00_offer`).** *Objective: Talk to the healer by the Ridge gate.* `EAD-D1`. Myr left before dawn; a tap-hand saw him on the Ash Road toward the tap. "Bring him back. Don't hurt him. Don't let anybody hurt him."

**Beat 1: His Way (`S01_wrap`).** *Objective: Learn Sereth's way and get a wet wrap.* Sereth teaches (`EAD-D2`): his heat first; cover him wet; count him down; never touch his arms. Then the wrap:
- **Option A (skill): make one** (**Leatherworking ~[GD: low]**). At Sereth's bench: **soak** a rawhide in the tub (interaction ~3 s), **cut** a wrap (standard Leatherworking at the bench), **lace** its edges (interaction ~3 s). ECD-02. Sets `EAD_WRAP = self`.
- **Option B (time-cost): borrow the Red Door's.** The Red Door healer has the clinic's wrap on a patient; keep watch one turn on the clinic bench until the dressing is done (`EAD-B1.1`). Sets `EAD_WRAP = loan`.
The wrap is carry-state and stays wet until used.

**Beat 2: The Road (`S02_road`).** *Objective: Follow Myr up the Ash Road.* Three signs in order along the road: a **scorched handprint** on a warm waymark (`EAD-I2`); a **clinic blanket**, smouldering, dropped at a bend (`EAD-I3`); the **culvert** where flarecap is bright and the mud holds a sitting mark (`EAD-I4`). He touched every warm stone. At the tap camp, Dalia (`EAD-D3`).

**Beat 3: The Tap (`S03_tap`).** *Objective: Talk to Dalia Vret.* `EAD-D3`. Her people will not go near him; the bead over the feed gate is red; beetles have come up the cut. "No fighting my people. Beetles, yes." She will let the player shut her gate: "It's not a city valve. It shuts hot. That's why it's mine." It costs her a night's draw.

**Beat 4: The Cut (`S04_cut`).** *Objective: Clear the cut.* **EAD-E1**: Slag Beetles in the trench (two waves). Myr's hazard zone sits at the lip, out of the fight; the beetles never enter it.

**Beat 5: Banked (`S05_contain`).** *Objective: Bring him down.* `[ED-2]` The containment interaction (Act III `EGA-D3` pattern, with a gate in place of a damper):
1. **Shut the feed gate** (channel ~3 s at the slide). The bead drops from red to amber; Myr's zone drops from Surging to Working.
2. **Settle the wrap** over his shoulders from behind (interaction ~2 s; the prompt is from behind only; never his arms).
3. **Count him down**: a 3-segment channel (~4 s each) in which the player counts his breaths as Sereth taught ("In. Hold. Out."). Myr talks (`EAD-D4`).
Moving away interrupts the current segment; completed segments are kept; the zone never spreads and never grows. On completion, the strange moment (EAD.5), and Myr's veins settle.

**Beat 6: The Walk (`S06_walk`).** *Objective: Walk him home.* Myr stands with a hand on the player's arm. **Escort:** he walks at a slow walk beside the player (the player cannot sprint while he holds on); twice on the road he stops at a warm waymark and puts his palm on it (`EAD-B6.*`); the player can wait or say his name (`EAD-D5.01`, he moves on). A tap-hand walks ahead with a hooded lamp to the working gate. No enemies on the road. Through the gate to Sereth's.

**Beat 7: The Book (`S07_book`).** *Objective: Settle Myr at the healing house.* Sereth puts him on a cot. The Emberguard notice is on the door (`EAD-I6`). Sereth asks how to write him (`EAD-D6`); Myr, lucid for a moment, gives the decision to the one who carried him. The choice (EAD.8). Sets `EAD_BOOK`. Small payment. **Quest Completed.**

### EAD.5 The breath in the cut (presentation spec: unease)

| Time | Element | Spec |
|---|---|---|
| Segment 1 | **With him** | On "in", the flarecap along both trench walls brightens; on "out", it dims. It keeps time with Myr's breathing, not the player's. |
| Segment 2 | **Slower** | The flarecap's pulse slows as his breath does. The vein's crack in the floor glows with it. The tap-hands at the trench head stop talking. |
| Segment 3 | **Still** | On the last "out" the cut goes dim and stays dim. His veins stop pulsing. He is banked. |
| +3 s | **Once more** | With his breathing settled and even, the vein's glow swells slowly up the cut once more, on its own, from far down, and fades. Nobody is breathing in time with it. |
| +6 s | **Myr** | Without opening his eyes: "It does that." (`EAD-D4.30`) |
| Meaning | None stated. Myr senses veins [CANON]. The pulse identifies nothing and proves nothing; no other character comments. |

### EAD.6 Encounters and hazards

Tuned for Expert identity (ED-10). Slag Beetles as Act I and Act III.

| Id | Enemies / hazard | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **EAD-E1** | Wave 1: 2 × Slag Beetle **crawler**, 1 × **sprayer**. Wave 2 (~20 s after wave 1 is half down): 1 × crawler, 1 × sprayer | The tap cut (T2), out of the wall vents and the trench floor | Crawlers guard the vents and the trench mouth; sprayers sit on vent lips and spit | **Crawler, Butt:** lowers its head, plates glowing (~1.5 s), then a short charge-butt with one-step knock-back. **Sprayer, Spit:** rears, abdomen swelling red (~1.0 s), then a slag gob that leaves a burning patch ~4 s. **Burst:** on defeat, ~0.5 s glow, then sparks in a 1-pace ring (light damage). | The beetles came up with the surge; the player clears the cut before anyone can reach him | 70–100 s; 55–75% HP |
| **EAD-H1** | Myr's zone `[ED-2]` | T3, ~2 m round him | Hazard (never an enemy) | His veins brighten; the stone round him glows | **Surging** (heavy periodic heat) until the gate is shut; **Working** after. Never spreads. Beetles never enter it and sprayers never target into it. | — |
| **EAD-H2** | Wall vents | T2 | Timed hazard | Ash lift ~1.5 s (~8 s cycle) | Damage and one-step knock-back | — |
| **EAD-H3** | Flarecap walls | T2 | Read | Bright orange | Nothing happens if struck by an attack (no trap); Dalia's bark teaches the miners' rule anyway (`EAD-B4.1`). | — |

**Rules.** Beetles defeated at 0 HP, bursting into sparks; harvestable where the economy allows. The trench is straight: ranged players shoot down it, melee players fight from the quench barrel's side of the trench head between exhales; the sprayers on the vent lips are reachable by both (the lips are a step up, no ledge out of reach). Nothing requires ranged. **Non-combatants:** Myr, Dalia, every tap-hand. Dalia's people stand at the camp edge and are never engaged. **Death:** respawn at the quench barrel (T1); defeated beetles stay defeated; a shut gate, a settled wrap and completed count segments are kept; Myr stays where he is.

### EAD.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to the healer by the Ridge gate. | `EAD-D1` accept | Yes | `EAD-B0.1` at the Red Door points the way |
| `S01_wrap` | Learn Sereth's way and get a wet wrap. | `EAD-D2` end + wrap made (Option A) **or** keep watch + loan given (Option B) | Yes | Sets `EAD_WRAP` |
| `S02_road` | Follow Myr up the Ash Road. | `EAD-I2` + `EAD-I3` + `EAD-I4` + enter camp volume (T1) | Yes | Inspect order free; the road is linear |
| `S03_tap` | Talk to Dalia Vret. | `EAD-D3` end | Yes | — |
| `S04_cut` | Clear the cut. | EAD-E1 (both waves) defeated | Yes | Vent states pinned Working; zone pinned Surging |
| `S05_contain` | Bring him down. | Gate channel + wrap interaction + 3 count segments | Yes | EAD.5 plays on completion |
| `S06_walk` | Walk him home. | Escort arrives at H1 volume | Yes | Escort waits if the player goes ahead; never lost |
| `S07_book` | Settle Myr at the healing house. | `EAD-D6` choice + `EAD-D6.40` end | Yes (→ **Completed**) | Sets `EAD_BOOK` |

| Flag | Set by | Read by |
|---|---|---|
| `EAD_WRAP` = self / loan | `S01` | `EAD-D5.12` |
| `EAD_BOOK` = named / unnamed | `S07` | Clinic book prop; healing-house barks |

### EAD.8 Choices and consequences

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **His name** (`named`): *"Write his name. Then when they come, Sereth can say no to his name."* | Sereth writes *Myr Adalrek. In my care. Not for evaluation.* in the book. | The notice has an address now. An Emberguard clerk calls every few presentation days; Sereth refuses at the door each time; Myr hears it and sleeps badly. | Bark scene at the door (`EAD-B7.1`). Myr greets the warden's hand by name: "You wrote me down." |
| **A care-name** (`unnamed`): *"Write him as the man from the tap. Nobody can ask for a man from the tap."* | Sereth writes *The man from the tap. In my care.* | Myr cannot draw ward relief or a Commons share in his own name; if he walks out again and is taken, Sereth has no name to claim him by. | The notice stays on the door, unanswered. Myr: "Nobody's harder to look for." (`EAD-B7.2`) |

No option is wrong. Myr stays in Sereth's care in both; Dalia's tap is open again the next night in both.

### EAD.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| Small payment | Currency | From Sereth ("I'm paid in eggs; you're paid in coin; that's fair.") [GD]. |
| The healing house | Access | A respawn and full-heal cot by the Ridge gate (no buff). |
| Dalia's camp | Access | Quench barrel and keep-watch at the tap. Dalia's people greet the player. |
| Leatherworking, Melee or Ranged XP | Action XP only [GD] | No Leatherworking XP on the loan path. No lump quest XP. |

### EAD.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Tries to wrap or count before the gate is shut | His zone is Surging; the prompt reads "Shut his heat first." (`EAD-B5.1`). No penalty. |
| Moves away mid-count | Segment interrupted; completed segments kept; Myr waits. |
| Will not or cannot do Leatherworking | Option B; never blocked. |
| Goes ahead on the walk | Myr stops and waits at the last waymark; a tap-hand calls (`EAD-B6.3`). He is never lost and never wanders into danger. |
| Death | Respawn at the quench barrel (`S02`–`S06`) or the healing house (`S00`, `S01`, `S07`); all kept. During `S06`, Myr waits at the last waymark. |
| Logout | Restore to the step's respawn. A wrap, if dropped, returns to Sereth's bench (Option A, re-soaked) or the Red Door (Option B, no second wait). During `S06`, Myr is back at the camp at the trench head, banked, and the walk restarts from there. |
| Walking away | Stays Active; resume at Sereth (`EAD-D1.00`) or Dalia (`EAD-D3.00` "He's still sitting there. My gate's still open."). |
| Co-op | Shared beetle fight; credit to a partner whose own `S04` is active (CDR-6). The gate, wrap, count, escort and book are per player: a partner's count does not bank your Myr, and each player walks their own Myr home in their own state (shared presentation fallback only). Each player makes their own `EAD_BOOK` choice. |

### EAD.11 Integration needs

Standard: a containment channel with kept segments and a refused-while-Surging prompt (Act III `S01` pattern); a gate channel that swaps the zone's state; a behind-only interaction facing for the wrap; flarecap and vein glow props pulsing on the count segments (scripted, per player); escort follow at a slow walk with two authored stops and a wait-if-ahead rule; a carry-state wet wrap; a door-notice prop and clinic-book variants by `EAD_BOOK`; a full-heal interaction at Sereth's cot. No new system.

### EAD.12 Mystery ledger entry

| Field | Entry |
|---|---|
| Author truth | Not decided by this package. Myr senses veins [CANON]; what he hears in them is withheld. |
| Public belief | "He's touched. He hears the veins." |
| Observable | The flarecap keeps his breath; the vein pulses once on its own; "It does that." |
| Wrong reading | Something below is calling him by name. Nothing here says so. |
| Withheld | What Myr hears. Never offered as evidence (bible §2.4). |

### EAD.13 Dialogue

#### Cast notes

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Sereth Vorn** [CANON] | Myr's case; his own way with heat and breath; that the Emberguard asked after Myr. | Why the Emberguard wants him; anything about the Remnant's interest (withheld). | Tired, kind, stubborn about dignity. "Care first. I promise nothing else." |
| **Myr Adalrek** [CANON] | Where the veins are. | What he hears. | Half clear statements, half sideways phrases. Calm, then urgent. Never an enemy. |
| **Dalia Vret** [CANON] | Her tap, her people, her gate. | — | Calm, rarely raises her voice. Long view. Protective of the lower tiers. Never fights here. |
| **Tap-hand** (role) | Where Myr went. | — | Nervous, practical. |
| **Red Door healer** (Act I role) | The loan wrap. | — | Short. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| `EAD-B0.1` | RED DOOR HEALER | Red Door, EH-M3 Completed, EAD Inactive | "Sereth by the Ridge gate's lost his walker again. Go and ask him. He won't ask you." |
| `EAD-B1.1` | RED DOOR HEALER | Option B wait | "Wrap's on a burn. When I'm done, it's yours. Sit." |
| `EAD-B2.1` | TAP-HAND (on the road) | `S02`, near the camp | "Your man? He walked past our lamps like they weren't there. Sat down on the lip. Dalia's at the cart." |
| `EAD-B4.1` | DALIA | `S04` start | "Mind the orange on the walls. Miners' rule: don't strike near it. Not that it'll bite. It's just manners." |
| `EAD-B5.1` | (prompt) | Wrap or count before the gate | "Shut his heat first." |
| `EAD-B6.1` | MYR | Walk, first waymark | (palm on the stone) "This one's warm all the way down." |
| `EAD-B6.2` | MYR | Walk, second waymark | "This one's tired." |
| `EAD-B6.3` | TAP-HAND | Player too far ahead | "He's stopped. He'll wait. He always waits for whoever's got his arm." |
| `EAD-B7.1` | SERETH (at the door, to an unseen clerk) | Post-quest, `named` | "He's in my care. His name's in my book. Your paper isn't." (the door shuts) |
| `EAD-B7.2` | MYR | Post-quest, `unnamed` | "Nobody's harder to look for." (a small smile) |
| `EAD-B7.3` | DALIA | Post-quest, camp | "Gate's open. He's not on my lip. Both good." |

#### Nodes

```
EAD-D1.00 [quest Active, returning] SERETH: "He's still out there, or he's on my cot. Which?" (pins step)  → end
EAD-D1.01 SERETH: (at a cot, his hand flat over a woman's burned shoulder; warmth comes off it like a hearth) "Warden's hand. One moment. Heat takes the time it takes."
EAD-D1.02 SERETH: "Myr Adalrek. He's been mine since the fissure. He walked out before dawn. A tap-hand saw him on the Ash Road."
EAD-D1.03 SERETH: "He goes to the veins. They call him, he says. They hurt him. Both are true."
  > "Where is he going?"                                            → EAD-D1.04
  > "Why not go yourself?"                                          → EAD-D1.06
EAD-D1.04 SERETH: "The Embervein Tap. Dalia Vret's people cut a trench down to a vein up there. They take from it without anyone's leave." (beat) "I don't ask. They bring me their burns."   → EAD-D1.08
EAD-D1.06 SERETH: (nods at the cots) "Four people. One of me."   → EAD-D1.08
EAD-D1.08 SERETH: "Bring him back. Don't hurt him. Don't let anybody hurt him." (beat) "I'll show you my way first."   {event: accept → S01_wrap}  → end
```

```
EAD-D2.01 SERETH: "When he flares, there are three things. In this order."
EAD-D2.02 SERETH: "His heat first. Whatever's feeding him, shut it, or get him off it."
EAD-D2.03 SERETH: "Then cover him wet. Shoulders and back. From behind, so he doesn't see hands coming."
EAD-D2.04 SERETH: "Then count him down. In. Hold. Out. Your voice, not his. He'll follow a voice."
EAD-D2.05 SERETH: "Never his arms. The cracks are worst there. You'll burn and he'll be ashamed of it."
  > "I'll make a wrap."                                             → EAD-D2.10
  > "Have you got one I can take?"                                  → EAD-D2.20
EAD-D2.10 SERETH: "Hide's in the tub. Soak it through, cut it wide, lace the edges so it holds water."   {event: Option A}  → end
EAD-D2.20 SERETH: "The Red Door has mine. On a burn. Ask nicely and wait."   {event: Option B}  → end
```

```
EAD-D3.00 [quest Active, returning] DALIA: "He's still sitting there. My gate's still open."  → end
EAD-D3.01 DALIA: (at the cart; ash on her sleeves, her fingers black to the knuckle) "You're Vorn's errand."
EAD-D3.02 DALIA: "He walked down my cut and sat on my lip. My people won't go near him. I don't blame them. I wouldn't send them."
EAD-D3.03 DALIA: "Beetles came up with the surge. They'll go for anything that moves that isn't him."
  > "I need the vein shut down."                                    → EAD-D3.04
  > "Why do you let him sit there?"                                 → EAD-D3.06
EAD-D3.04 DALIA: "There's a slide at the head of the cut. It's not a city valve. It shuts hot. That's why it's mine." (beat) "Costs me a night's draw. Shut it."   → EAD-D3.08
EAD-D3.06 DALIA: "Let him? Nobody lets him. He comes. Last time I sat with him till he cooled. I lost a brother to a Deepbrand 'accident'. I'm not losing a stranger to a crack in the floor."   → EAD-D3.04
EAD-D3.08 DALIA: "No fighting my people. Beetles, yes." (she hands over a hooded lamp) "Go on."   {event: S03 complete}  → end
```

```
EAD-D4.01 (At the lip. MYR sits with his knees up. The cracks along his forearms pulse orange. His left eye glows like a coal.)
EAD-D4.02 MYR: (not turning) "Don't come round the front. Everyone comes round the front."
EAD-D4.10 [segment 1] PLAYER (prompt: count): "In. Hold. Out." MYR: "Sereth's words. Your mouth." (beat) "Heartbeat below. It's slower tonight. I came to see if it was all right."
EAD-D4.20 [segment 2] PLAYER: "In. Hold. Out." MYR: "I know it's not a heart. I know. I'm not stupid. I'm cracked." (the flarecap dims on his out-breath)
EAD-D4.25 [segment 3] PLAYER: "In. Hold. Out." MYR: (quiet) "There." (the cracks stop pulsing)
EAD-D4.30 (The vein's glow swells up the cut once more on its own and fades.) MYR: (eyes shut) "It does that."   {event: S05 complete}  → end
```

```
EAD-D5.01 [walk, at a waymark] PLAYER: "Myr." MYR: (takes his hand off the stone) "Yes. Coming. Yes."   → end
EAD-D5.10 [walk, midway] MYR: "Sereth says the cracks are veins trying to sit in a person. I said I'd make room. He didn't laugh."
EAD-D5.12 [EAD_WRAP = self] MYR: (plucking at the wrap) "You laced this. It's crooked." (beat) "It's nice." / [= loan] MYR: "This is the Red Door's. It smells of their salve. I hate their salve."   → end
```

```
EAD-D6.01 SERETH: (Myr on a cot; Sereth's hand an inch above his forearm, warmth coming off it) "There. Banked."
EAD-D6.02 SERETH: (nods at the door) "That came while you were gone." (the Emberguard notice) "'For evaluation.' They asked after him before. He ran from them before."
EAD-D6.03 SERETH: "My book. Everyone I keep is in it. If his name's in it, they'll read it, and I'll say no to their face. If it's not, there's nothing for them to find. And nothing for me to claim him by, if they find him anyway."
EAD-D6.04 SERETH: (to Myr) "How do I write you?"
EAD-D6.05 MYR: (lucid, tired) "I can't hold a pen today." (beat; to the player) "You carried me. You say."
  > "Write his name. Then when they come, you can say no to his name."   → EAD-D6.10
  > "Write him as the man from the tap. Nobody can ask for a man from the tap."   → EAD-D6.30
EAD-D6.10 SERETH: (writes) "Myr Adalrek. In my care. Not for evaluation." (beat) "There. Now they have to talk to me."
      {set EAD_BOOK = named}  → EAD-D6.40
EAD-D6.30 SERETH: (writes) "The man from the tap. In my care." (beat) "I've a few of those. Nobody's ever asked for one."
      {set EAD_BOOK = unnamed}  → EAD-D6.40
EAD-D6.40 SERETH: (pays) "Coin. I'm paid in eggs; you're paid in coin. That's fair." (beat) "Come back if you're burned. I don't ask how."
      {event: EAD-D6 end → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| `EAD-I1` | Clinic book (before) | "Names, dates of care by season, what was done. Some lines have no name: *the woman from the slag tips*, *a boy, burned hands*." |
| `EAD-I2` | Warm waymark | "A handprint scorched into the soot on the stone. Five fingers, spread. Still warm." |
| `EAD-I3` | Clinic blanket | "One of Sereth's blankets, smouldering at the hem where it dragged on something hot." |
| `EAD-I4` | The culvert | "Flarecap bright orange along the culvert's lip. A sitting mark in the warm mud. He rested here." |
| `EAD-I5` | The feed gate bead | [`EH_TELLS`] "Red, crazed. Surging." / after the gate: "Amber. Working." |
| `EAD-I6` | Emberguard notice | "*Emberguard. Myr Adalrek, vein-touched, to present for evaluation. Any healer holding him to report.* A seal. No name of an officer." |
| `EAD-I7` | Clinic book (after) | `named`: "*Myr Adalrek. In my care. Not for evaluation.*" / `unnamed`: "*The man from the tap. In my care.*" |

### EAD.14 Open decisions

1. **EH-M6's fused worker** (Act III §14 item 14) stays a role. This package does not request that Myr be the worker: his case is a different kind (a vein at the Ridge, not a frost-night flare), and keeping EH-M6 independent of EAD needs no line. Recommend closing Act III item 14 as "not taken".
2. **"For evaluation."** The canon phrase of Myr's history; it is the Emberguard's notice, not "below", and is not presented as the EH-M2 ledger's line. If the Director prefers distance from EH-M2's wording, the notice can say "for assessment"; nothing else changes.
3. **Dalia's brother line** (`EAD-D3.06`) uses her canon history; it names Deepbrand only as the label on the accident and says nothing about what Deepbrand is.

### EAD.15 Review log

| Check | Result |
|---|---|
| ED-2 | Myr is a hazard zone ended by containment; never targetable; beetles avoid his zone. |
| No combat with Dalia | Her people never fight; she gives the gate. |
| CDR-1/2/6 | Beetles to 0 HP; ranged and melee viable in a straight trench with reachable lips; solo; per-player containment. |
| Evidence | The clinic book and the notice are records; the pulse proves nothing. |
| Dignity | Myr is asked; he defers to the one who carried him; Sereth's care is the same in both outcomes. |

---
---

## ECC — The Commissioner's Cargo `[ED-15]`

### ECC.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `emberholt.side.commissioners_cargo` |
| Type | Mystery (bible §7.2). |
| Unlock | EH-M4 Completed. Offered by Border-Warden Captain Haelric Stormvein at the wardens' post in the gate yards (`ECC-D1`); Sergeant Keld Dorrow's bark at the bonded shed points the way (`ECC-B0.1`). |
| Resume hook | Haelric at his table: `ECC-D1.00` "The case is where it was. So am I." |
| Skills | Smithing ~[GD: low–mid] (hook; farrier alternative); Melee or Ranged (optional) |
| Combat share | ~10%, optional (Dross Scavengers in the rope-store yard) |
| Choice | Who holds what was found (`EH_RIVERGLASS` = reported / held) |
| Unlocks | Haelric's post as a keep-watch point; Keld Dorrow's barks at the gate |
| **Anchor** (§7.1) | Embergate merchant houses; Trade Commissioner Oren Falx; Haelric Stormvein's Border-Wardens |
| **World-truth row** | H22 (postwar Emberholt's trade and its blind spots), H25 (the present pressure: someone buying another place's working hours) |
| **Revelation role** | **Seeds R15** (one bounded, discoverable act beyond Emberholt; FT-04). Owned by CV-M2 with its own custodians. In play the buyer is **unattributed**: no Remnant, Ashfall, Durell or Shadeweaver name; the river is not named; no Lowmark cause, transaction, route or carrier (ED-15; Part 4 ledger, Oren Falx row). |
| **Recurring evidence** | The gate manifest (gate clerks; Haelric's wardens' book) and the timetable case (bonded-shed custody, then the Marshal's office or Haelric's locked box). |
| **State compliance** | Inactive / Active / Completed. `EH_RIVERGLASS` = reported / held; no fail; the collection is never staked out; the Smithing hook has a farrier wait. |
| **Combat compliance** | Dross Scavengers (ECC-E1), optional, defeated at 0 HP with the ordinary human defeat presentation. Melee or ranged; neither required. Solo. Haelric, Keld, Oren Falx, his clerk, the carter, the rope-store keeper and every warden are never targetable. No SX. |

**In one paragraph.** A sealed document case is waiting in the bonded shed at Embergate under **Trade Commissioner Oren Falx**'s seal, consigned to *Ambry House, factors, the gate yards*. **Haelric Stormvein**'s wardens know every factor in the yards and nobody knows Ambry House. Haelric cannot break a Commissioner's seal and will not ask the Commissioner. The player reads the gate manifest, finds the carter who took earlier Ambry cases to a room over a rope-store, and opens the case without touching the seal, by drifting out its hinge pins at the farrier's anvil and forging two new ones. Inside are ruled sheets of a river's hours (locks, sluices, ferries, night barges) with every place written as a letter and a number, a corner mark Haelric has seen on other papers he has taken, and an unsigned slip: *Collect at the second bell.* Oren Falx, charming, signs hundreds of cases and cannot name Ambry's owner. Ambry House is an empty counting room with a new brass plate, a desk, a drop-slot and a rent book paid in advance by note. Haelric will not stake out the collection ("You'd see a hired boy, and they'd know we watched"). The player decides with him whether the case goes to the Grand Marshal's office under a warden's seal, or goes on to Ambry House as if nothing had happened while Haelric keeps a copy of what it said.

### ECC.2 Selection record and canon grounding

Selected shape: manifest → carter → open by the hinges (Smithing) → read → the Commissioner (no confession) → the empty room → custody choice. Rejected: a stake-out and pursuit (would attribute the buyer, which ED-15 forbids); an escort of Oren's caravan (canon hook, but it would place a route); matching the sheets to a Lowmark record (Part 4 ledger: no counterpart without the same transaction on both sides).

| Element | Source | Status |
|---|---|---|
| Oren Falx: interregional trade policy; wax-sealed ledgers; plausible deniability; looks the other way on some shipments | Characters §23 | [CANON]; his secrets are not used or shown |
| Haelric Stormvein: Border-Warden captain; has intercepted coded messages; does not know whom in the city to trust | Characters §26 | [CANON]; he names no external target or route (bible §5.1) |
| The Fog and Riverglass act: one discoverable Remnant act beyond Emberholt, unattributed in play | Bible ED-15, §2.5, §8.2; Arcs series table; Revelation Ledger R15 | [PROPOSAL — DIRECTOR] ED-15 |
| Embergate: gate, merchant yards; Emberguard checkpoints | Dossier §VII.1; bible EP01 | [CANON] |
| Ambry House, Keld Dorrow, the bonded shed, the wardens' farrier, the rope-store | This package | [NEW] |

### ECC.3 The places [MAP VERIFICATION REQUIRED]

All inside Embergate, in the merchant yards (bible §4.2: inside the gate). Nothing outside the gate is described.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **G1. The Border-Wardens' post** | Offer; reading; choice; respawn | A stone guardroom against the gate wall. Crossbow rack; grey cloaks on pegs; Haelric's table with his **locked box** and the **wardens' book**. Keep-watch bench. |
| **G2. The bonded shed** | Manifest; the case | A long shed where cargo waits for the Commissioner's seal. The **gate manifest** on a lectern under a lamp. Crates, bales, a shelf of sealed cases. Every case is warm to the touch from the shed's floor pipes except one. |
| **G3. The wardens' farrier's forge** | Smithing hook | A small yard forge for warden horses and fittings: anvil, drift punches, bar rack, quench tub, a bead on the forge hood. |
| **G4. The Commission house** | Oren Falx | A narrow upper office over the yards: wax, ledgers, a window that sees every wagon. A clerk at a standing desk. |
| **G5. The rope-store yard** | ECC-E1 (optional) | A walled yard under a rope-store: coils on pegs, a brass **winch**, an alley side-gate with an outside stair to the room above. |
| **G6. Ambry House's counting room** | The empty room | Above the rope-store, up the outside stair: a door with a new **brass plate** and a **drop-slot**. Inside: one desk, one chair, dust everywhere except two oblong clean patches on the desk. The rope-store keeper downstairs keeps the **rent book**. |

### ECC.4 Beats

**Beat 0: Haelric (`S00_offer`).** *Objective: Talk to the Border-Warden captain.* `ECC-D1`. The case; Ambry House; the seal he cannot break. "Find out what it is without breaking his wax. And without asking him first."

**Beat 1: The Manifest (`S01_manifest`).** *Objective: Read the manifest and look at the case.* Inspect the **manifest** (`ECC-I1`): *Commission papers, sealed. For Ambry House, factors, the gate yards. O. Falx.* and, further back this season, several earlier lines in the same form. Inspect the **case** (`ECC-I2`): leather over oak, iron bands, a hasp under the Commissioner's wax, two outside hinges. **The strange moment** (ECC.5) plays on first touch. Keld (`ECC-D2`) on the cork lining.

**Beat 2: The Carter (`S02_carter`).** *Objective: Find out where Ambry's cases go.* The carter at the shed door (`ECC-D3`): he took the earlier Ambry cases from the shed to a room over the rope-store and put them through a slot in the door; he was paid at the shed, by note; he never saw anyone. He took the case on at the shed, from the shelf, after the clerk sealed it; he does not ask where a case was before the shed.

**Beat 3: The Hinges (`S03_hinges`).** *Objective: Open the case without breaking the seal.* Haelric: "The seal's on the hasp. The hinges aren't sealed." Carry the case (carry-state) to the farrier's forge (G3).
- **Option A (skill): drift and replace** (**Smithing ~[GD: low–mid]**). **Drift** the two hinge pins out at the anvil (interaction ~2 s each); the old pins bend on the way out. **Forge** two new pins from bar (ECD-03): heat until the hood bead shows amber, draw, cut (standard Smithing at the anvil). Sets `ECC_PINS = self`.
- **Option B (time-cost): the farrier.** Leave the case with the wardens' farrier and keep watch one turn at Haelric's bench; at first light the pins are out and new ones are made (`ECC-B3.1`). Sets `ECC_PINS = farrier`.
Back to Haelric's table with the case and the pins.

**Beat 4: The River's Hours (`S04_read`).** *Objective: Read what is in the case.* At Haelric's table, lift the lid by its hinge side; the hasp and the wax stay closed. Inspect the **sheets** (`ECC-I4`) and the **slip** (`ECC-I5`). `ECC-D4`: Haelric reads over the player's shoulder: a river's hours; not a molten one; every place written as a letter and a number; a corner mark he has seen before on other papers he has taken, "never the same paper, never a name". Optional Lowmark line (`ECC-D4.20`, flavour only). Haelric copies the headings and the corner mark into his own book. The pins go back in; the case looks untouched.

**Beat 5: The Commissioner (`S05_commissioner`).** *Objective: Ask the Commissioner about Ambry House.* Oren Falx at the Commission house (`ECC-D5`). He signs what he is brought; Ambry House pays its fees on time; he could not say who owns it and sees no reason he should. If the player describes the corner mark, he is still for one beat too long, then smiles and says Captain Stormvein should bring him cases, not stories. He does not ask what was in the case. Nothing he says shows he knows what the sheets are for.

**Beat 6: Ambry House (`S06_room`).** *Objective: Find Ambry House.* The rope-store yard (G5): **ECC-E1** (optional; Dross Scavengers stripping the brass winch; the alley side-gate and outside stair avoid the yard). Up the outside stair to the door: the **brass plate** (`ECC-I6`), the **drop-slot**. Inside (the door is on the latch): the **desk** (`ECC-I7`). Downstairs, the rope-store keeper and the **rent book** (`ECC-I8`; `ECC-D6`): rent paid in advance by note; *No name; paid.* A lamp up there some nights, after the second bell; she has never seen who.

**Beat 7: Who Holds It (`S07_decide`).** *Objective: Decide with Haelric what happens to the case.* `ECC-D7`. Haelric refuses a stake-out. The choice (ECC.8). Sets `EH_RIVERGLASS`. Small payment. **Quest Completed.**

### ECC.5 The cold case (presentation spec: unease)

| Time | Element | Spec |
|---|---|---|
| First touch | **Warm shelf** | The bonded shed's floor pipes keep everything on the shelf warm: crates, bales, every other case. The player's hand passes along them. |
| 0–2 s | **Cold** | The Ambry case is cold. Not cool: cold, like a stone from a stream. A thin bloom of condensation appears where the player's palm rests, and fades. |
| 2–4 s | **Keld** | Keld, at the door, without looking round: "That one's been on a warm shelf two days. Hasn't warmed." |
| After | `ECC-D2.02` | "Cork-lined. Somebody wanted the paper kept dry. Or cool." |
| Meaning | Physical: a cork-lined, waxed case that came in at the gate and holds cold. It came from somewhere that is not here. Nothing says where. |

### ECC.6 Encounters and hazards

Tuned for Expert identity. Dross Scavengers as Act III EGA-E1.

| Id | Enemies | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **ECC-E1** (optional) | 2 × Dross Scavenger **scavenger**, 1 × **slinger** | The rope-store yard (G5), at the brass winch | Scavengers hold the winch with pry-bars; the slinger stands on a coil stack and throws | **Scavenger, Bar:** lifts the pry-bar overhead (~1.0 s), then an overhead strike. **Scavenger, Shove:** shoulder dips, feet set (~1.5 s), then a shove and one-step knock-back. **Slinger, Whirl:** sling whirls with a glowing slag pellet (~1.4 s), then a shot that leaves a burning patch ~4 s. **Slinger, Reload:** ~2.5 s visible reload (the window to close). | Brass-strippers who heard the room upstairs is empty. They know nothing about Ambry House and are never questioned. | 60–90 s; 60–80% HP |

**Rules.** Scavengers defeated at 0 HP with the ordinary human defeat presentation; no dialogue afterwards; the rope-store keeper's one sober line (`ECC-B6.2`). The coil stack is two steps high and climbable from the yard: the slinger is reachable by melee and duellable by ranged; there is no point in the yard or on the outside stair from which a player can attack without being answered (the slinger covers the stair). The yard is avoidable: the alley side-gate reaches the outside stair without entering the scavengers' aggro volume. **Combat never reveals evidence:** the scavengers carry brass, not paper. **Death:** respawn at the wardens' post (G1); defeated scavengers stay defeated; the case's state (open, pinned, read) is kept.

### ECC.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to the Border-Warden captain. | `ECC-D1` accept | Yes | `ECC-B0.1` at the bonded shed |
| `S01_manifest` | Read the manifest and look at the case. | `ECC-I1` + `ECC-I2` + `ECC-D2` end | Yes | ECC.5 plays on first case touch |
| `S02_carter` | Find out where Ambry's cases go. | `ECC-D3` end | Yes | — |
| `S03_hinges` | Open the case without breaking the seal. | Pins drifted + 2 pins forged (Option A) **or** keep watch + farrier done (Option B) | Yes | Sets `ECC_PINS`; the case is carry-state between G2, G3 and G1 |
| `S04_read` | Read what is in the case. | `ECC-I4` + `ECC-I5` + `ECC-D4` end | Yes | Optional `ECC-D4.20` with `UL_LEDGER_GIVEN` or `UL_LEDGER_TAKEN` |
| `S05_commissioner` | Ask the Commissioner about Ambry House. | `ECC-D5` end | Yes | — |
| `S06_room` | Find Ambry House. | `ECC-I6` + `ECC-I7` + `ECC-I8` + `ECC-D6` end | Yes | ECC-E1 optional |
| `S07_decide` | Decide with Haelric what happens to the case. | `ECC-D7` choice + `ECC-D7.40` end | Yes (→ **Completed**) | Sets `EH_RIVERGLASS` |

| Flag | Set by | Read by |
|---|---|---|
| `ECC_PINS` = self / farrier | `S03` | `ECC-D4.01` |
| **`EH_RIVERGLASS`** = reported / held `[ED-15]` | `S07` | CV-M2 (request) |
| *(read)* `UL_LEDGER_GIVEN` / `UL_LEDGER_TAKEN` (Lowmark) | — | `ECC-D4.20` option only |

### ECC.8 Choices and consequences

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Report it** (`reported`): *"Write it in your book and send the case to the Grand Marshal under your own seal."* | Haelric enters it in the wardens' book; a warden carries the case, still under the Commissioner's wax, to the Grand Marshal's office with Haelric's seal over it. It does not go to Ambry House. | Nobody collects at the second bell. Next day the brass plate is gone and the room is swept. Whatever was buying knows the gate looked. Oren Falx's clerk sends a polite note asking why a Commission case went to the Marshal. Haelric has shown his hand. | Haelric: "Now somebody upstairs has it. I hope it's the right somebody." (`ECC-B7.1`) The wardens' book carries the line (prop). CV-M2 may read the case from the Marshal's office (request). |
| **Let it go on** (`held`): *"Put it back on the shelf. Let it go where it was going. Keep your copy."* | The case goes back on the shelf, pins in, wax whole. The carter takes it up the outside stair at dusk. Haelric locks his copy of the headings and the corner mark in his box. | The sheets reach whoever buys them, and nobody knows what they do with them. Haelric carries it alone: "until I know whom to give it to." | The brass plate stays; a lamp burns up there some nights (prop). Keld's bark (`ECC-B7.2`). CV-M2 may read Haelric's copy (request). |

No option is wrong. In neither does the player learn who bought the sheets, whose river it is, or what the hours are for.

### ECC.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| Small payment | Currency | From the wardens' box ([GD]). |
| The wardens' post | Access | Keep-watch bench at the gate. |
| Smithing, Melee or Ranged XP | Action XP only [GD] | No Smithing XP on the farrier path. No lump quest XP. |

### ECC.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Tries to break the wax | Refused: "That's the Commissioner's seal. Haelric said no." (`ECC-B3.2`). Nothing resets. |
| Asks Haelric to watch the collection | Refused in `ECC-D7.05`; no stake-out step exists. |
| Will not or cannot Smith | Option B; never blocked. |
| Death | Respawn at the wardens' post; all kept. |
| Logout | Restore to the step: the post (`S00`, `S04`, `S07`), the shed (`S01`, `S02`), the forge (`S03`), the Commission house (`S05`), the rope-store (`S06`). The case, if dropped by logout, is on Haelric's table in its current state. |
| Walking away | Stays Active; resume at Haelric (`ECC-D1.00`). |
| Co-op | Shared optional fight; credit only via a partner's own active `S06` (CDR-6). The case, pins, sheets and choice are per player: each player opens and reads their own case in their own state; a partner's report does not report yours. Each sets their own `EH_RIVERGLASS`. Shared presentation fallback only. |

### ECC.11 Integration needs

Standard: a carry-state case with per-player states (sealed / pins out / read / re-pinned); a cold-to-touch feedback on first inspect (VFX condensation, ~2 s); Smithing at an anvil with a drift interaction; a keep-watch farrier option; read-in-place sheets and slip; a door plate, drop-slot and room props with day-after variants by `EH_RIVERGLASS`; an avoidable optional encounter with an alternate path. No new system.

### ECC.12 Mystery ledger entry

| Field | Entry |
|---|---|
| Author truth | [ED-15] The sheets are another region's river timetables, bought through intermediaries for the deep works' purposes, carried in through the gate to a front. CV-M2 owns this. |
| Public belief | "Commission papers." |
| Observable | A cold case; a river's hours with coded places; a recurring corner mark; an empty, prepaid room; a Commissioner who signs and does not ask. |
| Wrong reading | Oren Falx is the buyer (his signature is commercial routine, not proof: Part 4 ledger). The sheets prove a plot against the river's people (nothing here says what they are for). |
| Withheld | The buyer; whose river; what the hours are for; the corner mark's meaning. |

### ECC.13 Dialogue

#### Cast notes

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Haelric Stormvein** [CANON] | The yards; the corner mark on other papers he has taken. | Who uses the mark; whom in the city to trust. | Dutiful, reserved, suspicious; emotions tightly checked; protective of his wardens. Never names an external target or route. |
| **Keld Dorrow** [NEW], Border-Warden sergeant | Every factor in the yards; the shed. | — | Dry, observant, talks while looking elsewhere. |
| **Oren Falx** [CANON] | That he signs Ambry's cases; that Ambry pays its fees. | (Shown) nothing about the sheets' use. | Diplomatic, charming, neutral; peaceful leverage. Never confesses, never threatens. |
| **Commissioner's clerk** (role) | The seal routine. | — | Brisk. |
| **Carter** (role) | Where he took the cases. | Where they came from before the shed. | Unbothered. |
| **Rope-store keeper** (role) | The rent book. | Who pays it. | Gossipy and careful at once. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| `ECC-B0.1` | KELD | Bonded shed, EH-M4 Completed, ECC Inactive | "Captain's after somebody who reads more than labels. Post's by the wall." |
| `ECC-B3.1` | FARRIER | Option B complete | "Pins out, new pins cut. Didn't look inside. Don't tell me." |
| `ECC-B3.2` | (prompt) | Player tries the wax | "That's the Commissioner's seal. Haelric said no." |
| `ECC-B6.1` | ROPE-STORE KEEPER | Player enters the yard during ECC-E1 | "They're at my winch again! Somebody!" |
| `ECC-B6.2` | ROPE-STORE KEEPER | After ECC-E1 | "That's that. I'll want the brass back on before the wind." |
| `ECC-B7.1` | HAELRIC | Post-quest, `reported` | "Now somebody upstairs has it. I hope it's the right somebody." |
| `ECC-B7.2` | KELD | Post-quest, `held` | "Lamp's on up there again. Second bell. I don't look. Captain says don't look." |
| `ECC-B7.3` | OREN FALX'S CLERK | Post-quest, `reported`, Commission house | "The Commissioner asks the captain to send his cases to the Commission, not the Marshal. With respect." |

#### Nodes

```
ECC-D1.00 [quest Active, returning] HAELRIC: "The case is where it was. So am I." (pins step)  → end
ECC-D1.01 HAELRIC: (at his table; he does not get up) "You're the one who went down after the frame. Keld says you read more than labels."
ECC-D1.02 HAELRIC: "There's a case in the bonded shed. Commissioner's seal. Consigned to Ambry House, factors, the gate yards."
ECC-D1.03 HAELRIC: "My wardens know every factor in these yards. Every one. Nobody knows Ambry House."
  > "Open it."                                                      → ECC-D1.04
  > "Ask the Commissioner."                                         → ECC-D1.06
ECC-D1.04 HAELRIC: "I can't break his wax. Nobody on this gate can. And if I'm wrong about it, I've told the Commission I look at its cases."   → ECC-D1.08
ECC-D1.06 HAELRIC: "If I ask him first and I'm right, I've told the wrong man. If I ask him first and I'm wrong, I've insulted the right one." (beat) "Later."   → ECC-D1.08
ECC-D1.08 HAELRIC: "Find out what it is without breaking his wax. Start with the manifest. Keld'll show you."   {event: accept → S01_manifest}  → end
```

```
ECC-D2.01 KELD: (leaning on the shed door, watching the gate) "Every case on that shelf's warm. Floor pipes. That one's cold."
ECC-D2.02 KELD: (comes over; taps the leather) "Cork-lined. Somebody wanted the paper kept dry. Or cool."
ECC-D2.03 KELD: "Manifest's got Ambry lines going back to the thaw. Same words every time. 'Commission papers, sealed.' Commissioner's hand every time."
ECC-D2.04 KELD: "Carter's the fellow by the door with the bad hat. Ask him where they go."   {event: S01 complete}  → end
```

```
ECC-D3.01 CARTER: "Ambry? Room over the rope-store. Outside stair. Slot in the door. In it goes."
  > "Who's up there?"                                               → ECC-D3.02
  > "Where does the case come from?"                                → ECC-D3.04
ECC-D3.02 CARTER: "Never seen a soul. Paid at the shed, by note. I like that kind of job."   → ECC-D3.06
ECC-D3.04 CARTER: "From the shelf. After the clerk's sealed it. Before the shelf it's the gate's business, not mine. I don't ask where a case has been. You'd never get home."   → ECC-D3.06
ECC-D3.06 CARTER: "This one goes at dusk, same as ever. Unless somebody says it doesn't."   {event: S02 complete}  → end
```

```
ECC-D4.01 HAELRIC: [ECC_PINS = self] "Your pins. Good iron." / [= farrier] "Farrier says he didn't look. He looked." (lifts the lid on its hinge side; the hasp and the wax stay shut)
ECC-D4.02 HAELRIC: (reading over the player's shoulder; quietly) "Hours. Locks. Sluices. Ferries. 'Night barges.'"
ECC-D4.03 HAELRIC: "A river's hours. Not ours. We don't have a river that isn't molten."
ECC-D4.04 HAELRIC: "Every place is a letter and a number. Whoever wrote this didn't want a name on a page."
  > "Do you know the mark in the corner?"                           → ECC-D4.10
  > [UL_LEDGER_GIVEN or UL_LEDGER_TAKEN] "I've handled a pay book ruled like this."   → ECC-D4.20
  > "What's 'Collect at the second bell'?"                          → ECC-D4.30
ECC-D4.10 HAELRIC: "I've had that mark across this table before. On other papers, off other people. Never the same paper. Never a name." (beat) "I've never known who to show them to."   → ECC-D4.40
ECC-D4.20 HAELRIC: (looks at the ruling, then at the player) "Ruled paper's ruled paper. Every clerk in the world buys it from somebody." (beat) "Doesn't tell us whose."   → ECC-D4.40
ECC-D4.30 HAELRIC: "Somebody comes to that room at the second bell and takes what's in the slot." (beat) "Somebody paid to."   → ECC-D4.40
ECC-D4.40 HAELRIC: (copying the headings and the mark into his own book, small and neat) "Pins back. Lid down. It never opened." (beat) "Now go and ask the Commissioner about Ambry House. Ask about the house. Not the case."   {event: S04 complete}  → end
```

```
ECC-D5.01 OREN FALX: (rising, all courtesy) "The warden's hand. I hear you have been useful in the depths. Sit. Wine?"
ECC-D5.02 OREN FALX: "Ambry House? A small factor. Pays its fees on the day, which is more than the guilds do."
  > "Who owns it?"                                                  → ECC-D5.03
  > "You seal their cases."                                         → ECC-D5.05
ECC-D5.03 OREN FALX: "I couldn't tell you. I seal for a hundred houses. If I asked each one who owned it, the gate would close for a month." (smiles) "That's the opposite of my job."   → ECC-D5.07
ECC-D5.05 OREN FALX: "I seal what's brought to me and listed. Commission papers are commission papers. The gate stays open; the city eats." (beat) "Is there a complaint?"   → ECC-D5.07
ECC-D5.07 OREN FALX: (pleasantly) "Has Captain Stormvein sent you?"
  > [S04 complete] (Describe the corner mark.)                      → ECC-D5.10
  > "Just asking."                                                  → ECC-D5.20
ECC-D5.10 OREN FALX: (still, for one beat longer than the question needs; then the smile) "Clerks' marks. Every house has its own scrawl." (beat) "Tell the captain he should bring me cases, not stories. I'd be glad to look at any case he brings."   → ECC-D5.20
ECC-D5.20 OREN FALX: "Good day. Do come back when you want to be paid properly for something."   {event: S05 complete}  → end
```

```
ECC-D6.01 ROPE-STORE KEEPER: "Ambry? Upstairs. Rent's paid. Look." (turns the rent book round)
ECC-D6.02 ROPE-STORE KEEPER: "Paid in advance, by note, through the season. 'No name; paid.' That's what the note said to write, so I wrote it."
ECC-D6.03 ROPE-STORE KEEPER: "Lamp up there some nights. After the second bell. I've never seen who." (beat) "I've never gone up. Paid rent's the quietest kind."   {event: S06 complete (with I6, I7, I8)}  → end
```

```
ECC-D7.01 HAELRIC: "Well?"
ECC-D7.02 HAELRIC: (listens; then) "A cold case of somebody else's river, sealed in our name, going to a room nobody's in."
  > "Watch the room at the second bell."                            → ECC-D7.05
  > "What do we do with it?"                                        → ECC-D7.10
ECC-D7.05 HAELRIC: "And see what? A hired boy with a sack. Then whoever hired him knows the gate watched." (beat) "No."   → ECC-D7.10
ECC-D7.10 HAELRIC: "Two ways. I write it in my book and send it to the Grand Marshal under my seal. Or it goes on the shelf, goes up the stair at dusk, and I keep what we copied until I know who to give it to."
ECC-D7.11 HAELRIC: "Either way I don't know whose it is. Neither do you." (beat) "Say."
  > "Write it in your book and send the case to the Grand Marshal under your own seal."   → ECC-D7.20
  > "Put it back on the shelf. Let it go where it was going. Keep your copy."   → ECC-D7.30
ECC-D7.20 HAELRIC: (writes; seals the case over the Commissioner's wax with his own) "Then somebody upstairs has it." (beat) "And whoever was buying knows the gate looked."
      {set EH_RIVERGLASS = reported}  → ECC-D7.40
ECC-D7.30 HAELRIC: (locks his book in the box; turns the key twice) "Then it goes where it goes. And I carry this." (beat) "I've carried worse."
      {set EH_RIVERGLASS = held}  → ECC-D7.40
ECC-D7.40 HAELRIC: (pays from the wardens' box) "Keld will know your face at the gate. That's worth more than this." (beat) "Thank you."
      {event: ECC-D7 end → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| `ECC-I1` | Gate manifest | "*Commission papers, sealed. For Ambry House, factors, the gate yards. O. Falx.* Turning back through the season, the same line, in the same words, several times." |
| `ECC-I2` | The case | "Leather over oak, iron-banded. The hasp is under the Commissioner's wax. Two hinges on the outside, each with a pin." |
| `ECC-I3` | Hinge pin | "Iron pin through the knuckle. Not sealed. Peened over at one end." |
| `ECC-I4` | The sheets `[ED-15]` | "Ruled sheets. Columns of hours: *lock*, *sluice*, *ferry*, *night barge*. Every place is a letter and a number. In one corner of every sheet, the same small mark, pressed, not written." |
| `ECC-I5` | The slip | "*Collect at the second bell.* No name. No mark." |
| `ECC-I6` | Brass plate | "*AMBRY HOUSE, FACTORS.* New brass. The letters are cut shallow, as if nobody expected it to stay long." |
| `ECC-I7` | The desk | "Dust everywhere except two clean oblongs where something case-sized has sat. The drop-slot opens into a wire basket. Empty." |
| `ECC-I8` | Rent book | "*Ambry. Paid in advance, by note, through the season. No name; paid.*" |
| `ECC-I9` | Door (day after, `reported`) | "Screw holes where the plate was. The room is swept." |

### ECC.14 Open decisions

1. **ED-15 [Director].** If the Director cuts ECC, remove this package; `EH_RIVERGLASS` is never set and only CV-M2's request is affected. Nothing in Emberholt reads it.
2. **The Lowmark option** (`ECC-D4.20`) is the only Lowmark reference and is flavour: Haelric declines to match. Cut freely.
3. **The corner mark** is described, never drawn as a known faction sigil. Art should design a neutral clerk's press-mark; CV-M2 may give it meaning later.

### ECC.15 Review log

| Check | Result |
|---|---|
| ED-15 | No Remnant, Ashfall, Durell or Shadeweaver name; the river is unnamed; places coded; no route, origin or carrier beyond "came in at the gate"; no Lowmark transaction matched; no stake-out. |
| Oren Falx (Part 4 ledger) | Signs and smiles; one held beat; never shown to know the sheets' use; his canon secrets unused. |
| Haelric (bible §5.1) | Flags the cargo; names no external target or route. |
| Evidence | Manifest, case, sheets, rent book, carter, keeper. The scavengers carry brass and are never questioned. |
| CDR-1/2/6 | Optional fight to 0 HP; slinger reachable; solo; per-player case. |

---
---

## 5. Micro-events EME01–EME10

Each micro-event follows the Mire card (format model): a place, a visible invitation, one ordinary interaction, an immediate meaning, what it cannot prove. None is required for anything. Flags use the `EME##_` prefix and are read only by the micro-event itself unless stated. No items; rewards are a line, a nod, a bowl. Suggested content ids `emberholt.micro.<slug>`. Where a main package presents a micro-event in passing (Act I: EME01 gone wrong, EME02, EME03, EME04, EME06, EME09, EME10; Act III: EME02 in frost, EME10 balanced; EFC: EME03, EME07), the card here is the standing world version and the main's lines take precedence while that step is active.

### EME01 — A lantern at a gesture

| Field | Spec |
|---|---|
| Trigger | Any lane with doorway lamps at dusk (Cinderwall, the Cinderweave Quarter, Embergate). Not during `EGA_FROST` (EH-M6 `S00`–`S06`) or EH-M1 before `S06` (Act I shows it gone wrong). |
| What the player sees | A child lifts two fingers at a doorway lantern; it lights. The child looks round to see if anyone noticed. |
| Interaction | **Nod** (interaction on the child, ~1 s), or walk on. |
| Lines | [nod] CHILD: (a grin; the lantern brightens a hand) "Did you see?" · [walk on] (the child lights the next one anyway) · [EH-M1 Completed, Cinderwall] CHILD: "Warden's hand saw." |
| Persistence | `EME01_NODDED` (bool). |
| Repeatable | Every dusk, a different doorway. |
| Cannot prove | Anything. Heat follows the room; a noticed child's flame brightens. That is all. |

### EME02 — Mood banners

| Field | Spec |
|---|---|
| Trigger | Cinderwall lanes (W1 and the Cooling House lane), any time after first arrival. |
| What the player sees | Cinderweave cloths on poles over the lanes in one colour, changed by a dye-worker on a ladder every few presentation days. **Grey** after a burial; **white** on a feast or festival night (canon: white is ceremonial); **orange** in a working week; **yellow** when the ward is calm; **red** when the ward is running hot (a quarrel, a cold night). |
| Interaction | Inspect a banner; or ask the dye-worker on the ladder. |
| Lines | DYE-WORKER: "Grey's a burial. White's a feast. Orange is work." (beat) "Red's when we're all shouting. Nobody tells us. We hang it when we hear it." · [EH-M1 active, before `S06`] "Grey. Everything's grey this week." · [`EGA_FROST`] (Act III: stiff with ice; no line) |
| States | Grey / white / orange / yellow / red on a small authored rotation; mains pin grey (EH-M1) and frost (EH-M6). |
| Persistence | `EME02_ASKED`. |
| Repeatable | Always. |
| Cannot prove | Anything about any household. A banner is the ward's mood as the dye-worker heard it. |

### EME03 — The dimmed flame

| Field | Spec |
|---|---|
| Trigger | A Cooling House (Cinderwall's, or another ward's when added), on an authored "a death in the ward" day in the rotation (every several presentation days). Act I EGH `S08` and EFC `S05` present it with their own lines; they take precedence. |
| What the player sees | Every lamp in the room has been turned down one notch and left there. People eat quietly. The hood tell over the hearth reads a shade cooler. |
| Interaction | **Turn your table's lamp down a notch** (interaction ~1 s), or don't. |
| Lines | [turn down] HENNET: (a nod; no word) · [asked] HENNET: "Slag hand from the third lane. Down one for him. Up again tomorrow. We don't put them out. Never out." |
| Persistence | `EME03_DIMMED` (bool; whether the player has ever turned one down). |
| Repeatable | On each rotation day. |
| Cannot prove | Anything about the death. The dimming is manners, not testimony. |

### EME04 — Flame-balancing on the stair

| Field | Spec |
|---|---|
| Trigger | The Molten Stair (EP04), morning and noon, after EH-M2 `S01` (Act I presents it on the stair). |
| What the player sees | A line of students climbing with a small flame steady in each palm; an elder at the landing calls the breaths: "In. Hold. Climb." Failures are common; a flame goes out, a student laughs, relights it. |
| Interaction | **Walk with them** (follow interaction): the player climbs beside the line and stops on each "Hold" (three holds). The player holds no flame and casts nothing. |
| Lines | ELDER: "Hold." (the line stops) "Climb." · [the player stops on every hold] STUDENT (nearest): "You'd be good at this. If you had the hand." · [the player keeps walking through a hold] ELDER: "Our stair, outsider. Our breath." (no penalty) |
| Persistence | `EME04_WALKED`. |
| Repeatable | Each morning and noon. |
| Cannot prove | Anything about the test or the curriculum. It is a drill, done well. |

### EME05 — A hearthfire argument

| Field | Spec |
|---|---|
| Trigger | The Cinderwall Cooling House at dusk, after EH-M1 Completed; not during the frost. |
| What the player sees | Two neighbours argue whose turn it is at the hearth tonight (one with a stew pot, one with a kettle). The hood tell warms toward amber as voices rise. Someone starts banging a spoon. |
| Interaction | **Vote with a spoon** for the pot or the kettle (interaction: bang a spoon at that end of the table), or abstain. |
| Lines | NEIGHBOUR (pot): "Stew feeds eight. Kettle feeds one." · NEIGHBOUR (kettle): "One's my mother." · [vote] (the room's spoons follow, mostly; the winner takes the hearth; the loser gets the second hook) · HENNET (after any vote): "There. The hood's cooled. Sit down, both of you; you're running hot." |
| Persistence | `EME05_VOTED` = pot / kettle / none (last vote; flavour only). |
| Repeatable | Several dusks in the rotation, different neighbours. |
| Cannot prove | Anything. Heat follows the room; a calm room cools the hood. |

### EME06 — Shift bells

| Field | Spec |
|---|---|
| Trigger | Cinderwall and the Emberforges, at each shift change (presentation hour: morning, dusk). |
| What the player sees | A bell on a post rings the shift; the lanes fill with soot-black workers coming off and clean ones going on; then the lanes empty. |
| Interaction | None. |
| Lines | Ambient barks only: "Bell." / "That's me." / "Save me soup." |
| Persistence | None. |
| Repeatable | Every shift change. (EBL's bell post is the same prop; EBL's lines take precedence while EBL is active.) |
| Cannot prove | Anything. |

### EME07 — Warm stones

| Field | Spec |
|---|---|
| Trigger | The Cinderwall Cooling House, night, after EH-M1 Completed (EFC `S05` presents it at the naming; EFC's lines take precedence). |
| What the player sees | An elder by the hearth passes a warm stone round the bench while telling a story. Whoever holds the stone may speak; everyone else listens. |
| Interaction | **Hold the stone** when it reaches the player (interaction), then choose one line or pass it on. |
| Lines | ELDER (story, one of three in rotation): the year the gate froze shut; the smith who rang every bar twice; the cat that lived in the hood. · [player holds] > "It's warm." / > "Go on with the story." / > (pass it on) · ELDER: "Stone's for talking. Even that." |
| Persistence | `EME07_HELD`. |
| Repeatable | Each night in the rotation. |
| Cannot prove | Anything. Stories are stories; none is a record. |

### EME08 — Magma larks

| Field | Spec |
|---|---|
| Trigger | Any Ridge vent with heat shimmer (the Ash Roads, the Molten Scars, near Elyndra's shrine), day. |
| What the player sees | Small birds bathe in the shimmer over a vent, wings spread, feathers flashing emberlight. At a footstep they scatter. |
| Interaction | **Stand still** (stop moving for ~5 s at the edge of the flock volume): they settle back. Shed feathers lie on the warm stones as a gathering prop. |
| Lines | None (birdsong). · [EOP Completed, Molten Scars] (no line; EOP.5's lark ring does not repeat) |
| Persistence | `EME08_WATCHED`. |
| Repeatable | Always. Feather gathering and whether the feathers count for EWQ belong to the Work and Skills package; this card only places the flock and the prop. |
| Cannot prove | Anything. Larks bathe in heat. |

### EME09 — Hold it steady

| Field | Spec |
|---|---|
| Trigger | The Cinderweave courtyard at dusk, after EH-M2 Completed (Act I B10 places the invitation). |
| What the player sees | Children each hold a small flame in a palm, or a lantern, and try to keep it still the longest. Laughing loses. **Tavi Ostry** plays. |
| Interaction | **Join with a lantern** (the courtyard's spare lantern): a held interaction; keep still for ~6 s. Moving ends it (no penalty). The player does not cast; the lantern is lit by a child. |
| Lines | TAVI: "You have to not laugh. That's the whole game." · [`EEH_TAVI_LAUGHED`] TAVI: "Tell me the smith one again." (the player's option: > "No. You'll lose." → TAVI loses, laughing) · [player holds 6 s] CHILD: "Outsider wins!" / [Cinderwall-known] "Warden's hand wins!" · [player moves] TAVI: "You moved. Everyone saw." |
| Persistence | `EME09_PLAYED`; `EME09_WON` (bool). |
| Repeatable | Every dusk. |
| Cannot prove | Anything about the test. It is a game. |

### EME10 — The hourly tally

| Field | Spec |
|---|---|
| Trigger | The Gate Valve House public hall (EP26, V1), any hour after EH-M1 `S03` (Act I presents the board there). |
| What the player sees | Odile Prace calls the hour's figures and chalks the board: intake by vein, draws by ward. Before EH-M6, the last column never balances and its foot reads *old leaks*. After `EGA_BOARD_BALANCED`, it balances and reads *balanced*. |
| Interaction | **Read the board** (inspect). |
| Lines | ODILE (before): "Intake, full. Draws, as written. Old leaks, as ever." (beat) "That's not news. It's weather." · ODILE (after, `EGA_BOARD_BALANCED`): "Intake. Draws. Last column." (beat) "Balanced." (every hour; she never stops saying it; Act III §E.2) |
| Persistence | `EME10_READ`. The board's state is read from `EGA_BOARD_BALANCED` (one writer, Act III). |
| Repeatable | Every hour. |
| Cannot prove | Before EH-M6, where the shortfall goes (EH-M6 owns it). This card never explains "old leaks". |

---

## 6. Discoveries EDS01–EDS10 (three-layer framework)

Each discovery has a **surface** (what anyone sees), a **reading** (what a careful player learns, and the interaction that earns it) and, where marked, a **withheld** layer that no Emberholt content resolves. Discoveries are optional, set no quest steps and give no rewards beyond understanding. **Flags:** `EDS##_SEEN` (surface seen: entering the authored view volume or first inspect) and `EDS##_READ` (the reading's interaction completed); both are **persistent booleans on the character**. Suggested ids `emberholt.discovery.<slug>`. Evidence rule: none identifies a person, proves a claim or names the dead; none states a count of the held or of any people (D-C06) or names the precursor (D-C03). Availability: the Ridge discoveries open with the Ridge working gate after EH-M1; city discoveries from first arrival unless stated. **MAP VERIFICATION REQUIRED** for every placement.

### EDS01 — The Ash Roads (EP09)

| Layer | Content |
|---|---|
| Surface | Cracked old streets running out from the walls onto the Ridge, lined with burnt engravings in the kerbstones [CANON]. (`EDS01_SEEN` entering the first kerb volume past the working gate.) |
| Reading | **Kneel and rub the ash off a kerb engraving** (interaction ~3 s) at the marked stone where the road bends. Under the soot, a carved panel of flames and a band of symbols; across the symbols, straight chisel strokes, cut later and deliberately. Inspect: *"Flames, and under them a band of signs that aren't civic script. Someone chiselled across every sign, later, in straight strokes. The flames they left alone."* A herder, if asked: "Old marks. City had them cut off after the war. Nobody says why. Nobody asks." |
| Withheld | **Who carved them and who scraped them.** Nobody here calls the signs Volkhari. (R09 seed: the canon reading is that they are Volkhari symbols erased by the city; this discovery shows the erasure and names nothing.) |
| Flags | `EDS01_SEEN`; `EDS01_READ` on the rub. |
| Links | R09 seed (Revelation Ledger). After EH-M3, a player may draw their own conclusion; no line confirms it. |

### EDS02 — The Molten Scars (EP08)

| Layer | Content |
|---|---|
| Surface | Ridges melted into glass-smooth black slopes [CANON]. (`EDS02_SEEN` on the Scars' edge volume, also crossed in EOP `S02`.) |
| Reading | **Climb to the marked outcrop over the Scars and look back toward the walls** (inspect from the outcrop). From up here the glass lies in long fans, every fan's narrow end pointing back toward the city. Inspect: *"The glass runs in fans. Every fan starts narrow near the walls and spreads out across the ridge. Whatever melted this came from the city's side."* Teodor, if asked after EOP: "My grandfather said the Ridge used to be grass here. He said it once." |
| Withheld | **Who ordered it.** No unit, battle or casualty is named or counted. |
| Flags | `EDS02_SEEN`; `EDS02_READ` on the outcrop inspect. |
| Links | H13 (Emberholt's battle embercraft) by place only. |

### EDS03 — A backlash zone (EP03, a dye yard in the Cinderweave Quarter)

| Layer | Content |
|---|---|
| Surface | A circle of fused cobbles in an old dye yard, glassy and slightly sunk, with the yard's paving laid carefully round it. Dye-workers walk round it without looking. (`EDS03_SEEN` on first inspect.) |
| Reading | **Keep watch in the yard until its Working hour** (dusk, pinned) and inspect the circle again. Small flames lick up out of the joints of the fused stones for a few seconds, the air over it flickers, and the faint glow under the glass pulses slowly, then stops. Inspect: *"Fire out of nothing, for a breath, then gone. The yard laid its paving around this rather than mend it."* A dye-worker: "Backlash. Before my time. You don't stand on it at dusk. That's all anyone tells you." The flames are a hazard volume (light heat, ~3 s) only while they burn. |
| Withheld | **Who was hurt.** Nobody says. |
| Flags | `EDS03_SEEN`; `EDS03_READ` on the dusk inspect. |
| Links | Dossier "Emotional Backlash Zones" [CANON]. None. |

### EDS04 — The Ash-Clad Giant chalk (Cinderwall, a lane duct)

| Layer | Content |
|---|---|
| Surface | On a big brass-and-stone duct along a Cinderwall slag lane: a child's chalk drawing of a giant made of scribbled flame, walking down a stair into the ground. (`EDS04_SEEN` on first inspect.) |
| Reading | **Inspect the chalk closely**: beside the giant, in a different hand and a fire warden's crew chalk, *not funny*. Inspect: *"A giant of flame, walking down into the ground. Next to it, in warden's chalk: not funny."* Asked (after EH-M1), Veska: "Kids draw it. I wrote that." (beat) "Because people go down there for work." Asked, a child: "It's the Ash-Clad Giant. It lives under. Everybody knows." |
| Withheld | **Everything. Never explained.** No line says what the legend is about, where it came from, or whether anything is down there. The words "Fire Titan" are never used. |
| Flags | `EDS04_SEEN`; `EDS04_READ` on the close inspect. |
| Links | The Ash-Clad Giant legend [CANON]; R19 seed list (the legend only). |

### EDS05 — Elyndra's Vent Shrine (EP20)

| Layer | Content |
|---|---|
| Surface | Offerings heaped round a basalt bowl where a flame burns at a vent that never cools. (`EDS05_SEEN` on entering the terrace.) |
| Reading | **Put a hand on the plinth's base stone** (interaction ~2 s): warm, in every season, warm all the way through. Then **turn an offering stone** (inspect): names and marks scratched on the undersides, some fresh, some worn almost smooth. Inspect: *"The stone is warm to its heart. The offerings are stones from every road, with names scratched on the side that faces the ground."* Ivett (after EFD), `fitted`: "Bead says amber. Pilgrims say she's listening. Both, most nights." / `bare`: "Warm, yes. I keep it clear now. They don't know that. That's fine." Before EFD, a pilgrim: "She carried the flame up here. Elyndra. In a pot." |
| Withheld | **Who Elyndra is, and whether she still comes.** (Reworded from the bible's "whether Elyndra lived": canon's character file has her living; §EFD.14.) The vent is real; the story is belief. |
| Flags | `EDS05_SEEN`; `EDS05_READ` on the stone turn. |
| Links | EFD (the quest at the same place; this card is the standing world version, and EFD's lines take precedence while EFD is Active). |

### EDS06 — Cinderreach Spire's sign (EP24, the spire path)

| Layer | Content |
|---|---|
| Surface | On the path toward Cinderreach Spire, a weathered post with a sign, and beyond it an Emberguard bar across the path: *RESTRICTED. STRUCTURAL HAZARD.* [CANON]. The path beyond the bar is not walkable. (`EDS06_SEEN` on first inspect.) |
| Reading | **Brush the soot off the old sign** (interaction ~2 s) and compare it with the Emberguard bar's lettering (inspect both). The old sign's letters are older than civic script: the strokes join where civic letters stand apart, and one sign repeats twice with an arrow up the path. Inspect: *"An old waymark in a hand that doesn't match any civic sign in the city. The same sign twice, and an arrow up toward the spire. The bar below it is new, and says only: structural hazard."* |
| Withheld | **Its meaning.** Nobody in Emberholt reads that hand. What happens on the spire is not shown; the bar is never passable in Emberholt content. |
| Flags | `EDS06_SEEN`; `EDS06_READ` on the comparison. |
| Links | None. (The Speaker's high-holiday address from the spire is CV-M4's.) |

### EDS07 — The Cold Seam (EP21)

| Layer | Content |
|---|---|
| Surface | A fissure in the Ridge where no heat rises. People sit on the stones along its edge. Small stones are left in a line along the lip. (`EDS07_SEEN` entering the seam volume.) |
| Reading | **Pick up a stone from the scree and set it on the lip** (interaction ~2 s): it is cold in the hand, the only cold stone the player has held in Emberholt. Then **inspect the warden's bead** set into the rock at the seam's mouth: clear. Inspect: *"Cold stones in a row for the dead. The warden's bead in the rock reads clear, and has never read anything else, a sitter says. The only clear bead on the Ridge."* A sitter: "Comes here when there's nothing else to do with it. You sit. You leave a stone. You go home." |
| Withheld | **Why it is cold. Never explained** (bible §7.5). |
| Flags | `EDS07_SEEN`; `EDS07_READ` on setting a stone. |
| Links | EMS (Unburnt and Names package) carries a memory-stone here; this card never touches it, and EMS's lines take precedence while EMS is Active. |

### EDS08 — Joren Vale's draft map (EP01, a gate-yard crate)

| Layer | Content |
|---|---|
| Surface | In a split crate of waste paper at the gate yards' paper-buyer's stall, a torn survey sheet, ink over pencil. (`EDS08_SEEN` on first inspect.) |
| Reading | **Hold the sheet up to the yard lamp** (interaction ~3 s) so the pencil under the ink shows. The inked part is a fair plan of old mining shafts under the city. In pencil, below them, a cluster of small squares crossed through, each marked *sealed: no survey*. In the corner, in the same pencil: *J. Vale*. Inspect: *"A survey of old shafts. Under them, in pencil only, rooms drawn as crossed squares, each marked 'sealed: no survey'. Signed in the corner, J. Vale. Somebody inked the shafts and left the rooms in pencil."* The paper-buyer: "Comes in by the sack. I don't read it. I weigh it." |
| Withheld | **What the rooms were, and whether the plan is right.** The sheet is one surveyor's draft, not a record (Part 4 ledger, Joren Vale row: a possible custodian, not a truth source). |
| Flags | `EDS08_SEEN`; `EDS08_READ` on the lamp interaction. Available after EH-M1. |
| Links | R10 seed (sealed rooms on Joren Vale's maps). Joren Vale appears only as the hand on the sheet (bible §5.1). |

### EDS09 — The forge-collapse memorial (EP11, Cinderwall)

| Layer | Content |
|---|---|
| Surface | The bronze plaque on the old lower forge's wall, by the Undercroft stair head. Act I's inspect text (`ECW` inspect, Act I dialogue): *"Bronze, green at the edges. In memory of the shift hands of the lower forge, lost in the collapse. A list of names. Nobody has polished it for a long time."* Sets `EDS09_SEEN` (presented in EH-M1 `S01`; the same inspect anywhere sets it). With `EH_HOLLOW_TRUTH = told`: + *"Across it, in crew chalk: NOT A COLLAPSE."* |
| Reading | **Rub the verdigris off the names** (interaction ~3 s) and read the small trade-words cast beside each: *stoker*, *hammerman*, *water-carrier*, *night shift*, *night shift*. Inspect: *"Beside every name, a trade. Stokers. Hammermen. A water-carrier. Every one a shift hand. No rank, no scholar, no guard. Whoever was lost here was working the forge."* With `EH_HALF_NAME = named` (ENW's prop): + *"Beside one name, a chalk line and two words in a careful hand: walked out."* An old regular, if asked: "My grandmother's on there. Night shift. That's all they cast. That's all anyone knew." |
| Withheld | **Whether all were lost there.** (ENW owns the one case it resolves.) No number of names is stated. |
| Flags | `EDS09_SEEN` (one writer: the plaque inspect); `EDS09_READ` on the rub. |
| Links | R09 seed (civilians above the chamber, bible §2.2); ENW (sister file) owns the Half-Name Wall and the walked-out chalk. |

### EDS10 — A Volkhari Ash seizure notice (EP01, the gate yards' notice wall)

| Layer | Content |
|---|---|
| Surface | On the gate yards' notice wall among tariff lists and lost-cart notices: a printed seizure notice. *Contraband seized at this gate: Volkhari Ash. Possession is a crime.* (`EDS10_SEEN` on first inspect.) |
| Reading | **Compare the notice's mark with the gate's own notices** (inspect two neighbouring notices, then this one). Every other notice on the wall carries the gate's lamp stamp and a gate clerk's name. This one carries neither: only a mark of a delving-pick crossed with a brand, and *for the deep works*. Inspect: *"The gate's notices are stamped with the gate's lamp. This one isn't. It's signed for the deep works, with a pick-and-brand mark."* With EH-M3 Completed: + *"The same mark was on the work order in the crew's camp."* A gate clerk: "That's not ours. They pin what they like. Nobody takes it down." |
| Withheld | **What Volkhari Ash is made from.** Nobody says. No quantity is stated. |
| Flags | `EDS10_SEEN`; `EDS10_READ` on the comparison. Available after EH-M1. |
| Links | R10 seed ("Volkhari Ash" contraband, Revelation Ledger). Volkhari Ash appears only as this word on this notice (ED-11). |

---

## 7. File-level integration summary

| Need | Used by | Owner | Notes / fallback |
|---|---|---|---|
| Keep watch / presentation hour | All four quests; EME01/02/03/05/07/09; EDS03 | Systems | Lowmark convention; per player, never world time. |
| Heat states pinned per step (EI-HT-01 fallback) | EOP beads; EFD pit; EAD zone and vents | Systems | Quest-pinned states; no per-zone schedule needed. |
| Quest-start skill requirement | EOP (Hunting) | Systems / Schema | Mire MRH pattern. |
| Wallow-seeking boss AI with cappable wallows and a plate-glow buff | EOP | Gameplay / AI | Mire MRH patch-seeking loop plus a timed damage-reduction buff. |
| Resonance re-forming with a cap on a vent exhale | EFD | Systems | Act I ECW-E3 pattern; condition = the vigil song. |
| Scripted sequences (lark ring; flame-out; flarecap breath pulse; cold-case condensation) | EOP, EFD, EAD, ECC | VFX / Audio | Per-player event props. |
| Containment channel with kept segments and a refused-while-Surging prompt | EAD | Systems | Act III `S01` pattern (ED-2). |
| Escort follow at a slow walk with authored stops and wait-if-ahead | EAD | Systems | Standard escort. |
| Carry-state objects (sod, garland, wrap, case) | EOP, EFD, EAD, ECC | Systems | Act I convention; return to source on logout. |
| Smithing / Leatherworking / Mining at quest stations; quest-local Mining node | ECC, EAD, EFD | Systems / Economy | ECD-01 to ECD-04 for the economy pass. |
| Avoidable optional encounter with an alternate path | ECC | Level design | Side-gate and outside stair. |
| Persistent discovery booleans | EDS01–EDS10 | Schema | `EDS##_SEEN` / `EDS##_READ`. |
| Per-player props | All | Systems | Shared presentation fallback only (bible §9; MI-CO-06; CDR-6); never gates another player's navigation, interactions, credit or completion. |

No runtime need beyond bible §11.1–11.2 and standard requirement checks. Both bible runtime needs (EI-HT-01, EI-PR-01) are used here only in their fallback form.

---

## 8. Package review summary

| Check | Result |
|---|---|
| Brief fit (bible §7.2–7.5, §12) | EOP, EFD, EAD, ECC match their slate rows and §7.3 contracts (EOP Hunting with Old Plate as the side miniboss; EFD optional Wraiths, belief kept; EAD containment, beetles only, no combat with Dalia; ECC unattributed, optional scavengers, `EH_RIVERGLASS`). EME01–EME10 and EDS01–EDS10 match §7.4/§7.5 entry for entry, with the two deviations below. File name and contents confirmed against §12 Batch 3. |
| Six-field contract | On every summary card; Combat compliance states the CDR-6 solo test. |
| CDR-1 | Every enemy to 0 HP: boars, Old Plate, beetles, Wraiths, scavengers. No yield, flee, scatter, break-off or drive-off. Wraiths re-form only by condition; engaged Wraiths fight on when the condition ends. No SX. No defeated enemy speaks. |
| CDR-2 | Melee and ranged viable everywhere; nothing requires ranged; no unreachable safe spot (Old Plate reaches the rim; the Wraiths climb the rail and throw to the upper terrace's edge; the trench lips and the coil stack are reachable). |
| CDR-3 | No release wording. |
| CDR-4 | Standard systems only; one skill hook per quest with a time-cost alternative (EOP's requirement follows the bible's "Hunting skill quest"). |
| CDR-6 | Every step, boss and reward solo; per-player props, choices and flags; partner credit only via the partner's own active step. |
| Evidence | Records, objects and living people carry every fact; phenomena prove nothing; no evidence from combat or loot. |
| Reserved decisions | No D-E2, D-S1, `[INITIATE]`, D-3, C07 or "invaders" dependency. No Volkhari person appears; no count of the held or of anyone (D-C06); no precursor name or roster (D-C03). ECC nodes tagged `[ED-15]`; EAD's containment `[ED-2]`. |
| Revelation Ledger | No R09–R12 content revealed here; EDS01, EDS09 seed R09; EDS08, EDS10 seed R10; EDS04 carries the legend only (R19); ECC seeds R15 and leaves it to CV-M2. Nothing explains the Titan, the bindings, Perfect Flame or the buyer. |
| ED-15 (ECC) | Buyer unnamed; no Remnant, Ashfall, Durell or Shadeweaver word; river unnamed and places coded; no route, origin, carrier or transaction across regions; no Lowmark requirement (one flavour option, declined by Haelric); Oren Falx shown signing and smiling only (Part 4 ledger). |
| ED-16 | EDS09 reads ENW's `EH_HALF_NAME` for one chalk line; no Mire flag is read; no route. |
| Flags | One writer each. Region flag written: `EH_RIVERGLASS` only. Main-line flags read exist exactly as defined: `EH_TELLS`, `EH_HOLLOW_TRUTH`, `EEH_TAVI_LAUGHED`, `EGA_BOARD_BALANCED`, quest states for EH-M2/M3/M4; sister/region: `EH_HALF_NAME`; Lowmark: `UL_LEDGER_GIVEN`, `UL_LEDGER_TAKEN`. |
| Quest items | 0. |
| Map | Relative placement only; MAP VERIFICATION REQUIRED throughout; nothing beyond the Ridge or past Embergate is placed. |
| New names checked for collisions | **Ivett Quarle**, **Keld Dorrow**, **Ambry House** grepped across `04_CONTENT_PRODUCTION`, `LORE` and `00_ADMIN`: no hits outside this file. Teodor Marsk and Old Plate appear only in the bible. Ids `EOP-`, `EFD-`, `EAD-`, `ECC-` (dialogue, barks, inspects, encounters) and `ECD-01`–`ECD-04` are unused elsewhere. Rejected while naming: "Ilse" (near Ilyen, Ilverin), anything with "river" or "glass" in the front's name (would echo Lowmark's riverglass). |
| Deviations from the bible | (1) **EME02:** the bible's "red on a forge feast" changed to **white** on a feast (canon Cinderweave code: white ceremonial, red volatile); red now means the ward is running hot. (2) **EDS05 withheld layer** reworded from "whether Elyndra lived" to "who Elyndra is, and whether she still comes", because the canon character file has Elyndra living (EFD.14 item 1). (3) **Sereth's healing house** is placed as a new sub-site of Cinderwall by the Ridge working gate, distinct from the Red Door clinic (whose healer stays a role). (4) **EAD sets no region flag** and asks nothing of EH-M6 (Act III §14 item 14 recommended closed). |
| Open for the Director (consequential) | ED-15 (keep or cut ECC); Elyndra canon vs bible (EFD.14). |
