1. Overview

The Vertical Slice quest chain is implemented using a server-authoritative event system.
Each objective completes when a corresponding gameplay event fires, and the QuestSystem advances the quest state.

This document defines:

The objective flow for each quest

The event hooks required for objective completion

Minimal rules for progression (no narrative, no UI spec)

2. Required Global Events

The following server-side events must be emitted by other systems:

Movement / Traversal

OnAgilityStep(stepId)

OnEnterZoneArea(areaId)

Interaction

OnInteract(objectId)

Combat

OnEnemyKilled(enemyId, familyId)

Loot & Inventory

OnItemLooted(itemId, qty)

Gathering

OnNodeHarvested(nodeId, itemId, qty)

Crafting

OnCraftCompleted(recipeId)

Equipment

OnEquipmentChanged(slot, itemId)

These events drive every objective in the Vertical Slice chain.

3. Quest 1 — “The Ridge and the Road”
Objective Flow

Reach the descent point & perform agility step

Reach Creek Crossing

Inspect the broken plank

Event-Hook Specification
Objective	Required Event	Event Condition
1	OnAgilityStep(stepId)	stepId == "ridge_downstep"
2	OnEnterZoneArea(areaId)	areaId == "creek_crossing"
3	OnInteract(objectId)	objectId == "broken_plank"
4. Quest 2 — “First Signs of Trouble”
Objective Flow

Follow the tracks along the right bank

Defeat 1× Field Goblin

Collect goblin scrap

Event-Hook Specification
Objective	Required Event	Event Condition
1	OnEnterZoneArea(areaId)	areaId == "creek_bank_tracks"
2	OnEnemyKilled(enemyId, familyId)	familyId == "field_goblin"
3	OnItemLooted(itemId)	itemId == "goblin_scrap"
5. Quest 3 — “Tools of the Trade”
Objective Flow

Mine Iron Ore

Craft 1× Iron Bar

Craft 1× Simple Blade or Iron Knife

Equip the crafted item

Event-Hook Specification
Objective	Required Event	Event Condition
1	OnNodeHarvested(nodeId, itemId)	itemId == "iron_ore"
2	OnCraftCompleted(recipeId)	recipeId == "smelt_iron_bar"
3	OnCraftCompleted(recipeId)	recipeId in ["craft_simple_blade", "craft_iron_knife"]
4	OnEquipmentChanged(slot, itemId)	slot == "weapon"
6. Quest 4 — “Through the Fields”
Objective Flow

Reach the Field Edges

(Optional) Hunt 1× Furrow Boar

Reach the Old Boundary Wall

Defeat the mixed encounter

Inspect the disturbed ashes

Event-Hook Specification
Objective	Required Event	Event Condition
1	OnEnterZoneArea(areaId)	areaId == "field_edges"
2 (Optional)	OnEnemyKilled(enemyId, familyId)	familyId == "furrow_boar"
3	OnEnterZoneArea(areaId)	areaId == "old_boundary_wall"
4	OnEnemyKilled(enemyId, familyId)	familyId in ["lost_footman", "goblin_lookout"] (must kill both)
5	OnInteract(objectId)	objectId == "old_campfire_ashes"
7. Quest Completion Conditions

A quest is considered complete when its last objective’s event hook fires and conditions are met.

All quests in the Vertical Slice are linear:

Objective N completes → advance to Objective N+1


Optional objectives do not block completion.

8. Required System Behavior
On any event:

QuestSystem evaluates all active quests for the player.

If the event matches the condition for the active objective, the objective completes.

Quest state advances to the next stage.

If no more objectives remain, the quest completes.

A quest update event is sent to the client UI.