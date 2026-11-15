# Emberholt Main Act III: Cast and Dialogue (Embergate Accounting)

**Status:** Authored production content for Creative Director milestone review (2026-11-14). This is the companion to `04_CONTENT_PRODUCTION/Quests/Caelmor_Emberholt_Main_Act_III.md`, which owns step ids, flags, encounters, mechanics and the epilogue matrix. Characters marked **[CANON ANCHOR]** come from `LORE/Characters/Caelmor_Characters_Region4_Emberholt.txt` and obey the Emberholt rows of the Part 4 character ledger (`00_ADMIN/Reference/Caelmor_Part4_Character_Family_Continuity_Ledger.md`): nothing here gives them a new age, wartime service, kinship, travel or record custody beyond what the ledger allows. Characters marked **[NEW]** come from the Emberholt bible §5.2, from Acts I–II, or are incidental role names. Act III adds **no new named speaking character** (two regulars, Margit and Old Ketta, are only mentioned). Nothing here is production JSON.

**Character rulings, 2026-11-15 (Architecture §5.0).** **D-E2:** Thalan was freed in EH-M4; `EGA-D11.50`, document `EGA-I30` and Dahrin's `EGA-B9.12` are the only version; the aided beat (`EGA-D11.55`–`.58`) and Asera's aided bark are removed. **D-S1:** the Speaker is an idealist and a manipulator, also dream-seeded; his letter (`EGA-I32`), its inspect (`EGA-I33`), `EGA-D13.12`, `EGA-D13.70`–`.80` and barks `EGA-B9.8`–`.9` stand; swap notes removed. **D-EL:** Elyndra's one optional aftermath line, `EGA-B9.13`. Other tags: `[ALLOCATION]` (`EGA-I14` second tag, `EGA-D11.21`/`.22`, `EGA-B1.6`), `[ED-2]` (the fused worker, `EGA-D3`), `[ED-12]` (Volkhari at the board).

**Node format** (Lowmark/Thornfell/Mire/Emberholt Acts I–II standard): `NODE SPEAKER: "Line." (stage note)`; conditions in brackets before the line; player options as `> [condition] "Option." → NEXT {effect}`. Ids follow bible §11.2: dialogue `EGA-D<n>.<nn>`, barks `EGA-B<n>.<nn>`, inspect texts `EGA-I<n>` in tables, documents in full.

**Voice rules (bible §5.3, binding):** civic pride first; criticism comes from inside: "It's our fire. That's why it matters who it warms." Craft, never magic; nobody calls a vein or the main alive (wardens call the main "she", as a crew calls a boat; it is a habit, not a belief). Fire grammar: running warm, banked, flaring, gone grey, backing up. Wardens read tells. **The Speaker never lies:** he thanks, reframes and omits. **Volkhari restraint:** short, guarded; each decides what is said. Children are children. The player is "warden's hand". Other regions are mentioned once (Tessaly Varn, `TAS_ACCOUNT`) and never caricatured. Humour is quick and warm and lives in Cooling Houses and forges. Plain sentences.

---

## Part 1: Act III voice additions

| Item | Status | Use |
|---|---|---|
| **"Hot below. Cold above."** | [NEW] A warden's whole diagnosis of the frost night. | Veska; then the crew and the room. |
| **"She's backing up."** | [NEW] Heat that cannot rise, as opposed to a surge from the vein. | Veska, the line hands. |
| **"You don't shut hot."** | [Act I, NEW] Reused as the rule that orders the night: bleed before you shut. | Veska. |
| **"Bleed a stage before you pass it, or it bleeds you."** | [NEW] | Veska; the line hands. |
| **"Read the frost, not the talk."** | [NEW] Veska's turn on her own saying, once, at dawn. | Veska, once. |
| **"Balanced."** | [NEW] Odile's new word at the foot of the last column. | Odile; then everyone at the gate. |
| **"A remnant."** | [NEW] Yorven's plain word for what is left below. The public word starts here (bible §1.2). | Yorven at the board; then barks. |
| **"The night you kept."** | [NEW] The Speaker's phrase in his letter (D-S1, ruled 2026-11-15). | The letter only. |

**What nobody in Act III says:** what the proving rings were holding for; what "the old circle" keeps; whose hand wrote in the margin; what or who is past the far doors; the words "Fire Titan"; the initiate's name; the precursor's name; how many people work below; anything Thalan said that Asera does not allow; what the Speaker knew; what the sob in the pipes is; that anything is magic, a ghost or a curse.

---

## Part 2: Cast notes

#### Veska Dunmor, Cinderwall fire warden [NEW]
- **In Act III:** leads the crew down; will not choose the relief or the custodian for the player; reads the book over the player's shoulder; watches the boss from the door niche; sits on the plinth after. Never fights (non-combatant; never targetable).
- **Voice:** as Act I: proud, tired, exact, short instructions. At dawn, for once, she looks a long time before she speaks.

#### Yorven Khelt, District Overseer of Cinderwall [CANON ANCHOR]
- **In Act III:** shouts for blankets; pays; carries the account to the Council if the player chooses it (he holds a Council seat as District Overseer, Factions §5). Coins the plain word "remnant" at the board.
- **Limits:** knows tunnels and surges; does not know what the deep works do or who leads them.
- **Voice:** loud, plain, fair; jokes that are orders.

#### Hennet Ulm, Cooling House cook [NEW]
- **In Act III:** feeds a frozen ward; bangs a ladle to quiet a quarrel; carries Thennek's slip (D-E2, ruled 2026-11-15).
- **Voice:** "Sit down; you're running hot." Tonight: "Sit down; you're running cold."

#### Odile Prace, valve-house tallyman [NEW]
- **In Act III:** sends the runner's note; finds every collar number in her book as a repair; writes *balanced*.
- **Voice:** counts aloud mid-sentence. Protective of the book; quietly furious that it was used.

#### The line hands [NEW, role names]
- **LINE HAND 1** (older, slow, has bled every junction in Cinderwall); **LINE HAND 2** (young, quick, frightened of the bore). Non-combatants. One line each at the relief.

#### The fused smelter-hand [NEW, role name] `[ED-2]`
- **Role:** a forge worker with ember-veined forearms from unstable stone; cold, frightened, ashamed of flaring in front of people. **Never targetable; never an enemy.** Speaks a little once steadied.

#### RED DOOR HEALER [Act I role]
- Counts breaths; firm, unsentimental. "In. Hold. Out. Again."

#### The Cinder Rat [CANON ANCHOR]
- **In Act III:** one appearance at a grille; "Still the same place." Never explained.

#### Durnan Volkryst, Forge-Master of the Basalt Forge Guild [CANON ANCHOR]
- **Canon:** guild pride; the guilds resent deep interference and keep pre-war techniques.
- **In Act III:** takes the account with `guilds`; reads it to the forge hands; offers a master commission.
- **Limits:** never a villain; knows forging, not the deep works.
- **Voice:** big, gravelly, measures everything in hammer-blows. "We'll know whose hands."

#### Vael Trossen, Magister [CANON ANCHOR]
- **In Act III (`council`):** reads the account into the Council's book before anyone speaks.
- **Voice:** precise, slow, every sentence finished.

#### Ralenne Kharveil, Magistrix [CANON ANCHOR]
- **In Act III:** at the Council table (`council`), one line; her clerk at the board with `settled` `[ALLOCATION]`.

#### Kaevren Thalos, Grand Marshal [CANON ANCHOR]
- **In Act III:** at the board with `kept`; his second ledger. At the Council reading as a guest, one line.

#### Idra Callow [NEW]; Hesper Tolk [NEW]; Darven Mott [CANON ANCHOR]; Maeryn Vall, Seredh Embercarver, Asera of the Three Breaths [CANON ANCHORS] `[ED-12]`; Tessaly Varn [NEW, Thornfell bible]
- At the board only, by flag (quest file §9.5). Each says one or two lines within their Acts I–II limits. Volkhari decide what is said.

#### The Flameward Speaker [CANON ANCHOR] (D-S1, ruled 2026-11-15)
- **In Act III:** a letter, and a lifted hand from a balcony in the epilogue. Never present at the board or the reading. The letter is sincere civic warmth and a man taking the city's moment as his to teach, at once; it shows no knowledge of the draw or the endgame.

#### Minor Act III cast
- **RUNNER** (valve house), **RUNNER 2** (Speaker's Hall), **REGULAR** (several), **CHILD** (arrival lane), **DROSS SCAVENGER**, **SLINGER** (pre-fight only; nothing after), **COUNCIL CLERK**, **FORGE HAND** (several), **CREW CHIEF**, **GATE STREET** (crowd voices).

---

## Part 3: EH-M6 Embergate Accounting (`EGA`)

### EGA-B0: arrival barks (Cinderwall in frost)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EGA-B0.1 | Entering the lane | REGULAR | (two coats, stamping) "Second coat's back on. I'd only just got used to having arms." |
| EGA-B0.2 | Lane | CHILD | (blowing on a doorway lantern) "It won't take. My fingers are too cold to be cross." |
| EGA-B0.3 | Lane, near the chalked door | REGULAR | "Cooling House is warm. That's the only warm thing in the ward. Go on." |
| EGA-B0.4 | Lane, passing a hood | REGULAR | "Hood's hot to the touch and the room under it's freezing. Explain that, warden's hand." |

### EGA-D1: the warming house (S00_frost)

```
EGA-D1.01 (The Cooling House, packed. Breath in the air. HENNET ladling. YORVEN at the door with an armful of nothing.)
EGA-D1.02 YORVEN: "Blankets! Somebody find me blankets that aren't on somebody!" (sees the player) "Warden's hand. You've a talent for coming on the bad nights."
EGA-D1.03 VESKA: (under the hood, arms folded, looking up at the tell) "Look at that."   {player inspects the hood tell: EGA-I2}
EGA-D1.04 VESKA: "Hot below. Cold above. She's not surging. She's backing up."
EGA-D1.05 YORVEN: "Same as the first night you walked in here. Worse. Then it was an order. Tonight nobody's ordered anything."
EGA-D1.06 (RUNNER comes in stamping frost off his boots, a folded note in his glove.) RUNNER: "From the gate. Odile Prace. She said give it to Dunmor and then to whoever Dunmor gives it to."   {document: EGA-I1}
EGA-D1.07 VESKA: (reads it twice; hands it to the player) "Read the tell, not the talk. That tell says the heat's under our feet and can't get up."
EGA-D1.08 VESKA: "Every vein open since noon and the ward gets nothing. It's gone somewhere. It's been going somewhere for years, and tonight there's not enough left over to hide it."
  > "I'll go down with you."            → EGA-D1.10 {S00_frost complete; the quest has been Active since the Cinderwall entry}
  > "Gone where?"                       → EGA-D1.09
  > "Not now."                          → EGA-D1.90
EGA-D1.09 VESKA: "Odile's 'old leaks'. Never balanced. Weather, she calls it." (beat) "Weather doesn't take more than the whole of Cinderwall in one afternoon."   → EGA-D1.08 options
EGA-D1.10 VESKA: "Not yet. The room first. Then we go down."
EGA-D1.11 HENNET: (pushing a bowl at the player) "Sit down; you're running cold. Then stand up; I need hands."   {journal: Get the warming house through the first hours.}   → S01
EGA-D1.90 HENNET: "Then sit and eat. The frost'll wait for you; it's patient." → END   {re-offer: YORVEN at the door: "Still backing up. Still need you." → EGA-D1.08}
```

### EGA-D2: Hennet and the supper (S01)

```
EGA-D2.01 HENNET: (at the hearth, three empty pails on hooks) "Night crews and the old ones on Kiln Stair can't come here. Supper goes to them. In pails. Hot when it gets there."
EGA-D2.05 [ESP Completed] HENNET: "You know this one. Pails, lids, salt last."
EGA-D2.06 HENNET: "Cook me three pails, or stand at my hatch and hand out bowls till the bell. Either way I get a pair of hands."
  > "I'll cook." (Cooking ~[GD: mid])            → EGA-D2.10
  > "I'll work the hatch."                       → EGA-D2.20
EGA-D2.10 HENNET: "Store's there. Hearth's hot; it's the only hot thing that's honest about it."   {Cooking interactions: three pails of shift supper}
EGA-D2.12 HENNET: (lifting a lid, sniffing) "That'll walk up Kiln Stair and still burn somebody's tongue. Good."   {EGA_SUPPER = cooked}
EGA-D2.20 HENNET: "Bowl in, bowl out. Don't let Margit take three. She'll try."   {held interaction at the hatch; one turn of the hour; dusk → night}
EGA-D2.22 HENNET: (as the bell goes) "That's a shift. You've a cook's arms now. I'm sorry."   {EGA_SUPPER = served}
EGA-D2.30 [EH_COMMONS] YORVEN: (reading the rota slate on the store door) "'Warming house: opened, cots laid, H.U.'" (beat) "The rota beat me to it. First Cooling did that. Thank whoever cooked."   {EGA_BLANKETS}
EGA-D2.31 [not EH_COMMONS] YORVEN: "Blankets. Commons store, behind the wash-house. Two armfuls. Don't stop to chat; the store's colder than here."   {journal: Fetch blankets from the Heat Commons store.}
EGA-D2.32 [not EH_COMMONS; second armful delivered] YORVEN: "That's cots for the old ones. Good."   {EGA_BLANKETS}
```

Production note: "Kiln Stair", "Margit" and "Old Ketta" are incidental: a lane and two regulars never met. Cut any of them if they collide with later naming. ("Old Dace" was renamed in independent review: Dace is a Lowmark character.)

### EGA-B1: the warming house (S01)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EGA-B1.1 | Quarrel starts (supper and blankets done) | REGULAR | "It's the wardens again. It's always the wardens." |
| EGA-B1.2 | Quarrel | REGULAR 2 | "It was an order last time. A salon wanted it warm. Maybe they want it warm again." |
| EGA-B1.3 | Quarrel | REGULAR | "Then let's go up and sit in their doorways. See how warm they keep." |
| EGA-B1.4 | Quarrel, hood tell brightens | REGULAR 3 | (pointing up) "Look at the hood. Look what you're doing to it." |
| EGA-B1.5 | After the containment | HENNET | (bangs the ladle on the pot once; the room goes quiet) "Heat follows the room. So does cold. Eat." |
| EGA-B1.6 `[ALLOCATION]` | Warming house, after the quarrel | REGULAR | `posted`: "Veska's page is still on our board from last time. Nobody's blaming her tonight." / `settled`: "Coal came from the Magistrix last week. Didn't come this week. Frost's early." |
| EGA-B1.7 | Warming house, `EGA_SUPPER = cooked` | REGULAR | "Pails went up Kiln Stair. Old Ketta says the salt's right." |

### EGA-D3: the fused smelter-hand (S01) `[ED-2]`

```
EGA-D3.01 (At the end bench, the FUSED SMELTER-HAND pulls the blanket tight. The ember-veins along his forearms brighten as the quarrel rises. The blanket's edge smoulders. People pull back. The RED DOOR HEALER is already crouched by him.)
EGA-D3.02 FUSED SMELTER-HAND: (through his teeth) "Not again. Not in here. Get them back."
EGA-D3.03 HEALER: (to the player, not looking up) "The hood. Shut his damper. Then sit by him. Don't touch his arms."
      {player shuts the hood damper over the bench: one interaction; the zone drops a band; the smoulder stops}
EGA-D3.10 HEALER: "Good. Now sit. Talk to him. Anything. I'll count."
      {3-segment channel, ~4 s each: sit with him}
EGA-D3.11 [segment 1] HEALER: "In. Hold. Out." FUSED SMELTER-HAND: "It's the cold. It does it worse in the cold. Nobody believes that."
  > "I believe it."                          → EGA-D3.12
  > "What's your work?"                      → EGA-D3.13
EGA-D3.12 FUSED SMELTER-HAND: "You'd be the only one this side of the forge." (a breath) "Thanks."   → EGA-D3.20
EGA-D3.13 FUSED SMELTER-HAND: "Smelter. Was. Bad stone, one shift. Twelve years ago." (a breath) "I can still pour. They won't let me."   → EGA-D3.20
EGA-D3.20 [segment 2] HEALER: "In. Hold. Out. Again." (the veins dim a little)
EGA-D3.21 FUSED SMELTER-HAND: "Is it the wardens? Like they say?"
  > "No. It's under us. We're going down to find it."   → EGA-D3.22
  > "Nobody knows yet."                                  → EGA-D3.22
EGA-D3.22 FUSED SMELTER-HAND: "Then go and find it. I'll stop scaring the room."
EGA-D3.24 [segment 3] HEALER: "In. Hold. Out." (the veins settle; the blanket stops smoking) "There. He's banked."   {EGA_FUSED_STEADIED}
EGA-D3.25 FUSED SMELTER-HAND: (embarrassed, to the room) "Sorry." (to the player) "Is there soup?"
EGA-D3.26 HENNET: (already bringing it) "There's always soup."
EGA-D3.30 VESKA: (at the stair door, two LINE HANDS behind her, a crew lamp lit) "Now we go down."   {journal: Follow the main down.}   → S02
```

Production rule: no option, prop or bark makes the smelter-hand an enemy, a danger to be removed, or a curiosity. People pull back because a blanket is smouldering, and come back when it stops.

### Inspect texts: the warming house and the lane (S00–S01)

| Object | Text | Condition |
|---|---|---|
| Odile's note (EGA-I1) | Document below. | Given at `EGA-D1.06` |
| The hood tell (EGA-I2) | `EH_TELLS`: "Red, crazed. The line under this room is running hot. None of it is reaching the room." | Required (`EGA-D1.03`) |
| The rota slate (EGA-I4) | `EH_COMMONS`: "*Warming house: opened, cots laid, H.U.* Under it, in other hands, a list of who's on which bench tonight." / otherwise: "*Blankets: store. Two armfuls a house.* Nobody has signed for tonight." | — |
| The fused worker's bench | "A blanket with a scorched edge. A bowl. Nobody else sits on this bench." | After `S01` |
| The chalked door (lane) | "*COOLING HOUSE IS WARM*, and an arrow. Somebody has added *ish*." | — |

### Document: Odile's note (EGA-I1)

Folded twice, valve-house paper, Odile's quick upright hand, a smear of chalk on the fold.

> *Dunmor.*
>
> *Intake at full. Every vein open since noon.*
> *Draws to the wards: near nothing. Cinderwall: nothing.*
> *Old leaks: more than the whole of Cinderwall, every hour since noon.*
>
> *It has gone somewhere. It is not coming up.*
>
> *O.P.*

### EGA-D4: Veska on the line (S02)

```
EGA-D4.01 VESKA: (at the stair niche; she breaks the ice in the trough with the ladle and drinks) "Never pass a niche without touching water. Even tonight. Especially tonight."
EGA-D4.02 VESKA: "Three stages between here and the bleed house. Each one's got a stage cock. You bleed a stage before you pass it, or it bleeds you."
EGA-D4.03 VESKA: "My lads go niche to niche. They don't fight. If something wants a fight, that's you."
EGA-D4.04 LINE HAND 1: "I've bled every junction in this ward. Never bled a stage in a frost."
EGA-D4.05 LINE HAND 2: "I've never been below the junction." (beat) "Is it bad below the junction?"
EGA-D4.06 VESKA: "It's warm below the junction. That's the problem."
EGA-D4.08 VESKA: "Read the tells. Red, don't touch. Amber, walk and touch water after. Clear, you don't need me."
EGA-D4.10 [EAC_PLATE_READ] VESKA: "Plates? Down there? Then you know what red means under your feet."
```

```
EGA-D4.20 (Stage A: after EGA-E1; at the stage cock, its handle missing.)
EGA-D4.21 VESKA: "They took the handle. Of course they took the handle. Brass is brass." (nods at the sack) "Find it. Fit it. Bleed it."
      {player takes the handle from the sack (EGA-I6), fits it, bleeds stage cock A (3-segment channel)}
EGA-D4.22 VESKA: (as the tells drop to amber) "That's A. She'll let us by."
```

```
EGA-D4.30 VESKA: (at the warden door below the junction; the brick bore beyond) "This is what the main was laid on. War bore. Don't touch the brick; it's hotter than the pipe."
EGA-D4.31 LINE HAND 2: "Who dug it?"
EGA-D4.32 LINE HAND 1: "People who wanted heat somewhere quick." (beat) "Same as us."
```

```
EGA-D4.40 [ESS_RAT_PAID] (At the second niche, a grille high in the wall. Behind it, a glass half-mask catches the crew lamp.) THE CINDER RAT: "Warden's hand. Pipes are loud tonight." (sing-song; then flat) "Still the same place."   {EGA_RAT_GRILLE}
EGA-D4.41 (He is gone. Nobody comments. If the player asks Veska:) VESKA: "Rats. Pipes. Same thing, tonight."
```

```
EGA-D4.45 VESKA: (at stage cock B, after EGA-E2) "B. Same as A. Slower; she's hotter." {bleed stage cock B}
EGA-D4.50 VESKA: (entering the bleed house; the room red and shimmering; the crew into the niches) "Bleed house. Every relief in Cinderwall goes up from here." (beat) "And past it, everything's red. Nobody works past this room till one of those wheels turns."   → S03
```

### EGA-B2: the descent (S02)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EGA-B2.1 | Duct run, missing brass | LINE HAND 1 | "Brackets stripped all along here. Somebody's been busy while we were cold." |
| EGA-B2.2 | Vent gallery, frost on the upper grate | LINE HAND 2 | "Frost on the top, sweat on the bottom. I don't like a pipe that can't decide." |
| EGA-B2.3 | Old conduits, fast vents | VESKA | "She's breathing quick. Count it. Go on the out-breath." |
| EGA-B2.4 | Player passes an unbled stage | VESKA | "We're not following you through red. Bleed it, or go alone and come back cooked." |
| EGA-B2.5 | Player stands in a niche | VESKA | "Water. Then go." |
| EGA-B2.6 | Player touches the bore brick | LINE HAND 2 | "She said don't touch the brick!" |

### EGA-B3: Dross Scavengers (S02, EGA-E1)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EGA-B3.1 | Player seen | DROSS SCAVENGER | "Warden's lot. Brass is ours tonight. Pipe's dying anyway." |
| EGA-B3.2 | Player seen | SLINGER | (whirling) "Off the grate!" |
| EGA-B3.3 | Fight, a scavenger knocked onto a breathing grate | DROSS SCAVENGER | (no line; a grunt) |
| EGA-B3.5 | Fight over | VESKA | (from the niche; quiet) "Brass from a dying pipe. They weren't wrong it was dying." (beat) "The handle'll be in that sack." |

Production rule: no line after the fight from any scavenger; nothing in the sack but brass and the handle (CDR-1 §3.1.3; combat never reveals evidence).

### Inspect texts: the descent (S02)

| Object | Text | Condition |
|---|---|---|
| Stripped brackets (EGA-I5) | "Bright metal where brass fittings were bolted. Pry marks. Fresh." | — |
| The sack (EGA-I6) | "Stripped brass: elbows, nuts, a gauge with its glass broken. And a cock handle, warden's pattern." | Take the handle (carry-state) |
| Stage cock A (EGA-I7) | `EH_TELLS`: "A stage cock on the down-line. Red, crazed. No handle." / after fitting: "Red, crazed. Bleed it." | — |
| The junction tells (EGA-I8) | `EH_TELLS`: "Every bead on the manifold red. She isn't surging from the vein; the pipe from below is the hot one. Backing up." | — |
| The grille (EGA-I9) | "An old duct meets the bore here. The grille's bars are bent outward at one corner, enough for someone small." | — |
| Stage cock B (EGA-I10) | `EH_TELLS`: "A stage cock in the bore, red and crazed. A warden's chalk board beside it: *Stage B. Bleed before passing.*" | — |
| The bore brick | "Old brick, laid round. Hot through a glove. The civic pipe is bracketed along one side, newer by thirty years." | — |

### EGA-D5: the bleed house (S03)

```
EGA-D5.01 VESKA: (at the three relief wheels, the room red round them) "You don't shut hot. Everything past this room is splices and a junction, and we shut none of it till the pressure's somewhere else."
EGA-D5.02 VESKA: "One relief. Two and neither carries; the main drops and the ward freezes solid."
EGA-D5.03 VESKA: "Ward. Terraces. Forges." (she taps each tag) "Read them."   {player inspects the tags: EGA-I13, EGA-I14, EGA-I15}
EGA-D5.10 [inspected WARD] VESKA: "Ward's the short way. Our own risers. Warm in an hour. Our pipes take the heat all night, and some of them won't like it."
EGA-D5.12 [inspected TERRACES] VESKA: "Terraces. Open stone. Nobody sleeps there. Safest place in the city to put a night's heat." (beat) "And the whole city watches it glow while we sit in the dark till we've shut what's under us."
EGA-D5.14 [inspected FORGES] VESKA: "The great hearths can hold it. The forges bank their work and open their halls." (beat) "And lose a night and a rack of crucibles, and remember who sent it."
EGA-D5.24 [inspected FORGES; EH_GUILDS = reformed] VESKA: "Durnan's new rules. They keep a relief seat open for wardens now. They'll take it without a word."
EGA-D5.25 [inspected FORGES; EH_GUILDS = restored] VESKA: "Old rules up there. 'By order only.' They'll take it. They'll bill the ward."
EGA-D5.30 VESKA: (stepping back from the wheels) "I've had a ward blamed on me once. Tonight it's your hand on the wheel. Pick the one you can say out loud in the morning."
EGA-D5.31 LINE HAND 1: "I'd send it up our risers. It's our heat. Our hoods'll crack, and we'll mend them."
EGA-D5.32 LINE HAND 2: "I'd send it where nobody's sleeping. Let them see it glow. Let them ask why."
  > (Turn the WARD wheel.)                      → EGA-D5.40 {EH_HEAT_MAIN = ward}
  > (Turn the TERRACES wheel.)                  → EGA-D5.42 {EH_HEAT_MAIN = terraces}
  > (Turn the FORGES wheel.)                    → EGA-D5.44 {EH_HEAT_MAIN = forges}
  > "What would the board say?"                 → EGA-D5.33
EGA-D5.33 VESKA: "The board says where it went. It doesn't say if you were right."   → EGA-D5.30 options
EGA-D5.40 (Confirm: "Send the night's heat up Cinderwall's risers?") VESKA: "Our heat, our hoods. Turn her."
EGA-D5.42 (Confirm: "Send the night's heat to the Ash Terraces?") VESKA: "Nobody sleeps on a terrace. Turn her."
EGA-D5.44 (Confirm: "Send the night's heat to the great forges?") VESKA: "The hearths can hold it. Turn her."
      {the wheel turns; the line roars; the other two wheels lock; the bleed house drops to Working (amber); EGA-E3: beetles out of the floor vents}
EGA-D5.50 VESKA: (after EGA-E3; at the wheel, which is trying to close) "She wants to shut. Pressure's pushing her shut. Something has to hold her open."
EGA-D5.51 VESKA: "Those wedges in the crate are cracked. Forge new ones, or we hold her by hand for two breaths of that vent and she'll seat herself."
  > "I'll forge wedges." (Smithing ~[GD: mid-high])   → EGA-D5.52
  > "Hold her. I'll call the vent."                   → EGA-D5.55
EGA-D5.52 VESKA: "Three. Thick end, short taper. Quench them hard."   {field forge: heat, shape, quench ×3; drive three wedges (3-segment channel)}
EGA-D5.53 VESKA: (as the last wedge goes in) "That's held. She'll stay."   {EGA_BLEED_WORK = wedges}
EGA-D5.55 VESKA: (to the line hands) "Shoulders." (to the player) "Call the out-breath. We push on the out."   {held interaction per vent cycle ×2}
EGA-D5.56 VESKA: (after two cycles, panting) "She's seated. Don't let go yet." (beat) "Now let go."   {EGA_BLEED_WORK = held}
EGA-D5.60 VESKA: (the tells in the run beyond dropping to amber) "That's somewhere else now. Let's go and see what's been taking it."
EGA-D5.62 [EGA_BLEED_WORK = wedges] LINE HAND 1: "Good wedges. I'll keep one." / [held] LINE HAND 2: (rubbing his shoulder) "I'll feel that tomorrow. Worth it."   → S04
```

### EGA-B4: the bleed house (S03, EGA-E3)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EGA-B4.1 | Beetles out of the vents | VESKA | "Off the grates! They're coming up with the heat." |
| EGA-B4.2 | Wave 2 | LINE HAND 2 | (from the niche) "More! Under the forge!" |
| EGA-B4.3 | Player tries a locked wheel | VESKA | "One's enough. One's all she'll carry." |
| EGA-B4.4 | Player tries the relief before both stage cocks are bled | VESKA | "Stage B is still holding. It'll fight you." |

### Inspect texts: the bleed house (S03)

| Object | Text | Condition |
|---|---|---|
| The crew slate (EGA-I11) | "Years of chalk. *Bled to ward. Bled to baths. Bled to forges. Bled to ward.* Nobody has ever chalked *terraces*." | — |
| The wedge crate (EGA-I12) | "Old bleed wedges, every one cracked across the taper. Somebody kept them anyway." | — |
| WARD relief (EGA-I13) | `EH_TELLS`: "*WARD. Cinderwall risers.* Red, crazed. This one goes straight up under the lanes." | Required (at least the one turned) |
| TERRACES relief (EGA-I14) | `EH_TELLS`: "*TERRACES. Emberhold line.* Red, crazed." `[ALLOCATION]` second line: "Beside it, newer, a brass tag stamped *ceremonies office*. The line the nine nights went up." | — |
| FORGES relief (EGA-I15) | `EH_TELLS`: "*FORGES. Great hearth line.* Red, crazed." `EH_GUILDS = reformed`: "A newer tag: *Relief seat held for wardens. D.V.*" / `restored`: "An older tag: *By order only. Billed.*" / unset: no second line. | — |
| A locked wheel (after the choice) | "The ward has its relief. One's enough." (wording by the relief turned: "The terraces have…", "The forges have…") | — |

### EGA-D6: the splices (S04)

```
EGA-D6.01 VESKA: (at the first collar with a second clamp; she puts her lamp close) "That's not a repair."   {player inspects: EGA-I16}
EGA-D6.02 VESKA: "City collar. Valve-house plate. Our pattern, our numbers." (she taps the clamp) "And that's theirs. Deepbrand's mark on the clamp. Ours on the outside and theirs on the inside."
EGA-D6.03 VESKA: (she takes a spanner from her belt and unbolts the number plate) "Odile will want these. They're her numbers."   {carry-state: collar plate 1; EGA-I17}
EGA-D6.04 VESKA: "Now you can shut it. She's not hot any more."   {3-segment channel: shut the splice}
EGA-D6.05 [second splice] VESKA: "Another." (unbolting) "Every forty paces. Like they were laying a main of their own inside ours."
EGA-D6.06 [third splice] VESKA: (she doesn't say anything; she unbolts the plate and hands it over and looks down the run)
EGA-D6.08 [splice valve tried before the relief] VESKA: "You don't shut hot." (a scald, a step back)
```

### EGA-D7: the fitter's cabin (S04)

```
EGA-D7.01 (A side room. A cot, a cold brazier, a bench. On the bench, a book in oilcloth.)   {player takes the junction book; EGA-I21; item EGA_junction_book}
      {player reads it: EGA-I22; EGA_BOOK_READ}
EGA-D7.02 [EAC_SLATE_READ] (journal line on reading the draw-holds page) "You've read this heading before."
EGA-D7.03 VESKA: (reading over the player's shoulder, the lamp held up) "'For the proving rings.' I don't know what a proving ring is." (beat) "I know what a quarter-hold is. That's a quarter of a ward."
EGA-D7.04 VESKA: (she stops at a line and puts her finger on it) "'Hold anyway.'" (beat) "They knew the main wouldn't carry it. They knew what that meant up top. And they wrote 'anyway'."
EGA-D7.05 VESKA: "'Doors to be barred from the deep side at first frost.'" (she looks at the cabin door, then down the run) "First frost was yesterday."
  > [EGA_HAND_MATCHED] "I've seen this hand before. In the Red-Lit annex."   → EGA-D7.08
  > "Let's see the junction."                                                → EGA-D8.01
EGA-D7.08 VESKA: (she looks at the margin a long moment) "Then whoever keeps old papers keeps new ones." (beat) "I'm a warden. I read beads. Show it to someone who reads hands."   → EGA-D8.01
```

### Inspect texts: the splice run and the cabin (S04)

| Object | Text | Condition |
|---|---|---|
| A splice collar (EGA-I16) | `EH_TELLS`: "A city-pattern collar on the main, a brass number plate stamped like every plate at the valve house. Over it, a second clamp, newer, with a branch pipe turning down into the floor. Deepbrand's mark on the clamp. Amber." | Required, each |
| A collar plate (EGA-I17) | "A brass number plate, valve-house stamp. Plate 1: *C-114*. Plate 2: *C-131*. Plate 3: *C-147*." (by plate) | Carry-state |
| The pegboard (EGA-I18) | "Spare number plates, city pattern, unstamped. Enough to fit a main." | — |
| The shift slate (EGA-I19) | "A slate wiped clean except one word in the corner: *barred*." | — |
| The book's cover (EGA-I21) | "Oilcloth round a ruled book. Deepbrand's mark burnt into the cover. Inside the cover: *Junction book. Civic main, lower works.*" | Take (item) |
| The margin (EGA-I23) | `EGH_KEEP_SEEN`: "*Keep the draw. Do not log.* The slope, the ink and the way the K is made are those of *Keep. Do not copy.* on the Red-Lit wrapper. Nobody signed it." | Optional; sets `EGA_HAND_MATCHED` |

Production rule for the plates: the numbers are fixed art (three plates), not a count of anything else.

### Document: the junction book (EGA-I22; `EGA_junction_book`)

A ruled book, oilcloth-wrapped, Deepbrand's mark burnt into the cover. Entries in two or three fitters' square hands across years, the older pages soft and grey. Read in the cabin (required).

> *Junction book. Civic main, lower works.*
>
> | Collar | Set as | Draw | For |
> |---|---|---|---|
> | *C-114* | *repair* | *quarter* | *proving rings* |
> | *C-131* | *repair* | *half* | *proving rings* |
> | *C-147* | *repair* | *half, full hold in series* | *proving rings* |
> | *Frame line* | *(deep side)* | *no draw* | *Fitter to attend.* |
>
> *Enter every collar at the valve house as repair, deep-works contract. Use their plates. Use their clerks.*
>
> ---
>
> ***Perfect Flame: draw holds.***
>
> *Hold each ring's draw through the series. Take from the civic main below the lower ward.*
>
> *Lower forge undercourse: do not draw. The old circle keeps this season.*
>
> *Ordinary winter: the main carries the holds. The board reads it as leaks.*
>
> *Hard frost: the main will not carry the holds. Hold anyway. Next series after the Kindling.*
>
> *(margin, another hand:) Keep the draw. Do not log.*
>
> ---
>
> *Doors to be barred from the deep side at first frost. Leave the junction to its keeper.*

Production rules: no person is named, counted or described; no precursor name; the margin hand is unsigned (D-C03). *Perfect Flame* is a heading only (bible §1.2; FT-04). "The old circle keeps this season" is the bible's fixed R19 seed line: nothing in the book, in any line, or in any bark says what keeps, what the circle holds, or anything about a Titan, an initiate or a binding (FT-05; R19 is CV-M4's). *Frame line: no draw. Fitter to attend.* is true in both branches and is not tagged. "Next series after the Kindling" matches the EH-M4 slate (R18 seed; never explained).

### EGA-D8: the far doors (S05)

```
EGA-D8.01 VESKA: (at the door niche outside the grille; she does not go in) "That's not ours."   {player inspects the construct: EGA-I20}
EGA-D8.02 VESKA: "It's standing on our valve like it owns it." (beat) "Don't touch the valve till you've seen where it goes. Then we'll know what we're shutting."
      {player crosses the floor to the far doors; inspects: EGA-I24, EGA-I25; optional listen}
EGA-D8.05 [listen] (Nothing. No footsteps, no voices. Only the hum of the joined line going down through the stone.)
EGA-D8.10 VESKA: (from the door niche, when the player turns back) "Barred?"
  > "From the other side."                 → EGA-D8.11
  > "Warm, and barred. Nobody's there."    → EGA-D8.11
EGA-D8.11 VESKA: "Before the frost. The book says so." (beat) "They didn't run from us. They went before anyone came."
EGA-D8.12 LINE HAND 2: (from behind her) "Where does it go?"
EGA-D8.13 LINE HAND 1: "Down."
EGA-D8.14 VESKA: "Whatever's past that door, it's not tonight's. Tonight's that valve." (she nods at the construct) "And that."   → S06
```

### Inspect texts: the splice junction (S05–S06)

| Object | Text | Condition |
|---|---|---|
| The dormant construct (EGA-I20) | "Embersteel plates over dark seams. A valve-wheel set in its chest, coupled by a rod to the draw valve. It is standing still. It is waiting on something." | Before `S06` |
| The far doors (EGA-I24) | "Iron doors where the four draw lines, joined into one, go through the wall. Warm to the hand. Barred from the far side: you can hear the bar seat when you push, and see a fresh scrape where it dropped." | Required; sets `EGA_DOORS_READ` |
| The chalk (EGA-I25) | "Chalk on this side, wiped with a sleeve. One corner of a mark is left: part of a ring." | — |
| The draw valve (EGA-I26) | `EH_TELLS`: "A great valve on a plinth where four channels meet. Red, crazed. A rod runs from its stem to the construct's chest." / after the fight: "Amber. Shut it." | Touch to begin `S06` |
| The fallen Sentinel (after) | "Cold. Locked mid-turn. The wheel in its chest won't move." | — |

### EGA-B5: the Draw Sentinel (S06, EGA-E4)

Veska speaks from the door niche outside the grille; she is never in the arena.

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EGA-B5.1 | Wake | VESKA | "Keeper! Get off the valve!" |
| EGA-B5.2 | P1, player hitting it with four collars open | VESKA | "It's drinking from the collars. Shut them. Starve it." |
| EGA-B5.3 | P1, Collar Pulse tell on the player's collar | VESKA | "Red on your collar! Step off! Then back on." |
| EGA-B5.4 | P1, a collar shut | VESKA | "That's one it can't drink." / "Two." / "Three. One more." |
| EGA-B5.5 | P2 begins (re-seat) | VESKA | "It's plating the niches. Watch the vent. Ash lifts, that niche shuts." |
| EGA-B5.6 | P2, Seal tell | VESKA | "Vent's breathing! Other niche!" |
| EGA-B5.7 | P2, player stays outside both niches long | VESKA | "You're cooking. Niche!" |
| EGA-B5.8 | P3 begins | VESKA | "It's venting what it drank. Read the floor. Amber line, get off it." |
| EGA-B5.9 | P3, Spill at a far player | VESKA | "It throws at whoever's furthest. Don't stand still that far out." |
| EGA-B5.10 | 0 HP | VESKA | (a long breath) "It's stopped." (beat) "It's not getting up. Go on. The valve." |
| EGA-B5.11 | Player beaten (heard on waking at the warming house) | HENNET | "Line hand brought you up. Sit. Eat. Then go back down. It's still there, and so are the collars you shut." |
| EGA-B5.12 | P1, the Sentinel held at its floor with a collar open | VESKA | "It's not taking it. Not while it's drinking. Shut the collars." |

### EGA-D9: the draw shut, and the ward through the night (S06)

```
      {player shuts the draw valve: 3-segment channel; the channels go dark; the collars' tells clear; the hum drops, then rises faintly somewhere above}
EGA-D9.01 VESKA: (comes in through the grille; sits on the plinth's edge; drinks from the ladle she carried down) "That's her. All of her."
EGA-D9.02 VESKA: "Hear that? That's going up. That's Cinderwall."
EGA-D9.03 VESKA: (she holds out the crew lamp) "Take it. You carried it further than I did."   {reward: warden's lamp}
EGA-D9.04 LINE HAND 2: (at the grille, looking at the construct) "Can I chalk something on it?"
EGA-D9.05 VESKA: "Chalk what you like. Then help me up."
```

```
EGA-D9.10 (The Cinderwall junction, on the way up. The manifold's tells amber.) VESKA: "Let her come up slow. Somebody keeps this junction till light."
EGA-D9.11 [EH_HEAT_MAIN = ward] VESKA: "Specially tonight. Our risers have had the night's heat already. We'll bleed her twice before morning."
EGA-D9.12 VESKA: "Sit. Water. Keep watch with us."   {keep watch: night → dawn}
EGA-D9.13 [EH_HEAT_MAIN = ward] (In the night, presentation: the line hands bleed the manifold twice; Veska calls the tells without opening her eyes.)
EGA-D9.14 VESKA: (at first light, standing) "Morning. Go up. I'll come when she's settled."   → S07
```

### EGA-D10: morning (S07)

At the stair head (W3), first light. Event `cinderwall.thaw_lines` (quest §8.2). Veska stands beside the player.

```
EGA-D10.01 (The frost over Cinderwall melts in long wet lines, lane after lane, over the roofs. Where the draw ran, the lines break off and the frost lies white.)
EGA-D10.02 VESKA: (a long look before she speaks) "Never seen her drawn on the ground before."
EGA-D10.03 VESKA: (she follows one line with her eyes to a gap, and stops) "There. And there. Where she was being drunk."
EGA-D10.04 VESKA: "Read the frost, not the talk."   {EGA_THAW_SEEN; frost variant ends for this player}
EGA-D10.05 [EH_HOLLOW_TRUTH = told] (Veska looks at the plaque by the stair, at the chalk across it. She says nothing. She touches the chalk with two fingers.)
EGA-D10.06 [EH_HOLLOW_TRUTH = kept] (Veska looks at the plaque by the stair. It is clean. She looks a moment longer than she needs to.)
EGA-D10.07 VESKA: "Go and eat. Hennet'll have saved you something, or he'll say he has."   → EGA-D10.10
```

The warming house (W2), by `EH_HEAT_MAIN` (quest §9.4). One scene plays.

```
EGA-D10.10 [EH_HEAT_MAIN = ward] (Too warm. People asleep on the benches in their shirts, blankets kicked to the floor. Two hood tells on the wall cracked across. Hennet asleep on his feet at the hearth.)
EGA-D10.11 [ward] A REGULAR: (fanning herself with a bowl) "We were warm by the second bell. Too warm. Somebody's hood popped two lanes over."
EGA-D10.12 [ward] HENNET: (waking with a start) "I wasn't asleep. I was resting my eyes on the stew."
EGA-D10.13 [ward] YORVEN: "Two hoods. The ward pays. I'll find it." (beat) "I'd rather pay for hoods than for coffins."

EGA-D10.15 [EH_HEAT_MAIN = terraces] (Cold air going out of the room at last. People still wrapped, but talking. The window shutters open to the terraces, high above the city: sightline MAP VERIFICATION REQUIRED; if there is none, the regulars talk about the glow at the door.)
EGA-D10.16 [terraces] A REGULAR: "Pretty, from here. Lit up like the Kindling. We watched it and ate stew."
EGA-D10.17 [terraces] ANOTHER REGULAR: "Middle of the night it came up through the floor. I cried. Don't tell Hennet."
EGA-D10.18 [terraces] HENNET: "I heard."
EGA-D10.19 [terraces] YORVEN: (at the shutters) "The terraces had the best seat in the city last night, same as every night." (beat) "It'll be on the board. Good."

EGA-D10.20 [EH_HEAT_MAIN = forges] (Warm and loud. Forge hands in leather aprons at the long table among the ward's people. One forge hand at the hearth beside Hennet, holding a ladle wrong.)
EGA-D10.21 [forges] A REGULAR: "Forge hands sat with us. One of them can't cook."
EGA-D10.22 [forges] HENNET: "Hennet's teaching him. Hennet is me." (to the forge hand) "Stir. Don't hammer it."
EGA-D10.23 [forges] FORGE HAND: "Half our crucibles cracked. Worth it." (he looks at the ladle) "This is harder."
EGA-D10.24 [forges] YORVEN: "The guild'll send me a bill. I'll frame it."

EGA-D10.30 HENNET: (to the player, all scenes) "Bowl. Sit. You're running cold." (beat) "I know. Wrong way round. Last night it wasn't."
EGA-D10.31 [EGA_FUSED_STEADIED] (At the end bench, the smelter-hand from last night is asleep under two blankets. His forearms are dark. He is snoring.)
EGA-D10.32 YORVEN: (he puts a purse by the bowl) "Ward's box. Don't count it in front of me."   {payment; quest §10}
EGA-D10.40 YORVEN: (a runner at the door, out of breath; Yorven reads the note and holds it up) "Odile's sent another runner. She wants you at the board, and she's never wanted anybody at the board."   → S08
```

### EGA-B6: the morning lanes (S07, on the walk to the valve house)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EGA-B6.1 | Passing a lane with a thaw line | A HOUSEHOLDER | "Look at my step. Wet in a line, dry either side. My grandmother would've had a word for that." (beat) "I've got one: odd." |
| EGA-B6.2 | Passing a gap in the lines | A CHILD | "This bit's still frosty. Watch. I can write my name." |
| EGA-B6.3 | Gate street | A CARTER | "Valve house is full. They say the board's come out even." |
| EGA-B6.4 | `EH_HEAT_MAIN = ward`, a cracked hood | A WARDEN | "Popped in the night. Too much, too fast. Better than too little." |
| EGA-B6.5 | `EH_HEAT_MAIN = terraces` | A HOUSEHOLDER | "Saw the terraces from the roof. Lovely. Cold." |
| EGA-B6.6 | `EH_HEAT_MAIN = forges` | A FORGE HAND, walking home | "Night shift with no work. Sat with strangers and ate stew. I'd do it again." |

### EGA-D11: the Tally Board (S08)

The public hall of the Gate Valve House (V1), morning, full.

```
EGA-D11.01 ODILE: (on the ladder at the board, chalking the hour; counting under her breath) "...eleven, twelve, and the deep vein, and... there." (she does not turn round)
EGA-D11.02 [ECW_SHORTFALL_SEEN] ODILE: "You read this board once. Read it again."
      {player inspects the tally board: EGA-I28 (required); sets EGA_BOARD_BALANCED}
EGA-D11.03 ODILE: (coming down the ladder) "Every hour since this main was rebuilt I've chalked 'old leaks' at the foot of that column. Every hour. My mother chalked it before me." (beat) "This morning there's nothing to chalk."
EGA-D11.04 ODILE: "So I wrote 'balanced'. I've never written it. My hand didn't know the shape."
```

The numbers:

```
EGA-D11.10 ODILE: "You've got something in your pack that's making you stand crooked."
  > [EGA_PLATES = 3] "Three number plates. Off three collars on the main."   → EGA-D11.11 {plates removed; carry-state ends}
EGA-D11.11 ODILE: (she reads the stamps; her face does not change) "My stamp." (she goes through to the book room)
      {V2: Odile pulls the valve book; finds each number; document EGA-I29}
EGA-D11.12 ODILE: (finger on the page) "C-one-fourteen. Repair, deep-works contract." (turning back years) "C-one-thirty-one. Repair, deep-works contract." (further) "C-one-forty-seven. Repair."
EGA-D11.13 ODILE: "Mine. My book. My clerks' hands. Every one a repair."
EGA-D11.14 [EGA_BOOK_READ] (The player lays the junction book open beside the valve book. The three numbers sit in both, in the same order, in two different hands.)
EGA-D11.15 ODILE: (quietly) "They used my clerks. They used my plates. They used my book to hide in." (beat) "Well. It's in my book now. Let it stay there, in the right column."
EGA-D11.16 ODILE: (she puts a few coins on the counter, exact) "Valve-house fee for a reading. It's a real fee. I'm not being kind."   {fee; quest §10}
```

Who stands at the board (quest §9.5). The always-present beat, then each flag's beat in this order; each is a few seconds and needs no input.

```
EGA-D11.20 (Veska comes in from the gate street with the line hands, soot to the elbows. Hennet behind her with a pail. Yorven pushes through, saying "District Overseer" to nobody in particular.)
EGA-D11.20a VESKA: (looking up at the board a long time) "Balanced." (beat) "Say it again, Odile."
EGA-D11.20b ODILE: "Balanced."

EGA-D11.21 [EH_COLD_WARD = posted] [ALLOCATION] (The Cooling House regulars stand behind Veska, coats still on.) A REGULAR: "We read it on our board once. We'll read it on this one."
EGA-D11.22 [EH_COLD_WARD = settled] [ALLOCATION] (A Council clerk, the coal book under his arm.) RALENNE'S CLERK: "The Magistrix's compliments. The coal book, as agreed. She says she would like to read the board herself one morning."

EGA-D11.30 [EH_CURRICULUM = guild] (Idra Callow with two teachers, chalk on their sleeves.) IDRA: "We came to see a board that adds up. We teach that."
EGA-D11.31 [EH_CURRICULUM = guild, EEH_TAVI_STRUCK] IDRA: "Tavi's line is still struck out. The new test spreads the flame. She passed it laughing."
EGA-D11.35 [EH_CURRICULUM = evidence] (Yorven lays the assessment ledger on the board's ledge, open at the transfer page.) YORVEN: "That's going back in my strongbox after. It's here so it can see the company it keeps."
EGA-D11.36 [EH_CURRICULUM = evidence, EEH_TAVI_STRUCK] (On the open page, Tavi's line is struck through. Inspect: EGA-I31.)

EGA-D11.40 [EH_HOLLOW_TRUTH = told] (Hesper Tolk and Darven Mott stand together near the door.) HESPER: "Lower forge. That's where it goes down, isn't it."
EGA-D11.41 [told] DARVEN: "Where the walls breathe."
EGA-D11.45 [EH_HOLLOW_TRUTH = kept] (Grand Marshal Kaevren Thalos at the edge of the crowd, a second ledger under his arm. He copies the board's last line into it, standing.) KAEVREN: "Second ledger. It's getting heavier."
```

(D-E2, ruled 2026-11-15: one beat, `freed`):

```
EGA-D11.50 HENNET: (at the player's elbow, quietly; a folded slip from his apron) "Left at my back door. Midnight. Your name on the outside, nothing else." (he does not watch the player read it)   {document EGA-I30}

```

```
EGA-D11.60 [EH_UNBURNT = kept] [ED-12] (At the back of the hall, Maeryn Vall and Seredh Embercarver. Maeryn catches the player's eye and nods. Seredh does not speak. Nobody near them says anything about them.)
EGA-D11.70 [TAS_ACCOUNT = named] (Tessaly Varn among a knot of masons.) TESSALY: "A gate book once named my crew. I like boards that say who did the work."
EGA-D11.75 (The hall goes quiet the way a room does when everyone is reading the same thing.)
```

The word:

```
EGA-D11.80 YORVEN: (looking at the junction book on the counter, its burnt mark) "Whoever wrote that is what's left of something, and they're still down there behind a door." (beat) "A remnant. Call it what it is."
EGA-D11.81 (Odile climbs the ladder and writes at the foot of the board, under *balanced*: *Draws: the deep works, below Cinderwall. Shut.*)
EGA-D11.82 VESKA: "Shut." (beat) "Good word. Two good words this morning."
```

### Documents and inspects: the board (S08)

| Object | Text | Condition |
|---|---|---|
| The tally board (EGA-I28) | "Intake against draws, by vein and ward, chalked by the hour through the night. [by `EH_HEAT_MAIN`: *Cinderwall* / *Ash Terraces* / *Emberforges*] runs double from the second bell to the hour before dawn. Every hour, at the foot of the last column: *old leaks*, and a figure. The morning hour has no figure. In its place, in a hand that has not written it before: *balanced.*" | Required; sets `EGA_BOARD_BALANCED` |
| The valve book (EGA-I29) | "Three lines, years apart, in three day clerks' hands, each with the valve-house mark: *C-114. Repair, deep-works contract.* / *C-131. Repair, deep-works contract.* / *C-147. Repair, deep-works contract.* Each with a fee paid. Each signed off as done." | Read at `EGA-D11.12` |
| The slip (EGA-I30) | See document below. | `EH_THALAN = freed` |
| The assessment ledger (EGA-I31) | "The transfer page, open on the ledge. Tavi's line: *Vigil guidance, pending*, struck through. Beside it, in Theryn Dalewright's hand: *Stays. Student.*" | `EH_CURRICULUM = evidence` with `EEH_TAVI_STRUCK` |
| Odile's tray (after) | "Three brass plates in a tin tray. *C-114, C-131, C-147.* Someone has put a fourth thing in the tray: a stub of chalk." | — |

### Document: Thennek's slip (EGA-I30) (D-E2, ruled 2026-11-15)

A torn strip of ledger paper, folded twice, the outside marked with the player's name in pencil.

> *He walks further each day. You do not need to know where. He heard about the frost. He asked me to tell you: good. T.*

Production rule: no place, no route, no count, no word about anyone below (D-C06: where Thalan lives stays unplaced).

### EGA-D12: the choice (S08)

```
EGA-D12.01 ODILE: (she stacks it on the counter: the junction book, the valve-book page she has copied, the plates in the tray) "That's an account. It can't stay on my counter. Counters get wiped."
EGA-D12.02 DURNAN: (pushing forward, apron on, with three wardens' crew chiefs from other wards behind him) "Every collar in this city was made by somebody with a hammer. We'll know whose hands." (beat) "Give it to the guilds. We'll read it to the people who fit the collars."
EGA-D12.03 YORVEN: "I've a seat at that table. I've never used it for anything but Cinderwall." (beat) "This is Cinderwall. Give it to the Council. They'll put it in the book with a seal on it."
EGA-D12.04 (Both look at Veska.)
EGA-D12.05 VESKA: "Don't look at me. I read beads. You walked it." (to the player) "Your hands carried it up. Your hands give it."
  > "Durnan. The guilds read it to the hammers."   → EGA-D12.10 {EH_ACCOUNT = guilds}
  > "Yorven. Put it in the Council's book."        → EGA-D12.20 {EH_ACCOUNT = council}
  > "Tell me what each of them does with it."      → EGA-D12.06
EGA-D12.06 ODILE: (counting on her fingers) "Durnan reads it to every forge hand by noon and nobody fits a collar without a warden's say. No law in it. Quick." (beat) "Yorven reads it into the Council's book. Law in it. Slower. Councillors hear it first, and the street hears it from them."   → EGA-D12.05
EGA-D12.10 DURNAN: "Good." (he takes the book; weighs it) "Lighter than I thought." → EGA-D13.40
EGA-D12.20 YORVEN: "Good." (to Odile) "Your copy, and your seal, and your clerk to hold my elbow." → EGA-D13.10
```

### EGA-D13: the reading (S08)

**The Council (`EH_ACCOUNT = council`), H2, the Council chamber.**

```
EGA-D13.10 COUNCIL CLERK: (at the door, before anyone sits) "The Speaker keeps vigil this morning." (he says nothing else; the Speaker's chair at the head of the table is empty)
EGA-D13.11 VAEL: (Magister Vael Trossen stands at the Council's book on its stand) "Before anyone speaks, the account goes in the book. Entire." (he reads, entry by entry: the three collars, the valve-book lines, *for the proving rings*, *hold anyway*, the board's figures by the hour) "Entered."
EGA-D13.12 [EH_SPEAKER = challenged] VAEL: "Enter also that the Speaker's chair was empty for the reading, and that a copy goes to his hall today, as to every member." 
EGA-D13.12 [EH_SPEAKER = exposed] VAEL: "Enter also that the Speaker's chair was empty for the reading. A copy goes to his hall today, as to every member. That is all the book says about it."
EGA-D13.13 RALENNE: (Magistrix Ralenne Kharveil, without standing) "'The board reads it as leaks.' They knew we read the board." (beat) "They counted on us reading it badly."
EGA-D13.14 KAEVREN: (Grand Marshal Kaevren Thalos, at the far end) "'Lower forge undercourse: do not draw.'" (beat) "Somebody down there knows that ground better than this table does." (he says nothing more)
EGA-D13.15 YORVEN: "Cinderwall asks one thing. Read the board. Out loud. Every day. Where people can hear."
EGA-D13.16 VAEL: "Moved: the valve house's board read aloud at noon each day for the season, by a Council clerk, in the public hall." (hands) "Carried. Entered."
EGA-D13.17 VAEL: (to the player, holding out his hand for the junction book) "It goes under my seal. You may read it whenever you like. So may anyone who asks the clerk."   {item EGA_junction_book removed}
EGA-D13.18 YORVEN: (on the steps after) "First time I've used that seat for anything but coal." (beat) "Felt like coal."   → EGA-D13.70
```

**The guilds (`EH_ACCOUNT = guilds`), F2, the Basalt Forge Guild hall.**

```
EGA-D13.40 (The hall off the great forges. Forge hands in aprons; crew chiefs from four wards; somebody has stopped the hammers.) DURNAN: (on a bench, the junction book open) "Quiet. You can hammer after."
EGA-D13.41 DURNAN: (he reads each splice aloud, slowly) "C-one-fourteen. Set as repair. Quarter draw." (a crew chief copies the number onto the guild board) "C-one-thirty-one. Half." "C-one-forty-seven. Half, then full hold." (beat) "Somebody in this city fitted those collars and was told 'repair'. I'd have believed it too."
EGA-D13.42 [EH_GUILDS = reformed] DURNAN: "New rules say any hand may ask to see a fitting book. I'm asking. Out loud. In front of you."
EGA-D13.43 [EH_GUILDS = restored] DURNAN: "Old rules say the guild answers to the guild. So the guild answers. To itself. Now."
EGA-D13.44 DURNAN: "'Hold anyway.'" (he closes the book) "We don't do anyway in this hall."
EGA-D13.45 A CREW CHIEF: "From today we fit no city collar without a warden's countersign."
EGA-D13.46 A FORGE HAND: "That'll slow every repair in the city."
EGA-D13.47 DURNAN: "Good. Slow and known." (hands) "Carried. Copies on every guild hall door by noon. The Council can read it on a door like everybody else."
EGA-D13.50 DURNAN: (to the player) "The book goes in our strongroom. Three keys. One's mine, one's a warden's, one's Odile's. She doesn't know yet."   {item EGA_junction_book removed}
EGA-D13.55 [EH_HEAT_MAIN = forges] A FORGE HAND: "We cracked half our crucibles for the ward last night. Now we know who we cracked them because of."
EGA-D13.60 VESKA: (at the hall door, arms folded) "Three keys." (beat) "I'll take the warden's."   → EGA-D13.70
```

**The letter (D-S1, ruled 2026-11-15) (both options).**

```
EGA-D13.70 (A runner in Speaker's Hall livery finds the player on the steps, out of breath, and holds out a sealed letter.) RUNNER: "From the Speaker. For your hand. I'm to say he hopes you're rested."
      {player reads it: EGA-I32 (required); sets EGA_LETTER_READ; then EGA-I33 with ESS_LETTER_READ}
EGA-D13.71 RUNNER: (if the player looks up) "No answer's needed. That's what he said."
EGA-D13.80 (The player closes the letter.)   {EH_STANDING; quest Completed}
```

### Document: the Speaker's letter (EGA-I32) (D-S1, ruled 2026-11-15)

Heavy paper, folded once, the Speaker's seal. In his own hand: the same hand as *To the Seat* (EH-M5). Warm, short. Nobody in the scene comments on it.

> *To the warden's hand who went down on the frost night,*
>
> *I am told Cinderwall is warm this morning, and that you are one of the reasons. I keep vigil for this city, and its fire is in every prayer I make. Thank you for the night you kept.*
>
> **[`EH_SPEAKER = challenged`]** *I heard a voice at the rehearsal ask what the fire is for. It is a fair question, and I mean the Kindling to answer it.*
>
> **[`EH_SPEAKER = exposed`]** *I know there is talk of who helped me to this chair. I have never thought help a shame. The city helped me, and I have tried to warm it back.*
>
> *The city will learn from this night. I will see that it is not frightened by what it learns.*
>
> *With the city's thanks, and mine,*
> *the Speaker*

Writing rules (D-S1, ruled 2026-11-15): he thanks, reframes and omits. He never mentions the draw, the junction book, the collars, the deep works or the far doors; he never claims not to have known; he never apologises; he states no fact that could be false. His vigil and prayers are sincerely held, and so is his taste for being the one who tells the city what it has learned; the help he took is something he chose (`exposed`: "I have never thought help a shame"). Nothing in the letter is a factual claim about the night.

| Inspect | Text | Condition |
|---|---|---|
| The letter beside the other (EGA-I33) | (Journal, document view: the letter set beside *To the Seat*.) "The same hand. *'I ask that the city not be frightened.'* *'The city will learn from this night.'*" | `ESS_LETTER_READ` (always set). Presentation only; never evidence; no comment. |

---

## Part 3b: post-story barks and the epilogue

### EGA-B9: after the board (post-`EH_STANDING`; the word in public speech)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EGA-B9.1 | Cinderwall, near the trough | A WARDEN | "Remnant's shut out of our main. Doesn't mean it's gone. Means it's not ours to feed." |
| EGA-B9.2 | Gate street | A CARTER | "Board balanced three days running. My cousin went to watch it like it was a dog fight." |
| EGA-B9.3 | Cinderweave Quarter | A WEAVER | "Remnant. That's what they're calling it. Whatever's left below." (beat) "Sounds like scraps. I hope it's scraps." |
| EGA-B9.4 | The Emberforges | A FORGE HAND | "Countersign or no collar. Took me an hour to fit one yesterday. Fine." (with `EH_ACCOUNT = guilds`) / "Council's got the numbers. We'll see if they read them." (with `council`) |
| EGA-B9.5 | Valve house, any hour | A CLERK | "Odile says it every hour. 'Balanced.' Says it like a prayer. Don't tell her I said prayer." |
| EGA-B9.6 | Undercroft stair head | A LINE HAND | "Chain on the far doors. Our side now, too. Nobody's touched it." |
| EGA-B9.7 | A tavern | A DRINKER | "Remnant of what, though?" / ANOTHER: "Of whoever. Drink." |
| EGA-B9.8 | Ash Terraces rehearsal, the player in the crowd | (presentation) | The Speaker, on his balcony, lifts his hand to the crowd. If the player is in his line of sight, he lifts it a little toward them, as he would to anyone. No line. |
| EGA-B9.9 | Ash Terraces, a terrace householder | `EH_SPEAKER = challenged`: A HOUSEHOLDER | "Somebody asked him what the fire's for. He wrote a letter about it, they say. Lovely letter. Didn't say." |
| | | `EH_SPEAKER = exposed`: A HOUSEHOLDER | "They say he had help getting that chair. Who didn't? He still keeps vigil. I still come and breathe." |
| EGA-B9.10 | Ash Terraces, `EH_HEAT_MAIN = terraces` | A BRAZIER KEEPER | "Two rows cracked the night of the frost. They'll be mended by the Kindling. They'd better be." |
| EGA-B9.11 | Cinderwall, a child | A CHILD | "I wrote my name in the frost and it melted. Then I wrote *remnant* on the wall and Hennet made me wash it." |
| EGA-B9.12 | Maeryn's shop, entering | DAHRIN | (once) "Did the board say anything about the deep works?" (the player's answer is not chosen; he hears it in the player's face) "Shut. Good. Shut is a word I like." |
| EGA-B9.13 (D-EL, ruled 2026-11-15) | EP20 Elyndra's Vent Shrine, after `EH_STANDING`; once per player; optional | ELYNDRA | (not turning from the vent) "The main is quiet now. Under the city, something isn't. Older than ember." (beat) "I can't tell you what. I may be wrong about where. Don't go looking on my word." |

### EGA-B10: epilogue state barks (quest §E)

| Id | Where (§E) | Condition | Speaker | Line |
|---|---|---|---|---|
| EGA-B10.1 | Cinderwall (E.1) | `EH_HEAT_MAIN = ward` | HENNET | "We were too warm. I'd do it again." |
| EGA-B10.2 | Cinderwall (E.1) | `= terraces` | HENNET | "We watched them glow. Don't do that to us twice." |
| EGA-B10.3 | Cinderwall (E.1) | `= forges` | HENNET | "One of the forge lads can nearly cook now." |
| EGA-B10.4 | Cinderwall (E.1) | All | VESKA, at the trough at shift change | "Amber. All day. I could get used to amber." |
| EGA-B10.5 | Cinderwall (E.1) | All | YORVEN | "Coal for the old out of my box this season. Don't make it a speech." |
| EGA-B10.6 | Valve house (E.2) | All, each hour | ODILE | (counting under her breath, at the last column) "...and the deep vein... Balanced." |
| EGA-B10.7 | Valve house (E.2) | `EH_ACCOUNT = council`, noon | COUNCIL CLERK | (reading aloud to the hall) "Intake, the deep vein. Draws by ward. Leaks: none. Balanced." (the gate street, a few dozen people, nods along) |
| EGA-B10.8 | Valve house (E.2) | `EH_ACCOUNT = guilds` | A CREW CHIEF, at the copy-board | "Four collars this week. Four countersigns. Write it big." |
| EGA-B10.9 | Valve house (E.2) | All | AUBIN HARL | "I sleep now." |
| EGA-B10.10 | Undercroft (E.3) | Inspecting the Sentinel | (inspect) | "Cold. Locked mid-turn. Chalked across the chest in a warden's hand: *DON'T.*" |
| EGA-B10.11 | Undercroft (E.3) | Inspecting the far doors | (inspect) | "Barred from the far side. Chained on this one. Deepbrand's mark scraped off the iron." |
| EGA-B10.12 | Emberforges (E.5) | `EH_ACCOUNT = guilds` | DURNAN | "Every collar with a countersign now. Slows us. Good." |
| EGA-B10.13 | Emberforges (E.5) | `EH_ACCOUNT = council` | DURNAN | "The Council has our numbers. We'd rather have had them first." |
| EGA-B10.14 | Emberforges (E.5) | `EH_GUILDS = reformed` | DURNAN | "My new rules held a seat for the wardens. First time a rule of mine's been used for anything but shouting." |
| EGA-B10.15 | Emberforges (E.5) | `EH_GUILDS = restored` | DURNAN | "We billed the ward for the forge night. I've torn the bill up. Don't tell my masters." |
| EGA-B10.16 | Old lower forge (E.6) | `EH_HOLLOW_TRUTH = told`, inspecting the plaque | (inspect) | "*NOT A COLLAPSE*, written over again in another hand. Under it, in a warden's: *The board balances now.*" |
| EGA-B10.17 | Marshal's office (E.6) | `EH_HOLLOW_TRUTH = kept`, inspecting the second ledger | (inspect) | "A new line, in the Marshal's hand, with the valve-house mark beside it. It says what the board says, and nothing else." |

### EGA-D14: Emberholt master commission offers (quest §E.10)

Each offer opens a commission; it grants nothing. All four are offered to every player with `EH_STANDING`.

```
EGA-D14.01 DURNAN: (at the Basalt Forge Guild door) "You've stood at my anvil and in my hall. Time you made something we'd hang on the wall." (beat) "A master piece. Basalt Forge standard."
EGA-D14.02 [EH_GUILDS = reformed] DURNAN: "Forge it to the new rules."
EGA-D14.03 [EH_GUILDS = restored] DURNAN: "Forge it the old way. I'll know."
  > "I'll make it."   {opens: Basalt Forge master piece}
  > "Not yet."        → (end; offer stays)

EGA-D14.10 VESKA: (at Durnan's anvil, or the Cinderwall yard forge) "Wardens carry a valve key and a bleed set. Ours are older than me. Make me new ones."
EGA-D14.11 [EH_HEAT_MAIN = ward] VESKA: "Make the key heavy. We'll be turning a lot of hoods."
  > "I'll make them."   {opens: Warden's valve key and bleed set}
  > "Not yet."          → (end; offer stays)

EGA-D14.20 BRISA TEGLAN: (in the Cinderweave Quarter, a frost-stiff coat over her arm) "Everybody in this city owns a coat for heat. Nobody owned one for that night."
EGA-D14.21 [Soot and Hide Completed] BRISA: "You know hide. Now learn cold."
  > "Show me."   {opens: Frost-warden's lined coat}
  > "Not yet."   → (end; offer stays)

EGA-D14.30 RYL DANNER: (in the Embergate yards, a stock half-cut on a trestle) "Wardens want something that reaches down a long duct. Crate-wood stock, smith-yard fittings."
EGA-D14.31 [Wardens' Quarrels Completed] RYL: "Feathers first. Then we'll talk about the stock."
  > "I'll build it."   {opens: Border-Warden's crossbow}
  > "Not yet."         → (end; offer stays)
```

### EGA-D15: the warden's round (quest §E.9; optional, repeatable)

```
EGA-D15.01 VESKA: (at the Undercroft stair head, once per presentation day after EH_STANDING) "Walk the line with me? Same as the first night. Less shouting."
  > "Lead on."      → EGA-D15.02 {round begins}
  > "Not today."    → EGA-D15.09
EGA-D15.02 VESKA: (at the stair niche) "Water. Then read me the first tell."
EGA-D15.03 VESKA: (at each named tell, after the player reads it) "Clear. Good." / "Amber. Note it." / "Red. Bleed it. You know how."
EGA-D15.04 [EH_HEAT_MAIN = ward] VESKA: (once per round, at the bleed house) "Our hoods still pop when she runs hard. We paid for that night. I'd pay again."
EGA-D15.05 [EH_HEAT_MAIN = terraces] VESKA: (once per round) "Every time I see the terraces lit I think of that night. I don't say anything. I just think it."
EGA-D15.06 [EH_HEAT_MAIN = forges] VESKA: (once per round) "Forge hands still drop in at the Cooling House. One of them's courting a line hand. Don't."
EGA-D15.07 VESKA: (at the bleed house slate, chalking the day's line) "There. That's a round." (Yorven's wage at the warming house.)
EGA-D15.08 [vent gallery encounter this round] VESKA: (from the niche) "Beetles. Same as ever. Go on, I'll hold the lamp."
EGA-D15.09 VESKA: "She'll be here tomorrow. So will I."
```

---

## Part 4: Dialogue review checks

| Check | Result |
|---|---|
| Node coverage | Every node the quest file references exists here: `EGA-D1`–`EGA-D15`, `EGA-B0`–`EGA-B10` (with `EGA-B9.13`), `EGA-I1`–`EGA-I33` (document and inspect ids in tables or full). |
| D-E2 (ruled 2026-11-15) | `EGA-D11.50`, document `EGA-I30`, bark `EGA-B9.12` (`freed` only). One short beat; no step, flag or completion depends on it. Nothing says Thalan's freedom ends the works or the suffering below. |
| D-S1 (ruled 2026-11-15) | Letter `EGA-I32`, inspect `EGA-I33`, `EGA-D13.12` (both values), `EGA-D13.70`–`.80`, barks `EGA-B9.8`–`.9`. The Speaker never appears in person, never fights, confesses or lies outright; the letter thanks, reframes and omits. |
| Voice | Civic pride first; criticism from inside (Odile on her book, Durnan on his hall, Yorven on his seat). Craft, never magic. Fire grammar throughout. Humour lives in the warming house and the forges. |
| The word "Remnant" | First spoken at `EGA-D11.80` by Yorven, plainly meant; used afterwards only in barks. Never defined, never given a leader, roster or count. |
| Forbidden content | No "Fire Titan", no precursor name, no initiate's name, no count of anyone below, nothing about what the proving rings are for or what "the old circle" keeps, the margin hand never named (D-C03, D-C06, FT-04/05). No one located. |
| ED-12 | Maeryn and Seredh are not discussed; Thennek's slip names nothing. |
| CDR | The boss barks are spoken from outside the arena; no NPC fights; Veska is a non-combatant throughout. |
| Other regions | Tessaly Varn once (`TAS_ACCOUNT = named`), never caricatured. |

## Part 5: Review log

| Pass | Change |
|---|---|
| Continuity (Acts I–II) | Odile's Act I board line returned at `EGA-D11.02`; Hennet's "running hot" turned to "running cold"; Veska's "read the tells" turned once at dawn; the Cinder Rat's "Still the same place" kept unexplained. |
| Canon anchors (Part 4 ledger) | Yorven's Council seat used as District Overseer only; Durnan, Vael, Ralenne and Kaevren speak within their offices; no new ages, kin, service or custody beyond the item's quest-defined removal. |
| Reserved decisions | D-E2 and D-S1 ruled 2026-11-15; nodes listed in the header; quest §14.1–§14.2 resolved. |
| Plain-language pass | Long sentences split; no line explains the thaw lines; the letter checked line by line against the never-lies rule. |
| Independent review, 2026-11-14 | `EGA-D11.58` chalk now *Someone was held below on this heat.* (the number removed, D-C06); `EGA-D11.80`/`.81` no longer cite the lower-forge night or place the draw under it (Yorven's limit, `kept` branch, D-C03); `EGA-B10.16` no longer claims heat was drawn at the lower forge; `EGA-D10.31` pronouns made consistent (he); "Old Dace" renamed Old Ketta (Lowmark collision); "Council grey", "amber wax" and "Thornfell dust" removed (no invented colours; no interregional implication); `EGA-B5.12` added (the boss's 65% floor called aloud); the bleed-house tell change on turning the wheel added; terraces shutters sightline marked MAP VERIFICATION REQUIRED. |
| Batch 4 encounter alignment review, 2026-11-15 | `EGA-D1` accept event aligned with Act III: the Cinderwall entry makes EH-M6 Active and sets `EGA_FROST`; the accept option completes `S00_frost` (Integration EQ-04). No line text changed. |
| Emberholt character rulings, 2026-11-15 | **D-E2:** aided beat `EGA-D11.55`–`.58` and Asera's aided half of `EGA-B9.12` removed (Zones EP03 matches); `EGA-D11.50`, `EGA-I30` and Dahrin's bark untagged as the only version. **D-S1:** Speaker cast note and letter writing rules state both halves; tags and swap pointers removed; letter text unchanged. **D-EL:** `EGA-B9.13` Elyndra's one unsure "older than ember" line at EP20, optional. |
