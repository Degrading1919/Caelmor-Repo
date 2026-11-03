# Thornfell Main Questline, Act II: The Echo of Shatterfall, The Summit Hall

**Status:** Authored production content for Creative Director milestone review. This package implements Thornfell milestones TF-M3 and TF-M4 (bible §6, §6.1), which carry Act II from the end of *The Iron Winter Stores* to the Act II turn. It follows the Lowmark act-package format (`Caelmor_Lowmark_Main_Act_I.md`). Everything marked **[NEW]** is authored and not canon until the Director promotes it. Everything marked **[PROPOSAL — DIRECTOR]** rests on an open bible §3 (TD-) decision. **[CANON]** items come from Phase 1 or the reconciled `LORE/` files. No schema, production JSON or C# is created here. Nothing here is release scope (bible scope guard: Thornfell is v1.5 direction).

**Controlling document:** `04_CONTENT_PRODUCTION/Quests/Caelmor_Thornfell_Narrative_Production_Bible.md`. Its §6 table, §6.1 briefs, §5.3 voice rules, §9 flags and §11 conventions are binding and are implemented as written. Where detail had to be invented it is marked [NEW] and stays inside those briefs.

**Companion file:** `04_CONTENT_PRODUCTION/Dialogue & Narrative/Caelmor_Thornfell_Main_Act_II_Dialogue.md`. It holds cast notes, every dialogue node referenced here (`TES-`, `TSH-` prefixes), barks, inspect texts and the full text of `TES_horn_roster`, Maera's private cairn list, Iven's hum list and `TSH_trial_record`.

**Parallel dependency:** Act I (`Caelmor_Thornfell_Main_Act_I.md`, TF-M1 and TF-M2) is being authored in parallel. This package reads only what the bible defines for Act I: `TH_CALLS`, `TH_PASSWATCH_ROUTE`, `TH_STORES`, `TH_BRYNJAR`, the quest item `TIW_store_ledger` and its line of pay chits to "G. Carrick's men, Shatterfall, plates by the crate", and Eyvind's tuning sketches naming the Summit's great hall. If the Act I author names any of these differently, only the read-conditions in §A9.2, §B9.2 and the matching dialogue conditions change.

---

## Act II header

### What Act II does

Act I showed the player that a Thornfell splinter is arming on its own authority. Act II's job is to take apart the two stories that make that arming feel justified: the horn that "split the ridge" and the "guardian" on the Summit. The player does it with their ears and their hands, in places that are dangerous for ordinary reasons and strange for one reason each.

| Quest | The player learns | By doing |
|---|---|---|
| TF-M3 **The Echo of Shatterfall** | The horn that split the ridge was real, and it was aimed at the shelf where Thornfell's own rear guard stood. Two honest records about those people disagree. | Rigging two rope rescues to rock they can only find by its echo, enduring a storm-bound phenomenon, sounding a wartime plate rack, and reading a roster out of a tin. |
| TF-M4 **The Summit Hall** | The Summit "guardian" is old stone answering a horn. The splinter's tests woke it, and silencing the horn stops it. The splinter has a leader. | Mapping a hall by listening, finding dead-sound pockets, and damping a horn plate by plate between pressure pulses. |

**Act II turn (Arcs §3.1, bible §1 part 2):** Thornfell's proudest story is half a story, and its most feared wonder has no message. The last thing the player hears in Act II is nothing at all: one breath of total silence on the Summit, and a name, Ingrith Scarrow, given by a man who still thinks his horn was beautiful.

### Dependencies on Act I

| Act I state (bible §9.1, §6.1) | Read by | Effect |
|---|---|---|
| TF-M2 Completed | TF-M3 availability | TF-M3 is offered only after TF-M2 completes (bible §6 prerequisites). |
| `TIW_store_ledger` held, or TF-M2 Completed | TF-M3 lead-in, `TES-D1` | The ledger's pay-chit line ("G. Carrick's men, Shatterfall, plates by the crate") points to Carrick's Cut. With the ledger in the player's pack, the chit-nail inspect adds a match line. The quest is complete without the item. |
| `TH_CALLS` | Both quests | Call-shape glyphs display for every horn call; the echo-return glyph (§A12) displays for every sounding. Always true by Act II (TF-M1 sets it). |
| `TH_PASSWATCH_ROUTE` | `TES-D2` variant | One line from Dorn about the Narrows crossing. Flavour only. |
| `TH_STORES` = reported / seized / leverage | `TES-D1` variants; TF-M4 crew count (§B7) | Gerrit's chits are dead paper (reported, seized) or still cashing (leverage). With leverage, the Summit crew has one more spear. |
| `TH_BRYNJAR` = disowned / defended | Post-quest barks (both quests); `TSH` broken outcome lines | Brynjar's reaction to the Shatterfall account and to a broken horn. |
| Eyvind's tuning sketches (TF-M2 plate gallery; Act I flag `TIW_SKETCHES_SEEN`) | `TSH-D1` variant | If the player read them, Iven's offer adds a line: "The great hall. Your sketches said so too." Flavour; Iven's list carries the lead on its own. |

### Region flags (bible §9.1 only)

| Flag | Act II role |
|---|---|
| `TH_CALLS`, `TH_PASSWATCH_ROUTE`, `TH_STORES`, `TH_BRYNJAR` | **Read.** Act II never writes them. |
| `TH_SEASON` | **Read** as `snow` throughout Act II (TF-M2 set it). Storm presentation uses the snow prop set. |
| `TH_SHATTERFALL_ACCOUNT` = amended / beside / kept | **Set** by TF-M3 choice. Read by *The Weight of a Name*, TF-M5 Maera placement and Assembly posture (§9.3). |
| `TH_HORN` = silenced / broken / surrendered | **Set** by TF-M4 choice. Read by *The Notes We Keep*, TF-M5 lines. |

Act II invents no other `TH_` flag. Quest-local flags use `TES_` and `TSH_`. Those read by later packages are marked in each quest's flags table.

### Quest-item budget (bible §9.5: Thornfell total 4)

| Item | Quest | Fate |
|---|---|---|
| `TES_horn_roster` (the Horn Seat log tin's roster) | TF-M3 | Leaves the player's pack at the TF-M3 choice: to Maera's keeping with her list (amended), into the cairn niche (beside), or sealed under Maera's cord to the Passwatch warden post's strongbox (kept). Readable afterwards at its location (inspect). Not droppable, not sellable while held. |
| `TSH_trial_record` (Eyvind's horn-trial record) | TF-M4 | Kept by the player into TF-M5 (Assembly lines may read that it exists). Not droppable, not sellable. |

**Act II total: 2.** Everything else is a carry-state object (rope coils, anchor irons, a damped horn plate), an inspectable document held by an NPC (Maera's private cairn list, the Hushfold name-slip, Iven's hum list, Gerrit's pay chits, Iven's sketch), or knowledge carried in flags.

### Season, weather and level identity

- **Season:** `TH_SEASON = snow` for both quests. Snow cover on the stair and rim prop sets.
- **Weather:** TF-M3 runs on a **quest-local storm** (per-player presentation, never world weather), with five windows (§A8.1). TF-M4 runs in still, cold air: its only weather is what the hall does.
- **Level identity (TD-12):** both quests are tuned at **Advanced identity (Milestone 3)**. Exact levels are Gameplay Designer calls.

### Structure check against the bible §6 core verbs

| Quest | Primary verb | Distinct from |
|---|---|---|
| TF-M1 TPW | repair and escort against the clock | — |
| TF-M2 TIW | track and delve | — |
| TF-M3 **TES** | **rope-rig rescue by echo count**; endure a phenomenon; read plates and strata | The only rope work and the only rescue in Act II. Outdoors, vertical, weather-driven. Sound is **struck from rock** and counted. |
| TF-M4 **TSH** | **listen and triangulate**; find null-points; damp by ear | Indoors, still air, no storm. Sound is **heard from people and plates** and located. The player is told not to strike anything. |
| TF-M5 TSW | whiteout climb by horn alone | (Act III) |

No two quests share a set piece or a sound mechanic. TES counts returns off a face; TSH locates sources by angle and finds the loudest pitch under a hum. Combat changes family across the act: rock vipers and the Horn-Echo (TES) → ridge crows and Iron Winter crews under a hazard (TSH).

### Unlocks across Act II (bible §7)

After TF-M3: *The Weight of a Name* (TWN), *The Salvage Ledge* (TSG); *The Third Horn* (TTH) gains its richer variant; *Rope-Raising Day* (TRR) when *A Place at Smoke Week* is also complete. Shatterfall's storm event becomes revisitable. After TF-M4: *The Notes We Keep* (TNK) once *Witness at the Gate* is complete; Thornfell's **high routes**; TF-M5 (automatic on next entry to Windscar Pass or Stonewake).

---
---

# Part A — TF-M3 The Echo of Shatterfall (`TES`)

## A1. The quest in one paragraph

The pay chits in the Whinstone ledger lead the player to **Carrick's Cut**, a miners' camp at the mouth of Shatterfall Gorge, where Gerrit Carrick's out-of-work crew have been prising Echohewn horn plates out of the old collapse for a hornwright who pays by chit. A storm is coming in, and two salvage pairs are still down on the lower ledges. **Dorn Feldhorn** is already at the rim with a Ridge Warden horn, because Gerrit sent to Passwatch for one and Dorn will not let strangers near "that seat" alone. Dorn's Lost call gets two Answers back from under the overhangs: the pairs are alive, and the shelf path behind them has fallen. The player goes down the gorge between gusts, clears a jammed boulder, and at each overhang rigs a lowering line to rock they cannot see, finding **sound anchor rock by its echo**: strike the face and count; a quick, flat return is solid, a slow, doubled one is a loose slab. As the storm rises, a horn blast nobody blew rolls down the gorge and **figures form in the haze and charge**. They break when struck and come back while the storm lasts. Some of them run the wrong way, uphill, toward the Horn Seat. At the Seat's approach the figures stop running and stand across the path until the storm window turns. In the lull, Dorn and the player sound one plate on the **Horn Seat**'s rack: its echo comes back from the camp shelf below, not from the far approach. Under the seat, where the miners dug for plates, the collapse lies over a Thornfell camp: clan-stamped buckles, cookpots, a horn with Thornfell bindings. In the seat's niche is a log tin, and in the tin a roster with an hour, the word *Split*, and beneath it in another hand: *"Rear guard not recalled. No answer."* At the rim cairns, where the names have no bodies and the stones say "lost in the gorge storm", **Maera Cairnwatch** brings her private list, which says the rear guard "held the gorge" and gives a last sighting an hour after the Split. The player sets the two records side by side. Neither is a lie. The player tells Maera what they think the stone should say, and Maera decides.

**What the player should remember:** striking rock and hearing it lie or tell the truth, and the figures running uphill. **What the player should want next:** to know who is rebuilding the horn that did this, and where they are testing it.

## A2. Selection record

| Candidate | Verdict |
|---|---|
| **A. A combat descent to defeat the Horn-Echo at its "source".** | Rejected. The Horn-Echo is a canon scar that is never cured (bible §2.6); "defeating" it would imply a cause the player can remove, and it would make combat the evidence channel. |
| **B. A single rescue, then the Seat.** | Rejected. One rig teaches the echo count; the second, under the Horn-Echo, is where the player uses it under pressure. Two rigs is the brief. |
| **C. Maera reads the roster aloud and tells the player what it means.** | Rejected. The bible requires the player to set the records side by side. Maera keeps her authority over the stone, not over the meaning. |
| **D. Offer → horn and answers → storm descent → two echo-sounded rigs under a rising Horn-Echo → the stopped figures → the Seat (aim, strata, roster) → the rim (two records) → Maera's decision on the player's word** (selected; the bible brief). | **Selected.** One storm with one shape: build, peak, turn, lull, clearing. The player's competence peaks in the storm, the truth arrives in the lull, and the decision is made in clear air. |

## A3. Canon grounding

| Element | Source | Status |
|---|---|---|
| Shatterfall Gorge: wartime collapse, siege engines in the walls, armour on ledges, crumbling shelves | Dossier §V.3 | [CANON] |
| The Horn-Echo of Shatterfall: storm-triggered horn blast, echo-figures that charge blindly; resonance imprints, not spirits | Dossier §IX.1 | [CANON] |
| Echo-figures never identify anyone | Bible §2.4; Part 4 ledger (Maera row) | [CANON boundary] |
| The horn that split the ridge; Brynjar's boast | Thornfell anchors §II | [CANON] |
| Dorn: altered echoes; "some notes should never be played again"; "wind tricks" | Thornfell anchors §IV | [CANON] |
| Maera: absolute authority over the dead; "the stones know how to listen" | Thornfell anchors §V | [CANON] |
| Torvek: ends arguments with a sentence; cairns "the old way" | Thornfell anchors §II | [CANON] |
| Thornfell never speaks of its own dead at Shatterfall | World truth H16 | [APPROVED — FT-02b] |
| Who blew the horn and how many died stay withheld | Revelation ledger R06; TD-9 | [PROPOSAL — DIRECTOR] (withheld) |
| Carrick's Cut, Gerrit Carrick, the Horn Seat, the log tin, the roster, Maera's private list, the rear guard | Bible §2.1, §2.2, §4.2, §5.2 | [NEW] |
| Rock vipers; the Horn-Echo encounter family with the miniboss phenomenon "the Held Line" (design name only) | Bible §10 | [NEW] on [CANON] ecology |
| Agility triggers (no jump), walkable fallbacks | Phase 1.3 §1; bible §9.5 | [CANON]; approved, not yet implemented |

## A4. Quest summary card

| Field | Value |
|---|---|
| Working title | **The Echo of Shatterfall** |
| Suggested content id | `thornfell.main.03_echo_of_shatterfall` |
| Arc position | Act II opener; Main Arc movement "Separate weather, engineering, resonance and myth" (Arcs §3.1) |
| Prerequisite | TF-M2 Completed |
| Offer | Arrival at Carrick's Cut (`TES-D1`), led there by the TF-M2 ledger's chit line; journal lead "Carrick's men, Shatterfall" on TF-M2 completion |
| Target length | 50–65 minutes (one storm) |
| Combat share | ~30% (vipers, Horn-Echo, the stopped figures) |
| Dialogue share | ~10% |
| Traversal, rigging, sounding, reading, choice | ~60% |
| Skills | Melee (required); Mining (optional; crew alternative) |
| Choices | What becomes of the rear guard's stone: amended / beside / kept (3 options; the player recommends, Maera decides) |
| Unlocks | `TH_SHATTERFALL_ACCOUNT`; Shatterfall storm event revisitable; Carrick's Cut as a camp; *The Weight of a Name*, *The Salvage Ledge*; *The Third Horn* richer variant; TF-M4 |
| **Anchor** | Thornfell Cairn-Keepers (Maera) and Ridge Warden hornbearers (Dorn); Shatterfall Gorge; Gerrit Carrick's out-of-work miners |
| **World-truth row** | H16 (Thornfell's stop: Shatterfall), H11 (resonance forced into horns), H25 (present: the splinter's salvage) |
| **Revelation role** | **Owns R06 (horn half):** the Split killed Thornfell's own rear guard. Plants R14 (Register) via the Hushfold name-slip. Plants R06 (sealing half) via Dorn's Third Horn line. Supports R05/R07 lead-in (plates bought for the Wall-Horn). |
| **Recurring evidence** | The pay chits recur from TF-M2 (custodians: the store ledger; Gerrit's chit nail, independent). The roster recurs in *The Weight of a Name* (independent custodian: Maera's private list) and at TF-M5 only through the flag. Shatterfall plates recur in TF-M4 (custodian: the Wall-Horn's frame and Eyvind's trial record). |
| **State compliance** | Inactive / Active / Completed only. Choice recorded in `TH_SHATTERFALL_ACCOUNT`. No fail path: loose anchors cost time, never a fall; the stopped figures end when the storm window turns, whatever the player does; every required proof is on the critical path and persistent. |

## A5. The places

All placement is relative. **MAP VERIFICATION REQUIRED** for every placement in this section: the narrative needs only that Carrick's Cut sits at the gorge mouth by the rim, the ledges step down the near wall, the Horn Seat is cut into the wall above the lower "camp shelf", the far approach is the gorge's other end, and the rim cairns stand on the rim above the Seat. No compass direction toward Emberholt is asserted (TD-6).

### A5.1 Carrick's Cut [TP13]

| Area | Storytelling |
|---|---|
| **C1. The tally post and chit nail** | A post driven into the scree with a nail through a fat sheaf of **pay chits**, each stamped "W." and initialled for plates by the crate. The newest are a week old. Under them, older chits have been crossed through by someone who tried to cash them at Stonewake. **Required inspect** in `S00_cut` (sets `TES_CHITS_READ`). With `TIW_store_ledger` held, the inspect adds the match to the ledger line. |
| **C2. The plate stack** | Salvaged Echohewn plates under sacking, sorted by size. Grey Shatterfall grit in every groove (the same grit the player saw on the TF-M2 crates). Optional inspect. Touching one does nothing. That is the point. |
| **C3. The rim winch and horn rail** | A miners' winch over the drop, its rope cut short and frayed (the reason the pairs are stuck). A warden horn rail where Dorn stands. |
| **C4. The shelter** | Canvas, a cold stove, a child's carved goat on the bench (a miner's, left behind when the work went bad). Gerrit's men who did not go down wait here. |
| **C5. The overlook** | A spot on the rim where, across the gorge, the **Salvage Ledge** (TP12) shows small figures prising at the old siege works. Brigands, not miners (Gerrit: "Not mine."). Presentation only; seeds *The Salvage Ledge*. |

### A5.2 Shatterfall Ledges and the Broken Engine [TP11]

| Area | Storytelling |
|---|---|
| **L1. The Gust Stair** | The first descent: a staircase of broken shelves down the near wall. Fluted faces along it whistle up a fifth before each gust (bible wind-window convention). Old **warden shelter marks** (a chalked notch, renewed by Gerrit's men) show the faces that are always safe. Agility trigger: a shelf gap (step across). Walkable fallback: the miners' plank detour along the wall. |
| **L2. The Jam** | A boulder wedged in the shelf path where the shelf narrows. Fresh fall, from this week. Mining clears it (`S03_jam`), or Gerrit's two spare men come down and bar it out with levers. Shale around it is **rock-viper ground**. |
| **L3. The Lip (first overhang)** | A ledge above an overhang. Below and out of sight, Arni and Kolla Vass sit on a stance where their shelf path has fallen away. The face above the ledge has **five candidate seams** for anchor irons: old wartime iron scars (rust stains) and the miners' chalk ticks. Two are solid rock; three are loose slabs. |
| **L4. The Broken Engine** [TDS06] | A wartime siege engine embedded in the wall, its frame wedged as a prop. Inspect: Thornfell timber, set to hold a shelf up "before the fall". The rescued pairs shelter in its lee. It is also the respawn point for the lower gorge. |
| **L5. The Hollow (second overhang)** | Deeper and closer to the Seat. Hjalti Brekk and old Tamsin are on the stance below. **Six candidate seams**; two solid. The gorge is louder here: the Horn-Echo's blasts mask returns struck during a swell. |
| **L6. The camp shelf** | The broad lower shelf below the Horn Seat. The miners dug their plates out of the collapse here and opened a cut through it: the **strata**. Snow lies on the debris. The rescued pairs reach the gorge floor path from here and walk out. |
| **L7. The seat approach** | A shelf path about eight metres wide between the wall and the drop, climbing to the Horn Seat. Three marked shelter faces along it. The figures stop here (§A7, TES-E4). Agility trigger: a short scramble to the upper shelter face. Fallback: the ramp. |
| **L8. The miners' ladders** | Iron-pinned ladders up the wall from the camp shelf to the rim, rigged years ago and kept up by Gerrit's crew. The way out (`S08_climb_out`). |

### A5.3 The Horn Seat [TP10]

| Area | Storytelling |
|---|---|
| **H1. The seat** | A stone seat cut into the gorge wall, worn smooth where someone sat. Facing down the shelf. A snow-drift in the seat. |
| **H2. The plate rack** | An iron rack bolted into the rock beside the seat, holding Echohewn plates in a row, every plate angled **down the shelf**, toward the camp shelf below, and away from the far approach. Three slots are empty; the pry marks are fresh. **Required inspect** and the **sounding** with Dorn (`S07_seat`). |
| **H3. The log niche** | A niche at shoulder height with a lead-lidded tin, wedged shut by ice. Inside: the horn-station roster (`TES_horn_roster`). **Required pickup.** The left margin of every leaf, where duty names would sit, has rotted to lace (TD-9: who blew the horn stays withheld). |
| **H4. The strata cut** | Reached by a short path down from the seat to the camp shelf's cut face. In the cut, under the collapse: **clan-stamped buckles** (several clans' marks), **cookpots**, and a **horn with Thornfell bindings**, all on the near side of the fall. Three **required inspects**. Nothing here is a body, and nothing is countable. |

### A5.4 The Rim Cairns [TP14]

| Area | Storytelling |
|---|---|
| **R1. The cairn row** | Cairns along the gorge rim above the Seat. Each carries names cut into a facing stone and, under them, **LOST IN THE GORGE STORM**. No bodies are under them; the cairns are hollow at the base the old way (Torvek's practice). The row runs further along the rim than the path does. Three cairns are reachable and inspectable; at least one is required. |
| **R2. The reading stone** | A flat stone at the head of the row where Maera sets things down. The side-by-side interaction happens here. |
| **R3. The cairn niche** | A small niche in the largest cairn, stopped with a slate. Used in the *beside* outcome. |
| **R4. The rim path** | From the ladders' head along the rim to the row. After the storm: clear air, snow, the gorge quiet. |

## A6. Player-facing sequence

### Beat 0 — Plates by the Crate (`S00_cut`)
**Objective:** *Find Gerrit Carrick at Carrick's Cut.*
The player arrives at the gorge mouth with the weather turning: a hard wind with snow in it, and the fluted faces down the gorge already whistling. **Gerrit Carrick** is at the rim winch with a cut rope in his hands (`TES-D1`). He is defensive before the player says anything ("If you're from the Assembly, I've a licence for the scree."). His men have been salvaging plates for a hornwright who pays by chit; the chits are no good at Stonewake (variant by `TH_STORES`). Two pairs went down this morning for the last of a seam, the winch rope parted on a shelf edge, and the storm is early.
Required: inspect the **chit nail** (C1; `TES_CHITS_READ`). Optional: the plate stack (C2), the overlook (C5).
**Verbs:** arrive, talk, inspect.

### Beat 1 — Lost and Answer (`S01_answer`)
**Objective:** *Listen for the salvage pairs.*
**Dorn Feldhorn** is on the horn rail (`TES-D2`). Gerrit sent a runner to Passwatch for a warden horn to call his pairs back; Dorn brought it himself. He does not say why at once. When asked, he says only that he will not let strangers near "that seat" alone, and that he has never been down there.
Dorn blows **Lost** (one long, rising; glyph shown). The player listens at the rail. Two **Answer** calls come back (two short; glyph shown), from two different places below, each with its own echo count. Dorn counts aloud with the player: the first answer is near and under a lip (the Lip, L3); the second is further down and comes back "with the gorge in it" (the Hollow, L5). Optional: Dorn shows how to tell an answer from its echo (the echo is fainter and late; this is TF-M1's echo count, reused). He does not blow Gather: the pairs cannot come up, because the shelf path behind them is gone. He blows an Answer of his own instead ("We heard. Stay.").
**Verbs:** listen, count.

### Beat 2 — The Gust Stair (`S02_descent`)
**Objective:** *Climb down to the first overhang.*
Down the Gust Stair (L1) with Dorn following one shelf behind (he climbs slowly and does not apologise for it). The **wind window** convention runs here: the fluted faces whistle up a fifth (~2.5 s) before each gust; shelter faces are chalk-marked. A player caught in the open by a gust is pushed back toward the wall and loses a little health; never off a ledge (gust volumes push wallward only). Gust cycle ~25 s at this window.
Agility trigger: a shelf gap (step across). Fallback: the plank detour (adds ~20 s).
Two **rock vipers** and a shale-coil on the shale before the Jam (**TES-E1**).
Optional inspect: armour fragments on the ledges (dossier canon): *"A rusted plate from a shoulder. No mark you can read. The snow is filling it."*
**Verbs:** traverse, time, fight.

### Beat 3 — The Jam (`S03_jam`)
**Objective:** *Clear the jammed shelf.*
A boulder blocks the shelf path (L2).
- **Mining** (recommended): break it with a pick (channelled, 3 segments of ~4 s, segments persist). Gust tells still apply; a gust interrupts but completed segments are kept.
- **Crew alternative:** call Gerrit's two spare men (interaction at the shelter face; Dorn blows **Gather** up the gorge). They come down and bar it out with levers. Cost: they need **one full gust cycle** to arrive and another to work (about a minute), and the storm moves up to window 2 (§A8.1) one cycle earlier, so the first Horn-Echo wave at the Lip begins sooner.
Either way the path opens. (`TES_JAM_MINED` or `TES_JAM_CREW` for barks only.)
**Verbs:** mine, or call a crew.

### Beat 4 — The Lip (`S04_rig_one`)
**Objective:** *Find sound rock for two anchor irons.* Then: *Rig the line.* Then: *Lower the Vass pair.*
**The signature mechanic, taught.** Dorn explains in four short lines (`TES-D3`): an iron is only as good as the rock it is in; the rock tells you if you ask it; strike and count; quick and flat is solid, slow and doubled is a slab with air behind it. "Two irons. Never one."
- **Sounding.** The face above the Lip shows **five candidate seams** (rust scars and chalk ticks, highlighted on interaction range). The player uses **Sound the rock** on a seam (an interaction, ~1 s strike with the iron's butt). The return plays as positional audio **and**, with `TH_CALLS`, a small echo-return glyph above the seam: a single short tick (quick, flat) or two spaced ticks (slow, doubled). The interaction log also prints the result ("A quick, flat knock comes back." / "Slow. It comes back twice."). A seam can be sounded as often as the player likes.
- **Setting irons.** The player sets an anchor iron (carry state from Dorn's coil bag; two irons) into any seam with **Drive the iron** (~2 s). No confirmation is shown. The rock only tells the truth when it is loaded.
- **Rigging.** With two irons set, **Rig the line** (channelled, 2 segments of ~4 s; segments persist). Dorn ties the pair's loop and lowers the end over the Lip.
- **Lowering.** The player stands at the brake post and **Pay out** the line (channelled, **3 segments of ~5 s**; completed segments persist). Dorn blows Answer to the pair before each segment so they know when to move.
- **Loose irons.** If either iron is in a loose slab, the first loaded segment shows it: the slab shifts with a grinding crack, the iron tilts, the line jerks onto the other iron, and the segment stops (no progress lost from earlier segments; the pair is held by the other iron or by their own stance; **nobody ever falls**). Dorn: "Feel that? Pull it." The player pulls the bad iron (interaction) and sounds again. If both irons are loose, the line will not take load at all and Dorn stops the rig before the first segment. **Cost:** time. The storm is rising; every reset lets one more Horn-Echo wave reach the Lip.
- **The first Horn-Echo (TES-E2).** During the rig at the Lip the storm reaches window 2. A horn blast nobody blew rolls up the gorge (§A8.2). Haze thickens in **lanes** along the shelf and figures form in it and charge. The player can stand at the brake (completed segments hold; a charge through the brake interrupts the current segment) or step out of the lane, or strike the figures, which break and re-form while the storm lasts.
On the third segment, Kolla and then Arni reach the shelf below the Lip and go down the scree run to the Broken Engine (L4). Arni calls up (`TES-B4`). `TES_PAIR_ONE` set.
**Verbs:** sound, choose, drive, rig, hold, endure.

### Beat 5 — The Hollow (`S05_rig_two`) — *the strange moment*
**Objective:** *Climb down to the second overhang.* Then: *Find sound rock for two anchor irons.* Then: *Lower the last pair.*
The player and Dorn go down the scree run past the Broken Engine (optional inspect, TDS06) to the Hollow (L5). Storm window 3: gusts every ~18 s, Horn-Echo swells roughly every 30 s. **The player sounds alone.** Dorn holds the horn and the pair's attention; he will tell the player if a return is masked, never which seam is good.
- **Six seams; two solid.** New wrinkle: **a seam struck during a horn swell gives no reading** ("Couldn't hear it over the gorge."). The player must strike in the quiet between swells. The swell has a tell: the haze darkens and the fluted faces drop a note (~2 s) before the blast.
- Rigging and lowering exactly as at the Lip (2 + 3 segments, persistent; loose irons cost time, never a fall).
- **TES-E3:** the Horn-Echo at full strength: more lanes, a wider "echo-line" variant (three figures abreast that charge together), and re-form time shorter while the swells last.
- **The uphill figures (strange moment, §A8.3).** During the second lowering segment, a group of figures forms on the **camp shelf below** and runs **up the shelf toward the Horn Seat**, away from the far approach, past the player and not at them. They break on the wall below the Seat. Tamsin, on the line, says they are running the wrong way. Dorn does not answer. Nothing explains it. (`TES_UPHILL_SEEN`, presentation only.)
On the third segment Hjalti and Tamsin reach the camp shelf and take the gorge floor path out. `TES_PAIR_TWO` set. The player and Dorn go down after them to the camp shelf (walkable scree; no rope needed for the player).
**Verbs:** sound under pressure, rig, hold, witness.

### Beat 6 — The Seat Approach (`S06_seat_approach`)
**Objective:** *Reach the Horn Seat.*
On the seat approach (L7) the figures **stop running**. They form across the path between the player and the Seat and stand. This is **TES-E4**, the miniboss phenomenon (design name **the Held Line**; never shown in UI, never said in dialogue). The stand holds until the storm window turns. The player endures it and breaks it (§A7): the stand surges forward on each swell, the player shelters behind marked faces or takes the push, and breaking figures opens gaps that close again. **Every fully broken stand advances the storm one swell nearer turning.** Endurance alone always works: four swells and the window turns on its own (about 2.5–3 minutes). When the window turns, the whistle drops, the haze thins from the top down, and the figures fade where they stand. Dorn says only: "Window's turning." Then: "Go on. Before it thinks better of it."
**Verbs:** endure, position, break.

### Beat 7 — The Seat (`S07_seat`)
**Objective:** *Look at the Horn Seat.* Then: *Read what's under it.*
The lull (window 4): the wind drops to a steady hard blow; snow still falling; no Horn-Echo. Three required parts, any order:
1. **The rack and the sounding.** Inspect the plate rack (H2): *every plate aimed down the shelf*. Dorn will let the player sound **one plate**, gloved, with the iron's butt, once (`TES-D5`): "One plate. Not a call. Never a call." The player strikes it. The note is low and plain. Its **return comes back from below, from the camp shelf, in two beats** (positional audio from below; glyph: a near tick under the player). Dorn counts it aloud. He names what it did not do: "The far approach is eight, nine beats off. That came back in two." Then he takes his glove off the rack and does not touch it again. Sets `TES_SEAT_SOUNDED`.
2. **The strata.** Go down the short path to the strata cut (H4) and inspect the **buckles**, the **cookpots** and the **Thornfell horn** (`TES_STRATA_READ` on all three). Each inspect text says where the object lies: under the collapse, on the near side of it, among the debris the miners dug through. Gerrit, if asked later, admits they found pots and left them.
3. **The log tin.** Break the ice from the niche (H3) and take the tin: `TES_horn_roster` (quest item). The player reads it (document view; full text in the dialogue file). Dorn asks to see it. He reads the last lines and says nothing for a moment (`TES-D6`). He points at "No answer" and says he wants Maera to see it before anyone else does.
`S07` completes when all three are done (sounded, strata read, roster held). Dorn blows **Rest** up the gorge for Gerrit's men (all clear), and the player hears it answered faintly from the Cut.
**Verbs:** sound, read, dig through the record.

### Beat 8 — Out by the Ladders (`S08_climb_out`)
**Objective:** *Climb to the rim cairns.*
Storm window 5 (clearing). The miners' ladders (L8) up the wall to the rim: a climb in four pitches, each a short channelled climb (~3 s) between ledges; no gusts now, but snow slides off the rim in sheets (cosmetic; a dust of snow over the player). Dorn climbs below the player. At the top, the rim path (R4) to the cairn row.
**Verbs:** climb.

### Beat 9 — Two Honest Records (`S09_cairns`)
**Objective:** *Read the cairns.* Then: *Set the roster beside Maera's list.*
- **The cairns.** Inspect at least one cairn (R1; three are reachable): names, and under them **LOST IN THE GORGE STORM**. Required: one (`TES_CAIRNS_READ`).
- **Maera Cairnwatch** is at the reading stone (`TES-D7`). Dorn sent word up from the Cut before he came down; she has been waiting since the storm broke. She asks what was in the tin before she shows anything. When the player gives the roster's gist (or shows it), she takes from her coat her **private list** (inspectable document; text in the dialogue file), which says the rear guard "held the gorge" and gives the last sighting: on the lower shelf, holding, at the fifth hour, by those who came up the rim path.
- **Side by side.** The player uses **Set the records side by side** on the reading stone: the roster and Maera's list lie together, and the document view shows both texts in two columns. The disagreement is visible without commentary: the roster's Split is in the fourth hour, late; the list's last sighting is the fifth. Sets `TES_RECORDS_SET`. Maera's response (`TES-D7.20`) does not reconcile them: "Both honest. Both written by people who weren't down there."
- **No answer.** Dorn reads "No answer" aloud (`TES-D8`). He says the **Third Horn** was the reply that used to mean someone was still out (Answer, then a long rising), and that by the roster nobody blew it. He half-remembers it from his own training board; he does not know why it was dropped. Sets `TES_THIRD_HORN_HEARD` (read by *The Third Horn*). Dorn knows this **from the roster**, and says so: "It's what it says. I wasn't there."
- **The name-slip.** Maera mentions that a Hushfold household renews a temporary name-slip with her each spring for someone "who went over the pass", and that one name on it is also on her list (`TES-D7.40`). Optional inspect of the slip (`TES_NAMESLIP_SEEN`, read by *The Weight of a Name*). Maera: "Names repeat up here. Could be two people. Could be one." Register seed only.
**Verbs:** read, compare, listen.

### Beat 10 — What the Stone Says (`S10_choose`)
**Objective:** *Tell Maera what you think the stone should say.*
The player recommends; **Maera decides** (`TES-D9`). Her decision follows the player's recommendation in every case: she has asked because she wanted to hear it said by someone who climbed down. The three recommendations (§A9.3):
- **Amend the stone:** cut "beneath our own horn" under the names. Maera cuts the first word herself, there and then (a chisel on the facing stone; the player can hold the lamp).
- **Lay it beside:** lodge the roster in the cairn's niche and leave the stone as it is. The player places the tin in the niche (R3) and Maera stops it with the slate.
- **Keep it:** the roster goes to the **Passwatch warden post's keeping**, sealed under Maera's cord; the stone stays silent for now. A Ridge Warden runner from the Passwatch post carries the packet down to the post's strongbox (`TES-D9.32`). Dorn never handles it: "Post keeps it. Not me. Good." (`TES-D9.33`).
**Old Torvek** has walked up the rim path during the conversation and stands at the end of the row. He says one sentence, keyed to the outcome (`TES-D10`), and goes. The quest completes on `TES-D10` end.
**Verbs:** recommend, witness.

## A7. Encounters

Tuned for **Advanced identity (Milestone 3)** (TD-12). Echo-figures follow bible §2.6: **combat disperses, conditions decide.** No echo-figure has a nameplate, a name, a face, a clan mark or colours; target frames show no name (blank). The design names below are for this document and the Enemies package only.

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TES-E1** | 2 × rock viper, 1 × shale-coil | Shale before the Jam (L1–L2) | Vipers: ambush from shale patches beside the path. Shale-coil: holds the narrow, lunges | **Viper strike:** shale rattles around the patch (~1.0 s), then a fast strike. **Shale-coil lunge:** the coil draws back and the shale slides under it (~1.4 s), then a lunge along a straight line (step aside) | Low-tier warm-up; reading ground tells while managing gusts | 40–60 s; 70–85% HP remaining |
| **TES-E2** | Echo-figures, 2 lanes, 2 figures per lane per swell | The Lip (L3) during `S04_rig_one` | Each figure forms in a lane and **charges straight down it**, colliding with whatever is in the lane (blind; no tracking). Struck: breaks into haze. Re-forms in its lane after ~12 s while the storm window lasts | **Lane tell:** the haze thickens along the whole lane and snow lifts off the ledge in a line (~1.6 s); a low drag in the audio. **Charge:** knockback toward the wall plus moderate damage; never off the ledge | Teach the Horn-Echo: lanes are readable; stepping out works; striking works; neither ends it | Rig completes in 2–4 min including resets; player never below ~40% HP if using shelter |
| **TES-E3** | Echo-figures, 3 lanes; 1 × echo-line (three figures abreast) per swell; the uphill group (non-hostile presentation) | The Hollow (L5) during `S05_rig_two` | As E2; re-form ~9 s. **Echo-line:** forms across two lanes and charges as one; breaking the middle figure collapses the line | As E2. **Echo-line:** the haze darkens in a broad band and the fluted faces drop a note (~2.0 s) | Same mechanic under more pressure; striking between swells to sound | 3–5 min including resets |
| **TES-E4** | **The Held Line** (design name only): a stand of 7 figures across the seat approach, re-forming in place | Seat approach (L7) | The stand **holds** the path. On each horn swell it **surges** one step forward as a wall (pressure push). Between swells, individual figures step out and charge short lanes at the player. Broken figures leave gaps that close in ~6 s. **Breaking all seven before the gaps close disperses the stand**, which counts as one swell endured early; it re-forms on the next swell | **Surge:** the horn swell builds (~2.5 s; haze darkens, every figure leans), then the wall pushes ~4 m (heavy damage + knockback if caught in the open; none behind a marked shelter face). **Short charge:** as E2 lane tell (~1.6 s) | Miniboss phenomenon: endurance and positioning, with aggression rewarded. Ends when the window turns (4 swells), never by a kill | 2.5–3 min (window turns on its own); ~1.5–2 min with aggressive play |

**Rules**
- **Combat never reveals evidence.** The aim of the rack, the strata, the roster and the list are found by sounding, inspecting and reading. The figures prove nothing and identify no one. Nobody in dialogue says who they are, and the one wrong reading voiced aloud ("the dead are up", a miner's bark) is answered with Dorn's "Wind trick." and nothing else.
- **The uphill figures** are a presentation group, not combatants: they run their path and break on the wall. If the player stands in their path, they pass through the player as haze (no damage).
- **No fall deaths.** Gust and charge knockback push wallward. Rig failure is a time cost; NPCs never fall.
- **Death:** respawn at the Gust Stair head (before the Jam), at the Broken Engine (after the Lip), or at the camp shelf (after the Hollow). Completed rig segments and set irons persist. Rescued pairs stay rescued. In TES-E4, swells endured persist; the stand re-forms at the start position.
- **Storm windows** are per player (§A8.1). Leaving the gorge pauses the storm at its current window; returning resumes it.
- **Co-op:** shared figures; each partner's storm window follows their own step (fallback: host's window). Sounding results are per player (each hears their own strike). Rig and lowering segments are shared; all present are credited. In TES-E4, either partner's breaks count.

## A8. The discovery and strange moments: presentation specs

### A8.1 The storm windows

A quest-local, per-player weather state. Never world weather. Each window changes gust cycle, Horn-Echo activity and ambience.

| Window | When | Gust cycle (whistle tell ~2.5 s) | Horn-Echo | Look and sound |
|---|---|---|---|---|
| 1. **Building** | `S00`–`S03` | ~25 s | None | Hard wind, light snow; the fluted faces' whistle; Dorn's horn carries clean |
| 2. **Rising** | `S04` (or one gust cycle earlier if the Jam used the crew) | ~22 s | Swell every ~40 s; 2 lanes | Haze forms in the gorge below the player; snow driven sideways |
| 3. **Hard** | `S05` | ~18 s | Swell every ~30 s; 3 lanes + echo-line | Haze at shelf height; the gorge roars; the uphill group once |
| 4. **Peak, then turning** | `S06` | ~15 s | The stand (TES-E4); 4 swells | Visibility ~25 m; on turning, the whistle drops, haze thins from the top down |
| 5. **Lull, then clearing** | `S07`–`S10` | No gusts after `S07` | None | Steady wind, falling snow, then clear air and low sun on the rim |

### A8.2 The first horn blast (Beat 4)

| Time | Element | Spec |
|---|---|---|
| 0–2 s | **The draw** | All ambience ducks except the wind, which seems to pull up the gorge toward the player (a long inward rush). Dorn stops mid-word. |
| 2–5 s | **The blast** | A single horn note rolls up the gorge from below, very loud, very low, slightly wrong in pitch (it is not any Ordinary Call; **no call glyph appears**). It is not music. Rumble where supported. |
| 5–8 s | **The echoes** | The note comes back off both walls, and comes back again, more times than the gorge's width allows. The echo-return glyph does **not** show; this is not a sounding. |
| 6–10 s | **The haze** | Haze thickens in lanes along the shelf; within it, upright shapes form. Shapes of people running, without colour, without faces, without anything that could be read as a clan mark. |
| 10 s+ | **The charge** | The first figures charge (TES-E2). |
| Dialogue | Dorn | `TES-B4.1`: "Wind trick." (He does not smile.) |
| UI | | The current objective stays on screen. No popup, no name, no boss frame. |

### A8.3 The uphill figures (Beat 5) — *the strange moment*

| Time | Element | Spec |
|---|---|---|
| Trigger | Second lowering segment at the Hollow begins (once per player; if it already played, it does not repeat in later visits during the quest) | |
| 0–2 s | **Formation** | On the camp shelf below the player (visible from the Hollow), haze gathers into a group of five or six upright shapes. Ordinary lane tell. |
| 2–7 s | **The wrong way** | They do not charge along the shelf toward the far approach like the others. They turn and run **uphill**, up the seat approach, **toward the Horn Seat**, away from the far approach. Their audio is the same drag as other figures, but their footfalls (the only footfalls any figure makes) can be heard, uneven, climbing. |
| 7–9 s | **The wall** | They reach the wall below the Seat and break against it into haze that rises, not falls. |
| Dialogue | Tamsin on the line | `TES-B5.4`: "Those ones are running the wrong way." Dorn: no line. A stage beat: he looks up at the Seat, then back at the brake. |
| After | | Nothing explains it, then or later. The player makes any link from the roster. `TES_UPHILL_SEEN` set (barks only). |
| Accessibility | | Subtitle: "[Footsteps, climbing.]" |

### A8.4 The sounding at the Seat (Beat 7)

| Element | Spec |
|---|---|
| The strike | One interaction on one plate (the player chooses which; all give the same result). The note is plain and low; it is not loud. No haze, no figures, no blast: the storm window is in the lull. |
| The return | Positional audio returns **from below and slightly behind the player**, from the camp shelf, in two counted beats. With `TH_CALLS`, the echo-return glyph shows a near single tick with a small down-arrow. |
| Dorn's count | He counts "One. Two." aloud with the return, then names the far approach's distance as a number ("eight, nine beats off"). He does not say "they aimed it at their own". The player hears the aim. |
| The rack after | If the player tries to strike a second plate, Dorn's hand is on their wrist (`TES-B7.2`): "Once." The interaction is disabled for the rest of the quest. |
| Post-quest | The rack can be inspected on later visits; the sounding cannot be repeated (Dorn's rule becomes the player's: the interaction reads *"You said once."*). |

### A8.5 The two records (Beat 9)

| Element | Spec |
|---|---|
| Interaction | **Set the records side by side** on the reading stone. The roster and Maera's list appear as props on the stone and as a two-column document view: roster left, list right. |
| Highlight | No automatic highlight. The player reads. The two hours are in the same position on each page (the roster's last entries; the list's sighting line) so the eye finds them. |
| Audio | Wind on the rim; snow hiss; a far raven. Nothing else. |
| Afterward | Maera's line and Dorn's "No answer" scene. Nobody reconciles the hours. |

## A9. Quest structure for implementation

### A9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_cut` | Find Gerrit Carrick at Carrick's Cut. | Enter Cut volume + `TES-D1` end + chit-nail inspect | Yes | Quest Active from entering the Cut volume (with TF-M2 Completed) or from the journal lead. Storm window 1 starts |
| `S01_answer` | Listen for the salvage pairs. | `TES-D2` end + listen interaction at horn rail | Yes | Dorn's Lost; two Answers |
| `S02_descent` | Climb down to the first overhang. | TES-E1 defeated + enter Jam volume | Yes | Gust volumes; agility gap optional |
| `S03_jam` | Clear the jammed shelf. | 3 × `mine_jam` segments **or** crew event complete | Yes | Crew path advances storm to window 2 one gust cycle early |
| `S04_rig_one` | Find sound rock for two anchor irons. / Rig the line. / Lower the Vass pair. | 2 irons set + 2 × `rig_line` + 3 × `pay_out` segments | Yes | Loose-iron reset logic (§A6 Beat 4). TES-E2 active. Sets `TES_PAIR_ONE` |
| `S05_rig_two` | Climb down to the second overhang. / Find sound rock... / Lower the last pair. | Enter Hollow volume + 2 irons set + 2 × `rig_line` + 3 × `pay_out` | Yes | Masked strikes during swells. TES-E3. Uphill group on `pay_out` segment 2 start. Sets `TES_PAIR_TWO` |
| `S06_seat_approach` | Reach the Horn Seat. | Storm window turns (4 swells endured, stand-breaks counting as swells) | Yes | TES-E4. Persisted swell count |
| `S07_seat` | Look at the Horn Seat. / Read what's under it. | `TES_SEAT_SOUNDED` + `TES_STRATA_READ` + `TES_horn_roster` acquired | Yes | Any order. Window 5. `TES-D5`, `TES-D6` |
| `S08_climb_out` | Climb to the rim cairns. | 4 × `climb_ladder` + enter rim-cairn volume | Yes | |
| `S09_cairns` | Read the cairns. / Set the roster beside Maera's list. | 1 cairn inspect + `TES-D7` to `.20` + side-by-side interaction + `TES-D8` end | Yes | Name-slip optional |
| `S10_choose` | Tell Maera what you think the stone should say. | `TES-D9` choice + outcome interaction + `TES-D10` end | Yes | Sets `TH_SHATTERFALL_ACCOUNT`; roster leaves pack; quest → Completed |

### A9.2 Flags

| Flag | Set by | Read by (here) | Read by (later) |
|---|---|---|---|
| `TES_CHITS_READ` | Chit-nail inspect (required) | `TES-D1` options | TF-M4 `TSH-D1` optional line |
| `TES_JAM_MINED` / `TES_JAM_CREW` | `S03` path | Barks; storm timing | — |
| `TES_LOOSE_IRONS` (count) | Each loose iron loaded | Dorn barks (`TES-B4.6`, `TES-B5.6`) | — |
| `TES_PAIR_ONE`, `TES_PAIR_TWO` | Lowerings complete | Barks at the Broken Engine; post-quest Cut barks | — |
| `TES_UPHILL_SEEN` | Uphill group played | Post-quest barks | *The Third Horn* (one optional Dorn line) |
| `TES_SEAT_SOUNDED` | Seat sounding | `TES-D6`, `TES-D8` | — |
| `TES_STRATA_READ` | All three strata inspects | `TES-D7.30` option | — |
| `TES_CAIRNS_READ` | One cairn inspect | `TES-D7` | — |
| `TES_RECORDS_SET` | Side-by-side interaction | `TES-D9` | ***The Weight of a Name*** (second reading available) |
| `TES_THIRD_HORN_HEARD` | `TES-D8` | — | ***The Third Horn*** (richer variant; Dorn opens with the roster) |
| `TES_NAMESLIP_SEEN` | Name-slip inspect (optional) | — | ***The Weight of a Name*** (opening variant) |
| `TH_SHATTERFALL_ACCOUNT` | `S10` | `TES-D10` | *The Weight of a Name*; TF-M5 Maera placement; Assembly posture (§9.3: amended +1 open, kept +1 sealed) |

Quest item: `TES_horn_roster` (acquired `S07`; leaves the pack at `S10`; location by outcome).

### A9.3 Choice: what becomes of the rear guard's stone

The player **recommends**; Maera **decides**, and in every case she decides as recommended. The choice is the player's word, given to the person with authority over the dead.

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Amended** (`TH_SHATTERFALL_ACCOUNT = amended`): *"Cut it under the names: beneath our own horn."* | Maera cuts the words into the facing stone of the first cairn, under the names and under LOST IN THE GORGE STORM, which she leaves. The roster goes into her keeping with her list at the name-stone wall (TP15). | The stone now says what Thornfell never says. Blood-Oath households take it as an insult to the boast; some will not walk the rim (barks). Torvek: "Honest is heavy." Brynjar's lines in TF-M5 are colder toward the cairns. | **TF-M5:** Maera stands near the speaking stone; posture +1 toward open. ***The Weight of a Name***: Maera has both records at hand; the testimony scene is shortest. |
| **Beside** (`= beside`): *"Put the roster in the cairn. Leave the stone."* | The tin goes into the cairn's niche, stopped with the slate. Anyone who opens the niche can read it. The stone is unchanged. | The account is there for whoever looks, and nobody is told to look. Damp will reach the tin in time (Maera says so). Torvek: "Paper in a cairn. The wind reads it first." | **TF-M5:** neutral placement; no posture weight. ***The Weight of a Name***: the player opens the niche to read the roster again (a short walk). |
| **Kept** (`= kept`): *"Send it to Passwatch. Let the wardens keep it. Leave the stone."* | Maera seals the tin in oilcloth under her cord. A Ridge Warden runner carries it down to the Passwatch warden post's strongbox (the post keeps; Dorn never handles it). The stone stays silent for now. | The truth is held by the people whose horn it was, under seal; nobody is told. Maera: "For now." Torvek: "Silence is a stone too." | **TF-M5:** posture +1 toward sealed; Maera stands back. ***The Weight of a Name***: the player asks at the Passwatch post for the packet (the post's sergeant breaks Maera's cord in front of them). The roster can still be read. |

**All** outcomes: the roster survives and is readable at its location; the figures still run in storms; the player knows the aim, the strata and the roster. Nobody is told who blew the horn or how many died. Neither of those is in any record the player can reach. None of the options is wrong.

## A10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| Shatterfall storm event | World change | The Horn-Echo is revisitable in storms at the Lip, the Hollow and the seat approach (no stand; the stand is quest-only). |
| Carrick's Cut | Access | A camp with Gerrit's crew (vendor of rope and irons, economy pass); the ladders stay rigged as a gorge route. |
| A rigger's sounding iron | Tool (functional name; item pass to define) | Dorn gives the player one of his irons: "You know how to ask it now." Lets the player sound rock in *Seam Rights* and on high routes. No stats proposed. |
| Small payment | Currency | A Ridge Warden rescue due, paid at the Passwatch post (economy tuning). Gerrit has nothing to pay with and says so. |
| Skill XP | Action only | Melee; Mining (if used). |
| Side-quest unlocks | Story | *The Weight of a Name*; *The Salvage Ledge*; *The Third Horn* richer variant (`TES_THIRD_HORN_HEARD`); *Rope-Raising Day* when *A Place at Smoke Week* is complete. |
| TF-M4 | Story | Offered by Iven Ridgeborne on next entry to Stonewake or Passwatch. |

## A11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Iron in a loose slab | Shown on load; the iron is pulled and re-sounded. Time cost only. **No fall, no failure.** |
| Both irons loose | Dorn stops the rig before loading. Re-sound. |
| Strike during a swell (Hollow) | "Couldn't hear it over the gorge." No information; strike again in the quiet. |
| Caught by a gust or a charge | Wallward knockback and damage. Never off a ledge. |
| Death | Respawn points per §A7. Irons, rig segments, rescued pairs, swell count and the roster persist. |
| Player leaves the gorge mid-storm | Storm pauses at its current window (per-player). On return, resumes. The pairs stay on their stances ("We're not going anywhere." `TES-B4.8`). |
| Logout | Restore to the persisted step at the nearest respawn point; irons and segments kept. |
| Walking away | Stays Active. Resume hook: Gerrit at the rim winch (`TES-D1.90`) before `S07`; Dorn at the Passwatch horn post (`TES-D6.90`) after `S07` if the player leaves before the rim. Maera waits at the reading stone indefinitely. |
| Fail state | None. |
| Co-op | §A7. The choice is per player: each partner recommends to Maera in their own state. Prop fallback: the first choice in the shard sets the visible cairn state (cut words / slate in niche / unchanged); other partners' choices are stored and reflected in dialogue and later reads only. |

## A12. Integration needs

Documented dependencies for a later Systems Engineer. None is implemented here.

| Need | Owner | Minimum viable form |
|---|---|---|
| **Sounding interaction** with echo-return result | Systems + audio + UI | An interaction on tagged seam objects that plays one of two authored returns (quick-flat / slow-doubled) as positional audio, prints a log line, and (with `TH_CALLS`) shows an echo-return glyph (one tick / two spaced ticks). A "masked" variant when a storm swell is active. Seam solidity is authored data, not physics. |
| **Anchor-iron placement and load test** | Systems | Two carry-state irons placed on seams; on the first loaded `pay_out` segment, a loose seam triggers a scripted shift (prop animation), interrupts the segment, and offers *Pull the iron*. |
| **Channelled segments with persistence** | Systems | Reused from Lowmark crank (Act I §C12): `rig_line` ×2, `pay_out` ×3 per rig, `mine_jam` ×3, `climb_ladder` ×4. |
| **Quest-local storm state** | Systems + VFX + audio | Per-player window index (1–5) driving gust cycle, haze density, snow, ambience and Horn-Echo spawning. Pause when the player leaves the gorge volume. Fallback: three windows (building / hard / clear) if five is too many. |
| **Gust volumes** with whistle tell | Systems + audio | Reused bible convention (TF-M1): a tell sound ~2.5 s, then a wallward push volume; shelter-face volumes negate. |
| **Lane spawner** for echo-figures | Gameplay | Authored lanes; figures spawn on a swell, charge along the lane (no tracking), break on hit, re-form on a timer while the window allows. No nameplate, blank target frame. |
| **The stand (TES-E4)** | Gameplay | A formation of seven figures with a surge on each swell and break-gap timers; a "swells endured" counter persisted; the window turns at 4. |
| **Uphill presentation group** | Gameplay + animation | A non-hostile scripted group on a path toward the Seat; passes through the player as haze; footfall audio. |
| **Side-by-side document view** | UI | Two documents in two columns. Fallback: open them in sequence with a "set beside" log line. |
| **Cairn state props** by outcome | Art + Systems | Facing stone with/without the added line; niche open/stopped; per-player with first-choice fallback. |
| Creatures | Schema / Gameplay | Rock viper, shale-coil; echo-figure, echo-line; the stand (design name "the Held Line", never displayed). |
| Quest item `TES_horn_roster` | Schema | Non-droppable document with inspect text; removed at `S10`; location-bound readable copy (inspect) at Maera's wall, the cairn niche, or the Passwatch strongbox. |
| **Act I read-conditions** | Act I author / Schema | `TIW_store_ledger` possession check; `TH_STORES`; `TH_PASSWATCH_ROUTE`. |

## A13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **What the horn that split the ridge did** (R06 horn half) | The Split was sounded from the Horn Seat while the rear guard was still on the lower shelf; the shelf fell on them. | Brynjar's boast: it saved Thornfell; or it is an exaggeration. | The rack aimed down the shelf; the sounding returning from the camp shelf; strata with Thornfell kit on the near side; the roster's "Rear guard not recalled. No answer." | The figures are enemy ghosts; the horn is a myth; the cairn is a lie. | Who blew it; how many died (TD-9). | **TF-M3 (owned).** |
| **Two hours that disagree** | Both records are honest and partial: the roster gives the station's hour of the Split; Maera's list gives a sighting reported by survivors who came up the rim path. | Nothing; nobody has set them together before. | Side-by-side view. | One record is false; the rear guard survived the Split; the sighting proves a ghost. | Which hour is right. Never resolved. | None (left open). |
| **Why some figures run uphill** | A resonance imprint of the moment of the Split, carrying movement toward the Seat. Seed, not testimony. | "Wind trick." | The uphill group; Tamsin's line; Dorn's silence. | They are chasing the hornbearer; the dead are accusing someone. | Any explanation. | Never explained. |
| **The Third Horn's lost meaning** | "Heard; someone is still out." Dropped after the war. | A reply nobody blows. | Dorn's line reading "No answer". | It was a war signal; it was the Split. | Why it was dropped. | *The Third Horn*; R06 sealing half (TF-M5). |
| **The Hushfold name** | One rear-guard name is also on a Hushfold slip as "went over the pass". | Hushfold says its people came over the pass. | Maera's line; the slip. | Hushfold are deserters' families. | Whether it is one person or two. | *The Weight of a Name*; R14 seed. |
| **The empty rack slots** | Eyvind took three plates from the rack himself for the Wall-Horn. | — | Fresh pry marks; Gerrit: "Stall went up himself. Once." | Brigands took them. | — | TF-M4 (the frame's plates). |

## A14. Open decisions

1. **TD-9** is kept: no record reachable in TF-M3 names the hornbearer (the roster's duty margin has rotted) or gives a count (Maera's list is shown one leaf; the cairn row runs past the path; no line totals anyone). If the Director ever releases either, only the roster's margin and Maera's list change.
2. **Carrier of the roster in "kept" (resolved, independent review).** A Ridge Warden runner from the Passwatch post carries it (`TES-D9.32`); Dorn never handles it, so the Part 4 ledger's "no named roster" limit for Ressa and Dorn holds without interpretation.
3. **The Hushfold name-slip name (resolved, independent review):** **Sig Brede**, matching *The Weight of a Name* (Asa Brede's slip, renewed each spring). The earlier draft name was dropped because it collided with TF-M5's straggler Halvard.
4. **Storm window count** (5) may be cut to 3 for scope (§A12 fallback) without changing beats.
5. **Rewards:** "a rigger's sounding iron" needs the item pass. If it is cut, Dorn's line stays and the sounding becomes knowledge only.
6. **Map:** the relative geometry in §A5 needs the zone package (MAP VERIFICATION REQUIRED).

## A15. Internal review log

| Finding | Revision |
|---|---|
| The rope rescue first risked a failure state (a pair falls if both irons are loose). | Removed. Loaded loose irons stop the segment; both loose prevents loading. Nobody falls; the cost is storm time. |
| The echo count risked duplicating TF-M1's face-distance reading. | TF-M1 counts distance to a face; TF-M3 strikes the face and reads its **quality** (single quick vs. slow doubled). TF-M4 does not strike at all. |
| The stand risked being named in UI or speech. | Blank target frame; no boss bar; Dorn's lines are "Window's turning." and "Go on." Design name confined to §A6 Beat 6 parentheses, §A7 and §A12. |
| A miner's line called the figures "the dead". | Kept as a belief bark (allowed wrong reading), answered with "Wind trick." No line confirms it. |
| Dorn's knowledge of Shatterfall. | He says twice that he was never down there and that what he knows is "what it says". The aim reading is his skill (counting), not memory. |
| Maera's list risked giving a casualty count. | The player sees one leaf with a few names; the list "continues"; the rim row continues past the path. No total appears anywhere. |
| The clan-stamped buckles risked assigning a family casualty to an anchor's clan. | Stamps are "several clans' marks", none named. Brynjar's clan is not identified. |
| The choice risked Maera taking orders from the player. | The player recommends; she says she wanted to hear it from someone who climbed down, and decides. Authority over the dead stays hers. |
| "Kept" risked giving Ressa or Dorn named roster custody (Part 4 ledger). | The **post's strongbox** keeps it under Maera's cord; a Ridge Warden runner carries it (independent review). Dorn never handles it. |
| Combat as evidence. | The figures prove nothing; the rack, strata, roster and list are inspected. |
| Agility triggers. | Shelf gap (plank detour), seat-approach scramble (ramp). Ladders are channelled climbs, click-to-move friendly. |
| Quest item budget. | `TES_horn_roster` is Thornfell item 2 of 4. Maera's list, the slip and the chits stay with their keepers. |
| **Independent review (2026-11-03)**, TF-M3: 3 findings (1 high, 1 medium, 1 low). | "Kept": Dorn no longer carries the roster; a Ridge Warden runner does (`TES-D9.32`–`.33`), closing the Part 4 ledger risk. Name-slip renamed Sig Brede to match *The Weight of a Name* and remove the Hallvard/Halvard (TF-M5) collision; slip is renewed each spring, as TWN says. |

---
---

# Part B — TF-M4 The Summit Hall (`TSH`)

## B1. The quest in one paragraph

**Iven Ridgeborne** finds the player with a list: nights the Summit hummed "with no storm in it", written up in his Ridge Warden log by date, hour and wind. Eyvind Stall's tuning sketches from the Whinstone Store named the Summit's great hall. **Kaldren Deepdelver** meets them at the foot of the carved stairs, because "somebody has to stop you all from being clever". The ascent climbs cliff-hugging stairs and an inner stair where air-channels breathe out torches on a rhythm, and on one landing the player hears their own footstep from the next landing up before they take it. Iven says, "That one. Every time." At the top, the **whisper hall** runs behind the great hall's wall: a whisper at one mouth is heard at the others. From three listening mouths the player hears the crew's tools and voices along Iven's carry lines, whispers down each line to see which come back, and marks on Iven's sketch where each crewman is and which alcoves have gone silent. Kaldren shows them how to confirm a **null-point**: dust falls straight, your own voice goes flat. The map decides the way in. In the **great hall**, Eyvind and his crew have mounted the **Wall-Horn**, a frame of Echohewn plates, and are sounding test notes. With each note the hall answers: the air hums, dust spills off the floor into rough upright shapes that never hold, and a pressure pulse rolls out from the centre stone on a rhythm the player can count. The player fights the crew between pulses until they yield, and takes the horn out of Eyvind's hands. The plates keep ringing on their own. The player listens along the frame for the plate that is **carrying the others**, has Kaldren read the stress in its bolts, unbolts it and carries it into a silent alcove between pulses, and again, until the last plate goes quiet. The hum stops. For one breath the whole Summit is silent, and the dust that was spilling toward the player falls straight down. Eyvind's **horn-trial record** dates every test; Iven's list dates every hum; the player sets them together, and they match. Kaldren says, "Stresses settled. That's all I can tell you." Eyvind, yielded, names the person he answers to: **Ingrith Scarrow**, the Quartermaster, who "will close the wall herself if she can't sound it". The player decides what happens to the horn.

**What the player should remember:** the silence. **What the player should want next:** to reach Ingrith before she closes the wall.

## B2. Selection record

| Candidate | Verdict |
|---|---|
| **A. Fight the "guardian".** | Rejected. C11: the node is never a creature, never fought. The pulses are a hazard. |
| **B. Kaldren explains the node.** | Rejected. Character ledger: Kaldren explains no origins and cannot validate a Summit account. His only Summit line on the matter is about stresses. |
| **C. A stealth infiltration of the great hall.** | Rejected. No stealth system. The triangulation decides the **start state** of an ordinary fight instead. |
| **D. Silence the horn by striking each plate and counting returns.** | Rejected. That is TF-M3's mechanic. Here nothing is struck: the player listens to a sound already in the air and finds its loudest pitch. |
| **E. Offer → ascent with wonder → listen at three mouths and mark a sketch → confirm a null-point → fight under pulses → stop Eyvind → damp plates by ear between pulses → silence → two records → a name → the horn's fate** (selected; the bible brief). | **Selected.** The quest gets quieter as it goes: wind on the stairs, voices in the walls, a hum in the hall, then nothing. |

## B3. Canon grounding

| Element | Source | Status |
|---|---|---|
| Echochamber Summit: carved stairs on cliff faces; resonant halls where whispers carry impossible distances; air-channels that shape airflow; chambers that hum in storms | Dossier §V.6 | [CANON] |
| The Summit's Stonebound node: hums, dust spiralling into rough shapes, pressure pulses; passive, place-bound; no speech, no intent | Dossier §IX.2; Stage A C11; Part 4 ledger contradiction 4 | [CANON] |
| Null-points: Echohewn sound-dampening pockets | Dossier; bible §2.1; TDS01 | [CANON] |
| Kaldren: stresses and alignments, not origins; "They're asleep. And waking them all at once would tear the mountain apart."; limits reactivation | Thornfell anchors §III | [CANON] |
| Iven: echoes that arrive before sound; stone faces humming; does not think it magic; leads the player step by step | Thornfell anchors §VI | [CANON] |
| Horn plates salvaged and bolted into horns to force resonance | Bible §2.1; H11 | [CANON] |
| Eyvind Stall, the Wall-Horn, the trial record, Ingrith Scarrow as Quartermaster | Bible §2.3, §5.2 (TD-1) | [NEW] / [PROPOSAL — DIRECTOR] `[SPLINTER]` |
| The whisper hall's three listening mouths, the six alcoves, the counting room, the frost-count calendar | This package | [NEW] |
| Iron Winter crews (spear, hornman); ridge crows | Bible §10 | [NEW] on [CANON] ecology |

## B4. Quest summary card

| Field | Value |
|---|---|
| Working title | **The Summit Hall** |
| Suggested content id | `thornfell.main.04_summit_hall` |
| Arc position | Act II turn (Arcs §3.1: "Show ancient power as passive and dangerous, and Thornfell's own misuse as the trigger") |
| Prerequisite | TF-M3 Completed |
| Offer | Iven Ridgeborne (`TSH-D1`), on the player's next entry to Stonewake's Signal Terrace or the Passwatch horn post after TF-M3 |
| Target length | 50–65 minutes |
| Combat share | ~25% (crows, lookouts, the great-hall crew under pulses) |
| Dialogue share | ~10% |
| Traversal, listening, mapping, damping, reading, choice | ~65% |
| Skills | Melee (required); Ranged optional (crows) |
| Choices | What happens to the horn: silenced / broken / surrendered (3 options) |
| Unlocks | `TH_HORN`; the Summit node quiet (no hum without a storm); Thornfell **high routes**; *The Notes We Keep* (with *Witness at the Gate*); TF-M5 |
| **Anchor** | Echohewn keepers (Kaldren); Ridge Warden high-path scouts (Iven); Echochamber Summit |
| **World-truth row** | C.5 / C11 (Stonebound node passive; Thornfell powers); H11 (plates forced into horns); H25 (the splinter's unsanctioned readiness) |
| **Revelation role** | **Owns R07:** the Summit "guardian" is a passive response and the splinter's horn woke it. Plants TF-M5 (Ingrith named). Supports R06 (the Seat's plates are in the Wall-Horn). |
| **Recurring evidence** | The Wall-Horn's plates recur from TF-M2 (crates) and TF-M3 (the Seat's empty slots) with independent custodians (the store ledger; the rack). The plates recur in *The Notes We Keep* (custodian by `TH_HORN`: Kaldren, the hall floor, or Ressa under seal). Ingrith's name recurs in TF-M5 (independent custodian: TF-M5's own encounter and the Assembly). The trial record recurs at TF-M5 as a held item. |
| **State compliance** | Inactive / Active / Completed only. Choice recorded in `TH_HORN`. No fail path: wrong marks only harden the fight; a wrong plate only brings a pulse early; a dropped plate is picked up; the hum always stops when the last plate is damped. |

## B5. The places

**MAP VERIFICATION REQUIRED** throughout. The narrative needs only that the stairs climb from a foot reachable from Stonewake's high road to the Summit, that the whisper hall runs beside the great hall with three mouths, that the great hall is a round hall with six alcoves and a dais, and that the Crown (the summit top) is above it with views of the ridgelines. No compass direction toward Emberholt is asserted.

### B5.1 The Stair Foot

| Area | Storytelling |
|---|---|
| **F1. The lowest step** | The first carved step, wider than a cart, worn into a dish. A Ridge Warden way-cairn. Kaldren is sitting on the step with his boots off, rubbing his feet, when the player arrives (`TSH-D2`). |
| **F2. The sled marks** | Fresh runner marks and crate-scrapes going up the steps' edge, where something heavy was hauled on a sledge. Optional inspect. |

### B5.2 The Carved Stairs [TDS02]

| Area | Storytelling |
|---|---|
| **S1. The outer stair** | Steps hugging the cliff face, snow on the treads, a long drop to one side with a carved lip that is always high enough. **Ridge crows** (TSH-E1) nest in the face at the Narrow Turn. Agility trigger: a short cut up a broken flight (scramble). Fallback: the full switchback. |
| **S2. The inner stair** | The stair turns into the rock. Wall sconces hold Ridge Warden torches; **air-channel mouths** in the wall breathe on a rhythm. Before each draw the torch flames lean toward the channel (~1.5 s); then the draw pulls (~2 s), putting out a carried lantern and pushing the player back a step on the narrow treads. Pass between draws. |
| **S3. The Echo Landing** | A landing where the player hears their own footstep from the next landing up before they take it (bible TME09 language, here in-quest). Never explained. Optional "wait and listen" interaction repeats it once. |
| **S4. The Upper Landing** | The last landing below the halls: a crew's sledge, empty crates with Shatterfall grit, a cookfire, two lookouts (TSH-E2). The landing hears the halls; the halls do not hear the landing (Iven). |

### B5.3 The Whisper Hall

| Area | Storytelling |
|---|---|
| **W1. The Low Mouth** | The first of three listening mouths: a carved opening in the gallery wall like a deep, smooth funnel. Three **carry lines** run from it across the great hall on Iven's sketch: left, ahead, right. |
| **W2. The Long Mouth** | The second mouth, midway along the gallery. Three carry lines. |
| **W3. The Crown Mouth** | The third, at the gallery's high end under a stair to the Crown. Three carry lines. |
| **W4. The Counting Room** | A small square room off the gallery, sound-dead: a **null-point**. Tally grooves cut in a bench (Echohewn counting; nobody can read them). Kaldren's lesson (`S06_null`). |
| **W5. The Quiet Passage** | A narrow passage from the Counting Room's back wall that runs through dead rock and opens into great-hall alcove **V** (a null alcove). The way in when the map is good. |
| **W6. The open stair** | The ordinary way into the great hall: a short stair to its door. The way in otherwise. |

### B5.4 The Great Hall

| Area | Storytelling |
|---|---|
| **G1. The dais and the frame** | A raised dais facing the hall's great mouth. On it, the **Wall-Horn**: an iron bell-frame with **five Echohewn plates** bolted in a curve, and a mouthpiece horn of goat horn and brass that drives them. Three of the plates have grey Shatterfall grit in the grooves and are the size of the Horn Seat's empty slots (TF-M3). |
| **G2. The six alcoves** | Alcoves around the hall wall, numbered on Iven's sketch **I–VI** clockwise from the door. **II and V are null-points.** In play: crew at I, III and VI (VI holds two with `TH_STORES = leverage`); IV is empty with a dripping bucket. |
| **G3. The centre stone** | A worn round stone in the floor before the dais, polished by nothing anyone remembers. Pulses roll out from here. Dust gathers around it between pulses. |
| **G4. The pillars** | Four pillars between the centre and the alcoves. Each casts a **pressure shadow**: a pulse does not strike behind it. Snow has blown in and lies in the shadows in neat wedges (a readable tell: where snow lies, pulses do not reach). |
| **G5. Eyvind's bench** | A tuning bench by the dais: files, wedges, a felt-wrapped mallet, a pot of grease, and a bound book: the **horn-trial record** (`TSH_trial_record`). |
| **G6. The great mouth** | A wide opening in the hall's far wall onto the sky. Kaldren will not let anyone sound into it, whistle into it, or stand in it with the horn. |

### B5.5 The Crown

| Area | Storytelling |
|---|---|
| **K1. The summit top** | A small flat top above the halls, reached by the stair from the Crown Mouth. Wind, cold, and every ridge of Thornfell. Iven's coda and the high-route marks (`S12_crown`). |

## B6. Player-facing sequence

### Beat 0 — Nights With No Storm (`S00_offer`)
**Objective:** *Talk to Iven Ridgeborne.*
After TF-M3, on the player's next visit to the Signal Terrace at Stonewake or the Passwatch horn post, **Iven** is waiting (`TSH-D1`). He has come down off the high path to show someone his list (inspectable document; text in the dialogue file): nights the Summit hummed "with no storm in it", each with date, hour and wind, written into his Ridge Warden log. He reports before he interprets, and he interprets very little: "Mountains get tired. Not like this." Variant with Eyvind's sketches seen in TF-M2: the player can say the sketches named the great hall. Iven will take the player up. Kaldren will meet them at the stair foot; Iven sent word.
**Verbs:** talk, read.

### Beat 1 — The Stair Foot (`S01_stair_foot`)
**Objective:** *Meet Kaldren at the foot of the Summit stairs.*
Kaldren is on the lowest step with his boots off (`TSH-D2`). He has come because "somebody has to stop you all from being clever". He sets one rule before anyone climbs: on the Summit nobody hits anything to hear what it says. "You've been down Shatterfall. Up here you listen. You don't knock." Optional: the sled marks (F2).
**Verbs:** talk.

### Beat 2 — The Stairs (`S02_ascent`) — *a wonder*
**Objective:** *Climb the Summit stairs.*
- **Outer stair** (S1): snow on the treads. At the Narrow Turn, a **ridge crow** flock mobs the stair (**TSH-E1**). Mid-fight, a faint test note comes down from above (Eyvind is playing) and every crow on the face lifts at once and wheels away (callback to TF-M2's trial frame). The fight ends there or with the last diver. Agility trigger: the broken flight; fallback: the full switchback.
- **Inner stair** (S2): the **air-channel draws**. The torches lean; the player waits in a sconce niche, then climbs past the channel mouth between draws. Caught in a draw: pushed back one step, carried lantern out. Iven relights it ("Again."). No damage; no fall. Four channel mouths. Optional inspect: a channel mouth (*"The draw pulls at your sleeve, then lets go. Something below is breathing in and out through the rock. It's only air."*).
- **The Echo Landing** (S3): stepping onto the landing, the player hears a footstep from the next landing up, one beat before their own next step lands there. Iven, behind: "That one. Every time." Nobody explains it.
**Verbs:** climb, time, fight, listen.

### Beat 3 — The Upper Landing (`S03_landing`)
**Objective:** *Deal with the lookouts.*
Two Iron Winter lookouts at the Upper Landing (**TSH-E2**): a spear and a hornman. The hornman's call buffs the spear unless interrupted. They yield. Iven ties them to the sledge (prop). Optional inspect: the empty crates (Shatterfall grit), the cookfire (*"Warm. A pot of something with too much salt. They've been up here days."*).
**Verbs:** fight.

### Beat 4 — Three Mouths (`S04_listen`)
**Objective:** *Listen at the three mouths.*
Iven explains the whisper hall in three lines (`TSH-D3`): a whisper at one mouth is heard at the others; each mouth hears along its carry lines; he has drawn the lines on his sketch from years of whispering into them. The sketch (UI document) shows the great hall's ring of alcoves I–VI, the dais, and nine carry lines (three per mouth).
At each mouth (W1–W3), two interactions:
- **Listen** (passive, ~6 s): the player hears what is coming along each of the mouth's three lines. Positional audio pans left / centre / right; subtitles name the direction and the sound ("Left: a file on metal, slow."). Iven writes what was heard in the sketch's margin (an automatic log, accessible and click-to-move friendly).
- **Whisper down a line** (active, ~3 s per line, three lines): the player whispers; the whisper comes back off the far wall, or it does not ("Your whisper goes out along the line and doesn't come back."). Iven notes "back" or "gone" on that line.
Kaldren permits whispering ("A whisper's not a knock.").
The full solution table is §B8.1. A player who has listened and whispered at all three mouths has everything they need.
**Verbs:** listen, whisper, record.

### Beat 5 — The Sketch (`S05_mark`)
**Objective:** *Mark the crew and the silent alcoves on Iven's sketch.*
The sketch UI: each alcove I–VI can be marked **Crew**, **Silent** or **Empty**, or left blank. Iven reads the margin notes back if asked (`TSH-D4`) but does not solve it. He gives one method line: "Something heard on two lines is where the lines cross." Kaldren gives one: "Something that eats a whisper on both its lines is a quiet room." The player can change marks until the way in is chosen in `S07`.
**Verbs:** deduce, mark.

### Beat 6 — The Counting Room (`S06_null`)
**Objective:** *Find out how Kaldren tells a quiet room.*
Kaldren takes the player into the Counting Room (W4) (`TSH-D5`). The player's footsteps vanish at the threshold. He drops a pinch of grit from his glove: it falls straight down, no drift, onto the floor in a small heap. He says a word: it comes out flat, as if spoken into wool. The player repeats both (**Drop grit**, **Speak**; two interactions). Sets `TSH_NULL_TAUGHT`. Kaldren: "That's a quiet room. Builders worked loud and counted quiet." (Function, not origin.) He points out the Quiet Passage (W5) at the back and says where it comes out: "Into one of theirs. If that one's quiet too, nobody hears you come." The player may now revise the sketch.
**Verbs:** test, learn.

### Beat 7 — The Great Hall (`S07_great_hall`)
**Objective:** *Stop the test.*
The player commits the sketch by telling Iven to go in (`TSH-D4.50`). The marks set the **way in and the start state** (§B8.2):
- **Good map** (5–6 of 6 correct): Iven takes the **Quiet Passage**; the player enters at alcove V (a null-point, confirmed) unheard. The crew are in their alcoves, facing the dais. First strike on alcove VI; I and III join late.
- **Fair map** (3–4 correct): the **open stair**. The crew hear the stair and turn, but stay in their alcoves at first; the fight arrives in two waves.
- **Poor map** (0–2 correct): the open stair, and the crew have heard the whispering in the walls. They are gathered before the dais and the hornman has his call off as the player enters (all crew buffed for the first ~20 s).
All three are solo-clearable. None fails.
Inside: **Eyvind Stall** `[SPLINTER]` is on the dais with the mouthpiece. He counts four on his heel and blows a test note into the frame. **The hall answers** (§B8.3): the hum climbs a step, dust spills off the floor around the centre stone into rough upright shapes that lean outward and never hold, and a **pressure pulse** rolls out from the centre stone to the walls. Then quiet, and he counts again. The player fights the crew (**TSH-E3**) between pulses, using alcoves and pillar shadows. The pulses stagger the crew too.
The crew yield. Iven ties them; Kaldren stands in a pillar's shadow with his hand on the stone and does not fight.
**Verbs:** enter, fight, read the rhythm.

### Beat 8 — The Hornwright (`S08_stop_eyvind`)
**Objective:** *Take the horn from Eyvind.*
Eyvind keeps playing. He is not a fighter and does not fight; he does not stop either (`TSH-D6`). The player walks onto the dais and uses **Take the horn** (channelled ~2 s, interrupted by a pulse; start it right after a pulse). He lets go at once, more upset about the mouthpiece than about himself. He yields and sits on the dais step.
**The plates keep ringing.** The hum does not stop. The pulses slow (~18 s) but keep coming. Kaldren: "He's stopped. It hasn't." (`TSH-D7`.)
**Verbs:** stop a person.

### Beat 9 — Carrying the Others (`S09_silence`)
**Objective:** *Find the plate carrying the others.* Then: *Carry it to a quiet alcove.* (Repeat until the frame is silent.)
**The signature mechanic.** Five plates hang in the frame, each ringing its own pitch inside the hum. One is **carrying the others**: the loudest under the hum, the one whose ring the rest are riding on.
- **Listen** at a plate (~1.5 s, ear close; masked if a pulse tell is building): the player hears either *"Under the hum, this one is loudest. The others are riding on it."* (the carrier) or *"Thin. It's singing along with something else."* With `TH_CALLS`, a hum glyph shows a thick or thin bar.
- **Ask Kaldren** about a plate the player has listened to: he puts his hand on the frame by its bolts and reads the stress (`TSH-D8`): "That bolt's taking the load. That's your carrier." or "Bolt's slack. Not that one." He confirms only plates the player has listened to, and he will not strike anything.
- **Unbolt** the plate (2 segments of ~3 s; persistent; a pulse interrupts the segment, not the progress).
- **Carry** it (heavy carry state: walk only) to a **silent alcove** (II or V). If the sketch marked them correctly they are highlighted; if not, Kaldren tests both with grit as the phase begins and calls them out ("Two. That one and that one."). Guaranteed path.
- **Set it down** in the alcove: the plate goes dead quiet; its pitch drops out of the hum; the dust over the alcove floor falls straight.
- **Pulses** keep coming from the centre stone while the player works. Hit while carrying: the player drops the plate, which rings when it hits the floor (hum bump; the next pulse comes a few seconds sooner); pick it up again.
- **Wrong plate:** unbolting a plate that is not carrying makes the others flare: the hum jumps and the **next pulse comes ~6 s early**. The plate still has to be carried and still counts as damped. Harder, never a failure.
- **Right plate:** the hum drops a step and the pulse rhythm slows (~18 → 22 → 26 → 30 s) and weakens.
Answer key (design): P3 (centre), then P2, then P4, then P5, then P1 (the last is trivially the carrier). Plates are labelled only in this document.
**Verbs:** listen, confirm, unbolt, carry, time.

### Beat 10 — The Silence (`S09_silence` completion) — *the strange moment*
When the last plate is set down in the alcove (§B8.4): the hum stops. For **one breath** the whole Summit is silent: no wind in the great mouth, no breath, no footsteps, no UI sounds. The last dust that was spilling from the centre stone toward the player **falls straight down**. Then sound comes back in ordinary order: the wind at the great mouth, Iven's breath, Eyvind saying "Oh," very quietly.
**Verbs:** witness.

### Beat 11 — Two Records and a Name (`S10_records`)
**Objective:** *Take Eyvind's trial record.* Then: *Set it beside Iven's list.* Then: *Talk to Eyvind.*
- **The trial record** (G5): pickup, `TSH_trial_record` (quest item; text in the dialogue file). It dates every test, with plates seated, how long the note was held and what the hall did.
- **Set them together:** Iven takes out his list and the player uses **Set the records side by side** (the TF-M3 interaction and two-column view). The dates match: every hum Iven logged on a night with no storm is a trial night; the one trial with no hum logged is a night Iven was on the Passwatch rota and says so in his own log; the one trial on a storm night is listed by Iven with the storms, where he cannot separate it. Sets `TSH_RECORDS_SET`. Iven: "Every one." (`TSH-D9`.)
- **Kaldren**, asked what it was, or whether it is over: "Stresses settled. That's all I can tell you." (`TSH-D9.30`.) He says nothing else about it.
- **Eyvind** `[SPLINTER]`, yielded, talks (`TSH-D10`). He thought the hum meant the horn was "right". He tells the player he answers to **Ingrith Scarrow**, the Quartermaster, and that she "will close the wall herself if she can't sound it". Sets `TSH_NAMED_QM`. This is testimony after the fight, not a drop.
**Verbs:** take, compare, listen.

### Beat 12 — The Horn (`S11_choose`)
**Objective:** *Decide what happens to the horn.*
Physical choice at the alcoves and the dais (§B9.3, `TSH-D11`):
- **Silenced:** leave the plates damped in the silent alcoves. Kaldren sets his mark (a chalk sign of his own) on each alcove lip and says he will keep them.
- **Broken:** crack the plates on the hall floor. Kaldren insists it is done inside the silent alcoves ("In the quiet, if you're going to."). The player uses the crew's maul (prop) on each plate in the alcove: a crack with no sound at all (3 interactions per alcove).
- **Surrendered:** wrap the plates in the crew's sacking (2 interactions) for the Ridge Wardens to carry down to Ressa for the Assembly. Iven goes up to the Crown to call the wardens.
**Verbs:** decide, do.

### Beat 13 — The Crown (`S12_crown`)
**Objective:** *Climb to the Crown with Iven.*
The stair from the Crown Mouth to the summit top (K1). Iven blows **Gather** for the wardens (they will come up for Eyvind, the crew, and in the surrendered outcome the plates). He shows the player the ridgelines and marks three **high routes** on his sketch (§B10), then says what he thinks of weather and a person who wants to close a wall (`TSH-D12`). The quest completes on `TSH-D12` end.
**Verbs:** climb, look.

## B7. Encounters

Tuned for **Advanced identity (Milestone 3)** (TD-12).

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TSH-E1** | Ridge crow flock (6) + 2 × diver | Outer stair, the Narrow Turn (S1) | Flock: mobs and harasses (light pecks, small accuracy debuff). Divers: target the player from above | **Diver:** climbs, folds wings with a sharp caw (~1.2 s), then dives in a straight line (step aside). Flock: circles tighten before a mob (~1.0 s) | Low-tier opener on a narrow stair; Ranged is useful | 40–60 s; ends early when the distant test note lifts the flock (scripted ~45 s in) |
| **TSH-E2** | 1 × Iron Winter spear, 1 × hornman | Upper Landing (S4) | Spear: holds the landing. Hornman: hangs back and signals | **Spear thrust:** plants the back foot and draws the spear back (~1.0 s), then a long thrust. **Hornman call:** raises the horn (~2.0 s, interruptible), then a call that buffs allies' damage for ~15 s | Teach the hornman's interrupt before the hall | 45–70 s; 65–80% HP remaining |
| **TSH-E3** | 2 × spear (I, VI), 1 × hornman (III); **+1 × spear (VI) with `TH_STORES = leverage`**; plus the **node pulse hazard** | Great hall | Start state by map tier (§B8.2). Crew fight from and toward the alcoves; they shelter from pulses too | As E2. **Pulse hazard** (not an enemy): Eyvind's four heel-taps (audible) → test note (~3 s) → hum climbs and dust lifts and leans outward from the centre stone (~2.0 s) → ring expands to the walls (~1 s). Heavy damage + stagger in the open; none behind a pillar (snow-wedge tell) or in a silent alcove; half in an ordinary alcove. Period ~14 s while Eyvind plays | Combat inside a readable hazard rhythm; crew and player both obey it | Good map: 90–120 s. Fair: 2–2.5 min. Poor: 2.5–3.5 min |
| **TSH-H1** (hazard) | Node pulses during `S08`–`S09` | Great hall | No combatants. Pulses continue from the ringing plates | As E3, but the tell begins without Eyvind's taps: the hum climbs a step first (~1 s), then the dust lean (~2.0 s). Period ~18 s, then +4 s per correct plate; −6 s once per wrong plate; weaker as plates are damped | Labour under a rhythm | 4–6 min for five plates |

**Eyvind Stall** `[SPLINTER]` is not a combatant. He never attacks. He is stopped by an interaction and yields at once.

**The node is never an encounter.** It has no health, no target frame, no name, no AI. The dust shapes do nothing; they are the tell. The pulses are environmental, roll out from the centre stone on a rhythm set by the ringing plates, and stop entirely when the horn stops (C11, R07).

**Rules**
- **Combat never reveals evidence.** The trial record is found on the bench; Iven's list is his own log; Ingrith's name is Eyvind's testimony after he yields.
- Defeated crew **yield** and are tied (prop). Nobody is killed in presentation (TD-7).
- **Death:** respawn at the Upper Landing (before `S07`) or in the Counting Room (after). Defeated crew stay defeated. Damped plates stay damped. Unbolt segments persist.
- **Co-op:** shared crew and pulses. Each partner marks their own sketch; the **host's** map tier sets the shared start state (fallback). Plates are shared objects: any partner can listen, unbolt or carry; all present are credited. Kaldren answers whoever asks.

## B8. The discovery and strange moments: presentation specs

### B8.1 The whisper hall: solution table (design)

Iven's sketch draws three carry lines per mouth. Each alcove sits on exactly two lines from different mouths; the null alcoves always lie at a line's far end, so sound from nearer alcoves still reaches the mouth while a whisper sent past them is swallowed.

| Mouth | Line | Alcoves on it (near → far) | **Listen** (what comes along it) | **Whisper** |
|---|---|---|---|---|
| Low Mouth | Left | I → II | A file on metal, slow, near. A man swearing at it softly. | Gone |
| Low Mouth | Ahead | dais | A horn note, very loud, and a man counting four. | Back |
| Low Mouth | Right | VI → V | Dice in a cup. A voice muttering about luck (with leverage: two voices, one laughing). | Gone |
| Long Mouth | Left | III → II | Someone humming the test note, badly. A cough. | Gone |
| Long Mouth | Ahead | dais → IV | The horn note; under it, water dripping into a bucket, steady, no breath near it. | Back |
| Long Mouth | Right | I → VI | The file on metal; further off, dice. | Back |
| Crown Mouth | Left | III | Humming, close. The cough again. | Back |
| Crown Mouth | Ahead | dais | The horn note, and the hall humming after it. | Back |
| Crown Mouth | Right | IV → V | The drip, near. Nothing else. | Gone |

**Solution:** I = Crew (file: Low-Left ∩ Long-Right). II = Silent (both its lines eat whispers). III = Crew (humming: Long-Left ∩ Crown-Left). IV = Empty (drip, no breath: Long-Ahead ∩ Crown-Right). V = Silent (both lines eat whispers). VI = Crew (dice: Low-Right ∩ Long-Right).
The decoy is IV: it is audible but holds no one. A player who marks IV as Crew fights one fewer surprise than they expected and loses one correct mark. Nothing worse happens.

### B8.2 The way in (map tier)

| Correct marks (of 6) | `TSH_MAP_TIER` | Way in | Start state |
|---|---|---|---|
| 5–6 | good | Quiet Passage (W5) into alcove V | Crew unalerted in alcoves facing the dais; first strike on VI; I and III join after ~6 s. The sketch overlay shows crew positions the player marked correctly. |
| 3–4 | fair | Open stair (W6) | Crew alerted on the last turn of the stair; they hold their alcoves; VI and I engage first, III (hornman) joins as a second wave. |
| 0–2 | poor | Open stair (W6) | Crew gathered before the dais; hornman's call already sounded (buff ~20 s); all engage together. |

### B8.3 The hall answering (Beat 7 onward)

| Time (per cycle) | Element | Spec |
|---|---|---|
| 0–2 s | **The count** | Eyvind taps four on his heel (audible across the hall; subtitle "[Four taps.]"). After `S08`: no taps; instead the hum steps up (~1 s). |
| 2–5 s | **The note** | The test note: one long horn tone through the frame, rich, beautiful, slightly too loud for the room. Not an Ordinary Call; no call glyph. |
| 5–7 s | **The hum and the dust** | A low hum rises from the floor and walls, felt as much as heard (rumble). Around the centre stone, dust lifts off the floor and spills into rough upright shapes that lean outward toward the walls. They never hold a form and never turn toward anyone. |
| 7–8 s | **The pulse** | A ring of pressure rolls out from the centre stone to the walls: a visible shimmer in the dust, snow lifted off the floor in a ring, torches flattened. Damage and stagger in the open (§B7). |
| 8 s+ | **Settling** | The dust falls back loosely (not straight). The hum fades to a floor. Eyvind breathes in. |
| Rules | | The hum, dust and pulse have no voice, no face, no target and no intent. No NPC says they are a guardian, a warning or a judgement except as a crew belief bark, which nobody confirms. |

### B8.4 The silence (Beat 10)

| Time | Element | Spec |
|---|---|---|
| Trigger | The fifth plate is set down in a silent alcove. | |
| 0–0.5 s | **The cut** | The remaining hum stops, not fading: it is simply gone. |
| 0.5–3.5 s | **The breath** | **All audio** goes to silence: ambience, wind at the great mouth, NPC breathing, the player's footsteps, UI sounds. The player can move; their steps make no sound. Controller rumble stops. This is the only total silence in Thornfell. |
| 0.5–3.5 s | **The dust** | The last loose dust in the air, which was drifting from the centre stone toward the player, **falls straight down**, as it does in a null-point, everywhere in the hall at once. |
| 3.5–6 s | **The return** | Sound comes back in order: wind at the great mouth first, then Iven's breath, then the player's footsteps, then Eyvind: "Oh." |
| UI | | No objective update until the return completes. No music. |
| After | | The great hall no longer hums without a storm. On later visits it is a quiet hall with a cold wind; in a storm it hums as storms make it hum, without pulses. |

## B9. Quest structure for implementation

### B9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to Iven Ridgeborne. | `TSH-D1` end | Yes | Quest Active. Iven's list readable |
| `S01_stair_foot` | Meet Kaldren at the foot of the Summit stairs. | Enter stair-foot volume + `TSH-D2` end | Yes | |
| `S02_ascent` | Climb the Summit stairs. | TSH-E1 ended + enter Echo Landing volume + enter Upper Landing approach volume | Yes | Channel draws; Echo Landing presentation |
| `S03_landing` | Deal with the lookouts. | TSH-E2 defeated | Yes | |
| `S04_listen` | Listen at the three mouths. | Listen ×3 (one per mouth) | Yes | Whisper interactions optional but logged; margin notes auto-written |
| `S05_mark` | Mark the crew and the silent alcoves on Iven's sketch. | At least one mark placed | Yes | Marks editable until `S07` starts |
| `S06_null` | Find out how Kaldren tells a quiet room. | Enter Counting Room + `drop_grit` + `speak` + `TSH-D5` end | Yes | Sets `TSH_NULL_TAUGHT` |
| `S07_great_hall` | Stop the test. | `TSH-D4.50` (commit) + TSH-E3 defeated | Yes | Sets `TSH_MAP_TIER` on commit; entry route by tier |
| `S08_stop_eyvind` | Take the horn from Eyvind. | `take_horn` channel complete + `TSH-D6` end | Yes | Pulses switch to plate-driven rhythm (TSH-H1) |
| `S09_silence` | Find the plate carrying the others. / Carry it to a quiet alcove. | 5 plates set down in II or V | Yes | Listen / Ask Kaldren / Unbolt (2 seg) / Carry / Set down; silence presentation on the fifth |
| `S10_records` | Take Eyvind's trial record. / Set it beside Iven's list. / Talk to Eyvind. | `TSH_trial_record` acquired + side-by-side + `TSH-D10` end | Yes | Sets `TSH_RECORDS_SET`, `TSH_NAMED_QM` |
| `S11_choose` | Decide what happens to the horn. | Outcome interactions complete (silenced: Kaldren's marks; broken: 3 strikes × 2 alcoves; surrendered: wrap × 2) | Yes | Sets `TH_HORN` |
| `S12_crown` | Climb to the Crown with Iven. | Enter Crown volume + `TSH-D12` end | Yes | High routes unlocked; quest → Completed; TF-M5 armed |

### B9.2 Flags

| Flag | Set by | Read by (here) | Read by (later) |
|---|---|---|---|
| `TSH_MARKS` (per alcove) | Sketch UI | `TSH-D4` | — |
| `TSH_MAP_TIER` = good / fair / poor | Commit in `S07` | Entry route, TSH-E3 start state, barks | — |
| `TSH_NULL_TAUGHT` | `S06` | `S09` (Kaldren's grit lines) | *The Notes We Keep*, TME05 (variant lines: the player can name a null-point) |
| `TSH_WRONG_PLATES` (count) | Wrong unbolts | Kaldren barks | — |
| `TSH_RECORDS_SET` | Side-by-side | `TSH-D9` | TF-M5 Assembly line (the trial record "dated against a Warden log") |
| `TSH_NAMED_QM` | `TSH-D10` | — | **TF-M5** (Ingrith's opening lines assume the player has her name) |
| `TH_HORN` | `S11` | `TSH-D11`, `TSH-D12` variants | *The Notes We Keep*; TF-M5 lines |
| Read: `TH_STORES` | TF-M2 | TSH-E3 crew count; `TSH-D10.20` | — |
| Read: `TH_BRYNJAR` | TF-M2 | Post-quest barks (broken) | — |
| Read: `TES_CHITS_READ`, `TES_UPHILL_SEEN` | TF-M3 | `TSH-D1`, `TSH-D10` options | — |

Quest item: `TSH_trial_record` (acquired `S10`; kept).

### B9.3 Choice: what happens to the horn

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Silenced** (`TH_HORN = silenced`): *leave the plates damped in the quiet alcoves; Kaldren keeps them* | The plates stay on the Summit in alcoves II and V, under Kaldren's chalk. Nobody hears them. | The horn exists. Anyone who carries the plates out of the quiet could start again. Kaldren must come up to check them, and he is old. Iven: "Somebody will want them." | ***The Notes We Keep***: Kaldren brings one plate down to the Signal Terrace in a null-lined box. TF-M5: what is left of the splinter knows where the horn is (Ingrith's `TSW-D4.03` silenced line). |
| **Broken** (`= broken`): *crack them in the quiet* | Five plates cracked in the silent alcoves: no sound at all. Nobody can rebuild the Wall-Horn, or any horn from these plates. | **Brynjar's clan loses its proudest boast**: the horn that split the ridge is gone for good, and the Echohewn work with it. Kaldren does it with the player and does not like it. Eyvind weeps. | ***The Notes We Keep***: the shards only (a question of what Thornfell keeps without a horn). TF-M5: Brynjar's lines are sharpest (variant by `TH_BRYNJAR`). |
| **Surrendered** (`= surrendered`): *wrap them for the Wardens to carry to Ressa for the Assembly* | Ridge Wardens carry the plates down under Ressa's seal for the Assembly to decide. | The Assembly now holds a horn it will argue about. Ressa does not want it ("I keep the horns anyway."). The plates leave the quiet and must be kept in a null-room at Stonewake. | ***The Notes We Keep***: used as the bible says (never reinstalled in any horn). TF-M5: the Assembly has the plates in the room. |

**All** outcomes: the Summit stops humming without storms; the trial record and Iven's list stand; Ingrith is named. None is wrong. `TH_HORN` changes Assembly lines only (bible §9.3), never posture.

## B10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| The Summit quiet | World change | No hum without a storm; the great hall becomes a revisitable quiet hall (Kaldren there in the silenced outcome). |
| **High routes** | Access | Agility-trigger routes across Thornfell, each with a walkable fallback for click-to-move [NEW, MAP VERIFICATION REQUIRED]: **the Crown Traverse** (Summit → Stormwake road above Black Glass Hostel); **Iven's High Path** (Summit stair foot → Ridgewall above the Old Watchfire Line); **the Rim Way** (Oath Cairn Fields → Shatterfall rim, joining Carrick's ladders). Fallbacks: the existing valley roads (longer). |
| Kaldren's quiet-room test | Knowledge | The player can test any null-point with grit and voice (inspect variant lines everywhere null-points exist: TDS01, TME05, TGM's den). |
| Small payment | Currency | A Ridge Warden scouting due from Iven (economy tuning). |
| Skill XP | Action only | Melee; Ranged if used. |
| Side-quest unlocks | Story | *The Notes We Keep* (with *Witness at the Gate*). |
| TF-M5 | Story | Armed: on next entry to Windscar Pass or Stonewake, the blizzard comes in. |

## B11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Wrong or blank marks | A harder fight start (§B8.2). No failure, no retry needed. |
| Player never whispers | Listening alone still locates the crew; the silent alcoves are marked for them by Kaldren in `S09`. |
| Caught in a channel draw | One step back; lantern out; Iven relights. No damage. |
| Caught by a pulse | Damage and stagger; while carrying, the plate drops and is picked up again. |
| Wrong plate unbolted | Next pulse ~6 s early; plate still damped. |
| Death | Respawns per §B7. Crew defeated, plates damped, unbolt segments and the trial record persist. |
| Leaving the Summit mid-quest | Stays Active at the persisted step. Before `S07`, the crew are still at their test (state persists). After `S08`, the plates keep ringing until the player returns (per-player presentation); the hum is audible from the Crown stair as a lure. |
| Walking away | Resume hook: Iven at the stair foot (`TSH-D2.90`) or, before `S01`, the original offer location. |
| Fail state | None. |
| Co-op | §B7. Each partner makes their own `TH_HORN` choice; prop fallback: the first choice in the shard sets the visible alcove state; the other is stored and read later. |

## B12. Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| **Listening points** with directional cues | Systems + audio + UI | Three interaction points; each plays an authored three-direction mix (left / centre / right) with subtitles naming direction and sound. Data per line (§B8.1). |
| **Whisper-down-a-line** | Systems + audio | Per-line interaction with an authored result: return or no return. |
| **Sketch marking UI** | UI | A document view of six alcoves with three-state marks and an auto-written margin log; marks persisted; commit locks them and computes `TSH_MAP_TIER` from an authored answer key. Fallback: a dialogue-based marking ("Alcove one: crew / silent / empty"). |
| **Null-point volumes** | Systems + audio + VFX | Footstep and voice audio duck/flatten inside; dust particles fall straight; pulse damage negated. Reused for TDS01, TME05, TGM. |
| **Air-channel draw** | Systems + VFX | Periodic volume with a torch-lean tell, a one-step push and a lantern-out state. |
| **Node pulse hazard** | Gameplay + VFX + audio | A ring AoE from a fixed point on a period driven by quest state (Eyvind playing / plates remaining / wrong-plate offset). Pillar shadow volumes and alcove volumes modify damage. No entity, no target frame. |
| **Plate frame** | Systems | Five plate objects with listen result (carrier / not) from an authored order; unbolt (2 persistent segments); heavy carry state with drop-on-hit; set-down volumes in II and V. |
| **Total-silence presentation** | Audio | A one-shot that mutes every bus (including UI) for ~3 s, then restores in a scripted order. |
| **Side-by-side document view** | UI | Reused from TF-M3. |
| **Entry-route variants** | Systems | Map tier selects Quiet Passage or open stair and the crew's start state. |
| Creatures | Schema / Gameplay | Ridge crow flock, diver; Iron Winter spear, hornman. |
| Quest item `TSH_trial_record` | Schema | Non-droppable document with inspect text. |
| **High-route agility triggers** | Systems + Zone | Three routes, each with a walkable fallback; unlocked by TF-M4 completion. |

## B13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The Summit guardian** (R07) | A passive Stonebound node coupled to the Wall-Horn's Echohewn plates; it responds physically to the disturbance and stops when it stops. | It judges intruders; it warns of Emberholt; "the stones remembering". | Trial record dates = Iven's no-storm hums; the hum stopping when the last plate is damped; the dust falling straight. | The guardian was angry and the player calmed it; the plates are alive. | Makers; the node's extent; what it is [CANON]. | **TF-M4 (owned).** |
| **Who leads the Iron Winter** | Ingrith Scarrow `[SPLINTER]`, former pass quartermaster. | Unknown. | Eyvind's testimony; "the Quartermaster" on the trial record's flyleaf. | Brynjar; the Blood-Oath clans as a body; Emberholt agents. | Her plan's details. | **TF-M5.** |
| **What she will do** | Fire the Gatefall's re-propped deadfalls in a blizzard. | — | "Close the wall herself if she can't sound it." Iven's weather line. | She will blow the horn from the passes. | Where and when. | TF-M5. |
| **The echo before sound** | Unexplained forever (bible §7.4). | Iven: "That one. Every time." | The Echo Landing. | It proves the node is aware. | Everything. | Never. |
| **The tally grooves in the Counting Room** | Echohewn counting. | — | The bench. | A record someone could read. | What they count. | Never (TD rule: no origins). |
| **The great mouth** | An acoustic opening; Kaldren's limit on reactivation. | — | Kaldren's refusal. | It is a weapon. | Its purpose. | Never in Thornfell. |

## B14. Open decisions

1. **TD-1 swap layer:** Eyvind is named in `TSH-D6`, `TSH-D7`, `TSH-D10` and on the trial record; Ingrith is named only in `TSH-D10` and on the trial record's flyleaf ("for the Quartermaster"). All tagged `[SPLINTER]`.
2. **Frost-count calendar** [NEW]: Ridge Warden days counted from the first frost on the Passwatch horn rail. Used by Iven's log and Eyvind's record so the dates match. **Coordinated with Act I (independent review):** frost-count is the wardens' and hornwrights' reckoning; Bersi's ledger uses the storekeepers' weeks counted down to First Smoke. Both are local reckonings in use at once, no page converts one into the other, and the TF-M2 ledger's "weeks before that night on the Cut" line stays untouched. Vessa's slate keeps its undated *Dusk. Storm.* Needs Director acceptance only.
3. **High routes:** the three named routes and their endpoints need the zone package (MAP VERIFICATION REQUIRED).
4. **Plate count** (5) and pulse timings are Gameplay Designer calls.
5. **Map tier thresholds** (5–6 / 3–4 / 0–2) are tunable.
6. **Eyvind's custody** after yielding: held by the Ridge Wardens pending the Assembly (consistent with TF-M5's clan tribunal for Ingrith). *The Notes We Keep* needs him available.

## B15. Internal review log

| Finding | Revision |
|---|---|
| The node risked reading as a boss (dust shapes "attacking"). | The shapes are only the tell; pulses are a ring hazard from a fixed stone; no target frame, health or AI. The dust leans outward toward the walls, never toward anyone, until the final breath, when it falls straight. |
| Kaldren risked explaining the node. | His lines are rules ("listen, don't knock"), function ("builders worked loud and counted quiet"), stress readings and one fixed line: "Stresses settled. That's all I can tell you." |
| The triangulation risked being unsolvable or a hidden fail. | Full solution table (§B8.1) with each alcove on two lines; the margin log records everything heard; wrong marks only change the start state. |
| Null alcoves needed a guaranteed path for the plate carry. | Kaldren tests and names them at the start of `S09` if the sketch is wrong. |
| Silencing risked duplicating TF-M3's strike-and-count. | Kaldren forbids striking. The player listens to an existing hum and asks Kaldren to read bolts; nothing is struck until the broken outcome, which happens in the quiet. |
| Eyvind risked being fought. | He is a craftsman; he never attacks; he is stopped by an interaction. |
| "Stops when the horn stops" vs. Eyvind stopping. | The horn is the frame, not the mouthpiece: the plates ring on until damped. The hum stops with the last plate, exactly. |
| Iven risked interpreting. | He reports dates, hours, winds and the rota gap; his only interpretation is "Mountains get tired. Not like this." and "Every one." |
| Ingrith named by a phenomenon or combat. | Named only by Eyvind's testimony after yielding, and on a flyleaf in a record the player picks up. |
| Brynjar's "proudest boast" cost in the broken outcome. | Kept, with `TH_BRYNJAR` variant barks; no family casualty or war service assigned to him. |
| Quest-item budget. | `TSH_trial_record` is Thornfell item 3 of 4. Iven's list and sketch stay with Iven. |
| **Independent review (2026-11-03)**, TF-M4: 4 findings (1 medium, 3 low). | "The splinter's remnant" reworded (could read as the Remnant faction). Frost-count coordinated with Act I's ledger reckoning. `[SPLINTER]` tags added to `TSH-B3.5`, the `TSH-D9` Eyvind option, the `TSH-D12` Ingrith option and `TSH-D12.10`. |

---

## Act II cross-check (final review)

| Rule | Check |
|---|---|
| Canon anchors | **Dorn:** altered echoes are "wind tricks"; his Shatterfall knowledge comes from the roster ("It's what it says. I wasn't there."); he neither carries nor keeps the roster (a runner carries it in `kept`). **Maera:** decides the stone; no grave or echo identifies anyone; her list is a record, set beside another. **Torvek:** one sentence; no wartime claim. **Kaldren:** no origins, no Summit validation, stresses only; limits reactivation (no knocking; the great mouth). **Iven:** direction, weather, timing first. **Brynjar:** barks only; no splinter membership; no family casualty. **Ressa:** receives plates for the Assembly in one outcome; no roster custody. |
| Evidence rule | Rack aim, strata, roster, list, trial record and Iven's log carry R06 (horn) and R07. Echo-figures, the stand, the uphill group, the hum, dust and pulses identify no one and prove nothing. Ingrith's name is testimony. |
| Withheld | Who blew the Split; how many died (TD-9). The node's makers and extent. |
| Three states | No fail or abandon logic in either quest. Loose irons, masked strikes, wrong marks, wrong plates and dropped plates cost time or ease only. |
| Guaranteed paths | All R06/R07 custodians are required steps. Null alcoves are named by Kaldren if unmarked. The storm window always turns. |
| No cutscenes | Every presentation spec keeps the player camera and control (the silence lets the player walk). |
| Solo / co-op | Solo-clearable; per-player storm, sounding and sketch state with host fallbacks. |
| Movement reality | Click-to-move; agility triggers (shelf gap, seat scramble, broken flight, high routes) all have walkable fallbacks; channelled climbs and interactions are untimed except for the "between pulses/swells" windows, which are generous and repeatable. |
| Quest items | 2 in Act II (`TES_horn_roster`, `TSH_trial_record`); Thornfell running total 3 of 4 with `TIW_store_ledger`. |
| Region flags | Read: `TH_CALLS`, `TH_PASSWATCH_ROUTE`, `TH_STORES`, `TH_BRYNJAR`, `TH_SEASON`. Set: `TH_SHATTERFALL_ACCOUNT`, `TH_HORN`. No new `TH_` flag. |
| Splinter tagging | Every node naming Eyvind or Ingrith is `[SPLINTER]` in the dialogue file; the pay chits' initials and the trial record are tagged. |
| Map | Relative placement only; MAP VERIFICATION REQUIRED in §A5, §B5, §B10. No grain route stated. No Remnant presence. No compass toward Emberholt. |
| Magic stays dormant | No NPC calls anything magic; no player spellcasting; the Horn-Echo is a "wind trick", the hum is "the hall ringing", null-points are "quiet rooms". |
| Lowmark independence | No Lowmark state is required. One optional variant (`TES-D2.40`, Lowmark MQ3 Completed) is flavour. |
