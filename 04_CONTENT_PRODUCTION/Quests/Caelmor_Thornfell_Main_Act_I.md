# Thornfell Main Questline, Act I: The Closing of Passwatch, The Iron Winter Stores

**Status:** Authored production content for Creative Director milestone review. This package implements Thornfell main milestones TF-M1 and TF-M2 (bible §6, §6.1), which carry Act I from the player's arrival at Passwatch to the Act I turn. It follows the Lowmark act-package format (`Caelmor_Lowmark_Main_Act_I.md`). Everything marked **[NEW]** is authored and not canon until the Director promotes it. Everything marked **[PROPOSAL — DIRECTOR]** rests on an open bible §3 decision (TD-1 to TD-14). **[CANON]** items come from Phase 1 or the reconciled `LORE/` files. **[APPROVED — id]** items rest on an architecture ruling. No schema, production JSON or C# is created here. This is Thornfell milestone content: an internal production milestone, not a release boundary (CDR-3); nothing here authorizes release scope. Combat follows the Director rulings of 2026-11-03 (`Caelmor_Director_Rulings_Combat_Ranged_Release.md`): every enemy is defeated at 0 HP (CDR-1), and every fight accepts melee or ranged (CDR-2).

**Controlling document:** `04_CONTENT_PRODUCTION/Quests/Caelmor_Thornfell_Narrative_Production_Bible.md`. Its §6 table and §6.1 briefs are binding and are implemented as written. Where this package adds detail, it is marked [NEW] and stays inside the bible's cast, places, flags and rulings.

**Companion file:** `04_CONTENT_PRODUCTION/Dialogue & Narrative/Caelmor_Thornfell_Main_Act_I_Dialogue.md`. It holds cast notes, every dialogue node referenced here (`TPW-`, `TIW-` prefixes), barks, inspect texts and the full text of every document (Vessa's slate, the haulier's chit, the broadsheet, the store ledger).

---

## Act I header

### What Act I does

The player arrives in Thornfell as a stranger and leaves Act I knowing that someone in Thornfell is preparing for a war nobody declared. Act I's job is to make the player competent in Thornfell's readable system (sound) and then turn that competence on a hidden thing: a full store-house that should be empty. It gives the player a reserve, a ledger and a name for the hoard (*the Iron Winter*), but not the hand that signs for it.

| Quest | The player learns | By doing |
|---|---|---|
| TF-M1 **The Closing of Passwatch** | How Thornfell closes a gate: by horn, by count, by weather. The six Ordinary Calls. That Thornfell writes down what it closed and not who it left outside. That someone is storing grain "up the track". | Answering calls at the horn post, rebuilding a rope bridge between gusts, and bringing one load through before the last Close. |
| TF-M2 **The Iron Winter Stores** | A Thornfell splinter is filling a wartime store with grain, iron and horn plates on nobody's authority. Some of that grain is Lowmark relief grain. The splinter calls it the Iron Winter, "for when Emberholt comes for the passes". | Tracking sledge marks up a cliff, climbing an old hoist shaft into a store that should be empty, reading its inventory, and deciding how Brynjar Korr learns and what happens to the hoard. |

**Act I turn (Arcs §3.1, Thornfell movement 2):** the misunderstanding ladder moves from "Emberholt is buying up the passes" to "a Thornfell splinter is arming on its own" (bible §8.3). The last thing the player sees in Act I is the first snow falling on Stonewake's ridge-market while Elira counts sacks that are not enough, whichever way the stores went.

### Dependencies on earlier content

Thornfell has **no quest prerequisite** (bible §6, §11.12). Lowmark completion is never required. Lowmark state is read only for optional variant lines.

| Lowmark state read | Read by | Effect |
|---|---|---|
| `LM_CIVIC_STANDING` | TF-M1 `S00_arrive` | A caravan hand's farewell line at the Passwatch gate (`TPW-B0.1`). Nothing else. |
| `lowmark.main.02_short_measure` Completed | TF-M1 store-yard sack inspect; TF-M2 grain-gallery inspect | Inspect addition: the player recognises the Crestbridge tally notches. Never a gate. |
| `lowmark.main.04_night_flush` Completed | TF-M1 offer option ("the Whinstone Store"); TF-M2 ledger inspect and Bersi option | Optional recognition: the account name and "sixty-eight measures" (the two-halves connection, R05). Never a gate. Never states how the grain came. |

### Region flags (bible §9.1 only)

| Flag | Act I role |
|---|---|
| `TH_CALLS` | **Set** by TF-M1 (`S01_calls`). Turns on call glyphs everywhere. |
| `TH_PASSWATCH_ROUTE` = sledge / caravan / split | **Set** by TF-M1 choice. Read by TF-M2 (Brynjar's ledger line, Elira's closing), *Nettlehook Rope*, TF-M5 posture. |
| `TH_STORES` = reported / seized / leverage | **Set** by TF-M2 choice. `leverage` is only reachable on the private route. Read by TF-M4 crew count, TF-M5 crew strength and Assembly lines. |
| `TH_BRYNJAR` = disowned / defended | **Set** by TF-M2 route (private → disowned; public → defended). Read by *Whose Colours*, TF-M5 placement. |
| `TH_SEASON` = autumn → snow | **Set** to snow on TF-M2 completion (bible §9.2). Presentation only. |

Act I invents no other `TH_` flag. Quest-local flags use `TPW_` and `TIW_`. Those read by later packages are listed in each quest's flags table under "Read by (later packages)".

### Quest-item budget (bible §9.5: four for all of Thornfell)

| Item | Quest | Fate |
|---|---|---|
| `TIW_store_ledger` (the Whinstone Store ledger) | TF-M2 | Kept by the player through TF-M5 (Assembly line and chip). Not droppable, not sellable. |

**Act I total: 1.** Everything else in Act I is a carry-state object (stormwood stakes, iron fittings, the guide line, a grain sack), an inspectable world object (Vessa's slate, the haulier's chit, the broadsheet, Eyvind's tuning sketches, the trial frame), or knowledge carried in flags. The reward horn (TF-M1) is a **reward tool named functionally** and waits on the item pass (bible §11.5); it is not a quest item.

### Structure check against the bible §6 core verbs

| Quest | Primary verb | Distinct from |
|---|---|---|
| TF-M1 | **repair and escort** against the clock; learn calls | Open air, weather-driven, the only bridge build and the only escort in Act I. Combat is bandits and wolves. No dungeon. |
| TF-M2 | **track and delve** (cliff dungeon); read inventory; fight through a clerk's crews | Interior, vertical, four galleries; the only dungeon and the only human assault in Act I. Investigation is in objects, not in a chase. |

No two quests share a set piece. Combat changes family across the act: pass bandits and ridge wolves (TF-M1) → Iron Winter crews and Ridge Crows (TF-M2). Sound changes job across the act: in TF-M1 the calls are *taught* and used to move people; in TF-M2 the player turns the splinter's own calls against it and meets the first sound that should not be there (the trial frame).

### Unlocks across Act I (bible §7)

| After | Unlocks |
|---|---|
| TF-M1 | *The Third Horn* (TTH), *Nettlehook Rope* (TNR), *Seam Rights* (TSR), *Stormwood* (TST), *Goat Year* (TGY), *The Bridge That Chose* (TBC), *Ash in the Snow* (TAS), *Oathkeeper's Step* (TOS); TF-M2 |
| TF-M2 | *Stormlight on the Ridge* (TSL), *First Smoke* (TFS), *The Mason's Margin* (TMM), *The Snow-Height Mark* (TSN), *Greymantle* (TGM); *A Place at Smoke Week* (TSM, also needs TNR); TF-M3 |

### Act I clocks and weather (shared conventions, bible §9.5)

| Convention | Act I use |
|---|---|
| **Keep watch / quest clock** (Lowmark) | TF-M1's **Close count**: a per-player presentation clock measured in Close calls, never world time. It advances on quest events, never on a timer, and it cannot run out (§A6, §A9.1). |
| **Wind windows** | TF-M1 (the Narrows guide line, the escort); TF-M2 (the cliff-ledge route, the hoist shaft). One rule everywhere: the fluted faces whistle up a fifth before a gust; sheltering behind a marked face is always safe. |
| **Agility triggers** | Optional shortcuts only, each with a walkable fallback (click-to-move). |
| **Channelled segments with persistence** | TF-M1 span haul; TF-M2 cage winding. Completed segments are kept. |
| **Per-player props with fallback** | The Close sky, the Passwatch tarp, the store's fill level, first snow. Co-op fallback: the host's state. |

---
---

# Part A — TF-M1 The Closing of Passwatch (`TPW`)

## A1. The quest in one paragraph

The player walks up to **Passwatch** on the day the Ridge Wardens decide to close it. An early storm is coming over Windscar, and Sergeant **Vessa Galt** will shut the gate at dusk until it breaks. Before she does, three loads are still beyond the **Narrows**, where a rockfall has cut the rope bridge: **Nettlehook's winter grain sledge**, **Ketil Rask's** ropeway crew with it, and a Stonewake-bound fur-and-iron caravan. Vessa has no wardens to spare and a stranger is better than nobody, so she sends the player to the horn post, where **Dorn Feldhorn** teaches the six Ordinary Calls the way children learn them: by being called. The player answers a Gather, takes cover on a Fall, and replies to a Lost. Ressa Highcrag passes and stops a young warden mid-interval without saying why. Down in the store-yard, sacks with a lowland relief stencil sit under a tarp chalked "W. acct.", waiting for hauliers to take them up the track; nobody says where they came from. Out on the pass the player takes the goat track over the **Blind Corners**, where bandits are using the closing to rob the stranded, and reaches the Narrows. With **Aud Hammerlee** they cut stormwood stakes, set fittings at her field anvil and run a guide line across the gap between gusts, counting echoes off the face above to know when it will shed. As the span goes up, Dorn's Close comes back off the cliffs **before he has finished blowing it**. Aud laughs too loudly. The patched bridge will carry one heavy load before the last Close, and the player decides which: the sledge, the caravan, or half of each. They bring it through under a Fall, with wolves at the beasts, and step inside as Vessa shuts the gate and writes on her slate: *Passwatch shut. Dusk. Storm.* Dorn blows **Rest**.

**What the player should remember:** the Close coming back too early, and Aud's laugh. **What the player should want next:** where the "W. acct." sacks went up the track, and why nobody writes down who is left outside.

## A2. Selection record

| Candidate | Verdict |
|---|---|
| **A. A tutorial at the horn post, then a separate bridge quest.** | Rejected. It splits learning from use. The bible wants the calls taught as play and used at once. |
| **B. A real-time countdown to dusk.** | Rejected. A timer that can run out is a fail state (bible §11.4). Replaced by the Close count: a clock made of quest events that waits on the player once the bridge is built. |
| **C. Calls taught as play → store-yard pass-by → Blind Corners → bridge build in weather (skills, crew alternative) → strange moment → load choice → escort by call → gate** (selected; the bible brief). | **Selected.** One afternoon of rising weather. Each beat uses the calls the player just learned, and the closing itself is the quest's spine. |

## A3. Canon grounding

| Element | Source | Status |
|---|---|---|
| Passwatch: Windscar outpost; smugglers and agitators move through it | Dossier §3 (Passwatch — Windscar Outpost) | [CANON] |
| Windscar Pass; rope bridges over landslide gaps; fluted faces that whistle | Dossier §V; bible §2.1 | [CANON] feature |
| Dorn Feldhorn: long-range horn codes; altered echoes; "wind tricks" | Thornfell anchors §IV | [CANON] |
| Ressa Highcrag: knows which tones caused "wrong results"; refuses certain calls; keeps the horns | Thornfell anchors §IV | [CANON] |
| Pass bandits at blind corners; ridge wolves on high trails | Bible §10; dossier ecology | [CANON] family |
| Stormwood (Woodcutting), smithing at a field anvil | Bible TD-13 (dossier legacy concepts, not catalog items) | [PROPOSAL — DIRECTOR] TD-13 |
| The six Ordinary Calls and their glyphs | Bible §9.4 | [NEW] |
| Vessa Galt, Aud Hammerlee, Ketil Rask, Three Calls Shelter, Nettlehook | Bible §5.2, §4.2 (TD-4) | [NEW] / [PROPOSAL — DIRECTOR] TD-4 |
| The "W. acct." sacks in the store-yard; no arrival stated | Bible §2.3, TD-11; FT-03 | [APPROVED — FT-03]; [NEW] detail |
| Storm closure (lifts) distinct from the season's sealing | Bible §6.1, independent review | [NEW] |
| Assembly closure practice records no one outside | Bible TD-5 | [PROPOSAL — DIRECTOR] TD-5 |

## A4. Quest summary card

| Field | Value |
|---|---|
| Working title | **The Closing of Passwatch** |
| Suggested content id | `thornfell.main.01_closing_of_passwatch` |
| Arc position | Act I entry (Arcs §3.1, Thornfell movement 1: "the wall closes") |
| Prerequisite | None (travel only). Tuned for Competent identity (TD-12). |
| Offer | Auto-offered on entering the Passwatch gate volume (`TPW-D1`), from any route. MAP VERIFICATION REQUIRED for the approach. |
| Solo / co-op | Solo-clearable. Co-op partners share bandits and wolves; the Close count, the bridge state and the load choice are per player. |
| Target length | 40–55 minutes first time |
| Combat share | ~25% |
| Dialogue share | ~15% |
| Calls, traversal, building, escort, choice | ~60% |
| Skills touched | Melee (required); Woodcutting and Smithing (optional: crew alternative for each) |
| Choices | Which load crosses first (3 options); whether to ask Vessa to write who is outside (optional, flag only) |
| Unlocks | `TH_CALLS`; `TH_PASSWATCH_ROUTE`; Passwatch hub (gate, barracks, store-yard, horn post, ridge stables); the Narrows crossing; eight side quests (Act I header); TF-M2 |
| **Anchor** (contract) | The Ridge Wardens and the horn line (Ressa, Dorn, Vessa); the highsteads (Nettlehook) |
| **World-truth row** (contract) | H11 (forced horns; Ressa's refused calls; Dorn's altered echoes); H16 (closures: "we write what we closed, not who"); H25 (the "W. acct." sacks: unsanctioned stores, partly Lowmark relief grain) |
| **Revelation role** (contract) | **Plants** R05 (the "W. acct." sacks, no arrival stated); **plants** R06 (Ressa's refusal of a wrong interval; Dorn's echo; Vessa's slate and `TPW_NAMES_ASKED`); **plants** the Third Horn (Dorn's training board, TTH). Owns nothing. |
| **Recurring evidence** (contract) | The relief sacks: seen here under the "W. acct." tarp, inspected again in the Whinstone Store's grain gallery (TF-M2), whose ledger is the independent custodian. Vessa's slate: recurs as the template the closure account replaces (TF-M5); its second custodian is the gatehouse roster. |
| **State compliance** (contract) | Inactive / Active / Completed. The Close count cannot run out. Choice recorded in `TH_PASSWATCH_ROUTE`; no fail path; resume at the persisted step with a hook at the gate (Vessa). |

## A5. The places

### A5.1 Passwatch [TP02, CANON settlement; NEW detail]

A walled outpost across the throat of Windscar Pass: one gate toward the pass, barracks, a store-yard, ridge stables and a horn post on a stone shoulder above the gate. Wind sock and pennant on the post. Smoke from the barracks flattened sideways. **MAP VERIFICATION REQUIRED:** Passwatch's inner side faces the Marches (Stonewake's road, Nettlehook's track); its gate faces the pass.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **P1. The gate** | Arrival; Vessa; the finale. | A heavy timber gate on stone posts, with a drop-bar on chains. A **warden's slate** hangs on a nail inside the gatehouse arch, chalk on a string. Old chalk ghosts under the current lines: dates and the word *Storm* many times. The gate's inner face has notches cut at child height (an old habit of measuring children; no comment). |
| **P2. The horn post** | Dorn's lessons (`S01_calls`). | A stone platform on the shoulder above the gate with a long horn on a swivel and a rack of practice horns. A **training board** nailed to the parapet: six call-shapes painted in white, one under the other, and a seventh row painted over in grey, still faintly raised under the paint (the Third Horn; inspect only; TTH seed). A brazier. A young warden practising. |
| **P3. The store-yard** | Required pass-by (`S02_yard`). | A walled yard between the barracks and the gate. Hay, firewood under cover, warden kit. In the lee of the wall, a tall stack of grain sacks under a tarp lashed down against the coming storm. On the tarp, in chalk: **W. acct.** A hauliers' sledge stands empty beside it with its runners greased. A Passwatch storekeeper sits on a crate with a tally board, not counting these. |
| **P4. Barracks and ridge stables** | Hub; epilogue. | Bunks, a hearth with a bench (the epilogue's keep-watch interaction), goats and two ridge ponies. A board of patrol pairs with one pair chalked "out" (Vessa's own patrol later in TF-M5; here, a quiet detail). |

### A5.2 Windscar Pass, near stretch [Windscar subzone]

Relative route order (bible §4.2; **MAP VERIFICATION REQUIRED**): Passwatch gate → the Blind Corners → the Narrows → Three Calls Shelter → (later) the Whinstone track → the Gatefall.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **W1. The pass road** | Travel; Close calls carry along it. | A cart road cut into the pass wall, with snow-poles. **Fluted faces** on the pass wall: vertical grooves cut into the rock in rows (Echohewn work, read by locals as "the old cutting"). They whistle up a fifth before a gust. **Shelter faces** are marked by the Wardens with a painted white bar at shoulder height. |
| **W2. The Blind Corners** [TP26] | Ambush; route choice (`S03_corners`). | Three tight switchbacks where the road doubles back under its own cliff. A stranded peddler's handcart is overturned at the second bend, bales cut open. Above the corners, a **goat track** runs along a ledge: goat droppings, a frayed hand-rope pinned to the rock. |
| **W3. The stormwood slope** | Woodcutting (`S05_stakes`). | A burned-over slope below the Narrows where stormwood grows twisted through old ash: short, dense trunks the wind has already tested. Old stumps cut at knee height (warden practice). |
| **W4. The Narrows** [TP07] | The set piece (`S04`–`S08`). | A landslide gap across the pass road, about forty paces wide. The old rope bridge hangs from the near anchors in a tangle; its far anchors are buried under fresh scree. Above the gap, a **shedding face**: a tall slab of broken rock that drops stones in the wind. **Aud's field anvil** on a cart at the near side, with a bellows, a tub, and a stack of bar stock. The **scree path** runs down into the gap and up the far side between three marked shelter faces (S1, S2, S3). |
| **W5. The far bridgehead** | The waiting loads; the choice (`S09_choose`). | The road beyond the gap, wider: Ketil's grain sledge with two goats in harness and a crew of four; the caravan (five pack beasts, fur bales and iron bar under oiled cloth, a caravan master). People sitting on their loads with their hoods up. |
| **W6. Three Calls Shelter (lower ledge)** [TP06] | Where half of each load waits in the split outcome. | Only its lower guest ledge is in view in TF-M1: a roofed ledge with a horn map painted on its back wall (inspect: TTH seed). A lantern lit. |

## A6. Player-facing sequence

### The Close count (the quest clock)

The Close count is a **per-player presentation clock** using the Lowmark keep-watch convention. It is measured in Close calls blown by Dorn from the horn post, heard everywhere in the near stretch of the pass. It never advances on a timer. It advances only on the quest events listed below. Each Close darkens the per-player sky by one step and adds sleet density and gust frequency (presentation only; wind windows stay readable at every step).

| Position | Sounds when | Notes |
|---|---|---|
| **Close I** | The player leaves the gate after `S02_yard`. | Always. |
| **Close II** | The player reaches the Narrows (enter W4). | Always. |
| *Close (crew stakes)* | Aud's crew finishes the stakes (`TPW_CREW_STAKES`). | Optional extra. |
| *Close (crew fittings)* | Aud's crew finishes the fittings (`TPW_CREW_FITTINGS`). | Optional extra. |
| **The span Close** | The span is hauled up (`S08_span`, segment 2). | Always. This is the **strange moment** (§A8). |
| **The last Close** | The escort reaches the outer road in sight of the gate (`S10_escort` end). | **Held.** It never sounds until the escort is home. |

So the count runs from three positions (player does both skill steps) to five (crew does both) before the last Close, and the last Close is reserved. The UI shows the Close glyph (two falling bars) with pips for Closes heard; the last pip is outlined and never fills until the escort is home. **The clock cannot run out.** Once the bridge is built, it waits on the player.

### Beat 0 — Walking Up (`S00_arrive`)
**Objective:** *Speak to the warden at the Passwatch gate.*
The player reaches Passwatch from any route as the sky starts to go yellow over the pass. Wardens are lashing tarps; a goat is being argued into the stables. **Vessa Galt** stands in the gate with her slate (`TPW-D1`). She looks the player over once: "Walker. You've come up on a closing day."
She explains in four lines: storm by dusk, gate shuts until it breaks, three loads beyond the Narrows, the bridge is down, she has no wardens to spare. She asks if the player can follow a horn. If they say no: "Then Dorn'll teach you. Horn post. Up the steps."
- **Variant (`LM_CIVIC_STANDING`):** a caravan hand from Lowmark, heading back down, passes the player at the gate and says farewell (`TPW-B0.1`). One line; no cargo or route is mentioned.
- **Optional option (`lowmark.main.04_night_flush` Completed):** "I'm looking for the Whinstone Store." Vessa: "Never heard of it." A haulier mending a harness by the gate looks away and goes on mending (`TPW-D1.30`; sets `TPW_WHINSTONE_ASKED`). Nobody else admits the name.
**Verbs:** arrive, talk.

### Beat 1 — The Ordinary Calls (`S01_calls`)
**Objective:** *Learn the calls at the horn post.*
Dorn Feldhorn (`TPW-D2`) teaches the six calls (bible §9.4) the way he teaches children: he blows a call and the player does what it says. Each call's **glyph** appears on screen as the player first answers it correctly, and stays on (`TH_CALLS` on completion). Lessons can be taken in Dorn's order only; each takes 20–40 seconds.

| # | Call | Glyph | What Dorn does | What the player does | If the player gets it wrong |
|---|---|---|---|---|---|
| 1 | **Gather** | three dots | Sends the player to the far end of the platform, then blows three short. | Walks back to Dorn (enter a volume at the horn). | Dorn blows it again. "Three short. Come." |
| 2 | **Fall** | dot-bar-dot | Kicks a bucket of gravel off the parapet ledge above the platform (harmless grit), blowing short-long-short as he does. | Steps under the platform's stone eave (marked with a white bar) within ~3 s. | The grit patters on the player's hood (no damage). "Under the bar. Every time. Don't look up first." Repeat. |
| 3 | **Rest** | a flat line | Blows one long. | Nothing: the player stands down; Dorn shows that Rest ends any call. | Not failable. |
| 4 | **Close** | two falling bars | Blows two long, falling. | Listens. Dorn explains counting down: "Every Close is one less. The last one, the gate shuts." | Not failable. |
| 5 | **Lost** | a rising line | Blows one long, rising, and waits. | Replies with **Answer** using the **practice horn** (the call wheel; §A12). | If the player blows anything else, Dorn waits and blows Lost again. "Lost wants an answer. Two short." |
| 6 | **Answer** | two dots | Learned in lesson 5. | Two short on the call wheel. | — |

The call wheel offers only the calls the player has heard (Rest, Close, Gather, Fall, Lost, Answer). It is click-friendly (pick a glyph) and has no rhythm input: the horn plays the shape.
**The refused-call seed (required pass-by, no interaction):** during lesson 4 or 5, a **young warden** at the practice rack runs an interval Dorn has not taught (it is not reproduced: one long and the start of a second that bends wrong). **Ressa Highcrag**, crossing the shoulder, puts her hand flat on the horn's bell and stops it (`TPW-B1.1`). "Not that one." She walks on. Dorn does not explain (`TPW-D2.70` if asked: "Ask her. She won't tell you either.").
**Optional inspect:** the training board's painted-over seventh row (`TPW-I` table; sets `TPW_BOARD_SEEN`; TTH reads it).
On completion Dorn hands over the **practice horn** for the day ("Bring it back. They all say they will.") and sends the player down: "Close comes when you go out the gate. Listen for it."
**Verbs:** listen, respond, blow a call.

### Beat 2 — The Store-Yard (`S02_yard`)
**Objective:** *Go out through the gate.*
The steps from the horn post come down into the store-yard, and the route to the gate runs past the tarp (required pass-by: a volume on the path). The storekeeper glances up (`TPW-B2.1`: "Not mine. Waiting on the hauliers. Up the track, once the weather lets them."). The objective does not change; the player can walk past.
**Optional inspect:** the sacks under the tarp (`TPW-I` table): grain sacks with a stencilled relief mark (a sheaf over a wave and **RELIEF — FENMERE**, the wording of Lowmark's own wartime relief stencils) and tally notches on their tags. The chalk on the tarp: *W. acct.* With `lowmark.main.02_short_measure` Completed, the inspect adds the recognition of the Crestbridge tally notches. **Nothing here, in any variant, says when, how or from which direction the sacks came** (TD-11, FT-03). Sets `TPW_SACKS_SEEN` (optional; TF-M2 reads it for a variant line).
The player walks out through the gate. **Close I** sounds behind them from the horn post as they pass under the arch.
**Verbs:** pass, look.

### Beat 3 — The Blind Corners (`S03_corners`)
**Objective:** *Get through the Blind Corners.*
Shouting from the switchbacks. A stranded peddler pair are being robbed at the second bend (`TPW-B3`). Two routes, both open, neither stealth:
- **The goat track (agility route):** a ledge above the corners with a frayed hand-rope. One **agility trigger** (a step across a gap in the ledge) has a walkable fallback (a longer scramble round the back of a boulder, 15 s). The track comes down **behind and above the slingers**, so the player engages them before they can volley (`TPW_GOAT_TRACK`).
- **The road:** straight down the switchbacks. The slingers get the first volley; the cutters meet the player at the bend.
The fight (**TPW-E1**) ends when every bandit is defeated. The **Corner-Boss** fights to 0 HP like the rest. **Optional inspect (T-2):** his cut-off Warden's badge, nailed to the overturned cart for luck (`TPW-B3.6`), says what he was: a deserter in an old Warden's coat. The peddlers (role names) thank the player in two lines and say they'll wait out the storm at Passwatch "if the gate'll have us" (`TPW-B3.7`). Optional: right the handcart (one interaction) for a small coin.
**Verbs:** traverse, fight.

### Beat 4 — The Narrows (`S04_narrows`)
**Objective:** *Find the bridgewright at the Narrows.*
**Close II** sounds as the player comes round the last corner and sees the gap. **Aud Hammerlee** (`TPW-D3`) is swearing at a rope she clearly loves. Across forty paces of scree the far loads wait, small and hooded. She lays out the work in three lines: stakes, fittings, a guide line across. Then she teaches the two things the player needs to get the line over (each a short, practical lesson on the spot):
- **Wind windows:** "Listen to the cutting." The fluted faces whistle up a fifth; a gust comes about two breaths later. Get behind a white bar. The player sees one gust come through and the crew drop behind a face.
- **Echo count:** Aud has the player blow **Answer** at the shedding face and count the beats till it comes back (the echo plays; three soft pulses on the call glyph count the beats). "Three, steady: the face is holding. If it comes back short, or smeared, it's moving. Wait for it to drop." She has them blow it once more; this time it comes back smeared, and a few seconds later a slide of stones comes down into the gap. "That."
**Verbs:** listen, count, learn.

### Beat 5 — Stormwood Stakes (`S05_stakes`)
**Objective:** *Get three stormwood stakes.*
Down on the stormwood slope (W3) two **ridge wolves** are worrying a goat carcass (**TPW-E2**). They move on the player when they see them. After the wolves, Aud's choice (`TPW-D3.20`):
- **Cut them yourself (Woodcutting):** cut three stormwood stakes from marked trunks (3 interactions). Carry them up to the anvil cart (carry state, one trip with a sledge-board).
- **Leave it to the crew:** Aud sends two of her crew down. "That's another Close, mind." The crew finish while the player moves on; **a Close sounds** when they do (`TPW_CREW_STAKES`).
**Verbs:** fight, cut, carry (or delegate).

### Beat 6 — Fittings (`S06_fittings`)
**Objective:** *Make four bridge fittings.*
At Aud's field anvil (W4):
- **Smith them yourself (Smithing):** four fittings (two shackles, two anchor plates) from Aud's bar stock (4 interactions; no material cost to the player; the bar is hers). Aud comments on the first one only.
- **Leave it to the crew:** her striker does it. **A Close sounds** when he finishes (`TPW_CREW_FITTINGS`).
The two skill steps can be done in either order. Neither is ever required: the crew alternative is always offered.
**Verbs:** smith (or delegate).

### Beat 7 — The Guide Line (`S07_guide_line`)
**Objective:** *Carry the guide line across the gap.*
The player shoulders the light guide line (carry state; movement slightly slowed; drops nothing if hit) and takes it down the scree path and up the far side, paying it out behind them. The path has three marked shelter faces (S1–S3). Two hazards, both readable, neither failable:
- **Gusts:** the fluted face whistles up a fifth; about two breaths later a gust crosses the path. A player caught in the open is pushed a step and loses a little health. Behind a white bar they take nothing.
- **The shedding face:** at S2 the path crosses under the face. The player blows **Answer** and counts. Three steady beats: go. Short or smeared: wait for the slide (dust spills first, ~2 s, then stones). A player who goes anyway takes moderate damage and is knocked back to S2; the line stays paid out.
At the far side the crew there (Ketil's people) take the line and make it fast to a buried anchor the player helps them dig out (one interaction). The far loads cheer, thinly.
**Verbs:** carry, listen, count, wait, cross.

### Beat 8 — The Span (`S08_span`) — *the strange moment*
**Objective:** *Haul the span across.*
Back on the near side (the player can walk the scree back or ride the guide line's traveller basket, which Aud now rigs: a walkable fallback and a shortcut in one), Aud's crew bends the stakes and fittings into new anchors and hauls the main ropes across on the guide line. The player works the **snub post**: a channelled interaction in **three segments** (each ~5 s) that takes up slack while the crew pulls. Gusts interrupt a segment (the whistle tells first: let go and step behind the post), but **completed segments are kept**.
During segment 2, the **span Close** sounds from Passwatch, and it is wrong (§A8): its echo comes back off the cliffs **before Dorn has finished the second note**. Everyone on the near side hears it. Aud laughs too loudly (`TPW-B8.2`). Nobody explains. Segment 3 completes the span: the new footropes and handlines are up, walkable, swaying.
**Verbs:** channel, hold, listen.

### Beat 9 — One Load (`S09_choose`)
**Objective:** *Decide what crosses first.*
The player crosses the new span to the far bridgehead (it is walkable; the sway is presentation). Aud has said what the bridge will take before the last Close: "One heavy load. Not two. Not tonight." At the far bridgehead (`TPW-D4`), **Ketil Rask** and the **caravan master** both make their case in two lines each. Neither argues with the other: they argue with the weather. The choice (§A9.3):
- **The sledge:** Nettlehook eats this winter. The caravan waits out the storm at Three Calls Shelter.
- **The caravan:** Stonewake's market and the Wardens' pay. The sledge waits at Three Calls.
- **Split:** lighten both. Half the sledge's sacks and the caravan's beasts go on to wait at Three Calls Shelter until the storm breaks; the sledge with half its load and the caravan's lightest bales cross together.
The player tells them by blowing **Gather** at the bridgehead when ready (the call wheel; the column forms on Gather). The ones who wait walk off toward Three Calls' lantern without complaint (`TPW-B9`).
**Verbs:** choose, call.

### Beat 10 — Under a Fall (`S10_escort`)
**Objective:** *Bring them home.*
The escort runs from the far bridgehead, across the span, through the Blind Corners, to the outer road below Passwatch. The column **moves on Gather and halts on Fall**: the player gives both with the call wheel. This is the act's use of what Dorn taught.
- **On the span:** gusts. The player blows **Fall** when the fluted face whistles (the column stops and crouches on the span); **Gather** after the gust. If the player does nothing, the column's leader stops by herself after the gust starts (it is slower, never fatal).
- **Under the shedding face (near side):** a Fall is needed. The player counts the echo or watches the dust; blowing Fall halts the column under cover of the near anchors. If the player forgets, Aud's crew blows Fall from the anvil cart (the column halts late and a beast is grazed by a stone: a presentation limp, a line from Ketil; no loss).
- **At the Blind Corners: wolves** (**TPW-E3**). A small pack comes down the goat track for the beasts. The column halts on its own when wolves engage. A **howler** lifts its head and holds a howl (~1.5 s); if not interrupted, two more runners come down. The beasts cannot die; wolves "worry" a beast (it bawls and stops the column) until they are defeated.
- **The outer road:** the gate in sight. **The last Close** sounds as the column comes onto the outer road (the held pip fills).
**Verbs:** escort, call, fight.

### Beat 11 — Passwatch Shut (`S11_gate`)
**Objective:** *Get inside before the gate shuts.*
The column goes in under the arch. Wardens count the beasts. Vessa waits until the player is inside, then drops the bar herself. She takes the slate off its nail and writes: *Passwatch shut. Dusk. Storm.* (`TPW-D5`; document text in the dialogue file). The player can read it over her shoulder (inspect).
**Optional:** ask her to write down who is still outside (the waiting loads at Three Calls, the far shielings, her own patrol pairs). "We write what we closed. Not who." (sets `TPW_NAMES_ASKED`). She doesn't say it is wrong or right. She hangs the slate back on its nail.
**Verbs:** enter, read, ask.

### Beat 12 — Rest (`S12_rest`)
**Objective:** *Listen for Rest.*
From the horn post, Dorn blows **Rest**: one long, flat. It comes back off the cliffs on time this time. The quest completes when Rest finishes. Dorn calls down for his practice horn. If the player offers it back, he waves it off (`TPW-B12.3`: "Keep it. You'll lose it in a better place than I would."). **The player always leaves TF-M1 with the practice horn** (reward tool, not a quest item); TF-M3 to TF-M5 rely on it, with Warden horn racks and Ressa's TF-M5 loan as fallbacks only.

**Epilogue (no step):** the barracks hearth bench offers *Keep watch until the storm breaks* (keep-watch interaction: two steps, sleet against the shutters, wardens dicing, Ketil asleep sitting up). At the end, or on the player's next entry to Passwatch if they leave, the storm has broken: clear cold sky, the gate open, Vessa wiping *Storm* off the slate with her sleeve. With `split` or with the waiting load at Three Calls, that load comes in through the gate in the morning (`TPW-B12`).

## A7. Encounters

Tuned for **Competent identity** (bible TD-12; Milestone 2 equipment). Exact levels are Gameplay Designer calls.

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TPW-E1** | 2 × pass bandit cutter, 2 × slinger, 1 × **Corner-Boss** (elite) | The Blind Corners: slingers on the second bend's ledges, cutters and Corner-Boss at the overturned cart | Slingers: zone the road. Cutters: rush. Corner-Boss: anchors the bend, steps in when a cutter is defeated | **Slinger:** whirls the sling overhead (~1.2 s, a rising whirr), then a stone along a straight line (sidestep). **Cutter:** drops the shoulder (~0.9 s), then a lunge. **Corner-Boss:** raises his cut-badge coat's hood and plants his feet (~1.4 s), then a two-hit heavy chop; second hit is the bigger one. | First Thornfell fight; terrain matters (the goat track gives the player the slingers first) | 90–120 s; 50–70% HP remaining. Goat-track route is ~20% easier |
| **TPW-E2** | 2 × ridge wolf runner | Stormwood slope, at a carcass | Runners circle and bite from the flank | **Runner:** flattens its ears and hunches (~0.8 s), then a lunge-bite | Short, readable; introduces wolves before the escort | 30–45 s |
| **TPW-E3** | 3 × ridge wolf runner, 1 × howler (+2 runners if the howl completes) | The Blind Corners, during the escort; they come down the goat track | Runners: go for the beasts, then the player when struck. Howler: hangs back on the goat track | **Howler:** lifts its head and draws breath (~1.5 s, visible ribcage swell), then a long howl that calls two runners. Interruptible by any hit or by the player's horn (any call blown at it makes it flinch: a small, cheerful use of the calls). | Escort pressure without escort failure | 60–90 s; beasts cannot die |

**Hazards (not encounters):** gusts (whistle a fifth up, ~2 breaths, push and light damage in the open); the shedding face (smeared echo or dust spill, ~2 s, then stones: moderate damage and knockback). Both are always readable and never fatal on their own at Competent identity.

**Rules**
- **Defeat at 0 HP** (CDR-1; supersedes TD-7). Bandits and the Corner-Boss fight until defeated and take the ordinary defeat presentation. Wolves fight to 0 HP. No ally comments on mercy.
- **Melee or ranged** (CDR-2): every fight accepts both. The ledge slingers can be answered with arrows or reached by the goat track; ranged is never required.
- **Combat never reveals evidence.** No bandit carries anything about the stores.
- **Death:** respawn at the Passwatch gate before the Blind Corners; at Aud's anvil cart after. Completed encounters stay defeated. The Close count never advances on death. Built bridge stages persist.
- **Co-op:** bandits and wolves shared. Each partner's Close count, bridge stage and load choice are their own; presentation follows each player's state. Fallback: the host's Close sky and bridge stage; partners still complete their own steps and choice.

## A8. The discovery moment: the Close that comes back early

**What it is:** the span Close (Beat 8). Dorn's Close is two long notes, falling. In the storm, the player hears the first note, then **the second note's echo off the cliffs above the Narrows before Dorn's second note has reached them**. Then the second note arrives, as if it were the echo of itself. It is never explained (bible §7.4 "deliberately unexplained forever"). It is not resonance shown as power: no glow, no shake, no UI. It is a wrong order of sounds.

| Time | Element | Spec |
|---|---|---|
| 0 s | **The first note** | Close, note 1, from Passwatch (distant, positional, down-pass). Ordinary. Its normal echo off the near cliffs follows at ~1.0 s. |
| ~2.0 s | **The early echo** | A falling long note, softer and slightly smeared, **from the cliffs above the far side** of the Narrows. It is the second note's shape. Nothing has been blown. |
| ~2.0–3.5 s | **Ambience duck** | Wind and sleet duck by about half for 1.5 s, as if the pass were listening. The crew's work sounds continue. No music. |
| ~3.5 s | **The second note** | Dorn's actual second note arrives from Passwatch. It sounds like an echo of the echo. Its own echo then follows on time. |
| 3.5–5 s | **The laugh** | Aud laughs, too loud, too long (`TPW-B8.2`). One crewman makes the Rest gesture (a flat hand) at the cliff, a habit. Ketil, across the gap, has stopped with a rope in his hands. |
| After | **The glyph** | The Close pip fills as normal. The echo-count pulses on the glyph (if the player has used echo count) show **two beats, then one before**: a single pulse on the left of the glyph that the player has never seen before. It fades. |
| Never | **Explanation** | Nobody says what it was. If asked (`TPW-D3.50`): Aud: "Wind trick." Dorn later (`TPW-B12.4`, optional): "I heard it from the post. I'm not talking about it on a closing day." |
| UI | | Segment 2 of the snub-post channel **does not interrupt** for the moment. The player is holding the post. The camera stays with the player. |

**Why it is here:** it is the Wonder beat of Thornfell's emotional line (bible §1), and the first instance of Iven's "echoes that arrive before sound" [CANON experience], experienced by the player before they meet Iven (TF-M4) or TME09. It identifies no one and proves nothing.

## A9. Quest structure for implementation

### A9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_arrive` | Speak to the warden at the Passwatch gate. | Enter gate volume + `TPW-D1` end | Yes | Quest Active on entering the gate volume. `TPW_WHINSTONE_ASKED` optional (Lowmark MQ4 Completed) |
| `S01_calls` | Learn the calls at the horn post. | Six lessons complete (`TPW-D2`) | Yes | Sets `TH_CALLS`. Ressa's refusal (`TPW-B1.1`) plays during lesson 4 or 5 on a volume, always. Practice horn granted (temporary; reward tool on completion) |
| `S02_yard` | Go out through the gate. | Enter store-yard pass-by volume, then exit-gate volume | Yes | Pass-by volume is on the only path from the horn post to the gate. Sack inspect optional (`TPW_SACKS_SEEN`). **Close I** on exit |
| `S03_corners` | Get through the Blind Corners. | TPW-E1 all defeated | Yes | `TPW_GOAT_TRACK` if the goat-track volume was entered before E1 |
| `S04_narrows` | Find the bridgewright at the Narrows. | Enter W4 (**Close II**) + `TPW-D3` lessons end (wind window seen; echo count blown twice) | Yes | |
| `S05_stakes` | Get three stormwood stakes. | TPW-E2 defeated + (3 stakes delivered **or** crew chosen) | Yes | Crew: `TPW_CREW_STAKES`; a Close sounds when the crew finishes (~60 s after choice) |
| `S06_fittings` | Make four bridge fittings. | 4 smithing interactions **or** crew chosen | Yes | Crew: `TPW_CREW_FITTINGS`; a Close sounds. Either order with S05 |
| `S07_guide_line` | Carry the guide line across the gap. | Enter far-side volume carrying the line + anchor interaction | Yes | Hazards never fail; knockback to last shelter face |
| `S08_span` | Haul the span across. | 3 × `snub_post` segments complete | Yes | **Span Close** and the strange moment on segment 2 start (server event `passwatch.close_early`). Traveller basket enabled |
| `S09_choose` | Decide what crosses first. | Option chosen in `TPW-D4` + Gather blown at the bridgehead | Yes | Sets `TH_PASSWATCH_ROUTE` |
| `S10_escort` | Bring them home. | Column reaches the outer-road volume | Yes | TPW-E3 at the Corners. **The last Close** on completion |
| `S11_gate` | Get inside before the gate shuts. | Player inside gate volume + `TPW-D5` end | Yes | `TPW_NAMES_ASKED` optional. The gate shuts behind the player only (per-player gate state; co-op fallback below) |
| `S12_rest` | Listen for Rest. | Rest call finished (server event `passwatch.rest`) | Yes | Quest → Completed. Epilogue unlocked (storm breaks on keep-watch end or next zone entry) |

### A9.2 Flags

| Flag | Set by | Read by (here) | Read by (later packages) |
|---|---|---|---|
| `TH_CALLS` | `S01_calls` complete | Call wheel; glyphs; S07–S10 | All milestones; *Horn and Silence*; *Goat Year* |
| `TPW_WHINSTONE_ASKED` | `TPW-D1.30` (Lowmark MQ4 Completed only) | — | TF-M2 `TIW-D2` (the same haulier, variant line) |
| `TPW_BOARD_SEEN` | Training-board inspect (optional) | — | *The Third Horn* opening line |
| `TPW_SACKS_SEEN` | Sack inspect (optional) | — | TF-M2 `TIW-D3` and the grain-gallery inspect (variant line) |
| `TPW_GOAT_TRACK` | Goat-track volume before E1 | `TPW-B3` barks | — |
| `TPW_CREW_STAKES` | `TPW-D3.20` option | Close count | — |
| `TPW_CREW_FITTINGS` | `TPW-D3.30` option | Close count | *The Bridge That Chose* (Aud: "You'll smith them yourself this time") |
| `TPW_CLOSE_COUNT` | Close-count events | Sky/sleet presentation; Close glyph pips | — (per-player presentation; cleared on completion) |
| `TH_PASSWATCH_ROUTE` | `S09_choose` | `TPW-D5`, `TPW-B12` | TF-M2 (Brynjar's ledger line; Elira's closing); *Nettlehook Rope*; TF-M5 posture (sledge +1 open) |
| `TPW_NAMES_ASKED` | `TPW-D5.20` (optional) | `TPW-D5.21` | TF-M5 Vessa line at the Gatefall; *The Third Horn* (Dorn) |

### A9.3 Choice: what crosses first

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **The sledge** (`TH_PASSWATCH_ROUTE = sledge`): *Nettlehook's winter grain* | The sledge and Ketil's crew come through. Nettlehook's granary is full for winter. | The caravan waits at Three Calls through the storm. Stonewake's market opens short; the Wardens' pay is late (caravan master: "Wardens'll eat goodwill this week."). | TF-M2: Brynjar's line on the ledger's struck children's ration is sharpest ("Ketil hauled grain over a broken bridge for those children."). *Nettlehook Rope*: Ketil owes the player. TF-M5 posture: +1 open. |
| **The caravan** (`= caravan`): *Stonewake's market and the Wardens' pay* | The caravan comes through. Wardens are paid; Stonewake's market has fur and iron for winter. | Nettlehook's sledge waits at Three Calls. The highstead goes on short rations until the storm breaks. Ketil: "They'll eat bread with nothing on it. They've done it before." | TF-M2: Elira's allotment worry is sharper at Nettlehook. *Nettlehook Rope*: Ketil is polite, not warm. No posture weight. |
| **Split** (`= split`): *half of each* | Half the sledge's sacks and the lightest bales cross. The rest wait at Three Calls and come in at morning. | Nobody gets enough tonight. Both Ketil and the caravan master grumble, evenly. The escort has more beasts to herd (one more Fall needed on the span). | TF-M2: Elira's closing names both. *Nettlehook Rope*: neutral. No posture weight. |

All three loads are **safe** in every outcome: whatever waits at Three Calls arrives the morning the storm breaks. None is wrong. The cost is who goes short tonight.

## A10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| The six Ordinary Calls (`TH_CALLS`) | Knowledge / UI | Glyphs on screen for every call heard from now on; the call wheel with the horn |
| **Hornbearer's practice horn** | Reward tool (functional name; item pass defines it) | Lets the player blow the six calls anywhere. Needed by later milestones' call interactions (fallback: horn racks at Warden posts) |
| Passwatch hub | Access | Gate, barracks, store-yard, horn post, ridge stables; a respawn point; the Warden post |
| The Narrows crossing | Access | Windscar Pass opens to Three Calls Shelter and beyond (after the epilogue's storm break) |
| Small payment | Currency | Aud's day rate for "a stranger who can hold a snub post", or the caravan master's thanks (by route). Economy tuning |
| Skill XP | Action only | Melee; Woodcutting and Smithing if done personally |
| Side-quest unlocks | Story | TTH, TNR, TSR, TST, TGY, TBC, TAS, TOS |
| TF-M2 | Story | Offered by Elira at Stonewake's ridge-market once the storm has broken |

## A11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player takes a long time anywhere | The Close count only advances on events. Once the bridge is built, nothing advances until the escort is home. **No failure.** |
| Player chooses the crew for both skill steps | Two extra Closes; the sky is darker and sleet heavier. The last Close is still held. |
| Player answers a call wrongly at the horn post | Dorn repeats the call. No penalty. |
| Player is hit by a gust or a slide | Damage and knockback to the last shelter face; the guide line stays paid out; segments of the snub post persist. |
| Player forgets to call Fall on the escort | The column's leader (span) or Aud's crew (near side) calls it late. A beast limps (presentation). No loss. |
| Wolves reach the beasts | The beast bawls and the column halts until the wolves are defeated. Beasts cannot die. |
| Death | Respawn at the gate (before Corners) or at Aud's anvil cart (after). Encounters defeated stay defeated. Bridge stages and the chosen load persist. |
| Logout mid-escort | Restore to `S10`: the column is waiting at the far bridgehead (or the span's near end if the player had crossed); wolves reset. |
| Walking away | Quest stays Active at its step. Resume hook: Vessa at the gate ("Still shut. Still waiting on you."); after S04, Aud at the anvil cart. The Close count resumes where it stood. |
| Fail state | None. |
| Co-op | Shared enemies. Per-player Close count, bridge stage, load choice and gate state. Presentation follows each player's own state. Fallback: the host's state drives the sky, bridge prop and gate as presentation only; each partner's steps and flags are still their own (a partner already past `S11` sees the gate shut and passes through it as a warden opens the wicket). No partner's escort or step waits on another player's bridge or gate state; a partner who leaves or is ahead never blocks the other, who finishes from their own step (CDR-6). |

## A12. Integration needs

Documented dependencies for a later Systems Engineer. Nothing here is implemented.

| Need | Owner | Minimum viable form |
|---|---|---|
| **Call wheel** (blow a call) | Systems + UI | An interaction offering the calls the player knows (glyph buttons; no rhythm input). Plays the call's audio shape from the player's position. Emits a `call_blown(call_id, position)` event that quest volumes and NPC groups can listen for. Fallback: context prompts ("Blow Gather") at the places a call is needed. |
| **Call glyphs** | UI | When a horn call plays within hearing and `TH_CALLS` is set, show its glyph near the screen edge for ~2 s. Accessibility: also for players with audio off. |
| **Close count** (per-player quest clock) | Systems | A per-player counter advanced by named events; drives a sky/sleet presentation step and a pip display. A held final position released by an event. Lowmark keep-watch convention; no world time. |
| **Wind windows** | Systems + audio + art | Hazard volumes on a gust schedule with a whistle tell (~2 breaths before); "shelter face" safe volumes marked by a painted bar. Damage and a one-step push in the open. |
| **Echo count** | Audio + UI | When the player blows a call at a marked face, play the echo with a delay set by the face's state (steady / short / smeared) and pulse the glyph per beat. One state machine per shedding face (holding → shedding → dropped → holding). |
| **Escort column** commanded by calls | Systems / NPC | A group of NPCs and beasts on a path that moves on `Gather` and halts (crouch) on `Fall`; auto-halts when engaged; cannot die; "worried" state when a wolf attacks. |
| **Channelled segments with persistence** | Systems | Snub post: three segments; interrupt on gust; segments kept. |
| **Agility triggers** | Systems | Goat-track gap step; walkable fallback path. Traveller basket on the guide line (ride interaction) with the scree path as fallback. |
| **Scripted audio event** (`passwatch.close_early`) | Audio | §A8: the echo before the second note, an ambience duck, then the late note. Per player. |
| **Per-player gate state** | Systems | The Passwatch gate shut for players between `S11` and the epilogue's storm break; open otherwise. Fallback: a wicket door that wardens open for players on other steps. |
| **Keep-watch interaction** (epilogue) | Systems | Lowmark convention. Two steps; per-player sky. |
| Creatures | Schema / Gameplay | Pass bandit cutter, slinger, Corner-Boss; ridge wolf runner, howler. |
| Cut-badge inspect | Art / Systems | The Corner-Boss's cut badge on the overturned cart (inspect prop, `TPW-B3.6`). Ordinary defeat presentation for all bandits (no yield state, no tied props). |
| Reward tool | Item pass | "Hornbearer's practice horn": the call wheel's carrier. |

## A13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The "W. acct." sacks** | Lowmark relief grain bought on the Whinstone account by Bersi Coldbrook for the Iron Winter. | Somebody's order waiting for the weather. | Relief stencil, tally notches, chalk "W. acct.", "up the track". With Lowmark MQ4: the name rings. | Emberholt is buying grain through Passwatch. | How or from where the grain came (**never told**, FT-03). | TF-M2 (R05). |
| **The interval Ressa stopped** | A start of the Split, the wartime forcing call. | Nobody plays it. | Ressa's hand on the bell; "Not that one." | A bad note; a young warden's mistake. | What it is and what it did. | *Horn and Silence*; TF-M3 (R06 horn half). |
| **The painted-over row on the training board** | The Third Horn: "heard; someone is still out". Dropped after the war. | An old mistake painted out. | Raised paint under grey. | A call nobody needed. | Its meaning. | *The Third Horn*; TF-M3 (Dorn). |
| **Who is outside** | Thornfell's closures record nothing about who is left out (TD-5). | It's the weather's business. | Vessa's slate; "We write what we closed. Not who." | It doesn't matter for a storm closure. | The late-war sealings' roster. | TF-M5 (R06 sealing half). |
| **The Close that came back early** | Unexplained forever (bible §7.4). | Wind tricks. | The sound order; Aud's laugh. | The mountain answering; a warning. | Everything. | None (deliberately). |

## A14. Open decisions

1. **TD-11 (Whinstone route):** the store-yard sacks are shown with no arrival. If the Director rules a route, only the sack inspect and `TPW-B2.1` change.
2. **TD-13 (stormwood, bar stock):** the stakes and fittings use no player materials and create no inventory items, so the economy pass is not blocked. If stormwood becomes a catalog item, the stakes can become real carried items.
3. **The Fenmere relief stencil (resolved, independent review):** "Fenmere" is established Lowmark canon (House Fenmere; the Fenmere granaries in the Lowmark bible; the depot stencil **RELIEF — FENMERE — LOT** in Lowmark Act III and the Lowmark zone package; the sheaf-over-a-wave image in Lowmark Act I). The sack stencil now reads a sheaf over a wave and **RELIEF — FENMERE**, the established wording without the lot line. Inspect text only; no route implied.
4. **Reward horn:** the practice horn needs an item-pass definition. Until then, later call interactions use Warden horn racks as fallback.
5. **Where Nettlehook's sledge was fetching from [NEW]:** the sledge went out for Nettlehook's autumn share held at Three Calls Shelter's grain-house. It does not imply any trade route over the pass. MAP VERIFICATION REQUIRED.
6. **Level framing (TD-12):** encounter tuning assumes Competent identity.

## A15. Internal review log

| Finding | Revision |
|---|---|
| A real-time dusk timer would be a fail state. | Replaced by the Close count: event-driven, per player, with the last Close held until the escort is home. |
| The crew alternative must cost something without punishing. | Each crew alternative costs one Close (darker sky, heavier sleet). It never brings the last Close closer. |
| The calls risked being a lecture. | Each call is taught by doing what it says, and four of the six are used again in the same quest (Gather, Fall, Answer, Close; Rest ends it; Lost is answered at the post and returns in TF-M5). |
| The store-yard sacks risked stating an arrival. | Inspect and bark say only what is there and where it is going ("up the track"). No "came", no direction, no carrier. |
| Passwatch's closing could be confused with the season's sealing. | Vessa's lines and the slate say *Storm*; the epilogue reopens the gate. The Gatefall's sealing belongs to TF-M5. |
| Ressa's refusal must stay within her ledger limits. | She refuses a call; she does not explain it, name a roster or a battle. |
| The strange moment risked reading as magic. | No glow, no UI, no shake: a wrong order of sounds and a duck. Aud calls it a wind trick; Dorn won't discuss it. |
| Escort risked a fail state. | Beasts cannot die; forgotten Falls are called late by NPCs at a presentation cost. |
| Agility. | Goat-track gap and traveller basket each have walkable fallbacks. |
| Address. | Vessa, Aud and Dorn say "walker". No name, title or origin. |
| **Independent review (2026-11-03)**, TF-M1: 2 findings (1 medium, 1 low). | Fenmere verified as Lowmark canon; sack stencil changed to the established RELIEF — FENMERE wording (open decision 3 closed). Practice horn made unconditional (the player always keeps it) so TF-M5 can rely on it. |
| **Director rulings reconciliation (2026-11-03)**, TF-M1: CDR-1, CDR-2, CDR-3. | TPW-E1 bandits and the Corner-Boss fight to 0 HP; yield, kneel and tied-prop rule removed; Corner-Boss march-off barks removed. Deserter detail re-sourced as an optional cut-badge inspect on the overturned cart (T-2, `TPW-B3.6`). `S03_corners` completes on defeat. Melee-or-ranged rule added (slingers). Header release wording reconciled. Yield-presentation integration need replaced. |

---
---

# Part B — TF-M2 The Iron Winter Stores (`TIW`)

## B1. The quest in one paragraph

The storm has broken and the Hearthguard storekeepers at Stonewake's ridge-market are counting winter allotments that will not stretch. **Elira Hearthward** tells the player why she thinks so: somebody is buying up grain and iron at two over the board and paying with chits that nobody can cash in Stonewake. The player reads the market's price board, talks a haulier into showing a chit stamped **"W."**, and finds the tarp in the Passwatch store-yard folded and the sacks gone, with sledge-runner marks leading out of the gate and up the **Whinstone track**. On the climb, a haul crew's voices ahead of them vanish in the middle of a word as they pass through a gully where the player's own footsteps make no sound and the dust falls straight down. Above stands the **Muster Hut**, where a splinter crew drills clanless hires with spears and a horn, under an unsigned broadsheet: *"When the forges eat the grain, the passes go dark."* The player fights through or takes the cliff ledge around. The **Whinstone Store**, a wartime store-house cut into the cliff, has its front gate barred from inside, so the player climbs the **old hoist shaft** and can wind its cage up behind them. Inside are four galleries: grain (including sacks with the lowland relief stencil), iron (new spearheads; Ridge Crows nesting in the vents), horn plates packed in grit from Shatterfall (with tuning sketches that name the Summit's great hall), and the counting room. There the store-factor **Bersi Coldbrook**, brave about paperwork and terrified of the drop outside his window, gives up when his last crewman falls. His **ledger** shows receipts on the Whinstone account, pay chits to Shatterfall miners for plates by the crate, a struck-through children's ration for Nettlehook, and one line: *"Relief grain, sixty-eight measures. Received."* He calls the reserve **the Iron Winter**, "for when Emberholt comes for the passes", and he will not say how the grain came. In the last bay, the player touches a plate on a trial frame and the whole rock hums and every crow on the cliff lifts at once. Then the player decides how **Brynjar Korr** learns, privately at the store or in public before Hadrik, and what happens to the stores. The quest ends with Elira at the market in the first snow.

**What the player should remember:** the crows lifting off the cliff, and the struck line on the ledger. **What the player should want next:** whose countersign is missing, and what the plates are being tuned for.

## B2. Selection record

| Candidate | Verdict |
|---|---|
| **A. A market investigation that ends in a report.** | Rejected. It is the administrative pattern Phase 1.5 warns against. The bible requires a cliff dungeon. |
| **B. A stealth raid on the store.** | Rejected. No stealth system (Phase 1.3). The hut is a route choice, not a sneak. |
| **C. Three small leads → tracked climb with a null-point → hut route choice → hoist-shaft entry → four galleries that read as an inventory → the clerk gives up and testifies → the trial-frame hum → how Brynjar learns → what happens to the stores** (selected; the bible brief). | **Selected.** The investigation is done with the player's feet and eyes. The dungeon *is* the evidence: each gallery is a line in the ledger before the player reads the ledger. |

## B3. Canon grounding

| Element | Source | Status |
|---|---|---|
| Elira Hearthward: exhausted, practical; pushes for relief; argues with Brynjar and defends him | Thornfell anchors §II | [CANON] |
| Brynjar Korr: loud, loyal, pounds the table, would die for any Thornfell child; the clan keeps the loudest horn towers; brags about "the horn that split the ridge" | Thornfell anchors §II | [CANON]; not in the splinter (Part 4 ledger) |
| Hadrik Stonewake: keeps the Assembly together while it decides; chooses where people stand | Thornfell anchors §I | [CANON] |
| Horn plates salvaged in the war; Echohewn null-points | Bible §2.1 | [CANON] |
| Ridge Crows: harassers that follow patrols and mob the weak | Bible §10; dossier ecology | [CANON] family |
| A Thornfell faction's unsanctioned war stores, partly bought with Lowmark relief grain; buyer named, route not | H25; FT-03 | [APPROVED — FT-03] |
| The Iron Winter, the Whinstone Store, the Muster Hut, Bersi Coldbrook, the store ledger, the trial frame | Bible §2.3, §4.2 TP08/TP27, §5.2 | [NEW] / [PROPOSAL — DIRECTOR] TD-1 |
| Brynjar's two responses | Bible TD-2 | [PROPOSAL — DIRECTOR] TD-2 |
| The broadsheet phrase | Bible §2.3, §8.2 (R15 seed) | [NEW]; seed only |

## B4. Quest summary card

| Field | Value |
|---|---|
| Working title | **The Iron Winter Stores** |
| Suggested content id | `thornfell.main.02_iron_winter_stores` |
| Arc position | Act I turn (Arcs §3.1, Thornfell movement 2: "a reserve nobody declared") |
| Prerequisite | TF-M1 Completed and its storm broken (epilogue played or Passwatch re-entered). Tuned for Competent identity (TD-12). |
| Offer | Elira Hearthward at Stonewake's ridge-market (`TIW-D1`). |
| Solo / co-op | Solo-clearable. Co-op partners share crews and crows; leads, inventory inspects, the route and the stores choice are per player. |
| Target length | 45–55 minutes first time |
| Combat share | ~30% |
| Dialogue share | ~20% |
| Tracking, climbing, reading, choice | ~50% |
| Skills touched | Melee (required); Smithing (optional: open the iron gallery's hasp at the crew's own forge; the vent crawl is the alternative) |
| Choices | How Brynjar learns (private / public); what happens to the stores (reported / seized / leverage, leverage on the private route only) |
| Unlocks | `TH_STORES`; `TH_BRYNJAR`; `TH_SEASON = snow`; R05 owned; the Whinstone Store as a revisitable site (state by `TH_STORES`); the cage shortcut; five side quests (Act I header); TF-M3 |
| **Anchor** (contract) | The Hearthguard (Elira, the storekeepers); the Blood-Oath (Brynjar); the Assembly (Hadrik) |
| **World-truth row** (contract) | H25 (the splinter's unsanctioned stores, partly Lowmark relief grain); H11 (salvaged horn plates being rebuilt into a horn) |
| **Revelation role** (contract) | **Owns R05.** **Plants** R07 (the trial-frame hum; Eyvind's sketches naming the Summit's great hall); **plants** R06 horn half (plates with Shatterfall grit; pay chits to Carrick's men; Brynjar's boast); **plants** R15 (the broadsheet phrase; never explained). |
| **Recurring evidence** (contract) | The relief sacks (TF-M1 store-yard → grain gallery), custodians: the stencil on the sacks and the store ledger. The account name "Whinstone" and "sixty-eight measures" (Lowmark MQ4 bill), custodians: the Lowmark bill and this ledger (two-halves connection, optional, never a gate). The pay chits to G. Carrick's men recur in TF-M3, custodian: Gerrit Carrick's testimony. |
| **State compliance** (contract) | Inactive / Active / Completed. Choices recorded in `TH_BRYNJAR` and `TH_STORES`; no fail path; every required proof (sacks, ledger, sketches) is on the critical path and persistent; resume hook with Elira at the market, or Bersi in the counting room after S09. |

## B5. The places

### B5.1 Stonewake ridge-market [TP01, CANON settlement; NEW detail]

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **M1. The Hearthguard stall** | Elira; the offer; the closing scene. | A long trestle under a stone arch (Hearthguard "good old building": the arch carries voices across the market). Allotment boards: highstead names in chalk with measures beside them, many rubbed down and rewritten smaller. Empty sacks folded in a pile taller than the full ones. Storekeepers with tally boards. |
| **M2. The price board** | Lead 1. | A slate board on a post: grain, iron bar, salt, wool, with prices chalked and re-chalked upward. Under grain and iron, in a different hand: **"W. pays two over. Any lot."** Someone has scratched a line under it with a knife point. |
| **M3. The hauliers' stand** | Lead 2. | Sledges, harness, a brazier. A **haulier** sits with his sledge, not working. Tied to his harness peg, a bundle of paper chits. |

### B5.2 The Passwatch store-yard [TP02] (return)

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **P3'. The empty lee** | Lead 3 (`S02_tarp`). | Where the sacks stood, a rectangle of dry ground. The tarp is gone. Grain spilt in the cracks of the paving. **Sledge-runner marks** cross the yard from the empty rectangle to the gate: two parallel grooves in the frost, heavy, many times over. The storekeeper on his crate. |

### B5.3 The Whinstone track [Windscar subzone]

Relative route (bible §4.2; **MAP VERIFICATION REQUIRED**): beyond the Narrows and Three Calls Shelter, a narrower track leaves the pass road and **climbs the cliff above the pass** in switchbacks. It is not on any Warden patrol board.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **K1. The track foot** | Start of the tracking. | A cairn with an old wartime painted sign scraped off. Runner grooves leave the pass road here, deeper where the sledges were turned. |
| **K2. The switchbacks** | Tracking; light traversal. | Snow-poles, new ones among old ones. A rest shelf with a stamped-out fire. Runner grooves; at two forks, the fresh grooves are on one side only (the trail reads itself; the objective marker re-pins at each fork). |
| **K3. The quiet gully** | **Null-point** (foreshadowing TF-M4, TDS01). | A short, deep cleft the track threads through. The walls are smooth, and the smoothness is cut. Nothing grows. The air does not move. §B8.1. |
| **K4. The hut shoulder** | Approach to the Muster Hut. | The track widens onto a shoulder where the hut stands. Drill noise carries down: a horn, stamping, a crew boss counting. |
| **K5. The cliff ledge** | Alternate route around the hut. | A wartime ledge path cut along the cliff face above the hut, with iron rail pins and an old rail. Fluted cuts in the wall whistle. Ridge Crows roost in the cracks. |

### B5.4 The Iron Winter Muster Hut [TP27]

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **H1. The drill yard** | Encounter; route choice (`S04_hut`). | Beaten ground, a rack of practice spears with ridge-iron heads, a straw target in the shape of a man wearing a scrap of red cloth (a crude "Emberholt" target; it is ugly and they know it). Clanless hires in a ragged line. |
| **H2. The hut wall** | Broadsheet (pass-by). | A stone-and-turf hut with a horn hung by the door. **The broadsheet** is nailed to the door at eye height. A chalk board inside the door: a list of hires by first name and pay owed, all marked "chit". |
| **H3. The ledge rail** | Broadsheet copy (pass-by on the ledge route). | A copy of the same broadsheet has blown off the hut and caught on the ledge's rail pin, flapping. |

### B5.5 The Whinstone Store [TP08] — Thornfell's first dungeon

A wartime cliff store-house cut into the rock above Windscar Pass. Its front faces the track on a ledge; its back is a hoist shaft dropping to a lower terrace where carts used to come. It reads in two layers: **wartime order** (stencilled bay numbers, iron rings, ventilation shafts that whistle) and **this autumn's filling** (new timber racks, pale; fresh straw; lamp oil; a cold-weather smell of grain and iron). It should be empty. It is full. **MAP VERIFICATION REQUIRED** for the cliff's position relative to the pass road and the Gatefall.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **G0. The front gate** | Barred; points to the shaft. | Twin wartime doors of iron-bound timber in a rock-cut arch. **Barred from inside.** The hinges are greased fresh; the ledge in front is swept. A wartime stencil above the arch: a bay number and **WHINSTONE**. The door has no handle on this side. |
| **G1. The hoist foot** | Entry (`S05_shaft`). | A lower terrace reached by a path down from the gate ledge. A cart turning-circle grown over. An **iron cage** sits at the bottom of a vertical shaft, chained to a ring with an old padlocked chain (rusted solid). The hoist cable runs up into the dark. Iron rungs climb the shaft wall beside the cage track. |
| **G2. The hoist shaft** | The climb. | Three runs of rungs, two **rest ledges**. Two **vent slits** in the shaft wall open onto the cliff face and whistle up a fifth before a down-draught that swings the cable (the wind-window tell). |
| **G3. The winding head** | Shortcut (`S05b_cage`, optional). | A timber winding drum with a crank and pawl, a brake lever, a lamp hook. Fresh tallow on the pawl. From here the store's inner passage runs to the galleries. |
| **G4. The grain gallery** | Required inspect (`S06_grain`). | A long vault with nine bays of new pale racks. Sacks to the roof: highstead sacks with Thornfell clan marks, and a whole bay of sacks with the **lowland relief stencil**. The **Passwatch tarp**, folded, chalk side in, on a bay end. A lamp, a bench, two bowls of porridge going cold (the guards' break). |
| **G5. The iron gallery** | Crows; hasp; required inspect (`S07_iron`). | Racks of **new spearheads** of ridge iron, bundled shafts, a field forge with a bellows and quench tub (warm). Three **vent shafts** in the ceiling run up to the cliff face. **Ridge Crow nests** of sticks and wire in all three. Droppings on the racks. The inner door to the plate gallery is chained with a new **hasp and chain**. A **vent crawl** at knee height runs around the door through an old air passage (alternate route). |
| **G6. The plate gallery** | Required inspect (`S08_plates`); sound puzzle. | Crates packed in straw, each holding Echohewn **horn plates** (curved tuned stone backed with horn, holes for bolts). Grey-gold **grit** in the straw and on the floor: gorge stone. A pinboard of **Eyvind's tuning sketches**. The gallery's far mouth opens onto a short passage to the counting room; a side alcove carries sound well (an old signal niche). |
| **G7. The counting room** | Boss room (`S09_counting`). | A clerk's room with a stove, a high desk, a strongbox, pigeonholes of chits, a **loophole window** looking straight down the cliff at the pass far below. Bersi's chair is set as far from the loophole as the room allows. |
| **G8. The last bay** | The strange moment. | A deep bay off the counting room. A **trial frame**: a timber A-frame with five plates hung on gut cord, a felt-headed mallet on a hook. A second loophole looks out along the cliff face, where crows roost on every ledge. Chalk on the frame's beam. |

## B6. Player-facing sequence

### Beat 0 — Short Allotments (`S00_offer`)
**Objective:** *Speak to Elira Hearthward at the ridge-market.*
After TF-M1's storm breaks, a Hearthguard runner at Passwatch tells the player that Elira asked for "the walker who brought the sledge in" (or "the caravan", or "half of both", by `TH_PASSWATCH_ROUTE`). At the market (M1), **Elira** (`TIW-D1`) is counting. She does not look up until she has finished the row. Her storekeepers' allotments are short because a buyer is taking every lot at two over the board and paying in chits "nobody in Stonewake can cash". She won't guess who. "Brynjar says Emberholt. Brynjar says Emberholt about the weather." She asks the player to find where the grain is going.
**Verbs:** talk.

### Beat 1 — The Board and the Chit (`S01_market`)
**Objective:** *Find out who is buying.*
Two leads in the market, in either order:
- **The price board** (M2; inspect). "W. pays two over. Any lot." (`TIW_LEAD_BOARD`.)
- **The haulier** (M3; `TIW-D2`). He hauled for "W." until the coin ran out; now he's paid in chits he can't spend. He shows one (document: **the haulier's chit**, stamped "W."). He hauled sacks from the Passwatch yard up the Whinstone track to "the hut" and was turned back there; he has never seen the store. He will not say more than "up the track". With `TPW_WHINSTONE_ASKED`, he is the haulier who looked away at the gate: "You asked. At the gate. I didn't answer you." (`TIW_LEAD_CHIT`.)
When both are done: *Look at the Passwatch store-yard.*
**Verbs:** read, talk.

### Beat 2 — The Empty Tarp (`S02_tarp`)
**Objective:** *Look at the Passwatch store-yard.*
At Passwatch (P3'), the sacks are gone and the tarp with them. The storekeeper (`TIW-D3`): "Hauliers came the day after the storm. Up the track." With `TPW_SACKS_SEEN`: "You looked at them. I saw you look." Required inspect: **the runner marks** (they lead out of the gate; objective *Follow the sledge marks.*). Optional inspect: spilt grain in the paving cracks ("Lowland grain. Thin, pale, small. Not ridge oats.").
**Verbs:** look, track.

### Beat 3 — The Whinstone Track (`S03_track`)
**Objective:** *Follow the sledge marks.*
Through the Blind Corners, over the Narrows (repaired), past Three Calls, to the track foot (K1). The grooves are the trail: at two forks only one side carries fresh marks (objective re-pins on entering each fork's correct branch; the wrong branch dead-ends at a goat ledge in 30 paces with a "The marks don't come this way." log line).
**The quiet gully (K3; §B8.1):** above the second fork the player hears a **haul crew** somewhere ahead: a sledge creaking, two voices calling the pull ("And up. And up."). The voices **stop mid-word**. A few seconds later they start again, further on, as if nothing happened. When the player walks into the gully, their own footsteps vanish; dust from the wall falls straight down. When they leave it, sound comes back all at once. Nobody comments. Optional inspect in the gully (`TIW_GULLY_HEARD`): *"Quiet. Not the quiet of snow. Your own breath is gone."* The haul crew is never caught: their sledge's fresh marks lead on to the hut.
**Verbs:** track, traverse, listen.

### Beat 4 — The Muster Hut (`S04_hut`)
**Objective:** *Get past the Muster Hut.*
From the hut shoulder (K4) the player sees the drill: a **hornman** blows Gather, a crew boss counts, six **clanless hires** run at a straw target in a ragged line and mostly miss (`TIW-B4`). The **broadsheet** is on the hut door (H2) and its copy on the ledge rail (H3): either route passes one (required pass-by volume; inspect optional, `TIW_BROADSHEET_READ`). Its text: *"When the forges eat the grain, the passes go dark."* It is unsigned and explains nothing.
Two routes (the player chooses by walking; not stealth):
- **Through the yard** (`TIW_HUT_ROUTE = yard`): **TIW-E1**. When the fight starts, the hires drop their spears and run downhill (`TIW-B4.5`: "We're hired, not sworn!"). The crew fight until defeated. The hornman's **Gather** calls the crew boss's buff; **the player can blow Rest within ~3 s of a Gather to cancel it** (Dorn: "Rest ends any call"). The crew are startled (`TIW-B4.7`: "Who blew Rest?").
- **The cliff ledge** (`= ledge`): the wartime ledge (K5) around and above the hut. Wind windows on fluted faces (shelter at painted bars: someone kept these painted) and a **Ridge Crow flock** (TIW-E1b) that mobs from the cracks. One **agility trigger** (a step round a broken rail section) with a walkable fallback (an inside path through a cleft, 10 s longer). The ledge comes down onto the track above the hut. The drill goes on below, unaware.
After the hut, the track's last switchback ends at the store's gate ledge.
**Verbs:** watch, read, fight or climb.

### Beat 5 — The Hoist Shaft (`S05_shaft`, `S05b_cage`)
**Objective:** *Find a way into the store.*
**The front gate** (G0) is barred from inside: required inspect ("Barred from inside. Greased hinges. Swept ledge.") re-pins the objective to *Find another way in.* A path drops from the gate ledge to the old **hoist foot** (G1). The cage is chained at the bottom with a rusted padlock nobody has opened in years; the cable runs up.
**The climb:** three runs of rungs (a climb interaction: hold to climb, release to hang; click-to-move friendly as "climb to next ledge" prompts). The vent slits whistle up a fifth before a **down-draught** swings the cable and pushes air down the shaft: on a rest ledge the player is safe; on the rungs they are pushed (they hang on, lose a little health, and stop climbing for the gust). One **agility trigger** on the second run (a step across to the cage track's crossbar, skipping half a run) has the rungs as its fallback.
**The winding head** (G3): **optional:** wind the cage up (`S05b_cage`): a channelled interaction in **three segments** (~4 s each) on the crank; segments persist. The rusted padlock at the bottom breaks under the load with a crack that echoes up the shaft (one bark from deep in the store: "Wind's at the shaft again." `TIW-B5.2`). The cage now rides between the hoist foot and the winding head: **the shortcut** (and the respawn path). Sets `TIW_CAGE_WOUND`.
**Verbs:** climb, wait, wind.

### Beat 6 — The Grain Gallery (`S06_grain`)
**Objective:** *Search the store.*
Two guards are on a porridge break at the bench (**TIW-E2**); the player has the first move. After they are defeated:
- **Required inspect: the relief sacks** (`TIW_SACKS_INSPECTED`): the lowland relief stencil, tally-notched tags. With `lowmark.main.02_short_measure` Completed: the Crestbridge notches. With `TPW_SACKS_SEEN`: "The same sacks as the Passwatch yard." Nothing says how they came.
- Optional: **the Passwatch tarp**, folded chalk side in (*W. acct.*); **the highstead sacks** with clan marks bought at two over; **count the bays** ("Nine bays. Eight full. One being filled.").
**Verbs:** fight, inspect, count.

### Beat 7 — The Iron Gallery (`S07_iron`)
**Objective:** *Search the store.* (continues)
Racks of new spearheads. **Required inspect: the spearheads** (`TIW_IRON_SEEN`): *"New. Ridge iron, hammered this autumn. Hundreds."*
**Ridge Crows (TIW-E3):** the three vent shafts in the ceiling are nesting shafts. When the player crosses under a vent, the flock comes down and mobs; **divers** drop from the shaft mouths. **The vents whistle** up a fifth before a draught blows down them: during the draught (~3 s) the crows cannot hold their dive and scatter to the walls. A player who crosses under a vent on the draught crosses free; one who fights under a vent faces the full flock. Readable, optional, never required: the crows can simply be fought.
**The hasp:** the door to the plate gallery is chained with a new hasp. Two ways on:
- **Smithing (optional):** heat the hasp's staple at the crew's own **field forge** and draw it (2 interactions). The irony is noted in the inspect text.
- **The vent crawl** (fallback, walkable): a knee-high old air passage round the door (15 s), with a crow nest in it (one diver; a squawk; an egg-less nest).
**Verbs:** inspect, fight, time, smith or crawl.

### Beat 8 — The Plate Gallery (`S08_plates`)
**Objective:** *Search the store.* (continues)
Crates of horn plates in straw and grit. **Required inspects:**
- **The plates** (`TIW_PLATES_SEEN`): *"Curved stone backed with horn, drilled for bolts. The grit in the straw is grey and gold: gorge stone."* (R06 seed: Shatterfall, not named here.)
- **Eyvind's tuning sketches** (`TIW_SKETCHES_SEEN`): plate outlines with pitch marks, a frame, and a note: *"Try in the great hall, Summit. Third mouth carries. — E."* `[SPLINTER]`. (R07 seed; TF-M4's offer reads it.)
**TIW-E4:** a spear and a **hornman** guard the passage to the counting room. When the hornman raises his horn (~1.5 s) and blows **Gather**, the second counting-room crew comes out to join this fight **unless the player blows Rest within ~3 s** (cancelled: `TIW-B8.3`, "That's not ours. Who's that?"), or interrupts the raise. This is the act's sound puzzle: the player turns the splinter's own calls against it. If the reinforcement comes, the counting room starts with one crew instead of two; the total fight is the same size either way, just split differently.
**Verbs:** inspect, fight, call.

### Beat 9 — The Counting Room (`S09_counting`)
**Objective:** *Confront whoever keeps this store.*
**Bersi Coldbrook** `[SPLINTER]` is at the high desk with the ledger in both arms (`TIW-B9`). His crews (**TIW-E5**) come at the player and fight until defeated. Bersi stays as far from the loophole as he can. **When the last crewman is defeated, Bersi gives up** (scripted, SX-N1; he never fights): "Enough! Enough. It's a ledger, not a wall!" (`TIW-B9.3`). He puts the ledger on the desk and sits on the floor away from the window.
**Required:**
- **The store ledger** (`TIW_store_ledger`, quest item): picked up from the desk (it is not a combat drop). Its full text is in the dialogue file. Reading it is optional at this point and always available from the item.
- **The trial frame** (G8): *Touch a plate.* §B8.2: the rock hums and every crow on the cliff lifts at once. Sets `TIW_FRAME_TOUCHED`.
**Verbs:** fight, take, touch.

### Beat 10 — The Iron Winter (`S10_bersi`)
**Objective:** *Question the store-factor.*
Bersi talks (`TIW-D6`), because he is a clerk and the ledger is already in the player's hands. **Testimony, after he gives up (T-3: he is a non-combatant witness):**
- The reserve is **the Iron Winter**: "what we're storing for". It is "for when Emberholt comes for the passes".
- He buys on **standing orders**. They come "carried by hand" with a **countersign** line, and he has never seen the line signed. He buys anyway: "An empty line is still a line." **He does not say whose orders they are.** Purchase authority stays withheld (R05).
- The grain came "**by the usual hands**". He will not say more. It is not courage; it is that he never asked.
- The plates are paid by chit to "G. Carrick's men, Shatterfall" (the ledger shows it). He knows nothing about horns: "I count them. I don't blow them."
- **Optional, `lowmark.main.04_night_flush` Completed:** the player can say they have seen a bill for sixty-eight measures on the Whinstone account. Bersi: "Then you've seen more paper than me." (`TIW_LOWMARK_RECOGNISED`). The ledger's own recognition line plays on reading (§B8.3).
- He asks whether the player will throw him off the cliff. The answer is no; he asks twice.
Bersi stays in the counting room. "I'm not climbing down that shaft. I'll be here."
**Verbs:** question.

### Beat 11 — How Brynjar Learns (`S11_brynjar`)
**Objective:** *Decide who hears about the store first.*
The objective names two people at Stonewake: **Brynjar Korr** (the Blood-Oath horn terrace) and **Speaker Hadrik** (the Assembly Hall). Whoever the player speaks to first about the store sets the route. (If the player goes to Elira first: `TIW-D1.40`, "Not me first. It's Blood-Oath sacks up there or it isn't. Tell Brynjar, or tell the hall. Then come back to me.")
- **Privately** (`TIW_ROUTE = private` → `TH_BRYNJAR = disowned`): the player finds Brynjar (`TIW-D7`) at the horn terrace, shouting at a horn crew. He doesn't believe it. He comes anyway "to prove you wrong in front of a clerk". He meets the player at the hoist foot (he walks up; NPC placed at G1 when the player arrives). With `TIW_CAGE_WOUND` they ride the cage; otherwise he climbs the rungs fast, swearing at the down-draught. In the counting room he takes the ledger from the player, reads, and stops at a struck line: **Nettlehook, children's winter ration, fourteen measures**, struck through, and beside it *"Held. Iron Winter."* He pounds the desk once. He **disowns** the splinter in front of Bersi: "Not my clan's. Not in my name. Not those children." He sees the plates and says, quieter, that his clan's horns split a ridge once (the boast; R06 seed), "and we never needed a clerk's crate of them".
- **In public** (`TIW_ROUTE = public` → `TH_BRYNJAR = defended`): the player reports straight to **Hadrik** in the Assembly Hall (`TIW-D8`). Hadrik listens, takes the ledger, and reads the receipts aloud in a hall that carries some voices further than others. **Brynjar is in the hall** (he is always in the hall) and hears it there, before Elira, Torvek and the hall's listeners. Out of pride he **defends readiness**: "Somebody up there is ready. Good. Somebody should be." He does not see the struck line, because Hadrik does not read it out (Hadrik reads totals). Privately furious: after the scene, outside the hall, he puts his fist on the stone table hard enough to hurt (`TIW-B11.3`), and if the player speaks to him: "I said what I said in there. Don't ask me what I say out here."
**Verbs:** choose, escort (private) or report (public).

### Beat 12 — What Happens to the Stores (`S12_stores`)
**Objective:** *Decide what happens to the stores.*
The choice is offered where the route has put the player: in the counting room with Brynjar (private) or in the hall with Hadrik (public). Hadrik does not decide; he asks what the player will carry word for, and says nobody will stop either the Wardens or the storekeepers (`TIW-D8.30`). Options (§B9.3):
- **Reported** (`TH_STORES = reported`): the store goes under Assembly seal. Ressa's Wardens guard it. The grain stays where it is until the Assembly decides. Hunger holds.
- **Seized for relief** (`= seized`): Elira's storekeepers carry it down to the highsteads tonight. The store is emptied. The evidence is the ledger alone.
- **Left as leverage** (`= leverage`; **private route only**): the player and Brynjar keep quiet. Bersi goes back to his desk with a new book and a story about a stranger who came, saw grain, and left. The splinter keeps moving where Brynjar's people can watch it. Elira will be angry.
With **seized**, an optional beat: help the storekeepers lower sacks down the hoist (with the cage wound) or carry three sacks down the shaft (carry state; the shaft's rest ledges make it a slow, honest job). Optional; flavour only.
**Verbs:** choose.

### Beat 13 — First Snow (`S13_elira`)
**Objective:** *Return to Elira at the ridge-market.*
The first snow is falling on Stonewake when the player comes back (the per-player season turns: `TH_SEASON = snow` on this step's start). **Elira** (`TIW-D9`) is at the stall. Her closing depends on `TH_STORES`:
- **Reported:** she counts what she has, which is not enough. "So we wait on a vote. Grain doesn't vote."
- **Seized:** her storekeepers are coming in with empty sledges and red faces. Nettlehook and the other highsteads have sacks tonight. "Hadrik will have words. I'll have porridge." She knows what it cost: "All you've got now is a book."
- **Leverage:** she is angry, quietly: "You found it, and you left it." She doesn't stop the player leaving. She says she'll defend Brynjar in the hall anyway, "because somebody has to, and it's always me".
The quest completes at `TIW-D9` end. Act I is over.

## B7. Encounters

Tuned for **Competent identity** (TD-12). Iron Winter crews are the splinter's fighters; they fight until defeated at 0 HP (CDR-1; supersedes TD-7). Every fight accepts melee or ranged (CDR-2): crow divers and the hornman hanging back can be answered with arrows; ranged is never required.

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TIW-E1** | 2 × Iron Winter **spear**, 1 × **hornman** (+ crew boss: a spear with more health); 6 clanless hires (non-combatant; flee) | Muster Hut drill yard | Spears: hold a line and jab; hornman: hangs back and signals | **Spear:** sets the haft under the arm and steps (~1.0 s), then a long thrust along a line (sidestep). **Hornman:** raises the horn (~1.5 s), blows **Gather**: spears gain faster thrusts for 8 s. **Counter:** interrupt the raise, or **blow Rest within ~3 s** to cancel the buff. | First splinter fight; first use of the calls *against* a crew | 90–120 s; 50–70% HP remaining |
| **TIW-E1b** | Ridge Crow **flock** (×1) | Cliff ledge route | Mobs the player on open stretches | Flock gathers on the rail and goes silent (~1.0 s) before a swirl that pecks for light damage | Ledge-route pressure; teaches crow tells before the iron gallery | 30–45 s, or avoided by moving on the draught |
| **TIW-E2** | 2 × spear (on break) | Grain gallery bench | Guards; slow to rise | As E1; **on break**: they take ~1.5 s to stand, giving the player the first move | Pacing; gentle dungeon opener | 30–50 s |
| **TIW-E3** | Ridge Crow **flock** ×2, **diver** ×2 | Iron gallery, under the three vent shafts | Flocks: mob under vents. Divers: drop from shaft mouths | **Diver:** a shriek and a shadow on the floor (~1.2 s), then a straight drop strike. **Vent draught:** whistle up a fifth (~2 breaths), then ~3 s when crows cannot dive and scatter. | Environment timing; the vents as a wind window | 45–75 s if fought; ~20 s if crossed on draughts |
| **TIW-E4** | 1 × spear, 1 × hornman | Plate gallery, at the counting-room passage | As E1. Hornman's Gather calls counting-room crew B here unless cancelled | As E1 | The sound puzzle: Rest cancels Gather | 45–70 s (more if crew B joins) |
| **TIW-E5** | Crew A: 1 × spear, 1 × hornman. Crew B: 2 × spear (if not drawn out in E4). **Bersi** (non-combatant) | Counting room | Crews defend the desk; Bersi stays away from the loophole | As E1. Crews fight to 0 HP. **When the last crewman is defeated → Bersi gives up** (quest script, SX-N1) | Climax that ends with a clerk giving up the ledger | 60–90 s |

**Rules**
- **Combat never reveals evidence.** The ledger is picked up from the desk; the sacks, spearheads, plates and sketches are inspected in place; the Iron Winter, the standing orders and "the usual hands" are Bersi's testimony after he gives up.
- **Defeat at 0 HP** (CDR-1). Crews take the ordinary defeat presentation; no yield state, no tied props. The hires are non-combatants who run at the first blow (a scripted reaction to the fight starting, not a health state) and are never enemies.
- **Bersi is never attacked.** He is a non-combatant actor. Player attacks on him are not available (no target).
- **Death:** respawn at the Three Calls Shelter ledge before the hut; at the hoist foot after `S05` (with the cage, if wound, ready). Defeated groups stay defeated. Required inspects and the ledger persist.
- **Co-op:** crews and crows shared. Inspects, the ledger and the choices are per player. Each partner picks up their own ledger (per-player prop on the desk). Bersi's give-up is shared (it plays when the last crewman is defeated); each partner still gets their own ledger item from the desk.

## B8. The discovery moments: presentation specs

### B8.1 The quiet gully (Beat 3)

A null-point, shown before it is named (TF-M4 teaches it; TDS01 is the side discovery). No one explains it here.

| Time | Element | Spec |
|---|---|---|
| Approach | **The haul crew ahead** | Positional voices and a sledge creak from up the track, beyond the gully: "And up. And up." |
| 0 s | **The cut** | As the crew's audio source passes into the gully volume, the voices **stop mid-word** ("And u—"). The creak stops. No fade: a cut. |
| 0–6 s | **The gap** | Wind still plays on the player's side. Nothing from the gully. |
| ~6 s | **The return** | The voices resume beyond the gully, further up, mid-call, as if nothing happened. |
| Player enters | **The quiet** | Inside the volume: footsteps, breath, armour and wind are muted to near zero over 0.5 s. A small cloud of dust from the cut wall **falls straight down** despite the wind outside. Snow-poles' pennants hang still. |
| Player leaves | **The rush** | All ambience returns at once over 0.2 s, slightly loud. |
| UI | | None. The optional inspect is the only text. |

### B8.2 The trial frame (Beat 9) — *the strange moment*

| Time | Element | Spec |
|---|---|---|
| 0 s | **Touch** | The player lays a hand on the largest plate (interaction). The plate rings, a low note, softly. |
| 0.5–2 s | **The rock answers** | A **hum** rises through the room: sub-bass, felt more than heard (controller rumble where supported). It is not music. The lamp flames lean all one way. Dust lifts off the desk and hangs a hand above it. |
| ~2 s | **The crows** | Through the last bay's loophole, **every crow on the cliff lifts at once**: hundreds, silently for half a second, then a roar of wings. The flock wheels out over the pass and does not come back for the rest of the scene. The iron gallery's vents go quiet too. |
| 2–4 s | **Hold** | The hum holds. The other plates on the frame shiver on their cords without being touched. |
| ~4 s | **Stop** | The player's hand damps the plate (automatic). The hum stops when the plate stops. Dust falls. Flames straighten. |
| After | **Bersi** | (given up, on the floor) "Don't. He says it carries." `[SPLINTER]` (`TIW-B9.6`). He means Eyvind's word, not a meaning he knows. |
| After | **Inspect the frame** | *"Five plates on gut cord. A felt mallet. Chalk on the beam: three short strokes and a word, 'hums'."* |
| Never | **Explanation** | Nobody says what it is. Brynjar, if brought (private route), touches nothing on the frame and says "Leave it." It is R07's first seed: the Summit node is not here; this is a plate in a frame, and the cliff answered. |

### B8.3 The ledger line (Beat 9–10)

| Element | Spec |
|---|---|
| The line | In the ledger's receipts, in Bersi's steady hand: *"Relief grain, sixty-eight measures. Received."* Dated **"9 wk to Smoke"** (the ledger counts weeks down to First Smoke, the first true winter night). The current page is "2 wk to Smoke". |
| Recognition (only with `lowmark.main.04_night_flush` Completed) | On reading the line: *"Sixty-eight measures, on the Whinstone account. The bill at the Hollow Lock said the same. But this line is old. It was written weeks before that night on the Cut."* Sets `TIW_LOWMARK_RECOGNISED`. Nothing else: no route, no carrier, no direction, no explanation of why the number and account recur. |
| Without Lowmark MQ4 | The line is an ordinary receipt among others. The relief stencil on the sacks carries R05 on its own. |
| The struck line | *"Nettlehook, children's winter ration, 14 measures"*, struck through with one ruled line; beside it, *"Held. Iron Winter."* The player can read it themselves at any time. Brynjar reads it aloud only on the private route. |

## B9. Quest structure for implementation

### B9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_offer` | Speak to Elira Hearthward at the ridge-market. | `TIW-D1` end | Yes | Offered after TF-M1 Completed and its storm broken. Quest Active on `TIW-D1` accept |
| `S01_market` | Find out who is buying. | `TIW_LEAD_BOARD` + `TIW_LEAD_CHIT` | Yes | Either order |
| `S02_tarp` | Look at the Passwatch store-yard. | Runner-marks inspect + `TIW-D3` end | Yes | Grain-crack inspect optional |
| `S03_track` | Follow the sledge marks. | Enter hut-shoulder volume (K4) | Yes | Fork volumes re-pin; the gully event (`whinstone.gully_quiet`) on the crew audio actor; `TIW_GULLY_HEARD` optional inspect |
| `S04_hut` | Get past the Muster Hut. | (TIW-E1 all defeated) **or** enter ledge-end volume | Yes | Broadsheet pass-by volume on both routes (required); `TIW_HUT_ROUTE`; `TIW_BROADSHEET_READ` optional |
| `S05_shaft` | Find a way into the store. | Front-gate inspect + enter winding-head volume (G3) | Yes | Climb; wind windows in the shaft |
| `S05b_cage` | (optional) Wind the cage up. | 3 × `wind_cage` segments | No | Sets `TIW_CAGE_WOUND`; enables the cage shortcut and respawn path |
| `S06_grain` | Search the store. | TIW-E2 defeated + relief-sack inspect | Yes | `TIW_SACKS_INSPECTED` |
| `S07_iron` | Search the store. | Spearhead inspect + enter plate gallery (via hasp **or** vent crawl) | Yes | `TIW_IRON_SEEN`; `TIW_HASP_SMITHED` if Smithing used |
| `S08_plates` | Search the store. | Plates inspect + sketches inspect + TIW-E4 defeated | Yes | `TIW_PLATES_SEEN`; `TIW_SKETCHES_SEEN`; `TIW_GATHER_CANCELLED` if Rest blown in time |
| `S09_counting` | Confront whoever keeps this store. | TIW-E5 defeated (Bersi gives up) + `TIW_store_ledger` acquired + trial-frame touch | Yes | Server event `whinstone.frame_hum` (per player); `TIW_FRAME_TOUCHED` |
| `S10_bersi` | Question the store-factor. | `TIW-D6` end | Yes | `TIW_BERSI_TESTIMONY`; `TIW_LOWMARK_RECOGNISED` optional |
| `S11_brynjar` | Decide who hears about the store first. | **Private:** `TIW-D7` at the terrace + Brynjar at the counting room + `TIW-D7.40` end. **Public:** `TIW-D8` end | Yes | Sets `TIW_ROUTE` and `TH_BRYNJAR` on the first of `TIW-D7.01` or `TIW-D8.01` |
| `S12_stores` | Decide what happens to the stores. | Option chosen in `TIW-D7.50` (private) or `TIW-D8.30` (public) | Yes | Sets `TH_STORES`. `leverage` only offered in `TIW-D7.50` |
| `S13_elira` | Return to Elira at the ridge-market. | `TIW-D9` end | Yes | `TH_SEASON = snow` on step start; quest → Completed |

### B9.2 Flags

| Flag | Set by | Read by (here) | Read by (later packages) |
|---|---|---|---|
| `TIW_LEAD_BOARD` | Price-board inspect | S01 | — |
| `TIW_LEAD_CHIT` | `TIW-D2` | S01 | TF-M3 (haulier cameo at Carrick's Cut, optional) |
| `TIW_GULLY_HEARD` | Gully inspect (optional) | — | TF-M4 Kaldren null-point lesson (variant: "You've stood in one.") |
| `TIW_HUT_ROUTE` = yard / ledge | S04 | `TIW-B` barks | — |
| `TIW_BROADSHEET_READ` | Broadsheet inspect (optional; the pass-by is required and always places it in view) | — | EH-M1 (Emberholt) optional recognition of the reversed phrase; never a gate |
| `TIW_CAGE_WOUND` | S05b | Private-route ride; respawn | Revisits of the Whinstone Store (TF-M5 lead-in, if any) |
| `TIW_SACKS_INSPECTED` | Required | `TIW-D7`, `TIW-D8` | — (TF-M5 reads only `TH_STORES`, in Elira's `TSW-D9.69a`) |
| `TIW_IRON_SEEN`, `TIW_PLATES_SEEN` | Required | `TIW-D6`, `TIW-D7` | TF-M3 offer (plates) |
| `TIW_SKETCHES_SEEN` | Required | `TIW-D6.30` | **TF-M4** offer (Eyvind's sketches name the Summit's great hall) |
| `TIW_HASP_SMITHED` | Smithing at the forge | Inspect text | — |
| `TIW_GATHER_CANCELLED` | Rest blown within window (E1 or E4) | `TIW-D6.50` (Bersi: "That's cheating.") | *Horn and Silence* (Dorn: "I hear you blew Rest at a crew.") |
| `TIW_FRAME_TOUCHED` | Required | `TIW-D6`, `TIW-D7` | — (Iven's list logs Summit hums only; a plate touched at the Whinstone Store is not on it, so no phenomenon is used to date anything) |
| `TIW_BERSI_TESTIMONY` | `TIW-D6` | S11 | — (TF-M5 neither stages nor cites it) |
| `TIW_LOWMARK_RECOGNISED` | Ledger read or `TIW-D6.40` (MQ4 Completed only) | — | Convergence (two-halves connection chip, optional) |
| `TIW_ROUTE` = private / public | S11 | S12 options | — |
| `TH_BRYNJAR` = disowned / defended | S11 (private → disowned; public → defended) | `TIW-D9` | *Whose Colours*; TF-M5 placement and posture |
| `TH_STORES` = reported / seized / leverage | S12 | `TIW-D9` | TF-M4 crew count; TF-M5 crew strength; Assembly lines; posture (leverage +1 sealed) |
| `TH_SEASON` = snow | S13 start | Season presentation | All Thornfell (bible §9.2) |

### B9.3 Choices and consequences

**How Brynjar learns (`TH_BRYNJAR`).**

| Route | Immediate | Cost | Later |
|---|---|---|---|
| **Privately** (`disowned`): bring him to the store | He reads the struck children's ration himself and disowns the splinter in front of Bersi. He is loud, and he is on the player's side. | Time and a climb. The hall hears nothing yet: the Assembly learns only what the stores outcome tells it. Elira is told after Brynjar, and notices. | Unlocks `leverage` as a stores option. *Whose Colours*: Brynjar trusts the player. TF-M5: he stands where the player can see him; posture +1 open. |
| **In public** (`defended`): report to Hadrik | The hall knows at once. Brynjar defends readiness out of pride before Elira and Torvek. | Brynjar's pride is now on record. He is furious in private and won't say so. `leverage` is not available: too many people heard. | *Whose Colours*: Brynjar is stiff with the player until the banner. TF-M5: posture +1 sealed. |

**What happens to the stores (`TH_STORES`).**

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Reported** (`reported`): Assembly seal | Ressa's Wardens go up the track and seal the store. Bersi and the crews are taken to Passwatch's lock-up for the Assembly. The store becomes a Warden-guarded site. | Hunger holds until the Assembly decides. Elira's allotments stay short through first snow. | Strongest evidence: the full store under seal. TF-M4: fewer Iron Winter crew (their stores are gone). TF-M5: Assembly lines cite the sealed store. No posture weight. |
| **Seized for relief** (`seized`): Elira's storekeepers carry it down tonight | The highsteads eat this winter. Nettlehook gets its children's ration back. The store is empty by morning. | **The evidence is the ledger alone.** The splinter can say the store was a highstead reserve that the Hearthguard robbed. Hadrik has words with Elira. Bersi is handed to the Wardens ("clerks go to wardens, not to ropes"). | TF-M4: fewer crew (no stores). TF-M5: Assembly lines are weaker on the stores ("a book and some empty racks"). No posture weight. |
| **Left as leverage** (`leverage`; private only): keep quiet and watch | Nothing visible happens. Bersi goes back to his desk with a new book and a story about a stranger. Brynjar's people watch the track. | Elira is angry. Hunger holds and the splinter keeps buying: **later scenes show the store still filling** (the grain gallery's ninth bay full; new crates in the plate gallery; the Muster Hut drilling). | TF-M4: more crew at the Summit. TF-M5: stronger splinter crews at the Gatefall; Brynjar's watchers give the player one early warning line. Posture +1 sealed. |

Every outcome keeps the ledger with the player. None is wrong.

## B10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| The ledger (`TIW_store_ledger`) | Quest item / knowledge | Readable at any time; carried to TF-M5 |
| The Whinstone Store | Revisitable site | State by `TH_STORES`: sealed (Warden at the hoist foot), emptied (racks bare, storekeepers' sledge marks), or still filling (crew present; avoid or fight; no quest content) |
| The cage shortcut | Access | If wound: the hoist foot to the winding head in one ride |
| Small payment | Currency | Elira's storekeepers' "finder's share" (reported/seized); none with leverage (Brynjar pays instead, in a clumsy handful of coin) |
| Skill XP | Action only | Melee; Smithing if the hasp was drawn |
| Season | World presentation | `TH_SEASON = snow` |
| Side-quest unlocks | Story | TSL, TFS, TMM, TSN, TGM; TSM (with TNR) |
| TF-M3 | Story | The pay chits to G. Carrick's men lead to Carrick's Cut |

## B11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player takes the wrong fork | A short dead end with a log line; the correct branch re-pins. |
| Player falls off the ledge route | The ledge has a rail; there is no fall. A gust can push the player a step against the rail. |
| Down-draught in the shaft | Push and light damage on the rungs; never a fall (the climb holds). |
| Crow mobs | Damage only; vents give safe windows. |
| Hornman reinforcement | The fight is the same total size; cancelling it is a reward, not a requirement. |
| Death | Respawn at Three Calls (before the hut) or the hoist foot (after S05). Defeated groups stay defeated. Inspects, the ledger and the wound cage persist. |
| Logout in the store | Restore to the persisted step at the hoist foot (cage ready if wound). |
| Walking away before S09 | Quest stays Active. Resume hook: Elira at the market ("Still short. Still counting."). |
| Walking away after S09 | Resume hook: Bersi in the counting room (he has not moved; "Still here. Still not climbing."), and the S11 objective at Stonewake. |
| Brynjar on the private route | He waits at the hoist foot until the player arrives; he cannot be lost. If the player leaves, he goes home and meets them at the hoist foot next time the objective is pursued. |
| Fail state | None. |
| Co-op | Shared enemies. Per-player inspects, ledger item, route and stores choice. The store's fill-level prop follows each player's `TH_STORES` (fallback: the host's). Bersi's give-up is shared; testimony is per player. Brynjar escorts only the player whose route is private; a partner on the public route sees him in the hall (per-player NPC placement; fallback: Brynjar appears at both, each partner's dialogue from their own state). |

## B12. Integration needs

Documented dependencies for a later Systems Engineer. Nothing here is implemented.

| Need | Owner | Minimum viable form |
|---|---|---|
| **Call wheel and listener NPCs** | Systems | From TF-M1. NPC hornmen emit `call_blown(gather)`; the encounter listens for the player's `call_blown(rest)` within a window and cancels the buff/reinforcement. |
| **Null-point volume** | Audio + Systems | An audio-mute volume (footsteps, breath, ambience) with a straight-falling dust VFX; an audio actor whose voice cuts on entering it. Reused by TDS01, TF-M4, TGM. |
| **Tracking trail** | Systems | Runner-groove decals plus fork volumes that re-pin the objective; dead-end log line. |
| **Climb interaction** | Systems / animation | Ladder climb with rest ledges and a gust "hang on" state; agility shortcut with fallback. |
| **Channelled segments with persistence** | Systems | The cage winding (3 segments); the cage as a two-stop lift once wound. |
| **Ridge Crow flock AI and vent draughts** | Gameplay + audio | Flock and diver behaviour; draught windows on a whistle tell that suspend diving. |
| **Bersi give-up (on-defeat quest hook)** | Systems | When the last TIW-E5 crewman is defeated, the quest plays Bersi's give-up (`TIW-B9.3`, `TIW-B9.5`). Bersi is a non-targetable NPC throughout. No encounter-level surrender, timer or proximity trigger (removed, CDR-1). |
| **Scripted presentation** (`whinstone.frame_hum`) | Audio + VFX | §B8.2: hum, lamp lean, dust lift, crow lift (a flock VFX outside the loophole), stop on damp. Per player. |
| **Per-player NPC placement** | Systems / NPC | Brynjar at the hoist foot (private) or in the hall (public); Bersi present or gone by `TH_STORES`. |
| **Per-player site state** | Systems / art | The Whinstone Store's fill props (sealed / emptied / filling) and the Muster Hut's drill (leverage only). |
| **Season state** | Systems / art | `TH_SEASON = snow`: snowfall effect and a short list of snow-covered props (bible §9.2). |
| Creatures | Schema / Gameplay | Iron Winter spear, hornman, crew boss; Ridge Crow flock, diver. |
| Quest item `TIW_store_ledger` | Schema | Non-droppable document with pages (front leaf, receipts, pay chits, allotments) and the conditional recognition line. |
| Lowmark state read | Systems | Read `lowmark.main.02_short_measure` and `lowmark.main.04_night_flush` status for variant text only. |

## B13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Who buys on the Whinstone account** (R05, owned) | An independent Blood-Oath splinter, the Iron Winter, through its factor Bersi. | Emberholt is cornering the passes. | Board, chit, tarp, sledge marks, store, ledger, Bersi's testimony. | Emberholt; the Remnant; the Blood-Oath clan as a whole. | Who signs the standing orders. | TF-M4 (Eyvind names the leader); TF-M5. |
| **How the Lowmark grain reached Thornfell** | Not stated anywhere (FT-03). | — | Relief stencils; "by the usual hands"; with MQ4, the account name and the number. | A trade route; a convoy over the pass. | **Everything about the route, forever.** | None. |
| **Why "sixty-eight measures" recurs** (MQ4 Completed) | Bersi bought relief lots on the same account more than once; the number recurs. Not explained. | — | The ledger line, dated weeks before the Lock night; the bill. | The same sacks; a single shipment. | Any explanation. | None in Thornfell. |
| **The plates** | Salvaged Echohewn horn plates from Shatterfall, for the Wall-Horn. | Scrap. | Grit; Carrick pay chits; Eyvind's sketches; the trial frame. | Building stone; trade goods. | What the horn is and what the Split did. | TF-M3, TF-M4. |
| **The hum** (R07 seed) | Plate resonance coupling with the cliff's Echohewn stone; a disturbance, not a voice. | — | The trial frame; the crows; "He says it carries." | The mountain's warning; a guardian. | The Summit node. | TF-M4. |
| **The broadsheet** (R15 seed) | Splinter rumour; its phrasing will surface reversed in Emberholt. | Somebody's angry poster. | The phrase, unsigned. | It is about Emberholt's forges only. | Its origin and reversal. | EH-M1 / CV-M2 (outside Thornfell). |
| **The quiet gully** | An Echohewn null-point. | Solemn ground. | Voices cut; dust falls straight. | A trick of the cleft. | What null-points were for. | TF-M4; TDS01. |

## B14. Open decisions

1. **TD-1 (splinter leadership):** Bersi is named in `TIW-B9`, `TIW-D6`, `TIW-D7`, `TIW-D8`, `TIW-B9.6`, the chit's initials and the ledger's hand (all tagged `[SPLINTER]`). Eyvind is named only by the sketches' "E." and Bersi's "he". Ingrith is **never named** in this package; crews and hires say "the Quartermaster" (tagged). Eyvind names her in TF-M4.
2. **TD-2 (Brynjar's response):** private → disowned; public → defended, as recommended. If replaced, edit `TIW-D7.40`, `TIW-D8.20` and the flag mapping.
3. **TD-11:** no route stated anywhere; "by the usual hands" is Bersi's only line on it.
4. **Ledger dating [NEW] `[APPROVED — CDR 2026-11-03]`** (two calendars approved): the ledger counts weeks down to First Smoke ("9 wk to Smoke"), which lets the recognition line say "weeks before that night" without a shared calendar. **Coordinated with Act II (independent review):** storekeepers and factors count weeks to First Smoke; Ridge Wardens and hornwrights count days from the first frost on the Passwatch horn rail (Iven's log, Eyvind's record). Both are local reckonings in use at once; no page converts one into the other. Approved by the Director 2026-11-03 (rulings §2).
5. **Nettlehook's children's ration line [NEW]:** the splinter outbid the Hearthguard for a lot already allotted to Nettlehook's children. This is the bible's required trigger for Brynjar's disowning.
6. **Hadrik reads totals, not lines** (public route): this keeps Brynjar from seeing the children's line in public, which is why pride wins. **Confirmed against TF-M5 (independent review):** no TF-M5 line has Hadrik or a defended Brynjar refer to the children's-ration line; Hadrik's TF-M5 knowledge of the stores is the totals he read.
7. **Season change on S13 start:** the first snow falls as the player walks back to Elira. If the season pass wants it on S12, move it.

## B15. Internal review log

| Finding | Revision |
|---|---|
| Bersi stating his authority would spend TF-M4/M5. | He names only standing orders and an unsigned countersign. He never says "the Quartermaster". Crews and hires say "the Quartermaster" as a figure, never as a signature. Ingrith is never named. |
| The ledger's sixty-eight line could imply the Lowmark barge's sacks arrived here. | Dated weeks before the Lock night; the recognition line notes the date and says nothing else. No route, no carrier. |
| The Lowmark callbacks risked gating R05. | The relief stencil carries R05 for every player. Lowmark recognition is optional variant text read from Lowmark quest state. |
| Leverage could be chosen after a public report. | Only offered in `TIW-D7.50` (private route). |
| Combat revealing evidence. | Ledger from the desk; everything else inspected in place; testimony from Bersi, a non-combatant, after he gives up. |
| The hut risked being stealth. | Two routes chosen by walking; the ledge is a traversal route with its own pressure, not a hide. |
| The hires as enemies. | They are clanless hires, "hired, not sworn". They flee on the first blow and are never targets. |
| The trial frame risked becoming a guardian moment. | It is a plate, a hum, crows and dust. It stops when the plate stops. Nobody names it. The Summit node is TF-M4's. |
| The null-point gully risked teaching TF-M4 early. | It is shown, not taught. No one comments; one optional inspect. |
| Sound puzzle needed in TF-M2. | Rest cancels a hornman's Gather (TF-M1's lesson 3, used against the splinter). Optional, rewarded, never required. |
| Skill with crew alternative. | Smithing the hasp is optional; the vent crawl is the walkable alternative. No hard skill gate. |
| Brynjar's ledger limits. | Not a member, didn't know; no war service, no family casualty. His boast is the canon one. He disowns or defends; he is protective of children either way. |
| Elira's line "Brynjar says Emberholt about the weather" might caricature him. | Kept: it is Elira's affectionate exasperation; she defends him in the leverage closing. |
| Agility. | Ledge rail break and shaft crossbar each have walkable fallbacks. |
| **Independent review (2026-11-03)**, TF-M2: 5 findings (2 medium, 3 low). | Calendar coordinated with Act II (weeks-to-Smoke and frost-count coexist; open decision 4). Hadrik-totals rule confirmed against TF-M5 (open decision 6). `TIW_FRAME_TOUCHED` no longer claimed as dating a Summit hum (a phenomenon dating nothing). `TIW_SACKS_INSPECTED`/`TIW_BERSI_TESTIMONY` later-read claims removed (TF-M5 reads `TH_STORES` only). Dialogue: three Bersi nodes tagged `[SPLINTER]`; three em-dash chains removed. |
| **Director rulings reconciliation (2026-11-03)**, TF-M2: CDR-1, CDR-2. | Crews fight to 0 HP in every encounter; steps S04/S06/S08/S09 complete on defeat. The encounter-level surrender (first yield / ~60 s / loophole proximity) is removed: Bersi (SX-N1, non-combatant) gives up when the last TIW-E5 crewman is defeated, then testifies (T-3). Tied crews removed. Integration "Surrender rule" replaced by an on-defeat quest hook. Ranged accepted (divers, hornman). Two calendars labelled approved (open decision 4). |
| **CDR-6 solo-completion sweep, 2026-11-14** | TPW §A11 co-op: host-state sky/bridge/gate fallback marked presentation only; no partner's escort or step waits on another's bridge or gate; a partner leaving or ahead never blocks. |

---

## Act I cross-check (final review)

| Rule | Check |
|---|---|
| Canon anchors | Dorn: codes, altered echoes, "wind tricks"-adjacent; no roster custody. Ressa: refuses a call without explaining; no roster, no battle. Elira: rebuilder, defends Brynjar. Brynjar: not a member; learns in TF-M2; disowns or defends; the canon boast. Hadrik: reads, asks, does not decide. None receives an invented age, service, kinship or record custody. |
| Evidence rule | Sacks, chit, board, tarp, marks, spearheads, plates, sketches and the ledger are found or inspected; the Iron Winter and the standing orders are Bersi's testimony after he gives up. The Close that came early, the quiet gully and the hum identify nothing and prove nothing. |
| FT-03 | No line in either quest states how, when or by which way the Lowmark grain arrived. "Up the track" (TF-M1) is where the sacks are going, not where they came from. |
| No Remnant | None shown or implied. The broadsheet is unsigned and unexplained. |
| Splinter tagging | Every node naming Bersi or Eyvind, and every "the Quartermaster" line, is `[SPLINTER]` in the dialogue file. Ingrith is unnamed in Act I. |
| No fail, no soft-lock | The Close count cannot run out; the escort cannot be lost; Brynjar waits; every required inspect is on the path and persistent. |
| No cutscenes | The early Close, the gully, the trial-frame hum and the first snow all play under the player camera. |
| Solo / co-op | Solo-clearable; per-player state with fallbacks. |
| Movement reality | Click-to-move; every agility trigger has a walkable fallback; no timing-critical input (call windows are generous and optional). |
| Quest items | 1 (`TIW_store_ledger`). |
| Region flags | `TH_CALLS`, `TH_PASSWATCH_ROUTE`, `TH_STORES`, `TH_BRYNJAR`, `TH_SEASON` only. |
| Skills | Melee or ranged (CDR-2; ranged never required); Woodcutting, Smithing (both optional with alternatives). |
| Defeat model | CDR-1: every enemy defeated at 0 HP. Bersi (SX-N1) is the only scripted give-up, and he never fights. |
