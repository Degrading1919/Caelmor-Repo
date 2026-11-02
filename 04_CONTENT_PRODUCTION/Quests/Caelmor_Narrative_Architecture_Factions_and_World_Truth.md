# Caelmor Narrative Architecture — Factions and World Truth

**Status (updated 2026-11-02):** Part of the narrative architecture package indexed in `Caelmor_Narrative_Architecture.md`, now the controlling plan after the Creative Director's rulings (Review §5.0). This file covers **deliverable 1** (faction histories, relationships, and long-term motivations) and **deliverable 2** (the consolidated historical-event and world-truth framework). Rows marked **[APPROVED]** were ruled on and promoted into `LORE/` by the controlled canon pass (Review §5.3); every other proposal stays a proposal. It creates no schemas, JSON, or C#.

## Status labels used in this file

| Label | Meaning |
|---|---|
| **[CANON]** | Stated in the reconciled live sources: Phase 1.1–1.5, `LORE/Timeline`, `LORE/Worldbuilding Docs/Caelmor_War_History.md`, `LORE/Factions`, the four detailed regional dossiers, the merged overview, and the character anchor files. |
| **[CANON-OPEN]** | Canon explicitly leaves this unresolved (for example C03 precursor name and transition, C06 Volkhari population, C07 Founder roster). The architecture works around it and does not settle it. |
| **[V1-AUTHORED]** | Authored in the Lowmark v1 production package (marked [NEW] there). Built content, not canon until promoted. |
| **[PROPOSAL]** | An ordinary structural or creative choice made by this package under Master Protocol §5.6. Reversible; does not change locked facts. |
| **[APPROVED — FT-nn / D-…]** | A foundational truth or decision the Creative Director ruled on 2026-11-02 (Review §5.0) and the canon pass promoted. Where a ruling approved only a direction, the row says what stays open. |
| **[FOUNDATIONAL — DIRECTOR]** | A new truth about history, causation, or a major faction that would change how the world is understood. Requires explicit Creative Director approval. Each has an id (FT-nn) and is listed with a recommendation in `Caelmor_Narrative_Architecture_Review_and_Authoring_Sequence.md` §5. |

Public beliefs are labelled as beliefs. A belief is never author truth unless a row says so.

---

## Part A — The world truth in one page

**What actually happened (author truth, condensed).** Caelmor's four regions grew interdependent through food, passage, shelter, labor, and trade long before learned magic [CANON]. Regional elemental traditions were rediscovered and later taught by distinct figures remembered as Founders [CANON; roster CANON-OPEN]. Interdependence created obligations without any shared authority to inspect or restrain another region's dangerous practice [CANON]. The prewar attempt to manage that gap by custom, the **Crossing Concord**, an informal custom of mutual witness and never a government, failed on the Road to War [APPROVED — FT-01]. A 5–10-year Great War followed, ending about thirty years ago [CANON]. It did not end in a treaty. It wore out: exhaustion, hunger, desertion, and local truces did most of the work over its last years, and inside that collapse each region made one withdrawal, at a different time and for its own reasons, some feeding others. Thornfell's forced resonance had already collapsed Shatterfall Gorge onto its own people, and over the last years the Assembly sealed the passes one by one (earliest and slowest); Lowmark's river crews began refusing flushes and night convoys after a relief convoy was drowned by a supply flush, and the refusal spread over a season or more; the precursor's war-ending gamble at the Glassed Hollow destroyed Emberholt's capacity to continue in a night; and the Mire's last Memorywardens grounded the last great battle and were broken by it. Raids went on for a time after [APPROVED — FT-02]. Each region's public history credits itself with ending the war and hides its own cost. **Nobody made the peace.** Thirty years later, the same pressures that started the war (scarcity, hoarding, closure, concealed experiment, and the refusal to accept another region's witness) are returning, and a patient hidden faction, the formal Remnant, is ready to exploit them [CANON core; FT-01, FT-02, FT-04 for the specific shape].

**What the player discovers, in order of experience.** First, that Lowmark's water is going wrong because of one local house's greed and an old broken work (Lowmark v1, complete). Then, region by region, that every community's proudest war story is partly a cover for something it did or failed to do, and that each region holds one honest piece of the end of the war. Finally, that the peace they live in was never agreed, and that making it is now possible only because the player has earned standing in each place and can carry evidence each community will accept.

**Why this is not one conspiracy.** Each region's present crisis has a local human cause that would exist without the Remnant: House Marrick's profiteering, a Thornfell faction's fear-driven rearmament, a Mire community's unresolved care and testimony, and Emberholt's class-shaped civic order. The Remnant is causally central only in Emberholt and in the convergence, where its specific operations are discoverable and bounded. What connects the regions is a shared structural wound, not a shared villain.

---

## Part B — Consolidated historical-event and world-truth framework

### B.1 Historical chronology (author truth)

Relative order only. Ancient dates remain uncertain [CANON]. War-year labels are relative ("late war", "final year") so the optional seven-year campaign spine in Part 2 is neither adopted nor contradicted.

| # | Era | Event | Historical truth | Status | Public belief(s) | Evidence custodians | Owning arc |
|---|---|---|---|---|---|---|---|
| H01 | Mythic Age | The Forgotten God walks the living world | Direct communion with the divine; no learned elemental magic. | [CANON] | Faith, custom, superstition. | None reliable. | **Long Horizon; never resolved** [PROPOSAL design rule] |
| H02 | Mythic Age | The Stonebound are made beneath what becomes Emberholt | Passive, place-bound works maintaining deep balance, pressure, volcanic harmony. Makers unknown. | [CANON]; makers [CANON-OPEN] | Guardians, judges, buried creatures. | Physical works only; they never testify. | Thornfell (Summit node), Emberholt (deep works), Long Horizon |
| H03 | Mythic Age | The Volkhari arise near the volcanic ridges | Inherited fire attunement distinct from learned embercraft. | [CANON] | Dragonkin myth; extinct. | Volkhari memory-stones and oral history (Seredh Embercarver). | Emberholt |
| H04 | Quiet Withdrawal | Divine contact fades; regional knowledge develops; regions become interdependent | Passage, subsistence, labor, refuge, and exchange connect regions. | [CANON] | Each region thinks it was self-sufficient. | Practical remains: channels, shelters, hazard marks. | Background for all |
| H05 | Rediscovery | Four elemental traditions emerge; rediscoverers then later Founders | Riverwardens (water, Lowmark), Echohewn (air resonance and acoustic engineering, Thornfell), Memorywardens (earth-memory, Mire), Emberholt fire tradition beside Volkhari inheritance. | [CANON]; roster [CANON-OPEN C07] | One heroic Founder per element. | Riverwarden tablets; Echohewn halls; Memorywarden shards and anchor circles; Red-Lit restricted archives. | Each region; optional late history line |
| H06 | Rediscovery | The Riverwardens tune Lowmark's floods with the Braids and Marking Stones | Distributed flood-tuning network. | [V1-AUTHORED] | Flood Calendar Stones are old luck. | Marking Stones; the Listening Steps flow-table. | Lowmark (done) |
| H07 | Road to War | **The Crossing Concord** | A prewar custom by which the four regions hosted one another's witnesses at major crossings and passes to inspect dangerous practice and settle duties of passage. It had no army and no court: only access, testimony, and the shame of refusal. | **[APPROVED — FT-01]** (informal custom, not a government) | Forgotten; survives as a few customs (a crossing oath, horn calls for "witness at the gate", a Mire hearing form). | Lowmark crossing rolls (Fenmere ledgers older than the war, [CANON] that they exist); Thornfell horn rosters; Mire testimony forms; Emberholt inspection gaps (Part 4 event 5). | Convergence |
| H08 | Road to War | The Concord fails | Emberholt refuses inspection of concealed experiments; Thornfell closes passes to force the issue and strands civilians; Lowmark's houses demand floods on command for leverage and the Riverwardens withdraw rather than comply; Mire witnesses are ignored. Each refusal has a defensible local reason. | [CANON] pattern; Concord failure **[APPROVED — FT-01]**; each region's specific refusal [PROPOSAL until its arc]; Riverwarden withdrawal cause consistent with Oriel's v1 line [V1-AUTHORED] | Each region blames another region. | Same as H07, plus Oriel's account. | Convergence (with Lowmark echo) |
| H09 | Road to War | The wartime precursor forms and exploits the failures | Name and transition unresolved; limited personnel continuity. | [CANON]; continuity [APPROVED — D-C03]; name, transition, survivors [CANON-OPEN] | "The Remnant started the war." (false) | Red-Lit restricted archive; Emberguard records. | Emberholt, Convergence |
| H10 | Great War | Lowmark becomes the contested breadbasket; the Relief Cut and Hollow Lock are dug through the Braids | Wartime engineers (canon: dwarven engineers fortified mills and bridges) cut the Cut to run grain fast. House Fenmere compacts move food to several sides. | Breadbasket [CANON]; Cut [V1-AUTHORED]; several sides [CANON: Fenmere records document river movements that fed armies on several sides] | "Lowmark fed the war but stayed clean." | Fenmere ledgers; Bramblelock convoy stones; Thornfell engineering work logs [PROPOSAL]. | Lowmark (done) and Lowmark return arc |
| H11 | Great War | Thornfell's passes become barriers; rare resonance is forced into weapons | Horns with resonance plates, pressure pockets, masked echoes. | [CANON] | "Lucky weather"; "the horn that split the ridge" is exaggeration. | Horn plates, Shatterfall resonance scar, Ressa's forbidden calls, Dorn's altered echoes. | Thornfell |
| H12 | Great War | The Mire becomes the central battlefield; Memorywardens are conscripted | Earth-memory pressed into battlefield service; imprint accumulates. | [CANON] | "The war sank here." | Drowned trenches; Memorywarden shards; Sennic's childhood stories. | Mire |
| H13 | Great War | Emberholt weaponizes fire practice | Battle embercraft, amplification conduits, siege engines. | [CANON] | "Emberholt only defended itself." / "Emberholt caused everything." (both partial) | Molten scars; restricted archives. | Emberholt |
| H14 | Late war | **The Fourteenth Lot** | A flush is released while a relief convoy is still in Stillwater Fen; the convoy sinks with its crews; the loss is hushed up. The order-giver is not identified in v1. | [V1-AUTHORED] | Unknown in public; Bramblelock stone missing an entry. | Bramblelock stones; Corvin's burned ledger (unrecoverable [V1-AUTHORED]); a second custodian outside Lowmark needed for the order. | Lowmark return arc |
| H15 | Late war (second, over a season or more) | **Lowmark's stop** | After the Fourteenth Lot, Relief Cut and river crews begin refusing flushes and night convoys. The refusal spreads unevenly: some crews hold out for months, some houses keep running grain by road at road speed. Supply to every front thins. Lowmark's houses later recast it as "orderly armistice provisioning". | **[APPROVED — FT-02a]** (the convoy loss and the crews' refusal; the order-giver stays open) | "Lowmark kept every front fed until the armistice." | Crew songs (the missing verse in *A Verse Kept Back* is compatible but not required); Fenmere ledgers showing the uneven drop; Thornfell receiving records. | Lowmark return arc |
| H16 | Late war (earliest and slowest) | **Thornfell's stop** | Thornfell's forced resonance horns had already brought down passes onto attackers and its own people; Shatterfall Gorge is the remembered instance. Over the war's last years the Assembly pulled its forces home and sealed the high passes one by one, behind horn-made collapses and closures. Refugees on the wrong side were stranded; some reached the Mire. The sealings closed overland routes and put more weight on Lowmark's river convoys. Thornfell never speaks of its own dead at Shatterfall. (Fits the optional Part 2 spine, where Shatterfall falls in Year 2.) | **[APPROVED — FT-02b]**; gorge collapse and resonance scar [CANON]; who blew the horn and casualty counts open | "The horn that split the ridge" saved Thornfell; or it never happened; "Thornfell held the wall." | Shatterfall horn plates and scar; horn rosters; closure dates cut into the sealing works; cairn names (Maera); Mire care records of arrivals (Part 4 braid 8). | Thornfell |
| H17 | Final year (the last great battle) | **The Mire's stop** | As the war comes apart, retreating columns from more than one front and their pursuers collide on the Field of Fallen Standards in a battle neither side can win or needs. The last Memorywardens attempt a mass grounding (a "calm-field", canon technique) to make the armies unable to keep fighting. Fighting in the Mire stops. The overload kills most of them and concentrates command, fear, and obedience into the coherent imprint later called the General Who Wouldn't Fall. Survivors abandon the practice. | **[APPROVED — FT-02c]**; General's nature and Memorywarden downfall [CANON] | "The ground swallowed the armies." "The Lantern That Would Not Go Out was a Memorywarden's final act." (Folklore that is near the truth.) | Memorywarden record beneath the Sunken Chapel altar (rumored relic [CANON] rumor); anchor circles (the Turning Stone); Sennic's memories; regimental logs. | Mire |
| H18 | Final year (sudden) | **Emberholt's stop: the Glassed Hollow** | Hungry and cut off by sealed passes and slowing grain, the precursor gambles on an amplification ritual using Volkhari knowledge and captives to end the war fast in Emberholt's favor. A precursor initiate became the Fire Titan; the lower works glassed; Kaelith escaped; Thalan was seized later, in the purges that followed [CANON]. Emberholt lost its offensive capacity in a night, and its civic leaders stopped. Public record: forge collapse. | Core [CANON]; "intended as war-ending" and "proximate end of Emberholt's war" **[APPROVED — FT-02d]** | "A forge collapse." "Emberholt chose peace and discipline." | Glassed Hollow site; restricted archives; Volkhari testimony; Mire care of displaced civilians (Part 4 event 6). | Emberholt |
| H19 | The Stopping | The war wears out without victory or treaty | The war did not end on a day. Exhaustion, hunger, sickness, desertion, and broken supply did most of the work; local truces and unofficial prisoner exchanges spread from front to front; raids and skirmishes went on for some time after the last great battle. Inside that ragged collapse, the four withdrawals above happened at different times, for their own reasons, and some fed one another: sealed passes put weight on the river convoys, and thinning grain and closed routes pushed Emberholt toward its gamble. Fractured command and magical escalation [CANON, War History §VI] did the rest. The Fourteenth Lot had its own cause, and the Mire's last battle was not any one region's doing. None was coordinated, and nobody signed anything. Part 2's "the Stopping" and "Cessation without settlement" name this stretch. | War ended without victory [CANON]; "withdrawals, no treaty" **[APPROVED — FT-02]** | "There was an armistice." Each region believes its own stop ended the war and that the others agreed to something. | All of H15–H18 together, plus ordinary records of hunger, desertion, and local truces. No single custodian holds the whole. | **Convergence** |
| H20 | Postwar | Regional restraint; no universal ban | Each region restricts weaponization, amplification, uncontrolled ritual, dangerous research in its own way. | [CANON] | "Magic was outlawed." | Regional decrees and customs. | All |
| H21 | Postwar | Dreamers appear | Fragments may be true and misread; Hearthveil can seed visions. | [CANON] | Prophecy; curse; the dead speaking. | Independent corroboration only. | Emberholt; optional personal stories everywhere |
| H22 | Postwar | The formal Remnant forms beneath Emberholt; the Flameward Speaker rises | The Remnant shapes public embercraft into mass conditioning; advanced practice stays restricted. The Speaker rises on a promise of discipline. | [CANON]; continuity [CANON-OPEN C03] | "Safe embercraft." | Curriculum records; Hearthveil chambers; Speaker correspondence. | Emberholt |
| H23 | Recovery | Thirty years of uneven recovery | Repair, migration, fosterage, debt, grudges, disputed credit. | [CANON] | Each region thinks it carried the others. | Household and institutional records everywhere. | All |
| H24 | Present | Lowmark's water goes wrong | House Marrick reopens the Relief Cut; the fen's grief spreads; the player helps the Vale tend the Braids. | [V1-AUTHORED] | Curses; smugglers; the Field-Mage. | v1 evidence chips. | Lowmark v1 (complete) |
| H25 | Present | **The Second Road begins** | Hoarding (a Thornfell faction's unsanctioned war stores, partly bought with Lowmark relief grain), Emberguard civic-reserve drills, pass closures, and Remnant probing reproduce the prewar pattern. The Sorrowback stirs in the Mire because it is drawn to violent conflict [CANON trait]. | **[APPROVED — FT-03 (buyer, no route invented) and FT-04 (Perfect Flame definition)]**; Emberguard drills and Remnant probing [PROPOSAL] | "Emberholt is arming." "Thornfell is arming." Both partly true. | Bills of lading, store inventories, drill orders, Sorrowback sightings. | Thornfell, Emberholt, Convergence |

### B.2 What remains unresolved, and how the architecture treats it

| Item | Status | Architecture treatment |
|---|---|---|
| C03 precursor name, transition, personnel continuity | Limited personnel continuity [APPROVED — D-C03]; name, transition and survivor identities [CANON-OPEN] | Content uses "the precursor". No approved precursor name and no extensive surviving roster may be invented; a named survivor needs a separate ruling. |
| C06 Volkhari population and community form | Kept unnumbered and unresolved [APPROVED — D-C06] | Emberholt arc depicts individuals and protected testimony only. No enclave reveal, census, or settlement map. |
| C07 Founder roster and teaching links | [CANON-OPEN] | Every region keeps its own simplified origin tale as belief. An optional late history storyline (Long Horizon) may refine them after a ruling. |
| Forgotten God | Withheld by design [PROPOSAL] | Never met, never explained, never a boss. Present only in faith, ruins, and the question of what the Stonebound were made to keep. |
| Echohewn disappearance | Withheld by design [CANON rule: "never fully explained"] | Fragments only. |
| Origin of "Sinking Star" | [CANON] unasserted | No milestone explains the name. |
| Who gave the Fourteenth Lot order | Withheld in v1 [V1-AUTHORED] | Lowmark return arc identifies the **office** (the wartime supply command and the Fenmere compact under which it acted) through two custodians. Whether a named person is identified is left to that arc's authoring and the Part 4 character ledger. |
| Map geometry, routes, travel times | Deferred [CANON] | Relative placement only; every placed journey needs the Part 4 map audit. |
| Lowmark's ruling-family question | [CANON] open political tension | Remains open after v1. Marrick's exposure weakens one claimant, not the question. |
| Exact constitutional powers and offices in all regions | Deferred [CANON] | Milestones use neutral roles (Assembly, Board, Council, hearing). |

### B.3 Rules that bind the world truth

1. **Several causes, never one.** Every historical turning point keeps human decisions, damaged infrastructure or institutions, and (where present) bounded resonance as separate causes. The precursor or Remnant may exploit a turning point without causing it [CANON principle].
2. **Two custodians.** No revelation in this package is earned from a single record, a single witness, or any supernatural phenomenon. Each requires two differently situated human or material sources [CANON control D04/D06].
3. **Local truth stands.** A later revelation can add responsibility or context to an earlier region's resolution. It can never make the player's earlier help meaningless [Part 5 control].
4. **No witness phenomena.** Wraiths, earth-memory, the General, the Sorrowback, Stonebound responses, horn-echoes, Cinder Wraiths and dreams can prompt inquiry and create danger. They never identify, testify, or settle anything [CANON].
5. **Beliefs are content.** Every public belief listed above is something an NPC may say sincerely. Writers attribute it; they never narrate it as fact.

---

## Part C — Faction dossiers

Each dossier covers history, objectives, leadership, internal disagreements, allies, adversaries, secrets, and long-term narrative role. Names and facts come from the live sources unless labelled. No faction reputation system is implied (Phase 1.1 §8); "allies" and "adversaries" describe story relationships.

### C.1 The Remnant (and the wartime precursor)

| Field | Content |
|---|---|
| **History** | An unnamed wartime precursor exploited the Road to War and conducted the Glassed Hollow ritual [CANON]. The formal Remnant followed after the war, based in the Ashfall Depths beneath Emberholt [CANON]; **limited personnel continuity** between the two [APPROVED — D-C03]; the precursor's name, the transition, and who survived into the Remnant [CANON-OPEN]. It rebuilt the fire tradition into civic embercraft and shaped curricula, ceremonies, and civic dreams toward a forge-ready population [CANON]. |
| **Objectives** | A continent where fire practice is universal but true mastery belongs to the Remnant [CANON]. Present plan: **Perfect Flame**, defined here as a reliable, transmissible method of advanced embercraft that does not break its user, built from Thalan's attunement, ember-vein conduction, and the conditioned emotional state of a trained population [CANON elements; definition **APPROVED — FT-04**: advanced embercraft made reproducible through conditioning and controlled knowledge]. Its failure mode is a second Glassed Hollow at district scale, including the breaking of the Fire Titan's degrading bindings. |
| **Leadership** | Ashfall Authority: Matriarch Selvara Cael'Thalos (High Seat), Lord Varyn Durell (interregional strategy), Lady Meryndis Kael'Vorra (forbidden rites); Deepbrand under Dreadbrand Varos Keln; Red-Lit Scribes (Archivist Marenya Silvertide, Scribe-Magus Ilverin Qael); Hearthveil Initiates (Vision-Mother Calynne Vorr, Initiate-Lumen Serix Arden) [CANON]. |
| **Internal disagreements** | [PROPOSAL] Three temperaments create the faction's eventual fracture: **Selvara** is patient and civic, willing to wait a generation for the population to be ready; **Meryndis** wants a ritual breakthrough now and studies the Fire Titan, which she helps keep bound, as a template; **Durell** believes Emberholt alone cannot hold mastery unless the other regions are kept divided and afraid. Deepbrand fears the Titan's re-emergence [CANON] and resents being the arm that "retrieves what's left". Red-Lit Scribes maintain dual archives [CANON]; at least one scribe keeps what should have been destroyed. |
| **Allies** | The Flameward Speaker (knowing ally, see C.2 and Review §2 contradiction 2); some merchant houses as fronts [CANON]; Remnant-aligned Emberguard officers [CANON]. |
| **Adversaries** | Volkhari survivors [CANON]; Cinderwall syndicates and the Cinder Rat [CANON]; forgeguilds that resent interference [CANON]; traditional civic guards [CANON]; later, the convergence coalition the player helps assemble. |
| **Secrets** | Thalan Veyr held in ritual chambers [CANON]; the Glassed Hollow truth [CANON]; Hearthveil dream-seeding of Emberholt civic leaders [CANON]; the Fire Titan bound beneath Emberholt by degrading bindings that Meryndis refined [CANON] (its nature and fate: **FT-05**); the precursor's continuity (C03); Durell's bounded operations outside Emberholt (below). |
| **Bounded reach outside Emberholt** [PROPOSAL] | Durell's operations are specific and discoverable: buying information from Lowmark smugglers (Factions: Shadeweavers "sometimes feed information into Remnant channels unwillingly" [CANON]), seeding rumors of Thornfell rearmament in Emberholt and of Emberholt rearmament in Thornfell, and repeating Hearthveil-shaped visions through Emberholt delegates and traders who travel (Hearthveil's own seeding stays inside Emberholt; any direct reach beyond it is part of **FT-04** for the Director). The Remnant does **not** cause House Marrick's scheme, the Thornfell war stores, the Mire's grief, or the Lowmark drift. It exploits them in the convergence. |
| **Long-term narrative role** | Emberholt's hidden antagonist and the convergence's active threat. Its defeat is not the end of embercraft: public civic fire practice remains legitimate [CANON]. The Remnant ends as a broken faction whose surviving knowledge must be placed under the new peace, not erased. |

### C.2 Emberholt civic order

Covers the Flameward Speaker and Civic Council, the Emberguard Legions, the Ember-Seared Covenant, the Forgeguilds and Emberforged, the Cindermind scholars, the Merchant Houses, and the Cinderwall syndicates.

| Field | Content |
|---|---|
| **History** | Emberholt was both architect and victim of wartime devastation [CANON]. After the Glassed Hollow it doubled down on fire-control doctrine; the Speaker rose promising discipline; schools began teaching "safe embercraft" [CANON]. |
| **Objectives** | Public: useful heat, craft dignity, public safety, civic pride, industrial progress [CANON]. Hidden (Speaker and Remnant-aligned officers): a disciplined population ready to project fire at scale [CANON]. Ordinary citizens want warmth, work, safety, and to stop being blamed for the war. |
| **Leadership** | The male Flameward Speaker; Magister Vael Trossen, Magistrix Ralenne Kharveil, Trade Commissioner Oren Falx, District Overseers such as Yorven Khelt; Grand Marshal Kaevren Thalos; Ember-Priestess Seralynd Hearthveil; Forge-Master Durnan Volkryst and Selice Morra; Merchant-Lord Eraven Cyl; Dalia Vret of the Embervein Traffickers; the Cinder Rat [CANON]. |
| **Internal disagreements** | Traditional civic guards versus Remnant-aligned officers inside the Emberguard [CANON]; Covenant branches shifted by Hearthveil versus orthodox fire-as-memory practice [CANON]; forgeguilds resent Remnant interference and guard pre-war forging fragments [CANON]; merchant houses split between fronts and fearful resisters [CANON]; Cinderwall districts distrust all elites [CANON]. |
| **Allies** | Lowmark grain and river trade (dependence, not friendship) [CANON]; Thornfell stoneworkers respect the Emberforged [CANON]. |
| **Adversaries** | Thornfell's Blood-Oath clans [CANON]; the Mire's memory of fire devastation [CANON]. Internally, Cinderwall syndicates. |
| **Secrets** | Accidents redirected into "training reports"; fire-control exams double as compatibility assessments; some ceremonies were designed as mass emotional testing [CANON]. Emberholt does stockpile food as dense-city civic policy, which outsiders read as war preparation [PROPOSAL]. |
| **Long-term narrative role** | The region where the most good and the most harm sit side by side. Its arc must give the player sincere civic competence to respect (fire wardens, teachers, guild workers) before it reveals the hidden face. In the convergence, Emberholt's ordinary citizens are the decisive actors: Perfect Flame needs their conditioned emotion, and their refusal is what breaks it (**FT-04**). |

### C.3 Volkhari survivors

| Field | Content |
|---|---|
| **History** | An ancient fire-attuned people near the volcanic ridges [CANON]. Devastated and dispersed by the Glassed Hollow; Kaelith Veyr'un escaped and remains free; Thalan Veyr is the sole known current captive [CANON]. |
| **Objectives** | Survival; prevent another catastrophe; avoid Emberholt; observe the Remnant without intervening unless forced [CANON]. |
| **Leadership** | No political form is established [CANON-OPEN C06]. Known or reported individuals: Matron Vaelyra (elder; "Vaelyra of the Cooling Flame" in the character file), Seredh Embercarver (historian), Asera of the Three Breaths (ritualist, teacher of emotional fire control), Thennek Vorren (guardian), Maeryn Vall (hidden in Emberholt), Dahrin Vosk (fugitive), Ilyen, Kaelen, and Kaelith Veyr'un [CANON]. |
| **Internal disagreements** | [PROPOSAL] Whether to act for Thalan at the risk of exposing everyone else; whether to share Asera's discipline with outsiders (it is the one method that could make advanced fire practice safe, which is exactly what the Remnant wants). |
| **Allies** | None reliably; possibly individual Emberholt citizens (Maeryn Vall's neighbours) and, through earned trust, the player. |
| **Adversaries** | The Remnant [CANON]. |
| **Secrets** | Their number and form (C06); Asera's discipline; the "Volkhari Oathbinder" story of fire bound without emotion [CANON legend], which the Remnant seeks [CANON]. |
| **Long-term narrative role** | Witnesses, not plot keys. Their testimony is protected; Kaelith is never "rescued" [CANON] and never chosen. Thalan's fate is a Director decision (Review §5, D-E2). In the convergence, Asera's discipline is offered, not taken, and only if the player's earlier choices showed restraint [PROPOSAL]. |

### C.4 Lowmark powers

Covers House Fenmere and the stewardship, competing houses (House Marrick [V1-AUTHORED]), the Provision Board [V1-AUTHORED], the Crestbridge Keepers, village councils, river crews, Wraithwatchers, Flow-Menders, Glasswrights, Watergarden Keepers, the Lensemasters, the Shadeweavers, the Riverwardens, and the Last Field-Mage.

| Field | Content |
|---|---|
| **History** | Breadbasket and transport artery of the war; refused large-scale water warcraft [CANON]. Fenmere compacts moved food to several sides [CANON]. Postwar, competing houses each claim they "kept Lowmark alive" [CANON]. |
| **Objectives** | Reliable food and movement; deciding who pays for repair and whose record counts [CANON]. After v1, tending the Braids together under the public plan [V1-AUTHORED]. |
| **Leadership** | Steward Aldric Fenmere; Keeper-Captain Bram Hesketh [V1]; Provisioner Edda Marrick [V1, `[ANTAGONIST]`]; Maelin Rowe (crews); Corvin Tath (granaries); Lessa Mirepath (fen guide); Oriel (Riverwarden) [V1]; Sedge (Last Field-Mage) [V1] [CANON names where not marked]. Shadeweavers and Lensemasters have no named leaders [CANON]. |
| **Internal disagreements** | Which family should rule [CANON]; commons roll versus household practice [CANON C09; v1 MQ7]; whether the Fourteenth Lot should be spoken of; whether Lowmark's neutrality was moral or merely profitable. |
| **Allies** | Thornfell trade [CANON]; the Mire through shared grief [CANON]. |
| **Adversaries** | None by region; distrust of Emberholt ambition [CANON]. |
| **Secrets** | Fenmere ledgers prove food went to several sides [CANON]; the Fourteenth Lot [V1]; Lowmark's stop (**FT-02a**); the Riverwardens withdrew partly because Lowmark houses demanded floods on command (Oriel's v1 line, interpreted) [V1-AUTHORED / PROPOSAL]. |
| **Long-term narrative role** | Lowmark is the **hinge** [CANON: "moral and logistical hinge between more extreme regions"]. It gives the player the first tool of the peace, **tending held by many hands with no single owner** (v1's Braid plan), and it carries the first account to the convergence. Its own reckoning, that it fed every side and hushed the Fourteenth Lot, comes after the player has seen other regions' hidden costs, so it lands as recognition rather than accusation. |

### C.5 Thornfell powers

Covers the Stonewake Assembly, Blood-Oath clans, Hearthguard clans, the Old Stone traditionalists, Ridge Wardens and the ridge-patrol Cliffward Sentinels, Hornbearers, Cairn-Keepers, Bridgewrights, and dwarven custodians.

| Field | Content |
|---|---|
| **History** | The raised shield of the war; passes as barriers and shelters; forced resonance now denied or forgotten [CANON]. Clans fractured over wartime strategy [CANON]. |
| **Objectives** | Pass safety, shelter, repair, collective survival [CANON]. The open question: prepare for war with Emberholt or accept peace [CANON]. |
| **Leadership** | Hadrik Stonewake (Assembly Speaker), Brynjar Korr (Blood-Oath voice), Elira Hearthward (Hearthguard voice), Old Torvek (Old Stone), Kaldren Deepdelver (dwarven custodian), Ressa Highcrag (High Ridge Warden), Dorn Feldhorn (Hornbearer), Maera Cairnwatch (Cairn-Keeper), Iven Ridgeborne (scout) [CANON]. |
| **Internal disagreements** | Blood-Oath readiness versus Hearthguard recovery [CANON]; tradition versus change [CANON]; [PROPOSAL] a Blood-Oath splinter that acts without the Assembly: it keeps unsanctioned war stores (**APPROVED — FT-03**: it acts independently of its clans and the Assembly; the route Lowmark grain took to Thornfell, river, road, or transfer, stays open until the map pass, per the Part 4 map audit and the ruling's instruction not to invent routes) and is trying to rebuild "the horn that split the ridge" from Echohewn horn plates as a deterrent. Brynjar is loud but is **not** made the splinter's leader (Part 4 ledger forbids new deeds for anchors); he must choose whether to defend or disown it. |
| **Allies** | Lowmark trade; respect for the Mire [CANON]. |
| **Adversaries** | Emberholt's ambition [CANON]. |
| **Secrets** | The friendly dead of Shatterfall and the stranded refugees (**FT-02b**); Ressa knows which tones caused wrong results [CANON]; Hadrik chooses where people stand in the hall [CANON]. |
| **Long-term narrative role** | Gives the player the second tool of the peace: **an honest account of who a closure left behind**, and the Assembly's practice of deciding without a ruler. Its arc is the first future region and must stand alone for players who skipped every Lowmark side quest. In the convergence, Thornfell controls whether the passes close again. |

### C.6 Mire communities

Covers Memorykeepers, Chapel-Tenders, Marshwardens, Rootcrafters, Bannerbearers, Misttide Traditions, the Rootshadow Syndicate, and work-group households.

| Field | Content |
|---|---|
| **History** | Central battlefield; Memorywardens conscripted and broken; a culture of honesty, remembrance, and shared burden formed [CANON]. |
| **Objectives** | Keep people safe without turning uncertainty into silence [CANON]; care, testimony, route maintenance, memorial duty [CANON]. |
| **Leadership** | No central office. Informal: Edris Hollowmere (caretaker), Rowan Mirewake (only reliable living guide to the Chapel), Old Sennic Vale (elder), Calwen Reed-Binder, Mara Fenholt, Lysa Thornettle, Bran Hollowstep [CANON]. |
| **Internal disagreements** | Remembrance as care versus remembrance as a claim to authority [CANON]; cleanse or preserve grief sites [CANON]; Rootshadow distrust and fragmentation [CANON]. |
| **Allies** | Lowmark sympathy; Thornfell Ridge Wardens [CANON]. |
| **Adversaries** | Bitter resentment of Emberholt [CANON]. |
| **Secrets** | The Memorywardens' last grounding (**FT-02c**); people in Mire care records who are mourned elsewhere (Part 4 events 2, 4, 6). |
| **Long-term narrative role** | Gives the player the third tool of the peace: **testimony that two custodians can stand behind**, and the discipline of not letting a manifestation speak for the dead. The Mire's register of the unreturned is the cross-region civilian storyline that binds Thornfell, Lowmark, and Emberholt families. In the convergence, the Sorrowback's stirring is the world's alarm bell for the Second Road. |

### C.7 Ancient and spiritual layers

| Layer | Truth | Present presence | Long-term role |
|---|---|---|---|
| **Riverwardens** | Water-attuned people who withdrew behind Veilwater [CANON]; trained the Last Field-Mage [CANON]. | A small remnant; Oriel at the Listening Steps [V1]. | Never return to rule. After v1 they teach Braid tending to many hands; any future player water practice (unapproved system) would be framed through this condition [PROPOSAL]. |
| **Echohewn** | Dwarven-influenced builders; engineering plus rare resonance [CANON]. | Vanished; works and horn plates remain. | Thornfell's mystery; never fully explained [CANON]. |
| **Memorywardens** | Earth-attuned order; perished or suppressed in the war [CANON]. | No living practitioners [PROPOSAL]; Chapel-Tenders keep forms without function [CANON]. | The Mire's tragic heroes (**FT-02c**). Their method survives only as records and anchor circles. |
| **Founders and rediscoverers** | Distinct roles [CANON]; roster open [C07]. | Regional hero tales. | Optional late history line. |
| **Stonebound** | Passive place-bound works [CANON]. | Summit node [CANON]; deep works under Emberholt [CANON]. | They respond to disturbance and never act by choice. They play no part in the Titan's binding; the deep works remain Long Horizon exploration. |
| **The Forgotten God** | Mythic presence that withdrew [CANON]. | None. | Never met (Long Horizon rule). |

### C.8 Relationship matrix (present day, before the player intervenes)

Rows describe how the row faction regards the column faction. Source: Factions §VII [CANON] unless labelled.

| | Lowmark | Thornfell | Mire | Emberholt civic | Remnant | Volkhari |
|---|---|---|---|---|---|---|
| **Lowmark** | — | Respectful, strained by caravan safety | Mourning respect | Wary dependence | Unaware | Unaware |
| **Thornfell** | Trade, mild envy of calm politics | — | Sympathy, caution | High tension | Unaware (sees Emberholt only) | Unaware |
| **Mire** | Shared grief | Respect between wardens | — | Bitter resentment | Unaware | Unaware |
| **Emberholt civic** | Mocks as soft, depends on grain | Sees as fearful traditionalists | Sees as stagnant | — | Speaker allied; most unaware | Claims they "abandoned the city" |
| **Remnant** | Limited interest; buys information | Sees as dormant | Dismisses as inert | Shapes it | — | Hunts and studies |
| **Volkhari** | Unknown | Unknown | Unknown | Avoids | Greatest threat | — |

How the matrix changes over the journey [PROPOSAL]: each regional arc can soften one hostile cell by evidence (Thornfell learns its own stop; the Mire receives names; Emberholt citizens see their curriculum). The convergence asks whether the remaining cells can hold long enough for the four seats to meet.
