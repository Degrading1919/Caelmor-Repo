# Thornfell Side Quests — Horn and Silence; Clans of the High Steads

**Status (2026-11-02):** Authored production content for Creative Director review (Thornfell bible §12, batch 3). Six side-quest packages in two interconnected questlines (bible §7.1): ***Horn and Silence*** (**TTH** *The Third Horn*, **TWG** *Witness at the Gate*, **TNK** *The Notes We Keep*) and ***Clans of the High Steads*** (**TNR** *Nettlehook Rope*, **TSM** *A Place at Smoke Week*, **TRR** *Rope-Raising Day*). Everything marked **[NEW]** is authored here and is not canon until the Director promotes it. **[CANON]** items come from the reconciled `LORE/` files. **[PROPOSAL — DIRECTOR]** marks a consequential choice the content is built on. **[APPROVED — id]** cites an architecture ruling. No schema, JSON or C# is created here; nothing here sets release scope (Thornfell is an internal production milestone; the first public beta contains the complete game, CDR-3). **Reconciled 2026-11-03** to the binding `Caelmor_Director_Rulings_Combat_Ranged_Release.md` (CDR-1 defeat at 0 HP, CDR-2 ranged included, CDR-3 milestone wording).

**Controlled by:** `Caelmor_Thornfell_Narrative_Production_Bible.md` (author truth §2, cast and voice §5, side-quest slate §7.1, revelation map §8, flags §9, encounter families §10, conventions §11). **Format:** the Lowmark side-quest package format (`Caelmor_Lowmark_Side_Quests_Settlements_and_Combat.md`), extended with the Lowmark act-package sections the Thornfell bible §11.1 requires (selection record, canon grounding, contribution-contract fields, strange-moment presentation spec, mystery ledger, open decisions). **Dialogue is inline** in each package (§x.18), in the Lowmark node format, with node ids `<CODE>-D<n>.<nn>`, barks `<CODE>-B<n>.<nn>` and encounters `<CODE>-E<n>`.

**Other sources used:** `00_ADMIN/Reference/Caelmor_Part3_Thornfell_Proposal.md` (Nettlehook, Hushfold, Three Calls Shelter, the shelter tally, Rope-Raising Day, First Smoke's "third call too late" verse, Dorn's worry about a missing reply); `LORE/Regions/Caelmor_Region2_ThornfellMarches.md` (Silent Gorge, horn towers, relay horns, fauna); `LORE/Characters/Caelmor_Characters_Region2_Thornfell_Anchors (Not Full List).txt` §IV; `00_ADMIN/Reference/Caelmor_Part4_Character_Family_Continuity_Ledger.md` (Thornfell rows); `Caelmor_Narrative_Architecture_Review_and_Authoring_Sequence.md` §7.1 (the contribution contract); `Caelmor_Narrative_Architecture_Revelation_Ledger.md` R16; `Caelmor_Narrative_Architecture_Factions_and_World_Truth.md` H07, H08, H11, H16, H23, H25, C.5.

---

## 0. Slate header

### 0.1 The six quests at a glance

| Code | Quest | Series (part) | Type | Unlock | Where | Core verb (primary first) | Gameplay identity | Strange / wonder moment | Sets |
|---|---|---|---|---|---|---|---|---|---|
| **TTH** | The Third Horn | Horn and Silence (1/3) | Memory/lore | TF-M1 Completed (`TH_CALLS`); richer after TF-M3 | Passwatch horn post; the answering stones on the Windscar track; Three Calls Shelter | **compare**, listen, restore | A **call-and-reply relay walk**: blow Lost from four old answering stones and compare the replies against a painted horn map, a bed book and a child's verse; rebuild the missing call on Dorn's peg board | At the Narrows stone, the player's own Answer comes back off the fluted faces **with a rising tail it did not have** | `TH_THIRD_HORN` (always true on completion); `TTH_KEEPER` |
| **TWG** | Witness at the Gate | Horn and Silence (2/3) | Environmental | TTH Completed | The Old Watchfire Line (six horn towers); the Silent Gorge | **climb**, decode, carry | **Tower-to-tower groove reading**: climb ruined towers, read each groove's cut by hand and breath, match five to known calls, decode the sixth by holding a note; then carry the call down the line into a null-point | The decoded call runs on by itself from groove to groove along the ridge and **stops dead** at the lip of the Silent Gorge; below, frost slides into four worn cup-hollows | `TWG_CALL` (plants R16) |
| **TNK** | The Notes We Keep | Horn and Silence (3/3) | Settlement/finale | TF-M4 Completed (`TH_HORN` set) **and** TWG Completed | Signal Terrace, Stonewake; plate custody site per `TH_HORN` | **decide**, retune, perform | **Retune by ear, then perform**: true the ridge's ordinary horns against a reference at the practice face, settle the code book page by page, then sound the kept set while the towers answer across the ridge | Every tower on the ridgeline answers the terrace in turn; with the forgotten call kept, Dorn sounds it last and **nothing answers** | `TH_HORN_CODES` (kept / pruned); `TNK_PLATES`; `TNK_EYVIND` |
| **TNR** | Nettlehook Rope | Clans of the High Steads (1/3) | Skill-adjacent settlement | TF-M1 Completed | Nettlehook Highstead ropeway; the lower longhouse | **repair**, ride, rota | **Fix a machine, ride it, then redraw who rides**: clear and re-pin a fouled sheave at height under crow attack, test-ride the car through a wind window, then rebuild the peg rota against daylight, loads and brake crews | Stopped mid-span in a gust, the cable sings a rising note, and from the shelf below **Tova hums it back exactly** | `TNR_ROTA` |
| **TSM** | A Place at Smoke Week | Clans of the High Steads (2/3) | Settlement (Hushfold) | TNR Completed **and** TF-M2 Completed (`TH_SEASON` = snow) | Hushfold; the far woodstacks; the goat shoulder above Nettlehook | **haul**, hunt, decide | **Work off a debt, then argue it**: haul two sledge loads of the household's owed wood along a shelf path in wind windows, hunt the meat share, and stand at the tally reading | At the first smoke, every chimney on the shelter line rises straight, then **all lean together at one height toward the far shielings** | `TH_HUSHFOLD_VOICE`; `TSM_CLAIM`; `TSM_PLAYER_TALLIED` |
| **TRR** | Rope-Raising Day | Clans of the High Steads (3/3) | Festival | TSM Completed **and** TF-M3 Completed | The Windscar Narrows (permanent span); Nettlehook for the meal | **inspect**, carry, celebrate | **A festival you work**: witness the span inspection knot by knot, lead the children's guide-line carry across in wind windows, tie and have judged a festival knot, and settle where a clanless household's ribbon goes | When the guide line touches the far anchor, every horn post in earshot blows Rest at once and the Narrows throws it back as **one chord** | `TH_HIGHSTEADS_TOGETHER`; `TRR_RIBBON` |

**Length targets:** TTH 30–40 min; TWG 35–45; TNK 30–40; TNR 30–40; TSM 35–45; TRR 25–35. About 3.5 hours across the six.

**Combat share:** TTH ~15%; TWG ~20%; TNK 0% by design (a finale of listening and deciding); TNR ~15%; TSM ~20%; TRR 0–5% (optional). Combat is never the core verb in either series (bible §7.2 structure check: TGM and TSG carry Thornfell's combat-core side content).

### 0.2 Series spines

**Horn and Silence: a reply, a stranger's call, a code.** Thornfell's horns say what the Marchers will admit to. This series walks the player through the three calls nobody plays (bible §1.1, §9.4) in the order the bible teaches them, and never plays the first.

| Part | What the player recovers | What stays missing | Spine line |
|---|---|---|---|
| TTH | **The Third Horn**: Answer + one long rising, "heard; someone is still out". Its meaning is recovered from a horn map and a host's bed book; the player chooses who keeps it. | Why the Wardens ordered it dropped. The bed book stops recording it in the late war with a one-line order and no reason (R06 sealing seed). | *A reply is a promise. Someone has to keep the beds.* |
| TWG | **Witness at the Gate**: two long, one held. The shape is recovered from tower grooves and the name from a lintel. | **Its meaning, forever, in Thornfell.** Ressa remembers only "for strangers". The grooves end at a null-point beside two gateposts with no gate. Plants R16; nothing names the custom. | *Some things were built to be heard by people who aren't here.* |
| TNK | **The code**: which calls Thornfell keeps in its book, what happens to the Wall-Horn's plates, whether a splinter hornwright may tune ordinary horns. | Nothing new is learned. The quest is a decision about memory. The Split is **never** sounded, shown as a shape or reproduced in audio. | *A warning has to mean one thing to the one who blows it and the one who hears it.* |

**Clans of the High Steads: a rope, a tally, a ribbon.** Thornfell says it stands together. This series is three ordinary winter jobs that show who actually gets to stand where, and lets the player move the line a little.

| Part | Who is left out | By what rule | What the player can change |
|---|---|---|---|
| TNR | Tova Rask, eleven, who has missed lessons all autumn. | The ropeway rota runs by lineage; the keeper's household (the newest on the shelf) rides last, and in short winter light the last runs are cancelled. | The rota, after the player has fixed the thing it schedules. |
| TSM | The Kvist household at Hushfold. | The winter tally counts work done; the Kvists missed their hauls while nursing a sick traveller and were kept back from shared work for fear of the fever. | Whether need and shared work make a claim. Whether the player is counted too. |
| TRR | A clanless household at the clan festival. | Witness ribbons have always been tied by clan households. | Where the ribbon goes, and whether everyone ties one. |

### 0.3 Unlock graph

```
TF-M1 The Closing of Passwatch (TH_CALLS, TH_PASSWATCH_ROUTE)
 ├─► TTH The Third Horn ───────────► TWG Witness at the Gate ──┐
 │      (richer after TF-M3)                                   │
 │                                   TF-M4 The Summit Hall ────┼─► TNK The Notes We Keep
 │                                     (TH_HORN)               │     (practical window: after TF-M5; see TNK.16)
 │
 └─► TNR Nettlehook Rope ──► TSM A Place at Smoke Week ──► TRR Rope-Raising Day
                              ▲ also needs TF-M2              ▲ also needs TF-M3
                              (TH_SEASON = snow)

Feeds TF-M5 The Gatefall / Stonewake:  TH_THIRD_HORN (TTH) · TH_HUSHFOLD_VOICE (TSM) · TH_HIGHSTEADS_TOGETHER (TRR)
Feeds the convergence:                 TH_HORN_CODES (TNK) · TWG_CALL (TWG, R16 seed) · TH_THIRD_HORN (closure-account weight)
```

The two series do not gate each other. A player can finish either without touching the other. TF-M1–TF-M4 gates come from the bible; no package here adds a main-quest prerequisite. TNK's practical window is discussed in TNK.16 (open decision).

### 0.4 Flags set and read

**Region flags set** (all from bible §9.1; none created here):

| Flag | Values | Set by | Read by | Effect |
|---|---|---|---|---|
| `TH_THIRD_HORN` | bool | TTH `S10_keeper` (true on every completion path) | TF-M5 column beat; TF-M5 Assembly lines; TNK; convergence (request) | TF-M5: the player blows the restored reply themselves to bring in the two stragglers (otherwise Dorn does). One Assembly line names the reply as part of the new closure account. |
| `TH_HUSHFOLD_VOICE` | bool | TSM `S07_reading` (true for `TSM_CLAIM` = counted or shared; false for = private) | TF-M5 placement (§9.3: +1 toward open); TF-M5 Runa lines | Hushfold comes to the Assembly with an agreed tally and one voice; Runa stands with her households, not alone. |
| `TH_HIGHSTEADS_TOGETHER` | bool | TRR `S06_ribbon` (true for `TRR_RIBBON` = everyone or witness; false for = old_line) | TF-M5 placement (§9.3: +1 toward open); TF-M5 Ketil, Aud and Runa lines | The highsteads stand as one block in the hall: Nettlehook beside Hushfold. |
| `TH_HORN_CODES` | kept / pruned | TNK `S03_book` | Convergence alarm network (CV-M2); CV-M1 R16 custody (request) | See 0.5. |

**Quest-local flags other packages may read** (all optional variant lines; nothing depends on them):

| Flag | Values | Set by | Read by (request) |
|---|---|---|---|
| `TTH_KEEPER` | board / wardens / hosts | TTH | TF-M5 (who answers the straggler call beside the player); TRR bark; CV-M2 |
| `TWG_CALL` | recorded / greeting / left | TWG | TNK code-book page; Passwatch gate barks; CV-M1 (R16 custodian: "horn rosters") |
| `TNK_PLATES` | damped_sealed / damped_open / shards_step / shards_gorge / shard_given / store_kept / store_summit / store_broken | TNK | TF-M5 or epilogue lines; *Whose Colours* (Brynjar, request) |
| `TNK_EYVIND` | helped / refused | TNK | Assembly epilogue line on Eyvind (request; optional) |
| `TNR_ROTA` | children_first / lots / lineage_swap | TNR | TSM, TRR, TF-M5 Ketil line |
| `TSM_CLAIM` | counted / shared / private | TSM | TRR, *The Weight of a Name* (Hushfold barks), TF-M5 |
| `TSM_PLAYER_TALLIED` | bool | TSM | All Hushfold and Nettlehook hosts (name address, §5.3 rule 4). Every name-address reader checks `TSM_PLAYER_TALLIED` **or** `TME01_TALLIED` (Settlements and Combat file); TF-M5 reads the same pair (request) |
| `TRR_RIBBON` | everyone / witness / old_line | TRR | TF-M5; Narrows barks |

**Region and quest flags read here:** `TH_CALLS`, `TH_PASSWATCH_ROUTE`, `TH_STORES`, `TH_BRYNJAR`, `TH_SHATTERFALL_ACCOUNT` (one line), `TH_HORN`, `TH_SEASON`, `TH_COLUMN` and `TH_ASSEMBLY_POSTURE` (TNK variants after TF-M5), `TPW_NAMES_ASKED` (TTH variant), TF-M3 Completed (TTH richer lines), TFS Completed (TTH verse variant).

### 0.5 How the series feed TF-M5 and the convergence

**TF-M5's Assembly placement (bible §9.3).** Hadrik places people; the player chooses only their own place. Two flags from this file count **+1 toward open** each:

| Flag | Who stands where because of it | If false or unset |
|---|---|---|
| `TH_HUSHFOLD_VOICE` | Runa Weatherall stands at the speaking stone's left with Hushfold's households behind her, holding the amended tally book. When the rubbing is read, she answers it as Hushfold, not as one host. | Runa stands alone at the back with the tally book under her arm. She still reads (the TF-M5 second-custodian beat is required regardless). |
| `TH_HIGHSTEADS_TOGETHER` | Ketil Rask, Aud Hammerlee and the Nettlehook households stand in one block with Hushfold. Tova is on the wall bench with the other children. A witness ribbon is tied round Aud's wrist. | Nettlehook stands with its clan neighbours, Hushfold apart. Nobody remarks on it. |

`TH_THIRD_HORN` does not move the posture. It changes **TF-M5 beat 5** (the player blows the restored reply to bring in two stragglers) and adds one Assembly line when the closure account is adopted: *"And the stones will answer with the third horn, so the one who closes knows who's still out."* (Act III package request; wording theirs.) The restored reply is the sound of the closure account: the same idea, one in a horn and one in a book.

**The convergence (bible §8.2).**

| Output | Pays off | Contract |
|---|---|---|
| `TH_HORN_CODES` = kept | CV-M2 alarm network: Thornfell's book carries every call, including the forgotten one, with what is and is not known written beside it. The network is **richer and slower** to teach. | Network exists in both values. |
| `TH_HORN_CODES` = pruned | CV-M2: Thornfell's book carries the six Ordinary Calls and the Third Horn only. The network is **smaller and faster**; the Split and Witness survive only in stone (the Horn Seat, the tower grooves). | Network exists in both values. |
| `TWG_CALL` (any) + TWG Completed | R16 (CV-M1): one of the custodians "horn rosters". With `recorded` the call is in Dorn's code book; with `greeting` it is in Passwatch's gate practice; with `left` it is only in the Old Watchfire grooves and the player's memory. **In every value the grooves and the lintel remain** (guaranteed custody). | Thornfell content never names the custom, never explains the call, never names the Crossing Concord. |
| `TH_THIRD_HORN` + `TTH_KEEPER` | CV-M3 "witness at every crossing" chip (request, outcome only). | Flag read only. |

### 0.6 Shared rules for all six packages

- **Quest items: none.** Thornfell's budget of four belongs to the milestones (bible §9.5). Carried things (a chalk copy of a horn map, a tally page, sheave pins, a wood sledge, game, a guide line, a ribbon, a sack of plate shards) are **carry-state objects**. Reward tools are named functionally.
- **The horn.** Every call the player blows uses the **call interaction** taught in TF-M1 (`TH_CALLS`). TF-M1 always leaves the player holding the **hornbearer's practice horn** (Act I reward tool); every quest here relies on it. Only if the player is not carrying it does the quest-giver lend a horn as a **carry-state loan**, returned on completion (Dorn in TTH-D1; Warden horn racks elsewhere). No new item. Calls show their accessibility glyph (bible §9.4) when blown and when heard.
- **The peg board** [NEW]. TTH, TWG and TNK share one small puzzle surface: a board of four peg types (**short**, **long**, **rising**, **held**) set in a row to compose a call, then blown. It reuses the glyph art. A wrong composition plays back what was composed and gets a dry line. Nothing fails.
- **Steps** use `S00_…` ids scoped to the quest. **Completion events** are the Lowmark set: enter-volume, inspect, interaction-complete, carry-deposit, creature-defeated, dialogue-node-reached, plus *watch* (advance the per-player presentation hour; Lowmark keep-watch convention) and *call-blown* (a call interaction completed with a given shape inside a volume) [NEW event type; TTH.14].
- **No quest can fail.** Inactive / Active / Completed only. Death respawns at the quest's named safe point with step and flags intact. Logout restores the last persisted step; channels in progress are discarded, completed channel segments persist, and a dropped carry-state object returns to its source. Walking away keeps the quest Active at its step with the resume hook named in each package.
- **Wind windows** (bible §9.5): the fluted-face whistle "a fifth before the gust" is the tell; sheltering behind chalk-marked faces is always safe. A gust that catches the player in the open knocks them down (stagger, small damage, never off a ledge).
- **Agility triggers** are optional shortcuts; each has a walkable fallback named in its place table (click-to-move).
- **Defeat** (CDR-1; TD-7 superseded): every enemy, human or animal, fights until defeated at 0 HP and uses the ordinary defeat presentation. No yields, tied props, break-off or low-health retreat. None of these six packages has a scripted surrender.
- **Evidence rule.** Every fact is carried by a record, an object, a place or a person. The echo that adds a tail (TTH), the call that runs the towers (TWG), the cable's note (TNR), the leaning smoke (TSM), the chord (TRR) and the unanswered call (TNK) **prove nothing and identify nobody**. Combat drops nothing that advances an investigation.
- **Season** (`TH_SEASON`): TTH, TWG and TNR can be played in autumn or snow (both presentations noted where they differ). TSM and TRR are always in snow (TSM needs TF-M2). TNK is always in snow.
- **Co-op:** independent instances; shared world creatures give step credit to every participant on that step; quest-state props and NPC placement are per player (Lowmark per-player prop pattern; fallback: the host's state drives props, each player's own state drives dialogue).
- **Skills:** Hunting (TSM), Smithing (TNR, TNK), Woodcutting (TSM optional), Melee and Ranged (all combat; Ranged is a first-class option, never required, CDR-2). Every skill step has a crew alternative. Exact levels belong to the Gameplay Designer. Ridge iron, stormwood and goat leather remain unapproved item concepts (TD-13): no step consumes or rewards them as named items.
- **Splinter tagging:** every node naming Eyvind Stall, Ingrith Scarrow or Bersi Coldbrook is tagged `[SPLINTER]` (TNK names Eyvind throughout; TWG-D6.03 names him once; all tagged).
- **Lowmark independence:** no quest here reads a Lowmark flag. None is needed.

### 0.7 Distinctness check

| Quest | What the player physically does | Not the same as |
|---|---|---|
| TTH | Walks a chain of answering stones blowing Lost and listening for replies; compares three records; composes a call on a board | TF-M1 (learns the calls at one post); TF-M5 (climbs toward calls in whiteout) |
| TWG | Climbs ruined towers, reads grooves by touch and breath, fights a bandit lookout, descends into a null-point by sight | TF-M4 (triangulates voices in halls); TME05 (stands still in a null-point); TGM (fights in a null-point) |
| TNK | Tunes horns by comparing echoes at a practice face; settles a code book; performs a call sequence with distant replies | TF-M4 (damps plates under pressure); TTH (composes one call) |
| TNR | Climbs a sheave tower, clears ice and a crow nest, sets a new pin, rides a ropeway car; rebuilds a rota board | TF-M1 (bridge build against a clock); TBC (triage plan for one crossing) |
| TSM | Hauls a loaded sledge along a shelf path; tracks and hunts; stands at a public reading | TGY (hunting intro, herd driving); TFS (cooking, storytelling) |
| TRR | Witnesses an inspection, leads children along a guide line, ties a judged knot, places a ribbon | TF-M1 (builds the bridge under threat); TBC (repairs it after a storm) |

### 0.8 Ids and names used

Content ids (suggested; the Schema & Content Engineer owns naming): `thornfell.side.the_third_horn`, `thornfell.side.witness_at_the_gate`, `thornfell.side.the_notes_we_keep`, `thornfell.side.nettlehook_rope`, `thornfell.side.a_place_at_smoke_week`, `thornfell.side.rope_raising_day`.

New minor names [NEW] introduced here: **Thyra Brack** (host of Three Calls Shelter); **Osk Varrow** (Nettlehook's rota elder); **Leiv** (lesson-keeper at Nettlehook's lower longhouse); **Ama Kvist** and **Pell Kvist** (the Hushfold household); **Grima Loft** (Hushfold's hauling elder, who keeps the work count). All other speakers are bible cast or role names.

---

# Series one — Horn and Silence

---

## TTH — The Third Horn

### TTH.1 The quest in one paragraph

Dorn Feldhorn's training board at the Passwatch horn post has a row for every call a Marcher child learns, and one row more: two Answer pegs and a third hole gouged out, with a label board scraped bare. "Reply nobody blows," Dorn says, and he does not like being asked. He half remembers that it once meant somebody was still on the path. He lends the player a practice horn and sends them down the old **answering stones** of the Windscar track, where Ressa has agreed to run a drill: blow Lost from each stone and see what comes back. What comes back is always Answer, and at the Corner Stone the drill shows what Answer cannot say: two cadets are "out", one comes in, the next station hears Answer and blows Rest, and the second cadet is left on the hill grumbling that nobody waited. A winter-thin wolf pack answers the horn too. At the Narrows Stone, under the fluted faces, the player's own Answer comes back off the cliff **with a rising tail it did not have**. At **Three Calls Shelter**, the host Thyra Brack shows the painted **horn map** on her guest-room wall: beside two of the stones, the reply is drawn as two dots and a rising line, and a smoke-dark legend reads *"Two and the rise: keep the beds."* Her grandmother's **bed book** records it being blown and beds being kept, until a late-war page that says only *"Wardens' word: answer with two from the stones. No third."* Thyra's grandchildren skip rope to the First Smoke verse that ends *"Third call's too late, and nobody's here."* The player rebuilds the call on Dorn's board, **Answer and one long rising**, "heard; someone is still out", and blows it from the post. Ressa comes up the steps. She will not refuse a reply, she says, but a reply that says someone is still out is a promise, and somebody has to keep it. The player decides who.

**Remember:** your own call coming back off the cliff, changed. **Want next:** the other call nobody knows (TWG), and the night TF-M5 asks the player to blow this one for real.

### TTH.2 Selection record

| Candidate | Verdict |
|---|---|
| **A. Dorn tells the player the meaning; the player teaches it.** | Rejected. Talk-led, and Dorn's limit is that he half remembers. The meaning has to come from records and places. |
| **B. The echo at the Narrows "reveals" the lost call.** | Rejected. A phenomenon would be testifying (bible §11.3). The echo stays a strange moment that proves nothing. |
| **C. Relay walk → drill that shows the gap → map and bed book → child's verse → compose → Ressa's promise question → keeper choice** (selected). | **Selected.** The player feels the missing reply in play before reading why it existed, and the evidence is two records (map, book) plus testimony (Dorn) and folk memory (the verse). |

### TTH.3 Canon grounding

| Element | Source | Status |
|---|---|---|
| Dorn maintains the long-range horn codes with ritual seriousness and private fear; altered echoes | Anchors §IV | [CANON] |
| Ressa refuses certain calls; keeps the horns | Anchors §IV | [CANON] |
| Dorn worries a missing reply will be mistaken for an omen rather than human error | Part 3 proposal, "People who can carry recurring stories" | Proposal; used as Dorn's motive |
| Three Calls Shelter: guest ledge with a horn map from evacuation years; hosts keep bed space by household count | Part 3 proposal; bible TP06 | [NEW, Part 3] |
| "Third call too late" verse preserving the missing-reply controversy | Part 3 proposal (First Smoke); bible TFS | [NEW, Part 3] |
| The Third Horn: Answer + one long rising, "heard; someone is still out", dropped after the war | Bible §9.4 | [NEW] |
| Answering stones, the drill, Thyra Brack, the bed books, the legend line, the late-war order | This package | [NEW] |
| Ridge Wolves (runner, howler) | Bible §10 | [NEW on dossier fauna] |

### TTH.4 Summary card

| Field | Value |
|---|---|
| Suggested content id | `thornfell.side.the_third_horn` |
| Series | *Horn and Silence*, part 1 of 3 |
| Type | Memory/lore |
| Unlock | TF-M1 Completed (`TH_CALLS`). Offered by Dorn at the Passwatch horn post (`TTH-D1`), or by inspecting the seventh row of the training board (Dorn then calls the player over). **Richer after TF-M3:** Dorn's lines connect the reply to the horn roster's "No answer" (`TTH-D1.06`, `TTH-D6.04`). |
| Length | 30–40 minutes |
| Combat share | ~15% (one wolf encounter) |
| Skills | Melee or Ranged (encounter only) |
| Choice | Who keeps the restored reply (`TTH_KEEPER`: board / wardens / hosts) |
| Outputs | `TH_THIRD_HORN` = true; `TTH_KEEPER`; Three Calls "kept bed" rest point |
| **Anchor** | Thornfell Hornbearers and Ridge Wardens (Dorn, Ressa); Three Calls Shelter's hosts. |
| **World-truth row** | H16 (Thornfell's stop: the sealings), touched only as a seed: the bed book's late-war order. H11 (horn codes) as practice. |
| **Revelation role** | **Supports R06 (sealing half)** as a seed: "the Third Horn's lost meaning" is listed in bible §8.1 as a seed before TF-M5. Owns nothing. |
| **Recurring evidence** | The **horn map** (Three Calls Shelter wall; custodian: Thyra Brack as host) and the **bed book** (Thyra's family chest) are independent of each other and of Dorn. Both stay in place after the quest and can be re-inspected. Neither reappears as an item. |
| **State compliance** | Inactive → Active on `TTH-D1` end or board inspect; Completed on `TTH-D7` end. No fail path. The choice is recorded in `TTH_KEEPER`; `TH_THIRD_HORN` is true on every path. Walking away keeps the step; resume hook: Dorn at the horn post (`TTH-B1.04`). |

### TTH.5 The places

All placements relative. **MAP VERIFICATION REQUIRED** for every answering stone: the bible route order is Passwatch gate → Blind Corners → Narrows → Three Calls Shelter (§4.2). The stones sit on that line.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Passwatch horn post** (TP02) | Hook, compose, sound | Dorn's **training board**: a weathered plank with seven rows of peg holes and painted glyphs. Six rows for the Ordinary Calls, pegs worn smooth by children's thumbs. The seventh: two short pegs, then a gouged hole where a third peg was prised out, and a label board scraped back to wood. Under the scrape, in raking light, the ghost of a painted rising line. A spare peg box under the bench holds every peg shape, including rising pegs nobody uses. |
| **B1. The Gate Stone** | Relay stone 1 | Waist-high post outside the Passwatch gate, a mouth-hollow cut at horn height, the top worn into two elbow dips. A glyph cut on its face: a rising line (Lost), then two dots. |
| **B2. The Corner Stone** | Relay stone 2; TTH-E1; the drill | Above the Blind Corners on the goat-track shoulder (TF-M1's agility route; the walkable fallback is the switchback road below, which has its own steps up to the stone). Wolf scat on the stone's lee side. The cadets' drill markers: two chalked stakes, one at the stone, one 40 m further up the shoulder. |
| **B3. The Narrows Stone** | Relay stone 3; strange moment | On the near-side bluff above the Narrows bridge, under three fluted faces. The faces' flutes run upward. Snow (or grit, in autumn) lies in the flutes in neat rising lines. |
| **B4. The Shelter Stone** | Relay stone 4 | At the lip of Three Calls Shelter's guest ledge. Its mouth-hollow is soot-blackened from someone using it as a lamp niche. |
| **C1. Three Calls guest room** | Horn map | The **horn map** is painted across four wall boards: the pass drawn as one long line, the four stones as circles, each with call glyphs beside it in pairs: a rising line (Lost) and then the reply. At the Narrows Stone and the Shelter Stone, the reply is two dots **and a rising line**. Lower left, a smoke-darkened legend. Bunks along the far wall with numbers chalked on the posts. |
| **C2. Thyra's chest** | Bed books | A cedar chest of bed books, one per host. The oldest are stitched with goat sinew. Thyra's grandmother's book has a wolf-tooth bookmark. |
| **C3. The guest ledge** | The verse | Thyra's two grandchildren and a haulier's boy skip a rope on the ledge. In snow they skip in a cleared square. |

**Variant (TF-M1 `TH_PASSWATCH_ROUTE` = split):** the caravan's beasts that waited out the storm at Three Calls have left a stable smell and a broken halter on the ledge; Thyra bark `TTH-B3.02`.

### TTH.6 Player-facing sequence

**Beat 0 — The seventh row (`S00_hook`).** *Objective: Ask Dorn about the board.* `TTH-D1`. Dorn names the row ("reply nobody blows"), half remembers its meaning, and, only if the player is not carrying their TF-M1 practice horn, lends one as a carry-state loan. He sends them to Ressa's drill on the answering stones.

**Beat 1 — The board (`S01_board`).** *Objective: Look at the seventh row.* Two inspects (both required): the gouged hole, and the scraped label (raking light from the post lantern, 2 s channel `rake_board`: the ghost of a rising line). Optional: the spare peg box.

**Beat 2 — The Gate Stone (`S02_gate_stone`).** *Objective: Blow Lost from the Gate Stone.* `call-blown` (Lost) in the stone volume. The warden on the gate answers: Answer. Glyphs show. A cadet chalks a tick. This teaches the relay.

**Beat 3 — The Corner Stone and the drill (`S03_corner_drill`).** *Objective: Run the drill at the Corner Stone.* The two drill cadets are "out" (at the chalked stakes). The player blows Lost. Cadet one walks in to the stone. The player must now reply to the next station. The peg prompt offers only what the player knows: **Answer**. The player blows it. Passwatch hears Answer and blows **Rest**. Cadet two, still at the far stake, throws up her hands and walks down: *"Nobody waited."* (`TTH-D2`). The point lands in play: Answer means "heard"; nothing says "someone is still out". **TTH-E1** (the wolves) begins as the Rest call fades: the pack answered the horn. The cadets retreat behind the stone (they are never targets). The step completes when E1 is defeated and `TTH-D2` ends.

**Beat 4 — The Narrows Stone (`S04_narrows_stone`).** *Objective: Blow Lost from the Narrows Stone.* `call-blown` (Lost). The warden posted at Three Calls answers with Answer. The player is prompted to acknowledge (blow Answer back, a courtesy Dorn taught). **The strange moment** (TTH.8): the player's Answer returns off the fluted faces with a long rising tail. One inner-voice inspect. If the player blows Answer again, it comes back plain. Nothing explains it. Dorn, if asked later, says "wind tricks" and does not smile (`TTH-D6.02`).

**Beat 5 — Three Calls Shelter (`S05_shelter_map`).** *Objective: Ask the shelter host about the stones.* `TTH-D3` (Thyra). The **horn map**: three required inspects: the stone line, the reply beside the Narrows and Shelter stones (two dots and a rising line), and the legend (*"Two and the rise: keep the beds."*). The Shelter Stone relay completes here automatically (Thyra blows Lost herself for the drill, and grumbles about it), so the player is not asked to repeat the relay mechanic a fourth time.

**Beat 6 — The bed book (`S06_bed_book`).** *Objective: Read the old bed book.* Thyra opens her grandmother's book (`TTH-D3.20`). Three required inspects: the **kept beds** entry, the **kept the fourth till thaw** entry, and the **order** page. Optional: the funny entry (`TTH-I2.04`).

**Beat 7 — The verse (`S07_verse`).** *Objective: Listen to the children's rhyme.* A *watch* interaction on the ledge bench (one rope-skip round, ~25 s). The verse plays whole once with no subtitles prompt until it ends. Then `TTH-D4` (the children, then Thyra). With TFS Completed, the player has heard it before (variant `TTH-D4.01`). Beats 5–7 may be done in any order once at the shelter.

**Beat 8 — Compose (`S08_compose`).** *Objective: Build the reply on Dorn's board.* Back at the horn post. The peg board (0.6): the target shape is **short, short, rising** (Answer + one long rising). Dorn watches (`TTH-D5`). Wrong compositions play back as composed, with a dry line each (`TTH-B1.10`–`.13`). After three wrong tries Dorn says which half the map gives and which half the verse gives (`TTH-D5.10`), and the board is then one peg from right. The step completes on the correct composition.

**Beat 9 — Sound it (`S09_sound`).** *Objective: Blow the reply from the horn post.* `call-blown` (Third Horn shape) at the post. It carries down the pass. After a pause, the Corner Stone cadet answers it, badly, then properly. Ressa comes up the post steps (`TTH-D6`).

**Beat 10 — Who keeps it (`S10_keeper`).** *Objective: Decide who keeps the reply.* `TTH-D6` choice. Sets `TTH_KEEPER` and `TH_THIRD_HORN`. Then `TTH-D7` (Dorn) closes the quest: he cuts a rising peg and sets it in the seventh row (in every outcome; what changes is who is taught). Quest Completed.

### TTH.7 Encounters

Tuned for Competent identity (TD-12, TF-M1–M2 band).

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TTH-E1** | 2 × Ridge Wolf runner, 1 × Ridge Wolf howler | Corner Stone shoulder; runners come down the goat track, howler holds a rock 15 m upslope | Runners: Aggressive, flank in a pair (one front, one circles behind the stone). Howler: Defensive at range; howls to call. Leashed to the shoulder. | **Runner lunge:** drops its chest to the snow, ears flat (~0.9 s), then a straight lunge 4 m; side-step beats it. **Howler call:** throws its head back, throat working (~1.5 s), then a **rising** howl; if not interrupted (any hit, or the player blowing **Fall** at it, which startles it), one more runner comes over the ridge (at most once). | The pack "answers" the horn: a light, readable fight that makes the Corner Stone a place, not a menu. The rising howl rhymes with the Lost glyph. | 40–60 s; player at 60–80% HP. Optional Ranged on the howler. |

**Rules.** Cadets stand behind the stone and are never targeted; the drill resumes after E1. Wolves fight until defeated at 0 HP (CDR-1). Nothing they leave advances the quest. If the player arrives at the Corner Stone after dark, the pack is already on the shoulder (same fight, eyes in the dark as the first tell).

### TTH.8 The strange moment: the Narrows return (Beat 4)

| Time | Element | Spec |
|---|---|---|
| 0 s | **The courtesy** | The player blows Answer (two short) from the Narrows Stone toward Three Calls. Glyph: two dots. |
| 0–1.2 s | **The flutes** | Ordinary first return off the near face: two short, slightly late (normal echo count, about 2 beats). |
| 1.2–2.0 s | **The second return** | From the fluted faces above: the two short again, and then a **long rising note** that the player did not blow, about 1.5 s, climbing a fifth. It is in the horn's own timbre. Glyph area shows the two dots and, after a breath, a faint rising line that fades **without settling** (the glyph UI never confirms it). |
| 2.0–4.0 s | **The flutes settle** | Loose snow (autumn: grit) trickles down the flutes in thin rising-then-falling lines, as if the flutes had been played. Wind ambience unchanged. No gust. |
| 4 s+ | **Nothing** | The Three Calls warden does not react. Nothing answers. |
| Repeat | **Plain** | Any later Answer from this stone returns plain. The return happens once per player. |
| Inspect | Inner voice | *"Two short. Then a long one, rising, that you didn't blow. The cliff is quiet now."* |
| UI | No objective update until 4 s after the return. No music. |
| What it means | Nothing that can be proved. Fluted faces shape sound (bible §1.1); this one shaped yours. A player may decide the stone "remembers" the old reply. The map and the book carry the evidence; the cliff carries none. Never explained in Thornfell (add to bible §7.4 "deliberately unexplained" list: request). |

### TTH.9 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_hook` | Ask Dorn about the board. | `TTH-D1` end node, or seventh-row inspect then `TTH-D1` | Yes | Inactive → Active. Practice horn given if the player has none. |
| `S01_board` | Look at the seventh row. | Inspect `hole` + `rake_board` channel (2 s) on the label | Yes | |
| `S02_gate_stone` | Blow Lost from the Gate Stone. | `call-blown` (Lost) in Gate Stone volume | Yes | Gate warden answers (scripted call). |
| `S03_corner_drill` | Run the drill at the Corner Stone. | `call-blown` (Lost) → cadet one arrives → `call-blown` (Answer) → TTH-E1 defeated → `TTH-D2` end | Yes | Drill state persists per segment. |
| `S04_narrows_stone` | Blow Lost from the Narrows Stone. | `call-blown` (Lost) then `call-blown` (Answer) in Narrows volume | Yes | Strange moment fires on the Answer, once per player. |
| `S05_shelter_map` | Ask the shelter host about the stones. | `TTH-D3` reaches `.10` + 3 map inspects | Yes | Shelter Stone relay auto-completes. |
| `S06_bed_book` | Read the old bed book. | 3 required bed-book inspects | Yes | Parallel with S05/S07. |
| `S07_verse` | Listen to the children's rhyme. | Watch interaction on ledge bench + `TTH-D4` end | Yes | Parallel with S05/S06. |
| `S08_compose` | Build the reply on Dorn's board. | Peg board composition = short, short, rising | Yes | Hint after three wrong tries. |
| `S09_sound` | Blow the reply from the horn post. | `call-blown` (Third Horn shape) in horn-post volume | Yes | Corner Stone answer (scripted). |
| `S10_keeper` | Decide who keeps the reply. | `TTH-D6` choice resolved, then `TTH-D7` end | Yes | Sets `TTH_KEEPER`, `TH_THIRD_HORN`; → Completed. |

### TTH.10 Flags

| Flag | Set by | Read by |
|---|---|---|
| `TTH_DRILL_SEEN` | `S03` | `TTH-D5` line, `TTH-D6` opener |
| `TTH_RETURN_HEARD` | Strange moment fired | `TTH-D6.02` (optional ask) |
| `TTH_KEEPER` = board / wardens / hosts | `TTH-D6` | TWG opener, TF-M5 (request), TRR bark, CV-M2 (request) |
| `TH_THIRD_HORN` = true | `TTH-D6` (every option) | TF-M5 beat 5 and Assembly line; TNK; convergence |

### TTH.11 Choices and consequences: who keeps the reply

Ressa's question is about accountable warning (anchor limit): a reply that says "someone is still out" commits whoever blows it to keep watch until that someone is in.

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Board** — *"Every child. Put it on the board with the rest."* (`TTH_KEEPER = board`) | Dorn sets the peg and teaches it at the next children's practice. Ressa writes one rule on the board's edge: *"Blow the third, keep the watch."* | Children blow it in play. A warden runs to the Corner Stone for nothing within a week (bark `TTH-B4.01`). Ressa is short with the player about it once. | TF-M5: when the player blows the reply for the stragglers, a highstead child's thin reply comes back from somewhere in the whiteout (presentation only). |
| **Wardens** — *"Wardens and hornbearers. People who'll stay out for it."* (`= wardens`) | Ressa writes it into the Warden code: whoever blows it holds the stone until the last is in. | Highsteads hear it and do not know it. Thyra grumbles that hosts are left to guess at their own beds (bark). | TF-M5: Vessa Galt's patrol answers the player's reply from beyond the gate (presentation only; `TH_COLUMN` unchanged). |
| **Hosts** — *"The shelters. It meant keep the beds. Give it back to the people with beds."* (`= hosts`) | Thyra repaints the legend on the horn map; shelter hosts blow it from the stones when they are keeping beds. | Hosts carry the burden. Poor households feel the bed count most (Part 3), and Thyra says so: *"So it's my beds again."* | TF-M5: Runa answers the player's reply from inside the gate with the reply itself, "beds kept" (presentation only). |

All three set `TH_THIRD_HORN = true`. None is wrong. None makes the reply both universally known and always kept.

### TTH.12 Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| **The Third Horn** | Knowledge | Added to the player's calls with its glyph (two dots and a rising line). Usable anywhere; meaningful at answering stones (NPC barks) and in TF-M5. |
| **A kept bed at Three Calls** | Access | Rest point and respawn option at Three Calls Shelter (Thyra: "Your bed's the fourth. It always is."). |
| **Practice horn** | — | Not a reward here: the player already holds TF-M1's practice horn. A `TTH-D1` loan (fallback only) returns to Dorn on completion. |
| Small payment | Currency | Ressa's drill pay for a walker. Economy tuning. |
| Skill XP | Actions only | Melee or Ranged. |
| *Witness at the Gate* | Story | Dorn: "There's another. Not on any board." (`TTH-D7.04`) |

### TTH.13 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Wrong call blown at a stone | The warden answers with a confused Gather (dry bark); the prompt repeats. No failure. |
| Wrong composition on the board | Plays back as composed; hint after three tries; the step cannot be failed. |
| Death at the Corner Stone | Respawn at the Passwatch gate; drill state kept; TTH-E1 resets if not defeated. |
| Arrives at the shelter before the stones | Thyra talks and shows the map and book; the stone steps stay open and can be done after. `S04` must still be done before `S08` (the composition needs the full relay seen). |
| Walking away | Stays Active. Resume: Dorn at the horn post (`TTH-B1.04`). Drill cadets wait at the Corner Stone indefinitely (they have a fire). |
| Logout mid-drill | Restores to `S03` start; cadets back at their stakes. |
| Fail state | None. |
| Co-op | Each player blows their own calls and composes their own reply. Wolves are shared (credit to all on `S03`). The strange moment fires per player (each hears their own; a partner standing by hears a plain return). Choice per player; the board's peg is per-player presentation (fallback: the peg is always present after any player completes; dialogue reflects each player's own `TTH_KEEPER`). |

### TTH.14 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| **Call interaction with shape** (`call-blown` event) | Systems | The TF-M1 call interaction emits an event with the call's shape id and the volume it was blown in. **Fallback:** a radial menu of call names. |
| **Practice horn** | Item pass | TF-M1's reward tool (Act I). **Fallback only:** a carry-state loan from Dorn, returned on completion. |
| **Peg board puzzle** | UI / Systems | A row of up to four slots, four peg types, a play button; compares to a target shape. Shared with TWG and TNK. **Fallback:** dialogue options listing shapes in words. |
| **Scripted reply calls** from NPC stations | Audio / NPC | Positional one-shot horn sounds at named points, triggered by step events. |
| **Altered echo** (strange moment) | Audio | One authored audio file (Answer + rising tail, cliff reverb) played once per player at the Narrows volume; per-player flag. **Fallback:** inspect text alone. |
| **Drill NPCs** | NPC | Two cadets with three positions (stake, stone, walking down). No combat AI; hide behind stone on combat start. |
| **Raking light on the board** | Art | Decal reveal during a 2 s channel. **Fallback:** inspect text. |
| **Watch interaction** (verse) | Systems | Lowmark keep-watch convention; here a ~25 s seated watch with the verse audio. |
| Creatures | Encounters package | Ridge Wolf runner, howler (with "startled by Fall" interrupt). |

### TTH.15 Mystery ledger

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **What the Third Horn meant** | A reply to Lost: "heard; someone is still out". It told the next station not to stand down and told hosts to keep beds. | An unlucky call; "third call too late" is a rhyme about being late for supper. | Board gouge and ghost glyph; horn map reply glyphs and legend; bed-book entries; the verse; Dorn's half memory; the drill. | An omen: blowing it calls the dead (Dorn's fear, Part 3). | — (owned here) | TTH |
| **Why it was dropped** | Late-war closures: beyond a sealed gate there was nobody the Wardens would go out for, and a reply that said "someone is still out" would have been true (author truth §2.2). | "The war changed the codes." | The bed book's order page: no reason, no signature beyond "Wardens' word". | The reply caused confusion and was simplified. | **Yes.** Never stated in TTH. | R06 sealing (TF-M5): the closure roster lets the player make the link. |
| **The Narrows return** | Fluted faces shaping a return (or rare resonance). | Wind tricks. | The return itself, once. | The stone remembers the reply / the dead answer. | Whether anything more is going on. | **Never** (unexplained). |

### TTH.16 Open decisions

1. **Verse text sync (resolved, independent review).** TFS owns the canonical text (TFS.14); `TTH-I3` quotes it word for word. The load-bearing line is "Third call's too late, and nobody's here."
2. **Practice horn (resolved, independent review).** TF-M1 gives it (Act I); TTH relies on it and keeps only a loan fallback.
3. **Answering stones on the map.** Four new props on the Windscar route; MAP VERIFICATION REQUIRED. If fewer fit, the Gate Stone can be cut (its beat folds into the Corner Stone).
4. **Unexplained list.** Request the bible owner add "the Narrows return" to §7.4's deliberately unexplained list.

### TTH.17 Internal review log

| Finding | Revision |
|---|---|
| First draft had the relay at all four stones as identical blow-and-listen steps. | The Corner Stone carries the drill (the gap felt in play), the Narrows the strange moment, the Shelter Stone auto-completes; only two are pure relay. |
| The Narrows return risked being the clue that "reveals" the shape. | It happens after the drill but the shape is only confirmed by the map glyph and the verse; the glyph UI never confirms the tail. |
| Ressa first refused to restore the call. | Changed: her limit is about accountable warning, not refusal for its own sake. She accepts a reply and asks who keeps the promise. |
| Dorn's TF-M3 line risked giving him Shatterfall knowledge. | He cites only the roster ("By the roster nobody blew it"), per the character ledger. |
| `TH_THIRD_HORN` as a bool could look like a pass/fail. | It is true on every path; the choice lives in `TTH_KEEPER`. |
| The order page risked revealing R06 sealing. | One line, no date, no reason. TF-M5's roster is where the player can connect it. |

### TTH.18 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Dorn Feldhorn** | Every code; that the seventh row once meant "people still on the path" (half); that some echoes come back altered. After TF-M3: the roster's "No answer". | Why it was dropped; what the map says; the verse's link. | Ritual about his board; few words; frightened of omens and ashamed of the fear. Never smiles about echoes. |
| **Ressa Highcrag** | The Warden code; that the order came from Wardens in the war; which tones caused wrong results. | Who gave the order or why; the roster. | Plain, short, tired of politics. Her question is always "who is accountable?" |
| **Thyra Brack** [NEW] | Her shelter, her grandmother's books, the map she paints over every spring except the legend. | What the legend meant beyond beds. | A host who counts beds in her sleep. Dry, practical, generous and annoyed about it. |
| **Cadets** (two; role names) | The drill. | Anything else. | Young, keen, cold. |
| **Children** (Thyra's grandchildren; role names) | The rhyme. | What it's about. | Rhyme-voice, then blunt. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| TTH-B1.01 | Dorn | Quest available, player near board | *"Don't touch the seventh row. Touch any other row."* |
| TTH-B1.02 | Dorn | Quest available, child practising | *"Two short. Two. Not two and a sneeze."* |
| TTH-B1.04 | Dorn | Quest Active, player returns before `S08` | *"Stones first. Then the board. Then we'll see."* |
| TTH-B1.10 | Dorn | Composition: Lost | *"That's Lost. You're not lost. You're at my board."* |
| TTH-B1.11 | Dorn | Composition: Answer only | *"That's what we've been blowing for thirty years. That's the problem."* |
| TTH-B1.12 | Dorn | Composition: rising first | *"Backwards. You've told them someone's out before you've said you heard."* |
| TTH-B1.13 | Dorn | Other wrong shape | *"I don't know what that is. Neither will anyone downhill."* |
| TTH-B2.01 | Gate warden | `S02` complete | *"Heard you. Chalked you. Go on."* |
| TTH-B3.01 | Thyra | Player arrives at shelter, quest Active | *"If you're the walker blowing Lost at my stone, I've a kettle on and an opinion."* |
| TTH-B3.02 | Thyra | `TH_PASSWATCH_ROUTE` = split | *"Caravan beasts slept here through the storm. Ate the thatch. I've written it down."* |
| TTH-B4.01 | Passwatch warden | Completed, `TTH_KEEPER` = board | *"Ran to the Corner Stone. Third horn. It was a girl with a goat. She'd lost the goat."* |
| TTH-B4.02 | Thyra | Completed, `= wardens` | *"Third horn's back and nobody's told the hosts what to do with it. Typical."* |
| TTH-B4.03 | Thyra | Completed, `= hosts` | *"Fourth bed's made up. If I blow it, I mean it."* |

#### Nodes

```
TTH-D1.01 DORN: (re-pegging a child's Gather) "Calls are on the board. Learn them off the board."
TTH-D1.02 [player inspected the seventh row] DORN: "I said don't touch that row."
  > "What's the seventh row?"                              → TTH-D1.10
  > "Why is a peg missing?"                                → TTH-D1.10
  > "Nothing. Sorry."                                      → end
TTH-D1.10 DORN: "Reply nobody blows."
TTH-D1.11 DORN: "Two short, and then something. Prised out before I had the board."
TTH-D1.12 DORN: "My teacher said it meant people still on the path. Then he said forget it. So I half did."
TTH-D1.06 [TF-M3 Completed] DORN: (quieter) "The roster at the Seat. 'Rear guard not recalled. No answer.'" (beat) "By the roster nobody blew it."
  > "Why was it dropped?"                                  → TTH-D1.20
  > "Can it be got back?"                                  → TTH-D1.30
TTH-D1.20 DORN: "Don't know. I don't like not knowing. A missing call gets a story put in it."
TTH-D1.21 DORN: "Then children say it's the call that brings the dead in. It isn't. It's a reply someone stopped making."   → TTH-D1 options
TTH-D1.30 DORN: "The old stones down the pass. Every one had a reply. Ressa's running a drill on them today, cold as it is."
TTH-D1.31 [practice horn not carried] DORN: (hands over a dented horn) "Lost mine already? Take this. Dented on a child. Don't dent it on a wall."   {loan horn (carry-state; returns to Dorn on completion)}
TTH-D1.32 DORN: "Blow Lost from each stone. Listen to what comes back. Then come and tell me what's missing."
      {event: S00_hook; objective → S01_board}
```

```
TTH-D2.01 CADET (ONE): (arriving at the stone, breathless) "In. One in."
TTH-D2.02 CADET (ONE): "Now you reply to Passwatch. Go on."
      {peg prompt: Answer is the only learned reply}
      {after Answer: Passwatch blows Rest}
TTH-D2.03 CADET (TWO): (from the far stake, arms up) "Oi. I'm still out."
TTH-D2.04 CADET (TWO): (walking down) "They blew Rest. Nobody waited."
TTH-D2.05 CADET (ONE): "Drill says you're dead in a drift."
TTH-D2.06 CADET (TWO): "Drill can come up here and be dead in a drift."
      {wolves on the ridge: TTH-E1 starts}
TTH-D2.10 [after TTH-E1] CADET (ONE): "They answered the horn. Wolves always answer Lost. They think it's one of them."
TTH-D2.11 CADET (TWO): "So the wolves have more replies than we do."   {set TTH_DRILL_SEEN}  {event: S03_corner_drill}
```

```
TTH-D3.01 THYRA: "Three Calls Shelter. Twelve beds, eight blankets, one host. Which are you?"
  > "I'm on Dorn's drill. The stones."                     → TTH-D3.05
  > "Just passing."                                         → TTH-D3.02
TTH-D3.02 THYRA: "Then pass. Mind the haulier's boy, he skips into people."   → end
TTH-D3.05 THYRA: "That was you blowing Lost at my stone. The kettle jumped."
TTH-D3.06 THYRA: (blows Lost from the Shelter Stone herself, flatly) "There. Your drill's done. My grandmother's map's inside, since you're going to ask."
TTH-D3.10 THYRA: "I paint it over every spring. Not the corner. You don't paint over the corner."   {event: S05 dialogue condition; map inspectable}
  > [3 map inspects] "Two and the rise. Keep the beds. What does it mean?"    → TTH-D3.15
TTH-D3.15 THYRA: "Means what it says. A stone blows two and the rise, you keep beds. Somebody's still coming."
TTH-D3.16 THYRA: "Hosts kept beds by the count on the map. My grandmother kept them till thaw once."
TTH-D3.17 THYRA: "She wrote everything. Bed books. In the chest."
TTH-D3.20 THYRA: (opens the chest; finds the wolf-tooth book) "Hers. Don't lick your thumb."   {bed book inspectable}
  > [3 book inspects] "This page. 'No third.'"            → TTH-D3.30
TTH-D3.30 THYRA: "That's when she stopped keeping the fourth bed."
TTH-D3.31 THYRA: "Doesn't say why. She'd write a goat sneezing. She didn't write why."
TTH-D3.32 THYRA: "Ask the children what the third call is. They'll tell you. They're wrong, but they'll tell you."
```

```
TTH-D4.01 [TFS Completed] (inner voice, prompt line) "The First Smoke rhyme. You've heard the end of it before."
TTH-D4.02 CHILD (GRANDDAUGHTER): (still skipping) "Third call's when you're too late."
TTH-D4.03 CHILD (HAULIER'S BOY): "For supper."
TTH-D4.04 CHILD (GRANDDAUGHTER): "No, for the gate. The gate shuts and you're too late."
TTH-D4.05 CHILD (HAULIER'S BOY): "My da says it's supper."
  > "Who taught you the rhyme?"                            → TTH-D4.10
  > "Thank you."                                            → TTH-D4.20
TTH-D4.10 CHILD (GRANDDAUGHTER): "Nobody teaches it. You just know it. Like the cold."   → TTH-D4.20
TTH-D4.20 THYRA: (from the door) "They've sung it for forty years. Same words every winter. Nobody asks what they mean."
      {event: S07_verse}
```

```
TTH-D5.01 DORN: "Well. What's missing."
  > [TTH_DRILL_SEEN] "A reply that says someone's still out. Answer can't say it."   → TTH-D5.05
  > "Show me the board."                                   → TTH-D5.06
TTH-D5.05 DORN: "No. It can't." (beat) "Build it, then. The pegs are in the box."  → TTH-D5.06
TTH-D5.06 {peg board opens}
TTH-D5.10 [three wrong tries] DORN: "The map gives you the front. Two dots. The rhyme gives you the end. 'Third call.' Third."
TTH-D5.11 DORN: "What's the third thing after two short that a child would know?"   {hint: board pre-set to short, short, [empty]}
TTH-D5.20 [correct] DORN: (long look at the row) "Two short and the rise. Lost's tail on Answer's head."
TTH-D5.21 DORN: "Heard. Someone's still out." (beat) "Go on. Blow it. If it brings anything up the pass, it'll be Ressa."
      {event: S08_compose}
```

```
TTH-D6.01 RESSA: (coming up the post steps, unhurried) "That's not on the board."
TTH-D6.02 [TTH_RETURN_HEARD] (optional ask, any time in this node)
  > "At the Narrows, my Answer came back with the rise on it."           → TTH-D6.03
TTH-D6.03 DORN: "Wind tricks." (he doesn't smile) "Faces do that."
TTH-D6.04 RESSA: "Faces do all sorts. It doesn't go in the code because a cliff did it."   → TTH-D6.05
TTH-D6.05 RESSA: "My order says Answer from the stones. I didn't write it. I keep it, because somebody had a reason."
TTH-D6.06 [TPW_NAMES_ASKED] RESSA: "You asked Vessa who was outside, the night we shut Passwatch. Same question. With a horn on it."
TTH-D6.07 RESSA: "I won't refuse a reply. A reply's honest."
TTH-D6.08 RESSA: "But that one's a promise. 'Someone's still out' means somebody stays till they're in. Who stays?"
  > "Every child. Put it on the board with the rest."                        → TTH-D6.10
  > "Wardens and hornbearers. People who'll stay out for it."                 → TTH-D6.20
  > "The shelters. It meant keep the beds. Give it back to the people with beds."  → TTH-D6.30
TTH-D6.10 RESSA: "Then children will blow it at goats." (beat) "And every child will know it. Fine."
TTH-D6.11 RESSA: (writes along the board's edge with a nail) "'Blow the third, keep the watch.'"   {set TTH_KEEPER = board; set TH_THIRD_HORN}  → TTH-D7.01
TTH-D6.20 RESSA: "Warden code, then. Whoever blows it holds the stone till the last one's in. I'll write it tonight."
TTH-D6.21 DORN: "Highsteads won't know it."
TTH-D6.22 RESSA: "Highsteads will know a warden standing on a stone in the snow."   {set TTH_KEEPER = wardens; set TH_THIRD_HORN}  → TTH-D7.01
TTH-D6.30 RESSA: "Hosts." (beat) "They'll carry it. They carry everything."
TTH-D6.31 RESSA: "Tell Thyra. She'll swear. Then she'll repaint the corner."   {set TTH_KEEPER = hosts; set TH_THIRD_HORN}  → TTH-D7.01
```

```
TTH-D7.01 DORN: (cuts a rising peg from the box, sets it in the seventh row, thumbs it home) "There."
TTH-D7.02 DORN: "Thirty years that hole's been looking at me."
TTH-D7.03 [TF-M3 Completed] DORN: "If it had been on the stones at the Seat..." (stops) "Roster says what it says."
TTH-D7.04 DORN: "There's another one. Not on any board. Two long and one held. Ressa was taught it once. Nobody taught me."
TTH-D7.05 DORN: "Ask her. Don't ask her today."
      {event: S10_keeper → quest Completed; TWG becomes available}
```

**Post-quest (by `TTH_KEEPER`):** DORN [board]: *"Children have learned it in a day. Took me thirty years to unlearn it."* / RESSA [wardens]: *"Two wardens stood the Corner Stone all night for a haulier. He'd stopped for a drink."* / THYRA [hosts]: *"Fourth bed. Made. Don't sit on it."*

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| TTH-I1.01 | Seventh row: the hole | *"Two short pegs, thumb-smooth. Then a hole gouged wider than a peg, as if it was prised out in a hurry."* |
| TTH-I1.02 | Seventh row: label (raked) | *"Scraped back to wood. In the lantern's slant, the ghost of a painted line: rising."* |
| TTH-I1.03 | Spare peg box | *"Every peg shape. The rising pegs are clean. Nobody's used one in a long time."* |
| TTH-I1.04 | Gate Stone | *"A mouth-hollow at horn height. Cut on its face: a rising line, then two dots."* |
| TTH-I1.05 | Corner Stone | *"Two elbow dips worn in the top. Wolf scat on the lee side. Fresh."* |
| TTH-I1.06 | Narrows Stone flutes | *"The flutes above run upward. Snow lies in them in thin, neat lines."* (autumn: *"Grit lies in them…"*) |
| TTH-I2.01 | Horn map: the line | *"The pass as one long line. Four circles for the stones. Beside each, a rising line, and then its reply."* |
| TTH-I2.02 | Horn map: the replies | *"At the Gate and the Corner, the reply is two dots. At the Narrows and the Shelter, two dots and a rising line."* |
| TTH-I2.03 | Horn map: the legend | *"Smoke-dark, but legible: 'Two and the rise: keep the beds.'"* |
| TTH-I2.04 | Bed book (optional) | *"'Fourth bed. He came in at thaw. Ate everything. Sang. Left.'"* |
| TTH-I2.05 | Bed book: kept beds | *"'Third horn from the Narrows stone at dusk. Kept four beds. Three came.'"* |
| TTH-I2.06 | Bed book: till thaw | *"'Kept the fourth till thaw.' Below it, a line ruled across the page, and nothing more for that winter."* |
| TTH-I2.07 | Bed book: the order | *"A page on its own: 'Wardens' word: answer with two from the stones. No third.' No date. No name. The next page lists beds by count, and the fourth bed is never kept again."* |

#### Document: the children's rhyme (TTH-I3; canonical text owned by TFS)

*The canonical text is authored in* First Smoke *(TFS.14, `…_Work_and_Skills.md`) and quoted here word for word. At Three Calls the children skip to it instead of clapping: the rope stops for one beat where the clap stops.*

```
One for the gather, two for the gate,
Wind at the window, supper's on the grate.
Long for the lost one, short for the near,
Third call's too late, and nobody's here.
(clap, clap, stop.)
```

*(Independent review: the earlier Three Calls variant with a changing last word was cut so the verse has one text across the slate.)*

---

## TWG — Witness at the Gate

### TWG.1 The quest in one paragraph

Ressa Highcrag was taught one call she has never blown on duty: two long, one held. She remembers what her teacher told her it was for, and nothing else: "For strangers." If it was ever cut anywhere, she says, it was cut into the **Old Watchfire Line**, the ruined horn towers along the Ridgewall crest whose parapets carry **grooves** shaped to throw each call clean to the next tower. The player climbs the towers. At the first, they read the groove bank by hand and breath and match six channels to the Ordinary Calls; the seventh matches nothing: two long troughs and a third that ends in a closed cup. At the third tower they rebuild the shape and hold the note, and the call is **taken**: the fourth tower's groove carries it, then the fifth, then the sixth, receding along the ridge, and then it drops over the lip of the **Silent Gorge** and stops as if a door had shut. Pass bandits holding the fourth tower as a lookout heard it and did not like it. At the sixth tower a lintel names the call, *WITNESS AT THE GATE*, and its groove points down into the gorge, not at any tower. Below, in the null-point where no sound carries, stand two worn gateposts with no gate between them and a stone bench with four cup-hollows worn into it. The player blows the call there and hears nothing at all, and the frost on the bench slides slowly into the hollows. Back at Passwatch, Ressa listens to it once and says "For strangers" again, and nothing more. The player decides whether Thornfell writes it down, blows it at the gate as a courtesy with no meaning, or leaves it in the stone.

**Remember:** a call travelling away from you along a ridge, tower by tower, and stopping. **Want next:** to know who the strangers were (never answered in Thornfell; R16, CV-M1).

### TWG.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| **A. An old warden explains the custom.** | Rejected. R16's rule: an unexplained custom in its own region (Revelation Ledger R16). |
| **B. The towers "replay" the call's meaning (voices, a vision).** | Rejected. No phenomenon testifies (C11; bible §11.3). |
| **C. Read the grooves → decode by echo → follow the call to where it ends → find a place shaped for something nobody remembers → Ressa's one memory → custody choice** (selected). | **Selected.** Climbing and decoding are the gameplay; the meaning stays absent, and absence is the seed. |

| Element | Source | Status |
|---|---|---|
| Old Watchfire Line: horn towers with acoustic grooves | Bible TP22, TDS03 | [CANON feature]; tower count and details [NEW] |
| The Silent Gorge: a null-point created by Echohewn architecture | Dossier §XII; bible TP18, TDS01 | [CANON] |
| Witness at the Gate: two long, one held; Ressa: "for strangers"; meaning not recovered | Bible §9.4, §7.1 | [NEW] |
| R16 seed: "a Thornfell horn call meaning 'witness at the gate'", planted as an unexplained custom | Revelation Ledger R16; H07 | [APPROVED — FT-01] (R16 truth); the custom never named here |
| Pass bandits using cliff hideouts and relay horns | Dossier (enemies); bible §10 | [CANON family] |
| Lintel, gateposts, four-hollow bench, groove bank of seven, the call running the line | This package | [NEW] |

### TWG.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `thornfell.side.witness_at_the_gate` |
| Series | *Horn and Silence*, part 2 of 3 |
| Type | Environmental |
| Unlock | TTH Completed. Offered by Ressa at Passwatch on the player's next visit after TTH (`TWG-D1`); alternatively, inspecting a groove bank on the Old Watchfire Line (TDS03) with TTH Completed starts the quest at `S01` and Ressa's node becomes the hand-in. |
| Length | 35–45 minutes |
| Combat share | ~20% (one bandit fight) |
| Skills | Melee or Ranged (encounter); agility triggers (optional) |
| Choice | What Thornfell does with the call (`TWG_CALL`: recorded / greeting / left) |
| Outputs | `TWG_CALL`; the Old Watchfire Line traversal route; R16 seed placed |
| **Anchor** | Ridge Wardens (Ressa) and the Old Watchfire Line as a place. |
| **World-truth row** | H07 (a prewar custom of witness at passes), **seed only; never named**. H11 (horn codes) as practice. |
| **Revelation role** | **Plants R16.** The call, its name on a lintel and Ressa's "for strangers" are the Thornfell seed. Nothing in Thornfell explains it. |
| **Recurring evidence** | The **tower grooves and the lintel** (place; permanent in every outcome). Ressa's testimony (one line). With `recorded`, Dorn's **code book** (record; custodian: the Hornbearers), which TNK may keep or prune. The convergence's "horn rosters" custodian is satisfied by the grooves in every case. |
| **State compliance** | Inactive → Active on `TWG-D1` end or groove inspect; Completed on `TWG-D6` end. No fail path; choice recorded in `TWG_CALL`. Resume hook: Ressa at the Passwatch gate (`TWG-B1.03`). |

### TWG.4 The places

**MAP VERIFICATION REQUIRED:** the Line runs along a Ridgewall crest; Tower 1 is the end nearest the Windscar track, Tower 6 the end above the Silent Gorge. The TME05 ledge (*The Horn That Never Fell*) is above the Line (bible §7.3); this quest does not use it.

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **T1. First tower** | Read the groove bank | Squat tower, stair intact. On the parapet, a **groove bank**: seven channels cut into a dressed stone, each a different profile, all aimed along the crest at Tower 2. Old fire-scorch on the floor stones. Six channels are polished by use; the seventh is clean. | Stair. |
| **T2. Second tower** | Ladder carry | Stair collapsed into rubble. A Warden's ladder lies half-buried in snow below (left by a repair party, rungs tarred). | **Agility:** rubble climb. **Fallback:** carry the ladder (carry-state, slow walk) and set it against the breach (2 s channel). |
| **T3. Third tower** | Decode; strange moment | Upper floor half gone, parapet whole. Its seventh channel is packed with old ice. A wren's nest in the Gather channel. | Stair to a ledge, then a short scramble (fallback: steps cut in the inner wall). |
| **T4. Fourth tower** | TWG-E1 (bandit lookout) | Bandits' lookout: a hide of goat hides on the floor, a pot, a sling-stone pile, a chalk tally of carts seen on the track below. Their own crude marks beside the Gather channel: a stick-man and three dots. | Stair (bandit-held). |
| **T5. Fifth tower** | Wind windows | Exposed shoulder; the parapet is ice-sheathed. Fluted rock beside the tower whistles a fifth before each gust. Chalked shelter faces. | Parapet walk between gusts (fallback: interior stair, longer, same gusts at the windows). |
| **T6. Sixth tower** | Lintel | The end tower. Above its parapet groove bank, a lintel stone cut in old square letters: **WITNESS AT THE GATE**. Its seventh channel is cut at a steep downward angle: not along the crest, but **down into the gorge**. | Stair. |
| **G1. The gorge stair** | Descent | Steps cut down the gorge side, iced. A rope anchor ring at the top. | **Agility:** rope descent from the ring. **Fallback:** the cut stair. |
| **G2. The gateposts** | The null-point; second strange beat | At the gorge floor, two worn stone posts, shoulder height, a cart's width apart, with **no gate and no hinge marks**. Between them, against the gorge wall, a long stone bench with **four cup-hollows** worn into its seat at even intervals. Snow falls straight down. Footsteps vanish. The player's own voice (any emote) is flat and close. | Walk. |

### TWG.5 Player-facing sequence

**Beat 0 — For strangers (`S00_hook`).** *Objective: Ask Ressa about the call nobody blows.* `TWG-D1`. Ressa gives the one memory and points to the Line.

**Beat 1 — The first groove bank (`S01_read_bank`).** *Objective: Read the grooves on the first tower.* Seven channel inspects; for six, the player matches the glyph to the channel (the inspect describes the cut; a glyph picker confirms; any wrong match gets a line and lets them try again). The seventh matches nothing (`TWG-I1.07`).

**Beat 2 — Along the line (`S02_second_tower`).** *Objective: Get onto the second tower.* Rubble climb or ladder carry.

**Beat 3 — Decode (`S03_decode`).** *Objective: Find the call the seventh groove was cut for.* At T3 the seventh channel is iced; clear it (3 s channel, `chip_ice`). Then compose on the peg board. **The test is the echo** (bible §1.1): blown into the right groove, a shape that fits returns one clean echo off Tower 4's parapet; a shape that does not fit returns a smeared, doubled echo. The **held** peg is a hold of 5 s on the call interaction with a breath bar; releasing early plays it short (and smears). Hints come from the groove itself (`TWG-I1.07`: two long troughs and a closed cup). On **long, long, held** the strange moment (TWG.7, part 1) fires: the call is taken down the line.

**Beat 4 — The lookout (`S04_lookout`).** *Objective: Get past the fourth tower.* The bandits heard the call run past them. **TWG-E1.** Defeat the crew. (The slinger's groove call in the fight shows the bandits using the Gather groove; no post-fight talk.)

**Beat 5 — The shoulder (`S05_shoulder`).** *Objective: Cross to the sixth tower.* T5 parapet in wind windows. No combat.

**Beat 6 — The lintel (`S06_lintel`).** *Objective: Read the end tower.* Required inspects: the lintel and the downward-cut seventh channel.

**Beat 7 — The gate with no gate (`S07_gorge`).** *Objective: Follow the groove down.* Descend the gorge stair. In the null-point, three required inspects (the gateposts, the bench, the falling snow). Optional: blow the call at the bench (strange moment part 2). The step completes on the three inspects whether or not the player blows.

**Beat 8 — Ressa (`S08_ressa`).** *Objective: Tell Ressa what you found.* At the Passwatch gate. The player may blow the call for her (dialogue option). `TWG-D4`. The choice.

**Beat 9 — Dorn (`S09_close`).** *Objective: Tell Dorn.* `TWG-D6`. Quest Completed.

### TWG.6 Encounters

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TWG-E1** | 2 × Pass Bandit cutter, 1 × Pass Bandit slinger (lookout) | T4: cutters on the stair landing and floor, slinger on the parapet | Cutters: Aggressive, hold the stair. Slinger: Defensive at range; moves to the Gather channel to call help. | **Cutter:** drops the blade behind the hip (~1.0 s), then a two-cut rush. **Slinger:** the sling whirrs overhead (~1.4 s, a rising whirr: a sound tell), then a stone; strafe beats it. **Groove call:** slinger steps to the parapet and leans to the channel (~2.0 s); if not interrupted, one more cutter comes up from the scree (once). Interrupt: any hit, or the player blowing **Fall**, which makes every bandit duck for 1 s (once per fight; they know the calls too). | A readable mixed fight on a tight tower floor; calls as tools. | 50–75 s; player at 60–80% HP. |

**Rules.** Bandits fight until defeated at 0 HP (CDR-1). The former lookout talk (`TWG-D2`) was flavour and is cut (rulings §3.2 T-4); nothing about the call depends on it. After the quest the T4 hide stays empty. Death respawns at T1 (or at T6 once reached); E1 stays defeated once won.

### TWG.7 The strange moment: the call runs the line, and stops

**Part 1 — Tower 3, on the correct composition (required).**

| Time | Element | Spec |
|---|---|---|
| 0–6 s | **The call** | The player blows long, long, held (held = 5 s). Glyph: two bars and a bar with a closed end. This glyph appears **only** in this quest's UI (bible §9.4). |
| 6–7 s | **The clean return** | One clean echo off T4's parapet, slightly late. |
| 7–9 s | **T4 takes it** | T4's seventh groove sounds the call itself, quieter, in the horn's timbre but hollower (stone in it). |
| 9–11 s | **T5** | Fainter, further along the crest. |
| 11–13 s | **T6** | Faint. The held note at T6 bends **downward**. |
| 13–14 s | **The stop** | The held note drops over the gorge lip and **cuts off mid-hold**, not fading: stopping. All ambient wind drops 30% for 2 s. |
| 14 s+ | **Ordinary** | Wind returns. A wren in the T3 Gather channel complains. |
| Inspect | Inner voice | *"It went on without you. Tower to tower. Then over the edge, and gone, as if something shut."* |
| UI | No objective update until 16 s. No music. |

**Part 2 — the gateposts, optional (the player blows the call in the null-point).**

| Time | Element | Spec |
|---|---|---|
| 0–6 s | **Silence** | The call animation plays; **no sound at all** (null-point rule: resonance cannot carry; bible §1.1). No glyph appears. |
| 2–10 s | **The bench** | The frost on the bench seat creeps slowly, in two long pulses and one long held one, into the four cup-hollows, and stops. Snow keeps falling straight down. |
| Inspect | Inner voice | *"You heard nothing. The frost moved anyway: into the four hollows, and no further."* |
| What it means | Nothing provable. Stone carries what air cannot; or the player's breath warmed the stone. Never explained. It proves nothing about who sat here. |

### TWG.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_hook` | Ask Ressa about the call nobody blows. | `TWG-D1` end, or first groove-bank inspect with TTH Completed | Yes |
| `S01_read_bank` | Read the grooves on the first tower. | 6 glyph matches + seventh-channel inspect at T1 | Yes |
| `S02_second_tower` | Get onto the second tower. | Enter T2 top volume (agility or ladder) | Yes |
| `S03_decode` | Find the call the seventh groove was cut for. | `chip_ice` (3 s) + `call-blown` (long, long, held) in T3 seventh-channel volume | Yes |
| `S04_lookout` | Get past the fourth tower. | TWG-E1 defeated | Yes |
| `S05_shoulder` | Cross to the sixth tower. | Enter T6 volume | Yes |
| `S06_lintel` | Read the end tower. | Lintel inspect + downward-channel inspect | Yes |
| `S07_gorge` | Follow the groove down. | Enter G2 + 3 inspects (gateposts, bench, snow) | Yes |
| `S08_ressa` | Tell Ressa what you found. | `TWG-D4` choice resolved | Yes |
| `S09_close` | Tell Dorn. | `TWG-D6` end | Yes (→ Completed) |

### TWG.9 Flags

| Flag | Set by | Read by |
|---|---|---|
| `TWG_FROST_SEEN` | Strange moment part 2 | `TWG-D4.06` option |
| `TWG_LADDER_SET` | Fallback at T2 | Ladder stays (world prop, per player) |
| `TWG_CALL` = recorded / greeting / left | `TWG-D4` | TNK code book; Passwatch gate barks; CV-M1 (request) |

### TWG.10 Choices and consequences

Ressa's line in every option: she will not put a meaning on a call she cannot explain. A warning nobody can explain is a rumour (accountable warning, anchor limit).

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Recorded** — *"Write it in the code book. With what we don't know."* | Dorn writes a page: *"Witness at the Gate. Two long, one held. 'For strangers' (R.H.). Meaning not known. Not to be blown as a warning."* | A page with no meaning invites one. Ressa: "Somebody will explain it. Wrongly. In a tavern." Within a few days a Passwatch bark has it as "the call for ghosts" (`TWG-B2.01`). | TNK: the page is on the table (keep or prune). CV-M1 custodian: the code book. |
| **Greeting** — *"Blow it at the gate when strangers come. A courtesy. Nothing more."* | Ressa agrees to have it blown at the Passwatch gate when a stranger party arrives, "and it means hello, and it means nothing else". | Some Wardens dislike announcing strangers to the whole pass (bark). Strangers ask what it means and nobody can tell them, which is awkward every time. | Passwatch plays it for arrivals (ambient, per player). TNK: it is a practice, not a page. CV-M1 custodian: Passwatch's practice. |
| **Left** — *"Leave it in the stone. It kept this long."* | Nothing is written. Dorn: "Then it's yours. And the towers'." | If the player forgets it, nobody remembers it. Dorn is uneasy about a call only a walker knows. | TNK: Dorn mentions it once and moves on. CV-M1 custodian: the grooves and lintel (always present). |

None is wrong. None tells anyone what the call meant.

### TWG.11 Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| **Witness at the Gate** | Knowledge | Added to the player's calls with its glyph. It does nothing mechanically anywhere in Thornfell. |
| **The Line route** | Access | The six towers become a traversal route along the crest (ladder left at T2; ice cleared at T3), with a view of Windscar and the Silent Gorge. |
| Small payment | Currency | Ressa: "for the ladder". Economy tuning. |
| Skill XP | Actions only | Melee or Ranged. |
| *The Notes We Keep* | Story | Available once TF-M4 is also Completed. |

### TWG.12 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Can't hold the note 5 s | Breath bar refills instantly; unlimited retries. Accessibility option: "held" as a toggle (press to start, press to stop). |
| Wrong glyph matches at T1 | Line and retry. |
| Fall from the T5 parapet | Gusts knock down, never off. The walkable stair route is always available. |
| Death | Respawn at T1 (or T6 once reached). Steps, the set ladder, cleared ice and defeated bandits persist. |
| Walking away | Stays Active. Resume: Ressa at the gate (`TWG-B1.03`), or simply returning to the Line. |
| Fail state | None. |
| Co-op | Each player decodes their own call; strange moments are per player (a partner hears an ordinary echo and nothing travelling). Bandits shared. Choice per player; Passwatch's greeting ambience follows each player's own `TWG_CALL` (fallback: the host's). |

### TWG.13 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| **Held call** | Systems / UI | Call interaction with a hold duration and a breath bar; emits shape with "held" if ≥ 5 s. Toggle option for accessibility. |
| **Echo-quality test** | Audio / Systems | Two authored returns per groove (clean / smeared), chosen by shape match. **Fallback:** inspect line ("The echo comes back clean." / "…smeared.") |
| **The call running the line** | Audio | One authored positional sequence across T4–T6 and the gorge lip with a hard cut, plus a 2 s wind-duck. Per-player. **Fallback:** the clean echo and the inspect line. |
| **Null-point volume** | Audio / Systems | Zone that mutes player-generated sound and gust audio; snow particles fall vertical. Shared with TF-M4 and TGM conventions. |
| **Frost creep decal** | Art | One-shot animated decal on the bench, per player. **Fallback:** inspect text. |
| **Carry-state ladder + set point** | Systems | Slow-walk carry; deposit volume converts it to a climbable prop (per player; fallback: shared once set). |
| Glyph matcher at a groove bank | UI | Pick a glyph per channel; compare to a table. **Fallback:** dialogue options. |
| Creatures | Encounters package | Pass Bandit cutter, slinger (with groove-call behaviour and Fall-duck reaction). |
| **R16 custody note** | Convergence author | CV-M1 reads TWG Completed and `TWG_CALL`. The lintel and grooves are permanent world props. |

### TWG.14 Mystery ledger, open decisions, review

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Witness at the Gate** | A prewar call sounded when another region's witnesses came to a pass (H07). The Silent Gorge gateposts are where they were met and seated. (Author knowledge only.) | Nothing; or "for ghosts" (`recorded` bark). | Grooves, lintel, downward channel, the gateposts and bench, Ressa's "for strangers". | A call to welcome the enemy; a call for the dead; a smuggler's signal. | **All of it, in Thornfell.** No line names the custom or the Concord. | R16 (CV-M1). |
| **Why the call stops at the gorge** | The null-point. Whether the builders meant the call to be heard only by whoever sat between the posts is unknown even to the author. | — | The stop; the frost. | The gorge "swallows" calls. | **Never explained.** | Never. |

**Open decisions.** (1) Tower count: six is the design; four is the minimum (T2's ladder and T5's wind windows can merge). MAP VERIFICATION REQUIRED. (2) Whether the four hollows are too pointed a seed for R16 (four regions). Recommendation: keep; nothing in Thornfell counts them aloud. **[PROPOSAL — DIRECTOR]** (3) Request the bible owner add the call running the Line and the frost to §7.4's unexplained list.

| Review finding | Revision |
|---|---|
| A first draft had Ressa tell a story about strangers at the gate. | Cut to one memory, three words. Her other lines are about not putting a meaning on it. |
| The null-point fight was considered for the gorge. | Rejected: TGM owns combat in a null-point. The gorge is a quiet place to look at. |
| The "greeting" option risked implying welcome to Emberholt. | Ressa's line limits it to "hello, and nothing else"; no faction is named. |
| The call running the line risked reading as magic. | Grooves are acoustic (bible §1.1, H05 Echohewn acoustic engineering); the effect is sound carried by cut stone. No light, no music. |
| Crossing Concord risked being named in Dorn's code-book page. | Page text fixed: shape, Ressa's three words, "meaning not known". |

### TWG.15 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Ressa Highcrag** | That she was taught the call and told "for strangers". That it was not a warning. | Which strangers; why it stopped; the gateposts. | Short. Distrusts any call she can't explain to the person who hears it. |
| **Dorn Feldhorn** | The code book's form. | The call (he was never taught it). | Wants it written down; afraid of what people will put in the gap. |
| **Bandit lookout** (role name) | Nothing spoken (TWG-D2 removed: CDR-1). Combat role only. | — | — |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| TWG-B1.01 | Ressa | Available (after TTH) | *"Dorn's been telling walkers about my calls again."* |
| TWG-B1.03 | Ressa | Active, before `S08` | *"Towers are where they always were. Up."* |
| TWG-B2.01 | Passwatch warden | Completed, `TWG_CALL` = recorded | *"There's a page in the book for the ghost call now. Two long and a held. Don't blow it near me."* |
| TWG-B2.02 | Passwatch warden | `= greeting`, stranger arrival | *"That's the hello. Means hello. Stop asking."* |
| TWG-B2.03 | Dorn | `= left` | *"Still in the stone, is it. Good. I don't have to think about it."* (He does.) |
| TWG-B3.01 | Player inner voice | Entering G2 | *"Your footsteps stop being there."* |

#### Nodes

```
TWG-D1.01 RESSA: "Dorn says you want the other one."
TWG-D1.02 RESSA: "Two long, one held. I was taught it. I've never blown it on a stone."
  > "What's it for?"                                       → TWG-D1.10
  > "Who taught you?"                                       → TWG-D1.05
TWG-D1.05 RESSA: "A warden. Long dead. He taught me forty calls and that one last, and said I'd not need it."   → TWG-D1.10
TWG-D1.10 RESSA: "For strangers." (beat) "That's all he said. That's all I have."
TWG-D1.11 RESSA: "If it was cut anywhere, it was cut into the old watchfire towers. Every call had a groove there."
TWG-D1.12 RESSA: "Go and see if they cut that one. If they did, it was a real call. If not, it was an old man's joke."
      {event: S00_hook}
```

```
TWG-D2.01 (removed: CDR-1)
TWG-D2.02 (removed: CDR-1)
TWG-D2.10 (removed: CDR-1)
TWG-D2.11 (removed: CDR-1)
TWG-D2.20 (removed: CDR-1)
  (Former post-yield lookout talk; flavour only, cut per rulings §3.2 T-4. S04 completes on TWG-E1 defeated.)
```

```
TWG-D4.01 RESSA: "Well. Did they cut it?"
  > "On every tower. The end tower names it. 'Witness at the Gate.'"        → TWG-D4.05
TWG-D4.05 RESSA: (quiet a moment) "Witness at the gate."
TWG-D4.06 [TWG_FROST_SEEN] (optional ask)
  > "At the bottom of the gorge there are gateposts. No gate. A bench. It's silent."   → TWG-D4.07
TWG-D4.07 RESSA: "The Silent Gorge. Nobody goes down. Children dare each other to shout in it." (beat) "I've never seen posts."
  > "Shall I blow it for you?"                               → TWG-D4.10
  > "What do you want done with it?"                         → TWG-D4.20
TWG-D4.10 {player blows long, long, held at the gate; Ressa listens to the end}
TWG-D4.11 RESSA: "That's it." (beat) "For strangers."
TWG-D4.12 RESSA: "Don't ask me which. I've told you everything I was given."   → TWG-D4.20
TWG-D4.20 RESSA: "I won't put a meaning on it. A call has to mean the same to the one who blows it and the one who hears it."
TWG-D4.21 RESSA: "That one means nothing to anyone alive. So what do we do with it?"
  > "Write it in the code book. With what we don't know."                       → TWG-D4.30
  > "Blow it at the gate when strangers come. A courtesy. Nothing more."         → TWG-D4.40
  > "Leave it in the stone. It kept this long."                                 → TWG-D4.50
TWG-D4.30 RESSA: "Dorn will like that. He likes a page." (beat) "Somebody will explain it. Wrongly. In a tavern."   {set TWG_CALL = recorded}  → TWG-D6.01
TWG-D4.40 RESSA: "When strangers come up the pass, the gate blows it. It means hello." (beat) "And it means nothing else. I'll say that to every warden twice."   {set TWG_CALL = greeting}  → TWG-D6.01
TWG-D4.50 RESSA: "In the stone." (nods) "Stone doesn't make things up."   {set TWG_CALL = left}  → TWG-D6.01
```

```
TWG-D6.01 DORN: "Ressa says you found it. Cut on six towers and nobody blew it for longer than I've been alive."
TWG-D6.02 [TWG_CALL = recorded] DORN: (writes slowly) "'Meaning not known.' Hardest thing I've written in that book."
TWG-D6.02 [TWG_CALL = greeting] DORN: "A hello. Fine. Better than a ghost."
TWG-D6.02 [TWG_CALL = left] DORN: "Then you know a call I don't. Don't blow it at me."
TWG-D6.03 [TF-M4 Completed] DORN: "And Ressa's got Eyvind's plates on her mind. And the whole book's coming apart. Come up to the terrace when you can." [SPLINTER]
TWG-D6.03 [else] DORN: "Some day the whole book wants going through. Not today."
      {event: S09_close → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| TWG-I1.01–.06 | T1 channels (Ordinary) | Rest: *"One long, flat trough."* Close: *"Two long troughs, each lower than the last."* Gather: *"Three short cups in a row."* Fall: *"A short cup, a long trough, a short cup."* Lost: *"One long trough that climbs."* Answer: *"Two short cups."* |
| TWG-I1.07 | T1 seventh channel | *"Two long troughs. Then a third that doesn't run out: it ends in a closed cup, as if the sound were meant to stay. Clean. Never polished by use."* |
| TWG-I1.08 | T4 bandit tally | *"Chalk strokes for carts on the track. Three crossed through. One drawn with a big wheel and 'RICH?'."* |
| TWG-I1.09 | T6 lintel | *"Old square letters, worn but deep: WITNESS AT THE GATE."* |
| TWG-I1.10 | T6 seventh channel | *"Cut steeply downward. Not along the crest. Into the gorge."* |
| TWG-I2.01 | Gateposts | *"Two posts, a cart's width apart. No hinge marks. No gate was ever hung here."* |
| TWG-I2.02 | Bench | *"A long stone bench against the gorge wall. Four cup-hollows worn into the seat, evenly spaced, as if by people who sat a long time."* |
| TWG-I2.03 | Snow | *"It falls straight down. Nothing moves it."* |

---

## TNK — The Notes We Keep

### TNK.1 The quest in one paragraph

Thornfell's code book is coming apart at the stitching, the ridge's ordinary horns have split their sleeves in the cold, and the Assembly's new closure account wants every closing written with the calls that ordered it. Ressa and Dorn meet at the **Signal Terrace** in Stonewake to copy the book fresh, and find they do not agree on what goes in it. The Third Horn is back. Witness at the Gate is wherever the player left it. The Split has a name and no shape, and Dorn wants the name kept so nobody forgets why it is not played; Ressa wants it gone so nobody is tempted to find it. Under the terrace, or up at the Summit, the Wall-Horn's plates wait wherever `TH_HORN` put them, and **Eyvind Stall** `[SPLINTER]`, held by the Ridge Wardens until the Assembly decides about him, has offered to tune every horn on the ridge in a week if someone will let him near "his" plates again. Nobody will. The player settles the plates' custody (they are **never reinstalled in any horn**), retunes three of the ordinary horns by ear at the practice face, with or without Eyvind's help on ordinary horns only, and sits with Ressa and Dorn through the book page by page. Then, from the terrace, the player sounds the calls Thornfell has kept, one by one, and every tower post on the ridge answers in turn. If the forgotten call was kept, Dorn sounds it last, and nothing answers at all.

**Remember:** the ridge answering you, post after post, and one call that nobody can answer. **Want next:** the day these calls have to carry further than Thornfell (CV-M2).

### TNK.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| **A. Build a better, louder alarm horn from the plates.** | Rejected. Ressa's limit (no new horn weapons); bible §7.1: plates are never reinstalled. |
| **B. A debate scene at the Assembly.** | Rejected. Talk-led; the Assembly is TF-M5's. |
| **C. Plate custody → retune by ear → the book page by page → performance with distant replies** (selected). | **Selected.** Every decision is attached to a physical act: a crate, a sleeve, a page, a call. |

| Element | Source | Status |
|---|---|---|
| Signal Terrace for horn codes at Stonewake | Dossier §VI.1; bible TP01 | [CANON] |
| Ressa refuses certain calls but keeps the horns; refusals concern accountable warning, never new horn weapons | Anchors §IV; Part 3; bible §5.1 | [CANON] / limit |
| Dorn maintains code continuity | Anchors §IV; Part 3 | [CANON] |
| The Wall-Horn's plates; `TH_HORN` silenced / broken / surrendered | Bible §2.3, TF-M4 | [NEW] |
| Eyvind Stall, hornwright, careless craftsman | Bible §5.2 | [NEW] `[SPLINTER]` |
| Kaldren keeps silenced plates; reports stresses only | Bible TF-M4; character ledger | [NEW] / limit |
| Eyvind held by the Ridge Wardens pending the Assembly (as Act II sets it); the code book; the practice face; sleeve tuning | This package | [NEW] |

### TNK.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `thornfell.side.the_notes_we_keep` |
| Series | *Horn and Silence*, part 3 of 3 (finale) |
| Type | Settlement/finale |
| Unlock | TF-M4 Completed (`TH_HORN` set) **and** TWG Completed. Offered by Dorn at the Signal Terrace (`TNK-D1`). While TF-M5 is Active, the offer waits (`TNK-B1.01`); see TNK.12 open decision 1. |
| Length | 30–40 minutes |
| Combat share | 0% by design |
| Skills | Smithing (sleeve fitting; crew alternative: Dorn's apprentices) |
| Choices | Plate custody (`TNK_PLATES`, 2–3 options by `TH_HORN`); Eyvind's help (`TNK_EYVIND`); the code (`TH_HORN_CODES` kept / pruned) |
| Outputs | `TH_HORN_CODES`; `TNK_PLATES`; `TNK_EYVIND`; the ridge horn network presentation |
| **Anchor** | Hornbearers and Ridge Wardens; the Signal Terrace. |
| **World-truth row** | H11 (forced resonance horns, now restricted) and H20 (regional restraint): Thornfell decides its own restraint in its own book. |
| **Revelation role** | Self-contained in Thornfell. **Feeds** the convergence alarm network (CV-M2) and R16 custody (CV-M1) through outcome flags only. |
| **Recurring evidence** | The **code book** (record; custodian: the Hornbearers, Dorn). The plates (object; custodian by outcome: Kaldren, the Wardens' store under Assembly seal, or none). |
| **State compliance** | Inactive → Active on `TNK-D1` end; Completed on `TNK-D8` end. No fail path. Outcomes in `TH_HORN_CODES`, `TNK_PLATES`, `TNK_EYVIND`. Resume hook: Dorn at the code-book lectern (`TNK-B1.03`). |

### TNK.4 The places

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. The Signal Terrace** (TP01) | Hub; performance | A broad stone terrace over Stonewake's tiers, open to the ridge. Horn racks along the parapet. The **practice face**: a dressed cliff face across the gully, chalked with echo-count marks. Distant posts visible on clear days: Passwatch's tower, Nettlehook's ropeway head, Three Calls' ledge, Hushfold's smoke, the first watchfire tower (MAP VERIFICATION REQUIRED: sightlines). |
| **B. The code-book lectern** | The book | Under a slate roof. The old book: sinew-stitched, pages loose, a dozen hands. A fresh book beside it, blank, and a pot of ink nobody wants to open first. |
| **C. The terrace workshop** | Retune | A bench with horn vices, bore sleeves of horn and copper in a tray, shims, a rasp, a small forge. Six ordinary horns from the ridge posts hang on pegs, each tagged with its post. Dorn's **reference horn** in a cloth. |
| **D. The Wardens' store** | Plates (surrendered) or shards (broken) | A locked room cut under the terrace, Assembly seal on the hasp. Inside, by `TH_HORN`: three crates of plates (surrendered), or one sack of shards (broken; Wardens swept them from the Summit hall floor). Empty racks for nothing. |
| **E. Eyvind's bench** `[SPLINTER]` | Eyvind | A corner of the workshop where he works under guard, ankle-roped to the bench leg, one Warden on a stool reading. His tools laid out with love. |

**Variant (silenced):** Kaldren is at the terrace with a chalk sketch of the Summit alcoves' stresses; the store is empty.

### TNK.5 Player-facing sequence

**Beat 0 — The book is coming apart (`S00_hook`).** *Objective: Find out what Dorn and Ressa are arguing about.* `TNK-D1`. Three jobs: the plates, the horns, the book.

**Beat 1 — The plates (`S01_plates`).** *Objective: Settle where the plates stay.* By `TH_HORN` (TNK.9 table). **Surrendered:** open the store (Ressa's key), inspect the crates (they still hum faintly when a cart passes above, `TNK-I1.02`), then act: load the crates on Kaldren's sledge for the Summit's null alcoves (3 carries, slow), break them on the terrace anvil-stone (3 × 3 s maul channels, very loud), or re-lock under Assembly seal (2 s channel). **Broken:** the shard sack: mortar the shards into the new step at the terrace's top stair (3 s channel, Smithing-free; masons help), carry the sack (light carry) to the Silent Gorge and empty it at the gateposts (optional travel; the step completes on the deposit), or give one shard to Brynjar's clan as a boast-stone (`TNK-D3.30`). **Silenced:** Kaldren's sketch (inspect) and one decision: seal the alcove mouths with lintels (his crew) or leave them open in his keeping. In every case Eyvind asks; in every case the answer is no.

**Beat 2 — The horns (`S02_retune`).** *Objective: Retune three of the ridge's horns.* At the workshop. Each horn: blow it at the practice face and count the return (`TNK-I2.01`: a doubled return means the sleeve is off). Fit a sleeve at the bench (Smithing interaction, 3 s: *shave*, *seat* or *shim*; the inspect after blowing says which way it's off). Blow again; a single clean return matching the reference horn's completes that horn. Three horns required (Passwatch, Nettlehook, Three Calls); the other three are done by whoever helps. **Who helps:** Eyvind `[SPLINTER]` (fast; he does three horns while the player does theirs; on the last he proposes a deeper bore, "a plate's worth of depth", and Ressa refuses: `TNK-D4.20`) or Dorn's two apprentices (slow: one *watch* interaction, ~30 s). **Crew alternative** for the player's own three: apprentices do them too (a second watch), and the player only blows the test calls.

**Beat 3 — The book (`S03_book`).** *Objective: Go through the code book with Ressa and Dorn.* `TNK-D5`. Page by page, in the old book: the six Ordinary Calls (copied; no choice), the Third Horn (copied with its keeper rule from `TTH_KEEPER`), Witness at the Gate (by `TWG_CALL`: a page, a practice note, or nothing), and **the Split**: a page with a name and the words *"not to be sounded"*, and no shape (Ressa will not let a shape be written, now or ever). Then the decision: **kept** or **pruned**.

**Beat 4 — The ridge answers (`S04_perform`).** *Objective: Sound the kept calls from the terrace.* A guided sequence on the parapet: the player blows each kept call in the book's order; after each, the posts answer one by one across the ridge (TNK.7). The player blows every call; NPCs answer. Pruned: ends with Rest from all posts. Kept: Dorn sounds Witness at the Gate last.

**Beat 5 — The new book (`S05_close`).** *Objective: Sign the new book as witness.* `TNK-D8`. The player's mark goes under Ressa's and Dorn's (origin-neutral: "walker, witness", or the player's name if `TSM_PLAYER_TALLIED` or `TME01_TALLIED`). Quest Completed.

### TNK.6 Encounters

None. TNK is a finale of listening, fitting and deciding. The Wardens' guard on Eyvind is presentation only; Eyvind never tries to escape (he would not leave his tools).

### TNK.7 The wonder moment: the ridge answers

| Time | Element | Spec |
|---|---|---|
| Per call, 0–3 s | **The call** | The player blows the call from the parapet; its glyph shows. |
| 3–5 s | **Passwatch** | Passwatch's tower answers with the call's proper reply (Answer for Lost; the same call back for Rest, Close, Gather, Fall), faint, about 2 s late per sightline distance. |
| 5–12 s | **The posts** | Nettlehook, Hushfold, Three Calls, the first watchfire tower, in turn, each fainter. With `TTH_KEEPER` = hosts, Three Calls answers Lost with the **Third Horn** (beds kept). Others answer Lost with Answer, except the farthest post, which answers with the Third Horn in every outcome ("someone is still out" because the farthest post cannot see the last one in). |
| After the last call (pruned) | **Rest, counted in** | Dorn blows Rest. The posts answer it one at a time from the farthest inward, each a little louder and nearer, until Passwatch's Rest arrives last and the line is quiet. It sounds like a tally read from the bottom up. Stonewake's terraces go quiet to listen, then resume. (Distinct from *Rope-Raising Day*'s single chord: no two posts sound together here.) |
| After the last call (kept) | **The unanswered call** | Dorn takes his reference horn and blows **Witness at the Gate**. The call goes out. **Nothing answers.** 10 s of wind. A child on a lower terrace asks her mother what it was; the mother doesn't know. With `TWG_CALL` = greeting, Passwatch does **not** answer either: it answers only strangers at its gate. |
| UI | Each answer's glyph appears faintly at the post's direction (accessibility). No music. |
| What it means | The network exists and carries. The unanswered call proves only that nobody alive knows the reply. |

### TNK.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_hook` | Find out what Dorn and Ressa are arguing about. | `TNK-D1` end | Yes |
| `S01_plates` | Settle where the plates stay. | `TNK-D3` choice resolved + its physical act (carries, channels or deposit) | Yes |
| `S02_retune` | Retune three of the ridge's horns. | 3 horns at clean return (player or apprentice watch) + helper choice (`TNK-D4`) | Yes |
| `S03_book` | Go through the code book with Ressa and Dorn. | `TNK-D5` choice resolved | Yes |
| `S04_perform` | Sound the kept calls from the terrace. | All kept calls blown in order (sequence complete) | Yes |
| `S05_close` | Sign the new book as witness. | `TNK-D8` end | Yes (→ Completed) |

`S01` and `S02` may be done in either order.

### TNK.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `TNK_PLATES` | `TNK-D3` | Epilogue/TF-M5 lines (request); *Whose Colours* Brynjar line (request) |
| `TNK_EYVIND` = helped / refused | `TNK-D4` | Assembly epilogue line (request; optional) |
| `TH_HORN_CODES` = kept / pruned | `TNK-D5` | CV-M2, CV-M1 (request) |

**Plate custody (by `TH_HORN`).** In every option the plates go into no horn.

| `TH_HORN` | Option | Immediate | Cost | `TNK_PLATES` |
|---|---|---|---|---|
| silenced | **Seal the alcoves** | Kaldren's crew sets lintels over the null alcoves. Moving the plates would now take a crew and a week. | Kaldren can no longer check them himself without the same crew. "I'll have to trust stone. I usually do." | damped_sealed |
| silenced | **Leave them in Kaldren's keeping** | Open alcoves; Kaldren checks them each moon. | One old dwarf is the only thing between a hornwright and the plates. | damped_open |
| broken | **Mortar the shards into the top step** | Every hornbearer walks over them to reach the racks. Dorn: "The notes we don't play. Underfoot." | Brynjar's clan, who lost the boast, call it an insult (bark). | shards_step |
| broken | **Empty them at the Silent Gorge** | Where nothing carries. The sack is left empty on the bench. | Nobody can ever study them; Kaldren is mildly put out. | shards_gorge |
| broken | **One shard to Brynjar's clan** | A boast-stone on a cord for their longhouse. The rest go into the step. | The boast survives, smaller. Ressa: "A stone is a stone. Until someone wants it to be a horn." | shard_given |
| surrendered | **To the Summit** (Kaldren's null alcoves) | Three crates on Kaldren's sledge. | Custody leaves the Assembly's hand for a dwarf's; some Wardens object (bark). | store_summit |
| surrendered | **Break them on the terrace** | Loud, public, final. Half of Stonewake watches. | Kaldren winces at every blow ("Stresses. In the terrace."). Eyvind weeps. | store_broken |
| surrendered | **Keep them sealed in the store** | Under Assembly seal, Ressa's key. | The plates sit under the place where horns are kept. Ressa sleeps less. | store_kept |

**Eyvind's help** `[SPLINTER]` (ordinary horns only).

| Option | Immediate | Cost |
|---|---|---|
| **Let him tune** (`helped`) | Three horns done beautifully in the time it takes the player to do one. Ressa refuses his deeper bore. | He has touched the ridge's horns; some posts distrust their own horn for a season (bark). He asks once more about the plates. |
| **Refuse** (`refused`) | Apprentices do the three. Slow. | Eyvind is hurt in a way he can't hide. "They'll be flat by spring. You'll hear it." (They are, slightly; bark.) |

**The code** (`TH_HORN_CODES`).

| Option | Immediate | Cost | Convergence |
|---|---|---|---|
| **Kept** — *"Keep every page. Write what we know and what we don't."* | The new book holds the six, the Third Horn, Witness (page or note, by `TWG_CALL`; with `left`, a blank page headed only with its name), and the Split's name page with no shape. | A book that carries the Split's name keeps the temptation alive. Ressa: "Then I'll keep the key to the book too." | Richer network; slower to teach. |
| **Pruned** — *"Keep what means one thing to everyone. Let the stone keep the rest."* | The new book holds the six and the Third Horn. The Split and Witness are struck; they survive only in stone (Horn Seat, tower grooves). | Dorn grieves a book that forgets. "My teacher's teacher wrote some of these." | Smaller, faster network. |

None is wrong.

### TNK.10 Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| **The ridge network** | World change | Posts across Thornfell answer the player's calls from the Signal Terrace any time (ambient answers; no mechanical effect). |
| **Witness mark in the code book** | Standing | Thornfell master commissions treat this as Hornbearer standing (request to the commissions author). |
| Small payment | Currency | Dorn, from the Hornbearers' box. |
| Skill XP | Actions only | Smithing (sleeve fitting). |

### TNK.11 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Wrong sleeve fit | The return stays doubled and the inspect says which way it's off; unlimited fits. |
| Wrong call in the performance | The posts answer what was blown; Dorn: "That's not on the page. Again." Sequence continues from the right call. |
| Plate carries interrupted (surrendered → Summit) | Crates loaded stay loaded; a dropped crate returns to the store. |
| Shards to the gorge, then walks away | The sack stays in the player's carry state until deposited or logout (returns to the store); step stays at `S01`. |
| Walking away | Stays Active. Resume: Dorn at the lectern (`TNK-B1.03`). |
| Fail state | None. |
| Co-op | Each player makes their own custody, help and code choices; props (crates, step, store seal) follow each player's own `TNK_PLATES` (fallback: host's). The performance is per player; a partner hears their own answers if they have the quest, otherwise ordinary ambient answers. |

### TNK.12 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| **Distant post answers** | Audio | Positional one-shots at five far points with distance delays; per player. **Fallback:** one mixed answer track per call. |
| **Echo quality per horn state** | Audio / Systems | Two returns (clean/doubled) per horn by sleeve state. Shared with TWG's clean/smeared returns. |
| **Sleeve fitting** | Systems / Gameplay | Bench interaction with three options and a hidden correct value per horn. **Fallback:** dialogue options. |
| **State-dependent store contents** | Systems | Props by `TH_HORN`. |
| **Code-book pages** | UI / Narrative | A document view that assembles pages from flags (`TTH_KEEPER`, `TWG_CALL`, `TH_HORN_CODES`). **Fallback:** fixed text variants. |
| Tethered NPC (Eyvind) | NPC | Seated workstation NPC; no pathing. |
| Convergence | CV-M2 author | Reads `TH_HORN_CODES`. |

**Mystery ledger.** *What the Split sounded like:* never written, never played, never reproduced (bible §9.4); the Split's page has a name only, in every outcome. *Wrong reading:* the book is hiding a weapon. Nothing is withheld except the shape, which is withheld forever.

**Open decisions.**
1. **TNK and TF-M5 sequencing.** TF-M5 starts automatically when the player enters Stonewake or Windscar after TF-M4 (bible §6.1). TNK's terrace is in Stonewake, so for most players TNK is played after TF-M5. This package holds the offer while TF-M5 is Active (a sequencing hold, not a new prerequisite). **[PROPOSAL — DIRECTOR]** Alternative: allow TNK before TF-M5 by moving its hook to the Passwatch horn post; not recommended (TF-M5 also triggers there).
2. **Eyvind's custody (resolved, independent review).** Act II §open 6: held by the Ridge Wardens pending the Assembly. TNK follows it; the clan tribunal stays Ingrith's alone (TF-M5).
3. **Post-TF-M5 variants.** `TNK-D5.02` reads `TH_ASSEMBLY_POSTURE`; if TF-M5 is not Completed the line is skipped.

| Review finding | Revision |
|---|---|
| A first draft let Eyvind use one plate as a "tuning reference". | Cut. Plates never touch a horn, a bench or a sleeve. |
| Ressa's argument risked being about tradition. | It is about accountable warning: a call must mean one thing to blower and hearer; the Split's shape is never written. |
| The performance risked a rhythm minigame with failure. | Guided sequence, wrong calls just get answered. |
| `left` + `kept` had no page. | A blank page headed with the name only. |

### TNK.13 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Dorn Feldhorn** | The book; every hand in it. | What the Split sounded like (and is glad). | Wants things written. Grief for pages. |
| **Ressa Highcrag** | Which tones caused "wrong results". | The roster's details. | "A call has to mean the same thing to both ends." Refuses new weapons flatly. |
| **Eyvind Stall** `[SPLINTER]` | Plates, bores, pitch. That the Summit hummed when he tested. | What the hum was; why anyone is upset with him beyond the law. | Courteous, rapt, careless. Talks to horns. |
| **Kaldren Deepdelver** (silenced, surrendered→Summit) | Stresses, alignments. | Origins (never explains). | Dry, brief, protective of stone. |
| **Warden guard** (role) | Her book. | — | Bored. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| TNK-B1.01 | Dorn | Available, TF-M5 Active | *"After the gate. Horns are busy."* |
| TNK-B1.03 | Dorn | Active, returns | *"Plates, horns, book. In any order. Not all at once."* |
| TNK-B2.01 | Eyvind `[SPLINTER]` | Player in workshop | *"That Nettlehook horn's a quarter flat and it knows it."* |
| TNK-B2.02 [SPLINTER] | Warden guard | Player near Eyvind | *"He talks to them. Don't answer for them."* |
| TNK-B3.01 | Blood-Oath clansman | `shards_step` | *"Walking on our boast. Every day. Lovely."* |
| TNK-B3.02 | Post warden | `helped` | *"Splinter tuned our horn. Sounds lovely. I don't trust it."* |
| TNK-B3.03 | Post warden | `refused`, later | *"Horn's gone flat. Dorn says it's the cold. It's not the cold."* |

#### Nodes

```
TNK-D1.01 DORN: (holding the old book shut with both hands) "It's coming apart. Like everything this winter."
TNK-D1.02 RESSA: "So we copy it. That's not the argument."
TNK-D1.03 DORN: "The argument is what goes in."
TNK-D1.04 [TF-M5 Completed] RESSA: "The Assembly wants every closing written with the calls that ordered it. So the calls have to mean one thing."
TNK-D1.05 DORN: "And the plates are still sitting where they're sitting. And the horns are split. And he's in my workshop."
  > "Who's in your workshop?"                              → TNK-D1.10
  > "Where do I start?"                                     → TNK-D1.20
TNK-D1.10 RESSA: "Eyvind. The hornwright. Roped to a bench till the Assembly sits on him. He's offered to tune the ridge." [SPLINTER]
TNK-D1.11 RESSA: "He wants his plates back for it. He's not getting them."   → TNK-D1.20
TNK-D1.20 DORN: "Plates first, if you want sleep tonight. Horns if you want warm hands. Book last. Book's always last."
      {event: S00_hook}
```

```
TNK-D3.01 [TH_HORN = surrendered] RESSA: (unlocking the store) "Assembly seal. My key. Three crates. They hum when a cart goes over."
TNK-D3.02 RESSA: "Kaldren will take them to the Summit. Or we break them here. Or they stay where they are, under my feet."
  > "To the Summit. Kaldren's alcoves."                     → TNK-D3.10 {set TNK_PLATES = store_summit; carries}
  > "Break them. Here. Where people can see."              → TNK-D3.11 {set TNK_PLATES = store_broken; maul channels}
  > "Keep them sealed. Under the Assembly's hand."          → TNK-D3.12 {set TNK_PLATES = store_kept; seal channel}
TNK-D3.10 KALDREN: "I'll take them up. Don't help me lift. Help me not drop them."
TNK-D3.11 RESSA: "Then everyone will hear it. Good." (Kaldren, from the steps: "Stresses. In my terrace.")
TNK-D3.12 RESSA: "Then I'll sleep less. That's a cost I can count."
TNK-D3.20 [TH_HORN = broken] DORN: (lifts a sack; it clinks) "Wardens swept the hall floor. This is the horn that split the ridge, now."
  > "Mortar them into the top step."                        → TNK-D3.21 {set TNK_PLATES = shards_step}
  > "Take them to the Silent Gorge."                        → TNK-D3.22 {set TNK_PLATES = shards_gorge; sack becomes light carry}
  > "Give one to Brynjar's clan. The rest in the step."    → TNK-D3.30 {set TNK_PLATES = shard_given}
TNK-D3.21 DORN: "The notes we don't play. Underfoot. I like that."
TNK-D3.22 DORN: "Where nothing carries." (beat) "Bring the sack back. It's a good sack."
TNK-D3.30 RESSA: "A stone is a stone. Until someone wants it to be a horn." (beat) "One. On a cord. Not in a horn."
TNK-D3.40 [TH_HORN = silenced] KALDREN: (unrolls a chalk sketch) "Alcoves are settled. Stresses down. That's all I can tell you."
TNK-D3.41 KALDREN: "I can lintel them shut. Then nobody moves them without a crew and a week. Including me."
  > "Seal them."                                            → TNK-D3.42 {set TNK_PLATES = damped_sealed}
  > "Keep them open. In your keeping."                      → TNK-D3.43 {set TNK_PLATES = damped_open}
TNK-D3.42 KALDREN: "I'll have to trust stone. I usually do."
TNK-D3.43 KALDREN: "Then I'll go up each moon and look at them. Somebody has to be dull about it."
TNK-D3.50 (any, after) EYVIND: (from the workshop door, roped) "Whatever you've done with them, they were beautiful. You should know that." [SPLINTER]
      {event: S01_plates on physical act complete}
```

```
TNK-D4.01 EYVIND: (not looking up from a horn) "Six horns. Six sleeves split in the cold. I can do the lot by dark." [SPLINTER]
TNK-D4.02 EYVIND: "Ordinary horns. I know. Ressa's said it in four tones of voice." [SPLINTER]
  > "Do the other three. I'll do these."                    → TNK-D4.10
  > "No. The apprentices will do it."                       → TNK-D4.30
TNK-D4.10 EYVIND: "You'll want to shave the Passwatch one. Not much. It's proud." [SPLINTER]   {set TNK_EYVIND = helped; Eyvind tunes three}
TNK-D4.20 EYVIND: (holding up the last horn) "This one would carry twice as far with a plate's worth of depth in the bore—" [SPLINTER]
TNK-D4.21 RESSA: "No."
TNK-D4.22 EYVIND: "It's only depth." [SPLINTER]
TNK-D4.23 RESSA: "A call that knocks a man down isn't a warning. It's the thing we're warning about." (beat) "Ordinary bore."
TNK-D4.24 EYVIND: (to the horn) "Ordinary bore." [SPLINTER]   → end
TNK-D4.30 EYVIND: "They'll be flat by spring. You'll hear it." (quieter) "I'd have done them well." [SPLINTER]   {set TNK_EYVIND = refused}  → end
```

```
TNK-D5.01 DORN: (old book open, new book open) "Rest. Close. Gather. Fall. Lost. Answer." (copies each) "No argument there."
TNK-D5.02 [TF-M5 Completed] RESSA: "Every closing writes these now. Who closed, what was blown, who's outside."
TNK-D5.03 DORN: "Third Horn." (copies, then reads the keeper rule aloud by TTH_KEEPER: board / Warden code / hosts)
TNK-D5.04 [TWG_CALL = recorded] DORN: "Witness at the Gate. 'Meaning not known.' My hand."
TNK-D5.04 [TWG_CALL = greeting] DORN: "Witness at the Gate. 'Blown at Passwatch for strangers. Means hello.'"
TNK-D5.04 [TWG_CALL = left] DORN: "Witness at the Gate." (beat) "There's nothing else to write. Just the name."
TNK-D5.05 DORN: (turns to a page near the back; it has a name and a line, and nothing else) "And this."
TNK-D5.06 RESSA: "The Split. 'Not to be sounded.' No shape. There's never been a shape on that page and there never will be."
TNK-D5.07 DORN: "If we write the name, they'll know why we don't."
TNK-D5.08 RESSA: "If we write the name, someone will go looking for the rest."
TNK-D5.09 RESSA: (to the player) "You've walked the stones and the towers. What does Thornfell keep?"
  > "Keep every page. Write what we know and what we don't."                     → TNK-D5.10
  > "Keep what means one thing to everyone. Let the stone keep the rest."         → TNK-D5.20
TNK-D5.10 DORN: (relieved, copying) "Every page."
TNK-D5.11 RESSA: "Then I keep the key to the book too. That's fair."   {set TH_HORN_CODES = kept}  → TNK-D6.01
TNK-D5.20 DORN: (long pause) "My teacher's teacher wrote some of these." (he strikes the Split's page, then Witness, with one line each) "There."
TNK-D5.21 RESSA: "Seven calls. A child can hold seven."   {set TH_HORN_CODES = pruned}  → TNK-D6.01
```

```
TNK-D6.01 DORN: "Now blow them. In the order of the book. The ridge will tell us if it's listening."
      {S04_perform sequence}
TNK-D7.01 [kept, after Dorn's Witness call and silence] DORN: (lowering the horn) "Nobody knows the reply."
TNK-D7.02 RESSA: "Then nobody does. Write that too."
TNK-D7.01 [pruned, after all-posts Rest] RESSA: "That's the ridge. Seven calls and everyone heard."
```

```
TNK-D8.01 DORN: (sands the ink) "Witnesses sign. That's the old form."
TNK-D8.02 RESSA: (signs) "R. Highcrag." DORN: (signs) "D. Feldhorn."
TNK-D8.03 [TSM_PLAYER_TALLIED or TME01_TALLIED] DORN: "Your name. You're on a tally. You've got one to write." 
TNK-D8.03 [else] DORN: "'Walker, witness.' That'll do. It's done before."
TNK-D8.04 RESSA: "If the passes ever have to carry further than Thornfell, this is what they'll carry."
TNK-D8.05 DORN: (closes the new book; the old one he keeps, loose pages and all) "I'm not throwing this out. Don't ask me to."
      {event: S05_close → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| TNK-I1.01 | Old code book | *"A dozen hands. Sinew stitching gone at the spine. Some pages are only a glyph and a word."* |
| TNK-I1.02 | Plate crates (surrendered) | *"Packed in straw. When a cart goes over the terrace, the straw shivers."* |
| TNK-I1.03 | Shard sack (broken) | *"Stone and horn in pieces. Each shard rings a different note if you flick it. Don't."* |
| TNK-I1.04 | Kaldren's sketch (silenced) | *"Chalk lines for stresses, arrows for loads. Every arrow points down and stops."* |
| TNK-I2.01 | Practice face, doubled return | *"The echo comes back twice, a hair apart. The sleeve is off. Sharp: shave. Flat: shim. Loose: seat it."* |
| TNK-I2.02 | Reference horn | *"Dorn's own. Dented in three places, each with a story he won't tell."* |
| TNK-I2.03 | The Split page | *"A name. 'Not to be sounded.' No shape. The paper is clean where a shape would go."* |

---

# Series two — Clans of the High Steads

---

## TNR — Nettlehook Rope

### TNR.1 The quest in one paragraph

Tova Rask, eleven, has a slate of half-finished letters and has not been to lessons since the leaves turned. Nettlehook's ropeway is the only winter way down to the lower longhouse where Leiv keeps lessons, and the ropeway rota runs by **lineage**: founding households ride first, and the keeper's household, the newest on the shelf, rides last. In short autumn light the last runs are cancelled, so Tova walks the brake with her father instead. This week nobody rides at all: the upper **sheave** is fouled with ice and a crows' nest, and its pin has sheared. Ketil Rask, who worries about everything except himself, cannot climb the sheave tower with a bad knee and will not say so. The player climbs it under a mob of Ridge Crows, clears the housing, forges a new pin at Ketil's field forge (or has a neighbour do it), seats it in three hard pulls, and test-rides the car down through a wind window. Stopped mid-span in a gust, the cable sings a rising note, and from the shelf below Tova hums it back exactly: she has been learning by ear what she could not learn at the longhouse. Then the rota board. Osk Varrow, the rota elder, keeps it the way his grandfather pegged it. The player redraws it with Ketil, Osk and Tova watching: children first, lots, or the old order with the keeper's household moved onto the morning brake crew.

**Remember:** a child humming a cable's note back to it. **Want next:** Smoke Week, when Nettlehook's ropeway carries Hushfold's tally down the shelf.

### TNR.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| **A. Talk Osk into changing the rota.** | Rejected. Talk-led. The player earns the right to touch the board by fixing what it schedules. |
| **B. Repair only; the rota changes off-screen.** | Rejected. The brief's point is the rota. |
| **C. Climb and repair under crows → forge → seat → test ride with the strange moment → the board as a puzzle with a principle** (selected). | **Selected.** Traversal, skilling, light combat and a civic decision with a physical board. |

| Element | Source | Status |
|---|---|---|
| Nettlehook: mixed-clan repair base; ropeway decides who reaches school, stores and Assembly in winter; a child's missed lessons expose a lineage rota | Part 3 proposal; bible TP03 | [NEW, Part 3] |
| Ketil Rask (keeper), Tova Rask (about eleven) | Bible §5.2 | [NEW] |
| Ridge Crows (flock, diver) | Bible §10 | [NEW on dossier fauna] |
| Wind windows: whistle a fifth before the gust | Bible §1.1, §9.5 | [NEW] |
| The sheave tower, the pin, Osk Varrow, Leiv, the peg rota board, the brake crew | This package | [NEW] |

### TNR.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `thornfell.side.nettlehook_rope` |
| Series | *Clans of the High Steads*, part 1 of 3 |
| Type | Skill-adjacent settlement |
| Unlock | TF-M1 Completed. Offered by Tova at the upper ropeway station (`TNR-D1`) or Ketil (`TNR-B1.01` bark leads to Tova). |
| Length | 30–40 minutes |
| Combat share | ~15% |
| Skills | Smithing (pin; crew alternative), agility (optional) |
| Choice | The new rota (`TNR_ROTA`: children_first / lots / lineage_swap) |
| Outputs | `TNR_ROTA`; ropeway running (fast route upper station ↔ lower longhouse) |
| **Anchor** | Nettlehook Highstead; Bridgewright-style ropeway crews; highstead households. |
| **World-truth row** | H23 (thirty years of uneven recovery: who gets the repaired thing first). Present-day only otherwise. |
| **Revelation role** | Self-contained. |
| **Recurring evidence** | The **rota board** (Nettlehook; custodian Osk Varrow) recurs in TSM and TRR barks. |
| **State compliance** | Inactive → Active on `TNR-D1` end; Completed on `TNR-D6` end. No fail path; choice in `TNR_ROTA`. Resume hook: Ketil at the upper station (`TNR-B1.03`). |

### TNR.4 The places

**MAP VERIFICATION REQUIRED:** upper station on Nettlehook's shelf; the lower longhouse on the shelf below; the span crosses a ravine (bible TP03).

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **A. Upper station** | Hook; rota board | Brake wheel, a car (wicker-and-board, room for four or a load), Ketil's field forge under a lean-to. The **rota board**: eight household pegs on a lineage ladder, oldest at top. "RASK" at the bottom, its peg newer wood. Tova's slate on the bench: *TOVA* written well, the rest of the alphabet stops at *G*. | — |
| **B. Sheave tower** | Repair; TNR-E1 | A timber tower above the station carrying the upper sheave. Ice beards. The sheave housing is packed with sticks: a crows' nest. The pin's sheared head lies on the platform. | **Agility:** climb the outer lattice. **Fallback:** inner ladder, rungs iced; chip three rungs (2 s each). |
| **C. The span** | Test ride; strange moment | The cable runs over the ravine. Fluted rock on the far wall whistles before gusts. A chalked board at the brake: *GUST — STOP — WAIT.* | Ride (car). |
| **D. Lower longhouse** | Lessons | Leiv's benches, a slate wall with letters to *Z*. Eleven slates on pegs; one peg empty. | — |

### TNR.5 Player-facing sequence

**Beat 0 — Letters to G (`S00_hook`).** *Objective: Ask Tova why nobody's riding.* `TNR-D1`. Tova explains the rota in a child's flat way, and the sheave. Ketil interrupts, says it's nothing, limps.

**Beat 1 — Up the tower (`S01_climb`).** *Objective: Climb the sheave tower.* Lattice or ladder. **TNR-E1** at the top.

**Beat 2 — Clear the sheave (`S02_clear`).** *Objective: Clear the sheave housing.* Two channels: pull the nest (3 s), chip the ice (3 s). Recover the sheared pin (inspect: `TNR-I1.03`).

**Beat 3 — A new pin (`S03_pin`).** *Objective: Make a new sheave pin.* At Ketil's forge: Smithing interaction (heat, draw, quench; the TF-M1 field-anvil interaction). **Crew alternative:** Osk's grandson forges it (watch interaction, ~30 s; Osk notes who did it, `TNR-B2.02`).

**Beat 4 — Seat it (`S04_seat`).** *Objective: Seat the pin in the sheave.* Carry the pin up (light carry). Three channelled pulls on the seating bar (3 × 4 s; segments persist). Ketil calls the timing from below with Gather (pull) and Rest (hold).

**Beat 5 — Test ride (`S05_ride`).** *Objective: Ride the car down to the lower longhouse.* Tova rides too ("someone has to watch the cable"). Mid-span the fluted rock whistles: the player pulls the stop-cord (Ketil brakes). If the player doesn't pull it, Ketil brakes anyway (the car sways; nothing else). **The strange moment** (TNR.7). The car runs on after the gust.

**Beat 6 — The longhouse (`S06_longhouse`).** *Objective: Take Tova to lessons.* `TNR-D3` (Leiv). Tova's slate goes on the empty peg.

**Beat 7 — The board (`S07_rota`).** *Objective: Redraw the ropeway rota.* Back at the upper station (ride up). `TNR-D4`: Osk, Ketil, Tova. The player picks a principle, then pegs the board (TNR.9). Any board that meets the constraints is accepted.

**Beat 8 — Done (`S08_close`).** *Objective: Tell Ketil the board's done.* `TNR-D6`. Quest Completed.

### TNR.6 Encounters

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TNR-E1** | 1 × Ridge Crow flock, 2 × Ridge Crow diver | Sheave platform (about 3 × 4 m, railed) | Flock: Aggressive, swirls over the platform. Divers: harassers from the tower top. Leashed to the tower. | **Diver:** folds its wings with a sharp double caw (~0.8 s), then a straight dive; step aside. **Flock:** the swirl darkens and tightens over one spot (~1.2 s), then pecks in a 2 m circle; leave the circle. The rail stops all knockback; nobody falls. | Fight at height that is about footing, not damage. | 35–50 s; player at 70–90% HP. Ranged welcome. |

**Rules.** Each crow fights until defeated at 0 HP (CDR-1; rulings §3.1.4 flock rule). After the quest, crows return to the tower as ambient scenery, without a nest. Tova and Ketil stay on the ground and are never targets.

### TNR.7 The strange moment: the cable's note

| Time | Element | Spec |
|---|---|---|
| 0 s | **The tell** | Fluted rock whistles a fifth up (the standard gust tell). Stop-cord prompt. |
| 0–2 s | **Stop** | The car stops mid-span with a soft jolt. |
| 2–6 s | **The cable sings** | The cable above hums, a low steady note that **rises** as the gust arrives, a long slow climb. |
| 4–8 s | **Tova** | Beside the player, Tova hums it back: the same note, the same climb, a breath behind, exactly in tune. She doesn't look up from her mittens. |
| 8–12 s | **The gust** | The gust passes; the car sways; the cable's note falls; Tova's falls with it and stops when it stops. |
| After | `TNR-D2` | *"It does that before every gust. I learned it. Nobody asked me to."* |
| What it means | Nothing strange about a cable singing in wind. What is strange is a child who learned a weather instrument by ear because she was kept out of a room with letters in it. No phenomenon; the wonder is hers. |

### TNR.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_hook` | Ask Tova why nobody's riding. | `TNR-D1` end | Yes |
| `S01_climb` | Climb the sheave tower. | Enter platform volume + TNR-E1 defeated | Yes |
| `S02_clear` | Clear the sheave housing. | `pull_nest` + `chip_ice` channels; sheared-pin inspect | Yes |
| `S03_pin` | Make a new sheave pin. | Smithing interaction complete **or** watch (crew) | Yes |
| `S04_seat` | Seat the pin in the sheave. | 3 × `seat_pin` segments (persist) | Yes |
| `S05_ride` | Ride the car down to the lower longhouse. | Ride complete (strange moment plays) + `TNR-D2` | Yes |
| `S06_longhouse` | Take Tova to lessons. | `TNR-D3` end | Yes |
| `S07_rota` | Redraw the ropeway rota. | `TNR-D4` principle chosen + valid board pegged | Yes |
| `S08_close` | Tell Ketil the board's done. | `TNR-D6` end | Yes (→ Completed) |

### TNR.9 Flags, the board, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `TNR_PIN_FORGED` = self / crew | `S03` | `TNR-D6` line; Osk bark |
| `TNR_ROTA` = children_first / lots / lineage_swap | `TNR-D4` | TSM opener, TRR knot judge line, TF-M5 Ketil line (request) |

**The board.** Six daylight runs in snow (eight in autumn; `TH_SEASON`). Every run needs a brake pair (two adults, never the riders). One run before mid-morning must carry the children if lessons are to happen. Loads (grain, wood) take a full run each; with `TH_PASSWATCH_ROUTE` = sledge there are two grain loads this week (Nettlehook's winter grain came over the Narrows), with = caravan none (bark: *"Nothing to carry and nothing to eat"*), with = split one. The player pegs households and loads into runs. Any board meeting the constraints is valid; the chosen principle colours the result.

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Children first** — *"School run first, every day, whoever's children they are."* | The first run of every day carries the children; lineage order follows. | Founding households' loads go later in colder light; Osk is offended and says so to everyone. | TSM: Hushfold's children ride with Nettlehook's when the tally goes down the shelf. TRR: Osk judges knots stiffly. |
| **Lots** — *"Draw lots each week. Your grandfather's grandfather drew lots."* | Osk admits lots are older than lineage. A bag of marked pegs hangs on the board. | Fair and unpredictable: some weeks Tova still misses lessons. Ketil worries about it aloud. | TRR: the knot judges are drawn by lot too (Osk's idea). |
| **Old order, keeper on the morning brake** — *"Keep the order. Put the Rasks on the first brake crew, and Tova rides with them."* | The lineage ladder stands. Ketil's household takes the first brake shift every day; Tova rides down with them. | Ketil works the brake every morning on a bad knee. Only Tova's problem is solved. | TRR: Osk is gracious. Ketil limps through the festival. |

### TNR.10 Rewards, failure, co-op

| Reward | Type | Notes |
|---|---|---|
| **The ropeway** | Access | Fast route upper station ↔ lower longhouse (ride interaction; gust stops are ambient). |
| Small payment / a meal | Currency / gift | Ketil insists. Economy tuning. |
| Skill XP | Actions only | Smithing, Melee or Ranged. |
| *A Place at Smoke Week* | Story | Unlocks after TF-M2. |

| Situation | Handling |
|---|---|
| Falls from the lattice | The agility trigger fails safe to the platform below; the ladder is always there. |
| Death on the tower | Respawn at the upper station; nest and ice progress persist; E1 resets if not defeated. |
| No Smithing | Crew alternative. |
| Board won't validate | The board highlights the run that breaks a constraint (no brake pair, no morning child run, load overlap). No limit on tries. |
| Walking away | Stays Active; resume with Ketil (`TNR-B1.03`). |
| Fail state | None. |
| Co-op | Shared crows; each player seats their own pin segments (fallback: shared progress). Each player pegs their own board and choice; Nettlehook's board prop follows each player's own `TNR_ROTA` (fallback: host's). |

### TNR.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| **Ropeway car ride** | Systems | Moving platform on a spline with a stop point (stop-cord interaction) and a gust event. **Fallback:** a fade-free scripted ride with fixed stop. |
| **Rota peg board** | UI / Systems | Grid of runs × slots; constraint checker (brake pair, morning child run, loads). **Fallback:** three preset boards chosen by dialogue. |
| Cable note + Tova hum | Audio / NPC | Two synced audio tracks; Tova seated in car. |
| Channel segments with persistence | Systems | Lowmark convention. |
| Creatures | Encounters package | Ridge Crow flock, diver. |

**Mystery ledger.** *Why the Rasks ride last:* the lineage ladder dates from when the founding households rebuilt the ropeway after the war; Ketil's household came later and "hasn't been here long enough" at thirty years. Self-contained; no withheld layer.
**Open decisions.** Exact daylight-run counts are the Gameplay Designer's. MAP VERIFICATION REQUIRED for the span.

| Review finding | Revision |
|---|---|
| Osk first read as a villain. | He keeps the board because the board kept Nettlehook fed once; option "lots" lets him be right about something older. |
| The cable note risked being a phenomenon. | It is physics. The wonder is Tova. |
| Children near combat. | Tova stays on the ground for E1 and rides only after the crows are gone. |

### TNR.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Tova Rask** | The rota, the cable's moods, every brake signal. | Letters after G. | Asks the question adults avoid. Flat, exact, eleven. |
| **Ketil Rask** | The ropeway; his knee. | How to ask for help. | Worries about everything except himself. |
| **Osk Varrow** [NEW] | The board's history. | That lots are older (he half knows). | Formal, proud, not unkind. |
| **Leiv** [NEW] | Every child's slate. | — | Brisk, glad. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| TNR-B1.01 | Ketil | Available | *"Car's down. It's fine. Nothing's fine. It's fine."* |
| TNR-B1.03 | Ketil | Active, returns | *"Tower's still there. So's the pin. Well. Half the pin."* |
| TNR-B2.02 | Osk | `TNR_PIN_FORGED` = crew | *"My grandson made the pin. I've written it on the board's back. Small."* |
| TNR-B3.01 | Tova | Completed, `children_first` | *"I'm on H. H is a ladder with a rung missing."* |
| TNR-B3.02 | Tova | Completed, `lots` | *"Drew a bad peg this week. I'm learning the cable instead. Again."* |
| TNR-B3.03 | Tova | Completed, `lineage_swap` | *"Da does the brake every morning. He says his knee likes it. His knee doesn't."* |

#### Nodes

```
TNR-D1.01 TOVA: (writing in the frost on the car's side) "It's broken. You can't ride."
TNR-D1.02 TOVA: "The wheel at the top's got a nest in. And ice. And the pin snapped. Da says it's nothing."
  > "Why aren't you at lessons?"                           → TNR-D1.10
  > "I could look at the wheel."                            → TNR-D1.20
TNR-D1.10 TOVA: "Rota. Old houses ride first. We ride last. Last runs get cancelled when it's dark early."
TNR-D1.11 TOVA: "It's dark early since the leaves. So I walk the brake with Da." (beat) "I'm on G."
TNR-D1.12 TOVA: "Is that fair? Nobody says."   → TNR-D1 options
TNR-D1.20 KETIL: (limping over) "No, no. I'll do it. Tomorrow. When the knee's— I'll do it."
TNR-D1.21 TOVA: "He can't climb."
TNR-D1.22 KETIL: "I can climb. I can't come down." (beat) "If you'd go up. Mind the crows. They think they own it now."
      {event: S00_hook}
```

```
TNR-D2.01 TOVA: (after the gust) "It does that before every gust. Goes up. Then down."
TNR-D2.02 TOVA: "I learned it. Nobody asked me to."
  > "You hummed it exactly."                               → TNR-D2.10
  > "Does your father know?"                               → TNR-D2.20
TNR-D2.10 TOVA: "It's easier than letters. It's only one letter. Long."   → end
TNR-D2.20 TOVA: "He brakes when I hum. Says I'm faster than the whistle." (beat) "I am."   → end
      {event: S05_ride}
```

```
TNR-D3.01 LEIV: (sees Tova) "Tova Rask. With a slate." (to the player) "You fixed the wheel."
TNR-D3.02 LEIV: "Eleven slates. Ten on pegs since autumn. Go on, then."
      {Tova hangs her slate on the empty peg}
TNR-D3.03 LEIV: "The wheel's half of it. The board's the other half. You'll find Osk at the top, defending it."
      {event: S06_longhouse}
```

```
TNR-D4.01 OSK: (hand on the board) "This board fed Nettlehook through the first winters. It's not a toy."
TNR-D4.02 KETIL: "Nobody said toy, Osk."
TNR-D4.03 TOVA: "Why are we at the bottom?"
TNR-D4.04 OSK: (after a while) "Because you came last."
TNR-D4.05 TOVA: "Thirty years ago."
TNR-D4.06 OSK: (to the player) "You mended the wheel. That buys you a say. Not the board."
  > "School run first, every day, whoever's children they are."                         → TNR-D4.10
  > "Draw lots each week. Your grandfather's grandfather drew lots."                       → TNR-D4.20
  > "Keep the order. Put the Rasks on the first brake crew, and Tova rides with them."      → TNR-D4.30
TNR-D4.10 OSK: "Then the founding loads go down in the cold." (beat) "Children don't eat letters." 
TNR-D4.11 KETIL: "They don't eat grain without them either, by the time they're running the stores."   {set TNR_ROTA = children_first; board opens}
TNR-D4.20 OSK: (stiff) "Lots." (long pause) "...He did. Before the war. I'd forgotten I knew that."   {set TNR_ROTA = lots; board opens}
TNR-D4.30 KETIL: "Every morning. On the brake." (the knee) "Fine. Fine. She rides."
TNR-D4.31 OSK: "The order stands. Good." (to Ketil, quieter) "Your knee, Rask."
TNR-D4.32 KETIL: "My knee's my business."   {set TNR_ROTA = lineage_swap; board opens}
      {board valid → TNR-D5}
TNR-D5.01 OSK: (reads the pegs) "It works." (as if that were an insult) "It works."
```

```
TNR-D6.01 KETIL: "Wheel turns. Board's pegged. Tova's on H by Smoke Week, she says."
TNR-D6.02 [TNR_PIN_FORGED = self] KETIL: "And that pin's better than mine. Don't tell anyone."
TNR-D6.03 [TH_PASSWATCH_ROUTE = sledge] KETIL: "And the grain you brought over the Narrows goes down on the second run. Didn't forget."
TNR-D6.04 KETIL: "Hushfold sends their tally down our rope at first smoke. You'll want to be about for that."
      {event: S08_close → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| TNR-I1.01 | Rota board | *"Eight pegs on a ladder, oldest houses at the top. RASK at the bottom, in newer wood."* |
| TNR-I1.02 | Tova's slate | *"TOVA, neat. Then A to G. Then nothing."* |
| TNR-I1.03 | Sheared pin | *"Sheared clean through the shoulder. Old iron, older than the tower timber round it."* |
| TNR-I1.04 | Brake board | *"GUST — STOP — WAIT. Underneath, in a child's hand: HUM."* |

---

## TSM — A Place at Smoke Week

### TSM.1 The quest in one paragraph

At first heavy snow every highstead reads its **winter tally** aloud: beds, food, who is expected, who is still out. Hushfold's tally decides each shelter household's claim on Nettlehook's shared granary, and it is kept by work: Grima Loft counts every haul. This year it leaves out the **Kvist household**. In autumn Ama Kvist and her son Pell took in a sick traveller with a fever nobody could name, nursed him for three weeks, and were kept back from shared work for fear of it. He got well and walked on. The Kvists are two wood hauls and a meat share short, and the count says short is short. Runa Weatherall reads the tally on the last night of Smoke Week and hates this year's page. The player does what the count says the Kvists owe: two sledge hauls of cut wood along the shelf path from the near woodstacks, in wind windows, and a cliff goat from the shoulder above Nettlehook, carried home with a winter-thin pack following. Then the first smoke: at Runa's word every chimney on the shelter line is lit at once, the smokes rise straight in the still cold, and at one height they all lean together toward the far shielings. At the reading the player says what the work means: work done for a household counts for it; need itself makes a claim; or leave the tally and see they eat. Runa then asks the question every host asks: *"And you? Expected or not?"*

**Remember:** the smokes leaning together. **Want next:** to see Hushfold stand in the Assembly with one voice (TF-M5); Rope-Raising Day.

### TSM.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| **A. A hearing where the player argues the Kvists' case.** | Rejected. Talk-led; Thornfell is talkative only in the Assembly (bible §1). |
| **B. The player donates goods to buy the Kvists' place.** | Rejected. Makes belonging a purchase with no civic stakes. |
| **C. Do the owed work → first smoke → the reading → three principles with costs → the player's own tally question** (selected). | **Selected.** The player's hands earn the right to an opinion; the decision is the shelter line's, voiced through Runa. |

| Element | Source | Status |
|---|---|---|
| Shelter tally read at first snow; beds, food, expected, unaccounted | Part 3 proposed customs; bible TME01 | [NEW, Part 3] |
| *A Place at Smoke Week*: a family excluded after sheltering a sick traveller; need and shared work as a claim | Part 3 side-quest list; bible §7.1 | [NEW, Part 3] |
| Hushfold: clanless wartime shelter line; route labour; no agreed Assembly voice | Part 3; bible §2.2, TP04 | [NEW] |
| Runa Weatherall: warm, tired, proud; says "we" | Bible §5.2 | [NEW] |
| A host who adds the player uses their name thereafter | Bible §5.3 rule 4 | [NEW] |
| Ridge Wolves; cliff goats as Hunting fauna | Bible §10 | [NEW on dossier] |
| The Kvists, Grima Loft, the near woodstacks, the work count, the leaning smokes | This package | [NEW] |

### TSM.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `thornfell.side.a_place_at_smoke_week` |
| Series | *Clans of the High Steads*, part 2 of 3 |
| Type | Settlement (Hushfold) |
| Unlock | TNR Completed **and** TF-M2 Completed (`TH_SEASON` = snow). Offered by Runa at Hushfold (`TSM-D1`), or by Pell at Nettlehook's granary door (`TSM-B1.01`). |
| Length | 35–45 minutes |
| Combat share | ~20% |
| Skills | Hunting (crew alternative: Pell's snares); Woodcutting (optional; stacks are pre-cut) |
| Choices | The claim (`TSM_CLAIM`: counted / shared / private); the player's place (`TSM_PLAYER_TALLIED`) |
| Outputs | `TH_HUSHFOLD_VOICE`; `TSM_CLAIM`; `TSM_PLAYER_TALLIED` |
| **Anchor** | Hushfold's clanless households; Nettlehook's shared granary. |
| **World-truth row** | H16 (Hushfold began as a wartime shelter line) as background only; H23 (uneven recovery). Present-day pressure: winter stores. |
| **Revelation role** | **Supports R06 (sealing half)** only as setting: Hushfold's clanlessness is a listed seed (bible §8.1). Nothing about the roster is said. |
| **Recurring evidence** | **Hushfold's tally book** (record; custodian: Runa as host). Its *current* page is read here; its *first* book is TF-M5's second custodian. This quest never opens the first book. |
| **State compliance** | Inactive → Active on `TSM-D1` end; Completed on `TSM-D7` end. No fail path; outcomes in `TSM_CLAIM`, `TH_HUSHFOLD_VOICE`, `TSM_PLAYER_TALLIED`. Resume hook: Runa at the tally hearth (`TSM-B1.03`). |

### TSM.4 The places

**MAP VERIFICATION REQUIRED:** Hushfold sits on the Ridgewall above the pass road; its far shielings lie beyond the Gatefall (bible §4.2) and are **not** visited here. The near woodstacks are on a shelf path above Hushfold.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Hushfold tally hearth** | Hook; reading | The shelter line's common hearth: a long room, benches, the tally book on a stand. Chalk on the lintel: household marks, one per door, no clan signs. The current page lists households with strokes for hauls. |
| **B. The Kvist house** | The family | End of the line. A cot by the fire, still made up, a fever-cloth folded on it. A carved spoon on the shelf that isn't Hushfold work (the traveller's thanks; no origin stated). Two split-wood strokes on the doorframe where the tally gives others five. |
| **C. Grima's count** | The rule | A board by the woodshed with every household's hauls. Kvist: two short. Grima's chair beside it. |
| **D. The shelf path and near woodstacks** | Hauling | A path along a shelf above Hushfold to stacks of cut crag-pine. Fluted rock whistles before gusts. Chalked shelter faces every 60 m. |
| **E. The goat shoulder** | Hunting; TSM-E1 | Above Nettlehook: ledges, cropped heather, goat tracks and droppings; the TGY ledges' near edge (bible TP28). |

### TSM.5 Player-facing sequence

**Beat 0 — This year's page (`S00_hook`).** *Objective: Ask Runa about the tally.* `TSM-D1`. She shows the page: Kvist, left out.

**Beat 1 — The Kvists (`S01_sedges`).** *Objective: Visit the Kvist house.* `TSM-D2` (Ama, Pell). Inspects (2 required): the cot, the doorframe strokes. Optional: the spoon.

**Beat 2 — The count (`S02_count`).** *Objective: Ask Grima what the Kvists owe.* `TSM-D3`. Two wood hauls and a meat share. Grima is not cruel: the count kept Hushfold alive when there was nothing else.

**Beat 3 — Two hauls (`S03_haul_one`, `S04_haul_two`).** *Objective: Haul the Kvists' wood from the near woodstacks.* Load a sledge (3 s), pull it (carry-state, slow walk, sprint disabled) along the shelf path. Gusts: the whistle tells; stop behind a chalked face and the sledge is braced; caught in the open, the player is knocked down and the sledge slides back to the last face (never off the shelf). Unload at the Kvist woodpile (3 s). Pell joins the second haul (`TSM-B2.01`). **Crew alternative** for the physical strain: none needed (no skill), but Pell and two youths can pull with the player on either haul, halving gust knock-backs.

**Beat 4 — The meat share (`S05_hunt`).** *Objective: Bring the Kvists a meat share.* Track a cliff goat on the shoulder: three sign inspects (tracks, droppings, cropped heather) narrow the ledge; take it with Hunting. **Crew alternative:** Pell's snare line for snowhares (set three snares, watch interaction ~30 s; equals a share). Carry the meat home (light carry). **TSM-E1** on the way down: the pack smelled it.

**Beat 5 — First smoke (`S06_first_smoke`).** *Objective: Light the Kvist hearth at Runa's word.* At dusk Runa blows **Gather** from the hearth step; every household lights its fire. The player lights the Kvists' (interaction). **The wonder** (TSM.7).

**Beat 6 — The reading (`S07_reading`).** *Objective: Stand at the tally reading.* Runa reads (`TSM-D5`). She reaches the Kvists and stops. The choice. Then the player's own place.

**Beat 7 — Done (`S08_close`).** *Objective: Eat.* Smoke Week supper. `TSM-D7`. Quest Completed.

### TSM.6 Encounters

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TSM-E1** | 3 × Ridge Wolf runner, 1 × Ridge Wolf howler | Goat shoulder descent, on the path down | Runners: Aggressive, go for the **carried meat** (one tries to snatch; a successful snatch drops the meat 5 m away, where it can be picked up again). Howler: holds a rock; calls. | **Runner lunge:** chest down, ears flat (~0.9 s). **Snatch:** circles behind, head low, a growl (~1.2 s), then dives for the carry. **Howler:** head back (~1.5 s), rising howl calls one extra runner (once); interrupted by a hit or the **Fall** call. | Protect a carry while you fight; the snatch is the readable twist. | 55–80 s; player at 55–75% HP. |

**Rules.** Wolves fight until defeated at 0 HP (CDR-1). The meat cannot be lost: if dropped it stays where it fell until the player picks it up (and after a logout it returns to the shoulder kill site). If the player took the snare alternative, E1 still runs (hares smell too).

### TSM.7 The wonder moment: the smokes lean together

| Time | Element | Spec |
|---|---|---|
| 0 s | **Gather** | Runa blows Gather from the hearth step (glyph: three dots). |
| 2–8 s | **Fires** | Doors open down the line; fires are lit in a ripple. The player lights the Kvists' last. |
| 8–20 s | **Straight up** | In the still cold, every smoke rises straight, a row of grey columns. Snow falls straight. The shelter line goes quiet. |
| 20–30 s | **The lean** | At one height, all the columns bend together the same way, toward the pass and the far shielings beyond it, like a row of reeds in a current. (An inversion layer moving with a high wind; nobody says so.) |
| 30 s+ | **Runa** | `TSM-D4`: *"Smoke points at whoever's still out. Old saying."* (before TF-M5: Hushfold's column is still out at the far shielings; after TF-M5: she adds "There's nobody out this year. It still points.") |
| What it means | Weather. It points at nobody in particular and proves nothing. |

### TSM.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_hook` | Ask Runa about the tally. | `TSM-D1` end | Yes |
| `S01_sedges` | Visit the Kvist house. | `TSM-D2` end + 2 inspects | Yes |
| `S02_count` | Ask Grima what the Kvists owe. | `TSM-D3` end | Yes |
| `S03_haul_one` | Haul the Kvists' wood (1 of 2). | Carry-deposit of sledge load at Kvist woodpile | Yes |
| `S04_haul_two` | Haul the Kvists' wood (2 of 2). | Second deposit | Yes |
| `S05_hunt` | Bring the Kvists a meat share. | Meat (goat or snare share) carry-deposited at the Kvist house; TSM-E1 defeated | Yes |
| `S06_first_smoke` | Light the Kvist hearth at Runa's word. | Hearth interaction after Runa's Gather; `TSM-D4` end | Yes |
| `S07_reading` | Stand at the tally reading. | `TSM-D5` choice + `TSM-D6` answer | Yes |
| `S08_close` | Eat. | `TSM-D7` end | Yes (→ Completed) |

`S03`–`S05` run in parallel; `S06` unlocks when all three are done.

### TSM.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `TSM_CLAIM` = counted / shared / private | `TSM-D5` | TRR, TF-M5 Runa lines (request), Hushfold barks |
| `TH_HUSHFOLD_VOICE` | `TSM-D5`: true for counted or shared; false for private | TF-M5 placement (§9.3) |
| `TSM_PLAYER_TALLIED` | `TSM-D6` | Every Hushfold and Nettlehook host's address (player's name); TNK-D8; TME01 |

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Counted** — *"Work done for a household counts for it. The hauls are the Kvists'."* | Runa writes the Kvists in, five strokes. The shelter line agrees, slowly: work is the rule, and the rule is kept. `TH_HUSHFOLD_VOICE` = true. | Grima: "So anyone can buy a place with a stranger's back." A precedent: next winter's poorest households will look for someone to haul for them. | TF-M5: Runa speaks for Hushfold with the tally in her hand. TRR: Ama ties her ribbon as a household that "kept the count". |
| **Shared** — *"Need makes a claim. And keeping a sick man alive is Hushfold's work."* | Runa adds a new line to the tally's form: *"shelter given"*, counted as hauls. Every household's granary share is cut by a measure to carry it. `TH_HUSHFOLD_VOICE` = true. | Thinner stores for everyone; three households grumble at supper; Grima signs last. | TF-M5: Runa speaks for Hushfold and the new line is read out. TRR: the Kvists are asked to tie a ribbon by others, not by themselves. |
| **Private** — *"Leave the tally. I'll see they eat."* | The page stands. The player's wood and meat feed the Kvists; Runa adds a sack from her own store, quietly. `TH_HUSHFOLD_VOICE` = false. | The Kvists eat and are not counted. Ama's pride. Hushfold has no agreed position to carry anywhere. | TF-M5: Runa stands alone. TRR: Ama hesitates to ask about the ribbon at all. |

**The player's place.** Yes: *"Expected."* Runa writes the player's name under "expected from the path" and every Hushfold and Nettlehook host uses it from then on (`TSM_PLAYER_TALLIED`; bible §5.3 rule 4; nothing else changes). No: *"Not this year."* "Walker" stays. Neither affects `TH_HUSHFOLD_VOICE`.

### TSM.10 Rewards, failure, co-op

| Reward | Type | Notes |
|---|---|---|
| Smoke Week supper | Gift / buff | One cooked food item (item pass). |
| A bench at the tally hearth | Access | Rest point at Hushfold. |
| Skill XP | Actions only | Hunting, Woodcutting (optional), Melee or Ranged. |
| *Rope-Raising Day* | Story | After TF-M3. |

| Situation | Handling |
|---|---|
| Sledge caught by gusts repeatedly | Slides back only to the last chalked face; load never lost. Crew halves knock-backs. |
| Meat dropped / logout with meat | Stays where it fell / returns to the kill site. |
| No Hunting skill | Pell's snares. |
| Death | Respawn at Hushfold hearth; hauled loads and deposited meat persist. |
| Walking away | Stays Active; resume with Runa (`TSM-B1.03`). |
| Fail state | None. |
| Co-op | Each player hauls and hunts for their own state (shared wolves). The reading is per player; Runa's page shows each player's own `TSM_CLAIM` (fallback: the host's on the prop, own choice in dialogue). Name address is per player. |

### TSM.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| **Sledge carry** with slide-back to checkpoint | Systems | Heavy carry state; gust event moves it to the last brace point. **Fallback:** gust knocks the player down only; sledge stays. |
| **Snatchable carry** | Systems / AI | Creature action that forces a drop of a carry-state object at a point. **Fallback:** no snatch; wolves attack normally. |
| **Smoke columns** | Art / VFX | Particle columns with a scripted bend at a height; per-player presentation. **Fallback:** inspect line. |
| **Name address** | Dialogue system | Hosts' lines swap "walker" for the player's name on `TSM_PLAYER_TALLIED` or `TME01_TALLIED` (TME01, Settlements and Combat file). |
| Creatures | Encounters package | Ridge Wolf runner (snatch), howler. |

**Mystery ledger.** *Who the traveller was:* author truth unspecified; a walker with a fever who got well and left. **Never identified** (no cross-region tie; the spoon is unremarkable work). *Wrong reading:* the Kvists were hiding someone dangerous. Self-contained.
**Open decisions.** (1) The new tally line "shelter given" is a custom change [NEW]; TF-M5 may read it aloud (request). (2) Whether Elira's storekeepers appear: with `TH_STORES` = seized, one Runa line notes the granary is fuller this year (`TSM-D5.03`); no other link.

| Review finding | Revision |
|---|---|
| Grima risked being the villain. | Grima's count kept Hushfold alive; she signs in every outcome. |
| "Private" risked being the obviously wrong option. | It feeds the family at once with no cut to anyone's stores; its cost is civic. |
| The player-tally question risked being tied to the claim. | Separate question, no effect on posture. |
| The far shielings risked a map conflict. | Not visited; the woodstacks are near. |

### TSM.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Runa Weatherall** | The tally, every household. Her family "came over in the thaw". | Anything about the Gatefall (TF-M5). | Warm, tired, proud. Says "we" for the whole line. |
| **Ama Kvist** [NEW] | The traveller, the three weeks, the fever. | His name beyond "Tam, he said". | Proud, short, will not ask. |
| **Pell Kvist** [NEW] | Snares, the shelf path. | Why adults are so slow about everything. | Fifteen, keen, embarrassed by his mother's pride. |
| **Grima Loft** [NEW] | Every haul for thirty winters. | How to say yes quickly. | Hard, fair, counting. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| TSM-B1.01 | Pell | Available, at Nettlehook | *"You're the one who fixed the rope. Hushfold's tally's wrong. Mam won't say. I'm saying."* |
| TSM-B1.03 | Runa | Active, returns | *"Page is still open. So is the Kvists' door."* |
| TSM-B2.01 | Pell | Second haul | *"I'll take the front. You take the gusts."* |
| TSM-B2.02 | Grima | Watching a haul | *"That's a haul. Badly loaded. Still a haul."* |
| TSM-B3.01 | Hushfold host | `TSM_PLAYER_TALLIED` | *"{PLAYER}. You're expected. Bed by the door's yours if you want it."* |
| TSM-B3.02 | Hushfold host | `TSM_CLAIM` = shared | *"A measure short this winter. For a stranger's fever." (beat) "I'd have done it."* |

#### Nodes

```
TSM-D1.01 RUNA: (book open on the stand) "Smoke Week. We read the tally on the last night. We're always proud of it."
TSM-D1.02 RUNA: "Not this page." (turns it) "Kvist. Left out. Two hauls and a meat share short."
  > "Why short?"                                           → TSM-D1.10
  > "Who decides?"                                         → TSM-D1.20
TSM-D1.10 RUNA: "They nursed a sick walker three weeks. We kept them back from shared work. Fever. Nobody knew what it was."
TSM-D1.11 RUNA: "He got well. Walked on. We counted, the way we count." (beat) "We're right. I hate it."   → TSM-D1 options
TSM-D1.20 RUNA: "We do. Hushfold. I read it. Grima counts it. Everyone sits and listens and argues after."
TSM-D1.21 RUNA: "If you want to argue, do the hauling first. Nobody here listens to soft hands."
      {event: S00_hook}
```

```
TSM-D2.01 AMA: (at the door, not opening it wide) "If Runa sent you, we're fine."
TSM-D2.02 PELL: (behind her) "We're not fine."
TSM-D2.03 AMA: "Tam, he said his name was. Burning up on the shelf path. What were we to do, count him?"
  > "You did right."                                       → TSM-D2.10
  > "I'll do the hauls."                                    → TSM-D2.20
TSM-D2.10 AMA: "Right doesn't go on the tally."   → TSM-D2.20
TSM-D2.20 AMA: "We don't take charity." (beat) "Hauls aren't charity. Hauls are hauls."
TSM-D2.21 PELL: "Woodstacks are up the shelf. I'll show you. Mam, I'm showing them."
      {event: S01_sedges}
```

```
TSM-D3.01 GRIMA: "Two hauls. One meat share. Same as anyone. Same as me."
TSM-D3.02 GRIMA: "Thirty winters I've counted. The count's why there's a Hushfold. Clanless don't get given. We do."
  > "And if someone else does their hauls?"                 → TSM-D3.10
  > "Fair."                                                 → end
TSM-D3.10 GRIMA: "Then it's hauled." (looks at the player a long time) "What it counts for, that's the reading."
      {event: S02_count}
```

```
TSM-D4.01 RUNA: (as the smokes lean) "Smoke points at whoever's still out. Old saying."
TSM-D4.02 [TF-M5 not Completed] RUNA: "Our column's at the far shielings till the herds come down. It's pointing at them." 
TSM-D4.02 [TF-M5 Completed] RUNA: "There's nobody out this year." (beat) "It still points."
      {event: S06_first_smoke}
```

```
TSM-D5.01 RUNA: (reading) "Weatherall: beds four, hauls five, meat two. Loft: beds two, hauls five, meat one..." (and on, through the line)
TSM-D5.02 RUNA: (reaches the page's end; stops) "Kvist."
TSM-D5.03 [TH_STORES = seized] RUNA: "Granary's fuller than last year. Elira's people brought sacks up. Nobody asked from where."
TSM-D5.04 GRIMA: "Two hauls short, one meat."
TSM-D5.05 PELL: "They're hauled. The walker hauled them. I was there."
TSM-D5.06 RUNA: (to the player) "You did the work. Say what it counts for. Then we'll argue."
  > "Work done for a household counts for it. The hauls are the Kvists'."            → TSM-D5.10
  > "Need makes a claim. And keeping a sick man alive is Hushfold's work."           → TSM-D5.20
  > "Leave the tally. I'll see they eat."                                            → TSM-D5.30
TSM-D5.10 GRIMA: "So anyone can buy a place with a stranger's back." (beat) "...It's hauled. I said it was hauled."
TSM-D5.11 RUNA: (writes five strokes) "Kvist: hauls five." (to the room) "We count the work. We always have."   {set TSM_CLAIM = counted; set TH_HUSHFOLD_VOICE}  → TSM-D6.01
TSM-D5.20 RUNA: (long pause) "A new line." (writes) "'Shelter given.' Counted as hauls."
TSM-D5.21 GRIMA: "That's a measure off every house."
TSM-D5.22 RUNA: "Yes." (beat) "We kept a man alive. We'll be a measure hungry for it."
TSM-D5.23 GRIMA: (takes the pen; signs last) "Put my name at the bottom. So they know I argued."   {set TSM_CLAIM = shared; set TH_HUSHFOLD_VOICE}  → TSM-D6.01
TSM-D5.30 RUNA: "Then the page stands." (quietly, to the player) "I'll put a sack by their door. Don't tell Grima."
TSM-D5.31 AMA: (from the back) "We'll eat. Thank you." (it costs her)   {set TSM_CLAIM = private; TH_HUSHFOLD_VOICE stays false}  → TSM-D6.01
```

```
TSM-D6.01 RUNA: (the end of every tally) "Expected from the path." (looks at the player) "And you? Expected or not?"
  > "Expected."                                          → TSM-D6.10
  > "Not this year."                                     → TSM-D6.20
TSM-D6.10 RUNA: "Then I need your name." (writes it) "{PLAYER}. Expected." {set TSM_PLAYER_TALLIED}  → TSM-D7.01
TSM-D6.20 RUNA: "Walker it is. Bed by the door's still yours."   → TSM-D7.01
```

```
TSM-D7.01 RUNA: "That's the tally read. Now we eat, and say worse things about the weather."
TSM-D7.02 [TSM_PLAYER_TALLIED] RUNA: "Sit, {PLAYER}. You're counted. Counted people carry bowls."
TSM-D7.03 PELL: "Rope-Raising's at the Narrows when they make the span proper. Mam wants to ask about a ribbon. She won't."
TSM-D7.04 AMA: "Pell."
      {event: S08_close → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| TSM-I1.01 | Tally page | *"Households in a column, strokes for hauls. The Kvist line ends after two strokes, and a line is drawn under it."* |
| TSM-I1.02 | The cot | *"Made up neatly. A fever-cloth folded on the pillow, washed thin."* |
| TSM-I1.03 | Doorframe strokes | *"Two split-wood strokes. Every other door on the line has five."* |
| TSM-I1.04 | Spoon (optional) | *"A carved spoon. Plain work, not Hushfold's pattern. Left on the shelf like a thank-you."* |
| TSM-I1.05 | Goat sign | Tracks: *"Split hooves, fresh, going up."* Droppings: *"Warm."* Heather: *"Cropped to the stem. It's on the next ledge."* |

---

## TRR — Rope-Raising Day

### TRR.1 The quest in one paragraph

Aud Hammerlee has finally replaced the storm patch the player helped throw across the **Narrows** with a proper span, and a span made permanent is raised the old way: **Rope-Raising Day**. A bridgewright crew inspects it in front of an apprentice and a regular traveller, so that no crew's knowledge becomes private power; Aud asks the player to be the traveller. Then the children of every highstead carry the **unweighted guide line** across, hand over hand, while an adult walks ahead calling them forward between gusts; this year that adult is the player, with a horn. Thyra Brack brings the old guide line from Three Calls so a strand of it can be spliced into the new one, and its knots turn out to be a notation, every tenth knot doubled, that the old crews used for something they did not write down. Elders judge knots, and the player's knot is judged with everyone's, badly or well. At the meal, Ama Kvist asks, or does not quite ask, whether a clanless household may tie a **witness ribbon** on the span, as the clan households do. Ressa checks the safety; Hadrik eats and listens and does not let it become a vote. When the guide line touches the far anchor, every horn post in earshot blows Rest at once, and the Narrows throws it back as one chord.

**Remember:** the chord, and twenty children cheering inside it. **Want next:** the Assembly, where the highsteads stand (TF-M5).

### TRR.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| **A. A pure festival of minigames.** | Rejected. No stakes; the ribbon would be decor. |
| **B. A clan elder blocks the ribbon and the player out-argues him.** | Rejected. Talk-led and villain-shaped. |
| **C. Witness the inspection → lead the line → knot judging → the old line's notation → ribbon placement as a community choice** (selected). | **Selected.** The player works the festival; the ribbon decision has three honest shapes. |

| Element | Source | Status |
|---|---|---|
| Rope-Raising Day: children carry the unweighted guide line, elders judge knots, communal meal; Bridgewrights lead, Ressa checks safety, Hadrik hears contributions without a vote; migrant households may place a nonstructural witness ribbon | Part 3 proposed occasions; bible §7.1 | [NEW, Part 3] |
| Inspection witnessed by an apprentice and a regular traveller | Part 3 proposed customs | [NEW, Part 3] |
| A faded guide line at Three Calls whose repair notation once marked a civilian evacuation crossing | Part 3 | [NEW, Part 3] |
| Aud Hammerlee; the Narrows bridge | Bible §5.2, TP07, TF-M1 | [NEW] |
| Hadrik Stonewake places and listens; does not decide | Anchors I; bible §5.1 | [CANON] / limit |
| Brynjar would die for any Thornfell child | Anchors II | [CANON] |
| Held at any first permanent span of a season (not only spring); the old-line splice; the knot sequence; the chord | This package | [NEW] |

### TRR.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `thornfell.side.rope_raising_day` |
| Series | *Clans of the High Steads*, part 3 of 3 (festival) |
| Type | Festival |
| Unlock | TSM Completed **and** TF-M3 Completed. Offered by Aud at the Narrows (`TRR-D1`) or Tova (`TRR-B1.01`). |
| Length | 25–35 minutes |
| Combat share | 0–5% (optional) |
| Skills | None required. Knot-tying is a festival interaction, not a skill. |
| Choice | Where the ribbon goes (`TRR_RIBBON`: everyone / witness / old_line) |
| Outputs | `TH_HIGHSTEADS_TOGETHER`; `TRR_RIBBON`; the Narrows permanent span (presentation) |
| **Anchor** | Bridgewrights (Aud), the highsteads together (Nettlehook, Hushfold, Three Calls). |
| **World-truth row** | H16 as a seed only (the old line's notation marked an evacuation crossing: author knowledge; never stated). H23. |
| **Revelation role** | **Supports R06 (sealing half)** with an unexplained seed: a crossing that was counted in knots. Owns nothing. |
| **Recurring evidence** | The **old guide line** (object; custodian: Thyra Brack at Three Calls). Its notation is seen, not decoded. |
| **State compliance** | Inactive → Active on `TRR-D1` end; Completed on `TRR-D6` end. No fail path; choice in `TRR_RIBBON` and `TH_HIGHSTEADS_TOGETHER`. Resume hook: Aud at the near anchor (`TRR-B1.03`). |

### TRR.4 The places

**MAP VERIFICATION REQUIRED:** the Narrows as in TF-M1 (TP07); the meal at the near-side ledge (Nettlehook's ovens carried down on sledges).

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Near anchor** | Hook; inspection | New anchor posts, ropes tarred black, Aud's crew in clean coats (they own one each). Clan ribbons in a basket by household; no basket for Hushfold. |
| **B. The span** | Inspection walk; line carry | The new span beside the stumps of the storm patch. Seven inspection points (lashings, a splice, a toggle, deck boards). Fluted faces above: the whistle tells. Chalked "kneel" marks every 10 m on the deck. |
| **C. Far anchor** | The chord | Where the guide line is made fast. Clear view of the ravine walls. |
| **D. Meal ledge** | Knots; ribbon; optional crows | Trestles, Nettlehook's bread, a goat on a spit, the knot-judging bench with three elders, Hadrik at the end of a bench as if he'd just sat down. |

### TRR.5 Player-facing sequence

**Beat 0 — Be the traveller (`S00_hook`).** *Objective: Ask Aud what she needs.* `TRR-D1`.

**Beat 1 — The inspection (`S01_inspect`).** *Objective: Witness the span inspection.* Walk the span with Aud and her apprentice. At each of seven points the apprentice states a check; the player inspects (all seven required; each a short text). At one point (the splice, point 4) the apprentice is wrong (*"Splice is sound"*; the inspect shows a tuck pulled); the player can say so (`TRR-D2.10`) or not. If they say so, the crew re-tucks it in front of everyone and Aud is delighted; if not, Aud finds it herself at the end and is less delighted (no failure; flag `TRR_SPLICE_CALLED`).

**Beat 2 — The old line (`S02_old_line`).** *Objective: Look at the old Three Calls guide line.* Thyra has brought it. Inspect (required): the knots and the doubled tenth knots. Splice a strand into the new line (3 s channel). Nobody can read the notation (`TRR-D3`).

**Beat 3 — The children's line (`S03_line_carry`).** *Objective: Lead the children across with the guide line.* Twelve children hold the light line at intervals. The player walks ahead. **Calls conduct the carry:** **Gather** brings the children forward to the player; the whistle tells a gust: blow **Fall** and the children kneel at the chalk marks and hold the rail; after the gust, **Gather** again. Three snag points (iced rail post, a toggle catching the line, a deck board lifting): clear each (2 s) before calling them on. Wrong call: Gather in a gust makes the children giggle and kneel anyway (Ressa, from the anchor: *"Fall, walker."*); nobody is ever in danger. Tova is third on the line and hums the gust before the whistle (with TNR Completed).

**Beat 4 — The chord (`S04_far_anchor`).** *Objective: Make the line fast at the far anchor.* Tie off (interaction). **The wonder** (TRR.7).

**Beat 5 — Knots (`S05_knots`).** *Objective: Tie a knot for the elders.* At the meal: a four-step knot sequence (bight, turn, tuck, set) chosen from prompts; any order produces a knot. Three elders judge (Aud plus two: Osk and Grima; with `TNR_ROTA` = lots the two are drawn by lot and are a Hushfold child and a Nettlehook baker). Scores are comments (`TRR-D4`), never pass/fail.

**Beat 6 — The ribbon (`S06_ribbon`).** *Objective: Hear Ama out.* `TRR-D5`. The choice.

**Beat 7 — Tie it (`S07_ribbon_tied`).** *Objective: Tie the ribbon(s).* Walk to the span or the old line, tie (2 s). `TRR-D6` (Aud, Hadrik). Quest Completed.

### TRR.6 Encounters

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TRR-E1** (optional) | 1 × Ridge Crow flock | Meal ledge, after the knots | Opportunist: dives for the bread trestle, not people | Swirl tightens over the trestle (~1.2 s), then the flock drops on the bread. Children shriek, gladly. | Comic beat; a chance to be a hero about bread. | 20–30 s. Ignoring it costs one loaf (bark). |

No other combat. Nothing here can hurt a child.

### TRR.7 The wonder moment: one chord

| Time | Element | Spec |
|---|---|---|
| 0 s | **Fast** | The player ties off the guide line at the far anchor. The children let go on Aud's word. |
| 1 s | **Aud** | Aud blows Rest from the near anchor (glyph: flat line). |
| 2–4 s | **Every post** | Nettlehook's ropeway head, Three Calls, Passwatch's tower, the Blind Corners warden: every horn post in earshot blows Rest at once (they were watching for the line). |
| 4–9 s | **The chord** | The Narrows' two walls throw it back as one sustained chord, fuller than any horn, for about five seconds. Snow sifts off the fluted faces. |
| 6–12 s | **The cheer** | The children cheer inside the chord and the walls give that back too. |
| With `TTH_KEEPER` set | **The tail** | Three Calls adds the Third Horn after Rest, faint: "someone's still out" (Thyra: *"Somebody always is."*). |
| What it means | Acoustics. Two walls and a lot of horns. Nobody explains it because everyone knew it would happen; only the player didn't. |

### TRR.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_hook` | Ask Aud what she needs. | `TRR-D1` end | Yes |
| `S01_inspect` | Witness the span inspection. | 7 point inspects + `TRR-D2` end | Yes |
| `S02_old_line` | Look at the old Three Calls guide line. | Old-line inspect + `splice` channel | Yes |
| `S03_line_carry` | Lead the children across with the guide line. | 3 snags cleared + children reach far anchor volume | Yes |
| `S04_far_anchor` | Make the line fast at the far anchor. | Tie-off interaction (chord plays) | Yes |
| `S05_knots` | Tie a knot for the elders. | Knot sequence + `TRR-D4` end | Yes |
| `S06_ribbon` | Hear Ama out. | `TRR-D5` choice resolved | Yes |
| `S07_ribbon_tied` | Tie the ribbon. | Tie interaction at span or old line + `TRR-D6` end | Yes (→ Completed) |

### TRR.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `TRR_SPLICE_CALLED` | `TRR-D2.10` | Aud's lines |
| `TRR_KNOT` = neat / odd / disaster | Knot sequence | Barks |
| `TRR_RIBBON` = everyone / witness / old_line | `TRR-D5` | TF-M5 (request), Narrows barks |
| `TH_HIGHSTEADS_TOGETHER` | `TRR-D5`: true for everyone or witness; false for old_line | TF-M5 placement (§9.3) |

Ama's opener depends on `TSM_CLAIM`: counted, she asks herself; shared, others ask for her; private, Pell asks and she stops him, and the player can take it up.

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Everyone** — *"Everyone ties one. Clan or not. One span, one row."* | Aud hands out ribbons from every basket and a new one; every household, clan or clanless, ties one on the near rail. `TH_HIGHSTEADS_TOGETHER` = true. | A few clan elders feel their ribbons mean less now; Osk ties his last and says nothing. The Kvists' ribbon is one among many and nobody sees it particularly. | TF-M5: the highsteads stand as one block. Narrows bark: a rail of ribbons. |
| **Witness** — *"The Kvists tie a witness ribbon. As witnesses, not as a clan."* | Ama ties a plain ribbon on the far rail, apart, as Part 3's nonstructural witness ribbon: belonging made visible without a clan oath. `TH_HIGHSTEADS_TOGETHER` = true. | It marks the Kvists out. Ama: "Everyone will know which one's ours." That's the point, and it's also the cost. | TF-M5: highsteads stand together with Hushfold at the front. |
| **Old line** — *"Tie it on the old Three Calls line. It's carried more people than this span has."* | The ribbon goes on the old guide line, which Thyra takes home to hang in the shelter. `TH_HIGHSTEADS_TOGETHER` = false. | No row on the span; no argument on the day; the highsteads go home separately. | TF-M5: Nettlehook stands with its clan neighbours. Thyra hangs the line by the horn map; it is still there. |

None is wrong.

### TRR.10 Rewards, failure, co-op

| Reward | Type | Notes |
|---|---|---|
| **The Narrows permanent span** | World change | Presentation swap at the Narrows (storm-patch stumps remain beside it). |
| Festival meal | Gift | Cooked food (item pass). |
| A judged knot | Standing (flavour) | Bridgewright barks remember it. |
| Small payment | Currency | Aud's witness fee "for being a traveller, which you are". |

| Situation | Handling |
|---|---|
| Wrong call during the carry | Children kneel anyway; Ressa corrects; no harm, no failure. |
| Player leaves mid-carry | The children wait at the nearest kneel mark with an adult; resume from there. |
| Death (optional crows) | Respawn at the meal ledge; step kept. |
| Walking away | Stays Active; resume with Aud (`TRR-B1.03`). |
| Fail state | None. |
| Co-op | Partners can both walk ahead; either's calls conduct the line. Knots and the ribbon choice are per player; the rail's ribbons follow each player's own `TRR_RIBBON` (fallback: host's). |

### TRR.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| **Call-conducted NPC group** | AI / Systems | Twelve child NPCs on a path with kneel points; states: advance (on Gather), kneel (on Fall or gust), wait. **Fallback:** six children; scripted advance on Gather only. |
| Chord | Audio | One authored chord bounce with distance-staggered horn one-shots. |
| Knot sequence | UI | Four prompts; result lookup to three outcomes. **Fallback:** dialogue choices. |
| Ribbon props | Art / Systems | Per-player ribbon rail states. |
| Festival crowd | NPC | Ambient eaters, three judges, Hadrik seated (no pathing). |

**Mystery ledger.** *The old line's doubled tenth knots:* author truth: the old crews' count of people taken across in an evacuation, one knot a person, doubled for a family (Part 3; H16 years). **Withheld** in Thornfell beyond Thyra's "It was for counting something. It wasn't bread." *Wrong reading:* festival decoration. No later owner is required; TF-M5's roster may make a careful player wonder.
**Open decisions.** (1) Festival timing: Part 3 places Rope-Raising Day at the first safe spring opening; this package holds it at the first permanent span of a season so it can feed TF-M5 [PROPOSAL — DIRECTOR]. (2) Hadrik's presence is presentation and two lines; he does not decide.

| Review finding | Revision |
|---|---|
| Children on a bridge in gusts. | Kneel marks, Ressa at the anchor, nothing can knock a child; wrong calls are funny, not dangerous. |
| Ribbon refusal as villainy. | No one forbids it; the choice is about where belonging shows, and each shape has a cost. |
| Hadrik risked ruling. | He listens and refuses to make it a vote (`TRR-D6.03`). |

### TRR.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Aud Hammerlee** | Every lashing. The custom. | The old line's notation. | Swears at rope affectionately. Loves being corrected by a traveller. |
| **Ama Kvist** | What a ribbon means to clan households. | Whether she's allowed. | Will not ask; asks anyway, badly. |
| **Thyra Brack** | That the old line is old. | What the knots counted. | Dry. |
| **Ressa Highcrag** | Safety. | — | One word where three would do. |
| **Hadrik Stonewake** | That the Assembly is afraid; who brought bread. | — | Gentle, wry, refuses to be the decision. |
| **Brynjar Korr** (optional) | Which child is where on the line. | — | Loud; protective. Variant by `TH_BRYNJAR`. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| TRR-B1.01 | Tova | Available | *"Aud made the bridge proper. There's a day for it. You have to come, it's a rule. Probably."* |
| TRR-B1.03 | Aud | Active, returns | *"Rope's waiting. Rope's patient. I'm not."* |
| TRR-B2.01 | Brynjar | Carry, `TH_BRYNJAR` = disowned | *"Mind the little one third from the end. If she slips, I'm going in after her, bridge or no bridge."* |
| TRR-B2.02 | Brynjar | Carry, `= defended` | *"Readiness. This is readiness. Twelve of them on a line and every one kneels on the call. Good."* |
| TRR-B2.03 | Ressa | Wrong call in gust | *"Fall, walker."* |
| TRR-B3.01 | Baker | Crows took a loaf | *"That was the good loaf."* |
| TRR-B3.02 | Narrows haulier | Completed, `everyone` | *"Rail's all ribbons. Can't tell whose is whose. Suppose that's it."* |

#### Nodes

```
TRR-D1.01 AUD: "Proper span. Proper rope. Proper day for it, which means everyone comes and nobody works but me."
TRR-D1.02 AUD: "Inspection's witnessed. An apprentice and a regular traveller. Keeps us honest. Keeps me from being a wizard about knots."
TRR-D1.03 AUD: "You've crossed this gap more than anyone this season. You're the traveller."
  > "What do I do?"                                       → TRR-D1.10
TRR-D1.10 AUD: "Look where she points. If she's wrong, say so. She'd better not be wrong."   {event: S00_hook}
```

```
TRR-D2.01 APPRENTICE: (at point 4) "Splice is sound."
  > [inspected point 4] "That tuck's pulled."              → TRR-D2.10
  > "Next."                                                → TRR-D2.20
TRR-D2.10 AUD: (looks; beams) "It is! It's pulled! Traveller found it!" (to the crew) "Re-tuck, and everyone watch you do it."   {set TRR_SPLICE_CALLED}  → TRR-D2.30
TRR-D2.20 (at the end) AUD: "Point four." (re-tucks it herself) "Nobody saw that. I saw that."   → TRR-D2.30
TRR-D2.30 AUD: "Span's sound. Write it." (the apprentice writes) {event: S01_inspect}
```

```
TRR-D3.01 THYRA: (unrolling a grey line on the snow) "Old guide line. Three Calls has had it since before my grandmother. You splice a strand in. Custom."
TRR-D3.02 THYRA: "Knots all along. Every tenth one doubled."
  > "What do they count?"                                 → TRR-D3.10
TRR-D3.10 THYRA: "Something. It wasn't bread." (beat) "Splice it in. It's held more than this span has."   {event: S02 on splice}
```

```
TRR-D4.01 OSK: (holding the player's knot up) "Hm."
TRR-D4.02 [TRR_KNOT = neat] AUD: "That would hold a goat. A large goat." GRIMA: "It's counted."
TRR-D4.02 [TRR_KNOT = odd] AUD: "That's a knot. It's not a knot I know. It'll hold till Tuesday." GRIMA: "Half a stroke."
TRR-D4.02 [TRR_KNOT = disaster] AUD: (delighted) "I've never seen that in my life." OSK: "Nor should anyone." (the children applaud it anyway)
TRR-D4.03 [TNR_ROTA = lots] AUD: "Judges by lot this year. Osk's idea. I'm still recovering."
      {event: S05_knots}
```

```
TRR-D5.01 [TSM_CLAIM = counted] AMA: (to Aud, then the player) "Hushfold hauled for this span. Some of us. We'd tie a ribbon. If it's allowed."
TRR-D5.01 [TSM_CLAIM = shared] RUNA: "The Kvists kept a man alive and Hushfold went a measure short for it. They should tie a ribbon." AMA: "Runa—"
TRR-D5.01 [TSM_CLAIM = private] PELL: "Mam wants a ribbon." AMA: "I don't." PELL: "She does."
TRR-D5.02 AUD: "Ribbons are clan custom. Not law. There's no law about ribbons. I've looked."
TRR-D5.03 OSK: "Custom is how we know who's ours."
TRR-D5.04 AUD: (to the player) "Traveller. You walked the span and the line. Where does it go?"
  > "Everyone ties one. Clan or not. One span, one row."                                  → TRR-D5.10
  > "The Kvists tie a witness ribbon. As witnesses, not as a clan."                        → TRR-D5.20
  > "Tie it on the old Three Calls line. It's carried more people than this span has."      → TRR-D5.30
TRR-D5.10 AUD: (tipping the baskets out) "Everyone. Here's a pile. Take one." OSK: (last; ties his without a word)   {set TRR_RIBBON = everyone; set TH_HIGHSTEADS_TOGETHER}
TRR-D5.20 AMA: "Everyone will know which one's ours." (beat) "Good."   {set TRR_RIBBON = witness; set TH_HIGHSTEADS_TOGETHER}
TRR-D5.30 THYRA: "Then it comes home with me and hangs by the map." AMA: (relieved and not) "Nobody fights about it, then."   {set TRR_RIBBON = old_line}
      {event: S06_ribbon}
```

```
TRR-D6.01 AUD: "Span's raised. Line's fast. Ribbons are where they are. Eat something."
TRR-D6.02 HADRIK: (from the bench end) "Good bread. Who brought it?" (listens to the answer; nods) "Nettlehook. And the wood was Hushfold's."
TRR-D6.03 HADRIK: (someone asks him to rule on ribbons) "It's a festival. If I decide things at a festival, nobody will invite me." (beat) "I'll remember who stood where."
TRR-D6.04 [TH_HIGHSTEADS_TOGETHER] AUD: "When the Assembly sits, we'll stand as we tied. One lot."
TRR-D6.04 [else] AUD: "Assembly'll be Assembly. We'll stand where we stand."
      {event: S07_ribbon_tied → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| TRR-I1.01–.07 | Inspection points | Lashing: *"Tight. Tarred."* Toggle: *"Seated."* Deck board: *"Pegged both ends."* **Splice (point 4):** *"Three tucks. The last has pulled half out."* Anchor wrap: *"Five turns."* Rail: *"Sound."* Far lashing: *"Tight."* |
| TRR-I1.08 | Old guide line | *"Grey, hard with age. Knots at even spacing; every tenth knot doubled. Some doubled knots have a third tied small against them."* |
| TRR-I1.09 | Clan ribbon basket | *"A basket for each clan household. Plain ribbons, dyed by house. No basket says Hushfold."* |

---

## Package review summary

| Check | Result |
|---|---|
| Bible §7.1 contract fields | Every summary card declares Anchor, World-truth row, Revelation role, Recurring evidence, State compliance. |
| Three states | No fail or abandon anywhere. Every walk-away has a resume hook; every channel, carry and wrong answer recovers. |
| Evidence rule | The Narrows return, the call running the Line, the frost, the cable note, the smokes, the chord and the unanswered call prove nothing and identify nobody. Meanings come from the horn map, bed book, grooves, lintel, tally and testimony. |
| R16 | Planted in TWG as a call, a lintel name and "for strangers". The Crossing Concord is never named; the meaning is never recovered. Custody guaranteed by permanent grooves and lintel. |
| Anchor limits | Ressa's refusals concern accountable warning (the promise of a reply; no meaning on an unexplained call; no deeper bore); Dorn's altered returns stay "wind tricks"; Kaldren reports stresses only; Hadrik never decides; Brynjar protective, no war deeds. |
| Plates | Never reinstalled in any horn in any outcome; Eyvind tunes ordinary horns only, under Ressa's refusal of added depth. `[SPLINTER]` tags on every Eyvind node. |
| Split | Never sounded, shaped or reproduced; its page carries a name only. |
| Flags | Only bible §9.1 region flags set (`TH_THIRD_HORN`, `TH_HUSHFOLD_VOICE`, `TH_HIGHSTEADS_TOGETHER`, `TH_HORN_CODES`); all others quest-local. |
| Quest items | None. Carry-state objects only. |
| Lowmark | No Lowmark flag read; no grain route stated (TSM mentions seized stores only, with no origin). |
| Distinct verbs | compare / climb-decode / retune-perform / repair-ride-rota / haul-hunt / inspect-carry-celebrate. |
| **Independent review (2026-11-03)** | 8 findings (1 high, 4 medium, 3 low). High: TTH's rhyme differed from TFS's canonical verse; TTH-I3 now quotes TFS.14 word for word, the changing-last-word variant cut. Medium: name collisions with the main acts: Three Calls host Signy Brack (Act II rear guard Signy Rook) renamed **Thyra Brack**; Hallvor (Act II cairn name Hallvard Brenn) renamed **Leiv**. Medium: TNK's pruned ending duplicated TRR's single chord; now the posts answer Rest one by one, farthest first. Medium: Eyvind's custody said "clan tribunal"; aligned to Act II (held by the Ridge Wardens pending the Assembly). Medium: TTH lent a practice horn as if TF-M1 gave none; TF-M1's horn is now relied on, loan is carry-state fallback only. Low: two Eyvind-naming nodes untagged (TWG-D6.03, TNK-B2.02); tagged `[SPLINTER]`. Low: name-address readers now accept `TSM_PLAYER_TALLIED` or `TME01_TALLIED`; token unified to `{PLAYER}`. Low: Ranged mentions gated on S01 (superseded 2026-11-03, see next row). |
| **Director rulings reconciliation (2026-11-03)** | Applied `Caelmor_Director_Rulings_Combat_Ranged_Release.md`. CDR-1: shared rule §0.6 "Human enemies yield" replaced by defeat at 0 HP; TTH-E1, TSM-E1 wolves and TNR-E1 crows no longer disperse at low health (steps complete on *defeated*); TWG-E1 bandits no longer yield or are tied; lookout talk `TWG-D2` cut (T-4, ids kept as removed); TWG Beat 4, step table and speaker row updated. No scripted exceptions in this file. CDR-2: six "Ranged if S01 allows" hedges and the §0.6 skills line now read Melee or Ranged (first-class, never required). CDR-3: header release-scope wording replaced with milestone wording. Step ids, flags, beats and choices unchanged. |
