# Mire of Fallen Banners — Narrative Production Bible

**Status (2026-11-09):** Draft production direction, **independently reviewed 2026-11-07; fixes applied in place** (§13). Cross-package fixes from the Batch 4 zones/integration review (2026-11-09) applied in place (§13). This is the controlling document for every Mire quest, NPC, dialogue, encounter, discovery and world-content package. It turns the approved narrative architecture (`Caelmor_Narrative_Architecture.md` and its four companion files; rulings in `Caelmor_Narrative_Architecture_Review_and_Authoring_Sequence.md` §5.0) into a concrete, playable slate for the Mire of Fallen Banners. Everything marked **[NEW]** is authored here and is not canon until the Creative Director promotes it. Everything marked **[PROPOSAL — DIRECTOR]** is a consequential story choice the content is built on but that Collin may replace; §3 lists exactly what changes if he does.

**Scope guard.** The Mire is the **Mire milestone**: an internal production milestone of the complete game, not a separate release (CDR-3; the first public beta contains the complete planned game). It follows Thornfell in production order (D-R1) and is not a required player order. This package authorizes **no** scope change, no schema, no production JSON and no C#. It is schema-ready markdown for the day Roadmap 31.2/31.3/31.5 exist (Master Protocol §5.1). Technical needs are listed in §11.2 and roll up into the Mire integration handoff (§12, Batch 4); nothing here implements them.

**Binding rulings (2026-11-03):** `Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md` (CDR-1 defeat at 0 HP, CDR-2 ranged included and never required, CDR-3 no partial release, CDR-4 standard systems over realism) governs wherever this bible could disagree. The §7.1 contract (six fields, including Combat compliance) applies to every quest card.

**Authority used (in order):** the rulings file above; Phase 1.1–1.5 (superseded by the rulings where they say "Lowmark only" or "no ranged"); the approved architecture (Arcs §3.2, §5, §6; World Truth H07, H12, H17, H25, C.6, C.7, B.3; Revelation Ledger R08, R14, R16, R17 and seeds for R09; Review §5.0 rulings FT-01–FT-05, D-C03, D-C06, D-CV1, D-R1, §7.1); canon lore (`LORE/Regions/Caelmor_Region3_MireOfFallenBanners.md`, the dossier; `LORE/Characters/Caelmor_Characters_Region3_Mire_Of_Fallen_Banners_Anchors (Not Full List).txt`; Timeline; War History; Factions §17; Region Merged §III). Proposal sources, cited but not promoted: `00_ADMIN/Reference/Caelmor_Part3_Mire_Proposal.md`, `Caelmor_Regional_Source_Process_Mire_Proposal.md`, Part 4 (character ledger; migration proposal; relationship web braids 4, 8, 12; shared events 2, 4, 6), Part 5 (continuation briefs, callback lattice, mystery ledger, discovery framework), Part 6 (material-culture readiness, canon selection), the canon-selection decision sheet and the RuneScape quest architecture study. Format and rigour follow `Caelmor_Thornfell_Narrative_Production_Bible.md`.

---

## 1. The Mire in one page

***What the Earth Refuses to Forget.*** The long wet has come early. The player arrives at **Sorrowmere** as a stranger on the morning the Names Below register is opened for a reading nobody wants: Mara Fenholt's ground has given up remains with a stitched name-tape, and the name on it belongs to a woman who is alive, sitting at the back of the room, holding her foster mother's hand.

Over five milestone quests the player learns why a region that lives by honest testimony is losing its footing.

**The answer has three parts, and the player learns them in this order:**

1. **The Mire is feeding itself across its own battlefield.** The spring spate shifted the Blackwater channels and soured the old ferry way between Sorrowmere and Marshfall. To move peat, food and the sick before the long wet closed everything, Sorrowmere's Reedsward crews relaid a wartime causeway straight across the **Field of Fallen Standards**. Nobody did anything wicked. Edris Hollowmere asked them not to; they needed to eat. Since the causeway went down, banners along it have been rising out of the mud and Banner Wraiths walk the work route at dusk. (Act I: MR-M1, MR-M2)
2. **The place everyone calls haunted is a place where people chose to break.** Earning Rowan Mirewake's crossing and reaching the **Chapel of the Sinking Star**, the player recovers the last record of the Memorywardens. In the final year of the war, retreating columns and their pursuers met on the Field of Fallen Standards in a battle nobody could win. A handful of Memorywardens laid a calm-field over the whole battlefield so that the armies could not keep fighting. It worked. It killed most of them, and it pressed the command, fear and obedience of that field into one coherent imprint. (Act II: MR-M3, MR-M4)
3. **What they left behind still gives orders.** That imprint, the **General Who Wouldn't Fall**, is pushing out along **Bannerline Ridge**, drawing Hollowfoot drifters `[MD-7]` and Earthen Echo files after it. It cannot be bargained with and it cannot testify. Combat disperses it for a night. What quiets the ridge is ordinary people finishing a mourning circle that was left open for thirty years, with the player holding the gap. (Act III: MR-M5)

The player leaves with the Mire's tool for the peace: **testimony that holds**. A name is said aloud only when two different keepers can stand behind it, and no manifestation is ever allowed to speak for the dead.

**Emotional line (Phase 1.1 §6):** Wonder (a banner lifting out of still mud with no wind) → Competence (reading channel stakes, banner states and a command count) → Attachment (Nell's two families, Rowan's silence, Mabyn's lanterns) → Agency (how a name is written, what happens to the banners and the record, how Bannerline is left) → Mastery (Rowan's routes, Mire master commissions, the channel reading the convergence will need).

**What makes it an RPG and not a funeral:** every quest has a route to read, a thing to carry or mend, danger that telegraphs, and a moment that is strange. Grief is a shared load, so the player always has something to lift.

### 1.1 The Mire's readable system: ground and water

Lowmark taught the player to read water against a marking stone. Thornfell taught sound. The Mire teaches **ground**: whether it will hold you today, and what is standing up out of it. It is learned knowledge (Pillar A), never a spell, and every element is a **world marker the player looks at**, not a UI mode.

| Element | What the player learns | Where first taught | Used again |
|---|---|---|---|
| **Channel stakes** | Reedsward depth stakes stand at every crossing, painted in three bands. Water at the **pale** band: the channel is **Running** (boats go, causeway shallows are under). At the **ochre** band: **Slack** (shallows and causeways are walkable; channels go still and shoals go dry, so boats ground on the shoals. Rowan uses Slack his own way: he poles his narrow cuts, which pour like a weir at Running, and hauls the boat over the dry shoals, MR-M3). Stake leaning or water over the **black** band: **Sour** (the bottom has turned; nobody crosses). Each crossing changes state on a fixed daily pattern keyed to the presentation hour (morning, noon, dusk, night). | MR-M1 (walk to the care site with Edris's crew) | Every milestone; MR-M3 crossing; Nine Stakes; convergence footings |
| **Rowan's knots** | Rowan ties knots in reed heads beside channels he trusts: one knot, it turns at dusk; two, at first light; a knot cut through, never this season. Only he ties them, and they mark only his route. | MR-M3 | MR-M4 approach; post-story Chapel route |
| **Lantern moss** | Moss on walkway posts glows faintly when damp. A dark post at night means its foot is dry; a lit post in a line means the line is tended. Chapel-Tenders' lantern lines are moss-wicked: lit = held ground. | MR-M1 (night walk back); taught properly in MR-M4 | MR-M4 chapel; *The Broken Lantern Light*; night travel everywhere |
| **Banner states** | A standard is **laid** (flat or retired: the site is quiet), **leaning** (stirring: Earthen Echoes may form in grief), or **risen** (standing clear of the mud, cloth moving with no wind: Banner Wraiths walk at dusk). | MR-M2 | Field of Fallen Standards, Bannerline, *Cloth for Sale* |
| **The command count** | Near the General, the ground pulses on a count of three: two soft beats, then the third. On the third the Echo files move down their lanes. Step out of lane on two. (Three beats, not four, so it reads differently from Lowmark's four-knock Muster.) | MR-M5 (Bran's warning, then the ridge) | Post-story Night Count (MD-8) |
| **Two holds** | The Memorykeepers' rule for a name: two holds, one name. A register entry, a household book, an object or a living witness each count as one hold; a banner, a dream or a manifestation counts as none. The player sets holds side by side by showing items or recalling testimony in dialogue. | MR-M1 (Ysolde Haverel at the register) | Every investigation; the MR-M5 roll; the Register cases |

---

## 2. Author truth

This is the private truth behind the arc. Players learn it gradually and never from one source. It keeps the architecture's three causes: **a present human decision** (the causeway), **older damaged infrastructure** (broken anchor circles, the sinking chapel, the open circle on Bannerline), and **bounded resonance** (earth-memory imprints, the General) that never testifies.

### 2.1 The old works [CANON core; NEW detail]

- **Anchor circles [CANON].** Memorywardens set stone arrangements to stabilize gatherings and ground grief. The **Turning Stone** near Sorrowmere was one stone of such a circle [CANON]; it turns slightly under a hand during mournful rites. Modern Mirefolk use the circles as gathering points without knowing their function [CANON].
- **The Chapel of the Sinking Star [CANON].** One site with three names: formal and historical *Chapel of the Sinking Star*, common *Sunken Chapel*, riverfolk and ferrymen's *Sunken Church* [C14]. Almost fully submerged; Chapel-Tenders keep lantern lines from its roof; stained glass is intact under the surface; a Memorywarden relic is rumoured beneath the altar [CANON]. The name's origin is **never explained**. It sank slowly, not by collapse [CANON, Sennic].
- **The chapel's drains [NEW].** The chapel was built on a raised bank and drained by stone culverts with wooden sluice boards. The boards are rotted shut. Opening them in the right order, at Slack, drops the nave in stages. This is ordinary building, the same craft as Sorrowmere's walkways.
- **The Bannerline circle [NEW].** On the crown of Bannerline Ridge stands a ring of low stones with one gap, beside the old palisade. It is the circle the last Memorywardens laid out to anchor their calm-field. The rite that should have closed it was never finished: the people who began it did not come back down. Griefwatch thinks it is an old mourning ring that "was never done properly" and leaves it alone.
- **The Standards Causeway [NEW].** A wartime corduroy road of logs and fascines laid straight across the Field of Fallen Standards to move troops and wounded. It sank after the war. Sorrowmere's Reedsward crews relaid it this spring on the old line because it is the only ground that holds.

### 2.2 The war [APPROVED FT-02c; NEW detail]

- The Mire was the war's central battlefield; Memorywardens were conscripted as guides and healers, and their practice broke under trenches, pyres and mass burial [CANON H12].
- **The last great battle [APPROVED FT-02c].** As the war came apart, retreating columns from more than one front and their pursuers collided on the Field of Fallen Standards. Neither side could win and neither needed the field. The last Memorywardens laid a mass grounding, a **calm-field** [CANON technique], over the battlefield so that the armies could not keep fighting. Fighting in the Mire stopped. The overload killed most of them and concentrated command, fear and obedience into the imprint later called **the General Who Wouldn't Fall** [CANON nature]. Survivors abandoned the practice.
- **What the record shows [NEW].** The Memorywardens wrote their plan and their tallies on fired clay leaves and sealed them under the chapel altar before going out. They signed with office marks pressed into the clay, never names. Regimental logs on both sides stop on the same day, mid-entry or with a single line ("ground will not take a step", "men sat down").
- **The Lantern That Would Not Go Out [CANON myth; NEW reading].** Kept burning for seven nights after the battle by Chapel-Tenders with peat-wax and covered housings, waiting for people who did not come back from the field. Craft, not a miracle. Folk belief that it was "a Memorywarden's final act" is near the truth by accident and stays belief.
- **Names withheld forever in Mire content [R08]:** the Memorywardens' names, which armies collided, and how many died.

### 2.3 The present wrong: feeding across the field [NEW]

- **The spate.** The spring spate shifted the Blackwater channels. The ferry way from Sorrowmere to Marshfall runs Sour most of the day. Before the long wet, Sorrowmere must bring in Marshfall's peat and food and send the sick to Rootrest.
- **The causeway.** **Oswin Garvey**, Sorrowmere's Reedsward crew-lead, relaid the Standards Causeway. Edris asked him to wait for a Silt hearing. He did not: "The hearing sits after the rain. People eat before it." Laying the logs, his crews lifted fallen standards out of the way and stood them at the roadside "so nobody drives over them". Standing them up is what woke them. This is the region's care dispute (architecture rule 4: the Mire's antagonist is its own unresolved care): a decision that was kind and wrong at once.
- **The Rootshadow side-trade [CANON group; NEW act].** The loosened ground lets Rootshadow cutters strip banner cloth from risen standards to sell as "commemorative goods". They worsen it; they did not cause it [FT-04 spirit: no single villain]. They appear in MR-M2 (sign only) and *Cloth for Sale* (fight).
- **Why now on Bannerline.** Each risen banner on the causeway is a standard of the last battle's columns. Raised, they pull at the imprint that formed from that field. The General pushes out from Bannerline along the line of the standards; Hollowfoot drifters and Earthen Echo files follow it. Griefwatch closes the Bannerline road.

### 2.4 The resonance [CANON boundaries]

- **Earthen Echoes and Banner Wraiths are minor, place-bound impressions [C15].** Not ghosts, not souls, never undead. They repeat motions. They are drawn to strong emotion and risen standards. A Banner Wraith dissipates if its banner is properly honoured or retired [CANON].
- **Chapel Shades [C15]** are impressions in the dark of the Sunken Chapel. They are a **hazard**, not a combat family: they dim lanterns and press the player back toward light (§10).
- **The General Who Wouldn't Fall [C15]** is a singular coherent earth-memory manifestation formed from command, fear, obedience, death and trauma. It is not a returned commander. It repeats the pressure and form of command: "Hold." "Close up." "No one leaves." It never names a unit, a battle or a person, and it never answers a question.
- **The Sorrowback [C15]** is the Mire's other major threat. It is **not** a Mire-arc boss. Its trail and Bran's warning appear (MDS07); it stirs in the convergence (CV-M2).
- **The Memorywarden shard** (MR-M2) reacts to grief: lantern moss near it brightens and loose silt settles flat around it when someone grieving stands close. It proves nothing about anyone.

### 2.5 Who knows what

| Person | Knows | Does not know |
|---|---|---|
| Edris Hollowmere | Her own care work; that she received a child off the Standards road in the war's last year and wrote her into care under the name the child gave. That the causeway should have waited. | Who the child's mother was; what stopped the fighting. |
| Oswin Garvey | Why he relaid the causeway; that his crews stood the banners up. | That standing them up is what woke them. |
| Calwen Reed-Binder | Which fabrics rot slower; how a standard is folded and retired. | Whose any banner is. He refuses to guess. |
| Mara Fenholt | Where the ground released remains; the name-tape she found. | Whose remains they are. |
| Ysolde Haverel | The Names Below register, its forms and the stranger's seat. | Why the seat exists (R16, withheld). |
| Rowan Mirewake | The safe approach to the Chapel; the knots; why he does not cross at night (if told). | What the Chapel was for. |
| Old Sennic Vale | Childhood stories: bells that rang without sound, mages who listened, the church sinking slowly. | Any system or spell. He gives *where*, never *why*. |
| Mabyn Coyle | The roof lantern line; the Tenders' craft for the seven-night lantern. | What is under the altar. |
| Bran Hollowstep | Which ground is still unsafe; the Sorrowback's trail; the count he feels in the ridge. | Anything beyond his own watch (ledger limit: no theatre or dates). |
| Nell Ferrow | Her life in the Ferrow house; a scrap of a lullaby; that she "came in on the road". | Her birth name. |

### 2.6 What defeating an imprint means

Earthen Echoes and Banner Wraiths follow the Lowmark drift precedent (Lowmark bible §2.5): **combat disperses, conditions decide.** Each is defeated at 0 HP and collapses into mud. While its condition lasts (a risen standard, an open circle, a grief event), it re-forms. In an active encounter a collapsed figure re-forms on its site's trigger (Echo 6 s; boat cut ~10 s; a standard's forming tell or pulse; the next third beat on Bannerline); outside an encounter, only when a quest next presents its condition (Enemies C-3; outside quests, standards are presentation only, Zones §7; pending Gameplay Designer confirmation). Retiring or honouring the standard, or closing the circle, ends the condition. **The General** is defeated at 0 HP in MR-M5 and disperses for the night; it re-forms while the circle stands open. Closing the circle ends the condition for the story; the General remains a canon major threat and a revisitable night encounter afterwards (§3, MD-8). No defeated enemy, human or imprint, ever gives testimony (rulings §3.2).

---

## 3. Director decisions and how the content depends on them

Mire decisions use the prefix **MD-**. Each is open; content is built on the recommendation and isolated so a change touches only the listed places.

| # | Decision | Recommendation (what content assumes) | Content that changes if replaced |
|---|---|---|---|
| MD-1 | **The present cause** | The relaid Standards Causeway (a Reedsward care decision by Oswin Garvey [NEW]), with Rootshadow cutters exploiting it. No villain organization. | MR-M2, MR-M5 lead-in, *Cloth for Sale*. Tagged `[CAUSEWAY]` (§3.1). |
| MD-2 | **MR-M1's case** | An intra-Mire fosterage: Nell Ferrow (Sorrowmere foster household) is Linnet Hayle of a Marshfall family; the remains are probably her birth mother's. Braid 4 and braid 8 shapes are used in the Register side series instead, so the entry milestone stands alone. | MR-M1 only. |
| MD-3 | **Night crossing vs. Rowan's canon refusal** | The architecture's "guided night crossing" conflicts with Rowan's anchor ("refuses night crossings"). Recommendation: **a first-light crossing in fog** ("the grey", which Rowan does not count as night). The night is still present: the player walks the lantern lines back at night in MR-M1 and holds the Bannerline vigil in MR-M5. | MR-M3 timing and lines. |
| MD-4 | **Chapel "breath management"** (Arcs §3.2) | Replaced under CDR-4 by **staged drainage** (open three sluice boards in order at Slack to drop the nave) and **lantern lines** (lit posts hold ground against Chapel Shades). No swimming, no air bar, no new movement mode. | MR-M4 beats; §11.2. |
| MD-5 | **Adopting Part 3 practices** | Adopt as [NEW]: the **Names Below register**, **Reedsward** as a household work rota (not a place), the **Silt hearing** (no appeal rules stated), **lantern debt** (never hereditary), **lifting day**. The merged overview's place name "Reedsward" (architecture contradiction 5) stays unplaced and unused as a place. | Text only; MR-M1, *Lifting Day*, *The Hushed Granary Key*. |
| MD-6 | **The Memorywarden record** | Fired clay leaves in a lead-lined box beneath the altar, signed with office marks, no names; the plan, a stone list, and tally marks going out and coming back (no figure is ever stated or totalled: casualty counts stay withheld, FT-02/R08). Custody choice in MR-M4. | MR-M4 inspect text; CV-M1 custody line. |
| MD-7 | **Hollowfoot as enemies** | Canon makes Hollowfoot **humans** driven half-mad by war trauma. Under CDR-1 they are an ordinary human enemy family: they fight to 0 HP with the ordinary defeat presentation. Dignity rules: they appear only where the General's pulse drives them (MR-M5, Bannerline road); no named or known person is ever among them; no NPC treats a fight as a cure; Lysa's settled Hollowfoot at Fenward are non-combatant NPCs, never targetable. Alternative for the Director: retire Hollowfoot as an enemy family and depict them only as non-combatant survivors (MR-M5 then uses Echo files alone). **Status: OPEN, both options kept (Director, 2026-11-08).** Every package tags Hollowfoot content `[MD-7]`, keeps it off required evidence and sole routes, and carries a one-line non-combat swap. | MR-M5 encounter mix; §10; every `[MD-7]` tag. |
| MD-8 | **The General after MR-M5** | It stays a canon major threat. After the story it is a **revisitable night encounter** ("the Night Count"; not "the Muster", which is Lowmark's Act III boss) that the player starts by striking the muster post on Bannerline. `MR_BANNERLINE` changes the ridge and lines, not access to the rematch. | MR-M5 epilogue; §9. |
| MD-9 | **Map placement** | Relative only (§4). **MAP VERIFICATION REQUIRED** wherever geometry matters. No compass direction toward any region; the dossier's "eastern incursions" wording (architecture contradiction 3) is not used. No trade route or travel path to another region is stated (FT-03 spirit). Mirebone Crossing appears as a dangerous ford only; its convergence role stays **provisional** and no Mire content builds toward it. | Travel lines; MP10. |
| MD-10 | **Level framing** | No quest prerequisite; tuned as post-Thornfell content in production terms: MR-M1–M2 Competent, MR-M3–M5 Advanced. Exact levels are Gameplay Designer calls. | Encounter tuning. |
| MD-11 | **Skills** | The Mire uses Hunting (fen fowl, reedlurkers), Fletching and Ranged (reed-shafted fowling arrows), Cooking (care and mourning tables), Leatherworking (repair of imported leather), Woodcutting (reclaimed and root wood) and Melee. Mining and Smithing have no Mire intro: the Mire has no approved ore and no forge, and battlefield metal is evidence, not feedstock (source-process proposal). Reed shafts, fen fowl and griefroot are legacy concepts or proposals for the economy pass, not catalog items. | Skill-intro side quests only. |
| MD-12 | **Rootshadow presence** | Cutters and a go-between appear; the Syndicate is fragmented and avoids large conflict [CANON]; no Rootshadow leader is named; nothing links them to the Remnant. | *Cloth for Sale*; MR-M2 signs. |
| MD-13 | **Glassed Hollow arrivals (braid 12)** | Held back. One Rootrest care-book entry for a burned man "from the fire roads" who would not give his name stays an **unresolved name** (MDS09) until the Emberholt bible exists. Nothing says Glassed Hollow. | MDS09 only. |
| MD-14 | **The Brede case (Thornfell TWN)** | The Mire's Book of Arrivals adds a care entry for "a Brede, down from the high passes with a thaw column", which does not settle which Brede. Thornfell's resolution stands. | *The Book of Arrivals* only. |
| MD-15 | **Lowmark's sealed tin (FC)** | The Mire does **not** read `FC_SEAL_NOTED`. No Mire archive identifies the seal; inventing one would imply a route. Left for a later owner. | None. |
| MD-16 | **Canon promotion** | Promote nothing from this package. | None. |

**SX proposal: none.** No Mire story needs a scripted surrender or mercy outcome. Every human enemy (Mud-Clad Raiders, Rootshadow cutters, Hollowfoot) fights to 0 HP. Non-combatants (Gethin Scarth the go-between, Oswin Garvey, every claimant) never fight and are never targetable, so they need no SX-N entry.

### 3.1 Causeway swap layer

If MD-1 changes, edit only nodes tagged `[CAUSEWAY]`: Oswin Garvey in MR-M1 (mentioned), MR-M2 (named; the standing-up confession), MR-M5 (circle placement); the Reedsward crew barks; *Lifting Day*. The banners, the shard, the logs, the chapel record and the Bannerline circle survive any replacement that is still "a present, local reason the field's standards were raised".

---

## 4. The map and points of interest

### 4.1 Subzones (dossier §VI–VII)

| Subzone | What it is in play | Main content |
|---|---|---|
| **Sorrowmere and the Raised Ways** | The hub on elevated walkways: register room, memorial gardens, mood banners, the Turning Stone, Calwen's reed sanctuary at its edge. | MR-M1, hub, Names Below series |
| **The Field of Fallen Standards** | The flattened banner bog crossed by the Standards Causeway; Nine Stakes at its edge. | MR-M2, *Cloth for Sale*, *Nine Stakes* |
| **Marshfall Edge** | Where marsh meets forest: hunters, peat-cutters, fowling meres, the Hushed Granary. | MR-M1 claim, skill intros |
| **The Blackwater Channels** | Shifting channels, Rowan's landing, the Drowned Encampment, Stillgrave Hollow, the Chapel. | MR-M3, MR-M4 |
| **Rootrest and the Fenward** | The settlement around surviving roots; Lysa's Fenward huts; the Unfired Kiln. | Care content, MR-M5 lead-in |
| **Bannerline Ridge and Griefwatch** | The rare high ground: watch settlement, Bran's watchpost, the palisade, the circle, the Dry Muster. | MR-M5 |

### 4.2 POI slate (28 POIs; Phase 1.5 range 24–32)

Ids are planning labels (`MP##`). Placement is relative. **MAP VERIFICATION REQUIRED** for every placement; the zone package (Batch 4) carries the detail.

| Id | POI | Category | Subzone | Status | Main use |
|---|---|---|---|---|---|
| MP01 | **Sorrowmere** (raised ways, longhouses, register room, memorial gardens, mood banners) | Settlement | Sorrowmere | [CANON] | Hub; MR-M1; Names Below series |
| MP02 | **Marshfall** (stilt houses, peat yards, smoke sheds) | Settlement | Marshfall Edge | [CANON] | MR-M1 claim; *Reed Shafts*; *Weight of the Soil* |
| MP03 | **Griefwatch** (watch settlement, vigil hall, closure gate on the Bannerline road) | Settlement | Bannerline | [CANON] | MR-M5; *The Bell Roster* |
| MP04 | **Rootrest** (root-sheltered homes, herbalists, bonecarvers) | Micro-settlement | Rootrest | [CANON] | Care hub; *The Unfired Kiln* discovery; MDS09 |
| MP05 | **Fenward Huts** (Lysa's care huts) | Micro-settlement | Rootrest | [CANON anchor location] | MR-M5 Hollowfoot care; *A Table for the Wet* |
| MP06 | **Blackwater Landing** (Rowan's reed docks and boat shed) | Micro-settlement | Blackwater | [CANON anchor location; NEW name] | MR-M3; *The Ferry Harness* |
| MP07 | **The Field of Fallen Standards** | Unique landmark | Field | [CANON] | MR-M2 |
| MP08 | **The Standards Causeway** (relaid wartime log road) | Ruin/war site | Field | [NEW] | MR-M1 walk; MR-M2 |
| MP09 | **The Drowned Encampment** | Ruin/war site | Blackwater | [CANON] | *The Mud That Remembers*; MR-M3 approach |
| MP10 | **Mirebone Crossing** (bone-littered ford) | Unique landmark | Blackwater edge | [CANON]; convergence role provisional | Discovery MDS10 only |
| MP11 | **Stillgrave Hollow** | Unique landmark | Blackwater | [CANON] | *The Broken Lantern Light* |
| MP12 | **Bannerline Ridge** (palisade, muster post, the circle) | Ruin/war site | Bannerline | [CANON; circle NEW] | MR-M5 |
| MP13 | **The Chapel of the Sinking Star** (roof lantern line, nave, vestry, altar crypt) | Cave/dungeon | Blackwater | [CANON] | MR-M4 |
| MP14 | **Calwen's Reed Sanctuary** (washing frames, banner store, retirement pool) | Shrine | Sorrowmere edge | [CANON anchor location] | MR-M2; *A Banner With No Side* |
| MP15 | **The Turning Stone** | Shrine | Sorrowmere | [CANON] | MDS01; micro-event |
| MP16 | **The Last Root of Sorrow** | Shrine | Rootrest | [CANON myth] | MDS08 |
| MP17 | **Bran's Broken Watchpost** | Ruin/war site | Bannerline | [CANON anchor location] | MR-M5; MDS07 |
| MP18 | **Sennic's Driftwood Rise** (peat-edge shelter) | Unique landmark | Blackwater edge | [CANON anchor location] | MR-M3 leads |
| MP19 | **The Singing Trench** | Ruin/war site | Field edge | [CANON myth] | *The Singing Trench* |
| MP20 | **The Sodden Pyres** (burned wood over smouldered peat) | Ruin/war site | Marshfall Edge | [CANON feature] | MDS03 |
| MP21 | **Nine Stakes** (marked crossing, raider ground) | Bandit site | Field edge | [NEW, Part 3] | *Nine Stakes* |
| MP22 | **The Hushed Granary** (raised emergency store) | Unique landmark | Marshfall Edge | [NEW, Part 3] | *The Hushed Granary Key* |
| MP23 | **The Reed Hide** (Rootshadow cutters' camp in a drowned trench) | Camp | Field | [NEW on CANON group] | *Cloth for Sale* |
| MP24 | **The Dry Muster** (old drill ground with a gap in the lines) | Ruin/war site | Bannerline | [NEW, Part 3] | MDS04; *The Bell Roster* |
| MP25 | **The Wading Ford** (where the Father waits) | Unique landmark | Blackwater | [NEW place on CANON myth] | *The Father at the Ford* |
| MP26 | **The Fowling Meres** | Hunting ground | Marshfall Edge | [NEW] | *Reed Shafts* |
| MP27 | **The Rust Hollow** (ironbloom ground, stalker range) | Hunting ground/danger | Field edge | [NEW] | *The Rust Hart* |
| MP28 | **The Unfired Kiln** (Rootrest children's rain shelter) | Ruin/war site | Rootrest | [NEW, Part 3] | MDS05 |

Counts against Phase 1.5 (each POI counted once): settlements 3 (MP01–03); micro-settlements 3 (MP04–06); ruins/war sites 8 (MP08, MP09, MP12, MP17, MP19, MP20, MP24, MP28); cave/dungeon 1 (MP13); camps/bandit sites 2 (MP21, MP23); shrines 3 (MP14–16); unique landmarks 6 (MP07, MP10, MP11, MP18, MP22, MP25); hunting grounds 2 (MP26, MP27). Total 28. The Mire has no mine by design (MD-11).

**Relative route order** (MAP VERIFICATION REQUIRED): Sorrowmere → (old ferry way, Sour this season) → Marshfall; Sorrowmere → the Standards Causeway across the Field → Marshfall's near side, with Nine Stakes and the Reed Hide off the causeway. Rootrest lies on firmer ground beyond Marshfall. Blackwater Landing sits below Sorrowmere; the Chapel is reached only by Rowan's route through the Blackwater, past the Drowned Encampment and Stillgrave Hollow. Griefwatch sits at the foot of Bannerline Ridge; the Bannerline road climbs from Griefwatch's closure gate to the crown. Bran's watchpost stands on a shoulder above Griefwatch, off the road; **requirement:** the path to it leaves from Griefwatch's side of the closure gate and never passes through the gate, because MR-M5 `S02` sends the player there while the road is shut (Zones MT-14; MAP VERIFICATION REQUIRED). Before MR-M5 the closure gate stands open (*The Bell Roster*); Ide shuts it at MR-M5's start and it reopens in both outcomes. Whether the bends and the crown may be walked before MR-M5 is **open** (Zones Q-3). Mirebone Crossing lies at an edge of the Blackwater and is not on any milestone route.

---

## 5. Cast

### 5.1 Canon anchors (limits from the Part 4 character ledger apply to every line)

| Anchor | Role here | Limits kept |
|---|---|---|
| **Edris Hollowmere** | Informal caretaker; MR-M1 care testimony (she received the child); MR-M2 objector to the causeway; MR-M5 holds a stone of the circle. | Owns her own care account only. Her "the Mire knows when it's respected" is ethics, not proof the land has agency. No unit, age or service. Never turns a manifestation into a witness. |
| **Calwen Reed-Binder** | Banner tender; MR-M2 retirement rite; *A Banner With No Side*. | Refuses to identify banners by faction. A banner needs a second channel before naming anyone. |
| **Mara Fenholt** | Bone-gatherer and marker-setter; MR-M1 find; MR-M2; *Weight of the Soil*. | Marks with stones, never names. Never digs deeper than the ground offers. |
| **Rowan Mirewake** | Ferryman; MR-M3 and MR-M4 guide. | The only known living guide to the one chapel. Learned the route from someone who never returned. Refuses night crossings. Passage proves nothing about the chapel's origin. No second guide is created. |
| **Old Sennic Vale** | Elder; MR-M3 leads (where, not why). | Bells, listening mages, slow sinking are stories. He never explains earth-memory or names a rite. |
| **Lysa Thornettle** | Healer; MR-M1 (Nell's care), MR-M5 (Hollowfoot care); *A Table for the Wet*. | Present care only. "Healing is making space." |
| **Bran Hollowstep** | Veteran who watches; MR-M5 boundary warnings and the count; MDS07 Sorrowback trail. | Direct witness only to his own experience; no theatre, dates or battle assigned. Never claims to have been at the last battle. |

### 5.2 New for the Mire [NEW]

| Name | Role | Where | Voice note |
|---|---|---|---|
| **Ysolde Haverel** | Memorykeeper; keeper of Sorrowmere's Names Below register. | MR-M1; *The Stranger's Seat*; *The Book of Arrivals*; MR-M5 roll. | Precise, kind, will not round a number. "Two holds, one name." |
| **Nell Ferrow** | Fostered woman of Sorrowmere; came in off the Standards road as a small child. | MR-M1; MR-M5 circle. | Funny when frightened. Decides about her own name. |
| **Agna Ferrow** | Her foster mother; old, sharp, lame on wet ground. | MR-M1. | "I did the raising. Write that." |
| **Dunstan Hayle** | Marshfall peat-cutter; keeps the Hayle household book; was a boy when his mother and small sister were lost on the road. | MR-M1; *Weight of the Soil*. | Says less than he means; brings food instead of words. |
| **Oswin Garvey** `[CAUSEWAY]` | Sorrowmere's Reedsward crew-lead; relaid the causeway. | MR-M1 (mentioned); MR-M2; MR-M5. | Tired, decent, defensive. "People eat before hearings." |
| **Mabyn Coyle** | Chapel-Tender; keeper of the Sunken Chapel's roof lantern line. | MR-M3; MR-M4; *The Lantern That Would Not Go Out*. | Religious, practical, smells of peat-wax. Never claims a miracle. |
| **Ide Larrow** | Marshwarden captain at Griefwatch; keeps the Bannerline closure. | MR-M5; *The Bell Roster*. | Clipped. Treats a closure as a weight she carries, not a power. |
| **Corra Sallis** | Young Bannerbearer at Sorrowmere. | MR-M2; *Lifting Day*; barks. | Earnest; carries a mood banner and wants to carry a real one. |
| **Hob Merrit** | Marshfall fowler and fletcher. | *Reed Shafts*; MR-M1 hunting line. | Cheerful, patient, swears at herons. |
| **Gethin Scarth** | Rootshadow go-between at the Marshfall jetty; never fights. | *Cloth for Sale*. | Polite, evasive, frightened of his own suppliers. |

Minor roles (role names only unless a package names them): Reedsward crews, Chapel-Tenders, Bannerbearers, Memorykeepers, Marshwardens, ferry households, Rootrest healers and bonecarvers, Marshfall hunters, Mud-Clad Raiders, Rootshadow cutters, a Thornfell Ridge Warden pair (Griefwatch visitors [CANON]).

### 5.3 Voice rules (binding)

1. **Plain, heavy and kind.** Short sentences. No false hope [dossier §III]. *"I won't tell you it'll be all right. I'll tell you what we're doing about it."*
2. **Seen, then thought.** Mirefolk separate what they saw from what they believe, out loud. *"Seen: the banner's up. Thought: it shouldn't be. That's all I've got."* Memorykeepers add the source: *"That's Sennic's story. I'm not saying it's so."*
3. **Nobody speaks for the dead.** No "he'd want", no "she's at peace". *"We don't know what she'd want. We know what we can carry."*
4. **Nobody calls anything magic.** The ground is "heavy", "full", "remembering"; older people may say "full of spirit" meaning lives pressed into a place [C08], never souls. Wraiths are "impressions" to Memorykeepers and "the risen" to crews.
5. **Water and ground grammar.** "The water's running / slack / sour." "It's a heavy night." "That ground won't have you."
6. **Care comes before explanation.** *"Sit. Eat. Then tell it."* Food is offered before any question.
7. **Record-keeping is love.** Writing a thing down is how people mind each other. *"We write that you asked. Not found is a record too."*
8. **Addressing the player** is origin-neutral (Lowmark D-3). Strangers are "traveller". After MR-M1, people who saw the reading say "witness" (the stranger's seat). Nothing else changes.
9. **Humour** is dry, gallows-light and kept for tables and work. *"Rowan's smiled twice. Once was wind."*
10. **Emberholt** is resented rationally (war escalation, peat and timber fears) and never caricatured. No region is called "invaders"; no direction is given for any enemy.

---

## 6. Main questline (five milestones)

All milestones use the Lowmark package format (§11). **All Mire codes are three letters beginning with M and never begin with "MQ"** (Lowmark uses MQ1–12), so they cannot collide with Lowmark's two-letter or Thornfell's T codes. Region flags use `MR_` (§9).

| # | Milestone | Code | Act | Where | Core verbs (primary first) | Set piece | Strange moment | Choice | Unlocks / world change |
|---|---|---|---|---|---|---|---|---|---|
| MR-M1 | **The Name at Sorrowmere** | MNS | I (entry) | Sorrowmere register room, the Standards Causeway, Marshfall, Fenward | **search and match records**, walk a shifting route, sit as witness | A night walk back along the causeway by lantern moss with a care cart, the stakes turning Sour behind you | Nell hums a lullaby nobody taught her; Dunstan, on the bench outside the door, finishes the line | How the register writes her | `MR_CHANNELS`; `MR_NAME_RECORD`; Sorrowmere hub; Act I side quests |
| MR-M2 | **The Banners That Refuse to Fall** | MBR | I (turn) | Field of Fallen Standards, the Causeway, Calwen's sanctuary | **recover and retire** under attack, read banner states, repair route | Lifting and folding a risen standard on the causeway while its Wraiths form around you at dusk | A sunken officers' chest: three units' logs stop on one day; carrying the shard past Dunstan, the lantern moss on the nearest post brightens and the silt settles flat round his boots | Retire or restore the field's standards | `MR_BANNERS`; `MR_CAUSEWAY`; R08 seeds |
| MR-M3 | **Rowan's Crossing** | MRC | II | Blackwater Landing, Sennic's rise, the Drowned Encampment, Stillgrave edge | **prepare, learn, wait**: mend, gather, read knots; then a guided crossing | The first-light crossing in fog through channels that turn under the boat | A bell rings across the water with no sound in it: the player sees the reeds flatten in rings and hears nothing | Ask Rowan, gently and again, or let him keep it | `MR_ROWAN_TRUST`; Chapel route |
| MR-M4 | **The Chapel of the Sinking Star** | MCS | II (turn) | The Sunken Chapel | **drain and light**: sluice puzzle at Slack, lantern lines, crypt delve | Dropping the nave in three stages while Chapel Shades press at the edge of each lit line | The stained glass, uncovered by the falling water, is lit from behind by nothing | Who keeps the record | `MR_WARDEN_RECORD`; R08 |
| MR-M5 | **Bannerline** | MBL | III (capstone) | Griefwatch, the Bannerline road, the crown of the ridge | **read the count and hold the gap**; retire the ridge's standards; complete the circle | Holding the circle's gap stone while the General's files come down their lanes and the community fills the stones one by one | When the last stone is filled, the count stops mid-beat, and the ridge's standards lean, one after another round the ring, toward whoever stands nearest, and lie down without wind | How Bannerline is left | `MR_BANNERLINE`; `MR_STANDING` |

**Length targets:** MR-M1–M2 40–55 minutes each; MR-M3 35–45 (deliberately quieter); MR-M4 55–70; MR-M5 60–75 including the aftermath. Main line about 4–5 hours; side content roughly doubles the Mire's narrative hours.

**Prerequisites.** MR-M1 has **none** (travel only). MR-M2–M5 each require the previous milestone. No Lowmark or Thornfell content is ever required.

### 6.1 Milestone briefs

These briefs bind the Act packages. The packages author beats, steps, flags, encounters, dialogue and integration notes.

**MR-M1 The Name at Sorrowmere (`MNS`).** *Offer:* on first entering Sorrowmere (any route; MAP VERIFICATION REQUIRED). Ysolde Haverel stops the stranger on the raised way: a register amendment needs someone from outside the household lines to sit the stranger's seat, and "you're the only one here who isn't somebody's cousin". Optional hooks: a Thornfell cairn name (TF-M3 Completed) or a Lowmark name (*The Candle Rule* Completed: Ewan Holt). Ysolde searches the register: **not found**, and she writes that the player asked ("Not found is a record too"). The Mire end of those cases belongs to the Register series (§7.6). **Situation:** Mara Fenholt's ground beside the Standards Causeway released remains with a stitched cloth name-tape: *Linnet*. The Hayle household of Marshfall lost a mother and a small daughter, Linnet, on the Standards road in the war's last year; Dunstan Hayle has come to claim the remains as his sister's and to have her name cut. Nell Ferrow, who came into Edris's care off that road as a small child, is alive in the room. Agna Ferrow wants the register to say Nell is a Ferrow and nothing else. **Beats:** (1) **The reading** (`S01`): the stranger's seat (a carved stool on the visitor's side of the register table; nobody explains it, R16 seed). Ysolde reads the register entry aloud: *"Received off the Standards road. Girl, small. Gave her name as Nell. Mother not found. Care: Hollowmere. Fostered: Ferrow."* Dunstan reads a Memorykeeper's copy of the Hayle book's entry (the book itself stays under its own roof at Marshfall). Required: hear both. (2) **The care site** (`S02`): Ysolde needs Edris's care leaf read where it is kept, at Edris's old care station on the Marshfall side (the leaf stays in Edris's keeping; the player carries it as knowledge). The ferry way is Sour; the only way is the causeway. Edris's crew teaches the **channel stakes** (pale, ochre, black) on the walk out; the player waits for Slack at one stake, crosses, and sees the roadside banners leaning (seed for MR-M2; Oswin's crew standing standards up as they work, `[CAUSEWAY]` pass-by). Griefbit beetles swarm a sick traveller's cart at the far end (fight). (3) **Holds** (`S03`, any order): **Edris's care testimony** (she tells what she did that night, not what it means); the **care leaf** (in her station's tin box: the child's clothes described, "a reed charm sewn in the hem, three knots"); the **name-tape** (Mara's find; she lets the player lift it from her marker for the reading, carried as `MNS_name_tape`: the stitching is a child's name-tape sewn into an adult's sleeve, as mothers did so a child could be found); the **Hayle book** at Marshfall (a three-knot reed charm drawn beside Linnet's name: the Hayle household mark). Lysa, sitting with Nell at Fenward, offers the last hold if asked: Nell still has the charm. (4) **The walk back** (`S04`): the sick traveller's care cart back to Sorrowmere, at night, on the causeway, by the lantern moss on the posts; behind the player the stakes turn Sour and the far end closes. A Banner Wraith forms at a risen standard and walks across the road (first sight; fight or wait it out; it re-forms). **Strange moment:** at the Ferrow house in Sorrowmere, where Lysa has brought Nell back from Fenward for the reading, Nell hums a lullaby nobody taught her. Dunstan, outside the door, finishes the line. Nobody comments. (5) **The second reading** (`S05`): the player sets the holds side by side for Ysolde (showing the name-tape and recalling the care leaf, the Hayle mark and Edris's account). Ysolde's conclusion: Nell is very probably Linnet Hayle; the remains are very probably her mother's, who carried her daughter's tape in her sleeve. Nell decides how her name is written; the player, as witness, is asked what they would write. **Choice** (`MR_NAME_RECORD`): **amended** (both names written, "Nell Ferrow, born Linnet Hayle"; the remains named as Hayle, mother, "probable"; Mara cuts no name on her stone, but the register carries it) or **qualified** (the entry stays "Nell", with a qualifying line naming the Hayle book as a hold; the remains are marked by Mara's stone, unnamed, and the Hayles may mourn there). Neither outcome is wrong. Complete when Ysolde blots the page and offers the player a seat at the table that night. Sets `MR_CHANNELS`. *Combat compliance:* beetles and the Wraith fight to 0 HP; the Wraith re-forms at its standard (condition), melee or ranged.

**MR-M2 The Banners That Refuse to Fall (`MBR`).** *Offer:* Calwen Reed-Binder at his sanctuary, the morning after MR-M1: the causeway crews are bringing him banners "that won't stay down", and two carters were knocked off the road at dusk by "the risen". Edris and Oswin are both there and not speaking. **Beats:** (1) **Banner states** (`S01`): with Calwen on the near causeway, learn laid / leaning / risen. Corra Sallis, a young Bannerbearer, has followed to help and is told to stay back (she does not). (2) **Oswin's confession** (`S02`, required talk; `[CAUSEWAY]`): his crews stood the standards up "so nobody'd drive over them". He knows what it looks like now. (3) **Recovery under attack** (`S03`): three risen standards on the causeway. For each: free the pole (a channelled lift beside Mara, who keeps her rule: dig only to the pole's foot, never under it), re-pin the causeway logs the pole was holding (a short repair), then **fold the cloth** in Calwen's fold (read the cloth's seams: fold along the strongest seam first, then the hem, then the hoist; a wrong fold just unfolds, no penalty). Banner Wraiths form as the cloth comes free; fight in the open causeway (melee or ranged; the causeway is narrow, so lanes matter). One standard's foot-socket holds a **Memorywarden shard**: a clay fragment with faint marks. (4) **The officers' chest** (`S04`): the third standard stands over a sunken chest at the causeway's foot. Clear the Reedlurkers in the ditch, then lever it up. Inside: three regimental day-books in oilcloth, from units of different columns (Calwen will not say whose), each stopping on the same day. One reads *"ground will not take a step"*; one ends mid-word; one says only *"men sat down"* (`MBR_unit_logs`, quest item; R08 seed). Ysolde, shown them later, names them **Memorykeeper material**: records. The shard she will not touch: "That's not ours. That's older than anything we keep." This is the records/relics distinction the dossier asks for. **Strange moment:** carrying the shard past Dunstan (who came to help carry banners), the lantern moss on the nearest post brightens and loose silt settles flat in a ring around his boots. He does not notice. The player does. (5) **The Risen Colour** (`S05`, miniboss phenomenon, never named in UI): at dusk, the Banner That Sank Twice [CANON myth] rises at the field's centre and a coherent knot of Wraiths forms round it, moving as a colour party. Defeat its bearers to 0 HP between the standard's dusk pulses; they re-form until the standard is down. Lift and fold it under pressure. (6) **Choice** (`MR_BANNERS`), argued at the sanctuary by Calwen, Edris, Oswin and Corra: **retired** (the standards are washed and laid in the retirement pool; the field's causeway sites go quiet for good; the Banner That Sank Twice is laid down with them) or **restored** (the Banner That Sank Twice is re-raised at Griefwatch's vigil hall with honours, as the old story asks, and the others laid; Corra carries it; the causeway sites go quiet, and Griefwatch now flies a banner the ridge can feel, a line MR-M5 reads). Either way the causeway is reset with no standards beside it (`MR_CAUSEWAY` = reset). Complete when Calwen stores the shard in his unsorted chest "with everything else nobody owns". *Combat compliance:* Wraiths and Reedlurkers fight to 0 HP; Wraiths re-form while their standard is risen; no exception.

**MR-M3 Rowan's Crossing (`MRC`).** *Offer:* Ysolde reads the unit logs and needs to know what stopped three columns on one day. Sennic, asked, says the Sunken Church "listened" and that the mages "went out from there". Only Rowan Mirewake knows the way. Rowan says no. **Beats:** (1) **No** (`S01`): Rowan declines, twice, dryly. The quest asks the player to do nothing hasty: the objective reads *Help at the landing.* (2) **Preparation** (`S02`, any order; each has a crew alternative that costs a day): **re-caulk the boat** with reed and resin (cut reed at the landing's own reed beds, Woodcutting a split root-knee for a thwart from reclaimed wood); **mend the tow harness** (Leatherworking repair of imported leather); **lantern moss** for the bow lantern (gather at Stillgrave's edge in the dark, where it glows; Reedlurkers; *Combat compliance:* to 0 HP, melee or ranged); **listen to Sennic** three times on different days (bells that rang without sound; mages who listened more than they spoke; the church going down "slow as a held breath"). Sennic's stories give *where* (the bell-side of the church faces the slack water; the altar is "under the big window"), never *why*. (3) **The knots** (`S03`): Rowan teaches in daylight at the landing. He ties knots in reed heads and makes the player read stakes and knots together on short practice runs (two channels, one wrong turn that simply grounds the boat). (4) **Asking** (`S04`, optional, across three separate visits): ask gently why he will not cross at night. The third time he tells it: the woman who taught him the route went out one night to fetch a sick child and did not come back, and he found her boat in the morning with her knots still tied (`MR_ROWAN_TRUST` = told). [NEW detail inside his ledger row: "learned the route from someone who never returned"; no war relation is given.] A player who never asks gets the crossing all the same (= kept); Rowan respects it and says so once. (5) **The crossing** (`S05`): at first light in fog (MD-3). Rowan poles; the player reads stakes and knots aloud through choices. A wrong call only means Rowan corrects and they wait in a side channel for the turn. Past the Drowned Encampment, Earthen Echoes form on the banks and wade toward the boat; the player fights from the boat's bow (ranged is natural here; melee works when they reach the gunwale; nothing in this fight requires either). **Strange moment:** passing Stillgrave, a bell rings across the water with no sound: the reeds flatten outward in rings, the fog shivers, and there is nothing to hear. Rowan does not look round. (6) **Arrival:** the roof lantern line of the Sunken Chapel comes out of the fog, half its lanterns dark. Mabyn Coyle, on the roof, says the line has been failing since spring. Complete at the roof. Unlocks the **Chapel route** (Rowan ferries the player to the Chapel at Slack, mornings and noons, poling his cuts and hauling the shoals `[MD-3]`; a Running or Sour channel means wait). *State compliance:* no step can fail; waiting is always available.

**MR-M4 The Chapel of the Sinking Star (`MCS`).** *Offer:* continuous from MR-M3. Mabyn will let the player in to help relight the inner line; she has not been below the gallery since the spate. **Beats:** (1) **The roof line** (`S01`): relight the outer lanterns (moss wicks from MR-M3, peat-wax from Mabyn). Teach the rule: lit posts hold ground; in the dark, Chapel Shades form and press the player back toward light and dim their lantern (hazard, §10). (2) **The gallery** (`S02`): down into the bell-loft and gallery above a flooded nave. Below the surface the stained glass is intact. The vestry door is under water. (3) **Staged drainage** (`S03`, the core puzzle): the chapel's culverts have three sluice boards, reached from three dry points. Each board works only at Slack (read the stake painted on the chapel's own buttress through a window). Opening a board in the wrong order backs water up and nothing drains (harmless reset). The order is read from the building itself: each culvert mouth carries an old water stain, and the board under the highest stain opens first. (Lowmark's outfall boards are read by rope wear; the Mire's version is deliberately read from the chapel walls so the puzzle does not repeat.) Each correct board drops the nave one stage, opens new ground, and leaves new posts to light before the dark ground fills with Shades. Silt Crawlers (fauna stirred by the draining) and Reedlurkers in the drained bays (to 0 HP, melee or ranged). (4) **The vestry** (`S04`): drained at stage two. A field post: an officer's dispatch case on a hook with a **regimental log** whose last entry is the same day as the MR-M2 logs, from a column the MR-M2 logs did not cover (required inspect; the second custodian; read in place). (5) **The crypt** (`S05`): at stage three, the altar under the great window stands clear. **Strange moment:** as the last water falls, the stained glass is lit from behind, gold and blue, by nothing; then it is only glass. The crypt steps go down beneath the altar. A lead-lined box: **the Memorywarden record** (`MCS_warden_leaves`, quest item): fired clay leaves, pressed with office marks and no names. The plan (*"lay the calm across the field of standards at the turning of the light; the ground will take what we give it; if we cannot carry it, it will carry us"*), a list of the stones to be held on Bannerline, a row of tally marks for those going out, and on the last leaf, in a different hand, a much shorter row for those who came back, and *"The circle is not closed. We could not."* No text states or totals a number (casualty counts stay withheld). With the vestry log, two custodians: the Memorywardens grounded the battlefield to stop the fighting, it worked, and it killed them (R08). The General is not named in the record; Ysolde, later, makes that link herself from the date and the ridge, and says it is her reading. (6) **Out** (`S06`): carry the leaves out by the lantern line; Shades press hard on the stairs; Mabyn holds the top post. **Choice** (`MR_WARDEN_RECORD`): **sorrowmere** (Ysolde's Memorykeepers keep the leaves and read them publicly; the register gains a page for people with no names), **altar** (resealed beneath the altar with Mabyn's prayers; Ysolde makes a reed copy of the last leaf), or **tenders** (kept in the Chapel-Tenders' roof loft, read to anyone Rowan brings). Each outcome keeps the knowledge public; CV-M1 reads the custody line. Complete at Blackwater Landing.

**MR-M5 Bannerline (`MBL`).** *Offer:* automatic after MR-M4 when the player next enters Sorrowmere or Griefwatch: Griefwatch's bell rings the closure, Ide Larrow has shut the Bannerline road, and Bran Hollowstep has walked down from his watchpost for the first time anyone remembers. **Situation:** the General's imprint is pushing out along Bannerline, drawing Hollowfoot drifters and Echo files down the road toward Griefwatch. The record says the circle on the crown was never closed. **Beats:** (1) **Bran's warning** (`S01`): at his watchpost, Bran teaches **the count** by feel: hand on the ground, two soft, then the third. "Move on two. Don't be there on three." He also points out a great furrow ploughed through the peat below the ridge, full of broken weapons and banner rags, and says "not tonight's trouble". (Sorrowback trail; MDS07; never followed in the Mire arc.) (2) **The road up** (`S02`): fight up the Bannerline road. `[MD-7]` Hollowfoot drifters wander a hollow below the road and react to noise and bright cloth (flavour; ordinary aggro); they are optional, avoidable by keeping to the road, never evidence, and fight to 0 HP with the ordinary defeat presentation. *MD-7 swap:* the drifters sit among the rags, non-hostile; the player may pass or sit with them, and they walk down to the wardens to be taken to Lysa. Echo files form in lanes on the count. Ide's Marshwardens hold the road behind the player (and, with `TH_STANDING`, a Thornfell Ridge Warden pair visiting Griefwatch [CANON] holds the far bend: optional variant). (3) **The ridge standards** (`S03`): the palisade holds the last battle's standards, risen. Retire three of them under the count (MR-M2's fold; the player now does it faster). With `MR_BANNERS` = restored, Corra brings the Banner That Sank Twice up from Griefwatch and stands it at the circle, and the ridge's standards answer it (a harder retirement, one more Wraith wave, one more ally line). (4) **The General** (`S04`, Act III boss, §10.1): at the muster post on the crown it coheres out of mud, iron and banner rags into the shape of a commander that is never quite one shape. It repeats orders without names: *"Hold." "Close up." "No one leaves."* A Marshfall man who came up with the wardens begs it, out loud, to say where his father fell. The player's tool beat: the player either answers him (*"It can't tell you. We can look in the books."*) or simply stands between him and the thing; the General never answers. Defeat it at 0 HP. It disperses. Mud still slides toward the gap in the circle. It will re-form tonight while the circle stands open. (5) **The circle** (`S05`, the rite): the circle has twelve stones and one gap. The player holds the **gap stone** (a channelled hold in three segments, progress kept) while the community comes up the road and stands at the stones, one by one. **Who comes is driven by earlier flags** (§9.3): Edris, Calwen, Mara, Ysolde, Mabyn, Rowan (if told), Nell and Dunstan, Oswin, Corra, Lysa with a settled Hollowfoot man she cares for, Bran, Ide; empty stones are filled by Griefwatch households. While they come, Echo files re-form and come down their lanes on the count; the player must step off the gap on two and back on after three (holding the gap through the third beat costs health, never the rite). Ysolde reads the **names roll** (`MBL_names_roll`, quest item, compiled from the register by Ysolde before the climb): only names with two holds are read as names; the rest are read as *"one we hold, not yet known"*. If MR-M1 was amended, Linnet Hayle's mother is read as a name. **Strange moment:** when the last stone is filled, the count stops mid-beat. In the quiet the ridge's standards lean, one after another round the ring, toward whoever stands nearest, and lie down without wind. (6) **Choice** (`MR_BANNERLINE`): **quieted** (the gap is closed with a new stone Mara chooses, the standards are laid in the earth inside the ring, Griefwatch opens the Bannerline road) or **tended** (the gap is left with a step in it, the standards are re-raised as Griefwatch's vigil banners in community colours, and the road opens under Griefwatch's watch with a vigil kept on the crown). Both quiet the ridge for the story. **Aftermath at Sorrowmere:** the meal first, then remembrance; Agna Ferrow makes the player sit. Sets `MR_STANDING`. Post-story, the General can be met again as **the Night Count** (MD-8). *Combat compliance:* every enemy to 0 HP; the General re-forms by condition, never by health; melee and ranged both fully viable (§10.1).

### 6.2 Main-quest contribution contract (§7.1, six fields)

| Code | Anchor | World-truth row | Revelation role | Recurring evidence (independent custodian) | State compliance | Combat compliance |
|---|---|---|---|---|---|---|
| MNS | Memorykeepers (Names Below); Sorrowmere and Marshfall households | H23 (recovery: fosterage, uncertain names) | Self-contained case; plants R16 (stranger's seat, unexplained) | Name-tape (Mara's marker) + care leaf (Edris's station) + Hayle book (Marshfall) + Edris's testimony; the reed charm (Nell) | `MR_NAME_RECORD` amended / qualified; no fail; hooks re-offer at the register | Griefbit beetles and one Banner Wraith to 0 HP; the Wraith re-forms at its standard (condition); melee or ranged |
| MBR | Banner and bone tenders; Bannerbearers | H12, H17 (seed), H25 present pressure (local) | Plants R08 (logs stop on one day; shard reacts to grief) | Unit logs (`MBR_unit_logs`) recur in MCS beside the vestry log (a different custodian) | `MR_BANNERS` retired / restored; `MR_CAUSEWAY` reset; folds cannot fail | Wraiths, Reedlurkers, the Risen Colour to 0 HP; Wraiths re-form while their standard is risen; no SX |
| MRC | Ferry households; Rowan | H12 (seed) | Plants R08 (Sennic's listening mages, soundless bell) | Sennic's stories (oral; leads only) | `MR_ROWAN_TRUST` told / kept; waiting always available; wrong reads ground the boat, never fail | Reedlurkers and Earthen Echoes to 0 HP; Echoes re-form on the banks while the fog lasts; ranged natural, never required |
| MCS | Chapel-Tenders | **H17** | **Owns R08** | Warden leaves (`MCS_warden_leaves`) + vestry regimental log (read in place); MBR logs add weight | `MR_WARDEN_RECORD` sorrowmere / altar / tenders; drainage puzzle resets harmlessly | Shades are a hazard (no HP); Reedlurkers and Silt Crawlers to 0 HP; melee or ranged |
| MBL | Griefwatch; the whole community | **H17** (consequence), H25 (Sorrowback seed only) | Pays off R08 as consequence; tool for the peace; seeds R14 and CV-M2 | Names roll (`MBL_names_roll`) built from two-hold register entries; Warden leaves' stone list | `MR_BANNERLINE` quieted / tended; a beaten player returns to Griefwatch with the quest Active; the circle always completes | Hollowfoot `[MD-7]` (human, optional) and Echo files to 0 HP, ordinary defeat; the General to 0 HP, re-forms by condition; no SX |

---

## 7. Side-quest slate (20 quests; Phase 1.5 range 16–22)

Three **interconnected questlines** (8 quests) and twelve standalone quests. **14 of 20 have no cross-region link or cross-region seed** (architecture rule: at least half self-contained). Codes are three letters beginning with M, never "MQ".

### 7.1 Interconnected questlines

| Code | Quest | Series (part) | Type | Unlock | Where | Core verb | One-line pitch | Feeds |
|---|---|---|---|---|---|---|---|---|
| MSS | **The Stranger's Seat** | Names Below (1/3) | Memory/lore | After MR-M1 | Sorrowmere register room, Griefwatch vigil hall, Rootrest | ask, compare, sit | Three settlements keep a stool on the visitor's side of their record tables and none can say why. Sit three hearings (a mooring claim, a recovered spoon, a lantern debt) and find the oldest seat. | **Plants R16** (a hearing that needs a stranger). Never explained in the Mire. `MR_STRANGER_SEAT` |
| MBA | **The Book of Arrivals** | Names Below (2/3) | Memory/lore (Register of the Unreturned, Mire case) | After MSS and MR-M3 | Sorrowmere archive loft, Marshfall | search, match, decide | A Marshfall foster household keeps a highstead tally token from "a man who came down from the high passes with the thaw". Find his care entry and decide what the arrivals wall says. | **Owns the Mire end of R14** (optional, exempt). Thornfell variants with `TWN_MIRE_HOOK` or TF-M5 (MD-14). `MR_ARRIVALS` |
| MEP | **The Empty Place** | Names Below (3/3) | Settlement | After MBA | Sorrowmere, Blackwater Landing | read, find, welcome | A child keeps leaving a work sign at the second place at her family's table. The adults think she is mourning an uncle. The ferry book says he is alive, working away, and stopped writing. | Optional Lowmark callback line (`CN_COMPLETE`: the player tells of the Holt boat); resolves locally. Names Below finale: the register gains a column for "away, not lost" |
| MLL | **The Broken Lantern Light** | Lanterns and Tenders (1/3) | Environmental | After MR-M1 | Stillgrave Hollow | gather, tend, finish | A Chapel-Tender's lantern will not stay lit at Stillgrave. A family's mourning circle there was abandoned halfway through, and the Hollow's grief sits in the water. Gather moss, mend the lantern, help the family finish. | Teaches lantern moss early; MR-M5 "finishing a circle" rehearsal; `MR_LANTERN_LINE` |
| MLW | **The Lantern That Would Not Go Out** | Lanterns and Tenders (2/3) | Memory/lore | After MLL and MR-M4 | The Chapel roof, Sorrowmere | read, craft, keep | Mabyn finds the Tenders' old wax book: the seven-night lantern was craft and stubbornness, kept for people who did not come back. Rebuild the lantern and choose who keeps it. | Supports R08 (the Tenders waited the same nights); keeps belief as belief |
| MLD | **Lifting Day** | Lanterns and Tenders (3/3) | Festival | After MLL and MR-M2 | The Standards Causeway, Sorrowmere | carry, cook, celebrate | The first dry stretch: the repaired way is walked at ordinary pace, children carry work signs, households eat before remembrance. Oswin wants to walk the causeway; Edris wants it walked last. | `[CAUSEWAY]`; Oswin and Edris stand together at MR-M5 |
| MBS | **A Banner With No Side** | Cloth and Colour (1/2) | Memory/lore | After MR-M2 | Calwen's sanctuary, Griefwatch | inspect, ask, retire | A banner stitched in a high-pass manner and mended in a lowland one. Two visitors each want it as proof. Calwen wants testimony, not a story. | Cross-region (stitch styles as leads only; no region proven). Mixed treatment crew suggested, never confirmed |
| MCF | **Cloth for Sale** | Cloth and Colour (2/2) | Combat challenge | After MBS | Marshfall jetty, the Reed Hide | track, assault, recover | Banner cloth is turning up at the Marshfall jetty as "commemorative goods". Follow it to the Reed Hide, where cutters strip risen standards in a drowned trench, and bring the cloth home. | Rootshadow cutters (human, to 0 HP); Gethin Scarth's ledger names the buyers' marks; `MR_CLOTH` |

### 7.2 Standalone side quests

| Code | Quest | Phase 1.5 type | Unlock | Where | Core verb | One-line pitch | Systems link | Cross-region |
|---|---|---|---|---|---|---|---|---|
| MRS | **Reed Shafts** | Skill intro (Fletching, Ranged, Hunting) | After MR-M1 | Fowling Meres, Marshfall | cut, fletch, shoot, pluck | Hob Merrit teaches fowling the Marshfall way: straight reed shafts, heron-feather fletching, and patience in a hide. | Fletching → Ranged → Hunting loop (CDR-2): select and cut reed shafts, fletch a bundle, shoot fen fowl from a hide; feathers return to Fletching. Item names are proposals for the economy pass (MD-11). | None |
| MFT | **A Table for the Wet** | Skill intro (Cooking) | After MR-M1 | Fenward Huts | gather, cook, serve | Lysa needs a meal that will keep for a week of flood for people who cannot cook for themselves. | Cooking intro: root and fowl stew, smoked eel (economy pass); care through food | None |
| MFH | **The Ferry Harness** | Skill quest (Leatherworking taught; requires Woodcutting [GD: entry level, reachable in the Mire]) | After MR-M1 | Blackwater Landing | strip, mend, fit | A ferry household's tow harness and thole pins have failed at the start of the long wet. Mend imported leather and cut pins from root-knees. | Leatherworking (repair) and Woodcutting (reclaimed wood) intro; no local tanning (source process) | None |
| MWS | **Weight of the Soil** | Settlement (Marshfall) | After MR-M2 | Marshfall walkways | repair, clear, decide | A Marshfall row is worn out: walkways collapsing, roots choking the paths, everyone tired. Clearing roots uncovers a buried Memorywarden marker under the worst walkway. Cleanse the site (dig the marker out and lift the walkway) or preserve it (route round it). | Dossier questline 4; Dunstan Hayle appears | None |
| MMR | **The Mud That Remembers** | Environmental | After MR-M2 | Drowned Encampment | observe, track, correct | A visiting Memorykeeper scholar is mapping "troop movements" in the mud and is sure they show a famous retreat. The prints repeat motions, nothing more; the camp's ration board tells what really happened there. | Dossier questline 2; Earthen Echoes; Fenny does flee before the player senses anything | None |
| MFW | **The Father at the Ford** | Memory/lore | After MR-M3 | The Wading Ford, Blackwater Landing | watch, read, ask | Travellers see a man knee-deep in the ford calling names. He never answers. A ferry list and a family naming habit may identify a real man who kept asking after evacuees. His descendants disagree whether "may" is a comfort. | The figure is an impression and never answers; the ferry list and the family are the holds | None |
| MSG | **The Singing Trench** | Environmental | After MR-M1 | The Singing Trench | listen, dig, prop | In storms a drowned trench hums. Memorykeepers say airflow; Tenders say grief. Both are partly right, and a collapsing revetment is about to bury a reed cutter's shortcut. | Echo-free puzzle: open and close trench vents in a storm window | None |
| MHG | **The Hushed Granary Key** | Settlement | After MR-M2 | The Hushed Granary, Sorrowmere, Rootrest | find, weigh, decide | The emergency store's key is gone before flood season. Theft, a flood bypass, or a frightened old custodian who will not be replaced? A family cannot wait for a hearing. | Lantern debt practice (MD-5) | None |
| MBO | **The Bell Roster** | Settlement (Griefwatch) | After MR-M2 | Griefwatch, the Dry Muster | audit, cover, account | Missed bells at Griefwatch are blamed on an old volunteer. Neighbours had quietly swapped shifts to protect a carer and never fixed the public roster. A visiting Ridge Warden wants an accountable substitute rule. | Ide Larrow; Thornfell Warden pair [CANON visits] | Thornfell (people only; reads `TH_STANDING` for one line) |
| MRW | **The Returning Wage** | Settlement | After MR-M3 | Rootrest | haul, mediate, accept | A worker home from Emberholt wage work to care for an elder is useful and suspect at the same table. Help him get the elder's peat stack in before the wet while the neighbours watch, then sit the table where his account of the war makes it worse. | Braid 11 shape; no Remnant, no Glassed Hollow | Emberholt (one person; no absolution of the war) |
| MNK | **Nine Stakes** | Combat challenge | After MR-M1 | Nine Stakes | read, clear, re-stake | Mud-Clad Raiders have pulled the stakes at Nine Stakes and wait for travellers who cross Sour. Clear them, then read the old depth marks and re-set the stakes so the crossing tells the truth. | Raider family; channel stakes; the nine stakes' history (one diversion saved a fleeing group) | None |
| MRH | **The Rust Hart** | Combat challenge (miniboss) | After MR-M2 | The Rust Hollow | track, read, fight | A great tarnish stalker with iron-stained antlers has made the ironbloom ground its own and charges anything on two legs. Its path is erratic, but its stops are not. | Tarnish Stalker miniboss; Hunting (tracking sign) | None |

**Structure check.** No two side quests share a core verb and setting. Combat is the core in MCF, MNK and MRH; present but secondary in MLL, MMR, MRS, MFH. Talk-led resolution is limited to closing beats.

**Skill coverage.** Hunting (MRS, MRH, MR-M1 line), Fletching and Ranged (MRS teaches both), Cooking (MFT, MR-M5 meal), Leatherworking (MFH, MR-M3), Woodcutting (MFH, MR-M3), Melee and Ranged (all combat; ranged is first-class, never required). No Mining or Smithing intro (MD-11). No main milestone hard-gates on a skill; every skill step has a crew alternative that costs time, not access.

**Self-contained count.** Cross-region links or seeds: MSS (R16 seed), MBA (R14, Thornfell variants), MEP (Lowmark line), MBS (stitch styles), MBO (Thornfell people), MRW (Emberholt person). The other 14 end where they begin.

### 7.3 Side-quest contribution contract (§7.1, six fields)

| Code | Anchor | World-truth row | Revelation role | Recurring evidence | State compliance | Combat compliance |
|---|---|---|---|---|---|---|
| MSS | Memorykeepers; Silt hearing | H07 (seed) | Plants R16 | None | `MR_STRANGER_SEAT`; hearings cannot be lost | None |
| MBA | Names Below; Marshfall host household | H16, H23 | Owns Mire end of R14 (optional) | Tally token + care entry; with Thornfell, the closure rubbing or Maera's slip as the other region's hold | `MR_ARRIVALS` (named / held); no fail | None |
| MEP | Sorrowmere households; ferry households | H23 | Self-contained | None | Outcome is the family's; no fail | None |
| MLL | Chapel-Tenders; Stillgrave | None (present-day grief) | Self-contained | None | `MR_LANTERN_LINE`; circle always completes | Earthen Echoes to 0 HP; re-form until the circle is finished |
| MLW | Chapel-Tenders | H17 | Supports R08 | Tenders' wax book (Mabyn) | Keeper choice flag (quest-local) | None |
| MLD | Reedsward; Bannerbearers | None | Self-contained | None | Celebration completes on walking the way | Griefbit beetles optional skirmish to 0 HP |
| MBS | Banner tenders | H23 | Self-contained (thematic link only) | Banner (Calwen's store) needs a second channel; none supplied, so no identity | Retire / keep (quest-local) | None |
| MCF | Rootshadow; Marshfall jetty | H25 (local) | Self-contained | Gethin's ledger (read in place) | `MR_CLOTH` returned / burned | Rootshadow cutters to 0 HP, ordinary defeat; Gethin never fights; melee or ranged |
| MRS | Marshfall hunters | None | Self-contained | None | No choice | Fen fowl (Hunting fauna) and one Reedlurker to 0 HP |
| MFT | Fenward care | None | Self-contained | None | No choice | None |
| MFH | Ferry households | None | Self-contained | None | No choice | Bog Hounds at the landing to 0 HP |
| MWS | Marshfall households | H05 (marker), H23 | Self-contained | Marker stays in place or with Calwen | Cleanse / preserve (quest-local) | Griefbit beetles to 0 HP |
| MMR | Memorykeepers | H12 | Self-contained | Ration board (read in place) | No fail | Earthen Echoes to 0 HP; MMR-E1 and MMR-E2 do not re-form; the stake-string Echoes re-form only while `S04` is active and stakes remain |
| MFW | Ferry households | H23 | Self-contained | Ferry list + family naming habit | Tell / keep (quest-local) | None (the figure is never hostile) |
| MSG | Memorykeepers and Tenders | None | Self-contained | None | No fail | Reedlurkers to 0 HP |
| MHG | Three settlements | H23 | Self-contained | None | Custody choice (quest-local) | None |
| MBO | Griefwatch | None | Self-contained | None | Roster rule choice (quest-local) | Bog Hounds on the Dry Muster to 0 HP |
| MRW | Rootrest households | H23 | Self-contained | None | No fail | None |
| MNK | Marshwardens; ferry households | H23 | Self-contained | None | No fail | Mud-Clad Raiders and the Mud-Boss to 0 HP, ordinary defeat |
| MRH | Marshfall hunters | None | Self-contained | None | No fail | The Rust Hart to 0 HP; harvestable per economy |

### 7.4 Micro-events (10; Phase 1.5 range 6–10)

| Id | Micro-event | Where | What happens | Interaction |
|---|---|---|---|---|
| MME01 | **Mood banners** | Sorrowmere raised ways | Street banners change colour with the settlement's week: grey after a burial, green on a birth, ochre when a way is closed. | Read; ask a Bannerbearer. |
| MME02 | **Soil before testimony** | Any hearing table | A witness touches soil from a bowl before speaking. "Habit." | Touch it or don't. |
| MME03 | **Lantern walk** | A raised path at dusk | A line of mourners walks with lanterns at ordinary pace; nobody overtakes. | Walk with them; don't overtake. |
| MME04 | **The second place** | Any household meal | An empty place is set; a child leaves a small work sign on it. | Ask; adults say it means "ask after someone", never "dead". |
| MME05 | **Mudstone faces** | Field edges after rain | The drying mud seems to make faces. A child names them; an elder tells the child to stop. | Look. Never explained. |
| MME06 | **The Turning Stone** | MP15, during a mourning rite | The flat stone turns a finger's width under the mourner's hand. | Put a hand on it during a rite. |
| MME07 | **The does go first** | Marshfall Edge | A small herd of fenny does bolts. A minute later the ground shudders. | Follow the does' lead. |
| MME08 | **Story circle** | Sorrowmere | A Memorykeeper teaches children "say whose story it is" before telling it. | Join; tell one. |
| MME09 | **Banner shadows** | The Field at dusk | Banners cast shadows longer than their poles. | Watch; Calwen: "Light bends round heavy cloth here." |
| MME10 | **Depth marks** | Sorrowmere jetty | Children play a jumping game on painted depth bands; the loser is "Sour". | Play; the game is the stake rule. |

### 7.5 Discoveries (three-layer framework)

Each has a surface (what anyone sees), a reading (what a careful player learns) and, where marked, a withheld layer.

| Id | Discovery | Surface | Reading | Withheld |
|---|---|---|---|---|
| MDS01 | **The Turning Stone** | A flat stone that turns under a hand. | It sits in a ring of sunken stones only visible at low water: one of an anchor circle [CANON]. | Whether the circle did anything. |
| MDS02 | **Stillgrave's reflection** | Water too clear; lantern light bends. | The reflection shows the bank as it stood before the war (old stilt-stumps). | Why. **Never explained.** |
| MDS03 | **The Sodden Pyres** | Burned trunks over warm, wet peat. | The peat smouldered for months [CANON]; ironbloom marks where the fires ran. | — |
| MDS04 | **The Dry Muster** | A gap in old drill lines. | A transferred list in Griefwatch's chest shows the gap was opened to move wounded and civilians. | Every claimed motive. |
| MDS05 | **The Unfired Kiln** | A children's rain shelter. | Promise marks in the wall: tallies of marker work never finished in a retreat. | Whose promises. |
| MDS06 | **Bannerline iron** | Red soil on the ridge. | Old palisade stakes and iron-rich soil [CANON]; tarnish serpents bask there. | — |
| MDS07 | **The great furrow** | A trench ploughed through peat below Bannerline, full of broken weapons and banner rags. | Bran: something big walks when there's fighting. "Not tonight's trouble." | **The Sorrowback.** Never followed in the Mire arc (CV-M2). |
| MDS08 | **The Last Root of Sorrow** | A black-rooted tree with white flowers [CANON myth]. | Rootrest's trees are its descendants; mourners hold griefroot here. | — |
| MDS09 | **The man from the fire roads** | A Rootrest care-book entry: burns, would not give his name. | Read only. Nobody here knows more. | **Held back** (MD-13, braid 12). |
| MDS10 | **Mirebone Crossing** | A ford littered with bone; animals avoid it; the ground shivers. | The bones are old and many; the ford shifts daily; no stake holds there. | Its future (convergence; provisional, MD-9). |

**Deliberately unexplained in the Mire forever** [PROPOSAL]: the origin of "Sinking Star" [CANON], the soundless bell, Stillgrave's reflection, the stained glass lit by nothing, Nell's lullaby, the Mudstone faces.

### 7.6 The Register of the Unreturned: shared civilian ledger (Mire cases)

Review §7 step 3 asks for this before the Mire bible. Each case resolves where its family lives; none is required by any milestone.

| Case | Region owning resolution | Mire hold | Other hold | Status |
|---|---|---|---|---|
| **Nell / Linnet** (MR-M1) | Mire | Care leaf, Edris's testimony | Hayle book (Marshfall), name-tape | Main path; local |
| **The Brede arrival** (MBA) | Thornfell (cairn); Mire (care entry) | Book of Arrivals entry; tally token | TF-M3 roster / TWN slip / TF-M5 rubbing | Optional; adds a record, settles nothing (MD-14) |
| **The Holt name** (MR-M1 hook) | Lowmark | Register search: not found, written | *The Candle Rule* | Honest no-record; Lowmark's garden stands |
| **The man from the fire roads** (MDS09) | Emberholt (later) | Rootrest care-book | None yet | Held back (MD-13) |

---

## 8. Revelation map (worked backward from the payoffs)

### 8.1 Owned revelations

| Rev | Truth | Owner | Custodians (two, never a phenomenon) | Seeds before payoff | Wrong reading supported | Guaranteed path |
|---|---|---|---|---|---|---|
| **R08** | The Mire's front stopped because the last Memorywardens grounded the battlefield; the overload killed them and concentrated the General. | MR-M4 | The Warden leaves beneath the altar (`MCS_warden_leaves`); the vestry regimental log (read in place). MBR logs add weight. | MBR unit logs stopping on one day; the shard reacting to grief; Sennic's listening mages and slow sinking (MRC); the soundless bell; the Lantern That Would Not Go Out (MLW); the Turning Stone (MDS01). | The Memorywardens cursed the land; the General is a real commander who would not die; the land swallowed the armies. | MR-M4 required inspects (vestry log, crypt leaves). |
| **R14 (Mire end)** | Some people stranded by Thornfell's sealings reached the Mire. | *The Book of Arrivals* (optional, exempt) | Book of Arrivals entry + tally token; with Thornfell content, the closure rubbing or Maera's slip. | TF-M3 / TWN / TF-M5 seeds; MR-M1 "not found" search. | The cairn is a lie; they all died. | None required (exempt by design). |

### 8.2 Seeds the Mire plants for others

| Seed | Where | Pays off | Rule |
|---|---|---|---|
| The stranger's seat | MR-M1; *The Stranger's Seat* | R16 (CV-M1) | Unexplained custom in the Mire. |
| The Warden record and its custody | MR-M4 | CV-M1 (Memorywarden record) | `MR_WARDEN_RECORD` custody line only. |
| Channel reading | §1.1, all milestones | CV-M3 footings | Readable-system reuse only. |
| The great furrow and Bran's warning | MR-M5; MDS07 | CV-M2 (Sorrowback) | Seen, never followed. |
| The man from the fire roads | MDS09 | R09 seed (EH-M3); braid 12 | Held as an unresolved name. |
| The names roll (two holds) | MR-M5 | CV-M3 "testimony that holds" | Practice only. |

### 8.3 Misunderstanding ladder in the Mire

| Topic | First reading | After MR-M2 | After MR-M5 |
|---|---|---|---|
| The Mire | A graveyard. | A community doing hard work on bad ground. | A community whose care stopped a war and still holds it. |
| The risen banners | Ghosts with messages. | Impressions woken by standing the standards up. | Consequences that need tending, never witnesses. |
| The Memorywardens | Villains who cursed the land. | Old practitioners whose relics react to grief. | People who broke themselves to make the fighting stop. |
| The General | A commander who would not die. | Something on the ridge that pulls at the field. | The field's own command, fear and obedience, repeating orders with no one in it. |
| The causeway | A practical fix. | The thing that woke the field. | A kind decision that needed a hearing first. |

---

## 9. World state

Solo-first (Pillar D): all state is per player. Co-op partners see presentation driven by their own state, with the Lowmark per-player prop pattern and its fallback (a shard-level fallback; Lowmark §8.1). **Presentation fallback only, governed by CDR-6 (2026-11-14):** every quest is completable by one player and co-op is optional assistance; where per-player props are not available, one shared visual state (for example the host's) may be shown. It never decides another player's walkable ground, interaction availability, step, credit or choice: each player's own quest state decides their own navigation, objectives, credit and completion, and each partner's own flags still drive their barks, dialogue and epilogue. Where a shared state would change navigation or gameplay, the conflict and the options are recorded for Sol (Integration MI-CO-06, §5.2 Q-18); no networking architecture is chosen here.

### 9.1 Region flags (persist on the character)

Prefix `MR_`. Quest-local flags use the quest code (`MNS_…`, `MBR_…`).

| Flag | Values | Set by | Read by |
|---|---|---|---|
| `MR_CHANNELS` | bool (stake reading learned) | MR-M1 | Stake inspect text everywhere; MR-M3 |
| `MR_NAME_RECORD` | amended / qualified | MR-M1 | MR-M5 roll and placement; *Weight of the Soil* lines |
| `MR_CAUSEWAY` | raised (default, unset) / reset | MR-M2 sets reset | Causeway props; *Lifting Day* |
| `MR_BANNERS` | retired / restored | MR-M2 | MR-M5 (Corra's banner, extra wave); Griefwatch props |
| `MR_ROWAN_TRUST` | told / kept | MR-M3 (a third ask after completion can upgrade kept to told until MR-M5 is Active) | MR-M5 (Rowan comes to the circle if told); post-story Rowan lines |
| `MR_WARDEN_RECORD` | sorrowmere / altar / tenders | MR-M4 | MR-M5 roll source line; CV-M1 custody |
| `MR_BANNERLINE` | quieted / tended | MR-M5 | Ridge state; Griefwatch lines; convergence |
| `MR_STANDING` | bool | MR-M5 | Mire master commissions; CV-M1 gate |
| `MR_STRANGER_SEAT` | bool | MSS | R16 chip; "witness" address variants |
| `MR_ARRIVALS` | named / held | MBA | R14 chip (CV-M3) |
| `MR_LANTERN_LINE` | bool | MLL | MR-M3 moss crew-alternative line; MR-M4 Mabyn line; MR-M5 placement |
| `MR_CLOTH` | returned / burned | MCF | MR-M5 placement (Calwen) |

### 9.2 Channel states (per player)

Each crossing has a small authored schedule of three states (Running, Slack, Sour) keyed to the existing presentation hour (Lowmark keep-watch convention: morning, noon, dusk, night). A state swaps walkable segments, stake water-line props and boat availability. **Waiting is always available** ("keep watch" until the next turn). Quests may pin a crossing's state for a step. No tide simulation, no per-tile mud, no world clock. Co-op: each player's walkable segments follow their own state; any shared stake presentation is provisional (MI-CO-06, CDR-6) and never gates navigation or credit.

### 9.3 Who comes to the circle (MR-M5)

The circle always completes; flags decide who fills which stone and what they say. There are twelve stones beside the gap: named characters take stones in the order below, anyone beyond twelve stands behind the stone of the person they came with, and Griefwatch households fill any stone still empty.

1. Always: Edris, Calwen, Mara, Ysolde, Bran, Ide, Mabyn, Lysa.
2. `MR_NAME_RECORD` = amended: Nell and Dunstan stand together; = qualified: Nell with Agna, Dunstan across the ring.
3. `MR_ROWAN_TRUST` = told: Rowan comes up from the landing. = kept: he keeps the landing lantern lit below and the player sees it.
4. `MR_BANNERS` = restored: Corra carries the Banner That Sank Twice. *Lifting Day* complete: Oswin stands beside Edris.
5. `MR_CLOTH` = returned: Calwen brings the recovered cloth to lay. `MR_LANTERN_LINE`: the Stillgrave family lights the ring.
6. `TH_STANDING`: a Thornfell Ridge Warden pair stands at the road stone. With TF-M5 completed, one of them mentions closure accounts in one line.

### 9.4 Shared conventions

- **Keep watch / quest clock** reused from Lowmark for channel turns and dusk Wraith timing: a per-player presentation hour, never world time.
- **Defeat** (CDR-1): every enemy is defeated at 0 HP with the ordinary defeat presentation. Earth-memory enemies collapse into mud and re-form while their condition lasts. No Mire SX entry.
- **Agility triggers** are optional shortcuts (walkway gaps, palisade climbs); every one has a walkable fallback.
- **Quest items:** Mire budget 4 (`MNS_name_tape`, `MBR_unit_logs`, `MCS_warden_leaves`, `MBL_names_roll`). Side quests use carry-state objects, read-in-place records, or none.

---

## 10. Encounter families (summary; full requirements in the Enemies package, Batch 4)

Nine families (Phase 1.5 §4.1) from dossier ecology. Marsh Rats are ambient vermin; mire boars, fenny does, silt crawlers, marrow herons, tarnish serpents and fen fowl are Hunting fauna that fight only when provoked and are not counted. Chapel Shades are an **environmental hazard** (no HP; they dim lanterns and press the player toward light). The Sorrowback is **not** a Mire encounter.

| Tier | Family | Role | Standard variants | Elite | First seen |
|---|---|---|---|---|---|
| Low | Bog Hounds | Hungry packs on peat paths | runner, gnawer | — (wildlife) | *The Ferry Harness* |
| Low | Reedlurkers | Amphibious ambushers in shallows; telegraph by reed-ripple | lurker, snapper | — (wildlife) | MRS / MLL / MSG (after MR-M1); main line MR-M2 ditch |
| Low | Griefbit Beetles | Swarm where fear rises; one extra swarm, once per fight, while a nearby NPC is still frightened (Enemies C-12) | swarm, carapace | — (vermin) | MR-M1 |
| Mid | Mud-Clad Raiders | Camouflaged bandits at bad crossings | mudcutter, reed-slinger | Mud-Boss | *Nine Stakes* |
| Mid | Rootshadow Cutters | Syndicate cloth-strippers; poisoned blades [CANON poisons] | cutter, poisoner | — | *Cloth for Sale* |
| Mid | Tarnish Stalkers | Erratic iron-antlered elk; stop-and-charge pattern | stalker, rutting stalker | **the Rust Hart** (side miniboss) | *The Rust Hart* |
| Mid | Hollowfoot | Human drifters driven by war trauma; react to noise and bright cloth (MD-7) | wanderer, shouter (calls others when struck) | — | MR-M5 |
| High | Banner Wraiths | Impressions tied to risen banners; dusk; re-form while risen | wraith, bearer (buffs nearby wraiths while its standard stands) | **the Risen Colour** (MR-M2 miniboss phenomenon; never named in UI) | MR-M1 |
| High | Earthen Echoes | Mud figures repeating motions; collapse when struck; re-form by condition | echo, file (moves in lanes on a count) | **the General Who Wouldn't Fall** (MR-M5 boss) | MLL / MMR (after MR-M1 / MR-M2); main line MR-M3 |

**Elites.** Phase 1.5 §4.2 asks for one elite per non-wildlife family. Rootshadow Cutters and Hollowfoot have none on purpose: Rootshadow avoids large conflict [CANON], and no Hollowfoot person is ever made a boss (MD-7). Recorded deviation. The rutting stalker is placed by the Enemies package as MW-03, or cut (count 21).

**Count:** 18 standard variants + 4 elites (Mud-Boss, Rust Hart, Risen Colour, the General) = **22**. **Bosses:** 1 Act III boss (the General) and 2 minibosses (the Risen Colour, the Rust Hart), matching Phase 1.5 §4.3. The General is one of the Mire's two canon major threats; the Risen Colour is a minor/local phenomenon [C15].

**Ranged and melee (CDR-2).** Every encounter is designed for both. Reed-slingers and Reedlurker spit give ranged players something to answer and melee players cover to close behind. Wraiths and Echo files are slow and readable, so ranged kiting is valid but bounded: they re-form at their condition, so out-ranging them never ends a fight on its own. No fight needs ranged.

### 10.1 Boss brief: the General Who Wouldn't Fall (MR-M5)

| Element | Brief |
|---|---|
| Arena | The crown of Bannerline: the muster post, the palisade arc, the twelve-stone circle with its gap. Three lanes run from the palisade down to the circle. |
| The count | The ground pulses two soft beats, then the third (a deep thud and a visible ripple through the mud). On the third, the General's files advance one lane-length and the General issues an order. Audio and a ground-ripple decal both carry the count (accessibility). |
| Phase 1: "Hold" | Two Echo files hold the lanes; the General stands at the post. Clear files between strikes; striking the General while a file holds its lane is shielded (readable: mud plates on its front). |
| Phase 2: "Close up" | Files converge on the player's lane. The General moves into the lane and strikes on the third beat. Ranged players must keep moving lanes; melee players fight inside the turn. |
| Phase 3: "No one leaves" | The arena edge thickens with banner rags (no exit pressure, only a visual). The count keeps its three beats but quickens. The General's strikes leave mud that slows for a short time (a standard slow debuff). At 0 HP it collapses into the ground; mud slides toward the circle's gap. |
| Defeat | 0 HP. It disperses for the night. It re-forms at the next night while the circle stands open (condition), which is why the rite follows at once. |
| Failure | A beaten player wakes at Griefwatch with the quest Active and the step unchanged. No checkpoint loss of progress already made in the rite. |
| Never | It never speaks a name, a unit or a place. It never answers a question. It is never called a ghost by any Memorykeeper or Tender. |

---

## 11. Authoring conventions (binding for every Mire package)

1. **Format.** Quest packages follow the Lowmark act-package format (`Caelmor_Lowmark_Main_Act_I.md`): the quest in one paragraph, selection record, canon grounding, summary card **with all six §7.1 contract fields** (Anchor, World-truth row, Revelation role, Recurring evidence, State compliance, Combat compliance), places, player-facing beats with objective text, encounters, discovery presentation spec, steps table, flags table, choices and consequences, rewards, failure/recovery/co-op, integration needs, mystery-ledger entries, open decisions, internal review log. Dialogue follows the Lowmark dialogue-file node format and §5.3 voice rules.
2. **Ids.** Content ids `mire.main.NN_slug` and `mire.side.slug` (suggested; the Schema & Content Engineer owns naming). Steps `S00_…`. Quest-local flags `<CODE>_…` with three-letter M codes (never `MQ…`); region flags `MR_…` from §9.1 only. Dialogue nodes `<CODE>-D<n>.<nn>`; barks `<CODE>-B<n>.<nn>`; encounters `<CODE>-E<n>`. POIs `MP##`, micro-events `MME##`, discoveries `MDS##` with `MDS##_SEEN` / `MDS##_READ`.
3. **Evidence rule.** Phenomena never identify a person, prove guilt, settle a claim or name the dead. **Combat never reveals evidence, and no defeated enemy ever speaks testimony.** Registers, household books, objects, places and living witnesses do; every revelation has two holds (§8).
4. **Three states only.** Inactive, Active, Completed. No fail or abandon logic. A player who walks away resumes at the persisted step through an authored resume hook (default: the original offer, re-offered at the giver). Choices are outcome flags. Missed moments (a dusk Wraith, a channel turn, an optional ask) are re-offered at the next turn.
5. **Combat (CDR-1, CDR-2).** Every enemy fights to 0 HP. No yields, no break-off, no "downed" state, no tied props. Earth-memory enemies re-form only by a place condition. Every fight can be won with melee or ranged; none requires ranged. The Mire registers no SX exception.
6. **Rewards.** Access (Rowan's Chapel route; the Bannerline road), knowledge (channel reading), small payments, standing, tools named functionally ("a ferryman's pole", "a fowler's bundle"). No lump quest XP. No new items beyond the four quest items unless the item pass defines them.
7. **Tone.** Heavy, plain, kind, with dry humour at tables. At least one moment of wonder or unease per quest. No exposition dumps. No cutscenes; the camera stays with the player.
8. **Magic stays dormant.** No Mire NPC practises or recognises magic; Memorywardens are history, not a present faction; no player spellcasting.
9. **Causeway tagging.** Any node naming Oswin Garvey's causeway decision is tagged `[CAUSEWAY]` (§3.1).
10. **Map.** Relative placement only; mark **MAP VERIFICATION REQUIRED**. No route or direction to another region. No "eastern" or "invader" wording. Mirebone stays a ford.
11. **Status labels.** [CANON], [APPROVED — id], [NEW], [PROPOSAL — DIRECTOR], MAP VERIFICATION REQUIRED.
12. **Scope.** No schema, JSON or C#. No Mire content requires Lowmark or Thornfell completion; callbacks are optional variant lines read from their flags.

### 11.1 Mechanics: standard RPG systems (CDR-4)

| Mechanic | System used | Status |
|---|---|---|
| Inspect, carry-state objects, read-in-place records | Lowmark/Thornfell interaction set | Standard |
| Channelled interactions (lift a pole, fold a banner, hold the gap stone, wind a sluice) | Lowmark channel convention with kept progress | Standard |
| Folding a banner by seams; sluice order read from the culverts' water stains | Interact sequence with harmless reset | Standard |
| Showing evidence to an NPC | Use-item-on-NPC / dialogue options gated by quest flags | Standard |
| Boat crossings with Rowan | Lowmark ferry convention (*Night Ferry*): an escorted ride on a fixed route; choices in dialogue | Standard |
| Wading and causeways | Walkable segments toggled by state; deep water is non-walkable | Standard |
| Earth-memory re-forming by condition | Lowmark drift-site state model | Standard |
| Boss telegraphs (the count, lanes, shield plates, slow) | Ordinary boss telegraphs and a standard slow debuff | Standard |
| Agility shortcuts | Phase 1.3 agility triggers with walkable fallbacks | Standard |
| Waiting for a turn | Lowmark keep-watch presentation hour | Standard |

**Explicitly not used:** swimming, breath or air meters, per-tile mud physics, stamina, new UI modes, a tide simulation, a reputation meter.

### 11.2 Needs that may require new runtime support (few; for the integration handoff)

| # | Need | Smallest form | Fallback if not built |
|---|---|---|---|
| N-1 | **Channel-state schedule per crossing** keyed to the presentation hour (three states, prop and walkable-segment swap) | A per-crossing state table read by the existing world-state variant system | Quest-pinned states only (each step sets the state it needs) |
| N-2 | **One lit-radius effect off a lit prop**, two uses: a lit Chapel post suppresses Shade spawns in its radius (MR-M4); a lit lantern slows Earthen Echoes in the same radius (*The Broken Lantern Light*) | Spawn gating and one standard slow by a prop's lit/unlit state | Pre-authored lit/dark zones that flip at each drainage stage; MLL drops the slow and loses one wave |
| N-3 | **Staged water level** in the Chapel nave (three discrete levels) | Three environment variants swapped by quest step | None needed; this is the fallback form |

These are the only three. The Griefbit fear add is an ordinary encounter timer cancelled by the calm event, one pattern for MNS and MWS (Enemies C-12), not a new need. Integration ids: N-1 = MI-CH-01, N-2 = MI-LT-01, N-3 = MI-WL-01.

---

## 12. Production plan and file map

| Batch | Content | Files | Status (2026-11-09) |
|---|---|---|---|
| 1 | This bible | `Quests/Caelmor_Mire_Narrative_Production_Bible.md` | Reviewed 2026-11-07; Batch 4 cross-package fixes in review |
| 2 | Milestone packages and dialogue | `Quests/Caelmor_Mire_Main_Act_I.md` (MR-M1, MR-M2), `_Act_II.md` (MR-M3, MR-M4), `_Act_III.md` (MR-M5) and matching `Dialogue & Narrative/Caelmor_Mire_Main_Act_<n>_Dialogue.md` | Reviewed 2026-11-08; Batch 4 alignment edits in review |
| 3 | Side quests, micro-events, discoveries | `Quests/Caelmor_Mire_Side_Quests_Names_and_Lanterns.md` (MSS, MBA, MEP, MLL, MLW, MLD); `…_Cloth_and_Memory.md` (MBS, MCF, MFW, MMR, MSG); `…_Work_and_Skills.md` (MRS, MFT, MFH, MWS, MHG); `…_Settlements_and_Combat.md` (MBO, MRW, MNK, MRH, MME01–MME10, MDS01–MDS10) | Reviewed 2026-11-09 (e98147e); Batch 4 alignment edits in review |
| 4 | Encounters, POIs, integration handoff | `Enemies/Caelmor_Mire_Encounter_and_Enemy_Requirements.md`; `Zones/Caelmor_Mire_POI_and_Zone_Requirements.md`; `Quests/Caelmor_Mire_Integration_Requirements.md` | In review (independent review 2026-11-09) |
| 5 | Independent review and fix pass | Revisions in place; review log in each package | Running per batch |

**Authoring order inside the Mire** (Review §7): R08 and its custodians first (MR-M4), then the capstone (MR-M5), then the act turn and entry (MR-M2, MR-M1, MR-M3); then seed placement; then series that carry seeds (Names Below, Lanterns and Tenders); then the self-contained slate; then micro-events and discoveries; then independent review.

**Production dependencies (not narrative work):** quest step/flag schema (Roadmap 31.3), dialogue schema (31.5), NPC schema (31.2), zone and encounter data (31.4, 33.7), runtime step tracking (24.1), the Mire map pass, and the economy pass for reed shafts, fen fowl and griefroot. Nothing here waits on them; nothing here implements them.

---

## 13. Internal review log

**Status: draft; independent review done 2026-11-07; Batch 4 zones/integration review fixes 2026-11-09 (last row of the table below).**

| Package (Batches 3 and 4) | Status (2026-11-09) |
|---|---|
| `Quests/Caelmor_Mire_Side_Quests_Names_and_Lanterns.md`, `…_Cloth_and_Memory.md`, `…_Work_and_Skills.md`, `…_Settlements_and_Combat.md` | Independently reviewed (e98147e); Batch 4 alignment edits in review |
| `Enemies/Caelmor_Mire_Encounter_and_Enemy_Requirements.md` | In review |
| `Zones/Caelmor_Mire_POI_and_Zone_Requirements.md` | In review |
| `Quests/Caelmor_Mire_Integration_Requirements.md` | In review |

| Check | Result |
|---|---|
| Architecture fit | Five milestones match Arcs §3.2 in name, order, purpose, revelation and flag (`MR_NAME_RECORD`, `MR_BANNERS`, `MR_ROWAN_TRUST`, `MR_WARDEN_RECORD`, `MR_BANNERLINE`, `MR_STANDING`). R08 owned by MR-M4 with altar record plus one regimental log, as the ledger requires. R14 Mire end optional. R16 and R09 seeds placed, not revealed. |
| Rulings | CDR-1: all enemies to 0 HP; earth-memory re-forms by condition; Hollowfoot treated as human per canon (MD-7); no SX proposed; no testimony from defeated enemies. CDR-2: ranged first-class everywhere, Fletching/Ranged intro (MRS), never required. CDR-3: milestone language only. CDR-4: standard systems table (§11.1); three narrow runtime needs (§11.2); breath management replaced (MD-4). |
| Canon and ledger | One chapel, three names, origin unexplained [C14]; two major threats, the Sorrowback not a Mire boss [C15]; Rowan the only guide, never crosses at night (MD-3); Sennic gives where, not why; Bran's knowledge limited to his own watch; Edris owns only her own care account; Calwen never names a side; Mara never names a stone. Memorywardens not a present faction. |
| Open items respected | D-E2, D-S1 untouched; no "eastern" or "invader" wording; origin-neutral player (D-3); C07 untouched; Glassed Hollow arrivals held as an unresolved name (MDS09); Mirebone provisional and unused as a site; no trade routes. |
| Counts | 28 POIs; 20 side quests (14 self-contained); 10 micro-events; 10 discoveries; 9 families, 22 variants; 1 boss, 2 minibosses; 4 quest items. |
| Three states | No fail or abandon anywhere; every wait is available; the circle always completes; a beaten player returns to Griefwatch with the quest Active. |
| Independent review (2026-11-07) | 19 findings (3 high, 8 medium, 8 low), all fixed in place. **High:** the post-story refight was called "the Muster", Lowmark's Act III boss (now "the Night Count", MD-8); the Warden leaves gave a count out and a count back, which would state how many died (R08/FT-02 withhold casualty counts; now tally marks, never a stated or totalled figure, MR-M4 and MD-6); Corra Sallis was "Merrin", an existing Lowmark NPC (Greyharrow). **Medium:** the General's three-soft-then-fourth count copied Lowmark's four-knock Muster count (now a three-beat count: move on two; §1.1, MR-M5, §10.1); the chapel's three sluice boards were read by rope wear exactly as in Lowmark's *The Candle Rule* (now read from water stains on the chapel walls); the capstone's "every banner lies down at once" mirrored Lowmark's "every Marking Stone holds at once" (now the count stops and the standards lie down one after another toward the people at the stones); MR-M1's night cart "for Rootrest" ran back toward Sorrowmere and the strange moment sat at Fenward (now the cart returns to Sorrowmere and the moment is at the Ferrow house); the name-tape was read in place yet listed as quest item `MNS_name_tape` (now carried); Sennic's "star window" hinted at the never-explained "Sinking Star" (now "the great window"); the circle has twelve stones but up to sixteen attendees (overflow rule in §9.3); Rootshadow and Hollowfoot lack the Phase 1.5 elite (recorded as a deliberate deviation in §10); Gethin Scarth and Oswin Garvey renamed from Tobin Scarth and Oswin Tarr, too close to Lowmark's Tovin (canon anchor) and Wynn Tarrow. **Low:** MR-M2 summary row contradicted its beat (shard glow vs. moss and silt); MR-M2 lacked Mara on site and the Arcs "route repair" verb (added); POI categories and count line inconsistent for MP17, MP18, MP28 (fixed; total still 28); `MR_CAUSEWAY` set "raised" by an MR-M1 beat that never set it (now the unset default); the Lantern myth's craft reading and Rowan's teacher story tagged [NEW]; Silt Crawlers marked as stirred fauna; *The Returning Wage* given a concrete task; Phase 3 "three beats in total" clarified. **Verified unchanged:** every [CANON] claim against the dossier, anchors, Timeline §V (FT-02c is now Timeline canon), Factions §17 and the Part 4 ledger rows; MR-M1..M5 purposes, revelations and the six flags; Sorrowback trail-only; CDR-1..4 (no SX, no yields, ranged never required, no release wording); three-state lifecycle; codes (`MNS_`/`MNK_` do not collide with Lowmark `MN_`; `MR_` vs `MRC_`/`MRS_`/`MRW_`/`MRH_` are distinct strings but read alike, so validators should match the trailing underscore); cross-region flags `TH_STANDING`, `TWN_MIRE_HOOK`, `CN_COMPLETE`, `FC_SEAL_NOTED` exist in their owners; counts (28 POIs, 20 side quests with 14 self-contained, 10 micro-events, 10 discoveries, 22 variants, 4 quest items). **For the Director:** MD-7 (Hollowfoot as killable humans in a region whose canon tone is merciful), MD-3 and MD-4 (both amend approved Arcs §3.2 wording). Recommendation for the Gameplay Designer: CDR-4 asks for meaningful skill requirements, and no Mire quest has one yet; light level requirements on a few side quests (MRS, MFH, MRH) would fit. |
| Batch 4 zones/integration review, 2026-11-09 | Cross-package conflicts resolved to the reviewed act packages, text only (no id, step or flag renamed): §11.1 sluice order now read from **water stains** (was rope bands; Act II §B8.2); §1.1 Slack now says boats ground on the shoals and Rowan poles his cuts and hauls the shoals, and §6.1 MR-M3's Chapel route says mornings and noons `[MD-3]` (Act II A14.2); MR-M3 reed is cut at the landing's own reed beds (Act II A14.3); §4.2 states the Bran's-watchpost path requirement (never through the closure gate; MAP VERIFICATION REQUIRED) and the Bannerline road's pre-MR-M5 state as the packages give it, crown access left open (Zones Q-3); §9 records the recommended host-state co-op rule (Integration MI-CO-06, pending Director review). Enemies §13.3 bible rows applied: Reedlurker and Earthen Echo "First seen" (I-3, I-4), the in-fight re-form layer in §2.6 (I-5), the rutting stalker note (I-15). §11.2 N-2 now covers both lit-radius uses as one need, and the Griefbit fear add is stated once (C-12). MR-M5 beat 2 and §6.2 now keep Hollowfoot optional and avoidable with the MD-7 swap line (the old beat read as a required fight). §9.1: `MR_ROWAN_TRUST` post-completion upgrade and the MR-M3 `MR_LANTERN_LINE` read recorded. §12 and §13 now carry package status. |
| Playability audit fixes, 2026-11-13 | SM-13, SS-02 (option a: MLD no longer needs MLW; option b recorded in MLD's open decisions), SS-06, CO-01, CO-02. Authored walkthrough only (no Unity build exists; nothing was played). Text only; no id, step, flag or geography changed; no Director recommendation promoted. |
| Playability audit fixes review, 2026-11-13 | Independent review of the same-day fixes. §2.6 outside-encounter re-form aligned to Enemies C-3 as changed by SM-14 (when a quest next presents its condition; pending GD). Authored walkthrough only; text only; no id, step, flag or geography changed; no Director recommendation promoted. |
| CDR-6 solo-completion sweep, 2026-11-14 | §9 co-op paragraph: presentation fallback only, governed by CDR-6 (every quest completable by one player; co-op optional). MI-CO-06 references restated likewise. Text only; no id, step, flag, line or geography changed; Sol's co-op conflicts kept as presentation questions. |

**Source contradictions found (for the reviewer and the Director):**

1. Arcs §3.2 MR-M3 calls for a "guided night crossing"; Rowan's canon anchor refuses night crossings. Resolved here as a first-light crossing (MD-3).
2. Arcs §3.2 MR-M4 calls for "breath and lantern management"; Phase 1.3 has no swimming, and CDR-4 discourages a breath system added for realism. Replaced by staged drainage (MD-4).
3. The dossier and the coordinator brief differ on Hollowfoot: canon makes them humans; the brief listed them with spirit enemies. Content follows canon under CDR-1 with dignity rules (MD-7).
4. "Reedsward" is a civic work rota in the Part 3 Mire proposal and a place name in the merged overview (architecture contradiction 5). Used here only as the rota (MD-5).
5. The dossier's §II "eastern incursions" and §XXI "V1 is Lowmark-only" wording conflict with architecture contradiction 3 and CDR-3; neither is used.
6. Arcs §3.2 describes channel states as "learned rather than marked", while CDR-4 favours readable world markers. Resolved as vernacular world markers the player learns to read (stakes, knots, moss), with no UI marking.
7. The Part 6 readiness pass lists Mire timber/fletching and smithing as gaps; reed fletching is therefore a proposal for the economy pass, and the Mire has no Smithing or Mining intro (MD-11).
