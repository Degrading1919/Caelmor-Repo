# Mire Main Act II: Cast and Dialogue (Rowan's Crossing, The Chapel of the Sinking Star)

**Status:** Authored production content for Creative Director milestone review. This is the companion to `04_CONTENT_PRODUCTION/Quests/Caelmor_Mire_Main_Act_II.md`, which owns step ids, flags and mechanics. Characters marked **[CANON ANCHOR]** come from `LORE/Characters/Caelmor_Characters_Region3_Mire_Of_Fallen_Banners_Anchors (Not Full List).txt` and obey the Mire rows of the Part 4 character ledger: nothing here gives them a new age, wartime service, kinship, meeting or record custody. Characters marked **[NEW]** are authored in the Mire bible (§5.2) and are not canon until promoted. Nodes that name Oswin Garvey's causeway decision are tagged `[CAUSEWAY]` (bible §3.1). Nodes that depend on the first-light crossing are tagged `[MD-3]`; nodes that depend on staged drainage are tagged `[MD-4]`. Nothing here is production JSON.

**Node format (writer brief):**
- A line: `ID SPEAKER: "Line." (stage note)`.
- A condition goes in braces before the speaker: `ID {if MR_NAME_RECORD = amended} YSOLDE: "..."`. Several lines may share an id when they are condition variants; exactly one plays.
- Player options are numbered lines under the node: `  1. "Option." → NEXT`. An option with a condition: `  2. {if MCS_VESTRY_READ} "Option." → NEXT`. Player lines are options only; the player never speaks unprompted.
- Effects go in braces after the line: `{set FLAG}`, `{set FLAG = value}`, `{event: ...}`.
- Ids follow bible §11 rule 2: `<CODE>-D<n>.<nn>`. Barks use `-B`, inspect texts `-I`. Option menus return to the node's option list ("→ options") unless stated.

**Voice rules:** bible §5.3 is binding. Plain, heavy and kind; short sentences; seen, then thought; nobody speaks for the dead; nobody calls anything magic; care before explanation; record-keeping is love. Strangers are "traveller"; people who saw the MR-M1 reading say "witness" (Ysolde). No line in this file names a Memorywarden, names an army, gives or implies a count of the dead, explains "Sinking Star", calls a Shade or an Echo a ghost or a soul, or explains how a calm-field works.

---

## Part 1: Act II voice additions

| Item | Status | Use |
|---|---|---|
| **"The grey."** | [NEW] `[MD-3]` Ferry households' word for first light in fog. Rowan does not count it as night: "Grey isn't night. Night's when you can't see your own knots." | Rowan, ferry households. |
| **"Mud's honest."** | [NEW] Rowan's comfort for a wrong call: the boat ran aground, nobody lied, try again. | Rowan. |
| **"Driftwood's honest. It's already been drowned once."** | [NEW] Ferry saying for reclaimed wood. | Rowan. |
| **"Pole the cuts, haul the shoals."** | [NEW] Rowan's route at Slack. | Rowan. |
| **"Lit is held."** | [NEW] The Chapel-Tenders' one rule for lantern lines (bible §1.1: lit = held ground). | Mabyn; Tenders. |
| **"Somebody awake."** | [NEW] The part of lantern craft people forget. | Mabyn. |
| **"The press" / "the shades"** | [NEW] Tenders' words for Chapel Shades. "Only dark that's heavy." Memorykeepers say "impressions". | Mabyn. |
| **"The chapel tells you where the water stood."** | [NEW] Mabyn's teacher's rule for the sluice boards. | Mabyn. |
| **"That's my reading. It isn't a hold."** | [NEW] Memorykeeper form for a link the speaker makes without two holds. | Ysolde. |
| **"Not found is a record too." / "Two holds, one name."** | [NEW, bible] Carried from Act I. | Ysolde. |
| **"Sit. Eat. Then tell it."** | [NEW, bible §5.3 rule 6] | Ysolde, ferry households, Mabyn, Sennic. |

**What nobody in Act II says:** the Memorywardens' names; which armies met on the field; how many went out, came back or died; why the chapel is called the Sinking Star; what the soundless bell is; why the glass lit; that the Shades, the Echoes or the glass are anyone; that the General *is* the wardens' grounding (Ysolde says only that she has set two things side by side); how a calm is laid.

---

## Part 2: Cast notes

### Ysolde Haverel, Memorykeeper [NEW]
- **In MR-M3:** the offer. Has the three day-books open at the register table. Asked Sennic already, and frames his words as his story.
- **In MR-M4:** waits at Blackwater Landing at first light; hears the account; sets the log and the leaves side by side as two holds; makes one link of her own and calls it her reading, not a hold; writes the outcome.
- **Knows:** the register; the day-books' last lines; that Griefwatch talks about "the General" on Bannerline (as talk); that Memorywardens were an old order (history). **Doesn't know:** what stopped the columns, until told; anything about the chapel's interior.
- **Voice:** precise, kind, will not round a number. Separates seen from thought out loud. Calls the player "witness".
- **Guard:** never states a count; never says the General is anyone; calls her link "my reading" twice.

### Rowan Mirewake, Ferryman of the Blackwater Channels [CANON ANCHOR]
- **Canon:** knows the waterways better than anyone alive; refuses night crossings; avoids certain channels; explains why only if pressed gently and repeatedly; reserved, dry-witted, deeply cautious; the only known living guide to the chapel; learned the routes from someone who never returned; treats the church as a place of mourning, not power; grants passage once the player shows restraint.
- **In MR-M3:** refuses twice; sets the player to work; teaches knots; answers three gentle asks over three visits; crosses at the grey `[MD-3]`.
- **In MR-M4:** drops the player at the roof, will not come onto it; returns at first light; one line about the lit line.
- **Knows:** his water; his knots; his teacher's story. **Doesn't know:** what the chapel was for; what is under the altar; what the bell is. **Ledger guard:** no war relation; the teacher is unnamed and dead; no second living guide; his passage proves nothing about the chapel.
- **Voice:** few words, dry, never unkind. Says "traveller" once and then nothing. Answers questions about the chapel's name with "Riverfolk say Church. I say Church."

### Old Sennic Vale, Mire elder and storyteller [CANON ANCHOR]
- **Canon:** remembers the Mire before it sank; childhood stories of the Sunken Church, where mages practised quietly; bells that rang without sound; mages who listened more than they spoke; the church sinking slowly; gentle; fragmented; more lucid about the past than the present; gives *where*, not *why*.
- **In MR-M3:** three sittings, one story each; feeds the player first.
- **Ledger guard:** his stories are leads, never holds. He never explains earth-memory, names a rite, or says what the mages did on the field. Every *where* he gives (bell side faces slack water; the altar under the big window; in by the top) is checked by the player in MR-M4.
- **Voice:** short bursts, then drift. Laughs at himself. Uses "mages" (his childhood word) and "the listeners" (his mother's). Calls the player nothing in particular.

### Mabyn Coyle, Chapel-Tender [NEW]
- **In MR-M3:** meets the boat on the roof.
- **In MR-M4:** keeps the roof line; trades entry for help; teaches "lit is held"; comes down as far as the gallery and no further; holds the top post on the way out; sits the vigil; prays over the record wherever it goes.
- **Want:** the line lit and someone to keep her awake. **Fear:** the dark below the gallery, which she admits.
- **Knows:** lantern craft; that the chapel had drains; her teacher's two rules; the Tenders' story of the seven-night lantern. **Doesn't know:** what is under the altar; which board is first; what the glass is.
- **Voice:** religious, practical, warm, a little bossy. Smells of peat-wax. Gives tea before questions. Never claims a miracle; prefers "people not sleeping". "Seen / thought" when frightened.

### Minor roles (role names only)
| Role | Where | Notes |
|---|---|---|
| Ferry households (a boatwright, a harness-mender, neighbours, a child) | Blackwater Landing | Food, barks, crew alternatives. The boatwright has wanted at Rowan's seams for years. |
| A Chapel-Tender of the memorial gardens | Sorrowmere | Moss crew alternative. |
| The Stillgrave family | Blackwater Landing (morning) | Only with `MR_LANTERN_LINE` (*The Broken Lantern Light*); moss crew-alternative variant. |
| A Memorykeeper runner | Sorrowmere | Lead-in. |

### Barks-only cast (post-quest)
| NPC | Status | Notes |
|---|---|---|
| Calwen Reed-Binder | [CANON ANCHOR] | Records vs. relics; never names a side. |
| Edris Hollowmere | [CANON ANCHOR] | Only hears what is read publicly (`sorrowmere`). Owns her own care ethic only. |
| Oswin Garvey `[CAUSEWAY]` | [NEW] | One line, `sorrowmere` only. |
| Nell Ferrow | [NEW] | One line, `sorrowmere` only. |
| Ferry households, Memorykeepers, Sorrowmere folk | Role-based | Barks. |

---

## Part 3: MR-M3 Rowan's Crossing (`MRC`)

### MRC-B0: lead-in barks

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MRC-B0.0 | MR-M2 Completed | (journal) | "Three columns, one day." |
| MRC-B0.1 | Next entry to Sorrowmere after MR-M2 | MEMORYKEEPER RUNNER | "Witness. Ysolde's asking for you. She's got those books open again." |
| MRC-B0.2 | Near the register room | MEMORYKEEPER | "Three books, one day. She's been at it since the causeway. She won't eat till somebody makes her." |
| MRC-B0.3 | Near the register room | SORROWMERE WOMAN | "Ysolde's frowning at a book. That's either very good or very bad for somebody." |

### MRC-D1: Ysolde at the register table (`S00_offer`)

```
MRC-D1.01 YSOLDE: (three day-books open, each held flat with a river stone) "Witness. Sit, if you like. I've been reading the same three pages since the causeway."
MRC-D1.02 {if MBR_unit_logs held} YSOLDE: "You've still got the books? May I?" (she lays them beside the others' places, each open at its last page)
MRC-D1.02 {if MBR_unit_logs not held} YSOLDE: "They came to my shelf from the causeway chest. Mostly they've been on my table."
MRC-D1.03 YSOLDE: (a finger under each last line) "'Ground will not take a step.' This one stops in the middle of a word. And this one: 'Men sat down.'"
MRC-D1.04 YSOLDE: "Three hands. Three columns. One day. Then nothing. I don't like nothing. Nothing isn't a record."
  1. "What do you think stopped them?"                     → MRC-D1.10
  2. "Who would know?"                                     → MRC-D1.20
  3. {if MR_NAME_RECORD = amended} "How is Nell?"          → MRC-D1.30
  3. {if MR_NAME_RECORD = qualified} "How is Nell?"        → MRC-D1.30
  4. "Where do I go?"                                      → MRC-D1.40

MRC-D1.10 YSOLDE: "I don't think. Not yet." (beat) "Seen: three books stop on one day. Thought: something happened that day bigger than three columns. That's all I've got."   → options

MRC-D1.20 YSOLDE: "I asked the oldest person I know. Sennic Vale, out on the driftwood rise."
MRC-D1.21 YSOLDE: "He says the Sunken Church listened. He says the mages went out from there."
MRC-D1.22 YSOLDE: "That's Sennic's story. I'm not saying it's so. I've written it down as his."
  1. "The Sunken Church?"                                   → MRC-D1.23
  2. "Mages?"                                               → MRC-D1.24
  3. (back)                                                 → options
MRC-D1.23 YSOLDE: "Riverfolk call it that. The Tenders say the Sunken Chapel. In my books it's the Chapel of the Sinking Star. One place. Nobody here knows why the name, and I don't write down guesses."   → options
MRC-D1.24 YSOLDE: "His word. A child's word. There was an old order here once, before the war broke it. History, not a story. What they did out there, nobody's written that I've found."   → options

MRC-D1.30 {if MR_NAME_RECORD = amended} YSOLDE: "She signs both names now. Practises the second one on the backs of my reed strips. I let her."   → options
MRC-D1.30 {if MR_NAME_RECORD = qualified} YSOLDE: "She came by to ask if the page was still dry. It is. Agna came with her to make sure I said so."   → options

MRC-D1.40 YSOLDE: "One person alive knows the way out there. Rowan Mirewake. The ferryman at Blackwater Landing, below us."
MRC-D1.41 YSOLDE: "He'll say no. Go anyway."
MRC-D1.42 YSOLDE: (writing) "'Asked: the witness, to go to the ferryman.'" (blots it) "There. Now it's a record."
      {event: MRC-D1 end → S01; journal: Blackwater Landing}

MRC-D1.90 (resume, before S01) YSOLDE: "Rowan's still at the landing, witness. He hasn't moved in thirty years. He won't have moved today."
```

**Inspect: the day-books (R1)** `MRC-I1.10` "Three regimental day-books, three hands, each open at its last page under a river stone. Ysolde has laid a reed strip in each. No dates. Each day is headed by its weather, and all three run the same: rain, rain, rain, a hard frost, a thaw, fog, fog. Then nothing."
**Inspect: the story shelf (R2, optional)** `MRC-I1.09` "Sennic Vale's stories, written down years ago by a younger Memorykeeper. 'Bells, no sound. Mages, listened. Church, sank slow.' Flat as a list. In the margin, in Ysolde's hand: *Better from him.*"

### MRC-D2: Rowan says no (`S01_no`)

```
MRC-D2.01 ROWAN: (the harness across his knees; he does not look up) "Traveller."
  1. "I need to get to the Sunken Church."                  → MRC-D2.10
  2. "Ysolde sent me."                                      → MRC-D2.05
  3. "What are you mending?"                                → MRC-D2.07

MRC-D2.05 ROWAN: "Ysolde sends everyone. She sent a man with a question about eels once."   → options
MRC-D2.07 ROWAN: "Harness." (lifts a rotted trace; it parts in his hand) "Was."   → options

MRC-D2.10 ROWAN: "No."   {set MRC_REFUSED = 1}
  1. "I can pay."                                           → MRC-D2.20
  2. "Please. It matters."                                  → MRC-D2.20
  3. "Why not?"                                             → MRC-D2.20

MRC-D2.20 ROWAN: "No." (beat) "Boat leaks."   {set MRC_REFUSED = 2}
  1. "Then I'll wait."                                      → MRC-D2.30
  2. "Then I'll help fix it."                               → MRC-D2.30
  3. (Stay. Say nothing.)                                   → MRC-D2.30

MRC-D2.30 ROWAN: (a tilt of the chin toward the shed) "If you're staying, it leaks there."
      {event: objective → "Help at the landing."; S04_ask available; → MRC-D3}
```

### MRC-B1: landing barks

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MRC-B1.1 | Passing the households | FERRY HOUSEHOLD | "Rowan's smiled twice. Once was wind." |
| MRC-B1.2 | First arrival at the landing | FERRY HOUSEHOLD (holding out a bowl) | "Sit. Eat. Rowan won't feed you; he forgets he eats." |
| MRC-B1.3 | At the dock stake | FERRY CHILD (jumping on painted bands) | "You're sour! You're sour! I'm slack, I win." |
| MRC-B1.4 `[CAUSEWAY]` | `MR_CAUSEWAY` = reset | FERRY HOUSEHOLD | "Causeway's quiet since the standards came down. Ferry way's still sour. Oswin says by the long wet. Oswin says." |
| MRC-B1.5 | After `S01` | FERRY HOUSEHOLD | "Nobody goes out to the church but Rowan and the Tender. And now you, by the look of you." |
| MRC-B1.6 | After `S01` | FERRY HOUSEHOLD | "He said no twice? That's friendly. He says it once to me." |

### MRC-D3: help at the landing (`S02_prepare`)

```
MRC-D3.01 ROWAN: (at the shed, one hand on the upturned hull) "Three seams weep. Thwart's cracked. Turn her over, you'll see."
MRC-D3.02 ROWAN: "Harness rotted. Bow lantern's got no wick. And Sennic'll want to talk to you. He wants to talk to everyone. Let him."
  1. "How do I mend the boat?"                              → MRC-D3.10
  2. "And the harness?"                                     → MRC-D3.15
  3. "Where do I find a wick?"                              → MRC-D3.17
  4. "Why Sennic?"                                          → MRC-D3.19
  5. "Some of this is beyond me."                           → MRC-D3.20
  6. "Where do I start?"                                    → MRC-D3.30
  7. {if MRC_REFUSED = 2} "Why won't you cross at night?"   → MRC-D6.01

MRC-D3.10 ROWAN: "Reed from the beds. Long ones, not the brown. Resin warm off my fire. Cold won't take."
MRC-D3.11 ROWAN: "And a new thwart. Root-knee from the driftwood up at Sennic's. Driftwood's honest. It's already been drowned once."   → options
MRC-D3.15 ROWAN: "Traces are gone. There's trade leather in the box. Mire doesn't tan. Too wet to wait for it."   → options
MRC-D3.16 ROWAN: (if asked what it's for) "Shallow bits. You'll see."   → options
MRC-D3.17 [MD-3] ROWAN: "Lantern moss. It only shows itself in the dark. Stillgrave's edge has it. Go at night. On your feet. Not in my boat."   → options
MRC-D3.19 ROWAN: "He's the oldest thing on this water that isn't mud. You'll hear something. Maybe not what you came for."   → options
MRC-D3.20 ROWAN: "Boatwright in the end house. Mender next door. They'll do it. Takes a day. I'm not in a hurry." (beat) "I'm never in a hurry."   → options
MRC-D3.30 ROWAN: "Anywhere. It's all leaking."   → options

MRC-D3.40 (S02 complete) ROWAN: "Boat's whole. Harness is whole. You've a light."
MRC-D3.41 ROWAN: (beat) "And you've let an old man talk."
MRC-D3.42 ROWAN: "Come in daylight. I'll show you the knots."   {event: S02 → S03}

MRC-D3.90 (resume, S01–S04) ROWAN: "Still here. Still leaking, unless you fixed it." (looks) "Did you?"   → options
```

**Crew alternatives (household row, L6):**

```
MRC-D3.21 BOATWRIGHT: "Rowan's boat? I've wanted at those seams ten years. He won't let me." (beat) "He'll let me if you ask. Go on, ask me."
  1. "Will you mend his boat?"                              → MRC-D3.22
  2. "I'll do it myself."                                   → end
MRC-D3.22 BOATWRIGHT: "Morning. Go and sleep. I've got the good resin."
      {event: keep watch to morning; set MRC_HULL_CREW}
MRC-D3.23 (morning) BOATWRIGHT: "Done. Floats. Don't tell him I used the good resin."

MRC-D3.24 HARNESS-MENDER: "Traces? Leave it. Morning."
  1. "Thank you."                                           → MRC-D3.25
  2. "I'll stitch it myself."                               → end
MRC-D3.25 HARNESS-MENDER: (morning) "Stitched it double. He pulls hard, Rowan. For a man who never goes anywhere."
      {event: keep watch to morning; set MRC_HARNESS_CREW}

MRC-D3.26 CHAPEL-TENDER (Sorrowmere memorial gardens): "Moss for Rowan's bow? I'll pick it tonight from the garden posts. You sleep."
  1. "Thank you."                                           → MRC-D3.27
  2. "I'll go to Stillgrave myself."                        → end
MRC-D3.27 CHAPEL-TENDER: (morning) "A jar of it. Keep it damp and it keeps."
      {event: keep watch to morning; set MRC_MOSS_CREW}
```

### MRC-B2: preparation barks

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MRC-B2.1 | Cutting brown reed | ROWAN (from the bench) | "Not the brown. The brown's tired." |
| MRC-B2.2 | Caulking with cold resin | (log) | "Cold resin. It won't take." |
| MRC-B2.3 | Turning the boat (two-person lift) | ROWAN | "Your end. No. Your other end." |
| MRC-B2.4 | The boat floats | ROWAN | "Hm." (He looks at it a long time.) |
| MRC-B2.5 | Harness stitched by the player | ROWAN | "That'll pull." |
| MRC-B2.6 | `MR_LANTERN_LINE`; moss crew alternative chosen | STILLGRAVE FAMILY (morning, at the landing) | "Moss for Rowan's bow. From our ring at the Hollow. You helped us finish it. This is the least of it." {set `MRC_MOSS_CREW`} |
| MRC-B2.7 | Player sets out for Stillgrave by day | ROWAN | "Night. It doesn't show by day. You'll pick weed and call it moss." |
| MRC-B2.8 | Player returns with moss | ROWAN | (He takes a pinch, wets it, wicks the bow lantern.) "Fat. Good." |
| MRC-B2.9 | Woodcutting the root-knee | SENNIC (from his fire) | "That one drowned the year my sister married. Good wood. Bad year." |

**Inspect texts (MRC)**
- `MRC-I1.01` The boat (L2): "A long, flat-bottomed pole boat, black with old resin. Three seams weep. The thwart is cracked through. It has been mended so many times it's mostly mending."
- `MRC-I1.02` The harness (L2): "A tow harness: a chest pad and two traces. Both traces have rotted through. The pad is stuffed with reed fluff gone to dust."
- `MRC-I1.03` The landing stake (L3): {if `MR_CHANNELS`} "A Reedsward stake in three bands. The water stands at the ochre. Slack." (The band named follows the current state.)
- `MRC-I1.04` Knots (L3, before `MRC_KNOTS_READ`): "Reed heads with knots tied in them. Somebody ties these on purpose." (After: per quest file §A8.3.)
- `MRC-I1.05` Reed beds (L4): "Long green reed, good for caulking. The brown is last year's."
- `MRC-I1.06` A root-knee (D2): "A bend of old root wood, grey and hard. It came down the water a long time ago and stayed."
- `MRC-I1.07` Moss on a stilt-stump (S1), night: "Lantern moss, glowing faintly where it is damp." By day: "Moss. Or weed. Hard to tell in daylight."
- `MRC-I1.08` Stillgrave's surface (S3), night: "Too clear. You hold the lantern out over it and its light bends away from the water as if the water didn't want it."
- `MRC-I1.11` The fog bank from Sennic's rise (D3): "The channels run out into a low fog that never lifts. Somewhere in it is the church."

### MRC-D4: sitting with Sennic (`S02_prepare`, sittings)

```
MRC-D4.05 (hour not turned since the last sitting) SENNIC: (asleep by the fire, a slow snore)
  1. (Keep watch by his fire.)                              → {event: keep watch; next hour}
  2. (Leave him.)                                           → end
```

**Sitting one: bells.**
```
MRC-D4.10 SENNIC: (eel in a pot, a stool pushed toward the player with his foot) "Eat first. Then I'll talk. I'll talk either way, but eat."
MRC-D4.11 SENNIC: "Ysolde sent you. She writes me down. I don't mind. It's still mine when she's done."
MRC-D4.12 SENNIC: "Bells. You want bells. Everyone wants bells."
MRC-D4.13 SENNIC: "When I was small. The church had more of its top out of the water. And a bell. My mother said it rang. You'd see the reeds lie down. Round and round, out from it. And not a sound."
MRC-D4.14 SENNIC: "Not a sound. I used to put my hands over my ears to hear it better." (he laughs) "Children."
  1. "Where did the bell hang?"                             → MRC-D4.15
  2. "Why didn't it make a sound?"                          → MRC-D4.16
  3. "Thank you."                                           → MRC-D4.19
MRC-D4.15 SENNIC: "Side by the slack water. The still side. You'd tie up there. Bell side's the quiet side."   → options
MRC-D4.16 SENNIC: "Ask the bell." (he laughs, and then he doesn't) "I don't know why. I know what I saw. Some of what I saw. I was small."   → options
MRC-D4.19 SENNIC: (his eyes closing) "Come back when I'm awake. I'm more awake some hours than others. I was, anyway."
      {set MRC_SENNIC = 1}
```

**Sitting two: the listeners.**
```
MRC-D4.20 SENNIC: "You came back. Eat."
MRC-D4.21 SENNIC: "The mages. That's what we called them. Children's word. My mother said the listeners."
MRC-D4.22 SENNIC: "They'd come to a house where someone had died. Sit. Not say. Listen. Listen more than they spoke. You'd go to bed lighter." (beat) "I don't know how. I know I did."
MRC-D4.23 SENNIC: "They went out from the church, the last time. That's all I know about the last time. That's all anyone told me."
  1. "Where in the church did they keep things?"            → MRC-D4.24
  2. "What did they do, the last time?"                     → MRC-D4.25
  3. "Went out where?"                                      → MRC-D4.26
MRC-D4.24 SENNIC: "Under the big window. By the altar. We weren't let near. Children aren't let near anything good."   → options
MRC-D4.25 SENNIC: "Sat. Listened. I told you." (beat) "I don't know the rest. Don't let anyone tell you I do. Ysolde won't."   → options
MRC-D4.26 SENNIC: (a long look at the fog bank) "Out."   → MRC-D4.29
MRC-D4.29 SENNIC: "Another day. My mouth's tired."
      {set MRC_SENNIC = 2}
```

**Sitting three: the slow sinking.**
```
MRC-D4.30 SENNIC: "Eat. Then the church."
MRC-D4.31 SENNIC: "It didn't fall. People say it went down in a night with everyone in it. It didn't. Slow as a held breath. A step a year."
MRC-D4.32 SENNIC: "My mother marked it on the door with her knife. A notch each spring where the water stood. Then she couldn't reach the door. Then there wasn't a door. You go in by the top now."
MRC-D4.33 SENNIC: "By the top. Remember that. People drown looking for the door."
  1. "Why did it sink?"                                     → MRC-D4.34
  2. "Did you ever go inside?"                              → MRC-D4.35
  3. "Thank you, Sennic."                                   → MRC-D4.39
MRC-D4.34 SENNIC: "Ground's soft. Water's patient. That's all I know. It's enough for me."   → options
MRC-D4.35 SENNIC: "Once. With my mother. She said, be quiet, it's a house of mourning. I was quiet. Only time I ever was."   → options
MRC-D4.39 SENNIC: "That's three. That's all my good ones. The rest are about eels."
      {set MRC_SENNIC = 3}
```

### MRC-B3: Stillgrave's edge at night (MRC-E1)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MRC-B3.1 | Arrival at night | (none) | (Ambience only: drips; frogs; the glow of moss on the stumps.) |
| MRC-B3.2 | First lunge telegraph | (subtitle) | "[The reeds ripple outward.]" |
| MRC-B3.3 | Fifth cluster gathered | (log) | "Enough moss for a bow lantern, and more." |

### MRC-D5: the knots (`S03_knots`)

```
MRC-D5.01 {if hour = dusk or night} ROWAN: "Tomorrow. Daylight."   → end
MRC-D5.02 ROWAN: "Daylight. Good. Sit there. Don't touch the pole."
MRC-D5.03 ROWAN: (ties a knot in a reed head) "One knot. This channel turns at dusk."
MRC-D5.04 ROWAN: (ties two) "Two. Turns at first light."
MRC-D5.05 ROWAN: (ties one, then cuts it through with his thumbnail) "Cut through. Never this season. Don't care what the stake says."
MRC-D5.06 ROWAN: "I tie them. Nobody else. They're for my water. Anywhere else they're just reed."
  1. "And the stakes?"                                      → MRC-D5.10
  2. "Who taught you?"                                      → MRC-D5.15
  3. "Show me."                                             → MRC-D5.20

MRC-D5.10 ROWAN: "Same stakes. I read them my own way."
MRC-D5.11 ROWAN: "Pale's running. Ferries like it. They go with it. My cuts don't. It pours through them like a weir."
MRC-D5.12 ROWAN: "Ochre's slack. Cuts go still. Shoals go dry. We pole the cuts and haul the shoals."
MRC-D5.13 ROWAN: "Black, nobody."   → options
MRC-D5.15 ROWAN: "Somebody who knew."   → options

MRC-D5.20 (practice run one, at the cut mouths) ROWAN: "Two cuts. Read them. Tell me."
  1. "The two-knot cut. Ochre, two knots."                  → MRC-D5.21
  2. "The other one. It's ochre too."                       → MRC-D5.22
MRC-D5.21 ROWAN: "Mm." (poles through)   → MRC-D5.30
MRC-D5.22 ROWAN: (the boat runs softly onto mud; he stands and leans on the pole) "That's mud. Mud's honest." (pushes off) "Again."   → MRC-D5.20

MRC-D5.30 (practice run two) ROWAN: "Noon. Two cuts. Tell me."
  1. "The one-knot cut. It turns at dusk. We'll be back before."   → MRC-D5.31
  2. "The other. Stake's ochre."                            → MRC-D5.32
MRC-D5.31 ROWAN: "Good."   → MRC-D5.40
MRC-D5.32 ROWAN: (aground again) "The stake says yes. I said no." (beat) "Who's been on this water longer?"   → MRC-D5.30

MRC-D5.40 ROWAN: "The grey, then. Tomorrow's. Come at the end of the night and don't talk till I do."
      {set MRC_KNOTS_READ; event: S03 → S05}
```

### MRC-B4: practice barks

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MRC-B4.1 | Second wrong call in one run | ROWAN | "Look at the knot. Not at me. I'm not going to tell you." |
| MRC-B4.2 | Both runs right first time | ROWAN | "Hm." (He nearly says something else. He doesn't.) |
| MRC-B4.3 | Player tries to take the pole | ROWAN | "No." |

### MRC-D6: asking (`S04_ask`, optional)

Available on Rowan's menu from `S01` end until MR-M5 is Active (after MRC completes, through `MRC-L-ROWAN`). An ask counts only if the presentation hour differs from `MRC_LAST_ASK_HOUR`.

```
MRC-D6.01 (menu)
  1. "Why won't you cross at night?" (gentle)               → MRC-D6.10 / .20 / .30 by MRC_ASKED
  2. "Just tell me why you won't go at night."              → MRC-D6.05

MRC-D6.05 ROWAN: "No."   (does not count; nothing else changes)
MRC-D6.06 (hour not turned) ROWAN: "Asked me that already today."   (does not count)

MRC-D6.10 (first) ROWAN: "Can't see the knots."   {set MRC_ASKED = 1; set MRC_LAST_ASK_HOUR}

MRC-D6.20 (second) ROWAN: "Lanterns show you water. Not what it's doing."
MRC-D6.21 ROWAN: (a pause; he works the harness) "Somebody I knew thought a lantern was enough."   {set MRC_ASKED = 2; set MRC_LAST_ASK_HOUR}
  1. (Say nothing.)                                         → end
  2. "I'm sorry."                                           → MRC-D6.22
MRC-D6.22 ROWAN: "Don't be. Wasn't you."

MRC-D6.30 (third) ROWAN: (puts the harness down) "All right."
MRC-D6.31 ROWAN: "The one who taught me this water. She went out one night. Sick child, far channels. Somebody came to the landing in the dark and asked, and she went."
MRC-D6.32 ROWAN: "I was younger than you. I said wait for the grey. She said children don't wait for the grey."
MRC-D6.33 ROWAN: "I found her boat in the morning. Side channel. Pole still in it. Her knots tied all along the way. Every one right."
MRC-D6.34 ROWAN: "So she wasn't wrong about the water." (beat) "She just couldn't see it."
MRC-D6.35 [MD-3] ROWAN: "So. The grey. Not the dark."   {set MRC_ASKED = 3}
  1. (Say nothing.)                                         → end
  2. "Thank you for telling me."                            → MRC-D6.36
  3. "What happened to the child?"                          → MRC-D6.37
MRC-D6.36 ROWAN: (a nod; he picks up the harness)
MRC-D6.37 ROWAN: "Don't know. Nobody wrote it down." (beat) "Ysolde would've."
```

### MRC-D7: the grey (`S05_crossing`) `[MD-3]`

```
MRC-D7.01 ROWAN: (in the boat, the bow lantern lit green-gold in the fog) "Now."
MRC-D7.02 {if the player arrived in the morning} ROWAN: "Late. Still grey. Get in."
MRC-D7.03 ROWAN: "Sit in the bow. Read me the water. Don't talk unless it's water."
MRC-D7.05 (optional, once: "Isn't it still night?") ROWAN: "Grey isn't night. Night's when you can't see your own knots."

MRC-D7.90 (resume, S05) ROWAN: "Grey's still on. Get in."
```

### MRC-D8: calling the water

**Junction one.**
```
MRC-D8.10 ROWAN: (holds the boat on the pole at the cut mouths) "Well?"
  1. "The cut with two knots. Ochre. It's first light."     → MRC-D8.11
  2. "The other cut. It's ochre."                           → MRC-D8.12
  3. "I don't know."                                        → MRC-D8.13
MRC-D8.11 ROWAN: "Mm." (poles on)
MRC-D8.12 ROWAN: "Look at the knot." (he poles them into a side channel) "We wait. Costs the morning a little."   {MRC_WRONG_CALLS +1}
MRC-D8.14 (after the wait) ROWAN: "On."
MRC-D8.13 ROWAN: "Then look till you do. I've got all morning. Most of it."   → MRC-D8.10
```

**Junction two.**
```
MRC-D8.20 ROWAN: (stops; the cut ahead runs fast and pale against its stake) "Well?"
  1. "Go. It's running."                                    → MRC-D8.21
  2. "The side channel."                                    → MRC-D8.22
  3. "Wait. Two knots. It turns now."                       → MRC-D8.23
MRC-D8.21 ROWAN: "It runs. Into the bank." (beat) "Two knots: it turns at first light. It's first light. So we wait for it."   {MRC_WRONG_CALLS +1}   → MRC-D8.24
MRC-D8.22 ROWAN: "Stake's leaning. You know that one. Sour." (beat) "We wait for the cut."   {MRC_WRONG_CALLS +1}   → MRC-D8.24
MRC-D8.23 ROWAN: "That's it." (beat) "That's all it is."   → MRC-D8.24
MRC-D8.24 (the water slides down the stake to the ochre as the light comes up) ROWAN: "On."
```

### MRC-B5: crossing barks

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MRC-B5.1 | The shoal; the boat grounds | ROWAN (handing over the harness) | "Your turn to be a horse." |
| MRC-B5.2 | First haul segment | ROWAN | "Pull on the posts. Not on me." |
| MRC-B5.3 | Haul complete | ROWAN {if `MRC_HARNESS_DONE`} | "Holding. You stitch like you mean it." |
| MRC-B5.3 | Haul complete | ROWAN {if `MRC_HARNESS_CREW`} | "Good stitching. Not yours. Still good." |
| MRC-B5.4 | After the cut, if the player speaks to him | ROWAN | "Mud. It stands up. It sits down. Keep your hands in the boat." |
| MRC-B5.5 | An Echo forms on a bank (once per stretch) | ROWAN | "Bank." |
| MRC-B5.6 | An Echo grips the gunwale | ROWAN | "Off the gunwale. I can't pole with company." |
| MRC-B5.7 | The distant shouting in the cut | ROWAN | "That's not anyone. Don't answer it." |
| MRC-B5.8 | Player defeated in the boat, respawned aboard | ROWAN | "Sit up. We're still going." |
| MRC-B5.9 | `MRC_WRONG_CALLS` ≥ 2 at the roof | ROWAN | "You'll learn. Faster than I did." |

### MRC-B6: Stillgrave (the soundless bell)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MRC-B6.1 | The rings | (subtitle) | "[Silence. The reeds lie down.]" |
| MRC-B6.2 | Player speaks to Rowan within 20 s | ROWAN (not looking round) | "Keep your eyes on the knots." |
| MRC-B6.3 | Player asks him later, at the roof or the landing | ROWAN | "Didn't hear anything." (beat) "That's the truth." |

### MRC-D9: the roof (`S06_roof`)

```
MRC-D9.01 MABYN: (coming down the ridge with a pole lantern) "Rowan. You brought someone." (to the player) "Hand. Mind the moss, it's slick. There."
MRC-D9.02 MABYN: (a cup) "Peat-tea. Drink it before it's cold. It's worse cold."
MRC-D9.03 ROWAN: (holding up the moss bundle) "Moss."
MRC-D9.04 MABYN: "Oh, bless. Look at that. Damp and fat."
MRC-D9.05 MABYN: "Line's been failing since spring. Since the spate. Damp gets in the housings. And I can't keep it alone. The others won't come out since the water came up."
MRC-D9.06 ROWAN: (when the player looks back at him) "Not coming up. Not my place. It's hers."
MRC-D9.10 [MD-3] {if MRC_ASKED = 3} ROWAN: "Morning slack. Not before." (beat) "You know why."
MRC-D9.11 [MD-3] {if MRC_ASKED = 0} ROWAN: "Morning slack. Not before." (beat) "You never asked me about the night. I noticed. Thank you for that."
MRC-D9.11 [MD-3] {if MRC_ASKED = 1 or 2} ROWAN: "Morning slack. Not before." (beat) "You asked, and you left it. I noticed. Thank you for that."
MRC-D9.12 ROWAN: (he poles away into the fog without looking back)
MRC-D9.13 MABYN: "He nearly smiled. Did you see? Don't tell him."
      {set MR_ROWAN_TRUST = told if MRC_ASKED = 3, else kept; event: MRC Completed; MCS Active → MCS-D1.01}
```

### MRC-L-ROWAN: asking after the crossing (optional; until MR-M5 is Active)

```
MRC-L-ROWAN.01 (Rowan's menu at the landing, MRC Completed, MR_ROWAN_TRUST = kept)
  1. "Why won't you cross at night?" (gentle)               → MRC-D6.10 / .20 / .30 by MRC_ASKED
MRC-L-ROWAN.10 (after MRC-D6.35 plays here) {set MR_ROWAN_TRUST = told}
```

### MRC post-quest barks

| Id | Speaker | Line | Condition |
|---|---|---|---|
| MRC-B9.1 | FERRY HOUSEHOLD | "Rowan took somebody out to the church. In the grey. I've not seen that since I was small." | MRC Completed |
| MRC-B9.2 | BOATWRIGHT | "His boat's dry. First time in ten years. He'll never say thank you. I'm saying it for him. Badly." | `MRC_HULL_DONE` |
| MRC-B9.3 | ROWAN (landing, Chapel route) | "Slack. Get in." / at dusk: "Morning." / at night: (he does not answer; he is asleep in the shed) | Chapel route |
| MRC-B9.4 | ROWAN | "She tied a good knot. Better than mine." | `MR_ROWAN_TRUST` = told |
| MRC-B9.5 | ROWAN | "You still haven't asked me. I still notice." | `MR_ROWAN_TRUST` = kept |
| MRC-B9.6 | SENNIC | "Did you see the bell? No. Nobody sees it. You see the reeds." | `MRC_BELL_SEEN` |
| MRC-B9.7 | MEMORYKEEPER (Sorrowmere) | "Ysolde says you went out with Rowan. She's written it. She's very pleased. You can tell because she's frowning less." | MRC Completed |

---

## Part 4: MR-M4 The Chapel of the Sinking Star (`MCS`)

### MCS-D1: Mabyn's trade (`S00_offer`)

```
MCS-D1.01 MABYN: (still holding the cup out until the player drinks) "There. Now."
MCS-D1.02 MABYN: "They said at the landing somebody's been asking about the Sunken Church. Asking Rowan, which is brave."
MCS-D1.03 MABYN: "I won't ask why yet. I'll ask for help. That's the order up here."
MCS-D1.04 MABYN: "Half the line's dark. I can't keep it alone. And I've not been below the gallery since the spate. The water came up inside and I didn't like the dark. I'll say that plainly, so you know."
MCS-D1.05 MABYN: "Help me light it and I'll let you in. That's the trade. It's a fair one. I'm the one who has to live on the roof."
MCS-D1.06 {if MR_LANTERN_LINE} MABYN: "Wait. You're the one who helped at Stillgrave. The family that finished their ring. Then you know what a line's for."
  1. "What's below?"                                        → MCS-D1.10
  2. "Why is it called the Sinking Star?"                   → MCS-D1.20
  3. "Where are the other Tenders?"                         → MCS-D1.25
  4. "I'll help."                                           → MCS-D1.30

MCS-D1.10 MABYN: "Bell-loft. Gallery. Then water. The glass is under it; you can see the colour when the light's right."
MCS-D1.11 MABYN: "What's under that, I don't know. Tenders say a relic. Tenders say a lot of things. I don't dig for sayings."   → options
MCS-D1.20 MABYN: "Nobody knows. The name's older than our book. I don't guess at names. Names are heavy enough."   → options
MCS-D1.25 MABYN: "In Sorrowmere, keeping the garden lines. They'll come back out when the water goes down. Or when I shame them. Whichever's first."   → options
MCS-D1.30 MABYN: "Good. Wicks from your bundle, wax from me. I'll do the ridge with you. The bottom two are in the water. Mind what's in the water."
      {event: S00 → S01}

MCS-D1.80 [MD-3] (any time; "I need to go back to the landing.") MABYN: "Then I'll hang the second lantern on the hook. Rowan sees it at morning slack and comes. Not before." (beat) "Everything stays where you left it. So do I."
MCS-D1.90 (resume, S00–S02) MABYN: "You came back. The line's where you left it. So am I."
```

### MCS-D2: the roof line and the rule (`S01_roofline`)

```
MCS-D2.01 MABYN: (at the first housing) "Open it. Scrape the old wick out, it's rot. Moss in, wax over, light."
MCS-D2.02 MABYN: "Peat-wax. Thick wick. Covered housing." (beat) "And somebody awake. That's the part people forget."

MCS-D2.10 (all six lit; at the hatch) MABYN: "There. Look at that. Held."
MCS-D2.11 MABYN: "Now listen, because I say it once and then I say it every day. Lit is held."
MCS-D2.12 MABYN: "In the dark down there, the shades come. Don't let anybody tell you they're people. They're not anyone. They're only dark that's heavy."
MCS-D2.13 MABYN: "They lean on your light till it goes out. Then they push you back to the nearest lit post. They don't hurt you. They take your time. Down there, time's the thing."
MCS-D2.14 MABYN: (unhooks a small lantern and puts it in the player's hand) "Here. Mine's the pole. This one's spare. Keep it full. Stand by a lit post and it fills."
      {event: carry-state hand lantern}
  1. "Have you seen them?"                                  → MCS-D2.20
  2. "What are they, really?"                               → MCS-D2.21
  3. "Let's go down."                                       → MCS-D2.30
MCS-D2.20 MABYN: "Seen: the dark goes thick at the edge of my light, and my light goes small. Thought: I don't like it. That's all I've got."   → options
MCS-D2.21 MABYN: "Memorykeepers say impressions. Tenders say grief. I say dark that's heavy and a light that's light. Argue with them on your own time."   → options
MCS-D2.30 MABYN: "You first. I'll hold the hatch."   {event: S01 → S02}
```

### MCS-B1: roof barks (MCS-E1)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MCS-B1.1 | Lurker telegraph at a low post | MABYN | "In the water, by the bottom post! I said mind it." |
| MCS-B1.2 | MCS-E1 defeated | MABYN | "Snappers. They like the warm off the housings. So do I." |
| MCS-B1.3 | A post lit | MABYN | "That's one." / "Two." / "Three, and the ridge's half itself again." |
| MCS-B1.4 | `MRC_HULL_DONE` | MABYN | "Rowan's boat's not weeping. You did that? He'll never say. I'm saying." |
| MCS-B1.5 | `MRC_HULL_CREW` | MABYN | "Rowan's boat's dry for once. The boatwright finally got at it? About time." |

**Inspect texts (roof)**
- `MCS-I1.01` The ridge path: "Tiles worn smooth in a path along the ridge. Generations of feet, walking the same few steps between lanterns."
- `MCS-I1.02` A dark housing: "Damp in the housing. The old wick has gone to black string."
- `MCS-I1.03` The landing stage: "Planks pegged to the roof. Rowan's mooring ring, worn bright on one side."
- `MCS-I1.04` The Tenders' chest (T3): "A wooden chest with a peg lock. Spare wicks, a prayer cord, a cake of wax, nothing much. Room in it."
- `MCS-I1.05` The moss jars (T3): "Lantern moss in damp jars. 'Take what you need,' says a scratched note on the shelf."

### MCS-D3: the loft and the gallery (`S02_gallery`)

```
MCS-D3.01 (first loft post lit) MABYN: (from the hatch) "One. Now the other. Don't dawdle in between."
MCS-D3.05 (gallery reached; she climbs down the ladder slowly and lights the gallery post) MABYN: "This far I'll come." (beat) "Below the gallery's yours."
MCS-D3.06 MABYN: "Look at it. Full to the rail. When I was a girl you could see the floor in a dry summer. Not the floor. The shine off the floor."
  1. "The glass is under there."                            → MCS-D3.10
  2. "That's a door, on the side wall."                     → MCS-D3.11
  3. "How do we get down?"                                  → MCS-D4.01
MCS-D3.10 MABYN: "Whole. All of it. I've never seen it out of the water. Nobody living has."   → options
MCS-D3.11 MABYN: "Vestry. Under since before me."   → options
```

### MCS-B2: loft barks

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MCS-B2.1 | First lean | (subtitle) | "[The dark leans on your lantern.]" |
| MCS-B2.2 | First push | MABYN (from the hatch) | "There you are. That's all it does. Fill up and go again." |
| MCS-B2.3 | Second loft post lit | MABYN | "Held. See?" |
| MCS-B2.4 | Player uses the gallery gap | MABYN | "I'll go round. I'm not stepping over anything I can't see the bottom of." |

**Inspect texts (loft and gallery)**
- `MCS-I2.01` The bell frame: "An oak frame and an iron pin where a bell hung. A groove worn into the beam by a rope. No bell. No clapper. Nothing on the floor beneath it."
- `MCS-I2.02` The bell-loft window: "A narrow window on the still side. Below it, slack water and a painted stake on the buttress."
- `MCS-I3.01` The gallery rail: "Initials and small marks cut into the rail. Next to one, someone has cut a lantern."
- `MCS-I3.02` The nave water (required): "Black water to within an arm's length of the gallery. Down in it, where your lantern reaches, colour: blue, then gold, then gone. Glass. Whole, under the water."
- `MCS-I3.03` The vestry door (required): "The top of a door frame, a dark line under the surface on the side wall. The door is somewhere under that."

### MCS-D4: reading the building (`S03_drain`) `[MD-4]`

```
MCS-D4.01 MABYN: "It had drains. Every Tender knows that much. Stone culverts. Wooden boards in them."
MCS-D4.02 MABYN: "The boards rotted shut. Water came in at the top, rain and seep, and had nowhere to go. So it stayed."
MCS-D4.03 MABYN: "My teacher had two rules about the boards. She never used them, so take them for what they're worth."
MCS-D4.04 MABYN: "One: they only work at slack. If the water outside's running, it leans on them. Two: the chapel tells you where the water stood. That's all she said. She liked saying it."
MCS-D4.05 {if MRC_SENNIC = 3} MABYN: "Bell side faces the slack water, your old man says? Then the stake's that side. Bell-loft window."
MCS-D4.05 {if MRC_SENNIC < 3} MABYN: "There's a stake painted on the buttress. You'll find it from one of the windows."
  1. "Which board goes first?"                              → MCS-D4.10
  2. "Where are the boards?"                                → MCS-D4.11
  3. "I'll look."                                           → end
MCS-D4.10 MABYN: "I don't know. If I knew I'd have done it years ago and I'd have a dry floor to pray on."   → options
MCS-D4.11 MABYN: "Windlasses by the windows. Three. Rods go down in the wall to the boards."   → options

MCS-D4.20 (any stain read; optional) MABYN: "Well? What does it tell you?"
  1. {if MCS_STAINS_READ = 3} "The far stain's highest. Then the corner. Then the loft."   → MCS-D4.21
  2. "I'm not sure yet."                                    → MCS-D4.22
MCS-D4.21 MABYN: "Then try it that way. If it's wrong, it's wrong. The chapel's been wrong a long time and it's still standing."
MCS-D4.22 MABYN: "Look again. It's not going anywhere. Neither's the water."
```

**Inspect texts (the stake and the stains)**
- `MCS-I4.01` The buttress stake (G2): "A stake painted on the chapel's own buttress in three bands. The water stands at the ochre. Slack." (Running: "...at the pale. Running.") {if `MRC_SENNIC` = 3} adds: "The bell side faces the slack water. Sennic said so."
- `MCS-I4.02` Outfall B (G4): "Below the window, a culvert mouth stopped with silt. Above it the stone is stained black right up to the string-course under this window."
- `MCS-I4.03` Outfall C (G5): "Below the window, a culvert mouth. The black stain above it stops at the second course of stone."
- `MCS-I4.04` Outfall A (G2): "Below the window, a culvert mouth with a low black band just above it. Barely higher than the water at slack."

### MCS-B3: windlass barks

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MCS-B3.1 | Windlass tried at Running | (log) + MABYN | "The board won't lift. The water outside is leaning on it." / MABYN: "Running. Wait for slack." |
| MCS-B3.2 | Wrong-order board | (log) + MABYN | "The culvert chokes. Water backs up, and the board drops back into its slot." / MABYN: "Not that one. Nothing's broken. Try another." |
| MCS-B3.3 | Board B opened (stage 1 begins) | MABYN | (a roar in the walls) "Oh. Oh, listen to it. Hold the rail!" |
| MCS-B3.4 | Second wrong board | MABYN | "The chapel tells you where the water stood. She said it like that. I've nothing better." |
| MCS-B3.5 | Third wrong board | MABYN | "Look at each mouth from its own window. Highest stain first. That's all she ever told me, I swear it." |
| MCS-B3.6 | Board C opened (stage 2) | MABYN | "Again. It's going. It's going." |
| MCS-B3.7 | Windlass segment interrupted | MABYN | "Stiff. Lean on it. It's been shut longer than I've been alive." |

### MCS-D5: the wait (`S03_drain`, stage 1)

```
MCS-D5.01 (stake turns pale after stage 1) MABYN: "Running till dusk now. That first board let most of it out and the channel's come up to meet it. Come and sit by a lit post."
  1. (Keep watch with Mabyn until dusk.)                    → MCS-D5.05
  2. "Tell me about the Tenders."                           → MCS-D5.10
  3. "How did you come to the roof?"                        → MCS-D5.20
  4. "What's the line for?"                                 → MCS-D5.30
  5. "Does Rowan ever come up?"                             → MCS-D5.40
MCS-D5.05 (dusk) MABYN: "Ochre. There. Go on."   {event: stake → Slack}

MCS-D5.10 MABYN: "We clean bone pits. Light lines. Cook for the grieving. Sit up with people. Nobody's magic. Somebody has to be awake."   → options
MCS-D5.20 MABYN: "My teacher fell asleep on a vigil once. The lantern went out and a family walking home took the wrong path. Nobody was hurt. She never slept on a vigil again."
MCS-D5.21 MABYN: "I came the next spring. I think she wanted somebody to keep her awake. I think I wanted somebody to keep awake for."   → options
MCS-D5.30 MABYN: "So people walking at night know which ground's held. And so somebody coming home sees it from the water." (beat) "Anything else people say about it, they're only saying."   → options
MCS-D5.40 MABYN: "He's been on the roof once. Stood there, looked at the line, went back down. I think it was a compliment."   → options

MCS-D5.90 (resume, S03–S06) MABYN: "Still here. Line's still lit. Down you go."
```

### MCS-B4: stage barks

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MCS-B4.1 | Stage 1 settles | MABYN | "There's the aisle. I'd forgotten there was an aisle." |
| MCS-B4.2 | Stage 2 settles | MABYN | "There's your door. Look. A door." |
| MCS-B4.3 | The glass (§B8.3), when the player next looks up at her | MABYN | "Seen: it lit. Thought: I don't know. That's all I've got." |
| MCS-B4.4 | Stage 3 posts lit | MABYN | "The floor. I can see the floor. Oh, the shine off it." |
| MCS-B4.5 | Player asks her about the glass later | MABYN | "I'm not going to say what it was. I'd only be saying." |

### MCS-B5: fight and floor barks (MCS-E2, MCS-E3)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MCS-B5.1 | Stage 3, the altar comes clear | MABYN | {if `MRC_SENNIC` = 3} "Under the big window. Sennic's right about something." / {else} "There's the altar. Under the big window, where it ought to be." |
| MCS-B5.2 | MCS-E2 burst | MABYN | "Crawlers! Out of the silt. They don't like being woken. Nor do I." |
| MCS-B5.3 | Player fights in dark ground | MABYN | "Get to the light! Fight in the light!" |
| MCS-B5.4 | MCS-E3 start | MABYN | "There's water left in the bays. There's something in it." |
| MCS-B5.5 | An encounter ends | MABYN | "Quiet. Good. I like quiet." |
| MCS-B5.6 | Crawler front hit (first time) | (log) | "Your blow skids off the shell." |

**Inspect texts (the nave)**
- `MCS-I5.01` Stage 1 aisle silt: "Fresh silt, still settling. Something moved under it."
- `MCS-I5.02` A lower bay pool: "Water left in the hollow of the bay. Too dark to see the bottom."
- `MCS-I5.03` The nave floor: "Flagstones. Some are cut with old signs, worn past reading. None of them are names."
- `MCS-I5.04` The altar: "A plain stone altar on a step, under the great window. In the step, a slab with an iron ring."

### MCS-D6: the vestry (`S04_vestry`)

**Inspect texts (vestry)**
- `MCS-I6.01` The field post: "A camp table swollen with water. An ink stone. A cot frame, its canvas gone. A lamp with a broken glass. Nothing else. Somebody tidied before they left, or the water did."
- `MCS-I6.02` The dispatch case (required read in place): "An officer's dispatch case on a high hook, above the old water line. Oiled leather. The mark on its flap has rotted to a pale patch. Inside, a log. The early leaves are pulp. The last ones are clear." {event: document view} {set `MCS_VESTRY_READ`} {if MR-M2 Completed} adds after reading: "Rain, rain, rain, a hard frost, a thaw, fog, fog. The same weather as the three day-books from the causeway chest, and it stops on the same fog. A different hand. A different column."
- `MCS-I6.03` The case, after reading: "You leave it on its hook. It's been there long enough to belong there."

**Document: the vestry regimental log (read in place)**

> *[The unit mark has rotted off the case. The first leaves are pulp. There are no dates: each entry is headed by the day's weather, as the day-books from the causeway chest are.]*
>
> **Rain.** Post moved into the chapel vestry. Dry, for now. The chapel's own people keep a lantern on the roof and asked us to keep our boots off the altar step. Agreed.
>
> **Rain.** The column is on the field of standards. So is the other lot, and the lot behind them, and nobody can go back over the channels.
>
> **Rain.** Nobody can win this ground. Nobody wants it. Captain says hold.
>
> **Hard frost.** Ground like iron in the morning. Men stamping. Nobody moved.
>
> **Thaw.** Mud to the knee by noon. Nobody moved.
>
> **Fog.** Can't see the far lines. The chapel's people came to the post after dark. Asked that nobody fire on anyone walking out at first light without arms. Captain read their paper and said let them. I have written it down so it is written.
>
> **Fog.** Grey light. They went out from the chapel in a line with lanterns and no arms, onto the field. Not ours. Not theirs.
>
> **Fog, later.** Quiet on the field. Not a shot. Not a shout. The men are sitting where they stood. I cannot make them get up. I find I do not want to.
>
> **Fog, dusk.** Some of the chapel's people came back past the post. Not many. They would not be helped. They went down under the big window and shut the stair.
>
> The lantern on the roof is lit.

*Writer note:* no calendar date or year anywhere; the weather run (rain, rain, rain, hard frost, thaw, fog, fog) must stay identical to `MBR_unit_logs` (coordinated with Act I). No unit name, no army, no direction, no number of men, no number of dead. "Not many" is the only quantity word and is not a figure. The log never says what the chapel's people did on the field, only what the soldiers saw.

**Mabyn, from the gallery:**
```
MCS-D6.01 MABYN: (calling down) "What's in there? Talk to me. I'm up here on my own."
  1. "A soldiers' field post. A log."                       → MCS-D6.10
  2. "Later. On the roof."                                  → MCS-D6.30
MCS-D6.10 MABYN: "Soldiers. In our vestry." (beat) "What does it say?"
  1. "The chapel's people went out from here at first light. Lanterns. No arms."   → MCS-D6.11
  2. "The last line says the lantern on the roof is lit."   → MCS-D6.20
  3. "I'll tell you the rest on the roof."                  → MCS-D6.30
MCS-D6.11 MABYN: "Went out where?"
  1. "Onto the field. The log doesn't say more."            → MCS-D6.12
MCS-D6.12 MABYN: (quiet) "Go on. Find what you came for. Tell me the rest after."
MCS-D6.20 MABYN: (a long silence) "The roof." (beat) "Our lantern."   {set MCS_TOLD_MABYN_LANTERN}
MCS-D6.21 MABYN: "Go on. I'll be here. I'm not going anywhere tonight, I don't think."
MCS-D6.30 MABYN: "On the roof, then. I'll hold you to it."
```

### MCS-B7: the glass

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MCS-B7.1 | The glass lights | (subtitle) | "[The glass is lit from behind.]" |
| MCS-B7.2 | The glass goes out | (subtitle) | "[It is only glass.]" |

**Inspect texts (the glass)**
- `MCS-I8.01` The great window, before stage 3 (from the gallery): see `MCS-I3.02`.
- `MCS-I8.02` The great window, after: "Reeds and water. Herons. A ring of low stones under a pale sky. Glass, with black peat pressed against the outside of it. There is nothing behind it to give light."

### MCS-D7: the crypt (`S05_crypt`)

The player is alone. Inspect texts and documents only.

- `MCS-I7.01` The slab: "A slab in the altar step with an iron ring. It lifts." {event: crypt open}
- `MCS-I7.02` The steps: "Dry. Cold. Nobody has walked here since the stair was shut."
- `MCS-I7.03` The box: "A box lined with lead, its lid sealed with a lead strip pressed down by thumbs. The thumbprints are still in it."
- `MCS-I7.04` Inside: "Four clay leaves wrapped in cloth that comes apart when you touch it. Three are fired hard and pale. One isn't fired at all: sun-dried, cracked across." {event: acquire `MCS_warden_leaves`}
- `MCS-I7.05` The marks: "No names on any leaf. In the corner of three of them, the same small mark pressed into the clay. On the cracked one, a different mark, pressed twice. The second time it went crooked."
- `MCS-I7.06` The likeness (optional, MR-M2 Completed): "The pressed mark is like the faint marks on the clay shard from the causeway. Like. You couldn't swear to it." {set `MCS_MARK_LIKENESS`}

**Document: `MCS_warden_leaves` (quest item; four leaves)**

> **Leaf one** *(fired clay; pressed letters; an office mark in the corner)*
>
> From the wardens of memory kept at this house.
>
> The field of standards will not stop. Neither side can win it and neither can leave it. We have sat with the dying of both and we will not sit with more.
>
> We will lay the calm across the field of standards at the turning of the light. The ground will take what we give it. If we cannot carry it, it will carry us.
>
> We go without arms. We go without names. The marks are enough.

> **Leaf two** *(fired clay; the same office mark; broken across one corner)*
>
> To be held on Bannerline while the calm is laid:
> The post stone.
> The low stone by the palisade.
> The split stone.
> The stone that faces the field.
> The stone with the old cut in it.
> *[The list runs on to the broken corner. Whatever followed is gone.]*
> *[Below the break, along the surviving edge:]* and the last stone, which closes it, to be set when the calm is laid.

> **Leaf three** *(fired clay; the same office mark; broken along one side)*
>
> Going out.
> *[A row of pressed marks, close and even, that runs off the broken edge of the leaf.]*

> **Leaf four** *(unfired, sun-dried clay, cracked across; a different hand; a different office mark, pressed twice)*
>
> Come back.
> *[A short row of marks, pressed in a hurry and smeared by a thumb. The crack runs through them.]*
>
> The circle is not closed. We could not.

**Inspect lines on the rows** (document hover or inspect):
- Leaf three: "Marks in a row, close and even. The row runs off the broken edge. Wherever it began is gone."
- Leaf four: "A short row, smeared, with the crack running through it. The marks run together. You can't count them. You stop trying."

*Writer and art note:* no leaf may show a countable row; no inspect line may give or estimate a figure; no leaf names a person, army, battle, or the General; nothing is said about how the calm is laid beyond the wardens' own sentence.

### MCS-B6: the draught (`S06_out`)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MCS-B6.0 | Leaves taken; the breath up the steps | (subtitle) | "[A cold draught pulls past you, up the steps.]" |
| MCS-B6.1 | First post gutters | MABYN (from the hatch, far above) | "There's a wind! Where's a wind come from?" |
| MCS-B6.2 | Player on the aisle walk | MABYN | "Keep coming. Light it and move." |
| MCS-B6.3 | Player stands in the dark more than ~3 s | MABYN | "Don't stop in the dark. Don't stop." |
| MCS-B6.4 | Gallery post gutters | MABYN | "I've got the top. I've got it. It won't go." |
| MCS-B6.5 | Player pushed back | MABYN | "Again. Fill up. Again." |
| MCS-B6.6 | Player on the loft ladder | MABYN | (reaching down) "Hand. Give me your hand." |
| MCS-B6.7 | At the hatch | MABYN | (pulls them up into the air; the draught stops) "There. There. Sit." |

### MCS-D9: the vigil and the record (`S07_vigil`)

```
MCS-D9.01 MABYN: (lighting the last ridge lantern; then a cup, and bread and smoked eel on a cloth) "Sit. Drink. Eat this. It's only bread and eel. Rowan brings it and won't say so."
MCS-D9.02 MABYN: "Then tell it."
  1. {if MCS_VESTRY_READ and not MCS_TOLD_MABYN_LANTERN} "The log in the vestry. Its last line: 'The lantern on the roof is lit.'"   → MCS-D9.20
  2. "Under the altar. Clay leaves."                        → MCS-D9.30
  3. "The glass."                                           → MCS-D9.10

MCS-D9.10 MABYN: "I saw it. I've been a Tender twenty years and I don't know what it was. That's the honest bit. I'm keeping it honest."   → options

MCS-D9.20 MABYN: (very quiet for a long moment)   {set MCS_TOLD_MABYN_LANTERN}   → MCS-D9.21
MCS-D9.21 MABYN: "There's a story the Tenders tell. A lantern on this roof that wouldn't go out. Seven nights after a battle, rain or no."
MCS-D9.22 MABYN: "People say miracle. People say a warden did it as a last thing. I always thought: somebody kept it lit. Peat-wax, a covered housing, and somebody not sleeping."
MCS-D9.23 MABYN: "If your log says it was lit the night they came back past the post..." (beat) "...then the Tenders were waiting for them. That's what it was for. For people who went out."
MCS-D9.24 MABYN: "That's my thought. Not a miracle. I'd rather it was people."   → options

MCS-D9.30 MABYN: "Show me, or tell me. I won't touch them."
  1. (Tell her the leaves: the plan, the stones, the rows, the last leaf.)   → MCS-D9.31
MCS-D9.31 MABYN: "'The circle is not closed. We could not.'" (beat) "Which circle?"
  1. "Somewhere on Bannerline. There's a list of stones."   → MCS-D9.32
MCS-D9.32 MABYN: "Bannerline. Griefwatch's ridge." (she looks out at the dark) "I'll pray for whoever goes up there. I'm not going. I'll keep the light for them."   → MCS-D9.40

MCS-D9.40 MABYN: "Now. Who keeps them?"
MCS-D9.41 MABYN: "You brought them up. The leaves were never ours; we only kept the roof. Say where they go, and I'll pray over them either way."
  1. "Ysolde's people. They'll read them out in Sorrowmere."            → MCS-D9.50
  2. "Back under the altar, where they left them."                      → MCS-D9.60
  3. "The Tenders. You kept the light for them. Keep this too."         → MCS-D9.70
  4. "Let me think."                                                    → MCS-D9.45
MCS-D9.45 MABYN: "Think. The night's long. I'm not going anywhere."   → MCS-D9.40

MCS-D9.50 MABYN: "Sorrowmere. All right. Read them where people can hear."
MCS-D9.51 MABYN: "And bring them back to be read here sometimes. They were under our roof a long while."
      {set MR_WARDEN_RECORD = sorrowmere}   → MCS-D9.80

MCS-D9.60 MABYN: "Back where they left them. All right. We go down now, while the line's lit and the wind's gone."
MCS-D9.61 MABYN: "There's reed paper in the loft. Bring charcoal. Ysolde will want the last one, at least."
      {set MR_WARDEN_RECORD = altar; event: walk the lit line to the crypt with Mabyn}
MCS-D9.62 (in the crypt; the player lays the leaves in the box) MABYN: (a river hymn, low) "Water, take it slow. Ground, take it soft. Light, stay on the roof till the walkers are home."
MCS-D9.63 MABYN: "Rub the last one. Gently. There." {event: carry-state reed-paper rubbing}
MCS-D9.64 MABYN: (they close the slab) "There. Where they left it. Now it's ours to light the way to."   → MCS-D9.80

MCS-D9.70 MABYN: "Us." (beat) "All right."
MCS-D9.71 MABYN: (the player lays the leaves in the Tenders' chest; she pegs it) "I'll read them to anybody Rowan brings. Rowan doesn't bring many. He'll bring the right ones."
MCS-D9.72 MABYN: "I'll pray over them every night. I'm up anyway."
      {set MR_WARDEN_RECORD = tenders}   → MCS-D9.80

MCS-D9.80 MABYN: "Sleep, if you like. I won't. Somebody has to be awake."
      {event: keep watch until first light}

MCS-D9.90 (resume, S07) MABYN: "Sit. The night's long and I've told you everything I know twice."
```

### MCS-D10: first light (`S08_landing`) `[MD-3]`

```
MCS-D10.01 ROWAN: (the boat out of the grey; he looks at the lit ridge a long time) "Line's lit."
MCS-D10.02 MABYN: "It is."
MCS-D10.03 ROWAN: (to the player) "Get in."
MCS-D10.04 {if MR_WARDEN_RECORD = sorrowmere} ROWAN: "Ysolde's on my dock. Since before light. Don't keep her."
MCS-D10.04 {if MR_WARDEN_RECORD = altar} ROWAN: (seeing the rubbing) "Left it where it was." (beat) "Good."
MCS-D10.04 {if MR_WARDEN_RECORD = tenders} ROWAN: "Hers to keep, then." (beat) "Good."
MCS-D10.05 MABYN: (from the ridge, as the boat pulls off) "Come back. Bring somebody. Bring bread."

MCS-D10.10 (optional, during the ride: "Rowan. Why 'the Sinking Star'?") ROWAN: "Riverfolk say Church. I say Church."
MCS-D10.11 (optional, during the ride: "Did you know what was in there?") ROWAN: "No." (beat) "Didn't need to. It was somebody's."
```

### MCS-D11: Ysolde at the landing (`S08_landing`)

```
MCS-D11.01 YSOLDE: (on the dock with bread in a cloth) "Witness. Rowan told the landing when he'd bring you back. I came down early. Sit. Eat. Then tell it."
MCS-D11.02 YSOLDE: (after bread) "Tell it in order. What you saw, then what you think. I'll write the first and keep the second separate."
  1. "In the vestry, a soldiers' field post. A log."        → MCS-D11.10
  2. "Under the altar, clay leaves."                        → MCS-D11.20

MCS-D11.10 YSOLDE: "Whose?"
  1. "The mark's rotted off. A column. Not one of the three from the causeway."   → MCS-D11.11
MCS-D11.11 YSOLDE: "And the weather?"
  1. "Rain, rain, rain. A hard frost. A thaw. Fog, fog. Then it stops."   → MCS-D11.12
MCS-D11.12 YSOLDE: (writing) "'Seen, by the witness: a fourth column's log, the same weather, stopping on the same fog.'" (beat) "What does it say?"
  1. "The chapel's people went out at grey light, in a line, lanterns, no arms. The field went quiet. The men sat down where they stood. Not many came back. They went down under the big window and shut the stair."   → MCS-D11.13
MCS-D11.13 YSOLDE: "'The men sat down.'" (she turns one of her own books to its reed strip) "That's the last line of the third day-book."   → options

MCS-D11.20 YSOLDE: "Leaves?"
  1. "Four. From 'the wardens of memory kept at this house'. A plan: lay the calm across the field of standards at the turning of the light. A list of stones on Bannerline. Marks going out. A short row coming back. And: 'The circle is not closed. We could not.'"   → MCS-D11.21
MCS-D11.21 YSOLDE: "Names?"
  1. "Marks. No names."                                     → MCS-D11.22
MCS-D11.22 YSOLDE: "Memorywardens. The old order. History, not a story." (she writes) "They signed with marks so nobody would ever write them down by name." (beat) "All right. We won't."
MCS-D11.23 YSOLDE: "The marks. Going out, coming back. Did you count them?"
  1. "I couldn't. The leaf's broken, and the last row's smeared."   → MCS-D11.24
MCS-D11.24 YSOLDE: "Good." (beat) "I mean: then we won't write a number. We'll write 'went out' and 'came back' and that it was fewer. That's what's held."   → options
MCS-D11.25 {if MCS_MARK_LIKENESS} YSOLDE: "Like the shard in Calwen's chest? Like isn't same. I'll write 'like'."   → options

MCS-D11.30 (both told) YSOLDE: "The log is one hold. The leaves are another. Two different hands that never met. Two holds. That's an account."
MCS-D11.31 YSOLDE: (writing it in full) "'The wardens went out from the chapel at the turning of the light to stop the fighting on the field of standards. The field went quiet. Fewer came back.'" (beat) "That's what's held."
MCS-D11.32 YSOLDE: "Now my reading. Separate. And you'll let me say it's mine."
MCS-D11.33 YSOLDE: "Griefwatch talks about something on Bannerline that gives orders. Has since the war, they say. They call it the General. I've written that they say so. Nothing more."
MCS-D11.34 YSOLDE: "And the leaves say the circle on Bannerline was never closed."
MCS-D11.35 YSOLDE: "I've put those two side by side. That's my reading. It isn't a hold. Don't let anybody tell you it is. Me included."
  1. "What do we do?"                                       → MCS-D11.36
  2. "I think you're right."                                → MCS-D11.37
  3. (Say nothing.)                                         → MCS-D11.40
MCS-D11.36 YSOLDE: "Today? Write it down. Eat. Then I want to see that ridge with this in my hand."   → MCS-D11.40
MCS-D11.37 YSOLDE: "Think it, then. Write it as a thought. That's allowed."   → MCS-D11.40

MCS-D11.40 {if MR_WARDEN_RECORD = sorrowmere} YSOLDE: (receiving the oilcloth bundle; she does not open it on the dock) "We'll read them on the raised way, where anyone can hear. And I'll start a page in the register. For the ones we hold without names."
      {event: MCS_warden_leaves leaves the pack}
MCS-D11.42 {if MR_WARDEN_RECORD = altar} YSOLDE: (taking the rubbing) "The last leaf. I'll make a reed copy for the register. And I'll go out with Rowan at slack and read the rest myself, under the altar, where they left them."
      {event: rubbing leaves the pack}
MCS-D11.44 {if MR_WARDEN_RECORD = tenders} YSOLDE: "The Tenders hold it. I'll write where it's held and who keeps it. A keeper and a place. That's a hold too."
MCS-D11.45 {if MR_BANNERS = restored} YSOLDE: "Griefwatch is flying the Banner That Sank Twice in its vigil hall. I keep thinking about that. I'm not saying anything. I'm thinking it."
MCS-D11.50 YSOLDE: (blots the page) "There. Written. What was found, what's held, and where."
MCS-D11.51 YSOLDE: "Come and sit at a table tonight. Somebody will be cooking. Somebody always is."
      {event: MCS Completed; MR-M5 armed for next entry to Sorrowmere or Griefwatch}

MCS-D11.90 (resume, after one hour turn; register table) YSOLDE: "Witness. I waited at the landing till the bread went hard. Sit. Tell it."
```

### MCS-L-MABYN: Mabyn, after (optional, chapel roof, post-quest)

```
MCS-L-MABYN.01 MABYN: "You came back. Bring bread? No. Next time."
  1. "How's the line?"                                      → MCS-L-MABYN.10
  2. {if MR_WARDEN_RECORD = tenders} "Read me a leaf."      → MCS-L-MABYN.20
  3. {if MR_WARDEN_RECORD = altar} "Can I go down?"         → MCS-L-MABYN.30
  4. "Goodbye, Mabyn."                                      → end
MCS-L-MABYN.10 MABYN: "Lit. All of it. The others came back out when they heard the floor was dry. I didn't even have to shame them. Much."   → options
MCS-L-MABYN.20 MABYN: (unpegs the chest; reads the first leaf aloud, plainly, to the end) "...'The marks are enough.'" (pegs it again) "There. Read. That's what it's for."   → options
MCS-L-MABYN.30 MABYN: "Line's lit all the way. Go on. Mind the vestry corner; I never put a post in there. The dark sits in it like a cat."   → options
```

### MCS post-quest barks

| Id | Speaker | Line | Condition |
|---|---|---|---|
| MCS-B9.1 | MEMORYKEEPER (raised way, reading aloud to a small crowd) | "'...We go without arms. We go without names. The marks are enough.'" | `sorrowmere` |
| MCS-B9.2 | NELL FERROW (Sorrowmere) | "Ysolde's started a page for people with no names. I nearly was one. I'm going to read it every week so it doesn't get lonely." | `sorrowmere` |
| MCS-B9.3 | EDRIS HOLLOWMERE (Sorrowmere) | "Sat with the dying of both sides, the leaf says. Then they were carers. That's all I'll say about them. It's a lot." | `sorrowmere` |
| MCS-B9.4 `[CAUSEWAY]` | OSWIN GARVEY (Sorrowmere) | "They walked out on that field without a stick between them. And I stood the standards up so nobody'd drive over them." (beat) "I'm not saying it's the same. I'm saying I heard it." | `sorrowmere` |
| MCS-B9.5 | FERRY HOUSEHOLD (landing) | "Rowan took Ysolde out to the church at slack. She came back with charcoal on her face and wouldn't talk till she'd written." | `altar` |
| MCS-B9.6 | FERRY HOUSEHOLD (landing) | "The Tender reads to anyone Rowan brings, they say. Rowan's bringing people. Rowan. Bringing people." | `tenders` |
| MCS-B9.7 | CALWEN REED-BINDER (sanctuary) | "Records go to Ysolde. Relics go in my chest. A box of clay with writing on it is both. I'm glad it wasn't mine to decide." | MCS Completed |
| MCS-B9.8 | ROWAN (landing) | "Line's lit every night now. I can see it from the shed in the grey." | MCS Completed |
| MCS-B9.9 | SENNIC (driftwood rise) | "You went in by the top? Good. People drown looking for the door." | MCS Completed |
| MCS-B9.10 | FERRY HOUSEHOLD (landing) | "They say the drowned get up in the Encampment cut." (Rowan, if near: "Mud.") | MRC Completed |

---

## Part 5: Review notes (dialogue file)

| Check | Result |
|---|---|
| Line length | Every conversation returns options or control within six NPC lines, except Rowan's told story (`MRC-D6.30`–`.35`, six lines) and Ysolde's account (`MCS-D11.30`–`.35`, six lines). Barks are one or two short sentences. |
| Canon anchors | **Rowan:** refuses night crossings (`MRC-D3.17`, `MRC-D7.05`, `MRC-D9.10`); explains only on the third gentle ask on separate visits (`MRC-D6`); pushing gets "No." (`MRC-D6.05`); his teacher "never returned" (`MRC-D6.31`–`.34`), unnamed, no war relation; "Not my place. It's hers." (`MRC-D9.06`) keeps the church a place of mourning; passage proves nothing ("Didn't need to. It was somebody's." `MCS-D10.11`). **Sennic:** three stories (`MRC-D4.13`, `.22`, `.31`); each gives a *where* (bell side, under the big window, in by the top); "I don't know the rest. Don't let anyone tell you I do." (`MRC-D4.25`); never explains. |
| New cast limits | **Ysolde:** two holds; her General link is "my reading. It isn't a hold." (`MCS-D11.35`); refuses to write a number (`MCS-D11.24`). **Mabyn:** does not know what is under the altar (`MCS-D1.11`); never claims a miracle (`MCS-D9.22`–`.24`); admits fear of the dark (`MCS-D1.04`). |
| Evidence rule | R08 rests on the vestry log (read in place) and the leaves (quest item), both required. The bell, the glass, the Shades and the Echoes prove nothing; Mabyn and Rowan decline to explain them (`MCS-B4.5`, `MRC-B6.3`). No defeated enemy speaks. |
| Withheld | No Memorywarden name (office marks only; `MCS-D11.22`). No army or unit (the case's mark rotted; "the column", "the other lot"). No count: leaf three runs off a broken edge, leaf four is smeared and cracked; "You can't count them. You stop trying."; "not many" / "fewer" only. "Sinking Star": "Nobody knows" (Ysolde `MRC-D1.23`, Mabyn `MCS-D1.20`); Rowan: "Riverfolk say Church. I say Church." (`MCS-D10.10`). |
| The General | Named only as what Griefwatch "says" (`MCS-D11.33`), linked only as Ysolde's reading. Not in either record. |
| Nobody speaks for the dead | No "they'd want", no "at peace". Mabyn's "I'd rather it was people" is her own preference. Rowan's teacher is described by what she did. |
| Magic | Nobody calls anything magic. Sennic's "mages" is his child's word, framed by Ysolde (`MRC-D1.24`) as "an old order ... history, not a story". Mabyn: "Nobody's magic. Somebody has to be awake." (`MCS-D5.10`). |
| Address | Ysolde: "witness". Rowan: "traveller" once. Mabyn, Sennic: no title. No name, gender, title or origin for the player. |
| `[MD-3]` tags | `MRC-D3.17`, `MRC-D6.35`, `MRC-D7` (all), `MRC-D9.10`, `MRC-D9.11`, `MCS-D1.80`, `MCS-D10`. |
| `[MD-4]` tags | `MCS-D4` (all) and the stage barks depend on staged drainage; the rule lines (`MCS-D2.11`–`.13`) depend on lantern lines. |
| `[CAUSEWAY]` tags | `MRC-B1.4`, `MCS-B9.4`. |
| Flags | Set here: `MRC_REFUSED`, `MRC_HULL_CREW`, `MRC_HARNESS_CREW`, `MRC_MOSS_CREW`, `MRC_SENNIC`, `MRC_KNOTS_READ`, `MRC_ASKED`, `MRC_LAST_ASK_HOUR`, `MRC_WRONG_CALLS`, `MR_ROWAN_TRUST`, `MCS_VESTRY_READ`, `MCS_TOLD_MABYN_LANTERN`, `MCS_MARK_LIKENESS`, `MR_WARDEN_RECORD`. Set by interactions (quest file): `MRC_HULL_DONE`, `MRC_HARNESS_DONE`, `MRC_MOSS_DONE`, `MRC_BELL_SEEN`, `MCS_OUTER_LIT`, `MCS_STAGE`, `MCS_WRONG_BOARDS`, `MCS_STAINS_READ`, `MCS_GLASS_SEEN`, `MCS_LEAVES_READ`. Read: `MR_CHANNELS`, `MR_NAME_RECORD`, `MR_BANNERS`, `MR_CAUSEWAY`, `MR_LANTERN_LINE`, `MBR_unit_logs` (possession). Matches the quest-file tables. |
| No route, no region | Trade leather has no named origin. No direction to any region. No Lowmark or Thornfell reads. |
| Release wording | None. |
