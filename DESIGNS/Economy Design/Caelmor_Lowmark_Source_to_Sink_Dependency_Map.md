# Caelmor — Lowmark V1 Source-to-Sink Dependency Map

**Status:** integrated proposal-stage dependency audit. All selections are provisional pending Creative Director review. This document traces approved economic relationships without assigning quantities, rates, prices, exact recipes, nodes, or implementation structures.

## Audit standard

Every represented state and supporting relationship must answer:

1. where it originates;
2. who performs the relevant action;
3. how it becomes an inventory state;
4. which processing or recipe consumes it;
5. which equipment or maintenance purpose creates demand;
6. how ordinary supply and player action coexist;
7. what prevents infinite reuse or artificial scarcity; and
8. whether the activity remains worthwhile without XP.

The nine approved equipment-chain states remain unchanged. D11 adds one broader v1 economy inventory state, ordinary wood. Edible Hunting output, suitable fat, and other unapproved goods remain relationship placeholders outside the represented catalog.

Normal lawful transferable goods have a dependable baseline market outlet under D07. Specialist, processor, and civic destinations remain contextual and may differ in value or purpose; no outlet is an unlimited high-value deletion sink.

## End-to-end chain map

| World source or ordinary supplier | Logical action | Output relationship | Represented state | Processing or circulation | Equipment destination | Maintenance or sink |
|---|---|---|---|---|---|---|
| Conventional outside metal production | Produce, carry, receive, and inspect lawful stock | Imported guaranteed consignment | Plain carbon steel stock | Market, storage, Smithing workshop | Keeper's Blade, Crestbridge Guard, Bridgewarden Harness, justified hard fittings | Hard refurbishment, working-surface restoration, structural section repair, retirement loss |
| Eligible hide-bearing game | Hunt and field-dress successfully | Source-conditional guaranteed output | Raw hide | Player Leatherworking or ordinary tannery | Converted to leather before equipment use | Spoilage or rejection before tanning; no direct repair use |
| Ordinary husbandry and animal processing | Direct legitimate hide flow to a processor or market | Ordinary guaranteed or source-conditional supply | Raw hide | Player Leatherworking or ordinary tannery | Converted to leather before equipment use | Household retention, spoilage, or processing loss constrains supply |
| Raw hide plus tannin-rich bark | Perform approved tanning process | Guaranteed processing output | Vegetable-tanned leather | Storage, market, construction, repair | Riverpath Leathers; justified flexible parts across other paths | Patching, refitting, fastening replacement, section replacement, retirement of unsafe material |
| Lowmark household cultivation | Cultivate, harvest, dry, and bundle flax | Guaranteed ordinary supply | Flax bundle | Household or specialist textile conversion | No direct equipment use | Converted rather than consumed in equipment; storage loss remains possible later |
| Flax bundle | Prepare fiber, retain tow, spin and weave | Deterministic joint conversion | Flax tow | Storage, market, Leatherworking | Damping, padding, fitted flexible work | Padding renewal; packed or contaminated tow is retired |
| Flax bundle | Prepare fiber, spin, and weave | Deterministic joint conversion | Linen textile | Storage, market, Leatherworking | Lining, joining, wrapping, flexible support | Relining, restitching, wrapping, patching; unsafe remnants retired |
| Eligible managed woodland work | Perform stewardship-approved selective harvest | Source-conditional guaranteed co-output | Tannin-rich bark | Storage, trade, Leatherworking or tannery | Indirectly enables every leather component | Consumed in tanning; spent bark has no equipment inventory identity |
| Suitable wood flow from player, ordinary, civic, or trade sources | Fuel workers dry and convert feedstock | Guaranteed ordinary-labor conversion | Wood charcoal | Storage, trade, Smithing workshop | Heat for all steel construction | Heat for refurbishment; consumed fuel does not recycle |
| Legitimate animal-processing flow | Renderers clean and stabilize suitable fat | Guaranteed ordinary-labor conversion | Rendered tallow | Storage, market, Leatherworking, bounded Smithing use | Finishing and conditioning where justified | Recurring care, thread dressing, friction and surface management; consumed through use |

## Functional dependency graph

```text
HUNTING ───────────────────────┐
  edible relationship ────────┼─→ future Cooking economy
  raw hide ───────────────────┤
  suitable-fat route ───────┐ │
                            │ │
HUSBANDRY ──────────────────┼─┼─→ raw hide ─┐
  suitable-fat route ───────┘ │             │
                              │             ├─→ Leatherworking / tannery ─→ leather
MANAGED WOODCUTTING ──────────┼─→ bark ─────┘                                │
  ordinary wood [inventory] ──┼─→ bank / baseline trade / repair supply       │
  suitable wood route ────────┴─→ fuel workers ─→ charcoal                   │
                                                                              ├─→ flexible equipment
HOUSEHOLD FLAX ─→ flax bundle ─→ textile labor ─→ linen + tow ───────────────┤
                                                                              └─→ flexible repairs

OUTSIDE METAL PRODUCTION ─→ receiving ─→ steel stock ─┐
                                                       ├─→ Smithing equipment
charcoal ──────────────────────────────────────────────┤
leather / linen / tow where physically required ──────┘

animal-processing flow ─→ renderers ─→ tallow ─→ finishing + recurring maintenance

markets + storage + workshops connect self-supply, ordinary supply, crafting, and repair
```

## Inventory-state dependency ledger

### Plain carbon steel stock

- **Supply reason:** Lowmark needs conventional metal but lacks an approved complete local ore chain.
- **Player interaction:** buy, receive through authored work, store, allocate, craft, or use in repair. The player does not mine it locally.
- **Primary sinks:** three Smithing-led equipment paths and hard refurbishment.
- **Scarcity controls:** import disruption, receiving acceptance, civic demand, storage, workshop backlog, fuel availability, and rejection of unsafe stock.
- **Oversupply outlet:** new construction, delayed repairs, civic or household metal demand outside this pass, and storage subject to later limits. No XP-only smithing sink is created.
- **Reuse boundary:** only inspected sound recovered matter may later return to the same stock state; recovery loss and safe retirement must prevent closed-loop multiplication.
- **Without-XP value:** essential equipment and repair input.

### Raw hide

- **Supply reason:** visible transformation gives Hunting, husbandry, and Leatherworking a real relationship.
- **Player interaction:** recover from eligible game, buy, sell, store subject to later condition rules, or tan.
- **Primary sink:** leather preparation.
- **Scarcity controls:** target eligibility, recovery condition, husbandry supply, spoilage risk, tanning capacity, and household retention.
- **Oversupply outlet:** ordinary tanners and trade, bounded by processing and storage rather than disposable recipes.
- **Reuse boundary:** cannot be recovered once tanned; rejected or spoiled hide does not become a new material tier.
- **Without-XP value:** direct trade and leather-production value.

### Vegetable-tanned leather

- **Supply reason:** stable flexible structure needed across all four equipment paths where justified.
- **Player interaction:** make through Leatherworking, buy bounded ordinary supply from tanners, store, craft, repair, or sell. A universal on-demand NPC conversion service is not assumed.
- **Primary sinks:** Riverpath construction, mixed flexible work, replacement fastenings, patches, refitting, and section repair.
- **Scarcity controls:** hide and bark supply, tanning water and waste constraints, labor, drying, and repair demand.
- **Oversupply outlet:** broad construction and repair use; ordinary household and work uses can exist later but are not invented here.
- **Reuse boundary:** sound offcuts may remain workshop efficiency; removed, stretched, rotten, or contaminated pieces do not automatically return as leather inventory.
- **Without-XP value:** versatile equipment and repair material.

### Flax bundle

- **Supply reason:** maintains a visible agricultural source for linen and tow without creating Farming.
- **Player interaction:** buy, sell, deliver, store, or commission ordinary conversion.
- **Primary sink:** textile conversion.
- **Scarcity controls:** household production, harvest disruption, water and drying conditions, labor, storage, and food-versus-fiber land pressure.
- **Oversupply outlet:** conversion into two useful outputs; no direct equipment stuffing shortcut.
- **Reuse boundary:** converted bundle does not return from textile goods.
- **Without-XP value:** source commodity with independent conversion and trade value.

### Flax tow

- **Supply reason:** distinct damping and padding behavior produced from the same flax flow as linen.
- **Player interaction:** buy, sell, store, allocate to construction or repair.
- **Primary sinks:** impact damping, padding, refitting, and renewal.
- **Scarcity controls:** flax supply, conversion capacity, competing textile demand, and actual equipment designs needing damping.
- **Oversupply outlet:** repairs and later ordinary textile uses only if separately approved; the design must not inflate tow output beyond sinks.
- **Reuse boundary:** packed, wet-damaged, or contaminated tow is retired.
- **Without-XP value:** improves equipment fit and maintains damping.

### Linen textile

- **Supply reason:** supplies lining, joining, wrapping, and repair without a separate thread inventory.
- **Player interaction:** buy, sell, store, allocate to construction, relining, stitching, or patches.
- **Primary sinks:** all equipment paths where physically required and recurring flexible repair.
- **Scarcity controls:** flax and household conversion, labor, clean water, drying, storage, and ordinary cloth demand.
- **Oversupply outlet:** repeated lining and repair sinks plus broader household use left for later economy design.
- **Reuse boundary:** sound remnants may reduce workshop loss internally; worn or contaminated textile does not automatically return as linen inventory.
- **Without-XP value:** common cross-path construction and maintenance input.

### Tannin-rich bark

- **Supply reason:** grounds leather transformation in responsible woodland work and a real consumed input.
- **Player interaction:** receive as eligible Woodcutting co-output, buy ordinary forestry supply, store, sell, or use in tanning.
- **Primary sink:** every hide-to-leather operation.
- **Scarcity controls:** eligible sources, legitimate cutting purposes, woodland closure, bank protection, public repair priority, household fuel pressure, and ordinary forestry capacity.
- **Oversupply outlet:** leather production; no bark-burning or bark-only XP recipe is added.
- **Reuse boundary:** consumed in tanning; spent bark has no approved equipment sink.
- **Without-XP value:** directly enables a valuable processed material.

### Ordinary wood — broader v1 economy state

- **Supply reason:** gives valid Woodcutting tangible accumulation and connects managed woodland work to trade, ordinary repair, and fuel conversion without species tiers.
- **Player interaction:** keep, bank, buy, sell through a dependable baseline outlet, supply household or civic repair demand, or deliver suitable stock to fuel workers.
- **Primary sinks:** ordinary household and civic repair relationships plus conversion into charcoal where suitable. Later uses require separate approval.
- **Scarcity controls:** legitimate work, source health, stewardship, closures, ordinary forestry supply, repair demand, and fuel-worker acceptance.
- **Oversupply outlet:** dependable baseline trade at later-tuned value. Specialist demand may be more useful or valuable but is contextual.
- **Reuse boundary:** one broad state only; no species logs, grades, repair stock, fuelwood, offcuts, or multiple tiers.
- **Without-XP value:** supports accumulation, banking, trade, self-supply, repair supply, and indirect Smithing fuel.

### Wood charcoal

- **Supply reason:** makes Smithing heat a visible economic dependency without a player fuel-making skill.
- **Player interaction:** supply eligible ordinary wood to fuel workers, buy, sell, store, allocate between construction and repair.
- **Primary sinks:** all steel construction and hard refurbishment.
- **Scarcity controls:** suitable feedstock, woodland stewardship, drying, conversion capacity, fire risk, household and civic heat claims, storage, and imports.
- **Oversupply outlet:** recurring Smithing and repair demand. No ash or fines catalog is created.
- **Reuse boundary:** consumed as heat; no recovery.
- **Without-XP value:** required for hard equipment production and repair.

### Rendered tallow

- **Supply reason:** supplies a stable, ordinary maintenance input from legitimate animal use.
- **Player interaction:** deliver eligible Hunting output into ordinary processing, buy, sell, store, use in finishing or maintenance.
- **Primary sinks:** leather conditioning, thread preparation inside workshops, bounded steel surface care, and repeated item maintenance.
- **Scarcity controls:** husbandry and eligible-game flow, spoilage before rendering, rendering labor, heat, clean storage, household competition, and trade.
- **Oversupply outlet:** recurring maintenance across equipment milestones; broader household uses remain future economy work.
- **Reuse boundary:** consumed through application; residue is not recovered.
- **Without-XP value:** extends equipment service life and supports repairability.

## Equipment destination map

| Equipment path | Construction dependencies | Ongoing sinks | Dependency character |
|---|---|---|---|
| Keeper's Blade | Steel and charcoal; leather, linen, or tallow only if final form physically requires them | Surface care, edge or structure refurbishment, justified control-interface repair | Import-sensitive, Smithing-led, low intermediate count |
| Crestbridge Guard | Steel and charcoal; leather and/or tow/linen only for justified control, retention, damping, or wear | Control and damping service, hard deformation repair, refitting | Mixed but Smithing-led; repeated impact supports repair demand |
| Bridgewarden Harness | Steel and charcoal; leather for flexible interfaces; linen/tow for lining or damping; tallow for maintenance | Fastening, lining, padding, section, and hard-structure refurbishment | Densest material integration, but no extra inventory component family |
| Riverpath Leathers | Leather, linen/tow, tallow; steel only for a justified hard fitting | Conditioning, seam, lining, padding, fastening, panel, and fit repair | Leatherworking-led and locally grounded; no aspirational material swap |

The paths share materials without requiring every item to consume every state. Exact forms remain open.

## Player and ordinary-supply coexistence

| Tension | Required architecture |
|---|---|
| Ordinary supply makes gathering irrelevant | Ordinary sellers offer continuity; players gain control, responsiveness, trade value, and route efficiency through gathering. Authored shortages can increase the value of knowledge without eliminating purchase. |
| Player gathering makes the world implausibly dependent on the player | Husbandry, forestry, tanners, processors, merchants, and households continue to supply goods. The player participates in an existing economy. |
| Buying bypasses skill identity | Buying inputs does not replace the Hunting or Woodcutting mastery experience, but it remains a valid way to pursue Smithing or Leatherworking. |
| Self-supply becomes a mandatory chore | Recipes can draw from storage and markets remain viable. No commission requires personal gathering of every input. |
| Processor services erase crafting | Ordinary conversion covers flax, charcoal, and tallow; player Leatherworking retains meaningful tanning and equipment work, while Smithing retains hard equipment work. |

## Scarcity and repair boundary

Repair is both an attachment system and an economic sink. It must not create either immortality without cost or punitive replacement.

- Field maintenance consumes only justified materials and delays deeper damage; it does not reset every failure.
- Workshop refurbishment consumes appropriate represented materials and access to the primary craft.
- Material use depends on actual damage class, not a generic repair kit.
- Commissioned equipment remains repairable using the same materials; fitting records and accountable labor preserve identity.
- Unsafe primary structures can be retired. Not all matter is recoverable.
- Recovery, if later represented, returns only an existing material state and must include inspection and loss.
- High repair demand should shift player choices toward maintenance, supply, and allocation rather than require constant recrafting.
- Aspirational completion does not end demand: maintenance, alternate paths, household and civic economy, and further mastery keep the same materials relevant.

## Dead-end and artificial-dependency audit

| Risk | Finding | Correction embedded in architecture | Result |
|---|---|---|---|
| Raw hide has one use | Tanning is one transformation but leather has broad construction and repair demand | Hide has mixed supply; Hunting also has food and rendering relationships | **NO DEAD END** |
| Flax bundle is a pass-through item | It exists for cultivation, trade, storage, and a meaningful two-output conversion | Linen and tow have distinct sinks | **JUSTIFIED INTERMEDIATE** |
| Tow becomes surplus | Equipment need may be narrower than linen demand | Tow output proportions remain tunable; no separate tow gathering; repeated padding repair supplies a sink | **WATCH IN BALANCE PASS** |
| Bark drives repetitive cutting | Tanning creates persistent demand | Bark is tied to eligible useful wood work and ordinary forestry supply; never a separate action | **CONTROLLED** |
| Charcoal becomes a mandatory chore | All steel work consumes heat | Ordinary fuel workers and trade supply charcoal; player wood supply is optional | **CONTROLLED** |
| Tallow is single-purpose clutter | Maintenance is recurring but bounded | Tallow crosses flexible equipment and some steel care; no raw-fat inventory is added | **JUSTIFIED** |
| Steel import makes Mining irrelevant globally | Lowmark has no ore loop | Mining can retain regional identity elsewhere; this pass does not force it into v1 | **INTENTIONAL REGIONAL DEPENDENCY** |
| Ordinary leather erases Leatherworking | Leather is purchasable | Player Leatherworking still transforms hide, constructs Riverpath equipment, and repairs flexible work | **CONTROLLED** |
| Repair destroys scarcity | Reuse could close the material loop | Repair consumes materials; retirement and recovery loss remain required | **CONTROLLED, IMPLEMENTATION-SENSITIVE** |
| Crafting exists for XP | Disposable output could absorb surplus | No XP-only recipes or generic components are authorized | **PROHIBITED** |
| Hidden skill dependencies | Ordinary conversions resemble skills | Ownership is explicit: only Smithing, Leatherworking, Hunting, and Woodcutting participate where physically justified | **NO HIDDEN SKILL** |

## Dependency completeness result

- Every approved inventory state has a source or supply relationship.
- Every represented intermediate has trade, storage, conversion, or multi-recipe value.
- Every state reaches construction, repair, or both.
- Hunting serves food, hide, and ordinary rendering relationships.
- Woodcutting serves ordinary wood, tanning bark, and indirect fuel supply.
- Ordinary labor supplies the world without making player action irrelevant.
- Repair consumes represented materials and cannot recover everything.
- Aspirational equipment extends rather than terminates material demand.
- No new skill, material, or supernatural source is required.

**Dependency-map result: COMPLETE FOR PROPOSAL-STAGE NODE AND CONTENT DESIGN.**
