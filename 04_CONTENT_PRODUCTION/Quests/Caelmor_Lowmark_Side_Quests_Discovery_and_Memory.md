# Lowmark Side Quests — Discovery and Memory

**Status:** Authored production content for Creative Director milestone review (bible §12, batch 3). Seven side quests and the ten micro-events of `Caelmor_Lowmark_v1_Narrative_Production_Bible.md` §7 and §7.1. Everything here is **[NEW]** unless marked **[CANON]**; consequential story choices are marked **[PROPOSAL — DIRECTOR]**. No schema, JSON or C# is created. Format, voice and conventions follow `Caelmor_Lowmark_Quest_The_True_Line.md` and Part 1 of `Caelmor_Lowmark_The_True_Line_Cast_and_Dialogue.md`; each package carries its own dialogue inline.

**Covers:** environmental discovery **SB** The Silent Bell, **UC** The Uphill Canal, **TB** The Twice-Burned Tree, **WD** The Whispering Door; memory/lore **CN** The Candle Rule, **VK** A Verse Kept Back, **FC** What the Flood Carried; micro-events **ME01–ME10**.

**Canon hooks used:** dossier §XI (the Silent Bell, the Riverwarden Lullaby, the Twice-Burned Tree, the Uphill Canal, the Whispering Door, the Field-Mage's Mantle, Circle of Unburnt Reeds, Flood Calendar Stones), §V.3 (Ember-Well, Path of Unburnt Reeds), §V.4 (Greyharrow's bell), §III (Wraithwatcher tools, Watergarden Keepers), §IX (softmoss, banner-thistle); anchor limits for Joric Fen, Annelise Reed and Tovin Pell; lattice L-S09, L-S11, L-S12, L-S17, M02–M07; discovery framework (three layers; optional-discovery card).

---

## 0. Shared rules for this file

### 0.1 Unlock gates

| Code | Suggested content id | Unlock | How it is offered | Later gate |
|---|---|---|---|---|
| SB | `lowmark.side.silent_bell` | MQ1 Completed | Enter the Greyharrow tower square: Teague and Merrin are arguing at the roster wall. | — |
| UC | `lowmark.side.uphill_canal` | MQ3 Completed | Enter the canal foot volume (P28), or Bryn Ruddock's bark at the orchards ("The canal up the hazel cut's running backwards again"). | Richer payoff after MQ9 Completed (§2.11). |
| TB | `lowmark.side.twice_burned_tree` | MQ5 Completed | Ashenstead household bark at the remembrance circle ("It's fruiting. First time since my lad was small."), or approach P27 at dusk. | Fruit and dream need dusk/night (§0.4). |
| WD | `lowmark.side.whispering_door` | MQ4 Completed | Ansel Corrie's patrol book entry (bark at the Lantern Post: "Dunnock farm. Door went again."), or approach the Dunnock farm gate. | Defence needs night (§0.4). |
| CN | `lowmark.side.candle_rule` | MQ3 Completed | Enter the Ashenstead watergarden: the Holt family's accusation is in progress. | — |
| VK | `lowmark.side.verse_kept_back` | MQ3 Completed | Greyharrow dock notice and the Sayer–Coombe quarrel. | Steps S03 onward require MQ9 Completed (§6). |
| FC | `lowmark.side.what_the_flood_carried` | MQ4 Completed | Approach the Lark low field: debris across the furrows, nobody working. | — |

None of these quests is required by the main line, by `LM_CIVIC_STANDING`, or by any commission. CN sets one quest-local flag that adds a line to MQ11's Tend argument; MQ11's Tend option exists without it (§5.9).

### 0.2 Discovery philosophy

1. **Reward attention, never demand it.** Every strange thing has a visible invitation in the place: wear, a habit, a sound tied to conditions, a seat that faces the wrong way. A player who misses a detail loses colour, never progress. Nothing requires an external guide, arbitrary clicking or a collectible set.
2. **Nothing optional solves a main mystery.** These quests do not explain the Marking Stones, the drift, the Field-Mage, the Riverwardens or the Fourteenth Lot. The bell stays silent and unexplained. The canal never says why it is shy. The dream shows no person, no event and no name. The door's creak has an ordinary half and an unexplained half. Each package's mystery ledger states what it cannot prove.
3. **The strange moment belongs to the player.** No UI, no camera takeover, no text explaining it, no music sting. The world does something; a person reacts, or pointedly doesn't. Inspect text afterwards describes only what is now visible.
4. **Evidence rule.** Supernatural effects never identify a person, prove guilt, settle a claim or name the dead. Combat never reveals evidence. Objects, places, records and testimony do the proving (CN's pinched wick, SB's ringers' slate, FC's solder and silt line).
5. **The place stays useful.** After its secret, the canal still runs, the tower is still Greyharrow's landmark, the garden is still tended, the field is still planted (framework: "the place remains useful after its secret is noticed").

### 0.3 Conventions

- **Steps** are scoped by quest id (`SB` `S00_offer` is distinct from `UC` `S00_offer`). **Flags** use the quest code prefix. No new `LM_` flags; region flags are only read.
- **Quest items: none.** All seven quests use carry-state objects (TB fruit, FC tin case, CN offering boat, UC gate paddle) or placed props. This file adds **0** to the v1 quest-item budget (bible §11.6).
- **Dialogue** uses the True Line format with `<CODE>-D<n>.<nn>` ids. `[condition]`, `{effect}`, *(repeatable)* as in the cast file. Nodes with Sedge are tagged **`[D-7]`** and the one optional Oriel node **`[D-8]`**, so those Director decisions can be swapped by search. No node in this file names the antagonist.
- **Death** in any encounter: respawn at the quest's named safe point with step, flags and carried state restored to the last deposit (carried objects return to their pickup point). No quest here can fail.
- **Co-op:** independent instances; shared world creatures give step credit to every participant on that step; step-conditioned props and strange moments are presented per player from their own state.

### 0.4 Time-of-day gate

Several beats need dusk, night or dawn. Each uses a named **wait** interaction (a seat, a fire, a step) that completes when the world clock enters the window. If no shared world clock exists when these are built, the wait interaction is itself the gate: it fades the local player's lighting to the window and spawns that player's step encounters. This is the same need as MQ4's keep-watch interaction and should be one shared contract (§9).

---

## 1. SB — The Silent Bell

### 1.1 In one paragraph

Greyharrow is getting ready for **Rope Day**, the spring market under the bell tower, opened every year by pulling a bell that has not rung since the armistice. Sergeant Aubrey Teague has a bucket of whitewash and a council note telling him to paint over the wartime watch roster on the tower's ground-floor wall: two families say its column of "absent" marks makes their grandparents look like people who never turned up. Merrin, who has rebraided the bell rope every spring for longer than Tamsin has been alive, wants the roster kept and the rope kept, and cannot say why either matters. The player climbs a tower nobody has climbed since the stair rotted and finds the ringers' own slate in the bell chamber. On the "absent" nights, the ringers came up, pulled, and heard nothing. The roster recorded a routine being interrupted, not people failing it. Tamsin pulls the rope from below while the player stands beside the bell. It swings. The clapper strikes. There is no sound. The player chooses what Greyharrow keeps, and Rope Day goes ahead.

**What the player should remember:** a bell swinging full in silence. **What the player might want next:** Merrin's thaw-song verse (VK lead). Nothing about the bell.

### 1.2 Summary card

| Field | Value |
|---|---|
| Type | Environmental discovery (Phase 1.5). Lattice L-S11, micro-event M03 folded in. |
| Unlock | MQ1 Completed. Auto-offered on entering the tower square. |
| Length | 20–30 minutes. |
| Combat | None. Danger is the climb (rotten boards with readable tells). |
| Skills | None required. Woodcutting optional (S04b, patch the stair). |
| NPCs | Sergeant Aubrey Teague, Merrin, Tamsin; a Sayer elder and a Coombe elder (role voices; named households shared with VK). |
| Choice | What Greyharrow keeps (3 options). |
| Unlocks | Tower lookout (per-player drop ladder); Merrin's VK lead; Rope Day market props. |

### 1.3 The place: Greyharrow bell tower (P25)

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Tower square** | Hook; Rope Day stalls being set up. | Trestles stacked, bunting in a basket, a whitewash bucket with the brush standing in it. The bell rope hangs out of a hole in the ground-floor ceiling, braided in three colours, newer than anything near it. |
| **B. Roster wall** | The dispute. | A painted board in a watch clerk's tidy hand: names down the side, nights across the top, ticks for **rang**, and for the last weeks a column of black crosses headed **ABSENT**. Two names have been scrubbed at with a thumb. |
| **C. First landing** | Start of the climb. | The stair is sound to here. Above, three treads hang by one nail each. Pigeon feathers, old rope offcuts, a child's chalk ladder drawn on the wall reaching exactly as high as a child can reach. |
| **D. Joist route** (agility) | Fast route. | Step up onto the wall joist, walk the beam above the gap, climb the bell-frame ladder. |
| **E. Militia gallery** (walkable fallback) | Slow route. | Outside stone stair to the lookout gallery (Teague's key), then an inner door onto the second landing. Teague's grievance list is nailed inside the door. |
| **F. Second landing** | Hazard. | Boards grey with age. Two of them are rotten (see §1.5). |
| **G. Bell chamber** | The discovery. | The bell on its frame, louvres onto the side branch of the river, the ringers' slate on a hook, chalk tallies on the frame beam, a folded drop ladder lashed under the hatch. The clapper is worn bright. The dust on the frame is undisturbed except in a ring under the bell. |

**MAP VERIFICATION REQUIRED:** the louvres must overlook the side-branch water for the river-ring detail in §1.6.

### 1.4 Beats

**Beat 0 — Whitewash (`S00_offer`).** *Objective: Find out why the roster is being painted over.* Teague and Merrin at the wall (SB-D1). Teague will wait for the player before painting ("I'd rather someone else decided I was right.").

**Beat 1 — Read the wall (`S01_read_roster`).** *Objective: Read the roster.* Three inspects: **ticks** (years of nightly ticks in one hand), **absent column** (the crosses start on the same night for every ringer at once), **scrubbed names** (Sayer and Coombe). The second inspect is the hook: everyone "deserted" on the same night.

**Optional — The rope (`S02_rope`).** Tamsin is rebraiding the rope at its foot with Merrin's old cords (SB-L-TAMSIN). Pulling the rope from the ground floor is always available: *"The rope pulls heavy and smooth. Something high above swings. Nothing sounds."*

**Beat 2 — Up (`S03_climb`).** *Objective: Climb to the bell chamber.* Teague unlocks the tower door during SB-D1. The player chooses the joist route (agility) or asks Teague for the gallery key (SB-D2). Either reaches the second landing and the chamber.

**Optional — Patch the stair (`S04b_patch`).** At the first landing, inspect the hanging treads. Cutting one straight stem from the town's coppice edge (Woodcutting, entry level) and seating it (3 s channel) makes the inner stair walkable for this player and lets Merrin climb in Beat 6.

**Beat 3 — The ringers' side (`S05_read_chamber`).** *Objective: Look around the bell chamber.* Three inspects: **slate**, **beam tallies**, **clapper** (texts in §1.12). The slate's last weeks read *"Pulled. Nothing."* night after night, ending *"Pulled. Nothing. Try at dawn."* The beam tallies match the roster's ticks exactly up to the absent column, then continue as ringers' marks.

**Beat 4 — Send it down (`S06_lower_slate`).** *Objective: Get the slate to the ground.* The slate hangs on a cord. Interaction **Lower the slate** (3 s) feeds it down the rope hole; Tamsin's voice from below: "Got it. It's heavy. It's mine now." Optional `S06b_ladder`: unlash the drop ladder (3 s), a walkable route down for this player from now on.

**Beat 5 — The pull (`S07_pull`) — the strange moment.** *Objective: Ring the bell.* At the louvre, the player calls down (SB-D4). Tamsin pulls. See §1.6.

**Beat 6 — What the town keeps (`S08_choose`).** *Objective: Decide what happens to the roster.* At the wall, Teague, Merrin, Tamsin with the slate, and the two elders (SB-D5).

**Beat 7 — Rope Day (`S09_rope_day`).** *Objective: Open Rope Day.* The stalls go up. Tamsin pulls the rope; nothing sounds; the square cheers anyway (SB-D6 barks). Quest Completed on the dialogue end node.

### 1.5 Encounters and hazards

| Id | Hazard | Placement | Tell | Effect | Solo target |
|---|---|---|---|---|---|
| **H1** | Rotten boards (2) | Second landing | A loud creak and a puff of dust from the board's edges ~1.5 s after the player steps on it. | If the player is still on it when the tell ends, it gives: the player drops to the first landing, small fall damage, re-climb. | Never fatal. A player who keeps walking crosses without noticing. |
| **H2** | Pigeon burst | Joist route | Wings rattle in the beams before the burst. | Cosmetic. The beam walk cannot be failed. | — |

No combat. The danger is real but slow and readable, which suits a town landmark.

### 1.6 The strange moment: presentation spec

| Element | Spec |
|---|---|
| Trigger | SB-D4 end node: Tamsin's pull, server event `silent_bell.pull`. |
| Duration | ~12 s: three full swings. |
| Bell | Swings through a full arc on each pull. The clapper visibly strikes the lip on each swing. The bell is not cracked (its inspect says so). |
| Audio | Normal tower ambience (wind, pigeons, creaking frame) continues until the first strike. On each strike: **nothing**, and for half a second the ambience itself drops out, as if the strike swallowed it. No music, no chime, no low tone. The frame's creak and the rope's hiss through the hole stay audible throughout. |
| Dust | A ring of dust jumps off the frame on each strike and drifts down through the light. |
| The river | If the player is looking through the louvres at the side-branch water when a strike lands, a single wide ring spreads across the surface, as from a dropped stone with no stone. Client-side and view-dependent, like the True Line far-bank figure. |
| UI | None. No objective update until the bell is still. |
| Camera | Player-controlled throughout. |
| After | Bell inspect: *"Still now. The lip is bright where the clapper has struck it, over and over, for years."* Ground-floor rope pulls stay silent forever. |
| What it means | Nothing that the quest states. The ringers were not lying. That is proved by the slate, not by the bell. |

### 1.7 Steps

| Step | Objective | Completes on | Required |
|---|---|---|---|
| `S00_offer` | Find out why the roster is being painted over. | Enter square volume → SB-D1 end node | Yes |
| `S01_read_roster` | Read the roster. | 3 inspects (ticks, absent column, scrubbed names) | Yes |
| `S02_rope` | (Optional) Ask about the rope. | SB-L-TAMSIN end node | No |
| `S03_climb` | Climb to the bell chamber. | Enter bell-chamber volume | Yes |
| `S04b_patch` | (Optional) Patch the stair. | Interaction `seat_tread` complete | No |
| `S05_read_chamber` | Look around the bell chamber. | 3 inspects (slate, beam, clapper) | Yes |
| `S06_lower_slate` | Get the slate to the ground. | Interaction `lower_slate` complete | Yes |
| `S06b_ladder` | (Optional) Let down the ringers' ladder. | Interaction `unlash_ladder` complete | No |
| `S07_pull` | Ring the bell. | SB-D4 end node (fires `silent_bell.pull`) | Yes |
| `S08_choose` | Decide what happens to the roster. | SB-D5 choice node | Yes |
| `S09_rope_day` | Open Rope Day. | SB-D6 end node → Completed | Yes |

### 1.8 Flags

| Flag | Set by | Read by |
|---|---|---|
| `SB_ROPE_ASKED` | SB-L-TAMSIN | SB-D5 option (Tamsin's rope idea) |
| `SB_STAIR_PATCHED` | `S04b_patch` | SB-D5 Merrin variant; tower prop |
| `SB_LADDER_DOWN` | `S06b_ladder` | Tower prop (per player) |
| `SB_KEEP_BOTH` / `SB_INTO_ROPE` / `SB_TO_FAMILIES` | SB-D5 (exactly one) | Wall and rope props; Teague and Merrin barks; VK-D1 variant |
| `SB_COMPLETE` | Completion | VK-D1 (Tamsin as bell-puller at the thaw) |

### 1.9 Choices and consequences

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Keep both halves** — *"Hang the slate beside the roster. Let people read both."* | The slate is hung on the wall; Merrin chalks under it: *They came. The bell didn't.* | The Coombe elder: "Now everyone reads it twice." The roster stays public. | Visitors read the wall (ambient). Teague: "Council's annoyed. I'm told that's my fault." |
| **Into the rope** `[SB_ROPE_ASKED]` — *"Paint it over. Braid a thread for every ringer into the rope."* | Whitewash goes on. Tamsin and Merrin braid one cord per ringer into the rope. | No public list survives; only people who braid know which thread is whose. | The rope gains coloured threads (prop). Each Rope Day it is rebraided, so the names are carried by work. |
| **Give it to the families** — *"Paint it over. The slate goes to the families."* | Whitewash goes on. The Sayer and Coombe elders take the slate between them. | The town loses its only record of the ringers' routine. Merrin goes quiet. | The slate appears on a Sayer mantel (VK interior prop). Merrin: "It's somewhere warm. That's something." |

No option is wrong. The proof is the same in all three: the ringers came.

### 1.10 Rewards

| Reward | Type | Notes |
|---|---|---|
| Militia odd-job wage | Small payment | From Teague; sized by economy tuning. |
| Tower lookout | Access | The bell chamber becomes a viewpoint over the side branch for this player (drop ladder if `SB_LADDER_DOWN`, else the route they climbed). |
| VK lead | Story | Merrin's slow line about the thaw song's quiet verse (SB-D5.40). |
| Skill XP | Action only | Woodcutting from `S04b_patch`. No lump quest XP. |

### 1.11 Failure, recovery, co-op

Falls through H1 drop the player one landing; never fatal. Death (from unrelated causes) respawns at the tower square. Logout restores the last step; a lowered slate stays lowered. Leave and return: the quest stays Active with committed progress and choice props intact; resume from the current objective at the square. Co-op: each player climbs and pulls in their own instance; when Tamsin pulls for one player, partners in the chamber see the bell swing (the swing is a world animation) but only the requester's client plays the river ring. Props (whitewash, threads, slate) are per player; fallback if per-player props are not ready: the wall shows the slate hung beside a half-whitewashed roster for everyone, and the choice is carried in dialogue.

### 1.12 Dialogue

```
SB-D1.01 TEAGUE: "Council says paint it. Two families say paint it. Merrin says over his body."
SB-D1.02 MERRIN: "Over the rope's body. My body's not the point."
SB-D1.03 TEAGUE: "It's crosses, mostly. 'Absent.' Nobody wants their gran on a wall marked absent."
SB-D1.04 MERRIN: "They weren't absent. I don't know what they were. They weren't that."
  > "Who wrote the roster?"                     → SB-D1.10
  > "Can I take a look before you paint?"       → SB-D1.20
SB-D1.10 TEAGUE: "Watch clerk, down here, every night. Ticked when he heard the bell."
SB-D1.11 MERRIN: "And crossed when he didn't."            → SB-D1.20
SB-D1.20 TEAGUE: (unlocks the tower door) "Look all you like. The paint's patient. I'm less so."
       {event: SB-D1 end → completes S00_offer}
```

```
SB-L-TAMSIN (at the rope foot, braiding)
ST.01 TAMSIN: "Don't touch. It's a three-strand. You'd make it a two-strand."
  > "Why braid a rope for a bell that doesn't ring?"   → ST.02
  > "Carry on."                                        → end
ST.02 TAMSIN: "Because it's frayed. You don't leave a rope frayed. Merrin, tell them."
ST.03 MERRIN: (not looking up from his cords) "You don't leave a rope frayed."
ST.04 TAMSIN: "See? Also somebody has to pull it on Rope Day and it's going to be me."
  > "What happens when you pull it?"                   → ST.05
ST.05 TAMSIN: "Nothing. Everyone claps. Then the pie stall opens."   {set SB_ROPE_ASKED} → end
```

```
SB-D2 (Teague, if asked for another way up)
SB-D2.01 TEAGUE: "Stair's rotten past the first landing. Militia uses the outside stair to the gallery."
SB-D2.02 TEAGUE: (hands over a key) "Bring it back. I have a list of people who didn't."   → end {give gallery access}
```

**Bell-chamber inspects**

| Object | Text |
|---|---|
| Ringers' slate | "A ringers' slate, chalked in many hands. Marks for every night. Near the end, the same words over and over: *Pulled. Nothing.* The last line: *Pulled. Nothing. Try at dawn.*" |
| Beam tallies | "Tally marks cut into the frame beam. They match the roster downstairs night for night, then keep going where the roster says absent." |
| Clapper | "Worn bright on one face. It has struck the bell many times. Recently, too." |
| Bell | "No crack. No wedge. Good bronze, cold to the touch." |
| Hatch ladder | "A ringers' ladder, folded and lashed. Someone tied it up to keep it safe and never came back to untie it." |

```
SB-D4 (at the louvre, after S06; the player calls down the rope hole)
SB-D4.01 TAMSIN: (from far below) "Are you ready? I'm ready. I've been ready for ages."
  > "Pull."                                 → SB-D4.02
  > "Wait a moment."                        → end (repeatable)
SB-D4.02 TAMSIN: "Pulling!"
       {event: silent_bell.pull → presentation §1.6; S07 complete when bell is still}
SB-D4.03 TAMSIN: (after) "Did it? Up there? Did it do anything?"
  > "It swung. That's all."                 → SB-D4.04
  > "No. Nothing."                          → SB-D4.04
SB-D4.04 TAMSIN: "Told you. Come down, Merrin's being slow at the wall."   → end
```

```
SB-D5 (at the roster wall; Tamsin holds the slate)
SB-D5.01 TAMSIN: "They came. Look. Every night. They pulled and nothing happened."
SB-D5.02 SAYER ELDER: "My gran said she rang it. Nobody believed her."
SB-D5.03 COOMBE ELDER: "And the clerk wrote absent, because he was downstairs and heard nothing."
SB-D5.04 TEAGUE: "So the roster's right. And wrong. I hate that."
SB-D5.05 MERRIN: (to the player) "You've been up. You decide. I'll braid whatever you say."
  > "Hang the slate beside the roster. Let people read both."            → SB-D5.10
  > [SB_ROPE_ASKED] "Paint it over. Braid a thread for every ringer."   → SB-D5.20
  > "Paint it over. The slate goes to the families."                     → SB-D5.30
SB-D5.10 MERRIN: (chalks under the slate) "They came. The bell didn't."
SB-D5.11 COOMBE ELDER: "Now everyone reads it twice." (beat) "Good."   {set SB_KEEP_BOTH} → SB-D5.40
SB-D5.20 TAMSIN: "One cord each. I'll need more cord. I'll need so much cord."
SB-D5.21 TEAGUE: (lifting the brush) "Finally."                        {set SB_INTO_ROPE} → SB-D5.40
SB-D5.30 SAYER ELDER: (takes one end of the slate) "We'll keep it warm."
SB-D5.31 MERRIN: (quietly) "It's somewhere warm. That's something."    {set SB_TO_FAMILIES} → SB-D5.40
SB-D5.40 [SB_STAIR_PATCHED] MERRIN: "You fixed my stair. I'll go up tonight. First time in years."
SB-D5.40 [else] MERRIN: "There's a verse we don't sing at the thaw. We hum it. Ask me when the ice goes."
       {event: S08 complete}
```

```
SB-D6 (Rope Day; barks around the square)
TEAGUE:   "Market's open. Bell's silent. All's normal in Greyharrow."
TAMSIN:   (pulling the rope with both hands, feet off the ground) "Rope Day!"
HOUSEHOLD:"Every year. Every year it doesn't ring and every year we clap."
MERRIN:   "That rope'll last till next spring." (beat) "Then I'll do it again."
       {event: SB-D6 end → quest Completed}
```

### 1.13 Mystery ledger

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The roster's absent marks** | The ringers came; the bell stopped sounding; the clerk below recorded silence as absence. | The ringers deserted their watch. | Slate, beam tallies, bright clapper. | The families lied to cover shame. | — | SB (resolved locally). |
| **The silent bell** | **Deliberately unselected [PROPOSAL — DIRECTOR]: never explained in v1.** | Cursed since the armistice; cracked; held by the drowned. | Swings, strikes, no sound; a ring on the river if watched. | It's cracked (inspect: it isn't). The river ring means the bell "rings into the water" (unconfirmed; nothing builds on it). | Everything. | None in v1. |

### 1.14 Integration, open decisions, review log

**Needs:** agility triggers (joist route) with the gallery fallback; per-player props (whitewash, threads, slate, drop ladder) with the shared fallback in §1.11; inspect and channelled interactions; one world animation (bell swing) plus a local audio-duck and view-dependent water ring (`silent_bell.pull`); a "lower object down a hole" interaction can be a plain channel that despawns the slate prop above and spawns it in Tamsin's hands.
**Open:** whether the bell is ever explained (recommend no). Rope Day as a recurring ambient event after completion (recommend yes, cheap).
**Review log:** first draft had the player carry the slate down the rotten stair (carry + agility conflict) → replaced with lowering it down the rope hole. First draft let the bell ring once at the end → cut; the brief and canon require silence. The two complaining families are the Sayers and Coombes so VK inherits a known quarrel; both quests work in either order.

---
## 2. UC — The Uphill Canal

### 2.1 In one paragraph

Up a hazel cut in Brackenford Woods, a narrow stone channel climbs a slope in short steps from a reed-choked foot pool to a cistern at the top. Water should run down it. Orchard hands swear it runs up, "when nobody's looking," and nobody has ever seen it do so. The foot pool has backed up into the mouth of an old stone culvert through the hill, drowning a path the Brackenford cutters used to take. The player tests the rumour by setting a reed float in the pool and walking away; when they come back, the float is three steps up the channel. Watching directly, the water lies still. The answer is built into the place: a stone seat under a heavy brow at the foot, facing a small, wind-sheltered basin with its back to the channel. Sitting there, the player sees the canal in the basin's reflection, climbing, step over step, like a ribbon drawn upward. It also shows why the canal has stalled: the head gate's paddle is gone, so the cistern spills straight back down. The paddle is the doorstep of a cutter's hut in the coppice. The player carries it up, seats it, and leaves the canal alone. When they come back, the foot pool has dropped and the culvert is a dry stone path through the hill. Sedge is cutting reeds at the pool and asks the right questions.

**What the player should remember:** sitting with their back to a wonder and watching it in a basin of still water. **What they might want next:** after MQ9, to come back and recognise the canal as one stitch of the flow-table (§2.11).

### 2.2 Summary card

| Field | Value |
|---|---|
| Type | Environmental discovery. Dossier §XI "The Uphill Canal" [CANON hook]; a still-working Riverwarden Braid (bible §2.1) [NEW]. |
| Unlock | MQ3 Completed. Richer payoff after MQ9 Completed. |
| Length | 25–35 minutes. |
| Combat | ~10%: one required encounter in the drained culvert. |
| Skills | None required. Melee for E1. |
| NPCs | Sedge `[D-7]`; Bryn Ruddock (bark only). |
| Choice | None. This quest is about watching. |
| Unlocks | **The Hazel Culvert shortcut**; canal-foot rest seat. |

### 2.3 The place: the Uphill Canal (P28)

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Hazel cut** | Approach. | A sunken lane between coppiced hazel, banks taller than a person. The sound of water is wrong in a way that is hard to name: it comes from uphill. |
| **B. Foot pool** | Start; Sedge. | Reed-choked, high, flat. A stone arch with a carved lintel stands half drowned at the back: the culvert mouth. Moss on the channel's first steps grows on the *downhill* faces, as if water usually comes from above. |
| **C. The channel** | The canal. | Twenty-odd short stone steps up the slope, each with a lip. Sunk a body-height into the bank and **roofed along its length with stone lintel slabs** (Riverwarden work, Braid-like), with a hazel screen over the joints, so its water cannot be seen from above or from a distance at all. The only gaps in the roof run beside the flagged lip path, and those gaps lie inside the observation volume. A damp line runs up the inside walls to the top step. A leaf is stuck to the top lip. |
| **D. The listening seat** | The watching place. | Beside the foot pool, a stone seat in an alcove under a heavy carved brow, facing a small round basin ringed with stone. The seat faces away from the channel. The basin is mirror-still; a lip of stone keeps the wind off it. |
| **E. Head cistern** | The stall. | A square stone tank at the top of the slope, full to the brim and spilling down a side spillway back into the pool. Its outlet gate is an empty slot a hand wide, carved with three rings. Chisel scars on the slot edges. |
| **F. Cutter's hut** | The paddle. | A collapsed coppice-cutter's shelter in the hazel. Its doorstep is a flat stone a hand thick with three carved rings on its edge and a groove worn by boots across the middle. |
| **G. Switchback** | Route up. | An old stepped path beside the channel (agility step-ups) and a longer earth switchback (walkable fallback). |
| **H. The Hazel Culvert** | Shortcut. | A stone-lined passage through the hill, Riverwarden carving at both mouths, wartime brick patches inside. Drained, it is a walkable path. |

**MAP VERIFICATION REQUIRED:** the culvert's far mouth should open somewhere the long road does not reach quickly (recommendation: the Ashenstead Fields edge, bypassing the orchard berms). If geometry does not allow, any useful lower path works; quest logic does not depend on the destination.

**LEVEL-ART REQUIREMENT (now supporting, not load-bearing):** the roof slabs and screen make the channel's water surface directly visible only from inside the observation volume at ordinary positions and zooms. The volume's edge is marked in the world: the lip path and channel-side bank are **flagged stone**, and everything outside is earth. The listening-seat brow and alcove walls are tagged **non-fading occluders** (exempt from the camera's occluder fade). Verify on the real rig, including with co-op partners in view. The **render rule in §2.4 is what guarantees honesty**, so a geometry miss can never show the water moving.

### 2.4 The observation rule [NEW]

The canal climbs only while **no one is watching it**. The game expresses "watching" in a way a server can check and a click-to-move player with a free camera can work out:

| Layer | Rule |
|---|---|
| **Server (progress)** | The rule is: **no player inside the observation volume watching the channel.** For each player, the canal is *unobserved* while that player's character is **outside the observation volume** (the flagged lip path, channel-side bank and head-cistern rim; the listening seat is outside it). Progress (float position, cistern drain, foot-pool level) advances only while unobserved. No camera data is used on the server. |
| **Client (render rule, binding)** | **Whenever the channel's water surface is directly in a camera view, it renders still.** Every client checks, every frame, whether any part of the channel surface is in its camera frustum and unoccluded. If it is, that part renders at rest (a thin skin of still water on each step), and the float shows at its last-seen step. This holds at any orbit, pitch or zoom, with occluder fade, from any position, and for a partner's camera too. The climbing animation is drawn **only in the listening basin's reflection**, seen from the seat. |
| **Geometry (support)** | The roof slabs, screen and non-fading brow keep direct views rare, so the render rule seldom has to act and the effect never looks like popping. |
| **The seat** | The **Sit** interaction applies a soft camera limit while seated: an orbit cone facing the basin and a zoom clamp. There is no cutscene and the player keeps control. Standing up releases it. |

How the player learns it, in order, without text: (1) the float moves while they are away; (2) it never moves while they watch, from anywhere, at any zoom; (3) the seat faces the wrong way, and its basin shows what the lip cannot.

### 2.5 Beats

**Beat 0 — Running backwards (`S00_arrive`).** *Objective: See what's wrong with the canal.* Enter area A. Sedge is at the pool (UC-D1). Three inspects at the foot: **moss on the downhill faces**, **damp line to the top**, **drowned arch**. Any two complete the step.

**Beat 1 — The float (`S01_float`).** *Objective: Test the water.* A bundle of cut reeds lies by Sedge's stack. Interaction **Set a reed float** (2 s) places a float prop on the foot pool at the channel's first step. The player must then leave the observation volume. On returning, the float is three steps up (it advances one step per ~10 s unobserved, up to three). Inspect on return: *"The float is three steps up the channel. The water around it is still."* Completes on that inspect.
If the player stands and watches instead, nothing happens; after ~60 s inside the volume, Sedge offers UC-D2.

**Beat 2 — Watch without watching (`S02_watch`) — the strange moment.** *Objective: See the water climb.* Sit on the listening seat (interaction **Sit**). See §2.6. The step completes when the reflected water reaches the top and the player sees the cistern spill back down (end of the presentation).
Hints, in order of escalation (no tracker text): the seat's inspect ("You can't see the channel from here at all."); Sedge's UC-D2; after a second failed watch, Sedge sits on the seat himself and looks at the basin, then gets up and goes back to his reeds.

**Beat 3 — The missing paddle (`S03_find_paddle`).** *Objective: Find what belongs in the head gate.* Climb to the head cistern (agility step-ups or the switchback). Inspect the **empty slot** ("three carved rings; chisel scars where something was levered out"). The player now recognises the hut step if they passed it; if not, the slot's inspect adds: *"Someone used good stone for something else, once."* Inspect the **hut doorstep** to complete.

**Beat 4 — Carry it home (`S04_seat_paddle`).** *Objective: Put the paddle back in the gate.* **Lever up the step** (3 s), then carry the paddle (carry state: walk and sprint, no agility, so the switchback is the only route) to the head cistern, then **Seat the paddle** (3 s). The spill stops; the cistern begins to fill properly. If the carry is dropped or the player logs out, the paddle returns to the hut.

**Beat 5 — Leave it be (`S05_leave`).** *Objective: Leave the canal to its work.* The canal needs ~90 s of accumulated unobserved time (anywhere, including the listening seat, where the player can watch the foot pool drop in the reflection while the canal lifts it away). Completes when the foot-pool level prop reaches "low" and the culvert mouth is clear.

**Beat 6 — Through the hill (`S06_culvert`).** *Objective: Walk the culvert.* Enter the Hazel Culvert. Stranded vermin in the last puddles (E1). Reach the far mouth: shortcut enabled. UC-D4 with Sedge on return, or the quest completes on the far-mouth volume if Sedge is not met.

### 2.6 The strange moment: presentation spec

| Element | Spec |
|---|---|
| Trigger | Player sits on the listening seat while unobserving (server event `uphill_canal.seat`). Repeatable every time they sit; required once. |
| Duration | ~20 s for the first full climb; afterwards continuous while seated. |
| The basin | A planar reflection (or a state-driven pre-baked reflection texture, §2.12) of the slope beyond and above the basin, which the seat's brow hides from direct view. The climb is seen **only** here. |
| What it shows | Water lifting from the foot pool into the first step as a smooth, clear sheet, the way cloth lifts when pulled from one corner. It climbs step over step, pausing at each lip for a heartbeat before going over, the reed float riding it. At the top it fills the cistern, which spills down the side spillway back into the pool: a loop going nowhere. |
| Audio | The water sound, normally a babble from uphill, softens to a steady pour that moves slowly upslope. Nothing else changes. No music. |
| The direct world | If the player turns the camera inside the alcove, they see the alcove walls and the brow. Nothing else moves. |
| Standing up | If the player stands up, the reflection breaks with a single ripple across the basin and the channel (now observed) is still. |
| UI | None. |
| Camera | Player-controlled within the seat's soft limit (orbit cone toward the basin, zoom clamp; no cutscene). If any direct view of the channel still occurs, the §2.4 render rule shows it still. |
| After | Seat inspect: *"A seat facing the wrong way. Built that way on purpose."* |

### 2.7 Encounters

| Id | Enemies | Placement | Role | Telegraph | Solo target |
|---|---|---|---|---|---|
| **E1** | 4 × River Skitter, 1 × River Leech | Last puddles in the drained culvert | Skitters: swarm, leashed to puddles. Leech: slow latcher | Skitters: chitter and bunch (~0.8 s) before a rush. Leech: rears (~1.2 s) | Required. Ends at 60–80% HP on a Milestone 1 character. Step onto dry stone to break the latch. |

Rule: nothing dropped advances the quest. Respawn point: the listening seat.

### 2.8 Steps

| Step | Objective | Completes on | Required |
|---|---|---|---|
| `S00_arrive` | See what's wrong with the canal. | Enter area A + 2 of 3 inspects | Yes |
| `S01_float` | Test the water. | Interaction `set_float`, then inspect float after ≥30 s unobserved | Yes |
| `S02_watch` | See the water climb. | `uphill_canal.seat` presentation reaches its loop point | Yes |
| `S03_find_paddle` | Find what belongs in the head gate. | Inspect slot + inspect hut doorstep | Yes |
| `S04_seat_paddle` | Put the paddle back in the gate. | `lever_step`, carry-deposit at gate, `seat_paddle` | Yes |
| `S05_leave` | Leave the canal to its work. | Accumulated unobserved time ≥ 90 s after S04 | Yes |
| `S06_culvert` | Walk the culvert. | E1 defeated + enter far-mouth volume → Completed | Yes |

### 2.9 Flags

| Flag | Set by | Read by |
|---|---|---|
| `UC_SEDGE_ASKED` | UC-D2 any node | UC-D4 variant |
| `UC_PADDLE_SEATED` | `S04` | Head cistern and foot-pool props |
| `UC_CULVERT_OPEN` | `S06` | Shortcut traversal (per player); Bryn bark |
| `UC_COMPLETE` | Completion | Post-MQ9 payoff (§2.11) |

### 2.10 Rewards

| Reward | Type | Notes |
|---|---|---|
| **The Hazel Culvert** | Access | A walkable shortcut through the hill. Latched per player: once drained, it stays drained even if the player stands on the lip forever. |
| Canal-foot seat | Place | The listening seat is a rest spot the player can return to. Sitting there always shows the canal working. |
| Knowledge | Knowledge | No mechanical bonus. After MQ9, the canal's inspects read as Braid work (§2.11). |
| Skill XP | Action only | Melee from E1. No lump quest XP. |

### 2.11 After MQ9: the richer payoff

If MQ9 is Completed (whether UC was finished before or after it), on the next visit:

| Where | Text or line |
|---|---|
| Head cistern inspect (replaces default) | *"Three rings on the paddle, three on the slot. The flow-table had the same marks along its braided lines. This is one of them. Small. Still working. Nobody told it to stop."* |
| Culvert lintel inspect (replaces default) | *"Riverwarden carving outside, wartime brick inside. The braid ran through here before the war patched it."* |
| Sedge (UC-D5) | See dialogue. Only if `LM_SEDGE_TRUST` is set (MQ8 Completed). |

Optional request to the Act II package (not required): if `UC_COMPLETE`, MQ9's flow-table could offer one extra inspect on the Brackenford braid: *"A tiny loop up a hill. You've sat beside it."* Nothing depends on it.

### 2.12 Failure, recovery, co-op, integration

| Situation | Handling |
|---|---|
| Player never thinks to walk away | The float moves for any reason the player leaves the volume (even fetching reeds). Sedge's UC-D2 at 60 s. |
| Player never finds the seat | Sedge sits on it (Beat 2 hint 3). The seat is the only furniture at the pool. |
| Carry interrupted | Paddle returns to the hut; re-lever (3 s). |
| Logout | Steps and latched props persist; float resets to the pool if S01 incomplete. |
| Co-op | Unobserved is per player (§2.4). A partner on the lip does not stop your canal; in your basin you may see their reflection standing beside water that climbs past their feet. Each player seats their own paddle prop; fallback if per-player props are not ready: the paddle is seated world-wide by the first player and later players' S04 completes on inspecting the seated paddle. |

**Needs:** an observation volume with per-player accumulated-time tracking (server); state-driven channel presentation (rest / climbing); a planar reflection on one small basin or a pre-baked animated reflection keyed to state (fallback); carry state; agility step-ups with switchback fallback; per-player latched water-level prop and culvert traversal gate.

### 2.13 Dialogue

```
UC-D1 (Sedge at the foot pool, cutting reeds)  [D-7]
UC-D1.01 SEDGE: (doesn't stop cutting) "Come to see it go uphill?"
  > "Does it?"                                      → UC-D1.02
  > "Who are you?"                                  → UC-D1.04
  > "Just passing."                                 → end
UC-D1.02 SEDGE: "What do you see it doing now?"
  > "Sitting there."                                → UC-D1.03
UC-D1.03 SEDGE: "Then that's what it's doing." (holds out a reed) "Float's cheaper than an argument."   → end
UC-D1.04 SEDGE: "Reed-cutter. Sedge, they call me. Cut where it's thick, leave where it's thin."   → UC-D1 options
```

```
UC-D2 (Sedge, after ~60 s of the player watching the float, or on talk after S01)  [D-7]
UC-D2.01 SEDGE: "Did it move while you watched it?"
  > "No."                                           → UC-D2.02
  > "It moved while I was gone."                    → UC-D2.03
UC-D2.02 SEDGE: "And while you weren't?"            {set UC_SEDGE_ASKED} → end
UC-D2.03 SEDGE: "So where would you sit, to see a thing that won't be seen?"
UC-D2.04 SEDGE: (nods at the alcove without looking at it) "Somebody thought about that. Long time ago."   {set UC_SEDGE_ASKED} → end
```

**Inspects**

| Object | Text | Condition |
|---|---|---|
| Moss, channel foot | "Moss grows on the downhill faces of the steps. As if water usually comes from above." | — |
| Damp line | "A damp line runs up the channel walls all the way to the top step. A leaf is stuck to the top lip." | — |
| Drowned arch | "A stone arch, half under the pool. Carved lintel. A path went through here once." | — |
| Listening seat | "A stone seat under a heavy brow, facing a small round basin. You can't see the channel from here at all." | before S02 |
| Basin | "Still as glass. A lip of stone keeps the wind off it." | — |
| Empty slot | "A slot a hand wide, three carved rings at its edges. Chisel scars where something was levered out." | — |
| Hut doorstep | "A flat stone with three carved rings on its edge. A groove worn across it by boots. Too good a stone for a step." | — |
| Seated paddle | "It fits as if it never left." | after S04 |

```
UC-D3 (barks)
On seating the paddle (S04), from below:   SEDGE: "That'll do it." (goes back to cutting)  [D-7]
Bryn Ruddock at the orchards, after S06:  BRYN: "Cutters say the hazel path's open again. Didn't touch it, did you?" (beat) "Course you did."
```

```
UC-D4 (Sedge at the foot pool, after S06)  [D-7]
UC-D4.01 SEDGE: "Pool's down. Path's dry."
UC-D4.02 [UC_SEDGE_ASKED] SEDGE: "You sat with your back to it. Most people won't."
UC-D4.02 [else] SEDGE: "Found the seat yourself. Good."
  > "Why does it stop when someone watches?"        → UC-D4.03
  > "Who built it?"                                 → UC-D4.05
  > "River keep you."                               → UC-D4.06
UC-D4.03 SEDGE: "What did it do while you watched it in the basin?"
  > "It climbed."                                   → UC-D4.04
UC-D4.04 SEDGE: "Then it doesn't mind being seen. Only stared at." (back to his reeds)   → UC-D4.06
UC-D4.05 SEDGE: "Somebody patient." (beat) "Somebody who didn't need thanking."   → UC-D4.06
UC-D4.06 SEDGE: "Leave it be, now. It knows its work."
       {event: UC-D4 end → quest Completed if S06 done}
```

```
UC-D5 (after MQ9 Completed, LM_SEDGE_TRUST set; Sedge at the foot pool)  [D-7]
UC-D5.01 SEDGE: "You've seen the table behind the falls."
UC-D5.02 SEDGE: "This is one stitch of it. The war pulled a hundred like it. This one somebody only stepped on."
  > "Can the others be put back?"                    → UC-D5.03
  > "It was still working, all that time."          → UC-D5.04
UC-D5.03 SEDGE: "Some. Ask the one at the Steps. Not me."   → end
UC-D5.04 SEDGE: "Water doesn't stop because people do."      → end
```

### 2.14 Mystery ledger

| Mystery | Author truth [PROPOSAL — DIRECTOR] | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Why the canal climbs** | A small surviving Braid that lifts water from a low wet hollow to a higher channel, spreading flood pressure over the hill. | Haunted; "forgets gravity." | The float; the reflection; the matching rings. | It's the Field-Mage's doing; it's a pump. | How Braids move water uphill at all. | Partly MQ9 (context: it is Braid work). The mechanism stays open in v1. |
| **Why it stops when watched** | Riverwarden works were made by listeners; a watcher's attention is a living imprint the water answers by holding still (C08 resonance). **Never stated in v1.** | "It's shy." | Only the behaviour. | Watching "breaks" it. | Everything. | None in v1. |
| **Who pulled the paddle** | Wartime work crews pulled Braid paddles when the Relief Cut was dug; this one ended up as a hut step. | — | Chisel scars, the doorstep, brick patches in the culvert. | Children stole it. | Who, when, by whose order. | None (local colour). |

**Review log:** independent review pass (Director ruling 6): the geometry-only honesty layer would break under a free, fading, zooming camera. The channel is now roofed and screened; the server rule is "no player inside the observation volume watching the channel"; the client render rule (the channel always renders still when directly in a camera view) is binding; the climb is shown only in the basin reflection from the seat, which applies a soft camera limit; the volume edge is flagged stone; E1 is restated as Milestone 1. Earlier: first draft used camera direction as the server rule; replaced with a server-checkable volume plus a geometry requirement so the free camera can never "catch" the canal and server and client always agree. The head-gate fix originally repeated MQ3's woodcutting-and-lever; replaced with finding and carrying a reused stone. Co-op griefing risk (a partner standing on the lip) removed by making observation per player.

---
## 3. TB — The Twice-Burned Tree

### 3.1 In one paragraph

On the Ashen Flats stands a tree split down the middle by two burnings, black on both halves, alive in the fork. Once a decade it fruits, and this is the year. Ashenstead says the fruit gives "a dream you walk in." The goblins from the burned barns say nothing; they have simply brought rakes. At dusk the player drives off a goblin crew shaking the tree, climbs into the fork (or uses the goblins' own hook-pole), and picks the fruit as it ripens. Sedge is sitting under the tree and has no intention of eating any. When the player eats a fruit, the Ashen Flats change around them while they stand in them: ash warms to gold, stumps become hedges, the barns stand whole, the furrows carry grain to the knee. It is night, and the player walks the real Flats through fields before the burning. There is no one in them. No fire, no voice, no name. At the end of the walk the tree stands single and whole, in leaf. Touching it, the player wakes under the split tree at first light. A second fruit can be carried to Joric Fen, who decides what to do with it himself.

**What the player should remember:** walking through standing grain where they know there is only ash. **What they might want next:** nothing required. The dream is a gift, not a clue.

### 3.2 Summary card

| Field | Value |
|---|---|
| Type | Environmental discovery. Dossier §XI "The Twice-Burned Tree" [CANON hook]. |
| Unlock | MQ5 Completed. |
| Length | 20–30 minutes (dusk to first light). |
| Combat | ~15%: one goblin encounter at dusk. |
| Skills | Melee. |
| NPCs | Sedge `[D-7]`; Joric Fen [CANON ANCHOR] (optional gift); an Ashenstead household voice. |
| Choice | What to do with the second fruit (give to Joric, leave it at the tree). |
| Unlocks | Nothing mechanical. Joric's later line; a fruit prop on his gatepost. |

### 3.3 The place: the Twice-Burned Tree (P27) and the Ashen Flats at night

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. The tree** | Fruit; Sedge; dream start and end. | A broad trunk split to the ground in two black halves, each scarred by a different fire (the inner char is older and smoother). Green shoots and small pale fruit in the fork. Fallen fruit pecked at on the ground. Offerings of nothing: just stones set in a ring, the way people mark a place they don't know what to do with. |
| **B. The goblin path** | Encounter. | A trampled line from the burned barns (P20) to the tree, dropped rakes, a broken basket, a goblin-sized ladder made of two hoe handles that could not have worked. |
| **C. The fork** | Agility climb. | Step up the lower char-scar, pull up into the fork. Fruit within reach. |
| **D. The Flats at night** | Dream walk. | The real terrain: burn boundaries, Joric's unplanted plot, the remembrance circle, the guide-line field (MQ5), the barns. In the dream all of it unburnt. |

### 3.4 Beats

**Beat 0 — It's fruiting (`S00_offer`).** *Objective: See the Twice-Burned Tree.* Offered by the household bark or by approaching the tree. Reaching area A before dusk shows green fruit; Sedge is not there yet. Inspect the fruit: *"Small, hard, green. Not yet."* A wait seat (a flat root) is offered: *Wait for dusk* (§0.4).

**Beat 1 — Rakes (`S01_goblins`).** *Objective: Drive off the goblins.* At dusk a Field Goblin crew arrives along the goblin path and starts beating the branches (E1). Unripe fruit falls and bursts. Win and they scatter back to the barns, leaving a long **hook-pole**.

**Beat 2 — The fork (`S02_pick`).** *Objective: Pick a ripe fruit.* As full dusk sets, the fruit in the fork pales and softens (prop swap). Two routes: climb into the fork (agility) and **Pick** (2 s), or use the dropped hook-pole at the base (**Hook a fruit**, 4 s; walkable fallback). Picking produces a fruit in the player's hand (carry state). Sedge is now under the tree (TB-D1).

**Beat 3 — Eat (`S03_eat`).** *Objective: Eat the fruit.* Interaction **Eat** on the carried fruit (consumes the carry). The dream begins (§3.6). If the player would rather not, they can set it down (**Leave it at the tree**); the quest then completes on TB-D3 without the dream and the tree keeps fruiting for this player until a later visit at dusk.

**Beat 4 — Walk (`S04_dream`).** *Objective:* none shown (§3.6: no UI). The step completes when the dream ends by any of its three exits.

**Beat 5 — First light (`S05_wake`).** *Objective: Speak with Sedge, or don't.* At first light the player stands where the dream ended. Sedge has gone; his cut reeds are stacked by the tree. A second ripe fruit hangs low enough to pick by hand from the ground. Picking it is optional (`S06_gift`).

**Optional — For Joric (`S06_gift`).** Carry the fruit to Joric at the Ashen Flats work edge (TB-D4). If the carry is dropped, the fruit returns to the tree. Fallback if carry cannot travel that far: tell Joric where it hangs; next dawn he stands under the tree holding it (scheduled position for this player).

The quest completes at the end of TB-D3 (Sedge's dawn line, spoken by Ashenstead household instead if `LM_SEDGE_TRUST` is unset and the player skips him) or at `S06_gift` end, whichever comes first after S05.

### 3.5 Encounters

| Id | Enemies | Placement | Role | Telegraph | Solo target |
|---|---|---|---|---|---|
| **E1** | 2 × Field Goblin trapper, 1 × Field Goblin scrapper | At the tree, beating branches | Trappers: drop a rake-trap at their feet when engaged (visible tines, ~1 s set); scrapper: rushes the player with a hoe | Trapper: kneels to set (~1 s). Scrapper: raises hoe two-handed (~1.2 s) before an overhead | Required. 40–60 s. A player who walks round the set traps takes little damage. They do not flee at low HP; they scatter only when all three are down (rout as a group bark on defeat, not mid-fight). |

The goblins drop farm-tool junk only. Nothing advances the quest except the hook-pole, which is a world prop, not loot.

### 3.6 The strange moment: the dream (presentation spec)

| Element | Spec |
|---|---|
| Trigger | `S03_eat` complete → server event `twice_burned.dream_start` for that player. |
| Transition | ~10 s, around the player, while they keep control: ash ground warms through grey to gold from the player's feet outward; charred stumps resolve into hedgerows; the barns at P20 stand whole and roofed (no goblins); furrows rise into standing grain to the knee. The sky does not change. It is the same night, the same moon. |
| Space | The real Ashen Flats, walked in real space, within a bounded dream area (Flats boundary, MAP VERIFICATION REQUIRED). The player walks and sprints as normal. Grain parts and rustles around them. |
| What is there | Fields, hedges, gates (one standing open), the barns, lanes, a scarecrow on a pole (empty sleeves, no face), the remembrance circle's site as a plain field corner, Joric's plot as grain like every other field, a window in a barn with light behind it and nothing inside when looked into. |
| What is never there | **No person, no figure, no shadow of one, no voice with words, no fire, no smoke, no event, no name, no writing.** No animals that belong to someone (no dog, no tethered horse). No guide-line channel, no culvert, no stone the player could read. Nothing to inspect: inspect interactions are disabled for the dreamer. |
| Audio | Wind through grain, crickets, a gate knocking softly on its latch, the river very far off. No music. |
| The tree | Seen from anywhere in the dream: a single whole tree in full leaf where the split tree stands. |
| Exits | (1) Touch the whole tree (interaction **Touch**) → the dream fades over ~5 s and the player wakes under the split tree at first light. (2) Walk off the dream boundary → the grain thins to ash at the boundary edge and the player wakes where they stand. (3) Time: after ~6 minutes the fields fade from the edges inward, and the player wakes where they stand. |
| Safety | The dreamer has no aggro for its duration; any hostile entering 15 m ends the dream softly (exit 3 at once). Damage ends it. |
| UI | None from start to wake. No objective text. |
| Camera | Player-controlled. |
| Co-op | Per player. Partners see the dreamer walking in the burned Flats, slowly, through nothing. They cannot join it; talking to the dreamer does nothing until they wake. |
| After | Tree inspect: *"Split to the ground. Something green in the fork."* The dream does not repeat this decade (once per character). |
| What it means | The Flats were fields once. That is all it shows. It does not say who farmed them, what burned them or when. |

### 3.7 Steps

| Step | Objective | Completes on | Required |
|---|---|---|---|
| `S00_offer` | See the Twice-Burned Tree. | Enter area A | Yes |
| `S01_goblins` | Drive off the goblins. | Time window dusk → E1 defeated | Yes |
| `S02_pick` | Pick a ripe fruit. | Interaction `pick_fruit` or `hook_fruit` complete | Yes |
| `S03_eat` | Eat the fruit. | Interaction `eat_fruit` (or `leave_fruit` → skip to S05) | Yes |
| `S04_dream` | — | `twice_burned.dream_end` (any exit) | Yes if eaten |
| `S05_wake` | Speak with Sedge, or don't. | Time window first light + TB-D3 end, or 60 s after wake | Yes |
| `S06_gift` | (Optional) Take a fruit to Joric. | Item-given (carry deposit) to Joric → TB-D4 end | No |

### 3.8 Flags

| Flag | Set by | Read by |
|---|---|---|
| `TB_DREAMED` | `S04` | TB-D3 variant; Joric's later line |
| `TB_DECLINED` | `leave_fruit` | TB-D3 variant |
| `TB_TOUCHED_TREE` | Dream exit 1 | TB-D3 variant |
| `TB_GIFT_JORIC` / `TB_GIFT_TREE` | TB-D4 (Joric keeps it / asks for it left at the tree) | Joric gatepost prop; Joric bark |

Reads `LM_SEDGE_TRUST` (Sedge variants) and `LM_FIELD_FIX` (Joric variant).

### 3.9 Choices and consequences

| Choice | Result |
|---|---|
| Eat or leave the fruit | Eating gives the dream. Leaving it is respected: Sedge: "Some don't. That's an answer too." No cost. |
| Give a fruit to Joric | **Joric decides**, not the player (anchor rule: he decides about his field himself). He either keeps it (sets it on his gatepost, where it stays until it is gone soft: `TB_GIFT_JORIC`) or asks the player to put it back at the tree (`TB_GIFT_TREE`). Which he chooses depends on whether the player tells him about the dream: if they do, he keeps it; if not, he asks for it to go back. Both responses are gentle. Neither reveals anything about his loss. |

### 3.10 Rewards

The dream. Nothing else, by design. Action XP from E1 (Melee). No item, no bonus. Ashenstead households greet the player differently afterwards (barks: "You ate one? What was it like?" / "My gran said you see the fields. Did you?").

### 3.11 Failure, recovery, co-op, integration

Death in E1: respawn at Ashenstead's remembrance circle; goblins reset at next dusk wait. Logout during the dream: the dream ends; on login the player is at the tree at first light with `S04` complete (do not re-run a once-per-decade moment the player already started). Logout before eating: the carried fruit returns to the fork. Co-op: per §3.6.

**Needs:** time-of-day windows (§0.4); per-player **dream presentation layer**: a client-side swap of the Ashen Flats dressing to an "unburnt" set within a bounded area, with ambient audio, inspect suppression and dreamer aggro immunity. This is the most expensive presentation in this file. **Fallback:** a smaller dream area (a ring ~60 m around the tree with the nearest field, hedge and barn swapped) keeps the moment intact. A full instanced phase is not required and is not recommended.

### 3.12 Dialogue

```
TB-D1 (Sedge under the tree at dusk, after S02)  [D-7]
TB-D1.01 SEDGE: "Got one, then."
  > "Will you eat one?"                         → TB-D1.02
  > "What does it do?"                          → TB-D1.04
  > [LM_SEDGE_TRUST] "Is it safe?"              → TB-D1.06
TB-D1.02 SEDGE: "Ate one once." (beat) "Didn't need to again."   → TB-D1 options
TB-D1.04 SEDGE: "It shows you a place." (beat) "Not a reason. Don't go looking for one."
TB-D1.05 SEDGE: "Eat it here, if you're going to. You'll walk. Mind you come back to the tree."   → end
TB-D1.06 SEDGE: "Safer than most things I've seen you do." → TB-D1.05
```

```
TB-D2 (Ashenstead household bark at the offer)
HOUSEHOLD: "It's fruiting. First time since my lad was small. Goblins found it before we did."
HOUSEHOLD: "My gran said you see the fields. Wouldn't say more. Said you'd see."
```

```
TB-D3 (first light; Sedge at the tree if LM_SEDGE_TRUST is set, else an Ashenstead household at the tree)  [D-7]
TB-D3.01 [TB_TOUCHED_TREE] SEDGE: "You came back to the tree. Good."
TB-D3.01 [TB_DREAMED, else]  SEDGE: "You walked off the edge of it. Most do."
TB-D3.01 [TB_DECLINED]       SEDGE: "Some don't. That's an answer too."
  > [TB_DREAMED] "It was all fields."            → TB-D3.02
  > [TB_DREAMED] "There was no one there."       → TB-D3.03
  > "River keep you."                            → end
TB-D3.02 SEDGE: "It was." (beat) "It will be again, some of it."   → end
TB-D3.03 SEDGE: "No. It doesn't show you people. People you have to go and find."   → end
       {event: TB-D3 end → S05 complete; quest Completed if S06 not started}

(household variant if LM_SEDGE_TRUST unset)
TB-D3.H1 HOUSEHOLD: "You're up early. Or late." (looks at the player's face for a while) "Oh. You ate one."   → end
```

```
TB-D4 (Joric Fen at the work edge, mending a net; player carrying a fruit)
TB-D4.01 JORIC: (looks at the fruit, not the player) "The tree's."
TB-D4.02 JORIC: "Didn't think I'd see it fruit again."
  > "It's for you."                                    → TB-D4.03
  > [TB_DREAMED] "I ate one. I walked the fields."     → TB-D4.10
TB-D4.03 JORIC: (keeps mending) "Kind of you. I'll not eat it."
TB-D4.04 JORIC: "Put it back at the tree, if you would. It should be there when it's ready to drop."
       {set TB_GIFT_TREE; carry → returned to tree} → end
TB-D4.10 JORIC: (stops mending)
TB-D4.11 JORIC: "Were they standing?"
  > "To the knee."                                     → TB-D4.12
TB-D4.12 JORIC: (long pause) "Water gives things back slowly. So does the ground, I suppose."
TB-D4.13 [LM_FIELD_FIX = plot] JORIC: "I'll set it on the post by the new ditch. It can watch the water go by."
TB-D4.13 [else]               JORIC: "I'll set it on my gatepost. Till it's gone soft. Then the ground can have it."
       {take fruit; set TB_GIFT_JORIC} {event: S06 complete → quest Completed}
```

Joric bark after `TB_GIFT_JORIC`, on the gatepost prop: "Still there. Going soft. That's all right."

### 3.13 Mystery ledger

| Mystery | Author truth [PROPOSAL — DIRECTOR] | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The dream** | The tree grew on ground soaked in the Flats' grief before and after two fires; its fruit carries the place's imprint, not any person's (C08). It shows land, never people or events. | "You see the fields." Some say you see the dead (you don't). | The dream itself. | It's a vision of the burning (it isn't); it shows Joric's family (it shows no one). | Why the tree, why a decade. | None in v1. |
| **The two burnings** | Two separate fires; the older char is smoother. | War, and "the second time." | Char texture; household talk. | Both were the war. | What the second fire was. | None in v1 (local colour; do not build on it without a record). |

**Review log:** a household line once showed gold dust on the player's boots after waking; cut (no physical trace of the dream). First draft showed one figure at the end of a lane; cut (the brief forbids any person). First draft let Joric recognise his field in the dream; cut, his plot is indistinguishable and he is never told it was "his" field. The dream once lit inspect texts in the fields; cut (no text explaining). The goblins originally fled at low HP; changed to a group scatter after defeat, per combat rules.

---
## 4. WD — The Whispering Door

### 4.1 In one paragraph

The Dunnock farm sits on the Heartlands edge where the fields start to run toward Ashenstead. Its cellar door creaks before drift comes: a long, slow, rising creak, like someone breathing in. The Dunnocks treat it as a warning bell. When the door goes, the children go upstairs and Rhoda Dunnock sits on the stair with a hay fork, listening for which way it creaked. Since the flushes stopped, the door has gone more often, not less. The player arrives on a night it is going to go. They help the household ready the yard, wait, and learn to listen: before each rise the door creaks, and the length and pitch of the creak tell which of the yard's three outlets the water will come up through next. The player gets there first and holds the lid while drift rises around them. At first light the door is quiet, and the player goes down. Under the cellar floor is a brick wartime drain stencilled KEEP CLEAR, running toward the fields (after MQ5, its stencils and debris show what that ground was used for). Its iron flap valve has rusted open, so heavy water backs up the drain whenever the fields' water rises, and the air it pushes ahead of it climbs the cellar stair and works the door. The player follows the drain to the valve, fights what lives in it, and decides with the Dunnocks how to close it. The site goes quiet. The door is mostly explained. Mostly.

**What the player should remember:** the creak in the dark before anything happens, and knowing where to run because of it. **What they might want next:** nothing required; after MQ5 the drain's stencils echo it.

### 4.2 Summary card

| Field | Value |
|---|---|
| Type | Environmental discovery. Dossier §XI "The Whispering Door" [CANON hook]. Drift site **farmhouse cellar** (bible §9.2). |
| Unlock | MQ4 Completed. |
| Length | 30–40 minutes. |
| Combat | ~35%: a listening defence (3 waves) and the drain. |
| Skills | Melee. Smithing optional (rehang the flap); Woodcutting optional (bar timber). |
| NPCs | Rhoda Dunnock (farmer) [NEW], Col Dunnock (her son, about twelve) [NEW]; Ansel Corrie (bark). |
| Choice | How to close the drain (rehang the flap / brick it shut). |
| Unlocks | Farmhouse cellar drift site → **quieted**. The Dunnock farm as a friendly waypoint (hearth, a meal). |

New names checked against `LORE/` and every `04_CONTENT_PRODUCTION` file: Dunnock, Rhoda, Col (no matches; independent review pass). The household was renamed from "Hobb", which collided with Act I's far-bank Hobb household.

### 4.3 The place: the Dunnock farm

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Yard** | Defence ground. | Muddy yard with **three outlets** where the water comes up: a stone-lidded yard drain in the middle that nobody walks over, the pump trough by the wall, and the cellar light-well grate under the kitchen window. Each has a worn plank lid beside it. Hurdles stacked to make a pen. Lanterns burn on the corner poles (ambience only). |
| **B. Kitchen** | Hearth; family. | Low beams; tally marks on the doorframe by the cellar door, one per creak, in seasons, each with a small sign beside it (a line, a cup, a square) for which outlet rose. The marks are thicker this year. A hay fork leaning by the stair. |
| **C. The cellar door** | The door. | Old oak, iron-strapped, warped at the top corner. Its latch is tied with twine. Light shows under it. |
| **D. Cellar** | Descent. | Shelves of crocks and apples, a damp floor, and in the corner a square iron grate in the floor that the Dunnocks have covered with a board and two flour sacks. A tide line on the wall at knee height. |
| **E. The drain** | Lore and danger. | Brick-lined, stooping height. **Before MQ5 Completed:** stencilled at intervals **DRAIN — KEEP CLEAR** and a direction arrow; silt and broken crocks only. **After MQ5 Completed** (an echo, never a first reveal): the stencils read **TREATMENT BOUNDARY — KEEP CLEAR**, and old bandage tins (no names) and a rotted stretcher pole lie in the silt. |
| **F. The valve chamber** | Fix. | Where the drain meets a larger stone channel (the guide-line's outfall branch). A hinged iron flap valve rusted fully open, a wedge of debris jammed in its hinge. |

**MAP VERIFICATION REQUIRED:** the farm must lie on the Heartlands edge nearest Ashenstead Fields so that a drain toward the guide-line is plausible. The drain section authored here is short; it ends at the valve chamber and does not connect to MQ5's culvert for traversal.

### 4.4 Beats

**Beat 0 — The farm gate (`S00_offer`).** *Objective: Find out what the Dunnocks are afraid of.* Rhoda is hauling hurdles across the yard at dusk (WD-D1).

**Beat 1 — Ready the yard (`S01_ready`).** *Objective: Help the Dunnocks get ready for the night.* Three tasks, any order: **Lay the lids** on the three outlets (interaction ×3; Col names each one and the creak that goes with it), **Pen the hurdles** around the yard drain (one carry ×2: hurdle to drain), **Bar the kitchen door** (interaction; the bar is short a length; a Woodcutting stem from the hedge ash makes a longer bar, optional `S01b_bar`, which reduces wave 3 pressure on the door). Col follows the player and narrates.

**Beat 2 — Wait (`S02_wait`).** *Objective: Wait with the Dunnocks.* Sit at the kitchen hearth (wait interaction, §0.4). Rhoda and Col talk (WD-D2) while the night comes in. Then the door (§4.6).

**Beat 3 — Hold the house (`S03_defend`).** *Objective: Keep the drift away from the house.* **The listening loop.** About 12 s before each wave the cellar door creaks, and the creak says where the water will rise: **long and low** = the yard drain; **short and high** = the pump trough; **two quick catches** = the light-well grate. The player goes to that outlet and **Holds the lid** (stand on it; a 3 s channel that completes if they arrive before the rise). A held outlet lets up one drift fewer, and those that do rise form slowly (+1 s on their telegraph). A wrong or late guess costs nothing but a fuller wave. Col calls his guess from the stair, and he is right only for the first wave. If drift reaches the kitchen door it batters it; the door holds (it cannot break), but Col's barks escalate and the wave timer extends. Nothing is lost if the player is slow. Before wave 3 a second creak follows the first and matches no outlet; nothing rises where it might point (§4.6).

**Beat 4 — First light (`S04_down`).** *Objective: Go down to the cellar.* The door is quiet. Rhoda unties the latch (WD-D3). In the cellar: inspect **tide line**, **grate**; **Lift the grate** (3 s).

**Beat 5 — The drain (`S05_drain`).** *Objective: Follow the drain.* A stooping crawl along the brick drain (walkable, slow; no agility needed). Stencils and debris inspects. River Skitters in the silt pools and a River Leech at the valve (E4).

**Beat 6 — The valve (`S06_fix`).** *Objective: Close the drain.* Inspect the flap (rusted open; a wedge in the hinge). **Clear the hinge** (3 s). Then the choice (WD-D4, Rhoda has followed with a lantern):
- **Rehang the flap** (Smithing entry level at a portable anvil-stone in the chamber: 3 s channel ×2; or, without Smithing, a crew repair channel taking longer, 6 s ×2). Water can leave the cellar but not come back up.
- **Brick it shut.** Old bricks are stacked in the chamber (left by whoever patched the drain). Three **Lay bricks** channels.

**Beat 7 — The quiet (`S07_quiet`).** *Objective: Tell the Dunnocks it's done.* Back in the kitchen, Col makes one more tally mark on the doorframe and crosses it through (WD-D5). Drift site: farmhouse cellar → quieted. Quest Completed.

### 4.5 Encounters

| Id | Enemies | Placement | Role | Telegraph | Solo target |
|---|---|---|---|---|---|
| **E1** | 2 × drift (1 if the outlet is held) | The outlet the creak named (wave 1: always the yard drain, long and low) | Place-bound; drift toward the player at the lid, then the kitchen door | Water at the outlet "stands up" (~1.5 s; ~2.5 s at a held outlet) before each forms; a cold-mist lunge with ~1 s windup | Disperse all. ~30 s. |
| **E2** | 3 × drift (2 if held) | The outlet the creak named (pump trough or light-well grate, varied per night) | As E1 | As E1 | ~45 s. |
| **E3** | 2 × drift, 1 × lantern-drift (1 drift fewer if held) | The outlet the first creak named; nothing rises at the second creak's | Lantern-drift carries a cold light; its pulse is a ring on the ground (~1.5 s) that the player steps out of | Ring telegraph | 60–90 s. Ends at 50–70% HP on a Milestone 1 character. Dispersed drift does not re-form tonight (the night's water has gone back down). |
| **E4** | 3 × River Skitter, 1 × River Leech | Drain silt pools; leech at the valve | As UC E1 | As UC E1 | Required. Short. |

Drift re-forms on later nights until S07 (site **active**). After S07 the farm spawns no drift. Respawn point: the Dunnock kitchen hearth.

### 4.6 The strange moment: the door (presentation spec)

| Element | Spec |
|---|---|
| Trigger | End of WD-D2 (server event `whispering_door.creak`), ~20 s before wave 1; then before waves 2 and 3 (`whispering_door.creak_wave`, carrying the outlet id that selects the creak sound). |
| The sound | A long, slow creak rising in pitch over ~4 s, like a breath drawn in through the teeth, from the cellar door. Positional; loud enough to be heard in the yard. Then a pause. Then a second, shorter one. |
| The door | Moves inward a finger's width against its twine, holds, settles back. The light under it flickers as air moves past. The candle on the kitchen table leans toward the door and straightens. |
| The household | Rhoda stands, takes the fork, sits on the stair. Col goes up two steps and stops. Nobody speaks for the length of the creak. Then Rhoda: "That's it, then." |
| UI | None until wave 1 forms. |
| Camera | Player-controlled. |
| Repeat | Plays on every active night the player is present before S07. After S07 rehang: the door creaks only on wet-season nights (air, no drift), a shorter, plainer sound. After S07 brick: it never creaks again. |
| The three creaks | Long and low (yard drain), short and high (pump trough), two quick catches (light-well grate). Each is distinct by length and pitch, so it reads without subtitles; Col's WD-D2 lines teach the set once. |
| The unexplained half | At the first creak, and again before wave 3, a second, shorter creak comes **before** the drain water rises (the tide in the cellar only begins after it) and matches no outlet. The air explanation covers the first creak. Nobody comments on the second. |

### 4.7 Steps

| Step | Objective | Completes on | Required |
|---|---|---|---|
| `S00_offer` | Find out what the Dunnocks are afraid of. | WD-D1 end node | Yes |
| `S01_ready` | Help the Dunnocks get ready for the night. | 3 `lay_lid` interactions + 2 hurdle deposits + bar interaction | Yes |
| `S01b_bar` | (Optional) Cut a longer bar. | Woodcutting stem acquired + `fit_bar` | No |
| `S02_wait` | Wait with the Dunnocks. | Wait interaction (night window) → WD-D2 end (fires creak) | Yes |
| `S03_defend` | Keep the drift away from the house. | E1, E2, E3 dispersed | Yes |
| `S04_down` | Go down to the cellar. | Dawn window + `lift_grate` complete | Yes |
| `S05_drain` | Follow the drain. | Enter valve-chamber volume + E4 defeated | Yes |
| `S06_fix` | Close the drain. | `clear_hinge` + WD-D4 choice + repair channels complete | Yes |
| `S07_quiet` | Tell the Dunnocks it's done. | WD-D5 end node → Completed; site → quieted | Yes |

### 4.8 Flags

| Flag | Set by | Read by |
|---|---|---|
| `WD_BAR_LONG` | `S01b_bar` | E3 door pressure |
| `WD_LIDS_HELD` (0–3) | `hold_lid` before each rise | Rhoda's dawn line (`WD-D3.00`) |
| `WD_FLAP` / `WD_BRICKED` | WD-D4 (exactly one) | Door behaviour (§4.6); Rhoda and Col barks |
| `WD_QUIETED` | `S07` | Drift-site state for farmhouse cellar |

Reads `LM_FEN_ENDING`: after MQ11 the site stays quieted under every ending (the cause was local).

### 4.9 Choices and consequences

| Option | Result | Cost |
|---|---|---|
| **Rehang the flap** | The drain works as built: the cellar drains in wet weather; nothing comes back up. The door keeps a plain creak on wet nights. Col: "So it still talks. Just about rain." | Needs care. Rhoda: "Someone'll have to grease that every spring. Me, then." |
| **Brick it shut** | Nothing comes up, ever. The door is silent. | The cellar takes groundwater damp in wet seasons (crock shelves raised: prop). Col is quietly sad: "It was our bell." |

### 4.10 Rewards

| Reward | Type | Notes |
|---|---|---|
| Quieted drift site | World change | No more drift at the farm. |
| Dunnock hearth | Place | A friendly waypoint: the player can rest and is given a cooked meal once per visit (existing food item; item pass). |
| Small payment | Currency | Rhoda, "for the listening." |
| Skill XP | Action only | Melee; Smithing (rehang) or none; Woodcutting (optional bar). No lump quest XP. |

### 4.11 Failure, recovery, co-op, integration

Death during the defence: respawn at the hearth; the current wave restarts; dispersed waves stay dispersed. Logout during the night: on return, the night restarts from S02 (the wait). Logout in the drain: restart at the cellar grate. Co-op: shared world drift; each player's wave progress is credited from shared kills; the door creak plays for every player in the kitchen whose own step is S02; per-player valve state (fallback: first player's fix is world-wide; later players' S06 completes on inspecting the closed valve and making the same choice in dialogue, which sets their flags only).

**Needs:** night and dawn windows (§0.4); drift-site state with per-player quieting (bible §9.2); wave spawner bound to three outlet points, chosen per wave and announced by a creak sound keyed to the outlet; a `hold_lid` channel at each outlet that reduces that wave's count; a door that "holds" (damage target that cannot break, drives barks); stooping crawl animation or simply a low-ceiling walk; Smithing station-less channel (portable anvil-stone) or route the rehang through a crew-repair channel only if a field Smithing interaction is out of scope.

### 4.12 Dialogue

```
WD-D1 (Rhoda in the yard at dusk, dragging a hurdle)
WD-D1.01 RHODA: "If you're lost, the road's that way. If you're not, grab the other end of this."
  > (Take the other end.)                         → WD-D1.02
  > "What's all this for?"                        → WD-D1.03
WD-D1.02 RHODA: "Good. Over the drain. Nobody steps on that drain."   → WD-D1.03
WD-D1.03 RHODA: "Door's going to go tonight. Cellar door. It creaks before they come up."
WD-D1.04 COL: (from the kitchen step) "It's a warning bell. It's better than a bell. Bells you have to ring."
WD-D1.05 RHODA: "Lids on the drain, the trough and the window grate. Hurdles round the drain. Bar on the door. Then we sit, and we listen."
       {event: WD-D1 end → S00 complete}
```

```
WD-D2 (kitchen hearth, waiting; opens on the wait interaction)
WD-D2.01 COL: "Thirty-one marks this year. Mam says last year was nine."
WD-D2.02 RHODA: "Since they stopped the barges. You'd think it'd go the other way."
  > "How long has the door done this?"             → WD-D2.03
  > "Have you ever opened it when it creaks?"      → WD-D2.05
WD-D2.03 RHODA: "Longer than me. Gran said it was a draught. Then she said it was a warning. Then she stopped saying."   → WD-D2.06
WD-D2.05 RHODA: "Once." (beat) "Water on the stair. Cold. I shut it."     → WD-D2.06
WD-D2.06 COL: "Long and low's the drain. Short and squeaky's the trough. Two little ones is the window grate." (beat) "I worked it out. Mam says I made it up."
WD-D2.07 RHODA: "He didn't make it up."
WD-D2.08 COL: (very quietly) "Shh."
       {event: whispering_door.creak → §4.6; S02 complete}
```

Defence barks:

| Trigger | Speaker | Line |
|---|---|---|
| Wave 1 forms | RHODA | "Out of the drain. Same as ever." |
| Creak before a wave | COL | (his guess, from the stair) "Drain!" / "Trough!" / "Window!" |
| Player holds the right lid | RHODA | "That's the one. Stand on it." |
| Drift at the kitchen door | COL | "It's at the door. It's at the *door*." |
| Drift at the door, `WD_BAR_LONG` | RHODA | "Bar's holding. Good bar." |
| Wave 3 dispersed | RHODA | "That's it. That's always it, the third lot." |

```
WD-D3 (first light, at the cellar door)
WD-D3.00 [WD_LIDS_HELD ≥ 2] RHODA: "You were on the lids before Col was." (beat) "Don't tell him."
WD-D3.01 RHODA: (unties the twine) "Quiet now. It's always quiet by morning."
WD-D3.02 RHODA: "There's a grate in the corner. We put sacks on it. That's where the water comes."
  > "I'll go down."                                → WD-D3.03
WD-D3.03 COL: "Take the lantern. And come back. Mam, tell them to come back."
WD-D3.04 RHODA: "Come back."                       → end
```

Drain inspects:

| Object | Text |
|---|---|
| Tide line | "A damp line at knee height on every wall. The cellar has filled to here, and drained, many times." |
| Grate | "Iron, old, square. Cold air comes up through it. It smells of river, not of cellar." |
| Stencil (before MQ5) | "DRAIN — KEEP CLEAR. An arrow points down the drain." |
| Stencil (after MQ5) | "TREATMENT BOUNDARY — KEEP CLEAR. An arrow points down the drain." |
| Bandage tins (after MQ5 only) | "Empty tins, rusted. Wartime issue. No names." |
| Stretcher pole (after MQ5 only) | "Half a stretcher pole, rotted. Somebody carried people along here once." |
| Flap valve | "A hinged iron flap meant to let water out and not back in. Rusted wide open. Something is wedged in the hinge." |
| Valve chamber channel | "A bigger stone channel runs past, toward the fields. When it rises, all of it can come up the drain." |

```
WD-D4 (valve chamber, after clear_hinge; Rhoda has come down with a lantern)
WD-D4.01 RHODA: "So that's the door. Water comes up the drain and pushes the air up my stair."
WD-D4.02 RHODA: "And the cold ones come with the water." (beat) "Can you shut it?"
  > "I can rehang the flap. Water out, nothing in."    → WD-D4.10
  > "Brick it up. Nothing comes through, ever."         → WD-D4.20
WD-D4.10 RHODA: "Someone'll have to grease it every spring." (beat) "Me, then."   {set WD_FLAP} → end
WD-D4.20 RHODA: "Cellar'll be damp." (beat) "Damp I can live with."            {set WD_BRICKED} → end
```

```
WD-D5 (kitchen; Col at the doorframe with a knife)
WD-D5.01 COL: (cuts a mark, then a line through it) "That's the last one."
WD-D5.02 [WD_FLAP]    COL: "So it still talks? Just about rain?"
WD-D5.02 [WD_BRICKED] COL: "So it won't go again. Ever." (beat) "It was our bell."
WD-D5.03 RHODA: "Sit. Eat. You've earned the good end of the loaf."
  > "Why did it creak twice?"                         → WD-D5.04
  > (Sit and eat.)                                    → WD-D5.05
WD-D5.04 RHODA: (looks at the door for a while) "Draught." (beat) "Eat."   → WD-D5.05
WD-D5.05 RHODA: "River keep you. Come back when you're passing. The door won't mind."
       {set WD_QUIETED; event: WD-D5 end → quest Completed}
```

Ansel Corrie bark at the Lantern Post after completion: "Dunnock farm's off my list. Never had a door taken off my list before."

### 4.13 Mystery ledger

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Why the door creaks** | Mostly air: water backing up a wartime drain pushes air up the cellar stair (resolved here). | A warning from the dead; a draught. | Tide line, open flap, the channel, the cold air through the grate. | The door is haunted. | — | WD (resolved). |
| **The second creak** | **Left open [PROPOSAL — DIRECTOR].** It comes before the water rises. Compatible with resonance; never stated. | — | Timing only, for a player who notices. | It proves the dead knock first. | Everything. | None in v1. |
| **Why drift got worse after the flushes stopped** | After MQ4 the fen is holding pressure (bible §2.3); fields' water rises more often. Consistent with Act II; not explained here. | — | Col's tally. | The Dunnocks did something wrong. | The fen. | MQ5, MQ8, MQ11. |

**Review log:** independent review pass: (1) the lantern-relight defence repeated NT's verb set, so it was replaced with the listening loop (the creak tells which outlet rises; hold the lid), and the lanterns are now ambience; (2) the treatment-boundary dressing gave away MQ5's reveal when WD was played between MQ4 and MQ5, so it is now conditional on MQ5 Completed; (3) E3 was restated as Milestone 1; (4) the household was renamed Hobb → **Dunnock** (name collision with Act I). Earlier: first draft had the drain lead the player into MQ5's culvert; cut to avoid spoiling MQ5 and to keep this quest local. The door originally broke in wave 3; changed to an unbreakable door that drives barks (no fail state). The rusted flap originally needed a forge visit at Crestbridge; replaced with an in-place repair so the fix stays physical and close.

---
## 5. CN — The Candle Rule

### 5.1 In one paragraph

Maud Holt has set a candle-boat on the Ashenstead watergarden every flood season since her son Ewan went to the war and did not come back. This week it is gone, and her daughter Bet says Annelise Reed took it: that Annelise, who keeps Ewan's name off the memorial stone, has now put out his light as well. Annelise does not argue. She pinches out every unattended candle in the garden; she always has. The player reads the garden: the wax on Annelise's snuffer, the drying ledge by the outlet where families' boats sit with their own chalk signs, an empty space marked with the Holt sign, and a wet line on the stone above it from the flush night. The boat was set safe and the water took it. It is circling in the outfall pool below the garden, where rotting offerings have choked the water still and drift has started to rise. The player cannot chase a boat through heavy water; they change the water instead, setting the outfall's three boards to the heights their rope-wear shows, under drift attack. The pool unwinds and brings the boat to the lip. Its wick is pinched flat between two fingers. The Holts and Annelise then decide, together, how Ewan is remembered in a garden that cannot hold an unattended flame.

**What the player should remember:** the stuck water letting go and handing the boat back. **What they might want next:** to see the boat launched on water that can carry it (MQ11, if Tend or Shared).

### 5.2 Summary card

| Field | Value |
|---|---|
| Type | Memory/lore (Phase 1.5). Lattice L-S09 (L-S18's evidence threshold respected). Drift site **watergarden outlet** (bible §9.2). |
| Unlock | MQ3 Completed. |
| Length | 25–35 minutes. |
| Combat | ~25%: drift at the outfall pool. |
| Skills | Melee. |
| NPCs | Annelise Reed [CANON ANCHOR]; Maud Holt [NEW], Bet Holt [NEW] (Maud's daughter, Ewan's sister); Ashenstead garden visitors (role). |
| Choice | The form of remembrance (2 options). |
| Feeds | MQ11 Tend argument (§5.9). |

**Canon guard for Annelise:** her lines use only canon traits (gentle, deliberate, speaks softly to the water while working, dislikes unattended candles, removes offerings before they rot, knows which names never appear on public memorials, "light enough to carry"). No age, service, kinship, travel, meetings or record custody is given to her. The families chalk their own boats; Annelise keeps no register.

### 5.3 The place: Ashenstead watergarden and outfall (P23)

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Reflection pool** | The accusation. | Still, clear water. Candle-stands of flat stone at the rim, each with wax drips. Small offerings: ribbons, a carved fish, a dried flower crown. Annelise's long-handled snuffer leans on her basket. |
| **B. Memorial stone** | Context. | Names cut for the confirmed dead. A smooth band at the bottom with nothing on it. Fresh chalk marks on the band, scrubbed off, faint. |
| **C. Drying ledge** | Evidence. | A stone shelf beside the outlet, above the usual water. Small reed boats in a row, each chalked with a family sign on the bow. An empty space, its chalk sign (a hooked H) still on the stone. A dark wet line on the wall a hand above the shelf. |
| **D. Outlet and outfall head** | The fix. | Where the pool drains: three wooden outfall boards in stone slots, each raised or lowered by a rope over a peg. Each rope has a pale worn band where it usually sits on the peg; two are set wrong (flood debris knocked them). |
| **E. Outfall pool** | Danger; the boat. | Below the stepped outfall, a round pool choked with rotting offerings swept down from the garden, turning slowly in one place. The Holt boat circles in the middle. The water is dark and heavy; softmoss on the stones round it has gone brown. |

### 5.4 Beats

**Beat 0 — The accusation (`S00_offer`).** *Objective: Find out what happened to the Holts' boat.* Entering the garden: Bet's raised voice, Annelise working, Maud sitting by the pool (CN-D1).

**Beat 1 — Read the garden (`S01_read`).** *Objective: Look for the boat.* Inspects: **candle-stand** (Holt stand: wax drips, a clean ring where the boat sat), **snuffer** (wax on the cup; this is ordinary), **drying ledge** (row of boats, the empty Holt space), **wet line** (above the ledge: the water rose higher than the ledge in the night). Ledge + wet line are required; the others enrich CN-D2/D3 options. Talking to Annelise (CN-D2) and Maud (CN-D3) is optional but changes the closing scene.

**Beat 2 — The outfall (`S02_outfall`).** *Objective: Follow the outlet down.* Walk the stepped outfall to the pool. The boat is visible circling. Wading toward it: drift forms and the player is pushed back by the turning water (a slow shove, telegraphed, no damage; heavy water will not let the player reach the centre). Inspect the pool: *"The water turns in one place. It isn't going anywhere, and it won't let anything else go either."*

**Beat 3 — The boards (`S03_boards`).** *Objective: Get the outfall running.* At the outfall head, three boards. Each **Set the board** interaction (3 s) raises or lowers it one notch; the right height is where the rope's worn band sits on the peg (inspect each rope: *"The rope is worn pale in one band. That's where it usually sits."*). Drift from the pool harass the player at the head (E1). When all three sit at their worn bands, the outfall runs steadily: see §5.6.

**Beat 4 — The boat comes back (`S04_boat`).** *Objective: Take the boat.* The boat lodges at the pool lip. **Lift the boat** (carry state). Inspect while carrying: *"The wick is pinched flat between two fingers. The candle is dry. It was put out by hand before the water took it."* Site: watergarden outlet → quieted.

**Beat 5 — The light (`S05_choose`).** *Objective: Bring the boat back to the garden.* Deposit at the Holt candle-stand. CN-D4: the Holts, Annelise, the choice.

**Beat 6 — Dusk (`S06_dusk`).** *Objective: Sit with the light.* At dusk (wait, §0.4) the boat is lit on the pool with Maud beside it (both options; this is the first attended light). The player can sit (interaction) or leave. On sitting, or 60 s later, CN-D5 and Completed.

### 5.5 Encounters

| Id | Enemies | Placement | Role | Telegraph | Solo target |
|---|---|---|---|---|---|
| **E1** | 2 × drift, re-forming | Rise from the outfall pool, climb to the outfall head | Place-bound; target the player at the boards | Pool surface "stands up" (~1.5 s); cold lunge (~1 s windup) | Each dispersal buys ~20 s before re-forming. A player can set boards between waves or fight and set. Never more than 2 at once. |
| **E1b** | 1 × lantern-drift | Forms once, when the second board is set | Pulse ring on the ground (~1.5 s) | Step out | Disperses on hit like drift. When the third board is set, all drift sink (§5.6). |

Combat protects the work; it does not get the boat. Respawn point: the reflection pool bench.

### 5.6 The strange moment: the water lets go (presentation spec)

| Element | Spec |
|---|---|
| Trigger | Third board set to its worn band → server event `candle_rule.unwind`. |
| Duration | ~12 s. |
| Sound | The outfall's low, stuck gurgle (present all quest) clears into an ordinary running pour. Under it, for ~3 s, the whole pool makes no sound at all. No music. |
| The pool | The slow turn falters, stops, then the surface moves in one direction for the first time: toward the outlet lip. Rotted offerings sink in a slow ring from the edge inward. Any drift present sink with them, without being struck, like stones set down. |
| The boat | It stops circling, turns its bow to the lip, and comes across the pool at walking pace, not spinning, and lodges against the lip at the player's side of it. |
| Softmoss | The brown softmoss on the pool stones is unchanged (it does not heal; it simply stops getting worse; inspect later: *"Brown, but drying. Nothing new has rotted."*). |
| UI | None until the boat lodges. |
| Camera | Player-controlled. |
| What it means | The water moves now, so it can carry things. Nothing more. The boat's own wick, not the water, shows what Annelise did. |

### 5.7 Steps

| Step | Objective | Completes on | Required |
|---|---|---|---|
| `S00_offer` | Find out what happened to the Holts' boat. | CN-D1 end node | Yes |
| `S01_read` | Look for the boat. | Inspect drying ledge + wet line | Yes |
| `S02_outfall` | Follow the outlet down. | Enter outfall-pool volume + inspect pool | Yes |
| `S03_boards` | Get the outfall running. | 3 boards at worn height → `candle_rule.unwind` | Yes |
| `S04_boat` | Take the boat. | Interaction `lift_boat` (carry) | Yes |
| `S05_choose` | Bring the boat back to the garden. | Carry deposit at Holt stand + CN-D4 choice | Yes |
| `S06_dusk` | Sit with the light. | Dusk window + sit interaction or 60 s → CN-D5 end → Completed | Yes |

### 5.8 Flags

| Flag | Set by | Read by |
|---|---|---|
| `CN_ASKED_ANNELISE` / `CN_ASKED_MAUD` | CN-D2 / CN-D3 | CN-D4 options |
| `CN_WICK_SEEN` | Carry inspect in S04 | CN-D4 proof option |
| `CN_FORM_WATCH` / `CN_FORM_CARRY` | CN-D4 (exactly one) | Garden props; MQ11 Annelise argument variant (§5.9); barks |
| `CN_OUTLET_QUIETED` | `S04` | Drift-site state for watergarden outlet |
| `CN_COMPLETE` | Completion | MQ11 (Act III reads "completed CN") |

### 5.9 Choices and consequences

| Option | Immediate | Cost | MQ11 (Act III) |
|---|---|---|---|
| **The watch light** — *"Light it only when someone sits with it."* | The boat hangs on a hook by the Holt stand. On flood nights Maud or Bet light it and sit; when they go, they pinch it themselves. | Somebody has to sit, every time. Bet: "Then I'll sit." | Annelise brings the boat with Maud's leave. Suggested line: "Maud Holt sits with her light. Nothing goes heavy where someone sits." |
| **Water that carries** — *"Keep it until there's water fit to carry it."* | The family gives the boat into Annelise's keeping, to launch together the first time moving water runs from the garden to the fen edge. | It sits on a shelf, unlit, for now. Maud: "I can wait. I'm good at it." | Annelise brings the boat as her argument and launches it with the Holts in the Tend/Shared ending. Suggested line: "The Holts have waited for water that can carry. Give them some." |

Both forms answer the accusation the same way: the light was put out because no one was sitting with it, and the boat was set safe and taken by water. Neither puts Ewan's name on the stone (no confirming evidence exists; L-S18's threshold); Annelise offers, in both, to leave the bottom band blank "for whoever comes with something I can carve."

The suggested MQ11 lines are requests to the Act III package; Act III owns the final wording.

### 5.10 Rewards

| Reward | Type | Notes |
|---|---|---|
| Quieted outlet | World change | No drift at the outfall pool. |
| Annelise's trust | Standing | Barks; she greets the player by speaking to the water instead of stopping work (her way of including someone). |
| Small payment | Currency | From Maud, refused and pressed on the player. |
| Skill XP | Action only | Melee. No lump quest XP. |

### 5.11 Failure, recovery, co-op

The boat can always be reached by fixing the boards; there is no way to lose it. Dropped carry: the boat returns to the pool lip. Death: respawn at the pool bench; boards stay as set. Logout: steps persist; carry returns to the lip. Co-op: each player's boat and boards are per player; drift shared. Fallback without per-player props: the boards are world props and stay set; later players' S03 completes on inspecting the set boards and E1 spawns once for them.

### 5.12 Dialogue

```
CN-D1 (reflection pool; Bet standing, Maud sitting, Annelise clearing a flower crown)
CN-D1.01 BET: "She took it. Same as she takes his name off the stone every time we chalk it."
CN-D1.02 ANNELISE: (softly, to the water, lifting the crown out) "There. You were going brown."
CN-D1.03 BET: "Are you listening? He's not dead. Nobody ever said he's dead."
CN-D1.04 MAUD: "Bet." (beat) "Ask someone to look. Not shout."
  > "I'll look for the boat."                         → CN-D1.05
  > "Annelise, did you take it?"                      → CN-D1.06
CN-D1.05 MAUD: "It's a reed boat. A hooked H on the bow. He cut that mark on everything."   → end {event: S00 complete}
CN-D1.06 ANNELISE: "I put out a candle. I put out every candle that's left alone." (beat) "I didn't take a boat."   → CN-D1.05
```

```
CN-D2 (Annelise, working; optional)
CN-D2.01 ANNELISE: (to the water, as the player approaches) "Someone's come to ask."
  > "Why put out the candles?"                         → CN-D2.02
  > "Why isn't his name on the stone?"                 → CN-D2.04
  > "Where would a boat go?"                           → CN-D2.06
CN-D2.02 ANNELISE: "Because a flame left alone isn't remembrance. It's just a flame, and the reeds are dry."
CN-D2.03 ANNELISE: "Pinch it, set the boat on the ledge to dry. Every night. They know I do."   {set CN_ASKED_ANNELISE} → CN-D2 options
CN-D2.04 ANNELISE: "The stone is for the ones we know." (beat) "I don't know. Nobody does. That isn't the same as forgetting."   → CN-D2 options
CN-D2.06 ANNELISE: "Out the bottom, if the water rose. It rose." (looks toward the outlet) "And the pool down there's gone still. I don't like it still."   → end
```

```
CN-D3 (Maud, by the pool; optional)
CN-D3.01 MAUD: "I lit it and went home. Rain was coming. I meant to come back."
CN-D3.02 MAUD: "She's right about candles. I know she's right. Bet knows."
CN-D3.03 MAUD: "It's the stone. Bet can't stand the blank bit."
  > "And you?"                                         → CN-D3.04
CN-D3.04 MAUD: "I want the boat back. That's all I want today. Today's enough."   {set CN_ASKED_MAUD} → end
```

```
CN-D4 (at the Holt stand, after the boat is set down)
CN-D4.01 BET: (picks it up, turns it over) "It's ours. It's — the wick's pinched."
  > [CN_WICK_SEEN] "Put out by hand, before the water took it."      → CN-D4.02
  > "It was on the drying ledge. The water came over it."           → CN-D4.02
CN-D4.02 BET: (to Annelise, after a while) "You set it safe."
CN-D4.03 ANNELISE: "I set them all safe. The water doesn't always agree."
CN-D4.04 MAUD: "It can't sit there burning on its own. Not with the reeds. So what do we do with it?"
CN-D4.05 ANNELISE: (to the player) "You brought it up. What would you do?"
  > "Light it only when someone sits with it."                     → CN-D4.10
  > "Keep it till there's water fit to carry it."                  → CN-D4.20
CN-D4.10 BET: "Then I'll sit. I'm good at sitting. I've been sat at that stone for years."
CN-D4.11 ANNELISE: "And pinch it when you go." (beat) "Light enough to carry. That's all I've ever asked."
       {set CN_FORM_WATCH} → CN-D4.30
CN-D4.20 MAUD: "Water that carries." (beat) "Not this water. Not yet."
CN-D4.21 ANNELISE: (takes the boat in both hands) "I'll keep it dry. The first night the water runs clean to the fen, we'll go down together."
       {set CN_FORM_CARRY} → CN-D4.30
CN-D4.30 ANNELISE: "The bottom of the stone stays blank. Bring the stone-cutters something they can carve. I'll keep the water clear for it."
CN-D4.31 BET: "That's not nothing." (beat) "That's not nothing."
       {event: S05 complete}
```

```
CN-D5 (dusk; the boat lit on the pool, Maud sitting beside it; the player sits or stands)
CN-D5.01 MAUD: (not looking away from the flame) "He'd have laughed at all this fuss."
CN-D5.02 ANNELISE: (to the water, very softly) "There. Someone's with you."
CN-D5.03 MAUD: "Go on. I've got it now."
       {event: CN-D5 end → quest Completed}
```

Post-quest barks:

| Speaker | Line | Condition |
|---|---|---|
| BET | "My night to sit. Bring a blanket if you're stopping." | `CN_FORM_WATCH` |
| ANNELISE | (to the water) "Still on the shelf. Still dry. Not long, maybe." | `CN_FORM_CARRY`, before MQ11 |
| VISITOR | "The bottom pool's moving again. Smells better, anyway." | `CN_OUTLET_QUIETED` |

### 5.13 Mystery ledger

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Who took the boat** | Nobody: Annelise pinched and shelved it; the flush-night rise took it. | Annelise erased him. | Snuffer wax, ledge, wet line, pinched wick. | Annelise threw it away. | — | CN (resolved). |
| **What happened to Ewan Holt** | **Deliberately unselected.** No v1 content knows. | Unreturned. | None. | The drift at the pool was Ewan (nothing identifies anyone). | Everything. | None in v1; any later answer needs an independent record (L-S18). |
| **Why still water goes heavy** | Grief left to rot in still water gathers (bible §2.3). Moving water carries it. | "Bad water." | The pool unwinding; drift sinking. | The boards are magic. | The fen-scale version. | MQ8, MQ11. |

**Review log:** independent review pass: CN-D4.30 made Annelise custodian of the memorial stone; reworded so the stone-cutters carve and she only keeps the water. Earlier: first draft had Annelise keep a register of boats; cut (record custody). First draft let the boat drift to Widow's Step and be launched at once; revised so the boat stays in the garden's care, matching Act III's "Annelise brings the recovered offering boat." Board-setting reuses the rope-wear reading idea rather than Braid-gate ordering, to stay distinct from MQ11 Phase 2. The drift no longer "lead" the player to the boat; the boat is visible from the start.

---
## 6. VK — A Verse Kept Back

### 6.1 In one paragraph

Greyharrow will not open its winter boom until the thaw song is sung, and this year it cannot be sung. The song has four verses. The third has always been hummed. The Sayers say it once had words for the river's dead, dropped in the war out of shame, and want them back. The Coombes say it was always hummed, and that putting words to it at the water is an insult to the people it is hummed for. Each family says the other is dishonouring the dead. The player collects versions: the Sayers' song-book, where the words are written in a later hand; the Coombe elder's hum, which they will only give while working the ice-poles; Merrin's memory that it was hummed "before the bell went quiet"; Tamsin's version, which is rude about Sergeant Teague; and Nan Ferrin's listeners' tune at the Brookhollow water, which is the same melody. Nobody knows where it began. After MQ9, at the Listening Steps, the player hears water running over a carved channel make that same rising phrase, beside cut count-marks: four, held, four. It was a work count for opening water before it was anyone's mourning. That is context, not a translation, and it gives no version the whole past. Greyharrow sings, the boom opens, and the ice goes out.

**What the player should remember:** a melody they first heard by a fire in the True Line, running in stone behind a waterfall. **What they might want next:** Nan to sing it once more (MQ12).

### 6.2 Summary card

| Field | Value |
|---|---|
| Type | Memory/lore. Lattice L-S17; dossier §XI "The Riverwarden Lullaby" [CANON hook]; Nan's tune (True Line). |
| Unlock | MQ3 Completed. Steps S03 onward require **MQ9 Completed**. |
| Length | 30–40 minutes in total, split across the act break. |
| Combat | None. |
| Skills | None. The pole-work and boom pins are plain interactions. |
| NPCs | Sayer elder, Coombe elder (Greyharrow households [NEW], shared with SB); Merrin, Tamsin, Sergeant Teague; Nan Ferrin (True Line); Oriel (optional, D-8). |
| Choice | How the verse is performed (3 options). |
| Feeds | MQ11 after-hold hum and MQ12 Nan scene (Act III reads "completed VK"; §6.9). |

### 6.3 Places

| Place | Purpose | Environmental storytelling |
|---|---|---|
| **Greyharrow winter boom** | Hook; performance. | A chain of lashed logs across the side-branch dock mouth, holding back a raft of rotten ice and winter debris. Pin-posts at each end. Poles racked on the bank. Nobody touching them. |
| **Sayer house** | Version A. | A song-book on a shelf, its cover mended with sacking. If `SB_TO_FAMILIES`, the ringers' slate on the mantel. |
| **Coombe ice-poles** | Version B. | A side channel where the Coombe elder works floes off the jetty legs alone, in silence, until someone picks up a second pole. |
| **Bell tower foot** | Merrin, Tamsin (versions C, D). | As SB. |
| **Brookhollow docks edge** | Version E. | Nan sings only "at the water." The step where she stands is worn. |
| **The Listening Steps: the count channel** (P29, after MQ9) | Context. | A narrow carved channel off the main Steps where water drops over a run of shaped riffles. Cut into the lip beside it: groups of strokes, four, a long bar, four. Moss everywhere except on the strokes, which have been kept clear. |

**MAP VERIFICATION REQUIRED:** the count channel must sit inside the area MQ9 opens. If Act II places Oriel at the Steps after MQ9, VK-D6 is used; if not, the channel and its marks carry the beat alone.

### 6.4 Beats

**Beat 0 — The boom stays shut (`S00_offer`).** *Objective: Find out why the thaw song won't be sung.* At the boom: the quarrel (VK-D1).

**Beat 1 — Versions (`S01_versions`).** *Objective: Hear the thaw song's third verse, as many ways as you can.* Required: **A**, **B** and **E**. Optional: **C**, **D**. Any order.
- **A. The Sayers' book.** Inspect the song-book: verses one, two and four in one faded hand; the third verse in a different, later hand, words "for the ones the water kept." (VK-D2.)
- **B. The Coombe hum.** The elder will not talk; pick up a pole and **Work the floes** (3 interactions, 3 s each, pushing debris off the jetty legs). On the second push the elder starts to hum; on the third, VK-D3.
- **C. Merrin.** "Before the bell went quiet, we hummed it then too." (VK-D4a.) Quietly undermines the Sayers' claim that words were dropped in the war.
- **D. Tamsin.** The children's words, which rhyme Teague with "fatigue" (VK-D4b). Undermines everyone's solemnity.
- **E. Nan.** At Brookhollow, walk with Nan to the dock edge (she will not sing indoors). She hums it at the water: the listeners' tune. Same melody (VK-D5).

**Beat 2 — The trail goes quiet (`S02_wait`).** *Objective: Learn where the tune began.* Tracker sub-line: *(Nobody in the villages knows. The trail continues later.)* If MQ9 is already Completed, the sub-line is skipped.

**Beat 3 — The count channel (`S03_steps`).** *Objective: Listen at the Listening Steps.* Requires MQ9 Completed. Enter the count-channel volume. See §6.6. Inspect the strokes. Optional VK-D6 with Oriel.

**Beat 4 — Back to the boom (`S04_choose`).** *Objective: Bring what you heard back to Greyharrow.* The families, Merrin, Teague at the boom (VK-D7, the choice).

**Beat 5 — The thaw song (`S05_perform`).** *Objective: Open the boom.* The performance event (§6.7). Completed on the last pin.

### 6.5 Encounters

None. This is the slate's quiet quest (bible §7: combat in VK is absent by design). Ambient Silt Swimmers in the debris raft do not engage.

### 6.6 The strange moment: the count channel (presentation spec)

| Element | Spec |
|---|---|
| Trigger | Enter the count-channel volume (server event `verse.channel`), any time after MQ9. |
| Sound | Ordinary Steps ambience, then, as the player nears the riffles, the water's sound resolves into a rising phrase of four notes, a held note, four notes, repeating with the falling water. It is the listeners' tune's third-verse phrase, played by water, not voice. It is quiet; the player must be close. Moving away dissolves it back into water noise. |
| The marks | Strokes cut beside the channel: four, a long bar, four. Kept clear of moss. |
| What does not happen | No voice, no words, no figure, no light, no inscription in any language. |
| UI | None. |
| Camera | Player-controlled. |
| After | Strokes inspect: *"Four, held, four. Cut where a hand would rest while it counted. Someone kept these clear."* |
| What it means | The tune fits a count for working water. It does not say whose dead the verse is for, or whether words ever belonged to it. |

### 6.7 The performance (presentation spec)

| Element | Spec |
|---|---|
| Trigger | VK-D7 choice → `S05_perform`. |
| Crowd | Greyharrow at the boom: both families, Teague's militia on the poles, children, Merrin. If `SB_COMPLETE`, Tamsin pulls the silent bell rope to start (no sound; everyone starts singing on the swing). Else Merrin raises a hand. |
| Song | Verses one and two sung by everyone (full-crowd vocal loop). Verse three per the choice (§6.9). Verse four sung by everyone. |
| The player | At the east pin-post. Each verse, a **Pull the pin** interaction (3 s) is offered; pulling it during the verse frees one log section. No timing test: the song waits on the player if they are slow, and the crowd hums the last line again until they pull. |
| The ice | With the last pin, the boom swings open and the debris raft goes out down the side branch in one slow, grinding mass. The crowd cheers, stops singing, and argues about lunch. |
| Camera / UI | Player-controlled; no UI during the song. |
| After | The boom stays open (prop). At night, near reeds anywhere in Lowmark, the player may now hear the Riverwarden Lullaby (dossier §XI): a soft hum of the tune, no voice located, once per night at most, ambient only. |

### 6.8 Steps

| Step | Objective | Completes on | Required |
|---|---|---|---|
| `S00_offer` | Find out why the thaw song won't be sung. | VK-D1 end node | Yes |
| `S01_versions` | Hear the third verse, as many ways as you can. | A (inspect song-book + VK-D2), B (3 `work_floe` + VK-D3), E (VK-D5 end) | Yes |
| `S01c`, `S01d` | (Optional) Merrin's and Tamsin's versions. | VK-D4a / VK-D4b end | No |
| `S02_wait` | Learn where the tune began. | Auto-passes when MQ9 Completed | Yes |
| `S03_steps` | Listen at the Listening Steps. | Enter count-channel volume + inspect strokes | Yes |
| `S04_choose` | Bring what you heard back to Greyharrow. | VK-D7 choice node | Yes |
| `S05_perform` | Open the boom. | 4 `pull_pin` interactions → Completed | Yes |

### 6.9 Flags and choices

| Flag | Set by | Read by |
|---|---|---|
| `VK_HEARD_MERRIN`, `VK_HEARD_TAMSIN` | Optional versions | VK-D7 lines |
| `VK_PERF_BOTH` / `VK_PERF_COUNT` / `VK_PERF_HUM` | VK-D7 (exactly one) | Performance verse three; MQ12 Nan (request to Act III) |
| `VK_COMPLETE` | Completion | Lullaby ambience; Act III "completed VK" |

Reads `FK_NAN_TUNE` (Nan's opening variant) and `SB_COMPLETE`, `SB_TO_FAMILIES`.

| Option | Verse three becomes | Cost | MQ12 request (Act III owns wording) |
|---|---|---|---|
| **Both stand** — *"Sing the words over the hum."* | Sayers sing their words; Coombes hum beneath. | Neither family gets its whole way. Coombe elder: "Loud. But under it, it's ours." | Nan sings the verse with the Sayer words, humming between lines. |
| **The count** — *"Hum it as a count, the way it started. Say the words at the bell after."* | Everyone hums verse three as the pin count (four, held, four); the Sayer words are spoken at the tower after the boom opens. | The words leave the water. Sayer elder: "At the bell, then. Where they'll be heard." | Nan hums it as a count, tapping four, held, four on the rail. |
| **The hum alone** — *"Hum it. Keep the words in the book."* | Hum only, as Greyharrow always has. | The Sayers' words stay private. Sayer elder takes the book home. | Nan hums the verse; no words. |

No option is wrong; the Steps did not choose one.

### 6.10 Rewards

The boom opens (Greyharrow dock trade and side-route boats resume: ambient). The Lullaby ambience. Small payment from Teague's militia fund ("thaw wages, for the pin"). No lump quest XP.

### 6.11 Failure, recovery, co-op

No failure path. The pause at S02 is explicit in the tracker. If the player reaches MQ9 first, S02 passes on accept. Logout during the performance restarts it from verse one. Co-op: each player's performance is their own; partners present hear the crowd sing for whoever is on S05 (crowd audio is local to the performer; fallback: the performance is a world event that any partner's S05 completes on).

### 6.12 Dialogue

```
VK-D1 (the boom; both elders, Teague between them)
VK-D1.01 TEAGUE: "No song, no boom. No boom, no boats. No boats, I get the complaints."
VK-D1.02 SAYER ELDER: "There were words. They stopped singing them in the war, and we let them."
VK-D1.03 COOMBE ELDER: "There were never words. You hum it for them. You don't shout at the water."
VK-D1.04 [SB_COMPLETE] TEAGUE: "Didn't we just do this? With a wall?"
VK-D1.04 [else]        TEAGUE: "Every thaw. Every single thaw."
  > "Let me hear all the versions."                   → VK-D1.05
VK-D1.05 TEAGUE: "Please. Somebody. Before the ice rots the jetty."   {event: S00 complete} → end
```

```
VK-D2 (Sayer house, after inspecting the song-book)
VK-D2.01 SAYER ELDER: "My gran wrote that. After. She said she knew the words and nobody else would sing them."
  > "The third verse is in a different hand."         → VK-D2.02
VK-D2.02 SAYER ELDER: "Hers." (beat) "So the words came after. Doesn't make them wrong."   → end
```

```
VK-D3 (Coombe jetty, during the third floe push; the elder has been humming)
VK-D3.01 COOMBE ELDER: (stops humming) "You push like a Sayer."
VK-D3.02 COOMBE ELDER: "We hum it working. You don't put words on work. The work's the words."
  > "Who taught you?"                                 → VK-D3.03
VK-D3.03 COOMBE ELDER: "My mam. Hers. Nobody taught it. It was just there, like the river."   → end
```

```
VK-D4a (Merrin, at the rope)
VK-D4a.01 MERRIN: "We hummed it before the bell went quiet. I was small. I remember the hum."
VK-D4a.02 MERRIN: "Never heard words. Doesn't mean there weren't any. Means I never heard them."   {set VK_HEARD_MERRIN} → end

VK-D4b (Tamsin)
VK-D4b.01 TAMSIN: "There are words. We have them. 'Old Teague, old Teague, with his fatigue —'"
VK-D4b.02 TAMSIN: "There's more but you'd tell."   {set VK_HEARD_TAMSIN} → end
```

```
VK-D5 (Nan, Brookhollow; she walks to the dock edge first)
VK-D5.01 [FK_NAN_TUNE] NAN: "The listeners' tune again? You'll have me singing it in my sleep. Duchess already does."
VK-D5.01 [else]        NAN: "Not in here. At the water. My mam only sang it at the water."
VK-D5.02 NAN: (at the dock edge, hums the third-verse phrase; stops) "That one?"
  > "That's the thaw song's third verse. In Greyharrow."   → VK-D5.03
VK-D5.03 NAN: "Is it?" (beat) "Mam sang it before crossings. Never a word. Like counting, she said."
VK-D5.04 NAN: "Maybe it's everyone's. Maybe nobody's." (beat) "That's the best kind of tune."   → end
```

```
VK-D6 (optional; Oriel at the count channel, only if Act II places Oriel at the Steps after MQ9)  [D-8]
VK-D6.01 ORIEL: "You hum it." (beat) "Downriver they still hum it."
VK-D6.02 ORIEL: "It is a gate count. Four, hold, four. Hands on the paddles, so the water goes over together."
  > "In Greyharrow they sing it for their dead."         → VK-D6.03
VK-D6.03 ORIEL: "Then that is what it is for, there." (beat) "We only used it to open water."   → end
```

```
VK-D7 (the boom)
VK-D7.01 SAYER ELDER: "Well? Was it ours?"
  > "It was a count for opening water, long before anyone's dead."   → VK-D7.02
VK-D7.02 COOMBE ELDER: "Work. Told you."
VK-D7.03 SAYER ELDER: "And then people put their dead into it. My gran did. That happened too."
VK-D7.04 [VK_HEARD_MERRIN] MERRIN: "Hummed before the war. Worded after. Both true."
VK-D7.05 TEAGUE: "Lovely. Pick one. The jetty's going soft."
  > "Sing the words over the hum."                                      → VK-D7.10 {set VK_PERF_BOTH}
  > "Hum it as a count, the way it started. Say the words at the bell after."  → VK-D7.11 {set VK_PERF_COUNT}
  > "Hum it. Keep the words in the book."                               → VK-D7.12 {set VK_PERF_HUM}
VK-D7.10 COOMBE ELDER: "Loud." (beat) "But under it, it's ours."       → VK-D7.20
VK-D7.11 SAYER ELDER: "At the bell, then. Where they'll be heard."     → VK-D7.20
VK-D7.12 SAYER ELDER: (holds the book closer) "Then it stays in the house. Where she wrote it."   → VK-D7.20
VK-D7.20 TEAGUE: "Poles! East pin's yours. Pull when the verse turns."   {event: S04 complete}
```

Performance barks: TAMSIN (on the rope) "Now! Now now now!" · HOUSEHOLD (after) "Every thaw, the same song, and every thaw I cry. Pass the bread." · TEAGUE "Boom's open. Complaints are closed."

### 6.13 Mystery ledger

| Mystery | Author truth [PROPOSAL — DIRECTOR] | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The missing verse** | The melody began as a Riverwarden gate count; Lowmark folk kept it as a work hum; after the war some households set words to it for their dead. | Words were dropped in shame / there were never words. | Sayer book's later hand; Merrin's prewar hum; Nan's "like counting"; the count channel. | One family is right. | Who first set words; whose dead. | VK (context only). |
| **The Riverwarden Lullaby** | The same tune, heard near reeds at night. **Its source is never stated.** | For lost Riverwarden children. | The hum after VK. | It's ghosts; it's Sedge. | Everything. | None in v1. |

**Review log:** first draft had Oriel translate words; cut (context, never translation). The pause before MQ9 now has explicit tracker text so it cannot read as a bug. The performance was a rhythm test in draft; replaced with untimed pin pulls (no twitch mechanics).

---
## 7. FC — What the Flood Carried

### 7.1 In one paragraph

The flood went down off the Lark low field and left a raft of driftwood, hurdles and reed across the furrows, and in the middle of it a sealed tin case the size of a bread loaf. Hester Lark will not plant until somebody tells her what it is. Her father Amos says it is a wartime fire-tin and will take the barn with it. Her son Jem wants to keep it. The case sits on top of the raft in plain view of the gate, ticking in the sun from the first minute, while the player clears the raft around it (Woodcutting through one jammed log, hurdles to drag, vermin in the standing pools); then it sits alone on the bare furrow, still ticking. The ticking is the sun warming the metal. Nobody believes that until the player has looked: hand-soldered seam, no fuse or vent, no smell of tar, a dry shift inside like seed, a silt line in the lid groove that says it lay a long time under water still sealed, and a scratched household mark that matches no gatepost, tool or hurdle on this side of the field. That is all the evidence can say: it arrived, and it frightened people. Then the Larks decide. Opened, it holds a twist of dry seed, a note whose ink has run but for a few words, and an inner oilcloth packet sealed with wax that nobody will break. Unopened, it goes to the keepers or into the hedge-bank for whoever comes. Either way, Hester plants.

**What the player should remember:** a family standing well back from a ticking tin in a bare field. **What they might want next:** to come back and see whether the old seed comes up.

### 7.2 Summary card

| Field | Value |
|---|---|
| Type | Memory/lore. Lattice L-S12; dossier §XII "What the Flood Carried" (war remnants drift into Lowmark) [CANON hook]. |
| Unlock | MQ4 Completed. |
| Length | 20–30 minutes. |
| Combat | ~20%: standing-pool vermin; an optional boar. |
| Skills | Woodcutting (entry level, required), Melee; Smithing optional insight. |
| NPCs | Hester Lark (farmer) [NEW], Amos Lark (her father) [NEW], Jem Lark (her son, about nine) [NEW]; a road-patrol keeper (role). Names checked: no collisions. |
| Choice | What the household does with the case (3 options). |
| Cross-region callback | **Optional and removable** (§7.9). |

### 7.3 The place: the Lark low field (Heartlands field edge)

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Field gate** | Hook. | Seed sacks stacked unopened under a tarp. A plough left mid-furrow. The family on the gate, not in the field. |
| **B. The raft** | Clearing. | A tangle across six furrows: one jammed driftwood log, the Larks' own broken hurdles, a neighbour's hurdle with a different weave, reed mats, a cart wheel. The flood line on the hedge is chest high. |
| **C. Standing pools** | Danger. | Two pools left in the low corner, milky with silt. Movement under the surface. |
| **D. The case** | Discovery. | A soldered tin case, dented, a scratched mark on the lid, lodged on top of the raft where the gate can see it. Once the raft is cleared, it sits alone on bare earth. |
| **E. Hedge-bank niche** | Option. | An old stone-lined hollow in the bank where the Larks leave things for collection: a mended pail, a lost glove. |

### 7.4 Beats

**Beat 0 — Nobody's planting (`S00_offer`).** *Objective: Find out why the field isn't being planted.* FC-D1 at the gate.

**Beat 1 — Clear the raft (`S01_clear`).** *Objective: Clear the flood debris.* One jammed log (Woodcutting gather interaction at entry level, standard; a loaned hatchet from Amos if the player has none, returned at the end), then **Drag the hurdles** clear (3 carries to the hedge). Entering the low corner starts E1. The case is visible and ticking from the gate throughout; every hurdle dragged past it makes the Larks call out.

**Beat 2 — It ticks (`S02_case`).** *Objective: Look at the case.* The family will not come closer than the gate. The case ticks softly and irregularly. Five inspects; any four complete the step (texts in §7.11): **seam**, **weight** (lift and set down: a dry shift), **smell**, **silt line**, **mark**. Optional: the player with Smithing gets an added line on the seam. Optional: inspect the **ticking** (*"It ticks faster when the sun comes out from the cloud. Warm metal."*).

**Beat 3 — Whose mark (`S03_mark`).** *Objective: Look for the mark on the farm.* Compare the lid mark against three local marks: **gatepost**, **Amos's tool handles** at the gate, **the neighbour's hurdle** in the raft. None match. Completes on the third comparison. (The mark cannot be traced from here; the step proves only that it isn't local.)

**Beat 4 — The household decides (`S04_choose`).** *Objective: Tell the Larks what you found.* Carry the case to the gate (carry state; the family steps back as the player comes). FC-D3: the choice.

**Beat 5 — Planting (`S05_plant`).** *Objective: Help start the planting.* Lift the tarp, carry one seed sack to the field (carry), Hester sows the first furrow (ambient). If opened, Jem plants the tin's seed in a short row by the hedge. FC-D4. Completed.

### 7.5 Encounters

| Id | Enemies | Placement | Role | Telegraph | Solo target |
|---|---|---|---|---|---|
| **E1** | 2 × Silt Swimmer, 1 × River Leech | Standing pools in the low corner | Leashed to the pools | Ripple line (~0.8 s); leech rears (~1.2 s) | Required (the log lies across a pool). Short. |
| **E2** | 1 × Furrow Boar | Rooting in the reed mats | Wildlife, neutral until provoked; aggressive if the player drags a hurdle within 5 m | Paws and lowers head (~1.5 s) before charge | Optional. Hunting harvest afterwards (entry level). |

### 7.6 The strange moment: the tin (presentation spec)

FC's moment is unease, then something ordinary that feels like wonder.

| Element | Spec |
|---|---|
| Unease (from minute one) | From the player's arrival at the gate, the case ticks on top of the raft: small, uneven metallic clicks, faster when sun is on it (tie to cloud cover or a simple timer). The Larks flinch at each one. No music. The ticking is real physics; its inspect says so. |
| Opening (only if `FC_OPENED`) | Server event `flood_carried.open` on the **Prise the lid** interaction (4 s, at the gate). The lid comes off with a small breath of dry air. The family leans in. For a moment nobody speaks. Inside, everything is bone dry after its years in the water, and for one breath the air from it smells of **fresh bread**, warm, before it goes stale like any old tin. Nothing explains it and nothing comes of it. Amos: "Dry." That is the only line until the player inspects. |
| UI / camera | None; player-controlled. |
| What it means | Someone sealed this well. Nothing else. |

### 7.7 Steps

| Step | Objective | Completes on | Required |
|---|---|---|---|
| `S00_offer` | Find out why the field isn't being planted. | FC-D1 end node | Yes |
| `S01_clear` | Clear the flood debris. | 1 log-gather event + 3 hurdle deposits + E1 defeated | Yes |
| `S02_case` | Look at the case. | 4 of 5 inspects on the case | Yes |
| `S03_mark` | Look for the mark on the farm. | 3 comparison inspects | Yes |
| `S04_choose` | Tell the Larks what you found. | Carry deposit at gate + FC-D3 choice node | Yes |
| `S05_plant` | Help start the planting. | Seed-sack carry deposit → FC-D4 end → Completed | Yes |

### 7.8 Flags

| Flag | Set by | Read by |
|---|---|---|
| `FC_OPENED` / `FC_TO_KEEPERS` / `FC_TO_HEDGE` | FC-D3 (exactly one) | Props; barks |
| `FC_SEED_ROW` | `S05` if `FC_OPENED` | Hedge-row prop; later sprout state |
| `FC_SEAL_NOTED` | Inspect of the inner packet (only if opened) | **Removable callback hook** (§7.9). Nothing in v1 reads it. |
| `FC_COMPLETE` | Completion | Lark barks |

### 7.9 Choices, consequences and the removable callback

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Open it here** — *"Open it. Then you'll know."* | Seed twist, run-ink note (*"...keep these dry till the spring after..."*, no names), inner oilcloth packet with an unbroken wax seal. Jem plants the seed by the hedge; the packet goes on the Lark mantel, unopened. | Amos: "Now it's ours to worry about." | Hedge row: nothing after one return visit ("Beans are stubborn"); after MQ11 Completed, three thin shoots (prop). No meaning is assigned. |
| **Give it to the keepers** — *"Hand it to the keepers. It's a thing someone lost."* | The road-patrol keeper (passing at the gate on a schedule) logs it in the lost-goods book and takes it, unopened. | The Larks never learn what was inside. Jem sulks. | Keeper bark at Crestbridge: "Lost-goods has your tin. Nobody's asked." |
| **Set it aside** — *"Put it in the hedge-bank. Whoever it belongs to can find it."* | Into the niche, unopened. Amos marks the niche stone with the same scratched mark. | It may never be claimed. | The niche keeps the tin (prop). Hester: "If they come, they'll see their mark." |

In all three, planting starts. The household decides; the player only reports what the case shows.

**Removable cross-region callback [PROPOSAL — DIRECTOR].** The wax seal on the inner packet carries a pressed mark (art: a simple stamped device, deliberately unassigned to any region). Inspect: *"A wax seal, pressed with a mark nobody here knows. The Larks won't break it."* It sets `FC_SEAL_NOTED`. Per lattice L-S12 and the framework's long-delay rules:
- **Owner:** a later region's independent archive or household record must identify the device. Until that owner exists, nothing reads the flag.
- **Never sole proof:** a later scene must restate the context and treat the seal as corroboration only.
- **Removal:** delete the inner packet prop, its inspect and `FC_SEAL_NOTED`. The opened tin then holds only the seed and the note. No step, choice, line or reward changes.
- **No route is inferred.** Nothing here says where the case came from or which way the water ran.

### 7.10 Rewards

Planting resumes (field prop changes to sown). Small payment from Hester "in seed-money, which is to say not much." Amos's hatchet loan, if taken, is returned (not a reward). Action XP: Woodcutting, Melee, optional Hunting. No lump quest XP.

### 7.11 Inspects and dialogue

| Object | Text | Condition |
|---|---|---|
| Seam | "Soldered by hand. The bead wanders. Somebody did this at a kitchen table." | — |
| Seam (Smithing) | "Tin and lead, cheap and careful. No fuse port, no vent. It was made to keep water out, not to do anything." | Smithing skill ≥ entry |
| Weight | "Lighter than it looks. Something inside shifts like dry seed. Nothing sloshes." | — |
| Smell | "Mud. River. No tar, no oil, nothing sharp." | — |
| Silt line | "Fine silt packed into the lid groove, all the way round. It lay under still water a long time, sealed." | — |
| Mark | "A household mark scratched into the lid: a ring with a bar through it." | — |
| Gatepost / tools / neighbour's hurdle | "The Lark mark is a forked line." / "Amos's handles: the forked line again." / "The neighbour's weave, and their mark: three notches. Not this." | — |
| Note (if opened) | "Paper, the ink run to grey. A few words hold: *keep these dry till the spring after.* No name. No date." | `FC_OPENED` |

```
FC-D1 (the field gate)
FC-D1.01 HESTER: "Seed's ready. Field's ready. That isn't."   (nods at the raft and the glint in it)
FC-D1.02 AMOS: "Fire-tin. Saw one go up in a barn. You don't touch fire-tins."
FC-D1.03 JEM: "It's treasure. Obviously."
FC-D1.04 HESTER: "Clear that lot and tell me what it is. Then I'll decide if I'm planting round it."
  > "I'll take a look."                         → end {event: S00 complete}
  > [no cutting tool] "I've no blade."          → FC-D1.05
FC-D1.05 AMOS: (hands over a hatchet) "Mine. I want it back. Sharp."   → end {event: S00 complete}
```

```
FC-D2 (barks while the case ticks)
JEM:   "It's ticking! Mam, it's ticking!"
AMOS:  "Told you. Told you."
HESTER:"Stand back from it and look at it. Both. At the same time, if you can."
```

```
FC-D3 (at the gate; the player sets the case down; the family takes one step back, then one forward)
FC-D3.01 HESTER: "Well?"
  > "It's hand-soldered. No fuse, no vent. It ticks because the sun's on it."   → FC-D3.02
FC-D3.02 AMOS: "Ticks because the sun's on it." (beat) "I knew that."
FC-D3.03 HESTER: "Whose is it?"
  > "Not anyone's on this farm. The mark doesn't match. That's all I can tell."   → FC-D3.04
FC-D3.04 JEM: "So it's ours."
FC-D3.05 HESTER: "It isn't anybody's yet." (to the player) "What would you do?"
  > "Open it. Then you'll know."                                     → FC-D3.10
  > "Hand it to the keepers. It's a thing someone lost."             → FC-D3.20
  > "Put it in the hedge-bank. Whoever it belongs to can find it."   → FC-D3.30
FC-D3.10 AMOS: (prises the lid himself, slowly, at arm's length) ...
       {event: flood_carried.open → §7.6}
FC-D3.11 AMOS: "Dry."
FC-D3.12 JEM: "It's seeds. It's just seeds." (beat) "Can I plant them?"
FC-D3.13 HESTER: "By the hedge. Not in my good furrow."  {set FC_OPENED} → end
FC-D3.20 HESTER: "Keeper comes past at noon. He can write it in his book."
FC-D3.21 JEM: "We'll never know." (beat) "That's the worst."   {set FC_TO_KEEPERS} → end
FC-D3.30 AMOS: "I'll scratch their mark on the niche stone. So they know it's waiting."
FC-D3.31 HESTER: "Then it's not ours to worry about. Good."   {set FC_TO_HEDGE} → end
       {all: event S04 complete}
```

```
FC-D4 (after the first furrow)
FC-D4.01 HESTER: "First furrow. Late, but in."
FC-D4.02 [FC_OPENED] JEM: (patting the hedge row flat) "They'll come up. They've been waiting ages."
FC-D4.02 [else]      AMOS: "Well. It frightened us for a day. Plenty of things do worse."
FC-D4.03 HESTER: "River keep you. Come back at harvest and see if I was right to bother."
       {small payment; event: FC-D4 end → quest Completed}
```

### 7.12 Failure, recovery, co-op, integration

Dropped carry: the case returns to where it lay. Death: respawn at the field gate. Logout: steps persist. Co-op: per-player case, raft and field props; shared vermin. Fallback without per-player props: the raft stays cleared world-wide after the first player; later players' S01 completes on entering the cleared field, and the case is a per-player interactable at the gate. **Needs:** carry state; a scheduled role NPC (road keeper) at the gate; field-state props; a ticking audio loop tied to time or weather.

### 7.13 Mystery ledger

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The tin case** | A household's sealed seed store from the war years, lost in some flood and carried here in this one. Origin **deliberately unselected**. | Fire-tin; treasure. | Seam, weight, smell, silt line, unmatched mark. | It's a weapon; it came from a specific region (nothing shows that). | Who sealed it; where; the wax mark. | Optional later archive (removable; §7.9). |

**Review log:** first draft let the mark match a vanished Lowmark household; cut, because that would invent a history and imply a river route. The callback is isolated to one prop and one flag that nothing reads. The ticking was originally supernatural; made ordinary so the evidence teaches looking, not fear. Independent review pass: the opening repeated the woodcut-a-jam pattern of BW and UR and its unease came late, so the case is now visible and ticking from the gate at once, the raft is one log plus hurdles, and the opened tin smells of fresh bread for one unexplained breath.

---

## 8. Micro-events ME01–ME10

Each micro-event follows the discovery framework's optional-discovery card: a place, a visible invitation, one ordinary interaction, an immediate meaning, what it cannot prove. None is required for anything. Flags use the `ME0n_` prefix and are read only by the micro-event itself unless stated. No quest items, no rewards beyond a line, a smile or the odd food item from the item pass.

### ME01 — Safe-bank game

| Field | Spec |
|---|---|
| Trigger | After MQ1 Completed. Daytime, Whisperflow shallows below the landing. Enter a 20 m volume. |
| What the player sees | Three children racing ankle-deep along the stretch between two of the grey marker posts, and nowhere else. A stick lies across the water at each end as a line. If `BW` is Completed, Tamsin is with them (down on a market cart), refereeing with the measuring cord. |
| Interaction | Watch (stand within 8 m for 15 s) → they stop and appeal to the player to settle a rule. Two options. |
| Lines | KID A: "You have to touch the post before you turn. Everyone knows." · KID B: "You have to touch the post *and* say 'notch'. Because of the shoe." · KID A: "The shoe was ages ago." · KID B: "The shoe is *why*." · *(Tamsin variant: "I've measured it. The shoe went in there. That's out of bounds forever.")* |
| Options | > "Touch the post and say 'notch'." → KID B: "Ha." · > "Just touch the post." → KID A: "Ha." Either: KID C: "Can we go again?" |
| Persistence | `ME01_RULE` = notch / post. On later visits the winning rule is shouted in their game bark. |
| Repeatable | Settle once; the game loops ambiently thereafter. |
| Cannot prove | Anything about routes. It shows flood knowledge as play. |

### ME02 — Dock lunch tally

| Field | Spec |
|---|---|
| Trigger | Brookhollow docks, midday window, after MQ1. Rain-shortened shift (if weather exists; else always at midday). |
| What the player sees | Four dock workers under a beam out of the wet, arguing. Knife marks in groups on the beam: who forgot food, by season. One worker has no food. |
| Interaction | Give any food item to the worker without (item-given), **or** inspect the beam and **Add a mark** (2 s). |
| Lines | WORKER 1: "Third time this month." · WORKER 2: "It's on the beam. The beam doesn't lie." · WORKER 3: "The beam lies all the time. Ossie cuts extra marks for me." · *(on food given)* WORKER WITHOUT: "Oh. I'll — the beam's going to say I owe you now." · *(on mark added)* WORKER 1: "That's a stranger's mark. Now we owe the beam a stranger." |
| Persistence | `ME02_SHARED` / `ME02_MARKED`. A small extra mark appears on the beam (marked) or the worker nods to the player in later barks (shared). |
| Repeatable | Once per character; the argument loops ambiently. |
| Cannot prove | Nothing. The marks are not a cipher or ledger (framework). |

### ME03 — The old knot

| Field | Spec |
|---|---|
| Trigger | Ashen Flats work edge, dusk window, after MQ1. Joric Fen [CANON ANCHOR] mending a net beside a young worker (role). |
| What the player sees | The young worker ties a net knot. Joric watches, then without a word unpicks it and re-ties it a different, older way. |
| Interaction | **Wait.** If the player stands within 6 m without talking to either of them for 20 s, Joric speaks once. If the player talks first, Joric nods and goes back to work (no line; the moment is gone until the next dusk). |
| Lines | JORIC: (to the young worker, not the player) "My hands learned that one before I did. Pull till it bites. Then once more." · YOUNG WORKER: (tries; it holds) "...Oh." |
| Persistence | `ME03_SEEN`. Afterwards, the young worker's nets on the Flats use the older knot (inspect: *"An old knot. Pulled till it bit, then once more."*). |
| Repeatable | Once. |
| Cannot prove | Anything about Joric's past. Canon guard: no kinship, event or loss is mentioned. |

### ME04 — Offering sweep

| Field | Spec |
|---|---|
| Trigger | Ashenstead watergarden, before rain (weather state; fallback: a fixed afternoon window), after MQ3. |
| What the player sees | Annelise Reed [CANON ANCHOR] and a second caretaker (role) clearing spoiled offerings into a basket: browned flower crowns, a sodden ribbon, a bread crust. |
| Interaction | Help (**Clear an offering**, 2 s, up to 3 offerings at the pool rim), or watch. |
| Lines | ANNELISE: (to the water, lifting a crown) "You've done your job. Off you go." · CARETAKER: "That one was fresh yesterday." · ANNELISE: "Yesterday it was." · *(if helped)* ANNELISE: (to the water, of the player) "Careful hands. Good." · *(if `CN_COMPLETE`)* ANNELISE: "The bottom pool's moving now. They don't rot down there any more." |
| Persistence | `ME04_HELPED`. None visible: the pool is simply clear when the rain comes. |
| Repeatable | Every rain window (ambient); the helped line plays once. |
| Cannot prove | No name or death is revealed (lattice M04). |

### ME05 — Three water cups

| Field | Spec |
|---|---|
| Trigger | A Heartlands farmhouse threshold (the Lark farm, any time after MQ1; independent of FC). Enter the doorway volume. |
| What the player sees | Three cups set out on the step before a tense family talk inside (overheard: who gets the second cow): one chipped clay, one wooden, one riverglass. |
| Interaction | Drink one (interaction on any cup). |
| Lines | *(clay)* AMOS: "The chipped one. That's the guest cup. Chipped so you know it's not ours." · *(wooden)* HESTER: "Wood. Doesn't break when someone slams it down. Which someone will." · *(glass)* JEM: "The glass one. So you can see there's only water in it. Gran said." · then, from inside: "Right. The cow." |
| Persistence | `ME05_CUP` = clay/wood/glass. Each later visit, the cup the player chose is set first. |
| Repeatable | Once; the cups stay set out. |
| Cannot prove | It's a courtesy, not a test (lattice M05). All cups are right. |

### ME06 — The reed dare

| Field | Spec |
|---|---|
| Trigger | Circle of Unburnt Reeds (P26), dusk window, after MQ3. |
| What the player sees | Child-height footprints stop at a warning stake ("KEEP OUT — THIS MEANS YOU, PIP" in two adult hands). One set goes on, into the ring. A child (Pip, role) is sitting inside the circle, arms folded. Two others at the stake. The reeds show careful cutting at the edge: the ring is maintained, not wild. |
| Interaction | Talk. The player cannot pull or carry the child out; only talk. Three options; any one works, eventually. |
| Lines | PIP: "I'm not coming out. I'm being brave." · > "Brave's done. Come and tell them about it." → PIP: "...It *was* brave." (comes out) · > "What's it like in there?" → PIP: "Quiet. Too quiet. I'm coming out because I want to, not because you said." (comes out) · > "Your mam's coming." → PIP: "She's *not*." (beat) "Is she?" (comes out) · then KID AT STAKE: "You were in for ages." PIP: "Ages and ages." |
| Persistence | `ME06_DONE`. On later dusks, footprints stop at the stake; none go in. |
| Repeatable | Once. |
| Cannot prove | Why the reeds never burned stays unexplained; not part of MQ8's use of the circle. |

### ME07 — The sweet well

| Field | Spec |
|---|---|
| Trigger | A Heartlands farm well (the Dunnock farm yard pump-well, independent of WD; available after MQ1). |
| What the player sees | A bucket on a rope, a cup chained to the windlass. A child (Col Dunnock) watching to see if the player will try it. |
| Interaction | **Drink** (cup), then optional **Inspect** the well. |
| Lines | *(drink)* — inspect text: *"Faintly sweet. Not unpleasant."* · COL: "It's always sweet. Mam says it's the clay. Gran said the old orchard's roots go down there. I think somebody dropped honey in it once and it never came out." · *(inspect well)* *"Old stone, good water. The rope's newer than the windlass."* · RHODA (if near): "It's the clay." |
| Persistence | `ME07_DRUNK`. Col's later bark: "Sweet today?" |
| Repeatable | Drink any time; lines once. |
| Cannot prove | Which explanation is right. None is. This is not Ember-Well (whose water tastes sharper to the grieving); the contrast is deliberate and never pointed out. |

### ME08 — The lagging pool

| Field | Spec |
|---|---|
| Trigger | A still pool in a Whisperflow acoustic dead spot (dossier §IV.1), upstream of the True Line footing; after MQ1. Enter the pool-edge volume. |
| What the player sees | A small, round, perfectly still pool among reeds. The river is audibly quieter here. |
| Interaction | Look. If the player stands still at the edge for 5 s and then moves, their reflection follows a breath late (client-side, local player only). Nothing else happens. Leaving ends it. |
| Lines | None. No inspect text describes the lag. Pool inspect: *"Still water. Very quiet here."* If `TL_TOVIN_TRUSTED`, Tovin Pell sits on a stone nearby on some visits, sketching. TOVIN (only if spoken to): "I come here to draw the bend." He does not name it, ask about it or explain it (canon). |
| Persistence | None. |
| Repeatable | Always. |
| Cannot prove | Anything. It is a quiet echo of the True Line's lag and MQ6's mill pond; nothing builds on it. |

### ME09 — The mantle at dawn

| Field | Spec |
|---|---|
| Trigger | The Mantle Shrine (P24), dawn window, **after MQ8 Completed**. First dawn approach within 30 m. |
| What the player sees | Mist lying over the shrine stone like a cloak over a chair. As the player comes within 10 m, it lifts and thins away over ~6 s, as mist does with the sun. Fresh softmoss pressed onto the stone, still damp. Nobody there. |
| Interaction | Inspect the stone. Then **Leave something** (give any small food or common item: item-given to the shrine) or leave nothing. |
| Lines | Stone inspect: *"Fresh softmoss, pressed down by a hand. Still damp."* No NPC lines. If the player leaves something, on the next dawn visit it is gone and the softmoss is fresh again. If they leave nothing, nothing changes. |
| Persistence | `ME09_LEFT`. |
| Repeatable | The mist plays on every dawn approach; the offering exchange once. |
| Cannot prove | Who presses the moss. Players who know Sedge will think so; nothing confirms it `[D-7]`. |

### ME10 — Walk a leg with the Watchers

| Field | Spec |
|---|---|
| Trigger | Watchers' Lantern Post (P21), dusk window, after MQ3. Two Watchers (role; one older, one new) prepare to walk to Widow's Step. |
| What the player sees | Lanterns lit, banner-thistle bundles, rope, the patrol book open on a barrel. |
| Interaction | Talk → **Carry a lantern** (carry state, lights the path) → walk with them (escort-style; they wait if the player lags). At a heavy bend halfway, one optional drift forms; the player may disperse it or let the Watchers smoke it back (they light banner-thistle; it sinks). At Widow's Step the older Watcher writes in the book; the player may read the entry. |
| Lines | OLD WATCHER: "Walk. Watch. Write it down. Mostly walk." · NEW WATCHER: "Do we always go this slowly?" · OLD WATCHER: "Only when we want to get there." · *(at the bend)* OLD WATCHER: "Heavy. Smoke, not steel, if you can help it." · *(book entry, inspect)* *"Bend below the Post. Heavy at dusk. One drift, smoked. Lantern held. Three walking."* · *(after MQ11, `LM_FEN_ENDING` tend/shared)* OLD WATCHER: "Tended bend now. We still walk it. That's the deal." · *(after MQ11, seal)* "Nothing heavy past the boundary. We walk to the boundary and back." |
| Persistence | `ME10_WALKED`. The player's "three walking" entry stays in the book (inspectable). |
| Repeatable | Repeatable at any dusk; the book entry once. |
| Cannot prove | Combat and smoke here identify nothing. It shows how Ansel's book (MQ3) is made. |

---

## 9. File-level integration summary

| Need | Used by | Notes / fallback |
|---|---|---|
| Time-of-day windows and wait interactions | TB, WD, CN, VK (none), ME03/04/06/09/10 | One contract shared with MQ4 keep-watch (§0.4). |
| Carry state | UC paddle, TB fruit, CN boat, FC case and sack, ME10 lantern, WD hurdles | True Line fallback (lift-and-stack interactions). |
| Per-player props | All seven | Each package lists its shared-world fallback. |
| Drift-site state | WD (farmhouse cellar), CN (watergarden outlet) | Bible §9.2 site ids. |
| Observation volume with per-player timer | UC | Load-bearing level-art requirement (§2.3). |
| Planar reflection on one basin | UC | Fallback: state-driven pre-baked reflection. |
| Dream presentation layer | TB | Fallback: 60 m ring. |
| Agility triggers | SB, UC, TB | All have walkable fallbacks. |
| View-dependent local effects | SB river ring, ME08 lag | Same pattern as True Line far-bank figure. |

## 10. Flags other packages read

| Flag | Owner | Reader |
|---|---|---|
| `CN_COMPLETE`, `CN_FORM_WATCH` / `CN_FORM_CARRY` | CN | Act III MQ11 Annelise Tend argument and launched-boat prop (suggested lines in §5.9). `CN_FORM_*` is a request: nothing breaks if unread. |
| `VK_COMPLETE`, `VK_PERF_BOTH` / `VK_PERF_COUNT` / `VK_PERF_HUM` | VK | Act III MQ11 after-hold hum; **MQ12 Nan verse must be keyed to the performance flag**, never to `VK_COMPLETE` alone: `VK_PERF_BOTH` = she sings the Sayer words over the hum; `VK_PERF_COUNT` = she hums it as a count, tapping four, held, four; `VK_PERF_HUM` = hum only, no words (§6.9). |
| `UC_COMPLETE` | UC | Optional Act II MQ9 flow-table inspect (§2.11; request). |
| `WD_QUIETED`, `WD_FLAP` / `WD_BRICKED` | WD | Drift-site state for the farmhouse cellar (stays quieted in every fen ending); Dunnock barks. |
| *(read)* MQ5 Completed | Act II | WD drain dressing (§4.3): the treatment-boundary stencils and props appear only after MQ5. |
| *(read)* `LM_SEDGE_TRUST`, MQ9 Completed | Act II | UC-D5; VK `S03` onward. |
| `SB_COMPLETE`, `SB_TO_FAMILIES` | SB | VK (this file). |
| `FK_NAN_TUNE` | FK (Work and Skills) | VK-D5 (read here). |
| `FC_SEAL_NOTED` | FC | No v1 reader (removable callback). |

## 11. Independent review pass

Applied the independent side-content review and Director rulings 3 and 6. Entries are in each package's review log.

| Finding | Action |
|---|---|
| UC camera honesty (major) | **Applied.** Ruling 6: the channel is roofed and screened. The server rule is "no player inside the observation volume watching the channel". The binding client rule is that the channel renders still whenever it is directly in a camera view. The climb is seen only in the basin reflection from the seat (with a soft camera limit). The volume edge is marked with flagged stone, and the brow does not fade. |
| WD repeats NT's lantern loop (major) | **Applied.** The defence is now a listening loop: the creak tells which outlet rises, and the player holds that lid. The unexplained second creak matches no outlet. |
| WD spoils MQ5 between MQ4 and MQ5 (major) | **Applied.** WD keeps its MQ4 unlock. The drain shows its treatment-boundary dressing only after MQ5 Completed. |
| Name collision (major) | **Applied.** Ruling 3: the Hobb household is renamed **Dunnock** (Rhoda Dunnock, Col Dunnock), including in ME07. It has no hits in any `04_CONTENT_PRODUCTION` file. |
| VK verse in MQ12 (major, Act III side) | The MQ12 keying is stated in §10. The Act III edit is owned by the main-act designer. |
| CN-D4.30 record custody (major) | **Applied.** The stone-cutters carve; Annelise keeps the water. |
| ME08 Tovin seeking the anomaly (minor) | **Applied** the line: "I come here to draw the bend." The location stays at Whisperflow, because Tovin appears there in MQ1 (`TL_TOVIN_TRUSTED`). |
| UC E1 / WD E3 tier labels (minor) | **Applied.** Both are now Milestone 1. |
| VK gate stated three ways (minor) | **Applied.** Every mention now reads "S03 onward". |
| Tamsin pronoun (minor) | **Applied.** ME01 is now pronoun-neutral, matching BW (note in the Work and Skills BW.11 log). The bible's "her" is an open item for the bible owner. |
| FC repetition and weak strange moment (minor) | **Applied.** The case is visible and ticking from minute one, the raft is one log plus hurdles, and the opened tin gives a fresh-bread breath. |
| TB goblins → Mud Pipers (minor) | **Rejected.** Mud Pipers are first seen in MQ7, and TB unlocks after MQ5, so the swap would take MQ7's family introduction. |
| Sedge cameo count (minor, bible D-7) | **No change here.** UC-D1.04 keeps Sedge's plain self-introduction. The bible owner should update D-7/§5.3 to "first met in MQ5 or UC". |
| Flags with no reader (minor) | Unread promises are marked "(request)" in §10. |

No flag renames in this file. Renamed: Hobb farm/household → Dunnock (Rhoda Hobb → Rhoda Dunnock, Col Hobb → Col Dunnock).
