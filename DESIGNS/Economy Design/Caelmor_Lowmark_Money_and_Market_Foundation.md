# Caelmor — Lowmark Money and Market Foundation

**Status:** Proposal-stage monetary and relative-value model
**Scope:** Currency faucets, sinks, local market behavior, relative material values, processing incentives, and arbitrage controls; no final currency name or price table

## 1. Monetary design rules

- Analysis uses neutral **value units**. No currency name is selected.
- Lowmark has local buyers, workshops, households, custodians, and traders rather than a global auction house.
- A baseline buyer prevents lawful ordinary goods from becoming stranded.
- The baseline buyer pays a modest floor and is not the best destination for bulk gathering.
- Higher value comes from real local demand, processing, useful equipment, repair, or bounded commissions.
- NPC production prevents player monopoly; player gathering and crafting remain worthwhile through self-supply, timing, knowledge, and demand access.
- Processing can add value but cannot guarantee profit after buying every input at retail.
- Fees exist only where a worker performs conversion, fitting, transport, storage, or repair that benefits the player.

## 2. Provisional relative values

These figures test relationships. They are not final prices.

| Good | Baseline buyer floor | Ordinary trade reference | Ordinary NPC retail reference | Economic role |
|---|---:|---:|---:|---|
| Edible unit | 1 | 3 | 5 | High-volume food value pending Cooking design |
| Ordinary-wood unit | 1 | 3 | 5 | High-volume repair, fuel, and general-use input |
| Tannin-rich bark | 2 | 7 | 11 | Specialist tanning input with bulk-pressure risk |
| Raw hide | 6 | 14 | 21 | Valuable perishable-to-stable transformation input |
| Vegetable-tanned leather | 11 | 24 | 34 | Stable construction and repair material |
| Flax bundle | 3 | 6 | 9 | Ordinary agricultural source good |
| Flax tow | 2 | 5 | 8 | Narrower padding/damping output |
| Linen textile | 5 | 11 | 16 | Broad lining/joining/repair output |
| Wood charcoal | 6 | 14 | 21 | Consumed Smithing heat input |
| Rendered tallow | 4 | 9 | 14 | Small recurring finishing and maintenance input |
| Plain carbon steel stock | 18 | 30 | 42 | Imported hard-construction and refurbishment input |

The reference column is a comparison point for ordinary local trade, not a guaranteed buyer price. Actual lawful demand may sit between floor and retail. Bounded commissions can value delivery or workmanship above the raw reference because they consume a specific need.

## 3. Ordinary processing fees and value formation

| Conversion | Input reference value | Service fee | Output reference value | Gross added value | Finding |
|---|---:|---:|---:|---:|---|
| 2 hide + 1 bark → 2 leather | 35 | 6 | 48 | 7 | Tanning rewards useful transformation, but raw sale remains valid |
| 3 wood → 1 charcoal | 9 | 3 | 14 | 2 | Small stable margin; fuel demand, not free multiplication, justifies processing |
| 3 flax → 2 linen + 1 tow | 18 | 5 | 27 | 4 | Joint outputs add value through distinct uses; tow can still oversupply |
| 4 eligible renderer relationships → 1 tallow | No raw-fat inventory value | 3 | 9 | Contextual | The player contributes legitimate flow and pays/settles ordinary labor; no gather-tallow action exists |

Player Leatherworking can perform tanning without an NPC tanning fee, but it spends skill time and still consumes the same hide/bark ratio. Fuel, textile, and rendering conversions remain ordinary labor rather than player crafting skills.

## 4. Raw, processed, crafted, and kept choices

### Raw sale

- Fastest route to currency and inventory relief.
- Pays the floor when local specialist demand is saturated.
- Makes HM2/HM5 and WM2 useful without forcing processing.
- Deliberately leaves value for a tannery, renderer, fuel worker, textile worker, or player craft.

### Processing

- Adds modest reference value when the player supplies inputs efficiently or meets current demand.
- Does not guarantee profit from inputs purchased at NPC retail.
- Creates bankable materials for later equipment and repairs.
- May be chosen for skill progression or self-supply even when immediate sale margin is small.

### Crafting

- Creates functional equipment and repair value.
- Baseline equipment buyers do not pay enough to turn purchased-retail inputs into infinite currency.
- Demand-bound commissions may pay for workmanship because the delivered item or repair fulfills an actual need.
- Aspirational commissions primarily reward identity and access; they are not repeatable currency printers.

### Keeping and banking

- Protects future construction and repair access.
- Avoids paying the NPC retail spread later.
- Has opportunity cost because the player declines current currency and uses storage capacity.
- Makes familiar low-level sources relevant when a future repair or batch is short by one ordinary unit.

## 5. Vendor-arbitrage checks

| Test | Buy-side cost | Sale-side return | Result |
|---|---:|---:|---|
| Buy 2 hide + 1 bark at NPC retail, pay tanning service, sell 2 leather to baseline buyer | 59 | 22 | **No arbitrage** |
| Buy 3 wood at NPC retail, pay fuel-worker service, sell charcoal to baseline buyer | 18 | 6 | **No arbitrage** |
| Buy 3 flax at NPC retail, pay textile service, sell 2 linen + 1 tow to baseline buyers | 32 | 12 | **No arbitrage** |
| Buy tallow from NPC, resell to baseline buyer | 14 | 4 | **No arbitrage** |
| Buy imported steel from NPC, resell to baseline buyer | 42 | 18 | **No arbitrage** |

At gathered floor values, processing is near break-even to modestly positive only after labor/service cost:

- tanning gathered inputs: floor opportunity 14 value, plus 6 service, produces a 22-value floor return;
- charcoal from gathered wood: floor opportunity 3 plus 3 service produces a 6-value floor return;
- textile conversion from floor-value flax: opportunity 9 plus 5 service produces a 12-value floor return.

This prevents guaranteed vendor profit while allowing processing to make sense for self-use, demand sales, and player-skill value.

## 6. Equipment and repair valuation rules

| Transaction | Proposed relationship |
|---|---|
| Baseline sale of finished equipment | At or below 60–75% of material reference value unless a specific buyer has real use; generic crafting cannot print money |
| Ordinary NPC retail equipment | Material reference plus workshop labor, fit, risk, and retail spread |
| Demand-bound equipment commission | Consumes specified material/equipment and pays a bounded labor premium; access and need limit repetition |
| NPC repair service | Replacement material at ordinary retail or supplied by player, plus labor/service charge |
| Player self-repair | Consumes the same represented materials and player time; avoids service labor, not material cost |
| Aspirational commission | Player contributes materials/craft and pays or earns a context-specific workshop settlement; no repeatable premium-resale loop |

The exact labor coefficient remains open until action times and equipment utility are tested.

## 7. Currency faucets

| Faucet class | World basis | Control |
|---|---|---|
| Baseline sale of ordinary goods | Households, traders, workshops, and ordinary market intake | Low floor value; bulk sale is convenient rather than optimal |
| Demand sale to processors | Tanners, renderers, fuel workers, repair shops, food users | Real input need and local demand; no unlimited premium buyer |
| Work and repair commissions | Disclosed civic, household, or workshop need | Bounded task/access; payment reflects labor and delivered value |
| Ordinary trade margin | Buying where supply is healthy and selling into a real shortage/demand | Local spread, transport/time, and no global auction certainty |
| Approved quest/reward payments | Existing narrative or civic completion where later specified | Authored and non-repeatable or bounded; no new reward source is invented here |

Material transfers between ordinary actors are not all currency faucets from the player’s perspective. Currency enters only when a world buyer, employer, or reward source pays the player.

## 8. Currency sinks

| Sink class | Player value received | Guardrail |
|---|---|---|
| Material purchases | Saves gathering time; supplies imported or missing inputs | NPC retail spread; ordinary supply prevents monopoly |
| Processing services | Converts wood, flax, eligible animal flow, or hides when the player does not own the transformation | Fee corresponds to real labor and may be avoided through player Leatherworking only where approved |
| Repair/refurbishment | Restores useful attached equipment | Consumes real material and labor; not a tax on elapsed time |
| Equipment/workshop purchase | Provides functional equipment, fit, or specialist work | Price reflects utility and labor; no prestige surcharge without value |
| Commission integration/fitting | Provides verified fit, inspection, and accountable workshop work | Paid once per actual commission or refurbishment, not as a recurring license |
| Useful transport | Moves bulky inputs or finished goods when it genuinely changes route choice | No mandatory fee on every bank visit |
| Useful storage service | Expands or organizes material access where storage has gameplay value | No arbitrary rent or loss timer |

Taxes, permit fees, listing fees, repair taxes, and nuisance transport charges are not introduced merely to delete currency.

## 9. Best-XP versus best-money separation

### Hunting

Using only baseline buyer floors:

| Method | Approximate bulk floor value/h | XP position | Money identity |
|---|---:|---|---|
| HM1 | ~24–27 | Low | Convenient food sale |
| HM2 | ~144–160 when hide-qualified | Low–moderate | Strong mixed raw supply |
| HM3 | ~25–27 | Moderate | Food route, not money leader |
| HM4 | ~19–20 at light non-hide profile | High | XP-focused |
| HM5 | ~144–162 plus renderer relationship | Moderate | Focused hide/animal-value money route |
| HM8 | ~129–137 continuous circuit | Highest | Strong bulk flow, below focused HM5 when ordinary hide/renderer value is realized |

HM8 remains best XP but not best focused money, self-supply, convenience, or reliability.

### Woodcutting

| Method | Approximate bulk floor value/h | XP position | Money identity |
|---|---:|---|---|
| WM1 | ~30–33 plus limited bark | Low | Convenient ordinary sale |
| WM2 | ~43–60 depending bark eligibility | Moderate | Focused bark/self-supply; can earn more through real tannery demand |
| WM3 | ~17–31 plus bounded public value | Low–moderate | Civic/repair demand rather than bulk |
| WM4 | ~55–78 depending bark eligibility | High | Broad self-supply and route value |
| WM6 | ~14–23 raw floor plus bounded commission value | High | Repair-purpose money when demand exists |
| WM8 | ~88–129 depending bark eligibility | Highest | Highest bulk floor pressure, but focused tannery/repair commissions may outperform it within bounded demand |

WM8 remains a dominance risk. It passes provisionally because its best gross outcome requires valid mixed-route ecology and high bark eligibility, while processor demand, commission pay, local intake, and market spreads are bounded. Exact price and intake testing must confirm that continuous WM8 bulk sale does not become both the best XP and dependable best money method.

## 10. RuneScape-like choice test

| Desired choice | Supported relationship |
|---|---|
| Train faster with less useful output | HM4/HM6 and WM7 emphasize XP/judgment over dependable focused supply |
| Gather or buy | Every player-facing material has ordinary supply or trade; imported steel is intentionally bought |
| Older material remains useful | Hide, bark, wood, linen, tow, charcoal, and tallow recur in later construction and repair |
| Route knowledge matters | HM8/WM4/WM8 reduce invalid work and duplicate returns without changing item tiers |
| Sell raw or process | Raw floors, modest conversion value, service fees, and downstream self-use all coexist |
| Best XP differs from best money | HM8 versus HM5; WM8 versus bounded WM2/WM6 demand, pending price verification |
| Familiar low-level area remains useful | HM1/HM3/WM1/WM2 retain convenient food, wood, bark, repair, and bank relationships |

## 11. Decisions and later tuning

No Creative Director decision is required to accept this monetary foundation. The value-unit table is an analytical test frame, not a final economy lock.

Later tuning must set:

- final currency name, if any;
- actual item prices and regional variation;
- NPC stock and intake behavior;
- local demand capacity and recovery;
- final equipment utility/labor values;
- storage and transport implementation;
- quest and commission payment amounts.
