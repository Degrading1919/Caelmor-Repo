# Lowmark Main Act III — Cast Notes and Dialogue (MQ10–MQ12)

**Status:** Authored production content for Creative Director milestone review. Companion to `04_CONTENT_PRODUCTION/Quests/Caelmor_Lowmark_Main_Act_III.md`, which owns step ids, flags, chips and mechanics. **[CANON ANCHOR]** characters come from `LORE/Characters/Caelmore_Characters_Region1_Lowmark_Anchors (Not Full List).txt`; their lines here are authored. **[NEW]** characters are authored in the bible or The True Line. Nodes naming Edda Marrick or Gideon Sallow are tagged `[ANTAGONIST]`. Nothing here is production JSON.

**Binding:** The True Line cast file, Part 1 (voice rules), applies in full: plain nouns of work, understatement, dry humor, at most two sentences per named-character line, at most six NPC lines before a choice or control returns, address-neutral player options.

---

## Part 1 — Act III voice addenda

- **The act gets quieter as it gets bigger.** The siege is barked; the hearing is clipped; the vigil is mostly calls across water; MQ12 is said in short lines with long pauses. Nobody makes a speech, including the player.
- **Nobody explains the fen.** Sedge describes what to do; Ansel describes where; Oriel describes work. No one says what the Muster "is."
- **Marrick never names anyone.** She says "the Keeper-Captain," "my factor," "the young person with the drawings," "the households." She is the only character who never uses a name. Writers must keep this rule.
- **The plan's language** is "aye," "named," "the roll," "tenders." Never "council," "office," "authority," "government."
- **"Done"** is Lessa's word. Others borrow it in Act III, and she notices.

### Format

```
NODE  SPEAKER: "Line."                       (stage note)
  > [condition] "Player option."  → NEXT     {effect}
```

Conditions use flags from the quest file §0.2–0.5 and each quest's flag table. Options already used are hidden unless marked *(repeatable)*.

---

## Part 2 — Cast notes (Act III roles)

### Edda Marrick — Provisioner, House Marrick [NEW] `[ANTAGONIST]`
- **Act III function:** the face of the present wrong; answers every chip.
- **Want:** her house remembered as the one that kept Lowmark fed. **Fear:** being remembered as a profiteer.
- **Knows:** the whole scheme; that the fire was "arranged" (she never says by whom). **Doesn't know:** the Braids, the stones, the fen. She thinks drift is superstition.
- **Believes:** she *did* feed people, and in the war her house did more than anyone thanked it for. Some of that is true. That is what makes her dangerous.
- **Voice:** warm, unhurried, generous with other people's time. Never raises her voice. Never names anyone. Compliments before she disagrees. Treats every accusation as a misunderstanding she is happy to clear up.
- **Arc in Act III:** she loses gracefully, and that is the sting. Her last act in the hall is to ask the clerk to record that she attended. In MQ12 she asks the player how they will tell it.
- **Guardrail:** no cackling, threats or confession speech. She never says "I did it." She says what she thinks she did instead.

### Gideon Sallow — river factor [NEW] `[ANTAGONIST]`
- **Act III function:** miniboss; yields; optional witness.
- **Want:** paying, and dry feet. **Fear:** the fen.
- **Knows:** the Lock, the posts, the flush schedule, the buyer's name on the bill. **Doesn't know:** who the buyer really is.
- **Voice:** cheerful, quick, superstitious. Touches any chain before he does anything that matters. Jokes in a fight. Calls the player "friend" the way a man says it to a horse.
- **Change:** when he learns what the flushes stirred, he is frightened in a way the keepers never managed.

### Bram Hesketh — Keeper-Captain, Crestbridge [NEW]
- **Act III function:** the frightened official; saves his own signed orders from the fire; the hall's judgment.
- **Want:** no riots. **Fear:** that he signed something terrible. (He did.)
- **Voice:** clipped, tired, proud of his keepers. Says "my keepers" often. When he admits fault he uses short, complete sentences, as if reading from a charge sheet.
- **Change:** from hiding behind procedure to standing in front of it.

### Aldric Fenmere — Acting Steward [CANON ANCHOR]
- **Canon:** administers rather than commands; polite, reserved, fair; House Fenmere signed wartime supply compacts; keeps old ledgers; "quietly ashamed."
- **Act III function:** convenes the hearing and the plan; reads the finding; refuses to keep the plan.
- **Knows:** that the Board is pressing his stewardship; Fenmere's old compacts. **Doesn't know:** the Cut was open until Act I; anything about the Braids beyond what the player and Oriel's condition told him.
- **Voice:** quiet, exact, a little formal. Never raises his voice. Defers before he decides. **Guardrail:** no assigned wartime service; his shame is institutional ("my house signed"), never "I did."

### Corvin Tath — grain factor [CANON ANCHOR]
- **Canon:** numbers, weights, losses, never opinions; duplicate tallies; burned one ledger after the armistice and regrets it.
- **Act III function:** lays C2; regrets the ledger aloud **once**, at the table.
- **Voice:** numbers first. When he says something personal he says it as a number.
- **Guardrail:** the burned ledger stays unrecoverable. He does not say what was in it.

### Hollis Avery — Crestbridge Keeper [NEW, TL]
- **Act III function:** rings no bell, but finds the fire; holds the barge post at the table; lights the Whisperflow lanterns (keepers/shared).
- **Voice:** as TL, slightly more confident; still corrects himself. Calls Maelin "Mistress Rowe."

### Maelin Rowe — barge master [CANON ANCHOR]
- **Canon:** calm, efficient, observant; never asks what she's hauling; refuses night passage through specific stretches.
- **Act III function:** C1 holder (riverfolk); crews at the gates; the heart-stone post (crews); the night crossing.
- **Voice:** fewest words in the cast. In Act III she says even less. Her one long line in the act is mid-river (`RR-D6`).
- **Guardrail:** her night crossing is a judgment about one stretch now reading true, not a change of character.

### Lessa Mirepath — fen-edge guide [CANON ANCHOR]
- **Canon:** treats certain paths as permanently closed; speaks to the land as if it listens; refuses to explain why.
- **Act III function:** reopens the Cutters' Causeway for the evacuation; voices **Seal**.
- **Voice:** quiet, practical. Speaks to the path, not to the player, when it matters. Never explains the closure; she explains the reopening ("People are out there").
- **Guardrail:** no Mire kinship or travel implied.

### Sedge — reed-cutter (the Last Field-Mage, D-7) [NEW, PROPOSAL — DIRECTOR]
- **Act III function:** risk adviser in the hall (one line); the vigil's centre; spreads the pressure; refuses to choose; refuses to train.
- **Voice:** few words, exact ones. Answers questions with questions about what the player saw. Never names what he does.
- **`LM_SEDGE_TRUST`:** warm → a word of thanks he would never give anyone else; cool → the same facts, and nothing else.
- **Guardrail:** never confirms he is the Field-Mage aloud. Never rules, never teaches.

### Oriel — Riverwarden of the Listening Steps [NEW, PROPOSAL — DIRECTOR]
- **Act III function:** MQ12 only: quotes the player's promise; asks for their mark.
- **Voice:** formal, unhurried; water as work, never as a spirit. Uses "the Vale" for Lowmark. Says no more than she must.

### Ansel Corrie — Wraithwatcher [NEW, TL]
- **Act III function:** brings the news (MQ10 close); arms the player with smoke; voices **Shared**.
- **Voice:** gentle gallows humor, writes everything down. In Act III the jokes get shorter.
- **OL completed:** Joss Garrow is home in the only way he can be; Ansel speaks more steadily and hangs Joss's lantern.

### Annelise Reed — watergarden caretaker [CANON ANCHOR]
- **Canon:** tends quiet memorials; removes offerings before they rot; speaks softly to the water; dislikes unattended candles; "light enough to carry"; knows which names never appear on public memorials.
- **Act III function:** voices **Tend**.
- **Voice:** gentle, deliberate, speaks to the water as much as to people.
- **Guardrail:** she never says a name, and never says what she knows about unlisted names.

### Elspeth Quill — Flow-Mender [NEW]
- **Act III function:** trance-care station at Reedmere; one line on cost at the choice.
- **Voice:** gentle, practical, never wastes softmoss. Counts blankets aloud.

### Wynn Tarrow — carter [NEW, TL]
- **Act III function:** MQ12, loading the far-bank debt; pays Dace for the skiff.
- **Voice:** fast, blunt, counting. Calls the player "friend."

### Nan Ferrin — householder [NEW, TL]
- **Act III function:** MQ12 far bank; finally home, in her own bed. VK completed: sings the verse.
- **Voice:** slow, teasing, precise about small things. Duchess the hen is still treated with full formality.

### Tovin Pell — dock laborer and mill runner [CANON ANCHOR]
- **Canon:** notices; sketches; never names, never seeks, never solves.
- **Act III function:** C6 (named: stands up in the hall and answers one question); MQ12, looks at his own sheets on the keepers' wall.
- **Voice:** apologetic, short, concrete. **Guardrail:** his hall line describes what he saw on a floor, not what it means.

### Role-based and minor
Keepers (tired, sooty, proud), crews (terse), Watchers (call-and-answer), Reedmere cutters (dazed then dry-humored), far-bank households, the Keeper-Lieutenant (role-based; Hesketh's successor if stood down), the young pole-man (role-based; Sallow calls him "the lad"), Rhosyn Lyle (UL, NEW), Bryn Ruddock, Joric Fen [CANON ANCHOR], Brigid Corliss, Kell Ashby, Dace.

---

## Part 3 — MQ10 The Crest Hall Reckoning

### CR-D1 — Aldric on the hall steps (`S00_convene`)

```
CR-D1.01 ALDRIC: "You came. Good. I've called the plan for the morning bell."
CR-D1.02 ALDRIC: "The Riverwarden asked for public. Public means everyone hears it at once, so I've asked everyone."
  > "Will the Board be there?"                     → CR-D1.10
  > "What do you need from me?"                     → CR-D1.20
  > "Where do I sleep?"                             → CR-D1.30
CR-D1.10 ALDRIC: "All of it. The Provisioner arrived at noon with bread for the wall."   [ANTAGONIST]
CR-D1.11 ALDRIC: (looks at the households on the wall) "It was good bread."           → CR-D1 options
CR-D1.20 ALDRIC: "Whatever you've carried since Whisperflow. Bring it to the table in the morning."
CR-D1.21 ALDRIC: "Fenmere convenes. It doesn't keep. I'd like that understood before anyone sits down."   → CR-D1 options
CR-D1.30 ALDRIC: "Keepers' loft. Captain Hesketh has found you a bunk." (beat) "He hasn't found himself one."
      {event: CR-D1 end → completes S00_convene}
```

### CR-D2 — Marrick on the Waiting Wall (optional, `S01_evening`) `[ANTAGONIST]`

```
CR-D2.01 MARRICK: (breaking a loaf for a child) "There. Now go and show your mother you've been fed."
CR-D2.02 MARRICK: (to the player, delighted) "Oh, it's you. Sit, sit. I've heard about you from half the Vale."
  > "What have you heard?"                          → CR-D2.10
  > "You're feeding the wall."                      → CR-D2.20
  > "Do you know what tomorrow's about?"            → CR-D2.30
  > "Good night."                                   → CR-D2.40
CR-D2.10 MARRICK: "That you read a river bank better than most keepers read a page. That's rare. I'd hire you."
CR-D2.11 MARRICK: "Don't look so worried. I'm not allowed to hire anyone this week."     → CR-D2 options
CR-D2.20 MARRICK: "Someone should. Three settlements walked here for a meeting. Nobody thought to feed them."
CR-D2.21 MARRICK: "That's always the way. Plans for the households, and the households bring their own lunch."   → CR-D2 options
CR-D2.30 MARRICK: "Of course. The Braids. Very old, very wise, I'm told. I'll vote for whatever keeps the wall fed."
CR-D2.31 MARRICK: (gently) "Sleep well tonight. Big days start badly when people don't."   → CR-D2 options
CR-D2.40 MARRICK: "Good night, my dear. Mind the stair. It's old wood."   → end
```

*Note for writers:* CR-D2.31 and .40 are the only foreshadowing of the fire. Neither is evidence; both are true.

### CR-D12 — Corvin at the granary door (optional, `S01_evening`)

```
CR-D12.01 CORVIN: "One hundred and twenty drawn. Forty carried. I've said it to myself every night since the depot."
CR-D12.02 CORVIN: "Tomorrow I say it to the hall. Then it's not mine any more."
  > "Are you ready?"                     → CR-D12.03
  > "Keep them close tonight."           → CR-D12.04
CR-D12.03 CORVIN: "Numbers are always ready. It's the room that isn't."   → end
CR-D12.04 CORVIN: (taps his coat) "Two copies. I've learned that much."   → end
```

### CR-D13 — Hesketh in the yard (optional, `S01_evening`)

```
CR-D13.01 HESKETH: "Again. Stand straighter. You're Crestbridge keepers, not sacks." (to the player) "They've been up since dawn."
CR-D13.02 HESKETH: "So have I. I'll sleep after."
  > "After what?"                           → CR-D13.03
  > "Your keepers look fine."               → CR-D13.05
CR-D13.03 HESKETH: "After they read the orders out. Mine are in there."  (nods at the hall)
CR-D13.04 HESKETH: "I signed what I was handed. Every time. I'd like to have been the kind of man who asked."   → end
CR-D13.05 HESKETH: "They are. That's what worries me. They'll stand there and do what they're told."   → end
```

### CR-D3 — Hollis at the top of the stair (`S02_alarm`)

```
CR-D3.01 HOLLIS: "Both hoardings! It's in the tow, somebody laid tow —" (coughs) "I can't get down."
CR-D3.02 HOLLIS: "Cut it out or smother it. There's wet sacks on the pegs in the granary passage."
CR-D3.03 HOLLIS: "The records are down there. All of them." (beat) "Yours too."
      {event: objective → S03_firelines}
```

### CR-D4 — Hesketh behind the Board press (`S04_records`)

```
CR-D4.01 HESKETH: (hauling at the cabinet, hands wrapped in his coat) "Don't. Don't take it off me. I'm not burning it."
CR-D4.02 HESKETH: "The Board's minute book. Every order I signed is in it, with what I was told it was for."
CR-D4.03 HESKETH: "Take it. Read it out in the morning. Every line, with my name in it."
      {give CR_board_minute}
  > "Come on. Out."                          → CR-D4.04
  > "Who did this?"                          → CR-D4.05
CR-D4.04 HESKETH: "Right behind you. Don't wait for me, I'm slow."   {event: Hesketh escort begins} → end
CR-D4.05 HESKETH: "Lock men. I saw a boat-hook on the water-gate stair." (beat) "Out. Ask me outside."   {event: Hesketh escort begins} → end
```

### CR-D5 — Sallow arrives on the landing (`S06_sallow`, barks) `[ANTAGONIST]`

```
CR-D5.01 SALLOW: (climbing out of the basin, dripping, touching the gate chain) "Evening! Don't mind me. Just here for the barge."
CR-D5.02 SALLOW: "No? Shame. Nobody's ever let me have anything easy, friend."
      {event: E4 begins}
```

**Sallow fight barks**

| Trigger | Line |
|---|---|
| First Hook Sweep | "Mind your knees!" |
| Rope Cut | "Lights out. Sorry. Sorry, that one was rude." |
| Player falls in the basin | "Water's cold, isn't it? I hate it. Hate it." |
| Player relights a lantern | "Oh, put that out, it's not helping anyone." |
| Chain Touch at 66% | (hand on the chain, eyes shut) "Keep me dry. Keep me dry." |
| Chain Touch at 33% | "That's the last time I come down here. I mean it this time." |
| Pole-men join | "Lads! Work for your money!" |
| Shove misses into a bollard | "Ow. Yes. Fair." |

### CR-D6 — Sallow yields (`S06_sallow`) `[ANTAGONIST]`

```
CR-D6.01 SALLOW: (both hands on the chain) "Enough. Enough. I'm done. Look, no hook."
CR-D6.02 SALLOW: "Keepers'll want me. Fine. Get me out of this basin first, I'm begging."
  > [CR_HAULED_CREWMAN] "I pulled your lad out of the gate."        → CR-D6.10
  > "Do you know what the flushes did to the fen?"                 → CR-D6.20
  > "Save it for the keepers."                                      → CR-D6.40

CR-D6.10 SALLOW: (long look) "You did. I saw." (beat) "He can't swim. None of them can. I never asked."
CR-D6.11 SALLOW: "All right. Lock, posts, the buyer's name off the bill. And tonight."
CR-D6.12 SALLOW: "She said there should be nothing to read in the morning. Those words. I'll say them in the hall."
CR-D6.13 SALLOW: "One thing. My crew work the seal, not the lock-up. They only did what I paid them for."
      {set CR_SALLOW_ACCOUNT = full}  → CR-D6.30

CR-D6.20 SALLOW: "The fen?" (touches the chain) "Don't. Don't talk about the fen down here."
CR-D6.21 SALLOW: (listening to the player) "Every flush. Every one dragged that out." (quietly) "I used to wave at the fog."
CR-D6.22 SALLOW: "I'll tell them how we ran the Lock. Every flush, every post. Not tonight, though. Tonight's hers."
CR-D6.23 SALLOW: "One thing. My crew work the seal, not the lock-up. They only did what I paid them for."
      {set CR_SALLOW_ACCOUNT = lock if not already full}  → CR-D6.30

CR-D6.30
  > "You have my word. Your crew work the seal."     → CR-D6.31
  > "That's not mine to promise."                   → CR-D6.33
CR-D6.31 SALLOW: "Then you have mine. Such as it is." (lets go of the chain)
      {set CR_CREW_LENIENCY}  → CR-D6.40
CR-D6.33 SALLOW: "Then I've got nothing to say to a hall." (beat) "Shame. I'd have been good at it."
      {clear CR_SALLOW_ACCOUNT}  → CR-D6.40

CR-D6.40 HOLLIS: (arriving with keepers) "Gideon Sallow. You're in keepers' custody." (to the player, quieter) "Are you hurt?"
      {event: CR-D6 end → completes S06_sallow}
```

Repeat interaction after CR-D6.33: Sallow, in custody, offers CR-D6.30 once more ("Changed your mind? Mine's for sale."), until the hearing begins.

### CR-D7 — Dawn in the yard (`S07_dawn`)

```
CR-D7.01 ALDRIC: (looks at the cart of scorched records, the keepers, the player) "..."
CR-D7.02 ALDRIC: "I'm told the hall still stands because you cut a staircase in half."
CR-D7.03 [CR_FED_KEEPERS] HESKETH: "And fed my keepers. They'll follow you into the river now, which is not procedure."
CR-D7.03 [else]           HESKETH: "My keepers did well. All of them. Write that down somewhere, someone."
CR-D7.04 ALDRIC: "We meet at the bell. The Provisioner sent word she'll attend." [ANTAGONIST] (beat) "She asked if anyone was hurt."
  > "Was anyone?"                       → CR-D7.05
  > "Ring the bell."                    → end {event: wait_for_bell enabled}
CR-D7.05 HESKETH: "Hands. Mine. And one Lock lad who swallowed half the basin." (beat) "Nobody drowned in my hall."   → end {event: wait_for_bell enabled}
```

### CR-D8 — The long table (`S08_table`) `[ANTAGONIST]`

**Opening**

```
CR-D8.01 ALDRIC: "We're here to plan. Before we plan, someone has asked to lay things on this table. I've agreed."
CR-D8.02 MARRICK: "Of course. Let's have everything out. The households deserve that much." (folds her gloves)
      {event: chip holders become interactable}
```

**Chip lines.** Taking a chip from its holder plays the holder's line; laying it plays the reading and Marrick's answer. After her answer, control returns.

```
— C1, Whisperflow proof —
CR-D8.10 [LM_TL_EVIDENCE = keepers] HOLLIS: (from the record cart) "My report. And the post. Singed, but you can see the notch."
CR-D8.10 [LM_TL_EVIDENCE = riverfolk] MAELIN: "The Whisperflow post. And one more off the Greyharrow bend. Same notch, same hand."
CR-D8.10 [LM_TL_EVIDENCE = player] (player lays the post they have carried since Whisperflow; no line)
CR-D8.11 HESKETH: "A crossing post. Moved overnight, on a flush night, to read open."
CR-D8.12 MARRICK: "On a dark bank? Anyone can move a post. Children do it for dares."
CR-D8.13 [C5 already laid] MARRICK: (glancing at the yellow post already on the table) "...Though not usually with a matching set."

— C2, Corvin's tallies —
CR-D8.20 CORVIN: "One hundred and twenty sacks drawn under the emergency. Forty carried by road. Eighty are not anywhere."
CR-D8.21 MARRICK: "Grain is lost every season, Factor. To damp, to rats. To goblins under your own depot, I heard."
CR-D8.22 CORVIN: "Twelve sacks to goblins. I counted them too."
CR-D8.23 CORVIN: (to the table, not to anyone) "I burned a ledger once, after the war. I've wished every year I hadn't. Not this one."

— C3, depot slip —
CR-D8.30 HESKETH: "A requisition slip. Board seal. A night draw, lowered down the depot chute by rope."
CR-D8.31 MARRICK: "The Board's seal goes on a hundred slips a season. I can't answer for every clerk with a stamp."

— C4, Hollow Lock bill —
CR-D8.35 HESKETH: "Bill of lading from the Hollow Lock. Relief grain. Board seal. Sold downriver at priority rate."
CR-D8.36 MARRICK: "A buyer paid what we could not refuse. And the far bank ate because of it."
CR-D8.37 [C2 already laid] CORVIN: "Forty sacks' worth of eating."

— Grain-route clause (fires once, after C4 or C2, whichever is second) —
CR-D8.40 [LM_GRAIN_ROUTE = escort] HOUSEHOLDER: (from the gallery) "We were fed by road. Keepers walked it. Nobody rioted. We said thank you."
CR-D8.40 [LM_GRAIN_ROUTE = hold]   MARRICK: "And when it was held? They went hungry. As I said they would. Ask them."
CR-D8.41 [LM_GRAIN_ROUTE = hold]   HOUSEHOLDER: (from the gallery, after a moment) "We were hungry. We'd still rather know."
CR-D8.40 [LM_GRAIN_ROUTE = split]  HOUSEHOLDER: "Half came by road. Half didn't come. We noticed which half."

— C5, Lock posts —
CR-D8.45 HOLLIS: (sets the yellow post down; it is the same as the one at Whisperflow) "From the Lock. There's a barge full."
CR-D8.46 [LM_LOCK_STATE = chained] HESKETH: "My keepers inspected the Lock before the chain was cut. Stock of posts, notches pre-cut, a hand high."
CR-D8.47 MARRICK: "Smugglers, then. My factor hired badly. I grant you that freely."

— C6, Tovin's calendar —
CR-D8.50 [LM_TOVIN_CREDITED = named] ALDRIC: "Master Pell. Would you tell the hall what these are?"
CR-D8.51 [named] TOVIN: (standing, holding the sheets against his chest) "The mill floor. Mornings. I drew where it was wet."
CR-D8.52 [named] TOVIN: "It was wet on the same mornings. Every time. I drew what the floor did. That's all."   {set CR_TOVIN_STOOD}
CR-D8.50 [unsigned] HESKETH: "Sheets. Unsigned. Wet-lines on the Drowsebank floor, dated. Each a day after a draw."
CR-D8.53 MARRICK: "Pretty drawings." (kindly) "Whose?"
CR-D8.54 [named] MARRICK: "...Well. You were very brave to stand up. Sit down, dear, before you fall."

— C7, the Board's minute book —
CR-D8.60 HESKETH: (opens the book; reads the first entry aloud) "Emergency declared, far bank. Moved by the Provisioner. Carried. Blanket order signed: B. Hesketh."
      {event: cr.minute_read → water-gate stills (quest file §10.7)}
CR-D8.61 HESKETH: (keeps reading; three more entries, same shape; his voice does not change)
CR-D8.62 MARRICK: "I moved them because the households were hungry. Read it: I said so every time. I meant it every time."

— C8, Rhosyn's papers (completed side quest UL) —
CR-D8.65 RHOSYN: "Keeper-passes. My work, I'm afraid, and very good. Paid for from this purse." (lays a purse-ledger page beside them)
CR-D8.66 MARRICK: "A forger. In Crest Hall." (smiles) "Bless you. You'll be very popular after this."
CR-D8.67 RHOSYN: "I usually am."   {set CR_RHOSYN_LAID}

— C9, Sallow's account —
CR-D8.68 [CR_SALLOW_ACCOUNT = full] SALLOW: (from custody, by the floor-grate) "The Lock, the posts, the buyer. And last night: 'nothing to read in the morning.' Her words."
CR-D8.68 [CR_SALLOW_ACCOUNT = lock] SALLOW: "I ran the Lock. Every flush on her draw nights. I moved the posts. That's all you get."
CR-D8.69 MARRICK: (not looking at him) "My factor will say anything to stay out of the water."
CR-D8.69b [C4 and C5 laid] ALDRIC: "He's saying what the bill and the posts already said, Provisioner."
```

**The silence (after `cr.minute_read`, when sound returns)**

```
CR-D8.70 MARRICK: (glancing at the floor-grates) "Even the river is listening. How flattering for all of us."
```

**Rejected objects (not chips; quest file §10.5.3)**

```
CR-D8.R1 [Ansel's patrol book] ALDRIC: "It tells us when the water went wrong. It doesn't tell us who."
CR-D8.R2 [Joss's lantern]      ANSEL: (from the wall) "That's a man's lantern, not a witness. Put it down gently."
CR-D8.R3 [any account of the stone, the flow-table, drift] MARRICK: "The river has opinions now? How flattering for all of us."
```

**Three valid chips laid**

```
CR-D8.80 ALDRIC: (stands) "That's enough to answer."
  > "There's more."                       → (control returns; chips stay interactable)
  > "That's all of it."                   → CR-D8.90
```

When the last available chip is laid, CR-D8.90 follows automatically.

**The finding**

```
CR-D8.90 ALDRIC: "The Provision Board's emergency draws were moved by the Provisioner, sold downriver, and hidden behind moved posts."
CR-D8.91 [CR_TERMS = bare] ALDRIC: "That is what this table shows. What the Board does with it is the Board's to say."
CR-D8.91 [firm/full]       ALDRIC: "House Marrick's seat is vacated. Its claim on the stewardship is withdrawn." [full: "Struck."]
CR-D8.92 MARRICK: (rises, unhurried, collects her gloves) "Write that I came. That I sat at this table and heard it all."
CR-D8.93 [CR_TERMS = full] MARRICK: "And open my granaries. The households shouldn't wait on anyone's pride. Least of all mine."
CR-D8.93 [else]            MARRICK: "My granaries are open to the vigil, of course. No one needs to order it. I'm offering."
CR-D8.94 MARRICK: (to the player, warmly, on her way past) "You did that very well. I meant it. I would have hired you."
      {set LM_MARRICK_EXPOSED; set CR_TERMS, CR_MARRICK_STORES; event: S08 complete}
```

### CR-D9 — Hesketh stands (`S09_hesketh`)

```
CR-D9.01 HESKETH: (standing; reads from nothing) "I signed every blanket order in that book. I didn't ask where the grain went."
CR-D9.02 HESKETH: "I was told the far bank would riot. I believed it because it was easier to believe."
CR-D9.03 ALDRIC: "The keepers need a captain this afternoon. Does anyone speak for this one?"
CR-D9.04 ALDRIC: (the hall turns, slowly, to the player)
  > "I do. He carried his own orders out of a fire to have them read."   → CR-D9.10
  > (Say nothing. Let the hall decide.)                                → CR-D9.20
  > "Let him speak for himself."                                        → CR-D9.30

CR-D9.10 HESKETH: (a long breath) "...Thank you."
CR-D9.11 ALDRIC: "Then Captain Hesketh stays, under a crossing keeper's countersign. As does every captain after him."
      {set LM_HESKETH = kept}  {event: S09 complete}

CR-D9.20 ALDRIC: (after a silence) "Then I'll stand him down. With thanks for his keepers. Lieutenant, you have the yard."
CR-D9.21 HESKETH: "Put me on the seal crew. I can carry a plank." (beat) "My hands'll mend."
      {set LM_HESKETH = stood-down}  {event: S09 complete}

CR-D9.30 HESKETH: (to the hall) "Then I stand myself down. Lieutenant, the yard's yours. Put me on the seal crew."
CR-D9.31 ALDRIC: "...So recorded." (quietly) "That was well done, Captain."
      {set LM_HESKETH = stood-down; set CR_HESKETH_SELF}  {event: S09 complete}
```

### CR-D10 — The Braid plan (`S10_plan`)

```
CR-D10.01 ALDRIC: "Now the plan. Fenmere convenes it. Fenmere doesn't keep it." (to the player) "The condition was given to you. Speak first."
CR-D10.02 ALDRIC: "Crews open and close the Braid gates. Watchers walk the heavy water. That much everyone agrees."
CR-D10.03 [first time] ALDRIC: "Before we go on. You, at the back. You know the fen."
CR-D10.04 SEDGE: (by the door, not moving forward) "When the Cut's shut for good, the fen holds its breath. Then it lets go."
CR-D10.05 [LM_SEDGE_TRUST = warm] SEDGE: "Be there. All of you. Not just the one." (nods at the player; leaves)
CR-D10.05 [cool]                  SEDGE: "Be there." (leaves)
CR-D10.06 ALDRIC: "Who calls the crossings shut when the water rises?"
  > "The crews. They read the river."                                 → CR-D10.10
  > "The keepers. They hold the posts and the record."               → CR-D10.11
  > "Both. Crews call it, keepers post it."                          → CR-D10.12
CR-D10.10 MAELIN: "Aye."                    {set LM_PLAN_ROUTES = crews}    → CR-D10.20
CR-D10.11 [kept] HESKETH: "Aye." [stood-down] LIEUTENANT: "Aye."  {set LM_PLAN_ROUTES = keepers}  → CR-D10.20
CR-D10.12 MAELIN: "Aye." HOLLIS: "Aye. Yes. Aye."                   {set LM_PLAN_ROUTES = shared}   → CR-D10.20

CR-D10.20 ALDRIC: "And who tends the fen's memorial ground? The edge, where people go to mourn."
  > "The Watchers. They're out there every night already."           → CR-D10.21
  > "Annelise and the watergarden keepers. It's their work."        → CR-D10.22
  > "Reedmere. They live beside it."                                → CR-D10.23
CR-D10.21 ANSEL: "Aye. I'll need a bigger book."                     {set LM_PLAN_MEMORIAL = watchers}  → CR-D10.30
CR-D10.22 ALDRIC: "I'll send to Ashenstead. Mistress Reed will want it light enough to carry."  {set LM_PLAN_MEMORIAL = gardens} → CR-D10.30
CR-D10.23 LESSA: (from the gallery steps) "Aye. Some of it." (beat) "We'll see which."   {set LM_PLAN_MEMORIAL = reedmere} → CR-D10.30

CR-D10.30 ALDRIC: "Farm ditches to the orchard hands." [LM_BRYN_ROLL = commons: "Bryn Ruddock named, on the commons roll."] [household: "Bryn Ruddock named, as household, by her own word."]
CR-D10.31 ALDRIC: "A trance-care station at every vigil, Mistress Quill named. The Cut sealed today, both ends, by crews and keepers."
CR-D10.32 [CR_CREW_LENIENCY] ALDRIC: "With the Lock men carrying the planks, under watch."
CR-D10.33 ALDRIC: "Written three times. Keepers' record, crews' book, Watchers' book. No chair. No seal." (beat) "Is it agreed?"
      (gallery barks: "Aye." ×6, overlapping; one household: "Is there lunch?")
      {event: S10 complete}
```

### CR-D11 — Ansel at dusk (`S11_dusk`)

```
CR-D11.01 ANSEL: (walking in off the fen road, lantern unlit) "They dropped the last plank at noon. I was on the fen road by one."
CR-D11.02 ANSEL: "It's gone still. No birds. Fog lying flat on the water like a sheet on a bed."
CR-D11.03 ANSEL: "Like it's holding its breath." (beat) "I've never been scared of quiet before."
  > "Sedge said this would happen."           → CR-D11.04
  > "Then we go."                             → CR-D11.05
CR-D11.04 ANSEL: "He said it to a whole hall. That's the most I've ever heard him say." → CR-D11.05
CR-D11.05 ANSEL: "Reedmere, then. Before dusk tomorrow. Bring food. Bring your boots." (lights his lantern) "Bring everyone."
      {event: CR-D11 end → quest Completed; MQ11 offered}
```

### MQ10 barks

| Trigger | Speaker | Line | Condition |
|---|---|---|---|
| Evening, wall | HOUSEHOLD | "Three settlements, one wall. Good bread, mind." | — |
| Evening, yard | KEEPER | "Captain says sleep. Captain hasn't." | — |
| Bell | KEEPER | "Fire! Undercroft! Wake up, that's not a drill, I've never rung it for a drill!" | — |
| Fire-line cut | KEEPER | "Line's down! Go, go!" | — |
| Sack smother | KEEPER | "That's old fire practice. My gran would kiss you." | — |
| Bundle singed | KEEPER | "Got it out! It's warm. It's — it's fine, it's readable." | singe |
| Bundle delivered | HOLLIS | "On the cart. Go back for the other." | — |
| Barge lines | POLE-MAN | "Cut it! Cut it and push!" | — |
| Crewman swept | POLE-MAN (young) | "I can't — the gate — I can't swim!" | — |
| Haul complete | POLE-MAN (young) | (coughing) "...Thanks. Don't tell him." | `CR_HAULED_CREWMAN` |
| Hearing, gallery, after C2 | HOUSEHOLD | "Eighty sacks. That's our winter." | — |
| Hearing, fed keepers | KEEPER | (at the wall, to another) "That's the one who cooked." | `CR_FED_KEEPERS` |
| Plan agreed | CREW | "Aye. And when it floods?" / KEEPER: "Then we do what we said." | — |
| Post-quest, Crestbridge | KEEPER | "Countersign. On everything. I've signed my name more this week than all last year." | — |

---

## Part 4 — MQ11 Stillwater's Vigil

### SV-D1 — Sedge on the lantern-store steps (`S01_vigil`)

```
SV-D1.01 SEDGE: "Tonight. Maybe sooner."
SV-D1.02 SEDGE: "People in first. Then the gates. Then the middle." (beat) "What did the water do when you walked in?"
  > "Nothing. That's what bothered me."       → SV-D1.03
  > "It was still. Too still."                → SV-D1.03
  > "It felt like it was waiting."            → SV-D1.04
SV-D1.03 SEDGE: "Good. That's what it did."                            → SV-D1.05
SV-D1.04 SEDGE: "It was still. Waiting's yours." (not unkindly)         → SV-D1.05
SV-D1.05 [LM_SEDGE_TRUST = warm] SEDGE: "I'll be in the middle when you get there. Don't hurry. Don't be late."
SV-D1.05 [cool]                  SEDGE: "I'll be in the middle."
      {event: SV-D1 end}
```

### SV-D2 — Ansel at the lantern store

```
SV-D2.01 ANSEL: "Smoke-pot. Three good puffs a fill. Racks along both lanes. Lessa hung the ones on the Causeway."
SV-D2.02 ANSEL: "If someone stops and turns to the water, don't argue. Smoke, then lantern. They'll follow the light."
SV-D2.03 ANSEL: "They don't go deeper than the knee. I've never seen one go deeper than the knee." (beat) "Tonight I'm not promising."
  > "What makes them turn?"                    → SV-D2.04
  > "Got it."                                  → end {give smoke-pot if needed}
SV-D2.04 ANSEL: "They say they hear a count. Four knocks. Then they want to go and see who's counting."   → end {give smoke-pot if needed}
```

### SV-D3 — Lessa pulls her stake (`S01_vigil`)

```
SV-D3.01 LESSA: (to the stake, hand on its wound cloth) "I said you were done."
SV-D3.02 LESSA: (pulls it up, lays it on the bank) "People are out there. That's the only reason."
SV-D3.03 [completed side quest FW] LESSA: (to the player) "My knots are on the ridge too. Faster. Narrower. Don't run on it."
SV-D3.04 LESSA: "Bring them in by the stones. The causeway remembers carts. It can remember feet."
      {event: Causeway lane open; FW → Lessa's route open}
```

### Evacuation lines

**Cutters (when found)**

| Hut | Speaker | Line |
|---|---|---|
| Hookreed | CUTTER 1 | "Lantern? Oh, thank the — is it bad? It sounds bad." |
| Hookreed | CUTTER 2 | "I'm not leaving my bundles." (beat) "I'm leaving my bundles." |
| Two Posts | CUTTER 3 | "Kettle's on. Kettle's always on. Take the kettle?" |
| Two Posts | CUTTER 4 | "My brother went in at the Far Racks. Is he — " (if Far Racks not done) |
| Two Posts | CUTTER 5 | "Walk slow. My knee's older than the causeway." |
| Far Racks | CUTTER 6 | (by the boots, barefoot, staring at the water; silent until smoked) |
| Far Racks | CUTTER 7 | "Don't listen to the reeds. They've been calling in Hollin's voice all night. Hollin's here." |

**Trance and recovery (any follower)**

| Stage | Line |
|---|---|
| Warning (distant) | (four hollow knocks, evenly spaced) |
| Turning | (no line; the follower lowers their lantern) |
| Walking | (no line; only footsteps in water) |
| Smoked, recovered | "...What? Why am I wet?" / "I heard someone counting." / "Was I — sorry. Sorry." / "That's foul. Again, if I do it again." |
| Led out from standing | "It's cold. It wasn't cold a minute ago." |

**Mud Pipers at the Far Racks**

| Line (in a cutter's voice, from the wrong reeds) |
|---|
| "Over here — I'm stuck — over here —" |
| "Hollin? Hollin, bring the light —" |

**Reedmere tally board (keeper or crew by `LM_PLAN_ROUTES`)**

| Trigger | Line |
|---|---|
| First arrival | "One off the board. Six to go." |
| Middle arrivals | "Off. Good. Next." |
| Last arrival | "Board's clean. Everybody's in." |
| `LM_PLAN_ROUTES = shared` | CREW: "Mine." KEEPER: "Ours." CREW: "...Ours." |

### SV-D4 — Elspeth in the loft (optional, any time)

```
SV-D4.01 ELSPETH: "Seven blankets. Five softmoss packs. Two kettles. One very rude cutter."
SV-D4.02 ELSPETH: "They come out of it cold and ashamed. The cold I can fix."
  > [CR_MARRICK_STORES] "Is there food?"                          → SV-D4.03
  > "What do you tell them?"                                    → SV-D4.04
SV-D4.03 [ordered] ELSPETH: "Crestbridge sacks. Marrick's. The keepers made sure we knew they were owed."
SV-D4.03 [offered] ELSPETH: "Crestbridge sacks. A gift, the label says. Very large letters."   → SV-D4 options
SV-D4.04 ELSPETH: "That they heard something, and walked towards it, and came back. That's all that happened."   → end
```

Cooked food given (`S02b_feed`): ELSPETH: "Oh, warm. Warm is the medicine. Give it to the barefoot one first."

### Gate lines

```
SV-D5.01 [gate 1] CREW: "Board's chalked one. Read your stone and we'll crank."
SV-D5.02 [gate 1, CR_CREW_LENIENCY] LOCK MAN: "Didn't think I'd be opening one of these." KEEPER: "Crank."
SV-D5.03 [gate 1 open] MAELIN: "Running. Next."
SV-D5.10 [gate 2] CREW: "Something's under the sill. Something big's under the sill —"
SV-D5.11 [Serpent breach] MAELIN: "Get it off the sill! It's pushing the gate shut!"
SV-D5.12 [gate 2 open] MAELIN: "Two." (to the crew) "Breathe later."
SV-D5.20 [gate 3, 50%] WATCHER: (from the sluice pier) "Lights! In the middle! There's lights standing up!"
SV-D5.21 [gate 3 open] MAELIN: (looking towards the heart pool, quiet) "Go on. We'll hold these."
```

**Gate stone inspect texts:** before opening: *"Water's stuck under the notch. It wants to move."* After: *"Water's moving past the notch. A Watcher's lantern hangs beside it."*

**Watchers' call-and-answer (ambient, Beat 3 onwards):** "Lantern on the weir!" / "Lantern holds!" · "Lantern on the sill stone!" / "Holds!" · "Every stone, Ansel said, every one —" / "I'm doing every one!"

### SV-D6 — Sedge at the heart pool (`S06_muster`)

```
SV-D6.01 SEDGE: (knee-deep at the edge, hands at his sides) "Don't stand where it's stuck. Stand where it moves."
SV-D6.02 SEDGE: "The stones by the new water. They'll read." (beat) "You know how."
      {event: E5 begins}
SV-D6.20 [after player death] SEDGE: (still standing there) "Again. Where it moves."
```

**Muster audio (non-verbal; never a voice):** the four-count knock; a long creak of wood under strain; on dispersal, nothing.

### SV-D7 — After the fen exhales (`S07_heart_stone`)

```
SV-D7.01 SEDGE: (sitting on the heart stone's plinth, hands dripping) "..."
SV-D7.02 SEDGE: "That's the whole of it. Spread thin. Every Braid." (beat) "What did you see?"
  > "Every stone held a line at once."              → SV-D7.03
  > "The fen let go."                               → SV-D7.04
  > "You did that."                                  → SV-D7.05
SV-D7.03 SEDGE: "Yes."                                                               → SV-D7.06
SV-D7.04 SEDGE: "It went down a hand. You saw that. The rest is a word for it."      → SV-D7.06
SV-D7.05 SEDGE: "I put my hands in the water. The crews opened the gates. You seated a post." → SV-D7.06
SV-D7.06 [warm] SEDGE: "Thank you." (looks surprised to have said it)
SV-D7.06 [cool] SEDGE: "Go and sleep. They'll want you at dawn."
```

### SV-D8 — Dawn: what happens to Stillwater (`S08_choose`)

```
SV-D8.01 MAELIN: "The plan said Stillwater's for those who stood the vigil. We stood it. We can't agree."
SV-D8.02 MAELIN: "You were at the stone. You say."
  > "What do you want, Lessa?"                    → SV-D8.10
  > "Annelise?"                                   → SV-D8.20
  > "Ansel?"                                      → SV-D8.30
  > "Sedge, what would you do?"                   → SV-D8.50
  > [all three heard] "I've heard enough."        → SV-D8.60
```

**Seal — Lessa**

```
SV-D8.10 LESSA: (to the fen, not to the player) "I opened one last night. It was the right one."
SV-D8.11 LESSA: "Close the deep. A whole generation. Let the reeds have it. Let the children grow up never knowing the way in."
SV-D8.12 [kept] HESKETH: "My keepers will post it. Stakes, rope, lanterns. Nobody crosses." [stood-down] LIEUTENANT: (same line)
SV-D8.13 ANNELISE: "You've shut the door on people who still knock."
SV-D8.14 LESSA: "Then they knock on a door. Not on deep water."            → SV-D8 options
```

**Tend — Annelise**

```
SV-D8.20 [completed side quest CN] ANNELISE: (sets the recovered offering boat on the water; it turns once and sits still) "This came back."
SV-D8.21 ANNELISE: "Cut a channel at the edge. Light it. Let people bring what they can carry, and let the water carry it."
SV-D8.22 ANNELISE: "Remembrance should be light enough to carry. A sealed fen isn't light. It's a stone on a chest."
SV-D8.23 LESSA: "You'll be walking people out of the water every winter."
SV-D8.24 ANNELISE: "Then I'll walk them out. I've done harder walks."    → SV-D8 options
```

**Shared — Ansel**

```
SV-D8.30 [completed side quest OL] ANSEL: (hangs a dented lantern on a reed-stake at the edge) "Joss walked the deep for years. The deep doesn't give back Watchers."
SV-D8.30 [else]                    ANSEL: "The deep takes Watchers. I've known two it took. I'd rather not know three."
SV-D8.31 ANSEL: "Shut the deep pools. Keep the edge. People need somewhere to stand that isn't a rope."
SV-D8.32 ANSEL: "I'll walk both. I'll need help. I'll need a lot of help."
SV-D8.33 MAELIN: "That's two jobs. Plan's got hands for one and a half."
SV-D8.34 ANSEL: "Then it'll get more hands. That's what the plan's for."   → SV-D8 options
```

**Sedge refuses**

```
SV-D8.50 SEDGE: "Not mine."
  > "Tell me something true about each."      → SV-D8.51
  > "All right."                              → SV-D8 options
SV-D8.51 SEDGE: "Seal holds as long as someone keeps the rope."
SV-D8.52 SEDGE: "Tend keeps it heavy, a little, where people can see it."
SV-D8.53 SEDGE: "Both is the most work." (beat) "Work is what holds."   → SV-D8 options
```

**Elspeth (auto, once, before the choice)**

```
SV-D8.55 ELSPETH: "Whatever you say, someone walks into water somewhere next winter. My station stays." 
SV-D8.56 [SV_FED_EVACUEES] ELSPETH: "And bring food next time. That helped more than the softmoss."
```

**The choice**

```
SV-D8.60 MAELIN: "Well?"
  > "Seal it. Close the deep for a generation."                 → SV-D8.70
  > "Tend it. Cut the channel at the edge."                     → SV-D8.80
  > "Both. Seal the deep pools. Tend the edge."                 → SV-D8.90

SV-D8.70 LESSA: "Done." (picks up her stake) "That's the last time I say it this year."
SV-D8.71 ANNELISE: (after a moment) "Then I'll bring the baskets to the Step. People will need somewhere."
      {set LM_FEN_ENDING = seal}  → SV-D9

SV-D8.80 ANNELISE: (to the water, softly) "There. You'll have visitors."
SV-D8.81 LESSA: "I'll knot the deep paths. Guides only." (beat) "I'm not saying it's wrong."
      {set LM_FEN_ENDING = tend}  → SV-D9

SV-D8.90 ANSEL: (writing) "Seal deep. Tend edge. Watchers both." (looks up) "That's the biggest thing I've ever written."
SV-D8.91 LESSA: "Half done." ANNELISE: "Half light." (they look at each other; neither smiles; both nearly do)
      {set LM_FEN_ENDING = shared}  → SV-D9
```

### SV-D9 — Maelin closes (`S09_close`)

```
SV-D9.01 MAELIN: "Crews keep what you said. That's the plan."
SV-D9.02 MAELIN: "Walk the Vale today. See what it looks like." (beat) "Come to the landing at dusk."
  > "Why dusk?"                          → SV-D9.03
  > "I'll be there."                     → end {event: quest Completed; MQ12 begins}
SV-D9.03 MAELIN: "You'll see."           → end {event: quest Completed; MQ12 begins}
```

### MQ11 barks

| Trigger | Speaker | Line | Condition |
|---|---|---|---|
| Arrival | CREW | "Rope, rope, more rope. Who brought the rope?" | — |
| Arrival | KEEPER | "Crestbridge sacks, mind. Don't stand on them." | `CR_MARRICK_STORES` |
| Arrival | CREW (to Lock man) | "You. Under watch. Crank's that way." | `CR_CREW_LENIENCY` |
| Current begins | WATCHER | "There it goes. Lanterns up!" | — |
| Serpent killed | CUTTER (post-quest) | "They found it on the sill at dawn. Big as a barge. Nobody's eating it." | `SV_SERPENT_KILLED` |
| Serpent driven | CUTTER (post-quest) | "It went back down. It'll stay down, if it's sensible." | `SV_SERPENT_DRIVEN` |
| After the hold | WATCHER | "Lantern holds!" / "Holds!" | — |
| After the hold | CUTTER (humming) | (the listeners' tune, badly) | completed side quest VK |
| Memorial station | ANSEL / ANNELISE / LESSA at Widow's Step | "Watch your feet on the Step. Watch the water." / "Light enough." / "Stay off the edge." | `LM_PLAN_MEMORIAL` |

---

## Part 5 — MQ12 The River Remains

### RR-D1 — Wynn and the last sack (`S01_crestbridge`)

```
RR-D1.01 WYNN: "Friend! One more. Last of the eighty. Put it on the top, it's the only one that isn't split."
      (player carries the sack to the cart)
RR-D1.02 WYNN: "Eighty sacks. Dry. Over a bridge. Not one eaten by a pig. I'll take it." (beat) "Again."
RR-D1.03 WYNN: (to DACE, if present; else to the air) "Here. For the skiff. Told you. When I'm paid."
RR-D1.04 [completed side quest NT] DACE: "...That's too much." WYNN: "It's interest. Take it before I count it."
RR-D1.05 WYNN: (to the player, a coin) "And yours. Don't argue, I've had a week."
      {currency: small}
```

### RR-D2 — Marrick at her granary door (`S01_crestbridge`) `[ANTAGONIST]`

```
RR-D2.01 [CR_TERMS = bare] MARRICK: (on her step, a teapot beside her) "Come and sit. I'm a householder now. We're allowed to have visitors."
RR-D2.01 [firm]            MARRICK: (beside the keepers' seal on her door) "Mind the seal. Very official. I had them make it straight."
RR-D2.01 [full]            MARRICK: (watching keepers count sacks out) "Eighty-one, eighty-two. They're very thorough. I trained half of them."
RR-D2.02 MARRICK: "Tea? It's my own. Nobody's ordered that yet."
  > "Why did you do it?"                    → RR-D2.10
  > "Are you all right?"                    → RR-D2.20
  > "No. Thank you."                        → RR-D2.30
RR-D2.10 MARRICK: "I kept the Vale fed in the war, and the Vale thanked Fenmere. I wanted it to remember right."
RR-D2.11 MARRICK: "It will now, I suppose. Just not the way I meant."     → RR-D2.30
RR-D2.20 MARRICK: (surprised, then pleased) "That's kind. You're the first to ask." (beat) "I'm writing my house's history."   → RR-D2.30
RR-D2.30 MARRICK: "Tell me one thing. When you tell this, and you will, how will you tell it?"
  > "That you fed people, and sold the rest."           → RR-D2.31
  > "That you came to the table and heard it all."      → RR-D2.32
  > "I won't tell it. The record will."                 → RR-D2.33
RR-D2.31 MARRICK: "Fair. Both true. Put the feeding first, if you can bear to."   → end
RR-D2.32 MARRICK: "Oh." (genuinely moved, covers it at once) "Well. That's the part I'd have chosen."   → end
RR-D2.33 MARRICK: "The record. Three copies, I hear." (smiles) "They'll all spell my name right, at least."   → end
      {event: S01 complete when sack also deposited}
```

### RR-D3 — Sedge refuses (`S02_sedge`)

```
RR-D3.01 SEDGE: (cutting reeds; does not look up) "You walked a long way to watch a man cut reeds."
  > "Teach me what you do."                   → RR-D3.10
  > "I wanted to see you were all right."     → RR-D3.20
RR-D3.10 SEDGE: "No."
  > "Why not?"                                → RR-D3.11 {set RR_ASKED_SEDGE_WHY}
  > "All right."                              → RR-D3.20
RR-D3.11 [warm] SEDGE: "Because you'd be good at it. And then they'd need you, and you'd go, every time, until you couldn't."
RR-D3.11 [cool] SEDGE: "Because the water doesn't need two of me. It needs a hundred of them."
RR-D3.12 SEDGE: (nods towards the Vale, the crews, the roll) "It has a hundred of them now. That's better than me."   → RR-D3.20
RR-D3.20 SEDGE: "At the stone. Before it held. What did you see?"
  > "The water stood still in every notch."     → RR-D3.21
  > "Something let go."                         → RR-D3.22
RR-D3.21 SEDGE: "Yes. Remember that, not the rest."            → RR-D3.23
RR-D3.22 SEDGE: "The water went down a hand. Remember that."   → RR-D3.23
RR-D3.23 [warm] SEDGE: "Go on. They're lighting the posts at Whisperflow tonight. I heard." (beat) "I hear most things."
RR-D3.23 [cool] SEDGE: "Go on."
      {event: S02 complete}
```

### RR-D4 — Oriel at the flow-table (`S03_oriel`)

```
RR-D4.01 ORIEL: (at the flow-table; the Cut's scar runs dark and dry) "The Vale said it aloud, in a hall, all at once. I heard of it."
RR-D4.02 [LM_ORIEL_PROMISE = promise_1] ORIEL: "You said to me: '<promise_1 text, Act II>'. You did that."
RR-D4.02 [promise_2] ORIEL: "You said to me: '<promise_2 text, Act II>'. It was done in front of everyone. That counts."
RR-D4.02 [promise_3] ORIEL: "You said to me: '<promise_3 text, Act II>'. Others carried it with you. That was the point."
RR-D4.03 [LM_FEN_ENDING = seal]   ORIEL: (touching the miniature fen, still and dark) "Closed. Kept closed is a kind of work."
RR-D4.03 [tend]                   ORIEL: (a small bright eddy turns at the fen's edge) "Kept open, a little. Someone must walk it."
RR-D4.03 [shared]                 ORIEL: (the deep still; the edge turning) "Both. The hardest to keep. The Vale chose it."
RR-D4.04 ORIEL: "When you cut a tally, what mark do you cut?"
  > "A notch, with a line under it."          → RR-D4.05 {set RR_MARK = notch}
  > "A ring."                                 → RR-D4.05 {set RR_MARK = ring}
  > "Three crossed cuts."                     → RR-D4.05 {set RR_MARK = hatch}
RR-D4.05 ORIEL: (nods once; says nothing about it)
  > "Will you come to Whisperflow?"            → RR-D4.06
  > "Thank you, Oriel."                        → RR-D4.07
RR-D4.06 ORIEL: "No. Rulers have long memories for faces. The Vale has hands enough."   → RR-D4.07
RR-D4.07 ORIEL: "Go carefully on the falls path. The stone is wet. It always is."
      {event: S03 complete}
```

*Writers:* `<promise_n text>` is quoted verbatim from Act II's MQ9 options. If Act II's phrasing makes RR-D4.02's second sentence redundant, cut the sentence, not the quote.

### RR-D5 — Whisperflow at dusk (`S04_lanterns`)

```
RR-D5.01 MAELIN: (at the stone, a lantern unlit at her feet) "Crews cut their marks this morning. As the plan said."
RR-D5.02 MAELIN: (looks at the row of marks; at one in particular) "That one wasn't there this morning."
  > "That's my mark."                          → RR-D5.03
  > "Who cut it?"                              → RR-D5.04
  > (Say nothing.)                             → RR-D5.05
RR-D5.03 MAELIN: "I know." (beat) "Same depth as ours. Same hand, near enough."  → RR-D5.06
RR-D5.04 MAELIN: "Not one of mine." (beat) "Somebody who knew the rule."         → RR-D5.06
RR-D5.05 MAELIN: "Good. Most people talk."                                        → RR-D5.06
RR-D5.06 [LM_PLAN_ROUTES = crews]   MAELIN: "Five posts. One lantern each. Crews take the far three."
RR-D5.06 [keepers]                  HOLLIS: "Five posts, five lanterns. I've counted them twice. Mistress Rowe pretends not to notice."
RR-D5.06 [shared]                   HOLLIS: "Crews take the far three, keepers the near two." MAELIN: "Or the other way." HOLLIS: "...Or the other way."
      {event: light_post_lantern enabled}
```

**Stone inspect (post-MQ12, permanent):** *"The crews' marks, cut fresh beside the notch. And yours, the same depth, the same hand as theirs."* Variant by `RR_MARK`: *"…a notch with a line under it."* / *"…a ring."* / *"…three crossed cuts."*

**Lantern barks**

| Trigger | Speaker | Line |
|---|---|---|
| First lantern | CREW or HOLLIS | "One." |
| Third lantern | HOUSEHOLD (on the high landing) | "Look. They're lighting the line." |
| Fifth lantern | MAELIN | (reads the post) "Water's under the notch. Reads open." (beat) "Get in." |

### RR-D6 — Mid-river (`S05_crossing`)

The crossing is the player's to look at. Maelin says nothing until the ferry passes the halfway post.

```
RR-D6.01 MAELIN: (at the bow, lantern up, not turning round)
RR-D6.02 MAELIN: "I've never crossed here after dark. Not once, in all the years. My teacher didn't either."
RR-D6.03 MAELIN: "It reads true. That's all it ever needed to do." (beat) "Hold the rail."
```

If the player speaks to her during the crossing at any other point: MAELIN: "Watch the water. Not me."

### RR-D7 — The far bank (`S06_far_bank`)

```
RR-D7.01 [LM_GRAIN_ROUTE = escort] HOUSEHOLDER: "That's the one who walked the grain. Make room. Make room on the step."
RR-D7.01 [split]                   HOUSEHOLDER: "Is that the ferry? At night? Somebody fetch the others."
RR-D7.01 [hold]                    HOUSEHOLDER: "We came down. Not many of us. But we came down."
RR-D7.02 NAN: (in her own shawl, Duchess under one arm) "Well. There you are. I've slept in my own bed nine nights running."
RR-D7.03 NAN: "Duchess has laid four. She'd like you to know."
  > "Sing the tune, Nan."                           → RR-D7.04
  > "Was it worth the wait?"                        → RR-D7.06
  > "River keep you, Nan."                          → RR-D7.07
RR-D7.04 [completed side quest VK] NAN: "The whole of it? With the verse back in?" (sings: the listeners' tune, with its missing verse)
RR-D7.05 [completed side quest VK] NAN: (after) "My mam'd be cross it took this long."    → RR-D7.07
RR-D7.04 [else] NAN: (hums it, slow and rising) "There's a verse missing. Always has been. Never mind."  → RR-D7.07
RR-D7.06 NAN: "The bed? Yes." (beat) "The rest? Ask me in spring."   → RR-D7.07
RR-D7.07 NAN: "Go on. She's waiting on you, that one. She never waits on anyone."
```

### RR-D8 — Maelin at the boat (`S06_far_bank`, final node)

```
RR-D8.01 MAELIN: (at the bow, already looking back across the water) "Line reads true both ways."
RR-D8.02 MAELIN: "You read the bank before you read the paper. All the way to the end."
  > "What now?"                          → RR-D8.03
  > "Thank you, Maelin."                 → RR-D8.04
  > (Say nothing.)                       → RR-D8.05
RR-D8.03 MAELIN: "Now I cross back. Then morning. Then more river." (beat) "There's always more river."  → RR-D8.06
RR-D8.04 MAELIN: "Don't." (beat) "...All right."                                                         → RR-D8.06
RR-D8.05 MAELIN: (nods)                                                                                  → RR-D8.06
RR-D8.06 MAELIN: "River keep you." (pushes off; crosses back alone by lantern)
      {set LM_CIVIC_STANDING; event: RR-D8 end → quest Completed}
```

### Optional station dialogue (MQ12)

**RR-D10 — Hesketh**

```
RR-D10.01 [LM_HESKETH = kept] HESKETH: (on the bridge, countersign log under his arm) "I sign second now. I read first. Takes twice as long."
RR-D10.02 [kept] HESKETH: "Best thing that's happened to this bridge in years." (looks at his hands) "They mended."
RR-D10.01 [stood-down] HESKETH: (at the Cut mouth, shovel) "Seal's holding. I count the planks every morning. Old habit."
RR-D10.02 [stood-down, CR_HESKETH_SELF] HESKETH: "I stood myself down. That's the only part of this I'm proud of."
RR-D10.02 [stood-down, else] HESKETH: "Lieutenant's good. Better at asking than I was."
```

**RR-D11 — Tovin at the keepers' hall wall**

```
RR-D11.01 [LM_TOVIN_CREDITED = named] TOVIN: "They put my name on it. 'T. Pell.' I keep reading it in case it's moved."
RR-D11.02 [named, CR_TOVIN_STOOD] TOVIN: "I said one thing in that hall. I keep hearing it. It was all right, wasn't it?"
  > "It was exactly right."                → RR-D11.03
RR-D11.03 TOVIN: (nods several times) "...All right."
RR-D11.01 [unsigned] TOVIN: "Someone pinned one of mine. Nobody knows it's mine." (beat) "That's all right. You know."
RR-D11.04 TOVIN: "The mill floor's dry now. Every morning." (pause) "I still draw it. In case."
```

**RR-D12 — Sallow** `[ANTAGONIST]`

```
RR-D12.01 [CR_CREW_LENIENCY] SALLOW: (at the Cut mouth with a shovel, cheerful) "Look at me. Honest work. Wet feet. Worst of both."
RR-D12.01 [else]             SALLOW: (behind the lock-up grille) "Visiting hours? Lovely. Bring a pie next time."
RR-D12.02 SALLOW: (quieter) "Is it quiet? The fen?"
  > [LM_FEN_ENDING = seal]   "It's closed. Roped off."                → RR-D12.03
  > [tend]                   "It's tended. Lanterns at the edge."     → RR-D12.04
  > [shared]                 "Deep's closed. Edge is tended."         → RR-D12.04
RR-D12.03 SALLOW: (touches the nearest chain or bar) "Good. Good. Keep it shut."   → end
RR-D12.04 SALLOW: (touches the nearest chain or bar) "Lanterns. Right." (beat) "I'll not go and look."   → end
RR-D12.05 [CR_HAULED_CREWMAN] SALLOW: "The lad's on the planks. Learning to swim. In the Cut. Mad."
```

**RR-D13 — Corvin and Aldric (one line each)**

| Speaker | Line | Condition |
|---|---|---|
| CORVIN | "Eighty owed. Eighty paid. First tally I've closed this year that came out even." | `CR_TERMS` full |
| CORVIN | "Eighty owed. She's paying it. Calls it a gift. My tally calls it eighty." | offered |
| ALDRIC | "Fenmere convened. That's all. I'm told it went well." (beat) "I'm told that by everyone except Fenmere." | — |

**RR-D14 — Lessa (Reedmere, morning)**

| Line | Condition |
|---|---|
| (setting her stake back at the Causeway mouth) "That one's done again." | `LM_FEN_ENDING = seal` |
| (knotting a deep path) "Guides only. I said it to the path. It listened, this time." | tend |
| (stake back; a new knot on the boundary rope) "Half done. That's a new one for me." | shared |
| "Your ridge held. My knots. Tell people that." | `SV_LESSA_ROUTE` (extra line) |

**RR-D15 — Ashenstead (Joric, Annelise)**

| Speaker | Line | Condition |
|---|---|---|
| ANNELISE | "We relaid the circle a hand to the left. Nobody minded. The water doesn't come up there now." | `LM_FIELD_FIX = circle` |
| JORIC | (at his plot, planting the ditch banks) "Ditch runs clear. I put something on the banks. It's growing." | plot |
| JORIC | "Fields came in a season late. Both of them. Whole." | dike |
| JORIC | "I decided what this ground is. It's mine to decide. That helps." | completed side quest UR |
| ANNELISE | "I take the baskets to the Step now. People need somewhere, when the door's shut." | `LM_FEN_ENDING = seal` |
| ANNELISE | "Boats on the channel every dusk. I clear them every dawn. Light enough." | tend / shared |
| ANNELISE | (help with one basket, ME04 echo) "Thank you. Not that one. That one stays a day longer." | optional physical beat |

**RR-D16 — Bryn (orchards)**

| Line | Condition |
|---|---|
| "Commons roll. Got a teacher. She's wrong about half of it. I'm wrong about the other half." | `LM_BRYN_ROLL = commons` |
| "Still household. Still mine. Still nobody's bloody business." | household |
| "Not a tree lost. Not one. Turn that gate for me, my back's done." | `LM_ORCHARD_LOSS = none` |
| "Replanted the low section. Whips. Ten years to fruit. I'll be here." | partial |

**RR-D17 — Ansel (Lantern Post)**

```
RR-D17.01 ANSEL: "New book. First page." (holds it out with a pencil) "You write the date. Your hand's steadier than mine today."
RR-D17.02 [completed side quest OL] ANSEL: "First entry's already in: 'Joss's lantern hung.' I wrote that one myself."
RR-D17.03 [LM_FEN_ENDING = seal] ANSEL: "Boundary walk every night. It's very quiet. I'm not used to quiet being good."
RR-D17.03 [tend/shared]          ANSEL: "Channel walk at dusk. Drift drifts. It doesn't do anything. I write it down anyway."
```

**RR-D18 — Elspeth (Reedmere, morning)**

| Line | Condition |
|---|---|
| "Seven came in cold. Seven went home warm. That's a good night's count." | — |
| "Someone cooked. They still talk about it." | `SV_FED_EVACUEES` |

**RR-D19 — Rhosyn (Brookhollow, completed side quest UL)**

| Line | Condition |
|---|---|
| (at a keepers' table with a queue of workers) "Real papers. Stamped. Countersigned. Terribly dull. They're all gate hands now." | `CR_RHOSYN_LAID` |
| (in the cellar, a wink) "Still here. Still good at it. Don't tell anyone you saw me." | not laid |

### MQ12 variant line index

The table collects every MQ12 line keyed to an input flag, so the Schema & Content Engineer can check coverage.

| Flag / condition | Value | Node(s) |
|---|---|---|
| `LM_TL_EVIDENCE` | keepers / riverfolk / player | Hollis barks below |
| `LM_GRAIN_ROUTE` | escort / split / hold | RR-D7.01 |
| `LM_LOCK_STATE` | smashed / chained | Sallow bark below |
| `LM_FIELD_FIX` | circle / plot / dike | RR-D15 |
| `LM_TOVIN_CREDITED` | named / unsigned | RR-D11 |
| `LM_BRYN_ROLL`, `LM_ORCHARD_LOSS` | all | RR-D16 |
| `LM_SEDGE_TRUST` | warm / cool | RR-D3.11, RR-D3.23 |
| `LM_ORIEL_PROMISE` | 1 / 2 / 3 | RR-D4.02 |
| `LM_FEN_ENDING` | seal / tend / shared | RR-D4.03, RR-D12, RR-D14, RR-D15, RR-D17 |
| `LM_HESKETH` (+ `CR_HESKETH_SELF`) | kept / stood-down | RR-D10 |
| `LM_PLAN_ROUTES` | crews / keepers / shared | RR-D5.06 |
| `LM_PLAN_MEMORIAL` | watchers / gardens / reedmere | Memorial bark below |
| `CR_TERMS`, `CR_MARRICK_STORES` | all | RR-D2.01, RR-D13 |
| `CR_CREW_LENIENCY`, `CR_HAULED_CREWMAN` | | RR-D12 |
| `CR_RHOSYN_LAID` | | RR-D19 |
| `RR_MARK` | notch / ring / hatch | Stone inspect |
| completed side quests NT, VK, OL, UR | | RR-D1.04, RR-D7.04, RR-D17.02, RR-D15 |

**Remaining variant barks**

| Speaker | Line | Condition |
|---|---|---|
| HOLLIS (Whisperflow) | "I wrote that one down too. The night crossing. First one in the record." | `LM_TL_EVIDENCE = keepers` |
| HOLLIS | "Mistress Rowe's crews found the second false post too. It's leaning on the crew fire. Nobody'll burn it." | riverfolk |
| HOLLIS | "Do you still have that post? The hall would hang it. Beside Pell's sheets." (option: give it) | player |
| SALLOW | "Smashed my winding floor, you did. Still had dreams about it." / "Cut that chain myself. Should've left it." | `LM_LOCK_STATE` smashed / chained |
| ANSEL / ANNELISE / LESSA (fen edge) | "My patrol, my edge." / "My baskets, my edge." / "Our edge. We live on it." | `LM_PLAN_MEMORIAL` watchers / gardens / reedmere |
| HOUSEHOLD (Crestbridge) | "Marrick's gift, they're calling it." / "Marrick's debt, it says on the sacks." | `CR_MARRICK_STORES` offered / ordered |
| HOUSEHOLD (far bank) | "We were hungry a while. Then we weren't." | `LM_GRAIN_ROUTE = hold` |

---

## Part 6 — Commission offer lines (post-`LM_CIVIC_STANDING`)

Spoken once, on first meeting with the flag set. Each opens the commission package (owned elsewhere); none grants an item.

| Giver | Commission | Line | Condition |
|---|---|---|---|
| BRIGID CORLISS | Keeper's Blade / Bridgewarden Harness | "Hall says you're Crestbridge's now. Hall says a lot. I'll make you a blade if you'll do the work. Or a harness. Or both, if your back's up to it." | — |
| BRIGID | (addition) | "You proved salvage steel at my anvil once. Bring that patience." | completed side quest HS |
| HESKETH | Crestbridge Guard | "Keepers stand in front of things. You stood in front of my hall. Let's make you something to stand behind." | `LM_HESKETH = kept` |
| KEEPER-LIEUTENANT | Crestbridge Guard | "Captain Hesketh asked me to make you an offer. Former Captain. He still says 'my keepers.'" | stood-down |
| HESKETH | (addition, present) | "I asked her to. It's the last order I gave." | stood-down, `CR_HESKETH_SELF` |
| KELL ASHBY | Riverpath Leathers | "Maelin's crews want you kitted proper. I want bark, hide and three weeks of your time. That's the deal." | — |
| KELL | (addition) | "You kept my pits fed when nobody else would. I remember who brought bark." | completed side quest BP |
| MAELIN (bark, any landing) | — | "Kell's cutting you leathers? Good. Crews'll want to see them wet." | after Kell's offer |

---

## Part 7 — Review log (dialogue)

| Check | Result |
|---|---|
| Line length and six-line rule | Checked every node; Hesketh's CR-D9.01–.04 and Marrick's CR-D8 chip answers come in at or under six NPC lines before control returns. Maelin's RR-D6 is her one long line of the act. |
| Marrick never names anyone | Verified across CR-D2, CR-D8, RR-D2. She says "Factor," "my factor," "dear," "the households." |
| `[ANTAGONIST]` tags | Every node naming or voicing Marrick or Sallow: CR-D1.10, CR-D2, CR-D5, CR-D6, CR-D7.04, CR-D8, RR-D2, RR-D12. |
| Tovin canon guard | CR-D8.51–.52 and RR-D11 describe only; no name for the phenomenon; he solves nothing. |
| Anchors | Corvin's ledger regret spoken once (CR-D8.23), content unrevealed. Aldric's shame institutional only. Annelise names no one. Lessa explains the reopening, never the closure. No ages, kinship, service or travel added. |
| Evidence rule | Rejected-object lines (CR-D8.R1–R3); CR-D8.70 mocks the silence; Sedge's lines describe what the water did, never what it means. |
| Address-neutral | No gendered or origin terms for the player. "Friend" (Wynn, Sallow) and "my dear" (Marrick) are character habits used for anyone. |
| Flags match quest file | `CR_*`, `SV_*`, `RR_*`, `LM_PLAN_ROUTES/MEMORIAL`, `LM_FEN_ENDING`, `LM_CIVIC_STANDING`, `LM_HESKETH`, `LM_MARRICK_EXPOSED` cross-checked. |
