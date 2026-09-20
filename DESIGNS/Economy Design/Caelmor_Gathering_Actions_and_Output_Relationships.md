# Caelmor — Gathering Actions and Output Relationships

**Status:** proposal-stage source and supply model following Creative Director approval of Option A. This document defines logical actions and output relationships before world-node design. It does not define exact materials beyond the approved equipment chain, species, cuts, recipes, quantities, XP, action times, success rates, tool tiers, levels, node types, locations, respawn, prices, drop tables, schemas, or JSON.

## Authority and boundaries

This proposal works from the approved processing and recipe structure, minimum coherent material set, Lore Foundation Lock, regional source/process foundations, and approved noncombat skill direction.

The governing chain is:

```text
WORLD SOURCE
→ LOGICAL GATHERING OR SUPPLY ACTION
→ ONE OR MORE OUTPUT RELATIONSHIPS
→ INVENTORY STATE OR TRADE FLOW
```

- Hunting and Woodcutting are the only approved player gathering skills connected to this equipment-chain pass.
- The connection is justified by actual outputs. Neither skill is included merely to increase interconnection.
- Plain carbon steel stock remains imported. Lowmark receives no ore node or forced Mining loop.
- Flax cultivation remains ordinary Lowmark agricultural labor. No Farming skill is introduced.
- Flax processing, charcoal production, and tallow rendering remain ordinary-labor conversions rather than player skills.
- Raw hide and tannin-rich bark are source-conditional guaranteed outputs, never weighted random drops.
- Hunting must have an edible-output relationship as well as a hide relationship. This pass does not create a meat catalog.
- Ordinary wood is a relationship placeholder outside the current equipment-chain state list. This pass does not select wood species, lumber items, Fletching materials, fuel quantities, or nodes.
- S01 remains deferred. No ranged gathering demand is inferred.

## Output relationship vocabulary

| Relationship type | Meaning in this proposal |
|---|---|
| **Guaranteed direct output** | The logical action produces the output whenever the action completes validly. Amount remains later tuning. |
| **Source-conditional guaranteed output** | The output is guaranteed when the selected source and recovery conditions qualify; an ineligible source never rolls for it. |
| **Deterministic co-output** | A valid action produces the co-output alongside its primary relationship because the source physically contains both. It is not a rare bonus roll. |
| **Ordinary-labor conversion output** | Households or specialist workers transform an input flow into a represented inventory good outside a player skill. |
| **Imported trade supply** | A represented state enters Lowmark through merchants, carriers, markets, or receiving workshops rather than a local player gathering action. |
| **Mixed supply** | Player action and ordinary labor or trade both provide legitimate supply without making either source universal. |

No weighted random relationship is required for the nine equipment-chain states. Later variation may affect condition, access, or amount only if separately approved; it must not turn a physically eligible core output into a lottery.

## 1. Player-gathered versus ordinary-supply matrix

| Represented state | Source category | Supply classification | Player skill, if any | Logical action or supply relationship | Output rule |
|---|---|---|---|---|---|
| **Plain carbon steel stock** | Conventional outside metal production | Imported trade supply | None in Lowmark | Receive, inspect, and circulate conventional stock through markets and workshops | Guaranteed delivered good when a lawful consignment arrives; no ore or random salvage roll |
| **Raw hide** | Eligible hide-bearing game; ordinary husbandry and animal processing | Mixed supply | Hunting for the game source | Hunt and field-dress eligible game; ordinary households process legitimate livestock flows | Source-conditional guaranteed from eligible animals under successful recovery conditions |
| **Vegetable-tanned leather** | Processed raw hide | Player processing plus ordinary workshop or trade supply | Leatherworking | Transform raw hide with tannin-rich bark; ordinary tanners may also supply finished leather | Guaranteed processing output when a valid tanning operation completes; no gathering drop |
| **Flax bundle** | Cultivated Lowmark fiber crop | Ordinary-labor supply | None | Household cultivation, harvest, drying, and bundling | Guaranteed agricultural output from a valid harvest relationship; no Farming skill |
| **Flax tow** | Flax-bundle processing | Ordinary-labor conversion | None | Household or specialist fiber preparation | Deterministic co-output with linen from the same source flow; proportions deferred |
| **Linen textile** | Flax-bundle processing | Ordinary-labor conversion | None | Household or specialist spinning and weaving | Deterministic output from the same conversion flow that also yields useful tow |
| **Tannin-rich bark** | Eligible managed woodland work | Mixed supply | Woodcutting for player source | Stewardship-approved selective harvest, pruning, or yard recovery; ordinary forestry may also supply it | Source-conditional guaranteed co-output when the selected source and action yield usable bark |
| **Wood charcoal** | Suitable wood flows converted by fuel workers | Ordinary-labor conversion and trade | None for conversion | Fuel workers dry and convert suitable wood supplied by player, household, civic, or trade flows | Guaranteed conversion output from accepted feedstock; no player Charcoal-making recipe |
| **Rendered tallow** | Legitimate animal-processing flows | Ordinary-labor conversion and trade | None for conversion | Renderers process suitable fat from husbandry, ordinary animal processing, and eligible delivered game | Guaranteed conversion output from accepted feedstock; never gathered directly |

This matrix governs the equipment chain only. It neither approves nor prohibits other future goods from Hunting, Woodcutting, husbandry, food production, or trade.

## 2. Logical gathering and supply actions

### Player action A — Hunt and field-dress eligible game

| Required field | Approved relationship |
|---|---|
| Source category | Living game that later ecology and content design establish as huntable. Eligibility for hide, food, or suitable fat depends on the animal and its recovered condition. |
| Supply classification | Player-gathered, with ordinary husbandry remaining an alternate source for animal materials. |
| Responsible skill | Hunting. |
| Logical action | Locate or pursue suitable game, complete the hunt, and field-dress the animal sufficiently to recover useful outputs. Exact encounter, tool, timing, and interaction structure remain later design. |
| Primary output relationship | A usable animal-output bundle with an edible relationship for Cooking where the animal and condition qualify. No meat item or cut is named here. |
| Equipment-chain output | Raw hide is a source-conditional guaranteed output from eligible hide-bearing animals under successful recovery conditions. |
| Secondary or routed output | Suitable fat may enter an ordinary renderer's supply flow. It does not become a required player inventory state in this equipment chain. |
| Output classification | Guaranteed or source-conditional guaranteed. No weighted hide chance, rare fat roll, or universal hide output. |
| Stewardship and access | Later design must respect eligible game, local access, season or population pressure where supported, ownership, and the Lowmark principle that use should not become waste. Exact authority remains open. |
| Economic purpose | Supplies Leatherworking, supports a future Cooking relationship, contributes to ordinary rendering, and gives Hunting value through a useful output bundle. |
| Processing destination | Raw hide goes to player or ordinary Leatherworking; edible output goes toward later Cooking design; suitable fat enters ordinary rendering where accepted. |
| Meaning without XP | Yes. The action produces useful and tradable relationships for equipment, food, and maintenance supply. |
| Why separate | Hunting is the approved player source of intact biological structure. Field recovery creates decisions and outputs distinct from household husbandry without making hide its sole purpose. |

### Player action B — Stewardship-approved selective harvest

| Required field | Approved relationship |
|---|---|
| Source category | Managed woodland sources approved for selective cutting, pruning, coppice-like renewal where later supported, or yard recovery from legitimate woodland work. No species or node form is selected. |
| Supply classification | Player-gathered Woodcutting plus ordinary forestry supply. |
| Responsible skill | Woodcutting. |
| Logical action | Carry out an approved selective harvest that produces usable wood while respecting bank stability, future repair stock, source health, fire risk, and community claims. |
| Primary output relationship | Ordinary wood outside the current equipment-chain catalog. Its later forms and uses require their own design pass. |
| Equipment-chain co-output | Tannin-rich bark is source-conditionally guaranteed when the eligible source and approved action physically produce usable bark. |
| Secondary routed relationship | Suitable player-supplied wood may be sold or delivered into the ordinary fuel-worker flow that produces charcoal. The player does not convert it directly in this pass. |
| Output classification | Wood is the guaranteed primary relationship of valid harvest. Bark is a deterministic co-output only for qualifying source/action combinations. It is never a weighted bonus. |
| Stewardship and access | Bank protection, woodland health, public repair needs, land or household custody, fire conditions, and closure decisions can permit, restrict, or redirect harvest. Exact jurisdiction and sites remain open. |
| Economic purpose | Supplies later wood uses, sustains tanning input without a bark-only grind, and can feed the ordinary charcoal economy through trade. |
| Processing destination | Ordinary wood enters future woodworking, fuel, repair, or trade relationships; bark enters Leatherworking; accepted wood flow reaches fuel workers. |
| Meaning without XP | Yes. Wood has wider future uses and trade value, bark sustains leather production, and stewardship changes which work is responsible or available. |
| Why separate | Selective Woodcutting is an approved skill relationship with broad physical value. Bark remains attached to legitimate woodland work rather than becoming an artificial standalone resource. |

### Ordinary supply A — Receive conventional steel stock

| Required field | Approved relationship |
|---|---|
| Source category | Conventional metal stock produced outside Lowmark's incomplete metal base. |
| Supply classification | Imported trade supply. |
| Responsible skill | None for supply. Smithing begins when the stock is used. |
| Logical supply action | Merchants, carriers, markets, and workshops receive and inspect a lawful consignment. Exact supplier, route, stock form, and volume remain open. |
| Primary output | Plain carbon steel stock. |
| Output classification | Guaranteed consignment output when delivery is completed and accepted. No Mining roll, local ore node, or routine battlefield salvage. |
| Stewardship and access | Provenance, condition, transport disruption, civic demand, and workshop acceptance govern circulation. War remains and sealed-site material require separate custody. |
| Economic purpose | Creates Lowmark's intentional metal dependency and a recurring trade and repair pressure. |
| Processing destination | Smithing construction and hard refurbishment. |
| Meaning without XP | Yes. Access to conventional stock controls equipment production and repair. |
| Why separate | Lowmark's repair culture needs metal but its lore does not support a complete local ore chain. Import dependence is a world relationship, not a missing gathering action. |

### Ordinary supply B — Cultivate and bundle flax

| Required field | Approved relationship |
|---|---|
| Source category | Lowmark household fiber cultivation on suitable agricultural ground. |
| Supply classification | Ordinary household production, with trade able to supplement shortage. |
| Responsible skill | No player Farming skill. |
| Logical supply action | Households cultivate, harvest, dry, and bundle flax through ordinary agricultural labor. |
| Primary output | Flax bundle. |
| Output classification | Guaranteed agricultural output from a valid harvest flow. Exact harvest conditions and amount remain outside this pass. |
| Stewardship and access | Land use, household labor, water scheduling, crop rotation or equivalent care, storage, flood risk, and food-versus-fiber pressure constrain supply without creating a new skill. |
| Economic purpose | Feeds linen and tow supply while connecting equipment to Lowmark households and agriculture. |
| Processing destination | Household or specialist textile labor. |
| Meaning without XP | Yes. It supports clothing, repair, padding, and trade even though it is not a player gathering loop. |
| Why separate | Flax is cultivated rather than plausibly gathered through Foraging. Ordinary production preserves Lowmark's agricultural identity without inventing Farming. |

### Ordinary supply C — Process flax into linen and tow

| Required field | Approved relationship |
|---|---|
| Source category | Flax bundles from household cultivation or trade. |
| Supply classification | Economy-visible ordinary-labor conversion. |
| Responsible skill | No new Textile or Weaving skill. Leatherworking begins when the outputs enter equipment work. |
| Logical supply action | Households or specialists prepare fiber, retain useful tow, spin suitable long fiber, and weave linen. Intermediate fiber and thread remain workshop-internal. |
| Primary output | Linen textile. |
| Co-output | Flax tow. |
| Output classification | Both are deterministic outputs of the same accepted source flow. Exact proportions remain future tuning; tow is not a rare byproduct. |
| Stewardship and access | Clean water, drying space, household labor, fire and pest safety, and competing cloth needs constrain conversion. |
| Economic purpose | Supplies distinct lining, joining, repair, damping, and padding functions from one crop foundation. |
| Processing destination | Leatherworking construction and repairs; other economy uses remain future work. |
| Meaning without XP | Yes. Both outputs have independent uses, storage value, and trade demand. |
| Why separate | Linen and tow perform materially different functions and prevent one abstract textile item from hiding real production choices. |

### Ordinary supply D — Convert suitable wood flow into charcoal

| Required field | Approved relationship |
|---|---|
| Source category | Stewardship-approved wood supplied through player Woodcutting, ordinary forestry, civic work, offcuts, or trade where later justified. |
| Supply classification | Economy-visible ordinary-labor conversion. |
| Responsible skill | No player Charcoal-making skill. Smithing consumes the output. |
| Logical supply action | Fuel workers accept suitable feedstock, dry it, convert it under controlled conditions, cool it safely, and release charcoal to stores or workshops. |
| Primary output | Wood charcoal. |
| Output classification | Guaranteed conversion output from accepted feedstock. Ash, fines, and failed fuel are not equipment inventory outputs. |
| Stewardship and access | Woodland permissions, structural-stock priority, household fuel demand, drying, fire control, smoke, and safe storage constrain supply. |
| Economic purpose | Makes Smithing heat and refurbishment depend on visible labor and managed woodland flows. |
| Processing destination | Smithing construction and hard refurbishment. |
| Meaning without XP | Yes. Charcoal is a persistent fuel sink with trade value and supply risk. |
| Why separate | Fuel conversion is economically important but does not contain enough distinct player decision-making to justify a new skill in this equipment chain. |

### Ordinary supply E — Render legitimate animal-processing flow

| Required field | Approved relationship |
|---|---|
| Source category | Suitable fat from husbandry, ordinary animal processing, or eligible game delivered into a renderer's flow. |
| Supply classification | Economy-visible ordinary-labor conversion. |
| Responsible skill | No player Rendering skill and no forced Cooking requirement. Leatherworking or Smithing consumes the output where justified. |
| Logical supply action | Renderers accept suitable material, clean, heat, strain, cool, store, and distribute stable tallow. |
| Primary output | Rendered tallow. |
| Output classification | Guaranteed conversion output from accepted suitable feedstock. The player never performs a “gather tallow” action. |
| Stewardship and access | Legitimate animal use, cleanliness, spoilage, rendering heat, fire safety, storage, and household competition constrain supply. |
| Economic purpose | Supports leather conditioning, thread preparation, bounded steel care, and continuing equipment maintenance. |
| Processing destination | Leatherworking finishing and repair; justified Smithing surface care; market maintenance supply. |
| Meaning without XP | Yes. Tallow has repeated equipment sinks and household economic context. |
| Why separate | Rendering stabilizes a legitimate byproduct into a useful maintenance good without creating another player production loop. |

### Ordinary supply F — Tan leather outside player production

| Required field | Approved relationship |
|---|---|
| Source category | Raw hides and tannin-rich bark held by ordinary tanning households or specialists. |
| Supply classification | Ordinary workshop and trade supply alongside player Leatherworking. |
| Responsible skill | Leatherworking owns the player transformation; ordinary NPC labor can supply the market. |
| Logical supply action | Prepare and tan valid hides using the approved ordinary process, then release finished leather through workshops or markets. |
| Primary output | Vegetable-tanned leather. |
| Output classification | Guaranteed processing output from an accepted operation; quality tiers and quantities remain unselected. |
| Stewardship and access | Water use, waste placement, odor, drying space, labor, and source legitimacy constrain production. |
| Economic purpose | Ensures leather exists in the wider economy and keeps a player from being the world's sole processor. |
| Processing destination | Leatherworking equipment construction, mixed workshop use, and repairs. |
| Meaning without XP | Yes. It is a necessary trade good and repair input. |
| Why separate | Player transformation and ordinary supply may coexist where the world already supports both, preserving player agency without making the economy implausibly dependent on the player. |

### Ordinary supply G — Husbandry and animal processing

| Required field | Approved relationship |
|---|---|
| Source category | Ordinary livestock and animal-processing relationships already supported by Lowmark. |
| Supply classification | Ordinary-labor supply, supplemented by imports where needed. |
| Responsible skill | No new Husbandry or Farming skill is introduced by this equipment pass. |
| Logical supply action | Legitimate household animal use produces hides for tanning and routes suitable fat toward renderers rather than wasting it. |
| Primary equipment-chain output | Raw hide. |
| Routed output | Suitable fat enters the ordinary rendering flow and later returns as rendered tallow. |
| Output classification | Guaranteed or source-conditional according to the animal and legitimate processing event; no random drop table is implied. |
| Stewardship and access | Ownership, animal health, season, household need, food use, waste control, and market claims govern supply. |
| Economic purpose | Provides a stable alternate hide source and the main ordinary context for tallow without making Hunting universal or mandatory. |
| Processing destination | Raw hide goes to player or ordinary tanners; suitable fat goes to renderers. |
| Meaning without XP | Yes. The relationship supports food, household continuity, leather, maintenance, and trade. |
| Why separate | Husbandry explains regular supply while Hunting remains a meaningful but non-universal player source. |

## 3. Multi-output relationships

### Approved multi-output map

| Source/action | Primary relationship | Co-output or routed relationship | Rule |
|---|---|---|---|
| Eligible game hunt and field dressing | Edible-output relationship where qualified | Raw hide from eligible hide-bearing game; suitable fat routed to renderers | Source-conditional guaranteed; no weighted rare outputs |
| Stewardship-approved selective harvest | Ordinary wood relationship | Tannin-rich bark from eligible source/action; suitable wood may enter fuel-worker supply | Bark is deterministic when qualified; never a separate roll or grind |
| Ordinary flax processing | Linen textile | Flax tow | Both arise from the same source flow; proportions deferred |
| Household animal processing | Raw hide where qualified | Suitable fat routed to renderers | Source-conditional ordinary supply |

### Multi-output rules

1. A co-output must follow from the physical source, not from a desire to add reward variety.
2. No listed co-output exists only to grant XP.
3. A source that cannot physically provide an output never rolls for it.
4. Eligibility is readable through source category, permitted action, and recovery condition rather than hidden rarity.
5. An output without an approved sink remains outside the catalog even if real-world processing could produce it.
6. A routed output can enter ordinary labor without becoming a required player inventory state.
7. Future tuning may adjust amounts, but it may not convert bark or raw hide into weighted jackpot drops.

## 4. Hunting output architecture

### Purpose

Hunting supplies intact biological structure while also supporting food and ordinary byproduct use. It does not exist merely to feed Leatherworking.

### Eligibility layers

| Layer | Required question |
|---|---|
| Target eligibility | Is the animal approved as huntable, and does its ecology support player hunting? |
| Output eligibility | Is it hide-bearing, suitable for an edible-output relationship, or capable of providing suitable fat? These properties are not universal. |
| Recovery eligibility | Was the hunt and field recovery completed in a condition that leaves the relevant output usable? Exact mechanics remain later design. |
| Access eligibility | Is the hunt permitted by local stewardship, ownership, seasonal pressure, or story access? Exact rules remain open. |

### Output architecture

```text
eligible game
→ Hunting action and successful field recovery
→ edible-output relationship where qualified
+ raw hide where hide-bearing and recoverable
+ suitable fat routed to ordinary rendering where present and accepted
```

- Raw hide is not universal across animals, enemy categories, or combat kills.
- The edible output remains a relationship only. No meat item, cut, dish, or Cooking recipe is approved here.
- Suitable fat remains a routed ordinary-labor relationship. It is not added to the nine equipment inventory states.
- Horns, bones, sinew, organs, trophies, glands, and other possible outputs remain excluded until a later system proves several meaningful sinks or a necessary specialist purpose.
- A hunt remains valuable without XP because it connects food, Leatherworking, trade, and ordinary maintenance supply.
- Husbandry provides alternate regular supply so equipment progression does not require ecologically implausible hunting volume.

### Anti-grind boundary

Hunting progression must later change route knowledge, animal behavior, preparation, risk, recovery decisions, or output value. It cannot become the same stationary action repeated against reskinned animals solely for higher hide yield.

## 5. Woodcutting and bark relationship

### Approved relationship

```text
eligible managed woodland source
→ stewardship-approved selective harvest
→ ordinary wood relationship
+ tannin-rich bark when source/action qualifies
→ optional delivery of suitable wood flow to ordinary fuel workers
→ wood charcoal trade supply
```

### Bark rules

- Bark is a co-output of legitimate woodland work.
- There is no bark-stripping skill action, bark-only node, or bark route detached from useful wood work.
- Bark is guaranteed when the selected source and approved action physically provide usable tanning bark.
- Ineligible sources and actions provide no bark and do not roll for it.
- Later tuning must preserve the co-output relationship. Scarcity may arise from stewardship, eligible sources, closures, competing work, and supply demand rather than a low random chance.
- Ordinary forestry and yard recovery may also supply bark, so the player is neither the sole source nor forced to harvest beyond responsible woodland need.

### Wood and charcoal rules

- Ordinary wood remains outside the current equipment-chain state list because its species, forms, and wider uses require their own design.
- Player Woodcutting may feed suitable wood into fuel-worker stores through sale, delivery, or another ordinary exchange interface chosen later.
- Fuel workers, not the player skill, perform charcoal conversion.
- The conversion may accept ordinary forestry, civic, yard, or imported wood flows as well as player supply.
- Structural stock, protected bankside growth, or scarce repair wood is not automatically valid fuel feedstock.
- No charcoal recipe, new skill, or direct charcoal output is awarded by Woodcutting.

### Anti-grind boundary

Woodcutting must remain useful because ordinary wood serves real construction, repair, Fletching where later approved, trade, and fuel relationships. Bark cannot become the dominant reason to repeat a nominally different harvest action.

## 6. Flax, steel, charcoal, tallow, and related supply relationships

### Flax

- Lowmark households cultivate and harvest flax through ordinary agricultural work.
- The player does not receive a Farming skill from this relationship.
- Flax bundle enters markets, household stores, or textile conversion.
- Textile labor produces linen and tow from the same source flow.
- Exact proportions, labor time, loss, and market interface remain future tuning.
- Foraging does not gather wild flax merely to create a player loop.

### Steel

- Plain carbon steel stock remains imported conventional supply.
- Lowmark markets and workshops receive it through broad Thornfell, Emberholt, or other ordinary trade relationships without fixing source share or route.
- No local ore body, Mining action, battlefield harvesting loop, or salvage node is created.
- Civilian reuse may later return inspected sound material to stock, but Great War evidence and memorial matter remain outside routine supply.

### Charcoal

- Fuel workers convert accepted wood flow into inventory-represented charcoal.
- Player Woodcutting can contribute feedstock economically without becoming a conversion skill.
- Charcoal also may arrive through trade, preserving supply during local closures.
- Ash, fines, and failed fuel do not receive inventory identities without demonstrated sinks.

### Tallow

- Renderers convert accepted animal-processing flow into inventory-represented tallow.
- Husbandry is the stable ordinary source context; eligible game may contribute suitable fat after delivery.
- Players do not gather fat or tallow as required equipment-chain inventory states.
- Tallow remains useful through Leatherworking finishing, maintenance, and bounded Smithing care rather than becoming a food or alchemical item by implication.

### Leather

- Player Leatherworking converts raw hide and bark into leather under the approved recipe family.
- Ordinary tanners also supply the market.
- Leather is processed output, not a gathered drop.
- Dual supply prevents the player from becoming the only tannery while preserving Leatherworking as a meaningful transformation.

## 7. Processing destinations

| Source or supply output | Immediate destination | Later equipment destination |
|---|---|---|
| Plain carbon steel stock | Market, receiving workshop, or storage | Smith-led construction and hard refurbishment |
| Hunting-supplied raw hide | Player or ordinary tanning custody | Vegetable-tanned leather, then flexible construction or repair |
| Husbandry-supplied raw hide | Household, market, player, or ordinary tanning custody | Vegetable-tanned leather, then flexible construction or repair |
| Vegetable-tanned leather | Market, workshop, or storage | Leather-led construction, mixed construction, and flexible repair |
| Flax bundle | Household or specialist textile conversion | Linen and tow supply |
| Flax tow | Market, workshop, or storage | Damping, padding, and padding repair |
| Linen textile | Market, workshop, or storage | Lining, joining, wrapping, and repair |
| Tannin-rich bark | Leatherworking or ordinary tannery | Hide-to-leather conversion |
| Suitable ordinary wood flow | Future wood economy or fuel-worker intake | Indirect charcoal supply; other uses remain later design |
| Wood charcoal | Smithing workshop or storage | Construction heat and refurbishment heat |
| Suitable animal fat flow | Renderer intake | Indirect tallow supply |
| Rendered tallow | Market, workshop, or storage | Conditioning, finishing, maintenance, and bounded surface care |
| Edible Hunting relationship | Future Cooking supply design | No equipment destination required |

Storage crafting remains compatible because every material consumed by the approved equipment recipes is an inventory-represented state. Routed fat and ordinary wood relationships become represented equipment inputs only after ordinary labor produces tallow or charcoal.

## 8. Resource-existence and redundancy audit

| Relationship | Real downstream purpose | Meaning without XP | Alternate supply where appropriate | Redundancy finding | Result |
|---|---|---|---|---|---|
| Imported steel stock | Three equipment paths and hard refurbishment | Controls production and repair access | Multiple ordinary external suppliers may exist | Cannot be replaced by Lowmark Mining without contradicting the foundation | **KEEP** |
| Hunting raw hide | Leatherworking and trade | Valuable flexible-structure source | Husbandry and trade | Distinct player route with multi-output context | **KEEP** |
| Husbandry raw hide | Stable ordinary leather supply | Supports households, trade, and repair economy | Hunting and imports | Prevents ecologically forced hunting volume | **KEEP** |
| Ordinary leather supply | Construction and repair | Stable market access | Player Leatherworking | Supports a credible world economy without invalidating the skill | **KEEP** |
| Household flax bundle | Linen and tow source | Supports clothing, repair, and trade | Imports during shortage | Cultivated source cannot be replaced credibly by Foraging | **KEEP** |
| Linen and tow co-output | Joining/lining and damping/padding | Both outputs have distinct sinks | Trade | Two functions from one crop without separate gathering resources | **KEEP** |
| Woodcutting bark co-output | Leather tanning | Valuable alongside ordinary wood | Ordinary forestry and trade | Avoids an isolated bark resource loop | **KEEP** |
| Ordinary charcoal conversion | Smithing heat | Persistent construction and repair sink | Imported fuel supply | Real economy relationship without a new skill | **KEEP** |
| Ordinary tallow conversion | Equipment finishing and maintenance | Recurring upkeep demand | Husbandry, delivered game, and trade | Real byproduct use without a gather-tallow action | **KEEP** |
| Hunting edible-output relationship | Future Cooking supply | Makes Hunting useful beyond leather | Husbandry or other food systems later | Required multi-output relationship; catalog remains deferred | **KEEP AS RELATIONSHIP** |

### Excluded outputs and actions

- No weighted raw-hide drop.
- No universal hide from every animal or enemy.
- No named meat, cut, dish, or Cooking recipe.
- No horn, bone, sinew, organ, gland, trophy, or similar output without demonstrated sinks.
- No isolated bark-stripping action or bark-only node.
- No player charcoal recipe or Charcoal-making skill.
- No gathered tallow or required raw-fat inventory state.
- No Farming, Textile, Weaving, Rendering, Fabrication, or Adornment skill.
- No Lowmark ore source or Mining action for steel.
- No Great War salvage, Stonebound matter, Mire manifestation material, Volkhari source, or supernatural production shortcut.
- No output exists only to create XP.

## 9. Node-readiness audit

This audit tests whether the action and output logic is specific enough to derive node families without placing them.

| Future node or supply family | Required action/output logic now established | Placement requirements preserved for next pass | Result |
|---|---|---|---|
| Hunting opportunity family | Eligible game, successful hunt and field recovery, edible relationship, conditional hide, optional routed fat | Ecology, access, ownership, pressure, recovery space, encounter risk, and non-universal outputs | **READY** |
| Managed Woodcutting family | Selective harvest, ordinary wood primary, eligible bark co-output, optional fuel-worker routing | Bank stability, source health, public repair claims, fire, custody, and closures | **READY** |
| Bark relationship | Attribute of eligible managed woodland work rather than its own action | Must inherit the wood source and stewardship context; no separate bark node | **READY WITH PROHIBITION** |
| Steel receiving family | Imported consignment and workshop acceptance | Markets, crossings, receiving yards, route uncertainty, provenance, and repair demand | **READY AS SUPPLY, NOT GATHERING NODE** |
| Flax supply family | Household cultivation and bundle output | Agricultural suitability, water use, household labor, storage, flood risk, and food-versus-fiber pressure | **READY AS ORDINARY SUPPLY** |
| Textile conversion family | Linen and tow deterministic outputs | Household or specialist work space, water, drying, storage, and market access | **READY AS PROCESSING/SUPPLY** |
| Charcoal supply family | Fuel-worker conversion of suitable wood flow | Safe conversion area, smoke, fire, drying, structural-stock priority, and trade access | **READY AS PROCESSING/SUPPLY** |
| Tallow supply family | Renderer conversion of legitimate animal flow | Household or market animal processing, cleanliness, heat, storage, and waste | **READY AS PROCESSING/SUPPLY** |
| Ordinary tannery family | Raw hide and bark into market leather | Water access, waste separation, odor, drying, custody, and downstream effects | **READY AS PROCESSING/SUPPLY** |

### Node-design constraints carried forward

1. A node or opportunity must represent a world source or supply interface, not merely an inventory item name.
2. Bark may be configured only as an eligible co-output relationship on managed woodland work.
3. Raw hide may be configured only on eligible hide-bearing game with successful recovery conditions or through ordinary animal supply.
4. Steel in Lowmark appears through receiving and trade interfaces, never an invented ore node.
5. Flax appears through household agricultural supply, not a Foraging or Farming node.
6. Charcoal and tallow appear through processors or trade, not natural gathering nodes.
7. Linen, tow, leather, charcoal, and tallow processing sites may become world-facing service or supply interfaces without becoming gathering nodes.
8. Exact map routes, source locations, travel times, site counts, respawn behavior, and regional volumes remain unknown.
9. No supernatural phenomenon validates source eligibility, ownership, condition, or output.

**Node-readiness result: PASS.** The next pass can define node and supply-interface families from approved actions without inventing new materials, skills, or sources.

## Final action and supply model

### Approved player gathering actions

1. **Hunt and field-dress eligible game — Hunting**
   - produces an edible-output relationship where qualified;
   - produces raw hide when the animal is hide-bearing and recovery succeeds;
   - may route suitable fat into ordinary rendering;
   - never uses weighted core-material drops.

2. **Stewardship-approved selective harvest — Woodcutting**
   - produces the ordinary wood relationship;
   - produces tannin-rich bark when the eligible source/action physically supports it;
   - may route suitable player-supplied wood into ordinary charcoal production;
   - never becomes a bark-only action.

### Approved ordinary-labor and trade supply relationships

- Imported conventional supply → plain carbon steel stock.
- Husbandry and ordinary animal processing → alternate raw hide supply and suitable fat flow.
- Player Leatherworking or ordinary tanners → vegetable-tanned leather.
- Lowmark household cultivation and harvest → flax bundle.
- Household or specialist textile labor → linen textile plus flax tow.
- Ordinary forestry and yard work → alternate tannin-rich bark supply where physically eligible.
- Fuel-worker conversion of suitable wood flow → wood charcoal.
- Renderer conversion of legitimate animal-processing flow → rendered tallow.

### Approved output relationship types

- guaranteed direct output;
- source-conditional guaranteed output;
- deterministic co-output;
- ordinary-labor conversion output;
- imported trade supply;
- mixed player and ordinary supply.

Weighted random outputs are not used for the nine core equipment-chain states.

### Unresolved decisions

- Exact huntable animals, ecology, and which are eligible for edible, hide, or suitable-fat relationships.
- Exact recovery conditions and whether field dressing is one interaction or a linked step after the hunt.
- Final edible inventory outputs and Cooking relationships.
- Exact ordinary wood inventory states, species, processing, and uses outside this equipment-chain pass.
- Exact managed woodland source eligibility for usable tanning bark.
- Exact ordinary-labor interfaces for flax, textile, charcoal, tallow, husbandry, tannery, and steel supply.
- Exact ownership, permissions, closures, seasonal constraints, and stewardship authorities.
- Exact conversion proportions, yields, prices, timing, access, and supply volumes.
- Exact imported steel supplier mix, receiving process, and route.
- Whether routed suitable fat or wood is represented elsewhere in the broader economy before conversion.
- All node families, source placement, site count, respawn behavior, and map relationships.
- All S01 ranged gathering and output implications.

No unresolved decision prevents node-family derivation, provided the next pass keeps these source and stewardship constraints visible.

## Exact next handoff

Derive **world node families and placement requirements** from the approved Hunting, Woodcutting, ordinary-labor, processing, receiving, and trade relationships.

Define what kind of world opportunity or supply interface represents each relationship, what ecological or civic conditions permit it, which outputs it can expose, and what placement constraints it inherits. Continue to defer exact coordinates, map routes, quantities, timings, XP, respawn, and implementation schemas.
