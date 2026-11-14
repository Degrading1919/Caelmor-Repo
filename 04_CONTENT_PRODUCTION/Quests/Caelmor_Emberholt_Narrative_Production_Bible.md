# Emberholt Heights: Narrative Production Bible

**Status (2026-11-14):** Draft production direction, **independently reviewed 2026-11-14 and still in review** (§13): nothing here is approved by that review. This is the controlling document for every Emberholt quest, NPC, dialogue, encounter, discovery and world-content package, in the way `Caelmor_Mire_Narrative_Production_Bible.md` controls the Mire. It turns the approved narrative architecture (`Caelmor_Narrative_Architecture.md` and its four companion files; rulings in `Caelmor_Narrative_Architecture_Review_and_Authoring_Sequence.md` §5.0) into a concrete, playable slate for Emberholt Heights. Everything marked **[NEW]** is authored here and is not canon until the Creative Director promotes it. Everything marked **[PROPOSAL — DIRECTOR]** is a consequential story choice the content is built on but that Collin may replace; §3 lists exactly what changes if he does. Decisions in §3 are **recommendations for the Director, never rulings.**

**Scope guard.** Emberholt is the **Emberholt milestone**: an internal production milestone of the complete game, not a separate release (CDR-3; the first public beta contains the complete planned game). It follows the Mire in production order (D-R1) and is not a required player order. This package authorizes **no** scope change, no new system, no schema, no production JSON and no C#. It is schema-ready markdown for the day Roadmap 31.2/31.3/31.5 exist (Master Protocol §5.1). Technical needs are listed in §11.2 and roll up into a later Emberholt integration handoff (§12, Batch 4); nothing here implements them. **No Emberholt terrain, map or zone exists yet**; every placement in this file is relative and provisional.

**Binding rulings:** `Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md` (CDR-1 defeat at 0 HP and scripted survival only through the §4 register; CDR-2 ranged first-class and never required; CDR-3 no partial release, regions are internal milestones; CDR-4 RuneScape-style structure and ordinary RPG mechanics over bespoke simulation; CDR-6 every quest, boss and reward completable solo, co-op optional assistance only) governs wherever this bible could disagree. The §7.1 contract (six fields; the Combat compliance field includes the CDR-6 solo test) applies to every quest card.

**Director rulings this bible builds on:** FT-02 and FT-02d (Emberholt's war ended in the Glassed Hollow, hidden as a forge collapse); FT-04 (Perfect Flame is the attempt to make advanced embercraft reproducible through conditioning plus controlled knowledge; outside Emberholt only specific, bounded, discoverable acts); FT-05 as **direction only** (the Fire Titan is a suffering transformed initiate; the Last Binding ends in containment; mechanics still subject to review); D-C03 (limited personnel continuity from precursor to Remnant; no precursor name; no survivor roster); D-C06 (Volkhari unnumbered; individuals only); D-CV1 (the Titan bound to rest; release open).

**Reserved for the Director and not decided here:** D-E2 (Thalan's fates), D-S1 (the Speaker's knowledge), the eastern "invaders" wording (architecture contradiction 3), character origins (D-3, contradiction 6) and C07 (Founders). Where content needs them it is written around them on the architecture's recommendation and the dependent nodes are tagged (`[D-E2]`, `[D-S1]`) so a ruling changes only those nodes (§3.2).

**Authority used (in order):** the rulings file above; Phase 1.1–1.5 (superseded by the rulings where they say "Lowmark only" or "no ranged"); the approved architecture (Arcs §1.3, §3.3, §4, §6; World Truth H02, H03, H05, H09, H13, H18–H22, H25, C.1–C.3, C.7, C.8, B.2, B.3; Revelation Ledger R09–R12 owned, seeds for R15, R16, R18, R19; Review §2 contradictions 2, 3, 6, 7, 8, §5.0, §7, §7.1); canon lore (`LORE/Regions/Caelmor_Region4_EmberholtHeights.md`, the dossier; `LORE/Factions/Caelmor_Factions.md` §1–§14; `LORE/Characters/Caelmor_Characters_Region4_Emberholt.txt`; `LORE/Timeline/Caelmor_Timeline.md` §V–§VIII; `LORE/Worldbuilding Docs/Caelmor_War_History.md` §IV–§IX); `00_ADMIN/Reference/Caelmor_Part4_Character_Family_Continuity_Ledger.md` for every character limit. Proposal sources, cited but not promoted: `00_ADMIN/Reference/Caelmor_Part3_Emberholt_Proposal.md` (story networks, Cooling Houses, Heat Commons, First Cooling, Half-Name Wall, Cold Seam, Bridge of Seven Repairs), `Caelmor_Regional_Source_Process_Emberholt_Proposal.md` (imports, timber and fuel dependence, the postwar safety boundary), Part 4 shared events 5 and 6 and the relationship web (braids 9, 11, 12). Cross-region callbacks are read only from flags their owners define (Lowmark `HS_*`, `UL_*`; Thornfell `TH_STANDING`, `TAS_ACCOUNT`, TF-M3; Mire `MR_STANDING`, `MDS09_READ`, MR-M2). Format and rigour follow the Mire bible.

---

## 1. Emberholt in one page

***The Brightest Flame.*** The player comes into **Cinderwall**, Emberholt's lowest working ward, on an evening when a city built on volcanic heat is cold. People who have never owned a coat are wearing two. The ward's fire warden, **Veska Dunmor** [NEW], is being shouted at in the Cooling House because her junction is the one that went dark.

Over six milestone quests the player learns why a city that makes fire safe for everyone keeps finding that safety is not shared.

**The answer has three parts, and the player learns them in this order:**

1. **The city's heat follows influence, and its schools sort its children.** Cinderwall went cold because a ceremonies-office order sent the ward's heat to the Ash Terraces for a festival rehearsal, signed at an Ashspire salon's request; the warden protested and was overruled, and her protest was cut out of the book. Up the Molten Stair, the academies that teach every child to light a lantern are also measuring which children can be pushed. Nobody in either story is a villain. The wardens and teachers are good at their work. (Act I: EH-M1, EH-M2)
2. **The forge collapse was the end of Emberholt's war.** Following a contract crew that Deepbrand lost near the old Hollow, the player crosses the **Glassed Hollow** and puts site evidence beside a restricted record with provenance: in the war's last year the wartime precursor ran an amplification ritual with Volkhari captives to end the war in the city's favour; a precursor initiate became what the legend calls the Ash-Clad Giant; a Volkhari child walked out of the fire; and one Volkhari elder was taken in the purges afterwards and held below. Only in Act II does the player learn he is still alive, and find him (R10 belongs to EH-M4). (Act I turn and Act II: EH-M3, EH-M4)
3. **What is hidden is still drawing on the city.** The Flameward Speaker smiles over rehearsals that teach a crowd to breathe as one, and his own visions are given to him in Hearthveil's sleep rooms. Under Cinderwall, draw lines spliced into the civic heat main have been feeding the deep works for years. In a hard frost the main fails. The player goes down with the wardens, chooses where to bleed the pressure, cuts the draw, gets the cold ward through the night, and carries what was found up to a public tally board. (Act II turn and Act III: EH-M5, EH-M6)

The player leaves with Emberholt's tool for the peace: **accountable power**, a civic account that separates useful fire from hidden harm. Where the heat goes is written where anyone can read it.

**Emotional line (Phase 1.1 §6):** Wonder (a lantern lit by a guard's gesture at Embergate; a whole terrace of flames steadying with one breath) → Competence (reading tells, vent breath and a valve board) → Attachment (Veska's stubbornness, Tavi's class, Darven's need to be believed, Thalan's dignity) → Agency (who sees the order, where the ledgers go, what the crew's families are told, what happens to Thalan, how the Speaker is faced, where the heat goes) → Mastery (heat routes, Smithing master commissions, the heat reading the convergence's curing and sealing will need).

**What makes it an RPG and not a lecture:** every quest has a route through heat to read, something to forge or mend, danger that telegraphs, and a moment that is strange. The city is beautiful and competent first. The player sees it working before they see what it hides.

### 1.1 Emberholt's readable system: heat

Lowmark taught water against a marking stone, Thornfell taught sound, the Mire taught ground. Emberholt teaches **heat**: where it is, where it is going, and what is pushing it. It is learned knowledge (Pillar A), never a spell, and every element is a **world marker the player looks at**, not a UI mode or a meter.

| Element | What the player learns | Where first taught | Used again |
|---|---|---|---|
| **Tells** [NEW] | Fire wardens set a bead of emberglass in every vent hood, junction and main valve. A tell is **clear** when the line is **Cool**, **amber** when it is **Working**, and **red with a crazed skin** when it is **Surging** (do not pass, do not touch). The colours borrow the city's own street code (yellow calm, orange productive, red volatile [CANON, Cinderweave banners]). Each zone changes state on a small fixed pattern keyed to the presentation hour (morning, noon, dusk, night); quests may pin a state. | EH-M1 (walking the line with Veska's crew) | Every milestone; *The Flarecap Seam*; EH-M6 at its hardest |
| **Vent breath** | Floor vents and wall ducts exhale on a cycle. Ash lifts off the grate a moment before each exhale; walk on the rest. A breathing vent is an ordinary timed hazard (damage and a short knock-back), never a puzzle of numbers. | EH-M1 | EH-M3 glass, EH-M4 Warrens, EH-M6 main, the Draw Sentinel |
| **Cooling niches** [NEW on Part 3 Cooling Houses] | Wardens wash safe alcoves blue and keep a quench trough in each. Hot zones deal ordinary periodic damage; standing in a niche stops it. The wardens' rule: *never pass a niche without touching water.* There is no heat meter: heat is terrain, not a stat. | EH-M1 | Every descent |
| **Flarecap** [CANON flora] | Miners read the fungus: it glows bright orange near a live ember vein. Orange cap means a live vein close by: do not strike, cut or brace there. | EH-M3 (Darven) | *The Flarecap Seam*; EH-M4; EH-M6 |
| **Heat follows the room** [CANON principle; NEW rule] | Strong feeling near a vein raises the local tell one band; calm lowers it. A shouting meeting warms its own junction; a frightened child's flame flares; a crowd that breathes in step lifts a whole terrace. In play this is an authored state change on a quest step, answered by dialogue, a quench, or a steadied breath. | EH-M1 (the ward meeting) | EH-M2 test; EH-M5 rehearsal; EH-M6 warming houses |
| **The valve board** [NEW] | The civic heat main is run from a valve house near Embergate, where a public **tally board** shows what the main takes in and where it sends it. Reading the board (intake against draws) is reading the city's account. | EH-M1 (Odile's tally) | EH-M6 accounting; *The Water That Did Not Arrive* |

### 1.2 Terminology

Writers use these words consistently. Status labels follow §11.

| Term | Use | Status |
|---|---|---|
| **Embercraft** | Fire practice as Emberholt teaches it. Citizens say *craft*, not *magic*; "magic" is an outsider's word and sounds faintly rude here. | [CANON] |
| **The heat main** | The civic network of stone ducts, pipes and valves that carries heat from ember veins and vents to wards, kitchens, baths and forges. Rebuilt after the war over older works. | [NEW] |
| **Fire wardens** | The civic crews who keep the heat main: read tells, bleed junctions, open and shut valves under a District Overseer's authority. Not soldiers. Distinct from the Emberguard's **Cinderwatch** [CANON], which answers riots, accidents and surges. | Architecture term; institution [NEW] |
| **Cooling House / warming house** | A ward's rest room after a hot shift: water, shade, gossip, a cook. In a hard frost the same rooms become warming houses. | [Part 3; NEW] |
| **Heat Commons** | A lower ward's shared wash, warmth and repair arrangements. Social infrastructure, not a resource system. | [Part 3; NEW] |
| **Cinderwall** | Emberholt's rough lower ward or wards, governed by Overseer Yorven Khelt [CANON]. Named in Factions and the character file, absent from the dossier's district list; placed here only as "the lower ward beside the Emberfall Dross" (MAP VERIFICATION REQUIRED). | [CANON name; unplaced] |
| **The precursor** | The unnamed wartime organization that ran the Glassed Hollow ritual. Never given a name, a leader or a roster (D-C03). | [CANON] |
| **The Remnant / "below" / Ashfall** | The formal hidden faction. Citizens who suspect anything say "below" or "Ashfall" as rumour. The word "Remnant" enters public speech only after EH-M6. Its leadership (Selvara, Durell, Meryndis, Varos Keln) never appears in Emberholt content. | [CANON] |
| **Deepbrand** | The Remnant's excavation and containment arm. Lower Emberholt knows it as the deep-works crews that "doesn't rescue you; retrieves what's left" [CANON]; its public standing as a sanctioned contractor is [NEW]. | [CANON; contractor framing NEW] |
| **The Glassed Hollow / the forge collapse** | One place, two accounts. "Forge collapse" is the public record and a sincere belief for most citizens; writers attribute it and never narrate it as fact. | [CANON] |
| **The Fire Titan / the Ash-Clad Giant** | Never met in Emberholt. Citizens know the legend of the Ash-Clad Giant [CANON]. Only Volkhari and the restricted record speak of an initiate. The words "Fire Titan" appear in no Emberholt dialogue except Thalan's and the record's. | [CANON] |
| **Perfect Flame** | Appears only as a heading in Remnant documents (EH-M4 research slate, EH-M6 junction book). No Emberholt NPC explains it beyond what the documents show. Its climax belongs to CV-M4. | [APPROVED — FT-04] |
| **Volkhari** | A people, named as such. Never "dragonkin" in dialogue, never "the extinct", never a monster. The public claim that they "abandoned the city" [CANON] is a belief. | [CANON] |
| **Ember-Fused** | Workers hurt by unstable emberstone who suffer flares. People, never enemies (ED-2). | [CANON; ED-2] |
| **Cinder Wraiths, Ashfall Revenants** | Resonance distortions and constructs. Not undead, not conscious, never ghosts. | [CANON] |
| **Embermind Echo** | A resonance phenomenon that shows hallucinations of past fires. A hazard, never a witness. | [CANON] |
| **The High Kindling** | The high-holiday festival at which the Speaker addresses the city [CANON practice: he speaks from Cinderreach Spire on high holidays]; its rehearsals run on the Ash Terraces. The festival CV-M4 uses. | [NEW name] |
| **First Cooling** | Cinderwall's own remembrance: lowered flames, repaired work shown in public, a meal before names. | [Part 3; NEW] |

**Words not used:** "ghost", "undead", "curse"; "invaders" or any compass direction for an enemy (architecture contradiction 3); a precursor name; a count of Volkhari; "the Chosen", or any line that makes the player special by birth (origin-neutral, D-3); "city-wide ignition" spectacle (FT-04).

---

## 2. Author truth

This is the private truth behind the arc. Players learn it gradually and never from one source. It keeps the architecture's three causes separate (World Truth B.3.1): **present human decisions** (a valve order that follows influence; a school test that sorts children; a hidden draw on the city's heat), **older damaged infrastructure** (a heat main laid over wartime conduits; a sealed, glassed chamber; bindings that are failing), and **bounded resonance** (veins that answer feeling; wraiths and revenants; a Titan nobody meets here) that never testifies.

### 2.1 The city's heat [CANON core; NEW detail]

- **Ember veins** run beneath the mountain and feed the city's heat [CANON]. Vents release it as shimmering air; Flarecap glows near live veins [CANON].
- **The heat main [NEW].** After the war the city rebuilt its civic heat as one main: stone ducts and iron pipes drawing from veins and vents through junctions to every ward. Much of it was laid along older wartime conduits because they were already cut. The main is run from a **valve house near Embergate**, where a public tally board has shown intake and draws since the rebuilding. Its figures have never balanced. The shortfall is blamed, sincerely, on "old leaks".
- **Fire wardens [NEW institution].** Crews under each District Overseer read tells, bleed junctions and keep the valves. They are proud, underpaid and blamed for everything that goes cold.
- **Cooling Houses and the Heat Commons [Part 3; NEW].** Each lower ward keeps a rest house with water and a cook, and a shared arrangement for wash water and repair. They are where the ward meets, argues and mourns.
- **Children and craft [CANON].** Every child learns lantern ignition, controlled heat pulses, ember-thread weaving and emotional grounding. Academies assess emotional volatility and sort students into civic roles [CANON]. Fire-control exams double as compatibility assessments; some ceremonies were designed as mass emotional tests [CANON].

### 2.2 The war and the Hollow [APPROVED FT-02d; CANON core; NEW detail]

- Emberholt weaponized fire practice in the war: battle embercraft, amplification conduits, siege engines [CANON H13]. The Molten Scars are where it melted its own ridges.
- **The Glassed Hollow [CANON; APPROVED FT-02d].** Hungry and cut off by sealed passes and thinning grain, the wartime precursor gambled on an amplification ritual using Volkhari knowledge and captives to end the war fast in Emberholt's favour. The ritual spiralled when emotional overload triggered an ember surge; heat flash-melted the chamber into glass. A precursor initiate, not a Volkhari, became the Fire Titan. Kaelith Veyr'un escaped and remains free. Thalan Veyr was seized later, in the purges that followed, and is the sole known current captive. Emberholt lost its offensive capacity in a night and its civic leaders stopped. The public record says "forge collapse".
- **Where it happened [NEW].** The ritual chamber lay deep beneath the old lower forge on Cinderwall's working edge. After that night the forge yard was walled off and a memorial plaque named the people "lost in the collapse of the lower forge": lower-forge shift hands who were above the chamber when the surge came up. They were civilians and had nothing to do with the ritual. Some were never found; at least one walked out burned and was not counted (*The Half-Name Wall*). Whether he is the Mire's unnamed "man from the fire roads" (MDS09) is never confirmed, and no route out of Emberholt is implied (ED-16).
- **What the record shows [NEW].** The precursor kept a **chamber roll** for the ritual night: a sheet with a heading seal and a line for each person admitted. The heading seal was cut away long ago. The surge glassed the sheet's lower half where it lay in the chamber's niche: every line is unreadable except one, the line for the initiate "placed at the centre", whose name is legible `[INITIATE]` (ED-3). A second sheet in the same hand, written after the night, notes "one child unaccounted: the door" and "one elder taken in the purge, held below". After the war these sheets crossed into the Red-Lit Scribes' forbidden archive; a later annotation in a different hand reads *"Keep. Do not copy."* That is the whole of the continuity the player can see: someone who kept the precursor's papers kept them into the Remnant (D-C03, limited continuity). Nobody is named.
- **The inspection gap [NEW; R16 seed].** On the same archive shelf sits a prewar inspection register with a column headed "visiting witness", empty for the last years before the war and its heading struck through. It is never explained in Emberholt.
- **Withheld forever in Emberholt content:** the precursor's name; who survived into the Remnant; how many died in the Hollow or the purges; how many Volkhari live; how the Titan's bindings work or are made (FT-05 mechanics under review); anything about the Stonebound beyond what canon already says.

### 2.3 The present wrongs [NEW]

- **Allocation follows influence** `[ALLOCATION]` (EH-M1). For the High Kindling rehearsal, an Ashspire salon asked the ceremonies office for "a warm rehearsal". The Magistrix's aide, **Sarne Ardane**, signed a valve order in her name moving Cinderwall's junction allotment to the Ash Terraces for nine nights. Veska Dunmor protested, chalked her protest on the junction slate, and was overruled. Her protest page was cut from the valve-house book by a clerk who thought the order embarrassing. When the ward went cold, the ward blamed the warden. No Remnant is involved.
- **The schools sort** (EH-M2). The Molten Stair academy's volatility test uses emberglass test lenses whose curve was changed on a Council schedule to focus the flame rather than spread it: "a lens for pushing, not seeing". The assessment ledgers keep a coded second column beside each child's civic placement; a transfer list sends some children to "vigil guidance" (Hearthveil), some to Emberguard schools, and a few "for evaluation below". **Theryn Dalewright** [CANON] is a covert recruiter: she sincerely believes she protects gifted children from their own power, sees Ashfall guidance as stewardship, and quietly funnels talent toward Hearthveil and the Emberguard. She also resisted one order to turn an unstable child over to Deepbrand and hid the child instead [CANON secret]. The content shows her as a person with a conscience inside a system, never as a villain to be beaten; the other teachers are not part of it.
- **The lost crew** (EH-M3). Deepbrand hired a contract mining crew to cut a bypass gallery toward the Hollow's outer glass, because the deep works want the veins around it. The cut broke into a heat pocket and the gallery came down. **Darven Mott** [CANON] came out alone. Deepbrand "retrieved what's left" and sealed the gallery; the official account calls Darven unstable. The work order went around the Grand Marshal [CANON: Kaevren has intercepted orders routed around him].
- **The draw** (EH-M6). For years Deepbrand has spliced draw lines into the civic main below Cinderwall, using civic valve fittings so the splices look like repairs, and taken heat down toward the deep works for Perfect Flame research (Thalan's frame and the proving rings, EH-M4). The tally board's "old leaks" are the draw. In an ordinary winter the main carries it. In a hard frost it does not. **Nobody set a fire;** the failure is the cost of a hidden draw.
- **Why now.** The High Kindling is coming, and with it the rehearsals that teach a crowd to breathe in step (EH-M5). The research below needs more heat and more measured crowds. Thalan's frame has been worked harder this year than any year since the purges.

### 2.4 Resonance and what is never met [CANON boundaries]

- **Cinder Wraiths** are blazing silhouettes caused by emotional surges in ember veins; not undead, not conscious [CANON]. They form where a vein surges and re-form while it surges.
- **Ashfall Revenants** are resonance constructs formed from intense trauma and uncontrolled embercraft [CANON]. The Hollow Revenant (EH-M3 miniboss) is one, at the ritual circle. It is not the initiate and not any person.
- **The Embermind Echo** shows hallucinations of past battles or ritual failures during strong eruptions [CANON]. It is a **hazard**: it overlays the scene, never changes the ground, and never identifies anyone.
- **Emberdeep Sentinels** are constructs made by Remnant engineers to patrol sealed chambers [CANON]. They are machines.
- **Ember-Fused Workers** are people hurt by unstable emberstone [CANON]. They are never an enemy family here (ED-2).
- **The Fire Titan** is not met in Emberholt. It is felt only as other people's words: the Ash-Clad Giant legend [CANON], Thennek's suspicion that it is not fully dormant [CANON], Thalan's recognition of suffering [CANON], and one Deepbrand note that "the old circle keeps this season" (EH-M6). Its binding is CV-M4's.
- **The sobbing in the pipes** (EH-M1). The Cinder Rat has sensed "one particular sobbing ember" for years [CANON]. The player hears it once. It is **never explained** in Emberholt.
- **Stonebound.** Canon places Stonebound works beneath Emberholt. This bible uses none of them: no gate, mechanism, "song" or memory wall appears, and no anchor's Stonebound secret is used (C11; World Truth C.7).

### 2.5 Perfect Flame and the Remnant inside Emberholt [APPROVED FT-04]

The player never meets the Ashfall Authority. They meet its work: a valve fitting that is not a repair, a test lens that pushes, a sleep room with a ledger, a frame with a man in it, and two documents headed *Perfect Flame*. From those the player can see what FT-04 defines: an attempt to make advanced embercraft reproducible, so that anyone conditioned the right way can be made to do it, while the knowledge stays below. The Remnant's reach outside Emberholt appears only as two specific, discoverable acts: the broadsheet phrase in EH-M1 (planted, unattributed; R15 is owned by CV-M2) and the river timetables in *The Commissioner's Cargo* (ECC). Neither explains anything in Lowmark, Thornfell or the Mire. The Remnant does not cause the cold ward; it exploits a main that already favours Ashspire.

### 2.6 Who knows what

| Person | Knows | Does not know |
|---|---|---|
| Veska Dunmor [NEW] | Her junction, her protest, every tell in the ward; that the board never balances. | Where the shortfall goes. |
| Yorven Khelt [CANON] | Cinderwall; older tunnels that bypass Ashfall security [CANON secret]; vein surges that contradict official safety [CANON]. | What the precursor did; who draws on the main. |
| Odile Prace [NEW] | The valve-house book and tally board. Who signed the order. | That the "old leaks" are a draw. |
| Ralenne Kharveil [CANON] | The rehearsal schedule; that her scripts get "suggestions". | That her aide moved the ward's heat; that the suggestions are conditioning [CANON: unaware]. |
| Theryn Dalewright [CANON] | The test, the ledgers, the transfers and who receives them; that "below" means Deepbrand; the one child she hid. | What Deepbrand does with the children sent there; Perfect Flame. |
| Maeryn Vall [CANON] | Every scorched smock and mitt she mends; that she is Volkhari. | What the coded column means. |
| Darven Mott [CANON] | His crew, the cut, the breathing walls. | Why Deepbrand wanted the cut; what the Hollow was. |
| Kaevren Thalos [CANON] | His disappearance ledger; orders routed around him [CANON secrets]. | What is below in detail. |
| Marenya Silvertide [CANON] | Shelf-marks and custody of the forbidden archive. | She vouches for provenance, never for content. |
| Seredh Embercarver [CANON] | His memory-stone account of the night (one account). | The precursor's papers. |
| Dahrin Vosk [CANON] | Where he was held; the opening phrase of the Titan's binding [CANON secret; not spoken in Emberholt]. | Thalan's present state. |
| Thalan Veyr [CANON] | His captivity; the Titan's suffering as he feels it. | The city above; who will come. |
| The Flameward Speaker [CANON] `[D-S1]` | What he is told and what he is shown in dreams; that he serves Remnant aims for his own ambition. | The Ashfall endgame (character ledger). |
| Serix Arden [CANON] | How visions are seeded; that he has started seeing ones he did not make. | Who is making them. |

### 2.7 What defeating a resonance enemy means

Cinder Wraiths and Ashfall Revenants follow the Lowmark drift and Mire imprint precedent: **combat disperses, conditions decide.** Each is defeated at 0 HP and collapses into ash. While its condition lasts (a surging vein, a burning brazier, a heat pocket), it re-forms: in an active encounter on the site's trigger (a vent's exhale, a brazier's flare, the pocket's pulse); outside an encounter only when a quest next presents the condition (pending Gameplay Designer confirmation, as in the Mire). Bleeding the junction, dousing the brazier or quenching the pocket ends the condition. **Emberdeep Sentinels** are constructs and are destroyed at 0 HP. **Human enemies** (Dross Scavengers, Forge Saboteurs, Deepbrand Crews) are defeated at 0 HP with the ordinary defeat presentation. No defeated enemy, human or construct, ever gives testimony (rulings §3.2). No Volkhari, Ember-Fused worker, child or civic official is ever targetable.

---

## 3. Director decisions and how the content depends on them

Emberholt decisions use the prefix **ED-**. Each is a **recommendation** for the Director, not a ruling; content is built on the recommendation and isolated so a change touches only the listed places. The consequential ones are marked ●.

| # | Decision | Recommendation (what content assumes) | Content that changes if replaced |
|---|---|---|---|
| ED-1 ● | **EH-M1's present cause** | Allocation by influence: a ceremonies-office valve order for the High Kindling rehearsal, signed by an aide at an Ashspire salon's request; the warden's protest cut from the book. No Remnant (Arcs: "No Remnant required"). Tagged `[ALLOCATION]` (§3.1). | EH-M1, *The Water That Did Not Arrive*, *First Cooling* lines. |
| ED-2 ● | **Ember-Fused Workers** | The dossier recommends non-lethal containment [CANON]; CDR-1 forbids health-based yields. Recommendation: fused workers are **never combatants**. A flare is a hazard zone around a non-targetable person, ended by a containment interaction (cool the vent, steady the breath, carry them to care). This needs **no SX entry** because they never fight (like SX-N). Alternative for the Director: make them an enemy family and register each containment as an SX exception. | EH-M6 S01, *The Vein-Touched Man*, §10. |
| ED-3 ● | **The precursor record and the initiate's name** | EH-M3 recovers the chamber roll with one legible line, the initiate's (R19 custodian). The name string is **reserved for the Director** and written `[INITIATE]` in every package; it is recorded in the player's journal in EH-M3 and spoken nowhere in Emberholt. The heading seal is cut away (no precursor name) and every other line is glassed (no roster) (D-C03). A later "Keep" annotation shows records crossed into the Remnant's archive without naming who carried them. | EH-M3 S07, CV-M4 binding. |
| ED-4 ● | **Thalan's fate** `[D-E2]` | D-E2 is open. Content authors both architecture options as player choices, **freed** and **aided in place**, each with Thalan's own voiced consent, and never an option to end his life or exploit him (contradiction 7). If the Director rules for one, the other branch is cut and its nodes removed; nothing else changes. | EH-M4 S06–S07, EH-M6 §9.3 line, CV-M4 testimony. |
| ED-5 ● | **The Speaker** `[D-S1]` | D-S1 is open. Content follows the architecture's recommendation: a knowing ally for his own ambition **and** sincerely dream-seeded; he lacks the Ashfall endgame (ledger). He never fights, never confesses and never lies outright (he uses omission). He **stays in office** in both EH-M5 outcomes, so the High Kindling still happens (CV-M4). | EH-M5 S03–S06, EH-M6 letter line. |
| ED-6 ● | **Heat as terrain under CDR-4** | Heat is ordinary hazard volumes with periodic damage, timed vents, safe cooling niches and a three-state schedule per zone. No heat or temperature meter, no stamina, no stealth or detection system. The Arcs' "infiltration" (EH-M4) is routes, a warrant, sigil doors and fights; "heat-pressure traps" are pressure plates whose tells show when they are primed. | §1.1, §9.2, §11; EH-M3, EH-M4, EH-M6. |
| ED-7 | **EH-M3 gate** | Hard prerequisites: EH-M2 Completed **and** (TF-M3 **or** MR-M2) Completed. Two hard prerequisites, within the Arcs §6.1 limit. The locked journal entry is visible and names both alternatives (no hidden gate). Each alternative unlocks one optional variant line, never a different quest. | EH-M3 offer. |
| ED-8 ● | **Bosses** | The Act III boss is a construct, **the Draw Sentinel** (EH-M6). Minibosses: **the Hollow Revenant** (EH-M3, a resonance construct) and **Old Plate** (side, an emberback sow). No named anchor is ever fought in Emberholt: Varos Keln, Meryndis, Selvara, Durell, Gavric Ember-Crown and Thaliax Brend never appear as enemies (convergence and the character ledger). | §10. |
| ED-9 | **Map placement** | Relative only (§4). **MAP VERIFICATION REQUIRED** wherever geometry, distance, heat or terrain matters. Embergate is "the city's main entrance" [CANON] and leads out; no destination region, direction or route beyond the city is ever stated. No "eastern" or "invader" wording. | Travel lines; §4. |
| ED-10 | **Level framing** | No quest prerequisite for EH-M1 (travel only). Tuned as post-Mire content in production terms: EH-M1–M2 Advanced, EH-M3–M6 Expert. Exact levels are Gameplay Designer calls (`[GD]`). | Encounter tuning. |
| ED-11 | **Skills** | Emberholt is the **Smithing** region (a hook in three milestones and two side quests; master commissions after `EH_STANDING`), with a **Mining** intro (ridge workings), **Leatherworking** heat gear, **Cooking**, and **Fletching/Ranged** through the Border-Wardens' crossbows. Timber is imported (source process): Woodcutting appears only as reclaimed crate-wood. Legacy materials (ember shards, emberglass, ashsteel, conduction plates, Volkhari Ash) are not catalog items; Volkhari Ash appears only as contraband evidence. | Skill hooks; §7 skill coverage. |
| ED-12 | **Volkhari depiction** (D-C06) | Individuals only: Maeryn, Kaelen, Asera, Thennek, Dahrin, Seredh, Thalan; Kaelith seen and never rescued, followed or chosen. No refuge is located, no number is stated, no community form is shown. Volkhari testimony is protected: it is read in public only with that person's consent flag. No Volkhari is ever an enemy or targetable. | EH-M2–M4, EH-M6, Unburnt series. |
| ED-13 | **Adopting Part 3 practices** | Adopt as [NEW]: fire wardens and the heat main, tells, Cooling Houses (warming houses in frost), the Heat Commons, the valve house and tally board, First Cooling, the Half-Name Wall, the Cold Seam, the Bridge of Seven Repairs. **Not adopted:** the Measure of Ash inquest and the Hearth Tally as a selection record (both need a Council-authority ruling). | Text only. |
| ED-14 | **R15 phrase** | Thornfell's broadsheet *"When the forges eat the grain, the passes go dark."* appears reversed in EH-M1 as *"When the passes go dark, the forges go cold."* Planted on a junction door, never attributed or explained (R15 owned by CV-M2; FT-04). | EH-M1 S01 only. |
| ED-15 ● | **Fog and Riverglass act** | *The Commissioner's Cargo* (ECC) authors one discrete, discoverable Remnant act beyond Emberholt (FT-04): Lowmark river timetables, bought through Shadeweaver contacts [author truth], carried through Embergate to a merchant-house front. In play the buyer stays **unattributed**: no Remnant, Ashfall or Durell name, no Lowmark cause, no route or carrier between regions, and no Lowmark transaction is matched (Part 4 ledger, Oren Falx row). R15 stays CV-M2's. Held in review; alternative: cut ECC and leave the series entirely to CV-M2. | ECC; `EH_RIVERGLASS`. |
| ED-16 ● | **The man from the fire roads** (Mire MD-13, MDS09) | *The Half-Name Wall* (ENW) resolves an **Emberholt** case only: Corm Brask, a lower-forge shift hand listed as lost in the "collapse", walked out burned (proved in Emberholt by the lower-forge pay list). He is never met and is recorded "walked out; not found since". A civilian above the chamber, never a precursor member. The Mire entry is an optional, **unconfirmed** echo (`MDS09_READ`): one extra line in which his kin hears of a burned man who would not give his name and decides whether to hope. It is never a hold, never proves identity, never places the fire roads and implies no route between regions. The Mire gains no content, flag or requirement. Alternative: leave MDS09 wholly unresolved and cut the line. | ENW; Register §7.6. |
| ED-17 | **Dreams and the player** | No player dreams in Emberholt. Serix Arden's unscripted visions are reported as his experience only; the canon line that they centre on "the player" is not used (origin-neutral, no chosen one). No dream or vision is evidence [CANON]. | EH-M5; *Glassmoth's Tonic*. |
| ED-18 | **The festival's name** | "The High Kindling" [NEW], the high holiday at which the Speaker addresses the city [CANON practice]. Rehearsals on the Ash Terraces; the festival itself is CV-M4's. | EH-M1, EH-M5, CV-M4 wording. |
| ED-19 | **Canon promotion** | Promote nothing from this package. | None. |
| ED-20 ● | **EH-M2 prerequisite (architecture conflict)** | The Arcs §3.3 entry text says "No quest prerequisite for EH-M1 and EH-M2"; the Arcs §6 graph draws a solid E1 → E2 arrow (hard prerequisite). Recommendation: follow the graph (EH-M2 requires EH-M1). The stand-alone principle (Arcs §1.3 rule 2) still holds, because the entry milestone EH-M1 has no prerequisite and nothing before EH-M3 needs another region. Alternative (the prose): EH-M2 offered on arrival with no prerequisite; then its offer must not use "warden's hand" and Jessa approaches "the outsider". The Director should rule and the Arcs text or graph be corrected. | EH-M2 offer line; §6 prerequisites. |

**SX proposal: none.** No Emberholt story needs a scripted surrender, mercy or survival outcome. Every human enemy (Dross Scavengers, Forge Saboteurs, Deepbrand Crews) fights to 0 HP with the ordinary defeat presentation. People who could have needed an exception never fight and are never targetable: the Speaker, Serix Arden, Theryn Dalewright, Sarne Ardane, Marenya Silvertide, every Volkhari, every Ember-Fused worker (ED-2) and every child, so they need no SX-N entry either. Constructs (Emberdeep Sentinels) and resonance enemies are not persons.

### 3.1 Allocation swap layer

If ED-1 changes, edit only nodes tagged `[ALLOCATION]`: EH-M1 S03, S04 and S07 (the order, Sarne Ardane, Ralenne's scene, the choice wording), the Cooling House barks, and the `EH_COLD_WARD` lines in *The Water That Did Not Arrive*, *First Cooling* and EH-M6 §9.3. The cold ward, Veska's slate, the tally board's shortfall (the EH-M6 seed) and the broadsheet survive any replacement that is still "a present, local, non-Remnant reason the ward's heat went elsewhere".

### 3.2 Reserved-decision layers

- **`[D-E2]`** marks every node that depends on Thalan's fate: EH-M4 S06–S07, `EH_THALAN`, the EH-M6 tally-board line (§9.3 item 5), the Unburnt series' Asera lines that refer to him, and the CV-M4 testimony note. Both branches are authored to the same length and land at the same completion step, so cutting one leaves a complete quest.
- **`[D-S1]`** marks every node that asserts what the Speaker knows or intends: EH-M5 S03 letter text, S04 chamber-record lines about him, S06 his reaction and both outcome lines, and his EH-M6 letter. If D-S1 rules "wholly puppet", the letters are re-read as drafted for him and the replies as instructions he did not understand; if "wholly mastermind", the chamber record's lines about him are cut. The investigation, the custodians and both choices survive either ruling.
- **Origins (D-3):** the player is addressed as "outsider" or "traveller", then "warden's hand" after EH-M1. Nothing else depends on origin.

---

## 4. The map and points of interest

**No Emberholt terrain exists.** Nothing in this section is a coordinate, a distance or a direction. Each placement is relative to a canon place and is a request to the Environment and Map team, not a fact. **MAP VERIFICATION REQUIRED** applies to every row below wherever geometry, distance, heat or terrain matters to a quest. Embergate is the city's main entrance [CANON] and the only way toward other regions this bible uses; it never names where the road goes, and no route between regions is invented here. The working gate on Cinderwall's side (below) opens only onto the Ridge.

### 4.1 Subzones (dossier districts, plus Cinderwall)

| Subzone | What it is in play | Main content |
|---|---|---|
| **Embergate and the Gate** | The main entrance [CANON]: the gate, the merchant yards, the Gate Valve House with its tally board, the Bridge of Seven Repairs. | EH-M6 aftermath; *The Commissioner's Cargo*; *The Seven Repairs* |
| **Cinderwall and the Dross** | The working ward the dossier does not list as a district (Factions: District Overseer Yorven Khelt; §13 note): Cooling House, Red Door clinic, the old lower forge, the slag tips. | EH-M1; EH-M6; Heat Commons series; *The Half-Name Wall* |
| **Cinderweave Quarter and the Molten Stair** | Artisans and academies [CANON]: Maeryn's shop, Brisa Teglan's tannery, Theryn's academy on the stair. | EH-M2; Unburnt series; skill intros |
| **Emberhold District, the Ash Terraces and Ashspire** | Civic heart [CANON]: Speaker's Hall, the terraces where the High Kindling is rehearsed, the Ashspire salons, the Covenant lamp-house. | EH-M5; EH-M1 valve order trail |
| **The Emberforges** | The great forges [CANON] and the guild halls around them. | *Sound Stock*; *The Old Methods*; EH-M6 bleed choice |
| **The Underworks** | Beneath the city: the heat main's ducts and junctions, the Cinderwall Undercroft, the Emberdeep Warrens, the ritual chambers, the Glassed Hollow. | EH-M3; EH-M4; EH-M6 descent |
| **The Ridge** | The volcanic ridge beyond the walls [CANON]: Ash Roads, Molten Scars, ridge workings, Elyndra's shrine, the Cold Seam, Cinderreach Spire. | Skill intros; *Old Plate*; discoveries |

### 4.2 POI slate (28 POIs; Phase 1.5 range 24–32)

Ids are planning labels (`EP##`). Placement is relative. **MAP VERIFICATION REQUIRED** for every placement; the zone package (Batch 4) carries the detail.

| Id | POI | Category | Subzone | Status | Main use |
|---|---|---|---|---|---|
| EP01 | **Embergate** (the main gate, merchant yards, gate market) | Settlement | Embergate | [CANON] | Arrival; EH-M6 aftermath; *The Commissioner's Cargo* |
| EP02 | **Cinderwall** (lower ward: Cooling House, Red Door clinic, terraced tenements, slag lanes) | Settlement | Cinderwall | [CANON ward; NEW detail] | Hub; EH-M1; EH-M6; Heat Commons series |
| EP03 | **Cinderweave Quarter** (Maeryn's shop, Brisa Teglan's tannery, dye yards) | Settlement | Cinderweave | [CANON; NEW detail] | EH-M2; Unburnt series; *Soot and Hide* |
| EP04 | **The Molten Stair** (Theryn's academy, practice courts, student lodgings) | Micro-settlement | Cinderweave | [CANON] | EH-M2; *Three Breaths* |
| EP05 | **The Ridge Steadings** (herders and charcoal burners outside the walls) | Micro-settlement | The Ridge | [NEW] | *Old Plate*; *The Flarecap Seam* |
| EP06 | **Slagside** (scavenger shanties on the Dross tips) | Micro-settlement | Cinderwall | [NEW] | *The Case That Never Reached the Court*; Dross Scavengers |
| EP07 | **The Glassed Hollow** (outer glass, circle site) | Ruin/war site | Underworks | [CANON] | EH-M3 |
| EP08 | **The Molten Scars** | Ruin/war site | The Ridge | [CANON] | *Old Plate*; EDS02 |
| EP09 | **The Ash Roads** (cracked old streets lined with burnt engravings, running out from the walls onto the Ridge) | Ruin/war site | The Ridge | [CANON; placement NEW] | EDS01; *Wardens' Quarrels* |
| EP10 | **Darven's Gallery** (the collapsed bypass cut) | Ruin/war site | Underworks | [NEW] | EH-M3 |
| EP11 | **The Old Lower Forge** (walled yard, memorial plaque) | Ruin/war site | Cinderwall | [NEW] | EH-M1 pass-by; *The Half-Name Wall*; EDS09 |
| EP12 | **The Half-Name Wall** (a wall of part-names on the forge yard's outer side) | Ruin/war site | Cinderwall | [NEW, Part 3] | *The Half-Name Wall* |
| EP13 | **The Emberdeep Warrens** | Cave/dungeon | Underworks | [CANON] | EH-M4 |
| EP14 | **The Ridge Workings** (shallow flarecap and ore galleries) | Cave/dungeon | The Ridge | [NEW] | *The Flarecap Seam*; Mining intro |
| EP15 | **The Cinderwall Undercroft** (heat-main ducts and junctions below the ward) | Cave/dungeon | Underworks | [NEW] | EH-M1; EH-M6 |
| EP16 | **The Ritual Chambers** (Thalan's frame, the proving ring) | Cave/dungeon | Underworks | [CANON] | EH-M4 |
| EP17 | **The Saboteurs' Kiln** (abandoned charcoal kiln used as a hideout) | Camp/bandit site | The Ridge | [NEW] | *The Old Methods* |
| EP18 | **The Dross Scavenger Pits** | Camp/bandit site | Cinderwall | [NEW on CANON group] | *The Case That Never Reached the Court* |
| EP19 | **The Embervein Tap** (Dalia Vret's camp at an exposed vein) | Camp/bandit site | The Ridge | [NEW place on CANON anchor] | *The Vein-Touched Man* |
| EP20 | **Elyndra's Vent Shrine** | Shrine | The Ridge | [CANON myth] | EDS05; *The Flame That Would Not Die* |
| EP21 | **The Cold Seam** (a fissure where no heat rises; a place of quiet grief) | Shrine | The Ridge | [NEW, Part 3] | EDS07 |
| EP22 | **The Covenant Lamp-House** (vigil hall above; the Hearthveil sleep rooms below an old dormitory) | Shrine | Emberhold District | [NEW place on CANON practice] | EH-M5; *Glassmoth's Tonic* |
| EP23 | **The Ash Terraces** | Unique landmark | Emberhold District | [CANON] | EH-M1 order trail; EH-M5 rehearsal |
| EP24 | **Cinderreach Spire** | Unique landmark | The Ridge | [CANON] | EDS06 |
| EP25 | **The Emberforges** | Unique landmark | Emberforges | [CANON] | *Sound Stock*; *The Old Methods*; EH-M6 |
| EP26 | **The Gate Valve House** (valve book, tally board) | Unique landmark | Embergate | [NEW] | EH-M1; EH-M6 |
| EP27 | **The Bridge of Seven Repairs** | Unique landmark | Embergate | [NEW, Part 3] | *The Seven Repairs* |
| EP28 | **Speaker's Hall** | Unique landmark | Emberhold District | [CANON] | EH-M5 letters |

Counts against Phase 1.5 (each POI counted once): settlements 3 (EP01–03); micro-settlements 3 (EP04–06); ruins/war sites 6 (EP07–12); caves/dungeons 4 (EP13–16); camps/bandit sites 3 (EP17–19); shrines 3 (EP20–22); unique landmarks 6 (EP23–28). Total 28. Hunting is staged in the Molten Scars and the ridge around the steadings rather than at a separate hunting POI; the Ridge Workings are Emberholt's mine.

**Relative route order** (MAP VERIFICATION REQUIRED): Embergate opens into the city; the valve house and the Bridge of Seven Repairs sit inside the gate. Cinderwall lies below the civic heart and close enough to the gate that its main runs past the valve house. The Cinderweave Quarter sits between Cinderwall and the Emberhold District; the Molten Stair climbs from the quarter toward the civic terraces. The Ash Terraces and Speaker's Hall sit in the Emberhold District; Ashspire is above them. The Emberforges lie beside Cinderwall's working edge, and the old lower forge was part of that edge. The Undercroft is entered from Cinderwall; the Emberdeep Warrens are reached from deeper junctions; the Glassed Hollow lies beneath the old lower forge; the ritual chambers lie in the Warrens. The Ridge is outside the walls and reached through a working gate on Cinderwall's side; the steadings, the workings and the Molten Scars are along the Ash Roads, with Elyndra's shrine, the Cold Seam and Cinderreach Spire further out. Nothing beyond the Ridge or past Embergate is placed.

---

## 5. Cast

### 5.1 Canon anchors (limits from the Part 4 character ledger apply to every line)

| Anchor | Role here | Limits kept |
|---|---|---|
| **Yorven Khelt** | District Overseer of Cinderwall; EH-M1 contact, EH-M2 strongbox, EH-M3 bypass tunnel, EH-M6 crew lead. | Knows old bypass tunnels and contradicting surge records [CANON]. Never knows the precursor's work or who draws on the main. Not the blamed warden (§13). |
| **Ralenne Kharveil** | Magistrix; ceremonies office. EH-M1 sincere scene; EH-M5 rehearsal script. | Unaware her scripts are conditioning [CANON]. Never a villain and never targetable. Her aide's order is in her name without her reading. |
| **Theryn Dalewright** | Molten Stair academy instructor; covert recruiter; EH-M2. | Sincere in her stewardship; funnels talent [CANON]; hid one child from Deepbrand [CANON secret]. Never fights, never targetable, never exposed as Remnant in Emberholt (her choice of loyalties belongs to later content). Does not know what Deepbrand does below. Never calls the player "special" (origin-neutral). |
| **Selice Morra** | Master emberglass artisan; EH-M2 lens reading (she did not make the test lenses). | Speaks to the glass, not to motives. "A lens for pushing, not seeing." |
| **Maeryn Vall** | Volkhari seamstress in Cinderweave; EH-M2, EH-M4 safehouse, Unburnt series. | Her heritage is her own to disclose; never forced. Afraid of a Covenant-grey visitor [CANON-consistent]. |
| **Darven Mott** | Sole survivor of the lost crew; EH-M3. | Speaks to his crew and the cut only. Not "unstable"; frightened and precise. |
| **Kaevren Thalos** | Grand Marshal; EH-M3 recovery warrant, EH-M5 intercepts. | Keeps a disappearance ledger and intercepts routed orders [CANON secrets]. Never a Remnant member and never fought. |
| **Marenya Silvertide** | Red-Lit archive custodian; EH-M3 roll provenance. | Custodian, not a truth source: she vouches for shelf-marks, never for what a page means. |
| **Seredh Embercarver** | Volkhari keeper of memory-stones; EH-M3 one account; *The Memory-Stone*. | A memory-stone is one account and needs a second channel. No numbers, no refuge. |
| **Asera of the Three Breaths** | Volkhari ritualist; EH-M4 ally (breath steadying); *Three Breaths*. | Steadies breath and calms flares [CANON ability]; never casts at enemies and teaches the player no spellcasting. Decides how far she goes. Her nightmares of the captive are her own experience, never evidence. |
| **Thennek "Stone-Quiet" Vorren** | Volkhari pathfinder; EH-M4 guide to the Warrens' mouth. | R19 line only: the Titan is "awake enough to be uncomfortable". Explains no binding. |
| **Dahrin Vosk** | Escaped captive; EH-M4 account and sigil-stone. | Knows the binding's opening phrase [CANON secret]; never speaks it in Emberholt. |
| **Thalan Veyr** | Captive in the frame; EH-M4 `[D-E2]`. | Voiced consent in either branch; never killed, never exploited, never fought. May say that the fire below suffers (R19 seed only); never explains the Titan, its bindings or the initiate, and never names anyone. |
| **Kaelith Veyr'un** | Seen once as emberlight above the chamber (EH-M4). | Never met, rescued, followed or chosen. |
| **Kaelen Veyr'un** | Kaelith's sibling, a Volkhari youth hiding near the city; *Stitches in the Lining*. | His emberburst is a hazard; never targetable. Angry at Emberholt, and allowed to be. His dreams of something calling from below are never evidence (R19). He is never told where Kaelith is, and never leads the player to a refuge. |
| **The Flameward Speaker** `[D-S1]` | EH-M5 subject; EH-M6 letter. | Never fights, confesses or lies outright; stays in office; lacks the Ashfall endgame (ledger). |
| **Seralynd Hearthveil** | Ember-Priestess of the Covenant; EH-M5. | Her dreams are shaped by Hearthveil operatives and she has unscripted visions [CANON secrets]; she confides doubts and makes her own choice on the terrace. Her suspicion about Volkhari foundations of Covenant rites is not used. |
| **Serix Arden** | Hearthveil dreamwright; EH-M5 witness. | Knows how visions are seeded; reports his own unscripted visions as his experience only (ED-17). |
| **Saelia Verithe** | Ritual Conductor; runs the EH-M5 rehearsal. | Suspects something is off in her scripts and cannot pinpoint it [CANON]; never knowingly complicit. |
| **Vael Trossen** | Magister; EH-M5 sealed inquiry (exposed branch). | Named on the guided-sleeper list; never shown as Remnant. |
| **Durnan Volkryst** | Forgeguild master; *Sound Stock*; EH-M6 guild account. | Guild pride; never a villain. |
| **Haelric Stormvein** | Border-Warden captain; *Wardens' Quarrels*, *The Commissioner's Cargo*. | Has intercepted coded messages hinting at Remnant reach beyond the city and does not know whom to trust [CANON secret]; he flags the cargo and never names an external target or route. |
| **Oren Falx** | Trade Commissioner; *The Commissioner's Cargo*. | Signs what passes the gate; never shown to know the timetables' use. |
| **Sereth Vorn** | Ember healer; *The Vein-Touched Man*. | Care first; no cures promised. |
| **Glassmoth** | Tonic-seller; *Glassmoth's Tonic*. | Sells relief for dreams; not Remnant. |
| **Myr Adalrek** | Ember-Fused worker; *The Vein-Touched Man*. | Never a combatant (ED-2). |
| **The Cinder Rat** | Glimpsed in EH-M1; duct in EH-M5. | Hears "one particular sobbing ember" [CANON]; never explains it. |
| **Elyndra** | Myth only; *The Flame That Would Not Die*; EDS05. | No appearance; no proof. |

**Named canon figures not used in Emberholt content** (reserved for later packages or kept off-screen by the ledger): Selvara, Durell, Meryndis, Varos Keln, Gavric Ember-Crown, Thaliax Brend, Ilverin, Kharos, Nythra, Lyria Caelith, Kalen, Envalos, Ravox, Lyria Velsin, Tannon, Rhys, Ilyen, Vaelyra. **Joren Vale** appears only as a hand on a draft map (EDS08). **Calynne** appears only as a name in a record. None is fought.

### 5.2 New for Emberholt [NEW]

| Name | Role | Where | Voice note |
|---|---|---|---|
| **Veska Dunmor** | Cinderwall fire warden blamed for the cold ward. | EH-M1; EH-M6 crew; *The Ward That Answers Its Own Bell*. | "Read the tell, not the talk." Proud, tired, exact. |
| **Odile Prace** | Valve-house tallyman; keeps the book and the board. | EH-M1; EH-M6. | Counts aloud. "The board's never balanced. That's not news; it's weather." |
| **Sarne Ardane** `[ALLOCATION]` | The Magistrix's aide who signed the valve order. | EH-M1; *The Water That Did Not Arrive*. | Polished, embarrassed, not cruel. "It was nine nights." |
| **Jessa Ostry** | Cinderweave dye-worker; Tavi's mother. | EH-M2. | Fierce, practical, frightened of the test. |
| **Tavi Ostry** | Her daughter, a student. | EH-M2; micro-event EME09. | A child. Laughs easily. Never targetable. |
| **Idra Callow** | Junior teacher at the Molten Stair. | EH-M2; *Three Breaths*. | Believes in the craft and is starting to doubt the test. |
| **Hesper Tolk** | Sister of the lost crew's foreman. | EH-M3. | Wants a body to bury, not an argument. |
| **Hennet Ulm** | Cinderwall Cooling House cook. | EH-M1; EH-M6; *Shift Supper*. | Feeds first. "Sit down; you're running hot." |
| **Corm Brask** | Lower-forge shift hand listed as lost; walked out burned. **Never met** (a name on the wall and the pay list only); not found since. Not confirmed as the Mire's "man from the fire roads" (ED-16). | *The Half-Name Wall*. | None (never speaks). |
| **Imra Brask** | His kin in Cinderwall. | *The Half-Name Wall*. | Kept his name on the wall "in case". |
| **Breck Krell** | Ridge Workings quarry foreman. | *The Flarecap Seam*. | Cheerful, cautious, never sends anyone where he would not go. |
| **Brisa Teglan** | Tanner in the Cinderweave Quarter. | *Soot and Hide*; EH-M2 alternative. | Blunt; "Hide first, heat second." |
| **Teodor Marsk** | Ridge-steading hunter. | *Old Plate*. | Talks to animals more kindly than to people. |
| **Ryl Danner** | Border-Warden fletcher. | *Wardens' Quarrels*. | Dry; scorns guild smiths and loves good feathers. |
| **Tessaly Varn** | Emberforged mason from the Thornfell bible (`TAS_ACCOUNT`). | *The Seven Repairs*; EH-M6 tally board (if named). | As the Thornfell bible sets her. Present only if her account was named there. |

Minor roles (role names only unless a package names them): fire wardens, valve-house clerks, Cooling House regulars, Emberguard patrols, Deepbrand overseers, Covenant lamp-keepers, academy students, guild apprentices, gate merchants, ridge herders and charcoal burners, Dross scavengers, Forge Saboteurs.

### 5.3 Voice rules (binding)

1. **Civic pride first.** Emberholt people are proud of their city and their craft. Criticism comes from inside: *"It's our fire. That's why it matters who it warms."*
2. **Craft, never magic.** Embercraft is "craft", "work" or "the hand". Nobody calls it magic, and nobody calls a vein alive.
3. **Fire grammar.** "Running warm", "banked", "flaring", "gone grey". *"The ward's banked tonight."* *"She's flaring; give her room."*
4. **Wardens read tells.** *"Read the tell, not the talk."* Fire wardens trust the colour of a stone over what anyone says.
5. **The Speaker never lies.** He omits, reframes and thanks. Every line is checked against `[D-S1]` (§3.2).
6. **Volkhari restraint.** Short, guarded, kind when trusted. A Volkhari decides what of their life is told. No one else describes their community.
7. **Children are children.** No child is called "gifted", "dangerous" or "an asset" by a sympathetic speaker; teachers say "student".
8. **Addressing the player** is origin-neutral (D-3): "outsider" or "traveller" at first; "warden's hand" after EH-M1 among those who saw the ward reopened. Nothing else changes.
9. **Other regions** are distrusted rationally (grain, passes, old blame) and never caricatured. No region is "the invaders", and no direction is given for any enemy.
10. **Humour** is quick and warm and lives in Cooling Houses and forges. *"Hennet's soup could reopen a ward on its own."*

---

## 6. Main questline (six milestones)

All milestones use the Lowmark package format (§11). **All Emberholt codes are three letters beginning with E and never begin with "MQ"** (Lowmark uses MQ1–12), so they cannot collide with Lowmark's two-letter codes, Thornfell's T codes or the Mire's M codes. Region flags use `EH_` (§9), keeping every flag the architecture already names.

| # | Milestone | Code | Act | Where | Core verbs (primary first) | Set piece | Strange moment | Choice | Unlocks / world change |
|---|---|---|---|---|---|---|---|---|---|
| EH-M1 | **Cold Ward** | ECW | I (entry) | Cinderwall, the Undercroft, the Gate Valve House | **read tells and repair the line**, follow a paper trail | Reopening the junction at a surge: bleeding three cocks in order while Cinder Wraiths form at the vents | In the Undercroft the pipes sob, once, like someone crying. Veska: "Pipes do that." | How the ward's account is kept | `EH_TELLS`; `EH_COLD_WARD`; Cinderwall hub |
| EH-M2 | **The Ember in Every Hand** | EEH | I | Cinderweave Quarter, the Molten Stair | **assist and observe**, make gear, read a ledger | A volatility test in which a student flares and the class must be steadied | Every lantern in the court dims when Tavi cries and brightens when she laughs | Where the ledger goes | `EH_CURRICULUM` |
| EH-M3 | **The Hollow That Should Not Burn** | EGH | I (turn) | Darven's Gallery, the Glassed Hollow, the Red-Lit annex | **descend and recover**: read the glass, cross the Hollow, recover the roll | Crossing the Hollow's glass while the Embermind Echo shows a night that did not happen to you | A warm handprint, child-high, on glass that should be cold | Who hears the Hollow truth first | `EH_HOLLOW_TRUTH`; R09 |
| EH-M4 | **Ash-Stained Chains** | EAC | II | The Emberdeep Warrens, the ritual chambers | **find the way by sigils**, avoid primed plates, decide with Thalan | Reaching Thalan's frame past the proving ring | Emberlight above the chamber. Asera: "Don't look. He isn't here." | Thalan's path `[D-E2]` | `EH_THALAN`; R10 |
| EH-M5 | **The Speaker's Smile** | ESS | II (turn) | The Ash Terraces, Speaker's Hall, the Covenant lamp-house | **watch, compare and copy**: rehearsal tells, letters, a chamber record | The sleep rooms below the lamp-house while braziers flare into Wraiths | At the rehearsal the crowd's breath carries on one beat after the cue, the player's with it | How the Speaker is answered `[D-S1]` | `EH_SPEAKER`; R11, R12 |
| EH-M6 | **Embergate Accounting** | EGA | III (capstone) | Cinderwall in frost, the Undercroft, the main, the Gate Valve House | **descend the failing main**, bleed pressure, shut splices, keep a ward through the night | The Draw Sentinel at the splice junction as the main breathes | In the morning the frost has melted in lines along the mains, with dark gaps where the draw ran | Where the heat goes; who receives the account | `EH_HEAT_MAIN`; `EH_ACCOUNT`; `EH_STANDING` |

**Length targets:** EH-M1–M2 40–55 minutes each; EH-M3 55–70; EH-M4 50–65; EH-M5 45–60; EH-M6 60–75 including the tally-board scene. Main line about 5–6 hours; side content roughly doubles Emberholt's narrative hours.

**Prerequisites.** EH-M1 has **none** (travel only). EH-M2 requires EH-M1 (the architecture graph E1 → E2; the Arcs entry text reads otherwise; recommendation ED-20, for the Director). The stand-alone principle holds: the entry milestone EH-M1 has no prerequisite, and nothing before EH-M3 needs another region. EH-M3 requires EH-M2 **and** (TF-M3 **or** MR-M2) Completed (ED-7). EH-M4–M6 each require the previous milestone. No Lowmark content is ever required.

**Skill hooks.** Every milestone has at least one real skill hook with a `[GD]` level placeholder and a time-cost alternative that needs no skill. Smithing carries the hook in three milestones (EH-M1, EH-M4, EH-M6) and two side quests; Leatherworking, Mining, Ranged and Cooking each carry one milestone hook. Ranged is viable in every fight and required in none (CDR-2).

### 6.1 Milestone briefs

These briefs bind the Act packages. The packages author beats, steps, flags, encounters, dialogue and integration notes.

**EH-M1 Cold Ward (`ECW`).** *Offer:* on first entering Cinderwall (any route; MAP VERIFICATION REQUIRED). The Cooling House is full and cold. Hennet Ulm hands the stranger a bowl and says the warm air is "following the room upstairs" (teaching the phrase "heat follows the room"). Yorven Khelt is there with Veska Dunmor, whom half the room blames. Yorven needs an outsider to walk the line with Veska "so nobody can say a warden checked a warden". **Beats:** (1) **Walking the line** (`S01`): into the Undercroft with Veska. Teach the readable system (§1.1): tells clear, amber or red-crazed; the vent breath (ash lifts before the exhale); cooling niches. Cinder Rats and Slag Beetles in the ducts. On a junction door, a pasted broadsheet: *"When the passes go dark, the forges go cold."* (ED-14; never explained). On the way, the memorial plaque for the lower forge is passed and not remarked on. (2) **The junction** (`S02`): the ward's junction is shut, not broken. A brass tag reads "ceremonies office". Veska's chalk slate shows her protest: "Shut on order. Protested. Overruled." **Strange moment:** the pipes sob once, like someone crying; Veska, without looking up, says "Pipes do that." (3) **The valve house** (`S03`, `[ALLOCATION]`): up to the Gate Valve House. Odile Prace shows the book: the order signed by Sarne Ardane in the Magistrix's name; the page after it, where a protest should be, cut out. The tally board shows its usual shortfall, "old leaks" (`ECW_SHORTFALL_SEEN`, the EH-M6 seed). (4) **The Magistrix** (`S04`, `[ALLOCATION]`): Ralenne Kharveil at the terraces is sincere and dismayed; she did not read the order. Sarne Ardane admits it. "It was nine nights." Ralenne countersigns a reopening. (5) **Reopen** (`S05`): the seat ring on the junction valve is warped. **Smithing hook:** forge a replacement seat ring at the Cooling House's small forge (Smithing `[GD]`), or wait for the warden crew to fit one overnight (the quest pauses until the next in-game morning). (6) **The surge** (`S06`): opening the junction draws a surge; Cinder Wraiths form at the vents. Bleed three cocks in the order the tells show while the Wraiths re-form at each exhale until the last cock is bled. Melee or ranged. (7) **The account** (`S07`, choice, `[ALLOCATION]`): at the Cooling House, the ward asks what to say. **Post** the order and the cut page on the Cooling House board (`EH_COLD_WARD = posted`: the ward knows; Sarne is named in Cinderwall; Ralenne sends coal) or **settle** it quietly with Yorven and Ralenne for a fixed junction allotment and Veska's name cleared in the book (`EH_COLD_WARD = settled`: the ward is warm and Sarne keeps his post). Neither is wrong. As the player leaves, a small figure watches from a vent grille and is gone: the Cinder Rat. Sets `EH_TELLS`. *Re-offers:* every beat can be walked away from; the junction stays shut and the Cooling House stays cold until the player returns.

**EH-M2 The Ember in Every Hand (`EEH`).** *Offer:* Jessa Ostry, a dye-worker, asks the warden's hand to come to her daughter Tavi's volatility test: "They've changed something. She comes home with her hands shaking." Theryn Dalewright accepts a helper for the practice court ("every class needs another pair of hands"). **Beats:** (1) **The class** (`S01`): assist Idra Callow's lesson: lantern ignition, heat pulses, ember-thread, grounding breaths. The craft is shown as good. (2) **Mitts** (`S02`): the students' mitts are scorched through. **Leatherworking hook:** make heat mitts at Brisa Teglan's tannery (Leatherworking `[GD]`), or fetch a mended set from Maeryn Vall's shop (a walk and a wait). At Maeryn's, her mending book shows scorch outlines of children's hands, in pencil; she is afraid of a grey-cloaked Covenant visitor who has started to call. (Either route gives the Maeryn conversation; the skill route reaches it after.) (3) **The test** (`S03`): Selice Morra's emberglass lenses are on the test bench. The flame they focus is too narrow. Tavi flares: a hazard zone around her, non-targetable, ended by the containment interaction (steady the breath with Idra, cool the vent, carry her out). **Strange moment:** every lantern in the court dims when Tavi cries and brightens when she laughs. (4) **The lenses** (`S04`): Selice reads the curve: "This is a lens for pushing, not seeing." The schedule that changed it came from the Council. (5) **The annex** (`S05`): the assessment ledgers are kept in the annex above the heat cellar; vermin in the cellar (Cinder Rats). The ledger (`EEH_ledger`): a coded second column beside each placement; transfers to "vigil guidance", Emberguard schools, and three lines "for evaluation below". One line has Theryn's note in the margin: "Not this one." (6) **Theryn** (`S06`): confronted gently, Theryn defends the sorting as stewardship and goes quiet at "below": she knows it means Deepbrand and has never asked what happens there. She does not explain "Not this one" (the child she hid) and the quest does not push. (7) **The ledger** (`S07`, choice): give it to **the guild** of teachers through Idra, so the academies change the test (`EH_CURRICULUM = guild`: lenses changed; Theryn keeps her post), or keep it as **evidence** in Yorven's strongbox for a later accounting (`EH_CURRICULUM = evidence`: the test stays this season; the ledger reappears in EH-M6 and CV-M4). *Re-offers:* the class repeats each in-game day; the test re-runs until assisted.

**EH-M3 The Hollow That Should Not Burn (`EGH`).** *Offer:* requires EH-M2 and either TF-M3 or MR-M2 (ED-7; the locked entry names both). Hesper Tolk asks for her brother's body; Darven Mott, the only man who came out, will show the way if someone stands beside him. Kaevren Thalos signs a recovery warrant for the gallery ("I sign for bodies. That one I can sign."). **Optional variant lines:** with TF-M3 or MR-M2 Completed, the player has one extra dialogue option comparing the cut to what they saw there (a proud record proved partial; an impression that was not a witness). Darven answers only about his own crew and never shows knowledge of another region. Neither changes a step. **Beats:** (1) **Darven** (`S01`): his account; the crew; the cut "toward the glass". He knows a drain route that avoids Deepbrand's seals. (2) **Flarecap** (`S02`): Darven teaches flarecap: it glows near live veins; follow it to cool rock, avoid it in the dark. Deepbrand Crews hold the sealed mouth. (3) **The fall** (`S03`): a glassed rockfall blocks the gallery. **Mining hook:** cut through the glassed fall (Mining `[GD]`), or take Darven's slower drain route (a longer descent with two extra heat rooms). Heat gear from *Soot and Hide* is recommended, never required. (4) **The crew camp** (`S04`): the crew's last camp; Hesper's brother. A Deepbrand work order with Deepbrand's mark, routed around the Grand Marshal. (5) **The Hollow** (`S05`): across the glass. The Embermind Echo overlays the crossing with a night of fire; it never changes the ground, and the player is told to **read the tells, not the vision**. **Strange moment:** a warm handprint, child-high, on glass that should be cold. (6) **The circle** (`S06`): the circle site (required inspect; R09 site evidence): a frame broken from the inside; nothing burnt inside it. The Hollow Revenant forms at the circle (miniboss, resonance; §10). It re-forms while the heat pocket pulses; bleed the pocket at the crew's own valve to end it. (7) **The roll** (`S07`, `[INITIATE]`): Yorven leads the player out by a bypass tunnel to the Red-Lit annex. Marenya Silvertide has left the shelf open with a note: "Shelf-marks are on the spine. The rest is yours to read." The chamber roll (`EGH_roll`): heading seal cut away, every line glassed but one, `[INITIATE]`, "placed at the centre". The second sheet. The *"Keep. Do not copy."* annotation. The inspection register with its struck "visiting witness" column (R16 seed). Seredh Embercarver's memory-stone gives one Volkhari account of the night (one account; it agrees with the sheet on a child at the door). (8) **The truth** (`S08`, choice): **tell** it at the Cooling House and the forge-yard memorial (`EH_HOLLOW_TRUTH = told`: the plaque is chalked "not a collapse"; Cinderwall argues) or **keep** it with Kaevren and Marenya until the evidence is complete (`EH_HOLLOW_TRUTH = kept`: the city is quiet; Kaevren starts a second ledger). The crew is buried with dimmed flames either way. Owns **R09**.

**EH-M4 Ash-Stained Chains (`EAC`).** *Offer:* after EH-M3, Maeryn sends for the player: Dahrin Vosk has come to her back room. **Beats:** (1) **Dahrin** (`S01`): his account of where he was held; a sigil-stone that warms near true doors. He knows something more and does not say it. If the player asks twice, he says "Not here" and the quest notes it (`EAC_PRESSED`; no penalty). (2) **Allies** (`S02`): Thennek Vorren will take the player as far as the Warrens' mouth and says the Titan is "awake enough to be uncomfortable" (R19 seed). Asera comes further: she steadies breath in heat rooms, never fights. Maeryn's shop becomes a safehouse. (3) **The Warrens** (`S03`): pressure plates show a red-crazed tell when primed; step round them or wait for them to cool. Deepbrand Crews; the first Emberdeep Sentinel. (4) **The sigil gallery** (`S04`): choose doors by the sigil-stone's warmth. A wrong door is a dead end, never a trap. (5) **The chamber** (`S05`): Thalan Veyr in a basalt frame. A proving-ring slate: *"Perfect Flame: trial series."* **Strange moment:** emberlight moves above the chamber; Asera says "Don't look. He isn't here." (Kaelith, seen only.) (6) **Thalan** (`S06`, choice, `[D-E2]`): Thalan speaks for himself. **Freed** (`EH_THALAN = freed`): he agrees to go; **Smithing hook:** cut the frame's collar pins at the chamber's own anvil (Smithing `[GD]`), or wait two cool cycles for the frame to slacken; Thennek takes him onward and the player is not told where. **Aided** (`EH_THALAN = aided`): he refuses to leave: "If the frame is empty, they will fill it." The player breaks the array's draw so the frame stops working him, and promises to bring the account. Both branches are the same length. (7) **Out** (`S07`, `[D-E2]`): back to Maeryn's. Owns **R10**.

**EH-M5 The Speaker's Smile (`ESS`).** *Offer:* Seralynd Hearthveil, the Ember-Priestess, asks the player to stand in the rehearsal crowd: she has dreams she does not trust and wants an outside eye. **Beats:** (1) **The rehearsal** (`S01`): on the Ash Terraces. Read the crowd's tells: they rise together. Saelia Verithe, conducting, stops the second run and says it is "too tidy"; she wrote the cues and did not write that. (2) **The script** (`S02`): Ralenne's script has been revised: "one flame, one breath, one city". She did not write that line. (3) **The letters** (`S03`, `[D-S1]`): Kaevren's intercepts lead to a courier box in Speaker's Hall, reached through the Cinder Rat's duct. The letters (`ESS_letters`) are addressed to "the Seat" and answered. They show the Speaker asked for help in his rise and accepted it. They do not show the Ashfall endgame. (4) **The sleep rooms** (`S04`, `[D-S1]`): Serix Arden lets the player into the Hearthveil rooms below the Covenant lamp-house. Braziers flare into Cinder Wraiths. The chamber record: the Speaker's vigil nights; a list of guided sleepers including Vael Trossen. Copied under Serix's witness. (5) **The damper** (`S05`): the record room's damper is jammed. **Ranged hook:** shoot the damper latch from the gallery (Ranged `[GD]`), or climb the ladder and wait two vent cycles. **Strange moment:** at the next rehearsal the crowd's breath carries on one beat after the cue; the player's breath does too. (6) **The answer** (`S06`, choice, `[D-S1]`): **challenge** him in public through Seralynd, who speaks on the terrace (`EH_SPEAKER = challenged`: the crowd hears doubt; the rehearsal ends early) or **expose** the record to a sealed inquiry under Vael Trossen (`EH_SPEAKER = exposed`: the Council knows; the public does not). The Speaker stays in office in both; the High Kindling still happens. Owns **R11** and **R12**.

**EH-M6 Embergate Accounting (`EGA`).** *Offer:* automatic after EH-M5 when the player next enters Cinderwall: a hard frost (`EGA_FROST`). The main is failing under Cinderwall; the cold ward is freezing above while pressure builds below. **Beats:** (1) **Warming houses** (`S01`): the Cooling Houses become warming houses. **Cooking hook:** cook for the warming house (Cooking `[GD]`), or work Hennet's kitchen through a shift. An Ember-Fused worker flares in the cold: containment interaction (ED-2). (2) **The descent** (`S02`): with Veska's crew, down the main in three pressure stages; Dross Scavengers stripping fittings; Slag Beetles. (3) **The bleed** (`S03`, choice): the pressure must go somewhere: into **the terraces**, **the ward** or **the forges** (`EH_HEAT_MAIN`). **Smithing hook:** forge bleed wedges (Smithing `[GD]`), or wait while the crew holds it for two cycles. (4) **The splices** (`S04`): collars with valve-house numbers and Deepbrand marks. The junction book (`EGA_junction_book`): "for the proving rings"; *"Perfect Flame: draw holds"*; "the old circle keeps this season". (5) **The far doors** (`S05`): sealed from the other side. The Remnant withdraws deeper; nobody retreats past the player. (6) **The Draw Sentinel** (`S06`, boss, §10.1): at the splice junction. If the player is defeated, they wake at the warming house with the quest Active and every splice already shut kept shut. (7) **Morning** (`S07`): **strange moment:** the frost has melted in lines along the mains, with dark gaps where the draw ran. (8) **The tally board** (`S08`, choice): at the valve house the board balances for the first time. Who receives the account: **the guilds** (`EH_ACCOUNT = guilds`) or **the Council** (`EH_ACCOUNT = council`). Who stands at the board depends on earlier flags (§9.3). Sets `EH_STANDING`. A letter arrives from the Speaker: "The city will learn from this night." `[D-S1]`

### 6.2 Main-quest contribution contract (§7.1, six fields)

| Code | Anchor | World-truth row | Revelation role | Recurring evidence (independent custodian) | State compliance | Combat compliance |
|---|---|---|---|---|---|---|
| ECW | Fire wardens; Cinderwall households | H23, H25 present pressure (local) | Plants R15 (broadsheet; unexplained); EH-M6 shortfall seed | Valve-house book (Odile) + Veska's slate + the cut page | `EH_COLD_WARD` posted / settled; no fail; the Smithing hook has a wait | Cinder Rats, Slag Beetles, Cinder Wraiths to 0 HP; Wraiths re-form at each exhale until bled; melee or ranged; solo |
| EEH | Academies; Cinderweave households | H13 (aftermath), H22 | Seeds R18 (volatility tests; the curriculum ledger as custodian) | Assessment ledger (`EEH_ledger`; academy custody) + Selice's lens reading + Maeryn's mending book | `EH_CURRICULUM` guild / evidence; the test re-runs | Cinder Rats only; Tavi's flare is a hazard; solo |
| EGH | Deepbrand's lost crew; Red-Lit archive | **H18**, H09 | **Owns R09**; seeds R16 (inspection gap) and R19 (the roll's one line) | Chamber roll (`EGH_roll`; Marenya's shelf-marks) + Seredh's memory-stone + the circle site | `EH_HOLLOW_TRUTH` told / kept; the Mining hook has a slower route | Deepbrand Crews to 0 HP; the Hollow Revenant re-forms while the pocket pulses; ranged viable; solo |
| EAC | Volkhari individuals | H03, H18, H22 | **Owns R10**; seeds R19 | Sigil-stone (Dahrin) + proving-ring slate + Thalan's own words | `EH_THALAN` freed / aided `[D-E2]`; wrong doors are dead ends | Deepbrand Crews, an Emberdeep Sentinel to 0 HP; plates are hazards; solo |
| ESS | Council and Covenant | H21, H22 | **Owns R11, R12**; seeds R18 (rehearsals) | Letters (`ESS_letters`; Kaevren's intercepts) + chamber record (Serix's witness) | `EH_SPEAKER` challenged / exposed `[D-S1]`; the Ranged hook has a climb | Cinder Wraiths to 0 HP; re-form while braziers burn; solo |
| EGA | Fire wardens; guilds; Council | H22, H25, H18 (record) | Pays off EH-M1 seed; Emberholt's stop enters the civic record | Junction book (`EGA_junction_book`) + valve-house book + splice collars | `EH_HEAT_MAIN`; `EH_ACCOUNT`; a beaten player wakes at the warming house with shut splices kept | Dross Scavengers, Slag Beetles, the Draw Sentinel to 0 HP; no SX; ranged viable; solo |

---

## 7. Side-quest slate (20 quests; Phase 1.5 range 16–22)

Three **interconnected questlines** (8 quests) and twelve standalone quests. **16 of 20 have no cross-region link or cross-region seed** (architecture rule: at least half self-contained). The four with a cross-region read are *Sound Stock* (ESK), *The Half-Name Wall* (ENW), *The Commissioner's Cargo* (ECC) and *The Seven Repairs* (ESR); each reads only flags their owners define and each works without them. Six side quests (ETB, EMS, EAD, ENW, EGT, ECC) unlock after EH-M3 or later, so they wait on its cross-region gate (ED-7); the other 14 are reachable with no other region's content. Codes are three letters beginning with E, never "MQ".

### 7.1 Interconnected questlines

| Code | Quest | Series (part) | Type | Unlock | Where | Core verb | One-line pitch | Feeds |
|---|---|---|---|---|---|---|---|---|
| EWA | **The Water That Did Not Arrive** | Heat Commons (1/3) | Settlement | After EH-M1 | Cinderwall, the Cooling House, the Undercroft | trace, repair, share | The Heat Commons' wash water runs cold while the ward's heat is back. A shared cistern pipe was rerouted when the junction was shut and never put back. Trace it and decide the rota. | `[ALLOCATION]` lines only; teaches junction reading again in a smaller space |
| ECN | **The Case That Never Reached the Court** | Heat Commons (2/3) | Combat challenge | After EWA | Slagside, the Dross Scavenger Pits | track, recover, return | Scavengers are stripping Commons pipe for scrap and a ward complaint has sat unheard for a season. Recover the fittings from the pits and put the case where it will be heard. | Dross Scavengers (human, to 0 HP); the complaint reaches Yorven's book |
| EFC | **First Cooling** | Heat Commons (3/3) | Festival | After ECN and EH-M2 | Cinderwall, the Cooling House | cook, carry, celebrate | The ward's own festival on the first night the heat is shared fairly: food, songs, a dimmed flame for the year's dead. Hennet wants it plain; the young want it bright. | Sets `EH_COMMONS`; the ward fills the EH-M6 warming house faster |
| EST | **Stitches in the Lining** | Unburnt (1/3) | Settlement | After EH-M2 | Maeryn's shop, Cinderweave | mend, steady, keep | A hooded youth keeps coming to Maeryn's back door for headbands and long sleeves that will not scorch. He is Kaelen Veyr'un, and a Covenant visitor is in the front of the shop. When he flares, steady the room, then decide with Maeryn what goes in her book. | Kaelen's emberburst is a hazard (never targetable); Maeryn's trust |
| ETB | **Three Breaths** | Unburnt (2/3) | Memory/lore | After EST and EH-M4 | The Molten Stair, Idra's rooms, Maeryn's back room | practise, compare, teach | Idra Callow has found an older grounding exercise in a pre-war primer: three breaths, not one. It steadies flares better, and the academy calls it "out of syllabus". Asera of the Three Breaths, asked through Maeryn, recognises it and decides how much to say. | Supports R18 (what the test is for); never explains Perfect Flame |
| EMS | **The Memory-Stone** | Unburnt (3/3) | Memory/lore | After ETB and EH-M3 | Seredh's workroom; the Cold Seam | listen, carry, decide | Seredh asks the player to carry a memory-stone to the Cold Seam so it can be kept where no heat rises. A Covenant collector wants it "for safekeeping". | Sets `EH_UNBURNT` kept / strained (strained is mendable by a later visit) |
| ESK | **Sound Stock** | Guild Ledgers (1/2) | Skill intro (Smithing) | After EH-M1 | The Emberforges, guild yard | inspect, forge, test | Durnan Volkryst tests an outsider's hands: forge a sound bar from imported stock and learn why Emberholt smiths ring every bar twice. | Smithing intro. Optional Lowmark line from `HS_SALVAGE_KEEPERS` / `HS_SALVAGE_REFUSED` (*Honest Steel*): Durnan has heard of a forge that refuses salvage. |
| EOM | **The Old Methods** | Guild Ledgers (2/2) | Combat challenge | After ESK and EH-M2 | The Emberforges; the Saboteurs' Kiln | inspect, track, assault | New safety rules at Durnan's Basalt Forge Guild are being sabotaged. A rival forge is blamed; the saboteurs are a crew Durnan once dismissed, working from a ridge kiln. | Forge Saboteurs and the Saboteur Captain (to 0 HP); sets `EH_GUILDS` |

### 7.2 Standalone side quests

| Code | Quest | Phase 1.5 type | Unlock | Where | Core verb | One-line pitch | Systems link | Cross-region |
|---|---|---|---|---|---|---|---|---|
| EFS | **The Flarecap Seam** | Skill intro (Mining) | After EH-M1 | The Ridge Workings | mine, read, haul | Breck Krell teaches the ridge: follow flarecap to the seam, and leave the seam when the tells go amber. | Mining intro; flarecap reading reused in EH-M3. Ore names are proposals for the economy pass. | None |
| EWQ | **Wardens' Quarrels** | Skill intro (Fletching, Ranged) | After EH-M1 | Embergate yards; the Ash Roads | salvage, fletch, shoot | Ryl Danner, fletcher to Haelric Stormvein's Border-Wardens, needs crossbow quarrels and the guild will not sell to them. Shafts from reclaimed crate-wood, magma-lark fletching, heads from the Smithing yard. | Fletching → Ranged loop (CDR-2); Woodcutting only as reclaimed crate-wood (source process); Smithing heads optional | None |
| ESP | **Shift Supper** | Skill intro (Cooking) | After EH-M1 | The Cooling House | cook, carry, serve | Hennet needs a shift supper for the night crews that keeps hot in a pail. | Cooking intro; reused as the EH-M6 Cooking hook | None |
| ESH | **Soot and Hide** | Skill intro (Leatherworking) | After EH-M1 | Brisa Teglan's tannery | cut, stitch, fit | Brisa teaches heat gloves and a leather hood for duct work. | Leatherworking intro; heat gear recommended (never required) in EH-M3 | None |
| EOP | **Old Plate** | Skill quest (Hunting) | After EH-M2 | Ridge Steadings, the Molten Scars | track, hunt, decide | An old emberback sow with a hide like slag plate is taking steading stock. Teodor Marsk wants her dealt with and is sorry about it. | Hunting; Old Plate is a side miniboss (wildlife, §10) | None |
| EBL | **The Ward That Answers Its Own Bell** | Settlement (Cinderwall) | After EH-M1 | Cinderwall streets | listen, read, mend | The shift bell rings by itself at night. It is a pressure valve tied to the bell rope during the cold-ward nights and forgotten. Mend it and decide whether the ward keeps it as a warning. | Veska appears; uses tells | None |
| EFD | **The Flame That Would Not Die** | Environmental | After EH-M2 | Elyndra's Vent Shrine | tend, observe, decide | A shrine flame burns on with no fuel the keeper can find. Pilgrims call it Elyndra's. A vent feeds it from below. | Belief kept as belief; the vent is real; Elyndra unproven | None |
| EAD | **The Vein-Touched Man** | Settlement / care | After EH-M3 | The Embervein Tap; Sereth's clinic | find, contain, carry | Myr Adalrek has gone to the exposed vein at Dalia Vret's tap. Bring him to Sereth Vorn without hurting him. | Ember-Fused containment (ED-2); Dalia's camp, no combat with her | None |
| ENW | **The Half-Name Wall** | Memory/lore (Register of the Unreturned) | After EH-M3 | The Half-Name Wall; the Old Lower Forge; Cinderwall | search, match, decide | Imra Brask keeps her kinsman's half-name on the wall "in case". The lower-forge pay list shows he drew his pay, in his own mark, after the night of the "collapse": he walked out burned. Find what can be proved, then decide what the wall says. | Register case (§7.6); sets `EH_HALF_NAME` named (his full name moved from "lost" to "walked out; not found since") / held (Imra keeps the half-name) | Optional, unconfirmed Mire echo `MDS09_READ`: Imra hears of a burned man who would not give his name and decides whether to hope. Never a hold, never identity proof, no route (ED-16). Complete without it. |
| EGT | **Glassmoth's Tonic** | Memory/lore (Dreamers) | After EH-M5 | Glassmoth's stall; the lamp-house | ask, compare, decide | Glassmoth sells a tonic that stops dreams. Three customers had the same dream on the same night. | Supports R12 (one more access pattern); never dismisses all Dreamers | None |
| ECC | **The Commissioner's Cargo** | Mystery | After EH-M4 | Embergate yards; Oren Falx's office | inspect, trace, decide | Haelric Stormvein's wardens flag a sealed case passing the gate under Oren Falx's signature: river timetables, bound for a merchant-house front whose owner nobody at the gate can name. | ED-15: one discoverable act beyond Emberholt (FT-04), unattributed in play (no Remnant or Durell name; R15 is CV-M2's); sets `EH_RIVERGLASS` | Optional Lowmark line from `UL_LEDGER_GIVEN` / `UL_LEDGER_TAKEN`: the player thinks the ruled paper looks like the Lowmark ledgers they handled. Flavour only: no transaction matched, no Lowmark cause, no route. |
| ESR | **The Seven Repairs** | Environmental | After EH-M1 | The Bridge of Seven Repairs | read, repair, credit | Seven crews repaired one bridge across thirty years; each left a mark. The bridge plaque credits one guild. | Smithing or a crew wait for the eighth repair | Optional Thornfell line from `TAS_ACCOUNT` = named: Tessaly Varn's crew mark is one of the seven, and she comes to see it. |

### 7.3 Side-quest contribution contract (§7.1, six fields)

| Code | Anchor | World-truth row | Revelation role | Recurring evidence | State compliance | Combat compliance |
|---|---|---|---|---|---|---|
| EWA | Heat Commons; fire wardens | H23 | None (local) | Veska's slate (recurs from ECW) | No fail; rota choice is text only | Cinder Rats to 0 HP; solo |
| ECN | Heat Commons; Slagside | H23, H25 (local) | None | The ward complaint (Yorven's book) | Fittings recovered or crew-recovered next morning | Dross Scavengers to 0 HP; ranged viable; solo |
| EFC | Cinderwall households | H23 | None | None | `EH_COMMONS`; festival always completes | None |
| EST | Volkhari individuals (Maeryn, Kaelen) | H03 | None | Maeryn's mending book (recurs from EEH) | Kaelen's flare is a hazard; steadying cannot fail | None |
| ETB | Academies; Asera | H03, H13, H22 | Supports R18 | Pre-war primer (read in place) + Asera's own account | No fail; Asera's lines about Thalan are `[D-E2]` | None |
| EMS | Seredh; Covenant collector | H03, H18 | Supports R09 (weight only) | Memory-stone (carry-state) | `EH_UNBURNT` kept / strained; strained mendable | None |
| ESK | Forgeguilds | H23 | None | None | Bars can be re-forged | None |
| EOM | Forgeguilds; Forge Saboteurs | H25 (local) | None | Kiln ledger (read in place) | `EH_GUILDS` reformed / restored; no fail | Forge Saboteurs, Saboteur Captain to 0 HP; ranged viable; solo |
| EFS | Ridge miners | H02 (surface only) | None | None | Seam re-offers | Slag Beetles to 0 HP; solo |
| EWQ | Border-Wardens | H25 (local) | None | None | Crate-wood re-spawns | Emberback Boars to 0 HP; ranged natural; solo |
| ESP | Cooling House | H23 | None | None | No fail | None |
| ESH | Cinderweave artisans | H23 | None | None | No fail | None |
| EOP | Ridge steadings | H13 (Molten Scars as place) | None | None | Hunt re-offers at dusk | Emberback Boars and Old Plate to 0 HP; melee or ranged; solo |
| EBL | Cinderwall; fire wardens | H23 | None | The bell valve (inspect) | Keep / remove; no fail | None |
| EFD | Shrine keepers | H01 (belief only) | None | None | No fail | Cinder Wraiths at a surge (optional); solo |
| EAD | Ember-Fused workers; Sereth Vorn | H22 | None | Sereth's clinic book | Containment cannot fail; re-offers | Slag Beetles at the tap to 0 HP; Myr never targetable; solo |
| ENW | Register; Cinderwall households | **H18**, H23 | Supports R09 (civilians above the chamber); Register case | The wall + the lower-forge pay list (both in Emberholt); the Mire Rootrest book is an optional echo only (`MDS09_READ`), never a custodian | `EH_HALF_NAME` named / held; no fail | None |
| EGT | Dreamers; Hearthveil | H21 | Supports R12 | Customer accounts + the lamp-house access book | No fail | None |
| ECC | Merchant houses; Oren Falx; Haelric Stormvein | H22, H25 | Seeds R15 (one bounded act; CV-M2 owns) | Gate manifest + the timetable case | `EH_RIVERGLASS` reported / held; no fail | Dross Scavengers at the yard (optional) to 0 HP; solo |
| ESR | Masons and crews | H23 | None | The seven marks (inspect in place) | Credit choice text only | None |

### 7.4 Micro-events (10; Phase 1.5 range 6–10)

| Id | Micro-event | Where | What happens | Interaction |
|---|---|---|---|---|
| EME01 | **A lantern at a gesture** | Any street at dusk | A child lights a doorway lantern with a flick of two fingers and looks to see if anyone noticed. | Notice; nod. |
| EME02 | **Mood banners** | Cinderwall | Street cloths change with the ward's week: grey after a burial, red on a forge feast. | Read; ask. |
| EME03 | **The dimmed flame** | A Cooling House | At a death, every lamp in the room is turned down by one notch and left there for the night. | Turn yours down or don't. |
| EME04 | **Flame-balancing on the stair** | The Molten Stair | Students walk the stair holding a small flame steady in a palm while an elder calls the breaths. | Watch; walk with them. |
| EME05 | **A hearthfire argument** | Cooling House | Two neighbours argue whose turn it is at the hearth; the room votes with spoons. | Vote with a spoon. |
| EME06 | **Shift bells** | Cinderwall and the forges | Bells mark shift change; the streets fill and empty. | None. |
| EME07 | **Warm stones** | Cooling House | An elder passes a warm stone round while telling a story; whoever holds it may speak. | Hold it; listen. |
| EME08 | **Magma larks** | The Ridge | Larks bathe in vent shimmer and scatter at a footstep. | Watch; feathers can be gathered for EWQ. |
| EME09 | **Hold it steady** | Cinderweave courtyard | Children play a game: whose flame stays still longest. Tavi plays if EEH is complete. | Join with a lantern. |
| EME10 | **The hourly tally** | The Gate Valve House | Odile calls the hour's figures and chalks the board. Before EH-M6 the last column never balances; after, it does. | Read the board. |

### 7.5 Discoveries (three-layer framework)

Each has a surface (what anyone sees), a reading (what a careful player learns) and, where marked, a withheld layer. Flags `EDS##_SEEN` / `EDS##_READ`.

| Id | Discovery | Surface | Reading | Withheld |
|---|---|---|---|---|
| EDS01 | **The Ash Roads** | Cracked streets lined with burnt engravings [CANON]. | Some engravings are Volkhari symbols, scraped away by the city [CANON; R09 seed]. | Who carved them and who scraped them. |
| EDS02 | **The Molten Scars** | Ridges melted into glassy slopes. | Siege-craft scorch patterns [CANON H13]; Emberholt melted its own ground. | Who ordered it. |
| EDS03 | **A backlash zone** | A circle of fused cobbles in an old yard. | An embercraft backlash; the paving was laid around it rather than mended. | Who was hurt. |
| EDS04 | **The Ash-Clad Giant chalk** | Children's chalk of a giant on a duct wall. | The legend [CANON]; a fire warden has chalked "not funny" beside it. | Everything. **Never explained.** |
| EDS05 | **Elyndra's Vent Shrine** | Offerings at a vent that never cools. | The vent is real; the story is belief. | Whether Elyndra lived. |
| EDS06 | **Cinderreach Spire's sign** | A weathered sign on the spire path. | A pre-war waymark in a hand that no longer matches civic script. | Its meaning. |
| EDS07 | **The Cold Seam** | A fissure with no heat; people sit there. | A place of quiet grief [Part 3]; small cold stones left for the dead. | Why it is cold. **Never explained.** |
| EDS08 | **Joren Vale's draft map** | A torn survey sheet in a gate-yard crate. | Sealed rooms beneath the Warrens marked on it (R10 seed). | What the rooms were. |
| EDS09 | **The forge-collapse memorial** | The plaque on the old lower forge's wall. | Names of shift hands "lost in the collapse"; one is chalked over later (ENW). | Whether all were lost there. |
| EDS10 | **A Volkhari Ash seizure notice** | A gate-yard notice of contraband seized. | "Volkhari Ash" seized; the notice is signed by Deepbrand, not the gate (R10 seed). | What it is made from. |

### 7.6 The Register of the Unreturned: shared civilian ledger (Emberholt cases)

Each case resolves where its family lives; none is required by any milestone.

| Case | Region owning resolution | Emberholt hold | Other hold | Status |
|---|---|---|---|---|
| **Corm Brask** (ENW) | Emberholt | The Half-Name Wall; the lower-forge pay list | None (the Mire Rootrest book, `MDS09_READ`, is an optional unconfirmed echo, not a hold; ED-16) | Optional; two Emberholt holds; recorded "walked out; not found since" |
| **The lost crew** (EH-M3) | Emberholt | The crew camp; Hesper Tolk's testimony | Deepbrand's work order | Main path; local |
| **The children "for evaluation below"** (EH-M2) | Emberholt (CV-M4 later) | The assessment ledger | None yet | Held open; no outcome stated in Emberholt |

---

## 8. Revelation map (worked backward from the payoffs)

### 8.1 Owned revelations

| Rev | Truth | Owner | Custodians (two, never a phenomenon) | Seeds before payoff | Wrong reading supported | Guaranteed path |
|---|---|---|---|---|---|---|
| **R09** | Emberholt's war ended in the Glassed Hollow, hidden as a forge collapse; a precursor initiate became the Titan; Kaelith escaped; Thalan was taken later. | EH-M3 | The chamber roll and second sheet (`EGH_roll`, Marenya's shelf-marks); Seredh's memory-stone (one account). Site evidence: the circle site (S06). | The memorial plaque (ECW, EDS09); Darven's breathing walls; the sobbing in the pipes; *The Half-Name Wall*. | It really was a collapse; the Volkhari caused it; the Titan is a Volkhari. | EH-M3 S06 (circle site) and S07 (roll and sheet) required inspects. |
| **R10** | Thalan lives, in a frame, used for Perfect Flame research. | EH-M4 | Dahrin's account; the chamber and its proving-ring slate. | Volkhari reluctance; EDS10 seizure notice; EDS08 draft map. | No captive survives. | EH-M4 S05. |
| **R11** `[D-S1]` | The Speaker knowingly accepts Remnant help for his own rise and is also dream-seeded. | EH-M5 | Letters (`ESS_letters`); the Hearthveil chamber record. | Rehearsals; Ralenne's revised script; councillors quoting one dream. | Wholly puppet or wholly mastermind. | EH-M5 S03 and S04. |
| **R12** | Some visions are induced. | EH-M5 (Dreamers deepen it) | Chamber record + access pattern. | *Glassmoth's Tonic*; Seralynd's doubts. | All Dreamers are frauds, or all are prophets. | EH-M5 S04. |

### 8.2 Seeds Emberholt plants for others

| Seed | Where | Pays off | Rule |
|---|---|---|---|
| The reversed broadsheet phrase | EH-M1 S01 (ED-14) | R15 (CV-M2) | Unattributed; never explained in Emberholt. |
| The inspection gap ("visiting witness" struck) | EH-M3 S07 | R16 (CV-M1) | Never explained in Emberholt. |
| Volatility tests; curriculum ledgers; rehearsals | EH-M2, ETB, EH-M5 | R18 (CV-M4) | Shown as practice, never as a plan. |
| The roll's one line `[INITIATE]`; Thennek's "awake enough"; "the old circle keeps this season"; the warm handprint | EH-M3, EH-M4, EH-M6 | R19 (CV-M4) | The Titan is never met, described or explained. |
| The river timetables | ECC | R15 (CV-M2) | One bounded act, unattributed in play; no Lowmark cause, no route. |

### 8.3 Misunderstanding ladder in Emberholt

| Topic | First reading | After EH-M3 | After EH-M6 |
|---|---|---|---|
| The cold ward | A careless warden. | An order that followed influence. | One small case of a main that always favoured the top. |
| The schools | Strict and proud. | Sorting children by a test changed from above. | Practice that someone below has been measuring. |
| The forge collapse | An accident. | The Glassed Hollow. | The war's end in Emberholt, now in the civic record. |
| The Remnant | A rumour. | Papers kept by someone. | A draw on the city's heat, exposed and withdrawn deeper, not ended. |

---

## 9. World state

Solo-first (Pillar D): all state is per player. **Presentation fallback only, governed by CDR-6 (2026-11-14):** every quest, boss and reward is completable by one player and co-op is optional assistance. Where per-player props are not available, one shared visual state (for example the host's) may be shown. It never decides another player's walkable ground, interaction availability, step, credit or choice: each player's own quest state decides their own heat zones, junctions and splices (MI-CO-06 pattern).

### 9.1 Region flags (persist on the character)

Prefix `EH_`. Quest-local flags use the quest code (`ECW_…`, `EGA_…`). The eight flags the architecture names are kept unchanged.

| Flag | Values | Set by | Read by |
|---|---|---|---|
| `EH_TELLS` | bool (tells learned) | EH-M1 | Tell inspect text everywhere |
| `EH_COLD_WARD` | posted / settled `[ALLOCATION]` | EH-M1 | EWA, EFC lines; EH-M6 tally board |
| `EH_CURRICULUM` | guild / evidence | EH-M2 | ETB; EH-M6; CV-M4 |
| `EH_HOLLOW_TRUTH` | told / kept | EH-M3 | Memorial props; ENW; EH-M6; CV-M1 |
| `EH_THALAN` | freed / aided `[D-E2]` | EH-M4 | EH-M6 tally board; CV-M4 |
| `EH_SPEAKER` | challenged / exposed `[D-S1]` | EH-M5 | Terrace barks; EH-M6 letter; CV-M4 |
| `EH_HEAT_MAIN` | terraces / ward / forges | EH-M6 | Post-story heat states; barks |
| `EH_ACCOUNT` | guilds / council | EH-M6 | CV-M1 custody |
| `EH_STANDING` | bool | EH-M6 | Emberholt master commissions; CV-M1 gate |
| `EH_UNBURNT` | kept / strained | EMS | Volkhari lines; EH-M6 tally board |
| `EH_GUILDS` | reformed / restored | EOM | Forge barks; EH-M6 bleed lines |
| `EH_COMMONS` | bool | EFC | EH-M6 warming house |
| `EH_HALF_NAME` | named / held | ENW | Memorial props; CV-M1 Register |
| `EH_RIVERGLASS` | reported / held | ECC | CV-M2 (request) |

### 9.2 Heat states (per player)

Each heat zone has a small authored schedule of three states (Cool, Working, Surging) keyed to the presentation hour, as the Mire's channel states are (MI-CH-01). A state swaps hazard volumes, vent timings and tells. **Waiting is always available** in a cooling niche until the next state. Quests may pin a zone's state for a step. No temperature simulation, no meter, no world clock.

### 9.3 Who stands at the tally board (EH-M6)

The scene always completes; flags decide who stands there.

1. Always: Veska, Odile, Yorven, Hennet.
2. `EH_COLD_WARD` = posted: the Cooling House regulars stand behind Veska; = settled: Ralenne sends a clerk with the coal book. `[ALLOCATION]`
3. `EH_CURRICULUM` = guild: Idra brings two teachers; = evidence: the ledger is laid on the board.
4. `EH_HOLLOW_TRUTH` = told: Hesper Tolk and Darven stand together; = kept: Kaevren comes with his second ledger.
5. `EH_THALAN` `[D-E2]`: = freed: Thennek sends word, one line; = aided: Asera brings "the account he asked for".
6. `EH_UNBURNT` = kept: Maeryn and Seredh stand at the back.
7. `TAS_ACCOUNT` = named (Thornfell): Tessaly Varn stands with the masons.

### 9.4 Shared conventions

- **Presentation hour** reused from Lowmark for heat states and waits.
- **Defeat** (CDR-1): every enemy is defeated at 0 HP with the ordinary defeat presentation. Resonance enemies re-form while their condition lasts. No Emberholt SX entry.
- **Containment interactions** for Ember-Fused workers and flaring children are channelled interactions (§11.1), never combat.
- **Quest items:** Emberholt budget 5 (`EEH_ledger`, `EGH_roll`, `ESS_letters`, `EGA_junction_book`, and Dahrin's sigil-stone as a carry-state object rather than an item if the budget is 4). Side quests use carry-state objects, read-in-place records, or none.

---

## 10. Encounter families (summary; full requirements in the Enemies package, Batch 4)

Nine families from dossier ecology. Magma larks and ridge goats are ambient. Ember-Fused flares, the Embermind Echo and pressure plates are **hazards**, not families.

| Tier | Family | Role | Standard variants | Elite | First seen |
|---|---|---|---|---|---|
| Low | Cinder Rats | Duct vermin | scurrier, biter | — (vermin) | EH-M1 |
| Low | Slag Beetles | Armoured beetles on slag and vents | crawler, sprayer | — (wildlife) | EH-M1 |
| Low | Emberback Boars | Ridge boars with heated hide | boar, tusker | **Old Plate** (side miniboss) | EWQ / EOP |
| Low | Dross Scavengers | Human pipe-strippers | scavenger, slinger | — | ECN; EH-M6 |
| Mid | Forge Saboteurs | Smuggler band that targets emberwork [CANON]; in EOM led by a crew Durnan once dismissed [NEW] | wrecker, thrower | **Saboteur Captain** | EOM |
| Mid | Deepbrand Crews | Deep-works guards and hands | guard, crossbow | — | EH-M3 |
| Mid | Cinder Wraiths | Surge silhouettes; re-form while the vein surges | wraith, flare | — | EH-M1 |
| High | Ashfall Revenants | Resonance constructs from trauma | revenant, glasswalker | **the Hollow Revenant** (EH-M3 miniboss) | EH-M3 |
| High | Emberdeep Sentinels | Remnant constructs | sentinel, warden-frame | **the Draw Sentinel** (EH-M6 boss) | EH-M4 |

**Elites.** Dross Scavengers, Deepbrand Crews and Cinder Wraiths have none on purpose: no scavenger is made a boss, Deepbrand's commander is reserved for later content, and Wraiths are phenomena. Recorded deviation.

**Count:** 18 standard variants + 4 elites (Old Plate, Saboteur Captain, Hollow Revenant, Draw Sentinel) = **22**. **Bosses:** 1 Act III boss (the Draw Sentinel) and 2 minibosses (the Hollow Revenant, Old Plate), matching Phase 1.5 §4.3.

**Ranged and melee (CDR-2).** Every encounter is designed for both. Slingers, throwers and Deepbrand crossbows give ranged players something to answer; heat rooms give melee players cooling niches to fight from. Wraiths re-form at their condition, so out-ranging them never ends a fight on its own. No fight needs ranged.

### 10.1 Boss brief: the Draw Sentinel (EH-M6)

| Element | Brief |
|---|---|
| Arena | The splice junction below Cinderwall: four splice collars round a central draw valve, two cooling niches, one vent. |
| Phase 1: "Draw" | The Sentinel pulls heat from the collars; open collars feed it a visible glow and a damage shield. Shutting a collar (channelled interaction) removes one source. |
| Phase 2: "Seal" | It closes the niches with plates on a telegraphed cycle; the vent breath shows when a niche will open. |
| Phase 3: "Vent" | It vents stored heat in lines along the floor, telegraphed by tells. At 0 HP it seizes and cools. |
| Defeat | 0 HP. It is destroyed (construct). |
| Failure | A beaten player wakes at the warming house with the quest Active; every collar already shut stays shut. |
| Never | It never speaks, never carries a name, and never yields evidence. The junction book is found before the fight. |

---

## 11. Authoring conventions (binding for every Emberholt package)

1. **Format.** Quest packages follow the Lowmark act-package format, with all six §7.1 contract fields on every summary card. Dialogue follows the Lowmark node format.
2. **Ids.** Content ids `emberholt.main.NN_slug` and `emberholt.side.slug` (suggested; the Schema & Content Engineer owns naming). Steps `S00_…`. Quest-local flags `<CODE>_…` with three-letter E codes (never `MQ…`); region flags `EH_…` from §9.1 only. Dialogue nodes `<CODE>-D<n>.<nn>`; barks `<CODE>-B<n>.<nn>`; encounters `<CODE>-E<n>`. POIs `EP##`, micro-events `EME##`, discoveries `EDS##` with `EDS##_SEEN` / `EDS##_READ`.
3. **Evidence rule.** Phenomena never identify a person, prove guilt or name the dead. Combat never reveals evidence, and no defeated enemy ever speaks testimony. Every revelation has two holds (§8).
4. **Three states only.** Inactive, Active, Completed. No fail or abandon logic. A player who walks away resumes at the persisted step. Choices are outcome flags. Missed moments (a surge, a rehearsal, an optional ask) are re-offered.
5. **Combat (CDR-1, CDR-2, CDR-6).** Every enemy fights to 0 HP. No yields, no "downed" state. Every fight can be won solo, with melee or ranged; none requires ranged. No SX exception.
6. **Rewards.** Access, knowledge (tells), small payments, standing, tools named functionally. No lump quest XP. No items beyond §9.4 unless the item pass defines them.
7. **Tone.** Proud, warm, uneasy. At least one moment of wonder or unease per quest. No cutscenes; the camera stays with the player.
8. **No player spellcasting.** Embercraft is something NPCs do; the player reads tells, works valves and makes things.
9. **Tags.** `[ALLOCATION]` (§3.1), `[D-E2]`, `[D-S1]` (§3.2), `[INITIATE]` (ED-3).
10. **Map.** Relative placement only; mark **MAP VERIFICATION REQUIRED**. No route or direction to another region. No "eastern" or "invader" wording.
11. **Status labels.** [CANON], [APPROVED — id], [NEW], [PROPOSAL — DIRECTOR], MAP VERIFICATION REQUIRED.
12. **Scope.** No schema, JSON or C#. Lowmark content is never required; Thornfell or Mire is required only at the EH-M3 gate (ED-7).

### 11.1 Mechanics: standard RPG systems (CDR-4)

| Mechanic | System used | Status |
|---|---|---|
| Inspect, carry-state objects, read-in-place records | Lowmark/Thornfell interaction set | Standard |
| Channelled interactions (bleed a cock, shut a collar, steady a breath, carry a person) | Lowmark channel convention with kept progress | Standard |
| Heat rooms | Hazard volumes with periodic damage; cooling niches as safe volumes | Standard |
| Vents and pressure plates | Timed hazards with visible tells | Standard |
| Showing evidence to an NPC | Dialogue options gated by quest flags | Standard |
| Resonance enemies re-forming by condition | Lowmark drift-site state model | Standard |
| Waiting for a state | Presentation-hour wait | Standard |

**Explicitly not used:** heat or temperature meters, stamina, stealth or detection, new UI modes, a reputation meter.

### 11.2 Needs that may require new runtime support (few; for the integration handoff)

| # | Need | Smallest form | Fallback if not built |
|---|---|---|---|
| EI-HT-01 | **Heat-state schedule per zone** (three states) | Reuse MI-CH-01's per-crossing state table | Quest-pinned states only |
| EI-PR-01 | **Staged pressure** in the EH-M6 main (three stages) | Reuse MI-WL-01's environment-variant swap | None needed; this is the fallback form |

These are the only two, and both reuse Mire integration patterns. No new system.

---

## 12. Production plan and file map

| Batch | Content | Files | Status (2026-11-14) |
|---|---|---|---|
| 1 | This bible | `Quests/Caelmor_Emberholt_Narrative_Production_Bible.md` | Draft; independently reviewed 2026-11-14 (§13); awaiting Director review |
| 2 | Milestone packages and dialogue | `Quests/Caelmor_Emberholt_Main_Act_I.md` (EH-M1–M3), `_Act_II.md` (EH-M4–M5), `_Act_III.md` (EH-M6) and matching dialogue files | Not started |
| 3 | Side quests, micro-events, discoveries | `Quests/Caelmor_Emberholt_Side_Quests_Unburnt_and_Names.md` (EST, ETB, EMS, ENW, EGT); `…_Side_Quests_Commons_and_Wards.md` (EWA, ECN, EFC, EBL, ESR); `…_Side_Quests_Work_and_Skills.md` (ESK, EOM, EFS, EWQ, ESP, ESH); `…_Side_Quests_Combat_and_Discovery.md` (EOP, EFD, EAD, ECC, EME01–EME10, EDS01–EDS10) | Not started |
| 4 | Encounters, POIs, integration | Enemies, Zones and Integration packages | Not started |
| 5 | Independent review and fix pass | Revisions in place | Not started |

**Authoring order** (Review §7): R09 and its custodians first (EH-M3), then the capstone (EH-M6), then EH-M4 and EH-M5 once D-E2 and D-S1 are ruled or the tagged layers are accepted, then EH-M1 and EH-M2; then seeds; then series; then the self-contained slate; then micro-events and discoveries; then review.

**Production dependencies (not narrative work):** quest, dialogue and NPC schemas (Roadmap 31.2/31.3/31.5), zone and encounter data, an Emberholt map pass, and the economy pass. Nothing here waits on them; nothing here implements them.

---

## 13. Internal review log

**Status: draft (2026-11-14); independently reviewed 2026-11-14 (log below). Still in review; nothing is approved.**

| Check | Result |
|---|---|
| Architecture fit | Six milestones match Arcs in name, order and flag (`EH_COLD_WARD`, `EH_CURRICULUM`, `EH_HOLLOW_TRUTH`, `EH_THALAN`, `EH_SPEAKER`, `EH_HEAT_MAIN`, `EH_ACCOUNT`, `EH_STANDING`). R09–R12 owned; R15, R16, R18, R19 seeded, not revealed. |
| Rulings | CDR-1: all enemies to 0 HP; no SX. CDR-2: ranged viable everywhere, never required. CDR-3: milestone language only. CDR-4: §11.1. CDR-6: every quest solo. FT-04, FT-05 (direction), FT-02, D-C03, D-C06, D-CV1 respected. |
| Open items respected | D-E2, D-S1 written around and tagged; no "invaders"; origin-neutral; C07 untouched. |
| Counts | 28 POIs; 20 side quests (16 self-contained); 10 micro-events; 10 discoveries; 9 families, 22 variants; 1 boss, 2 minibosses; 5 quest items. |

**Source contradictions found (for the reviewer and the Director):**

1. Arcs EH-M1 calls Yorven Khelt "a [NEW] fire warden"; Factions makes him a canon District Overseer. Followed canon; the blamed warden is Veska Dunmor [NEW].
2. Cinderwall is absent from the dossier's district list but named in Factions and the Arcs. Used as a ward (§4.1).
3. The dossier's non-lethal containment of Ember-Fused Workers conflicts with CDR-1 if they are enemies. Resolved by ED-2.
4. The dossier's "end their suffering" option for Thalan conflicts with Review contradiction 7. Excluded.
5. Canon places Perfect Flame's city-wide ignition in Emberholt's capstone; FT-04 moves the payoff to CV-M4. Followed FT-04.
6. D-C03's earlier note that the precursor name would be "chosen in the Emberholt bible" is superseded by D-C03 (no name). The roll's heading is cut away.
7. Arcs EH-M4 asks for "infiltration" and "heat-pressure traps"; CDR-4 rules out stealth. Resolved by ED-6.
8. Serix Arden's canon visions "centred on the player" conflict with origin neutrality. Not used (ED-17).
9. Canon has Darven's crew as miners; Arcs says "Deepbrand lost a crew". Resolved as a contract crew hired by Deepbrand.
10. The dossier and Timeline call Lowmark "the sole full v1 region"; CDR-3 supersedes. Not used.
11. **For the Director (ED-20).** The Arcs §3.3 entry text says no quest prerequisite for EH-M1 and EH-M2; the Arcs §6 graph shows a solid E1 → E2 hard prerequisite. Followed the graph. The stand-alone principle (entry milestone without prerequisite; no other region needed before EH-M3) holds either way. The Arcs file should be corrected to match the ruling.
12. Varos Keln's "execution" hook and the Thalan anchor's "exploiting his power" option are unused.
13. Canon makes Theryn Dalewright a covert Remnant recruiter; the Arcs ask EH-M2 to reveal conditioning "without condemning teachers". Resolved by showing her stewardship and her one act of resistance, never exposing or punishing her in Emberholt, and keeping the other teachers outside it. Her later choice of loyalties is left to later content.

**Review log**

| Pass | Result |
|---|---|
| Independent review, 2026-11-14 | Re-read against the binding rulings (CDR-1 to CDR-6, §3.7, §4 register), the approved architecture (Arcs, Revelation Ledger, Review §5.0 and §7.1), the Emberholt dossier, Factions, Timeline, War History and the Part 4 character ledger; every new name, place and code grepped across `04_CONTENT_PRODUCTION`, `LORE` and `00_ADMIN`. **Renames (collisions or near-duplicates):** Tamsa Orrel → **Veska Dunmor** (Tamsin in Lowmark and Thornfell, already removed from the Mire; Orrel/Oriel); Elbet Raine → **Idra Callow** (Mire Elspet Rye); Pell Ardane → **Sarne Ardane** (Lowmark Tovin Pell, Thornfell Pell Kvist); Brisa Hale → **Brisa Teglan** (Lowmark Watchers Hale & Pim; Wenna Hale already renamed); Ama Tolk → **Hesper Tolk** (Thornfell Ama Kvist); Corm and Lissel Abbet → **Corm and Imra Brask** (Lissel/Lessa/Lysa; Abbet/Mire Abner); Nim Ostry → **Tavi Ostry** (Lowmark Pim); Dovan Krell → **Breck Krell** (Darven Mott in the same cast). Codes ECW–ESR, EP, EME, EDS and EI ids are unique. **Fixed, medium:** §1 revealed in EH-M3 that Thalan is still alive (R10 is EH-M4's): now past tense only; R09's guaranteed path lacked the ledger's site evidence: the EH-M3 circle (S06) is now a required custodian; ENW asked the player to "find" Corm while also recording him "not found", and treated the Mire's unnamed MDS09 entry as an identity hold that implied a journey between regions: Corm is now never met, proved walked-out by the Emberholt pay list, and MDS09 is an optional unconfirmed echo (ED-16 ●; the Mire gains no requirement); ECC attributed the timetables to the Remnant in play and matched a Lowmark hand to Oren Falx's papers: now unattributed, flavour only, no route (ED-15; Part 4 ledger Oren row); the Ash Roads were reinvented as wartime supply roads: restored to canon streets with burnt engravings and the R09 Volkhari-symbol seed (EP09, EDS01); §4 called Embergate the only way out while the Ridge used a second gate; the EH-M1/EH-M2 entry conflict is now ED-20 ● for the Director. **Fixed, low:** Darven's variant lines no longer give him knowledge of other regions; Thalan's R19 limit added; `[D-S1]` added to EH-M5 S04; step references in ED-3, ED-14, §3.1 and §3.2 corrected; Deepbrand's "sanctioned contractor" and the Forge Saboteurs' EOM framing labelled [NEW] beside canon; §7 notes six side quests wait on the EH-M3 gate; file-map names completed; status lines updated. **Verified unchanged:** every enemy to 0 HP, no yield, retreat or break-off, no SX; the Speaker, Theryn, Volkhari, Ember-Fused workers, children and officials never fight and are never targetable; ranged viable everywhere and required nowhere; no release wording; no meter, stealth or detection system; every quest, boss and reward solo; FT-02, FT-04, FT-05, D-C03, D-C06 kept; D-E2, D-S1, the "invaders" wording, D-3 and C07 not decided and tagged; flags have one writer each and every side-quest unlock is reachable. **Left open:** "the Undercroft" shares a generic noun with Lowmark's Records Undercroft (kept, always qualified as Cinderwall's in tables); letters addressed to "the Seat" echo Selvara's title without naming her. |
