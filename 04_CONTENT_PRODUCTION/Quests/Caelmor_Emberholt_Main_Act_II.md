# Emberholt Main Questline, Act II: Ash-Stained Chains, The Speaker's Smile

**Status:** Authored production content for Creative Director milestone review (2026-11-14). This package implements Emberholt main milestones EH-M4 and EH-M5 (bible §6, §6.1), which carry Act II from the Red-Lit roll's "held below" to the Act II turn on the Ash Terraces. It follows the Emberholt Act I package (`Caelmor_Emberholt_Main_Act_I.md`), itself the Mire, Thornfell and Lowmark act-package format. Everything marked **[NEW]** is authored and not canon until the Director promotes it (ED-19: promote nothing). Everything marked **[PROPOSAL — DIRECTOR]** rests on an open bible §3 decision. **[CANON]** items come from the Emberholt dossier, the Emberholt character file, Factions and the Part 4 ledger. **[APPROVED — id]** items rest on an architecture ruling (FT-02d, FT-04, D-C03, D-C06). No schema, production JSON or C# is created here. Emberholt is an internal production milestone of the complete game (CDR-3). Combat follows the Director rulings (`Caelmor_Director_Rulings_Combat_Ranged_Release.md`): every enemy is defeated at 0 HP (CDR-1), every fight accepts melee or ranged and none requires ranged (CDR-2), standard RPG systems are preferred to bespoke simulation (CDR-4), and every step, boss and reward is completable solo with co-op as optional assistance (CDR-6). Emberholt registers no scripted-survival exception (rulings §4; bible §3 "SX proposal: none").

**Controlling document:** `04_CONTENT_PRODUCTION/Quests/Caelmor_Emberholt_Narrative_Production_Bible.md`. Its §6 table, §6.1 briefs and §6.2 contract rows for EH-M4 (`EAC`) and EH-M5 (`ESS`) are binding and are implemented as written; the codes are confirmed against bible §6. Where this package adds detail it is marked [NEW] and stays inside the bible's cast (§5), places (§4.2), flags (§9.1), encounter families (§10) and conventions (§11). Where it has to read a brief more narrowly, reorder a beat or add a sub-site, the reason is recorded in that quest's open decisions (§A14, §B14); the bible is not edited.

**Companion file:** `04_CONTENT_PRODUCTION/Dialogue & Narrative/Caelmor_Emberholt_Main_Act_II_Dialogue.md`. It holds cast notes, every dialogue node referenced here (`EAC-`, `ESS-` prefixes), barks, inspect texts and the full text of every document (the proving-ring slate, the Speaker's outgoing letter, the kept answers, the vigil access book, the chamber record, Ralenne's script and the suggestion slip, Kaevren's intercepts).

**Reserved decisions in this package. Nothing here decides them.**
- **Thalan's fate (D-E2, ruled 2026-11-15): fixed liberation** (bible ED-4, §3.2; Review §2 contradiction 7; Architecture §5.0). Thalan is freed in EH-M4, with his own voiced consent to leaving; liberation is the only outcome. The aid-in-place branch (`EAC-D10`, `EAC-B8`, `EAC_ACCOUNT_PROMISED` and every aided read) is removed. Both ways of freeing him stay: the Smithing drift and the two-cool-cycle hand work. Thalan survives and can give testimony at convergence (CV-M4 rest-binding). His liberation does not resolve the Remnant threat or the Fire Titan's suffering. `EH_THALAN` keeps its id with one value, `freed`, set at `S06`. Never an option to end his life or exploit him.
- **The Speaker (D-S1, ruled 2026-11-15): idealist and manipulator** (bible ED-5, §3.2; Review §2 contradiction 2; Architecture §5.0). He genuinely believes in Emberholt's discipline, progress and strength, and he enjoys and pursues personal authority. He knowingly takes part in institutional manipulation and accepts harmful compromises for his rise: the letters show him asking for and accepting that rise, letting orders go round the Marshal through his own letter-room, and choosing not to ask what the deep works are for (§6.1). The Remnant also works on him through planted dreams that exploit those convictions: the chamber record shows his vigil dreams set for him, which he sincerely believes are his own and divine (character file; Part 4 ledger). The dreams do not absolve him; he is neither an innocent puppet nor an omniscient mastermind. He lacks the Ashfall endgame and does not understand Perfect Flame. Nothing shows him knowing that his dreams are set. He never fights, never confesses, never lies outright (he uses omission), and stays in office in both outcomes; `EH_SPEAKER` remains the player's outcome. The "wholly puppet" and "wholly mastermind" swap notes are resolved and removed (§B14.1).
- **Other tags.** `[ALLOCATION]` (ED-1): one Ralenne variant line in EH-M5 `S02` (`ESS-D3.03`). `[ED-12]`: protected Volkhari testimony and self-disclosure (Dahrin, Asera, Thennek, Thalan, Maeryn). `[ED-6]`: the Warrens' "infiltration" built from routes, a favour, sigil doors, plates and fights. `[ED-17]`: Serix's unscripted visions reported as his experience only. ED-3 (ruled 2026-11-15: Iven Calder) does not apply: Act II never shows or speaks the initiate's name. D-EL (ruled 2026-11-15): Elyndra the Cinderseer can be consulted once, optionally, during EH-M5 (`ESS-D12`, §B6 optional lead); no step waits on her.

---

## Act II header

### What Act II does

Act I ended with a glassed roll, a line nobody says aloud, and a sheet that said one elder was "taken in the purge after; held below". Act II answers the second half of that sentence and then turns the player's eyes upward. In EH-M4 the player goes below, past plates and sigil doors, and finds that "held below" is not history: a Volkhari elder is alive in a frame that feeds a proving ring, under a slate headed *Perfect Flame* (R10). In EH-M5 the player comes back up into the brightest part of the city and finds the same patience at work in daylight: a rehearsal that teaches a crowd to breathe on a beat nobody wrote, a Speaker who asked for help in his rise, and vigil dreams that were set for him (R11, R12). The act's job is to make the hidden order present-tense without making it a villain the player can fight: the player reads plates, doors, a slate, letters and a record; the only things they fight are guards, constructs and Wraiths.

| Quest | The player learns | By doing |
|---|---|---|
| EH-M4 **Ash-Stained Chains** | Pressure plates (a primed plate shows a red, crazed tell like a warden's bead: step round it or wait for it to vent and cool). That a Volkhari breath-keeper can bring a hot room down a band, and decides how far she goes. That "held below" is now: Thalan Veyr is alive in a basalt frame, and the frame feeds a proving ring logged as *Perfect Flame: trial series*. That Volkhari are not gone, and that what is said about them is theirs to decide. | Hearing a hunted man's account in a seamstress's back room, borrowing a door from an Overseer, following a pathfinder down an old shaft, crossing a plate run, reading doors with a stone that warms, fighting a construct on a floor that primes like a clock, and then asking an old man what he wants and doing it with a forge and an anvil that were built to keep him. |
| EH-M5 **The Speaker's Smile** | That the High Kindling rehearsals teach a crowd to breathe in step on a fifth beat nobody's cue sheet holds. That the Magistrix's best lines arrive on unsigned slips from the vigil. That the Speaker asked for his rise and was given it, let orders go round the Marshal to keep it, and does not know what the deep works are for. That his vigil dreams were set by name and night, and that not every dream in the record was set. | Standing in a crowd and reading brazier tells on cue, comparing a script with a slip, buying a way through the pipes from a man in a glass mask, reading letters and taking the ones he kept, dousing braziers under a frightened initiate's eyes, shooting or climbing to a damper, copying a record under witness, feeling your own breath fall in with a crowd, and deciding who hears it. |

**Act II turn (Arcs §3.3; bible §8.3 misunderstanding ladder):** the player moves from "papers kept by someone" to "a present operation with a man in a frame and a hand in the Speaker's dreams", and from "the Speaker is the city's pride" (or "the Speaker is the villain") to a man who believes in his city, likes being its voice, knowingly took help and let harm be done for it, and sincerely dreams what he is given (D-S1, ruled 2026-11-15). The Remnant is still never named in public speech (bible §1.2); the player has seen its work, not its face. The last thing the player sees in Act II is the Speaker, still in office, thanking someone. EH-M6 follows on the player's next entry to Cinderwall (`EGA_FROST`).

### Dependencies on other regions

**None.** Act II reads no Lowmark, Thornfell or Mire flag and asserts nothing about another region. Both quests are reachable by any player who completed EH-M3 (whose cross-region gate, ED-7, is the only one in Emberholt's main line).

### Region flags (bible §9.1 only)

| Flag | Act II role |
|---|---|
| `EH_THALAN` = freed (D-E2, ruled 2026-11-15) | **Set** by EH-M4 `S06` (one value). Read by EH-M4 `S07` and `EAC-D11`; EH-M6 tally board (§9.3 item 5); ETB (Asera's lines); CV-M4 testimony note (Thalan's testimony at the rest-binding). |
| `EH_SPEAKER` = challenged / exposed (D-S1, ruled 2026-11-15) | **Set** by EH-M5 `S06`. Read by `ESS-B9` terrace barks; EH-M6 letter; CV-M4. |
| `EH_TELLS` | Read: plate and brazier tells give their state on inspect (always set by this point). |
| `EH_HOLLOW_TRUTH` = told / kept | Read by `EAC-D2.12`/`.13` (Dahrin's variant). |
| `EH_CURRICULUM` = guild / evidence | Read by `ESS-I8` (the dormitory door notice and cots). |
| `EH_COLD_WARD` = posted / settled `[ALLOCATION]` | Read by `ESS-D3.03` (one Ralenne line). |

Act II invents no other `EH_` flag. Quest-local flags use `EAC_` and `ESS_`. Act I quest-local flags read here: `EGH_SHEET_READ`, `EGH_STONE_HEARD`, `EGH_FLARECAP`, `EGH_WORK_ORDER`, `EGH_ORDER_SHOWN`, `EEH_LEDGER_READ`, `ECW_RAT_SEEN`, `ECW_SOB_HEARD`, each with the reading Act I already promised. Every flag has exactly one writer.

### Quest-item budget (bible §9.4: five for the whole of Emberholt)

| Item | Quest | Fate |
|---|---|---|
| `EAC_sigil_stone` (Dahrin's sigil-stone, a palm-sized dark stone with a seam of emberglass) | EH-M4 | Given by Dahrin in `S01`. Read as a held item in `S04`–`S05` (its inspect and glow give cold / cool / warm by the nearest Remnant door). Returned to Dahrin at `S07` (`EAC-D11.30`). Not droppable, not sellable. Bible §9.4 names it the fifth item; fallback in §A14.4. |
| `ESS_letters` (the bundle of answers the Speaker kept, tied with a ribbon) | EH-M5 | Taken from the letter-case in Speaker's Hall in `S03`. Removed at `S06`: with `challenged`, to Kaevren's ledger box; with `exposed`, under Vael Trossen's seal to the sealed inquiry. Not droppable, not sellable. |

**Act II total: 2. Emberholt running total: 4 of 5** (`EEH_ledger`, `EGH_roll`, `EAC_sigil_stone`, `ESS_letters`); `EGA_junction_book` (EH-M6) is the fifth. Everything else is a carry-state object (Yorven's gate key, the forged drift, the vigil ewer, the record copy, Kaevren's intercepts), an inspectable world object (plates, doors, the slate, the outgoing letter, the access book, the cue sheet, the script, the slip, the chamber record), or knowledge in flags.

### Structure check against the bible §6 core verbs

| Quest | Primary verb | Distinct from |
|---|---|---|
| EH-M4 | **find the way by sigils**, avoid primed plates, decide with Thalan | A descent with allies who will not fight, a door puzzle read with a held stone and the flarecap Act I taught, a construct fight on a floor that primes in rotation, and a choice the player must ask another person to make. |
| EH-M5 | **watch, compare and copy**: rehearsal tells, letters, a chamber record | A civic investigation in daylight: a crowd to read, a script to compare, a duct to crawl, a letter-case to open, one fight in sleep rooms, a damper to shoot or climb to, a record to copy under witness, and a choice about who hears. Combat ~15%. |

No two quests in Emberholt share a set piece. Combat changes family across the act: Deepbrand Crews and the first Emberdeep Sentinels (EH-M4) → Cinder Wraiths only (EH-M5). The readable system changes job again: EH-M4 makes tells into **traps** (plates) and **clocks** (the proving ring), and lets a person bring a room down; EH-M5 turns tells on a **crowd** and makes the player feel heat following the room in their own breath.

### Unlocks across Act II (bible §7)

| After | Unlocks |
|---|---|
| EH-M4 | *The Commissioner's Cargo* (ECC); *Three Breaths* (ETB, also needs EST); EH-M5 |
| EH-M5 | *Glassmoth's Tonic* (EGT); EH-M6 (auto-offered on next entry to Cinderwall, `EGA_FROST`) |

### Act II clocks and conventions (additions to Act I's table)

Act I's conventions table (presentation hour and keep watch, heat states pinned per step, tells, vent breath, cooling niches, heat follows the room, resonance re-forming, channels with kept progress, carry-state objects, per-player props, agility triggers with walkable fallbacks, origin-neutral address "warden's hand") applies unchanged. Act II adds:

| Convention | Act II use |
|---|---|
| **Pressure plates** `[ED-6]` (bible §1.1, ED-6: "heat-pressure traps are pressure plates whose tells show when they are primed") | A floor plate with an emberglass tell set in its face. **Primed:** red with a crazed skin. Stepping on a primed plate vents a column of heat after ~0.6 s (damage and a one-step knock-back). **Spent:** clear for ~8 s after venting. **Re-priming:** amber for ~2 s, then primed. Step round on the unplated ribs, or wait for a plate to vent (throw nothing; just wait or let it vent empty on its own cycle) and cross while it is clear. Never a reset, never a trap door, never an alarm. |
| **Asera's three breaths** `[ED-12]` | In a Surging heat room, stand in the niche beside Asera and breathe on her count: a 3-segment channel (~4 s each) whose segments end on her "three". On completion the room drops one band (Surging → Working) and stays there for the step. **Alternative:** keep watch in the niche (one turn of the presentation hour). Asera does the craft; the player keeps time. No player spellcasting (bible §11.8). Same pattern as Idra's count in EH-M2. |
| **The sigil-stone** (`EAC_sigil_stone`) | A held quest item. Near a Remnant door its seam glows and its inspect reads *cold*, *cool* or *warm*. Warm means a true door, or heat close behind the wall (a live vein or a hot conduit); flarecap tells a vein and Dahrin's mark tells a door. The stone never points, never speaks and never shows a map. |
| **Escort-follow** (EH-M4, Thalan's walk out) | The EH-M2 escort-follow: the NPC walks with the player at walking pace, stops when they stop, and is never targetable and never harmed by hazards. |
| **Rehearsal inspect windows** (EH-M5) | During a scripted rehearsal run (~90 s), a conductor's cue opens a short window (~6 s) on a marked brazier row; inspecting its tell in the window completes that cue. A missed window is simply re-offered on the next run. |
| **Carry-state ewer** (EH-M5) | A vigil ewer filled at a cistern. While carrying it the player can move and dodge but not attack; setting it down is one interaction and it stays full. |
| **Address** | "Warden's hand" continues from Act I. Volkhari allies use "you" and nothing else; the Speaker calls the player "friend" (D-S1, ruled 2026-11-15), which is warmth, not trust. |

---
---

# Part A: EH-M4 Ash-Stained Chains (`EAC`) (D-E2, ruled 2026-11-15)

## A1. The quest in one paragraph

**Maeryn Vall** sends for the warden's hand and takes them through the curtain without a word. In her back room, by the stove, sits **Dahrin Vosk**: horns broken at the tips, scales cracked with old ritual scarring, ember-veins under his skin flickering out of rhythm. He is frightened and courageous in the same breath. He was taken below years ago, held in a frame in the ritual chambers, and escaped when a ring failed and cracked his wall; beside his frame, through the basalt, an older man spoke to him in their own tongue every night and taught him to count breaths instead of days. "You've read 'held below'. I was below." He was alive the night Dahrin ran. Dahrin gives the player a **sigil-stone** that came out in his fist ("It warms near their true doors. My hands shake too much to read it.") and teaches one mark: a ring closed with a bar, *where they keep*. He knows something more and does not say it; asked twice, he says "Not here." **Asera of the Three Breaths** comes at dusk and decides how far she will go: as far as the room the elder is in, and no further, and she will lift her hand at nobody. **Yorven Khelt** gives the warden's hand a key to the miners' gate in his old bypass ("Maeryn Vall asked me for a door. I don't ask Maeryn Vall why."), and at the foot of an abandoned shaft below it **Thennek "Stone-Quiet" Vorren** is waiting, barefoot on hot stone. He walks them down to the **Emberdeep Warrens**' mouth, puts his palm to the rock, says something below is "awake enough to be uncomfortable", and stops. Past a Deepbrand post, a **plate run** teaches the Warrens' traps: a primed plate shows a red, crazed tell like a warden's bead. In the pulsing heat rooms Asera brings the air down a band while the player keeps her count. In the **sigil gallery** the stone warms at true doors, and once at a false one where orange flarecap shows a vein behind the wall; an **Emberdeep Sentinel** walks the middle landing. Past the last door, in the **proving ring**, a warden-frame Sentinel draws strength from floor sectors that prime one after another like the hand of a slow clock. Beyond the ring, in a chamber with a fitter's anvil, **Thalan Veyr** hangs in a frame of basalt and ember shards with his horns collared, under a slate headed *Perfect Flame: trial series*. Emberlight moves along the vault above; Asera says "Don't look. He isn't here." Thalan asks what the young one did, and then asks the player to ask him. Asked to come, he agrees in his own words to leave (D-E2, ruled 2026-11-15), and says plainly that cutting him out will not quiet what burns below. The player forges a drift and drives his collar pins, or eases the collars over two cool cycles, and walks him out to Thennek, who takes him on and does not say where. The player climbs back to Maeryn's back room, gives the stone back, and tells Dahrin what the old man said.

**What the player should remember:** a voice through a wall that taught someone to count breaths; the floor priming like a clock; "Don't look. He isn't here."; an old man asking to be asked. **What the player should want next:** who the proving ring was proving, and who in daylight is breathing on someone else's count.

## A2. Selection record

| Candidate | Verdict |
|---|---|
| **A. A stealth infiltration** (disguise, guard sight-lines, alarms). | Rejected. ED-6 and CDR-4: no stealth or detection system. The Arcs' "infiltration" is built from a route (Dahrin's escape shaft reversed), a favour (Yorven's key), sigil doors, plates and fights. |
| **B. The player decides Thalan's fate.** | Rejected. Bible ED-4 and contradiction 7: Thalan speaks for himself and consents in his own voice. The player's choice is which question to ask him; his answer is his. |
| **C. A third option, ending his suffering** (dossier §XIX.3). | Rejected and never offered (Review contradiction 7; bible §13 item 4). There is no node, prop or bark that suggests it. |
| **D. A vision or the Embermind Echo shows Thalan alive.** | Rejected. R10 needs two custodians and no phenomenon (Revelation Ledger §1): Dahrin's escape account and the chamber itself. |
| **E. Dahrin's account → allies and a door → the shaft and the mouth → plates and breath rooms → the sigil gallery → the proving ring → the chamber and the slate → Thalan asked → out** (selected; the bible brief). | **Selected.** R10 is earned from a living witness and a place; Volkhari allies are people with limits, not keys; the readable system becomes traps and a clock; the liberation is a conversation with consent; the player chooses how, never whether. |

## A3. Canon grounding

| Element | Source | Status |
|---|---|---|
| Thalan Veyr: the sole known current captive; captured in the post-Hollow purges; imprisoned for decades; suspended in a frame of carved basalt with embedded ember shards; horns bound with metal collars, tail shackled; calm, dignified, soft with steel; holds to the Volkhari doctrine of restraint and distance; senses the Titan's resonance as suffering, not kinship | Character file §50; dossier §V.5, §X; Part 4 ledger | [CANON] |
| Thalan "considered vital to Project Perfect Flame"; "used for ember-blood resonance testing" | Dossier §X | [CANON]; shown only as the slate heading and a frame that feeds a ring (R10 withholds what he is made to give) |
| Dahrin Vosk: fugitive Volkhari who escaped Remnant experimentation; horns broken at the tips, scarred scales, erratic ember-veins; paranoid, courageous, hates Ashfall; emberflare reflex; brings a sigil-stone; knows the opening phrase of the Titan's binding (never spoken here) | Character file §49; bible §5.1 | [CANON] |
| Asera of the Three Breaths: breath-binding calms flares; soft-spoken, precise; feels the captive's pain as nightmares and chest pressure | Character file §46; bible §5.1 | [CANON]; her nightmares are her own, never evidence |
| Thennek "Stone-Quiet" Vorren: pathfinder; tremor-sense; barefoot on hot stone; suspects the Titan is not fully dormant | Character file §47; bible §5.1 | [CANON]; one R19 line only |
| Maeryn Vall: safehouse for Volkhari on the run; "the Volkhari are not gone" if trust is earned | Character file §48 | [CANON]; her disclosure is optional and her own `[ED-12]` |
| Kaelith Veyr'un: free, hunted, trails emberlight when distressed; feels the captive's presence | Character file §41; Part 4 ledger C05 | [CANON]; seen as emberlight only, never named, met or followed |
| The Emberdeep Warrens: abandoned mining shafts, sealed Remnant doors, heat pockets that pulse with emotion, conduits to ritual chambers; the ritual network's containment chambers and resonance rings | Dossier §VI.5, §VII.6 | [CANON] |
| Emberdeep Sentinels: Remnant-engineered constructs of embersteel and ember veins that patrol sealed chambers | Dossier §XII; bible §10 | [CANON] |
| Deepbrand oversees containment chambers in the Warrens, including Volkhari holding cells | Factions §2 | [CANON] |
| Yorven Khelt knows older tunnels that bypass Ashfall security | Character file §24 | [CANON] |
| Pressure plates as heat-pressure traps; Asera's steadying in heat rooms; Thennek to the mouth; the sigil gallery; Thalan's liberation, consented | Bible ED-4, ED-6, §6.1 | ED-4 (D-E2, ruled 2026-11-15); [PROPOSAL — DIRECTOR] ED-6 |
| Dahrin's account of the voice through the wall; the taught sigil; Yorven's miners' gate; the proving-ring sectors and warden-frame draw; the fitter's anvil; the drift; Thalan's "ask me" (D-E2, ruled 2026-11-15); Dahrin's message to Thalan | This package | [NEW] |

## A4. Quest summary card

| Field | Value |
|---|---|
| Working title | **Ash-Stained Chains** |
| Suggested content id | `emberholt.main.04_ash_stained_chains` |
| Arc position | Act II opening (Arcs §3.3, EH-M4: "Find Thalan, and treat Volkhari as people, not plot keys") |
| Prerequisite | EH-M3 Completed. Tuned for Expert identity (ED-10). |
| Offer | Journal lead from EH-M3: *Maeryn Vall has sent for you again.* Maeryn at her shop counter (`EAC-D1`). |
| Solo / co-op | Solo-clearable. Co-op partners share the mouth fight, the Sentinel and the proving ring; the account, the stone, allies, plates, breath rooms, doors, the chamber, Thalan's conversation, the frame work and the walk out are per player. |
| Target length | 50–65 minutes first time |
| Combat share | ~20% |
| Dialogue share | ~30% |
| Descent, plates, doors, smithing or waiting, escort or walk, choice | ~50% |
| Skills touched | Melee or Ranged (either; neither required); Smithing ~[GD: mid] (optional, at the chamber anvil; two cool cycles of hand work is the time-cost alternative); flarecap reading from EH-M3 reused |
| Choices | How Thalan is freed (forge or wait; `EH_THALAN = freed` is fixed, (D-E2, ruled 2026-11-15)); forge or wait (`EAC_FRAME_WORK`, flag only); Asera's breaths or the wait in each heat room (`EAC_BREATH`, flavour); press Dahrin twice (`EAC_PRESSED`, no penalty) |
| Unlocks | `EH_THALAN`; Maeryn's back room as a safehouse (respawn, keep-watch stool); the old shaft to the Warrens' mouth as a route (sealed beyond, post-quest); ECC; ETB (with EST); EH-M5 |
| **Anchor** (contract) | Volkhari individuals (Dahrin, Asera, Thennek, Thalan; Maeryn) |
| **World-truth row** (contract) | H03 (the Volkhari are not gone), H18 (the Hollow's aftermath: the purges), H22 (present hidden harm: Perfect Flame research) |
| **Revelation role** (contract) | **Owns R10** (Thalan lives, in a frame, used for Perfect Flame research). Two custodians on the main path: Dahrin's escape account (`S01`) and the containment chamber with its proving-ring slate (`S05`). Withholds what Thalan has been made to give. **Seeds R19** (Thennek's "awake enough to be uncomfortable"; Thalan's "something below burns that cannot stop"). Optional R18 seed (the slate's mark column matches the Molten Stair ledger's). Optional EH-M6 seed (a feed pipe with a city-pattern collar, its number filed off). |
| **Recurring evidence** (contract) | Three independent holds: **Dahrin's account** and the **sigil-stone** (`EAC_sigil_stone`; his custody), the **proving-ring slate** (read in place in the chamber; Deepbrand's hand), and **Thalan's own words** (protected testimony, `[ED-12]`, used only as he allows). The slate's heading recurs in EH-M6 (the junction book's *Perfect Flame: draw holds*). |
| **State compliance** (contract) | Inactive / Active / Completed. Wrong doors are dead ends, never traps; plates never reset anything; breath rooms can be waited out; the Smithing hook has a two-cool-cycle alternative; channel progress is kept. Outcome recorded in `EH_THALAN = freed` (D-E2, ruled 2026-11-15). Resume at the persisted step with a hook at Maeryn's shop (Maeryn or Dahrin), the shaft foot (Thennek, until `S05`), or the ring edge niche (Asera, `S05`–`S07`). |
| **Combat compliance** (contract) | Deepbrand Crews (human) defeated at 0 HP; Emberdeep Sentinels (constructs, including the warden-frame) destroyed at 0 HP. Plates and heat rooms are hazards, not enemies. Melee or ranged; ranged viable everywhere and never required; the warden-frame's draw on primed sectors makes both styles move. Solo-tuned. No SX. No defeated enemy gives testimony. Dahrin, Asera, Thennek, Maeryn and Thalan are never targetable and never engaged. |

## A5. The places

### A5.1 The Cinderweave Quarter: Maeryn's shop and back room [EP03] (return)

**MAP VERIFICATION REQUIRED** (as Act I). Maeryn's back room is shown only as a room `[ED-12]`; nothing in it locates anyone.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **C4. Maeryn's shop** | Offer (`S00`); safehouse respawn point and keep-watch stool from `S02`. | As EH-M2: bolts of ember-resistant cloth, the counter, the mending book. A shop bell on a spring over the door. |
| **C5. The back room** | Dahrin (`S01`); Asera (`S02`); the end (`S07`). | A cutting table, a stove, two chairs, a third chair brought in. A hood and long gloves on a peg, sized for someone who is not Maeryn. |

### A5.2 Cinderwall [EP02] and the Undercroft [EP15] (return)

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **W2. The Cooling House** | Yorven's key (`S02`). | As Act I, with the outcomes of `EH_COLD_WARD` and `EH_HOLLOW_TRUTH` in the room. |
| **U6. Yorven's bypass, Cinderwall end** [NEW sub-site of EP15] | The miners' gate (`S02`). | The far end of the old miners' bypass Yorven used in EH-M3, entered from a deep Undercroft junction. An iron **miners' gate** in its wall, padlocked, rust in the hasp. **MAP VERIFICATION REQUIRED.** |

### A5.3 The old shaft and the Emberdeep Warrens [EP13, CANON]

An abandoned mining shaft below Yorven's bypass drops to the Warrens. Dahrin came up it; the player goes down it. **MAP VERIFICATION REQUIRED** (depth, heat and every relative position below matter here): relative order from the gate: the shaft head → the shaft (ladders and landings) → the shaft foot → the Warrens' mouth → the plate run with two heat rooms → the sigil gallery (three tiers) → the ring gallery door.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **K1. The shaft head** | Thennek (`S02` end). | A square shaft with old ladders pinned to the rock, a winch frame with no rope. Chalk crew marks decades old. Thennek sitting on the lip with his feet on hot stone. |
| **K2. The shaft and the shaft foot** | Descent (`S03`); respawn point for `S03`–`S04`. | Ladders and three landings; vent breath through cracks on the second landing; flarecap in the seams. At the foot a cooling niche with a dry trough and a water cask that someone has kept full. |
| **K3. The Warrens' mouth** | Thennek stops; the R19 line; Deepbrand post (**EAC-E1**) (`S03`). | Where the old shaft breaks into a cut tunnel. Dressed stone begins, conduits run along the walls, a sealed iron door stands open on a Deepbrand **landing**: a brazier, a rack of poles, a crossbow rest on a raised step, a slate of shift names wiped clean. |
| **K4. The plate run** | Plates; two heat rooms (`S03`). | A long gallery floored in iron plates set in stone ribs, each plate with an emberglass tell in its face. Two widenings where **heat pockets** pulse through cracks (**K4a**, **K4b**), each with a blue-washed niche cut by Deepbrand for their own crews. Conduits overhead hum and are warm to the hand. |
| **K5. The sigil gallery** | Doors and the stone; the first Sentinel (**EAC-E2**) (`S04`). | Three stacked **tiers**, each a landing with **three doors** in a curved wall, each door bearing a Remnant **sigil** cut and filled with dark glass. Stairs between tiers. Dead-end passages behind false doors: a store of conduit plates (tier 1), a fitter's store with collar blanks on pegs (tier 2), a dry cistern (tier 3). Flarecap at one tier-2 jamb. |

### A5.4 The ritual chambers [EP16, CANON]

**MAP VERIFICATION REQUIRED.** Relative order: the ring gallery door → the proving ring and its gallery → the chamber door → the chamber → the vault above (seen, not reached).

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **R1. The proving ring** | The set piece (**EAC-E3**) (`S05`). | A round sunken floor, eight wedge **sectors** of iron plate round a central disc, each sector with a large tell at its outer edge. Around the rim, eight **stations** marked in the stone with a shallow footprint pair and a small mark (ring, ring with a dot, filled ring). Conduits run from under the floor to a wall where the **chamber door** stands with the closed-ring-and-bar sigil. A raised **gallery** on one side with a stair and a crossbow rest. A blue-washed **edge niche** at the ring's entrance: Asera's place. |
| **R2. The chamber** | Thalan (`S05`–`S06`); the slate; the anvil. | A tall round room. At its centre a **frame** of carved basalt posts with ember shards set in them, conduits running from its foot through the wall toward the ring. In it **Thalan Veyr**, upright, held at the horns by metal collars on short chains to the posts, his tail shackled to the base. The frame's draw breathes on a slow cycle (~40 s: a hum and a rising glow for ~25 s, then a cool phase of ~15 s). On the wall, the **proving-ring slate** in a wooden frame. Along one side a **fitter's hearth**, an **anvil**, a quench trough and a rack of embersteel bar and tools: the place where collars are fitted. A **feed pipe** comes down through the roof into the frame's base (optional inspect). A blue niche by the door. |
| **R3. The vault above** | The emberlight (`S05`). | The chamber's roof is open in a ragged ring to a higher gallery in the dark. Nothing can be climbed. |

## A6. Player-facing sequence

### Beat 0: Maeryn (`S00_offer`)
**Objective:** *See Maeryn Vall at her shop.*
Maeryn is at her counter, bright and too quick (`EAC-D1`). "Back room. Somebody's waiting who doesn't wait well." With `EGH_STONE_HEARD` (always set by EH-M3): "You've been through that curtain once. You kept the terms. That's why he asked for you."
- **Accept:** the quest becomes **Active**; Maeryn lifts the curtain.
- **Not now:** "He's waited years. He can wait for you to finish your soup." Re-offered at the counter (`EAC-D1.90`).
**Verbs:** listen, accept.

### Beat 1: Dahrin (`S01_dahrin`)
**Objective:** *Hear Dahrin Vosk.*
**Dahrin Vosk** is by the stove (`EAC-D2`). When the shop bell rings behind the curtain, the stove flame stands up tall and his hands spread on his knees (**heat follows the room**: his emberflare reflex as a presentation beat only; nothing burns); Maeryn says "Bread man, Dahrin. Breathe," and the flame comes down.
He tells what happened to him and nothing more (`EAC-D2.20`–`.28`): taken below years ago, held in a frame in the ritual chambers past the Warrens; a wall of basalt between his frame and an older one; the older man spoke to him through it in their own tongue every night and taught him to count breaths so he would not count days; one night a ring failed, the heat cracked his wall, and he ran with whatever was in his fist, up an old shaft that "comes out under your Overseer's ward". **The elder was alive the night he ran.** "That's all I have a right to say: he was alive then." This is R10's first custodian.
- **With `EGH_SHEET_READ`** (always set by EH-M3): "You've read 'held below'. I was below." (`EAC-D2.10`, the line Act I promised).
- **Variant by `EH_HOLLOW_TRUTH`** (`EAC-D2.12`/`.13`): `told`: he went and looked at the chalked plaque at night and put his hand on it; `kept`: he would like to be a line in the Marshal's second ledger one day, "not yet".
- **The stone** (`EAC-D2.40`): he puts the **sigil-stone** in the player's hand (**`EAC_sigil_stone`**, quest item). "It warms near their true doors. My hands shake too much to read it."
- **The mark** (`EAC-D2.45`, required): he draws it in the stove ash: a ring closed with a bar. "Where they keep." Sets `EAC_SIGIL_TAUGHT`.
- **Pressing** (optional): "What else do you know?" Dahrin: "Enough to be hunted." Asked again (`EAC-D2.32`): he looks at the curtain, then the player. **"Not here."** Sets `EAC_PRESSED`. No penalty; the conversation goes on; there is no third ask.
- **His message** (`EAC-D2.50`): "If he's there, tell him the young one lived. He'll know which."
Sets `EAC_DAHRIN_HEARD` at the end. The step completes.
**Verbs:** listen, hold, learn a mark.

### Beat 2: Allies (`S02_allies`)
**Objective:** *Find a way down.* (Sub-objectives in any order; Thennek last.)

| Sub-objective | Where | What the player does | Sets |
|---|---|---|---|
| **Asera** | The back room (C5), at dusk | If it is not dusk, keep watch on Maeryn's stool (one turn). **Asera of the Three Breaths** comes in from the yard door (`EAC-D3`). She decides how far she goes, out loud: "As far as the room he's in. Not into their ring. I won't lift my hand at anyone. If that's not enough, go without me." She shows what she does: she breathes with Dahrin, three breaths, and the stove flame steadies (presentation). "In a hot room, stand by me and breathe when I breathe. The room will come down." Of the elder: "I've felt that room in my chest for years. That's mine. It isn't proof of anything." | `EAC_ASERA` |
| **A door** | The Cooling House (W2) | **Yorven Khelt** (`EAC-D4`) takes a key off his ring. "Maeryn Vall asked me for a door. I don't ask Maeryn Vall why." The miners' gate at the Cinderwall end of his bypass; behind it an old shaft "goes down further than I ever went". He marks it on the player's map. **Carry-state: the gate key.** | `EAC_GATE_KEY` |
| **The safehouse** | Maeryn's shop | As the player comes out through the curtain after Dahrin (start of `S02`), Maeryn: "If anyone asks, you're being fitted." From now on the shop is a respawn point with a keep-watch stool, so a player who needs dusk for Asera can always wait for it here. | — |
| **Thennek** (after the other two) | The miners' gate (U6) and the shaft head (K1) | The player unlocks the **miners' gate** (one interaction; it takes the key only when `EAC_ASERA` and `EAC_GATE_KEY` are both set; before that its inspect is `EAC-I1` and the journal reads *Asera comes at dusk.*). At the shaft head **Thennek "Stone-Quiet" Vorren** is sitting on the lip with his feet on hot stone (`EAC-D5`). He says very little: "I'll walk you to their mouth. Not past it." He does not say how he got there. | `EAC_THENNEK_MET` |

The step completes on `EAC-D5` end. Asera is at the shaft head with Thennek when the player arrives (she came her own way; nobody explains it).
**Verbs:** wait, ask, borrow, unlock.

### Beat 3: The Warrens (`S03_warrens`) `[ED-6]`
**Objective:** *Reach the sigil gallery.*
1. **The shaft (K2).** Down ladders and landings. Thennek goes first and never looks down. The second landing's cracks breathe (vent breath, ~10 s). Flarecap in the seams: with `EGH_FLARECAP`, Thennek watches the player step round an orange cap and nods once (`EAC-B3.2`). At the foot, the niche and a full water cask.
2. **The mouth (K3).** At the shaft's end Thennek stops, crouches, and lays his palm flat on the rock for a long moment (`EAC-D6`). "Something under all of this is awake. Awake enough to be uncomfortable." He says nothing more about it, here or anywhere in Emberholt (R19 seed; sets `EAC_THENNEK_HEARD`). "Here's their mouth. I'll be at the foot when you come back up." He goes back to the niche. Past the mouth is a **Deepbrand landing** (**EAC-E1**). The crossbow calls from the raised step (`EAC-B3.4`: "Sealed works."); the post fights to 0 HP. Asera waits in the shaft-foot niche until it is over; one sober line after (`EAC-B3.6`).
3. **The plate run (K4).** Asera stops at the first plate (`EAC-D7.01`): "Red and cracked. Like your wardens' beads." The player **inspects a plate** (required once; `EAC-I3`; sets `EAC_PLATE_READ`). The run is a gallery of plates on stone ribs: the ribs are always safe; stretches where the plates run wall to wall must be crossed on clear plates between vents (§Act II conventions). A primed plate stepped on vents and knocks back; nothing else happens.
4. **The heat rooms (K4a, K4b).** Each pocket is pinned **Surging** on arrival (the fight at the mouth woke it: heat follows the room). Two ways, per room, both valid:
   - **Asera's three breaths:** stand in the niche beside her and keep her count (3-segment channel; §conventions). The room drops to **Working** and stays there.
   - **Wait:** keep watch in the niche (one turn). The room drops to Working.
   `EAC_BREATH` = asera / waited (flavour; set by the first room; Asera's bark varies, `EAC-B4.3`).
The step completes on reaching the sigil gallery's first landing (K5, tier 1).
**Verbs:** climb, read, fight, step round, wait, breathe on a count.

### Beat 4: The Sigil Gallery (`S04_sigils`)
**Objective:** *Find the way by the stone.*
Three tiers, three doors each. Holding the stone near a door makes its seam glow; its inspect reads *cold*, *cool* or *warm*. A wrong door opens on a **short dead end** and the stone goes cold inside; the player walks back. Nothing resets; nothing locks; no fight waits behind a wrong door.
- **Tier 1 (teaching).** One door warm. The true door. (Dead ends: a store of conduit plates; `EAC-I5`.)
- **Tier 2 (the vein).** An **Emberdeep Sentinel** (**EAC-E2**) walks the landing; it engages on sight and is destroyed at 0 HP. Two doors read *warm*. At the jamb of one, bright **orange flarecap** grows in the seam (`EAC-I6`). The warmth there is a live vein behind the wall, not a door. The other warm door, with pale cap, is true. (With `EGH_FLARECAP`, Asera: "Your miner's cap. Look at it before you look at the stone." `EAC-B5.3`. Without it the cap's inspect still says orange cap means a live vein close by.) The orange door's passage is a fitter's store with collar blanks on pegs (`EAC-I7`), and the stone is cool inside it.
- **Tier 3 (the mark).** Two doors read *warm* and neither has cap. One bears the mark Dahrin drew in the ash: a ring closed with a bar (`EAC-I8`). The true door. (The other is warm from a hot conduit behind it and opens on a dry cistern; the stone is cool inside.)
The step completes on passing the tier-3 true door into the ring gallery.
**Verbs:** hold, read, compare, fight, choose a door.

### Beat 5: The Chamber (`S05_chamber`): *the set piece and R10*
**Objective:** *Reach the elder.*
1. **The proving ring (R1).** Asera stops at the edge niche (`EAC-D7.20`): "That ring is fed from his frame. I won't step on it." On the floor: a **warden-frame Sentinel** and two **Deepbrand guards**; on the gallery, a **crossbow** (**EAC-E3**; §A7). The eight sectors **prime in turn** clockwise like the hand of a slow clock: each sector's tell goes amber (~2 s), then red and crazed (~6 s), vents (a sheet of heat across the sector), then clear; the next sector begins its amber as the last turns red. **The warden-frame draws** from whatever primed sector it stands on: its seams glow and it shrugs off most damage while it does. Bait it onto clear sectors, or wait for the hand to pass it. The rim stations are safe ground. Every enemy fights to 0 HP. When the ring is clear the sectors keep turning (they are fed from the frame); the rim is safe and the chamber door is on the rim.
2. **The door.** Hold the stone to the chamber door: *warm* (`EAC-I9`). The bar lifts (one interaction). Asera comes in behind the player.
3. **The chamber (R2).** **Thalan Veyr** in the frame (§A8.1). The player **approaches the frame** (required; sets `EAC_THALAN_SEEN`: R10's second custodian is the place itself, with him in it). The presentation is plain and still: an upright man in a basalt frame, collars at the horns, a shackle at the tail, his eyes open. The frame's slow draw glows and fades; his breath tightens on the glow and eases in the cool.
4. **The emberlight** (§A8.2). As the player reaches the frame, faint emberlight moves along the rim of the vault above, from one side to the other, and is gone. Asera, without looking up: "Don't look. He isn't here." Thalan closes his eyes until it has passed. Sets `EAC_EMBERLIGHT_SEEN`. Nobody explains it.
5. **The slate** (required; document `EAC-I10` in the dialogue file). Headed ***Perfect Flame: trial series.*** Columns: trial, ring, hands at the stations (by mark only), "frame carried" (yes / no), "held to the mark" (a tally of how many stations held). The early trials mostly read *frame carried: no*. The recent ones read *yes*. It says nothing about what the frame takes from the man in it. Sets `EAC_SLATE_READ`.
   - *Optional, with `EEH_LEDGER_READ`:* the marks in the hands column are the rings, dotted rings and filled rings of the Molten Stair ledger's second column (`EAC-I11`). Nothing says more. Sets `EAC_MARKS_MATCHED` (R18 seed; never explained).
   - *Optional:* the **feed pipe** into the frame's base wears a city-pattern valve collar with its number filed off (`EAC-I12`; EH-M6 seed; never explained).
The step completes when the ring is clear, the chamber is entered, Thalan is seen and the slate is read.
**Verbs:** fight, bait, read the clock, open, see, read.

### Beat 6: Thalan (`S06_thalan`): *the liberation* (D-E2, ruled 2026-11-15) from `EAC-D8.60`
**Objective:** *Speak with Thalan.*
**Common part.** Thalan speaks first (`EAC-D8.01`): the ring went quiet, so someone came through it. He knows Asera is there before she speaks, and they exchange a few words in their own tongue that are not translated (`EAC-D8.10`; Asera: "That was between us."). He asks one thing before anything else: did the young one live. The player gives **Dahrin's message** (`EAC-D8.20`, required): "The young one lived. He said you'd know which." Thalan: "I know which." (sets `EAC_MESSAGE_GIVEN`). Optional asks, each answered and then closed:
- *What they take from him* (`EAC-D8.30`): "That is mine." (R10 withholds it; there is no second ask.)
- *How long* (`EAC-D8.32`): "I counted breaths. I stopped counting days. He told you that." (No number.)
- *What is below* (`EAC-D8.34`; R19 seed): "Under this floor, far down, something burns that cannot stop burning. It is in pain. I have listened to it longer than I have listened to anything." Nothing more: no name, no shape, no binding.
- *Who put him here:* "People who write things down." (He names no one.)

**The ask** (D-E2, ruled 2026-11-15) (`EAC-D8.60`–`.62`). Asera lays it out, plainly: "We can cut you out, and Thennek takes you on. You decide. They ask." Thalan, to the player: "I have wanted that every night for a long time. Ask me." The player asks: **"Come with us. Thennek is waiting."** Thalan consents to leaving in his own voiced words and gives his own reason (`EAC-D8.62`): "If the frame is empty, they will look for someone to fill it. Let them look. Let them look a long time. Yes. I will leave this place. Cut me out." Then: cutting him out will not quiet what burns under the floor. Sets `EH_THALAN = freed`. Liberation is the only outcome; there is no option to leave him in the frame, harm him or use him. His leaving does not end the works, the Remnant's operation or the suffering below, and no line says it does.

**The work.** The chamber's own **fitter's hearth and anvil**. The player chooses the approach; both free him.

| Approach | What the player does |
|---|---|
| **Option A (skill): Smithing ~[GD: mid]** | **Forge a drift** from a bar in the fitter's rack: **heat** it until the hearth's tell shows amber (one interaction, ~4 s); **shape** a tapered punch on the anvil horn (2-segment channel, ~3 s each); **quench** it in the trough (one interaction). Then **drive the collar pins** at the frame (3-segment channel, ~4 s each); Asera holds Thalan's breath steady through it (`EAC-D9.10`). |
| **Option B (time-cost): two cool cycles** | Wait for the frame's **cool phase** (~15 s in each ~40 s cycle); in each of **two** cool phases, **ease the collars** by hand (a 3-segment channel that runs only in the cool phase and pauses, progress kept, when the glow returns). |
| **Result** | The collars open. The tail shackle is keyed, not riveted; Asera turns the key off its hook on the post. Thalan steps out of the frame on his own and stands, slowly, with one hand on a post (`EAC-D9.20`). The frame's glow goes on without him for one cycle and then gutters; in the ring outside, the sectors go dark one by one. |
| **Flag** | `EAC_FRAME_WORK` = self / wait |

Nothing in the work can fail. A channel in the chamber is interrupted only by the player moving off it; there are no enemies left in the chamber. The step completes on `EAC-D9.24`.
**Verbs:** listen, ask, forge, drive, or wait.

### Beat 7: Out (`S07_out`)
**Objective:** *Go back up to Maeryn's.*
The way out crosses the same ground in the same order: the ring (dark: with nothing drawn from the frame, the sectors stop), the sigil gallery (doors stay open behind the player), the plate run (plates still cycling; heat rooms stay Working), the mouth, the shaft foot, the shaft, Yorven's gate. No enemies spawn on the way out; everything defeated stays defeated.
Thalan walks with the player (**escort-follow**, slow; never targetable, never harmed by plates or heat). He stops at each heat room and Asera breathes with him (presentation). At the **shaft foot**, Thennek stands up from the niche. He and Thalan look at each other for a long time and do not speak (`EAC-D9.40`). Then Thennek says to the player: "You don't need to know where." He takes Thalan into a side cut the player has not seen used, and they are gone. The player is never told where (`EAC-D9.42`; D-C06: Thalan's destination stays unplaced).
Then up the shaft; at the top Asera goes her own way ("I'll come to Maeryn's when I come."); the player goes to Maeryn's back room. **Dahrin** is by the stove (`EAC-D11`). The player tells him (summary line). His answer (`EAC-D11.10`–`.11`) and `EAC_PRESSED` (`EAC-D11.20`) follow. The player gives the **stone** back (`EAC-D11.30`; item removed). **Maeryn**, at the curtain, may say one thing she has never said to the player (`EAC-D11.35`, optional, her own choice, `[ED-12]`; it plays if the player stays ~5 s after `EAC-D11.31` before speaking to Dahrin again): "We're not gone, you know. Whatever people say." Sets `EAC_MAERYN_SAID` if heard. **Completes** on Dahrin's last line (`EAC-D11.40`). Maeryn's hood (`EAC-D11.36`) is given at the counter as the player leaves.
**Verbs:** walk, escort, return, tell.

**Epilogue (no step).** Post-quest, Yorven's gate and the old shaft to the Warrens' mouth stay walkable (the player keeps the gate key); past the mouth a new Deepbrand **barricade** (non-interactive prop) closes the Warrens. A second hood and pair of gloves hang on Maeryn's peg and are gone the next day.

## A7. Encounters

Tuned for **Expert identity** (ED-10). Exact levels are Gameplay Designer calls. Emberdeep Sentinels are constructs: destroyed at 0 HP, they seize, cool and stay down. Deepbrand Crews take the ordinary defeat presentation.

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **EAC-E1** | 2 × Deepbrand Crew **guard**, 1 × **crossbow** | The Deepbrand landing at the Warrens' mouth (K3); the crossbow on a raised step reached by three stairs | Guards hold the landing with hooked poles and shields; the crossbow covers the shaft mouth | **Guard, Hook:** draws the pole back to the hip (~1.5 s), then a hooking sweep that pulls the player one step toward him. **Guard, Shield bash:** feet set, shield up (~1.5 s), then a bash with a short stagger. **Crossbow, Aimed shot:** red glint on the bolt-tip, steadied stance (~1.5 s), then a heavy bolt (sidestep or break line of sight behind the brazier). **Crossbow, Reload:** ~3 s visible reload (the window to close). | The quest's first fight and the reason the heat rooms are up (heat follows the room) | 70–100 s; 55–75% HP |
| **EAC-E2** | 1 × Emberdeep **Sentinel** (the first in Emberholt) | The sigil gallery, tier 2 landing (K5), on a fixed patrol between the three doors | Patrols; engages on sight; keeps to the landing | **Sweep:** draws one arm back, ember seams brightening down it (~1.2 s), then a wide horizontal sweep (duck behind a door jamb or step out). **Vent:** chest plates part, glow inside (~1.5 s), then a short cone of heat ahead. **Lock-step:** its eye-slit brightens and it plants (~1.5 s), then a straight charge to the point it was facing and a skid stop (sidestep). | Introduces the construct family on its own, one telegraph at a time | 60–90 s; 60–80% HP |
| **EAC-E3** | 1 × Emberdeep **warden-frame** (heavier Sentinel variant; the ring's keeper), 2 × Deepbrand **guard**, 1 × Deepbrand **crossbow** on the gallery | The proving ring (R1) and its gallery | Warden-frame holds the floor and moves toward primed sectors; if its target stands off the sunken floor (rim or gallery) it follows by the ring's ramps and the gallery access and has no Draw off the sectors, so neither is a safe firing spot; guards press the player toward the turning hand; crossbow covers the rim | **The hand (the floor):** each sector amber (~2 s) → red-crazed (~6 s) → vent (a sheet of heat across that sector, damage and knock-back toward the rim) → clear; one sector at a time clockwise, the next starting amber as the last turns red, so about two sectors are hot at once. **Warden-frame, Draw (the condition):** while it stands on a red sector its seams glow white and it takes heavily reduced damage; on a clear or amber sector it takes full damage. **Warden-frame, Stride:** crouches, seams flicking toward the nearest red sector (~1.0 s), then strides to it (the tell shows where it wants to go: get there first, or let it go and wait for the hand to pass). **Warden-frame, Clamp:** both arms open wide (~1.2 s), then a two-armed clamp in front (step back or out to the side). **Warden-frame, Brand:** plants a foot, the sector under it flares amber early (~1.5 s), then vents early (leave that sector). **Guards and crossbow:** as EAC-E1. | The set piece: fight a construct on a floor that keeps time; read the hand, bait the frame onto cold iron, use the rim | 3–4 min; 40–60% HP |

**Hazards (not encounters):**
- **Pressure plates** (K4; K5 landings have none): primed red-crazed, spent clear, re-priming amber (§Act II conventions).
- **Heat rooms** (K4a, K4b): Surging on arrival; Working after Asera's breaths or a wait.
- **Shaft vents** (K2): timed exhale, ash lift ~1.5 s.
- **Flarecap seams** (K2, K5): orange cap = live vein; striking or bracing there bursts (moderate damage, knock-back).
- **The ring's sectors** after the fight: they keep turning until the frame stops drawing; the rim is always safe.
- **The frame's draw** (R2): presentation only. It does not harm the player.

**Rules**
- **Defeat at 0 HP** (CDR-1). Guards and crossbowmen take the ordinary defeat presentation. Sentinels seize and cool (destroyed). No enemy flees, yields or breaks off.
- **The warden-frame's draw is a place rule** (like a resonance condition): it depends on the sector under it, never on its health. It never heals and never re-forms.
- **Melee or ranged** (CDR-2): every fight accepts both. At the mouth the crossbow can be duelled or reached by the stair. In the ring, ranged players can hit the warden-frame from the rim when it stands on clear iron, and must move round the rim to keep a line as the hand turns; melee players work it on clear sectors and step out of the hand. Ranged never ends the ring faster than reading the floor does. Ranged is never required.
- **Combat never reveals evidence.** Dahrin's account is his; the slate is read on a wall; Thalan speaks for himself. Guards carry ordinary loot and no paper; Sentinels drop nothing.
- **Non-combatants:** Dahrin, Maeryn, Asera, Thennek, Yorven and Thalan are never targetable and never engaged. Asera waits in a niche during every fight and is never in an enemy's path; Thennek is never in a fight.
- **Death:** respawn at Maeryn's shop during `S00`–`S02`; at the shaft foot (K2) during `S03`–`S04`; at the ring's edge niche (R1) during `S05`–`S07` until the player climbs back past the shaft foot; at Maeryn's shop after that. Defeated guards and the tier-2 Sentinel stay defeated. In the ring: defeated guards and crossbowman stay defeated; the warden-frame resets to full (ordinary leash reset) if the player dies. Heat-room states, opened doors, the read slate and channel progress are kept.
- **Co-op:** every fight shared; a defeat credits each partner whose own active step consumes it (CDR-6). Each partner's stone, doors, heat rooms, chamber, Thalan conversation, frame work and walk out are their own. Plates and ring sectors are per-player hazard states; any shared floor presentation is a presentation fallback only (bible §9; MI-CO-06 pattern) and never decides a partner's step or credit. During EAC-E3 the shared warden-frame reads one sector cycle: which partner's cycle drives it when partners' floors differ is a presentation question for Sol (Act I Q-18 pattern), and solo play is unaffected. Thalan's scene is per player: a partner whose own step is not `S06` waits at the chamber door (as Seredh's scene in EH-M3); a partner on their own `S06` plays their own scene in their own phase and never waits on the other; each player's Thalan answers only that player's ask.

## A8. The discovery moments: presentation specs

### A8.1 The frame (Beat 5)

| Time | Element | Spec |
|---|---|---|
| 0 s | **The door** | The bar lifts; the door swings in on a tall round room lit by the frame's glow and nothing else. |
| ~1 s | **The frame** | Basalt posts, ember shards set in them like teeth, conduits from the base. Upright in it, a man held at the horns by collars on short chains, tail shackled at the foot. He is not hanging; he is standing, because he has learned to. |
| ~3 s | **The draw** | The shards brighten in a slow wave toward the base and the hum rises; his jaw sets and his breath goes short. Then the cool phase: the glow sinks, the hum drops, he breathes out. |
| ~6 s | **His eyes** | He looks at the player. He does not look surprised. |
| Always | **Dignity** | No wounds shown, no blood, no restraint close-ups. Scales dulled and ashen (canon), collars, shackle, the frame. The camera stays with the player. |
| Never | **Explanation** | No UI, no caption, no prompt over him. What the frame takes from him is never shown or said (R10 withheld). |

### A8.2 The emberlight (Beat 5)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Trigger** | The player enters the frame's interaction volume for the first time. |
| ~0.5 s | **The light** | A faint ember-coloured light moves along the rim of the open vault above, left to right, the height of a small person, not fast. It trails a little behind itself, like a lamp carried by someone walking. ~4 s. No sound. |
| ~1 s | **Asera** | Without looking up: "Don't look. He isn't here." (`EAC-D7.30`) |
| ~1 s | **Thalan** | Closes his eyes until it has gone. |
| ~4.5 s | **Gone** | The rim is dark. |
| After | **Nothing** | No option about it. Asked later, Asera: "I said what I said." Thalan: silence. Dahrin (if told): "Then you saw nothing. Say you saw nothing." |
| Never | **Identification** | Nobody names who it was. It is never followed, never reachable, never evidence. Kaelith is never met, rescued, followed or chosen (bible §5.1; Part 4 ledger C05). |

### A8.3 The sigil gallery (Beat 4)

| Element | Spec |
|---|---|
| **The stone** | Held in the player's hand (held-item pose when inspected). Near a Remnant door its emberglass seam glows faintly; inspect gives *cold* (no door near), *cool* (a false door), *warm* (a true door, or heat close behind the wall: a live vein or a hot conduit). |
| **Tier 1** | Teaches the reading: one door warm. |
| **Tier 2** | Teaches doubt: two warm; flarecap at one jamb. The Sentinel's patrol passes between them. |
| **Tier 3** | Teaches memory: two warm, no cap; one bears Dahrin's mark. |
| **Wrong door** | A short passage (10–20 paces) to a dead end with something to look at (conduit plates; collar blanks on pegs; a dry cistern). The stone goes cold. No trap, no fight, no reset. |
| **Never** | The stone never points, never shows a path, never glows brighter "the right way". The sigils are never translated beyond Dahrin's one mark. |

## A9. Quest structure for implementation

### A9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_offer` | See Maeryn Vall at her shop. | `EAC-D1` end with accept | Yes | Requires EH-M3 Completed. Re-offer `EAC-D1.90` |
| `S01_dahrin` | Hear Dahrin Vosk. | `EAC_DAHRIN_HEARD` + item gained (`EAC-D2.40`) + `EAC_SIGIL_TAUGHT` | Yes | `EAC_PRESSED` optional (second ask, `EAC-D2.32`). Stove flare presentation (`cinderweave.stove_flare`) on the bell |
| `S02_allies` | Find a way down. | `EAC_ASERA` + `EAC_GATE_KEY` + gate unlocked + `EAC_THENNEK_MET` | Yes | Asera at dusk (keep watch if needed). Maeryn's shop becomes a respawn point and keep-watch stool |
| `S03_warrens` | Reach the sigil gallery. | EAC-E1 defeated + plate inspect + both heat rooms Working + enter K5 tier 1 | Yes | Sets `EAC_THENNEK_HEARD` (`EAC-D6.05`, on the path), `EAC_PLATE_READ`, `EAC_BREATH`. K4a/K4b pinned Surging until breaths or a wait |
| `S04_sigils` | Find the way by the stone. | EAC-E2 defeated + pass the tier-3 true door | Yes | Stone states per door. Wrong doors are dead ends |
| `S05_chamber` | Reach the elder. | EAC-E3 all defeated + chamber door opened + `EAC_THALAN_SEEN` + `EAC_SLATE_READ` | Yes | **R10 guaranteed path.** Emberlight event (`warrens.emberlight`) sets `EAC_EMBERLIGHT_SEEN`. `EAC_MARKS_MATCHED` optional (needs `EEH_LEDGER_READ`); feed pipe inspect optional |
| `S06_thalan` | Speak with Thalan. | `EAC_MESSAGE_GIVEN` + Thalan's consent (`EAC-D8.62`) + frame work complete (`EAC-D9.24`) | Yes | (D-E2, ruled 2026-11-15) from `EAC-D8.60`. Sets **`EH_THALAN = freed`**, `EAC_FRAME_WORK` |
| `S07_out` | Go back up to Maeryn's. | Shaft foot scene (`EAC-D9.42`) + `EAC-D11.40` end | Yes | Escort-follow (Thalan). Item `EAC_sigil_stone` removed at `EAC-D11.30`. `EAC_MAERYN_SAID` optional. Quest → **Completed** |

### A9.2 Flags

| Flag | Set by | Read by (here) | Read by (later packages) |
|---|---|---|---|
| `EAC_DAHRIN_HEARD` | `EAC-D2` end | `S01` | — |
| `EAC_PRESSED` | `EAC-D2.32` (optional) | `EAC-D11.20` | **CV-M4** (request: Dahrin's opening phrase; "You asked me twice once. Here.") |
| `EAC_SIGIL_TAUGHT` | `EAC-D2.45` | Tier-3 door inspect (`EAC-I8`) | — |
| `EAC_ASERA` | `EAC-D3` end | `S02` | — |
| `EAC_GATE_KEY` | `EAC-D4.06` | Miners' gate interaction | — |
| `EAC_THENNEK_MET` | `EAC-D5` end | `S02` | — |
| `EAC_THENNEK_HEARD` | `EAC-D6.05` | — | **CV-M4** (R19 seed; request) |
| `EAC_PLATE_READ` | Plate inspect (`EAC-I3`) | `S03` | EH-M6 (Veska: "Plates? Down there? Then you know what red means under your feet.") |
| `EAC_BREATH` = asera / waited | First heat room | `EAC-B4.3` | ETB (Asera: "You kept my count once.") with `asera` |
| `EAC_THALAN_SEEN` | Frame volume (`S05`) | `S05`, `S06` | R10 guaranteed path (with `EAC_DAHRIN_HEARD`) |
| `EAC_EMBERLIGHT_SEEN` | `warrens.emberlight` event | — | None (deliberately) |
| `EAC_SLATE_READ` | Slate read (`EAC-I10`) | `S05` | **EH-M6** (the junction book's *Perfect Flame: draw holds*: "You've read this heading before.") |
| `EAC_MARKS_MATCHED` | `EAC-I11` (optional; needs `EEH_LEDGER_READ`) | — | **CV-M4** (R18; request) |
| `EAC_MESSAGE_GIVEN` | `EAC-D8.20` | `EAC-D11.10` | — |
| `EH_THALAN` = freed (D-E2, ruled 2026-11-15) | `S06` (`EAC-D8.62`) | `S07`; `EAC-D9`; `EAC-D11`; `EAC-B9` | EH-M6 tally board (§9.3 item 5); ETB (Asera's lines); CV-M4 (testimony note) |
| `EAC_FRAME_WORK` = self / wait | `S06` frame work | `EAC-D9.22` | — |
| `EAC_MAERYN_SAID` `[ED-12]` | `EAC-D11.35` (optional) | — | EST/ETB (Maeryn: "I told you once. I don't say it twice in a week.") |

### A9.3 Outcome: Thalan freed (D-E2, ruled 2026-11-15)

One outcome; the player chooses only the approach (Smithing drift or two cool cycles).

| Outcome | Immediate result | Cost | Later |
|---|---|---|---|
| **Freed** (`EH_THALAN = freed`) | Thalan, consenting, is cut out of the frame and walks out; Thennek takes him on at the shaft foot to a place the player is not told. The frame and the ring go dark. | The frame is empty and Deepbrand will look for someone to fill it (his words); Thalan's account goes with him, not up to the city; Asera carries nothing. | EH-M6: Thennek sends word, one line. ETB: Asera speaks of him as someone who walked. CV-M4: Thalan survives to give testimony at the rest-binding, reached through Thennek (where he lives stays unplaced, D-C06). His freedom does not end the works below or the suffering he hears. |

**Neither is presented as right.** Both are Thalan's consent to a question the player asked, both stop the frame working him, both darken the ring, both return the stone, and both keep what he has been made to give withheld. There is no third option.

## A10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| Plate reading | Knowledge | Primed plates read like tells. No region flag (`EAC_PLATE_READ` local). |
| Maeryn's back room | Access | A safehouse: respawn point and keep-watch stool in the shop; Maeryn's quiet welcome (barks). |
| A lined duct hood | Tool (named functionally) | Maeryn gives a hood lined with ember-thread at `EAC-D11.36` ("You'll be in ducts again. Everybody is."). Heat gear in the *Soot and Hide* family: recommended, never required. Item pass defines it (ED-11). |
| The old shaft | Access | Yorven's gate to the Warrens' mouth stays walkable; the Warrens are barricaded beyond. |
| Skill XP | Action only [GD] | Melee or Ranged at defeat; Smithing if done personally. No lump quest XP (bible §11.6). |
| Payment | None | No Volkhari pays the warden's hand. Yorven, asked, says the Cooling House owes them soup. |
| Side-quest unlocks | Story | ECC; ETB (with EST) |
| EH-M5 | Story | Journal lead on completion: *The Ember-Priestess has asked for the warden's hand at the Covenant lamp-house.* |

## A11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player steps on a primed plate | Heat column, damage and a step of knock-back. Nothing resets; no alarm. |
| Player will not wait or breathe in a heat room | The room stays Surging (heavy periodic damage). It can be run; the player may die and respawn at the shaft foot. A wait or Asera's count always turns it. |
| Player opens a wrong door | A dead end; the stone goes cold; walk back. |
| Player has not done EH-M3's flarecap lesson | Impossible on the main path (`EGH_FLARECAP` is required in EH-M3); the cap's own inspect text still states the rule. |
| Player is beaten in the ring | Respawn at the edge niche. Defeated guards stay defeated; the warden-frame resets to full; the hand keeps turning. |
| Player cannot or will not smith | Two cool cycles of hand work (Option B). Never blocked. |
| Player tries to leave the chamber mid-work | Allowed. Channel progress and the drift are kept; Asera stays with Thalan; resume at the edge niche. |
| Player tries to harm Thalan, Asera or anyone | Not possible: none is targetable; no option exists. |
| Death | Respawn by step (§A7). The stone, the key, doors, heat rooms, the slate reading and channel progress persist. During `S07`, Thalan rejoins the player at the respawn point and escort-follow resumes. |
| Logout | Restore to the persisted step: Maeryn's shop (`S00`–`S02`, `S07` after the climb), the shaft foot (`S03`–`S04`), the ring's edge niche (`S05`–`S07` before the climb). A player who logs out during the walk resumes at the edge niche with Thalan beside them. |
| Walking away | Quest stays Active. Resume hooks: Maeryn ("He's still by my stove. He's eating, which is new."), Dahrin ("I'm here. I'm always here now."), Thennek at the shaft foot ("Still here."), Asera at the edge niche ("I said as far as his room. I'm still saying it."). |
| Fail state | None. |
| Co-op | Shared fights. Per-player stone, allies' scenes, doors, heat rooms, plates, chamber, Thalan's conversation, frame work, walk out and Dahrin's scene. Presentation follows each player's own state (CDR-6). Each partner sees their own Thalan; no partner's approach moves another's. |

## A12. Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| **Pressure plates** | Gameplay | Standard timed trap: a floor volume with three states (primed / spent / re-priming) on a fixed cycle; stepping in while primed fires a heat column after ~0.6 s (damage, knock-back); a tell prop in the plate face swaps with state. Per player. |
| **Quest-pinned heat states** | Systems | K2 vents Working; K4a/K4b Surging on arrival, swapped to Working by Asera's channel or keep watch; R2 Working. EI-HT-01 fallback form; no schedule needed. |
| **Asera's three breaths** | Systems | The EH-M2 synced channel (3 segments ending on an NPC bark cadence) in a niche volume; completion swaps the room's state. |
| **Sigil-stone states** | Systems / Art | Trigger volumes at each K5 door and at the chamber door set a quest-local state (cold / cool / warm) that the held item's inspect text and seam glow read. **Possible new need:** if a held item cannot read a world volume, the **fallback** is an inspect on each door that reads "The stone in your hand is warm / cool / cold"; the puzzle is unchanged. |
| **Proving-ring sectors** | Gameplay | Eight timed floor hazards on a rotating sequence (the plate pattern on a ring). Standard timed hazards in sequence. |
| **Warden-frame draw** | Gameplay | A damage-reduction buff applied while the creature stands in a "primed" volume; a stride behaviour toward the nearest primed volume with a ~1.0 s tell. Standard zone-applied buff and target-point move. |
| **The frame's slow cycle** | Art / Systems | A ~40 s presentation loop (glow, hum) with a cool-phase flag that Option B's channels read (channel runs only while the flag is set; pauses, progress kept). |
| **Smithing at a hearth and anvil** | Skills | Existing heat, shape, quench; the drift is a carry-state quest objects until the item pass defines them (ED-11). |
| **Escort-follow** | Systems | The EH-M2 escort-follow (Thalan, `S07`): walking pace; never targetable; hazard-immune. |
| **Emberlight** (`warrens.emberlight`) | Art / VFX | A light that travels a fixed path along the vault rim (~4 s), per player, once. |
| **Stove flare** (`cinderweave.stove_flare`) | Art | The back-room stove flame stands up and settles (~3 s) on the shop bell during `EAC-D2`. |
| **Barricade prop** | World state | Deepbrand barricade past the Warrens' mouth post-quest (non-interactive). |
| **Document view** | UI | The proving-ring slate. |
| Creatures | Schema / Gameplay | Deepbrand Crew guard, crossbow; Emberdeep Sentinel **sentinel**, **warden-frame** (bible §10). |

**New runtime needs: one possible, with a fallback that needs none.** The sigil-stone's world-volume reading may need support; the per-door inspect is the fallback. Everything else is a standard system, the EI-HT-01 fallback form, or an EH-M2 pattern.

## A13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The elder held below** (R10) | Thalan Veyr, taken in the purges, alive, held in a frame used for Perfect Flame research (bible §2.3). | The Volkhari "abandoned the city"; no captive survives. | Dahrin's account (alive the night he ran); the chamber with Thalan in it; the slate. | No captive survives; he died long ago. | What Thalan has been made to give. | **EH-M4 (resolved here).** |
| **The proving ring** | Trials to make advanced embercraft reproducible through conditioned hands carried by the frame (FT-04). | — | The slate; the stations with marks; "frame carried". | A training floor; a punishment. | Who stood at the stations; what "held to the mark" means beyond the tally. | EH-M6 (draw); CV-M4 (R18). |
| **The marks** | The Molten Stair ledger's coded column (R18). | — | Rings, dotted rings, filled rings on the slate (optional). | Coincidence. | Everything. | CV-M4. |
| **What is awake below** | The Titan (FT-05 direction). | The Ash-Clad Giant legend. | Thennek's palm and line; Thalan's "something burns that cannot stop". | A vein; a monster. | Everything. | R19, CV-M4. |
| **The emberlight** | Kaelith (canon: trails emberlight; feels the captive). | The Unburnt Boy, a children's story. | A light on a rim; Asera's "He isn't here." | A ghost; a guard's lamp. | Who; where. | None in Emberholt (deliberately). |
| **What Dahrin will not say** | The opening phrase of the Titan's binding (canon secret). | — | "Not here." | He is hiding his captors' names. | The phrase. | CV-M4. |
| **The feed pipe** | Heat drawn from the civic main (bible §2.3). | Old leaks (EH-M1). | A city-pattern collar with its number filed off (optional). | Old works. | Everything. | EH-M6. |

## A14. Open decisions

1. **D-E2, ruled 2026-11-15: fixed liberation.** Applied: `EAC-D10`, `EAC-B8`, the aided column and paragraph, `EAC_ACCOUNT_PROMISED` and every aided read are deleted; `EAC-D8.60`–`.62` is now Asera's single line, Thalan's "Ask me", the player's one ask and Thalan's voiced consent to leaving (`EAC-D8.64` and `.66` retired). `S00`–`S05`, the common part of `S06`, R10, the stone, both approaches and the walk out are unchanged. No option to end his life or exploit him exists (contradiction 7). Thalan's destination stays unplaced (D-C06).
2. **Smithing hook (resolved by the D-E2 ruling).** The hook stays where the bible puts it, the collar pins of the freed path, with two cool cycles of hand work as the time-cost alternative. The aided branch's blanking-plate hook was removed with that branch.
3. **Route in (`[ED-6]`).** The bible says the Warrens are reached from deeper junctions. This package uses Dahrin's escape shaft, which comes up below Yorven's EH-M3 bypass, opened with Yorven's key (a favour, not a disguise), and Thennek as guide. MAP VERIFICATION REQUIRED for the gate, the shaft and its depth. Thennek's own way in and out is never shown, so no refuge or route is located.
4. **The sigil-stone as the fifth item** (bible §9.4). Taken here as an item. **Fallback** if the item budget drops to four: a carry-state object with the same states; nothing else changes.
5. **The sigil gallery's three tiers [NEW].** The stone, flarecap and one taught mark. The sigils are otherwise never translated. Text, props and states only.
6. **The proving ring's sectors and the warden-frame's draw [NEW].** A readable construct fight on a floor that keeps time. Asera's "That ring is fed from his frame" and the darkening ring after `S06` say what the frame is used for without saying what it takes from him (R10 withheld).
7. **The slate's mark column (optional R18 seed) [NEW].** Matches the EH-M2 ledger's coded marks and says nothing more; the marks stay undeciphered (Act I §B14.3). Cut freely; `EAC_MARKS_MATCHED` goes with it.
8. **The feed pipe's filed collar (optional EH-M6 seed) [NEW].** Cut freely if the Act III package prefers the first sight of a city collar to be in the main.
9. **Maeryn's "We're not gone." (`EAC-D11.35`) `[ED-12]`.** Canon gives Maeryn this line "if trust is earned". It is optional, unforced and her own; the player cannot ask for it. Independent review cut her second sentence ("People say we went. We didn't go anywhere."), which described where her people are and sat against canon's "dispersed" and "avoid Emberholt" (World Truth C.3); the line is now the canon hook only. If the Director prefers it held for *Stitches in the Lining* (EST) or later, cut the node and `EAC_MAERYN_SAID`.
10. **Dahrin's account and his message to Thalan [NEW].** Dahrin's history stays inside the Part 4 ledger: captured after the war, escaped; no age, no wartime role, no count of years. Thalan names nobody and gives no number.
11. **"Ask me" (`EAC-D8.60`–`.62`) (D-E2, ruled 2026-11-15).** The player asks; Thalan consents in his own words; `EH_THALAN = freed` is set by his line. There is no other ask.
12. **Thennek and Asera as non-combatants.** Bible §5.1: Asera never fights; Thennek's canon is pathfinding. Neither is ever in a fight or engaged.
13. **Level framing (ED-10).** Expert identity. Smithing `[GD: mid]` with two cool cycles as the time-cost alternative.

## A15. Internal review log

| Finding | Revision |
|---|---|
| R10 guaranteed path (Revelation Ledger: "the chamber in EH-M4"; custodians "Dahrin Vosk's escape account and the containment chamber"). | `S01` requires Dahrin's account; `S05` requires seeing Thalan in the frame and reading the slate. Both on the main path; nothing missable. |
| R10 withheld ("what Thalan has been made to give"). | The slate tallies trials and "frame carried"; Thalan says "That is mine"; no inspect, line or prop shows what is taken. |
| R10 wrong reading supported. | Act I's "held below" is past tense; Dahrin says only "alive the night I ran"; the player believes the elder may be dead until the door opens. |
| R19 kept to seeds. | Thennek's one line; Thalan's "burns that cannot stop... in pain". No Titan word, shape, binding or initiate. Dahrin's phrase stays unsaid ("Not here."). |
| Contradiction 7. | No option, line or prop offers to end Thalan's life or use him. |
| Consent. | Thalan consents to leaving in his own words with his own reason (`EAC-D8.62`) (D-E2, ruled 2026-11-15); the player chooses how he is freed, never whether. |
| One outcome (D-E2, ruled 2026-11-15). | Aided branch removed; both approaches (Smithing drift, two cool cycles) kept at the same anvil; one Thennek scene and one Dahrin scene. Nothing implies his leaving ends the works or the suffering below (`EAC-D8.62`). |
| `[ED-12]`. | Dahrin, Asera, Thennek and Thalan each decide what they say; Asera decides how far she goes; Maeryn's line is optional; nothing locates a refuge or counts anyone; Thennek's side cut is never followed. |
| Kaelith. | Emberlight only; Asera's "He isn't here"; never named. |
| ED-6, CDR-4. | No stealth, detection, disguise or alarm. The route is a shaft opened by a favour; doors are read; plates are timed hazards; guards fight. |
| CDR-1, CDR-2, CDR-6. | Every enemy to 0 HP; the warden-frame's draw is a place rule; ranged viable, never required; per-player stone, doors, Thalan and approach; solo-tuned. |
| Skill hook. | Smithing `[GD: mid]` with two cool cycles as the time-cost alternative. |
| Remnant word. | No NPC says "Remnant". Dahrin says "Ashfall" and "their"; the slate says *Perfect Flame*. |

---
---

# Part B: EH-M5 The Speaker's Smile (`ESS`) (D-S1, ruled 2026-11-15)

## B1. The quest in one paragraph

**Seralynd Hearthveil**, the Ember-Priestess, has dreams she does not trust, and she asks the warden's hand to stand beside her in the rehearsal crowd on the **Ash Terraces**: "You're not ours, and you're not his. Yorven says you read tells." On the terraces the High Kindling is being rehearsed. **Saelia Verithe** conducts from a cue sheet; **Ralenne Kharveil** reads from her lectern; on the balcony above, the **Flameward Speaker** smiles at his city. On each cue the player reads a row of brazier tells, and they go amber together, on the crowd's in-breath. On the second run Saelia stops everything: "Too tidy." Her cues are on four; the crowd is breathing on a fifth beat that is not on her sheet. It came in the script: Ralenne's new line, *one flame, one breath, one city*, with a breath mark under it, arrived on an unsigned **suggestion slip** sealed with the Covenant's vigil wax. Ralenne keeps every slip; they are the best lines she has ever been given. **Grand Marshal Kaevren Thalos** sends for the warden's hand: his guards were told where to stand at the rehearsal, and not by him. The orders routed round him all bear one duct-post mark, the **letter-room** under **Speaker's Hall**, and he cannot walk into the Speaker's house. The **Cinder Rat** can walk under it. His price is to be told where the player heard the pipes sob ("Same place. Always the same place."). Through his duct the player reaches the letter-room and a locked case: the Speaker's own letter, *To the Seat*, waiting for collection, and a ribboned bundle of answers he has kept for years. He asked for the Council's vote, for the safe-craft schools, for the terraces; each was given. He asked once what the deep works are for, and was told they are kept. Seralynd takes the warden's hand to **Serix Arden**, a frightened young initiate who keeps the **Hearthveil sleep rooms** below the Covenant lamp-house. The vigil access book upstairs names who slept which night. Below, the braziers answer Serix's fear and flare into **Cinder Wraiths** until the player douses them; the record room's damper is jammed open and must be shot shut from the gallery or reached by a hot ladder. In the **chamber record** the Speaker's vigil nights are listed with what was "set" in each, and the night before Ralenne's slip says *one flame, one breath, one city*. A list of guided sleepers names a magister, councillors by office, and the Priestess herself. And a column Serix did not want anyone to see lists nights when sleepers dreamed things nobody set. The player copies it under Serix's witness. At the next rehearsal, standing in the crowd, the player feels the crowd's breath carry one beat past the cue, and their own breath goes with it. Then the warden's hand decides who hears: Seralynd, on the terrace, in her own words (**challenged**), or **Magister Vael Trossen**, whose own name is on the list, in a sealed inquiry (**exposed**). The Speaker answers both with warmth and omission. He stays in office. The High Kindling will go on.

**What the player should remember:** the fifth beat; the ribboned answers; "I ask that the city not be frightened"; their own breath going with the crowd's. **What the player should want next:** where the heat for all of this comes from.

## B2. Selection record

| Candidate | Verdict |
|---|---|
| **A. The Speaker is unmasked and removed.** | Rejected. Bible ED-5: he stays in office in both outcomes so that CV-M4's festival happens; the Arcs' exit is "the Remnant exposed but not ended". |
| **B. The Speaker confesses or lies.** | Rejected. Canon and bible §5.3 rule 5: he omits, reframes and thanks; he never lies outright. (D-S1, ruled 2026-11-15) |
| **C. The player dreams, and the dream shows the truth.** | Rejected. ED-17: no player dreams in Emberholt; no dream or vision is evidence. |
| **D. The letters alone prove it.** | Rejected. R11 needs the correspondence **and** the Hearthveil chamber record (two custodians); R12 needs the record **and** an access pattern. |
| **E. Rehearsal → script and slip → intercepts → the Rat's duct → letters → the access book and the sleep rooms → the record copied under witness → the second rehearsal → who hears** (selected; the bible brief with one beat moved, §B14.2). | **Selected.** Every finding is a record, an object or a living witness; the readable system is turned on a crowd and then on the player; the one fight frames a frightened witness's room; the choice decides who hears, not what is true. |

## B3. Canon grounding

| Element | Source | Status |
|---|---|---|
| The Flameward Speaker: middle-aged man; warm, measured, "every ember of Emberholt"; avoids direct lies, prefers omissions; rose from a lower-tier family; chosen and groomed by the Remnant as the city's public face; receives visions seeded by Hearthveil initiates and believes them divine; does not know the Ashfall endgame; suspects something is wrong beneath the city and fears what knowing would demand | Character file §1; Part 4 ledger; Review §2 contradiction 2 | [CANON]; what he knows is (D-S1, ruled 2026-11-15) |
| He addresses Emberholt from Cinderreach Spire on high holidays; rallies on the Ash Terraces | Dossier §VI.2, §VI.6 | [CANON] |
| Seralynd Hearthveil: Ember-Priestess; soft-spoken, firm, compassionate toward doubt; her dreams are shaped by Hearthveil operatives; occasional unscripted visions; confides doubts | Character file §3; Factions §7 | [CANON] |
| Serix Arden: young Hearthveil initiate; crafts and seeds dreams; suppresses doubt; has started seeing visions he did not craft (the canon "centred on the player" is not used, ED-17) | Character file §12; Factions §4 | [CANON] |
| Calynne Vorr: Vision-Mother; plants visions affirming the Speaker as chosen; appears only as a name in a record | Character file §13; bible §5.1 | [CANON]; name only |
| Vael Trossen: High Magistrate; appointed by the Speaker; dreams disrupted by Hearthveil work; keeps a private list of cases where evidence conflicted with reports | Character file §19 | [CANON] |
| Ralenne Kharveil: receives "suggestions" for script changes from an intermediary, believing them inspired; unaware of conditioning | Character file §20 | [CANON] |
| Saelia Verithe: ritual conductor; initiates embed motifs in her scripts; she suspects something is off and cannot pinpoint it | Character file §25 | [CANON] |
| Kaevren Thalos: intercepted orders routed around him; private disappearance ledger | Character file §2; Part 4 ledger | [CANON] |
| The Cinder Rat: lives in old conduits; "hears secrets through the pipes"; trades information; seeks the "sobbing ember" | Character file §28 | [CANON] |
| Hearthveil Initiates seed dreams into civic leaders, instructors and promising students; several Council members act under dream influence | Factions §4, §5 | [CANON] |
| Rehearsals teaching a crowd to breathe in step; the letters to "the Seat"; the chamber record; the sealed inquiry; the two answers | Bible §2.3, ED-5, §6.1 | ED-5 (D-S1, ruled 2026-11-15); [PROPOSAL — DIRECTOR] detail |
| The fifth beat; the suggestion slip and vigil wax; the guard-formation intercept; the duct-post letter-room; the Rat's price; the kept answers; the vigil access book; the "not set" column; the braziers answering Serix | This package | [NEW] |

## B4. Quest summary card

| Field | Value |
|---|---|
| Working title | **The Speaker's Smile** |
| Suggested content id | `emberholt.main.05_the_speakers_smile` |
| Arc position | Act II turn (Arcs §3.3, EH-M5: "Expose the Speaker's double nature in public view") |
| Prerequisite | EH-M4 Completed. Tuned for Expert identity (ED-10). |
| Offer | Journal lead from EH-M4: *The Ember-Priestess has asked for the warden's hand at the Covenant lamp-house.* Seralynd in the vigil hall (`ESS-D1`). |
| Solo / co-op | Solo-clearable. Co-op partners share the sleep-room fight; the rehearsal readings, script, intercepts, the Rat's price, the letter-case, the access book, the damper, the record copy, the second rehearsal and the choice are per player. |
| Target length | 45–60 minutes first time |
| Combat share | ~15% |
| Dialogue share | ~35% |
| Watching, comparing, crawling, reading, copying, dousing, the damper, choice | ~50% |
| Skills touched | Melee or Ranged (either; neither required); **Ranged ~[GD: mid]** (optional: shoot the damper latch; climbing the hot ladder over two vent cycles is the time-cost alternative) |
| Choices | How the Speaker is answered (`EH_SPEAKER` = challenged / exposed) (D-S1, ruled 2026-11-15); shoot or climb (`ESS_DAMPER`, flag only) |
| Unlocks | `EH_SPEAKER`; the Covenant lamp-house vigil hall as a rest point (keep-watch bench); EGT; EH-M6 |
| **Anchor** (contract) | Council and Covenant (the Speaker, Ralenne, Vael Trossen; Seralynd, Serix, Saelia) |
| **World-truth row** (contract) | H21 (dreams and induced visions), H22 (present hidden harm through civic ceremony) |
| **Revelation role** (contract) | **Owns R11** (D-S1, ruled 2026-11-15) (the Speaker believes in his city, knowingly accepts help and harmful compromises for his own rise, and is also dream-seeded; he lacks the endgame): custodians the letters (`ESS_letters`, from the letter-room Kaevren's intercepts point to) and the chamber record (copied under Serix's witness). **Owns R12** (some visions are induced): one case proven by the vigil access book (pattern) plus the chamber record, corroborated by Ralenne's slip; the record's "not set" column keeps it from dismissing all Dreamers. **Seeds R18** (rehearsals teaching a crowd to breathe in step; students on the steadying list, optional). |
| **Recurring evidence** (contract) | Four independent holds: the **letters** (`ESS_letters`; the Speaker's own case; routing marks matching **Kaevren's intercepts**), the **chamber record** (Hearthveil's; copied and witnessed by **Serix**), the **vigil access book** (the Covenant's, public, read in place), and **Ralenne's script and slip** (her custody). The letters recur in EH-M6 (the Speaker's letter) and CV-M4. |
| **State compliance** (contract) | Inactive / Active / Completed. Rehearsal windows re-run; the duct's hot stretch can be waited out; the Ranged hook has a climb; channel progress is kept; the copy cannot fail. Choice recorded in `EH_SPEAKER` (D-S1, ruled 2026-11-15). Resume at the persisted step with a hook at the vigil hall (Seralynd), the terraces (Saelia), the Marshal's office (Kaevren) or the terraces' service yard (the Rat). |
| **Combat compliance** (contract) | Cinder Wraiths (wraith, flare) defeated at 0 HP; they re-form at a lit brazier's flare while any brazier in the row burns (place condition, never health); dousing the last brazier ends the condition and any Wraith standing fights on to 0 HP. Melee or ranged; ranged never required. Solo-tuned. No SX. No defeated enemy gives testimony. The Speaker, Seralynd, Serix, Saelia, Ralenne, Vael, Kaevren, the Rat and every citizen are never targetable. |

## B5. The places

### B5.1 The Covenant lamp-house [EP22, NEW place on CANON practice], Emberhold District

**MAP VERIFICATION REQUIRED.** Relative order: the street door → the vigil hall → the old dormitory stair → the dormitory → the sleep-room corridor → the record gallery and record room.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **L1. The vigil hall** | Offer (`S00`); Serix (`S04`); the choice (`S06`); rest point after. | A long, quiet hall of hanging emberlight lamps turned low. Benches. A lectern by the inner door with the **vigil access book** chained to it. Grey cloaks on pegs (the Covenant's lamp-keepers wear them). |
| **L2. The old dormitory** | Passed through (`S04`); optional inspect. | A plain dormitory of narrow cots, some small, made up tight. A notice board on the door. The cots are the "vigil guidance" students' (Act I §B14.4). |
| **L3. The sleep rooms** | Braziers and Wraiths (**ESS-E1**) (`S04`). | Three low vigil rooms in a row (**L3a**, **L3b**, **L3c**), each with a cot, a stool for a watcher, and an iron **brazier** with a tell in its rim. A **vigil cistern** with a ewer at the far end. A blue niche by the cistern. |
| **L4. The record gallery and record room** | The damper (Ranged hook); the record; the copy (`S04`). | A narrow **gallery** with a rail above a small **record room** of shelves and a desk. A **chimney breast** in the room's wall carries the braziers' flue; high on it a **damper latch** on an iron plate. An iron **ladder** up the breast beside a wall vent. |

### B5.2 The Ash Terraces [EP23, CANON] (return)

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **T1. The rehearsal terrace** | Ralenne's lectern (`S02`). | As Act I. |
| **T2. The crowd floor** | The rehearsals (`S01`, `S05`, `S06` challenged). | A broad lower terrace where the crowd stands in loose rows between three **brazier rows** (left, centre, right), each brazier with a tell. A painted **mark** on the stone for each rehearsing citizen. Saelia's cue stand at the front. Above, the **Speaker's balcony**. |
| **T3. The service yard** | The Cinder Rat (`S03`). | A yard below the terraces where the brazier feed lines run into the stone. A **vent grille** at knee height, big enough to crawl through. |

### B5.3 The Rat's duct [NEW sub-site of the Underworks]

An old heat duct from the terraces' feed lines under the Emberhold District to the cellar of Speaker's Hall. **MAP VERIFICATION REQUIRED.** Crawl-height then walk-height; two floor vents; one **Working** stretch along a brazier feed with a niche; one optional agility drop (walkable fallback by a side crawl). The Rat's things in a dry alcove: a blanket, a lamp, a row of keys on a wire.

### B5.4 Speaker's Hall [EP28, CANON]

**MAP VERIFICATION REQUIRED.** The player sees only two rooms of it.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **H1. The letter-room** [NEW sub-site] | The letter-case (`S03`). | A cellar room at the end of an old **duct-post** line: a brass tube mouth in the wall with a bell, a sorting shelf, a locked **letter-case** of dark wood on the wall, a lamp. The duct grate opens from a low arch. Nobody is here at night. |
| **H2. The Magister's chambers** [NEW sub-site] | The sealed inquiry (`S06` exposed). | A plain panelled room with a long table, a seal-press, a high window. Vael Trossen's emberstone seal-ring on his hand. |

### B5.5 Embergate: the Marshal's office [EP01 sub-site, as Act I E1]

Kaevren's map table and ledger box (`S02` end, `S03`; `S06` challenged aftermath).

### B5.6 The Ridge: EP20 Elyndra's Vent Shrine [existing bible POI; optional] (D-EL, ruled 2026-11-15)

Used only for the optional consult (`ESS-D12`). The site, its layout and its placement are owned by EFD / EDS05 (Side Quests: Combat and Discovery); nothing is added. **MAP VERIFICATION REQUIRED.**

## B6. Player-facing sequence

### Beat 0: Seralynd (`S00_offer`)
**Objective:** *Speak to the Ember-Priestess at the Covenant lamp-house.*
**Seralynd Hearthveil** is in the vigil hall turning the lamps down one notch for the night (`ESS-D1`). She is soft-spoken and plain about why she asked: she has been dreaming the High Kindling before it happens, the same dream on the nights she keeps vigil, and she does not trust a dream that arrives on time. "Fire remembers. We must remember rightly. I'd like to know if I'm remembering something I was given." She asks the warden's hand to stand beside her in the rehearsal crowd at dusk "and read it the way you'd read a junction". "You're not ours, and you're not his. Yorven says you read tells."
- **Accept:** **Active**.
- **Not now:** "The rehearsals run every dusk until the Kindling. I'll be at my mark." Re-offered (`ESS-D1.90`).
**Verbs:** listen, accept.

### Beat 1: The Rehearsal (`S01_rehearsal`)
**Objective:** *Stand in the rehearsal crowd and read the braziers.*
The terraces at **dusk** (keep watch at the vigil hall bench or a terrace bench if not dusk; rehearsals run every dusk). The player stands at the mark beside Seralynd's on the crowd floor (T2). **Saelia Verithe** at her cue stand, chalk on her hands; **Ralenne** at her lectern above; on the balcony, **the Speaker**, in red and black, smiling down at his city (`ESS-B1.1`; he lifts a hand to the crowd and says one line, `ESS-D2.02`).
**The first run** (~90 s; §conventions, rehearsal inspect windows). Saelia calls the cues on a count of four (`ESS-D2.10`): "Lamps. Two. Three. Four." On three of her cues a **window** opens on a brazier row (left, centre, right in turn); the player **inspects** that row's tell in the window (required, all three; `ESS-I1`). Each time the tell has just gone amber, and each time the crowd round the player has just breathed in, together. Sets `ESS_RUN_READ`. (A missed window is re-offered on the next run; nothing fails.)
**The second run.** Runs repeat ("From the top!") until all three windows are read; halfway through the first run after `ESS_RUN_READ`, Saelia stops it (`ESS-D2.20`): "Stop. Stop." The crowd stops. "Too tidy." To the player and Seralynd, low: her cues are on four; the crowd is breathing in on a fifth beat that is not on her sheet. She shows the **cue sheet** (inspect, required; `ESS-I2`): counts of four, her chalk marks, no fifth. "I wrote the cues. I didn't write that." Sets `ESS_TOO_TIDY`. "It's in the script. Ask the Magistrix where the script came from. Nicely; she loves it."
**Verbs:** stand, read on cue, listen, compare.

### Beat 2: The Script (`S02_script`)
**Objective:** *Ask the Magistrix about the script.*
**Ralenne Kharveil** at her lectern on the rehearsal terrace (T1), delighted to be asked about her script (`ESS-D3`). `[ALLOCATION]` variant (`ESS-D3.03`): `posted`: "You put my aide's name on a Cooling House board. I read every order twice now."; `settled`: "Your Overseer countersigns my clerk's coal book every week. He is very slow about it."
- **The script** (required; `ESS-I3`): the High Kindling address and responses, much revised in her hand. One line is not in her hand's rhythm: ***One flame, one breath, one city.*** Under it, a small breath mark between the beats. Sets `ESS_SCRIPT_READ`.
- **The slip** (required): asked where the line came from, she is glad to say: it came on a **suggestion slip**, as her best lines do. They come unsigned, "from the vigil"; a lamp-keeper leaves them. She keeps every one, tied in her script stack, and shows the newest (`ESS-I4`): the line and the breath mark, on Covenant paper, sealed with a dab of the lamp-house's **vigil wax**. "Somebody dreams better than I do. I'm not too proud to take a good line." Sets `ESS_SLIP_SEEN`.
- She is sincere and unaware [CANON]. The player can ask whether she wonders who writes them; she says she used to, and then decided it did not matter if the lines were good. There is no option to tell her it is conditioning (the player does not yet know it is).
As the player leaves the terrace, an **Emberguard clerk** is waiting (`ESS-B2.4`): "The Marshal asks for the warden's hand. He says you'll know where." The step completes.
**Verbs:** read, ask, compare.

### Beat 3: The Letters (`S03_letters`) (D-S1, ruled 2026-11-15)
**Objective:** *Find where the orders go.* (Sub-objectives in order.)

| Sub-objective | Where | What the player does | Sets |
|---|---|---|---|
| **The intercepts** | Marshal's office (E1) | **Kaevren Thalos** (`ESS-D4`) lays four **intercepted orders** on his map table (documents; `ESS-I5`): orders to Emberguard officers, routed round him. The newest tells guards at the High Kindling rehearsal to stand the crowd in rings and "hold their line on the fifth beat". Each carries the same small stamped **routing mark** on its back: a flame in a square, the duct-post mark of the Speaker's Hall letter-room (the Act I work-order document shows only its face, so the stamp is on the back). With `EGH_ORDER_SHOWN`: he turns the gallery order over: "It was the first I could hold." With `EGH_WORK_ORDER` but not shown: he tells the player what to look for on its back (`ESS-D4.04`); the player need not still hold it. "I can't walk into the Speaker's house. I'm the Marshal. You're not anybody's. That's useful again." Of the pipes: "There's a man who lives in them and sells what he hears. My clerks call him the Rat. He seems to know you." **Carry-state: the intercepts.** | `ESS_INTERCEPTS` |
| **The Rat's price** | The service yard (T3) | At the vent grille, **the Cinder Rat** (`ESS-D5`): soot-stained cloak, rough glass half-mask, amused. With `ECW_RAT_SEEN`: "You looked back. Most don't." His price is a question: where were you standing when the pipes sobbed (`ECW_SOB_HEARD`, always set by EH-M1)? The player tells him: under Cinderwall, at the ward's junction. He goes still. "Same place. Always the same place." He says nothing else about it, then or ever. He takes the player into his duct. | `ESS_RAT_PAID` |
| **The duct** | The Rat's duct (B5.3) | A crawl and a walk under the district (vent breath; one Working stretch with a niche; optional agility drop). No enemies (it is the Rat's home and he knows what lives in it). The Rat goes ahead and waits at the far grille; he hands the player a key off his wire: "Everything in the pipes comes to me eventually. Keys too." | `ESS_DUCT_DONE` |
| **The letter-room** | H1 | **Inspect the duct-post tube** (required; `ESS-I6`): its routing plate bears the flame-in-a-square. **Open the letter-case** with the Rat's key (one interaction). Inside: (1) a sealed letter **in the Speaker's hand**, addressed *To the Seat*, waiting for the morning collection; the seal is a soft wax the Rat lifts and resets with a warm knife (`ESS-D5.30`); the player **reads it in place** (document; required) and puts it back. Sets `ESS_LETTER_READ`. (2) A **bundle of answers** tied with a red ribbon, years of them, kept (document; required): **`ESS_letters`**, quest item. The Rat: "Take the old ones. Leave the new one. If the new one doesn't go, someone comes looking. If the old ones go, he can't tell anyone they're gone." | `ESS_LETTER_READ`; item |
| **Back to Kaevren** | E1 | Kaevren reads the bundle at his table, slowly (`ESS-D4.40`). "He asked. Every one of these, he asked." He hands it back: "Carry it. If I hold it, it's the Marshal against the Speaker. If you hold it, it's evidence." | — |

The letters (D-S1, ruled 2026-11-15) (full text in the dialogue file). **The kept answers**, in a hand that is not his, each beginning *Answered:* and quoting his ask: the Council's vote carried; the safe-craft schools his to open; the terraces his on high holidays, "speak from the spire"; and one answer to a question: *You asked what the deep works are for. They are kept. That is all the Speaker needs.* **His outgoing letter**, in his hand: thanks for a fuller Kindling; his vigils "clear this season", in which he has "seen the city as one flame"; that the orders have gone down the tube "as you wished, under my office's mark", so the Marshal need not be troubled; that the terraces going quiet for him tell him he was right to ask; and *I do not ask what the deep works are for. I ask that the city not be frightened.* Together they show a man who believes in his city, who asked for his rise and accepted it, who knowingly lets orders go round the Marshal through his own letter-room, who likes being heard, who sincerely dreams what he is given, and who has been told he does not need to know the rest (R11; Part 4 ledger limit). Nothing in them shows the Ashfall endgame. Nobody in them is named but the Speaker.
The step completes when Kaevren hands the bundle back.
**Verbs:** compare marks, pay, crawl, open, read, take, leave.

### Beat 4: The Sleep Rooms (`S04_sleep_rooms`) (D-S1, ruled 2026-11-15) on the record's lines about the Speaker
**Objective:** *Read the vigil record below the lamp-house.*
1. **Serix** (L1). Seralynd has asked **Serix Arden** to meet the warden's hand (`ESS-D7`). He is thin, barefoot, ash on his feet, and frightened in a careful way. He agrees because "I'd like someone to see what I didn't make." He will witness a copy; he will not let anything leave the room but a copy. Seralynd stays in the hall: "It's his room. And they're my dreams. I'll wait."
2. **The access book** (required; `ESS-I7`). Chained to the lectern by the inner door: the Covenant's public vigil book, who kept vigil which night and in which room. The Speaker's name stands on a run of nights in **the third room**. Seralynd's own on some nights in the second. Sets `ESS_ACCESS_READ`.
3. **The dormitory** (L2; optional inspect `ESS-I8`). Narrow cots, some small, made up tight. The **notice on the door** reads by `EH_CURRICULUM`: `guild`: *Steadying transfers suspended pending the teachers' guild review*, and half the cots are stripped; `evidence`: no notice, and every cot is made up. Serix does not look at them.
4. **The sleep rooms** (L3; **ESS-E1**; §B7). As they enter the corridor Serix's breath goes short, and the three braziers stand up white: **heat follows the room**. "It's me. It's always me in here." **Cinder Wraiths** form at the braziers on each flare. **Douse the braziers:** fill the **vigil ewer** at the cistern (one interaction; carry-state; no attacking while carrying), carry it to a brazier and **pour** (2-segment channel, ~3 s each). Each doused brazier lowers the cap. When the third is out, nothing more forms; any Wraith standing fights on to 0 HP. Serix stands in the cistern niche and is never targeted. Sets `ESS_BRAZIERS_OUT`.
5. **The damper** (L4; the skill hook). The record room's flue damper is jammed open and the room below is **Surging** (the braziers' heat went up the flue and down into it). Two ways, both complete the beat:
   - **Option A (skill): Ranged ~[GD: mid].** From the gallery rail, **shoot the latch** on the chimney breast (one hit on a plate-sized target at ~12 paces; a missed shot simply misses). The latch drops, the damper swings shut with a clang, and the room drops to **Working**. `ESS_DAMPER` = shot.
   - **Option B (time-cost): climb.** Down into the room (heavy periodic damage on the floor while Surging; a cooling niche at the ladder foot, and the ladder itself, out of the worst of it, takes only light periodic damage), up the iron **ladder** beside the wall vent (exhale ~10 s, ash lift ~1.5 s; climb on the rest), and at the top **pull the latch** by hand: a 2-segment channel that runs only between exhales (progress kept), so it takes **two vent cycles**. `ESS_DAMPER` = climbed.
   Ranged is the skill hook, never the only way (CDR-2).
6. **The record** (required; document `ESS-I9` in the dialogue file). The Hearthveil **chamber record**: a ruled book of nights. Columns: night, room, sleeper, "set" (a motif), hand ("light", "full"), "carried" (where the motif surfaced after), and a mark for who set it (on most set nights, *C. Vorr*; on some, *S.A.*). The Speaker's pages: on the nights the access book puts him in the third room, the record shows a motif set "full", and on the night before Ralenne's newest slip, the motif is *one flame, one breath, one city*, "carried: to the Magistrix's script by slip, next day". A list headed **guided sleepers**: *Magister V. Trossen*; councillors by office only (*a councillor of trade*, *a councillor of guilds*); *the Priestess (light hand)*; and student numbers under "steadying". At the back, a column Serix keeps in his own hand: **not set**: nights when a sleeper woke and reported a dream nobody set. Sets `ESS_RECORD_READ`.
   - *Optional, with `EEH_LEDGER_READ`:* the steadying numbers are the Molten Stair's student numbers (`ESS-D8.44`); **40 is not among them** (Tavi's line was struck in EH-M2). Sets `ESS_STUDENTS_SEEN` (R18 seed).
7. **The copy** (required). At the record desk the player copies the Speaker's pages and the guided-sleepers list into a blank vigil book (3-segment channel, ~4 s each). Serix reads the copy against the record and signs under it: *Witnessed, copied from the record this night. S. Arden, initiate.* **Carry-state: the record copy.** Sets `ESS_COPY`.
8. **Serix's account** (`ESS-D8.20`–`.36`, required). How a vision is set: "You sit with them. You breathe with them, slow. You put a picture in the breath, and you leave it there." Of the Speaker (D-S1, ruled 2026-11-15): "He believes it. Every word I give him, he believes. He thanks me for them without knowing it's me." And: "Don't make him a lamb. What I set, he wanted already. I only made it sound like the fire." (`ESS-D8.33`) Of the "not set" column `[ED-17]`: "Some nights I see things I didn't set. So do some of the people I sit with. I don't know who sets those. I'm not saying it's anyone." Sets `ESS_SERIX_HEARD`.
The step completes on `ESS-D8.40` end.
**Verbs:** ask, read, douse, carry, shoot or climb, read, copy, listen.

### Beat 5: The Second Rehearsal (`S05_second_rehearsal`)
**Objective:** *Stand in the crowd again.*
At the next dusk the player takes their mark beside Seralynd again (`ESS-D9`).
1. **The compare** (required, before the run): hold the record copy against the script line Ralenne reads (an inspect at the mark, `ESS-I10`): the breath mark in the script sits on the beat the record names. Sets `ESS_MOTIF_MATCH`. This is R12's one proven case: a dream set by name and night (record), slept by that man that night (access book), carried into a public script the next day (slip), and believed (his letter).
2. **The strange moment** (§B8.1). The run begins. Saelia calls four. On the fifth beat the whole crowd breathes in together, and the player's breath goes with it: the player character's in-breath is heard among the crowd's, in time, unbidden. The three brazier rows steady to one colour. Then the crowd's breath carries **one beat after the cue**, held, and lets go. Sets `ESS_BREATH_CARRIED`.
3. Saelia stops the run and looks straight at the player (`ESS-D9.20`): "You breathed with them." Seralynd, quietly: "Now you know what I've been dreaming."
The step completes on Seralynd's line.
**Verbs:** compare, stand, breathe.

### Optional lead (no step): Elyndra at the vent shrine (D-EL, ruled 2026-11-15)
While `S01`–`S05` are active, the player may go out to **EP20 Elyndra's Vent Shrine** on the Ridge (the existing EFD/EDS05 site; MAP VERIFICATION REQUIRED as there; no new place) and ask **Elyndra the Cinderseer** about the Speaker's dreams (`ESS-D12`, once per player). Seralynd's walk-away aside (`ESS-D6.12`) points there; a player who has met Elyndra in EFD can simply go. She can tell that some of the Speaker's dreams come "folded" (the seeded pattern) and that what is folded into them is what he already wanted. She does not prove it: she sends the player to what is written, his own letters and "a book of nights" (the chamber record). She offers her canon vision of the Speaker burning while weeping as an image she does not understand, and says she has read a burning wrong before. She never names the Remnant, the Seat, Hearthveil's operators, the endgame or Perfect Flame, and her reading is never evidence for `S03`, `S04` or `S06`. Sets `ESS_ELYNDRA_HEARD` (flavour). Nothing is required; the guaranteed path is unchanged.

### Beat 6: The Answer (`S06_answer`): *the choice* (D-S1, ruled 2026-11-15)
**Objective:** *Decide who hears it.*
In the vigil hall (L1), Seralynd, with the record copy on the bench between them (`ESS-D10`). Kaevren has come in a plain cloak and stands by the door. The **choice** (§B9.3):
- **Challenge it in public** (`EH_SPEAKER = challenged`): give the copy to Seralynd. She decides what she will say; she tells the player she will not read the list of names, only what is hers to say. **Next dusk on the terraces** (keep watch if needed; `ESS-D10.30`–`.48`): during the rehearsal, with the Speaker on his balcony, Seralynd steps to Ralenne's lectern (Ralenne lets her) and speaks in her own words: that she has dreamed what she was given; that she believes others have; that a dream that comes on time should be doubted; and she asks the crowd to breathe on their own count today. The crowd's breath falls out of step; the brazier tells scatter, some amber, some clear (heat follows the room, the other way). Saelia stops the rehearsal early. **The Speaker** answers from the balcony with warmth and omission: the Priestess has kept long vigils for the city; doubt is a kind of flame too; everyone should rest; they will try again tomorrow (`ESS-D10.44`). He denies nothing and admits nothing. Passing the player on the stair afterwards, he smiles: "You stood in my crowd. Thank you for coming, friend." (`ESS-D10.46`). The letters go to **Kaevren**'s ledger box (`ESS-D10.48`; item removed). **Completes** on Kaevren's line.
- **Expose it to a sealed inquiry** (`EH_SPEAKER = exposed`): take the copy and the letters to **Magister Vael Trossen** at Speaker's Hall (H2), with Kaevren (`ESS-D11`). Vael reads the letters, then the copy. He finds his own name on the guided-sleepers list and is silent for a long moment. Then he takes out a private list of his own (cases where evidence conflicted with reports [CANON]) and lays it beside the copy. He convenes a **sealed inquiry** of the Council for the next morning (keep watch in the Hall's anteroom if needed): the record, the letters and Serix's witness under his seal. **The Speaker** attends the sealed opening, summoned: "I have kept vigil as every Speaker has. I have never asked the Covenant for a dream." Asked about the letters: "A Speaker hears from many quarters, Magister." (`ESS-D11.30`–`.34`). He denies nothing he wrote and explains nothing. Vael seals the papers. The Council knows; the public does not. The rehearsals go on as written, except that Saelia, on her own, rubs the fifth beat off her cue sheet (ambient). The letters go under Vael's seal (item removed). **Completes** on Vael's seal (`ESS-D11.40`).
- **Ask Seralynd** returns her line ("They're my dreams. But it's your copy. I'll speak if you give it to me. I'll understand if you don't.") and the options again.
**Either way** the Speaker stays in office and the High Kindling will be held. The record copy stays with whoever was given it; the original stays in the record room.
**Verbs:** choose, give, watch, listen.

## B7. Encounters

Tuned for **Expert identity** (ED-10). Cinder Wraiths are resonance distortions (bible §2.4): defeated at 0 HP, they collapse into ash and re-form only while their condition lasts.

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **ESS-E1** | Cinder **wraith** and **flare** forms at the three braziers (L3a–c), cap 3 → 2 → 1 as braziers are doused (opening mix 2 × wraith, 1 × flare) | The sleep-room corridor and its three rooms | Wraiths go for the player wherever they are, and harder for a player carrying the ewer; flares hang over a lit brazier and throw | **Brazier flare (the condition):** a lit brazier's flame stands up white and its tell crazes red (~1.5 s), then it flares (a ring of heat ~2 paces round it); a defeated Wraith re-forms in the flare if the cap allows. Flare cycle ~10 s per brazier, staggered. **Wraith, Grasp:** arms flare white (~1.0 s), then a two-handed lunge (sidestep). **Wraith, Flash:** body brightens and hums (~1.5 s), then a heat burst in a 2-pace ring. **Flare, Toss:** a ball of fire swells between its hands (~1.2 s), then an arcing throw leaving a burning patch ~4 s. | The quest's one fight: a frightened witness's room answering him; carry water under pressure | 2.5–3.5 min from first flare to last Wraith; 50–70% HP |

**Hazards (not encounters):**
- **Duct vents** (B5.3) and the **record-room wall vent** (L4): timed exhale, ash lift ~1.5 s.
- **The duct's Working stretch:** light periodic damage outside the niche.
- **The record room while Surging:** heavy periodic damage until the damper is shut.
- **Burning patches** from flares: ~4 s.

**Rules**
- **Defeat at 0 HP** (CDR-1). Wraiths collapse into ash. **No enemy is cleared by the condition ending**: when the third brazier is doused, nothing re-forms, and those standing fight on.
- **Re-forming is a place rule** (rulings §3.1.2; bible §2.7): it depends on lit braziers, never on health or time.
- **Melee or ranged** (CDR-2): ranged players can thin flares from the cistern niche but must carry the ewer to each brazier; melee players clear a room and then carry. Out-ranging never ends the fight: only the water does. Ranged is never required; the damper's Ranged hook has a climb.
- **Combat never reveals evidence.** The letters are in a case, the record on a shelf, the pattern in a public book, the motif on a slip. Wraiths drop nothing.
- **Non-combatants:** Serix (in the niche), Seralynd, Saelia, Ralenne, Kaevren, Vael, the Rat, the Speaker and every citizen are never targetable. No crowd member is ever an enemy.
- **Death:** respawn at the vigil hall during `S00`, `S04`, `S06`; at the terraces' service yard during `S03` duct (until the letter-room), at the Marshal's office after it; at the crowd floor during `S01`, `S02`, `S05`. In the sleep rooms: doused braziers stay doused and the cap stays lowered; live Wraiths reset (ordinary leash reset); a carried ewer is set down full where the player fell. The damper, once shut, stays shut. The copy and the letters persist.
- **Co-op:** the fight shared; a defeat credits each partner whose own active step consumes it (CDR-6). Each partner's braziers, ewer, damper, record copy and choice are their own. Braziers are per-player props; a partner may fight in another's rooms, but dousing advances only the dousing player's step. Which partner's brazier state drives the shared re-form cap when partners' braziers differ is a presentation question for Sol (Act I Q-18 pattern); solo play is unaffected. Shared brazier presentation is a fallback only (bible §9) and never decides a partner's step or credit. Rehearsal windows and the strange moment are per player.

## B8. The discovery moments: presentation specs

### B8.1 The breath that carries (Beat 5)

**What it is:** heat follows the room (bible §1.1), shown in a crowd and then in the player. It is canon that rites were designed as mass emotional tests; what the player feels is their own breath falling in. It is **never explained** and never evidence: the evidence is the record, the access book and the slip.

| Time | Element | Spec |
|---|---|---|
| 0 s | **The run** | Saelia: "Lamps. Two. Three. Four." The crowd's lamps come up on four, as written. |
| ~1 s | **The fifth beat** | The whole crowd breathes in together on a beat that is not called. The sound is large and soft. |
| ~1.2 s | **The player** | The player character's own in-breath is heard in the crowd's, in time, close and unmistakable (a breath sound on the player, not a UI cue). The camera does not move. |
| ~1.5 s | **The braziers** | All three rows' tells go to the same amber at once and hold. |
| ~2.5 s | **The carry** | The crowd holds the breath one beat past where Saelia's next cue should come. The player character's breath holds with it. |
| ~3.5 s | **The release** | The crowd breathes out together. The player character too, a half-beat late, as if catching up. |
| ~5 s | **Saelia** | She stops the run and looks straight at the player: "You breathed with them." |
| Never | **Control** | Player input is never taken; the player can move throughout; nothing is shown as a meter, a status or a spell. Accessibility: a subtitle line *(you breathe in with the crowd)* for players without audio. |
| Never | **Explanation** | Asked later, Saelia: "Everyone does. That's what bothers me." Seralynd: "I know." |

### B8.2 The letter-case (Beat 3)

| Element | Spec |
|---|---|
| **The case** | A locked case on the wall beside the tube mouth. Inside: one sealed letter on top, and below it a bundle of folded answers tied with a red ribbon, the old ones softer and browner. |
| **The outgoing letter** | Read in place in the document view; returned to the case; the Rat resets the seal with a warm knife. Leaving it is the point: its collection in the morning goes on as if nobody had been there. |
| **The bundle** | Taken (`ESS_letters`). Its absence is not discovered in Act II. |
| **Never** | No signature on the answers; no name for "the Seat"; no place they come from. |

## B9. Quest structure for implementation

### B9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_offer` | Speak to the Ember-Priestess at the Covenant lamp-house. | `ESS-D1` end with accept | Yes | Requires EH-M4 Completed. Re-offer `ESS-D1.90` |
| `S01_rehearsal` | Stand in the rehearsal crowd and read the braziers. | Three window inspects (`ESS_RUN_READ`) + cue sheet inspect + `ESS-D2.24` end | Yes | Dusk pinned (keep watch). Windows re-offer per run. Sets `ESS_TOO_TIDY` |
| `S02_script` | Ask the Magistrix about the script. | Script inspect + slip inspect + `ESS-D3` end | Yes | Sets `ESS_SCRIPT_READ`, `ESS_SLIP_SEEN`. `[ALLOCATION]` variant `ESS-D3.03`. Clerk bark `ESS-B2.4` on leaving |
| `S03_letters` | Find where the orders go. | `ESS_INTERCEPTS` + `ESS_RAT_PAID` + `ESS_DUCT_DONE` + tube inspect + `ESS_LETTER_READ` + item gained + `ESS-D4.44` end | Yes | (D-S1, ruled 2026-11-15) on the letters and `ESS-D4.40`–`.42`. Item **`ESS_letters`** gained in H1 |
| `S04_sleep_rooms` | Read the vigil record below the lamp-house. | `ESS_ACCESS_READ` + ESS-E1 all defeated and `ESS_BRAZIERS_OUT` + damper shut + `ESS_RECORD_READ` + `ESS_COPY` + `ESS-D8.40` end | Yes | (D-S1, ruled 2026-11-15) on the record's Speaker pages and `ESS-D8.30`. Sets `ESS_DAMPER` = shot / climbed, `ESS_SERIX_HEARD`. `ESS_STUDENTS_SEEN` optional (needs `EEH_LEDGER_READ`) |
| `S05_second_rehearsal` | Stand in the crowd again. | `ESS_MOTIF_MATCH` + `ess.breath_carried` event + `ESS-D9.22` end | Yes | Dusk pinned. Sets `ESS_BREATH_CARRIED`. R12 proven case complete |
| `S06_answer` | Decide who hears it. | Choice in `ESS-D10` + challenged scene end (`ESS-D10.48`) or sealed inquiry end (`ESS-D11.40`) | Yes | (D-S1, ruled 2026-11-15). Sets **`EH_SPEAKER`**. Item `ESS_letters` removed (Kaevren or Vael). Quest → **Completed** |

### B9.2 Flags

| Flag | Set by | Read by (here) | Read by (later packages) |
|---|---|---|---|
| `ESS_RUN_READ` | Three window inspects (`ESS-I1`) | `S01` | — |
| `ESS_TOO_TIDY` | `ESS-D2.22` | `ESS-D3.10` option | — |
| `ESS_SCRIPT_READ` | `ESS-I3` | `ESS-I10` | — |
| `ESS_SLIP_SEEN` | `ESS-I4` | `ESS-D7.06`, `ESS-D8.12` | EGT (Glassmoth: "Slips? Somebody sells dreams on slips? Not me.") |
| `ESS_INTERCEPTS` | `ESS-D4.10` | `S03` | — |
| `ESS_RAT_PAID` | `ESS-D5.14` | `S03` | EH-M6 (the Rat at a grille: "Still the same place."); CV-M4 (request) |
| `ESS_DUCT_DONE` | Enter H1 | `S03` | — |
| `ESS_LETTER_READ` (D-S1, ruled 2026-11-15) | Outgoing letter read (`ESS-I6a`) | `ESS-D4.42` | **EH-M6** (the Speaker's letter: "The city will learn from this night" read beside "I ask that the city not be frightened") |
| `ESS_ACCESS_READ` | `ESS-I7` | `ESS-I10` | EGT (the access book recurs) |
| `ESS_BRAZIERS_OUT` | Third brazier doused | `S04` | — |
| `ESS_DAMPER` = shot / climbed | `S04` | `ESS-D8.02` | — |
| `ESS_RECORD_READ` | `ESS-I9` | `ESS-D8` options | EGT, EMS (`EMS-D4.20`); CV-M3 (dream-influenced delegates; request) |
| `ESS_STUDENTS_SEEN` | `ESS-D8.44` (optional) | — | **CV-M4** (R18; request) |
| `ESS_COPY` | Copy channel + Serix's signature (`ESS-D8.18`) | `S05`, `S06` | — |
| `ESS_SERIX_HEARD` | `ESS-D8.36` | — | EGT (Serix recurs) |
| `ESS_ELYNDRA_HEARD` (D-EL, ruled 2026-11-15) | `ESS-D12.40` (optional) | — | EH-M6 (`EGA-B9.13`, Elyndra's one aftermath line, optional); CV-M2/CV-M4 planning (she may recur as a guide who warns and points) |
| `ESS_MOTIF_MATCH` | `ESS-I10` | `ESS-D10.05` | — |
| `ESS_BREATH_CARRIED` | `ess.breath_carried` event | `ESS-D9.20` | CV-M4 (request: "You've breathed with a crowd before. Don't.") |
| `EH_SPEAKER` = challenged / exposed (D-S1, ruled 2026-11-15) | `S06` choice | `ESS-D10`/`D11`; `ESS-B9` | EH-M6 letter; terrace barks; CV-M4 |

### B9.3 Choice: how the Speaker is answered (D-S1, ruled 2026-11-15)

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Challenged** (`EH_SPEAKER = challenged`) | Seralynd speaks on the terrace in her own words; the crowd breathes on its own count; the rehearsal ends early. The Speaker answers with warmth and omission. Letters to Kaevren. | The public hears doubt without the evidence; the Speaker's warmth answers it in the same breath; some say the Priestess is tired (barks). The Council has no papers before it. Seralynd's standing in her own Covenant is strained. | EH-M6: the Speaker's letter. CV-M4: citizens who heard doubt on the terrace are readier to refuse (R18). |
| **Exposed** (`= exposed`) | Vael Trossen convenes a sealed inquiry with the record, the letters and Serix's witness. The Speaker answers with omission. | The public never hears; the rehearsal runs as written (without Saelia's fifth beat); the inquiry is sealed and slow; Vael's own name is in it. | EH-M6: the Speaker's letter. CV-M4: the Council arrives knowing; the crowd does not. |

**Neither is wrong.** Both keep the Speaker in office and the High Kindling on; both put the letters with a custodian; both keep the original record where it is; neither says what the Speaker does not know.

## B10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| The vigil hall | Access | A rest point (keep-watch bench) in the Emberhold District. |
| Rehearsal reading | Knowledge | The player can read a crowd's tells (ambient terrace content). No flag. |
| Payment | Currency | Kaevren pays an informant's fee at `ESS-D4.44` (small). Economy tuning [GD]. |
| Skill XP | Action only [GD] | Ranged if the latch is shot; Melee or Ranged at defeat. No lump quest XP. |
| Side-quest unlocks | Story | EGT |
| EH-M6 | Story | No journal lead. On the player's next entry to Cinderwall after completion, EH-M6 is auto-offered in a hard frost (`EGA_FROST`; bible §6.1). |

## B11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player misses a rehearsal window | Re-offered on the next run. Nothing fails. |
| Player arrives when it is not dusk | Keep watch at a terrace bench or the vigil hall. |
| Player leaves the duct midway | The Rat waits at the far grille; re-entry at the service yard. |
| Player takes the outgoing letter | Not possible: the case's interaction offers *read and return*; the Rat's line explains why. |
| Player cannot or will not shoot | The ladder (Option B), two vent cycles. Never blocked. |
| Player is beaten in the sleep rooms | Respawn at the vigil hall. Doused braziers stay out; cap lowered; a carried ewer set down full; live Wraiths reset. |
| Player tries to confront the Speaker before `S06` | He is reachable only on his balcony (out of reach) and in `S06`. If spoken to on the stair after a rehearsal, one bark (`ESS-B1.4`). No option accuses him. |
| Death | Respawn by step (§B7). Intercepts, letters, copy and sub-objectives persist. |
| Logout | Restore to the persisted step: the vigil hall (`S00`, `S04`, `S06` before the choice), the crowd floor (`S01`, `S02`, `S05`; `S06` after `challenged`), the Magister's chambers (`S06` after `exposed`), the Marshal's office or the service yard (`S03`). |
| Walking away | Quest stays Active. Resume hooks: Seralynd ("The rehearsals are every dusk. So are my dreams."), Saelia at her cue stand ("Four. Still four. Still five."), Kaevren ("The mark's still on everything I catch."), the Rat at his grille ("Pipes are open. They always are."). |
| Fail state | None. |
| Co-op | Shared fight. Per-player rehearsal windows, script, intercepts, Rat's price, letter-case, access book, braziers, damper, copy, strange moment and choice. A partner in another player's rehearsal sees their own crowd state (CDR-6). |

## B12. Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| **Rehearsal sequence with inspect windows** | Systems / Quest data | A scripted ~90 s run (crowd animation, cue barks) that opens three ~6 s inspect windows on brazier props; completion counts windows inspected; re-runs each dusk or on the player's request at the cue stand. Standard scripted sequence. |
| **Crowd breath presentation** (`ess.breath_carried`) | Audio / Animation | Crowd breath audio in time; a breath sound on the player character; brazier tells to one state; subtitle for accessibility. Presentation only; input never taken. Per player. |
| **Brazier re-form with a cap** (ESS-E1) | Gameplay | The Act I re-form-with-cap model (ECW-E3) keyed to lit braziers (3/2/1/0). |
| **Carry-state ewer** | Systems | Fill at a cistern; while carried, attack disabled; set down is one interaction; pour is a 2-segment channel at a brazier. |
| **Shootable latch** | Gameplay | A prop that takes a ranged hit and plays its state change (the Thornfell TST bowyer's mark precedent). |
| **Ladder with timed vent and a gated channel** | Systems | Ladder climb; a latch channel that runs only between the wall vent's exhales. |
| **Heat states** | Systems | Duct Working stretch; record room Surging until the damper is shut, then Working. Quest-pinned. |
| **Letter-case** | Systems | Locked container opened by a carry-state key; one read-and-return document; one take (quest item). |
| **Document views** | UI | Cue sheet, script, slip, intercepts, outgoing letter, kept answers, access book, chamber record, record copy. |
| **Dormitory notice prop** | World state | Notice and stripped cots by `EH_CURRICULUM` (per player). |
| **Agility trigger** | Systems | Duct drop; walkable fallback by a side crawl. |
| Creatures | Schema / Gameplay | Cinder Wraith wraith, flare (bible §10). |

**New runtime needs: none.** Everything is a standard system, an Act I or Thornfell precedent, or a scripted presentation event.

## B13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The Speaker** (R11) (D-S1, ruled 2026-11-15) | Idealist and manipulator: sincerely believes in the city's discipline, progress and strength; enjoys and pursues authority; knowingly takes part in institutional manipulation and accepts harmful compromises for ambition; also dream-seeded through those convictions, which does not absolve him; lacks the endgame and Perfect Flame (Architecture §5.0; Part 4 ledger). | The city's beloved guide. | The kept answers; his outgoing letter; the record's nights; Serix's "he believes it" and "he wanted it already"; optionally Elyndra's reading (`ESS-D12`, never proof). | Wholly a puppet (Serix's reading); wholly the mastermind (Kaevren's reading). | What he suspects below; what "the Seat" is. | **EH-M5 (resolved here).** |
| **Induced visions** (R12) | Hearthveil sets dreams by night and name (canon). | Visions are gifts. | Record + access book + slip + letter: one proven case. The "not set" column. | Every vision is induced; or none is. | Who sets the unset ones. | **EH-M5 (one case).** Dreamers series deepens. |
| **The fifth beat** | A conditioning motif in the script (canon: Saelia's scripts; Ralenne's suggestions). | A good line. | The cue sheet, the script, the slip, the player's own breath. | A conductor's mistake. | What the crowd's breath is for. | CV-M4 (R18). |
| **"The Seat"** | The Ashfall Authority's head (Factions; never named in Emberholt). | — | A form of address on letters. | The Council; the Speaker's own office. | Everything. | Later content. |
| **The "not set" column** | Unexplained in Emberholt (canon: something else is entering the dreamspace). | — | Serix's own column. | Proof of prophecy; proof of fraud. | Who or what. | None in Emberholt (deliberately). |
| **"Same place"** (the Rat) | Unexplained (bible §2.4). | — | The Rat's stillness. | Thalan. | Everything. | None in Emberholt (R19 shadow). |

## B14. Open decisions

1. **D-S1, ruled 2026-11-15: idealist and manipulator, also dream-seeded.** The former working layer is kept and the "wholly puppet" and "wholly mastermind" swap notes are resolved and removed (here, after `ESS-I6a`, after `ESS-D8`, and the `ESS-I9` block P alternative row). To show both halves, the outgoing letter (`ESS-I6a`) gains two sentences in his own hand (the orders sent round the Marshal under his office's mark; the terraces going quiet for him) and Serix gains `ESS-D8.33` ("What I set, he wanted already"). Nothing shows him knowing his dreams are set, and nothing gives him the endgame or Perfect Flame. He never fights, never confesses, never lies outright, and stays in office in both outcomes. **Independent review (2026-11-14), kept:** a kept answer asking for "clear" vigils was cut, and the letter thanks "the fire", because canon has him believe his dreams divine.
2. **Beat order (deviation, recorded).** The bible puts the damper in `S05` and the strange moment "at the next rehearsal". This package puts the damper inside `S04` (it guards the record room, so the skill hook sits before the record it opens) and makes `S05` the second rehearsal, where the strange moment and the record-to-script comparison happen. Step ids `S00`–`S06` and the bible's step count are kept; R11/R12 guaranteed paths stay in `S03` and `S04`.
3. **Calynne Vorr as *C. Vorr* in the record.** Bible §5.1: "Calynne appears only as a name in a record." Only the initial and surname, on set nights; nobody says it aloud.
4. **The Priestess on the guided-sleepers list [NEW use of a CANON secret].** Canon: her dreams are shaped by Hearthveil operatives. It makes her terrace choice her own reckoning. If the Director prefers to hold it, cut *the Priestess (light hand)* from the record and her access-book nights; her `S06` speech loses one sentence.
5. **Kaevren's formation intercept and the duct-post mark [NEW].** Gives "Kaevren's intercepts lead to a courier box" a concrete chain. Kaevren never enters the Hall and never handles the letters before the player brings them (Part 4: no anchor reaches another's evidence on their own).
6. **The Rat's price and "Same place" [NEW].** Pays off `ECW_SOB_HEARD`'s promise without explaining the sob. Cut the price line freely; the duct is unchanged.
7. **Leaving the outgoing letter [NEW].** Keeps the exchange running so nothing in Act II alerts the Speaker; the kept answers are what the player carries.
8. **Vael Trossen finds his own name [NEW use of a CANON secret].** Canon: his dreams are disrupted by Hearthveil work, and he keeps a private list of conflicting cases. He convenes the inquiry anyway. No ruling of his is shown.
9. **Students under "steadying" (optional R18 seed).** Numbers only; Tavi's 40 is absent. Cut freely with `ESS_STUDENTS_SEEN`.
10. **ED-17.** No player dream. Serix's unscripted visions are his and his sleepers', never about the player, never evidence.
11. **"The Seat".** Echoes a Remnant title without naming anyone (bible §13 left open). Kept as written in the bible.
12. **The Speaker's two short lines to the player** (`ESS-D10.46`, `ESS-B1.4`) are warmth, not threat, and fit D-S1 (ruled 2026-11-15).
13. **Level framing (ED-10).** Expert identity. Ranged `[GD: mid]` with the ladder as the time-cost alternative.

## B15. Internal review log

| Finding | Revision |
|---|---|
| R11 guaranteed path (Revelation Ledger: "the correspondence in EH-M5"; custodians correspondence plus Hearthveil chamber records). | `S03` requires the outgoing letter read and the kept answers taken; `S04` requires the record read and copied under witness. |
| R11 wrong readings supported honestly. | Kaevren reads "bought" from the letters; Serix reads "believes every word" from the record; the player holds both. |
| R11 limit (no endgame). | The answers tell him the deep works "are kept"; his letter says he does not ask; nothing in Act II tells him or the player more. |
| R12 guaranteed path and limit. | One case proven by four holds (record, access book, slip, letter); the "not set" column and Serix's account keep it from dismissing all Dreamers. |
| The Speaker never lies. | Every line he speaks is warmth, thanks, reframing or a true statement he believes ("I have never asked the Covenant for a dream"). |
| Ralenne and Saelia never villains. | Ralenne keeps slips because they are good lines; Saelia stops her own rehearsal twice and rubs out the fifth beat. Neither is targetable. |
| Serix's limit. | He sets dreams and says so; his unscripted visions are his experience; he never names who sets them. |
| "Infiltration" (ED-6). | A duct the Rat lives in, a key he owns, an empty cellar at night. No detection, disguise or alarm. |
| CDR-1, CDR-2, CDR-6. | Wraiths to 0 HP; re-forming by lit braziers only; ranged viable, the damper hook has a climb; per-player props and choice; solo-tuned. |
| Remnant word. | No NPC says "Remnant". "The Seat", "below", "the vigil" only. |
| Combat share. | One encounter; the rest is reading, comparing and copying. |

---
---

## Act II cross-check (final review)

| Rule | Check |
|---|---|
| Canon anchors | Dahrin: his own captivity and escape; the phrase unsaid. Asera: steadies, never fights, decides how far. Thennek: one R19 line; never fights; his way unshown. Maeryn: safehouse; disclosure optional and hers. Thalan: alive, dignified, consenting, names nobody, withholds what is taken. Kaelith: emberlight only. Yorven: a key and a door. The Speaker: warmth and omission; stays in office; lacks the endgame. Seralynd: doubts, her own words. Serix: sets dreams; his own unset visions. Ralenne: sincere, unaware. Saelia: suspects, stops the run. Vael: his own name, a sealed inquiry. Kaevren: intercepts and ledger. The Rat: a duct, a key, "same place". Calynne: a name in a record. |
| Evidence rule | R10 from Dahrin's account and the chamber; R11 from letters and the record; R12 from the record, the access book, the slip and the letter. The plates, the emberlight, the crowd's breath and the Rat's stillness are never proof. No defeated enemy speaks or carries a document. |
| Revelation limits | R10 and R11/R12 owned and paid here. R10 withholds what Thalan gives. R18 seeded (slate marks, rehearsal beat, steadying numbers; all optional or shown as practice). R19 seeded (Thennek; Thalan). R15, R16 untouched. R09 not re-told. No Titan word. |
| Reserved decisions | D-E2 (ruled 2026-11-15): Thalan freed with his voiced consent; one outcome; both approaches kept; no option to end or exploit. D-S1 (ruled 2026-11-15): idealist and manipulator, also dream-seeded; he never fights, confesses or lies outright and stays in office; swap notes removed. ED-3 (Iven Calder) not shown. D-EL (ruled 2026-11-15): one optional Elyndra consult (`ESS-D12`). Origin-neutral address; no "invaders", no direction; C07 untouched; D-C03 and D-C06 kept (no precursor name, no roster, no Volkhari count, no refuge). |
| No fail, no soft-lock | Plates never reset; wrong doors are dead ends; heat rooms and the record room can be waited or worked; the Smithing hook and the damper have time-cost alternatives; rehearsal windows re-run; every channel keeps progress; every choice completes. |
| No cutscenes | The stove flare, the emberlight, the frame, the fifth beat and both `S06` scenes play under the player camera. |
| Solo / co-op (CDR-6) | Every step, boss and reward solo; partner credit only from a partner's own active step; Thalan's scene, the letter-case, the record copy and both choices per player. |
| Defeat model (CDR-1) | Every enemy to 0 HP. Wraiths re-form only by lit braziers; the warden-frame's draw is a floor rule. No SX. No Volkhari, citizen, official or child targetable. |
| Ranged (CDR-2) | Viable in every fight; required in none; the Ranged hook has a climb. |
| Skills (CDR-4) | Smithing `[GD: mid]` (EH-M4) and Ranged `[GD: mid]` (EH-M5), each with a time-cost alternative. |
| Quest items | 2 (`EAC_sigil_stone`, `ESS_letters`); Emberholt running total 4 of 5. |
| Region flags | `EH_THALAN`, `EH_SPEAKER` set; `EH_TELLS`, `EH_HOLLOW_TRUTH`, `EH_CURRICULUM`, `EH_COLD_WARD` read. One writer each. |
| Geography | Bible POIs only (EP03, EP02, EP15, EP13, EP16, EP22, EP23, EP28, EP01) and dossier places, plus sub-sites inside them (Yorven's bypass end and the Rat's duct in the Underworks; the letter-room and the Magister's chambers in Speaker's Hall). Relative placement; MAP VERIFICATION REQUIRED on every place table. Thennek's side cut is never followed; nothing beyond the city is placed. |
| Terminology | No release wording. "Craft", never "magic". No "ghost", "undead", "curse". No NPC says "Remnant". |
| Runtime | One possible need (the sigil-stone reading a world volume) with a per-door inspect fallback. Nothing else new. |
| Size | Both quests complete; repetition with Act I avoided by referencing its conventions table instead of restating it. |

## Act II review log

| Review | Findings and revisions |
|---|---|
| Independent review, 2026-11-14 | Authored walkthrough of EH-M4 and EH-M5 against the brief, CDR-1 to CDR-6 (§3.7), the bible, Arcs, Revelation Ledger, dossier, Factions, character file, Part 4 ledger and the reviewed Act I package (nothing was played; no build exists). Every Act I flag read here exists in Act I under the same name with one writer (`EGH_SHEET_READ`, `EGH_STONE_HEARD`, `EGH_FLARECAP`, `EGH_WORK_ORDER`, `EEH_LEDGER_READ`, `ECW_SOB_HEARD` are required there, so always set). **High:** `[D-S1]` working layer showed the Speaker asking his patron for "clear" vigils, which would make him know his dreams are set (canon and Part 4 ledger: sincerely believed); the answer is cut, the letter thanks "the fire", Serix's `ESS-D8.32` reworded (§B14.1). **Medium:** Asera at dusk required the keep-watch stool before it existed (stool now from `S02` start); the tier-3 false door read *warm* with no vein, breaking the stone's own rule (now a hot conduit; convention and §A8.3 aligned); the second rehearsal could cut off before the three windows were read (runs now repeat until `ESS_RUN_READ`); Kaevren found a routing mark on the Act I work order whose document shows none, and asked to see a carry-state object that may no longer be held (stamp moved to the back; `ESS-D4.03`/`.04` and `ESS-I5`); `EAC-I7` "collar blanks... some are small" implied present child captives against Part 4 (Thalan the sole current captive), cut; the record's "not set" row put the Priestess on a night the access book does not list (moved to *K. less 23*); Maeryn's "We didn't go anywhere" located her people against World Truth C.3, trimmed to the canon line. **Low:** Thennek's gate gated on Asera and the key; freed Thalan rejoins at respawn; the damper climb given a niche and kept progress; exposed inquiry's overnight wait and branch logout points defined; co-op shared-enemy reads of per-player sectors and braziers logged as Sol presentation questions (Act I pattern); Yorven's post-quest bark matched the walkable gate; Maeryn's `.35`/`.36` timing; Dahrin's Act I-promised line restored verbatim; Ralenne's EH-M1 line `ESS-D3.02` tagged `[ALLOCATION]`; the epilogue tagged `[D-E2]`; one material prescription removed. **Renames:** none (Act II adds no named character; new place and prop names collide with nothing in 04_CONTENT_PRODUCTION or LORE). Checked and holding: R10 owned with two custodians and withheld; R11/R12 owned within ledger limits; R15/R16 untouched; R18/R19 seeds only; guided-sleeper list (the Priestess, Vael Trossen, *C. Vorr* as a written mark) matches canon secrets and bible §5.1; D-E2 both branches tagged, equal, consented, neither canon; FT-04/FT-05, D-C03, D-C06 kept; `[INITIATE]` absent; every enemy to 0 HP, no SX, no named character fought, no non-combatant targetable; ranged viable, never required; solo-completable. |
| Batch 4 encounter alignment review, 2026-11-15 | Applied Enemies file PE-6 (Deepbrand Hook and Shield bash 1.5 s; EAC-E3 inherits; the bash pending GD G1), PE-7 (EAC-E2 Lock-step 1.5 s, matching the Draw Sentinel) and PE-18 (EAC-E3: the warden-frame follows a target onto the rim or the gallery, so a ranged player on the gallery is answered; CDR-2 no unreachable safe spot; gallery access per Zones ML-12). No id, step, flag or line changed. |
| Emberholt character rulings, 2026-11-15 | **D-E2:** fixed liberation applied to EAC: aided branch removed (Beat 6 column, Beat 7 paragraph, epilogue line, A9.3 row, `EAC_ACCOUNT_PROMISED`, aided step and flag reads); `EAC-D8.60`–`.62` now one ask with Thalan's voiced consent to leaving and his line that it will not quiet what burns below; Smithing drift and two cool cycles kept; `EH_THALAN` = `freed` only; A14 items 1, 2, 11 resolved. **D-S1:** tags replaced; header, R11 row, B3, Beat 3 letters, Serix's account and B13 now show both halves (sincere conviction; knowing, self-serving manipulation through his letter-room; dream-seeded without absolution; no endgame); B14.1 swap notes resolved and removed. **D-EL:** optional Elyndra consult at EP20 during `S01`–`S05` (`ESS-D12`, flag `ESS_ELYNDRA_HEARD`, place note B5.6); not required. **ED-3:** tag note updated (Iven Calder; not shown in Act II). |
