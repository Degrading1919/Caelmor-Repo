# Caelmor — Lowmark Economy Content Integration

**Status:** proposal-stage content integration for Creative Director audit. Every content example and selection first introduced here is **PROVISIONAL**. This document makes the approved economy architecture concrete enough for later content production without altering canon or authorizing implementation.

## Authority and limits

This proposal integrates the approved material, inventory, processing, gathering, progression, placement, and node-blueprint work.

- The nine represented equipment-chain states remain plain carbon steel stock, raw hide, vegetable-tanned leather, flax bundle, flax tow, linen textile, tannin-rich bark, wood charcoal, and rendered tallow.
- Hunting, Woodcutting, Smithing, and Leatherworking retain their approved responsibilities. No new skill is introduced.
- Household flax, textile work, husbandry, ordinary tanning, charcoal work, rendering, and steel receiving remain ordinary labor or trade.
- Ordinary wood is one broad provisional tangible inventory state outside the nine equipment-chain states. Edible Hunting output remains a functional relationship pending its later catalog.
- All exact species, wood forms, food items, quantities, values, levels, timings, locations, routes, stock rates, and implementation behavior remain open.
- S01 remains deferred. This document contains no ranged dependency.

## 1. Integration proposition

Lowmark's economy should be encountered as a set of **visible custody handoffs**, not as isolated resource stations or a simulated commodity market:

```text
source or ordinary supplier
→ gather, deliver, receive, or commission
→ approved output relationship
→ ordinary conversion or player craft
→ represented inventory state
→ equipment construction or use
→ maintenance, refurbishment, civic demand, or trade sink
```

The player may enter this chain at several points. They may gather, buy, supply, commission ordinary conversion, craft, repair, store, or sell. Background workers remain credible because production does not wait for the player. The design stays comprehensible because no interaction requires managing workers, prices, transport schedules, or businesses.

### Tangible ordinary-wood contract

Ordinary wood is a tangible player-owned v1 economy state while remaining outside the nine equipment-chain states.

1. Valid Woodcutting produces one broad provisional **ordinary wood** inventory state.
2. The player may keep, bank, trade, or supply it to an approved downstream relationship.
3. Normal lawful ordinary wood has a dependable baseline market outlet. Specialist, civic, and processor demand may provide different value, convenience, usefulness, or purpose without becoming unlimited high-value deletion sinks.
4. Purpose-bound work preserves its disclosed special destination through successful completion, but the resulting wood remains player owned until the player chooses to supply it.
5. Eligible bark remains its existing inventory co-output and follows the tanning relationship separately.

This selection supports accumulation, familiar bank routes, trade versus self-supply, and later-use choice without species-specific logs, grades, fuelwood, repair stock, offcuts, or multiple tiers. A later split requires an approved downstream system demonstrating a real need.

## 2. Provisional ordinary-economy content set

The following are reusable content situations, not final named nodes, buildings, professions, or locations. They map to the six approved supply interface patterns and may share assets or physical space only where their work is compatible.

### P-O1 — Household flax exchange

**Interface pattern:** S1, household produce and animal exchange.

**Concrete world evidence:** cultivated fiber drying under cover, tied source bundles, protected household stores, and conversation that distinguishes family need from marketable surplus.

**Player verbs:** purchase a flax bundle, sell an accepted bundle obtained through later lawful relationships if any are approved, deliver a bounded household or civic order, or learn that household stock is being retained after disruption.

**Normal flow:** household cultivation and harvest → flax bundle → household store, textile workroom, or market exchange.

**Provisional changed state:** flood damage, wet storage, labor diverted to food recovery, or household cloth need temporarily reduces market surplus. This changes availability or destination; it does not create a Farming activity.

**Why it matters:** flax is rooted in Lowmark households before it becomes an abstract crafting input. The player sees why a bundle exists and where textile workers obtain it.

**Must not become:** a crop node, planting minigame, daily household chore, wild-flax gathering loop, or exact crop calendar.

### P-O2 — Husbandry and animal-processing handoff

**Interface pattern:** S1.

**Concrete world evidence:** animal care, food priority, protected hide handling, separation of edible use from workshop material, and a processor able to reject spoiled or ineligible deliveries.

**Player verbs:** purchase ordinary raw hide when available, sell a qualified hunted hide, deliver eligible game into a legitimate food-and-processing flow, or choose another receiving point when household stock is retained.

**Normal flow:** husbandry or eligible game delivery → edible relationship remains with food use; qualified hide enters inventory or tannery custody; suitable fat routes internally toward rendering.

**Provisional changed state:** animal illness, household retention, failed preservation, or disrupted processor access reduces accepted hide or rendering feed without making all wild game suddenly more productive.

**Why it matters:** husbandry supports baseline leather supply and tallow feed, while Hunting remains a meaningful alternate source with more direct player control.

**Must not become:** livestock management, a raw-fat item, a universal hide rule, a meat catalog, or an excuse to add horns, bones, sinew, organs, and trophies without sinks.

### P-O3 — Shared textile workroom

**Interface pattern:** S2, textile workroom.

**Concrete world evidence:** sorted flax bundles, internal fiber preparation, visible tow retention, woven linen, dry work surfaces, and finished goods held separately from work in progress.

**Player verbs:** sell or deliver a flax bundle, commission the established conversion, collect or purchase linen textile and flax tow, or store the finished states for later Leatherworking.

**Normal flow:** flax bundle → ordinary drying and fiber preparation → linen textile plus flax tow. Thread and intermediate fiber remain workshop-only.

**Provisional changed state:** wet conditions, storage pests, household cloth priority, or workroom damage interrupts conversion and points the player toward held stock or another ordinary supplier.

**Why it matters:** the one-to-two conversion makes linen and tow legible as physically distinct outputs without inventing Textile as a skill.

**Must not become:** a loom skill, a timing minigame, separate tow harvesting, a choice that destroys the unselected sibling output, or an inventory chain of prepared fiber and thread.

### P-O4 — Tannery intake and leather exchange

**Interface pattern:** S3, tannery and leather exchange.

**Concrete world evidence:** controlled water use, separated waste, bark and hide custody, drying work, odor, finished leather, and visible reasons for refusing unsafe input.

**Player verbs:** buy or sell accepted raw hide, bark, or finished leather; perform player Leatherworking at an approved workspace; obtain suitable repair material; respond when a yard closes for water or waste reasons.

**Normal flow:** raw hide plus tannin-rich bark → player Leatherworking or ordinary tanning → vegetable-tanned leather → flexible construction, mixed construction, and repair.

**Provisional service boundary:** ordinary tanners sell finished leather and may buy valid inputs. They do not automatically offer unrestricted on-demand conversion of every player hide.

**Why it matters:** the world can repair and clothe itself, while player Leatherworking retains transformation control and equipment mastery.

**Must not become:** a universal instant converter, a superior-leather ladder, a residue-item generator, or dirty work placed beside protected domestic or memorial water for player convenience.

### P-O5 — Fuel-worker intake and charcoal store

**Interface pattern:** S4, fuel and rendering exchange.

**Concrete world evidence:** separated feedstock, drying, firebreaks, controlled conversion, cooled charcoal, smoke constraints, and wood reserved for uses more important than fuel.

**Player verbs:** deliver an accepted ordinary-wood relationship from legitimate Woodcutting, sell suitable supply, purchase charcoal, or learn that structural and household claims currently take priority.

**Normal flow:** suitable ordinary wood → ordinary fuel-worker conversion → wood charcoal → Smithing construction and hard refurbishment.

**Provisional changed state:** wet feedstock, high fire risk, smoke restrictions, or public reservation temporarily changes intake or charcoal availability.

**Why it matters:** player Woodcutting can feed Smithing indirectly without producing charcoal through a new skill. Fuel demand provides one legitimate destination among several for ordinary wood.

**Must not become:** a charcoal recipe, charcoal node, universal wood sink, kiln-management game, or reason to cut material reserved for repair.

### P-O6 — Renderer intake and maintenance supply

**Interface pattern:** S4.

**Concrete world evidence:** a legitimate animal-processing handoff, controlled heat, cleanliness, strained finished supply, safe storage, and rejection of spoiled or unsuitable matter.

**Player verbs:** deliver eligible game through the processor relationship, sell to an accepting intake, buy rendered tallow, and use the finished good in justified finishing or maintenance.

**Normal flow:** suitable fat routed from husbandry or eligible delivered game → ordinary rendering → rendered tallow → Leatherworking maintenance and bounded Smithing surface care.

**Provisional changed state:** absent feed, contamination, fire closure, or household priority reduces finished tallow without creating a gather-fat task.

**Why it matters:** a real byproduct becomes a persistent maintenance good without cluttering Hunting inventory or forcing Cooking into the equipment chain.

**Must not become:** a Rendering skill, raw-fat item, direct player recipe, tallow loot drop, or universal repair substance.

### P-O7 — Imported steel receiving and inspection

**Interface pattern:** S5, imported steel receiving.

**Concrete world evidence:** secured consignments, condition inspection, ordinary custody records, stock separated from suspicious remains, carriers, and repair workshops waiting on accepted material.

**Player verbs:** purchase lawful plain carbon steel stock, place it in accessible storage, sell accepted conventional stock where later supported, collect workshop supply, or respond to an interrupted consignment by conserving and repairing.

**Normal flow:** outside conventional production → lawful consignment → receiving inspection → plain carbon steel stock → storage or Smithing → equipment and hard refurbishment.

**Provisional changed state:** delayed arrival, damaged consignment, disputed custody, or civic repair reservation constrains circulation until another lawful shipment or resolution arrives.

**Why it matters:** Lowmark's dependence is visible, and hard equipment scarcity can matter without inventing local ore.

**Must not become:** Lowmark Mining, a superior-metal tier, renewable Great War salvage, a contraband default, or an exact supplier route.

### P-O8 — Market, accessible storage, and craft cluster

**Interface pattern:** S6, market, storage, and craft network.

**Concrete world evidence:** household sellers, received goods, secured stores, repair queues, smith and leather workshops, and separation between clean trade space and risky production.

**Player verbs:** buy, sell to an accepting buyer, deposit, withdraw, craft from accessible storage, commission textile conversion or appropriate equipment work, repair, refurbish, and read bounded shortage or priority notices.

**Normal flow:** all approved transferable states circulate through credible custody → Smithing or Leatherworking uses represented inputs → finished equipment returns to use and later repair.

**Provisional changed state:** a damaged store, public repair priority, delayed receiving, or workshop backlog alters one relationship at a time and offers a clear alternate response.

**Why it matters:** the cluster connects gathering and ordinary labor without collapsing every profession into one universal counter.

**Must not become:** a global auction house, infinite vendor sink, warehouse-management game, universal production station, or player-to-player dependency.

### P-O9 — Public repair demand

**Cross-interface condition:** C3 reserved/commissioned applied across W5, S4, S5, and S6 rather than a seventh supply family.

**Concrete world evidence:** visibly worn or damaged crossings, water-control works, storage structures, work yards, or ordinary public equipment; workers sorting what can be maintained; and a bounded statement of the current need.

**Player verbs:** direct suitable ordinary wood from approved woodland work, sell or supply accepted charcoal or conventional steel stock, perform only already-approved equipment craft or refurbishment where independently relevant, or leave the entire need to ordinary crews.

**Normal flow:** existing civic wear or bounded damage → declared repair need → accepted ordinary supply → ordinary crews and their specialist workshop labor restore public function → consumed material and continuing maintenance demand.

**Why it matters:** public repair connects Woodcutting, imported stock, fuel work, markets, and workshops while expressing Lowmark's culture of patient upkeep. It provides a recurring sink and post-mastery purpose without manufacturing endless superior gear.

**Must not become:** a daily task board, mandatory tax, construction-management system, permit token, exact governance ruling, or excuse to accept every wood and metal delivery.

Public infrastructure repair is not a fifth player recipe family. Supplying an intake does not authorize the player to craft bridges, dikes, buildings, or waterworks.

## 3. Concrete source-to-sink traces

Each trace uses only approved states and relationships. No arrow requires an inventory item merely because a physical step occurs.

### Trace 1 — Hunted hide into flexible equipment

```text
eligible Hunting opportunity
→ hunt and successful field recovery
→ conditional guaranteed raw hide [inventory]
→ player Leatherworking with tannin-rich bark
→ vegetable-tanned leather [inventory]
→ Leatherworking construction
→ Riverpath-path equipment
→ leather or fastening repair using represented material
```

The edible relationship and suitable-fat route remain available where physically appropriate, so the hunt does not exist solely for hide.

### Trace 2 — Hunted game into food and maintenance relationships

```text
eligible Hunting opportunity
→ responsible recovery and animal-processing delivery
→ edible relationship toward later Cooking design
+ suitable fat routed internally when qualified
→ ordinary rendering
→ rendered tallow [inventory/trade]
→ finishing or maintenance where justified
→ recurring care sink
```

No meat, cut, fat, or recipe catalog is selected. The relationship is functional because food use and maintenance receive separate destinations.

### Trace 3 — Husbandry into ordinary leather supply

```text
ordinary husbandry and legitimate animal processing
→ qualified raw hide [inventory or tannery custody]
→ ordinary tanner using approved bark supply
→ vegetable-tanned leather [inventory/trade]
→ buyer/crafter construction or repair
→ equipment use and recurring flexible repair
```

This trace keeps a non-Hunting path viable without granting an unrestricted NPC conversion service for every player-held hide.

### Trace 4 — Flax household to equipment lining and damping

```text
household cultivation
→ flax bundle [inventory/trade]
→ textile workroom commission or ordinary production
→ linen textile + flax tow [inventory/trade]
→ Leatherworking integration
→ lining, joining, wrapping, damping, or padding function
→ later lining or padding repair sink
```

Thread, cut panels, and padding packages remain workshop-only.

### Trace 5 — Managed woodland into tanning

```text
eligible stewardship-approved Woodcutting opportunity
→ selective harvest or pruning for a legitimate primary purpose
→ ordinary wood [inventory/trade/storage]
+ conditional guaranteed tannin-rich bark [inventory]
→ player Leatherworking or ordinary tannery
→ vegetable-tanned leather
→ construction and repair sinks
```

Bark remains a co-output. If the ordinary wood has no legitimate destination, the opportunity cannot be justified as disguised bark gathering.

### Trace 6 — Managed woodland into forge fuel

```text
approved Woodcutting or ordinary forestry
→ suitable ordinary wood [inventory/trade/storage]
→ accepted fuel-worker intake
→ ordinary conversion
→ wood charcoal [inventory/trade]
→ Smithing construction or hard refurbishment
→ equipment use and future repair demand
```

The same Woodcutting action can instead direct suitable wood toward household or public repair use. Fuel is one destination choice, not the universal answer.

### Trace 7 — Imported steel into hard equipment

```text
outside conventional metal production
→ lawful consignment and receiving inspection
→ plain carbon steel stock [inventory/trade/storage]
→ Smithing with charcoal
→ Keeper's Blade, Crestbridge Guard, or Bridgewarden Harness path construction
→ use
→ maintenance or workshop refurbishment using physically appropriate represented inputs
```

Later milestones deepen workmanship, geometry, fitting, inspection, repairability, and commission legitimacy. They do not substitute a superior metal.

### Trace 8 — Public repair as an ordinary-wood and workshop sink

```text
bounded civic maintenance need
→ W5 public-repair reserve selection or accepted ordinary supply
→ player-owned ordinary wood supplied to the declared public intake
+ accepted conventional hard inputs and fuel where physically needed
→ ordinary repair crews and their appropriate specialist workshop labor
→ restored civic function
→ future maintenance remains possible
```

Ordinary wood remains one broad inventory family. Public repair consumes useful supply without inventing a repair-token or repair-stock item.

### Trace 9 — Personal equipment repair through accessible storage

```text
equipment condition creates a justified maintenance need
→ workshop reads accessible stored materials
→ Smithing or Leatherworking repair family
→ appropriate steel, charcoal, leather, linen, tow, or tallow consumed according to actual failure
→ restored safe function
→ replaced wear, lining, or fastening creates a recurring sink
```

No generic repair kit or per-component durability simulation is required. Unsafe primary structure still requires workshop refurbishment.

## 4. Hunting and Woodcutting integration

### Hunting integration rules

1. Each opportunity communicates whether edible use, hide eligibility, and possible rendering feed are physically supported; those facts are related but not identical.
2. The player chooses custody after recovery: keep a represented hide, deliver eligible game, sell to an accepting intake, or use another approved destination.
3. Normal lawful transferable outputs have a dependable baseline market outlet. Specialist processors may apply capacity, preservation, and role requirements, and no outlet provides unlimited premium value.
4. Husbandry protects non-Hunting viability. Hunting protects player control and gives ecology, route knowledge, recovery, and multi-output judgment a direct economic payoff.
5. Advanced and later Hunting content earns value through condition preservation, routing, and purpose, not superior hide names.

### Woodcutting integration rules

1. Every opportunity begins with a legitimate ordinary-wood purpose. Bark may appear only when the chosen source and action physically produce it.
2. Valid work produces player-owned ordinary wood that may be kept, banked, sold through the baseline market, or supplied to household, public-repair, or fuel-worker demand where suitable.
3. Bark enters tanning directly; it never receives a bark-only node, action, or opportunity.
4. Ordinary forestry protects non-Woodcutting viability. Player Woodcutting provides direct custody, source judgment, civic participation, and route efficiency.
5. Advanced and later Woodcutting content earns value through selecting the smallest responsible intervention and matching condition to destination, not higher-tier trees.

### Shared anti-management pattern

Workers perform ordinary conversion. The player may accumulate and route transferable goods, but does not allocate labor, operate production calendars, negotiate freight, maintain processor inventories, or balance several civic claims at once. Purpose-bound work may expose at most one special destination choice.

## 5. Playstyle stress tests and revisions

### Hunting-heavy player

**Concrete route:** complete varied H1–H6 opportunities → recover edible and eligible hide relationships → keep some hide for Leatherworking → sell accepted hide → deliver eligible game to food/renderer intake → purchase missing flax, bark, charcoal, tallow, and steel as needed.

**Risk found:** raw hide could outpace tannery demand, and repeating the easiest target could become a hide grind.

**Revision:** lawful transferable goods retain a dependable baseline market outlet while processors offer contextual destinations; higher progression requires different behavior, habitat, recovery, stewardship, and routing. Edible use and rendering feed preserve value outside Leatherworking. No extra animal outputs are added as surplus sinks.

**Result:** **STRONG**, subject to later content proving the six Hunting archetypes feel materially different.

### Woodcutting-heavy player

**Concrete route:** complete W1–W6 legitimate work → receive ordinary wood inventory plus qualified bark where applicable → keep or bank wood, use baseline trade, or supply public repair or accepted fuel intake → keep or sell bark → buy other equipment inputs.

**Risk found:** fuel work could become the automatic destination, while bark could dominate the reason to cut.

**Revision:** ordinary wood remains the primary purpose; structural and public repair claims can outrank fuel; bark occurs only from a qualified cut and cannot justify an otherwise pointless opportunity. The baseline market prevents routine stranding, while specialist destination matching remains part of mastery.

**Result:** **STRONG**, subject to later ordinary-wood design preserving several real uses without item bloat.

### Buyer/crafter

**Concrete route:** purchase lawful stock and ordinary inputs → commission textile conversion where useful → perform Smithing or Leatherworking → maintain and refurbish equipment → sell accepted finished or surplus goods only under later trade rules.

**Risk found:** easy ordinary supply could detach crafting from the world and make gathering irrelevant.

**Revision:** visible custody, bounded stock, occasional disruptions, and direct-gathering control preserve a difference between buying and sourcing. Player craft retains construction, repair, and aspirational mastery that ordinary suppliers do not replace.

**Result:** **STRONG.** Buying is a legitimate playstyle with exposure to ordinary availability.

### Mostly self-supplying player

**Concrete route:** hunt eligible hides, gather qualified bark and ordinary wood, tan leather personally, route wood to fuel workers, commission textile conversion, and trade gathered value for imported steel and other ordinary outputs.

**Risk found:** “self-supply” could be interpreted as a requirement to personally cultivate flax, make charcoal, render tallow, weave cloth, or mine steel.

**Revision:** self-supply means controlling chosen sources and primary craft while using credible ordinary labor. It does not mean solitary production of every input. The architecture exposes clear handoffs without hidden skills.

**Result:** **STRONG.** Ordinary interdependence remains intentional rather than a failure of autonomy.

### Post-mastery player

**Concrete route:** select H6 or W6 purpose-bound work, combine gathering with accepted delivery and repair needs, preserve hard-to-recover value, maintain aspirational equipment, contribute to bounded public repair, and choose between market, workshop, and civic sinks.

**Risk found:** after aspirational equipment, output volume or cosmetic reskins could become the only reason to continue.

**Revision:** later opportunities must provide at least one approved nonnumeric knowledge payoff: earlier diagnosis, invalid-work avoidance, safer recovery, more efficient combined delivery, or legitimate access to purpose-limited work. Civic repair and equipment maintenance recur without superior materials or mandatory daily tasks.

**Result:** **STRONG architecturally.** Later content must demonstrate an appropriate cadence and payoff, not add another tier.

## 6. Economy fault audit and applied fixes

| Fault tested | Concrete symptom | Applied architecture fix | Result |
|---|---|---|---|
| Surplus hides | Hunting-heavy player produces more than immediate Leatherworking need | Dependable baseline market outlet plus contextual tannery/processor demand; edible and renderer relationships remain distinct | **FIXED architecturally** |
| Surplus bark | Player chooses every eligible cut for tannery sales | Bark remains co-output of legitimate wood work; acceptance and hide demand constrain sink; no bark-only opportunity | **FIXED** |
| Linen/tow imbalance | One sibling output has lower current equipment demand | Both retain several construction and repair functions; conversion remains joint; later tuning validates proportions rather than inventing a disposal recipe | **BOUND FOR BALANCE** |
| Missing hard-material supply | Steel disruption halts all hard construction | Lawful trade, accessible storage, conservation, and refurbishment remain; flexible work continues; no local ore patch | **FIXED** |
| Repetitive routing | Every gathered output travels to the same market counter | Hunting has keep, processor, tannery, and market custody; ordinary wood supports bank, baseline trade, repair, and fuel destinations; dirty work remains separate | **FIXED** |
| Stranded lawful goods | Contextual specialists refuse normal transferable output | Provide a dependable baseline market outlet while preserving specialist/civic/processor destinations; purpose-bound demand remains valid through completion | **FIXED** |
| Forced processing chores | Player must run every ordinary conversion before crafting | Ordinary workers sell output and accept bounded commissions; buying remains viable | **FIXED** |
| Hidden professions | Textile, fuel, or rendering service gains XP-like repeated input loop | Ordinary commission or market handoff only; no new progression track or player production minigame | **FIXED** |
| Weak gathering progression | Later play repeats the same interaction for more output | Six archetypes per skill change behavior, context, stewardship, recovery, and purpose; knowledge payoff contract applies | **FIXED architecturally** |
| Repair destroys scarcity | Maintenance restores any failure with a cheap universal input | Failure-specific represented materials; structural refurbishment remains bounded workshop work | **FIXED** |
| Ordinary supply erases skills | NPC goods are unlimited and equivalent to player mastery | Ordinary supply ensures continuity; player skills own control, construction, repair, opportunity judgment, and commission qualification | **FIXED** |
| Player supply erases society | Region waits for the player to produce essentials | Households and specialists continue background supply; player contribution is optional and responsive | **FIXED** |

No new material or skill is required to correct these faults.

## 7. Rejected content ideas

| Rejected idea | Reason |
|---|---|
| Daily profession request board | Turns ordinary work into mandatory rotating chores and multiplies authored maintenance. |
| Personal farm, herd, kiln, renderer, or textile shop | Creates management systems and hidden skills outside v1 scope. |
| Infinite all-goods merchant | Erases source, labor, custody, disruption, and self-supply value. |
| Separate vendor for each represented state | Mistakes inventory identity for a need for a separate world object. |
| Raw fat, thread, charcoal feedstock, repair kit, lining kit, or strap kit items | Adds intermediates without a demonstrated trade, choice, storage, or multi-recipe need. |
| Public-repair token or permit inventory | Turns civic legitimacy into a consumable object and adds arbitrary gating. |
| Player charcoal or rendering recipe | Introduces an unapproved profession-shaped loop. |
| Local ore emergency source | Contradicts intentional imported-steel dependence. |
| Great War metal recovery circuit | Treats finite, political, and evidentiary remains as renewable supply. |
| Higher-tier hides, bark, flax, charcoal, or tallow | Replaces workmanship progression with material reskins. |
| Rare animal byproducts added as overflow sinks | Creates catalog bloat and gathering incentives before uses exist. |
| Public repair that accepts any wood | Removes stewardship and source-condition judgment. |

## 8. Resolved Creative Director direction applied

- Public repair is occasional, optional, and left active through ordinary crews.
- Normal lawful transferable goods have a dependable baseline market outlet; specialist demand remains contextual and role-specific.
- Textile conversion remains commissionable ordinary labor.
- Ordinary tanners sell leather and buy appropriate inputs without erasing player Leatherworking.
- Disruptions are occasional, authored, stable enough to learn, and never rotating chores.
- Ordinary wood is tangible, bankable, tradeable, and broadly reusable as one provisional state.

These rulings affect content presentation and recurrence without changing the six-material equipment foundation, nine equipment-chain states, or canon.

## 9. Content-integration result

The approved economy can now be expressed through nine provisional content situations and nine complete source-to-sink traces without adding a skill, material, inventory intermediate, management layer, or exact map commitment. Hunting and Woodcutting feed ordinary labor through clear custody decisions; households and specialists keep the region functional; markets, storage, workshops, and public repair provide understandable circulation and sinks.

The remaining risks belong to later content and balance validation:

- demonstrate that six Hunting and six Woodcutting archetypes produce distinct decisions with shared systems;
- verify that linen and tow demand remains healthy when quantities are designed;
- set a bounded cadence for disruption and public repair;
- decide only if a later approved downstream system genuinely requires splitting ordinary wood or representing edible output more precisely; and
- tune baseline market value against specialist and civic value without creating an unlimited high-value sink.

No missing supply relationship or fixable content-architecture gap remains in this integration pass.
