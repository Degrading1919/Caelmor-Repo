# Emberholt Side Quests: Work and Skills

**Status (2026-11-15):** Authored production content for Creative Director milestone review (Emberholt bible §12, Batch 3). Six side quests from `Caelmor_Emberholt_Narrative_Production_Bible.md` §7.1 and §7.2: the **Guild Ledgers** pair, **ESK** *Sound Stock* (1/2, Smithing intro) and **EOM** *The Old Methods* (2/2, combat challenge); and four standalone skill intros, **EFS** *The Flarecap Seam* (Mining), **EWQ** *Wardens' Quarrels* (Fletching and Ranged), **ESP** *Shift Supper* (Cooking) and **ESH** *Soot and Hide* (Leatherworking). Everything here is **[NEW]** unless marked **[CANON]** or **[APPROVED — id]**. Choices that rest on an open bible §3 recommendation are marked **[PROPOSAL — DIRECTOR]**. Markdown only: no schema, production JSON or C#. Dialogue sits inline in each package (§x.12), as in `Caelmor_Mire_Side_Quests_Work_and_Skills.md` and the sibling `Caelmor_Emberholt_Side_Quests_Commons_and_Wards.md`, in the node format `NODE SPEAKER: "Line." (stage note)`, `> [condition] "Option." → NEXT {effect}`, with node ids `<CODE>-D<n>.<nn>`, barks `<CODE>-B<n>.<nn>` and inspect texts `<CODE>-I<n>`. Voice follows bible §5.3.

**Binding rulings:** `Caelmor_Director_Rulings_Combat_Ranged_Release.md`: CDR-1 (every enemy defeated at 0 HP; no yield, retreat, break-off, scatter or drive-off; Emberholt registers no SX exception), CDR-2 (ranged first-class in every fight, required in none), CDR-3 (Emberholt is an internal production milestone of the complete game), CDR-4 (standard RPG systems before bespoke simulation; meaningful skill requirements), CDR-6 (every step, encounter and reward completable solo; co-op is optional assistance; partner credit only when the partner's own active step consumes it; personal choices and flags independent).

**Sources used:** the Emberholt bible (binding: §1.1, §2.1, §3 ED-6, ED-10, ED-11, ED-13, §4.2, §5, §7.1–7.4, §9, §10, §11); `Caelmor_Emberholt_Main_Act_I.md`, `_Act_II.md`, `_Act_III.md` and their dialogue files (every flag and line this file reads or makes true is cited at its row in §0.7); the Emberholt dossier (`LORE/Regions/Caelmor_Region4_EmberholtHeights.md`); `LORE/Characters/Caelmor_Characters_Region4_Emberholt.txt` §21 Durnan Volkryst, §26 Haelric Stormvein; `LORE/Factions/Caelmor_Factions.md` §6, §8; the Part 4 character ledger; Lowmark *Honest Steel* (`HS_SALVAGE_*`); the Revelation Ledger.

**Scope guard.** Nothing here grows scope or adds a system. Every technical need is listed in each package's integration section for the Emberholt integration handoff (bible §12, Batch 4). **No Emberholt terrain exists:** every placement is relative and marked **MAP VERIFICATION REQUIRED** where geometry, distance or heat matters. No route or direction to another region is stated or implied.

**Not in this file.** EST, ETB, EMS, ENW, EGT (Unburnt and Names), EWA, ECN, EFC, EBL, ESR (Commons and Wards), and EOP, EFD, EAD, ECC with the micro-events and discoveries (Combat and Discovery) belong to other packages. This file sets none of their flags, uses none of their quest-givers as givers, and does not author EME or EDS content: the magma larks (EME08) and the Ash Roads' engravings (EDS01) appear here as scenery only, with no reading layer. Teodor Marsk and Old Plate (EOP) are not used; the Emberback Boars in EWQ are an ordinary pack on the Ash Roads.

---

## 0. Purpose and shared rules

Emberholt's main line teaches the player to read heat so they can see where the city's warmth goes. These six quests teach the same reading as a working hand's skill: a smith rings a bar twice because heat can hide a fault; a miner walks off the seam when the face goes amber; a fletcher straightens shafts over a bed that must be amber and never red; a cook packs pails in vent-warmed stones; a tanner softens hide on a bed that would scorch it if it ran hot. Every lesson is a real skill loop with an ordinary output, using the city's own markers (bible §1.1). The **Guild Ledgers** pair carries the region's craft politics at the scale of one hall; EOM sets `EH_GUILDS`, which EH-M6 reads.

### 0.1 Unlock gates and placement

| Code | Quest | Series / type (bible §7) | Core verb (primary first) | Unlock (quest state) | Skill hook (CDR-4) and time-cost alternative | Where (bible §4.2) | Length |
|---|---|---|---|---|---|---|---|
| **ESK** | Sound Stock | Guild Ledgers 1/2; Skill intro (Smithing) | **inspect**, forge, test | EH-M1 Completed (`emberholt.main.01_cold_ward`) | **Smithing ~[GD: entry; taught from any level]**: draw a bar to the guild gauge; alternative: keep watch until the evening bell and call the heats while the apprentice hammers | The Emberforges (EP25): the Basalt Forge Guild yard, receiving shed and apprentice hearth | 25–35 min |
| **EOM** | The Old Methods | Guild Ledgers 2/2; Combat challenge | **inspect**, track, assault | ESK Completed **and** EH-M2 Completed (`emberholt.main.02_ember_in_every_hand`) | **Smithing ~[GD: low]**: rivet a patch on the holed quench trough; alternative: keep watch until morning for the guild's crew | The Emberforges (EP25); the Ridge Steadings (EP05); the Saboteurs' Kiln (EP17) | 40–50 min |
| **EFS** | The Flarecap Seam | Standalone; Skill intro (Mining) | **mine**, read, haul | EH-M1 Completed | **Mining ~[GD: entry; taught from any level]**: work the seam face by its tells; alternative: haul two carts for Breck's hands (about a turn of walking) | The Ridge (outside the Cinderwall working gate): the Ridge Steadings (EP05), the Ridge Workings (EP14) | 30–40 min |
| **EWQ** | Wardens' Quarrels | Standalone; Skill intro (Fletching, Ranged) | **salvage**, fletch, shoot | EH-M1 Completed | **Fletching ~[GD: entry; taught]** and **Ranged ~[GD: entry; taught]**; optional **Smithing ~[GD: low]** for heads. Alternatives: reclaim spent heads from the old butts and wait while Ryl files them; spot for Ryl at the marks at dusk instead of shooting | Embergate (EP01): the Border-Wardens' bench in the merchant yards; the Ash Roads (EP09) range; a vent bath on the Ridge | 35–45 min |
| **ESP** | Shift Supper | Standalone; Skill intro (Cooking) | **cook**, carry, serve | EH-M1 Completed | **Cooking ~[GD: entry; taught from any level]**: the shift-supper stew; alternative: work Hennet's hatch for a turn while he cooks | Cinderwall (EP02): the Cooling House and yard; the Undercroft stair; the slag lanes; the Emberforges' Cinderwall gate | 25–30 min |
| **ESH** | Soot and Hide | Standalone; Skill intro (Leatherworking) | **cut**, stitch, fit | EH-M1 Completed | **Leatherworking ~[GD: entry; taught from any level]**: heat gloves and a duct hood; alternative: keep watch until morning while Brisa cuts and stitches (the player still dresses and fits) | The Cinderweave Quarter (EP03): Brisa Teglan's tannery and soot loft; the Cinderwall Undercroft stair (EP15) | 30–40 min |

All six are optional, solo-clearable, cannot fail and give no lump quest XP (skill XP comes from actions; bible §11.6). Inactive, Active or Completed only. **No quest items** (bible §9.4: the Emberholt budget is spent by the milestones); every carried thing is a carry-state prop, a lent tool, a station object, an inspect point or an ordinary output the economy pass will define (§0.3).

**Skill requirements (CDR-4).** One quest-start requirement, on the skill the quest **builds on**, never on the one it teaches (Mire precedent): **EOM requires Smithing ~[GD: low]**, the level ESK's own forging reaches from a standing start (any public forge also trains it). The offer is visible to everyone, and a player below the level is told plainly what to train (`EOM-D1.06`). The other five teach their skill from any level. Inside every quest, each skill step has a time-cost alternative that is still play (the player reads, calls, carries, dresses or spots while someone else supplies the hand), costing a turn of the presentation hour, a walk or skill XP, never the quest. All `[GD]` levels are placeholders for the Gameplay Designer and are reachable inside Emberholt.

**Level framing (ED-10).** ESK, EFS, EWQ, ESP and ESH sit at EH-M1's Advanced identity; EOM at EH-M2's. Exact levels are Gameplay Designer calls.

### 0.2 Skill coverage and how the six feed one another

```text
ESK  Smithing (taught): first ring on receiving ──► heat to the forge's amber tell ──► draw to the guild gauge
     ──► quench ──► second ring by another hand ──► two-mark tag on the guild rack            [EWS-01, EWS-02]
     └─ the guild's rule "nobody rings their own second" is the rule EOM's saboteurs broke
EOM  Inspection (no skill): a holed trough, a cut strap, forged tags ──► ridge charcoal ──► the kiln
     Smithing (requirement + hook): rivet a patch on the holed trough                         [EWS-01, EWS-14]
     Melee or Ranged: Forge Saboteurs and the Saboteur Captain at the kiln
     └─ sets EH_GUILDS (read by EH-M6 S03, S08, §E.5, §E.10)
EFS  Mining (taught): read flarecap (pale strike, orange leave) ──► follow the pale to the seam
     ──► work the face while its tells are clear; walk to the niche when they go amber ──► ridge ironstone [EWS-03]
     Melee or Ranged: Slag Beetles on an old slag spill
     └─ EFS Completed is read by EH-M3 S02 (Darven's variant line)
EWQ  Woodcutting (reclaimed crate-wood only, ED-11) ──► shaft blanks                           [EHC-05 shared]
     Fletching (taught): shave, roll-test, straighten over an amber bed, fletch with moulted lark feathers [EWS-05, EWS-06]
     Smithing (optional) or reclaim: quarrel heads                                            [EWS-07]
     Ranged (taught): a lent Border-Warden crossbow at the Ash Roads marks ──► Emberback Boars at dusk
     └─ EWQ Completed is read by EH-M6 §E.10 (Ryl's crossbow commission line)
ESP  Cooking (taught): the shift-supper stew (rib, barley, beans; salt last) ──► three lidded pails
     Vent breath (no skill): warm packing stones on the yard grate between exhales ──► carry to three night crews [EWS-10]
     └─ ESP Completed is read by EH-M6 S01 (EGA-D2.05)
ESH  Leatherworking (taught): pick a hide, soften on an amber bed, cut, stitch, palm-test ──► heat gloves
     ──► duct hood, soot-and-tallow dressing in the loft ──► fit on a line hand in a Working duct [EWS-11 to EWS-13]
     └─ ESH Completed is read by EH-M6 §E.10 (Brisa's coat commission line); heat gear recommended in EH-M3 S03
```

Smithing is the region skill (ED-11): every forge step uses Act I's pattern (heat to the forge tell's amber, shape in channelled segments, quench). Timber is imported, so shafts come only from reclaimed crate-wood. Magma larks are never hunted (EOP owns Hunting). **Ranged is never required**: EWQ's marks have a spotting path and every fight accepts melee.

### 0.3 Economy-pass dependencies (ED-11)

Every material and output below is a **dependency**, not an item. **EWS-01 to EWS-15 are this file's proposal labels for the economy pass, not catalog ids or item names.** Legacy materials (ember shards, emberglass as a catalog item, ashsteel, conduction plates, Volkhari Ash) are not used. Labels shared with the Commons file are noted, not duplicated.

| Id | Working name | Used by | Nearest approved state | Economy pass decides |
|---|---|---|---|---|
| **EWS-01** | imported bar stock | ESK, EOM, EWQ (optional) | Iron bar (= Commons EHC-06) | The gauge-bar recipe. |
| **EWS-02** | guild tag (brass, two marks) | ESK; EOM (forged props) | None | Prop only, unless a maker's-mark system is added. |
| **EWS-03** | ridge ironstone (ore) | EFS | Ore | Name, yield, smelting into EWS-01 (bible §7.2: ore names are proposals). |
| **EWS-04** | flarecap | EFS, EOM | None | Not harvestable here; a world marker. |
| **EWS-05** | crate-wood shaft blanks | EWQ | Ordinary wood (node type = Commons EHC-05) | Shaft recipe (shave, roll-test, straighten). |
| **EWS-06** | magma-lark moult | EWQ | None | A gathered feather at vent baths (EME08 note). Never a Hunting output here. |
| **EWS-07** | quarrel heads | EWQ | None | Head recipe; whether reclaimed heads are a lesser state. |
| **EWS-08** | Border-Warden quarrels | EWQ | None | Ammunition item and stats (rulings §3.4.5: not authored here). |
| **EWS-09** | lent warden crossbow | EWQ (lent tool, returned; not a carry-state, so it can be fired) | None | Not a reward; Act III §E.10's commission is the item pass's. |
| **EWS-10** | shift supper (stew in a lidded pail) | ESP; EH-M6 `S01` | Prepared food | Recipe from imported staples (barley, beans, onion, smoked rib, salt). |
| **EWS-11** | imported hide | ESH | Vegetable-tanned leather | Whether ember-softened hide is a separate state. |
| **EWS-12** | soot-and-tallow dressing | ESH | None | A step, not an item, unless wanted. |
| **EWS-13** | heat gloves; duct hood | ESH (one set fitted to Lenk, one to the player) | Leather gear | Protection value (Act I EH-M3 `S03` assumes heat gear lightens heat-room damage; not set here). |
| **EWS-14** | trough patch (plate, rivets) | EOM | Iron bar products | A station repair, not a carried item. |
| **EWS-15** | guild crates (stolen emberwork) | EOM | None | Props; recovered, never kept. |

### 0.4 Commission givers and stations established

Emberholt's master commissions are gated by `EH_STANDING` and authored in Act III §E.10 (who offers what, where, and the offer line). This file establishes the craft relationships behind four of them and five stations.

| Giver | Craft | Established by | Station opened on completion | Act III §E.10 line this file must make true |
|---|---|---|---|---|
| **Durnan Volkryst** [CANON] | Smithing | ESK, EOM | The Basalt Forge Guild's apprentice hearth (public Smithing station) | *Basalt Forge master piece*: "Forge it to the new rules." / "Forge it the old way. I'll know." by `EH_GUILDS` (EOM). |
| **Ryl Danner** [NEW, bible §5.2] | Fletching, Ranged | EWQ | Ryl's bench in the Embergate yards (public Fletching station; the Ash Roads range as a public practice range) | *Border-Warden's crossbow*: "Feathers first. Then we'll talk about the stock." with *Wardens' Quarrels* Completed. |
| **Brisa Teglan** [NEW, bible §5.2] | Leatherworking | ESH | The tannery cutting bench and stitching horse (public Leatherworking station) | *Frost-warden's lined coat*: "You know hide. Now learn cold." with *Soot and Hide* Completed. |
| **Hennet Ulm** [NEW, bible §5.2] | Cooking | ESP | The Cooling House hearth (public Cooking station) | EH-M6 `S01`: "You know this one. Pails, lids, salt last." with *Shift Supper* Completed. |
| **Breck Krell** [NEW, bible §5.2] | Mining | EFS | The Ridge Workings' upper galleries (public Mining site; Breck weighs ore) | None (no commission proposed). EH-M3 `S02` variant reads EFS Completed. |

### 0.5 Distinctness check

| Quest | Core verb | Physical problem | Wonder or unease | Human choice with a cost |
|---|---|---|---|---|
| ESK | inspect, forge, test | Ring a pallet cold; draw a bar only while it shows colour; hear a lapped bar ring dull after work; take your bar to another hand for its second ring | **Wonder:** at the shift bell the whole hearth line rings its day's bars twice, and the gratework floor hums under the player's boots | None (contract: bars can be re-forged) |
| EOM | inspect, track, assault | Read a holed trough, a cut strap and forged tags; patch the trough; follow ridge charcoal to a kiln; fight the crew; read their ledger | **Unease:** inside the kiln, the crew's own guild aprons hang on pegs in a row, scorched at the same place, as if the hall were still waiting for them | Keep Durnan's new rules (`reformed`) or give the masters their old methods back (`restored`) |
| EFS | mine, read, haul | Strike only where the cap is pale; follow the pale through a gallery of orange; work a face that goes amber and walk off it; clear beetles off a spill | **Wonder:** at dusk the cap along the whole gallery warms from pale to orange in a slow wave toward the player, and back | None (contract: the seam re-offers) |
| EWQ | salvage, fletch, shoot | Split crate-wood; reject a shaft that wobbles; straighten over an amber bed; pick moult off warm stones without the larks; head and fletch; shoot marks; meet boars at dusk | **Wonder:** at dusk, quarrels fletched with lark moult leave a faint ember thread in the air for a heartbeat, all the way to the butt | None (contract) |
| ESP | cook, carry, serve | Brown, simmer and salt last; lid three pails; warm packing stones on a breathing grate; carry a crate to three crews who cannot leave their posts | **Wonder:** a line hand knocks the empty pail lid on the pipe; far down the main, other night crews knock back, one after another, fainter | None (contract) |
| ESH | cut, stitch, fit | Choose a hide; soften on an amber bed; double the palms; hold a gloved hand through a vent's exhale; dress a hood in a hot loft; fit it on a line hand in a Working duct | **Wonder:** in the loft, sparks from the flue land on the dressed hood and roll off it like beads of water | None (contract) |

None repeats a milestone's primary verb or strange moment. ESK's second ring differs from Lowmark *Honest Steel*'s receiving ring (there a bad bar cracks in the trough; here a sound bar is spoiled by cold striking and only another hand's ring after the work hears it). ESP differs from EFC's ward pot and EH-M6 `S01`'s frost pails; ESH's adult gear from EH-M2's children's mitt shells; EFS teaches flarecap on the surface, EH-M3 uses it against a vision.

### 0.6 Shared rules for all six packages

- **Address.** Cinderwall NPCs say "warden's hand" (bible §5.3 rule 8); Durnan says "outsider", then "hand"; Breck and Ryl say "traveller". Origin-neutral (D-3).
- **Tells and heat.** `EH_TELLS` is always true here. Each step pins the heat states it needs (bible §9.2; EI-HT-01 fallback). Waiting in a niche or at a keep-watch bench is always available. No heat meter, no stamina, no stealth or detection (ED-6).
- **The EH-M6 frost (playability audit ES-01).** The EGA hour pin (`EGA_FROST`: dusk until EGA `S01`, night from `S02` to the `S06` keep watch) governs only EGA steps and the frost-variant areas (Cinderwall W1 to W4 and the upper Undercroft). A side step placed in those areas is held while `EGA_FROST` is set and resumes at `EGA_THAW_SEEN`, as EME01 and EME05 already do. Keep watch anywhere else advances this player's hour normally. Any other quest's hour pin applies only to keep watch inside that quest's own step volume (ES-06). EDI-3 (EH-M6 auto-activation) stays open.
- **Skill steps** name their alternative in the beat text; the alternative is still play and costs a turn, a walk or skill XP, never the quest. Skill XP is lower on an alternative (balance pass).
- **Refusal, not failure.** Where a craft rule matters (striking a grey bar, striking under orange cap, mining at amber, salting before the beans soften, straightening over a red bed), the action is **refused** with a small scald, a bounce or a line, and nothing resets. This is the Act I red-cock pattern.
- **Combat.** Every enemy is defeated at 0 HP with the ordinary defeat presentation (CDR-1); none yields, flees, scatters or breaks off; no SX. Every fight accepts melee or ranged and requires neither (CDR-2), and is solo-tuned (CDR-6). No defeated enemy speaks or carries evidence (rulings §3.2): EOM's kiln ledger is read in place (T-2) and the crew is named by Durnan from it, a living non-combatant (T-3).
- **Non-combatants.** Every named person in this file, every apprentice, every line hand, every charcoal burner and every Border-Warden is never targetable. Magma larks are scenery.
- **Evidence and revelations.** Nothing here is evidence for a revelation. The hammerfall, the cap wave, the ember thread, the supper call and the rolling sparks prove nothing. No Remnant, Deepbrand or "below" presence: EOM's saboteurs are a dismissed guild crew selling stolen work to an unnamed ridge carter. The tally board's "old leaks" is not mentioned.
- **Reserved decisions.** No node depends on D-E2, D-S1 or the initiate's name (Iven Calder, ED-3), all ruled 2026-11-15, or on D-3, C07 or the "invaders" wording, and none names the EH-M1 valve order, so no node here carries `[ALLOCATION]`. No Volkhari person appears on screen (D-C06); Maeryn Vall is named once as a seamstress who lined mitts (`EEH_MITTS`), nothing more. No precursor name, roster or casualty count (D-C03). Durnan's canon secrets (destroyed Remnant designs, hidden pre-war methods) are not used.
- **Time.** No calendar dates; the past is dated by events.
- **No failure.** Inactive / Active / Completed only. Death respawns at the quest's named safe point with step, flags and kept progress intact; logout restores the last persisted step and returns a dropped carry-state object or lent tool to its source; walking away keeps the quest Active with the resume hook named in each package; missed moments re-offer on the next keep watch. **Carry-state classes (Integration EI-CA-04; playability audit ES-03):** small documents and tokens are possession flags that never limit movement or attack and are kept across death and logout; only bulky loads (walk, cannot attack) return to their source.
- **Co-op (CDR-6).** Each player's own quest state decides their own tells, stations, props, steps and choices. Shared enemies credit a partner only when the partner's own active step consumes the defeat. A partner who leaves or is ahead never blocks the other. Shared prop presentation is a fallback only (bible §9; MI-CO-06 pattern). No step needs two players; where an NPC supplies a "second hand" (ESK's second ring, ESP's crews, ESH's line hand), it is always an NPC.

### 0.7 Flags set and read

All flags set here are quest-local (`ESK_…`, `EOM_…`, `EFS_…`, `EWQ_…`, `ESP_…`, `ESH_…`) except **`EH_GUILDS`** (bible §9.1, set by EOM). Every flag has exactly one writer. Quest completion states read by the main packages are set by each quest's own completion event and nothing else.

| Flag or state | Values | Set by (one writer) | Read by |
|---|---|---|---|
| `ESK_BAR` | self / called | ESK `S02_draw` | `ESK-D4.10`; EOM `EOM-D1.03` |
| `ESK_LAP_RUNG` | bool | ESK `S03_second` (the lapped bar rung) | `ESK-D4.02` |
| **ESK Completed** (`emberholt.side.sound_stock`) | quest state | ESK `S04_rack` | EOM unlock (with EH-M2) |
| `EOM_SIGNS` | bool | EOM `S01_yard` (three sabotage inspects) | `EOM-D3` options |
| `EOM_TROUGH` | self / crew | EOM `S02_trough` | `EOM-D6.12` |
| `EOM_LEDGER_READ` | bool | EOM `S05_ledger` | `EOM-D6` options |
| `EOM_LID` | bool | EOM `S05_ledger` (stamped crate lid taken, carry-state) | `EOM-D6` options |
| **`EH_GUILDS`** | reformed / restored | **EOM** `S06_hall` (the choice) | **EH-M6** `S03` (`EGA-I15` forges tag; Veska's bleed line), `S08` (`EGA-D13.42`/`.43`), §E.5 barks (`EGA-B10.14`/`.15`), §E.10 (`EGA-D14.02`/`.03`) |
| `EFS_FACE` | self / hauled | EFS `S04_seam` | `EFS-D5.03`; Breck barks |
| **EFS Completed** (`emberholt.side.flarecap_seam`) | quest state | EFS `S05_haul` | **EH-M3** `S02_mouth` Darven variant (flarecap at G4) (Act I dialogue `EGH-D4.12`: "You've read cap before? Breck's ridge? Good.") |
| `EWQ_HEADS` | forged / reclaimed | EWQ `S04_heads` | `EWQ-D5.04` |
| `EWQ_RANGE` | shot / spotted | EWQ `S05_range` | `EWQ-D7.03`; Ryl barks |
| **EWQ Completed** (`emberholt.side.wardens_quarrels`) | quest state | EWQ `S07_bundle` | **EH-M6 §E.10** (`EGA-D14.31`) |
| `ESP_SUPPER` | cooked / hatch | ESP `S02_cook` | `ESP-D5.02` |
| `ESP_CALL_HEARD` | bool | ESP `S04_carry` (the supper call plays) | `ESP-D5.04`; Hennet bark |
| **ESP Completed** (`emberholt.side.shift_supper`) | quest state | ESP `S05_return` | **EH-M6** `S01` (`EGA-D2.05`) |
| `ESH_SET` | self / brisa | ESH `S03_hood` | `ESH-D5.02` |
| **ESH Completed** (`emberholt.side.soot_and_hide`) | quest state | ESH `S05_return` | **EH-M6 §E.10** (`EGA-D14.21`) |
| *(read)* `EH_TELLS` | bool | EH-M1 | Every tell inspect here |
| *(read)* `ECW_SEAT_RING` | self / crew | EH-M1 `S05` | ESK `ESK-D1.10` (`self`, the line Act I A9.2 promised: "You made a seat ring for Dunmor. Show me.") and `ESK-D1.11` (`crew`) |
| *(read)* `EEH_MITTS` | self / maeryn | EH-M2 `S02` | ESH `ESH-D1.10` (`self`, the line Act I promised: "Your shells held. Vall's lining helped.") |
| *(read)* `EGH_FLARECAP` | bool | EH-M3 `S02` | EFS `EFS-D1.10` (the line Act I C9.2 promised: "You've been under the city. Cap's the same everywhere.") |
| *(read)* `HS_SALVAGE_KEEPERS` / `HS_SALVAGE_REFUSED` | bool (exactly one set by Lowmark HS `HS-D5`) | Lowmark *Honest Steel* | ESK `ESK-D2.20` (one optional player line and Durnan's answer). Never required; complete without it. |

---
---

## ESK — Sound Stock

### ESK.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `emberholt.side.sound_stock` |
| Type | Skill intro (Smithing). Guild Ledgers 1/2 (bible §7.1). |
| Unlock | EH-M1 Completed. Offered by Durnan Volkryst at the Basalt Forge Guild receiving shed in the Emberforges (`ESK-D1`). Pointed there by Hennet's bark at the Cooling House (`ESK-B0.1`) and a notice on the Cooling House board (*Basalt Forge: hands wanted for receiving. Ask D.V.*). |
| Resume hook | Durnan at the receiving shed: `ESK-D1.00` "Bars don't ring themselves. Where were you?" pins the step. |
| Skills | Smithing ~[GD: entry; taught from any level] (hook; alternative: call the heats for the apprentice at the evening bell). No combat. |
| Combat share | 0% |
| Cameo | Hennet Ulm (bark); Quint Saddick, Durnan's apprentice [NEW] |
| Choice | None (contract: bars can be re-forged) |
| Unlocks | The guild's apprentice hearth as a public Smithing station; receiving inspection (first and second ring) on bar stock in Emberholt; EOM (with EH-M2) |
| **Anchor** (§7.1) | The Forgeguilds (Durnan Volkryst's Basalt Forge Guild) |
| **World-truth row** | H23 (recovery: the rebuilt city's craft standards) |
| **Revelation role** | None (self-contained). |
| **Recurring evidence** | None. The two-mark guild tag recurs in EOM as a forged prop (no custodian role). |
| **State compliance** | Inactive / Active / Completed. No fail path: a grey bar refuses the hammer (reheat, one interaction); a dull second ring sends the bar back to the fire; the Smithing hook has an evening-bell alternative. |
| **Combat compliance** | No combat. Solo test (CDR-6): one player completes every step alone; the "second hand" is always Quint, an NPC; a partner's ring never completes the player's step. |

**In one paragraph.** **Durnan Volkryst** wants to hear an outsider ring a bar before he lets them near his hearth. The player rings a pallet of imported bar cold and sets aside the dull one; draws a bar to the guild gauge, striking only while it shows colour; then rings a bar Durnan's own hall finished cold yesterday, which rang clear on the trestle and rings dull now. "First ring's for the merchant. Second ring's for whoever stands under it." Nobody rings their own second, so the apprentice **Quint Saddick** rings the player's bar and they strike their marks on each other's tags. At the shift bell the whole hearth line rings its day's work twice.

### ESK.2 Selection record and canon grounding


| Element | Source | Status |
|---|---|---|
| Durnan Volkryst: Basalt Forge Guild; gruff, blunt, honourable; protective of workers and apprentices; rigid safety standards; family forged war tools and he vowed to refocus the guild on infrastructure and defence | Character file §21; Factions §8 | [CANON] |
| The Emberforges: molten rivers, hammerfalls all day, ember veins glowing beneath gratework floors | Dossier §VI.3 | [CANON] |
| Forgeguilds: limited weaponmaking under city mandate | Factions §8 | [CANON] |
| "Ring it twice. Durnan's lot always ring it twice." | Act I `S05` (Hennet) | [NEW], pays off |
| Quint Saddick; the gauge; the colour rule; the two-mark tag; the shift-bell ringing | This package | [NEW] |

### ESK.3 The places [MAP VERIFICATION REQUIRED]

Relative order: the Emberforges' Cinderwall gate (sibling EBL B3) → the Basalt Forge Guild yard → the receiving shed → the apprentice hearth → the guild rack along the yard wall → the gallery over the great hearth line. The guild hall (Act III F2) opens off the yard.

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **K1. The receiving shed** | Offer; first ring | An open shed against the yard wall. Two trestles with six bars of **imported stock** under an importer's chalk tag. A **ring-hammer** on a chain. A refused-bar crate with a few dull bars already in it. | — |
| **K2. The apprentice hearth** | Draw a bar | A small hearth with a bellows, an emberglass **tell** in its hood lip (the forge tell from Act I), an anvil with a **gauge block** (a notched iron plate the bar must pass through), tongs on a rail, a **quench trough** with its own tell at the rim. | — |
| **K3. The guild rack** | Second ring; tags | Along the yard wall: racks of finished bars and hooks, each with a brass **tag** struck with two marks. A small anvil at the rack's end for second rings. Quint's bench. | — |
| **K4. The hearth-line gallery** | Wonder | An iron walkway above the great hearths. Under its **gratework floor**, ember veins glow orange (canon). Forty smiths along the line; hammers going. | Stair from the yard |

### ESK.4 Beats

**Beat 0: The Trestles (`S00_offer`).** *Objective: Talk to the Forge-Master.* At the Cooling House, Hennet: "Durnan's asking after you. Said he'd heard you've got hands. I said I'd heard you had a stomach." (`ESK-B0.1`). In the Emberforges, Durnan at the receiving shed (`ESK-D1`) wants to see an outsider's hands before he lets them near his hearth. With `ECW_SEAT_RING = self`: "You made a seat ring for Dunmor. Show me." (`ESK-D1.10`); with `crew`: "Dunmor's crew fitted your ring. Fine. Your own hands, now." (`ESK-D1.11`). He asks whether the player knows why his hall rings twice; any answer is fine.

**Beat 1: The First Ring (`S01_receive`).** *Objective: Ring the receiving pallet.* Six bars on the trestles. For each: **ring** it with the ring-hammer (one interaction, ~1 s) and **inspect** the result (`ESK-I1`: *Rings clear.* / *Rings dull.*). Five ring clear; one rings dull (a different bar each time the pallet is laid). **Set the dull bar** in the refused crate (one interaction). Setting a clear bar aside is allowed and costs nothing ("Your loss, it was a good bar." `ESK-B1.2`); the step waits for the dull one. Durnan (`ESK-D2`): "First ring's for the merchant. You've done the merchant." Optional, with a Lowmark *Honest Steel* flag set: the player may say where they learned to ring a bar (`ESK-D2.20`).

**Beat 2: Draw a Bar (`S02_draw`).** *Objective: Draw a bar to the guild gauge.* At the apprentice hearth (K2). Two ways, both complete the step:

- **Option A (skill): draw it yourself** (**Smithing ~[GD: entry]**). Take a bar from the trestle (EWS-01). **Heat** it until the forge's tell shows amber (one interaction; ~4 s). **Draw** it on the anvil: a 3-segment channel (~3 s each). The bar shows **colour** for ~6 s after it leaves the fire; its glow fades from orange to dull red to **grey** (visible on the bar). A segment started on a grey bar is **refused**: the hammer bounces and rings flat, a small jar (no damage), and Quint calls "Grey! Back in!" (`ESK-B2.2`). **Reheat** (one interaction) and carry on; completed segments are kept. After the third segment, **pass it through the gauge block** (one interaction; it fits) and **quench** it in the trough (one interaction; the trough's rim tell flicks amber and back). `ESK_BAR = self`.
- **Option B (time-cost): call the heats.** Quint is on the great line until the evening bell. **Keep watch** at the hearth bench until dusk (one turn), then work the bellows and **call** Quint's strikes: three call interactions, each available only while the bar shows colour (calling on grey is refused with Quint's "That's grey. I'm not hitting grey." `ESK-B2.3`). Quint draws, gauges and quenches. `ESK_BAR = called`. Lower Smithing XP.

**Beat 3: The Second Ring (`S03_second`).** *Objective: Get your bar its second ring.* Durnan comes over with a bar from yesterday's rack (`ESK-D3`). "Rang clear on the trestle. Finished cold by a hand who wanted his supper. Ring it." The player **rings** it (one interaction): it rings **dull** (`ESK-I3`; sets `ESK_LAP_RUNG`). **Inspect** it (`ESK-I4`): a hairline lap at the shoulder where it was struck grey. Durnan: "Second ring's for whoever stands under it." Then the rule: "Nobody rings their own second." The player **carries** their bar to Quint at the rack (K3) (carry-state; walk, cannot attack). Quint **rings** it at the rack anvil: clear (the colour rule makes a cold lap impossible on the player's bar). He **strikes his mark** on a brass tag (EWS-02) and hands the player the punch to strike theirs (one interaction). Then Quint holds out his own bar: the player **rings** it for him (one interaction; clear) and strikes their mark on his tag. "Now we're both under each other's bars." (`ESK-D3.20`).

**Beat 4: The Rack (`S04_rack`).** *Objective: Hang your bar on the guild rack.* **Hang** the tagged bar (one interaction). Durnan tells the player to go up to the gallery (K4) before the bell. At the shift bell, **the hammerfall (ESK.5)** plays. Durnan comes up after (`ESK-D4`), pays, and names the apprentice hearth as open to the player. With `ESK_BAR = called` he says so plainly and without contempt (`ESK-D4.11`). He mentions, in passing, that Basalt does not sell edges outside the city's mandate (`ESK-D4.20`; seeds EWQ). Quest Completed.

### ESK.5 The hammerfall (presentation spec: wonder)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Bell** | The shift bell over the great forges. The hammers along the hearth line stop, all of them, within a second. |
| 1–3 s | **First** | At the far end of the line a smith lifts a finished bar and rings it once. The next smith rings theirs. The note travels down the line toward the gallery, forty bars, forty notes, no two quite the same. |
| 3–6 s | **Second** | It comes back: every smith rings the bar of the smith beside them. The second wave is quicker. The gratework under the player's boots hums with it, and the ember veins beneath the grate brighten very slightly with the noise and settle (heat follows the room; no tell changes). |
| 6–8 s | **Quiet** | The hall is silent for one breath. Then someone laughs, and the night shift comes in. |
| After | **Durnan** | "Every bar in this hall's been under two hands. That's all a city is." |
| Meaning | A guild custom. Proves nothing. |

### ESK.6 Encounters and hazards

No enemies. Hazards: the hearth (touching the fire: ordinary small burn and a step back); the quench trough's steam on quench (~1 s plume above head height, harmless). Nothing in the yard is a heat zone.

### ESK.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to the Forge-Master. | `ESK-D1` accept | Yes | Hennet's bark points the way |
| `S01_receive` | Ring the receiving pallet. | Six rings + the dull bar set in the refused crate + `ESK-D2` end | Yes | Dull bar randomised per laying. `ESK-D2.20` optional with an `HS_` flag |
| `S02_draw` | Draw a bar to the guild gauge. | Option A: 3 draw segments + gauge + quench; **or** Option B: keep watch to dusk + 3 calls | Yes | Grey refusal (A) or call refusal (B); nothing resets. Sets `ESK_BAR` |
| `S03_second` | Get your bar its second ring. | Lapped bar rung + inspected + bar carried to K3 + Quint's ring + both tags struck | Yes | Sets `ESK_LAP_RUNG` |
| `S04_rack` | Hang your bar on the guild rack. | Bar hung + gallery volume entered + bell event + `ESK-D4` end | Yes | Hammerfall plays; small payment; quest Completed; EOM offered if EH-M2 is Completed |

| Flag | Set by | Read by |
|---|---|---|
| `ESK_BAR` = self / called | `S02` | `ESK-D4.10`/`.11`; EOM `EOM-D1.03` |
| `ESK_LAP_RUNG` | `S03` | `ESK-D4.02` |

### ESK.8 Choices and consequences

None. The contract row says "Bars can be re-forged"; the quest's weight is a rule learned in the hands.

### ESK.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| Small payment | Currency | Durnan's purse ([GD]). |
| The apprentice hearth | Access | A public Smithing station in the guild yard (K2). |
| Receiving inspection, Emberholt form | Knowledge | Bar stock anywhere in Emberholt can be rung: *"Rings clear."* / *"Rings dull."*; finished work on authored racks can be given a second ring: *"Rings clear after work."* / *"Rings dull after work. Look at the shoulder."* (extends Lowmark HS's receiving ring; no new system). |
| Smithing XP | Action XP only [GD] | Lower on Option B. No lump quest XP. |
| EOM | Story | Offered once EH-M2 is also Completed. |

### ESK.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Strikes a grey bar | Refused; reheat; nothing resets. |
| Sets a clear bar aside | Allowed; Durnan's bark; the step waits for the dull bar. |
| Will not or cannot smith | Option B: one keep-watch turn and three calls; never blocked. |
| Death | Not expected (no hazards beyond the hearth). If it occurs, respawn at the yard bench with all progress kept. |
| Logout | Restore to the step at the receiving shed (`S00`, `S01`), the hearth (`S02`), the rack (`S03`, `S04`). A carried bar returns to the rack anvil. |
| Walking away | Stays Active; resume hook at Durnan (`ESK-D1.00`) or Quint (`ESK-B3.4` "Your bar's on my anvil. It's not ringing itself."). |
| Co-op | Per-player trestles, bar, tags and calls. A partner may stand at the next hearth and draw their own bar; Quint rings each player's bar for that player. The hammerfall plays for every player in the gallery whose own `S04` is active; a partner without the step sees the ordinary bell. |

### ESK.11 Integration needs

All standard: ring interaction with a two-result inspect; a dull bar picked per laying; a hearth heat interaction with the forge tell (Act I); a 3-segment draw channel refused while the held bar's colour state is grey (a ~6 s colour fade on the held prop after leaving the fire: the Act I seat-ring "needs reheating" rule made visible); a gauge-pass interaction; a keep-watch-to-dusk alternative with three call interactions; a carry-state bar; tag strike interactions; a scripted audio and light event for the hammerfall on the bell (forty NPC smith emotes, gratework vein-glow pulse ~3 s).

### ESK.12 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Durnan Volkryst** [CANON], Forge-Master of the Basalt Forge Guild | Every bar in his hall; who rang what; why the rules are what they are. | Nothing he would say to an outsider about what is below. | Gruff, blunt, honourable. Short sentences. Praise is one word. Protective of apprentices: he shouts at the work, never at the hand. Calls the player "outsider", then "hand". |
| **Quint Saddick** [NEW], Durnan's apprentice | The gauge, the rack, every smith's mark. | — | Young, quick, cheerful, says what Durnan says a beat early. |
| **Hennet Ulm** [NEW, bible §5.2] | Everyone's business. | — | Feeds first. |

**Offer** (`ESK-D1`, step `S00_offer`)

```
ESK-D1.00 [quest Active, returning] DURNAN: "Bars don't ring themselves. Where were you?"   (pins step) → end
ESK-D1.01 DURNAN: (not looking up from the trestle) "You're the one who walked Dunmor's line."
ESK-D1.10 [ECW_SEAT_RING = self] DURNAN: "You made a seat ring for Dunmor. Show me." (he holds out a hand; looks at the player's palm, not the face) "Hm. Burn on the thumb. Good."
ESK-D1.11 [ECW_SEAT_RING = crew] DURNAN: "Dunmor's crew fitted your ring. Fine. Your own hands, now."
ESK-D1.02 DURNAN: "I don't let anybody near a hearth of mine I haven't heard ring a bar. Outsider or not."
ESK-D1.03 DURNAN: "Your cook says my lot ring everything twice. Know why?"
  > "So it's sound."                                                  → ESK-D1.04
  > "Because one ring can lie?"                                       → ESK-D1.05
  > "No idea."                                                        → ESK-D1.06
  > "Not now."                                                        → ESK-D1.07
ESK-D1.04 DURNAN: "Half right. Ring the pallet."   {event: accept → S01_receive}
ESK-D1.05 DURNAN: (a grunt that might be approval) "Ring the pallet."   {event: accept → S01_receive}
ESK-D1.06 DURNAN: "Honest. Ring the pallet."   {event: accept → S01_receive}
ESK-D1.07 DURNAN: "The bars'll wait. So will I. Badly."   → end (offer stays open)
```

**Barks: the way in and the trestles**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| ESK-B0.1 | Passing the Cooling House hatch after EH-M1 | HENNET | "Durnan's asking after you. Said he'd heard you've got hands. I said I'd heard you had a stomach." |
| ESK-B1.2 | A clear bar set in the refused crate | DURNAN | "Your loss. It was a good bar." |
| ESK-B1.3 | The dull bar rung | DURNAN | "Hear that? Like a spoon in a cup." |

**The first ring** (`ESK-D2`, end of `S01`)

```
ESK-D2.01 DURNAN: "First ring's for the merchant. You've done the merchant." (he chalks REFUSED on the crate) "He'll argue. He always argues."
ESK-D2.02 DURNAN: "Now make something. Hearth's there. Gauge is the notched plate. If it won't go through the notch, it's not a bar, it's an opinion."
ESK-D2.20 [HS_SALVAGE_KEEPERS or HS_SALVAGE_REFUSED] (optional player line) > "Where I learned to ring a bar, a smith turned away stock that wasn't what its tag said."
ESK-D2.21 DURNAN: "Good smith." (beat) "Every honest forge in the world does the first ring. It's the second one people skip."   → ESK-D2.02
```

**At the hearth** (barks, `S02`)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| ESK-B2.1 | Bar heated to amber | QUINT | "Amber. Hit it while it's talking." |
| ESK-B2.2 | Draw started on a grey bar | QUINT | "Grey! Back in!" |
| ESK-B2.3 | Option B, call on grey | QUINT | "That's grey. I'm not hitting grey." |
| ESK-B2.4 | Gauge passed | DURNAN (from across the yard) | "Through the notch. Quench it." |
| ESK-B2.5 | Option B chosen | QUINT | "I'm on the great line till the bell. Keep the bench warm. Then you call, I hit." |
| ESK-B3.4 | At the rack, `S03` Active, returning | QUINT | "Your bar's on my anvil. It's not ringing itself." |

**The second ring** (`ESK-D3`, `S03`)

```
ESK-D3.01 DURNAN: (a bar from yesterday's rack in one hand) "Rang clear on the trestle. Finished cold by a hand who wanted his supper. Ring it."
      {event: lapped bar ring available; ESK-I3}
ESK-D3.02 [ESK_LAP_RUNG] DURNAN: "Look at the shoulder."   {event: ESK-I4}
ESK-D3.03 DURNAN: "Hit cold, it folds a skin over itself. Rings fine on the trestle, because it hasn't been made yet. Rings like that once it has."
ESK-D3.04 DURNAN: "First ring's for the merchant. Second ring's for whoever stands under it. A hook. A bracket. A seat ring." (beat) "A bridge."
ESK-D3.05 DURNAN: "And nobody rings their own second. You'll always hear what you want from your own bar. Take it to Saddick."
ESK-D3.10 (At the rack.) QUINT: (rings the player's bar; listens with his head on one side) "Clear." (strikes a small mark on a brass tag; hands over the punch) "Yours goes beside it."
ESK-D3.11 QUINT: (holds out his own bar) "And mine. You're my second today."
      {event: ring Quint's bar (clear); strike the player's mark on his tag}
ESK-D3.20 QUINT: "Now we're both under each other's bars." (beat) "That's what he says. I say it first so he can't."
```

**The rack and the bell** (`ESK-D4`, `S04`)

```
ESK-D4.01 DURNAN: (on the gallery, after the bell) "Every bar in this hall's been under two hands. That's all a city is."
ESK-D4.02 [ESK_LAP_RUNG] DURNAN: "That bar you rang. I know whose it was. He'll draw it again tomorrow, and I'll ring his second myself."
ESK-D4.10 [ESK_BAR = self] DURNAN: "Your bar's on my rack. With a mark on it nobody here can read yet." (beat) "Hand."
ESK-D4.11 [ESK_BAR = called] DURNAN: "You called it and Saddick hit it. Calling's half the work. Most people only want the hitting half." (beat) "Hand."
ESK-D4.20 DURNAN: "The apprentice hearth's yours when it's free. Bars, hooks, brackets. Not edges. Basalt doesn't sell edges outside the city's mandate, and I don't lend the hearth for them either."
ESK-D4.21 DURNAN: (coin) "For the pallet."   {small payment; event: ESK-D4 end → quest Completed; EOM offered if EH-M2 is Completed}
```

**Inspect texts**

| Id | Object | Text | Condition |
|---|---|---|---|
| ESK-I1 | A trestle bar, after ringing | "Rings clear." / "Rings dull. Like a spoon in a cup." | — |
| ESK-I3 | Yesterday's bar, rung | "Rings dull." | Sets `ESK_LAP_RUNG` |
| ESK-I4 | Yesterday's bar, the shoulder | "A hairline across the shoulder, where the metal has been folded over itself and not joined. You would not see it unless you were told where to look." | — |
| ESK-I5 | Guild tag (after) | "A brass tag struck with two marks: Quint Saddick's hammer-and-dot, and yours." | — |

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| QUINT | "Need a second? I'm free after the bell." | ESK Completed |

### ESK.13 Open decisions

1. **The Lowmark line (`ESK-D2.20`).** The bible row says "Durnan has heard of a forge that refuses salvage". This package makes it a **player** line answered by Durnan, so he gains no knowledge of another region and no news travels between regions (Part 4 ledger: no individual gains access to another region by role). This is a deliberate deviation from the bible row: giving Durnan the line would hand an Emberholt NPC knowledge of another region's forge, so it is not offered as a swap. `ESK-D2.21` stays generic ("Every honest forge...") and names no place.
2. **Colour fade (~6 s).** A Gameplay Designer value. The rule (no striking grey) is the lesson; the timing is tuning.
3. **"Not edges" (`ESK-D4.20`)** follows Factions §8 (limited weaponmaking under mandate) and Durnan's canon vow; it seeds EWQ's "the guild will not sell to them". If cut, EWQ still works on Ryl's own scorn of the guild.
4. **Smithing `[GD: entry]`:** Gameplay Designer to set; Option B is one turn.

### ESK.14 Review log

| Finding | Revision |
|---|---|
| First draft repeated Lowmark HS (a bad bar cracks on quench). | Replaced with the second ring: a bar sound on receiving is ruined by cold striking, and only another hand's ring after the work hears it. |
| Risk of a skill "fail" state on the draw. | The grey strike is refused, never ruined; the player's bar always rings clear, and the dull note is heard on Durnan's demonstration bar. |
| Second ring by a partner (co-op temptation). | Always Quint (NPC). A partner's ring never completes the player's step (CDR-6). |
| Durnan's canon secrets. | Not used. His war-tool family history is left as subtext ("A bridge."); no war detail is stated. |

---
---

## EOM — The Old Methods

### EOM.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `emberholt.side.old_methods` |
| Type | Combat challenge. Guild Ledgers 2/2 (bible §7.1). |
| Unlock | ESK Completed **and** EH-M2 Completed. **Quest-start requirement: Smithing ~[GD: low]** (the level ESK's own forging reaches; trainable at any public forge). Offered by Durnan Volkryst in the Basalt Forge Guild yard the morning after the sabotage (`EOM-D1`); Quint's bark at the Emberforges gate points there (`EOM-B0.1`). |
| Resume hook | Durnan at the rule board: `EOM-D1.00` "Board's still up. For now. Where are you?" pins the step. |
| Skills | Smithing ~[GD: low–mid] (hook: patch the trough; guild-crew alternative); Melee or Ranged (Forge Saboteurs) |
| Combat share | ~40% (two encounters at the kiln, the second with the Saboteur Captain) |
| Cameo | Quint Saddick (scalded hand); a Whitehearth Forge apprentice; a charcoal burner at the Ridge Steadings (role names) |
| Choice | The masters' vote: keep Durnan's new rules (`EH_GUILDS = reformed`) or restore the old methods (`EH_GUILDS = restored`) |
| Unlocks | `EH_GUILDS` (read by EH-M6); the Saboteurs' Kiln as an empty ridge landmark |
| **Anchor** (§7.1) | The Forgeguilds; Forge Saboteurs |
| **World-truth row** | H25 (present pressure, local: who pays for safety in the city's forges) |
| **Revelation role** | None (local). No Remnant, Deepbrand or "below". |
| **Recurring evidence** | The kiln ledger (read in place; the crew's hammer marks stand for names, and Durnan reads them). The forged two-mark tags recur from ESK as props. |
| **State compliance** | Inactive / Active / Completed. No fail path: the Smithing hook has an overnight crew alternative; defeated groups stay defeated; the vote is always held and both outcomes complete. `EH_GUILDS` reformed / restored. |
| **Combat compliance** | Forge Saboteurs (wrecker, thrower) and the Saboteur Captain (elite) defeated at 0 HP with the ordinary defeat presentation; no yield, retreat or break-off; no SX. Melee or ranged; ranged never required. Solo-tuned (CDR-6): one player clears both encounters alone; a partner's kills credit them only if their own `S04` consumes them; the vote is per player. |

**In one paragraph.** Durnan Volkryst has posted five new rules in the Basalt Forge Guild yard (two rings by two hands; a full trough at every hearth; one shift on the great line; a relief seat banked for the wardens' main; any hand may see a fitting book), and someone is breaking them on purpose. The yard blames the rival **Whitehearth Forge**, and the masters have called a vote to take the rules down. The player reads the sabotage (a round drift, ridge charcoal in a hall that burns none, two marks from one punch), patches the holed trough, and follows the charcoal out to an old kiln on the Ridge, where a crew Durnan dismissed lives among the guild's stolen crates. They fight to the last. Inside are five aprons on pegs and a ledger signed with hammer marks, with the crew's grievance at the front. At the guild hall the masters vote, and Durnan asks the outsider to tell them what was found.

### EOM.2 Selection record and canon grounding


| Element | Source | Status |
|---|---|---|
| Forge Saboteurs: rival smuggler bands; target emberwork shipments | Dossier §XII | [CANON] |
| A crew Durnan once dismissed, working from a ridge kiln | Bible §7.1 EOM row; §10 | [NEW] |
| The Saboteurs' Kiln: an abandoned charcoal kiln used as a hideout | Bible §4.2 EP17 | [NEW] |
| `EH_GUILDS` reformed / restored; the relief seat held for wardens; "By order only. Billed."; "any hand may ask to see a fitting book"; "the guild answers to the guild" | Bible §9.1; Act III `EGA-I15`, `EGA-D13.42`/`.43`, §E.5 | [NEW], made true here |
| Ruel Kessick, the Whitehearth Forge, the five rules, the forged tags, the kiln ledger, the aprons | This package | [NEW] |

### EOM.3 The places [MAP VERIFICATION REQUIRED]

Relative order: the Basalt Forge Guild yard (ESK K1–K4) → (optional) the Whitehearth Forge gate along the hearth line → the Emberforges' Cinderwall gate → Cinderwall → the Cinderwall working gate (bible §4) → the Ash Roads → the Ridge Steadings → a side track up the ridge → the Saboteurs' Kiln. Back the same way to the guild hall (Act III F2).

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **M1. The rule board** (by the guild hall door) | Offer | A new slate beside the guild board, five rules chalked in Durnan's square hand. Someone has scratched *OLD WAYS* across it and somebody else has half rubbed that out. | — |
| **M2. The apprentice hearth** (ESK K2) | Sabotage site 1; the patch | The quench trough, dry, a round hole low in its side, punched from inside. A wet stain across the yard stone. Quint's hand wrapped in wet cloth. | — |
| **M3. The relief hearth** | Sabotage site 2 | One great-line hearth banked low under a painted sign *RELIEF SEAT: WARDENS*. Its bellows hang slack; the strap is cut through. | — |
| **M4. The finished rack** (ESK K3) | Sabotage site 3 | A rack of bracket hooks for the heat main, each tagged with two marks. | — |
| **M5. The Whitehearth Forge gate** (optional) | Clearing the rival | A rival hall's yard gate along the line. A Whitehearth apprentice sweeping. Their drifts hang on a board: square, every one. | — |
| **M6. The Ridge Steadings** (EP05) | Track | Turf-roofed steadings below the ridge. A charcoal burner's clamp smoking; sacks of char stacked; a cart track going up. A fire with a bench (respawn point for `S03`–`S05`). | Through the Cinderwall working gate and along the Ash Roads |
| **M7. The kiln track** | Track | A cart track off the Ash Roads, rutted fresh. Splinters of guild crate (Basalt's stencil) in two ruts. | — |
| **M8. The kiln yard** (EP17) | EOM-E1 | An old beehive kiln of black brick on a ledge, its yard walled with stacked guild crates and slag. A rim ledge on the kiln's shoulder (throwers). The kiln is relit and used as a forge; its mouth **breathes**. | Ramp to the rim ledge (optional, both sides) |
| **M9. The kiln mouth and inside** | EOM-E2; the ledger; the aprons | The mouth's iron door, propped. Inside, a cold chamber: bedrolls, a stolen anvil, five guild **aprons** on pegs, a **ledger** on a crate, a **stamped crate lid**. | — |
| **M10. The Basalt Forge Guild hall** (Act III F2) | The vote | As Act III: smoke-dark, hammers racked, the guild board. Masters on benches; hands standing at the back. | — |

### EOM.4 Beats

**Beat 0: The Board (`S00_offer`).** *Objective: Talk to the Forge-Master.* Quint at the Emberforges gate, hand wrapped: "Durnan wants you. Don't ask about my hand, everybody asks about my hand." (`EOM-B0.1`). Durnan at the rule board (`EOM-D1`): three things broken in one night, a vote called for tomorrow's bell, the yard saying Whitehearth. "Rules didn't hole a trough." He wants someone with no hearth in this hall to look. With `ESK_BAR`, one line remembers the player's bar (`EOM-D1.03`). Below the requirement, the offer is declined plainly (`EOM-D1.06`).

**Beat 1: Three Breaks (`S01_yard`).** *Objective: Find out how the rules were broken.* Three required inspects, any order:

- **The trough** (M2, `EOM-I1`): punched from inside with a **round drift**, a smith's tool, one clean blow.
- **The relief hearth's strap** (M3, `EOM-I2`): cut, not worn; black dust packed in the cut. Inspect again (`EOM-I3`): it is **charcoal**. Quint (`EOM-B1.2`): "We don't burn char. Veins heat this hall."
- **The tags** (M4, `EOM-I4`): every hook carries two marks, and both are the **same punch** struck twice.

Sets `EOM_SIGNS`. Optional: walk to the **Whitehearth Forge gate** (M5): the apprentice there shows the drift board (`EOM-I5`: every drift square) and says Whitehearth wants Basalt's contracts, not its troughs (`EOM-D2`). Durnan hears the three breaks (`EOM-D3`): "One punch, two marks. Somebody's laughing at us."

**Beat 2: The Trough (`S02_trough`).** *Objective: Get the apprentice hearth running.* Under the new rules no hearth runs without a full trough, and the masters will point at a cold hearth tomorrow. Two ways, both complete the step:

- **Option A (skill): patch it** (**Smithing ~[GD: low–mid]**). At the hearth, take a plate blank (EWS-01) from the stock box: **heat** to the forge tell's amber (one interaction); **punch** two rivet holes on the anvil (a 2-segment channel, colour rule as ESK: refused on grey); **set** the plate over the hole and **rivet** it (a 2-segment channel); **fill** the trough at the yard cistern (two carries of a bucket, carry-state). The rim tell reads amber at the first quench test (`EOM-I6`). `EOM_TROUGH = self`.
- **Option B (time-cost): the guild crew.** Durnan sends for the night crew. **Keep watch** at the yard bench until morning (one turn); the crew rivets it while the player fills it (the same two bucket carries). `EOM_TROUGH = crew`.

**Beat 3: The Charcoal (`S03_track`).** *Objective: Follow the charcoal.* Out through the Cinderwall working gate onto the Ash Roads (burnt engravings on the old street walls as scenery; no reading layer here, EDS01 is another package's). At the **Ridge Steadings** (M6), a charcoal burner (`EOM-D4`, role name) says nobody has bought char from him that he did not know, but there is smoke at night from the old kiln up the ridge, which has not been burned in years, and a carter goes up there "with an empty cart and comes down with a full one". Up the side track (M7), **inspect two ruts** (`EOM-I7`, `EOM-I8`): splinters of guild crate with Basalt's stencil. The step completes on reaching the kiln yard's edge.

**Beat 4: The Kiln (`S04_kiln`).** *Objective: Deal with the crew at the kiln.* The kiln yard (M8): **EOM-E1**. Then at the mouth (M9), when the player crosses the yard's inner line: **EOM-E2**, the Saboteur Captain with one wrecker, the kiln mouth breathing on its cycle. Everyone fights to 0 HP. Nothing is said by or taken from the defeated as evidence. The step completes when EOM-E2 is defeated.

**Beat 5: The Ledger (`S05_ledger`).** *Objective: Find out who they were.* Inside the kiln (M9). **The aprons (EOM.5)** play on entering. Required: **read the ledger** in place (`EOM-I10`; sets `EOM_LEDGER_READ`): on the first page five hammer marks instead of names, and the grievance; inside, their tally of the sabotage and the crates sold to "the carter, no name, Ash Roads". **Take the stamped crate lid** (carry-state; sets `EOM_LID`) as proof the crates were Basalt's. Optional: inspect the anvil (`EOM-I11`: Basalt's own, missing from the yard since before the rules). The ledger stays on the crate (read in place, T-2).

**Beat 6: The Vote (`S06_hall`).** *Objective: Tell the masters what you found.* Back to the guild hall (M10). The masters are on the benches; the vote is called (`EOM-D6`). Durnan lays the lid on the board; the player tells what the yard, the ruts and the kiln showed. Durnan reads the marks in the ledger aloud from the player's account: "That's Kessick's." Then the masters ask the outsider the question in front of them. The choice (EOM.8) sets **`EH_GUILDS`**. The masters vote with the player's account. Durnan pays. Quest Completed.

### EOM.5 The aprons (presentation spec: unease)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Enter** | The kiln's inside is cold and smells of old char. The player's lamp finds a row of pegs on the curved brick. |
| 1–3 s | **Aprons** | Five heavy guild aprons hang there, Basalt's stabilising runes on the bibs (canon), each scorched in the same place low on the left, where a smith leans into a hearth. They are hung neatly, spaced as if on the guild hall's own pegs. |
| 3–5 s | **The sixth peg** | A sixth peg is empty. The player's lamp lingers on it. Nothing else happens. |
| After | **No line** | No one speaks. The ledger is on the crate. |
| Meaning | A crew that kept its aprons as if the hall would call them back. Proves nothing about who the sixth was for; the quest never says. |

### EOM.6 Encounters and hazards

Tuned for EH-M2's Advanced identity (ED-10). Forge Saboteurs are the bible's mid-tier human family (§10: wrecker, thrower; elite Saboteur Captain). First seen here.

| Id | Enemies / hazard | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **EOM-E1** | 2 × Forge Saboteur **wrecker**, 2 × **thrower** | The kiln yard (M8): wreckers in the yard, throwers on the kiln's rim ledge | Wreckers close and hold the yard; throwers lob from the ledge | **Wrecker, Overhead:** lifts a sledge two-handed, head glowing from the kiln (~1.5 s; it displaces), then a slam with a 1-pace shock and one-step knock-back. **Wrecker, Bar Sweep:** draws a bar back low (~1.0 s), then a sweeping arc in front. **Thrower, Coal Pot:** swings a smoking pot back behind the shoulder (~1.2 s), then lobs it; it bursts in a 2-pace burning patch (~3 s). | Ranged players duel the ledge; melee players take the ramp; crate walls give cover from the pots | 70–100 s; 55–75% HP |
| **EOM-E2** | **Saboteur Captain** (elite) + 1 × wrecker | The kiln mouth (M9), the mouth breathing | The Captain fights at the mouth and uses its breath; the wrecker guards his flank | **Captain, Hot Bar:** pulls a glowing bar from the kiln mouth, the bar brightening white at the tip (~1.2 s), then a wide arc swing. **Captain, Quench Steam:** hooks a water bucket with his foot (~1.5 s; the bucket lifts), then kicks it across a hot brick: a steam cone in front (damage; no blinding). **Captain, Door:** at about half health he kicks the kiln door wide (~1.0 s windup, the door's hinge glows); from then the **mouth breathes** harder (ash lifts ~1.5 s, exhale in a 3-pace line out of the mouth every ~9 s). **Captain, Close:** if the player stays at range more than ~6 s, he plants a foot and charges (~1.5 s, head down) to melee range. | The yard's last stand: a fight about the forge's own heat | 2.5–3.5 min; 45–65% HP |
| **EOM-H1** | The kiln mouth breath | M9 | Timed hazard | Ash lifts off the mouth's lip ~1.5 s before each exhale (~12 s cycle; ~9 s after the Door) in a 3-pace line; damage and one-step knock-back | The bible's vent breath on a ridge kiln | — |

**Rules.** Every saboteur is defeated at 0 HP with the ordinary defeat presentation; the Captain is defeated at 0 HP like any other enemy (CDR-1); nobody yields, flees or calls a truce. No one speaks after a fight and no evidence drops: the crew is identified only by the ledger (read in place) and by Durnan reading their marks (T-2, T-3). **Melee or ranged** (CDR-2): throwers can be answered by ranged or reached by either ramp; the Captain's Close stops pure range-kiting from trivialising him without making ranged weaker than melee. **Death:** respawn at the steadings fire (M6); EOM-E1, once defeated, stays defeated; the Captain and his wrecker reset on leash (ordinary reset, not a retreat).

### EOM.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to the Forge-Master. | `EOM-D1` accept | Yes | Quest-start requirement Smithing ~[GD: low] gates the accept option |
| `S01_yard` | Find out how the rules were broken. | Trough + strap (two inspects) + tags inspects + `EOM-D3` end | Yes | Sets `EOM_SIGNS`. Whitehearth visit (`EOM-D2`, `EOM-I5`) optional |
| `S02_trough` | Get the apprentice hearth running. | Option A: plate punched + riveted + trough filled; **or** Option B: keep watch to morning + trough filled | Yes | Sets `EOM_TROUGH` |
| `S03_track` | Follow the charcoal. | `EOM-D4` end + both rut inspects + enter kiln-yard edge volume | Yes | — |
| `S04_kiln` | Deal with the crew at the kiln. | EOM-E1 and EOM-E2 all defeated | Yes | Kiln mouth breath on |
| `S05_ledger` | Find out who they were. | Ledger read + lid taken | Yes | Sets `EOM_LEDGER_READ`, `EOM_LID`. Aprons moment plays |
| `S06_hall` | Tell the masters what you found. | `EOM-D6` choice + `EOM-D6.40` end | Yes | Sets **`EH_GUILDS`**; lid removed (left on the guild board); small payment; quest Completed |

| Flag | Set by | Read by |
|---|---|---|
| `EOM_SIGNS` | `S01` | `EOM-D3` options |
| `EOM_TROUGH` = self / crew | `S02` | `EOM-D6.12` |
| `EOM_LEDGER_READ` | `S05` | `EOM-D6` options |
| `EOM_LID` | `S05` | `EOM-D6` options |
| **`EH_GUILDS`** = reformed / restored | `S06` | EH-M6 (`EGA-I15`, `EGA-D13.42`/`.43`, `EGA-B10.14`/`.15`, `EGA-D14.02`/`.03`); forge barks |

### EOM.8 Choices and consequences

| Option | Immediate | Cost | Later (EH-M6 reads) |
|---|---|---|---|
| **Keep the new rules** (`reformed`): *"The rules held. Somebody had to break them on purpose to make them look bad."* | The masters vote the board up. Durnan chalks the five rules on the guild board itself. The relief hearth stays banked under its sign. | Work is slower; pay by the bar stays down; two masters walk out of the vote and say so in the yard; the crew's grievance stands in their ledger, unanswered. | EH-M6: the forges hold a relief seat for the wardens (`EGA-I15` *Relief seat held for wardens. D.V.*); Durnan: "New rules say any hand may ask to see a fitting book." |
| **Restore the old methods** (`restored`): *"The rules cost hands their pay and made them wait for a ring nobody paid for. Give the masters their hearths back."* | The board comes down. Each master's word runs at his own hearth again; pay by the bar returns; the smith rings his own. Durnan keeps two rings in his own hall as his custom, not the guild's rule. | The relief seat goes: the forges take civic heat only by Council order, and bill for it. Durnan's authority is dented in front of his hall. Quint asks who will ring his second now. | EH-M6: the forges take the main's pressure by order and bill the ward (`EGA-I15` *By order only. Billed.*); Durnan: "Old rules say the guild answers to the guild." |

**Neither is wrong.** Both end the sabotage, both return the crates' lid to the guild board, and both leave five aprons on pegs in a cold kiln.

### EOM.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| Small payment | Currency | Durnan's purse ([GD]). |
| `EH_GUILDS` | Region flag | Read by EH-M6 (bleed choice tag, guild reading, barks, master commission line). |
| Melee or Ranged, Smithing XP | Action XP only [GD] | Less Smithing XP on Option B. No lump quest XP. Ordinary loot from defeated saboteurs (economy pass); never evidence. |

### EOM.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Below Smithing ~[GD: low] | The accept option is unavailable; `EOM-D1.06` says what to train (any public forge, including the apprentice hearth after ESK). Never a hidden gate. |
| Strikes a grey plate | Refused (ESK colour rule); reheat. |
| Will not or cannot smith | Option B: one keep-watch turn; never blocked. |
| Beaten at the kiln | Respawn at the steadings fire (M6). EOM-E1 stays defeated; the Captain's group resets on leash; the Door phase resets with him. |
| Logout | Restore to the step: the guild yard (`S00`–`S02`, `S06`), the steadings fire (`S03`–`S05`). The lid, if dropped, returns to the crate in the kiln. |
| Walking away | Stays Active; resume hooks at Durnan (`EOM-D1.00`) or the charcoal burner (`EOM-B3.3` "Smoke again last night. Up there."). The vote waits for the player. |
| Co-op | Shared fights at the kiln (credit to each partner whose own `S04` consumes it). Sabotage inspects, trough, ruts, ledger, lid and vote are per player; a partner's vote does not set the other's `EH_GUILDS`. Any shared rule-board or kiln presentation is presentation only (CDR-6). |

### EOM.11 Integration needs

All standard: three sabotage inspects (one with a second inspect layer); a hearth repair with punch and rivet channels (ESK colour rule); two bucket carries; a keep-watch-to-morning alternative; a rut-inspect trail; two encounter groups with a rim ledge; a phased elite (Hot Bar, Quench Steam, Door at ~50% health, Close on range time) using the ordinary combat kit; a timed hazard at the kiln mouth whose cycle shortens on the Door event; an aprons scripted light beat (~5 s, no line); a carry-state lid; a read-in-place ledger; rule-board and guild-board prop variants by `EH_GUILDS`.

### EOM.12 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Durnan Volkryst** [CANON] | His rules and why; every hammer mark in his hall; why he dismissed Kessick. | Who sabotaged, until the marks are read. | As ESK. Angrier, quieter. |

**Offer** (`EOM-D1`, step `S00_offer`)

```
EOM-D1.00 [quest Active, returning] DURNAN: "Board's still up. For now. Where are you?"   (pins step) → end
EOM-D1.01 DURNAN: (at the rule board; someone has scratched OLD WAYS across it) "Three things broke in my yard last night. Saddick's trough. The relief hearth's strap. A rack of tags."
EOM-D1.02 DURNAN: "The masters have called a vote for tomorrow's bell. They'll stand in front of a cold hearth and say my rules did it. The yard says Whitehearth."
EOM-D1.03 [ESK_BAR] DURNAN: "Your bar's on that rack. Somebody re-tagged the hooks next to it. Didn't touch yours. I'd like to know why."
EOM-D1.04 DURNAN: "Rules didn't hole a trough. I want somebody with no hearth in this hall to look. That's you."
  > [Smithing ~GD low] "I'll look."                                   → EOM-D1.05
  > "What are the rules?"                                            → EOM-D1.20
  > "Not now."                                                       → EOM-D1.07
EOM-D1.05 DURNAN: "Trough's by the apprentice hearth. Strap's on the relief line. Tags on the rack. Don't touch anything till you've read it."   {event: accept → S01_yard}
EOM-D1.06 [Smithing below GD low] DURNAN: "Not with those hands yet. You'll be patching iron before this is done. Get some bars through the notch at the apprentice hearth, or any forge, and come back."   → end (offer stays open)
EOM-D1.07 DURNAN: "Vote's at the bell. It won't wait. I will."   → end
EOM-D1.20 DURNAN: (taps each line) "Rung twice; nobody rings their own second. A full trough at every hearth. Nobody on the great line past one shift. One hearth banked for the wardens' main. Any hand can ask to see a fitting book."
EOM-D1.21 DURNAN: "Five rules. Every one of them is something I've seen go wrong."   → EOM-D1 options
```

**Barks: the yard**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EOM-B0.1 | Emberforges gate, EOM available | QUINT | "Durnan wants you. Don't ask about my hand, everybody asks about my hand." |
| EOM-B1.1 | Trough inspected | QUINT | "I reached for the water. Wasn't any. Only steam." |
| EOM-B1.2 | Strap second inspect | QUINT | "We don't burn char. Veins heat this hall." |
| EOM-B1.3 | Near the rule board | A SMITH | "Whitehearth. Has to be. They've wanted the bracket work for years." |

**Whitehearth** (`EOM-D2`, optional, M5)

```
EOM-D2.01 WHITEHEARTH APPRENTICE: (sweeping) "If Basalt's sent you to accuse us, I'll save you the walk back. We didn't."
  > "Show me your drifts."                                           → EOM-D2.02
EOM-D2.02 WHITEHEARTH APPRENTICE: (points at the board) "Square. All of them. Master likes a square hole." (beat) "We want their bracket contracts. We don't want their troughs."   {EOM-I5} → end
```

**The three breaks** (`EOM-D3`, end of `S01`)

```
EOM-D3.01 [EOM_SIGNS] DURNAN: "Well?"
  > "A round drift, from inside. A smith did it."                     → EOM-D3.02
EOM-D3.02 DURNAN: "Mine are round." (beat) "So are half the city's."
  > "Charcoal in the strap. You don't burn charcoal."                 → EOM-D3.03
EOM-D3.03 DURNAN: "No. Burners on the ridge do."
  > "Two marks on every tag. Both the same punch."                    → EOM-D3.04
EOM-D3.04 DURNAN: (looks at a tag for a long moment) "One punch, two marks. Somebody's laughing at us."
EOM-D3.05 DURNAN: "Get Saddick's hearth running before the bell, or they'll point at it. Then follow the char."   → end
```

**The trough** (barks, `S02`)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EOM-B2.1 | Option A begun | QUINT | "Round plate, two rivets. Don't punch it grey." |
| EOM-B2.2 | Option B chosen | DURNAN | "Night crew'll rivet it. You fill it. Sit." |
| EOM-B2.3 | Trough filled; first quench test | QUINT | "Water. Look at that. Water in a trough." |

**The burner** (`EOM-D4`, M6)

```
EOM-D4.01 CHARCOAL BURNER: (raking a clamp) "City hand. Don't see many up the Ash Roads that aren't lost."
  > "Who buys your char?"                                            → EOM-D4.02
EOM-D4.02 CHARCOAL BURNER: "Everybody I know. Nobody I don't." (beat) "But there's smoke at night off the old kiln. That's not been burned since my father. And a carter goes up with an empty cart and comes down with a full one."
EOM-D4.03 CHARCOAL BURNER: "Track's off the road past the second marker. I don't go up. I've a clamp to mind and a head to keep."   → end
```

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EOM-B3.2 | Kiln-yard edge | (journal) | *The kiln's been relit. Somebody is using it as a forge.* |
| EOM-B3.3 | Returning to M6, quest Active | CHARCOAL BURNER | "Smoke again last night. Up there." |

**At the kiln.** No dialogue with the crew. No lines after the fight beyond the player's journal: *The yard is quiet. The kiln mouth is still breathing.* (`EOM-B4.1`, on EOM-E2 defeated.)

**The vote** (`EOM-D6`, `S06_hall`)

```
EOM-D6.01 (The guild hall. Masters on the benches; hands at the back.) A MASTER: "There's a cold hearth in this yard and five new rules on a board. I don't need a vote to see what broke what."
EOM-D6.02 DURNAN: "Saddick's hearth isn't cold." (to the player) "Tell them."
EOM-D6.12 [EOM_TROUGH = self] QUINT: (from the back) "Outsider riveted it. Two rivets. Not grey."
EOM-D6.13 [EOM_TROUGH = crew] QUINT: (from the back) "Night crew riveted it. Outsider filled it. It holds."
  > [EOM_LID] "These crates were yours. A crew sold them on the ridge."    → EOM-D6.20 (Durnan lays the lid on the board)
  > [EOM_LEDGER_READ] "They signed with hammer marks. Five of them."       → EOM-D6.21
EOM-D6.20 A MASTER: (picks up the lid; turns it over) "That's our stencil."   → EOM-D6 options
EOM-D6.21 DURNAN: (the player describes the marks; he knows the first before the description is finished) "Chipped corner. Kessick." (beat) "The other four followed him off my line. I won't say their names in this hall. Their families can."
EOM-D6.22 DURNAN: "Ruel Kessick. I dismissed him for ringing his own second. Twelve years on my line. A good hand. He wanted to be trusted more than he wanted to be checked."
EOM-D6.23 (optional) > "They wrote why, at the front."                  → EOM-D6.24
EOM-D6.24 DURNAN: (quietly, for the hall) "'Rules cut the shift. Pay's by the bar. Wait for a second and you're not paid to wait.'" (beat) "That's true. I knew it was true."
EOM-D6.30 A SECOND MASTER: "So. Outsider. You've seen the yard and the ridge. Do the rules stay?"
  > "The rules held. Somebody had to break them on purpose to make them look bad."      → EOM-D6.31 {EH_GUILDS = reformed}
  > "The rules cost hands their pay and made them wait for a ring nobody paid for. Give the masters their hearths back."   → EOM-D6.35 {EH_GUILDS = restored}
EOM-D6.31 DURNAN: (takes the chalk; writes the five rules on the guild board itself) "Then they stay. Slow and known." (two masters leave the bench without a word)
EOM-D6.32 QUINT: "Relief seat stays banked, then. Somebody'll be glad of it one night."   → EOM-D6.40
EOM-D6.35 DURNAN: (a long breath) "Then it's every master's word at his own hearth again." (he wipes the rule board himself) "My hall rings twice. That's mine. Nobody else's."
EOM-D6.36 QUINT: "Who rings my second now?" DURNAN: "I do. Same as always."   → EOM-D6.40
EOM-D6.40 DURNAN: (coin; the lid stays on the guild board) "For the walk up the ridge." (beat) "I'll see Kessick's families get the shift they were owed. Don't tell the masters."
      {lid removed (left on the guild board); small payment; event: EOM-D6.40 end → quest Completed}
```

**Inspect texts**

| Id | Object | Text | Condition |
|---|---|---|---|
| EOM-I1 | The trough | "A round hole low in the side, the metal pushed outward. Punched from inside with a round drift, one blow. Somebody knew where to stand." | — |
| EOM-I2 | Relief hearth strap | "Cut, not worn. A clean knife. Black dust packed into the cut." | — |
| EOM-I3 | The strap, again | "Charcoal. Fine and greasy, the kind that comes off a burner's sacks." | — |
| EOM-I4 | Rack tags | "Two marks on every tag, as the rule says. Both marks are the same punch: the same chip on the same corner, struck twice." | — |
| EOM-I5 | Whitehearth drift board | "Drifts on pegs, every one square in section." | Optional |
| EOM-I6 | Trough rim tell, first quench test | "Amber, and back to clear. Water where water should be." | `EH_TELLS` |
| EOM-I7 | First rut | "Fresh. Splinters of crate in the mud, stencilled with Basalt's mark." | — |
| EOM-I8 | Second rut | "Heavier going down than up." | — |
| EOM-I10 | The kiln ledger | First page: five hammer marks in a column, struck into the paper with a punch. Under them, in one hand: *Rules cut the shift. Pay's by the bar. Wait for a second and you're not paid to wait. Ring your own and you're out. Twelve years.* Inside: *Trough, one. Strap, one. Tags, a rack. Crates, four. To the carter, no name, Ash Roads.* | Sets `EOM_LEDGER_READ` |
| EOM-I11 | The anvil (optional) | "A guild anvil, Basalt's mark on the foot. The kind that goes missing from a yard and is never mentioned." | — |

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| DURNAN | "Board's on the wall where it belongs." | `EH_GUILDS = reformed` |
| DURNAN | "My hall rings twice. Theirs can do as they like." | `EH_GUILDS = restored` |
| QUINT | "Hand's healed. Trough's holding." | Either |

### EOM.13 Open decisions

1. **The relief seat as one of Durnan's rules [NEW].** Act III reads `EH_GUILDS = reformed` as "the forges hold a relief seat open for the wardens under Durnan's new rules"; this package puts the seat on the rule board so that reading is true. If the Director prefers the seat to come from elsewhere, rule 4 is cut from `EOM-D1.20` and the board; the vote is unchanged.
2. **Ruel Kessick and the Whitehearth Forge [NEW]:** grepped across `04_CONTENT_PRODUCTION`, `LORE` and `00_ADMIN` with no collision.
3. **The crew's grievance** makes `restored` a principled choice rather than a weak one. If the Director wants the old methods shown as plainly worse, cut `EOM-D6.24`; the choice still stands on the masters' authority.
4. **The unnamed carter** is deliberately not a thread. It must not be linked to ECC's merchant-house front or to any Remnant buyer.
5. **Quest-start requirement Smithing ~[GD: low]:** Gameplay Designer to set at or below what ESK's own forging reaches.

### EOM.14 Review log

| Finding | Revision |
|---|---|
| First draft had the Captain give up the crew's names at low health. | Removed (CDR-1). He fights to 0 HP; the ledger's marks name the crew, read by Durnan (T-2 then T-3). |
| Rival forge as a red herring with no check. | The Whitehearth drift board clears it by an object, optionally; the main path clears it by the charcoal. |
| Choice weight. | Both outcomes have a visible cost in the hall and a distinct EH-M6 reading; neither is the "correct" answer. |
| Risk of a Remnant reading of a smuggler band. | No below, no Deepbrand, no gate buyer; the carter is unnamed and stays so. |

---
---

## EFS — The Flarecap Seam

### EFS.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `emberholt.side.flarecap_seam` |
| Type | Skill intro (Mining). Standalone (bible §7.2). |
| Unlock | EH-M1 Completed. Offered by Breck Krell at the Ridge Workings head (`EFS-D1`); a notice on the Cooling House board (*Ridge Workings: hands for the seam. Ask Krell.*) and a ridge hand's bark at the Cinderwall working gate (`EFS-B0.1`) point there. |
| Resume hook | Breck at the tag board: `EFS-D1.00` "Your tag's still on the board. That means you're still down. Are you?" pins the step. |
| Skills | Mining ~[GD: entry; taught from any level] (hook; alternative: haul two carts); Melee or Ranged (Slag Beetles) |
| Combat share | ~15% (one beetle spill) |
| Choice | None (contract: the seam re-offers) |
| Unlocks | The Ridge Workings' upper galleries as a public Mining site; Breck weighs ore |
| **Anchor** (§7.1) | Ridge miners (the Ridge Workings; the Ridge Steadings) |
| **World-truth row** | H02 (surface only: the ridge's veins as working ground) |
| **Revelation role** | None (self-contained). |
| **Recurring evidence** | None. |
| **State compliance** | Inactive / Active / Completed. No fail path: striking under orange cap or at an amber face is refused, never reset; the face cycles back to clear; the Mining hook has a hauling alternative. |
| **Combat compliance** | Slag Beetles (EFS-E1) defeated at 0 HP. Melee or ranged; ranged never required. Solo-tuned (CDR-6): one player clears the spill and mines or hauls alone; a partner's kills credit them only if their own `S03` consumes them. No SX. |

**In one paragraph.** Out through the Cinderwall working gate and along the Ash Roads, past the steadings, the Ridge Workings are shallow galleries where Emberholt's ridge hands cut ironstone from the cool margins of the veins. **Breck Krell**, the quarry foreman, cheerful and careful, teaches the outsider the miners' oldest rule: flarecap glows pale on cool rock and orange beside a live vein, so you strike where it is pale and leave the orange alone. He sends the player down the cap gallery, through a stope where Slag Beetles feed on an old spill, to the seam face, where the wardens' tells set in the rock tell the second rule: work while the face is clear, and when the tells go amber, walk to the niche and wait. At dusk the player sees the whole gallery's cap warm and fade like a held breath. Then they haul what they cut up to the head, Breck weighs it, and takes their tag off the board.

### EFS.2 Selection record and canon grounding


| Element | Source | Status |
|---|---|---|
| Flarecap fungus glows bright orange near ember veins; used by miners to locate unstable pockets | Dossier §XIII | [CANON] |
| "Orange cap means a live vein close by: do not strike, cut or brace there"; Darven's "Pale cap, cool rock" | Bible §1.1; Act I `EGH-D4.10` | [NEW], consistent |
| The Ridge Workings (shallow flarecap and ore galleries); the Ridge Steadings | Bible §4.2 EP14, EP05 | [NEW] |
| Slag Beetles (crawler, sprayer; burst into sparks) | Dossier §XII; bible §10; Act I `ECW-E2` | [CANON] |
| Breck Krell | Bible §5.2 | [NEW] |
| Ridge ironstone (ore name), the practice face, the cap wave | This package | [NEW] |

### EFS.3 The places [MAP VERIFICATION REQUIRED]

Relative order: the Cinderwall working gate → the Ash Roads → the Ridge Steadings (EP05) → the Ridge Workings head (EP14) → the upper gallery → the cap gallery → the beetle stope → the seam face. Nothing beyond the Ridge is placed.

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **R1. The Workings head** | Offer; tag board; weighing | A timber-propped mouth in the ridge (timber reused from crates, scarred with stencils). A **tag board** with brass tags on pegs, a tool shed, an ore cart on a short rail, a beam scale. A warden's **tell** set in the mouth's lintel. Breck's slate: *CAP PALE, STRIKE. CAP ORANGE, LEAVE. FACE AMBER, WALK.* | — |
| **R2. The upper gallery** | Practice face | A short, well-lit gallery. A **practice face** with three clumps of cap: two pale, one orange at a seam. | — |
| **R3. The cap gallery** | Follow the pale | A longer gallery forking twice. Pale cap along the safe wall; patches of orange where the rock is warm, each a pinned **Surging** heat zone (red-crazed tell at its edge; heavy periodic damage). The pale way is always walkable. | One optional agility step across a dry runnel (fallback: round by the pale wall) |
| **R4. The beetle stope** | EFS-E1 | A wide chamber where an old smelting spill cooled into a slag fan. Slag Beetles on it, feeding. A cooling niche cut in the wall with a water butt. | — |
| **R5. The seam face** | Mine | A low face streaked with dark ironstone. Three **ore points** along it, each with a small tell set into the rock by the wardens. Pale cap above, a band of orange far below in a sump (out of reach; scenery). A cooling niche with a water butt and a keep-watch ledge. | — |

### EFS.4 Beats

**Beat 0: Tag In (`S00_offer`).** *Objective: Talk to the quarry foreman.* At the Workings head, Breck Krell (`EFS-D1`): the seam is open and his hands are short. With `EGH_FLARECAP`: "You've been under the city. Cap's the same everywhere." (`EFS-D1.10`). Accept: take a pick from the shed (or use the player's own) and **hang a tag** on the board (one interaction). Inspect the lintel tell (`EFS-I1`: clear).

**Beat 1: The Cap (`S01_cap`).** *Objective: Learn to read the cap.* At the practice face (R2), Breck teaches (`EFS-D2`). **Inspect** a pale clump (`EFS-I2`) and the orange clump (`EFS-I3`). **Strike** the pale rock: three Mining interactions (~2 s each), each giving a piece of ironstone (EWS-03). **Striking near the orange clump is refused:** a puff of heat out of the seam (small damage, one step of knock-back); Breck: "Orange! Leave her!" (`EFS-B1.2`). Nothing resets. The step completes on three pale strikes.

**Beat 2: Follow the Pale (`S02_gallery`).** *Objective: Follow the pale cap to the seam.* Down the cap gallery (R3). At each fork the pale wall is the way; the orange patches are Surging zones that heavily damage anyone who walks in (pinned; the red-crazed tells show it). Two required tell inspects at the forks (`EFS-I4`, `EFS-I5`). The step completes on entering the stope.

**Beat 3: The Spill (`S03_stope`).** *Objective: Clear the beetles off the spill.* **EFS-E1** on the slag fan (R4). When the last beetle is defeated, Breck's voice comes down the gallery (`EFS-B3.2`).

**Beat 4: The Seam (`S04_seam`).** *Objective: Cut six pieces from the seam.* At the face (R5). Each ore point's tell runs on a short timed cycle: **clear ~30 s, amber ~15 s** (a timed hazard with a visible tell, bible §11.1). Two ways, both complete the step:

- **Option A (skill): work the face** (**Mining ~[GD: entry]**). Strike an ore point while its tell is clear: one Mining interaction (~2 s) per piece. Striking a point whose tell is amber is **refused**: the pick bites, steam spits from the crack (small damage, no ore), and Breck's rule comes up (`EFS-B4.2`: "Amber, you walk."). Nothing resets. The three points are staggered, so a player who reads the tells can usually find one clear; one who cannot waits in the niche. Six pieces. `EFS_FACE = self`.
- **Option B (time-cost): haul for the hands.** Two of Breck's hands come down to cut. The player **pushes the ore cart** from the face to the head and back, **twice** (a carry-state cart on the rail; walk, cannot attack; the run passes the cap gallery's pale way), about a turn of walking. The hands' six pieces are counted to the player. `EFS_FACE = hauled`. Lower Mining XP.

On the sixth piece (either way), if the presentation hour is dusk or later, **the cap wave (EFS.5)** plays; otherwise it plays on the first keep watch in the niche or on the way out at dusk.

**Beat 5: Haul and Tag Out (`S05_haul`).** *Objective: Bring the ironstone up and tag out.* Up to the head. **Load** the cart (one interaction, Option A) and **weigh** at the beam scale with Breck (`EFS-D5`). **Take the tag** off the board (one interaction). Breck pays by weight and opens the upper galleries to the player. Quest Completed.

### EFS.5 The cap wave (presentation spec: wonder)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Dusk** | The face's tells are clear. The gallery is quiet. |
| 1–4 s | **Warming** | Far down the gallery the pale cap begins to colour: yellow, then orange, clump by clump, the colour travelling up the gallery toward the player like a lamp being carried. The face's tells go amber with it. |
| 4–6 s | **Held** | For a breath the whole gallery glows orange. The player's own shadow is thrown up the wall. |
| 6–10 s | **Fading** | The colour goes back down the gallery the way it came, and the cap is pale again. The tells clear. |
| After | **Breck** (if present) or journal | "She does that at dusk. Walk when she does it; come back when she's done." |
| Meaning | The vein below warming and cooling. Proves nothing. |

### EFS.6 Encounters and hazards

Tuned for EH-M1's Advanced identity (ED-10).

| Id | Enemies / hazard | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **EFS-E1** | 3 × Slag Beetle **crawler**, 1 × **sprayer** (bible §10) | The slag fan (R4) | Crawlers guard the fan; the sprayer sits on its crest and spits | As Act I `ECW-E2`: **Crawler, Butt** (head down, plates glowing ~1.5 s, short charge-butt, small knock-back). **Sprayer, Spit** (rears, abdomen swelling red ~1.0 s, slag gob, burning patch ~4 s). **Burst** on defeat (~1.5 s glow, sparks in a 1-pace ring, light damage). | A wide room to move in after a narrow gallery | 50–75 s; 65–85% HP |
| **EFS-H1** | Orange-cap Surging zones | R3 | Pinned hazard volumes | Red-crazed tell at each edge; orange cap visible from a distance | The cap rule as terrain | — |
| **EFS-H2** | Amber face | R5 | Timed refusal | The ore point's tell turns amber (~15 s); strike refused with steam and small damage | The tell rule as a work rhythm | — |

**Rules.** Beetles are defeated at 0 HP (sparks; canon). Melee on the fan or ranged at the sprayer on the crest both work; nothing requires ranged. **Death:** respawn at the Workings head (R1) with the tag still on the board; defeated beetles stay defeated; ore already cut is kept; the cart (Option B) returns to the face.

### EFS.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to the quarry foreman. | `EFS-D1` accept + tag hung | Yes | `EFS-D1.10` with `EGH_FLARECAP` |
| `S01_cap` | Learn to read the cap. | Two cap inspects + three pale strikes | Yes | Orange strike refused |
| `S02_gallery` | Follow the pale cap to the seam. | Two fork tell inspects + enter stope volume | Yes | Orange patches pinned Surging |
| `S03_stope` | Clear the beetles off the spill. | EFS-E1 all defeated | Yes | — |
| `S04_seam` | Cut six pieces from the seam. | Option A: six strikes at clear; **or** Option B: two cart runs | Yes | Face tells on a 30 s / 15 s cycle. Sets `EFS_FACE`. Cap wave at dusk |
| `S05_haul` | Bring the ironstone up and tag out. | Weighed + `EFS-D5` end + tag taken | Yes | Payment by weight; quest Completed (read by EH-M3 `S02_mouth`) |

| Flag | Set by | Read by |
|---|---|---|
| `EFS_FACE` = self / hauled | `S04` | `EFS-D5.03`; Breck barks |

### EFS.8 Choices and consequences

None. The contract row says "Seam re-offers"; after completion the upper galleries are an ordinary Mining site on the same face cycle.

### EFS.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| Payment by weight | Currency | Breck's scale ([GD]). |
| Ridge ironstone | Output | The pieces the player cut are theirs (EWS-03; economy pass). On Option B the hands' pieces are paid out instead. |
| The Ridge Workings | Access | Upper galleries as a public Mining site; Breck weighs and buys ore (economy pass). |
| Cap and face reading | Knowledge | Flarecap clumps across the Ridge are inspectable (pale / orange). |
| Mining, Melee or Ranged XP | Action XP only [GD] | Lower Mining XP on Option B. No lump quest XP. |

### EFS.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Strikes under orange cap | Refused with a heat puff; nothing resets. |
| Walks into an orange patch | Heavy periodic damage; a red-crazed tell warned first; the pale way is always open. |
| Strikes at amber | Refused; wait for clear or use another point. |
| Will not or cannot mine | Option B: two cart runs; never blocked. |
| Death | Respawn at R1 (above). |
| Logout | Restore to the step at R1 (`S00`–`S02`, `S05`) or the stope niche (`S03`, `S04`). The cart returns to the face. |
| Walking away | Stays Active; resume hook at Breck (`EFS-D1.00`). The tag stays on the board until the player tags out (presentation only; it blocks nothing). |
| Co-op | Shared beetle fight (credit to each partner whose own `S03` consumes it). Each player has their own ore points' cycle, pieces, cart and tag; a partner's strikes never count to the player's six. Any shared face presentation is presentation only (CDR-6). |

### EFS.11 Integration needs

All standard: Mining interaction on ore points; a per-point timed tell (clear ~30 s, amber ~15 s) with a strike refusal at amber; orange-cap pinned hazard volumes with red tells (EI-HT-01 fallback); a refused strike near orange cap at the practice face; a carry-state ore cart on a short rail; a beam-scale weigh interaction; a tag-board prop; the cap-wave light event at dusk (~10 s emissive sweep along the gallery's cap props, tied to the presentation hour).

### EFS.12 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Breck Krell** [NEW, bible §5.2], quarry foreman | Every gallery on the ridge; every hand's tag. | What lies under the city. | Cheerful, cautious; never sends anyone where he would not go. Counts on his fingers. Calls the player "traveller", then "hand". |
| **RIDGE HAND** (role; two speakers) | The cart, the face. | — | Short, friendly, dusty. |

**Offer** (`EFS-D1`)

```
EFS-D1.00 [quest Active, returning] BRECK: "Your tag's still on the board. That means you're still down. Are you?"   (pins step) → end
EFS-D1.01 BRECK: (cheerful, a slate under his arm) "Traveller! You've got the look of somebody who walked out the working gate on purpose. Want a day's work?"
EFS-D1.10 [EGH_FLARECAP] BRECK: "Oh, you've been under the city. I can see it on your boots. Cap's the same everywhere. Worse manners down there, I hear."
EFS-D1.02 BRECK: "The seam's open and I'm two hands short. I'll teach you the cap, you cut what you can, I pay by weight. Nobody goes where I wouldn't."
  > "Teach me."                                                       → EFS-D1.03
  > "Why's the board full of tags?"                                   → EFS-D1.04
  > "Not now."                                                        → EFS-D1.05
EFS-D1.03 BRECK: "Pick from the shed. Hang a tag. You take it off coming out, so I know you came out."   {event: accept → S00 tag interaction}
EFS-D1.04 BRECK: "Everybody who's down. I count them twice a shift." (beat) "Every miner on every mountain does it. It's not clever. It's just the thing you do."   → EFS-D1 options
EFS-D1.05 BRECK: "Seam's not going anywhere. Neither am I, much."   → end
```

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EFS-B0.1 | At the Cinderwall working gate, EFS available | RIDGE HAND | "Krell's after hands at the Workings. Pays by weight. Feeds you if you look sad." |

**The cap** (`EFS-D2`, practice face)

```
EFS-D2.01 BRECK: (holds his lamp low; the cap shows pale) "Cap. Grows on the ridge anywhere it's warm and damp. Pale like this, the rock behind it's cool. Strike there."
EFS-D2.02 BRECK: (moves the lamp; one clump at the seam glows orange) "That's a vein, close. Don't strike it, don't cut it, don't lean on it. You'd be surprised how many lean."
EFS-D2.03 BRECK: "Ironstone sits in the cool beside the warm. So you follow the cap toward the orange, and you stop on the pale. Three on the pale. Go on."   → end
```

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EFS-B1.1 | First pale strike | BRECK | "That's it. Dark streak, pale cap. That's ironstone. Two more." |
| EFS-B1.2 | Strike near orange | BRECK | "Orange! Leave her!" |
| EFS-B2.1 | Entering the cap gallery | BRECK (calling after) | "Pale wall all the way. If the cap's orange in front of you, you're on the wrong side of it." |
| EFS-B3.1 | Stope entered | RIDGE HAND (far up) | "Beetles on the old spill! They'll be eating!" |
| EFS-B3.2 | EFS-E1 defeated | BRECK (down the gallery) | "Was that sparks? Don't tell me, I can smell it." |
| EFS-B4.2 | Strike at amber | BRECK (echoing; or journal) | "Amber, you walk." |

**The weigh** (`EFS-D5`)

```
EFS-D5.01 BRECK: (on the scale) "Six. Clean pieces. No orange in them."
EFS-D5.02 [cap wave seen] BRECK: "Saw her at dusk, did you? She does that. Walk when she does it; come back when she's done."
EFS-D5.03 [EFS_FACE = hauled] BRECK: "You pushed that cart like it owed you money. My hands say thank you. I'll pay you their weight."
EFS-D5.04 BRECK: (coin, counted on his fingers) "Take your tag off. Then I know you're out." (beat) "Upper galleries are yours when you want them. Same rules."
      {payment by weight; event: tag taken → quest Completed}
```

**Inspect texts**

| Id | Object | Text | Condition |
|---|---|---|---|
| EFS-I1 | Lintel tell | "Clear. Cool." | `EH_TELLS` |
| EFS-I2 | Pale cap | "Flarecap, pale as a candle in daylight. The rock behind it is cool to the hand." | — |
| EFS-I3 | Orange cap | "Flarecap glowing bright orange at a seam in the rock. The air in front of it shimmers. A live vein, close." | — |
| EFS-I4 | First fork tell | "Left: clear. Right: red, crazed. Orange cap on the right wall." | `EH_TELLS` |
| EFS-I5 | Second fork tell | "Straight on: clear. Down: amber, then red past the bend." | `EH_TELLS` |
| EFS-I6 | Ore point tell | "Clear. Cool. Strike." / "Amber. Working. Walk." | `EH_TELLS` |

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| BRECK | "Hand! Seam's clear today. Mostly." | EFS Completed |

### EFS.13 Open decisions

1. **Ore name** "ridge ironstone" (EWS-03) is a proposal for the economy pass (bible §7.2).
2. **Face cycle (30 s / 15 s)** is a Gameplay Designer value; the rule (work at clear, walk at amber) is the lesson.
3. **Order with EH-M3.** EFS can be done before or after EH-M3. Before: EH-M3's Darven variant fires. After: Breck's `EFS-D1.10` fires. Both are flavour.
4. **Mining `[GD: entry]`:** Gameplay Designer to set; EH-M3's fall needs Mining ~[GD: mid], reachable at the upper galleries after EFS.

### EFS.14 Review log

| Finding | Revision |
|---|---|
| Risk of duplicating EH-M3's flarecap lesson. | EFS teaches the same rule on the surface and adds the face tell rhythm; EH-M3 uses the cap under the city against a vision. Each reads the other's completion only for one line. |
| A strike that hurts could read as a fail. | Refusals deal small damage and never reset progress; the pale way and the niche are always available. |

---
---

## EWQ — Wardens' Quarrels

### EWQ.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `emberholt.side.wardens_quarrels` |
| Type | Skill intro (Fletching, Ranged). Standalone (bible §7.2). |
| Unlock | EH-M1 Completed. Offered by Ryl Danner at the Border-Wardens' bench in the Embergate merchant yards (`EWQ-D1`). |
| Resume hook | Ryl at the bench: `EWQ-D1.00` "Feathers don't fletch themselves. Neither do I, these days." pins the step. |
| Skills | Woodcutting (reclaimed crate-wood only); Fletching ~[GD: entry; taught]; Ranged ~[GD: entry; taught]; optional Smithing ~[GD: low]. Alternatives: reclaim heads from the old butts and wait for Ryl's file; spot for Ryl at dusk. Melee or Ranged (Emberback Boars). |
| Combat share | ~20% (one boar pack at the range) |
| Choice | None (contract) |
| Unlocks | Ryl's bench as a public Fletching station; the Ash Roads range as a public practice range; Ryl's crossbow commission later (Act III §E.10) |
| **Anchor** (§7.1) | Border-Wardens (Emberguard division; Haelric Stormvein's command, off-screen) |
| **World-truth row** | H25 (present pressure, local: who the guilds will supply) |
| **Revelation role** | None (self-contained). |
| **Recurring evidence** | None. |
| **State compliance** | Inactive / Active / Completed. No fail path: a warped shaft is set aside, a red bed refuses the jig, the larks return; every skill step has an alternative. Crate-wood re-spawns. |
| **Combat compliance** | Emberback Boars (EWQ-E1) defeated at 0 HP. Ranged natural here, never required: the pack can be fought in melee, and the marks have a spotting alternative. Solo-tuned (CDR-6): one player clears the pack, fletches and shoots alone; Ryl never fights; a partner's kills credit them only if their own `S06` consumes them. No SX. |

**In one paragraph.** **Ryl Danner** fletches for Captain Haelric Stormvein's Border-Wardens and is out of quarrels; the Basalt Forge Guild will not sell edges outside the city's mandate, and Ryl would rather make his own. The player splits shaft blanks from broken import crates, shaves and rolls them, straightens them over an ember bed that must be amber and never red, picks magma-lark moult off the warm stones of a ridge vent bath, and forges or reclaims heads. At dusk on the Ash Roads range the player shoots the marks, or spots for Ryl, and each lark-fletched quarrel leaves a thread of emberlight. Then Emberback Boars come down to the warm range.

### EWQ.2 Selection record and canon grounding


| Element | Source | Status |
|---|---|---|
| Border-Wardens: mountain perimeter patrols under Haelric Stormvein (Emberguard division) | Factions §6; character file §26 | [CANON] |
| Forgeguilds: limited weaponmaking under city mandate | Factions §8; ESK `ESK-D4.20` | [CANON]; [NEW] consequence |
| Magma larks nest near heat vents; feathers shimmer with emberlight | Dossier §XIII | [CANON] |
| Larks bathe in vent shimmer and scatter at a footstep; feathers gatherable for EWQ | Bible §7.4 EME08 | [NEW] |
| Emberback Boars: ember-hardened plates; charge during resonance spikes | Dossier §XIII; bible §10 | [CANON] |
| Ryl Danner: dry; scorns guild smiths; loves good feathers | Bible §5.2 | [NEW] |
| The jig, the range, the ember thread, the boars at dusk | This package | [NEW] |

### EWQ.3 The places [MAP VERIFICATION REQUIRED]

Relative order: Embergate's merchant yards (EP01) → (for forged heads) Cinderwall and the Cooling House yard forge (Act I W2) → the Cinderwall working gate → the Ash Roads (EP09) → the wardens' range beside the road → a vent bath on the ridge slope above it.

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **Q1. Ryl's bench** | Offer; shafts; fletching | Under the gate wall in the merchant yards: a fletcher's bench, a shaving horse, a **straightening jig** over a small **ember bed** with a tell, a glue pot, a rack with three empty quiver-boxes stencilled *B-W*. Ryl's file hangs on a nail. | — |
| **Q2. The crate stack** | Woodcutting | Broken import crates stacked against the yard wall, stencils of merchant houses on the boards (no house named). A chopping block and hatchet. | — |
| **Q3. The range** | Marks; boars | Beside the Ash Roads where the old street widens: three **marks** (painted discs on straw butts against a fallen wall), a shooting line chalked on the road stones, and two **old butts** stuck with spent quarrels. Burnt engravings on the street walls (scenery; EDS01 not read here). | — |
| **Q4. The vent bath** | Feathers | A shelf of warm stones on the slope above the range, a vent breathing shimmer. **Magma larks** bathing in it. Moulted feathers lie on the stones, each catching the light. | Short climb from the range |

### EWQ.4 Beats

**Beat 0: The Empty Boxes (`S00_offer`).** *Objective: Talk to the wardens' fletcher.* Ryl at Q1 (`EWQ-D1`): three empty boxes, a guild that won't sell, a captain who wants full boxes before the next long patrol, and an outsider standing about. He lends the player a hatchet.

**Beat 1: Crate-Wood (`S01_blanks`).** *Objective: Split shaft blanks from crate-wood.* At the crate stack (Q2): **split** three crate boards into billets (Woodcutting interaction ×3, ~3 s each; reclaimed crate-wood only, shared node type with the Commons file's EHC-05). Woodcutting is taught from any level here; there is no skill gate.

**Beat 2: Shafts (`S02_shafts`).** *Objective: Make six straight shafts.* At Ryl's bench (**Fletching ~[GD: entry]**): **shave** each billet to the gauge on the shaving horse (a 2-segment channel); **roll** each shaft down the bench (one interaction) and **inspect** it (`EWQ-I2`): one of the first batch wobbles every time; **set it aside** (one interaction) and shave a seventh. **Straighten** in the jig over the ember bed (one interaction per shaft) while the bed's tell is **amber**. Ryl stokes the bed during this step; at one point it runs **red** (scripted, once): the jig is **refused** (the shaft scorches at the tip; the player lets go; Ryl damps the bed: "Red. Leave it. Amber straightens, red burns."). Nothing resets.

**Beat 3: Moult (`S03_feathers`).** *Objective: Gather lark moult from the vent bath.* Out through the working gate to the Ash Roads and up to the vent bath (Q4). The larks scatter at a footstep (ambient; no stealth, no detection) and come back to the shimmer ~10 s later. **Pick up** four moulted feathers from the warm stones (one interaction each). The vent breathes on its cycle (ash lifts ~1.5 s, exhale; small damage and one step of knock-back on the shelf's centre stones). No lark is ever harmed or targetable (scenery).

**Beat 4: Heads (`S04_heads`).** *Objective: Get six quarrel heads.* Two ways, both complete the step:

- **Option A (skill): forge them** (**Smithing ~[GD: low]**). Ryl gives a bar offcut (EWS-01). At the Cooling House yard forge in Cinderwall (Act I W2; public since EH-M1): **heat** to the forge tell's amber; **draw a point** (a 2-segment channel per pair; ESK colour rule if ESK is known, otherwise the same refusal without the name); **punch the socket** (one interaction); **quench**. Six heads (EWS-07). `EWQ_HEADS = forged`.
- **Option B (time-cost): reclaim them.** At the range's old butts (Q3), **pull** six spent quarrels (one interaction each) and bring the heads to Ryl. He files them at the bench while the player **keeps watch** until dusk (one turn). `EWQ_HEADS = reclaimed`.

Then at the bench: **fletch** (a 2-segment channel per pair: glue and bind three feathers) and **seat the heads** (one interaction per pair). Six quarrels (EWS-08). Ryl inspects one, holds it to the light, and is quiet for a moment (`EWQ-D5`).

**Beat 5: The Marks (`S05_range`).** *Objective: Test the quarrels at the marks.* At the range at **dusk** (keep watch at the range bench if it is earlier). Ryl lends a **Border-Warden crossbow** (EWS-09; a lent tool, not a carry-state, returned at `S07`). Two ways, both complete the step:

- **Option A (Ranged ~[GD: entry; taught]): shoot.** Ryl teaches the span and the loose in two lines (`EWQ-D6`). Shoot the three marks (near, middle, far; any hits count, misses cost only a quarrel picked up again from the butt). Each lark-fletched quarrel leaves **the ember thread (EWQ.5)**. `EWQ_RANGE = shot`.
- **Option B (spotting, no Ranged): call the fall.** Ryl shoots; the player stands at the spotting stone and, after each of three loosings, **inspects** the butt (`EWQ-I6`) and calls where the quarrel struck (dialogue choice: *high*, *true*, *low*). Ryl adjusts the fletching between shots. Any call completes; the true call earns his nod. The ember thread plays on Ryl's shots. `EWQ_RANGE = spotted`.

**Beat 6: The Boars (`S06_boars`).** *Objective: Deal with the boars on the range.* As the light goes, an **Emberback Boar** pack comes down the Ash Roads to the warm stones at the range (`EWQ-B6.1`): **EWQ-E1**. Ryl stays on the fallen wall and calls the charges; he never fights (`EWQ-B6.2`–`.4`). The step completes when the pack is defeated.

**Beat 7: The Bundle (`S07_bundle`).** *Objective: Bring the bundle to Ryl.* At Ryl's bench, the player hands over the quarrels (the economy pass decides how many the player keeps) and returns the crossbow. Ryl chalks the box *B-W: 6. R.D.* (`EWQ-D7`), pays, and opens his bench to the player. Quest Completed.

### EWQ.5 The ember thread (presentation spec: wonder)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Loose** | At dusk, a lark-fletched quarrel leaves the crossbow. |
| 0–0.6 s | **Thread** | Behind it, for the length of its flight, a fine line of emberlight hangs in the air, the colour of the larks' feathers in the vent shimmer. |
| 0.6–1.5 s | **Hang** | The thread stays a heartbeat after the quarrel strikes the butt, then thins from the bow end forward and is gone. |
| After | **Ryl** | First time only: "Huh." (beat) "Never got that from a goose." |
| Meaning | Lark feathers shimmering (canon). Proves nothing; gives no combat bonus. |

### EWQ.6 Encounters and hazards

Tuned for EH-M1's Advanced identity (ED-10). Emberback Boars are the bible's low-tier ridge family (boar, tusker). Old Plate (EOP) is not here.

| Id | Enemies / hazard | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **EWQ-E1** | 2 × Emberback Boar **boar**, 1 × **tusker** (bible §10) | The range (Q3), arriving down the Ash Roads | Boars charge in lines along the old street; the tusker holds close and gores | **Boar, Charge:** lowers its head, back plates glowing ember-orange (~1.5 s), then charges ~6 paces in a straight line; sidestep. **Tusker, Gore:** paws the stones twice (~1.5 s), then a hooking tusk sweep in a front arc (no displacement). **Resonance spike** (canon): when the range vent exhales (ash lift ~1.5 s, ~12 s cycle), every boar's plates flare and its next action is a Charge. | The bundle's first real use: open ground for ranged, the fallen wall's corners for melee | 50–80 s; 60–80% HP |
| **EWQ-H1** | The vent bath and range vent | Q4 centre stones; Q3 corner vent | Timed hazard | Ash lifts ~1.5 s before each exhale; damage and one-step knock-back | Vent breath outside the city | — |

**Rules.** Boars are defeated at 0 HP and can be harvested where the economy allows (rulings §3.1.4). None breaks off. **Melee or ranged** (CDR-2): the charges reward sidestepping either way; nothing requires ranged. **Death:** respawn at the range bench (Q3); defeated boars stay defeated; the quarrels, crossbow and any completed marks are kept.

### EWQ.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to the wardens' fletcher. | `EWQ-D1` accept | Yes | Hatchet lent |
| `S01_blanks` | Split shaft blanks from crate-wood. | Three splits | Yes | Reclaimed crate-wood only |
| `S02_shafts` | Make six straight shafts. | Six shaved + rolled + straightened (one set aside) | Yes | One scripted red-bed refusal |
| `S03_feathers` | Gather lark moult from the vent bath. | Four pickups | Yes | Larks scatter and return; vent breath |
| `S04_heads` | Get six quarrel heads. | Option A: six forged; **or** Option B: six pulled + keep watch to dusk; then fletch + seat | Yes | Sets `EWQ_HEADS` |
| `S05_range` | Test the quarrels at the marks. | Option A: three marks hit; **or** Option B: three calls | Yes | At dusk. Crossbow lent. Sets `EWQ_RANGE` |
| `S06_boars` | Deal with the boars on the range. | EWQ-E1 all defeated | Yes | Ryl never fights |
| `S07_bundle` | Bring the bundle to Ryl. | Hand-in + crossbow returned + `EWQ-D7` end | Yes | Small payment; quest Completed (read by EH-M6 §E.10) |

| Flag | Set by | Read by |
|---|---|---|
| `EWQ_HEADS` = forged / reclaimed | `S04` | `EWQ-D5.04` |
| `EWQ_RANGE` = shot / spotted | `S05` | `EWQ-D7.03`; Ryl barks |

### EWQ.8 Choices and consequences

None (contract). The quest's question (why will the guild not sell to the wardens) is answered in ESK and here by the same canon fact, and left as a working grievance.

### EWQ.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| Small payment | Currency | Ryl's purse ([GD]). |
| Quarrels | Output | A share of the bundle (EWS-08; economy pass). The lent crossbow is returned (EWS-09). |
| Ryl's bench; the range | Access | Public Fletching station; practice range on the Ash Roads. |
| Fletching, Ranged, Woodcutting, Smithing (A) XP | Action XP only [GD] | Lower on the alternatives. No lump quest XP. |

### EWQ.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Keeps a warped shaft | It fails the roll inspect every time; the step waits for six straight ones. |
| Uses the jig on red | Refused; Ryl damps the bed. |
| Will not smith | Option B: reclaim and one keep-watch turn. |
| Will not shoot | Option B: spot for Ryl. Never blocked. |
| Beaten by the boars | Respawn at the range bench (above). |
| Logout | Restore to the step at Ryl's bench (`S00`–`S02`, `S04` fletching, `S07`), the range bench (`S03`, `S05`, `S06`), or the yard forge (`S04` Option A). The crossbow returns to Ryl and is lent again at `S05`. |
| Walking away | Stays Active; resume hook at Ryl (`EWQ-D1.00`). |
| Co-op | Shared boar fight (credit to each partner whose own `S06` consumes it). Each player splits, shaves, gathers, heads, fletches and shoots their own; a partner's hits never count to the player's marks. Any shared range presentation is presentation only (CDR-6). |

### EWQ.11 Integration needs

All standard: a reclaimed-wood node (as EHC-05); Fletching channels at a bench; a roll-test inspect with one scripted reject; a jig interaction refused while the bed tell is red (scripted once); ambient larks that scatter at proximity and return (~10 s), with feather pickups; Smithing at the existing yard forge; reclaim pickups at the butts; a lent carry-state crossbow; three range marks; a spotting alternative (three inspects and a dialogue call); the ember-thread trail VFX on lark-fletched quarrels at dusk (presentation only); boar Charge tied to the range vent's exhale.

### EWQ.12 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Ryl Danner** [NEW, bible §5.2], Border-Warden fletcher | Feathers, glue, every warden's draw weight; the guild's refusal. | Anything his captain intercepts (never raised). | Dry; scorns guild smiths; loves good feathers. Says "huh" when moved. Calls the player "traveller", then "fletcher" once. |

**Offer** (`EWQ-D1`)

```
EWQ-D1.00 [quest Active, returning] RYL: "Feathers don't fletch themselves. Neither do I, these days."   (pins step) → end
EWQ-D1.01 RYL: (tapping an empty box stencilled B-W) "Three boxes. Empty. Captain wants them full before the next long patrol."
EWQ-D1.02 RYL: "Basalt won't sell me heads. 'Not outside the mandate.' Mandate's on a desk. Desk's in a building. Building's full of people who don't shoot."
EWQ-D1.03 RYL: "So I'll make them. Timber's dear. Crates aren't." (he holds out a hatchet) "You've got hands, traveller. Want to use them on something that flies?"
  > "Show me."                                                        → EWQ-D1.04
  > "Why not buy from another forge?"                                 → EWQ-D1.05
  > "Not now."                                                        → EWQ-D1.06
EWQ-D1.04 RYL: "Split three boards. Not the ones with nails. Bring me billets."   {lend hatchet; event: accept → S01_blanks}
EWQ-D1.05 RYL: "They all look at Basalt before they decide what they think." (beat) "Smiths."   → EWQ-D1 options
EWQ-D1.06 RYL: "Boxes'll stay empty. They're good at it."   → end
```

**At the bench** (barks)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EWQ-B2.1 | First roll | RYL | "Roll it. If it wobbles, it'll wobble in the air too, only further away." |
| EWQ-B2.2 | Warped shaft rolled | RYL | "That one's a walking stick. Set it aside." |
| EWQ-B2.3 | Bed runs red (scripted) | RYL | "Red. Leave it. Amber straightens, red burns." (he damps the bed with a wet sack) |
| EWQ-B3.1 | Leaving for the vent bath | RYL | "Larks bathe in the shimmer above the range. Don't chase them. Pick up what they drop. They drop plenty." |

**The heads and fletching** (`EWQ-D5`)

```
EWQ-D5.01 RYL: (holds a fletched quarrel up to the light; lark feathers catching it) "Huh."
EWQ-D5.02 RYL: "Good feathers. Better than goose. Don't tell the geese."
EWQ-D5.04 [EWQ_HEADS = forged] RYL: "And heads with no guild mark on them. I like them more already."
EWQ-D5.05 [EWQ_HEADS = reclaimed] RYL: "Old heads, new shafts. That's how the wardens have always done it, whatever the captain thinks."   → end
```

**The range** (`EWQ-D6`)

```
EWQ-D6.01 RYL: (handing over a crossbow) "Warden's issue. It's lent, not given. Foot in the stirrup, pull to the nut, quarrel in the groove, look, loose."
EWQ-D6.02 RYL: "Near mark first. Don't aim at the middle of it. Aim at a speck in the middle of it."
  > [Option A] "I'll shoot."                                          → end {S05 Option A}
  > [Option B] "You shoot. I'll watch where they land."               → EWQ-D6.10
EWQ-D6.10 RYL: "Spotter, then. Stand on the stone. Tell me high, true or low. Lie and I'll know."   {S05 Option B}
EWQ-D6.11 (after each loosing; the player inspects the butt) > "High." / "True." / "Low."
EWQ-D6.12 RYL: [call matches] "Good eye." / [call misses] "Look again. No. Fine. I'll trust you this once."
```

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EWQ-B5.1 | First ember thread | RYL | "Huh." (beat) "Never got that from a goose." |
| EWQ-B6.1 | Boars arrive | RYL | "Company. They like the warm stones at dusk." |
| EWQ-B6.2 | Vent ash lifts | RYL | "Vent's going. They'll charge." |
| EWQ-B6.3 | Tusker paws | RYL | "Big one's pawing. Step off." |
| EWQ-B6.4 | Pack defeated | RYL | "That's a test the captain can't argue with." |

**The bundle** (`EWQ-D7`)

```
EWQ-D7.01 RYL: (counting quarrels into a box) "Six." (chalks the box: B-W: 6. R.D.)
EWQ-D7.03 [EWQ_RANGE = shot] RYL: "And you can shoot, a bit. Keep the span you learned. Don't let anybody teach you to rush it."
EWQ-D7.04 [EWQ_RANGE = spotted] RYL: "And you can see where they land. Most shooters can't. They just shoot again."
EWQ-D7.05 RYL: (takes the crossbow back; pays) "Bench is yours when I'm not on it. Bring your own feathers." (beat) "Fletcher."
      {crossbow returned; small payment; event: EWQ-D7 end → quest Completed}
```

**Inspect texts**

| Id | Object | Text | Condition |
|---|---|---|---|
| EWQ-I1 | Ember bed tell | "Amber. Working. Warm enough to straighten." / (scripted) "Red, crazed. Too hot." | `EH_TELLS` |
| EWQ-I2 | A rolled shaft | "Rolls straight." / "Rolls with a wobble at the far end." | — |
| EWQ-I4 | Lark moult | "A flight feather, red-gold, that seems to hold the vent's shimmer in it after it is picked up." | — |
| EWQ-I6 | Butt after a loosing (spotting) | "High." / "True." / "Low." (the authored result for that shot) | Option B |

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| RYL | "Feathers, fletcher? No? Then what are you for?" | EWQ Completed |

### EWQ.13 Open decisions

1. **Haelric Stormvein stays off-screen.** His canon secret (intercepted messages) belongs to ECC; this quest only names him as Ryl's captain.
2. **The ember thread** is presentation only; if the Director wants lark feathers to be ordinary, cut the VFX and `EWQ-B5.1`.
3. **No pass wording.** Ryl says "the next long patrol", never "the passes", so nothing here echoes the R15 broadsheet phrase (ED-14).
4. **Ranged and Fletching `[GD: entry]`:** Gameplay Designer to set; spotting is the non-ranged path.

### EWQ.14 Review log

| Finding | Revision |
|---|---|
| Ranged as a required step. | The marks have a spotting alternative; the boars can be fought in melee (CDR-2). |
| Larks as Hunting targets. | Never: moult only, scenery that scatters and returns. Hunting stays with EOP. |
| Timber. | Crate-wood only (ED-11); the node type is shared with EBL's crate-oak. |
| Boars breaking off at low health. | None: they fight to 0 HP (CDR-1). |

---
---

## ESP — Shift Supper

### ESP.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `emberholt.side.shift_supper` |
| Type | Skill intro (Cooking). Standalone (bible §7.2). |
| Unlock | EH-M1 Completed. Offered by Hennet Ulm at the Cooling House hatch, from the shift supper list on the board (`ESP-D1`). |
| Resume hook | Hennet: `ESP-D1.00` "Pails are where you left them. So are the crews. Hungry." pins the step. |
| Skills | Cooking ~[GD: entry; taught from any level] (hook; alternative: work Hennet's hatch for a turn). No combat. |
| Combat share | 0% |
| Cameo | Veska Dunmor and two line hands (the Undercroft stair); a slag-lane night crew; forge night hands at the Emberforges' Cinderwall gate (role names) |
| Choice | None (contract) |
| Unlocks | The Cooling House hearth as a public Cooking station; the shift supper recipe (EWS-10); EH-M6 `S01` line |
| **Anchor** (§7.1) | The Cooling House (Cinderwall's night crews) |
| **World-truth row** | H23 (recovery: a ward feeding the people who keep it warm) |
| **Revelation role** | None (self-contained). |
| **Recurring evidence** | None. |
| **State compliance** | Inactive / Active / Completed. No fail path: salting early is refused, stones wait for the next rest, nothing goes cold on the way; the Cooking hook has a hatch alternative. |
| **Combat compliance** | No combat. Solo test (CDR-6): one player cooks, packs and carries alone; the crews are NPCs; a partner's pails never count to the player's three. |

**In one paragraph.** On the Cooling House board, under the rotas and the lost cat, is the **shift supper list**: three night crews who cannot leave their posts and eat what is carried to them. Hennet's hatch boy used to carry it; now he works the slag shift himself and is on the list. Hennet teaches the stew the night crews have always eaten (rib browned, barley and beans in, a long simmer under the brass hood, **salt last**), then the part that makes it a shift supper: lids on, pails packed in a crate of stones warmed on the yard's vent grate, carried out hot. The player takes the crate down the Undercroft stair to Veska's line, out along the slag lanes, and over to the Emberforges' night gate. At the stair, a line hand knocks his empty lid on the pipe, and far down the main, other night crews knock back.

### ESP.2 Selection record and canon grounding

| Element | Source | Status |
|---|---|---|
| Cooks create flame patterns for evenly seared food; emberwork fuels cooking | Dossier §III | [CANON] |
| The Cooling House: hearth under a brass hood with a tell; a board with "a shift supper list"; the yard vent | Act I W2 | [NEW], consistent |
| Hennet Ulm: "Feeds first. Sit down; you're running hot." | Bible §5.2 | [NEW] |
| *Shift Supper*: a stew that keeps hot under a lid; "Pails, lids, salt last" | Bible §7.2; Act III `S01`, `EGA-D2.05` | [NEW], made true here |
| Vent breath (ash lifts before the exhale) | Bible §1.1 | [NEW], consistent |
| The packing stones, the three crews, the supper call | This package | [NEW] |

### ESP.3 The places [MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **P1. The Cooling House hearth** (Act I W2) | Offer; cook | The hearth under the brass hood, its tell in the lip; **pails and lids** on hooks; Hennet's store shelves (barley sacks, a bean crock, onion strings, a smoked rib on a hook, the salt crock). The board with the **shift supper list**. | — |
| **P2. The yard vent grate** | Packing stones | In the yard: an iron grate over a warm vent that breathes (~10 s). A heap of fist-sized river stones (imported, smooth) and a straw-lined **crate** with three pail wells. | — |
| **P3. The Undercroft stair niche** (Act I U1) | Delivery 1; the supper call | The blue niche at the stair's foot; Veska and two line hands on the night line. | Stair |
| **P4. The slag lanes** (EP02) | Delivery 2 | A lane along the tip edge at night: a slag-cart crew at a brazier. Hennet's hatch boy among them. | — |
| **P5. The Emberforges' Cinderwall gate** (sibling EBL B3) | Delivery 3 | The gatekeeper's hut; forge night hands come to the gate on their break. | — |

### ESP.4 Beats

**Beat 0: The List (`S00_offer`).** *Objective: Talk to the cook.* Hennet, ladle in hand, taps the supper list (`ESP-D1`): three crews, one pair of hands short. "You've got a stomach and two feet. I'll teach you the rest."

**Beat 1: The Store (`S01_store`).** *Objective: Get what the stew needs from the store.* From the shelves (P1): **take** the rib, a measure of barley, a measure of beans, an onion string and the salt crock (five interactions; the salt crock goes on the hearth shelf, not in the pot).

**Beat 2: The Stew (`S02_cook`).** *Objective: Cook the shift supper.* Two ways, both complete the step:

- **Option A (skill): cook it** (**Cooking ~[GD: entry]**). Standard cooking interactions at the hearth: **brown** the rib (one interaction, ~3 s; the hood tell amber); **add** onion, barley, beans and water (one interaction); **simmer** (a 3-segment channel, ~4 s each, at the hearth; the pot can be left and the channel resumed); **salt** (one interaction, after the third segment). Salting before the simmer is done is **refused**: Hennet's hand on the player's wrist, "Salt last. Beans'll never soften." (`ESP-B2.2`). Nothing resets. `ESP_SUPPER = cooked`.
- **Option B (time-cost): work the hatch.** Hennet cooks; the player **works the hatch** for one turn of the presentation hour (a held interaction handing out bowls, leavable and resumable; dusk → night). `ESP_SUPPER = hatch`. Lower Cooking XP.

**Beat 3: Pails and Stones (`S03_pack`).** *Objective: Pack three pails to keep hot.* **Ladle** the stew into three pails and **lid** them (one interaction each; the lid's cloth tie is part of it). At the yard grate (P2): **set** six stones on the grate (one interaction for three) while the vent rests, and **lift** them after an exhale (one interaction): ash lifts off the grate ~1.5 s before each exhale; setting or lifting during the exhale deals small damage and a step of knock-back (Hennet: "Watch the ash, not the stones." `ESP-B3.2`). Twice. **Pack** the warm stones round the pails in the crate (one interaction). Hennet: "Pails, lids, salt last. And stones." (`ESP-D3.01`).

**Beat 4: The Crews (`S04_carry`).** *Objective: Carry supper to the three night crews.* The **crate** is carry-state (walk, cannot attack; set down and picked up freely). Three deliveries, any order, each **set a pail down** (one interaction) and a short exchange:

- **The Undercroft stair** (P3): Veska and two line hands (`ESP-D4.10`). When the pail is emptied, **the supper call (ESP.5)** plays; sets `ESP_CALL_HEARD`.
- **The slag lanes** (P4): the cart crew, and Hennet's hatch boy, who pretends not to know the pail (`ESP-D4.20`).
- **The forge gate** (P5): two forge night hands (`ESP-D4.30`).

Nothing goes cold on the way; there is no timer (the stones are the reason, not a clock).

**Beat 5: The Pails Come Back (`S05_return`).** *Objective: Bring the pails back to Hennet.* The crews send the empty pails back with the player (or the player collects them on a second pass; either). At the Cooling House, Hennet chalks *Carried* against each line of the supper list, feeds the player first, then pays (`ESP-D5`). Quest Completed.

### ESP.5 The supper call (presentation spec: wonder)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Lid** | At the stair niche, a line hand finishes, stands, and knocks his empty lid three times on the main's pipe beside the niche. |
| 1–3 s | **First answer** | A pause. Then, far down the duct, three knocks come back, small. |
| 3–8 s | **More** | Then another three, further and fainter; then another; four or five answers in all, each from a junction the player cannot see, each a little later and quieter, until the last is barely there. |
| After | **Veska** | "Supper's come. Everybody on the line knows now. Half of them'll be jealous." |
| Meaning | Night crews telling each other supper has come, the old way. Proves nothing. |

### ESP.6 Encounters and hazards

No enemies. Hazard: the yard vent grate (ESP.4 Beat 3; small damage and knock-back on the exhale). The Undercroft stair niche is a cooling niche; nothing in the delivery route is a heat zone the player must cross.

### ESP.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to the cook. | `ESP-D1` accept | Yes | — |
| `S01_store` | Get what the stew needs from the store. | Five takes | Yes | — |
| `S02_cook` | Cook the shift supper. | Option A: brown + add + 3 simmer segments + salt; **or** Option B: one hatch turn | Yes | Early salt refused. Sets `ESP_SUPPER` |
| `S03_pack` | Pack three pails to keep hot. | Three pails lidded + two stone cycles + packed | Yes | Vent breath on the grate |
| `S04_carry` | Carry supper to the three night crews. | Three deliveries | Yes | Carry-state crate. Sets `ESP_CALL_HEARD` at the stair |
| `S05_return` | Bring the pails back to Hennet. | Pails returned + `ESP-D5` end | Yes | Small payment and a bowl; quest Completed (read by EH-M6 `S01`) |

| Flag | Set by | Read by |
|---|---|---|
| `ESP_SUPPER` = cooked / hatch | `S02` | `ESP-D5.02` |
| `ESP_CALL_HEARD` | `S04` | `ESP-D5.04`; Hennet bark |

### ESP.8 Choices and consequences

None (contract).

### ESP.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| A bowl and a small payment | Food, currency | Hennet feeds first ([GD]). |
| The Cooling House hearth | Access | Public Cooking station; the shift supper recipe (EWS-10) is known to the player (economy pass). |
| Cooking XP | Action XP only [GD] | Lower on Option B. No lump quest XP. |

### ESP.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Salts early | Refused; nothing resets. |
| Caught by the vent's exhale | Small damage and knock-back; the stones stay where they were. |
| Will not or cannot cook | Option B: one hatch turn; never blocked. |
| Death | Not expected; if it occurs, respawn at the Cooling House with progress kept and the crate at the hearth. |
| Logout | Restore to the step at the Cooling House (`S00`–`S03`, `S05`) or at the last delivery made (`S04`; the crate returns to the hearth with the undelivered pails). |
| Walking away | Stays Active; resume hook at Hennet (`ESP-D1.00`). |
| Co-op | Per-player pot, pails, stones, crate and deliveries; each crew eats from each player's own pail. A partner's deliveries never count to the player's three. The supper call plays for each player whose own delivery triggers it. |

### ESP.11 Integration needs

All standard: store pickups; Cooking interactions and a 3-segment simmer at an existing hearth with a refused out-of-order salt; a hatch hold interaction advancing the presentation hour (Act III Option B pattern); set and lift interactions on the yard vent grate with its timed exhale; a carry-state crate with three pail props; three delivery interactions; the supper-call audio event (three knocks, then four or five answering knocks, each further and quieter, ~8 s); supper-list chalk prop variants.

### ESP.12 Dialogue

**Cast notes**

| Character | Knows | Voice |
|---|---|---|
| **Hennet Ulm** [NEW, bible §5.2] | Every crew's supper and who skips it. | Feeds first. "Sit down; you're running hot." Short, warm, bossy. Calls the player "warden's hand". |
| **Veska Dunmor** [NEW, bible §5.2] | Her line. | As Act I: short, exact. |
| **HATCH BOY** (role; on the slag crew now), **LINE HAND**, **SLAG CREW**, **FORGE HAND** | Their own night. | Quick Cooling House humour. |

**Offer** (`ESP-D1`)

```
ESP-D1.00 [quest Active, returning] HENNET: "Pails are where you left them. So are the crews. Hungry."   (pins step) → end
ESP-D1.01 HENNET: (taps the board with the ladle) "Supper list. Three crews who can't leave their posts. Line wardens on the stair, the slag carts, the forge night gate."
ESP-D1.02 HENNET: "My hatch boy used to carry it. Now he's on the slag shift and on the list." (beat) "Proud of him. Short of feet."
  > "I'll carry it."                                                  → ESP-D1.03
  > "Teach me the stew."                                              → ESP-D1.03
  > "Not now."                                                        → ESP-D1.04
ESP-D1.03 HENNET: "You'll do both. You've a stomach and two feet. Store's behind me. Rib, barley, beans, onion. Salt crock on the shelf, not in the pot."   {event: accept → S01_store}
ESP-D1.04 HENNET: "Then sit and eat. They'll still be hungry later. So will you."   → end
```

**The stew** (barks, `S02`)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| ESP-B2.1 | Rib browning | HENNET | "Brown, not black. Hood's amber. Good." |
| ESP-B2.2 | Salt tried before the simmer ends | HENNET | (a hand on the wrist) "Salt last. Beans'll never soften." |
| ESP-B2.3 | Option B chosen | HENNET | "Hatch, then. Hand bowls out, take nothing back but the bowl. I'll do the pot." |
| ESP-B3.2 | Caught at the grate | HENNET | "Watch the ash, not the stones." |

```
ESP-D3.01 HENNET: (checking the crate) "Pails, lids, salt last. And stones." (beat) "Every night crew in this ward has eaten out of a pail like that since before I could lift one. Nobody remembers the nights. Everybody remembers the stew."   → end
```

**The crews** (`ESP-D4`)

```
ESP-D4.10 (Stair niche.) VESKA: "Hennet's?" (lifts the lid; smells it) "Hennet's." (to the line hands) "Eat. Then read the tells. In that order tonight."
ESP-D4.11 LINE HAND: (eating) "Rib. He found rib." (finishes; stands; knocks the lid on the pipe three times)   {event: supper call; set ESP_CALL_HEARD}
ESP-D4.12 VESKA: (listening to the answers) "Supper's come. Everybody on the line knows now. Half of them'll be jealous."   → end
ESP-D4.20 (Slag lanes.) SLAG CREW: "Pail! Somebody's remembered us!"
ESP-D4.21 HATCH BOY: (not looking at the pail) "That's not Hennet's. That's somebody else's." (eats) "...It's Hennet's."   → end
ESP-D4.30 (Forge gate.) FORGE HAND: "Hot? Still hot? How's it still hot?" (feels the stones in the straw) "Oh. Stones. My nan did that."   → end
```

**The pails come back** (`ESP-D5`)

```
ESP-D5.01 HENNET: (chalks CARRIED three times; puts a bowl in front of the player before anything else) "Eat first."
ESP-D5.02 [ESP_SUPPER = cooked] HENNET: "Your stew. Three crews ate it and nobody came back to complain. That's a review."
ESP-D5.03 [ESP_SUPPER = hatch] HENNET: "You worked my hatch a whole turn and only dropped one bowl. The stew's mine, the feet were yours."
ESP-D5.04 [ESP_CALL_HEARD] HENNET: "Did they knock? On the stair? Good. They used to knock for me."
ESP-D5.05 HENNET: (coin, under the bowl) "Hearth's yours when I'm not on it. You know the stew now. Pails, lids, salt last."
      {small payment; event: ESP-D5 end → quest Completed}
```

**Inspect texts**

| Id | Object | Text | Condition |
|---|---|---|---|
| ESP-I1 | Shift supper list | "*SUPPER: Stair (wardens), 3. Slag carts, 4. Forge night gate, 2.* Under it, older chalk, rubbed: *carried by T.*" | — |
| ESP-I2 | Hood tell | "Amber. Working. A cooking heat." | `EH_TELLS` |
| ESP-I4 | Packed crate | "Three lidded pails bedded in straw and warm stones. The straw smells of rib." | — |

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| HENNET | "Supper list's carried tonight. Somebody's feet." | ESP Completed |

### ESP.13 Open decisions

1. **The hatch boy's chalk initial "T."** is a role detail only; he is not named.
2. **Cooking `[GD: entry]`:** EH-M6 `S01` asks Cooking ~[GD: mid] for the same recipe; ESP is the low rung.

### ESP.14 Review log

| Finding | Revision |
|---|---|
| A cooling timer on the pails would add a meter. | No timer: the stones are the craft, not a clock. |
| Distinct from EFC and EH-M6 `S01`. | EFC is one ward pot read by the hearth tell; EH-M6 cooks three pails in a frost; ESP teaches the recipe and the packing and carries it to people who cannot leave their posts. |
| A draft line dated the stew to "the night the war stopped". | Cut: it pointed at the night R09 owns. Hennet now dates it to his own childhood. |
| The supper call as a phenomenon. | It is people knocking on pipes; no tell changes, nothing glows. |

---
---

## ESH — Soot and Hide

### ESH.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `emberholt.side.soot_and_hide` |
| Type | Skill intro (Leatherworking). Standalone (bible §7.2). |
| Unlock | EH-M1 Completed. Offered by Brisa Teglan at her tannery in the Cinderweave Quarter (`ESH-D1`); Veska's bark at the Undercroft stair head points there (`ESH-B0.1`). |
| Resume hook | Brisa at the frames: `ESH-D1.00` "Hide's still on the frame. Not getting younger." pins the step. |
| Skills | Leatherworking ~[GD: entry; taught from any level] (hook; alternative: keep watch until morning while Brisa cuts and stitches). No combat. |
| Combat share | 0% |
| Cameo | Veska Dunmor; Lenk Doak, a new line hand on her crew [NEW] |
| Choice | None (contract) |
| Unlocks | The tannery's bench and horse as a public Leatherworking station; heat gloves and a duct hood for the player (EWS-13) |
| **Anchor** (§7.1) | Cinderweave artisans (the tanneries) |
| **World-truth row** | H23 (recovery: the craft that keeps the city's line hands whole) |
| **Revelation role** | None (self-contained). |
| **Recurring evidence** | None. |
| **State compliance** | Inactive / Active / Completed. No fail path: a bad hide is set back, a red bed refuses the hide, the palm test always passes on gear made in the quest; the Leatherworking hook has an overnight alternative. |
| **Combat compliance** | No combat. Solo test (CDR-6): one player makes, dresses and fits alone; Lenk is an NPC; a partner's stitching never completes the player's step. |

**In one paragraph.** Veska's newest line hand, **Lenk Doak**, came off his first duct shift with a scorched neck because the crew's spare hood had worn through at the cape. **Brisa Teglan** makes the wardens' gear and is three orders behind, so she teaches the warden's hand to make it: pick a hide that has been softened right on the ember bed (not the stiff one, not the one somebody left too long), cut heat gloves with the palms doubled, stitch them tight, and hold a gloved hand over the yard's test vent through one exhale. Then a duct hood: crown, cheek flaps, a cape over the shoulders, stitched tighter, and dressed in the soot loft with soot scraped from the flue and worked into tallow, so sparks roll off it. In the loft the sparks do exactly that. The player takes the hood and gloves to Lenk at the Undercroft stair and walks him down the Working duct to the first junction, where Veska looks at his neck, then at the hood, and says one word.

### ESH.2 Selection record and canon grounding

| Element | Source | Status |
|---|---|---|
| Cinderweave Quarter: weavers, glasswrights, tannery workers; embercraft used to soften hides | Dossier §VII.2 | [CANON] |
| Brisa Teglan: "Hide first, heat second."; her tannery, frames over a low ember bed, cutting bench, patterns on pegs, stitching horse; "Amber all day. Softens the hide." | Bible §5.2; Act I C1, `EEH-D4.01`, `EEH-D4.12` | [NEW], consistent |
| Heat gear "in the *Soot and Hide* family": recommended, never required (EH-M3 `S03`; EH-M4 duct hood) | Act I; Act II | [NEW], made true here |
| Tells, vent breath, cooling niches; the Undercroft stair and its niche | Bible §1.1; Act I W3, U1 | [NEW], consistent |
| Lenk Doak; the palm test; the soot loft and dressing; the rolling sparks | This package | [NEW] |

### ESH.3 The places [MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **H1. The tannery yard** (Act I C1) | Offer; hides | Hides on frames over a low **ember bed** with a tell in its kerb. Brisa's sign: *HIDE FIRST, HEAT SECOND.* Three hides on the near frames. | — |
| **H2. The bench and horse** | Cut; stitch | The cutting bench, patterns on pegs (gloves, hood), the stitching horse, waxed thread. | — |
| **H3. The test vent** | Palm test | A small hooded vent in the yard wall that breathes (~10 s), with a scorched iron ring where hands have been held. | — |
| **H4. The soot loft** | Dressing | A loft over the tannery's flue, reached by a ladder: hot, dim, a shaft of light from a roof slit, soot thick on the flue's brick, a tallow pot on a hook. A water bucket by the hatch (a cooling niche in all but name; the loft is a pinned **Working** heat zone, light periodic damage away from the bucket). The flue throws **sparks** on the flue's breath. | Ladder |
| **H5. The Undercroft stair and first duct** (Act I W3, U1–U2) | Fitting; the walk | As Act I: the stair head, the niche, the duct run pinned **Working** with breathing grates, to the first junction. | Stair |

### ESH.4 Beats

**Beat 0: The Order (`S00_offer`).** *Objective: Talk to the tanner.* At the Undercroft stair head, Veska (`ESH-B0.1`): "Doak's neck's cooked. Brisa's behind. Go and be in front." At the tannery, Brisa (`ESH-D1`). With `EEH_MITTS = self`: "Your shells held. Vall's lining helped." (`ESH-D1.10`).

**Beat 1: The Hide (`S01_hide`).** *Objective: Choose a hide fit to cut.* **Inspect** the three hides on the frames (`ESH-I1` to `ESH-I3`): one stiff (not softened), one thin with a glossy scorch (left on a red bed), one supple and even. **Choose** the good one (one interaction). Choosing a bad one: Brisa sets it back (`ESH-B1.2`), nothing lost. **Soften** it a last time on the bed (one interaction, ~4 s) while the bed's tell is **amber** (pinned; the bed is never red in this step).

**Beat 2: Gloves (`S02_gloves`).** *Objective: Make a pair of heat gloves.* Two ways, both complete Beats 2 and 3 together:

- **Option A (skill): make them** (**Leatherworking ~[GD: entry]**). At the bench (H2): **cut** palms (twice, doubled), backs and cuffs on the glove pattern (one interaction); **stitch** on the horse (a 2-segment channel; Brisa: "Tight. Tighter."). **Palm test** at the test vent (H3): hold a gloved hand in the iron ring through one exhale (a held interaction; ash lifts ~1.5 s, then the exhale). The gloves made here always pass: the player takes no damage and feels warmth, not heat (`ESH-I5`). Holding a **bare** hand in the ring is allowed and scalds (small damage; Brisa: "That's why we make gloves." `ESH-B2.3`). `ESH_SET = self` is set at the end of Beat 3.
- **Option B (time-cost): Brisa cuts and stitches.** The player **keeps watch** at the tannery bench until morning (one turn); Brisa has cut and stitched gloves and a hood. The player still does the **palm test** (Beat 2) and the **dressing** and **fitting** (Beats 3 and 4), which need no skill. `ESH_SET = brisa`. Lower Leatherworking XP.

**Beat 3: The Hood (`S03_hood`).** *Objective: Make and dress a duct hood.* Option A: **cut** crown, two cheek flaps and a cape on the hood pattern (one interaction) and **stitch** (a 3-segment channel). Then up the ladder to the **soot loft** (H4; Working heat away from the bucket; touch water at the bucket, Veska's rule, bark if skipped): **scrape** soot from the flue brick (one interaction), **work** it into tallow in the pot (one interaction), **dress** the hood's cape and crown (a 2-segment channel) in the light from the roof slit. On the second segment, the flue breathes and **the sparks roll (ESH.5)**. Sets `ESH_SET`.

**Beat 4: The Fitting (`S04_fit`).** *Objective: Fit the hood on Lenk in a Working duct.* Carry the set (carry-state) to the Undercroft stair head (H5). **Fit** the hood on Lenk (a 2-segment channel: lace the cheek flaps, settle the cape; `ESH-D4`) and give him the gloves (one interaction). **Walk the duct** with him to the first junction (U2, pinned Working; floor grates breathing ~10 s; touch water at the niche). Lenk walks ahead, talking. At the junction, Veska looks at the hood (`ESH-D4.20`). The step completes on `ESH-D4.21`.

**Beat 5: Back to Brisa (`S05_return`).** *Objective: Tell Brisa it fitted.* At the tannery, Brisa (`ESH-D5`) hands the player a second set she cut "on the same hide while you were in the loft" (EWS-13; heat gloves and duct hood), pays, and opens her bench and horse. Quest Completed.

### ESH.5 The sparks roll (presentation spec: wonder)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Breath** | In the loft, the flue breathes out. A drift of sparks rises from the brick into the shaft of light. |
| 1–3 s | **Fall** | The sparks come down on the bench and the dressed hood. On the bare wood they lie and smoke. On the soot-and-tallow cape they **roll**, bead and skitter off the edge like water off oilcloth, and go out on the floor. |
| 3–5 s | **Look** | One spark sits on the crown a moment, rolls, and drops. The leather is unmarked. |
| After | **Brisa** (from below) | "Rolling, are they? Good. That's the soot doing the work. Hide first, heat second, soot third." |
| Meaning | Craft. Proves nothing. |

### ESH.6 Encounters and hazards

No enemies. Hazards: the test vent's exhale on a bare hand (small damage); the soot loft's Working heat (light periodic damage away from the bucket); the duct grates' exhale (as Act I). No step requires taking damage.

### ESH.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to the tanner. | `ESH-D1` accept | Yes | `ESH-D1.10` with `EEH_MITTS = self` |
| `S01_hide` | Choose a hide fit to cut. | Three hide inspects + good hide chosen + softened at amber | Yes | Bad hide set back |
| `S02_gloves` | Make a pair of heat gloves. | Option A: cut + stitch; **or** Option B: keep watch to morning; then palm test | Yes | — |
| `S03_hood` | Make and dress a duct hood. | (Option A: cut + stitch) + scrape + work + dress (2 segments) | Yes | Loft pinned Working. Sparks moment. Sets `ESH_SET` |
| `S04_fit` | Fit the hood on Lenk in a Working duct. | Fit channel + gloves given + reach the first junction + `ESH-D4.21` end | Yes | Duct pinned Working |
| `S05_return` | Tell Brisa it fitted. | `ESH-D5` end | Yes | Gear reward; small payment; quest Completed (read by EH-M6 §E.10) |

| Flag | Set by | Read by |
|---|---|---|
| `ESH_SET` = self / brisa | `S03` | `ESH-D5.02` |

### ESH.8 Choices and consequences

None (contract).

### ESH.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| Heat gloves and a duct hood | Gear (EWS-13) | Item pass defines protection. Act I EH-M3 `S03` recommends heat gear for the drain's heat rooms; never required. |
| Small payment | Currency | Brisa's ([GD]). |
| The tannery | Access | Public Leatherworking station (bench and horse). |
| Leatherworking XP | Action XP only [GD] | Lower on Option B. No lump quest XP. |

### ESH.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Chooses a bad hide | Set back; choose again. |
| Bare hand in the test vent | Small scald; allowed; nothing resets. |
| Will not or cannot do Leatherworking | Option B: one keep-watch turn; the dressing and fitting need no skill. |
| Death | Respawn at the tannery yard (`S00`–`S03`, `S05`) or the stair niche (`S04`); progress kept; the set returns to the tannery bench if dropped. |
| Logout | Restore to the step as above. |
| Walking away | Stays Active; resume hooks at Brisa (`ESH-D1.00`) or Lenk at the stair head (`ESH-B4.4` "Is that my hood? Tell me that's my hood."). |
| Co-op | Per-player hides, gear, loft dressing and fitting; Lenk is fitted with each player's own hood in that player's state. A partner's stitching never completes the player's step. Any shared Lenk presentation is presentation only (CDR-6). |

### ESH.11 Integration needs

All standard: hide inspects with a choose interaction; a soften interaction at the bed (amber pinned); Leatherworking cut and stitch channels at an existing bench and horse; a held palm-test interaction on a timed vent; a pinned Working heat zone in the loft with a water-bucket safe volume; scrape, work and dress interactions; the rolling-sparks VFX on the second dressing segment (presentation only); a carry-state gear set; a fit channel on an NPC; an NPC follow along the Act I duct run; a gear reward (item pass).

### ESH.12 Dialogue

**Cast notes**

| Character | Knows | Voice |
|---|---|---|
| **Brisa Teglan** [NEW, bible §5.2], tanner | Every hide in the quarter; what wardens wear out first. | Blunt. "Hide first, heat second." Never looks up from the work while she talks. Calls the player "warden's hand". |
| **Lenk Doak** [NEW], new line hand on Veska's crew | His first shift; his neck. | Young, eager, talks in the duct to keep his nerve. |
| **Veska Dunmor** [NEW, bible §5.2] | Her crew. | As Act I. |

**Offer** (`ESH-D1`)

```
ESH-D1.00 [quest Active, returning] BRISA: "Hide's still on the frame. Not getting younger."   (pins step) → end
ESH-D1.01 BRISA: (not looking up from a frame) "Hide first, heat second."
ESH-D1.10 [EEH_MITTS = self] BRISA: "Your shells held. Vall's lining helped." (beat) "You can stitch. Good. I'm three orders behind."
ESH-D1.02 BRISA: "Dunmor's new boy cooked his neck in a duct. The crew's spare hood went at the cape. I can't make him one before next week. You can."
  > "Show me."                                                        → ESH-D1.03
  > "Why's it always the cape?"                                       → ESH-D1.04
  > "Not now."                                                        → ESH-D1.05
ESH-D1.03 BRISA: "Gloves first. You learn on gloves. Then a hood. Pick me a hide off the frames. Not the stiff one. Not the shiny one."   {event: accept → S01_hide}
ESH-D1.04 BRISA: "Because they bend their heads to read the tells, and the grates breathe up their backs." (beat) "Read with your eyes, I tell them. They don't listen."   → ESH-D1 options
ESH-D1.05 BRISA: "His neck'll keep. Badly."   → end
```

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| ESH-B0.1 | Undercroft stair head after EH-M1 | VESKA | "Doak's neck's cooked. Brisa's behind. Go and be in front." |
| ESH-B1.2 | A bad hide chosen | BRISA | "That one? Feel it again. No. Back it goes." |
| ESH-B2.3 | Bare hand in the test vent | BRISA | "That's why we make gloves." |
| ESH-B2.4 | Palm test passed | BRISA | "Warm, not hot? Then it's a glove." |
| ESH-B3.1 | Loft entered without touching water | BRISA (from below) | "Bucket by the hatch! Dunmor's rule, mine too!" |
| ESH-B4.4 | Lenk at the stair head, quest Active | LENK | "Is that my hood? Tell me that's my hood." |

**The fitting** (`ESH-D4`)

```
ESH-D4.01 LENK: (at the stair head, a cloth wrapped round his neck) "Brisa sent you? Or you're Brisa now? Either's fine."
ESH-D4.02 LENK: (the hood goes on; the player laces the cheek flaps) "It smells like a chimney." (beat) "In a good way."
ESH-D4.10 (Walking the duct.) LENK: "Amber. That's amber. Light damage, touch water at the next niche. I know. I know. I'm saying it so I know."
ESH-D4.11 LENK: (a grate breathes behind him; the cape takes it) "Oh. Oh, that's nothing. That's nothing!"
ESH-D4.20 (First junction.) VESKA: (looks at Lenk's neck, then at the hood, a long look) "Good."
ESH-D4.21 LENK: (when Veska has gone back to the slate) "She said good. To a hood. I'm going to remember that."   → end
```

**Back to Brisa** (`ESH-D5`)

```
ESH-D5.01 BRISA: "Fitted? Walked? Dunmor said a word?" (beat) "Which word?" (the player tells her) "Huh. She said that to me once. About a boot."
ESH-D5.02 [ESH_SET = self] BRISA: "Your stitching's in that hood. It'll hold. I cut you a set on the same hide while you were in the loft. Yours." 
ESH-D5.03 [ESH_SET = brisa] BRISA: "My stitching, your soot. It'll hold. There's a set on the bench for you too."
ESH-D5.04 BRISA: (coin) "Bench and horse are yours when I'm not on them. Hide first, heat second, soot third."
      {gear reward (EWS-13); small payment; event: ESH-D5 end → quest Completed}
```

**Inspect texts**

| Id | Object | Text | Condition |
|---|---|---|---|
| ESH-I1 | Stiff hide | "Stiff at the edges, pale. Not softened enough. It would crack at the first fold." | — |
| ESH-I2 | Shiny hide | "Thin, with a glossy patch the size of a hand. Left too long on a red bed." | — |
| ESH-I3 | Good hide | "Supple, even, warm right through. Softened on an amber bed." | — |
| ESH-I5 | Gloved hand in the ring | "The exhale comes up through the ring. Warm on the palm. Not hot." | — |
| ESH-I6 | Dressed hood | "Black and dull, a little greasy. A spark would not stay on it." | — |

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| LENK (Undercroft) | "Still got my neck. Still got my hood." | ESH Completed |

### ESH.13 Open decisions

1. **Lenk Doak [NEW]:** grepped with no collision. A named line hand is new to Veska's crew; if the Director prefers role names, he becomes "the new line hand" and nothing else changes.
2. **Gear protection** is the item pass's; Act I's "halves the rooms' periodic damage" (EH-M3 `S03`) is that package's figure and is flagged here for the item pass rather than set.
3. **Leatherworking `[GD: entry]`:** Gameplay Designer to set; Act III's frost coat is the higher rung.

### ESH.14 Review log

| Finding | Revision |
|---|---|
| Distinct from EH-M2's mitts. | EH-M2 makes children's mitt shells that Maeryn lines; ESH makes adult heat gear and teaches hide choice, the palm test and soot dressing. |
| A palm test that could fail. | It always passes on gear made in the quest; the bare-hand scald is optional and teaches why. |
| Soot dressing as a new mechanic. | Three ordinary crafting interactions; the sparks are presentation only. |

---
---

## File review log

| Pass | Result |
|---|---|
| Authoring check (2026-11-15) | Six packages against bible §7.1–7.3 rows (codes, titles, unlocks, places, cast, families, contracts), §9.1 (`EH_GUILDS` only region flag set), §10, §11; against Acts I–III for every read (`ECW_SEAT_RING`, `EEH_MITTS`, `EGH_FLARECAP`) and every promise (EFS, ESP, ESH and EWQ Completed lines; `EH_GUILDS` reformed / restored meanings, including the relief seat and "by order only, billed"). Every enemy to 0 HP; no SX; ranged first-class and never required (EWQ has a spotting path); every step solo with NPC second hands; no quest items; no Remnant, Deepbrand, "below", tally-board, `[ALLOCATION]`, D-E2, D-S1 or ED-3 (Iven Calder; all three ruled 2026-11-15) dependency; no Volkhari person; no route or direction to another region; no R15 pass wording. |
| Collision grep | New names and ids grepped across `04_CONTENT_PRODUCTION`, `LORE` and `00_ADMIN`: Quint Saddick, Ruel Kessick, the Whitehearth Forge, Lenk Doak, `ESK_`/`EOM_`/`EFS_`/`EWQ_`/`ESP_`/`ESH_` flags and `-D`/`-B`/`-I`/`-E` ids, `EWS-` labels: no collision. Avoided on grep: Halse (near Lowmark Hale), Arne and other crew names (cut; the crew stays unnamed but for Kessick). |
| Fixes made in the pass | A draft Hennet line dated the stew to "the night the war stopped" (cut, R09 is EH-M3's); Ryl's "before the passes close" (cut, echoes the R15 phrase); EOM's Captain naming his crew at low health (cut, CDR-1; the ledger and Durnan carry it); the Lowmark line given to the player rather than to Durnan (Part 4 ledger); a mining joke that blurred ESK's "dull ring" (cut). |
| Independent review, 2026-11-15 | Read against CDR-1 to CDR-6 (§3.7), the bible, Acts I to III and dialogue, the sibling Combat and Discovery file, the dossier, the character file and the Part 4 ledger (nothing was played). Every read verified as named and set where claimed: `ECW_SEAT_RING` (`ECW-D7.12`/`.30`), `EEH_MITTS`, `EGH_FLARECAP` (EH-M3 `S02`, `EGH-I3`), `HS_SALVAGE_*` (Lowmark HS, flavour only); completion lines match Acts I/III (`EGH-D4.12` for EFS, `EGA-D2.05` for ESP, `EGA-D14.21`/`.31` for ESH/EWQ, `EGA-D14.02`/`.03` and `EGA-I15`, `EGA-D13.42`/`.43`, `EGA-B10.14`/`.15` for `EH_GUILDS`, one writer). Fixes: EFS logout restored `S01`–`S02` to R1 rather than the stope; the Darven quote and id corrected in §0.7; ESK.13 no longer offers giving Durnan Lowmark knowledge; displacing telegraphs in EOM-E1 and EWQ-E1 raised to ~1.5 s to match the sibling file and Act III's C-1 requirement; D-C06 wording on Maeryn clarified. New names (Quint Saddick, Ruel Kessick, Whitehearth Forge, Lenk Doak) re-grepped across `04_CONTENT_PRODUCTION`, `LORE`, `00_ADMIN`: no collision. Saboteur Captain solo-tuned; no unreachable safe spot (both rim-ledge ramps open). |
| Batch 4 encounter alignment review, 2026-11-15 | Applied Enemies file PE-11 (EFS-E1 crawler Butt and beetle burst 1.5 s), PE-12 (wrecker Bar Sweep 1.0 s; thrower Coal Pot 1.2 s), PE-13 (Captain Close 1.5 s) and PE-14 (EWQ-E1 tusker Gore has no displacement, the family kit). Telegraph minimums are authored tuning pending the Gameplay Designer, not approved rules. No id, step, flag or line changed. |
| Emberholt character rulings, 2026-11-15 | Reserved-decision notes (§0, review summary) updated: D-E2, D-S1 and ED-3 ruled; `[INITIATE]` placeholder replaced by Iven Calder (not used in any node). No node, flag or line changed; no Thalan, Speaker-knowledge or Elyndra content here. |
| Playability audit fixes, 2026-11-15 | Playability audit fixes, 2026-11-15: ES-01, ES-03 (EWQ crossbow as lent tool). |
