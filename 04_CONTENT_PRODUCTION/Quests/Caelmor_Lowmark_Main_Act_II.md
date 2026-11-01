# Lowmark Main Quests 5–9 — Act II: Old Duties, Incomplete Records, Restraint

**Status:** Authored production content for Creative Director milestone review. This package implements Lowmark main-arc **movements 5–9** from `00_ADMIN/Reference/Caelmor_Part5_Lowmark_Main_Arc_Architecture.md`, following the binding slate in `Caelmor_Lowmark_v1_Narrative_Production_Bible.md` (§6 table, §6.1 briefs, §2.6 Sedge, §2.7 Oriel). Everything marked **[NEW]** is authored and is not canon until promoted. **[PROPOSAL — DIRECTOR]** marks a consequential story choice the content is built on. **[CANON]** marks material taken from Phase 1 or the reconciled `LORE/` files. No schema, production JSON or C# is created here.

**Companion file:** `04_CONTENT_PRODUCTION/Dialogue & Narrative/Caelmor_Lowmark_Main_Act_II_Dialogue.md` (Act II cast notes, all dialogue nodes referenced below, barks, inspect texts). The True Line's voice rules (cast file Part 1) are binding.

**Swap tags.** Nodes naming Marrick or Sallow are tagged `[ANTAGONIST]` (bible §3.1). Nodes that depend on Sedge being the Field-Mage are tagged `[D-7]`; nodes that depend on Oriel are tagged `[D-8]`, matching the side-quest packages' convention.

---

## Act II header

### A2.1 Purpose

Act I ends with the barges stopped and Stillwater's fog thicker than ever (MQ4). Act II teaches the second part of the answer (bible §1): **what the scheme used was already broken.** The player learns it with their hands, in five different kinds of place:

| # | Quest | Code | What the player learns | How (core verb) |
|---|---|---|---|---|
| 5 | The Guide-Line | GL | The war rebuilt the land underneath the fields; the water still follows wartime lines. | Trace and excavate a buried channel; a flooded crawl. |
| 6 | Tovin's Floor | TF | A man everyone dismissed was keeping the only record of the water; the pattern is partly human, partly not. | Repair a hazard; reconstruct a pattern on a floor; hold a gate. |
| 7 | What the Ditch Knows | DK | Ordinary household water practice is real, small and lawful, and cannot fix the fen. | Gather for, then defend, a working. |
| 8 | The Mantle | MN | Force spreads heavy water. Someone has been quieting it by hand for years. | Tests of restraint; herd; read stones; watch. |
| 9 | Behind the Falls | BF | The Vale was built to share its water's pressure. The Cut is a scar through that design. | Pilgrimage; explore; work a model of the Vale. |

**Act II turn (movement 9):** the emergency can be stabilized only by combining ordinary repair, civic cooperation, memorial restraint and limited expert practice. Oriel's condition sends the player to Crest Hall for MQ10.

### A2.2 The Act II through-line: the backwater [PROPOSAL — DIRECTOR]

**Author truth.** Closing the Hollow Lock in MQ4 stopped the flushes. It did not empty the fen. The pressure the flushes used to draw off now builds behind the Lock and finds the older ways the war engineers cut through when they dug the Cut: culverts, spurs and severed Braid channels. Every few nights the fen pushes water back out through those ways in a slow surge. Crews call these **backwater nights** [NEW term; "backwater" is the bible's own word in the MQ5 brief]. The surges are getting stronger. The heavy water rides them, so drift turns up wherever they reach.

This is how Act II proves "stopping the barges does not stop the drift" (bible §1.2) without a lecture:
- **MQ5:** the Rebirth Fields still flood from below after the Lock was shut.
- **MQ6:** Tovin's floor sketches show two kinds of wet line. Sharp lines on the race side are the crew's pulses, which are human and run on a schedule. A slow, growing patch at the tail-race door is the backwater, which is not human.
- **MQ7:** the keepers project the backwater from Tovin's dates. The next surge tops the orchard dikes.
- **MQ9:** the flow-table shows why. The Cut ties the fen to everything; only sealing it and spreading the pressure through the Braids ends it (MQ11).

The backwater is physical and patterned. It is pressure, not intent. It never "targets" anyone. If the Director replaces it, MQ5's flooding cause, the tail-door lines in MQ6 and MQ7's lead-in change. Nothing else depends on it.

### A2.3 Order and unlocks

```
MQ4 Completed ──► MQ5 The Guide-Line ──┐
              └─► MQ6 Tovin's Floor ───┴─► MQ7 What the Ditch Knows ─► MQ8 The Mantle ─► MQ9 Behind the Falls ─► MQ10 lead-in
```

MQ5 and MQ6 open together and can be played in either order. Their lines read each other's flags where that helps, and work without them. MQ7 needs both: the calendar from MQ6, and Elspeth Quill at Ashenstead, whom the player meets again in MQ5's village. MQ8 and MQ9 are strictly sequential.

### A2.4 Inputs read

| Input | Source | Read by | Effect |
|---|---|---|---|
| `LM_LOCK_STATE` (smashed / chained) | MQ4 | MQ6 crew talk (`TF-D3`), MQ6 keeper (`TF-D8`) | Why the crew moved to the mill. One line each; no branch. |
| `LM_GRAIN_ROUTE` (escort / hold / split) | MQ2 | Act II ambient barks (Ashenstead, orchards) | Flavor only. |
| `LM_TL_EVIDENCE` | MQ1 | `TF-D8` keeper line | Whether the keepers' record already holds the player's name. |
| `TL_TOVIN_TRUSTED` | MQ1 | `TF-D4` | Tovin hands over the sheets one line sooner. |
| `TL_STONE_PUBLIC` / `TL_STONE_KEPT` | MQ1 | `BF-D4` | One flow-table line about the Whisperflow stone. |
| `TL_LEAD_NAN` (heard the listeners' tune) | MQ1 | Listening Steps inspect | Optional recognition line. The VK side quest owns the payoff. |
| `UR_GATE_RUN` / `UR_LINE_STAKED` / `UR_LEFT` | Side quest *Unreplanted* | `GL-D5` | Changes Joric's framing of the plot option. Never removes it (side-quest contract). |
| First drift site quieted; Ansel's patrol book | MQ3 | MQ8 lead-in | Ansel's book exists and the player has used it. |
| Bryn Ruddock and Elspeth Quill met | MQ3 | `DK-D1`, `GL` ambient | First lines assume acquaintance. |

Act II relies on nothing else from Act I.

### A2.5 Region flags set (bible §9.1)

| Flag | Values | Set by | Read by (owner) |
|---|---|---|---|
| `LM_FIELD_FIX` | circle / plot / dike | MQ5 `S06_choose` | MQ12 Ashenstead; *Unreplanted* epilogue |
| `LM_TOVIN_CREDITED` | named / unsigned | MQ6 `S09_record` | MQ10 chip weight; MQ12 |
| `LM_FLUSH_CALENDAR` | bool | MQ6 `S09_record` | MQ7 lead-in; MQ10 chip |
| `LM_BRYN_ROLL` | commons / household | MQ7 `S06_council` | MQ12 |
| `LM_ORCHARD_LOSS` | none / partial | MQ7 `S05_defend` | MQ12; orchard props |
| `LM_SEDGE_TRUST` | warm / cool | MQ8 `S08_close` | MQ9; MQ11; MQ12 |
| `LM_ORIEL_PROMISE` | aloud / many_hands / return | MQ9 `S07_promise` | MQ12 (quoted back) |

No other region flags are created. Quest-local flags use the quest code. The local flags that other packages read are listed in §A2.8.

### A2.6 Quest items (budget: 2 for the act, bible §11.6)

| Item | Quest | Source | Fate |
|---|---|---|---|
| `tovin_floor_sheets` | MQ6 | Tovin hands over seven loose sketch sheets (`TF-D4`) | Laid on the floor and picked up again in order; given to the keeper at `S09_record` and held in the Keepers' record room (Act III: among the records carried out of the fire in MQ10). |
| `riverglass_bowl` | MQ7 | Ottilie Penner's bench (`S02a_bowl`) | Given to Bryn at `S03_set`; stays with Bryn. |

Everything else is a **carry-state object** (circle stones, turf, beam, softmoss bundle, stake bundle), an interaction prop (spades, pry bar, the shift board, the flow-table gates), or a **loaned tool** handled like the True Line crew hatchet. The act uses 2 quest items, which brings v1 to 3 (MQ1) + Act I + 2.

### A2.7 Drift sites touched (bible §9.2)

| Site (working id) | Quest | Before | After |
|---|---|---|---|
| `drift.drowsebank_race` | MQ6 | Active (forms only during the hold) | **Quieted** at MQ6 completion. The pond is regulated and the gate locked, so the conditions have changed. |
| `drift.orchard_dike` | MQ7 | Active (backwater nights) | Stays **active** after MQ7: the hold saved the orchard, not the water. Found **quieted** overnight at the start of MQ8. Sedge did it, and nobody says so. |
| `drift.mantle_channel` | MQ8 | Active | **Quieted** by Sedge in the demonstration. |

MQ5 and MQ9 have no drift site. The culvert's trouble in MQ5 is flooding, vermin and a predator, not heavy water. The Listening Steps hold the stillest water in the Vale.

### A2.8 Quest-local flags other packages read

| Flag | Set by | Read by |
|---|---|---|
| `GL_SEDGE_SPOKEN` | MQ5 `GL-D3` | MQ8 inspect variant ("cut like the reeds at the Rebirth Fields"); MQ8 `MN-D2` greeting |
| `TF_KEEPERS_READ_BACKWATER` | MQ6 `TF-D8` | MQ7 lead-in notice text (always set at MQ6 end; separate so Act III can cite the keeper's reckoning) |
| `MN_SAW` (water / you / mage) | MQ8 `MN-D7` | MQ9 `BF-D3` (one line); MQ12 optional Sedge line |
| `MN_ELK_KILLED` | MQ8 `S04_elk` | MQ9 Sedge path bark |

### A2.9 Distinctness check

| Quest | Primary verb | Not the same as |
|---|---|---|
| GL | Read a field and dig into it | TL reads a bank and seats a post. GL works under the ground and ends in a land-use decision. |
| TF | Put evidence in order on a floor | MQ3 cross-checks a book. TF reconstructs a sequence by hand from physical sketches and then defends the gate it predicts. |
| DK | Supply and protect someone else's work | MQ1 and MQ3 have the player do the repair. In DK the player cannot do the working and is its guard. |
| MN | Show restraint | The only quest where the player is judged on what they *don't* do. The single "fight" exists to prove fighting is the wrong tool. |
| BF | Pilgrimage and understanding | No investigation and no enemy pressure. The wonder is a model the player operates. |

Combat share by quest: GL ~20%, TF ~25%, DK ~35% (set-piece defense), MN ~5%, BF ~0–5%. That gives the act a combat valley at MN–BF before Act III.

### A2.10 Shared rules for all five packages

- **Level framing:** Competent identity (bible §6; Milestone 2). Exact levels belong to the Gameplay Designer.
- **Death:** respawn at the quest's named safe point with step, flags and items intact. No quest item is lost. No quest can fail.
- **Co-op:** independent instances; shared world creatures give step credit to every participant on that step. Set-piece outcome counters (DK slips, TF gate bands) are per player, from that player's own interactions and NPC.
- **Keep watch:** every "wait for dusk/night" uses one interaction that advances the player's local quest time to the next scripted window (`keep_watch`, as in MQ4). It never waits on real time.
- **No cutscenes.** The camera stays with the player. Every set piece runs with the player in control.
- **Agility triggers** (Phase 1.3, approved, not yet built) always come with a walkable fallback, listed in each package.

---

# MQ5 — The Guide-Line (`GL`)

## GL.1 The quest in one paragraph

On backwater nights the Rebirth Fields at Ashenstead flood from below. Seedlings rot in straight strips, and the Ember-Well runs strange. The Lock is shut and it still happens. Joric Fen knows where the old boundary stones stand because the ploughs have always gone round them. Annelise Reed knows the water rises first inside the remembrance circle. The player waits out a backwater dusk to see where the water comes up, traces the wet line across the field, and digs at three points. Under the field they open a stone-lined wartime channel that once carried water *around* an emergency treatment ground. Inside is a tense flooded crawl: light falling in bars from field grates, the culvert breathing water up to the knee, River Skitters, a Reed Stalker in a collapsed shaft, painted boundary markers, a row of scratched marks nobody can read, and finally a choked iron grate directly under the circle's stones. The fix is the player's choice, and each option asks something of someone: lift the circle (Annelise), cut a ditch through Joric's never-replanted plot (Joric), or build a slow dike around both (a season's planting). At the field edge an old reed-cutter says one sentence about where the water wants to go. Most players walk past him.

**Remember:** light in nine bars through the gaps between the circle stones, seen from underneath. **Want next:** what else the war buried under working land, and who the reed-cutter was.

## GL.2 Canon grounding

| Element | Source | Status |
|---|---|---|
| Ashenstead rebuilt on burned ground; Ember-Well tastes sharper to the grieving; Rebirth Fields begin each season with a remembrance circle; Path of Unburnt Reeds | Dossier §V.3 | [CANON] |
| Joric Fen: burned land never replanted; works neighbours' fields; mends nets at dusk; avoids standing water; "the water gives things back slowly" | Anchors §III | [CANON]. No age, service, kin detail or incident detail is added. |
| Joric can recognize an old field guide-line | Part 3 Lowmark proposal | Proposal, used |
| Annelise Reed: watergarden caretaker; removes offerings before they rot; dislikes unattended candles; knows which names never appear; "light enough to carry" | Anchors §III | [CANON] |
| Movement 5: wartime guide-line or treatment boundary; land altered for emergency care and supply; no imprint identifies a patient or soldier | Main Arc | Approved architecture |
| Reed Stalkers; River Skitters; Ash Hounds; Field Goblins | Dossier §VIII–IX; bible §10 | [CANON] families |
| The culvert (P13), the circle stones, the scratched marks, the stencils, the backwater | This package; bible §4.2 | [NEW] |

## GL.3 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `lowmark.main.05_guide_line` |
| Arc position | Act II, movement 5 |
| Prerequisite | MQ4 *The Night Flush* Completed |
| Offered | On entering Ashenstead (area A) |
| Target length | 30–40 minutes |
| Combat share | ~20% |
| Skills touched | Melee (required); Woodcutting (dike option); Hunting (optional, Ash Hound pelts if the plot option draws them) |
| Choice | The fix: circle / plot / dike → `LM_FIELD_FIX` |
| Quest items | None |
| Unlocks | Dry Rebirth Fields; field guide-lines readable; Sedge seeded; *The Twice-Burned Tree* (bible §7: after MQ5) |

## GL.4 The place: Ashenstead and the Rebirth Fields

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. The green and the Ember-Well** | Arrival | A bucket left on the well lip with the rope still tied. Households carry river water up the lane in yokes. A chalk scrawl on the well cap: *BEASTS ONLY TILL IT SETTLES*. Somebody has added *SETTLES WHAT*. |
| **B. Annelise's watergarden** | Annelise | Reflection pools edged in pale stone. A basket of spent offerings. A hooded lantern hangs on a hook beside the candle shelf, which is empty. The outflow stone of the lowest pool has a fresh silt line a finger above the old one. |
| **C. The Rebirth Fields** | Trace | Communal plots in neat strips. Seedlings have rotted in **straight bands** that cut across the furrows. Rushes grow in a line where no rush should grow. Half the strips have been dug over and re-sown. Twice. |
| **D. The remembrance circle** | The rise | Nine low field stones at the field's low centre, no two alike, each set by a different household (one has a ploughshare mark, one is river-round). A grey ring of silt sits on every stone at the same height. The grass inside is soft underfoot. |
| **E. Joric's plot** | Option 2 | Burned ground at the Flats edge. Charred fence posts. Nets drying on the one sound rail. The corner nearest the field drain has no footprints at all. |
| **F. Field hut** | Tools, watch point | Spade rack, a turf stack, a bench facing the circle. Chalk tallies of re-sowings on the door. |
| **G. Boundary stones** | Trace | Waist-high stones half-sunk in the hedge banks, three visible and more under bramble, each with a faded painted band. The plough furrows bend round each one in a smooth curve, as if the ploughs were taught to. |
| **H. Reed edge** | Sedge | Reeds along the field drain toward the Path of Unburnt Reeds. Cut stems stand in neat bundles, slanted clean. |
| **I. The guide-line culvert (P13)** | The crawl | See §GL.6. |

**MAP VERIFICATION REQUIRED:** the Rebirth Fields lie between Ashenstead and the Ashen Flats edge where Joric's plot sits; the field drain runs toward the reeds and the Path of Unburnt Reeds. The narrative depends only on the circle being at the field's low point and the plot lying lower than the circle.

## GL.5 Player-facing sequence

### Beat 0 — Bad Water at the Well (`S00_arrive`)
**Objective:** *Find out what's wrong with Ashenstead's water.*
Entering area A offers the quest. Barks: households complain about carrying water; a child dares another to drink from the bucket. **Inspect** the Ember-Well bucket (optional): *"Clear. It smells of nothing. The woman beside you says it tastes sharp to some people, and always has."*
**Verbs:** explore.

### Beat 1 — Two Who Know the Field (`S01_ask`)
**Objective:** *Ask the watergarden keeper and the net-mender about the fields.*
- **Annelise** at the watergarden (`GL-D1`). The water comes up first inside the circle. It started at the end of last season, and it came again last week, after the Lock was shut. She has moved offerings off the circle stones three times.
- **Joric** at the field edge, mending a net on the rail (`GL-D2`). He knows where the old boundary stones stand. "Ploughs go round them. Always have." He won't walk on the wet ground and doesn't say why. He will point.
Completes when both conversations reach their end nodes, in either order.
**Verbs:** talk (short).

### Beat 2 — Backwater Dusk (`S02_dusk`) — *the strange moment*
**Objective:** *Watch the fields at dusk.*
At the field-hut bench the player uses **Keep watch** and time advances to dusk. Then, under the player's control:
1. The field goes quiet and the rooks settle.
2. A thin film of water wells up **inside the circle** first and spreads outward. Then a pale wet line glistens across the field in a dead-straight run between two of Joric's boundary stones and on toward the hedge. It lasts about 90 seconds.
3. **Steam rises from the Ember-Well mouth** on the green, visible from the field in the cold air. If the player goes to it (optional, `S02b_well`), the bucket water is **warm as a hand**. A household member at the well: *"That's never happened."*
During the 90-second glisten the player can inspect the line at any of three points (optional; gives an early trace credit). If they miss it, the traces stay visible in the morning.
Annelise comes to the circle's edge during the dusk and stands with the player. She does not go in. Joric is nowhere near the water.
**Verbs:** watch, observe.

### Beat 3 — Read the Field (`S03_trace`)
**Objective:** *Trace where the water runs under the field.*
Four inspect points, any order; three are required:

| Point | Inspect text (summary; full text in dialogue file) |
|---|---|
| The rush line | Rushes growing in a ruler-straight line across three strips. "They need wet feet. They found some." |
| The sunken furrow | A shallow dip running the same line; the ground has settled over something long and narrow. |
| The circle's soft ground | The grass inside the ring gives like a sponge; water beads up under the boot. |
| Joric's stones | The line runs exactly between two boundary stones and on toward a third in the hedge. Painted bands, faded: an old ring sign. |

If the player brings Joric to the stones (talk to him while near area G), he walks the line with them and stops a stride short of the wet ground every time (`GL-D2` branch, sets `GL_JORIC_WALKED`): *"That's a guide-line. We kept the plough to it. Nobody said what it guided."*
**Optional:** the reed-cutter at area H (`GL-D3`, `[D-7]`). See §GL.5 Beat 3b.
**Verbs:** investigate, read the land.

### Beat 3b — The Reed-Cutter (optional; `S03b_sedge`) `[D-7]`
An old man cuts reeds at the field drain with a short sickle held low. He has no marker, no name over his head (standard role-based nameplate: "Reed-cutter") and no quest icon. If spoken to, he says **one sentence** about the water and goes back to work: *"It wants to go round. It always did."* Further interaction plays only a gesture: he keeps cutting. Sets `GL_SEDGE_SPOKEN`. If the player never speaks to him, nothing is lost. His slanted cut stems at area H are inspectable either way: *"Cut low and clean, at a slant. Somebody who does this every day."*

### Beat 4 — Open the Field (`S04_dig`)
**Objective:** *Dig where the line runs.*
Three dig points along the traced line, each marked by a **field-crew spade** stuck in the ground (interaction prop; nothing enters inventory). Each dig is a 3 s channel, twice, then a 3 s **clear**.

| Dig | Find | Effect |
|---|---|---|
| **Dig 1, on the rush line** | Dressed capstones, mortared, with dark water gurgling under a gap. | "Stone. Laid. Somebody built this." |
| **Dig 2, at Joric's middle stone** | The boundary stone runs deep, and its buried face carries a stencil under the paint band: **KEEP DRY WITHIN THE STONES**, and below it an arrow pointing along the line. | The treatment boundary is revealed. Annelise's line in `GL-D4`. |
| **Dig 3, by the hedge** | An inspection shaft with iron rungs going down into the dark. Water sound. | **Encounter GL-E1**: River Skitters boil up out of the opened shaft. |

After the third dig, a short exchange at the shaft (`GL-D4`) with Annelise and the field crew. Joric arrives and stands back: *"Ground was used for something. Before it was ours again."* Nobody says more than they know.
**Verbs:** dig, fight.

### Beat 5 — The Crawl (`S05_culvert`)
**Objective:** *Follow the channel under the field.*
See §GL.6 for the crawl's sections, tension rules and encounters. Completes on reaching the grate chamber and inspecting the **grate**, the **cap above** and the **side culvert** (three inspects).
**Verbs:** traverse, fight, investigate.

### Beat 6 — What Gets Moved (`S06_choose`)
**Objective:** *Decide how to free the water.*
Back up the shaft (or out through the same way; the crawl is one-way in feeling only). At the circle, Joric and Annelise are both present. `GL-D5` puts the three fixes on the table. Two of them need someone's agreement, and the player has to **ask** for it:

| Fix | What it needs | Who must agree |
|---|---|---|
| **Clear the grate from beneath the circle** | Lift the three circle stones that sit on the old shaft cap; open the cap; go down and clear the grate; set the stones back. | **Annelise.** She agrees when asked, on her condition: every stone goes back in its own place, the same way up. |
| **Cut a relief ditch through Joric's plot** | Dig a ditch across the burned plot to break into the side culvert and lead the backed water to the Flats drain. | **Joric.** He decides himself. If the player *tells* him it's sensible instead of asking, he says to ask him properly; the option stays open (`GL-D5.40`). *Unreplanted* flags change how he frames it. |
| **Build a slow dike round both** | Cut stakes, carry turf, raise a low dike that leads the seep around the circle and the plot to the field drain. | Nobody's ground is touched. **Cost:** extra labour now, and the Rebirth Fields lose a season's planting while the dike takes the low strips and the ground drains. The field crew says so plainly. |

The choice sets `LM_FIELD_FIX` and is final for this quest.
**Verbs:** choose.

### Beat 7 — The Work (`S07_fix_circle` / `S07_fix_plot` / `S07_fix_dike`)
**Objective (varies):** *Lift the circle stones and clear the grate.* / *Cut the ditch through the plot.* / *Raise the dike.*

**Circle.** Annelise chalks each stone's outline and an arrow for which face is up. The player lifts three stones (carry state; set down on the chalked cloth Annelise spreads). Open the cap (3 s channel ×2: rust and turf). Below, the grate chamber is half full and sunlight comes straight down the shaft for the first time. Clear the grate: three 3 s channels with the crew's **pry bar** (interaction prop), pulling out rotted sacking, a tangle of wire and the broken top of a boundary marker. **GL-E4a**: Skitters stirred up from the silt. On the third clear, the backed water drops away with a long sigh down the main channel. Carry the three stones back. Each must be set on its chalk outline, and the set-down interaction checks the facing. Set wrong, Annelise says *"Other way up"* and the player turns it (one extra interaction; no fail).

**Plot.** Joric runs a net cord along the line he wants. It is not the shortest: it avoids the corner he never walks. Three ditch lengths (3 s channel ×2 each) through burned ground; one charred post must come out (Joric: *"Leave the next one."*). Clearing the scrub at the second length disturbs a den: **GL-E4b**, Ash Hounds. The last length breaks into the side culvert. Water runs out into the new ditch, dark, then clearing.

**Dike.** The field crew foreman marks the course with stakes from the hut. The player cuts **four stakes** from the ribboned hedge stools (Woodcutting, entry level, managed stools only, as in MQ1) and carries **four turf sods** from the stack (carry state). Raising four dike sections takes a 3 s tamp channel ×2 each. Between sections three and four, night falls (scripted keep-watch prompt). **GL-E4c**: Field Goblins come for the tool pile, and a trapper sets rake traps (visible, avoidable). The last section is tamped at first light.

**Verbs:** carry, dig, fight; Woodcutting (dike).

### Beat 8 — The Next Backwater (`S08_test`)
**Objective:** *Watch the water come up again.*
Keep watch at the bench to the next backwater dusk. The water comes, and goes where the fix sends it:
- **Circle:** the wet line glistens and then **sinks**; the shaft breathes once, audibly; the circle stays dry. The silt ring on the stones is the last one.
- **Plot:** the water runs in the new ditch across Joric's ground in a bright line in the dusk. Joric watches it from the rail, a long way back.
- **Dike:** the water stands in the low strips behind the dike like a long mirror and runs along its foot to the drain. The circle and the plot are dry. The re-sown strips are under water for the season.

The Ember-Well does not steam. If the player touches the bucket, it is cold (`S08b_well`, optional): *"Cold again. Whatever it was has gone back down."*
**Verbs:** watch.

### Beat 9 — Dawn at the Circle (`S09_close`)
**Objective:** *Speak with Joric and Annelise.*
`GL-D8`. Short and variant by fix. Completes the quest.

### Completion
Quest → Completed. `LM_FIELD_FIX` persists. The Rebirth Fields' presentation changes per fix (§GL.10). Boundary stones across Ashenstead Fields become inspectable as "guide-line" stones (knowledge reward).

## GL.6 The culvert crawl (P13): sections and tension

The crawl must feel **tight, wet and listened-to**. Its tension comes from sound, narrowing space and water that rises and falls on its own, never from a timer or drowning damage.

| Section | Space | Tension device | Encounter |
|---|---|---|---|
| **I1 Entry shaft** | Iron rungs down 4 m into a stone channel | The field noise cuts off overhead. Use-rungs interaction moves the player down; agility trigger optional. | — |
| **I2 The long run** | Knee-deep, head-high stone channel; light shafts every ~10 m from field grates | Bars of daylight. Footsteps of the field crew overhead, then gone. Water is cold, ankle to knee. | **GL-E2** Skitters |
| **I3 The low run** | Ceiling drops to just over head height for ~25 m; agility trigger "stoop-through" (fallback: walkable at standard speed with a low ceiling, no camera change) | **The culvert breathes.** A long gurgle sounds from ahead (the telegraph, ~3 s), then the water rises a hand over ~6 s, holds ~10 s, and falls back. It happens twice while the player is inside I3, never as damage. While it is high, Skitters can reach the side ledge. The light-shaft reflections shiver on the ceiling. | Skitter stragglers |
| **I4 Marker chamber** | Wider vault where two channels meet | Painted boundary markers (stone posts with the ring sign), a stencil **CLEAN WATER — THIS SIDE**, a row of iron hooks, a washed-in bottle, bandage pins in the silt. In a niche, **rows of scratched marks**, some shaped like letters, worn too far to read (`GL_MARKS_SEEN`). No light shaft: the only light is the next shaft's glow. | — |
| **I5 Reed shaft** | A collapsed field drain where reeds grew down into the culvert in a dark green curtain | The reeds hang to the water. One sways when nothing else does. | **GL-E3** Reed Stalker ambush |
| **I6 Grate chamber** | Under the circle | An iron grate across the channel, choked to the top bar. Backed water rises up a side culvert toward the circle. Above, a capped shaft: **light falls in nine thin bars** through the gaps between the circle stones on the cap. Inspects: the grate ("Set from above. Whoever fitted it came down through the cap."), the cap ("Stones sit on it. You can see their shadows."), the side culvert ("Runs low, toward the Flats. Under the burned plot."). | — |

**Rules.** No step needs the player to fight while the water is high; the rises are atmosphere and spacing. The culvert stays open after the quest as an explorable space (Skitters respawn as ordinary vermin; the stalker does not). Respawn point while inside: the top of the entry shaft.

**Evidence boundary.** Nothing in the culvert identifies anyone. The scratched marks are physical marks that cannot be read; no presentation reads them for the player, and no NPC claims to know whose they are. Nothing "remembers" here; this is a drain.

## GL.7 Encounters

| Id | Enemies | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **GL-E1** | 2 swarms of River Skitters | Shaft mouth on Dig 3 | Aggressive; leashed to wet ground around the shaft | Swarm hiss and a ripple toward the player (~0.8 s) | A warm-up that says "it's wet down there" | Required. ~20 s; minor damage |
| **GL-E2** | 3 Skitter swarms + 1 latcher | I2 long run, water volume | Leashed to water; latcher grabs the ankle | Latcher rears from the water (~1.2 s); latch breaks on stepping to the ledge or two hits | Spacing in a corridor; the ledge as safety | Required. Ends at 60–80% HP |
| **GL-E3** | 1 Reed Stalker (stalker) + 1 Reed Stalker (lurker) | I5 reed shaft | Stalker: ambush from the reed curtain, then melee. Lurker: submerged; surfaces to bite when the player stands in deep water | Stalker: the reed curtain parts and its throat bulges with a low croak (~1.2 s) before a leap. Lurker: a line of bubbles toward the player (~1.5 s) | **First Reed Stalkers** (bible §10). Teaches that reeds hide things and that the dry stones are the safe footing | Required. 45–70 s. The player who reads the croak takes one hit, not three |
| **GL-E4a** | 2 Skitter swarms | Grate chamber (circle fix) | As E2 | As E2 | Keeps the work physical | Required on the path |
| **GL-E4b** | 2 Ash Hound runners + 1 ash-shaker | Joric's plot scrub (plot fix) | Pack: runners flank; shaker hangs back | Shaker shakes its coat (~1.5 s) and an ash cloud forms; standing in it chokes (minor DoT); step out | Burned-ground danger on burned ground | Required on the path. ~60 s |
| **GL-E4c** | 2 Field Goblin scrappers + 1 trapper | Field-hut tool pile at night (dike fix) | Raiders target the tool pile, then the player | Trapper sets rake traps (visible rake heads in the grass, ~2 s set animation); scrappers wind up overhead swings (~1 s) | The extra labour costs a night | Required on the path. ~50 s |

Combat never reveals evidence. Nothing a creature drops advances the quest.

## GL.8 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_arrive` | Find out what's wrong with Ashenstead's water. | Enter area-A volume | Yes | Quest Uninitialized → Active (auto-accept) |
| `S01_ask` | Ask the watergarden keeper and the net-mender. | `GL-D1` and `GL-D2` end nodes reached | Yes | Any order |
| `S02_dusk` | Watch the fields at dusk. | `keep_watch` at field-hut bench → dusk window event `gl.backwater_dusk` ends | Yes | Fires the steam/warm-well presentation |
| `S02b_well` | (Optional) Touch the well water. | Inspect `ember_well_bucket` during the dusk window | No | Sets `GL_WELL_WARM` |
| `S03_trace` | Trace where the water runs. | 3 of 4 trace inspects | Yes | Glisten-window inspects count |
| `S03b_sedge` | (Optional) Speak to the reed-cutter. | `GL-D3` end node | No | Sets `GL_SEDGE_SPOKEN` `[D-7]` |
| `S04_dig` | Dig where the line runs. | 3 `dig_clear` interactions complete + GL-E1 defeated | Yes | Dig 3 spawns E1 |
| `S05_culvert` | Follow the channel under the field. | Inspects: `grate`, `cap`, `side_culvert` in I6 | Yes | E2, E3 on route; `GL_MARKS_SEEN` optional |
| `S06_choose` | Decide how to free the water. | `GL-D5` fix node resolved | Yes | Sets `LM_FIELD_FIX` |
| `S07_fix_*` | (Varies.) | Circle: 3 stones lifted + `open_cap` + 3 `clear_grate` + 3 stones reset. Plot: 3 ditch lengths + post removed + `break_culvert` + E4b. Dike: 4 stakes acquired → deposited + 4 turf deposited + 4 sections tamped + E4c | Yes | Exactly one branch is active |
| `S08_test` | Watch the water come up again. | `keep_watch` → `gl.backwater_test` window ends | Yes | Presentation per fix |
| `S09_close` | Speak with Joric and Annelise. | `GL-D8` end node | Yes | Quest → Completed |

## GL.9 Flags

| Flag | Set by | Read by |
|---|---|---|
| `LM_FIELD_FIX` = circle / plot / dike | `GL-D5` | MQ12; *Unreplanted* epilogue; field presentation |
| `GL_JORIC_WALKED` | `GL-D2` stones branch | `GL-D8` Joric variant |
| `GL_WELL_WARM` | `S02b_well` | `GL-D4` Annelise line; `GL-D8` |
| `GL_MARKS_SEEN` | I4 niche inspect | `GL-D5` (an option to tell Annelise) |
| `GL_SEDGE_SPOKEN` | `GL-D3` | MQ8 (§A2.8) |
| `GL_JORIC_ASKED_BADLY` | `GL-D5.40` | `GL-D5` re-ask line only |

## GL.10 Choices and consequences

| Fix | Immediate | Cost | Later |
|---|---|---|---|
| **Circle** — *"Lift the stones and clear it from underneath."* | Fields dry this season; grate clear; shaft capped with a new lid and the stones reset on chalk. | The circle has been moved, even if only for a day. This season's remembrance circle is held on ground that was opened. Some households are uneasy (barks). Annelise carries the weight of having agreed. | MQ12: the circle stands, and Annelise has scratched a tiny chalk arrow under each stone "so the next person knows which way up." Ashenstead barks treat the lifting as something done properly. |
| **Plot** — *"Run a ditch through Joric's ground."* | Fields dry this season; water runs in a new ditch across the burned plot to the Flats drain. | Joric's unworked ground now does work, whether or not he ever plants it. Water runs through the place he avoids, though not the corner he never walks. | MQ12 and *Unreplanted* epilogue: the ditch is lined with stones Joric chose; the net rail stands beside it. Joric still never walks the far corner. |
| **Dike** — *"Build round both. Touch nobody's ground."* | Circle and plot untouched; water led round to the drain. | A night's extra labour and a goblin raid; the re-sown low strips are lost for a season; households go short of a planting (barks; Ashenstead buys in seed). | MQ12: the low strips are back in crop, and the dike has a path worn along its top. Both Joric and Annelise say the same short thing about it. |

No option is wrong. Each touches a value: Annelise's belief that remembrance should be **light enough to carry** (stones carried here can be carried again, and put back), Joric's right to **decide about his field himself**, and the community's willingness to **pay in time** rather than ask either of them.

## GL.11 Rewards

| Reward | Type | Notes |
|---|---|---|
| Dry Rebirth Fields | World change | Presentation per fix |
| Guide-line reading | Knowledge | Boundary stones with the ring sign across Ashenstead Fields become inspectable: *"A guide-line stone. Something under here was kept dry."* |
| Field share | Small payment | From the Ashenstead field crew; amount set in economy tuning |
| Skill XP | Actions only | Melee; Woodcutting (dike); Hunting if Ash Hounds are harvested |

## GL.12 Failure, recovery, co-op

| Situation | Handling |
|---|---|
| Death in the culvert | Respawn at the top of the entry shaft; step and flags kept |
| Logout mid-crawl | Resume at the entry shaft; inspects done stay done |
| Logout mid-fix | Carried stone/turf returns to its source; completed sections stay complete |
| Missed the dusk glisten | Morning traces remain inspectable; nothing missed is required |
| Stone set wrong way up | Annelise's correction line; turn and re-set |
| Co-op | Each player's fix is their own. Field presentation is per player (fallback: show the dike state to everyone, carry the others in dialogue; §A2-INT) |

## GL.13 Integration needs (beyond §A2-INT)

| Need | Minimum form |
|---|---|
| Timed dusk window with presentation (`gl.backwater_dusk`) | Water-film decal spreading from the circle; glisten line; steam particle at the well; warm-bucket inspect variant valid only during the window |
| Culvert "breathing" water volume | Water-volume height animated in two steps on a script during I3 occupancy; telegraph audio first |
| Light-shaft bars through the circle stones | Static lighting in I6; no state |
| Carry-state facing check (circle stones) | Set-down volume validates rotation within tolerance; else play `GL-D6.12` and keep the stone carried |
| Per-fix field presentation | Three prop/terrain-decal sets keyed on `LM_FIELD_FIX` |

## GL.14 Mystery ledger

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| What the Rebirth Fields were in the war | Emergency treatment and supply ground; the culvert carried water around it to keep it dry and fed clean troughs. | "Always fields"; the circle marks the first planting after the burning. | Stencils, markers, hooks, pins, the guide-line Joric's ploughs kept to. | A mass grave; a cursed field. | Who was treated there; who died; who carved the marks. | Nobody in v1; independent records only (Part 5 lattice L-S18 pattern). |
| The scratched marks | Marks made by people in the culvert during the war; unreadable. | — | The niche. | They are names of the dead and can be read by the water. | Everything. | Not revealed. |
| The warm well | Unexplained. Compatible with backed fen water moving under the green. | "Never happened." | Steam; warm bucket; cold after the fix. | The well is grieving. | Cause. | Not revealed in v1. |
| The reed-cutter | Sedge, the Last Field-Mage (D-7). | An old cutter. | One sentence; clean cuts. | — | Everything. | MQ8 (never confirmed aloud). |

## GL.15 Open decisions

1. **Backwater author truth** (§A2.2). *Recommendation: approve.* It is the act's spine.
2. **Treatment-ground history.** The quest shows emergency care and supply use with no date, unit or side named. *Recommendation: keep it unnamed in v1* (Main Arc movement 5; Part 4 ledger).
3. **The nine circle stones each set by a household** is a [NEW] memorial detail. *Recommendation: promote with Ashenstead.*

## GL.16 Internal review log

| Finding | Revision |
|---|---|
| First draft let the scratched marks be "almost readable" with a lagging reflection over them. That made an effect point at the dead. | Removed. The marks are simply worn; no effect plays in I4. |
| Joric walked into the culvert in one draft. That contradicts canon (avoids standing water). | Joric never enters water. He walks the line to the wet edge and stops, which shows character through action. |
| Joric's agreement was gated by a dialogue "right answer" that closed the plot option. | Telling instead of asking now gets "ask me properly" and the option stays open. He decides; the player can't lose the option by phrasing. |
| An invented line had Joric naming who he lost. | Cut. He says only what canon allows: the water gives things back slowly. |
| The dike option was free of cost, so it dominated. | It now costs a night, a raid and a season's planting, stated by the crew before the choice. |
| The culvert had a rising-water damage timer. | Replaced with telegraphed, non-damaging rises that change spacing. Tense without punishment. |
| Sedge had three lines. | One sentence, then a gesture. Players may miss him entirely. |

---

# MQ6 — Tovin's Floor (`TF`)

## TF.1 The quest in one paragraph

Miller Imber Cobb has chalked a notice on the Brookhollow dock post: **MILL RUNNER WANTED — DROWSEBANK — STEADY HANDS.** The runner he means to replace is Tovin Pell. Tools move overnight, the floor is wet in the mornings, and Tovin "sees things." The player turns up about the job and finds Tovin packing. First the demonstrable hazard: the mill-race gate's paddle is cracked and its strap bent. The player lowers a seasoned beam on the mill hoist, cuts a new board, re-forges the strap or straightens it with Imber, and seats it. A night watch from the beam loft explains the tools. Two of Sallow's crew come in by the tail door, use the hoist, borrow the long bar, try the gate and swear at the new pin. Then Tovin, asked directly, hands over seven loose sheets: the floor, drawn on the mornings it was wet. The player lays them on the mill floor in order using the wet-line evidence and works out the crew's pulse cadence from Tovin's shift tallies. The next pulse is tonight. The set piece is holding the race gate shut while the crew winds from the far bank and pries the pawl from this side, with drift rising out of whatever water gets through. Afterward, in the quiet, the mill-pond reflections lag behind the lanterns. Tovin sees it too and doesn't name it. At dawn a keeper writes the calendar into the record, with Tovin's name on it or without.

**Remember:** seven sheets on the floor in a row, each with one more stain line than the last. **Want next:** what the second set of lines, the ones coming up from below, means for the orchards.

## TF.2 Canon grounding

| Element | Source | Status |
|---|---|---|
| Tovin Pell: dock laborer and mill runner; reflections that lag; tools moved; water sounds without current; sketches mill floors; assumes something is wrong with him; never names, never seeks answers | Anchors §IV | [CANON]. Guarded: he describes, never explains, never solves. |
| Movement 6: fix the demonstrable hazard first; Tovin becomes a credible observer, not a mage or savant; the pattern is partly ordinary | Main Arc | Approved architecture |
| L-S14 *Pell's Floor Plan*: humane work response; sketches preserved without declaring cause | Part 5 lattice | Folded into this main quest (bible §6) |
| Drowsebank Mill: inconsistent repairs; altered gearing; Tovin's sketches explain a repair sequence | Part 3 proposal | Proposal, used |
| Dwarven engineers fortified mills in the war | Dossier §II | [CANON]; basis for the Drowse spur |
| Imber Cobb, the crew route, the sheets, the calendar, the Drowse spur | Bible §5.3; this package | [NEW] |

## TF.3 Summary card

| Field | Value |
|---|---|
| Content id | `lowmark.main.06_tovins_floor` |
| Arc position | Act II, movement 6 |
| Prerequisite | MQ4 Completed (parallel with MQ5) |
| Offered | Reading the dock-post notice in Brookhollow, or entering Drowsebank's yard |
| Target length | 35–45 minutes |
| Combat share | ~25% |
| Skills touched | Melee (required); Smithing (optional path, entry level); Cooking (optional, night meal) |
| Choice | Credit Tovin by name or submit unsigned → `LM_TOVIN_CREDITED` |
| Quest items | `tovin_floor_sheets` |
| Unlocks | `LM_FLUSH_CALENDAR`; Drowsebank race quieted; the mill-smith's anvil usable; MQ7 (with MQ5) |

## TF.4 The place: Drowsebank Mill (P11)

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Mill yard and pond bank** | Arrival; the strange moment | A broad, still pond behind the mill. Ducks avoid the corner by the race gate. A bench where Tovin eats alone, facing the water. |
| **B. Ground floor** | Puzzle floor | Two millstones; a hoist trap with chain; seven **sack bays** chalk-numbered 1–7 along the race-side wall. A **tool rack with painted outlines** (Imber painted them so he could see what goes missing); three outlines are empty. Faint **stain lines** on the race-side boards, one above another, like tide marks. A **shift board** by the door: chalk strokes in fives. |
| **C. Race and race gate** | Repair; hold | A wooden paddle gate in an iron frame between pond and race, raised by a **rack and two cranks**: a near crank on the mill side and a far crank across a narrow footbridge on the pond bank. Painted bands on the paddle post (Imber's height marks). The bottom board is split; one strap is bent; the pawl has **bright fresh scars** where something pried it. |
| **D. Tail race and tail door** | Crew entry; backwater | The tail race runs out under the mill into an older channel of dressed stone with iron rings, much better built than the mill. The tail door's lower step has a **damp patch** that isn't from the race side. |
| **E. Beam loft** | Watch point; timber | Seasoned beams on trestles. A gap between floorboards gives a clear view of the floor and the gate. Tovin's sheets were drawn from here. |
| **F. Mill-smith's corner** | Smithing | A small hearth and anvil for pins and straps. Mills keep one. (**POI VERIFICATION:** confirm with the Zones package.) |
| **G. Pond far bank and spill boards** | Crew work | The pond's old spill weir with wooden boards slotted in. Someone has added two extra boards so the pond can be held high. |
| **H. The Drowse spur** | Context | Downstream, the dressed channel joins a straight wartime spur toward the Relief Cut below Crestbridge. **MAP VERIFICATION REQUIRED:** the narrative needs only "the tail race can reach the lower Cut by a wartime spur." |

## TF.5 Player-facing sequence

### Beat 0 — Runner Wanted (`S00_notice`)
**Objective:** *Ask at Drowsebank about the runner's job.*
The dock-post notice in Brookhollow (inspect) or simply walking into Drowsebank's yard starts the quest. Dock barks (`TF-D0`) say plenty: *"Cobb's letting Pell go."* *"About time, he's touched."* *"He's the only one who turns up sober."*

### Beat 1 — Tools, Floors and Seeing Things (`S01_imber`)
**Objective:** *Talk to the miller.*
`TF-D1`. Imber is gruff, embarrassed and decided: tools moved, floors wet, the gate cracked, and Tovin "seeing things." Tovin is wrapping his own tools in sacking at the bench and doesn't look up. If the player asks for the job, Imber says it's theirs if they can fix the gate. If the player asks *what if it isn't him*, Imber says: *"Then show me what it is. Start with the gate."*
**Verbs:** talk.

### Beat 2 — Look at the Gate (`S02_inspect`)
**Objective:** *Examine the race gate and the tool rack.*
Four inspects, all required: **split board** ("split along the grain from the bottom: forced upward against the water, not rotted"), **bent strap**, **pawl scars** ("bright. Metal on metal. Days old, not years."), **tool rack** ("Three empty outlines: the long bar, the race key, a hoist hook. The hook is on the floor by the trap, not where anyone works."). An optional fifth, the **stain lines** on the boards, counts the lines (seven old ones plus a fresh damp one) and pays off in Beat 6.
**Verbs:** investigate.

### Beat 3 — Mend the Gate (`S03_repair`)
**Objective:** *Repair the race gate.*
1. **Lower a beam** from the loft on the mill hoist (`hoist_lower`: 3 s channel at the loft hatch; the beam swings down to the floor). This is the hoist the crew uses; the player's hands learn it.
2. **Cut the board** at the saw horse (3 s channel ×2).
3. **The strap**, two ways:
   - **Smithing:** heat and straighten the strap at the mill-smith's anvil (station interaction; entry-level Smithing action; XP from the action).
   - **With Imber:** if the player has no Smithing or declines, Imber clamps it in the vice and the player leans on the bar while he hammers (3 s channel ×2). *"Lean. More. That's it."*
4. **Seat the board and strap** at the gate from the footbridge (3 s channel ×2). **TF-E1**: Skitters in the race shallows harass the player at the footbridge. Light.
Imber fits a new **lock pin** through the pawl and pockets the key. *"Gate's sound. That's one thing."* (`TF-D2`)
**Verbs:** carry, craft (optional Smithing), repair.

### Beat 4 — Night in the Loft (`S04_watch`)
**Objective:** *Watch the mill tonight.*
Imber goes home. Tovin goes home. The player climbs to the loft gap and uses **Keep watch** → night. Under player control:
1. The tail door opens. Two crew with hooded lanterns come in talking (`TF-D3`, positional, `[ANTAGONIST]`). Their talk plays **before** they reach the gate, so no player action can cut it short. They name their master, say why they've come to the mill (an `LM_LOCK_STATE` variant), and say they'll pull the gate *tomorrow night* "pin or no pin."
2. They take the long bar from the rack, drop the hoist hook to haul a line from the tail race, try the near crank, find the pin, and swear.
3. They leave the bar by the trap and go out the way they came.

If the player drops down and engages (`S04b_fight`, optional) at any point after the key lines, **TF-E2**: the two crew fight. Defeated, they're down and stay down; Imber ties them at dawn and the keepers collect them. Fighting gains nothing for the investigation and loses nothing.
Completes when the crew's scene reaches its end (they leave) or both are defeated.
**Verbs:** watch; optional fight.

### Beat 5 — Morning, and the Sheets (`S05_sheets`)
**Objective:** *Tell the miller what you saw.*
`TF-D4` at dawn. Imber hears it and goes quiet. The tools are explained. *"And the wet floors? He draws them."* Imber calls Tovin over. Tovin, **asked directly** (canon), takes a fold of loose sheets from his tool sacking: the floor from the loft gap, on mornings it was wet. Seven sheets, out of order, two of them torn from different books. Gives `tovin_floor_sheets`. If `TL_TOVIN_TRUSTED`, Tovin hands them over a line sooner and says he kept them "in case you came."
**Verbs:** talk.

### Beat 6 — Lay Out the Floor (`S06_calendar`) — *the puzzle*
**Objective:** *Lay Tovin's sheets on the floor in order.*
The player lays the seven sheets in the seven chalked **sack bays** along the race wall (bay 1 nearest the door, oldest first). Laying is an interaction at each bay that opens a pick-a-sheet list (each sheet has a short descriptive name). Sheets can be picked up and moved freely. Each sheet is also inspectable in inventory and in its bay.

**The evidence on the sheets** (designer key; the player sees only the drawings and inspect text):

| Sheet (name in list) | Old stain lines drawn under the fresh wet line | Gate | Tail door | Margin tally |
|---|---|---|---|---|
| "Sacks by the door" | 0 | Whole | Dry | 12 strokes |
| "The cat on the stone" | 1 | Whole | Dry | — |
| "Hook down" | 2 | Whole | Dry | — |
| "Long bar gone" | 3 | Whole | Dry | 39 strokes |
| "Gate side only" | 3 *visible*: Tovin drew only the gate half; the 4th line runs off the edge of the sheet | **Small crack** | Damp patch on the step | — |
| "Rain at the window" | 5 | Crack longer | Damp patch larger | — |
| "Imber's boots" | 6 | Crack longest | Damp up to the second step | 66 strokes |

**How the player solves it.** The **stain count** orders most of the sheets: each wet morning leaves one more line. "Gate side only" ties with "Long bar gone" at three lines, and the **crack** breaks the tie: a crack can't heal. The tail-door patch confirms the order of the last three. Players can check against the **real floor**: kneeling at the race wall (inspect) shows seven stain lines and today's damp.

**Checking.** When all seven bays are filled, the player uses **Walk the row** at bay 7. If correct, the step completes. If not, the inspect text names **the first contradiction in physical terms**, with no NPC solving it:
- *"Bay 4 shows a crack in the gate. Bay 5 shows it whole. The crack didn't mend itself."*
- *"Bay 2 has three old lines under the wet one. Bay 3 has two. The floor doesn't lose lines."*

If the player checks wrongly three times, **Imber** (not Tovin) offers one practical nudge: *"Count the lines first. Same as rings in a stump."* Tovin watches and never corrects. He describes his drawings if asked (`TF-D5` sheet lines), and that is all.

**Then the cadence** (`S06b_cadence`). With the sheets in order, the three tallies read 12, 39 and 66: nine shifts between each wet morning. The **shift board** by the door (inspect): *"Seventy-four strokes. Today's makes seventy-five."* 66 + 9 = 75. In `TF-D5`, Imber asks when the next one comes: **tonight** / in nine days / can't tell. A wrong answer gets *"Count it again,"* and the player can re-inspect the board and the sheets.

**And the other lines.** Once the cadence is settled, Imber crouches at the tail-door step (`TF-D5.30`): *"That's not from the pond. That came up from below."* The tail-door patches on the last three sheets are growing. Nobody knows what they mean yet. Tovin says only, *"It's been wetter there. I drew it how it was."*
**Verbs:** reconstruct, deduce.

### Beat 7 — Before Dark (`S07_prepare`)
**Objective:** *Be at the race gate by dark.*
Imber sends Tovin running for the keepers at the Cut watch. He is a mill runner, after all. *"Go on. You're faster than me and you know the path in the dark."* Tovin goes. That matters: he isn't in the fight, and he arrives with the keepers.
Optional preparations (each gives a small advantage; none is required):
- **Brace the gate** with the spare beam (carry + set): the far crank needs one extra wind per band.
- **Hang the lantern** on the footbridge post: drift telegraphs read more clearly in the race (presentation).
- **Cook** at the mill hearth and give a meal to Imber: one warm line, and Imber stays at the near crank for the first band (holds the pawl for ~10 s at the start).
Keep watch at the gate → the pulse hour.

### Beat 8 — Hold the Gate (`S08_hold`) — *set piece*
**Objective:** *Keep the race gate shut.*
See §TF.6. Completes when the pulse has passed, the crew is defeated, the drift in the race is dispersed and the spill boards are pulled.

### Beat 9 — Into the Record (`S09_record`)
**Objective:** *Give the keeper Tovin's sheets.*
At dawn the keepers bind the crew. A **Keeper** (role-based, from the Cut watch) reads the sheets on the mill floor where they still lie in order (`TF-D8`). They see the cadence, and they see the tail-door lines and go quiet. *"If that keeps growing like this, the next big one comes over the orchard dikes."* (Sets `TF_KEEPERS_READ_BACKWATER`.) Then the choice: **credit Tovin by name** in the Keepers' record, or **submit the sheets unsigned**. Tovin is standing right there. Item `tovin_floor_sheets` goes to the keeper either way. Sets `LM_TOVIN_CREDITED` and `LM_FLUSH_CALENDAR`.
**Verbs:** choose.

### Beat 10 — Steady Hands (`S10_close`)
**Objective:** *Speak with Imber and Tovin.*
`TF-D9`. Imber rubs out his notice himself. Tovin's last line varies by the choice. Completes the quest.

## TF.6 The gate hold: set-piece spec

**State.** The paddle has a height band of **0** (shut) to **3** (wide). Water through the race scales with the band. The pond is high (the crew's extra spill boards) and the leat head upstream has been opened: the **pulse** is the pond surging against the gate for ~3 minutes.

**The crew's plan, readable at a glance:**
- **Far-crank man** (pole-man variant) on the pond bank across the footbridge. While the near pawl is **free**, he winds the paddle up **one band every 8 s** (the crank clacks loudly on each tooth; a band rise has a heavy *thunk* and a gush).
- **Pry-men** (2 × pole-man) come at the near crank from the tail door. Their special is **Pry the pawl**: crouch at the crank with the long bar, ~2.5 s, bar glinting in the lantern light (the telegraph). If it completes, the pawl is free.
- **Cutter** (1) hangs back and harries whoever is at the near crank.
- When the far-crank man is defeated, **the cutter takes his place** once, after crossing the footbridge (~6 s; readable). When both are down, winding stops for good.

**The player's tools:**
- **Re-seat the pawl** at the near crank: 2 s channel. While seated, the paddle cannot rise.
- **Wind down** at the near crank: 3 s channel per band, pawl seated.
- **Interrupt** a pry by hitting the prying crewman: any hit cancels the channel.
- **Cross the footbridge** to stop the far crank. It's narrow; while on it, the player is exposed to the cutter.

**Phases (~4–6 minutes):**
1. **The roar** (0:00): the pulse arrives as a rising rumble from the leat; the pond lifts visibly against the gate. Crew enter. *"Bar! Get the bar on it!"*
2. **The hold** (~0:15–3:00): the juggle above. A focused player keeps the band at 0–1. A struggling player sees it reach 2 or 3, never more. No outcome is a fail.
3. **The race turns** (as soon as the band has ever been ≥ 1, and in any case at ~2:30): the water that got through churns in the race. **Drift rises out of the churn** (§TF.7, TF-E3b), one more for each band reached, minimum one so the moment always plays. It climbs onto the footbridge and the floor's race edge.
4. **Spill the pond** (after the crew is down): Imber shouts *"Spill boards!"* The player crosses to the far bank and pulls the crew's two extra boards (2 × 3 s channel). The pond drops over the old spill weir with a long rush, the safe way. The pulse dies.
5. **Keepers** arrive with Tovin as the last drift disperses.

**The strange moment** (after phase 5, unprompted): see §TF.8.

**Outcome counter.** `TF_MAX_BAND` (0–3) feeds only presentation: the race-edge flood decal inside the mill and one Imber line. It is never a failure or a flag other quests read.

## TF.7 Encounters

| Id | Enemies | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TF-E1** | 2 Skitter swarms | Race shallows at the footbridge | Leashed to water | Ripple line (~0.8 s) | Keeps the repair physical | Required, light |
| **TF-E2** | 1 pole-man, 1 cutter (smugglers) | Mill floor, night | Pole-man: reach sweeps; cutter: quick, close | Pole-man plants feet and draws the pole back (~1.2 s) before a wide sweep; cutter's lunge has a shoulder dip (~0.8 s) | Optional; lets players act on anger without costing evidence | Optional. ~45 s |
| **TF-E3a** | 2 pole-men (pry), 1 pole-man (far crank), 1 cutter | Gate, footbridge, far bank | See §TF.6 | Pry: crouch + bar glint ~2.5 s. Sweep: as E2. Far crank: audible clack per tooth | The gate juggle: priorities over damage | Required. A first-time player reaches band 1–2 |
| **TF-E3b** | 1–4 drift (Water Wraith, standard) | Race and race edge | Place-bound to race volume; lash when approached | The water surface goes glassy and still around the drift (~1.5 s) before an arm-lash; a cold mist ring on the ground marks reach | Drift forms from churned water: conditions, not souls | Required. Disperse all; they won't re-form after the race is quieted |

Crew who are defeated stay down and are bound by the keepers. They are not killed on screen. Nothing they carry is evidence; the keepers' record names the crew's employer from the MQ4 evidence, not from these men (`[ANTAGONIST]` swap layer unaffected).

## TF.8 The lagging pond: presentation spec

| Element | Spec |
|---|---|
| Trigger | Server event `tf.pond_lag` when `S08_hold` completes and the player is within the pond-bank volume (A) or the race footbridge; otherwise it fires on the next entry to that volume before `S09` |
| Duration | ~8 s |
| Audio | The pond's lap and the mill's drip continue normally. **No duck, no sting.** The quiet belongs to the night, not to the effect. |
| Visual | Reflections on the pond within ~15 m **lag a breath behind** their sources: the keepers' lanterns, Tovin, the player. The player raises a hand and the reflection raises it late. Then it catches up. |
| Tovin | If within 10 m, he stops beside the player, looks, and says **one line**: *"...There. Like that."* (`TF-D7.20`). He doesn't explain it and doesn't name it. If the player asks, his answer is *"I don't know. I just see it."* |
| UI | None |
| Meaning | Nothing. It identifies no one and proves nothing. It stays **unexplained** in v1 (bible §6.1: "What stays unexplained"). |
| Repeatable | No. Afterward the pond has the ME08-style inspect: *"Still. Your reflection keeps up."* |

## TF.9 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_notice` | Ask at Drowsebank about the runner's job. | Inspect dock-post notice **or** enter Drowsebank yard volume | Yes | Auto-accept |
| `S01_imber` | Talk to the miller. | `TF-D1` end node | Yes | |
| `S02_inspect` | Examine the race gate and the tool rack. | 4 inspects (board, strap, pawl, rack) | Yes | Stain lines optional |
| `S03_repair` | Repair the race gate. | `hoist_lower` + 2 `cut_board` + strap (anvil station **or** 2 `vice_lean`) + 2 `seat_gate` + TF-E1 defeated | Yes | |
| `S04_watch` | Watch the mill tonight. | `keep_watch` in loft → `tf.crew_scene` end, or TF-E2 both defeated | Yes | Key lines play before engagement is possible |
| `S05_sheets` | Tell the miller what you saw. | `TF-D4` end node; `tovin_floor_sheets` acquired | Yes | |
| `S06_calendar` | Lay Tovin's sheets on the floor in order. | `walk_the_row` validates order | Yes | Three wrong checks → Imber hint |
| `S06b_cadence` | Work out when the next one comes. | `TF-D5` "tonight" node | Yes | |
| `S07_prepare` | Be at the race gate by dark. | `keep_watch` at gate → pulse window starts | Yes | Optional preps: `brace_gate`, `hang_lantern`, cooked food given to Imber |
| `S08_hold` | Keep the race gate shut. | Pulse window ends + TF-E3a all defeated + TF-E3b all dispersed + 2 `pull_spill_board` | Yes | Fires `tf.pond_lag` |
| `S09_record` | Give the keeper Tovin's sheets. | `TF-D8` choice node; item given | Yes | Sets `LM_TOVIN_CREDITED`, `LM_FLUSH_CALENDAR`, `TF_KEEPERS_READ_BACKWATER` |
| `S10_close` | Speak with Imber and Tovin. | `TF-D9` end node | Yes | Quest → Completed; `drift.drowsebank_race` → quieted |

## TF.10 Flags

| Flag | Set by | Read by |
|---|---|---|
| `LM_TOVIN_CREDITED` = named / unsigned | `TF-D8` | MQ10; MQ12 |
| `LM_FLUSH_CALENDAR` = true | `TF-D8` | MQ7; MQ10 |
| `TF_KEEPERS_READ_BACKWATER` | `TF-D8` | MQ7 notice; Act III |
| `TF_FOUGHT_IN_LOFT` | `S04b_fight` | `TF-D4` Imber variant |
| `TF_FED_IMBER`, `TF_BRACED`, `TF_LANTERN_HUNG` | Optional preps | `TF-D7` barks; hold modifiers |
| `TF_MAX_BAND` (0–3) | `S08_hold` | Presentation; one `TF-D7` line |

## TF.11 Choices and consequences

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Credit Tovin by name** — *"Write his name on it. He drew them."* | The keeper writes *Sheets drawn by Tovin Pell, mill runner, Drowsebank* at the head of the entry. Tovin goes white. | Tovin becomes a **witness**. His name is in a record Sallow's people can learn of, and he is frightened (`TF-D8.20`). He did not ask for this. | MQ10: the calendar chip carries **full weight**; it's testimony with a name behind it. MQ12: Tovin's sketch is pinned in the Keepers' hall with his name under it. |
| **Submit unsigned** — *"Leave his name off. The sheets speak for themselves."* | The keeper writes *Sheets, Drowsebank, source kept back*. Tovin breathes out. | The record is **weaker**: an unsigned pattern can be argued with. Tovin's care stays private. Some will say he was protected; some will say he wasn't believed. | MQ10: the chip counts with **less weight** (Act III owns the number). MQ12: the sketch is pinned in the hall unsigned, and Tovin knows which one it is. |

Neither option is wrong. One honors Tovin publicly at his expense. The other protects him at the record's. Imber's arc completes either way: he keeps Tovin on.

## TF.12 Rewards

| Reward | Type | Notes |
|---|---|---|
| The flush calendar | Knowledge / world state | `LM_FLUSH_CALENDAR`; enables MQ7 |
| Drowsebank race quieted | World change | No drift in the race |
| Mill-smith's anvil | Access | Usable Smithing station afterward (if the Zones package keeps it) |
| Runner's wage, two nights | Small payment | From Imber; economy tuning sets the amount |
| Skill XP | Actions only | Melee; Smithing (anvil path); Cooking (optional) |

## TF.13 Failure, recovery, co-op

| Situation | Handling |
|---|---|
| Death during the hold | Respawn in the mill yard; the hold **resumes at its current state** (band and crew positions kept; pulse timer paused while the player is dead) |
| Logout during the hold | On return the pulse window restarts from phase 1 with full crew; repairs and sheets kept |
| Logout mid-puzzle | Sheets return to inventory; bays clear; nothing lost |
| Player sells or drops the sheets | Not droppable or sellable |
| Co-op | Each player has their own gate state and puzzle bays (per-player interaction state on shared props; fallback: puzzle bays are per-player UI over the same floor). Shared crew and drift give credit to all on the step. |

## TF.14 Integration needs

| Need | Minimum form |
|---|---|
| Ordered-slot placement puzzle | Seven slot interactions accepting one of seven item "pages" from a single quest item (or seven sub-items under one quest-item id); a validate interaction returning the first contradiction's text key |
| Gate band state machine | Integer 0–3; inputs: pawl seated/free, far-crank alive, wind-down channel; tick timer per §TF.6 |
| NPC special "pry the pawl" | Channelled NPC interaction on a world object, interruptible by damage |
| Hoist-lower interaction | One channel that moves a prop from loft to floor |
| Pond reflection lag | Client-side planar reflection delay, local only, time-limited |

## TF.15 Mystery ledger

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| Tovin's moved tools and wet floors | The crew uses the mill at night as their route since the Lock was closed; their pulses wet the race side. | Tovin is losing his mind. | The night scene; the pawl scars; empty outlines; the sheets. | Tovin did it. | — | This quest. |
| The tail-door lines | The backwater (§A2.2) arriving up the Drowse spur. | — | The sheets; the step. | The crew again. | Why it grows. | MQ7 (projection), MQ9 (flow-table). |
| The lagging pond | Unexplained bounded resonance. | Tovin "sees things." | Seen by the player and Tovin. | It's a ghost; it's Tovin's fault. | Everything. | Not revealed in v1. |

## TF.16 Open decisions

1. **The Drowse spur** linking Drowsebank's tail race to the lower Cut. *Recommendation: approve*; it grounds the Part 3 note about Drowsebank's "altered gearing and bank work" in wartime fortification (dossier §II).
2. **MQ10 chip weight** for unsigned vs named is Act III's number. This package states only that named weighs more.

## TF.17 Internal review log

| Finding | Revision |
|---|---|
| A draft had Tovin suggest the stain-count rule. That makes him the solver. | Tovin only describes his drawings. The hint comes from Imber, and only after three wrong checks. |
| Tovin was present for the gate fight and "noticed" the drift. | He runs for the keepers before dark. He sees only the pond lag afterward and doesn't name it. |
| The crew's key lines could be skipped by attacking early. | They play on entry, before engagement is possible. Combat never carries the information. |
| The gate hold had a fail state (gate fully open → flood → restart). | The band caps at 3; outcomes change presentation only. |
| The puzzle could be brute-forced with no reasoning. | The validator names a physical contradiction, so even brute force teaches the rule. Three wrong checks bring Imber's practical nudge. |
| "Salvage timber" risked endless war-salvage gathering (Woodland portfolio rejects renewable war salvage). | The beam is Imber's own seasoned stock: one beam, one board, no node. |
| Credit choice implied unsigned was cowardly. | Both options are written with a cost borne by someone. Tovin's fear is respected in both. |

---

# MQ7 — What the Ditch Knows (`DK`)

## DK.1 The quest in one paragraph

A keepers' notice is nailed to the Sluice Shelter post: from Tovin's floor, the next backwater comes in three nights and stands a hand over the Long Bank, the lowest run of the orchard dikes. Bryn Ruddock means to hold her section of it the way her household always has: kneeling on the dike crown with a riverglass bowl of ditch water, a rim of fresh softmoss and a line of driftroot stakes to show the water where to go. Her bowl cracked this spring. The player fetches a new one from Ottilie Penner (who makes them ring before she'll sell one), cuts softmoss at the shrine stones (moss near drift rots black, and Elspeth Quill won't let a scrap be wasted), and cuts stakes from storm-thrown driftroot, never the living roots that hold the bank. A Fenmere charter officer arrives with a measuring chain to say a dike this size is charter business. On the night, the player guards Bryn while she works. The water climbs the Long Bank and, at her section, folds aside around the bowl like cloth smoothed by a hand, then runs along the stakes back into the ditch. Drift rises in the overtopping water. Mud Pipers in the reeds call for help in Bryn's voice. A flood-mad elk comes down the rows. If anything reaches her, the hold slips and the old pear rows flood. The orchard is saved, wholly or mostly. The fen is not. In the morning the orchard households decide what Bryn's work is, with the player's word deciding it.

**Remember:** water folding aside around a bowl. **Want next:** who has been quieting the ditches since, without signing anyone's book.

## DK.2 Canon grounding

| Element | Source | Status |
|---|---|---|
| Layered farm-water model: small practice household- and neighbour-taught; shared works on commons rolls with experienced teachers; Fenmere charter oversight only for larger irrigation works | Director decision sheet D08; dossier §III, §VII | [CANON] as reconciled (region file §III) |
| "Flood-Calming: small adjustments to dikes and channels, guided by instinct and practice"; practice breaks when forced or when emotion surges | Dossier §VII | [CANON] |
| Riverglass bowls (glasswrights; Flow-Menders use them); riverglass helps water "hold a line"; works best when the user is steady | Dossier §III, §XV | [CANON] lore layer; nobody in Lowmark says it aloud |
| Softmoss reinforces dikes; rots faster near Wraiths | Dossier §X | [CANON] cue |
| Floodplain Orchards: raised berms, dike lines, sluice gates; driftroot trees in banks and dikes; Mud Pipers mimic reed sounds; Bog-Touched Elk dangerous when panicked | Dossier §IV, §VIII, §IX | [CANON] |
| Sluice Shelter (P15), child-height names | Part 3 proposal; bible §4.2 | Proposal, used |
| Living bank-binding trees are never stock | Woodland portfolio S-WD3 | Proposal-stage economy design, honoured |
| Bryn, Ottilie, Elspeth, the charter officer, the Long Bank, the hold | Bible §5.3; this package | [NEW] |

## DK.3 Summary card

| Field | Value |
|---|---|
| Content id | `lowmark.main.07_what_the_ditch_knows` |
| Prerequisite | MQ5 and MQ6 Completed |
| Offered | The keepers' notice at the Sluice Shelter, or speaking to Bryn |
| Target length | 35–45 minutes |
| Combat share | ~35% |
| Skills touched | Melee (required); Woodcutting (required, entry level); Hunting (optional, elk) |
| Choices | Commons roll or household practice → `LM_BRYN_ROLL`; outcome of the hold → `LM_ORCHARD_LOSS` |
| Quest items | `riverglass_bowl` |
| Unlocks | Orchard saved; Ottilie's shop as a known stop; MQ8 |

## DK.4 The place: the Floodplain Orchards (P16)

| Area | Environmental storytelling |
|---|---|
| **A. Bryn's ditch head** | A sluice gate with a hand-carved board: *RUDDOCK — TURN AT FIRST FROST, NOT BEFORE.* A cracked riverglass bowl on the gatepost, cleaned and kept anyway. |
| **B. The old pear rows** | The lowest rows, gnarled and propped. Windfall in the grass. The section that floods if the hold slips. |
| **C. The Long Bank** | A dike run a little lower than the rest, with a dip in its crown worn by feet. Bryn's boundary stones at either end, and a neighbour's beyond. |
| **D. The Sluice Shelter (P15)** | Roofless; child-height names scratched on the inside walls in more than one hand; a bench for council talk. The keepers' notice on the post. |
| **E. Shrine stones** | Three wayside stones along the orchard track, each thick with softmoss. The one nearest the reed margin has moss blackening at the edges. |
| **F. The river edge** | Living driftroots binding the bank, and a storm-thrown driftroot lying across the shingle, roots in the air. |
| **G. Reed margin** | Dense reeds between orchard and river. Reed sounds that are almost words. |
| **H. Ottilie's glass shop (Brookhollow, P01)** | Bowls, bottles and lenses on every surface, each with a small paper tag in Ottilie's hand. A sign: *NO RIVERGLASS FOR CELLARS.* |

## DK.5 Player-facing sequence

### Beat 0 — The Notice (`S00_notice`)
**Objective:** *Find Bryn Ruddock at the orchard ditches.*
Inspecting the notice or approaching Bryn starts the quest. Notice text (keepers' hand): *"By the Drowsebank reckoning: backwater three nights hence. Height over the Long Bank by a hand. Orchard households, make ready."*

### Beat 1 — Bryn's Plan (`S01_bryn`)
**Objective:** *Hear Bryn out.*
`DK-D1`. Brisk and proud. She'll hold her section as her mother taught her. She needs a bowl, moss and stakes, in that order of difficulty. Elspeth Quill is there checking an orchard hand's cut, and adds that she'll show the player which moss to take. Bryn's last line sets the rule for the whole quest: *"And don't call it anything. It's ditch work."*

### Beat 2 — Bowl, Moss, Stakes (`S02a_bowl`, `S02b_moss`, `S02c_stakes`)
**Objective:** *Fetch a riverglass bowl, fresh softmoss and driftroot stakes.* Any order.

- **Bowl (Brookhollow).** Ottilie sets three bowls on the bench (`DK-D2`): *"Ring them. Hold them to the window. Then tell me."* Each bowl has two inspects. **Ring** (tap): A rings short, B rings long, C rings long. **Window**: A shows a seed bubble, B shows a faint strain line across the base, C is clean. The player names C. A wrong pick gets Ottilie talking to the bowl: *"She's not ready for ditches, are you,"* and the player tries again. Ottilie asks what it's for. She wants her glass used for bowls, not schemes. An honest answer gets the bowl on Bryn's account. Gives `riverglass_bowl`.
- **Softmoss (shrine stones).** Elspeth meets the player at the stones (`DK-D3`). Inspect each: two fresh ("green, springy, cold to the touch"), one rotting ("black at the edges, soft as wet bread. There's heavy water near here."). Cutting at the rotting stone is allowed, but the bundle is refused at the dike (*"That won't last the night"*) and the player returns. Elspeth teaches by watching: *"Cut, don't tear. Leave the root on the stone."* One cut gives a **softmoss bundle** (carry state).
- **Stakes (river edge).** Inspecting a living driftroot: *"Living roots, holding the bank. Bryn would have your hide."* The storm-thrown driftroot is the Woodcutting target. One gather gives a **stake bundle** (carry state). **DK-E1**: Mud Pipers in the reed margin. They come out piping, and one piper calls *"Oi! Over here!"* in a voice like Bryn's from inside the reeds. First taste of the mimicry, played straight.

### Beat 3 — Set the Bank (`S03_set`)
**Objective:** *Set the stakes and moss along Bryn's section.*
Bryn shows the line: three stake points (3 s channel each) slanting along the crown toward the ditch, and two moss points (3 s channel each) packed into the crown's dip. The bowl is handed over (`item-given`).
At the second stake the **charter officer** arrives with a measuring chain and a ledger (`DK-D4`): a dike this size falls under Fenmere charter oversight, and who authorised this? Bryn bristles. The officer will measure: *"Hold the end."* The player holds the chain's end at Bryn's west boundary stone (3 s channel) and then at the east stone (3 s channel) while the officer reads it. The section is **one holding's length, on Bryn's own stones**. On its face the officer allows it as household practice below the charter line, but the Long Bank as a whole is a shared work, so the commons roll is the council's business. *"If it fails, it floods four holdings. I'll be watching."* They stay to watch.

### Beat 4 — Waiting (`S04_wait`)
**Objective:** *Wait for the backwater at the Sluice Shelter.*
Keep watch → night. Before the water comes, Bryn says the quest's key instruction (`DK-D5`): *"I won't shout. Whatever happens, I won't. If you hear me shouting, it isn't me."*

### Beat 5 — The Hold (`S05_defend`) — *set piece*
**Objective:** *Keep everything off Bryn until the water falls.*
See §DK.6.

### Beat 6 — The Council at the Shelter (`S06_council`)
**Objective:** *Speak for Bryn at the Sluice Shelter.*
At first light the orchard households gather, along with the charter officer, Elspeth, Bryn and the **roll-keeper** (the eldest ditch-turner on the orchard commons roll, role-based). `DK-D7`. The practice was seen by everyone. Now the households decide what it was. Bryn won't argue for herself: *"You saw it. You tell them."* The player chooses (§DK.9). Sets `LM_BRYN_ROLL`.

### Beat 7 — The Pear Rows (`S07_close`)
**Objective:** *Walk the orchard with Bryn.*
`DK-D8` among the rows. If `LM_ORCHARD_LOSS` = partial, the old pear rows stand in brown water to the knee and Bryn is already propping the worst tree. Either way she says the thing the quest is about: *"That's one night. It'll come again, and it's not mine to stop."* Completes the quest.

## DK.6 The hold: set-piece spec

**Bryn's state.** Bryn kneels at the centre of the Long Bank's dip with the bowl in both hands. The hold runs **~3 minutes** across three waves while the backwater is over the bank. The player can't help with the working, only keep things off her.

**Showing the practice plainly** (presentation, from the first second of the hold):
- The backwater tops the Long Bank along its whole length. Along the rest of the dike it pours over in a thin, ugly sheet.
- At Bryn's section the water reaches the bowl's reach (~4 m) and **folds aside**: the surface bends around her in a smooth, slow curve **like cloth smoothed flat by a hand**, then runs along the line of stakes and pours back into the ditch. Softmoss darkens as it soaks.
- Bryn's hands are steady. Her breath is audible and even. No light, no glow, no particles, no sound sting. Just water doing something water doesn't do, slowly.
- The charter officer, lantern raised, says nothing at all through the hold.

**The slip rule.** If any hostile creature **reaches Bryn** (lands a hit on her or ends a lunge inside 2 m), she flinches and the hold **slips**: the curve breaks at the west end and water pours through into the old pear rows (one section; the cap). After ~5 s she has it back. `DK_SLIPS` counts slips. One or more sets `LM_ORCHARD_LOSS` = partial; the flooded section doesn't get worse with more slips. Bryn can't be killed and doesn't take lasting harm. No outcome fails the quest.

**Waves:**

| Wave | Time | Threat | Readability |
|---|---|---|---|
| **1 — The overtop** | 0:00–1:00 | **2 drift** rise out of the sheet of water pouring over the bank's far end and drift along the crown toward Bryn | The overtop water goes glassy and still before each forms; a cold mist ring marks their reach |
| **2 — Her own voice** | 1:00–2:00 | **Mud Pipers**: 2 pipers in the reed margin and 1 bog-diver in the ditch. The pipers **call in Bryn's voice** from the reeds: *"Here! Help me — here!"*, *"I've slipped, I'm in, quick!"*. Positional audio, deliberately away from her. If the player goes to the voice, the pipers ambush there, and the bog-diver comes up the ditch at the real Bryn. | Bryn's real position never moves and **she never shouts** (set up in `DK-D5`). The diver's approach shows as a V of ripples up the ditch (~2 s) |
| **3 — The elk** | 2:00–3:00 | **1 Bog-Touched Elk**, flood-driven, comes down the orchard rows at a run with **1 drift** behind it | Head lowered and stamping (~1.5 s), then a straight charge along the dike crown at Bryn. Hitting it once draws it onto the player; sidestepping its charge makes it overrun and stand exposed (~2 s), the same language as the MQ1 boar |

**The end.** The backwater crests and falls. The curve relaxes back into ordinary water. Bryn sits back on her heels and doesn't get up for a while. Elspeth tends her: *"Hands."* Downstream, in the far ditches, cold mist still hangs over two pools. The orchard is saved; the drift site is still **active** (§A2.7).

## DK.7 Encounters

| Id | Enemies | AI role | Telegraph | Solo target |
|---|---|---|---|---|
| **DK-E1** | 2 Mud Pipers (piper) | Skittish lurers; engage when the player is in the reeds; fight to defeat once engaged | Puffed throat and a rising reed note (~1 s) before a spit or lunge | Required (near the stake gather). ~40 s. **First Mud Pipers** (bible §10) |
| **DK-E2** | Wave 1: 2 drift. Wave 2: 2 pipers + 1 bog-diver. Wave 3: 1 elk + 1 drift | As §DK.6 | As §DK.6 | Required. A first attempt typically gives 0–1 slips |

## DK.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_notice` | Find Bryn Ruddock at the orchard ditches. | Inspect notice or enter Bryn's volume | Yes |
| `S01_bryn` | Hear Bryn out. | `DK-D1` end | Yes |
| `S02a_bowl` | Fetch a riverglass bowl. | `riverglass_bowl` acquired (`DK-D2`) | Yes |
| `S02b_moss` | Cut fresh softmoss. | Fresh softmoss bundle deposited at the Long Bank basket | Yes |
| `S02c_stakes` | Cut driftroot stakes. | Stake bundle deposited at the Long Bank + DK-E1 defeated | Yes |
| `S03_set` | Set the stakes and moss. | 3 `set_stake` + 2 `pack_moss` + bowl given + 2 `hold_chain` (`DK-D4` end) | Yes |
| `S04_wait` | Wait for the backwater. | `keep_watch` at the shelter → `DK-D5` end → hold window starts | Yes |
| `S05_defend` | Keep everything off Bryn. | Hold window ends + all DK-E2 defeated | Yes | 
| `S06_council` | Speak for Bryn at the Sluice Shelter. | `DK-D7` choice node | Yes |
| `S07_close` | Walk the orchard with Bryn. | `DK-D8` end | Yes |

## DK.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `LM_ORCHARD_LOSS` = none / partial | `S05_defend` (from `DK_SLIPS`) | MQ12; orchard props |
| `LM_BRYN_ROLL` = commons / household | `DK-D7` | MQ12 |
| `DK_SLIPS` (int) | Hold | `DK-D8` variant |
| `DK_FOLLOWED_VOICE` | Player entered the wave-2 voice volume | `DK-D8` Bryn line ("Told you I wouldn't shout.") |
| `DK_OTTILIE_HONEST` | `DK-D2` honest answer | Ottilie's later barks |

**The council choice** (C09 layered model; both options are lawful under it):

| Option | What it means | Cost | Later |
|---|---|---|---|
| **Enrol her on the commons roll** — *"Put her on the roll. Let her teach the bank, with the roll-keeper watching."* | Bryn's work on the Long Bank becomes **shared-work stewardship**: her name on the orchard commons roll, the roll-keeper as her experienced teacher. The charter officer closes the ledger. | Bryn is **watched**. Her name is written down as someone who does this. She hates it, and says so (`DK-D7.20`). Her household practice now answers to the roll. | MQ12: Bryn is teaching two orchard hands on the Long Bank, sour about it and good at it. |
| **Vouch for household practice** — *"It was her own section, on her own stones. Household work, below the charter line."* | The council records nothing. Bryn's work stays **household practice**, free and unwritten. The officer notes the measure and their objection. | Bryn is **exposed**. If the Long Bank ever fails, nobody's roll stands behind her, and the officer has a ledger line ready. The player's word is what she has. | MQ12: Bryn holds her section alone again and tells the player, gruffly, that their word has held as well as her stakes. |

No option is wrong. It's the C09 threshold question made personal: **protection that watches you**, or **freedom that leaves you alone with the risk**.

## DK.10 Rewards

| Reward | Type | Notes |
|---|---|---|
| The orchard saved (wholly or mostly) | World change | Props per `LM_ORCHARD_LOSS` |
| Share of the orchard's fruit | Small payment in kind | Ingredient definition belongs to the item pass |
| Ottilie's shop | Access | Ottilie sells ordinary glass afterward (economy pass) |
| Skill XP | Actions only | Woodcutting; Melee; Hunting if the elk is harvested |

## DK.11 Failure, recovery, co-op

| Situation | Handling |
|---|---|
| Death during the hold | Respawn at the Sluice Shelter; the hold **pauses** (the water stays high; Bryn holds) until the player re-enters the dike volume |
| Logout during the hold | The hold window restarts at wave 1; `DK_SLIPS` resets to the value at the last completed wave |
| Rotten moss brought | Refused at the basket; the player cuts again (`DK-D3.20`) |
| Co-op | Each player's Bryn, slips and orchard state are their own. Partners' fights clear shared creatures for both, which is a real benefit of grouping |

## DK.12 Integration needs

| Need | Minimum form |
|---|---|
| Water "fold" presentation | Local water-surface deformation around an NPC within ~4 m while a hold state is true; flow decal along the stake line |
| NPC hold state with slip trigger | NPC flag `holding`; any hostile hit or lunge-end inside 2 m triggers the slip event, a 5 s recovery and the west-section flood decal |
| Positional voice-mimic barks | Mud Piper barks using Bryn's voice lines, emitted from the piper's position |
| Carry-state bundles | As in MQ1 (moss, stakes) |

## DK.13 Mystery ledger and open decisions

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Reveal owner |
|---|---|---|---|---|---|
| What Bryn does | Bounded household water practice (C09): small, attentive, real, steadied by riverglass. | "She's good with the ditch-water." Outsiders: magic, fraud, privilege. | The hold, seen by a skeptic. | She's a mage. She could fix the fen. | This quest (shown, not explained) |
| Why it can't fix the fen | The backwater is regional pressure; a hold moves one bank's water for one night. | — | Drift still in the far ditches; Bryn's own words. | Enough Bryns could stop it. | MQ9 flow-table |

**Open decision:** the exact charter threshold. This package uses "one holding's length, on the holder's own stones" as the observable test for household practice. *Recommendation:* adopt as a local Lowmark custom, not a code, under D08.

## DK.14 Internal review log

| Finding | Revision |
|---|---|
| A draft had the bowl glow. That reads as spellcasting. | No light, no particles. Only the water's shape changes. |
| Bryn explained how the practice works. | She refuses to name it. Elspeth and Ottilie talk around it. Nobody explains. |
| A loss state flooded the whole orchard. | Capped at one section; no fail. The loss is a scar, not a defeat. |
| The officer was a strawman. | The officer measures honestly, concedes on the measure and keeps a fair concern (four holdings). They watch and say nothing during the hold. |
| Stakes from living driftroots would teach stripping. | Living roots are inspect-only; the storm-thrown root is the only target. |
| The commons option read as the "good" answer. | Bryn's dislike of being watched is voiced, and the household option's risk is real. |

---

# MQ8 — The Mantle (`MN`)

## MN.1 The quest in one paragraph

Ansel Corrie's patrol book has a new kind of entry: *quiet by morning, no repair.* Three sites, including Bryn's orchard dike, went still overnight with nobody signing for it. At each one the player finds the same signs: softmoss pressed into the bank by a thumb, reeds cut low and clean at a slant, settled water, and at dawn a mist lying low. Bundles of cut reeds are left along the Path of Unburnt Reeds like a cutter's day's work, and they lead to the Mantle Shrine. At dawn the shrine wears its mist like a cloak, and the mist lifts as the player arrives. Sedge is sitting on the step binding reeds. He admits nothing. He sets three tasks he never calls tests. Walk a panicked elk out of heavy water without killing it. Read three Marking Stones and say which reads true. Tell him what you've seen. Then he asks the player to strike a drift. They do, and it **splits**: two smaller drifts form in two pools downstream. *"Now there are two."* Sedge kneels and quiets the pool by hand. It takes a long time, the rings in the water close inward, and when he's finished the mist sits on his shoulders and he can barely stand. He confirms nothing about himself. He agrees to take the player to someone who knows how the water used to be kept.

**Remember:** one drift becoming two, and an old man shaking with the cost of making it none. **Want next:** the someone.

## MN.2 Canon grounding

| Element | Source | Status |
|---|---|---|
| The Field-Mage's Mantle: mists that cling around shrines, "said to be his cloak"; cloaked figure near wells near Ashenstead | Dossier §V.3, §XI | [CANON] rumor |
| The Last Field-Mage alone keeps combat water practice; a restrained inheritor of Riverwarden teaching; refuses to make the player a weapon; knows why force spreads the problem | Dossier §I, §VII; Main Arc movement 8 | [CANON] / approved architecture |
| Sedge as the Field-Mage; three tests; force splits drift; never confirms aloud | Bible §2.6, §6.1 | [PROPOSAL — DIRECTOR] D-7 |
| Bog-Touched Elk "skittish but dangerous when panicked; sometimes driven mad by Wraith presence" | Dossier §VIII | [CANON] |
| Herding by alert radius | Hunting portfolio F4 traveling-grazer alert framework (one reusable alert-and-movement framework) | Proposal-stage economy design, reused |
| Water practice breaks when forced; "Wraith Cleansing — the most dangerous rite" | Dossier §VII | [CANON] |

## MN.3 Summary card

| Field | Value |
|---|---|
| Content id | `lowmark.main.08_the_mantle` |
| Prerequisite | MQ7 Completed |
| Offered | Ansel at the Watchers' Lantern Post (bark on approach: *"You'll want to see this. I don't."*) |
| Target length | 30–40 minutes |
| Combat share | ~5% (one strike by design; one optional) |
| Skills touched | Hunting (the elk, by not hunting it); Melee (one strike); Cooking (optional, feeding Sedge) |
| Choice | What the player says they saw → `MN_SAW`; with the elk, sets `LM_SEDGE_TRUST` |
| Quest items | None |
| Unlocks | Braid-stone reading; ME09 *The mantle at dawn*; MQ9 |

## MN.4 Places

| Area | Environmental storytelling |
|---|---|
| **A. Lantern Post (P21)** | Ansel's book open on the table under a stone. Three entries ringed in a different ink. |
| **B. The quieted sites** | Bryn's Long Bank far ditch; a Heartlands field ditch; the pool at the Circle of Unburnt Reeds (P26). Each is calm and clear, with thumb-pressed softmoss in the bank and cut reed ends. |
| **C. Path of Unburnt Reeds** | Reeds taller than the player on both sides. Every few hundred paces, a **bound reed bundle** set upright against a stake, waiting to be collected. The children's warning stake (ME06). |
| **D. Mantle Shrine (P24)** | A small wayshrine furred in softmoss. At dawn a mist sits on it **shaped like a cloak over shoulders**. A stone step, worn in one place by one person sitting. |
| **E. The Mantle channel** | A fen channel below the shrine: a heavy pool (cold mist, no birds) with a **stone causeway** of old Marking-Stone footings running to dry ground on the east side. Deeper water to the west. |
| **F. The stone run** | Three Marking Stones along the channel, a stride apart, all looking much alike at first. |
| **G. The lower pools** | Two small pools downstream, linked to the heavy pool by trickles. This is where the split drift goes. |

**MAP VERIFICATION REQUIRED:** the shrine lies on the Path of Unburnt Reeds between Ashenstead and Veilwater, above a fen-edge channel (bible §4.1).

## MN.5 Player-facing sequence

### Beat 0 — Quiet by Morning (`S00_book`)
**Objective:** *Read Ansel's patrol book.*
`MN-D1`. Ansel shows the three ringed entries. *"Somebody's doing our job better than us, and not signing the book."* He's half amused and half frightened. He asks the player to look, because he doesn't want to be the one who finds out.

### Beat 1 — The Signs (`S01_signs`)
**Objective:** *Look at the quieted sites.*
Visit **any two** of the three sites. At each, three inspects: **pressed moss** ("pressed into the bank by a thumb, recently. Somebody packed this by hand."), **cut reeds** ("cut low and clean, at a slant"; if `GL_SEDGE_SPOKEN`: "like the stems at the Rebirth Fields' edge"), **the water** ("clear to the bottom. Not cold."). At dawn, a fourth: **the mist** lying low over the water and lifting as the player comes near.
**Verbs:** investigate.

### Beat 2 — The Bundles (`S02_trail`)
**Objective:** *Follow the cut reeds.*
On the Path of Unburnt Reeds, four upright reed bundles at intervals, each inspectable (*"Bound with a cutter's knot. Left to be collected."*), lead to the Mantle Shrine. If the player arrives outside dawn, **Keep watch** at the shrine step advances to dawn. At dawn the mist sits on the shrine like a cloak and lifts as the player steps into area D. Sedge is sitting on the worn step with a bundle across his knees.

### Beat 3 — The Cutter (`S03_meet`)
**Objective:** *Speak with the reed-cutter.*
`MN-D2` `[D-7]`. He admits nothing. *"You've been following my bundles. They're for thatch."* Every question the player asks, he answers with a question about what they saw. Then he sets the first task without calling it one: *"There's an elk in the channel. Get it out. Don't kill it."*

### Beat 4 — The Elk (`S04_elk`) — *test 1*
**Objective:** *Get the elk out of the heavy water.*
A **Bog-Touched Elk** stands chest-deep in the heavy pool, panicked, wheeling, eyes white. It uses the reusable alert-and-movement framework (Hunting F4): an **alert radius** (~8 m, visible as the elk's head snapping toward the player and its ears flattening) and a **flight rule** (it moves directly away from the player when they enter the radius).
- Approached from the dry east bank, it flees **west into deeper water**, where it struggles and calms only after the player backs off (it resets to the start).
- The solution is to **wade round through the shallows to the west side** (slow, cold, quiet) and step into its radius from there. It flees **east**, onto the causeway, and climbs out on dry ground, shakes, and trots off into the reeds.
- Old stakes on the west shallows mark where people have stood before (a hint, not a sign).
- Sedge's only help, if the player waits by him: *"Stand where you'd want it not to go."*
- Attacking the elk **provokes** it (wildlife). It fights to defeat with a lowered-head charge (~1.5 s telegraph). If it dies, the task ends: `MN_ELK_KILLED`. Sedge says one quiet line (`MN-D3.10`) and moves on. This is not a failure. It cools Sedge (§MN.8).
**Verbs:** herd, wade, restraint.

### Beat 5 — The Stones (`S05_stones`) — *test 2*
**Objective:** *Find the stone that reads true.*
`MN-D4`. Sedge: *"One of these reads true. Which?"* Three inspects per stone, extending the True Line skill:

| Stone | What the player can see | Truth |
|---|---|---|
| **1** | Crisp notch; **square chisel marks** inside the groove; the old grooves around it are water-rounded. | Re-cut. Somebody made the notch say something new. |
| **2** | Grooves water-rounded, older notches below. But the **moss is on its upstream face** and its silt line **slants**: the stone has been tipped. Its notch no longer sits level with the high-water stain on the reed stems. | Moved. A true stone in a false place. |
| **3** | Grooves rounded; older notches below; the notch **level with the old high-water stain** on the reed stems and with stone 2's oldest notch. Silt line level. | True. |

The player names a stone. A wrong pick gets *"What did you see on it?"* and the player can look again with no penalty. After the right pick, Sedge asks *"Why?"* An observational reason is accepted; an interpretive one is gently corrected (*"You felt it. What did you see?"*), and the player picks again from observations. Completing the task unlocks **Braid-stone reading** (§MN.9).
**Verbs:** read stones.

### Beat 6 — What You've Seen (`S06_seen`) — *test 3*
**Objective:** *Answer the cutter.*
`MN-D5`. Sedge asks about the player's road: the stone at Whisperflow, the orchard hold, the race at Drowsebank, the warm well (if `GL_WELL_WARM`). Each round offers one **observation** and one **interpretation**. Observations are accepted (*"Yes."*). Interpretations are corrected without scorn (*"You saw water climb. You didn't see a reason."*). Nothing here is scored. It teaches the evidence rule through the one character who could break it and won't.

### Beat 7 — Now There Are Two (`S07_demo`) — *the demonstration*
**Objective:** *Do what the cutter asks.*
Back at the heavy pool, a single **drift** forms where the elk stood. Sedge: *"Hit it."* (`MN-D6`).
1. The player disperses it with a weapon (**MN-E1**, one standard drift, normal fight).
2. **It splits.** The cold mist doesn't sink. It runs downstream in **two threads** along the trickles, and in each lower pool a **smaller drift** forms (~60% size, weaker). Sedge: *"Now there are two."*
3. If the player attacks a small one (optional, **MN-E2**), it disperses and **two wisps** rise further down. Wisps are harmless, faint and visible. Sedge: *"Enough."* The demonstration caps there.
4. **Sedge quiets the pool** (§MN.7). The player's only task is to **stay still and keep their weapon down**. Attacking anything during the quieting interrupts it (the small drifts split again into wisps). Sedge has to start over and says one line: *"Don't."*
**Verbs:** fight once; watch; restraint.

### Beat 8 — The Shrine Step (`S08_close`)
**Objective:** *Help the cutter back to the shrine.*
Sedge can barely stand. The player walks beside him (walk-with: he moves at a slow pace and stops twice; fallback: he walks slowly ahead and waits). At the step, the player may give him cooked food (optional, `MN_FED`). `MN-D7` closes. He asks once more what the player saw, and **this** answer is the choice (§MN.8). He confirms nothing about himself, whatever the player says. Then: *"There's someone who knows how it used to be kept. I'll take you. Dawn."* Completes the quest.

## MN.6 Encounters

| Id | Enemy | Role | Telegraph | Solo target |
|---|---|---|---|---|
| — | Bog-Touched Elk (wildlife) | Not hostile unless provoked; alert/flight framework | Head snap + ears flat at alert; lowered-head charge (~1.5 s) if provoked | Avoidable by design |
| **MN-E1** | 1 drift (standard) | Place-bound; lashes when approached | Glassy stillness (~1.5 s) before an arm-lash; mist ring | Required. ~30 s |
| **MN-E2** | 2 small drifts (60%) → wisps | Small drifts lash weakly; wisps don't engage | As E1, faster and fainter | Optional |

## MN.7 The quieting: presentation spec

| Element | Spec |
|---|---|
| Trigger | `S07_demo` after the split (and after MN-E2 if the player chooses it) |
| Duration | ~40 s, unbroken if the player stays still; restarts once on interruption |
| Sedge | Wades to the pool's centre, kneels until the water is at his chest, and lays both hands flat on the surface. He doesn't move again until it's done. |
| Water | **Rings move inward.** Ripples start at the pool's edge and travel **toward his hands**, closing on him: water doing the reverse of what water does. As each ring reaches him, the pool's surface stills a little further out. |
| Downstream | Over the last ~10 s the two small drifts (and any wisps) **sink** where they stand, their mist running back up the trickles into the pool and down into the stillness. They are not "killed": they go back down. |
| Mist | As the pool stills, the cold mist lifts off the whole channel and **settles on Sedge's shoulders and back like a cloak**, the shrine's mantle shape. It stays as he stands and thins over ~30 s as he walks. Nobody comments on it. |
| Audio | The channel's ambient fades to near silence over the 40 s. At the end, one bird. His breathing, ragged. |
| Cost | When he stands, his hands are grey and shaking. He staggers. He says nothing until the shrine step. |
| UI / camera | None / player's own |
| Meaning | Shown, never said: force spreads heavy water downstream; quieting by hand gathers it back and costs the person doing it. It says nothing about who the drift "was." |
| Fallback | If inward rings aren't feasible, play the surface going still from the edges inward over 40 s with the downstream sinking. The meaning survives. |

## MN.8 Steps, flags, choice

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_book` | Read Ansel's patrol book. | `MN-D1` end | Yes |
| `S01_signs` | Look at the quieted sites. | 3 inspects at each of 2 sites | Yes |
| `S02_trail` | Follow the cut reeds. | Enter shrine volume at dawn (keep watch if needed) | Yes |
| `S03_meet` | Speak with the reed-cutter. | `MN-D2` end | Yes |
| `S04_elk` | Get the elk out of the heavy water. | Elk enters the causeway exit volume **or** elk killed | Yes |
| `S05_stones` | Find the stone that reads true. | `MN-D4` correct-reason node | Yes |
| `S06_seen` | Answer the cutter. | `MN-D5` end | Yes |
| `S07_demo` | Do what the cutter asks. | MN-E1 dispersed → split event → quieting presentation completes | Yes |
| `S08_close` | Help the cutter back to the shrine. | Walk-with arrives + `MN-D7` choice node | Yes |

| Flag | Set by | Read by |
|---|---|---|
| `MN_ELK_KILLED` | `S04_elk` | `LM_SEDGE_TRUST`; MQ9 bark |
| `MN_SAW` = water / you / mage | `MN-D7` | `LM_SEDGE_TRUST`; MQ9 `BF-D3`; MQ12 |
| `LM_SEDGE_TRUST` = warm / cool | `S08_close` | MQ9, MQ11, MQ12 |
| `MN_FED` | Cooked food given | `MN-D7` variant |
| `MN_INTERRUPTED` | Attack during quieting | `MN-D7` variant ("You'll learn.") |

**The closing question** (`MN-D7`, "So. What did you see?"):

| Answer | `MN_SAW` | Sedge |
|---|---|---|
| *"The water went still. The two downstream went back down."* | water | *"Yes."* He looks at the player properly for the first time. |
| *"I saw you make it go still. It cost you."* | you | *"It costs."* A long pause. *"Yes."* |
| *"I saw the Field-Mage."* | mage | Silence. *"You saw an old man in a pool."* He turns back to his reeds. |

**`LM_SEDGE_TRUST` rule:** **cool** if `MN_ELK_KILLED` **or** `MN_SAW` = mage; otherwise **warm**. Both are legitimate. Killing the elk is allowed, and naming him is allowed; both make him trust the player less, because what he wants most is for nobody to need him and nobody to say it. Cool changes his warmth in MQ9–12, never access. The guide to the falls is offered either way.

## MN.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| **Braid-stone reading** | Knowledge | Marking Stones on fen and side channels become inspectable: *"A Braid mark. Water's under the notch: the channel is carrying."* / *"Over the notch: the channel is choked or cut."* / *"Square tool marks in the groove: re-cut. Don't trust it."* Extends the True Line skill (bible §8) |
| ME09 enabled | Access | *The mantle at dawn* micro-event |
| Skill XP | Actions only | Melee (one fight); Hunting XP is **not** granted for herding unless the Gameplay Designer adds an alert-avoid action under F4 (open, §MN.11) |

## MN.10 Failure, recovery, co-op

| Situation | Handling |
|---|---|
| Elk driven deep repeatedly | It always calms and resets; no limit |
| Elk killed | The task ends; trust cools; the quest continues |
| Death | Respawn at the shrine step |
| Interrupting the quieting | It restarts once with Sedge's line; a second interruption makes him finish anyway, slower (no soft-lock) |
| Co-op | The elk, the stones and the demonstration are **per-player instanced props** (the elk is a quest-spawned creature visible only to its owner; fallback: a partner's attack on the shared elk counts for that partner only). Sedge's quieting plays per player. |

## MN.11 Mystery ledger, open decisions

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Reveal owner |
|---|---|---|---|---|---|
| Who quiets the ditches | Sedge (D-7). | The Field-Mage's Mantle; nobody; Watchers' luck. | Thumb-pressed moss, slanted cuts, bundles, the mantle mist, the quieting. | A spirit of the shrine. | This quest, by sight. Never by his word. |
| Why force fails | Dispersal sends heavy water downstream into new pools. Quieting gathers it back down at a personal cost. | Watchers: "disperse it and move on." | The split; the inward rings; the sinking. | Kill enough of them and it ends. | This quest |

**Open decisions:** (1) D-7 itself. Every Sedge node here is tagged `[D-7]`. (2) Whether herding should give Hunting XP (Gameplay Designer; F4 framework).

## MN.12 Internal review log

| Finding | Revision |
|---|---|
| Sedge said "I'm not the Field-Mage." A denial is a confirmation by another route. | He never addresses it. He answers with what the player saw. |
| The quieting used a glow and a chant. That's spellcasting theatre. | Hands on water, inward rings, mist, cost. No light, no words. |
| Killing the elk ended the quest in failure. | Allowed; it cools trust only (bible §6.1). |
| The stone test had one obviously wrong stone and two coin-flips. | Each stone has a distinct physical tell (re-cut, moved, true), all readable with the True Line habits. |
| Test 3 scored the player. | It no longer does. Only the closing answer, after the demonstration, matters, and every answer is accepted. |
| The demonstration risked a free combat loop (split forever). | Capped at drift → two small drifts → wisps. |

---

# MQ9 — Behind the Falls (`BF`)

## BF.1 The quest in one paragraph

At dawn Sedge walks the player to the end of the Path of Unburnt Reeds and up the Veilwater falls path: wet switchbacks, spray-slick stone, and step-stones where the plunge-pool outflow narrows. Behind the curtain the roar stops as if a door had shut. The Listening Steps are terraces of carved channels descending into moss, each channel making its own small clear note. It is a stillness full of sound, the opposite of a dead spot. A Riverwarden called Oriel is clearing a channel with a reed brush and doesn't look up until it's done. Oriel shows them the **flow-table**: a carved basin where water runs the Vale's real channels in miniature. The player can find Whisperflow's bend, the orchards, the guide-line ring under Ashenstead, Drowsebank, the fen. They can also see the **Relief Cut**, a raw straight gash hacked through the braided lines with none of the carving's care. Oriel runs a pulse down it. Silt clouds the little fen and rides out into everything. Then the player plugs the scar and opens three Braid gates in the order Oriel teaches, and watches the pressure divide, slow and settle. Oriel speaks of water as work, never as anything else. The Riverwardens withdrew because rulers kept asking for floods on command. Oriel will give the Braid knowledge to the Vale's workers on one condition: the Vale agrees, in public, to tend the Braids together, with no single house or office owning them. The player makes a promise in their own words, and it will be quoted back to them at the end.

**Remember:** a whole valley in a stone basin, and one ugly straight line through it. **Want next:** Crest Hall, and whether the Vale can agree on anything in public.

## BF.2 Canon grounding

| Element | Source | Status |
|---|---|---|
| Veilwater Falls; behind it the Riverwarden enclave; limestone, moss, reedwork, flowing channels; rituals of listening, not bending | Dossier §IV.6, §VI | [CANON] |
| Riverwardens taught flood-timing and irrigation; prevented floods by tuning channels; withdrew as wars intensified and demands for power grew | Dossier §VI | [CANON] |
| Withdrawal because rulers repeatedly tried to turn care for water into command over people | Main Arc author truth; bible §6.1 | Approved architecture |
| Inner oasis and Warden's Hearth unseen in v1; Riverwardens do not return to rule | Bible §2.7; Main Arc movement 12 | [PROPOSAL — DIRECTOR] D-8 |
| Flood Calendar Stones; "Magic is not taken, it is heard" | Dossier §VI, §XI | [CANON]. The First Listener is **not** referenced (C07 open). |
| Listening Steps, Oriel, the flow-table, the Braid gate rule | Bible §2.1, §2.7; this package | [NEW] |

## BF.3 Summary card

| Field | Value |
|---|---|
| Content id | `lowmark.main.09_behind_the_falls` |
| Prerequisite | MQ8 Completed |
| Offered | `MN-D7` end; starts at the Mantle Shrine at dawn |
| Target length | 25–35 minutes |
| Combat share | ~0–5% (one optional vermin pocket) |
| Skills touched | None required. This is a pilgrimage. |
| Choice | The promise → `LM_ORIEL_PROMISE` |
| Quest items | None |
| Unlocks | Braid knowledge; the Listening Steps as a revisitable place (outer channels only); MQ10 lead-in; VK *A Verse Kept Back* completion gate (bible §7) |

## BF.4 Places

| Area | Environmental storytelling |
|---|---|
| **A. End of the reeds** | The Path of Unburnt Reeds ends at a pale stone lip; the falls' sound arrives first as a feeling in the chest. The children's dare stake is far behind; nobody's footprints come this far. |
| **B. Plunge pool and outflow** | White water, spray rainbows at morning. Step-stones cross the narrow outflow. They are shaped, with a shallow cup in each top, worn by feet. |
| **C. Falls path** | Switchbacks cut into the cliff beside the falls; the stone is slick and green; iron rings, very old, set in the rock at the worst turns. |
| **D. The curtain** | A ledge passing behind the falling water. Light comes through the water, grey-green and moving. |
| **E. The Listening Steps** | Terraces of narrow carved channels stepping down into a hollow, moss trimmed neatly back from every edge. Tiny stone gates in slots. Each channel sounds a different note. **The sound is clear, not muffled.** Marking-Stone grooves on the channel walls, like the Whisperflow stone's. A tool niche: reed brushes, a wooden rake, a kneeling stone worn hollow. |
| **F. Flow-table chamber** | A wide round basin at the bottom of the Steps under a natural stone roof, open on one side to falls-light. |
| **G. The further way** | Beyond the chamber a passage is closed by a hanging reed screen. Oriel stands between it and everyone. It is not interactable, not marked and never explained. |

**MAP VERIFICATION REQUIRED:** Veilwater Falls at the far end of the Path of Unburnt Reeds from Ashenstead (bible §4.1).

## BF.5 Player-facing sequence

### Beat 0 — Dawn at the Shrine (`S00_set_out`)
**Objective:** *Meet the cutter at the shrine at dawn.*
`BF-D1` `[D-7]`. Short. Variants by `LM_SEDGE_TRUST`. Warm: *"Eaten? Good. It's a climb."* Cool: *"Keep up."* He sets off.

### Beat 1 — The Path (`S01_path`)
**Objective:** *Follow the cutter.*
Walk-with along the Path of Unburnt Reeds. Sedge walks at a working pace and stops when the player stops. Proximity barks (`BF-D2`), two to four of them, are his only talk; with warm trust he says a little more. At the dare stake, he touches it in passing, the only sign he's ever been here as anything but a cutter.

### Beat 2 — The Climb (`S02_climb`)
**Objective:** *Climb the falls path.*
Three segments. Each has an agility trigger with a walkable fallback:

| Segment | Agility trigger (approved, not built) | Walkable fallback |
|---|---|---|
| Step-stones across the outflow | Step-across, four stones | A lower ford in the shallows; slower; **BF-E1** optional Skitters there |
| The slick ledge | Ledge-shuffle along a wet face holding iron rings | Cut steps one turn further out, longer, in full spray |
| The last pitch | Hand-line climb on an old rope through the rings | Switchback stairs, worn and steep |

Spray reduces visibility on the ledge (presentation). Sedge waits at each landing and never helps. There's no fall damage, because no falls are possible on the walkable routes.
**Verbs:** traverse.

### Beat 3 — Behind the Curtain (`S03_curtain`)
**Objective:** *Go behind the falls.*
The player steps onto the curtain ledge (area D). See §BF.6, *The curtain*.

### Beat 4 — The Listening Steps (`S04_steps`)
**Objective:** *Look around.*
Inspect **three of five**: the **gates** ("Stone gates the size of a hand, in slots. Some up, some down. Somebody sets these."), the **trimmed moss**, the **tool niche**, the **grooves** ("The same groove and notch as the Whisperflow stone. Here they're cut into the walls, dozens of them."), the **singing channel** (if `TL_LEAD_NAN`: "Its note rises and falls. You know this tune. Nan hummed it by the fire."; otherwise "Its note rises and falls, like something hummed.").
Oriel is at work at a lower channel, clearing silt from a gate slot with a reed brush. Approaching starts nothing until the player has done three inspects. Then Oriel finishes the slot, sets the gate and stands (`BF-D3`) `[D-8]`.

### Beat 5 — Oriel (`S05_oriel`)
**Objective:** *Speak with the Riverwarden.*
`BF-D3`. Formal and unhurried. Oriel greets Sedge with no name and no ceremony (they know each other), asks the player what they came for, and answers by showing rather than telling: *"Come and see what you are standing in."*

### Beat 6 — The Flow-Table (`S06_table`) — *the wonder*
**Objective:** *Study the flow-table.*
See §BF.7 for the full presentation and interaction spec. Three parts: **find** (four inspect points on the table, three required), **the pulse** (Oriel opens the Cut), **the Braids** (the player plugs the scar and opens three gates in Oriel's order).

### Beat 7 — Why We Left (`S07_condition`)
**Objective:** *Hear Oriel's condition.*
`BF-D5` `[D-8]` at the table's edge. Why the Riverwardens withdrew (rulers asked for floods on command). What the Braids need (the gates opened in this order during a pulse, the Cut sealed for good, and many hands). The condition: the Vale must agree **in public** to tend the Braids together, and no house or office may own them. *"I will not hand a gate to a steward. I will teach it to whoever does the work, if all of them are in the room."*

### Beat 8 — The Promise (`S08_promise`)
**Objective:** *Give Oriel your answer.*
`BF-D6`. Three phrasings, all of them a yes (§BF.9). Sets `LM_ORIEL_PROMISE`.

### Beat 9 — The Foot of the Falls (`S09_down`)
**Objective:** *Go back down.*
The descent uses the same routes. At the plunge pool, Sedge's parting (`BF-D7`) varies by trust. He goes back to his reeds. The quest completes when `BF-D7` ends. The **MQ10 lead-in** objective appears: *Take Oriel's condition to Crest Hall.* (Act III owns it.)

## BF.6 The curtain and the Steps: presentation

| Moment | Spec |
|---|---|
| **The curtain** | On the ledge, the falls' roar is at full level (the loudest place in Lowmark). Light is grey-green and moving. At the ledge's midpoint a single step crosses a threshold volume, and the roar **drops by most of its volume in under a second**, as if a door had shut behind the player. It doesn't fade; it stops. Then the Steps' channels are audible, each its own note. Turning back, the player sees the falls from inside, silent-looking, a moving wall. |
| **The stillness** | Not the Whisperflow dead-spot behaviour. Sound here is **clearer** than outside: footsteps crisp, water notes distinct, Sedge's breathing audible. A place for listening, not a place where listening stops. |
| **Light** | Falls-light through the curtain on one side; moss green; limestone pale. No glow, no magical light source anywhere. |

## BF.7 The flow-table: presentation and interaction spec

The quest's centrepiece. It must feel like **looking at the whole Vale from above for the first time** and then understanding it with your own hands. It is a model, made by people, worked by people. Nothing in it is alive.

### BF.7.1 The object

| Element | Spec |
|---|---|
| Form | A round basin carved from one limestone floor, ~8 m across, waist-high rim, walkable around its full circumference. The player can lean on the rim anywhere. |
| Terrain | The Vale in low relief (**MAP VERIFICATION REQUIRED**: the table must match the final POI map; it is the map). The river and its branches are carved channels a finger wide. Raised berms, the orchard dikes and the Crestbridge span are tiny carved lines. Settlements are small flat stones with a single cut mark each. No words, no names, no labels anywhere. |
| The Braids | Dozens of hair-fine carved channels that split from the main river at bends and rejoin it lower down: a braided pattern visible everywhere once seen. Each split has a tiny **stone gate** in a slot, smaller than a fingernail. Most are set; some are choked with silt. |
| Marking Stones | At every crossing, a pin-sized notch stone. Whisperflow's has a single bright scratch beside it: someone here noticed the post was re-seated. |
| Water | Fed from the Steps' channels at the table's "upstream" edge. Water a few millimetres deep runs the real channels at a visible, slow pace. Tiny reed fragments drift on it, showing flow direction. |
| The fen | Where the river spreads: a shallow, many-channelled basin carved finer than anywhere else. The water there is clouded with a fine grey **silt** that settles slowly. |
| **The Cut** | From the fen's deep pools to the river below Crestbridge: **a straight, raw, hacked channel**. Its edges are chipped, not carved, with tool marks visible and no care taken. It cuts **through** five or six braided lines, severing them; their stubs end at its edge. It is the only ugly thing in the room. A clay plug sits beside the table on a stone ledge. |
| Light | Falls-light from the open side makes the water glitter. No other light. |
| Sound | Faint trickle; at the table's edge, each Braid makes a thin, distinct note when it carries water. A choked Braid is silent. |

### BF.7.2 Find (`S06a_find`)

The player walks around the rim. Inspect points glint faintly in the water (standard inspect highlight). Three of four are required, and every one gets a reaction from someone:

| Point | Inspect text | Reaction |
|---|---|---|
| **Whisperflow's bend** | "A wide bend. A notch stone at the crossing, and a fresh scratch beside it." | `TL_STONE_PUBLIC`: Oriel: *"Your keepers wrote one down. We heard."* `TL_STONE_KEPT`: *"Your crews keep one quietly. Good."* |
| **The orchards** | "Raised lines along a flood route. One run of dike is cut a hair lower than the rest." | Sedge: *"Ruddock's bank."* |
| **Ashenstead** | "A ring of tiny stones on a field, and a channel carved round it, not through it." | If done MQ5: player-recognition text, *"The guide-line. It goes round."* Sedge (warm only): *"Told you."* |
| **The fen** | "Fine channels, fine as hair, clouded grey. The cloud never quite settles." | Oriel: *"That is weight. Not a thing. Weight."* |
| **The Cut** (always required) | "Straight. Hacked, not carved. It cuts through the fine lines as if they weren't there." | Oriel: *"That is yours."* (said without blame: a fact) |

### BF.7.3 The pulse (`S06b_pulse`)

Oriel lifts a gate at the Cut's head on the fen's edge (Oriel's interaction; the player watches from anywhere on the rim):
1. The fen basin's water **drops** toward the Cut's mouth. The clouded silt **streams into the Cut** in a dark thread.
2. It runs down the straight channel **fast**, much faster than anything else on the table, and spills into the river below Crestbridge.
3. The severed Braid stubs **choke**: silt piles at their cut ends. Their notes stop one by one.
4. The silt spreads downstream into the orchard dikes, the Drowsebank channel and the Whisperflow bend. Little grey clouds settle into every low place on the table. **The player has stood in every one of them.**
5. Oriel closes the gate. The silt stays where it fell. *"Every flush. And when they stopped, the weight stayed in the fen with nowhere to go but the old ways."*

**It shows pressure and weight, not names.** No figure forms in the silt. Nothing moves that the water doesn't move.

### BF.7.4 The Braids (`S06c_braids`) — *the player's hands*

Oriel hands the player the clay plug (prop interaction): *"Shut it."*
1. **Plug the Cut** at its mouth (3 s channel). The fen basin's water stops falling. It **rises**, slowly, with no way out (the fen "holding its breath," readable at miniature scale).
2. Oriel indicates three fen-edge Braid gates, choked stubs the Cut once severed, now reconnected by fresh carved channels Oriel has cut into the table. *"The furthest from the Cut first. Each gate takes what the last one gives. The nearest last."* The three gates are distinguishable by position only (far, middle, near), never by name. **Act III names the real gates; this table teaches the rule.**
3. The player lifts the gates (3 s channel each).
   - **Correct order** (far → middle → near): each gate takes a share; the pressure **divides** into three braids, then into the finer braids below them. The silt thins as it spreads and **settles** in the old channels' pools. The notes return one by one until the whole table is sounding, a quiet chord. The fen basin clears from the edge inward.
   - **Wrong order:** the near gate takes everything at once; the silt bunches, overtops a tiny fen-edge stone (Reedmere's mark), and clogs the next gate. Oriel resets it (closes the gates; the silt slowly settles back): *"Again. Slower. The far one first."* No limit, no fail.
4. When the table is sounding, Oriel says nothing for a moment. Then: *"That is all we ever did. Gates, in order, by many hands, every season."*

### BF.7.5 Rules

| Rule | Spec |
|---|---|
| UI | None beyond standard inspect and interaction prompts |
| Camera | Player's own. The rim is walkable all the way round and every point is visible from the rim. |
| Repeatable | After the quest, the table is an inspectable object with the Cut plugged and the Braids sounding: *"The Vale, running as it was meant to."* The player can lift and drop the Braid gates freely afterward (no effect on the world). |
| Co-op | Per-player instance of the table state; partners see their own table state (fallback: the table runs a loop of the pulse and the braids for anyone in the chamber, and only the owning player's interactions advance steps) |
| Evidence rule | The table shows how water moves. It says nothing about who opened the Cut, who drowned in the fen, or what Marrick did. Those belong to records (MQ10). |

## BF.8 Encounters

| Id | Enemies | Placement | Purpose | Solo target |
|---|---|---|---|---|
| **BF-E1** | 2 Skitter swarms | Plunge-pool ford (fallback route only) | The walkable route carries a small cost; the agility route has none | Optional. Trivial at Competent level |

No other combat. Nothing behind the falls is hostile. Drawing a weapon at the Steps gets one Oriel line (`BF-D3.40`) and nothing else.

## BF.9 Steps, flags, the promise

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_set_out` | Meet the cutter at the shrine at dawn. | `BF-D1` end (keep watch to dawn if needed) | Yes |
| `S01_path` | Follow the cutter. | Walk-with reaches area A | Yes |
| `S02_climb` | Climb the falls path. | Enter curtain-ledge volume (any route) | Yes |
| `S03_curtain` | Go behind the falls. | Cross threshold volume (`bf.curtain_hush`) | Yes |
| `S04_steps` | Look around. | 3 of 5 inspects | Yes |
| `S05_oriel` | Speak with the Riverwarden. | `BF-D3` end | Yes |
| `S06_table` | Study the flow-table. | 3 of 4 find-inspects + Cut inspect; `bf.pulse` ends; `plug_cut` + 3 gates in valid order → `bf.braids_sound` | Yes |
| `S07_condition` | Hear Oriel's condition. | `BF-D5` end | Yes |
| `S08_promise` | Give Oriel your answer. | `BF-D6` choice node | Yes |
| `S09_down` | Go back down. | `BF-D7` end at the plunge pool | Yes |

| Flag | Set by | Read by |
|---|---|---|
| `LM_ORIEL_PROMISE` = aloud / many_hands / return | `BF-D6` | MQ12 (quoted back) |
| `BF_WRONG_ORDER` (int) | Gate attempts | `BF-D4` Oriel line only |

**The promise** (`BF-D6`; all three are yes; MQ12 quotes the player's exact words back):

| Value | The player says | Oriel |
|---|---|---|
| `aloud` | *"I'll say it in front of the whole Vale. Out loud, where everyone hears it."* | *"Then it will have been said. That is most of it."* |
| `many_hands` | *"Nobody will hold those gates alone. Not a steward, not a house. Not me."* | *"Not you either. Good. You heard that part."* |
| `return` | *"I'll come back and tell you whether they kept it."* | *"Then I will be here. I am usually here."* |

## BF.10 Rewards

| Reward | Type | Notes |
|---|---|---|
| Braid knowledge | Knowledge / story | The gate rule; the Cut must be sealed for good. Feeds MQ10 and MQ11. |
| The Listening Steps | Access | The outer channels stay visitable. Oriel is present at dawn and dusk with a short idle bark set. The further way stays shut. |
| No payment | — | Oriel has nothing to pay with and wouldn't. Sedge won't take anything either. The reward is the knowledge. |

## BF.11 Failure, recovery, co-op

| Situation | Handling |
|---|---|
| Death on the climb | Impossible on walkable routes; on the optional ford, respawn at area A |
| Wrong gate order | Unlimited retries; Oriel resets |
| Logout | Resume at the last completed step; inside the Steps, at the curtain ledge |
| Co-op | §BF.7.5. Sedge walks with each player's instance (per-player NPC; fallback: Sedge waits at area A and at the curtain for whoever is furthest behind). |

## BF.12 Mystery ledger, open decisions

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Reveal owner |
|---|---|---|---|---|---|
| What the Braids are | A distributed flood-tuning network built and tended by many hands; gates set by season. | Children's stories; "the listeners." | The flow-table; the grooves; Oriel. | A weapon; a battery; a spell. | This quest |
| Why the Riverwardens withdrew | Rulers asked for floods on command. Withdrawal was an ethical survival choice. | Extinct; cowardly; hoarding. | Oriel's account. | They caused the crisis to be needed again. | This quest (in outline; no leaders, dates or Founder named) |
| What lies past the reed screen | The inner oasis and Warden's Hearth. | Myth. | A closed passage. | — | Not in v1 |

**Open decisions:** (1) D-8 (Oriel). All Oriel nodes are tagged `[D-8]`. (2) **Riverwarden appearance.** This package describes Oriel by clothing, tools and manner only: grey work clothes, a reed apron, wet forearms. *Recommendation:* the Art Director sets the people's look; nothing here depends on it. (3) **The flow-table must match the final POI map.** It is the one asset where map geometry is narratively load-bearing.

## BF.13 Internal review log

| Finding | Revision |
|---|---|
| Oriel said water "remembers" and "wishes." That's spirit-talk. | Every Oriel line now uses work nouns: carry, scour, rest, weight, gate, season. |
| A draft let the flow-table show figures in the fen silt. That brushed the evidence rule. | Silt and pressure only. No shapes. |
| The withdrawal reason was a long speech. | Two lines and one concrete example (a road drowned on a named day), with the player in control throughout. |
| The table's gate order was a hidden puzzle. | Oriel states the rule plainly. The learning is in the hands, not in guessing. |
| An Oriel line quoted the First Listener. | Cut. Oriel uses the canon saying in a work sense only and attributes it to nobody (C07 stays open). |
| The promise options included a "no." | All three are yes, and differ in what the player commits to. Refusing would make MQ10 impossible, and the arc doesn't need a fake exit. |

---

## A2-INT. Act II shared integration requirements

These extend the True Line's §12 table. None is a new core system.

| Need | Used by | Owner | Minimum viable form |
|---|---|---|---|
| **Keep-watch time windows** | GL, TF, DK, MN, BF | Systems | One interaction that advances the player's local quest clock to a named window (`dusk`, `night`, `pulse`, `dawn`) and fires the window's scripted presentation. Per player. |
| **Per-player prop/terrain state** | GL fixes, TF floor bays, DK orchard flood, BF table | Systems (33.1.B2) | Client presentation keyed on local quest state. Fallbacks are in each package. |
| **Carry state** | GL stones/turf, TF beam, DK bundles | Systems | As MQ1. GL adds a rotation check on set-down. |
| **Channelled holds on NPCs and props** | TF gate, DK Bryn, MN Sedge | Systems | NPC/world-object state flags with interrupt-on-damage and timed recovery. |
| **Ordered-slot puzzle** | TF | Schema + Systems | §TF.14 |
| **Walk-with NPC** | MN, BF | Systems (35.x NPC behaviour) | Follow-path NPC that matches a slow pace and waits at checkpoints. Fallback: NPC waits at checkpoints only. |
| **Alert/flight wildlife behaviour** | MN elk (and DK elk charge) | Gameplay (Hunting F4) | Reuse the traveling-grazer framework; one quest-spawned instance per player. |
| **Drift-site state writes** | TF, DK, MN | Schema + Systems | Site id → state on step completion (§A2.7). |
| **Drift split behaviour** | MN | Gameplay + Systems | On dispersal at a flagged site, spawn N smaller variants at linked downstream points; cap depth at 2. |
| **Water presentation set** | GL dusk, TF pond lag, DK fold, MN inward rings, BF table | Art + Systems | All client-side and time-limited. No gameplay reads them. |
| **Flow-table model** | BF | Art + Zones | §BF.7. Must be built from the approved POI map. |
| **Cross-quest flag reads** | All | Schema | Dialogue show-conditions on `LM_*`, `TL_*`, `UR_*`, `GL_*`, `MN_*`. |

### A2-INT.1 Acceptance tests (act level)

1. A fresh Competent character completes MQ5→9 using only objectives and dialogue, in 2.5–3.5 hours total.
2. MQ5 and MQ6 complete in either order with correct cross-lines.
3. Each `LM_FIELD_FIX`, `LM_TOVIN_CREDITED`, `LM_BRYN_ROLL` and `LM_ORIEL_PROMISE` value is reachable in separate runs and persisted.
4. `LM_ORCHARD_LOSS` = none and = partial are both reachable; partial never blocks MQ8.
5. `LM_SEDGE_TRUST` = cool through each route (elk killed; "mage" answer) and = warm; MQ9 is offered in all cases.
6. The TF puzzle validator returns a contradiction for every wrong order tested; three wrong checks trigger Imber's line.
7. Death and logout at every set piece (TF hold, DK hold, MN quieting, BF table) resume without loss.
8. Two-player co-op completes each quest independently.

Playtest questions (the real bar): *What did the water do that water doesn't do? Who do you trust in the Vale now? What do you think the Cut is?*

## A2-REV. Act-level internal review

| Check | Result |
|---|---|
| **Canon anchors** | Joric: no age, service, kin or incident detail; avoids standing water; decides about his field himself. Annelise: knows which names never appear (she says so and names none); "light enough to carry" is her argument for lifting the stones. Tovin: describes, never explains, never names, never solves; the solver is the player, and the hint comes from Imber. |
| **Evidence rule** | Warm well, pond lag, water fold, inward rings, flow-table silt: none identifies a person, proves guilt or names the dead. The scratched marks stay unread. Combat carries no information (TF crew lines play before engagement). |
| **Soft-locks** | Every required proof has a guaranteed path: the TF validator plus Imber's hint; MN wrong stones re-inspectable; BF gate retries unlimited; GL Joric's agreement re-askable; DK rotten moss refused but re-cuttable. |
| **No fail** | DK slips cap at one section; TF bands cap at 3; elk death and the "mage" answer cool trust only. |
| **Duplicate structures** | Five distinct primary verbs (§A2.9). Two night-watches (GL dusk, TF loft) differ: one watches water, one watches people. The two holds (TF gate, DK Bryn) differ: one is the player's hands, the other is guarding someone else's. |
| **Flags** | Region flags set exactly as §A2.5. The quest-local flags other packages read are listed in §A2.8. No new `LM_` flags. |
| **Quest items** | 2 (`tovin_floor_sheets`, `riverglass_bowl`); within budget. |
| **Spellcasting** | None by the player. Bryn's and Sedge's practice is shown without light or words. Oriel's gates are stone and clay. |
| **Antagonist tags** | Sallow is named only in `TF-D3` and `TF-D8`, both tagged. Marrick is not named in Act II. |
| **Skills** | Melee, Woodcutting, Hunting, Cooking, Smithing (optional path). No Ranged, Fletching or Mining. |
| **Size discipline** | MQ7–9 packages are shorter than MQ5–6 by design; MQ8–9 are low-combat quests whose substance is in their presentation specs. |
