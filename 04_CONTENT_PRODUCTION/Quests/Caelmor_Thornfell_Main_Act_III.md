# Thornfell Main Questline, Act III: Stonewake

**Status:** Authored production content for Creative Director milestone review. This package implements Thornfell milestone **TF-M5 *Stonewake*** (`TSW`), the regional capstone, as written in the Thornfell bible §6 table and §6.1 brief, with the Assembly posture algorithm of §9.3 and the calls of §9.4. Everything marked **[NEW]** is authored here and is not canon until the Director promotes it. **[PROPOSAL — DIRECTOR]** marks a consequential choice the content is built on. **[CANON]** marks material taken from Phase 1 or the reconciled `LORE/` files. **[APPROVED — id]** marks an approved foundational truth. No schema, production JSON or C# is created here.

**Controlling document:** `04_CONTENT_PRODUCTION/Quests/Caelmor_Thornfell_Narrative_Production_Bible.md`. Its §6.1 TF-M5 brief, §9 world state and §11 conventions are binding and are implemented as written. Where this package invents detail, it is marked [NEW] and stays inside the bible.

**Companion file:** `04_CONTENT_PRODUCTION/Dialogue & Narrative/Caelmor_Thornfell_Main_Act_III_Dialogue.md`. It holds cast notes, every dialogue node referenced here (`TSW-` prefix), barks, inspect texts, the full text of the closure roster and of the rubbing, Hushfold's first tally-book entry, the Assembly variants, epilogue barks and the commission offer lines.

**Format:** this package follows the Lowmark act-package format (`Caelmor_Lowmark_Main_Act_I.md`, Part C; `Caelmor_Lowmark_Main_Act_III.md` for the capstone boss spec and ending matrix). Every node or beat naming Ingrith Scarrow, Bersi Coldbrook or Eyvind Stall is tagged `[SPLINTER]` (bible §3.1).

**Parallel authoring note.** TF-M1 to TF-M4 and the Thornfell side quests are being authored in parallel. This package reads only the region flags exactly as bible §9.1 defines them, plus the few quest-local flags the bible itself names (`TPW_NAMES_ASKED`). Where it relies on an Act I/II detail the bible does not fix, it states a fallback and lists the dependency in §12. (Independent review: TF-M1 gives the player the Hornbearer's practice horn as a reward tool, Act I §A6 Beat 12 and §A10; TF-M5 relies on it.)

---

## Act III header

### What Act III does

Acts I and II gave the player three findings: a splinter is arming on its own (TF-M2), Thornfell's proudest horn killed its own rear guard (TF-M3), and the Summit's "guardian" is old stone answering a noise the splinter made (TF-M4). Act III turns all of that into **one night at the far gate and one morning in a hall**. The player climbs to the Gatefall by sound alone, stops the splinter's last crews, finds the names Thornfell shut out the last time it sealed itself, holds the gate open while the people it is about to shut out again come through, and then stands somewhere in the Assembly.

| Quest | Code | The player learns | By doing |
|---|---|---|---|
| TF-M5 **Stonewake** | TSW | Thornfell held the wall by leaving people outside it, and the hunger winter it blames on Emberholt came partly through its own gate. | Climbing blind by horn calls, reading gallery glyphs, holding a winch, answering a Lost call, and choosing where to stand. |

**Act III turn (bible §1 part 3; R06 sealing half):** "Thornfell held the wall" becomes "Thornfell held the wall and left people outside it." The player leaves with Thornfell's tool for the peace: **an honest closure** (a closing that names who is left outside), decided by an Assembly that has no ruler.

**Length:** 60–75 minutes including the Assembly (bible §6). **Level framing:** Advanced identity, Milestone 3 equipment (TD-12). Exact levels belong to the Gameplay Designer.

### Inputs read (region flags set by Acts I–II and side quests)

TF-M5 never asks how an earlier flag was set; it reads only the §9.1 values. Every value has authored content. No value can block progress. A player who did no side quest has a complete, authored path.

| Flag | Values | Read in | Effect in TF-M5 |
|---|---|---|---|
| `TH_CALLS` | bool | Everywhere | Always true after TF-M1 (required). Turns on the call-shape glyphs used by the whiteout climb, the galleries and the stragglers. Authored fallback in §6 if ever false. |
| `TH_PASSWATCH_ROUTE` | sledge / caravan / split | Assembly placement (Ketil and Nettlehook); posture (+open if sledge); Nettlehook epilogue | Who owes whom at Nettlehook; Ketil's place in the hall. |
| `TH_STORES` | reported / seized / leverage | Gallery crew strength; boss phase 2; Ingrith's lines; posture (+sealed if leverage); Assembly lines; Whinstone epilogue | Leverage: crews are well fed and armed with new spearheads; seized: one gallery is unmanned. |
| `TH_BRYNJAR` | disowned / defended | Assembly placement; posture (±1); tribunal line | Where Brynjar stands and what he says about Ingrith's tribunal. |
| `TH_SHATTERFALL_ACCOUNT` | amended / beside / kept | Assembly placement (Maera); posture (amended +open, kept +sealed); reader line | Whether Maera stands near the speaking stone. |
| `TH_HORN` | silenced / broken / surrendered | Ingrith's lines; Assembly lines; Kaldren's attendance; epilogue | Lines and props only (§9.3 rule 5). |
| `TH_THIRD_HORN` | bool | Stragglers (`S07`) | True: the player blows the restored Third Horn. False: Dorn blows Answer from the gate. |
| `TH_HUSHFOLD_VOICE` | bool | Assembly placement (Runa near the stone); posture (+open); reader | Who reads the rubbing. |
| `TH_HIGHSTEADS_TOGETHER` | bool | Assembly placement (Nettlehook beside Hushfold); posture (+open) | |
| `TH_BANNER` | blood-oath / hearthguard / shared | Assembly placement (Torvek, the banner); posture (+sealed if blood-oath) | |
| `TH_SEASON` | snow | Presentation | Always snow by TF-M5 (TF-M2 sets it). The blizzard is a quest-local weather event (§9.2). |

| Quest-local or completion condition (never required) | Read in | Effect |
|---|---|---|
| `TPW_NAMES_ASKED` (TF-M1) | Dawn (`TSW-D8`) | Vessa remembers the player asked her to write who was outside. |
| TDS10 *The Gatefall from below* inspected (`TDS10_SEEN`: **[NEW] placeholder; Batch 3 package fixes the name**) | Galleries | A bark and a tick on each pale-propped marker: "Three pale. Same as from below." |
| *The Weight of a Name* (TWN) Completed | Assembly reading; Maera's line | Maera notes this is the second wall this autumn that kept names nobody read. Name-slip weight only (bible §8.1). |
| *A Place at Smoke Week* (TSM) Completed or TME01 tally-add (`TME01_TALLIED`: **[NEW] placeholder; Batch 3 package fixes the name**; the Batch 3 draft currently uses `TME01_EXPECTED`) | Runa's lines | Runa uses the player's name instead of "walker" (bible §5.3 rule 4). |
| *The Third Horn* (TTH) Completed | Stragglers | Read through `TH_THIRD_HORN`. |
| *Ash in the Snow* (TAS) Completed | Assembly (optional bark) | Tessaly Varn's crew stands at the back wall. One line. Never a placement factor. |
| `LM_CIVIC_STANDING` (Lowmark) | Assembly (optional line) | Elira's one variant line about the Vale deciding at one table. Never a gate. |

### Region flags this act sets

| Flag | Values | Set by | Notes |
|---|---|---|---|
| `TH_COLUMN` | player_brought / patrol_brought | `S07_stragglers` end | player_brought only if the player brought **both** stragglers in. Every straggler is safe either way. |
| `TH_STAND` | hushfold / wardens / cairn / brynjar | `S10_stand` | The player's own place in the hall. |
| `TH_ASSEMBLY_POSTURE` | watchful / open / sealed_with_terms | `S11_reading` end | Computed by §9.3 (§9.3 of this package restates it). |
| `TH_STANDING` | bool | `S12_close` | Always true at completion. Opens the Thornfell master commission offers (§E.8), LR-M1 and the convergence chain. |

Act III invents no other `TH_` flag. Quest-local flags use `TSW_` (§9.2).

### Quest-item budget (bible §9.5: Thornfell total 4)

| Item | Quest | Fate |
|---|---|---|
| `TSW_closure_rubbing` | TF-M5 | Kept by the player after the Assembly ("The wall has the cut one. Keep that."). Not droppable, not sellable. Seeds the CV-M3 "stranded refugees" chip (bible §8.2). Thornfell item 4 of 4. |

Everything else is a carry-state object (a rope line to a straggler, a gallery wedge, the charcoal and count sheet before the rubbing is made), a loaned or existing tool (the player's horn), or an inspectable world object (the roster wall, the drill board, Hushfold's first tally book, which Runa keeps and never hands over).

### Canon grounding (Act III)

| Element | Source | Status |
|---|---|---|
| Hadrik chooses where people stand; knows the hall carries some voices; never asks why; scars never dated | Thornfell anchors I; Part 4 ledger | [CANON] |
| Assembly as Thornfell's government form; clan tribunals; no ruler | Dossier; Factions §16 | [CANON] |
| Ressa refuses certain calls and keeps the horns | Anchors IV | [CANON] |
| Dorn maintains the long-range codes; altered echoes are "wind tricks" | Anchors IV | [CANON] |
| Maera: absolute authority in matters of the dead; no grave identifies anyone by itself | Anchors V; Part 4 ledger | [CANON] |
| Brynjar loud, loyal, would die for any Thornfell child; not in the splinter | Anchors II; bible TD-1, TD-2 | [CANON] / [PROPOSAL — DIRECTOR] |
| Thornfell's late-war sealings stranded people; "Thornfell held the wall" | World Truth H16 | [APPROVED — FT-02b] |
| Sealing at the Gatefall was mechanical (deadfalls on pins, ordered by horn call); no resonance at this site | Bible §2.1, TD-8 | [PROPOSAL — DIRECTOR] (narrows FT-02b for this site only) |
| The closure roster; its unnamed cutter | Bible §2.1, TD-10 | [NEW] |
| Hushfold as a clanless shelter line; Runa Weatherall | Part 3 proposal; bible §5.2, TD-4 | [NEW] |
| Ingrith Scarrow and the Iron Winter | Bible §2.3, TD-1 | [NEW] `[SPLINTER]` |
| The Ordinary Calls; the Third Horn | Bible §9.4 | [NEW] |
| Human enemies yield | Bible TD-7; Lowmark D-13 | [PROPOSAL — DIRECTOR] |
| Agility triggers are optional with walkable fallbacks | Phase 1.3 §1 | [CANON]; approved, not yet implemented |

### Structure check against the bible §6 core verbs

| Milestone | Primary verb | Distinct from |
|---|---|---|
| TF-M1 | repair and escort against a clock | — |
| TF-M2 | track and delve | the only cliff dungeon |
| TF-M3 | rope-rig rescue by echo count | echo count used to find **rock** |
| TF-M4 | listen and triangulate | the whisper hall; null-points |
| **TF-M5** | **whiteout climb by horn alone**, read gallery glyphs, hold the gate; then **stand** | Echo count used to find **the face you are walking along** (not anchor rock); horn calls used as **the only guidance** (not taught, as in TF-M1); the only channelled hold in Thornfell's main line; the only scene where the player's answer is a place in a room. |

No set piece repeats: TF-M1's bridge is built in wind windows; TF-M5's slab is wound in them. TF-M1 counts down a gate closing; TF-M5 holds one open.

### Unlocks across Act III

After TF-M5: `TH_STANDING`; Thornfell master commission offers (§E.8); the Gatefall as a revisitable site with a horn post; the post-game Thornfell states (§E); LR-M1 eligibility (with Lowmark's `LM_CIVIC_STANDING`, per the architecture); the thaw presentation (§E.7).

---
---

# TF-M5 Stonewake (`TSW`)

## 1. The quest in one paragraph

The early blizzard comes in the day after the Summit goes quiet, and Ressa Highcrag's **Gather** sounds from every tower on the ridge. At Three Calls Shelter she tells the player what Iven saw from the high path before the snow closed it: the last of the Iron Winter crews have taken the **Gatefall** gatehouse at the far end of Windscar Pass and are dropping the deadfall galleries they quietly re-propped this autumn, to seal the far gate for the whole winter. **Hushfold's winter column**, thirty-one people bringing the herds and the last wood down from the far shielings, and **Vessa Galt's patrol** are still beyond it. Above Three Calls the snow takes the world to white. Sight is useless, so the player climbs toward the wardens' horns: Gather means come, Fall means stop and shelter, and the echo off the cliff says how near the face is. Under the Gatefall the cut makes its own lee, and the player can see again: seven galleries above the gate, most of them grey-propped and spent since the war, three of them braced with fresh pale timber. A splinter hornman on the gatehouse roof calls the old sealing order, one gallery at a time; the player hears each call, matches it to the glyph on a gallery's marker stone, and reaches the live ones before their wedge crews can pull. A gust drives the player into the gatehouse's warden room, where the crew's three-night fire has cracked the plaster off the inner wall. Under the soot are dates, and beside each date, names: the people on the far side when the slab came down, and, beside some dates in the final year's long winter, a shorter line: *relief train turned back*. One of the names is **Weatherall**. The player takes a rubbing. Above, at the gate-slab winch, **Ingrith Scarrow** `[SPLINTER]`, the Quartermaster, has the slab half down and is counting. She fights, and yields. The player winds the slab back up and holds the winch while Hushfold comes through under the last loose gallery, and Runa Weatherall reads Hushfold's first tally book aloud as her people come in, the way every host reads a tally on first snow: *"Weatherall, came over in the thaw."* Two herders are still out. The player answers their Lost call, and brings them in, or leaves them to Vessa's patrol, which finds them at dawn. The next day the Assembly meets at Stonewake. There is no hearing. Hadrik Stonewake places people where they will stand, and asks the player where they will stand. The rubbing is read aloud once. The hall decides by where it stands, Ingrith goes to her clan's tribunal, and in every outcome Thornfell starts keeping a closure account: from now on, a closing names who is outside.

**What the player should remember:** climbing blind toward a horn; the names coming out from under the soot; Runa reading her grandmother's name off a page while her people walk past her. **What the player should want next:** to take the closure account, and the standing it earned, out of Thornfell.

## 2. Selection record

| Candidate | Verdict |
|---|---|
| **A. Storm the gatehouse first, then rescue the column.** | Rejected. It puts the boss before the climb and makes the column a cutscene. The brief's order (climb, galleries, roster, boss, hold) builds from sound to sight to names to people. |
| **B. An evidence hearing in the Assembly**, with the rubbing laid as proof. | Rejected by the brief ("no evidence hearing"). Lowmark MQ10 already owns the table-of-proof structure. Thornfell decides by standing. |
| **C. Horn-Echo surges at the Gatefall** (as the architecture summary once proposed). | Rejected by the bible (§2.4, TD-8, independent review): the Gatefall's dangers are ordinary. Gusts, loose stone and whiteout only. Resonance stays at Shatterfall and the Summit. |
| **D. Whiteout climb by horn → gallery glyph puzzle with yielding crews → roster in a forced shelter → human boss who yields → three-segment winch and hold with the tally reading → optional straggler search with a guaranteed patrol fallback → dawn → Assembly by placement** (selected; the bible brief). | **Selected.** One night with one rhythm (blind, then seeing, then reading, then holding), then one morning of standing. |

## 3. Canon grounding

| Element | Source | Status |
|---|---|---|
| Windscar Pass; Passwatch; ridge horns; whiteout storms on the high passes | Dossier §V | [CANON] |
| The Gatefall, its galleries, gatehouse and slab | Bible §2.1, TP09 | [NEW]; mechanism [PROPOSAL — DIRECTOR TD-8] |
| Fresh pale props visible from below (TDS10) | Bible §7.4 | [NEW] |
| Three Calls Shelter (guest ledge with a horn map) | Part 3; bible TP06 | [NEW, Part 3] |
| Hushfold, the far shielings, the far hut | Bible TP04; §2.3 | [NEW] |
| Iron Winter crews: spear, hornman; Ingrith as boss | Bible §10 | [NEW] |
| Ridge Wolves (runner, howler) | Bible §10 | [NEW on dossier ecology] |
| The Assembly Hall at Stonewake; Hadrik places speakers | Anchors I; bible TD-3 | [CANON] |
| Shelter tally read aloud on first snow | Bible TME01 | [NEW] |
| The closure account | Bible TD-5, §6.1 | [PROPOSAL — DIRECTOR] |

## 4. Quest summary card

| Field | Value |
|---|---|
| Working title | **Stonewake** |
| Suggested content id | `thornfell.main.05_stonewake` |
| Arc position | Act III, regional capstone; owns **R06 (sealing half)** |
| Prerequisite | TF-M4 Completed |
| Offer | Automatic: the next time the player enters the Windscar Pass subzone or Stonewake after TF-M4 completes, the blizzard event starts and Ressa's Gather sounds from every tower (`TSW-B0`). Objective appears: *Answer the Gather at Three Calls Shelter.* |
| Target length | 60–75 minutes (night ~45–55; Assembly ~12–18) |
| Combat share | ~25% |
| Traversal and sound puzzles | ~35% |
| Labour (winch, hold) and searching | ~15% |
| Dialogue and standing | ~25% |
| Skills | Melee or Ranged (required for the crews and the boss; either works). No skill gate. Cutting a pull-line uses a plain knife interaction, not a skill. |
| Choices | Each live gallery: drive off the crew or cut the pull-line (local). Stragglers: search or leave to the patrol (`TH_COLUMN`). Where the player stands (`TH_STAND`). |
| Unlocks | `TH_COLUMN`, `TH_STAND`, `TH_ASSEMBLY_POSTURE`, `TH_STANDING`; master commission offers; Gatefall revisitable; Thornfell epilogue states |
| **Anchor** (contribution contract) | **Hadrik Stonewake** (places people; asks the player where they stand). Supporting anchors: Ressa Highcrag (the Gather; the closure account's first writer), Dorn Feldhorn (calls at the gate; the reply), Maera Cairnwatch (reads the rubbing or stands by it), Brynjar Korr, Elira Hearthward, Old Torvek (placement), Iven Ridgeborne (a horn post on the climb), Kaldren Deepdelver (attends only if `TH_HORN = silenced`). All within the Part 4 ledger limits (§15). |
| **World-truth row** | **H16 Thornfell's stop** [APPROVED — FT-02b]: the late-war sealings stranded people on the wrong side; Thornfell never recorded it except here. Quiet mirror (seed only, never stated): the same sealings turned back relief and fed Thornfell's own hunger winter. |
| **Revelation role** | **Owns R06 (sealing half)**. Custodian 1: the closure roster cut in the gatehouse wall, with the turn-back lines (`TSW_closure_rubbing`). Custodian 2: Hushfold's first tally book, read aloud by Runa ("Weatherall, came over in the thaw", dated a thaw after the roster date). Plants: the rubbing's names for the CV-M3 "stranded refugees" chip; the closure account for CV-M3 "witness at every crossing" (bible §8.2). Never explains the seed that the sealings helped push Emberholt (War History §VI). |
| **Recurring evidence** | Vessa's slate from TF-M1 ("We write what we closed. Not who."); Hushfold's clanlessness; the Third Horn's lost meaning (TTH, TF-M3 roster "No answer"); TDS10's pale props; the Ordinary Calls and echo count (TF-M1); the tally read on first snow (TME01). |
| **State compliance** | Three states only (Inactive / Active / Completed). No fail, no abandon, no re-instancing. Every required proof (roster inspect, rubbing, Runa's tally beat) sits on the critical path and persists. The column always comes through; every straggler is always safe. Region flags only from bible §9.1. Per-player state with the Lowmark per-player prop fallback. |

## 5. The places

**MAP VERIFICATION REQUIRED** for every placement in this section. The narrative needs only these: Three Calls Shelter lies between the Narrows and the Whinstone track; the track above it climbs toward the far gate along a cliff face with a roped drop on the open side; the Gatefall is a narrow cut at the far end of Windscar Pass with galleries above it; Hushfold's far shielings and the far hut lie beyond the Gatefall; Stonewake is reachable from Passwatch by the ordinary road.

### 5.1 Three Calls Shelter and the high track [TP06, NEW detail]

| Area | Storytelling |
|---|---|
| **C1. Three Calls Shelter** | The guest ledge with its horn map cut into the back wall (Part 3). Tonight it is a muster point: wardens stamping snow off, a brazier, Ressa at the horn map with a stub of chalk. A Hushfold herd-lad, **Kolli** [NEW], who came down ahead of the column with the count, sits wrapped by the brazier. |
| **C2. The Switchback Stair** | The first leg of the track above the shelter. Cut steps, a rope rail on the drop side. The white closes in here. Warden post **W1**: a young warden (the one Ressa stopped in TF-M1; role name only) blowing Gather on a slow cycle. |
| **C3. The Fluted Run** | A long traverse under fluted faces (bible §1.1). The faces whistle up a fifth before each gust. **Shelter niches** are cut into the face every forty paces, each marked with a red rag tied to an iron ring (visible at arm's length in the white). Warden post **W2**: a pair of wardens who blow **Fall** when the face above sheds. |
| **C4. The Fork** | Where the old drovers' path splits off toward the drop and is roped shut. The Gather from W3 arrives twice here, once direct and once off the opposite face (the echo puzzle, §6 Beat 1). |
| **C5. Iven's Post (W3)** | A ledge with a horn ring. **Iven Ridgeborne** stands here, the high path closed above him by snow. A short encounter zone below it (TSW-E1, ridge wolves sheltering from the same storm). |
| **C6. The Last Rise** | The final climb into the Gatefall's lee. Warden post **W4**: **Dorn Feldhorn**, who came up ahead with two wardens. The white thins as the cut's walls take the wind. |

### 5.2 The Gatefall [TP09, NEW]

| Area | Storytelling |
|---|---|
| **G0. The near apron** | A flat of trampled snow below the cut, where Dorn sets his post. The cut's walls rise on both sides. Visibility here is ~25–30 m: the cut makes its own lee (fiction; tune to readability). |
| **G1–G7. The deadfall galleries** | Seven stone galleries cut into the walls above the cut, each a shelf of stacked stone held back by props, wedges and iron pins, with a **marker stone** at its foot cut with the call-glyph that ordered its release (bible §2.1). Four are **spent** (dropped in the war): grey, weathered props hold up nothing but the gallery roof; their stone lies in old heaps along the cut floor, half buried. Three are **live**: never dropped, their rotten props replaced this autumn by the splinter with **fresh pale timber**, their pins re-set, their pull-lines run down to a ledge (TDS10). Live: **G3 (the Shoulder)**, **G5 (the Lintel)** and **G7 (the Gate gallery)**, directly above the gatehouse. |
| **Gallery ledges** | Each gallery is reached by a cut stair from the cut floor (walkable) or by a short rock scramble (**agility trigger**, optional shortcut). The pull-line of each live gallery runs from its pin-beam down to a **pull ledge** where a wedge crew hauls. |
| **The cut floor** | Old war heaps, a wagon axle frozen into one of them, a grey prop fallen across the path (inspect). The slab slot runs across the cut at the gatehouse. |
| **H1. The gatehouse, warden room** | A stone room on the near side of the gatehouse at cut level. The crew have lived here three nights: bedrolls, a cookpot, a hearth built hard against the inner wall and **kept roaring**. The heat has cracked the old plaster off that wall in plates. Under the plaster and a lifetime of soot: **the closure roster** (§8.2). A warden's desk with a slate shelf (empty) and the crew's paper: Ingrith's count sheets, a stack, figures down one side, the backs blank. A **drill board** on a peg: the wartime sealing order, glyph after glyph (optional inspect). |
| **H2. The stair** | A narrow stair up inside the gatehouse wall to the winch floor. |
| **H3. The winch floor** | An open timber floor over the cut, roofed by a timber hood on the near side and open over the slab slot on the far side. The **winch drum**, the **pawl** (knocked out and lying on the boards), and the **gate-slab** hanging in its slot, half down. A parapet with a horn ring where the **hornman** stands. A fluted parapet stone that whistles before each gust. The far parapet looks down onto the far apron. |
| **F1. The far apron** | Beyond the slab: a flat below the far wall of the cut, where the column gathers to come through. Above it, G7's loose stone. |
| **F2. The far track and the far hut** | Beyond the far apron the white closes again. The track runs toward the far shielings. A **far hut** (a stone bothy) lies some distance out; its exact distance is a zone call. The stragglers are on this track (§6 Beat 7). |

### 5.3 The Assembly Hall at Stonewake [TP01, CANON place; NEW detail]

| Area | Storytelling |
|---|---|
| **A1. The hall** | The echo-carved chamber (anchors I). A round floor; a **speaking stone** at its centre (a waist-high stone with a worn top, where a speaker sets a hand). Nobody sits. People stand where Hadrik places them. |
| **A2. The near ring** | The floor within a few paces of the speaking stone. Voices from here carry to every wall. |
| **A3. The carrying spot** | One place on the near ring, slightly off the stone, where any voice, even a quiet one, comes back clear from every side. Hadrik knows it [CANON: "knows the hall amplifies certain voices"] and never says why. He places the reader of the rubbing here. |
| **A4. The walls and the door** | The outer floor along the walls, where voices fall flat. The **door wall** is where the clanless have always stood. The **side door** is where Ingrith is held between two wardens. |
| **A5. The four standing places** | For the player's choice: **with Hushfold** (Runa's people, door side), **at the wardens' rail** (Ressa and Vessa, a timber rail on the near-ring edge), **by the cairn bench** (Maera's place: a stone bench along the wall with the name-stones' rubbing-board), **at the Blood-Oath table** (Brynjar's stone table, near ring). Their positions in the hall are fixed; who stands near the stone around them varies by flags (§8.4). |
| **A6. The Signal Terrace** | Outside the hall, used only in the epilogue: where public closure accounts are posted and called (`open` posture). |

## 6. Player-facing sequence

### Beat 0 — The Gather (`S00_gather`)
**Objective:** *Answer the Gather at Three Calls Shelter.*
The quest starts the next time the player enters Windscar Pass or Stonewake after TF-M4. The sky goes iron. Snow comes in sideways. From every horn tower within hearing, one after another down the ridge, comes **Gather** (three short), with its three-dot glyph at the screen edge pointing toward the nearest tower (`TSW-B0`). In Stonewake, a warden runner at the Signal Terrace says only: "Three Calls. Ressa's asking for you by name of walker." (`TSW-B0.3`). Travel is ordinary; the storm thickens as the player climbs Windscar.

At **Three Calls Shelter** (C1), Ressa is at the horn map (`TSW-D1`). She gives the situation in her own short way: Iven saw crews on the Gatefall from the high path before it closed; the galleries are coming down one by one; Hushfold's column is beyond the far gate with the herds, and Vessa's patrol went over two days ago to bring them. Kolli, the herd-lad, came down ahead with the count: thirty-one and the herd. Ressa's wardens are posted up the track at intervals: "Climb to the horns. Don't climb to anything else."

- **The player's horn.** The player uses the **Hornbearer's practice horn** Dorn gave them in TF-M1 (Act I §A6 Beat 12; a reward tool, not a quest item). **Fallback only:** a player who does not carry it (for example, if the item pass ever makes it droppable) gets Ressa's **warden's horn** here as a loaned tool (`TSW-D1.20`, option shown only with no horn). The player can blow any Ordinary Call from the horn's call wheel at any time in this quest. Calls are never required inputs except where a step says so.
- **Variants:** `TH_STORES` (Ressa's line about what the crews are eating), `TH_HORN` (her line about the plates).
- **Optional:** the horn map. With `TH_THIRD_HORN`, the map's restored reply mark is chalked fresh (inspect: *"Someone's chalked the Third Horn back onto the map. Recently. Small, neat chalk."*).

**Verbs:** answer, listen.

### Beat 1 — Whiteout (`S01_whiteout`)
**Objective:** *Climb to the Gatefall by the wardens' horns.* (Sub-objective text changes per post: *Go toward the Gather.* / *Shelter. Wait for Rest.*)
Above the shelter the screen goes to white (§8.1). Visibility drops to about three metres. **Sight is useless here; sound is the whole guide.**

**The rules the player already knows (TF-M1), used for real:**

| Call or sound | Meaning on the climb | What the player does |
|---|---|---|
| **Gather** (three short; three-dot glyph) from a warden post | "Come to the call." | Walk toward it. The glyph appears at the screen edge in the call's direction and fades; positional audio is the primary cue. |
| **Fall** (short-long-short; dot-bar-dot glyph) | "Rockfall or slide; take cover." | Stop. Get into the nearest **shelter niche** (red rag on an iron ring, visible at arm's length). Stone sheds onto the track for a few seconds (telegraphed: a grinding creak above, then grit). A player caught in the open takes moderate damage and is knocked down; never lethal at full health. |
| **Rest** (one long; flat-line glyph) | "All clear." | Leave the niche. |
| **The whistle** (a fluted face rising a fifth) | A gust is coming (~2.5 s). | Step into the lee of the face (any niche or the inner wall). In the open, the gust shoves the player a step back toward the inner wall (never toward the drop) and slows them for 3 s. |
| **The player's Answer** (two short) blown at the face | Echo count. | The echo comes back off the face. **One beat:** the face is at your shoulder; you are on the track. **Two beats:** you have drifted out a little. **Three or more, or no echo:** you have wandered out from the face toward the open side; turn back to the wall. A tick mark per beat appears beside the glyph (accessibility). |

**Legs (each ends at a warden post, which is a checkpoint):**

1. **Switchback Stair (C2) to W1.** Teaching leg. W1's young warden blows Gather on a slow cycle. The stair is rope-railed on the drop side: a player who walks into the rope hears "Rope. Wrong side." (`TSW-B1.2`) and cannot pass it. No fall is possible.
2. **The Fluted Run (C3) to W2.** Gusts with whistle tells; twice, W2 blows **Fall** as the face sheds. The player must shelter and wait for **Rest**. A player who ignores Fall is knocked down by grit, gets up, and hears the wardens swear at them affectionately (`TSW-B1.6`).
3. **The Fork (C4) to W3.** **The echo puzzle.** W3's Gather arrives here **twice**: first the direct call, louder and sharper; then, a beat later, its echo off the far face of the drovers' fork, softer and from the wrong side. The glyph shows both (the echo glyph dimmer). Walking toward the echo leads to the roped-off drovers' path (rope boundary; no fall; Iven's horn blows again and the player turns back). Blowing Answer at the inner face tells the player the face is still at their shoulder on the true track. With `TH_CALLS` the player already knows "the first one's the horn; the second one's the mountain" from Aud's TF-M1 lesson; Iven says it again from the post either way (`TSW-B1.9`).
4. **W3, Iven's Post (C5).** Iven gives one short report (`TSW-D2`): direction, weather, timing, and that he heard the galleries calling "the old way" before the snow came. Below his post, **TSW-E1**: two ridge wolves and a howler are sheltering in the lee rocks from the same storm, and the player walks into them. Fought in near-white: the howler's howl is the telegraph (§7). They break off when hurt (wolves flee at 30%; they are animals, not humans).
5. **The Last Rise (C6) to W4.** Dorn's Gather is close, steady, and the white thins as the cut walls rise. The player walks out of the white onto the near apron.

**No failure:** there is no timer on the climb. Wandering only means the next Gather comes again. If the player has not progressed toward the current post for 45 s, that post's warden blows Gather twice in a row and then the glyph stays pinned for 5 s (`TSW-B1.7`, assist). Death (wolves, a knockdown at low health) respawns the player at the last post reached.

**Fallback if `TH_CALLS` is false** (should not occur after TF-M1): W1's warden teaches Gather and Fall in two lines at the foot of the stair (`TSW-B1.0`), and glyphs display from then on.

**Verbs:** listen, climb, shelter, count.

### Beat 2 — The Galleries (`S02_galleries`)
**Objective:** *Stop the gallery crews.* (Sub-objectives: *Listen for the gallery call.* / *Find the gallery with that glyph.*)
At W4, **Dorn** (`TSW-D3`) points up at the cut. The player can see again. Seven galleries, seven marker stones at their feet. From the gatehouse roof a hornman is blowing **the old sealing order**: the **Close** call (two long, falling) followed by a short **tag** of shorts and longs. Dorn knows the shape even if he never blew it: "Close, then the tag. Every gallery has its own tag. It's cut on its stone."

**The gallery calls** [NEW]. Every sealing call is Close followed by a tag. The tag is cut on the gallery's marker stone under two falling bars:

| Gallery | Tag | Marker glyph | State |
|---|---|---|---|
| G1 | one short | ⟍⟍ • | spent (grey props) |
| G2 | two short | ⟍⟍ • • | spent (grey props) |
| **G3 the Shoulder** | one long | ⟍⟍ — | **live (pale props)** |
| G4 | short-long | ⟍⟍ • — | spent (grey props) |
| **G5 the Lintel** | long-short | ⟍⟍ — • | **live (pale props)** |
| G6 | long-long | ⟍⟍ — — | spent (grey props) |
| **G7 the Gate gallery** | long-long-short | ⟍⟍ — — • | **live (pale props), above the gatehouse** |

Tags never use three shorts (Gather) or short-long-short (Fall), so no gallery call can be mistaken for an Ordinary Call. (Text note for audio: Close's two long falling notes lead every tag, so a sealing call is always longer than any Ordinary Call.)

**How it plays:**
1. The hornman calls the old order from the **drill board** (G1, G2, G3 … G7). He waits between calls for the crews' **Answer** (two short = "ready"). The crews at live galleries answer; nobody answers from a spent gallery, and the hornman moves on after a count. Ingrith runs it by the board: "We do it by the board." (`TSW-B3.1`).
2. When a call sounds, its glyph appears at the screen edge pointing to the gatehouse roof (the source), not to the gallery. The player must **match the tag to a marker stone**. Inspecting a marker shows its glyph large. Grey props and an old heap below mean **spent**: nothing behind the props, nothing can fall. Pale props and a taut pull-line mean **live**.
3. **The crews pull only in a lull.** A live gallery's crew hauls slack on the pull-line between gusts, so the stone falls true; the fluted wall's whistle stops them. Their haul is shown by the pull-line visibly tightening in stages. **The haul advances only while the player is inside the gallery zone** (fiction: the gust pattern; implementation: the stages are paced to the player). A crew never completes a pull before the player arrives.
4. At each live gallery the player chooses:
   - **Drive off the wedge crew** (fight, **TSW-E2/E3**; crew yield), or
   - **Cut the pull-line** from the ledge below the pin-beam: reach the ledge (cut stair, or agility scramble), then a 3 s channelled cut, interrupted by damage, while the crew throws stones and shouts. Cutting the line ends the haul; the crew gives up and sits down (yields without a fight; `TSW-B3.8`). This is the quieter route and the faster one for a careful player.
5. **Wrong guesses** (walking to a spent gallery) cost only walking time. Dorn's bark tells the player once: "Grey. Nothing behind it. Let him call." (`TSW-D3.30`). Spent galleries' calls get no Answer, which is itself a clue the player can learn.
6. **Order:** G1 and G2 (spent; teach the glyph match), **G3** (live), G4 (spent), **G5** (live), G6 (spent). The hornman repeats a live gallery's call until it is dealt with. After G6 he calls **G7**: and this time the answer comes from the gatehouse roof itself. **Ingrith has drawn G7's pins herself.** The Gate gallery groans and sheds its first stone onto the far apron. Dorn blows **Fall** from the near apron. The step completes.

**Strength by `TH_STORES`:**

| Value | G3 | G5 |
|---|---|---|
| reported | wedge crew of 3 | wedge crew of 3 |
| seized | wedge crew of 3 | **unmanned**: the crew went home hungry (bark from a crewman at G3: "Half of them walked. No grain, no wall."); the player only cuts the line |
| leverage | wedge crew of 3, new ridge-iron spearheads (stronger) | wedge crew of 4 with new spearheads |

**Discovery tie (TDS10):** with the TDS10 discovery flag, the first time the player sees the galleries from the apron, the bark *"Three pale. Same as from below."* plays (`TSW-B2.1`) and each live marker shows a small tick when inspected.

**Optional inspects:** grey prop fallen across the cut floor; a war heap with the frozen wagon axle; the pull-line (pale new rope, Whinstone stencil on the coil end if `TH_STORES` ≠ seized: *"New rope. The coil end's stamped 'W.'"*).

**Verbs:** listen, read, choose, climb, fight or cut.

### Beat 3 — The Warden Room (`S03_gatehouse`) — *the strange moment*
**Objective:** *Get up to the winch.* → *Shelter.* → *Read the wall.* → *Take a rubbing.*
The player crosses the cut floor toward the gatehouse. G7 sheds again. Dorn blows **Fall**; the fluted parapet whistles at the same moment, and the hard wind sits down on the cut. The only cover in reach is the gatehouse's warden room door (H1). The player goes in. The wind keeps the cut closed **as long as the player is inside and the rubbing is not taken** (a forced shelter; the objective says *Shelter. Wait for Rest.*).

Inside: the splinter's three-night camp. The fire is still banked high. On the wall behind it the plaster has come away in plates, and where it has gone the soot is cut through by letters. The presentation is in §8.2.

1. **Read the wall (required).** Three panels, left to right. Each needs a short **wipe** interaction (2 s, with the crew's rag from the cookpot) to clear soot from the cut letters; each then gives its inspect text and the full roster section for that panel (dialogue file Document D-1). Panel 1: the first closings. Panel 2: the final year, including the long-winter dates and the **turn-back lines**. Panel 3: the last closings and the last line. **Weatherall** is on panel 2. Sets `TSW_ROSTER_READ` after the third panel.
2. **Take a rubbing (required).** The player takes a sheet from Ingrith's stack of count sheets on the desk (the figures face down; the blank back is the paper) and a stick of charcoal from the hearth's edge (carry state), and rubs the three panels in turn (3 × 3 s channels; each completed panel persists). On completion: **`TSW_closure_rubbing`** (quest item). Its inspect text notes the count-sheet figures showing through from the back (dialogue file Document D-2).
3. When the rubbing is finished, the wind lifts. Dorn blows **Rest** outside (`TSW-B3.12`). The objective returns: *Get up to the winch.*

**Optional:** the **drill board** (the wartime sealing order; *"The galleries in order, one glyph to a line. Someone's added a new line at the bottom in fresh chalk: G7 — Q."*); the empty slate shelf (*"A shelf for slates. No slates. Whatever the gate-warden wrote on, it wasn't kept."*); the crew's bedrolls (*"Six bedrolls. One has a child's mitten tucked into the blanket fold. Nobody here is a child."*).

**Verbs:** shelter, wipe, read, rub.

### Beat 4 — The Quartermaster (`S04_ingrith`) `[SPLINTER]`
**Objective:** *Stop the Quartermaster at the winch.*
Up the stair (H2) to the winch floor (H3). **Ingrith Scarrow** `[SPLINTER]` stands at the winch drum with a ridge-iron spear, the knocked-out pawl at her feet and her hornman at the parapet. The slab hangs half down in its slot. She is counting under her breath. She sees the player and finishes the count before she speaks (`TSW-D4`). She does not monologue: three short lines, one of them a number.

Boss fight, **TSW-E4** (§7.1). She fights with a spear and with the gate: on her hornman's Close she lets the drum slip and the slab drops a notch, a telegraphed hazard along the slot. In phase 2 two crew come up the outer stair (three with `TH_STORES = leverage`). At about **20%** she **yields**: she plants the spear butt-down, sits on the drum frame and stops counting (`TSW-D5`).

**The yield scene** (`TSW-D5`) is short and can be left at any line. She asks how many small ones are with the column. She says the sentence the bible gives her: *"They're clanless. They know the cold."* The player may set the roster against her (an option, never required): she has not read the wall. She asks one question about the turn-back lines and does not get an answer she can bear, so she goes back to counting. Nothing she says is evidence; it is a person, beaten, at a winch. Her `TH_HORN` line plays here. Two wardens come up the stair with Dorn and take her and the hornman down to the warden room (they stay held through the night; they are walked to Stonewake at dawn).

**Verbs:** fight; listen.

### Beat 5 — Wind the Slab (`S05_wind`)
**Objective:** *Wind the gate-slab up.*
The pawl is out; the slab will not hold itself. The player takes the winch: a **channelled interaction in three segments** (each 6 s). **Damage or a gust interrupts the current segment; completed segments are kept** (Lowmark convention). The slab rises by visible degrees; through the widening gap the far apron and the column's lanterns come into view (§8.3).

Between and during segments (**TSW-E5**, hazards only; no enemies):
- **Gusts:** the fluted parapet whistles (~2.5 s). A player who stops channelling under the drum hood is safe; one who keeps channelling in the open is interrupted (segment progress lost, completed segments kept).
- **G7 sheds:** Dorn, now on the near apron below, blows **Fall**. Stone comes off the Gate gallery onto the far apron and the open edge of the winch floor (marked circles of grit fall first, ~2 s). The hood covers the drum.

After segment 3 the slab is up. A Hushfold herd-lad (Kolli, who came up with Dorn) jams a **gallery wedge** into the pawl seat at Dorn's call; it holds the drum **only while someone leans on the bar** (fiction: the wedge is the wrong size). The objective changes.

**Verbs:** wind, endure.

### Beat 6 — Hold the Gate (`S06_hold`)
**Objective:** *Hold the winch while the column comes through.*
A sustained **hold** interaction on the winch bar. While it is held, the column moves: Hushfold's people, the herd and the wood sledges come off the far apron, under the slab and in. Releasing the bar at any time does **not** drop the slab (the wedge catches it); the column simply **stops and waits in the lee** until the player leans on the bar again (fiction: Runa will not send people under a slab nobody is holding). Gusts and G7 sheds continue on a slower rhythm; the player can let go to shelter under the hood and take the bar again.

**Runa's tally (required beat; second custodian).** Runa Weatherall stands in the gate below the winch floor with **Hushfold's first tally book** open on her arm, counting her people in by touch on the shoulder. As they come in she reads from the book, the way every host reads a tally on first snow (TME01), because this is the first snow and this is the first time the whole shelter line has come through one gate together. She reads the book's first page aloud, from the beginning (`TSW-D6`; full text in dialogue file Document D-3). Its entry: *"Weatherall, Astrid, and two small. Came over in the thaw."*, dated the thaw after the long winter of the final year, a thaw after the roster's date for the same name. The player, holding the bar, hears it. If the player has inspected panel 2 (always true: it is required in `S03`), a quiet interaction-log line appears: *"Weatherall. The wall downstairs has that name, the winter before."* No NPC draws the link. The step completes when the column is through **and** `TSW-D6` has finished. The hold presentation is paced so the reading ends as the last sledge passes under the slab (~75–90 s of holding).

Runa's count ends two short: *"Twenty-nine."* (`TSW-D6.20`).

**Verbs:** hold, listen.

### Beat 7 — Lost (`S07_stragglers`)
**Objective:** *Answer the Lost call.* (then optional: *Bring them in.*)
From beyond the far apron, faint in the white, comes **Lost** (one long, rising; rising-line glyph): two herders who went back for strayed goats, **Oddny** and old **Halvard** [NEW], one call from each, from two directions.

**The reply.** Dorn sets fresh wedges and the slab holds by itself now. The player goes down to the far apron.
- **With `TH_THIRD_HORN`:** the player blows **the Third Horn** (Answer + one long rising) from the far apron, the call restored in *The Third Horn*: "heard; someone is still out." The gate hears it as well as the stragglers. Dorn lowers his horn and does not blow (`TSW-D7.02`). Runa's people stop moving inside the gate and turn round. From then on, both stragglers **answer** every call the player blows with Answer, which makes them easier to find.
- **Without it:** Dorn blows **Answer** from the gate (`TSW-D7.01`). The stragglers keep blowing Lost on a slow cycle.

**The search (optional, encouraged).** Beyond the far apron is the whiteout again (§8.1 rules). The player follows each straggler's call:
- **Oddny** (nearer): sheltering under a boulder with three goats. Echo count off the boulder says when she is close. She takes the player's **rope line** (carry state: the player tows her and the goats back at walking pace).
- **Halvard** (further, toward the far hut): sitting down on the track with a turned ankle. He takes the rope line once Oddny is in.
The player can bring in one, both, or neither. Gusts and whistles apply; there are no enemies.

**Ending the step.** The step ends when either:
- both stragglers are inside the gate (**`TH_COLUMN = player_brought`**), or
- the player talks to Dorn or Runa at the gate and says to leave it to the patrol (`TSW-D7.30`): Vessa's patrol is out there and the far hut is on their way. (**`TH_COLUMN = patrol_brought`**; any straggler not yet brought in waits at the far hut and comes in with the patrol at dawn.)

If the player has brought in one and returns, Dorn offers both options again. **Nobody is ever lost**: a straggler the player does not reach is safe at the far hut and is seen alive at dawn.

**Verbs:** answer, search, tow, choose.

### Beat 8 — Dawn at the Gatefall (`S08_dawn`)
**Objective:** *Wait for the patrol.*
A **keep-watch** interaction at the warden-room hearth (Lowmark convention: per-player presentation hour; cancellable; never world time). Hushfold's people are bedded in the warden room and the gatehouse passage. The roster wall is in firelight behind them. Two steps of watch, then grey light, and the storm breaks.

**Vessa Galt's patrol** comes in through the gate at dawn, white with snow, with the stragglers the player did not bring (if any) (`TSW-D8`). Vessa looks at the wall for a long time. With `TPW_NAMES_ASKED` she says what she says (`TSW-D8.10`). Ressa arrives from below with more wardens. The slab is left **up and wedged, with wardens on it**: nobody seals anything until the Assembly sits. Ingrith and the hornman are walked down to Stonewake to be held. Ressa: "Assembly sits tomorrow. Bring the paper." (`TSW-D8.30`).

**Verbs:** wait, witness.

### Beat 9 — The Hall (`S09_assembly`)
**Objective:** *Go to the Assembly Hall at Stonewake.*
Travel is ordinary. The storm is over; Stonewake is under snow. The hall is full. **Hadrik Stonewake** is placing people (§8.4), as he always does, moving from group to group with a hand on an elbow, a word, a nod toward a place on the floor. Who stands near the speaking stone and who stands at the wall is driven by the player's earlier flags (§8.4 table). The player sees the hall settle before anything is said. Ingrith stands at the side door between two wardens `[SPLINTER]`.

Hadrik comes to the player last (`TSW-D9`).

### Beat 10 — Where Will You Stand (`S10_stand`)
**Objective:** *Choose where to stand.*
Hadrik asks the player where they will stand. He does not suggest. The player walks to one of four places (a physical choice: walk to it and confirm; the four places are marked by the people there) (§9.3):
- **With Hushfold** (`TH_STAND = hushfold`): beside Runa, at the door side.
- **At the wardens' rail** (`= wardens`): beside Ressa and Vessa.
- **By the cairn bench** (`= cairn`): beside Maera.
- **At the Blood-Oath table** (`= brynjar`): beside Brynjar.
One line greets the player at each place (`TSW-D9.20`–`.24`).

### Beat 11 — The Reading (`S11_reading`)
**Objective:** *Listen.*
Hadrik puts the reader on **the carrying spot** (A3). The reader is **Runa** if `TH_STAND = hushfold` or `TH_HUSHFOLD_VOICE`; otherwise **Maera** (`TSW_READER`). The player hands over the rubbing (one interaction; it comes back afterward). The rubbing is read aloud **once** (`TSW-D9.40` onward): every date, every name, every turn-back line. The hall carries the reader's voice to every wall. Nobody interrupts. There is no hearing, no question, no proof laid.

Then the hall decides **by where it stands**: Hadrik says "Stand where you mean it," and people move, a few steps each, toward the speaking stone or away (§8.4). The movement is the posture. The **posture** is computed (§9.3) and `TH_ASSEMBLY_POSTURE` is set. A short exchange of clan voices follows (one line each; posture variants), and Ingrith says one thing `[SPLINTER]` (`TSW-D9.70`).

### Beat 12 — The Account (`S12_close`)
**Objective:** *Hear the Assembly's word.*
Hadrik repeats what the hall has said; he says that is all a speaker does (`TSW-D9.80`). Three things are said in every outcome:
1. The posture for the winter (watchful / open / sealed with terms; §9.3 consequences).
2. **Ingrith Scarrow goes to her clan's tribunal** `[SPLINTER]`. The Assembly does not judge her; her clan does, with the Assembly watching.
3. **The closure account**: from today, any closing in Thornfell names who is outside. Ressa writes the first entry on a new slate, for the Gatefall itself (posture variant), and hands the chalk to whoever the posture says keeps the account.
Hadrik gives the rubbing back to the player: "The wall has the cut one. Keep that." **`TH_STANDING`** is set. The quest completes on `TSW-D9.90`.

**Verbs:** stand, listen, keep.

## 7. Encounters

Tuned for **Advanced identity, Milestone 3 equipment** (bible TD-12). Exact levels and numbers are Gameplay Designer calls; the targets below are intent.

| Id | Enemies (bible §10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TSW-E1** | 2 × ridge wolf runner, 1 × howler | Lee rocks below W3 (C5), in near-white (visibility ~3 m) | Runners circle at the edge of sight; howler hangs back and calls | **Howl:** the howler's rising howl (~1.5 s, positional; glyph-free but captioned "a howl, left") precedes a runner lunge from that side. **Lunge:** runner drops low with a snarl (~0.8 s). | A fight by ear; proves the sound rules work for danger too | 40–60 s; 65–85% HP remaining. Wolves flee at 30% (animal behaviour, not yield) |
| **TSW-E2** | G3 wedge crew: 2 × Iron Winter spear, 1 × hornman | G3 pull ledge | Spears hold the ledge stair; hornman stays by the line and buffs | **Spear lunge:** set feet, lower spear (~1.0 s), long straight thrust. **Hornman Gather:** raises horn (~1.2 s), three short; allies within 8 m attack faster for 8 s. Interrupt by hitting him during the raise. | Readable crew fight with a sound telegraph | 50–70 s; 60–80% HP. Skipped entirely if the line is cut |
| **TSW-E3** | G5 wedge crew: as E2 (`reported`); unmanned (`seized`); 3 × spear + 1 × hornman with new spearheads (`leverage`) | G5 pull ledge | As E2 | As E2; with `leverage`, **new spearheads** add a short bleed to the lunge (visible bright iron) | `TH_STORES` made physical | 50–90 s by value; skipped if the line is cut |
| **TSW-E4** | **Ingrith Scarrow** `[SPLINTER]` (boss), 1 × hornman; phase 2 adds 2 × spear (3 with `leverage`) | Winch floor (H3) | Boss spec §7.1 | §7.1 | Act III boss (bible §10: 1 Act III boss) | 5–7 minutes |
| **TSW-E5** | Hazards only: gusts, G7 sheds | Winch floor, far apron | — | Whistle (~2.5 s); Fall call + grit circles (~2 s) | Labour under weather | Winding and holding ~3–4 minutes total |

**Rules**
- **Combat never reveals evidence.** The roster and Runa's tally are a wall and a book. Ingrith's lines after she yields are a person speaking, not proof; the closure account rests on the wall and the book.
- **Defeated humans yield** (TD-7): they go down to one knee, drop their spears and sit where they are; the wardens bind them later (prop). Nobody dies. Wolves flee.
- **No resonance at the Gatefall** (bible §2.4, TD-8). No echo-figures, no surges, no hum. The only dangers are wind, loose stone, white and people.
- **Death:** respawn at the last checkpoint reached: Three Calls (C1) → each warden post W1–W4 → the near apron (G0) → the warden room (H1). Completed gallery steps stay completed. The rubbing persists. Winch segments persist. A beaten player is never sent back past a completed step.
- **Co-op:** shared crews and wolves for partners on the same step; health scales per participant. Each partner's galleries, roster, winch and column are presented per player from their own step state (fallback: the host's state, all present credited). The rubbing is created per player (each partner takes their own).

### 7.1 Boss spec: Ingrith Scarrow, the Quartermaster `[SPLINTER]`

**What she is (author truth):** a former pass quartermaster, a child in the final year's long winter, who has counted every measure in the Iron Winter and believes every number. She fights like someone who drilled crews: economical, on a count, using the gate as a weapon because it is the thing she knows best. **She is not a monster.** She never threatens the column, and she stops when she is beaten.

**What the player sees:** a broad, weathered woman in a quartermaster's quilted coat with tally cords at the belt, a ridge-iron spear, her lips moving as she counts.

#### 7.1.1 Arena

| Element | Spec |
|---|---|
| Shape | Rectangular timber floor ~18 × 10 m over the cut. |
| The drum hood | A roofed section (~6 × 4 m) over the winch drum on the near side: cover from G7's stone and from gusts. |
| The slab slot | A 2 m strip across the far side of the floor where the slab hangs. Standing in it is dangerous when the slab drops a notch. |
| The parapet | The hornman's post on the far corner; a fluted parapet stone (the whistle) on the open side. |
| Stairs | The inner stair (from the warden room; the player's entry) and the outer stair (phase-2 crew entry). |
| Edges | Railed. No fall is possible. |

#### 7.1.2 Mechanics

| Ability | Telegraph (readable, non-twitch) | Effect | Counter |
|---|---|---|---|
| **The Count** | She says "One." "Two." "Three." aloud, one number per ~0.8 s, stepping forward on each (captioned). | A three-thrust spear combo: one thrust on each number after it is spoken. Moderate damage each. | Step aside on each number, or after "Two" step out of her line; a block takes reduced damage. |
| **Short Measure** [NEW name, internal only] | She says "Short." and reverses the spear (~1.0 s). | A butt-stroke that knocks the player back 2 m and briefly staggers. | Step back or sideways. |
| **The Close** | Her hornman blows **Close** (two long, falling; ~2.0 s total). On the second falling note she kicks the drum brake. | The slab drops a notch with a crash: heavy damage and knockdown to anyone **in the slab slot**. Dust falls first along the slot (visible strip). | Be out of the slot strip by the second note. Interrupting the hornman during his raise (~1.2 s) cancels it. |
| **The Gust** | The fluted parapet whistles (~2.5 s). She steps behind the drum hood's post. | A gust crosses the open floor: players in the open are pushed 2 m toward the inner wall and slowed 3 s. She lunges at a slowed player. | Get under the hood with her (she then cannot use the lunge) or brace against the rail (stand still facing the wind). |
| **Gate gallery shed** (phase 2–3) | Dorn's **Fall** from below (positional), then grit circles on the open floor (~2 s). | Falling stone in the circles: moderate damage. Hits her too. | Under the hood or out of the circles. |

#### 7.1.3 Phases

| Phase | Health | Pattern | Transition |
|---|---|---|---|
| **P1, the Count** | 100–60% | The Count, Short Measure, The Close every ~20 s. Gusts every ~25 s. | At 60% she steps back to the drum: "Gather." Her hornman blows Gather; two crew come up the outer stair (three with `leverage`). |
| **P2, the Crew** | 60–35% | Crew spears press; hornman buffs (Gather) and calls The Close every ~15 s. Gate gallery sheds start. | When the crew have yielded (or at 35% if they are left), she drops her tally cords (a visible clatter) and stops speaking aloud. |
| **P3, Silent** | 35–20% | She no longer counts aloud: **The Count** is now telegraphed only by her steps and a raised spear for each number (each still ~0.8 s, still three). The hornman calls The Close every ~12 s. The player has learned the rhythm; now they must read it with their eyes. | At ~20% she **yields** (below). |

#### 7.1.4 Tuning, yield, death, co-op

| Item | Target |
|---|---|
| Solo duration | 5–7 minutes for an Advanced-identity player with cooked food. |
| Solo end state | A player who moves on the count and keeps out of the slot ends at 30–60% HP. No single hit above 30% max HP except The Close in the slot (~35%). |
| **Yield** | At ~20% health (the fight ends on reaching the threshold; she is not damaged further), she plants her spear butt-down, sits on the drum frame and stops counting. The hornman puts his horn down on the boards. Any crew still standing sit down. `TSW-D5` opens. No loot. Nothing evidentiary. |
| Death | Respawn in the warden room (H1). The fight resets to the **top of the phase the player died in** (100 / 60 / 35%). Yielded crew stay yielded. |
| Logout | `S04` persists; the fight restarts at 100% on re-entry. |
| Co-op | Shared boss for partners on `S04`. Health scales per participant. The Count targets one player at a time in rotation. Each partner sees their own yield scene (per player); fallback: shared scene, every partner given the options. |
| Splinter swap | If TD-1 is replaced, the boss's name, coat and lines swap; the mechanics (count, gate, gust) are built on "a quartermaster who knows the gate" and survive any replacement that is still an independent Thornfell faction. |

## 8. The discovery moments: presentation specs

### 8.1 The whiteout (Beat 1; reused in Beat 7)

| Time / element | Spec |
|---|---|
| 0–8 s above C1 | Snow density ramps up; the far edges of the screen go white first, then the middle. Terrain beyond ~3 m fades to a white field; the player character and anything within arm's length stay readable (soft contrast outline on the rope rail and the red rags). No full-screen overlay that hides the character. |
| Audio priority | Wind bed ducked under all horn calls (−6 dB while a call plays). Horn calls are the loudest positional source in the zone. Footsteps on snow stay audible. |
| Glyphs | Each call heard shows its call-shape glyph (bible §9.4) at the screen edge in the direction of the source, for 3 s. An echo's glyph is dimmer and later. Echo-count ticks sit beside the player's own Answer glyph. A caption line ("Gather, ahead left") is available for players without audio. |
| Rope boundaries | Walking into a rope plays a rope creak and `TSW-B1.2`. The rope cannot be crossed. |
| Shelter niches | A niche's red rag flutters harder before a gust (a second visual tell beside the whistle). |
| What it means | The player walks a mountain blind and is never lost, because people are blowing horns for them. That is the Thornfell they are about to ask to keep doing that for others. |

### 8.2 The roster under the soot (Beat 3)

The bible's strange moment: *names cut into the gatehouse wall under the soot, beside dates.* Nothing here is supernatural. The unease is human.

| Time | Element | Spec |
|---|---|---|
| Entry | **The room** | Firelight, heat after the storm, the crew's things. The wind outside goes to a roar against the door, then a steady, shut-in hum. The player's breath stops steaming. |
| First look | **The wall** | Behind the hearth, plaster has come away in plates (some lie broken on the hearthstone). Where it has gone, the soot is not flat: there are **lines** in it, thin and regular, the way cut letters hold soot differently. A prompt: *Wipe the soot.* |
| Wipe 1 (2 s) | **The first panel** | The rag drags; cut letters come up pale under black, a date first, then a column of names under it. The fire pops. The player's camera stays free. |
| After each wipe | **The reading** | The inspect text and the panel's roster text show in the reading panel (dialogue file Document D-1). Ambient: the hearth, the wind hum, once (panel 2) the wind dropping for a breath so the room is very quiet while the turn-back lines are read. That drop is the only "event". |
| Panel 2 | **Weatherall** | The name is cut like every other name. No highlight. The interaction log does not comment. |
| Rubbing | **The paper** | Ingrith's count sheets: rows of figures on one side. The player turns a sheet over and rubs. The cut letters come up black on the blank back; the figures show faintly through from the other side. |
| End | **Rest** | When the third panel is rubbed, the wind outside eases. Dorn's **Rest** comes through the door. |
| UI | Objectives suppressed during the wipes; restored at the rubbing prompt. |

### 8.3 The column comes through (Beats 5–6)

| Element | Spec |
|---|---|
| The gap | As the slab rises, the far apron's lanterns appear in the gap first, low, then people's legs, then people. They have been waiting in the lee, in a tight knot round the herd. |
| The movement | Hushfold comes through in tally order (households in the order the book reads), not in a rush: adults with sledges, then the herd driven by two older children, then the old. Each touches Runa's arm or is touched on the shoulder as they pass. |
| Runa | Below the winch floor, in the gate, the book open on her arm. She reads without looking at the page for most of it (she knows the first page). She looks down for the Weatherall line. |
| Audio | Wind, goat bells, sledge runners, Runa's voice carrying up through the open floor. No music until the last sledge is under the slab; then a single low drone from a hand-horn Kolli blows badly, which makes someone laugh. |
| G7 | Sheds once during the hold (Fall from Dorn; the column waits; the player can keep holding under the hood). Nobody is hurt. |
| Count | Runa's "Twenty-nine." The two missing are named by a woman in the column: "Oddny went back for the brown nanny. Halvard went after Oddny." |

### 8.4 The hall (Beats 9–11)

**Placement.** Hadrik places people before he speaks. Each group's spot on the floor is set by flags. "Near" means within the near ring around the speaking stone (voices carry); "wall" means at the outer wall (voices fall flat).

| Who | Near the stone if… | Otherwise | Notes |
|---|---|---|---|
| **Runa and Hushfold** | `TH_HUSHFOLD_VOICE` | Door wall, where the clanless have always stood | With `TH_COLUMN = player_brought`, Oddny and Halvard stand at the front of Hushfold's group. With `patrol_brought`, they stand with Vessa. |
| **Ketil, Tova and Nettlehook** | `TH_HIGHSTEADS_TOGETHER` (beside Hushfold, wherever Hushfold stands) | Hearthguard side, apart from Hushfold | `TH_PASSWATCH_ROUTE = sledge`: Ketil stands at Hushfold's shoulder in either case ("the highstead eats"; `TSW-B9.3`). `caravan`: Stonewake ridge-market traders stand behind the Blood-Oath table. `split`: no change. |
| **Maera Cairnwatch** | `TH_SHATTERFALL_ACCOUNT` = amended or beside | Cairn bench at the wall (`kept`) | Maera never stands on the carrying spot unless she is the reader. |
| **Brynjar Korr** | Always at the Blood-Oath table (near ring) | — | `disowned`: Hadrik turns the table so Brynjar faces Hushfold across the stone. `defended`: Brynjar stands with his back to the door and does not turn. On the public route Hadrik read the ledger's totals only (TF-M2 `TIW-D8.10`–`.11`), so no TF-M5 line has Hadrik or a defended Brynjar mention the Nettlehook children's-ration line. |
| **Old Torvek** | `TH_BANNER = shared`: alone at the foot of the speaking stone, the banner folded on the stone | `blood-oath`: at Brynjar's shoulder. `hearthguard`: at Elira's shoulder. Not done: at the wall by the cairn bench. | Torvek never moves when the hall moves. |
| **Elira Hearthward** | Always on the near ring, Hearthguard side | — | `TH_STORES = seized`: her storekeepers stand beside Hushfold (they fed them). |
| **Ressa Highcrag, Vessa Galt** | Wardens' rail (near ring) | — | Vessa holds her slate. |
| **Dorn Feldhorn** | Door, horn on his hip (always) | — | |
| **Kaldren Deepdelver** | Back wall, `TH_HORN = silenced` only | Absent ("doesn't come down for talking") | One line at most, about stresses (§15). |
| **Ingrith Scarrow** `[SPLINTER]` | Side door, standing, two wardens | — | |
| **Tessaly Varn's crew** (TAS Completed) | Back wall, together | Absent | One bark; not a placement factor. |

**The movement.** After the reading, Hadrik says "Stand where you mean it." Each group steps a few paces toward the stone (toward open) or holds or steps back (toward sealed), in the pattern of the posture. Presentation only; the posture is computed first (§9.3) and the movement plays it.

| Posture | What the hall does |
|---|---|
| **open** | Hushfold steps in from the door wall to the near ring (if not already there); Nettlehook goes with them; Elira steps toward them; Brynjar does not move, then moves one step. The near ring is crowded. |
| **watchful** | Small movements both ways. The wardens' rail stays where it is and the floor settles around it. |
| **sealed_with_terms** | The Blood-Oath table holds; the near ring thins toward the door; Hushfold stays where it is. Ressa steps forward alone to the stone (she writes the terms). |

**The carrying spot.** The reader stands on A3. Her voice comes back from every wall at the same strength. Hadrik stands one step off it. This is the only time in the quest the hall's acoustics are shown, and nobody remarks on them.

### 8.5 The strange moment, summarised

The bible's strange moment is the roster: names under soot. TF-M5 has no phenomenon. Its wonder is the climb (being guided blind by people) and its unease is the wall. The Third Horn, if restored, is the only call in the quest that has not been blown at a Thornfell gate since the war; nothing supernatural answers it, but the whole gate turns round to hear it.

## 9. Quest structure for implementation

### 9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_gather` | Answer the Gather at Three Calls Shelter. | Enter C1 volume + `TSW-D1` end | Yes | Quest Active on entering Windscar Pass or Stonewake after TF-M4 Completed (server event `tsw.blizzard_start`, per player). Loaned horn granted here only if the player lacks the TF-M1 practice horn (fallback). |
| `S01_whiteout` | Climb to the Gatefall by the wardens' horns. | Enter G0 (near apron) volume | Yes | Checkpoints at W1, W2, W3, W4. `TSW-D2` at W3 (Iven) is required (short; gates the wolves' zone and the Fork's echo lesson). TSW-E1 must be resolved (wolves flee) to leave W3's zone. Assist re-call after 45 s without progress. |
| `S02_galleries` | Stop the gallery crews. | G3 and G5 each resolved (`fought` or `cut`), then G7 call and shed event | Yes | Hornman call sequence G1→G7; live calls repeat until resolved. With `TH_STORES = seized`, G5 is resolved by cutting only. Sets `TSW_G3`, `TSW_G5`. |
| `S03_gatehouse` | Get up to the winch. / Shelter. / Read the wall. / Take a rubbing. | 3 × `wipe_panel` + 3 × `rub_panel` complete → `TSW_closure_rubbing` acquired | Yes | Forced shelter: the cut stays in a gust until the rubbing is acquired. Wipes and rubs persist individually. Sets `TSW_ROSTER_READ`. |
| `S04_ingrith` | Stop the Quartermaster at the winch. | TSW-E4 reaches yield threshold + `TSW-D5` end | Yes | `[SPLINTER]`. Phase checkpoints. `TSW-D5` can be exited at any line (exit counts as end). |
| `S05_wind` | Wind the gate-slab up. | 3 × `wind_slab` segments complete | Yes | Completed segments persist. TSW-E5 hazards. |
| `S06_hold` | Hold the winch while the column comes through. | Column passage complete **and** `TSW-D6` complete | Yes | Hold interaction; release pauses column. `TSW-D6` is the second-custodian beat. |
| `S07_stragglers` | Answer the Lost call. | Both stragglers inside the gate **or** `TSW-D7.30` "leave it to the patrol" | Yes | Reply blown on reaching F1 (player Third Horn with `TH_THIRD_HORN`; otherwise Dorn's Answer). Sets `TSW_ODDNY`, `TSW_HALVARD`, then `TH_COLUMN`. |
| `S08_dawn` | Wait for the patrol. | Keep watch × 2 at H1 + `TSW-D8` end | Yes | Cancellable watch. Patrol arrival brings unreached stragglers. |
| `S09_assembly` | Go to the Assembly Hall at Stonewake. | Enter A1 volume + placement presentation + `TSW-D9.01–.10` | Yes | Placement read from flags (§8.4). |
| `S10_stand` | Choose where to stand. | Player enters one of four standing-place volumes and confirms (`TSW-D9.20`–`.23`) | Yes | Sets `TH_STAND`. |
| `S11_reading` | Listen. | `TSW-D9.40`–`.62` (reading) end + posture computed + movement presentation + `TSW-D9.70` end | Yes | Sets `TSW_READER` (at reading start) and `TH_ASSEMBLY_POSTURE` (on computation). |
| `S12_close` | Hear the Assembly's word. | `TSW-D9.80`–`.90` end | Yes | Sets `TH_STANDING`; quest → Completed. Epilogue states apply (§E). |

### 9.2 Flags

| Flag | Values | Set by | Read by (here) | Read by (later) |
|---|---|---|---|---|
| `TSW_HORN_LOANED` | bool | `S00` (fallback only: the player lacks the TF-M1 practice horn) | `TSW-D9.90` (Ressa: "Keep the horn.") | Item pass (whether the loaned horn becomes the player's) |
| `TSW_G3`, `TSW_G5` | fought / cut | `S02` | Barks; Ingrith's crew line (`TSW-D5.12`) | — |
| `TSW_ROSTER_READ` | bool | `S03` (always set) | `TSW-D5` options; `TSW-D6.11` log line | Epilogue inspect at the Gatefall |
| `TSW_INGRITH_WALL` | bool | `TSW-D5.20` (player told Ingrith about the wall) | `TSW-D9.70` variant | Epilogue holding-room line (`TSW-L-INGRITH`) |
| `TSW_ODDNY`, `TSW_HALVARD` | player / patrol | `S07` | `TSW-D8`; Assembly placement | Hushfold epilogue barks |
| `TSW_READER` | runa / maera | `S11` start | Reading node variants | Hushfold / cairn epilogue line |
| `TSW_THAW` | bool | First re-entry to Thornfell after Completed, after the player has left the region once (§E.7) | — | Thaw presentation (§E.7) |
| `TH_COLUMN` | player_brought / patrol_brought | `S07` end | Assembly placement; posture; `TSW-D9` lines | Epilogue; convergence (bible §9.1) |
| `TH_STAND` | hushfold / wardens / cairn / brynjar | `S10` | Posture | Epilogue lines |
| `TH_ASSEMBLY_POSTURE` | watchful / open / sealed_with_terms | `S11` | `TSW-D9.70`–`.90` | Epilogue states (§E); convergence |
| `TH_STANDING` | bool | `S12` | — | Master commissions (§E.8); LR-M1; CV-M1 via `LR_STANDING` |

### 9.3 The posture (bible §9.3, implemented as written)

Hadrik places people; the player chooses only their own place. The posture is the Assembly's choice, read from who stands where.

1. Start at **watchful**. Count **open** points and **sealed** points.
2. **Toward open (+1 each):** `TH_STAND` = hushfold or cairn; `TH_HUSHFOLD_VOICE`; `TH_HIGHSTEADS_TOGETHER`; `TH_SHATTERFALL_ACCOUNT` = amended; `TH_BRYNJAR` = disowned; `TH_COLUMN` = player_brought; `TH_PASSWATCH_ROUTE` = sledge.
3. **Toward sealed (+1 each):** `TH_STAND` = brynjar; `TH_BRYNJAR` = defended; `TH_STORES` = leverage; `TH_BANNER` = blood-oath; `TH_SHATTERFALL_ACCOUNT` = kept.
4. **open − sealed ≥ 3 → open. ≤ −2 → sealed_with_terms. Otherwise watchful.**
5. `TH_STAND = wardens` adds nothing either way (the wardens keep the account whatever the hall decides). `TH_HORN`, and `TH_STORES` = reported or seized, change Assembly **lines only**. Every outcome adopts the closure account. None is wrong. Weights are tunable by the Gameplay Designer.

**Worked examples (for QA):**

| Player | Inputs | Open | Sealed | Result |
|---|---|---|---|---|
| Main line only, private Brynjar route, caravan, stands at the wardens' rail, brings both stragglers | disowned, player_brought, beside, reported | 2 | 0 | **watchful** |
| Same, stands with Hushfold | + hushfold | 3 | 0 | **open** |
| Public Brynjar route, kept the Shatterfall roster, stands with Brynjar, leaves stragglers to the patrol | defended, kept, brynjar, patrol_brought | 0 | 3 | **sealed_with_terms** |
| Full highstead series and Smoke Week, sledge, amended, stands at the cairn bench | voice, together, sledge, amended, cairn, disowned, player_brought | 7 | 0 | **open** |
| Leverage route (private), blood-oath banner, stands at the cairn bench | leverage, blood-oath, disowned, cairn | 2 | 2 | **watchful** |

**Note on leverage:** `TH_STORES = leverage` is available only on TF-M2's private route, which also sets `TH_BRYNJAR = disowned`, so leverage (+1 sealed) always arrives with disowned (+1 open). This is intended: keeping quiet to watch the splinter is a readiness choice that Brynjar's disowning balances.

### 9.4 Choices and consequences

**Choice A: each live gallery (local, no region flag)**

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Drive off the crew** (`fought`) | Crew yield on the ledge; the gallery stays rigged and is later re-wedged by wardens. | A fight; health and time. | Yielded crew are walked down at dawn; one says a line at the Assembly door (`TSW-B9.8`). |
| **Cut the pull-line** (`cut`) | The haul ends; the crew sit down without a fight. | The gallery can no longer be pulled from the ledge, so it stays live until wardens re-pin it; a short climb under stones thrown. | Ingrith: "Cut my lines. Rope's dear." (`TSW-D5.12`). Wardens grumble about re-rigging (`TSW-B9.9`). |

**Choice B: the stragglers (`TH_COLUMN`)**

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Search and bring both** (`player_brought`) | Oddny and Halvard come in on the player's rope line. Runa's count closes at thirty-one before dawn. | Time in the white; gusts. | +1 open. The two stand at the front of Hushfold in the hall. Hushfold barks name the player as "the one who went out". |
| **Leave it to the patrol** (`patrol_brought`), possibly after bringing one | The gate stays open and watched all night. At dawn Vessa's patrol brings the rest in from the far hut, cold and alive. | Hushfold waits the night with a count short. Vessa's line about the far hut is the uncomfortable echo of Ingrith's sentence. | No posture point. The two stand with Vessa in the hall. Nothing is lost. |

**Choice C: where the player stands (`TH_STAND`)**

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **With Hushfold** (`hushfold`) | Runa reads the rubbing (she reads it anyway if `TH_HUSHFOLD_VOICE`). +1 open. | Brynjar's people look at the door, not the player. One Blood-Oath bark cools afterward (`TSW-B10.4`). | Hushfold epilogue: the player's place at the Hushfold tally is kept. |
| **At the wardens' rail** (`wardens`) | Standing with the people who keep the account. No posture point. | The player adds no weight; the hall decides without them. Ressa: "Rail's for people who'll be out in it." | Ressa writes the first entry with the player beside her. |
| **By the cairn bench** (`cairn`) | Standing with the names. +1 open. Maera reads unless Runa does. | Maera's bench is at the wall unless she was placed near the stone: the player's own voice carries less there. | Maera keeps a copy of the rubbing at the name-stone wall (epilogue). |
| **At the Blood-Oath table** (`brynjar`) | Standing with readiness and with the man who would die for any child. +1 sealed. | Elira's look; one Hearthguard bark cools (`TSW-B10.5`). | Brynjar's epilogue lines toward the player warm; he volunteers his clan's towers for the relief line (sealed) or the thaw opening (open). |

**The posture (`TH_ASSEMBLY_POSTURE`), what each means for the winter**

| Posture | Passes | Closure account | Readiness | Cost |
|---|---|---|---|---|
| **open** | The far gate closes at deep snow in the ordinary way, with the wardens' rope route kept for need. At thaw the passes reopen by **shared opening**: Hushfold, the highsteads and any outside are called to the gate and witness it. | **Public.** Read on the Signal Terrace and posted at Passwatch; anyone may ask who is outside. | The Iron Winter reserve is counted out into the highstead granaries as a common winter store, publicly. | Brynjar's people call it "a gate with no lock". Passwatch's wardens carry more work (more names to keep, more people to answer). |
| **watchful** | The far gate closes at deep snow, kept by the Wardens; storm closings at Ressa's word. Reopens at thaw at the Wardens' word. | **Kept by the Wardens** on slates at each gate; read to anyone who asks a warden. | Readiness is kept **under Assembly account**: the reserve stays in store, counted, under seal, and nobody adds to it without the Assembly. | Nobody is fully satisfied. Hushfold's people still have to ask. |
| **sealed_with_terms** | The passes **stay shut until the thaw**, beginning now: the slab comes down this week, early and hard. | Kept, with the names of everyone known to be outside, and a **relief line** to them: a weekly rope-and-horn run from Passwatch to the far hut and the shielings, carrying food from the reserve. | Readiness kept in full; the reserve feeds the relief line first. | The far-side winterers are outside all winter. Hushfold's people who chose to winter at the shielings are named in the account and fed by rope, not let in. |

**Every outcome:** Ingrith goes to her clan's tribunal. The closure account is adopted. The Iron Winter as a splinter is ended (its leader held, its crews walked down, its store under Assembly account). `TH_STANDING` is set.

## 10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| `TH_STANDING` | Standing | Thornfell's regional standing: opens the master commission offers (§E.8), LR-M1 eligibility (with `LM_CIVIC_STANDING`), and the CV chain via `LR_STANDING`. |
| The Gatefall | Access | Revisitable site: the gatehouse (roster wall inspectable, rubbed or railed per posture), the galleries (re-wedged), the horn post on the near apron where the player can blow any Ordinary Call and get a true echo. |
| A place in Hushfold's tally | Standing (non-mechanical) | Runa adds the player to Hushfold's current tally as "expected" if not already added by TME01/TSM. From then on, Hushfold voices use the player's name (bible §5.3 rule 4). |
| The horn | Tool | If loaned (`TSW_HORN_LOANED`), Ressa tells the player to keep it ("warden's horn"; functional name; item pass decides) (`TSW-D9.90`). |
| Small payment | Currency | A Ridge Warden's due for "a night at the gate", paid by Vessa at Passwatch afterward (economy tuning). |
| Skill XP | Action only | Melee or Ranged. No lump quest XP. |
| Post-quest world | Story | Epilogue states (§E). |

## 11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Lost in the whiteout | Rope boundaries; the post re-calls; assist pin after 45 s. **No failure.** |
| Ignoring Fall | Knockdown and damage; never lethal at full health; get up and continue. |
| Wrong gallery | Walking time only. The live call repeats. |
| Gallery haul | Advances only with the player in the zone; never completes. |
| Leaving during the roster | Wipes and rubs persist individually. The forced shelter resumes on re-entry. |
| Death | Respawn at the last checkpoint (§7). Completed steps, wipes, rubs and winch segments persist. Boss resets to the top of the current phase. |
| Logout | Restore to the persisted step. Mid-whiteout: at the last post. Mid-boss: warden room, boss at 100%. Mid-hold: on the winch floor with the column waiting in the lee. Mid-search: at the far apron; stragglers where they were (a straggler on the player's rope is restored inside the gate). |
| Walking away | Quest stays Active at the persisted step. Resume hook: Ressa at Three Calls (`S00–S01`), Dorn at the near apron (`S02–S08`), Hadrik's runner at the Signal Terrace (`S09–S12`): "Hall's waiting. It's good at it." |
| The storm and the world | The blizzard is a per-player quest-local weather event. Other players in the zone see ordinary snow. After `S08` the storm is over for that player. |
| Fail state | None. |
| Co-op | §7 rules. Assembly: each partner chooses their own `TH_STAND` and gets their own posture from their own flags (per-player presentation); fallback: the host's hall arrangement is shown, each partner's own posture is stored and reflected in their epilogue. Each partner holds their own rubbing. |

## 12. Integration needs

Documented dependencies for a later Systems Engineer. None is implemented here.

| Need | Owner | Minimum viable form |
|---|---|---|
| **Per-player blizzard / whiteout** | Systems + art | Quest-local weather state with a visibility clamp (~3 m) and a readable character outline. Fallback: heavy fog volume with the same clamp. |
| **Positional horn calls with call-shape glyphs** | Audio + UI | Call events with source position; screen-edge glyph in source direction; dimmer delayed glyph for echoes; caption line. Reused from TF-M1's call system (Act I §A12). |
| **Player horn call wheel** | Systems + UI | Blow any Ordinary Call (Rest, Close, Gather, Fall, Lost, Answer; plus the Third Horn if `TH_THIRD_HORN`). Carrier: the TF-M1 practice horn (Act I §A10). Fallback: Ressa's loaned warden's horn in `S00`. |
| **Echo-count return** | Audio + Systems | When the player blows Answer, a raycast to the nearest face tagged `echo_face` returns a beat count (1 / 2 / 3+ / none) by distance band; plays the echo after that many beats with tick UI. |
| **Warden post call cycles and assist re-call** | Systems | Per-post timed call loop; progress check; double call + pinned glyph after 45 s without progress. |
| **Rope boundary volumes** | Systems | Blocking volumes with a bark. |
| **Shelter niches** | Systems | Safe volumes for Fall and gusts. |
| **Gust hazard with whistle tell** | Systems | Bible §9.5 wind-window convention; push toward a defined inner side only. |
| **Gallery call sequencer** | Systems | Ordered call list with per-gallery state (spent / live / resolved); repeat live calls; haul stages advance only with the player in zone. |
| **Marker stone glyph inspect** | UI | Inspect showing the glyph large. |
| **Pull-line cut interaction** | Systems | 3 s channel, interrupt on damage; resolves the gallery. |
| **Forced shelter** | Systems | Gust state on the cut that holds while `S03` is incomplete; ends on rubbing acquired. |
| **Wipe and rub interactions** | Systems | Per-panel channels with persistence; rubbing creates `TSW_closure_rubbing`. |
| **Boss: Ingrith** | Gameplay + animation + audio | Spear moveset with spoken count; drum-brake slab drop on the hornman's Close; gust and shed hazards; yield threshold at ~20%. |
| **Channelled segments with persistence** (winch) | Systems | Lowmark MQ4 crank convention, three segments. |
| **Hold interaction pacing a crowd** | Systems | Sustained hold; release pauses a scripted crowd path; crowd waits in a lee volume. |
| **Scripted column crowd** | Systems + NPC | ~31 NPCs, goats and sledges on a path in tally order. Fallback: 10–12 visible walkers with goat and sledge props, the rest implied by Runa's count. |
| **Straggler NPCs with call loops and rope tow** | Systems + NPC | Two NPCs blowing Lost; reply logic per `TH_THIRD_HORN`; tow carry state at walking pace; patrol fallback places unreached stragglers with the dawn patrol. |
| **Keep watch** | Systems | Lowmark convention. |
| **Assembly placement from flags** | Systems + NPC | Per-player NPC position sets keyed on §8.4; one movement animation set per posture. Fallback: static placements per posture without the movement. |
| **Four standing-place volumes with confirm** | Systems | Enter + confirm sets `TH_STAND`. |
| **Posture computation** | Systems / quest scripting | §9.3 arithmetic on flags at `S11`. |
| **Quest item `TSW_closure_rubbing`** | Schema | Non-droppable document with inspect text (dialogue file D-2). |
| **Epilogue state presentation** | Systems + art | Per-player props keyed on `TH_ASSEMBLY_POSTURE`, `TH_STORES`, `TH_HORN` (§E). |
| **Thaw presentation** | Systems | `TSW_THAW` set on first re-entry after leaving the region post-completion; swaps snow props for thaw props (§E.7). See open decision 3. |
| Creatures | Schema / Gameplay | Ridge wolf runner, howler; Iron Winter spear, hornman; Ingrith (boss). From the Batch 4 enemies package. |
| Batch 3 flag names | Side-quest authors | `TDS10_SEEN` and `TME01_TALLIED` are **[NEW] placeholders; the Batch 3 package fixes the names** (its draft uses `TME01_EXPECTED` for the tally-add; TDS10 has no named flag yet). Swap in this file and the dialogue file only. |

## 13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Who Thornfell shut out** (R06 sealing) | The late-war sealings left people on the far side; the gate-warden cut their names beside the dates; nobody read it. | "Thornfell held the wall." | The roster (required inspect); the rubbing; Hushfold's first tally book (Weatherall, came over in the thaw). | The sealing was pure heroism; Hushfold are deserters' families. | How many died outside; where the rest went (some reached the Mire: R14, not here). | **TF-M5** (owned here). |
| **Why Thornfell went hungry** (quiet) | Relief trains that reached the far gate in the final year's long winter were turned back by Thornfell's own closing. | Emberholt starved Thornfell. | The turn-back lines, dated in the long winter; Ingrith's own date for her hunger. | The roster lies; the trains were Emberholt tricks. | Where the trains came from; who ordered them turned back. Never stated (FT-03 spirit: no invented routes). | Seed only. Never stated in Thornfell. |
| **Who cut the roster** (TD-10) | An unnamed late-war gate-warden. | Nobody knows it exists. | Uneven hand; the last line ("snow too thick to count"). | An Assembly order; a clan record. | The cutter's name. | **Never** (TD-10). |
| **What Ingrith's tribunal decides** | Open. | — | She is held; her clan will sit at thaw. | — | The verdict. | Not authored in Thornfell v1.5 (open decision 5). |
| **The stranded who did not come back** | Some reached the Mire. | — | Names on the rubbing with no Hushfold match. | They all died. | Their fates. | R14 / CV-M3 chip (bible §8.2). |

## 14. Open decisions

1. **TD-8** (Gatefall mechanism) is used as recommended: mechanical deadfalls, horn-ordered, no resonance. If the Director restores a resonance cause here, the galleries become the place it lives; the roster, the slab and the Assembly are unaffected.
2. **TD-5 / closure account** [PROPOSAL — DIRECTOR]: adopted in every outcome as the brief requires. If replaced, the three posture endings lose their "who keeps the account" line only.
3. **Thaw presentation** [PROPOSAL — DIRECTOR]: `TH_SEASON` has only autumn / snow (bible §9.2). This package does **not** add a `thaw` value; it proposes a quest-local `TSW_THAW` presentation state set on the player's first re-entry to Thornfell after completing TF-M5 and leaving the region once. The Director may instead extend `TH_SEASON` with `thaw`; the §E.7 table works with either.
4. **The player's horn (resolved, independent review).** TF-M1 gives the Hornbearer's practice horn as a reward tool; TF-M5 relies on it. Ressa's loan (`TSW_HORN_LOANED`) remains only as a fallback for a player without it. The item pass decides both horns' item form.
5. **Ingrith's tribunal verdict** is deliberately not authored. Recommendation: leave it unresolved in v1.5; epilogue shows her held and the tribunal "sitting at thaw".
6. **Bersi and Eyvind** `[SPLINTER]`: their fates belong to TF-M2, TF-M4 and *The Notes We Keep*. TF-M5 does not mention them except that "the Iron Winter's crews" are walked down. Recommendation: one Assembly bark at most, none required.
7. **Gallery calls** [NEW]: the Close-plus-tag sealing calls are new wartime calls. They are not refused calls (bible §9.4 lists only the Split, the Third Horn and Witness at the Gate). Ressa's line treats them as calls nobody needed to refuse because nobody thought they would be blown again. If the Director prefers them refused, add one line to `TSW-D1` and nothing else changes.
8. **Architecture wording.** The architecture's TF-M5 row mentions "Horn-Echo surges"; the bible (review finding) removed them. This package follows the bible.

## 15. Internal review log

| Finding | Revision |
|---|---|
| The whiteout climb risked being unreadable for deaf or hard-of-hearing players. | Call-shape glyphs with direction, dimmer delayed echo glyphs, echo-count ticks, and a caption line. Visual second tell at niches (rag flutter). |
| The climb risked a fall-death fail state. | Rope boundaries everywhere on the open side; gusts push only toward the inner wall; no timer; assist re-call. |
| The gallery puzzle risked a race against a pull timer. | Crews haul only in lulls and only with the player in zone; live calls repeat. A wrong guess is walking time. |
| Gallery tags could collide with Gather (three short) or Fall (short-long-short). | Tag set excludes both; every sealing call begins with Close. |
| Resonance at the Gatefall (architecture wording). | Removed per bible §2.4/TD-8. Only gusts, loose stone and white. |
| The roster risked being missed under time pressure. | A forced shelter holds the storm on the cut until the rubbing is taken; no clock runs during it; wipes and rubs persist. |
| The roster risked identifying people by itself as "the dead". | The roster says who was outside, not who died. Maera, if she reads, reads names, not deaths. No line says anyone on it died. |
| Runa's tally beat could be missed while fighting. | It plays during the hold, which has no enemies; the hold cannot finish until the reading has. |
| Ingrith risked a villain speech or a contrition scene. | Three lines before the fight; a short exitable yield scene; one question about the turn-back lines; she goes back to counting. Nothing she says is proof. |
| The hunger-winter contradiction risked being stated. | The roster dates the turn-backs in the final year's long winter; Ingrith dates her hunger to the same winter in her own words. No NPC links them; one interaction-log line at most. |
| Stragglers risked being lost. | Patrol fallback at dawn; both always seen alive. `patrol_brought` costs only a posture point. |
| The Assembly risked becoming a hearing. | No questions, no proof, no testimony: placement, one reading, movement, a repeated decision. |
| Hadrik risked deciding. | He places people and repeats what the hall says; "That's all a speaker does." |
| Hadrik's scars. | No date, battle or Stonebound contact; a stage note only (a hand on the speaking stone). |
| Brynjar risked being cast as splinter-adjacent. | His lines say he did not know; his tribunal line is about his clan's duty. Not a member (TD-1, ledger). |
| Maera's authority over the dead. | She reads names and decides nothing about stones here; if the player stands at her bench she says the names will go "where I put them" (epilogue copy at the name-stone wall). |
| Kaldren appearing to validate. | Present only if he keeps the plates; one line, about stresses. |
| Iven reporting interpretation. | His W3 report gives direction, weather and timing before any reading of it. |
| Dorn and named roster custody. | Dorn never holds the roster or the rubbing. The wall stays where it is; the player keeps the rubbing; Ressa writes the new account. |
| Item budget. | One quest item; Thornfell total 4 of 4. |
| Lowmark independence. | No Lowmark state required. One optional Elira line with `LM_CIVIC_STANDING`. The turn-back lines never say where relief came from. |
| **Independent review (2026-11-03)**: 10 findings (2 medium, 8 low). | Horn: relies on TF-M1's practice horn; Ressa's loan is fallback only. `TDS10_SEEN`/`TME01_TALLIED` marked [NEW] placeholders. `TSW-D9.2x` made explicit. `TSW-B6` reference corrected to `TSW-D6.11`. Hadrik-totals consistency stated (§8.4; dialogue cast note). §E.6 relief sacks now exclude `seized`; §E.10 no longer contradicts sealed_with_terms. Roster near-collisions renamed (Sigrid→Astrid Weatherall, Asgeir Holt→Arvid Lunde, Ragna Holt→Ragna Lunde, Brekke→Tofte carters). `[SPLINTER]` tags on `TSW-D5.40`, `TSW-B10.2`. |

---

# E. Thornfell epilogue states

This section is the single reference for how TF-M5's outcomes change Thornfell after `TH_STANDING`. Everything here is **per-player presentation** (bible §9): props, NPC positions and barks keyed on the player's own flags, with the Lowmark per-player prop fallback (partners see their own state; where that is impossible, the host's props and each player's own barks). Barks are in the dialogue file Part 6 (`TSW-B11` onward). No epilogue state removes access to any site or service.

## E.1 Passwatch [TP02]

| Element | **open** | **watchful** | **sealed_with_terms** |
|---|---|---|---|
| Vessa's gate slate | Two slates on the gate post: "Shut / Open" and, beneath, a second slate headed **Outside**, filled in, wiped and refilled each closing. A copy is chalked on a public board by the store-yard. | The **Outside** slate hangs inside the warden post; Vessa reads it to anyone who asks. | The **Outside** slate is full: the far-hut winterers and the shieling households by name, with "fed" ticks by week. |
| Gate | Storm closings only; opens after each storm. | Storm closings at Ressa's word. | Gate shut for the season at deep snow; the relief line goes out through a postern each week (wardens with rope, a sledge, Dorn's horn). |
| Horn post | Dorn teaches Answer to children at the post on fair days. | Ordinary. | Dorn blows **Lost** once each dusk toward the far side; the far hut **Answers** (audible from the post on calm evenings). |
| Store-yard | Empty tarp gone; highstead sledges loading common-store sacks. | Ordinary. | Relief-line sledges loading. |
| Vessa | "Two slates now. Twice the chalk." | "People ask. I tell them. That's new." | "I write them every week. Every week they're still there." |

## E.2 Hushfold [TP04]

| Element | **open** | **watchful** | **sealed_with_terms** |
|---|---|---|---|
| The shelter line | Smoke from every house; the far-shieling households wintered in. Doors marked with the tally chalk. | As open, with two shieling households who chose to winter outside named on Vessa's slate. | Three households winter at the shielings and the far hut by choice (herds), named in the account and fed by the relief line; their Hushfold houses are shut with tally chalk on the doors: "Out. Fed. Expected." |
| Runa | At the tally board, reading it to newcomers; adds names freely. | At the tally board. "We still have to ask. We ask louder now." | At Passwatch on relief-line days, counting the sacks out herself. |
| The first tally book | Kept in Runa's house. A ribbon now marks the Weatherall page. With `TSW_READER = runa`: a copy of the rubbing pinned beside it. | Same. | Same. |
| Oddny and Halvard | `TSW_ODDNY/HALVARD = player`: they greet the player by name (Hushfold uses names after the tally add). Halvard on a stick. `patrol`: they talk about Vessa's patrol and "the far hut, which is a terrible hut". | | |
| Name-slip (TWN Completed) | The TWN family's slip and the Weatherall page sit on the same shelf. | | |

`TH_HUSHFOLD_VOICE` true in any posture: Hushfold has a standing place on the near ring of the hall from now on (prop: a chalk mark on the hall floor by the stone; Hadrik's post-quest bark).

## E.3 Stonewake [TP01]

| Element | **open** | **watchful** | **sealed_with_terms** |
|---|---|---|---|
| Assembly Hall | A **closure account board** stands by the door wall: closings and names, public. | The board is in the Wardens' room off the hall; a warden reads it on request. | The board by the wardens' rail lists the relief line's runs with the names fed. |
| Signal Terrace | Each closing is called with **Close** and then read aloud: who is outside. A crier role (warden). | Ordinary. | Each relief run leaves with **Gather** and returns with **Rest**. |
| Hadrik | In the hall, placing nobody, sweeping snow off the floor himself. | Same. | Same. Hadrik's bark varies by posture only in one word. |
| Ingrith `[SPLINTER]` | Held in the hall's cold room until her clan's tribunal sits at thaw (all postures). Optional conversation `TSW-L-INGRITH`. | | |
| Brynjar | `disowned`: at the ridge-market with Elira, arguing about sacks, then defending her to a stranger. `defended`: at the Blood-Oath towers; gruff with the player unless `TH_STAND = brynjar`. | | |
| Market | Ridge-market prices ease (common store). | Prices steady. | Prices tight; Elira's storekeepers ration. |

## E.4 Nettlehook [TP03]

| Element | **open** | **watchful** | **sealed_with_terms** |
|---|---|---|---|
| Granary | Shared granary topped up from the common store (Iron Winter reserve counted out). | Ordinary winter stocks; `TH_PASSWATCH_ROUTE = sledge` makes it full, `caravan` lean, `split` middling (bible TF-M1 consequence, unchanged). | As watchful; relief-line sledges stop here to load ropes. |
| Ropeway | Running; Tova rides it to lessons if *Nettlehook Rope* Completed. | Same. | Running; carries relief-line loads up the first leg. |
| Ketil | "Granary's full. I don't trust it. I'm counting it every day." | "Same as every winter. That's good. I'm told that's good." | "Rope goes out Mondays. I check the rope Sundays." |
| Tova | Asks the player who is outside this winter. The answer is on the public board (open), "ask a warden" (watchful), or a list she reads off Vessa's slate herself (sealed). | | |
| `TH_HIGHSTEADS_TOGETHER` | Rope-Raising Day's witness ribbon still tied to the ropeway pylon in all postures. | | |

## E.5 The Gatefall [TP09]

| Element | **open** | **watchful** | **sealed_with_terms** |
|---|---|---|---|
| The slab | Up and wedged until deep snow, then lowered with the wardens' rope route left open beside it (a narrow cut stair). At thaw: the shared opening (§E.7). | Up until deep snow; lowered at Ressa's word. | **Down** this week; a postern hatch in the gatehouse lets the relief line through. |
| The roster wall | Cleaned of soot; plaster not replaced; a rail in front and a bench. Anyone may read it. | Cleaned; a warden's rail; read by asking the post warden. | Cleaned; the new closure account slate hangs **beside** the roster, so the old names and this winter's names are side by side. |
| The galleries | All three live galleries **re-wedged and pinned dead** by wardens (iron straps across the pins). G7 cleared and its loose stone barrowed off. Same in every posture: nobody can drop them again. | | |
| Horn post | On the near apron. The player can blow any call and hear a true echo. With `TH_THIRD_HORN`: a small Third Horn glyph cut beside the post. | | |
| Wardens | Two on the gate. | Two on the gate. | Four; a brazier; the relief line's sledge stored here. |
| Ingrith's camp | Bedrolls gone; the cookpot left on the hearth (the wardens use it). The child's mitten pinned on the drill board peg, unclaimed (all postures). | | |

## E.6 The Whinstone Store [TP08], by `TH_STORES` and posture

| `TH_STORES` | **open** | **watchful** | **sealed_with_terms** |
|---|---|---|---|
| **reported** (Assembly seal since TF-M2) | Seal cut in public; Elira's storekeepers count the reserve **out** into highstead granaries and Hushfold. The store stands empty with its hoist cage wound up and a closure-account-style list chalked on the gate: what went where. | Seal kept; the reserve stays in store **under Assembly account**, counted at each new moon by a warden and a Hearthguard storekeeper together. The hoist shaft is barred. | Seal kept; the store becomes the **relief line's depot**: sacks go out weekly to the far side. |
| **seized** (carried down in TF-M2) | Empty already. Becomes a shelter on the track (hauliers sleep there); weapons and plates gone. | Empty; wardens use the galleries as a storm shelter. | Empty; the relief line stages ropes and sledges here. |
| **leverage** (still filling until TF-M5) | At TF-M5's end the store is taken under Assembly account in every posture (the splinter is over). Open: counted out publicly; the iron goes to the bridgewrights for fittings (Aud, *The Bridge That Chose* tie). | Kept as reserve under account, now fuller than any other outcome. Brynjar's people call it "the Assembly's iron". | Kept; feeds the relief line; the iron stays racked under seal. |

**With `reported` or `leverage`** (with `seized` they went down to the highsteads in TF-M2 and were eaten) the Lowmark relief sacks (the RELIEF — FENMERE stencils) are set apart in the grain gallery with their stencils facing out, untouched, under a chalk note: *"Not ours. Kept till asked."* Nothing says where they came from or how (FT-03; TD-11). This is a seed the Lowmark return arc may read; nothing here depends on it.

## E.7 The thaw [PROPOSAL — DIRECTOR; open decision 3]

When `TSW_THAW` is set (first re-entry to Thornfell after completing TF-M5 and leaving the region once), Thornfell shows the thaw: snow-cover props swap to meltwater and wet stone, the Narrows runs loud, goats are back on the ledges. One **thaw event** plays at the Gatefall the first time the player visits it after `TSW_THAW`:

| Posture | Thaw event at the Gatefall |
|---|---|
| **open** | **The shared opening.** Dorn blows **Gather** for everyone, then **Rest**. Hushfold, Nettlehook and the wardens stand on both aprons; Ressa reads the winter's closure account aloud (short: "Outside this winter: none we know of. Every closing called.") and the slab goes up with many hands on the winch. The player is asked to take a turn on the bar. |
| **watchful** | Ressa and two wardens raise the slab. Vessa reads the Outside slate to the wardens and wipes it. Runa comes up with Kolli to watch and says one line. |
| **sealed_with_terms** | The slab goes up; the relief line comes home through it for the last time this season, with the far-hut winterers walking in behind it. Ressa reads every name on the winter's account as they pass. |

In all three, the roster wall is visited by someone (Runa in open, Vessa in watchful, the winterers in sealed) and Ingrith's tribunal is said to be "sitting this week" (bark). No verdict is given.

## E.8 Thornfell master commissions

`TH_STANDING` is Thornfell's regional standing (bible §9.1), the narrative-legitimacy step for its master commissions, extending the approved aspirational-commission pattern (`DESIGNS/Economy Design/Caelmor_Aspirational_Equipment_Foundation.md`; architecture "regional master commissions: high skill plus regional standing"). This package authors only **who offers what, where, and the offer line** (dialogue file Part 7). The offer opens a commission; it grants nothing. Skill thresholds, materials (ridge iron, stormwood and goat leather are not yet catalog items; TD-13), stats and steps belong to the economy pass. Names are functional placeholders [NEW].

| Commission (functional name) | Giver | Where | Skill line | Variant |
|---|---|---|---|---|
| **Bridgewright's fittings** | Aud Hammerlee | The Narrows / Passwatch field anvil | Smithing | *The Bridge That Chose* Completed: she mentions the triage board. `TH_STORES = leverage` and open: "Assembly gave me iron. Splinter iron. It doesn't know." |
| **Stormwood war-bow** | The Stonewake bowyer (role name from *Stormwood*) | Stonewake | Fletching / Ranged | *Stormwood* Completed: the bowyer remembers the stave the player picked. |
| **Ridge Warden's horn and harness** | Ressa Highcrag | Three Calls Shelter | Smithing / Leatherworking | Ordinary horn, no plates (Ressa: "Cow horn and brass. Nothing in it but breath."). `TSW_HORN_LOANED`: built on the horn she loaned. |
| **Far-side coat** | Runa Weatherall with a Hushfold leatherworker | Hushfold | Leatherworking (goat leather) | *Goat Year* Completed: the leather is from "your herd". |

None depends on posture, `TH_STAND` or any other TF-M5 choice. Every player who completes TF-M5 receives all four offers. Posture changes only one word or line in each offer.

## E.9 `TH_HORN` in the epilogue

| Value | Presentation |
|---|---|
| **silenced** | Plates damped in the Summit's null alcoves; Kaldren visits them. At the Assembly he stands at the back wall. Epilogue bark: "Still asleep. I check." |
| **broken** | Cracked plates swept into a pile on the Summit hall floor, roped off. The Blood-Oath towers' boast is not heard in Stonewake's market barks any more; Brynjar's clan tower crew bark sourly about it. |
| **surrendered** | Plates in Ressa's keeping at Three Calls, crated, under a tarp chalked "Not for blowing." *The Notes We Keep* reads them. |

No posture changes `TH_HORN` presentation. No plate is ever reinstalled in a horn (bible TNK).

## E.10 What every ending shares

Nobody outside is left unnamed: the gate stays open while anyone is still coming in, and when it shuts (deep snow, or now under terms) everyone known to be outside is on the account. The Iron Winter is over: its leader is held for her clan, its crews are walked down, its store is under Assembly account, its galleries are pinned dead. The roster is uncovered and read. Hushfold's tally book is the second custodian, and stays in Runa's hands. Every closing in Thornfell from now on names who is outside, and somebody keeps that account. The player has a place to stand in the hall and a rubbing in their pack. Nobody in Thornfell says where the turned-back relief came from, or what the long winter did to anyone on the other side of a pass.

---

# Act III review log (cross-package)

| Check | Result |
|---|---|
| Brief compliance (bible §6.1 TF-M5) | Offer, situation and beats 1–6 implemented in order: whiteout by horn; galleries with glyphs, grey/pale props, wedge crews or pull-lines; gatehouse roster with required inspect and rubbing (Weatherall; turn-back lines in the long winter); Ingrith boss yielding ~20%; three-segment winch and hold; Runa's tally (second custodian); stragglers by Lost call, Third Horn or Dorn, patrol at dawn; Assembly by placement, one reading, posture, tribunal, closure account, `TH_STANDING`. |
| No resonance at the Gatefall | No echo-figures, surges or hum. Ordinary gusts, loose stone, whiteout. |
| Anchor limits | Hadrik: places and repeats; scars undated. Brynjar: not in the splinter; protective of children. Maera: authority over the dead respected; names read, not deaths assigned. Ressa: refuses calls only in her own practice; no named roster custody (she writes a new account, the old roster stays in the wall). Dorn: calls and replies; altered echoes never proof. Kaldren: stresses only. Iven: reports direction, weather, timing. |
| Evidence rule | Roster and tally book carry the revelation. Combat reveals nothing. Ingrith's words are testimony with no proof weight. |
| Three states | No fail anywhere. Every required proof on the critical path, persistent. Column always through; stragglers always safe. |
| Region flags | Reads only §9.1 flags; sets `TH_COLUMN`, `TH_STAND`, `TH_ASSEMBLY_POSTURE`, `TH_STANDING`. No new `TH_` flag. Thaw uses a quest-local state pending decision. |
| Quest items | `TSW_closure_rubbing` only (Thornfell 4 of 4). |
| Splinter tagging | Every beat and node naming Ingrith tagged `[SPLINTER]` here and in the dialogue file. |
| Lowmark independence | No requirement; one optional line; the Lowmark sacks are kept "till asked" with no route stated. |
| Scope | No schema, JSON or C#. Integration needs listed for later. |
