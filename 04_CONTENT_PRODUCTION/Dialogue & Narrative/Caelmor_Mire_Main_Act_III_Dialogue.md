# Mire Main Act III: Cast and Dialogue (Bannerline)

**Status:** Authored production content for Creative Director milestone review. This is the companion to `04_CONTENT_PRODUCTION/Quests/Caelmor_Mire_Main_Act_III.md`, which owns step ids, flags and mechanics. Characters marked **[CANON ANCHOR]** come from `LORE/Characters/Caelmor_Characters_Region3_Mire_Of_Fallen_Banners_Anchors (Not Full List).txt`; their lines are authored here, and nothing gives them a new age, wartime service, battle, kinship, travel, meeting or record custody (Part 4 ledger). Characters marked **[NEW]** are authored and are not canon until promoted. Nodes naming Oswin Garvey's causeway decision are tagged `[CAUSEWAY]` (bible §3.1); every Hollowfoot node is tagged `[MD-7]`; the post-story refight is tagged `[MD-8]`. Nothing here is production JSON.

**Voice rules:** Mire bible §5.3 is binding: plain, heavy and kind; seen, then thought; nobody speaks for the dead; nobody calls anything magic; water and ground grammar; care before explanation; record-keeping is love; dry humour kept for tables and work. **Address:** people who saw the MR-M1 reading (Ysolde, Edris, Mara, Lysa, Nell, Dunstan, Agna) call the player "witness"; Bran calls them nothing ("you"); Ide calls them "traveller" until the circle is complete and "witness" after; the Thornfell Ridge Wardens call them "walker" (Thornfell voice). Lines are short: at most two sentences per named-character line, at most six NPC lines before a choice or control returns. **Two exceptions, by design:** the reading of the roll (`MBL-D7.10`–`.40`) runs one line per arrival without options, because the reading is the scene; and the arrival lines (`MBL-B7`) play during a hold, not a conversation.

**Node format** (Thornfell and Lowmark dialogue files): `NODE SPEAKER: "Line." (stage note)`, `> [condition] "Option." → NEXT {effect}`. Conditions are written `[FLAG = value]`; effects and events `{set …}`, `{event: …}`. Ids: `MBL-D<n>.<nn>` dialogue, `MBL-B<n>.<n>` barks, `MBL-I` inspect texts, `MBL-R` roll lines, Documents D-1 to D-3. `{PLAYER}` is never used: nobody in this act uses the player's name.

---

## Part 1: Act III voice additions

| Item | Status | Use |
|---|---|---|
| **"Move on two."** | [NEW] Bran's whole teaching of the count. | Bran; Ide; wardens; the player hears it in their head (caption) on the first counts. |
| **"Don't be there on three."** | [NEW] The other half. | Bran, wardens. |
| **"Not tonight's trouble."** | [NEW] Bran on the furrow. | Bran only. |
| **"One we hold, not yet known."** | [NEW] How the roll reads a person with fewer than two holds. | Ysolde; Memorykeepers. |
| **"Held probable."** | [NEW] Ysolde's phrase for a two-hold name that is still a probability (MR-M1). | Ysolde. |
| **"The witness carries it."** | [NEW] The stranger's seat's job at a rite: carry the record in, say what is decided. | Ysolde, Edris. |
| **"Up: three. Down: three."** | [NEW] Griefwatch's road-count after the closure (tended). | Wardens, vigil keepers. |
| **The order** | [NEW] What people call the General's three words. "It gave the order." Never "it said". | Wardens, Bran. |

**What nobody in MR-M5 says:** what the circle did or how; that the General is anyone's ghost or a real commander; which armies stood on the field or how many died; any Memorywarden's name; that the standards lay down "for" anyone; that Hewin's father fell anywhere; that fighting the Hollowfoot helps them; where the Thornfell pair came from or how.

---

## Part 2: Cast notes

### Bran Hollowstep, veteran who never left [CANON ANCHOR]
- **Canon:** survived the Mire's worst years and stayed; does not patrol, watches; quiet, watchful, unmoved by heroics; knows which ground still isn't safe; leaves offerings for no one in particular.
- **In MR-M5:** comes down to Griefwatch at dawn for the first time anyone remembers; teaches the count by hand; points out the furrow; watches the whole rite from the palisade and takes the last stone.
- **Knows:** the count, by feel, from years of sitting on the ridge; which ground will have you. **Doesn't know:** what the General is; what the circle does. Never says he was at the last battle. No theatre, no dates.
- **Voice:** fewest words in the act. Seen, then thought, said bare. Never praises the player.

### Ide Larrow, Marshwarden captain at Griefwatch [NEW]
- **In MR-M5:** rang the closure; opens the road "for people going up to finish something"; holds the road stone first; argues for a vigil at the choice.
- **Voice:** clipped. Treats a closure as a weight she carries. Counts people up and down. "Traveller" until the ring is filled, "witness" after.

### Ysolde Haverel, Memorykeeper [NEW]
- **In MR-M5:** brings the register's pages; checks three names with the player; reads the roll; writes the last line.
- **Knows:** the register; the rule. Her link between the leaves and the ridge is her reading and she says so. **Doesn't know:** why the stranger's seat exists (R16, withheld).
- **Voice:** precise, kind, will not round a number. "Two holds, one name."

### Edris Hollowmere, informal caretaker [CANON ANCHOR]
- **In MR-M5:** takes S2; tells everyone to sit after the strange moment; says they will carry either choice.
- **Guard:** owns her own care; never speaks for the dead or for what the land wants. "The Mire knows when it's respected" is ethics, said at most once, and not as proof.

### Calwen Reed-Binder [CANON ANCHOR]
- **In MR-M5:** takes S4; folds and lays (quieted) or carries down (tended). With `MR_CLOTH = returned` lays the recovered cloth. Never names a side.

### Mara Fenholt [CANON ANCHOR]
- **In MR-M5:** takes S5; chooses the gap stone (quieted). Marks with stones, never names. Never digs deeper than the ground offers: she turfs the laid standards, she does not dig a pit (they are laid in a shallow scrape the households cut).

### Lysa Thornettle [CANON ANCHOR]
- **In MR-M5:** at Griefwatch with people brought down off the crofts and with Jory Wick; guidance about the drifters; takes S9. "Healing is making space."
- **Guard:** present care only. Never says a fight helps anyone.

### Mabyn Coyle, Chapel-Tender [NEW]
- **In MR-M5:** takes S8; with `MR_WARDEN_RECORD = tenders` says the last leaf from memory. Never claims a miracle.

### Rowan Mirewake [CANON ANCHOR]
- **In MR-M5:** `told`: walks up the road (never by water at night) and takes S12. `kept`: keeps the landing lantern lit. Dry.

### Nell Ferrow, Agna Ferrow, Dunstan Hayle [NEW]
- **In MR-M5:** Nell takes S10. Amended: Dunstan beside her at S11. Qualified: Agna at Nell's shoulder; Dunstan across the ring at S3. Agna runs the meal and makes the player sit.
- **Voices:** Nell funny when frightened; Agna sharp ("I did the raising"); Dunstan says less than he means and brings food.

### Oswin Garvey, Reedsward crew-lead [NEW] `[CAUSEWAY]`
- **In MR-M5:** with *Lifting Day* complete, at Edris's shoulder; else at the closure gate with his crew. Tired, decent. One line each place.

### Corra Sallis, Bannerbearer [NEW]
- **In MR-M5:** `MR_BANNERS = restored` only: carries the Banner That Sank Twice up the ridge after the first standard; holds a stone. Earnest.

### Hewin Collard, Marshfall fowler [NEW]
- **Who:** a fowler from Marshfall who came up with the wardens to carry lanterns. His father went up the ridge in the war and did not come down. He does not know where or when beyond that, and nobody tells him.
- **In MR-M5:** asks the General where his father fell. Never answered by it. Searched for at the register: not found, written.
- **Voice:** loud only once. Otherwise apologetic.

### Jory Wick, settled Hollowfoot man in Lysa's care [NEW]
- **Who:** a man who wandered for years and has lived at the Fenward huts for some time. He is the settled man who sorts reeds by length in MR-M1 (Act I `MNS-B6.2`–`.4`, unnamed there; he never spoke in Act I). **Non-combatant, never targetable** (MD-7 dignity rule). No war history is given.
- **In MR-M5:** at Griefwatch, then at Lysa's shoulder at the ring with his hands over his ears through the count. Says very little.

### Thornfell Ridge Warden pair [role names] (`TH_STANDING` only)
- **Who:** two Ridge Wardens visiting Griefwatch, as Ridge Wardens sometimes do [CANON]. **ELDER WARDEN** and **YOUNG WARDEN** (role names). Not named Thornfell cast.
- **Voice:** Thornfell understatement; call the player "walker". One mentions closure accounts once. Neither says where they came from or how.

### Minor cast [role names]
| Role | Voice |
|---|---|
| **Memorykeeper** (Sorrowmere register door) | Brisk, kind. |
| **Marshwardens** | Oilcloth, mud to the knee, wry. |
| **Griefwatch cook** | Generous, bossy. |
| **Vigil keeper** (tended epilogue) | Patient; brings tea. |
| **Griefwatch households** (arrivals) | One line each, plain. |
| **Old Sennic Vale** [CANON ANCHOR] | Table bark only. Gentle, fragmentary; stories, never systems. |

---

## Part 3: MR-M5 Bannerline (`MBL`), Griefwatch and the watchpost

### MBL-B0: the closure (offer)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MBL-B0.1 | Quest start in Griefwatch | (vigil bell) | Three strokes. A rest. Three strokes. (captioned: "The vigil bell. Closure.") |
| MBL-B0.2 | Quest start in Sorrowmere, register room door | MEMORYKEEPER | "Ysolde took the ridge pages up to Griefwatch. She asked for the witness." (beat) "Banners are ochre. You'll have seen." |
| MBL-B0.3 | Sorrowmere raised ways, passing a Bannerbearer on a ladder | BANNERBEARER | "Ochre. Way's shut. Which way? Bannerline. Nobody's said why." |
| MBL-B0.4 | Reaching the closure gate (W1) before `MBL-D1` | IDE | "Road's shut. Hall first, traveller. Ysolde's waiting and she doesn't wait well." |
| MBL-B0.5 | Entering the vigil hall | MARSHWARDEN (by the door) | "Bran was in. Sat on that bench, said four words to Ide and went back up. Four. We counted." |
| MBL-B0.6 | Griefwatch street | GRIEFWATCH HOUSEHOLDER | "Two of them walked into the crofts last night. Drifters. Lysa's got them." `[MD-7]` |

### MBL-D1: Ide and Ysolde in the vigil hall (S00)

```
MBL-D1.01 YSOLDE: (at the long table, register pages weighted with cups) "Witness. Sit. There's tea, it's terrible." (pours it anyway)
MBL-D1.02 IDE: (standing) "Files have come further down the road every night since the chapel. Last night, the Low Bend."
MBL-D1.03 IDE: "Bran came down at dawn. He said, 'It's counting.' Then he went back up."
MBL-D1.04 YSOLDE: "The last leaf says the circle on the crown was never closed." (beat) "Bran says the ridge counts. I put those two together. That's my reading, not the leaves'."
MBL-D1.05 YSOLDE: "So I'll read a roll at the circle. Names only where two keepers stand behind them."
  > "What's the circle?"                                   → MBL-D1.10
  > "Why do you need me?"                                  → MBL-D1.20
  > [MR_BANNERS = restored] (Look at the banner over the door.)   → MBL-D1.30
  > "What's on the road?"                                  → MBL-D1.40
  > "Let's finish the roll."                               → MBL-D1.50

MBL-D1.10 IDE: "Ring of stones on the crown with a gap in it. Griefwatch has always called it a mourning ring that was never done right." (beat) "We leave it be. Left it be."   → MBL-D1 options

MBL-D1.20 YSOLDE: "Three of my names have one hold each. Griefwatch's vigil book might be the second." (beat) "And somebody from outside the lines carries the roll up. That's the seat's job."   → MBL-D1 options

MBL-D1.30 CORRA: (beside it, very straight) "I asked to carry it up. Captain says not yet."
MBL-D1.31 IDE: "Not yet means not yet. Not no."   → MBL-D1 options

MBL-D1.40 IDE: "Echo files. Mud in lines, walking on the count. And drifters, the ones the count's woken." (beat) "I'll open it for people going up to finish something. Not for people going up to look."   → MBL-D1 options

MBL-D1.50 [MR_WARDEN_RECORD = sorrowmere] YSOLDE: (lays a hand on the oilcloth bundle at her elbow) "I brought the leaves. They're going up with us."
MBL-D1.50 [MR_WARDEN_RECORD = altar]     YSOLDE: (touches a reed slip in her sleeve) "The leaves are under the altar. I've the last line, copied. That's enough to read."
MBL-D1.50 [MR_WARDEN_RECORD = tenders]   YSOLDE: "Mabyn's coming. She has the leaves by heart now; she's said them to everyone Rowan brought her."
MBL-D1.51 YSOLDE: "The book's here. Let's find out who we can name."   {event: MBL-D1 end → S01 active}
```

**With *The Bell Roster* (MBO) Completed:** `MBL-D1.03` adds IDE: "Bell went on time. Roster's fixed. One thing in Griefwatch is."

### MBL-D2: checking the roll (S01)

The player reads each register line at the table, opens the vigil book (read in place; Document D-2), turns to a bell-night page and shows Ysolde the match. Each check can be done in any order. A wrong page gets `MBL-D2.90`.

```
MBL-D2.01 YSOLDE: (sliding three register slips across) "Three. Each one's a register line, one hold. If the vigil book holds them too, they're names."
MBL-D2.02 YSOLDE: "If it doesn't, they're read as ones we hold, not yet known. That's not less. It's honest."
  > (Read the slips.)                                      → MBL-D2 checks

-- Check: Hamon Tasker
  > [vigil page 'water-carriers' open] "The vigil book has him. 'Rung down for the water-carriers: Tasker.'"   → MBL-D2.10
MBL-D2.10 YSOLDE: (reads the vigil line herself; then the register slip) "Reed-cutter. Went up with the water-carriers. Rung down for the water-carriers." (beat) "Two holds. Hamon Tasker."   {check_1 done}

-- Check: Lettice Coldridge
  > [vigil page 'water-carriers' open] "Same night. 'Coldridge, the bell-keeper's girl.'"   → MBL-D2.20
MBL-D2.20 YSOLDE: "One line, two people, both named clearly. A line counts for everyone it names." (writes) "Lettice Coldridge."   {check_2 done}

-- Check: Osric Peale
  > [vigil page 'water-carriers' open] "'And a boy.' That's him."             → MBL-D2.30
  > [vigil page 'water-carriers' open] "'And a boy.' Is that enough?"         → MBL-D2.30
MBL-D2.30 YSOLDE: (a long look at the page) "We know a name. We don't know it's his."
MBL-D2.31 YSOLDE: "So he's read as one we hold, not yet known. I'll write Osric Peale beside the vigil line in pencil. If anyone brings a second hold, the pencil goes to ink."
  > "That's hard."                                         → MBL-D2.32
  > (Nod.)                                                 → MBL-D2.33
MBL-D2.32 YSOLDE: "It is. It's still true." → MBL-D2.33
MBL-D2.33 YSOLDE: "His people get to hear 'not yet'. Not 'never'."   {check_3 done}

-- After all three
MBL-D2.40 YSOLDE: (rolls the pages, ties them with reed) "That's the roll. The witness carries it up. That's the seat's job."   {grant MBL_names_roll; event: MBL-D2 end → S02 active}
MBL-D2.41 YSOLDE: "Bran's gone back to his watchpost. He'll want to show you something. He won't say what."

MBL-D2.90 YSOLDE: (wrong page) "That's a bell-night, but it's not them. Try the water-carriers."
MBL-D2.91 YSOLDE: (second wrong page) "Bell-keepers wrote by night, not by name. Look for who went up together."
```

### MBL-D2b: Lysa and Jory in the fold (S01, optional)

```
MBL-D2b.01 LYSA: (a blanket over her arm; Jory on an upturned basket beside her) "Witness. Sit a minute if you're going up. Eat if you haven't."
MBL-D2b.02 JORY: (not looking up) "It's counting."
MBL-D2b.03 LYSA: "It is, Jory. They're going to see to it." (to the player) "He's been saying that since the bell."
  > "The drifters on the road. What should I know?"        → MBL-D2b.10   [MD-7]
  > "Can I help here?"                                     → MBL-D2b.20
  > "Going up."                                            → MBL-D2b.30

MBL-D2b.10 [MD-7] LYSA: "They come at bright and at noise. If you can pass them, pass them."
MBL-D2b.11 [MD-7] LYSA: "If they come at you, they come at you. I'll not tell you different." (beat) "They were somebody's. That's all I'll say about it."   → MBL-D2b options

MBL-D2b.20 LYSA: "Ide's wardens haven't eaten. There's a pot by the hearth wants filling, or the cook's got one that wants carrying."   {S01b_pot offered}
MBL-D2b.21 [A Table for the Wet Completed] LYSA: "The one you made for the wet. That one. It keeps."   → MBL-D2b options

MBL-D2b.30 LYSA: "Come down again. That's the only thing I'll ask."   {event: MBL-D2b end}
```

### MBL-B1: the vigil pot (S01b, optional)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MBL-B1.1 | Player starts cooking at the hall hearth | GRIEFWATCH COOK | "More root than fowl. Wardens don't notice. Don't tell them." |
| MBL-B1.2 | Player takes the cook's pot instead | GRIEFWATCH COOK | "Carry it level. If you spill it on the road I'll know." |
| MBL-B1.3 | Pot delivered at the gate | MARSHWARDEN | "Sit. Eat. Then tell it. That's the rule, and I like the rule." |
| MBL-B1.4 | Same, Thornfell pair present (`TH_STANDING`) | YOUNG WARDEN (Thornfell) | "Hot. Walker, you're a good person." (beat) "Is this root? It's fine. It's root." |

### MBL-D3: Bran at the watchpost (S02)

Bran is sitting on the edge of his broken platform when the player arrives. He gets down without a word, kneels on the turf, and puts his palm flat on it. The node waits until the player does the same (interact *Put your hand on the ground*).

```
MBL-D3.01 BRAN: (palm flat; eyes on the turf) "Wait."
              (beat 1, soft; beat 2, soft; beat 3, deep. The cup on the offering stone jumps.)
MBL-D3.02 BRAN: "Two soft. Then the third."
MBL-D3.03 BRAN: "Move on two. Don't be there on three."
  > "How long has it done that?"                           → MBL-D3.10
  > "What is it?"                                          → MBL-D3.11
  > "Show me."                                             → MBL-D3.12

MBL-D3.10 BRAN: "Since I sat up here. Quiet, mostly. Not quiet now."   → MBL-D3 options
MBL-D3.11 BRAN: "Seen: the ground counts. Thought: something's giving orders." (beat) "That's all I've got."   → MBL-D3 options
MBL-D3.12 BRAN: (nods down at the drill furrow below) "Lane. Something walks it on three. Be in it on one. Be out of it by three."   {event: MBL-E1 active}
```

### MBL-B2: the practice lane (MBL-E1; S02)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MBL-B2.1 | First file forms | (caption, first three counts only) | "one… two… THREE" |
| MBL-B2.2 | First clean count | BRAN | (nothing; he nods once) |
| MBL-B2.3 | Player knocked down on three | (log) | "Mud, and the ground coming up. You're on your back." |
| MBL-B2.4 | Second knockdown | BRAN | "Two. Not three." |
| MBL-B2.5 | Player defeats the file | BRAN | "Hitting it's fine. It comes back." (beat) "The count doesn't stop for you." |
| MBL-B2.6 | Lesson complete | BRAN | "That's it. That's all I know." |

```
MBL-D3.20 BRAN: (at the platform's edge, pointing down into the peat) "Look."
MBL-D3.21 [MDS07_READ] BRAN: "You've seen it. Then you know."
MBL-D3.21 [else]       BRAN: "Something big walks there when there's fighting."
MBL-D3.22 BRAN: "Not tonight's trouble."
  > "What is it?"                                          → MBL-D3.23
  > "Should we go down?"                                   → MBL-D3.24
  > (Look a while longer.)                                 → MBL-D3.25
MBL-D3.23 BRAN: "Don't know. Don't go looking." → MBL-D3.25
MBL-D3.24 BRAN: "No." → MBL-D3.25
MBL-D3.25 BRAN: "We go up at dusk. It comes down in the dark." (sits on his offering stone; waits)   {event: furrow inspected; keep watch available}
MBL-D3.30 BRAN: (at dusk, getting up) "Gate."   {event: MBL-D3 end; night pin begins}
```

**Inspect: offering stone** "A bent spoon. A ribbon gone grey. A heel of bread, fresh. Nothing says who for." / after dusk, with the player's own bread in their pack: *(option)* "Leave some bread." → "You leave it. Bran doesn't look."

### MBL-D4: Ide at the closure gate (S03)

```
MBL-D4.01 IDE: (hand on the bar) "Bran says you've got the count." (beat) "Have you?"
  > "Move on two."                                         → MBL-D4.10
  > "I think so."                                          → MBL-D4.10
MBL-D4.10 IDE: "Good enough. Wardens come up behind you and hold what you've walked. We don't go first. That's yours."
MBL-D4.11 [TH_STANDING] ELDER WARDEN (Thornfell): "We'll take the far bend, walker. We've stood a few." (beat) "Not in this. Mud's new."
MBL-D4.12 [MBL_POT] MARSHWARDEN: "And we've eaten. Ask me anything."
MBL-D4.13 IDE: (unbars the gate) "Up you go, traveller. Bring the roll back down."   {event: MBL-D4 end; gate open}
```

`[CAUSEWAY]` **Oswin at the gate** (only without *Lifting Day* Completed): OSWIN: "Crew's here if anything wants carrying. We're good at carrying. It's the other thing we're bad at." (bark `MBL-B3.0`, plays as the gate opens)

### MBL-B3: the road (S03)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MBL-B3.0 | Gate opens; without *Lifting Day* | OSWIN `[CAUSEWAY]` | "Crew's here if anything wants carrying. We're good at carrying. It's the other thing we're bad at." |
| MBL-B3.1 | Reaching the Low Bend | MARSHWARDEN (behind) | "Two lanes. Cross on two. If you can't, hit it and cross after." |
| MBL-B3.2 | Same, `MBL_POT` | MARSHWARDEN | "Fed and frightened. Better than hungry and frightened." |
| MBL-B3.3 | Player crosses a lane cleanly | (log) | "Three. Mud where you were standing." |
| MBL-B3.4 | First view of the Rag Bend hollow `[MD-7]` | MARSHWARDEN | "Keep to the road. They're in the rags." |
| MBL-B3.4a | Hollowfoot shouter, when struck `[MD-7]` | HOLLOWFOOT SHOUTER | "Close up! Close up!" (then wordless) |
| MBL-B3.4b | Hollowfoot wanderer, aggro `[MD-7]` | HOLLOWFOOT WANDERER | "Who's there? Who's that?" |
| MBL-B3.5 | After MBL-E3, if fought `[MD-7]` | MARSHWARDEN | "Keep to the road. Lysa'll want to know where they were." |
| MBL-B3.6 | MD-7 swap only: player sits with the survivors | (log) | "You sit in the rags. After a while one of them gets up, and then the others, and they walk down toward the wardens' fire." `[MD-7]` |
| MBL-B3.6a | MD-7 swap only: survivor, walking past | HOLLOWFOOT SURVIVOR | "Is it done counting?" `[MD-7]` |
| MBL-B3.7 | Reaching the Iron Bend, `TH_STANDING` | ELDER WARDEN (Thornfell) | "Three lanes. In Thornfell we'd blow Fall. Here you just step." |
| MBL-B3.8 | Iron Bend cleared | IDE (arriving behind) | "Held. Go on. Palisade's above you." |
| MBL-B3.9 | Agility shortcut taken | MARSHWARDEN | "Show-off." (beat) "Mind the lane at the top." |

### MBL-B4: the ridge's standards (S04)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MBL-B4.1 | First view of the palisade | (log) | "Standards on every stake. Most of them standing clear, cloth moving. There's no wind." |
| MBL-B4.2 | Player lacks the Woodcutting level, or chooses the crew | MARSHWARDEN (with a bow-saw) | "Stand off. Two counts. Keep them off me." |
| MBL-B4.3 | Stake cut by the player | MARSHWARDEN | "Clean. Lift it." |
| MBL-B4.4 | First fold | (log) | "Strongest seam. Hem. Hoist. Your hands remember it." |
| MBL-B4.5 | Wrong fold | (log) | "The cloth slides open. Start at the strongest seam." |
| MBL-B4.6 | Wraiths form | MARSHWARDEN | "The risen! On three!" |
| MBL-B4.7 | Second standard folded | (log) | "On the third beat, the mud at the muster post moves." |
| MBL-B4.8 | Third standard folded | (log) | "The third beat lands at the post now. Mud is standing up there." |

### MBL-D5: Corra brings the banner (S04; `MR_BANNERS = restored` only)

Plays after the first standard is folded. Corra comes up the road with two Bannerbearers and the Banner That Sank Twice on its pole.

```
MBL-D5.01 CORRA: (out of breath, very straight) "Captain said not yet. Then she said now."
MBL-D5.02 CORRA: "Where does it go?"
  > "Down at the circle. By the road stone."               → MBL-D5.10
  > "Keep it back. It's not safe."                         → MBL-D5.11
MBL-D5.10 CORRA: "By the road stone." (goes; stands it there; every risen cloth along the arc turns toward it at once)   → MBL-D5.20
MBL-D5.11 CORRA: "I know. I'll put it by the road stone and stand there." (goes)   → MBL-D5.20
MBL-D5.20 BANNERBEARER: "They've answered it. Every one." (beat) "We'll hold the far end."   {event: MBL-D5 end; extra wave armed at standard 3; ally line active}
```

---

## Part 4: Documents

### Document D-1: `MBL_names_roll` (quest item) [NEW]

Reed paper, several sheets tied with a reed. Ysolde's hand, very even. Inspect shows the header and the first lines; the lines below are the ones read at the ring (`MBL-R`), and the later sheets are shown only as more of the same hand. No line states or implies a total, and the `R` ids are production ids, never shown to the player.

> **NAMES BELOW. For reading at the circle on Bannerline.**
> *From the field of standards and the ridge. Two holds, one name. The rest held, not yet known.*
>
> MBL-R1: [MR_NAME_RECORD = amended] *Aldith Hayle, of Marshfall, mother of Dunstan and of Linnet. Held probable.* (Name as in the Hayle book, MR-M1.)
> MBL-R1: [MR_NAME_RECORD = qualified] *One we hold, not yet known. Found by the Standards road, with a child's tape in her sleeve.*
> MBL-R2: *Hamon Tasker, reed-cutter, of Sorrowmere.*
> MBL-R3: *Lettice Coldridge, of Griefwatch, the bell-keeper's girl.*
> MBL-R4: *One we hold, not yet known. A boy who carried water.* (pencil, beside: *Osric Peale?*)
> MBL-R5: *Bettony Larch, peat-cutter, of Marshfall.*
> MBL-R6: *One we hold, not yet known. Two who wore the same stitched mark and lay together.*
> MBL-R7: *Gil Stannard, ferry hand, of the Blackwater.*
> MBL-R8: *Cicely Ashlin, of Rootrest, who kept the root-house.*
> MBL-R9: *One we hold, not yet known. Found under the palisade, with a spoon.*
> MBL-R10: *Garret Mossop, carter on the Standards road, of Sorrowmere.*
> MBL-R11: *Annet Brigge, of Griefwatch.*
> MBL-R12: *Those who went out from the chapel, by their marks. Held. Not yet known.*
>
> *Read by Y. Haverel, Memorykeeper. Carried by the witness.*

(Every named person is a civilian of the Mire's own settlements. No army, unit, side or Memorywarden is named. The tape, the stitched mark and the spoon are objects, not identities. R12 covers the leaves' tally marks without a number.)

### Document D-2: Griefwatch's vigil book, the water-carriers' page [NEW]

Read in place at the vigil-hall table. A bell-keeper's hand, cramped, one line per bell-night; no year written, only "the last wet" at the head of the page (the season of the Act I day-books and the Act II vestry log; the two fog nights below are the end of their weather run, unstated).

> *Bell-night. Fog. Ridge loud all day. Rung up for the water-carriers going up at noon.*
> *Bell-night. Fog. Ridge quiet. Very quiet. Nobody rung down.*
> *Bell-night. Rung down for the water-carriers: Tasker. Coldridge, the bell-keeper's girl. And a boy.*
> *Bell-night. Rung for nobody. Rang it anyway.*

(The second line is the day the fighting stopped; nothing says so. The fourth is the vigil Griefwatch has kept since.)

**Inspect: the vigil book (cover)** "Bell-keepers' lines, one a night, for longer than anyone in Griefwatch has been alive. Later pages are in many hands." / with *The Bell Roster* Completed: "The newest pages are in the fixed roster hand. Every night has a name beside it now."

### Document D-3: the register's closing line (`S08`, written by Ysolde) [NEW]

> *Read at the circle on Bannerline, which is* **closed** [quieted] / **kept** [tended]. *Every stone stood.*
> *Witness: the stranger's seat.*
> *Asked after: Collard, father of Hewin, of Marshfall. Not found. Asked.*

---

## Part 5: The crown

### MBL-I: inspect texts on the crown (S04–S06)

| Object | Text | Condition |
|---|---|---|
| Palisade stake | "Old timber, iron-red at the foot where the soil has stained it. Rope marks worn into the wood." | any |
| A risen standard | "Standing clear of the stake, cloth lifting and falling. No wind. The cloth's device is gone to rot; you couldn't say whose it was." | before the strange moment |
| A laid standard | "Flat on the turf, folded or not. Still." | after |
| The muster post | "Tall, iron-shod. A crossbar worn smooth by hands, at a height for calling from." | any |
| The muster post (after `S05`) | "Mud round its foot, drying. The count still comes up through it, softer." | `S05`–`S06` |
| A circle stone | "Waist high, lichened. Old." | any |
| One of the five listed stones (S3, S5, S7, S9, S11) | "Waist high. The post stone." / "The low stone by the palisade." / "The split stone." / "The stone that faces the field." / "The stone with the old cut in it." (Ysolde, if asked: "That's on the leaves. By its place. That's all the leaves say of it.") | `MR_WARDEN_RECORD = sorrowmere` or `altar` (her copy names them) |
| One of the five listed stones | Same place-names. (Mabyn, if asked: "That one's on the list. I've said it often enough to know it.") | `tenders` |
| Any other stone | "Waist high. Not on what's left of the list." | any value, after a listed stone is inspected |
| The footing stone (gap) | "A flat stone set in the turf where a thirteenth should stand. Wet. The mud from the post has soaked into it." | `S05`–`S06` |
| Iron soil | "Red ground. A tarnish serpent lies on it in the last warmth and does not move for you." | any |
| The Banner That Sank Twice | "Stood by the road stone, on its old pole. Corra's hand on it." | restored |
| The landing lantern (from the gap) | "Far down, one point of light where the Blackwater must be." | `MR_ROWAN_TRUST = kept` |

### MBL-B5: the General (MBL-E6; S05)

It has three words. Nothing else it does is speech.

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MBL-B5.0 | Coheres at the muster post | (log) | "Mud, iron and rag stand up out of the ground into the shape of someone in command. The shape won't settle." |
| MBL-B5.1 | P1, on third beats | THE GENERAL | "Hold." |
| MBL-B5.2 | P2, on third beats | THE GENERAL | "Close up." |
| MBL-B5.3 | P3, on third beats | THE GENERAL | "No one leaves." |
| MBL-B5.4 | Shield up, player strikes | (log) | "Mud plates take the blow. Clods spray. The files are still holding." |
| MBL-B5.5 | Shield down | (log) | "The plates slough off into the grass." |
| MBL-B5.6 | Player in the swept lane | (log) | "The pole comes down the whole lane." |
| MBL-B5.7 | Player dies | IDE (distant) | "Get them down. Gently." |
| MBL-B5.8 | 30%: rags at the edge | (log) | "Banner rags stand up all round the crown's edge, thick as reeds. Nothing stops you walking through them." |
| MBL-B5.9 | 0 HP | (log) | "It goes down into the ground. The mud slides down the lane into the gap in the ring and soaks into the stone there. Under your feet: two soft. Then the third, quieter." |

### MBL-D6: the asker (S05, at the 65% re-muster)

The General stands at the post, invulnerable, re-mustering (~8 s). Hewin breaks from the wardens' line below the palisade and runs up the Post Lane. The player can talk to him (one line) or step into the lane between him and the post. On timeout Ide reaches him.

```
MBL-D6.01 HEWIN: (shouting, running) "Where did my father fall? You were here. Tell me where."
MBL-D6.02 THE GENERAL: "Hold."
MBL-D6.03 HEWIN: "Tell me where!"
  > [talk prompt on Hewin] "It can't tell you. We can look in the books."   → MBL-D6.10  {set MBL_ASKER = answered}
  > [enter interposition volume] (Stand between them.)                     → MBL-D6.11  {set MBL_ASKER = stood}
  > [timeout]                                                               → MBL-D6.12  {set MBL_ASKER = wardens}

MBL-D6.10 HEWIN: (stops dead) "...Books." (walks back down the lane without looking at it again)
MBL-D6.11 HEWIN: (stops behind the player; looks at their back, not at it) "...All right. All right."
MBL-D6.12 IDE: (has him by the coat) "Not here. Not from that." (pulls him back to the line)
MBL-D6.13 THE GENERAL: "Close up."   {event: P2 begins}
```

```
MBL-D6.20 BRAN: (at the palisade, after it goes down; hand on a stake) "It'll stand up again tonight." (beat) "Unless."
MBL-D6.21 YSOLDE: (coming up the road head with a lantern) "The leaves said the circle's not closed. So we close it." (beat) "Witness. The roll."   {event: MBL-D6 end → S06 active}
```

### MBL-D7: the rite (S06)

**Opening** (before the hold; the player gives the roll to Ysolde at S7):

```
MBL-D7.01 YSOLDE: (takes the roll; unties the reed) "Thank you."
MBL-D7.02 [MR_WARDEN_RECORD = sorrowmere] YSOLDE: "From the Names Below, and from the leaves the Wardens left." (unwraps the oilcloth; reads the last leaf) "'The circle is not closed. We could not.'"
MBL-D7.02 [MR_WARDEN_RECORD = altar]     YSOLDE: "From the Names Below. The leaves stay where Mabyn put them. I've the last line." (reads the reed slip) "'The circle is not closed. We could not.'"
MBL-D7.02 [MR_WARDEN_RECORD = tenders]   MABYN: (at S8 when she arrives, or at the road head if not yet) "I'll say it. I've said it often enough." (beat) "'The circle is not closed. We could not.'"
MBL-D7.03 YSOLDE: "We can." (to the player) "Kneel at the gap. Hand on the stone. Step off when it says three's coming."
MBL-D7.04 EDRIS: (from below, at the road head with the first lanterns) "We're coming up. Hold it open for us, witness."
  {event: hold available; MBL-E7 active}
```

**The roll** (read by Ysolde from S7, one line per arrival interval through segments 2 and 3; texts from Document D-1, `MBL-R1`–`R12`):

```
MBL-D7.10 YSOLDE: (to the ring, not loud) "Names Below. Two holds, one name. The rest held, not yet known."
MBL-D7.11 YSOLDE: (MBL-R1, amended) "Aldith Hayle, of Marshfall. Mother of Dunstan and of Linnet. Held probable."
            (stage: Dunstan, at S11, looks at Nell. Nell holds his sleeve.)
MBL-D7.11 YSOLDE: (MBL-R1, qualified) "One we hold, not yet known. Found by the Standards road, with a child's tape in her sleeve."
            (stage: Dunstan, across the ring at S3, looks at the ground. Agna's hand on Nell's arm.)
MBL-D7.12 YSOLDE: (MBL-R2) "Hamon Tasker, reed-cutter, of Sorrowmere."
MBL-D7.13 YSOLDE: (MBL-R3) "Lettice Coldridge, of Griefwatch, the bell-keeper's girl."
            (stage: a Griefwatch householder at a household stone, if any, bows her head; else Ide does.)
MBL-D7.14 YSOLDE: (MBL-R4) "One we hold, not yet known. A boy who carried water."
MBL-D7.15 YSOLDE: (MBL-R5) "Bettony Larch, peat-cutter, of Marshfall."
MBL-D7.16 YSOLDE: (MBL-R6) "One we hold, not yet known. And one we hold, not yet known. Two who wore the same mark."
MBL-D7.17 YSOLDE: (MBL-R7) "Gil Stannard, ferry hand, of the Blackwater."
            (stage, MR_ROWAN_TRUST = told: Rowan, at S12, nods once.)
MBL-D7.18 YSOLDE: (MBL-R8) "Cicely Ashlin, of Rootrest, who kept the root-house."
MBL-D7.19 YSOLDE: (MBL-R9) "One we hold, not yet known. Found under the palisade, with a spoon."
            (stage: Bran, at the palisade, looks toward his watchpost.)
MBL-D7.20 YSOLDE: (MBL-R10) "Garret Mossop, carter on the Standards road, of Sorrowmere."
MBL-D7.21 YSOLDE: (MBL-R11) "Annet Brigge, of Griefwatch."
MBL-D7.40 YSOLDE: (MBL-R12; the last line, read as segment 3 completes) "Those who went out from the chapel, by their marks. Held. Not yet known."
            (She rolls it. She does not say "that's all". Everyone is looking at Bran.)
```

(If the hold is paused, the reading pauses at the next line break and resumes with the hold. The reading never outruns the arrivals and never ends before segment 3.)

**The strange moment and after:**

```
MBL-D7.50 (Bran sets his palm on S6. Two soft beats. The third does not come. Silence. The standards lean, one after another round the ring, toward whoever stands nearest, and lie down. No wind. No line for about five seconds.)
MBL-D7.60 EDRIS: "Sit a minute. Everybody."
            (people sit down where they stand; Agna on Nell's arm, slowly; Jory takes his hands off his ears)
MBL-D7.61 [optional: talk to Bran] BRAN: "Seen: they lay down." (beat) "Thought: I've nothing."
MBL-D7.62 [optional: talk to Ide] IDE: "Witness." (that's all; it's the first time she's used it)
MBL-D7.63 [optional: talk to Hewin; MBL_ASKER = answered] HEWIN: "You said books. I'm holding you to books."
MBL-D7.63 [optional: talk to Hewin; MBL_ASKER = stood]    HEWIN: "You stood in front. I'd have kept asking it. All night."
MBL-D7.63 [optional: talk to Hewin; MBL_ASKER = wardens]  HEWIN: "I shouldn't have run up. Ide's got a grip on her."
   {event: MBL-D7 end → S07 active when the player talks to Ysolde or after 20 s}
```

### MBL-B7: arrivals at the stones (S06)

Each person walks up from the road head with a lantern, sets a hand on their stone, and says one line. Lines play only while the gap is held. Stone assignment is the quest file §8.2.

| Id | Stone | Speaker | Line | Condition |
|---|---|---|---|---|
| MBL-B7.0 | S1 | IDE | (already there) "Road stone. Wardens hold the road. That's all we're for tonight." | always |
| MBL-B7.0a | S1 (shoulder) | ELDER WARDEN (Thornfell) | "We keep a closure account at home now. Who's outside." (beat) "You keep one for who didn't come home. Same chalk, different wall." | `TH_STANDING` |
| MBL-B7.0b | S1 (shoulder) | HEWIN | (quiet) "I'll just stand here." | always |
| MBL-B7.1 | S2 | EDRIS | "I won't tell you this mends anything. I'll tell you we came." | always |
| MBL-B7.1a | S2 (shoulder) | OSWIN `[CAUSEWAY]` | "I stood them up. I'll stand here." | *Lifting Day* Completed |
| MBL-B7.2 | S4 | CALWEN | "All the same once they hit the mud." (beat) "All the same up here." | always |
| MBL-B7.2a | S4 | CALWEN | (lays the folded cloth at the foot of the stone) "Came home off a jetty. Lie down." | `MR_CLOTH = returned` |
| MBL-B7.3 | S5 | MARA | "Ground's ready." (that's all) | always |
| MBL-B7.4 | S7 | YSOLDE | (already there with the roll) | always |
| MBL-B7.5 | S8 | MABYN | "Tenders kept a lantern seven nights for people off this field. I'll keep one more." | always |
| MBL-B7.6 | S9 | LYSA | "Making space. That's all this is." | always |
| MBL-B7.6a | S9 (shoulder) | JORY | (hands over his ears) "It's counting." | always |
| MBL-B7.6b | S9 (shoulder), after the count stops | JORY | (lowers his hands; nods to the player, the way he held out a reed at Fenward) | `MNS_FENWARD_VISITED` |
| MBL-B7.7 | S10 | NELL | "I'm terrified. Agna says that's fine." / [amended] "I'm terrified. Dunstan says that's a family trait." | by `MR_NAME_RECORD` |
| MBL-B7.7a | S10 (shoulder) | AGNA | "Wet ground. I'm here anyway. Write that." | qualified |
| MBL-B7.8 | S11 | DUNSTAN | (hands Nell a heel of bread; says nothing; takes his stone) | amended |
| MBL-B7.8a | S3 | DUNSTAN | (from across the ring, to nobody) "She's there. That's enough for tonight." | qualified |
| MBL-B7.9 | S3/S11/S12 | CORRA | "I carried it all the way up. My arms are shaking. I'm fine." | `MR_BANNERS = restored` |
| MBL-B7.9a | S3/S11/S12 | CORRA | (adds) "You gave me the corner, on the causeway. I've not forgotten." | `MR_BANNERS = restored`, `MBR_CORRA_CORNER` |
| MBL-B7.10 | S12 | ROWAN | "Walked. Up a hill. At night." (beat) "Don't tell anyone." | `MR_ROWAN_TRUST = told` |
| MBL-B7.10a | (from the gap, looking down) | (log) | "Far below, the landing lantern is lit." | `MR_ROWAN_TRUST = kept` |
| MBL-B7.11 | household stone | GRIEFWATCH HOUSEHOLDER | "Thirty years we rang the bell for this ridge. Now we're stood on it." | any household stone |
| MBL-B7.11a | household stone (second) | GRIEFWATCH HOUSEHOLDER | "My gran rang for the water-carriers. I'll stand for her." | second household stone |
| MBL-B7.12 | lanterns | STILLGRAVE FAMILY (eldest) | "We finished ours. We'll light yours." | `MR_LANTERN_LINE` |
| MBL-B7.13 | S6 (last) | BRAN | (walks down from the palisade; no line) | always |

**Hold barks:**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MBL-B7.20 | Player releases the gap | (log) | "You step off. Up the road, the lanterns stop and wait." |
| MBL-B7.21 | File passes through the gap | (log) | "Three. It walks through the gap and comes apart on the grass inside the ring." |
| MBL-B7.22 | Player held through three | BRAN (from the palisade) | "Two." |
| MBL-B7.23 | Segment 3, second file forms | IDE | "Two lanes now! Watch the left!" |
| MBL-B7.24 | Player strikes a file down from the gap | (log) | "It comes apart in the lane. Four counts before it stands again." |

### MBL-D8: how Bannerline is left (S07)

At the ring, after the quiet. Ysolde, Edris, Mara, Ide and Calwen near the gap; Bran at S6.

```
MBL-D8.01 YSOLDE: "Somebody from outside the lines says it. That's what the seat's for. Then we all carry it."
MBL-D8.02 EDRIS: "Whatever you say, we'll carry. I won't tell you it's easy either way."
MBL-D8.03 MARA: (nodding at the palisade foot) "The gap'll take a stone. I've seen the one. No mark on it. It doesn't need one."
MBL-D8.04 IDE: "Or leave it a step. Somebody stands in it every night." (beat) "Griefwatch has stood a vigil for thirty years without knowing what for. We'd know."
MBL-D8.05 [MR_BANNERS = retired]  CALWEN: "The cloth's tired. Lay it in the ground and let it rest. Or carry it down and I'll make it something people can look at."
MBL-D8.05 [MR_BANNERS = restored] CALWEN: "Corra's banner's up at Griefwatch. These could go up here in our colours. Or down. Cloth doesn't mind."
  > "Close it. A stone in the gap; the standards in the earth."     → MBL-D8.20  {set MR_BANNERLINE = quieted}
  > "Keep it. A step in the gap, and a vigil."                      → MBL-D8.30  {set MR_BANNERLINE = tended}
  > "Bran?"                                                         → MBL-D8.10
  > [MR_BANNERS = restored] "Corra?"                                → MBL-D8.11
  > "Ysolde, what would you do?"                                    → MBL-D8.12

MBL-D8.10 BRAN: "Either way I'll watch it."   → MBL-D8 options
MBL-D8.11 CORRA: "I'd carry them. Every one. Up or down." (beat) "Up, if you're asking."   → MBL-D8 options
MBL-D8.12 YSOLDE: "I'd write down what you say. That's what I do."   → MBL-D8 options

-- Quieted
MBL-D8.20 MARA: (walks to the palisade foot; puts her hand on a fallen footing stone) "This one."
MBL-D8.21 IDE: "Wardens. Roll it." (to the player) "I'll take the slate off the gate in the morning."
MBL-D8.22 CALWEN: (folding the first of the fallen standards) "Lie down. You've stood long enough."
MBL-D8.23 [MR_BANNERS = restored] CORRA: (lifting the Banner That Sank Twice) "I'll take this one home, then." (beat) "On my own. It's fine."
MBL-D8.24 EDRIS: "Then it's closed." (beat) "Down, everybody. Agna's cooking and she'll come up here if we're late."   {event: S07 end}

-- Tended
MBL-D8.30 IDE: (takes a mattock from a warden; cuts a step into the footing stone, ankle-deep; it takes a while; nobody helps and nobody leaves)
MBL-D8.31 IDE: "There. Somebody stands in that every night." (beat) "Starting tonight. I'll do the first."
MBL-D8.32 CALWEN: "Bring them down. I'll make them something people can look at."
MBL-D8.33 [MR_BANNERS = restored] CORRA: "Grey and green and ochre. Like the street." (beat) "I'll carry them back up."
MBL-D8.34 EDRIS: "Then it's kept." (beat) "Down, everybody but Ide. Agna's cooking and she'll come up here if we're late."   {event: S07 end}
```

---

## Part 6: The table at Sorrowmere (S08)

### MBL-D9: the meal and the register

```
MBL-D9.01 AGNA: (at the long table; points at a bench with a ladle) "Sit."
  > (Sit.)                                                         → MBL-D9.02  {event: forced seat}
  > "I should tell Ysolde—"                                        → MBL-D9.03
MBL-D9.03 AGNA: "You've stood all night. Ysolde can wait for a bowl. Sit." → MBL-D9.02
MBL-D9.02 AGNA: (puts a bowl in front of the player; nobody asks anything) "Eat."
MBL-D9.04 AGNA: "I did the raising. I'll do the feeding." (beat) "Then you can all cry, I don't mind."
MBL-D9.05 (Table barks MBL-B9 play while the player sits. Standing up ends them.)
```

**Remembrance** (register room, after the player stands):

```
MBL-D9.10 YSOLDE: (the Names Below open on its stand) "Lay it on the page, witness."
  > (Lay the roll on the register.)                                → MBL-D9.20  {remove MBL_names_roll}
MBL-D9.20 [MR_BANNERLINE = quieted] YSOLDE: (writes; reads it as she writes) "Read at the circle on Bannerline, which is closed. Every stone stood. Witness: the stranger's seat."
MBL-D9.20 [MR_BANNERLINE = tended]  YSOLDE: (writes) "Read at the circle on Bannerline, which is kept. Every stone stood. Witness: the stranger's seat."
MBL-D9.21 [MR_STRANGER_SEAT] (Ysolde rests her hand on the back of the stranger's seat for a moment. She says nothing about it.)
MBL-D9.30 [MBL_ASKER = answered] HEWIN: (at the door, cap in his hands) "Witness said books."
MBL-D9.30 [else]                 YSOLDE: (seeing Hewin at the door) "Come in. You asked something on the ridge. We can look in the books."
MBL-D9.31 YSOLDE: (searches; a long time; the player can watch the pages) "Collard. Marshfall. Not found."
MBL-D9.32 HEWIN: "Right."
MBL-D9.33 YSOLDE: (writes) "Asked after: Collard, father of Hewin. Not found. Asked." (to Hewin) "Not found is a record too. You're on the page now, asking."
MBL-D9.34 HEWIN: "...That's more than I had."
MBL-D9.40 AGNA: (from the doorway) "Now eat the rest."   {set MR_STANDING; quest → Completed}
```

### MBL-B9: table barks (S08)

| Id | Speaker | Line | Condition |
|---|---|---|---|
| MBL-B9.1 | NELL | "Dunstan brought bread. He always brings bread. We're going to have to talk about the bread." | amended |
| MBL-B9.1a | NELL | "Agna, sit down, you've been on wet ground." / AGNA: "I'll sit when I'm dead." / NELL: "Don't." | qualified |
| MBL-B9.2 | DUNSTAN | (passes the player the bread; nods) | any |
| MBL-B9.3 | ROWAN | "I don't climb. I want that known." | told |
| MBL-B9.3a | ROWAN | "Saw the lanterns go round. Kept mine lit." | kept |
| MBL-B9.4 | OSWIN `[CAUSEWAY]` | "Edris says I can walk the causeway first next spring." (beat) "She said 'maybe'." | *Lifting Day* Completed, `MLD_ORDER` ≠ first |
| MBL-B9.4b | OSWIN `[CAUSEWAY]` | "Walked it first. Crews behind me. Nobody went in." | *Lifting Day* Completed, `MLD_ORDER` = first |
| MBL-B9.4a | OSWIN `[CAUSEWAY]` | "Crew carried every lantern back down. Didn't drop one." | without *Lifting Day* |
| MBL-B9.5 | CORRA | "My arms still hurt. Is that normal? Calwen says it's normal." | restored |
| MBL-B9.6 | MABYN | "No miracles. Just a lot of people walking up a hill." | any |
| MBL-B9.7 | MARA | (eating; to nobody) "Good stone." | quieted |
| MBL-B9.7a | MARA | (eating) "Ide'll be cold. Somebody take her a bowl." | tended |
| MBL-B9.8 | OLD SENNIC VALE | "They say it's quiet up there. I'll believe it when I've slept a night on it." | any |
| MBL-B9.9 | YOUNG WARDEN (Thornfell) | "We'll stay for the soup. Then back to our own hills, walker. They'll want to hear it." | `TH_STANDING` |
| MBL-B9.10 | LYSA | "Jory slept on the walk down. First time in a week." | any |
| MBL-B9.11 | EDRIS | "The Mire knows when it's respected. That's not a fact. That's how I try to live." | any |

---

## Part 7: Epilogue barks (by place and state)

All per-player; keyed on the quest file §E tables.

| Id | Place | Speaker | Line | Condition |
|---|---|---|---|---|
| MBL-B11.1 | Bannerline crown | (inspect, the new stone) | "A little greyer than the others. No mark. Somebody has left a heel of bread on it." | quieted |
| MBL-B11.2 | Bannerline crown | (inspect, the mound) | "A low green mound inside the ring. Turf, settled." | quieted |
| MBL-B11.3 | Bannerline crown | VIGIL KEEPER | "Up: three. Down: three. That's the road tonight. I've had worse." | tended |
| MBL-B11.4 | Bannerline crown, taking a vigil at midnight | VIGIL KEEPER | "Tea. It's terrible. Ysolde taught me." | tended |
| MBL-B11.5 | Bannerline crown, player approaches the muster post at night | VIGIL KEEPER `[MD-8]` | "You're going to hit that. I'll step off the gap. Put it back down when you're done." | tended |
| MBL-B11.6 | The muster post, night `[MD-8]` | (inspect) | "Strike the post. The count will answer." | any |
| MBL-B11.7 | The muster post, after a Night Count | (log) `[MD-8]` | "It goes back into the ground at the post's foot. The ground is still." | any |
| MBL-B12.1 | Griefwatch gate | IDE | "Road's open. I keep looking at it." | quieted |
| MBL-B12.2 | Griefwatch gate | IDE | "Road's open, and watched. That's the closure I wanted." | tended |
| MBL-B12.3 | Griefwatch vigil hall | CORRA | "I take it down and air it on feast days. It doesn't stand up by itself any more. I check." | restored |
| MBL-B12.4 | Griefwatch vigil hall | GRIEFWATCH HOUSEHOLDER | "Ide's teaching the bell-keepers' children their letters. Says we need something to do now." | quieted |
| MBL-B12.5 | Griefwatch street | JORY | (waving at someone going up the road) "It's stopped counting." | any |
| MBL-B13.1 | Bran's watchpost | BRAN | "Nothing to watch. I'll watch it anyway." | quieted |
| MBL-B13.2 | Bran's watchpost | BRAN | "Stood the gap Tuesday. Cold." | tended |
| MBL-B13.3 | Bran's watchpost, asked about the furrow | BRAN | "Still there. Still not tonight's trouble." | any |
| MBL-B14.1 | Sorrowmere register room | YSOLDE | "The water-carriers are in the children's circle now. 'Say whose story it is.' They say mine." | any |
| MBL-B14.2 | Sorrowmere long table | AGNA | "Sit." | any |
| MBL-B14.3 | Sorrowmere register room | YSOLDE | "Somebody brought a second hold for a pencil name last week. It went to ink. Not the boy. Somebody." | any (after a long absence) |
| MBL-B15.1 | Marshfall | HEWIN | "Not found. It's written. That's more than I had." | any |
| MBL-B15.2 | Marshfall, Dunstan's table | HEWIN | "Dunstan's teaching me the book. You write what you know and what you don't." | `MBL_ASKER = answered` |
| MBL-B15.3 | Marshfall | DUNSTAN | (shows the player the Hayle book: Nell's name beside Linnet's; says nothing) | amended |
| MBL-B15.3a | Marshfall | DUNSTAN | (shows the ribbon at Linnet's page) "Hers to say. Not mine." | qualified |
| MBL-B16.1 | Fenward | LYSA | "He sleeps through now. Two more walked down off the ridge after it stopped. Making space." | any |
| MBL-B17.1 | Blackwater Landing | ROWAN | "Walked up a hill at night. Don't tell anyone." | told |
| MBL-B17.2 | Blackwater Landing | ROWAN | "Saw your lantern go round the ring. I kept mine." | kept |
| MBL-B17.3 | Sunken Chapel roof | MABYN | "...and then it was finished, by people who came up the road. That's the end of the reading now." | `MR_WARDEN_RECORD = tenders` |
| MBL-B17.4 | Sunken Chapel altar | MABYN | "One prayer for the circle. Short. They'd had enough long ones." | altar |
| MBL-B17.5 | Sorrowmere reading stand | (inspect, the leaves in their oilcloth) | "A reed slip tucked into the oilcloth, Ysolde's hand: *Closed.*" / "*Kept.*" | sorrowmere, by `MR_BANNERLINE` |

---

## Part 8: Mire master commission offer lines (first meeting with `MR_STANDING`)

The offer opens a commission; it grants nothing (quest file §E.10).

| Giver | Line | Variant |
|---|---|---|
| **Hob Merrit** (fowler's reed bow and quiver) | "Stood on a ridge all night and didn't shoot a single heron. Come and make a bow worth that kind of patience." | *Reed Shafts* Completed: "That heron's still out there. Laughing." |
| **Rowan Mirewake** (root-wood pole) | "A pole's a root that agreed to be straight. Find one that agrees." | told: "I'll show you where the good root is." / kept: "There's root. Find it." |
| **Ide Larrow** (Marshwarden's oilcloth coat) | "Wardens' coat. Imported hide, our oilcloth, mended till it's ours. You've earned the mending." | tended: "For the vigil. It's cold on that stone." |

---

## Part 9: Review notes (dialogue file)

| Check | Result |
|---|---|
| Line length and the six-line rule | Every conversation returns options or control within six NPC lines, except the roll (`MBL-D7.10`–`.40`, by design) and arrivals (`MBL-B7`, during a hold). |
| Voice (§5.3) | Plain and short. Seen/thought (Bran `MBL-D3.11`, `MBL-D7.61`). Nobody speaks for the dead: no "she'd want", "at peace", "for them" beyond "I'll stand for her" (a living person's own act). Nobody calls anything magic: the General is "it", "the order", "mud"; the circle is "closed" or "kept". Care before explanation: Ysolde's tea, Lysa's "eat if you haven't", Agna's meal before the register. Record-keeping as love: the pencil-to-ink rule; "You're on the page now, asking." Humour at tables and work only. |
| Address | "Witness" from those who saw the reading; Bran never addresses the player by any word; Ide moves from "traveller" to "witness" at `MBL-D7.62`; the Thornfell pair says "walker". No `{PLAYER}`. |
| The General | Three words only (`MBL-B5.1`–`.3`, `MBL-D6.02`, `.13`). Never answers Hewin. Never named as a ghost or a commander by anyone. |
| Canon anchors | Bran: no battle, theatre or date; knows the count by feel and unsafe ground; "Don't know. Don't go looking." Edris: her own care and ethics, the respect line framed as how she lives, not proof. Calwen: no side named. Mara: chooses a stone, no mark, no digging. Rowan: walks up by road; never crosses water at night. Lysa: present care; no fight as cure. Sennic: one bark, what he saw. |
| Evidence rule | Roll from register + vigil book; the boy stays "not yet known" on one hold. The General, the files and the Hollowfoot give nothing. |
| R08 withholds | No army, unit, side, Memorywarden name or casualty figure in any line or document. "Those who went out from the chapel, by their marks" has no number. |
| Tags | `[CAUSEWAY]`: `MBL-B3.0`, `MBL-B7.1a`, `MBL-B9.4`, `MBL-B9.4a`, Oswin's cast note. `[MD-7]`: `MBL-B0.6`, `MBL-D2b.10`–`.11`, `MBL-B3.4`–`.6a`. `[MD-8]`: `MBL-B11.5`–`.7`. |
| Thornfell independence | Two optional ally lines and one table bark with `TH_STANDING`. No route or direction to Thornfell is stated ("back to our own hills"). |
| Names | New names checked against the repository for collisions: Hewin Collard, Jory Wick, Hamon Tasker, Lettice Coldridge, Osric Peale, Bettony Larch, Gil Stannard, Cicely Ashlin, Garret Mossop, Annet Brigge (no existing use). |
| Flags | Every flag set here (`MBL_ASKER`, `MR_BANNERLINE`, `MR_STANDING`) and every item effect (`MBL_names_roll` granted at `MBL-D2.40`, removed at `MBL-D9.10`) matches the quest file §9.2. |
| Batch 4 encounter alignment review, 2026-11-09 | `MBL-B0.2` drops "at first light": Ysolde meets the boat at the landing that morning (`MCS-D11.01`), and the quest now starts only after the player leaves Blackwater Landing (quest file `S00_closure`). No other line changed. |
