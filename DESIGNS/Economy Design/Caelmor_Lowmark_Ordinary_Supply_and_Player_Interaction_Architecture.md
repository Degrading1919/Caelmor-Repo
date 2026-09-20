# Caelmor — Lowmark Ordinary Supply and Player Interaction Architecture

**Status:** proposal-stage architecture for Creative Director audit. Decisions in this document are provisional unless already approved in the source material. This document defines how Lowmark's ordinary producers and player-facing economy coexist. It does not define prices, quantities, refresh rates, XP, action times, management simulation, exact routes or locations, final interfaces, schemas, or content data.

## Authority and boundaries

This proposal preserves the approved six-material foundation, nine equipment-chain inventory states, four player-facing recipe families, and gathering/output relationships.

- Player skills remain Smithing, Leatherworking, Hunting, and Woodcutting where already assigned. Cooking and Fletching receive no artificial dependency.
- Flax cultivation and textile work, husbandry, charcoal burning, rendering, and steel receiving remain ordinary labor rather than player skills.
- Ordinary tanners coexist with player Leatherworking.
- Lowmark receives conventional steel stock through trade. It does not gain an ore source or forced Mining loop.
- Hunting and Woodcutting remain optional ways to participate in useful supply, not mandatory sources for the whole region.
- Exact governance powers, map geometry, routes, prices, supply volumes, and S01 remain unresolved.

## 1. Selected interaction model

### Alternatives considered

| Model | Strength | Cost or risk | Provisional result |
|---|---|---|---|
| **Distributed civic economy** | Households, specialist yards, markets, stores, and craft workshops each expose the relationship they physically own. Short transactions make labor legible without simulating every worker. | Requires several recognizable interface families and clear signposting. | **SELECT** |
| **Single central exchange** | Lowest navigation and interface burden. | Makes Lowmark feel like a menu, hides dirty industries and household production, and weakens disruption and environmental storytelling. | **REJECT** |
| **Continuous production simulation** | Could show every input, worker, queue, and shipment. | Creates management play, balancing burden, fragile dependencies, and multiplayer-style market assumptions outside scope. | **REJECT** |

The selected model exposes a small number of **custody handoffs**. A player brings, buys, sells, commissions, stores, or repairs a good at the kind of place that can credibly perform that action. Background production continues without the player. Interfaces communicate current constraints through visible work, short notices, stock condition, and conversation rather than dashboards.

### Interaction verbs

| Verb | Meaning in this architecture | Boundary |
|---|---|---|
| **Gather** | Perform an approved Hunting or Woodcutting action in the world. | No ordinary profession becomes a gathering skill. |
| **Supply** | Deliver a valid good or routed output relationship to a worker, store, or market that can use it. | Supplying does not make the player manage production. |
| **Commission conversion** | Hand an accepted input to ordinary labor and receive or later collect the established output relationship. | No XP, minigame, or hidden crafting skill is implied. |
| **Purchase / sell** | Exchange represented goods through a suitable merchant or workshop. | Exact price and stock behavior remain later tuning. |
| **Store** | Place represented inventory states in accessible custody compatible with crafting from storage. | No new warehouse-management system. |
| **Craft / repair** | Use Smithing or Leatherworking through the four approved recipe families. | Workshop-only states remain internal. |
| **Respond** | Use another approved source, conserve supply, deliver an accepted input, or complete bounded civic work when a disruption affects access. | The player does not become regional production manager. |

## 2. Ordinary supply families

These families represent kinds of work and custody. They are not one world object per item and need not each receive a unique interface screen.

### Family A — Household produce and animal flow

**Covers:** flax bundles, husbandry-supplied raw hides, and suitable animal matter routed toward renderers.

| Question | Provisional design |
|---|---|
| Operators | Farm and animal-keeping households, seasonal helpers, ordinary animal processors, and carriers. |
| Player interaction | Purchase or sell household goods through markets or an appropriate household exchange; supply Hunting-derived raw hides; at recovery, route eligible game into the animal-processing handoff so edible use and rendering relationships remain visible without adding a carcass, fat, or hidden-token inventory state. |
| Output custody | Flax bundles and raw hides may enter inventory and trade. Suitable fat remains a routed relationship that processors can pass to renderers. |
| Constraints | Household needs, flood damage, season, animal health, preservation, storage, water scheduling, and food-versus-fiber pressure. |
| Why it matters | It prevents the player from becoming Lowmark's sole source of hides and makes textile supply originate in lived-in agricultural work. |
| Excludes | No Farming skill, livestock-management simulation, raw-fat inventory, finalized crop or animal catalog, or automatic raw hide from every animal. |

Household supply is background-stable rather than infinite. It supports baseline access, while player deliveries can matter during a bounded shortage or for immediate self-supply.

### Family B — Textile workroom

**Covers:** flax-bundle conversion into linen textile and flax tow.

| Question | Provisional design |
|---|---|
| Operators | Household spinners and weavers or a small shared specialist workroom. |
| Player interaction | Buy linen or tow, sell flax bundles, or commission the approved combined conversion of accepted flax bundles into both outputs. |
| Output relationship | Linen textile and flax tow are deterministic sibling outputs from one legitimate source flow. Exact proportions are deferred. |
| Constraints | Dry storage, clean working space, ordinary water, labor availability, household cloth demand, and disruption to flax supply. |
| Why it matters | It preserves the distinct physical roles of woven cloth and tow while avoiding a Textile skill and invisible source chain. |
| Excludes | No separate thread inventory, weaving minigame, player loom skill, padding package, lining kit, or choose-one conversion that falsely discards the other useful fraction. |

**Provisional choice:** a player may commission conversion because flax bundle is an approved inventory state whose transformation has two meaningful inventory outputs. The commission is an ordinary service, not player crafting.

### Family C — Tannery and leather exchange

**Covers:** ordinary leather supply alongside player Leatherworking.

| Question | Provisional design |
|---|---|
| Operators | Small tannery households or specialists placed away from domestic and memorial water, with waste and drying responsibilities. |
| Player interaction | Buy or sell raw hide, bark, or finished leather; craft leather personally through Leatherworking at an appropriate workspace; obtain repair inputs. |
| Supply relationship | Ordinary tanners release some vegetable-tanned leather to the market. Player Leatherworking remains the direct, controllable transformation path. |
| Constraints | Eligible hide condition, bark supply, water access, odor, waste handling, drying conditions, fire, storage, and downstream complaints. |
| Why it matters | The world can clothe and repair itself without the player, while Leatherworking retains value through control, immediacy, and equipment construction. |
| Excludes | No NPC conversion that automatically reproduces all benefits of skilled player Leatherworking, no leather grades masquerading as tiers, and no universal tallow cure for structural damage. |

**Provisional choice:** ordinary tanners primarily sell finished leather and buy valid inputs. A universal on-demand hide-to-leather service is not assumed. This avoids making Leatherworking a needless detour while still permitting a later bounded commission if access and delay create a real choice.

### Family D — Fuel yard

**Covers:** suitable wood flows converted into wood charcoal.

| Question | Provisional design |
|---|---|
| Operators | Fuel workers responsible for feedstock acceptance, drying, controlled conversion, fire safety, cooling, and storage. |
| Player interaction | Sell or deliver later-approved suitable wood relationships; purchase charcoal; respond to fuel shortage through lawful supply or conservation. |
| Output relationship | Accepted feedstock enters ordinary conversion and charcoal returns to market or workshop stores. Exact settlement and proportions are deferred. |
| Constraints | Stewardship permissions, structural-timber priority, drying, smoke, fire risk, household fuel competition, and secure dry storage. |
| Why it matters | Smithing fuel has visible labor and scarcity without adding Charcoal-making. Woodcutting can support the economy without becoming a charcoal recipe. |
| Excludes | No player charcoal skill, charcoal node, direct charcoal drop from cutting, or assumption that every wood output is suitable fuel feedstock. |

### Family E — Renderer and maintenance-goods flow

**Covers:** ordinary production of rendered tallow.

| Question | Provisional design |
|---|---|
| Operators | Renderers or animal processors working with controlled heat, cleanliness, waste handling, and storage. |
| Player interaction | Sell or deliver eligible game through an animal-processing handoff, purchase tallow, and use tallow through justified Leatherworking or Smithing maintenance. |
| Output relationship | Suitable fat is routed internally from eligible husbandry or game. Rendered tallow enters inventory only after ordinary conversion. |
| Constraints | Legitimate animal use, spoilage, cleanliness, heat, fire safety, household demand, and storage. |
| Why it matters | A perishable byproduct becomes a recurring maintenance good without adding a raw-fat item or Rendering skill. |
| Excludes | No gather-tallow action, fat loot requirement, Cooking dependency, or claim that all hunted animals yield suitable fat. |

**Provisional choice:** routed fat is settled as part of the sale or delivery of eligible game rather than tracked by a hidden player token. Tallow is later purchased as an ordinary good. This keeps the causal relationship visible without inventing an inventory state.

### Family F — Imported steel receiving

**Covers:** lawful receipt, inspection, storage, and circulation of plain carbon steel stock.

| Question | Provisional design |
|---|---|
| Operators | Merchants, carriers, receiving workers, market factors, repair smiths, and civic custodians where public demand applies. |
| Player interaction | Purchase or sell accepted stock, collect a lawful workshop order, place stock in storage, use it through Smithing, or respond to interrupted consignments through repair and conservation. |
| Supply relationship | Conventional stock enters from external production through broad trade. More than one supplier may exist; exact origin shares and routes remain open. |
| Constraints | Consignment condition, provenance, transport disruption, storage security, fuel availability, public repair claims, and workshop inspection. |
| Why it matters | It makes Lowmark's material dependence legible and gives trade disruption consequences without inventing local ore. |
| Excludes | No Lowmark Mining node, routine Great War salvage supply, superior-metal ladder, exact route, or stock-form catalog. |

Great War remains, memorial objects, and evidentiary material never enter routine receiving merely because they contain metal.

## 3. Shared exchange and service interfaces

### Market and receiving area

The market aggregates household output, imported stock, and finished ordinary goods. It supports buying and selling; it does not perform every conversion. Steel consignments may be received near this area, while dirty or fire-risk processes remain physically separate.

The market should show dependence through signs of custody: bundled household goods, inspected consignments, repair demand, posted shortages, and carriers waiting on work. These are presentation cues, not a commodity simulation.

### Craft and repair workshops

Smithing and Leatherworking workshops provide the four approved player-facing recipe families and receive materials from accessible storage. They may use ordinary specialist labor for physically necessary mixed-material fitting without creating Fabrication, Adornment, Textile, or another skill.

The player's primary interactions are:

- construct through Smithing or Leatherworking;
- prepare leather through Leatherworking;
- repair or refurbish with appropriate represented states;
- purchase ordinary inputs where supplied;
- place an aspirational commission once its acquisition and craft requirements are met.

Commission fitting, inspection, custody, and provenance remain qualifications and workshop work. They are never consumable components.

### Storage and custody

All nine equipment-chain inventory states can pass through ordinary storage suited to their broad condition. Crafting from accessible storage remains required. The architecture does not yet impose spoilage, bulk, warehouse fees, or separate container simulation.

Storage has three design purposes:

1. preserve the short production chains;
2. let gathering, trade, and crafting occur in different sessions without work-in-progress clutter; and
3. allow a player to prepare for a known shortage or repair need without turning stockpiling into a management game.

Raw-hide condition and fuel dryness are physically relevant, but their exact mechanical representation remains deferred. They must not generate extra item identities merely to prove that handling occurred.

## 4. Player participation map

| Relationship | Gather | Supply | Commission ordinary conversion | Purchase / sell | Store | Craft / repair | Respond to disruption |
|---|---:|---:|---:|---:|---:|---:|---:|
| Eligible game and raw hide | Yes, Hunting | Yes | No required NPC conversion | Yes | Raw hide only | Leatherworking after acquisition | Hunt eligible game or rely on husbandry/trade |
| Household husbandry | No player skill | Via accepted market flow | No | Yes | Raw hide where represented | Leatherworking may use purchased hide | Shift between ordinary and hunted supply |
| Flax and textile work | No Farming | Flax bundle | Yes, bundle to linen plus tow | Yes | Yes | Leatherworking integrates outputs | Use held goods, alternate ordinary supply, or await recovery |
| Tanning | Bark/hide come from approved sources | Yes | Not universal; decision deferred | Yes | Yes | Leatherworking owns player conversion and flexible repair | Craft personally, buy leather, or conserve |
| Fuel work | Woodcutting may feed accepted wood | Yes | Ordinary service/exchange form deferred | Buy charcoal; sell accepted wood | Charcoal | Smithing consumes charcoal | Deliver eligible wood, use trade supply, prioritize repairs |
| Rendering | No direct gathering | Eligible animal delivery routes fat | Internal ordinary conversion | Buy tallow | Tallow | Justified maintenance only | Rely on husbandry, eligible game, or trade |
| Imported steel | No Lowmark gathering | Accepted trade stock only | No | Yes | Yes | Smithing construction/refurbishment | Repair, conserve, or wait for lawful supply |
| Finished equipment | No | No | Aspirational commission is craft service | Later trade rules deferred | Equipment storage | Smithing or Leatherworking | Maintain existing equipment instead of requiring new stock |

## 5. Shortage and disruption response

### Selected model: bounded world states

Supply disruptions should be authored or selected from a small bounded set rather than simulated continuously. A disruption changes one or more visible relationships for a limited context: availability, workshop acceptance, conversion access, or civic priority. It does not require the player to balance regional ledgers.

| Disruption class | World-facing cause | Player response set | What remains protected |
|---|---|---|---|
| Imported stock interruption | Delayed or rejected lawful consignment | Maintain or refurbish current equipment, use stored stock, complete bounded receiving assistance, or wait for alternate ordinary supply | No emergency Lowmark ore or war-salvage farming |
| Woodland restriction | Bank instability, fire risk, public repair priority, or source recovery | Work an open managed opportunity, deliver already-held eligible supply, buy ordinary stock, or defer consumption | Bark remains a co-output; closed sources cannot be bypassed through bark-only stripping |
| Flax or textile shortage | Flood loss, household need, storage damage, or labor diversion | Use stored textile, purchase imported or recovered ordinary supply if offered, or delay nonessential work | No Farming or Textile skill appears as a workaround |
| Tannery restriction | Water, waste, odor, drying, or public-health problem | Use player Leatherworking where an appropriate safe workspace exists, buy held leather, or help restore lawful operation | Dirty processing does not move beside protected domestic or memorial water for convenience |
| Animal-flow shortage | Household need, animal health, season, or poor game recovery | Hunt eligible game within stewardship rules, buy held supply, repair instead of replace, or wait | Raw hide remains non-universal; hunting does not become forced ecological overharvest |
| Fuel constraint | Structural-wood priority, wet feedstock, fire closure, or household heat demand | Use held charcoal, supply accepted wood, prioritize refurbishment, or wait for trade | Players do not gain direct charcoal manufacture |
| Workshop overload | Civic repair demand after damage | Use another appropriate workshop if supported, defer commission, supply inputs, or prioritize maintenance | No queue-management simulation or purchase of priority through an invented token |

Shortages should create understandable choices, local stories, and temporary value shifts. They should not routinely block basic participation or make hoarding the only rational response.

## 6. Coexistence safeguards

### Ordinary supply must not invalidate player activity

- Player Hunting offers direct control over an eligible hide source and contributes to future food and rendering relationships.
- Player Woodcutting offers direct access to ordinary wood relationships and qualified bark co-output under stewardship.
- Player Leatherworking controls personal hide preparation, equipment construction, and flexible repair.
- Player Smithing controls hard equipment construction and refurbishment.
- Ordinary suppliers provide continuity and convenience, but they do not perform player mastery, aspirational qualification, or all construction on demand.

### Player supply must not invalidate the world

- Husbandry remains the regular ordinary context for hides and rendering feedstock.
- Households produce flax without waiting for the player.
- Tanners, textile workers, fuel workers, renderers, carriers, and merchants remain economically active.
- Imported steel enters through lawful trade independently of player gathering.
- Civic repair and household consumption create claims on supply beyond the player's equipment.

### Anti-chore rule

No path requires the player to gather every input personally. Buying, ordinary conversion, storage, personal processing, and selective self-supply are legitimate styles. A player chooses gathering because it provides control, discovery, useful output bundles, or trade value, not because NPC society stops functioning.

## 7. Solo-development scope controls

The architecture needs a small set of reusable interaction patterns:

1. buy or sell represented goods;
2. deliver an accepted source relationship;
3. commission one established ordinary conversion;
4. craft or repair at the correct workshop;
5. store and retrieve approved inventory states;
6. read a bounded closure, shortage, or priority state.

The same patterns can serve multiple workers and settlements through context and presentation. The design does not require worker schedules, simulated transport, live regional prices, production queues, spoilage clocks, business ownership, or settlement management.

## 8. Redundancy and hidden-skill audit

| Candidate feature | Finding | Decision |
|---|---|---|
| Separate vendor for each represented item | One-object-per-item thinking; unnecessary interface burden | **REJECT** |
| Player flax cultivation | Would invent Farming to fill a supply chain already grounded in households | **REJECT** |
| Player textile production | Would introduce a hidden Textile skill and extra WIP states | **REJECT** |
| Player charcoal production | Would add a new skill-shaped conversion without a demonstrated need | **REJECT** |
| Player tallow rendering | Would add Rendering or force Cooking into an equipment chain | **REJECT** |
| Universal NPC tanning service | Risks erasing player Leatherworking's transformation value | **DEFER; ordinary market leather is sufficient** |
| Central all-purpose economy counter | Efficient but erases labor, placement, and civic consequences | **REJECT** |
| Continuous supply simulation | High implementation and tuning burden with little mastery payoff | **REJECT** |
| Textile commission | Exposes a meaningful one-to-two output conversion without a new skill | **KEEP** |
| Wood-to-fuel-yard delivery | Connects Woodcutting to ordinary fuel work without direct charcoal crafting | **KEEP AS RELATIONSHIP; exact settlement deferred** |
| Eligible-game delivery to processors | Preserves food and rendering relationships without extra inventory states | **KEEP** |

No additional material, skill, or equipment-chain inventory state is required by this architecture.

## 9. Provisional decisions and morning review

### Provisional selections

1. Use a distributed civic economy with a few reusable custody-handoff interactions.
2. Allow ordinary textile conversion to be commissioned because both linen and tow are represented and useful.
3. Let ordinary tanners supply finished leather, but do not assume a universal on-demand conversion service.
4. Settle suitable game byproducts inside the animal-processing handoff; do not create a fat item or hidden token.
5. Use bounded authored supply disruptions rather than continuous simulation.
6. Keep storage mechanically simple while preserving crafting from accessible storage.

### Genuine Creative Director review items

1. **Disruption cadence:** approve bounded authored/state-based shortages as occasional world texture and player opportunity, or restrict disruptions to explicitly authored story moments. This affects systemic content burden, not lore truth.
2. **Ordinary conversion presentation:** approve direct service commissions for textile conversion and a simple sale/delivery relationship for fuel and rendering, or keep every ordinary conversion wholly market-mediated. The recommendation preserves textile clarity while avoiding pseudo-skills for charcoal and tallow.
3. **NPC tanning boundary:** confirm that ordinary tanners sell finished leather without providing unrestricted player-input conversion. This preserves Leatherworking's transformation identity while keeping the world self-sufficient.

All exact exchange values, settlement methods, stock behavior, and interfaces remain later production and balance decisions.

## Architecture result

Lowmark can represent household flax and husbandry, textile conversion, ordinary tanning, charcoal work, rendering, imported steel receiving, markets, workshops, and storage through a compact set of credible labor and custody relationships. The player can gather, supply, commission, purchase, sell, store, craft, repair, and respond to disruption without managing businesses or training hidden skills. Ordinary society remains functional, while Hunting, Woodcutting, Smithing, and Leatherworking retain distinct reasons to matter.
