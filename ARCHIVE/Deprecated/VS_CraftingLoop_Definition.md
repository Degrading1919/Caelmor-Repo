# Vertical Slice Crafting Loop Definition
### Role: Progression & Economy Designer
### Document: VS_CraftingLoop_Definition.md
### Purpose: Define the minimal crafting loops for the Vertical Slice and describe their XP intent and progression impact.

---

# 1. Overview

The Vertical Slice (VS) requires a minimal but complete crafting ecosystem that teaches the player:

- How gathering feeds crafting  
- How crafting feeds combat readiness  
- How each early-game skill interacts with the others  
- How Caelmor’s progression philosophy (“slow but rewarding”) manifests at level 1–3  

This crafting loop must feel **meaningful**, not filler-based, and should reinforce the early-game fantasy of being an ordinary wanderer learning to survive in Lowmark Vale.

The VS uses **three foundational loops**:

1. **Ore → Bar → Training Sword** (Mining + Smithing)  
2. **Logs → Arrows** (Woodcutting + Fletching)  
3. **Meat → Cooked Meat** (Hunting + Cooking)

These loops are intentionally minimal, but they establish the core identity for Caelmor’s economy, gear progression, and skill system.

---

# 2. Minimal Crafting Loop Breakdown

## 2.1 Mining → Smithing → Training Sword
### Steps
1. Mine **Lowmark Iron Ore** from T1 ore nodes.  
2. Smelt **Iron Ore → Iron Bar** at a basic forge.  
3. Craft **Training Sword** using Iron Bars.

### Purpose
- Introduce the foundational gear progression loop.  
- Make the player feel the tangible benefit of crafting their own weapon.  
- Teach Smithing as a central early-game skill.

### Skill XP Intent
- Mining a node: **3 XP**  
- Smelting a bar: **4 XP (Smithing)**  
- Crafting the Training Sword: **8 XP (Smithing)**  

XP targets:
- Player should reach **Mining 2** after ~5–6 nodes.  
- Player should reach **Smithing 2** after 1–2 crafted bars and 1 sword.

### Progression Impact
- Unlocks the first real melee weapon for the player.  
- Establishes early-game mastery pattern: *gather → refine → craft → equip*  
- Creates a noticeable TTK improvement in VS combat encounters.

---

## 2.2 Woodcutting → Fletching → Arrows
### Steps
1. Chop **T1 Logs** from simple trees.  
2. Craft **Wood Shafts** at the fletching bench.  
3. Combine Shafts + Foraged Feathers (optional) → **Arrows**.

### Purpose
- Introduces ranged viability early, even though melee remains primary.  
- Teaches lightweight crafting chains.  
- Gives players a repeatable sink for wood materials.

### Skill XP Intent
- Woodcutting a tree: **2 XP**  
- Crafting Shafts: **3 XP (Fletching)**  
- Crafting Arrows: **5 XP (Fletching)**  

XP targets:
- Player should reach **Woodcutting 2** after ~8 logs.  
- Player should reach **Fletching 2** after crafting first 10–20 arrows.

### Progression Impact
- Gives the player a ranged fallback tool for Field Edges wildlife.  
- Smooths early combat difficulty against Ash Hounds and Goblins.  
- Establishes foundation for more complex bows/crossbows in v1.

---

## 2.3 Hunting → Cooking → Cooked Meat
### Steps
1. Hunt wildlife (Furrow Boars).  
2. Acquire **Raw Meat**.  
3. Cook meat at a campfire → **Cooked Meat**.

### Purpose
- Provide early-game sustain.  
- Model a simple, satisfying loop that rewards exploration.  
- Establish Cooking as a real utility, not filler.

### Skill XP Intent
- Harvesting carcass: **2 XP (Hunting)**  
- Cooking meat: **3 XP (Cooking)**  

XP targets:
- Player should reach **Hunting 2** after 4–6 carcasses.  
- Player should reach **Cooking 2** after 4–5 meals.

### Progression Impact
- Provides reliable healing during early combat pockets.  
- Trains the player early to gather ingredients across zone traversal.  
- Makes Cooking feel organically useful rather than grindy.

---

# 3. System-Level Progression Goals

These three crafting loops must collectively:

### 3.1 Teach the Early Economy Flow
Players learn:
- “I gather materials because they matter.”  
- “Crafting gives me a meaningful advantage.”  
- “Upgrading gear improves combat outcomes.”

### 3.2 Bridge the Skill XP Curve
Combined loops should raise multiple skills naturally to level 2–3:

| Skill | Expected Level After VS Completion |
|-------|-----------------------------------|
| Mining | 2–3 |
| Smithing | 2 |
| Woodcutting | 2 |
| Fletching | 2 |
| Hunting | 2 |
| Cooking | 2 |

No grinding required — progression is earned through normal zone traversal.

### 3.3 Support the VS Quest Chain
These loops enable the quest chain to require:
- gathering ore  
- crafting arrows  
- cooking a meal  
- forging a training sword  

Without introducing complexity or UI friction.

### 3.4 Support Gear + Combat Pacing
- Training Sword = first real spike in TTK efficiency  
- Arrows = ranged option to handle tricky pulls  
- Cooked Meat = let the player survive Boundary Wall encounter

---

# 4. Item & Recipe Dependencies (for Pipeline Assistant)

To support the minimal loops, the next assistant will require:

### 4.1 Items
- lowmark_iron_ore  
- iron_bar  
- training_sword  
- log_t1  
- wood_shaft  
- arrow_basic  
- raw_meat  
- cooked_meat  

### 4.2 Recipes
- smelt_iron_bar  
- craft_training_sword  
- craft_wood_shaft  
- craft_arrows_basic  
- cook_meat_basic  

---

# 5. Hand-Off Notes for Next Assistants

### For CONTENT TEMPLATE & PIPELINE ASSISTANT
- Produce schema-compliant `VS_Items.json` & `VS_Recipes.json`.  
- Ensure each recipe includes: input list, output item, station type, XP award, craft time.  
- Map skill XP awards exactly as specified above.

### For ENGINE-AGNOSTIC CODING ASSISTANT
- Implement crafting execution logic using simple:  
  `ConsumeInputs → SpawnOutput → AwardXP → OnCraftComplete()`  
- Ensure crafting consumes inventory slots according to the Slot Inventory rules.

---

# End of Document
