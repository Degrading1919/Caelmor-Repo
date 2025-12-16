# VS Recipe Validation Report
Pipeline Assistant  
Stage 3.7 — Crafting Stations  
Date: Auto-Generated

## Schema References
- Crafting_Recipe_Schema_Modular_v2.1  
- Required fields: id, skill, required_level, station, ingredients[], result, time, xp

---

# 1. Summary of Validation Results

| Recipe ID            | Status   | Notes                                  |
|----------------------|----------|----------------------------------------|
| smelt_iron_bar       | VALID    | Fully schema-compliant                 |
| craft_training_sword | VALID    | Fully schema-compliant                 |
| craft_wooden_shaft   | VALID    | Multi-output OK; no issues             |
| craft_training_arrows| VALID    | Ammo batch crafting OK                 |
| cook_meat            | VALID    | Fully compliant                         |

---

# 2. Detailed Findings

## 2.1 smelt_iron_bar
- Matches schema exactly  
- XP and station correctly defined  

## 2.2 craft_training_sword
- No inconsistencies  

## 2.3 craft_wooden_shaft
- Multi-output quantity valid  

## 2.4 craft_training_arrows
- Training arrow batch (10) valid  

## 2.5 cook_meat
- Consumable crafting valid  

---

# 3. Final Assessment

All VS recipes are **100% schema-compliant**.  
No corrections required.

This set is now approved for:
- CraftingStation.cs implementation  
- Tick-based crafting integration  
- Inventory consumption logic  

