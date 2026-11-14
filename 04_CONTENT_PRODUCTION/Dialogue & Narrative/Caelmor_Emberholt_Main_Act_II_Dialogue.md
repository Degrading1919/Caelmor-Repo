# Emberholt Main Act II: Cast and Dialogue (Ash-Stained Chains, The Speaker's Smile)

**Status:** Authored production content for Creative Director milestone review (2026-11-14). This is the companion to `04_CONTENT_PRODUCTION/Quests/Caelmor_Emberholt_Main_Act_II.md`, which owns step ids, flags, encounters and mechanics. Characters marked **[CANON ANCHOR]** come from `LORE/Characters/Caelmor_Characters_Region4_Emberholt.txt` and obey the Emberholt rows of the Part 4 character ledger (`00_ADMIN/Reference/Caelmor_Part4_Character_Family_Continuity_Ledger.md`): nothing here gives them a new age, wartime service, kinship, travel or record custody beyond what the ledger allows. Characters marked **[NEW]** come from the Emberholt bible §5.2 or Act I, or are incidental role names; Act II adds **no new named character**. Nothing here is production JSON.

**Reserved decisions.** **`[D-E2]`** (Thalan's fate) marks every node that depends on it: `EAC-D8.60`–`.66`, all of `EAC-D9` (freed) and `EAC-D10` (aided), the branch lines in `EAC-D11` and `EAC-B9`. **Both branches are authored; neither is canon.** **`[D-S1]`** (the Speaker) marks every node that asserts what he knows or intends: the outgoing letter and the kept answers, the chamber record's Speaker block, Kaevren's and Serix's readings of him, and every line he speaks in `S06`. Other tags: `[ALLOCATION]` (one Ralenne line, `ESS-D3.03`), `[ED-12]` (protected Volkhari testimony and self-disclosure), `[ED-17]` (Serix's unset visions).

**Node format** (Lowmark/Thornfell/Mire/Emberholt Act I standard): `NODE SPEAKER: "Line." (stage note)`; conditions in brackets before the line; player options as `> [condition] "Option." → NEXT {effect}`. Ids follow bible §11.2: dialogue `<CODE>-D<n>.<nn>`, barks `<CODE>-B<n>.<nn>`, inspect texts `<CODE>-I<n>` in tables, documents in full.

**Voice rules (bible §5.3, binding):** civic pride first; criticism comes from inside. Craft, never magic; nobody calls a vein alive. Fire grammar: running warm, banked, flaring, gone grey. Wardens read tells. **The Speaker never lies:** he omits, reframes and thanks. **Volkhari restraint:** short, guarded, kind when trusted; a Volkhari decides what of their life is told, and nobody else describes their community. Children are children. The player is "warden's hand"; Volkhari say "you"; the Speaker says "friend". Other regions are never mentioned in Act II. Humour is quick and warm and lives in Cooling Houses, shops and forges. Plain sentences.

---

## Part 1: Act II voice additions

| Item | Status | Use |
|---|---|---|
| **"Breathe when I breathe."** | [NEW] Asera's whole instruction. | Asera. |
| **"Where they keep."** | [NEW] Dahrin's name for the closed-ring-and-bar mark. | Dahrin; the player's journal. |
| **"Not here."** | [NEW] What Dahrin says instead of what he knows. | Dahrin, once. |
| **"Awake enough to be uncomfortable."** | [Bible §6.1; R19 seed] | Thennek, once. Never repeated, never explained. |
| **"That is mine."** | [NEW] Thalan's answer to what is taken from him (R10 withheld). | Thalan. Echoes Theryn's "That's mine." in EH-M2 by design. |
| **"Ask me one."** | [NEW] Thalan's consent frame `[D-E2]`. | Thalan. |
| **"Too tidy."** | [NEW] Saelia's word for a crowd that breathes on a beat she did not write. | Saelia; later, the player's allies. |
| **"Every ember of Emberholt."** | [CANON] The Speaker's address to the city. | The Speaker. |
| **"Answered:"** | [NEW] The head of every reply in the kept bundle. | Documents only. |
| **"Fire remembers. We must remember rightly."** | [CANON] Seralynd's theology. | Seralynd. |
| **"Same place."** | [NEW] The Rat on the sob. | The Cinder Rat, once. |

**What nobody in Act II says:** what Thalan has been made to give; the phrase Dahrin keeps; who the emberlight was; where Thennek takes anyone; the words "Fire Titan"; the initiate's name; what "the Seat" is or who; who sets the dreams nobody set; what the sob in the pipes is; what a crowd's breath is for; the word "Remnant"; how many Volkhari there are or where they live; that anything is magic, a ghost or a curse.

---

## Part 2: Cast notes

### EH-M4 (`EAC`)

#### Dahrin Vosk, hunted survivor [CANON ANCHOR] `[ED-12]`
- **Canon:** fugitive Volkhari who escaped Remnant experimentation; horns broken at the tips; scales cracked and mottled with old ritual scarring; ember-veins that flicker in erratic rhythms; paranoid, anxious, deeply courageous; hates Ashfall; emberflare reflex when cornered; brings a sigil-stone; knows the opening phrase of the Titan's binding.
- **Limits (Part 4 ledger; bible §5.1):** speaks to his own captivity and escape only. No age, no wartime role, no count of years ("years"; "enough years"). Never speaks the phrase. Never locates a refuge. Never names a captor.
- **Voice:** quick, then stopped short; checks the curtain; says the true thing and then nothing. "That's all I have a right to say."

#### Asera of the Three Breaths, ritualist [CANON ANCHOR] `[ED-12]`
- **Canon:** soft-spoken, patient, precise; breath-binding calms flares; takes failures personally; feels the captive's pain as nightmares and chest pressure.
- **Limits:** never fights, never casts at anyone, teaches the player no craft. Decides how far she goes and says so. Her nightmares are hers and never evidence. Never names the emberlight.
- **Voice:** counts. Three-beat sentences. "Breathe when I breathe."

#### Thennek "Stone-Quiet" Vorren, pathfinder [CANON ANCHOR] `[ED-12]`
- **Canon:** speaks rarely; observant; protective of younger survivors; tremor-sense; barefoot on hot stone; suspects the Titan is not fully dormant.
- **Limits:** one R19 line ("awake enough to be uncomfortable"), never explained. Never fights. His own ways in and out are never shown. "You don't need to know where."
- **Voice:** almost nothing. Single sentences. Looks at the stone, not at people.

#### Thalan Veyr, captive elder [CANON ANCHOR] `[ED-12]`; his branch lines `[D-E2]`
- **Canon:** sole known current captive; captured in the post-Hollow purges; imprisoned for decades; held in a frame of carved basalt and ember shards, horns collared, tail shackled; calm and dignified; soft-spoken with steel; holds to the Volkhari doctrine of restraint and distance; senses the fire below as suffering, not kinship.
- **Limits (bible §5.1):** voiced consent in either branch; never killed, exploited or fought; may say that the fire below suffers; never explains the Titan, its bindings or the initiate; **never names anyone**; never says what is taken from him; gives no number.
- **Voice:** slow, exact, unhurried by pain. Short sentences with long silences between. Never self-pitying.

#### Maeryn Vall, seamstress [CANON ANCHOR] `[ED-12]`
- **In Act II:** sends for the player; keeps the back room; a safehouse. May say, once, unasked, that "we're not gone" (`EAC-D11.35`). Her heritage is otherwise still hers.
- **Voice:** warm, quick, deflecting with jokes; very still when afraid.

#### Yorven Khelt, District Overseer [CANON ANCHOR]
- **In Act II:** a key and a door. Knows old tunnels; does not ask Maeryn why; knows nothing of what is below.

#### Minor EH-M4 cast
- **DEEPBRAND CROSSBOW**, **DEEPBRAND GUARD** (pre-fight only; nothing after). **BREAD MAN** (off, the shop bell).

### EH-M5 (`ESS`)

#### Seralynd Hearthveil, Ember-Priestess [CANON ANCHOR]
- **Canon:** soft-spoken, firm; compassionate toward doubt; divided between faith and unease; her dreams are shaped by Hearthveil operatives; occasional unscripted visions.
- **Limits:** her own doctrine and her own dreams; her suspicion about the Covenant's Volkhari foundations is not used. Makes her own choice on the terrace.
- **Voice:** quiet, unhurried, honest about fear. "Fire remembers. We must remember rightly."

#### Saelia Verithe, Ritual Conductor [CANON ANCHOR]
- **Canon:** creative, organised; cares about the crowd's health; suspects something is off in her scripts.
- **Limits:** never knowingly complicit; stops her own rehearsal; never targetable.
- **Voice:** brisk, counts aloud, chalk on her hands. "Too tidy."

#### Ralenne Kharveil, Magistrix [CANON ANCHOR] (`[ALLOCATION]` on one line)
- **Canon:** theatrical, sincere about morale; keeps "suggestions" believing them inspired; unaware of conditioning.
- **Voice:** delighted, generous, quick to credit others.

#### The Flameward Speaker [CANON ANCHOR] `[D-S1]`
- **Canon:** middle-aged man; warm, measured, paternal; loves being loved; avoids direct lies, prefers omissions and symbolic language; believes he guides a renaissance.
- **Limits (Part 4 ledger; bible ED-5):** never fights, confesses or lies outright; lacks the Ashfall endgame; stays in office. Every line is checked: is it true as he believes it, or an omission? Nothing he says threatens.
- **Voice:** "every ember of Emberholt"; "friend"; thanks people for things they did not mean to give.

#### Kaevren Thalos, Grand Marshal [CANON ANCHOR]
- **In Act II:** intercepts, a duct-post mark, a ledger box. Reads the letters only because the player brings them. "He asked." `[D-S1]` on his reading.

#### The Cinder Rat [CANON ANCHOR]
- **Canon:** skittish, amused by danger; metaphors and double meanings; lives in old conduits; trades what he hears; seeks one "sobbing ember".
- **Limits:** a duct and a key; "Same place." and never more about the sob.
- **Voice:** sing-song, half-finished, pleased with himself; drops into flatness when the sob comes up.

#### Serix Arden, Hearthveil initiate [CANON ANCHOR] `[ED-17]`
- **Canon:** thin, barefoot, ash-marked feet; gentle-seeming, soft, unnervingly certain; young; trained to craft and seed dreams; has started seeing visions he did not craft.
- **Limits:** explains how a dream is set; reports unset visions as his and his sleepers' experience only; never says they centre on anyone; never names who sets them. Never fights.
- **Voice:** soft, careful, breathless when afraid. "I'd like someone to see what I didn't make."

#### Vael Trossen, High Magistrate [CANON ANCHOR]
- **Canon:** calm, logical, dispassionate; law as sacred architecture; dreams disrupted by Hearthveil work; a private list of cases where evidence conflicted with reports.
- **In Act II (exposed only):** finds his own name; convenes a sealed inquiry anyway.
- **Voice:** precise, slow, every sentence finished.

#### Minor EH-M5 cast
- **EMBERGUARD CLERK**, **LAMP-KEEPER** (grey Covenant cloak), **CROWD** (several), **CROWD 2**, **CHILD IN THE CROWD**.

---

## Part 3: EH-M4 Ash-Stained Chains (`EAC`)

### EAC-B0: Cinderweave barks (after EH-M3)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EAC-B0.1 | Passing Maeryn's shop | MAERYN | (from the door) "Warden's hand. You've a fitting. Don't make that face; everyone has a fitting." |
| EAC-B0.2 | Inside the shop, before `S00` | MAERYN | "If the bell rings while you're in the back, don't jump. Somebody in there jumps enough for both of you." |

### EAC-D1: Maeryn (S00_offer)

```
EAC-D1.01 MAERYN: (at the counter; a bolt of cloth half-measured; too quick) "There you are. Back room. Somebody's waiting who doesn't wait well."
EAC-D1.02 [EGH_STONE_HEARD] MAERYN: "You've been through that curtain once. You kept the terms. That's why he asked for you."
EAC-D1.03 MAERYN: (lower) "He's frightened. He'll tell you he isn't. Let him."
  > "I'll see him."                        → EAC-D1.05 {quest Active}
  > "Who is it?"                           → EAC-D1.04
  > "Not now."                             → EAC-D1.90
EAC-D1.04 MAERYN: "Somebody who came up out of the ground with nothing in his hands but a stone." (beat) "That's his to tell."   → EAC-D1.03 options
EAC-D1.05 MAERYN: (lifts the curtain) "Mind the third chair. It's new and it wobbles. Like everyone."   → EAC-D2.01
EAC-D1.90 MAERYN: "He's waited years. He can wait for you to finish your soup." → END   {re-offer at the counter: EAC-D1.01}
```

### EAC-D2: Dahrin Vosk (S01_dahrin)

```
EAC-D2.01 (The back room. Dahrin on the third chair by the stove, a hood pushed back: horns broken off at the tips, scales cracked and mottled, the veins under his skin flickering out of time. He stands when the player comes in, and then doesn't know what to do with standing.)
EAC-D2.02 DAHRIN: "You're the one from the circle." (he sits) "Sit. Please. I talk better sitting."
EAC-D2.03 (The shop bell rings beyond the curtain. The stove flame stands up tall; Dahrin's hands spread flat on his knees.)   {event: cinderweave.stove_flare}
EAC-D2.04 MAERYN: (through the curtain, calm) "Bread man, Dahrin. Breathe."
EAC-D2.05 (The flame comes down. Dahrin breathes out.) DAHRIN: "Bread man." (a short, unhappy laugh) "I know the bread man."
EAC-D2.10 [EGH_SHEET_READ] DAHRIN: "You read a sheet in the Red-Lit. 'One elder taken in the purge after. Held below.'" (beat) "You read 'held below'. I was below."
EAC-D2.12 [EH_HOLLOW_TRUTH = told] DAHRIN: "Somebody chalked the forge plaque. I went and looked at it at night. I put my hand on it. I don't know why."
EAC-D2.13 [EH_HOLLOW_TRUTH = kept] DAHRIN: "The Marshal keeps a second ledger now. Maeryn hears things. I'd like to be a line in it one day." (beat) "Not yet."
  > "Tell me what happened to you."          → EAC-D2.20
  > "Who are you?"                           → EAC-D2.15
EAC-D2.15 DAHRIN: "Dahrin. Vosk. That's all of it you need. The rest I'll give you in order or I'll lose it."   → EAC-D2.20

EAC-D2.20 DAHRIN: "They took me years ago. After the war. Enough years." (he doesn't say how many)
EAC-D2.21 DAHRIN: "Below the old works there are rooms with frames in them. Basalt. Shards in the posts. They put you in one and they leave you there."
EAC-D2.22 DAHRIN: "There was a wall between my frame and the next. Basalt too. Thick. And in the next one there was an older man."
EAC-D2.23 DAHRIN: "He talked to me through the wall. Every night. In our own tongue. Quiet, so they wouldn't hear, and slow, so I would."
EAC-D2.24 DAHRIN: "He taught me to count my breaths so I wouldn't count the days." (he looks at the stove) "I still do it. In queues. At the bread man's."
EAC-D2.25 DAHRIN: "One night a ring failed. Out past the frames, where they practise. The heat came through the floor and cracked my wall, and my collar with it."
EAC-D2.26 DAHRIN: "I ran with whatever was in my hand. I didn't look back at his frame. I've had a long time to be sorry about that."
EAC-D2.27 DAHRIN: "I came up an old shaft. Ladders, mostly. It comes out under your Overseer's ward."
EAC-D2.28 DAHRIN: "He was alive the night I ran. I heard him say my name through the wall when the floor went." (beat) "That's all I have a right to say: he was alive then."   {R10 custodian 1}
  > "What else do you know?"                 → EAC-D2.30
  > "Why come to me?"                         → EAC-D2.35
  > "What did you have in your hand?"         → EAC-D2.40
EAC-D2.30 DAHRIN: "Enough to be hunted."   → EAC-D2.31
EAC-D2.31  > "What else do you know, Dahrin?"   → EAC-D2.32
           > (Let it go.)                       → EAC-D2.28 options
EAC-D2.32 DAHRIN: (he looks at the curtain; then at the player; a long breath) "Not here."   {EAC_PRESSED}   → EAC-D2.28 options (the ask is not offered again)
EAC-D2.35 DAHRIN: "Because you went to the circle and came back and told it the way it was. Or kept it the way it was. Either's honest." (beat) "And because you're not ours. They count ours."   → EAC-D2.28 options

EAC-D2.40 DAHRIN: (opens his fist; a dark stone the size of a palm, a seam of emberglass through it) "This. It was on the fitter's bench by my frame. I don't know why I took it. I took it."   {item EAC_sigil_stone gained}
EAC-D2.41 DAHRIN: "It warms near their true doors. The doors that go somewhere. My hands shake too much to read it." (he holds up his hands; they shake)
EAC-D2.42 DAHRIN: "It doesn't know you. It doesn't know anyone. It just warms."
EAC-D2.45 DAHRIN: (draws in the stove ash with a finger: a ring, closed across with a bar) "This mark. On a door. Where they keep." (he wipes it out)   {EAC_SIGIL_TAUGHT; journal: The closed ring with a bar: where they keep.}
EAC-D2.46 DAHRIN: "There are other marks. I don't know them. I know that one. You learn the door you're carried through."
EAC-D2.50 DAHRIN: "If he's there." (stops) "If he's there, tell him the young one lived. He'll know which."
EAC-D2.51 DAHRIN: "Asera will come at dusk. She'll tell you how far she'll go. Believe her." (beat) "Maeryn says your Overseer has a door. Ask him nicely. He likes being asked nicely, and nobody does."   {EAC_DAHRIN_HEARD; journal: Find a way down.}   → END
```

### EAC-D3: Asera of the Three Breaths (S02, the back room at dusk)

```
EAC-D3.01 (Asera comes in from the yard door, hood down: long coiled horns, a slender tail, eyes that take in the room before the people in it. She touches Dahrin's shoulder once as she passes.)
EAC-D3.02 ASERA: "You're the one he chose." (she sits) "I'll tell you how far I'll go. Then you'll know what you have."
EAC-D3.03 ASERA: "As far as the room he's in. Not into their ring. I won't lift my hand at anyone, not to save you and not to save me."
EAC-D3.04 ASERA: "If that isn't enough, go without me. I'll think no less of you."
  > "It's enough."                                   → EAC-D3.10
  > "What do you do, then?"                          → EAC-D3.06
EAC-D3.06 ASERA: "I breathe." (beat) "Watch."   → EAC-D3.10
EAC-D3.10 (Asera turns to Dahrin. She breathes in, slow, and holds it, and lets it go, three times. Dahrin breathes with her by the second. The stove flame, which has been restless all evening, settles low and blue at the root.)
EAC-D3.11 ASERA: "In a hot room, stand by me and breathe when I breathe. The room will come down. Not because of me. Because of both of us."
  > "Do you know who's down there?"                  → EAC-D3.20
  > "I'm ready."                                     → EAC-D3.30
EAC-D3.20 ASERA: (a hand flat on her chest) "I've felt that room in my chest for years. At night. Like a weight." (beat) "That's mine. It isn't proof of anything. Don't carry it as proof."   → EAC-D3.30
EAC-D3.30 ASERA: "I'll find your shaft. I know my own way to it." (she does not say what way)   {EAC_ASERA}   → END
```

### EAC-D4: Yorven Khelt (S02, the Cooling House)

```
EAC-D4.01 YORVEN: (at the end table, a cup of something steaming) "Warden's hand. Sit or stand, the soup's the same."
EAC-D4.02 YORVEN: "Maeryn Vall sent word. She wants a door." (he takes a ring of keys off his belt and starts working one loose) "Maeryn Vall asked me for a door. I don't ask Maeryn Vall why."
EAC-D4.03 YORVEN: "My old bypass. The one I brought you up. At the Cinderwall end there's a miners' gate in the wall. Padlocked since before I was Overseer."
EAC-D4.04 YORVEN: "Behind it there's a shaft. Goes down further than I ever went. I went down two ladders once, at nineteen, and came back up because I didn't like how warm my feet were."
EAC-D4.05 YORVEN: (marks the player's map with a stub of chalk) "There. If anyone asks, you're inspecting the gate for the ward. You are, too. Tell me if the hasp's gone."
EAC-D4.06 YORVEN: (hands over the key) "Bring it back. It's the only one."   {carry-state: gate key; EAC_GATE_KEY}
  > [EH_HOLLOW_TRUTH = told] "You walked that tunnel. You said it wasn't a forge."    → EAC-D4.08
  > "Thank you."                                                                     → EAC-D4.10
EAC-D4.08 YORVEN: "I did. I'll say it again if anyone wants it said." (beat) "I don't know what's further down. I'd rather you told me after than before."   → EAC-D4.10
EAC-D4.10 YORVEN: "The Cooling House owes you soup. That's not nothing in Cinderwall." → END
```

### EAC-D5: Thennek at the shaft head (S02 end)

```
EAC-D5.01 (The miners' gate swings in on a short passage and a square shaft. On its lip, Thennek sits with his bare feet on the hot stone. Asera stands a little behind him. Neither says how they got here.)
EAC-D5.02 THENNEK: (doesn't look up) "You."
EAC-D5.03 ASERA: "Thennek. He'll take us down."
EAC-D5.04 THENNEK: "To their mouth." (beat) "Not past it."
  > "Why not past it?"                  → EAC-D5.06
  > "That's enough."                    → EAC-D5.08
EAC-D5.06 THENNEK: "Past it they count." (he stands) "I don't go where I'm counted."   → EAC-D5.08
EAC-D5.08 THENNEK: (swings onto the first ladder) "Watch your feet. Not mine."   {EAC_THENNEK_MET; journal: Reach the sigil gallery.}   → END
```

### EAC-B3: the shaft and the mouth (S03)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EAC-B3.1 | Second landing, vents breathing | ASERA | "The ash lifts first. You know this." |
| EAC-B3.2 | `EGH_FLARECAP`; player steps round an orange cap | THENNEK | (a single nod; no line) |
| EAC-B3.3 | Player strikes or braces on an orange cap | THENNEK | "No." |
| EAC-B3.4 | Player crosses into the landing (K3) | DEEPBRAND CROSSBOW | "Sealed works." |
| EAC-B3.5 | EAC-E1 begins | DEEPBRAND GUARD | "Off the landing." |
| EAC-B3.6 | EAC-E1 ends | ASERA | (from the shaft-foot niche; quietly) "They had names. I didn't know them." |
| EAC-B3.7 | Shaft foot, the full cask | ASERA | "Somebody keeps this full. Don't ask him." |

### EAC-D6: Thennek at the Warrens' mouth (S03)

```
EAC-D6.01 (Where the shaft breaks into dressed stone, Thennek stops, crouches, and lays his palm flat on the rock. He stays like that for a long moment. The conduits along the walls hum.)
EAC-D6.02 ASERA: (quietly) "Thennek."
EAC-D6.05 THENNEK: "Something under all of this is awake." (beat) "Awake enough to be uncomfortable."   {EAC_THENNEK_HEARD}
  > "What is it?"                       → EAC-D6.06
  > (Say nothing.)                      → EAC-D6.08
EAC-D6.06 THENNEK: (takes his hand off the rock) "I said what I felt."   → EAC-D6.08
EAC-D6.08 THENNEK: "Here's their mouth. I'll be at the foot when you come back up." (he goes back to the niche without another word)   → END
```

### EAC-D7: Asera underground (S03–S05)

```
EAC-D7.01 ASERA: (at the first plate; she doesn't step on it) "Red and cracked. Like your wardens' beads. Don't step."
EAC-D7.02 ASERA: "Clear ones are spent. Amber ones are thinking about it. The stone between them never changes its mind."
      {player inspects a plate: EAC-I3; EAC_PLATE_READ}
EAC-D7.10 (First heat room. The pocket pulses through the cracks; the air shakes.)
EAC-D7.11 ASERA: (in the niche) "It woke when they fought. Rooms do." (beat) "Stand by me. Breathe when I breathe. Or wait. Both are true."
  > (Stand by her and keep her count.)        → EAC-D7.12
  > (Wait in the niche.)                      → EAC-D7.15 {keep watch, one turn}
EAC-D7.12 ASERA: "In." (beat) "Hold." (beat) "Three."   {channel segment 1 of 3}
EAC-D7.13 ASERA: "In." (beat) "Hold." (beat) "Three."   {segment 2}
EAC-D7.14 ASERA: "In." (beat) "Hold." (beat) "Three." (the room's tell drops from red to amber; the shaking air goes still)   {segment 3; room → Working; EAC_BREATH = asera (first room)}   → END
EAC-D7.15 ASERA: (sits; closes her eyes) "Then we wait." (the room turns on its own)   {room → Working; EAC_BREATH = waited (first room)}   → END
EAC-D7.20 (The ring's edge niche.) ASERA: "That ring is fed from his frame." (beat) "I won't step on it. I said so in Maeryn's room and I say so here."
EAC-D7.21 ASERA: "I'll be in this niche. Come back for me when the floor is yours."
EAC-D7.30 [warrens.emberlight] ASERA: (without looking up) "Don't look. He isn't here."
```

### EAC-B4: the plate run (S03)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EAC-B4.1 | Player steps on a primed plate | ASERA | "Red. You read it. Believe it." |
| EAC-B4.2 | Player waits on a rib for a plate to clear | ASERA | "Good. Stone between doesn't change its mind." |
| EAC-B4.3 | Second heat room | ASERA | `EAC_BREATH = asera`: "You kept my count. Again?" / `= waited`: "We can wait again. Or you can breathe with me this time." |
| EAC-B4.4 | Overhead conduits | ASERA | "Warm. Everything here is warm toward the same place." |

### Inspect texts: the shaft, the run and the gallery (S03–S05)

| Object | Text | Condition |
|---|---|---|
| The miners' gate (EAC-I1) | "An iron gate in the bypass wall. The hasp is rusted but whole. Yorven will want to know." | — |
| The shaft-foot cask (EAC-I2) | "A water cask, full, the lid wet. Nobody you've seen filled it." | — |
| A pressure plate (EAC-I3) | `EH_TELLS`: "An iron plate set in stone, an emberglass bead in its face. Red, with a crazed skin: primed. It will vent if you step on it. The stone ribs between the plates carry no bead." | Required once |
| The sigil-stone, held (EAC-I4) | "Dark stone, a seam of emberglass. Here: *cold*." / "*cool*" / "*warm*". | Reads the nearest door |
| Tier 1 dead end (EAC-I5) | "Conduit plates stacked to the roof, each stamped with a number. The stone in your hand is cold." | — |
| Tier 2 jamb with flarecap (EAC-I6) | "Bright orange cap in the seam of the jamb. A live vein close behind this wall. The stone is warm here, and so is the wall." | — |
| Tier 2 orange-cap dead end (EAC-I7) | "A fitter's store. Collar blanks hang on pegs in sizes. Some are small. The stone is cool." | — |
| Tier 3 true door (EAC-I8) | `EAC_SIGIL_TAUGHT`: "A ring closed across with a bar, cut and filled with dark glass. Where they keep. The stone is warm." | — |
| The chamber door (EAC-I9) | "The same mark: a ring closed with a bar. The stone is warm, warmer than anywhere yet." | — |
| The slate's marks (EAC-I11) | `EEH_LEDGER_READ`: "Rings, rings with a dot, filled rings. The same marks as the second column in the Molten Stair's ledger. Nothing on the slate says what they mean." | Optional |
| The feed pipe (EAC-I12) | "An iron pipe down through the roof into the frame's base. Its collar is city pattern, the kind on every junction in Cinderwall. Where the valve-house number should be stamped, the metal has been filed smooth." | Optional |
| The fitter's anvil (EAC-I13) | "A fitter's anvil, a hearth, a quench trough, a rack of embersteel bar. Tools for fitting collars. Kept in good order." | — |

### EAC-B5: the sigil gallery (S04)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EAC-B5.1 | Tier 1, first warm door | ASERA | "Warm. Dahrin said warm." |
| EAC-B5.2 | Player opens a wrong door | ASERA | "Nothing. Come back. Nothing's lost." |
| EAC-B5.3 | Tier 2, two warm doors, `EGH_FLARECAP` | ASERA | "Your miner's cap. Look at it before you look at the stone." |
| EAC-B5.4 | Tier 2, two warm doors, no `EGH_FLARECAP` | ASERA | "Two warm. Something besides a door is warm. Look round the jambs." |
| EAC-B5.5 | Tier 3, two warm doors | ASERA | "Dahrin drew you a mark. He drew it for this." |
| EAC-B5.6 | EAC-E2 seen | ASERA | (stepping back into a doorway) "That one isn't anybody. It walks. Mind its arm." |

### EAC-B6: the proving ring (S05, EAC-E3)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EAC-B6.1 | Fight begins | DEEPBRAND GUARD | "Off the ring!" |
| EAC-B6.2 | Warden-frame on a red sector, player hitting it | ASERA | (from the niche) "It's drinking. Let the floor go past it." |
| EAC-B6.3 | Player caught in a vent | ASERA | "The hand goes one way. Go the other." |
| EAC-B6.4 | Fight ends | ASERA | (she doesn't come out until the last sector has passed) "His door is on the rim. Keep to the rim." |

### Document: the proving-ring slate (EAC-I10; R10 custodian) 

Read in place on the chamber wall. Chalk on slate in a fitter's square hand; older rows wiped and rewritten.

> ***Perfect Flame: trial series.***
>
> | Trial | Ring | Hands (by mark) | Frame carried | Held to the mark |
> |---|---|---|---|---|
> | *(early rows, half wiped)* | *1st* | *○ ○ ◉ ○ ○ ● ○ ○* | *no* | *—* |
> | | *1st* | *○ ◉ ◉ ○ ● ○ ○ ○* | *no* | *—* |
> | | *2nd* | *◉ ◉ ● ◉ ○ ◉ ● ◉* | *no* | *—* |
> | *(recent rows)* | *2nd* | *◉ ● ● ◉ ● ◉ ● ●* | *yes* | *‖‖* |
> | | *2nd* | *● ● ◉ ● ● ● ◉ ●* | *yes* | *‖‖‖* |
> | | *2nd* | *● ● ● ● ◉ ● ● ●* | *yes* | *‖‖‖‖‖* |
>
> *Frame: hold the draw longer. Next series after the Kindling.*

Production rule: the trial column is left blank on purpose; the number of rows is fixed art, not a count. The marks are the three marks of the Molten Stair ledger's second column (ring, ring with a dot, filled ring). Nothing on the slate names a person, a place they came from, or what the frame takes from the man in it (R10 withheld). The last line ties the series to the festival without saying why (R18 seed; never explained here).

### EAC-D8: Thalan (S05–S06)

```
EAC-D8.01 THALAN: (in the frame; the glow sinking into a cool phase; his voice low and level) "The ring went quiet. So someone came through it."
EAC-D8.02 THALAN: (he looks at the player, then past them) "And someone stayed at its edge, because she said she would." 
EAC-D8.03 ASERA: (in the doorway; she comes in now) "Elder."
EAC-D8.10 (Thalan says something to Asera in their own tongue, slow, a few words. She answers with fewer. Neither translates.)
EAC-D8.11 ASERA: (to the player, not unkindly) "That was between us."
EAC-D8.12 THALAN: "Before anything." (the glow begins to rise again; his breath shortens; he waits it out, and speaks in the cool) "The young one. Through the wall. Did he live?"
  > "The young one lived. He said you'd know which."      → EAC-D8.20
EAC-D8.20 THALAN: (a long breath, the whole of a cool phase) "I know which."   {EAC_MESSAGE_GIVEN}
EAC-D8.21 THALAN: "I said his name when the floor went. I didn't know if it reached." (beat) "Good. Ask what you came to ask. I'll answer what's mine to answer."
  > "What do they take from you?"                         → EAC-D8.30
  > "How long have you been here?"                        → EAC-D8.32
  > "What's below us?"                                    → EAC-D8.34
  > "Who put you here?"                                   → EAC-D8.36
  > "What happens now?"                                   → EAC-D8.60
EAC-D8.30 THALAN: "That is mine." (he does not say it hard) "Keep your eyes on the frame if you like. You'll see what it does. You won't see what it takes."   → EAC-D8.21 options (not offered again)
EAC-D8.32 THALAN: "I counted breaths. I stopped counting days." (beat) "He told you that."   → EAC-D8.21 options
EAC-D8.34 THALAN: "Under this floor, far down, something burns that cannot stop burning." (beat) "It is in pain. I have listened to it longer than I have listened to anything." (He says nothing more about it.)   → EAC-D8.21 options
EAC-D8.36 THALAN: "People who write things down." (beat) "I won't give you their names. I don't owe them that much attention."   → EAC-D8.21 options
```

```
EAC-D8.60 [D-E2] ASERA: (to both of them, plainly) "We can cut you out, and Thennek takes you on. Or we can break what the frame draws from you, and leave you as you choose." (beat) "You decide. They ask."
EAC-D8.61 [D-E2] THALAN: (to the player) "I have wanted both of those every night for a long time." (beat) "Ask me one."
  > [D-E2] "Come with us. Thennek is waiting."                                   → EAC-D8.62
  > [D-E2] "Tell us what to break, and we'll leave you as you choose."            → EAC-D8.64
  > [D-E2] "Which do you want?"                                                   → EAC-D8.66
EAC-D8.62 [D-E2] THALAN: (a long silence; the glow rises and sinks once) "If the frame is empty, they will look for someone to fill it." (beat) "Let them look. Let them look a long time." (beat) "Yes. Cut me out."   {EH_THALAN = freed}   → EAC-D9.01
EAC-D8.64 [D-E2] THALAN: "If the frame is empty, they will fill it." (beat) "Break what it draws. Leave me in it. Then take what you have seen up to where they write things."   {EH_THALAN = aided}   → EAC-D10.01
EAC-D8.66 [D-E2] THALAN: "Both are true." (beat) "Ask me one."   → EAC-D8.61 options
```

### EAC-D9: freed `[D-E2]` (S06–S07)

```
EAC-D9.01 [D-E2] ASERA: "The pins are riveted. The fitter's things are there." (a nod to the hearth) "Or the collars slacken in the cool. Twice would do it."
  > [D-E2] (Forge a drift at the fitter's anvil.)              → EAC-D9.05 {Option A}
  > [D-E2] (Ease the collars in the cool, by hand.)            → EAC-D9.07 {Option B}
EAC-D9.05 [D-E2] THALAN: (watching the player at the hearth) "They kept it well. They keep everything well."
      {heat, shape, quench: the drift; carry-state}
EAC-D9.07 [D-E2] THALAN: "Wait for the cool. I've had practice. You'll learn the rhythm in one."
      {two cool-phase channels on the collars}
EAC-D9.10 [D-E2] ASERA: (her hand flat on Thalan's chest, breathing with him while the player works) "In. Hold. Three."
EAC-D9.11 [D-E2] (Option A: the drift goes through the first pin; the second; the last. Option B: the collars ease a finger's width in the first cool, and open in the second.)
EAC-D9.20 [D-E2] (The collars open. Asera lifts the shackle key off its hook on the post and turns it. Thalan steps forward out of the frame on his own and stands, slowly, one hand on a basalt post. The frame glows once without him, and then gutters.)
EAC-D9.21 [D-E2] THALAN: (looking at his own hand on the post) "Standing is different when you choose it."
EAC-D9.22 [D-E2] [EAC_FRAME_WORK = self] THALAN: "Your hands are steady. Steadier than his were." / [= wait] THALAN: "You waited well. Most people can't."
EAC-D9.23 [D-E2] (Out in the ring, the sectors go dark one by one.)
EAC-D9.24 [D-E2] THALAN: "Walk slowly. I'll keep up if you walk slowly."   {journal: Go back up to Maeryn's.; escort-follow on}   → END
```

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EAC-B7.1 `[D-E2]` | Freed: walking the dark ring | THALAN | "It was loud. I didn't know how loud until now." |
| EAC-B7.2 `[D-E2]` | Freed: the sigil gallery | THALAN | (touching a door's mark as he passes) "Where they keep." |
| EAC-B7.3 `[D-E2]` | Freed: a heat room | ASERA | (stopping with him) "Breathe when I breathe, elder." THALAN: "I taught a boy that." |
| EAC-B7.4 `[D-E2]` | Freed: the plate run | THALAN | "I'll walk where you walk." |

```
EAC-D9.40 [D-E2] (The shaft foot. Thennek stands up out of the niche. He and Thalan look at each other for a long time. Neither speaks.)
EAC-D9.41 [D-E2] THALAN: (to the player) "Tell the young one I walked."
EAC-D9.42 [D-E2] THENNEK: (to the player) "You don't need to know where." (He takes Thalan by the forearm and into a side cut the player hasn't seen used. Their footsteps go on for a while after they're out of sight, and then don't.)   → (climb; EAC-D11)
```

### EAC-D10: aided `[D-E2]` (S06–S07)

```
EAC-D10.01 [D-E2] ASERA: "The draw comes out at the foot. There." (the coupling where the conduits leave the frame) "The fitter's things are there. Or it can be wedged in the cool. Twice would do it."
  > [D-E2] (Forge a blanking plate at the fitter's anvil.)     → EAC-D10.05 {Option A}
  > [D-E2] (Wedge the draw valve in the cool, by hand.)         → EAC-D10.07 {Option B}
EAC-D10.05 [D-E2] THALAN: (watching the player at the hearth) "They kept it well. They keep everything well."
      {heat, shape, quench: the blanking plate; carry-state}
EAC-D10.07 [D-E2] THALAN: "Wait for the cool. I've had practice. You'll learn the rhythm in one."
      {two cool-phase channels on the valve}
EAC-D10.10 [D-E2] ASERA: (her hand flat on Thalan's chest, breathing with him while the player works) "In. Hold. Three."
EAC-D10.11 [D-E2] (Option A: the plate seats in the coupling, one turn, two, three. Option B: the wedge goes in a finger in the first cool, and home in the second.)
EAC-D10.20 [D-E2] (The glow fades from the shards outward and does not come back. The hum stops. Thalan, still collared, still in the frame, breathes out the whole of a breath without it catching.)
EAC-D10.21 [D-E2] THALAN: "It is quiet." (beat) "I had forgotten quiet."
EAC-D10.22 [D-E2] [EAC_FRAME_WORK = self] THALAN: "Your hands are steady. Steadier than his were." / [= wait] THALAN: "You waited well. Most people can't."
EAC-D10.23 [D-E2] (Out in the ring, the sectors go dark one by one.)
EAC-D10.24 [D-E2] THALAN: "They will mend it. Slower than you think. Slower is what I have." (beat) "Take an account up. Not to be sung. To be written where they write things. Will you?"
  > [D-E2] "I'll carry it."                 → EAC-D10.26 {EAC_ACCOUNT_PROMISED}
EAC-D10.26 [D-E2] THALAN: "Then go. Asera, go with them. Come back when you come back."   {journal: Go back up to Maeryn's.}   → END
```

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EAC-B8.1 `[D-E2]` | Aided: walking the dark ring | ASERA | "It's dark because of you. Remember that when it's lit again." |
| EAC-B8.2 `[D-E2]` | Aided: the sigil gallery | ASERA | (touching a door's mark as she passes) "Where they keep." |
| EAC-B8.3 `[D-E2]` | Aided: a heat room | ASERA | (stops; breathes three times, alone, for nobody; walks on) |
| EAC-B8.4 `[D-E2]` | Aided: the plate run | ASERA | "Walk where I walk. I'm not in a hurry tonight." |

```
EAC-D10.40 [D-E2] (The shaft foot. Thennek stands up out of the niche and looks past them, down the tunnel, for someone who isn't there.)
EAC-D10.41 [D-E2] ASERA: "He chose. He asked for an account."
EAC-D10.42 [D-E2] THENNEK: (a long look at the player) "Then carry it." (He goes into a side cut the player hasn't seen used, alone.)   → (climb; EAC-D11)
```

### EAC-D11: the back room (S07 end)

```
EAC-D11.01 (The top of the shaft. Asera stops at the miners' gate.) ASERA: "I'll come to Maeryn's when I come." (she goes her own way)
EAC-D11.02 (Maeryn's back room. Dahrin is on the third chair by the stove. He stands when the player comes in. This time he knows what to do with standing: he waits.)
EAC-D11.03 PLAYER (summary line, shown): "He was there. He's alive. I told him the young one lived. He said he knew which."
EAC-D11.04 DAHRIN: (sits down hard; covers his face with both hands for a moment; takes them away) "He knew which."
EAC-D11.10 [D-E2] [EH_THALAN = freed] PLAYER (shown): "He walked out. Thennek took him on. He said to tell you he walked."
EAC-D11.11 [D-E2] [freed] DAHRIN: "He walked." (beat) "Don't tell me where. I'd only go." (a breath; counting) "Don't tell me where."
EAC-D11.12 [D-E2] [EH_THALAN = aided] PLAYER (shown): "He chose to stay. The frame's stopped drawing on him. He asked me to carry an account up."
EAC-D11.13 [D-E2] [aided] DAHRIN: "He stayed." (long silence) "Of course he stayed. He'd have stayed for me. He did, once, through a wall." (beat) "Then you carry it. I'll help you carry it, when it's time."
EAC-D11.20 [EAC_PRESSED] DAHRIN: "You asked me twice what else I know. I said not here." (beat) "It's still not here. It's not never."
EAC-D11.21 [not EAC_PRESSED] DAHRIN: "There's a thing I know that I haven't told anyone. You didn't ask. I noticed."
EAC-D11.30 DAHRIN: (holds out his hand) "The stone. It's warm still. It'll go cold up here." (the player gives it back)   {item EAC_sigil_stone removed}
EAC-D11.31 DAHRIN: (closes his fist round it; his hand isn't shaking) "Look at that."
EAC-D11.35 MAERYN: (at the curtain; she has been there a while) "We're not gone, you know." (beat) "People say we went. We didn't go anywhere." (she lets the curtain fall behind her)   {optional, plays once if the player stays in the room ~5 s after EAC-D11.31; EAC_MAERYN_SAID} [ED-12]
EAC-D11.36 MAERYN: (back at the counter, handing over a folded hood) "Lined. You'll be in ducts again. Everybody is." (beat) "If anyone asks, you were being fitted."   {reward: lined duct hood}
EAC-D11.40 DAHRIN: (to the stove, or to the player) "In. Hold. Three." (he breathes) "Go home, warden's hand. Wherever that is tonight."   {quest Completed; journal: The Ember-Priestess has asked for the warden's hand at the Covenant lamp-house.}
```

### EAC-B9: post-quest barks

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EAC-B9.1 | Maeryn's shop | MAERYN | "Your fitting's still open. It's always open." |
| EAC-B9.2 `[D-E2]` | Maeryn's back room | DAHRIN | `freed`: "I don't count days now. I count bread men." / `aided`: "When you carry it up, tell me. I'd like to be standing." |
| EAC-B9.3 `[D-E2]` | Maeryn's back room, ambient | ASERA | `freed`: (not present; a second hood and pair of gloves on the peg, gone the next day) / `aided`: (in the third chair, eyes shut, a hand flat on her chest; she does not speak) |
| EAC-B9.4 | Cooling House | YORVEN | "Gate's locked again. Hasp held. Thank you for asking it." |
| EAC-B9.5 | Shaft head, post-quest | (none) | (A water cask at the foot, full. A barricade past the mouth, Deepbrand's mark burned into it.) |

---

## Part 4: EH-M5 The Speaker's Smile (`ESS`)

**Counting convention (documents).** The Covenant counts vigils down to the festival: *Kindling less 12* is the twelfth night before the High Kindling. The access book, the chamber record and the slips all use it. No calendar month is named.

### ESS-B0: Emberhold barks (after EH-M4)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| ESS-B0.1 | Emberhold street, dusk | CROWD | "Rehearsal tonight. My boy's got a mark on the stone with his name chalked by it." |
| ESS-B0.2 | Emberhold street | CROWD 2 | "They say it's the biggest Kindling since my mother's day. They say that every year. This year I believe it." |
| ESS-B0.3 | Covenant lamp-house door | LAMP-KEEPER | "Vigil hall's open to anyone who'll sit quiet. The Priestess is inside." |
| ESS-B0.4 | Ash Terraces, by day | CHILD IN THE CROWD | (practising, alone, very seriously) "Lamps. Two. Three. Four." (and a big breath after) |

### ESS-D1: Seralynd (S00_offer)

```
ESS-D1.01 (The vigil hall. Seralynd moves down the line of hanging lamps with a long hook, turning each one down a notch.) SERALYND: "Warden's hand. Thank you for coming in. Sit, if you like. I'll finish the row."
ESS-D1.02 SERALYND: (the last lamp; she hangs the hook up) "I keep vigil here two nights in seven. On those nights I dream the High Kindling. The lamps, the terraces, the city breathing as one. I dream it before it happens."
ESS-D1.03 SERALYND: "People tell me that's a gift. I'd like it to be. I don't trust a dream that arrives on time."
ESS-D1.04 SERALYND: "Fire remembers. We must remember rightly. I'd like to know if I'm remembering something I was given."
  > "What do you want from me?"                  → ESS-D1.05
  > "Why me?"                                    → ESS-D1.06
  > "Not now."                                   → ESS-D1.90
ESS-D1.05 SERALYND: "Stand beside me in the rehearsal crowd at dusk. Watch it. Read it the way you'd read a junction."   → ESS-D1.07
ESS-D1.06 SERALYND: "You're not ours, and you're not his." (beat) "Yorven says you read tells. I've watched braziers all my life and never once read one."   → ESS-D1.04 options
ESS-D1.07 SERALYND: "I'll be at my mark on the crowd floor. Yours is beside it. Someone's chalked it already; they chalk one for anyone who comes."
  > "I'll be there."                             → ESS-D1.08 {quest Active; journal: Stand in the rehearsal crowd at dusk.}
  > "Not now."                                   → ESS-D1.90
ESS-D1.08 SERALYND: "Thank you." (she means it, and looks a little afraid of having asked) "If it's nothing, I'd like to know that too."   → END
ESS-D1.90 SERALYND: "The rehearsals run every dusk until the Kindling. I'll be at my mark." → END   {re-offer: Seralynd in the vigil hall, ESS-D1.01}
```

### ESS-D2: the first rehearsal (S01)

```
ESS-D2.01 (Dusk on the crowd floor. Three brazier rows, left, centre, right. Citizens on their chalked marks. Seralynd on hers. Saelia at the cue stand, chalk to the wrist. Ralenne at her lectern above. On the balcony, the Speaker in red and black.)
ESS-D2.02 [D-S1] SPEAKER: (from the balcony; one hand lifted; a voice that carries without trying) "Every ember of Emberholt. Thank you for your evening. We are only practising tonight. Practise well, and the night itself will be easy."
ESS-D2.03 SERALYND: (beside the player, low) "He comes to every rehearsal. He says he likes to watch the city learn its part."
ESS-D2.10 SAELIA: (calling the run) "Lamps. Two. Three. Four." (the crowd lifts its lamps on four)   {rehearsal run begins; three inspect windows open in turn on the left, centre and right rows (ESS-I1)}
ESS-D2.11 SAELIA: "Lamps. Two. Three. Four." / "Turn. Two. Three. Four." / "Raise. Two. Three. Four."   {cue barks, looped through the run}
ESS-D2.12 [ESS_RUN_READ] SERALYND: (between cues) "What did you see?"
  > "Every time a row goes amber, the crowd's just breathed in."   → ESS-D2.13
  > "Nothing yet."                                                → ESS-D2.14
ESS-D2.13 SERALYND: "Together?" (she listens, then nods) "Together."   → ESS-D2.20
ESS-D2.14 SERALYND: "Then watch the next one with me." → ESS-D2.20
ESS-D2.20 SAELIA: (halfway through the second run; she drops her hands) "Stop. Stop." (the crowd stops, lamps half raised) "Too tidy."
ESS-D2.21 SAELIA: (to the player and Seralynd, coming down off her stand, low) "My cues are on four. Listen to them. They're breathing in on a five. There's no five on my sheet." (she holds the sheet out)   {inspect: the cue sheet (ESS-I2)}
ESS-D2.22 SAELIA: "I wrote the cues. I didn't write that."   {ESS_TOO_TIDY}
  > "Where else could a beat come from?"         → ESS-D2.23
  > "Does it hurt anyone?"                       → ESS-D2.25
ESS-D2.23 SAELIA: "The words. The crowd breathes where the words let it. It's in the script." (beat) "Ask the Magistrix where the script came from. Nicely; she loves it."   → ESS-D2.24
ESS-D2.25 SAELIA: "A crowd that breathes together stands together. That's the job. I like my crowds standing." (beat) "I don't like not knowing who's counting."   → ESS-D2.23
ESS-D2.24 SAELIA: (back up on her stand; loud, cheerful) "From the top! Lamps!"   {step S01 complete; journal: Ask the Magistrix about the script.}   → END
```

### ESS-B1: the terraces during rehearsals

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| ESS-B1.1 `[D-S1]` | Any rehearsal, ambient | SPEAKER | (on his balcony; smiling down; he lifts his hand to a child on her father's shoulders, and she waves back) |
| ESS-B1.2 | Between runs | CROWD | "My arms are going to fall off before the real night." |
| ESS-B1.3 | Between runs | CROWD 2 | "It feels good, doesn't it, when it all goes at once? Like being bigger than yourself." |
| ESS-B1.4 `[D-S1]` | Player speaks to the Speaker on the stair after a rehearsal (before `S06`) | SPEAKER | (pausing; a warm hand near, not on, the player's shoulder) "Thank you for coming, friend. Stand nearer the front tomorrow. It's warmer." (he goes on up; there is no option to stop him) |
| ESS-B1.5 | Saelia, between runs | SAELIA | "Breathe when you like, everybody. It's not a test." (under her breath) "It's not supposed to be." |

### ESS-D3: Ralenne (S02_script)

```
ESS-D3.01 RALENNE: (at her lectern; scripts stacked under one hand; delighted) "You were in my crowd! Did it move you? It's meant to move you."
ESS-D3.02 RALENNE: "And you're the one who made me read my own name on a coal order. I've read every word since. You'd be amazed what I sign."
ESS-D3.03 [ALLOCATION] RALENNE: [EH_COLD_WARD = posted] "You put my aide's name on a Cooling House board. I read every order twice now." / [= settled] "Your Overseer countersigns my clerk's coal book every week. He is very slow about it."
ESS-D3.04 RALENNE: "What can I do for you? Ask anything. I'll show anyone my script; it's the best thing I've ever been given."
  > "May I see the script?"                       → ESS-D3.05
  > [ESS_TOO_TIDY] "Saelia says there's a beat in it she didn't write."   → ESS-D3.10
  > "Nothing for now."                            → END   {re-entry: ESS-D3.04}
ESS-D3.05 RALENNE: (turns the stack round for the player) "The address and the responses. I've been at it since the thaw."   {inspect: the script (ESS-I3); ESS_SCRIPT_READ}   → ESS-D3.06
ESS-D3.06 [ESS_SCRIPT_READ] RALENNE: "You've found my favourite line. Everyone does." (she says it, softly, as written) "One flame, one breath, one city."
  > "Where did that line come from?"              → ESS-D3.12
  > "Who wrote it?"                               → ESS-D3.12
ESS-D3.10 [ESS_TOO_TIDY] RALENNE: "Saelia counts in fours. She always has. The line wants a breath after it; you can feel it wanting one." (she shows the mark under the line) "I didn't put that mark there either, to be honest. It came with the line."   {if not ESS_SCRIPT_READ: inspect ESS-I3, ESS_SCRIPT_READ}   → ESS-D3.12
ESS-D3.12 RALENNE: "A suggestion slip. My best lines come that way. Unsigned. From the vigil." (she unties a ribbon round the back of her stack) "A lamp-keeper leaves them on my lectern. I've never seen which one."
ESS-D3.13 RALENNE: (hands over the newest) "That's the one."   {inspect: the slip (ESS-I4); ESS_SLIP_SEEN}
ESS-D3.14 RALENNE: "Somebody dreams better than I do. I'm not too proud to take a good line."
  > "Do you ever wonder who writes them?"         → ESS-D3.15
  > "Thank you, Magistrix."                       → ESS-D3.20
ESS-D3.15 RALENNE: "I used to. I'd sit up making guesses." (beat) "Then I decided it didn't matter, if the lines were good. They are good. You heard the crowd."   → ESS-D3.20
ESS-D3.20 RALENNE: (tying the ribbon again) "Come on the night itself. Stand at the front. You'll see what all this is for."   → END   {on leaving the terrace: ESS-B2.4}
```

### ESS-B2: the terrace and the clerk

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| ESS-B2.1 | Ralenne's lectern, ambient | RALENNE | (to herself, trying the line) "One flame. One breath." (a breath) "One city." |
| ESS-B2.2 | Saelia's cue stand, after `ESS_SLIP_SEEN` | SAELIA | "A slip. Of course it's a slip. Everything good comes on a slip." |
| ESS-B2.3 | A lamp-keeper crossing the terrace | LAMP-KEEPER | (a grey cloak; a basket of lamp wicks; she nods to Ralenne and does not stop) |
| ESS-B2.4 | Player leaves the rehearsal terrace after `ESS_SLIP_SEEN` | EMBERGUARD CLERK | "Warden's hand? The Marshal asks for you. He says you'll know where."   {step S02 complete; journal: Find where the orders go.} |

### ESS-D4: Kaevren (S03, the Marshal's office)

```
ESS-D4.01 KAEVREN: (at the map table; four folded papers squared in front of him) "Sit." (he finishes the line he's writing first)
ESS-D4.02 KAEVREN: "I'm told my guards will be standing the High Kindling crowd in rings. I'm told it by a sergeant who thought I'd ordered it."
ESS-D4.03 [EGH_ORDER_SHOWN] KAEVREN: "The gallery order you brought me carried a mark in the corner. It was the first one I could hold." (he lays it beside the four) "Here's the rest."   → ESS-D4.10
ESS-D4.04 [EGH_WORK_ORDER and not EGH_ORDER_SHOWN] KAEVREN: "You carried a Deepbrand work order out of that gallery. Have you still got it?" (he reads it; he turns it over; he puts his thumb on the corner) "There. I wondered."   → ESS-D4.10
ESS-D4.05 [neither] KAEVREN: "Orders to my officers that never crossed my desk. I've been catching them for a season."   → ESS-D4.10
ESS-D4.10 KAEVREN: (turns the four papers round) "Read them."   {inspect: the intercepts (ESS-I5); ESS_INTERCEPTS; carry-state: the intercepts}
ESS-D4.11 KAEVREN: "The mark. Flame in a square. It's the duct-post stamp for the letter-room under Speaker's Hall. Everything that leaves that cellar by tube gets it."
ESS-D4.12 KAEVREN: "I can't walk into the Speaker's house and open his post. I'm the Marshal. If I do it, it's the Marshal against the Speaker, and the city picks a side by supper."
ESS-D4.13 KAEVREN: "You're not anybody's. That's useful again."
  > "How do I get in?"                            → ESS-D4.14
  > "What do you think is in there?"              → ESS-D4.16
ESS-D4.14 KAEVREN: "Not by the door. There's a man who lives in the pipes and sells what he hears. My clerks call him the Rat." (beat) "He seems to know you. He's been seen at a grille near wherever you've been."   → ESS-D4.15
ESS-D4.15 KAEVREN: "The terraces' service yard. He likes the feed lines. They're warm."   {journal: Find the Cinder Rat in the terraces' service yard.}   → END
ESS-D4.16 KAEVREN: "Paper. I don't guess about the Speaker. I've watched people do it. It never ends well for them." → ESS-D4.14
```

```
ESS-D4.40 [D-S1] (The Marshal's office. The player lays the ribboned bundle on the map table. Kaevren unties it and reads every answer, slowly, in order, the oldest first.)
ESS-D4.41 [D-S1] KAEVREN: (squaring them again) "He asked. Every one of these, he asked."
ESS-D4.42 [D-S1] [ESS_LETTER_READ] KAEVREN: "And the one you left in the case. What did he ask for this time?" (the player tells him) (beat) "'I don't ask what the deep works are for.'" (he says it flat, once) "No. He wouldn't."
ESS-D4.43 KAEVREN: (ties the ribbon; holds the bundle out) "Carry it. If I hold it, it's the Marshal against the Speaker. If you hold it, it's evidence."
ESS-D4.44 KAEVREN: "Informant's fee." (a small purse; he doesn't make a thing of it) "I'd sooner pay you than the Rat. He spends it on keys."   {informant's fee [GD]; step S03 complete; journal: The Ember-Priestess wants you to meet someone at the lamp-house.}   → END
```

### ESS-D5: the Cinder Rat (S03, the service yard, the duct and the letter-room)

```
ESS-D5.01 (The service yard. The feed lines run into the stone with a low roar. At knee height, a grille. A glass half-mask catches the light behind it.)
ESS-D5.02 RAT: (sing-song) "Somebody's walking where the pipes can hear them. Hello, somebody."
ESS-D5.03 [ECW_RAT_SEEN] RAT: "You looked back. At the grille, in the cold ward. Most don't look back. Most don't look at all." (pleased)
ESS-D5.04 RAT: "The Marshal's sent you. He sends a smell of boot polish ahead of everything. What does a warden's hand want with the pipes?"
  > "A way under Speaker's Hall."                 → ESS-D5.06
  > "Kaevren says you sell what you hear."        → ESS-D5.05
ESS-D5.05 RAT: "Sell, trade, borrow, find. Pipes talk. I listen. Sometimes somebody pays me to stop." → ESS-D5.04 options
ESS-D5.06 RAT: "Under the Hall. The old post line. Warm all the way, if you don't mind warm." (beat) "Price."
ESS-D5.07 RAT: "Not coin. A question." (he leans close to the grille; the sing-song goes out of his voice) "The pipes sobbed for you once. Where were you standing?"
  > "Under Cinderwall. At the ward's junction."   → ESS-D5.12
  > "Why do you want to know?"                    → ESS-D5.10
ESS-D5.10 RAT: "Because I asked." (beat) "That's the price. You can pay it or go round by the front door and knock."   → ESS-D5.07 options
ESS-D5.12 RAT: (he goes still behind the glass, completely still, for a long breath)
ESS-D5.14 RAT: "Same place." (flat) "Always the same place."   {ESS_RAT_PAID}
ESS-D5.15 RAT: (and then, bright again, as if nothing was said) "In you come. Mind your head. Mind your knees. Mind everything, really."   {grille opens; the duct}
  > "What's in the same place?"                   → ESS-D5.16
  > (follow him in)                               → END
ESS-D5.16 RAT: (already crawling ahead) "Pipes are open. They always are."   → END   {the Rat never answers this, here or later}
```

```
ESS-D5.20 (The far grille. The Rat sits on his heels in a dry alcove: a blanket, a lamp, a row of keys on a wire.) RAT: "Under the Hall now. Hear it? Nobody walking. Nobody walks here at night but letters."
ESS-D5.21 RAT: (unhooking one key off the wire without looking) "Everything in the pipes comes to me eventually. Keys too."   {carry-state: the Rat's key}
ESS-D5.22 RAT: "Case on the wall. Brass lock. Don't knock the bell on the tube. It rings upstairs."   → END
```

```
ESS-D5.30 [D-S1] (The letter-room, the case open. The player has read the sealed letter.) RAT: (holding a knife-blade in the lamp flame until it shines) "Give it here." (he warms the wax and presses the seal back, neat as new) "Soft wax. He likes soft wax. Takes a good impression."
ESS-D5.31 RAT: (puts the letter back on top in the case) "Take the old ones. Leave the new one."
ESS-D5.32 RAT: "If the new one doesn't go in the morning, somebody comes looking. If the old ones go, he can't tell anyone they're gone." (pleased with that) "Can he?"   {player takes the bundle: item ESS_letters}
ESS-D5.33 RAT: (locking the case; the key back on his wire) "Back the way you came, or up through the yard. I'm staying. It's warm, and the post comes at dawn."   → END
```

### ESS-B3: the Rat's duct (S03)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| ESS-B3.1 | First floor vent | RAT | (ahead) "This one breathes out. Count it. Then go." |
| ESS-B3.2 | Working stretch, entering | RAT | "Warm bit. There's a dip in the wall halfway. I sit in it and think about soup." |
| ESS-B3.3 | Player stands in the niche | RAT | (somewhere ahead, echoing) "That's the soup spot." |
| ESS-B3.4 | The agility drop | RAT | "Jump, or the long way round on your belly. The long way's dustier. I don't judge." |
| ESS-B3.5 | Player leaves the duct midway | RAT | (from the dark) "I'll be at the far end. I'm always at the far end." |
| ESS-B3.6 | Under the Emberhold District, ambient | (none) | (voices through a grate overhead: a kitchen, someone laughing, a pan set down) |

### ESS-D6: resume hooks and later asides

```
ESS-D6.01 [S01–S06 Active, walk-away] SERALYND: "The rehearsals are every dusk. So are my dreams."
ESS-D6.02 [S01–S06 Active, walk-away] SAELIA: (at her cue stand, chalking) "Four. Still four." (beat) "Still five."
ESS-D6.03 [S03 Active, walk-away] KAEVREN: "The mark's still on everything I catch."
ESS-D6.04 [S03 Active, walk-away, ESS_RAT_PAID] RAT: (at his grille) "Pipes are open. They always are."
ESS-D6.05 [S03 Active, walk-away, not ESS_RAT_PAID] RAT: (at his grille) "Price hasn't changed. Prices never do with me."
ESS-D6.10 [ESS_BREATH_CARRIED] SAELIA: (asked about the fifth beat later) "Everyone does. That's what bothers me."
ESS-D6.11 [ESS_BREATH_CARRIED] SERALYND: (asked the same) "I know."
```

### ESS-D7: Serix (S04, the vigil hall)

```
ESS-D7.01 (The vigil hall. Seralynd at the inner door. Beside her, a thin young man, barefoot, ash on his feet, standing as if the floor might move.) SERALYND: "This is Serix Arden. He keeps the sleep rooms below."
ESS-D7.02 SERIX: (soft; certain about nothing but this) "She says you read tells. She says you don't belong to anyone."
ESS-D7.03 SERIX: "I'll take you down. I'd like someone to see what I didn't make."
  > "What didn't you make?"                       → ESS-D7.04
  > "What's down there?"                          → ESS-D7.05
ESS-D7.04 SERIX: "You'll see the column. I'll tell you about it in the room. Not up here." (a glance at the lamps)   → ESS-D7.06
ESS-D7.05 SERIX: "The rooms where people keep vigil. Where they sleep, when they sleep. And the record of it."   → ESS-D7.06
ESS-D7.06 [ESS_SLIP_SEEN] SERIX: (the player mentions Ralenne's slip) (he flinches, small) "Yes. Paper comes from the record room. There's a drawer of it." (beat) "Let me show you the record first. Then ask me."
ESS-D7.07 SERIX: "I'll witness a copy. Nothing leaves the room but a copy. The record is the Covenant's." (firm, for him) "That's what I can do."
ESS-D7.08 SERALYND: "It's his room. And they're my dreams." (she sits on the nearest bench) "I'll wait."
ESS-D7.09 SERIX: "The book first. On the lectern. It's public; anyone can read it. Nobody does."   {inspect: the access book (ESS-I7)}   → END
```

### ESS-B4: the dormitory and the sleep rooms (S04, ESS-E1)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| ESS-B4.1 | Passing the dormitory | SERIX | (he does not look at the cots; he walks faster) |
| ESS-B4.2 | Entering the sleep-room corridor | SERIX | (his breath goes short; the three braziers stand up white) "It's me. It's always me in here." |
| ESS-B4.3 | First Wraiths form | SERIX | (backing into the niche by the cistern) "Water. The ewer. They don't stand up from a wet brazier." |
| ESS-B4.4 | Player fills the ewer | SERIX | "Don't run with it. They'll come for it. Walk." |
| ESS-B4.5 | First brazier doused | SERIX | (a breath that goes all the way in) "One." |
| ESS-B4.6 | Second brazier doused | SERIX | "Two. I can hear myself." |
| ESS-B4.7 | Third brazier doused | SERIX | "Three. That's all of them." (the Wraiths still standing do not go out; they come on) |
| ESS-B4.8 | Fight ends | SERIX | (comes out of the niche; touches the cold rim of the last brazier) "They answer what's in the room. I was in the room." |
| ESS-B4.9 | Player defeated and returns | SERIX | (at the corridor mouth) "The wet ones stayed wet. Go on." |

### ESS-B5: the record gallery (S04, the damper)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| ESS-B5.1 | Gallery rail, first look | SERIX | "The damper. It's jammed open. All the heat from the rooms went up and came down in there." |
| ESS-B5.2 | Gallery rail, the latch inspected | SERIX | "The latch on the iron plate. If it drops, the damper shuts." |
| ESS-B5.3 | Player climbs down while Surging | SERIX | "There's a ladder by the vent. Climb between the breaths. You know how." |
| ESS-B5.4 | Latch shot (`ESS_DAMPER` = shot) | SERIX | (the clang; the room's air goes slack) "Oh. Well done." |
| ESS-B5.5 | Latch pulled (`ESS_DAMPER` = climbed) | SERIX | (as the player comes down the ladder) "You climbed it. Nobody climbs it. I'll tell them to fix the latch." |

### Inspect texts: ESS

| Object | Text | Condition |
|---|---|---|
| Brazier tells in a rehearsal window (ESS-I1) | `EH_TELLS`: "The row's tells have just gone amber, all at once." Then, from the second window on: "Around you the crowd has just breathed in. Together." | Rehearsal window; required ×3 |
| The dormitory (ESS-I8) | `EH_CURRICULUM = guild`: "Narrow cots, some small. Half are stripped to the boards. A notice on the door: *Steadying transfers suspended pending the teachers' guild review.*" / `= evidence`: "Narrow cots, some small, every one made up tight, corners folded square. No notice on the door. Someone has made the beds today." | Optional |
| The sleep-room cot (L3c) | "A cot, a stool for a watcher beside it. The stool is worn smooth where someone has sat a long time." | Optional |
| The vigil cistern | "Cold water, a long iron ewer on a hook." | — |
| The chimney breast | "A flue up from the braziers. High on it, an iron plate with a latch, jammed up. A ladder beside a wall vent." | — |
| The duct-post tube (ESS-I6) | "A brass tube mouth in the wall, a bell on a cord beside it. The routing plate above it is stamped with a flame in a square: the mark on Kaevren's orders." | Required |
| The letter-case | "Dark wood, a brass lock. Inside: one sealed letter on top, and under it a bundle of folded papers tied with a red ribbon, the oldest softer and browner." | — |
| The Rat's alcove | "A blanket, a lamp, a row of keys on a wire. More keys than doors you can think of." | Optional |
| The compare (ESS-I10) | `ESS_SCRIPT_READ` + `ESS_RECORD_READ` + `ESS_COPY`: "Your copy of the record, and the script on Ralenne's lectern. The record: *Kindling less 12, set: one flame, one breath, one city (breath on the fifth)*. The script: the same line, and the breath mark under it, after the fourth beat. The beat the record names." `{ESS_MOTIF_MATCH}` | Required, at the mark, `S05` |

### Document: Saelia's cue sheet (ESS-I2)

> *HIGH KINDLING. Crowd cues. S. Verithe.*
>
> *Lamps* · 2 · 3 · 4 *(lift on 4)*
> *Turn* · 2 · 3 · 4 *(face the balcony on 4)*
> *Raise* · 2 · 3 · 4 *(lamps high on 4; hold for the address)*
> *Response* · 2 · 3 · 4 *(the Magistrix leads; the crowd answers on 4)*
>
> *(in chalk, rubbed and redone in the margin)* *4. FOUR. Not five.*

### Document: Ralenne's script, the line (ESS-I3)

The High Kindling address and responses, many pages, much revised in Ralenne's round, generous hand, with stage notes to herself (*here they will cheer; let them*). Near the end, a line in a different rhythm, copied out in her hand but not in her way of writing:

> *MAGISTRIX:* ***One flame,*** *(beat)* ***one breath,*** *(beat)* ***one city.***
> *(a small mark under the space after "city": a short curve, like a breath taken)*
> *CROWD: One city.*

Production rule: every other line on the page has her crossings-out. This one has none.

### Document: the suggestion slip (ESS-I4)

A narrow slip of good Covenant paper, the kind the lamp-house uses for vigil notes. Unsigned. A dab of soft grey wax at the fold: the lamp-house's vigil wax, the same wax on the lamp-keepers' wick bundles.

> *For the Magistrix, from the vigil.*
> ***One flame, one breath, one city.***
> *(the breath mark, the same small curve, under the space after "city")*
> *Let them take the breath after. They will.*

### Document: Kaevren's intercepts (ESS-I5)

Four orders on Emberguard form paper, each to a named office (never to a person by name), none bearing the Marshal's countersign. Each carries the same stamped routing mark in the lower corner: **a flame in a square**.

> *1. To the officer of the Embergate night watch. Patrols past the Cinderweave lanes to be thinned for the season. Not to be logged with the Marshal's office.*
>
> *2. To the officer of the terrace detail. Two posts on the service yard stair withdrawn after dusk until the Kindling.*
>
> *3. To the officer of the Ashspire watch. Reports of persons missing from the lower wards to be entered as departures.*
>
> *4. To the officer of the terrace detail. At the High Kindling rehearsals, guards to stand the crowd in rings, facing in, and hold their line on the fifth beat. On the night itself, the same.*

Production rule: no order names who issued it. Order 3 is the only one touching disappearances, and says nothing of where anyone went.

### Document: the outgoing letter, *To the Seat* (ESS-I6a) `[D-S1]`

Sealed in soft red wax with the Speaker's flame seal; read in place and returned (`ESS-D5.30`). In the Speaker's own hand: large, warm, fluent, the hand on every public proclamation in the city.

> *To the Seat.*
>
> *I write with thanks. The Kindling will be the fullest in living memory. The terraces are ready and the city is ready to fill them.*
>
> *My vigils have been clear this season. On the long nights I have seen the city as one flame, every ember of it, and I have woken knowing what to say to it. I do not know a greater gift, and I thank whoever has the keeping of such things.*
>
> *The Marshal is restless. He is a good man and a careful one. I would not have him troubled.*
>
> *I do not ask what the deep works are for. I ask that the city not be frightened.*
>
> *In warmth,*
> *the Speaker of the Flame*

`[D-S1]` swap (wholly puppet): the hand becomes a secretary's fair copy, and a line is added at the foot in another hand, *Sealed by the Speaker*; the text is unchanged.

### Document: the kept answers (`ESS_letters`) `[D-S1]`

A bundle of folded papers tied with a red ribbon, the oldest soft and brown at the folds. Every one is in the same small, upright hand that is not the Speaker's. None is signed. None says where it came from. Each begins *Answered:* and quotes his ask back to him.

> *Answered: "a seat at the Council's table, and a vote that carries." It will carry.*
>
> *Answered: "schools where the young can learn the safe crafts." They are yours to open. Open them in your name.*
>
> *Answered: "the terraces on the high holidays." Speak from the spire. The city will come.*
>
> *Answered: "that the vigils be clear." They will be.*
>
> *Answered: "a Kindling the city will remember." It will be the fullest yet.*
>
> *You asked what the deep works are for. They are kept. That is all the Speaker needs.*

Production rule: the asks are in his words, quoted; the answers are never in his hand. Nothing names the Seat, a place, a person, a mine or a date beyond the order of the papers. Nothing shows what the deep works are.

### Document: the vigil access book (ESS-I7)

A heavy public book chained to the lectern. Every vigil night, in many hands: the night, the room, the name of who kept vigil. Read in place.

> *Kindling less 31 · first room · a lamp-keeper (grey)*
> *Kindling less 30 · second room · the Priestess*
> *Kindling less 27 · third room · the Speaker of the Flame*
> *Kindling less 24 · third room · the Speaker of the Flame*
> *Kindling less 23 · second room · the Priestess*
> *Kindling less 20 · third room · the Speaker of the Flame*
> *Kindling less 16 · second room · the Priestess*
> *Kindling less 15 · first room · a councillor (trade)*
> *Kindling less 13 · second room · the Priestess*
> *Kindling less 12 · third room · the Speaker of the Flame*
> *Kindling less 9 · second room · the Priestess*

`{ESS_ACCESS_READ}`. Production rule: other rows (lamp-keepers, citizens keeping a night's vigil) fill the page around these in art; the readable rows are fixed.

### Document: the chamber record (ESS-I9)

A ruled book on the record-room shelf, the Covenant's own, in several hands. Columns: **Night · Room · Sleeper · Set · Hand · Carried · By**. Read in place; the player copies the marked pages (`ESS_COPY`).

**Block S: the Speaker's pages** `[D-S1]` *(working layer; cut under "wholly mastermind", see block P)*

> | Night | Room | Sleeper | Set | Hand | Carried | By |
> |---|---|---|---|---|---|---|
> | *K. less 27* | *third* | *the Speaker* | *the city as one flame* | *full* | *to the spire address* | *C. Vorr* |
> | *K. less 24* | *third* | *the Speaker* | *the young in the safe crafts* | *full* | *to the schools' charter* | *C. Vorr* |
> | *K. less 20* | *third* | *the Speaker* | *the Marshal tired; let him rest* | *full* | *to a letter* | *C. Vorr* |
> | *K. less 12* | *third* | *the Speaker* | *one flame, one breath, one city (breath on the fifth)* | *full* | *to the Magistrix's script by slip, next day* | *S.A.* |

**Block P: the Priestess's nights** *(alternative for D-S1 "wholly mastermind"; under the working layer only the first two rows below are present, as part of the guided-sleepers evidence)*

> | Night | Room | Sleeper | Set | Hand | Carried | By |
> |---|---|---|---|---|---|---|
> | *K. less 16* | *second* | *the Priestess* | *the terraces full at dusk* | *light* | *—* | *C. Vorr* |
> | *K. less 9* | *second* | *the Priestess* | *the city breathing as one* | *light* | *—* | *S.A.* |
> | *[alt only] K. less 13* | *second* | *the Priestess* | *one flame, one breath, one city (breath on the fifth)* | *light* | *to the Magistrix's script by slip, two days after* | *S.A.* |

**Guided sleepers** (a list on its own page):

> *Magister V. Trossen. Light. (Restless; keep it light.)*
> *A councillor of trade. Full.*
> *A councillor of guilds. Full.*
> *The Priestess. Light hand.*
> *Steadying: 12, 17, 23, 31, 38, 44.*

**Not set** (the back pages, in Serix's own hand, smaller):

> *K. less 22 · first room · a lamp-keeper woke and spoke of a door under ash. Not set.*
> *K. less 18 · second room · S.A. (watching) saw a light where the wall is. Not set.*
> *K. less 11 · third room · S.A. (watching) heard breathing that was not the sleeper's. Not set.*
> *K. less 10 · second room · the Priestess woke weeping. Would not say why. Not set.*

`{ESS_RECORD_READ}`. Production rules: *C. Vorr* is never spoken aloud by anyone. *S.A.* is Serix; he says so (`ESS-D8.24`). The steadying numbers are the Molten Stair's student numbers; **40 is not among them**. No row names the Seat, the deep works or anyone outside the city. The "not set" rows are never explained (`[ED-17]`); none is about the player.

### Document: the record copy (`ESS_COPY`)

The player's own copy, in a blank vigil book: the Speaker's pages (block S) and the guided-sleepers list, in the player's hand. Under it, in Serix's small careful hand: *Witnessed, copied from the record this night. S. Arden, initiate.*

### ESS-D8: the record room (S04)

```
ESS-D8.01 (The record room, cooling. Serix comes down the ladder or the gallery stair, whichever way the player came.)
ESS-D8.02 [ESS_DAMPER = shot] SERIX: "I've watched that latch stick for a year. I've never thought to shoot it." / [= climbed] SERIX: "You went up there with the wall breathing at you. I'd have waited for someone to come and mend it. Nobody comes."
ESS-D8.03 SERIX: (takes the book off the shelf; opens it on the desk; turns it to face the player) "The record. Read it. Then I'll answer what I can."   {inspect: the chamber record (ESS-I9)}
ESS-D8.10 [ESS_RECORD_READ] SERIX: (waiting with his hands flat on the desk) "Ask."
  > "Copy it. You'll witness?"                                 → ESS-D8.16
  > [ESS_SLIP_SEEN] "The slip on the Magistrix's lectern came from here." → ESS-D8.12
  > "Who is C. Vorr?"                                          → ESS-D8.14
  > [EEH_LEDGER_READ] "These steadying numbers."               → ESS-D8.44
ESS-D8.12 [ESS_SLIP_SEEN] SERIX: (opens a drawer: slips of the same paper; a cake of the same grey wax) "When a set dream is meant to be carried, someone writes it out and a lamp-keeper takes it where it goes." (beat) "I wrote that one. The night after I sat with him."   → ESS-D8.10 options
ESS-D8.14 SERIX: (he looks at the name and not at the player) "Someone who sets more than I do." (beat) "I won't say it. You've read it. That's enough."   → ESS-D8.10 options
ESS-D8.16 SERIX: "The Speaker's pages. The list. Not the back." (he puts a blank vigil book and a pen beside the record) "Take your time. The ink's slow."   {channel: copy (3 segments, ~4 s each)}
ESS-D8.17 SERIX: (reading the copy against the record, line by line, his finger on each) "Yes. Yes. Yes."
ESS-D8.18 SERIX: (signs under it; blows on the ink) "'Witnessed, copied from the record this night. S. Arden, initiate.'" (he hands it over) "Now it's mine too."   {ESS_COPY; carry-state: the record copy}   → ESS-D8.20
```

```
ESS-D8.20 SERIX: (he sits on the watcher's stool he has brought in from the rooms, as if he wants something under him) "You'll want to know how it's done. Everyone thinks it's a draught or a smoke. It isn't."
ESS-D8.21 SERIX: "You sit with them. You breathe with them, slow, until you're breathing the same. You put a picture in the breath, and you leave it there."
ESS-D8.22 SERIX: "Light hand, they wake and think it was theirs. Full hand, they wake and know what to do with it."
ESS-D8.24 SERIX: "S.A. is me. Most of the nights are someone else's. Some are mine."
  > "And the Speaker?"                            → ESS-D8.30
  > "Do they know?"                               → ESS-D8.26
ESS-D8.26 SERIX: "The light ones don't. The full ones..." (beat) "Some of the full ones asked for vigils. Asking for a vigil isn't asking for a dream. I used to think that mattered."   → ESS-D8.30
ESS-D8.30 [D-S1] SERIX: "He believes it." (quiet) "Every word I give him, he believes."
ESS-D8.31 [D-S1] SERIX: "He thanks me for them without knowing it's me. He says good morning to me on the stair as if I were the one who'd had the good night."
ESS-D8.32 [D-S1] SERIX: "He asks for the vigils. He asks for them clear. He doesn't ask what's in them." (beat) "I don't think he wants to."
ESS-D8.34 [ED-17] SERIX: (he turns the record to the back pages and puts one finger on his own column) "This is what I wanted someone to see." (beat) "Some nights I see things I didn't set. So do some of the people I sit with."
ESS-D8.35 [ED-17] SERIX: "I don't know who sets those. I'm not saying it's anyone." (beat) "I'm saying it isn't me."
ESS-D8.36 SERIX: (closes the record; puts it back on the shelf, exactly where it was) "There. Someone's seen it."   {ESS_SERIX_HEARD}
  > [EEH_LEDGER_READ and not ESS_STUDENTS_SEEN] "The steadying numbers."   → ESS-D8.44
  > "Thank you, Serix."                           → ESS-D8.40
ESS-D8.40 SERIX: "Go up to her. She's been waiting with her hands in her lap the whole time. She does that." (he stays by the shelf)   {step S04 complete; journal: Stand in the rehearsal crowd again at dusk.}   → END
ESS-D8.44 [EEH_LEDGER_READ] SERIX: (the player reads the numbers out: twelve, seventeen, twenty-three, thirty-one, thirty-eight, forty-four) "The school sends them. Children who wake in the night. We steady them. Light hand." (beat) "They sleep better after. I've watched them sleep better."   {ESS_STUDENTS_SEEN; R18 seed}
ESS-D8.45 [ESS_STUDENTS_SEEN] PLAYER (summary line, shown): "There's no forty."
ESS-D8.46 SERIX: "No. Forty was on the list and then struck off. Somebody came and took the name back." (he doesn't know more, and says so with his face)   → ESS-D8.10 options or ESS-D8.36 options (whichever the player came from)
```

`[D-S1]` swap: under "wholly mastermind", cut `ESS-D8.30`–`.32` and the "And the Speaker?" option; `ESS-D8.12` reads "The night after I sat with *her*." and points at block P. Under "wholly puppet", `ESS-D8.32` loses its last sentence.

### ESS-D9: the second rehearsal (S05)

```
ESS-D9.01 (Dusk. The crowd floor. Seralynd on her mark. The player on theirs.) SERALYND: "You found something." (not a question) "Don't tell me yet. Watch it first. Then tell me."
ESS-D9.02 SERALYND: "Ralenne's reading the line tonight. The real one, full voice."   {inspect at the mark: the compare (ESS-I10); ESS_MOTIF_MATCH}
ESS-D9.10 SAELIA: (calling) "Lamps. Two. Three. Four."   {the run; event ess.breath_carried, §B8.1; ESS_BREATH_CARRIED}
ESS-D9.11 RALENNE: (from the lectern, full voice) "One flame. One breath. One city."
ESS-D9.12 CROWD: "One city." (and on the fifth beat, everyone breathes in; the player's own breath with them)
ESS-D9.20 SAELIA: (she stops the run; the lamps waver; she looks straight at the player over the heads) "You breathed with them."
ESS-D9.22 SERALYND: (beside the player, quietly, still looking at the balcony) "Now you know what I've been dreaming."   {step S05 complete; journal: Take what you found to the Ember-Priestess at the lamp-house.}   → END
```

Accessibility subtitle for `ess.breath_carried`: *(you breathe in with the crowd)*.

### ESS-D10: the answer (S06, the vigil hall; the terraces)

```
ESS-D10.01 (The vigil hall, lamps low. Seralynd on a bench. The player sets the record copy between them. Kaevren, in a plain cloak, stands by the street door.)
ESS-D10.02 SERALYND: (she reads the copy without touching it) "The Priestess. Light hand." (beat) "So that's what a light hand feels like. It feels like being right."
ESS-D10.03 KAEVREN: (from the door) "I came as nobody. Nobody saw me come."
ESS-D10.05 [ESS_MOTIF_MATCH] SERALYND: "And the line. Set on the twelfth night out, in the third room, and on Ralenne's lectern the next morning." (beat) "And in my mouth on the terrace. And in yours tonight."
ESS-D10.06 SERALYND: "Somebody has to hear this. You found it. You choose who."
  > "Say it on the terrace. In your own words." (give her the copy)                        → ESS-D10.20 {EH_SPEAKER = challenged}
  > "Take it to the High Magistrate. A sealed inquiry." (keep the copy; go with Kaevren)  → ESS-D11.01 {EH_SPEAKER = exposed}
  > "What would you do?"                                                                   → ESS-D10.10
ESS-D10.10 SERALYND: "They're my dreams. But it's your copy." (beat) "I'll speak if you give it to me. I'll understand if you don't."
ESS-D10.11 KAEVREN: "Vael Trossen reads everything twice and seals what he reads. That's slow. It's also safe." (beat) "The Priestess on a terrace is quick. Nobody can unhear it."   → ESS-D10.06 options
```

**Challenged** `[D-S1]` on the Speaker's lines.

```
ESS-D10.20 SERALYND: (takes the copy; folds it once, the list inside, and puts it in her robe) "I won't read the names. They're not mine to read. I'll say what's mine."
ESS-D10.21 SERALYND: "Tomorrow at dusk. Stand at your mark." (beat) "Stand near me."
ESS-D10.22 KAEVREN: "The letters come to me after. My ledger box. If she's going to say it, somebody had better be holding the paper."   {journal: Stand in the rehearsal crowd at dusk.}   → (keep watch to dusk)
```

```
ESS-D10.30 (Dusk. The crowd floor, full. The Speaker on his balcony. Saelia calls the first cue.) SAELIA: "Lamps. Two. Three—"
ESS-D10.31 (Seralynd leaves her mark and goes up the stair to the rehearsal terrace. Ralenne sees her coming, looks at her face, and steps back from the lectern.)
ESS-D10.32 SERALYND: (not loud; the terraces carry it) "I'm going to say something that isn't in the script."
ESS-D10.33 SERALYND: "I keep vigil for this city. On those nights I've dreamed the Kindling before it came. The lamps, the terraces, all of us breathing as one. I told people it was a gift."
ESS-D10.34 SERALYND: "I've learned that I dreamed what I was given. I believe others here have too." [B14.4: cut this sentence's first half if the Priestess is held off the list]
ESS-D10.35 SERALYND: "Fire remembers. We must remember rightly. A dream that comes on time should be doubted. I'm doubting mine, out loud, so you can see that it doesn't burn."
ESS-D10.36 SERALYND: "Today, when Saelia counts, breathe on your own count. Not mine, not the script's. Your own."
ESS-D10.37 SAELIA: (a long beat; then, steady) "Lamps. Two. Three. Four."
ESS-D10.38 (The crowd lifts its lamps on four. On the fifth beat the breath comes ragged: some in, some out, some laughing. The brazier tells scatter, amber here, clear there. A child in the crowd breathes very loudly on purpose.)
ESS-D10.39 SAELIA: (she puts the chalk down) "That's enough for tonight. Thank you, everyone. That's enough."
ESS-D10.40 CROWD: (murmurs) "What did she mean, given?" / "The Priestess is tired." / "I breathed when I liked. It felt like being late."
ESS-D10.44 [D-S1] SPEAKER: (from the balcony; warm; unhurried; both hands open) "Every ember of Emberholt. Our Priestess has kept long vigils for this city, longer than most of us could. Doubt is a kind of flame too. It shows us where we stand." (beat) "Let's all rest tonight. We'll try again tomorrow, together."
ESS-D10.45 (He smiles down at the crowd, and the crowd, most of it, smiles back. He goes in.)
ESS-D10.46 [D-S1] SPEAKER: (on the stair, passing the player; he stops for exactly one breath) "You stood in my crowd. Thank you for coming, friend." (he goes on down)
ESS-D10.47 SERALYND: (at the foot of the stair; her hands are shaking and her voice is not) "He didn't say I was wrong." (beat) "He didn't say anything."
ESS-D10.48 KAEVREN: (in the crowd, plain cloak; holds out his hand for the bundle) "Ledger box. Under my seal. They'll still be there when somebody needs them."   {item ESS_letters removed; quest Completed; Seralynd keeps the record copy}   → END
```

### ESS-D11: the sealed inquiry (S06 exposed, the Magister's chambers)

```
ESS-D11.01 (Speaker's Hall, the Magister's chambers. A long table, a seal-press, a high window. Vael Trossen stands to receive them, a seal-ring on his hand. Kaevren closes the door.)
ESS-D11.02 VAEL: "Marshal. Warden's hand." (he does not ask why they have come at night) "Put it on the table. I will read all of it before anyone speaks."
ESS-D11.03 VAEL: (the letters first: each answer, in order, then the bundle squared and set aside) "These are not in his hand. The asks they quote are in his words."
ESS-D11.04 VAEL: (the record copy; the Speaker's pages; Serix's witness line) "Witnessed by an initiate. Copied from the Covenant's record. Read against the vigil book, which is public."
ESS-D11.05 VAEL: (the guided-sleepers list. He stops. He reads one line a second time.) "'Magister V. Trossen. Light. Restless; keep it light.'"
ESS-D11.06 (A long silence. He does not sit down.)
ESS-D11.07 VAEL: "I have not slept well this year. I put it down to the work."
ESS-D11.08 VAEL: (he opens a drawer and takes out a short list in his own small hand, and lays it beside the copy) "Cases where the evidence said one thing and the report said another. I have kept it for some time. I did not know what to put at the top of it."
ESS-D11.09 KAEVREN: "And now?"
ESS-D11.10 VAEL: "Now I know what the inquiry is for." (beat) "My name is in it. That is a reason to be slower, not a reason to stop."
  > "What happens now?"                           → ESS-D11.11
  > "Will the city hear?"                         → ESS-D11.12
ESS-D11.11 VAEL: "A sealed inquiry of the Council. The record, the letters and the initiate's witness, under my seal. He will be summoned to the opening. He will come; he always comes."   → ESS-D11.20
ESS-D11.12 VAEL: "Not from me. A sealed inquiry is sealed. That is its strength and its cost."   → ESS-D11.11
ESS-D11.20 (The opening of the inquiry, the next morning. The same room, more chairs. Councillors by office. Kaevren by the door. The Speaker comes in last, in red and black, and greets each of them by name and the player as "friend".)
ESS-D11.21 VAEL: "Speaker. The record of the lamp-house names your vigils and what was set in them. These letters quote your asks. Will you answer?"
ESS-D11.30 [D-S1] SPEAKER: (warmly; to the whole room) "I have kept vigil as every Speaker has. I have never asked the Covenant for a dream."
ESS-D11.31 [D-S1] VAEL: "And the letters?"
ESS-D11.32 [D-S1] SPEAKER: (he looks at the bundle a moment; something passes over his face and is put away) "A Speaker hears from many quarters, Magister."
ESS-D11.33 [D-S1] VAEL: "Who is the Seat?"
ESS-D11.34 [D-S1] SPEAKER: (a smile) "Every ember of Emberholt is my seat." (he thanks the room for its care of the city, and sits, and says nothing more)
ESS-D11.40 VAEL: (when the room is empty; he presses his ring into the wax on the bound papers) "Sealed. The Council knows. The terraces don't." (beat, to the player) "If you think that was the wrong door, you may be right. It is the one I keep."   {item ESS_letters removed; quest Completed; the record copy under Vael's seal}   → END
```

Production rule on `ESS-D11.34`: an evasion, not a lie (he says nothing about who the Seat is). `[D-S1]`: under any ruling the Speaker's three lines stand.

### ESS-B9: post-quest barks (by `EH_SPEAKER`) `[D-S1]`

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| ESS-B9.1 | Crowd floor, dusk | CROWD | `challenged`: "I breathe on my own count now. My wife says I'm always late." / `exposed`: "Lamps, two, three, four. Same as ever." |
| ESS-B9.2 | Crowd floor | CROWD 2 | `challenged`: "The Priestess was tired, that's all. The Speaker said so." (beat) "He didn't say so. He said she'd kept long vigils." / `exposed`: "The Magistrate's been at every rehearsal. Just standing." |
| ESS-B9.3 | Saelia's cue stand | SAELIA | `challenged`: "They don't breathe together any more. Not quite. I like it better." / `exposed`: (she has rubbed the fifth beat off her sheet; she calls four and stops) "Four." |
| ESS-B9.4 | Vigil hall | SERALYND | `challenged`: "Some of the lamp-keepers won't sit with me. Some sit closer." / `exposed`: "The Magistrate asked to keep vigil here. In the first room. With nobody watching." |
| ESS-B9.5 | Vigil hall, inner door | SERIX | "I sleep upstairs now. With the lamps." |
| ESS-B9.6 | Marshal's office | KAEVREN | `challenged`: "Ledger box is heavier. I like it heavy." / `exposed`: "Trossen reads slowly. I've stopped minding." |
| ESS-B9.7 | Ralenne's lectern | RALENNE | "No more slips. I write my own lines now. They're worse." (cheerful) "They're mine." |
| ESS-B9.8 `[D-S1]` | Speaker's balcony, any rehearsal | SPEAKER | (smiling down at his city; when he sees the player he lifts his hand to them, the same as to anyone) |

---

## Part 5: Act II dialogue review

| Check | Result |
|---|---|
| **No reserved decision presented as canon** | `[D-E2]`: both Thalan branches are authored in full and tagged (`EAC-D8.60`–`.66`, `EAC-D9`, `EAC-D10`, branch lines in `EAC-D11`, `EAC-B8`, `EAC-B9`). `[D-S1]`: every assertion of the Speaker's knowledge or intent is tagged (`ESS-I6a`, the kept answers, `ESS-I9` block S/P, `ESS-D4.40`–`.42`, `ESS-D8.30`–`.32`, all his lines). Swap blocks given at `ESS-I6a`, after `ESS-D8`, and in the quest file §B14.1. |
| **R10 withheld** | Nobody says what the frame takes from Thalan. The slate shows marks and duration only. Thalan: "That is mine." |
| **R11 / R12 limits** | The Speaker asked and accepted; he dreams what he is given; he is told he does not need to know the deep works. No endgame, no "Fire Titan", no name for the Seat. One induced case proven by record + access book + slip + letter. The "not set" column keeps Dreamers from being dismissed. |
| **R18 / R19 seeds only** | The fifth beat and the crowd rings (R18) are never explained. Thennek's "awake enough" and the Rat's "Same place" (R19 shadows) are never explained. |
| **Speaker never lies** | Each line checked: thanks, omission, reframing, evasion ("Every ember of Emberholt is my seat"). No denial of anything he wrote. |
| **Combat never reveals evidence** | Every finding is a document, an object, a public book or a living witness. No enemy speaks. |
| **ED-12** | Volkhari speak only of their own lives; nobody describes their community, numbers or refuge. Maeryn's "We're not gone" is self-disclosure, optional. |
| **ED-17** | No player dream. Serix's unset visions are his and his sleepers' only; none is about the player. The breath that carries is presentation, never evidence. |
| **Names** | No NPC says "Remnant", "Fire Titan", Calynne's given name, the initiate's name or the Seat's identity. *C. Vorr* is written once in the record and never spoken. |
| **Other regions** | Not mentioned. |
| **CDR-6** | Every line that sets a flag is per player; partners hear shared ambient barks only. |
