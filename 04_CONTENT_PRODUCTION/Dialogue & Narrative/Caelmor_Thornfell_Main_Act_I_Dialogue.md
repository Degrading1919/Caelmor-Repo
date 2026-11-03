# Thornfell Main Act I: Cast and Dialogue (The Closing of Passwatch, The Iron Winter Stores)

**Status:** Authored production content for Creative Director milestone review. This is the companion to `04_CONTENT_PRODUCTION/Quests/Caelmor_Thornfell_Main_Act_I.md`, which owns step ids, flags and mechanics. Characters marked **[CANON ANCHOR]** come from `LORE/Characters/Caelmor_Characters_Region2_Thornfell_Anchors (Not Full List).txt` and obey the Thornfell rows of the Part 4 character ledger: nothing here gives them a new age, wartime service, kinship, travel, meeting or record custody. Characters marked **[NEW]** are authored and not canon until promoted. Every node that names Ingrith Scarrow, Bersi Coldbrook or Eyvind Stall, or refers to the splinter's leader as "the Quartermaster", is tagged `[SPLINTER]` (bible §3.1). Ingrith is never named in Act I. Nothing here is production JSON.

**Node format** (Lowmark standard): `NODE SPEAKER: "Line." (stage note)`; conditions in braces or brackets before the line; player options as `> [condition] "Option." → NEXT {effect}`. Ids follow bible §11.2: dialogue `<CODE>-D<n>.<nn>`, barks `<CODE>-B<n>.<nn>`, inspect texts in `-I` tables, documents in full.

**Voice rules (bible §5.3, binding):** few words; a long speech means fear or anger. Nobody calls anything magic: wind has moods, stones remember, echoes are tricks. Weather is grammar. Strangers are "walker". Humour is dry and at the speaker's own expense. Emberholt is distrusted rationally, never caricatured.

---

## Part 1: Act I voice additions

| Item | Status | Use |
|---|---|---|
| **"Walker."** | [CANON practice, bible §5.3] | Every Marcher addressing the player. |
| **"A fifth before the gust."** | [NEW] The fluted-face whistle tell. | Aud, wardens, crews. |
| **"The hard wind" / "the forgiving wind"** | [NEW] | Everyone. The forgiving wind is the one you can work in. |
| **"Under the bar."** | [NEW] Warden habit: shelter faces are marked with a white bar. | Dorn, Aud, Vessa. |
| **"Closing day."** | [NEW] Any day a gate shuts for weather. | Passwatch. |
| **"Two over."** | [NEW] Market phrase: two over the Stonewake board. | Elira, the haulier, the price board. |
| **"Up the track."** | [NEW] Where things go that nobody wants to name. | Storekeeper, haulier. |
| **"Wk to Smoke"** | [NEW] Ledger dating: weeks counted down to First Smoke. Storekeepers' and factors' reckoning. It coexists with the Ridge Wardens' frost-count (days from first frost on the Passwatch horn rail; Act II); neither is converted into the other on any page. | Bersi's ledger; storekeepers. |
| **"Rest ends any call."** | [NEW] Hornbearer teaching. | Dorn; used against a crew in TF-M2. |

**What nobody in Act I says:** how or from where the relief grain came; who signs the standing orders; Ingrith's name; what the hum is; why the Close came back early; what the interval Ressa stopped was; that anything is magic.

---

## Part 2: Cast notes

### TF-M1

#### Vessa Galt, Ridge Warden sergeant at the Passwatch gate [NEW]
- **Role:** keeps the gate. Decides the storm closure on hazard grounds.
- **Want:** everyone inside by dusk. **Fear:** the patrol pair she can't count.
- **Knows:** the storm, the loads beyond the Narrows, that the gate shuts until the storm breaks. That closures are written as "what we closed". **Doesn't know:** the Whinstone Store (she has never heard the name); the sacks' account (not her yard).
- **Voice:** short sentences, dry. Follows the rule and dislikes that it is the rule. Says "walker" until the gate shuts behind the player, then still says "walker", but differently.

#### Dorn Feldhorn, Veteran Hornbearer [CANON ANCHOR]
- **Canon:** maintains the long-range horn codes; ritual seriousness and private fear; claims echoes sometimes return altered; calls it "wind tricks" and never smiles when he says it; some notes should never be played again.
- **In TF-M1:** teaches the six calls by calling the player. Blows the Closes and Rest.
- **Knows:** the codes; that echoes come back altered. Half-remembers that a seventh row once meant something. **Doesn't know:** why the row was painted out; why the Close came back early.
- **Voice:** teacher's patience, used sparingly. Repeats a call rather than an explanation. Never laughs at a wrong answer.
- **Ledger guard:** no war service, battle or roster is given to him. His fear is shown, not explained.

#### Ressa Highcrag, High Ridge Warden [CANON ANCHOR]
- **Canon:** knows which tones caused "wrong results"; refuses certain calls; keeps the horns anyway.
- **In TF-M1:** one action and two words. Stops a young warden mid-interval. Does not explain.
- **Voice:** none needed. If spoken to: "Busy, walker. Storm."
- **Ledger guard:** no named roster, no battle, no new horn weapons.

#### Aud Hammerlee, master bridgewright of Windscar [NEW]
- **Want:** a bridge up before dark. **Fear:** the face over the Narrows.
- **Knows:** rope, iron, scree, wind windows, echo counting off a face. **Doesn't know:** what the early Close was, and she does not want to.
- **Voice:** swears at rope affectionately ("you lovely frayed bastard"). Praises work by insulting it less. Her laugh at the early Close is too loud, and she knows it.

#### Ketil Rask, Nettlehook ropeway keeper [NEW]
- **Want:** the sledge home. **Fear:** everybody else's safety.
- **Knows:** Nettlehook's winter needs to the sack; his crew; the goats. **Doesn't know:** anything about W. accounts.
- **Voice:** worried about everything except himself. "Mind the goats. Mind your feet. Mind that rope." Never asks for himself.

#### The caravan master [NEW, role name]
- **Want:** Stonewake's market stocked and the Wardens paid. **Voice:** a trader's even keel. Argues with the weather, not with Ketil.

#### Minor TF-M1 cast
| NPC | Status | Notes |
|---|---|---|
| **Young warden** | Role | Practising at the horn rack. Embarrassed. |
| **Passwatch storekeeper** | Role | Sits on a crate. "Not mine." |
| **Haulier** (at the gate) | Role | Looks away at the name Whinstone. Returns in TF-M2. |
| **Lowmark caravan hand** | Role, `LM_CIVIC_STANDING` only | One farewell line. No cargo or route mentioned. |
| **Peddler pair** | Role | Robbed at the Blind Corners. |
| **Corner-Boss** | Role (elite) | A deserter in a Warden's coat with the badge cut off. |
| **Pass bandits, Aud's crew, Ketil's crew** | Role | Barks. |

### TF-M2

#### Elira Hearthward, Hearthguard Clan Voice [CANON ANCHOR]
- **Canon:** exhausted, practical, protective; Thornfell is bleeding itself dry; children deserve more than drills; argues with Brynjar constantly and defends him as fiercely; calls acoustic stonework "good old building".
- **In TF-M2:** gives the quest; closes it in the first snow.
- **Knows:** the allotments, the prices, the chits nobody can cash. **Doesn't know:** the store, the splinter.
- **Voice:** counts while she talks. Finishes a row before she looks up. Tired jokes. Angry quietly.
- **Ledger guard:** no war history.

#### Brynjar Korr, Blood-Oath Clan Voice [CANON ANCHOR]
- **Canon:** hot-headed, loud, fiercely loyal; Emberholt will betray Thornfell again; readiness is love; pounds the stone table; would die for any Thornfell child; his clan keeps the loudest horn towers; brags about "the horn that split the ridge".
- **In TF-M2:** learns about the store from the player, privately or in public. Disowns or defends.
- **Knows:** his clan's horns; the boast. **Doesn't know:** the stores, the splinter, the Quartermaster, what the boast covers. He is **not** a member.
- **Voice:** interrupts. Pounds things. A long speech from Brynjar is anger; a short one is worse.
- **Ledger guard:** no war service or family casualty.

#### Hadrik Stonewake, Speaker of the Assembly [CANON ANCHOR]
- **Canon:** a buffer, not a ruler; calm, patient; scars he never speaks of; lets arguments burn out; chooses where people stand.
- **In TF-M2 (public route):** listens, reads totals aloud, asks the player what they will carry word for. Does not decide.
- **Voice:** slow, low, few words. Asks questions he already knows the answer to so the room can hear them.
- **Ledger guard:** no battle, date or Stonebound contact for his scars.

#### Bersi Coldbrook, store-factor at the Whinstone Store [NEW] `[SPLINTER]`
- **Want:** the ledger to balance. **Fear:** heights, then the player, then the Quartermaster's opinion of his columns.
- **Knows:** every receipt, buyer and seller by account, the pay chits, the standing orders' wording, that the countersign line is empty. **Doesn't know:** where the relief grain came from or how ("the usual hands"); anything about horns; who signs (he has decided not to know).
- **Voice:** a clerk's courage: brave about paperwork, terrified of the window. Precise numbers. Says "properly" a lot. Never says "the Quartermaster" to the player: he says "the orders".
- **Swap layer:** every Bersi node is tagged.

#### The haulier [NEW, role name]
- Clanless; hauled for "W." until coin ran out. Paid in chits now. Ashamed and stubborn. Never went past the hut.

#### Minor TF-M2 cast
| NPC | Status | Notes |
|---|---|---|
| **Hearthguard storekeepers** | Role | Counting; barks. |
| **Passwatch storekeeper** | Role | Returns. |
| **Haul crew** (heard, never met) | Role | "And up. And up." |
| **Iron Winter crew boss, spears, hornmen** | Role | Barks. Say "the Quartermaster" `[SPLINTER]`. |
| **Clanless hires** | Role | Flee. "Hired, not sworn." |
| **Hall listeners, Old Torvek** (public route) | Role / [CANON ANCHOR] | Torvek has one sentence (`TIW-D8.24`), no wartime claims. |

---

## Part 3: TF-M1 The Closing of Passwatch (`TPW`)

### TPW-B0: arrival barks

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TPW-B0.1 | Gate volume, `LM_CIVIC_STANDING` | LOWMARK CARAVAN HAND (heading down, shouldering a pack) | "You're staying up here? In this?" (beat) "River keep you anyway. Even this high." |
| TPW-B0.2 | Gate volume | WARDEN (lashing a tarp) | "Closing day. Mind the ropes." |
| TPW-B0.3 | Gate volume | WARDEN (to a goat) | "In. In. You're not special. In." |

### TPW-D1: Vessa at the gate (S00_arrive)

```
TPW-D1.01 VESSA: (slate under her arm; looks the player over once) "Walker. You've come up on a closing day."
TPW-D1.02 VESSA: "Storm by dusk. Gate shuts till it breaks."
TPW-D1.03 VESSA: "Three loads are still past the Narrows. Bridge is down. Rockfall."
TPW-D1.04 VESSA: "I've no wardens spare. Can you follow a horn?"
  > "I can."                                   → TPW-D1.10
  > "What does that mean, follow a horn?"      → TPW-D1.20
  > [lowmark.main.04_night_flush Completed] "I'm looking for the Whinstone Store."   → TPW-D1.30
  > "What's past the Narrows?"                 → TPW-D1.40

TPW-D1.10 VESSA: "Everybody says that. Dorn'll find out. Horn post, up the steps."   → TPW-D1.50
TPW-D1.20 VESSA: "Means you'll learn. Dorn teaches children. You'll do." (beat) "Horn post. Up the steps."   → TPW-D1.50

TPW-D1.30 VESSA: "Never heard of it."
TPW-D1.31 (By the gate, a HAULIER mending a harness looks up at the word, then down, and goes on mending. He doesn't look up again.)   {set TPW_WHINSTONE_ASKED}   → TPW-D1 options

TPW-D1.40 VESSA: "A grain sledge for Nettlehook. Ketil's rope crew with it. A caravan for Stonewake."
TPW-D1.41 VESSA: "And weather. Mostly weather."   → TPW-D1 options

TPW-D1.50 VESSA: "Close starts when you go out the gate. Every Close is one less. Last one, I shut it."
TPW-D1.51 VESSA: "I don't shut it on people. Don't make me find out if I would."
      {event: TPW-D1 end → S01 active}
```

**Resume hook (quest Active, player at the gate before S04):** `TPW-D1.90 VESSA: "Still shut. Still waiting on you."`

### TPW-D2: Dorn at the horn post (S01_calls)

Each lesson opens when the previous one is done. Dorn blows the call himself from the long horn.

```
TPW-D2.01 DORN: (at the long horn; doesn't turn round) "Vessa's walker. Good. Stand over there. Far end."
TPW-D2.02 DORN: "Children learn these by being called. So do you. Don't think. Do what it says."
      {lesson 1 begins: player walks to the far end}

TPW-D2.10 (Dorn blows Gather: three short.)
TPW-D2.11 [player walks back] DORN: "Gather. Three short. Come to the call. That's all it ever means."   {glyph: three dots}
TPW-D2.12 [player does not move within ~8 s] DORN: (blows it again) "Three short. Come."

TPW-D2.20 DORN: (picks up a bucket of grit; looks at the ledge above) "This one you'll thank me for."
TPW-D2.21 (Dorn kicks the bucket off the ledge and blows Fall: short-long-short.)
TPW-D2.22 [player under the eave in time] DORN: "Fall. Under the bar. Every time. Don't look up first."   {glyph: dot-bar-dot}
TPW-D2.23 [player caught] (Grit patters on the player's hood.) DORN: "Under the bar. Don't look up first." (refills the bucket) "Again."   → TPW-D2.21

TPW-D2.30 (Dorn blows Rest: one long.)
TPW-D2.31 DORN: "Rest. All clear. Stand down." (beat) "Rest ends any call. Remember that. It's the only one with power over the others."   {glyph: a flat line}

TPW-D2.40 (Dorn blows Close: two long, falling.)
TPW-D2.41 DORN: "Close. A gate's shutting. It repeats. Every Close is one less."
TPW-D2.42 DORN: "Count them. The last one, Vessa drops the bar."   {glyph: two falling bars}
      {TPW-B1.1 plays here or during lesson 5 on the rack volume}

TPW-D2.50 DORN: (hands the player a practice horn from the rack) "Now you blow. Don't puff your cheeks. The horn knows the shape. You choose it."
TPW-D2.51 (Dorn blows Lost: one long, rising. He waits.)
TPW-D2.52 [player blows Answer] DORN: "Answer. Two short. Heard; we're here." (beat) "Lost always wants an answer. Always."   {glyphs: a rising line; two dots}
TPW-D2.53 [player blows anything else] DORN: (waits; blows Lost again) "Lost wants an answer. Two short."   → TPW-D2.51
TPW-D2.54 [player blows nothing within ~10 s] DORN: "Somebody's out there in the snow waiting on you. Two short."   → TPW-D2.51

TPW-D2.60 DORN: "Six. Every Marcher child knows six." (He doesn't look at the training board.)
  > "What happened just now? Ressa stopped that warden."   [TPW-B1.1 seen]   → TPW-D2.70
  > "Only six?"                                              → TPW-D2.75
  > [TPW_BOARD_SEEN] "There's a seventh row on the board. Painted over."   → TPW-D2.78
  > "Where do I go?"                                         → TPW-D2.80

TPW-D2.70 DORN: "Ask her. She won't tell you either."   → TPW-D2.60 options
TPW-D2.75 DORN: "Six we blow." (beat) "Some we don't."   → TPW-D2.60 options
TPW-D2.78 DORN: (a long look at the board) "Paint's cheap." (beat) "It meant something once. People stopped needing it. Or stopped wanting to." → TPW-D2.60 options

TPW-D2.80 DORN: "Out the gate, down the pass. Close comes when you go out. Listen for it."
TPW-D2.81 DORN: "Bring the horn back. They all say they will."
      {set TH_CALLS; event: TPW-D2 end → S02 active}
```


### TPW-B1: the refused interval

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TPW-B1.0 | Rack volume, before Ressa | YOUNG WARDEN (practising; one long, then a second note that bends wrong. The audio is cut before the call completes; the Split is never reproduced.) | — |
| TPW-B1.1 | Immediately after | RESSA (crossing the shoulder; puts her hand flat on the horn's bell; the note dies) | "Not that one." |
| TPW-B1.2 | After | YOUNG WARDEN (red to the ears) | "Sorry, Warden. I heard it once. I thought..." |
| TPW-B1.3 | After | RESSA (already walking) | (No reply.) |
| TPW-B1.4 | Player speaks to Ressa during TPW | RESSA | "Busy, walker. Storm." |
| TPW-B1.5 | Player speaks to the young warden | YOUNG WARDEN | "I'm not to play it. That's all I know. That's all anyone tells you." |

### Inspect texts: Passwatch (S01–S02)

| Object | Text | Condition |
|---|---|---|
| Training board (TPW-I1) | "Six call-shapes painted white, one under another. Below them, a seventh row painted over in grey. The old shape is still raised under the paint: two short, then something rising." {set `TPW_BOARD_SEEN`} | — |
| Long horn | "Bound in old iron. The mouthpiece is worn to the shape of one mouth." | — |
| Practice-horn rack | "Six horns. One peg empty: yours, for today." | During S01+ |
| Gate notches | "Notches cut in the gate's inner face at a child's height. Names beside some. Not recent." | — |
| Warden's slate (before S11) | "Chalk ghosts under chalk ghosts. Dates. *Storm.* *Storm.* *Storm.*" | — |
| The tarp (TPW-I2) | "A tarp lashed down hard against the weather. Chalked on it, in a big plain hand: *W. acct.*" | — |
| The sacks (TPW-I3) | "Grain sacks, stacked tall. Each is stencilled with a sheaf over a wave and the words RELIEF — FENMERE. Their tags are cut with tally notches." {set `TPW_SACKS_SEEN`} | Optional |
| The sacks (addition) | "Crestbridge tally notches. Corvin cut his like that." | `lowmark.main.02_short_measure` Completed |
| The sacks (addition) | "Whinstone. W. acct." (beat) "Nobody here will say the name." | `TPW_WHINSTONE_ASKED` |
| Hauliers' sledge | "Empty. Runners freshly greased. Waiting for weather." | — |
| Patrol board (barracks) | "Pairs of names in chalk. One pair marked *out*." | — |

No variant of any of these says when, how or from where the sacks came.

### TPW-B2: store-yard

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TPW-B2.1 | Pass-by volume (required) | STOREKEEPER (on his crate, not looking up) | "Not mine. Waiting on the hauliers. Up the track, once the weather lets them." |
| TPW-B2.2 | Player inspects the sacks | STOREKEEPER | "Don't count them. I don't." |
| TPW-B2.3 | Player speaks to him | STOREKEEPER | "I keep the yard. What's in it is somebody's account." |
| TPW-B2.4 | Player exits the gate (Close I) | (Close, two long falling, from the horn post behind. The first pip fills.) | — |

### TPW-B3: the Blind Corners (S03, TPW-E1)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TPW-B3.1 | Approach | PEDDLER (offscreen, from the second bend) | "That's all of it! That's all we've got!" |
| TPW-B3.2 | Spotted (road) | SLINGER | "Walker on the road! Stones!" |
| TPW-B3.3 | Spotted (goat track, from behind) | SLINGER | "Where did... He came over the top!" |
| TPW-B3.4 | Cutter engages | CUTTER | "Closing day, walker. Everybody's stranded. Everybody pays." |
| TPW-B3.5 | Cutter yields | CUTTER | "Down. I'm down. It's cold enough without you." |
| TPW-B3.6 | Corner-Boss yields | CORNER-BOSS (kneels; pulls the hood off) | "Fine. Fine." (beat) "Wore this coat for eleven winters. They took the badge. They never asked for the coat back." |
| TPW-B3.7 | After E1 | PEDDLER (righting a bale) | "Thank you. We'll wait out the storm at Passwatch." (beat) "If the gate'll have us." |
| TPW-B3.8 | Cart righted (optional) | PEDDLER | "For your trouble. Don't argue. It's bad luck to argue on a closing day." |

### TPW-D3: Aud at the Narrows (S04–S08)

```
TPW-D3.01 AUD: (to a rope, fondly) "Look at you. You lovely frayed bastard. You held till you didn't."
TPW-D3.02 AUD: (to the player) "Vessa's walker? Good. I need hands that don't argue."
TPW-D3.03 AUD: "Three things. Stakes off the slope. Fittings off my anvil. A guide line across that." (the gap)
TPW-D3.04 AUD: "Then my lot haul the span and we all go home. Before Dorn runs out of breath."
      {lessons: wind window, echo count}

TPW-D3.10 AUD: "First thing. Listen to the cutting." (the fluted face) "Hear it climb?"
TPW-D3.11 (The face whistles up a fifth. Two breaths. The gust crosses the road; Aud's crew drop behind a white bar.)
TPW-D3.12 AUD: "A fifth before the gust. Get under a bar. Then move. That's the forgiving wind's only manners."

TPW-D3.13 AUD: "Second thing. That face up there sheds. Blow Answer at it. Count till it comes back."
TPW-D3.14 [echo steady] AUD: "Three, steady. Holding. Good."
TPW-D3.15 AUD: "Again."
TPW-D3.16 [echo smeared] AUD: (watching dust spill from the face) "Hear that? Short and smeared."
TPW-D3.17 (A slide of stones comes down into the gap.)
TPW-D3.18 AUD: "That." (beat) "Smeared, you wait. You don't argue with a face."
      {event: lessons end → S05 and S06 active}

TPW-D3.20 [after TPW-E2] AUD: "Stakes. Stormwood, off the slope. The wind's already tested it. Three."
  > "I'll cut them."                         → TPW-D3.21
  > "Can your crew do it?"                   → TPW-D3.22
TPW-D3.21 AUD: "Marked trunks. Knee-high cut. Don't take the pretty ones, they lie."   {S05: player cuts}
TPW-D3.22 AUD: "They can. That's another Close, mind." (shouts) "Brann! Holt! Slope!"   {set TPW_CREW_STAKES; a Close sounds when they finish}

TPW-D3.30 AUD: (at the anvil) "Fittings. Two shackles, two plates. Bar's mine. Sweat's yours, or Odo's."
  > "I'll smith them."                       → TPW-D3.31
  > "Let Odo."                               → TPW-D3.32
TPW-D3.31 AUD: "Go on, then."
TPW-D3.33 [first fitting complete] AUD: (turns it over) "Ugly. Holds. That's the only kind I trust."
TPW-D3.32 AUD: "Odo! Strike!" (beat) "Another Close. Dorn's lungs'll have opinions."   {set TPW_CREW_FITTINGS}

TPW-D3.40 [S05 and S06 complete] AUD: (hands over the coiled guide line) "Across. Pay it out behind you. Bars at three faces."
TPW-D3.41 AUD: "Middle one's under the shedder. Count before you go. Don't be brave."
TPW-D3.42 AUD: "Ketil's lot will take the end. Then come back and hold the snub post for me."
      {S07 active}

TPW-D3.45 [S07 complete; player back on near side] AUD: "Basket's rigged on the line now. Ride it or walk it. I don't care which, just be here."
TPW-D3.46 AUD: "Snub post. Take up slack when I shout. Let go when the cutting climbs."
      {S08 active}

TPW-D3.50 [after the span Close; player speaks to Aud] AUD: "Wind trick." (beat; she isn't laughing now) "Hold the post."
TPW-D3.51 [S08 complete] AUD: (slaps a new handline) "There. One heavy load before the last Close. Not two. Not tonight."
TPW-D3.52 AUD: "Go tell them. They'll both want to be first. They're both right."
      {S09 active}
```

**Resume hook (after S04):** `TPW-D3.90 AUD: "You came back. The rope's still here. So am I, more's the pity."`

### TPW-B5/B7: work barks

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TPW-B5.1 | Stormwood slope, wolves sighted (TPW-E2) | AUD (from above, shouting) | "Wolves on the slope! They're thin! Thin means brave!" |
| TPW-B5.2 | Stake cut | (log) | "Stormwood. Dense, twisted, dry right through." |
| TPW-B5.3 | Crew stakes finish | CREW (Brann) | "Stakes up!" (a Close sounds from Passwatch) |
| TPW-B6.1 | Crew fittings finish | ODO (striker) | "Fittings!" (a Close) |
| TPW-B7.1 | Guide line: gust tell | AUD (shouting across) | "Cutting's climbing! Bar!" |
| TPW-B7.2 | Guide line: player in shelter during gust | (log) | "The gust goes over. The bar's paint is fresh." |
| TPW-B7.3 | S2, echo smeared | AUD (from the near side) | "Smeared! Wait!" |
| TPW-B7.4 | S2, player goes and is hit | AUD | "What did I say? What did I *say*?" (fondly) "Idiot. Back to the bar." |
| TPW-B7.5 | Far side reached | KETIL | "Here! Give it here. Mind your hands. Mind the anchor. Mind — thank you. Thank you." |
| TPW-B7.6 | Anchor dug out | KETIL'S CREW | "There's the old ring. Buried, not broken." |

### TPW-B8: the span and the early Close (S08)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TPW-B8.1 | Segment 1 | AUD | "Take up! Take up! Lovely." |
| TPW-B8.2 | Span Close (§A8, ~3.5 s) | AUD (laughs, too loud and too long) | "Ha! Hah. Wind's having a joke. Wind's having a *day*." |
| TPW-B8.3 | Same, after | CREWMAN (makes the flat-hand Rest gesture at the cliff; says nothing) | — |
| TPW-B8.4 | Same, across the gap | KETIL (stopped with the rope in his hands; then, quietly) | "...Pull. Keep pulling." |
| TPW-B8.5 | Segment 3 complete | AUD | "Span's up. Nobody say anything clever." |
| TPW-B8.6 | Player speaks to any crewman after | CREWMAN | "Didn't hear anything. Wind." |

### TPW-D4: one load (S09)

```
TPW-D4.01 KETIL: (by the sledge, goats steaming) "Nettlehook's winter. Every sack of it. Children, old Freya, the lot."
TPW-D4.02 KETIL: "I'm not asking for me. I don't eat much. Ask anyone."
TPW-D4.03 CARAVAN MASTER: (by the beasts) "Stonewake's market. Fur and iron for winter. And the Wardens' pay's in these bales."
TPW-D4.04 CARAVAN MASTER: "I won't argue with Ketil. I'll argue with the sky. It's winning."
TPW-D4.05 AUD: (calling across from the near side) "One heavy load! Decide, walker! Dorn's not getting younger!"
  > "The sledge goes first."                  → TPW-D4.10
  > "The caravan goes first."                 → TPW-D4.20
  > "Split it. Half of each. The rest waits at Three Calls."   → TPW-D4.30
  > "What happens to whoever waits?"          → TPW-D4.40

TPW-D4.10 KETIL: (closes his eyes a moment) "Thank you."
TPW-D4.11 CARAVAN MASTER: "Three Calls, then. They've a lantern and a roof. We'll come in when it breaks."
TPW-D4.12 CARAVAN MASTER: "Wardens'll eat goodwill this week."   {set TH_PASSWATCH_ROUTE = sledge}   → TPW-D4.50

TPW-D4.20 CARAVAN MASTER: "Right. Fair." (to his drovers) "Beasts up."
TPW-D4.21 KETIL: "They'll eat bread with nothing on it. They've done it before." (beat) "Go on. Mind the third beast, she kicks."   {set TH_PASSWATCH_ROUTE = caravan}   → TPW-D4.50

TPW-D4.30 KETIL: "Half." (counting sacks with his hand) "Half's not winter. Half's most of autumn."
TPW-D4.31 CARAVAN MASTER: "Lightest bales. The rest of us walk to the lantern." (beat) "Everybody's short. That's fair, in a way I don't like."   {set TH_PASSWATCH_ROUTE = split}   → TPW-D4.50

TPW-D4.40 KETIL: "Three Calls has a roof. The storm breaks, they come in at morning."
TPW-D4.41 CARAVAN MASTER: "Nobody's left on the road, walker. Just left short."   → TPW-D4 options

TPW-D4.50 AUD: (across) "Blow Gather when you're ready. They'll come to it. Fall, they stop. You know that now."
      {event: TPW-D4 end; Gather blown at bridgehead → S10 active}
```

### TPW-B9/B10: the waiting and the escort

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TPW-B9.1 | Waiting load walks off (sledge outcome) | DROVER | "Lantern's lit at Three Calls. Somebody's expecting us. Nice, that." |
| TPW-B9.2 | Waiting load walks off (caravan outcome) | KETIL'S CREW | "Come on, goats. Roof and a fire. Better than most." |
| TPW-B9.3 | Split, both groups | CARAVAN MASTER | "Half of us walk, half of us cross. Like a bad joke with no end." |
| TPW-B10.1 | Gather blown, column moves | KETIL / DROVER | "Coming!" |
| TPW-B10.2 | Fall blown on the span | KETIL | "Down! Hold the line, hold the goats!" |
| TPW-B10.3 | Player doesn't call Fall on the span; leader halts late | KETIL'S CREW (lead) | "Gust! Down! Down!" (late, a little ragged) |
| TPW-B10.4 | Near side, player misses the Fall; Aud's crew calls it | AUD (blowing Fall herself from the cart, then) | "I'll do your job. Once." |
| TPW-B10.5 | Beast grazed by a stone (late Fall) | KETIL | "She's limping. She's walking. She's walking." |
| TPW-B10.6 | Wolves sighted (TPW-E3) | DROVER | "Wolves on the goat track!" |
| TPW-B10.7 | Howler draws breath | KETIL | "That one's calling the rest! Stop it!" |
| TPW-B10.8 | Player's horn makes the howler flinch | DROVER | "Ha! Even they don't like Dorn's lessons." |
| TPW-B10.9 | Wolf worrying a beast | (beast bawls; column halts) KETIL | "Get it off her!" |
| TPW-B10.10 | Outer road reached; **the last Close** | (Close, two long falling, from the horn post. The last pip fills.) VESSA (distant, from the gate) | "In! Everybody in!" |

### TPW-D5: Passwatch shut (S11)

```
TPW-D5.01 (The column goes under the arch. Wardens count beasts aloud. Vessa waits until the player is through, then drops the bar herself.)
TPW-D5.02 VESSA: (takes the slate off its nail; writes; reads it back flat) "Passwatch shut. Dusk. Storm."
TPW-D5.03 VESSA: (to the player) "That's the closing. Thank you, walker."
  > "Who's still out there?"                  → TPW-D5.10
  > "Will you write down who's outside?"      → TPW-D5.20
  > "When does it open?"                      → TPW-D5.30
  > (Say nothing.)                            → TPW-D5.40

TPW-D5.10 [sledge or caravan] VESSA: "The load at Three Calls. The far shielings. One of my pairs." (beat) "All of them know the cold."
TPW-D5.10 [split]             VESSA: "Half a sledge and half a caravan at Three Calls. The far shielings. One of my pairs."   → TPW-D5 options

TPW-D5.20 VESSA: (doesn't look up from the slate) "We write what we closed. Not who."   {set TPW_NAMES_ASKED}
TPW-D5.21 VESSA: (a pause; she hangs the slate on its nail) "That's how it's done. I didn't say it was good."   → TPW-D5 options

TPW-D5.30 VESSA: "When it breaks. Storm closure. Not the season. That's a different gate and a different day."   → TPW-D5 options

TPW-D5.40 VESSA: "Warm yourself. Dorn'll blow Rest."
      {event: TPW-D5 end → S12 active}
```

**Document: Vessa's slate** (world object; inspect from S11 on)

> *[older chalk, smeared, underneath:]* ...*Storm.* ...*Storm.*
>
> **Passwatch shut. Dusk. Storm.**

(No names. No count. That is the point. The epilogue wipes *Storm* off with a sleeve and leaves *Passwatch shut. Dusk.* in ghost chalk under *Open.*)

**Document: Vessa's slate (epilogue, after the storm breaks)**

> ~~Passwatch shut. Dusk.~~ *(ghost chalk)*
>
> **Open. Clear.**

### TPW-B12: Rest and epilogue

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TPW-B12.1 | Rest (S12) | (Dorn blows Rest: one long, flat. It comes back off the cliffs on time.) | — |
| TPW-B12.2 | After Rest | DORN (calling down from the post) | "Walker! My horn!" |
| TPW-B12.3 | Player returns or keeps the horn | DORN | "Keep it. You'll lose it in a better place than I would." |
| TPW-B12.4 | Player asks Dorn about the early Close (optional, after completion) | DORN (not smiling) | "I heard it from the post. I'm not talking about it on a closing day." (beat) "Wind tricks." |
| TPW-B12.5 | Barracks, keep watch step 1 | WARDEN (dicing) | "Ketil's asleep sitting up. Don't wake him. He'll start minding things." |
| TPW-B12.6 | Keep watch step 2 | VESSA (at the shutters) | "Sleet's thinning." |
| TPW-B12.7 | Storm breaks (morning) | VESSA (wiping the slate with her sleeve) | "Open. Clear. Go and be useful elsewhere, walker." |
| TPW-B12.8 | Morning, waiting load comes in (sledge/caravan/split) | WARDEN at gate | "Three Calls lot coming in! All of them! Count them!" |
| TPW-B12.9 | Morning, `sledge` | KETIL (passing with the goats) | "Nettlehook eats. I'll tell them who to thank. I'll tell them twice." |
| TPW-B12.10 | Morning, `caravan` | CARAVAN MASTER | "Wardens paid. Market stocked. Ketil's lot came in at dawn, cold and cheerful. You did fine." |
| TPW-B12.11 | Morning, `split` | KETIL | "Half and half, and now the other halves. Like a sum that comes out in the end." |

### TPW post-quest barks (Passwatch, Windscar)

| Speaker | Line | Condition |
|---|---|---|
| YOUNG WARDEN (horn rack) | "I practise the six now. Only the six." | TPW Completed |
| AUD (Narrows) | "Span's holding. I talk to it every morning. It doesn't answer, which is how I like a bridge." | TPW Completed |
| AUD (Narrows) | "You smithed those fittings. They're still ugly. Still holding." | not `TPW_CREW_FITTINGS` |
| PEDDLER (Passwatch) | "The gate had us. Warden counted us like goats. Nicest thing all week." | TPW Completed |
| STOREKEEPER (store-yard) | "Hauliers'll come for those once the track's clear. Not my business." | TPW Completed, before TIW S02 |
| WARDEN (gate) | "Closing days are the worst days. Opening days are the second worst. Everybody wants to be first." | TPW Completed |
| DORN (horn post) | "You blow Answer like you mean it now. Good. Somebody always does." | TPW Completed |
| VESSA (gate) | "Still don't write who. Still think about it." | `TPW_NAMES_ASKED` |

---

## Part 4: TF-M2 The Iron Winter Stores (`TIW`)

### TIW-B0: lead-in barks

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TIW-B0.1 | Passwatch, after TPW epilogue, `sledge` | HEARTHGUARD RUNNER | "Elira's asking for the walker who brought the sledge in. Ridge-market. She says no hurry, which means hurry." |
| TIW-B0.2 | Same, `caravan` | HEARTHGUARD RUNNER | "Elira's asking for the walker who brought the caravan in. Ridge-market. She says no hurry, which means hurry." |
| TIW-B0.3 | Same, `split` | HEARTHGUARD RUNNER | "Elira's asking for the walker who brought half of everything in. Ridge-market. She says no hurry, which means hurry." |
| TIW-B0.4 | Ridge-market ambient | STOREKEEPER (rubbing out a number, writing a smaller one) | "Smaller. Smaller again." |
| TIW-B0.5 | Ridge-market ambient | MARKET WOMAN | "Two over for oats. Two over! My grandmother would have climbed the board." |

### TIW-D1: Elira at the ridge-market (S00_offer)

```
TIW-D1.01 ELIRA: (counting a row of sacks; finishes the row before she looks up) "Forty-one. Should be fifty-six."
TIW-D1.02 [sledge] ELIRA: "You're the one who brought Ketil's sledge in. Nettlehook's fed. Thank you. Now help me feed everyone else."
TIW-D1.02 [caravan] ELIRA: "You're the one who brought the caravan in. Wardens paid. Thank you. Nettlehook ate plain bread for two days. I'm not blaming you. I'm counting."
TIW-D1.02 [split] ELIRA: "You're the one who split the loads. Everybody short and nobody shorter. I respect that. I hate it, and I respect it."
TIW-D1.03 ELIRA: "Somebody's buying every lot of grain and bar iron that comes to this market. Two over the board."
TIW-D1.04 ELIRA: "They pay in chits. Nobody in Stonewake can cash them. So the sellers take the chits, and my storekeepers take nothing."
  > "Who's buying?"                            → TIW-D1.10
  > "What do you need?"                        → TIW-D1.20
  > "How short are you?"                       → TIW-D1.30

TIW-D1.10 ELIRA: "I don't guess. I count." (beat) "Brynjar says Emberholt. Brynjar says Emberholt about the weather."   → TIW-D1 options
TIW-D1.20 ELIRA: "Where it's going. Board's there. Hauliers are there. One of them has a chit he keeps looking at."   → TIW-D1.25
TIW-D1.30 ELIRA: "Every highstead allotment's down a fifth. Nettlehook's children's ration I had to buy twice, and I still don't have it."   → TIW-D1 options
TIW-D1.25 ELIRA: "Find where the grain goes, walker. Then come and tell me. I'll be here. I'm always here."
      {event: TIW-D1 end → S01 active}

TIW-D1.40 [S11 active; player speaks to Elira before Brynjar or Hadrik] ELIRA: "Not me first."
TIW-D1.41 ELIRA: "It's Blood-Oath sacks up there or it isn't. Tell Brynjar. Or tell the hall. Then come back to me." (beat) "I'll still be counting."
```

**Resume hook (before S09):** `TIW-D1.90 ELIRA: "Still short. Still counting."`

### Inspect texts: the market (S01)

| Object | Text | Condition |
|---|---|---|
| Price board | "Grain, iron bar, salt, wool. The prices have been rubbed out and chalked higher, twice. Under grain and iron, in another hand: *W. pays two over. Any lot.* A knife-scratch underlines it." {set `TIW_LEAD_BOARD`} | Required |
| Allotment boards | "Highstead names, measures beside them. Most rubbed down and rewritten smaller. *Nettlehook (children's)*: written, crossed, written again." | — |
| Folded empty sacks | "A pile of empty sacks taller than the full ones." | — |
| The stall arch | "Old cut stone. Voices from the far side of the market come through it clear. Elira calls it good old building." | — |

### TIW-D2: the haulier (S01)

```
TIW-D2.01 HAULIER: (on his sledge, not working; a bundle of chits tied to his harness peg) "Not hauling today, walker."
TIW-D2.02 [TPW_WHINSTONE_ASKED] HAULIER: (looks up; recognises the player) "You. You asked about it at the gate. I didn't answer you."
  > "Who pays you in those chits?"             → TIW-D2.10
  > "Can I see one?"                           → TIW-D2.20
  > "Where did you haul?"                      → TIW-D2.30
  > [TPW_WHINSTONE_ASKED] "Why didn't you answer me?"   → TIW-D2.40

TIW-D2.10 HAULIER: "W." (beat) "That's all it says. W. paid coin all summer. Then chits. Then more chits."   → TIW-D2 options

TIW-D2.20 HAULIER: (unties one and hands it over, reluctantly) "Read it. Give it back. It's worth nothing and it's mine."
      {document: the haulier's chit; set TIW_LEAD_CHIT}   → TIW-D2 options

TIW-D2.30 HAULIER: "Passwatch yard, up the track. Whinstone track, past Three Calls. To the hut."
TIW-D2.31 HAULIER: "They take it off you at the hut. They don't let you past. I never saw the store." (beat) "If there is one."
TIW-D2.32 HAULIER: "Before that? Don't know. Sacks were in the yard when I came for them. I haul. I don't ask a sack where it's been."   → TIW-D2 options

TIW-D2.40 HAULIER: "Because I'm clanless, and they pay clanless men to haul and not to talk." (beat) "And they stopped paying. So."   → TIW-D2 options

TIW-D2.50 [all seen] HAULIER: "If you go up there, don't tell them I sent you. I didn't. You found it."
      {event: TIW-D2 end}
```

**Document: the haulier's chit**

> **W.** *(stamped, in a ring)*
>
> Haul, Passwatch yard to the hut. One sledge, full.
> Good for **four measures' worth** at the Whinstone, on the account.
> To bearer.
>
> *B.C.* `[SPLINTER]`
> *2 wk to Smoke*

(The initials are Bersi's. Nothing on the chit says where the Whinstone is beyond "the account". Swap per bible §3.1.)

### TIW-D3: the Passwatch store-yard, empty (S02)

```
TIW-D3.01 STOREKEEPER: (on his crate) "Gone. Hauliers came the day after the storm. Up the track."
TIW-D3.02 [TPW_SACKS_SEEN] STOREKEEPER: "You looked at them. I saw you look."
  > "Whose account is W.?"                     → TIW-D3.10
  > "Where did the sacks come from?"           → TIW-D3.20
  > "Thanks."                                  → TIW-D3.30

TIW-D3.10 STOREKEEPER: "Somebody's. They pay the yard fee on time. That's all the yard asks."   → TIW-D3 options
TIW-D3.20 STOREKEEPER: "They were in the yard. Then they weren't. I keep the yard, walker, not the roads."   → TIW-D3 options
TIW-D3.30 STOREKEEPER: "Runner marks go out the gate. You've got eyes."
      {event: TIW-D3 end}
```

| Object | Text | Condition |
|---|---|---|
| Runner marks (required) | "Two deep grooves in the frost, many times over, from the empty patch to the gate. Heavy sledges. They turn up-pass." {S03 active} | Required |
| Empty patch | "A dry rectangle where the sacks stood. The tarp's gone too." | — |
| Grain in the cracks | "Lowland grain. Thin, pale, small. Not ridge oats." | — |

### TIW-B3: the Whinstone track (S03)

| Id | Trigger | Speaker | Line (log or voice) |
|---|---|---|---|
| TIW-B3.1 | Track foot | (log) | "The runner grooves leave the pass road here. Someone has scraped the old sign off the cairn." |
| TIW-B3.2 | Wrong fork dead end | (log) | "The marks don't come this way." |
| TIW-B3.3 | Haul crew heard ahead | HAUL CREW (positional, unseen) | "And up. And up." |
| TIW-B3.4 | Voices enter the gully (§B8.1) | HAUL CREW | "And u—" (cut) |
| TIW-B3.5 | ~6 s later, further up | HAUL CREW | "—up. And up. Rest at the shelf." |
| TIW-B3.6 | Gully inspect (optional) | (log) | "Quiet. Not the quiet of snow. Your own breath is gone. Dust from the wall falls straight down, and the wind outside is blowing." {set `TIW_GULLY_HEARD`} |
| TIW-B3.7 | Leaving the gully | (log, only if no inspect) | "Sound comes back all at once." |
| TIW-B3.8 | Rest shelf | (log) | "A stamped-out fire. Still warm under the ash." |

No NPC comments on the gully. Ever.

### TIW-B4: the Muster Hut (S04, TIW-E1)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TIW-B4.1 | Hut shoulder (drill) | CREW BOSS | "Again! Gather means run at it, not near it!" |
| TIW-B4.2 | Drill | HIRE | "I am running at it." |
| TIW-B4.3 | Drill | CREW BOSS `[SPLINTER]` | "The Quartermaster counts every spear. Count yours. Again!" |
| TIW-B4.4 | Spotted (yard route) | SPEAR | "Walker on the shoulder! Hornman!" |
| TIW-B4.5 | Fight starts | HIRE (dropping a spear, running downhill) | "We're hired, not sworn!" |
| TIW-B4.6 | Hornman blows Gather | (Gather: three short; spears quicken) | — |
| TIW-B4.7 | Player blows Rest in the window | SPEAR (stopping, confused) | "Who blew Rest?" |
| TIW-B4.8 | Spear yields | SPEAR | "Down. I'm down. It's for Thornfell, you idiot. It's all for Thornfell." |
| TIW-B4.9 | Crew boss yields | CREW BOSS | "You'll see. When the forges eat the grain. You'll see." |
| TIW-B4.10 | Ledge route, crows | (log) | "Crows on the rail, gone quiet." |
| TIW-B4.11 | Ledge route, drill below (unaware) | CREW BOSS (below) | "Again!" |

**Document: the broadsheet** (nailed to the hut door; a copy caught on the ledge rail)

> **WHEN THE FORGES EAT THE GRAIN,**
> **THE PASSES GO DARK.**
>
> *Remember the hunger winter.*
> *Count what you have. Keep what you count.*

(Unsigned. Printed from a cut-wood block, uneven ink. No device, no mark, no name. The first line is the R15 seed and must be printed exactly: *"When the forges eat the grain, the passes go dark."* Nothing in Thornfell explains or attributes it.)

| Object | Text | Condition |
|---|---|---|
| Broadsheet (inspect) | Document above. {set `TIW_BROADSHEET_READ`} | Optional; pass-by required |
| Hut chalk board | "First names and pay owed. Every line ends *chit*." | — |
| Straw target | "A straw man with a scrap of red cloth tied on. Somebody meant it as Emberholt. It is ugly, and it has been stabbed a lot, mostly in the legs." | — |
| Practice spears | "Ridge-iron heads. New. Too good for practice." | — |

### TIW-B5: the gate and the shaft (S05)

| Object / Id | Text or line | Condition |
|---|---|---|
| Front gate (inspect, required) | "Iron-bound doors in a cut arch. WHINSTONE stencilled above. Barred from inside. Greased hinges. The ledge is swept." | Required |
| Hoist foot cage | "An iron cage at the shaft's foot, chained to a ring. The padlock is rusted solid. The cable runs up into the dark." | — |
| Rungs | "Iron rungs, old, sound. Somebody has knocked the rust off the first dozen." | — |
| Vent slit | "A slit to the cliff face. It sings when the wind turns." | — |
| TIW-B5.1 | Down-draught on the rungs | (log) "The cable swings. Hold on." |
| TIW-B5.2 | Padlock breaks (cage wound) | CREWMAN (deep in the store, unseen) "Wind's at the shaft again." |
| Winding drum | "A timber drum and crank. Fresh tallow on the pawl." | — |

### Inspect texts: the galleries (S06–S08)

| Object | Text | Condition |
|---|---|---|
| Relief sacks (required) | "A whole bay of grain sacks stencilled with a sheaf over a wave and RELIEF — FENMERE. Tally-notched tags. Lowland grain, a long way from the lowlands." {set `TIW_SACKS_INSPECTED`} | Required |
| Relief sacks (addition) | "Crestbridge tally notches." | `lowmark.main.02_short_measure` Completed |
| Relief sacks (addition) | "The same sacks as the Passwatch yard." | `TPW_SACKS_SEEN` |
| Folded tarp | "The Passwatch tarp, folded, chalk side in. *W. acct.*" | — |
| Highstead sacks | "Thornfell clan marks. Bought at two over, most likely. Bought from people who needed the coin and got chits." | — |
| Bays (count) | "Nine bays. Eight full. One being filled." | — |
| Porridge bowls | "Two bowls. Cold now." | After TIW-E2 |
| Spearheads (required) | "New. Ridge iron, hammered this autumn. Hundreds." {set `TIW_IRON_SEEN`} | Required |
| Field forge | "Warm. Bellows patched. Someone works here most days." | — |
| Crow nests | "Sticks, wire and a strip of red cloth. Ridge Crows build with what people leave." | — |
| Hasp | "New chain, new hasp, through a staple in old stone." | — |
| Hasp (after Smithing) | "Drawn at their own forge. That seems fair." {set `TIW_HASP_SMITHED`} | Smithing used |
| Vent crawl | "An old air passage, knee high. It goes round." | — |
| Plates (required) | "Curved stone backed with horn, drilled for bolts, packed in straw. The grit in the straw is grey and gold: gorge stone." {set `TIW_PLATES_SEEN`} | Required |
| Plate (lift) | "Heavier than it looks. It feels like it is holding a note." | — |
| Eyvind's sketches (required) | See document below. {set `TIW_SKETCHES_SEEN`} | Required |
| Signal niche (alcove) | "An old niche in the wall. Your breath sounds close in it." | — |

**Document: Eyvind's tuning sketches** (pinboard; not a quest item) `[SPLINTER]`

> *[plate outlines in charcoal, each with a pitch mark: a short line and a dot at different heights]*
> *[a frame drawn in elevation: five plates hung, then nine]*
>
> Plates 3 and 7 carry. 5 fights them. Shim 5.
> Frame too small for the full set. The rock here takes it but muddies it.
> **Try in the great hall, Summit. Third mouth carries.**
> Next dark.
>
> *— E.*

(The "E." is Eyvind Stall's. Swap per bible §3.1. TF-M4's offer reads `TIW_SKETCHES_SEEN`.)

### TIW-B6/B7/B8: gallery barks

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TIW-B6.1 | TIW-E2 (guards rising) | SPEAR | "Who... The porridge. Get up, get *up*!" |
| TIW-B6.2 | Guard yields | SPEAR | "Sitting. I was already sitting. Let me keep sitting." |
| TIW-B7.1 | Crows dive | (log) | "A shriek, and a shadow on the floor." |
| TIW-B7.2 | Draught | (log) | "The vent sings. The crows scatter to the walls." |
| TIW-B8.1 | TIW-E4 spotted | HORNMAN | "Store's got a visitor!" |
| TIW-B8.2 | Hornman blows Gather (not cancelled) | CREWMAN (from the counting room) | "Coming!" |
| TIW-B8.3 | Player blows Rest in the window | HORNMAN | "That's not ours. Who's that?" |
| TIW-B8.4 | Hornman yields | HORNMAN | "Don't break the horn. It's my own. It's the only thing here that's mine." |

### TIW-B9: the counting room (S09, TIW-E5) `[SPLINTER]`

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TIW-B9.1 | Player enters | BERSI `[SPLINTER]` (ledger clutched to his chest; as far from the loophole as the room allows) | "No. No, you can't be in here, this is the counting room." |
| TIW-B9.2 | Crews engage | BERSI `[SPLINTER]` | "Not near the desk! Not near the — mind the ink!" |
| TIW-B9.3 | Surrender trigger | BERSI `[SPLINTER]` | "Down! Put them down! It's a ledger, not a wall!" |
| TIW-B9.4 | Crews yield | CREWMAN | "You heard the factor." |
| TIW-B9.5 | Bersi sits | BERSI `[SPLINTER]` (puts the ledger on the desk; sits on the floor with his back to the inner wall) | "Take it. Mind the binding. It's properly sewn." |
| TIW-B9.6 | Trial frame touched (§B8.2) | BERSI `[SPLINTER]` (flinching) | "Don't. He says it carries." |
| TIW-B9.7 | Player asks "Who says?" (optional, one line) | BERSI `[SPLINTER]` | "The man who tunes them. I don't hear the difference. I count them." |
| TIW-B9.8 | Ledger picked up | (log) | "A thick book, properly sewn. Kept in one steady hand." |

| Object | Text | Condition |
|---|---|---|
| Loophole | "Straight down the cliff to the pass. A long way. Very long." | — |
| Strongbox | "Coin. Not much. A lot more chits." | — |
| Pigeonholes | "Pay chits sorted by name of account. W. on most of them." | — |
| Trial frame (after the moment) | "Five plates on gut cord. A felt mallet. Chalk on the beam: three short strokes and a word, *hums*." | After `TIW_FRAME_TOUCHED` |
| Last-bay loophole | "The cliff ledges are empty. The crows haven't come back." | After `TIW_FRAME_TOUCHED` |

### Document: `TIW_store_ledger` (quest item) `[SPLINTER]`

The ledger is the act's one quest item. It is kept in Bersi's hand throughout. The text below is the full readable content in the item's page order. Lines in *italics* are marginal.

> **WHINSTONE — STORE LEDGER**
> *Opened 11 wk to Smoke.*
>
> ---
>
> **FRONT LEAF — STANDING ORDERS** *(copied fair by the factor)*
>
> Buy grain, iron in bar, and horn plate on the Whinstone account.
> Pay to two over the Stonewake board, no higher.
> Pay chits where coin is short.
> Keep accounts, not names.
> Store for the Iron Winter.
>
> Carried by hand.
> Countersigned: ______________________
>
> *(The countersign line is ruled and empty.)*
>
> ---
>
> **RECEIPTS**
>
> | Wk to Smoke | Entry | Measure | Paid |
> |---|---|---|---|
> | 11 | Store opened. Racks, new timber, 9 bays. | — | coin |
> | 11 | Highstead oats, Red Slope. | 20 measures | 2 over, coin |
> | 10 | Bar iron, ridge. | 40 weight | 2 over, coin |
> | 10 | Highstead oats, Three Calls grain-house surplus. | 12 measures | 2 over, coin |
> | 9 | **Relief grain, sixty-eight measures. Received.** | 68 | *on account* |
> | 9 | Plate, by the crate. Pay chit to G. Carrick's men, Shatterfall, plates by the crate. | 3 crates | chit |
> | 8 | Bar iron, ridge. | 60 weight | 2 over, coin |
> | 7 | Spear shafts, ash, bundled. | 200 | coin |
> | 7 | Plate, by the crate. Pay chit to G. Carrick's men, Shatterfall, plates by the crate. | 4 crates | chit |
> | 6 | Grain, ridge-market, mixed lots. | 31 measures | 2 over, chit |
> | 5 | ~~Nettlehook, children's winter ration, 14 measures~~ *Held. Iron Winter.* | 14 | 2 over, chit |
> | 5 | Hauls, Passwatch yard to the hut. | 6 sledges | chit |
> | 4 | Plate, by the crate. Pay chit to G. Carrick's men, Shatterfall, plates by the crate. | 2 crates | chit |
> | 4 | Lamp oil, salt, straw. | — | chit |
> | 3 | Grain, ridge-market, any lot. | 44 measures | 2 over, chit |
> | 2 | Hauls, Passwatch yard to the hut (after storm). | 4 sledges | chit |
> | 2 | *Ninth bay begun.* | — | — |
>
> ---
>
> **PAY CHITS OUTSTANDING**
>
> G. Carrick's men, Shatterfall: 9 crates, 6 paid by chit, 3 owing.
> Hauliers (clanless), Passwatch to the hut: 10 sledges, all by chit.
> Hires, hut: by the week, by chit.
>
> *Chits to be made good after Smoke. Properly.*
>
> ---
>
> **ALLOTMENT FOR THE IRON WINTER** *(the factor's own reckoning)*
>
> Grain: enough for the passes' crews and households for one winter, shut.
> Iron: spears for every household that will carry one.
> Plate: as the hornwright asks.
>
> *Balance carried.*

**Recognition line** (plays on reading the week-9 relief line; only with `lowmark.main.04_night_flush` Completed):
> *"Sixty-eight measures, on the Whinstone account. The bill at the Hollow Lock said the same. But this line is old. It was written weeks before that night on the Cut."* {set `TIW_LOWMARK_RECOGNISED`}

Nothing else is said, in any variant, about how the grain arrived, by whom, by which way, or why the number recurs.

### TIW-D6: Bersi's testimony (S10) `[SPLINTER]`

```
TIW-D6.01 BERSI [SPLINTER]: (on the floor, back to the inner wall) "You've got the book. You'll read it anyway. Ask."
  > "What is all this for?"                    → TIW-D6.10
  > "Who gives you the orders?"                → TIW-D6.20
  > "Where did the relief grain come from?"    → TIW-D6.30
  > [TIW_PLATES_SEEN] "What are the plates for?"   → TIW-D6.35
  > [lowmark.main.04_night_flush Completed] "I've seen a bill for sixty-eight measures on the Whinstone account."   → TIW-D6.40
  > [TIW_GATHER_CANCELLED] "Your hornman's call didn't work."   → TIW-D6.50
  > [TIW_FRAME_TOUCHED] "What happened when I touched the frame?"   → TIW-D6.55
  > [all of .10, .20, .30 seen] "Are you going to stay here?"   → TIW-D6.60

TIW-D6.10 BERSI [SPLINTER]: "The Iron Winter. That's what we call it. What we're storing for."
TIW-D6.11 BERSI [SPLINTER]: "For when Emberholt comes for the passes." (beat) "They did it before. Starved us. Everyone knows that."
TIW-D6.12 BERSI [SPLINTER]: "When they come, the passes will have grain and spears, and nobody will have to beg the lowlands or the forges."   → TIW-D6 options

TIW-D6.20 BERSI [SPLINTER]: "Standing orders. Front leaf. I copied them fair."
TIW-D6.21 BERSI [SPLINTER]: "They come carried by hand. With a countersign line." (beat) "I've never seen it signed."
TIW-D6.22 BERSI [SPLINTER]: "An empty line is still a line. I buy." (beat) "I don't ask whose hand. Asking isn't in the orders."   → TIW-D6 options
      (He does not name anyone. If the player presses: TIW-D6.23)
TIW-D6.23 BERSI [SPLINTER]: "You can throw me off the cliff and the line will still be empty, walker. Please don't."   → TIW-D6 options

TIW-D6.30 BERSI [SPLINTER]: "By the usual hands."
TIW-D6.31 BERSI [SPLINTER]: "It was in the Passwatch yard on the account. I paid the account. That's all a factor needs."
TIW-D6.32 BERSI [SPLINTER]: "I didn't ask where. I don't want to know where. Write that down if you like."   → TIW-D6 options

TIW-D6.35 BERSI [SPLINTER]: "I count them. I don't blow them."
TIW-D6.36 BERSI [SPLINTER]: "The miners at Shatterfall prise them out and I pay by the crate. The book says. Carrick's men."
TIW-D6.37 [TIW_SKETCHES_SEEN] BERSI [SPLINTER]: "The sketches aren't mine. He tunes. I balance."   → TIW-D6 options

TIW-D6.40 BERSI [SPLINTER]: "Then you've seen more paper than me."
TIW-D6.41 BERSI [SPLINTER]: "Sixty-eight's a good round lowland number. I wrote it the week it came. Long before your bill, I'd think." (beat) "Don't ask me how. I've said how. The usual hands."   {set TIW_LOWMARK_RECOGNISED}   → TIW-D6 options

TIW-D6.50 BERSI [SPLINTER]: "Somebody blew Rest at a crew." (almost admiring) "That's cheating. Who taught you that?"   → TIW-D6 options

TIW-D6.55 BERSI [SPLINTER]: "It hums. The rock. The crows go." (beat) "He says that means it's right. I don't know what right means for a noise."   → TIW-D6 options

TIW-D6.60 BERSI [SPLINTER]: "I'm not climbing down that shaft." (beat) "I'll be here. Tie the knots loose, would you? I bruise."
TIW-D6.61 BERSI [SPLINTER]: "Are you going to throw me off the cliff?"
  > "No."                                      → TIW-D6.62
TIW-D6.62 BERSI [SPLINTER]: "...Are you sure?"
  > "Yes."                                     → TIW-D6.63
TIW-D6.63 BERSI [SPLINTER]: "All right." (lets out a breath) "All right. Properly."
      {set TIW_BERSI_TESTIMONY; event: TIW-D6 end → S11 active}
```

**Resume hook (after S09, player returns to the counting room):** `TIW-D6.90 BERSI [SPLINTER]: "Still here. Still not climbing."`

### TIW-D7: Brynjar, privately (S11 private, S12) `[SPLINTER]`

```
TIW-D7.01 BRYNJAR: (at the horn terrace, shouting at a horn crew) "Again! Louder! If Emberholt can't hear it, it's a whistle!"
TIW-D7.02 BRYNJAR: (turning) "Walker. You've a face like a closing day. Out with it."
      {set TIW_ROUTE = private; set TH_BRYNJAR = disowned}
  > "Someone's filling the Whinstone Store with grain and spears. Come and see."   → TIW-D7.10
  > "There's a reserve nobody declared. The ledger says the Iron Winter."   → TIW-D7.10

TIW-D7.10 BRYNJAR: "The Whinstone? That's a hole in a cliff. Pigeons and old tallow." (pounds the parapet) "Who told you this?"
TIW-D7.11 BRYNJAR: "No. Don't tell me. Show me. I'll come up there and prove you wrong in front of whatever clerk you've got tied up."
TIW-D7.12 BRYNJAR: "Hoist foot. I'll be there before you. I'm faster on a track than I look."
      {Brynjar placed at the hoist foot; objective: Meet Brynjar at the hoist foot}

TIW-D7.20 [at the hoist foot, TIW_CAGE_WOUND] BRYNJAR: (looking at the cage) "You wound it. Good. My knees thank you. My pride doesn't."
TIW-D7.20 [else]                           BRYNJAR: (looking up the shaft) "Rungs. Fine." (climbs fast; a down-draught swings the cable) "And you can shut up, wind!"

TIW-D7.30 [counting room] BRYNJAR: (sees the racks, the spears; says nothing for once; takes the ledger from the player)
TIW-D7.31 BRYNJAR: (reading; his finger stops) "Nettlehook. Children's winter ration. Fourteen measures."
TIW-D7.32 BRYNJAR: "Struck." (beat) "'Held. Iron Winter.'"
TIW-D7.33 [sledge] BRYNJAR: "Ketil hauled grain over a broken bridge for those children. And here's a clerk striking them out."
TIW-D7.33 [else]   BRYNJAR: "Nettlehook ate plain bread for two days this autumn. And here's a clerk striking them out."
TIW-D7.34 BERSI [SPLINTER]: (from the floor) "It was the orders, it was only —"
TIW-D7.35 BRYNJAR: (pounds the desk once; the ink jumps) "Not one more word."
  > "Is this your clan's doing?"               → TIW-D7.40
  > "You've said Emberholt will come. They're getting ready for it."   → TIW-D7.40

TIW-D7.40 BRYNJAR: "Readiness is a horn on a tower where everyone can hear it. This is a hole in a cliff."
TIW-D7.41 BRYNJAR: "Not my clan's. Not in my name." (beat; quieter) "Not those children."
TIW-D7.42 BRYNJAR: (looking at the plate crates through the door) "My clan's horns split a ridge once. Everybody knows it." (beat) "We never needed a clerk's crate of them."
TIW-D7.43 [TIW_FRAME_TOUCHED] BRYNJAR: (sees the trial frame; doesn't touch it) "Leave it."
      {event: disowned}

TIW-D7.50 BRYNJAR: "So. What happens to this?" (gesturing at everything) "You found it. You say. I'll stand by it."
  > "Report it. The Assembly seals it and the Wardens guard it."       → TIW-D7.51
  > "Seize it. Elira's storekeepers take it down to the highsteads tonight."   → TIW-D7.53
  > "Leave it. Keep quiet. Let them keep filling it where we can watch."   → TIW-D7.55
  > "What would you do?"                                                → TIW-D7.58

TIW-D7.51 BRYNJAR: "The hall, then. Fine. They'll argue till spring and the grain will sit here, sealed and safe and no use to anyone."
TIW-D7.52 BRYNJAR: "I'll send to Ressa. Her wardens'll be up by dark. Clerk goes to the lock-up."   {set TH_STORES = reported}   → TIW-D7.60

TIW-D7.53 BRYNJAR: "Tonight." (a short, hard laugh) "Elira'll kiss you and then shout at me for a month. Good."
TIW-D7.54 BRYNJAR: "All you'll have left is a book. Mind it."   {set TH_STORES = seized}   → TIW-D7.60

TIW-D7.55 BRYNJAR: (a long breath) "That's cold, walker." (beat) "It's also right. Whoever signs for this will just start another hole in another cliff."
TIW-D7.56 BRYNJAR [SPLINTER]: (to Bersi) "You. Go back to your desk. Start a new book. A stranger came, saw grain, and went. Nobody believes strangers."
TIW-D7.57 BRYNJAR: "My people will watch the track. Elira will hate us both. She'll be right."   {set TH_STORES = leverage}   → TIW-D7.60

TIW-D7.58 BRYNJAR: "I'd burn it." (beat) "Which is why you're deciding."   → TIW-D7.50 options

TIW-D7.60 BRYNJAR: "Go and tell Elira. Tell her I disowned it. Tell her before someone else does."
      {event: TIW-D7 end → S13 active}
```

### TIW-D8: Hadrik and the hall, in public (S11 public, S12) `[SPLINTER]`

```
TIW-D8.01 HADRIK: (at the speaking stone in the empty hall; turns) "Walker. Sit, or stand. Most stand."
      {set TIW_ROUTE = public; set TH_BRYNJAR = defended}
  > "There's a reserve in the Whinstone Store. Grain, spears, horn plates. Here's its ledger."   → TIW-D8.10

TIW-D8.10 HADRIK: (takes the ledger; reads in silence; then aloud, in a hall that carries some voices further than others) "Grain, near two hundred measures."
TIW-D8.11 HADRIK: "Iron, a hundred weight in bar. Spears, two hundred. Horn plate, nine crates." (beat) "Store for the Iron Winter."
TIW-D8.12 (The hall is not empty after all: from the benches, Elira; Old Torvek by a pillar; listeners; and Brynjar, who is always in the hall, already on his feet.)

TIW-D8.20 BRYNJAR: "Somebody up there is ready." (pounds the stone table) "Good. Somebody should be."
TIW-D8.21 ELIRA: "Ready with my allotments, Brynjar."
TIW-D8.22 BRYNJAR: "Ready with Thornfell's winter! When Emberholt comes for the passes, and it will, you'll thank whoever filled that hole!"
TIW-D8.23 HADRIK: (lets it burn a moment) "No one in this hall signed for it." (beat) "Did they?" (Nobody answers.)
TIW-D8.24 TORVEK: (by the pillar) "A wall nobody built isn't a wall. It's a heap."
TIW-D8.25 BRYNJAR: (sits, hard) (says nothing more)

TIW-D8.30 HADRIK: (to the player, quietly; the hall hears it anyway) "I don't decide. I keep this room standing while it does."
TIW-D8.31 HADRIK: "The Wardens can seal it tonight. Elira's storekeepers can empty it tonight. Nobody here will stop either." (beat) "You found it. Which will you carry word for?"
  > "Seal it. The Assembly decides what happens to it."           → TIW-D8.32
  > "Empty it. Elira's storekeepers take it to the highsteads tonight."   → TIW-D8.34
  > "Why me?"                                                     → TIW-D8.36

TIW-D8.32 HADRIK: "Then it's sealed. Ressa will send wardens. The factor goes to the lock-up." (beat) "And we will argue till the snow is deep."
TIW-D8.33 ELIRA: (from the bench) "Grain doesn't vote."   {set TH_STORES = reported}   → TIW-D8.40

TIW-D8.34 HADRIK: "Then Elira has work tonight." (beat) "And the hall has only a book to argue over. Keep it safe."
TIW-D8.35 ELIRA: (already moving) "Sledges. All of them."   {set TH_STORES = seized}   → TIW-D8.40

TIW-D8.36 HADRIK: "Because you climbed the shaft. Because you're not a clan." (beat) "And because if I decide, I'm a ruler, and Thornfell doesn't have one."   → TIW-D8.31 options

TIW-D8.40 HADRIK: (hands the ledger back) "Keep this. Read it again before the snow is gone."
      {event: TIW-D8 end → S13 active}
```

`leverage` is not offered in TIW-D8: the hall has heard. (Quest file §B9.3.)

### TIW-B11/B12: after the choice

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TIW-B11.1 | Public route, outside the hall | (Brynjar alone at the stone table outside; he puts his fist on it, hard enough to hurt) | — |
| TIW-B11.2 | Public route, player speaks to him | BRYNJAR | "I said what I said in there." |
| TIW-B11.3 | Same, next line | BRYNJAR | "Don't ask me what I say out here." |
| TIW-B11.4 | Public route, Elira passing him | ELIRA | (stops; puts a hand on his shoulder; goes on without a word) |
| TIW-B12.1 | `reported`, Whinstone track | WARDEN (at the hoist foot) | "Sealed. Nobody up, nobody down. Grain's very safe. Nobody's eating it." |
| TIW-B12.2 | `seized`, hoist foot (optional haul) | STOREKEEPER | "Lower away! Mind the cage! Mind the — thank you!" |
| TIW-B12.3 | `seized`, carry a sack down the rungs | (log) | "One sack. Rest ledge. One sack. Rest ledge. It's an honest way to spend a night." |
| TIW-B12.4 | `seized` | STOREKEEPER | "Nettlehook's children's ration. Fourteen measures. Back where it was going." |
| TIW-B12.5 | `seized`, Bersi led out `[SPLINTER]` | ELIRA (by message, read by a storekeeper) | "'Clerks go to wardens, not to ropes.' That's what she said. Off you go, factor." |
| TIW-B12.6 | `leverage`, Bersi at his desk | BERSI `[SPLINTER]` (not looking up; a new book open) | "A stranger came, saw grain, and went." (beat) "I'm writing it properly." |

### TIW-D9: First snow (S13, closes the quest and Act I)

```
TIW-D9.01 (Snow begins as the player comes into the ridge-market: first a few flakes, then the whole air. The storekeepers look up all at once.)
TIW-D9.02 ELIRA: (at the stall, counting; she finishes the row) "First snow."

TIW-D9.10 [reported] ELIRA: "Brynjar's lot or Ressa's lot will tell me the store's sealed. So it's safe. So it's sitting there."
TIW-D9.11 [reported] ELIRA: "So we wait on a vote." (beat) "Grain doesn't vote."
TIW-D9.12 [reported] ELIRA: "You did it the right way. I'll be hungry the right way."

TIW-D9.10 [seized] ELIRA: (her storekeepers coming in with empty sledges, red-faced) "Nettlehook has sacks tonight. Red Slope. Three Calls. All of them."
TIW-D9.11 [seized] ELIRA: "Hadrik will have words. I'll have porridge."
TIW-D9.12 [seized] ELIRA: "I know what it cost. All you've got now is a book. Mind it."

TIW-D9.10 [leverage] ELIRA: "Brynjar told me." (doesn't look up) "You found it, and you left it."
TIW-D9.11 [leverage] ELIRA: "I know why. I can count the reason. I still hate it."
TIW-D9.12 [leverage] ELIRA: "I'll defend him in the hall anyway. Somebody has to. It's always me."

  > [disowned] "Brynjar disowned it."          → TIW-D9.20
  > [defended] "Brynjar defended it."          → TIW-D9.21
  > "Who signs for it?"                        → TIW-D9.22
  > (Watch the snow.)                          → TIW-D9.30

TIW-D9.20 ELIRA: "I heard. In front of a clerk, at the top of a cliff." (a tired smile) "That's Brynjar. Loud in the right place for once."   → TIW-D9 options
TIW-D9.21 ELIRA: "In the hall. Out of pride." (beat) "He went and hit the stone table after. He thinks nobody saw. Everybody saw."   → TIW-D9 options
TIW-D9.22 ELIRA [SPLINTER]: "The book doesn't say. Bersi doesn't say." (beat) "Someone who counts. That's all I've got. It's not much."   → TIW-D9 options

TIW-D9.30 (No line. Snow settles on the empty sacks and the full ones alike.)
TIW-D9.31 ELIRA: (counting again) "Forty-one." (beat) "Forty-two." [seized: "Fifty-six. Fifty-seven."]
TIW-D9.32 ELIRA: "Go on, walker. Get warm. I'll be here. I'm always here."
      {TH_SEASON = snow (set on step start); event: TIW-D9 end → quest Completed; Act I complete}
```

TIW-D9.31 is the act's last line: a count, not a speech. It carries the Act I turn without saying it.

### TIW post-quest barks

| Speaker | Line | Condition |
|---|---|---|
| HAULIER (hauliers' stand) | "Chits still don't cash. But somebody wrote my name down as owed. That's a start." | TIW Completed |
| HEARTHGUARD STOREKEEPER | "Snow's on the allotment boards. Can't rub numbers out in snow. Good." | `TH_SEASON = snow` |
| WARDEN (Passwatch) | "Wardens on the Whinstone track now. Cold duty. Quiet duty." | `reported` |
| NETTLEHOOK CHILD (at Nettlehook) | "We got extra. Nobody will say from where. Ketil says say thank you anyway." | `seized` |
| BLOOD-OATH WATCHER (Whinstone track, loitering) | "Just walking. Lovely track. Lot of sledges on it lately." | `leverage` |
| MARKET WOMAN | "W.'s stopped buying." / "W.'s still buying." | not `leverage` / `leverage` |
| BRYNJAR (horn terrace) | "Louder! If they can't hear it from a tower, it's not readiness, it's a secret!" | `disowned` |
| BRYNJAR (horn terrace) | (to his horn crew, quietly) "Again." | `defended` |
| DORN (Passwatch horn post) | "I hear you blew Rest at a crew." (beat) "Good. That's what it's for." | `TIW_GATHER_CANCELLED` |
| ELIRA (market) | "Still counting. Snow helps. It slows everybody down but me." | TIW Completed |

---

## Part 5: Review notes (dialogue file)

| Check | Result |
|---|---|
| Line length | Every conversation returns options or control within six NPC lines. Brynjar's longest run (TIW-D7.40–.42) is anger, as the voice rule says. |
| Canon anchors | Dorn: teaches, fears, deflects; no service or roster. Ressa: "Not that one." and nothing else; no roster, no battle. Elira: counts, defends Brynjar. Brynjar: not a member; disowns or defends; the canon boast; protective of children. Hadrik: reads totals, asks, does not decide; no scars mentioned. Torvek: one sentence, no wartime claim. |
| Splinter tags | Bersi (TIW-B9, TIW-D6, TIW-D7.34, TIW-B12.6, the chit initials, the ledger); Eyvind (the sketches' "E."; Bersi's "he"); "the Quartermaster" (TIW-B4.3 only). **Ingrith is never named. Bersi never says "the Quartermaster" and never names whose orders they are.** |
| FT-03 | "Up the track" (destination), "in the yard", "by the usual hands". No line states when, how, by whom or from which direction the relief grain arrived. The recognition line notes only the date and the account. |
| Evidence rule | The early Close, the quiet gully and the hum are never interpreted by any NPC. Bersi's testimony follows his yield. |
| Magic | Nobody calls anything magic. "Wind trick", "it hums", "it carries". |
| Address | "Walker" throughout. No name, gender, title or origin for the player. |
| R15 phrase | Printed exactly: "When the forges eat the grain, the passes go dark." Echoed once by a yielded crew boss (TIW-B4.9) in a shortened form; never explained. |
| Flags | Every flag set here (`TPW_WHINSTONE_ASKED`, `TPW_BOARD_SEEN`, `TPW_SACKS_SEEN`, `TPW_CREW_STAKES`, `TPW_CREW_FITTINGS`, `TH_CALLS`, `TH_PASSWATCH_ROUTE`, `TPW_NAMES_ASKED`, `TIW_LEAD_BOARD`, `TIW_LEAD_CHIT`, `TIW_GULLY_HEARD`, `TIW_BROADSHEET_READ`, `TIW_SACKS_INSPECTED`, `TIW_IRON_SEEN`, `TIW_HASP_SMITHED`, `TIW_PLATES_SEEN`, `TIW_SKETCHES_SEEN`, `TIW_BERSI_TESTIMONY`, `TIW_LOWMARK_RECOGNISED`, `TIW_ROUTE`, `TH_BRYNJAR`, `TH_STORES`) matches the quest file's tables. `TIW_GATHER_CANCELLED`, `TIW_FRAME_TOUCHED`, `TIW_CAGE_WOUND`, `TIW_HUT_ROUTE` and `TH_SEASON` are set by world events, not dialogue. |
| Lowmark independence | Every Lowmark-conditioned line (`TPW-B0.1`, `TPW-D1.30`, sack and ledger recognition, `TIW-D6.40`) is optional variant text. |
| Minor names [NEW] | Aud's crew (Brann, Holt, Odo) and Nettlehook's "old Freya" are incidental names; removable. |
| Independent review (2026-11-03) | Stencil wording RELIEF — FENMERE; ledger-calendar coexistence note; `[SPLINTER]` on `TIW-D7.56`, `TIW-B12.5`, `TIW-D9.22`; em-dash chains removed from `TPW-B3.3`, `TIW-B6.1`, `TIW-D8.22`. |
