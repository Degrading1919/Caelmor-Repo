# Caelmor — Lowmark Hunting Progression Architecture

**Status:** proposal-stage architecture for the Lowmark v1 gathering and supply economy. All selections in this document are provisional pending Creative Director audit. It defines progression identities, opportunity patterns, output relationships, and placement requirements before final species, nodes, levels, yields, timings, tools, or implementation data.

## Authority and boundaries

This proposal follows the approved gathering and material chain:

```text
eligible living game
→ locate, approach, hunt, and field-dress
→ edible relationship where appropriate
→ source-conditional guaranteed raw hide where appropriate
→ suitable fat may enter ordinary rendering
```

It preserves these constraints:

- Lowmark is the only full v1 region and is culturally neutral toward Hunting rather than defined by a hunter culture.
- Raw hide comes only from eligible hide-bearing animals under successful recovery conditions. It is never a universal or weighted random drop.
- The edible output remains a relationship for later Cooking design. No meat, cut, or recipe catalog is created here.
- Suitable fat may enter ordinary rendering, but it is not a required player inventory state and there is no gather-tallow action.
- Horns, bones, sinew, organs, trophies, and similar outputs remain excluded until a separate design proves real sinks.
- No final species, resource tiers, exact levels, XP, timings, yields, success rates, tool tiers, respawn behavior, routes, or locations are selected.
- Hunting does not introduce Trapping, Tracking, Husbandry, or another player skill.
- S01 ranged scope remains deferred. This proposal creates no ranged material demand.
- Ordinary husbandry and animal processing remain legitimate alternate sources of raw hide and rendering feedstock.

## Provisional architecture decision

### Selected: five-phase opportunity resolution with bounded variation

Every Hunting opportunity may draw from five legible phases:

1. **Read** — identify current sign, target condition, habitat pressure, and access rules.
2. **Prepare** — choose an approach, route, and recovery plan appropriate to the opportunity.
3. **Approach** — use cover, terrain, timing, and target behavior to reach a viable encounter.
4. **Resolve** — complete the hunt through the later approved encounter system.
5. **Recover** — field-dress successfully, choose which useful relationships to retain or route, and leave the site responsibly.

The phases are a design grammar, not five mandatory clicks. Early opportunities can compress them into a short readable loop. Later opportunities become deeper by changing which evidence matters and how the phases constrain one another. Field dressing remains part of the opportunity and never becomes a detached carcass-processing grind.

### Alternatives considered

| Alternative | Benefit | Rejection reason |
|---|---|---|
| One interaction resolves hunt and all outputs | Lowest implementation burden | Leaves too little room for knowledge, approach, recovery, and stewardship to become meaningful without relying on larger numbers. |
| Separate tracking, combat, and carcass-processing activities | Makes every phase mechanically explicit | Risks hidden new skills, excessive interaction count, inventory clutter, and mandatory chore loops. |
| **Five-phase grammar with compressed early use** | Supports visible mastery while allowing economical implementation | **Selected provisionally.** It provides reusable structure without requiring every opportunity to expose every phase as a separate action. |

## Progression identity

Progression changes the player's relationship with the opportunity. It does not replace one animal with the same interaction and a superior hide.

| Progression band | Player identity | Knowledge and preparation | Approach and risk | Recovery and output decisions | Stewardship and economy |
|---|---|---|---|---|---|
| **Novice** | A careful learner who can complete a nearby, well-signposted hunt | Distinguishes fresh from stale sign, recognizes obvious eligibility, and brings basic recovery readiness | Uses clear cover and forgiving terrain; target behavior is readable and consequences of withdrawal are low | Learns that edible value, hide eligibility, and recoverable condition are separate facts; can recover straightforward qualified outputs | Works in open or guided opportunities near ordinary receiving points; learns that taking an animal creates a duty to use it |
| **Competent** | An independent hunter who chooses opportunities for purpose rather than proximity | Reads habitat use, simple weather or disturbance cues, and prepares for a desired output relationship | Chooses among approach lines and adapts to movement or concealment; difficult ground begins to affect recovery | Can prioritize food, intact hide, or safe delivery where these compete; plans onward processing before committing | Understands open, conditional, and temporarily closed access; balances household, market, and workshop demand |
| **Advanced** | A route-aware practitioner who connects ecology, recovery, and trade | Follows interrupted sign across habitat boundaries, recognizes pressure caused by people or predators, and stages recovery before contact | Handles wary or dangerous behavior, constrained visibility, waterlogged ground, or longer pursuit without treating risk as a pure stat check | Makes consequential keep, process, sell, or deliver decisions; preserves condition through route and preparation rather than receiving automatic superior output | Selects work that relieves crop, bank, or public-safety pressure without stripping a habitat; understands when an apparently profitable hunt should be refused |
| **Masterful** | A trusted specialist who can diagnose unusual opportunities and protect the surrounding economy | Interprets indirect sign chains, conflicting accounts, and short-lived opportunity windows; prepares fallback routes and custody before departure | Combines terrain knowledge, target behavior, restraint, and existing combat competence where necessary; avoids preventable collateral harm | Recovers useful relationships under difficult conditions and knows when damaged output should be downgraded, redirected, or left rather than magically restored | Can take bounded civic or custodian commissions, work within closures, and choose among food security, ecological pressure, and craft demand |
| **Practical Mastery** | A broadly capable Lowmark hunter whose advantage is judgment | Can identify the best viable method across the core opportunity set, including when not to hunt | Access to nearly all core practical patterns; later refinement improves reliability, routing, specialization, and exceptional opportunity handling | Can sustain dependable supply without creating a unique late material or mandatory post-mastery input | Serves as a trusted supplier or problem-solver while ordinary hunters, husbandry, and markets continue to matter |

After practical mastery, advancement should emphasize chosen specialization, difficult combinations of known constraints, cleaner recovery, route knowledge, and personal identity. It should not reserve an essential hide, food relationship, or equipment chain behind the final stretch.

## Bounded Hunting opportunity archetypes

The v1 architecture needs **six genuinely different opportunity patterns**. Final content may express them through a small shared fauna set; an archetype does not require a unique species or bespoke subsystem.

### H1 — Guided margin opportunity

**Progression role:** Novice foundation.

| Dimension | Requirement |
|---|---|
| Ecological function | A common target uses field edges, settlement margins, drainage margins, or other worked-land boundaries. |
| Read | Obvious sign and a locally explained reason for the opportunity. Eligibility for food and hide remains target-dependent. |
| Approach | One clear approach problem: cover, noise, or a simple movement window. |
| Recovery | Forgiving ground and nearby delivery make field recovery legible. |
| Stewardship | Open or explicitly guided access; taking beyond the stated purpose is discouraged. |
| Economic decision | Keep or sell useful outputs, or deliver against a household need. |
| Placement class | Worked-land margin within understandable reach of households, storage, or market flow. |
| What makes it distinct | Teaches the whole hunt-to-use relationship without disguising a tutorial target as a permanently optimal resource. |

### H2 — Crop-pressure response

**Progression role:** Novice to Competent; recurring civic usefulness.

| Dimension | Requirement |
|---|---|
| Ecological function | A target is feeding, sheltering, or moving through cultivated ground in a way that causes a current household or communal problem. |
| Read | Damage pattern, tracks, and household testimony identify the correct pressure; the nearest animal is not automatically responsible. |
| Approach | Agricultural boundaries, workers, livestock, or irrigation infrastructure limit safe movement and resolution. |
| Recovery | Useful recovery matters, but preventing further damage is also a successful civic outcome. |
| Stewardship | Permission is tied to the affected holding or stewarded field relationship, without settling exact office powers. |
| Economic decision | Immediate food need, hide delivery, and damage prevention can compete with open-market sale. |
| Placement class | Agricultural household zone and its habitat edge. |
| What makes it distinct | The purpose begins with a human need and evidence, not a resource node. It remains meaningful even when market prices are poor. |

### H3 — Concealed wet-ground opportunity

**Progression role:** Competent to Advanced.

| Dimension | Requirement |
|---|---|
| Ecological function | A target uses reeds, shallow channels, wet meadows, or soft banks where traces and footing behave differently from dry margins. |
| Read | Broken vegetation, water disturbance, crossing traces, and safe-ground knowledge matter more than a continuous trail. |
| Approach | Visibility, footing, water, and noise constrain the route; withdrawal remains valid when conditions deteriorate. |
| Recovery | Reaching and returning from the recovery site can be harder than making contact. Wet or fouled condition affects usability through explicit recovery logic, not a random hide roll. |
| Stewardship | Flood conditions, bank vulnerability, and temporary closures can make an otherwise eligible opportunity unavailable. |
| Economic decision | A shorter risky return can protect condition; a longer stable route protects the player and banks. Exact efficiency remains later tuning. |
| Placement class | Plausible wet habitat outside supernatural zones; **MAP VERIFICATION REQUIRED** before any channel or crossing is asserted. |
| What makes it distinct | Terrain changes reading, approach, and recovery together. It is not the margin opportunity with more health. |

### H4 — Route-crossing or moving-range opportunity

**Progression role:** Advanced knowledge and planning.

| Dimension | Requirement |
|---|---|
| Ecological function | A target moves between feeding, shelter, or watering areas rather than occupying a fixed spawn-like site. |
| Read | The player infers a viable window from several signs and local knowledge; exact routes remain unplaced. |
| Approach | Preparation and interception matter more than direct pursuit. A missed window should redirect play rather than demand idle waiting. |
| Recovery | The likely recovery route and downstream buyer must be considered before interception. |
| Stewardship | Local pressure, recent take, and crossing safety can redirect or close the opportunity. |
| Economic decision | The player weighs current demand and delivery burden against a more convenient stationary opportunity. |
| Placement class | Habitat transition or broad movement corridor; **MAP VERIFICATION REQUIRED** for any future route claim. |
| What makes it distinct | Knowledge converts movement into opportunity. It rewards route understanding without requiring a population simulation or real-time migration schedule. |

### H5 — Threat-complicated recovery

**Progression role:** Advanced to Masterful risk integration.

| Dimension | Requirement |
|---|---|
| Ecological function | An otherwise ordinary eligible target occupies ground complicated by predators, raiders, unstable terrain, or another grounded hazard. |
| Read | The player must distinguish target sign from hazard sign and decide whether the opportunity remains responsible. |
| Approach | Existing combat or avoidance systems may intervene, but combat alone does not complete Hunting or guarantee intact recovery. |
| Recovery | Delayed or careless recovery can make some relationships unusable. No supernatural source improves the yield. |
| Stewardship | Hazard response does not grant unrestricted access or excuse waste. Custodians may close the ground rather than ask for extermination. |
| Economic decision | High apparent value is weighed against preparation, damage risk, and the possibility of returning without usable craft output. |
| Placement class | Ordinary habitat overlapping an established danger context; no Great War remains, Wraiths, or magical creatures become renewable material sources. |
| What makes it distinct | Risk affects whether and how the useful source can be recovered. It is not a combat drop table relabeled as Hunting. |

### H6 — Stewardship commission

**Progression role:** Masterful and Practical Mastery; enduring post-mastery identity.

| Dimension | Requirement |
|---|---|
| Ecological function | A household, steward, market authority, or other later-approved custodian needs a bounded response to pressure, safety, food demand, or evidence of imbalance. |
| Read | Accounts may conflict. The hunter verifies the condition and may recommend delay, redirection, or closure rather than accepting the premise. |
| Approach | Draws on one or more established patterns instead of adding a new minigame. |
| Recovery | Custody and destination matter: household food, tannery hide, renderer flow, or market sale may be the legitimate outcome. |
| Stewardship | Permission is explicit and temporary. Exact authorizing office remains unresolved with governance. |
| Economic decision | The player chooses a defensible response whose value includes public service, not merely maximum material recovery. |
| Placement class | Reuses established habitat classes and receiving interfaces. It does not require a special mastery-only biome. |
| What makes it distinct | Mastery is judgment under competing needs. The opportunity can conclude with a hunt, a redirected hunt, or a justified refusal without becoming an investigation quest. |

## Opportunity composition and variation

Content production should vary a small set of dimensions across these archetypes:

| Dimension | Useful variation | Prohibited shortcut |
|---|---|---|
| Target behavior | feeding, bedding, crossing, fleeing pressure, defending space | identical stationary interaction with a renamed target |
| Evidence | tracks, disturbed crops, broken cover, water traces, witness account | opaque hidden roll that reveals no learnable information |
| Approach constraint | cover, noise, footing, wind or disturbance, safe firing/contact line if later relevant | higher skill requirement as the only difference |
| Recovery constraint | ground, distance, contamination, interruption, safe return | weighted raw-hide drop from an eligible intact source |
| Access state | open, guided, conditional, commissioned, temporarily closed | permanent arbitrary lock with no world explanation |
| Purpose | food, crop protection, public safety, craft input, market supply | XP-only opportunity |
| Destination | household, market, tannery, renderer handoff, personal storage | unique vendor for each target |

An authored opportunity should combine only the dimensions needed to create a readable decision. Complexity comes from relationships among two or three constraints, not from stacking every modifier.

## Output and economic architecture

### Approved useful relationships

| Relationship | When it exists | Player-facing value | Downstream destination |
|---|---|---|---|
| **Edible output** | The target and recovered condition support food use | Self-supply, household delivery, market sale, or later Cooking use | Cooking and ordinary food economy; catalog deferred |
| **Raw hide** | The target is hide-bearing and recovery conditions succeed | Leatherworking input, tannery supply, sale, or storage | Player Leatherworking or ordinary tanners |
| **Suitable fat flow** | The animal and legitimate recovery produce suitable rendering feedstock | Routed value through an ordinary renderer; not a required inventory item in this chain | Ordinary rendering, returning as rendered tallow |
| **Civic service value** | The opportunity addresses verified crop, safety, or stewardship pressure | Access, trust, demand fulfillment, or ordinary compensation structure to be designed later | Households, custodians, and market relationships |

### Keep, process, sell, and supply choices

- **Keep:** retain represented or later-approved outputs for personal processing or use.
- **Process:** send raw hide into player Leatherworking; the edible relationship awaits its Cooking pass.
- **Sell:** circulate raw hide or future edible goods through ordinary trade rather than requiring self-processing.
- **Supply:** fulfill a household, tannery, renderer, or bounded civic demand. This is an economic destination, not a new contract-management system.
- **Decline or leave:** abandon a hunt when recovery would be wasteful, unsafe, or contrary to a closure. The design must not reward taking unusable animals merely for XP.

### Hunting beyond Leatherworking

Hunting remains worthwhile through four independent reasons:

1. it contributes to a future food and Cooking economy;
2. it can route legitimate feedstock into recurring tallow maintenance supply;
3. it addresses household, agricultural, and public-safety pressures;
4. it provides self-supply, trade, and knowledge-based routing choices even when the player buys leather.

No extra biological inventory category is needed to achieve these roles.

## Placement requirements

| Placement class | Opportunity support | Required context | Must remain unresolved |
|---|---|---|---|
| Worked-land margin | H1, H2 | Visible relationship among habitat, households, crop pressure, and receiving points | Exact field, village, route, and count |
| Managed riverside or wet meadow margin | H1, H3 | Stable enough for ordinary fauna; bank use, flooding, and recovery risks are legible | Exact channel or crossing; **MAP VERIFICATION REQUIRED** |
| Reed or wet-ground habitat | H3, H5 | Concealment and footing affect both approach and recovery; not every wet space is a Wraith site | Exact fen boundary; **MAP VERIFICATION REQUIRED** |
| Habitat transition or movement corridor | H4 | Two plausible habitat needs create movement and interception logic | Exact movement route and schedule; **MAP VERIFICATION REQUIRED** |
| Hazard overlap | H5 | An ordinary ecological opportunity intersects grounded risk without becoming supernatural harvesting | Exact hazard and encounter composition |
| Custodian-directed area | H2, H6 | A clear household or civic need and a readable permission state | Exact authority and governance power |

The same broad area may support different archetypes under different conditions, but the content blueprint should never present all targets as permanent resource fixtures. Environmental signs, local testimony, working boundaries, and receiving destinations should explain why an opportunity exists.

## Solo-developer content model

The six archetypes can be supported through shared systems and authored parameters:

- one reusable evidence vocabulary with contextual combinations;
- one approach framework that allows terrain and behavior to change the viable method;
- one encounter handoff compatible with later approved Hunting or existing combat resolution;
- one recovery framework with source eligibility and condition checks;
- a small set of access states;
- shared market, household, tannery, renderer, and storage destinations;
- authored opportunity records that combine an archetype, habitat context, target eligibility, and destination demand.

Distinctive content should come from a few authored relationships and visible environmental cues. The architecture does not require bespoke AI, a continent-scale animal simulation, individual carcass inventories, dynamic market pricing, or a unique interface for each animal.

## Anti-reskin audit

| Test | Result | Reason |
|---|---|---|
| Does progression change what evidence the player reads? | **STRONG** | Sign advances from obvious traces to interrupted chains, habitat inference, and conflicting accounts. |
| Does progression change preparation? | **STRONG** | Later work requires route, recovery, destination, access, and hazard planning. |
| Does progression change approach? | **STRONG** | Margins, wet ground, movement windows, and hazard overlap create different constraints. |
| Does progression change output decisions? | **STRONG** | Food, hide, rendering flow, condition, and civic purpose can pull in different directions without adding resource types. |
| Is later content merely a better hide? | **STRONG — avoided** | No hide tiers or unique mastery material are introduced. Value comes from opportunity, condition, use, and knowledge. |
| Is routine repetition still possible? | **STRONG** | H1–H3 support dependable familiar loops; mastery improves method choice and routing. |
| Is complexity readable? | **PARTIAL pending implementation** | The five-phase grammar is clear on paper, but interface and sign readability require prototype validation. |

## Scope and dependency audit

| Risk | Control | Result |
|---|---|---|
| Hidden Tracking or Trapping skill | Reading and preparation are Hunting capabilities within one skill | **Controlled** |
| Hunting exists only for raw hide | Edible, rendering, civic, self-supply, and trade relationships are integral | **Controlled** |
| Player becomes sole animal supplier | Husbandry and ordinary animal processing remain active | **Controlled** |
| Ordinary supply makes Hunting irrelevant | Hunting offers self-supply, responsive opportunity value, route knowledge, and civic purposes | **Controlled, requires later economic tuning** |
| Dangerous fauna becomes a combat drop table | Hunting owns eligibility, approach, and recovery; combat alone cannot grant qualified outputs | **Controlled** |
| Biological output bloat | Only approved relationships are exposed; additional parts require demonstrated sinks | **Controlled** |
| Mandatory chore processing | Field recovery is integrated and compressible; fat can route without a required inventory item | **Controlled** |
| Supernatural resource drift | All outputs come from ordinary eligible animals; supernatural phenomena confer no resource | **Controlled** |
| Governance contradiction | Uses abstract permission states and custodians; exact office powers stay open | **Controlled** |
| Exact map invention | Placement remains by class, with map verification flags | **Controlled** |
| Multiplayer assumptions | Opportunities, supply, and closures require no player market or group encounter | **Controlled** |
| Solo-developer burden | Six patterns share evidence, access, recovery, and receiving systems | **Controlled** |

## Provisional decisions and morning review

### Recommended for approval

1. **Six-opportunity portfolio:** H1 guided margin, H2 crop-pressure response, H3 concealed wet-ground, H4 route-crossing, H5 threat-complicated recovery, and H6 stewardship commission.
2. **Five-phase grammar:** Read, Prepare, Approach, Resolve, Recover, with early opportunities allowed to compress phases.
3. **Knowledge-first progression:** later mastery combines evidence, access, route, risk, recovery, and destination rather than substituting superior hides.
4. **Shared content model:** archetypes reuse systems and habitat classes rather than demanding unique species and mechanics.

### Genuine Creative Director review items

1. **Encounter ownership:** provisionally, Hunting owns reading, approach, eligibility, and recovery; an approved normal combat encounter may resolve dangerous contact, but combat alone never produces Hunting recovery. Alternative: all hunt resolution uses a dedicated noncombat interaction. The selection affects combat integration and implementation scope.
2. **Recovery granularity:** provisionally, field dressing is a meaningful recovery phase that can be compressed into the opportunity and is never a separate repeatable station. Alternative: resolve recovery automatically after a valid hunt. The selection affects how much condition and preparation can matter without adding inventory bloat.
3. **Opportunity-state model:** provisionally, use the shared authored vocabulary of open, guided/purpose-limited, reserved/commissioned, disrupted/recovery, and unsafe/closed states without a live animal-population simulation. An ordinary instance receives at most one altered state unless story-critical. Alternative: omit temporary ecological closure and use only fixed access. The selection affects stewardship visibility and content-state burden.

### Safe to defer

- final species and eligibility tables;
- exact signs, tools, encounter controls, recovery conditions, and failure handling;
- exact access authorities, seasonality, and closure triggers;
- final edible inventory catalog and Cooking destinations;
- quantities, yields, timings, XP, prices, and demand tuning;
- exact sites, routes, corridors, and opportunity counts;
- whether suitable fat is ever represented elsewhere in the wider economy before ordinary rendering;
- all S01 ranged implications.

## Hunting architecture result

The proposal supplies six distinct opportunity patterns across the approved progression identities. It keeps raw hide deterministic when physically eligible, gives Hunting several reasons to exist beyond Leatherworking, preserves ordinary animal supply, and creates mastery through knowledge and judgment rather than resource substitution.

**HUNTING ARCHITECTURE: READY FOR INTEGRATED ECONOMY AUDIT.**
