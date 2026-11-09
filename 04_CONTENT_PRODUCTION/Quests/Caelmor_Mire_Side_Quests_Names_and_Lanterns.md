# Mire Side Quests — Names Below; Lanterns and Tenders

**Status (2026-11-08):** Authored production content for Creative Director review (Mire bible §12, Batch 3, part A). Six side-quest packages in two interconnected questlines (bible §7.1): ***Names Below*** (**MSS** *The Stranger's Seat*, **MBA** *The Book of Arrivals*, **MEP** *The Empty Place*) and ***Lanterns and Tenders*** (**MLL** *The Broken Lantern Light*, **MLW** *The Lantern That Would Not Go Out*, **MLD** *Lifting Day*). Everything marked **[NEW]** is authored here and is not canon until the Director promotes it. **[CANON]** items come from the reconciled `LORE/` files. **[PROPOSAL — DIRECTOR]** marks a consequential choice the content is built on. **[APPROVED — id]** cites an architecture ruling. No schema, JSON or C# is created here. The Mire is an internal production milestone of the complete game (CDR-3). Combat follows `Caelmor_Director_Rulings_Combat_Ranged_Release.md`: every enemy is defeated at 0 HP (CDR-1); the Mire registers no scripted exception; every fight accepts melee or ranged and none requires ranged (CDR-2); standard systems over bespoke simulation (CDR-4).

**Controlled by:** `Caelmor_Mire_Narrative_Production_Bible.md` (author truth §2, cast and voice §5, side-quest slate §7.1, contract §7.3, Register of the Unreturned §7.6, revelation map §8, flags §9, encounter families §10, conventions §11). **Format:** mirrors `Caelmor_Thornfell_Side_Quests_Horn_and_Highsteads.md` (per-quest summary card with the six §7.1 contract fields, places, beats, encounters, strange-moment spec, steps, flags and choices, rewards, failure and co-op, integration, ledger, open decisions, review log). **Dialogue is inline** in each package (§x.12), node ids `<CODE>-D<n>.<nn>`, barks `<CODE>-B<n>.<nn>`, inspects `<CODE>-I<n>.<nn>`, encounters `<CODE>-E<n>`.

**Main-quest inputs read (the mains exist and were checked on 2026-11-08):** `Caelmor_Mire_Main_Act_I.md`, `_Act_II.md`, `_Act_III.md` and their dialogue files. Act III's input table reads three outputs of this file exactly: `MR_STRANGER_SEAT` (bool, MSS), `MR_LANTERN_LINE` (bool, MLL) and **Completion of *Lifting Day*** (MLD), plus the Stillgrave family's role names (MLL). This file sets them as Act III reads them (§0.4, §0.5).

---

## 0. Slate header

### 0.1 The six quests at a glance

| Code | Quest | Series (part) | Type | Unlock | Where | Core verb (primary first) | Gameplay identity | Strange / wonder moment | Sets |
|---|---|---|---|---|---|---|---|---|---|
| **MSS** | The Stranger's Seat | Names Below (1/3) | Memory/lore | MR-M1 Completed | Sorrowmere register room; Griefwatch vigil hall; Rootrest hall | **ask**, compare, sit | **Sit three Silt hearings as the stranger** and gather each one's evidence (a stake read, a household mark matched, a debt tally read); compare the three seats; re-leg the oldest one with root-wood | At Rootrest the soil bowl is passed to the player, unasked, and the soil in it is warm | `MR_STRANGER_SEAT` (true on completion); `MSS_RUBBING` |
| **MBA** | The Book of Arrivals | Names Below (2/3) | Memory/lore (Register case) | MSS **and** MR-M3 Completed | Sorrowmere archive loft; Marshfall (Rudd house) | **search**, match, decide | **Mend a damp book, then search it by weather run**: re-stitch the spine, page through candidate entries, match one to a carrier's tally token and a household book | The token's double knot, untied for the first time in thirty years, keeps its kinks and will not lie straight | `MR_ARRIVALS` (named / held) |
| **MEP** | The Empty Place | Names Below (3/3) | Settlement | MBA Completed | Sorrowmere (Keel house); Blackwater Landing; the root-timber lot past Rootrest | **read**, find, welcome | **Read a child's signs, find a living man in a ferry book, help him finish his work, bring him to the table** | Lew has been carving the same work sign Posy leaves on his plate | `MEP_HOME`; Names Below "away, not lost" column |
| **MLL** | The Broken Lantern Light | Lanterns and Tenders (1/3) | Environmental | MR-M1 Completed | Stillgrave Hollow; Sorrowmere memorial gardens | **gather**, tend, finish | **Night gathering, a lantern mend, then holding a lit line** while a family finishes a mourning ring and Earthen Echoes come out of the grief at the edge | When the ring is closed, Stillgrave's water stops bending the lantern light and lets it lie straight | `MR_LANTERN_LINE` (true on completion); `MLL_PLACE` |
| **MLW** | The Lantern That Would Not Go Out | Lanterns and Tenders (2/3) | Memory/lore | MLL **and** MR-M4 Completed | The Chapel roof and loft; Sorrowmere | **read**, craft, keep | **Read the Tenders' wax book, rebuild the seven-night lantern, keep it lit for one wet night** with trim-and-feed turns | The wax book's last night is signed "Kept." in a hand no Tender knows | `MLW_KEEPER` |
| **MLD** | Lifting Day | Lanterns and Tenders (3/3) | Festival | MLW **and** MR-M2 Completed | The Standards Causeway; Sorrowmere long table | **carry**, cook, celebrate | **A festival you work**: cook for the table, settle who walks the repaired way first and last, lead the children's sign walk at ordinary pace | As the last walker steps off, every crew stake along the causeway shows Slack at once, which nobody has seen since spring | *Lifting Day* Completed; `MLD_ORDER` |

**Length targets:** MSS 35–45 min; MBA 30–40; MEP 30–40; MLL 35–45; MLW 30–40; MLD 30–40. About 3.5–4 hours across the six.

**Combat share:** MSS 0% (hearings); MBA 0%; MEP 0%; MLL ~20%; MLW 0%; MLD 0–5% (optional skirmish). Combat is never the core verb in either series (bible §7.2 structure check: MCF, MNK and MRH carry the Mire's combat-core side content).

### 0.2 Series spines

**Names Below: a seat, a book, a column.** Sorrowmere's register says who was lost, who was found and who is still asked after. This series walks the player through the register's three edges: who must be in the room (MSS), who came in from outside (MBA), and who is simply away (MEP).

| Part | What the player helps record | What stays missing | Spine line |
|---|---|---|---|
| MSS | Three small hearings, each witnessed from the stranger's seat; the oldest written hearing form, which says a hearing is not held without one "not of the households". | **Why**, forever, in the Mire (R16 seed). Ysolde: "Not found is a record too." | *Somebody from outside the lines has to be in the room.* |
| MBA | A man who came down from the high passes with a thaw column, lodged at Marshfall and went on. | Which Brede; where he went. The Mire holds his arrival, not his fate (R14, optional). | *Arrived is a record too.* |
| MEP | A living uncle the family had started to mourn. The register gains a column: **away, not lost**. | Nothing. This one ends at a table. | *Asking after someone isn't mourning them.* |

**Lanterns and Tenders: a ring, a lantern, a road.** The Chapel-Tenders keep lights for people who are out. This series moves from one family's unfinished ring, to the Tenders' oldest vigil, to the day the whole settlement walks its repaired road in daylight.

| Part | Light kept for | By whom | What the player carries |
|---|---|---|---|
| MLL | A man drowned in this spring's spate, whose family's mourning ring at Stillgrave was left half done. | The Haddow household (the Stillgrave family) and a Tender. | Moss, a mended lantern, and the line itself while the family speaks. |
| MLW | The people who went out from under the chapel roof and did not come back (R08 support; no names, no counts). | Tenders thirty years ago; now whoever the player chooses. | A rebuilt lantern, one night. |
| MLD | Everyone, including the living. Returns, births, apprentices, and the dead last. | The whole settlement. | Food, children's signs, and a decision about who walks first. |

### 0.3 Unlock graph

```
MR-M1 The Name at Sorrowmere (MR_CHANNELS, MR_NAME_RECORD)
 ├─► MSS The Stranger's Seat ──┐
 │                             ├─► MBA The Book of Arrivals ──► MEP The Empty Place
 │   MR-M3 Rowan's Crossing ───┘     (Thornfell variant lines: TWN_MIRE_HOOK, TWN Completed, TF-M5 Completed)
 │                                                             (Lowmark variant line: CN_COMPLETE)
 │
 └─► MLL The Broken Lantern Light ──┐
                                    ├─► MLW The Lantern That Would Not Go Out ──┐
     MR-M4 The Chapel ──────────────┘                                          ├─► MLD Lifting Day
                                                    MR-M2 The Banners ─────────┘   (practically always met: MR-M4 needs MR-M2)

Feeds MR-M5 Bannerline (Act III input table):
   MR_STRANGER_SEAT (MSS)  · MR_LANTERN_LINE (MLL)  · Lifting Day Completed (MLD)
Feeds MR-M3 / MR-M4 (Act II): MR_LANTERN_LINE (moss crew variant MRC-B2.6; Mabyn MCS-D1.06)
Feeds the convergence: MR_STRANGER_SEAT (R16 chip, CV-M1) · MR_ARRIVALS (R14 chip, CV-M3)
```

The two series do not gate each other. Neither gates a milestone. A player who never touches this file has a complete, authored path through MR-M1–MR-M5.

### 0.4 Flags set and read

**Region flags set** (bible §9.1; none created here):

| Flag | Values | Set by | Read by | Effect |
|---|---|---|---|---|
| `MR_STRANGER_SEAT` | bool | MSS `S06_rubbing` at `MSS-D9.01` (true on every completion path) | **MR-M5 `S08` (`MBL-D9.21`)**: Ysolde rests her hand on the seat's back and says nothing; R16 chip (CV-M1); "witness" address variants in Rootrest and Griefwatch | The seat stays unexplained (R16). |
| `MR_ARRIVALS` | named / held | MBA `S06_wall` | R14 chip (CV-M3, request: outcome only) | `named`: "Brede, down from the high passes with the thaw" on the arrivals wall. `held`: "One we hold, not yet known; down from the high passes with the thaw." |
| `MR_LANTERN_LINE` | bool | MLL `S08_ring` (true on every completion path) | **MR-M3** `MRC-B2.6` (the Stillgrave family brings the bow moss as the crew alternative); **MR-M4** `MCS-D1.06` (Mabyn); **MR-M5** circle (`MBL-B7.12`, the Stillgrave family comes up and lights the ring's lanterns) | See 0.5. |

**Completion read by a main quest:**

| Condition | Set by | Read by | Effect |
|---|---|---|---|
| *Lifting Day* (MLD) **Completed** | MLD `S06_table` | **MR-M5** circle placement and table (`MBL-B7.1a`, `MBL-B9.4`) `[CAUSEWAY]` | Oswin Garvey stands at Edris's shoulder at stone S2. Without it, he waits at the closure gate with the Reedsward crew (`MBL-B3.0`). |

**Quest-local flags other packages may read** (all optional variant lines):

| Flag | Values | Set by | Read by |
|---|---|---|---|
| `MSS_RUBBING` | taken / left | MSS | MBA opener line; Rootrest bark |
| `MSS_SEAT_LEGS` | self / crew | MSS | Rootrest bark (Elric Daw) |
| `MBA_SPINE` | self / crew | MBA | Ysolde bark |
| `MEP_HOME` | table / way | MEP | MLD (Lew walks with the returns) |
| `MLL_PLACE` | ring / garden | MLL | MLW opener; MR-M5 (request, presentation only: none needed) |
| `MLW_KEEPER` | roof / gardens / landing | MLW | MLD (where the lantern stands on the day); post-quest barks |
| `MLD_ORDER` | first / last / together | MLD | Sorrowmere barks; Act III `MBL-B9.4` (≠ first) / `MBL-B9.4b` (= first), already authored |

**Region and quest flags read here:** `MR_CHANNELS`, `MR_NAME_RECORD`, `MR_CAUSEWAY`, `MR_BANNERS`, `MR_ROWAN_TRUST`, `MR_WARDEN_RECORD`, `MNS_HOOK_ASKED`, `MBR_PINS`, `MCS_TOLD_MABYN_LANTERN`, MR-M5 Completed (MLD variant), `TWN_MIRE_HOOK`, `TWN_COMPLETE`, `thornfell.main.05_stonewake` Completed, `CN_COMPLETE`.

### 0.5 How the series feed MR-M5

Act III's input table (`Caelmor_Mire_Main_Act_III.md`, "Inputs read") is implemented exactly:

| Act III row | Value set here | What the player sees at Bannerline |
|---|---|---|
| `MR_STRANGER_SEAT` (side quest MSS), bool, read at the meal (`S08`) | **true** at MSS completion, every path | Ysolde rests her hand on the back of the stranger's seat for a moment and says nothing about it (`MBL-D9.21`). |
| `MR_LANTERN_LINE` (side quest MLL), bool, read at circle placement | **true** at MLL completion, every path; unset otherwise (read as false) | The Stillgrave family, the Haddow household, comes up last-but-one and lights a lantern at every stone, then stands at the road stone. Their eldest, **Ebba Haddow**, speaks `MBL-B7.12` ("We finished ours. We'll light yours."). Act III's speaker tag `STILLGRAVE FAMILY (eldest)` is Ebba. |
| *Lifting Day* (MLD) Completed, read at circle placement | Completion | Oswin stands at Edris's shoulder (`MBL-B7.1a`); at the meal, `MBL-B9.4`. |

**Stillgrave family role names (for Act III and Act II):** the **Haddow household** of Sorrowmere's lower ways: **Ebba Haddow** (eldest; grandmother), **Bryony Haddow** (her daughter), **Dob Haddow** (Bryony's son, about ten). In Act II's `MRC-B2.6` and Act III's `MBL-B7.12` the line is spoken by Ebba; Bryony and Dob carry. Where a package uses the role tag `STILLGRAVE FAMILY`, these are the people.

### 0.6 Shared rules for all six packages

- **Quest items: none.** The Mire's budget of four belongs to the milestones (bible §9.4). Carried things (a reed strip, a tally token on loan, a moss bundle, a lantern, a wax cake, a root-knee frame, a pot, children's signs) are **carry-state objects**. Records are **read in place**. Reward tools are named functionally.
- **Dating.** The Mire never states a calendar date or year (Act I §B14.2, Act II §B14.3). Old entries are placed by **weather run** ("the thaw after the long frost", "three rains, a frost, a thaw"); present-day entries by event ("the morning after the reading"). Ysolde writes no date numerals.
- **R08 custody.** No text here names a Memorywarden, an army, a unit or a side, or states or implies a number of dead. Tenders' and households' records say "went out", "came in", "not many"; never a figure.
- **Two holds, one name** (bible §1.1). The player sets holds side by side in dialogue (show a carry-state object, recall testimony). A banner, a dream, an impression or a strange moment counts as none.
- **Steps** use `S00_…` ids scoped to the quest. **Completion events** are the Lowmark/Thornfell set: enter-volume, inspect, interaction-complete (channel), carry-deposit, creature-defeated, dialogue-node-reached, *watch* (keep watch: advance the per-player presentation hour), *show* (use a carry-state object on an NPC).
- **No quest can fail.** Inactive / Active / Completed only. Death respawns at the quest's named safe point with step and flags intact. Logout restores the last persisted step; channels in progress are discarded, completed channel segments persist, and a dropped carry-state object returns to its source. Walking away keeps the quest Active with the resume hook named in each package. Missed moments (a dusk, a channel turn) re-offer at the next turn.
- **Channel states** (bible §9.2, N-1): every crossing a step needs is **quest-pinned** (the N-1 fallback), so nothing waits on the per-crossing schedule. Keep watch is always available.
- **Skills** (bible MD-11): each quest has one real skill hook with a light requirement written as a Gameplay Designer placeholder (`~[GD: low]`) and a **crew alternative that costs time, never access**. Woodcutting (MSS, MEP), Leatherworking (MBA, MLL), Cooking (MLW, MLD), Melee and Ranged (MLL, MLD; ranged first-class, never required).
- **Defeat** (CDR-1): every enemy is defeated at 0 HP. Earthen Echoes collapse into mud and re-form only while their place condition lasts (bible §2.6). No yields, break-off or retreat.
- **Evidence rule.** Phenomena never identify a person, settle a claim or name the dead. Combat drops nothing that advances an investigation.
- **MD-7.** No Hollowfoot appear in any of these six quests (bible MD-7: Hollowfoot appear only where the General's pulse drives them). Each package carries a one-line swap note anyway, as the brief asks.
- **MD-3 / MD-4.** Rowan never crosses at night in any of these quests. MLW reaches the chapel roof by Rowan's Chapel route at Slack by day (`[MD-3]` noted where it matters). No quest here enters the nave; MD-4 is not touched.
- **Co-op:** independent instances; shared world creatures give step credit to every participant on that step; quest-state props and NPC placement are per player (Lowmark per-player prop pattern; fallback: host state drives props, each player's own state drives dialogue).
- **Address** (bible §5.3 rule 8): people who saw the MR-M1 reading say "witness"; others say "traveller". After MSS, Rootrest's and Griefwatch's hearing keepers also say "witness".
- **Map.** Relative placement only. **MAP VERIFICATION REQUIRED** wherever geometry matters. No route or direction to another region is stated; "the high passes" and "the lowlands" are used only as people's own words for where someone came from.

### 0.7 Distinctness check

| Quest | What the player physically does | Not the same as |
|---|---|---|
| MSS | Sits a stool through three short hearings in three settlements; reads a stake, matches a scratch-mark, reads a debt tally; cuts and fits stool legs | MR-M1 (one long investigation; here three small rulings the player does not make) |
| MBA | Re-stitches a book spine; pages an archive by weather; matches a token to an entry; posts a strip | MR-M1 (matching for a living woman, across a causeway); MSS (hearings) |
| MEP | Reads a child's signs at a table; searches a ferry book; splits root-knees at a timber lot; walks a man home | MRC (Blackwater Landing as a place to wait; here as a book) |
| MLL | Gathers moss at night, re-stitches a lantern hood, holds a lit ring under Echo pressure | MR-M4 (lantern lines indoors against a hazard; here outdoors against enemies, for a family) |
| MLW | Reads a wax book, renders wax, builds a housing, keeps a flame through a wet night | MLL (a ring of lanterns; here one lantern, one night, tending not fighting) |
| MLD | Cooks for a long table, escorts children at walking pace, settles an order of walkers | MR-M1 (night causeway escort with a cart under threat; here daylight, nothing chasing) |

### 0.8 Ids and names used

Content ids (suggested; the Schema & Content Engineer owns naming): `mire.side.the_strangers_seat`, `mire.side.the_book_of_arrivals`, `mire.side.the_empty_place`, `mire.side.the_broken_lantern_light`, `mire.side.the_lantern_that_would_not_go_out`, `mire.side.lifting_day`.

New minor names [NEW] (each checked against the repository for collisions on 2026-11-08): **Wat Crake** and **Lowri Bask** (Sorrowmere ferry households, MSS); **Abel Wren** and **Hanne Lister** (Griefwatch households, MSS); **Elric Daw** (Rootrest bonecarver, keeper of Rootrest's hearing table, MSS); **Saffy Teal** and **Davy Hesk** (Rootrest, MSS); **Senna Rudd** and her grandson **Wyn Rudd** (Marshfall, MBA); **Posy**, **Annis** and **Lew Keel** (Sorrowmere, MEP); **Prue Calloway** (Chapel-Tender at Sorrowmere's memorial gardens, MLL, MLW, MLD); **Ebba**, **Bryony** and **Dob Haddow** (the Stillgrave family, MLL; see §0.5); **Corin Haddow** (named only; drowned in this spring's spate). All other speakers are bible cast or role names. *(Independent review 2026-11-09 renamed four first-name collisions with Lowmark/Thornfell NPCs and one in-batch duplicate: Jem Keel → **Lew Keel**, Pim Haddow → **Dob Haddow**, Tam Haddow → **Corin Haddow**, Ned Rudd → **Wyn Rudd** (Ned Siskin is in the companion file).)*

---

# Series one — Names Below

---

## MSS — The Stranger's Seat

### MSS.1 The quest in one paragraph

After the reading, Ysolde Haverel has three Silt hearings waiting and nobody to sit the stranger's seat at any of them. "You've done it once. You didn't fidget." A **Silt hearing** is small: the affected households, one Chapel-Tender, one Memorykeeper, and, at every table in the Mire, a stool on the visitor's side for somebody who is not anybody's cousin. The player sits three. At **Sorrowmere**, two ferry households, the Crakes and the Basks, both claim a mooring post the spate moved; the player reads the post's stake bands against the jetty book and the hearing rules on what the water says. At **Griefwatch**, a pewter spoon Mara Fenholt lifted from the Bannerline road edge is claimed by two households; the player matches its scratch-mark against two household books, and both books hold it. At **Rootrest**, Saffy Teal asks Davy Hesk to work her peat against a **lantern debt** her mother kept for rescuing his father in the flood years; the player reads the debt tally, and the hearing holds that a lantern debt is acknowledged, never inherited. At each table the player looks at the seat. They differ: new legs, old tops. Rootrest's is the oldest, its legs rotten through. The player cuts new ones from root-wood, and turning the top over to fit them, finds letters cut underneath that match the oldest **hearing form** on Rootrest's hall wall: *"Not held without one not of the households."* Nobody knows why. Ysolde writes that the player asked.

**Remember:** the warm soil in a bowl passed to you without a word. **Want next:** the archive loft Ysolde mentions, and the book of people who came in from outside (MBA).

### MSS.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| **A. One hearing; the player decides it.** | Rejected. The stranger witnesses; households decide (Silt hearing practice, MD-5). One hearing would not let the player compare seats. |
| **B. A search for the "origin" of the seat that ends in an explanation.** | Rejected. R16 must stay unexplained in the Mire (bible §8.2). |
| **C. Three small hearings in three settlements, each with one evidence task; compare the seats; mend the oldest and find the form's words** (selected). | **Selected.** Ask, compare, sit (bible §7.1), with concrete work at each table, a Woodcutting hook, and a seed that is a written form (an R16 custodian: "Mire testimony forms") rather than a phenomenon. |

| Element | Source | Status |
|---|---|---|
| Silt hearing: affected households, one Chapel-Tender, one Memorykeeper; mediates route claims, recovered property, old rescue obligations | Part 3 Mire proposal; bible MD-5 | [NEW, Part 3] |
| Lantern debt: rescue recorded as a relationship to acknowledge, never a price, never hereditary | Part 3; bible MD-5 | [NEW, Part 3] |
| The stranger's seat at every register table; nobody explains it | Bible §6.1 MR-M1; `MNS-D1.20` | [NEW] |
| "A Mire hearing form that requires a stranger's presence" (R16 seed; custodian "Mire testimony forms") | Revelation Ledger R16 | [APPROVED — FT-01 seed] |
| Soil before testimony | Bible MME02 | [NEW] |
| Griefwatch vigil hall; Rootrest root-sheltered homes, bonecarvers | Dossier §VII; bible §4.2 | [CANON] |
| The three hearings, the seats' legs, the Rootrest form board, all named households | This package | [NEW] |

### MSS.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `mire.side.the_strangers_seat` |
| Series | *Names Below*, part 1 of 3 |
| Type | Memory/lore |
| Unlock | MR-M1 Completed. Offered by Ysolde at the register room door (`MSS-D1`). With `MNS_HOOK_ASKED`: Ysolde points at the player's not-found strip still on the index board (`MSS-D1.03`). |
| Length | 35–45 minutes |
| Combat share | 0% |
| Skills | **Woodcutting ~[GD: low]**: cut and shape two root-wood stool legs at Rootrest. Crew alternative: Elric Daw's apprentice cuts them overnight (keep watch to morning). |
| Choice | Whether Ysolde takes a rubbing of the seat's underside for the register (`MSS_RUBBING`: taken / left). The hearings' outcomes belong to the households. |
| Outputs | **`MR_STRANGER_SEAT` = true** (every completion path); `MSS_RUBBING`; `MSS_SEAT_LEGS`; "witness" address at Griefwatch and Rootrest |
| **Anchor** | Memorykeepers (Ysolde); the Silt hearing; Sorrowmere ferry households, Griefwatch households, Rootrest households. |
| **World-truth row** | H07 (seed only: a custom of witness older than anyone's memory). |
| **Revelation role** | **Plants R16** (a hearing that needs a stranger). Never explained in the Mire. |
| **Recurring evidence** | None required. The **Rootrest hearing form** (painted board on Rootrest's hall wall; custodian Elric Daw) and the letters under the Rootrest seat stay in place and can be re-inspected; with `MSS_RUBBING = taken`, a reed rubbing is pinned in Sorrowmere's register room. These are R16 custodians for CV-M1 ("Mire testimony forms"). |
| **State compliance** | Inactive → Active on `MSS-D1` accept; Completed on `MSS-D9` end. Hearings cannot be lost: each rules whatever the player brings; a player who brings nothing hears the hearing rule on testimony alone. `MR_STRANGER_SEAT` true on every path. Resume hook: Ysolde at the register room (`MSS-B1.02`). |
| **Combat compliance** | None. No enemy appears. |

### MSS.4 The places

**MAP VERIFICATION REQUIRED** for every placement. Griefwatch sits at the foot of Bannerline Ridge; Rootrest on firmer ground beyond Marshfall (bible §4.2 route order).

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Sorrowmere register room** (MP01) | Offer; hearing 1; close | The register table; the stranger's seat (MR-M1 prop `MNS-I1`: carved top worn pale, legs newer than the top). A soil bowl at the head of the table. The index boards by the door with their reed strips. |
| **A2. Sorrowmere jetty** | Hearing 1 evidence | Two mooring posts: one where the jetty book says the Crake post stood, one where it stands now, a boat's length down the channel. The old post is a stub with painted bands; the spate shifted it. A channel stake beside it. Children's depth-band game chalked on the boards (MME10). |
| **B. Griefwatch vigil hall** (MP03) | Hearing 2 | The long table and cook-hearth (as in MR-M5); a smaller hearing table at the hearth end with its own stranger's seat: a three-legged stool, one leg a splinted spear shaft. A bell rope through the roof. |
| **B2. Two Griefwatch houses** | Hearing 2 evidence | The Wren house: household book in a box under the bed. The Lister house: household book on a shelf over the door with a row of wooden spoons. |
| **C. Rootrest hall** (MP04) | Hearing 3; the oldest seat; Woodcutting | A hall half under the roots of an old black-rooted tree. The hearing table is a slab of root. The stranger's seat: a heavy, dark top on legs rotted almost through, propped on a peat block. On the wall, the **hearing form board**: painted lines, repainted many times, the top line older and smaller than the rest. Elric Daw's bench of bone needles and markers in the corner. |
| **C2. Root-wood pile** | Woodcutting | Reclaimed root-knees stacked under the eaves (dead roots cut back from paths). A chopping block and a drawknife. |
| **C3. The Teal peat stack** | Hearing 3 evidence | Saffy Teal's half-cut stack. On the door-post of her house, a **lantern hook** and under it a column of small cut notches: the debt tally. |

### MSS.5 Player-facing sequence

**Beat 0 — Three hearings (`S00_offer`).** *Objective: Ask Ysolde about the hearings.* `MSS-D1`. Three Silt hearings waiting; each needs the seat sat. "You don't decide anything. You sit, you listen, you say back what was decided so everybody heard it the same."

**Beat 1 — The mooring (`S01_mooring`).** *Objective: Sit the hearing at the register room.* The player sits (interaction *Sit the seat*). `MSS-D2`: Wat Crake and Lowri Bask, Ysolde, a Chapel-Tender (Prue Calloway). Everyone touches the soil bowl before speaking (MME02); the bowl is not offered to the player. Wat: the post is his, it moved. Lowri: it's in front of her door now. The Tender asks for "what the water says". **Evidence task:** at the jetty, inspect the **old stub's bands** and the **channel stake** (with `MR_CHANNELS`, the inspect reads which band the stub was set at: ochre, the Slack line, where a mooring belongs) and read the **jetty book** (three entries; the post's setting, "set at the ochre, Crake's"). Return and *show* (recall in dialogue). The hearing rules (`MSS-D2.30`): the post is re-set at the ochre line on the new channel, which falls between both doors; both tie there, Crake first in the morning. The player says it back (`MSS-D2.40`). Inspect the seat (required): the Sorrowmere seat (`MSS-I1.01`).

**Beat 2 — The spoon (`S02_spoon`).** *Objective: Sit the hearing at Griefwatch.* Travel. `MSS-D3` at the vigil hall: Abel Wren and Hanne Lister, a Griefwatch Memorykeeper, a Tender. Mara Fenholt brought the spoon up from the Bannerline road edge (she says where, and that she dug no deeper than the ground offered). It has a scratch-mark on the handle: a ring with a stroke. Both households say it is theirs. **Evidence task:** read both household books (inspects in two houses). The Wren book draws a ring with a stroke beside "Grandmother's spoons, six"; the Lister book draws the same mark beside "Spoons from the Wren wedding, given, two". Both books hold it: the spoon was a wedding gift between the houses. The hearing (`MSS-D3.30`): the spoon is both houses'; it hangs in the vigil hall on the spoon nail and goes to whichever house is feeding the bell-keeper that week. The player says it back. Inspect the seat (required, `MSS-I1.02`: spear-shaft splint).

**Beat 3 — The lantern debt (`S03_debt`).** *Objective: Sit the hearing at Rootrest.* Travel. `MSS-D4` in the Rootrest hall: Saffy Teal, Davy Hesk, Elric Daw (keeps the hall's table), a Tender, a Rootrest Memorykeeper. **The seat is not fit to sit** (rotted legs). Elric: "Sit on the peat block then. It's held worse." The hearing opens anyway (beat 4 happens before the ruling). **Evidence task:** at the Teal house, inspect the **debt tally** (notches under a lantern hook: one cut each year on the night of the rescue, by Saffy's mother; the last few cuts in a different, newer hand: Saffy's) and the **peat stack** (half cut). The point lands in the objects: the debt was kept as a night's light, and Saffy has started cutting notches herself.

**Beat 4 — The oldest seat (`S04_legs`).** *Objective: Make new legs for Rootrest's seat.* Elric shows the player the root-wood pile. **Woodcutting ~[GD: low]**: select two straight root-knees (inspect: one is split, harmless), split and shape on the block (two 4 s channels each; segments persist). **Crew alternative:** Elric's apprentice cuts them overnight (`MSS-D5.05`; keep watch to morning; sets `MSS_SEAT_LEGS = crew`). Fitting the legs needs the top turned over (interaction *Turn the seat over*): underneath, letters cut and blacked with age (`MSS-I1.03`). The player can compare them to the **hearing form board** on the wall (inspect; required): the board's top line, smaller and older than the rest, says the same thing (`MSS-I2.01`). Fit the legs (one 3 s channel). Elric: "Nobody's turned that over in my time."

**Beat 5 — The ruling (`S05_ruling`).** *Objective: Sit the hearing on the mended seat.* The player sits. `MSS-D6`. Everyone touches the soil bowl. **The strange moment** (MSS.7): the bowl is passed to the player. The ruling: a lantern debt is acknowledged, never inherited. Davy will light the lantern on Saffy's hook on the night of the rescue each year for as long as he chooses to; he owes no peat. Saffy will cut no more notches. Davy, unasked, says he'll help with the stack this once "because it's wet, not because of the hook". The player says it back.

**Beat 6 — The rubbing (`S06_rubbing`).** *Objective: Tell Ysolde what the seat says.* Back at Sorrowmere, `MSS-D7`. Ysolde listens, writes the three rulings into the hearing book, then the form's words. She asks whether she should send for a rubbing of the seat's underside for the register room. Choice (`MSS_RUBBING`): **taken** (Ysolde's apprentice goes to Rootrest; the rubbing is pinned beside the register's own seat) or **left** (the words stay under the seat at Rootrest where they were cut; Ysolde writes where they are).

**Beat 7 — Not found (`S07_record`, folded into `S06` close).** Ysolde writes a final strip: *"Why the seat: asked by the witness. Not found."* and pegs it on the index board. Quest Completed (`MSS-D9`). Sets `MR_STRANGER_SEAT`.

### MSS.6 Encounters

None. MSS is a talk-and-work quest. Travel between settlements uses the ordinary routes and their ambient wildlife.

**MD-7 swap note:** no Hollowfoot content. Nothing to swap.

### MSS.7 The strange moment: the warm soil (Beat 5)

| Time | Element | Spec |
|---|---|---|
| 0 s | **The bowl goes round** | Each person at the Rootrest table touches the soil bowl before they speak (MME02). It has not been offered to the player at either earlier hearing. |
| 0–4 s | **Passed** | Elric, last before the ruling, touches it and then, without looking up, slides it across the root slab to the stranger's seat. Prompt: *Touch the soil* / *Leave it*. |
| Touch | **Warm** | The soil is warm, as if it had been sitting in sun. The hall is cold; the bowl is clay; there is no fire near it. Inner voice: *"Warm. Like a hand had just been in it."* |
| After | **Nothing** | Nobody remarks on it. If the player asks (`MSS-D6.15`), Elric: "Habit." (beat) "I've never passed it over before. Habit too, maybe." |
| Leave it | — | The ruling proceeds. No line changes. |
| UI | | No objective update until the ruling begins. No music. |
| What it means | | Nothing that can be proved. It is one of the small Mire moments that is never explained. It is not a hold and does not affect the ruling. |

### MSS.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Ask Ysolde about the hearings. | `MSS-D1` end with accept | Yes (Inactive → Active) |
| `S01_mooring` | Sit the hearing at the register room. / Read the stub, the stake and the jetty book. / Tell the hearing what the water says. | Sit + `stub` + `stake` + `jetty_book` inspects + `MSS-D2.40` end + seat inspect `MSS-I1.01` | Yes |
| `S02_spoon` | Sit the hearing at Griefwatch. / Read the Wren and Lister books. | Sit + 2 book inspects + `MSS-D3.40` end + seat inspect `MSS-I1.02` | Yes (any order with S01) |
| `S03_debt` | Sit the hearing at Rootrest. / Read the debt tally. | `MSS-D4` end + `tally` + `stack` inspects | Yes |
| `S04_legs` | Make new legs for Rootrest's seat. | 2 × leg (2 × `shape_leg` segments each) **or** keep watch (crew) + `turn_seat` + `MSS-I1.03` + `MSS-I2.01` + `fit_legs` | Yes |
| `S05_ruling` | Sit the hearing on the mended seat. | Sit + `MSS-D6.40` end | Yes |
| `S06_rubbing` | Tell Ysolde what the seat says. | `MSS-D7` choice → `MSS-D9` end | Yes (→ Completed) |

### MSS.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `MSS_SOIL_TOUCHED` | Strange moment, *Touch* | `MSS-D7.04` (optional line) |
| `MSS_SEAT_LEGS` = self / crew | `S04` | `MSS-B3.02` |
| `MSS_RUBBING` = taken / left | `MSS-D7` | MBA opener (`MBA-D1.04`); Rootrest bark |
| **`MR_STRANGER_SEAT` = true** | `MSS-D9.01` (every path) | MR-M5 `MBL-D9.21`; CV-M1 R16 chip; "witness" address at Griefwatch and Rootrest |

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Taken** — *"Take a rubbing. Put it by our seat."* | Ysolde's apprentice rubs the underside next visit; the rubbing hangs in a reed frame beside Sorrowmere's seat (inspect `MSS-I2.03`). | Elric minds: the words were Rootrest's and now they hang in Sorrowmere. He says so once (`MSS-B3.03`). | Anyone at the register room can read the form's words. The rubbing is a second custodian beside the seat itself (CV-M1 can find either). |
| **Left** — *"Leave it under the seat. Write where it is."* | Ysolde writes "Rootrest's seat, underneath" in the hearing book. | Only someone who turns Rootrest's seat over will read it. | Elric: "Right where it was cut." The words are found by whoever looks (CV-M1 custodian: the seat and the form board, guaranteed in both values). |

Both values set `MR_STRANGER_SEAT = true`. Neither explains the seat.

### MSS.10 Rewards, failure, co-op

| Reward | Type | Notes |
|---|---|---|
| **"Witness" at three tables** | Standing (address) | Griefwatch's and Rootrest's hearing keepers address the player as "witness". |
| **A seat at Rootrest's hall fire** | Access | Rest point at Rootrest hall (Elric: "Sit on your own legs."). |
| Small payment | Currency | A hearing pays the stranger "for their day". Economy tuning [GD]. |
| Skill XP | Actions only [GD] | Woodcutting. |
| *The Book of Arrivals* | Story | Unlocks when MR-M3 is also Completed (`MSS-D9.04`: Ysolde mentions the archive loft). |

| Situation | Handling |
|---|---|
| Brings no evidence to a hearing | The hearing waits ("We'll sit till you're back"); the evidence inspects stay open. There is no way to lose a hearing. |
| Wrong recall in dialogue | The NPC says what the book actually said ("That's not what it says, look again"); options repeat. |
| No Woodcutting | Crew alternative (overnight). |
| Visits Rootrest first | `S03`–`S05` can run before `S01`/`S02`; `S06` needs all three. |
| Walking away | Stays Active. Resume: Ysolde (`MSS-B1.02`), or the keeper of whichever hearing is open. |
| Fail state | None. |
| Co-op | Each player sits their own seat (each hearing places a second stool for a partner: "Two strangers. That's allowed."; presentation only). Rulings and the rubbing are per player; the Rootrest seat's legs prop follows each player's own step (fallback: host's). |

### MSS.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| *Sit the seat* interaction | Systems | Seated state at a prop; dialogue opens from it. Reused in MR-M1. |
| *Turn the seat over* | Systems / Art | Prop swap (upright / upturned) with an inspect point. **Fallback:** inspect text on the upright seat. |
| Channel segments with persistence | Systems | Lowmark convention (shape leg, fit legs). |
| Soil bowl pass (strange moment) | NPC / Systems | One scripted NPC push of a prop to the player's position; touch interaction with inspect. **Fallback:** dialogue prompt "Elric slides the bowl to you." |
| Per-player hearing props | Systems | Mooring post, spoon nail, seat legs (Lowmark per-player prop pattern). |
| Woodcutting interaction on root-knees | Systems / economy | Existing Woodcutting gather; root-knee is a reclaimed-wood node (bible MD-11). No new item: the legs are carry-state. |

**Mystery ledger.**

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Why every table keeps a stranger's seat** | A survival of the prewar Crossing Concord's custom of mutual witness (R16, FT-01). | "It's always been there." "Bad luck to take it out." | The seats; the Rootrest form's top line; the letters under the oldest seat. | A Memorywarden rite; a superstition about the dead. | **Yes. Forever in the Mire.** | CV-M1 (R16). |

**Open decisions.** (1) The form's wording is [NEW]; CV-M1's owner may want it to echo Lowmark's crossing oath phrase and the Thornfell *Witness at the Gate* call; it is kept short so it can be matched without rewriting. (2) MAP VERIFICATION REQUIRED for the Sorrowmere jetty's two posts.

| Review finding | Revision |
|---|---|
| First draft let the player rule each hearing. | The households rule; the player gathers, sits and says it back (Silt hearing practice). |
| The lantern-debt ruling risked reading as a law with enforcement. | It is a hearing's ruling that depends on cooperation; Davy's acknowledgement is voluntary (Part 3 limit). |
| The warm soil risked being a sign that the seat "works". | Nobody comments; it affects nothing; it is not a hold. |
| The spoon at Griefwatch came from the Bannerline road edge; risked implying a battle find. | Mara's line places it at the road edge "with the ordinary rubbish"; a wedding spoon, nothing older than the households. |

### MSS.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Ysolde Haverel** | The register, the hearing book, the forms. | Why the seat exists (R16). | Precise, kind, will not round a number. |
| **Prue Calloway** [NEW], Chapel-Tender | Tender practice at hearings: "what the water says". | — | Brisk, pious, carries a wick-knife. |
| **Wat Crake / Lowri Bask** [NEW] | Their doors, their boats. | — | Wat aggrieved; Lowri tired. |
| **Abel Wren / Hanne Lister** [NEW] | Their own books. | That both are right. | Abel stubborn; Hanne embarrassed to be here. |
| **Mara Fenholt** [CANON] | Where the spoon lay. | Whose it is. | Few words; never digs deeper than the ground offers. |
| **Elric Daw** [NEW], Rootrest bonecarver | The hall, the table, the form board's age. | What the top line means. | Slow, dry, kind with his hands. |
| **Saffy Teal** [NEW] | Her mother's tally. | That she is making it a price. | Proud, frightened of winter. |
| **Davy Hesk** [NEW] | That his father was pulled out of the flood. | — | Young, stiff, decent. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| MSS-B1.01 | Ysolde | Available, player near register room | *"Three hearings and an empty stool at each. I could do with a stranger."* |
| MSS-B1.02 | Ysolde | Active, returns | *"The tables wait. They're good at it. Same as this room."* |
| MSS-B2.01 | Wat Crake | After `S01` | *"Crake ties first in the morning. Written. Heard."* |
| MSS-B2.02 | Lowri Bask | After `S01` | *"His boat's under my window all night. Still. Better than the channel."* |
| MSS-B2.03 | Griefwatch bell-keeper | After `S02`, `MR_STRANGER_SEAT` | *"Witness. Spoon's on the nail. Whoever's feeding me this week gets it."* |
| MSS-B3.01 | Elric Daw | After completion | *"Sit, witness. Your own legs."* |
| MSS-B3.02 | Elric Daw | `MSS_SEAT_LEGS = crew` | *"My lad cut the legs. You turned it over. Somebody had to do both."* |
| MSS-B3.03 | Elric Daw | `MSS_RUBBING = taken` | *"Our words are on a wall in Sorrowmere. Hope they're dusting them."* |
| MSS-B3.04 | Davy Hesk | Completed | *"Lit the hook. Saffy brought bread out. Nobody said debt."* |

#### Nodes

```
MSS-D1 (register room door; S00)
MSS-D1.01 YSOLDE: (a stack of hearing slips under her arm) "Witness. You sat the seat once. You didn't fidget."
MSS-D1.02 YSOLDE: "I've three Silt hearings and nobody for the stool. Here, Griefwatch, Rootrest."
MSS-D1.03 [MNS_HOOK_ASKED] YSOLDE: (nodding at the index board) "Your not-found strip's still up. People stop and read it. That's what it's for."
MSS-D1.04 YSOLDE: "You don't decide anything. You sit, you listen. Then you say back what was decided, so everybody heard it the same."
  > "I'll sit them."                                       → MSS-D1.10
  > "What's a Silt hearing?"                               → MSS-D1.20
  > "Why does it need a stranger?"                         → MSS-D1.30
  > "Not now."                                             → MSS-D1.40
MSS-D1.10 YSOLDE: "Good. Mooring first, it's here. Then a spoon, then a lantern debt. Small things." (beat) "Small things are most of it."
      {quest Active; event: S00_offer}
MSS-D1.20 YSOLDE: "The households it touches. One Tender. One of us. We sit till it's settled or till we agree it won't be today."   → MSS-D1 options
MSS-D1.30 YSOLDE: "I don't know. Every table I've sat at has the stool. I've asked. Nobody's ever said." (beat) "Sit three. Look at the stools. Tell me if you find out."   → MSS-D1 options
MSS-D1.40 YSOLDE: "They'll keep. The Crakes won't, but the hearing will."   {quest stays Inactive}
```

```
MSS-D2 (register room; S01)
MSS-D2.01 (Everyone at the table touches the soil bowl in turn before speaking. It is not offered to the player.)
MSS-D2.02 WAT: "Spate shifted the post a boat's length down. It's mine. It was mine before the spate and it's mine after."
MSS-D2.03 LOWRI: "It's in front of my door now. His boat knocks all night."
MSS-D2.04 PRUE: "Then let's hear what the water says. Witness, the stub and the book are on the jetty."   {objective: read the stub, the stake and the jetty book}
MSS-D2.20 (return) YSOLDE: "Witness. What did you find?"
  > [stub + stake read, MR_CHANNELS] "The old stub was set at the ochre band. Slack line."   → MSS-D2.21
  > [jetty_book] "The jetty book says 'set at the ochre, Crake's.'"                          → MSS-D2.22
  > [both said] "That's all of it."                                                          → MSS-D2.30
MSS-D2.21 PRUE: "Ochre. Where a mooring belongs. Not where a door is."   → MSS-D2.20
MSS-D2.22 WAT: "There."  LOWRI: "It says ochre. It doesn't say outside your door."   → MSS-D2.20
MSS-D2.30 YSOLDE: (writes) "Post re-set at the ochre on the new channel. That's halfway between your doors. Both tie. Crake first in the morning, Bask first at dusk."
MSS-D2.31 WAT: "...First in the morning."  LOWRI: "Fine."
MSS-D2.40 YSOLDE: "Witness. Say it back."
  > "The post goes at the ochre, between both doors. Crake ties first in the morning, Bask first at dusk."   → MSS-D2.41
MSS-D2.41 YSOLDE: "Heard." (beat) "That's the job. Griefwatch next."   {event: S01 dialogue condition}
```

```
MSS-D3 (Griefwatch vigil hall; S02)
MSS-D3.01 [MR_STRANGER_SEAT unset] GRIEFWATCH MEMORYKEEPER: "Ysolde's stranger. Sit. The stool's got a spear for a leg. It holds."
MSS-D3.02 MARA: (sets a pewter spoon on the table) "Bannerline road edge. In the ditch with the ordinary rubbish. I didn't dig under it."
MSS-D3.03 ABEL: "Wren spoon. Ring and a stroke. My grandmother's mark."
MSS-D3.04 HANNE: (quietly) "It's ours. I'm sorry, Abel. It's in our book."
MSS-D3.05 TENDER: "Two books. Witness, read both."   {objective: read the Wren and Lister books}
MSS-D3.20 (return) GRIEFWATCH MEMORYKEEPER: "Well?"
  > [both books] "The Wren book has six of your grandmother's spoons with the mark. The Lister book has two with the same mark, 'from the Wren wedding, given'."   → MSS-D3.21
MSS-D3.21 ABEL: (long pause) "...My aunt's wedding. To a Lister." (beat) "I'd forgotten we were related. We don't speak."
MSS-D3.22 HANNE: "We don't."
MSS-D3.30 GRIEFWATCH MEMORYKEEPER: "Both books hold it. It's both houses'. It hangs on the nail here. Whoever's feeding the bell-keeper that week takes it home."
MSS-D3.40 GRIEFWATCH MEMORYKEEPER: "Witness."
  > "It's both houses'. It hangs here and goes home with whoever feeds the bell-keeper."   → MSS-D3.41
MSS-D3.41 ABEL: "Heard."  HANNE: "Heard." (they do not look at each other; they leave by the same door)   {event: S02 dialogue condition}
```

```
MSS-D4 (Rootrest hall; S03)
MSS-D4.01 ELRIC: (looking at the stool's legs, then at the player) "You're the stranger. That seat won't have you. Sit on the peat block. It's held worse."
MSS-D4.02 SAFFY: "My mother pulled his father out of the flood. Lantern on the hook every year since, the night of it. Her notches. Now he can cut my peat."
MSS-D4.03 DAVY: "I wasn't born. I'll say thank you every year till I die. I won't be owned for it."
MSS-D4.04 ROOTREST MEMORYKEEPER: "Witness, the tally's on her door-post. Read it before we say anything."
MSS-D4.05 ELRIC: "And while you're up, I'd like that seat stood properly. It's older than any of us. Nobody's let it go."   {objective: read the debt tally; make new legs for Rootrest's seat}
```

```
MSS-D5 (Elric at the root pile; S04)
MSS-D5.01 ELRIC: "Root-knee. Dead roots off the paths. Straight ones. Split along the grain or it'll split along you."
  > "I'll cut them."                                       → MSS-D5.02
  > "Can someone who knows what they're doing cut them?"   → MSS-D5.05
MSS-D5.02 ELRIC: "Good. Block's there. Drawknife's sharp; I don't lend blunt things."   {Woodcutting interaction; MSS_SEAT_LEGS = self}
MSS-D5.05 ELRIC: "My lad. Tomorrow. He's slow and he's never wrong." {keep watch to morning; MSS_SEAT_LEGS = crew}
MSS-D5.10 (legs ready) ELRIC: "Turn it over. Gently, it's older than the hall."   {interaction: turn_seat}
MSS-D5.11 (after MSS-I1.03) ELRIC: (bending to look) "Nobody's turned that over in my time." (beat) "Read the board. Top line."
MSS-D5.12 (after MSS-I2.01) ELRIC: "Same words. Painted over and over and nobody's changed that line. I'd thought it was a prayer."
  > "What does it mean?"                                   → MSS-D5.13
  > "Let's fit the legs."                                  → MSS-D5.14
MSS-D5.13 ELRIC: "Means what it says. Why it says it, I couldn't tell you. Neither could my teacher."   → MSS-D5.14
MSS-D5.14 ELRIC: "Fit them. Then sit on it and we'll have the hearing properly."
```

```
MSS-D6 (Rootrest hall; S05)
MSS-D6.01 (Everyone touches the soil bowl. Elric, last, slides it across the slab to the stranger's seat.)   {strange moment; prompt: touch / leave}
MSS-D6.15 [MSS_SOIL_TOUCHED; optional] "The soil's warm."
MSS-D6.16 ELRIC: "Habit." (beat) "I've never passed it over before. Habit too, maybe."
MSS-D6.20 ROOTREST MEMORYKEEPER: "Witness. The tally."
  > [tally read] "One notch a year under the hook, the night of the flood. The last few are in a newer hand."   → MSS-D6.21
MSS-D6.21 SAFFY: (after a while) "Mine. Since Mother died. I didn't want the hook to go bare."
MSS-D6.22 TENDER: "That's a light. It isn't a price."
MSS-D6.30 ROOTREST MEMORYKEEPER: "A lantern debt is said. It isn't owed on. It doesn't go down to children. Davy lights the hook the night of it, while he chooses to. Nobody cuts notches."
MSS-D6.31 DAVY: "I'll light it." (beat) "And I'll help with the stack this once. Because it's wet. Not because of the hook."
MSS-D6.32 SAFFY: "...Because it's wet."
MSS-D6.40 ELRIC: "Witness."
  > "A lantern debt is said, never owed. Davy lights the hook while he chooses. No more notches."   → MSS-D6.41
MSS-D6.41 ELRIC: "Heard. Sat on proper legs and all."   {event: S05}
```

```
MSS-D7 (register room; S06)
MSS-D7.01 YSOLDE: "Sit. Eat that, it's yesterday's but it's bread. Then tell it."
MSS-D7.02 (the player recalls the three rulings; Ysolde writes each into the hearing book)
MSS-D7.03 YSOLDE: "And the seats?"
  > "New legs on old tops, all three. Rootrest's is oldest. Underneath it, cut: 'Not held without one not of the households.' Same as the top line of their form board."   → MSS-D7.05
MSS-D7.04 [MSS_SOIL_TOUCHED] (optional) "Elric passed me the soil bowl. It was warm."  YSOLDE: "I'll write that he passed it. I won't write warm. That's yours."   → MSS-D7.05
MSS-D7.05 YSOLDE: (stops writing) "Not held without." (beat) "So it was always a rule. Not a habit."
MSS-D7.06 YSOLDE: "Still doesn't say why." (beat) "Should I send for a rubbing? Put it by our own seat?"
  > "Take a rubbing. Put it by our seat."                       → MSS-D7.10
  > "Leave it under the seat. Write where it is."               → MSS-D7.20
MSS-D7.10 YSOLDE: "My apprentice goes on the next dry morning. Elric will mind. He'll say so, and then he'll make tea."   {set MSS_RUBBING = taken}   → MSS-D9.01
MSS-D7.20 YSOLDE: (writes) "'Rootrest's seat. Underneath.' There. Anyone who wants it knows where to bend down."   {set MSS_RUBBING = left}   → MSS-D9.01
```

```
MSS-D9 (close)
MSS-D9.01 YSOLDE: (writes a reed strip, pegs it on the index board) "'Why the seat: asked by the witness. Not found.'"   {set MR_STRANGER_SEAT}
MSS-D9.02 YSOLDE: "Not found is a record too. Somebody, someday, will read that you asked."
MSS-D9.03 YSOLDE: "Three tables. Three new pairs of legs on old seats. People keep fixing what they can't explain. I like that about us."
MSS-D9.04 [MR-M3 Completed] YSOLDE: "There's a book in the loft I've been meaning to open. People who came in from outside. You're good at outside."
      {event: S06 → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| MSS-I1.01 | Sorrowmere seat | *"Carved top, worn pale. The legs are newer than the top. Someone has replaced them more than once."* |
| MSS-I1.02 | Griefwatch seat | *"Three legs. One is a spear shaft, cut down and splinted. The top is older than the shaft by a long way."* |
| MSS-I1.03 | Rootrest seat, underside | *"Cut into the wood and blacked with age, in letters older than any on the hall's boards: NOT HELD WITHOUT ONE NOT OF THE HOUSEHOLDS."* |
| MSS-I2.01 | Rootrest hearing form board | *"Lines painted and repainted: who sits, who speaks, the soil before testimony. The top line is smaller and older than the rest, and nobody has changed it: 'Not held without one not of the households.'"* |
| MSS-I2.02 | Old mooring stub | *"Painted bands, faded. The stub was set with its foot at the ochre band."* With `MR_CHANNELS`: *"Ochre: Slack. Where a mooring belongs."* |
| MSS-I2.03 | Rubbing (taken) | *"A reed-paper rubbing in a frame beside the seat. The letters come up white: NOT HELD WITHOUT ONE NOT OF THE HOUSEHOLDS."* |
| MSS-I3.01 | Jetty book | *"'Crake post. Set at the ochre, Crake's.' Below it, in a newer hand: 'Spate. Post gone down the channel.'"* |
| MSS-I3.02 | Wren household book | *"'Grandmother's spoons, six.' A ring with a stroke drawn beside it."* |
| MSS-I3.03 | Lister household book | *"'Spoons from the Wren wedding, given, two.' The same ring and stroke."* |
| MSS-I3.04 | Debt tally | *"A lantern hook. Under it, a column of small notches, one a year. The last few are cut deeper, by a different knife."* |

---

## MBA — The Book of Arrivals

### MBA.1 The quest in one paragraph

**Senna Rudd** of Marshfall brings Ysolde a carrier's **tally token**: a short notched stick on a thong, tied with a double knot. Her mother took in "a man who came down from the high passes with the thaw" in the war's last years. He lodged, carried peat, said little, and one spring went on, leaving the token on her mother's peg. Senna is old now and wants him on Sorrowmere's **arrivals wall**, the reed strips for people who came into Mire care from outside. Ysolde needs his **care entry**: everyone received into care was written in the **Book of Arrivals**, which sits in the archive loft with its spine split and its pages stuck with damp. The player re-stitches the spine (Leatherworking), then searches it. The book is not dated; it is grouped by weather, and Senna's mother remembered the spring "the ferry way froze". Three entries fit the season. The player matches them against the token and against the **Rudd household book** at Marshfall. One holds: *"Received: a man, down from the high passes with a thaw column. Gave his name as Brede. Hands raw from carrying. Care: Rudd, Marshfall."* Two holds, one name. But "Brede" is a family name, and the household book only ever calls him "the high-pass man". Ysolde asks the witness what the strip should say.

**Remember:** a knot nobody had untied for thirty years refusing to lie straight. **Want next:** the arrivals wall filling; and, for a player who has walked the high passes, the thought of a slip renewed every spring somewhere else.

### MBA.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| **A. The Mire entry settles the Thornfell Brede case.** | Rejected. MD-14: the Mire entry adds a record and settles nothing; Thornfell's resolution stands. |
| **B. Only playable with Thornfell flags.** | Rejected. The Mire end of R14 is optional and must stand alone; Thornfell content gives variant lines only. |
| **C. A Mire household's object → a damaged book → search by weather → two holds → a strip whose wording is the choice** (selected). | **Selected.** Self-contained for a Mire-only player; richer for a Thornfell player, never a gate. |

| Element | Source | Status |
|---|---|---|
| Stranded refugees reached the Mire (R14 Mire end), optional and exempt | Revelation Ledger R14; bible §8.1 | [APPROVED — owner Register series] |
| A Brede "down from the high passes with a thaw column"; does not settle which Brede | Bible MD-14 | [NEW] |
| Register of the Unreturned: Book of Arrivals entry + tally token (Mire holds); TF-M3 roster / TWN slip / TF-M5 rubbing (other region) | Bible §7.6 | [NEW] |
| Sig Brede's family slip, his tally stick with a double knot (Hushfold), "Other places keep books" | Thornfell TWN (`TWN_MIRE_HOOK`) | [NEW, Thornfell package] |
| Two holds, one name | Bible §1.1 | [NEW] |
| Senna Rudd, the arrivals wall, the archive loft, the weather grouping, the token | This package | [NEW] |

### MBA.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `mire.side.the_book_of_arrivals` |
| Series | *Names Below*, part 2 of 3 |
| Type | Memory/lore (Register of the Unreturned, Mire case) |
| Unlock | MSS **and** MR-M3 Completed. Senna Rudd is at the register room with Ysolde on the player's next visit (`MBA-D1`). |
| Length | 30–40 minutes |
| Combat share | 0% |
| Skills | **Leatherworking ~[GD: low]**: re-stitch the Book of Arrivals' split leather spine (repair of imported leather, bible MD-11). Crew alternative: Ysolde's apprentice re-stitches it overnight (keep watch to morning). |
| Choice | What the arrivals strip says (`MR_ARRIVALS`: named / held). |
| Outputs | **`MR_ARRIVALS`**; `MBA_SPINE`; the arrivals wall readable |
| **Anchor** | Names Below (Ysolde); the Marshfall host household (Rudd). |
| **World-truth row** | H16 (Thornfell's sealings stranded people; Mire end only as an arrival), H23 (recovery: uncertain names). |
| **Revelation role** | **Owns the Mire end of R14** (optional, exempt from the guaranteed-path rule). |
| **Recurring evidence** | **Tally token** (Rudd household; carry-state loan, returned) + **care entry** (Book of Arrivals; archive loft, read in place) + **Rudd household book** (Marshfall, read in place). With Thornfell content: TWN's tally stick and Hushfold slip, or the TF-M5 closure rubbing, recalled in dialogue as **the other region's hold** (never a Mire hold; never settles which Brede). |
| **State compliance** | Inactive → Active on `MBA-D1` accept; Completed on `MBA-D6` end. No fail. `MR_ARRIVALS` named or held; both are honest. Resume hook: Ysolde (`MBA-B1.02`). |
| **Combat compliance** | None. |

### MBA.4 The places

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Register room** (MP01) | Offer; the choice | The **arrivals wall**: a side wall of reed strips on pegs, each "came in" and from where in a person's own words ("off the Standards road", "up from the fowling meres", "from away"). Some strips say only *"One we hold."* |
| **B. Archive loft** | Spine repair; search | Up a ladder over the register room. Chests of household copies, reed bundles, a damp smell. The **Book of Arrivals**: a thick ledger in imported leather, its spine split, its middle pages stuck. A work bench with an awl, waxed thread and a pot of glue. A window that looks out over the raised ways. |
| **C. Marshfall, the Rudd house** (MP02) | Household book | A stilt house by the peat yards. **The peg** by the door where the token hung for thirty years: a lighter patch on the wall around it. The Rudd household book in a tin on the shelf. |

**MAP VERIFICATION REQUIRED** for the Rudd house; reached by the causeway (reset after MR-M2).

### MBA.5 Player-facing sequence

**Beat 0 — The token (`S00_offer`).** *Objective: Hear Senna out.* `MBA-D1`. Senna, Ysolde, the token on the table. Inspect the token (required, `MBA-I1.01`; with `TWN_COMPLETE`, variant `MBA-I1.02`). Senna gives her mother's words: "the thaw after the long frost, the spring the ferry way froze". Ysolde: the care entry will be in the Book of Arrivals, "if the book will open". Senna lends the token (carry-state; returns to her at the end).

**Beat 1 — The spine (`S01_spine`).** *Objective: Mend the Book of Arrivals.* Archive loft. **Leatherworking ~[GD: low]**: the repair interaction on the spine (cut the old thread, re-stitch, glue; three 4 s channels, segments persist). Then *Ease the pages* (a 3 s channel on the stuck block). **Crew alternative:** Ysolde's apprentice does it overnight (`MBA-D2.05`; keep watch to morning; `MBA_SPINE = crew`).

**Beat 2 — Search by weather (`S02_search`).** *Objective: Find entries from the spring the ferry way froze.* The book is grouped by weather runs, with a weather line heading each run (inspect any heading for flavour). The player pages to the run headed *"Long frost. Ferry way frozen. Thaw."* (an index interaction: three runs visible per page spread, the right one found by reading headings; wrong runs simply show other entries). Three entries in that run are candidates (three required inspects, `MBA-I2.01`–`.03`): a woman with two children "up from the fowling meres"; an old man "from the Field's edge, would not say"; and **the Brede entry**.

**Beat 3 — Match (`S03_match`).** *Objective: Match an entry to the token.* *Show* the token on the book (use carry-state on the open book): the Brede entry has a margin note, *"Carries a stick, notched, on a thong."* (`MBA-I2.03`). That is one hold that fits the token. The player needs a second hold from outside the book.

**Beat 4 — The Rudd book (`S04_rudd`).** *Objective: Read the Rudd household book at Marshfall.* At the Rudd house, inspect the **peg** (`MBA-I3.01`) and read the **household book** (`MBA-I3.02`): *"Took in the high-pass man from the care list. Carries peat. Says little. Hangs his stick on the peg."* and, a thaw later, *"The high-pass man went on with the thaw. Left his stick on the peg. Mother says leave it."* The household book never writes "Brede"; it says "the high-pass man". Optional: Senna's grandson Wyn's bark at the peat yard (`MBA-B2.01`).

**Beat 5 — Untie it (`S05_knot`, optional but offered).** Back at the register room, before the strip is written, Senna asks the player to untie the token's double knot so she can hang it on the wall with the strip "loose, like it was put down". *Untie* (a 3 s channel). **The wonder moment** (MBA.7). Skipping it leaves the knot tied; nothing else changes.

**Beat 6 — The wall (`S06_wall`).** *Objective: Tell Ysolde what the strip should say.* `MBA-D5`. Ysolde sets the holds side by side: the care entry (book) and the household book with the token (household). "Two holds. One man. Whether it's one **name** is another thing." The book says *Brede*; the household never did. **Thornfell variants** (optional lines; never holds here): with `TWN_MIRE_HOOK`, the player may say a family at the high steads renews a slip each spring for a Brede who "went over the pass" (`MBA-D5.20`); with `thornfell.main.05_stonewake` Completed, the player may mention the gatehouse wall (`MBA-D5.25`). Ysolde writes that the player said it, as testimony from away, and that it is not a hold here. Choice (`MR_ARRIVALS`):
- **Named:** *"Brede, down from the high passes with the thaw. Lodged with Rudd, Marshfall. Carried peat. Went on."*
- **Held:** *"One we hold, not yet known. Down from the high passes with the thaw; gave the name Brede. Lodged with Rudd, Marshfall. Went on."*

Senna hangs the token beside the strip (or takes it home: her choice, presentation only). Quest Completed (`MBA-D6`).

### MBA.6 Encounters

None. **MD-7 swap note:** no Hollowfoot content.

### MBA.7 The wonder moment: the knot that won't lie straight (Beat 5)

| Time | Element | Spec |
|---|---|---|
| 0–3 s | **Untie** | The player works the double knot loose. Close camera on hands (no cutscene; the player's own view of the interaction). |
| 3–6 s | **The thong** | Laid on the table, the thong keeps the shape of the knot: two kinks, exactly where the loops were. The player can *Smooth it* (2 s). It springs back. |
| After | **Senna** | `MBA-D4.02`: "Thirty years on a peg. It's learned the knot." |
| With `TWN_COMPLETE` | **Inner voice** | *"The same double knot as the thong on Asa Brede's tally stick at Hushfold. Carriers tie them that way. That proves nothing."* |
| What it means | | Leather that has kept a shape for thirty years. Nothing more is suggested. It is the quest's moment of wonder because it is ordinary. |

### MBA.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Hear Senna out. | `MBA-D1` end with accept + token inspect | Yes |
| `S01_spine` | Mend the Book of Arrivals. | 3 × `stitch_spine` + `ease_pages` **or** keep watch (crew) | Yes |
| `S02_search` | Find entries from the spring the ferry way froze. | Correct run found + 3 candidate inspects | Yes |
| `S03_match` | Match an entry to the token. | *Show* token on book at the Brede entry | Yes |
| `S04_rudd` | Read the Rudd household book at Marshfall. | Peg + 2 household-book inspects | Yes (any order with S02–S03) |
| `S05_knot` | (Optional) Untie the token's knot. | `untie_knot` channel | No |
| `S06_wall` | Tell Ysolde what the strip should say. | `MBA-D5` choice + `MBA-D6` end | Yes (→ Completed) |

### MBA.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `MBA_SPINE` = self / crew | `S01` | `MBA-B1.03` |
| `MBA_KNOT_UNTIED` | `S05` | `MBA-D5.03` variant; wall prop (token hangs loose or knotted) |
| `MBA_FROM_AWAY` | `MBA-D5.20` or `.25` | Ysolde's written line; `MBA-D6.03` |
| **`MR_ARRIVALS` = named / held** | `MBA-D5` | CV-M3 R14 chip (request: reads value only) |

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Named** | The strip names him "Brede". | A family name stands for a man; if two Bredes went over, the strip cannot say which, and Ysolde writes "Name as he gave it" beneath. | CV-M3: the Mire's arrival can be set beside a Thornfell record by the player (request). Senna: "There. He's somebody." |
| **Held** | The strip holds him "not yet known" with the name he gave. | Senna is disappointed: "He told Mother his name." Ysolde: "He told her a name. We hold it." | CV-M3: same chip value; the record is more careful than the family. Senna comes round (`MBA-B2.03`). |

Neither value says what happened to him. He "went on". No route, direction or destination is given.

### MBA.10 Rewards, failure, co-op

| Reward | Type | Notes |
|---|---|---|
| **The arrivals wall** | Knowledge | Readable strips (`MBA-I4.01`); flavour for every Mire settlement's "came in" stories. |
| **A bed at the Rudd house** | Access | Rest point at Marshfall (Senna: "His bed. It's a bed."). |
| Small payment | Currency | Ysolde pays for a mended book [GD]. |
| Skill XP | Actions only [GD] | Leatherworking. |
| *The Empty Place* | Story | `MBA-D6.04`: Ysolde has a Sorrowmere child she is worried about. |

| Situation | Handling |
|---|---|
| Wrong run or entry | Other entries show; no penalty. |
| *Show* token on wrong entry | Ysolde: "Nothing about a stick there." |
| No Leatherworking | Crew alternative. |
| Walking away | Stays Active; the token stays with the player (carry-state) and returns to Senna on completion; if dropped, it returns to Senna and she hands it back on the next talk. |
| Fail state | None. |
| Co-op | Each player mends and searches their own instance of the book (fallback: shared spine progress). The wall strip shows each player's own value (fallback: host's). |

### MBA.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| Book index by weather run | UI | A paged document view with run headings; three entries inspectable on the right spread. **Fallback:** dialogue list of three run headings. |
| *Show* carry-state on a document | Systems | Use-object-on-prop with a match id. |
| Leatherworking repair interaction | Systems | Existing repair interaction on a prop (bible MD-11: repair of imported leather). |
| Knot prop with two states | Art | Thong tied / untied-kinked. |
| Per-player wall strip | Systems | Per-player prop text. |
| Cross-region condition reads | Schema | `TWN_MIRE_HOOK`, `TWN_COMPLETE`, `thornfell.main.05_stonewake` Completed: variant lines only. |

**Mystery ledger.**

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Who the high-pass man was** | A man stranded by Thornfell's late-war sealings who reached the Mire with a thaw column (R14). Which Brede is never settled. | "A carrier from away." | Care entry; token; Rudd book; (Thornfell) slip, stick, rubbing as the other region's records. | He is certainly Sig Brede; the Thornfell cairn is a lie. | Which Brede; where he went. | R14 (here, optional); CV-M3 chip. |

**Open decisions.** (1) MD-14 stands: if the Director wants no Brede in Mire content at all, the entry reads "gave a carrier's name" and only `MBA-I2.03` and `MBA-D5` change. (2) "The high passes" is used as people's words for where he came from; no route is described.

| Review finding | Revision |
|---|---|
| Draft let the Thornfell slip count as a second hold. | Ysolde writes it as testimony from away, not a hold here. The Mire's two holds are the book and the household. |
| The knot risked implying the token proves Sig. | Inner voice says carriers tie them that way and it proves nothing. |
| The book first had a calendar year on the frost. | Weather-run headings only. |

### MBA.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Senna Rudd** [NEW], about seventy | Her mother's words; the token; that he left in spring. | His first name; where he went. | Brisk, a bit deaf when it suits her, fond of him still; she had children of her own when he lodged. |
| **Ysolde Haverel** | The book's form; two holds. | Anything the book doesn't say. | Careful about "name" versus "man". |
| **Wyn Rudd** [NEW], Senna's grandson (bark only) | Peat. | — | Cheerful. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| MBA-B1.01 | Ysolde | Available | *"There's a woman from Marshfall with a stick she won't put down. Come and meet her."* |
| MBA-B1.02 | Ysolde | Active, returns | *"The book's in the loft. It doesn't go anywhere. Neither does Senna."* |
| MBA-B1.03 | Ysolde | `MBA_SPINE = self` | *"The spine's holding. Better than I'd have done. Don't tell my apprentice."* |
| MBA-B2.01 | Wyn Rudd | `S04` | *"Gran's high-pass man? Carried more peat than two of us, Gran says. Gran says a lot."* |
| MBA-B2.02 | Senna | Completed, `named` | *"Brede. On a wall. Mother would've made him a cake."* |
| MBA-B2.03 | Senna | Completed, `held` | *"'Not yet known.' Well. Neither am I, much."* |

#### Nodes

```
MBA-D1 (register room; S00)
MBA-D1.01 SENNA: (holding a notched stick on a thong) "You're the stranger. Good. She said you'd help and you look like you lift."
MBA-D1.02 YSOLDE: "Senna Rudd, Marshfall. Her mother took someone in, in the war."
MBA-D1.03 [MNS_HOOK_ASKED] YSOLDE: "You've asked after names before. This one came the other way."
MBA-D1.04 [MSS_RUBBING = taken] YSOLDE: (glancing at the framed rubbing) "Another one from outside the lines."
MBA-D1.05 SENNA: "A man came down from the high passes with the thaw. Mother had him in care. He carried peat. Said almost nothing. One spring he went on. Left this on her peg."
MBA-D1.06 SENNA: "I want him on the wall. With the others who came in. He was somebody to us."
MBA-D1.07 YSOLDE: "Then I need his care entry. Everyone we took in went in the Book of Arrivals." (beat) "The book's in the loft. The spine went in the wet. It may not open."
MBA-D1.08 SENNA: "Mother said: the thaw after the long frost. The spring the ferry way froze. She'd say it like that, every time."
  > "I'll find him."                                         → MBA-D1.10
  > "Can I see the stick?"                                   → MBA-D1.20
  > "Not now."                                               → MBA-D1.40
MBA-D1.10 SENNA: (holds out the token) "Take it. Bring it back. It's the only thing of his."   {carry-state token; quest Active; event: S00}
MBA-D1.20 {token inspect} SENNA: "Notches for loads. He'd cut one every time. Then he stopped cutting."   → MBA-D1 options
MBA-D1.40 SENNA: "I'm seventy. I'll wait a bit. Not long."   {quest Inactive}
```

```
MBA-D2 (archive loft; S01)
MBA-D2.01 YSOLDE: (from the ladder) "Awl, thread, glue. The leather's from away, so it stitches like from away. Tight."
  > "I'll stitch it."                                        → MBA-D2.02
  > "Better someone who's done it before."                   → MBA-D2.05
MBA-D2.02 YSOLDE: "Go gently. Every page in there is a person."   {Leatherworking repair; MBA_SPINE = self}
MBA-D2.05 YSOLDE: "My apprentice. Tomorrow. She'll complain about the glue."   {keep watch to morning; MBA_SPINE = crew}
MBA-D2.10 (book open) YSOLDE: "It's kept by weather. Every run has a heading. Find the frost and the frozen ferry."
```

```
MBA-D3 (on the match; S03)
MBA-D3.01 (inner voice, prompt line) "A margin note beside the Brede entry: 'Carries a stick, notched, on a thong.'"
MBA-D3.02 YSOLDE: (if present, or at the next talk) "That's one hold. The book says a stick. Now I want the house to say so too."
```

```
MBA-D4 (register room; S05)
MBA-D4.01 SENNA: "Untie it for me. My fingers don't. I want it hung loose, like it was put down. Not tied like it was waiting."
MBA-D4.02 [MBA_KNOT_UNTIED] SENNA: (watching it spring back) "Thirty years on a peg. It's learned the knot."
```

```
MBA-D5 (register room; S06)
MBA-D5.01 YSOLDE: "Sit. Senna's brought bread. Eat it or she'll tell everyone." (beat) "Now."
MBA-D5.02 YSOLDE: "The book: 'Received: a man, down from the high passes with a thaw column. Gave his name as Brede. Hands raw from carrying. Care: Rudd, Marshfall.' And a stick in the margin."
MBA-D5.03 YSOLDE: "The house: 'the high-pass man', a stick on the peg, gone with the thaw. And the stick itself." [MBA_KNOT_UNTIED] "Untied, now."
MBA-D5.04 YSOLDE: "Two holds. One man. That's sound." (beat) "Whether it's one **name** is another thing. The book says Brede. The house never wrote it. Brede's a family name."
  > [TWN_MIRE_HOOK] "In the high steads, a family renews a slip every spring for a Brede who 'went over the pass'."   → MBA-D5.20
  > [thornfell.main.05_stonewake Completed] "There's a wall at a gatehouse in the passes with names cut on it. No Brede."   → MBA-D5.25
  > "What should the strip say?"                                                                                      → MBA-D5.30
MBA-D5.20 YSOLDE: (writes) "'Witness says: a family at the high steads keeps a slip for a Brede, went over the pass.'" (beat) "That's testimony from away. I'll keep it. It isn't a hold here, and it doesn't say which Brede."   {set MBA_FROM_AWAY}   → MBA-D5.04 options
MBA-D5.25 YSOLDE: (writes) "'Witness says: a gatehouse wall, no Brede on it.'" (beat) "Not being on a wall isn't nothing. It isn't a hold either."   {set MBA_FROM_AWAY}   → MBA-D5.04 options
MBA-D5.30 YSOLDE: "You're the witness. What do I write?"
  > "Write his name as he gave it. 'Brede, down from the high passes with the thaw.'"               → MBA-D5.40
  > "Hold him. 'One we hold, not yet known.' With the name he gave."                                → MBA-D5.50
MBA-D5.40 YSOLDE: (writes) "'Brede, down from the high passes with the thaw. Lodged with Rudd, Marshfall. Carried peat. Went on.'" (beat) "And under it: 'Name as he gave it.'"   {set MR_ARRIVALS = named}   → MBA-D6.01
MBA-D5.50 YSOLDE: (writes) "'One we hold, not yet known. Down from the high passes with the thaw; gave the name Brede. Lodged with Rudd, Marshfall. Went on.'"   {set MR_ARRIVALS = held}   → MBA-D6.01
```

```
MBA-D6 (close)
MBA-D6.01 SENNA: (takes the token back; hangs it on the peg beside the strip, or pockets it) "There."
MBA-D6.02 YSOLDE: "Arrived is a record too. Somebody may come asking after a Brede from the passes. They'll find he was here, and that somebody kept his stick."
MBA-D6.03 [MBA_FROM_AWAY] YSOLDE: "And they'll find you said what you'd heard away. That's written too."
MBA-D6.04 YSOLDE: "There's a child down the way who keeps setting a place for her uncle. I don't like it. Come by when you can."
      {Senna's token returns to her; event: S06 → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| MBA-I1.01 | Tally token | *"A short stick, notched along one edge, close together, then a gap, then nothing. A leather thong tied with a double knot."* |
| MBA-I1.02 | Tally token (`TWN_COMPLETE`) | *As above, then:* *"The double knot is the one carriers use. You have seen it on a thong at Hushfold."* |
| MBA-I2.01 | Candidate entry 1 | *"'Received: a woman, two children, up from the fowling meres. Gave her name as Iva. Care: Sallis.'"* |
| MBA-I2.02 | Candidate entry 2 | *"'Received: an old man from the Field's edge. Would not give a name. Care: the Fenward. Died the same run.' A ring is drawn round it."* |
| MBA-I2.03 | The Brede entry | *"'Received: a man, down from the high passes with a thaw column. Gave his name as Brede. Hands raw from carrying. Care: Rudd, Marshfall.' In the margin: 'Carries a stick, notched, on a thong.'"* |
| MBA-I2.04 | A run heading | *"'Long frost. Ferry way frozen. Thaw.' Below it, entries in three hands."* |
| MBA-I3.01 | The Rudd peg | *"A wooden peg by the door. The wall round it is paler, in the shape of something that hung there a long time."* |
| MBA-I3.02 | Rudd household book | *"'Took in the high-pass man from the care list. Carries peat. Says little. Hangs his stick on the peg.' A thaw later: 'The high-pass man went on with the thaw. Left his stick on the peg. Mother says leave it.'"* |
| MBA-I4.01 | Arrivals wall | *"Reed strips. 'Off the Standards road.' 'Up from the meres.' 'From away.' Some say only: 'One we hold.'"* |

*(Iva Sallis in `MBA-I2.01` is a reed-strip name only; Corra Sallis's family name is common in Sorrowmere and nothing connects them.)*

---

## MEP — The Empty Place

### MEP.1 The quest in one paragraph

At the Keel house in Sorrowmere, **Posy Keel**, eight, sets a second place at every meal and leaves a small **work sign** on it: a peg-knife cut from reed, a painted chip, a twist of moss. Her mother **Annis** thinks Posy is mourning her uncle **Lew**, who went to the root-timber cut past Rootrest in spring and stopped writing. Annis has started talking about him in the past tense. Ysolde is worried: in the Mire, the second place means "ask after someone" (MME04), never "dead", and a child has understood it better than the adults. The player **reads the signs** (each one points somewhere: the peg-knife is a timber cutter's; the painted chip is a ferry token), asks Posy, and **searches the ferry book** at Blackwater Landing: Lew has crossed both ways twice since his last letter, most recently a few weather runs ago. He is alive. The player finds him at the **root-timber lot**: behind on his quota after a split went wrong, ashamed to come home with nothing, and unable to write the word "nothing". The player helps him finish (Woodcutting), or the crew covers him for a day. Lew walks home. On his way past the table he stops: in his coat is a reed peg-knife, the same as the one on his plate. He taught her to make it before he left. The register gains a column.

**Remember:** two identical reed knives, one on a plate, one in a coat. **Want next:** Lifting Day, when returns are celebrated with the dead.

### MEP.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| **A. Lew is dead and the child is right to mourn.** | Rejected. The bible pitch: he is alive. The quest is about asking after, not mourning. |
| **B. The player tells Annis; Lew never appears.** | Rejected. "Welcome" needs a body at the table. |
| **C. Signs → ferry book → the lot → work → home** (selected). | **Selected.** Read, find, welcome; a Woodcutting hook; a warm ending that adds a column to the register. |

| Element | Source | Status |
|---|---|---|
| The second place; a child's work sign; "ask after someone", never "dead" | Bible MME04 | [NEW] |
| Ferry households; Blackwater Landing | Bible §4.2 MP06 | [CANON anchor location; NEW name] |
| Rootrest root-sheltered homes; reclaimed root wood | Dossier §VII; bible MD-11 | [CANON]; [NEW] |
| Optional Lowmark line: the Holt candle-boat (`CN_COMPLETE`) | Lowmark *The Candle Rule*; bible §7.1 | [NEW, Lowmark package] |
| The Keels, the timber lot, the ferry book, "away, not lost" | This package | [NEW] |

### MEP.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `mire.side.the_empty_place` |
| Series | *Names Below*, part 3 of 3 (finale) |
| Type | Settlement |
| Unlock | MBA Completed. Ysolde's line `MBA-D6.04`; or MME04 at the Keel house (Posy's bark `MEP-B1.01` points the player to Ysolde). |
| Length | 30–40 minutes |
| Combat share | 0% |
| Skills | **Woodcutting ~[GD: low–mid]**: split three root-knees to finish Lew's quota. Crew alternative: the timber crew covers him (keep watch one turn; Lew comes home a turn later, `MEP_QUOTA = crew`). |
| Choice | How Lew comes in (`MEP_HOME`: table / way). The outcome is the family's. |
| Outputs | `MEP_HOME`; Names Below "away, not lost" column (world prop); Lew at Sorrowmere |
| **Anchor** | Sorrowmere households (Keel); ferry households (the landing's ferry book). |
| **World-truth row** | H23 (recovery: who counts as lost). |
| **Revelation role** | Self-contained. Optional Lowmark callback line (`CN_COMPLETE`), resolved locally. |
| **Recurring evidence** | None required. The ferry book (Blackwater Landing; ferry households) is read in place. |
| **State compliance** | Inactive → Active on `MEP-D1` accept; Completed on `MEP-D6` end. No fail. Resume hook: Annis at the Keel house (`MEP-B1.03`). |
| **Combat compliance** | None. |

### MEP.4 The places

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. The Keel house** (Sorrowmere) | Hook; signs; welcome | A one-room longhouse off the raised way. Table for three; the third stool pushed in. At the second place, a plate and Posy's sign of the day. On a shelf, Lew's last letter, folded small. A child's drawing of a boat on the wall. |
| **B. Blackwater Landing** (MP06) | Ferry book | The ferry households' passage book on a lectern in the boat shed, under a lantern. Rowan is about; he says one thing (`MEP-B2.01`). |
| **C. The root-timber lot** (past Rootrest) | Find Lew; Woodcutting | A clearing of dead and cut roots on firm ground, MAP VERIFICATION REQUIRED (bible §4.2: Rootrest on firmer ground beyond Marshfall). A quota board with crew names and notches. A split root-knee, ruined, pulled aside. Lew's lean-to: a blanket, a carving knife, reed shavings. |

### MEP.5 Player-facing sequence

**Beat 0 — The second place (`S00_offer`).** *Objective: Ask Ysolde about the Keel child.* `MEP-D1` (Ysolde). She explains the second place; Annis has started saying "was". "I don't think he's dead. I think he's late. I can't go knocking." The player goes.

**Beat 1 — The signs (`S01_signs`).** *Objective: Look at what Posy leaves.* At the Keel house, `MEP-D2` (Annis, Posy). Three signs over three meals (keep watch twice, or arrive at different hours; the house has a meal at morning, noon and dusk): **a reed peg-knife** (a timber cutter's marking knife, `MEP-I1.01`), **a painted chip** (a ferry token, `MEP-I1.02`), **a twist of moss** (lantern moss, "so he can see", `MEP-I1.03`). Ask Posy (`MEP-D2.20`): "It's asking. You leave a sign so the place knows what to ask." Read Lew's last letter on the shelf (`MEP-I1.04`).

**Beat 2 — The ferry book (`S02_ferry`).** *Objective: Search the landing's ferry book for Lew Keel.* At Blackwater Landing, page the book by weather runs (as in MBA, simpler: one spread per run). Two entries after his last letter: *"Keel, J. Across, Rootrest side."* and, a few runs later, *"Keel, J. Back over, Rootrest side. Didn't stop."* (`MEP-I2.01`–`.02`). He came within a landing of home and turned round.

**Beat 3 — The lot (`S03_lot`).** *Objective: Find Lew at the root-timber lot.* Travel. `MEP-D3` (Lew). The quota board (`MEP-I3.01`): his line short. The ruined root-knee (`MEP-I3.02`). Lew: a split went wrong, he lost a week's work, the crew's paid by quota, he wasn't going home with nothing. He didn't write because "Annis writes back asking when."

**Beat 4 — The quota (`S04_quota`).** *Objective: Help Lew finish his quota.* **Woodcutting ~[GD: low–mid]**: three root-knees from the lot's pile, split along the grain (each a 4 s channel; segments persist), stacked on Lew's mark. **Crew alternative:** the timber crew's foreman covers him (`MEP-D3.30`; keep watch one turn; `MEP_QUOTA = crew`).

**Beat 5 — Home (`S05_home`).** *Objective: Walk Lew home.* Choice at the lot gate (`MEP_HOME`): **table** (straight to the house, at the next meal) or **way** (Lew asks to walk the raised way first so the street sees him, and Posy runs out). Either way, at the Keel house: **the wonder moment** (MEP.7). Annis, then Posy.

**Beat 6 — The column (`S06_column`).** *Objective: Tell Ysolde.* At the register room, Ysolde rules a new column on the index board and heads it *"Away, not lost."* She moves Lew's strip into it, then three others from elsewhere on the board that she has been worried about. Optional Lowmark line (`CN_COMPLETE`): the player tells Annis of a mother in the lowlands who sets a candle-boat every flood season for a son (`MEP-D5.10`). Quest Completed (`MEP-D6`).

### MEP.6 Encounters

None. **MD-7 swap note:** no Hollowfoot content.

### MEP.7 The wonder moment: two knives (Beat 5)

| Time | Element | Spec |
|---|---|---|
| 0 s | **The door** | Lew steps into the Keel house. Annis stands up. Nobody speaks for about two seconds. |
| 2–5 s | **The plate** | Lew looks at the second place: today's sign is the reed peg-knife. He puts his hand in his coat and takes out an identical one, half carved, reed shavings still caught in the binding. He lays it beside hers. |
| 5–8 s | **Posy** | Posy, from the stool: "You taught me." Lew: "I did." |
| After | `MEP-D4` | Annis makes him sit. Food before anything (bible §5.3 rule 6). |
| What it means | | He kept carving the sign he taught her. Nothing uncanny: two people asking after each other with the same tool. |

### MEP.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Ask Ysolde about the Keel child. | `MEP-D1` end with accept | Yes |
| `S01_signs` | Look at what Posy leaves. | 3 sign inspects (three meal hours) + `MEP-D2.20` + letter inspect | Yes |
| `S02_ferry` | Search the landing's ferry book for Lew Keel. | 2 ferry-book inspects | Yes |
| `S03_lot` | Find Lew at the root-timber lot. | `MEP-D3` end + 2 inspects | Yes |
| `S04_quota` | Help Lew finish his quota. | 3 × `split_root` **or** keep watch (crew) | Yes |
| `S05_home` | Walk Lew home. | `MEP-D3.50` choice + escort to Keel house + `MEP-D4` end | Yes |
| `S06_column` | Tell Ysolde. | `MEP-D5` + `MEP-D6` end | Yes (→ Completed) |

### MEP.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `MEP_QUOTA` = self / crew | `S04` | `MEP-D3.40` variant; timber-lot bark |
| `MEP_HOME` = table / way | `MEP-D3.50` | MLD (Lew walks with the returns; Posy's sign); Sorrowmere barks |

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Table** — *"Straight home. Next meal."* | Lew walks quietly to the house; the moment is private. | The street hears about it second-hand; a neighbour sulks (`MEP-B3.02`). | MLD: Lew walks with the returns; Posy carries the peg-knife. |
| **Way** — *"Walk the raised way. Let them see you."* | Lew walks the raised way in daylight; people stop work; Posy runs out to meet him before the door. | Lew hates it and says so; the two-knives moment happens at the door with half the street watching. | MLD: Lew walks first among the returns ("I've done it once"). |

The outcome is the family's in both: Lew is home, Posy keeps setting the second place (now for whoever is away), and the register gains its column.

### MEP.10 Rewards, failure, co-op

| Reward | Type | Notes |
|---|---|---|
| **The Keel table** | Access | A meal at the Keel house at any hour (an ordinary cooked food item once per presentation day) [GD]. |
| **"Away, not lost"** | Knowledge / world | A new column on the Names Below index board; Ysolde barks change for missing-person asks. |
| Small payment | Currency | Lew's first quota pay, half pressed on the player [GD]. |
| Skill XP | Actions only [GD] | Woodcutting. |

| Situation | Handling |
|---|---|
| Arrives at a meal already seen | The sign is the same; keep watch for the next. |
| No Woodcutting | Crew alternative. |
| Leaves Lew at the lot | He waits at the lot gate ("I'll go when you go"). Escort is a follow, not a protect; no threats on the route. |
| Walking away | Stays Active; resume at Annis (`MEP-B1.03`) or Lew (`MEP-B2.03`). |
| Fail state | None. |
| Co-op | Shared escort (Lew follows the player who spoke to him; fallback: host). Signs and the column are per player (fallback: host). |

### MEP.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| Meal-hour sign prop | Systems | Prop variant keyed to presentation hour (three signs). |
| Follow escort | NPC | Standard follow with a gate wait. |
| Index-board column prop | Art / Systems | Per-player prop swap at completion. |
| Ferry book document | UI | Same paged view as MBA. |

**Mystery ledger.** *Why Lew stopped writing:* shame at a short quota; "nothing" was a word he would not write. Self-contained; no withheld layer.
**Open decisions.** MAP VERIFICATION REQUIRED for the timber lot. If the economy pass objects to root-knee volume, the quota can be "three loads carried" instead (Woodcutting becomes carry); only `S04` changes.

| Review finding | Revision |
|---|---|
| Annis first scolded Posy. | Annis is grieving early; she never scolds; she just stops saying "is". |
| The Lowmark line risked implying Ewan Holt is in the Mire. | It is only about the Holt mother's practice; nothing about Ewan's fate. |

### MEP.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Posy Keel** [NEW], 8 | What the second place means. | That the adults misread her. | Exact; explains as if to a slow adult. |
| **Annis Keel** [NEW] | Lew's last letter; her fear. | That he crossed twice. | Tired, polite, says "was" and hears herself. |
| **Lew Keel** [NEW] | The lot; his quota. | That Posy thinks he's asking back. | Says less than he means. |
| **Rowan Mirewake** (bark only) | The landing. | — | One line. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| MEP-B1.01 | Posy | Available, player at the Keel door | *"That place isn't yours. It's asking."* |
| MEP-B1.03 | Annis | Active, returns | *"She set it again. I didn't move it. I can't."* |
| MEP-B2.01 | Rowan | `S02` | *"Keel. Crossed twice. Didn't look at the landing either time."* |
| MEP-B2.03 | Lew | Active, at the lot | *"I'll come when it's done. Or when you drag me."* |
| MEP-B3.01 | Sorrowmere neighbour | Completed, `way` | *"Lew Keel walked the way at noon like a wedding. Nobody's let him forget it."* |
| MEP-B3.02 | Sorrowmere neighbour | Completed, `table` | *"Keel's back and nobody told me. I'd have made something."* |
| MEP-B3.03 | Posy | Completed | *"It's for whoever's away now. Today it's a moss. That's for the Tenders' girl. She's on the roof."* |

#### Nodes

```
MEP-D1 (register room; S00)
MEP-D1.01 YSOLDE: "The Keel child sets a second place. Every meal. That's not odd. We all do it, now and then."
MEP-D1.02 YSOLDE: "Her mother's started saying 'was' about her brother. He's at the root-timber, past Rootrest. Stopped writing."
MEP-D1.03 YSOLDE: "The second place means ask after someone. It doesn't mean dead. The child knows that. I think the adults have forgotten."
MEP-D1.04 YSOLDE: "I can't go knocking. I keep the register. If I knock, it's a register visit."
  > "I'll knock."                                             → MEP-D1.10
  > "Not now."                                                → MEP-D1.20
MEP-D1.10 YSOLDE: "Thank you. Eat whatever she gives you."   {quest Active}
MEP-D1.20 YSOLDE: "It'll keep. I hope."   {Inactive}
```

```
MEP-D2 (Keel house; S01)
MEP-D2.01 ANNIS: "Ysolde sent you. Sit. There's enough." (she does not look at the second place)
MEP-D2.02 ANNIS: "Lew was..." (stops) "Is. My brother. Root-timber. He writes. He did."
MEP-D2.03 ANNIS: "She sets that every meal. I let her. It's how she's managing."
MEP-D2.20 [first sign inspected] POSY: (not looking up from her bowl) "It's asking."
  > "Asking what?"                                            → MEP-D2.21
MEP-D2.21 POSY: "You leave a sign so the place knows what to ask. That's a cutter's knife. It's asking where he's cutting."
MEP-D2.22 [chip inspected] POSY: "Ferry. It's asking did he cross."
MEP-D2.23 [moss inspected] POSY: "Moss. So he can see. It's dark at the timber."
MEP-D2.24 ANNIS: (very quiet) "I thought she was..." (beat) "Oh."
```

```
MEP-D3 (the lot; S03–S05)
MEP-D3.01 LEW: (splitting badly) "If Annis sent you, I'm fine. If Ysolde sent you, I'm still fine."
MEP-D3.02 LEW: "Split went wrong. Lost a week of knees. Crew's paid by the board. I'm not going home with nothing."
MEP-D3.03 LEW: "I came as far as the landing. Twice. Turned round." (beat) "Annis writes back asking when. I can't write 'nothing'."
  > "Your niece sets a place for you every meal."  → MEP-D3.04
  > "Let's fill your board."                                  → MEP-D3.20
MEP-D3.04 LEW: "Posy." (long pause) "Annis thinks I'm dead, doesn't she."  → MEP-D3.20
MEP-D3.20 LEW: "Three knees and the board's square. Grain runs this way. Don't fight it."
  > "I'll split them."                                        → MEP-D3.21
  > "Can the crew cover you?"                                 → MEP-D3.30
MEP-D3.21 {Woodcutting; MEP_QUOTA = self}
MEP-D3.30 FOREMAN: "We'll cover him a day. He's covered us." {keep watch; MEP_QUOTA = crew}
MEP-D3.40 [quota done] LEW: "Square." [MEP_QUOTA = self] "You split straighter than me. Don't say so at home."
MEP-D3.50 LEW: "How do I go in?"
  > "Straight home. Next meal."                               → MEP-D3.51  {set MEP_HOME = table}
  > "Walk the raised way. Let them see you."                  → MEP-D3.52  {set MEP_HOME = way}
MEP-D3.51 LEW: "Quiet. Good."
MEP-D3.52 LEW: "In daylight. Like a fool." (beat) "All right."
```

```
MEP-D4 (Keel house; S05)
MEP-D4.01 (wonder moment: the two knives)
MEP-D4.02 POSY: "You taught me."  LEW: "I did."
MEP-D4.03 ANNIS: (pulls the third stool out) "Sit. Eat. Then tell it."
MEP-D4.04 LEW: "There's nothing to tell." (beat) "There's a split knee and a board."
MEP-D4.05 ANNIS: "Then tell me that."
```

```
MEP-D5 (register room; S06)
MEP-D5.01 YSOLDE: "He's home." (it isn't a question)
MEP-D5.02 YSOLDE: (rules a new column on the index board with a reed and a straightedge) "'Away, not lost.'" (moves Lew's strip; then three others) "These three I've been worried about. They're not lost either. Just not here."
MEP-D5.10 [CN_COMPLETE] (optional, to Annis on a later visit) "In the lowlands, a mother sets a candle-boat every flood season for a son who went to the war."
MEP-D5.11 ANNIS: "Every season." (beat) "Then she's still asking. Good. Somebody should be."
```

```
MEP-D6 (close)
MEP-D6.01 YSOLDE: "We spend so long writing who's lost, we forget to write who's only late." (beat) "Thank you, witness."
      {event: S06 → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| MEP-I1.01 | Reed peg-knife | *"A cutter's marking knife made of reed, bound with grass. A child's copy of a real one. Well made."* |
| MEP-I1.02 | Painted chip | *"A ferry token: a wood chip painted ochre, the Slack colour."* |
| MEP-I1.03 | Moss twist | *"Lantern moss, twisted into a knot. It glows faintly where it is damp."* |
| MEP-I1.04 | Lew's last letter | *"'Lot's good. Knees are hard. Home before the long wet. Tell Posy to practise her knife.'"* |
| MEP-I2.01 | Ferry book 1 | *"'Keel, J. Across, Rootrest side.'"* |
| MEP-I2.02 | Ferry book 2 | *"A few runs later: 'Keel, J. Back over, Rootrest side. Didn't stop.'"* |
| MEP-I3.01 | Quota board | *"Crew names and notches. Lew's line is short by three."* |
| MEP-I3.02 | Ruined root-knee | *"Split across the grain, into useless wedges. A week's drying gone."* |

---

# Series two — Lanterns and Tenders

---

## MLL — The Broken Lantern Light

### MLL.1 The quest in one paragraph

**Prue Calloway**, a Chapel-Tender at Sorrowmere's memorial gardens, has walked to **Stillgrave Hollow** three nights running to help a family with a burial rite, and three nights her lantern has gone out at the water's edge. The family is the **Haddow household** of Sorrowmere's lower ways: **Ebba**, the eldest; her daughter **Bryony**; Bryony's son **Dob**. Bryony's husband **Corin** drowned at Stillgrave's edge in this spring's spate, cutting reed. The family began a **mourning ring** of lantern stakes on the bank, one stake for each of them, and abandoned it halfway: the lanterns would not stay lit, and the last night something stood up out of the mud where Bryony was kneeling. Prue knows lantern moss and wax. She does not know why the Hollow swallows light. The player goes at night to gather moss at the Hollow's edge (it glows only in the dark), re-stitches the split leather hood of Prue's lantern so the wick stays dry, and asks why grief sits in this water: Ebba gives only what she has seen (stones worn hollow, a Hollow nobody fishes), and Prue gives the Tenders' saying that the dead were washed here at the war's end and the water keeps it, labelled as belief. Then the player holds the line: while each Haddow sets a stake and says what they are setting it for, the player keeps the ring lit as **Earthen Echoes** stand up out of the grief at the edge. They re-form until the ring is finished. When Dob sets the last stake, Stillgrave's water stops bending the light.

**Remember:** lantern light lying straight on water that has always pushed it away. **Want next:** Mabyn's roof, and the lantern the Tenders say would not go out.

### MLL.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| **A. A war-dead family's ring.** | Rejected. Contract: present-day grief. Stillgrave's war past is a reason the water is heavy, not the case. |
| **B. Fix the lantern and the Hollow quiets.** | Rejected. A lantern does not resolve grief. The family finishing their ring does. |
| **C. Moss at night → mend the hood → learn why → hold the lit ring while the family finishes** (selected). | **Selected.** Dossier questline 3 elements in play; teaches lantern moss early (bible §1.1); rehearses MR-M5 "finishing a circle". |

| Element | Source | Status |
|---|---|---|
| A Chapel-Tender's lantern won't stay lit near Stillgrave; gathering lantern moss; burial rites; why grief saturates the area; an unfinished mourning circle | Dossier §XV questline 3 | [CANON] |
| Stillgrave: unnervingly clear water; lantern light bends near the surface; imprints in deep grief | Dossier §VI.4 | [CANON] |
| Lantern moss glows when damp; lit line = tended line | Bible §1.1 | [NEW] |
| Earthen Echoes drawn to strong emotion; collapse when struck | Dossier §IX; bible §2.4 | [CANON] |
| Tender belief that the dead were washed at Stillgrave at the war's end (said only as a belief; no record or living witness supports it, and no canon source states it) | This package (Prue's line) | [NEW, belief only] |
| The Haddow household, Corin, the ring of stakes, Prue Calloway | This package | [NEW] |

### MLL.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `mire.side.the_broken_lantern_light` |
| Series | *Lanterns and Tenders*, part 1 of 3 |
| Type | Environmental |
| Unlock | MR-M1 Completed (`MR_CHANNELS`; the night walk taught lit posts). Prue at the memorial gardens (`MLL-D1`). |
| Length | 35–45 minutes |
| Combat share | ~20% (one held-ring encounter in three waves, one optional edge fight) |
| Skills | **Leatherworking ~[GD: low]**: re-stitch the split leather hood of Prue's lantern. Crew alternative: Prue sends it to the gardens' harness-mender overnight (keep watch to morning). Melee or Ranged (encounters). |
| Choice | Where the finished ring's lanterns are kept after (`MLL_PLACE`: ring / garden). |
| Outputs | **`MR_LANTERN_LINE` = true** (every completion path); `MLL_PLACE`; Stillgrave edge as a lit night place |
| **Anchor** | Chapel-Tenders (Prue); Stillgrave Hollow; the Haddow household. |
| **World-truth row** | None (present-day grief). |
| **Revelation role** | Self-contained. |
| **Recurring evidence** | None. |
| **State compliance** | Inactive → Active on `MLL-D1` accept; Completed on `MLL-D7` end. The ring always completes. Resume hook: Prue at the gardens (`MLL-B1.02`) or Ebba at Stillgrave by night (`MLL-B2.02`). |
| **Combat compliance** | Earthen Echoes (echo) to 0 HP; they collapse into mud and **re-form at the edge while the ring is unfinished** (condition, never health). Melee or ranged; ranged is natural across the lit ring, never required. |

### MLL.4 The places

**MAP VERIFICATION REQUIRED.** Stillgrave Hollow lies in the Blackwater (bible §4.2), reachable on foot along the peat edge from below Sorrowmere; Act II's MR-M3 gathers moss at "Stillgrave's near edge" by night on foot. MLL uses the same near edge and the bank just beyond it.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Memorial gardens** (Sorrowmere) | Offer; hood repair | Raised beds of white-flowered griefroot, small stones with marks, lantern posts. Prue's work shelf: wicks, a wax pot, a lantern with its leather hood split along the seam. |
| **B. Stillgrave near edge** (MP11) | Moss (night) | Water too clear; the reed edge; posts with lantern moss on their feet, glowing faintly when damp. Lantern light bends away from the surface (canon; `MLL-I1.02`). Reedlurker ripples. |
| **C. The Haddow ring** | Hold the line | A shelf of firm bank above the water. Three reed stakes in a half-circle with dead lanterns on them; three empty stake-holes that would close the ring. A trampled patch where someone knelt. A child's boot-print, filled with water. |
| **D. The wash stones** | Why | Flat stones at the water's edge, worn hollow in the middle. Tenders say the dead were washed here at the war's end; nobody living says they saw it. No marks, no names. |

### MLL.5 Player-facing sequence

**Beat 0 — Three nights (`S00_offer`).** *Objective: Ask the Tender about her lantern.* `MLL-D1`. Prue, the split hood, the Haddows. "I can bring a light. I can't keep it there."

**Beat 1 — The hood (`S01_hood`).** *Objective: Mend Prue's lantern hood.* **Leatherworking ~[GD: low]**: unpick the split seam, re-stitch (two 4 s channels; persist). **Crew alternative:** the gardens' harness-mender, overnight (`MLL-D1.20`; `MLL_HOOD = crew`).

**Beat 2 — Moss (`S02_moss`).** *Objective: Gather lantern moss at Stillgrave's edge after dark.* Keep watch to night if needed. Moss shows only where it glows (gather nodes visible only at night; by day the inspect reads "weed"). Gather four bunches from post feet (2 s each). **MLL-E1** (optional): Reedlurkers in the shallows by the far posts (ripple tell); the player can gather from the near posts only and skip them.

**Beat 3 — The ring (`S03_ring`).** *Objective: Find the Haddows at the ring.* `MLL-D2`. Ebba, Bryony, Dob, Prue. Inspect the half ring (`MLL-I2.01`), the kneeling patch, the boot-print. Bryony does not want to come near the water.

**Beat 4 — Why (`S04_why`).** *Objective: Ask why the Hollow holds grief.* `MLL-D3` at the wash stones: Ebba gives only what she has seen ("Seen: stones worn hollow, and nobody fishes here. Thought: the water keeps something. That's all I've got."); Prue gives the Tenders' saying that the dead were washed here at the war's end, labelled as belief. No count, no names. Inspect the wash stones (`MLL-I3.01`).

**Beat 5 — Light it (`S05_light`).** *Objective: Wick and light the ring's lanterns.* Moss wicks in the three dead lanterns (3 × 2 s), wax from Prue, light. With the mended hood on Prue's lantern, flame from it lights the others; they hold.

**Beat 6 — Finish it (`S06_finish`).** *Objective: Keep the ring lit while the family sets their stakes.* The set piece (MLL.6, **MLL-E2**). Three segments, one per Haddow, each an ordinary **hold objective**: the Haddow kneels to bed a stake and its lantern (a visible ~45 s progress bar); Echoes stand out of the grief at the water's edge and walk toward that stake's lantern; the player fights them at the ring's edge. The bar advances only while that lantern is lit (the standard capture-point rule); an Echo's swing can knock it out and the player relights it (2 s). When the bar fills, the Haddow stands and says what the stake is for (`MLL-D4`), the segment's Echoes collapse, and the next Haddow kneels. Lit lanterns slow Echoes that cross their light (a standard slow). Completed segments persist.

**Beat 7 — The light lies straight (`S07_straight`).** When Dob sets the last stake, **the strange moment** (MLL.7). The Echoes collapse and do not re-form.

**Beat 8 — After (`S08_ring`).** *Objective: Sit with the family.* `MLL-D5`. Ebba gives the player bread from her pocket. Choice (`MLL_PLACE`): leave the lanterns on the ring, lit by whichever Haddow comes on the night (**ring**), or take them to the memorial gardens, where Prue keeps them lit (**garden**). Quest Completed (`MLL-D7`). Sets `MR_LANTERN_LINE`.

### MLL.6 Encounters

Tuned for Competent identity (MD-10, after MR-M1).

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **MLL-E1** (optional) | 2 × Reedlurker (lurker), 1 × snapper | Far posts of the near edge, in the shallows | Ambush from water; leash to shallows. | **Reed-ripple:** a line of reeds bends toward the player (~1.5 s, the family's first-appearance length) before a lurker lunges 3 m from the water; step back from the edge. **Snapper spit:** head lifts out of the water, throat swells (~1.0 s), then a spit arc; sidestep. | Makes the edge a place; teaches the reed-ripple before MR-M2. Avoidable by gathering near. | 30–45 s; player at 70–90% HP. |
| **MLL-E2** | Earthen Echo (echo): wave 1: 2; wave 2: 3; wave 3: 3 + 1 that walks to Dob's lantern specifically | Stand up out of the mud at the water's edge, one per 3–4 s within a wave; walk a straight line toward the kneeling Haddow's lantern | Slow, relentless walkers that repeat one motion (kneeling, lifting, reaching) as they come; they walk to the kneeling Haddow's lantern, never at a person. Re-form at the edge 6 s after defeat while the segment lasts. | **Stand-up:** a hump of mud rises and holds (~1.5 s) before the figure stands; a ranged shot during the hold is a free hit. **Swing:** the figure stops, both arms lift (~1.2 s), then a wide downward swing (2 m arc) that knocks out a lantern if one is in the arc; step out. | The family finishing their ring is the work; the fight is the frame. The player protects people and light, not a point. | ~2.5–3.5 min across three speeches; player ends at 50–70% HP. Melee holds the ring edge; ranged picks walkers off across the lit ground. |

**Rules.** Echoes target lanterns, never people: an Echo that reaches the kneeling Haddow's stake swings at the lantern (the lit-gated bar pauses until it is relit). The Haddows and Prue are never targetable and never harmed. Echoes are defeated at 0 HP and collapse into mud; they re-form only while the ring is unfinished (bible §2.6). Nothing they leave advances the quest. A beaten player wakes at the memorial gardens with the ring's completed speeches kept.

**MD-7 swap note:** no Hollowfoot content. Nothing to swap.

### MLL.7 The strange moment: the light lies straight (Beat 7)

| Time | Element | Spec |
|---|---|---|
| 0 s | **The last stake** | Dob sets his stake (he insisted on going last), lights his lantern from the player's, and says his line (`MLL-D4.30`). |
| 0–2 s | **Collapse** | Every Echo in the ring folds into mud at once and lies flat. |
| 2–6 s | **The water** | All through the quest, lantern light has bent away from Stillgrave's surface (canon). Now the reflected ring of lanterns lies **straight** on the water: six clean points of light, still. |
| 6–10 s | **Bryony** | She walks down to the edge for the first time in the quest and looks at the water. Nobody speaks. |
| After | `MLL-D5` | Ebba: "Seen: it lies flat. Thought: I'm too old to have a thought." |
| Later visits | | By night with `MR_LANTERN_LINE`, the ring's light lies straight; anywhere else on Stillgrave light still bends. |
| What it means | | Never explained. The discovery MDS02 (Stillgrave's reflection) is owned by the discoveries package and is not touched. |

### MLL.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Ask the Tender about her lantern. | `MLL-D1` end with accept | Yes |
| `S01_hood` | Mend Prue's lantern hood. | 2 × `stitch_hood` **or** keep watch (crew) | Yes |
| `S02_moss` | Gather lantern moss at Stillgrave's edge after dark. | 4 × moss gather (night) | Yes |
| `S03_ring` | Find the Haddows at the ring. | `MLL-D2` end + ring inspect | Yes |
| `S04_why` | Ask why the Hollow holds grief. | `MLL-D3` end + wash-stone inspect | Yes |
| `S05_light` | Wick and light the ring's lanterns. | 3 × wick + light | Yes |
| `S06_finish` | Keep the ring lit while the family sets their stakes. | 3 hold segments complete (persist) | Yes |
| `S07_straight` | — | Strange moment presentation end | Yes |
| `S08_ring` | Sit with the family. | `MLL-D5` choice + `MLL-D7` end | Yes (→ Completed) |

### MLL.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `MLL_HOOD` = self / crew | `S01` | Prue bark |
| `MLL_PLACE` = ring / garden | `MLL-D5` | MLW opener (`MLW-D1.03`); post-quest barks |
| **`MR_LANTERN_LINE` = true** | `MLL-D7.01` (every path) | MR-M3 `MRC-B2.6`; MR-M4 `MCS-D1.06`; MR-M5 circle (`MBL-B7.12`) |

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Ring** — *"Leave them on the ring. Light them when you come."* | The lanterns stay on the bank. | The Haddows must walk to Stillgrave at night to light them; Bryony says she will, and does, not every night. | Night visits: the ring is sometimes lit, sometimes dark (per presentation day). Ebba bark. |
| **Garden** — *"Take them to the gardens. Prue will keep them."* | Prue hangs them on a post in the memorial gardens with Corin's name on a strip. | The ring on the bank is bare. Ebba minds a little: "It was out there he went." | The gardens' post is always lit. Prue bark. |

Both set `MR_LANTERN_LINE = true`; the Haddows come to Bannerline in both (Act III `MBL-B7.12`).

### MLL.10 Rewards, failure, co-op

| Reward | Type | Notes |
|---|---|---|
| **Lantern moss** | Knowledge | The player can gather lantern moss anywhere it grows at night; ordinary light source item per the economy pass [GD]. |
| **Prue's spare lantern** | Tool (functional) | "A Tender's covered lantern": an ordinary light source. Item pass [GD]. |
| Skill XP | Actions only [GD] | Leatherworking, Melee or Ranged. |
| *The Lantern That Would Not Go Out* | Story | After MR-M4 (`MLL-D7.04`). |

| Situation | Handling |
|---|---|
| Gathers by day | The nodes read "weed"; Prue/Rowan line on night. Keep watch. |
| Echo knocks out the kneeling Haddow's lantern | The bar stops (progress kept) until the player relights it. |
| Death during `S06` | Respawn at the memorial gardens; completed speeches persist; the family waits at the ring. |
| Walking away mid-ring | The family goes home; at the next night they are back at the ring, at the next speaker. |
| Fail state | None. |
| Co-op | Shared Echoes; credit to all. Each player's own ring progress drives speeches (fallback: host). The strange moment plays per player. |

### MLL.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| Night moss nodes | Systems | **No new runtime:** the nodes are a presentation-hour prop variant (night), the same world-state variant used for dusk Wraith timing (bible §9.4) and MEP's meal-hour signs. **Fallback:** nodes present at any hour during `S02`; Prue's line says the moss is easier to find after dark. |
| Lantern props (lit / out, relight) | Systems | Prop state with an interaction; Echo swing arc sets "out". |
| Lit radius slows Echoes | Systems | Standard slow debuff applied in a radius around a lit prop. **Fallback:** no slow; waves reduced by one. |
| Hold segments | Systems / NPC | Standard hold/capture objective: a timed bar that advances while a prop (the lantern) is lit; NPC kneel animation; dialogue node on bar complete. Replaces the first draft's "dialogue pauses while an enemy is near" (independent review 2026-11-09, CDR-4). |
| Straight reflection | Art / VFX | Per-player reflection swap on the ring's water. **Fallback:** inspect text. |
| Creatures | Encounters package (Batch 4) | Reedlurker lurker/snapper; Earthen Echo (echo). |

**Mystery ledger.**

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Why Stillgrave swallows light** | Unexplained (bible §7.5). | Grief in the water. | The bent light; the wash stones; the straight light after the ring. | The dead are in the water and want something. | **Yes, forever.** | Never. |

**Open decisions.** (1) The war-washing is [NEW] Tender belief only (Prue, `MLL-D3.03`); no canon source supports it, so nobody states it as seen. If the Director prefers no war-washing belief at all, Prue's line becomes "Tenders say still water holds grief longest", and only `MLL-D3.03` and the Area D note change. (2) MAP VERIFICATION REQUIRED for the ring's bank.

| Review finding | Revision |
|---|---|
| First draft had Echoes take the form of Corin. | Removed: Echoes repeat motions and never resemble a known person (dossier; bible §2.4). |
| Ebba's wash-stone line risked a count. | No number, no names. |
| Independent review (2026-11-09): Ebba "saw" war-washing as a girl, which states unsupported history as fact and makes a grandmother of a ten-year-old about forty. | Ebba gives only present sight; the washing is Prue's labelled Tender belief. |
| The straight light risked being read as "Corin is at peace". | Nobody interprets it; Ebba's line refuses a thought (§5.3 rule 3). |

### MLL.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Prue Calloway** [NEW], Chapel-Tender | Wax, wicks, rites, Tender belief. | Why the Hollow swallows light. | Brisk, pious, practical, a little cross with herself. |
| **Ebba Haddow** [NEW], eldest | Stillgrave as she has known it all her life. | Anything about the war here beyond what Tenders say. | Dry, short, kind; "Seen / thought". |
| **Bryony Haddow** [NEW] | Corin. | How to go near the water. | Quiet; says one true thing. |
| **Dob Haddow** [NEW], about ten | That he wants to go last. | — | Stubborn, brave in a small voice. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| MLL-B1.01 | Prue | Available | *"Three nights out and three nights dark. I'm a Tender. I'm meant to be good at this."* |
| MLL-B1.02 | Prue | Active, returns | *"Moss after dark, hood before you go. The family's waiting. They're good at it. Too good."* |
| MLL-B2.01 | Dob | Active, at the ring | *"I'm going last. I said."* |
| MLL-B2.02 | Ebba | Active, night, at the ring | *"We're here. We'll be here tomorrow too. Take your time. Don't take too long."* |
| MLL-B3.01 | Ebba | Completed, `ring` | *"Bryony lit it last night. On her own. I watched from the path."* |
| MLL-B3.02 | Prue | Completed, `garden` | *"Corin's lanterns. Never out. I've a girl sits with them when I'm on the roof."* |
| MLL-B3.03 | Dob | Completed | *"I set mine last. It was the one that made it go flat."* (Ebba: *"It wasn't."* Dob: *"It might have been."*) |

#### Nodes

```
MLL-D1 (memorial gardens; S00–S01)
MLL-D1.01 PRUE: (holding a lantern with its hood split) "Traveller. Three nights I've walked to Stillgrave with this. Three nights it's gone out at the water."
MLL-D1.02 PRUE: "The Haddows lost Corin in the spate. Reed-cutting at the Hollow. They started a ring for him. They stopped halfway."
MLL-D1.03 PRUE: "I can bring a light. I can't keep it there." (beat) "The hood's split. Damp gets the wick. That's the part I can fix. The rest I can't."
  > "I'll mend the hood."                                    → MLL-D1.10
  > "Is there someone who mends leather?"                    → MLL-D1.20
  > "What do you need for the rest?"                         → MLL-D1.30
MLL-D1.10 PRUE: "Thread's there. Close stitches. It's from away, that leather, it hates the wet more than we do."   {Leatherworking; MLL_HOOD = self; quest Active}
MLL-D1.20 PRUE: "The harness-mender by the gate. Overnight. He'll charge me in eel."   {keep watch; MLL_HOOD = crew; quest Active}
MLL-D1.30 PRUE: "Moss. Lantern moss off the post feet at the Hollow. Only shows after dark. Pick it by day and you'll pick weed."   → MLL-D1 options
```

```
MLL-D2 (the ring; S03)
MLL-D2.01 EBBA: (standing; Bryony behind her, Dob with a stake taller than he is) "Tender's brought somebody. Good. She needed somebody."
MLL-D2.02 EBBA: "Six stakes. One each, and one each for the things we wanted said. We got three in. Then it stood up."
  > "What stood up?"                                         → MLL-D2.03
MLL-D2.03 EBBA: "Seen: mud, where Bryony was kneeling. It stood up like a man getting off his knees. Thought: I've no thought. We went home."
MLL-D2.04 BRYONY: "I'm not going near the water." (beat) "I'll set mine from up here."
MLL-D2.05 DOB: "I'm going last."
```

```
MLL-D3 (wash stones; S04)
MLL-D3.01 EBBA: "You want to know why it's heavy here." (she sits on a stone) "Seen: these stones, worn hollow by somebody's hands. Nobody fishes the Hollow. Nobody ever has, in my time."
MLL-D3.02 EBBA: "Thought: the water keeps something. That's all I've got."
MLL-D3.03 PRUE: "Tenders say the dead were washed at these stones at the end of the war, and still water holds grief longest. That's what we say. I'm not saying it's so."
MLL-D3.04 PRUE: "What I know is a lit line holds ground. So we light it and we finish it."
```

```
MLL-D4 (the ring; S06; one line per segment, spoken when that segment's bar fills)
MLL-D4.10 EBBA: (sets her stake, lights it from the player's lantern) "For Corin, who carried my wood without being asked. That's mine."
MLL-D4.20 BRYONY: (from the bank, then, partway through, walking down to set it properly) "For Corin. I'm cross with you. I'll stop. Not yet."
MLL-D4.30 DOB: (last; it takes him two tries to get the stake in) "For my da. And for the reeds. He liked the reeds."
```

```
MLL-D5 (after; S08)
MLL-D5.01 EBBA: "Seen: it lies flat." (beat) "Thought: I'm too old to have a thought."
MLL-D5.02 EBBA: (takes bread from her coat; breaks it; hands the player half) "Eat. You held it."
MLL-D5.03 PRUE: "They're finished. Where do the lanterns live now?"
  > "Leave them on the ring. Light them when you come."      → MLL-D5.10  {set MLL_PLACE = ring}
  > "Take them to the gardens. Prue will keep them."         → MLL-D5.20  {set MLL_PLACE = garden}
MLL-D5.10 BRYONY: "I'll come." (beat) "Not every night."   → MLL-D7.01
MLL-D5.20 PRUE: "Always lit. I'll put his name on a strip." EBBA: "It was out here he went." (beat) "Gardens are nearer. Fine."   → MLL-D7.01
```

```
MLL-D7 (close)
MLL-D7.01 PRUE: "A family finished its ring. That's all a Tender's for, most days."   {set MR_LANTERN_LINE}
MLL-D7.02 EBBA: "If anyone ever needs a ring lit, they can send for the Haddows. We know how now."
MLL-D7.03 DOB: "And moss. I know the moss."
MLL-D7.04 [MR-M4 Completed] PRUE: "Mabyn's been asking for help on the roof. Something about an old book. Go when you can."
      {event: S08 → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| MLL-I1.01 | Lantern moss (night) | *"Pale green, glowing faintly where it's wet. It brightens when you breathe on it."* |
| MLL-I1.01d | Lantern moss (day) | *"Weed. Wet weed."* |
| MLL-I1.02 | Stillgrave surface | *"Too clear. Hold the lantern out and its light bends away from the water, as if the water didn't want it."* |
| MLL-I2.01 | The half ring | *"Three stakes in a half circle, each with a dead lantern. Three empty holes where the ring would close."* |
| MLL-I2.02 | Kneeling patch | *"Trampled reed, a hollow in the mud where someone knelt. The hollow is deeper than a knee makes."* |
| MLL-I3.01 | Wash stones | *"Flat stones at the water's edge, each worn hollow in the middle by a long time of use. No marks. Nothing written."* |

---

## MLW — The Lantern That Would Not Go Out

### MLW.1 The quest in one paragraph

On the chapel roof, **Mabyn Coyle** has found the Tenders' old **wax book** in a loft chest she thought held only wicks. Every Tender who kept the roof line wrote what wax they used, and what weather, every night. The pages from the end of the war cover the **seven-night lantern**: kept burning for seven nights after the last battle, rain or no. People call it a miracle, or a Memorywarden's last act. The book says peat-wax, a covered housing, and somebody not sleeping. Mabyn wants to build it again, properly, and wants help: a housing frame of root-knee, peat-wax rendered slow so it doesn't spit, moss wicks the Haddows send up from Stillgrave. The player reads the book, renders the wax at Mabyn's pot (Cooking), shapes the frame, and keeps the lantern lit for one wet night on the roof: trim the wick when it smokes, feed the wax when it sinks, shield it when the rain drives. At first light the player turns to the last of the seven nights in the book. Under the Tenders' entries, in a hand Mabyn does not know, one word: *"Kept."* Then the player chooses who keeps the new lantern.

**Remember:** one word in an unknown hand. **Want next:** Lifting Day, where the lantern stands at the end of the road.

### MLW.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| **A. The lantern was a miracle after all.** | Rejected. Bible: craft and stubbornness; belief stays belief. |
| **B. The book names the Tenders and the people they waited for.** | Rejected. R08 custody: no names of Memorywardens, no counts. |
| **C. Read → craft → one night's keeping → an unexplained signature → keeper choice** (selected). | **Selected.** Read, craft, keep (bible §7.1); supports R08 (the Tenders waited the same nights) without stating it. |

| Element | Source | Status |
|---|---|---|
| The Lantern That Would Not Go Out: seven nights, rain or no; Tenders protect the flame / a Memorywarden's final act | Dossier §XII.4 | [CANON myth] |
| Craft reading: peat-wax, covered housing, somebody awake | Bible §2.2; `MCS-D9.22` | [NEW] |
| The vestry log's last line, "The lantern on the roof is lit." | Act II §B8.4 | [NEW] |
| The weather run: rain, rain, rain, a hard frost, a thaw, fog, fog | Act I §B14.2; Act II §B14.3 | [NEW] |
| Mabyn Coyle; the roof loft; the Tenders' chest | Bible §5.2; Act II | [NEW] |
| The wax book, "Kept." | This package | [NEW] |

### MLW.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `mire.side.the_lantern_that_would_not_go_out` |
| Series | *Lanterns and Tenders*, part 2 of 3 |
| Type | Memory/lore |
| Unlock | MLL **and** MR-M4 Completed. Prue's line `MLL-D7.04`, or Mabyn on the roof on the next Chapel visit (`MLW-D1`). Reached by **Rowan's Chapel route** at Slack by day (`[MD-3]`: Rowan does not cross at night; the vigil is kept on the roof and the player returns at first light). |
| Length | 30–40 minutes |
| Combat share | 0% |
| Skills | **Cooking ~[GD: low]**: render peat-wax at Mabyn's pot (heat, skim, pour; a cooking interaction). **Woodcutting** (optional, no level): shape the root-knee frame. Crew alternatives: Mabyn renders the wax herself overnight; Rowan brings a frame cut at the landing. |
| Choice | Who keeps the new lantern (`MLW_KEEPER`: roof / gardens / landing). |
| Outputs | `MLW_KEEPER`; the seven-night lantern as a world prop at its keeper's place |
| **Anchor** | Chapel-Tenders (Mabyn). |
| **World-truth row** | H17 (the cost of the last battle, as the Tenders lived it). |
| **Revelation role** | **Supports R08**: the Tenders lit the roof for people who went out on the same weather run the vestry log and the day-books record. States no name, no army, no number. |
| **Recurring evidence** | **The Tenders' wax book** (Mabyn's loft; read in place). Its weather run matches the vestry log and the day-books (a third custodian of the day; never required). |
| **State compliance** | Inactive → Active on `MLW-D1` accept; Completed on `MLW-D6` end. The flame can gutter and be relit; nothing fails. Resume hook: Mabyn on the roof (`MLW-B1.02`). |
| **Combat compliance** | None. The roof is lit; Chapel Shades are an interior hazard and do not reach it. |

### MLW.4 The places

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. The roof** (MP13) | Offer; vigil | The roof lantern line from Act II, lit. A flat leaded stretch by the bell-cote where Mabyn sits. A rain-shield of reed hurdle. The black water of the Blackwater all round. |
| **B. The roof loft** | Wax book; wax pot | Under the roof's ridge: the Tenders' chest (`MCS-I1.04`), a peat stove with a wax pot, wicks drying on a string. With `MR_WARDEN_RECORD = tenders`, the Warden leaves' chest is pegged beside it; Mabyn keeps the two apart ("Ours and not ours."). |
| **C. The landing** (MP06) | Delivery | Rowan's boat; moss from the Haddows in a jar (`MLL_PLACE` either). |

### MLW.5 Player-facing sequence

**Beat 0 — The book (`S00_offer`).** *Objective: Ask Mabyn about the old book.* `MLW-D1`. With `MCS_TOLD_MABYN_LANTERN`, she opens with the vestry log's last line (`MLW-D1.02`).

**Beat 1 — Read it (`S01_read`).** *Objective: Read the wax book's war pages.* Four required inspects (`MLW-I1.01`–`.04`): the ordinary nights (wax, weather, "line lit"); the weather run (*rain, rain, rain, hard frost, thaw, fog*) and on the second fog: *"They went out from under us at the turn of the light. Lit the roof for them."*; the following nights, one per page (fog, rain, rain, wind, rain), each *"Kept it for the ones out."* with wax used and the Tender's mark; and the seventh page, which the player is told to leave until morning (Mabyn closes the book on it: "Last one when we've done ours.").

**Beat 2 — Wax (`S02_wax`).** *Objective: Render peat-wax.* **Cooking ~[GD: low]**: at the loft stove, three stages (heat until it runs, skim the peat grit, pour into the mould) as the ordinary cooking interaction with a wax recipe. A failed stage spits (small burn, cosmetic) and is repeated. **Crew alternative:** Mabyn does it overnight; the player keeps watch (`MLW_WAX = crew`).

**Beat 3 — Frame (`S03_frame`).** *Objective: Build the lantern housing.* Shape a root-knee frame (Woodcutting interaction, two 3 s channels) **or** take the frame Rowan cut at the landing (ride to the landing and back at Slack). Fit Prue's pattern hood (from MLL; the player knows the stitch), the moss wicks from the Haddows (delivered with Rowan: `MLW-B2.01`), and the wax. One assembly interaction.

**Beat 4 — Keep it (`S04_vigil`).** *Objective: Keep the lantern lit until first light.* The night on the roof (pinned rain), as four **keep-watch** turns. At each turn the lantern shows one readable need, untimed: **smoke** (the flame low and smoking: *Trim*), **sink** (the wax pool below the wick: *Feed*), or **rain hissing on the reed hurdle** (*Shield*). The player picks the matching interaction (2 s channel), then keeps watch to the next turn. A wrong pick does no harm: the flame gutters and the player relights it (2 s) and tries again (the bible's interact-sequence-with-harmless-reset). Mabyn talks between turns (`MLW-D3`). Nothing fails. The fourth turn ends at first light.

**Beat 5 — The seventh night (`S05_kept`).** *Objective: Read the last page.* **The strange moment** (MLW.7).

**Beat 6 — Who keeps it (`S06_keeper`).** *Objective: Decide who keeps the lantern.* Rowan's boat comes out of the grey (`MLW-D5`). Choice (`MLW_KEEPER`): **roof** (Mabyn keeps it on the bell-cote; the line has a lantern that is never trimmed by the wind), **gardens** (taken to Sorrowmere's memorial gardens, lit on Lifting Day and on burial nights), or **landing** (Rowan's landing, for whoever is out on the water). Quest Completed (`MLW-D6`).

### MLW.6 Encounters

None. **MD-7 swap note:** no Hollowfoot content. **MD-4:** the nave is not entered.

### MLW.7 The strange moment: "Kept." (Beat 5)

| Time | Element | Spec |
|---|---|---|
| 0 s | **First light** | Grey on the water. The player's lantern is lit (or relit). Mabyn opens the book at the seventh page. |
| 0–4 s | **The Tenders' entry** | *"Seventh night. Wax done. Kept it on the last stub. No more out."* with the Tender's mark. |
| 4–8 s | **Below it** | In a different hand, square and pressed hard, one word: *"Kept."* No mark. |
| 8 s | **Mabyn** | `MLW-D4.02`: "That's not one of ours. I know every hand in this book. I learned them." (beat) "Seen: a word. Thought: somebody else was awake." |
| After | | Nobody explains it. The player can inspect it again any time (`MLW-I1.05`). |
| What it means | | Unknown. It is not a hold, not a name, and not a Memorywarden's mark (Mabyn knows office marks from the leaves and says it is not one). Belief stays belief; Mabyn declines to make it a miracle. |

### MLW.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Ask Mabyn about the old book. | `MLW-D1` end with accept | Yes |
| `S01_read` | Read the wax book's war pages. | 4 inspects | Yes |
| `S02_wax` | Render peat-wax. | Cooking interaction **or** keep watch (crew) | Yes |
| `S03_frame` | Build the lantern housing. | Frame (shape or fetch) + assembly | Yes |
| `S04_vigil` | Keep the lantern lit until first light. | Vigil sequence end (first light) | Yes |
| `S05_kept` | Read the last page. | `MLW-I1.05` + `MLW-D4` end | Yes |
| `S06_keeper` | Decide who keeps the lantern. | `MLW-D5` choice + `MLW-D6` end | Yes (→ Completed) |

### MLW.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `MLW_WAX` = self / crew | `S02` | Mabyn bark |
| `MLW_GUTTERED` (count, presentation) | `S04` | `MLW-D3.20` variant ("You lost it twice. I lose it most nights.") |
| `MLW_KEEPER` = roof / gardens / landing | `MLW-D5` | MLD (where the lantern stands); barks |

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Roof** | On the bell-cote. | Seen only by people Rowan brings. | Mabyn: "It'll be lit when you come. Always." Night travel past the Chapel shows it. |
| **Gardens** | Prue takes it at Sorrowmere. | Mabyn keeps the old line without it. | MLD: it stands at the causeway's Sorrowmere end. |
| **Landing** | Rowan hangs it on the dock post. | Rowan has to keep it. He says "Hm." | Kept: visible from Bannerline's crown on the MR-M5 night only as Act III authors it (its own landing lantern; no change requested). MLD: Rowan brings it to the table. |

### MLW.10 Rewards, failure, co-op

| Reward | Type | Notes |
|---|---|---|
| **Peat-wax** | Knowledge (recipe) | A cooking recipe for lantern fuel per the economy pass [GD]. |
| **A Tender's thanks** | Standing | Mabyn's roof as a rest point. |
| Skill XP | Actions only [GD] | Cooking, Woodcutting. |
| *Lifting Day* | Story | `MLW-D6.03`. |

| Situation | Handling |
|---|---|
| Wrong tending pick | Flame gutters; relight; pick again. |
| Logout during the vigil | Resume at dusk on the roof, vigil restarted (short). |
| Arrives by night | Rowan won't cross; keep watch at the landing (`[MD-3]`). |
| Walking away | Stays Active; Mabyn waits. |
| Fail state | None. |
| Co-op | Each player keeps their own lantern prop (two lanterns on the roof); turns per player. Choice per player (fallback: host's keeper prop). |

### MLW.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| Tending turns | Systems | **No new runtime:** four keep-watch turns; at each, the lantern prop shows one of three states (smoke / sink / hiss) and offers three interactions; a wrong one sets the prop "out" with a relight interaction. Replaces the first draft's timed prompt windows (independent review 2026-11-09, CDR-4). |
| Cooking recipe: peat-wax | Economy pass | Proposal only (bible MD-11). **Fallback:** generic cooking interaction producing a carry-state cake. |
| Pinned rain on the roof | Systems | Per-player presentation weather (Lowmark keep-watch convention). |

**Mystery ledger.**

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The seven-night lantern** | Tenders kept it lit for people who went out on the last day and did not come back (R08 context). | A miracle; a Memorywarden's last act. | Wax book; vestry log line; Mabyn. | It was magic. | — | MLW (craft reading); R08 (MR-M4). |
| **"Kept."** | Unknown. | — | One word. | A ghost wrote it. | **Yes, forever.** | Never. |

**Open decisions.** Add "Kept." to the bible's §7.5 deliberately unexplained list (request).

| Review finding | Revision |
|---|---|
| The war pages first gave how many came back. | "No more out" only; no figure. |
| "Kept." risked reading as a Memorywarden's office mark. | Mabyn, who has seen the leaves, says it is not one. |

### MLW.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Mabyn Coyle** [NEW, bible] | Every hand in the wax book; the craft. | Who wrote "Kept." | Religious, practical, warm, bossy; never claims a miracle. |
| **Rowan Mirewake** [CANON] | The landing; the light. | — | Few words. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| MLW-B1.01 | Mabyn | Available | *"There's a book in my chest I've never read past the first page. Come up."* |
| MLW-B1.02 | Mabyn | Active, returns | *"Wax, frame, then the night. I've the tea."* |
| MLW-B2.01 | Rowan | Moss delivery | *"Haddow boy sent moss. Said to say he picked it himself. He did."* |
| MLW-B3.01 | Mabyn | Completed, `roof` | *"Your lantern's on the cote. It hasn't gone out. I've been watching it like a child."* |
| MLW-B3.02 | Rowan | Completed, `landing` | *"Lamp's lit." (beat) "It's a good lamp."* |

#### Nodes

```
MLW-D1 (the roof; S00)
MLW-D1.01 MABYN: (a ledger in oilcloth on her knees) "Sit. Tea first." (beat) "This was in the chest under the wicks. Every Tender who kept the line. Every night. Wax and weather."
MLW-D1.02 [MCS_TOLD_MABYN_LANTERN] MABYN: "You told me the soldier's last line. 'The lantern on the roof is lit.' I've been turning it over since."
MLW-D1.03 [MLL_PLACE set] MABYN: "Prue says you finished the Haddows' ring. Then you know what a light's for."
MLW-D1.04 MABYN: "The seven nights are in here. I want to build it again. Properly. Help me."
  > "Show me the book."                                      → MLW-D1.10
  > "Not now."                                               → MLW-D1.20
MLW-D1.10 MABYN: "Gently. It's older than me and in worse shape."   {quest Active}
MLW-D1.20 MABYN: "It's waited thirty years. It'll wait. I won't, much."   {Inactive}
```

```
MLW-D2 (after reading; S01)
MLW-D2.01 MABYN: "Rain, rain, rain, a frost, a thaw, fog." (beat) "Same as the soldier's log. Same as Ysolde's books." [MR-M2 Completed]
MLW-D2.02 MABYN: "'They went out from under us at the turn of the light. Lit the roof for them.'" (beat) "Not 'for the dead'. For them. Out."
MLW-D2.03 MABYN: "Wax every night. Two cakes, three, three, the wind night four. Somebody was feeding it." (she closes the book on the last page) "Last one when we've done ours."
```

```
MLW-D3 (vigil; S04; lines between turns)
MLW-D3.01 MABYN: "Smoke means trim. Sink means feed. Hiss means it's coming, get your hand up."
MLW-D3.10 MABYN: "People say it never went out. I think it went out every night. Somebody lit it again before anybody saw."
MLW-D3.20 [MLW_GUTTERED >= 1] MABYN: "You lost it. I lose it most nights. Light it."
MLW-D3.30 MABYN: "I'm not praying for a miracle. I'm praying I stay awake."
```

```
MLW-D4 (first light; S05)
MLW-D4.01 MABYN: (opens the last page) "Seventh night."
MLW-D4.02 [after MLW-I1.05] MABYN: "That's not one of ours. I know every hand in this book. I learned them."
MLW-D4.03 MABYN: "Seen: a word. Thought: somebody else was awake." (beat) "That's all I'll say. That's all there is."
```

```
MLW-D5 (Rowan's boat in the grey; S06)
MLW-D5.01 ROWAN: (looking at the lantern) "Lit."
MLW-D5.02 MABYN: "It's yours. You sat with it. Where does it live?"
  > "Here. On the cote."                                     → MLW-D5.10  {set MLW_KEEPER = roof}
  > "Sorrowmere. The gardens. Where people walk."            → MLW-D5.20  {set MLW_KEEPER = gardens}
  > "The landing. For whoever's out on the water."           → MLW-D5.30  {set MLW_KEEPER = landing}
MLW-D5.10 MABYN: "Then I'll keep it with the line. Thank you."
MLW-D5.20 MABYN: "Prue'll fuss over it. Good. It deserves fussing."
MLW-D5.30 ROWAN: "Hm." (beat) "I'll keep it."
```

```
MLW-D6 (close)
MLW-D6.01 MABYN: "Not a miracle. A lantern and people who didn't sleep. I'd rather that."
MLW-D6.02 MABYN: (writes in the wax book, a new page) "Wax: three. Weather: rain. Kept it with a stranger."
MLW-D6.03 MABYN: "When the first dry comes, Sorrowmere walks the causeway. Lifting Day. Go. Eat. Walk slow."
      {event: S06 → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| MLW-I1.01 | Wax book, ordinary nights | *"'Wax: one. Weather: rain. Line lit.' Night after night, a dozen hands."* |
| MLW-I1.02 | The run | *"'Rain.' 'Rain.' 'Rain.' 'Hard frost.' 'Thaw.' 'Fog.' Then: 'Fog. They went out from under us at the turn of the light. Lit the roof for them.'"* |
| MLW-I1.03 | The following nights | *"One page a night. Fog, rain, rain, wind, rain. 'Kept it for the ones out.' Wax used, more each night. A Tender's mark."* |
| MLW-I1.04 | The wind night (the fifth) | *"'Wind. Housing cracked. Held it with my coat. Kept it.'"* |
| MLW-I1.05 | The seventh night | *"'Seventh night. Wax done. Kept it on the last stub. No more out.' Below it, in a square hand pressed hard into the paper, unlike any other on any page: 'Kept.'"* |

---

## MLD — Lifting Day

### MLD.1 The quest in one paragraph

The first dry stretch comes: three days without rain in the long wet. Sorrowmere holds **lifting day**: a repaired way is walked at ordinary pace, children carry harmless work signs, and households eat before remembrance. This year the way is the **Standards Causeway**, relaid by Oswin Garvey's crews across the Field of Fallen Standards and reset after the banners came down `[CAUSEWAY]`. Corra Sallis is organising the children and their signs. **Oswin** wants his crews to walk it first: they laid every log. **Edris** wants it walked last by him, behind everyone, "so he sees what he carried". The player cooks for the long table, helps Corra's children with their signs, and settles the order of walkers with Oswin and Edris. Then the walk: the player leads the children's line out along the causeway at walking pace (no overtaking) to the field's centre turnout and back, past the pale holes where standards stood. Beetles stir in the ditch at the turnout when one child is frightened; they can be fought or simply walked past. As the last walker steps off the causeway, every crew stake along the road shows the ochre band at once: the whole way Slack, end to end, which nobody has seen since spring. Then the table, then remembrance.

**Remember:** a row of stakes all showing the same colour at once. **Want next:** Bannerline, where Oswin will stand where he stands.

### MLD.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| **A. The player decides the causeway was wrong.** | Rejected. Not a hearing; a celebration (Part 3). The dispute is about who walks when. |
| **B. A festival with no work.** | Rejected. A festival you work (Thornfell TRR precedent, varied: cooking, escort, a settlement). |
| **C. Cook → signs → settle the order → walk → stakes → table** (selected). | **Selected.** Carry, cook, celebrate (bible §7.1). |

| Element | Source | Status |
|---|---|---|
| Lifting day: first reliable dry stretch; repaired route walked at ordinary pace; children carry harmless work signs; households eat before formal remembrance; celebrates returns, births, apprentices as well as the dead | Part 3 Mire proposal; bible MD-5 | [NEW, Part 3] |
| Oswin's causeway; Edris's objection | Bible §2.3, §3.1 | [NEW] `[CAUSEWAY]` |
| Corra Sallis, Bannerbearers, mood banners | Bible §5.2, MME01 | [NEW] |
| Griefbit beetles swarm where fear rises | Dossier §IX | [CANON] |
| Lantern walk: nobody overtakes | Bible MME03 | [NEW] |

### MLD.3 Summary card

| Field | Value |
|---|---|
| Suggested content id | `mire.side.lifting_day` |
| Series | *Lanterns and Tenders*, part 3 of 3 |
| Type | Festival |
| Unlock | MLW **and** MR-M2 Completed (`MR_CAUSEWAY = reset`). Offered by Corra on the raised way (`MLD-D1`). Playable before or after MR-M5. |
| Length | 30–40 minutes |
| Combat share | 0–5% (optional) |
| Skills | **Cooking ~[GD: low]**: a pot of root-and-fowl stew for the long table (economy pass names). Crew alternative: the player carries pots for Agna Ferrow's kitchen (three carry-deposits); costs one presentation hour. Melee or Ranged (optional skirmish). |
| Choice | The order of walkers (`MLD_ORDER`: first / last / together). |
| Outputs | ***Lifting Day* Completed** (read by MR-M5); `MLD_ORDER` |
| **Anchor** | Reedsward crews (Oswin) `[CAUSEWAY]`; Bannerbearers (Corra); Edris; Sorrowmere households. |
| **World-truth row** | None. |
| **Revelation role** | Self-contained. |
| **Recurring evidence** | None. |
| **State compliance** | Inactive → Active on `MLD-D1` accept; Completed on `MLD-D6` end. The celebration completes on walking the way. Resume hook: Corra (`MLD-B1.02`). |
| **Combat compliance** | Griefbit beetles (swarm), optional skirmish, to 0 HP. Avoidable by walking on: the swarm stays in the ditch. |

### MLD.4 The places

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Sorrowmere long table** (MP01) | Cooking; table | Trestles down the raised way. Mood banners changed to green (MME01). Agna Ferrow commanding pots. |
| **B. Causeway, Sorrowmere end** (MP08) | Order; start | Crew stakes; the first logs; with `MLW_KEEPER = gardens`, the seven-night lantern on a post. |
| **C. The causeway** | Walk | Logs pinned with root-knee pins (MR-M2); pale holes in the peat where standards stood; lantern moss on post feet. With `MBR_PINS = self`, one post has the player's pins (`MLD-I1.02`). |
| **D. The centre turnout** | Turn; skirmish | The platform where the Banner That Sank Twice rose (MR-M2). Still black water. A ditch below the road. |

**MAP VERIFICATION REQUIRED** for the turnout's distance from Sorrowmere (the walk should take about three minutes each way at walking pace).

### MLD.5 Player-facing sequence

**Beat 0 — The dry (`S00_offer`).** *Objective: Ask Corra about lifting day.* `MLD-D1`. Weather is pinned dry for this player while the quest is Active (presentation only).

**Beat 1 — The pot (`S01_pot`).** *Objective: Make something for the long table.* **Cooking ~[GD: low]**: stew at a table hearth (ordinary cooking interaction; ingredients from Agna's baskets, carry-state). **Crew alternative:** carry three pots from Agna's kitchen to the table (`MLD_POT = crew`). Agna tastes it either way (`MLD-D2`).

**Beat 2 — Signs (`S02_signs`).** *Objective: Help the children with their work signs.* At Corra's bench: three children each want a sign (a reed spade, a painted stake band, a peg-knife). Give each the sign that matches what their household does (three short dialogue picks; a wrong pick gets a giggle and a retry). With `MEP_HOME`, Posy Keel brings her own peg-knife and Lew walks with the returns.

**Beat 3 — The order (`S03_order`).** *Objective: Settle who walks first and last.* `MLD-D3` `[CAUSEWAY]`: Oswin and Edris at the causeway end, Corra between them. Choice (`MLD_ORDER`): **first** (Oswin's crews walk first, the work shown), **last** (Oswin walks last, alone, behind the households, as Edris asks), **together** (Edris and Oswin walk last together). Neither is wrong.

**Beat 4 — The walk (`S04_walk`).** *Objective: Lead the children's line to the turnout and back. Walk; don't run.* A standard group follow: the player leads and the line follows; the causeway is a walk-only volume for the player while `S04` is active (run disabled), so nobody overtakes (a child calls "No overtaking!" at the start, MME03). Inspects along the way (optional): the pale holes (`MLD-I1.01`), the player's pins. At the turnout, a child is frightened by the black water and **MLD-E1** (optional) rises in the ditch below. It is leashed to the ditch and attacks only a player who enters the ditch or strikes it; otherwise it is scenery. The player calms the child (dialogue: *"Look at the stake. Ochre. It's holding."*) and the line turns. Fighting the swarm first is allowed and changes only the child's line. The walk back.

**Beat 5 — Slack (`S05_slack`).** As the last walker (per `MLD_ORDER`) steps off the causeway: **the wonder moment** (MLD.7).

**Beat 6 — The table (`S06_table`).** *Objective: Eat. Then stay for remembrance.* Sit (forced seat). Table barks (`MLD-B3`); returns are toasted first (Lew with `MEP_HOME`; the Haddows; new apprentices; a birth). Then Ysolde reads the remembrance (`MLD-D5`): a short list of the year's dead from the register, Corin Haddow among them with `MR_LANTERN_LINE`; with `MR_NAME_RECORD = amended`, Aldith Hayle "held probable". Quest Completed (`MLD-D6`).

### MLD.6 Encounters

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **MLD-E1** (optional) | 2 × Griefbit Beetle swarm | The ditch below the centre turnout | Rise and mill toward the frightened child, stopping at the road edge; leashed to the ditch; aggro only if the player enters the ditch or attacks. | **Swarm surge:** the cloud thickens and clicks loudly (~1.2 s), then a 3 m dash; step aside. **Spread:** the cloud flattens on the ground (~1.5 s) before biting in a 2 m circle; leave it. | Shows that beetles follow fear, on a day without fear; the calm option is the better one. | 20–35 s; player at 80–95% HP. |

**Rules.** Beetles fight to 0 HP if fought (CDR-1). Calming the child is the step's objective; the swarm is never driven off or calmed by it and stays in the ditch, unengaged, like ambient flocks (rulings §3.1.4). Children and NPCs are never targetable; the swarm never reaches the road while the player is on it. **MD-7 swap note:** no Hollowfoot content.

### MLD.7 The wonder moment: Slack end to end (Beat 5)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Last step** | The last walker steps off the final log onto Sorrowmere's boards. |
| 0–6 s | **The stakes** | Along the causeway, every crew stake, one after another from the far end to the near, shows the water at the **ochre** band. The whole way Slack. |
| 6 s | **Oswin** | `MLD-D4.01` `[CAUSEWAY]`: "That's not happened since spring. Not once. Not end to end." |
| After | | Edris: "The water's slack. That's all it is." (beat) "It's enough." |
| What it means | | Water. The day was dry for three days. It is wonder because it is ordinary and has not happened all season. |

### MLD.8 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Ask Corra about lifting day. | `MLD-D1` end with accept | Yes |
| `S01_pot` | Make something for the long table. | Cooking interaction **or** 3 carry-deposits + `MLD-D2` end | Yes |
| `S02_signs` | Help the children with their work signs. | 3 correct sign picks | Yes |
| `S03_order` | Settle who walks first and last. | `MLD-D3` choice | Yes |
| `S04_walk` | Lead the children's line to the turnout and back. | Escort to turnout + calm dialogue + escort back (MLD-E1 optional, never required) | Yes |
| `S05_slack` | — | Wonder-moment presentation end + `MLD-D4` | Yes |
| `S06_table` | Eat. Then stay for remembrance. | Sit + `MLD-D5` end + `MLD-D6` end | Yes (→ Completed) |

### MLD.9 Flags, choices and consequences

| Flag | Set by | Read by |
|---|---|---|
| `MLD_POT` = self / crew | `S01` | Agna bark |
| `MLD_ORDER` = first / last / together | `MLD-D3` | Sorrowmere barks; **request** to Act III (below) |
| ***Lifting Day* Completed** | `S06` | MR-M5 (`MBL-B7.1a`, `MBL-B9.4`) |

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **First** — *"Crews first. They laid it."* `[CAUSEWAY]` | Oswin's crews lead, pins on their belts. | Edris walks with the households and says nothing all the way. | MR-M5: Oswin at Edris's shoulder (completion). |
| **Last** — *"Oswin last. Behind everybody."* `[CAUSEWAY]` | Oswin walks alone at the back. | Oswin's crew mutter; he tells them to stop. | Same. Oswin: "She was right. You see it from the back." |
| **Together** — *"Both of you. Last. Together."* `[CAUSEWAY]` | Edris and Oswin walk last side by side, not talking, then talking. | Neither gets what they asked for. | Same. |

All three complete *Lifting Day*; MR-M5 reads completion only. Act III already gates its meal line by `MLD_ORDER` (`MBL-B9.4` with `last` / `together`; `MBL-B9.4b` with `first`); no request remains.

### MLD.10 Rewards, failure, co-op

| Reward | Type | Notes |
|---|---|---|
| **The long table** | Rest / food | A cooked food item at the table [GD]. |
| **Lifting-day sign** | Cosmetic (functional name) | "A child's work sign", a carry-state memento; item pass may make it a keepsake [GD]. |
| Skill XP | Actions only [GD] | Cooking, Melee or Ranged. |

| Situation | Handling |
|---|---|
| Tries to run | Run is disabled on the causeway during `S04`; walking only. |
| Death at the turnout | Respawn at Sorrowmere; the line waits at the turnout. |
| Walking away | Stays Active; dry weather pin persists; resume with Corra (`MLD-B1.02`). |
| Fail state | None. |
| Co-op | One line follows the leading player (fallback: host). Each player's own `MLD_ORDER` drives their own walkers' order (fallback: host's). Beetles shared. |

### MLD.11 Integration needs, ledger, open decisions, review

| Need | Owner | Minimum viable form |
|---|---|---|
| Group escort | NPC / Systems | **Standard** group follow with the player's run disabled in the causeway volume during `S04` (the first draft's pace-matching pause was dropped in independent review 2026-11-09, CDR-4). |
| Per-player pinned dry weather | Systems | Presentation-weather pin (as MLW's rain pin). |
| Sequential stake water-line swap | Systems / Art | Channel stake props set to Slack in sequence (N-1 fallback: quest-pinned states). |
| Ditch-leashed swarm | Encounters | Ordinary leash and aggro-on-attack/enter; no settle state (the first draft's dialogue-driven "settle" read as a drive-off and was removed). |

**Mystery ledger.** None.
**Open decisions.** (1) Season: the dry stretch is a per-player pin; Act III's "the long wet continues" stands as world presentation.

| Review finding | Revision |
|---|---|
| First draft had Oswin apologise publicly. | He did that in MR-M2. Here the order is the gesture; nobody makes a speech. |
| The beetle fight was required. | Optional, with a calm option that is the better one. |

### MLD.12 Dialogue

#### Cast notes

| Speaker | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Corra Sallis** | Every child's household, every sign. | — | Earnest, organising, delighted. |
| **Oswin Garvey** `[CAUSEWAY]` | Every log. | That walking last is a gift. | Tired, decent, defensive. |
| **Edris Hollowmere** | Why it should have waited. | — | Plain, heavy, kind. |
| **Agna Ferrow** | Food. | — | "Sit. Eat." |
| **Ysolde Haverel** | The year's register. | — | Precise. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| MLD-B1.01 | Corra | Available | *"Three dry days! Lifting day! I've forty children and thirty signs!"* |
| MLD-B1.02 | Corra | Active, returns | *"Signs, pot, order, walk. In that order. Mostly."* |
| MLD-B2.01 | Child | Walk | *"No overtaking!"* |
| MLD-B2.02 | Child | Walk, pale hole | *"That's where one stood up. My da says."* |
| MLD-B3.01 | Agna | Table, `MLD_POT = self` | *"Salty. Good. People cry, they want salt."* |
| MLD-B3.02 | Lew Keel | Table, `MEP_HOME` | *"Toasted for coming home. I've been home a month."* |
| MLD-B3.03 | Ebba Haddow | Table, `MR_LANTERN_LINE` | *"Returns first. Then Corin. That's right. That's the order."* |
| MLD-B3.04 | Oswin `[CAUSEWAY]` | Table, `last` | *"You see it from the back. All of it. She was right."* |

#### Nodes

```
MLD-D1 (raised way; S00)
MLD-D1.01 CORRA: (a bundle of signs under one arm) "Witness! Three dry days. Lifting day. Will you help? Please. Say yes."
MLD-D1.02 CORRA: "We walk the causeway. Slow, nobody overtakes. Children carry work signs. Then we eat. Then we remember. In that order. Eating first."
MLD-D1.03 [MR_BANNERS = restored] CORRA: "I'm not carrying the banner. It's a work day, not a banner day. Calwen says."
MLD-D1.04 CORRA: "And Oswin and Edris are both standing at the causeway end and not speaking. Again."
  > "Yes."                                                   → MLD-D1.10
  > "Not now."                                               → MLD-D1.20
MLD-D1.10 CORRA: "Agna needs a pot. Then signs. Then those two."   {quest Active; weather pin dry}
MLD-D1.20 CORRA: "It's dry for three days. Two now. Hurry. Not too much."   {Inactive}
```

```
MLD-D2 (table; S01)
MLD-D2.01 AGNA: (tasting) "It'll do. Sit later. Not now. Carry that."
```

```
MLD-D3 (causeway end; S03) [CAUSEWAY]
MLD-D3.01 OSWIN: "My crews laid every log of it. In the wet. They should walk it first. Let them be seen."
MLD-D3.02 EDRIS: "He should walk it last. Behind all of us. So he sees what he carried."
MLD-D3.03 OSWIN: "I see it every day."
MLD-D3.04 EDRIS: "From the front."
MLD-D3.05 CORRA: (to the player, very quietly) "You're the witness. Somebody has to say."
  > "Crews first. They laid it."                             → MLD-D3.10  {set MLD_ORDER = first}
  > "Oswin last. Behind everybody."                          → MLD-D3.20  {set MLD_ORDER = last}
  > "Both of you. Last. Together."                           → MLD-D3.30  {set MLD_ORDER = together}
MLD-D3.10 EDRIS: "Fine." (she isn't, and walks with the households)
MLD-D3.20 OSWIN: (a long breath) "...Last." (beat) "Fine."
MLD-D3.30 EDRIS: "Together." OSWIN: "Together." (neither looks at the other)
```

```
MLD-D4 (the stakes; S05) [CAUSEWAY]
MLD-D4.01 OSWIN: "That's not happened since spring. Not once. Not end to end."
MLD-D4.02 EDRIS: "The water's slack. That's all it is." (beat) "It's enough."
```

```
MLD-D5 (remembrance; S06)
MLD-D5.01 YSOLDE: "We've eaten. Now we remember. Returns, then births, then the ones we hold."
MLD-D5.02 [MEP_HOME] YSOLDE: "Lew Keel, home from the root-timber."
MLD-D5.03 YSOLDE: "A girl to the Basks, in the ochre week. An apprentice to the Reedsward crew."
MLD-D5.04 [MR_LANTERN_LINE] YSOLDE: "Corin Haddow, in the spate. His ring is finished."
MLD-D5.05 [MR_NAME_RECORD = amended] YSOLDE: "Aldith Hayle of Marshfall. Held probable."
MLD-D5.06 YSOLDE: "And the ones we hold, not yet known." (beat) "That's all of them. That's this year."
```

```
MLD-D6 (close)
MLD-D6.01 AGNA: "Now eat the rest."
MLD-D6.02 CORRA: "Next year I'm carrying a real one." (beat) "A sign. A real sign."
      {event: S06 → quest Completed (Lifting Day Completed)}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| MLD-I1.01 | Pale hole | *"A round pale scar in the peat by the road, where a standard stood. Grass is starting at the edge."* |
| MLD-I1.02 | Pinned post (`MBR_PINS = self`) | *"Root-knee pins, split a little crooked. Yours. Holding."* |
| MLD-I1.03 | Crew stake (after S05) | *"Water at the ochre band. Slack."* |

---

## Package review log (cross-quest)

| Check | Result |
|---|---|
| Bible §7.1 slate rows | All six quests match code, series part, type, unlock, place, core verb and feed. MBA and MEP add minor places (the Rudd house; the root-timber lot) inside the bible's subzones. |
| §7.3 contracts | Each card carries the six fields as the bible lists them. MLW's world-truth row H17 and R08 support kept without names or counts. |
| Flags for the mains | `MR_STRANGER_SEAT` (bool, MSS), `MR_LANTERN_LINE` (bool, MLL), *Lifting Day* Completed (MLD), as Act III's input table reads them. `MR_ARRIVALS` (named / held) for CV-M3. No other `MR_` flag set. |
| Stillgrave family role names | The Haddow household: Ebba (eldest, speaker of `MBL-B7.12` and `MRC-B2.6`), Bryony, Dob. |
| §7.6 Register | The Brede arrival: Book of Arrivals entry + tally token as Mire holds; Thornfell records only as testimony from away; settles nothing (MD-14). |
| Dating | No calendar date anywhere; weather runs for old entries (MBA run heading, MLW wax book matching the Act I/II run). |
| R08 custody | No names, armies, units, sides or figures of dead (MLL wash stones; MLW "no more out"). |
| CDR-1/2 | Echoes, Reedlurkers, beetles to 0 HP; re-forming only by condition; melee or ranged, ranged never required. No SX. |
| Three states | No fail anywhere; every skill step has a crew alternative; every wait is a keep-watch. |
| MD-7 | No Hollowfoot content in this file; swap notes say so per quest. |
| MD-3 | Rowan crosses only by day/first light (MLW). |
| Known cross-package request | None remaining (`MBL-B9.4`/`B9.4b` already gated by `MLD_ORDER` in Act III). |
| **Independent review (2026-11-09)** | 14 findings fixed in place (0 high, 7 medium, 7 low). **Medium:** first-name collisions with existing NPCs renamed (Jem → Lew Keel, Pim → Dob Haddow, Tam → Corin Haddow; Ned Rudd → Wyn Rudd, in-batch duplicate of Ned Siskin); MLL war-washing at Stillgrave was Ebba's eyewitness fact with no canon support (now labelled Tender belief only, which also fixes Ebba's age); MLL ring count contradicted itself (six stakes / "three in" / twelve lights; now three set, three to close, six lights); MLL "dialogue pauses near enemies" replaced by a standard lantern-gated hold bar; MLW timed tending prompts replaced by four untimed keep-watch turns; MLD pace-matching escort replaced by a standard follow with run disabled, and the dialogue-driven swarm "settle" (a drive-off in effect) replaced by an ordinary ditch leash with calm dialogue as the step; Senna's age contradicted "though she was a girl". **Low:** §0.4 named nonexistent steps (`S08_close`, MLD `S08_table`); the Act III `MBL-B9.4` request is already met; Rootrest Tender line misattributed to Prue; MLW wind night labelled sixth (it is the fifth); night moss nodes noted as an existing presentation-hour variant; MLL fallback for night nodes. Checked and unchanged: flags exactly as Act III/bible §9.1 (`MR_STRANGER_SEAT`, `MR_LANTERN_LINE`, *Lifting Day* completion, `MR_ARRIVALS`); Haddow role names match `MRC-B2.6` and `MBL-B7.12`; no calendar dates or casualty figures; no Hollowfoot; Rowan never crosses at night. |
| Batch 4 encounter alignment review, 2026-11-09 | Aligned with `Enemies/Caelmor_Mire_Encounter_and_Enemy_Requirements.md` §13.3 (numbers only; no id, step or flag renamed): MLL-E1 reed-ripple ~1.2 s → ~1.5 s, first-appearance length (C-5, I-2); MLD-E1 swarm spread ~1.0 s → ~1.5 s, area-effect minimum (C-1, I-12). Also fixed: speaker tags left over from the Batch 3 renames (`MEP-D3`/`MEP-D4` JEM → LEW, 11 lines; `MLL-D2.05`, `MLL-D4.30`, `MLL-D7.03` PIM → DOB); line text unchanged. |
