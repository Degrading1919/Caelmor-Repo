# Thornfell Main Act III: Cast and Dialogue (Stonewake)

**Status:** Authored production content for Creative Director milestone review. This is the companion to `04_CONTENT_PRODUCTION/Quests/Caelmor_Thornfell_Main_Act_III.md`, which owns step ids, flags and mechanics. Characters marked **[CANON ANCHOR]** come from `LORE/Characters/Caelmor_Characters_Region2_Thornfell_Anchors (Not Full List).txt`; their lines are authored here, and nothing gives them a new age, wartime service, battle, kinship, travel, meeting or record custody (Part 4 ledger). Characters marked **[NEW]** are authored and are not canon until promoted. Every node that names Ingrith Scarrow is tagged `[SPLINTER]` (bible §3.1). Nothing here is production JSON.

**Voice rules:** Thornfell bible §5.3 is binding: understated speech (a long speech is fear or anger); nobody calls anything magic; weather is grammar; the player is "walker" to strangers and is called by name only by a host who has added them to a shelter tally; dry humour at one's own expense; Emberholt distrusted rationally, never caricatured. Lines are short: at most two sentences per named-character line, at most six NPC lines before a choice or control returns. **One exception, by design:** the reading of the rubbing (`TSW-D9.40`–`.62`) runs one line per roster date without options, because the reading is the scene.

**Node format** (Lowmark dialogue files): `NODE SPEAKER: "Line." (stage note)`, `> [condition] "Option." → NEXT {effect}`. Ids: `TSW-D<n>.<nn>` dialogue, `TSW-B<n>.<n>` barks, `TSW-L-` optional leads, `TSW-I` inspect texts, Documents D-1 to D-3. `{PLAYER}` is the player's name, used only where a node says so.

---

## Part 1: Act III voice additions

| Item | Status | Use |
|---|---|---|
| **"Climb to the horns."** | [NEW] Warden instruction in a whiteout. | Ressa, wardens. |
| **"The first one's the horn. The second one's the mountain."** | [NEW] Echo rule of thumb (direct call before its echo). | Iven, Dorn; Aud's TF-M1 line if that package uses it. |
| **"By the board."** | [NEW] Quartermaster's phrase: do it in the drilled order. | Ingrith, her crews. |
| **The tag** | [NEW] The short pattern after Close that names a gallery. | Dorn, Ingrith, crews. |
| **Spent / live** | [NEW] Gallery that has dropped / that can still drop. | Everyone at the Gatefall. |
| **The long winter** | [NEW] What Thornfell calls the final year's hunger winter. "The hunger winter" is what people say when they are angry. | Ingrith ("the long winter"), Runa, Brynjar. |
| **"Where will you stand?"** | [CANON trait] Hadrik's only question in any Assembly. | Hadrik. |
| **"Outside."** | [NEW] The word on the new slates. | Vessa, Ressa, epilogue. |

**What nobody in TF-M5 says:** that the hunger winter was Thornfell's doing; where the turned-back relief came from; that anyone on the roster died; that the Assembly Hall's carrying spot is anything but "a good spot"; that the gallery calls are anything but drill.

---

## Part 2: Cast notes

### Hadrik Stonewake, Assembly Speaker [CANON ANCHOR]
- **Canon:** a buffer, not a ruler; calm, patient; carries war scars he never speaks of; lets arguments burn out; knows the hall carries some voices; chooses where people stand; never asks why.
- **In TF-M5:** places everyone; asks the player one question; puts the reader on the carrying spot; repeats what the hall decided.
- **Knows:** the hall is afraid; Hushfold has always stood at the door; on TF-M2's public route, the ledger totals he read aloud (totals only). **Doesn't know:** the roster (until it is read); the stores' line detail (never the children's-ration line).
- **Voice:** few words, often a hand on an elbow instead. Calls the player "walker" unless Hushfold has tallied them, and then still "walker" (he is not their host). Never says "I decide".
- **Canon guard:** his scars get one stage note (his hand closes on the speaking stone during the reading) and no date, battle or story.

### Ressa Highcrag, High Ridge Warden [CANON ANCHOR]
- **In TF-M5:** sounds the Gather, posts the wardens, writes the first closure-account entry.
- **Knows:** which calls are refused. The gallery calls are not on her refusal list, because nobody thought they'd be blown again. **Doesn't know:** the roster.
- **Voice:** orders without heat. Counts people, not feelings. "Climb to the horns."
- **Guard:** no named roster custody. She writes a new account; the old roster stays in the wall.

### Dorn Feldhorn, Veteran Hornbearer [CANON ANCHOR]
- **In TF-M5:** the last horn post; reads the gallery calls with the player; blows Fall and Rest; blows Answer to the stragglers if the player has not restored the Third Horn; lowers his horn if they have.
- **Knows:** call shapes; the Third Horn's half-remembered meaning. **Doesn't know:** the gallery calls by use, only by shape.
- **Voice:** ritual seriousness, private fear; "wind tricks" never with a smile.

### Iven Ridgeborne, high-path scout [CANON ANCHOR]
- **In TF-M5:** horn post W3. Reports direction, weather and timing, then stops.
- **Voice:** quiet; describes before he interprets; does not interpret tonight.

### Maera Cairnwatch, Cairn-Keeper [CANON ANCHOR]
- **In TF-M5:** stands at the cairn bench or near the stone; reads the rubbing if Runa does not.
- **Voice:** gentle, unyielding. Reads names as names: no "lost", no "dead". Her authority over the dead shows in what she will not say.

### Brynjar Korr, Blood-Oath voice [CANON ANCHOR]
- **In TF-M5:** Assembly only. Not in the splinter; did not know (TD-1, TD-2). Ingrith is of his clan's households, so her tribunal is his clan's duty.
- **Voice:** loud, pounds the stone table. The one thing he says quietly is about Hushfold's children.

### Elira Hearthward, Hearthguard voice [CANON ANCHOR]
- **In TF-M5:** Assembly. Practical about sacks and children. Argues with Brynjar and defends him.

### Old Torvek, Voice of the Old Stone [CANON ANCHOR]
- **In TF-M5:** Assembly. One sentence. Does not move when the hall moves.

### Kaldren Deepdelver [CANON ANCHOR]
- **In TF-M5:** at the back wall only if `TH_HORN = silenced`. One line, about stresses.

### Vessa Galt, Ridge Warden sergeant [NEW]
- **In TF-M5:** outside with her patrol all night; in at dawn with any stragglers. Looks at the wall.
- **Voice:** short sentences, dry; follows the rule and dislikes that it is the rule. TF-M1: "We write what we closed. Not who."

### Runa Weatherall, Hushfold shelter host [NEW]
- **In TF-M5:** brings the column through; reads the first tally book as her people come in; may read the rubbing.
- **Knows:** "we came over in the thaw". **Doesn't know (until tonight):** that her grandmother's name is cut into the Gatefall. She does not find out at the gate: the player has read the wall, she has not. She hears it in the hall (or reads it herself).
- **Voice:** warm, tired, proud; "we" for the whole shelter line. Uses `{PLAYER}` if the player is on a Hushfold tally (TSM Completed or TME01 tally-add).

### Ingrith Scarrow, the Quartermaster [NEW] `[SPLINTER]`
- **Who:** former pass quartermaster; eight years old in the final year's long winter; leads the Iron Winter.
- **Want:** a reserve no one can starve. **Fear:** the long winter again.
- **Knows:** everything she counted. **Doesn't know:** the roster; that the relief that might have fed her winter was turned back at this gate.
- **Voice:** counts aloud. Numbers instead of adjectives. Kind to children, merciless with numbers. Never threatens the column. When she runs out of numbers she stops talking.
- **Not a monster:** she believes it. She is wrong about Emberholt and right that winters kill.

### Minor cast [NEW]
| Name | Role | Voice |
|---|---|---|
| **Kolli** | Hushfold herd-lad, about fourteen; came down with the count. | Proud of the count, scared of the slab. |
| **Oddny** | Hushfold herder, young woman; went back for a strayed nanny goat. | Furious at the goat. |
| **Halvard** | Old Hushfold herder; went after Oddny; turned ankle. | Slow, polite, mortified. |
| **Young warden** (W1) | The one Ressa stopped in TF-M1. | Over-careful. |
| **Hornman** | Ingrith's call-man on the gatehouse roof. | Says nothing but calls until he yields. |
| **Wedge crews** | Blood-Oath households and clanless hires. | Tired, cold, half sure. |

---

## Part 3: TF-M5 Stonewake (`TSW`), the night

### TSW-B0: the Gather (offer)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TSW-B0.1 | Blizzard event start (Windscar) | (horns, tower after tower) | Gather. Gather. Gather. (three-dot glyph, toward the nearest tower) |
| TSW-B0.2 | Same, Passwatch | PASSWATCH WARDEN | "That's Ressa's Gather. All towers. Three Calls, walker. Now." |
| TSW-B0.3 | Same, Stonewake (Signal Terrace) | WARDEN RUNNER | "Three Calls. Ressa's asking for you by name of walker." |
| TSW-B0.4 | Climbing Windscar to C1 | HAULIER (sheltering) | "Snow's come a month early. Snow's never polite." |

### TSW-D1: Ressa at Three Calls (S00)

```
TSW-D1.01 RESSA: (at the horn map, chalk in hand; doesn't turn round) "Iven saw crews on the Gatefall before the high path shut. They're dropping galleries."
TSW-D1.02 RESSA: "Hushfold's column is past the far gate with the herds. Vessa's patrol went over to bring them two days back."
TSW-D1.03 KOLLI: (by the brazier, wrapped to the eyes) "Thirty-one. And the herd. I counted twice."
TSW-D1.04 RESSA: "Wardens are posted up the track. Climb to the horns. Don't climb to anything else."
  > "Who's on the gate?"                                  → TSW-D1.10
  > [no TF-M1 practice horn; fallback] "I've nothing to answer with."   → TSW-D1.20
  > "What are they eating up there?"                      → TSW-D1.30
  > [TH_HORN known] "Is it the horn?"                     → TSW-D1.40
  > "Going."                                              → TSW-D1.50

TSW-D1.10 RESSA [SPLINTER]: "Iven says the Quartermaster. Scarrow." (beat) "She counted my wardens' boots once. Every pair."   → TSW-D1 options

TSW-D1.20 RESSA: (unhooks a horn from the map peg; hands it over) "Warden's horn. Cow horn and brass. Answer when you're answered."   {set TSW_HORN_LOANED; grant horn}  → TSW-D1 options

TSW-D1.30 [TH_STORES = leverage] RESSA: "Whatever they've been carrying up that track while we watched. Well, then."
TSW-D1.30 [TH_STORES = seized]   RESSA: "Not much. Elira carried their grain down. Hungry crews walk home or get stubborn."
TSW-D1.30 [TH_STORES = reported] RESSA: "What they took before the seal. Enough for a few nights."   → TSW-D1 options

TSW-D1.40 [TH_HORN = silenced]    RESSA: "No. Kaldren has it asleep in a hole. This is rope and pins. Old work."
TSW-D1.40 [TH_HORN = broken]      RESSA: "No horn left to blow. So she's using the other thing the war left us."
TSW-D1.40 [TH_HORN = surrendered] RESSA: "I've got her plates under a tarp. This isn't that. This is rope and pins."   → TSW-D1 options

TSW-D1.50 RESSA: "Gather means come. Fall means get your back to stone. Rest means you can stop being frightened."
TSW-D1.51 RESSA: "Go on."   {event: TSW-D1 end → S01 active}
```

**Inspect: horn map** "Calls cut in the back wall, tower to tower, with lines between." / with `TH_THIRD_HORN`: "Someone's chalked the Third Horn back onto the map. Recently. Small, neat chalk."
**Inspect: brazier** "Wardens' boots steaming in a ring round it. Everyone's feet are wet. Nobody mentions it."

### TSW-B1: the whiteout (S01)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TSW-B1.0 | `TH_CALLS` false fallback, foot of the stair | YOUNG WARDEN (W1) | "Three short: come to me. Short-long-short: rock, get to the wall. That's all you need tonight." |
| TSW-B1.1 | Leaving C1 into the white | (log) | "White. The rail's at your hand and nothing past it." |
| TSW-B1.2 | Player walks into a rope | (log) | "Rope. Wrong side." |
| TSW-B1.3 | Reaching W1 | YOUNG WARDEN | "You came to the horn. Good. Most people come to the horn." (beat) "Next one's up. Listen for her." |
| TSW-B1.4 | First whistle (C3) | W2 WARDEN (distant) | "Face is singing! Get in a hole!" |
| TSW-B1.5 | First Fall at C3 | (horn) | Fall. (dot-bar-dot glyph) |
| TSW-B1.6 | Player ignored Fall and was knocked down | W2 WARDEN | "That was the mountain telling you. It doesn't tell twice." |
| TSW-B1.6a | Same, second time | W2 WARDEN (the other) | "We'll carve your name on the niche. 'Here stood one who knew better.'" |
| TSW-B1.7 | Assist: 45 s without progress | (horn, doubled) | Gather. Gather. (glyph pinned) |
| TSW-B1.8 | Reaching W2 | W2 WARDEN | "Rest." (blows it) "Means us too. Go on, Iven's next. He'll be quiet about it." |
| TSW-B1.9 | At C4, both glyphs shown | IVEN (from W3, a call between Gathers) | "First one's the horn. Second one's the mountain." |
| TSW-B1.10 | Player walks toward the echo, reaches the drovers' rope | (log) | "Rope across an old path. The call's behind you, and it's louder." |
| TSW-B1.11 | Player blows Answer, 1 beat | (log) | "One beat. The face is at your shoulder." |
| TSW-B1.12 | Player blows Answer, 2 beats | (log) | "Two beats. You've come off the wall a little." |
| TSW-B1.13 | Player blows Answer, 3+ or none | (log) | "Three beats, then nothing. Open air that way." |
| TSW-B1.14 | Reaching W4 / out of the white | DORN | "There you are. You walked out of it like a goat. That's a compliment." |

### TSW-D2: Iven at W3 (S01)

```
TSW-D2.01 IVEN: (a horn ring on the ledge; snow to his knees) "Galleries were calling before the snow came. The old way. From the gatehouse roof."
TSW-D2.02 IVEN: "Wind's out of the far side. It'll sit in the cut, so you'll see down there. Not up here."
TSW-D2.03 IVEN: "Something's in the rocks below me. It's been quiet. Quiet's worse."
  > "What's the old way?"      → TSW-D2.10
  > "Going down."               → TSW-D2.20
TSW-D2.10 IVEN: "Close, and then a short bit after. I don't know them. Dorn might." → TSW-D2 options
TSW-D2.20 IVEN: "Listen for the howl. It comes before the teeth."   {event: TSW-D2 end; TSW-E1 zone active}
```

### TSW-B2: wolves and the apron (TSW-E1; S02 start)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TSW-B2.0 | Howler howls | (caption) | "A howl, left." / "A howl, right." / "A howl, behind." |
| TSW-B2.0a | Wolves flee | IVEN (above) | "They're hungry, not stupid. Neither are you. Go on." |
| TSW-B2.1 | First view of the galleries with `TDS10_SEEN` ([NEW] placeholder; Batch 3 package fixes the name) | (log) | "Three pale. Same as from below." |
| TSW-B2.2 | First view without it | (log) | "Seven galleries over the cut. Most of the props are grey. Three are new wood, pale as bread." |

### TSW-D3: Dorn at the near apron (S02)

```
TSW-D3.01 DORN: (at the post; listening up at the gatehouse) "Hear that? Close, then the tag. That's a gallery call. I've never heard one blown."
TSW-D3.02 DORN: "Every gallery has its own tag. It's cut on its stone, under the Close."
TSW-D3.03 DORN: "He calls one. You find the stone with that tag. If someone up there answers, they're ready to pull."
  > "And if nobody answers?"                 → TSW-D3.10
  > "Which ones can still fall?"             → TSW-D3.20
  > "Why are they blowing it at all?"        → TSW-D3.25
  > "Going up."                               → TSW-D3.40
TSW-D3.10 DORN: "Then there's nobody there. Or nothing to pull." → TSW-D3 options
TSW-D3.20 DORN: "Grey props held stone once. The stone's in the cut now, under the snow. Pale props are holding something." → TSW-D3 options
TSW-D3.25 DORN: "Crews pull on their own call. That's drill. You don't drop a mountain on a nod." → TSW-D3 options
TSW-D3.30 DORN: (bark, first time the player inspects a spent gallery during a call) "Grey. Nothing behind it. Let him call."
TSW-D3.40 DORN: "Pull-line's the weak bit. Rope always is." (beat) "Don't tell Aud I said that."   {event: TSW-D3 end}
```

### Inspect texts: the Gatefall (S02)

| Object | Text | Condition |
|---|---|---|
| Marker G1 | "Two falling bars, then one short dot. Grey props above, black with age. Behind them, nothing but the gallery's back wall." | — |
| Marker G2 | "Falling bars, two dots. Grey props. An old heap below, snow on it like a blanket on a sleeper." | — |
| Marker G3 | "Falling bars, one long bar. The props above are new: pale wood, axe marks still sharp. A pull-line runs down from the pin-beam." | tick if `TDS10_SEEN` |
| Marker G4 | "Falling bars, dot and bar. Grey props, one cracked through. It isn't holding anything up but itself." | — |
| Marker G5 | "Falling bars, bar and dot. Pale props. The pins are new iron, oiled." | tick if `TDS10_SEEN` |
| Marker G6 | "Falling bars, two bars. Grey. The gallery's stone is in the cut below, where it fell in the war." | — |
| Marker G7 | "Falling bars, two bars and a dot. Pale props right over the gatehouse. The pins have been drawn halfway." | tick if `TDS10_SEEN` |
| Grey prop on the cut floor | "A prop from a spent gallery, fallen years back. The wood's gone grey and soft as felt." | — |
| War heap with axle | "Stone heaped in the cut, and in it a wagon axle, frozen in. Whatever it carried got the other side of the gate. Or didn't." | — |
| Pull-line | "New rope, hemp, tarred." / with `TH_STORES` ≠ seized: "The coil end's stamped 'W.'" | — |
| Pin-beam (from the ledge) | "Iron pins through the beam, each holding a prop's foot. Pull the line and the beam turns and the pins come out together." | — |

### TSW-B3: gallery crews (S02) `[SPLINTER]` where noted

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TSW-B3.1 | First call heard (from the roof) | INGRITH `[SPLINTER]` (faint, between calls) | "By the board. One gallery. Then the next." |
| TSW-B3.2 | Live crew answers | (horn, from the gallery) | Answer. (two dots) |
| TSW-B3.3 | Spent call, no answer, count passes | (log) | "No answer from that gallery. The call moves on." |
| TSW-B3.4 | Crew sees the player (G3/G5) | WEDGE CREWMAN | "Someone on the stair! Pull, pull before the gust!" |
| TSW-B3.5 | Whistle stops the haul | WEDGE CREWMAN | "Hold! Face is singing. Hold the line." |
| TSW-B3.6 | Crewman yields | WEDGE CREWMAN | "Down. I'm down. It's a wall, not a war." |
| TSW-B3.7 | Hornman (crew) yields | CREW HORNMAN | "Horn's on the ground. Look. On the ground." |
| TSW-B3.8 | Line cut | WEDGE CREWMAN | (the line goes slack and slithers down) "...Well. That's that." (sits on the ledge) |
| TSW-B3.9 | Seized: G3 crewman, after yield | WEDGE CREWMAN | "Half of them walked. No grain, no wall." |
| TSW-B3.10 | Leverage: G5 crew sighted | WEDGE CREWMAN | "New iron! Show them the new iron!" |
| TSW-B3.11 | G7 called; answer from the roof; first shed | DORN (from below) | Fall. (then, shouting) "That's the Gate gallery! Get in the gatehouse!" |
| TSW-B3.12 | Rubbing complete; wind eases | DORN (outside the door) | Rest. |

### TSW-I: the warden room (S03)

| Object | Text | Condition |
|---|---|---|
| The room | "Six bedrolls, a cookpot, the fire built up hard against the inner wall. Somebody's lived here three nights and kept it roaring." | Entry |
| The wall (before wipe) | "The plaster's come off in plates where the heat got at it. Under it, soot. In the soot, lines too straight to be cracks." | — |
| Panel 1 (after wipe) | "Cut letters under the soot. A date, then names beneath it. Then another date." (shows Document D-1, panel 1) | Required |
| Panel 2 (after wipe) | "More dates. The final year. Beside some of them, not names: a short line, the same each time." (shows D-1, panel 2) | Required |
| Panel 3 (after wipe) | "The last dates. The last line is cut shallower than the rest, as if the hand was tired." (shows D-1, panel 3) {set `TSW_ROSTER_READ`} | Required |
| Count sheets (desk) | "A stack of sheets in a neat hand: grain by the measure, iron by the bar, boots by the pair. The backs are blank." | — |
| Charcoal (hearth) | "Charcoal from the edge of the fire. It'll do." (carry) | — |
| Drill board | "The galleries in order, one glyph to a line. Someone's added a new line at the bottom in fresh chalk: G7 — Q." | Optional |
| Slate shelf | "A shelf for slates. No slates. Whatever the gate-warden wrote on, it wasn't kept." | Optional |
| Bedrolls | "Six bedrolls. One has a child's mitten tucked into the blanket fold. Nobody here is a child." | Optional |
| Wall (after rubbing) | "The names are there whether anyone reads them or not. Now someone has." | — |
| Weatherall (no special inspect) | — | The name is never highlighted. |

---

## Part 4: Documents

### Document D-1: The closure roster (cut in the gatehouse wall) [NEW]

Dates are relative war-year labels (architecture B.1 rule). The hand is one hand throughout, unpractised at first, steadier by panel 2, tired by panel 3. Nobody ordered it (TD-10). It says who was outside, never who died.

**Panel 1**

> LATE WAR. AUTUMN OF THE FIRST CLOSING. SLAB DOWN AT THE CLOSE.
> Outside: the Tofte carters, five. Unn Tarvald and her mother. A tinker, would not give his name. Two herd boys of no steading, brothers.
>
> LATE WAR. SAME WINTER. FIRST DEEP SNOW. SLAB DOWN.
> Outside: Ragna Lunde, Arvid Lunde, their three. Wounded with two carriers, number not known. One carrier was called Ebbe.
>
> LATE WAR. SECOND CLOSING AUTUMN. SLAB DOWN AT DUSK.
> Outside: Folke Arnesson. The Ostvik widow and her son. Hild, a weaver. Seven drovers, names not given.

**Panel 2**

> FINAL YEAR. BEFORE THE SNOW. SLAB DOWN AT THE CLOSE.
> Outside: Toril Ness and Gunnar Ness. Old Sverre, a shepherd. A family from the far shielings, five. Would not give a name. The man was angry.
>
> FINAL YEAR. FIRST DEEP SNOW. SLAB DOWN.
> Outside: Astrid Weatherall and two small. Bodil Kask. Eirik, the smith's boy, sent over for iron.
>
> FINAL YEAR. THE LONG WINTER. MIDWINTER.
> Relief train turned back.
>
> FINAL YEAR. THE LONG WINTER. AFTER MIDWINTER.
> Outside: a woman and a child at the far apron at first light. Names not given.
> Relief train turned back.
>
> FINAL YEAR. THE LONG WINTER. HUNGER MONTH.
> Relief train turned back. The second this month.

**Panel 3**

> FINAL YEAR. THAW. SLAB UP AT REST.
> In: some. The gate does not cut those.
>
> AFTER THE WAR. FIRST AUTUMN. SLAB DOWN FOR THE LAST TIME.
> Outside: not known. Snow too thick to count.

(Ten dated entries, four turn-back lines. "Weatherall" and "Kask" match the first tally book, Document D-3. The roster never says where the relief trains came from or who turned them back beyond "the gate" by implication. MAP and history: no route stated.)

### Document D-2: `TSW_closure_rubbing` (quest item) [NEW]

**Item name:** Rubbing of the Gatefall wall.
**Inspect text:** "Charcoal on the back of a quartermaster's count sheet. Three panels of cut letters, black where they were rubbed: dates, names, and four times the same short line. Through the paper, faint and backwards, run the Quartermaster's figures: grain by the measure, iron by the bar."
**Read:** shows Document D-1 in full.
**Fate:** read aloud once in the Assembly; returned to the player ("The wall has the cut one. Keep that."). Kept to the convergence (CV-M3 chip seed, bible §8.2). Not droppable, not sellable.

### Document D-3: Hushfold's first tally book, the first page (read aloud by Runa) [NEW]

Runa keeps the book. It is never handed to the player and is not an item. She reads the first page as the column passes (`TSW-D6`).

> THE TALLY OF THE SHELTER LINE AT THE FOLD.
> Kept from the long winter, the final year.
>
> Beds: eleven, and the floor.
> Food: the common pot, and what we bring.
> Expected: whoever comes.
>
> Aasen, Liv and her sister. Fed. The bench by the fire.
> Hollin, Ivar, with no steading now. Fed. Works the wood.
> A man who will not say his name. Fed. He mends.
> The long winter. Two of us gone to Stonewake for bread. Came back with none.
> Thaw after the long winter. Kask, Bodil. Came over in the thaw, alone. Fed.
> Thaw after the long winter. Weatherall, Astrid, and two small. Came over in the thaw. Fed from the common pot. Given the end bench.
> Still unaccounted for: everybody's somebody.

("Two of us gone to Stonewake for bread. Came back with none" is the shelter line's own record of the long winter's hunger inside the wall. Nobody comments on it.)

---

## Part 3 (continued): the winch, the column, the stragglers, dawn

### TSW-D4: Ingrith at the winch (S04) `[SPLINTER]`

She finishes her count before she speaks. Three lines, then the fight.

```
TSW-D4.01 INGRITH [SPLINTER]: (hand on the drum brake; lips moving) "...forty-one, forty-two." (looks up) "Forty-two measures of slab left to drop, walker. I counted."
TSW-D4.02 INGRITH [SPLINTER]: "One winter shut, and the Iron Winter's the only reserve in the Marches. Then they'll listen."
TSW-D4.03 [TH_HORN = silenced]    INGRITH [SPLINTER]: "Kaldren has my horn asleep in a hole. So. The wall, then."
TSW-D4.03 [TH_HORN = broken]      INGRITH [SPLINTER]: "You broke my horn. Good. Now there's only the wall."
TSW-D4.03 [TH_HORN = surrendered] INGRITH [SPLINTER]: "Ressa has my plates. She keeps everything she refuses."
  > "There are people outside that gate."           → TSW-D4.10
  > (Draw.)                                          → TSW-D4.20
TSW-D4.10 INGRITH [SPLINTER]: "Thirty-one and a herd. I can count." (lifts the spear) "One."   → TSW-E4 starts
TSW-D4.20 INGRITH [SPLINTER]: "One."   → TSW-E4 starts
```

### TSW-B4: boss barks (TSW-E4) `[SPLINTER]`

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TSW-B4.1 | The Count (P1–P2) | INGRITH `[SPLINTER]` | "One." "Two." "Three." |
| TSW-B4.2 | Short Measure | INGRITH `[SPLINTER]` | "Short." |
| TSW-B4.3 | The Close (hornman) | INGRITH `[SPLINTER]` | "Close it." (hornman: Close; the drum slips; the slab drops a notch) |
| TSW-B4.4 | Player dodges the slab drop | INGRITH `[SPLINTER]` | "Quick. Quick's not enough in winter." |
| TSW-B4.5 | Gust; she steps behind the post | INGRITH `[SPLINTER]` | "Face is singing. Mind your feet." (she means it) |
| TSW-B4.6 | 60%: transition | INGRITH `[SPLINTER]` | "Gather." (hornman: Gather) |
| TSW-B4.7 | Crew arrive | IRON WINTER SPEAR | "Quartermaster! Stairs are clear, we're up!" |
| TSW-B4.8 | Crewman yields | IRON WINTER SPEAR | "I'm sitting. Quartermaster, I'm sitting." |
| TSW-B4.9 | Leverage crew (new spearheads) | INGRITH `[SPLINTER]` | "New iron. Forty bars of it. Don't waste it on the floor." |
| TSW-B4.10 | First G7 shed in the fight | INGRITH `[SPLINTER]` | "That's mine. I drew those pins." (beat) "Hood. Get under the hood, you fool." (to her own crewman) |
| TSW-B4.11 | 35%: she drops the tally cords | (no voice: the cords clatter on the boards) | — |
| TSW-B4.12 | P3 (silent) | (no voice: her steps; she mouths the numbers) | — |
| TSW-B4.13 | Player hit by the Count three times in a row | INGRITH `[SPLINTER]` (P1–P2 only) | "You're not counting." |
| TSW-B4.14 | Player death | INGRITH `[SPLINTER]` | "Get them down the stair. Gently. Gently, I said." |

### TSW-D5: the yield (S04) `[SPLINTER]`

She plants the spear butt-down and sits on the drum frame. The hornman puts his horn on the boards. Any option can end the scene (exit counts as end).

```
TSW-D5.01 INGRITH [SPLINTER]: (sitting; breath smoking; not looking at the player) "Down. I'm down."
TSW-D5.02 INGRITH [SPLINTER]: "How many small ones in the column?"
  > "I don't know. Runa will."                                     → TSW-D5.10
  > "They're out there in this. Why?"                              → TSW-D5.11
  > [TSW_G3 = cut or TSW_G5 = cut] "Your lines are cut."            → TSW-D5.12
  > [TSW_ROSTER_READ] "Have you read the wall downstairs?"          → TSW-D5.20
  > (Leave her to the wardens.)                                     → TSW-D5.40

TSW-D5.10 INGRITH [SPLINTER]: "Nine, last tally. Unless they've had more." (beat) "Somebody should count them in."   → TSW-D5 options

TSW-D5.11 INGRITH [SPLINTER]: "Far hut's an hour past the apron. They'd have sheltered." (beat) "They're clanless. They know the cold."   → TSW-D5 options

TSW-D5.12 INGRITH [SPLINTER]: "Cut my lines. Rope's dear." (beat) "Everything's dear. That's the whole point."   → TSW-D5 options

TSW-D5.20 INGRITH [SPLINTER]: "What wall."   {set TSW_INGRITH_WALL}
  > "The warden room. Under the soot. Names, and dates."          → TSW-D5.21
TSW-D5.21 INGRITH [SPLINTER]: "I lit that fire for the crew. Three nights." (beat) "I didn't read the wall. I was counting."
  > "Final year. The long winter. 'Relief train turned back.'"    → TSW-D5.22
  > "Nothing. Never mind."                                         → TSW-D5 options
TSW-D5.22 INGRITH [SPLINTER]: "The long winter." (stops) "I was eight. We boiled harness."
TSW-D5.23 INGRITH [SPLINTER]: "Turned back by who."
  > "By the gate."                                                 → TSW-D5.24
  > (Say nothing.)                                                 → TSW-D5.24
TSW-D5.24 INGRITH [SPLINTER]: (a long breath; then, under it) "One. Two. Three. Four..." (she goes on counting, and does not look up)   → TSW-D5.40

TSW-D5.40 DORN [SPLINTER]: (up the stair with two wardens) "Ingrith." (beat) "Come on down. Fire's still lit, I'm told."
TSW-D5.41 INGRITH [SPLINTER]: (getting up; handing her spear to a warden butt-first) "Keep the pawl. It's under the boards. Somebody'll want it."   {event: TSW-D5 end → S05 active}
```

(TSW-D5.11 is the bible's sentence. No node answers it. TSW-D5.22–.24 is the quiet contradiction: nobody tells her what it means, and she does not say she understands. The pawl line is her one useful act; it gives Kolli the idea of the wedge.)

### TSW-B5: winding the slab (S05)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TSW-B5.1 | First segment starts | DORN (from below) | "Wind it! Short pulls. Stop when the stone sings." |
| TSW-B5.2 | Segment interrupted by gust | (log) | "The gust took the bar out of your hands. The slab's where you left it." |
| TSW-B5.3 | Segment 1 complete | KOLLI (on the apron below, to someone) | "It's going up! It's going up!" |
| TSW-B5.4 | G7 shed during winding | DORN | Fall. (then) "Hood!" |
| TSW-B5.5 | Segment 2 complete; lanterns visible in the gap | (log) | "Lanterns, low, on the far apron. Then legs. Then people." |
| TSW-B5.6 | Segment 3 complete | DORN | "Pawl! Who's got a pawl?" |
| TSW-B5.7 | Kolli jams the wedge | KOLLI | "Gallery wedge! It's the wrong size but it's wood!" |
| TSW-B5.8 | Hold begins | DORN | "Lean on it. Wedge holds while you hold. Runa won't send them under a stone nobody's holding." |

### TSW-D6: Runa's tally at the gate (S06; second custodian, required)

Plays while the player holds the bar. Runa stands in the gate below the open winch floor, the book on her arm, touching each shoulder as it passes. Her lines carry up through the floor. The player cannot answer while holding; releasing the bar pauses the column and Runa (she waits, then picks up the next line). Full page text: Document D-3.

```
TSW-D6.01 RUNA: (first sledge through; she looks up at the winch floor) "Who's on the bar?" (beat) [tallied] "{PLAYER}. Good. Hold it."
TSW-D6.01 [else] RUNA: (looks up) "Walker on the bar. Hold it, walker."
TSW-D6.02 RUNA: "First snow, so we read the tally. First snow, and the whole line's through one gate. So it's the first book."
TSW-D6.03 RUNA: (opens it; doesn't look at it) "The tally of the shelter line at the Fold. Kept from the long winter, the final year."
TSW-D6.04 RUNA: "Beds: eleven, and the floor. Food: the common pot, and what we bring. Expected: whoever comes."
TSW-D6.05 RUNA: (a shoulder; another) "Aasen, Liv and her sister. Fed. The bench by the fire." (to a woman passing) "That's your gran, Liv. Mind the slab."
TSW-D6.06 RUNA: "Hollin, Ivar, with no steading now. Fed. Works the wood." (the herd comes through; she shouts over it) "Mind the brown one, she's a biter!"
TSW-D6.07 RUNA: "A man who will not say his name. Fed. He mends." (beat) "We still don't know. He mended everything."
TSW-D6.08 RUNA: "The long winter. Two of us gone to Stonewake for bread. Came back with none."
TSW-D6.09 RUNA: "Thaw after the long winter. Kask, Bodil. Came over in the thaw, alone. Fed."
TSW-D6.10 RUNA: (she looks down at the page for this one) "Thaw after the long winter. Weatherall, Astrid, and two small. Came over in the thaw."
TSW-D6.11 RUNA: "Fed from the common pot. Given the end bench." (beat) "That's us. That's my gran. We still sit at the end."
      {log line (requires TSW_ROSTER_READ, always set): "Weatherall. The wall downstairs has that name, the winter before."}
TSW-D6.12 RUNA: "Still unaccounted for: everybody's somebody." (closes the book)
TSW-D6.20 RUNA: (last sledge under; counting on her fingers; then again) "Twenty-nine." (beat) "Twenty-nine. Thirty-one went out."
TSW-D6.21 HUSHFOLD WOMAN: "Oddny went back for the brown nanny. Halvard went after Oddny."
TSW-D6.22 RUNA: (shouting up) "Two out, Dorn!"   {event: TSW-D6 end → S06 complete → S07 active}
```

**Inspect: the tally book** (if the player releases the bar and looks down): "A small book, the cover worn white at the corners where hands hold it. Runa isn't letting go of it."

### TSW-D7: Lost (S07)

```
TSW-D7.00 (from beyond the far apron, faint, from two directions) Lost. ... Lost. (rising-line glyphs, two, dim)

TSW-D7.01 [not TH_THIRD_HORN] DORN: (on the far apron; wedges set) "I'll answer. You walk." (blows Answer) "They'll keep calling. Go to the call."

TSW-D7.02 [TH_THIRD_HORN] DORN: (horn half raised; he sees the player lift theirs; lowers his) "Go on. It's yours."
      {player blows the Third Horn: Answer + one long rising}
TSW-D7.03 [TH_THIRD_HORN] (inside the gate, Hushfold stops moving. People turn round.)
TSW-D7.04 [TH_THIRD_HORN] RUNA: (in the gate) "...What's that one?"
TSW-D7.05 [TH_THIRD_HORN] DORN: "Heard. Someone's still out." (beat) "Means the gate stays open. Means we're still looking."
TSW-D7.06 [TH_THIRD_HORN] (far off: Answer. A moment later, from the other side: Answer.)
TSW-D7.07 [TH_THIRD_HORN] DORN: "They'll answer you now. Every time. Go on."
      {stragglers now answer the player's calls}
```

**Oddny (nearer)**

```
TSW-D7.10 ODDNY: (under a boulder with three goats; snow to the shoulders) "Don't. Don't say anything. She's a biter and she's an idiot and I'm an idiot."
TSW-D7.11 ODDNY: "Halvard came after me. He's further out. He's slower than the goat."
  > "Take the rope."                        → TSW-D7.12
TSW-D7.12 ODDNY: (takes the rope line; ties the nanny to her belt) "If she bites you, she likes you."   {carry: rope line; tow Oddny}
TSW-D7.13 ODDNY: (at the gate) "Runa's going to say something. Runa always says something."   {set TSW_ODDNY = player}
```

**Halvard (further, toward the far hut)**

```
TSW-D7.20 HALVARD: (sitting on the track, very upright) "Good evening. I've turned my ankle. I'm sorry about the whole business."
TSW-D7.21 HALVARD: "I thought I'd make the far hut. The far hut thought otherwise."
  > "Take the rope."                        → TSW-D7.22
TSW-D7.22 HALVARD: "Slowly, then. I'm old and the mountain's in no hurry."   {carry: rope line; tow Halvard}
TSW-D7.23 HALVARD: (at the gate, to Runa) "Twenty-nine and me." (beat) "And Oddny, I suppose. And the goat. Thirty-one and a goat."   {set TSW_HALVARD = player}
```

**Leave it to the patrol (at the gate, any time after the reply)**

```
TSW-D7.30 DORN: "Vessa's out there. Far hut's on her road." (beat) "Your call. They'll be cold either way."
  > [both not yet in] "Leave it to the patrol."           → TSW-D7.31
  > "I'll go out."                                         → (ends; search continues)
TSW-D7.31 RUNA: (a long look past the slab into the white) "Then the gate stays open."
TSW-D7.32 DORN: "Gate stays open." (to the wardens) "Two on it all night. Brazier. Blow Lost on the hour."
      {any straggler not in: TSW_<name> = patrol; TH_COLUMN = patrol_brought; S07 complete}

TSW-D7.40 [both in] RUNA: (counts; again) "Thirty-one." (beat) "Thirty-one and a goat with no sense."
TSW-D7.41 [both in] RUNA: [tallied] "Thank you, {PLAYER}." [else] "Thank you, walker. You're on the tally, if you want it."
      {TH_COLUMN = player_brought; S07 complete; tally-add if not already}
```

### TSW-B7: the search (barks)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TSW-B7.1 | Leaving the far apron | (log) | "White again. Two calls, far apart." |
| TSW-B7.2 | Echo off Oddny's boulder, 1 beat | (log) | "One beat. Something big and close. A goat complains about it." |
| TSW-B7.3 | Towing in a gust | ODDNY / HALVARD | "Face is singing!" / "I hear it. I'm stopping. I'm very good at stopping." |
| TSW-B7.4 | Player returns with one only | DORN | "One in. One out." (beat) "Your call." |

### TSW-D8: dawn (S08)

```
TSW-D8.00 (Keep watch at the warden-room hearth: two steps. Hushfold asleep on the floor and in the passage. The wall in firelight. Grey light. The wind drops. Dorn blows Rest from the apron.)
TSW-D8.01 VESSA: (through the gate with her patrol, white to the eyebrows) "Patrol in. Six of us. All feet."
TSW-D8.02 [any straggler = patrol] VESSA: "Found two at the far hut." (beat) "They knew the cold." (beat) "Half a night of knowing it. They'll keep their toes."
TSW-D8.02 [both = player] VESSA: "Far hut was empty. Somebody'd been by and taken the people out of the weather. Tidy."
TSW-D8.03 VESSA: (sees the wall over the sleepers; stops; reads for a long time)
  > [TPW_NAMES_ASKED] "You told me you write what you closed. Not who."   → TSW-D8.10
  > "Somebody wrote who."                                                  → TSW-D8.11
  > (Let her read.)                                                         → TSW-D8.20
TSW-D8.10 VESSA: "I did say that." (beat) "Somebody didn't listen to me before I was born."   → TSW-D8.20
TSW-D8.11 VESSA: "Somebody always does. Nobody reads it."   → TSW-D8.20
TSW-D8.20 RESSA: (up from below with wardens; she looks at the slab, the wedges, the wall, in that order) "Slab stays up. Wedged. Two on it."
TSW-D8.21 RESSA: "Nobody seals anything till the Assembly sits." (to the wardens taking Ingrith out) "Walk her down. Walk, I said. She's not luggage." [SPLINTER]
TSW-D8.30 RESSA: "Assembly sits tomorrow. Bring the paper."   {event: TSW-D8 end → S09 active}
```

---

## Part 5: The Assembly (S09–S12)

### TSW-B9: entering the hall (placement presentation)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TSW-B9.1 | Hall entered | (log) | "The hall's full and nobody is sitting. A broad man in a plain coat is walking between them, a hand on an elbow here, a nod there." |
| TSW-B9.2 | Hadrik places Hushfold near (`TH_HUSHFOLD_VOICE`) | HADRIK | "Runa. Here. By the stone." |
| TSW-B9.2a | Hushfold at the door (else) | (log) | "Hushfold stands along the door wall. Nobody has told them to. Nobody has told them not to." |
| TSW-B9.3 | Ketil at Hushfold's shoulder (`sledge`) | KETIL | "The highstead eats. I said I'd stand where I owe." |
| TSW-B9.4 | Nettlehook with Hushfold (`TH_HIGHSTEADS_TOGETHER`) | TOVA | "We tied the ribbon. So we stand here. That's what a ribbon's for." |
| TSW-B9.5 | Brynjar's table turned (`disowned`) | BRYNJAR | (to Hadrik, loud) "Turn it, then. I'll look at them. I've nothing to hide from children." |
| TSW-B9.5a | Brynjar's back to the door (`defended`) | BRYNJAR | "Readiness isn't a crime, Hadrik. It's a coat." |
| TSW-B9.6 | Torvek at the stone with the folded banner (`shared`) | TORVEK | (nothing; he sets one hand on the banner) |
| TSW-B9.7 | Kaldren at the back wall (`silenced`) | KALDREN | "Hall's sound. Floor's sound. I came to check." |
| TSW-B9.8 | Yielded gallery crew at the door | WEDGE CREWMAN | "They let us stand at the back. I wasn't expecting the back." |
| TSW-B9.9 | Wardens at the rail (any `cut`) | WARDEN | "Re-pinning cut galleries in snow. Lovely work. Thank you." |
| TSW-B9.10 | TAS Completed | TESSALY VARN (back wall) | "We were told it would be quick. Nothing in Thornfell is quick. It's admirable." |
| TSW-B9.11 | Ingrith at the side door `[SPLINTER]` | (log) | "At the side door a woman in a quilted coat stands between two wardens, counting the people in the hall under her breath." |

### TSW-D9: Hadrik and the hall

```
TSW-D9.01 HADRIK: (to the player, last; quietly) "Walker." (beat) "You came down from the gate. Ressa says you held it."
TSW-D9.02 HADRIK: "I put people where they stand. That's all I do here. Everyone else decides."
TSW-D9.03 [LM_CIVIC_STANDING] ELIRA: (passing) "They say the Vale wrote its river plan at one long table. We do it standing. Our feet are tougher."
TSW-D9.10 HADRIK: "Where will you stand?"
      {S09 complete; four standing places active}
```

**At the chosen place (S10)**

```
TSW-D9.20 [hushfold] RUNA: [tallied] "{PLAYER}. Here. You're on the tally, you stand with the tally." [else] "Here, walker. Door's draughty. We're used to it."   {TH_STAND = hushfold}
TSW-D9.21 [wardens]  RESSA: "Rail's for people who'll be out in it." (beat) "You were. Stand."   {TH_STAND = wardens}
TSW-D9.22 [cairn]    MAERA: "Stand by me, then. The names don't mind company."   {TH_STAND = cairn}
TSW-D9.23 [brynjar]  BRYNJAR: (pounds the table, once) "Good! Somebody who's been up there." (quieter) "Did they get the little ones through?"
  > "All of them."     → TSW-D9.24
TSW-D9.24 [brynjar] BRYNJAR: "Good." (he looks across at Hushfold and does not say anything else)   {TH_STAND = brynjar}
```

**The reader (S11 start)**

```
TSW-D9.30 HADRIK: "There's a paper. Ressa says it's off a wall." (holds out a hand to the player)
      {player hands over TSW_closure_rubbing}
TSW-D9.31 [reader = runa]  HADRIK: "Runa. Read it." (he walks her a step off the stone, to a place on the floor that looks like any other) "Here. Good spot."
TSW-D9.31 [reader = maera] HADRIK: "Maera. Read it." (he walks her a step off the stone) "Here. Good spot."
TSW-D9.32 [reader = maera, TH_SHATTERFALL_ACCOUNT = kept] MAERA: "I'll read names. I've read worse places than this."
      {set TSW_READER}
```

**The reading (TSW-D9.40–.62).** One line per entry; no options; the hall carries the reader's voice to every wall. The reader reads exactly what is cut (Document D-1). Stage notes vary by reader.

```
TSW-D9.40 READER: "It's cut in the Gatefall gatehouse. Warden room. Under the plaster." (beat) "Dates, and who was outside."
TSW-D9.41 READER: "Late war. Autumn of the first closing. Slab down at the Close. Outside: the Tofte carters, five. Unn Tarvald and her mother. A tinker, would not give his name. Two herd boys of no steading, brothers."
TSW-D9.42 READER: "Late war. Same winter. First deep snow. Slab down. Outside: Ragna Lunde, Arvid Lunde, their three. Wounded with two carriers, number not known. One carrier was called Ebbe."
TSW-D9.43 READER: "Late war. Second closing autumn. Slab down at dusk. Outside: Folke Arnesson. The Ostvik widow and her son. Hild, a weaver. Seven drovers, names not given."
TSW-D9.44 READER: "Final year. Before the snow. Slab down at the Close. Outside: Toril Ness and Gunnar Ness. Old Sverre, a shepherd. A family from the far shielings, five. Would not give a name. The man was angry."
TSW-D9.45 [reader = runa]  RUNA: "Final year. First deep snow. Slab down. Outside: Astrid Weatherall and two small." (she stops; the hall waits; she goes on in the same voice) "Bodil Kask. Eirik, the smith's boy, sent over for iron."
TSW-D9.45 [reader = maera] MAERA: "Final year. First deep snow. Slab down. Outside: Astrid Weatherall and two small. Bodil Kask. Eirik, the smith's boy, sent over for iron." (at the door wall, Runa puts a hand over her mouth)
TSW-D9.46 READER: "Final year. The long winter. Midwinter. Relief train turned back."
TSW-D9.47 READER: "Final year. The long winter. After midwinter. Outside: a woman and a child at the far apron at first light. Names not given. Relief train turned back."
TSW-D9.48 READER: "Final year. The long winter. Hunger month. Relief train turned back. The second this month."
      (Hadrik's hand closes on the edge of the speaking stone. He says nothing.)
TSW-D9.49 READER: "Final year. Thaw. Slab up at Rest. In: some. The gate does not cut those."
TSW-D9.50 READER: "After the war. First autumn. Slab down for the last time. Outside: not known. Snow too thick to count."
TSW-D9.51 [TWN Completed] MAERA: (from her place, quietly) "That's two walls this autumn kept names nobody read."
TSW-D9.62 READER: (lowering the paper) "That's all of it."
      (silence; the hall does not echo it)
```

**The hall stands where it means it**

```
TSW-D9.63 HADRIK: (one step back from the stone) "Stand where you mean it."
      {compute TH_ASSEMBLY_POSTURE (quest file §9.3); play the movement for that posture}
```

**Clan voices (one line each; posture variants)**

| Id | Speaker | open | watchful | sealed_with_terms |
|---|---|---|---|---|
| TSW-D9.64 | BRYNJAR | (after a long moment, one step) "I'd die for any child in this hall. That's all of them, then. Fine." | "We keep the towers manned. And we answer when there's an answer owed." | "Shut means safe. Shut with names means we know who to carry bread to. My clan carries it." |
| TSW-D9.65 | ELIRA | "Count it out. Every sack. Into the granaries where people can see it." | "Keep it under account. If anyone adds a measure, the hall hears about it." | "Then the reserve feeds the rope first. Before readiness. Before anything." |
| TSW-D9.66 | TORVEK | "The wind remembers vows. Remember this one." | "Stone holds. Keep the stone." | "A wall holds. Write who it holds off." |
| TSW-D9.67 | RESSA | "Open at thaw, by many hands. Every closing called aloud." | "The Wardens keep the slates. Anyone may ask. I'll answer." | "I'll write every name outside and run rope to them weekly. That's the terms." |
| TSW-D9.68 | RUNA | [tallied] "We'll stand nearer next time, {PLAYER}." [else] "We'll stand nearer next time." | "We'll ask. We're good at asking." | "Our three shieling houses winter out by choice. Write them down. Feed them." |
| TSW-D9.69 [TH_HORN] | (one line by value, any posture) | silenced: KALDREN "Plates are asleep. Stresses settled. That's all." / broken: BRYNJAR "My clan's boast is in bits on the Summit floor. Good. I'll find another." / surrendered: RESSA "Her plates are under my tarp. Nobody blows them." | | |
| TSW-D9.69a [TH_STORES] | ELIRA (any posture) | reported: "The seal holds till we cut it, and we'll cut it in daylight." / seized: "We already carried it down. Hushfold ate it. Write that in your account too." / leverage: "We let it fill so we could watch it. It filled. Now it's ours to count." | | |

**Ingrith `[SPLINTER]`** (one line)

```
TSW-D9.70 [TSW_INGRITH_WALL] INGRITH [SPLINTER]: (from the side door) "Turned back." (beat) "I counted everything else."
TSW-D9.70 [else]             INGRITH [SPLINTER]: (from the side door; she had been counting the hall; she has stopped) "...Turned back."
```

**Hadrik repeats the hall's word (S12)**

```
TSW-D9.80 [open]              HADRIK: "The hall says: the far gate shuts at deep snow, the way it does. At thaw it opens by many hands. Every closing is called aloud."
TSW-D9.80 [watchful]          HADRIK: "The hall says: the Wardens close and open, as they do. The reserve stays in store under the hall's account. Every closing is written."
TSW-D9.80 [sealed_with_terms] HADRIK: "The hall says: the passes shut now, till thaw. With a rope to everyone outside, and their names written."
TSW-D9.81 HADRIK: "I'm only the one who says it back. That's all a speaker does."
TSW-D9.82 HADRIK [SPLINTER]: "Ingrith Scarrow goes to her clan's tribunal. The hall will be watching." 
TSW-D9.83 [disowned] BRYNJAR [SPLINTER]: "She's ours. We'll sit on it at thaw. I won't spare her and I won't shame her."
TSW-D9.83 [defended] BRYNJAR [SPLINTER]: "She's ours. We'll sit. She was ready when the rest of you were asleep." (beat; quieter) "She shouldn't have shut it on children."
TSW-D9.84 HADRIK: "And from today, a closing names who's outside. Every gate. Every time."
TSW-D9.85 RESSA: (a new slate; chalk) "First one, then." (writes as she speaks)
TSW-D9.86 [open]              RESSA: "Gatefall. Open till deep snow. Outside: none we know of. Called on the Terrace." (hands the chalk to Runa)
TSW-D9.86 [watchful]          RESSA: "Gatefall. Up, wedged, two on it. Outside: none we know of." (keeps the chalk; hands the slate to Vessa)
TSW-D9.86 [sealed_with_terms] RESSA: "Gatefall. Down this week. Outside: the Aasen shieling, the Hollin shieling, the far hut. Fed Mondays." (hands the chalk to Vessa)
TSW-D9.87 VESSA: "Outside." (beat) "Well. I've written stranger."
TSW-D9.90 HADRIK: (giving the rubbing back to the player) "The wall has the cut one. Keep that."
TSW-D9.91 [TSW_HORN_LOANED] RESSA: "Keep the horn, too. You know how to answer with it."
TSW-D9.92 HADRIK: (to the hall, not loudly) "Go home. It's snowing."
      {TH_STANDING = true; event: TSW-D9 end → quest Completed}
```

### TSW-B10: after the hall (barks, Stonewake)

| Id | Speaker | Line | Condition |
|---|---|---|---|
| TSW-B10.1 | HUSHFOLD ELDER | "Stood near the stone. My knees are shaking. Must be the cold." | `TH_HUSHFOLD_VOICE` or open |
| TSW-B10.2 `[SPLINTER]` | KOLLI | "I counted the hall. Two hundred and six. Ingrith counted it too. She got two hundred and seven. She counted herself." | — |
| TSW-B10.3 | HALVARD | "They let me stand at the front with a stick. I felt like a councillor." | `TSW_HALVARD = player` |
| TSW-B10.4 | BLOOD-OATH HOUSEHOLDER | "Stood at the door, didn't you. With the door folk." (cool) | `TH_STAND = hushfold` |
| TSW-B10.5 | HEARTHGUARD STOREKEEPER | "Stood with the table. Well. Somebody has to keep him company." (cool) | `TH_STAND = brynjar` |
| TSW-B10.6 | ODDNY | "The nanny's fine. Thank you for asking. Nobody asks." | `TSW_ODDNY = player` |
| TSW-B10.7 | MARKET TRADER | "Hall stood still a long time. Never seen it stand still." | — |

### TSW-L-INGRITH: the cold room (optional, post-quest) `[SPLINTER]`

Ingrith is held in the hall's cold room until her clan's tribunal sits at thaw. One visit; repeat visits get TSW-L-INGRITH.20.

```
TSW-L-INGRITH.01 INGRITH [SPLINTER]: (sitting; marks scratched on the wall in fives) "Eleven days. They feed me better than the crews ate."
TSW-L-INGRITH.02 INGRITH [SPLINTER]: "How many came through?"
  > [TH_COLUMN = player_brought] "Thirty-one. And a goat."          → TSW-L-INGRITH.10
  > [TH_COLUMN = patrol_brought] "Twenty-nine, then two at dawn."   → TSW-L-INGRITH.11
TSW-L-INGRITH.10 INGRITH [SPLINTER]: "Thirty-one." (she scratches it on the wall) "Good."   → TSW-L-INGRITH.12
TSW-L-INGRITH.11 INGRITH [SPLINTER]: "At the far hut." (beat) "I said they would." (beat) "I wish I'd been wrong out loud."   → TSW-L-INGRITH.12
TSW-L-INGRITH.12 [TSW_INGRITH_WALL] INGRITH [SPLINTER]: "I've been counting the long winter. From the other side of the gate. It doesn't come out."
TSW-L-INGRITH.12 [else] INGRITH [SPLINTER]: "Somebody read the wall to me. I'm still counting it."
TSW-L-INGRITH.20 INGRITH [SPLINTER]: (doesn't look up) "Still counting."
```

---

## Part 6: Epilogue barks (by place and state)

All per-player; keyed on the quest file §E tables.

| Id | Place | Speaker | Line | Condition |
|---|---|---|---|---|
| TSW-B11.1 | Passwatch gate | VESSA | "Two slates now. Twice the chalk." | open |
| TSW-B11.2 | Passwatch gate | VESSA | "People ask who's outside. I tell them. That's new." | watchful |
| TSW-B11.3 | Passwatch gate | VESSA | "I write them every week. Every week they're still there." | sealed_with_terms |
| TSW-B11.4 | Passwatch horn post | DORN | "Teaching the small ones Answer. They blow it at everything. Goats. Doors." | open |
| TSW-B11.5 | Passwatch horn post | DORN | "Lost, at dusk. Then I wait. The far hut answers. Every night so far." | sealed_with_terms |
| TSW-B11.6 | Passwatch horn post | DORN | (with `TH_THIRD_HORN`) "I hear it in my sleep now. The good one." | any |
| TSW-B12.1 | Hushfold | RUNA | [tallied] "{PLAYER}. Your bench is the end one. It's the best one. Don't tell anyone." | any |
| TSW-B12.2 | Hushfold | RUNA | "We still have to ask. We ask louder now." | watchful |
| TSW-B12.3 | Hushfold | RUNA | "Three houses out at the shielings. Fed Mondays. I count the sacks myself." | sealed_with_terms |
| TSW-B12.4 | Hushfold | RUNA | "Gran's name is on a wall and in a book. She'd have hated the fuss." | `TSW_READER = runa` |
| TSW-B12.5 | Hushfold | RUNA | "Maera read Gran's name. I couldn't have. I'm glad it was her voice." | `TSW_READER = maera` |
| TSW-B12.6 | Hushfold | HALVARD | "The far hut is a terrible hut. I've written to the Wardens about it." | `TSW_HALVARD = patrol` |
| TSW-B13.1 | Stonewake hall | HADRIK | "Hushfold's mark's on the floor by the stone now. Somebody chalked it. I didn't ask who." | `TH_HUSHFOLD_VOICE` |
| TSW-B13.2 | Stonewake hall | HADRIK | "Hall's quiet. I like it quiet. Means it's thinking." | any |
| TSW-B13.3 | Stonewake market | BRYNJAR | "My clan's carrying the rope run Mondays. Don't thank me. Thank the rope." | sealed_with_terms, `TH_STAND = brynjar` |
| TSW-B13.4 | Stonewake market | ELIRA | "Sacks counted out where people can see. You'd be amazed how honest a sack gets in daylight." | open |
| TSW-B13.5 | Signal Terrace | WARDEN CRIER | "Close at the Gatefall. Outside: none we know of. Ask at Passwatch." | open, after `TSW_THAW` false |
| TSW-B14.1 | Nettlehook | KETIL | "Granary's full. I don't trust it. I'm counting it every day." | open |
| TSW-B14.2 | Nettlehook | KETIL | "Rope goes out Mondays. I check the rope Sundays." | sealed_with_terms |
| TSW-B14.3 | Nettlehook | TOVA | "Who's outside this winter?" (beat) "I asked a warden. She told me. Nobody ever told me before." | watchful |
| TSW-B15.1 | Gatefall | GATE WARDEN | "Pins strapped. Nobody's dropping anything off this cut again. Not on a call. Not on a whim." | any |
| TSW-B15.2 | Gatefall wall | (inspect) | "The names, clean of soot. A bench in front of them. Someone has left a stormflower on the ledge under 'Weatherall'." | any |
| TSW-B15.3 | Gatefall wall | (inspect) | "The new slate hangs beside the old names. This winter's are in chalk." | sealed_with_terms |
| TSW-B15.4 | Gatefall drill board | (inspect) | "The child's mitten, pinned to the peg. Nobody has claimed it." | any |
| TSW-B16.1 | Whinstone Store gate | (inspect) | "Chalked on the gate: what went where, sack by sack." | reported or leverage, open |
| TSW-B16.2 | Whinstone Store, grain gallery | (inspect) | "The stencilled relief sacks, set apart, stencils facing out. Chalk: 'Not ours. Kept till asked.'" | any (not seized) |
| TSW-B16.3 | Whinstone track shelter | HAULIER | "Used to be a war hoard. Now it's where I sleep. Better use." | seized |
| TSW-B17.1 | Thaw, Gatefall (open) | RESSA | "Outside this winter: none we know of. Every closing called." (then) "Take a turn on the bar, walker." | `TSW_THAW`, open |
| TSW-B17.2 | Thaw, Gatefall (watchful) | VESSA | (reads the slate to the wardens; wipes it) "Nobody outside. Wipe it. Write it again in autumn." | `TSW_THAW`, watchful |
| TSW-B17.3 | Thaw, Gatefall (sealed) | RESSA | (names each winterer as they walk in behind the relief sledge) "Aasen. Hollin. The far hut. In." | `TSW_THAW`, sealed_with_terms |
| TSW-B17.4 | Thaw, Stonewake | WARDEN | "Tribunal's sitting this week. Blood-Oath. Nobody's saying anything." | `TSW_THAW` |

---

## Part 7: Thornfell master commission offer lines (first meeting with `TH_STANDING`)

The offer opens a commission; it grants nothing (quest file §E.8).

| Giver | Line | Variant |
|---|---|---|
| **Aud Hammerlee** (bridgewright's fittings) | "You held a slab on a wedge the wrong size. Come and make fittings the right size. I'll swear at you the whole time." | *The Bridge That Chose* Completed: "...and bring your triage board, I miss it." / `leverage` + open: "Assembly gave me iron. Splinter iron. It doesn't know." |
| **Stonewake bowyer** (stormwood war-bow) | "Wind's tested a stave for you. It's been waiting. So have I." | *Stormwood* Completed: "The one you picked on the Burned Slope. I kept it." |
| **Ressa Highcrag** (Ridge Warden's horn and harness) | "Cow horn and brass. Nothing in it but breath. You'll make your own, and you'll answer with it." | `TSW_HORN_LOANED`: "Start from the one I gave you." |
| **Runa Weatherall** (far-side coat) | [tallied] "{PLAYER}. Far-side coat. We make them for people who go out for other people." [else] "Far-side coat, walker. For people who go out." | *Goat Year* Completed: "From your herd. They're very proud." |

---

## Part 8: Review notes (dialogue file)

| Check | Result |
|---|---|
| Line length and the six-line rule | Every conversation returns options or control within six NPC lines, except the rubbing reading (`TSW-D9.40`–`.62`, by design) and Runa's tally (`TSW-D6`, played during a hold, not a conversation). |
| Voice (§5.3) | Nobody calls anything magic. The carrying spot is "a good spot". Weather as grammar ("face is singing", "the mountain's in no hurry"). Dry humour at one's own expense (Halvard, Oddny, Aud). Emberholt is named only in Ingrith's belief (bible) and nowhere caricatured. |
| Address | "Walker" for the player except by a host who tallied them (Runa, Hushfold), via `{PLAYER}`. Hadrik never uses the name. |
| Canon anchors | Hadrik: places, repeats, asks one question; scars only as a stage note (hand on the stone). Brynjar: not in the splinter; his lines are about children and his clan's duty. Maera: reads names, assigns no deaths. Ressa: writes a new account; no roster custody. Dorn: calls; no proof from echoes. Iven: direction, weather, timing. Kaldren: stresses only. |
| Evidence rule | The roster and tally book carry the revelation. Ingrith's lines are testimony with no proof weight; the turn-back contradiction is never stated by anyone. No echo, gust or call identifies anyone. |
| Splinter tags | `TSW-D1.10`, `TSW-B3.1`, `TSW-D4`, `TSW-B4`, `TSW-D5`, `TSW-D8.21`, `TSW-B9.11`, `TSW-D9.70`, `TSW-D9.82`–`.83`, `TSW-L-INGRITH`. |
| No route for relief | The roster says "relief train turned back" only; no origin, no direction. The Whinstone sacks are "not ours, kept till asked". |
| Flags | Every flag set here (`TSW_HORN_LOANED`, `TSW_INGRITH_WALL`, `TSW_ROSTER_READ`, `TSW_ODDNY`, `TSW_HALVARD`, `TSW_READER`, `TH_COLUMN`, `TH_STAND`, `TH_ASSEMBLY_POSTURE`, `TH_STANDING`) matches the quest file's §9.2. |
| Names | Roster and tally names avoid Ketil/Tova's family name (Rask) and every named cast member except Weatherall. "Aasen" and "Hollin" appear in the tally and in the sealed-posture account (the same Hushfold households). |
| Independent review (2026-11-03) | Roster names de-collided (Astrid Weatherall, the Lunde family, the Tofte carters); `TSW-D1.20` option is the no-practice-horn fallback; Hadrik cast note limited to ledger totals; `TDS10_SEEN` marked placeholder; `[SPLINTER]` on `TSW-D5.40`, `TSW-B10.2`. |
