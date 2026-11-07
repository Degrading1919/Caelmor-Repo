# The True Line — Lowmark Introductory Quest Package

**Status:** Authored production content for Creative Director milestone review. This package implements Lowmark main-arc **movement 1** ("A crossing that cannot simply stay open") from `00_ADMIN/Reference/Caelmor_Part5_Lowmark_Main_Arc_Architecture.md`. Everything marked **[NEW]** is authored here and is not canon until the Director promotes it. Everything marked **[CANON]** is taken from Phase 1 or the reconciled `LORE/` files. No schema, production JSON, or C# is created here; Section 12 hands the data requirements to the Schema & Content Engineer and Systems Engineer.

**Companion file:** `04_CONTENT_PRODUCTION/Dialogue & Narrative/Caelmor_Lowmark_The_True_Line_Cast_and_Dialogue.md` (cast, Lowmark voice rules, full dialogue, barks).

---

## 1. The quest in one paragraph

The player comes down the Brookhollow road to Whisperflow Landing and finds the crossing stalled: carts, households and a load of Crestbridge grain wait on the bank while barge master Maelin Rowe refuses to cross and a young Crestbridge Keeper insists a paper order makes the crossing "open." The marker post says open. Maelin says the marker is lying. The player reads the bank, tracks the dragged-away old post through the reeds, wades into the shallows to clear its footing, and finds that the old post stood on a carved stone far older than the crossing. After the player cuts and seats a new post on that stone, the river does something nobody at the landing will forget: a thin sheet of water climbs the stone's groove against the current, stands level in the notch for a few breaths, and lets go. The true line reads **shut**. The player proves the old marker was replaced overnight, gets the stranded people and grain to high ground before the river rises, fights off a furrow boar raiding the sacks, and decides who keeps the proof. Nobody learns who moved the post. Everybody learns that someone did.

**What the player should remember:** the moment the water climbed the stone. **What the player should want next:** who moved the post, who carved the stone, and what the Wraithwatcher meant when he said Stillwater has been "thick as wool" all week.

---

## 2. Selection record

Four approaches to movement 1 were evaluated against Phase 1 tenets (11, 14, 16, 18, 19), Pillars A–D, the evidence rule (supernatural effects cannot testify), and the prior audit's finding that proposed quests lean on records and hearings.

| Candidate | Core activity | Verdict |
|---|---|---|
| **A. The paper dispute** — mediate Maelin and the keeper through testimony and the dispatch order. | Talk, compare documents. | Rejected. Repeats the administrative pattern the audit flagged; no exploration, combat, skill use, or wonder. |
| **B. Night Ferry escort** (side-story L-S15 pulled forward) — protect a stranded crowd at night from opportunists. | Combat defense. | Rejected as the opener. Needs human enemies (bandits are mid-tier) and pre-empts the main-arc antagonist decision. Kept as a later side quest. |
| **C. The drifting wreck** — recover sunk cargo from a Wraith-haunted bend. | Combat, salvage. | Rejected. Requires deciding what defeating a Wraith means (open Director decision) and spends Lowmark's main supernatural enemy in minute five. |
| **D. The True Line** — the marker itself is the mystery; the player reads the bank, tracks, fights in the shallows, cuts and seats a new post, and witnesses the river honor an old mark. | Exploration, tracking, traversal, combat, Woodcutting, repair, discovery, defense, choice. | **Selected.** The physical object at the center of the dispute becomes the player's work. The supernatural moment is real, quiet, and non-testimonial. The human wrong is proven by ordinary evidence. Uses canon hooks the audit noted were dropped (the Uphill Canal behaviour, Flood Calendar Stones, Whisperflow's acoustic dead spots). |

Revisions made during internal review are listed in Section 15.

---

## 3. Canon grounding

| Element used | Source | Status |
|---|---|---|
| Arrival amid a delayed crossing; Maelin's judgment vs. keeper paperwork; altered marker; record of pressure; "ends with people and stores made safe, not an anomaly explained" | Main Arc movement 1 | Proposal approved for single-arc structure ("RECOMMEND REVISE", Part 6 ledger); this quest is the selected expression |
| Whisperflow Run: reeds, half-buried old stone markers, acoustic dead spots | Lowmark dossier §IV.1 | [CANON] |
| Collapsed ferry piers along river branches | Lowmark dossier §II | [CANON] |
| The Uphill Canal (water "forgets" gravity when unobserved); Flood Calendar Stones | Lowmark dossier §XI | [CANON] as environmental hooks |
| Riverglass/Riverwarden works help water "hold a line" | Lowmark dossier §XV | [CANON] lore layer |
| Maelin Rowe: calm, observant, refuses passage through specific stretches, never asks what she's hauling | Lowmark anchors §II | [CANON] |
| Tovin Pell: notices reflections that lag, sketches river bends, talks only if asked directly, does not name what he sees | Lowmark anchors §IV | [CANON] |
| Crestbridge Keepers manage tariffs and security; keep records | Lowmark dossier §III | [CANON] |
| Wraithwatchers: lanterns, blessed rope, banner-thistle smoke; no spellcasting | Lowmark dossier §III | [CANON] |
| Silt Swimmers, River Leeches, Marsh Fen Geese, Furrow Boars | Lowmark dossier §VIII, §IX | [CANON] |
| Field-Mage seen as a cloaked figure; mist clinging like a mantle | Lowmark dossier §V.3, §XI | [CANON] rumor |
| Managed renewal coppice as an ordinary wood source | `DESIGNS/Economy Design/Caelmor_Lowmark_Woodland_Content_Portfolio.md` S-WD2 | Proposal-stage economy design |
| Woodcutting, Hunting, Cooking, Melee | Phase 1.3 §5; Stage 3.1 | [CANON] skills; used only at entry level |
| No cutscenes, no spellcasting, solo-first, no faction reputation system | Phase 1.1 §8, Phase 1.2 Pillar D | [CANON] constraints honoured |

**[NEW] in this package:** Whisperflow Landing as a POI, the marker-notch crossing rule, the Marking Stone, Keeper Hollis Avery, Wynn Tarrow, Nan Ferrin, Dace, Wraithwatcher Ansel Corrie, Nan's rhyme, all dialogue, and all mechanics below.

---

## 4. Quest summary card

| Field | Value |
|---|---|
| Working title | **The True Line** |
| Suggested content id | `lowmark.main.01_true_line` (naming is the Schema & Content Engineer's call) |
| Arc position | Lowmark main arc, Act I, movement 1. First authored quest. |
| Prerequisite | None. Auto-offered on first approach to Whisperflow Landing. |
| Solo / co-op | Fully solo-clearable. Co-op players each run their own instance (Pillar D). |
| Target length | 25–35 minutes for a first-time player; ~12 minutes for an informed replay. |
| Combat share | ~20% (three small encounters, one optional). |
| Dialogue share | ~25%, in short exchanges. No conversation longer than six player-facing lines before the player is back in control. |
| Exploration, traversal, skill, repair | ~55% |
| Skills touched | Melee (required), Woodcutting (required, entry level), Hunting (optional), Cooking (optional) |
| Choices | Who keeps the proof (3 options); whether the Marking Stone is made public (2 options) |
| Unlocks | The crossing at Whisperflow Landing; the ability to read any Lowmark crossing marker; movement 2 lead-in |

---

## 5. The place: Whisperflow Landing [NEW POI]

A barge and ferry landing on the Whisperflow Run bend, a short walk down from the Brookhollow road. Exact map coordinates and which settlement lies on the far bank await the POI map (Section 14, item 4). The layout below is relative.

### 5.1 Areas

| Area | Purpose | Environmental storytelling (Tenet 11: tell it through space) |
|---|---|---|
| **A. Road head** | Arrival and first read of the scene. | The road crests and the whole landing is visible: a queue of carts, smoke from a fire, a half-sunk skiff downstream, and one marker post on the bank much paler than the rest. Players who look closely see the problem before anyone explains it. |
| **B. Tollpost and slate** | Hollis's station. | A slate board chalked **CROSSING SHUT — BY THE RIVER** in a weathered hand. Pinned over it, a clean paper notice: **OPEN UNDER EMERGENCY PROVISION**. The pin went through the chalk. |
| **C. Low cart-stand** | Where the waiting crowd sits; Wynn's grain cart. | Sacks bear Crestbridge granary tally marks. A child's chalk game on a flat stone. A caged hen beside Nan's trunk. Wet boots drying on a rail. |
| **D. Crew fire** | Dace, bandaged; Maelin's crew gear. | A coil of sounding line laid out to dry. A broken skiff oar. Dace's boots are soaked to the knee and the left one is torn. |
| **E. The marker bank** | The false post. | Five old grey marker posts down the bank, each with a notch at the same height, and one new yellow post with its notch a hand higher. Fresh earth tamped at its base. Drag marks lead upstream. |
| **F. Reed walk** | Tracking route upstream. | Drag marks through flattened reeds; a snapped reed stem with grey splinters caught in it; a goose nest with a ring of defensive geese. An alternative path runs over a fallen driftroot (agility trigger). |
| **G. The old footing** | The true bend: the discovery site. | A post hole at the waterline. Silt has slumped into it. Something flat and pale shows under the water. The river is audibly quieter here (Whisperflow dead spot). |
| **H. The drowned pier** (optional) | Wreck evidence. | Dace's skiff, holed, caught on a row of black pilings just under the surface: the stumps of a collapsed wartime ferry pier, directly on the line the false post marks. |
| **I. Renewal coppice** | Woodcutting. | Cut-and-regrow stools of straight young stems; a crew tally stick hung on a branch showing which stools were cut this year. |
| **J. High landing** | Night camp, finale. | A grassy terrace above the flood line with old fire rings. It has been used for this before. |

### 5.2 The crossing rule [NEW]

Every Lowmark crossing marker carries one notch. **Water over the notch, the crossing is shut.** River crews and keepers both accept the rule, which is why moving the post is so effective: it turns the river's own warning into a lie without touching any paper. After this quest every marker in Lowmark becomes an inspectable object that tells the player whether its crossing reads open or shut (Section 10).

---

## 6. Player-facing sequence

Each beat lists the objective text the player sees (short, imperative, no quest-giver names in the tracker, per Tenet 22), what the player actually does, and the verbs exercised. Step ids feed Section 9.

### Beat 0 — The Waiting Bank (`S00_arrive`)
**Objective:** *Find out why the crossing has stopped.*
The player crests the road head. Raised voices carry from the tollpost (Maelin and Hollis mid-argument, positional audio, looped until the player approaches). The objective is offered when the player enters area A. There is no quest-giver prompt: the scene is the hook.
**Verbs:** explore, observe.

### Beat 1 — Two Kinds of Open (`S01_hear_both`)
**Objective:** *Hear both sides at the tollpost.*
A short three-way exchange (dialogue node `D1`). Maelin: the marker is wrong. Hollis: the order says open; prove the marker wrong and he'll write it down. Advances when the player has spoken to both.
**Optional leads in the crowd** (each sets a flag that unlocks dialogue options later; none is required):

| Lead | Who | What it gives | Flag |
|---|---|---|---|
| The skiff | Dace (crew fire) | He took the skiff along the marked line at first light and hit "something under the water like a row of teeth." | `TL_LEAD_DACE` |
| The post was grey | Nan Ferrin (cart-stand) | The post was grey when she arrived yesterday evening; it's yellow this morning. Also her mother's rhyme. Also: the carter snored under her cart all night. | `TL_LEAD_NAN` |
| The order | Wynn Tarrow (grain cart) | She shows the dispatch order. It is dated yesterday and says the Whisperflow marker "reads open." | `TL_LEAD_ORDER` |
| The sketch | Tovin Pell (loading sacks) | Only if asked directly. His sketchbook shows this bend with the old post further upstream and a small carved mark at its foot. | `TL_LEAD_TOVIN` |

### Beat 2 — The Wrong Post (`S02_read_post`)
**Objective:** *Examine the new marker post.*
Three inspect points on the yellow post: **notch** ("cut a hand higher than the grey posts'"), **footing** ("earth packed fresh; no silt line on the wood"), **drag marks** ("something heavy was pulled upstream through the reeds"). All three required. Each inspect plays a one-line observation in the player's interaction log and a brief camera-free highlight.
**Verbs:** investigate.

### Beat 3 — Follow the Drag (`S03_find_old_post`)
**Objective:** *Follow the drag marks upstream.*
The reed walk (area F). Two routes:
- **Reed path:** direct, passes the goose nest. Two Marsh Fen Geese defend it (Encounter E1). The player can fight or back off; the geese will not pursue past the reed edge.
- **Root path:** an agility-trigger step down to the mud shelf, then over the fallen driftroot. No combat. Slightly longer.

The drag marks end at the reeds where the **weathered marker post** lies, snapped at the base. Picking it up gives the quest item. A few metres on, at the waterline, the player finds the empty post hole (area G).
**Verbs:** track, traverse, optional fight.

### Beat 4 — Under the Shallows (`S04_clear_footing`)
**Objective:** *Clear the silt from the old footing.*
The hole is at the waterline and the silt can only be cleared by wading in. Entering the shallows starts Encounter E2 (Silt Swimmers and a River Leech). After the encounter, a 3-second channelled interaction **Clear the silt** exposes a flat, pale, carved stone: worn grooves running up its face to a single crisp notch, plus older, fainter notches below. Inspect text: *"Older than the post. Older than the pier. The notch sits exactly where the grey posts' notches sit."*
If the player has `TL_LEAD_TOVIN`, a second inspect line appears: *"It's the mark in Tovin's sketch."*
**Optional side branch** (`S04b_wreck`, can be done any time after Beat 2): wade downstream to the skiff (area H, Encounter E3). Inspecting the pilings sets `TL_EVIDENCE_PILINGS`: *"The false post's line runs straight over a drowned pier."*
**Verbs:** fight, wade, interact.

### Beat 5 — A Post Worth Trusting (`S05_cut_post`)
**Objective:** *Cut a new marker post from the coppice.*
Maelin arrives at the footing (she has followed the player up the bank) and confirms the old post is snapped past saving. She points to the renewal coppice and, if the player has no cutting tool, hands over a **crew hatchet** (loaned quest tool; see Section 11). The player harvests one **marker stem** from a coppice stool using the standard Woodcutting gather interaction at entry level. Only marked stools are harvestable for this step (the crew tally stick shows which), so the player cannot strip the stand.
**Verbs:** gather (Woodcutting).

### Beat 6 — The River Reads Its Mark (`S06_seat_post`) — *the discovery*
**Objective:** *Set the new post on the old stone.*
Two interactions at the footing:
1. **Cut the notch** (3 s channel). The stone's crisp notch is the guide; the player is matching the river's old mark, not choosing a height.
2. **Seat the post** (3 s channel).

On completion, the discovery event plays in-world, under full player camera control, with no text, no music sting and no UI. See Section 8 for the full presentation spec. In short: the river's sound drops away, a thin sheet of water climbs the groove against the current, stands level in the notch, and holds for about four seconds before releasing. Reflections on the shallows lag the player by a fraction of a second while it holds. If the player is facing the far bank during the hold, a still grey figure stands at the treeline; it is gone when the hold ends.
Maelin is present and silent through it, then speaks one line (dialogue `D6`). The true line reads **shut**.
**Verbs:** repair, witness.

### Beat 7 — Prove It (`S07_prove`)
**Objective:** *Show Hollis what the river says.*
Return to the tollpost with the weathered post. Dialogue `D7`. The player presents evidence; each lead the player gathered unlocks one option. The beat completes as soon as the player gives **any two** of:

| Evidence | Requirement |
|---|---|
| The two notches don't match | Always available (the weathered post in inventory) |
| The post was changed overnight | `TL_LEAD_NAN` |
| The marked line runs over a drowned pier | `TL_EVIDENCE_PILINGS` or `TL_LEAD_DACE` |
| The order was written before the post was changed | `TL_LEAD_ORDER` and `TL_LEAD_NAN` |
| Tovin's sketch shows the old position | `TL_LEAD_TOVIN` |

A player who explored nothing optional still has the notch evidence and can ask Hollis to walk to the bank and look (a guaranteed second proof: Hollis inspects both posts himself). Nobody is soft-locked.
When the order-date evidence is presented, Hollis realizes someone *expected* the marker to read open before it did. He takes down the paper notice and closes the crossing on the keepers' authority. Wynn is not accused; Nan's testimony that Wynn slept under her cart is available to rule Wynn out if the player suspects her.
**Verbs:** argue with evidence (short).

### Beat 8 — Move It Uphill (`S08_high_ground`)
**Objective:** *Help move the waiting people and grain to the high landing.*
The river is rising (it read shut for a reason). Maelin calls the move. The player:
- carries **3 grain sacks** from Wynn's cart to the high landing (each is a short carry: one interaction to lift, one to set down; the player can sprint while carrying), and
- helps **Nan's trunk** up the bank (one carry; Nan walks alongside with the hen and talks).

On the third sack, a **Furrow Boar** comes out of the field edge for the grain stack (Encounter E4). It is the quest's combat climax. Crowd NPCs scatter to the high landing; the boar targets the grain stack until the player engages it.
**Optional:** after the fight, the boar is a Hunting harvest target at entry level. Cooking its meat at the high-landing fire and offering it to the crowd (`S08b_feed`) unlocks a warmer variant of the epilogue and a line from Dace.
**Verbs:** carry, fight, optional Hunting and Cooking.

### Beat 9 — Who Keeps the Proof (`S09_choose`)
**Objective:** *Decide who keeps the evidence.*
At the high landing, Maelin and Hollis both want the weathered post and (if obtained) the order. Dialogue `D9` presents the choice (Section 9.3). After it, Maelin asks about the stone (second choice).
**Verbs:** choose.

### Beat 10 — Night at the High Landing (`S10_night`)
**Objective:** *Speak with Maelin by the fire.*
An open-ended camp. Everything here is optional except the final conversation with Maelin:
- **Wraithwatcher Ansel Corrie** walks in on patrol with a lantern and banner-thistle smoke. He marks the bend in his patrol book and says the fog over Stillwater has been "thick as wool" all week and that two other bends "ran wrong" this month. (Hook: movement 3.)
- **Nan** hums an old tune and calls it "the listeners' tune." She doesn't know who the listeners were. (Hook: Riverwarden Lullaby.)
- **Tovin**, if asked, says he drew that notch years ago "and thought it was me seeing things." The player can tell him it wasn't. (Payoff for his arc; sets `TL_TOVIN_TRUSTED`.)
- **Dace** apologizes to Maelin if the player fed the camp; otherwise he sulks by the fire.

The final talk with Maelin completes the quest: the water will fall by morning, and when the true post reads clear she will take the player across first.
**Verbs:** listen, explore (all optional).

### Completion
Quest state → Completed. Crossing service at Whisperflow Landing becomes available to the player (Maelin's crossing interaction). Marker reading is enabled region-wide. Movement 2 lead-in becomes available at Crestbridge (Section 10).

---

## 7. Encounters

All encounters use the game's standard combat: auto-attack on tick, weapon cooldown specials, readable telegraphs, no flee-at-low-HP (Phase 1.3 §2); every creature fights until defeated at 0 HP (CDR-1). Every encounter accepts melee or ranged and none requires ranged (CDR-2). Tuning targets assume a fresh character with the onboarding starter melee weapon and no armor. Final numbers belong to Gameplay Designer tuning after a playable build exists; the targets below are the acceptance bar.

| Id | Enemies | Placement | AI role (Phase 1.3) | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **E1** | 2 × Marsh Fen Goose | Reed path nest | Defensive: engage within nest radius, do not pursue past reed edge | Neck stretch + hiss (~1 s) before wing-beat | Teaches threat radius and that avoidance is legitimate | Avoidable. If fought: <5% of player HP lost per hit; fight ends in ~20 s |
| **E2** | 3 × Silt Swimmer, 1 × River Leech | Shallows at the old footing (water volume only) | Silt Swimmers: Aggressive inside water volume, leashed to water. Leech: Aggressive, slow | Swimmers: ripple line toward player (~0.8 s). Leech: rears up (~1.2 s) before latching | Teaches telegraph reading and stepping out of a hazard (latch breaks if the player steps onto dry bank or lands two hits) | Required. Player ends at 50–75% HP on a first attempt; death possible only through ignoring every telegraph |
| **E3** | 1 × River Leech, 2 × Silt Swimmer | Wreck shallows | As E2 | As E2 | Optional repetition at slightly higher density; rewards curiosity with evidence | Optional |
| **E4** | 1 × Furrow Boar | Field edge → grain stack, high landing approach | Aggressive once at the grain; targets grain stack until engaged | Paws the ground and lowers its head (~1.5 s), then a straight-line charge. Sidestepping makes it overrun and pause, exposed (~2 s) | Combat climax: spacing and commitment (Pillar B). Readable and fair | Required. 45–75 s fight. A player who sidesteps charges takes little damage; one who stands still can lose the fight |

**Rules for all encounters**
- Combat cannot reveal evidence. Nothing dropped by a creature advances the investigation (evidence rule).
- No respawns during the step that requires them. E2 and E4 creatures respawn only after the quest's step has passed, and then as ordinary world wildlife.
- **Death:** respawn at the crew fire with quest step and quest items intact. No item loss for quest items (Phase 1.1 non-negotiable: no overly punishing death penalties).
- **Co-op:** world creatures are shared. Each participating player whose quest instance is on the relevant step receives step credit. Loot follows the game's instanced/fair loot rule.

---

## 8. The discovery moment: presentation spec

This is the quest's centerpiece. It must feel strange and quiet, never like a spell or a boss intro.

| Element | Spec |
|---|---|
| Trigger | Server event on completion of **Seat the post** (`S06_seat_post`). |
| Duration | ~10 s total: 2 s quiet, ~4 s climb and hold, ~2 s release, ~2 s return of sound. |
| Audio | River ambience at area G ducks to near silence over 1.5 s (reuses the Whisperflow dead-spot behaviour). No music. Player footsteps remain audible. A single soft lap of water as the sheet releases. |
| Water | A thin, clear sheet (a few centimetres deep, the width of the groove) runs *up* the stone against the current, reaches the notch, and stops level with it. It holds. It releases back into the river all at once. |
| Reflections | During the hold only, reflections on the shallows within ~10 m lag the player's movement slightly. |
| Far bank | A static, cloaked grey figure at the far treeline, visible only during the hold and only if within the player's view frustum when the hold starts. Mist clings at its shoulders. No interaction, no name, no pronoun. Not visible to co-op partners whose camera isn't facing it (client-side presentation). |
| UI | None. No objective popup until the sound has returned. |
| Camera | Never taken from the player (no cutscenes, Phase 1.1 §8). |
| Repeatability | Plays once per player, on their own seat event. Afterward, the stone is an inspectable object with the text: *"The groove is dry. The notch is level with the post's."* |
| What it means | It tells the player the true line reads **shut** today. It does **not** say who moved the post, name anyone, or answer anything. Maelin's reaction confirms it is rare but not unheard of. |

**Author truth (proposal, for the mystery ledger):** the stone is a flood-timing mark from the old works that once tuned this bend's channel. Where those works still survive, water sometimes "holds a line" (dossier §XV language) when the channel is disturbed and the mark is restored. Crossing crews kept seating posts on the stone for generations because the rule worked, without knowing the reason. The behaviour is bounded resonance, not a judgment, record, or presence. See Section 13.

---

## 9. Quest structure for implementation

### 9.1 Steps and completion events

| Step | Player objective | Completes on (server-recognized event) | Required | Notes |
|---|---|---|---|---|
| `S00_arrive` | Find out why the crossing has stopped. | Player enters area-A volume | Yes | Quest moves Inactive → Active on this event (auto-accept; Stage 15.2 permits) |
| `S01_hear_both` | Hear both sides at the tollpost. | Dialogue `D1` reaches end node | Yes | Leads (Nan, Dace, Wynn, Tovin) available from here until `S07` completes |
| `S02_read_post` | Examine the new marker post. | 3 inspect events on post (notch, footing, drag) | Yes | Any order |
| `S03_find_old_post` | Follow the drag marks upstream. | Player picks up `weathered_marker_post` | Yes | |
| `S04_clear_footing` | Clear the silt from the old footing. | Interaction `clear_silt` complete | Yes | Interaction disabled while any E2 creature is alive and engaged |
| `S04b_wreck` | (Optional) Inspect the wreck. | Inspect event on pilings | No | Available from `S02` onward |
| `S05_cut_post` | Cut a new marker post from the coppice. | `marker_stem` added to inventory | Yes | Loan `crew_hatchet` on `D5` if player lacks a cutting tool |
| `S06_seat_post` | Set the new post on the old stone. | Interactions `cut_notch` then `seat_post` complete | Yes | Fires discovery event (Section 8). Consumes `marker_stem` |
| `S07_prove` | Show Hollis what the river says. | Dialogue `D7` reaches a proof-accepted node | Yes | Requires 2 proofs (Section 6, Beat 7) |
| `S08_high_ground` | Help move the waiting people and grain to the high landing. | 3 sack-deposit events + trunk-deposit event + E4 boar defeated | Yes | Boar spawns on third sack lift |
| `S08b_feed` | (Optional) Cook for the camp. | Player gives cooked food item to camp NPC | No | |
| `S09_choose` | Decide who keeps the evidence. | Dialogue `D9` choice nodes resolved (evidence + stone) | Yes | |
| `S10_night` | Speak with Maelin by the fire. | Dialogue `D10` end node | Yes | Quest → Completed |

### 9.2 Flags (persisted with the quest instance)

| Flag | Set by | Read by |
|---|---|---|
| `TL_LEAD_DACE`, `TL_LEAD_NAN`, `TL_LEAD_ORDER`, `TL_LEAD_TOVIN` | Optional crowd dialogue | Stone inspect variant, `D7` options, `D9` stone variant |
| `TL_EVIDENCE_PILINGS` | `S04b_wreck` | `D7` options |
| `TL_NAN_ALIBI` | Nan's alibi line for Wynn | `D7` Wynn-suspicion branch |
| `TL_HOLLIS_SAW_ORDER` | `D7` order-date proof | `D7` closing line variant |
| `TL_FED_CAMP` | `S08b_feed` | `D10` variants (Dace) |
| `TL_TOVIN_TRUSTED` | `D10` Tovin exchange | Movement 6 (Tovin's pattern), later Tovin barks |
| `TL_EVIDENCE_KEEPERS` / `TL_EVIDENCE_RIVERFOLK` / `TL_EVIDENCE_PLAYER` | `D9` (exactly one) | Movement 2 opening variant; Hollis/Maelin later barks |
| `TL_STONE_PUBLIC` / `TL_STONE_KEPT` | `D9` (exactly one) | Landing prop state; movement 9 (Riverwarden works) |
| `LM_TL_EVIDENCE` (region flag: keepers / riverfolk / player) | Quest completion, copied from whichever `TL_EVIDENCE_*` is set | Main quest 2 lead-in; main quest 10 evidence chip (see the v1 production bible §9) |

### 9.3 Choices and consequences

There is no faction reputation system in Lowmark content (Phase 1.1 §8). Consequences are carried by flags that change dialogue, world props at the landing, and how movement 2 opens. No option is wrong; each reflects a real Lowmark authority (Main Arc thesis: authority is split among people who do necessary work).

**Choice 1 — Who keeps the proof**

| Option | Immediate result | Cost | Later (movement 2 and beyond) |
|---|---|---|---|
| **Give it to Hollis** — *"Put it in the keepers' record."* | Hollis logs an altered marker and sends a rider to Crest Hall at first light. The paper notice is burned at the tollpost. | Maelin: "Paper's slow. Hope it's honest." Her crews wait for the keepers instead of acting. | Movement 2 opens at Crestbridge with Hollis's report already on Corvin Tath's table; the player is named in it. |
| **Give it to Maelin** — *"Let the river crews handle it."* | Maelin will walk every marker on the Run with her crews before any paper moves. | Hollis logs the closure but not the cause. "Then it never happened, as far as Crest Hall knows." | Movement 2/3 opens with Maelin's crew having found a second tampered marker; Crestbridge has no record of the first. |
| **Keep it yourself** — *"I'll hold on to it until someone can tell me who wrote that order."* | Player keeps the weathered post and order as quest items. | Both are put out. Maelin: "Then don't lose it." Hollis: "You're not a keeper." | The player carries the proof into movement 2 and chooses where to present it; it can be presented at the movement 10 hearing. |

**Choice 2 — The stone**

| Option | Immediate result | Later |
|---|---|---|
| **Make it public** — *"Everyone who crosses here should know it's there."* | Hollis records the stone as the landing's reference mark. Tovin draws it for the record (if `TL_LEAD_TOVIN`). A chalk ring appears around the footing. | Ambient visitors come to look. In movement 9, the keepers' record is the first written trace of the old works. The record also makes the stone findable by anyone who might want to move it. |
| **Leave it under the post** — *"The post does the job. Leave the stone where it is."* | Only Maelin, Tovin and the player know. Maelin's crews start quietly checking other old footings. | In movement 9 the player and Maelin know where to look; no institution does. |

---

## 10. Rewards and unlocks

The reward is access, knowledge and a working tool, not power (Main Arc: "the player leaves with meaningful trust rather than new combat power").

| Reward | Type | Notes |
|---|---|---|
| Crossing at Whisperflow Landing | Access | Maelin's crossing interaction is enabled. Opens the far-bank route (destination awaits the POI map). |
| **Reading the river** | Knowledge | Every crossing marker in Lowmark becomes inspectable and returns one line: *"Water's under the notch. The crossing reads open."* / *"Water's over the notch. The crossing reads shut."* Uses the existing inspect interaction. Knowledge-based efficiency (Pillar A). |
| Crew hatchet | Tool | If loaned in Beat 5, Maelin tells the player to keep it. Entry-level cutting tool. Stats and item definition belong to the item pass. If the player already had a tool, no hatchet is given. |
| Small payment | Currency | From Hollis (keepers' waiting-wage) or Maelin (crew share), whichever the evidence went to; from Wynn if the player kept it. Amount: provisional, sized to roughly one early meal-and-repair's worth; set during economy tuning. No currency name is selected yet. |
| Skill XP | Action XP only | Woodcutting, Melee, Hunting and Cooking XP come from the actions themselves under the approved fixed-base XP architecture. **No lump quest XP.** Progression comes from mastery, not completion payouts. |
| Movement 2 lead-in | Story | Variant depends on Choice 1. |

### Quest items

| Item | Source | Fate |
|---|---|---|
| `weathered_marker_post` | Reeds, Beat 3 | Given away in Choice 1 (or kept) |
| `dispatch_order` | Wynn hands it over during `D7` if `TL_LEAD_ORDER` | Follows Choice 1 |
| `marker_stem` | Coppice, Beat 5 | Consumed by `seat_post` |
| `crew_hatchet` | Loaned in Beat 5 if needed | Kept by the player at completion |
| `grain_sack`, `nan_trunk` | Carried in Beat 8 | Carry-state objects, never enter inventory |

That is 3 quest items against the Phase 1.5 budget of 8–12 for all of Lowmark (the Lowmark milestone). The hatchet is a reward tool, not a quest item.

---

## 11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player dies | Respawn at the crew fire. Step, flags and quest items are kept. |
| Player logs out mid-quest | Stage 15/13 rules: restore the last persisted step and flags; in-progress channels and carries are discarded and must be redone. A dropped sack returns to the cart. |
| Player leaves the area | No failure. The quest waits. NPCs stay in their step-appropriate positions. |
| Player sells or drops a quest item | Quest items are not droppable or sellable. |
| Player has no cutting tool | Hatchet loan (Beat 5). |
| Player skips optional leads | Notch evidence plus Hollis's own inspection guarantee the two proofs (Beat 7). |
| Walking away | No abandon (Stage 15.2: Inactive, Active, Completed only). The quest stays Active at its current step; the next approach to the landing re-prompts with a resume line. This is Lowmark's first main-arc quest, so it must always be resumable (Section 12). |
| Failed state | None. This quest cannot fail. |
| Co-op | Each player has their own quest instance (Stage 15.1). Shared world creatures give step credit to every participant on that step. Step-conditioned props (post, notice, chalk ring) are presented per player from their own quest state (Section 12). The discovery plays for each player on their own seat event; partners present see the water for their own seat only. |

---

## 12. Integration guidance for the technical team

### 12.1 What already exists

- `CODE/Systems/QuestRuntimeSystem.cs` implements quest-level state (Inactive/Active/Completed) with server-authoritative transitions, a progression evaluator interface and a mutation gate (Stages 15, 22.2, 27).
- Combat runtime, inventory runtime and NPC runtime systems exist in `CODE/Systems/` with validation scenarios.
- Gathering resolution and inventory grant designs exist in `DESIGNS/Networking & Persistence/`.
- Movement agility triggers are approved in Phase 1.3 §1.

### 12.2 What this quest needs that does not yet exist

None of these is a new core system. Each is a field or contract the roadmap already lists.

| Need | Owner | Roadmap task | Minimum viable form |
|---|---|---|---|
| **Step-level objectives and flags** inside a quest instance | Schema & Content Engineer (schema), Systems Engineer (runtime) | 31.3 Quest Content Schema; 24.1 Quest State Runtime | Ordered steps with an objective text key, a completion predicate over server events (enter-volume, inspect, interaction-complete, item-acquired, creature-defeated, dialogue-node-reached, item-given) and a required/optional marker; a per-instance bag of boolean flags. Persist step index + flags + optional-step completion. |
| **Dialogue content** with conditions and flag writes | Schema & Content Engineer, Systems Engineer | 31.5 Dialogue/Interaction Content Schema; 35.2 NPC Interaction Sets | Nodes with speaker, line key, player options, show-conditions (flags, step, item-held) and effects (set flag, give/take item, emit dialogue-node-reached event). The companion file is written against this shape. |
| **NPC definitions** for 7 NPCs with step-conditioned positions | Schema & Content Engineer | 31.2 NPC Definitions Schema; 33.2 Lowmark NPC Set | Position sets keyed by quest step (tollpost/fire/high landing). |
| **Inspect interactions** with text | Systems Engineer | 33.1/33.7 world binding | Interaction volume → server event + one localized line. Reused for marker reading. |
| **Channelled interactions** (clear silt, cut notch, seat post) | Systems Engineer | 33.5-style station binding | Fixed 3 s channel, cancel on move or damage. |
| **Carry state** (sacks, trunk) | Systems Engineer | — | Simplest form: an interaction that toggles a carried-prop state and a deposit volume. If carry state is too costly for the slice, fallback: the sacks become three "Lift and stack" interactions at the cart that each move one sack prop up the bank. Design intent survives either way. |
| **Quest-state-conditioned props** (yellow post vs. new post, notice on/off, chalk ring) | Systems Engineer | 33.1.B2 zone binding | Client presentation keyed on the local player's quest state. **Fallback** if per-player presentation is not ready: leave the yellow post in place permanently as "the old false post the keepers left as a warning," add the new post beside it, and carry all state through dialogue. |
| **Discovery event presentation** | Systems Engineer + art | — | One server event (`true_line.stone_holds`) that clients play as a local, time-limited water-sheet and audio-duck effect. No gameplay state depends on it. |
| **Encounter pockets** E1–E4 with step-gated spawns | Schema & Content Engineer (data), Systems Engineer (spawn rules) | 33.7 Encounter Pockets | Spawn on step entry; despawn/normal wildlife after step passes. |
| **Resume hook after walking away** | Schema & Content Engineer, Systems Engineer | 34.5 Quest Interruption & Recovery | The quest stays Active at its persisted step; next area-A entry plays a resume prompt for that step. No new instance and no state change (Stage 15.2 has no abandon or fail). |
| **Creature definitions** for Silt Swimmer, River Leech, Marsh Fen Goose, Furrow Boar | Schema & Content Engineer, Gameplay Designer | 33.7, enemy family pass | Roles and telegraphs per Section 7. |

### 12.3 Recommended build order (shortest path to a playable slice)

1. Steps + flags in the quest schema and runtime (unblocks everything).
2. Dialogue schema minimal subset: linear nodes, options with flag conditions, flag/item effects.
3. Inspect + channelled interactions.
4. Beats 0–3 and 7 playable with placeholder art (proves the investigation loop).
5. Encounters E2 and E4.
6. Woodcutting stem + seat-post + discovery event.
7. Beats 8–10, choices and flags.
8. Fallbacks replaced by per-player props only if time allows.

### 12.4 Acceptance test (milestone bar)

A fresh solo character, with no prior knowledge, can:
1. Reach `S10_night` complete without external instructions, using only on-screen objectives and dialogue, in 25–45 minutes.
2. Complete the quest taking **only** required steps, and separately complete it taking every optional lead, with both runs reaching Beat 7 with at least two valid proofs.
3. Die in E2 and E4 and recover without losing progress.
4. Log out at Beats 3, 6 and 8 and resume correctly.
5. Make each Choice 1 option in three runs and see the matching flag persisted and the matching `D10`/movement-2 variant.
6. Witness the discovery with no UI, camera takeover or text, and afterwards find the stone's dry-groove inspect text.
7. In 2-player co-op, both players complete independently with neither blocked by the other's step.

Playtest questions to ask afterwards (the real bar): *What was the strangest thing you saw? Who do you think moved the post? Where do you want to go next?*

---

## 13. Mystery ledger entries

Uses the Part 5 author-truth/public-belief/evidence/wrong-reading/reveal-owner method (Part 6: "RECOMMEND CANON AS CONTROL").

| Mystery | Author truth (proposal) | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Who moved the Whisperflow post** | Replaced overnight by someone acting for the present interest that is using emergency procedure to keep grain moving (Main Arc movement 4). Identity and social placement **deliberately unselected** (Section 14, item 1). | Maelin is being difficult; paperwork error; the river "moved it." | Notch height, fresh earth, drag marks, snapped original post, Nan's testimony, the order dated before the change, the drowned pilings on the false line. | Wynn did it (she profits); Hollis did it (he enforces the order). Both are ruled out by testimony or conduct. | Who issued the order; whether other markers were moved. | Main arc movements 2 and 4. |
| **The Marking Stone** | A flood-timing mark from the old works that once tuned this bend; bounded resonance lets water hold a line there when the channel is disturbed and the mark restored. It records nothing and judges nobody. | Unknown to the public. Survives only as Nan's rhyme and the crews' habit of seating posts on "the old stone." | Grooves and notches older than the pier; the rhyme; Tovin's sketch; the water climbing to the notch. | The stone is a magic battery; the river is alive and judging; the stone is a grave marker; the Field-Mage made the water move. | Who carved it; how many such stones exist (Flood Calendar Stones). | Movement 9 (Riverwarden works). |
| **The figure on the far bank** | Left open. Compatible with the Field-Mage rumor; this quest never confirms it. | "The Field-Mage's Mantle": mist that clings around shrines. | A grey figure visible only during the hold, if the player is looking. | The figure caused the water to move. | Everything. | Movement 8 (the Field-Mage). |

---

## 14. Genuinely unresolved decisions

These need the Creative Director. The quest is built to work with any answer to each; none blocks implementation of this quest.

1. **Who moved the post and issued the order (the main-arc antagonist).** The order carries an issuer's mark that Hollis does not recognize; its text, seal and signer are placeholders until this is decided. *Recommendation: keep the issuer unnamed in this quest regardless of the decision. Revealing it in movement 1 would spend the arc's first mystery.*
2. **Who the player is and why they are on the Brookhollow road.** All dialogue is origin-neutral and address-neutral (no name, gender, homeland or prophecy). If origins become selectable, one variant line at `D1` and one at `D10` is enough. *Recommendation: keep "ordinary wanderer" (Phase 1.1 §6).*
3. **Is Whisperflow Landing the player's first location?** This ties to item 2 and Stage 14 onboarding placement. *Recommendation: yes. The road head is a strong first view, and the quest teaches movement, inspection, combat, gathering and choice in order.*
4. **POI map placement.** Which settlement lies across the crossing, the landing's distance from Brookhollow, and the phase 1.5 vs. dossier subzone list. The design uses relative placement only.
5. **Canon promotion.** Whether to promote Whisperflow Landing, the marker-notch rule, the Marking Stone and the five new NPCs into `LORE/`. Until then they are authored content.

Two related decisions remain open but are **not needed** by this quest: what defeating a Wraith means (the quest has no Wraith fight by design; the Wraithwatcher only foreshadows), and the Last Field-Mage's characterization (the far-bank figure is pronoun-free and never confirmed).

Decided here under delegated authority and recorded for review: no lump quest XP; the quest cannot fail and cannot be abandoned (walking away leaves it Active and resumable); reward is access, knowledge and a tool.

---

## 15. Internal review log

| Review finding | Revision |
|---|---|
| First draft had the river "reveal" the moved post by flowing toward it. That made the river testify. | The water now only reads the notch (open/shut). People and objects prove the tampering. |
| First draft used a Wraith at the footing. | Removed. Spends Lowmark's signature enemy too early and depends on an open Director decision. Replaced with Silt Swimmers and a River Leech, which the dossier places in exactly these shallows. |
| Beat 8 originally needed six sack carries. | Cut to three plus the trunk, with the boar interrupting the third, so the carrying never becomes a fetch chore (Phase 1.1: no filler). |
| Proof step could soft-lock a player who skipped every lead. | Hollis can walk to the bank and inspect both posts himself as a guaranteed second proof. |
| Wynn read as an obvious villain. | Kept as a red herring, ruled out by Nan's testimony. The player's suspicion is useful; the game should not punish it. |
| Hollis read as heartless (the "plausible wrong reading" the Main Arc predicts). | Gave him a reason: the far bank is waiting on grain, and the order is the procedure he was trained to trust. He changes his mind on evidence. That is his arc. |
| Choice 1 originally had a "wrong" answer (keeping the evidence lost the crossing). | All three options now resolve safely, with different costs and later doors. |
| The far-bank figure risked confirming the Field-Mage. | Made optional, view-dependent, unnamed and pronoun-free. |
| Skill coverage drifted toward the 14-skill economy list. | Limited to Melee, Woodcutting, Hunting and Cooking, which appear in both Phase 1.3 and Stage 3.1. |
| Director rulings reconciliation (2026-11-03, CDR-1/2/3). | No yield or non-lethal content existed here. §7 now states the 0 HP defeat rule and that every encounter accepts melee or ranged (ranged never required). "v1" release wording changed to "the game's" / "Lowmark content" / "the Lowmark milestone"; the "v1 production bible" document reference keeps its file label. No beats, steps or flags changed. |
