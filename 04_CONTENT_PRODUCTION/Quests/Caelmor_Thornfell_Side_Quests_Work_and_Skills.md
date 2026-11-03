# Thornfell Side Quests — Work and Skills

**Status (2026-11-02):** Authored production content for Creative Director review (Thornfell bible §12, batch 3). Five skill-introduction and work side quests from `Caelmor_Thornfell_Narrative_Production_Bible.md` §7.2: **TSR** *Seam Rights*, **TST** *Stormwood*, **TGY** *Goat Year*, **TFS** *First Smoke*, **TBC** *The Bridge That Chose*. Everything here is **[NEW]** unless marked **[CANON]** or **[APPROVED — id]**. Consequential choices the content depends on are marked **[PROPOSAL — DIRECTOR]**. Markdown only: no schema, JSON or C#. Dialogue sits inline in each package, as in `Caelmor_Lowmark_Side_Quests_Work_and_Skills.md`, in the node format of `Dialogue & Narrative/Caelmor_Lowmark_Main_Act_I_Dialogue.md` and the Thornfell voice rules (bible §5.3).

**Sources used:** the Thornfell bible (binding: §1.1 sound system, §3 TD-4/TD-7/TD-12/TD-13, §4 POIs TP03/TP06/TP07/TP21/TP24/TP28, §5 cast, §7.2 briefs, §9 flags and calls, §10 families, §11 conventions); `LORE/Regions/Caelmor_Region2_ThornfellMarches.md` (cliff goats that ram travellers, snowhares that vanish in drifts, goatwillow, crag pines, the legacy resource list in §XI); `00_ADMIN/Reference/Caelmor_Part3_Thornfell_Proposal.md` (Red Slope Terraces, Nettlehook, First Smoke Evening and the "third call too late" verse, crews in threes); `00_ADMIN/Reference/Caelmor_Regional_Source_Process_Thornfell_Proposal.md` (fuel stewardship, herding households, makers who refuse unsafe hides); `00_ADMIN/Reference/Caelmor_Part4_Cross_Region_Historical_Relationship_Web.md` braid 2 (a repair credited twice); `00_ADMIN/Reference/Caelmor_Part4_Character_Family_Continuity_Ledger.md` (Thornfell rows); `Caelmor_Narrative_Architecture_Review_and_Authoring_Sequence.md` §7.1 (the contribution contract); `DESIGNS/Economy Design/` (the approved material set, the economy content integration rules, S01 ranged deferral); `Caelmor_Lowmark_Side_Quests_Settlements_and_Combat.md` NB *Night Bridge* (for the optional Lowmark callback only); `Caelmor_Thornfell_Side_Quests_Horn_and_Highsteads.md` (sister package: names, wonder moments and distinctness, so nothing here repeats it).

---

## 0. Purpose and shared rules

These five quests are where a player first learns what a Thornfell skill is *for*. Lowmark taught skills as custody handoffs on a river. Thornfell teaches them as **listening work in a hard place**: every skill here is learned through Thornfell's readable system, sound (bible §1.1). The miner counts an echo to tell a grave from a seam. The bowyer picks the stems that stay silent in a gust. The herder moves goats with the Ordinary Calls. The cook times a smoke-flap to the whistle of the gust. The smith hammers until the iron stops singing.

Exact items, recipes, yields, stats, levels and XP belong to the item, economy and balance passes. **Ridge iron, stormwood and goat leather are dossier legacy concepts, not approved catalog items** (bible TD-13; dossier §XI status note). This file therefore names every output by what it does and lists every material and recipe as an **economy-pass dependency** (§0.3). No step consumes or rewards a named material item that the economy pass has not derived.

### 0.1 Unlock gates and placement

| Code | Quest | Skill introduced | Core verb (primary first) | Unlock (quest state) | Where (bible §4) | Length |
|---|---|---|---|---|---|---|
| **TSR** | Seam Rights | Mining | **prospect**, mine, judge | TF-M1 Completed | Red Slope Terraces (TP21), Stormwake shoulder | 30–40 min |
| **TST** | Stormwood | Woodcutting, Fletching (bow-stave work); Ranged only if S01 is ruled in | **select**, cut, tiller | TF-M1 Completed | Stonewake ridge-market (TP01); Burned Slope (TP24), Ridgewall | 35–45 min |
| **TGY** | Goat Year | Hunting, Leatherworking | **track**, cull or drive, tan | TF-M1 Completed (needs `TH_CALLS`, always set by TF-M1) | Goat Ledges of the Stormwake Shoulder (TP28) and a herding shieling at their foot | 35–45 min |
| **TFS** | First Smoke | Cooking (with entry Hunting) | **hunt**, cook, tell | TF-M2 Completed (`TH_SEASON` = snow) | Nettlehook Highstead (TP03), the upper longhouse and the snow shelf above it | 30–40 min |
| **TBC** | The Bridge That Chose | Smithing (settlement) | **triage**, smith, account | TF-M1 Completed | The Windscar Narrows (TP07): Passwatch-side bridgehead and Aud's field forge; Three Calls Shelter (TP06) across the gap | 35–45 min |

All five are optional, solo-clearable, cannot fail, and give no lump quest XP (skill XP comes from the actions; bible §11.5). They are Inactive, Active or Completed only. Co-op partners run independent instances against shared world creatures. **No quest items** (bible §9.5): every object is a carry-state prop, a station object, an inspect point, or an ordinary output the economy pass will define.

Level framing (TD-12): TSR, TST, TGY and TBC sit at TF-M1's Competent identity; TFS at TF-M2's. Exact levels are Gameplay Designer calls. **No skill step anywhere in this file checks a skill level.** Each has a crew or alternative path (§0.6).

### 0.2 Skill coverage and how the five feed one another

```text
TSR  Mining: echo-sound (prospecting) ──► open a face (wedge, pick) ──► seam ore [EC-01]
                                          └──► the seam rota (who mines it, from when)
TST  Woodcutting: select by ear in a gust ──► stool-cut one stem ──► wind-tested stave billet [EC-04] + ordinary wood
     Fletching: split, rough out, tiller ──► an unstrung stave racked at Brita's stall (default, TST.15)
     [PROPOSAL — DIRECTOR, gated on S01] string [EC-06] ──► fletch [EC-07, EC-08] ──► first bow [EC-05]; Ranged at the wind butts
TGY  Hunting: read herd sign ──► watch ──► cull (approach, resolve, field dress) or drive (calls + echo)
                 └─ cull ──► ram hide [EC-09] + meat (food relationship)
     Leatherworking: flesh, light-test, work, smoke ──► goat-leather piece [EC-10] ──► ledge-grip wraps [EC-11]
TFS  Hunting (entry): snowhare tracks, snare or still-approach, recover ──► hare (food relationship) [EC-12]
     Cooking: smoke-flap to the wind window, stew by the lid's sound ──► hot food now  or  smoke-cure ──► stored food [EC-13]
TBC  Smithing: read the break ──► forge by ear (sing / clack) ──► bridge fittings [EC-02, EC-03] ──► set them in sound rock
     (TSR's seam ore and TBC's bar stock are linked only by the economy pass: TBC never requires TSR)
```

- **Mining** is prospecting first. Tapping and counting is the skill; the pick comes after the ear (TSR). TF-M3 reuses the same ear for rope anchors, so a player who did TSR first already knows the shape of a hollow return.
- **Woodcutting** is selection and stewardship: one stem from a stool, cut between gusts, so the stool regrows (TST). Thornfell's fuel and timber are stewarded (Regional Source Process, fuel row: makers may reserve structural timber and protect cover).
- **Fletching** arrives in TST as bow-stave work: the bowyer will not hand over a bow, and the player tillers a stave she racks for them. **S01 is still open** (economy set: "no ranged concept enters v1 while S01 remains open") and initial-release scope may not grow, so TST ships its fallback (TST.15) as the **default**: no bow, no arrows, no Ranged step. Stringing the bow and the wind-butts Ranged lesson are kept as a **[PROPOSAL — DIRECTOR]** layer gated on S01.
- **Hunting** is herd-reading and judgment (TGY) and fresh-snow tracking (TFS). Combat may resolve a dangerous contact but never grants Hunting recovery; field dressing is the recovery phase (economy D02/D03, as Lowmark).
- **Leatherworking** is the player's step inside a herding household's shed that keeps working without the player (TGY; the Lowmark P-O4 pattern).
- **Cooking** is heat and smoke management, and food as recovery or as store (TFS).
- **Smithing** is reading a failure, then forging by ear (TBC). TF-M1 had the player set fittings at Aud's field anvil under a clock; TBC teaches why fittings fail and how to make them, with no clock at all.

### 0.3 Economy-pass dependencies (TD-13)

Every material and recipe below is a **dependency**, not an item. The working name in the right column is what the quest text calls it until the economy pass derives a state. Where a Lowmark-approved state could serve, it is named; otherwise the economy pass must derive one before any item exists.

| Id | Working name in this file | Dossier concept | Used by | Nearest approved state | What the economy pass must decide |
|---|---|---|---|---|---|
| **EC-01** | **seam ore** (from a ridge seam) | Ridge iron [legacy, not approved] | TSR (output) | None. Lowmark's hard-material rule is imported plain carbon steel stock; there is no approved ore state. | Whether Thornfell has a mined ore state at all; its processing (smelting labour, fuel); whether it becomes plain carbon steel stock or a separate state. Until then, TSR's ore goes to the seam rota's store and the player's share is paid in coin (TSR.9). |
| **EC-02** | **bar stock** (for fittings) | Ridge iron or imported steel | TBC (input) | **Plain carbon steel stock** (approved Lowmark chain state) | Whether Thornfell fittings use approved steel stock (recommended for v1.5 parity) or a derived ridge-iron state. TBC is written to work with either: Aud supplies the stock. |
| **EC-03** | **bridge fittings** (eye-bolts, shackles, anchor pins) | — | TBC (recipe output, installed at once) | None | Recipe definition. Fittings are installed into the bridge (a world-state change), so no inventory item is required for the quest. |
| **EC-04** | **wind-tested stave billet** | Stormwood [legacy, not approved] | TST (output, then input) | Ordinary wood (approved provisional state) for the trimmings only | Whether a bow-stave wood state exists; how it differs from ordinary wood; seasoning (TST compresses seasoning with Brita's swap, TST.4). |
| **EC-05** | **first bow** ("bowyer's first stave", bible §11.5 functional name) | — | TST (reward) | None. **S01 open.** | Ranged scope (S01) and the bow recipe. Fallback in TST.15. |
| **EC-06** | **bowstring** | — | TST (input from Brita's stock) | Flax linen and tow are approved Lowmark states; gut or sinew is not | String material for Thornfell (imported flax thread, goat gut, sinew). |
| **EC-07** | **arrow shafts** | Goatwillow (dossier flora: "wood used for bows and light tools") | TST (input from Brita's stock) | Ordinary wood | Shaft wood state, or ordinary wood with a recipe. |
| **EC-08** | **fletchings and arrowheads** | — | TST (input from Brita's stock) | None | Feather source (no approved feather output; Lowmark F3 is food-only) and head metal. |
| **EC-09** | **goat hide** (the old ram's hide, or a herder's stock hide) | Goat leather and wool [legacy, not approved] | TGY (output and input) | **Raw hide** (approved Lowmark state) | Whether goat hide is raw hide or its own state. TGY accepts either. |
| **EC-10** | **goat-leather piece** | Goat leather [legacy, not approved] | TGY (craft output) | **Vegetable-tanned leather** (approved) | Thornfell's tanning medium. Lowmark's is tannin-rich bark; Thornfell's is unselected (Bera's tub is described by what it does, not what is in it). Smoke-finishing as a step. |
| **EC-11** | **ledge-grip wraps** | — | TGY (reward, made by the player) | None | Recipe and function (frost grip on ledge paths). A cosmetic or traversal-comfort piece is the minimum; no stat is assumed. |
| **EC-12** | **snowhare** (food relationship) | Snowhares (dossier fauna) | TFS (output, input) | Edible Hunting output is a functional relationship pending its catalog (economy integration) | Food relationship only. **No pelt output** in TFS (as Lowmark F3 fowl). |
| **EC-13** | **hare stew** / **smoked hare** | — | TFS (craft outputs) | None | Two Cooking outputs: an eat-now recovery food and a preserved store food. Barley, roots and salt come from the host's store (Lowmark staple dependency, no route stated: FT-03). |
| **EC-14** | **fuel** (charcoal or dry wood for the field forge; longhouse firewood) | — | TBC, TFS | Wood charcoal; ordinary wood | Thornfell fuel stewardship (Regional Source Process: fuel row). The quests supply their own fuel from NPC stock. |

**Recipe dependencies** (all owned by the item and economy passes): seam-face extraction (TSR); stave roughing, tillering, stringing, fletching (TST); fleshing, tanning, working, smoke-finishing, wrap cutting and stitching (TGY); stew and smoke-cure (TFS); eye-bolt, shackle and anchor-pin forging (TBC).

### 0.4 Commission givers established

Lowmark ended BP and HS by establishing Kell and Brigid as future commission givers. These five do the same for Thornfell. The **master commissions** themselves are not designed here; `TH_STANDING` (TF-M5) gates them (bible §1 "Mastery").

| Giver | Craft | Established by | Flag | What they say they will one day ask for |
|---|---|---|---|---|
| **Aud Hammerlee** [NEW, bible §5.2] | Smithing, bridgework | TBC completion | `TBC_AUD_BENCH` | "A span for the far gate. When there's a far gate worth spanning." |
| **Brita Crane** [NEW] | Fletching, bowyery, Ranged | TST completion | `TST_BRITA_BENCH` | "Horn bows for the Wardens. Proper ones. When you can pick wood blind." |
| **Bera Scree** [NEW] | Leatherworking, herding | TGY completion | `TGY_BERA_SHED` | "Winter harness for a whole herd's carriers. And boots that don't lie about ice." |
| **The Red Slope seam rota** (Dagny Grell and Tormod Lisk) [NEW] | Mining | TSR completion | `TSR_SEAM` (any value) | A deep face at the upper scarp "when there's a crew who can count". |

TFS establishes no commission giver: the Nettlehook longhouse becomes a public Cooking station and its host a standing invitation (§TFS.9).

### 0.5 Distinctness check

| Quest | Core verb | Physical problem | Wonder or unease | Human choice with a cost |
|---|---|---|---|---|
| TSR | prospect, mine, judge | Tap and count rock to tell iron from hollow; follow rust up a scarp; open a face with wedge and pick | **Unease:** one hollow is a grave nobody listed | Who works the new seam, and from when |
| TST | select, cut, string | Pick stems by what they *don't* sound in a gust; cut between gusts; tiller a stave; shoot in wind | **Wonder:** the burned stumps moan in the gust and the old bowyer answers them by habit | Leave the slope's last sound stem to seed, or cut it for the Wardens' winter bows |
| TGY | track, cull or drive, tan | Read a herd; work out why it won't move; cull, or herd with the Ordinary Calls against the echo | **Wonder:** the herd walks a stair of hand-cut steps nobody knew was on the face | Cull the old ram (hide now, leaderless herd) or drive the herd (no hide, hard winter milking) |
| TFS | hunt, cook, tell | Track hares in fresh snow; work a smoke-flap to the wind; stew by sound; tell a story to a room | **Unease:** the children sing "third call too late" and the oldest man at the table gets up and looks out into the dark | The second hare in the pot tonight, or smoked into the tally store |
| TBC | triage, smith, account | Read a sheared fitting; forge by ear; plan three wind windows for four loads on a board everyone can see | **Wonder:** in the lull, snow in the gap falls upward. **Unease:** the old woman reading the board | Who waits for dawn; whether the board names who waited |

None repeats a milestone verb (bible §6: repair-and-escort, track-and-delve, rope-rig, triangulate, whiteout climb) or a sister-package verb (`…_Horn_and_Highsteads.md` §0.7). Wonder moments were checked against that package: no singing cable or span (TNR), no leaning smoke (TSM), no echo at the Narrows (TTH), no chord (TRR).

### 0.6 Shared rules for all five packages

- **Crew or alternative path (every skill step).** Each skill step lists its crew path in its beat text. The crew path is still play: the player does the reading, timing or calling while the crew does the strength work. Choosing it may cost time (a wind window), a share of output, or a coin share. It never costs the quest. Skill XP is lower on a crew path (exact values to the balance pass).
- **The horn.** Calls the player blows use the call interaction taught in TF-M1 (`TH_CALLS`). TF-M1 always gives the player the hornbearer's practice horn (Act I reward tool), and these quests rely on it. Only if it is not carried does Bera lend her herding horn (TGY-D1, carry-state, returned on completion). Calls show their glyph when blown and heard (bible §9.4).
- **Sounding.** TSR and TBC use a **sound the rock** interaction [NEW; shared with TF-M3's rope anchors]: a short strike, the return, and after the return a row of beat-dots on screen (accessibility, using the call-glyph art). Players count; the dots confirm. Never a meter, never a colour code.
- **Wind windows** (bible §9.5): the fluted-face whistle "a fifth before the gust" is the tell; sheltering behind chalk-marked faces is always safe. A gust that catches the player in the open staggers them (small damage, never off a ledge).
- **Agility triggers** are optional shortcuts, each with a walkable fallback named in the place table.
- **Human enemies yield** (TD-7). Animals in TGY and TFS are Hunting fauna that fight only when provoked (bible §10) and are not counted as a family.
- **Evidence rule.** Nothing in these quests is evidence for a revelation. The moments of wonder and unease prove nothing and identify nobody. The unlisted grave in TSR is never named.
- **No failure.** Inactive / Active / Completed only. Death respawns at the quest's named safe point with step and flags intact. Logout restores the last persisted step; completed channel segments persist; a dropped carry-state object returns to its source. Walking away keeps the quest Active with the resume hook named in each package.
- **Season.** TSR, TST, TGY and TBC play in autumn or snow (snow presentation notes where they differ). TFS is always snow.
- **Co-op.** Independent instances; shared world creatures give credit to each participant on that step; quest-state props and NPC placement are per player (Lowmark per-player prop pattern; fallback: the host's state drives props, each player's own state drives dialogue).
- **Lowmark independence.** Only TBC reads Lowmark state, for optional variant lines (TBC.8). No route between the regions is stated anywhere (FT-03; TD-11).

### 0.7 Flags other packages read

All flags here are quest-local (`T??_…`). **No region flag is set by this file.** Region flags read: `TH_CALLS`, `TH_PASSWATCH_ROUTE`, `TH_SEASON`, `TH_STANDING` (commission gate, later).

| Flag | Values | Set by | Read by (request; nothing depends on it) | Effect |
|---|---|---|---|---|
| `TSR_SEAM` | shared / brackenstep / kettlecrag | TSR `S06_judge` | Master commissions (`TH_STANDING`); TF-M3 Gerrit line | Who works the Red Slope seam; Gerrit's crew hired from the thaw on `shared`. |
| `TSR_VOID_MARKED` | bool (always true on completion) | TSR `S07_mark` | *The Weight of a Name* (Maera bark, request); TME10 bark | A plain marker stone for the unlisted grave. |
| `TST_STEM` | seeded / wardens | TST `S04_third_stem` | Passwatch and Ridge Warden barks; Burned Slope opportunity state | Whether the slope's last sound stem was left or cut for the patrol. |
| `TST_BRITA_BENCH` | bool | TST completion | Master commissions | Brita Crane as commission giver. |
| `TGY_WAY` | cull / drive | TGY `S03_choose` | TSM (goat shoulder herd bark, request); Stormwake path barks | Which herd presentation the shoulder path shows. |
| `TGY_STEPS_SEEN` | bool (always true on completion) | TGY strange moment | World route | The goat steps become an agility route (walkable fallback). |
| `TGY_BERA_SHED` | bool | TGY completion | Master commissions | Bera Scree as commission giver. |
| `TFS_HARE` | pot / store | TFS `S04_second_hare` | TSM tally reading (request: one host line); TME01 | Nettlehook's tally line about the player's hare. |
| `TFS_STORY` | boot / goat / drift / narrows | TFS `S05_stories` | Nettlehook barks; TRR (request) | Which ridiculous story the highstead remembers the player by. |
| `TFS_VERSE_ASKED` | asked / sang / left | TFS `S06_verse` | **TTH** (verse variant, already listed in the sister package §0.4); Dorn line (request) | The child's verse as a TTH lead. |
| `TBC_WAITS` | family / mules / sledge | TBC `S04_board` | Three Calls Shelter and Passwatch barks; TRR (request) | Who waited for dawn. |
| `TBC_WAIT_NAMED` | bool | TBC `S07_account` | TF-M5 (request: one Aud line at the Assembly); TTH (request) | Whether the Narrows repair post carries who waited. |
| `TBC_AUD_BENCH` | bool | TBC completion | Master commissions | Aud as commission giver. |
| *(read)* `TH_PASSWATCH_ROUTE` | sledge / caravan / split | TF-M1 | TBC-D1 opening variant | — |
| *(read)* `TH_SEASON` | autumn / snow | TF-M2 | All presentations; TFS unlock | — |
| *(read)* TF-M2, TF-M3 Completed | — | Act I/II | TSR Gerrit variants | — |
| *(read)* `lowmark.side.night_bridge` Completed + `NB_BOTH_CREDIT` / `NB_ALL_PAY` / `NB_WICKETT_CREDIT` | — | Lowmark NB | TBC-D7 optional variant | Repair-credit callback (Part 4 braid 2). No route claim. |

---

## TSR — Seam Rights

### TSR.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `thornfell.side.seam_rights` |
| Type | Skill introduction (Mining). Bible §7.2 brief; Part 3 Red Slope Terraces ("descendants argue over restoring cultivation, preserving graves, and testing slope stability"). |
| Unlock | TF-M1 Completed. Offered at the lower terrace gate of Red Slope Terraces on approach. |
| Resume hook | Dagny Grell at the shrine niche: "Still five on my board. Still a chalk line on my wall." |
| Skills | Mining (required: sounding, opening a face), Melee (light) |
| Combat share | ~10% (one small viper nest on the scarp) plus two readable hazards |
| Cameo | Gerrit Carrick [NEW, bible §5.2]: teaches the tap, offers his crew |
| Choice | Who works the new seam: both highsteads on a rota with Carrick's crew hired, Brackenstep, or Kettlecrag |
| Unlocks | Rock reading by sound; the upper-scarp seam face (Mining opportunity, EC-01 dependent); the seam rota as a future Mining commission giver |
| **Anchor** (§7.1) | The highstead households of the Stormwake shoulder (Kettlecrag and Brackenstep [NEW]) and Carrick's out-of-work miners. |
| **World-truth row** | H16 (the late-war retreat: Red Slope's refuge plots and their graves are its trace). Present pressure: winter scarcity of iron tools (H25 hoarding pressure felt, not explained). No new history asserted. |
| **Revelation role** | Self-contained. Plants nothing. The unlisted grave is a local mystery that stays withheld (TSR.13). |
| **Recurring evidence** | None. Gerrit Carrick recurs as a person in TF-M3; he carries no evidence here, and his TF-M3 role rests on the store ledger and his own testimony, not on this quest. |
| **State compliance** | Inactive / Active / Completed. Choice recorded in `TSR_SEAM`; `TSR_VOID_MARKED` always true on completion. No fail path. A face that sounds hollow cannot be mined: the interaction is unavailable there, so no player can open a grave by mistake. |

**In one paragraph.** Red Slope Terraces are war walls and the small, hasty refuge plots cut behind them when people came over the Stormwake shoulder in the retreat. The plots' back walls hide the old refuge cellars, and the cellars are graves now. Two highsteads want the same ridge-iron seam: Brackenstep's seam-reeve has chalked a cutting line straight along the plot terrace, where the rust stains run thickest, and Kettlecrag's plot-keeper is standing in front of it. Gerrit Carrick's out-of-work miners sit by a fire a little apart, waiting to be hired by whoever wins. Gerrit, who would rather teach than watch someone guess, shows the player how to sound rock: strike, count the return. Flat and quick is barren rock. A bright ring with a buzzing tail is iron. A slow boom that comes back doubled is hollow. The player sounds the chalk line and finds the seam really does run under the cellars. Then, at Dagny's insistence, they sound the whole plot terrace. Her board lists five cellars. The rock gives back six. Nobody knows who is in the sixth. The player follows the rust up the scarp, counting the ring's tail down to nothing, finds where the seam surfaces clear of the dead, and opens the first face with wedge and pick, listening for the moment the slab lets go. Then the two highsteads ask the stranger who counted to say who works it.

### TSR.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| A. Claim-jumpers raid the seam; fight them off. | Rejected. Combat-core side content belongs to TGM and TSG (bible §7.2 structure check). |
| B. A pure arbitration: hear both sides, rule. | Rejected. Talk-led resolution is limited to closing beats. |
| **C. Learn to sound rock → prove the seam runs under the graves → count the graves → find another surfacing by ear → open a face → judge** (selected). | **Selected.** The skill *is* the evidence: the player's own counting moves the argument off the dead. |

| Element | Source | Status |
|---|---|---|
| Red Slope Terraces: war walls, refuge plots, a seam | Part 3 Thornfell proposal; bible TD-4, TP21 | [NEW, Part 3, adopted] |
| Ridge iron "scraped from cliff seams" | Dossier §XI | Legacy concept, **not approved** (TD-13; EC-01) |
| Echo count (fewer beats, nearer face; a wrong return means the face moved) | Bible §1.1 | [NEW] system; TSR extends it to rock |
| Rock Vipers camouflaged against shale | Dossier §IX; bible §10 | [CANON] family |
| Gerrit Carrick, out-of-work miners' foreman | Bible §5.2 | [NEW] |
| Kettlecrag and Brackenstep highsteads | This package | [NEW]; not POIs; named only through their crews |
| Late-war retreat over the passes | H16 [APPROVED — FT-02b] | Used as background only |

### TSR.3 The place [NEW detail on Part 3 place; MAP VERIFICATION REQUIRED]

Red Slope Terraces sit below the Stormwake Plateau's shoulder (TP21). The far bell drill micro-event (TME10) plays in the hollow below them. Kettlecrag lies upslope and Brackenstep downslope (off-map; relative only).

| Area | Purpose | Environmental storytelling |
|---|---|---|
| A. Lower terrace gate | Hook | A gap in a war wall. Two camps: Kettlecrag's (an old woman's stool, a kettle, a shrine lantern) and Brackenstep's (picks, a barrow of wedges, a cracked mattock someone has bound with wire). Carrick's miners' fire apart from both. Rust streaks run down every wall face; in rain (or on snow) the slope looks like it is bleeding. |
| B. The war walls | Teaching | Dry-stone walls with slots facing upslope. Three loose wall stones by Gerrit's fire serve as teaching stones (barren, iron-bearing, a hollow wall-end). |
| C. The plot terrace | The problem | Narrow cut beds, some with a marker stone (a few names, mostly a single cut mark). The terrace back wall has five plank-shut cellar mouths, lintels whitewashed. Brackenstep's chalk line runs along the back wall at waist height. |
| D. The shrine niche | Record | A painted board: the **plot list**. Five cellars, each with a line. Cairn moss on the sill. Dagny keeps the brush and the paint. |
| E. The scarp | Prospecting | Shale fans and slabs above the terraces; rust bands climb it in a broken line. An agility scramble cuts the corner (fallback: the old wall-steps along the terrace ends, longer). Rock Vipers in the shale (E1). Chalk-marked shelter faces against gusts. |
| F. The upper face | Mining | A rust-black outcrop clear of the plots' ground, under a lip of overhang. Room for a crew of three. |

### TSR.4 Beats

**Beat 0 — Two Claims (`S00_dispute`).** *Objective: Find out why the terraces are arguing.* Entering area A opens `TSR-D1`: Tormod Lisk wants to cut along his chalk line before the snow; Dagny Grell will not move off the plot terrace. Gerrit says nothing until asked.

**Beat 1 — Strike and Count (`S01_learn`).** *Objective: Learn to sound the rock.* `TSR-D2`. Gerrit hands the player a sounding hammer if they lack a mining tool. Three **Sound the rock** interactions on the teaching stones (each ~1 s strike, then the return):

| Return | What the player hears | Beat-dots after the return | Reading |
|---|---|---|---|
| **Barren** | One flat knock, gone at once | one dot | Solid rock, nothing in it |
| **Iron** | A bright ring with a buzzing tail | two dots, the second smaller | Iron in the rock; the longer the tail, the further the body |
| **Hollow** | A slow, soft boom, then the same again, fainter | three or more dots, spaced wide | A void behind the face |

Gerrit has the player strike each twice. That is the whole lesson. Mining XP accrues per sounding.

**Beat 2 — The Chalk Line (`S02_chalk_line`).** *Objective: Sound Brackenstep's chalk line.* Five chalk crosses along the plot terrace's back wall. Results in order: iron, iron, hollow, hollow, iron. Each plays a one-line inspect. The two hollows sit behind cellar mouths; the iron runs either side of them and between. Tormod watches the count with his arms folded (`TSR-D3`). The seam runs under the dead.

**Beat 3 — Five on the Board (`S03_count`).** *Objective: Sound the whole plot terrace.* `TSR-D3` ends with Dagny asking the player to sound every cellar, "so we know what we're arguing over". Six chalk-free sounding points along the terrace back (marked by whitewash on the lintels and one bare stretch of wall). The player sounds all six: five hollows behind the five cellar mouths, and a sixth hollow behind a stretch of plain wall with no mouth, no lintel and no line on the board. The strange moment plays on the sixth (TSR.5). Required: all six points and the shrine-board inspect.

**Beat 4 — Follow the Rust (`S04_scarp`).** *Objective: Find where the seam comes up clear of the plots.* Up the scarp along the rust bands: agility scramble or the wall-step fallback. Four **sounding stations** (chalked by Gerrit's crew years ago, worn faint). At each, the ring's tail is shorter: four dots, three, two (vipers here, E1), and at the upper face one bright ring with no tail at all. Wind windows on the scarp: the whistle from the plateau faces is the tell; the shelter faces are chalked. A player who sounds out of order still gets honest readings (it is a hot-and-cold walk, not a sequence lock).

**Beat 5 — Open the Face (`S05_open_face`).** *Objective: Open the first face.* Mining as play, at the upper face:

1. **Score** (one pick channel along the rust line).
2. **Set two wedges** in the score (two short interactions).
3. **Drive and listen.** The player strikes the wedges; between strikes they sound the slab. The return starts flat (still bound). After the third or fourth strike it comes back **doubled** (loose). That is the moment to stop and lever. Levering on a flat return does nothing but cost a breath ("Still holding."). Striking on after the doubled return makes the slab let go on its own (hazard H1: grit trickle and a crack, ~1.5 s; step out of the chalked fall lane).
4. **Lever** the slab off (one channel). Bright ore-stained rock behind it.
5. **Pick** the face (three channels). Output: seam ore (EC-01).

**Crew path:** "Let Carrick's crew swing." Two miners drive the wedges and pick; the player still sounds between strikes and calls **strike** or **hold** (two-option prompt per strike). A wrong call only means one more strike. Cost: the crew's share comes out of the player's payment (TSR.9). Mining XP for the sounding and calls.

**Beat 6 — Who Works It (`S06_judge`).** *Objective: Say who works the new seam.* Back at the plot terrace, both delegations and Gerrit. `TSR-D5`; TSR.8.

**Beat 7 — The Sixth Stone (`S07_mark`).** *Objective: Mark the sixth cellar.* Dagny asks for a plain stone. The player lifts a fallen capstone from the war wall rubble (carry-state), carries it to the sixth hollow and sets it (one channel). Dagny paints a sixth line on the board (`TSR-D6`). Quest Completed.

### TSR.5 The sixth hollow (presentation spec: unease)

| Time | Element | Spec |
|---|---|---|
| 0 s | Strike | The player sounds the sixth point: a stretch of plain wall between the fourth and fifth cellar mouths. |
| 0–3 s | Return | The slow boom, then its double, fainter. Then, under it, a faint dry trickle from inside the wall: earth settling. No music. |
| 3–5 s | Beat-dots | The hollow pattern (wide-spaced dots) draws as usual. Nothing else on screen. |
| 3–7 s | Dagny | Her brush stops on the board. She does not turn round. She counts the board's lines with one finger, out loud, under her breath (`TSR-D4.01`). |
| 7–12 s | The camps | Brackenstep's crew stop talking. Tormod takes his hat off and then looks annoyed with himself for doing it. Gerrit's miners stand up. Ambient wind returns. |
| After | Inspect | Plain wall: *"No mouth, no lintel, no line on the board. The rock behind it is hollow, the size of a person lying down."* |
| UI | No objective update until `TSR-D4` ends. |
| Meaning | None stated. Someone was put in the wall and not written down. The quest never says who or why (TSR.13). Sounding identifies a void, never a person (bible §11.3). |

### TSR.6 Encounters and hazards

Tuned for TF-M1's Competent identity (TD-12).

| Id | Enemies / hazard | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TSR-E1** | 2 × Rock Viper (viper), 1 × Rock Viper (shale-coil) | Shale fan at the third sounding station | Vipers: ambush from shale, leashed to the fan. Shale-coil: holds the station stone | **Viper:** a line of shale shifts toward the player (~1.6 s, first-appearance length), then a strike. **Shale-coil:** a dry rattle of loose stones as it coils (~1.4 s), then a lunge that leaves a short slow on a hit | Required (the station is in the nest). First reading of shale ambushers | 30–45 s; little damage. Stepping onto bare rock off the fan breaks contact |
| **TSR-H1** | Slab drop | Upper face | Environmental | Grit trickles from the slab's top edge and a crack sounds (~1.5 s); the fall lane is chalked on the ground | Teaches that the ear says when to stop | Small damage and a stagger in the lane. Cannot kill a player above a quarter health |
| **TSR-H2** | Scarp gust | Scarp, between stations | Wind window | Fluted-face whistle a fifth before the gust (~3 s) | The universal Thornfell hazard | Stagger and small damage in the open; never off the scarp |

**Rules.**
- **Family note:** bible §10 lists Rock Vipers as first seen in TF-M3. TSR unlocks after TF-M1, so **TSR is the Rock Vipers' first appearance** for any player who takes it before TF-M3. Counts and telegraphs above are tuned for that (longer than the family standard). Flagged to the Encounters package (open decision 2).
- Combat drops nothing that advances the quest.
- **Death:** respawn at Gerrit's fire (area A, or the second sounding station once reached). Stations sounded stay sounded; wedges set stay set.

### TSR.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_dispute` | Find out why the terraces are arguing. | `TSR-D1` end node | Yes | Auto-offered on area A entry |
| `S01_learn` | Learn to sound the rock. | `TSR-D2` end + 3 `sound_rock` interactions on the teaching stones | Yes | Sounding hammer given if no mining tool |
| `S02_chalk_line` | Sound Brackenstep's chalk line. | 5 `sound_rock` interactions at the chalk crosses | Yes | Any order; `TSR-D3` plays after the fifth |
| `S03_count` | Sound the whole plot terrace. | 6 `sound_rock` interactions + shrine-board inspect | Yes | Strange moment on the sixth point; `TSR-D4` |
| `S04_scarp` | Find where the seam comes up clear of the plots. | 4 `sound_rock` interactions at the scarp stations; TSR-E1 defeated | Yes | Hot-and-cold; any order |
| `S05_open_face` | Open the first face. | `score`, 2 × `set_wedge`, `lever` (accepted only after a doubled return), 3 × `pick_face` **or** crew path (`call_strike` sequence + `lever`) | Yes | Sets `TSR_CREW_CUT` on the crew path |
| `S06_judge` | Say who works the new seam. | `TSR-D5` choice node | Yes | Sets `TSR_SEAM` |
| `S07_mark` | Mark the sixth cellar. | Carry-deposit of the capstone at the sixth point + `set_stone` interaction + `TSR-D6` end | Yes | Sets `TSR_VOID_MARKED`; quest Completed |

| Flag | Set by | Read by |
|---|---|---|
| `TSR_CREW_CUT` | `S05` crew path | `TSR-D5` Gerrit line; payment split |
| `TSR_SEAM` = shared / brackenstep / kettlecrag | `TSR-D5` (exactly one) | Post-quest props and barks; TF-M3 Gerrit line (request); master commissions |
| `TSR_VOID_MARKED` | `S07_mark` (always) | TME10 bark; *The Weight of a Name* (Maera bark, request) |

### TSR.8 Choices and consequences

| Option | Immediate result | Cost | Later (props, barks) |
|---|---|---|---|
| **Both, on a rota** (`shared`) — *"Both highsteads, turn about. Hire Carrick's crew to cut it."* | The seam is worked by a hired crew for both highsteads, Kettlecrag's turn first because it is their slope. Gerrit is hired from the thaw. | Both highsteads pay wages out of iron they need, so each has less this winter. Brackenstep patches its tools till spring. | A rota board appears at the lower gate. From the thaw (after TF-M3 Completed, as a stand-in for "the thaw"; Gameplay Designer may choose another state), Carrick's miners work the upper face (prop crew). |
| **Brackenstep works it** (`brackenstep`) — *"Brackenstep needs it before the snow. Kettlecrag keeps the plots and a tithe."* | Tormod's crew start at the upper face this week; Kettlecrag takes a tithe of every load. | Kettlecrag loses its say over the terraces' iron for a generation. Dagny is civil to the player and no warmer. | Brackenstep's barrow of new tools by the gate. Dagny barks about tithes "counted in my sleep". |
| **Kettlecrag works it** (`kettlecrag`) — *"It's Kettlecrag's slope. Kettlecrag cuts, and sells Brackenstep fair."* | Kettlecrag's old crew start slowly; Brackenstep buys what it needs. | Brackenstep pays for iron that comes out of the hill it lives under. Tormod: "So we buy it." Slower working; fewer loads before the snow. | Kettlecrag's crew of three old men and a girl at the face. Tormod buys, loudly. |

**All three:** the chalk line is wiped off the plot terrace; no one cuts under the cellars; the sixth cellar is marked. No option is wrong, and the quest never says which is best. Dagny and Tormod disagree about it afterwards in every outcome.

### TSR.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| **Reading rock** | Knowledge | Authored rock faces across Thornfell become soundable with the same interaction and return one line: *"Solid. Nothing in it."* / *"Iron rings in it. Near."* / *"Iron, but far in."* / *"Hollow. Leave it."* Supports TF-M3's rope-anchor sounding and later Mining placement. |
| Upper-scarp seam face | Access | A Mining opportunity at area F. **EC-01 dependent:** until the economy pass derives an ore state, the face is a station that the seam rota works (props) and the player can sound and assist. |
| Miner's sounding hammer | Tool | Given by Gerrit at `TSR-D2` if the player lacks a mining tool. Item pass defines it. |
| Small payment | Currency | From both delegations; amount at economy tuning. On the crew path, Gerrit's share comes out of it. While EC-01 is open, the player's ore share is paid as coin. |
| Mining, Melee XP | Action XP only | No lump quest XP. |

### TSR.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Death on the scarp | Respawn at the last reached sounding station or Gerrit's fire; stations sounded stay sounded. |
| Player tries to mine a hollow face | The pick interaction is unavailable on any face that has returned a hollow; the prompt reads "Hollow. Not here." |
| Player levers too early or strikes too long | Too early: "Still holding." Too long: the slab drops (H1). Either way the face opens; nothing fails. |
| Player has no mining tool | Sounding hammer at `TSR-D2`; the crew path also covers the cutting. |
| Capstone dropped (logout, death) | Returns to the rubble pile. |
| Walking away | Quest stays Active at its step; resume hook at the shrine niche (Dagny). |
| Logout | Last step restored; sounded points, set wedges and the opened face persist. |
| Co-op | Each player sounds their own points (per-player beat-dots). The sixth-hollow moment plays per player on their own sixth strike. The upper face is a per-player prop state; fallback if per-player props are unavailable: the face is pre-scored for later instances and `S05` begins at the wedges. Each player makes their own `TSR-D5` choice; the rota board prop follows the host. |

### TSR.11 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| **Sound-the-rock interaction** with authored returns | Systems + audio | A short interaction on tagged faces that plays one of three authored return sounds (barren / iron with tail length 1–4 / hollow) and draws beat-dots after the return. Shared with TF-M3 and TBC. Tag per face, no physics. |
| Lever accepted only after a doubled return | Systems | A face state that flips from bound to loose after N wedge strikes (authored N); the lever interaction checks the state. |
| Crew path (call strike/hold) | Systems / NPC | Two miner NPCs with a strike animation loop; a two-option prompt per strike; same face state. |
| Slab-drop hazard (H1) | Systems | Hazard volume with telegraph; triggered by strikes after the loose state. |
| Hollow faces block mining | Systems | Mining interaction disabled on hollow-tagged faces, with a prompt line. |
| Rock Vipers (first-appearance tuning) | Encounters package | Viper and shale-coil with the longer telegraphs listed. |
| Carry-state capstone and set interaction | Systems | Lowmark carry-state pattern. |
| Per-player props | 33.1.B2 | Chalk line wiped; sixth marker stone; rota board / tool barrow / old crew by `TSR_SEAM`. |
| Painted board update | Art | Plot list board with a sixth line (prop swap). |

### TSR.12 Economy dependencies

EC-01 (seam ore) is the only output. The seam face, the ore and its processing do not exist as items until the economy pass rules on Thornfell mining. Nothing here assumes ridge iron becomes a weapon or tool material.

### TSR.13 Mystery ledger entry

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The sixth cellar** | Someone was laid in a walled-up stretch of the plot terrace in the retreat winter and not written on the board. Who, and why they were not listed, is **not decided** and is not to be decided by later content without a Director ruling. | Five cellars, five lines. | A hollow return; no mouth, no lintel; the board's five lines. | A deserter hidden; a crime; Brackenstep's crew dug it. (None is supported: the wall is old work.) | Everything about the person. | **None.** Deliberately unexplained [PROPOSAL — DIRECTOR]. |

### TSR.14 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Dagny Grell** [NEW], Kettlecrag plot-keeper, old | The five lines on the board; that her mother's mother cut the plots "when people came over the shoulder"; how many are in each cellar. | That there is a sixth. Anything about the war beyond the plots. | Few words, all of them final. Calls the dead "the plots", as if they were the soil. |
| **Tormod Lisk** [NEW], Brackenstep seam-reeve | What his highstead's tools look like; that the snow is near; where rust runs thickest. | That the seam surfaces up the scarp. | Practical, not cruel. Says the hard thing first and is sorry after. "The dead don't need nails." |
| **Gerrit Carrick** [NEW, bible §5.2], miners' foreman | Rock, crews, how to sound a face. Before TF-M3: that his men have "other work, down the gorge, by the crate". | What the plates are for (bible §2.5). | Defensive, ashamed of the work, grateful. Teaches because "it's quicker than watching you guess". |

**Two claims** (`TSR-D1`, step `S00_dispute`)

```
TSR-D1.01 TORMOD: "If you're from Kettlecrag, I've heard it. If you're not, stand clear of the line."
TSR-D1.02 DAGNY: (sitting on a stool in front of the chalk line) "Walker. Sit, if you're stopping. I'm stopping."
TSR-D1.03 TORMOD: "Seam runs along that wall. Thickest rust on the slope. We cut before the snow or Brackenstep goes into winter with wire round its picks."
TSR-D1.04 DAGNY: "That wall's the plots."
TSR-D1.05 TORMOD: "The plots are on top. The iron's in the wall."
TSR-D1.06 DAGNY: "Under is through."
  > "What's in the wall?"                                → TSR-D1.07
  > "How do you know the seam runs along there?"         → TSR-D1.09
  > "Who are they?" (the miners at the fire)             → TSR-D1.11
TSR-D1.07 DAGNY: "Cellars. People hid in them, the winter they came over the shoulder. Then some of them stayed in them." (beat) "That's the plots."   → TSR-D1 options
TSR-D1.09 TORMOD: "Look at it. It's bleeding iron."
TSR-D1.10 GERRIT: (from the fire, not getting up) "Rust's where the water comes out. Not where the iron is."   → TSR-D1.13
TSR-D1.11 GERRIT: "Carrick's crew. Miners. For hire, to whoever's hiring." (beat) "Nobody's hiring."   → TSR-D1 options
TSR-D1.13 TORMOD: "Then you tell me where it is, Carrick."
TSR-D1.14 GERRIT: "I'm not paid to tell you." (looks at the player) "I'll show the walker. Quicker than watching you lot guess."
      {event: TSR-D1 end → completes S00_dispute}
```

**Strike and count** (`TSR-D2`, step `S01_learn`, at the teaching stones)

```
TSR-D2.01 GERRIT: "Rock talks back if you hit it right. Not loud. You count."
  > [no mining tool] "I've nothing to hit it with."                  → TSR-D2.02
  > "Show me."                                                       → TSR-D2.04
TSR-D2.02 GERRIT: "Here. Sounding hammer. Don't lose it, it's the last thing I own outright."   {give miner's sounding hammer}   → TSR-D2.04
TSR-D2.04 GERRIT: "That one first. Flat knock, gone. Nothing in it."
TSR-D2.05 GERRIT: "That one. Hear the ring? And the buzz after? That's iron. Longer the buzz, further in it sits."
TSR-D2.06 GERRIT: "That end. Slow, and it comes back twice. Hollow. Something's not there."
TSR-D2.07 GERRIT: "Twice each. Then you'll not need me."
      {event: TSR-D2 end; three sound_rock prompts enabled}
```

**Gerrit barks while teaching**

| Id | Trigger | Line |
|---|---|---|
| TSR-B1.01 | Barren stone sounded | "One. Nothing. Good." |
| TSR-B1.02 | Iron stone sounded | "Ring, buzz. Count the buzz." |
| TSR-B1.03 | Hollow stone sounded | "Hear it come back? That's the room behind it talking." |
| TSR-B1.04 | Second round complete | "You've an ear. Don't let it go to your head." |
| TSR-B1.05 | [TF-M2 Completed, TF-M3 not Completed] Idle near the fire | "Got work down the gorge. By the crate. Don't ask me what's in the crate." |
| TSR-B1.06 | [TF-M3 Completed] Idle near the fire | "You got my pairs off the ledges. I've not forgotten. I'm just bad at saying so." |

**Optional, Gerrit and the ledger** (`TSR-D2.10`, available after `S01_learn`, condition `[TIW Completed and TES not Completed]`)

```
TSR-D2.10 PLAYER: "Your men's name is on a store ledger. 'Plates by the crate.'"
TSR-D2.11 GERRIT: (a long look) "Lot of names on a lot of ledgers this winter."
TSR-D2.12 GERRIT: "Man pays by the crate. I don't ask what for. You don't ask a man who pays."   → end
```

(This adds nothing to TF-M3's evidence; it repeats what the ledger already says and keeps Gerrit's TF-M3 rescue unchanged.)

**After the chalk line** (`TSR-D3`, plays when `S02_chalk_line` completes)

```
TSR-D3.01 TORMOD: "Iron. Iron." (beat) "And two hollows."
TSR-D3.02 DAGNY: "Two cellars."
TSR-D3.03 TORMOD: "We'd go round them."
TSR-D3.04 GERRIT: "Round a hollow, in shale? You'd have the wall in your lap and them with it."
TSR-D3.05 DAGNY: "Sound them all. Every one. So we know what we're arguing over."
  > "All right."                                        → TSR-D3.06
  > "Why? The seam's the question."                     → TSR-D3.07
TSR-D3.06 DAGNY: "Board's in the niche. Five. Start at the end with the white lintel."   → end
TSR-D3.07 DAGNY: "Because I'll not have it said Kettlecrag hid one." (beat) "Five on the board. Start at the white lintel."   → end
      {event: TSR-D3 end → S03_count active}
```

**The sixth** (`TSR-D4`, after the strange moment, TSR.5)

```
TSR-D4.01 DAGNY: (finger moving down the board) "Haldis and the two little ones. Eyolf. The Vey sisters. The cart-man. The four with no names." (beat) "Five."
TSR-D4.02 DAGNY: "I've five."
  > "There's something behind the plain wall."           → TSR-D4.03
  > (say nothing)                                        → TSR-D4.04
TSR-D4.03 DAGNY: "I heard it." (puts her palm flat on the wall) "No door. Somebody walled it and walked away."   → TSR-D4.05
TSR-D4.04 DAGNY: (puts her palm flat on the wall) "No door. Somebody walled it and walked away."                 → TSR-D4.05
TSR-D4.05 TORMOD: (hat in hand, then annoyed with it) "...Well, we're not cutting there."
TSR-D4.06 DAGNY: "No. You're not."
TSR-D4.07 GERRIT: "Rust climbs the scarp. Where it stops climbing, it comes out. Go and count it, walker."
      {event: TSR-D4 end → S04_scarp active}
```

**Scarp barks** (interaction log, player alone)

| Id | Trigger | Line |
|---|---|---|
| TSR-B2.01 | Station 1 sounded | "Ring. The buzz runs on. Far in." |
| TSR-B2.02 | Station 2 sounded | "Shorter." |
| TSR-B2.03 | Station 3 sounded (after E1) | "Shorter again. It's close." |
| TSR-B2.04 | Upper face sounded | "One ring. No tail. It's right here." |
| TSR-B2.05 | Gust caught in the open | "The scarp shoves. Get behind the chalk." |

**Opening the face** (Gerrit, if present; crew path or his crew watching)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TSR-B3.01 | Score complete | GERRIT | "Wedges in the score. Then hit, and listen between." |
| TSR-B3.02 | Lever on a flat return | (log) | "Still holding." |
| TSR-B3.03 | First doubled return | GERRIT | "There. Hear that? It's let go inside. Lever it." |
| TSR-B3.04 | Strike after the doubled return | GERRIT | "Stop hitting a loose thing. Move." |
| TSR-B3.05 | Crew path, correct "hold" | MINER | "Holding." |
| TSR-B3.06 | Crew path, early "strike" | MINER | (strikes; flat) "It's a hill, walker. It's in no hurry." |
| TSR-B3.07 | First pick | GERRIT | "That's honest rock. Been a while." |

**Who works it** (`TSR-D5`, step `S06_judge`, at the plot terrace)

```
TSR-D5.01 TORMOD: "Clear of the plots. Up the scarp. Fine. Whose is it?"
TSR-D5.02 DAGNY: "It's Kettlecrag's slope. Always was."
TSR-D5.03 TORMOD: "And it's Brackenstep's picks that are wired together."
TSR-D5.04 [TSR_CREW_CUT] GERRIT: "My lads opened it. I'll say that once and then not again."
TSR-D5.05 DAGNY: (to the player) "You counted. Say."
  > "Both highsteads, turn about. Hire Carrick's crew to cut it."          → TSR-D5.10
  > "Brackenstep needs it before the snow. Kettlecrag keeps the plots and a tithe."   → TSR-D5.20
  > "It's Kettlecrag's slope. Kettlecrag cuts, and sells Brackenstep fair."  → TSR-D5.30
TSR-D5.10 TORMOD: "Wages. Out of iron we haven't got yet." (beat) "...Turn about. Fine."
TSR-D5.11 DAGNY: "Kettlecrag's turn first. It's our slope."
TSR-D5.12 GERRIT: (very carefully not looking pleased) "From the thaw. We've work till then."
TSR-D5.13 [TF-M3 Completed] GERRIT: "Honest work. From the thaw." (beat) "I'll take it."
      {set TSR_SEAM = shared; event: S06_judge complete}  → TSR-D5.40
TSR-D5.20 TORMOD: "This week. Before the snow."
TSR-D5.21 DAGNY: "A tithe. Every load. I'll count it in my sleep."
TSR-D5.22 DAGNY: "And you'll ask me, every time you go past the plots. Not tell me. Ask."
      {set TSR_SEAM = brackenstep; event: S06_judge complete}  → TSR-D5.40
TSR-D5.30 TORMOD: "So we buy it. Iron out of the hill we live under, and we buy it."
TSR-D5.31 DAGNY: "Fair. You heard the walker. Fair."
TSR-D5.32 TORMOD: "I heard 'buy'."
      {set TSR_SEAM = kettlecrag; event: S06_judge complete}  → TSR-D5.40
TSR-D5.40 DAGNY: "One more thing. The sixth wants a stone. A plain one. Off the wall."
      {event → S07_mark active}
```

**The sixth stone** (`TSR-D6`, step `S07_mark`)

```
TSR-D6.01 DAGNY: (painting a sixth line on the board, slowly) "No name. A mark." (beat) "And 'found by sound'. So whoever comes after knows how."
TSR-D6.02 TORMOD: "Cairn-Keeper should hear of it."
TSR-D6.03 DAGNY: "She will. From me."
  > "Who do you think it is?"                            → TSR-D6.04
  > "I'm glad it's marked."                              → TSR-D6.06
TSR-D6.04 DAGNY: "I think it's someone." (beat) "That'll do for the board."   → TSR-D6.06
TSR-D6.06 GERRIT: (handing back nothing, because there's nothing to hand back) "You keep the hammer. You've an ear."
TSR-D6.07 DAGNY: "Go on, walker. Five lines were enough for sixty years. Six'll do."
      {set TSR_VOID_MARKED; payment per TSR.9; event: TSR-D6 end → quest Completed}
```

**Inspect texts**

| Object | Text | Condition |
|---|---|---|
| Rust streaks | "Red runs down every wall face. Where the water comes out of the hill, it brings the colour." | — |
| Chalk line | "A cutting line, chalked at waist height straight along the plot terrace's back wall." | Before `S06` |
| Chalk line (wiped) | "Wiped. A pale smear where the line was." | After `S06` |
| Cellar mouth | "Planks, pegged shut. Whitewashed lintel. Cairn moss at the foot." | — |
| Plot list board | "Five cellars, five painted lines. Names on some. 'Four with no names' on one." | Before `S07` |
| Plot list board | "Six lines. The sixth: a mark, and 'found by sound'." | After `S07` |
| Plain wall (sixth) | "No mouth, no lintel, no line on the board. The rock behind it is hollow, the size of a person lying down." | After the sixth sounding |
| Marker stone (set) | "A plain capstone off the war wall. Nothing cut on it." | After `S07` |
| Upper face | "Rust-black rock under an overhang. It rings when you touch it with a fingernail." | — |
| Brackenstep's mattock | "Cracked through the eye and bound with wire. It will last one more winter, or it won't." | — |

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| DAGNY | "Kettlecrag's turn. Then theirs. Then ours. I've a board for that too now." | `TSR_SEAM` = shared |
| TORMOD | "New picks. Ask Dagny, every time. She makes me say please." | `TSR_SEAM` = brackenstep |
| TORMOD | "Bought iron out of my own hill. Tell nobody." | `TSR_SEAM` = kettlecrag |
| BELL-HAND (TME10 hollow) | "Kettlecrag's put a stone in the wall up there. Plain one. Nobody knows who." | `TSR_VOID_MARKED` |
| MINER (Carrick's) | "Thaw, she says. We'll be here. Somebody counted for us." | `TSR_SEAM` = shared, TF-M3 Completed |

### TSR.15 Open decisions

1. **EC-01:** whether Thornfell has an ore state at all. The quest stands without one (payment in coin, face as a station).
2. **Rock Vipers' first appearance** moves to TSR for players who take it before TF-M3. Encounters package to accept the longer telegraphs or move TSR's unlock after TF-M3 (not recommended: Mining would arrive too late to feed TF-M3's anchor sounding).
3. **Highstead names** Kettlecrag and Brackenstep are new, off-map and unplaced (MAP VERIFICATION REQUIRED). If the zone package prefers existing highsteads, swap the names; nothing else changes.
4. **The sixth cellar** stays unexplained [PROPOSAL — DIRECTOR]. A later Register of the Unreturned case could take it up only by Director ruling.
5. **Gerrit's thaw contract** is set by TSR but reads TF-M3 for its "honest work" line. The Act II author is asked (request) for one optional Gerrit line in TF-M3's coda: "We've a seam at Red Slope from the thaw." Nothing depends on it.

### TSR.16 Review log

| Finding | Revision |
|---|---|
| First draft let the player choose to cut under the cellars "carefully". | Removed. A face that sounds hollow cannot be mined at all. The choice is about who works the clear seam, not whether to disturb the dead. |
| Echo sounding risked duplicating TF-M3's rope-anchor reading. | Kept the same interaction on purpose (a skill taught once, used twice) but gave TSR its own third reading (iron's ring and tail) and its own use (prospecting by hot-and-cold, then timing a slab). TF-M3 reads only solid vs loose. |
| The sixth hollow could be read as a revelation seed. | It is self-contained and withheld; no record, no name, no link to the closure roster or the rear guard. Dagny notifies Maera off screen; no cairn stone is cut in this quest. |
| Gerrit's cameo risked pre-empting TF-M3. | He only hints at "work by the crate" and never names the hornwright or the plates' use. The optional ledger exchange repeats the TF-M2 ledger's own words. |
| Combat share. | One small viper nest on a required station; everything else is listening. |
| Ridge iron named as an item. | Every reference is "seam ore", tied to EC-01; payment falls back to coin. |

---

## TST — Stormwood

### TST.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `thornfell.side.stormwood` |
| Type | Skill introduction (Woodcutting, Fletching as bow-stave work). Bible §7.2 brief (its "first Ranged weapon" is held back pending S01, TST.15); discovery TDS09 (Burned Slope regrowth). |
| Unlock | TF-M1 Completed. Offered at Brita Crane's stall in Stonewake's ridge-market. |
| Resume hook | Brita at her stall: "Slope's still there. So's my patience, mostly." |
| Skills | Woodcutting (required), Fletching (required), Melee (light). Ranged only in the S01-gated proposal layer (TST.15). |
| Combat share | ~10% (one wolf pair and a howler at the slope foot) |
| Choice | The slope's last sound stem: leave it to seed, or cut it for the Ridge Wardens' winter bows |
| Unlocks | Wood selection by ear; the player's racked stave at Brita's stall; Brita as a future commission giver. [PROPOSAL — DIRECTOR, S01] a first bow (EC-05) and the wind butts as a Ranged practice station. |
| **Anchor** (§7.1) | Stonewake's craft households (the ridge-market bowyers) and the Ridge Wardens as the bowyer's customers. |
| **World-truth row** | None asserted (present-day only). The Burned Slope is a war site [CANON feature]; this quest does not say who burned it. |
| **Revelation role** | Self-contained. |
| **Recurring evidence** | None. |
| **State compliance** | Inactive / Active / Completed. Choice recorded in `TST_STEM`. No fail path: a wrong stem, a cut in a gust, a bad tiller pass or a missed shot each give a line and another try. |

**In one paragraph.** Brita Crane, the oldest bowyer in Stonewake's ridge-market, turns away a Warden who wants to buy a bow, and then turns down the player too: she does not sell to people who cannot pick wood, and she does not teach people who will not listen. On the Burned Slope, stormwood has come up through the ash, stems that have been whipped by the hard wind every day of their lives. The ones that cracked inside sing when the gust goes through them. The ones that held stay silent. The player shelters through three wind windows and, in each gust, marks the stem that makes no sound. They cut one stem from each stool between gusts, so the stool grows again, while ridge wolves come up the slope foot. On the last gust the hollow burned stumps moan all together, and Brita, sitting on a rock below, answers them with two short notes on her horn out of a lifetime's habit, and then laughs at herself. Back at her bench the player splits a seasoned billet along its grain, roughs it out, tillers it until both limbs bend alike, and hangs it unstrung on Brita's rack under their own tag. Then Brita takes the player to the wind butts on the terrace edge and shoots while the player calls the lulls: her arrows go where the wind says unless the call is right. (If S01 rules ranged in, a [PROPOSAL — DIRECTOR] layer lets the player string the stave, fletch arrows and shoot the butts themselves; TST.15.)

### TST.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| A. Fetch a rare wood from a dangerous place. | Rejected. A fetch quest teaches nothing about the wood. |
| B. Pick by sight (straight grain, no knots). | Rejected. Lowmark already taught sight reading; Thornfell's system is sound. |
| **C. Pick by what the wind does to it, by ear; cut as a steward; tiller the stave; watch the bowyer shoot in the wind** (selected). | **Selected.** Woodcutting and Fletching are each taught as wind-reading, which is the region's grammar. |

| Element | Source | Status |
|---|---|---|
| Burned Slope, crag-pine and stormwood regrowth | Bible TP24, TDS09 | [CANON feature]; [NEW] detail |
| Stormwood "shaped by heavy winds; durable, flexible, perfect for bows" | Dossier §XI | Legacy concept, **not approved** (TD-13; EC-04) |
| Goatwillow "used for bows and light tools" | Dossier §X | [CANON] flora; shafts (EC-07) |
| Wind windows and the whistle tell | Bible §1.1, §9.5 | [NEW] system |
| Ridge Wolves: runner, howler | Bible §10 | [CANON] family; [NEW] variants |
| Fletching and Ranged in Phase 1.3 `v1_core` | Bible TD-13 | Bible statement; **S01 open** in the economy set |
| Brita Crane | This package | [NEW] |

### TST.3 The places [MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling |
|---|---|---|
| A. Brita's stall (Stonewake ridge-market) | Hook; bench | A bow rack with three bows and a dozen empty pegs. A tillering board on the wall, marked in lines. Billets on a drying rack, each tagged with a year in knife-cuts. A Warden walking away empty-handed. |
| B. Burned Slope foot | Brita's rock | Old char on every stone. Hollow burned crag-pine stumps, some taller than a person. Brita sits here on a flat rock with her horn and a flask. |
| C. The three stands | Selection | Stools of stormwood (several stems from one root) in the lee of chalk-marked shelter faces. The fluted face above whistles before each gust. Some stems carry pale vertical lines in the bark: wind-shake. |
| D. The upper stand | Choice | The last good stool on the slope, three stems, one of them sound. Below it, the slope is ash and seedlings. |
| E. The wind butts (Stonewake terrace edge) | Ranged | Three straw butts on posts at the terrace lip, ribbons tied to each post to show the wind. A bench for watchers. |

### TST.4 Beats

**Beat 0 — Not For Sale (`S00_refused`).** *Objective: Find out what the bowyer wants.* `TST-D1`. Brita will teach if the player brings her three stems "the wind already tested".

**Beat 1 — The Slope (`S01_slope`).** *Objective: Go to the Burned Slope.* Enter area B. Brita is already there (`TST-D2`): "I'm old, not dead."

**Beat 2 — Listen in the Gust (`S02_listen`).** *Objective: Mark three stems the wind didn't crack.* At each of the three stands, the player shelters behind the chalked face. The whistle tells the gust (~3 s); the gust lasts ~6 s. During it, each stem in the stand bends. **Cracked stems sing:** a thin whistle from the shake cracks, each at its own pitch, positional. **The sound stem bends, stays silent, and comes back straight.** After the gust the player ties a rag on the stem they judge silent (one interaction). A wrong pick gets a Brita bark and the next gust; nothing is lost. Accessibility: during the gust, singing stems show a small subtitle cue ("[thin whistle, left]") and the controller rumbles on the singing side; the silent stem gets none. The third gust plays the strange moment (TST.5).

**Beat 3 — One From Each Root (`S03_cut`).** *Objective: Cut the marked stems.* Woodcutting as stewardship and timing:
- The cut goes **just above the collar** where the stem leaves the root (a chalked cut line Brita drew), so the stool regrows. Cutting elsewhere is not offered.
- The cut is a channel that **must pause in the gust**. When the whistle sounds, the player stops; a stem cut in a gust whips (hazard H1). The channel keeps its progress when paused.
- Outputs: a stave length (EC-04) per stem and ordinary wood from the trimmings.
- **Crew path:** "Let the lad cut." Brita's apprentice (role: APPRENTICE) saws while the player watches the face and calls **cut** or **stop** on each whistle. A late "stop" means the apprentice gets whipped and swears; no damage to the player, one more window. Woodcutting XP for calls.
- When the second stem falls, TST-E1 comes up the slope foot (wolves smell the sap, Brita says).

**Beat 4 — The Last One (`S04_third_stem`).** *Objective: Decide about the upper stand.* Area D: the slope's last sound stool. Its silent stem is the only seed-bearing sound wood left on this face. `TST-D4`; TST.8.

**Beat 5 — The Bench (`S05_bench`).** *Objective: Make the stave.* Back at Brita's stall. Brita puts the player's stems on the drying rack and hands down a seasoned billet from an earlier year: "Yours goes on the rack. You work mine. Somebody works yours." Fletching (bowyery) as play:
1. **Split** the billet: inspect the end grain; three split lines are offered; one follows the grain. A split off the grain runs out and Brita hands another billet ("They all do that once").
2. **Rough out** with the drawknife (one channel).
3. **Tiller** (three passes). The player draws the stave on the tillering board. The limb curve shows against the board lines; one zone of one limb stays flatter than the rest. The player picks the stiff zone (of three per limb) and scrapes it (short channel). After three passes both limbs bend alike. A wrong zone makes that zone weaker; the next pass shows it and the player corrects the other side. Always finishes in three to five passes.
- **Crew path for the tiller:** "Show me." Brita scrapes while the player reads the board and points to the stiff zone. Lower Fletching XP.

**Beat 6 — The Rack (`S06_string`).** *Objective: Rack your stave.* **Default (S01 open):** the tillered stave is left unstrung and the player hangs it on Brita's rack under a tag with their name cut in it (one interaction). Brita: "When you've a use for it." No item is granted. **[PROPOSAL — DIRECTOR, gated on S01]** *Objective: String the bow and fletch arrows.* Brace and string (one channel; string from Brita's stock, EC-06). Fletch five arrows at the bench: shaft, fletchings, head from Brita's bins (EC-07, EC-08); one short channel each. The first bow (EC-05) is the player's.

**Beat 7 — The Wind Butts (`S07_butts`).** **Default (S01 open):** *Objective: Call the lulls for Brita.* At the terrace edge Brita shoots and the player reads the ribbons and calls **now** or **wait** (two-option prompt per shot, three shots). A call in a lull or a steady wind lands her arrow; a call in a gust sends it wide and she laughs. Any three calls complete the step; nothing is consumed and no Ranged skill is used. **[PROPOSAL — DIRECTOR, gated on S01]** *Objective: Hit the three butts in the wind.* Ranged as wind-reading. The ribbons on each post show the wind. Three rules the player discovers by shooting: shoot **in a lull** after a gust and the arrow flies true; shoot in the **steady wind** and aim off into it by the ribbon; shoot **in a gust** and the arrow goes where the gust says. A hit on each of the three butts completes the step. Arrows come from Brita's practice quiver (no ammunition is consumed). No level check; aim is the player's.

**Beat 8 — Her Bench (`S08_close`).** *Objective: Hear what the bowyer says.* `TST-D7`. Quest Completed; `TST_BRITA_BENCH`.

### TST.5 The stumps (presentation spec: wonder)

| Time | Element | Spec |
|---|---|---|
| −3 s | Whistle | The third stand's gust tell, as usual. |
| 0–6 s | The gust | Cracked stems sing as before. Under them, the **hollow burned stumps** across the slope moan together: a low rising note, wavering, rough. Positional; from everywhere downslope. Ash lifts off the slope in a thin sheet. |
| 6–8 s | Lull | The moan stops with the gust. The ash settles. |
| 8–10 s | Brita | From her rock below, Brita lifts her horn and blows **Answer** (two short). The Answer glyph shows (it is a real call). |
| 10–14 s | Brita | She lowers the horn and laughs, short and at herself (`TST-B2.04`). |
| UI | No objective popup until the rag is tied. |
| Meaning | Terrain: wind across hollow trunks. Nothing calls; nothing answers back. Brita's Answer is sixty years of habit. It identifies nobody and means nothing (bible §11.3). Plays once per player; afterwards the stumps moan in any hard gust on the slope (ambient). |

### TST.6 Encounters and hazards

| Id | Enemies / hazard | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TST-E1** | 2 × Ridge Wolf (runner), 1 × Ridge Wolf (howler) | Slope foot below the second stand | Runners: flank and bite, leashed to the slope. Howler: hangs back on a rock | **Runner:** drops its head and shoulders (~1.0 s), then a lunge. **Howler:** sits back and lifts its muzzle (~2.0 s); a finished howl brings one more runner from the ridge (once only). Interrupting the howler (any hit) stops it | Readable pack pressure; a reason to want reach | Required. 45–60 s. Melee is enough; Brita throws stones at the howler if the player is slow (one interrupt, scripted) |
| **TST-H1** | Stem whip | Any stand, cutting in a gust | Environmental | The whistle (~3 s) | Teaches the wind window for cutting | Knockback and small damage. Cannot kill above a quarter health |
| **TST-H2** | Gust in the open | Between stands | Wind window | The whistle | Universal | Stagger; never off the slope |

Combat drops nothing the quest needs. Death: respawn at Brita's rock; marked stems and cut progress persist.

### TST.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_refused` | Find out what the bowyer wants. | `TST-D1` end node | Yes | |
| `S01_slope` | Go to the Burned Slope. | Enter area B + `TST-D2` end | Yes | Cutting tool lent if needed (`TST-D2.03`) |
| `S02_listen` | Mark three stems the wind didn't crack. | 3 × `tie_rag` on sound stems | Yes | Wrong stem: bark, retry next gust; strange moment on the third gust |
| `S03_cut` | Cut the marked stems. | 3 × `stool_cut` complete (or crew path) + TST-E1 defeated | Yes | Channel pauses in gusts, keeps progress; sets `TST_CREW_CUT` on the crew path |
| `S04_third_stem` | Decide about the upper stand. | `TST-D4` choice (and one `stool_cut` if *wardens*) | Yes | Sets `TST_STEM` |
| `S05_bench` | Make the stave. | `split` (on-grain) + `rough_out` + tiller passes until even | Yes | Crew path: Brita scrapes |
| `S06_string` | Rack your stave. | `rack_stave` (default). S01 proposal: `string_bow` + 5 × `fletch` | Yes | Default grants nothing. S01 proposal grants the first bow (EC-05) |
| `S07_butts` | Call the lulls for Brita. | 3 × `call_lull` (default). S01 proposal: one hit on each of 3 butts | Yes | No ammo used on either path |
| `S08_close` | Hear what the bowyer says. | `TST-D7` end | Yes | Sets `TST_BRITA_BENCH`; quest Completed |

| Flag | Set by | Read by |
|---|---|---|
| `TST_CREW_CUT` | `S03` crew path | `TST-D7` line |
| `TST_STEM` = seeded / wardens | `TST-D4` | Slope prop (seed-bearing stool, or a stump with a Warden's tally notch); Passwatch Warden barks; Burned Slope opportunity |
| `TST_BRITA_BENCH` | `S08` | Master commissions (`TH_STANDING`) |

### TST.8 Choices and consequences

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Leave it to seed** (`seeded`) — *"Leave it. The slope needs something to grow from."* | The stool stays whole. Brita ties a red rag round it: nobody cuts here. | The Ridge Wardens' patrol at Passwatch goes into winter one bow short; Vessa Galt's corporal grumbles (bark). | The upper stand shows seedlings round the stool (prop). The Burned Slope opens as a Woodcutting opportunity "for the stems the wind cracked": firewood and ordinary wood only. |
| **Cut it for the Wardens** (`wardens`) — *"Cut it. The patrol needs bows before the snow."* | One more stool-cut; Brita sends the stave to the Warden who walked away in Beat 0. | The slope's last sound seed-stem is gone; regrowth on this face slows (the stool still regrows, from the root). | The patrol has its bow (Warden bark at Passwatch). The upper stand is a cut stool with a Warden's tally notch. The slope's sound-wood opportunity stays **closed until** TF-M3 is Completed ("a season's growth"). |

Neither is wrong. Brita does not say which she would have done (`TST-D4.06`).

### TST.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| **Picking by ear** | Knowledge | Authored stormwood stands across Thornfell become readable in a gust: cracked stems sing, sound stems stay silent. Inspect lines: *"Shaken. It sings."* / *"Sound. It said nothing."* |
| Racked stave | Place / standing | The player's tagged stave hangs on Brita's rack (per-player prop). No item. |
| First bow ("bowyer's first stave") | Tool | **[PROPOSAL — DIRECTOR, gated on S01]** EC-05. Not granted by default. Item pass defines it if S01 rules ranged in. |
| Practice arrows | Ordinary output | **[PROPOSAL — DIRECTOR, gated on S01]** only. |
| Wind butts | Access | **[PROPOSAL — DIRECTOR, gated on S01]** a public Ranged practice station. By default the butts are Brita's and only watched. |
| Cutting saw | Tool | Lent at `TST-D2` if the player lacks a cutting tool; kept on completion. |
| Small payment | Currency | Brita pays for the stems she racked (economy tuning). |
| Woodcutting, Fletching, Melee XP | Action XP only | No lump quest XP. Ranged XP only in the S01 layer. |

### TST.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Wrong stem marked | Bark; the rag can be untied; next gust. |
| Cut in a gust | Whip (H1); progress kept. |
| Split off the grain | Brita hands another billet; unlimited. |
| Tiller wrong zone | Next pass shows it; always finishes. |
| Missing shots | No cost; the quiver does not run out. |
| Death | Respawn at Brita's rock (or her stall after `S05`). |
| Walking away / logout | Quest stays Active; last step restored; rags, cuts and bench progress persist. |
| Co-op | Gusts are world weather (shared); each player marks and cuts their own per-player stems. The upper stand's state follows each player's own `TST_STEM`; fallback: the host's. Each player racks their own stave (S01 proposal: makes their own bow). |

### TST.11 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Gust-driven stem audio | Audio + Systems | Stand volumes tied to the wind-window timer; tagged stems play an authored whistle during the gust; sound stems play none. Subtitle cue and rumble side. |
| Pausable channel keeping progress | Systems | Stool-cut channel that auto-pauses on the whistle and resumes. |
| Tillering board | UI + Systems | A curve overlay with three selectable zones per limb; each pass changes an authored curve state. Fallback: a three-step prompt ("left limb, middle stiff") with the board as art. |
| Lull-calling prompt (default) | Systems | Two-option prompt read against the wind-window state; Brita's shot plays an authored hit or miss. |
| Wind on arrows | Combat / Ranged system | **S01 proposal layer only.** Projectile drift by wind state (lull / steady / gust). Fallback: authored hit chance by wind state, shown by the ribbons. |
| Wolves with howl interrupt | Encounters package | Howler with a channelled call and one reinforcement. |
| Per-player stand props | 33.1.B2 | Rags, cut stools, seedling prop or tally-notch stump. |
| Crew NPC (apprentice) | NPC | Saw loop and a two-option call prompt. |

### TST.12 Economy dependencies

EC-04 (stave billet); EC-05 to EC-08 (bow, string, shafts, fletchings and heads) only if S01 rules ranged in; ordinary wood from trimmings (approved provisional state). Seasoning is compressed by Brita's swap so no timer is needed.

### TST.13 Mystery ledger entry

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Owner |
|---|---|---|---|---|---|---|
| **The stumps that moan** | Wind across hollow burned trunks. | "The slope does that. Since the fire." | The moan only in hard gusts; the hollow trunks. | The slope is calling; the dead of the fire. | Who set the fire (not decided). | None; ambient only. |

### TST.14 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Brita Crane** [NEW], bowyer, old | Wood, wind, Wardens' bow arms; which stands on the slope are left. | Anything about the war she would say aloud. | Tests people by what they choose. Rude to buyers, patient with learners. Dry about her own age. Habits older than her reasons. |
| **APPRENTICE** (role), a Stonewake lad | How to saw; that Brita is always right eventually. | When to stop sawing. | Cheerful, bruised. |

**Not for sale** (`TST-D1`, at the stall)

```
TST-D1.01 BRITA: (to a departing Warden) "Come back when you've a reason that isn't 'I need one.'"
TST-D1.02 BRITA: (to the player) "And you'll want a bow."
  > "I'd like to buy one."                                → TST-D1.03
  > "I'd like to learn to make one."                      → TST-D1.05
TST-D1.03 BRITA: "No."  (beat) "I don't sell to people who can't pick wood."   → TST-D1.05
TST-D1.05 BRITA: "Burned Slope. Stormwood's come up through the ash. Wind's been at it every day of its life."
TST-D1.06 BRITA: "Bring me three stems the wind already tested. Not the pretty ones. The ones that held."
  > "How do I tell which held?"                           → TST-D1.07
  > "That's all?"                                         → TST-D1.08
TST-D1.07 BRITA: "You listen. Wind'll tell you. It's a gossip."   → TST-D1.09
TST-D1.08 BRITA: "That's all. People say 'all' and then come back with kindling."   → TST-D1.09
TST-D1.09 BRITA: "I'll come. I'm old, not dead. And I want to see you get it wrong."
      {event: TST-D1 end → completes S00_refused}
```

**At the slope** (`TST-D2`)

```
TST-D2.01 BRITA: (on her rock, flask out) "Hear the face up there? It whistles before the gust. When it does, get behind the chalk."
TST-D2.02 BRITA: "In the gust, the stems that cracked inside sing. Thin, like a kettle. The ones that held say nothing at all."
  > [no cutting tool] "I've nothing to cut with."          → TST-D2.03
  > "The quiet ones."                                     → TST-D2.04
TST-D2.03 BRITA: "Saw. Mine. Bring it back with all its teeth."   {give cutting saw}   → TST-D2.04
TST-D2.04 BRITA: "The quiet ones. Tie a rag on it. Go on."
      {event: TST-D2 end → S02_listen active}
```

**Listening barks**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TST-B2.01 | First gust | BRITA (shouted up) | "Hear them? That's the cracked ones complaining." |
| TST-B2.02 | Wrong stem marked | BRITA | "That one sang. You were looking, not listening." |
| TST-B2.03 | Right stem marked | BRITA | "Hm." (from Brita, praise) |
| TST-B2.04 | After the strange moment | BRITA | (lowering the horn) "Ha. Sixty years. I still answer it." (beat) "Nobody out there, you old fool." |
| TST-B2.05 | Third rag tied | BRITA | "Three. One from each root, now. Above the collar, where I chalked. And not in the gust." |

**Cutting barks**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TST-B3.01 | Cut paused on whistle | (log) | "Whistle. Stop. Let it blow." |
| TST-B3.02 | Cut in a gust (H1) | BRITA | "Told you. Wind's got opinions." |
| TST-B3.03 | Crew path, late "stop" | APPRENTICE | (whipped) "Ow. Ow. That's fine. That's fine." |
| TST-B3.04 | E1 starts | BRITA | "Wolves. They smell the sap. Shift them before they shift you." |
| TST-B3.05 | Howler sits back, player slow | BRITA | (throws a stone; it lands) "Shut up, you." |

**The last one** (`TST-D4`, upper stand)

```
TST-D4.01 BRITA: "Last sound stool on this face. One stem in it held."
TST-D4.02 BRITA: "Everything below it grows from what falls off it. And the Wardens at Passwatch are a bow short for the winter."
TST-D4.03 BRITA: "That lad this morning. He had a reason after all. I just didn't like it."
  > "Leave it. The slope needs something to grow from."      → TST-D4.04
  > "Cut it. The patrol needs bows before the snow."         → TST-D4.05
TST-D4.04 BRITA: (ties a red rag round the stool) "Nobody cuts here. I'll say it at market."   {set TST_STEM = seeded}   → TST-D4.06
TST-D4.05 BRITA: "Above the collar. It'll come again, slower."   {set TST_STEM = wardens; one stool_cut enabled}   → TST-D4.06
TST-D4.06 BRITA: "Don't look at me. I'd have done the other one. I always do the other one."
      {event: S04_third_stem complete on choice (and cut, if wardens)}
```

**The bench** (barks, `S05`–`S06`)

| Id | Trigger | Line (BRITA) |
|---|---|---|
| TST-B5.01 | Bench reached | "Yours goes on the rack. Green wood's no good to anyone. You work mine, from three winters back. Somebody works yours." |
| TST-B5.02 | Split off grain | "Ran out. They all do that once. Here." |
| TST-B5.03 | Tiller, both limbs even | "Look at that. Bends like it means it." |
| TST-B5.04 | Crew path tiller | "Point. I scrape. You'd take my thumb off." |
| TST-B5.05 | Stave racked (default) | "Yours. On my rack. Don't tell anyone I tillered it." (beat) "I didn't." |
| TST-B5.06 | Bow strung (S01 proposal only) | "That's yours. Not mine. Don't tell anyone I made it." (beat) "I didn't." |

**Wind butts** (barks, `S07`)

| Id | Trigger | Line (BRITA) |
|---|---|---|
| TST-B7.01 | Arrival (default) | "Ribbons tell you the wind. I shoot. You say when." |
| TST-B7.05 | Call in a gust (default) | "Wide. You knew that. So did I." |
| TST-B7.06 | Call in a lull (default) | "There. You waited for it. So did the arrow." |
| TST-B7.07 | Arrival (S01 proposal only) | "Ribbons tell you the wind. Shoot when it's quiet, or aim into it. Or don't, and learn." |
| TST-B7.02 | Miss in a gust | "Wind took that. Wind takes most things." |
| TST-B7.03 | Hit in a lull | "There. Waited for it." |
| TST-B7.04 | Hit aiming off | "Into the wind. Good. Most people argue with it." |

**Her bench** (`TST-D7`, step `S08_close`)

```
TST-D7.01 BRITA: "Well. You can pick wood and you can tell a lull. That's most of it."
TST-D7.02 [TST_CREW_CUT] BRITA: "The lad did your sawing. You did his listening. Fair trade."
TST-D7.03 [TST_STEM = seeded] BRITA: "Red rag's still up. I told the market. They grumbled. They'll leave it."
TST-D7.04 [TST_STEM = wardens] BRITA: "Warden came back for his bow. Said thank you. Took him two goes."
TST-D7.05 BRITA: "One day I'll want horn bows for the Wardens. Proper ones. When you can pick wood blind."
TST-D7.06 BRITA: "Not yet. Go away. Come back."
      {set TST_BRITA_BENCH; payment; event: TST-D7 end → quest Completed}
```

**Inspect texts**

| Object | Text |
|---|---|
| Wind-shaken stem | "Pale lines up the bark. Shaken inside." |
| Sound stem (after gust) | "Bent with the gust and came back straight. Said nothing." |
| Burned stump | "Hollow all the way down. Char inside like a chimney." |
| Collar chalk | "Brita's line. Just above where the stem leaves the root." |
| Drying rack | "Billets tagged with knife-cut years. Yours goes at the end." |
| Tillering board | "Lines at even spacing. A good bow's curve sits on them." |
| Ribbons at the butts | "They tell you which way, and roughly how hard." |

### TST.15 Open decisions

1. **S01 (v1 ranged scope).** The economy set defers all ranged content until S01 is ruled, and initial-release scope may not grow. **The fallback below is now the default build**; the bow, arrows and Ranged lesson are a [PROPOSAL — DIRECTOR] layer that switches on only if S01 rules ranged in. **Default:** `S06` makes an unstrung stave that Brita racks for the player ("when you've a use for it"), `S07` becomes a Brita demonstration the player watches and calls the lulls for, and the reward is the knowledge and the commission giver only. Woodcutting and the choice are unchanged.
2. **EC-04 to EC-08** as listed; seasoning compressed by the swap.
3. Ridge Wolf **howler** reinforcement behaviour to the Encounters package.

### TST.16 Review log

| Finding | Revision |
|---|---|
| First draft picked wood by sight (straight, no knots). | Changed to picking by ear in a gust: Thornfell's system, and new against Lowmark BW. |
| Tillering risked a fail state (snapped stave). | Tiller cannot snap; a wrong pass is corrected next pass. |
| The moaning stumps could read as a call or a message. | It is terrain noise with no call shape and no glyph; only Brita's Answer is a real call, and she laughs at her own habit. Checked against TTH's altered echo and TNR's singing cable: different source, place and meaning. |
| Ranged appearing in v1.5 while S01 is open. | Fallback documented; flagged in open questions. Independent review: fallback made the default; bow reward kept only as [PROPOSAL — DIRECTOR] gated on S01. |
| Stormwood named as an item. | "Stave billet" tied to EC-04; trimmings are ordinary wood. |

---

## TGY — Goat Year

### TGY.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `thornfell.side.goat_year` |
| Type | Skill introduction (Hunting, Leatherworking). Bible §7.2 brief; dossier §IX ("cliff goats: territorial, can ram travelers from narrow paths"). |
| Unlock | TF-M1 Completed (`TH_CALLS` is always set). Offered on the Stormwake shoulder path below the Goat Ledges. |
| Resume hook | Bera Scree at her shieling door: "He's still on the path. So am I, most days." |
| Skills | Hunting (required: tracking and reading; cull path adds approach, resolve, recover), Leatherworking (required), Melee (Ranged if S01 allows) (cull path, optional contact) |
| Combat share | 0–10% (the ram's charge only on a careless approach or a dusk walk) |
| Choice | Cull the old ram, or drive the herd with the Gather and Fall calls |
| Unlocks | Herd reading; the goat steps (agility route, walkable fallback); Bera's shed as a Leatherworking station; Bera as a future commission giver |
| **Anchor** (§7.1) | Herding households of the Stormwake shoulder (Regional Source Process: herding households, highstead pasture customs). |
| **World-truth row** | None (present-day only). |
| **Revelation role** | Self-contained. |
| **Recurring evidence** | None. |
| **State compliance** | Inactive / Active / Completed. Choice in `TGY_WAY`. No fail path: a wrong call-stone moves the herd a short way and they settle; a spooked ram returns to the path. |

**In one paragraph.** On the Stormwake shoulder a pedlar sits in the path with a split pack, the third this month: the herd's old ram came down at dusk and put him in the heather. Bera Scree, whose household keeps the shoulder herd, says the herd has always answered the Ordinary Calls; herders have used Gather and Fall on these ledges for longer than anyone has kept count. This autumn the herd will not leave the warm path at dusk, and the player, reading hoof scuffs, wool on thorn and a horn-rub notched too many times to count, finds out why: when Bera blows Gather, every head turns but his. He has gone deaf, and the herd follows him, not the horn. A goat year is named for its lead ram, and this has been his ninth. The player either culls him cleanly, or herds the whole flock up to the high ledges by blowing the calls from stones where the echo agrees with the horn, so the old ram follows the herd by sight. Either way, at dusk the herd climbs a face the player would have sworn was blank, on a stair of hand-cut steps under the lichen that nobody knew was there. Then, in Bera's shed, the player learns goat leather: flesh, light-test, work, smoke, and cut a pair of ledge-grip wraps.

### TGY.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| A. Kill the aggressive goats. | Rejected. Makes a herd a monster pack; no judgment. |
| B. Escort travellers past the herd. | Rejected. Escort is TF-M1's verb. |
| **C. Read why the herd won't move → cull or drive with the calls the goats know → tan** (selected; the bible brief). | **Selected.** Two honest ways to solve one animal problem; Hunting as reading, calls as herding. |

| Element | Source | Status |
|---|---|---|
| Cliff goats ram travellers from narrow paths | Dossier §IX | [CANON] |
| Goat Ledges of the Stormwake Shoulder | Bible TP28 | [NEW] POI |
| The Ordinary Calls; echo count | Bible §1.1, §9.4 | [NEW] system |
| Goats obey Gather and Fall | Bible §7.2 brief | [NEW] |
| Goat leather and wool | Dossier §XI | Legacy, **not approved** (TD-13; EC-09, EC-10) |
| Makers may refuse unsafe or dishonestly sourced hides | Regional Source Process (Thornfell) | Proposal |
| "Goat year" named for the lead ram | This package | [NEW] custom |

### TGY.3 The place [MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling |
|---|---|---|
| A. The shoulder path | Hook | A narrow path along a slope, heather below (soft; a ram's victim lands in it). Niches cut into the uphill side every so often, marked with cairn moss: travellers' refuges from the ram. A split pack. |
| B. The warm stretch | Problem | A south-facing run of path where the stone holds the day's heat; goat droppings, wool, scuffs. Where the herd beds at dusk. |
| C. The ledges | Tracking; drive | Stepped ledges above the path. Thorn bushes with wool. A horn-rub rock. Three **call-stones**: flat-topped rocks with a worn standing hollow, herders' places. Each faces a different cliff. |
| D. The high ledges | Drive target | Upper pasture, sheltered, harder to reach for milking. |
| E. The blank face | Wonder | A grey lichened face between the ledges and the high pasture. Looks unclimbable. |
| F. Bera's shieling and shed | Leatherworking | Stone hut, a fleshing beam, a soaking tub (covered), a working stake, a smoke-hood over a smoulder fire. Hides on the wall, each tagged with a knot-cord. A row of ram skulls over the door, one per goat year, with notches cut in each. |

### TGY.4 Beats

**Beat 0 — Third This Month (`S00_knocked`).** *Objective: Find out what's knocking people off the path.* `TGY-D1` with the PEDLAR and Bera. Bera lends a herding horn (carry-state loan) only if the player is not carrying their TF-M1 practice horn.

**Beat 1 — Read the Herd (`S01_track`).** *Objective: Read the herd's sign on the ledges.* Hunting reading; four inspects, any order: hoof scuffs in lichen (where they cross), coarse grey wool on thorn (one old animal, not the herd's brown), warm vs cold droppings on the warm stretch (they bed here every dusk), the horn-rub (notched far above the others: the old ram). The trail ends at the warm stretch.

**Beat 2 — Watch at Dusk (`S02_watch`).** *Objective: Watch the herd at dusk.* A short **watch** (Lowmark keep-watch convention; per-player presentation hour to dusk) from a niche. The herd comes down onto the warm stretch behind the old ram. Bera, at her shieling, blows **Gather**. Every head lifts and turns toward the shieling, then turns back to the ram. **He does not turn.** Inspect the ram: *"He didn't move an ear."* If the player walks the path during the watch, the ram's charge plays (TGY-E1) and the player lands in a niche or the heather.

**Beat 3 — His Ninth Year (`S03_choose`).** *Objective: Decide what to do about the old ram.* `TGY-D3` at the shieling. TGY.8.

**Beat 4a — The Cull (`S04a_cull`).** *Objective: Take the old ram cleanly.* Hunting approach, resolve, recover:
- **Approach** from downwind. The wind on the shoulder blows up the slope in gusts; the whistle tells them. Moving during a gust hides footfall but carries scent uphill: approach from **above** in a gust, or from **below** in a lull. A careless approach alerts him (stamp, head lowered) and he charges (E1); he then resettles on the warm stretch after a short wait (no idle).
- **Resolve:** a bow shot (if the player has a ranged weapon, e.g. from TST) or Bera's ledge spear close in. Exact resolution belongs to the Hunting interaction pass.
- **Recover:** field dressing on the ram (Hunting recovery) yields his hide (EC-09) and meat (food relationship).
- **Crew path:** "Do it with me." Bera makes the approach and resolution; the player reads the wind and calls **move** or **hold** on each whistle, then does the recovery. Or the player approaches and Bera dresses. Hunting XP either way.

**Beat 4b — The Drive (`S04b_drive`).** *Objective: Drive the herd to the high ledges.* A herding puzzle on the Ordinary Calls and the echo count (bible §1.1):
- The herd moves **toward Gather** and **drops into cover and stays on Fall**. But a call blown near a cliff comes back as an echo, and if the echo is loud and late, the herd turns toward the echo instead.
- At each of the three call-stones the player blows **Answer** first (a test note; the herd ignores Answer) and counts the echo. **One beat or less:** the echo agrees with the horn; calls from here work. **Two or more beats:** the echo will pull the herd toward the face.
- Sequence (any order of testing; the herd's path is fixed): from the right stone, **Gather** brings the herd up onto the middle ledge; the old ram follows the herd by sight. From the next right stone, **Gather** again brings them to the foot of the blank face (TGY.5 plays). At the high ledges, **Fall** settles them in the sheltered cover so they stay.
- A call from a wrong stone moves the herd a short way toward the wrong face; they settle; the player tries another stone. Nothing fails, nobody falls.
- **Hint path:** Bera, if asked at `TGY-D3.20`, says "The stone with the wet moss on it. Echo's short where it's damp." (She is right about two of three.)
- Hunting XP for the reading and the drive; no combat.

**Beat 5 — The Goat Steps.** Not a step: TGY.5 plays at the blank face on either path (on the drive as the herd reaches the face; on the cull at the next dusk watch, when the young ram leads the herd up). Sets `TGY_STEPS_SEEN`.

**Beat 6 — The Shed (`S05_tan`).** *Objective: Make something from goat leather.* Leatherworking at Bera's shed.
- **Hide in.** Cull: the ram's hide goes into the soaking tub. Drive: Bera gives a winter-killed hide from her stock ("He's not giving you his coat. Here's Ash's, from last winter."). Either way it goes in the tub. Tanning takes weeks: **the player works one of Bera's finished hides from the tub's other end** (the Lowmark yard pattern: the shed keeps working without the player).
- **Flesh** the player's hide on the beam (two channels) before it goes in. **Light test:** hold it up to the smoke-hole; thin spots glow. Scraping a glowing spot again tears it (one bark; Bera patches it; nothing lost).
- **Work** the finished hide over the stake until it goes soft (two channels; Bera times them by the creak: when it stops creaking it is soft).
- **Smoke** it under the hood (one channel).
- **Cut and stitch** ledge-grip wraps (EC-11): a pattern on the hide, two cutting channels, one stitching channel.
- **Crew path:** Bera's household fleshes and works; the player light-tests and cuts and stitches. Lower Leatherworking XP.

**Beat 7 — The Path (`S06_return`).** *Objective: See the pedlar over the path.* Walk the pedlar along the shoulder path (no threat). `TGY-D6`. Quest Completed; `TGY_BERA_SHED`.

### TGY.5 The goat steps (presentation spec: wonder)

| Time | Element | Spec |
|---|---|---|
| 0 s | Trigger | Drive: the herd reaches the blank face's foot. Cull: next dusk watch, the young ram (role) leads the herd to the face. |
| 0–4 s | The herd | The goats stop at the face. Then the lead goes up it, straight up a face the player cannot see a hold on, and the herd follows in single file. |
| 4–12 s | The steps | As each goat passes, its hooves scrape lichen off: a line of square-cut steps appears behind them, each a hoof-width deep, climbing the face in a slant. Old tool marks on each. |
| 12–16 s | Silence | The herd tops the face. The goats stand on the lip looking down at the player. Wind sound only. |
| After | Inspect | *"Steps. Cut square, a hoof wide, all the way up. Under the lichen. Nobody made these for goats."* |
| UI | No music; no popup. The objective line updates after the herd tops the face. |
| Meaning | An old cut stair, Echohewn or later (never said). The goats knew it. Becomes the **goat steps** agility route between the ledges and the high pasture (walkable fallback: the herders' path round the shoulder, longer). Nothing is explained. |

### TGY.6 Encounters and hazards

| Id | Enemies / hazard | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TGY-E1** | The old ram (Hunting fauna, provoked) | Warm stretch / path | Charges along the path when a person walks it at dusk or approaches carelessly; then resettles | Head down and a **front-foot stamp** (~1.2 s), then a straight charge along the path. Step into a moss-marked niche or sidestep downhill into the heather | The dossier's hazard as readable play | Small damage; knockback lands the player in a niche or the heather, never off a cliff. Not a fight: he resettles after a short wait |
| **TGY-E2** | The young ram (cull path only, after `S04a`) | Path, post-quest ambient | Bluffs travellers for a season | Same stamp, shorter charge that stops short | Consequence presentation | Harmless bluff; optional |
| **TGY-H1** | Shoulder gust | Ledges | Wind window | Whistle | Universal | Stagger in the open |

No human enemies. Death (rare): respawn at Bera's shieling; step and herd position kept (the drive resumes from the last ledge reached).

### TGY.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_knocked` | Find out what's knocking people off the path. | `TGY-D1` end | Yes | Herding horn lent if needed |
| `S01_track` | Read the herd's sign on the ledges. | 4 inspects | Yes | Any order |
| `S02_watch` | Watch the herd at dusk. | `watch` interaction + ram inspect | Yes | Per-player dusk |
| `S03_choose` | Decide what to do about the old ram. | `TGY-D3` choice node | Yes | Sets `TGY_WAY` |
| `S04a_cull` | Take the old ram cleanly. | Hunting recovery on the ram | If cull | Crew path allowed |
| `S04b_drive` | Drive the herd to the high ledges. | Herd reaches ledge 2 (Gather), face foot (Gather), high ledges + `call_blown` Fall in the settle volume | If drive | *call-blown* event (sister package §0.6) |
| *(event)* | — | Goat-steps presentation complete | — | Sets `TGY_STEPS_SEEN` |
| `S05_tan` | Make something from goat leather. | `flesh` × 2, `light_test`, `work_hide` × 2, `smoke`, `cut` × 2, `stitch` (or crew path) | Yes | Wraps granted (EC-11) |
| `S06_return` | See the pedlar over the path. | Pedlar escort-lite reaches the far niche + `TGY-D6` end | Yes | Sets `TGY_BERA_SHED`; quest Completed |

| Flag | Set by | Read by |
|---|---|---|
| `TGY_WAY` = cull / drive | `TGY-D3` | Herd presentation; path barks; TSM herd bark (request) |
| `TGY_STEPS_SEEN` | Goat steps presentation | Agility route enabled |
| `TGY_BERA_SHED` | `S06` | Master commissions |

### TGY.8 Choices and consequences

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Cull him** (`cull`) — *"He's had nine years. I'll take him, cleanly."* | The path is clear at once. The household has meat; the ram's hide is in the tub. A new skull goes over the door. | The herd is leaderless; the young ram bluffs travellers for a season (E2) and the herd scatters at bad moments. Bera grieves in her own way: she cuts the ninth notch and a line under it. | "This is Brisk's year now." Path barks about the young one. |
| **Drive the herd** (`drive`) — *"Leave him his year. I'll move them up where he can follow."* | The herd beds on the high ledges; the old ram follows by sight; the path is clear. | No hide from him (Bera's stock hide is used). The household climbs to the high ledges for winter milking, every day, in snow. Bera: "My knees thank you. Not." | The old ram finishes his year on the high pasture. Next autumn (presentation: after TF-M5 Completed) a skull with nine notches is over the door: he died up there, in his own time. |

Neither is wrong. Bera does not say which she wanted.

### TGY.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| **Reading a herd** | Knowledge | Authored herd sign across Thornfell returns lines: *"One old animal, alone."* / *"They bed here. Warm stone."* / *"Fresh. They crossed this morning."* |
| Goat steps | Access | Agility route between the Goat Ledges and the high pasture (walkable fallback round the shoulder). |
| Ledge-grip wraps | Made by the player | EC-11. Item pass defines function (frost grip; no stat assumed). |
| Bera's shed | Access | Leatherworking station (bounded intake; economy pass). |
| Meat (cull) | Output | Food relationship (economy). |
| Small payment | Currency | From the pedlar (grateful, poor) and Bera. |
| Hunting, Leatherworking XP | Action XP only | No lump quest XP. |

### TGY.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Charged by the ram | Knocked into a niche or heather; he resettles. |
| Wrong call-stone | The herd moves a short way and settles; try another stone. |
| Ram spooked during the cull approach | Resettles on the warm stretch after a short delay. |
| Torn hide (light test ignored) | Bera patches it; continue. |
| No horn | Bera's herding horn (carry-state; returned on completion). |
| Walking away / logout | Quest stays Active; herd position per player persists at the last ledge reached; shed progress persists. |
| Co-op | The herd is per-player presentation (each player drives their own instance of the herd). Fallback if unavailable: the herd is a shared actor; any player's correct call advances it and all present get credit; each player still chooses cull or drive in their own state, and the path presentation follows the host. The ram for the cull is a per-player spawn in the fallback. |

### TGY.11 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Herd actor responding to calls | Systems / AI | A herd group with authored waypoints per call-stone and call (Gather → next waypoint; Fall → settle). A wrong stone moves to an authored "wrong face" waypoint and back. No flocking simulation required. |
| Echo per call-stone | Audio | Authored echo delay per stone (short / long), played on any call. |
| *call-blown* event | Systems | As the sister package (§0.6). |
| Ram charge and resettle | Encounters / AI | A single fauna actor with stamp telegraph and fixed charge lane. |
| Goat-steps reveal | Art + Systems | A decal/lichen swap along the step line, triggered per player; then an agility trigger and fallback path. |
| Hunting hooks (approach, resolve, recover) | Hunting interaction pass | Wind-direction scent check tied to the wind-window state (fallback: a fixed "approach from above in gusts" volume). |
| Leatherworking station chain | 33.5 station binding | Beam, tub, stake, hood, bench; authored sequence; per-player progress. |
| Watch to dusk | Systems | Lowmark keep-watch per-player hour. |

### TGY.12 Economy dependencies

EC-09 (goat hide; raw hide is the nearest approved state), EC-10 (goat-leather piece; Thornfell tanning medium unselected), EC-11 (ledge-grip wraps), meat as a food relationship. The tub's contents are never named.

### TGY.13 Mystery ledger entry

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Owner |
|---|---|---|---|---|---|---|
| **The goat steps** | An old stair cut into the face; who cut it is not decided. | Nobody knew it was there. "Goats know more than we do." | Square-cut steps, tool marks, lichen. | A smugglers' stair; a war escape route. | Who and when. | None. |

### TGY.14 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Bera Scree** [NEW], herder and hide-worker | Every goat by name; the calls; the shed; that the old ram is "slower to look round". | That he is deaf, until the watch. | Blunt, fond, practical. Names years after rams. Grief comes out as work. |
| **PEDLAR** (role) | His pack and his bruises. | Goats. | Aggrieved, then thankful in a way that sounds aggrieved. |

**Third this month** (`TGY-D1`)

```
TGY-D1.01 PEDLAR: (sitting in the heather, pack split) "Don't walk that bit. Don't. There's a goat."
TGY-D1.02 BERA: (arriving with a crook) "He's a ram. And you walked it at dusk. Everyone knows not to walk it at dusk."
TGY-D1.03 PEDLAR: "I'm not everyone. I'm from Stonewake."
TGY-D1.04 BERA: (to the player) "Third this month. They've always come off the path when I call. This autumn they don't."
  > "Call them? With a horn?"                                 → TGY-D1.05
  > [no horn] "I'd help, but I've no horn."                   → TGY-D1.07
  > "Why this autumn?"                                        → TGY-D1.08
TGY-D1.05 BERA: "Gather, Fall. Same as you. Herders were blowing them up here before the Wardens wrote them down."   → TGY-D1 options
TGY-D1.07 BERA: "Herding horn. My mother's. It's dented where she dropped it on my father."   {loan herding horn (carry-state; only if no practice horn carried)}   → TGY-D1 options
TGY-D1.08 BERA: "If I knew I'd not be standing here with a man in my heather. Go and look at them. Up the ledges."
      {event: TGY-D1 end → completes S00_knocked}
```

**Reading barks** (interaction log)

| Id | Object | Line |
|---|---|---|
| TGY-B1.01 | Hoof scuffs | "Lichen scraped in a line. They cross here." |
| TGY-B1.02 | Grey wool | "Coarse and grey. Not the herd's brown. One old animal." |
| TGY-B1.03 | Droppings on the warm stretch | "Some warm, some cold. They bed here every dusk." |
| TGY-B1.04 | Horn-rub | "Notched far above the rest. Nobody's kept count of these." |

**Watch barks**

| Id | Trigger | Line |
|---|---|---|
| TGY-B2.01 | Herd arrives | (log) "The old one first. The rest behind him." |
| TGY-B2.02 | Bera's Gather sounds | (log) "Every head turns." (beat) "Every head but his." |
| TGY-B2.03 | Player walked the path | BERA (distant) "Told you. Dusk." |

**His ninth year** (`TGY-D3`)

```
TGY-D3.01 BERA: (not looking round) "He didn't turn."
TGY-D3.02 BERA: "Nine years he's led them. We call a year after its ram up here. This is his ninth."
TGY-D3.03 BERA: "He can't hear me. They go where he goes. He goes where it's warm."
  > "He's had nine years. I'll take him, cleanly."                       → TGY-D3.10
  > "Leave him his year. I'll move them up where he can follow."         → TGY-D3.20
TGY-D3.10 BERA: "Cleanly." (beat) "He'll be on the warm stretch. Come at him from above when it gusts, or below when it's still. He's deaf, not stupid; he can smell."
TGY-D3.11 BERA: "Want me with you, or not?"
  > "With me."     {crew path enabled}                                    → TGY-D3.12
  > "Not."                                                                → TGY-D3.12
TGY-D3.12 BERA: "Then go on."   {set TGY_WAY = cull; S04a active}   → end
TGY-D3.20 BERA: "Up. He'll follow them by eye. He always looks to see where they've gone. Just can't hear me say it."
TGY-D3.21 BERA: "Call-stones on the ledges. Test before you call. Some of them talk back too loud."
  > "How do I tell?"                                                     → TGY-D3.22
  > "I'll manage."                                                       → TGY-D3.23
TGY-D3.22 BERA: "Blow Answer first. They don't care about Answer. Count what comes back. One beat, it's yours. Two, it's the cliff's." (beat) "And the stone with the wet moss on it. Echo's short where it's damp."   → TGY-D3.23
TGY-D3.23 BERA: "Fall when they're up. They'll stay." (beat) "My knees'll hate you all winter."   {set TGY_WAY = drive; S04b active}   → end
```

**Drive barks**

| Id | Trigger | Line |
|---|---|---|
| TGY-B4.01 | Answer test, short echo | (log) "One beat. The horn and the echo agree." |
| TGY-B4.02 | Answer test, long echo | (log) "Two beats. Three. The cliff has its own idea." |
| TGY-B4.03 | Gather from a wrong stone | (log) "They turn toward the face. Wrong way." (beat) "They settle." |
| TGY-B4.04 | Herd moves right | (log) "Up. The old one looks round, sees them go, follows." |
| TGY-B4.05 | Fall at the high ledges | BERA (distant, approving) "There. Stay." |

**Cull barks**

| Id | Trigger | Line |
|---|---|---|
| TGY-B5.01 | Approach discovered | (log) "He stamps. Head down." |
| TGY-B5.02 | Crew path, Bera | "Hold. Hold. Now. Move." |
| TGY-B5.03 | After the cull | BERA (kneeling, hand on his neck) "Nine." (a long breath) "Good lad." |

**The shed** (barks, `S05`)

| Id | Trigger | Line (BERA) |
|---|---|---|
| TGY-B6.01 | Arrival (cull) | "His coat goes in the tub. You work Ash's, from last winter. He'll be ready when you're not looking." |
| TGY-B6.02 | Arrival (drive) | "He's not giving you his coat. Here's Ash's, from last winter. And one for the tub, so somebody's got work next year." |
| TGY-B6.03 | Light test | "Hold it to the hole. Where it glows, it's thin. Leave the glowing bits alone." |
| TGY-B6.04 | Scraped a thin spot | "And there's a hole. Everyone makes one. I'll stitch it. Don't make two." |
| TGY-B6.05 | Working the hide | "When it stops creaking, it's soft. Hides tell you, same as goats." |
| TGY-B6.06 | Wraps stitched | "Ledge wraps. Frost won't have you on the path now. It'll still try." |

**The path** (`TGY-D6`)

```
TGY-D6.01 PEDLAR: (stepping carefully past the warm stretch) "No goat."
TGY-D6.02 [TGY_WAY = cull] PEDLAR: (sees the young ram on a ledge) "...Smaller goat."
TGY-D6.03 [TGY_WAY = cull] BERA: "That's Brisk. It's his year now. He'll bluff you. He's all noise."
TGY-D6.04 [TGY_WAY = drive] BERA: (looking up at the high ledges) "He's up there, looking down at us. Ninth year. He'll finish it."
TGY-D6.05 [TGY_STEPS_SEEN] BERA: "And steps. On my own face. Forty years I've looked at that rock."
TGY-D6.06 BERA: "Come back when you want harness made. A whole herd's worth, one day. And boots that don't lie about ice."
      {set TGY_BERA_SHED; payment; event: TGY-D6 end → quest Completed}
```

**Inspect texts**

| Object | Text | Condition |
|---|---|---|
| Moss-marked niche | "Cut into the uphill side, moss on the lip. Room for one person and their opinion of goats." | — |
| Call-stone | "Flat-topped, with a hollow worn where a herder stands." | — |
| Ram skulls over the door | "One per goat year. The notches are the years each led." | — |
| Goat steps | "Steps. Cut square, a hoof wide, all the way up. Under the lichen. Nobody made these for goats." | `TGY_STEPS_SEEN` |
| Soaking tub | "Covered. It smells like a decision you can't take back." | — |

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| PEDLAR (Stonewake market) | "Took the shoulder path. Dusk. Nothing happened. I was disappointed." | Any |
| BERA | "Brisk's year. He knocked his own shadow over yesterday." | `TGY_WAY` = cull |
| BERA | "Up the ledges every morning. I'll have legs like a ram myself." | `TGY_WAY` = drive |

### TGY.15 Open decisions

1. EC-09/EC-10/EC-11 as listed; Thornfell tanning medium unselected.
2. **The goat steps** as a new traversal route: the zone package (Batch 4) to place it (MAP VERIFICATION REQUIRED).
3. "Goat year" as a custom is [NEW]; the Director may prefer it local to the Stormwake shoulder only (as written).

### TGY.16 Review log

| Finding | Revision |
|---|---|
| Driving risked being the obvious "kind" choice. | The drive costs the household daily winter climbs and gives no hide; the cull gives meat and hide but a leaderless herd. Bera never ranks them. |
| Herding puzzle could fail (goats off a cliff). | Wrong stones move the herd to an authored safe waypoint and back. No goat or player can fall. |
| The goat steps could be read as Echohewn lore. | Never named; inspect says only that nobody made them for goats. |
| Tanning time. | Bera's tub swap (Lowmark yard pattern) keeps the quest to one session. |
| Goat leather named as an item. | EC-10 working name only; the reward is the wraps, named by function. |

---

## TFS — First Smoke

### TFS.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `thornfell.side.first_smoke` |
| Type | Skill introduction (Cooking, with entry Hunting). Bible §7.2 brief; Part 3 custom *First Smoke Evening* ("bread, stories, and a deliberately ridiculous account of some earlier weather mistake"; the "third call too late" verse). |
| Unlock | TF-M2 Completed (`TH_SEASON` = snow). Offered at Nettlehook by Tova Rask on the first snow evening after TF-M2. |
| Resume hook | Tova at the longhouse door: "It's still First Smoke till everyone's been. You haven't been." |
| Skills | Cooking (required), Hunting (required, entry level) |
| Combat share | None |
| Choice | The second hare: in the pot tonight, or smoke-cured into the tally store |
| Unlocks | The upper longhouse hearth as a public Cooking station; fresh-snow tracking; a standing welcome at Nettlehook |
| **Anchor** (§7.1) | Nettlehook Highstead households (Ketil and Tova Rask, the longhouse host). |
| **World-truth row** | H16, indirectly: the verse is a children's distortion of the dropped Third Horn (bible §9.4; Part 3). Nothing about it is explained here. |
| **Revelation role** | Plants a seed for *The Third Horn* (TTH). Owns nothing. |
| **Recurring evidence** | The verse recurs in TTH as one of three things the player compares. Its independent custodians there are the Three Calls Shelter horn map and the host's bed book (sister package). The verse is never evidence by itself. |
| **State compliance** | Inactive / Active / Completed. `TFS_HARE`, `TFS_STORY`, `TFS_VERSE_ASKED` are outcome flags. No fail path: a lost hare track re-forms, a smoky room clears, a story told early still gets laughs. |

**In one paragraph.** On the first true winter night after the stores business, Tova Rask finds the player in Nettlehook and tells them the rule: a house that makes it through the first true winter night shares bread, a meal and a ridiculous story about some weather mistake, and the best story wins the seat nearest the fire. The player goes up onto the snow shelf with Tova's snare line for snowhares, which vanish in drifts and lay tracks that stop dead in open snow because the last jump was sideways and long. Back in the upper longhouse, the hearth's smoke blows back into the room until the player learns to open the smoke-flap only when the gust has passed. They stew the first hare by the lid's tick, and decide whether the second goes in the pot for everyone tonight, two hauliers who knocked at dusk included, or into the smoke-hood for the tally store. Then the stories: Ketil's, the host's, a haulier's, and the player's own, told into the hush of the room. Afterwards the children sing their verse, the one with "third call too late" in it. The oldest man at the table puts his cup down, gets up, opens the door, looks out into the dark for a long moment, closes it and sits down again. Tova asks what the third call is. Nobody answers her.

### TFS.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| A. A cooking contest judged by a panel. | Rejected. A recipe test; teaches nothing about the place. |
| B. Lowmark FK's shape (fire, hunt, feed, who eats last). | Rejected as a repeat. TFS keeps food but moves the choice to now-or-store and adds the story custom. |
| **C. Hunt in fresh snow → cook by smoke and sound → now or store → tell a story into a room → the verse** (selected). | **Selected.** Cooking taught as heat and smoke in a wind country; the region's dry humour as play; the TTH seed placed in a child's mouth. |

| Element | Source | Status |
|---|---|---|
| First Smoke Evening; the "third call too late" verse | Part 3 Thornfell proposal (customs) | Proposal; bible §7.2 [NEW] |
| Snowhares "quick to vanish in drifts" | Dossier §X | [CANON] fauna |
| Nettlehook; Ketil and Tova Rask | Bible TP03, §5.2 | [NEW, Part 3] |
| Humour dry and at one's own expense | Bible §5.3 rule 5 | Binding |
| Third Horn meaning dropped after the war | Bible §9.4 | [NEW] |

### TFS.3 The place [MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling |
|---|---|---|
| A. Nettlehook lane | Hook | First real snow, ankle-deep. Doors swept. Smoke from some chimneys, not all yet. Children's sledge tracks. |
| B. The snow shelf | Hunting | A shelf above the highstead: drifts against boulders, goatwillow scrub, Tova's snare line marked with twig flags. |
| C. The upper longhouse | Cooking; stories | Long room, benches, a central hearth under a smoke-hole with a flap on a cord. A smoke-hood at one end over a smoulder fire for curing. The tally board by the door (TME01 has been read already tonight). Two hauliers' packs in the porch. The **smoke seat**: a stool with a worn cushion nearest the fire. |
| D. The door | Unease | A heavy door to the dark. Snow on the step. Outside: nothing but the snow and the ridge. |

### TFS.4 Beats

**Beat 0 — The Rule (`S00_invite`).** *Objective: Find out what First Smoke wants of you.* `TFS-D1` with Tova.

**Beat 1 — Tracks That Stop (`S01_snowhare`).** *Objective: Bring two snowhares for the pot.* Entry Hunting in fresh snow:
- **Read:** hare tracks are a group of four, the two long hind prints landing ahead of the small fore prints, so a track points the way the long prints point (first inspect teaches it).
- **The doubled track:** a hare runs, turns back on its own prints, then jumps sideways. The track appears to **stop dead** in open snow. The player searches to the side (a short radius) and finds the landing, a long jump away by a drift. That is the trick and the small wonder of the hunt.
- **Resolve:** set a snare on the run where the track enters scrub (one interaction), then a short **watch** (Lowmark keep-watch, per-player hour), or approach a sitting hare in the lee of a drift, still between gusts (the gust hides footfall). Exact resolution to the Hunting pass.
- **Recover:** Hunting recovery on each hare (food relationship only; no pelt output in this quest, EC-12).
- **Crew path:** Tova's snare line already holds one hare; she shows the player how to reset it and the second is caught on the next watch. Hunting XP lower.

**Beat 2 — Smoke Goes Up (`S02_fire`).** *Objective: Get the hearth drawing.* The hearth is laid but the room fills with smoke when lit, because the wind is gusting across the smoke-hole. The player works the **smoke-flap** cord: open it in the lull after a gust (the ridge whistle can be heard through the hole), close it on the next whistle. Two clean draws and the fire catches and the room clears. Opening into a gust blows smoke back: the room coughs, a bark, try the next lull. Cooking teaches fire first.

**Beat 3 — The Lid Ticks (`S03_stew`).** *Objective: Stew the first hare.* Cooking station: joint, brown (short channel), into the pot with the host's barley, roots and salt (EC-13; stores are the host's, no source stated). Then **stew by sound:** a simmer makes the lid tick slowly; a boil rattles it. The player adjusts the pot crane (higher, lower) to keep the slow tick for three ticks of the quest's cooking clock. A boil just means another adjustment. Output: hare stew (EC-13).
- **Crew path:** the host's grandson (role: GRANDSON) minds the pot and calls "rattling!" or "quiet!"; the player works the crane. Cooking XP lower.

**Beat 4 — The Second Hare (`S04_second_hare`).** *Objective: Decide where the second hare goes.* `TFS-D4`. Two hauliers who knocked at dusk are in the porch. TFS.8. On *store*, the player hangs the hare under the smoke-hood (one channel: smoke-cure, EC-13).

**Beat 5 — The Stories (`S05_stories`).** *Objective: Tell your weather story.* The custom (`TFS-D5`). Ketil tells his, the host tells hers, a haulier tells his. Then the player chooses one of four stories (TFS.14). **Delivery:** the player chooses when to say the last line. If they wait for **the hush** (the fire pops, the room goes quiet, ~1 s of silence) the cups bang on the table and the player wins the smoke seat. If they say it early, it still gets a laugh and Ketil's story takes the seat. Either way the room remembers the story (`TFS_STORY`).

**Beat 6 — The Verse (`S06_verse`).** *Objective: Listen to the children's verse.* The children sing (TFS.5). Tova asks the question. `TFS-D6`; `TFS_VERSE_ASKED`.

**Beat 7 — Through the Night (`S07_night`).** *Objective: See the night through.* A **watch** to grey dawn on a bench (per-player hour). The host speaks the closing words of the custom (`TFS-D7`). Quest Completed.

### TFS.5 The verse (presentation spec: unease)

| Time | Element | Spec |
|---|---|---|
| 0 s | Start | Tova stands on a bench; four children join. A clapping rhythm. |
| 0–14 s | The verse | Sung, not glyphed (it is a song, not a call). Text in TFS.14. On "third call's too late" the clapping stops for one beat, as the game requires. |
| 10–14 s | The table | The adults' talk stops. Spoons stop. Ketil looks at the fire. |
| 14–24 s | The old man | The host's father (role: OLD-HAND) puts his cup down, gets up without a word, walks to the door, opens it. Cold and snow-light come in. He looks out into the dark for a long moment. Wind only. He closes the door and sits down again. |
| 24–28 s | Tova | "What's the third call?" (`TFS-D6.01`). |
| UI | No music under the scene except the song; no popup. |
| Meaning | None stated. The verse keeps, as a game, a reply the Wardens dropped after the war (bible §9.4). The old man's look out of the door is habit or memory; nobody says which. It proves nothing and names nobody. TTH can pick it up (`TFS_VERSE_ASKED`). |

### TFS.6 Encounters and hazards

None. The only hazard is smoke in the room (a cough bark) and the gust on the snow shelf (stagger in the open; shelter in the lee of drifts).

### TFS.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_invite` | Find out what First Smoke wants of you. | `TFS-D1` end | Yes | Requires `TH_SEASON` = snow |
| `S01_snowhare` | Bring two snowhares for the pot. | 2 × Hunting recovery on snowhares | Yes | Doubled-track search volumes; crew path via Tova's line |
| `S02_fire` | Get the hearth drawing. | 2 × `smoke_flap` opened in a lull | Yes | Wrong timing: cough bark, retry |
| `S03_stew` | Stew the first hare. | `brown` + `stew` with three slow-tick holds | Yes | Crew path via GRANDSON |
| `S04_second_hare` | Decide where the second hare goes. | `TFS-D4` choice (+ `smoke_cure` on *store*) | Yes | Sets `TFS_HARE` |
| `S05_stories` | Tell your weather story. | `TFS-D5` story choice + delivery | Yes | Sets `TFS_STORY`, `TFS_SEAT` |
| `S06_verse` | Listen to the children's verse. | Verse presentation + `TFS-D6` end | Yes | Sets `TFS_VERSE_ASKED` |
| `S07_night` | See the night through. | `watch` to dawn + `TFS-D7` end | Yes | Quest Completed |

| Flag | Values | Set by | Read by |
|---|---|---|---|
| `TFS_HARE` | pot / store | `TFS-D4` | `TFS-D7`; TSM tally (request); TME01 Nettlehook line |
| `TFS_STORY` | boot / goat / drift / narrows | `TFS-D5` | Nettlehook barks; TRR (request) |
| `TFS_SEAT` | won / ketil | `S05` delivery | Barks only |
| `TFS_VERSE_ASKED` | asked / sang / left | `TFS-D6` | TTH verse variant; Dorn line (request) |

### TFS.8 Choices and consequences

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **In the pot** (`pot`) — *"Both in the pot. The hauliers are in from the cold."* | A full pot. The hauliers eat at the table and one tells the third story (a good one). | One hare less for the deep winter; the host chalks it on the tally board: "one hare, eaten, First Smoke". Ketil frowns at the board. | TME01 at Nettlehook later: the host reads "one hare less, and two hauliers fed". |
| **In the store** (`store`) — *"Smoke the second. It'll be worth more in the dark months."* | The player cures it under the hood; the host chalks "one hare, smoked, the walker's". | The hauliers eat bread and broth by the porch fire; they tell their story from the doorway. Tova takes them her own bowl (bark). | TME01 later: "one smoked hare, the walker's, kept". In deep winter (after TF-M3 Completed) the host bark: "Ate your hare last night. Thank you." |

Neither is wrong. The custom has always argued about it (Part 3: open invitation against count-the-stores-first).

### TFS.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| **Reading fresh snow** | Knowledge | Authored hare and small-game tracks in snow return lines: *"Hare. Going that way."* / *"It doubled back. Look to the side."* |
| Upper longhouse hearth | Access | A public Cooking station (with smoke-hood for curing). |
| Hare stew / smoked hare | Outputs | EC-13; the player keeps a bowl of stew in any outcome (food as recovery). |
| A standing welcome | Standing (local) | Nettlehook hosts greet the player warmly; no mechanical gate. |
| Cooking, Hunting XP | Action XP only | No lump quest XP; no payment (it is a feast, not a job). |

### TFS.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Lost the hare track | The doubled-track search volume re-pins; the hare re-forms in the scrub after a short delay. |
| Smoke blows back | Cough bark; room clears; next lull. |
| Pot boils | Rattle bark; adjust the crane. |
| Story told early | Laugh; Ketil wins the seat. Not a failure. |
| Walking away / logout | Quest stays Active (snow persists); restore to the last step; the hare(s) carried are kept; the pot keeps its progress. |
| Co-op | Each player has their own longhouse scene (per-player NPC placement); fallback: shared scene driven by the host, each player picks their own story and the cups bang for each. Hares are per-player spawns on the shelf. |

### TFS.11 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Doubled hare track | Systems + art | Authored track decals ending in open snow; a search volume that reveals the landing on entry. |
| Smoke-flap timed to wind windows | Systems | Cord interaction; success if used in the lull state of the wind-window timer; room smoke VFX on failure. |
| Stew by lid sound | Systems + audio | Pot state (simmer / boil) moved by crane height; audio tick vs rattle; three holds. |
| Story delivery timing | Systems / dialogue | A dialogue node with a timed "deliver" input during an authored hush cue (fire pop + 1 s silence). Fallback: a choice "wait for the room" vs "say it now". |
| Verse song | Audio | A sung track with children's voices; subtitled. |
| Watch to dawn | Systems | Lowmark keep-watch per-player hour. |
| Tally board chalk lines | Art | Prop swap by `TFS_HARE`. |

### TFS.12 Economy dependencies

EC-12 (snowhare as a food relationship; no pelt), EC-13 (stew, smoked hare), EC-14 (firewood from the host). Barley, roots, salt from the host's store (no source or route stated).

### TFS.13 Mystery ledger entry

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Owner |
|---|---|---|---|---|---|---|
| **What the third call was** | The Third Horn: "heard; someone is still out" (bible §9.4), dropped after the war. | A children's clapping game. | The verse; the old man at the door. | A game about being late for supper. | Everything; TTH owns it. | TTH (the meaning); R06 sealing seeds stay with TF-M5. |

### TFS.14 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Tova Rask** [NEW, bible §5.2], about eleven | The rules of First Smoke; the verse; the snare line. | What the third call is. | Asks the question adults are avoiding. Bossy about customs. |
| **Ketil Rask** [NEW, bible §5.2] | Ropes, worry, stories. | — | Worried about everything except himself; his story is about himself, of course. |
| **Solveig Tarn** [NEW], upper longhouse host | The tally; the hearth; that stores must be counted and guests fed. | — | Brisk, generous, keeps count aloud. |
| **OLD-HAND** (role), Solveig's father | Something about the third call. | — | Says nothing at all in this quest. |

**The rule** (`TFS-D1`)

```
TFS-D1.01 TOVA: "It's First Smoke. First proper winter night. You have to come."
TFS-D1.02 TOVA: "You bring something for the pot and a story. A stupid one. About weather. Something you did wrong."
TFS-D1.03 TOVA: "Best story gets the smoke seat. Dad's never won. He tells the same one."
  > "What should I bring for the pot?"                        → TFS-D1.04
  > "A stupid story. I can manage that."                       → TFS-D1.06
TFS-D1.04 TOVA: "Hares. Up the shelf. My snares are there, the twig flags. They're mine, so ask nicely."   → TFS-D1.06
TFS-D1.06 TOVA: "Hares go into drifts and then they're not anywhere. Look sideways." (beat) "That's free advice."
      {event: TFS-D1 end → completes S00_invite}
```

**Shelf barks**

| Id | Trigger | Line |
|---|---|---|
| TFS-B1.01 | First track inspect | (log) "Long prints ahead of the short ones. It went that way." |
| TFS-B1.02 | Track stops dead | (log) "Tracks stop. Open snow. Nothing beyond." |
| TFS-B1.03 | Landing found | (log) "There. A long jump sideways, into the drift's lee." |
| TFS-B1.04 | Crew path | TOVA "One in already. Reset it like this. Loop, not knot. Knots are for ropes." |

**Hearth barks** (`S02`–`S03`)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TFS-B2.01 | Flap opened in a gust | SOLVEIG | (coughing) "Not while it's blowing. Listen for the whistle to pass." |
| TFS-B2.02 | Clean draw | SOLVEIG | "There she goes. Up and out." |
| TFS-B3.01 | Pot boiling | GRANDSON | "Rattling!" |
| TFS-B3.02 | Slow tick | SOLVEIG | "That's the sound. Like someone tapping to come in." |

**The second hare** (`TFS-D4`)

```
TFS-D4.01 SOLVEIG: "Two hauliers in my porch. Knocked at dusk. Snow on their eyebrows."
TFS-D4.02 SOLVEIG: "One hare's stewed. The other: pot, or the hood? Hood, it keeps till the dark months. Pot, it's tonight."
TFS-D4.03 KETIL: "Count it first. Whatever you do. Count it."
  > "Both in the pot. The hauliers are in from the cold."     → TFS-D4.10
  > "Smoke the second. It'll be worth more in the dark months."   → TFS-D4.20
TFS-D4.10 SOLVEIG: (chalks the board) "'One hare, eaten, First Smoke.' There. Counted, Ketil." 
TFS-D4.11 KETIL: "Counted gone."   {set TFS_HARE = pot}   → end
TFS-D4.20 SOLVEIG: (chalks the board) "'One hare, smoked, the walker's.' Hang it high."
TFS-D4.21 TOVA: (already taking her bowl to the porch) "They can have mine. I had bread."   {set TFS_HARE = store}   → end
```

**The stories** (`TFS-D5`)

```
TFS-D5.01 KETIL: "Year I tied the ropeway car down for a storm. Lovely knots. Tied it to the wrong post." (beat) "Found it in spring. Half a mile down. Knots perfect."
TFS-D5.02 SOLVEIG: "Year I hung the washing out because the sky said fine. The sky meant Hushfold."
TFS-D5.03 HAULIER: "Walked a whole day toward Passwatch in fog. Fog lifted. I was at Passwatch. I'd walked round it twice."
TFS-D5.04 TOVA: "Walker. Yours."
  > "I once tried to outrun a gust to the next shelter. The gust won. It kept my boot."               → TFS-D5.10
  > "Fog so thick I shook hands with someone for an hour. It was a goat. It was a better listener."  → TFS-D5.20
  > "I argued with a snowdrift about which way the path went. I lost. The drift's still there."     → TFS-D5.30
  > [TH_PASSWATCH_ROUTE set] "At the Narrows I thought Dorn's horn was my own stomach. I answered it."   → TFS-D5.40
TFS-D5.10 {set TFS_STORY = boot; delivery prompt: "...It kept my boot."}
TFS-D5.20 {set TFS_STORY = goat; delivery prompt: "...It was a better listener."}
TFS-D5.30 {set TFS_STORY = drift; delivery prompt: "...The drift's still there."}
TFS-D5.40 {set TFS_STORY = narrows; delivery prompt: "...I answered it."}
      (delivery in the hush → TFS-D5.50; early → TFS-D5.60)
TFS-D5.50 (cups bang on every table) SOLVEIG: "Smoke seat. Walker. Shift, Ketil."
TFS-D5.51 KETIL: "Every year." (shifts)   {set TFS_SEAT = won}   → end
TFS-D5.60 (laughter; then Ketil's cup bangs alone, then everyone's) SOLVEIG: "Ketil. Finally. For the wrong post."
TFS-D5.61 KETIL: (stunned) "...Every year I tell it." (sits on the cushion) "It's a good post."   {set TFS_SEAT = ketil}   → end
```

**The verse** (sung, `S06`)

```
One for the gather, two for the gate,
Wind at the window, supper's on the grate.
Long for the lost one, short for the near,
Third call's too late, and nobody's here.
(clap, clap, stop.)
```

```
TFS-D6.01 TOVA: (still on the bench, watching the old man sit down again) "What's the third call?"
TFS-D6.02 SOLVEIG: "It's a song, Tova."
TFS-D6.03 TOVA: (to the player, because adults are useless) "It's a call. It says it's a call."
  > "I don't know. I'd like to."                               → TFS-D6.10
  > "Sing it again. I'll listen properly."                      → TFS-D6.20
  > (say nothing)                                               → TFS-D6.30
TFS-D6.10 TOVA: "Dorn knows. Dorn knows every call. Ask Dorn." (beat) "He won't tell me."   {set TFS_VERSE_ASKED = asked}   → end
TFS-D6.20 (Tova sings it alone, slower; on "third call" she does the stop and looks at the door)  {set TFS_VERSE_ASKED = sang}   → end
TFS-D6.30 TOVA: "Nobody ever says." (sits)   {set TFS_VERSE_ASKED = left}   → end
```

**Through the night** (`TFS-D7`, grey dawn)

```
TFS-D7.01 SOLVEIG: (at the door, which she opens) "Through." (beat) "That's First Smoke said."
TFS-D7.02 [TFS_HARE = pot] SOLVEIG: "Hauliers are gone already. Left the porch swept. That's thanks, up here."
TFS-D7.03 [TFS_HARE = store] SOLVEIG: "Your hare's on the hook. I'll say whose it was when we eat it."
TFS-D7.04 [TFS_SEAT = won] KETIL: "Next year I'm telling a new one. I'm not. But I'm saying I am."
TFS-D7.05 SOLVEIG: "The hearth's yours when you're passing. Bring something for the pot. You know how."
      {event: TFS-D7 end → quest Completed}
```

**Inspect texts**

| Object | Text |
|---|---|
| Smoke-flap cord | "A cord to the flap over the smoke-hole. The wind can be heard through it." |
| Smoke seat | "A stool with a worn cushion, nearest the fire. Hotly contested." |
| Tally board | "Beds, food, who's expected. Chalked tonight." / with `TFS_HARE`: the chalked hare line. |
| The door | "Heavy. Snow on the step. Outside, the dark and the ridge." |

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| NETTLEHOOK CHILD | "You're the boot one." / "You're the goat one." / "You're the drift one." / "You answered your stomach." | `TFS_STORY` |
| TOVA | "I asked Dorn. He went quiet. Grown-ups go quiet at it." | `TFS_VERSE_ASKED` = asked, TTH not started |
| HAULIER (Passwatch) | "Nettlehook fed us at First Smoke. Hare. Real hare." | `TFS_HARE` = pot |

### TFS.15 Open decisions

1. **Verse text** is authored here. The sister package (TTH) is asked to quote it as written (request).
2. Story delivery timing is a small new dialogue feature; fallback documented.
3. Solveig Tarn is new; TME01's Nettlehook host may be the same person (recommended).

### TFS.16 Review log

| Finding | Revision |
|---|---|
| First draft's wonder was dawn smoke from every chimney. | Cut: TSM owns a smoke moment. Replaced with the verse and the old man at the door, plus the small wonder of tracks that stop. |
| "Best story wins" risked a wrong answer. | Every story is fine; timing decides the seat, and losing gives Ketil his first win, which is its own joke. |
| The verse could over-explain the Third Horn. | It says "third call's too late, and nobody's here": a distortion. Nobody explains it; the old man says nothing. |
| Who-eats choice repeated Lowmark FK. | Moved to now-or-store, which teaches two Cooking relationships and the Part 3 argument. |

---

## TBC — The Bridge That Chose

### TBC.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `thornfell.side.bridge_that_chose` |
| Type | Settlement (Windscar), Smithing. Bible §7.2 brief. |
| Unlock | TF-M1 Completed. Offered by Aud's bark at the Passwatch-side bridgehead of the Narrows after a storm (any visit after TF-M1). The cracked state is per-player and shows **only while TBC is Active**; the scree path is walkable regardless (Zones §6.2). |
| Resume hook | Aud Hammerlee at her field forge: "Bridge is still broken. I've been swearing at it in your absence." |
| Skills | Smithing (required), Melee (light) |
| Combat share | ~10% (two pass bandits at the bridgehead, they yield) |
| Choice | Who waits for dawn (the family and its goats, the Wardens' mule train, or the grain sledge); whether the repair post names who waited |
| Unlocks | Reading a break; Aud's field forge as a public Smithing station; Aud as a future commission giver |
| **Anchor** (§7.1) | The Windscar bridge crews (Aud Hammerlee) and the people who wait at the Narrows: shieling families, Ridge Warden escorts, highstead sledgers. |
| **World-truth row** | Present pressure: closures (H25) and the closure practice of TD-5 ("nobody records who is outside"). H16 only as an old woman's memory. Part 4 braid 2 (a repair credited twice) as an optional Lowmark variant. |
| **Revelation role** | Supports the R06 (sealing) misunderstanding ladder as a seed only: a public board that names who waits, beside Vessa's "we write what we closed, not who" (TF-M1). Owns nothing; reveals nothing. |
| **Recurring evidence** | None. Aud recurs from TF-M1 (person, no evidence role). The repair post is a prop, never evidence. |
| **State compliance** | Inactive / Active / Completed. `TBC_WAITS`, `TBC_WAIT_NAMED`. Every load crosses by dawn in every outcome; nobody is lost; no clock can run out (the windows wait for the player's plan). |

**In one paragraph.** A storm has gone through the Windscar Narrows and split the far anchor rock, and the span that the player helped patch in the Closing of Passwatch is hanging by its guide line again. On the far side, at Three Calls Shelter, two shieling families are coming down for winter with children, an old woman and a string of goats. On the Passwatch side, a Ridge Warden escort waits with a mule train of lamp oil and salt for the far horn posts, and a highstead's grain sledge. Aud Hammerlee swears at rope affectionately and puts the player to work. They read the sheared eye-bolt and see it had been cracking for years before the storm finished it. They sound the far rock for a fresh seat. At Aud's field forge they hammer new fittings while the iron sings and put them back in the fire when it starts to clack. Then the hard part: the storm's back half gives three wind windows before dark, two long and one short, and the mended span carries one heavy load in a long window or two light ones in a short. Four loads, three windows. The player chalks the plan on a board at the bridgehead where everyone can read it, and somebody's name goes in the last row: *waits for dawn*. In the short window, snow in the gap falls upward. At the end, Aud cuts the repair post: who mended. The player decides whether it also says who waited.

### TBC.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| A. Repeat TF-M1's build-and-escort with a harder clock. | Rejected. Same verb as the milestone. |
| B. A single "who crosses first" dialogue choice. | Rejected. TF-M1 already has that choice; TBC must be a plan, not a pick. |
| **C. Read the failure → forge by ear → a public, readable crossing plan with wind-window logic → account** (selected). | **Selected.** Smithing as cause and craft; triage as a puzzle everyone can see; the account as Thornfell's closure idea in miniature. |

| Element | Source | Status |
|---|---|---|
| The Narrows rope bridge over a landslide gap | Bible TP07 | [NEW on CANON feature] |
| Aud Hammerlee, swears at rope affectionately | Bible §5.2 | [NEW] |
| Three Calls Shelter across the Narrows | Bible TP06, route order §4.2 | [NEW, Part 3] |
| Closure practice: nobody records who is outside | Bible TD-5 | [PROPOSAL — DIRECTOR] |
| Pass bandits (cutter, slinger) at blind corners | Bible §10 | [CANON] family |
| A repair credited twice (braid 2) | Part 4 relationship web | Proposal; optional variant only |
| Lowmark NB *Night Bridge* repair credits | `Caelmor_Lowmark_Side_Quests_Settlements_and_Combat.md` NB.7 | Lowmark authored; read-only |

### TBC.3 The place [MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling |
|---|---|---|
| A. Passwatch-side bridgehead | Hub; board | The near anchor, Aud's field forge (hearth, anvil, bellows, quench bucket), the mule train under tarps, the grain sledge with its sledgers. A blank slate board on two posts. The **repair post**: a squared timber carved with old repair marks. |
| B. The span | Traversal | Rope span, deck slats, guide line. Hanging slack from the far end. |
| C. Far anchor rock | Reading | The rock split by a fresh crack. The old eye-bolt sheared at the seat. Two other candidate seats chalked by Aud's crew last spring. |
| D. Three Calls side | Waiting | The two families, children on packs, the old woman (role: GRANDMOTHER) on a bundle, goats on a line. The shelter's guest ledge behind them. |
| E. The gap | Wonder | The landslide gap below the span. In a lull, updraft. |

The far rock is reached by the guide line (agility traverse) or the fallback: Aud's crew's bosun chair on the guide line, hauled (slower; no input needed but a "heave" call).

### TBC.4 Beats

**Beat 0 — Cracked Again (`S00_crack`).** *Objective: Find out what the storm broke.* `TBC-D1` with Aud (variant by `TH_PASSWATCH_ROUTE`).

**Beat 1 — Read the Break (`S01_read`).** *Objective: Read the broken fitting and find sound rock.* Cross to the far rock (guide-line traverse or bosun chair). Inspect the sheared eye-bolt: two faces on the break, a dull grey part with faint curved lines (an old crack that grew a little every storm) and a bright, grainy rim (where it finally let go). Then **sound the rock** (shared interaction, §0.6) at three candidate seats: one returns doubled (the new crack runs under it), two return flat. Aud picks one of the flat two with the player.

**Beat 2 — Forge by Ear (`S02_smith`).** *Objective: Forge the new fittings.* Smithing at the field forge: two eye-bolts and two shackles (EC-02 stock from Aud, EC-03 output, EC-14 fuel).
- **Heat** in the hearth (channel; the player works the bellows).
- **Hammer** on the anvil: each strike plays a note. **While the iron is hot enough it rings, a singing note. As it cools, the note goes dead: a clack.** On the clack, back to the fire. Striking on a clack shows a hairline at the edge (bark; reheat closes it at this level; nothing fails).
- **Shape** (three strike-sets per fitting), **punch** the eye (one channel), **quench** (one interaction).
- **Crew path:** Aud's striker (role: STRIKER) swings while the player works the bellows and calls **ring** (keep going) or **clack** (back to the fire) on each strike. Cost: the striker's wage comes out of the player's payment. Smithing XP lower.

**Beat 3 — Set the Seat (`S03_set`).** *Objective: Set the fittings in the far rock.* Drive the two eye-bolts into the chosen seat with wedges (two channels), shackle the span lines (two interactions), then tension: Aud's crew heaves on the player's call, **heave** only in the lull after a gust (the whistle tells). A heave in a gust just slips back a notch.

**Beat 4 — The Board (`S04_board`).** *Objective: Chalk a crossing plan the waiting can read.* `TBC-D4` sets the puzzle. Aud counts the whistles off the face: **three windows before dark: long, short, long.** The mended span takes **one heavy load in a long window, or two light loads in any window. Heavy loads cannot go in the short window.** Loads: Family A (light), Family B with GRANDMOTHER (light), Family B's goats (heavy; the family will not leave them, so if the goats wait, Family B waits too, which is a light load moved to dawn), the Warden mule train (heavy), the grain sledge (heavy). The board is a slate with three window rows and a fourth row, **waits for dawn**. The player drags chalk tokens into rows. Aud rejects an impossible plan with a dry line (a heavy in the short row; two heavies in one row). Valid plans always put both families in the short window (or Family A plus Family B's people if goats wait) and two of the three heavy loads in the long windows: **one heavy load waits for dawn.** That is the choice (TBC.8). The board stays up, readable by everyone; each group barks its reaction to its row (TBC-B4). The GRANDMOTHER reads it (unease, `TBC-D4.20`).

**Beat 5 — The Crossings (`S05_cross`).** *Objective: Get each window's load across.* Three windows play in order. The player walks each load across (escort-lite: loads move only in the lull, stop on the whistle). In the **short window**, the strange moment plays (TBC.5). In the second long window, two pass bandits come up from the Blind Corners to cut a load's lead line in the confusion (TBC-E1); they yield. Nobody can fall: loads stop and hold on the whistle.

**Beat 6 — The Account (`S06_account`).** *Objective: Help Aud cut the repair post.* `TBC-D6`/`D7`. Aud carves who mended. Optional Lowmark callback (`TBC-D7` variants). The choice to add who waited (`TBC_WAIT_NAMED`).

**Beat 7 — Dawn (`S07_dawn`).** *Objective: See the last load over at dawn.* A **watch** to dawn at the bridgehead fire (per-player hour). The waiting load crosses in the first long window of the morning. `TBC-D8`. Quest Completed; `TBC_AUD_BENCH`.

### TBC.5 Snow in the gap (presentation spec: wonder)

| Time | Element | Spec |
|---|---|---|
| 0 s | Trigger | The short window's lull begins with the families on the span. |
| 0–3 s | Stillness | The gust drops. The span stops swaying. |
| 3–12 s | The snow | In the gap below and around the span, falling snow slows, hangs, and then **drifts upward**, past the deck, past the children's faces, toward the sky, in an updraft from the gap. Outside the gap, snow falls normally. |
| 5–12 s | People | A child reaches out and catches a flake going up. The GRANDMOTHER stops and watches it. Nobody says anything. |
| 12–14 s | End | The whistle; the snow falls normally again; the crossing resumes. |
| UI | No popup, no music. Wind and rope creak only. Autumn variant: rain and spray rise instead. |
| Meaning | Air rising out of a deep cut in a lull. Nothing else. Aud's line afterwards: "Gap does that. Don't tell the Wardens, they'll want to regulate it." |

### TBC.6 Encounters and hazards

| Id | Enemies / hazard | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TBC-E1** | 1 × Pass Bandit (cutter), 1 × Pass Bandit (slinger) | Passwatch-side bridgehead, during the second long window | Cutter goes for the waiting load's lead line (an interaction he channels, ~4 s); slinger covers from the switchback | **Cutter:** knife drawn and a crouch at the line (~1.0 s) before he starts cutting; any hit interrupts. **Slinger:** whirls the sling overhead (~1.2 s), then a stone | Readable pressure while a plan is running | 40–60 s. They yield (TD-7). If the line is cut, Aud ties it again (bark); nothing is lost |
| **TBC-H1** | Gust on the span | Span | Wind window | Whistle (~3 s) | Loads stop; the player holds the guide line | Stagger only; the guide line keeps everyone on |
| **TBC-H2** | Forge spark | Anvil | Environmental | A bright spit on the strike after a clack | Teaches the clack | Cosmetic sting, no damage |

Defeated bandits are tied to the bridgehead posts and taken to Passwatch by the Warden escort at dawn. Combat reveals nothing. Death: respawn at the field forge; fittings forged and set stay set; windows already run stay run.

### TBC.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_crack` | Find out what the storm broke. | `TBC-D1` end | Yes | |
| `S01_read` | Read the broken fitting and find sound rock. | Eye-bolt inspect + 3 × `sound_rock` + `TBC-D2` end | Yes | Traverse or bosun chair |
| `S02_smith` | Forge the new fittings. | 2 eye-bolts + 2 shackles complete (or crew path) | Yes | Sets `TBC_CREW_FORGE` on crew path |
| `S03_set` | Set the fittings in the far rock. | 2 × `drive_bolt`, 2 × `shackle`, 3 × `heave` in lulls | Yes | |
| `S04_board` | Chalk a crossing plan the waiting can read. | Valid board submitted + `TBC-D4` end | Yes | Sets `TBC_WAITS` |
| `S05_cross` | Get each window's load across. | Three window crossings complete; TBC-E1 defeated | Yes | Strange moment in the short window |
| `S06_account` | Help Aud cut the repair post. | `TBC-D7` choice | Yes | Sets `TBC_WAIT_NAMED` |
| `S07_dawn` | See the last load over at dawn. | `watch` + dawn crossing + `TBC-D8` end | Yes | Sets `TBC_AUD_BENCH`; quest Completed |

| Flag | Values | Set by | Read by |
|---|---|---|---|
| `TBC_CREW_FORGE` | bool | `S02` crew path | `TBC-D7` line; payment |
| `TBC_WAITS` | family / mules / sledge | `S04` board | Barks; dawn presentation; TRR (request) |
| `TBC_WAIT_NAMED` | bool | `TBC-D7` | Repair post prop; TF-M5 Aud line (request); TTH (request) |
| `TBC_AUD_BENCH` | bool | `S07` | Master commissions |

### TBC.8 Choices and consequences

**Who waits for dawn** (`TBC_WAITS`, set by the board):

| Plan leaves waiting | Immediate result | Cost | Later |
|---|---|---|---|
| **Family B and its goats** (`family`) | Mules and sledge cross; Family A crosses in the short window. Family B, the GRANDMOTHER and the goats sleep in Three Calls Shelter. | An old woman spends one more night on a guest ledge in the cold; the children cry about it. | Family B crosses at dawn; the GRANDMOTHER pats the post as she passes. |
| **The Warden mule train** (`mules`) | Families and sledge cross. | The far horn posts go one night without lamp oil; the escort corporal stands at the board, reading it twice. | Warden bark at Passwatch: "Far posts dark one night. Board said so. Fair enough." |
| **The grain sledge** (`sledge`) | Families and mules cross. | A highstead eats a day late; the sledgers sleep beside the sledge under guard. | Sledger bark: "We ate the board's dust. One day. We'll live." |

**The account** (`TBC_WAIT_NAMED`, set at `TBC-D7`):

| Option | Result | Cost |
|---|---|---|
| **Name who waited** — *"Cut who waited, too. And why."* | The post carries the mended line and a second: who waited for dawn and the window that wasn't there. | Aud: "Wardens write loads, not people. They'll have words with me." (They do; bark.) |
| **The work only** — *"Who mended. That's what the post is for."* | The post carries the mended line only, as always. | The GRANDMOTHER (or the waiting group's speaker) looks at the post and says nothing (`TBC-D7.40`). |

No plan and no account option is wrong. Every load crosses.

### TBC.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| **Reading a break** | Knowledge | Authored broken fittings, tools and blades across Thornfell return a line: *"Old crack. It's been going for years."* / *"Bright all through. It went at once."* |
| Aud's field forge | Access | Public Smithing station at the Narrows bridgehead. |
| Smithing by ear | Knowledge | After TBC, forging anywhere plays the ring/clack cue. |
| Small payment | Currency | From Aud and the escort corporal; the striker's wage out of it on the crew path. |
| Smithing, Melee XP | Action XP only | No lump quest XP. |

### TBC.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Invalid board plan | Aud rejects it with a line; the player re-chalks. |
| Load caught by a gust | It stops and holds; resumes in the next lull. |
| Lead line cut by a bandit | Aud reties it; the load resumes. |
| Striking on a clack | Spark, hairline; reheat closes it. |
| Walking away mid-plan | Quest stays Active at the step; the windows wait (they are per-player presentation, not world time). Resume hook at the forge. |
| Logout | Restore last step; forged fittings and set seat persist; completed windows persist. |
| Co-op | Bridge state per player (cracked or mended). Fallback: the host's state drives the bridge; each player chalks their own board in dialogue and their own `TBC_WAITS`; the visible board shows the host's plan. Bandits shared, credit to all present. |

### TBC.11 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Ring/clack forging | Systems + audio | Workpiece temperature as a timer; strike audio switches from ring to clack below a threshold; striking on a clack plays a spark and adds a reheat. |
| Crossing board puzzle | UI + Systems | A slate with three rows plus *waits*; draggable tokens (light/heavy); validation rules as listed; a valid plan sets `TBC_WAITS`. Fallback: a dialogue choice of "which heavy load waits" with the board as a prop written accordingly. |
| Window sequence (long, short, long) | Systems | Authored wind-window pattern for this quest, per player. |
| Escort-lite loads | Systems / NPC | Group movers on the span spline that stop on the whistle. |
| Updraft snow | VFX | Local particle override inside the gap volume for ~9 s. |
| Repair post carving | Art | Prop swap with one or two lines by `TBC_WAIT_NAMED`. |
| Lowmark state read | Schema | Read `lowmark.side.night_bridge` Completed and its `NB_*` outcome flag for variant lines only. |
| Cracked-bridge state | 33.1.B2 | Per-player bridge state: cracked only while TBC is Active, mended on Completed; scree path walkable regardless (Zones §6.2, canonical). |

### TBC.12 Economy dependencies

EC-02 (bar stock; plain carbon steel stock recommended), EC-03 (fittings, installed), EC-14 (forge fuel). The lamp oil, salt and grain in the waiting loads are presentation only (no source or route stated: FT-03).

### TBC.13 Mystery ledger entry

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Owner |
|---|---|---|---|---|---|---|
| **"The bridge that chose"** | A local saying since the war: a bridge that can carry only some is said to "choose". Nobody remembers who first said it. | Bridges are lucky or unlucky. | The saying; the GRANDMOTHER's memory of an unchalked closing. | A real bridge spirit. (Aud: "Bridges don't choose. People choose and blame the rope.") | Which closing the GRANDMOTHER means. | None here; TF-M5 owns the sealing truth. |

### TBC.14 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Aud Hammerlee** [NEW, bible §5.2], master bridgewright | Every fitting on the Narrows; what TF-M1's patch was worth; that bridges fail slowly and then at once. | Anything of the war beyond old crews' talk. | Swears at rope affectionately. Practical, fast, fond of the player in the way of someone who has seen them work. |
| **GRANDMOTHER** (role), Family B | One old closing she was on the wrong side of. | Which one, by date; she was young. | Short sentences, no complaint; that is the complaint. |
| **CORPORAL** (role), Warden escort | Loads, the far posts, the rule. | — | Vessa Galt's school: dry, rule-bound, dislikes the rule. |
| **STRIKER** (role) | Hitting things. | When to stop. | Cheerful. |

**Cracked again** (`TBC-D1`)

```
TBC-D1.01 AUD: (to the hanging span) "You stupid, beautiful, ungrateful thing."
TBC-D1.02 [TH_PASSWATCH_ROUTE = sledge] AUD: "Walker. Last time you sent Nettlehook's sledge over first. They still send you their swearing, kindly."
TBC-D1.03 [TH_PASSWATCH_ROUTE = caravan] AUD: "Walker. Last time you sent the caravan. Market ate, Nettlehook ate late. Nobody's forgotten either."
TBC-D1.04 [TH_PASSWATCH_ROUTE = split] AUD: "Walker. Last time you split the loads. Half of everybody was cross with you. Good work."
TBC-D1.05 AUD: "Storm split the far rock. The eye-bolt went with it. Families on that side, Wardens and grain on this one, and everyone's looking at me."
  > "What do you need?"                                       → TBC-D1.06
  > "Didn't we just fix this?"                                → TBC-D1.07
TBC-D1.06 AUD: "Hands, iron, and someone to take the blame for the order. You'll do for all three."   → TBC-D1.08
TBC-D1.07 AUD: "We fixed the span. The rock didn't get a vote." (beat) "Come and look at what broke."   → TBC-D1.08
TBC-D1.08 AUD: "Over the guide line, or in the chair. Chair's slower. Chair's dignified."
      {event: TBC-D1 end → completes S00_crack}
```

**The break** (`TBC-D2`, far rock, after the inspect and soundings)

```
TBC-D2.01 AUD: "See the grey part? Lines in it, like a shell? That's been cracking for years. A little every storm."
TBC-D2.02 AUD: "Bright bit's this storm. It just finished the job."
TBC-D2.03 AUD: "And that seat comes back doubled. Crack runs under it. These two?"
  > "Flat. Both."                                                → TBC-D2.04
TBC-D2.04 AUD: "Then we take the left. It's further from where I'm standing, and I'm standing on the crack."
      {event: TBC-D2 end → S02_smith active}
```

**Forge barks**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TBC-B2.01 | First heat | AUD | "Hit it while it sings. When it goes dead, it's had enough. Back in." |
| TBC-B2.02 | Strike on a clack | AUD | "Hear that? Like hitting a table. It'll crack. Back in the fire." |
| TBC-B2.03 | Crew path, correct "clack" | STRIKER | "Back in she goes." |
| TBC-B2.04 | Crew path, late call | STRIKER | (spark) "Ooh. That's a mark. Never mind. Fire fixes it." |
| TBC-B2.05 | Fittings done | AUD | "Better than the old ones. Don't tell the old ones." |
| TBC-B3.01 | Heave in a gust | AUD | "It slipped. Wind's got its weight on it. Wait for the lull." |
| TBC-B3.02 | Span tensioned | AUD | "There. Now she'll carry. Not everything. Something." |

**The board** (`TBC-D4`)

```
TBC-D4.01 AUD: (counting whistles off the face, lips moving) "Three before dark. Long. Short. Long."
TBC-D4.02 AUD: "One heavy in a long window. Two light in any. Nothing heavy in the short one or we're all swimming."
TBC-D4.03 AUD: "Two families, light. The goats, heavy, and they won't leave their goats. Mules, heavy. Sledge, heavy."
TBC-D4.04 AUD: (hands the player the chalk) "Somebody waits for dawn. Write it where they can read it. People take waiting better when they can see it."
      {board puzzle opens}
(invalid plan) TBC-D4.05 AUD: "That's three heavies in two windows. That's a river."   → board
(invalid plan) TBC-D4.06 AUD: "Heavy in the short. No."   → board
(valid plan) TBC-D4.10 AUD: (reads it) "Right. That's the plan. Everyone can see it. Everyone can hate it equally."
      {set TBC_WAITS per board}   → TBC-D4.20
TBC-D4.20 GRANDMOTHER: (from the far side, reading across the gap, slowly) "'Waits for dawn.'"
TBC-D4.21 [TBC_WAITS = family] GRANDMOTHER: "That's us." (beat) "Well. It's written."
TBC-D4.22 GRANDMOTHER: "Last time they closed a crossing on me, I was a girl. Nobody chalked anything. We just stood there till we understood."
TBC-D4.23 AUD: (quietly) "...Bridges don't choose. People choose. Then they blame the rope."
      {event: S04_board complete}
```

**Board reaction barks** (each group reads its row)

| Id | Group | Row | Line |
|---|---|---|---|
| TBC-B4.01 | Family A | Short window | "Short one. With the children. Hold hands, then." |
| TBC-B4.02 | CORPORAL | Long window | "Mules second. Noted." |
| TBC-B4.03 | CORPORAL | Waits | "Far posts dark one night. It's on the board. Fair enough. I don't like it. Fair enough." |
| TBC-B4.04 | SLEDGER | Waits | "Dawn. We'll eat snow and opinions." |
| TBC-B4.05 | SLEDGER | Long window | "First over? Don't let the mules hear." |

**Crossing barks**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| TBC-B5.01 | Whistle during a crossing | AUD | "Hold! Hands on the line. Let it blow." |
| TBC-B5.02 | After the updraft | AUD | "Gap does that. Don't tell the Wardens, they'll want to regulate it." |
| TBC-B5.03 | E1 starts | CORPORAL | "Corner lads. Off the switchback. Mind the line!" |
| TBC-B5.04 | Cutter yields | BANDIT | "Fine! Fine. I wasn't going to cut it. Much." |
| TBC-B5.05 | Line cut (if it happens) | AUD | (retying) "I've tied worse in my sleep. I have tied worse in my sleep." |

**The post** (`TBC-D6`, `TBC-D7`)

```
TBC-D6.01 AUD: (knife to the repair post) "Who mended. Always. Crews, strikers, anyone who held the line."
TBC-D6.02 [TBC_CREW_FORGE] AUD: "Striker, for the hammer. You, for the ear."
TBC-D6.03 AUD: "The Hushfold lad who held the guide line in the second gust. Nobody asked him. He held it."
TBC-D6.04 AUD: "And you. Walker." (cuts) "Spell it later."
      → TBC-D7.01
TBC-D7.01 AUD: "That's the mended line. That's what the post's for."
  > "Cut who waited, too. And why."                                       → TBC-D7.10
  > "Who mended. That's what the post is for."                           → TBC-D7.30
  > [lowmark.side.night_bridge Completed] "In Lowmark they write repair credits by the bridge stone."   → TBC-D7.50
TBC-D7.10 AUD: "Who waited." (knife stops) "Wardens write loads, not people. They'll have words with me."
TBC-D7.11 AUD: (cuts anyway) "'Waited for dawn: ...' and the window that wasn't there."
TBC-D7.12 GRANDMOTHER (or the waiting group's speaker, by TBC_WAITS): "There. Now somebody'll know we stood here."
      {set TBC_WAIT_NAMED = true}   → TBC-D7.60
TBC-D7.30 AUD: "Work only. Like always." (cuts)
TBC-D7.40 GRANDMOTHER (or the waiting group's speaker): (looks at the post a while; says nothing)
      {set TBC_WAIT_NAMED = false}   → TBC-D7.60
TBC-D7.50 AUD: "Do they." (interested) "Who gets written?"
TBC-D7.51 [NB_BOTH_CREDIT] PLAYER: "Everyone who mended it. Two families who never liked each other, on the same stone."
TBC-D7.52 [NB_BOTH_CREDIT] AUD: "Both hands. Good. Ours too, then. Everyone who held something."
TBC-D7.53 [NB_ALL_PAY] PLAYER: "Nobody, in the end. Everyone pays a toll toward the next repair."
TBC-D7.54 [NB_ALL_PAY] AUD: "Sensible. Pays for rope. Doesn't remember anybody, though."
TBC-D7.55 [NB_WICKETT_CREDIT] PLAYER: "One family. The ones who patched it when nobody else would."
TBC-D7.56 [NB_WICKETT_CREDIT] AUD: "One remembered. Better than none. Worse than all."
TBC-D7.57 AUD: "Old crews tell it that Windscar hands mended a river crossing once, after the war. Somebody wrote it in their book. Somebody else wrote it in theirs, different." (beat) "I don't know which river. Nobody does. That's the point of a post."
      → TBC-D7.01 options (without the Lowmark option)
TBC-D7.60 AUD: "Now. Dawn. Somebody's still waiting."
      {event: S06_account complete}
```

(TBC-D7.57 is [PROPOSAL — DIRECTOR]: hearsay from old crews, Part 4 braid 2. It names no river, crossing, route or year and gives no individual a journey.)

**Dawn** (`TBC-D8`)

```
TBC-D8.01 AUD: (watching the waiting load come over in the first morning window) "There. Everyone. Late, and over."
TBC-D8.02 [TBC_WAITS = family] GRANDMOTHER: (pats the post as she passes) "Mended."
TBC-D8.03 [TBC_WAITS = mules] CORPORAL: "Far posts'll be lit tonight. Board was right. I'll say so. Once."
TBC-D8.04 [TBC_WAITS = sledge] SLEDGER: "Day late. Still bread. Thank the rope."
TBC-D8.05 AUD: "One day there'll be a span for the far gate worth building. When there is, I'll want you on the hammer."
TBC-D8.06 AUD: "Forge is here. Use it. Swear at it. It likes that."
      {set TBC_AUD_BENCH; payment; event: TBC-D8 end → quest Completed}
```

**Inspect texts**

| Object | Text | Condition |
|---|---|---|
| Sheared eye-bolt | "Two faces on the break. Dull grey with faint curved lines: an old crack, growing. A bright grainy rim: where it finally went." | — |
| Repair post | "Old cuts: crews' marks, a few names, dates. Who mended. Never who waited." | Before `S06` |
| Repair post | "A new line: who mended. And under it: who waited for dawn, and why." | `TBC_WAIT_NAMED` |
| Repair post | "A new line: who mended." | not `TBC_WAIT_NAMED` |
| The board | "Three rows and one more. 'Waits for dawn.' Everyone can read it from either side." | After `S04` |
| The gap | "A long way down. In a lull, the air comes up it." | — |

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| AUD | "Wardens had words. I had more." | `TBC_WAIT_NAMED` |
| CHILD (Three Calls) | "The snow went up. I caught one. It was going home." | Any |
| CORPORAL (Passwatch) | "Narrows has a board now. Aud says it's yours. I say it's useful. Don't tell her." | Any |

### TBC.15 Open decisions

1. **Braid 2 callback** (`TBC-D7.50`–`.57`) is optional and reads Lowmark NB state only. If the Director prefers no Lowmark read in Thornfell side content, delete those nodes; nothing else changes.
2. **TD-5:** the post's "who waited" line is a small local practice, not the Assembly's closure account (TF-M5 adopts that). Act III author may echo it (request: one Aud line at the Assembly if `TBC_WAIT_NAMED`).
3. **EC-02 stock:** recommend plain carbon steel stock for parity; ridge iron only if EC-01 lands.
4. **Resolved (Zones §6.2):** the Narrows has one per-player state machine; TBC shows it cracked only while TBC is Active; TRR's permanent span applies regardless of TBC.

### TBC.16 Review log

| Finding | Revision |
|---|---|
| Risk of repeating TF-M1's "who crosses first". | TBC is a plan with window logic everyone can read; the choice emerges from the board, and it is about who *waits*, not who goes. |
| A load could be lost to a gust or a bandit. | Loads stop and hold on the whistle; a cut line is retied. Every load crosses by dawn. |
| Early wonder was a singing span. | Cut: TNR owns the singing cable and TRR the Narrows chord. Replaced with updraft snow. Echo at the Narrows avoided (TTH owns it). |
| GRANDMOTHER's memory could reveal R06. | She names no closing, date or place; it supports the misunderstanding ladder only. |
| Lowmark callback risked a route claim. | Aud names no river, crossing or direction; it is hearsay and optional. |
| Cracked state ran "after TF-M1 until TBC completes", showing a broken bridge to players who never took TBC (Batch 4 review, Zones Z-1). | Cracked only while TBC is Active; offered by Aud's bark; scree path walkable regardless (TBC.1, TBC.11, open decision 4). |

---

## Cross-quest integration summary

| Need | Quests | Owner | Minimum viable form |
|---|---|---|---|
| Step-level objectives and flags | All | Schema & Content Engineer, Systems Engineer (31.3, 24.1) | Lowmark step shape; `S00_…` ids; quest-local flags only. |
| Dialogue with flag, item-held and Lowmark-state conditions | All | 31.5 | "Has no tool" conditions recur (TSR, TST, TGY). TBC reads NB state. |
| **Sound-the-rock** interaction with beat-dots | TSR, TBC (and TF-M3) | Systems + audio | One shared interaction; authored returns per face tag. |
| Wind-window timer driving audio, channels and NPC movement | TST, TGY, TFS, TBC | Systems | The bible §9.5 timer, exposed as lull / whistle / gust states to interactions. |
| *call-blown* event | TGY | Systems | As the sister package. |
| Keep-watch per-player hour | TGY, TFS, TBC | Systems | Lowmark convention. |
| Craft stations | TST (bench), TGY (shed chain), TFS (hearth, hood), TBC (field forge) | 33.5 station binding | Each persists after its quest as a public workspace. |
| Hunting hooks | TGY, TFS | Hunting interaction pass | Approach, resolve, recover; wind-scent tie to the timer (fallback volumes). |
| Ranged with wind drift | TST (S01 proposal layer only) | Combat / Ranged system | Not needed by the default build (TST.15). |
| Per-player persistent props | All | 33.1.B2 | Fallbacks listed in each package. |
| Encounters | TSR (Rock Vipers, first appearance), TST (wolves with howl interrupt), TBC (bandits) | Encounters package | Telegraphs as listed. |
| Economy states and recipes | All | Economy and item passes | EC-01 to EC-14 (§0.3). |

## Open questions for the Director and other passes

1. **TD-13 and the economy pass.** None of EC-01 to EC-14 exists as an item. Each quest is written to stand with coin, knowledge and station access if the economy pass derives nothing. Priority for derivation: EC-02 (steel stock for TBC, likely already covered), EC-09/EC-10 (hide and leather, near Lowmark states), EC-12/EC-13 (food), then EC-04 to EC-08 (bow chain, blocked by S01), then EC-01 (ore, a new hard-material decision).
2. **S01 (ranged scope).** The bible asks TST for a first Ranged weapon; the economy set says no ranged concept enters v1 while S01 is open. TST now builds its fallback by default (racked stave, lull-calling); the bow and Ranged lesson are [PROPOSAL — DIRECTOR] gated on S01.
3. **Rock Vipers' first appearance** moves to TSR for players who take it before TF-M3 (TSR.15).
4. **New names** [NEW]: Brita Crane, Bera Scree, Dagny Grell, Tormod Lisk, Solveig Tarn; highsteads Kettlecrag and Brackenstep (off-map, unplaced). None collides with the sister package's names.
5. **Deliberately unexplained** (add to bible §7.4's list if accepted): the sixth cellar at Red Slope; the moaning stumps; the goat steps' makers; snow that falls up in the Narrows gap.
6. **Requests to other authors** (nothing depends on them): TF-M3 coda Gerrit line about the Red Slope thaw contract (`TSR_SEAM` = shared); TTH to quote the TFS verse text and read `TFS_VERSE_ASKED`; TF-M5 one Aud line if `TBC_WAIT_NAMED`; TSM one tally line reading `TFS_HARE`.

## Internal review log (package)

| Check | Result |
|---|---|
| Bible §7.2 briefs | All five delivered with the brief's place, verbs and hooks: TSR tap-and-count at Red Slope with two highsteads, plots, graves and Gerrit; TST bowyer at Stonewake and wind-tested wood on the Burned Slope; TGY ram herd, cull or drive with Gather and Fall, goat leather; TFS first winter night at Nettlehook, snowhare, cooking, a chosen ridiculous story, the children's "third call too late"; TBC storm crack, escorts, grain and families, smithing with Aud, a visible triage plan, optional braid 2 callback. |
| §7.1 contract fields | In every summary card. |
| Three states | No fail or abandon logic; every step has a no-loss retry; every resume hook is named. |
| Skill steps | Each taught as play through sound or wind; each has a crew or alternative path; no level checks. |
| Distinct verbs | prospect / select / track / hunt / triage as primaries; checked against milestones and the sister package. |
| Wonder or unease | One or more per quest; none duplicates the sister package's moments. |
| Evidence rule | No phenomenon identifies anyone; combat yields nothing; no revelation owned. |
| TD-13 | No ridge iron, stormwood or goat leather item; every material listed as an economy-pass dependency. |
| FT-03 / TD-11 | No route for any grain, oil, salt or stock; the Lowmark callback names no river or crossing. |
| Remnant, magic | None present; no NPC recognises magic. |
| Splinter tagging | No node names Ingrith, Bersi or Eyvind. |
| Quest items | None; carry-state and stations only. |
| Lowmark independence | Only TBC reads Lowmark state, for optional lines. |
| **Independent review (2026-11-03)** | 6 findings (1 high, 3 medium, 2 low). High: TST granted the first Ranged weapon while S01 is open and release scope may not grow; TST.15's fallback is now the default (stave racked unstrung, the player calls lulls for Brita), and the bow, arrows and Ranged lesson are kept only as **[PROPOSAL — DIRECTOR]** gated on S01 (summary, beats, steps, rewards, integration, open questions). Medium: TSR's Asa Grell collided with TWN's Asa Brede; renamed **Dagny Grell**; a plot-list "Orm" collided with Orm Brede; renamed **Eyolf**. Medium: bowyer Hild Crane collided with "Hild, a weaver" on Act III's closure roster; renamed **Brita Crane** (`TST_HILD_BENCH` → `TST_BRITA_BENCH`). Medium: Bera's herding horn was a gift; now a carry-state loan only if the TF-M1 practice horn is not carried. Low: TFS verse confirmed as canonical; TTH now quotes it. Low: Ranged mentions gated on S01. |
| **Batch 4 handoff review (2026-11-03)** | 1 finding (medium). TBC's cracked Narrows state ran from TF-M1 until TBC completed, contradicting the Batch 4 bridge model. Smallest edit: TBC.1 Unlock and TBC.11 now show the bridge cracked only while TBC is Active (scree path walkable regardless); TBC.15 open decision 4 marked resolved; TBC.16 row added. No other text changed. |
