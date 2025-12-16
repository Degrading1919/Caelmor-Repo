# VS Quest Chain — “Learning the Land” (FINAL)
## Region: Lowmark Vale
## Vertical Slice Questline (Movement, Combat, Gathering, Crafting, Navigation)

---

## 0. Chain Overview

**Chain ID:** vs_learning_the_land  
**Quest Count:** 4  
**Primary NPC:** Rella, Ridge-Watch (optional if VS omits NPCs; see triggers)  

**Player-Facing Arc:**  
A practical local watcher asks you to verify whether the way down into the Vale is still safe after storms and skirmishes. In doing so, you learn how to move, fight, gather, craft, and navigate across the Lowmark test zone.

**Teaching Coverage:**

- **Movement & Agility:** Quest 1  
- **First Combat (Single Enemy):** Quest 2  
- **Gathering & Crafting Loop:** Quest 3  
- **Traversal & Mixed Roles Combat:** Quest 4  

---

## 1. Quest 1 — “The Ridge and the Road”

**Quest ID:** vs_q1_ridge_and_road  
**POI:** Overlook Ridge → Creek Crossing  
**Purpose:** Introduce basic movement and first agility-trigger.

### 1.1 Start Conditions & Triggers

- **Giver:** Rella, Ridge-Watch (NPC at Overlook Ridge), standing near a low stone marker.  
- **Start Trigger:**  
  - Player enters **trigger volume** `trig_overlook_spawn` AND interacts with NPC `npc_rella_ridgewatch`  
  - OR (fallback) auto-start when entering `trig_overlook_spawn` if NPC is omitted.

### 1.2 Player-Facing Text

**Quest Title:** The Ridge and the Road  

**Short Description (Log):**  
“Rella wants to know if the path down from the ridge still holds after the last storm. Step down carefully and reach the creek below.”

**Offer Dialogue (Rella):**  
> “Path’s been slipping since the rains.  
>  Do me a kindness—see if the drop still holds, and if the creek hasn’t swallowed the road.”  

**Completion Dialogue (Rella):**  
> “You’re back on your own feet and not in the water.  
>  That’s good news. The land’s still listening, even if it grumbles.”

### 1.3 Objectives & Triggers

1. **Reach the ridge descent point and step down.**  
   - Type: `location + interact`  
   - Target: `overlook_descent_trigger`  
   - Trigger:  
     - Player enters `trig_overlook_descent` volume  
     - Uses agility trigger `ag_step_down`  
   - Completion: Mark objective complete when agility animation finishes.

2. **Reach the Creek Crossing.**  
   - Type: `location`  
   - Target: `creek_crossing`  
   - Trigger:  
     - Enter `trig_creek_crossing_center`  

3. **Inspect the broken bridge plank.**  
   - Type: `interact`  
   - Target: `obj_broken_plank`  
   - Trigger:  
     - Interact with object `obj_broken_plank` at creek crossing.  

### 1.4 Rewards

- XP: `{ "movement": 5 }` (or flag as “world familiarity”)  
- Items: `1x dried_banner_thistle` (minor healing flavor item)

---

## 2. Quest 2 — “First Signs of Trouble”

**Quest ID:** vs_q2_first_signs  
**POI:** Creek Crossing (right bank)  
**Purpose:** Teach safe, readable first combat vs a single Tier 1 enemy.

### 2.1 Start Conditions & Triggers

- **Prerequisite:** Complete `vs_q1_ridge_and_road`.  
- **Giver:** Rella (same position) OR automatic handoff at creek.  

**Recommended Flow:**  
- On completion of Quest 1, Rella immediately offers Quest 2 if the player is still near the ridge.  
- Alternate: When player inspects the plank, auto-start Quest 2 with a short text popup.

### 2.2 Player-Facing Text

**Quest Title:** First Signs of Trouble  

**Short Description (Log):**  
“Tracks near the broken plank lead along the right bank of the creek. Follow them and deal with whoever’s been testing the crossing.”

**Offer Dialogue (Rella, if given at ridge):**  
> “See those markings on the plank?  
>  Goblins like to prod at soft places. Follow the prints along the bank and send one home limping.”  

**Completion Dialogue (Rella):**  
> “If there was one goblin, there’ll be more.  
>  Good that the first one met you instead of a caravan.”

### 2.3 Objectives & Triggers

1. **Follow the tracks along the right bank.**  
   - Type: `location`  
   - Target: `creek_right_bank`  
   - Trigger:  
     - Enter `trig_creek_right_bank` volume (simple soft waypoint).  
   - Optional: display faint track decals along this edge.

2. **Defeat a Field Goblin.**  
   - Type: `kill`  
   - Target: `enemy_field_goblin_v1`  
   - Count: `1`  
   - Trigger:  
     - OnDeath of Field Goblin within `trig_creek_right_bank`.

3. **Collect goblin scrap.**  
   - Type: `collect`  
   - Target: `item_goblin_scrap`  
   - Count: `1`  
   - Trigger:  
     - Auto-loot on goblin death OR interact with dropped item.

### 2.4 Rewards

- XP: `{ "combat": 10 }` (melee or ranged, based on weapon)  
- Items: `1x goblin_scrap` (used as flavor in Quest 3; can remain in inventory afterward)

---

## 3. Quest 3 — “Tools of the Trade”

**Quest ID:** vs_q3_tools_of_trade  
**POI:** Ruined Farmstead  
**Purpose:** Introduce gathering and crafting (ore → bar → simple weapon), plus equipping.

### 3.1 Start Conditions & Triggers

- **Prerequisite:** Complete `vs_q2_first_signs`.  
- **Start Trigger:**  
  - After Quest 2 completion, Rella references the ruined farmstead.  
  - Auto-start when the player enters `trig_farmstead_outer` or interacts with Rella again.

### 3.2 Player-Facing Text

**Quest Title:** Tools of the Trade  

**Short Description (Log):**  
“The farmstead ahead still hides shallow iron seams. Gather ore and forge yourself a simple edge before walking deeper into the Vale.”

**Offer Dialogue (Rella):**  
> “Scrap’s nothing on its own.  
>  There’s still iron in that old farmstead’s chimney rubble.  
>  Take a few chunks, work them at the fire, and carry something sharper than worry.”

**Completion Dialogue (Rella or system):**  
> “That’ll bite deeper than bare hands.  
>  Lowmark’s kinder when you meet it with steel.”

### 3.3 Objectives & Triggers

1. **Mine iron ore at the farmstead.**  
   - Type: `gather`  
   - Target: `node_iron_ore_t1_farmstead`  
   - Count: `1` (or `2`)  
   - Trigger:  
     - Player interacts with mining node `node_iron_ore_t1_farmstead` within `trig_farmstead_mine`.

2. **Smelt an iron bar.**  
   - Type: `craft`  
   - Target: `item_iron_bar_t1`  
   - Count: `1`  
   - Trigger:  
     - Player uses crafting station `station_farmstead_fire` with recipe `recipe_iron_bar_t1`.

3. **Craft a simple blade.**  
   - Type: `craft`  
   - Target: `item_simple_blade`  
   - Count: `1`  
   - Alternate acceptable target: `item_iron_knife_vs`  
   - Trigger:  
     - Craft completion event from same station.

4. **Equip the crafted weapon.**  
   - Type: `equip`  
   - Target: `item_simple_blade` (or `item_iron_knife_vs`)  
   - Trigger:  
     - Equipment change event where main-hand slot equals target item.

### 3.4 Rewards

- XP: `{ "smithing": 10, "mining": 10 }`  
- Items: Player retains the crafted weapon.

---

## 4. Quest 4 — “Through the Fields”

**Quest ID:** vs_q4_through_the_fields  
**POI:** Field Edges → Old Boundary Wall  
**Purpose:** Introduce navigation through open fields, optional hunting, and a final mixed-role encounter.

### 4.1 Start Conditions & Triggers

- **Prerequisite:** Complete `vs_q3_tools_of_trade`.  
- **Start Trigger:**  
  - Auto-start when the player exits Farmstead via `trig_farmstead_to_fields`,  
  - OR via dialogue with Rella if she is physically present near the farmstead gate.

### 4.2 Player-Facing Text

**Quest Title:** Through the Fields  

**Short Description (Log):**  
“Walk the field edge and see if the old boundary road still holds. Hunt if you like, then clear any trouble near the wall.”

**Offer Dialogue (Rella):**  
> “Last thing I need from you: walk the field edge, then the old boundary wall.  
>  If beasts are thick or blades are waiting, better we know it now.”  

**Completion Dialogue (Rella):**  
> “Wall still stands. Road still walks.  
>  That’s a good day for Lowmark.  
>  You’ve learned the land. It’ll treat you fair, if you keep listening.”

### 4.3 Objectives & Triggers

1. **Reach the Field Edges.**  
   - Type: `location`  
   - Target: `field_edges`  
   - Trigger:  
     - Enter `trig_field_edges_entry`.

2. **(Optional) Hunt a Furrow Boar.**  
   - Type: `kill`  
   - Target: `enemy_furrow_boar`  
   - Count: `1`  
   - Optional: `true` (quest can complete without this)  
   - Trigger:  
     - OnDeath of Furrow Boar within `trig_field_edges`.  
   - If killed, also grant `item_raw_boar_meat` for cooking.

3. **Reach the Old Boundary Wall.**  
   - Type: `location`  
   - Target: `old_boundary_wall`  
   - Trigger:  
     - Enter `trig_boundary_wall_entry`.

4. **Defeat the Lost Footman.**  
   - Type: `kill`  
   - Target: `enemy_lost_footman_vs`  
   - Count: `1`  
   - Trigger:  
     - OnDeath within `trig_boundary_combat`.

5. **Defeat the Goblin Lookout.**  
   - Type: `kill`  
   - Target: `enemy_goblin_lookout_vs`  
   - Count: `1`  
   - Trigger:  
     - OnDeath within `trig_boundary_combat`.

6. **Inspect the disturbed campfire ashes.**  
   - Type: `interact`  
   - Target: `obj_boundary_campfire_ash`  
   - Trigger:  
     - Interact with object once both enemies are dead.

### 4.4 Rewards

- XP: `{ "combat": 20, "hunting": 5 }` (grant Hunting XP only if optional step done)  
- Items:  
  - `1x field_checked_token` (simple flavor / display item)  
  - `1x raw_boar_meat` (if boar objective completed)

---

## 5. Chain Completion Summary

On completing **“Through the Fields”**, the player will have:

- Used **agility triggers** (ridge descent).  
- Engaged a **safe first combat** vs a single goblin.  
- Performed a **gather → craft → equip** loop.  
- Navigated the entire **VS S-curve** from ridge to boundary wall.  
- Fought a **mixed-role encounter** (Frontline Footman + ranged Lookout).  
- Touched on Lowmark’s tone: practical, cautious, bound to the land.

This chain is ready for implementation and for extraction into flat quest / dialogue schemas.
