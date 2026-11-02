# Lowmark Main Questline, Act I: Short Measure, Heavy Water, The Night Flush

**Status:** Authored production content for Creative Director milestone review. This package implements Lowmark main quests 2–4 (bible §6, §6.1), which carry Act I from the end of *The True Line* to the Act I turn. It follows the format of `Caelmor_Lowmark_Quest_The_True_Line.md`. Everything marked **[NEW]** is authored and not canon until the Director promotes it. Everything marked **[PROPOSAL — DIRECTOR]** rests on an open bible §3 decision. **[CANON]** items come from Phase 1 or the reconciled `LORE/` files. No schema, production JSON or C# is created here.

**Controlling document:** `04_CONTENT_PRODUCTION/Quests/Caelmor_Lowmark_v1_Narrative_Production_Bible.md`. Its §6 table and §6.1 briefs are binding and are implemented as written.

**Companion file:** `04_CONTENT_PRODUCTION/Dialogue & Narrative/Caelmor_Lowmark_Main_Act_I_Dialogue.md`. It holds cast notes, every dialogue node referenced here (`SM-`, `HW-`, `NF-` prefixes), inspect texts, document texts and barks.

---

## Act I header

### What Act I does

*The True Line* showed the player that someone moved a post. Act I's job is to turn "someone" into a working method the player has seen with their own eyes, without giving the player a name they could carry to court yet.

| Quest | The player learns | By doing |
|---|---|---|
| MQ2 **Short Measure** | Grain is going missing on purpose, and it is going by river. A Board seal is on the order. | Going into Lowmark's first real dungeon and finding a chute that goblins did not dig. |
| MQ3 **Heavy Water** | The strange water is real, it comes back when you fight it, and it goes wrong on a schedule. | Fixing three ordinary problems and noticing the one thing that survives all three. |
| MQ4 **The Night Flush** | The schedule is a machine. People are running it. Stopping them does not stop the water. | Watching, chasing, storming, and closing the Hollow Lock with their own hands. |

**Act I turn (Main Arc movement 4):** a human wrong and a supernatural condition coexist. Exposing one does not make the other fictional. The last thing the player sees in Act I is the fen's fog sitting thicker than ever after they have "won."

### Dependencies on *The True Line*

| TL flag | Read by | Effect |
|---|---|---|
| `TL_EVIDENCE_KEEPERS` / `_RIVERFOLK` / `_PLAYER` (stored region-wide as `LM_TL_EVIDENCE` keepers / riverfolk / player) | MQ2 lead-in, `SM-D1` opening, `SM-D6` | Three different ways into Crestbridge (§A6 Beat 0). |
| `TL_STONE_PUBLIC` / `TL_STONE_KEPT` | MQ2 depot stone inspect, `SM-D6.30` | The depot stone is compared with the Whisperflow stone in public or in private terms. |
| `TL_TOVIN_TRUSTED` | None in Act I | Reserved for MQ6. Tovin does not appear in Act I (bible §5.1). |
| *The True Line* Completed | MQ2 availability | MQ2 is offered only after TL completes. |

### Region flags (bible §9.1 only)

| Flag | Act I role |
|---|---|
| `LM_TL_EVIDENCE` | **Read** (MQ2). Act I never writes it. |
| `LM_GRAIN_ROUTE` = escort / hold / split | **Set** by MQ2 Choice. Read later by MQ10 terms and MQ12's far-bank scene. |
| `LM_LOCK_STATE` = smashed / chained | **Set** by MQ4 Choice. Read later by MQ6 crew-route line and MQ10 chip. |

Act I invents no other `LM_` flag. Quest-local flags use `SM_`, `HW_`, `NF_`. Those read by later packages are listed in each quest's flags table under "Read by (later packages)".

### Drift-site changes in Act I (bible §9.2)

| Site | Before Act I | After |
|---|---|---|
| Orchard pool (MQ3) | Active (dusk) | **Quieted** by MQ3. This is the first quieted site in the game. |
| Flats ditch (MQ3) | Active (flush nights only) | Stays active. It runs right again only when Act II/III changes its conditions. |
| Widow's Step (MQ3, MQ11) | Active (dusk, flush nights) | Stays active. Its fix belongs to MQ11. |
| Bramblelock pool (MQ4) | Active (flush nights) | **Quieted** at MQ4 dawn. The Lock no longer drags water through it. |
| Stillwater deep pools | Active | **Visibly worse** at MQ4 dawn (presentation only; spawns are MQ11's business). |

### Quest-item budget (bible §11.6: ≤2 per act)

| Item | Quest | Fate |
|---|---|---|
| `SM_requisition` (the dropped Board requisition slip) | MQ2 | Kept by the player to MQ10 (evidence chip). Not droppable, not sellable. |
| `NF_bill_of_lading` (Board-sealed bill to an outside buyer) | MQ4 | Kept by the player to MQ10 (evidence chip). Not droppable, not sellable. |

**Total: 2.** Everything else in Act I is a carry-state object (sacks, the smoke-pot, a pre-notched post), an inspectable world object (Ansel's patrol book, the depot stone, the Lock's gear), or knowledge carried in flags.

### Structure check against the bible §6 core verbs

| Quest | Primary verb | Distinct from |
|---|---|---|
| TL | investigate a bank, repair a marker | — |
| SM | **delve** a dungeon; count | The only Act I dungeon. Interior, vertical, trap-driven. |
| HW | **investigate three sites** in any order; first Wraith fight; rescue | Open-world, three short self-contained problems, then a synthesis the player does. No dungeon, no chase. |
| NF | **watch, pursue, assault** | Night, linear, momentum. The only chase and the only human-enemy assault in Act I. |

No two quests share a set piece. Combat changes family across the act: goblins (SM) → drift and hounds (HW) → humans, with drift as weather (NF).

### Unlocks across Act I (bible §7)

After MQ2: *Bark for the Pits*, *Honest Steel*, *Night Bridge*, *Night Ferry*. After MQ3: *Unreplanted*, *The Uphill Canal*, *Fen Watch*, *Old Lantern*, *The Candle Rule*, *A Verse Kept Back*. After MQ4: *Under the Lamb*, *The Whispering Door*, *What the Flood Carried*; MQ5.

---
---

# Part A — MQ2 Short Measure (`SM`)

## A1. The quest in one paragraph

Crestbridge's grain factor, Corvin Tath, keeps two tallies, and both say the same thing: 120 sacks went out of his granary under the Provision Board's emergency order, and Wynn Tarrow's cart carried 40 of them to the far bank. He thinks he is being robbed through the old hill passage behind the granary, where Field Goblins have broken in. He is half right. The player goes down through the passage into the **Hill Depot**, a wartime emergency store cut into the hill that has become a goblin warren. Inside are low tunnels, traps built out of rakes, scythes and harrows, and the **Sack-King**, a goblin who has made himself a throne of Crestbridge relief grain. Under the throne there are about a dozen sacks, and that is all. Past the warren the depot's old river chute has fresh rope burns, new tallow on the pulley, hobnailed boot prints that are not goblin, and a dropped requisition slip under a Board seal: *lower at the hill chute, eighty measures*. People sent the grain down to the river at night. Set into the chute gallery wall is a carved stone the player has seen before, a **Marking Stone** salvaged into the masonry, with a dark damp line in a dry room that stops exactly at its notch. Back in the granary yard the Keeper-Captain is signing for the next draw, and a Provisioner is thanking him for it. Nobody can accuse a Board on a slip. But Corvin now controls the sacks in his bays, and the player decides where they go.

**What the player should remember:** the Sack-King's grain throne, and the wet line on a stone in a dry wall. **What the player should want next:** where the river took the grain, and why that stencil on the gallery wall said RELIEF CUT.

## A2. Selection record

| Candidate | Verdict |
|---|---|
| **A. The audit.** Reconcile Corvin's tallies against Board copies in Crest Hall. | Rejected. This is the administrative pattern the audit flagged. The bible requires a dungeon. |
| **B. Goblins did it.** The depot is a straight clear-out and the grain comes back. | Rejected. It spends the dungeon on a wrong answer and teaches nothing. Kept as the *plausible wrong reading* that the dungeon itself overturns. |
| **C. The delve that changes its own question** (selected). The player enters to solve a goblin problem. The warren's own contents (only a dozen sacks) and the chute beyond it change the question to "who lowered the rest?" | **Selected.** The investigation happens with the player's feet, the strange moment sits inside the dungeon, and the human evidence is an object found on a floor, never a combat drop. |

## A3. Canon grounding

| Element used | Source | Status |
|---|---|---|
| Corvin Tath: grain factor, speaks in numbers, duplicate tallies, refuses Emberholt priority contracts | Lowmark anchors §II | [CANON] |
| Aldric Fenmere: acting Steward, polite, reserved, keeps ledgers older than the war | Lowmark anchors §I | [CANON] |
| Emergency depots carved into low hills, later goblin and bandit haunts | Lowmark dossier §II | [CANON] |
| Field Goblins: nest in old supply pits, broken farm tools, scrap armour | Lowmark dossier §VIII | [CANON] |
| Crestbridge granaries, toll offices, Keepers' records | Lowmark dossier §III, §IV.4 | [CANON] |
| Flood Calendar Stones | Lowmark dossier §XI | [CANON] hook |
| The Hill Depot, the Provision Board, House Marrick, Hesketh, the Relief Cut, salvaged Marking Stones | Bible §2, §4.2 P07, §5.3 | [NEW] / [PROPOSAL — DIRECTOR] |

## A4. Quest summary card

| Field | Value |
|---|---|
| Working title | **Short Measure** |
| Suggested content id | `lowmark.main.02_short_measure` |
| Arc position | Act I, Main Arc movement 2 ("The cost of moving grain") |
| Prerequisite | *The True Line* Completed |
| Offer | Auto-offered on entering the Crestbridge granary yard (Beat 0 variants). |
| Solo / co-op | Solo-clearable. Co-op players run independent instances and share world creatures. |
| Target length | 30–40 minutes first time; about 15 on replay |
| Combat share | ~35% (the dungeon) |
| Dialogue share | ~15% |
| Exploration, traps, counting, choice | ~50% |
| Skills touched | Melee (required); Woodcutting (optional: cut through a root-choked side tunnel) |
| Choices | Where the remaining relief grain goes (3 options) |
| Unlocks | `LM_GRAIN_ROUTE`; Corvin's trust (granary tally room access); the Hill Depot as a revisitable dungeon; MQ3 |

## A5. The places

### A5.1 Crestbridge granary yard and undercroft [NEW detail on CANON place]

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Granary yard** | Arrival; Corvin; the finale. | Wagons are lined up under the granary hoists. One barrel head serves as a writing desk, with an ink ring and a blotter. A **waiting wall** worn smooth at child height (bible P02) faces the yard. Keepers lean on it and children sit on it. |
| **B. Tally room** | Corvin's office. | Two tally racks side by side: notched sticks, one rack marked with the Board's ribbon and one plain. The two racks match exactly. A clean, bare shelf where a ledger would stand. |
| **C. Undercroft bays** | Where drawn sacks stand before loading. | Dust outlines on the floor show where sacks stood. Twelve bays have been swept, and three are still full: the next draw. A chalk line runs to a heavy door at the back marked HILL GATE. |
| **D. Hill passage** | Wartime passage from the undercroft into the hill. | Stone-lined, with old iron lamp hooks. A cart-rut floor is worn smooth, and it is worn fresh too: there is no dust in the ruts. Halfway down, a ragged goblin hole has been dug through the left wall, with grain spilt around it like a dropped necklace. |

### A5.2 The Hill Depot [NEW POI P07] — Lowmark's first dungeon

A wartime emergency store cut into the hill behind the granaries, built for engineers, porters and carts. When the war ended it was sealed at the granary end and forgotten at the river end. A Field Goblin warren has grown into it from below, through old grain-bin floors. The space reads in two layers: **orderly wartime stone** (stencils, racks, arches, numbered bays) and **goblin improvisation** (straw, twine, broken tools and stolen sacks). **MAP VERIFICATION REQUIRED** for the hill's position relative to the granaries and the river.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **E. The Sorting Hall** | First large room; trap tutorial; first goblin camp. | A long vaulted hall with wartime rack rows and stencilled bay numbers. Half the racks are pulled down to make goblin pens. Faded painted stencils: a sheaf over a wave, and **RELIEF — ROTATE BY LOT**. Straw is spread across the floor, and in places the straw is suspiciously even (the rake bed). |
| **F. The Twine Door** | Arch into the warren. | Baling twine is strung across the arch at ankle height and tied off to a bent sapling lashed to the wall with a scythe blade bound to it. A goblin has drawn a smiling face on the blade in grain dust. |
| **G. Low Tunnels (the warren proper)** | Close-quarters crawl. | Goblin-dug passages linking old grain-bin bases. The ceilings are low (camera collision handles framing; there is no crouch mechanic). Roots hang through the ceiling. Pans and cups are tied on twine as alarm bells. Two routes run in parallel and rejoin (§A6 Beat 4). Tiny goblin handprints in whitewash run along the walls at goblin shoulder height, like a child's game. |
| **H. The Larder** (optional) | Side room; loot; a trapper. | A goblin hoard of everything shiny: a keeper's button, spoons, a broken lantern lens, a horseshoe on a string. Nothing here is evidence (§A7 rules). |
| **I. The Harrow Run** | Corridor to the heaps. | A spiked harrow hangs on a rope above the corridor. The rope runs up to a ledge where a trapper waits. Dust drifts down whenever the rope creaks. |
| **J. The Heaps and the Throne** | The Sack-King's hall; the boss; the "wrong reading". | The depot's old mess hall. Grain sacks with Crestbridge tally marks are piled into a lopsided throne with a bushel hoop for a crown hung on the back. There are smaller nests of sacks around the walls. A wartime grain bin is propped over the throne on a jack. Count the sacks and there are **twelve**. |
| **K. The Chute Gallery** | The real discovery; past the warren. | A wartime gallery ending in a stone chute that drops through the hillside to the river, with a timber pulley gantry over its lip. The goblins have not been here: no straw, no twine. The gallery door on the warren side was barred **from the chute side**. The goblins came in through a tunnel beside it, which is how the player gets in too. **RELIEF CUT** is stencilled on the wall with an arrow pointing down the chute. The **Marking Stone** is mortared into the wall at shoulder height (§A8). |
| **L. Chute lip and river ledge** | Exit to daylight; optional. | A narrow ledge beside the chute mouth, high above a slack backwater of the river. Below, a mooring ring is driven into the rock, and its rust is rubbed bright. A short walk down the ledge reaches the riverbank and the hill road back to Crestbridge (shortcut unlocked after the boss). |

## A6. Player-facing sequence

### Beat 0 — Counted Twice (`S00_arrive`)
**Objective:** *Find the grain factor at the Crestbridge granaries.*
The lead-in depends on `LM_TL_EVIDENCE`. All three variants end with the player entering the granary yard volume (area A) and the quest becoming Active.

| `LM_TL_EVIDENCE` | Lead-in | First line in `SM-D1` |
|---|---|---|
| keepers | Hollis's report reached Crest Hall with the player's name in it. Hollis is at Crestbridge to give evidence and greets the player on the bridge (cameo, bark `SM-B0.1`). He walks them to the granary gate. | Corvin has the report on his barrel desk: "You're the one in Avery's report. Three pages. He writes a great deal." |
| riverfolk | Maelin's crews found a second wrong post (bark at Whisperflow after TL: "Grain on that order came from Crestbridge. Man who counts it is Tath."). Crestbridge has no record. | Corvin is wary: "Crest Hall has no report of any marker. You'll forgive me if I count you before I trust you." |
| player | The player carries the TL `dispatch_order`. The granary porter at the gate recognizes the paper stock (bark `SM-B0.3`). | Corvin: "That's my dispatch paper. It left this room blank." |

**Verbs:** travel, arrive.

### Beat 1 — Short Measure (`S01_count`)
**Objective:** *Check the granary's count.*
`SM-D1` with Corvin. He does not give an opinion; he gives numbers. Then the player counts for themselves in the tally room and undercroft (three inspects, any order):
- **The two tally racks:** both read 120 sacks drawn under the Board's order.
- **The swept bays:** dust outlines show where 120 sacks stood. Three bays are still full: the next draw, already staged.
- **The hill gate:** the chalk loading line runs to the HILL GATE, not to the yard doors. "Draws go out the hill gate to the hill road yard. Carts load there."

Corvin's case: 120 went out of the hill gate and only 40 reached Wynn's cart in the hill road yard, so something is eating sacks in the passage between them. The goblin hole proves it to him.
**Optional lead (`SM_LEAD_WYNN`):** Wynn Tarrow is in the hill road yard waiting for her next load (`SM-L-WYNN`). She counted her 40 twice, and the yard porter tried to hand her 42. "Gave two back. Somebody's counting worse than me." The lead is never required. It shows Wynn's honesty in play rather than asserting it, adds her to the escort option (`SM-D7.11`), changes `SM-D8.04`, and seeds MQ12.
**Optional drill (`S01c_drill`, `SM_DRILL_DONE`):** at the waiting wall, one of Captain Hesketh's keepers (role-based **Keeper drill-sergeant**) is running two recruits through the bridge drill and offers the player a turn (`SM-L-DRILL`). The sergeant swings a padded practice staff with a long, readable telegraph: staff raised high and drawn back, boots set (~1.4 s), then a heavy overhead blow. Three swings. The player can meet each one by **guarding** (if they carry a guard-capable off-hand or weapon) or by **stepping off the line** (always available). Either answer counts; a swing taken full on knocks the player back a step and the sergeant says so, no damage. The lesson is the one the Sack-King's flail and MQ4's pole sweeps will test: *read the wind-up, brace or move, then hit back*. At the end the sergeant points the player to a basic guard: **Brigid Corliss's forge under the span** (*Honest Steel*) or **the keepers' quartermaster** at the bridge house. No item is granted and no stats are named here; the item pass owns the guard's definition (Equipment Milestone 1). Skipping the drill costs nothing.
**Verbs:** count, investigate; optional drill.

### Beat 2 — The Hill Passage (`S02_descend`)
**Objective:** *Go down the hill passage.*
Corvin unlocks the HILL GATE. In the passage (area D), two Field Goblin scrappers are dragging a sack toward their hole (**SM-E1**). This is the first goblin fight, in a corridor wide enough to step around them. After it the player inspects the **goblin hole** (spilt grain, claw-dug, fresh) and the **ruts** (no dust; carts have used this lately). The hole leads into the Sorting Hall.
**Verbs:** fight, inspect, enter.

### Beat 3 — The Sorting Hall (`S03_sorting_hall`)
**Objective:** *Get through the Sorting Hall.*
This is the trap tutorial. Every trap is **visible to a player who looks** (inspect reveals it and offers a disarm interaction) and **survivable by a player who doesn't** (moderate damage and a short stagger, with no death from a trap alone).

| Trap | Built from | Telegraph | Disarm | Triggered |
|---|---|---|---|---|
| **Rake bed** | Rakes laid tines-up under even straw | Straw lies unnaturally flat; a tine glints in lantern light | *Kick the rakes over* (instant) | Handle swings up: light damage, 1 s stagger. Funny the first time. |
| **Twine scythe** (area F) | Scythe blade on a bent sapling, tripped by baling twine | Twine visible at ankle height; the sapling creaks under tension | *Cut the twine* (1.5 s channel) | Blade sweeps across the arch after a 1.2 s creak: moderate damage. Walking on through is the escape. |
| **Pan alarm** | Pans and cups on twine (area G) | Visible, clinks softly | *Lift the twine* (instant) | No damage. Wakes the nearest goblin group, which comes to the player. |

A goblin **trapper** and two **scrappers** hold the hall (**SM-E2**). The trapper re-sets rake beds during the fight (a 2 s crouch-and-scrape telegraph). Kill it first or keep clear of the straw. A collapsed rack makes an **agility trigger** up to a gallery ledge that skips the twine door. The walkable fallback is through the twine door.
**Verbs:** inspect, disarm, fight, traverse.

### Beat 4 — The Low Tunnels (`S04_warren`)
**Objective:** *Find where the goblins took the grain.*
The warren proper (area G). The player follows the grain spill: sacks leak, so the trail is literal. Two parallel routes rejoin at the Harrow Run:
- **Bin route:** through three old grain-bin bases. Scrapper ambushes burst from side holes (**SM-E3**); dirt trickles from the hole for 1 s before each one.
- **Root route:** shorter, choked by driftroot. With a cutting tool the player can **cut through** using the standard Woodcutting gather interaction (entry level). It avoids one ambush and grants Woodcutting XP for the action. Without a tool the player takes the bin route. Nobody is blocked.

Optional: **the Larder** (area H, **SM-E5**), a trapper guarding goblin shinies. Ordinary loot only.
**Verbs:** track, fight, optional Woodcutting.

### Beat 5 — The Harrow Run (`S05_harrow`)
**Objective:** *Get past the harrow.*
A trapper on a ledge holds the harrow rope. When the player walks under, the rope creaks and dust falls for 1.5 s, then the harrow drops on a marked strip of floor (heavy damage if standing on the strip; the shadow of the harrow is the marker). Options: walk through quickly after a drop (the trapper takes 6 s to haul it back up), or climb the ramp to the ledge and deal with the trapper (one fight, no harrow). Click-to-move friendly: the strip is short and the timing is generous.
**Verbs:** read a hazard, choose an approach.

### Beat 6 — The Sack-King (`S06_sack_king`)
**Objective:** *Deal with the Sack-King.*
The throne room (area J). The **Sack-King** (Field Goblin elite, **SM-E4**) wears a grain sack as a cloak and a bushel hoop as a crown and fights with a threshing flail. Two scrappers attend him. Full kit in §A7.
After the fight the room is quiet, and the player can **count the heaps** (`S06b_count_heaps`, required; three heap inspects). Total: **twelve sacks**, all with Crestbridge tally marks. The inspect text does the arithmetic the player is already doing: *"Twelve. That leaves sixty-eight nobody can find."* This is the moment the wrong reading ("goblins took it") fails, and the player has done the counting themselves.
**Verbs:** fight, count.

### Beat 7 — The Chute (`S07_chute`) — *the discovery*
**Objective:** *Find where the rest went.*
Behind the throne, the goblins' last tunnel breaks into the **Chute Gallery** (area K) beside a door barred from the far side. The player sees, in any order (three required inspects plus one pickup):
- **Rope burns** on the gantry beam: fresh, pale, with fibres still in them.
- **The pulley:** new tallow, still soft, smelling of the chandler's rather than of the war.
- **Boot prints** in the gallery dust: hobnailed and human-sized, many of them, coming up from the chute lip and going back down. There are no goblin prints.
- **The requisition slip** (`SM_requisition`, quest item 1): wedged under the gantry's foot where someone dropped it. *Lower at the hill chute. Eighty measures. Under the Provision Board's emergency order.* It carries the Board seal and no name.

Two things are in the gallery that the objective does not ask for:
- The **RELIEF CUT** stencil with its arrow down the chute (optional inspect, `SM_LEAD_STENCIL`).
- **The Marking Stone in the wall** (presentation plays on proximity; inspect is optional and sets `SM_STONE_SEEN`; §A8).

Unbarring the gallery door from the inside (`S07b_unbar`, required) opens a direct route back to the passage. Corvin's porters arrive behind the player to haul the goblins' twelve sacks home (barks `SM-B7`). That is the end of the dungeon. The chute lip (area L) is an optional view: the mooring ring rubbed bright, and the river backwater below.
**Verbs:** investigate, discover.

### Beat 8 — The Next Draw (`S08_yard`)
**Objective:** *Take the slip to Corvin.*
The player comes up into the granary yard (area A) **while the next draw is being signed**. This is the glimpse, and it plays as live world action, not a cutscene:
- **Keeper-Captain Bram Hesketh** signs the draw on the barrel head. He looks tired, and his keepers are lined up at the hoists.
- **Provisioner Edda Marrick** `[ANTAGONIST]` thanks him warmly on behalf of "the households" and leaves with her clerk (barks `SM-D5`). If the player stands near, she offers one gracious line about goblins (`SM-D5.03`). She does not stop to talk.
- **Steward Aldric Fenmere** has been present as witness to the draw, as stewards are. He stays.

The player can approach Hesketh briefly (`SM-D5.10`, optional). Then `SM-D6` in the tally room: Corvin does the subtraction aloud, and Aldric reads the slip. **Nobody accuses anybody.** "The Board has five seats and one seal." Aldric cannot move against the Board on a slip found in a goblin hole. Corvin can do one thing: he will not load the chute again, and the sacks in his bays answer to his tally.
**Optional lead:** with `SM_LEAD_STENCIL`, the player can ask Aldric about RELIEF CUT. He knows the name from the old supply compacts: a wartime channel, "closed after the armistice. Closed, not filled." He does not know it is open (bible §2.4). This sets `SM_LEAD_CUT_NAMED`.
**Verbs:** observe, present.

### Beat 9 — Where the Grain Goes (`S09_choose`)
**Objective:** *Decide where the remaining relief grain goes.*
`SM-D7`. The remaining grain is the goblins' twelve sacks plus the three full bays of the new draw. Corvin lays out what he can physically do; Aldric frames the cost; Hesketh is called in from the yard for the escort option. The choice is in §A9.3.
**Verbs:** choose.

### Beat 10 — Two Tallies (`S10_close`)
**Objective:** *Speak with Corvin.*
`SM-D8`. Corvin cuts a third tally stick, one that the player has seen him cut, and hangs it on the plain rack. This is his trust, shown rather than said. He gives the player the run of the tally room. The quest completes.

## A7. Encounters

Novice-equipment tuning targets. Final numbers belong to the Gameplay Designer after a playable build.

| Id | Enemies (family §10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **SM-E1** | 2 × Field Goblin scrapper | Hill passage, at the hole | Aggressive; drop the sack and engage on sight | Scrapper: hoe lifted overhead (~1.0 s), then a chop | First goblin read: small, quick, weak alone | 20–30 s; little damage taken |
| **SM-E2** | 1 × trapper, 2 × scrapper + rake beds | Sorting Hall | Trapper: keeps distance, re-sets rakes (2 s scrape), throws a sickle (~1.2 s windup, short range); scrappers aggressive | As listed | Teaches "kill the trapper" and "look at the floor" | 45–60 s; 70–85% HP remaining if the player reads the floor |
| **SM-E3** | 2 + 2 × scrapper (two ambush pairs) | Bin route side holes | Ambush from holes | Dirt trickle (~1.0 s) before emerging | Close-quarters reading | 2 short fights, ~20 s each; avoidable by the root route (one pair) |
| **SM-E4** | **Sack-King** (Field Goblin elite) + 2 × scrapper; up to 2 more scrappers called | Throne room | Elite melee with a summon and a room hazard | See below | Act I's first elite; the dungeon's payoff | 60–90 s; a first attempt ends at 30–60% HP; death possible only by ignoring every telegraph |
| **SM-E5** (optional) | 1 × trapper, 1 × scrapper, rake bed | The Larder | As E2 | As E2 | Curiosity reward (loot table only) | Optional |

**The Sack-King: kit**

| Ability | Telegraph | Counterplay |
|---|---|---|
| Flail (auto-attack) | — | — |
| **Threshing** (cooldown special) | Spins the flail overhead with a rising whistle (~1.5 s) | Slams a cone in front of him. Step to his side or behind him (click a nearby floor point). |
| **Call the heaps** (twice per fight, at 75% and 40% HP) | Bangs a pot lid on his crown (~1.0 s, loud) | Two scrappers burst out of the sack nests. They are weak, but ignoring them lets the Sack-King land Threshing. |
| **Bin pull** (once, at 50% HP) | Yanks a rope on the jack; grain begins trickling from the bin above in a visible ring (~2.0 s) | The bin pours. Standing in the pile slows the player (knee-deep grain) and deals light damage over time for ~6 s. Move out of the ring. The pile remains as slow ground for the rest of the fight, which narrows the room. |
| No flee | He fights to the end, wearing his crown (Phase 1.3 rule). | — |

**Rules for all SM encounters**
- **Combat never reveals evidence.** The slip is found on the floor of a room the goblins never entered. The twelve sacks are counted by inspection of a place. Nothing a goblin drops advances the investigation.
- **Respawn:** after S06 the depot becomes a revisitable dungeon. Goblins respawn as ordinary world creatures; the Sack-King is replaced by a non-elite "heap-boss" scrapper (the crown passes on; bark `SM-B9.3`).
- **Death:** respawn at the undercroft bays with step, flags and `SM_requisition` intact. Defeated trap states persist per player.
- **Co-op:** shared world creatures; each participant on the step gets credit. Traps are world objects: a trap one player disarms is disarmed for everyone in that shard instance, and partners who haven't reached S03 see it re-armed in their own presentation where per-player props are available. Fallback: shared state, which only helps.

## A8. The discovery moment: the stone in the dry wall

A quiet, unsettling moment in the middle of a dungeon. It must not look like a magic item or a puzzle.

| Element | Spec |
|---|---|
| Trigger | Player enters a ~4 m volume around the stone in area K. Plays once per player on first entry; inspect is available after. |
| Object | A carved slab mortared into the gallery wall at shoulder height, set sideways among ordinary building stone. A groove runs up its face to one crisp notch, with fainter notches below. It is the same kind of stone as the Whisperflow footing. Someone used it as building stone. |
| The line | The gallery is bone-dry. The stone carries a **dark damp line** up its groove that ends **exactly level with the notch**. Nothing above the notch is wet. There is no drip, puddle or source. |
| Audio | On entering the volume, the gallery's ambience (a draught over the chute lip, distant goblin clatter) ducks over 1.5 s, the same curve as the Whisperflow dead spot. A faint **sound of running water with no water** is audible for ~4 s (canon: Tovin's "sounds of water when no current flows"). Then the ambience returns. No music. |
| Touch | Optional interaction *Put a hand on the stone*: the interaction log reads *"Cold. Colder than the wall around it."* No effect, no buff. |
| UI / camera | No UI during the duck. Camera always the player's. |
| Inspect texts | See dialogue file, §SM inspect texts. Variants on `TL_STONE_PUBLIC` / `TL_STONE_KEPT`. |
| Co-op | Client-side presentation per player on their own first entry. |
| What it means | Nothing the player can prove. It tells an attentive player that the wartime builders broke up older carved works and that this one still "reads" its line, even in a wall. It names no one and settles nothing (evidence rule). |

**Author truth (for the ledger):** wartime engineers salvaged Marking Stones from the Braids the Relief Cut severed and used them as building stone in the depot and the Hollow Lock (bible §2.1). The damp line is bounded resonance at a stone whose Braid is still disturbed. It is not a message.

## A9. Quest structure for implementation

### A9.1 Steps and completion events

| Step | Objective | Completes on (server event) | Req. | Notes |
|---|---|---|---|---|
| `S00_arrive` | Find the grain factor at the Crestbridge granaries. | Enter granary-yard volume (area A) with TL Completed | Yes | Quest → Active. Lead-in variant by `LM_TL_EVIDENCE`. |
| `S01_count` | Check the granary's count. | `SM-D1` end node + 3 inspects (tally racks, swept bays, hill gate) | Yes | `SM-L-WYNN` available S01–S08 |
| `S01c_drill` | (Optional) Take a turn at the keepers' drill. | `SM-L-DRILL` end node after 3 practice swings met (guard or step-aside) | No | Sets `SM_DRILL_DONE`. Available S01–S10 and after completion. Practice staff deals no damage. |
| `S02_descend` | Go down the hill passage. | SM-E1 defeated + inspect goblin hole | Yes | Corvin unlocks HILL GATE at `SM-D1` end |
| `S03_sorting_hall` | Get through the Sorting Hall. | Enter warren volume (area G) | Yes | Agility shortcut or twine door; SM-E2 need not be cleared to pass, but it is in the way |
| `S04_warren` | Find where the goblins took the grain. | Enter Harrow Run volume (area I) | Yes | Root route: Woodcutting gather on `driftroot_choke` node (optional) |
| `S05_harrow` | Get past the harrow. | Enter throne-room volume (area J) | Yes | |
| `S06_sack_king` | Deal with the Sack-King. | Sack-King defeated | Yes | Throne-room door does not lock; the fight can be left and re-entered (the Sack-King resets to full) |
| `S06b_count_heaps` | (folded into S06 objective text) | 3 heap inspects | Yes | Sets `SM_HEAPS_COUNTED` |
| `S07_chute` | Find where the rest went. | 3 inspects (rope burns, pulley, prints) + `SM_requisition` acquired | Yes | Optional: stencil inspect, stone inspect |
| `S07b_unbar` | (folded into S07) | Interaction `unbar_gallery_door` | Yes | Opens return route; porters spawn |
| `S08_yard` | Take the slip to Corvin. | Enter tally room after glimpse volume; `SM-D6` reaches `SM-D6.40` | Yes | Glimpse actors run on entering the yard; if the player rushes past, Hesketh and Aldric still stand where the player can find them |
| `S09_choose` | Decide where the remaining relief grain goes. | `SM-D7` choice node resolved | Yes | Sets `LM_GRAIN_ROUTE` |
| `S10_close` | Speak with Corvin. | `SM-D8` end node | Yes | Quest → Completed |

### A9.2 Flags

| Flag | Set by | Read by (this package) | Read by (later packages) |
|---|---|---|---|
| `SM_LEAD_WYNN` | `SM-L-WYNN` | `SM-D8` variant | MQ12 Wynn-paid scene (suggested line in dialogue file) |
| `SM_HEAPS_COUNTED` | S06b | `SM-D6` subtraction line | — |
| `SM_DRILL_DONE` | `SM-L-DRILL` | Sergeant's repeat line | — (no later reads; points to the HS forge and the quartermaster only) |
| `SM_LEAD_STENCIL` | Stencil inspect (area K) | `SM-D6.30` option | MQ4 Cut-mouth inspect variant (`NF`); MQ9 flow-table line (optional) |
| `SM_LEAD_CUT_NAMED` | `SM-D6.31` | `NF-D1` Maelin option (`NF-D1.30`) | MQ10 (Aldric's archive line) |
| `SM_STONE_SEEN` | Stone inspect | `SM-D6` option | MQ4 counterweight-stone inspect; MQ8/MQ9 stone-reading lines |
| `SM_CORVIN_TRUST` | `SM-D8` | — | MQ10 (Corvin's tallies chip is offered without a request) |
| `LM_GRAIN_ROUTE` | `SM-D7` | `SM-D8` variant, post-quest barks | MQ10 terms; MQ12 far-bank scene |

### A9.3 Choice: where the remaining relief grain goes

The far bank is hungry and the Board's order says "delivered". Corvin has twelve recovered sacks plus three bays of a fresh draw, and he has barred the hill passage. No option is wrong. Each has a cost someone pays.

| Option | Immediate result | Cost | Later (consequence hooks) |
|---|---|---|---|
| **Escort** (`LM_GRAIN_ROUTE = escort`): *"Send it by road, with keepers, to households we can name."* | Hesketh lends a keeper escort. Wynn is hired to drive the lead cart (if `SM_LEAD_WYNN`, she asks for it by name). Corvin writes three household names on the dispatch: **the Carrows** at the far-bank ford, **the Hobbs** on the low smallholding, **the Haskins** up on the far-bank rise [NEW households]. Carts leave the yard as the player watches. | Slow (days on the road), and keepers on the far-bank road are keepers not at Crestbridge. The Board learns the depot is known. | **MQ10:** Hesketh's line "half my keepers were on the far-bank road" (reduced defenders in the siege's first wave, a flavour line only; no mechanical penalty). **MQ12:** all three households fed. A chalk sheaf (Lowmark thanks-mark [NEW]) on the Carrows' door; the Hobbs' oven is lit; Old Haskin waves from the rise. |
| **Hold** (`= hold`): *"Hold it here under your tally until the Board explains."* | Corvin seals the bays with his own tally ribbon. A courteous Board note arrives before the quest ends (`SM-B9.1`): the grain "will move when conditions allow." | The far bank goes without. Act I post-quest barks at Whisperflow carry it: thinner far-bank travellers, a household asking whether "the grain's still coming". | **MQ10:** strongest physical chip. Board books say "delivered" while the sacks sit under Corvin's seal (Corvin: "They can't have delivered what's in my bays"). **MQ12:** the Haskins have left the rise for dock work in Brookhollow (empty house prop). The Hobbs are thin and civil. The Carrows say the record was honest and the winter was not. |
| **Split** (`= split`): *"Send half by road now. Hold the rest as proof."* | Half the sacks go with a smaller escort to the Carrows and the Hobbs. Half stay sealed. | The Haskins, furthest away, wait. Both the Board and the far bank are half-satisfied. | **MQ10:** medium chip (sealed half). **MQ12:** Carrows and Hobbs fed. The Haskins are still on the rise, sharp with the player: "We were the other half." |

**MQ12 hook summary for the Act III author:** the three named households, their props (chalk sheaf, lit oven, empty or occupied rise house), and one seed line per outcome are in the dialogue file, §SM-H. Use the household names as written.

## A10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| Corvin's trust: tally-room access | Access / knowledge | The tally room's plain rack becomes inspectable and returns current draw counts on later visits (flavour; feeds MQ10). |
| The Hill Depot | Access | A revisitable low-tier dungeon with goblin respawns and an unlocked river-ledge shortcut to the hill road. |
| Small payment | Currency | Corvin pays a porter's day for the twelve sacks recovered ("Twelve sacks, twelve parts of a day"). Amount set in economy tuning. |
| Skill XP | Action XP only | Melee and optional Woodcutting from actions. No lump quest XP. |
| Side-quest unlocks | Story | *Bark for the Pits*, *Honest Steel*, *Night Bridge*, *Night Ferry*. |
| MQ3 lead-in | Story | A Watcher's lantern-tag is hung on Corvin's tally-room door for the player (§B6 Beat 0). |

## A11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Death in the depot | Respawn at the undercroft bays. Steps, flags, `SM_requisition` and disarmed traps are kept. The Sack-King resets to full if the player died during his fight. |
| Logout mid-dungeon | Restore last persisted step. On re-entry the player spawns at the hill gate with the shortcut states they had earned. |
| No cutting tool | Bin route (Beat 4). |
| Skipped optional inspects | All three proofs of human use are required inspects and are on the critical path. The slip is guaranteed: it does not despawn and cannot be looted by anyone else. |
| Rushed past the glimpse | Hesketh and Aldric stand where the glimpse leaves them. Marrick's lines are not required. |
| Walking away | Stays Active; next granary-yard entry re-prompts at the current step (no abandon; see TL §12 resume hook). |
| Fail state | None. |
| Co-op | Independent instances. The glimpse plays per player from their own step. `SM_requisition` is granted to each participant. The choice is per player, so two partners may route the grain differently. Each sees their own carts (per-player props). Fallback: the carts are a bark-only result. |

## A12. Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Steps, flags, region flag writes | Schema & Content / Systems (31.3, 24.1) | As TL §12.2. |
| **Trap objects** (rake bed, twine scythe, harrow, pan alarm) | Systems Engineer + Gameplay Designer | A world object with armed/disarmed state, a trigger volume, a telegraph timer and a damage/stagger payload. An inspect reveals it and offers the disarm interaction. One generic "farm-tool trap" definition with four presentations is enough. |
| Elite room hazard (bin pull) | Systems Engineer | Timed ground hazard volume (slow + damage over time) that persists to end of encounter. |
| Summon from props (call the heaps) | Systems Engineer | Spawn points bound to nest props, with a capped count. |
| Barred-door one-way shortcut | Systems / zone | Interaction on one side only; persistent per player. |
| Glimpse actors | Systems / NPC | Step-conditioned NPC positions and ambient barks. No cutscene. |
| Per-player cart props (choice result) | Systems | Client presentation by `LM_GRAIN_ROUTE`; fallback bark-only. |
| Creature definitions | Schema / Gameplay | Field Goblin scrapper, trapper, Sack-King (elite), heap-boss (post-quest). |
| Quest item `SM_requisition` | Schema | Non-droppable document item with inspect text. |

## A13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Where the relief grain went** | Lowered at night from the depot chute to barges, on Board-sealed slips, by Sallow's crew for Marrick's scheme `[ANTAGONIST]` (bible §2.2). | "Delivered" (Board books); goblins (Corvin's first reading). | 120 drawn, 40 carted, 12 in heaps; rope burns, tallow, hobnail prints, the slip. | Goblins took it; Corvin is skimming; Wynn is skimming (ruled out by her returned two sacks). | Who signed the slip; where the barges go. | MQ4 (the barge), MQ10 (the Board). |
| **The stone in the depot wall** | A salvaged Marking Stone from a severed Braid. | Unknown. | The damp line at the notch in a dry room; the water sound with no water. | A drowned person's grave marker; a magic battery; someone poured water. | How many such stones were salvaged and where. | MQ4 (the Lock's counterweight), MQ9. |
| **RELIEF CUT** | The wartime channel (bible §2.1). | Forgotten; a name in old compacts. | The stencil and arrow; Aldric's "closed, not filled". | A depot department; a grain grade. | That it is open. | MQ4. |

## A14. Open decisions

1. **D-1 antagonist.** Marrick's glimpse lines and the Board seal text on `SM_requisition` are the only antagonist-bearing content (tagged). Swap per bible §3.1.
2. **Board composition.** "Five seats and one seal" is a [NEW] line that fixes the Board's seat count. *Recommendation: keep it. It explains why a seal accuses nobody.* Director may change the number.
3. **Thanks-mark (chalk sheaf).** A [NEW] Lowmark custom used as an MQ12 prop. Removable.
4. **Map:** depot position relative to the granaries and the river backwater (MAP VERIFICATION REQUIRED).

## A15. Internal review log

| Finding | Revision |
|---|---|
| First draft had the slip dropped by the Sack-King. That is combat revealing evidence. | The slip lies in a gallery the goblins never entered, beside a door barred from the far side. |
| The grain choice originally had a "hold" option that simply failed the far bank, with no upside. | Hold now gives MQ10's strongest physical chip. Every option costs and pays. |
| "Talk to Corvin, then go to Crest Hall, then to Aldric" chain. | Collapsed: the draw is signed in the granary yard, so Aldric, Hesketh and Marrick come to the player. |
| The heaps were initially counted by an NPC. | The player counts them. The inspect line states the subtraction the player is already doing. |
| Traps risked twitch timing under click-to-move. | Every trap telegraphs ≥1.2 s, is visible on inspect, has a disarm, and cannot kill alone. |
| Corvin's burned-ledger regret was used here. | Removed. The bible gives him one aloud regret, and it belongs to MQ10. Here he shows only the bare shelf (environmental) and his duplicate racks. |
| Aldric risked knowing the Cut was open. | He knows only the wartime name from old compacts ("closed, not filled"), within the canon "ledgers older than the war" and bible §2.4. |
| Quest-item count. | One item (`SM_requisition`). The twelve sacks are carry-free (porters haul them). |
| Independent review pass. | Grain counts reconciled: the slip's "eighty" is the order; twelve were stolen by goblins; the heap line and the MQ4 bill now both say **sixty-eight**. Added the optional keepers' drill (`S01c_drill`) to teach bracing against a telegraphed blow and point to a basic guard (Equipment Milestone 1), with no item stats. |

---
---

# Part B — MQ3 Heavy Water (`HW`)

## B1. The quest in one paragraph

Wraithwatcher Ansel Corrie has three places on his patrol book he cannot cover properly, and he asks the player to look at them. Any order. In the **Floodplain Orchards**, ditch-turner Bryn Ruddock's sluice is jammed with driftroot and the trapped flood water stands among her roots. At dusk, something rises out of the pool. It is the player's first Wraith. It goes down under the blade and then, horribly, gathers itself back up, and Ansel says what every Watcher learns: it will keep doing that until the water moves. The player cuts the jam, hauls the lever, and watches the drift slump into the draining pool and not come back. On the **Ashen Flats**, livestock won't drink from a ditch. Ash Hounds denning in a burned culvert are the ordinary reason, but even with the den cleared the ditch bed shows ripples pointing the wrong way, and the herder has notched her gatepost on the nights it ran backwards. At **Widow's Step**, fen-guide Lessa Mirepath has had a rope on a cutter for a day and a night. He stands knee-deep in heavy water and does not answer. His footprints walk out into the deep water, and a second set walks back, **dry**. The player carries banner-thistle smoke out to him and walks him in, a hop at a time, while drift circles the smoke. Back at the Lantern Post, with three sets of nights in their head and Ansel's book open on the table, the player lines them up: same nights, same lantern-fill, every fifth night, starting on the fen side and moving down. One of those nights is the night someone moved the Whisperflow post.

**What the player should remember:** the first drift standing back up, and the dry footprints. **What the player should want next:** to be at Bramblelock on the next fifth night.

## B2. Selection record

| Candidate | Verdict |
|---|---|
| **A. Ansel explains the pattern.** | Rejected. The brief forbids it; the evidence rule has to be taught by play. |
| **B. One long site with three symptoms.** | Rejected. It loses "any order" and the sense of a Vale-wide problem. |
| **C. Three independent ordinary problems, each with a surviving anomaly, and a synthesis built from the player's own observations** (selected). | **Selected.** Each site is a complete little job (repair, clear-out, rescue). The anomaly is always something left over after the job. Ansel's only roles are to teach the drift rule where he is present and to write down what the player says. |

## B3. Canon grounding

| Element | Source | Status |
|---|---|---|
| Orchards: raised berms, dike lines, sluice gates; Wraith sightings when debris is trapped among roots | Dossier §IV.2 | [CANON] |
| Ashen Flats, Furrowed Plains trench lines, Ash Hounds and their lung-irritant ash | Dossier §II, §IV.3, §VIII | [CANON] |
| Wraithwatchers: lanterns, blessed rope, banner-thistle smoke, no spellcasting | Dossier §III | [CANON] |
| Banner-thistle calms panic during Wraith events | Dossier §X.4 | [CANON] |
| Wraiths are place-bound water-memory manifestations, not souls | Dossier §III, §VIII | [CANON] |
| Trances drawing people into dangerous water | Dossier §XVI.5 | [CANON] |
| Lessa Mirepath: quiet, practical, speaks to the land, treats some routes as permanently "done" and won't say why | Anchors §II | [CANON] |
| Driftroot trees tangle in banks and dikes | Dossier §IX | [CANON] |
| Flow-Menders, softmoss for wounds | Dossier §III, §IX | [CANON] |
| Widow's Step and its unmatched scraps | Part 3 proposal | Proposal; used as [NEW] POI P22 |
| Disperse vs. quiet | Bible §2.5 (D-6) | [PROPOSAL — DIRECTOR] |
| Bryn Ruddock, Elspeth Quill, Reedmere, the Lantern Post, Mabry Gorse, Orrin and Wenna Tull, "lantern fills" | This package / bible §5.3 | [NEW] |

## B4. Quest summary card

| Field | Value |
|---|---|
| Working title | **Heavy Water** |
| Suggested content id | `lowmark.main.03_heavy_water` |
| Arc position | Act I, Main Arc movement 3 ("Three sites, three plausible explanations") |
| Prerequisite | MQ2 Completed |
| Offer | Lantern-tag on Corvin's door points to the Watchers' Lantern Post (P21); `HW-D1` offers the quest. |
| Target length | 35–45 minutes |
| Combat share | ~30% (first drift fight; hounds; the walk-out) |
| Dialogue share | ~20% |
| Exploration, repair, rescue, synthesis | ~50% |
| Skills | Melee (required); Woodcutting (required at the orchard: entry-level driftroot); Hunting (optional: track the hound runner to the den) |
| Choices | Order of sites (free); how to bring Orrin out (smoke hops, with an optional rope assist from Lessa) |
| Unlocks | First quieted drift site; Ansel's patrol book (readable at the Lantern Post); MQ4 |

## B5. The places

### B5.1 Watchers' Lantern Post [NEW POI P21]
A Wraithwatcher rest post on a rise at the fen's edge: a stone shed with a lantern rack, coils of blessed rope (rope with knotted thistle sprigs), a rack of drying banner-thistle, a cold brazier and a lectern. **Ansel's patrol book** is chained to the lectern. It is a working object: thumb-darkened corners, wax drips, entries by place and lantern-fill. On the back wall is a scratched tally of names under "WALKED WITH US", with no dates and no explanations (Old Lantern hook).

### B5.2 Site A: Bryn's dike, Floodplain Orchards [P16]
| Area | Storytelling |
|---|---|
| **A1. Berm walk** | Fruit trees on raised berms. Bryn's ditches are immaculate. Each has a little cut-stone lip, with the turf trimmed like a lawn. |
| **A2. The sluice** | A timber sluice gate in the dike, jammed half-open by a raft of driftroot. Its board has a column of chalk ticks with a scrawl: "rose — no rain". |
| **A3. The root pool** | Flood water trapped among the roots of six old trees. Leaves are rotting on the surface. The bark is waterlined black. A wren's nest is abandoned. Softmoss packed on the dike to stop a seep has gone brown and slimy (canon cue: moss rots faster near drift). |

### B5.3 Site B: the Flats ditch [P14 edge]
| Area | Storytelling |
|---|---|
| **B1. The trough field** | Herder Mabry Gorse's sheep and two cows stand at the ditch and will not drink. A gatepost carries clean knife notches in a column, some marked with a cross. |
| **B2. The ditch** | A cut drainage ditch running from the trench line down to the river. The ditch bed holds the **ripples**: silt laid in little ridges that point *up* the ditch, toward the hills. Reed debris is caught on the **upstream** face of a sluice board. |
| **B3. The burned culvert** | An old trench culvert, charred. Ash, bones and a dead ewe have been dragged into the mouth: the hounds' den, fouling the water downstream. Deeper in (optional) is the Den Mother's chamber. |

### B5.4 Site C: Widow's Step [P22] and Reedmere [P06]
| Area | Storytelling |
|---|---|
| **C1. The offering bank** | An embankment above a slow bend. Unmatched scraps are tucked into the stones: a mitten, a ribbon, a strip of sail. Each is weighted with a pebble. |
| **C2. The drowned causeway** | An old reed-cutters' causeway running out into the bend, now under water to the knee. Lessa's guide stakes stop at the bank. Lessa's rope runs from a stake out to a man standing in the water. |
| **C3. The deep edge** | Where the causeway drops off into the bend's deep water. **Orrin Tull** stands here facing the deep water. The **footprints** are in the mud of the causeway's last dry hump (§B8). |
| **C4. Reedmere** | Fen-edge hamlet on stilts: cutters' huts, eel traps, the Watchers' lantern store. Elspeth Quill's treatment cot is set up on a porch. Wenna Tull sits on the steps of her hut stacking reed bundles (optional lead). |

## B6. Player-facing sequence

### Beat 0 — The Lantern-Tag (`S00_offer`)
**Objective:** *Go to the Watchers' Lantern Post.*
After MQ2 completes, a Watcher's lantern-tag (a tin disc on a thistle-knotted cord) hangs on Corvin's tally-room door with a scratched note: *For whoever read the Whisperflow stone. Lantern Post, by the fen. A.C.* Corvin bark: "A Watcher left that. Didn't want to come in. They never do." Entering the Lantern Post volume starts `HW-D1`.

### Beat 1 — Three Places (`S01_three_sites`)
**Objective:** *Hear what the Watchers need.*
`HW-D1`. Ansel shows the player three entries he has marked with a thumbnail, explains that his patrol leg cannot reach them properly, and asks the player to look and tell him what they find. He will be at the orchards at dusk because they sit on his way out ("the only one of the three I can get to before dark"). He does **not** say what connects them, and he does not know. Map markers are added for all three sites. The patrol book becomes inspectable (`HW-I1`, the pages as they are now).
**Verbs:** listen, read.

### Site A — The Orchard Pool (`S02a_*`)

**A-1 `S02a_bryn` — Objective:** *Find the ditch-turner at the orchard dike.* `HW-D2`. Bryn wants her trees kept and is short with anyone who calls what happens in the pool anything at all. Her sluice is jammed; she has cleared it twice and "it" came up both times. She points at her chalk column (`HW_NIGHTS_ORCHARD` on inspect, required: the nights the pool rose with no rain).

**A-2 `S02a_dusk` — Objective:** *Clear the sluice before dark.* (Whatever the player does, the drift rises at dusk.) If the player arrives in daylight, they can begin chopping the jam. At the first dusk tick while the player is at the pool (or immediately, if the player arrives after dusk), the **drift rises** (presentation: the pool goes glass-flat, leaves stop turning, then the surface draws up into a shape like a wet sheet over a person, and the softmoss on the dike darkens visibly). Ansel arrives along the berm with his lantern on the same tick.

**A-3 `S02a_first_drift` — the lesson.** **HW-E1:** 2 drift. When the first one is dispersed it **sinks, the pool wrinkles, and about 20 seconds later it draws back up** at the pool's centre. This is the teaching beat. Ansel (`HW-D3`) delivers the rule in one line during the fight and one after: *"It'll do that till the water moves."* The design makes the rule felt, not explained:
- Dispersing a drift opens a **visible window**: the pool surface stays slack and wrinkled for ~20 s, and the softmoss lightens briefly.
- During the window the player can work the jam: **chop the driftroot** (standard Woodcutting gather, entry level; three chop interactions on the `driftroot_jam` node, each a short gather). A window comfortably fits one or two chops.
- When a drift re-forms, chopping is interrupted (damage cancels channels). Disperse again to buy the next window.
- After the third chop, the **lever** is free: *Haul the lever* (4 s channel). It must be done in a window too.

If the first drift fight in the player's game happened at Widow's Step (`HW_DRIFT_TAUGHT` already set), Ansel's line changes: "You've seen them get back up, then. Good. Now watch one not."

**A-4 `S02a_drain` — the quieting.** On lever completion the sluice board drops, the pool drains with a long sucking pull through the gate, and any drift **mid-formation slumps into the draining water and goes with it**. No new drift forms. The softmoss stops darkening. Silence, then frogs. The **orchard pool drift site is set to quieted** (first in the game). `HW-D4`: Bryn swears at the sluice with great affection; Ansel writes. Optional: Bryn asks the player to re-pack her seep with fresh softmoss from the shrine stone on the berm (one gather, one place interaction). This is a small kindness that sets `HW_BRYN_MOSS` (an MQ7 line seed).

### Site B — The Ditch That Runs Back (`S02b_*`)

**B-1 `S02b_mabry` — Objective:** *Find out why the stock won't drink.* `HW-D5`. Mabry Gorse thinks it's hounds, and she is right about that. She is also sure the ditch "ran back" one night, and she is embarrassed to say so. Her gatepost notches (inspect, required, `HW_NIGHTS_DITCH`) mark nights the stock refused the water, and the crossed notches are the nights she saw it run uphill "about the second lantern" (she borrowed the Watchers' phrase; she used to walk with them).

**B-2 `S02b_den` — Objective:** *Clear whatever's fouling the ditch.* Follow the foul water (or optionally track a hound runner's ashy prints with Hunting at entry level, which leads in by a side gully and gives the player a flanking position) up to the burned culvert. **HW-E2:** 2 Ash Hound runners and 1 ash-shaker. Then *Drag out the carcass* and *Rake out the ash plug* (two interactions at the culvert mouth). Clean water runs again. The stock drink. **The ordinary cause is real and is fixed.**
Optional: the **Den Mother** (HW-E3) in the inner chamber, for players who want the elite. Sets `HW_DEN_CLEARED` (Joric's MQ5 line seed; the den stays empty).

**B-3 `S02b_ripples` — the surviving anomaly.** **Objective:** *Look at the ditch bed.* With the water running clean and low, the ditch bed is visible, and the ripples are still there: silt ridges pointing uphill, and reed debris stacked on the upstream face of the sluice board (two required inspects). Water doesn't lay silt like that running downhill. `HW-D6`: Mabry, with the stock drinking behind her, says the bit she was embarrassed about. **The hounds explain the drinking. They don't explain this.**

### Site C — Widow's Step (`S02c_*`)

**C-1 `S02c_lessa` — Objective:** *Find the fen-guide at Widow's Step.* `HW-D7`. Lessa has had a rope on Orrin Tull since the wrong night. He walked out along the drowned causeway, and he stands at the deep edge and won't come in. When she pulls the rope he leans toward the deep water. She will not walk the causeway herself: "That path's done." She doesn't say why. (Canon: she treats certain paths as permanently closed and won't explain.)

**C-2 `S02c_prints` — the strange moment.** **Objective:** *Look at the causeway.* On the causeway's last dry hump the player finds two lines of prints from the same hobnailed boots (§B8). Required inspect. Lessa, on hearing about them, says only: "His." She knows his boots. That is ordinary testimony; the dryness she doesn't touch.

**C-3 `S02c_smoke` — Objective:** *Carry the smoke out to Orrin.* Lessa lights a Watcher's banner-thistle **smoke-pot** from the Step's stake box (carry state; never enters inventory). The rule, shown before it is ever told: drift will not enter thick thistle smoke (a ~4 m ring around a set-down pot).
- **While carrying**, the player walks normally and can sprint. Carrying suspends auto-attack.
- **Setting the pot down** is instant and makes a safe ring that lasts until the pot is picked up again.
- On the causeway, drift rise out of the bend as the player approaches Orrin (**HW-E4**, wave 1). The player sets the pot down, fights from inside the ring or steps out to fight, and picks the pot back up when the wave is dispersed.
- At Orrin, the player sets the pot down beside him. In the smoke he turns, slowly, and looks at the player for the first time.

**C-4 `S02c_walk_out` — Objective:** *Walk Orrin back to the bank.* Orrin follows the smoke. He walks only inside a smoke ring. The player **hops the pot**: pick it up, carry it toward the bank (up to ~10 m; a ghost marker shows the furthest set-down point he will follow to), set it down, wait while he walks into the ring. Three hops. **HW-E4** waves 2 and 3 rise between hops. Drift that are dispersed re-form behind the player, which is fine, because the player is leaving.
- **Optional rope assist:** if the player talks to Lessa before the walk-out, she will haul the rope taut from the bank on the second hop (`HW-D8.02`), which stops Orrin turning back toward the deep water if the player lets the ring lapse. Without it, a lapsed ring makes Orrin stand still (never walk deeper), and he resumes when smoke reaches him again. **He cannot be lost** (§B11).
- Click-to-move friendly: every step is a click to a floor point plus one interaction. There is no timing, and the ghost marker removes guesswork.

**C-5 `S02c_elspeth` — Objective:** *Get Orrin to the Flow-Mender.* On the bank, Lessa and the player walk him to Reedmere (escort walk at his pace, no combat), where **Elspeth Quill** is on rounds. `HW-D9`: she treats him (cold, no sleep, rye spirit: "Any one of those would do it"). Orrin speaks once (he doesn't remember the night; the last thing he remembers is the lantern-fill). This sets `HW_NIGHTS_STEP`.
**Optional lead (`HW_LEAD_TALLY`):** Wenna Tull, Orrin's sister, on the hut steps (`HW-L-WENNA`). Orrin cuts a bundle of reed every half lantern-fill when he works nights, and his tally stick stops on the wrong night at exactly two and a half bundles past dusk. Read by `HW-D10` (lets the player name the hour exactly) and `NF-D1` (shortens the watch).
**Optional discovery (`HW_LEAD_SCRAP`):** among the offering-bank scraps, one sail strip is stitched in a pattern Lessa says is "not Lowmark stitching" (Part 3 proposal hook). Read by *The Candle Rule* (side package).

### Beat 5 — What the Book Says (`S03_synthesis`)
**Objective:** *Take what you found back to the Lantern Post.* (Available once all three `HW_NIGHTS_*` flags are set.)
The synthesis is the quest's payoff, and **the player does it**:
1. The patrol book is open on the lectern (`HW-I1`, now with Ansel's latest pages). The player can read it. Every entry gives a **place**, a **night** (counted from the dark moon, the Watchers' reckoning) and a **lantern-fill** (Watcher hours [NEW]: how many times the patrol lantern has been refilled since dusk). The Whisperflow entry Ansel wrote at the True Line camp is on the page: *"Whisperflow — post moved (wood liar). Crossing shut."*
2. `HW-D10`: Ansel asks only, "Go on, then. What've you got?" The player offers statements. Ansel's response depends on what kind of statement it is:
   - **Observations** (place, night, hour, order) he writes down.
   - **Interpretations** ("the drowned are walking", "it's the Field-Mage", "it's the goblins") he answers gently and does not write ("Can't put 'the drowned' in the book. Can put 'nineteenth night'.").
3. The beat completes when the player has made **the three core observations**, in any order:
   - **Same nights:** the orchard chalk, the gatepost crosses and Orrin's night all fall on Ansel's wrong nights (needs all three site flags).
   - **Every fifth night:** the spacing (always available once "same nights" is made).
   - **One of them is the Whisperflow night** (always available; the entry is on the page).
   Two **supporting observations** are optional and change lines: **same lantern-fill** (the hour), and the **fen side first** (Ansel's book records Widow's Step and his own fen-edge entries earlier in the night than the orchard and the ditch). The hour option names the fill precisely only with `HW_LEAD_TALLY`. Without it the player says "about the second fill", which is enough.
4. Ansel then contributes the **one thing only he knows**, his patrol geography: everything coming off the fen side passes Bramblelock Weir before it splits for the orchards and the Flats. "If you want to see it come, sit on the weir." He counts forward to the next fifth night. MQ4 is offered.

**Why this works:** ordinary causes (the jam, the hounds, Orrin's cold and rye) were real and the player fixed them. What survives all three is a pattern in time, and it is not supernatural testimony: it is three records kept by three different people, plus a Watcher's book. The drift never told anyone anything. That is the evidence rule, taught by play.

### Completion
Quest → Completed. The patrol book stays readable at the Lantern Post and updates with later quests (flavour). MQ4 is offered.

## B7. Encounters

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **HW-E1** | 2 × drift (Water Wraith, standard) | Orchard root pool, dusk | **Place-bound:** leashed to pool edge + ~3 m; re-forms ~20 s after dispersal while the sluice is shut | **Lash:** an arm of water rises (~1.0 s) and lashes in a line. **Cold pull:** the surface draws toward it (~1.5 s); standing in pool water near it applies a short slow ("heavy water") | **Teaches disperse vs. quiet** and the leash (stepping onto the berm is legitimate) | The fight is a loop, not a wall: each dispersal takes ~15–20 s. The full sequence (3 chops + lever) takes 3–4 minutes. A first-timer ends at 50–70% HP. |
| **HW-E2** | 2 × Ash Hound runner, 1 × ash-shaker | Burned culvert mouth | Runners: pack, flank. Ash-shaker: holds back | Runner: low crouch (~0.8 s) then a lunge. **Ash-shaker:** shakes its whole body (~1.5 s) and a grey cloud expands (~4 m); inside it the player coughs (attack speed reduced) until they step out | Teaches area denial; first Ash Hounds | 45–60 s |
| **HW-E3** (optional) | **Den Mother** (Ash Hound elite) + 1 runner | Inner culvert chamber | Elite: guards the den; heavier ash cloud; a charge | **Charge:** scrapes the ground twice (~1.5 s), then a straight charge. **Ash storm:** a larger cloud with a 2 s build | Optional elite for players who want one | 60–90 s; avoidable entirely |
| **HW-E4** | Wave 1: 2 × drift. Wave 2: 2 × drift. Wave 3: 3 × drift | Causeway and bend shallows, Widow's Step | Place-bound to the bend; **will not enter thistle smoke**; re-form after ~20 s | As HW-E1 | Teaches smoke as space control; escort without fail state | Each wave ~30 s. Smoke-ring play makes waves trivial to survive; it is about pace, not damage. |

**Rules**
- Combat never reveals evidence. Every night and hour comes from a record (chalk, notches, tally, book) or testimony.
- **Drift never flee** (Phase 1.3). They disperse and re-form. Re-formation is the mechanic, not fleeing.
- **Death:** respawn at the nearest site anchor (orchard berm shrine, culvert field gate, Reedmere porch). Chops, lever, carried-pot position (pot returns to the last set-down point) and Orrin's position persist.
- **Co-op:** shared world creatures. The orchard drain is per player: a partner who drained their own pool sees the pool drained, and a partner who hasn't sees it full and fights their own drift there (per-player site state presentation). Fallback if per-player site state is not ready: the first player to drain it drains it for the shard, and the other players' step completes on entering the drained-pool volume while their quest is at A-3/A-4. Each player walks out their own Orrin. Fallback: a shared Orrin, with credit to all.

## B8. The discovery moment: the dry footprints

| Element | Spec |
|---|---|
| Trigger | Inspect volume on the causeway's last dry hump (C3). Becomes visible from Beat C-1. |
| What the player sees | Two lines of prints from the **same hobnailed boots**. The line going **out** toward the deep water is pressed deep and full of water, as prints in wet mud should be. The line coming **back** toward the bank is crisp-edged and **dry to the bottom**, with the mud inside the print pale and cracked as if a dry summer had passed over it. The returning prints stop at the offering bank, beside a scrap tucked in the stones. |
| Audio | When the player stands in either line of prints: the bend's lap and the reed hiss duck over 1.5 s (same curve as TL and SM), for ~3 s, then return. No music. |
| Reflection | While the player stands in the returning prints, their reflection in the shallows lags by a fraction of a second (TL language). |
| Lessa | If asked, she says "His" (testimony about the boots) and nothing about the dryness. |
| UI / camera | No UI during the duck. Camera always the player's. |
| What it means | Orrin has walked out and back before, on an earlier wrong night, and doesn't remember. That is all an attentive player can take from it. The prints are physical. Their dryness proves nothing and names no one. |
| Co-op | Client-side; any player may inspect. |

**Second strange note (orchard, presentation only):** the drift's formation at dusk (glass-flat pool, leaves stop turning, softmoss darkens) is the first time the player sees a Wraith. It should feel cold rather than spectacular. No music sting. The drift has no face.

## B9. Quest structure for implementation

### B9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_offer` | Go to the Watchers' Lantern Post. | Enter Lantern Post volume (MQ2 Completed) | Yes | Quest → Active on `HW-D1` end |
| `S01_three_sites` | Hear what the Watchers need. | `HW-D1` end node | Yes | Unlocks sites A, B, C in parallel |
| `S02a_bryn` | Find the ditch-turner at the orchard dike. | `HW-D2` end + sluice-board inspect | Yes | Sets `HW_NIGHTS_ORCHARD` |
| `S02a_dusk` | Clear the sluice before dark. | Dusk tick while in pool volume (or entry after dusk) | Yes | Spawns HW-E1; Ansel arrives |
| `S02a_first_drift` | (same objective) | 3 × `driftroot_jam` gather + `haul_lever` interaction | Yes | Channels interrupted by damage; drift re-form loop until lever |
| `S02a_drain` | Speak with Bryn. | `HW-D4` end | Yes | Orchard pool → quieted; `HW_SITE_ORCHARD` |
| `S02a_moss` | (Optional) Re-pack Bryn's seep. | Softmoss gather + place interaction | No | `HW_BRYN_MOSS` |
| `S02b_mabry` | Find out why the stock won't drink. | `HW-D5` end + gatepost inspect | Yes | `HW_NIGHTS_DITCH` |
| `S02b_den` | Clear whatever's fouling the ditch. | HW-E2 defeated + `drag_carcass` + `rake_ash` | Yes | Hunting track optional |
| `S02b_den_mother` | (Optional) Clear the inner den. | HW-E3 defeated | No | `HW_DEN_CLEARED` |
| `S02b_ripples` | Look at the ditch bed. | 2 inspects (ripples, board debris) + `HW-D6` end | Yes | `HW_SITE_DITCH` |
| `S02c_lessa` | Find the fen-guide at Widow's Step. | `HW-D7` end | Yes | |
| `S02c_prints` | Look at the causeway. | Footprint inspect | Yes | Discovery §B8 |
| `S02c_smoke` | Carry the smoke out to Orrin. | Pot set down in Orrin volume | Yes | Carry state; HW-E4 wave 1 |
| `S02c_walk_out` | Walk Orrin back to the bank. | Orrin enters bank volume | Yes | 3 hops; waves 2–3 |
| `S02c_elspeth` | Get Orrin to the Flow-Mender. | Orrin enters Reedmere porch volume + `HW-D9` end | Yes | `HW_NIGHTS_STEP`, `HW_SITE_STEP` |
| `S03_synthesis` | Take what you found back to the Lantern Post. | `HW-D10` reaches `HW-D10.90` (three core observations made) | Yes | Quest → Completed; MQ4 offered |

Site-order flag: `HW_FIRST_DRIFT_SITE` = orchard / step (set on the first drift spawn), used to pick Ansel's or Lessa's teaching line. `HW_DRIFT_TAUGHT` is set by whichever teaching line plays first.

### B9.2 Flags

| Flag | Set by | Read by (here) | Read by (later) |
|---|---|---|---|
| `HW_NIGHTS_ORCHARD`, `HW_NIGHTS_DITCH`, `HW_NIGHTS_STEP` | Site records | `HW-D10` | — |
| `HW_SITE_ORCHARD`, `HW_SITE_DITCH`, `HW_SITE_STEP` | Site completion | Lantern Post barks | — |
| `HW_DRIFT_TAUGHT`, `HW_FIRST_DRIFT_SITE` | First drift spawn / teaching line | `HW-D3`, `HW-D7` variants | — |
| `HW_LEAD_TALLY` | `HW-L-WENNA` | `HW-D10` hour option | **MQ4** `NF-D1` (watch length) |
| `HW_LEAD_SCRAP` | Scrap inspect | — | *The Candle Rule* |
| `HW_BRYN_MOSS` | Optional seep | `HW-D4` coda | **MQ7** Bryn line |
| `HW_DEN_CLEARED` | Optional elite | — | **MQ5** Joric line; *Unreplanted* |
| `HW_FEN_FIRST` | Supporting observation in `HW-D10` | `HW-D10.80` | **MQ4** `NF-D1` (Ansel's opening) |

### B9.3 Choices and consequences
HW's choices are **how** rather than **what**: the order of sites (changes who teaches the drift rule and Ansel's line at the orchard); the rope assist (comfort only); the optional elite; the optional kindness to Bryn. The quest's real decision is the player's statements at the synthesis. There is no wrong answer there; interpretations are simply not written down, and that teaches the evidence rule.

## B10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| Ansel's patrol book | Knowledge / access | The lectern book at the Lantern Post is readable on every visit and grows with later quests. It never enters inventory. |
| First quieted drift site | World change | Orchard pool no longer spawns drift. Bryn's trees recover over the following visits (prop stages). |
| Watcher's welcome | Access | The Lantern Post becomes a rest point: brazier for Cooking, a bed for respawn binding if the respawn system supports it. |
| Small payment | Currency | Bryn pays in fruit (food item, existing type) or a coin. Ansel pays a Watcher's contract day "for three nights' work" (economy tuning). |
| Skill XP | Action only | Melee, Woodcutting, optional Hunting. |
| Side-quest unlocks | Story | *Unreplanted*, *The Uphill Canal*, *Fen Watch*, *Old Lantern*, *The Candle Rule*, *A Verse Kept Back*. |

## B11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player arrives at the orchard in daylight | Can chop the jam freely (no drift). The drift rises at the first dusk tick with the player present, whatever progress has been made. If the lever was already hauled in daylight (fast player), the drift rises mid-formation and slumps immediately; Ansel's line covers it ("You've beaten it to the water. Most people don't get the chance."), and `HW_DRIFT_TAUGHT` is set by the teaching line at Widow's Step or by Ansel's fallback line at the Lantern Post (`HW-D10.05`). |
| Orrin's ring lapses | Orrin stands still and never walks deeper. Lessa's rope (assist) keeps him from turning. **He cannot drown or be lost.** |
| Pot dropped and forgotten | The pot stays where it was set. If the player leaves the Step area, the pot returns to the last set-down point, Orrin to the last ring he stood in. |
| Death | Respawn at the site anchor; progress persists. |
| Logout | Restore step and flags. Orrin restores to his last ring position. Chops persist. |
| Synthesis with no optional leads | The three core observations are always available once the three sites are done. |
| Walking away | Stays Active; resume prompt at the Lantern Post. |
| Fail state | None. |

## B12. Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| **Drift-site state** (active/quieted) driving spawns | Systems + Schema | Per-site state on the character; spawn rule reads it. Fallback: shard-level state (§B7 co-op note). |
| **Re-forming creature** | Systems / Gameplay | On defeat: despawn, start a re-form timer, respawn at an anchor while a site condition flag is false. |
| **Dusk-tick event** | Systems | Time-of-day threshold as a server event while the player is inside a volume. Fallback if world time is not built: a *Wait until dusk* interaction at the berm shrine. |
| **Smoke ring** | Systems | A carry-state object that, when set down, creates a volume drift AI will not path into. Fallback: three pre-placed smoke stakes lit by interaction, with Orrin walking stake to stake. |
| **Follower at pace** (Orrin) | Systems / NPC | NPC follows to the nearest active ring; no combat AI; invulnerable. |
| **Synthesis dialogue** | Schema (31.5) | Options gated on flags; "core observation" counter; effect writes. |
| Creatures | Schema / Gameplay | Drift; Ash Hound runner, ash-shaker; Den Mother (elite). |

## B13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Why three places go wrong together** | Each Hollow Lock flush drags heavy water out of the fen and pushes a pulse down the Vale (bible §2.3). | Curses; bad dikes; hounds; drink. | Same nights, same fill, every fifth night, fen side first, including the Whisperflow night. | The drowned walk on a schedule; the Field-Mage does it; the goblins. | That it is a machine, and whose. | MQ4. |
| **What drift is** | Place-bound imprints that disperse and re-form while conditions remain (bible §2.5). | Hauntings; the drowned. | It gets back up; it stops when the water moves; it won't enter smoke. | Souls; killable monsters; an angry river. | Why grief collects in water at all. | MQ8 (Sedge's demonstration). |
| **The dry footprints** | Orrin walked out and back on an earlier wrong night in a trance; the dryness is bounded resonance at a grief-heavy bend. | — | Two lines of his prints; one wet, one dry. | Something walked back in his boots. | Everything else. | Not revealed in v1 (it stays strange). |

## B14. Open decisions

1. **D-6** (disperse vs. quiet) is the foundation of HW-E1. If the Director rules "Wraiths can be destroyed", HW-E1 becomes an ordinary fight and the lever becomes a plain repair. Ansel's lines `HW-D3` and `HW-D4` change.
2. **Lantern-fills** as Watcher hours [NEW]. *Recommendation: keep.* It fits "seasons not days" and gives Watchers their own time.
3. **Dark-moon reckoning** for nights [NEW]. A world calendar is not required; the book's numbers are fiction, and MQ4's "wrong night" is whichever night the player keeps watch (§C12).

## B15. Internal review log

| Finding | Revision |
|---|---|
| "Any order" conflicted with "the first Wraith fight teaches disperse-vs-quiet". | Both Widow's Step (Lessa) and the orchard (Ansel) carry a teaching line keyed on `HW_FIRST_DRIFT_SITE`. The *first quieted* site is always the orchard, because only there can the player change the conditions in Act I. |
| Ansel's first draft synthesis line said "So it's all on fifth nights, starting at the fen." | Cut. Ansel now only asks, writes and counts forward; every statement is the player's. His only contribution is patrol geography. |
| Lessa risked explaining why the causeway is "done". | She doesn't. "That path's done." Canon refusal kept. |
| The smoke-pot risked being a quest item. | Carry-state object; fallback pre-placed stakes. Act item count unchanged. |
| Escort could fail if Orrin walked into deep water. | Orrin never walks deeper; a lapsed ring makes him stand. |
| Orrin's grief risked naming a dead person. | Nobody names whom he mourns. The scrap at the bank is unnamed. |
| Mabry's crossed notches risked being supernatural evidence. | They are her record of what she saw: testimony and an object. |
| Ditch site risked being quieted by clearing hounds. | It stays active. Hounds were the ordinary cause; the backflow is the surviving anomaly. |
| Independent review pass: "the fourteenth" read as an accidental Fourteenth Lot clue. | Made deliberate and non-supernatural: Ansel adds *"Fourteenth. Watchers don't like that number."* (`HW-D10.30`). Watcher folk-dislike only; nothing explains it until MQ11. The culvert den is cleared here (`HW_DEN_CLEARED`, optional elite); MQ5 does not refight it. |

---
---

# Part C — MQ4 The Night Flush (`NF`)

## C1. The quest in one paragraph

On the next fifth night the player sits on Bramblelock Weir, where everything off the fen side passes before it splits. Maelin Rowe has come to watch the water with them, but she will not take a boat out on this stretch at night. Around the second lantern-fill the river's sound drops away. The weir goes quiet. Then a low thump comes up through the stones, and a pulse of water lifts the weir pool a hand over its marker notch, and on top of the pulse, poled silently with hooded lanterns, rides an unlit barge heavy with sacks. The player follows on foot along the weir walls and the towpath. They lose it, find it again by its wake on the bank and the grain it leaks, and see it turn off the river into a straight, wrong channel: the **Relief Cut**. Up the Cut stands the **Hollow Lock**, a chained wartime sluice-house whose chain has been cut and whose gear is greased fresh. The player storms it in two parts, the yard and then the winding floor. Inside, they find a stack of new yellow marker posts with notches already cut a hand high, a chalk list of crossings, and a bill of lading under Board seal. They wind the Lock shut by hand while the crew comes up from the barge and drift rises in the churning chamber. The factor running the Lock, a cheerful man who touches the chain before every flush, gets away by boat, and a beaten crewman says his name: **Gideon Sallow** `[ANTAGONIST]`. The player chooses whether to smash the winding gear or chain it as evidence. At dawn Bramblelock lies flat for the first time in a month, and Ansel arrives to say the fog over Stillwater is thicker than he has ever seen it.

**What the player should remember:** the weir going silent, then the barge on the pulse. **What the player should want next:** to understand why stopping the flush made the fen worse.

## C2. Selection record

| Candidate | Verdict |
|---|---|
| **A. Ambush the barge at the weir.** | Rejected. It spends the Lock, and the brief requires the pursuit and the two-part assault. |
| **B. A stealth infiltration of the Lock.** | Rejected. No stealth system in v1 (Phase 1.3). |
| **C. Watch → flush → unfailable pursuit → two-part assault → hold the crank → choice → dawn turn** (selected; the bible brief). | **Selected.** A single night with one escalating rhythm: stillness, surge, momentum, violence, labour, decision, quiet. |

## C3. Canon grounding

| Element | Source | Status |
|---|---|---|
| Maelin refuses night passage through specific stretches | Anchors §II | [CANON] |
| Smugglers and bandit crews tied to black-market routes | Dossier §VIII | [CANON] |
| Dwarven-engineered wartime water and bridge works | Dossier §II | [CANON] |
| Agility triggers (no jump) | Phase 1.3 §1 | [CANON]; approved, not yet implemented |
| Bramblelock Weir and its numbered convoy stones | Part 3 proposal; bible P08 | Proposal; [NEW] POI |
| The Relief Cut, the Hollow Lock, Sallow, the pre-notched posts, the bill of lading | Bible §2, §3 (D-1, D-2) | [NEW] / [PROPOSAL — DIRECTOR] |

## C4. Quest summary card

| Field | Value |
|---|---|
| Working title | **The Night Flush** |
| Suggested content id | `lowmark.main.04_night_flush` |
| Arc position | Act I, Main Arc movement 4 ("A harm someone is using"); **Act I turn** |
| Prerequisite | MQ3 Completed |
| Offer | `HW-D10` end (Ansel) |
| Target length | 35–45 minutes (one night) |
| Combat share | ~40% |
| Dialogue share | ~10% |
| Watch, pursuit, labour, choice | ~50% |
| Skills | Melee (required) |
| Choices | Smash the winding gear or chain it (2 options) |
| Unlocks | `LM_LOCK_STATE`; flushes stopped through the Lock; Bramblelock pool quieted; *Under the Lamb*, *The Whispering Door*, *What the Flood Carried*; MQ5 |

## C5. The places

### C5.1 Bramblelock Weir [P08]
| Area | Storytelling |
|---|---|
| **W1. The weir** | An overgrown wartime sluice and weir near the orchard ground. Its top is a broken stone walkway. A **weir-pool marker** with a notch stands on the near bank (readable by the TL skill). |
| **W2. The convoy stones** | Squared stones set along the weir wall, each cut with a lot number. Count along them and **one number is missing**: the stone between thirteen and fifteen is blank and newer, set in plain mortar. **Required inspect** in `S00_weir` (sets `NF_LEAD_CONVOY`); Maelin says, as the player passes it, *"Fourteen's missing. Always has been."* This is the first of three main-quest-only deliveries of the Fourteenth Lot (MQ4 stone, MQ9 flow-table wreck scar, MQ11 Lessa). |
| **W3. The watch bench** | A weir-keeper's stone bench with a lantern hook: the "keep watch" interaction. |

### C5.2 The towpath and the Relief Cut [P10]
| Area | Storytelling |
|---|---|
| **T1. Weir walls** | The first chase leg: along the weir top and down the spillway wall. **Agility trigger:** a gap in the weir top (step across). **Walkable fallback:** the footbridge 20 m downstream. |
| **T2. Orchard towpath** | A river towpath under the orchards' dike. A fallen tree crosses it: **agility trigger** (scramble over), **fallback** around by the dike top. |
| **T3. The Cut mouth** | The river bank breaks into a straight, stone-faced channel running away from the river at an unnatural angle, like a ruler laid on a drawing. The towpath runs alongside it. A silt sill at the mouth, with fresh pole-scrapes. A wartime stencil on the facing stone: a sheaf over a wave, and **RELIEF CUT**. |
| **T4. The straight** | Towpath beside the Cut. Silted culverts run under it, mouthing water. Every few hundred paces a wartime mile-stone stands, with numbers. It is too straight, and that is the unease of the place. |

### C5.3 The Hollow Lock [P09]
| Area | Storytelling |
|---|---|
| **L1. The yard** | Walled yard before the sluice-house. A crew shed and a lantern rack with hoods on every lantern. Rope coils, crates, a cookpot still warm. An old chain lies on the gate stones, **cut**, with bright metal at the cut. |
| **L2. The lock chamber** | A stone chamber where barges are worked through. The barge is moored in it at the lower gate. The water churns. |
| **L3. The winding floor** | The sluice-house's upper floor: a great timber-and-iron winding gear, the crank on a platform over the chamber. The gear is **greased fresh**, black and shining. The counterweight is a carved stone (§C8; `SM_STONE_SEEN` variant). |
| **L4. The post store** | A side room off the winding floor: a stack of **new yellow marker posts**, notches already cut, every one a hand high (D-2). A chalk board on the wall lists crossings with ticks (D-2). |
| **L5. The tally room** | A clerk's corner with a strongbox: the **bill of lading** under Board seal (`NF_bill_of_lading`). Flush nights scratched into the beam above it. |
| **L6. The slack gate** | A second, smaller gate in the chamber's flank, silted shut. The silt **bulges outward and is wet on this side**, as if pushed from behind. Someone dug at it and gave up. It is not a crew route. It is the **first visible sign of the fen backwater** (Act II §A2.2): the pressure the Lock used to draw off is already leaning on the old works. Inspect only. |
| **L7. The roof walk** | A parapet over the winding floor, reached by stair after the Lock is closed. At dawn it gives a long view toward Stillwater (§C8.3). |

**MAP VERIFICATION REQUIRED:** the narrative needs only these: the barge passes Bramblelock on the pulse; the Cut's mouth is reachable along the towpath from the weir; the Hollow Lock stands up the Cut toward the fen. How the Cut's route bypasses Crestbridge's tolls (bible §1) is for the zone package to make physically consistent.

## C6. Player-facing sequence

### Beat 0 — The Fifth Night (`S00_weir`)
**Objective:** *Keep watch at Bramblelock Weir.*
The player reaches the weir at dusk (any time; the watch interaction handles the hour). **Maelin** is sitting on the weir wall (`NF-D1`), because Ansel sent word to the crews and she wanted to see what kind of water lifts a post's lie. With `LM_TL_EVIDENCE = riverfolk` she has news: her crews found a second wrong yellow post at Greyharrow Reach. She will watch, and she will not take a boat out on this stretch at night (canon). Ansel is not here; he is walking the fen edge, "where I'm paid to be".
Required before the watch: count the **convoy stones** (W2; `NF_LEAD_CONVOY`; Maelin's pass-by bark `NF-B0.1`). Optional: read the **weir-pool marker** (TL skill: *"Water's under the notch. The crossing reads open."*).

### Beat 1 — Watch (`S01_watch`)
**Objective:** *Keep watch at Bramblelock Weir.*
The **watch bench** interaction: the player sits, the screen does not cut, and the world's time advances in steps while the player stays in control (they can stand at any moment to cancel). Each step is one lantern-fill: Maelin refills the hook lantern, the sky darkens, and the ambient set changes (frogs, a night bird, a fox along the dike).
- With `HW_LEAD_TALLY`, one watch step reaches the hour ("Two and a half bundles. Don't bother before.").
- Without it, two steps, with a **false alarm** in between: a splash and a wake at the far bank that turns out to be a swimming fox with a fish (Maelin: "Not that.").
**Verbs:** wait, watch.

### Beat 2 — The Flush (`S02_flush`) — *the strange moment*
**Objective:** none shown during it (UI suppressed). Afterwards: *Follow the barge.*
The presentation spec is in §C8. In short: the sound of the river drops away until the weir itself is silent. The pool goes glass-flat. Reflections lag. A low thump comes through the stones. Then the surge: the pool lifts a hand over the marker notch in a few breaths, the weir roars doubled, and an **unlit barge** rides the pulse past the player's feet, close enough to hear the sacks creak, crew poling silently and lanterns hooded to slits. Someone aboard is singing under their breath and stops when the barge passes the player. Behind it, the weir pool begins to gather into drift (it doesn't engage; it is weather).
`NF-D2`: Maelin, one line. Then she says the thing the player needs: "Go. I'll get word to the keepers and the Watcher. Go on." The pursuit begins.
**Verbs:** witness.

### Beat 3 — Towpath Pursuit (`S03_pursuit`)
**Objective:** *Follow the barge.*
**This cannot be failed. It can only be lost and found again.**
- The barge moves along a fixed path at a speed between walking and sprinting. Sprinting keeps it in sight.
- Three legs: **weir walls** (T1, agility gap or footbridge), **orchard towpath** (T2, fallen tree or dike top), **the Cut mouth** (T3).
- If the player falls out of sight range, the objective becomes *Find the barge's trail* and trail clues appear on the route: **wake slap** (a wet line high on the bank, still running), **leaked grain** (a sheen of floating grain at the reed edge, a burst sack snagged on a root), **the hooded lanterns** (a slit of light glimpsed through reeds). Each clue the player reaches (enter volume) re-pins the objective forward. The barge itself **waits at the Cut-mouth sill**, where the crew must pole it over the silt (fiction: the pulse is falling and the sill is shallow), so every player catches up there regardless of pace.
- Click-to-move friendly: no input timing. The agility triggers are optional shortcuts.

At the Cut mouth the player sees the barge scrape over the sill and turn into the straight channel. Optional inspect: the **RELIEF CUT stencil** (with `SM_LEAD_STENCIL`: *"The same stencil as the depot chute. Same arrow."*).
**Verbs:** pursue, track, traverse.

### Beat 4 — The Lookouts (`S04_lookouts`)
**Objective:** *Get past the lookouts.*
Two crew lookouts on the Cut-mouth towpath (**NF-E1**), a pole-man and a cutter: the first human enemies in Lowmark. Barks `NF-B4`. Defeated crew **yield** (they go down and stay down; Phase 1.3: no fleeing). They are tied up off the path (no player interaction needed; a crew rope prop).
**Verbs:** fight.

### Beat 5 — Up the Cut (`S05_straight`)
**Objective:** *Follow the Cut.*
A short, quiet walk up the straight (T4) after the fight, with the barge's wake still slapping the stone and the Lock's lit slits ahead. This is pacing, about 60–90 seconds. Silted culverts mouth water at the player's feet. A mile-stone gives the only joke of the walk (inspect: *"A wartime mile-stone. Someone has scratched 'TOO FAR' under the number."*).

### Beat 6 — The Yard (`S06_yard`)
**Objective:** *Get into the Hollow Lock.*
Assault part 1 (**NF-E2**). The yard is dark, and the crew see by hooded lanterns. Optional **environment interaction**: *Pull the hoods* on the lantern rack (2 s channel) to light the whole yard, which makes the crew's ambush pair in the shed visible and stops them getting the first blow. Two groups, fought in either order. The **cut chain** on the gate stones is inspectable (*"The old chain. Cut, not rusted through. The cut is bright."*).
**Verbs:** fight, use the environment.

### Beat 7 — The Winding Floor (`S07_winding_floor`)
**Objective:** *Stop the flush.*
Assault part 2 (**NF-E3**). The stair up from the yard opens onto the winding floor. Across the lock chamber, on the far gallery, a man in a good coat is standing with one hand on the lock-chain: **Gideon Sallow** `[ANTAGONIST]`. He touches the chain before every flush. He is calling the next one (`NF-D5`). He sees the player, and he is delighted rather than afraid ("Look at that! We've got a visitor!"). He sends his crew boss **Rusk** and two crew at the player. Sallow himself is out of reach across the chamber; the gallery is not connected to this side except by the lock gates. The fight is close and loud on the platform around the gear.
After the fight the player may explore the floor before closing it:
- **The greased gear** (inspect, required): *"Greased this week. The old grease under it is the war's."*
- **The post store** (inspect, required, D-2): the yellow posts with pre-cut notches and the chalk crossings board.
- **The bill of lading** (pickup, required, `NF_bill_of_lading`, quest item 2).
- **The counterweight stone** (optional; §C8.2).
- **The slack gate** (optional; the first visible sign of the backwater, Act II §A2.2).

### Beat 8 — Close the Lock (`S08_crank`)
**Objective:** *Wind the Lock shut.*
The crank is a **channelled interaction in three segments** (each 5 s). Damage interrupts a segment, but **completed segments are kept**. The gates close by visible degrees. Between segments (**NF-E4**):
- **Wave 1:** two crew come up the barge stair.
- **Wave 2:** the closing gates churn the chamber, and **drift rises** from the chamber water. This is the first **lantern-drift**: a drift with a cold light at its core that pulses before it lashes. They are place-bound to the chamber walls and reach the crank platform.
- **Wave 3:** the last two crew, plus the drift re-forming (the chamber is still churning; the player knows the rule).

**Sallow's escape** plays during wave 1, across the chamber: he drops down the far stair to a skiff at the lower gate, cuts its rope, and is gone downstream into the Cut's dark. He is cheerful about it (`NF-D6`). He cannot be reached or stopped. The player sees his face and his coat, and that is all.

On the third segment the gates meet with a sound felt in the floor. **The Cut's roar stops.** The silence that follows is ordinary: frogs, wind, the barge creaking. The drift in the chamber sinks into water that is no longer moving and does not re-form. The player has felt the difference between the flush's silence and an ordinary one.

### Beat 9 — The Name (`S09_rusk`)
**Objective:** *Talk to the crewman.*
Rusk has yielded and is sitting against the gear with his hands on his knees (`NF-D7`). He is frightened of the fen, not of the player. He names the man in the coat: Gideon Sallow, the factor, the one who pays. He doesn't know who Sallow answers to ("a name on a bill") and says so. Optional: ask where the crew gets paid. "At the Lamb, in Brookhollow. Back room." This sets `NF_LEAD_LAMB` (UL lead-in).
This is **testimony**, given in conversation after the fight. It is not a creature drop.

### Beat 10 — Smash or Chain (`S10_choose`)
**Objective:** *Decide what to do with the winding gear.*
A physical choice at the gear (§C9.3):
- **Smash it:** pick up the crew's maul (prop) and break the pawl and the drive teeth (3 interactions, loud).
- **Chain it:** take the crew's own chain from the yard (carry state), wrap the crank and the drum, and drive the wedge (2 interactions).
Rusk has a line for either (`NF-D8`).

### Beat 11 — Dawn (`S11_dawn`)
**Objective:** *Watch for the dawn.*
The player climbs to the **roof walk** (L7). The `S11` step plays dawn whenever the player steps onto the walk: the sky greys and the fen comes into view. Maelin's crew skiff comes up the Cut in the first light (she will move at dawn) with **Ansel** in the bow and two keepers behind on the towpath. `NF-D9`:
- Ansel reports, in his book voice, that Bramblelock lay flat at dawn for the first time in a month, and that the fog over Stillwater is **thicker than he has ever seen it**: "the last one stirred it."
- From the roof walk the player can see it for themselves (§C8.3).
- Maelin looks at the posts and says what she thinks of people who lie with posts.
- The keepers take Rusk and impound the posts (and, if chained, the gear).

The quest completes on `NF-D9` end. Act I is over.

## C7. Encounters

Tuned for **Milestone 1 dependable field equipment** (bible §6 level framing).

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **NF-E1** | 1 × smuggler pole-man, 1 × cutter | Cut-mouth towpath | Pole-man: holds the path. Cutter: flanks | **Pole sweep:** plants the pole and leans back (~1.2 s), then a wide sweep that shoves the player back a step (never into water). **Cutter hook:** reverses the hooked knife (~1.0 s), then a heavy cut | First humans: wider telegraphs, smarter spacing | 40–60 s; 60–80% HP remaining |
| **NF-E2** | Group A: 2 × pole-man, 1 × cutter (lantern rack). Group B: 2 × cutter (shed ambush) | Lock yard | Group B ambushes if the hoods are on; if the hoods are pulled, they are visible and engage normally | As E1; ambush: a door creak (~1.0 s) | Environment use; group management | 90–120 s total; groups can be pulled separately |
| **NF-E3** | **Rusk** (crew boss: pole-man variant with more health and a double sweep), 2 × cutter | Winding floor platform | Rusk: anchor. Cutters: pressure | **Double sweep:** two plants and two leans (~1.2 s each), second sweep reversed | Assault climax | 60–90 s |
| **NF-E4** | Wave 1: 2 × cutter. Wave 2: 2 × lantern-drift. Wave 3: 2 × pole-man + drift re-form | Crank platform | Crew: reach the crank; drift: place-bound to chamber walls, re-form ~20 s while the chamber churns | **Lantern-drift:** the core light pulses twice (~1.2 s) before a lash; the light is the tell | Labour under pressure; drift returns as "weather" | 3–4 minutes total. Completed crank segments persist |

**Gideon Sallow** appears only across the chamber in MQ4. **He is not fought here.** His miniboss fight belongs to MQ10 (bible §10). He has no combat definition in this package.

**Rules**
- **Combat never reveals evidence.** Posts, chalk board, bill and gear are found by inspection of the place. Sallow's name is Rusk's testimony after he yields.
- Defeated crew **yield** and are tied (prop). Nobody is executed. Human enemies are knocked down, not killed, in presentation (Lowmark tone). The Gameplay Designer may choose the same death-state as other enemies mechanically, with yield presentation.
- **Death:** respawn at the Cut mouth (T3) once reached, otherwise at the weir. Completed assault groups stay defeated. Crank segments persist. Quest item persists.
- **Co-op:** shared crew and drift. The flush and barge are presented per player from their own `S02` (fallback: shared event if both are on `S01` at the bench; partners on other steps see an empty night). Each partner closes their own Lock in presentation; fallback: shared Lock state, with all present credited.

## C8. The discovery moments: presentation specs

### C8.1 The flush (Beat 2)

Extends *The True Line* §8 language (sound-duck, no music, reflection lag, no UI, player camera) from a dead spot to a whole stretch of river.

| Time | Element | Spec |
|---|---|---|
| 0–3 s | **The drop** | River ambience across the weir area ducks to near silence over 3 s: first the frogs and insects, then the reed hiss, and last **the weir's own roar**. A weir going silent is the moment. The player's footsteps and Maelin's breathing stay audible. |
| 3–6 s | **The flat** | The weir pool goes glass-flat. The lip of the weir shows wet stone with almost no water going over it, as if the river were holding its breath. Reflections on the pool lag the player (TL behaviour, ~10 m radius). |
| ~6 s | **The thump** | One low sub-bass thump, felt more than heard (controller rumble where supported). It is not music. |
| 6–12 s | **The surge** | The pool lifts a hand over the weir-pool marker's notch in a few breaths. The weir's roar comes back **doubled**. Spray. |
| 10–25 s | **The barge** | The unlit barge rides the pulse past the weir bank within ~6 m of the bench: sacks creaking, poles dipping without splashes, lanterns hooded to slits, someone humming who stops. It does not stop or react to the player. |
| 25 s+ | **The gathering** | Behind the barge, the weir pool's surface begins to gather (drift forming: the same tell as the orchard). It does not engage and is not a step. |
| After | **The reading** | The weir-pool marker now reads *"Water's over the notch. The crossing reads shut."* Over the next minutes it falls back under. With `LM_TL_EVIDENCE` any value, the player has seen why someone would want a post that lies about this. |
| UI | No objective popup until the roar has returned and Maelin has spoken. |

### C8.2 The posts and the counterweight (Beat 7)

| Object | Spec |
|---|---|
| **The pre-notched posts** (D-2) [PROPOSAL — DIRECTOR] | A neat stack of new yellow posts, the same pale wood as the Whisperflow liar. Each has its notch already cut, **a hand high** of where a true notch would sit. The player can lift one (carry state) to hold it beside a crossing marker later; this is pure flavour. Inspect text in dialogue file. This **answers D-2 as a proposal**: Sallow's crew made and placed false posts to hide scheduled flushes. It does **not** say who stood at Whisperflow that night. |
| **The chalk crossings board** (D-2) [PROPOSAL — DIRECTOR] | Chalk list: *Whisperflow — ✓. Greyharrow Reach — ✓. Drowsebank tail — .* With `LM_TL_EVIDENCE = riverfolk`, the inspect adds *"Maelin's second post."* |
| **The counterweight stone** | The gear's counterweight is a carved slab: a groove and a notch. It hangs dry in the dark. With `SM_STONE_SEEN`: *"Another one. Like the depot wall. They built the war out of these."* Without it: *"A carved stone, grooved to a notch. It's been used as a weight."* No presentation event: it is just *there*, which is worse. |

### C8.3 The dawn turn (Beat 11)

| Element | Spec |
|---|---|
| Vista | From the roof walk, Stillwater lies toward the fen side. At dawn its fog **sits up like a wall**: tall, still, unmoved by the morning breeze that moves everything else. The Watchers' lantern dots along the fen edge stop at the fog's foot. |
| Audio | Ordinary dawn: birds, wind, the barge creaking. The ordinariness is the contrast. |
| Bramblelock | If the player later visits the weir, its pool is flat and reads under the notch (drift site quieted; no drift tell at dusk). |
| What it means | Stopping the barges did not stop the drift (bible §1 part 2). The player knows a human wrong and sees a water wound get worse in the same breath. Ansel's line carries it. Nothing explains it. |

## C9. Quest structure for implementation

### C9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_weir` | Keep watch at Bramblelock Weir. | Enter weir volume + `NF-D1` end + convoy-stone inspect | Yes | Quest Active from `HW-D10` end. Convoy stones are required (Fourteenth Lot delivery 1 of 3) |
| `S01_watch` | (same) | Watch interaction × 1 (`HW_LEAD_TALLY`) or × 2 | Yes | Cancellable; each step advances the client-side hour |
| `S02_flush` | — (UI suppressed) | Flush presentation complete + `NF-D2` end | Yes | Server event `night_flush.surge`. Barge path starts |
| `S03_pursuit` | Follow the barge. | Enter Cut-mouth volume (T3) | Yes | Trail-clue volumes re-pin objective. The barge waits at the sill until the player arrives |
| `S04_lookouts` | Get past the lookouts. | NF-E1 defeated | Yes | |
| `S05_straight` | Follow the Cut. | Enter Lock-yard volume | Yes | |
| `S06_yard` | Get into the Hollow Lock. | NF-E2 groups A and B defeated | Yes | `pull_hoods` optional |
| `S07_winding_floor` | Stop the flush. | NF-E3 defeated + inspect gear + inspect post store + `NF_bill_of_lading` acquired | Yes | Optional inspects: counterweight, slack gate, chalk board (part of post store) |
| `S08_crank` | Wind the Lock shut. | 3 × `wind_crank` segments complete | Yes | NF-E4 waves; Sallow escape actor on segment 1 start |
| `S09_rusk` | Talk to the crewman. | `NF-D7` end | Yes | `NF_LEAD_LAMB` optional |
| `S10_choose` | Decide what to do with the winding gear. | Smash interactions × 3 **or** chain interactions × 2 | Yes | Sets `LM_LOCK_STATE` |
| `S11_dawn` | Watch for the dawn. | Enter roof-walk volume + `NF-D9` end | Yes | Bramblelock pool → quieted; quest → Completed |

### C9.2 Flags

| Flag | Set by | Read by (here) | Read by (later) |
|---|---|---|---|
| `NF_LEAD_CONVOY` | Convoy-stone inspect (required in `S00`; always set) | `NF-D9.20` option | **MQ11** (Fourteenth Lot line; kept as a flag for variant text, never as a gate) |
| `NF_HOODS_PULLED` | Yard interaction | Barks | — |
| `NF_POSTS_SEEN` | Post-store inspect (required) | `NF-D9` | **MQ10** evidence chip (posts impounded by keepers at dawn in both outcomes) |
| `NF_LEAD_LAMB` | `NF-D7.20` | — | ***Under the Lamb*** opening line |
| `LM_LOCK_STATE` | S10 | `NF-D9` variants | MQ6 crew-route line; MQ10 chip |

### C9.3 Choice: smash or chain

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Smash** (`LM_LOCK_STATE = smashed`): *break the pawl and the drive teeth* | The Lock can never flush again without a new gear. The noise carries down the Cut. | The **mechanism evidence is gone**. The keepers at dawn see a broken machine, not a working one. Maelin: "Good. Now it's only a story." | **MQ6:** Sallow's crew falls back on its only other route (the Drowsebank mill race). **MQ10:** the gear chip is the player's word and the keepers' record of "a broken gear, greased" (weaker). The posts and the bill stand regardless. |
| **Chain** (`= chained`): *wrap the crank and drum with the crew's chain and drive the wedge* | The gear stays intact as evidence. At dawn the keepers inspect a **working, greased mechanism** and log it. | The keepers sit on the chained Lock day and night after dawn, so the crew moves wholly to the mill race. Ansel: "Chains get cut." (a worry; nobody cuts this one). | **MQ6:** the crew-route line mentions the keepers on the chain. **MQ10:** strong chip: a keeper-signed inspection of the working gear. |

**Both** outcomes: flushes stop through the Lock now; Bramblelock pool is quieted; posts and bill are evidence; Stillwater worsens at dawn. Neither is wrong.

## C10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| Flush stopped through the Lock | World change | Bramblelock pool quieted. The Hollow Lock becomes a revisitable site (keeper-watched after dawn; no hostile crew). |
| Relief Cut towpath | Access | A traversal route between the weir and the Lock. |
| Small payment | Currency | Maelin's crew share for "a night on the bank" or a keepers' finder's due (economy tuning). |
| Skill XP | Action only | Melee. |
| Side-quest unlocks | Story | *Under the Lamb*, *The Whispering Door*, *What the Flood Carried*. |
| MQ5 | Story | Act II begins (Ashenstead). |

## C11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player falls behind the barge | Trail clues. The barge waits at the sill. **No failure.** |
| Player stands up mid-watch | Cancels the watch; resuming continues from the last completed step. |
| Player leaves the weir mid-quest before the flush | No failure. The watch can be resumed any night. |
| Logout during pursuit | Restore to `S03`; the player spawns at the weir and the barge is waiting at the sill (trail clues pre-revealed). |
| Death in the Lock | Respawn at the Cut mouth; groups defeated stay defeated; crank segments persist. |
| Walking away | Stays Active; resume prompt at the Lantern Post (Ansel). |
| Fail state | None. |
| Co-op | §C7 note. Each player makes their own smash/chain choice in their own state. The prop presentation follows their own `LM_LOCK_STATE`; fallback: the first choice in the shard sets the visible prop, and the other player's choice is stored and reflected in dialogue only. |

## C12. Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| **Watch interaction** advancing the hour | Systems | Cancellable channel that advances a **per-player presentation hour** (sky, ambient set) without changing world time. The "fifth night" is whichever night the player watches; no world calendar is required. Fallback: a single "keep watch until the second fill" interaction with a fade-free sky change. |
| **Zone-wide ambience duck + scripted water level** | Systems + audio + art | One server event (`night_flush.surge`); client plays the duck, flat, thump, rise, and a level change on the weir-pool water plane and marker reading. |
| **Pathed NPC vessel** (barge) | Systems | A moving prop on a spline with a wait point at the sill. No collision with the player. |
| **Trail-clue volumes** | Systems | Enter-volume events that re-pin objective text. |
| **Channelled segments with persistence** (crank) | Systems | Three-segment interaction; completed segments persisted. |
| **Unreachable actor** (Sallow) | Systems / NPC | Scripted path to skiff; no combat definition in MQ4. |
| **Yield presentation** for human enemies | Gameplay / animation | Defeated humans kneel and are tied (prop swap). |
| Creatures | Schema / Gameplay | Smuggler pole-man, cutter, crew boss (Rusk); lantern-drift. |
| Quest item `NF_bill_of_lading` | Schema | Non-droppable document with inspect text. |
| **Act II seed** | Act II author | The slack gate (L6) is the first visible sign of the backwater (Act II §A2.2). It is not a crew route: after MQ4 the crew's pulses go only through the Drowsebank mill race (MQ6). |

## C13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Who moved the Whisperflow post** (D-2) | Sallow's Lock crew, on Marrick's scheme, to hide a scheduled flush. | Unknown. | Pre-notched posts, the chalk crossings board, the flush timing. | Wynn; the keepers; the river. | Who stood at Whisperflow that night. | MQ10 (Rhosyn, Sallow). |
| **Who Sallow answers to** | Edda Marrick `[ANTAGONIST]`. | — | A Board seal on the bill; "a name on a bill" (Rusk). | The whole Board; Hesketh; Aldric. | The name. | MQ10. |
| **Why the fen got worse** | The last flush dragged heavy water out of the deep pools; with the Lock shut, the pressure has nowhere to go but the old works, and it starts leaking out as the backwater (bible §2.3; Act II §A2.2). | The Watchers' bad luck; the dead are angry. | Fog wall at dawn; Ansel's book; the slack gate's wet, bulging silt. | Closing the Lock was a mistake; the Lock was holding something in. | The Braids; the Fourteenth Lot. | MQ8, MQ9, MQ11. |
| **The missing convoy stone** | The Fourteenth Lot (bible §2.1). | Nothing. | A blank stone between thirteen and fifteen (required inspect); Maelin: "Fourteen's missing. Always has been." | A broken stone replaced. | That a convoy sank. | MQ9 (flow-table wreck scar), MQ11 (Lessa, before the boss). |

## C14. Open decisions

1. **D-2** is answered here as a proposal (posts and chalk board). If the Director chooses otherwise, edit only the post-store inspect texts and `NF-D7.10`.
2. **D-1** — Sallow's name appears in `NF-D5`, `NF-D6`, `NF-D7` (tagged) and on nothing physical. The bill carries the Board seal (swap layer).
3. **Bill of lading buyer.** *Resolved 2026-11-02 (FT-03 approved):* the bill reads "for the account of the Whinstone Store". In v1 it is only a name; nothing in Lowmark says where the Whinstone Store is. Thornfell's TF-M2 reveals it as a Thornfell store-house used by an independent Blood-Oath splinter. No route for the grain is stated anywhere (ruling: do not invent unverified trade routes).
4. **Map and hydrology** of the Cut route (MAP VERIFICATION REQUIRED, §C5.3).

## C15. Internal review log

| Finding | Revision |
|---|---|
| The pursuit first had a fail timer. | Removed. The barge waits at the sill, and trail clues re-pin the objective. Lost and re-found only. |
| Sallow was fought on the winding floor. | Removed. He is MQ10's miniboss; here he is seen across an unbridgeable chamber, and his escape is scripted. |
| Rusk naming Sallow risked being "combat reveals evidence". | Rusk yields, then answers questions. It is testimony, and the bill and posts stand without it. |
| The flush risked reading as a spell. | No glow, no music. It is the water, a thump and a barge. The weir going silent carries it. |
| The smash/chain choice originally made "smash" the clearly better option. | Chain now gives MQ10's stronger mechanism chip; smash ends Lock flushes beyond doubt. Both converge on MQ6 via the mill race. |
| Bramblelock pool and Stillwater both changed with no explanation. | Ansel reports both, as observations. Nothing explains them. |
| Maelin might have joined the pursuit on the water. | Canon: she refuses night passage on specific stretches. She stays and arrives at dawn. |
| Act item budget. | `NF_bill_of_lading` is item 2 of 2. The posts are carry-state flavour; the evidence is a flag and an impound. |
| Agility triggers not yet built. | Each has a walkable fallback (footbridge, dike top). |
| Independent review pass. | The slack gate is no longer a crew route: its silt bulges wet from behind, the first visible sign of the backwater; after MQ4 the crew uses only the mill race. The chained Lock is watched by keepers and its chain is never cut. The convoy stones are a required inspect with Maelin's line, so every player meets the Fourteenth Lot's blank stone. The bill reads sixty-eight measures. |

---

## Act I cross-check (final review)

| Rule | Check |
|---|---|
| Canon anchors | Corvin: numbers, duplicate tallies; the ledger regret is reserved for MQ10. Aldric: polite, knows only the wartime name of the Cut from old compacts. Lessa: "done" path, no explanation. Maelin: no night passage. None receives an invented age, service, kinship, travel, meeting or record custody. Tovin absent. |
| Evidence rule | Slip on a floor; heaps counted; nights from chalk, notches, tally, book; posts, board and bill inspected; Sallow's name by testimony. No drift, stone or flush identifies anyone. |
| No fail, no soft-lock | Every required proof is on the critical path and persistent. No quest can fail. |
| No cutscenes | Glimpse, flush, escape and dawn are world actions under player camera. |
| Solo / co-op | Solo-clearable; per-player state with fallbacks. |
| Movement reality | Click-to-move; agility triggers have walkable fallbacks; no timing-critical input. |
| Quest items | 2 (`SM_requisition`, `NF_bill_of_lading`). |
| Region flags | Only `LM_TL_EVIDENCE` (read), `LM_GRAIN_ROUTE`, `LM_LOCK_STATE` (set). |
| Antagonist tagging | Every node naming Marrick or Sallow is `[ANTAGONIST]` in the dialogue file. |
| Skills | Melee, Woodcutting, Hunting only. No Ranged, Fletching or Mining. |
