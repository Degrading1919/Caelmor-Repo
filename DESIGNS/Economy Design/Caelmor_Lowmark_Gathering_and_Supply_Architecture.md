# Caelmor — Lowmark V1 Gathering and Supply Architecture

**Status:** integrated proposal-stage architecture. All decisions in this document are provisional pending Creative Director audit. It carries forward the approved equipment purpose, component, material, inventory, processing, and gathering chain without amending canon or authorizing implementation.

## Purpose and limits

Lowmark needs enough world-facing economic structure for player gathering, ordinary supply, processing, trade, storage, crafting, and repair to feel like one lived system. It does not need a simulated population economy or one bespoke station for every item.

This architecture defines opportunity and interface families before exact node production. It sets no species, wood types, node counts, map coordinates, routes, XP, timings, quantities, yields, prices, respawn rules, tool tiers, schemas, or runtime behavior.

The approved foundation remains:

```text
equipment purpose
→ component functions
→ six material foundations
→ nine inventory states
→ four recipe families
→ two player gathering relationships plus ordinary supply
```

## Architecture alternatives

| Alternative | Consequence | Provisional disposition |
|---|---|---|
| **Six world-facing families with reusable variants** | Preserves distinct ecological and civic contexts while allowing shared interaction patterns and assets. | **SELECTED** |
| One centralized economy hub | Easy to implement, but removes work from fields, woodland, settlement edges, crossings, and households. The economy would read as menus rather than Lowmark. | Rejected |
| One world object per material or profession | Makes every inventory state look like a separate node, creates station clutter, and encourages new skills and filler interactions. | Rejected |

The six-family model is a content architecture, not a demand for six prefabs or six locations. A family can have several placed opportunities or service interfaces, and compatible families may share a settlement while remaining socially and physically distinct.

## Family overview

| Family | Primary role | Player relationship | Approved outputs or services |
|---|---|---|---|
| 1. Hunting opportunities | Ecological, multi-output player gathering | Hunt, approach, recover, keep/process/sell | Edible-output relationship; conditional raw hide; routed suitable fat |
| 2. Managed woodland work | Stewardship-bound player gathering | Selective harvest, assess access, recover and route outputs | Tangible ordinary wood inventory; conditional tanning bark; fuel-worker feed possibility |
| 3. Household production network | Makes ordinary agriculture and husbandry visible | Supply, purchase, sell, respond to disruption | Flax bundles; ordinary raw-hide supply; legitimate rendering feed |
| 4. Textile conversion network | Turns flax household output into two useful goods | Commission conversion, purchase, sell, store | Linen textile plus flax tow |
| 5. Settlement-edge process yards | Handles water-, odor-, smoke-, heat-, and waste-bearing conversion | Supply eligible inputs, perform player Leatherworking where supported, or buy outputs through a yard or market | Leather, charcoal, tallow |
| 6. Market, receiving, storage, and craft network | Connects imports, ordinary supply, baseline trade, storage crafting, equipment production, and repair | Receive, trade, store, commission, craft, repair | Steel stock, ordinary wood, and all approved transferable equipment-chain states |

## Family 1 — Hunting opportunities

| Required field | Architecture |
|---|---|
| Purpose | Represent living game through behavior, habitat, access, pursuit, recovery, and output decisions rather than creature-shaped resource nodes. |
| Operator or custodian | No universal operator. Landholders, households, local stewards, settlement interests, and hunters may hold different claims. Exact powers remain open. |
| Logical actions | Read signs, approach or pursue, prepare for behavior and terrain, complete the hunt, field-dress eligible game, and decide what to keep, process, deliver, or sell. |
| Outputs | Edible-output relationship where appropriate; raw hide when the target is hide-bearing and recovery conditions succeed; suitable fat routed to ordinary rendering where accepted. |
| Access and stewardship | Target eligibility, local custody, ecological pressure, seasonal conditions where later supported, and recovery responsibility can permit or restrict an opportunity. |
| Ecological or civic requirements | Credible habitat, readable signs, space for approach and recovery, relationship to fields or woodland, and a reason communities tolerate, request, or refuse the hunt. |
| Broad placement logic | Field margins, orchard or farm edges, scrub and recovering ground, reed or wet-ground margins, maintained passages, and more remote cover classes where the reconciled map supports them. **MAP VERIFICATION REQUIRED.** |
| Disruption or closure | Habitat disturbance, dangerous anomalies, local overpressure, household claims, damaged access, public work, or story conditions may shift or close an opportunity without converting animals into timed dispensers. |
| Why the player cares | Hunting supports food, Leatherworking, trade, ordinary rendering, route knowledge, and mastery of target behavior. |
| Must not represent | Universal hide drops, named final species catalog, stationary carcass nodes, rare-material lotteries, trophies without sinks, supernatural harvesting, or ranged assumptions under S01. |

## Family 2 — Managed woodland work

| Required field | Architecture |
|---|---|
| Purpose | Represent Woodcutting as selective work performed for household, bank, crossing, repair, access, and long-term woodland needs. |
| Operator or custodian | Woodland stewards, households, landholders, repair crews, and local councils may authorize or contest work. No exact jurisdiction is selected. |
| Logical actions | Inspect source and purpose, accept or obtain access, prepare the work area, perform selective harvest, recover ordinary wood, identify eligible bark, and route suitable wood toward repair, trade, or fuel workers. |
| Outputs | One broad tangible ordinary-wood inventory state as primary; tannin-rich bark as a source-conditional guaranteed co-output; suitable wood may enter ordinary charcoal supply. |
| Access and stewardship | Bank stability, woodland health, future repair stock, fire conditions, household claims, public repair priorities, and temporary closures shape what work is responsible. |
| Ecological or civic requirements | A legitimate cutting purpose, safe access, a source whose removal or pruning will not create greater harm, and an accountable destination for the wood. |
| Broad placement logic | Managed working woodland, orchard or hedgerow maintenance contexts, floodplain edges, repair corridors, yards receiving legitimate cut material, and bounded recovery sites. **MAP VERIFICATION REQUIRED.** |
| Disruption or closure | Flood damage, fire risk, erosion, source stress, repair reservation, unsafe windfall, contamination, competing civic demand, or access disputes. |
| Why the player cares | Ordinary wood can be kept, banked, traded through a dependable baseline outlet, or supplied to household, civic, and fuel-worker relationships; bark sustains tanning; better judgment improves route and use choices. |
| Must not represent | Bark-only actions or nodes, clear-cutting, final species, automatic charcoal production, magic-enhanced timber, war-remain harvesting, or a disguised stationary tree-tier ladder. |

## Family 3 — Household production network

| Required field | Architecture |
|---|---|
| Purpose | Make flax cultivation, husbandry, animal processing, and ordinary household surplus visible without turning households into player-managed businesses. |
| Operator or custodian | Farm and animal-keeping households, market sellers, mutual-aid relationships, and ordinary carriers. |
| Logical actions | Households cultivate and bundle flax, care for animals, direct legitimate processing outputs, store necessities, and sell or exchange surplus. Players purchase, deliver, sell eligible Hunting output, or respond to a shortage request. |
| Outputs | Flax bundles; ordinary raw-hide supply; legitimate suitable-fat flow toward renderers. Food and other household outputs remain outside this equipment pass. |
| Access and stewardship | Household ownership, harvest season, flood damage, water scheduling, animal health, food priority, labor capacity, storage condition, and market access. |
| Ecological or civic requirements | Suitable agricultural land, ordinary water access under C09, dry storage, animal care, and connection to a market or processor. |
| Broad placement logic | Agricultural household zones, village edges, farm lanes, storage compounds, and settlement-facing exchange points. Exact farms and routes are unselected. **MAP VERIFICATION REQUIRED.** |
| Disruption or closure | Flood, crop loss, animal illness, damaged stores, labor shortage, route disruption, requisition pressure, or household retention during scarcity. |
| Why the player cares | Provides stable alternatives to gathering, places buy-and-sell relationships in the world, and creates shortages the player can respond to without becoming a manager. |
| Must not represent | A Farming or Husbandry skill, automated player estates, daily chore lists, universal raw-hide production, exact animal or crop catalogs, or infinite vendor generation detached from world conditions. |

## Family 4 — Textile conversion network

| Required field | Architecture |
|---|---|
| Purpose | Represent the economy-visible conversion from flax bundle to linen and tow while keeping fiber preparation, thread, and work in progress internal. |
| Operator or custodian | Household processors, village specialists, shared workrooms, market cloth workers, and carriers. |
| Logical actions | Accept flax bundles, prepare fiber, retain tow, spin and weave suitable fiber, return or sell linen and tow, mend existing work, and manage water and drying needs. |
| Outputs | Linen textile and flax tow as deterministic outputs of the same accepted source flow. |
| Access and stewardship | Clean-water scheduling, drying space, household labor, fire and pest safety, cloth priority, and storage. |
| Ecological or civic requirements | Connection to household flax supply, clean washing without fouling domestic or irrigation water, dry work space, and safe storage. |
| Broad placement logic | Household production areas, village workrooms, clean settlement-edge work areas, and market-facing textile sellers. This family should not share the dirtiest tanning or rendering spaces by default. |
| Disruption or closure | Wet weather, contaminated water, fire, pests, labor shortage, damaged stores, flood loss, or household need taking precedence over market output. |
| Why the player cares | Provides a predictable conversion service and market supply for distinct lining and damping inputs without a Textile skill. |
| Must not represent | A weaving minigame, thread inventory, separate tow harvesting, rare linen drops, textile tier ladders, or a fifth player-facing recipe family. |

## Family 5 — Settlement-edge process yards

This is one interaction family with three physically distinct variants. The variants may share asset and service logic, but they should not be forced into one literal site because their water, smoke, fire, odor, and waste needs differ.

| Variant | Operators | Logical service | Output | Placement and closure requirements |
|---|---|---|---|---|
| Tanning yard | Ordinary tanners and Leatherworking specialists | Accept suitable raw hide and bark; support player Leatherworking where approved; sell ordinary finished leather without promising unrestricted on-demand conversion | Vegetable-tanned leather | Away from domestic and memorial water; access to controlled water and drying; can close for unsafe waste, odor, flood, or water conflict |
| Fuel yard | Fuel workers, woodland carriers, storekeepers | Accept suitable wood flow where there is demand; perform ordinary charcoal conversion; sell or deliver fuel | Wood charcoal | Fire-separated, ventilated, dry, connected to managed wood and forge demand; can close for fire risk, wet feedstock, smoke, or wood reservation |
| Rendering yard | Renderers and animal-processing workers | Receive legitimate suitable-fat flow through animal processing; render, store, and sell maintenance supply | Rendered tallow | Heat-safe and clean enough for stable output, separated from domestic congestion; can close for spoilage, contamination, fire, or absent feed |

| Shared field | Architecture |
|---|---|
| Purpose | Make unpleasant or risk-bearing transformations visible while using one bounded service pattern. |
| Access and stewardship | Processors may refuse unsuitable, undocumented, contaminated, or unsafe inputs. Water, fire, waste, neighbor, and household claims can constrain operation. |
| Why the player cares | Supplies eligible inputs, performs Leatherworking where supported, purchases output, routes valid flows, and sees how shortages propagate into equipment work. Textile work remains the baseline direct ordinary-labor conversion service. |
| Must not represent | New skills, three management games, automatic conversion from storage without a responsible processor, extra residue items without sinks, or supernatural waste behavior. |

## Family 6 — Market, receiving, storage, and craft network

| Required field | Architecture |
|---|---|
| Purpose | Join imported steel, ordinary supply, player goods, accessible storage, primary crafting, repair, and commission work through understandable civic and commercial interfaces. |
| Operator or custodian | Merchants, carriers, receiving clerks, market sellers, storekeepers, Smithing and Leatherworking workshops, crossing staff, and commission witnesses where later selected. |
| Logical actions | Receive and inspect consignments; buy and sell; deposit and withdraw; route appropriate textile commissions; craft from accessible storage; repair or refurbish equipment; inspect commission eligibility; respond to shortage notices. |
| Outputs or services | Plain carbon steel stock; circulation of all nine equipment-chain states plus ordinary wood; dependable baseline trade for normal lawful transferable goods; Smithing and Leatherworking work; item-level repair; aspirational commission access when earned. |
| Access and stewardship | Provenance, condition, household and civic priority, market access, storage capacity, trade disruption, workshop qualification, and story legitimacy. Exact tariffs and governance remain open. |
| Ecological or civic requirements | Safe receiving space, dry stores, fire separation, access to workshops and ordinary transport, visible accountability, and separation of suspicious war remains from routine stock. |
| Broad placement logic | Crestbridge-class receiving and trade contexts, Brookhollow-class markets, town or village repair clusters, household or civic stores, and other reconciled settlement classes. Exact assignments require map and content verification. **MAP VERIFICATION REQUIRED.** |
| Disruption or closure | Delayed consignments, route closure, damaged stores, disputed custody, contaminated stock, emergency reservation, workshop backlog, or story-specific market pressure. |
| Why the player cares | Enables buy, sell, storage crafting, repair, self-supply, and commissioned progression while making outside dependence legible. |
| Must not represent | A global auction house, frictionless continent-wide market, player-to-player dependency, exact constitutional authority, stock-market simulation, contraband as normal supply, or a single menu replacing the world. |

## Cross-family flow

```text
Hunting opportunities ── raw hide ──┐
                                    ├─→ tannery / player Leatherworking ─→ leather ─┐
Household husbandry ─── raw hide ───┘                                               │
                                                                                     ├─→ equipment + repair
Managed woodland ─── tannin-rich bark ──────────────────────────────────────────────┘

Household flax ─→ textile conversion ─→ linen + tow ────────────────────────────────→ equipment + repair

Managed woodland ─→ ordinary wood [inventory] ─→ bank / baseline trade / repair supply
                                             └─→ fuel yard ─→ charcoal ─┐
Imported steel receiving ────────────────→ steel ─────┴─→ Smithing + refurbishment

Hunting/husbandry suitable-fat flow ─→ rendering yard ─→ tallow ─→ finishing + maintenance

markets + storage + workshops connect every transferable state through baseline trade plus contextual specialist demand
```

The diagram shows relationships, not exact routes, quantities, or required co-location.

## Player interaction rhythm

1. **Observe:** Read habitat, woodland condition, household demand, processor status, and market supply.
2. **Choose:** Gather, buy, sell, commission conversion, use stored supply, or postpone work.
3. **Act:** Complete Hunting or Woodcutting, deliver source goods, use ordinary services, craft, or repair.
4. **Resolve:** Keep useful outputs, route them to processing, trade surplus, restore equipment, or preserve scarce inputs.
5. **Learn:** Improve routes, source judgment, preparation, recovery, fitting, and shortage response rather than simply unlocking a higher material.

This rhythm supports self-supply and market use without requiring either approach exclusively.

## Disruption architecture

Disruption should alter decisions and relationships rather than disable the economy arbitrarily.

| Disruption class | Likely effect | Healthy player response |
|---|---|---|
| Ecological pressure | Hunting opportunity or woodland work becomes restricted or changes context | Shift route, target another approved archetype, buy ordinary supply, or address the local condition later |
| Household shortage | Flax, hide, or rendering feed is retained locally | Sell useful supply, commission later, buy substitutes only where approved, or prioritize repair over new construction |
| Processing closure | Textile, tannery, fuel, or rendering service pauses | Use stored output, another ordinary supplier, player Leatherworking where applicable, or delay nonessential work |
| Trade interruption | Steel or imported supplement becomes scarce | Repair existing equipment, use stored stock, defer new hard construction, or respond to receiving needs without inventing local ore |
| Workshop backlog | Craft or repair access slows | Use field maintenance, choose another approved workshop class, or schedule commission work rather than abandon the item |
| Custody dispute | Stock cannot be accepted as ordinary supply | Establish legitimate provenance or reject the material; no supernatural shortcut validates it |

No disruption requires precise simulation of household inventories or autonomous prices. Content can express it through availability states, dialogue, visible work, requests, and service access.

## Progression relationship

- **Novice:** understands one local opportunity and one reliable supply route; sees why processing and repair exist.
- **Competent:** chooses between self-supply and ordinary purchase, recognizes access and output eligibility, and uses conversion services deliberately.
- **Advanced:** coordinates several routes or interfaces, responds to disruption, and values source condition, recovery, and maintenance.
- **Masterful:** anticipates competing claims, selects high-value work for purpose rather than rarity, and integrates storage, processing, trade, and repair efficiently.
- **Practical Mastery:** has broad freedom among the same six families and gains advantage through knowledge, preparation, custody, and relationship density rather than an additional tier of sources.

Exact levels and unlocks remain unselected.

## Provisional decisions for Creative Director review

| ID | Provisional recommendation | Alternative | Consequence |
|---|---|---|---|
| E01 | Use six world-facing families with variants | Separate every profession or material into a family | Six families preserve world logic with fewer bespoke interactions and assets. |
| E02 | Use direct commission for textile conversion; give normal lawful transferable goods a dependable baseline market outlet; keep tannery, fuel, rendering, and civic demand contextual | Make every conversion universally commissionable, or make all output specialist-only | This keeps ordinary labor legible and supply dependable without turning specialists into infinite premium sinks. |
| E03 | Express disruptions as authored availability states and visible local conditions | Continuous simulation | Authored states preserve consequence without building a management economy. |
| E04 | Let storage crafting draw transferable inputs while requiring the relevant workshop/service context | Allow all crafting from any storage screen | Workshop context keeps production grounded while avoiding inventory shuffling. Exact UI remains later design. |
| E05 | Treat processor variants as one service architecture but physically separate them where risks differ | Build a combined universal processing hall | Shared logic saves scope; distinct placement preserves water, fire, odor, and civic meaning. |

E02 and E04 have the largest implementation and player-experience consequences and should receive explicit morning review. None changes canon.

## Scope audit

| Check | Result | Finding |
|---|---|---|
| Approved materials and states | **STRONG** | Six equipment foundations and nine equipment-chain states remain unchanged; ordinary wood is one broader v1 inventory state. |
| Player actions | **STRONG** | Only approved Hunting and Woodcutting relationships gather equipment-chain inputs. |
| Ordinary-world credibility | **STRONG** | Households, processors, carriers, markets, stores, and workshops provide parallel supply without making the player irrelevant. |
| Interface count | **STRONG** | Six families and three process-yard variants cover all needs without one station per item. |
| Hidden skills | **STRONG** | No Farming, Textile, Rendering, Charcoal-making, Fabrication, or Adornment skill appears. |
| Map certainty | **PARTIAL BY DESIGN** | Placement classes are actionable; exact geography remains subject to map verification. |
| Management burden | **STRONG** | Disruptions and supply use authored states and services rather than continuous simulation. |
| Solo play | **STRONG** | Player can gather, buy, commission, store, craft, and repair without another player. |
| Lore limits | **STRONG** | No supernatural source, renewable war salvage, Founder claim, Volkhari supply, or governance invention is used. |

This document supplies the shared world-facing architecture used by the dedicated progression, placement, node, dependency, stress, and audit documents in this proposal pack.
