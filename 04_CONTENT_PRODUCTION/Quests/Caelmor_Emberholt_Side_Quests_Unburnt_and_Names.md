# Emberholt Side Quests: The Unburnt; Names and Dreams

**Status (2026-11-15):** Authored production content for Creative Director review (Emberholt bible §12, Batch 3, first file). Five side-quest packages: the interconnected **Unburnt** questline (bible §7.1: **EST** *Stitches in the Lining*, **ETB** *Three Breaths*, **EMS** *The Memory-Stone*) and two standalone quests (bible §7.2: **ENW** *The Half-Name Wall*, **EGT** *Glassmoth's Tonic*). Everything marked **[NEW]** is authored here and is not canon until the Director promotes it (ED-19: promote nothing). **[CANON]** items come from the Emberholt dossier, the Emberholt character file, Factions and the Part 4 character ledger. **[PROPOSAL — DIRECTOR]** marks a consequential choice the content is built on. **[APPROVED — id]** cites an architecture ruling. No schema, production JSON or C# is created here. Emberholt is an internal production milestone of the complete game (CDR-3). None of these five quests has an encounter (bible §7.3); every step, choice and reward is completable by one player (CDR-6; §0.6).

**Controlled by:** `Caelmor_Emberholt_Narrative_Production_Bible.md` (author truth §2, decisions §3, places §4.2, cast and voice §5, slate §7.1 and §7.2, contract §7.3, Register §7.6, revelation map §8, flags §9.1, conventions §11). **Format:** mirrors `Caelmor_Mire_Side_Quests_Names_and_Lanterns.md` (per-quest summary card with the six §7.1 contract fields, places, beats, encounters and hazards, strange-moment spec, steps, flags and choices, rewards, failure, death, walk-away and co-op, integration, ledger, open decisions, review log). **Dialogue is inline** in each package (§x.12): nodes `<CODE>-D<n>.<nn>`, barks `<CODE>-B<n>.<nn>`, inspects `<CODE>-I<n>.<nn>`.

**Main-quest inputs read (checked 2026-11-15):** `Caelmor_Emberholt_Main_Act_I.md`, `_Act_II.md`, `_Act_III.md` and their dialogue files. Every main-line flag read here exists in those files under exactly the name and values used (§0.4). EH-M6 (`Caelmor_Emberholt_Main_Act_III.md`, "Inputs read") reads exactly one output of this file: **`EH_UNBURNT`** (kept / strained / unset) at `S08` attendance (bible §9.3 item 6). This file sets it as Act III reads it (§0.5).

**Decision tags used here.** D-E2 (Thalan's fate, ruled 2026-11-15: fixed liberation, `EH_THALAN = freed` only): Asera's one line in ETB that speaks of him (`ETB-D5.10`); the aid-in-place branch is removed. `[ED-12]` (Volkhari depiction, D-C06): every node where a Volkhari person decides what of their life is told. `[ED-16]` (the man from the fire roads): ENW's optional Mire echo. D-S1 (ruled 2026-11-15) needs no change here: no node asserts what the Speaker knows or intends, and none reduces him to only dream-fed. ED-3 (the initiate is Iven Calder, ruled 2026-11-15) does **not** apply: no node here shows, speaks or refers to the initiate's name. `[ALLOCATION]` does not apply.

---

## 0. Slate header

### 0.1 The five quests at a glance

| Code | Quest | Series (part) | Type | Unlock | Where | Core verb (primary first) | Gameplay identity | Strange / wonder moment | Sets |
|---|---|---|---|---|---|---|---|---|---|
| **EST** | Stitches in the Lining | Unburnt (1/3) | Settlement | EH-M2 Completed | Maeryn's shop (front, back room, yard); Brisa Teglan's tannery | **mend**, steady, keep | **Mould a brow-band to a knotted string and unpick a scorched lining; keep the counter while a lamp-keeper asks questions; then contain a flare in a room full of cloth** | As the youth steadies, the heat leaves the room at once and everyone's breath shows white, like winter | `EST_BOOK` (traced / unrecorded); `EST_KAELEN_NAMED` |
| **ETB** | Three Breaths | Unburnt (2/3) | Memory/lore | EST **and** EH-M4 Completed | The Molten Stair (Idra's lodging, the practice court); the Cooling House forge; Maeryn's back room | **practise**, compare, teach | **Forge and tune three chime bars, try an old exercise on a real student, take a torn page to the one person who knows the count, then teach a lesson by reading each child's flame** | Twenty flames at twenty heights, none in step, all steady; the court sounds like rain | `ETB_TAUGHT` (court / courtyard) |
| **EMS** | The Memory-Stone | Unburnt (3/3) | Memory/lore | ETB **and** EH-M3 Completed | Seredh's workroom (Maeryn's yard); the Ash Roads; the Cold Seam | **listen**, carry, decide | **Hold a carved account, carry it wet-wrapped along the Ash Roads without letting it warm, then cut it a seat in the one rock in Emberholt where no heat rises** | When the stone is seated, nothing in Emberholt breathes for three seconds: no vent, no tell, no wind | **`EH_UNBURNT`** (kept / strained) |
| **ENW** | The Half-Name Wall | Standalone (Register of the Unreturned) | Memory/lore | EH-M3 Completed | The Half-Name Wall (EP12); the old lower forge plaque (EP11); Imra's house, Cinderwall; the forge pay-house at the Emberforges (EP25) | **search**, match, decide | **Brush a wall clean, dress a dead man's tongs to raise his mark, take a rubbing, then search a pay-house binding for the week the forge fell** | The pay line after the night is in a steadier hand than the lines before it | **`EH_HALF_NAME`** (named / held) |
| **EGT** | Glassmoth's Tonic | Standalone (Dreamers) | Memory/lore | EH-M5 Completed | Glassmoth's stall (Cinderwall); Embergate yards; Selice's workshop; the Covenant lamp-house vigil hall | **ask**, compare, decide | **Brew a batch at a dream-seller's brazier, work beside three customers while they tell one dream, compare the three, then read the vigil book for that night** | In the vigil hall a woman asleep on a bench says the dream's words aloud | `EGT_TONIC` (told / sold) |

**Length targets:** EST 30–40 min; ETB 35–45; EMS 30–40; ENW 30–40; EGT 30–40. About 2.5–3.5 hours across the five.

**Combat share:** 0% in all five (bible §7.3); hazards only (EST's flare zone; EMS's vents and Working stretch).

### 0.2 Series spine and the two standalones

**The Unburnt: a lining, a count, a stone.** Three Volkhari individuals, each deciding what of their life is told (ED-12; bible §5.3 rule 6). The player is useful to them with their hands first and trusted second. No refuge is located, no number is stated, no community form is shown, and no Volkhari is ever an enemy or targetable (D-C06).

| Part | Whose trust | What the player makes or carries | What stays theirs | Spine line |
|---|---|---|---|---|
| EST | Maeryn Vall; Kaelen | A moulded brow-band; an unpicked lining; a shuttered window | Where Kaelen sleeps; whom he is looking for; Maeryn's heritage | *Some things go in the book. Some don't.* |
| ETB | Idra Callow; Asera | Three chime bars; a lesson | Where Asera's count comes from | *The third breath isn't held. It's given.* |
| EMS | Seredh Embercarver | A carved stone, wet-wrapped, to the cold | Who carved it; whose hands; what else he keeps | *Warm stone talks. Talk wears it.* |

**The Half-Name Wall** (ENW) is a Register of the Unreturned case resolved in Emberholt (bible §7.6): a civilian shift hand above the Hollow who was counted lost and walked out burned. **Glassmoth's Tonic** (EGT) is the Dreamers case that adds one more access pattern to R12 and shows, in the same quest, a dream that was nobody's but the dreamer's.

### 0.3 Unlock graph

```
EH-M2 The Ember in Every Hand (EEH_MENDING_BOOK, EEH_CLASS_DONE, EEH_LENS_READ, EH_CURRICULUM)
 └─► EST Stitches in the Lining ──┐
                                  ├─► ETB Three Breaths ──┐
 EH-M4 Ash-Stained Chains ────────┘   (EH_THALAN freed,   ├─► EMS The Memory-Stone ──► EH_UNBURNT
   (EAC_BREATH, EAC_MAERYN_SAID)       EAC_BREATH)        │     (EGH_STONE_HEARD)       └─► EH-M6 S08 attendance (item 6)
 EH-M3 The Hollow That Should Not Burn ───────────────────┘
   └─► ENW The Half-Name Wall (EH_HOLLOW_TRUTH, EGH_SHEET_READ, EDS09_SEEN; Mire MDS09_READ optional) ──► EH_HALF_NAME
 EH-M5 The Speaker's Smile (ESS_SLIP_SEEN, ESS_ACCESS_READ, ESS_RECORD_READ, ESS_SERIX_HEARD)
   └─► EGT Glassmoth's Tonic
```

Unlocks match the act packages exactly: Act I "Unlocks across Act I" (EST after EH-M2; ENW after EH-M3; EMS after EH-M3 with ETB), Act II "Unlocks across Act II" (ETB after EH-M4 with EST; EGT after EH-M5). Because ETB needs EH-M4, EMS is in practice reachable only after EH-M4; its listed gate stays as the bible states it. ENW, ETB, EMS and EGT all sit behind EH-M3's cross-region gate (ED-7), as the bible §7 notes. None of the five gates a milestone; a player who never touches this file has a complete path through EH-M1–EH-M6 (Act III reads `EH_UNBURNT` unset as "no line").

### 0.4 Flags set and read

**Region flags set** (bible §9.1; none created here):

| Flag | Values | Set by (one writer) | Read by | Effect |
|---|---|---|---|---|
| `EH_UNBURNT` | kept / strained | EMS: `kept` at `S04_seat` (`EMS-D5.20`), or at the post-completion mend (`EMS-D7.30`); `strained` at `S03_collector` (`EMS-D4.40`) | **EH-M6 `S08`** (§9.3 item 6, `EGA-D11.60`): kept, Maeryn Vall and Seredh Embercarver stand at the back; strained or unset, no line. Volkhari barks (§E.7 of Act III, request). | See EMS.9. |
| `EH_HALF_NAME` | named / held | ENW `S05_wall` (`ENW-D6.40` / `.50`) | Memorial props (EP11 plaque chalk, EP12 wall panel), EDS09 reading layer (Batch 3 discovery file, request: "one is chalked over later" shows with `named`); CV-M1 Register (request) | See ENW.9. |

**Main-line and cross-region flags read** (each exists in its owner's file exactly as written; all are optional variant reads unless marked as a gate):

| Flag / state | Owner (exact source) | Read here | Use |
|---|---|---|---|
| `emberholt.main.02_ember_in_every_hand` Completed | Act I §B4 | EST gate | Unlock. |
| `emberholt.main.03_hollow_that_should_not_burn` Completed | Act I §C4 | ENW gate; EMS gate (with ETB) | Unlock. |
| `emberholt.main.04_ash_stained_chains` Completed | Act II §A4 | ETB gate (with EST) | Unlock. |
| `emberholt.main.05_the_speakers_smile` Completed | Act II §B4 | EGT gate | Unlock. |
| `EEH_MENDING_BOOK` | Act I §B9.2 (EH-M2) | EST `EST-D2.12`, `EST-I1.02` | "Maeryn's mending book recurs" (Act I promise). Always set by EH-M2; the variant is safe. |
| `EEH_CLASS_DONE` | Act I §B9.2 | ETB `ETB-D1.03` | Idra: "You held the frame for Benno once." (Act I promise, verbatim). |
| `EEH_LENS_READ` | Act I §B9.2 | ETB `ETB-I2.02`, `ETB-D2.20` | "Idra's old primer and the old lenses" (Act I promise): the schedule number on the syllabus card. |
| `EH_CURRICULUM` = guild / evidence | Act I §B9.2 | ETB `S05`, `S06` (`ETB-D6`) | Guild: the guild's revised test can take Idra's older exercise (Act I §B9.3 promise). Evidence: the test stays this season; Theryn will not have it in her court. |
| `EAC_BREATH` = asera / waited | Act II §A9.2 | ETB `ETB-D5.04` / `.05` | Asera: "You kept my count once." (Act II promise, verbatim) with `asera`. |
| `EH_THALAN` = freed (D-E2, ruled 2026-11-15; one value) | Act II §A9.2 | ETB `ETB-D5.10` | Asera speaks of him as someone who walked (Act II §A9.3 promise). |
| `EAC_MAERYN_SAID` `[ED-12]` | Act II §A9.2 | EST `EST-D6.22`; ETB `ETB-D5.02` | Maeryn: "I told you once. I don't say it twice in a week." (Act II promise, verbatim). |
| `EGH_STONE_HEARD` | Act I §C9.2 (EH-M3) | EMS `EMS-D2.03` | Seredh: "You held one already." (Act I promise, verbatim). Always set by EH-M3. |
| `EH_HOLLOW_TRUTH` = told / kept | Act I §C9.2 | ENW offer (`ENW-D1.02` / `.03`), plaque state | Told: Imra has read the chalk *NOT A COLLAPSE* (Act I promise: "ENW: Imra Brask reads the chalk"). Kept: the plaque is clean. |
| `EGH_SHEET_READ` | Act I §C9.2 | ENW `ENW-D6.12` | The second sheet's *Shift above (lower forge): not ours. Not entered.* recalled. Always set by EH-M3. |
| `EDS09_SEEN` | Act I §A9.2 (EH-M1, optional) | ENW `ENW-I1.03` | "You have read this plaque before." |
| `ESS_SLIP_SEEN` | Act II §B9.2 | EGT `EGT-D1.12` | Glassmoth: "Slips? Somebody sells dreams on slips? Not me." (Act II promise, verbatim). |
| `ESS_ACCESS_READ` | Act II §B9.2 | EGT `EGT-I5.01` | "The access book recurs" (Act II promise): "You have read this book before." |
| `ESS_RECORD_READ` | Act II §B9.2 | EMS `EMS-D4.20` option; EGT `EGT-D8.27` / `.28` options | The rooms below recalled (inner line only); Serix asked about one night. |
| `ESS_SERIX_HEARD` | Act II §B9.2 | EGT `EGT-D8.01`–`.02` | "Serix recurs" (Act II promise). Always set by EH-M5. |
| `EH_SPEAKER` = challenged / exposed (D-S1, ruled 2026-11-15) reads only | Act II §B9.2 | EGT `EGT-B1.04` / `.05` (barks about the lamp-house mood) | Mood only; no line asserts what the Speaker knows. |
| `MDS09_READ` (Mire) | `Caelmor_Mire_Side_Quests_Settlements_and_Combat.md` MDS09 ("Reserved for the Emberholt bible as a possible read") | ENW `ENW-D6.30` option `[ED-16]` | Optional, unconfirmed echo. Never a hold, never identity, no route. |

No Lowmark or Thornfell flag is read. No `TH_*`, `MR_*`, `HS_*`, `UL_*` or `TAS_*` read.

**Quest-local flags** are listed with their writer and readers in each package's own flags table (EST.9, ETB.9, EMS.9, ENW.9, EGT.9); every one has a single writer in this file, and none is read outside it except `EST_BAND` (ESH, request), `ETB_TAUGHT` (EME09, request) and the quest-local reads between the Unburnt parts (`EST_ONDINE_MET`, `EST_CARD`, `EST_KAELEN_NAMED`, `EST_BOOK`). (Independent review, 2026-11-15: the duplicate table that stood here was cut; it had drifted from the package tables.)

### 0.5 How this file feeds EH-M6

Act III reads one output of this file, `EH_UNBURNT`, at `S08` attendance (§9.3 item 6; `EGA-D11.60`). `kept` (the stone seated in the Cold Seam, in EMS or its later mend): Maeryn Vall catches the player's eye and nods; Seredh does not speak. `strained` (given to the lamp-house and not yet mended) or unset (EMS never completed): no line. Nothing about either is said aloud (ED-12). The tally board reads the value when `S08` plays; a later `kept` changes nothing already seen.

### 0.6 Shared rules for all five packages

- **Quest items: none.** The Emberholt budget is full at five, all milestone items (Act III header: `EEH_ledger`, `EGH_roll`, `EAC_sigil_stone`, `ESS_letters`, `EGA_junction_book`). Carried things here (a knotted measuring string, a moulded band, quench cloths, a stock bar and three chime bars, a primer page copy, the memory-stone, a pair of tongs, a charcoal rubbing, a tray of tonic bottles) are **carry-state objects**: a held prop and a quest-state flag, not inventory, not droppable by a hit, returned to their source if the player logs out holding them. **Carry-state classes (Integration EI-CA-04; playability audit ES-03):** small documents and tokens are possession flags that never limit movement or attack and are kept across death and logout; only bulky loads (walk, cannot attack) return to their source. Records (the mending book, the primer, the syllabus card, the plaque, the wall, the pay-house binding, the vigil access book) are **read in place**. Reward tools are named functionally.
- **Dating.** No calendar date or year. Old entries are placed by the forge's own count ("Fire" weeks at the pay-house) or by event ("the week the lower forge fell"); present events by the presentation hour and "the next dusk".
- **No counts of the held** (D-C06; bible §2.2 withheld list). No text here states or implies how many Volkhari live, were held, died or escaped. No Volkhari refuge is placed or described. Kaelith is not seen, named or sought in these five quests. No line says how many died in the Hollow, the purges or the lower forge.
- **No precursor name, no roster** (D-C03). The lower forge's shift hands on the plaque and the pay list are civilians, never precursor members; their list is a memorial, not a roster of the precursor.
- **Evidence rule** (bible §11 item 3). Phenomena (a flare, a cold breath, a silence, a sleep-talker) never identify anyone, settle a claim or name the dead. Dreams are never evidence (ED-17); a dream is checked only against records (the vigil access book, the chamber record). A memory-stone is one account by one maker (Seredh's own terms; character file §45).
- **Steps** use `S00_…` ids scoped to the quest. **Completion events** are the Lowmark/Thornfell/Emberholt set: enter-volume, inspect, interaction-complete (channel, with kept progress), carry-deposit, dialogue-node-reached, *watch* (keep watch: advance the per-player presentation hour), *show* (use a carry-state object on an NPC or prop).
- **No quest can fail.** Inactive / Active / Completed only. Choices are outcome flags. Missed moments (a dusk visit, a fitting, a lesson) re-offer at the next presentation turn. Death respawns at the quest's named safe point with step and flags intact. Logout restores the last persisted step; channels in progress are discarded, completed segments persist; a carry-state object returns to its source and is handed back on the next talk. Walking away keeps the quest Active with the resume hook named in each package.
- **Heat** (bible §1.1, §9.2; ED-6). Every heat state a step needs is **quest-pinned** (the EI-HT-01 fallback), so nothing waits on the per-zone schedule. Tells, vent breath and cooling niches work as taught in EH-M1. No meter.
- **The EH-M6 frost (playability audit ES-01).** The EGA hour pin (`EGA_FROST`: dusk until EGA `S01`, night from `S02` to the `S06` keep watch) governs only EGA steps and the frost-variant areas (Cinderwall W1 to W4 and the upper Undercroft). A side step placed in those areas is held while `EGA_FROST` is set and resumes at `EGA_THAW_SEEN`, as EME01 and EME05 already do. Keep watch anywhere else advances this player's hour normally. Any other quest's hour pin applies only to keep watch inside that quest's own step volume (ES-06). EDI-3 (EH-M6 auto-activation) stays open.
- **Skills** (bible ED-11). Each quest has one real skill hook with a light requirement written as a Gameplay Designer placeholder (`~[GD: low]`) and a **time-cost alternative that never blocks access**: Leatherworking (EST), Smithing (ETB, ENW), Mining (EMS), Cooking (EGT). Skill XP is "actions only [GD]"; no lump quest XP (bible §11 item 6).
- **Containment, not combat** (ED-2 pattern). Kaelen's emberburst in EST is a hazard zone around a non-targetable person, ended by channelled containment parts. It cannot fail.
- **Co-op (CDR-6).** Every step, choice and reward is completable solo; nothing here has a co-op-only part. Each player has their own instance of every quest NPC scene (phased), every prop that a step reads (the band, the window, the stove, the chimes, the stone, the seat, the wall panel, the tongs, the binding, the brazier), and every choice. A partner's actions count toward their own step (Integration EI-CO-01). Where partners share an instance and do a shared task together (a containment part such as a cloth laid or the damper pulled), it credits every present partner whose own active step consumes it, so nobody repeats it (CDR-6 §3.7 item 2a; this supersedes the playability audit CO-05 wording for shared tasks); lessons, carries, readings, the seat and every choice stay each player's own. A partner never completes another player's step, takes a choice, sets a flag or receives a personal reward through another player's action. A partner leaving, disconnecting or being ahead never blocks anyone. Any shared visual state is a presentation fallback only (MI-CO-06 pattern) and never decides another player's walkable ground, interactions, credit or completion.
- **Address** (bible §5.3 rule 8). "Warden's hand" from everyone in these quests, since all five unlock after EH-M1. Origin-neutral (D-3). No one calls the player special, chosen or gifted.
- **Map.** Relative placement only. **MAP VERIFICATION REQUIRED** wherever geometry, distance, heat or water matters. No route or direction to another region is stated. The Mire is named in ENW only as the place where the player read a book; nothing says how far, which way, or by what road.

### 0.7 Distinctness check

| Quest | What the player physically does | Not the same as |
|---|---|---|
| EST | Unpicks a scorched lining; sets pegs on a carving block to a knotted string and wet-moulds a hide band; keeps a counter through a conversation; shutters, smothers, damps and vents a room around a flaring youth | EEH `S03` (Tavi's flare: a classroom, a damper, a bell count with a teacher; here a shop, cloth on fire, a window to hide, nobody who knows the count) |
| ETB | Forges and rings three chime bars; reads a primer against a syllabus card; tries an exercise on one student; brings a torn page to a ritualist; teaches a lesson by reading flames as tells | EEH `S01` (assisting someone else's lesson); EH-M5 (a crowd breathing on one beat; here a class breathing on twenty) |
| EMS | Holds a stone; wet-wraps it; carries it two-handed down a road of vents without climbing or running; cuts a seat in cold rock or chisels it slowly; decides who keeps it | EH-M3 (Seredh's stone heard indoors as evidence; here a stone carried as a trust) |
| ENW | Brushes soot off a wall panel; dresses tongs at a forge (or soaks and scrubs); takes a rubbing; climbs a pay-house ladder and pages a binding by forge weeks; matches a mark | EH-M3 (a precursor record read for the Hollow; here a civilian pay list read for one man) |
| EGT | Reduces a syrup at a brazier; carries crates, holds a glass blank and trims wicks while three people talk; lays three accounts side by side; reads a chained book | EH-M5 (the Speaker's case proved by a record and letters; here three ordinary sleepers, and one dream that was nobody's but the dreamer's) |

### 0.8 Ids and names used

Content ids (suggested; the Schema & Content Engineer owns naming): `emberholt.side.stitches_in_the_lining`, `emberholt.side.three_breaths`, `emberholt.side.the_memory_stone`, `emberholt.side.the_half_name_wall`, `emberholt.side.glassmoths_tonic`.

Bible cast used (bible §5.1, §5.2): Maeryn Vall, Kaelen Veyr'un, Brisa Teglan, Idra Callow, Theryn Dalewright, Selice Morra, Asera of the Three Breaths, Seredh Embercarver, Imra Brask, Corm Brask (never met, never speaks), Glassmoth (Jatha "Glassmoth" Nirel [CANON], character file §32), Serix Arden. Act I minor: Benno (EEH student), Tavi Ostry (bark only). Role names: students, a pay clerk's apprentice, vigil-goers.

New minor names [NEW] (each grepped across `04_CONTENT_PRODUCTION`, `LORE` and `00_ADMIN` on 2026-11-15; no whole-word hits and no near-duplicate in the same voice set): **Ondine Thursk** (Covenant lamp-keeper; the grey visitor of EEH, now named; EST, EMS, EGT); **Perrin Sedgwick** (forge pay-house clerk at the Emberforges; ENW); **Mattea Orsk** (gate-yard porter), **Dorrit Vane** (Selice Morra's apprentice), **Sabeth Tamber** (Cinderwall lamp-mender) (EGT customers). Rejected during the check: *Gessa* (Jessa Ostry), *Corl* (Corm Brask), *Callis* (Idra Callow), *Lume* (Initiate-Lumen title), *Wrenley* (Mire Abel Wren), *Ysane* (Mire Ysolde). New sub-sites [NEW]: Maeryn's yard and Seredh's workroom (a lean-to in it), Idra's lodging, the forge pay-house, Glassmoth's stall under the slag-lane arch. The primer *Grounding for the Young Hand* [NEW].

---

# Series: The Unburnt

---

## EST — Stitches in the Lining

### EST.1 Hook

**Remember:** breath showing white in a room that was on fire a moment before. **Want next:** to know what the old count was that Idra keeps half-remembering, and who still keeps it.

### EST.2 Selection record and canon grounding

Rejected: Kaelen leading the player to his sibling or a refuge (bible §5.1; D-C06); the Covenant visitor as a villain to fight or expel (lamp-keepers are never targetable; their steadying is sincere, Act I §B9).

| Element | Source | Status |
|---|---|---|
| Maeryn Vall: Volkhari seamstress, ember-resistant fabrics, ember-thread weaving that conceals minor ember traces, ward-stitching, a long-standing safehouse; her heritage is her own to disclose | Character file §48; bible §5.1 | [CANON]; ED-12 |
| Kaelen Veyr'un: hooded youth hiding near the city; ember freckles that glow when upset; horn ridges under hoods or headbands; anger at Emberholt; emberburst under stress; dreams of something calling from below | Character file §43; bible §5.1 | [CANON]; dreams never evidence (R19 seed only); his war presence is **not** used (Part 4 ledger: must be checked before use) |
| The grey visitor at Maeryn's window (EEH) | Act I §B6 Beat 2, §B8.2 ("seeded for EST") | [NEW, Act I] |
| Vigil guidance: the lamp-house takes students and young people for "steadying" | Act I §B6 Beat 5; Act II §B5.1 (grey cloaks of the lamp-keepers) | [NEW, acts] |
| Maeryn's mending book: pencil outlines of scorched mitts | Act I §B6 Beat 2 (`EEH_MENDING_BOOK`) | [NEW, Act I] |
| Brisa Teglan: "Hide first, heat second." | Bible §5.2; Act I §B5.1 | [NEW, bible] |
| The cold breath | This package | [NEW]; never explained |

### EST.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `emberholt.side.stitches_in_the_lining` |
| Series | *The Unburnt*, part 1 of 3 |
| Type | Settlement |
| Unlock | `emberholt.main.02_ember_in_every_hand` Completed. Maeryn is at her counter on the player's next visit to the Cinderweave Quarter (`EST-D1`); her bark `EST-B1.01` plays as the player passes the shop. |
| Length | 30–40 minutes |
| Combat share | 0% |
| Skills | **Leatherworking ~[GD: low]**: wet-mould a hide brow-band on Brisa's carving block to Maeryn's knotted string. Time-cost alternative: Brisa moulds it overnight (keep watch to morning; `EST_BAND = brisa`). The lining unpick is a channel with no skill gate. |
| Choice | Whether Kaelen's sleeve is traced in Maeryn's mending book (`EST_BOOK` = traced / unrecorded). Minor: the lamp-keeper's card (`EST_CARD` = taken / refused). |
| Outputs | `EST_BOOK`; `EST_KAELEN_NAMED`; ETB (with EH-M4) |
| **Anchor** (contract) | Volkhari individuals: Maeryn Vall and Kaelen. |
| **World-truth row** (contract) | H03 (the Volkhari as a people living on, individually, under a public belief that they "abandoned the city"). |
| **Revelation role** (contract) | None. One line carries the canon R19 shadow (Kaelen's dream of being called from below), unexplained and never evidence. Not one of bible §8.2's listed R19 seeds. |
| **Recurring evidence** (contract) | Maeryn's mending book (recurs from EEH; read in place at her counter). No new custodian; nothing here is proved. |
| **State compliance** (contract) | Inactive → Active on `EST-D1` accept; Completed on `EST-D7` end. No step can fail: the flare containment cannot fail, the band has an overnight alternative, the fitting re-offers each dusk. `EST_BOOK` traced or unrecorded; both honest. Resume hook at Maeryn's counter (`EST-B1.02`). |
| **Combat compliance** (contract) | None. No encounter. Kaelen's emberburst is a hazard zone around a non-targetable person, ended by channelled containment (ED-2 pattern); Ondine Thursk, Maeryn and Kaelen are never targetable. **CDR-6 solo test:** every part (unpick, mould, counter, four containment parts, the book) is done by one player in sequence; nothing needs a second player; no reward depends on co-op. |

### EST.4 The places

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Maeryn's shop, front** (EP03, C2 in Act I) | Offer; the counter (`S03`) | As EEH: bolts of ember-resistant cloth, a counter with the **mending book** by a pincushion, the keep-watch stool, a front **window** on the street with a wooden **shutter** folded back. A card rack by the door for customers' orders. |
| **B. The back room** (EP03, Act II C5) | The fitting; the flare (`S01`, `S04`) | Through the curtain: a cutting table, a small iron **stove** with a **damper** lever, shelves of **cloth bolts** (some ember-thread, some plain), a mirror, the "third chair" that wobbles (Act II). A **yard door** with an iron latch. A **quench bucket** by the stove. |
| **C. Maeryn's yard** [NEW sub-site] | The yard door's outside; a **trough** and a line of drying cloth | A small walled yard behind the shop with a water **trough** and a lean-to (Seredh's workroom in EMS). A gate onto a back lane. **MAP VERIFICATION REQUIRED.** |
| **D. Brisa Teglan's tannery** (EP03, C1 in Act I) | The band (`S02`) | Hides on frames over a low ember bed, a soaking **tank**, a rack of **carving blocks** for moulded work (helmet brows, saddle horns, bucket rims), a stitching horse. Her sign: *HIDE FIRST, HEAT SECOND.* |

### EST.5 Player-facing sequence

Exact wording lives in EST.12; beats cite node ids.

**Beat 0: The counter (`S00_offer`).** *Objective: Speak to Maeryn Vall.* `EST-D1`. Maeryn has "a back-door customer" who needs a fitting and does not like people, and wants the warden's hand on the counter stool at dusk. Accept: Active; journal *Mind Maeryn's counter at dusk.* Not now: re-offer by `EST-B1.01`.

**Beat 1: The back door (`S01_back_door`).** *Objective: Wait at Maeryn's counter at dusk.* Keep watch on the stool if it is not dusk. Maeryn chooses to take the player through the curtain (`EST-D2.01`). The **youth** stands in the yard doorway, hood up, sleeves over his hands, and does not want the player there (`EST-D2`). **Inspect** his sleeves (required, `EST-I1.01`; with `EEH_MENDING_BOOK`, `EST-I1.02` adds the children's palms): scorched through at the cuffs **from the inside**, in the shape of fingers. Maeryn measures his brow under his hood with a **knotted string** (the player sees only the string) and hands it over (carry-state) with his old sleeves for unpicking. He leaves by the yard. Sets `EST_SLEEVES_SEEN`.

**Beat 2: The band and the lining (`S02_band`).** *Objective: Make the band; unpick the old lining.* Either order.
- **The band**, at Brisa's tannery (`EST-D3`). **Option A (skill): Leatherworking ~[GD: low].** (1) **Set the pegs:** a brass peg at each knot as the string lies round a plain carving block (three place interactions; a coloured thread marks the string's start, so it goes round one way only). (2) **Cut** a blank from soaked hide (one interaction). (3) **Mould** the wet blank over block and pegs and bind it (3-segment channel, ~4 s each; segments persist). (4) **Dry** it by the ember bed (a short wait). The band has three soft rises where the pegs were. `EST_BAND = self`. **Option B (time-cost):** Brisa keeps the string; keep watch to morning at her bench. `EST_BAND = brisa`.
- **The lining**, at Maeryn's cutting table: **unpick** the scorched ember-thread (3-segment channel, ~4 s each; segments persist). The thread is black at the cuffs and gold above the elbow (`EST-D2.30`). No skill gate.
Completes on carry-deposit of band and sleeves on Maeryn's table. She lines both overnight; the fitting is the next dusk.

**Beat 3: The counter (`S03_counter`).** *Objective: Keep the counter while Maeryn does the fitting.* Next dusk. Maeryn draws the curtain on the fitting (`EST-D4.01`). After ~10 s the street bell: **Ondine Thursk**, grey-cloaked, a lamp-keeper's lantern on her belt (`EST-D4.10`). A young man in a hood was seen flaring by the dye yards; the lamp-house takes young people who flare "for steadying"; has the shop sold long sleeves to such a youth? Every answer is safe: no option points at the back room and none gives him away (ED-12). She glances at the curtain once and does not go to it. She offers a **card** (`EST_CARD` = taken, onto the counter rack; or refused, and she leaves it anyway). She buys grey thread and goes. Sets `EST_ONDINE_MET`. Completes on the street door closing.

**Beat 4: The flare (`S04_flare`), the set piece.** *Objective: Steady the back room.* The curtain stands out on a gust of heat. The youth has his hood down and his hands flat on the cutting table; his ember freckles are lit and the bolts behind him smoke (`EST-D5.01`). Maeryn is between him and the stove, talking low. **Kaelen's emberburst** (ED-2 pattern): a hazard zone ~3 paces round him (periodic heat damage [GD: light]; shimmer; the stove hood tell red and crazed; three bolts smouldering). Nobody in the room is targetable. **Containment**, four parts in any order, progress kept; each part shrinks the zone by a quarter and cools the tell a step:
1. **Shutter the front window** (front room, outside the zone; one interaction). The glow is hidden from the street. Sets `EST_SHUTTERED`.
2. **Smother the bolts:** dip a quench cloth from the yard line in the trough (carry-state: wet) and lay it on a bolt (~2 s). Three bolts, three cloths. A dry cloth prompts *Wet it first*.
3. **Damp the stove:** pull the damper shut (2-segment channel, ~3 s each, at the zone edge).
4. **Open the yard door:** the latch is too hot to hold (`EST-I3.03`); wrap a wet cloth round it and lift. Cold air comes in.
Maeryn talks to him throughout (`EST-D5.10`–`.16`): her hands, the thread, the weather, never his name. After the fourth part Kaelen speaks (`EST-D5.20`); any answer, or silence, works (`.21`–`.24`). He breathes out: **the strange moment** (EST.7). Completes on `EST-D5.40`.

**Beat 5: The book (`S05_book`).** *Objective: Decide with Maeryn what goes in her book.* `EST-D6`. Kaelen puts the band on (his hands, his choice; the player sees only that it sits) and tries a sleeve; it does not smoke. Maeryn opens her **mending book** at a clean page and lays his old sleeve on it: everything scorched that comes through the shop, she draws. She looks at the player, not at him; Kaelen will not choose (`EST-D6.21`). With `EST_CARD = taken`, he has seen the card on the rack (`EST-D6.10`). The choice (`EST_BOOK`):
- **Trace it.** Maeryn draws round the cuff, shades the scorch and writes no name: *back door; cuff; inside.* It sits beside the children's palms.
- **Leave it out.** She closes the book. He will have to come in himself for every pair.
At the yard door he gives his first name (`EST-D6.30`; `EST_KAELEN_NAMED`) and goes. Completes on `EST-D7`.

### EST.6 Encounters and hazards

**Encounters:** none. **Hazards:** Kaelen's flare zone (`S04`): periodic heat damage [GD: light], radius ~3 paces shrinking by a quarter per part; the zone never moves; it ends on the fourth part. The stove's hood tell shows the zone's state (red and crazed → amber → clear). Standing in the yard (outside) or the front room costs nothing.

### EST.7 The strange moment: breath like winter (Beat 4)

| Time | Element | Spec |
|---|---|---|
| 0 s | **He breathes out** | After `EST-D5.20`–`.24`. Kaelen's freckles go dark, all at once. |
| 0–1 s | **The heat goes** | The heat shimmer in the room stops. The stove tell goes clear. The yard door's draught stops moving the curtain. |
| 1–5 s | **White breath** | Maeryn's breath, Kaelen's and the player character's show white in the air, like a winter morning, three or four breaths each. Frost does **not** form; nothing is cold to the touch; the room's temperature is not shown as anything (no meter). |
| 5 s | **Back** | The breath stops showing. The room is an ordinary back room in the evening. |
| After | **Kaelen** | `EST-D5.31`: "Sorry. It goes somewhere." Maeryn says nothing about it. If asked (`EST-D5.32`), Maeryn: "I sew." |
| What it means | | Nothing is explained, in EST or later. It is not evidence and identifies nobody. The Cold Seam (EMS) is also a place where no heat rises; nothing connects them in any text. |

Sets `EST_COLD_BREATH` (read by nothing; deliberately).

### EST.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Speak to Maeryn Vall. | `EST-D1` accept | Yes |
| `S01_back_door` | Wait at Maeryn's counter at dusk. | Dusk **and** `EST-I1.01` inspect **and** `EST-D2.20` (string given) | Yes |
| `S02_band` | Make the band; unpick the old lining. | (`mould_band` 3 segments **or** keep watch at the tannery to morning) **and** `unpick_lining` 3 segments **and** carry-deposit of band + sleeves on Maeryn's table | Yes |
| `S03_counter` | Keep the counter while Maeryn does the fitting. | Next dusk **and** `EST-D4` card answer **and** street-door close event | Yes |
| `S04_flare` | Steady the back room. | `shutter_window` **and** 3 × `smother_bolt` **and** `damp_stove` **and** `open_yard_door` **and** `EST-D5.40` | Yes |
| `S05_book` | Decide with Maeryn what goes in her book. | `EST-D6` choice **and** `EST-D7` end | Yes (→ Completed) |

### EST.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `EST_SLEEVES_SEEN` | `S01` inspect | `EST-D3.02` |
| `EST_BAND` = self / brisa | `S02` | `EST-D6.04`; ESH (request: Brisa bark, "Your band held its shape. Mine always do.") |
| `EST_ONDINE_MET` | `S03` | EMS `EMS-D4.01`; EGT `EGT-D7.03` |
| `EST_CARD` = taken / refused | `EST-D4.20` / `.22` | `EST-D6.10`; EMS `EMS-D4.02` |
| `EST_SHUTTERED` | Containment part 1 | `EST-D5.40` |
| `EST_COLD_BREATH` | `est.cold_breath` event | None (deliberately) |
| `EST_KAELEN_NAMED` | `EST-D6.30` | ETB `ETB-D5.03` |
| **`EST_BOOK` = traced / unrecorded** | `EST-D6.40` / `.50` | Maeryn barks (`EST-B2.05` / `.06`); ETB `ETB-B1.03` |

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Trace it** | A page in the mending book: a cuff, scorched from inside, *back door*. | The book is a record that could be read by anyone who reads it; Kaelen is uneasy (`EST-D6.42`). | Maeryn's book now holds an adult's scorch beside the children's (ETB: Idra, shown the book by Maeryn, `ETB-B1.03`). No later content reads the page as evidence. |
| **Leave it out** | No page. | Kaelen has to come to the shop in person for every fitting; Maeryn has nothing to size from. | Maeryn: "He'll come. He'll complain." (`EST-B2.06`). |

Neither choice hurts Kaelen or helps Ondine. No later quest makes either the wrong one.

### EST.10 Rewards, failure, death, walk-away, co-op

| Reward | Type | Notes |
|---|---|---|
| **The yard way** | Access | Maeryn's yard gate opens from the back lane as a route into the shop's back room (used again by ETB and EMS). |
| **Spare ember-thread** | Tool (functional) | A spool of the good thread from the unpicking, for repairs to the player's own heat gear [GD: economy pass names and stats it, or it is flavour]. |
| Small payment | Currency | Maeryn pays for a hand at the counter [GD]. |
| Skill XP | Actions only [GD] | Leatherworking (Option A only). |
| *Three Breaths* | Story | With EH-M4 Completed. Maeryn's bark `EST-B2.07`: Idra Callow has been in asking for "somebody who knows old counts". |

| Situation | Handling |
|---|---|
| No Leatherworking | Brisa moulds the band overnight (time only). |
| A peg set in the wrong place | The string will not lie round the block; the peg can be lifted and reset. No penalty. |
| A dry cloth on a bolt | Prompt *Wet it first*; nothing happens. |
| Death in the flare zone | Respawn on the counter stool; completed parts kept; the zone stays at its current size; Maeryn has Kaelen in the yard doorway. |
| Missing the fitting | The fitting re-offers each dusk. Ondine comes in each time until `S03` completes. |
| Walking away | Stays Active. The string and the band (carry-state) return to Maeryn's table if the player logs out holding them; Maeryn hands them back. Resume: `EST-B1.02`. |
| Fail state | None. |
| Co-op (CDR-6) | Per §0.6. A partner leaving mid-flare leaves the other's parts as they were. |

### EST.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| Peg-and-string block (three placement points validated against the string) | Systems | Three fixed sockets on the block; the string prop snaps round them when all three pegs are placed. **Fallback:** the pegs auto-place on interact; the channel stays. |
| Wet/dry carry-state cloth | Systems | A carry-state with two values; the trough toggles it. Standard. |
| Flare zone shrinking by parts | Systems | EEH `S03` containment pattern (bible §11.1 channelled interactions; zone radius by completed-part count). Reused, not new. |
| `est.cold_breath` presentation event | Art/VFX | A short breath-fog effect on three characters; no environment change. |
| Per-player mending book page | Systems | Per-player prop text (traced / blank). |

No new runtime system.

**Mystery ledger.**

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Who Kaelen is** | Kaelith's sibling, a Volkhari youth hiding near the city (character file §43). | "A hooded lad who flares; the lamp-house will steady him." | His sleeves; the flare; his name. | He is a danger to the quarter; he is Kaelith. | His family name; whom he is looking for; where he sleeps. | None in Emberholt (his story continues in later content, request). |
| **The cold breath** | Unknown. | — | — | It proves something about Volkhari. | Everything. **Never explained.** | None. |

**Open decisions.**
1. **Kaelen's family name** `[ED-12]`. He says only "Kaelen". The journal records "Kaelen". The bible names him Kaelen Veyr'un; saying the family name aloud would tie him in the player's mind to the Unburnt Boy legend. Recommendation: keep it unsaid in Emberholt. If the Director wants it said, add one clause to `EST-D6.30`.
2. **The grey visitor named.** EEH kept the visitor nameless. This package names her (Ondine Thursk) so EST, EMS and EGT share one sincere lamp-keeper. If the Director prefers a role only, replace the name with LAMP-KEEPER in all three; the only texts that carry the name are the card (`EST-I3.01`, "Ask for Ondine" → "Ask at the hall") and the receipt stub (EMS Beat 3, "O. Thursk" → a lamp-keeper's mark). Checked against Act I (independent review, 2026-11-15): EEH's grey visitor is unnamed, non-interactive and "seeded for EST" (Act I §B, visitor row: "who and why" withheld), so naming her here contradicts nothing; Act II's grey cloaks of the lamp-keepers match.
3. **No Kaelith option.** A player who has done EH-M4 has seen emberlight above the chamber; there is deliberately **no** option to tell Kaelen about it (bible §5.1: he is never told where Kaelith is; the player does not know where either).

| Review finding | Revision |
|---|---|
| Draft let Maeryn name Kaelen to Ondine to send her away. | Cut. Maeryn never names him; the player has no option that points to the back room (ED-12). |
| Draft had Maeryn's stitches glow on her own headwrap during the flare. | Cut: it would disclose her heritage without her choice (ED-12). The strange moment is now breath, not light. |
| Draft used Kaelen's presence at the Hollow (character file). | Cut: the Part 4 ledger says his individual war presence must be checked before use. He says nothing of the war. |
| Draft containment repeated EEH's bell count. | Replaced by four physical parts (window, cloth, damper, door); nobody in the room knows a count (that is ETB's question). |

### EST.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Maeryn Vall** [CANON] | Her customers, her thread, the yard way; that the grey visitor has started to call. | What the Covenant wants with young people beyond "steadying". | Warm, quick, quietly witty; braver than she sounds. Talks with her hands busy. Never says what she is (ED-12). |
| **Kaelen** [CANON] | His own body, his anger, the city's outskirts. | Where his sibling is. | Short. Angry at Emberholt and allowed to be. Protective, proud, frightened under it. Never asks for help; accepts it sideways. |
| **Brisa Teglan** [NEW, bible] | Hide. | Who the band is for. | Blunt. "Hide first, heat second." |
| **Ondine Thursk** [NEW], Covenant lamp-keeper | That a young man was seen flaring; the lamp-house's steadying. | Anything about Volkhari; anything about Hearthveil's rooms below. | Kind, slow, a little sad; believes the lamp-house helps. Never threatens. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| EST-B1.01 | Maeryn | Available, player passes the shop | *"Warden's hand! Come in. Not for a hem. Well. Partly for a hem."* |
| EST-B1.02 | Maeryn | Active, returns | *"Dusk. The stool. If anyone asks, you're waiting for a hem."* |
| EST-B1.03 | Brisa | `S02`, band on the rack (`brisa`) | *"Your band. Three bumps in it. I didn't ask."* |
| EST-B2.01 | Maeryn | `S02`, lining not unpicked | *"The sleeves are on the table. Gold thread up top. Black at the cuffs. Keep the gold."* |
| EST-B2.02 | Ondine | Seen in the quarter after `S03` | *"Peace on your flame, warden's hand."* |
| EST-B2.03 | Maeryn | After a respawn in `S04` | *"He's in the doorway. He's breathing. Go on. You were doing the cloths."* |
| EST-B2.05 | Maeryn | Completed, `traced` | *"I look at that page more than I should. Same as the little ones."* |
| EST-B2.06 | Maeryn | Completed, `unrecorded` | *"He'll come. He'll complain. He'll come."* |
| EST-B2.07 | Maeryn | Completed, EH-M4 Completed | *"Idra Callow was in. Asking for somebody who knows old counts. I said I sew."* |

#### Nodes

```
EST-D1 (Maeryn's counter; S00)
EST-D1.01 MAERYN: (threading; bright) "Warden's hand. You've a counter face today. Good. I need one."
EST-D1.02 MAERYN: "I've a customer who uses the back door. He needs a fitting. He doesn't like people."
EST-D1.03 MAERYN: "At dusk, sit on that stool. If anyone comes in, you're waiting for a hem. If nobody comes in, you're waiting for a hem."
  > "I'll mind the counter."                       → EST-D1.10
  > "Who is he?"                                   → EST-D1.20
  > "Not now."                                     → EST-D1.40
EST-D1.10 MAERYN: "Dusk. Bring patience. He's got none."   {quest Active; event: S00}
EST-D1.20 MAERYN: "A customer." (beat) "One who needs sleeves that don't burn. That's all I ask of customers."   → EST-D1.03 options
EST-D1.40 MAERYN: "Dusk comes every day. So does he."   {quest stays Inactive; re-offer EST-B1.01}
```

```
EST-D2 (back room, at dusk; S01, S02)
EST-D2.01 MAERYN: (lifts the curtain herself) "Through. Mind the third chair."
EST-D2.02 YOUTH: (in the yard doorway; hood up; sleeves over his hands; steps back) "You said nobody."
EST-D2.03 MAERYN: "I said nobody who talks." (beat) "This one doesn't, much."
EST-D2.04 YOUTH: (to the player) "Look at the floor, then."
  > (Look at the floor.)                           → EST-D2.10
  > "I'm only here for the counter."               → EST-D2.10
EST-D2.10 MAERYN: "Sleeves." (he holds his arms out; she turns the cuffs back)   {prompt: inspect sleeves, EST-I1.01}
EST-D2.12 [EEH_MENDING_BOOK] MAERYN: (to the player, low) "You've seen my book. You know where I've seen this before."
EST-D2.14 YOUTH: "It's the lining. It's cheap."
EST-D2.15 MAERYN: "It's my lining. It isn't cheap." (beat) "It burns from inside. Hold still."
EST-D2.16 (Maeryn measures round his brow with a knotted string under his hood. He holds the hood so the player sees only the string.)
EST-D2.20 MAERYN: (hands the player the string and the old sleeves) "A band, moulded to that. Hide, so it holds its shape. Brisa has blocks. I'll line it."   {carry-state: string; sleeves to the cutting table}
EST-D2.22 YOUTH: (at the yard door) "Tomorrow. Dusk. If the room's empty."
EST-D2.23 MAERYN: "It won't be. It'll have this one in it." (he goes)   {event: S01}
EST-D2.30 [unpick channel complete] MAERYN: "Keep the good thread. Thread doesn't care who wore it."
```

```
EST-D3 (Brisa's tannery; S02)
EST-D3.01 BRISA: (takes the string; runs it through her fingers) "Three knots. Somebody's measured round something."
EST-D3.02 [EST_SLEEVES_SEEN] BRISA: "Vall's work. She measures right. I won't ask."
EST-D3.03 BRISA: "Pegs on the block where the knots sit. Wet hide over. Bind it. Let it dry by the bed. Hide first, heat second."
  > "I'll mould it."                               → EST-D3.10
  > "Leave it with you?"                           → EST-D3.15
EST-D3.10 BRISA: "Coloured thread's the start. It only goes round one way."   {Leatherworking: set pegs, cut, mould; EST_BAND = self}
EST-D3.12 [mould complete] BRISA: (turns the band over; three soft rises in it) "That'll sit. Whatever it's sitting on."
EST-D3.15 BRISA: "Morning. Don't hover."   {keep watch to morning; EST_BAND = brisa}
EST-D3.20 BRISA: (either way, handing it over) "Tell Vall it's dry. Tell her I didn't ask."
```

```
EST-D4 (the counter, next dusk; S03)
EST-D4.01 MAERYN: (draws the curtain behind her; through it) "Counter's yours."
EST-D4.10 ONDINE: (the street bell; grey cloak; a small lamp on her belt) "Peace on your flame. Is the seamstress in?"
EST-D4.11 ONDINE: "No matter. Perhaps you can help." (beat) "A young man in a hood was seen flaring by the dye yards, two nights since. Badly. The lamp-house takes young people who flare. For steadying. Before they hurt someone. Or themselves."
EST-D4.12 ONDINE: "Has a young man in a hood bought long sleeves here? Or a headwrap?"
  > "I'm waiting for a hem."                                 → EST-D4.14
  > "Plenty of people buy sleeves in this quarter."          → EST-D4.14
  > "What happens to them at the lamp-house?"                → EST-D4.16
EST-D4.14 ONDINE: (smiles) "That's fair." (she glances once at the curtain) "A fitting? I won't intrude."   → EST-D4.18
EST-D4.16 ONDINE: "They sleep with a lamp-keeper by them. They breathe slow. They wake steadier. I've seen it do good." (beat) "I've seen it."   → EST-D4.18
EST-D4.18 ONDINE: (holds out a card: a lamp drawn on it, and the lamp-house's door mark) "If he comes in. Or anyone like him."
  > (Take the card.)                               → EST-D4.20
  > "Keep it. I don't need it."                     → EST-D4.22
EST-D4.20 ONDINE: "Thank you." (the player sets it on the rack)   {EST_CARD = taken}   → EST-D4.24
EST-D4.22 ONDINE: (leaves it on the counter anyway) "In case."   {EST_CARD = refused}   → EST-D4.24
EST-D4.24 ONDINE: (buys a spool of grey thread; pays exactly) "Peace on your flame." (the bell; she is gone)   {EST_ONDINE_MET; event: S03}
```

```
EST-D5 (the back room; S04)
EST-D5.01 (The curtain stands out on a gust of heat. Behind it the youth has his hood down and his hands flat on the cutting table. The freckles on his face and arms are lit like coals. The bolts on the shelf behind him are smoking.)
EST-D5.02 MAERYN: (between him and the stove; not looking at the player) "Window first. Then cloths. Wet ones. The yard."
EST-D5.10 MAERYN: (ambient, low, as the player works) "I'm putting the blue down. It's ugly anyway."
EST-D5.11 MAERYN: "Gold thread from your old sleeves. Good thread. I'm keeping it."
EST-D5.12 MAERYN: "It's going to rain. It always rains after a hot week."
EST-D5.13 MAERYN: "That chair still wobbles. Everybody's does."
EST-D5.14 MAERYN: "Hands on the table. That's right. The table's had worse."
EST-D5.16 MAERYN: "Nobody's coming in. Nobody's looking. The shutter's down."   {plays after EST_SHUTTERED}
EST-D5.20 YOUTH: (when the fourth part is done; through his teeth) "She asked for me. By my sleeves. Your city counts the ones who burn."
  > "She thinks she's helping."                    → EST-D5.30
  > "I didn't tell her anything."                   → EST-D5.30
  > "It's not my city."                            → EST-D5.30
  > (Say nothing.)                                  → EST-D5.30
EST-D5.30 (He breathes out. The light goes out of his skin all at once. The heat leaves the room, and for a few breaths everyone's breath shows white, like winter.)   {event: est.cold_breath}
EST-D5.31 YOUTH: (watching his own breath) "Sorry. It goes somewhere."
EST-D5.32 [player asks, optional] "Where does it go?"  MAERYN: "I sew."
EST-D5.40 MAERYN: (sits down on the wobbling chair, hard) "Well." [EST_SHUTTERED] "Nobody saw a thing from the street. That's something."   {event: S04}
```

```
EST-D6 (the back room; S05)
EST-D6.01 (He puts the band on himself, under the hood, and pulls one new sleeve on. It does not smoke.)
EST-D6.02 YOUTH: (flexing his hand in the cuff) "It's tight."
EST-D6.04 MAERYN: [EST_BAND = self] "The warden's hand moulded that. To my string." / [EST_BAND = brisa] "Brisa moulded that. She didn't ask."
EST-D6.10 [EST_CARD = taken] YOUTH: (looking through the curtain at the rack) "You kept her card."
  > "In case she comes back. So I know her lamp."   → EST-D6.12
  > "I'll burn it."                                 → EST-D6.12
EST-D6.12 YOUTH: "Do what you want with it." (beat) "Everyone does."
EST-D6.20 MAERYN: (brings the mending book in from the counter; opens it at a clean page; lays his old sleeve on it) "Everything scorched that comes through this shop, I draw. That's how I know what's changing." (she looks at the player, not at him)
EST-D6.21 YOUTH: "Don't ask me. You're the one who keeps counters."
EST-D6.22 [player asks Maeryn, optional] "Is he—"  MAERYN: [EAC_MAERYN_SAID] "I told you once. I don't say it twice in a week." / [else] "He's a customer. He uses the back door. So do I, sometimes."
  > "Trace it. Somebody should know it's happening."   → EST-D6.40
  > "Leave it out. It's his sleeve."                   → EST-D6.50
EST-D6.40 MAERYN: (draws round the cuff; shades the scorch; writes small) "'Back door. Cuff. Inside.'" (beat) "Now somebody knows. Whoever reads my book."   {EST_BOOK = traced}
EST-D6.41 YOUTH: "Nobody reads your book."
EST-D6.42 MAERYN: "You'd be surprised." (he looks away; he does not argue)   → EST-D6.30
EST-D6.50 MAERYN: (closes the book) "Then you come in yourself. Every pair. I've nothing to size from."   {EST_BOOK = unrecorded}
EST-D6.51 YOUTH: "I can do that."   → EST-D6.30
EST-D6.30 YOUTH: (at the yard door; hood up; not turning round) "Kaelen."   {EST_KAELEN_NAMED}
EST-D6.31 KAELEN: "Something under this city says my name at night. She says it's the pipes."   [R19 shadow only; never evidence; never explained]
EST-D6.32 MAERYN: "It is the pipes."
EST-D6.33 KAELEN: "I'm looking for someone. That's why I stay near. That's all you get." (he goes)
```

```
EST-D7 (close)
EST-D7.01 MAERYN: (puts the kettle on the cold stove, notices, laughs once, lights it) "Sit. Have something. You've had a fitting."
EST-D7.02 MAERYN: (pays the player) "For the counter. The counter was very well kept."   {payment; event: S05 → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| EST-I1.01 | His sleeves | *"Plain cloth over a gold ember-thread lining. At the cuffs the lining is black and the cloth scorched through, from the inside out. The scorch has fingers."* |
| EST-I1.02 | His sleeves (`EEH_MENDING_BOOK`) | *As above, then:* *"The same shape as the children's palms in Maeryn's book. Bigger."* |
| EST-I2.01 | The knotted string | *"Waxed string, a coloured thread at one end, three knots along it at uneven spaces."* |
| EST-I2.02 | The moulded band | *"Stiff hide, lined in gold thread. Three soft rises along the inside, where the pegs were."* |
| EST-I3.01 | The card | *"A lamp drawn in grey ink, and the lamp-house's door mark. On the back, in a careful hand: 'Steadying, any night. Ask for Ondine.'"* |
| EST-I3.02 | Stove hood tell (`S04`) | *"The bead in the stove hood. Red, crazed."* / after parts: *"Amber."* / after: *"Clear."* |
| EST-I3.03 | The yard door latch (hot) | *"Too hot to hold. Wrap your hand."* |
| EST-I4.01 | Mending book, his page (`traced`) | *"A cuff, drawn round in pencil, the scorch shaded in. 'Back door. Cuff. Inside.' On the facing page, a child's palm."* |

---

## ETB — Three Breaths

### ETB.1 Hook

**Remember:** the sound of twenty chimes out of time with each other. **Want next:** to know who taught a whole city to breathe on one bell, and why.

### ETB.2 Selection record and canon grounding

Rejected: Asera revealing the primer's exercise as Volkhari in origin (ED-12; a resemblance proves nothing); the primer explaining the test's purpose (R18 is CV-M4's; practice only, bible §8.2).

| Element | Source | Status |
|---|---|---|
| Academies teach heat-channel breathing, controlled ignition, ember-thread weaving, emotional suppression drills and **group resonance synchronization**; they assess volatility and sort students | Dossier §XI.1 | [CANON] |
| Idra Callow: junior teacher, believes in the craft, starting to doubt the test; the class's count "In. Two. Three."; Benno | Act I §B6 Beat 1, `EEH-D3.11` | [NEW, Act I] |
| Lenses reground on a Council schedule; "a lens for pushing, not seeing" | Act I §B6 Beat 4 (`EEH_LENS_READ`) | [NEW, Act I] |
| Asera: Volkhari ritualist, breath-binding, calms flares; soft-spoken, precise; never casts at enemies and teaches no spellcasting; her count "In. Hold. Three." | Character file §46; bible §5.1; Act II `EAC-D7.12` | [CANON]; [NEW, Act II] |
| Guild outcome: the guild's revised test uses Idra's older exercise | Act I §B9.3 (`EH_CURRICULUM = guild`) | [NEW, Act I] |
| R18 seed: volatility tests, curriculum, rehearsals shown as practice | Revelation Ledger R18; bible §8.2 | [APPROVED — FT-04] seeds only |
| The primer *Grounding for the Young Hand*; the syllabus card; the chime exercise | This package | [NEW] |

### ETB.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `emberholt.side.three_breaths` |
| Series | *The Unburnt*, part 2 of 3 |
| Type | Memory/lore |
| Unlock | `emberholt.side.stitches_in_the_lining` (EST) Completed **and** `emberholt.main.04_ash_stained_chains` Completed. Idra is at the court gate on the Molten Stair (`ETB-D1`); Maeryn's bark `EST-B2.07` points to her. |
| Length | 35–45 minutes |
| Combat share | 0% |
| Skills | **Smithing ~[GD: low]**: forge three chime bars from an imported stock bar at the Cooling House small forge (Cinderwall; Act I hub) and ring each true. Time-cost alternative: the guild yard's apprentices cut a set from offcuts (keep watch to morning; `ETB_CHIMES = guild`). |
| Choice | Where the three breaths are taught (`ETB_TAUGHT` = court / courtyard). |
| Outputs | `ETB_TAUGHT`; EMS (with EH-M3) |
| **Anchor** (contract) | Academies (Idra; Theryn); Asera. |
| **World-truth row** (contract) | H03 (Volkhari individuals and their own discipline), H13 (the war's craft aftermath in schooling), H22 (conditioning practice in civic institutions). |
| **Revelation role** (contract) | **Supports R18** (what the test is for): the syllabus card's *readiness* and its Council schedule number beside the primer's *so the teacher may see*. Practice only; never explains Perfect Flame or a plan. |
| **Recurring evidence** (contract) | The pre-war primer (read in place in Idra's lodging) + Asera's own account of the count (her words, her terms) + the syllabus card (read in place at the court). Nothing is proved; R18's custodians are CV-M4's. |
| **State compliance** (contract) | Inactive → Active on `ETB-D1` accept; Completed on `ETB-D8` end. No fail: a dull bar is re-forged; a mistimed chime is "close enough"; Asera's scene re-offers each dusk. Asera's one line about Thalan reads `EH_THALAN = freed` (D-E2, ruled 2026-11-15). Resume hook: Idra at the court gate (`ETB-B1.02`). |
| **Combat compliance** (contract) | None. No encounter, no hazard beyond the forge's ordinary heat. **CDR-6 solo test:** forging, the trial, Asera's scene, the comparison and the lesson are all one player's actions with NPCs; the lesson's twenty prompts are paced to one player and never require two; no reward depends on co-op. |

### ETB.4 The places

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Idra's lodging** [NEW sub-site of EP04] | Offer follow-up; the primer (`S01`) | A narrow room in the teachers' lodging off the Stair. Marked essays in piles, a practice lantern on the sill, the **primer** open on the table under a lamp. Through the window, heat-shimmer from the chasm. |
| **B. The practice court** (EP04, M1 in Act I) | The trial (`S03`), the comparison (`S05`), the lesson (`S07`, `court`) | As EEH. The **syllabus card** framed by the bell post. The empty **chime frame** on the wall by the lantern rack: three hooks, nothing on them. The vent-hood tell. |
| **C. The Cooling House forge** (EP02, Act I hub) | The chime bars (`S02`, Option A) | The small forge, anvil, quench trough. A **measuring jig** Hennet uses for pot hooks. |
| **D. Maeryn's back room** (EP03) | Asera (`S04`) | As EST and EH-M4. Asera comes in by the yard door at dusk. |
| **E. Selice Morra's workshop** (EP03, C3 in Act I) | Borrow an old lens (`S05`) | As EEH. Her rack of old school lenses. |
| **F. The Cinderweave courtyard** (EP03; EME09's place) | The lesson (`S07`, `courtyard`) | A cobbled courtyard where children play "hold it steady" at dusk. Doorstep lanterns. |

**MAP VERIFICATION REQUIRED** for Idra's lodging and the courtyard.

### ETB.5 Player-facing sequence

Exact wording lives in ETB.12; beats cite node ids.

**Beat 0: Idra (`S00_offer`).** *Objective: Speak to Idra Callow at the court gate.* `ETB-D1`. Idra has a book under her arm that she will not open in the street, and wants to show the player something "I'm not supposed to want to show you". Accept: Active. Not now: re-offer by bark.

**Beat 1: The primer (`S01_primer`).** *Objective: Read the primer in Idra's lodging.*
1. **The primer** (`ETB-I1.01`; document `ETB-DOC1`): *Grounding for the Young Hand.* Three breaths; the child keeps her own count; the teacher sounds a low, a middle and a high chime "for each child, when that child's flame shows it is ready, and not before", *"so that the teacher may see how the child holds the flame."* The page on the third breath is torn away after *"The third breath is not"*.
2. **The syllabus card** (`ETB-I2.01`): *Grounding: one breath, counted three on the bell. The class together. Purpose: readiness.* A printed number in the corner; with `EEH_LENS_READ` (`ETB-I2.02`) the player knows its form from the reground-lens slip: a Council schedule.
3. **Compare** (`ETB-D2.10`–`.22`): three breaths, each the child's own, against one breath counted three times. Completes on `ETB-D2.30`.

**Beat 2: The chimes (`S02_chimes`).** *Objective: Get a set of three chime bars.* The court's old frame has three empty hooks (`ETB-I3.01`). Idra gives a **stock bar** (carry-state) and the primer's lengths on a slip: a hand, a hand and a thumb, a hand and two thumbs.
- **Option A (skill): Smithing ~[GD: low]**, at the Cooling House forge: **mark and cut** on Hennet's jig (three interactions; the jig takes only the slip's marks); **draw out** each bar (2-segment channel each; segments persist); **quench**; **ring twice**. A dull ring means a cold shut (`ETB-I3.03`): reheat, hammer (one channel), ring again. No limit, no loss. `ETB_CHIMES = self`.
- **Option B (time-cost):** a guild apprentice at the Emberforges cuts a set from offcuts; keep watch to morning. `ETB_CHIMES = guild`.
Hang the bars on the frame (three place interactions). Completes on the third.

**Beat 3: Benno (`S03_benno`).** *Objective: Try the exercise with Benno after class.* After the morning class, **Benno** stays with his lantern (`ETB-D3`; with `EEH_CLASS_DONE` he remembers the player). **Read and sound** (taught here, used at scale in `S07`): while his flame stands tall and flickers, wait; when it settles and stops moving (a clear ~1 s settle), sound the next chime, low, middle, high. Early: Idra says "Wait for him"; nothing resets. His flame settles lower on the low and middle chimes. On the high chime Idra guesses at the torn line, "Hold it?", Benno holds his breath, and **his flame stands straight up again** (`ETB-D3.20`). Idra knows one person who keeps old counts, who is not a teacher: ask Maeryn Vall. Completes on `ETB-D3.32`.

**Beat 4: Asera (`S04_asera`).** *Objective: Ask Maeryn about the count.* Maeryn says she sews (`ETB-D4`); with `EST_BOOK` set, she adds that Asera comes by at dusk, some dusks. Keep watch on the stool if needed. **Asera** comes in by the yard door (`ETB-D5`). With `EAC_BREATH` she remembers the player (`ETB-D5.04` / `.05`); with `EST_KAELEN_NAMED`, one line about the youth (`ETB-D5.03`). One line about Thalan, freed (`ETB-D5.10`; D-E2, ruled 2026-11-15). The player **shows** her Idra's copy of the page and sounds the three notes on the tuning nails Maeryn keeps for thread tension (presentation). Asera knows the count. She decides how much to say (`ETB-D5.20`–`.32`, `[ED-12]`): the third breath is **given, not held**, let out and not followed; where the count comes from stays hers. She will not go up the Stair. Sets `ETB_THIRD_GIVEN`. Completes on `ETB-D5.40`.

**Beat 5: The comparison (`S05_compare`).** *Objective: Try the third breath with Benno; compare the light.* Borrow one of Selice's **old school lenses** (`ETB-D6.01`; carry-state). At the court, read and sound again; on the high chime Benno gives the breath and **his flame spreads, wide, soft and low, and stays** (`ETB-D6.10`). Idra holds the lens behind it: a broad disc of light on the white card (`ETB-I6.01`; `ETB_LENS_SPREAD`). **Theryn** at the rail (`ETB-D6.20`): a good exercise, not in the syllabus, and the syllabus is not hers. By `EH_CURRICULUM`: `guild`, the guild is writing a new test and could take it; `evidence`, not in her court this season. Completes on her line. The lens goes back to Selice off-screen.

**Beat 6: Where it's taught (`S06_choice`).** *Objective: Decide with Idra where the three breaths are taught.* `ETB-D7`. Idra wants it taught and does not want it to be hers. The choice (`ETB_TAUGHT`):
- **The court.** `guild`: Idra takes the page and the chimes to the teachers' guild; the revised test begins with three breaths. `evidence`: she teaches it in her own class after the bell, out of syllabus, and may be spoken to.
- **The courtyard.** The page copied onto a board and the chimes hung in the Cinderweave courtyard, for any child at dusk, outside any syllabus, with no teacher's name on it.
Asking Idra returns her view (`ETB-D7.10`) and the options again.

**Beat 7: The lesson (`S07_lesson`), the set piece and the wonder.** *Objective: Sound the chimes for the lesson.* Next morning (court) or dusk (courtyard). Twenty children with lanterns in four bench rows of five, Tavi among them (`ETB-B2.03`). Each flame is its own tell; each child needs three chimes, each at their own settle; the player may sound any child's next chime in any order (the frame highlights the child looked at). Early chimes get "Wait for her." No timer, no fail. A row is done when all five flames are spread. **The wonder** (ETB.7). Completes when the fourth row is done and `ETB-D8` plays.

### ETB.6 Encounters and hazards

**Encounters:** none. **Hazards:** none on the path. The forge is ordinary forge heat (no damage). Benno's and the children's flames never become a flare zone in ETB (they are a lesson, not a test; Idra keeps a hand near every lantern).

### ETB.7 The wonder moment: rain on the court (Beat 7)

| Time | Element | Spec |
|---|---|---|
| Throughout | **Sound** | Every chime the player sounds stays in the air a moment; with twenty children on their own counts, the chimes fall out of step with each other. By the third row it sounds like rain on a roof, low and high and middle, never together. |
| Each child | **Flames** | After a child's third chime, the flame spreads wide and low and holds. Every spread flame is a different height. |
| End | **The tell** | The court's vent-hood tell (or, in the courtyard, the doorstep lanterns' tells) goes clear and **stays** clear. In EEH, the row lit on one breath turned it clear for a moment; here nothing is in step and it stays clear anyway. |
| After | **Idra** | `ETB-D8.02`: "Listen to that." (beat) "Nobody's together. Nobody needs to be." |
| What it means | | Nothing is explained. It contrasts, without comment, with the one-breath ignition (EEH) and the rehearsal crowd (EH-M5). No line names Perfect Flame, the crowd, or a purpose (R18 seed only). |

### ETB.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Speak to Idra Callow at the court gate. | `ETB-D1` accept | Yes |
| `S01_primer` | Read the primer in Idra's lodging. | `ETB-I1.01` **and** `ETB-I2.01` **and** `ETB-D2.30` | Yes |
| `S02_chimes` | Get a set of three chime bars. | (3 bars forged and rung true **or** keep watch to morning at the guild yard) **and** 3 × `hang_chime` | Yes |
| `S03_benno` | Try the exercise with Benno after class. | Low + middle + high chimes sounded at settle **and** `ETB-D3.32` | Yes |
| `S04_asera` | Ask Maeryn about the count. | Dusk **and** `ETB-D5.40` (`ETB_THIRD_GIVEN`) | Yes |
| `S05_compare` | Try the third breath with Benno; compare the light. | Lens borrowed **and** three chimes **and** `ETB-I6.01` **and** `ETB-D6.24` | Yes |
| `S06_choice` | Decide with Idra where the three breaths are taught. | `ETB-D7` choice | Yes |
| `S07_lesson` | Sound the chimes for the lesson. | 4 rows × 5 children spread **and** `ETB-D8` end | Yes (→ Completed) |

### ETB.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `ETB_CHIMES` = self / guild | `S02` | `ETB-D3.02` |
| `ETB_THIRD_GIVEN` | `ETB-D5.30` | `S05`, `S07` |
| `ETB_LENS_SPREAD` | `ETB-I6.01` | `ETB-D7.04` |
| **`ETB_TAUGHT` = court / courtyard** | `ETB-D7.20` / `.30` | Molten Stair barks; EME09 (request: with `courtyard`, the children's game uses three chimes); EMS `EMS-B1.03` (Maeryn) |

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **The court** | `guild`: the guild's revised test opens with three breaths. `evidence`: Idra teaches it after the bell, out of syllabus. | `guild`: slow and argued, as guild things are. `evidence`: Idra may be spoken to (`ETB-B2.05`); some teachers do not join her. | Stair barks; children who learn it in class. |
| **The courtyard** | Chimes and a copied board in the courtyard; any child at dusk. | Not in any syllabus; nobody's name on it; it depends on who comes. | EME09 (request); courtyard barks. |

Neither choice exposes Theryn, changes the test lenses, or reveals anything about "below". Neither is wrong.

### ETB.10 Rewards, failure, death, walk-away, co-op

| Reward | Type | Notes |
|---|---|---|
| **The three-chime count** | Knowledge | Journal entry: *"Three breaths. In. Hold. Given."* Flavour; no player embercraft (bible §11 item 8). |
| Small payment | Currency | Idra pays from her own purse; refuses to be thanked [GD]. |
| Skill XP | Actions only [GD] | Smithing (Option A only). |
| *The Memory-Stone* | Story | With EH-M3 Completed (always, by this point): Maeryn's bark `EMS-B1.01` the next time the player passes the shop. |

| Situation | Handling |
|---|---|
| No Smithing | The guild yard's apprentices cut a set overnight. |
| A dull bar | Re-forge it; no material is lost. |
| An early chime | "Wait for him." No reset. |
| Not dusk at Maeryn's | Keep watch on the stool. |
| Death | Not possible on the path (no damage sources). If the player dies elsewhere, they resume at the persisted step. |
| Walking away | Stays Active. The stock bar, slip and lens (carry-state) return to Idra or Selice if the player logs out holding them. Resume: `ETB-B1.02`. |
| Fail state | None. |
| Co-op (CDR-6) | Per §0.6. Each lesson is paced for one player; a partner sounds chimes in their own instance only. |

### ETB.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| Read-and-sound interaction (sound a chime when a lantern-flame settles) | Systems | A prompt that becomes valid while a target prop is in its "settled" state; the lantern prop cycles tall/flicker → settled on a short authored loop per child. Reuses EEH's "interaction prompted by a cue" (Idra's raised hand). **Fallback:** Idra calls "Now" for each child. |
| Three-pitch chime props | Audio/Art | Three bar props with three notes; positional sound so twenty overlapping chimes read as rain. |
| Lantern flame states (tall, settled, spread) | Art/VFX | Three flame variants on the existing practice lantern. |
| Forge, jig and ring-twice interactions | Systems | Existing Smithing interactions; "dull ring" is a state on the forged bar prop. |

No new runtime system.

**Mystery ledger.**

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Why the syllabus changed** | On a Council schedule, with the lenses, toward measuring how far a flame can be pushed and how a class breathes together (bible §2.1, §2.3; R18). | "The new card is more efficient." | The primer; the syllabus card's *readiness* and schedule number; Selice's lens slip. | Idra's predecessors were lazy; the old way was dangerous. | What *readiness* is for. | R18 (CV-M4). |
| **Where Asera's count comes from** | Hers to say. | — | Her recognition. | The primer was copied from the Volkhari; or the Volkhari copied it. | Everything. | None (ED-12). |

**Open decisions.**
1. **The primer's origin.** The primer is pre-war and unsigned. No text says who wrote it or whether its count and Asera's share a root. Recommendation: leave it so. If the Director later rules on the Volkhari foundations of civic practice, only `ETB-D5.32` changes.
2. **D-E2: resolved (ruled 2026-11-15).** Thalan is freed with his consent; `ETB-D5.11` (the aided line) is cut and `ETB-D5.10` stays. Nothing else changed.
3. **Theryn's line under `evidence`** ("Not in my court this season. I'm sorry.") keeps her inside her canon limits (sincere, not exposed). If later content resolves her loyalties differently, the line still holds.

| Review finding | Revision |
|---|---|
| Draft had Asera say "This was ours before it was yours." | Cut: asserts Volkhari origin of a civic practice (bible leaves Seralynd's suspicion unused). Now: "It's a count I know." and "Mine to know." |
| Draft gave the player a breathing ability. | Cut: no player embercraft (bible §11 item 8). The player sounds chimes and reads flames. |
| Draft's syllabus card said *for group resonance* outright. | Softened to *readiness*: practice only (R18 is CV-M4's). |
| Draft's EEH callback had Idra count "In. Two. Three." as the old way. | Fixed: that is the **current** count (one breath counted three, `EEH-D3.11`); the primer's is three breaths. Idra's line makes the difference plain. |

### ETB.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Idra Callow** [NEW, bible] | Her class; the card; the primer; the ledger (EEH). | What *readiness* means; who changed the card. | Warm, funny, tired, honest. Believes in the craft. Doubts the test out loud only with people she trusts. |
| **Benno** [NEW, Act I] | His flame is always in a hurry. | — | A child. Pleased with himself. |
| **Asera** [CANON] | Her count. Her own breath-binding. | Where the city's primer came from. | Soft, precise, sad underneath; takes failures personally. Decides how far she goes, out loud (Act II). |
| **Theryn Dalewright** [CANON] | The syllabus is set above her. | — | Kind, unhurried, careful. Sincere stewardship (bible §5.1). |
| **Selice Morra** [CANON] | Glass. | — | Speaks to the glass. |
| **Maeryn Vall** [CANON] | Who comes by at dusk. | — | As EST. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| ETB-B1.01 | Idra | Available, the court gate | *"Warden's hand. Got a minute? Got an hour? Got a hammer?"* |
| ETB-B1.02 | Idra | Active, returns | *"The page is still torn. I keep checking."* |
| ETB-B1.03 | Idra | Active, `EST_BOOK = traced` | *"Maeryn showed me her book. There's a page in it now that isn't a child's hand. I didn't ask."* |
| ETB-B1.05 | Hennet | `S02` Option A, a bar rung true | *"That's a note. Don't hang it in my kitchen."* |
| ETB-B2.03 | Tavi | `S07` | *"Is it my turn? Is it my turn? Oh. It's my turn when it's my turn."* |
| ETB-B2.05 | A teacher | Completed, `court` + `evidence` | *"Callow's running bells after hours again. Somebody'll say something."* |
| ETB-B2.06 | A child | Completed, `courtyard` | *"Low, middle, high. You wait for your own one."* |

#### Nodes

```
ETB-D1 (the court gate; S00)
ETB-D1.01 IDRA: (a book under her arm; she doesn't open it in the street) "Warden's hand. Come up to my rooms."
ETB-D1.03 [EEH_CLASS_DONE] IDRA: "You held the frame for Benno once."
ETB-D1.04 IDRA: "I want to show you something I'm not supposed to want to show you."
  > "Show me."                                      → ETB-D1.10
  > "Not now."                                      → ETB-D1.40
ETB-D1.10 IDRA: "It's old. It's in a book-press nobody's opened since the war. I opened it."   {quest Active; event: S00}
ETB-D1.40 IDRA: "It's waited a long time. It can wait for your soup."
```

```
ETB-D2 (Idra's lodging; S01)
ETB-D2.01 IDRA: (opens the primer under the lamp) "'Grounding for the Young Hand.' Read the middle. Then this." (lays the syllabus card beside it)
ETB-D2.10 IDRA: "Three breaths. Not one breath counted three times. Each child their own." (beat) "And chimes. One for each breath. For each child. When they're ready. Not on my hand."
ETB-D2.12 IDRA: "'So that the teacher may see how the child holds the flame.'" (she taps the card) "Ours says 'readiness'. Readiness for what? I've never asked. I teach it."
ETB-D2.20 [EEH_LENS_READ] IDRA: "That number in the corner. You've seen one like it."
  > "On the slip with Selice's lens. A Council schedule."   → ETB-D2.22
  > "Have I?"                                               → ETB-D2.22
ETB-D2.22 IDRA: "Same form. Same office, probably." (beat) "I'm not saying anything. I'm saying it's the same form."
ETB-D2.24 IDRA: (turns to the torn page) "And this. 'The third breath is not.' And then nothing. Somebody needed that page more than I do."
ETB-D2.30 IDRA: "The court had chimes once. The hooks are still there. I want to try it. On one child. A real one."   {event: S01}
```

```
ETB-D3 (the court, after class; S02 end, S03)
ETB-D3.01 IDRA: (hands over a stock bar and a slip) "A hand. A hand and a thumb. A hand and two thumbs. That's what the book says."
ETB-D3.02 [S02 done] IDRA: [ETB_CHIMES = self] "You made those. They ring like they mean it." / [= guild] "The guild boy cut them. He wanted paying in cake. Everyone wants paying in cake."
ETB-D3.10 BENNO: (with his lantern; the flame up past his ear) [EEH_CLASS_DONE] "You're the frame." / [else] "Are you the bell?"
ETB-D3.11 IDRA: "Benno. Three breaths, your own. You breathe. The warden's hand listens to your flame, not to you. When it sits, you'll hear a chime."
ETB-D3.12 IDRA: (to the player) "Wait till it settles. Not before. Watch the flame, not his face."
ETB-D3.13 [early chime] IDRA: "Wait for him."
ETB-D3.14 [low chime at settle] (Benno's flame sits lower.)  BENNO: "Oh."
ETB-D3.15 [middle chime at settle] (Lower again.)  BENNO: "Ohh."
ETB-D3.16 IDRA: (reading the torn page; guessing) "Third breath. Hold it?"
ETB-D3.20 [high chime] (Benno holds his breath. His flame stands straight up again, tall and fast.)  BENNO: "It went."
ETB-D3.30 IDRA: (kneels; settles his flame with her hand round the glass) "It says a third. It doesn't say what. The page is gone."
ETB-D3.31 IDRA: (to the player, low) "I know one person who keeps old counts. She isn't a teacher. I've seen her once, at Maeryn Vall's, through a curtain."
ETB-D3.32 IDRA: "Ask Maeryn. She'll know who I mean. Or she'll say she sews."   {event: S03}
```

```
ETB-D4 (Maeryn's shop; S04)
ETB-D4.01 MAERYN: (threading) "A count? I sew."
ETB-D4.02 [EST_BOOK set] MAERYN: (beat; not looking up) "Some dusks somebody comes by who doesn't sew. Sit on the stool. If she comes, she comes."
```

```
ETB-D5 (Maeryn's back room, dusk; S04)
ETB-D5.01 ASERA: (in from the yard; sees the player; sits) "Maeryn said a teacher's hand wanted a count."
ETB-D5.02 [EAC_MAERYN_SAID] MAERYN: (from the curtain) "I told you once. I don't say it twice in a week." (she lets it fall)
ETB-D5.03 [EST_KAELEN_NAMED] ASERA: "The boy with the sleeves came by. He said a stranger shuttered a window for him. He didn't say thank you. That was thank you."
ETB-D5.04 [EAC_BREATH = asera] ASERA: "You kept my count once."
ETB-D5.05 [EAC_BREATH = waited] ASERA: "You waited a room out once. Waiting's a count too."
ETB-D5.10 [EH_THALAN = freed] ASERA: "I sleep some nights now. He walked. I don't know where, and I don't ask."
ETB-D5.12 ASERA: "Show me what the teacher wants."
  {interaction: show the copied page; sound three notes on Maeryn's tension nails}
ETB-D5.20 ASERA: (eyes shut; after the third note) "In. Hold. Three." (she opens her eyes) "I know that count."
  > "What's the third breath? The page is torn."          → ETB-D5.30
  > "Where does the count come from?"                     → ETB-D5.32
  > "Will you come and teach it?"                         → ETB-D5.34
ETB-D5.30 ASERA: "The third isn't held. It's given. You let it go out of you, and you don't follow it." (beat) "Your teacher said 'hold'. Holding is what makes it stand up."   {ETB_THIRD_GIVEN}   → ETB-D5.20 options
ETB-D5.32 ASERA: "Mine to know." (not unkind) "Where your book learned it, ask your book."   → ETB-D5.20 options
ETB-D5.34 ASERA: "Not up there. Not where they write things down." (beat) "You heard it. You teach it. That's how counts go."   → ETB-D5.20 options
ETB-D5.40 [ETB_THIRD_GIVEN] ASERA: (stands) "Given. Not held. Tell the child it's allowed to go."   {event: S04}
```

```
ETB-D6 (Selice's workshop, then the court; S05)
ETB-D6.01 SELICE: (takes an old lens off her rack without looking) "One of mine. A seeing one." (beat) "Bring it back."
ETB-D6.10 [high chime; Idra says "Give it."] (Benno breathes out and doesn't hold. His flame spreads, wide and soft and low, and stays.)  BENNO: "It's flat. It's flat and it's fine."
ETB-D6.12 IDRA: (holds Selice's lens behind it; a broad disc of light on the white card) "That's how he holds it." (beat) "I can see it."   {prompt: inspect card, ETB-I6.01}
ETB-D6.20 THERYN: (at the rail; she has watched) "It's a good exercise." (beat) "It isn't in the syllabus. The syllabus isn't mine."
ETB-D6.22 [EH_CURRICULUM = guild] THERYN: "The guild is writing a new test. Take it to them, if you like."
ETB-D6.23 [EH_CURRICULUM = evidence] THERYN: "Not in my court this season. I'm sorry." (she means it)
ETB-D6.24 (Theryn goes back inside. Idra lets out a breath she didn't count.)   {event: S05}
```

```
ETB-D7 (the court bench; S06)
ETB-D7.01 IDRA: "I want it taught. I don't want it to be mine."
ETB-D7.04 [ETB_LENS_SPREAD] IDRA: "A disc. Not a point. I'll see that disc in my sleep."
ETB-D7.06 IDRA: "Where?"
  > "Here. In the court."                                   → ETB-D7.20
  > "In the courtyard. At dusk. Any child."                 → ETB-D7.30
  > "What would you do?"                                    → ETB-D7.10
ETB-D7.10 IDRA: "I'm a teacher. I'd say the court." (beat) "Then I think of the card in the corner."   → ETB-D7.06 options
ETB-D7.20 [EH_CURRICULUM = guild] IDRA: "Then it goes to the guild with the chimes. The new test starts with three. It'll be loud and slow and it'll happen." / [= evidence] IDRA: "Then I teach it after the bell. Out of syllabus. Let them speak to me."   {ETB_TAUGHT = court}   → ETB-D7.40
ETB-D7.30 IDRA: "A board and three bars on a wall. Nobody's syllabus. Nobody's name." (beat) "I like that more than I should."   {ETB_TAUGHT = courtyard}   → ETB-D7.40
ETB-D7.40 IDRA: [court] "Tomorrow morning. You're on the chimes." / [courtyard] "Tomorrow at dusk. You're on the chimes."
```

```
ETB-D8 (the lesson; S07)
ETB-D8.01 IDRA: (to twenty children) "Three breaths. Your own. The warden's hand is listening to your flame. When it sits, you'll hear your chime. Not before. Not with anyone else's."
ETB-D8.02 [end of the fourth row] IDRA: "Listen to that." (beat) "Nobody's together. Nobody needs to be."
ETB-D8.04 [ETB_THIRD_GIVEN] IDRA: "Given. Not held." (beat) "I'll put that on the board. In my hand. Without a name."
ETB-D8.05 IDRA: (pays the player) "From my own purse. Don't thank me. I'll cry and the children will see."   {payment; event: S07 → quest Completed}
```

#### Inspect texts and documents

| Id | Object | Text |
|---|---|---|
| ETB-I1.01 / ETB-DOC1 | The primer | *"Grounding for the Young Hand. ... Three breaths. The child keeps her own count; the teacher does not count for her. For each breath a chime: low, middle, high. Sound it for each child when that child's flame shows it is ready, and not before. The first breath is taken in. The second is held. The third breath is not"* (the rest of the page torn away) *... Purpose: so that the teacher may see how the child holds the flame."* |
| ETB-I2.01 | The syllabus card | *"Grounding: one breath, counted three on the bell. The class together. Purpose: readiness. In the corner, a printed number."* |
| ETB-I2.02 | The syllabus card (`EEH_LENS_READ`) | *As above, then:* *"The number is the same form as the one on the slip with the reground lens. A Council schedule."* |
| ETB-I3.01 | The empty chime frame | *"Three iron hooks on a board by the lantern rack. Three paler shapes on the wood where something hung."* |
| ETB-I3.03 | A dull bar | *"It rings flat and stops short. A cold shut. Heat it and close it."* |
| ETB-I6.01 | The white card (seeing lens) | *"A broad soft disc of light, the edges blurred. You can see where the flame is strongest and where it thins."* |

---

## EMS — The Memory-Stone

### EMS.1 Hook

**Remember:** a silence so complete the player notices they had never heard Emberholt without its vents. **Want next:** to stand at the tally board and see who stands at the back.

### EMS.2 Selection record and canon grounding

Rejected: the stone replaying the Hollow night with new detail (R09 is EH-M3's; weight only, bible §7.3); the collector as a Remnant agent to evade or fight (lamp-keepers are never targetable; Ondine is sincere).

| Element | Source | Status |
|---|---|---|
| Seredh: Volkhari historian and memory-stone artisan; stoic, slow to trust; stones preserve a maker's recollection and interpretation and cannot recreate objective events without corroboration; he hid stones to protect their memory | Character file §45; bible §5.1 | [CANON] |
| Seredh's terms: "It is one stone. One hand made it." "Not whose stone. Not whose hands." | Act I `EGH-D9.20`–`.32` | [NEW, Act I] |
| The Ash Roads: cracked old streets lined with burnt engravings; some Volkhari symbols scraped away by the city | Dossier; bible EP09, EDS01 | [CANON; placement NEW] |
| The Cold Seam: a fissure where no heat rises; a place of quiet grief; small cold stones left for the dead; why it is cold never explained | Bible EP21, EDS07; Part 3 proposal | [NEW, Part 3] |
| Volkhari Ash seizure notices signed by Deepbrand | Bible EDS10 | [NEW, bible] |
| `EH_UNBURNT` kept / strained; strained mendable by a later visit | Bible §7.1, §7.3, §9.1 | [NEW, bible] |

### EMS.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `emberholt.side.the_memory_stone` |
| Series | *The Unburnt*, part 3 of 3 |
| Type | Memory/lore |
| Unlock | `emberholt.side.three_breaths` (ETB) Completed **and** `emberholt.main.03_hollow_that_should_not_burn` Completed. Maeryn's bark `EMS-B1.01`; Seredh is in his workroom in Maeryn's yard (`EMS-D1`). |
| Length | 30–40 minutes |
| Combat share | 0% |
| Skills | **Mining ~[GD: low]**: cut a seat for the stone in the Cold Seam's wall with a pick (three strikes on marked points). Time-cost alternative: Seredh's cold chisel, a slow six-segment channel (`EMS_SEAT = chiselled`). |
| Choice | Who keeps the stone: the Cold Seam (`EH_UNBURNT = kept`) or the lamp-house (`EH_UNBURNT = strained`, mendable). |
| Outputs | **`EH_UNBURNT`**; `EMS_SEAT` |
| **Anchor** (contract) | Seredh Embercarver; a Covenant collector (Ondine Thursk). |
| **World-truth row** (contract) | H03 (Volkhari individuals and their memory craft), H18 (the city's erasure of Volkhari presence, here the scraped Ash Roads). |
| **Revelation role** (contract) | **Supports R09 (weight only)**: one maker's account of Volkhari marks being scraped from the Ash Roads (the EDS01 seed). Adds no fact about the Hollow and is never a custodian. |
| **Recurring evidence** (contract) | The memory-stone (carry-state; one account, Seredh's terms). Not used as proof of anything. |
| **State compliance** (contract) | Inactive → Active on `EMS-D1` accept; Completed on `EMS-D6` end. `EH_UNBURNT` kept or strained; strained is mendable after completion (`S07_mend`, optional, same writer). No fail: the stone cannot be lost or broken; a Surging stretch is waited out in a niche; the chisel replaces the pick. Resume hook: Seredh's workroom (`EMS-B1.02`) or the Cold Seam (`EMS-B2.01`). |
| **Combat compliance** (contract) | None. No encounter (the route is pinned clear of the Ridge's wildlife for this quest's steps). Hazards: one vent stretch and one Working stretch on the Ash Roads, ordinary periodic damage. Ondine, Seredh and Maeryn are never targetable. **CDR-6 solo test:** the carry, the choice, the seat and the mend are one player's; nothing needs a second player; no reward depends on co-op. |

### EMS.4 The places

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Seredh's workroom** [NEW sub-site: the lean-to in Maeryn's yard, EP03] | Offer; the stone; the return (`S00`, `S01`, `S05`) | A lean-to against the yard wall: a basalt **cutting block**, chisels laid in order of size, wool bundles on a shelf, a bucket. Cold work: no fire. Seredh works here when he is in the city; nothing says where else he goes. **MAP VERIFICATION REQUIRED.** |
| **B. Cinderwall's working gate** (bible §4: the gate on Cinderwall's side onto the Ridge) | Out onto the Ridge (`S02`) | A plain gate with a warden's bench; a niche with a trough just inside. |
| **C. The Ash Roads** (EP09) | The carry (`S02`) | Cracked old streets with burnt engravings on their kerbs, running out from the walls; in places a carving has been scraped smooth (EDS01 surface). **A vent stretch** (three floor vents on the road; ash lift ~1.5 s before each exhale). **A Working stretch** (amber tells in kerb-posts; light periodic damage) with a niche at each end; pinned **Surging** on arrival, turning Working after one keep-watch turn. Three cooling niches along the route in all. Magma larks (EME08, ambient). |
| **D. The Cold Seam** (EP21) | The choice; the seat (`S03`, `S04`) | A fissure in the ridge rock, man-high, where the air is still and nothing shimmers. A ledge of **small cold stones** left for the dead (EDS07; never to be taken; inspect only). A flat **far end** with a mourner's bench. No flarecap anywhere (inspect: *Nothing glows here.*). **MAP VERIFICATION REQUIRED.** |
| **E. The Covenant lamp-house vigil hall** (EP22, L1 in Act II) | The mend (`S07`, strained only) | As Act II: hanging lamps turned low, the access-book lectern, grey cloaks on pegs. A **custody shelf** behind the lectern where lamp-keepers keep things given into care. |

### EMS.5 Player-facing sequence

Exact wording lives in EMS.12; beats cite node ids.

**Beat 0: Seredh (`S00_offer`).** *Objective: Go to Seredh's workroom in Maeryn's yard.* Maeryn's bark sends the player through the yard way. **Seredh**, at his cutting block (`EMS-D1`), wants a stone set where no heat rises, in the Cold Seam past the Ash Roads, which he does not walk in daylight. Accept: Active.

**Beat 1: The stone (`S01_stone`).** *Objective: Hold the stone; wrap it.* `EMS-D2` (with `EGH_STONE_HEARD`, `EMS-D2.03`). **Hold it**: the account plays (`EMS-DOC1`; ~25 s; sound and a warm haze; no image identifies anyone). Seredh's terms (`EMS-D2.20`–`.21`): one stone, one hand; the player may say a Volkhari stone remembers marks scraped from the road, not whose stone or whose hands. Sets `EMS_HEARD`. **Wrap it**: soak wool in the bucket (one interaction), wrap (2-segment channel). Rule: wet the wool at every niche. The stone is **carry-state, two-handed**: no attacking, climbing or agility shortcuts while held (sprint as the ordinary carry allows; Integration EI-CA-04). It can be set down on any flat surface (stays, per player) and lifted again. Completes on `EMS-D2.30`.

**Beat 2: The road (`S02_road`).** *Objective: Carry the stone to the Cold Seam.* Out by Cinderwall's working gate along the Ash Roads. **MAP VERIFICATION REQUIRED** for the whole route.
- **Niches** (three): *Wet the wool* (~2 s each). All three sets `EMS_WOOL_KEPT`; a skipped one costs a line from Seredh.
- **Vent stretch:** three floor vents across the road; ash lifts ~1.5 s before each exhale. An exhale knocks the player back a step for light damage; carry-state is never dropped by a hit.
- **Working stretch:** kerb-post tells **red and crazed** on arrival (pinned Surging). Keep watch one turn at the near niche and they turn amber (Working); cross on amber for light periodic damage. Entering on red does ordinary heavy damage and **the stone speaks**: ~3 s of iron scraping stone from `EMS-DOC1`, then nothing. Sets `EMS_STONE_SPOKE`. Nothing fails.
- **Optional inspects:** a scraped kerb carving (`EMS-I2.01`; the EDS01 surface text; `EDS01_SEEN` belongs to the Batch 3 discovery file and is **not** set here); the larks.
Completes on entering the Cold Seam volume with the stone held.

**Beat 3: The collector (`S03_collector`).** *Objective: Set the stone in the Cold Seam.* `EMS-D4`. **Ondine Thursk** sits on the far mourner's bench with an unlit lamp, keeping a vigil of her own (`EMS-D4.01`; with `EST_CARD = taken`, `EMS-D4.02`). She knows an ember-carved stone by its wrapped shape and asks, kindly, to take it into the lamp-house's care: Deepbrand crews sign seizures of "anything Volkhari" at the gate (EDS10); the lamp-house keeps a custody shelf under the Covenant's seal for families who cannot. She believes it. With `ESS_RECORD_READ` the player has an inner line about the rooms below the lamp-house (`EMS-D4.20`); nothing says what she knows of them. The choice (`EMS-D4.30`):
- **Set it in the Seam.** She turns her back and lights her lamp. → `S04`.
- **Give it into her care.** She writes a **receipt** in her custody book and gives the player the stub (the `EMS_RECEIPT` flag only; not a carry-state): *Received into care: one carved stone, wool-wrapped, from the warden's hand. To be returned on asking. O. Thursk.* She carries the stone off in both hands. Sets `EH_UNBURNT = strained` (`EMS-D4.40`). `S04` is skipped and re-opens later as `S07_mend`. → `S05`.
- **Ask why** returns her account. There is no option to deceive or threaten her.

**Beat 4: The seat (`S04_seat`).** *Objective: Seat the stone in the rock.* Below the ledge of mourners' stones, three faint chalk crosses (Seredh's, from some other day; `EMS-I4.01`).
- **Option A (skill): Mining ~[GD: low].** With a pick (the player's own, or one at the Seam's mouth), strike the three marks (~2 s each; cold, sound rock, no flarecap). `EMS_SEAT = cut`.
- **Option B (time-cost):** Seredh's cold chisel: a 6-segment channel (~4 s each; segments persist; keep watch allowed between segments). `EMS_SEAT = chiselled`.
**Set the stone** (2-segment channel: unwrap, set). **The strange moment** (EMS.8). Sets `EH_UNBURNT = kept` (`EMS-D5.20`). Ondine, without turning, says it does that sometimes and blesses whoever it is (`EMS-D5.21`–`.22`). Completes on `EMS-D5.22`.

**Beat 5: Seredh (`S05_return`).** *Objective: Tell Seredh.* `EMS-D6`: where it is, and whether it spoke; lines vary by `EH_UNBURNT`, `EMS_WOOL_KEPT`, `EMS_STONE_SPOKE`, `EMS_SEAT`. **Kept:** one nod and a small cold pebble from his shelf (`EMS-D6.10`; keepsake, no stats). **Strained:** a long quiet; it is not where he asked; he does not shout and does not forgive in words; lamp-keepers keep receipts, and the Seam is still there (`EMS-D6.20`–`.21`). Completes on `EMS-D6.30`.

**Beat 6 (post-completion, strained only): The mend (`S07_mend`).** *Optional journal line: Ask the lamp-house for the stone back.* At the vigil hall (`EMS-D7`) show the receipt to Ondine, or to the lamp-keeper at the lectern. The stone comes back off the custody shelf without argument. Carry it to the Seam (as `S02`) and seat it (as `S04`). Sets `EH_UNBURNT = kept` (`EMS-D7.30`); Seredh thanks the player next visit (`EMS-D7.40`). Only the flag and Seredh's lines change.

### EMS.6 Encounters and hazards

**Encounters:** none. **Hazards (pinned for this quest's steps):** the vent stretch (three vents; exhale ~8 s cycle, ash lift ~1.5 s; light damage and a one-step knock-back); the Working stretch (Surging on arrival: heavy periodic damage; Working after one keep-watch turn: light periodic damage). Three cooling niches. A player who goes down respawns at the working gate's niche with the stone in hand and the step intact.

### EMS.7 The account on the stone (`EMS-DOC1`, presentation in `S01`)

Played as sound and a warm haze over the player's view while they hold the stone. No faces, no place names beyond what the sounds and words show, no numbers.

> *Warmth. The sound of a chisel, small and patient, on basalt.*
>
> *A voice, low, in the stone's own words, which are not a language the player knows; the journal gives them as Seredh says them afterward:* "Kerb by kerb. The marks our hands put on the road, the road the city walked on. Ours under theirs."
>
> *A second sound, far off, coming nearer: iron on stone, scraping. Many strokes. Not hurried.*
>
> "They are scraping the road. I have time for one mark. Which one."
>
> *The small chisel again, faster.*
>
> "This one. The one that means *we came this way.*"
>
> *The scraping arrives. Then quiet. Then the chisel, very small, finishing.*

Seredh afterward (`EMS-D2.20`): "That is what it holds. One hand. One morning. One mark kept." The journal records: *A stone that remembers marks being scraped from the Ash Roads, and one kept.* (No custodian status; no fact about the Hollow; R09 weight only.)

### EMS.8 The strange moment: the silence (Beat 4)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Seated** | The stone goes into the seat. The wool comes away cold. |
| 0–3 s | **Silence** | All ambient sound stops: no vent breath from the Ash Roads, no wind, no lark, no tell's tick, no distant forge. The player's own footsteps make no sound if they move. Ondine's lamp flame stands perfectly still. |
| 3 s | **Back** | The wind comes back first, then the larks, then, very faint, the city's vents. |
| After | **Ondine** | `EMS-D5.21`: (without turning) "It does that sometimes. When someone leaves something." She does not explain and does not know. |
| What it means | | Nothing. **Never explained** (EDS07: why the Seam is cold is never explained). Not evidence; identifies nobody. Sets `EMS_SILENCE`; read by nothing, deliberately. |

The silence plays only on a `kept` seating (in `S04` or `S07_mend`).

### EMS.9 Steps, flags, choices and consequences

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Go to Seredh's workroom in Maeryn's yard. | `EMS-D1` accept | Yes |
| `S01_stone` | Hold the stone; wrap it. | `hold_stone` interaction **and** `EMS-D2.20` **and** `wrap_stone` 2 segments **and** `EMS-D2.30` | Yes |
| `S02_road` | Carry the stone to the Cold Seam. | Enter the Seam volume with the stone held | Yes |
| `S03_collector` | Set the stone in the Cold Seam. | `EMS-D4.30` choice | Yes |
| `S04_seat` | Seat the stone in the rock. | (3 × `cut_seat` **or** 6 × `chisel_seat`) **and** `set_stone` **and** `EMS-D5.22` | Only on **Set** |
| `S05_return` | Tell Seredh. | `EMS-D6.30` | Yes (→ Completed) |
| `S07_mend` | (Optional, strained only) Ask the lamp-house for the stone back; seat it. | `EMS-D7.10` **and** `S02`-route carry **and** `S04` seat **and** `EMS-D7.30` | No (post-completion) |

| Flag | Set by | Read by |
|---|---|---|
| `EMS_HEARD` | `S01` | `S01` predicate only |
| `EMS_WOOL_KEPT` | `S02` (all three niches) | `EMS-D6.04` / `.05` |
| `EMS_STONE_SPOKE` | `S02` (red stretch entered) | `EMS-D6.06` |
| `EMS_RECEIPT` | `EMS-D4.40` | `S07_mend`; `EMS-D6.21` |
| `EMS_SEAT` = cut / chiselled | `S04` (or `S07_mend`) | `EMS-D6.08` |
| `EMS_SILENCE` | `ems.silence` event | None (deliberately) |
| **`EH_UNBURNT` = kept / strained** | `EMS-D5.20` / `EMS-D7.30` (kept); `EMS-D4.40` (strained). **One writer: EMS.** | **EH-M6 `S08`** (§9.3 item 6, `EGA-D11.60`); Volkhari barks |

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Set it in the Seam** (`kept`) | The stone is in cold rock where Seredh asked. Ondine did not look. | Ondine knows a carved stone went into the Seam; she says nothing to anyone (presentation). The Seam is public; anyone can sit there. | EH-M6: Maeryn and Seredh stand at the back of the tally board; Maeryn nods (`EGA-D11.60`). Seredh's workroom becomes a rest point (stool). |
| **Give it to the lamp-house** (`strained`) | The stone is on a custody shelf under the Covenant's seal; Ondine is grateful. | It is warm in the lamp-house; Seredh's request was not kept. His trust is strained, not broken. | EH-M6: no line. **Mendable** at any time after completion by `S07_mend`, which sets `kept`. |

Neither choice exposes Seredh, names him, or gives the Covenant anything but a stone. No later content treats the lamp-house's custody as sinister in fact; the player's unease, if any, is the player's.

### EMS.10 Rewards, failure, death, walk-away, co-op

| Reward | Type | Notes |
|---|---|---|
| **A cold pebble** (`kept` only) | Keepsake (functional: none) | From Seredh. Flavour; inspect text only. |
| **Seredh's stool** (`kept`, or after the mend) | Access | Rest point (keep watch) in the workroom. |
| Small payment | Currency | Maeryn, not Seredh, pays for the Ridge walk ("He won't. He'd carve you something instead, and you'd have to carry it.") [GD]. |
| Skill XP | Actions only [GD] | Mining (Option A only). |

| Situation | Handling |
|---|---|
| No Mining | Seredh's chisel; slow, never blocked. |
| Entering the red stretch | Heavy damage; the stone speaks (presentation); nothing fails. |
| Death on the road | Respawn at the working gate's niche, stone in hand, step intact. |
| Setting the stone down and walking off | It stays where set (per player). If the player logs out, it returns to Seredh's shelf and he hands it back (re-wrapping is automatic). |
| Walking away | Stays Active. Resume: `EMS-B1.02` (workroom) or `EMS-B2.01` (Seam). |
| Fail state | None. Strained is a choice, and it is mendable. |
| Co-op (CDR-6) | Per §0.6. Each player carries their own stone, meets their own Ondine and sets their own `EH_UNBURNT`. A partner may walk alongside and wet their own wool. The seat and the silence are per player. |

### EMS.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| Two-handed carry-state (no attack, climb or agility) | Systems | The EH-M5 ewer carry rule ("no attacking while carrying"), extended to block climb (Integration EI-CA-04, bulky class). Reused. |
| Set-down / pick-up of a carry-state prop, per player | Systems | Standard placeable carry-state. |
| `ems.silence` audio state (3 s full ambient mute in one volume) | Audio | A mix snapshot on the Seam volume. |
| Stone account playback (sound + view haze) | Audio/VFX | As EH-M3's stone (`EGH-D9.10`). Reused. |
| Post-completion flag write (`S07_mend`) | Systems/Schema | A dialogue node on a Completed quest that writes `EH_UNBURNT`. Standard dialogue-sets-flag; the quest's state does not change. |

No new runtime system.

**Mystery ledger.**

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **What the stone holds** | One maker's memory of keeping a mark while the Ash Roads were scraped (R09 weight). | — | The stone (one account). | It proves who scraped the roads, or when. | Whose hands; when; what else Seredh keeps. | None (ED-12). |
| **Why the Seam is cold; the silence** | Unknown. | "It's a sad place." | — | It is Stonebound; it is the dead. | Everything. **Never explained.** | None. |

**Open decisions.**
1. **The mend after strained.** The bible says strained is "mendable by a later visit". This package implements the mend inside EMS as an optional post-completion step so `EH_UNBURNT` keeps one writer. If the Director prefers strained to be final, cut `S07_mend` and `EMS-D7`.
2. **Ondine at the Seam.** She keeps her own vigil there; her grief is never explained. If the Director prefers the collector to be a different lamp-keeper from EST's visitor, swap the name; only `EMS-D4.01`–`.03` change.

| Review finding | Revision |
|---|---|
| Draft stone showed the Hollow night from a new angle. | Replaced with the Ash Roads scraping (R09 is EH-M3's; weight only here). |
| Draft let the player take a mourner's stone from the ledge to bed the memory-stone. | Cut: the mourners' stones are inspect-only. The seat is cut or chiselled. |
| Draft had the stone "wear" as a hidden meter if carried warm. | Cut: no meter (ED-6). Entering red plays a fragment once and sets a flag for one line. |
| Draft let Ondine refuse to return the stone on the mend. | Cut: she returns it on asking. The mend must be reachable solo and without a fight or a trick. |

### EMS.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Seredh Embercarver** [CANON] | His stones; his terms. | — | Stoic, few words, exact. Unshakable once he trusts. Silence is an answer. |
| **Ondine Thursk** [NEW] | The lamp-house custody shelf; Deepbrand seizure notices at the gate; her own grief. | What Hearthveil does below the lamp-house. | Kind, slow, sincere. Never threatens; never pleads. |
| **Maeryn Vall** [CANON] | That Seredh is in her yard. | — | As EST. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| EMS-B1.01 | Maeryn | Available | *"There's somebody in my lean-to who wants your arms. Not you. Your arms."* |
| EMS-B1.02 | Seredh | Active, at the workroom | *(He looks up; says nothing; looks at the door to the lane.)* |
| EMS-B1.03 | Maeryn | Available, `ETB_TAUGHT` set | *"Idra's chimes. I hear them from here at dusk. Three notes. Never in a row."* |
| EMS-B2.01 | Ondine | Active, at the Seam before `S03` | *"Peace on your flame. Sit if you like. It's quiet here."* |
| EMS-B2.02 | Ondine | Completed, `strained`, at the lamp-house | *"Your stone's on the shelf. Nobody touches the shelf."* |
| EMS-B2.03 | Maeryn | Completed, `kept` | *"He sat in my kitchen last night. He doesn't sit in my kitchen."* |

#### Nodes

```
EMS-D1 (the workroom; S00)
EMS-D1.01 SEREDH: (at the cutting block; doesn't stop) "Sit."
EMS-D1.02 SEREDH: "A stone needs to go where no heat rises."
EMS-D1.03 SEREDH: "The Cold Seam. Past the Ash Roads. I don't walk the Ash Roads in daylight."
  > "I'll carry it."                                  → EMS-D1.10
  > "Why there?"                                       → EMS-D1.20
  > "Not now."                                         → EMS-D1.40
EMS-D1.10 SEREDH: (puts the chisel down) "Good."   {quest Active; event: S00}
EMS-D1.20 SEREDH: "Warm stone talks. Talk wears it." (beat) "And a woman in grey has asked Maeryn twice about carved stones."   → EMS-D1.03 options
EMS-D1.40 SEREDH: "It has waited. Warm, it waits worse."
```

```
EMS-D2 (the workroom; S01)
EMS-D2.01 SEREDH: (unwraps a basalt stone the size of two fists)
EMS-D2.03 [EGH_STONE_HEARD] SEREDH: "You held one already."
EMS-D2.04 SEREDH: "Hold it. Once. So you know what you carry."
  {interaction: hold the stone; EMS-DOC1 plays}
EMS-D2.20 SEREDH: "That is what it holds. One hand. One morning. One mark kept."
EMS-D2.21 SEREDH: "You may say a Volkhari stone remembers marks scraped from the road. Not whose stone. Not whose hands."   {EMS_HEARD}
EMS-D2.22 SEREDH: (holds out a wool bundle and the bucket) "Wet. Wrap. Both hands on the road."
  {interaction: soak wool; wrap stone (2 segments)}
EMS-D2.25 SEREDH: "Wet the wool at every niche. Your wardens' rule. It's a good rule."
EMS-D2.26 SEREDH: (gives a cold chisel) "In the rock. Not on it. If your arms can't cut, this can. Slowly."
EMS-D2.30 SEREDH: "Go by the working gate. Don't run. It doesn't like running."   {event: S01}
```

```
EMS-D4 (the Cold Seam; S03)
EMS-D4.01 ONDINE: (on the far bench; an unlit lamp beside her) [EST_ONDINE_MET] "Warden's hand. From the seamstress's counter." / [else] "Peace on your flame."
EMS-D4.02 [EST_CARD = taken] ONDINE: "You kept my card."
EMS-D4.03 ONDINE: "I sit here for somebody of mine. Once a season." (she does not say who)
EMS-D4.05 ONDINE: (sees the wool bundle; stands) "That's a carved stone. Ember-carved. I've seen them in the lamp-house."
EMS-D4.06 ONDINE: "Let me take it into care. Please. Deepbrand crews walk this road. They sign seizures of anything Volkhari at the gate. I've read the notices."
EMS-D4.07 ONDINE: "The lamp-house has a custody shelf under the Covenant's seal. Families leave things with us they can't keep. Nobody touches the shelf."
  > "Why do you want it?"                                     → EMS-D4.10
  > [ESS_RECORD_READ] (Think about the rooms below the lamp-house.)   → EMS-D4.20
  > "It goes here. That's what was asked."                    → EMS-D4.30
  > "Take it. Keep it safe."                                  → EMS-D4.40
EMS-D4.10 ONDINE: "I don't want it. I want it kept." (beat) "I've seen what the gate does with things that are carved."   → EMS-D4.07 options
EMS-D4.20 (inner voice) "Below the lamp-house there are rooms with braziers and a record of who slept there. She keeps the hall upstairs. Whether she knows what is below, you don't know."   → EMS-D4.07 options
EMS-D4.30 ONDINE: (sits again) "Then I'll sit at the far end, and I won't look." (she turns her back and lights her lamp)   {event: S03; → S04}
EMS-D4.40 ONDINE: (writes in a small custody book; tears out the stub) "'Received into care: one carved stone, wool-wrapped, from the warden's hand. To be returned on asking.'" (beat) "On asking. Any day."   {EMS_RECEIPT; EH_UNBURNT = strained; she takes the stone in both hands; event: S03; S04 skipped}
EMS-D4.41 ONDINE: "Peace on whoever it is." (she goes down the road, carefully)
```

```
EMS-D5 (the Cold Seam; S04)
EMS-D5.01 (inspect the chalk crosses) "Three faint chalk crosses below the ledge. Not new."
EMS-D5.20 (The stone goes into the seat. The wool comes away cold. For three seconds nothing in Emberholt makes a sound.)   {event: ems.silence; EH_UNBURNT = kept}
EMS-D5.21 ONDINE: (from the far end, without turning) "It does that sometimes. When someone leaves something."
EMS-D5.22 ONDINE: "Peace on whoever it is."   {event: S04}
```

```
EMS-D6 (the workroom; S05)
EMS-D6.01 SEREDH: (doesn't look up) "Where."
EMS-D6.02 [EH_UNBURNT = kept] "In the Seam. In the rock."  /  [= strained] "In the lamp-house. On their custody shelf."
EMS-D6.04 [kept; EMS_WOOL_KEPT] SEREDH: "Cold all the way." (a nod)
EMS-D6.05 [kept; not EMS_WOOL_KEPT] SEREDH: "You forgot the water once. It's still a stone."
EMS-D6.06 [EMS_STONE_SPOKE] SEREDH: "It spoke on the road. A little went." (beat) "Most of it didn't."
EMS-D6.08 [kept] SEREDH: [EMS_SEAT = cut] "You cut it a seat. Good." / [= chiselled] "My chisel. Slow. Good."
EMS-D6.10 [kept] SEREDH: (takes a small cold pebble from the shelf; holds it out) "From the Seam. Someone else's. Given back to me a long time ago. Now it's yours to give back."
EMS-D6.20 [strained] SEREDH: (a long silence) "You did what you thought would keep it." (beat) "It isn't where I asked."
EMS-D6.21 [strained; EMS_RECEIPT] SEREDH: "Lamp-keepers keep receipts. If you ask, they'll give it. The Seam is still there."
EMS-D6.30 SEREDH: (back to his chisel) "Go on."   {event: S05 → quest Completed}
EMS-D6.31 MAERYN: (in the yard, paying the player) "He won't. He'd carve you something, and you'd have to carry it."
```

```
EMS-D7 (post-completion; strained only; S07_mend)
EMS-D7.01 ONDINE: (at the lectern or by the custody shelf) "Warden's hand."
  > (Show the receipt.) "I'm asking."                      → EMS-D7.10
EMS-D7.10 ONDINE: (reads her own stub; takes the stone from the shelf) "'To be returned on asking.' You're asking." (she gives it back, still wrapped) "I hope wherever it goes is cold."   {stone carry-state; journal: Carry the stone to the Cold Seam.}
EMS-D7.30 (on seating at the Seam) {event: ems.silence; EH_UNBURNT = kept}
EMS-D7.40 SEREDH: (next visit) "It's where I asked." (beat) "Thank you."   {pebble given if not before}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| EMS-I1.01 | The wrapped stone | *"Heavy, two fists of basalt in wet wool. Through the wool you can feel cut lines."* |
| EMS-I2.01 | A scraped kerb carving (Ash Roads) | *"A kerbstone with a burnt engraving along it. In the middle a patch has been scraped smooth, long ago, with an iron tool."* |
| EMS-I3.01 | Mourners' stones (ledge) | *"Small cold stones in a row, each the size of a thumb. Left for someone. Not yours to move."* |
| EMS-I3.02 | Flarecap check at the Seam | *"Nothing glows here."* |
| EMS-I4.01 | Chalk crosses | *"Three faint chalk crosses below the ledge. Not new."* |
| EMS-I5.01 | The receipt | *"'Received into care: one carved stone, wool-wrapped, from the warden's hand. To be returned on asking. O. Thursk.'"* |
| EMS-I5.02 | The cold pebble | *"A small stone, cold in the hand however long you hold it."* |

---

# Standalone quests

---

## ENW — The Half-Name Wall

### ENW.1 Hook

**Remember:** a pay line in a steadier hand than the lines before it. **Want next:** to know where a burned man goes when he will not be counted.

### ENW.2 Selection record and canon grounding

Rejected: finding Corm or a trail to him (ED-16: never met; "walked out; not found since"); the Mire entry as a second hold proving identity (ED-16: optional echo, never a hold, implies no route).

| Element | Source | Status |
|---|---|---|
| The lower-forge shift hands were civilians above the chamber; some never found; at least one walked out burned and was not counted | Bible §2.2 | [NEW, bible] |
| Corm Brask, never met; Imra Brask keeps his name "in case"; recorded "walked out; not found since" | Bible §5.2, ED-16, §7.6 | [NEW, bible] |
| The plaque: *In memory of the shift hands of the lower forge, lost in the collapse.* | Act I `ECW` inspect (EDS09 surface) | [NEW, Act I] |
| The second sheet: *Shift above (lower forge): not ours. Not entered.* | Act I §C, dialogue file | [NEW, Act I] |
| `told`: Hesper chalks *NOT A COLLAPSE* on the plaque; "ENW: Imra Brask reads the chalk" | Act I §C9.3 | [NEW, Act I] |
| MDS09: *"A man come in burned, from the fire roads, he said. Would not give his name. Healed in the hands. Left before the thaw. Said thank you to the roots."* | `Caelmor_Mire_Side_Quests_Settlements_and_Combat.md` MDS09 | [NEW, Mire]; read only |
| Half-Name Wall: damaged or incomplete memorial; one solved omission must not imply a single author for all omissions | Part 3 proposal (landmarks table) | [Part 3; NEW] |
| The forge pay-house; Perrin Sedgwick; the "Fire" weeks | This package | [NEW] |

### ENW.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `emberholt.side.the_half_name_wall` |
| Series | Standalone (Register of the Unreturned, Emberholt case) |
| Type | Memory/lore |
| Unlock | `emberholt.main.03_hollow_that_should_not_burn` Completed. Imra is at the wall at dusk or morning (`ENW-D1`); Cooling House bark `ENW-B1.01`. |
| Length | 30–40 minutes |
| Combat share | 0% |
| Skills | **Smithing ~[GD: low]**: dress the tongs' handle at the Cooling House forge (heat, scrape the scale, quench) to raise the burnt mark. Time-cost alternative: soak the tongs in the quench trough overnight (keep watch to morning) and scrub with sand (a 3-segment channel) (`ENW_TONGS = soaked`). |
| Choice | What the wall says (`EH_HALF_NAME` = named / held). |
| Outputs | **`EH_HALF_NAME`**; `ENW_ECHO_TOLD` (optional) |
| **Anchor** (contract) | The Register of the Unreturned; Cinderwall households (Imra Brask). |
| **World-truth row** (contract) | **H18** (the Hollow hidden as a forge collapse; civilians above the chamber), H23 (recovery: uncertain names). |
| **Revelation role** (contract) | **Supports R09** (civilians above the chamber were counted lost; one walked out). Register case (bible §7.6). No new fact about the ritual. |
| **Recurring evidence** (contract) | **The wall** (Imra's half-name; read in place) + **the lower-forge pay list** (the pay-house binding; Perrin Sedgwick's custody; read in place). Both in Emberholt. The tongs authenticate the mark (object). The Mire Rootrest book is an optional echo only (`MDS09_READ`), **never a custodian**. |
| **State compliance** (contract) | Inactive → Active on `ENW-D1` accept; Completed on `ENW-D7` end. No fail: wrong pages show other weeks; the soak replaces the forge. Both wall wordings are honest. Resume hook: Imra at the wall (`ENW-B1.02`). |
| **Combat compliance** (contract) | None. No encounter, no hazard. **CDR-6 solo test:** every step is one player's; nothing needs a second player; no reward depends on co-op. |

### ENW.4 The places

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. The old lower forge** (EP11) | The plaque | The walled yard; the bronze plaque, green at the edges, with its list of names (as EH-M1). `told`: *NOT A COLLAPSE* chalked across it (per player). |
| **B. The Half-Name Wall** (EP12) | The wall panel (`S01`, `S05`) | The yard wall's outer face beside the plaque. Panels of soot-dark stone with part-names in chalk and in scratches: *TEL—*, *ORRI M—*, *the boy from the bakehouse*, *MA— (red scarf)*. Some panels are clean, some black. A **wire brush** and a **water pail** at the wall's foot that mourners use. |
| **C. Imra's house** [NEW sub-site of EP02] | The tongs (`S02`) | A terraced room in Cinderwall's slag lanes. A **tool-box** under the bed with a forge-hand's things in it, returned "when they walled the yard": tongs, a leather apron gone stiff, a tally of pay chits. |
| **D. The Cooling House forge** (EP02 hub) | Dress the tongs (`S02`, Option A) | As Act I. |
| **E. The forge pay-house** [NEW sub-site of EP25] | The binding (`S03`, `S04`) | A long room at the Emberforges where every forge's pay was drawn at a **window**. Bound pay lists on high shelves, by forge, each spine with a forge mark; a **shelf index** board; a rolling **ladder**; a reading table. **Perrin Sedgwick** at the window. |

**MAP VERIFICATION REQUIRED** for Imra's house and the pay-house.

### ENW.5 Player-facing sequence

Exact wording lives in ENW.12; beats cite node ids.

**Beat 0: Imra (`S00_offer`).** *Objective: Speak to Imra Brask at the Half-Name Wall.* `ENW-D1`. Imra cleans one panel each season with a wet brush. By `EH_HOLLOW_TRUTH`: `told`, she has read *NOT A COLLAPSE* on the bronze and asks what he was lost in (`ENW-D1.02`); `kept`, she has heard the warden's hand went below on a Marshal's warrant and asks who else was down there (`ENW-D1.03`). Her mother put half his name here "in case"; she wants to know if "in case" was ever true. Accept: Active.

**Beat 1: The wall (`S01_wall`).** *Objective: Clean Corm's panel and read the plaque.* **Brush** the panel (3-segment channel; segments persist): *CORM BR—*, and beside it a small scratched mark, Imra's mother's copy of the way he marked his things (`ENW-I1.01`). **Read the plaque** (`ENW-I1.02`; with `EDS09_SEEN`, `ENW-I1.03`): *Brask, Corm* among the lost. Completes on `ENW-D2.20`.

**Beat 2: The tongs (`S02_tongs`).** *Objective: Raise the mark on Corm's tongs.* At Imra's house, his **tool-box**, returned when the yard was walled (`ENW-I2.01`): tongs, an apron, pay chits. A mark is burnt into the tongs' handle under black scale (`ENW-I2.02`). Imra lends the tongs (carry-state).
- **Option A (skill): Smithing ~[GD: low]**, at the Cooling House forge: **heat** the handle (the hood tell goes amber and the prompt says *Out now* before red), **scrape** the scale (2-segment channel), **quench**. `ENW_TONGS = dressed`.
- **Option B (time-cost):** soak overnight in the quench trough (keep watch to morning), then **scrub** with trough sand (3-segment channel). `ENW_TONGS = soaked`.
Take a **rubbing**: paper over the handle, charcoal across (one interaction; carry-state; `ENW-I2.03`). Sets `ENW_RUBBING`. The tongs go back to Imra. Completes on the rubbing.

**Beat 3: The pay-house (`S03_payhouse`).** *Objective: Find the lower forge's last pay week.* At the Emberforges, **Perrin Sedgwick** at the pay window (`ENW-D3`): the pay-house keeps every forge's lists, and no binding leaves the room. The **shelf index** (`ENW-I3.01`) gives the shelf; roll the **ladder**, climb, carry the binding to the reading table. It is headed in the forge's own count, *Fire* weeks (numbered from each relighting after a cold stop), and was rebound out of order. Page spreads (three weeks each) and read the headings; the last week is found by its heading and the clerk's line *Forge closed. No further lists.* (`ENW-I3.04`). Wrong spreads hold ordinary weeks. On the right spread:
- **Before the night** (`ENW-I3.05`): *Brask, C.* and his mark, ordinary, among the week's names.
- **After the night** (`ENW-I3.06`): every line of the last day struck through in a later, browner ink with *lost: collapse* written over it, except one: *Brask, C. Drawn. Paid at the window; hands bound.* His mark beside it is steadier than the clerk's hand above.
Sets `ENW_LINE_READ`. Completes on the second read.

**Beat 4: The match (`S04_match`).** *Objective: Match the mark.* *Show* the rubbing on the open binding: it matches (`ENW-I4.01`). Perrin (`ENW-D4`): that is a hand that drew its own pay, and the pay-house does not pay the lost; he knows no more. `ENW_TONGS` varies one line (`ENW-D4.10`). Sets `ENW_MATCH`. Completes on `ENW-D4.20`.

**Beat 5: The wall (`S05_wall`).** *Objective: Tell Imra what the wall should say.* At the wall, dusk or morning (`ENW-D6`). The player sets the two holds side by side: the wall (her mother's half-name and copied mark) and the pay list (his own mark, after the night, "hands bound"). With `EGH_SHEET_READ` the player may recall the second sheet's *Shift above (lower forge): not ours. Not entered.* (`ENW-D6.12`); nothing about the ritual is explained beyond what `EH_HOLLOW_TRUTH` already let Cinderwall hear. **Optional echo `[ED-16]`** (`ENW-D6.30`, with `MDS09_READ`): the player may tell her of a care-book entry read far from here, for a burned man who would not give his name and thanked the roots. Imra decides how much to hope (`ENW-D6.32`). It is not a hold, names no route, direction or distance, and she does not ask. The choice (`EH_HALF_NAME`):
- **Named.** Imra scratches the rest: *CORM BRASK. Walked out. Not found since.* She chalks *walked out* beside his name on the plaque (per-player prop states).
- **Held.** She leaves *CORM BR—*: "in case" is still true, and truer now.
Completes on `ENW-D7`.

### ENW.6 Encounters and hazards

None. The forge in Option A is ordinary forge heat with an amber/red hood tell as a timing cue; a red heat only makes the prompt say *Too hot. Let it cool.*, with no damage.

### ENW.7 The strange moment: the steadier hand (Beat 3)

| Time | Element | Spec |
|---|---|---|
| On reading `ENW-I3.06` | **The page** | The clerk's lines for the last day are hurried and blotted. The later *lost: collapse* overwrites are in another, browner ink. Corm's line is in the clerk's same hurried hand, but **his mark** beside it is larger, slower and steadier than anything on the page: made by a man with bound hands, pressing hard. |
| Optional | **Perrin** | `ENW-D3.30` (if the player asks about it): "Burned men press hard. So they don't drop the pen." |
| What it means | | Nothing beyond what it shows. It is a page, not a phenomenon; the evidence is the record, not the steadiness. |

### ENW.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Speak to Imra Brask at the Half-Name Wall. | `ENW-D1` accept | Yes |
| `S01_wall` | Clean Corm's panel and read the plaque. | `brush_panel` 3 segments **and** `ENW-I1.01` **and** `ENW-I1.02` **and** `ENW-D2.20` | Yes |
| `S02_tongs` | Raise the mark on Corm's tongs. | (heat + scrape 2 segments + quench **or** keep watch + scrub 3 segments) **and** `take_rubbing` | Yes |
| `S03_payhouse` | Find the lower forge's last pay week. | Binding at the table **and** `ENW-I3.05` **and** `ENW-I3.06` | Yes (any order with `S02`) |
| `S04_match` | Match the mark. | *Show* rubbing on the pay line **and** `ENW-D4.20` | Yes (needs `S02`, `S03`) |
| `S05_wall` | Tell Imra what the wall should say. | `ENW-D6` choice **and** `ENW-D7` end | Yes (→ Completed) |

### ENW.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `ENW_TONGS` = dressed / soaked | `S02` | `ENW-D4.10` |
| `ENW_RUBBING` | `S02` | `S04` |
| `ENW_LINE_READ` | `S03` | `S04`, `ENW-D6.10` |
| `ENW_MATCH` | `S04` | `S05` |
| `ENW_ECHO_TOLD` `[ED-16]` | `ENW-D6.30` (optional) | `ENW-D7.04`; nothing else, anywhere |
| **`EH_HALF_NAME` = named / held** | `ENW-D6.40` / `.50` | Memorial props (EP11, EP12); EDS09 reading layer (request); CV-M1 Register (request) |

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Named** | *CORM BRASK. Walked out. Not found since.* on the wall; *walked out* chalked beside his name on the plaque. | The memorial now says, in public, that one of the "lost" was not lost in it. With `kept`, Cinderwall barks start asking questions (`ENW-B2.04`). Imra has to live with "not found since". | EDS09 reading shows one name chalked over (request). CV-M1 Register: case resolved in Emberholt (request). |
| **Held** | The half-name stays. Imra writes nothing new. | The plaque still counts him lost. Only Imra and the player know. | CV-M1 Register: case known, held (request). |

Neither value says where he went or why he did not come home.

### ENW.10 Rewards, failure, death, walk-away, co-op

| Reward | Type | Notes |
|---|---|---|
| **Supper at Imra's** | Access | Imra feeds the warden's hand whenever they pass (a rest bench in her house). |
| Small payment | Currency | Imra tries to pay; the player may refuse (flavour) [GD]. |
| Skill XP | Actions only [GD] | Smithing (Option A only). |
| **The pay-house** | Access | Perrin lets the warden's hand read any forge's old lists (flavour inspects; used by later content on request). |

| Situation | Handling |
|---|---|
| No Smithing | The soak and scrub. |
| Wrong pay week | Other weeks show; no penalty. |
| *Show* rubbing on a wrong line | Perrin: "Not that one. That's somebody's cousin." |
| Death | No damage sources on the path. |
| Walking away | Stays Active. The tongs and the rubbing (carry-state) return to Imra if the player logs out holding them; she hands back the rubbing on the next talk. Resume: `ENW-B1.02`. |
| Fail state | None. |
| Co-op (CDR-6) | Per §0.6. Wall and plaque wording show the viewer's own value. |

### ENW.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| Paged binding with headings, out of order | UI | The Mire MBA paged document view (three entries per spread, headings readable). Reused. **Fallback:** dialogue list of week headings. |
| *Show* carry-state on a document line | Systems | Use-object-on-prop with a match id (MBA pattern). Reused. |
| Per-player wall panel and plaque chalk states | Systems/Art | Per-player prop variants: panel soot / clean / named; plaque clean / `told` chalk / `told` + named chalk / `kept` + named chalk. |
| Forge heat timing on a small object | Systems | Existing Smithing heat interaction with the hood tell as cue. |

No new runtime system.

**Mystery ledger.**

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Corm Brask** | A civilian shift hand above the chamber; walked out burned; drew his pay; was not counted; not found since (bible §2.2). | Lost in the collapse. | The wall; the pay list; his mark. | He was part of what happened below; or he caused it; or he is surely the Mire's burned man. | Where he went; why he did not come home; whether he lived. | Here (Register; Emberholt). |
| **The man from the fire roads** (Mire MDS09) | Unknown. | — | One care-book line, far away. | It is Corm. | Everything. **Never confirmed** (ED-16). | None. |

**Open decisions.**
1. **ED-16 stands.** If the Director cuts the Mire echo, delete `ENW-D6.30`–`.33`, `ENW_ECHO_TOLD` and `ENW-D7.04`; nothing else changes.
2. **Who overwrote "lost: collapse".** The browner ink is a later clerk's; the pay-house does not know whose. Recommendation: leave it unknown in Emberholt (D-C03; Part 3: one solved omission must not imply a single author for all omissions).

| Review finding | Revision |
|---|---|
| Draft let Imra ask the player how far away the Mire book was. | Cut: no route, distance or direction (ED-16; bible §11 item 10). |
| Draft had the pay list name the other lost by count ("eleven lines struck"). | Cut: no counts. "Every line from the last day." |
| Draft let the plaque's other names be completed too. | Cut: one case only; the other half-names stay as they are. |
| Draft used the tongs as a second hold. | Fixed: the holds are the wall and the pay list (bible §7.6); the tongs authenticate the mark. |

### ENW.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Imra Brask** [NEW, bible] | Her mother's stories; the half-name; the tool-box. | What happened to him. | Practical, dry, stubborn; has cleaned the same panel for years and pretends it is a chore. |
| **Perrin Sedgwick** [NEW] | Every forge's pay lists; how pay was drawn. | Why anyone overwrote anything. | Precise, fond of his bindings, unhurried; a little funny about it. |
| **Corm Brask** | — | — | Never appears; never speaks. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| ENW-B1.01 | Hennet | Available | *"Imra Brask's at the forge wall again with her brush. Ask her what for. She'll tell you it's a chore."* |
| ENW-B1.02 | Imra | Active, returns | *"Still says 'BR' and a line. I check."* |
| ENW-B2.01 | Perrin | `S03`, at the window | *"Every forge's pay. Every week. Some of it twice."* |
| ENW-B2.03 | Imra | Completed, `named` | *"Not found since. I say it in the morning. It's better than 'lost'."* |
| ENW-B2.04 | A Cooling House regular | Completed, `named` + `EH_HOLLOW_TRUTH = kept` | *"Somebody's chalked the forge plaque. 'Walked out.' Out of a collapse?"* |
| ENW-B2.05 | A Cooling House regular | Completed, `named` + `told` | *"Not a collapse, and one walked out. Write that on the board too."* |
| ENW-B2.06 | Imra | Completed, `held` | *"In case. Truer now."* |

#### Nodes

```
ENW-D1 (the Half-Name Wall; S00)
ENW-D1.01 IMRA: (brushing one panel; doesn't stop) "Warden's hand."
ENW-D1.02 [EH_HOLLOW_TRUTH = told] IMRA: (points the brush at the bronze plaque, chalked NOT A COLLAPSE) "Not a collapse." (beat) "Then what was he lost in?"
ENW-D1.03 [EH_HOLLOW_TRUTH = kept] IMRA: "They say you went under the forge with a Marshal's paper. Was anybody else down there?"
ENW-D1.04 IMRA: "My mother's brother. Corm. On the plaque with the lost. My mother put half his name on this wall. In case."
ENW-D1.05 IMRA: "I'd like to know if 'in case' was ever true."
  > "I'll find out what can be found."             → ENW-D1.10
  > "In case of what?"                             → ENW-D1.20
  > "Not now."                                     → ENW-D1.40
ENW-D1.10 IMRA: (hands over the brush) "Start with the soot. I've done my bit."   {quest Active; event: S00}
ENW-D1.20 IMRA: "In case he came back to finish it." (beat) "Nobody does. Everybody writes it."   → ENW-D1.05 options
ENW-D1.40 IMRA: "Wall's not going anywhere. Neither's the soot."
```

```
ENW-D2 (the wall; S01)
ENW-D2.01 [panel clean] IMRA: "'CORM BR', and a line. And that's his mark. Mother copied it off his tongs. Badly."
ENW-D2.10 [plaque read] IMRA: "Brask, Corm. Between a Telling and a Mott. Not that Mott."
ENW-D2.20 IMRA: "His tongs are under my bed. They came home in his box when they walled the yard. The mark's under the black. I've never got it off."   {event: S01}
```

```
ENW-D3 (the pay-house; S03)
ENW-D3.01 PERRIN: (at the window, without looking up) "Pay's drawn at the forges now, friend. This window's for the books."
ENW-D3.02 PERRIN: "The lower forge? We have it. Every forge's lists come here. Theirs came when they walled the yard." (beat) "It doesn't leave the room. Nothing leaves the room."
ENW-D3.03 PERRIN: "Index board, ladder, table. It's rebound out of order. The binder was in a hurry. Everyone was, that year."
ENW-D3.10 [player asks about the Fire weeks] PERRIN: "Each time a forge is relit after a cold stop, the count starts again. Fire one, Fire two. You find a week by its fire."
ENW-D3.20 [ENW_LINE_READ] PERRIN: (comes round; reads over the player's shoulder) "That's a struck week." (beat) "Except that one."
ENW-D3.30 [optional, the steadier mark] PERRIN: "Burned men press hard. So they don't drop the pen."
```

```
ENW-D4 (the pay-house; S04)
ENW-D4.01 (show the rubbing on the line)
ENW-D4.10 PERRIN: [ENW_TONGS = dressed] "That rubbing's sharp. Somebody's dressed a handle." / [= soaked] "That rubbing's soft at the edges. Soaked, was it? Still reads."
ENW-D4.12 PERRIN: (lays the rubbing beside the line; looks a long time) "Same mark."
ENW-D4.14 PERRIN: "'Drawn. Paid at the window. Hands bound.'" (beat) "That's a hand that drew its own pay. We don't pay the lost."
ENW-D4.16 PERRIN: "Who wrote 'lost' over the rest, I couldn't say. Not a pay-house hand. We don't write over."
ENW-D4.20 PERRIN: (closes the binding gently) "I'll put a slip in it. 'Read by the warden's hand.' That's all I'll put."   {ENW_MATCH; event: S04}
```

```
ENW-D6 (the wall; S05)
ENW-D6.01 IMRA: (the brush in her lap) "Well?"
ENW-D6.10 (The player sets it out: the half-name and her mother's copy of his mark; the pay line after the night, his own mark, 'hands bound'.)
ENW-D6.11 IMRA: (quiet) "He drew his pay." (beat) "Burned. And drew his pay. And didn't come home."
ENW-D6.12 [EGH_SHEET_READ] (inner voice) "On the second sheet, below Cinderwall: 'Shift above (lower forge): not ours. Not entered.'"
  > (Tell her the shift above was never counted by whoever was below.)    → ENW-D6.14
  > (Say nothing of the sheet.)                                            → ENW-D6.20
ENW-D6.14 IMRA: "Not counted." (beat) "That's what 'lost' was, then. Not counted."   → ENW-D6.20
ENW-D6.20 IMRA: "Two things say he walked. Mother's wall and his own hand." (beat) "Neither says where."
  > [MDS09_READ] "Far from here, I read a care-book. A burned man who wouldn't give his name. He said thank you to the roots."   → ENW-D6.30
  > "What do you want the wall to say?"                                → ENW-D6.38
ENW-D6.30 [ED-16] IMRA: (a long breath) "Burned. Wouldn't give his name." (beat) "That's every burned man there is."   {ENW_ECHO_TOLD}
ENW-D6.32 IMRA: "I'll hope a little. Not so it hurts." (beat) "Don't tell me where it was. I'd go, and he wouldn't be there."
ENW-D6.33 (She does not ask more. Nothing more is said about it.)   → ENW-D6.38
ENW-D6.38 IMRA: "You read it. I'll write what you say."
  > "Finish his name. 'Walked out. Not found since.'"                   → ENW-D6.40
  > "Leave it half. In case."                                           → ENW-D6.50
ENW-D6.40 IMRA: (scratches the rest of the name with a nail from her pocket, slowly; a line under it) "'CORM BRASK. Walked out. Not found since.'"
ENW-D6.41 IMRA: (takes chalk to the bronze; beside his name, small) "'Walked out.'" (beat) "There. Let them clean that."   {EH_HALF_NAME = named; prop states per player}   → ENW-D7.01
ENW-D6.50 IMRA: (looks at the half-name a long time) "In case is still true." (beat) "It's truer now."   {EH_HALF_NAME = held}   → ENW-D7.01
```

```
ENW-D7 (close)
ENW-D7.01 IMRA: "Come and eat. You've been in a pay-house. Nobody eats in a pay-house."
ENW-D7.02 IMRA: [named] "My mother would have hit you for making me cry. Then fed you." / [held] "My mother would have done the same. Then fed you."
ENW-D7.04 [ENW_ECHO_TOLD] IMRA: "A little. Not so it hurts." (she does not say it again)
ENW-D7.05 IMRA: (the brush back on its hook)   {event: S05 → quest Completed}
```

#### Inspect texts and documents

| Id | Object | Text |
|---|---|---|
| ENW-I1.01 | Corm's panel (clean) | *"Scratched, old: CORM BR, and a line. Beside it a small mark, scratched less sure: a ring with a hook through it."* |
| ENW-I1.02 | The plaque | *"In memory of the shift hands of the lower forge, lost in the collapse. A list of names. Among them: Brask, Corm."* With `told`: *"Across the bronze, in crew chalk: NOT A COLLAPSE."* |
| ENW-I1.03 | The plaque (`EDS09_SEEN`) | *As above, then:* *"You have read this plaque before. You did not read the names."* |
| ENW-I1.04 | Other half-names | *"TEL—. ORRI M—. 'The boy from the bakehouse.' MA— (red scarf). Some clean. Some black."* |
| ENW-I2.01 | The tool-box | *"A forge-hand's box. Tongs, an apron gone stiff as board, a twist of old pay chits. A label: 'Returned. Lower forge.'"* |
| ENW-I2.02 | The tongs (before) | *"Heavy forge tongs. On the handle, under a black crust of scale, something burnt in."* / after: *"A ring with a hook through it, burnt deep. Sure."* |
| ENW-I2.03 | The rubbing | *"Charcoal on paper: a ring with a hook through it."* |
| ENW-I3.01 | Shelf index | *"Forge marks in a column, each with a shelf. The lower forge's mark, struck through once, with its shelf beside it: top row."* |
| ENW-I3.04 | The last week's heading | *"'Lower forge. Fire' and a number. Under the week, in the clerk's hand: 'Forge closed. No further lists.'"* |
| ENW-I3.05 | Before the night | *"The week's first days. Names and marks down the column, each paid. 'Brask, C.' and a ring with a hook through it."* |
| ENW-I3.06 | After the night | *"The last day. Every line struck through in a later, browner ink, and over each: 'lost: collapse.' Except one, not struck: 'Brask, C. Drawn. Paid at the window; hands bound.' Beside it his mark, bigger and steadier than anything else on the page."* |
| ENW-I4.01 | Rubbing on the line | *"The ring. The hook through it. The same."* |
| ENW-I5.01 | The panel (`named`) | *"CORM BRASK. Walked out. Not found since. The new scratches are pale against the old."* |

---

## EGT — Glassmoth's Tonic

### EGT.1 Hook

**Remember:** a sleeper on a bench saying another person's dream. **Want next:** to know who keeps the second room's nights, and how many other stairs there are.

### EGT.2 Selection record and canon grounding

Rejected: Glassmoth proving all three dreams induced (R12 is never a universal explanation; Part 4 ledger); Glassmoth's sense as evidence (the evidence is the access book and the chamber record).

| Element | Source | Status |
|---|---|---|
| Jatha "Glassmoth" Nirel: underworld dream-dealer; diluted, non-lethal dream tonics; former Hearthveil initiate horrified by weaponized visions; empathetic; guilty; can sense when visions are externally manipulated | Character file §32; bible §5.1 ("Sells relief for dreams; not Remnant") | [CANON] |
| Induced visions proven by access pattern + chamber record; never dismiss all Dreamers | Revelation Ledger R12; bible §8.1 | [APPROVED] |
| The vigil access book chained to the lectern; the chamber record with "set", "hand" (light / full), "carried", and a setter's mark; Serix's "not set" column | Act II §B6 Beat 4 (`ESS-I7`, `ESS-I9`) | [NEW, Act II] |
| Serix Arden: knows how visions are seeded; witnesses copies; will not let originals leave | Act II §B6 Beat 4; bible §5.1 | [CANON]; [NEW, Act II] |
| True Dreamers begin after the war; no existing anchor is newly labelled one | Part 4 ledger | [CANON constraint] |
| No player dreams | Bible ED-17 | [PROPOSAL — DIRECTOR] |
| Mattea Orsk, Dorrit Vane, Sabeth Tamber, the stall | This package | [NEW] |

### EGT.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `emberholt.side.glassmoths_tonic` |
| Series | Standalone (Dreamers) |
| Type | Memory/lore |
| Unlock | `emberholt.main.05_the_speakers_smile` Completed. **Held under the §0.6 frost rule (playability audit ES-02):** the stall is in Cinderwall, so while `EGA_FROST` is set (EH-M6 `S00`–`S06`) it is shut and EGT is not offered; it opens at `EGA_THAW_SEEN`. Glassmoth's bark `EGT-B1.01` as the player passes her arch; `EGT-D1` on talk. |
| Length | 30–40 minutes |
| Combat share | 0% |
| Skills | **Cooking ~[GD: low]**: reduce Glassmoth's syrup at her brazier, stirring and taking it off when the pot's tell shows amber. Time-cost alternative: keep watch while she does it (`EGT_BATCH = waited`). |
| Choice | What Mattea and Dorrit are given (`EGT_TONIC` = told / sold). |
| Outputs | `EGT_TONIC` |
| **Anchor** (contract) | Dreamers (Glassmoth and three customers); Hearthveil (Serix, the lamp-house). |
| **World-truth row** (contract) | H21 (dreams and visions: some induced, some not). |
| **Revelation role** (contract) | **Supports R12** (one more access pattern: two sleepers, one night, one room, one set motif). Never dismisses all Dreamers: Sabeth's dream is in no book. No D-S1-dependent content. |
| **Recurring evidence** (contract) | **Customer accounts** (three living witnesses) + **the lamp-house access book** (public, chained; Covenant custody) + **the chamber record** read by its keeper Serix (Hearthveil custody; not copied). |
| **State compliance** (contract) | Inactive → Active on `EGT-D1` accept; Completed on `EGT-D11` end. No fail: a scorched pot is re-done; a wrong comparison is corrected; the vigil hall is always open (Act II rest point). Both choice branches are the same length. Resume hook: Glassmoth's stall (`EGT-B1.02`). |
| **Combat compliance** (contract) | None. No encounter, no hazard. Serix, Glassmoth, the customers and lamp-keepers are never targetable. **CDR-6 solo test:** every step is one player's; the three accounts, the book and the choice are per player; no reward depends on co-op. |

### EGT.4 The places

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Glassmoth's stall** [NEW sub-site of EP02, under an arch in the slag lanes] | Offer; the batch; the compare; the choice (`S00`, `S01`, `S03`, `S06`) | A plank counter under a brick arch, hung with **emberglass charms** that chime when the wind moves them. A small iron **brazier** with a tell in its rim and a copper **pot**. Rows of small stoppered bottles, mostly empty. A slate with no names on it. **MAP VERIFICATION REQUIRED.** |
| **B. Embergate yards** (EP01) | Mattea (`S02`) | Crates stacked by the gate scales; porters with shoulder pads; a weigh-clerk's booth. |
| **C. Selice Morra's workshop** (EP03, C3) | Dorrit (`S02`) | As EEH. Dorrit at the grinding wheel. Selice at her furnace. |
| **D. Sabeth's bench** [NEW sub-site of EP02] | Sabeth (`S02`) | A lamp-mender's bench at a slag-lane corner: wicks, oil cans, glass chimneys, a stool. |
| **E. The Covenant lamp-house vigil hall** (EP22, L1) | The access book; Serix (`S04`, `S05`) | As Act II. Vigil-goers dozing on benches. The **access book** chained to the lectern. |

### EGT.5 Player-facing sequence

Exact wording lives in EGT.12; beats cite node ids.

**Beat 0: Glassmoth (`S00_offer`).** *Objective: Speak to Glassmoth at her stall.* `EGT-D1`. Three customers came the same morning with the same dream from the same night. She is sure two were "put in"; she kept vigil rooms once; she knows nobody listens to the woman who sells the bottle. With `ESS_SLIP_SEEN`, `EGT-D1.12`. Accept: Active.

**Beat 1: The batch (`S01_batch`).** *Objective: Help Glassmoth make up a batch.* **Option A (skill): Cooking ~[GD: low].** At the brazier: pour her base and mix (she will not name the mix), **stir** (3-segment channel, ~4 s each) while the brazier tell moves clear to amber, **take it off** on amber. If it goes red the syrup scorches: tip it out and start again; only time is lost. **Bottle.** `EGT_BATCH = self`. **Option B (time-cost):** keep watch on her upturned crate while she brews (`EGT-D2.10`). `EGT_BATCH = waited`. Completes on the bottling.

**Beat 2: The three (`S02_customers`).** *Objective: Hear the three customers' dream.* Glassmoth says where to find them. Any order; each is a short job while they talk.
- **Mattea Orsk**, gate-yard porter: carry two crates from the stack to the scales (`EGT-D3`). Sets `EGT_ACCOUNT_M`.
- **Dorrit Vane**, Selice's apprentice: hold a glass blank on the rod while he grinds (3-segment channel) (`EGT-D4`). Sets `EGT_ACCOUNT_D`.
- **Sabeth Tamber**, lamp-mender: trim three wicks while she oils chimneys (`EGT-D5`). Sets `EGT_ACCOUNT_S`.
Each tells the dream and where they slept. Mattea (her mother's year-night) and Dorrit (sent for steadying twice a season) kept vigil at the lamp-house. Sabeth slept at home.

**Beat 3: Compare (`S03_compare`).** *Objective: Lay the three accounts side by side.* At the stall (`EGT-D6`): choose which accounts match. Mattea's and Dorrit's agree in every detail, including the words "rest, and be steady". Sabeth's stair goes down, with nobody at the top and no words. A wrong pick gets Glassmoth's correction and the options again. Sets `EGT_COMPARED`. Her feeling proves nothing; the lamp-house keeps a book.

**Beat 4: The vigil book (`S04_book`).** *Objective: Read the access book for that night.* At the vigil hall, the chained **access book** (`EGT-I5.02`; with `ESS_ACCESS_READ`, `EGT-I5.01` first): that night, the **second room**, *Orsk, M., year-night* and *Vane, D., steadying*. Sabeth's name is on no night the player pages (`EGT-I5.03`). With `EST_ONDINE_MET`, Ondine at the lectern says it is a public book (`EGT-D7.03`). **The strange moment** (EGT.7). Sets `EGT_BOOK_READ`.

**Beat 5: Serix (`S05_serix`).** *Objective: Ask Serix Arden about that night.* Serix comes up from the dormitory stair (`EGT-D8`) and remembers the warden's hand. He will not take the player below again and will not allow a copy. He goes down alone (keep watch, or wait at the lectern) and reads out only that night's entry: second room; light hand; set: *a stair, lit*; carried: nothing written (as on Act II's light-hand rows). Sabeth is not in it. With `ESS_RECORD_READ` the player may ask whose mark set it (`EGT-D8.27`: "Not mine," and nothing else) and whether his "not set" column has anything that night (`EGT-D8.28`: it does not). Sets `EGT_SET_HEARD` (`EGT-D8.30`).

**Beat 6: What they're given (`S06_choice`).** *Objective: Decide with Glassmoth what Mattea and Dorrit are given.* `EGT-D9`. They want sleep, or they want to know; Glassmoth cannot tell which. The choice (`EGT_TONIC`):
- **Tell them.** Glassmoth will not sell to them this time. The player carries what the book and the record show to each (`EGT-D10.10`–`.25`). Mattea will keep her mother's year-night at home; Dorrit will ask his master not to send him. Neither is told what to do.
- **Sell them the tonic.** Two doses. The player carries the **bottles** (`EGT-D10.30`–`.45`); they pay and will sleep without dreaming. Nobody tells them where the stair came from.
**In both branches** the player visits **Sabeth** (`EGT-D10.50`–`.56`): her dream is in no book. She wanted to know if it was hers or theirs, and keeps it. Glassmoth sells her nothing.
Completes at the stall (`EGT-D11`).

### EGT.6 Encounters and hazards

None. The brazier's red tell only scorches the syrup (no damage).

### EGT.7 The strange moment: the sleeper on the bench (Beat 4)

| Time | Element | Spec |
|---|---|---|
| On reading `EGT-I5.02` | **The sleeper** | On the nearest vigil bench a woman the player has never met (a vigil-goer, role only) is asleep under a grey blanket. As the player reads the second room's names, she says, clearly, in her sleep: *"Rest, and be steady."* Then she turns over and is quiet. |
| After | **Lamp-keeper** | If Ondine is present: she looks at the sleeper, then down, and turns the nearest lamp down a notch (EME03 practice). She says nothing. |
| What it means | | Nothing is shown about who she is, which room she slept in, or whether she was set. She is never identified and the player cannot wake her or question her. **Not evidence.** Sets `EGT_MURMUR_HEARD`; read by nothing, deliberately. |

### EGT.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Speak to Glassmoth at her stall. | `EGT-D1` accept | Yes |
| `S01_batch` | Help Glassmoth make up a batch. | (`stir` 3 segments + `take_off` at amber + `bottle` **or** keep watch one turn) | Yes |
| `S02_customers` | Hear the three customers' dream. | `EGT_ACCOUNT_M` **and** `_D` **and** `_S` | Yes |
| `S03_compare` | Lay the three accounts side by side. | Correct compare **and** `EGT-D6.20` | Yes |
| `S04_book` | Read the access book for that night. | `EGT-I5.02` **and** `EGT-I5.03` | Yes |
| `S05_serix` | Ask Serix Arden about that night. | `EGT-D8.30` (`EGT_SET_HEARD`) | Yes |
| `S06_choice` | Decide with Glassmoth what Mattea and Dorrit are given. | `EGT-D9` choice **and** two deliveries (truth or bottles) **and** Sabeth (`EGT-D10.56`) **and** `EGT-D11` end | Yes (→ Completed) |

### EGT.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `EGT_BATCH` = self / waited | `S01` | `EGT-D11.03` |
| `EGT_ACCOUNT_M` / `_D` / `_S` | `S02` | `S03` |
| `EGT_COMPARED` | `S03` | `S04` |
| `EGT_BOOK_READ` | `S04` | `S05`, `EGT-D9.02` |
| `EGT_MURMUR_HEARD` | `egt.sleeper` event | None (deliberately) |
| `EGT_SET_HEARD` | `S05` | `S06` |
| **`EGT_TONIC` = told / sold** | `EGT-D9.20` / `.30` | Stall barks; Mattea's and Dorrit's barks |

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Told** | Mattea and Dorrit know their dream was set in the second room. They choose for themselves. | Glassmoth loses two customers. Mattea is shaken (`EGT-D10.14`); Dorrit has to ask his master for something. Neither sleeps better tonight. | Barks: Mattea keeps her year-night at home; Dorrit asks not to be sent. |
| **Sold** | They sleep without dreaming. | They do not know. If they go back to vigil, the stair may be set again; the bottle only stops them seeing it. Glassmoth's guilt (`EGT-D11.05`). | Barks: they come back for more. |

Neither choice reaches the Council, the Covenant or the Speaker. Nothing here changes `EH_SPEAKER` or any later quest. Sabeth's outcome is the same in both.

### EGT.10 Rewards, failure, death, walk-away, co-op

| Reward | Type | Notes |
|---|---|---|
| **Glassmoth's stall** | Access | She sells the warden's hand a plain sleep draught [GD: item pass defines it, or it is flavour]. |
| Small payment | Currency | Glassmoth pays in coin and refuses to be thanked [GD]. |
| Skill XP | Actions only [GD] | Cooking (Option A only). |

| Situation | Handling |
|---|---|
| No Cooking | Keep watch while she brews. |
| Scorched syrup | Tip it out; start again. |
| Wrong compare | Glassmoth corrects; options again. |
| Death | No damage sources on the path. |
| Walking away | Stays Active. Carried bottles (carry-state) return to the stall on logout. Resume: `EGT-B1.02`. |
| Fail state | None. |
| Co-op (CDR-6) | Per §0.6. The access book is a public prop read per player. |

### EGT.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| Pot tell on a Cooking interaction (clear → amber → red over a stir channel) | Systems | The Emberholt tell prop on the brazier rim, driven by channel progress. Standard Cooking interaction with a state prop. |
| Compare-accounts interaction | UI | A dialogue with three recalled accounts and a pick (MBA's *show* pattern in dialogue). **Fallback:** Glassmoth asks "Which two?" with three options. |
| `egt.sleeper` ambient line on a non-interactable NPC | Systems/Audio | A one-shot bark on a sleeping ambient NPC triggered by the inspect. |

No new runtime system.

**Mystery ledger.**

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The stair dream** | Set in the second room for two vigil sleepers (bible §2.3; R12); why is not shown here. | "A lot of people are dreaming of stairs." | Two identical accounts; the access book; Serix's reading of the record. | Every dream in the city is set; or none is. | Who set it; why. | R12 (EH-M5; this is one more case); any purpose is CV-M4's (R18). |
| **Sabeth's stair** | Hers. | — | It is in no book. | It was set too; or it is prophecy. | Everything. | None. |
| **The sleeper** | Unknown. | — | — | She proves the dream is everywhere. | Who she is. **Never explained.** | None. |

**Open decisions.**
1. **The setter's mark.** In the record the mark is *C. Vorr* (Act II); Serix says only "Not mine". Calynne Vorr appears only as a name in a record (bible §5.1). Recommendation: keep it unsaid here.
2. **"Carried" (independent review, 2026-11-15).** The draft had Serix read *carried: to the vigil roll* and add "That's what it's for. To bring them back." With Dorrit's *steadying* entry that stated a purpose for setting dreams in young sleepers, which pre-empts R18 (CV-M4). Cut to *nothing written*, matching Act II's light-hand rows. If the Director wants a purpose seeded, it belongs to CV-M4; only `EGT-D8.24` and `EGT-D9.02`–`.03` would change.

| Review finding | Revision |
|---|---|
| Draft let Glassmoth's charms chime at set dreams. | Cut: a phenomenon would be identifying evidence. The charms chime with the wind. |
| Draft had Sabeth's dream end in "someone crying, a long way down". | Cut: it echoed the never-explained sob in the pipes (`ECW_SOB_HEARD`, read by nothing, deliberately). Her stair now simply goes down with nobody at the top. |
| Draft let the player copy the record a second time. | Cut: Serix refuses; he reads it aloud. The access book is public. |
| Draft had Glassmoth sense the player's dreams. | Cut: no player dreams (ED-17). |

### EGT.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Glassmoth** (Jatha Nirel) [CANON] | Her customers; her tonic; what a set dream feels like to her. | Who sets them now. | Gentle, melancholy, guilty, wry. Never names her mix. |
| **Mattea Orsk** [NEW] | Crates; her mother's year-night. | — | Loud, practical, proud of her shoulders; shaken under it. |
| **Dorrit Vane** [NEW] | Glass; his master's errands. | — | Young, earnest, a little vain about his grinding. |
| **Sabeth Tamber** [NEW] | Wicks, oil, her own dream. | — | Old, unhurried, amused, entirely sure of herself. |
| **Serix Arden** [CANON] | The record; how a dream is set; his "not set" column. | Who sets what he did not. | Soft, careful, frightened in a careful way (Act II). |
| **Selice Morra** [CANON] | Glass. | — | Speaks to the glass. |
| **Ondine Thursk** [NEW] | The hall. | What is below. | As EST. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| EGT-B1.01 | Glassmoth | Available | *"Warden's hand. You stood in his crowd. Come and stand at my counter."* |
| EGT-B1.02 | Glassmoth | Active, returns | *"The bottles are where you left them. So am I."* |
| EGT-B1.04 | A slag-lane regular | Available, `EH_SPEAKER = challenged` (D-S1, ruled 2026-11-15) read only | *"Since the Priestess spoke, half the lane's buying Glassmoth's bottles. The other half's buying lamp oil."* |
| EGT-B1.05 | A slag-lane regular | Available, `EH_SPEAKER = exposed` (D-S1, ruled 2026-11-15) read only | *"Something's sealed up at the Hall. Nobody says what. Glassmoth's busy."* |
| EGT-B2.01 | Mattea | Completed, `told` | *"Year-night at home this year. Mother'd have preferred it. She hated the lamp-house."* |
| EGT-B2.02 | Mattea | Completed, `sold` | *"Slept like a crate. Best night in a season."* |
| EGT-B2.03 | Dorrit | Completed, `told` | *"I asked. He said, 'Fine, grind instead.' So I'm grinding."* |
| EGT-B2.04 | Dorrit | Completed, `sold` | *"No stairs. Just black. It's restful. I think."* |
| EGT-B2.05 | Sabeth | Completed | *"Went down again last night. Nobody there. I said hello anyway."* |

#### Nodes

```
EGT-D1 (the stall; S00)
EGT-D1.01 GLASSMOTH: (the charms chime) "Warden's hand. Sit on the crate. It's a good crate."
EGT-D1.02 GLASSMOTH: "Three of mine came in the same morning. Same reason. The same dream, they said. The same night."
EGT-D1.03 GLASSMOTH: "Two of them were put in. I can tell." (beat) "I kept vigil rooms once. I left. I can tell."
EGT-D1.04 GLASSMOTH: "That isn't proof. Nobody listens to the woman who sells the bottle. They'll talk to you."
EGT-D1.12 [ESS_SLIP_SEEN] GLASSMOTH: (sharp) "And before you ask: slips? Somebody sells dreams on slips? Not me."
  > "I'll ask them."                                  → EGT-D1.20
  > "What does your tonic do?"                        → EGT-D1.30
  > "Not now."                                        → EGT-D1.40
EGT-D1.20 GLASSMOTH: "They come back at dusk. And I've nothing to give them. First help me with the pot."   {quest Active; event: S00}
EGT-D1.30 GLASSMOTH: "Stops you seeing anything when you sleep. That's all. It's weak. It's meant to be." (beat) "People want their nights back."   → EGT-D1.04 options
EGT-D1.40 GLASSMOTH: "They'll dream it again tonight. Come when you can."
```

```
EGT-D2 (the stall; S01)
EGT-D2.01 GLASSMOTH: "Base in. Mine in." (a twist of paper she doesn't explain) "Stir. Watch the bead in the rim. Off at amber. Red, and it's burnt sugar and we start again."
  > "I'll stir."                                      → EGT-D2.05
  > "You do it. I'll sit."                            → EGT-D2.10
EGT-D2.05 GLASSMOTH: "Slow. You're not churning butter."   {Cooking; EGT_BATCH = self}
EGT-D2.06 [scorched] GLASSMOTH: "Burnt sugar. Tip it. Again. Everyone burns the first."
EGT-D2.10 GLASSMOTH: (stirring) "When I kept rooms, we breathed with them. Slow. And you put a picture in the breath." (beat) "I stopped. That's all the history you get."   {keep watch; EGT_BATCH = waited}
EGT-D2.20 GLASSMOTH: (bottling) "Mattea Orsk, porter, the gate yards. Dorrit Vane, the glass apprentice at Selice Morra's. Sabeth Tamber, mends lamps at the corner. No names on my slate. I just know them."   {event: S01}
```

```
EGT-D3 (the gate yards; Mattea; S02)
EGT-D3.01 MATTEA: (a crate on one shoulder) "Glassmoth sent you? Grab the other end of that one. Talk while you lift."
EGT-D3.02 MATTEA: (walking to the scales) "Stairs. Lamps on the stairs. Each one lights as you get to it. Up and up."
EGT-D3.03 MATTEA: (second crate) "At the top a warm room. And somebody says, 'Rest, and be steady.' Kind. Like Mother used to."
EGT-D3.04 MATTEA: "I wake up and want to go back. To the lamp-house. Not to the dream. To the lamp-house. That's what frightens me."
EGT-D3.05 MATTEA: "That night? I was there. Mother's year-night. I keep vigil for her once a year."   {EGT_ACCOUNT_M}
```

```
EGT-D4 (Selice's workshop; Dorrit; S02)
EGT-D4.01 DORRIT: (at the wheel) "Hold the rod. Don't breathe on the blank."
EGT-D4.02 SELICE: (from the furnace, not turning) "He's mine. Don't keep him."
EGT-D4.03 DORRIT: (grinding) "Lamps on a stair. They light when you reach them. Up. A warm room. 'Rest, and be steady.'"
EGT-D4.04 DORRIT: "I wake up wanting to go and sleep at the lamp-house again. I don't even like the lamp-house. The cots are short."
EGT-D4.05 DORRIT: "That night? Lamp-house. Master sends us for steadying twice a season. Says it's good for our hands."   {EGT_ACCOUNT_D}
```

```
EGT-D5 (Sabeth's bench; S02)
EGT-D5.01 SABETH: (oiling a chimney) "Trim those. Square, not pointed. Pointed smokes."
EGT-D5.02 SABETH: "A stair of lamps. Yes." (beat) "Going down. Under everything. Each lamp lit already."
EGT-D5.03 SABETH: "Nobody at the bottom. Nobody says anything. I'm not frightened. I go down and look and come back up."
EGT-D5.04 SABETH: "I've had it since I could hold a wick. Heard the other two at the stall and thought, well, me too, that night. I have it most nights."
EGT-D5.05 SABETH: "Lamp-house? Never been. I mend lamps. I don't sit with them."   {EGT_ACCOUNT_S}
```

```
EGT-D6 (the stall; S03)
EGT-D6.01 GLASSMOTH: "Well? Lay them out. Which are the same?"
  > "Mattea and Dorrit. Word for word."              → EGT-D6.20
  > "All three. Stairs and lamps."                    → EGT-D6.10
  > "Dorrit and Sabeth."                              → EGT-D6.10
EGT-D6.10 GLASSMOTH: "Listen again. Hers goes down. Nobody at the top. Nobody talks."   → EGT-D6.01 options
EGT-D6.20 GLASSMOTH: "Two. I said two." (beat) "Same stair, same room, same words. 'Rest, and be steady.' And both woke wanting the lamp-house."   {EGT_COMPARED}
EGT-D6.22 GLASSMOTH: "My feeling's no good to anyone. The lamp-house keeps a book of who sits which night. It's chained to a lectern. Anyone can read it."   {event: S03}
```

```
EGT-D7 (the vigil hall; S04)
EGT-D7.01 (inner voice, at the lectern) "The night Glassmoth named."   {inspect EGT-I5.02}
EGT-D7.03 [EST_ONDINE_MET] ONDINE: (at the lectern, lamp-oil on her hands) "Warden's hand. It's a public book. Read what you like." (she goes back to her lamps)
EGT-D7.10 (On the nearest bench a woman asleep under a grey blanket says, clearly: "Rest, and be steady." She turns over and is quiet.)   {event: egt.sleeper}
EGT-D7.11 [Ondine present] (Ondine looks at the sleeper, then down, and turns the nearest lamp down a notch. She says nothing.)
```

```
EGT-D8 (the vigil hall; Serix; S05)
EGT-D8.01 SERIX: (up the dormitory stair, barefoot; stops) "The warden's hand."
EGT-D8.02 SERIX: "You're at the book again. That's the public one. You want the other."
  > "One night. The second room. Two sleepers."         → EGT-D8.10
EGT-D8.10 SERIX: "I won't take you down. I won't let it be copied. Once was a copy. Twice is a habit."
EGT-D8.11 SERIX: "I'll read it. You'll hear it. That's what I'll do."
  {Serix goes below; keep watch at the lectern (or wait ~20 s); he returns}
EGT-D8.20 SERIX: (quietly) "Second room. Two sleepers, the names in your book. Light hand."
EGT-D8.22 SERIX: "Set: a stair, lit."
EGT-D8.24 SERIX: "Carried: nothing written. Light hands mostly aren't." (beat) "I read what's there. I don't read what isn't."
EGT-D8.26 SERIX: "The mark isn't mine."
  > [ESS_RECORD_READ] "Whose is it?"                          → EGT-D8.27
  > [ESS_RECORD_READ] "Your 'not set' column. Anything that night?"   → EGT-D8.28
  > "And the third woman? Sabeth Tamber?"                     → EGT-D8.29
  > "Thank you."                                              → EGT-D8.30
EGT-D8.27 SERIX: "Not mine." (nothing else)   → EGT-D8.26 options
EGT-D8.28 SERIX: "Nothing. Nobody woke with anything I didn't set, that night. Or that anyone set." (beat) "Some nights there is."   → EGT-D8.26 options
EGT-D8.29 SERIX: "Not in the record. Not any night I keep." (beat) "Whatever she dreams, nobody here gave it to her."   → EGT-D8.26 options
EGT-D8.30 SERIX: (goes back down) "Don't come a third time. I'd tell you."   {EGT_SET_HEARD; event: S05}
```

```
EGT-D9 (the stall; S06)
EGT-D9.01 GLASSMOTH: (lays two bottles on the counter) "Well."
EGT-D9.02 [EGT_BOOK_READ] (The player tells her: the second room, the two names, Serix's reading: set, light hand, a stair, lit.)
EGT-D9.03 GLASSMOTH: (a long breath) "Set. Light hand." (beat) "That's how it was when I kept rooms. That's why I left."
EGT-D9.04 GLASSMOTH: "They want sleep. They don't want a lecture. Or they want to know. I can't tell which. You heard them."
  > "Tell them. Let them choose."                    → EGT-D9.20
  > "Sell them the tonic. Let them sleep."          → EGT-D9.30
EGT-D9.20 GLASSMOTH: (puts the bottles back) "Then I don't sell to them this time. Go and tell them. Tell them plain."   {EGT_TONIC = told}
EGT-D9.30 GLASSMOTH: (stoppers two doses; hands them over) "Then take these. They've paid already, in my head."   {EGT_TONIC = sold; carry-state: two bottles}
EGT-D9.40 GLASSMOTH: "And Sabeth. Tell Sabeth whatever you found. She's been waiting a long time to be told she's fine."
```

```
EGT-D10 (deliveries; S06)
EGT-D10.10 [told] MATTEA: (sets a crate down) "Second room. Set." (beat) "On Mother's night."
EGT-D10.14 [told] MATTEA: "I'll keep her year-night at home. She'd have liked that better. She hated the place." (her voice goes, comes back) "Thank you. Go away now."
EGT-D10.20 [told] DORRIT: (stops the wheel) "Set. For steadying." (beat) "I'll ask him not to send me. He'll say grind instead. I'd rather grind."
EGT-D10.25 [told] SELICE: (from the furnace) "Grind, then."
EGT-D10.30 [sold] MATTEA: (takes a bottle; pays) "No stairs tonight. Good." (beat) "Thank you."
EGT-D10.40 [sold] DORRIT: (takes a bottle) "Black. Just black?" (beat) "That'll do."
EGT-D10.45 [sold] (inner voice) "Neither asks where the stair came from. You don't say."
EGT-D10.50 SABETH: (trimming) "Well?"
EGT-D10.52 (The player tells her: hers is in no book, no record, no night at the lamp-house.)
EGT-D10.54 SABETH: (laughs) "Mine, then. I thought so. I didn't want her bottle anyway. I wanted to know if it was mine or theirs."
EGT-D10.56 SABETH: "I'll keep it. I like going down and looking."
```

```
EGT-D11 (the stall; close)
EGT-D11.01 GLASSMOTH: (the charms chime in the wind)
EGT-D11.03 GLASSMOTH: [EGT_BATCH = self] "Your batch was good. Don't take up the trade." / [= waited] "You sit well. That's half of this trade."
EGT-D11.04 [told] GLASSMOTH: "Two less customers. Good." (beat) "That's a strange thing for me to say."
EGT-D11.05 [sold] GLASSMOTH: "They'll sleep. If they go back, the stair will be waiting, and my bottle just shuts their eyes to it." (beat) "I know what I sell."
EGT-D11.06 GLASSMOTH: (pays the player) "Don't thank me."   {payment; event: S06 → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| EGT-I1.01 | The brazier tell | *"A bead set in the brazier's rim. Clear."* / stirring: *"Amber."* / too long: *"Red."* |
| EGT-I1.02 | Glassmoth's charms | *"Emberglass drops on threads. They chime when the wind comes under the arch."* |
| EGT-I1.03 | Her slate | *"A slate with marks for bottles sold. No names."* |
| EGT-I5.01 | The access book (`ESS_ACCESS_READ`) | *"The vigil access book, on its chain. You have read this book before."* |
| EGT-I5.02 | The access book, that night | *"The night Glassmoth named. First room: two names. Second room, in a lamp-keeper's hand: 'Orsk, M., year-night.' 'Vane, D., steadying.' Third room: no name that night."* |
| EGT-I5.03 | The access book, Sabeth | *"You page back and forward through the season. 'Tamber' is nowhere."* |

---

## Package review log (cross-quest)

| Check | Result |
|---|---|
| **Bible fit (§7.1, §7.2, §7.3, §12)** | Five codes, titles, types, unlocks, places and verbs as the bible lists them. EST settlement, ETB and EMS memory/lore, ENW memory/lore (Register), EGT memory/lore (Dreamers). Contract fields copied from §7.3 and expanded. `EH_UNBURNT` kept / strained (EMS) and `EH_HALF_NAME` named / held (ENW) are the only region flags set, as §9.1 lists; each has one writer. |
| **Unlocks against the acts** | EST after EH-M2; ETB after EST and EH-M4; EMS after ETB and EH-M3; ENW after EH-M3; EGT after EH-M5, matching Act I "Unlocks across Act I" and Act II "Unlocks across Act II" exactly. |
| **Main-line reads** | Every main-line flag read (§0.4) exists in the act files with the same name and values; every "promised" line (`EEH_CLASS_DONE`, `EAC_BREATH`, `EAC_MAERYN_SAID`, `EGH_STONE_HEARD`, `ESS_SLIP_SEEN`) is used verbatim. `ECW_SOB_HEARD`, `EEH_LANTERNS_SEEN` and `EAC_EMBERLIGHT_SEEN` ("read by none, deliberately") are not read. |
| **CDR-1 / CDR-2** | No encounters; nothing to defeat; no yield or retreat language. Ranged not relevant; never required. |
| **CDR-6** | Every step, choice and reward solo; partner credit only from the partner's own active step; choices and flags per player; no co-op-only mechanic; a partner leaving blocks nothing. |
| **CDR-4** | Standard systems only (carry-state, channels with kept progress, keep watch, inspect, *show*, paged document, tells). No new runtime system; the integration rows reuse EEH, EH-M5, Mire MBA and Act I patterns. |
| **Reserved decisions** | D-E2 (ruled 2026-11-15): only `ETB-D5.10`, freed; `.11` cut. D-S1 (ruled 2026-11-15): no assertion; two barks read `EH_SPEAKER` for mood. ED-3 (Iven Calder, ruled 2026-11-15): not used. ED-12: Maeryn's, Kaelen's, Asera's and Seredh's own disclosure in every node; no option to give anyone away. ED-16: ENW's echo optional, unconfirmed, no route. ED-17: no player dreams. |
| **Revelation Ledger** | Owns nothing. Supports R09 (EMS weight; ENW civilians), R12 (EGT access pattern), R18 (ETB practice). R19: one canon line (Kaelen's dream), never evidence. No reveal of R15, R16, R18 or R19. |
| **D-C03 / D-C06** | No precursor name or roster; no count of Volkhari held, living, dead or escaped; no refuge placed; Kaelith not seen, named or sought; no count of the lower forge's dead. |
| **Voice** | Civic pride; craft, never magic; fire grammar; Volkhari restraint; children are students (bible §5.3). "Warden's hand" address only. |
| **Names** | Five new minor names grepped (§0.8); six candidates rejected for near-collisions. |
| **Size** | See the independent review row below. |
| **Independent review, 2026-11-15** | Authored walkthrough against the brief, CDR-1 to CDR-6 (§3.7), the bible, Arcs, Revelation Ledger, dossier, Factions, Part 4 ledger and the reviewed Act I–III packages and dialogue (nothing was played; no build exists). **Flags:** every main-line read re-checked by name and value in the act files (all present; `EH_UNBURNT` kept / strained / unset matches Act III §inputs and `EGA-D11.60`); `EH_UNBURNT` and `EH_HALF_NAME` have one writer each. Act II's `ESS_RECORD_READ` row lists EGT but not EMS as a reader (the EMS read is optional and harmless; Act II row to be extended at integration). Fixed two wrong reader ids (`ESS_SERIX_HEARD` is read at `EGT-D8`, not `EGT-D6`; EGT completes on `EGT-D11`, not `EGT-D8`). The duplicate quest-local flag table in §0.4 had drifted (wrong reader for `EGT_BATCH`; `EST_SLEEVES_SEEN`, `EST_ONDINE_MET`, `EST_COLD_BREATH` missing) and was replaced by a pointer to the package tables; §0.5 folded to one paragraph. **Ledger (R18, Medium):** Serix's *carried: to the vigil roll* with "That's what it's for. To bring them back" (and Glassmoth's echo), beside Dorrit's *steadying*, stated a purpose for setting dreams in young sleepers; cut to *nothing written* (`EGT-D8.24`, `EGT-D9.02`–`.03`, EGT.5 Beat 5, mystery ledger, open decision 2). The access book's third-room line ("a run of the same name you have seen before") pointed at the Speaker's nights `[D-S1]`; now "no name that night". R15, R16, R19: seed only (Kaelen's one canon line). D-C03, D-C06: no counts, no roster, no refuge. Kaelen's family name is never spoken (bible cast name only). ENW's Mire echo stays optional, sets only `ENW_ECHO_TOLD`, creates no Mire requirement and states no route. **Ondine Thursk:** consistent with Act I (EEH's visitor unnamed, non-interactive, "seeded for EST") and Act II (grey cloaks); kept and swappable; open decision EST.11 item 2 now names the two texts that carry her name. **Rename:** Perrin Ardith → **Perrin Sedgwick** (near-duplicate of Serix Arden and Sarne Ardane in the Emberholt cast). **Playability:** all unlocks reachable; every quest has a physical step and a skill hook with a time-cost alternative; no softlock found; three states only. **Size:** about 168 KB after trimming the duplicate table; it remains above the 140 KB package guide. Further cuts would remove content, not redundancy (Director call). |
| **Emberholt character rulings, 2026-11-15** | D-E2: `EH_THALAN` read as `freed` only; `ETB-D5.11` (aided) cut; `[D-E2]` tags and the swap note (ETB open decision 2) resolved in the header, flow chart, §0 flag table, ETB card and beats, and the review row. D-S1: EGT's two `EH_SPEAKER` mood barks checked, unchanged (no claim of knowledge, no "only dream-fed"). ED-3: no `[INITIATE]` use here; header and review row name Iven Calder as not used. |
| Independent review of character rulings, 2026-11-15 | Remaining live `[D-S1]` tags (§0 flag table, EGS revelation-role row, `EGT-B1.04`/`.05` triggers) replaced with "(D-S1, ruled 2026-11-15)". |
| Playability audit fixes, 2026-11-15 | Playability audit fixes, 2026-11-15: ES-01, ES-02, ES-03, ES-13, CO-05, TD-10 (EMS stone sprint clause). |
| CDR-6 shared-credit clarification (§3.7 item 2a), 2026-11-15 | §0.6 co-op bullet: a shared task done together in a shared instance (e.g. EST containment parts) credits every present partner whose active step consumes it; lessons, carries, readings and choices stay per player. |
