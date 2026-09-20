# Caelmor — Processing Relationships and Recipe Structures

**Status:** proposal-stage production model following Creative Director approval of Option A. This document defines inventory representation, process ownership, recipe families, and repair relationships. It does not define quantities, XP, action times, prices, statistics, gathering actions, nodes, exact locations, drop tables, schemas, JSON, or final equipment forms.

## Authority and boundaries

This proposal works from the approved minimum coherent material set, equipment component functions, aspirational equipment foundation, major equipment milestones, and Lore Foundation Lock.

- The equipment material chain uses nine inventory-represented states drawn from six approved material foundations.
- The nine states are not the complete v1 item catalog. Future gathering and economy work may justify other goods through their own needs and relationships.
- Smithing and Leatherworking own the player-facing equipment transformations. Cooking and Fletching receive no artificial dependency; S01 remains deferred.
- Flax processing, charcoal production, and tallow rendering are economy-visible ordinary-labor conversions, not new player skills or a fifth player-facing recipe family.
- Fabrication, Adornment, Textile, Rendering, Charcoal-making, and other new skill identities are not introduced.
- Equipment-specific components and work in progress remain workshop-internal unless later play demonstrates a trade, choice, repair, storage, or reuse need.
- Aspirational commissions are advanced construction variants, not a separate recipe family and not a source of unique ingredients.
- Crafting from storage is a design requirement.

## 1. Inventory-state policy

### Representation test

A material state belongs in inventory only when it supports at least one durable player-facing purpose:

1. it enters or leaves a meaningful gathering, trade, or ordinary-labor relationship;
2. it creates a real processing choice;
3. it is stored independently because later use differs materially from its source or sibling output;
4. it is consumed by several recipes or repairs;
5. it can be reused without inventing a new identity; or
6. possession matters outside one uninterrupted workshop operation.

A state remains workshop-only when it merely shows that a believable physical step occurred, is fitted to one unfinished item, has no independent trade or storage decision, or would exist only to lengthen a recipe.

### Approved inventory granularity

| Inventory-represented state | Why representation matters |
|---|---|
| **Plain carbon steel stock** | Imported, traded, stored, used by several Smithing paths, and consumed in construction and refurbishment. |
| **Raw hide** | Makes the transformation into usable leather visible and supports later hunting, husbandry, trade, and spoilage relationships. |
| **Vegetable-tanned leather** | Stable, tradable output used across flexible equipment, mixed assemblies, maintenance, and repairs. |
| **Flax bundle** | Represents the source-side agricultural or gathered good before household processing and supports later output relationships. |
| **Flax tow** | Has a distinct damping, filling, and padding role that linen textile does not express equally well. |
| **Linen textile** | Has distinct lining, wrapping, joining, and repair uses and can circulate separately from tow. |
| **Tannin-rich bark** | Is a stored and traded tanning input whose availability affects Leatherworking. |
| **Wood charcoal** | Is a stored and consumed workshop fuel shared by construction and refurbishment. |
| **Rendered tallow** | Is a stored maintenance and finishing input used across multiple equipment paths. |

These are required conceptual inventory states within the equipment chain. Final player-facing names and schema identities remain later implementation decisions.

### Approved workshop-only states

The following remain non-inventory unless a later demonstrated gameplay need passes the representation test:

- formed steel pieces;
- prepared hide;
- tanning liquor;
- thread;
- cut panels;
- layered padding;
- fitted subassemblies;
- inspected commission work;
- generic equipment-specific components and work-in-progress pieces.

Other brief physical conditions, including heated stock, drying hide, softened leather, marked patterns, aligned junctions, fitted linings, and inspection holds, are also process steps rather than inventory items.

### Crafting from storage

- A recipe or workshop order may draw its approved inventory inputs from accessible storage under the existing storage-crafting requirement.
- Workshop-only states occur inside the ordered process and do not need to be moved into the player's inventory between steps.
- A multi-stage physical process does not require a chain of inventory transfers merely to prove that each step happened.
- The later implementation pass must define interruption, cancellation, and input-return behavior without changing this material architecture.
- Commission legitimacy, custody records, fitting references, and inspection results are qualifications or records, never material inputs.

## 2. Six material process chains

### 2.1 Plain carbon steel stock chain

```text
imported or otherwise lawfully received plain carbon steel stock [inventory]
→ inspect, sort, and clean [workshop-only]
→ heat, form, join, and establish working geometry [workshop-only]
→ heat treatment, fitting, finishing, and inspection as required [workshop-only]
→ finished equipment [inventory/equipment]
```

| Design question | Decision |
|---|---|
| Source/input state | Plain carbon steel stock begins the Lowmark equipment chain as an inventory good. Ore extraction and primary regional metal production remain outside this v1 equipment process. |
| Transformations that matter | Smithing converts fungible stock into purpose-specific structure, edge-bearing work, impact-facing work, hard reinforcement, or justified fittings. Later milestones demand more controlled geometry, force paths, joining, heat treatment, fitting, and inspection. |
| Inventory states | Plain carbon steel stock and finished equipment only. |
| Workshop-only states | Cleaned stock, heated work, formed pieces, aligned assemblies, heat-treated pieces, fitted work, and inspected commission work. |
| Player skill ownership | Smithing owns player-facing equipment construction and hard refurbishment. |
| Ordinary labor | Carriers, merchants, receiving workers, and workshop assistants can handle delivery, sorting, fuel tending, and routine support without becoming player skills. |
| Repair/refurbishment | Smithing uses steel stock and charcoal to correct safe distortion, restore working geometry, replace justified hard wear, or rebuild damaged sections. Tallow may support bounded surface care. |
| Byproducts | No new slag, scale, filings, blank, plate, or scrap inventory is created. Sound recoverable steel may re-enter the existing stock state only if later economy design gives inspection and recovery a real sink and constraint. |
| Milestone continuity | Every milestone uses the same steel state. Advancement comes from construction discipline rather than a succession of metals. |

### 2.2 Vegetable-tanned hide leather chain

```text
raw hide [inventory]
+ tannin-rich bark [inventory]
→ cleaning, preservation check, scraping, and preparation [workshop-only]
→ bark preparation and tanning liquor [workshop-only]
→ tanning, drying, softening, and conditioning [workshop-only]
→ vegetable-tanned leather [inventory]
```

| Design question | Decision |
|---|---|
| Source/input state | Raw hide remains visible because preservation and conversion into stable leather are meaningful. Tannin-rich bark supplies the approved tanning basis. |
| Transformations that matter | Leatherworking judges usable hide, controls preparation and tanning, establishes stable flexibility, and produces leather fit for later cutting and repair. Tallow may support finishing or later maintenance where physically appropriate. |
| Inventory states | Raw hide, tannin-rich bark, vegetable-tanned leather, and rendered tallow when used. |
| Workshop-only states | Prepared hide, tanning liquor, wet or drying hides, softened work, graded pieces, and spent process matter. |
| Player skill ownership | Leatherworking owns the raw-hide-to-leather transformation. |
| Ordinary labor | Husbandry, butchery, market transfer, water carrying, waste handling, and workshop assistance do not become extra player crafting skills. Hunting matters only when it actually supplies the hide. |
| Repair/refurbishment | Finished leather is patched, conditioned, refitted, or sectionally replaced through Leatherworking. Structural failure cannot be reversed merely by applying tallow or repeating the tanning step. |
| Byproducts | Flesh waste, hair, spent liquor, and spent bark receive no inventory identity because this equipment model gives them no approved sink. |
| Milestone continuity | All milestones use the same leather state. Later work selects, patterns, or integrates it more carefully instead of introducing superior named leathers. |

### 2.3 Flax textile chain

```text
flax bundle [inventory]
→ drying and fiber preparation [ordinary-labor process]
→ separation into useful long fiber and tow [ordinary-labor process]
→ flax tow [inventory]
or
→ spinning and weaving [ordinary-labor process]
→ linen textile [inventory]
```

| Design question | Decision |
|---|---|
| Source/input state | Flax bundle is the stored source good connecting later gathering or agriculture to household processing. |
| Transformations that matter | The branch between tow and woven linen matters because the outputs answer different physical needs. Tow supports damping and filling; linen supports lining, wrapping, stitching, and repair. |
| Inventory states | Flax bundle, flax tow, and linen textile. |
| Workshop-only states | Partly prepared fiber, spun thread, cut cloth, layered padding, quilted sections, fitted linings, and seam work. |
| Player skill ownership | No new Textile or Weaving skill is introduced. Leatherworking owns the use and integration of tow and linen in equipment. |
| Ordinary labor | Households and textile specialists perform fiber preparation, spinning, and weaving as economy-visible conversion labor. Players may buy, sell, store, or commission the outputs without training a new craft. |
| Repair/refurbishment | Leatherworking consumes linen textile or tow directly to renew seams, replace linings, restore padding, or patch suitable flexible work. Thread remains internal to that operation. |
| Byproducts | Tow is the only represented secondary output because it has approved equipment sinks. Dust, short unusable waste, and wash residue remain unrepresented. |
| Milestone continuity | Early equipment uses simple lining and padding; later work improves placement, layering, compression, seam control, and fitted replacement with the same two outputs. |

### 2.4 Tannin-rich bark chain

```text
tannin-rich bark [inventory]
→ dry, break, and prepare as required [workshop-only]
→ extract tanning liquor using ordinary water [workshop-only]
→ consume within Leatherworking leather preparation
```

| Design question | Decision |
|---|---|
| Source/input state | Tannin-rich bark arrives as an inventory good from stewardship-compatible woodland work or trade. Exact species and gathering method remain for the next handoff. |
| Transformations that matter | Availability and consumption matter; separate crushed bark or tanning-liquor items do not. |
| Inventory states | Tannin-rich bark only. |
| Workshop-only states | Sorted bark, crushed or steeping bark, tanning liquor, active tanning bath, and spent matter. |
| Player skill ownership | Leatherworking owns its use in tanning. The equipment chain does not create a separate extraction or alchemical skill. |
| Ordinary labor | Woodland custody, carrying, drying, water provision, and safe waste removal may be ordinary labor. |
| Repair/refurbishment | Bark supports new leather production and only those bounded restoration processes that physically require tanning treatment. It is not a universal leather repair consumable. |
| Byproducts | Spent bark and used liquor have no approved equipment sink and remain unrepresented. |
| Milestone continuity | The same bark foundation supports all leather milestones. Better outcomes come from process control, not prestigious bark tiers. |

### 2.5 Wood charcoal chain

```text
stewardship-approved wood feedstock [outside the equipment-chain state list]
→ drying, controlled conversion, cooling, and sorting [ordinary-labor process]
→ wood charcoal [inventory]
→ consumed by Smithing construction or refurbishment
```

| Design question | Decision |
|---|---|
| Source/input state | The equipment chain receives wood charcoal as its represented input. Wood feedstock may exist elsewhere in the v1 economy but requires its own gathering and output justification. |
| Transformations that matter | Charcoal production is economy-visible because woodland stewardship, competing fuel demand, conversion labor, storage, and supply interruption matter. It is not a player crafting skill in this model. |
| Inventory states | Wood charcoal only within the equipment material chain. |
| Workshop-only states | Drying feedstock, converting fuel, cooling fuel, fuel in an active forge, embers, and ash. |
| Player skill ownership | Smithing consumes charcoal in player-facing steel construction and hard refurbishment. Smithing does not own charcoal production. |
| Ordinary labor | Fuel workers perform preparation and conversion; carriers and stores handle distribution. Woodcutting involvement belongs to the next gathering/output pass if physically and economically justified. |
| Repair/refurbishment | Charcoal makes reheating and structural steel repair a real economic sink. It cannot repair equipment by itself. |
| Byproducts | Ash, fines, and partially burned fuel receive no inventory identity because no approved equipment sink exists. |
| Milestone continuity | All steel milestones consume the same fuel state. Later recipes demand more controlled workshop work, not superior charcoal grades. |

### 2.6 Rendered tallow chain

```text
suitable animal fat [outside the equipment-chain state list]
→ clean, render, strain, cool, and store [ordinary-labor process]
→ rendered tallow [inventory]
→ consumed in finishing, conditioning, or maintenance where justified
```

| Design question | Decision |
|---|---|
| Source/input state | The equipment chain receives rendered tallow as its represented input. Animal-processing outputs may exist elsewhere but require their own economic relationships. |
| Transformations that matter | Rendering is economy-visible ordinary labor because it turns a perishable byproduct into a stable workshop good. Separate raw-fat or strained-fat equipment items are unnecessary. |
| Inventory states | Rendered tallow only within the equipment material chain. |
| Workshop-only states | Cleaned fat, heated rendering work, strained liquid, cooling batches, applied dressing, and surface residue. |
| Player skill ownership | Leatherworking consumes tallow for flexible equipment finishing and maintenance. Smithing may consume it for a bounded justified surface-care operation. Cooking is not required merely because heat and animal fat are involved. |
| Ordinary labor | Animal processors or renderers perform the conversion; household and market labor may store or distribute the result. |
| Repair/refurbishment | Tallow supports conditioning, thread preparation, friction control, and surface protection. It cannot restore torn structure, failed joins, or distorted steel. |
| Byproducts | Rendering residue has no approved equipment sink and remains unrepresented. |
| Milestone continuity | Tallow remains a routine maintenance input from early equipment through aspirational service. It gains importance through care expectations rather than material ranking. |

## 3. Player-skill and ordinary-labor responsibility

| Activity | Responsibility | Player-facing result |
|---|---|---|
| Raw hide to vegetable-tanned leather | **Leatherworking** | A meaningful player transformation producing a stable, reusable equipment input. |
| Steel equipment construction | **Smithing** | Finished Blade, Guard, or Harness-path equipment using workshop-internal forming and assembly. |
| Leather-led equipment construction | **Leatherworking** | Finished Riverpath-path equipment and physically justified flexible construction. |
| Hard repair and structural refurbishment | **Smithing** | Restored hard-primary equipment using represented stock and fuel where needed. |
| Flexible repair, lining, fastening, and refitting | **Leatherworking** | Restored flexible-primary equipment or justified flexible portions of mixed equipment. |
| Flax bundle to tow or linen | **Ordinary household or specialist labor** | Economy-visible conversion outputs that can be traded, stored, and used. No new skill. |
| Wood feedstock to charcoal | **Ordinary fuel-worker labor** | Economy-visible fuel supply. No Charcoal-making skill. |
| Animal fat to rendered tallow | **Ordinary processor or renderer labor** | Economy-visible maintenance supply. No Rendering or forced Cooking dependency. |
| Commission fitting and inspection | **Primary craft plus accountable specialist workshop labor** | Finished commissioned equipment and provenance records, with no Fabrication or Adornment skill. |
| Fletching | **No current role** | S01 is deferred; no ranged dependency is inferred. |
| Cooking | **No required equipment role** | Cooking may later use shared economy outputs for its own reasons, but equipment does not force the connection. |

Where an item has a Smithing primary craft, necessary leather or textile work may be integrated as ordinary specialist workshop labor unless later design demonstrates a meaningful Leatherworking prerequisite. Where an item has Leatherworking as its primary craft, a justified hard fitting may be supplied as ordinary stock or workshop work without forcing Smithing mastery. This preserves one clear primary craft per path.

## 4. Recipe-family structure for Milestones 1–4

The v1 equipment model has **four player-facing recipe families**. Variants inside a family may serve different paths and milestones without becoming separate production systems.

### Family 1 — Leather preparation

**Owner:** Leatherworking.

**Structure:**

```text
raw hide + tannin-rich bark
+ rendered tallow only where the finishing method requires it
→ vegetable-tanned leather
```

| Milestone relationship | Process emphasis |
|---|---|
| Milestone 1 | Produce stable, usable leather and recognize unfit raw hide. |
| Milestone 2 | Control flexibility and surface preparation for intended working identities. |
| Milestone 3 | Select and prepare leather whose behavior is compatible across fitted and repairable sections. |
| Milestone 4 | Support matched commission work through disciplined preparation and traceable workshop handling; output remains vegetable-tanned leather rather than a new masterwork material. |

### Family 2 — Smith-led equipment construction

**Owner:** Smithing.

**Coverage:** Keeper's Blade, Crestbridge Guard, and Bridgewarden Harness path variants.

**Structure:**

```text
plain carbon steel stock + wood charcoal
+ only the leather, flax tow, linen textile, or tallow physically required by the item
→ internal forming, joining, fitting, finishing, and inspection
→ finished equipment
```

| Milestone | Recipe structure |
|---|---|
| **1 — Dependable field equipment** | Direct construction establishes stable geometry, a reliable working surface, and necessary control or fit. Internal parts are not inventory outputs. |
| **2 — Declared working identity** | The same materials are formed and integrated around the chosen generalist, active-defense, or heavy-protection behavior. Additional inputs appear only for real damping, fastening, lining, or wear needs. |
| **3 — Proven specialist equipment** | Construction tightens junction control, force paths, zoned protection, service access, and compatibility between hard and flexible work. Provenance and responsible use may gate access without entering the recipe. |
| **4 — Aspirational commission** | An advanced variant adds matched preparation, bearer fitting, close tolerances, staged inspection, accountable custody, and an established repair standard. It adds no new ingredient or fifth recipe family. |

### Family 3 — Leather-led equipment construction

**Owner:** Leatherworking.

**Coverage:** Riverpath Leathers path variants and other future flexible-primary equipment only where separately approved.

**Structure:**

```text
vegetable-tanned leather
+ flax tow, linen textile, and rendered tallow as physically required
+ plain carbon steel stock only for a justified hard fitting or reinforcement
→ internal patterning, cutting, stitching, layering, fitting, finishing, and inspection
→ finished equipment
```

| Milestone | Recipe structure |
|---|---|
| **1 — Dependable field equipment** | Establish a stable flexible structure, protective face, closure, and necessary lining. |
| **2 — Declared working identity** | Pattern for movement, reinforce actual stress points, and distinguish replaceable wear from primary structure. |
| **3 — Proven specialist equipment** | Zone protection and flexibility, match stretch and compression, control seams, and preserve repair access. |
| **4 — Aspirational commission** | An advanced variant adds wearer-specific patterning, matched flexible sections, full-movement inspection, documented fitting, and a repair standard. No commission-only substance is added. |

### Family 4 — Equipment repair and refurbishment

**Owner:** Smithing for hard-primary work; Leatherworking for flexible-primary work and justified flexible repairs.

**Structure:**

```text
damaged or worn equipment
+ represented material appropriate to the actual damage
+ charcoal for heat-dependent Smithing work
+ tallow for justified conditioning or surface care
→ internal inspection, correction, refitting, replacement, and verification
→ restored equipment
```

| Service class | Recipe role |
|---|---|
| Routine maintenance | Clean, dress, condition, adjust, or renew a minor service point using direct represented inputs where necessary. |
| Flexible repair | Patch, restitch, reline, repad, replace a fastening, or refit using leather, tow, linen, or tallow as justified. |
| Hard refurbishment | Restore working geometry, correct safe distortion, renew a hard wear point, or rebuild a damaged section using steel stock and charcoal. |
| Commission-preserving refurbishment | Repeat fitting references and inspection standards so repair preserves the commissioned behavior. Provenance guides the work but is not consumed. |

The family does not require repair kits, generic component items, or per-component durability meters.

## 5. Repair and refurbishment model

### Item-level condition

- Equipment condition is tracked and serviced at the item level unless later implementation proves that a smaller model is necessary.
- The physical diagnosis determines which represented material a repair consumes; the player does not manage eight component durability bars.
- Routine care delays workshop repair but cannot erase structural failure.
- Working surfaces and serviceable wear parts remain distinct. A repair may dress an integral working surface or replace a justified sacrificial part without assuming they are the same object.

### Field maintenance

Field maintenance covers cleaning, drying, simple adjustment, surface dressing, conditioning, and other bounded care that does not require structural reshaping. Tallow may be consumed when its physical role applies. Exact interfaces and timing remain later decisions.

### Workshop repair

- **Smithing refurbishment** handles lost alignment, hard structural damage, edge restoration beyond ordinary care, distorted protection, and failed major hard junctions.
- **Leatherworking repair** handles torn or stretched flexible structure, failed seams or fastenings, damaged lining, packed-down tow, refitting, and replacement of justified flexible wear parts.
- Mixed equipment goes to the craft responsible for the damaged primary structure. Ordinary specialist labor can integrate secondary work without introducing Fabrication.
- Commissioned equipment uses the same material states as earlier equipment. Its repair may require the accountable workshop, fitting reference, or inspection access that preserves its identity.

### Reuse and retirement

- Repair takes priority when the primary structure remains safe and the work preserves intended behavior.
- A retired item does not automatically explode into component inventory.
- Sound recovered steel, leather, or textile may return to an existing represented state only if later economy design establishes inspection, recovery loss, and a genuine reuse sink.
- Contaminated, overstrained, rotten, deeply cracked, evidentiary, or otherwise unsafe matter is retired rather than laundered into ordinary stock.
- Great War remains never enter routine recovery merely because a repair or recycling path exists.

## 6. Intermediate-item necessity audit

### Inventory-represented states

| State | Trade or source role | Distinct choice or use | Multi-recipe or repair value | Result |
|---|---|---|---|---|
| Plain carbon steel stock | Imported and stored | Allocate between construction and refurbishment | Three equipment paths and hard repairs | **KEEP** |
| Raw hide | Local or traded source | Process now, preserve, trade, or hold subject to later spoilage design | Feeds all leather production | **KEEP** |
| Vegetable-tanned leather | Stable processed good | Allocate across flexible structure, mixed work, and repair | Four paths where physically required | **KEEP** |
| Flax bundle | Source-side farm or gathering output | Convert through ordinary labor into tow or linen | Feeds two useful outputs | **KEEP** |
| Flax tow | Economy-visible textile output | Select damping or filling use rather than woven use | Guards, Harness, Leathers, and repairs where needed | **KEEP** |
| Linen textile | Economy-visible textile output | Select lining, wrapping, stitching, or patch use | Multiple construction and repair recipes | **KEEP** |
| Tannin-rich bark | Woodland or trade input | Allocate to leather production | Repeated Leatherworking batches | **KEEP** |
| Wood charcoal | Fuel supply | Allocate between construction and refurbishment | All heat-dependent Smithing recipes | **KEEP** |
| Rendered tallow | Animal-economy maintenance good | Allocate between finishing and upkeep | Flexible work, maintenance, and bounded steel care | **KEEP** |

### Workshop-only states

| State | Why it stays internal |
|---|---|
| Formed steel pieces | Shape is equipment-specific, lacks broad interchangeability, and would prematurely lock forms. |
| Prepared hide | Exists only on the path from raw hide to leather and adds no separate trade or use choice. |
| Tanning liquor | Is process-bound, cumbersome, and has no approved use outside the active tanning operation. |
| Thread | Is produced and consumed within textile or Leatherworking operations; current recipes do not justify separate trade or storage. |
| Cut panels | Are pattern-specific and have no reliable cross-path use. |
| Layered padding | Is fitted to an item; tow remains the transferable input. |
| Fitted subassemblies | Are matched to one workpiece or wearer and are unsuitable as generic market goods. |
| Inspected commission work | Is a status and accountable process state, not matter. |
| Generic blanks, plates, strap kits, lining kits, padding packages, and repair kits | Exist only to expose arrows in a chain and would duplicate the represented materials. |

No workshop-only state is prohibited forever. It may become inventory-represented only after a later design demonstrates independent trade, choice, repair, storage, or cross-recipe value.

## 7. Material sinks and reuse

| Represented material | Construction sinks | Repair or upkeep sinks | Reuse rule |
|---|---|---|---|
| Plain carbon steel stock | Blade, Guard, Harness, and justified hard fittings | Hard refurbishment, replaced hard wear, sectional rebuilding | Sound recovered material may re-enter the same stock identity only after a later recovery model is justified. |
| Raw hide | Leather preparation | None directly; repair uses finished leather | Converts into leather rather than circulating as repair stock. |
| Vegetable-tanned leather | Leathers, fastenings, flexible controls, wear parts, mixed protection | Patches, section replacement, refitting, closure repair | Sound offcuts or removed sections are handled inside workshop efficiency unless a future trade need appears. |
| Flax bundle | Ordinary-labor conversion | None directly | Converts into tow or linen. It is not used as filler merely to avoid processing. |
| Flax tow | Damping, filling, and layered protection | Padding renewal and compression repair | Removed packed or contaminated tow is not automatically reusable. |
| Linen textile | Lining, joining, wrapping, and flexible support | Relining, restitching, wrapping, and patching | Sound remnants may support a repair inside the same workshop process without a new scrap item. |
| Tannin-rich bark | Leather preparation | Bounded restoration only where tanning treatment is physically valid | Consumed; spent bark has no equipment sink. |
| Wood charcoal | Smithing heat for construction | Smithing heat for refurbishment | Consumed; ash and fines have no equipment sink. |
| Rendered tallow | Finishing and conditioning | Recurring maintenance, thread dressing, and surface care | Consumed through use; residue is not recovered. |

The sink structure keeps basic materials relevant after the player reaches later milestones. Repairs sustain demand without forcing disposable equipment or XP-only production.

## 8. Scope and redundancy audit

| Check | Result | Finding |
|---|---|---|
| Approved foundation preserved | **PASS** | All processes use the six approved material foundations. No new equipment material is introduced. |
| Inventory minimum | **PASS** | Nine states pass the trade, choice, storage, repair, or reuse test. All other process states remain internal. |
| Intermediate bloat | **PASS** | No blanks, plates, thread, kits, fitted parts, padding packages, or WIP objects are required as inventory. |
| Recipe-family count | **PASS** | Four player-facing families cover preparation, both primary craft identities, and service. Aspirational work is a variant rather than a fifth family. |
| Ordinary-labor boundary | **PASS** | Flax processing, charcoal making, and tallow rendering remain economy-visible without creating skills or player recipe families. |
| Core skill discipline | **PASS** | Smithing and Leatherworking own real equipment transformations. Cooking and Fletching are not forced into the chain; Fabrication and Adornment remain absent. |
| Crafting from storage | **PASS** | All transferable inputs are represented inventory states; internal steps require no intermediate inventory transfers. |
| Progression without substitution | **PASS** | Milestones deepen construction, process control, fitting, service access, inspection, and provenance while reusing the same materials. |
| Component-family reuse | **PASS** | The four paths share material and process logic without converting functional component vocabulary into generic inventory kits. |
| Repair economy | **PASS** | Direct material consumption supports maintenance and refurbishment without component durability simulation or mandatory replacement gear. |
| Byproduct discipline | **PASS** | Tow is represented because it has real sinks. Waste, ash, spent liquor, filings, residue, and scrap categories are omitted until a use exists. |
| Lore boundaries | **PASS** | No Stonebound, Mire manifestation, Volkhari, war salvage, magical, memorial, or capstone source enters production. |
| Form neutrality | **PASS** | Recipes define functional processes without deciding Blade shape, handedness, Guard slot, armor breakdown, or loadout compatibility. |
| S01 boundary | **PASS** | No ranged recipe, ammunition, or Fletching dependency is inferred. |

## Final production model

### Approved inventory-represented material states

1. Plain carbon steel stock.
2. Raw hide.
3. Vegetable-tanned leather.
4. Flax bundle.
5. Flax tow.
6. Linen textile.
7. Tannin-rich bark.
8. Wood charcoal.
9. Rendered tallow.

These are the minimum inventory states for the equipment material chain, not the entire v1 economy catalog.

### Workshop-only process states

- formed steel pieces;
- prepared hide;
- tanning liquor;
- thread;
- cut panels;
- layered padding;
- fitted subassemblies;
- inspected commission work;
- generic equipment-specific components and WIP pieces;
- other brief heating, drying, fitting, joining, finishing, and inspection states without independent economic value.

### Recipe-family count

**Four player-facing recipe families:**

1. Leather preparation — Leatherworking.
2. Smith-led equipment construction — Smithing.
3. Leather-led equipment construction — Leatherworking.
4. Equipment repair and refurbishment — Smithing or Leatherworking according to the damaged primary structure.

Flax processing, charcoal production, and tallow rendering are economy-visible ordinary-labor conversions. They do not count as a fifth player-facing recipe family.

### Unresolved decisions

- Final player-facing names and catalog representation for the nine states.
- Exact ordinary-labor interface for converting flax bundle into tow or linen and for supplying charcoal and tallow.
- Exact recipe inputs, quantities, timing, XP, access requirements, success behavior, and storage-selection rules.
- Exact representation of process quality without creating material tiers or redundant inventory states.
- Exact equipment condition model, repair thresholds, loss, interruption, cancellation, and input-return behavior.
- Whether safe recovered matter ever returns to an existing inventory state and under what losses or inspection requirements.
- Exact commission workshop, fitting, inspection, custody, replacement, and duplicate rules.
- Exact equipment forms and whether they later justify optional wool felt or seasoned hardwood.
- All S01 ranged processing and recipe questions.

No unresolved decision blocks the gathering-output pass.

## Exact next handoff

Define **gathering actions and output relationships** for the represented source-side and supply-side goods. Establish what player or ordinary labor produces, which approved inventory state receives the output, what stewardship or access governs it, and which outputs enter trade rather than direct player processing.

Do this before designing world nodes, exact locations, action timing, XP, yield, or spawn behavior.
