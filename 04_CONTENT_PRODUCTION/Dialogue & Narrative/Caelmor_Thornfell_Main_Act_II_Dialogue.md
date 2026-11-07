# Thornfell Main Act II: Cast and Dialogue (The Echo of Shatterfall, The Summit Hall)

**Status:** Authored production content for Creative Director milestone review. This is the companion to `04_CONTENT_PRODUCTION/Quests/Caelmor_Thornfell_Main_Act_II.md`, which owns step ids, flags and mechanics. Characters marked **[CANON ANCHOR]** come from `LORE/Characters/Caelmor_Characters_Region2_Thornfell_Anchors (Not Full List).txt` and obey the Thornfell rows of the Part 4 character ledger: nothing here gives them a new age, wartime service, kinship, travel, meeting or record custody. Characters marked **[NEW]** are authored and not canon until promoted. Every node that names Ingrith Scarrow, Bersi Coldbrook or Eyvind Stall is tagged `[SPLINTER]` (bible §3.1). Nothing here is production JSON.

**Node format (writer brief):**
- A line: `ID SPEAKER: "Line." (stage note)`.
- A condition goes in braces before the speaker: `ID {if TH_STORES = seized} GERRIT: "..."`. Several lines may share an id when they are condition variants; exactly one plays.
- Player options are numbered lines under the node: `  1. "Option." → NEXT`. An option with a condition: `  2. {if TES_STRATA_READ} "Option." → NEXT`.
- Effects go in braces after the line: `{set FLAG}`, `{set FLAG = value}`, `{event: ...}`.
- Ids follow bible §11.2: `<CODE>-D<n>.<nn>`. Barks use `-B`, inspect texts `-I`. Option menus return to the node's option list ("→ options") unless stated.

**Voice rules:** bible §5.3 is binding. Understated; weather is grammar; nobody calls anything magic; strangers are "walker"; long speeches mean fear or anger. No line in this file identifies an echo-figure, names the node, or gives a count of the Shatterfall dead.

---

## Part 1: Act II voice additions

| Item | Status | Use |
|---|---|---|
| **"Ask the rock."** | [NEW] Riggers' and hornbearers' phrase for sounding a face before trusting it. | Dorn, Gerrit, miners. |
| **"Quick and flat. Slow and twice."** | [NEW] The sounding rule: solid rock answers once and fast; a slab with air behind it answers late, twice. | Dorn teaches it; the player's log uses it. |
| **"Two irons. Never one."** | [NEW] Warden rigging rule. | Dorn. |
| **"Wind trick."** | [CANON behaviour] Dorn's name for altered echoes. He never smiles when he says it. | Dorn, for the Horn-Echo. |
| **"Window's turning."** | [NEW] The storm easing between gusts. Weather as grammar. | Dorn, Gerrit, Iven. |
| **Frost-count** | [NEW] Ridge Warden autumn dating: days counted from the first frost on the Passwatch horn rail ("the ninth of frost"). Wardens and hornwrights count this way; storekeepers and factors count weeks down to First Smoke (Act I ledger). Both reckonings are local and in use at once; no page converts one into the other. | Iven's log; Eyvind's record; any warden. |
| **"A quiet room."** | [NEW] Plain name for a null-point among Stonewake masons and Kaldren. | Kaldren, Iven. |
| **"The hall's ringing."** | [NEW] What sensible people call the Summit hum. Crew call it "the guardian"; nobody confirms them. | Kaldren, Iven; crew (belief). |
| **"Listen. Don't knock."** | [NEW] Kaldren's Summit rule. | Kaldren. |

**What nobody in Act II says:** who blew the Split; how many died at Shatterfall; that the figures are any particular people; that the Summit is alive, angry, judging or warning; what the Echohewn were; how any grain reached Thornfell.

---

## Part 2: Cast notes

### Gerrit Carrick, foreman of out-of-work miners [NEW]
- **In TF-M3:** his crew salvage plates from the Shatterfall collapse for a hornwright who pays by chit. Two pairs are stuck below; he cut his own winch rope short trying to haul.
- **Want:** his people paid and alive, in that order on a good day and the other order today. **Fear:** that the work is what it looks like.
- **Knows:** the plates sell; the buyer's man is a hornwright called Stall who paid at the Whinstone hoist; Stall went up to the Seat himself once; his men found pots in the collapse and left them. **Doesn't know:** what the plates are for; the roster; the Seat's aim.
- **Voice:** defensive first, grateful after. Talks about the licence before anyone asks. Short, blunt, a little too loud. Ashamed of the pots.
- **Change:** at the end he takes the chits off the nail.

### Dorn Feldhorn, Veteran Hornbearer [CANON ANCHOR]
- **Canon:** maintains Thornfell's long-range horn codes; ritual seriousness, private fear; claims echoes sometimes return altered; says some notes should never be played again; calls it "wind tricks", never smiling.
- **In TF-M3:** came with the warden horn because he will not let strangers near "that seat" alone. Teaches sounding, counts returns, sounds one plate once, reads the roster.
- **Knows:** the calls and their counts; that Horn Seats existed (every hornbearer knows the emplacements by reputation; nobody goes); the Third Horn's half-remembered meaning. **Doesn't know:** anything about Shatterfall beyond what the roster says. **Ledger guard:** he says plainly that he was never down there and that what he knows is "what it says". He carries the roster in one outcome and keeps nothing.
- **Voice:** counts aloud. Six words where others use twenty. Dry about his own knees. Never names a figure.

### Maera Cairnwatch, Cairn-Keeper [CANON ANCHOR]
- **Canon:** maintains cairns, remembrance sites and name-stones; gentle, unyielding; absolute authority over the dead; "The stones know how to listen."
- **In TF-M3:** waits at the rim with her private list; asks before she shows; decides the stone on the player's recommendation.
- **Knows:** the cairn names; her private list (from those who came up the rim path, as the list itself says); the Hushfold slip. **Doesn't know:** the roster, until now.
- **Voice:** quiet, complete sentences. Never argues; states. Calls the dead by their names and nobody else by anything but "you" or "walker" (the player, until they climb down; then "you").
- **Guard:** no grave or echo identifies anyone. She says the two records are both honest and does not reconcile them.

### Old Torvek, Voice of the Old Stone [CANON ANCHOR]
- **In TF-M3:** coda only. One sentence at the end of the cairn row, keyed to the outcome. **No wartime claims.**

### Arni and Kolla Vass; Hjalti Brekk; old Tamsin [NEW, minor]
- Gerrit's salvage pairs. Arni jokes; Kolla doesn't. Hjalti is young and frightened; Tamsin is old and isn't. Tamsin speaks the uphill line.

### Iven Ridgeborne, High-path ridge scout [CANON ANCHOR]
- **Canon:** patrols alone far above the passes; echoes before sound; wind carrying voices uphill; stone humming in storms; does not think it magic; believes the mountains are tired; leads the player step by step.
- **In TF-M4:** brings his dated list; guides the climb; owns the sketch and its carry lines; sets his log beside the trial record.
- **Knows:** dates, hours, winds and directions of every hum; the carry lines (from years of whispering); the Echo Landing. **Doesn't know:** that the dates match trials, until he sees.
- **Voice:** reports first (when, where, which wind), interprets last and least. Long silences; uses them.

### Kaldren Deepdelver, Echohewn Keeper [CANON ANCHOR]
- **Canon:** blunt, dryly amused, deeply cautious; understands systems, alignments and stresses, not origins; "They're asleep. And waking them all at once would tear the mountain apart."
- **In TF-M4:** sets the rule (listen, don't knock); teaches the quiet-room test; reads bolt stress; refuses the great mouth; keeps the plates in one outcome.
- **Ledger guard:** never explains what the Echohewn were or what the node is; cannot validate the Summit account. His only line on what happened: "Stresses settled. That's all I can tell you."
- **Voice:** short, dry, practical; insults with affection. Calls the player "walker" until the Counting Room, then "you".

### Eyvind Stall, hornwright [NEW] `[SPLINTER]`
- **In TF-M3:** named on the pay chits and by Gerrit. **In TF-M4:** on the dais, playing; stopped by *Take the horn*; gives up (SX-N2; never fights); names Ingrith.
- **Want:** the sound. **Fear:** that it was never his.
- **Knows:** tuning, the plates, every trial date; that the Summit hums when he tests (he thinks it means the horn is "right"). **Doesn't know:** what the hum is.
- **Voice:** a craftsman in love with a sound. Not cruel; careless. Talks to plates more kindly than to people. Grieves the silence.

### Iron Winter crew [NEW]
- Clan renegades and clanless hires. Crew call the hum "the guardian" and are afraid of it. They fight until defeated at 0 HP (CDR-1); no lines after defeat.

### Act II barks-only cast
| NPC | Status | Notes |
|---|---|---|
| Brynjar Korr | [CANON ANCHOR] | Post-quest barks only, by `TH_BRYNJAR`. No splinter membership; no family casualty. |
| Ressa Highcrag | [CANON ANCHOR] | Post-quest bark (surrendered). "Keeps the horns anyway." |
| Miners, wardens, Stonewake townsfolk | Role-based | Barks. |

---

## Part 3: TF-M3 The Echo of Shatterfall (`TES`)

### TES-B0: lead-in barks

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TES-B0.1 | TF-M2 Completed; journal lead | (journal) | "Carrick's men, Shatterfall. Plates by the crate." |
| TES-B0.2 | Approaching the Cut | MINER (at the shelter) | "Rope went. Rope just went." |
| TES-B0.3 | Approaching the Cut | MINER | "Don't stand on the edge. Gerrit's standing on the edge enough for all of us." |
| TES-B0.4 | Overlook (C5) inspected | MINER | "Them across there? Not ours. Ours don't wave knives." |

### TES-D1: Gerrit at the winch (`S00_cut`)

```
TES-D1.01 GERRIT: (holding a frayed rope end) "If you're from the Assembly, I've a licence for the scree. Somewhere."
TES-D1.02 GERRIT: "Two pairs went down this morning. Last of a seam. Rope parted on the shelf lip."
TES-D1.03 GERRIT: "Storm's early. They're under the overhangs and the path behind them's gone."
  1. "Who are you salvaging for?"                         → TES-D1.10
  2. "What's on the nail?"                                → TES-D1.20
  3. {if TIW_store_ledger held} "Your name's in a ledger at the Whinstone Store."   → TES-D1.30
  4. "Can the pairs be reached?"                          → TES-D1.40
  5. "I'll go down."                                      → TES-D1.50

TES-D1.10 [SPLINTER] GERRIT: "A hornwright. Stall. Eyvind Stall. Pays by the crate, by chit."
TES-D1.11 GERRIT: "I didn't ask what a hornwright wants with that much plate. Work's work. Was."   → options

TES-D1.20 {if TH_STORES = reported} GERRIT: "Chits. Stamped 'W.' Assembly sealed whatever 'W' was. Now they're kindling."   → options
TES-D1.20 {if TH_STORES = seized} GERRIT: "Chits. Hearthguard emptied the store they cash at. Now they're kindling."   → options
TES-D1.20 {if TH_STORES = leverage} GERRIT: "Chits. Still cashing at the hoist, if you don't ask questions. I've stopped asking."   → options

TES-D1.30 GERRIT: (a long look) "Then you know what I am." (beat) "Find my people first. Judge me after."   → options

TES-D1.40 GERRIT: "With a horn and somebody who can rig. I've the horn. Warden brought it."   (nods at the horn rail)   → options

TES-D1.50 GERRIT: "Talk to the warden first. He won't let you near the seat without him. Said so twice."
      {event: TES-D1 end; Dorn at the horn rail active}

TES-D1.90 (resume, before S07) GERRIT: "Still four of mine down there. Well. Two. You got two. Go on."
```

**Inspect: the chit nail (C1, required)** "A post with a nail through a fat sheaf of chits, each stamped 'W.' and initialled for plates by the crate: *E.S.* The newest are a week old. The older ones are crossed through in angry pencil: 'Stonewake won't.'" {set `TES_CHITS_READ`} `[SPLINTER]` (initials)
**Inspect: the chit nail (addition)** {if `TIW_store_ledger` held} "Same as the ledger's line: 'G. Carrick's men, Shatterfall, plates by the crate.' Same stamp."
**Inspect: the plate stack (C2)** "Plates of tuned stone, sorted by size under sacking. Grey Shatterfall grit in every groove. You touch one. Nothing happens. Good."
**Inspect: the carved goat (C4)** "A child's carved goat on the bench. Someone was making it for someone."

**Document: a pay chit** `[SPLINTER]`
> W.
> One crate, plates, Shatterfall grade. Paid at the hoist on sight.
> *E.S.*

### TES-D2: Dorn at the horn rail (`S01_answer`)

```
TES-D2.01 DORN: (horn on his shoulder, watching the gorge) "Walker." (beat) "You'll be the one going down, then."
  1. "Why did you come yourself?"                          → TES-D2.10
  2. "What seat?"                                          → TES-D2.20
  3. {if TH_PASSWATCH_ROUTE = sledge}  "Narrows held, after."   → TES-D2.30
  3. {if TH_PASSWATCH_ROUTE = caravan} "Narrows held, after."   → TES-D2.30
  3. {if TH_PASSWATCH_ROUTE = split}   "Narrows held, after."   → TES-D2.30
  4. {if Lowmark MQ3 Completed} "I've seen weather that breaks and gets back up."   → TES-D2.40
  5. "Call them."                                          → TES-D2.50

TES-D2.10 DORN: "Somebody sent for a horn. There's a seat down there. I don't let strangers near it alone."   → options
TES-D2.20 DORN: "Horn seat. War. Every hornbearer knows where the seats were. Nobody goes." (beat) "I've never been down."   → options
TES-D2.30 {if TH_PASSWATCH_ROUTE = sledge}  DORN: "Nettlehook ate. Good." → options
TES-D2.30 {if TH_PASSWATCH_ROUTE = caravan} DORN: "Wardens got paid. Nettlehook grumbled. Both alive." → options
TES-D2.30 {if TH_PASSWATCH_ROUTE = split}   DORN: "Half of everything got across. That's a lot of halves." → options
TES-D2.40 DORN: "Lowland weather. Ours is louder." → options

TES-D2.50 DORN: "Lost, then. Listen for two short. Count what comes after."
      (Dorn blows Lost: one long, rising. Glyph: a rising line.)
      {event: listen interaction active}
TES-D2.51 (after the listen) DORN: "Two Answers. First's near. One beat, under a lip."
TES-D2.52 DORN: "Second's three beats, and the gorge is in it. Lower down."
TES-D2.53 DORN: "Path's gone behind them, or they'd be climbing." (blows Answer: two short) "That's 'we heard; stay'."
      {event: TES-D2 end → S02}
```

### TES-B1: call barks

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TES-B1.1 | First Answer returns | (horn, below) | [Two short. Near.] |
| TES-B1.2 | Second Answer returns | (horn, below) | [Two short. Far, with the gorge behind it.] |
| TES-B1.3 | Optional: "Which is the echo?" | DORN | "Echo's fainter and late. The answer's the one with a person behind it." |

### TES-B2: the Gust Stair (`S02_descent`)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TES-B2.1 | First whistle tell | DORN (one shelf behind) | "Fifth up. Get behind a face." |
| TES-B2.2 | Player caught by a gust | DORN | "Wall's your friend. Lean on it." |
| TES-B2.3 | Player uses the shelf gap | DORN | "I'll take the planks. Knees." |
| TES-B2.4 | TES-E1 starts | DORN | "Shale's moving. That's not wind." |
| TES-B2.5 | TES-E1 ends | DORN | "Vipers sleep in shale. They were up early too." |

**Inspect: armour fragment (L1)** "A rusted plate from a shoulder. No mark you can read. The snow is filling it."
**Inspect: shelter mark (L1)** "A chalked notch on the face, renewed this season. Somebody keeps the shelters honest."

### TES-B3: the Jam (`S03_jam`)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TES-B3.1 | Jam reached | DORN | "Fresh. This week's. The gorge sheds." |
| TES-B3.2 | Mining starts | DORN | "Hit the seam, not the stone." |
| TES-B3.3 | Mining complete | DORN | "You've done that before." {set `TES_JAM_MINED`} |
| TES-B3.4 | Crew called | DORN | (blows Gather: three short) "They'll come. They'll take their time." |
| TES-B3.5 | Crew arrives | MINER | "Gerrit says if we lose a lever he'll take it out of us." |
| TES-B3.6 | Crew complete | MINER | "Window's going. Go on, before it shuts." {set `TES_JAM_CREW`} |

### TES-D3: asking the rock (`S04_rig_one`)

```
TES-D3.01 DORN: (crouched at the Lip, palm flat on the face) "An iron's as good as the rock it's in. No better."
TES-D3.02 DORN: "Rock tells you, if you ask. Strike it with the butt. Count."
TES-D3.03 DORN: "Quick and flat, it's solid. Slow and twice, it's a slab with air behind it."
TES-D3.04 DORN: "Two irons. Never one." (hands over the coil bag)
  1. "What if I pick wrong?"          → TES-D3.10
  2. "Why the rust stains?"           → TES-D3.20
  3. "Show me."                       → TES-D3.30

TES-D3.10 DORN: "Then the rock tells you when you load it. Loudly. Nobody falls. We lose time." (looks at the sky) "We haven't much."   → options
TES-D3.20 DORN: "Somebody rigged here before. In the war, by the look. Didn't all choose well either."   → options
TES-D3.30 DORN: (strikes the face beside a seam) "There. Hear it? Once. Quick. That's rock." (strikes a hand lower) "And that. Twice, late. Slab."
      {event: TES-D3 end; seams interactive}
```

### TES-B4: the Lip (barks)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TES-B4.0a | Sound: solid (log) | (log) | "A quick, flat knock comes back." |
| TES-B4.0b | Sound: loose (log) | (log) | "Slow. It comes back twice." |
| TES-B4.1 | First horn blast (§A8.2) | DORN | "Wind trick." |
| TES-B4.2 | First figures charge | DORN | "Out of the line. They don't turn. They don't look." |
| TES-B4.3 | First figure broken | DORN | "It'll be back. Storm's not done with it." |
| TES-B4.4 | Two irons set, before rig | DORN | "Line now. Then we find out." |
| TES-B4.5 | Before each pay-out segment | DORN | (blows Answer) "That's for them. They move when they hear it." |
| TES-B4.6 | Loose iron loaded | DORN | "Feel that? Pull it." |
| TES-B4.6b | Second loose iron in the quest (`TES_LOOSE_IRONS` ≥ 2) | DORN | "Rock's lying to you. Ask it again." |
| TES-B4.7 | Both irons loose | DORN | (hand on the brake) "Not loading that. Both are slab. Again." |
| TES-B4.8 | Player leaves the gorge (pairs waiting) | KOLLA (below) | "We're not going anywhere." |
| TES-B4.9 | Pay-out segment 1 | ARNI (below) | "Tell Gerrit it's my rope that broke. It wasn't. Tell him anyway." |
| TES-B4.10 | Pay-out segment 2 | KOLLA | "Slower. Slower. That's it." |
| TES-B4.11 | Pay-out segment 3 | ARNI | "Feet down! Feet on rock!" (beat) "Thank you, walker. I'll buy you a drink with a chit." |
| TES-B4.12 | Miner belief bark (first figures seen) | KOLLA (below) | "The dead are up." |
| TES-B4.13 | Reply to TES-B4.12 | DORN | "Wind trick." |
| TES-B4.14 | Rig complete | DORN | "Two left. Lower. Louder." {set `TES_PAIR_ONE`} |

### TES-D4: the Broken Engine (optional, `S05` approach)

```
TES-D4.01 KOLLA: (sheltered in the engine's lee, wrapped in Arni's coat) "Gerrit'll want to know we're alive. He'll pretend he didn't."
  1. "What did you dig for down there?"   → TES-D4.10
  2. "Stay here till the window turns."   → TES-D4.20

TES-D4.10 KOLLA: "Plates. Under the fall on the big shelf. You dig, you find what's under it." (stops) "We found pots."   → options
TES-D4.20 ARNI: "Here? It's the only thing in the gorge that's held up since the war." (pats the frame)   {event: TES-D4 end}
```

**Inspect: the broken engine (L4, TDS06)** "A siege engine, embedded in the wall. Its frame is Thornfell timber, cut square and wedged as a prop. It held a shelf up, before the fall."

### TES-B5: the Hollow (barks)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TES-B5.1 | Hollow reached | DORN | "Your turn to ask it. I'll keep them talking." |
| TES-B5.2 | Strike during a swell (log) | (log) | "Couldn't hear it over the gorge." |
| TES-B5.3 | Swell tell | DORN | "Note's dropping. Wait." |
| TES-B5.4 | Uphill group (§A8.3) | TAMSIN (on the line) | "Those ones are running the wrong way." |
| TES-B5.4b | After TES-B5.4 | DORN | (no line; he looks up at the Seat, then back at the brake) |
| TES-B5.5 | Echo-line charge | DORN | "Three abreast. Middle one." |
| TES-B5.6 | Loose iron loaded | DORN | "That's slab. You know what to do." |
| TES-B5.7 | Pay-out segment 1 | HJALTI (below) | "Is it holding? Tell me it's holding." |
| TES-B5.8 | Pay-out segment 1 reply | TAMSIN | "It's holding, boy. Stop asking it." |
| TES-B5.9 | Pay-out segment 3 | TAMSIN | "Floor path's sound. We'll walk. Mind yourselves near the seat." |
| TES-B5.10 | Rig complete | DORN | "That's all of them." (beat) "Now the seat." {set `TES_PAIR_TWO`} |

### TES-B6: the seat approach (`S06_seat_approach`)

No dialogue names what happens here. Dorn speaks only of weather.

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TES-B6.1 | The figures stop and stand | DORN | "They've stopped running." |
| TES-B6.2 | First surge tell | DORN | "Face. Now." |
| TES-B6.3 | Player breaks the whole stand | DORN | "That's a gust off the storm. More." |
| TES-B6.4 | Third swell endured | DORN | "Whistle's dropping." |
| TES-B6.5 | Window turns | DORN | "Window's turning." |
| TES-B6.6 | Figures fade | DORN | "Go on. Before it thinks better of it." |

### TES-D5: the rack (`S07_seat`, sounding)

```
TES-D5.01 DORN: (at the rack, not touching it) "Look where they point."
TES-D5.02 DORN: "Down the shelf. Every plate." (beat) "You can sound one. One plate. Not a call. Never a call."
  1. "Why one?"                       → TES-D5.10
  2. (Strike a plate.)                 → TES-D5.20

TES-D5.10 DORN: "Because some notes shouldn't be played again. One plate is a note. Two is a start."   → options

TES-D5.20 (the player strikes; a low, plain note; the return comes from below)
TES-D5.21 DORN: (counting) "One. Two." (beat) "From under us. The camp shelf."
TES-D5.22 DORN: "The far approach is eight, nine beats off. That came back in two."
TES-D5.23 DORN: (takes his glove off the rack) "That's enough asking."
      {set TES_SEAT_SOUNDED}
```

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TES-B7.1 | Strata path taken | DORN | "Careful. That's not scree you're on." |
| TES-B7.2 | Player tries a second plate | DORN | (hand on the player's wrist) "Once." |
| TES-B7.3 | Rack inspected later (post-quest) | (log) | "You said once." |

### Inspect texts: the Horn Seat (`S07_seat`)

| Object | Text | Condition |
|---|---|---|
| The seat (H1) | "A stone seat cut into the gorge wall, worn smooth where someone sat. It faces down the shelf. Snow in the seat." | — |
| The plate rack (H2, required) | "An iron rack bolted into the rock, holding tuned plates in a row. Every plate is angled down the shelf, toward the camp below, and away from the far approach." | — |
| Empty slots | "Three slots empty. The pry marks are bright. Not old." | — |
| Empty slots (addition) | "Gerrit said Stall went up himself once." `[SPLINTER]` | after `TES-L-GERRIT` or Gerrit asked |
| The log niche (H3) | "A niche at shoulder height. A lead-lidded tin, iced shut." | — |
| Buckles (H4, required) | "Belt buckles under the collapse, on the near side of the fall. Clan stamps. More than one clan. Thornfell's." | — |
| Cookpots (H4, required) | "Cookpots, flattened by stone. Someone was cooking on this shelf when it came down." | — |
| Horn (H4, required) | "A horn with Thornfell bindings, under the fall, on the near side. Its mouth is full of grit." {when all three: set `TES_STRATA_READ`} | — |
| The strata cut | "The miners dug through the collapse for plates. The cut shows the fall in layers, and under the layers, a camp." | — |

### TES-D6: the roster (`S07_seat`)

```
TES-D6.01 (the player opens the tin: TES_horn_roster acquired; document view)
TES-D6.02 DORN: "Let me see it." (reads; takes a long time over the last lines; says nothing)
TES-D6.03 DORN: (taps the leaf) "No answer."
TES-D6.04 DORN: "I want Maera to see that before anybody else does."
  1. "What does it mean?"                 → TES-D6.10
  2. "Who blew it?"                       → TES-D6.20
  3. "Let's go up."                       → TES-D6.30

TES-D6.10 DORN: "It means what it says. I wasn't there. Nor were you."   → options
TES-D6.20 DORN: (looks at the margin) "Damp took the names. Margins go first." (beat) "Don't ask the seat. It doesn't know."   → options
TES-D6.30 DORN: (blows Rest: one long; it is answered faintly from the Cut) "Ladders. Mind the snow off the rim."
      {event: TES-D6 end → S08}

TES-D6.90 (resume at Passwatch horn post, if the player left before the rim) DORN: "Maera's still on the rim. She'll wait. She's good at it. Better than me."
```

### Document: `TES_horn_roster` (quest item)

The tin holds four leaves of a station roster, sewn with gut. The left margin of every leaf, where duty names were written, has rotted to lace. What remains is the right-hand columns. The player sees the last leaf by default and can turn back. No year is legible; the day is given as the station counted it.

> **HORN STATION. SHATTERFALL SEAT.**
> *[left margin rotted on every leaf]*
>
> **Leaf 1.** Shelf watch, day 9. Weather hard. Rest at dawn, answered. Gather to the camp shelf, 2nd hr, answered. Plates checked. Rack seated.
>
> **Leaf 2.** Shelf watch, day 10. Weather harder. Fall from the upper rim, 1st hr past noon, answered. Enemy reported on the far approach, 2nd hr. Seat ordered ready.
>
> **Leaf 3.** Day 10, cont. Rear guard to hold the lower shelf till the far approach is filled. Seat to wait on the word.
> 3rd hr. Far approach filling.
> 4th hr. The word.
>
> **Leaf 4.** Day 10, cont.
> 4th hr, late. **Split.**
>
> *[beneath, in another hand, pressed hard]*
> Rear guard not recalled. No answer.

(No line names a person. No line gives a number of the dead. The roster never says the shelf fell; the player has the strata for that.)

### TES-B8: out by the ladders (`S08_climb_out`)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TES-B8.1 | First pitch | DORN (below) | "Hands, feet, hands. Don't look at the seat." |
| TES-B8.2 | Snow slides off the rim | DORN | "That's only snow. It's allowed." |
| TES-B8.3 | Top of the ladders | DORN | "Clear. Look at that. Like nothing happened." (beat) "Something happened." |

### Inspect texts: the rim cairns (`S09_cairns`)

Three cairns are reachable. Each facing stone carries several names and, under them, the same line. The row continues along the rim past the end of the path; the player cannot reach or count it.

| Object | Text | Condition |
|---|---|---|
| First cairn (required, any one) | "Names cut deep and kept clean: ASGEIR HOLM. BRENNA TALLOW. ULF GARROW. Under them: LOST IN THE GORGE STORM. The base is hollow, the old way. Nobody is under it." {set `TES_CAIRNS_READ`} | — |
| Second cairn | "HALLVARD BRENN. SIGNY ROOK. And more, under rime. LOST IN THE GORGE STORM." {set `TES_CAIRNS_READ`} | — |
| Third cairn | "TORSTEIN MARR. ODDA FELL. LOST IN THE GORGE STORM. Someone has left a stormflower in a crack, dried flat." {set `TES_CAIRNS_READ`} | — |
| The row beyond | "The cairns go on along the rim, further than the path." | — |
| First cairn (after amended) | "Under LOST IN THE GORGE STORM, a newer line, the cuts still pale: BENEATH OUR OWN HORN." | `TH_SHATTERFALL_ACCOUNT = amended` |
| Cairn niche (after beside) | "A slate stops the niche. Behind it, a lead tin." | `= beside` |

### TES-D7: Maera at the reading stone (`S09_cairns`)

```
TES-D7.01 MAERA: (standing by the flat stone, hands in her sleeves) "Dorn sent word up. I've been here since the storm broke."
TES-D7.02 MAERA: "What was in the tin?"
  1. (Give her the gist.)         → TES-D7.10
  2. (Show her the roster.)       → TES-D7.10

TES-D7.10 MAERA: (reads, or listens; her face does not change) "Fourth hour, late."
TES-D7.11 MAERA: (takes a folded list from inside her coat) "This isn't for the stones. It never has been." (Maera's private list opens; document view)
TES-D7.12 MAERA: "Set them down together. I want to see them next to each other. I never had the other one."
      {event: side-by-side interaction active}

TES-D7.20 (after the side-by-side) MAERA: "Both honest. Both written by people who weren't down there."
TES-D7.21 MAERA: "One says the horn was in the fourth hour. One says they were seen holding in the fifth."
TES-D7.22 MAERA: "I'm not going to tell you which. I don't know."
      {set TES_RECORDS_SET}
  1. {if TES_STRATA_READ} "Under the seat there's a camp. Under the fall."   → TES-D7.30
  2. "Why does the stone say 'storm'?"                                        → TES-D7.35
  3. "Is there anything else?"                                                → TES-D7.40
  4. "Dorn wants to say something."                                           → TES-D8.01

TES-D7.30 MAERA: "I know where the shelf is." (beat) "I didn't know what was on it."   → options

TES-D7.35 MAERA: "Because that's what we were told to cut. Storms are nobody's."   → options

TES-D7.40 MAERA: "One thing." (takes a small slip from another pocket) "Hushfold renews this with me every spring. They want a stone, for someone who went over the pass."
TES-D7.41 MAERA: "Same name as one on my list." (beat) "Names repeat up here. Could be two people. Could be one."
      {name-slip inspect available}   → options
```

**Inspect: the Hushfold name-slip (optional)** See document below. {set `TES_NAMESLIP_SEEN`}

### Document: Maera's private cairn list (held by Maera; not a quest item)

A single leaf of heavy paper, folded small and soft at the folds. It is the leaf for Shatterfall. The player sees only this leaf; the list continues onto another, which Maera keeps her hand on.

> **SHATTERFALL. NOT FOR THE STONES.**
>
> The rear guard of the gorge. They held the gorge.
> Last seen on the lower shelf, holding, at the fifth hour, by those who came up the rim path after.
>
> Asgeir Holm. Held.
> Brenna Tallow. Held.
> Ulf Garrow. Held.
> Sig Brede. Held.
> Signy Rook. Held.
> Torstein Marr. Held.
> Odda Fell. Held.
>
> *(continued)*
>
> *[at the foot, in the same hand, smaller]*
> Cut on the rim as the Assembly asked: lost in the gorge storm. I cut what I was asked. I keep what I was told.

(No line gives a total. "Continued" is the only indication the list is longer. Maera's hand covers the second leaf in every presentation.)

### Document: Hushfold name-slip (held by Maera; temporary name-slip)

> For a stone, if one can be had.
> **Sig Brede.** Went over the pass.
> Kept by the Brede hearth, Hushfold. Renewed each spring.

(Register seed only: *The Weight of a Name* owns it. Maera's reading "could be two people, could be one" stands. Not resolved here.)

### TES-D8: No answer (`S09_cairns`)

```
TES-D8.01 DORN: (has been standing back; steps up to the stone) "May I."
TES-D8.02 DORN: (reads the roster's last line aloud) "'Rear guard not recalled. No answer.'"
TES-D8.03 DORN: "There was a reply. The Third Horn. Answer, then a long rising. 'Heard. Someone's still out.'"
TES-D8.04 DORN: "It's on my training board. Nobody blows it. Nobody told me why." (beat) "By this, nobody blew it here."
  1. "Were you there?"                  → TES-D8.10
  2. "Why would they stop teaching it?"  → TES-D8.20
  3. (Say nothing.)                      → TES-D8.30

TES-D8.10 DORN: "No. It's what it says. I wasn't there."   → TES-D8 options
TES-D8.20 DORN: "Don't know. Somebody stopped wanting to hear it." (beat) "That's a guess. Don't write it down."   → TES-D8 options
TES-D8.30 DORN: (folds his hands over the horn) "Your word to give, Maera. Not mine."
      {set TES_THIRD_HORN_HEARD; event: TES-D8 end → S10}
```

### TES-D9: what the stone says (`S10_choose`)

```
TES-D9.01 MAERA: "I decide what's cut. I always have." (beat) "I asked Dorn to bring someone who'd climb down. You climbed down."
TES-D9.02 MAERA: "Tell me what you'd have the stone say. Then I'll decide."
  1. "Cut it under the names. 'Beneath our own horn.'"            → TES-D9.10
  2. "Put the roster in the cairn. Leave the stone."             → TES-D9.20
  3. "Send it to Passwatch. Let the wardens keep it. Leave the stone."   → TES-D9.30
  4. "Why ask me?"                                               → TES-D9.40

TES-D9.40 MAERA: "Because I've read this list alone for a long time. I wanted to hear it said by someone else."   → TES-D9 options

TES-D9.10 MAERA: (a long breath) "Then it's cut." (takes a chisel from her bag) "Hold the lamp."
TES-D9.11 MAERA: (cuts the first word; the sound of the chisel carries along the rim) "The rest by morning. It'll be straight. I don't cut crooked."
TES-D9.12 MAERA: "The roster comes with me. It goes with my list. They should be kept together now."
      {set TH_SHATTERFALL_ACCOUNT = amended; TES_horn_roster removed}   → TES-D10.01

TES-D9.20 MAERA: "Beside, then." (opens the niche) "Put it in yourself."
TES-D9.21 (the player places the tin; Maera stops the niche with the slate)
TES-D9.22 MAERA: "Anyone who opens it can read it. Nobody is told to." (beat) "Damp will find it, in time. So will someone."
      {set TH_SHATTERFALL_ACCOUNT = beside; TES_horn_roster removed}   → TES-D10.01

TES-D9.30 MAERA: "Kept." (wraps the tin in oilcloth and ties it with her cord) "Under my cord. For now."
TES-D9.31 MAERA: "The stone stays as it is. For now." (she says it twice; she means it twice)
TES-D9.32 MAERA: (hands the packet to the Ridge Warden runner who carried Dorn's word up to the rim) "Passwatch post. The strongbox. Under my cord till somebody with a reason asks."
TES-D9.33 DORN: (watching the runner go) "Post keeps it. Not me. Good."
      {set TH_SHATTERFALL_ACCOUNT = kept; TES_horn_roster removed}   → TES-D10.01
```

### TES-D10: Torvek (coda)

Old Torvek has walked up the rim path and stands at the end of the reachable row. He speaks once and goes.

```
TES-D10.01 {if TH_SHATTERFALL_ACCOUNT = amended} TORVEK: "Stone's honest now. Honest is heavy."
TES-D10.01 {if TH_SHATTERFALL_ACCOUNT = beside}  TORVEK: "Paper in a cairn. The wind reads it first."
TES-D10.01 {if TH_SHATTERFALL_ACCOUNT = kept}    TORVEK: "Silence is a stone too."
TES-D10.02 MAERA: (to the player, not looking away from the row) "Go down. Eat. Sleep in a bed. The stones know how to listen. They can manage without you tonight."
      {event: TES-D10 end → quest Completed}
```

### TES-L-GERRIT: Gerrit, after (optional, Carrick's Cut, post-quest)

```
TES-L-GERRIT.01 GERRIT: (taking the chits off the nail, one by one) "All four up. All four complaining. That's how you know."
  1. "Your men found pots under the fall."   → TES-L-GERRIT.10
  2. "Who took the plates from the seat's rack?"   → TES-L-GERRIT.20
  3. "What will you do now?"   → TES-L-GERRIT.30

TES-L-GERRIT.10 GERRIT: "We did. We left them. Didn't seem right to sell a pot." (beat) "Didn't seem right to say, either. So we didn't."   → options
TES-L-GERRIT.20 [SPLINTER] GERRIT: "Stall went up himself. Once. Wouldn't let us watch. Came down with three under his arm like they were his children."   → options
TES-L-GERRIT.30 GERRIT: "Rope and irons. People will want to go down there now. Somebody should sell them the right rope."   {event: end}
```

### TES post-quest barks

| Id | Speaker | Line | Condition |
|---|---|---|---|
| TES-B9.1 | ARNI (Carrick's Cut) | "Bought you that drink. Chit bounced. It's the thought." | TES Completed |
| TES-B9.2 | TAMSIN (Carrick's Cut) | "They were running the wrong way. I've said it. I'll not say it again." | `TES_UPHILL_SEEN` |
| TES-B9.3 | HJALTI (Carrick's Cut) | "I'm not going down again. I'm going to be a baker." | TES Completed |
| TES-B9.4 | DORN (Passwatch horn post) | "Two irons. Never one. You've got it now." | TES Completed |
| TES-B9.5 | WARDEN (Passwatch strongbox) | "Packet under a cairn-keeper's cord. Nobody touches it. I don't even look at it. Much." | `kept` |
| TES-B9.6 | MAERA (Oath Cairn Fields) | "The cut's straight. I told you." | `amended` |
| TES-B9.7 | MAERA (Oath Cairn Fields) | "Nobody has opened the niche yet. They will." | `beside` |
| TES-B9.8 | MAERA (Oath Cairn Fields) | "For now is a long word, up here." | `kept` |
| TES-B9.9 | BLOOD-OATH HOUSEHOLDER (Stonewake) | "Cut words on the rim. Our horn, she says. Our horn saved the passes." | `amended` |
| TES-B9.10 | BRYNJAR (Stonewake) | "Somebody's cutting at Shatterfall. Fine. Cut. The horn still split the ridge." (pounds a table that isn't there) | `amended` + `TH_BRYNJAR = defended` |
| TES-B9.11 | BRYNJAR (Stonewake) | "Shatterfall." (beat; quieter than anyone has heard him) "I've told that story at feasts. To children." | `amended` + `TH_BRYNJAR = disowned` |
| TES-B9.12 | BRYNJAR (Stonewake) | "Heard you were down the gorge. Heard it hums at you. Good place for a horn, the gorge." | `beside` or `kept` |
| TES-B9.13 | MINER (Carrick's Cut) | "The dead are up in storms. Don't let the warden tell you different. He'll say wind." | TES Completed |
| TES-B9.14 | DORN (reply if nearby) | "Wind trick." | with TES-B9.13 |

---

## Part 4: TF-M4 The Summit Hall (`TSH`)

### TSH-D1: Iven's list (`S00_offer`)

```
TSH-D1.01 IVEN: (at the horn board, a warden log under his arm, snow on his shoulders) "Walker. Maera said you'd go down a gorge for strangers."
TSH-D1.02 IVEN: "I've a list. Nights the Summit hummed with no storm in it." (opens the log; Iven's list readable)
TSH-D1.03 IVEN: "Dates, hours, wind. Six since first frost. It used to be never."
  1. "What do you think it is?"                         → TSH-D1.10
  2. {if TIW_SKETCHES_SEEN} "A hornwright's sketches named the Summit's great hall."   → TSH-D1.20
  3. {if TES_CHITS_READ} "Someone's been buying horn plates by the crate."   → TSH-D1.25
  4. "Take me up."                                       → TSH-D1.30

TSH-D1.10 IVEN: "Mountains get tired." (beat) "Not like this."   → options
TSH-D1.20 IVEN: "The great hall. Your sketches said so too." (writes something in the log's margin)   → options
TSH-D1.25 IVEN: "Then somebody's hauling them up. There are runner marks on the stair foot." → options
TSH-D1.30 IVEN: "Stair foot, then. I sent for Kaldren. He'll be sitting on the bottom step complaining. That's how you find him."
      {event: TSH-D1 end → S01}
```

### Document: Iven's hum list (Iven's Ridge Warden log; held by Iven)

Iven keeps two columns. He lists the storm nights as well so nobody can say he confused them.

> **RIDGE WARDEN LOG. HIGH PATH. I. RIDGEBORNE.**
> **Summit: hum heard, no storm in it.**
>
> | Frost | Hour | Wind | What |
> |---|---|---|---|
> | 3rd | an hour past dusk | light, from the pass side | Faint hum, Summit. Long. Thought it was me. |
> | 9th | second hour of night | still | Hum, Summit, plain. Crows off the Crown face at once. |
> | 14th | — | — | Not on the high path. Passwatch rota. Heard nothing there. |
> | 18th | second hour | light, uphill | Hum, Summit. Dust on the Crown stair in the morning, in rings. |
> | 21st | third hour | still | Hum, Summit. Echo before sound on the Echo Landing, twice. |
> | 24th | second hour | still, cold | Hum, Summit, strong. Felt it in the stair rail. |
> | 27th | second hour to fourth | light, from the pass side | Hum, Summit, strongest. Snow came off the Crown face in sheets. |
>
> **Storm nights, hummed as storms do (for comparison):**
> 11th (hard wind; hummed with the gusts, stopped with them). 20th (sleet; same). 26th (storm; hummed; can't separate anything from it).
>
> *[margin, in the same hand]* Six with no storm. It used to be never.

(Six hums in the no-storm column, plus the 14th rota line. Dates are frost-count. They match `TSH_trial_record`: trials on the 3rd, 9th, 14th, 18th, 21st, 24th, 26th, 27th. The 14th is the rota gap; the 26th is a storm night Iven cannot separate.)

### TSH-D2: Kaldren at the stair foot (`S01_stair_foot`)

```
TSH-D2.01 KALDREN: (on the lowest step, boots off, rubbing a foot) "Walker. Iven. You'll want to know why I'm here."
TSH-D2.02 KALDREN: "Somebody has to stop you all from being clever."
TSH-D2.03 KALDREN: "One rule. Up there, nobody hits anything to hear what it says."
TSH-D2.04 KALDREN: "You've been down Shatterfall, I hear. Up here you listen. You don't knock."
  1. "What's up there?"                 → TSH-D2.10
  2. "Is it a guardian?"                → TSH-D2.20
  3. "Put your boots on."               → TSH-D2.30

TSH-D2.10 KALDREN: "Stairs, halls, quiet rooms. Old work. Good work." (beat) "Asleep, mostly. I'd like it to stay that way."   → options
TSH-D2.20 KALDREN: "It's a hall. Halls ring." (beat) "They're asleep. And waking them all at once would tear the mountain apart. So we don't."   → options
TSH-D2.30 KALDREN: (pulling them on) "Dwarves climb better barefoot. Nobody believes me. Fine."
      {event: TSH-D2 end → S02}

TSH-D2.90 (resume) IVEN: "Stairs haven't moved. I checked."
```

**Inspect: sled marks (F2)** "Runner marks and crate-scrapes up the edge of the steps. Something heavy went up on a sledge. More than once."

### TSH-B2: the stairs (`S02_ascent`)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TSH-B2.1 | Outer stair | IVEN | "Lip's high enough everywhere. They built it for people who'd look down." |
| TSH-B2.2 | Crows mob (TSH-E1) | KALDREN | "Crows. Of course crows." |
| TSH-B2.3 | Distant test note; crows lift | (a faint horn note from above; every crow on the face lifts at once) | — |
| TSH-B2.4 | After the crows lift | IVEN | "That's the ninth of frost again. Same crows." |
| TSH-B2.5 | Inner stair, first draw | IVEN | "Watch the torches. They lean before it breathes." |
| TSH-B2.6 | Lantern blown out | IVEN | (relighting it from his) "Again." |
| TSH-B2.7 | Second time | IVEN | "Again." (beat) "Again is fine." |
| TSH-B2.8 | Channel mouth inspected | KALDREN | "Air goes in, air comes out. Rock's breathing because somebody cut it a throat. That's all." |
| TSH-B2.9 | Echo Landing (§B6 Beat 2) | (a footstep from the next landing up, one beat before the player's own) | — |
| TSH-B2.10 | Echo Landing | IVEN | "That one. Every time." |
| TSH-B2.11 | Echo Landing, player asks (wait and listen) | IVEN | "I don't know. I've stopped minding." |
| TSH-B2.12 | Echo Landing | KALDREN | (says nothing; looks at the ceiling a while) |

**Inspect: channel mouth (S2)** "The draw pulls at your sleeve, then lets go. Something below is breathing in and out through the rock. It's only air."

### TSH-B3: the Upper Landing (TSH-E2)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TSH-B3.1 | Spotted | SPEAR | "Up the stair! Somebody's on the stair!" |
| TSH-B3.2 | Hornman raises horn | HORNMAN | "Hold, I'll call it —" |
| TSH-B3.3 | Hornman interrupted | HORNMAN | "My teeth —" |
| TSH-B3.4 | Spear engages (second line) | SPEAR | "Don't go in there. It's awake." |
| TSH-B3.5 | Hornman engages `[SPLINTER]` | HORNMAN | "It's the guardian. Eyvind says it means the horn's right. I say it means go home." |
| TSH-B3.6 | Reply (during the fight) | IVEN | "Halls don't hear the landing. The landing hears the halls. You'll hear plenty." |

**Inspect: crates (S4)** "Empty plate crates. Grey grit in the corners. Shatterfall grit."
**Inspect: cookfire (S4)** "Warm. A pot of something with too much salt. They've been up here days."

### TSH-D3: the whisper hall (`S04_listen`)

```
TSH-D3.01 IVEN: (at the Low Mouth, the sketch open on his knee) "Whisper here and it's heard at the other two. Whisper there, here."
TSH-D3.02 IVEN: "Each mouth hears along three lines. I drew them. Years of whispering at a wall on my own."
TSH-D3.03 IVEN: "Listen at each one. Then whisper down the lines. Some come back. Some don't."
  1. "What doesn't come back?"            → TSH-D3.10
  2. (To Kaldren) "Is whispering knocking?"   → TSH-D3.20
  3. "Who's in there?"                     → TSH-D3.30
  4. "Let me listen."                      → TSH-D3.40

TSH-D3.10 IVEN: "Whatever goes into a quiet room. It just stops." (beat) "Like the gully on the Whinstone track. If you walked it."   → options
TSH-D3.20 KALDREN: "A whisper's not a knock." (beat) "Don't sing."   → options
TSH-D3.30 IVEN: "The horn's on the dais. You can hear that from Stonewake, nearly. The rest you'll have to find."   → options
TSH-D3.40 IVEN: "I'll write down what you hear. You say it, I write it."
      {event: TSH-D3 end; listening points active}
```

### TSH-B4: listening and whispering (the margin log)

Each **Listen** plays the mouth's three lines together with directional panning; the subtitles and Iven's margin log name each line. Each **Whisper** result is logged as "back" or "gone". Texts match the quest file §B8.1.

| Id | Mouth | Line | Listen (subtitle / margin) | Whisper (margin) |
|---|---|---|---|---|
| TSH-B4.1 | Low | Left | "Left: a file on metal, slow, near. A man swearing at it softly." | "Left: gone." |
| TSH-B4.2 | Low | Ahead | "Ahead: the horn, very loud. Someone counting four." | "Ahead: back." |
| TSH-B4.3 | Low | Right | "Right: dice in a cup. A voice muttering about luck." / {if `TH_STORES = leverage`} "Right: dice in a cup. Two voices, one laughing." | "Right: gone." |
| TSH-B4.4 | Long | Left | "Left: someone humming the test note, badly. A cough." | "Left: gone." |
| TSH-B4.5 | Long | Ahead | "Ahead: the horn. Under it, water dripping into a bucket. Steady. No breath near it." | "Ahead: back." |
| TSH-B4.6 | Long | Right | "Right: the file on metal. Further off, dice." | "Right: back." |
| TSH-B4.7 | Crown | Left | "Left: humming, close. The cough again." | "Left: back." |
| TSH-B4.8 | Crown | Ahead | "Ahead: the horn, and the hall humming after it." | "Ahead: back." |
| TSH-B4.9 | Crown | Right | "Right: the drip, near. Nothing else." | "Right: gone." |
| TSH-B4.10 | Any | Whisper gone (audio) | (your whisper goes out along the line and doesn't come back) | — |
| TSH-B4.11 | Any | Whisper back (audio) | (your whisper comes back off the far wall, thin, a beat late) | — |
| TSH-B4.12 | Crew, during listening | (heard at the Low Mouth, ahead) | EYVIND [SPLINTER]: "Again. Four, and..." | — |
| TSH-B4.13 | Crew, during listening | (heard at the Crown Mouth, left) | HORNMAN: "Dust's standing up again. I hate it when it stands up." | — |

### TSH-D4: the sketch (`S05_mark`, commit in `S07`)

```
TSH-D4.01 IVEN: (handing over the sketch) "Six alcoves. Mark them. Crew, silent or empty. Leave it blank if you don't know."
  1. "Read me the margin."                    → TSH-D4.10
  2. "How do I find where someone is?"         → TSH-D4.20
  3. (To Kaldren) "How do I find a quiet room?" → TSH-D4.30
  4. (Mark the sketch.)                        → TSH-D4.40

TSH-D4.10 IVEN: (reads back every line the player has heard, in order, in the margin's words)   → options
TSH-D4.20 IVEN: "Something heard on two lines is where the lines cross." (beat) "That's all I've got. It's usually enough."   → options
TSH-D4.30 KALDREN: "Something that eats a whisper on both its lines is a quiet room." (beat) "I'll show you one before you go in."   → options
TSH-D4.40 (sketch UI; marks editable)   {event: S05 complete on first mark}

TSH-D4.50 (commit; at the Counting Room door or the open stair, after S06) IVEN: "Happy with it?"
  1. "Go in."                → TSH-D4.51
  2. "Not yet."              → (sketch UI)

TSH-D4.51 {if TSH_MAP_TIER = good} IVEN: "Then the quiet way. Through his room. Nobody hears you come."
TSH-D4.51 {if TSH_MAP_TIER = fair} IVEN: "The stair, then. They'll hear the last turn. Be quick on it."
TSH-D4.51 {if TSH_MAP_TIER = poor} IVEN: "The stair." (beat) "They'll have heard us whispering. Walls go both ways."
      {set TSH_MAP_TIER; event: S07 entry route}
```

(Iven never says whether a mark is right. The tier lines are about the way in, not the answers.)

### TSH-D5: the Counting Room (`S06_null`)

```
TSH-D5.01 KALDREN: (at the threshold; his next step makes no sound) "In."
TSH-D5.02 KALDREN: (holds out a glove; lets a pinch of grit go) "Watch."
      (the grit falls straight down into a small heap; no drift)
TSH-D5.03 KALDREN: "Now say something." (his own word comes out flat, like wool)
      {event: drop_grit and speak interactions active}
TSH-D5.04 (after both) KALDREN: "That's a quiet room. Dust falls straight. Your voice goes flat. Feet go missing."
TSH-D5.05 KALDREN: "Builders worked loud and counted quiet. That's all I know about why, and it's a guess."
  1. "What are the grooves on the bench?"   → TSH-D5.10
  2. "Where does the back passage go?"      → TSH-D5.20
  3. "You can call me by my name now?"      → TSH-D5.30
  4. "Back to the sketch."                  → TSH-D5.40

TSH-D5.10 KALDREN: "Counting. Theirs. I can't read it. Neither can you. Don't make anything up about it."   → options
TSH-D5.20 KALDREN: "Into one of theirs. If that one's quiet too, nobody hears you come."   → options
TSH-D5.30 KALDREN: "No. But I'll stop calling you walker. You've walked enough."   → options
TSH-D5.40 KALDREN: "Change your marks if you like. Paper's cheap. I'm not."
      {set TSH_NULL_TAUGHT; event: TSH-D5 end}
```

**Inspect: tally bench (W4)** "Grooves cut in the bench in rows, some long, some short. Counting. Nobody can read it."

### TSH-D6: the great hall (`S07`–`S08`) `[SPLINTER]`

```
TSH-D6.01 [SPLINTER] EYVIND: (on the dais, eyes closed, heel tapping) "Four, and —" (the note; the hall answers)
TSH-D6.02 {if TSH_MAP_TIER = good} [SPLINTER] EYVIND: (doesn't open his eyes) "Who's in the quiet? Somebody's breathing in the quiet."
TSH-D6.02 {if TSH_MAP_TIER = fair or poor} [SPLINTER] EYVIND: (opens his eyes; not afraid) "Hold them off the frame. Don't let anyone touch the frame."
TSH-D6.03 [SPLINTER] EYVIND: "Listen to it. Listen. That's the mountain saying it's right."
      {event: TSH-E3 begins}

(during TSH-E3, between pulses)
TSH-D6.10 [SPLINTER] EYVIND: "Again. Four, and —"
TSH-D6.11 [SPLINTER] EYVIND: "You can hear it in Stonewake on a still night. Did you know? I didn't, at first."
TSH-D6.12 [SPLINTER] EYVIND: (to a crewman cowering from a pulse) "Get up. No. Stay down, then. Keep your head under it."

(after TSH-E3; the player steps onto the dais)
TSH-D6.20 [SPLINTER] EYVIND: (still playing) "Don't. Not yet. It isn't finished."
      {event: take_horn channel active}
TSH-D6.21 (take_horn complete) [SPLINTER] EYVIND: (lets go at once; reaches after the mouthpiece) "Careful with that. That's brass on horn. I bent it myself."
TSH-D6.22 [SPLINTER] EYVIND: (sits on the dais step) "All right. All right." (beat) "Did you hear it, though?"
      {event: TSH-D6 end → S09; pulses switch to plate rhythm}
```

### TSH-B6: great-hall barks (TSH-E3, TSH-H1)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TSH-B6.1 | Pulse tell (first) | IVEN | "Snow lies behind the pillars. Get where the snow is." |
| TSH-B6.2 | Pulse tell | KALDREN (in a pillar's shadow) | "Here it comes. Count four." |
| TSH-B6.3 | Crew staggered by a pulse | SPEAR | "It doesn't care whose side —" |
| TSH-B6.4 | Crew belief | SPEAR | "The guardian's angry. You've made it angry." |
| TSH-B6.5 | Reply to TSH-B6.4 | KALDREN | "The hall's ringing. Halls don't get angry." |
| TSH-B6.6 | Hornman calls | HORNMAN | (a short, ugly call) "Up, up, all of you!" |
| TSH-B6.7 | Leverage only: extra spear | SPEAR (VI) | "Two of us in here, Leif! Told you it'd be worth the climb!" |
| TSH-B6.8 | Spear caught by a pulse | SPEAR | "Get it to stop." |
| TSH-B6.9 | Hornman engages | HORNMAN | "I only hum it for him. I only hum it." |
| TSH-B6.10 | Dust shapes rise (first time) | IVEN | "Dust, standing up." (beat) "It does that on the Crown stair. After." |
| TSH-B6.11 | Kaldren, if asked during the fight | KALDREN | "I don't fight. I hold the wall up. Somebody has to." |

### TSH-D7: it hasn't stopped (`S08` end)

```
TSH-D7.01 (the hum goes on; the next pulse rolls out without taps)
TSH-D7.02 KALDREN: (hand flat on the frame's foot) "He's stopped. It hasn't."
TSH-D7.03 KALDREN: "The plates are ringing each other. One's carrying the rest. Find it. Listen, don't knock."
TSH-D7.04 {if TSH_MARKS correct for II and V} KALDREN: "You've marked your quiet rooms. Put them in there."
TSH-D7.04 {else} KALDREN: (drops grit at each alcove mouth in turn; at two it falls straight) "Two. That one and that one. Put them in there."
TSH-D7.05 [SPLINTER] EYVIND: (from the step) "You'll never hear it. It took me a month to hear it."
      {event: TSH-D7 end; plate interactions active}
```

### TSH-D8: carrying the others (`S09_silence`)

**Plate listen results** (interaction log and subtitle):

| Id | Result | Text |
|---|---|---|
| TSH-B8.1 | Carrier | "Under the hum, this one is loudest. The others are riding on it." |
| TSH-B8.2 | Not carrier | "Thin. It's singing along with something else." |
| TSH-B8.3 | Masked (pulse tell building) | "Can't hear it under the hall. Wait." |
| TSH-B8.4 | Plate with Shatterfall grit (P2, P3, P4) inspect | "Grey grit in the grooves. The size of the Seat's empty slots." (`TES` Completed) |

**Ask Kaldren** (only for a plate the player has listened to):

```
TSH-D8.01 {if plate is carrier} KALDREN: (hand by its bolts) "That bolt's taking the load. That's your carrier."
TSH-D8.01 {if plate is not carrier} KALDREN: (hand by its bolts) "Bolt's slack. Not that one."
TSH-D8.02 {if plate not yet listened to} KALDREN: "Listen first. I'm not your ears."
```

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TSH-B8.5 | Unbolt started | KALDREN | "Between. Do it between." |
| TSH-B8.6 | Right plate set down | KALDREN | "Hum's dropped. Hear it? One less voice." |
| TSH-B8.7 | Wrong plate unbolted | KALDREN | "Not that one. Now they're all shouting. Carry it anyway." |
| TSH-B8.8 | Second wrong plate (`TSH_WRONG_PLATES` ≥ 2) | KALDREN | "You've got ears. Use the ones on your head." |
| TSH-B8.9 | Plate dropped by a pulse | IVEN | "Pick it up. It's only loud." |
| TSH-B8.10 | Plate set down in a quiet alcove | (log) | "The plate goes dead quiet in your hands. Dust over the floor falls straight." |
| TSH-B8.11 | Third plate damped | [SPLINTER] EYVIND | "Don't. That's the low one. That's the one that makes it sing." |
| TSH-B8.12 | Fourth plate damped | IVEN | "Pulses are slowing. Thirty, near enough." |
| TSH-B8.13 | Fifth plate lifted | KALDREN | "Last. Gently." |

### TSH-D9: the silence and the records (`S09` end, `S10_records`)

```
TSH-D9.01 (the last plate set down; total silence for one breath; the dust falls straight; sound returns)
TSH-D9.02 [SPLINTER] EYVIND: "Oh." (very quietly)
TSH-D9.03 IVEN: (after a while) "That's the first time I've heard the Summit say nothing."
      {event: trial record pickup active on the bench}

TSH-D9.10 (TSH_trial_record acquired; the player may read it)
TSH-D9.11 IVEN: (takes out his log) "Put it by mine."
      {event: side-by-side interaction}
TSH-D9.12 IVEN: (reading down both columns with a finger) "Third. Ninth. Eighteenth. Twenty-first. Twenty-fourth. Twenty-seventh."
TSH-D9.13 IVEN: "Fourteenth, I was on the Passwatch rota. Twenty-sixth was a storm. I can't swear to those."
TSH-D9.14 IVEN: "The rest." (beat) "Every one."
      {set TSH_RECORDS_SET}
  1. (To Kaldren) "What was it?"          → TSH-D9.30
  2. (To Kaldren) "Is it over?"           → TSH-D9.30
  3. [SPLINTER] "Talk to Eyvind."        → TSH-D10.01

TSH-D9.30 KALDREN: (hand on the frame; then off it) "Stresses settled. That's all I can tell you."
TSH-D9.31 KALDREN: (when pressed) "That's all I can tell you."   → options
```

### Document: `TSH_trial_record` (quest item) `[SPLINTER]`

A narrow bound book, oiled against damp, written in a neat craftsman's hand with drawings of plates in the margins. Dates are frost-count, as wardens and hornwrights count autumn.

> *[flyleaf]*
> WALL-HORN. Trials at the great hall. E. Stall, hornwright.
> For the Quartermaster.
>
> **3rd of frost.** Trial I. Two plates seated (the big Shatterfall pair). Note held a count of twenty, an hour past dusk. Hall rang. A hum after, faint, long. Promising.
>
> **9th of frost.** Trial II. Three plates. Note held thirty, second hour of night. Hall rang plain. Hum came up through the floor. Crows went off the face outside, all at once. Ha.
>
> **14th of frost.** Trial III. Three plates, one re-cut. Note held thirty, second hour. Hum. Dust came up off the floor around the round stone and stood a moment. Crew unhappy.
>
> **18th of frost.** Trial IV. Four plates, with the first from the Seat's own rack. Note held forty, second hour. Hum strong. Dust stood. A push of air from the floor knocked Leif down. He's fine.
>
> **21st of frost.** Trial V. Four plates. Note held forty, third hour. Hum strong. Pushes came in a rhythm, after each note. It answers. It is answering the horn.
>
> **24th of frost.** Trial VI. Five plates, all three from the Seat seated. Note held sixty, second hour. Hum from the whole mountain. The pushes are even. You could set a clock by them. This is the horn.
>
> **26th of frost.** Trial VII. Storm in the hall. Could not hear the horn's own answer over the weather. Wasted night.
>
> **27th of frost.** Trial VIII. Five plates, retuned. Note held from second hour to fourth, in turns. Snow came off the face outside in sheets. The Quartermaster should hear this. Emberholt will.
>
> *[last page, newest]* Trials nightly now until it holds without me. Then it goes to the passes.

### TSH-D10: Eyvind (`S10_records`) `[SPLINTER]`

```
TSH-D10.01 [SPLINTER] EYVIND: (on the dais step, hands loose) "You've no idea what that was. It was right. The mountain said it was right."
  1. "Who is it for?"                                         → TSH-D10.10
  2. "The hum came when you played. Every night. Look."        → TSH-D10.15
  3. "What were you going to do with it?"                      → TSH-D10.20
  4. {if TES Completed} "Three of those plates came off the Shatterfall seat."   → TSH-D10.30
  5. "You'll go down with the wardens."                        → TSH-D10.40

TSH-D10.10 [SPLINTER] EYVIND: "The Quartermaster. Ingrith. Ingrith Scarrow." (beat) "She counted every plate. She'd want me to say so."
TSH-D10.11 [SPLINTER] EYVIND: "She says if Thornfell won't sound the wall, she'll close it herself."
TSH-D10.12 [SPLINTER] EYVIND: "She will close the wall herself if she can't sound it. She meant it. She means everything."
      {set TSH_NAMED_QM}   → options

TSH-D10.15 [SPLINTER] EYVIND: (looks at the two books) "Yes. That's what I'm telling you. It answered." (he does not see it)   → options

TSH-D10.20 {if TH_STORES = leverage} [SPLINTER] EYVIND: "Blow it from the passes. Let the forges hear Thornfell's ready. The stores are full; she says we're nearly there."   → options
TSH-D10.20 {else} [SPLINTER] EYVIND: "Blow it from the passes. Let the forges hear Thornfell's ready. Then you lot took the stores, and she said the horn would have to do for both."   → options

TSH-D10.30 [SPLINTER] EYVIND: "The best three. They were already tuned. Somebody tuned them in the war and then nobody played them." (beat) "Waste."   → options

TSH-D10.40 [SPLINTER] EYVIND: "Fine. Let them carry the mouthpiece. Don't let them bend it."
      {event: TSH-D10 end → S11}
```

(TSH-D10.10–.12 is a non-combatant's testimony after he gives up, SX-N2. If TD-1 changes, swap only these lines, the flyleaf and the record's mentions of "the Quartermaster".)

### TSH-D11: the horn (`S11_choose`)

```
TSH-D11.01 KALDREN: (standing between the two quiet alcoves) "Now what. It's not mine to say. It's yours, apparently. Everyone keeps handing you things."
  1. "Leave them in the quiet. Will you keep them?"      → TSH-D11.10
  2. "Break them."                                       → TSH-D11.20
  3. "Wrap them for Ressa. Let the Assembly decide."     → TSH-D11.30
  4. "What would you do?"                                → TSH-D11.40

TSH-D11.40 KALDREN: "Sit on them till I die. Then somebody else would have to." (beat) "That's not advice. That's a complaint."   → options

TSH-D11.10 KALDREN: (chalks his mark on each alcove lip) "Kept. Asleep. I'll come up and look at them. My knees will tell me about it."
TSH-D11.11 IVEN: "Somebody will want them."
TSH-D11.12 KALDREN: "Somebody always does."
      {set TH_HORN = silenced}   → TSH-D12.01

TSH-D11.20 KALDREN: "In the quiet, if you're going to." (hands the player the crew's maul)
      {event: break interactions in II and V}
TSH-D11.21 (each strike: a plate cracks with no sound at all)
TSH-D11.22 [SPLINTER] EYVIND: (weeping, without any noise of his own) "Nobody will ever hear that again."
TSH-D11.23 KALDREN: "No. That's the idea." (beat; quieter) "I don't like it either."
      {set TH_HORN = broken}   → TSH-D12.01

TSH-D11.30 IVEN: "Sacking, then. Wardens can carry. Ressa won't thank us."
TSH-D11.31 KALDREN: "Keep them out of the open on the way down. Wrapped, in a sledge, nothing knocking. Tell her a quiet room at the Terrace."
      {event: wrap interactions ×2}
      {set TH_HORN = surrendered}   → TSH-D12.01
```

### TSH-D12: the Crown (`S12_crown`)

```
TSH-D12.01 IVEN: (on the summit top; blows Gather: three short, for the wardens) "They'll be up by dark. For him." {if surrendered} "And the sledge."
TSH-D12.02 IVEN: (turning the sketch over; drawing on the back) "You can see it all from here. Look."
TSH-D12.03 IVEN: "That ridge, down to the Stormwake road. That line above the old watchfires. That rim, to Carrick's ladders."
TSH-D12.04 IVEN: "Nobody walks them but me. You can, now. Mind the wind."
      {event: high routes unlocked}
  1. [SPLINTER] "Where's Ingrith?"           → TSH-D12.10
  2. "What will you write in your log?"       → TSH-D12.20
  3. "Let's go down."                         → TSH-D12.30

TSH-D12.10 IVEN [SPLINTER]: "Don't know. Somewhere with a gate." (looks at the sky over the pass) "Snow's coming early. If somebody wants to close a wall, it'll be in weather."   → options
TSH-D12.20 IVEN: "'Summit quiet. No storm. No hum.'" (beat) "First time in a month I'll write that."   → options
TSH-D12.30 IVEN: "Down's easier. Mostly."
      {event: TSH-D12 end → quest Completed; TF-M5 armed}
```

### TSH post-quest barks

| Id | Speaker | Line | Condition |
|---|---|---|---|
| TSH-B9.1 | KALDREN (Summit great hall) | "Still asleep. Good. Go away, you'll wake them." | `silenced` |
| TSH-B9.2 | KALDREN (Stonewright Quarter) | "Five plates in pieces. A month's work for him. A long time's for whoever made them." | `broken` |
| TSH-B9.3 | RESSA (Signal Terrace) | "Plates in a quiet room under my seal. The Assembly decides. I keep the horns anyway." | `surrendered` |
| TSH-B9.4 | BRYNJAR (Stonewake) | "Broken. The horn that split the ridge, in pieces on a floor." (pounds the table) "Good. I don't care. I care." | `broken` + `TH_BRYNJAR = disowned` |
| TSH-B9.5 | BRYNJAR (Stonewake) | "You broke Thornfell's horn. Ours. Readiness, in pieces. And now what do we sound from the passes?" | `broken` + `TH_BRYNJAR = defended` |
| TSH-B9.6 | BRYNJAR (Stonewake) | "The Summit's quiet, they say. I liked it better loud. That's a lie. I didn't." | `silenced` or `surrendered` |
| TSH-B9.7 | STONEWAKE TOWNSFOLK | "Couldn't sleep for the hum, half the autumn. Slept last night like a stone." | TSH Completed |
| TSH-B9.8 | WARDEN (Passwatch) | "Iven came down smiling. Iven doesn't smile. What did you do up there?" | TSH Completed |
| TSH-B9.9 | IVEN (high path, if met) | "Summit quiet. No storm. No hum. I write it every night now." | TSH Completed |
| TSH-B9.10 | WARDEN (holding Eyvind, Passwatch) | "Hornwright keeps asking if anyone heard it from Stonewake. Like he wants a review." `[SPLINTER]` | TSH Completed |

---

## Part 5: Review notes (dialogue file)

| Check | Result |
|---|---|
| Line length | Every conversation returns options or control within six NPC lines. Barks are one or two short sentences. |
| Canon anchors | **Dorn:** "Wind trick." never smiling; "I've never been down" (TES-D2.20), "I wasn't there" (TES-D6.10, TES-D8.10); neither carries nor keeps the roster (a Ridge Warden runner carries it in `kept`, TES-D9.32). **Maera:** decides (TES-D9.01); "both honest"; does not reconcile; "The stones know how to listen" as custom, not testimony. **Torvek:** one sentence, no war claim. **Kaldren:** no origins (TSH-D5.05 "a guess"; TSH-D5.10); Summit account limited to "Stresses settled. That's all I can tell you." (TSH-D9.30); canon line in TSH-D2.20. **Iven:** reports first; "Mountains get tired. Not like this." **Brynjar:** barks only; no membership, no casualty. **Ressa:** "I keep the horns anyway." |
| Evidence rule | No line says who the echo-figures are. The miner belief ("The dead are up") and crew belief ("the guardian's angry") are answered and never confirmed. Ingrith is named only by Eyvind (a non-combatant) after he gives up and on the record's flyleaf. |
| Withheld | The roster's duty margin has rotted (no hornbearer name). Maera's leaf shows seven names and "continued"; cairn row runs past the path; no total anywhere. |
| Dates | Trial record: 3, 9, 14, 18, 21, 24, 26, 27 of frost. Iven's no-storm hums: 3, 9, 18, 21, 24, 27; 14th = rota gap; 26th = listed with storms. Hours match (an hour past dusk; second hour; third hour; second to fourth). |
| Roster vs. list | Roster: "4th hr, late. Split." List: "last seen... at the fifth hour". Shown side by side; not reconciled. |
| Splinter tags | Chit initials; TES-D1.10; TES-L-GERRIT.20; Seat slot addition; TSH-B4.12; TSH-D6; TSH-D7.05; TSH-B8.11; TSH-D9.02; trial record; TSH-D10; TSH-D11.22; TSH-B9.10. Bersi is not named in Act II. |
| Flags | Set here: `TES_CHITS_READ`, `TES_JAM_MINED`, `TES_JAM_CREW`, `TES_PAIR_ONE`, `TES_PAIR_TWO`, `TES_SEAT_SOUNDED`, `TES_STRATA_READ`, `TES_CAIRNS_READ`, `TES_RECORDS_SET`, `TES_NAMESLIP_SEEN`, `TES_THIRD_HORN_HEARD`, `TH_SHATTERFALL_ACCOUNT`, `TSH_MAP_TIER`, `TSH_NULL_TAUGHT`, `TSH_RECORDS_SET`, `TSH_NAMED_QM`, `TH_HORN`. Matches quest-file tables. |
| Address | "Walker" for strangers; Kaldren stops using it after the Counting Room; Maera after the climb. No name, gender, title or origin for the player. |
| Magic | Nobody calls anything magic. "Wind trick", "the hall's ringing", "a quiet room", "only air". |
| No route, no Remnant | No line says how grain or plates moved beyond "hauled up the stair". No Remnant presence. Emberholt appears only as the splinter's fear ("Emberholt will"; "let the forges hear"), never caricatured. |
| Independent review (2026-11-03) | `TES-D9.32` runner carries the kept roster, new `TES-D9.33`; slip and list name Sig Brede; frost-count coexistence note; `[SPLINTER]` on `TSH-B3.5`, `TSH-D9` option 3, `TSH-D12` option 1, `TSH-D12.10`. |
| Director rulings reconciliation (2026-11-03) | CDR-1: crew yield barks retriggered as engage/pulse barks (`TSH-B3.4`, `TSH-B3.5`, `TSH-B6.8`, `TSH-B6.9`; ids kept); Iven's tying direction (`TSH-B3.6`) and "the crew" in `TSH-D12.01` removed; `TSH-D6.12` no longer addresses a yielded crewman. Eyvind (SX-N2) unchanged. |
