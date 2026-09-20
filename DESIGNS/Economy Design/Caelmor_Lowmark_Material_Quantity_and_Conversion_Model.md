# Caelmor — Lowmark Material Quantity and Conversion Model

**Status:** Proposal-stage quantitative economy model
**Scope:** Analytical gathering quantities, ordinary-labor conversions, player-facing material conversions, and source-to-sink pressure; not final item data

## 1. Quantity policy

This model preserves the approved nine equipment-chain inventory states and adds no new material identity. Two terms remain analytical relationship units pending later catalog work:

- **edible unit:** a standardized amount of recoverable food value; it is not a final meat, cut, or recipe item;
- **ordinary-wood unit:** a standardized usable load or bundle from one completed wood recovery relationship; exact species and visual form remain open.

A unit is sized for inventory and economic reasoning, not as a literal whole animal, tree, hide, or log. Workshop-only stages remain workshop-only.

Quantity rules:

1. source and recovery determine output; no weighted jackpot rolls are added;
2. one event may yield several units when the source physically supports more recoverable value;
3. final inventory stack sizes and carrying limits remain open;
4. processing ratios create loss, labor, and choice without inventing waste items;
5. ordinary-world supply coexists with player supply at every approved interface.

## 2. Gathering output quantities

### 2.1 Hunting outputs

| Recovery profile | Provisional quantity | Representative use | Physical/economic purpose |
|---|---:|---|---|
| Light edible recovery | 1 edible unit | HM1, HM3, representative non-hide HM4 expression | Keeps small/food-focused opportunities useful without producing grazer-scale food |
| Ordinary mixed recovery | 2 edible units | HM2 and similar medium source expressions | Recognizes broader household food value while preserving recovery burden |
| Full grazer recovery | 3 edible units | HM5 and a comparable underlying HM6 source | Makes full field recovery materially worthwhile without adding cuts or byproducts |
| Qualified hide recovery | 1 raw-hide unit | Any eligible hide-bearing source with successful preservation | Represents one standardized usable hide lot after field loss and grading |
| Renderer-eligible recovery | 1 eligible-flow relationship | Suitable animal recovery routed to an ordinary renderer | Carries biological value into ordinary labor without creating a raw-fat item |

HM6 inherits the edible, hide, and renderer profile of its underlying ordinary source. HM7 inherits output only when a hunt is justified. Refusal, redirection, or delay can correctly produce no gathered material.

The representative HM8 circuit contains one HM3 light recovery, one non-hide HM4 light recovery, and one HM5 full recovery:

```text
HM8 complete circuit
→ 5 edible units
+ 1 raw-hide unit from the HM5 leg
+ 1 renderer-eligible relationship when that leg physically qualifies
```

### 2.2 Hunting material units per engaged hour

| Method | Baseline units/h | Knowledgeable units/h | Pressure finding |
|---|---|---|---|
| HM1 | 24 edible | 26.7 edible | Comfortable low-value food flow |
| HM2 | 36 edible; up to 18 raw hide and 18 renderer relationships | 40 edible; up to 20 hide/renderer | Strong early mixed supply; hide demand must not assume every player self-tans |
| HM3 | 24.8 edible | 27.3 edible | Focused food flow with no equipment material |
| HM4 | 18.5 edible at the representative light profile | 20.2 edible | Source expression may change quantity and hide eligibility; no default hide is assumed |
| HM5 | 48 edible; up to 16 raw hide and 16 renderer relationships | 54 edible; up to 18 hide/renderer | Highest dependable focused hide and animal-processing flow |
| HM6 | About 9–39 edible after valid declines/failures; hide/renderer source-conditional | Same sustainable range at knowledgeable execution | Not a dependable bulk source |
| HM7 | Zero to contextual ordinary output | Zero to contextual ordinary output | Material production is intentionally inconsistent |
| HM8 | 58.4 edible; 11.7 raw hide/renderer | 62.3 edible; 12.5 hide/renderer | Highest continuous food pressure; post-80 weighted play is about 52–55 edible units/h |

The HM8 weighted figure includes fallback HM5/HM6/HM7 time from the approved sustainable post-80 mix. It is not an additional circuit bonus.

### 2.3 Woodcutting outputs

| Output relationship | Provisional quantity | Rule |
|---|---:|---|
| Ordinary-wood recovery | 1 ordinary-wood unit per completed valid work | The unit abstracts a usable load; method identity changes work and routing, not wood tier |
| Bark-eligible recovery | 1 tannin-rich bark unit per qualifying work | Guaranteed when the selected source/action physically qualifies; absent otherwise |

| Method | Baseline units/h | Knowledgeable units/h | Pressure finding |
|---|---|---|---|
| WM1 | 30 wood; 0–8 bark across qualifying work | 33.3 wood; 0–8 bark target | High convenience, ordinary value |
| WM2 | 23.2 wood; 10–17 bark target | 25.7 wood; 10–17 bark target | Principal balanced wood/bark supply |
| WM3 | 17.1 wood; 0–6 bark | 18.9 wood; 0–6 bark | Lower bulk, stronger public/repair purpose |
| WM4 | 30.9 wood; 12–22 bark target | 34.3 wood; 12–22 bark target | High route throughput and tanning support |
| WM5 | Up to 16.4 wood; 0–5 bark | Up to 18 wood; 0–5 bark | Sustainable usable flow falls to about 8–14 wood/h after nonproductive outcomes |
| WM6 | 13.8 purpose-bound wood; 0–4 bark | 15.3 wood; 0–4 bark | Demand-limited repair supply |
| WM7 | 12.9 wood; 2–6 bark | 14.1 wood; 2–6 bark | Constraint-led, not bulk-led |
| WM8 | 51.9 wood; 18–37 bark target | 55.4 wood; 18–37 bark target | Highest continuous wood pressure; sustainable post-80 weighted flow is about 45.9 wood/h |

Bark targets describe how many works along a route are eligible. They are not random output probabilities.

## 3. Conversion ratios

### 3.1 Raw hide and bark into leather

```text
2 raw-hide units
+ 1 tannin-rich bark unit
→ ordinary preparation, tanning, drying, softening, and grading
→ 2 vegetable-tanned leather units
```

| Question | Finding |
|---|---|
| Physical reasoning | Each raw-hide unit remains traceable into one usable leather unit; one bark unit supports a small shared tanning batch rather than being consumed hide-for-hide |
| Gameplay purpose | Couples Hunting/husbandry supply to Woodcutting/forestry without making bark the dominant output |
| Supply pressure | One knowledgeable HM5 hour can supply 18 hide units and therefore needs 9 bark to become 18 leather; this sits inside one focused WM2 hour’s 10–17 bark target |
| Sink quality | Tanning consumes bark and stabilizes perishable raw hide without a prepared-hide or tanning-liquor inventory item |
| Ordinary competition | Husbandry supplies alternate raw hide; ordinary tanners buy both inputs and sell leather alongside player Leatherworking |

Tallow is not mandatory for base tanning. It enters finishing, construction, or maintenance only where physically justified.

### 3.2 Ordinary wood into charcoal

```text
3 ordinary-wood units accepted for fuel work
→ ordinary fuel-worker conversion
→ 1 wood-charcoal unit
```

| Question | Finding |
|---|---|
| Physical reasoning | Charcoal loses substantial mass and volume during controlled heating; three usable feed units for one stable fuel unit expresses that loss |
| Gameplay purpose | Gives ordinary wood a persistent Smithing relationship without creating a player Charcoal-making skill |
| Supply pressure | The sustainable post-80 WM8 flow could support about 15 charcoal/h if every wood unit were diverted to fuel; repair, market, and public wood demand compete for the same flow |
| Sink quality | Every heat-dependent Smithing construction or refurbishment consumes charcoal |
| Ordinary competition | Fuel workers also receive ordinary forestry and traded feedstock; player Woodcutting is useful but never monopolistic |

Protected bank growth, repair reserve, or otherwise purpose-bound wood cannot be diverted merely because the ratio exists.

### 3.3 Renderer flow into tallow

```text
4 renderer-eligible animal relationships
→ ordinary rendering and settling
→ 1 rendered-tallow unit
```

| Question | Finding |
|---|---|
| Physical reasoning | Suitable fat is a subset of animal value and rendering loses water and unusable matter; several recoveries support one stable workshop unit |
| Gameplay purpose | Keeps tallow useful but slower than hides or food, avoiding a third direct Hunting drop |
| Supply pressure | A knowledgeable HM5 hour has an absolute ceiling of 4.5 tallow units; actual flow is lower because not every recovery qualifies or routes to a renderer |
| Sink quality | Tallow supports leather conditioning, thread preparation, flexible maintenance, and bounded steel surface care |
| Ordinary competition | Husbandry and ordinary animal processing remain the dependable background source |

Raw fat remains unrepresented. The renderer receives the eligible relationship through custody/ordinary processing rather than a new inventory item.

### 3.4 Flax into linen and tow

```text
3 flax-bundle units
→ ordinary retting, breaking, sorting, spinning, and weaving
→ 2 linen-textile units
+ 1 flax-tow unit
```

| Question | Finding |
|---|---|
| Physical reasoning | A source batch separates longer fiber suitable for woven linen from shorter tow suitable for filling and damping |
| Gameplay purpose | Produces both approved textile states from one farm flow and gives linen the larger share expected by lining/joining demand |
| Supply pressure | Tow remains meaningfully scarcer than linen; exact household production volume is not fixed |
| Sink quality | Linen supports lining, joining, wrapping, and patches; tow supports damping, padding, and renewal |
| Ordinary competition | Household and specialist textile labor owns the conversion; the player buys, stores, trades, or uses the outputs without a Textile skill |

Thread, cut panels, and layered padding remain workshop-only.

### 3.5 Imported steel into Smithing use

```text
plain carbon steel stock
+ wood charcoal where heat is required
→ Smithing construction or hard refurbishment
```

One steel-stock unit is a standardized accepted workshop charge, not a metal tier. Forming, heat treatment, cut stock, plates, blanks, and fitted pieces remain internal. Construction and repair consume stock directly according to the demand patterns in the companion crafting model.

Ordinary importers and local workshops supply steel. No Lowmark ore or Mining loop is introduced.

## 4. Derived hourly conversion capacity

| Supply example | Conversion capacity if fully committed | Why full commitment is unlikely |
|---|---|---|
| 1 knowledgeable HM5 hour: 18 hide + up to 18 renderer relationships | 18 leather using 9 bark; up to 4.5 tallow | Food, market sale, ordinary tannery demand, renderer eligibility, and player goals divide the flow |
| 1 knowledgeable HM2 hour: 20 hide | 20 leather using 10 bark | Player may sell raw, keep food, lack bark, or buy ordinary leather instead |
| 1 knowledgeable WM2 hour: 25.7 wood + 10–17 bark | About 8 charcoal if all wood is accepted fuel; enough bark for 20–34 leather | Wood also serves repair, market, storage, and later approved uses; hide supply limits tanning |
| 1 sustainable post-80 WM8 hour: 45.9 wood | About 15 charcoal if every eligible unit is routed to fuel workers | Broad wood supply competes with repair/public demand and low-value bulk sale |
| 3 flax bundles from ordinary supply | 2 linen + 1 tow | Household availability, service cost, and equipment demand govern conversion |

These capacities show that no player must train both gathering skills. A Leatherworker can buy hide or bark; a Smith can buy steel and charcoal; a gatherer can sell raw relationships without processing everything.

## 5. Material existence and pressure audit

| Material or relationship | Supply basis | Primary consumption | Pressure | Control |
|---|---|---|---|---|
| Edible units | Hunting plus later ordinary food systems | Future Cooking, household use, market | **HIGH / UNRESOLVED** | Final edible catalog, per-unit recipes, consumption, storage, modest buyer floor |
| Raw hide | Hunting and husbandry | Tanning | **HIGH** | Two-unit tanning batches, ordinary tannery demand, low baseline sale floor, repair/construction leather sinks |
| Vegetable-tanned leather | Player and ordinary tanning | Flexible construction and repair | **MANAGEABLE TO HIGH** | Equipment demand, repairs, ordinary market competition, no guaranteed processing profit |
| Ordinary wood | Woodcutting and ordinary forestry | Repair/public work, fuel conversion, market, later approved uses | **HIGH** | Three-to-one charcoal ratio, demand routing, low buyer floor, event yield and source-density playtest |
| Tannin-rich bark | Eligible woodland work and ordinary forestry | Tanning | **HIGH / DEPENDENT ON HIDE FLOW** | One bark per two hides, eligibility mix, tannery demand; never bark-only gathering |
| Wood charcoal | Fuel workers and trade | Smithing construction/refurbishment | **MANAGEABLE** | Three-to-one conversion and imported supply prevent easy monopoly; Smithing demand prevents irrelevance |
| Rendered tallow | Renderer and husbandry flow | Finishing and maintenance | **MANAGEABLE** | Four-to-one eligible-flow ratio and recurring bounded care |
| Flax bundle | Household agriculture and trade | Ordinary textile conversion | **MANAGEABLE** | Three-bundle batch and competing household/clothing context |
| Linen textile | Ordinary conversion and trade | Lining, joining, patches | **MANAGEABLE** | Broader demand than tow; recurring repair |
| Flax tow | Ordinary conversion and trade | Damping, padding, renewal | **MANAGEABLE; SURPLUS WATCH** | One tow per three bundles; do not invent tow sinks if equipment forms use little damping |
| Plain carbon steel stock | Imports and stored trade | Smith-led construction/refurbishment | **SCARCITY WATCH** | Multiple ordinary suppliers, repair prioritization, stock acceptance; no forced local ore |

## 6. Anti-bloat result

No new inventory state is required. The model uses relationships among the approved goods:

- source-sized edible units;
- one standardized raw-hide unit;
- one standardized ordinary-wood unit;
- one bark unit per eligible work;
- shared batches for leather, charcoal, tallow, linen, and tow;
- direct steel-stock consumption.

Waste, raw fat, prepared hide, tanning liquor, thread, panels, padding packages, stock blanks, repair kits, ash, and scrap remain unrepresented.
