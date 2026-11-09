# Mire Main Questline, Act III: Bannerline

**Status:** Authored production content for Creative Director milestone review. This package implements Mire milestone **MR-M5 *Bannerline*** (`MBL`), the regional capstone, as written in the Mire bible §6 table and §6.1 brief, with the circle attendance rules of §9.3 and the boss brief of §10.1. Everything marked **[NEW]** is authored here and is not canon until the Director promotes it. **[PROPOSAL — DIRECTOR]** marks a consequential choice the content is built on. **[CANON]** marks material taken from Phase 1 or the reconciled `LORE/` files. **[APPROVED — id]** marks an approved foundational truth. No schema, production JSON or C# is created here. This is Mire milestone content, an internal production milestone of the complete game (CDR-3). Combat follows the Director rulings of 2026-11-03 (`Caelmor_Director_Rulings_Combat_Ranged_Release.md`): every enemy is defeated at 0 HP (CDR-1); the Mire registers **no** scripted exception (no SX entry); every fight accepts melee or ranged and none requires ranged (CDR-2); standard systems are preferred over bespoke simulation (CDR-4).

**Controlling document:** `04_CONTENT_PRODUCTION/Quests/Caelmor_Mire_Narrative_Production_Bible.md`. Its §6.1 MR-M5 brief, §9 world state, §10.1 boss brief and §11 conventions are binding and are implemented as written. Where this package invents detail, it is marked [NEW] and stays inside the bible.

**Companion file:** `04_CONTENT_PRODUCTION/Dialogue & Narrative/Caelmor_Mire_Main_Act_III_Dialogue.md`. It holds cast notes, every dialogue node referenced here (`MBL-` prefix), barks, inspect texts, the full text of the names roll and of the Griefwatch vigil-book page, the circle arrival lines, the epilogue barks and the master commission offer lines.

**Format:** this package mirrors `Caelmor_Thornfell_Main_Act_III.md` (capstone boss spec and ending matrix), which follows the Lowmark act-package format. Tags used in this file: `[CAUSEWAY]` on every node naming Oswin Garvey's causeway decision (bible §3.1); `[MD-7]` on every Hollowfoot encounter, so a Director ruling that retires Hollowfoot as enemies touches only tagged nodes (§14.1 swap note); `[MD-8]` on the post-story refight. MR-M5 does not depend on MD-3 or MD-4 beyond the bible's note that the night is present in MR-M5's vigil (MD-3 recommendation); no node here needs those tags.

**Parallel authoring note.** MR-M1 to MR-M4 and the Mire side quests are being authored in parallel. This package reads only the region flags exactly as bible §9.1 defines them, plus completion of the side quests the bible itself names in §9.3 (*Lifting Day*). The form of the Warden leaves' stone list is fixed by Act II §B8.4 (stones named by place only; tally marks only; nothing countable) and this act follows it. The Hayle mother's name (Aldith), the banner's place over Griefwatch's vigil-hall door, Lysa's settled man at Fenward and Corra's fold corner were checked against the Act I package, and the leaves' custody forms against Act II, on 2026-11-08.

---

## Act III header

### What Act III does

Acts I and II gave the player three findings: Sorrowmere relaid a wartime causeway across the Field of Fallen Standards and woke the banners (MR-M1, MR-M2); the Memorywardens laid a calm-field over the last battle to stop it, and it killed most of them (MR-M4, R08); and their last leaf says *"The circle is not closed. We could not."* Act III turns that into **one night on Bannerline Ridge and one meal at Sorrowmere**. The player learns the General's count from the one man who has felt it for years, climbs the closed road under it, retires the ridge's risen standards, defeats the General Who Wouldn't Fall for the night, and then holds the gap in the old circle while the people of the Mire come up the road and finish what the Memorywardens could not.

| Quest | Code | The player learns | By doing |
|---|---|---|---|
| MR-M5 **Bannerline** | MBL | The thing on the ridge is the field's own command, fear and obedience with no one in it. It cannot be answered or bargained with. What quiets it is ordinary people finishing a mourning circle. | Matching two holds for the names roll, reading a three-beat count, crossing lanes on it, retiring standards under it, defeating the General, and holding a gap stone while the community fills the ring. |

**Act III turn (bible §1 part 3; R08 as consequence):** "the General is a commander who would not die" becomes "the General is what a battlefield's orders leave in the ground, and the ground is quieted by people standing together, not by a sword." The player leaves with the Mire's tool for the peace: **testimony that holds** (a name is read only when two different keepers stand behind it, and no manifestation ever speaks for the dead).

**Length:** 60–75 minutes including the aftermath (bible §6). **Level framing:** Advanced (MD-10). Exact levels belong to the Gameplay Designer.

### Inputs read (region flags set by Acts I–II and side quests)

MR-M5 never asks how an earlier flag was set; it reads only the §9.1 values. Every value has authored content. No value can block progress. A player who did no side quest has a complete, authored path.

| Flag | Values | Read in | Effect in MR-M5 |
|---|---|---|---|
| `MR_CHANNELS` | bool | Presentation | Always true after MR-M1. No channel crossing is required in MR-M5 (the ridge is the Mire's high ground); one Ide line uses the stake grammar. |
| `MR_NAME_RECORD` | amended / qualified | Names roll; circle placement (§8.2); meal | Amended: the Hayle mother is read as a name; Nell and Dunstan stand side by side. Qualified: she is read as "one we hold, not yet known"; Nell stands with Agna, Dunstan across the ring. |
| `MR_CAUSEWAY` | reset (always after MR-M2) | None | Not read. Oswin's attendance comes from *Lifting Day* (§9.3 rule 4). |
| `MR_BANNERS` | retired / restored | `S04` (Corra and the Banner That Sank Twice); circle placement; choice lines; Griefwatch epilogue | Restored: Corra brings the banner up the ridge; the ridge's standards answer it (one more Wraith wave, one more ally line); she holds a stone. Retired: no banner comes up; Calwen's choice line leans toward laying the standards in the earth. |
| `MR_ROWAN_TRUST` | told / kept | Circle placement; meal | Told: Rowan comes up from the landing and holds a stone. Kept: he keeps the landing lantern lit below the ridge, and the player sees it from the gap. |
| `MR_WARDEN_RECORD` | sorrowmere / altar / tenders | `S01` roll source line; `S06` opening of the rite | Who reads the Warden leaves' last line at the ring, and from what (§9.4). |
| `MR_CLOTH` (side quest MCF) | returned / burned / unset | Circle placement | Returned: Calwen brings the recovered cloth and lays it at his stone. Burned or unset: no line. |
| `MR_LANTERN_LINE` (side quest MLL) | bool | Circle placement | True: the Stillgrave family comes up and lights the ring's lanterns. False: Griefwatch households carry the lanterns. |
| `MR_STRANGER_SEAT` (side quest MSS) | bool | Meal (`S08`) | One Ysolde line about the seat. It stays unexplained (R16). |
| `TH_STANDING` (Thornfell) | bool | `S03` far bend; circle (road stone) | A Thornfell Ridge Warden pair visiting Griefwatch [CANON visits] holds the Iron Bend beside the Marshwardens and stands at the road stone. One of them mentions closure accounts in one line. Never a gate. |

| Quest-local or completion condition (never required) | Read in | Effect |
|---|---|---|
| *Lifting Day* (MLD) Completed | Circle placement | Oswin stands at Edris's shoulder (`[CAUSEWAY]`). Without it, Oswin waits at the closure gate with the Reedsward crew and says one line as the player comes down. |
| MDS07 *The great furrow* read (`MDS07_READ`, Batch 3 discovery flag) | `S02` | Bran's line changes: "You've seen it. Then you know." The furrow is the same world object in both packages. |
| *The Bell Roster* (MBO) Completed | `S00`, `S01` | Ide's roster line; the vigil book's bell-keeper shift column is in the fixed hand the player helped agree. Flavour only. |
| *A Table for the Wet* (MFT) Completed | `S01` optional pot | Lysa asks for "the one you made for the wet". Flavour only. |
| `MNS_FENWARD_VISITED` (MR-M1 quest-local, Act I §A9.2) | Circle (`MBL-B7.6a`) | Jory Wick is the settled man the player met at the Fenward huts; with the flag he nods to the player when the count stops. Flavour only. |
| `MBR_CORRA_CORNER` (MR-M2 quest-local, Act I §B9.2) | Circle (`MBL-B7.9`) | With `MR_BANNERS = restored`, Corra's arrival line thanks the player for the corner of the fold. Flavour only. |
| `MNS` household detail: the Hayle mother's name, **Aldith Hayle** (MR-M1, from the Hayle book) | Names roll (`MBL-R1`) | Amended: read as "Aldith Hayle of Marshfall, mother of Dunstan and of Linnet. Held probable." Qualified: not read as a name. |

### Region flags this act sets

| Flag | Values | Set by | Notes |
|---|---|---|---|
| `MR_BANNERLINE` | quieted / tended | `S07_bannerline` | How the ridge is left. Both quiet the ridge for the story. |
| `MR_STANDING` | bool | `S08_table` | Always true at completion. Opens the Mire master commission offers (§E.10) and the CV-M1 gate. |

Act III invents no other `MR_` flag. Quest-local flags use `MBL_` (§9.2).

### Quest-item budget (bible §9.4: Mire total 4)

| Item | Quest | Fate |
|---|---|---|
| `MBL_names_roll` | MR-M5 | Given to the player by Ysolde at Griefwatch when the roll is finished (`S01`): "The witness carries it up. That's the seat's job." Handed to Ysolde at the ring for the reading and handed back (`S06`). Laid in the Names Below register by the player at the Sorrowmere meal (`S08`); removed from inventory there. Not droppable, not sellable. Mire item 4 of 4. |

Everything else is a carry-state object (the vigil pot, a lifted standard pole, a folded standard), a world object read in place (Griefwatch's vigil book, the circle stones, the muster post, the Warden leaves if `sorrowmere`), or nothing.

### Canon grounding (Act III)

| Element | Source | Status |
|---|---|---|
| The General Who Wouldn't Fall: a singular, coherent earth-memory manifestation of command, fear, obedience, death and trauma; not a ghost or a historical general; repeats command, cannot identify a battle, answer questions or settle a record | Dossier §IX; C15 | [CANON] |
| The General formed when the last Memorywardens grounded the last battle | World Truth H17; Timeline §V | [APPROVED — FT-02c] |
| Bannerline Ridge: rare high ground, a last-stand site, old palisade stakes, iron-rich soil | Dossier §VI.5 | [CANON] |
| Griefwatch keeps vigil over the old battlefield; Ridge Wardens from Thornfell sometimes visit | Dossier §VII.3 | [CANON] |
| Hollowfoot: humans driven half-mad by war trauma; wander without awareness of time; react violently to loud noise and bright banners | Dossier §IX | [CANON]; enemy use is MD-7 [PROPOSAL — DIRECTOR] |
| Earthen Echoes collapse into mud when struck; Banner Wraiths dissipate when the banner is honoured or retired | Dossier §IX | [CANON] |
| The Sorrowback: the other major threat; trail only here | Dossier §IX; bible §2.4 | [CANON]; trail [NEW] (MDS07) |
| Bran Hollowstep watches, does not patrol; knows which ground is unsafe; leaves offerings for no one in particular | Mire anchors V; Part 4 ledger | [CANON] |
| Edris, Calwen, Mara, Rowan, Sennic, Lysa limits | Mire anchors; Part 4 ledger | [CANON] |
| Public mourning circles; anchor circles; "the climax emphasizes healing through remembrance" | Dossier §VII.1, §XV.5 | [CANON] |
| The Bannerline circle (twelve stones and a gap), its unfinished rite | Bible §2.1 | [NEW] |
| The count (three beats, move on two) | Bible §1.1 | [NEW] |
| Two holds, one name; the names roll | Bible §1.1, MD-5 | [NEW] |
| Enemies defeated at 0 HP; earth-memory re-forms only by condition | CDR-1; bible §2.6 | BINDING |
| The Night Count | Bible MD-8 | [PROPOSAL — DIRECTOR] |

### Structure check against the bible §6 core verbs

| Milestone | Primary verb | Distinct from |
|---|---|---|
| MR-M1 | search and match records | — |
| MR-M2 | recover and retire under attack | — |
| MR-M3 | prepare, learn, wait | the only boat crossing |
| MR-M4 | drain and light | the only dungeon |
| **MR-M5** | **read the count and hold the gap**; retire the ridge's standards; complete the circle | The first rhythm fight in the Mire (the three-beat count, readable in the ground). The only place the player holds still while others act. The roll reuses MR-M1's two holds for many names at once, not one. The retirement reuses MR-M2's fold, faster and under the count, with a Woodcutting step MR-M2 did not have. |

No set piece repeats Lowmark or Thornfell: Lowmark's capstone counts four and pulls toward deep water, then every Marking Stone holds at once; Thornfell's holds a winch while a column passes. MR-M5 counts three in the ground, the player steps **off** the gap to survive it, and the standards lie down one after another toward people, not all at once.

### Unlocks across Act III

After MR-M5: `MR_STANDING`; the Mire master commission offers (§E.10); the Bannerline road open (both outcomes); Bannerline Ridge as a revisitable night site with **the Night Count** (§E.9, MD-8); the post-story Mire states (§E); the CV-M1 standing gate (with `LR_STANDING` and `EH_STANDING`).

---
---

# MR-M5 Bannerline (`MBL`)

## 1. The quest in one paragraph

The morning after the player brings the Memorywarden record out of the Sunken Chapel, the mood banners on Sorrowmere's raised ways turn ochre: a way is closed. At Griefwatch the vigil bell rings the closure, **Ide Larrow** has barred the Bannerline road, and **Bran Hollowstep** has walked down from his watchpost for the first time anyone can remember. Ysolde Haverel has come up from Sorrowmere with the register's pages for the field and the ridge; the Warden leaves said the circle on the crown was never closed, and she means to read a **names roll** there. She will read a name only where two keepers stand behind it, so the player sits at the vigil-hall table and checks her register lines against Griefwatch's own vigil book: two water-carriers become names, and a boy who went up with them stays "one we hold, not yet known". Then Bran takes the player to his watchpost and teaches **the count** by putting their hand on the ground: two soft, then the third. "Move on two. Don't be there on three." He points out a great furrow ploughed through the peat below the ridge, full of broken weapons and banner rags, and says it is not tonight's trouble. At dusk Ide opens the closure gate. The player climbs the Bannerline road under the count, crossing the lanes where Earthen Echo files march down on every third beat, past a hollow where Hollowfoot drifters wander, to the old palisade, where the last battle's standards stand risen. The player cuts three of them free and folds them in Calwen's fold while Banner Wraiths form on the count. At the muster post on the crown, the **General Who Wouldn't Fall** coheres out of mud, iron and banner rags. It says only *"Hold." "Close up." "No one leaves."* A Marshfall man who came up with the wardens begs it to say where his father fell. It never answers. The player defeats it at 0 HP and it sinks into the ground, and the mud slides toward the gap in the circle, and the count goes on, softer. Then the people come up the road with lanterns. The player kneels at the gap with a hand on the footing stone, stepping off on two and back on after three, while Edris, Calwen, Mara, Ysolde, Mabyn, Lysa, Nell, Dunstan and the rest take the stones one by one and Ysolde reads the roll. Bran takes the last stone. The count stops before its third beat, and in the quiet the ridge's standards lean, one after another round the ring, toward whoever stands nearest, and lie down without wind. The player says how Bannerline is left: **quieted** (a new stone in the gap, the standards laid in the earth, the road open) or **tended** (a step cut into the gap, the standards raised as Griefwatch's vigil banners, a vigil kept on the crown). Down at Sorrowmere, Agna Ferrow makes the player sit and eat before anyone says a word. Then the roll goes into the register.

**What the player should remember:** a hand on wet ground, waiting for the third beat; the General saying "Hold" to a man asking about his father; Bran stepping to the last stone. **What the player should want next:** to carry testimony that holds out of the Mire, to places that are still letting things speak for their dead.

## 2. Selection record

| Candidate | Verdict |
|---|---|
| **A. The boss as the climax**, with the rite as an epilogue scene. | Rejected. The brief and architecture (Arcs §3.2) say combat disperses the General for a night and the community quiets the ridge. The rite must be the climax and must be played. |
| **B. A "speak to the General" beat** in which the player gets it to stand down or to name someone. | Rejected by canon (C15) and the evidence rule (§11.3). It never answers. The man who asks is the scene's point. |
| **C. Hollowfoot as the main road fight.** | Rejected for MD-7 safety. The road's required fights are Earthen Echo files; the Hollowfoot are one optional, avoidable group, tagged `[MD-7]` and swappable. |
| **D. Names roll by holds at Griefwatch → the count taught by Bran → road under the count (lanes) → retire three standards (Woodcutting, fold) → the General (three phases on the count; the asker) → hold the gap while the community fills the ring and the roll is read → strange moment → choice → meal at Sorrowmere** (selected; the bible brief). | **Selected.** One rhythm learned by touch, used to move, then to fight, then to stand still. |

## 3. Canon grounding

See the Act III header table. Additional local grounding:

| Element | Source | Status |
|---|---|---|
| Griefwatch vigil hall, closure gate, vigil bell | Bible MP03 | [CANON place]; hall, gate and bell [NEW] |
| Bran's Broken Watchpost | Mire anchors V; bible MP17 | [CANON anchor location] |
| The muster post, the lanes, the twelve-stone circle | Bible §2.1, §10.1, MP12 | [NEW] |
| The Dry Muster (old drill ground) is a separate POI and not visited here | Bible MP24 | [NEW, Part 3]; not used |
| Ide Larrow, Hewin Collard, Jory Wick | This package (Ide from bible §5.2) | [NEW] |

## 4. Quest summary card

| Field | Value |
|---|---|
| Working title | **Bannerline** |
| Suggested content id | `mire.main.05_bannerline` |
| Arc position | Act III, regional capstone. Pays off **R08** as consequence; seeds CV-M2 (Sorrowback) and CV-M3 ("testimony that holds") |
| Prerequisite | MR-M4 Completed |
| Offer | Automatic: the next time the player enters Sorrowmere or Griefwatch after MR-M4 completes and they have left Blackwater Landing. In Sorrowmere the mood banners on the raised ways turn ochre (MME01) and a Memorykeeper at the register room says Ysolde has gone up to Griefwatch (`MBL-B0`). In Griefwatch the vigil bell rings the closure. Objective appears: *Go to Griefwatch's vigil hall.* |
| Target length | 60–75 minutes (Griefwatch and Bran ~15; road and standards ~20; General ~7; rite ~10; choice and meal ~10) |
| Combat share | ~35% |
| Traversal on the count | ~15% |
| Labour (cut, lift, fold, hold) | ~20% |
| Dialogue, records and the meal | ~30% |
| Skills | Melee or Ranged (required for the files, Wraiths and the General; either works). **Woodcutting ~[GD: mid]** to cut a standard's lashing stake (`S04`); crew alternative: a Marshwarden saws it, costing two counts per standard. **Cooking ~[GD: low]** optional at Griefwatch (`S01b`, the vigil pot); crew alternative: carry the Griefwatch cook's pot up. No skill gate. |
| Choices | The asker (`MBL_ASKER`: answered / stood / wardens; local). How Bannerline is left (`MR_BANNERLINE`). |
| Unlocks | `MR_BANNERLINE`, `MR_STANDING`; master commission offers; Bannerline road open; the Night Count; Mire epilogue states |
| **Anchor** (contribution contract) | **Griefwatch and the whole community.** Lead voices: Ide Larrow (the closure), Bran Hollowstep (the count; the last stone), Ysolde Haverel (the roll). Supporting anchors at the ring: Edris Hollowmere, Calwen Reed-Binder, Mara Fenholt (Arcs §3.2 list), Lysa Thornettle, Mabyn Coyle, Rowan Mirewake if told; Nell, Dunstan, Agna, Corra, Oswin by flag; a Thornfell Ridge Warden pair if `TH_STANDING`. All within the Part 4 ledger limits (§15). |
| **World-truth row** | **H17** as consequence (the General formed when the Memorywardens grounded the last battle); **H25** Sorrowback seed only (MDS07 trail; never followed). |
| **Revelation role** | **Pays off R08 as consequence** (the record's last leaf, "The circle is not closed", is answered by the community). Owns no new revelation. Plants: the names roll as practice for CV-M3 "testimony that holds"; the furrow and Bran's warning for CV-M2. Never states which armies, how many died, or any Memorywarden's name (R08 withholds). |
| **Recurring evidence** | **Names roll** (`MBL_names_roll`), built only from two-hold entries: Sorrowmere's Names Below register + Griefwatch's vigil book (a second, independent custodian, checked by the player in `S01`); **the Warden leaves' stone list** and last leaf (MR-M4), read at the ring in the custody line's voice (`MR_WARDEN_RECORD`). The General supplies none: it never names anyone. |
| **State compliance** | Three states only (Inactive / Active / Completed). No fail, no abandon. Every step persists; the hold keeps its progress through death, logout and walking away; the circle always completes. A beaten player returns to Griefwatch with the quest Active and the step unchanged, and a warden at the closure gate walks them back to the last ridge checkpoint. Region flags only from bible §9.1. Per-player state with the Lowmark per-player prop fallback. |
| **Combat compliance** | Earthen Echo files, Banner Wraiths and the General are earth-memory impressions: each is defeated at 0 HP, collapses into mud, and re-forms only by condition (the open circle; a risen standard), never by health. Hollowfoot `[MD-7]` are human: one optional group, defeated at 0 HP with the ordinary defeat presentation; avoidable; never carries evidence; never the only route. No SX exception. No defeated enemy speaks. Every fight accepts melee or ranged; none requires ranged; the count, lanes and lane sweep reach every position so neither style trivialises the General. |

## 5. The places

**MAP VERIFICATION REQUIRED** for every placement in this section. No Mire terrain exists yet. The narrative needs only these relations: Griefwatch sits at the foot of Bannerline Ridge; the Bannerline road climbs from Griefwatch's closure gate to the crown with three named bends; Bran's watchpost stands on a shoulder of the ridge above Griefwatch, off the road, with a view down onto the furrow in the peat below; the crown holds the palisade arc, the muster post and the circle; Sorrowmere is reached from Griefwatch by the ordinary way (no route is described here). No compass direction is given for anything.

### 5.1 Griefwatch [MP03, CANON place; NEW detail]

| Area | Storytelling |
|---|---|
| **W1. The closure gate** | A timber gate across the foot of the Bannerline road, hung between two old palisade stakes brought down from the ridge long ago. A slate on the post: *Road shut. Ask Ide.* Ide's Marshwardens stand here in oilcloth. With `TH_STANDING`, a Thornfell Ridge Warden pair warms their hands at the wardens' brazier (Griefwatch visitors [CANON]). |
| **W2. The vigil hall** | A long low hall built on stone footings (the only stone floor in Griefwatch). A bell rope hangs through the roof to the vigil bell. A long table where Ysolde has spread the register's ridge pages beside Griefwatch's **vigil book**, kept by bell-keepers since the war, one line per bell-night. A cook-hearth with a great pot. With `MR_BANNERS = restored`, the **Banner That Sank Twice** hangs over the vigil-hall door with honours, "for whoever" (MR-M2), Corra Sallis under it. |
| **W3. The fold** | A sheltered yard where Lysa Thornettle has brought people down off the outlying crofts for the night of the closure. **Jory Wick** [NEW], a settled Hollowfoot man in her care (the settled man who sorts reeds at the Fenward huts in MR-M1; Act I gives him no name), sits on an upturned basket with his hands in his lap. Non-combatant, never targetable (MD-7 dignity rule). |

### 5.2 Bran's watchpost and the furrow [MP17, CANON anchor location; MDS07]

| Area | Storytelling |
|---|---|
| **B1. The watchpost** | A broken timber watch-tower on the ridge's lower shoulder, half its platform gone; a lean-to underneath. Offerings on a flat stone: a bent spoon, a ribbon, a heel of bread "for no one in particular" [CANON]. |
| **B2. The practice lane** | Below the watchpost, an old drill furrow running downhill, worn into the turf. On the count, a short Earthen Echo file forms in it and walks down on each third beat (`MBL-E1`). Bran's ground: the count is faint here, so the file is slow and weak. |
| **B3. The view** | From the platform's edge: the peat below the ridge, and through it **the great furrow**, a trench ploughed by something huge, full of broken weapons and banner rags (MDS07). Seen, never followed. No path leads down to it from here. |

### 5.3 The Bannerline road [MP12, NEW detail]

| Area | Storytelling |
|---|---|
| **R1. The Low Bend** | The first turn above the closure gate. Two drill lanes cross the road here, running downhill from the palisade far above. On each third beat an Echo file steps down its lane across the road (`MBL-E2`). Teaching ground: cross on two. |
| **R2. The Rag Bend** `[MD-7]` | The road runs along the lip of a hollow full of torn banner rags caught in gorse. **Hollowfoot drifters** wander in the hollow (`MBL-E3`). The road passes at the edge of their reach; they react to noise and bright cloth (combat nearby, or entering the hollow). Optional. |
| **R3. The Iron Bend** | The last bend, on red iron soil (MDS06), where the palisade's first stakes stand. Three lanes cross here, and the Echo files are thicker. Ide's Marshwardens hold the bend; with `TH_STANDING` the Thornfell pair holds it beside them (`MBL-E4`). Checkpoint. |
| **Agility shortcut** | A short scramble between R1 and R3 up the palisade's fallen stakes (Phase 1.3 agility trigger, optional, walkable fallback is the road). It crosses one lane. |

### 5.4 The crown [MP12, NEW]

| Area | Storytelling |
|---|---|
| **C1. The palisade arc** | A curved line of old stakes along the crown's upper edge, iron-red at the foot. Standards of the last battle are lashed to the stakes, most of them **risen** (cloth moving with no wind). Three stand at the heads of the three lanes, lashed to iron-shod stakes; those are the ones the player retires (`S04`). The rest stand along the arc. |
| **C2. The muster post** | At the centre of the arc: a tall timber post, iron-shod, with a crossbar worn smooth by hands. Commands were called from here. It is where the General coheres. Post-story, striking it at night starts the Night Count (§E.9). |
| **C3. The three lanes** | Drill furrows, about three metres wide and twenty-five long (zone tune), running downhill from the palisade to the circle: **the Stake Lane** (from the leftmost stakes to the circle's left side), **the Post Lane** (from the muster post straight to the gap) and **the Ring Lane** (from the rightmost stakes to the circle's right side). Each lane is read in four segments by the files. |
| **C4. The circle** | A ring of twelve low standing stones, waist high, about sixteen metres across, below the lanes. One gap faces the Post Lane: a flat **footing stone** where a thirteenth should stand. Five of the stones answer the place-names on the Warden leaves' stone list (Act II §B8.4): **the post stone** (S7, beside the gap where the Post Lane ends), **the low stone by the palisade** (S5), **the split stone** (S9), **the stone that faces the field** (S11) and **the stone with the old cut in it** (S3). The rest of the list is lost on the broken corner; nothing says how many the list held. The stones are numbered S1–S12 for production, S1 being the **road stone** (where the road reaches the ring, opposite the gap), S2–S6 up the left side to the gap, S7–S12 from the gap down the right side. |
| **C5. Below the ring** | The road's head, where people arrive with lanterns. From the gap the player can see down over the Mire; with `MR_ROWAN_TRUST = kept`, Blackwater Landing's lantern is one point of light far below (presentation; **MAP VERIFICATION REQUIRED** for sightline, or replace with a light on the nearest channel). |

### 5.5 Sorrowmere [MP01]

| Area | Storytelling |
|---|---|
| **T1. The long table** | Beside the register room, under a reed roof: trestles, benches, a fire. The meal for everyone who came down off the ridge. |
| **T2. The register room** | The Names Below, open on its stand; the stranger's seat on the visitor's side. Where the roll is laid (`S08`). |

## 6. Player-facing sequence

### Beat 0: The Closure (`S00_closure`)
**Objective:** *Go to Griefwatch's vigil hall.*
The quest starts the next time the player enters Sorrowmere or Griefwatch after MR-M4 is complete and they have left Blackwater Landing (so it never starts during Ysolde's scene at the landing). In Sorrowmere, the street banners on the raised ways have turned ochre, the colour for a closed way (MME01); a Memorykeeper at the register room door says Ysolde took the ridge pages up to Griefwatch and asked for the witness (`MBL-B0.2`). In Griefwatch, the vigil bell rings the closure: three strokes, a rest, three strokes (`MBL-B0.1`). Travel is ordinary.

At the closure gate (W1), Ide Larrow will not open the road but sends the player to the hall (`MBL-B0.4`). In the vigil hall (W2), Ide and Ysolde give the situation together (`MBL-D1`): the Echo files have been coming further down the road each night since the chapel record came out; two drifters walked into Griefwatch's crofts last night and had to be brought to Lysa; Bran came down at dawn and said, to Ide, "It's counting." Ysolde has the record's last line on her mind: the circle is not closed. Her reading (she says it is hers): finish the circle. She has come to read a roll at it. Ide: "I'll open the road for people going up to finish something. Not for people going up to look."

- **Variants:** `MR_WARDEN_RECORD` (what Ysolde has with her: the leaves in Mabyn's oilcloth, her reed copy of the last leaf, or Mabyn's word that she will come up and say it); `MR_BANNERS = restored` (Corra by the Banner That Sank Twice, asking to carry it up; Ide says not yet).
- **Verbs:** travel, listen.

### Beat 1: The Roll (`S01_roll`)
**Objective:** *Help Ysolde check her names against the vigil book (0/3).*
Ysolde has compiled most of the roll at Sorrowmere from register entries that already have two holds. Three entries for people lost on the ridge road have only one hold, the register's own line. Griefwatch's vigil book is the second keeper she needs (`MBL-D2`). The player reads each register line (shown on the table, inspect), then turns the vigil book's pages to find a bell-night line that holds it, and **shows** Ysolde the match (dialogue option gated on the vigil-book page being open; the Lowmark/Thornfell show-evidence convention).

| Register line (hold 1) | Vigil-book line (the match) | Result |
|---|---|---|
| *"Hamon Tasker, reed-cutter, of Sorrowmere. Went up the ridge road with the water-carriers. Not come down."* | Bell-night page: *"Rung down for the water-carriers: Tasker. Coldridge, the bell-keeper's girl. And a boy."* | **Name.** Two holds. |
| *"Lettice Coldridge, of Griefwatch. Carried water. Not come down."* | Same vigil line. | **Name.** The vigil line names her clearly; it counts as a hold for each person it names. |
| *"Osric Peale, a boy of Marshfall, carried water for the ridge. Not come down."* | Same vigil line: "And a boy." | **One we hold, not yet known.** The vigil line does not name him. Ysolde: "We know a name. We don't know it's his." |

A wrong page shown is answered kindly ("That's a bell-night, but it's not him. Try the water-carriers.") with no penalty. When the three are done, Ysolde writes the last lines and gives the player the **names roll** (`MBL_names_roll`): "The witness carries it up. That's the seat's job." (`MBL-D2.40`). This is the region's tool, performed once by the player before the climb: the boy's name is known, and is not read as his.

**Optional (`S01b_pot`):** "Sit. Eat. Then tell it." Lysa (W3) asks for a pot for the wardens going up. Cook the vigil pot at the hall hearth (**Cooking ~[GD: low]**; fen fowl and root stew per the economy pass; *A Table for the Wet* complete: "the one you made for the wet") or carry the Griefwatch cook's pot to the gate (crew alternative). Either way the wardens eat before the climb (`MBL-B1`). Ordinary cooked food in the player's pack is the reward for cooking it. Also at W3: Lysa and Jory Wick (`MBL-D2b`): Lysa's guidance about the drifters on the road. "They come at bright and at noise. If you can pass them, pass them."

**Verbs:** read, match, show; cook (optional).

### Beat 2: The Count (`S02_count`)
**Objective:** *Find Bran at his watchpost.* / *Learn the count.* / *Wait for dusk.*
Bran left the hall as soon as the player arrived (`MBL-B0.5`). At his watchpost (B1) he does not explain anything. He kneels and puts his palm flat on the turf, and waits for the player to do the same (interact: *Put your hand on the ground*; the camera does not move). Through the ground: a soft beat, a soft beat, then a deeper one (`MBL-D3`). "Two soft. Then the third. Move on two. Don't be there on three."

**The practice lane** (B2, `MBL-E1`): a short Echo file of two forms in the drill furrow and walks down one segment on every third beat. Bran stands at the lane's edge. Step into the lane and out of it in time: three clean counts (in the lane on beats one and two, out before three) complete the lesson. Being in the file's segment on three knocks the player down lightly (`MBL-B2.3`); Bran says nothing about it. The player may also strike the file to 0 HP: it collapses into the furrow and re-forms on the next third beat, which Bran uses to make his point ("Hitting it's fine. It comes back. The count doesn't stop for you."). Defeating it once also completes the lesson, so a player who prefers to fight is never stuck.

**The furrow** (B3, required inspect): from the platform's edge Bran points down at the great furrow in the peat (`MBL-D3.20`). "Something big walks there when there's fighting. Not tonight's trouble." (Sorrowback seed; MDS07.) With `MDS07_READ`: "You've seen it. Then you know." No path leads down; the player is not asked to follow it.

**Dusk:** "We go up at dusk. It comes down in the dark." Keep watch at the watchpost (Lowmark keep-watch convention; cancellable) until dusk. The quest pins the presentation hour to night from `S03` until `S07` completes (§9.4 note). Bran walks down to the gate with the player.

**Verbs:** touch, listen, step on the count, look.

### Beat 3: The Road Up (`S03_road`)
**Objective:** *Climb the Bannerline road to the palisade.*
At the closure gate Ide unbars the road (`MBL-D4`). Her wardens (and the Thornfell pair, with `TH_STANDING`) go up behind the player to hold each bend once it is passed: "We hold what you've walked." The count is louder on the road; its ripple decal runs across the road surface on every third beat.

1. **The Low Bend (R1, `MBL-E2`).** Two lanes cross the road. On each third beat a file of three Echoes steps one segment down its lane, across the road. Cross a lane on two; or strike the file down (to 0 HP; it collapses and re-forms at the lane's head on the next third beat, which opens the lane for about four counts). Required: reach R2.
2. **The Rag Bend (R2, `MBL-E3`, `[MD-7]`, optional).** Hollowfoot drifters wander in the hollow below the road. Walking the road keeps the player outside their reach. Fighting the file at the bend's lane, or stepping down into the hollow, draws them (standard aggro and assist radius; the shouter calls the others when struck). If they come, they fight to 0 HP with the ordinary defeat presentation. Nobody comments on it except one sober warden line (`MBL-B3.5`). Nothing is found on them. The road does not require passing through the hollow.
3. **The Iron Bend (R3, `MBL-E4`).** Three lanes cross; two files are active at once, staggered by one count. The wardens hold the downhill side of the bend and fight beside the player (allied NPCs, never defeated). With `TH_STANDING`, the Thornfell pair holds the uphill side (`MBL-B3.7`). Checkpoint. Required: reach the palisade (C1).

**Verbs:** climb, cross on the count, fight.

### Beat 4: The Ridge's Standards (`S04_standards`)
**Objective:** *Retire the standards at the heads of the lanes (0/3).*
At the palisade the standards stand risen, cloth moving with no wind. Three stand at the heads of the three lanes, lashed to iron-shod stakes; while they stand, the files keep forming. For each, three interactions, all under the count:

1. **Cut the lashing stake** (channel, ~4 s; **Woodcutting ~[GD: mid]**). The old lashing is bound into a split stake that has to be cut out. Crew alternative: a Marshwarden saws it (`MBL-B4.2`), which takes two full counts while the player keeps the Wraiths off her. The cut is interrupted by a third-beat trample only if the player is in the lane's head segment; they are not, unless they choose to stand there.
2. **Lift the pole** (channel, ~3 s, progress kept): free it from the iron socket and lay it flat.
3. **Fold the cloth** in Calwen's fold (MR-M2): strongest seam, then the hem, then the hoist. A wrong fold just unfolds, no penalty. The player does it faster now: the fold is a three-step interact sequence with no channel between steps.

As each pole comes free, its **Banner Wraiths** form round it on the count (`MBL-E5`): two wraiths at the first standard; two wraiths and a bearer at the second and third (a bearer raises its standard-shape to speed up nearby wraiths; any hit during the raise stops it). Wraiths re-form while their standard is risen; once it is folded, the ones left fight to 0 HP and do not re-form.

**With `MR_BANNERS = restored`:** after the first standard, Corra Sallis comes up the road with the **Banner That Sank Twice** and two Griefwatch Bannerbearers (`MBL-D5`). She stands it at the circle's road stone, and the ridge's standards answer it: every risen cloth along the arc turns toward it at once (presentation). The third standard brings **one more Wraith wave** (two wraiths) and the Bannerbearers hold the palisade's far end as **one more ally line** (allied NPCs, never defeated). Corra stays below at the circle with the banner.

Folded standards are carried down to the circle (carry-state, one at a time, or left on the palisade for Calwen to collect; either completes). When the third is folded, the count changes: the third beat lands at the muster post, and mud starts to rise there.

**Verbs:** cut, lift, fold, fight.

### Beat 5: The General (`S05_general`)
**Objective:** *Face what stands at the muster post.*
At the muster post (C2) mud, iron and banner rags pull up out of the ground into the shape of a commander that is never quite one shape: a crest for a moment, then a pole, then shoulders too wide. It carries a standard pole with no cloth that can be read. It says only orders (`MBL-B5`). Full spec §7.1.

**The asker.** At the first phase change (65%), the General returns to the post and re-musters (an ~8 s invulnerable transition, standard boss behaviour). **Hewin Collard** [NEW], a Marshfall fowler who came up with the wardens, breaks from the wardens' line below the palisade and runs up the Post Lane toward it, calling: "Where did my father fall? You were here. Tell me where." The General says "Hold." and nothing else. During the transition the player has two ordinary ways to act, either of which completes the beat (`MBL-D6`):

- **Answer him** (talk prompt on Hewin, one line): *"It can't tell you. We can look in the books."* He stops (`MBL_ASKER = answered`).
- **Stand between them** (move into the Post Lane between Hewin and the post): he stops behind the player and looks at their back, not at it (`MBL_ASKER = stood`).
- **Neither:** at the transition's end Ide reaches him and pulls him back to the wardens' line (`MBL_ASKER = wardens`). He is never in danger: he is a non-combatant, never targetable, and the General's attacks do not resolve on him.

The General never answers. Defeat it at 0 HP. It collapses into the ground; the mud slides down the Post Lane toward the gap in the circle and soaks into the footing stone. The count goes on, softer (`MBL-B5.9`). Bran, at the palisade: "It'll stand up again tonight. Unless." (`MBL-D6.20`).

**Verbs:** fight on the count, read lanes, answer or stand.

### Beat 6: The Circle (`S06_circle`): the rite and the strange moment
**Objective:** *Hold the gap.* (Sub-objectives: *Step off on two.* / *Step back on.*)
People come up the road with lanterns. Ide is already at the road stone (S1). Ysolde reaches S7, beside the gap, and holds out her hand for the roll; the player gives it (interact), she opens it, and she gives the rite its opening line in the custody line's voice (`MBL-D7.01`–`.04`, §9.4). Then the player kneels at the gap with a hand flat on the footing stone.

**The hold** (channelled, three segments, progress kept):

- While the player holds, people step up to the stones one at a time, set a hand on their stone, and say one line (`MBL-B7`, §8.2). Nobody steps onto the ring while the gap is open and unheld: if the player lets go, arrivals pause at the head of the road and wait (presentation reason, and it means no arrival is ever missed).
- The count goes on. A single Echo file re-forms in the **Post Lane** and comes down it toward the gap one segment per third beat. On the count it arrives (every fourth third-beat), the ripple at the gap brightens on beat two (~1.2 s tell): **step off the gap on two** (release; progress paused, kept), and the file passes through the open gap on three and collapses into mud on the turf inside the ring. **Step back on after three.** A player who holds through the third beat takes moderate damage (~15% max HP) and is knocked back off the stone; the rite's progress is never lost (bible: costs health, never the rite).
- The player may instead strike the file down before it reaches the gap (to 0 HP; it re-forms at the post on the next third beat, buying about four counts). Melee meets it in the lane; ranged can shoot it from the gap. Neither is required.
- **Segment 3:** a second file forms in the Stake Lane and bends toward the gap, arriving two counts after the Post Lane file. The step-off rhythm doubles; the tell is the same.
- **Ysolde reads the roll** from S7 during segments 2 and 3, one entry per arrival interval (`MBL-D7.10`–`.40`, Document D-1). Named entries are read as names. The rest are read as *"One we hold, not yet known."* With `MR_NAME_RECORD = amended`, Aldith Hayle is read as a name, and Dunstan, at the next stone, looks at Nell. With `qualified`, she is read as one we hold, and Dunstan, across the ring, looks at the ground.

**Arrivals** (by flag; full placement in §8.2): Ide (S1) and Ysolde (S7) are already at their stones; segment 1, Edris, Calwen, Mara; segment 2, Mabyn, Lysa, Nell, and S11; segment 3, S3, S12, and last of all **Bran**, who has stood at the palisade watching the whole rite and walks down to S6, the stone beside the gap.

**The strange moment** (§8.3). When Bran sets his hand on the last stone, the count stops mid-beat: two soft beats, and the third never comes. Silence. Then, one after another round the ring, the ridge's standards along the palisade lean toward whoever stands nearest, and lie down without wind. The lantern flames do not move. Nobody says anything for a while. Edris: "Sit a minute. Everybody." (`MBL-D7.60`).

**Verbs:** give, kneel, hold, step off, step on, listen.

### Beat 7: How Bannerline Is Left (`S07_bannerline`)
**Objective:** *Say how Bannerline is left.*
At the ring, after the quiet. The people who stood the stones ask the witness to say it: the stranger's seat's job, Ysolde says, and Edris says they will carry either (`MBL-D8`). Mara speaks for a stone in the gap. Ide speaks for a vigil. Calwen speaks to the standards (variant by `MR_BANNERS`). Bran says nothing until asked, and then: "Either way I'll watch it." **Choice** (`MR_BANNERLINE`):

- **Quieted:** the gap is closed with a new stone that Mara chooses from the palisade's fallen footing stones (she marks it with nothing). The ridge's standards are folded by Calwen and laid in the earth inside the ring, under turf. Griefwatch opens the Bannerline road.
- **Tended:** the gap is left with a step cut into its footing stone, so a keeper can stand in it. The standards go down to Griefwatch to be re-made in community colours and are raised on the crown as Griefwatch's vigil banners. The road opens under Griefwatch's watch, with a vigil kept on the crown each night.

Both quiet the ridge for the story. Consequences in §9.5 and §E.

**Verbs:** decide.

### Beat 8: The Table (`S08_table`)
**Objective:** *Go down to Sorrowmere.* / *Sit.* / *Lay the roll in the register.*
Travel down is ordinary (the night pin ends at `S07`; the player arrives at Sorrowmere at the next presentation hour, morning). At the long table (T1) everyone who came down off the ridge is eating. **Agna Ferrow** makes the player sit before anyone speaks (`MBL-D9.01`): the player is placed on a bench (interact *Sit*), food is put in front of them, and nothing is asked. Table barks play by flag (`MBL-B9`): Nell and Dunstan (by `MR_NAME_RECORD`), Rowan (if told), Oswin (`[CAUSEWAY]`, if he came), Hewin (by `MBL_ASKER`), Corra (if restored), the Thornfell pair (one line about where they are going next; no route stated).

**Then remembrance.** Ysolde opens the Names Below in the register room (T2). The player lays the roll on the register (interact; item removed). Ysolde writes one line beneath the last page, headed by the night's weather as the Mire's records are (no calendar date): *"Read at the circle on Bannerline, which is closed"* (quieted) or *"which is kept"* (tended), and *"Witness: the stranger's seat."* (`MBL-D9.20`). With `MR_STRANGER_SEAT`, Ysolde rests her hand on the seat's back for a moment and says nothing about it. Hewin is at the door (`MBL-D9.30`): if the player answered him on the ridge, he asks for the books now; otherwise Ysolde offers. Ysolde searches: his father is **not found**, and she writes that he asked. "Not found is a record too." Agna: "Now eat the rest." Sets `MR_STANDING`. Quest Completed.

**Verbs:** sit, eat, lay, listen.

## 7. Encounters

Tuned for **Advanced** (MD-10). Exact levels and numbers are Gameplay Designer calls; the targets below are intent. All counts in seconds use the base count: **1.2 s per beat (3.6 s per count)**; the General's phase 3 quickens it to **0.9 s per beat (2.7 s per count)**.

| Id | Enemies (bible §10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **MBL-E1** | 1 × Earthen Echo **file** of 2 echoes (weak variant) | Practice lane (B2) | Lane mover: one segment per third beat; strikes its own segment on arrival | Count beats 1–2 soft (thin ripple), beat 3 deep (heavy ripple down the lane, ~1.2 s after beat 2) | Teach the count by feel | Under 60 s. Cannot drop the player below 70% HP. Defeated at 0 HP; re-forms on the next third beat (condition: the ridge's count) |
| **MBL-E2** | 2 × Echo file of 3 (one per lane) | The Low Bend (R1) | Lane movers crossing the road | As E1. Files raise their arms on beat 2 (~1.2 s) | Cross on two; or strike a file down to open the lane for ~4 counts | 60–90 s; 75–90% HP remaining. Each echo to 0 HP; files re-form at their lane head on the next third beat |
| **MBL-E3** `[MD-7]` | 2 × Hollowfoot wanderer, 1 × shouter | The Rag Bend hollow (R2), below the road | Wanderers drift in the hollow; aggro on entry or on combat within assist radius; shouter calls the others when struck | **Wanderer rush:** hunches, shoulders forward (~1.0 s) then a short charge. **Shouter:** throws head back (~1.2 s) then a shout that pulls the other two to him. Interrupt the shout by hitting him during the throw-back | Optional. Shows what the count is doing to people. Never required, never evidence | 40–60 s if engaged. Human: to 0 HP, ordinary defeat presentation, ordinary loot only. Avoidable entirely by keeping to the road |
| **MBL-E4** | 2 × Echo file of 3, staggered one count apart, across three lanes | The Iron Bend (R3) | Lane movers; one file's head echo turns to strike at the nearest target in its segment on beat 3 | As E2; a turning echo pivots its shoulders on beat 2 | Two rhythms at once with allies holding the flank | 90–120 s; 65–85% HP. Allies (Marshwardens; Thornfell pair with `TH_STANDING`) fight beside the player and are never defeated |
| **MBL-E5** | Per standard: 2 × Banner Wraith (1st); 2 × wraith + 1 × bearer (2nd, 3rd). With `MR_BANNERS = restored`: +2 wraiths at the 3rd | Palisade heads (C1) | Wraiths: slow, readable melee; bearer: **Raise** (lifts its standard-shape high and holds, ~2.0 s, cloth ripples; if not interrupted, wraiths within 8 m attack faster for 10 s; any hit during the raise cancels it) | **Wraith sweep:** cloth arm lifts (~1.0 s) then a wide arc. **Bearer plant:** grounds its pole on beat 3; the 3 m shock-ring decal shows from beat 1 (~2.4 s ahead), then the ring lands (moderate, small knockback outward). Wraiths form on beat 3 near the freed pole | Retire under pressure | ~2–3 minutes for all three. Re-form while their standard is risen; once folded, the remainder fight to 0 HP and do not re-form |
| **MBL-E6** | **The General Who Wouldn't Fall** (boss); Echo files per phase | The crown (C2–C4) | Boss spec §7.1 | §7.1 | Act III boss (bible §10: 1 Act III boss) | 6–8 minutes |
| **MBL-E7** | 1 × Echo file of 3 (Post Lane), segment 3 adds 1 × file of 3 (Stake Lane) | The lanes and the gap during the rite (C3–C4) | Lane movers that pass through the gap and collapse inside the ring | Gap ripple brightens on beat 2 of an arrival count (~1.2 s) | Rhythm while holding still | Rite ~6–8 minutes of hold time in all. Files to 0 HP if struck; re-form at their lane head |

**Rules**
- **Combat never reveals evidence.** The roll is built from the register and the vigil book. The General names nobody. Hollowfoot carry nothing evidentiary. No defeated enemy speaks.
- **Defeat at 0 HP** (CDR-1). Echo files, Wraiths and the General collapse into mud and re-form only by condition (§2.6 of the bible): the ridge's count while the circle is open; a Wraith's risen standard. Nothing re-forms because of its health. Hollowfoot `[MD-7]` take the ordinary human defeat presentation; no yield, no flight, no downed state, no ally comment on mercy beyond one sober line.
- **Melee or ranged** (CDR-2): every fight accepts both. Files can be struck in the lane or shot from beside it; Wraiths are slow and kitable but re-form at their standard, so out-ranging them never ends a fight; the General's lane sweep and Planted Standard reach every position on the crown. Ranged is never required.
- **Allies** (Marshwardens, the Thornfell pair, the Bannerbearers) fight beside the player and are never defeated (standard invulnerable ally NPCs). Non-combatants (Hewin, Jory, Ysolde, every attendee) are never targetable and no attack resolves on them.
- **Death:** see §11. A beaten player wakes at Griefwatch's vigil hall with the quest Active and the step unchanged; a warden at the closure gate walks them back up to the last ridge checkpoint reached. Checkpoints: the closure gate (W1) → the watchpost (B1) → the Iron Bend (R3) → the palisade (C1) → the circle's road stone (C4, from `S06`).
- **Co-op:** shared encounters for partners on the same step; health scales per participant; the count is shared. Each partner's arrivals, placement and roll are presented per player from their own flags (fallback: the host's placement, each partner's own flags stored).

### 7.1 Boss spec: the General Who Wouldn't Fall

**What it is (author truth):** the field's command, fear and obedience, pressed into one coherent imprint when the last Memorywardens grounded the battle (FT-02c). It repeats the pressure and form of command. It is not a returned commander and has nothing in it to answer with. It names no unit, battle or person, and it answers no question (C15).

**What the player sees:** a figure about two and a half times human height, made of peat, iron (old blades, stakes, buckles) and banner rags, whose outline never settles into one commander: a crest, then a pole, then shoulders, then a cloak that is a flag. It holds a standard pole with no readable cloth. A deep, layered voice, like several people saying one word at once. No face.

#### 7.1.1 Arena

| Element | Spec |
|---|---|
| Shape | The crown: the palisade arc above, the three lanes running downhill, the circle below. Play space ~30 × 35 m (zone tune). |
| The muster post | The General's anchor. Phase 1 it stands here. |
| The lanes | Stake, Post, Ring (C3). Each ~3 m wide, four segments. Files move only in lanes. Between lanes, turf strips ~4 m wide (safe from files). |
| The circle | Below the lanes; the lanes end at its stones. It is the arena's lower edge, not part of the arena: the General never enters the ring, and the ring is outside the encounter leash (below). A sweep ends at the lane's foot against the stones. |
| Edges | The palisade above (solid); the ring below; the slope beyond falls away gently to the road head. No fall is possible. **Leash (standard):** the arena is the crown between the palisade and the ring's stones. If no player has been inside it for ~5 s (everyone in the ring or down the slope), the General returns to the post and its health returns to the top of the current phase, as on death. This removes the ring as a safe firing position without any new rule. |
| Light | Night. Lanterns on the palisade stakes (the wardens lit them on arrival) and at the road stone. Every telegraph is a ground decal or a body pose readable in this light. |

#### 7.1.2 The count

| Element | Spec |
|---|---|
| Beats | Beat 1: soft thud, a thin ripple ring from the muster post. Beat 2: soft thud, the same. Beat 3: a deep thud and a heavy ripple that runs down all three lanes. 1.2 s per beat (P1–P2); 0.9 s (P3). |
| Carriers | Audio (positional from the post), ground-ripple decal, optional controller rumble, and an optional caption ("one… two… THREE") for players without audio. |
| What happens on three | Files step one segment; the General issues its phase order (captioned); any boss attack telegraphed on beat 2 lands. |
| The rule | **Move on two.** Every attack in this fight lands on a third beat and is shown on the second at the latest; in P3 every attack (files included) is shown on the first. |

#### 7.1.3 Mechanics

| Ability | Telegraph (readable, non-twitch) | Effect | Counter |
|---|---|---|---|
| **Files** | Files form at the lane heads on a third beat; their arms rise on beat 2 before each step (on beat 1 in P3) | A file's front echo strikes its own segment on arrival: moderate damage, 1 s knockdown | Be out of the file's next segment by three; or defeat the file (all three echoes to 0 HP) |
| **Hold** (shield; P1) | Mud plates across its front, clods spraying when struck | While any file holds a lane, damage to the General is heavily reduced (GD; suggested 80%) | Clear the files. With no file standing, the plates slough off for ~4 counts (~14 s) before files re-form on a third beat |
| **Planted Standard** (all phases) | Beat 2: it lifts the pole high, a ring decal (~5 m) at its feet | Beat 3: drives the pole into the ground; heavy damage and knockback in the ring | Out of the ring on two |
| **Close up** (P2) | Beat 1: mud ridges rise along the edges of the lane, or turf strip, the targeted player stands in. Beat 2: it steps into that lane's head and lowers the pole along it | Beat 3: a sweep down the whole lane length (heavy damage, ~35% max HP), except within ~2 m of its flanks ("inside the turn"). A turf strip is swept the same way when the target stands on one: strips are safe from files, not from the General | Ranged: change lane or strip on two. Melee: step inside the turn, at its flank, on two |
| **Converge** (P2) | Files in the other lanes turn their heads toward the targeted lane on beat 2 | Beat 3: those files step diagonally toward the targeted lane's segment | Read which way they turn; the turf strips stay safe |
| **No one leaves** (P3) | Banner rags thicken along the arena edge (visual only; no damage, no wall). The count quickens. To keep reaction time fair at 0.9 s per beat, in P3 the Planted Standard's ring decal appears and the file's arms rise on **beat 1** (as Close up's ridges already do), so every P3 attack is shown ~1.8 s before it lands | Its Planted Standard and sweep leave mud patches (3 m) that apply a standard slow (30%, 3 s) to anyone standing in them; patches last two counts | Keep out of the patches; the count's rhythm is the same, only faster |
| **The order** | On each phase's third beats it speaks its order (captioned) | None (flavour and tell) | — |

#### 7.1.4 Phases

| Phase | Health | Pattern | Transition |
|---|---|---|---|
| **P1, "Hold"** | 100–65% | Two files hold the Stake and Ring lanes; the General stands at the post and is shielded while either file stands. Planted Standard every second count. Clear files, then strike in the ~4-count window. | At 65% it returns to the post and **re-musters** (~8 s, invulnerable): "Close up." **The asker beat plays here** (§6 Beat 5). |
| **P2, "Close up"** | 65–30% | No shield. It moves into the targeted player's lane and sweeps on three (every second count); files in other lanes converge. Planted Standard between sweeps. | At 30% it plants its pole at the head of the Post Lane: "No one leaves." Rags rise at the edge. |
| **P3, "No one leaves"** | 30–0% | The count quickens to 0.9 s per beat. One file only (Post Lane). Sweeps and Planted Standards leave slowing mud. Still three beats; still move on two. | At **0 HP** it collapses into the ground. Its mud slides down the Post Lane into the gap. The count continues, softer: the condition (the open circle) is still there. `S05` completes. |

#### 7.1.5 Tuning, death, co-op

| Item | Target |
|---|---|
| Solo duration | 6–8 minutes for an Advanced player with cooked food. |
| Solo end state | A player who moves on two ends at 30–60% HP. No single hit above 30% max HP except the in-lane sweep (~35%). |
| Ranged parity | P1: files walk down every lane, so a ranged player must still cross and clear them. P2: the sweep covers a whole lane length, so lane ends are not safe; ranged players move lanes on two, melee players step inside the turn. Neither style has a spot the General cannot reach. |
| Death | Wake at Griefwatch (§11); return to the palisade checkpoint. The fight resets to the **top of the phase the player died in** (100 / 65 / 30%). |
| Logout | `S05` persists; the fight restarts at 100% on re-entry. |
| Co-op | Shared boss for partners on `S05`. Health scales per participant. Close up targets one player's lane at a time in rotation. The asker beat is resolved by whichever partner acts first (each partner's `MBL_ASKER` is set to that result; fallback: host). |
| Never | It never speaks a name, a unit, a place or a date. It never answers a question (Hewin's included). No Memorykeeper or Tender calls it a ghost. It drops no loot that identifies anything; ordinary non-metal material only (economy pass); no battlefield iron (MD-11). Its health bar shows no name (the folk name stays in people's mouths, not on the frame). |
| **Defeat (CDR-1)** | 0 HP. It disperses for the night. It would re-form at the next night while the circle stands open (condition), which is why the rite follows at once. After `S06`, the story General does not re-form; the Night Count (§E.9) is a separate, called encounter. |

### 7.2 Hazards

| Hazard | Where | Telegraph | Effect | Notes |
|---|---|---|---|---|
| **The third beat** | Any lane, from `S02` to `S06` | Beat 2 (~1.2 s; ~0.9 s in P3) | Only things in a file's segment or an attack's decal are hit | The count itself never damages anyone. |
| **Mud patches** | Crown, P3 only | Patch appears where a strike lands | Standard slow 30% for 3 s | Two counts' duration. |
| **Gap step-off** | The gap, `S06` | Gap ripple brightens on beat 2 | ~15% max HP and knock-back if held through beat 3 | Never costs rite progress. |
| **Iron soil** | The Iron Bend, the crown | Red ground | None. Tarnish serpents bask here (MDS06): ambient Hunting fauna that fight only if provoked | Not counted as an encounter. |
| **Dark** | The road and crown at night | — | None. Lanterns at each held bend and on the palisade | No light-gated mechanics here (those are the Chapel's, MR-M4). |

No hazard on the ridge can kill a player above 25% HP (Enemies file C-2); the gap step-off and the mud patches are clamped accordingly, and no knockback moves anyone down a slope.

## 8. The discovery moments: presentation specs

### 8.1 The count (Beat 2, used through Beat 6)

| Time / element | Spec |
|---|---|
| Hand on the ground | The player kneels beside Bran; hand flat on the turf (interact pose). Ambient drops away: wind low, no music. The first soft beat is felt (rumble, a slight camera tremble, a thin ripple ring in the grass under the hand) before it is heard. |
| The third beat | A deep thud heard as much as felt, with a heavy ripple. A cup on Bran's offering stone jumps. |
| Teaching cue | On the first three counts only, a faint caption under the hand: "one… two… THREE". Turned off after (unless the accessibility caption is enabled). |
| On the road | The ripple decal crosses the road surface on each third beat. Lane edges carry old drill-furrow lips so lanes are visible without UI. |
| What it means | The player learns the General's rhythm by touch from a man who has felt it for years and never told anyone. |

### 8.2 Who comes to the circle (Beat 6; bible §9.3 implemented)

The circle always completes. Twelve stones; named characters take stones as below; anyone beyond twelve stands at the shoulder of the person they came with; Griefwatch households fill any stone still empty. Positions are fixed so geometry and lines are authorable; flags decide who stands at each.

| Stone | Who | Arrives in | Notes |
|---|---|---|---|
| **S1, the road stone** | **Ide Larrow** (always) | Before the hold (she is there first) | With `TH_STANDING`: the Thornfell Ridge Warden pair stands at her shoulder. Hewin Collard stands at her shoulder (he came up with the wardens). With `MR_BANNERS = restored`, the Banner That Sank Twice is stood beside this stone by Corra in `S04`. |
| **S2** | **Edris Hollowmere** (always) | Segment 1 | *Lifting Day* Completed: **Oswin Garvey** at her shoulder `[CAUSEWAY]`. |
| **S3** | `MR_NAME_RECORD = qualified`: **Dunstan Hayle** (across the ring from Nell). Amended: **Corra Sallis** if `MR_BANNERS = restored`, else a Griefwatch household | Segment 3 | Corra takes the first free household stone in the order S3 → S11 → S12. |
| **S4** | **Calwen Reed-Binder** (always) | Segment 1 | `MR_CLOTH = returned`: he lays the recovered cloth folded at the foot of his stone. |
| **S5** | **Mara Fenholt** (always) | Segment 1 | |
| **S6** (left of the gap) | **Bran Hollowstep** (always) | **Last** | Stands at the palisade the whole rite, watching. Walks down when every other stone is filled. |
| **The gap** | **The player** | — | |
| **S7** (right of the gap) | **Ysolde Haverel** (always) | Before the hold (she takes the roll here) | Reads the roll. |
| **S8** | **Mabyn Coyle** (always) | Segment 2 | |
| **S9** | **Lysa Thornettle** (always) | Segment 2 | **Jory Wick** at her shoulder, hands over his ears through the count; he lowers them when it stops. |
| **S10** | **Nell Ferrow** (always) | Segment 2 | Qualified: **Agna Ferrow** at her shoulder (lame on wet ground; Nell holds her arm). |
| **S11** | Amended: **Dunstan Hayle** (beside Nell). Qualified: Corra if restored, else a Griefwatch household | Segment 2 | |
| **S12** | `MR_ROWAN_TRUST = told`: **Rowan Mirewake**. Kept: Corra if restored and not yet placed, else a Griefwatch household | Segment 3 | Kept: the landing lantern below (§5.4 C5). |

**Lanterns:** `MR_LANTERN_LINE`: the Stillgrave family (MLL; role names from that package) comes up last-but-one and lights a lantern at every stone, then stands at the road stone; else Griefwatch households set the lanterns as each person arrives.

**Count check (maximum):** 8 always-stones (Ide, Edris, Calwen, Mara, Bran, Ysolde, Mabyn, Lysa) + Nell + Dunstan + Rowan + Corra = 12. Everyone else (Agna, Oswin, Jory, Hewin, the Thornfell pair, the Stillgrave family, the Bannerbearers) stands at a shoulder or at the road stone. No configuration exceeds twelve stones; the minimum configuration (kept, retired, qualified or amended) fills two stones with Griefwatch households.

### 8.3 The strange moment (Beat 6)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Bran's hand** | He sets his palm on S6, the same way he showed the player at the watchpost. |
| 0–2.4 s | **Two beats** | Beat 1 (soft). Beat 2 (soft). |
| 2.4 s | **No third** | The third beat does not come. The audio bed that has run under every scene since `S02` cuts to nothing. No sting. |
| 2.4–6 s | **Silence** | Wind only. The lantern flames stand straight up. The player can let go of the footing stone (the prompt changes to *Stand*). |
| 6–16 s | **The standards** | Along the palisade arc, one after another round the ring (from the standard nearest S1, then onward), each standard leans toward whichever person at the stones stands nearest it, slowly, and lies down flat on the turf. Nothing else moves: no grass, no flame, no cloth flutter. With `MR_BANNERS = restored`, the Banner That Sank Twice, in Corra's hands at her stone, does not move; nobody remarks on it. |
| 16 s on | **After** | Nobody speaks for about five seconds. Then Edris: "Sit a minute. Everybody." (`MBL-D7.60`). People sit down where they stand. Later, only Bran says anything about it, and only when asked: "Seen: they lay down. Thought: I've nothing." |
| UI | | Objectives and the count caption suppressed from 0 s until Edris's line. The camera stays with the player; no cutscene. |

This is one of the Mire's deliberately unexplained moments (bible §7.5): the standards lean toward people, not toward any banner, stone or direction, and no one interprets it.

### 8.4 The table (Beat 8)

| Element | Spec |
|---|---|
| Order | The meal first, then remembrance (bible §5.3 rule 6). No question is asked of the player before they have eaten. |
| Sit | Agna's line opens a forced-seat interact: the player is seated on the bench nearest the fire. Food appears in front of them (a bowl prop; the player also receives an ordinary cooked food item). |
| Barks | Table barks play in turn while the player sits (`MBL-B9`); the player can stand at any time, which ends the barks and moves the objective to the register. |
| Light | Morning. The mood banners on the raised ways are being changed back from ochre by Bannerbearers on ladders (MME01). |

## 9. Quest structure for implementation

### 9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_closure` | Go to Griefwatch's vigil hall. | Enter W2 volume + `MBL-D1` end | Yes | Quest Active on entering Sorrowmere or Griefwatch after MR-M4 Completed **and** after the player has left the Blackwater Landing area (per-player event `mbl.closure_start`; ordinary predicate: MR-M4 Completed + exit-landing-volume flag + zone entry). It cannot fire during `MCS-D11` or the landing scene. |
| `S01_roll` | Help Ysolde check her names against the vigil book (0/3). | 3 × `show_match` accepted + `MBL-D2.40` end → `MBL_names_roll` granted | Yes | Wrong matches harmless. Checks persist individually. |
| `S01b_pot` | (Optional) Bring the wardens a pot. | Cooked vigil pot or the cook's pot delivered to W1 | No | Sets `MBL_POT`. |
| `S02_count` | Find Bran at his watchpost. / Learn the count. / Wait for dusk. | `MBL-D3` end + (3 clean counts **or** MBL-E1 defeated once) + furrow inspect + keep watch to dusk | Yes | Night pin begins at dusk. The furrow inspect also sets `MDS07_SEEN` and `MDS07_READ` so the discovery does not repeat after the story. |
| `S03_road` | Climb the Bannerline road to the palisade. | Enter C1 volume | Yes | `MBL-D4` at W1 required (opens the gate). MBL-E3 optional `[MD-7]`. Checkpoint at R3. |
| `S04_standards` | Retire the standards at the heads of the lanes (0/3). | 3 × (`cut_stake` or crew saw) + `lift_pole` + `fold_cloth` | Yes | Per-standard progress persists. `MR_BANNERS = restored`: `MBL-D5` plays after standard 1; extra wave at standard 3. |
| `S05_general` | Face what stands at the muster post. | MBL-E6 defeated (0 HP) + `MBL-D6.20` end | Yes | Phase checkpoints 100/65/30%. Asker beat at the 65% transition sets `MBL_ASKER`. |
| `S06_circle` | Hold the gap. | `give_roll` + 3 × hold segments complete + 12th arrival (Bran) + strange-moment presentation end + `MBL-D7.60` | Yes | Hold progress persists through death, logout and walking away. Arrivals pause when the gap is unheld. |
| `S07_bannerline` | Say how Bannerline is left. | `MBL-D8` choice + closing lines end | Yes | Sets `MR_BANNERLINE`. Night pin ends. |
| `S08_table` | Go down to Sorrowmere. / Sit. / Lay the roll in the register. | Enter T1 + `sit` + `MBL-D9.01`–`.05` + `lay_roll` (item removed) + `MBL-D9.20`–`.40` end | Yes | Sets `MR_STANDING`; quest → Completed. Epilogue states apply (§E). |

### 9.2 Flags

| Flag | Values | Set by | Read by (here) | Read by (later) |
|---|---|---|---|---|
| `MBL_POT` | bool | `S01b` | Warden bark at R1 (`MBL-B3.2`) | — |
| `MBL_ASKER` | answered / stood / wardens | `S05` (asker beat) | `MBL-D7` (Hewin's arrival line), `MBL-D9.30` | Hewin's Marshfall epilogue bark (§E.6) |
| `MR_BANNERLINE` | quieted / tended | `S07` | `S07` closing; `S08` register line | Ridge state; Griefwatch lines; Night Count presentation; convergence (bible §9.1) |
| `MR_STANDING` | bool | `S08` | — | Mire master commissions (§E.10); CV-M1 gate |

No other region flag is set. The `S02` furrow inspect sets `MDS07_SEEN` and `MDS07_READ` (see the step table) so the discovery does not repeat.

### 9.3 Night pin

From dusk at the end of `S02` until `S07` completes, the player's presentation hour is pinned to night (the Lowmark keep-watch convention; per player; never world time). A player who logs out mid-quest resumes at night at the persisted step. After `S07` the pin is released and the next presentation hour is morning, which the walk down to Sorrowmere uses.

### 9.4 The rite's opening by custody (`MR_WARDEN_RECORD`)

| Value | Who reads the last leaf at the ring, and from what | Roll source line (Ysolde) |
|---|---|---|
| **sorrowmere** | Ysolde, from the leaves themselves in Mabyn's oilcloth (she brought them up; the lead box stayed in the crypt, Act II). She can name the five listed stones by their places as the player inspects them (inspect variant; never a count), then reads the last line: *"The circle is not closed. We could not."* | "From the Names Below, and from the leaves the Wardens left." |
| **altar** | Ysolde, from her reed copy of the last leaf. The stone list stays under the altar; she says so. | "From the Names Below. The leaves stay where Mabyn put them; I've the last line." |
| **tenders** | Mabyn Coyle, from memory: she has read the leaves aloud to everyone Rowan brought to the roof since the chapel. | "From the Names Below. Mabyn has the leaves by heart; she'll say them." |

In every value the last line is spoken at the ring before the hold begins, and the rite answers it. No line says the circle "was" anything (a calm-field, a grounding): Memorykeepers and Tenders say only that it was left open and is being closed.

### 9.5 Choices and consequences

**Choice A: the asker (`MBL_ASKER`, local)**

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Answer him** (`answered`) | Hewin stops. "Books." He goes back to the wardens' line. | The player speaks during a fight. Nothing mechanical. | At the meal he asks Ysolde for the books himself. Marshfall epilogue: he sits with the Hayle book "learning how it's done". |
| **Stand between** (`stood`) | He stops behind the player and does not look at the thing again. | Standing in the Post Lane's head at the re-muster: the player begins P2 already in a lane (the first sweep's lane). | At the circle he says "You stood in front." At the meal Ysolde offers the books; he takes them. |
| **Neither** (`wardens`) | Ide pulls him back. | None. | Ysolde offers the books at the meal. Same search, same "not found". Nothing is lost. |

**Choice B: how Bannerline is left (`MR_BANNERLINE`)**

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Quieted** | Mara walks the palisade foot and chooses a fallen footing stone for the gap; the wardens roll it to the ring. Calwen folds the fallen standards; the households lay them in the earth inside the ring and Mara turfs them. Ide takes the slate off the closure gate. | The crown is empty. Griefwatch's vigil over the ridge ends; Griefwatch must find what it is for. The standards are gone from sight for good. Corra (restored) carries the Banner That Sank Twice back down to the vigil hall alone. | The circle is closed by a stone with no mark. The road is open to anyone. Bran returns to his watchpost: "Nothing to watch. I'll watch it anyway." The Night Count can still be called (§E.9). |
| **Tended** | Ide cuts a step into the footing stone with a mattock, ankle-deep. Calwen and the Bannerbearers carry the standards down to Griefwatch. A Griefwatch keeper stands the first vigil in the gap that night. | A keeper on the crown every night from now on: Griefwatch's labour, for good. The road is open under watch; travellers are counted up and down. | The standards return within days re-made in community colours (grey, green and ochre cloth stitched over the old, which is kept inside) and are raised on the crown as vigil banners. Bran stands some vigils. The player can take a vigil (§E.1). The Night Count can still be called. |

**Every outcome:** the circle is completed and the count stops for the story. The General does not push out along Bannerline again. The road opens. The roll is read and goes into the register. Hewin's father is searched for and not found, and the search is written down. `MR_STANDING` is set.

## 10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| `MR_STANDING` | Standing | The Mire's regional standing: opens the master commission offers (§E.10) and counts toward CV-M1. |
| The Bannerline road | Access | Open in both outcomes (watched in `tended`). The crown, the palisade and the circle are revisitable. |
| The Night Count | Access (repeatable encounter) | `[MD-8]` Strike the muster post at night to call the General (§E.9). Ordinary combat rewards only (Gameplay Designer; economy pass). |
| The witness's place | Standing (non-mechanical) | At Sorrowmere's long table the player is always given a seat and food (Agna's bench). |
| Small payment | Currency | A Marshwarden's due for "a night on the road", paid by Ide at Griefwatch afterward (economy tuning). |
| Skill XP | Action only | Melee or Ranged; Woodcutting for cut stakes; Cooking for the optional pot. **No lump quest XP** (bible §11.6). Values `[GD]`. |
| Cooked food | Item (ordinary) | The vigil pot's portions (if cooked); a bowl at the meal. Catalog items per the economy pass. |
| Post-quest world | Story | Epilogue states (§E). |

## 11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Wrong match at the vigil book | Ysolde's gentle correction; no penalty. |
| Mistiming the count | Knockdown and damage only; never lethal at full health from a single file strike. |
| Death anywhere on the ridge | **Wake at Griefwatch's vigil hall** with the quest Active and the step unchanged (bible §10.1). A warden at the closure gate offers "Back up?" and walks the player to the last ridge checkpoint reached (standard checkpoint return with a short escorted walk presentation). Completed bends stay held by the wardens (their files do not re-form for this player). Retired standards stay retired. The General resets to the top of its current phase. Rite progress and arrivals are kept; attendees wait at their stones. |
| Logout | Restore to the persisted step at night (if pinned). Mid-road: at the last bend reached. Mid-boss: the palisade, boss at 100%. Mid-rite: at the gap, segments and arrivals as left. |
| Walking away | Quest stays Active at the persisted step. Resume hooks: Ysolde in the vigil hall (`S00–S01`): "The roll's on the table where you left it." Bran at the watchpost (`S02`): he puts his hand on the ground again and waits. Ide at the closure gate (`S03–S07`): "Road's still shut. You're still the one I'd open it for." Agna at the long table (`S08`): "Sit." |
| The ridge and the world | The night pin, the count and the files are per-player quest-local state. Other players on the ridge see an ordinary closed road (if they have not reached MR-M5) or their own state. |
| Fail state | None. |
| Co-op | §7 rules. Each partner gives their own roll and holds their own gap stone presentation (the gap is per-player; fallback: the host's gap stone, arrivals and crown props are shown (MI-CO-06, pending Director review); the host's hold drives the shared arrivals and every partner present is credited per segment, each with their own roll item consumed at their own `S08`). Each partner chooses their own `MR_BANNERLINE`; fallback: the host's ridge props are shown, each partner's own value is stored and drives their epilogue. |

## 12. Integration needs

Documented dependencies for a later Systems Engineer. None is implemented here. **CDR-4 review (2026-11-08):** all three needs first drafted as new are ordinary systems in a new arrangement, and are listed as such. The count is one repeating encounter timer that broadcasts its tick; files are patrol-path enemies that advance one waypoint per tick-3 event with an ordinary telegraphed ground attack; the gap hold is the Lowmark kept-progress channel, where releasing simply pauses it, and the arrivals are scripted on the channel's active state. No bespoke runtime is required.

| Need | Owner | Minimum viable form | Justification / fallback |
|---|---|---|---|
| **The count: an encounter timer** (standard) | Systems + audio | A per-encounter metronome that emits beat 1/2/3 events at a configurable interval (1.2 s, 0.9 s), which AI, decals, audio and captions subscribe to. Active per player from `S02` to `S06`. | Every telegraph in the act keys off it; it is an ordinary boss timer exposed to several listeners. Fallback: each encounter runs its own timer at the same interval, started together. |
| **Lane movers** (standard) | Systems + AI | Patrol-path enemies with four waypoints per lane: advance one waypoint on each beat-3 event and use an ordinary telegraphed ground attack on their segment on arrival; respawn at the lane head on the next beat 3 after defeat (condition re-form, standard spawner). | Files are the core of the Mire's rhythm fight, built from patrol, spawner and telegraph systems that already exist. |
| **Shield by condition** | Gameplay | Damage reduction on the boss while any tagged file is alive; mud-plate visual. | Standard boss add-shield. |
| **Gap hold with step-off** (standard) | Systems | The Lowmark kept-progress channel, three segments: releasing it (stepping off) keeps progress, as every kept-progress channel already does; the scripted arrivals advance only while the channel is active. | The rite's mechanic. Fallback: three separate channel segments with arrivals scripted between them; files then arrive only between segments. |
| **Scripted arrivals and placement from flags** | Systems + NPC | Up to ~20 NPCs walk the road head to fixed stone or shoulder marks per §8.2, each triggering a bark on arrival. Per-player placement sets. | Same family as Thornfell's Assembly placement. Fallback: NPCs spawned at their marks with a fade, barks in order. |
| **Strange-moment prop sequence** | Systems + animation | ~9–12 standard props along the palisade, each with a lean-and-lie animation toward a precomputed nearest stone, triggered in order; audio bed cut on the 12th arrival. | Presentation only. Fallback: standards lie down in order without the lean. |
| **Asker beat** | Systems | During the boss's invulnerable transition: a non-hostile NPC runs a path; a talk prompt on him and an interposition volume both resolve the beat; timeout hands him to Ide. | Standard interact and volume. Fallback: bark-only beat; `MBL_ASKER = wardens` by default; the talk option moves to `S06` start. |
| **Vigil-book page turning and show-match** | UI | Read-in-place book with paged entries; dialogue options gated on the open page. | Lowmark/Thornfell show-evidence convention. |
| **Woodcutting interaction on a world stake** | Systems | Skill-checked channel (level `[GD]`) with a crew-alternative NPC action that takes two counts. | Standard skill interaction. |
| **Fold sequence** | Systems | MR-M2's three-step fold, no channel between steps. | Reuses MR-M2's implementation. |
| **Night pin** | Systems | Quest-local presentation hour pinned per player (Lowmark keep-watch). | Bible §9.4 convention. |
| **Forced sit and meal** | Systems | Seat interact with barks in sequence; stand to skip. | Standard. |
| **Quest item `MBL_names_roll`** | Schema | Non-droppable document with inspect text (dialogue file D-1); consumed at `S08`. | Mire item 4 of 4. |
| **Epilogue state presentation** | Systems + art | Per-player props keyed on `MR_BANNERLINE`, `MR_BANNERS`, `MR_WARDEN_RECORD`, `MR_ROWAN_TRUST` (§E). | Lowmark per-player prop fallback. |
| **Night Count entry** `[MD-8]` | Systems | Interact with the muster post at night (player hour) starts MBL-E6 as a repeatable encounter without story beats. | §E.9. |
| Creatures | Schema / Gameplay | Earthen Echo file (and weak variant), Banner Wraith, wraith bearer, Hollowfoot wanderer and shouter `[MD-7]`, the General. From the Batch 4 enemies package. | — |
| **Act I/II dependencies** | Act authors | (1) MR-M1: the mother is Aldith Hayle in the Hayle book (checked against the Act I draft, 2026-11-08). (2) MR-M2: the Banner That Sank Twice hangs over Griefwatch's vigil-hall door with Corra when `restored` (checked against the Act I draft). (3) MR-M4: the stone list on the Warden leaves is fixed by Act II §B8.4 (five stones named by place, then a broken corner; no marks, names or count beside any stone); §5.4 C4 and the `MBL-I` stone inspects follow it. (4) Act I reads promised here: `MNS_FENWARD_VISITED` (Jory's nod) and `MBR_CORRA_CORNER` (Corra's line). The leaves travel in Mabyn's oilcloth, not the lead box (Act II §B6 Beat 8). | Fallbacks in text. |
| **Batch 3 dependencies** | Side-quest authors | `MDS07_READ` name; the Stillgrave family's role names (MLL); *Lifting Day*, *A Table for the Wet*, *The Bell Roster* completion conditions. **Settled:** the `S02` furrow inspect sets `MDS07_SEEN` and `MDS07_READ` (§9.1, §9.2), so the discovery does not repeat. | Fallback: role names. |

## 13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **What the General is** | The field's command, fear and obedience pressed into one imprint by the grounding (H17, FT-02c). | A commander who would not die. | It repeats three orders and answers no one; it forms where the standards stood; the leaves' date and the ridge (Ysolde's reading, said to be hers). | It is a real general's ghost; it can be bargained with. | Which armies; whose commands. | MR-M4 (R08) truth; MR-M5 consequence. Never stated as a system. |
| **What the circle did** | Anchored the Memorywardens' calm-field; left open when they did not come back down. | "An old mourning ring that was never done properly." | The leaves' last line; the count stops when the ring is filled. | Closing it destroyed the General; the community "did magic". | How it worked. Nobody explains it. | Never (dormant magic; bible §11.8). |
| **Why the standards lay down toward people** | Unexplained. | — | The strange moment. | They "chose" someone; the dead were present. | Everything. | **Never** (bible §7.5). |
| **Where Hewin's father fell** | Unknown. | — | Register search: not found; written. | The General knows. | The answer. | Never. |
| **The furrow** | The Sorrowback's trail. | "Something big walks there when there's fighting." | The furrow; Bran's warning. | It is the General's work. | The creature. | CV-M2. |
| **The boy who carried water** | Osric Peale may be the vigil book's "and a boy". | — | One hold. | He is certainly the boy. | Proof. | A later Register case may add a hold (not authored). |

## 14. Open decisions

1. **MD-7 (Hollowfoot as enemies)** [PROPOSAL — DIRECTOR]: MBL-E3 is the only Hollowfoot fight in the act. It is optional, off the required route and carries no evidence. Swap note in §14.1.
2. **MD-8 (the Night Count)** [PROPOSAL — DIRECTOR]: the post-story refight is called **the Night Count**, never "the Muster" (Lowmark's Act III boss). If the Director prefers no refight, delete §E.9 and the muster-post interact; nothing else changes.
3. **§9.3 overflow** [PROPOSAL — DIRECTOR]: the placement in §8.2 assigns fixed stones so lines and geometry can be authored. Corra takes the first free household stone; Agna, Oswin, Jory, Hewin and the Thornfell pair stand at shoulders. If the Director wants Oswin on a stone of his own, he takes the first free household stone after Corra.
4. **The asker** [NEW]: Hewin Collard is a new minor NPC. The bible's "a Marshfall man" is kept anonymous in role but needs a name for the meal and the epilogue. If the Director prefers him unnamed, use "a Marshfall fowler" in every line.
5. **Hollowfoot reaction to "bright"**: the dossier says Hollowfoot react to bright banners. Implemented as flavour only (standard aggro and assist radius), not as a gear-visibility system (CDR-4). Recommendation: keep it that way.
6. **The Banner That Sank Twice at the strange moment**: it does not lean. Recommendation: keep it still and uncommented, so the moment stays about people.
7. **No season change.** Thornfell had the thaw; the Mire's first dry stretch belongs to *Lifting Day* (MLD), which this act does not pre-empt. The long wet continues in the epilogue.

### 14.1 MD-7 swap note

If the Director rules that Hollowfoot appear only as non-combatant survivors: **MBL-E3 becomes a survivor beat.** Three drifters sit among the rags in the Rag Bend hollow, rocking to the count. They are non-hostile and never targetable. The player can pass on the road, or step down and **sit with them** (interact, ~3 s; `MBL-B3.6` alt line), which makes them get up and walk slowly down the road toward the wardens' brazier, where a Griefwatch carer takes them to Lysa. No XP, no loot, no flag. Remove the Hollowfoot entries from §7's table and from the Batch 4 creature list for MR-M5. Nothing else in this act changes: no step, flag or evidence depends on MBL-E3. Jory Wick and Lysa's lines are already non-combat and stand as written.

## 15. Internal review log

| Finding | Revision |
|---|---|
| The rite risked being a cutscene after the boss. | The hold is played: three segments, step-off rhythm, arrivals paced by the player's hold. The circle is the climax; the boss precedes it (bible order). |
| The count risked being unreadable without audio. | Ground-ripple decal, body poses on beat 2, optional rumble and caption. Every attack lands on three and is shown on two. |
| The count risked copying Lowmark's four-knock Muster. | Three beats in the ground; the counter is to step off, not toward a stone; no pull toward water. |
| The strange moment risked mirroring Lowmark's "every stone at once". | One after another round the ring, toward people; no light, no water. |
| The General risked speaking, naming or answering. | Three orders only. The asker's question is never answered. No Memorykeeper or Tender calls it a ghost. |
| Ranged risked trivialising the boss from the lane ends. | Lane sweep covers the whole lane length; files walk every lane; Planted Standard ring. Ranged moves lanes on two. |
| The asker risked being hurt. | Non-combatant, never targetable; attacks never resolve on him; Ide pulls him back on timeout. |
| Hollowfoot dignity (MD-7). | One optional group, avoidable, no named or known person among them; Lysa's settled man Jory Wick is a non-combatant at Griefwatch and the ring; no NPC treats a fight as a cure; swap note §14.1. |
| The roll risked stating a count or a Memorywarden's name. | No number is read or totalled. The leaves' tally marks are never counted and the stone list is cited by place only (Act II §B8.4); those who went out are covered by "held, not yet known". No army, unit or Warden is named. |
| The roll risked reading a name on one hold. | The player performs the rule: Osric Peale's name is known and is not read as his. |
| Bran's ledger limits. | He knows the count by feel and the unsafe ground; he never claims to have been at the last battle; no theatre or date. His stepping to the last stone is an action, not testimony. |
| Edris's ledger limits. | She speaks for her own care and for sitting down; never for the dead or for what the land wants. |
| Calwen / Mara limits. | Calwen folds and lays; never names a side. Mara chooses a stone and marks it with nothing. |
| Rowan limit. | Comes only if told; never crosses at night to do it (he walks up by the road from Griefwatch, having come up by day). Kept: he keeps the landing lantern. |
| Sennic. | Not present at the ring (he does not climb; bible §9.3 does not list him). One table bark at Sorrowmere, a story, marked as his. |
| Thornfell independence. | `TH_STANDING` adds two allies and two lines. Never required; no route named. |
| Sorrowback. | Trail and Bran's warning only. Never followed. Not an encounter. |
| Quest items. | One (`MBL_names_roll`); Mire 4 of 4. |
| Three states. | No fail; every step persists; the circle always completes; a beaten player wakes at Griefwatch with the step unchanged and is walked back up. |

---

# E. Mire epilogue states

This section is the single reference for how MR-M5's outcomes change the Mire after `MR_STANDING`. Everything here is **per-player presentation** (bible §9): props, NPC positions and barks keyed on the player's own flags, with the Lowmark per-player prop fallback. Barks are in the dialogue file Part 7 (`MBL-B11` onward). No epilogue state removes access to any site or service.

## E.1 Bannerline crown [MP12]

| Element | **quieted** | **tended** |
|---|---|---|
| The gap | A new standing stone, a little greyer than the others, no mark. | The footing stone with an ankle-deep step cut into it. A **vigil keeper** (Griefwatch household, role name) stands in it each night with a lantern. |
| The standards | None standing. A low green mound inside the ring where they are laid. Turf grown over by the next visit. | Raised along the palisade arc in grey, green and ochre cloth; old cloth kept inside. They hang still (laid state, honoured). |
| The lanes | Drill furrows only; no ripple. | Same. |
| The muster post | Stands alone. Inspect: "Iron-shod. The crossbar worn smooth. Quiet." | A keeper's rope is tied round it, marking where the vigil walks. |
| Taking a vigil | — | Optional repeatable: at night, ask the keeper for the gap; keep watch until morning (Lowmark keep-watch). The keeper brings tea at midnight (`MBL-B11.4`). No reward beyond a bark and the night passing. |
| The Night Count | Available (§E.9). | Available; the keeper steps off the gap first (`MBL-B11.5`). |

## E.2 Griefwatch [MP03]

| Element | **quieted** | **tended** |
|---|---|---|
| Closure gate | Open, slate removed; the gate tied back. | Open; a warden at a slate counting travellers up and down: "Up: 3. Down: 3." |
| Vigil hall | The bell rings for ordinary vigils only. Ide teaches bell-keepers' children their letters at the long table: Griefwatch is finding out what it is for. | The bell rings each dusk as the keeper goes up. The vigil book has a new column: *Gap kept by*. |
| The Banner That Sank Twice (`MR_BANNERS = restored`) | Back over the vigil-hall door. Corra keeps it alone. | Back over the door. Corra goes up with the vigil banners on feast days. |
| Ide | "Road's open. I keep looking at it." | "Road's open, and watched. That's the closure I wanted." |
| Jory Wick and Lysa | Jory sits by the gate in the afternoons; he waves at people going up. | Same; he has asked to stand a vigil, and Lysa is thinking about it. |

## E.3 Bran's watchpost [MP17]

| Element | **quieted** | **tended** |
|---|---|---|
| Bran | Back at the watchpost. A new offering on his stone: a folded scrap of standard cloth. | At the watchpost by day; on the crown some nights, standing the gap. |
| The furrow (MDS07) | Bran, asked: "Still there. Still not tonight's trouble." (seed for CV-M2, all outcomes) | Same. |

## E.4 Sorrowmere [MP01]

| Element | All outcomes (variants as noted) |
|---|---|
| Names Below | The roll bound in at the back of the register. The last line reads "which is closed" (quieted) or "which is kept" (tended), with "Witness: the stranger's seat." |
| Long table | The player always has a seat and a bowl. Agna: "Sit." |
| Mood banners | Back to their week's colours. On the anniversary each year (presentation: first visit after a long absence), green and grey together. |
| Nell | Amended: signs the register's visitors' line "Nell Ferrow, born Linnet Hayle". Qualified: signs "Nell". She hums the lullaby once while carrying water; nobody comments (bible: never explained). |
| Ysolde | Teaches the children's story circle (MME08) the water-carriers' names: "Say whose story it is." |

## E.5 The Field of Fallen Standards and the causeway [MP07, MP08]

| Element | `MR_BANNERS = retired` | `MR_BANNERS = restored` |
|---|---|---|
| The field | Quiet. Laid standards only. | Quiet. Griefwatch's banner is visible on clear days far off (MAP VERIFICATION REQUIRED; else omit). |
| Causeway crews `[CAUSEWAY]` | Oswin's crews work the causeway without lifting anything they find; they call Mara. | Same. |

Neither `MR_BANNERLINE` value changes the field.

## E.6 Marshfall [MP02]

| Element | Variants |
|---|---|
| Dunstan Hayle | Amended: the Hayle book has Nell's name written in beside Linnet's. Qualified: it has a ribbon at Linnet's page. |
| Hewin Collard | `MBL_ASKER = answered`: at Dunstan's table with the Hayle book, "learning how it's done". `stood`: at the jetty, mending a net; he greets the player first. `wardens`: same as stood, a beat slower to look up. In all: "Not found. It's written. That's more than I had." |

## E.7 Rootrest and the Fenward [MP04, MP05]

Lysa: "He sleeps through now." (Jory, all outcomes.) The Fenward huts take two more drifters who walked down off the ridge after the count stopped (non-combatant NPCs; `[MD-7]`-safe in either ruling).

## E.8 Blackwater Landing and the Chapel [MP06, MP13]

| Element | Variants |
|---|---|
| Rowan | Told: "Walked up a hill at night. Don't tell anyone." Kept: "Saw your lantern go round the ring. I kept mine." |
| The Warden leaves (`MR_WARDEN_RECORD`) | Sorrowmere: on the register room's reading stand, a reed slip tucked into the leaves' oilcloth: *Closed* / *Kept*. Altar: Mabyn says one prayer at the altar for the circle. Tenders: the roof-loft reading now ends with "and then it was finished, by people who came up the road." |

## E.9 The Night Count `[MD-8]`

The General remains a canon major threat. After MR-M5, at night (player hour), the player can **strike the muster post** (interact) to call it. It is never called "the Muster".

| Element | Spec |
|---|---|
| Entry | Interact with the muster post at night. Confirmation text: *"Strike the post. The count will answer."* With `tended`, the vigil keeper steps off the gap first. |
| The fight | MBL-E6 without story beats: no asker, no rite. Same phases, telegraphs and count. Tuning may be raised for the refight (Gameplay Designer). |
| Defeat | 0 HP; it collapses into the post's foot. The count stops on its own after defeat (the circle is complete). The ridge is quiet until the post is struck again. |
| Ridge state | `MR_BANNERLINE` changes the props and lines around the fight (§E.1), not access to it. |
| Rewards | Ordinary combat rewards; any unique drop belongs to the economy and item passes and is non-metal (no battlefield iron, MD-11). Nothing evidentiary. |
| Death | Respawn at Griefwatch; ordinary. |

## E.10 Mire master commissions

`MR_STANDING` is the Mire's regional standing (bible §9.1), the narrative-legitimacy step for its master commissions, extending the approved aspirational-commission pattern. This package authors only **who offers what, where, and the offer line** (dialogue file Part 8). The offer opens a commission; it grants nothing. Skill thresholds, materials (reed shafts, fen fowl and root wood are proposals for the economy pass, MD-11), stats and steps belong to the economy pass. There is no Mire Smithing commission (MD-11: no ore, no forge). Names are functional placeholders [NEW].

| Commission (functional name) | Giver | Where | Skill line | Variant |
|---|---|---|---|---|
| **Fowler's reed bow and quiver** | Hob Merrit | Marshfall | Fletching / Ranged / Woodcutting | *Reed Shafts* Completed: he remembers the heron that got away. |
| **Root-wood pole** | Rowan Mirewake | Blackwater Landing | Woodcutting (root-knee) | Told: "I'll show you where the good root is." Kept: "There's root. Find it." |
| **Marshwarden's oilcloth coat** | Ide Larrow with a Griefwatch leatherworker | Griefwatch | Leatherworking (imported leather; repair craft) | Tended: "For the vigil. It's cold on that stone." |

None depends on `MR_BANNERLINE` beyond one line. Every player who completes MR-M5 receives all three offers.

## E.11 What every ending shares

The circle on Bannerline is complete, closed or kept, and the count has stopped. The General does not push out along the standards again; it can still be called to the muster post by anyone foolish enough to strike it at night. The road is open. The roll was read at the ring, with names only where two keepers stood behind them, and it is in the Names Below. Hewin's father is not found, and the search is written. Bran still watches the furrow and still says it is not tonight's trouble. Nobody in the Mire says what the circle did, what the General was made of, or which armies stood on the field; they say that people came up the road and stood at the stones.

---

# Act III review log (cross-package)

| Check | Result |
|---|---|
| Brief compliance (bible §6.1 MR-M5) | Offer (automatic after MR-M4 at Sorrowmere or Griefwatch; bell; Ide's closure; Bran down from his watchpost); beats 1–6 in order: Bran's warning and the count, the furrow ("not tonight's trouble"); road up with Hollowfoot (MD-7, optional) and Echo files on the count, Marshwardens behind, Thornfell pair with `TH_STANDING`; three ridge standards retired under the count, Corra and the Banner That Sank Twice with `restored` (harder retirement, one more wave, one more ally line); the General at the muster post, three orders, the Marshfall man's question unanswered, the player's tool beat, defeat at 0 HP, mud to the gap; the circle with the gap stone held in three segments, §9.3 attendance, step off on two, roll read by Ysolde with two holds, the Hayle mother by `MR_NAME_RECORD`; the strange moment as written; choice `MR_BANNERLINE` quieted / tended as written; meal first at Sorrowmere, Agna makes the player sit; `MR_STANDING`; the Night Count. |
| Boss brief (§10.1) | Arena, count, three phases ("Hold" shield, "Close up" lane convergence and in-lane strike, "No one leaves" quickened count and slow), defeat and failure as written; never speaks a name or answers. |
| Combat (CDR-1/2) | Everything to 0 HP; earth-memory re-forms by condition only; no SX; melee and ranged both viable at every encounter; ranged never required. |
| Evidence rule | Roll from register + vigil book (two custodians); Warden leaves read in custody voice; combat reveals nothing. |
| Canon and ledger | General (C15), Sorrowback trail only, Bran, Edris, Calwen, Mara, Rowan (never at night by water), Lysa, Sennic (not at the ring). R08 withheld items never stated. |
| Region flags | Reads only §9.1 flags plus `TH_STANDING`; sets `MR_BANNERLINE`, `MR_STANDING`. Quest-local `MBL_POT`, `MBL_ASKER`. |
| Quest items | `MBL_names_roll` only (Mire 4 of 4). |
| Tags | `[CAUSEWAY]` on Oswin's nodes; `[MD-7]` on MBL-E3 and its barks; `[MD-8]` on the Night Count. |
| Map | Relative only; MAP VERIFICATION REQUIRED in §5 and at two sightlines; no route to another region; no compass direction. |
| Scope | No schema, JSON or C#; no new runtime needs after the CDR-4 review (§12: timer, patrol-path files and a kept-progress channel are standard). |
| Independent review, 2026-11-08 (Act III and cross-act) | Fixed: stone inspects and C4 now follow Act II §B8.4 (place-named stones, no marks; nothing countable); leaves carried in Mabyn's oilcloth, not the lead box; the vigil book dated "the last wet" with fog on its last loud and quiet nights, matching the weather run (Act I day-books, Act II vestry log), not "the last summer"; Act I's promised reads added (`MNS_FENWARD_VISITED`, `MBR_CORRA_CORNER`); ring interior closed as a safe firing spot by an ordinary leash; Close up reaches turf strips; P3 Planted Standard shown from beat 1 (~1.8 s); file collapse inside the ring (was "outside", which a gap crossing cannot reach); Ysolde placed before the hold; household minimum corrected to two; Bran's watch no longer dated ("for years", Part 4 ledger); Sennic's bark no longer implies the ridge was loud in his childhood (war ended ~30 years ago); Hob Merrit's pronoun matches Act I; three runtime needs reclassified as standard (CDR-4). Checked and consistent: flags (bible §9.1 has `MR_CLOTH`, `MR_LANTERN_LINE`, `MR_STRANGER_SEAT`; `MDS07_READ` and the side-quest completions remain Batch 3 dependencies), four quest items, Aldith Hayle, banner over the vigil-hall door, cast and roles, 0 HP and the General's quieting by rite, MD-7 tagging and swap note, the Night Count naming, new names (no repo collisions). |
| Batch 4 encounter alignment review, 2026-11-09 | Aligned with `Enemies/Caelmor_Mire_Encounter_and_Enemy_Requirements.md` §13.3 (numbers and text only; no id, step or flag renamed): MBL-E5 bearer uses the interruptible Raise (2.0 s, 8 m, 10 s) in Beat 4 and §7, Plant ring decal from beat 1 (C-4, I-7); P3 file arms rise on beat 1 and §7.1.2's rule says so (C-7, I-12); §7.1.5 "Never" row and §E.9: non-metal drops only, no battlefield iron (I-21), boss bar with no name (C-9, I-18); §7.2 adds the 25% hazard clamp (C-2, I-22). §12 Batch 3 row no longer asks whether `S02` sets `MDS07_READ` (it does, §9). **`mbl.closure_start` gate:** MR-M4 completes at `S08_landing` on `MCS-D11` end at Blackwater Landing, so the zone-entry event could have fired while the landing scene was still playing (and the Memorykeeper's "at first light" contradicted Ysolde being at the landing that morning); activation now also requires leaving the landing area (ordinary predicate), stated in the card, Beat 0 and `S00_closure`; "at first light" dropped from Beat 0 and `MBL-B0.2`. |
