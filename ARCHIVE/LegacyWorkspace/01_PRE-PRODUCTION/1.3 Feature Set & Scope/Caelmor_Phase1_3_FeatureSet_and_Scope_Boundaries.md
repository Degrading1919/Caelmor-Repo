# Caelmor — Phase 1.3 Deep-Dive  
Specification

Version: Full Deep-Dive (20–30 pages)  
Prepared by: Game Director & Producer  
Project: Caelmor – Mythic Medieval Online RPG

---

# SECTION A — CORE V1 SYSTEMS (Deep-Dive)

---

## 1. Character Movement System — Deep Breakdown

The movement system in Caelmor v1 prioritizes grounded medieval traversal and simplicity for both the  
player and developer.

Movement includes Walk and Sprint only, with Sprint using no stamina resource and imposing no  
mechanical penalty.

This ensures players always feel free to move without restriction and allows the world to be designed  
without artificial gating.

Vertical traversal does not use a jump button; instead, agility triggers are placed in the environment.

These invisible boxes allow contextual interactions like stepping up, vaulting, climbing short ledges,  
or hopping across gaps. This maintains clarity and reduces bugs related to freeform jumping.

Movement State Machine:

• Idle → Walk → Sprint (based on input)  
• Walk/Sprint → AgilityTrigger (auto-animation)  
• Sprint never canceled by stamina limitations  
• Player retains full camera control at all times  

Environmental Constraints:

• Level designers place AgilityTriggers anywhere traversal realism is desired.  
• Triggers store: animation type, exit location, facing angle.  
• Prevents “pixel-jumping” exploits and preserves world believability.  

Camera Interaction:

• Player-controlled zoom only.  
• No automatic camera adjustments based on combat or tight spaces.  
• Collision-correcting camera prevents clipping and disorientation.  

Developer Advantages:

• Reduced animation requirements.  
• No need to synchronize complex jump arcs.  
• Works perfectly in multiplayer without desync issues from jump-state mismatches.  

---

## 2. Combat System — Auto-Attack, Cooldowns, and Tick Model

Combat in Caelmor is designed around deliberate timing, readable telegraphs, and grounded medieval  
realism.

The game uses a tick-based combat loop inspired by traditional RPG timing models, ensuring  
consistency across multiplayer clients.

Auto-Attack Loop:

1. Player selects target.  
2. Character initiates attack animation.  
3. Hit resolution occurs on server-authoritative tick.  
4. Auto-attacks repeat automatically at the weapon's speed interval.  

Special Attacks:

• Each weapon type may include one or more special attacks with cooldowns.  
• Cooldowns operate independently of stamina (no visible stamina bar exists).  
• Specials create combat variety without overwhelming complexity.  

Ranged Combat:

• Hit accuracy is NOT player-aim driven.  
• Accuracy governed by bow material, arrow quality, skill level, distance, and target movement.  
• Prevents misclick frustration and removes twitch dependency.  
• Arrows and bolts follow predictable trajectories with slight assist.  

Combat Tick Timing:

• Tick rate defines combat event resolution globally.  
• Ensures deterministic results during multiplayer sessions.  
• Server always authoritative; clients display predicted feedback.  

Enemy AI Roles:

• Passive: Animals that ignore player unless attacked.  
• Aggressive: Hostile foes that engage when player enters their threat radius.  
• Defensive: Enemies that defend territory but do not pursue indefinitely.  

Enemies never flee at low HP to avoid frustration and kiting abuse.

Damage Calculation Pipeline:

1. Attack event triggered.  
2. Server checks hit chance.  
3. If successful → base weapon damage applied.  
4. Armor mitigation applied (material-driven).  
5. Final HP reduction applied.  
6. XP awarded based on skill and enemy attributes.  

Combat Design Intent:

• Players should focus on positioning, timing, preparation, and gear progression.  
• Combat remains grounded, approachable, and readable — not reflex-based.  

---

## 3. Stats, Armor, and Progression Model

Stats in Caelmor v1 reinforce grounded progression:

• Health Points (HP)  
• Armor Rating (AR)  
• Weapon Damage (WD)  
• Skill Levels (9 total v1 skills)  

No stamina bar is shown to the player. Although stamina may exist internally for future use,  
it plays no mechanical role in v1. Attack pacing is driven solely by weapon speed and cooldowns.

Armor:

• Heavy Armor (Smithing): iron → improved iron → early steel.  
• Light Armor (Leatherworking): crude fur → hide → leather.  

Each material tier creates visible progression without introducing rarity colors like “Common/Rare/Epic.”

Progression Philosophy:

• Progress tied to mastering skills and crafting.  
• Strongly influenced by OSRS-style resource progression, not KCD-style item quality.  
• Encourages exploration and material acquisition as primary advancement.  

---

## 4. Inventory System — Slot Model

Caelmor uses a slot-based inventory system without weight. This reduces complexity and focuses the  
player’s attention on gathering and crafting rather than micromanaging encumbrance.

Key Features:

• Every item occupies exactly one slot in v1.  
• No Tetris or item-size system (reserved for v1.5+ exploration).  
• No weight-based penalties.  
• Player freely rearranges items in the grid.  

Advantages for Players:

• Fast mental parsing.  
• Encourages collecting resources without friction.  
• Aligns with OSRS-inspired design while avoiding UI clutter.  

Advantages for Development:

• Extremely stable in multiplayer.  
• Easy to serialize and store.  
• Prevents inventory desync issues.  

Future Expansion (v1.5+):

• Optional item sizing (2×1, 2×2, etc.)  
• Pouches/backpacks via Leatherworking additions.  

---

## 5. Skills Included in v1 — Full Breakdown

### Combat Skills:

1. Melee — Auto-attacks, weapon mastery.  
2. Ranged — Bow/crossbow combat, stat-driven accuracy.  

### Gathering Skills:

3. Mining — Ore extraction; fuels Smithing.  
4. Woodcutting — Timber collection; fuels Fletching.  
5. Hunting — Fauna harvesting; produces meat, hides, sinew, feathers.  

### Crafting Skills:

6. Smithing — Metal armor, tools, melee weapons, arrowheads.  
7. Fletching — Bows, crossbows, arrow/bolt craft.  
8. Cooking — Food for recovery; uses meat from Hunting.  
9. Leatherworking — Light armor, quivers, basic straps.  

Skills form an interconnected early-game economy:

• Hunting → Leatherworking + Cooking + Fletching.  
• Woodcutting → Fletching.  
• Mining → Smithing → Weapons/Armor.  
• Smithing + Fletching + Leatherworking → Ranged progression loop.  

---

## 6. World & Region Design — Lowmark Vale Deep Dive

Lowmark Vale serves as Caelmor’s introductory region, designed to teach every major system  
naturally.

Biome Composition:

• Rolling lowlands, forest edges, shallow rivers, marshy borders.  
• Farmland ruins and remnants of the long war.  
• Wildlife essential for Hunting skill loops.  
• Caves and early-level mines to support Mining and Smithing.  

Design Pillars:

• Environment tells stories through ruins, debris, and architecture.  
• No clutter; no empty-for-empty's sake fields.  
• Mandatory handcrafted landmarks guide player navigation.  

Core POI Types:

• Villages & homesteads  
• Logging camps  
• Abandoned watchtowers  
• War shrines  
• Mines & quarries  
• Hunting grounds  
• Minor dungeons/skirmish spaces  

v1 includes ONLY Lowmark Vale to maintain development feasibility and quality.  
Thornfell Marches becomes v1.5 content.

---

## 7. Story & Quest Design — v1 Narrative Arc

The v1 narrative is structured around a three-act progression:

### Act I — Arrival & Learning the Land  
• Introduces skills, movement, survival.  
• Player becomes familiar with Lowmark culture and war aftermath.  

### Act II — Rising Tension  
• Bandits, corrupted fauna, and whispers of forbidden magic.  
• Players learn fragments of history about elemental schools.  

### Act III — Revelation  
• Final quests lead to the discovery of the Water Wizard.  
• Magic is revealed as outlawed, misunderstood, and returning.  
• Player receives symbolic magical artifact (non-functional).  

Quest Types:

• Skill introduction quests (Mining, Woodcutting, Hunting, Crafting).  
• Regional subplots involving local disputes.  
• Lore breadcrumbs referencing the Long War.  

---

## 8. Crafting Systems — Material Loops & Stations

Crafting is the backbone of Caelmor’s early-game progression.

Principal Loops:

Mining → Smithing → Weapons/Armor  
Woodcutting → Fletching → Bows/Arrows  
Hunting → Leatherworking → Armor/Quivers  
Hunting → Cooking → Food for survival  

Station Breakdown:

• Smithing Forge — Metals, melee weapons, heavy armor.  
• Fletching Bench — Bows, crossbows, arrows, bolts.  
• Leather Rack — Fur/hide/leather armor; quivers and straps.  
• Cooking Fire — Prepared food for HP restoration.  

Material Tiers in v1:

• 3–4 early-game tiers only (iron, better iron, early steel equivalents).  
• Prevents content bloat and maintains achievable balancing.  

---

## 9. Networking & Co-op — Architecture & MMO Path

Caelmor v1 uses host-authoritative co-op (2–8 players). This model is easy for a solo dev  
and forms a scalable foundation for eventual MMO infrastructure.

Key Principles:

• Host machine simulates the world tick.  
• All combat, AI, and inventory operations resolved server-side.  
• Clients act as input devices + visual feedback layers.  
• Host saves world; clients save characters.  

Tick Synchronization:

• Every combat interaction must resolve on the host's tick.  
• Clients receive predicted results; corrections are applied subtly.  

Future MMO Path:

v1 → Host-authoritative  
v1.5 → Dedicated servers  
v2.0 → Regional shards and persistent worlds  

Because the v1 architecture obeys server-authority principles, no rewrites are needed later.

---

# SECTION B — V1.5 FEATURE EXPANSION

• Thornfell Marches becomes the first major new region.  
• Introduction of Water Magic skill in minimal form.  
• Leatherworking expansions: pouches, bags, component satchels.  
• Optional Foraging or Fishing skill.  
• New enemies, recipes, and item tiers.  
• Expanded storylines tied to the Water Wizard arc.  

---

# SECTION C — FUTURE SYSTEMS

Long-term planned expansions include:

• Full elemental magic schools.  
• Faction systems and regional politics.  
• Massive world events and war-scale encounters.  
• Tailoring skill for cloth armor and ritual gear.  
• Hunting 2.0 expansions (without simulation limits).  
• Caravan trade routes.  
• Procedural encounters and regional mutations.  
• Large-scale PvP (opt-in only).  

