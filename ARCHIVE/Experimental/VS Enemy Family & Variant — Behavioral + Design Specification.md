VS Enemy Family & Variant — Behavioral + Design Specification (Markdown)

(Provide this file directly to Balance Analyst + Narrative Designer)

# Lowmark Field Goblins — Behavioral, Ecological, and Combat Role Specification
### Vertical Slice Enemy Family Expansion  
### Role: Gameplay Systems & Combat Designer  
### Sources: Lowmark Region Dossier, VS Whitebox, Phase 1 Combat Vision

---

# 1. Family Identity Summary
**Family ID:** `lowmark_field_goblins`  
**Region:** Lowmark Vale  
**Role:** Low-tier hostile faction; simple melee skirmishers  
**Tier:** Low  
**Behavior Type:** Skirmisher (light melee, predictable movement)

Field Goblins represent Caelmor’s baseline “everyday hostile” — simple intentions, readable behavior, and low cognitive burden. They are intentionally predictable so players can train melee timing and spacing without analyzing complex patterns.

---

# 2. Behavioral Profile (Family Level)

## 2.1 Core Behaviors (Universal to Family)
- **Aggro Range:** Short (6–8m)  
  Prevents surprise pulls and reinforces solo-friendly pacing.
- **Approach Behavior:** Direct walk-in; minimal repositioning  
  No strafing, circling, flanking, or AI complexity.
- **Attack Style:**  
  - 1 basic poke attack  
  - Cooldown ~2.8s (steady rhythm)  
  - Small forward step for clarity  
  - No combos, no stance changes  
- **Retreat Behavior:** None  
  Lowmark enemies do not flee; avoids frustration and chase microgames.
- **Leash Radius:** 12–15m  
  Matches VS whitebox encounter spacing.

## 2.2 Motivations (Lore-Aligned but Mechanically Minimal)
- Scavengers sustaining themselves on abandoned farmlands and creek-side ruins.  
- Opportunistic rather than coordinated — reflect Lowmark’s war-scattered leftovers.  
- Driven by hunger, territorial instinct, and opportunistic theft, not malice.

These motivations help narrative designers place Goblins naturally in ruined POIs without requiring heavy lore justification.

---

# 3. Combat Role (Family Level)

## 3.1 Intended Role: **Basic Melee Skirmisher**
- Trains early-game combat without overwhelming players.
- Teaches spacing and pull control in small, clear encounters.
- Works well in pairs only when intentionally spaced (8–12m) to avoid multi-aggro.

## 3.2 Difficulty Range Supported
- **Player Level Range:** ~Lv 1–12 (remains useful up to ~Lv 15)  
  Supports the game’s long-term progression pacing requirements.

## 3.3 Behavior Load
- Very light.  
- No animation reads required beyond a predictable poke wind-up.  
- Attack conveys intent through a single weight-shift pose.

Follows Phase 1 combat vision: **clarity > speed**, **intentional over reflex-based**. :contentReference[oaicite:4]{index=4}

---

# 4. Environmental Niche of Field Goblins

## 4.1 Where They Live
Based on Lowmark Vale regional dossier:  
- **Creek crossings, ruins, field margins, collapsed farms**  
- Edges of trade routes  
- Places where They can scavenge materials or ambush without planning

These match all VS whitebox POIs:
- **B. Creek Crossing** (bridge sentry)  
- **C. Farmstead** (primary pocket)  
- **E. Boundary Wall** (Lookout variant is adjacent family archetype)

## 4.2 Why They Fit Lowmark
Lowmark’s lore describes:
- War-torn land with lingering low-tier threats  
- Scavengers and deserter-aligned factions  
- Region recovering, but not tamed

Field Goblins represent:
- Everyday danger that is not catastrophic  
- Creatures shaped by Lowmark’s post-war scarcity  
- A believable low-tier foe in farmland ruins and water-adjacent scavenger spaces

---

# 5. Base Stats & Scaling Philosophy

Stats from Pipeline output:

```json
"base_stats": {
  "health": 20,
  "power": 5,
  "armor": 0,
  "speed": 1.1
}

5.1 Rationale

HP = 20:
Yields early TTK of ~6–10 seconds depending on gear — aligns with VS combat pacing.

Power = 5:
Deals mild chip damage; dangerous only if ignored.

Armor = 0:
Reinforces low-tier identity; avoids spongey feel.

Speed = 1.1:
Slightly faster than player walk but slower than sprint (Movement System) to allow kiting discipline.

5.2 Scaling for Levels 1–15

Variant scaling via +HP/+Power ensures:

Remains viable XP source

Does not become trivial instantly

Does not require complex mechanics to remain relevant

This supports Lowmark’s required role as a Level 10–15 viable training zone.

6. Variant: Field Goblin — Bridge Sentry
Variant Definition (Pipeline output)
{
  "id": "field_goblin_bridge_sentry",
  "family": "lowmark_field_goblins",
  "level": 2,
  "variant_modifiers": {
    "health": 4,
    "power": 1
  },
  "abilities": ["simple_poke"],
  "spawn_regions": ["lowmark_creek_crossing"]
}

7. Variant Behavioral Details
7.1 Behavior Summary

Stands watch near broken plank bridge at Creek Crossing.

Patrol radius: 2–3m (extremely small — keeps behavior predictable).

Reaction: Delayed aggro by ~0.3s after spotting player; reinforces fairness.

Attack:

simple_poke every 2.8s

Telegraph: brief shoulder-drop + forward lean

No secondary behaviors.

7.2 Stats After Modifiers

Health: 24

Power: 6

Armor: 0

Effective Danger: Still Tier 1 (basic hostile)

8. Environmental Niche — Variant Level
8.1 Why a Sentry Exists at the Bridge

The VS whitebox highlights the Creek Crossing as a choice point:

Bridge path = “combat-forward”

Creekbank path = “wildlife-forward”

Placing this Goblin variant here:

Reinforces player agency (“risk vs safe path”)

Sets expectations for Lowmark enemies: simple, honest, readable

Introduces the idea that Goblins scavenge and guard access points

8.2 Lowmark Lore Alignment

Lowmark Vale’s wartime ruins often found near bridges, mills, and creek lines.
The bridge is a natural scavenger spot for a lone Goblin digging through debris for salvage.
It also echoes the region’s themes of:

Caution

Survival

Practical territoriality

9. How This Enemy Supports Caelmor’s Combat Philosophy
9.1 Supports Pillar B (Grounded, Deliberate Combat)

Predictable

Slow attack rhythm

No feints

No mental overloading

Players learn:

Pull spacing

Cooldown rhythm

Gear progression impact

9.2 Supports Phase 1.1 Vision (Clarity & Fairness)

This enemy never surprises the player with:

Multi-hit chains

Irregular timing

Chaotic movement

This respects the requirement for clear telegraphs and fair behavior.

9.3 Supports Lowmark’s Tone (Recovering, Weathered Land)

Goblins are not alien invaders — they feel like creatures shaped by Lowmark’s hardship.
They inhabit the edges, ruins, and forgotten structures, echoing the region’s “quiet recovery.”
They reinforce Lowmark’s low-tier ecology described in the dossier.

10. Narrative Hooks for the QUESTLINE & NARRATIVE DESIGNER

The family provides natural narrative opportunities:

Goblin tracks or dropped scavenged goods at POIs

Micro-quests involving stolen tools, crops, or livestock scraps

Environmental storytelling (fence gaps, disturbed soil, half-made nests)

Rare variant with scrap-woven ornaments suggesting cultural fragments

Best used in:

Early skill introduction quests

Investigative encounters

Teach-and-reward loops for low-tier combat mastery