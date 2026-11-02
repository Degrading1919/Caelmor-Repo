# Lowmark v1 — Side Quests: Work and Skills

**Status:** Authored production content for Creative Director milestone review (bible §12, batch 3). Five skill-introduction side quests from `Caelmor_Lowmark_v1_Narrative_Production_Bible.md` §7: **WC** *The Wrong Culprit*, **BW** *The Bank Walk*, **FK** *The Flood Kitchen*, **BP** *Bark for the Pits*, **HS** *Honest Steel*. Everything here is **[NEW]** unless marked **[CANON]**. Consequential choices the content depends on are marked **[PROPOSAL — DIRECTOR]**. Markdown only: no schema, JSON or C#. Dialogue sits inline in each package, in the node format and voice rules of `Dialogue & Narrative/Caelmor_Lowmark_The_True_Line_Cast_and_Dialogue.md` (Part 1 binding).

---

## 0. Purpose and shared rules

These five quests are where a player first learns what a Lowmark skill is *for*. Each one teaches a real economy relationship from the approved economy design set through a physical job in a real place, not through a recipe list. Exact items, recipes, yields, stats, levels and XP belong to the item and balance passes; packages name outputs by their economy-design state (ordinary wood, tannin-rich bark, raw hide, vegetable-tanned hide leather, plain carbon steel stock, wood charcoal, rendered tallow, flax linen and tow) and name reward tools functionally.

### 0.1 Unlock gates and placement

| Code | Quest | Skill introduced | Core verb | Unlock (quest state, not spawn location; bible D-4) | Where | Length |
|---|---|---|---|---|---|---|
| WC | The Wrong Culprit | Hunting | track and judge | `lowmark.main.01_true_line` Completed | Ashenstead field margin and P20 burned barns | 20–30 min |
| BW | The Bank Walk | Woodcutting | cut selectively | `lowmark.main.01_true_line` Completed | Greyharrow side-branch bank (P05) | 20–30 min |
| FK | The Flood Kitchen | Cooking | hunt, cook, feed | `lowmark.main.01_true_line` Completed | Brookhollow low lanes and shelter (P01) | 20–30 min |
| BP | Bark for the Pits | Leatherworking | gather, process, make | `lowmark.main.02_short_measure` Completed | Brookhollow tan-yard (settlement edge), renewal coppice (P17) | 30–40 min |
| HS | Honest Steel | Smithing | inspect, forge, decide | `lowmark.main.02_short_measure` Completed | Crestbridge forge (P02) | 25–35 min |

All five are optional, solo-clearable, cannot fail, and give no lump quest XP (skill XP comes from the actions). Co-op partners run independent instances against shared world creatures. Side quests use **no quest items** (bible §11.6): every object is a carry-state prop, a station object, an inspect point, or an ordinary economy output.

### 0.2 Skill coverage and how the five feed one chain

```text
WC  Hunting (F2 rooter, H2 evidence) ──► food relationship ──► household
                                    └──► raw hide ───────────────┐
FK  Hunting (F3 reed-margin fowl, H3-lite) ──► food ──► Cooking ─┘(no hide: F3 is food-only)
BW  Woodcutting (S-WD3 bank-binding, W3) ──► ordinary wood (+ bark on the one authorized intact removal)
BP  Woodcutting (S-WD2 renewal coppice, W2) ──► ordinary wood + tannin-rich bark (guaranteed co-output)
        bark ──► tan-yard (ordinary labour: brake, leach) ──► tanning medium
        raw hide (WC, MQ1 boar, or yard stock) + medium ──► player Leatherworking ──► vegetable-tanned hide leather
        leather + flax thread (household textile labour) + rendered tallow (renderers) ──► Milestone 1 light protection
HS  outside production ──► lawful consignment ──► receiving inspection (player) ──► plain carbon steel stock
        stock + wood charcoal (fuel workers, fed by ordinary wood) ──► Smithing ──► Milestone 1 basic blade; heavy protection opened
        war salvage found in the consignment ──► excluded from routine supply (custody decision)
```

- **Hunting** is evidence-led stewardship (WC: read, judge, sometimes refuse; FK: respect a closed margin, keep the flock calm). Combat may resolve dangerous contact but never grants Hunting recovery (economy D02); field dressing is the recovery phase (D03).
- **Woodcutting** is selective (BW: the smallest cut that solves the bank; BP: only this year's ribboned stools). Bark only ever arrives as a co-output of a valid cut; there is no bark-only action anywhere in this file.
- **Leatherworking** is the player-facing hide-to-leather step inside an ordinary yard that keeps working without the player (economy D05, P-O4).
- **Smithing** begins with inspection of imported stock (P-O7). War salvage is finite and evidentiary, never supply (Minimum Coherent Material Set §2.1).
- **Cooking** is food as recovery before MQ3's first drift fights.

### 0.3 Equipment Milestone 1 ("dependable field equipment")

| Milestone 1 teaching outcome | Where it is met here |
|---|---|
| Basic melee weapon (commitment and recovery) | HS: the player forges their own first dependable blade from sound stock |
| Basic heavy protection | HS: Brigid opens heavy-protection work at the forge (definition belongs to the item pass) |
| Basic light protection | BP: the player makes their first light protection from leather they tanned |
| Repair and upkeep visible | BP (tallow conditioning, the yard's repair pegs) and HS (the rejects rack, Brigid's refurbish queue) |
| Basic guard-capable setup | **Not covered by these five.** Flagged for the item/encounter pass (Open questions, item 1). |

BP and HS end by establishing **Kell Ashby** (Riverpath Leathers, with Maelin's crews) and **Brigid Corliss** (Keeper's Blade, Bridgewarden Harness) as the people who will one day take a commission from the player (bible §8). The commissions themselves are not designed here; MQ12's `LM_CIVIC_STANDING` gates them.

### 0.4 Distinctness check

| Quest | Core verb | Physical problem | Strange or wonderful touch | Human choice with a cost |
|---|---|---|---|---|
| WC | track and judge | Read a ruined field; follow a trail; clear a raiders' barn | Goblins have replanted the stolen roots in rows of ash, with a notched plough-blade for a marker | Take the sow with farrow for a hungry household, or leave her |
| BW | cut selectively | Free a driftroot jam; fell a failing tree; decide which tree stays | Under the jam, an old knotted cord tied the way the child ties theirs | Keep the tree that holds the bank, cut it for the poorer household's landing, or give up your wood to build them one |
| FK | hunt, cook, feed | Light a dead kitchen; take fowl without scattering the flock; cook and serve | The geese go silent a breath before the water climbs a step with no rain | Who eats from the last pot |
| BP | gather, process, make | Clear fouled drawing-water; cut bark the honest way; charge a pit; tan; make | Tea-dark water has kept a strap with the yard's own old mark | What the yard does with bark stripped from living trees |
| HS | inspect, forge, decide | Ring-test a consignment; forge a blade; watch a bad bar crack | The bridge's old iron ties hum back when sound steel is struck | Hand the salvage to the Keepers (the carrier loses their cart for a season) or refuse it back marked (it stays in circulation) |

None repeats The True Line's investigate-and-repair loop or a §6 main-quest verb.

---

## WC — The Wrong Culprit

### WC.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `lowmark.side.wrong_culprit` |
| Type | Skill introduction (Hunting). Source: Hunting portfolio C1 *The wrong culprit*, presented at entry level with N2's guided structure. |
| Unlock | TL Completed. Offered by the smallholder at the field edge on approach. |
| Skills | Hunting (required: reading and tracking; optional: take and recover), Melee (required), Cooking (optional) |
| Combat share | ~20% (one required barn fight; one optional dangerous-contact hunt) |
| Choice | The sow with farrow: take her, leave her, or leave her and feed the household yourself |
| Unlocks | Crop-damage reading; the Ashenstead margin rooter opportunity (state set by the choice) |

**In one paragraph.** An Ashenstead smallholder wants every furrow boar on the margin killed: their root rows are ruined. The player reads the field and finds three kinds of damage, none of them fresh rooting: the rows were *cut*, a low corner drowned, and the boar sign in the hedge-gap is days stale. Small bare footprints lead off with a trail of dropped roots to the burned barn row, where Field Goblins have carried the crop. Inside, past the raiders, the goblins have replanted the stolen roots in neat rows in the ash and stuck a broken plough-blade at the end of the row with a notch scratched in it, like a crossing marker. The player carries back what can be saved. Then the smallholder's eldest is at the scrub margin with a boar spear: there *is* a sow there, rooting bracken, nowhere near the crop, with farrow in her bed. The household is still short of food. The player decides.

### WC.2 The place [NEW; MAP VERIFICATION REQUIRED]

A smallholding on the near margin of Ashenstead Fields, a short walk from the P20 burned barn row.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| A. Field edge | Hook | A root-crop plot in scorched-rye country. A boar skull nailed to the gatepost, old and sun-white. A spear leaning on the gate. |
| B. The cut rows | Evidence | Leaves sheared flat at one height; holes where roots were pulled clean; no turned soil between rows. |
| C. The low corner | Contrast | Rows drowned and yellow; a silt line on the stems; a ditch overtopped at its weakest bank. Water, not animals. |
| D. Hedge-gap | Contrast | Boar slots in crusted, rain-pitted mud; rooting in the gap itself, grown over with new shoots. Days old. |
| E. Carry-trail | Tracking | Small bare prints with toe-drag; a dropped root every few paces; a snapped hurdle stake with a rag tied round it as a handle. |
| F. Burned barn row (P20) | Combat; discovery | Three fire-gutted barns. Scrap armour and broken farm tools heaped as nests. In the last barn, the goblin field (WC.4). |
| G. Scrub margin | The judgment | Bracken torn up in wide patches well away from any crop; a bed in the brambles with small slots beside the big ones. The eldest waits here. |

### WC.3 Beats

**Beat 0 — Every Boar on the Margin (`S00_claim`).** *Objective: Find out what ruined the field.* The smallholder (role: HOLDER) wants boars killed. Dialogue `WC-D1`. The player is asked to hunt and is told, gently or not, to look first.

**Beat 1 — Read the Field (`S01_read_field`).** *Objective: Read the damage in the field.* Four inspect points (B, C, D, E start), any order, all required. Each plays one observation line. This is H2 evidence reading: rooting vs. cutting vs. water vs. stale sign.

**Beat 2 — Small Feet (`S02_follow_trail`).** *Objective: Follow the fresh trail.* Three tracking inspects along E (dropped root, rag-handled stake, rake-scratches in the ash at the barn door). The trail cannot be lost; every point is in sight of the last.

**Beat 3 — The Burned Barns (`S03_barns`).** *Objective: Drive the raiders out of the burned barns.* Encounter E1. When the last raider falls, the goblin field in the end barn becomes inspectable (WC.4).

**Beat 4 — What's Left (`S04_recover`).** *Objective: Carry back what's left of the crop.* Two sacks of roots from the goblin heaps (carry-state; lift, carry, set down at the field gate). The replanted rows stay where they are.

**Beat 5 — The Sow (`S05_margin`).** *Objective: Find the boars the household blamed.* At the scrub margin the eldest (role: ELDEST) has a spear and a plan. The player inspects the fresh rooting and the bed (two inspects). The sow is visible, feeding, inside her alert radius only if the player blunders in.

**Beat 6 — Judge (`S06_judge`).** *Objective: Decide what the margin needs.* Dialogue `WC-D6` (WC.7). If the player takes the sow, `S06a_hunt` opens: approach, resolve, then field dressing (Hunting recovery) gives the food relationship and raw hide.

**Beat 7 — Tell Them (`S07_report`).** *Objective: Tell the household what you found.* Dialogue `WC-D7`. Quest Completed.

### WC.4 The goblin field (discovery)

In the end barn, under the fallen roof, the stolen roots stand replanted in three straight rows in the ash, watered from a cracked trough. At the end of the middle row, a broken plough-blade is driven upright into the ground with a notch scratched into it at a hand's height. Inspect text: *"Planted. In rows. Someone has been watching how it's done."* Second inspect (the blade): *"A notch, scratched at the height of a crossing marker's. Copying the posts."* No UI fanfare, no music. It explains nothing about the water; it shows that the raiders watch the farms closely. The rows persist as a prop until UR (bible §7) changes the camp.

### WC.5 Encounters

| Id | Enemies | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **E1** | 3 × Field Goblin scrapper, 1 × Field Goblin trapper | Barn row, in two barns | Scrappers: Aggressive in the barn volume. Trapper: keeps distance, lays rake traps | Scrapper: hoe raised overhead (~1 s) then a short chop. Trapper: crouches and sets a rake (~1 s); the tines stay visible; stepping on one staggers the player briefly | First goblin fight; reading traps on the ground (MQ2 builds on it) | Required. 60–90 s; player ends at 50–70% HP |
| **E2** | 1 × Furrow Boar sow (only if `WC_SOW_TAKEN` is chosen) | Scrub margin bed | Hunting approach target. If alerted at close range she turns territorial | Bristles and snorts (~1.2 s), then a short straight charge; sidestepping makes her overrun and pause (~1.5 s) | Dangerous contact handed to combat (economy D02); recovery still needs field dressing | Optional. A careful approach resolves without a charge; a careless one is a 30–45 s fight |

The farrow are ambient wildlife, not targets: they scatter into the brambles and are never harvestable in this quest. Goblin heaps hold no evidence (the trail and field did the proving). Death: respawn at the field gate with step and carried-sack state reset to the heap.

### WC.6 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_claim` | Find out what ruined the field. | Dialogue `WC-D1` end node | Yes | Quest auto-offered on area-A entry |
| `S01_read_field` | Read the damage in the field. | 4 inspect events (cut rows, low corner, hedge-gap, trail start) | Yes | Any order |
| `S02_follow_trail` | Follow the fresh trail. | 3 inspect events along the trail | Yes | |
| `S03_barns` | Drive the raiders out of the burned barns. | All E1 creatures defeated | Yes | Goblin-field inspects enabled after |
| `S03b_field` | (Optional) Look at the planted rows. | Inspect event on plough-blade marker | No | Sets `WC_SAW_ROWS` |
| `S04_recover` | Carry back what's left of the crop. | 2 sack-deposit events at the field gate | Yes | Carry-state; sprint allowed |
| `S05_margin` | Find the boars the household blamed. | 2 inspect events (fresh rooting, bed) | Yes | |
| `S06_judge` | Decide what the margin needs. | Dialogue `WC-D6` choice node | Yes | |
| `S06a_hunt` | (If chosen) Take the sow cleanly. | Hunting recovery (field dressing) interaction complete on the sow | Conditional | Required only after `WC_SOW_TAKEN`. Field dressing yields the food relationship and raw hide |
| `S07_report` | Tell the household what you found. | Dialogue `WC-D7` end node | Yes | Quest Completed |

| Flag | Set by | Read by |
|---|---|---|
| `WC_SAW_ROWS` | `S03b_field` | `WC-D7` line; UR camp line (optional) |
| `WC_BARNS_CLEARED` | `S03_barns` | UR (*Unreplanted*): one line that the raiders came back to P20 |
| `WC_SOW_TAKEN` / `WC_SOW_SPARED` / `WC_SOW_SPARED_FED` | `WC-D6` (exactly one) | `WC-D7` variants; margin opportunity state; BP Kell line about the hide |

### WC.7 Choices and consequences

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Take the sow** — *"The household needs feeding. I'll take her, cleanly."* | The player hunts her (`S06a_hunt`). Food relationship and raw hide recovered. The household eats this week. | The farrow are left. The margin rooter opportunity **closes** at this site (authored state) until MQ5 is Completed ("till the young are grown"). | Raw hide is ready for BP. The eldest's bark: "She's the one that didn't do it." |
| **Leave her** — *"She didn't touch your roots. Leave her."* | The eldest lowers the spear. The margin opens now as a household-guided rooter opportunity (a different animal, on verified damage only). | The household goes short this week; the smallholder says so, flatly. | Ongoing H2 opportunity at this margin (economy N2/C1 reuse). |
| **Leave her, feed them** — *[player holds cooked food]* *"Leave her. Take this instead."* | As *Leave her*; the player gives one cooked food item. | The player's own food. | As *Leave her*, with the warmer `WC-D7` variant. |

No option is wrong. The quest never tells the player which is right; the smallholder and the eldest disagree with each other about it.

### WC.8 Rewards

| Reward | Type | Notes |
|---|---|---|
| **Reading damage** | Knowledge | Authored crop-damage props across Lowmark become inspectable and return a cause line: *"Rooted. Fresh."* / *"Rooted, but days old."* / *"Cut, not rooted."* / *"Drowned. Water did this."* Same inspect interaction as marker reading. |
| Margin rooter opportunity | Access | Open now (`WC_SOW_SPARED*`) or after MQ5 (`WC_SOW_TAKEN`). |
| Hunter's field knife | Tool | Given by the eldest at `WC-D6` if the player lacks a recovery tool. Item pass defines it. |
| Small payment | Currency / kind | A meal at the gate plus a few coins (amount at economy tuning); fewer coins on *Leave her*, since the household is short. |
| Hunting, Melee XP | Action XP only | No lump quest XP. |

### WC.9 Failure, recovery, co-op

| Situation | Handling |
|---|---|
| Death in E1 or E2 | Respawn at the field gate; step and flags kept; a dropped sack returns to the heap. |
| Player kills the sow before `S06_judge` | Not possible to soft-lock: the sow is non-interactive until `S05_margin` completes. |
| Player takes the sow but scares her off | She returns to the bed after a short delay; no idle wait (the player can report back and return). |
| Player has no recovery tool | Field knife at `WC-D6`. |
| Logout | Last step and flags restored; carries discarded. |
| Co-op | Shared E1 creatures give credit to each participant. The sow is per-player presentation once any instance chooses; a partner who chose *Leave her* does not see their sow taken. If per-player creature presentation is unavailable, fallback: each instance's sow is a separate spawn in the same bed. |

### WC.10 Integration needs

Steps/flags (31.3, 24.1); dialogue with item-held conditions (31.5); inspect and carry-state interactions (as TL); Hunting approach/resolve/recover hooks on the sow (Hunting interaction pass; D02/D03); authored opportunity state for the margin rooter (economy D04 vocabulary: open / closed-until); step-gated encounter pocket E1; quest-state-conditioned props (goblin rows; spear at the gate).

### WC.11 Dialogue

```
WC-D1.01 HOLDER: "If you're passing, pass. If you've got a blade, I've got boars."
WC-D1.02 HOLDER: "Whole root plot. Gone in two nights. Every boar on this margin, I want them gone."
  > "Show me the damage."                      → WC-D1.03
  > "Every boar? That's a lot of boars."        → WC-D1.04
  > "How do you know it was boars?"             → WC-D1.05
WC-D1.03 HOLDER: "Walk the rows. You'll see." (folds arms)                    → WC-D1.06
WC-D1.04 HOLDER: "It was a lot of roots."                                     → WC-D1.06
WC-D1.05 HOLDER: "What else digs up a field? Skull on the gate's from the last one."   → WC-D1.06
WC-D1.06 HOLDER: "Go on, then. Look. Then go and do something about it."
      {event: WC-D1 end → completes S00_claim}
```

**Inspect texts**

| Object | Text | Condition |
|---|---|---|
| Cut rows | "The leaves are sheared at one height. The roots were pulled, not dug. No soil turned between rows." | — |
| Low corner | "Drowned. A silt line on every stem. The ditch went over here, at its weakest bank." | — |
| Hedge-gap | "Boar slots, crusted and rain-pitted. The rooting here has new shoots in it. Days old." | — |
| Trail start | "Small bare prints, toes dragging under a load. They lead away from the gap, not into it." | — |
| Dropped root | "A root, dropped whole. Another a few paces on." | — |
| Rag-handled stake | "A hurdle stake, snapped. A rag tied round one end for a grip." | — |
| Barn door | "Rake-scratches in the ash. Someone drags their tools home." | — |
| Fresh rooting (scrub) | "Bracken torn up in wide patches. Fresh. Nowhere near a crop." | — |
| The bed | "A bed in the brambles. Big slots, and small ones beside them." | — |

**At the scrub margin** (opens on `S05_margin` complete; the ELDEST has the gate spear)

```
WC-D6.01 ELDEST: "There. See her? That's your boar."
WC-D6.02 ELDEST: "I'll go in from the bramble side. You go in from the open."
  > "She didn't touch your roots. The goblins did."             → WC-D6.03
  > "She's got young in that bed."                               → WC-D6.04
  > [WC_SAW_ROWS] "The goblins are planting your roots in their barn."   → WC-D6.05
WC-D6.03 ELDEST: "I know." (beat) "I saw the barns. We're still hungry."      → WC-D6.06
WC-D6.04 ELDEST: "I know that too. Young eat. So do we."                      → WC-D6.06
WC-D6.05 ELDEST: (stares) "...In rows?"                                       → WC-D6.08
WC-D6.08 ELDEST: "Better rows than ours, I'd bet." (rubs face) "We're still hungry."   → WC-D6.06
WC-D6.06 ELDEST: "You're the one who reads sign. You say."
  > [player has no recovery tool] (continue)                     → WC-D6.07
  > "The household needs feeding. I'll take her, cleanly."       → WC-D6.10
  > "Leave her. She's not the one."                              → WC-D6.20
  > [player holds cooked food] "Leave her. Take this instead."   → WC-D6.30
WC-D6.07 ELDEST: "You'll want this, whatever you do. Holder's knife." {give hunter's field knife}   → WC-D6.06 options
WC-D6.10 ELDEST: "Cleanly, then. I'll keep the young off you."
      {set WC_SOW_TAKEN; S06a_hunt active; event: S06_judge complete}  → end
WC-D6.20 ELDEST: (lowers the spear) "Holder'll say I went soft."
WC-D6.21 ELDEST: "If one does come for the roots, I'll know it by the sign now. Won't I."
      {set WC_SOW_SPARED; event: S06_judge complete}  → end
WC-D6.30 ELDEST: (takes it, looks at it a long moment) "...That's not nothing."
      {take 1 cooked food; set WC_SOW_SPARED_FED; event: S06_judge complete}  → end
```

**Report** (field gate, step `S07_report`)

```
WC-D7.01 HOLDER: "Well? Boars?"
WC-D7.02 [any] HOLDER: (sees the two sacks) "...That's my roots. Where were they?"
  > "In the burned barns. Goblins carried them off."             → WC-D7.03
WC-D7.03 HOLDER: "Goblins." (spits) "And the boars?"            → WC-D7.10 / .20 / .30 by flag
WC-D7.10 [WC_SOW_TAKEN] ELDEST: "We'll eat this week. She wasn't the one, mind."
WC-D7.11 [WC_SOW_TAKEN] HOLDER: "Didn't need to be." (beat) "No more off that margin till the young are grown. I'll see to it."
WC-D7.20 [WC_SOW_SPARED] HOLDER: "So I've two sacks and no meat and a boar in my scrub."
WC-D7.21 [WC_SOW_SPARED] HOLDER: "Fine. If one roots my rows, it's yours. Proper sign, mind."
WC-D7.30 [WC_SOW_SPARED_FED] HOLDER: "You gave us your own supper and left the boar. Odd sort of hunter."
WC-D7.31 [WC_SOW_SPARED_FED] HOLDER: "If one roots my rows, it's yours."
      (all variants → WC-D7.40 if WC_SAW_ROWS, else → WC-D7.50)
WC-D7.40 [WC_SAW_ROWS] HOLDER: "They planted them? In rows?" (long pause) "I'll be damned. Straighter than mine."
WC-D7.50 HOLDER: "Eat before you go. That's not a question."
      {small payment per WC.8; event: WC-D7 end → quest Completed}
```

**Barks**

| Trigger | Speaker | Line |
|---|---|---|
| E1 starts | GOBLIN (chitter) | (scraping of a hoe on stone) |
| Sack lifted | HOLDER (from the gate) | "Mind the split one. They're all split." |
| Post-quest, margin open | ELDEST | "Fresh rooting by the ditch. Come and look, if you're passing." |
| Post-quest, margin closed | ELDEST | "Young are growing. Nobody touches the scrub. Holder's orders." |

### WC.12 Review log

| Finding | Revision |
|---|---|
| First draft made the boar the culprit after all. | The sow is never responsible; the household's need is real anyway. The judgment is about need, not guilt. |
| Taking the sow risked reading as the "wrong" answer. | It feeds the household and supplies BP's hide; its cost is a closed margin, not a scolding. |
| Goblin field could read as comic relief only. | Kept small and inspect-only; the notched blade quietly echoes TL's markers and tells the player raiders watch farms. |
| Combat could have looked like it gave Hunting output. | Barn combat gives none; the sow's output comes only from field dressing (D02/D03). |

---

## BW — The Bank Walk

### BW.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `lowmark.side.bank_walk` |
| Type | Skill introduction (Woodcutting). Sources: lattice L-S01 *The Bank Walk*; Woodland portfolio C-WD2 *Relieve the bank obstruction* (S-WD3 bank-binding riparian tree, W3), presented at entry level with a guide. |
| Unlock | TL Completed. Offered at the staked bank on approach. |
| Skills | Woodcutting (required), Melee (light) |
| Combat share | ~10% (one small shallows swarm) plus one environmental hazard |
| Choice | Which bank-binding tree stays: keep it, cut it, or give up your wood to build the poorer household a landing |
| Unlocks | Bank reading; the lower bank path; persistent bank state |

**In one paragraph.** On Greyharrow's side branch, a child called Tamsin has tied a knotted measuring cord to a stake and chalked a cross on it: this bank is unsafe. Two households who share the bank disagree about whether a child's cord should stop spring work. Tamsin walks the bank with the player and makes them measure properly. The cord goes in an arm's length under the turf: the bank is hollow, scoured by a driftroot jam wedged at the bend. The player wades into the scour pool, cuts the jam's key limb, stands clear as it swings, and watches it let go. Snagged under it, on an old repair stake, is another knotted cord, rotten and green, tied exactly the way Tamsin ties theirs. Then the trees: one driftroot is failing and has to come down; one is healthy and its roots span the hollow, but it blocks the lower household's boat landing. The player chooses what the bank keeps.

### BW.2 The place [NEW; MAP VERIFICATION REQUIRED]

A stretch of the Greyharrow side-branch bank downstream of the town docks.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| A. The staked bank | Hook | A stake with a chalk cross and a knotted cord tied to it. Two households on either side of it. A wheelbarrow of spring stakes waiting. |
| B. Bank-top path | Measuring | The upper household's fence and field. A crack in the turf running parallel to the edge, a pace back. |
| C. Old repair face | History | Weathered stakes with a crew cut-mark on each; rotted wattle between them. Someone repaired this bank before anyone here was born. |
| D. Wrack line | Evidence | Reed and flood trash caught in branches above head height. The last high water came higher than the households say. |
| E. Scour pool and jam | Physical problem | A toppled driftroot trunk and debris wedged at the bend; water boiling under it into the bank. |
| F. Three driftroots | The choice | *The leaner*: root plate cracked, leaning out over the water. *The holder*: healthy, roots visible spanning the hollow. *The old one*: hollow, full of nesting holes; nobody would cut it. |
| G. Lower landing | Cost | The lower household's boat drawn up on mud, drying racks crammed in behind the holder's trunk. Every trip means hauling the boat round it. |

### BW.3 Beats

**Beat 0 — A Child's Cross (`S00_stake`).** *Objective: Find out why the bank is staked.* Dialogue `BW-D1` with Tamsin and both households (UPPER, LOWER; role-based).

**Beat 1 — Measure It Properly (`S01_walk`).** *Objective: Walk the bank with Tamsin's cord.* Tamsin leads. Three **Measure** interactions (2 s channel) at their knot points: the cord goes in a hand, then a forearm, then an arm's length under the turf. Plus one inspect on the wrack line. The old repair face is an optional inspect (`S01b_repair_face`). Tamsin comments on every measurement and corrects the player's grip once.

**Beat 2 — The Jam (`S02_free_jam`).** *Objective: Cut the driftroot jam free.* Reach the jam by an agility step down the root shelf, or walk the fallback cut-steps the upper household dug last year (slightly longer). Wading in starts E1 (River Skitters). Then the cut: one Woodcutting channel on the key limb. The jam **groans and shudders** (~1.5 s); a ripple ring on the water marks its swing arc. The player steps out of the arc. The jam swings, catches, and lets go down the branch. The trapped water drops away from the bank with one long sigh. Sound wood from the cut limb is ordinary wood; the flood trash is not an output.

**Beat 3 — The Other Cord (`S03_old_cord`, optional but signposted).** Where the jam was, an old repair stake stands in the scour with a rotten knotted cord tied to it: the same knot spacing, the same hitch. Inspect text: *"A measuring cord, green with age, tied off at the same marks as Tamsin's. Someone measured this bank the same way, a long time ago."* Tamsin's reaction is the wonder (`BW-D3`). Nothing supernatural; nobody can say whose it was.

**Beat 4 — The Leaner (`S04_leaner`).** *Objective: Bring down the failing tree.* Inspect the three driftroots (three lines). The leaner must come down: two Woodcutting channels (notch, then back-cut) with a fall telegraph (creak, the crown sways ~2 s); it falls along Tamsin's chalk line onto the bank-top. This is an authorized intact removal of a bank-binding tree, so it yields ordinary wood **and** tannin-rich bark (S-WD3 conditional eligibility).

**Beat 5 — The Holder (`S05_choose`).** *Objective: Decide which trees stay.* Dialogue `BW-D5` at the holder, both households present. Three options (BW.6). Option *Build the landing* adds two channelled **Seat the stage** interactions at area G after the player gives ordinary wood to the lower household.

**Beat 6 — Heard (`S06_heard`).** *Objective: Tell the households what the bank needs.* Short closing `BW-D6`: the upper household agrees to re-stake the repair face; Tamsin is given the cord each spring because they are careful, not because they are special (L-S01 payoff). Quest Completed.

### BW.4 Encounters and hazards

| Id | Enemies / hazard | Placement | Role | Telegraph | Solo target |
|---|---|---|---|---|---|
| **E1** | 5 × River Skitter | Scour pool (water volume only) | Swarm; leashed to water | Ripple line toward the player (~0.8 s), then a nip | Required on first wade. 20–30 s; little damage. Stepping onto the root shelf breaks contact |
| **H1** | Jam swing | Scour pool | Environmental | Groan, shudder, ripple ring on the water (~1.5 s) | Standing in the ring: knocked back, small damage. Cannot kill a player above a quarter health |
| **H2** | Leaner fall | Bank-top | Environmental | Creak and crown sway (~2 s); chalk line shows the fall | Falls along the chalk line; a player standing on the line is pushed clear with small damage |

### BW.5 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_stake` | Find out why the bank is staked. | Dialogue `BW-D1` end node | Yes | |
| `S01_walk` | Walk the bank with Tamsin's cord. | 3 `measure` interactions + wrack-line inspect | Yes | Tamsin follows the player (NPC escort-lite; cannot be harmed) |
| `S01b_repair_face` | (Optional) Look at the old repair face. | Inspect event | No | Unlocks a `BW-D6` line |
| `S02_free_jam` | Cut the driftroot jam free. | Interaction `cut_jam` complete | Yes | Disabled while any E1 creature is engaged |
| `S03_old_cord` | (Optional) Look at what the jam was hiding. | Inspect event on old cord | No | Sets `BW_OLD_CORD_SEEN`; triggers `BW-D3` |
| `S04_leaner` | Bring down the failing tree. | 3 driftroot inspects + interactions `notch` and `back_cut` complete | Yes | Yields ordinary wood + bark |
| `S05_choose` | Decide which trees stay. | Dialogue `BW-D5` choice node; for *Build*, item-given (ordinary wood) + 2 `seat_stage` interactions | Yes | |
| `S06_heard` | Tell the households what the bank needs. | Dialogue `BW-D6` end node | Yes | Quest Completed |

| Flag | Set by | Read by |
|---|---|---|
| `BW_OLD_CORD_SEEN` | `S03_old_cord` | `BW-D6`; SB/VK Tamsin barks (optional) |
| `BW_BANK_KEPT` / `BW_BANK_CUT` / `BW_LANDING_BUILT` | `BW-D5` (exactly one) | Bank props (persistent); Greyharrow barks; SB package |
| `BW_TAMSIN_HEARD` | `S06_heard` (always) | SB (*The Silent Bell*) Tamsin opening line; Greyharrow micro-event barks |

### BW.6 Choices and consequences

| Option | Immediate result | Cost | Persistent bank state |
|---|---|---|---|
| **Keep the holder** — *"Leave it. Its roots are the bank."* | The bank holds; the upper household's fence stays. | The lower household keeps hauling their boat round the trunk. LOWER: "So we carry it. Again." Delay lands on the household least able to spare it (L-S01). | Holder stands; repair face re-staked; landing unchanged. |
| **Cut the holder** — *"Take it down. They need the landing."* | Two more cut channels; the landing opens. The player gets ordinary wood and tannin-rich bark. | After MQ3 is Completed (the season turns), the hollow section slumps a pace; the upper household's fence is moved back (prop). UPPER: "We lost a row to that." | Holder gone; landing open; slumped edge. |
| **Build the landing** — *"Keep it. I'll build them a landing from the leaner."* | The player gives ordinary wood (the leaner's, or any ordinary wood of the same amount) to the lower household and seats a plank stage beside the holder. | The player's wood and time. | Holder stands; small landing stage below it. |

### BW.7 Rewards

| Reward | Type | Notes |
|---|---|---|
| **Reading a bank** | Knowledge | Authored bank-binding trees across Lowmark become inspectable with one line: *"Roots are holding the bank."* / *"Root plate's failing."* / *"It's in the way, but it's holding."* Supports later W3 work (economy C-WD2, A-WD1). |
| Lower bank path | Access | A walkable path along the side branch past the cleared bend (destination awaits the POI map). |
| Small payment | Currency | Pooled by the households; amount at economy tuning. |
| Ordinary wood, tannin-rich bark | Outputs | From the jam limb (wood only) and the leaner (wood + bark); also the holder if cut. Ordinary inventory, not quest items. |
| Woodcutting, Melee XP | Action XP only | No lump quest XP. |

### BW.8 Failure, recovery, co-op

| Situation | Handling |
|---|---|
| Death in the scour pool | Respawn on the bank-top; jam state kept if already cut. |
| Player has no cutting tool | The upper household lends a "bank axe" at `BW-D1`, kept at completion. Item pass defines it. |
| Player has sold the leaner's wood before *Build* | Any ordinary wood of the required amount is accepted (ordinary wood is one state, D11). If the player has none, the option is shown but greyed with: "You'll need wood to give." They can cut the leaner's stump-side limbs (one more channel) for enough. No soft-lock. |
| Logout | Last step restored; jam and leaner states persist once cut. |
| Co-op | Each instance has its own jam, leaner and holder presentation. Fallback if per-player props are unavailable: the jam is pre-cleared for later instances and `S02_free_jam` becomes "Cut the last of the jam free" on a remaining limb. The holder choice is stored per player; the shared world shows the holder standing until the server supports per-player tree states. |

### BW.9 Integration needs

Measure and cut channels (3 s class, cancel on move or damage); escort-lite follow for Tamsin (no combat AI, invulnerable, waits at each knot point); environmental hazard volumes with telegraph (H1, H2); persistent per-player prop states for the bank (holder standing/cut, slump, stage); item-given of ordinary wood with an amount check; tree-fall direction fixed by authoring (no physics dependency).

### BW.10 Dialogue

Tamsin is bossy and precise and wants to be taken seriously. They are never cute on purpose.

```
BW-D1.01 TAMSIN: "Don't stand there. That's the bad bit. I measured."
BW-D1.02 UPPER: "That child's been out with that cord all week. We've stakes to set before the planting."
BW-D1.03 LOWER: "And I've a boat that won't get past that tree. Every day it's 'wait'."
BW-D1.04 TAMSIN: "It's hollow underneath. I put the cord in and it went in."
BW-D1.05 UPPER: "Cords go in mud, love. That's what mud does."
  > "Show me where you measured, Tamsin."               → BW-D1.10
  > "Has anyone else looked?"                           → BW-D1.06
  > [player has no cutting tool] "I'll need an axe if there's cutting."   → BW-D1.08
BW-D1.06 LOWER: "We've all looked. Looks like a bank."
BW-D1.07 TAMSIN: "Looking isn't measuring."                             → BW-D1 options
BW-D1.08 UPPER: "There's the bank axe. Bring it back." (beat) "Or don't. It's older than me."   {give bank axe}   → BW-D1 options
BW-D1.10 TAMSIN: "Fine. But you hold it how I say."
      {event: BW-D1 end → completes S00_stake}
```

**Measuring barks** (Tamsin, one per knot point)

| Point | Line |
|---|---|
| First | "Flat to the bank. Flat. Now push." (the cord goes in a hand) "See?" |
| Grip correction (once) | "Not like that. Like you're holding a bird." |
| Second | "That's a forearm. Banks aren't supposed to have forearms in them." |
| Third | "Arm. Whole arm." (quietly) "I didn't tell them it was a whole arm. They'd have said I made it up." |
| Wrack line | "That's where the water got to. Higher than anyone says. I checked twice." |

**Inspect texts**

| Object | Text |
|---|---|
| Turf crack | "A crack in the turf, a pace back from the edge, running with it." |
| Old repair face | "Weathered stakes, each with the same cut-mark. Wattle rotted between them. Somebody kept this bank once." |
| Wrack line | "Reed and flood trash in the branches, above head height." |
| The jam | "A toppled driftroot and a winter's debris, wedged at the bend. The water goes under it, into the bank." |
| The leaner | "Root plate cracked through. It's leaning further than it was." |
| The holder | "Healthy. Its roots run straight across the hollow, like ribs." |
| The old one | "Hollow, full of nesting holes. Holding nothing up but birds." |

**The other cord** (`BW-D3`, triggered by the old-cord inspect if Tamsin is near)

```
BW-D3.01 TAMSIN: (crouches; doesn't touch it) "That's my knots."
BW-D3.02 TAMSIN: "That's how I tie it. Every arm-span, double, then the hitch."
  > "Who taught you to tie it like that?"            → BW-D3.03
  > "Someone measured this bank before you."         → BW-D3.05
BW-D3.03 TAMSIN: "Nobody. I worked it out. It's the best way."
BW-D3.04 TAMSIN: (pause) "Somebody else worked it out too, then."               → end
BW-D3.05 TAMSIN: "And nobody listened to them either, probably." (beat) "It's still here, though."   → end
```

**The holder** (`BW-D5`, step `S05_choose`)

```
BW-D5.01 LOWER: "That one. That's the one that's been in my way for nine years."
BW-D5.02 UPPER: "That one's holding my field up, by the look of it."
BW-D5.03 TAMSIN: "Its roots go right across the hollow. I can show you."
BW-D5.04 LOWER: "And I'll keep dragging my boat round it for another nine, will I?"
BW-D5.05 UPPER: (to the player) "You've cut two today. You choose the third."
  > "Leave it. Its roots are the bank."                                   → BW-D5.10
  > "Take it down. They need the landing."                               → BW-D5.20
  > "Keep it. I'll build them a landing from the leaner."                → BW-D5.30
BW-D5.10 LOWER: "So we carry it. Again." (beat) "Fine. Fine."
BW-D5.11 UPPER: "I'll help you carry it. Some mornings."
      {set BW_BANK_KEPT; event: S05_choose complete}  → end
BW-D5.20 UPPER: "Then I'll move my fence back before it moves itself."
BW-D5.21 TAMSIN: "It'll slump. Not today. When the water's next high." (flat) "I'm only saying."
      {S05 adds two cut channels on the holder; set BW_BANK_CUT; event on second channel: S05_choose complete}  → end
BW-D5.30 LOWER: "A landing. Below the tree." (looks at it) "That'd do. That would actually do."
BW-D5.31 TAMSIN: "Put it on the downstream side. The upstream side's where it scours."
      {item-given: ordinary wood → LOWER; two seat_stage interactions; set BW_LANDING_BUILT; event: S05_choose complete}  → end
```

**Heard** (`BW-D6`)

```
BW-D6.01 UPPER: "Well. The cord was right."
BW-D6.02 [S01b_repair_face] UPPER: "Those old stakes. I'll re-set them where the old ones stood. Same marks."
BW-D6.03 LOWER: "And who measures it next spring?"
BW-D6.04 TAMSIN: (says nothing, very loudly)
  > "Tamsin. Tamsin's careful."                                   → BW-D6.05
  > "Whoever's careful. Today that was Tamsin."                → BW-D6.05
BW-D6.05 UPPER: "Tamsin, then. Every spring. And you tell us, and we listen, and that's that."
BW-D6.06 [BW_OLD_CORD_SEEN] TAMSIN: "I'm keeping the old cord. Not to use. Just keeping it."
BW-D6.07 TAMSIN: "You held it nearly right, by the end." 
      {set BW_TAMSIN_HEARD; small payment; event: BW-D6 end → quest Completed}
```

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| LOWER | "Still carrying the boat. Still here." | `BW_BANK_KEPT` |
| UPPER | "Lost a row. Gained a landing for them. It evens out, probably." | `BW_BANK_CUT` |
| LOWER | "Landing's good. Tamsin inspects it. Weekly." | `BW_LANDING_BUILT` |
| TAMSIN | "I measured the docks. Don't stand on the third plank." | `BW_TAMSIN_HEARD` |

### BW.11 Review log

| Finding | Revision |
|---|---|
| L-S01 warns against making the child a secret expert. | Tamsin is right because they measured, and gets the job because they are careful. The old cord is wonder, not a lineage. |
| A "cut everything that's in the way" path would teach clearing. | Only the failing tree must come down; the healthy one is a choice with a cost either way (economy W3). |
| Bark could have appeared from every cut. | Only the authorized intact removals (leaner, holder) give bark; the jam limb gives wood only (S-WD3 conditional eligibility). |
| Original slump was immediate, which felt punitive. | Delayed to after MQ3 (a season later), so the consequence arrives as a changed place, not a scolding. |

---

## FK — The Flood Kitchen

### FK.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `lowmark.side.flood_kitchen` |
| Type | Skill introduction (Cooking, with Hunting). New; built on Nan Ferrin (TL). Hunting follows portfolio F3 reed-margin flocking game (H3-lite, guided; the closure boundary from C2). |
| Unlock | TL Completed. Offered on entering the Brookhollow shelter. |
| Skills | Cooking (required), Hunting (required, entry level), Woodcutting (optional: wood for the fire) |
| Combat share | ~5–10% (optional geese, optional leech) |
| Choice | Who eats from the last pot |
| Unlocks | The shelter kitchen as a public Cooking station; flock reading; food-as-recovery taught before MQ3 |

**In one paragraph.** A night rise with no rain put Brookhollow's low lanes under water to the knee. The displaced families are in an empty grain warehouse on the high street, the hearth is cold, and Nan Ferrin, who got as far as her own door before she heard and turned straight round, is running a kitchen with no fire and not much food. The player gets the fire going, goes down to the reed margin below the docks for fowl, keeps clear of the nesting stakes, takes birds without scattering the flock into the deep water, and cooks. While the first pot is on, every goose on the river goes quiet at once, and a breath later the water at the shelter's bottom step climbs a hand and stops. No wind. No rain. Then there is one pot short, and Nan asks the player who should have it.

### FK.2 The place [NEW; MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling |
|---|---|---|
| A. The low lanes | Arrival | Water to the knee between houses. Doors chalked with a ring (empty, everyone out). A skiff poling door to door. A chair floating upright, as if waiting. |
| B. The shelter | Hub | An empty grain warehouse: families on sacking, wet clothes on the rafters, Nan's trunk again, Duchess the hen on it. A wall of old chalked flood lines, each with a season beside it; the oldest are highest. Children have added tonight's line. It is lower than most. |
| C. Field kitchen | Cooking station | A fire pit under the loading door, pot crane, a cold kettle, Nan's stores in a crate (barley, roots, salt). Wet wood stacked uselessly. |
| D. Reed margin | Hunting | Below the docks. An open section marked with a plain stake; a closed nesting section marked with rag-tied stakes. The flock feeds between them. |
| E. Recovery shallows | Recovery | Soft footing at the margin's edge where downed birds land. A River Leech in the deeper part. |

### FK.3 Beats

**Beat 0 — Hands (`S00_shelter`).** *Objective: Find out who's running the shelter.* Entering the shelter volume opens `FK-D1` with Nan.

**Beat 1 — A Dead Hearth (`S01_fire`).** *Objective: Get the kitchen fire going.* The stacked wood is soaked. Either give ordinary wood from inventory (item-given), or climb the warehouse loft ladder and carry down two crates of dry slats (carry-state; ladder is a walkable stair, no jump). Then **Light the fire** (3 s channel).

**Beat 2 — The Margin (`S02_fowl`).** *Objective: Bring back fowl from the open margin.* A guided Hunting opportunity (Read–Prepare–Approach–Resolve–Recover):
- **Read:** inspect the feeding traces and the sentinel bird on the bank (two inspects).
- **Approach:** through reed cover. The flock's alert is readable: heads up and a single honk is the warning (~1.5 s); a second honk lifts the flock. If the flock lifts, it resettles on the far end of the open section within a short walk; the player never waits idly.
- **Closed ground:** the rag-staked nesting section is closed. Entering it triggers a child's bark from the docks and two Marsh Fen Geese defend (E1); fowl there cannot be taken in this quest.
- **Resolve and recover:** downed birds fall in the recovery shallows (wet footing; optional E2). The quest needs two recovered fowl (count set by the Gameplay Designer). F3 is food-only: no hide, no feather output.

**Beat 3 — The Pot (`S03_cook`).** *Objective: Cook for the shelter.* Cooking station interaction using the fowl and Nan's stores. Exact recipe and output belong to the item pass; the quest accepts any edible cooked result and needs enough portions for the shelter (Gameplay Designer). During the first cook the **hush** plays (FK.4).

**Beat 4 — Feed Them (`S04_feed`).** *Objective: Feed the shelter.* Give a cooked portion to four households (item-given). Each gives a one-line bark. When the fourth is fed, Nan counts the crate.

**Beat 5 — The Last Pot (`S05_choose`).** *Objective: Decide who eats from the last pot.* `FK-D5`. Nan's stores make one more pot. The lane crew (who will clear the lanes at first light) and the lane-end family (carried out last, two children) both need it. FK.6.

**Beat 6 — Your Own Bowl (`S06_eat`).** *Objective: Eat something yourself.* Nan puts a bowl in the player's hands: the tutorial for eating to recover health between fights. `FK-D6` closes the quest.

### FK.4 The hush (presentation spec)

| Element | Spec |
|---|---|
| Trigger | Server event on first completion of the Cooking interaction in `S03_cook`. |
| Sequence | ~8 s. The geese on the river, audible all quest, stop at once. The shelter goes quiet a beat later. The flood water at the shelter's bottom step climbs one step-height, smoothly, with no wave and no wind (~3 s), holds, and stays. Talk resumes. |
| Camera / UI | Player-controlled; no UI, no music. |
| Meaning | None stated. Author truth: this is a Hollow Lock flush (bible §2.2), a human act; the geese hear the river change first. Nan: "Did that last night too. No rain." It identifies nobody and proves nothing. It plants the question MQ3 and MQ4 answer. |
| Repeat | Once per player. Afterward the step's waterline stays one step higher. |

### FK.5 Encounters

| Id | Enemies | Placement | Role | Telegraph | Solo target |
|---|---|---|---|---|---|
| **E1** | 2 × Marsh Fen Goose | Closed nesting section only | Defensive; do not pursue past the rag stakes | Neck stretch and hiss (~1 s) before a wing-beat | Avoidable; leaving the closed section ends it |
| **E2** | 1 × River Leech | Deep end of the recovery shallows | Aggressive, slow, leashed to water | Rears (~1.2 s) before latching; stepping onto the bank breaks the latch | Optional; birds can be recovered without entering its water |

Taking fowl is a Hunting resolution, not a combat kill; recovery is the Hunting recovery interaction on the downed bird.

### FK.6 Choices and consequences

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **The lane crew** — *"The crew. They're clearing the lanes at first light."* | The crew eat and go out at dawn; the shelter empties a day sooner (props). | The lane-end family's children eat bread and the end of Nan's own bowl. Nan says nothing about it, which is worse. | MQ12 Nan scene: "Lanes were clear by noon. You fed the right ones. Probably." |
| **The lane-end family** — *"The family. The children first."* | The children eat; Nan smiles at the player properly. | The crew work hungry; the lanes clear a day later; the shelter holds another night (props). | MQ12: "Those two still ask after you. And the crew still complain." |
| **Your own food** — *[player holds cooked food]* *"Both. Put this in as well."* | The player gives cooked food from their own inventory (item-given; any cooked food). Everyone eats. | The player's own supplies (which they may need before MQ3's fights). | MQ12: "You went out of here with nothing in your pack. I noticed." |

### FK.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_shelter` | Find out who's running the shelter. | Dialogue `FK-D1` end node | Yes | Auto-offered on shelter entry |
| `S01_fire` | Get the kitchen fire going. | (item-given: ordinary wood **or** 2 crate-deposit events) + interaction `light_fire` complete | Yes | |
| `S02_fowl` | Bring back fowl from the open margin. | 2 Hunting recovery interactions complete on open-section fowl | Yes | Read inspects are prompts, not gates |
| `S03_cook` | Cook for the shelter. | Cooking interaction(s) at the shelter station produce the required portions | Yes | Fires the hush once |
| `S04_feed` | Feed the shelter. | 4 item-given events (cooked food) to shelter households | Yes | Any cooked food counts |
| `S05_choose` | Decide who eats from the last pot. | Dialogue `FK-D5` choice node | Yes | |
| `S06_eat` | Eat something yourself. | Dialogue `FK-D6` end node | Yes | Eating the bowl is prompted, not required. Quest Completed |

| Flag | Set by | Read by |
|---|---|---|
| `FK_HUSH_SEEN` | Hush event | `FK-D3` line; Ansel's MQ3 opening (optional line: "Brookhollow too?") |
| `FK_POT_CREW` / `FK_POT_FAMILY` / `FK_POT_OWN` | `FK-D5` (exactly one) | Shelter props; MQ12 Nan scene; VK Nan lines |
| `FK_NAN_TUNE` | `FK-D6` tune exchange | VK (*A Verse Kept Back*) Nan opening variant |

### FK.8 Rewards

| Reward | Type | Notes |
|---|---|---|
| Shelter kitchen | Access | The warehouse fire pit stays as a public Cooking station in Brookhollow. |
| **Reading a flock** | Knowledge | Sentinel birds on Lowmark margins become inspectable: *"Heads down. Feeding."* / *"One's watching. Go slow."* (F3 group alert, H3). |
| Nan's bowl | Consumable | One cooked portion (item pass), the eating tutorial. |
| Small payment | Currency | From the crew (*crew*) or the shelter's collection tin (*family*, *own*); amount at economy tuning. Nan pays "in soup". |
| Cooking, Hunting XP | Action XP only | No lump quest XP. |

### FK.9 Failure, recovery, co-op

| Situation | Handling |
|---|---|
| Flock scattered | Resettles on the far end of the open section; a second scatter sends it back to the first end. Always available. |
| Cooking produces a failed result (if Cooking can fail) | Nan's crate covers repeat attempts for the quest's needs; fowl are not consumed by a failed attempt, or two spare fowl remain available on the margin. |
| Player enters closed ground | E1 drives them out; no penalty beyond the geese. |
| Death | Respawn at the shelter; step and flags kept. |
| Logout | Last step restored; carried crates discarded; cooked portions are ordinary inventory and persist. |
| Co-op | Shared flock: one player scattering it scatters it for both (that is the lesson). Each instance's shelter feeding and choice are per player. |

### FK.10 Integration needs

Cooking station binding at the shelter (33.5-style station); Hunting opportunity hooks for F3 (shared alert-and-movement framework per the Hunting portfolio, with an authored resettle point); closed-ground volume that disables take and triggers E1; item-given counting any cooked food; the hush as one client presentation event (audio duck on the geese bus, water plane step-height change kept per player); per-player shelter props (families present/leaving).

### FK.11 Dialogue

```
FK-D1.01 NAN: "Oh good. Hands. Are those hands? Come here with them."
FK-D1.02 NAN: "I got as far as my own front door. Heard the low lanes had gone under. Turned straight round."
FK-D1.03 NAN: "My bed will keep. Their supper won't."
FK-D1.04 NAN: "Fire's dead. Wood's wet. Pot's empty. Duchess is no help at all."
  > "Where do I start?"                                  → FK-D1.10
  > "What happened to the lanes?"                        → FK-D1.05
  > "You were at Whisperflow."                           → FK-D1.07
FK-D1.05 NAN: "Water came up in the night. No rain, no wind. Just up."
FK-D1.06 NAN: "Everyone says the river's in a mood. Rivers don't have moods. People do."   → FK-D1 options
FK-D1.07 NAN: "And you carried my trunk. I remember. Carry something else."               → FK-D1 options
FK-D1.10 NAN: "Dry wood. The loft has old crates if you've none. Then fowl. The geese below the docks are fat and rude."
FK-D1.11 NAN: "Stay off the nesting stakes or the children will skin you before the geese do."
      {event: FK-D1 end → completes S00_shelter}
```

**Inspect texts**

| Object | Text |
|---|---|
| Flood-line wall | "Chalked lines, each with a season. The oldest are highest. Tonight's is lower than most." |
| Wet woodpile | "Soaked through. It'll smoke and sulk." |
| Feeding traces | "Fresh droppings and torn weed at the soft edge. They've been here all day." |
| Sentinel bird | "One goose with its head up while the others feed. Watching." |
| Rag stakes | "Stakes with rags tied on. The nesting ground. Closed." |

**Margin barks**

| Trigger | Speaker | Line |
|---|---|---|
| Enter closed section | CHILD (from the docks) | "Not there! That's the nesting stakes! I'm telling Nan!" |
| First honk (warning) | — | (one goose, one honk; the flock's heads come up) |
| Flock lifts | DOCKHAND (role) | "There they go. They'll be back at the far end. They always are." |

**The hush** (`FK-D3`, on the hush event, if within 10 m of Nan)

```
FK-D3.01 NAN: (watching the bottom step; quiet) "...Did that last night too."
FK-D3.02 NAN: "No rain."
  > "What was it?"                       → FK-D3.03
  > "The geese went quiet first."        → FK-D3.04
  > (Say nothing.)                       → FK-D3.05
FK-D3.03 NAN: "Water, love. Doing something water doesn't do." (stirs) "Pot's catching."   → end
FK-D3.04 NAN: "They would. They live on it." (stirs) "Pot's catching."                     → end
FK-D3.05 NAN: (stirs) "Pot's catching."                                                    → end
```

**Feeding barks** (one per household, item-given)

| Household | Line |
|---|---|
| DOCK FAMILY | "Hot. Something hot. You've no idea." |
| OLD COUPLE | "He won't say thank you. Thank you." |
| CARTER (role) | "If you ever need anything carted. Anything. Not uphill." |
| MOTHER AND CHILD | "Say thank you." / "It's got a bone in." / "Say thank you." |

**The last pot** (`FK-D5`)

```
FK-D5.01 NAN: (counting the crate twice) "One more pot. That's what's left."
FK-D5.02 CREW LEAD (role): "We're out at first light shifting the lanes. Can't shovel mud on nothing."
FK-D5.03 LANE-END MOTHER (role): (says nothing; the two children are watching the pot)
FK-D5.04 NAN: (to the player) "You caught it. You cooked it. Who has it?"
  > "The crew. They're clearing the lanes at first light."   → FK-D5.10
  > "The family. The children first."                        → FK-D5.20
  > [player holds cooked food] "Both. Put this in as well."  → FK-D5.30
FK-D5.10 NAN: "Crew, then." (fills their bowls; then breaks bread for the children without a word)
      {set FK_POT_CREW; event: S05_choose complete}  → end
FK-D5.20 NAN: (smiles properly) "Children, then. Crew can work up an appetite."
FK-D5.21 CREW LEAD: "We'll be a day slower." (beat) "Fair enough."
      {set FK_POT_FAMILY; event: S05_choose complete}  → end
FK-D5.30 NAN: (takes it; adds it to the pot without asking what it is) "Both, then. You'll go hungry yourself, mind."
      {item-given: cooked food → NAN; set FK_POT_OWN; event: S05_choose complete}  → end
```

**Your own bowl** (`FK-D6`, step `S06_eat`)

```
FK-D6.01 NAN: (puts a bowl in the player's hands) "Eat that. Not later. Now."
FK-D6.02 NAN: "You'll go walking into worse than geese one day. Eat first. Always eat first."
  > "Thank you, Nan."                    → FK-D6.03
  > "What's that you're humming?"        → FK-D6.04
FK-D6.03 NAN: "Don't thank me. Thank Duchess. She supervised."                        → FK-D6.06
FK-D6.04 NAN: "Same as at the crossing. The listeners' tune. Shelters always want it."
FK-D6.05 NAN: "Nobody knows the words. I think there were words."   {set FK_NAN_TUNE}  → FK-D6.06
FK-D6.06 [FK_POT_CREW] NAN: "Crew'll have the lanes clear by noon. Then I'll try for my own bed again."
FK-D6.06 [FK_POT_FAMILY] NAN: "Another night here, then. I've slept worse. Mostly on that trunk."
FK-D6.06 [FK_POT_OWN] NAN: "You fed everyone and you've nothing in your pack. Eat that, then, at least."
FK-D6.07 NAN: "River keep you."
      {small payment per FK.8; event: FK-D6 end → quest Completed}
```

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| CREW LEAD | "Lanes are clear. Your goose did that. Partly." | `FK_POT_CREW` |
| LANE-END CHILD | "You're the goose one." | `FK_POT_FAMILY` |
| NAN (if still in Brookhollow) | "Duchess has laid. In the pot crate. I've decided it's a compliment." | — |

### FK.12 Review log

| Finding | Revision |
|---|---|
| Hunting fowl for food risked turning the margin into a grind. | Two birds, an open section and a closed one; the closure teaches stewardship (Hunting C2) and cannot be bypassed. |
| The hush risked revealing the flush early. | Nothing names it. It reads as water doing something water doesn't do; MQ3–4 own the answer. |
| Nan's MQ12 "own bed" payoff could be spent here. | She reached her door and turned back; the bed is still waiting for MQ12. |
| "Who eats" could feel like a trolley problem. | Both groups are ordinary and both costs are small and visible; a third option costs the player's own food. |

---

## BP — Bark for the Pits

### BP.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `lowmark.side.bark_for_the_pits` |
| Type | Skill introduction (Leatherworking, with Woodcutting). New; built on the woodland bark co-output (Woodland portfolio S-WD2, C-WD1) and tannery intake (Economy Content Integration P-O4). |
| Unlock | MQ2 *Short Measure* Completed. Offered at the tan-yard gate. |
| Skills | Leatherworking (required), Woodcutting (required), Hunting (optional: own hide) |
| Combat share | ~5% (one shallows swarm) |
| Choice | What the yard does with bark stripped from living household trees |
| Unlocks | Tan-yard workspace; bark and hide sales at the yard; first light protection (Milestone 1); Kell Ashby as future commission giver |

**In one paragraph.** Kell Ashby's tan-yard sits at Brookhollow's downstream edge, where it belongs, and its pits are starving: the flood carried off the bark stack and dumped it in a backwater where a household draws water, and the water there has gone the colour of strong tea. The player clears the fouled bark out of the drawing-water and carries it to the yard's spent pit, set well back from the river. In the dark water, something has kept: a leather strap stamped with the yard's own mark, older than anyone at the yard. Then the honest bark: the player cuts this year's ribboned stools in the renewal coppice, and the bark comes with the wood. On the way they pass a lane where someone has stripped the bark off living trees in rings. At the yard the player breaks the bark, charges a pit, tans a hide with their own hands, and makes their first light protection at Kell's bench. Then the lane household turns up with an armful of stripped bark to sell.

### BP.2 The place [NEW; MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling |
|---|---|---|
| A. Yard gate | Hook | The smell arrives first. A sign: KELL ASHBY, TANNER. NO HIDES AFTER DARK. A washing channel led off the river and back into it through a settling pond. |
| B. The pits | The problem | A row of pits in sequence, "the rounds". The weakest liquor is pale as dishwater. The bark-stack platform is bare boards and flood wrack. |
| C. Bark brake | Ordinary labour | A heavy breaking block and mallet, a leach pit beside it. Yard hands (role) work the rounds whether the player is there or not. |
| D. Workroom | Making | A bench, a tallow pot (renderers' mark on the crock), hanks of flax thread, paper patterns pinned up, and a board of pegs with repaired straps waiting for collection. |
| E. The backwater | Clean-up | Below the old stack site: matted bark in the reeds, tea-dark water, a household's drawing-steps with a chalked sign: BOIL IT. River Skitters. |
| F. Renewal coppice (P17) | Woodcutting | Cut-and-regrow stools; the crew tally stick (TL) with ribbons on this year's stools. A coppice crew hand (role) working the far end. |
| G. The lane | Contrast | Household trees along a lane, each with a fresh ring where the bark was stripped off the living trunk. One already dropping its leaves. |

### BP.3 Beats

**Beat 0 — Starving Pits (`S00_yard`).** *Objective: Find out why the tan-yard is idle.* `BP-D1` with Kell. Kell's first priority is not bark but the drawing-water.

**Beat 1 — Tea-Dark Water (`S01_backwater`).** *Objective: Clear the spoiled bark out of the drawing-water.* Wading in starts E1. Three armfuls of spoiled bark (carry-state) to the yard's spent pit, which is set back from the river behind a bank (the player walks past the drinking steps, then away from water, which is the lesson). Spoiled bark is not an output. On the third armful the strap is exposed (BP.4).

**Beat 2 — Honest Bark (`S02_coppice`).** *Objective: Cut this year's stems in the coppice.* Standard Woodcutting gather on ribboned stools only (unribboned stools are not interactable). Each valid stem gives ordinary wood and tannin-rich bark together (guaranteed co-output, S-WD2). The quest needs a minimum bark amount (Gameplay Designer). On the route, the lane (G) is passable and its ringed trees are inspectable (`S02b_lane`, optional).

**Beat 3 — Break and Charge (`S03_brake`).** *Objective: Break the bark and charge a pit.* Give the bark to the yard's store (item-given; any tannin-rich bark counts; Kell pays the yard rate). Two **Break bark** channels at the block, then **Charge the pit** (3 s). The yard hands take it from there: leaching is ordinary labour (D05). The pale pit darkens a shade.

**Beat 4 — The Hide (`S04_hide`).** *Objective: Tan a hide at the yard.* The player needs one raw hide: their own (WC sow, MQ1 boar, any eligible hunt) or one from the yard's husbandry stock, sold at cost (if the player cannot pay, Kell advances it against the bark payment). The player performs the Leatherworking tanning interaction at the yard workspace: raw hide → vegetable-tanned hide leather. The pits do the slow part; the player's step is the player-facing transformation (D05). Exact interaction and timing belong to the Leatherworking pass.

**Beat 5 — First Piece (`S05_make`).** *Objective: Make your first light protection.* At Kell's bench, a Leatherworking make interaction produces a Milestone 1 basic light protection piece (item pass defines form and inputs). The yard supplies flax thread and rendered tallow for this one piece. Kell shows the player how to condition it with tallow (upkeep is visible from the start).

**Beat 6 — Ringed Trees (`S06_choose`).** *Objective: Decide what the yard does with the stripped bark.* The lane household (role: STRIPPER, with a child) arrives at the gate with an armful of ring-stripped bark. They lost their dock work to the flood. `BP-D6`; BP.6.

**Beat 7 — The Peg (`S07_peg`).** *Objective: Hear what Kell has to say.* `BP-D7`. Kell keeps a peg on the workroom board for people the yard will want back, and hangs the offcut of the player's first leather on it. Kell names Maelin's crews as the yard's hardest customers. Quest Completed.

### BP.4 The strap (discovery)

Under the third armful, in the tea-dark shallows, lies a leather strap: supple, uncracked, its buckle rusted to lace, stamped with a mark of crossed scrapers. Inspect text: *"A strap, still supple. Tannin water keeps things. The stamp is two crossed scrapers."* Kell recognises the stamp: it is the yard's own mark, from before the board at the gate was painted. Nobody knows who made it or when. Kell hangs it on a nail by the gate (persistent prop). It proves only that the yard has been here a long time.

### BP.5 Encounter

| Id | Enemies | Placement | Role | Telegraph | Solo target |
|---|---|---|---|---|---|
| **E1** | 4 × River Skitter | Backwater shallows | Swarm, leashed to water | Ripple line (~0.8 s), then a nip | Required on first wade; 20–30 s. Stepping onto the drawing-steps breaks contact |

### BP.6 Choices and consequences

Kell's framing: "Bark's no use to those trees now. The question is the next tree."

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Buy it, once** — *"Buy it. Tell them never again."* | Kell pays the household at half rate and tells them so in front of the yard hands. The pits fill faster this week. | Word gets round that the yard took stripped bark: after MQ3 is Completed, one more ringed tree appears on another lane (prop). | Kell, later: "Someone else tried it. I sent them off. Once was once." |
| **Turn it away** — *"No. The yard doesn't buy it."* | Kell refuses. The household leaves. | They sell it to a passing trader on the docks instead (bark line); the trees are dead either way and the family is no better off for trying the honest door. | The stripped bark rots by the lane gate (prop). |
| **Take it, pay from my share** — *"Take it. Pay them out of what you owe me, and send them to the coppice crew."* | Kell puts the stripped bark in the pits, pays the household from the player's bark payment, and sends them to the crew with a word. | The player's payment for this quest's bark. | The household appears working in the coppice crew (prop and bark). |

### BP.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_yard` | Find out why the tan-yard is idle. | Dialogue `BP-D1` end node | Yes | |
| `S01_backwater` | Clear the spoiled bark out of the drawing-water. | 3 deposit events at the spent pit | Yes | Strap inspect enabled on third lift |
| `S01b_strap` | (Optional) Look at what the water kept. | Inspect event on the strap | No | Sets `BP_STRAP_FOUND` |
| `S02_coppice` | Cut this year's stems in the coppice. | Required amount of tannin-rich bark held | Yes | Any valid bark source counts |
| `S02b_lane` | (Optional) Look at the lane trees. | Inspect event on a ringed tree | No | Sets `BP_SAW_RINGS` |
| `S03_brake` | Break the bark and charge a pit. | item-given (bark) + 2 `break_bark` + `charge_pit` complete | Yes | Kell pays yard rate on item-given |
| `S04_hide` | Tan a hide at the yard. | Leatherworking tanning interaction complete (vegetable-tanned hide leather created) | Yes | Hide from inventory or yard stock |
| `S05_make` | Make your first light protection. | Leatherworking make interaction complete at the yard bench | Yes | Thread and tallow supplied |
| `S06_choose` | Decide what the yard does with the stripped bark. | Dialogue `BP-D6` choice node | Yes | |
| `S07_peg` | Hear what Kell has to say. | Dialogue `BP-D7` end node | Yes | Quest Completed |

| Flag | Set by | Read by |
|---|---|---|
| `BP_STRAP_FOUND` | `S01b_strap` | Gate prop; `BP-D7` line |
| `BP_SAW_RINGS` | `S02b_lane` | `BP-D6` player option |
| `BP_HIDE_OWN` / `BP_HIDE_YARD` | `S04_hide` | `BP-D4` lines |
| `BP_STRIPPED_BOUGHT` / `BP_STRIPPED_REFUSED` / `BP_STRIPPED_HIRED` | `BP-D6` (exactly one) | Lane and coppice props; Kell barks; Riverpath Leathers commission opening (future) |
| `BP_KELL_PEG` | `S07_peg` | Riverpath Leathers commission package (Milestone 4, gated by `LM_CIVIC_STANDING`); MQ12 Brookhollow line (optional) |

### BP.8 Rewards

| Reward | Type | Notes |
|---|---|---|
| Tan-yard workspace | Access | The player may use the yard's Leatherworking workspace (D06 workshop context). Kell buys accepted raw hide and tannin-rich bark and sells bounded finished leather (P-O4; no unlimited conversion service). |
| **Reading bark** | Knowledge | Trees and stems across Lowmark show one line: *"A cut stem. Bark's good for the pits."* / *"Standing tree. Leave its bark on it."* (economy bark eligibility; S-WD1 ineligible by default). |
| Yard knife | Tool | Lent at `BP-D4` if the player lacks a Leatherworking tool; kept. Item pass defines it. |
| First light protection | Made by the player | Milestone 1. Not a reward drop: the player made it. |
| Bark payment | Currency | Yard rate for delivered bark (transferred to the household on *Take it, pay from my share*). |
| Woodcutting, Leatherworking XP | Action XP only | No lump quest XP. |

### BP.9 Failure, recovery, co-op

| Situation | Handling |
|---|---|
| No raw hide | Yard stock at cost, or advanced against the bark payment. Never blocked. |
| Bark sold before delivery | Any tannin-rich bark from any valid source counts; ribboned stools are always available. |
| Leatherworking can fail (if the pass allows it) | The yard sells a replacement hide at cost; thread and tallow for the first piece are resupplied once. |
| Death in the backwater | Respawn at the yard gate; carried armful returns to the reeds. |
| Logout | Last step restored; carries discarded; outputs persist. |
| Co-op | Per-instance backwater armfuls and pit charge (per-player props). The lane household's visit is per player. |

### BP.10 Integration needs

Tan-yard workspace binding (Leatherworking station with tanning and make interactions); item-given with type match ("any tannin-rich bark"); a vendor relationship that buys accepted hide and bark and sells bounded leather (P-O4); per-player pit-colour state; ribbon-gated coppice stools (TL already needs this); lane and coppice props keyed to `BP_STRIPPED_*`.

### BP.11 Dialogue

Kell is blunt, smells of the yard and knows it.

```
BP-D1.01 KELL: "Stand upwind. Everyone does eventually."
BP-D1.02 KELL: "Kell Ashby. That's my yard, and those are my pits, and they're starving."
BP-D1.03 KELL: "Flood took the bark stack. Dumped the lot in the backwater where the lane households draw their water."
BP-D1.04 KELL: "Water's gone black. That's my bark in their kettles. That's first."
  > "I'll clear it."                                      → BP-D1.10
  > "Where does the spoiled bark go?"                     → BP-D1.05
  > "Why's the yard all the way out here?"                → BP-D1.07
BP-D1.05 KELL: "Spent pit. Behind the bank, away from the river. Not in it. Never in it."   → BP-D1 options
BP-D1.07 KELL: "Because nobody wants to drink downstream of me. Including me."              → BP-D1 options
BP-D1.10 KELL: "Good. Then bark. Real bark. I'll tell you what real means when you're back."
      {event: BP-D1 end → completes S00_yard}
```

**The strap** (`BP-D1b`, on returning with `BP_STRAP_FOUND`)

```
BP-D1b.01 KELL: (turns it over) "Crossed scrapers."
BP-D1b.02 KELL: "That's the yard's mark. Before the sign. Before my teacher's teacher, maybe."
BP-D1b.03 KELL: "Tannin keeps things. Hides, mostly. Apparently straps." (hangs it on the gate nail)   → end
```

**Real bark** (`BP-D2`, after `S01_backwater`)

```
BP-D2.01 KELL: "Coppice. This year's stools, the ribboned ones. Cut the stem, the bark comes with it."
BP-D2.02 KELL: "Bark off a cut stem. Not off anything still standing. You strip a living tree, it dies standing up."
  > "Why does it matter, if the bark's the same?"         → BP-D2.03
  > "On my way."                                          → end
BP-D2.03 KELL: "Bark's the same. Tree isn't. A stool grows back. A lane tree doesn't."   → end
```

**Lane inspect texts**

| Object | Text |
|---|---|
| Ringed tree | "Bark stripped off in a ring, right round the trunk. Fresh. The tree doesn't know it's dead yet." |
| Dropping tree | "Leaves coming down out of season. It knows." |
| Ribboned stool | "A ribboned stool. This year's cut." |
| Unribboned stool | "Growing. Not this year." |

**Break and charge, the hide** (`BP-D4`, at the workspace)

```
BP-D4.01 KELL: "Pits do the slow part. You do the part that goes wrong."
  > [BP_HIDE_OWN] "I brought my own hide."                 → BP-D4.02
  > [no raw hide] "I've no hide."                         → BP-D4.04
  > [player has no Leatherworking tool] "I've nothing to work it with."   → BP-D4.06
BP-D4.02 KELL: (feels it) "Clean. Somebody field-dressed this properly."    → BP-D4.03 if WC_SOW_TAKEN, else → BP-D4.08
BP-D4.03 [WC_SOW_TAKEN] KELL: "Ashenstead boar? Thought so. They come in muddy."  → BP-D4.08
BP-D4.04 KELL: "Yard stock. At cost. If you can't pay, I'll take it off your bark."   {BP_HIDE_YARD; hide from yard stock}  → BP-D4.08
BP-D4.06 KELL: "Yard knife. Don't use it on bread." {give yard knife}   → BP-D4 options
BP-D4.08 KELL: "Into the liquor, the way I showed you. Don't rush it. Rushing is how you get boots that squeak."
      {S04_hide interaction enabled}  → end
```

**First piece barks** (`S05_make`)

| Trigger | Speaker | Line |
|---|---|---|
| Make starts | KELL | "Cut it the way the hide wants to go, not the way you want it to." |
| Make complete | KELL | "That'll keep a reed-stalker's teeth out. Once. Twice if you're lucky." |
| Tallow prompt | KELL | "Tallow. Thin. Leather's like people: needs feeding or it cracks." |

**Ringed trees** (`BP-D6`)

```
BP-D6.01 STRIPPER: (at the gate, with an armful and a child) "Bark. Good bark. You're short, everyone says."
BP-D6.02 KELL: (looks at it) "That's lane bark. Off standing trees."
BP-D6.03 STRIPPER: "Flood took the dock work. We've got to eat something."
BP-D6.04 KELL: (quietly, to the player) "Bark's no use to those trees now. The question is the next tree."
BP-D6.05 KELL: "You cut the honest stuff. You say."
  > [BP_SAW_RINGS] "I saw the lane. One's already dropping its leaves."   → BP-D6.06
  > "Buy it. Tell them never again."                                     → BP-D6.10
  > "No. The yard doesn't buy it."                                       → BP-D6.20
  > "Take it. Pay them out of what you owe me, and send them to the coppice crew."   → BP-D6.30
BP-D6.06 STRIPPER: (looks at the child, not at the player) "I know."                     → BP-D6 options
BP-D6.10 KELL: "Half rate. Once. Next time I see a ring on a lane, I'll know where to look."
BP-D6.11 STRIPPER: "Once. Yes."
      {set BP_STRIPPED_BOUGHT; event: S06_choose complete}  → end
BP-D6.20 KELL: "No. Not here." 
BP-D6.21 STRIPPER: "There's a trader on the docks'll take it." (goes)
BP-D6.22 KELL: "There is. That's the trouble with no."
      {set BP_STRIPPED_REFUSED; event: S06_choose complete}  → end
BP-D6.30 KELL: (long look at the player) "Your bark money, their pocket."
BP-D6.31 KELL: (to the household) "Coppice crew needs hands. Tell them Ashby sent you. Cut stems. Not trees."
      {transfer quest bark payment → household; set BP_STRIPPED_HIRED; event: S06_choose complete}  → end
```

**The peg** (`BP-D7`)

```
BP-D7.01 KELL: (holds up the offcut of the player's first leather; hangs it on an empty peg)
BP-D7.02 KELL: "That board's for people the yard'll want back. Most pegs have a strap waiting. Yours has a mistake on it. That's how they all start."
  > "Who's the yard's hardest customer?"                  → BP-D7.03
  > [BP_STRAP_FOUND] "And the old strap by the gate?"     → BP-D7.05
  > "I'll be back."                                       → BP-D7.06
BP-D7.03 KELL: "Maelin Rowe's crews. River eats leather. They wear mine and they complain about it, which means they wear it."
BP-D7.04 KELL: "One day they'll want better than I can make alone. Keep working, and it might be you and me and them."   → BP-D7 options
BP-D7.05 KELL: "Stays on the nail. Somebody made it to last. I'd like to know who. I won't."    → BP-D7 options
BP-D7.06 KELL: "Yard's open to you. Bring hides clean and bark honest."
      {set BP_KELL_PEG; event: BP-D7 end → quest Completed}
```

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| KELL | "Pits are drinking again. Listen. No, don't. It's horrible." | — |
| KELL | "Someone tried a lane tree. Sent them off. Once was once." | `BP_STRIPPED_BOUGHT`, after MQ3 |
| COPPICE CREW HAND | "New pair of hands from the lanes. Cuts stems like they're apologising to them." | `BP_STRIPPED_HIRED` |
| YARD HAND | "Ashby kept your offcut. Ashby keeps nothing. Don't let it go to your head." | `BP_KELL_PEG` |

### BP.12 Review log

| Finding | Revision |
|---|---|
| A bark-gathering quest risked a bark-only action. | Bark comes only from cutting ribboned stems (S-WD2 co-output); the backwater bark is spoiled waste, not an output. |
| The yard looked like a vending machine for leather. | Yard hands work the rounds without the player; Kell buys and sells within bounds; the player's own Leatherworking does the transformation (D05, P-O4). |
| Dirty work beside drinking water for convenience. | The yard is downstream at the settlement edge; the first job is to undo exactly that harm (D09, P-O4 "must not become"). |
| Commission giver risked designing the commission. | Kell names Maelin's crews and a "maybe one day"; no form, inputs or steps. |

---

## HS — Honest Steel

### HS.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `lowmark.side.honest_steel` |
| Type | Skill introduction (Smithing). New; built on the imported-steel rule (Minimum Coherent Material Set §2.1; Economy Content Integration P-O7 receiving inspection). |
| Unlock | MQ2 *Short Measure* Completed. Offered at the Crestbridge forge. |
| Skills | Smithing (required) |
| Combat share | None. Danger is the forge itself (one readable hazard). |
| Cameo | Corvin Tath [CANON ANCHOR], numbers only |
| Choice | What happens to the salvage: Keepers' custody, or refused back to the carrier, marked |
| Unlocks | Forge workspace; lawful steel stock from the receiving bench; first dependable blade (Milestone 1); heavy-protection work opened; Brigid Corliss as future commission giver |

**In one paragraph.** Brigid Corliss's forge is built into the Crestbridge abutment, under the span, where the dwarven iron ties run through the stone. A consignment of "sound stock" has come in, plain carbon steel bars under an importer's tag, and one of them rang wrong under Brigid's hammer. Brigid teaches the player to ring-test: sound bars ring clear, and the old ties in the bridge hum back. Two bars ring dull and get no answer. Their ends are cut, not sheared; their sides carry plugged bolt-holes at even spacing; on one, a stencil has been ground nearly away, leaving a broad arrow and two letters. The player forges their first dependable blade from a sound bar, then heats and quenches a suspect one at Brigid's insistence, and steps clear when it cracks. Corvin Tath arrives with the crossing scale's tally and the carrier, who is frightened. The numbers say three bars were swapped after the bill was written. Nobody can say where the salvage came from. The player decides where it goes.

### HS.2 The place [NEW; MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling |
|---|---|---|
| A. Forge mouth | Hub | Under the first arch of the span. Hearth, anvil, bellows, a quench trough fed by a channel from the river. Charcoal sacks with the fuel workers' mark. Iron tie-ends, dark and old, set into the abutment stone at head height. |
| B. Receiving bench | Inspection | The consignment bundle, its importer's tag retied with newer cord. The carrier's bill nailed beside it. A testing horn bolted to the bench. |
| C. Rejects rack | Contrast | Sorted civilian scrap: cart tyres, hinges, a broken plough-share, each chalked KEEP or NO. Sound civilian scrap gets assessed; some gets used for small repairs. |
| D. Refurbish queue | Upkeep | Keepers' blades and harness plates on hooks, tagged with names and "regrind", "re-rivet", "strap". Brigid's real work. |
| E. Bridge walk | Optional | A short service ledge under the span to where the ties run through the piers (agility step, or the fallback ladder). |

### HS.3 Beats

**Beat 0 — Wrong Note (`S00_ring`).** *Objective: Find out what's wrong at the forge.* Entering the forge volume: Brigid is hammering, stops mid-stroke, strikes again, swears. `HS-D1`.

**Beat 1 — Ring Them (`S01_inspect`).** *Objective: Test the consignment.* Brigid has pulled six bars from the bundle. The player strikes each on the testing horn (six short interactions). Four ring clear and a low hum answers from the ties in the stone (HS.4). Two ring dull and nothing answers. Then three inspects on the dull bars: ends, bolt-holes, stencil. Required: all six rings and all three inspects.

**Beat 2 — Your Own Blade (`S02_blade`).** *Objective: Forge a blade from sound stock.* Brigid hands over one sound bar ("Your wage is in that"). Smithing interactions at the forge using the forge's charcoal: heat, draw out, shape, quench, finish at the wheel (each a channel; exact sequence and outcome belong to the Smithing interaction pass). The result is the player's Milestone 1 basic melee weapon (item pass defines it).

**Beat 3 — Why Not (`S03_crack`).** *Objective: Heat and quench a suspect bar.* Same heat and quench interactions on a dull bar. In the trough it **ticks twice** (~1.5 s) and a shard spits along the trough's line; the player steps aside. The bar cracks every time (authored outcome, not skill-based). Inspecting the break: *"Coarse and grey inside, with rust deep in the grain. It was wet for a long time."* This is why war salvage stays out of routine supply: unknown history, hidden flaws.

**Beat 4 — The Count (`S04_count`).** *Objective: Hear what the crossing tally says.* Corvin Tath arrives with his tally and the carrier (role: CARRIER). `HS-D4`. The bill says twelve bars at one weight; the crossing scale weighed twelve bars at another. Swapped, not added. Records do the proving; the bridge's hum proved nothing.

**Beat 5 — Where It Goes (`S05_choose`).** *Objective: Decide what happens to the salvage.* `HS-D5`; HS.6.

**Beat 6 — The Queue (`S06_queue`).** *Objective: Hear what Brigid has to say.* `HS-D6` at the refurbish queue. Brigid names what keepers bring to the forge and what they will one day ask for. Quest Completed.

### HS.4 The ties (wonder, and what it is not)

When sound plain carbon steel is struck on the testing horn, the iron ties in the abutment give back a faint, low hum for about a second, as old tuned ironwork does. Salvage bars, dull in themselves, get no answer. Brigid tests by it: "Strike true and they ring with you." Presentation: a positional low tone from the tie-ends; no visual effect; no UI. It is acoustics in old dwarven work (dossier: dwarven-reinforced bridge), not a supernatural judgment, and it identifies nothing. It is also not evidence in the story: Corvin's numbers are. After the quest, any steel stock struck on the horn plays the same response (a usable inspection cue).

### HS.5 The hazard

| Id | Hazard | Placement | Telegraph | Effect | Solo target |
|---|---|---|---|---|---|
| **H1** | Cracking bar | Quench trough | Two sharp ticks and a hiss (~1.5 s); the trough's line is the danger lane | A shard along the lane: small damage, brief knockback. Cannot kill a player above a quarter health | Teaches stepping out of a telegraphed lane without combat |

### HS.6 Choices and consequences

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Keepers' custody** — *"Give it to the Keepers. Let them find out where it came from."* | A Keeper (role) tags the three bars and takes them to Crest Hall's store. The carrier's cart is held pending inquiry. | The carrier loses a season's hauling. Brigid's stock is three bars short and the refurbish queue waits; Brigid pays the player only the bar and a few coins. | The bars sit tagged in the Keepers' store (prop, if Crest Hall's store is visited). Brigid: "Honest and slow. Like me." |
| **Refuse it back, marked** — *"Stamp it refused and send it back with the carrier."* | Brigid stamps the forge's refusal mark into each salvage bar. The carrier takes them back and repays the difference. The cart stays with its owner. | The salvage goes back into circulation, marked but not stopped. Somebody will buy it. | Optional, removable hook: a refusal-stamped bar can appear in the Drowned Lamb cellar (UL). It proves nothing there either. |

Neither option tells the player who swapped the bars. That stays open (HS.10).

### HS.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_ring` | Find out what's wrong at the forge. | Dialogue `HS-D1` end node | Yes | |
| `S01_inspect` | Test the consignment. | 6 `ring_test` interactions + 3 inspect events (ends, holes, stencil) | Yes | |
| `S01b_ties` | (Optional) Walk out to the bridge ties. | Enter tie-ledge volume | No | Sets `HS_TIES_SEEN`; agility step or ladder fallback |
| `S02_blade` | Forge a blade from sound stock. | Smithing interaction chain complete (weapon created) | Yes | Brigid supplies the bar and charcoal |
| `S03_crack` | Heat and quench a suspect bar. | Interaction `quench_suspect` complete | Yes | Outcome authored: always cracks |
| `S04_count` | Hear what the crossing tally says. | Dialogue `HS-D4` end node | Yes | Corvin and carrier spawn on `S03` complete |
| `S05_choose` | Decide what happens to the salvage. | Dialogue `HS-D5` choice node | Yes | |
| `S06_queue` | Hear what Brigid has to say. | Dialogue `HS-D6` end node | Yes | Quest Completed |

| Flag | Set by | Read by |
|---|---|---|
| `HS_TIES_SEEN` | `S01b_ties` | `HS-D6` line |
| `HS_SALVAGE_KEEPERS` / `HS_SALVAGE_REFUSED` | `HS-D5` (exactly one) | Forge props; Brigid barks; Crest Hall store prop; UL optional hook |
| `HS_BRIGID_QUEUE` | `S06_queue` | Keeper's Blade and Bridgewarden Harness commission packages (Milestone 4, gated by `LM_CIVIC_STANDING`); MQ12 Crestbridge line (optional) |

### HS.8 Rewards

| Reward | Type | Notes |
|---|---|---|
| Forge workspace | Access | The player may use Brigid's forge (D06 workshop context) and buy lawful plain carbon steel stock from the receiving bench. Charcoal is bought from the forge's fuel-worker supply. |
| Heavy protection | Access | Brigid's forge offers the Milestone 1 heavy-protection work (item pass defines it). |
| **Receiving inspection** | Knowledge | Steel stock and suspicious metal anywhere can be ring-tested: *"Rings clear."* / *"Rings dull. Don't trust it."* Inspect lines on cut ends and plugged holes become available on authored salvage props. |
| First dependable blade | Made by the player | Milestone 1. |
| Forge tongs | Tool | Lent at `HS-D1` if the player lacks Smithing tools; kept. Item pass defines them. |
| Small payment | Currency | The sound bar plus coins; fewer coins on *Keepers' custody*. |
| Smithing XP | Action XP only | No lump quest XP. |

### HS.9 Failure, recovery, co-op

| Situation | Handling |
|---|---|
| Smithing can fail (if the pass allows it) | Brigid supplies up to two more sound bars for the quest's blade. |
| Player stands in the shard lane | Small damage; the step still completes. |
| Death (unlikely) | Respawn at the forge mouth; step kept. |
| Logout | Last step restored; created weapon persists. |
| Co-op | Each instance has its own consignment bundle and choice (per-player props). Corvin and the carrier present per player; fallback if per-player NPC states are unavailable: they stand at the bench for everyone and their dialogue reads each player's own step. |

### HS.10 Mystery ledger entry

| Mystery | Author truth (proposal) | Public belief | Evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Who swapped the bars** | Deliberately unselected. Compatible with the Brookhollow black-market trade in steel (dossier) and with wartime ironwork being pulled from old sites. **No canon anchor's history is implied.** | The carrier cheated; or the importer did. | Retied tag; cut ends; plugged bolt-holes; a broad arrow and two letters; Corvin's weight difference. | The carrier did it (he is frightened, which looks like guilt); the stencil "proves" which wartime site it came from (it proves only that it was once marked). | Origin; who swapped it; what it was bolted to. | None in v1. UL may echo it. |

### HS.11 Integration needs

Ring-test interaction (short, plays a pass/fail audio cue and the tie response positionally); Smithing chain at a forge station; an authored-outcome interaction (`quench_suspect`) independent of skill rolls; hazard lane with telegraph (H1); NPC spawns on step (Corvin, CARRIER, KEEPER); per-player bundle and bar props; vendor for lawful steel stock and charcoal at the forge (P-O7, P-O5).

### HS.12 Dialogue

Brigid is loud in the forge and quiet outside it. Corvin speaks in numbers, weights and losses, never opinions.

```
HS-D1.01 BRIGID: (strikes; stops; strikes again) "HEAR THAT?"
HS-D1.02 BRIGID: "No, you didn't. Nobody does. COME HERE."
HS-D1.03 BRIGID: (lower, the moment the hammer is down) "Brigid Corliss. Bridge-smith. That bar rang wrong."
HS-D1.04 BRIGID: "Sold to me as sound stock. Importer's tag and all. I don't buy anything I haven't heard."
  > "How does steel ring wrong?"                         → HS-D1.05
  > "Show me."                                           → HS-D1.07
  > [player has no Smithing tools] "I've never worked a forge."   → HS-D1.06
HS-D1.05 BRIGID: "Sound bar sings. Bad bar thuds. You'll hear it once you've heard both."  → HS-D1 options
HS-D1.06 BRIGID: "Good. Nothing to unlearn. Tongs." {give forge tongs}                    → HS-D1 options
HS-D1.07 BRIGID: "Six on the bench. Strike each one on the horn. And listen past it."
      {event: HS-D1 end → completes S00_ring}
```

**Ring and inspect texts**

| Object | Text | Condition |
|---|---|---|
| Sound bar (ring) | "A clear note. Something in the stone answers it, low." | 4 of 6 |
| Dull bar (ring) | "A flat thud. Nothing answers." | 2 of 6 |
| Dull bar, ends | "Cut, not sheared. The importer's bars are sheared clean. These were cut from something longer." | — |
| Dull bar, holes | "Holes drilled at even spacing and plugged with soft iron. It was bolted to something big." | — |
| Dull bar, stencil | "Most of a stencil has been ground off. A broad arrow survives, and two letters: E, F." | — |
| Importer's tag | "Tied on with newer cord than the bundle's." | — |
| Tie-ends (stone) | "Old iron, set right through the stone. Warm to the hand when the hammer's going." | — |

**Ring barks** (Brigid)

| Trigger | Line |
|---|---|
| First clear ring | "THERE. Hear the bridge? It likes that one." |
| First dull ring | "And that's the wrong one. Flat as a pancake." |
| After all six | (quiet) "Look at the ends of the bad ones. Then the sides." |
| Stencil inspected | (quiet) "Supply stencil. Old ones had that arrow on everything." |

**The crack** (`HS-D3`, after `S03_crack`)

```
HS-D3.01 BRIGID: (looks at the break, not at the player) "That's why."
HS-D3.02 BRIGID: "You don't know where it's been or what it's held. It doesn't tell you till it breaks."
HS-D3.03 BRIGID: "Out on the bridge, it breaks in a keeper's hand."   → end
```

**The count** (`HS-D4`, Corvin and the carrier arrive)

```
HS-D4.01 CORVIN: "Twelve bars crossed my scale yesterday with your consignment. I keep the scale tallies."
HS-D4.02 CORVIN: "The bill says twelve bars at one weight. My tally says twelve bars at another. Three bars' difference."
HS-D4.03 CARRIER: "I didn't touch them. Bought the bundle tied, tag on, off a yard downriver."
  > "Swapped or added, Corvin?"                         → HS-D4.04
  > "Where did they come from?"                         → HS-D4.05
  > "The tag was retied with new cord."                 → HS-D4.07
HS-D4.04 CORVIN: "Swapped. The count is right. The weight is not."                    → HS-D4 options
HS-D4.05 CORVIN: "I don't know where they came from. I know what they weigh."
HS-D4.06 BRIGID: (quiet) "Somewhere that put an arrow on its iron."                    → HS-D4 options
HS-D4.07 CARRIER: (looks at it) "...That's not my knot." (beat) "That's not my knot."
HS-D4.08 CORVIN: "Then it was retied between the yard and my scale. That narrows the distance. Not the person."
      {event: HS-D4 end → completes S04_count}
```

**Where it goes** (`HS-D5`)

```
HS-D5.01 BRIGID: "I'm not putting that on a keeper. And I'm not keeping it under my bench."
HS-D5.02 CARRIER: "If the Keepers take it, they take my cart with it. That's my season."
HS-D5.03 BRIGID: (to the player) "You rang them. You choose."
  > "Give it to the Keepers. Let them find out where it came from."   → HS-D5.10
  > "Stamp it refused and send it back with the carrier."                   → HS-D5.20
HS-D5.10 KEEPER (role): (tags the bars) "Crest Hall store. And the cart, till it's looked into."
HS-D5.11 CARRIER: (sits down on the cart step) "...Right."
HS-D5.12 BRIGID: "Honest and slow. Like me." (beat) "I'm three bars short now. You'll get the bar and not much else."
      {set HS_SALVAGE_KEEPERS; event: S05_choose complete}  → end
HS-D5.20 BRIGID: (stamps the forge's refusal mark into each bar; three heavy strokes) "Anyone who buys these knows what I thought of them."
HS-D5.21 CARRIER: "I'll pay back the difference. I'll find the yard." (beat) "Thank you."
HS-D5.22 CORVIN: "Three bars, back into circulation. I'll note the weight."
      {set HS_SALVAGE_REFUSED; event: S05_choose complete}  → end
```

**The queue** (`HS-D6`, at the refurbish hooks)

```
HS-D6.01 BRIGID: (quiet now; hangs a keeper's blade back on its hook) "This is the real work. Regrind. Re-rivet. Strap."
HS-D6.02 BRIGID: "Every keeper's blade on this bridge has been on my anvil, and every harness plate they wear has been under my hammer twice. One day you'll come and ask me for one of your own, and I'll ask what you've done to deserve it, and you'll have an answer. Not yet."
  > "What would the answer be?"                          → HS-D6.03
  > [HS_TIES_SEEN] "The bridge hums at sound steel."     → HS-D6.05
  > "I'll be back."                                      → HS-D6.06
HS-D6.03 BRIGID: "Ask the keepers. Ask the bridge. Mostly ask yourself."                    → HS-D6 options
HS-D6.05 BRIGID: "It's old iron in old stone. My teacher said it was showing off." (beat) "I like it."   → HS-D6 options
HS-D6.06 BRIGID: "Forge is yours when it's free. Buy honest stock off my bench. Ring everything."
      {set HS_BRIGID_QUEUE; small payment per HS.8; event: HS-D6 end → quest Completed}
```

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| BRIGID (forge) | "RING IT FIRST." | — |
| BRIGID (outside the forge) | "Hm." (nods) | — |
| CARRIER (Crestbridge) | "Got the cart back. Lost the season. Still hauling for the forge." | `HS_SALVAGE_KEEPERS`, after MQ3 |
| CORVIN | "Three bars short at the forge. Three bars long somewhere else." | `HS_SALVAGE_REFUSED` |

### HS.13 Review log

| Finding | Revision |
|---|---|
| The bridge hum could read as the steel "knowing" its past (memory-bearing material, rejected by the Woodland and Material Set designs). | Framed as acoustics in old ironwork that answers sound steel; dull bars are simply flawed. No grief, no memory, no identification. |
| The stencil risked proving a wartime origin or an anchor's history. | A broad arrow and two letters only. Corvin says he doesn't know; his line is about weight. No anchor is tied to the bars. |
| Using the salvage for "non-load-bearing" work was considered. | Removed: war remains are excluded from routine supply. Both options keep it out of Brigid's work. |
| The forge lacked readable danger without combat. | The cracking bar is a telegraphed lane hazard that cannot kill. |
| Corvin's cameo could become a talk-to-X errand. | He walks to the forge himself, speaks four lines of numbers, and leaves. |

---

## Cross-quest integration summary

| Need | Quests | Owner | Note |
|---|---|---|---|
| Step-level objectives and flags | All | Schema & Content Engineer, Systems Engineer (31.3, 24.1) | Same shape as TL. |
| Dialogue with item-held and flag conditions; item-given effects | All | 31.5 | "Holds cooked food", "has no cutting tool" conditions recur. |
| Carry-state props | WC, FK, BP | Systems Engineer | Same fallback as TL (lift-and-stack interactions). |
| Hunting approach/resolve/recover hooks | WC, FK | Hunting interaction pass | One shared alert framework for F2/F3 presentation (Hunting portfolio rule). |
| Craft stations | FK (Cooking), BP (Leatherworking), HS (Smithing) | 33.5 station binding | Each persists after its quest as a public or opened workspace. |
| Authored opportunity states | WC margin, FK closed margin, BP ribbon-gated stools | Economy D04 vocabulary | Open / closed / closed-until. |
| Per-player persistent props | BW bank, BP lane/coppice, HS bundle, FK shelter | 33.1.B2 | Fallbacks listed in each package. |
| Vendors with bounded intake | BP (hide, bark, leather), HS (steel stock, charcoal) | Economy pass | P-O4, P-O5, P-O7; no unlimited conversion. |

## Open questions for the Director and other passes

1. **Guard-capable setup (Milestone 1)** is not taught by any of these five. Recommendation: let the item/encounter pass attach it to HS's opened heavy-protection work or to MQ2–4 encounters; do not add a sixth skill quest.
2. **FK's hush is a flush.** It foreshadows MQ4 at Brookhollow. If the Act I package changes the flush schedule, FK's hush should still fall on a flush night (it is unlock-gated after MQ1, before MQ4 in most playthroughs). If a player completes MQ4 first, play the hush anyway; Nan's line still works, and Ansel's optional MQ3 line is skipped.
3. **WC location tier.** Bible §4.1 places Ashenstead Fields at mid tier; WC uses its near margin right after MQ1. Confirm the margin sits at the Heartlands edge (MAP VERIFICATION REQUIRED).
4. **Hide flow for BP.** BP never requires Hunting; the yard always sells a raw hide at cost. Confirm with the economy pass that this matches husbandry as baseline hide supply.
