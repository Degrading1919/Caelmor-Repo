# VS_ResourceNode_Balance.md
### Vertical Slice — Resource Node XP, Yield, and Early-Level Pacing
### Role: Progression & Economy Designer
### Inputs: VS_ResourceNodes.json
### Purpose: Define XP tuning, resource yields, and early-level skill pacing for Mining, Woodcutting, and Hunting in the Vertical Slice.

---

# 1. Design Principles for VS Resource Balance

These rules derive from Caelmor’s progression philosophy (“slow but rewarding, never slow and empty”) and the need for early mastery signals without grind walls.

### Core Intent:
- Players should reach **Level 2** in each gathering skill through natural traversal of the VS.
- Level 3 should be reachable only for players who intentionally gather extras.
- Yields must feel meaningful but not exploitable; no high-density “corridors.”
- Respawn timers must prevent infinite-loop farming inside the small VS zone.
- XP gains must reinforce satisfaction without creating MMO-like grind pacing.

---

# 2. Node Set (from VS_ResourceNodes.json)

| Node ID | Type | Resource | Yield | Respawn | Skill |
|---------|------|----------|--------|----------|--------|
| vs_iron_vein_01 | Ore | Lowmark Iron Ore | 1–3 | 90s | Mining |
| vs_tree_01 | Wood | Lowmark Log | 1–2 | 60s | Woodcutting |
| vs_small_game_01 | Wildlife | Raw Meat | 1 | 45s | Hunting |

These are the *only* resource nodes required for the VS.

---

# 3. XP Values (Final Approved for VS)

XP must be high enough to indicate progress but low enough to avoid unintentional overshoot.

## 3.1 Mining XP
| Action | XP |
|--------|-----|
| Mine Iron Vein | **3 XP** |

Rationale:
- 2–3 nodes during traversal → ~6–9 XP  
- Level 2 target XP = ~10 XP (VS pacing)  
- Ensures player hits Mining Level 2 without grinding.

---

## 3.2 Woodcutting XP
| Action | XP |
|--------|-----|
| Chop T1 Tree | **2 XP** |

Rationale:
- Logs are used for arrows; loop must feel lightweight.
- 4 nodes in VS → ~8 XP  
- Level 2 reached naturally.

---

## 3.3 Hunting XP
| Action | XP |
|--------|-----|
| Harvest Carcass (Furrow Boar or Small Game) | **2 XP** |

Rationale:
- Hunting is high satisfaction but must not outpace others.
- 3–4 wildlife encounters provide ~6–8 XP.

---

## 3.4 Cooking XP (for completeness)
| Action | XP |
|--------|-----|
| Cook Raw Meat → Cooked Meat | **3 XP** |

Rationale:
- Completing one full meal teaches Cooking’s utility early.
- Not tied to nodes, but dependent upon hunting.

---

# 4. Resource Yields & Variance

Resource yields must reinforce the feeling of “every node matters” while still requiring a few nodes per recipe.

## 4.1 Iron Vein Yield
| Yield | Chance |
|--------|---------|
| 1 ore | 35% |
| 2 ore | 45% |
| 3 ore | 20% |

Outcome:
- Average ~1.85 ore per node.
- Training Sword chain requires: **2 bars (→ 4 ore)**.  
Player will naturally gather the required amount from 2–3 nodes.

---

## 4.2 Tree Yields
| Yield | Chance |
|--------|---------|
| 1 log | 50% |
| 2 logs | 50% |

Outcome:
- Arrows require logs → shafts → arrows.  
- Early ranged users can produce ~20–30 arrows without grinding.

---

## 4.3 Wildlife Yields
Consistently:
- **1 Raw Meat**  
This is intentional—simple, no-RNG interaction for new players.

Outcome:
- Ensures Cooking is straightforward and predictable.
- Reinforces Hunting + Cooking synergy.

---

# 5. Early-Level Pacing Targets (VS)

These are the explicit vertical slice pacing goals for gathering skills.

## 5.1 Level Curve (VS-Only)
To create predictable pacing across all three gathering skills:

| Level | Total XP Required |
|--------|----------------------|
| 1 → 2 | **10 XP** |
| 2 → 3 | **25 XP** |

VS only expects reaching Level 2.

---

# 6. Expected Player Progression Through Zone

### Mining:
- 2–3 ore nodes encountered naturally → **6–9 XP**
- Crafting loop gives an additional Smithing progression point.
- Player reliably reaches **Mining 2**.

### Woodcutting:
- 3–4 trees encountered → **6–8 XP**
- Enough logs for multiple batches of arrows.
- Player reaches **Woodcutting 2**.

### Hunting:
- 3–4 wildlife encounters → **6–8 XP**
- Cooking 2–3 meats → +6–9 XP  
- Player reaches **Hunting 2** and likely Cooking 2.

Result:
- All three gathering skills reach Level 2 with **no grinding**.
- Cooking may reach Level 2 slightly earlier due to crafting XP.

---

# 7. Respawn Timing Rationale (Economy Perspective)

| Node Type | Respawn | Rationale |
|-----------|----------|------------|
| Ore | 90s | Prevents standstill farming in small zone; encourages traversal. |
| Trees | 60s | Slightly faster since wood demand is higher (arrows). |
| Wildlife | 45s | Keeps Field Edges loop feeling alive; avoids empty spaces. |

Respawn times are intentionally *longer* than player-loot cycles but short enough to maintain a living-feeling world.

---

# 8. Anti-Exploitation Constraints

To prevent early-game resource corridor exploitation:

- No more than **2 ore nodes** are visible from any one position.
- Wildlife respawns stagger across 3 spawn points.
- No node is within 25m of another identical node (Whitebox Rule).
- XP per action is flat (no multi-node XP stacking).

---

# 9. Summary Table (Final VS Balancing)

| Skill | Node Type | XP / Action | Avg Yield | Expected XP (VS) | Expected Level |
|--------|------------|----------------|--------------|---------------------|----------------|
| Mining | Iron Vein | 3 | 1–3 (avg 1.85) | 6–9 | Level 2 |
| Woodcutting | T1 Tree | 2 | 1–2 | 6–8 | Level 2 |
| Hunting | Wildlife | 2 | 1 Raw Meat | 6–8 | Level 2 |
| Cooking | Cook Meat | 3 | — | 6–9 | Level 2 |

---

# 10. Notes for Pipeline & Coding Assistants

### For Pipeline Assistant:
- Confirm yield tables match Recipe_Schema expectations.
- Ensure XP awards are placed in node & crafting definitions (not hard-coded).

### For Coding Assistant:
- Implement XP awarding inside ResourceNode.cs → SkillSystem.
- Ensure respawn timers use host-authoritative clock.
- Add lightweight anti-macro debounce (1s min per interaction).

---

# End of Document
