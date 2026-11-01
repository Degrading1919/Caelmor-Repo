# Lowmark Vertical Slice — Whitebox Zone Plan
### Zone Size: 150–250m (≈180m primary traversal length)
### Region: Lowmark Vale  
### Role: Vertical Slice traversal + combat + gathering testbed

This whitebox design draws from established Lowmark Vale lore, early-game ecology, and Caelmor’s core principles of grounded traversal, low-density encounters, and meaningful environmental storytelling.

---

# 1. Zone Overview

**Biome:** Fringe of the Lowmark Heartlands — overgrown farmland remnants, shallow creek, ruined structures, and low wildlife presence.

**Target Experiences:**  
- Intro traversal and agility-trigger validation  
- Two core combat pockets with fair spacing  
- Early resource loop: Mining, Woodcutting, Hunting, Cooking  
- Lowmark tone: quiet, recovering land with subtle war residue  

**Shape:** Linear-but-branching S-curve flow with 5 major POIs.

---

# 2. Text Map (Whitebox Layout)

            [NORTH]
                ▲
                │
     ┌──────────────────────┐
     │  A. Overlook Ridge   │
     │   (Spawn Point)      │
     │                      │
┌───────┘ Path P1 └─────────┐
│ │
│ B. Creek Crossing (Traversal POI) │
│ • shallow water │
│ • broken plank bridge │
│ • reed + log nodes │
│ │
│ P2 → to C │
│ │
│ C. Ruined Farmstead (Primary Encounter) │
│ • collapsed barn │
│ • cellar hatch mock │
│ • ore + hide resources │
│ │
└─────P3───────────┐ │
│ │
D. Field Edges (Hunting Loop) │
│ │
└─────────P4──────────────┘
to E
     E. Old Boundary Wall (POI + Combat)
     • broken stone sections
     • mining seam + campfire placeholder

---

# 3. POIs (Points of Interest)

## A. Overlook Ridge — Spawn & Orientation
**Purpose:** Safe start point with a region vista.  
**Whitebox Elements:**  
- Slight elevation block  
- 1–2 placeholder tree objects  
- Agility Trigger: “step down” onto descending path  
**Resources:**  
- Woodcutting Node (T1)

---

## B. Creek Crossing — Traversal POI
**Purpose:** Demonstrates shallow water, branching path, and agility triggers.  
**Whitebox Elements:**  
- Water plane with 5–10cm depth  
- Broken plank bridge props  
- Agility Trigger: step-over/step-up log  
**Resources:**  
- 1× Woodcutting Node  
- 1× Reed/Herb Node (Cooking starter)

---

## C. Ruined Farmstead — Primary Encounter POI
**Purpose:** Core VS combat pocket with readable spacing and early-game threat.  
**Whitebox Elements:**  
- Barn silhouette (primitive cube structure)  
- Collapsed roof (angled geometry)  
- Fenced field remnants (scattered posts, low obstacles)  
- Cellar hatch (non-functional for VS)  
**Enemies:**  
- 2× Field Goblins (Low-tier)  
- 1× Ash Hound (roaming patrol)  
**Resources:**  
- 1× Iron Ore Node near chimney rubble  
- 1× Hide/Carcass prop for Leatherworking flavor

---

## D. Field Edges — Wildlife & Low-Pressure Loop
**Purpose:** Introduce Hunting skill with low-threat fauna.  
**Whitebox Elements:**  
- Tall grass plane  
- Light tree line forming semi-open arena  
**Enemies / Wildlife:**  
- 1–2× Furrow Boars  
- Rare spawn: 1× Ash Hound  
**Resources:**  
- 2× Woodcutting Nodes  
- 1× Herb Node (Banner-Thistle flavor)

---

## E. Old Boundary Wall — Secondary Combat POI
**Purpose:** Mid-tier mixed encounter and Mining node test.  
**Whitebox Elements:**  
- 8–12m segment of cracked stone wall  
- Campfire placeholder (Cooking station mock)  
**Enemies:**  
- 1× Lost Footman  
- 1× Goblin Lookout  
**Resources:**  
- 1× Mining T1 Node (Exposed seam)

---

# 4. Traversal Routes

### P1 — Ridge → Creek  
- Downward slope with agility-trigger drop.  
- Teaches grounded traversal (no jump button).

### P2 — Creek → Farmstead  
- Two branches:  
  - Direct bridge route (quicker, combat-forward).  
  - Left creekbank route (wildlife-focused).

### P3 — Farmstead → Field Edges  
- Broken fence openings create natural funnels.  
- Smooth LOS transition from tight space to open field.

### P4 — Field Edges → Boundary Wall  
- Gentle elevation shift to stone ruins.  
- Clear silhouette landmark anchoring the zone’s end.

---

# 5. Combat Pockets (Intent, Density, Readability)

### Combat Pocket 1 — Farmstead  
**Threat Level:** Low–Mid  
**Composition:**  
- 2× Field Goblins spaced 8–10m apart  
- 1× Ash Hound patrolling a 12m arc  
**Design Notes:**  
- Player can pull targets individually.  
- Obstacles enable LOS manipulation.  
- Telegraphs must remain readable.

---

### Combat Pocket 2 — Boundary Wall  
**Threat Level:** Mid  
**Composition:**  
- 1× Lost Footman (slow approach, defensive role)  
- 1× Goblin Lookout (delayed aggro)  
**Design Notes:**  
- Demonstrates mixed roles.  
- Wall cover adds decision-making.  
- Slightly harder than Farmstead but still solo-friendly.

---

### Wildlife Encounters — Field Edges  
**Threat Level:** Low  
**Composition:**  
- 1–2× Furrow Boars  
- Rare Ash Hound  
**Design Notes:**  
- Supports Hunting XP loop  
- Avoids swarming behavior

---

# 6. Resource Distribution Summary

| Skill | Node Type | Count | Locations |
|-------|-----------|-------|----------|
| Woodcutting | T1 Logs | 4 | Ridge, Creek, Field Edges |
| Mining | Iron (T1) | 2 | Farmstead chimney, Boundary Wall |
| Hunting | Wildlife | 3–4 | Field Edges, Farmstead carcass |
| Cooking | Herbs/Reeds | 2–3 | Creek, Field Edges |
| Leatherworking | Carcass/Hounds | 1–2 | Farmstead, Field Edges |

**Density Guidelines:**  
- No exploitable farming corridor.  
- Nodes spaced 25–40m apart.  
- Each route provides 1–2 opportunities, never a chain.

---

# 7. Whitebox Implementation Notes (Unity)

**Geometry Requirements:**  
- Flat terrain plane with 2–3 height layers  
- Primitive cubes for structures & ruins  
- Simple water plane  
- Trigger boxes (agility triggers) at Ridge and Creek

**Testing Needs:**  
- LOS and AI pathing around barn + fences  
- Combat spacing validation  
- Ensure traversal works without a jump mechanic  
- Wildlife spawn smoothing (no bunching)

---

# 8. Zone Purpose Within Vertical Slice

- Validates movement cadence and agility triggers  
- Demonstrates deliberate, readable combat  
- Tests low-density enemy placement rules  
- Provides early-game resource economy loop  
- Establishes Lowmark’s grounded, recovering atmosphere

This zone is intentionally simple, handcrafted, and progression-aligned, reflecting Caelmor’s Phase 1 pillars and Lowmark Vale’s thematic identity.

