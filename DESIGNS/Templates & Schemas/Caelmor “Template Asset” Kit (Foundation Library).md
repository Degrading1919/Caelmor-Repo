# Caelmor “Template Asset” Kit (Foundation Library)
*A small set of reusable base assets so you can assemble most NPCs/props without starting from scratch every time.*

---

## 1) Character Foundation Kit (Everything depends on this)

### 1.1 Shared Rig
- **One shared humanoid skeleton/rig** (standard proportions for Caelmor)
- Consistent **socket / attachment points** (hands, back, belt, neck)

### 1.2 Base Body Meshes (Same rig, same topology)
Create **3 body templates** you can scale and reuse:
- **Average build**
- **Lean / wiry build**
- **Stocky / heavy build**

> Most NPC variety comes from these + scaling + clothing silhouettes.

### 1.3 Head Kit (Compatible neck seam)
- **6–10 head shapes** (subtle variation, grounded, not caricature)
- Optional small variants:
  - **2–3 nose variants**
  - **2–3 ear variants**

### 1.4 Hands + Feet Variants
- **Hands:** work-worn (bare), gloved-ready, optional “fine” hands
- **Feet:** standard foot + a boot-friendly variant if needed

### 1.5 Hair Kit (Modular, hood-friendly)
- **10–15 hairstyles** (low complexity, practical silhouettes)
- **5–8 facial hair pieces** (stubble, trimmed beard, short beard, etc.)

---

## 2) Wardrobe Modules (The real time-saver)
Build clothing as **swappable layers** that fit all base bodies.

### 2.1 Base Layer (Universal across regions)
- **Tunic / shirt** (2 cuts)
- **Trousers** (2 cuts)
- **Wrap / scarf**
- **Basic belt** + belt hardware (buckles, ties)

### 2.2 Mid Layer
- **Vest / jerkin**
- **Work apron**
- **Gambeson / padded jacket**
- **Simple robe layer** (for civic/religious roles)

### 2.3 Outer Layer (Highest silhouette impact)
- **Cloak** (short + long)
- **Hood** (2 shapes: tight + draped)
- **Coat / mantle** (1 “authority” silhouette)
- **Poncho / rain wrap** (travel + Mire)

### 2.4 Footwear + Gloves
- **Boots:** soft boot, hard boot, patched boot
- **Gloves:** none / work gloves / thin formal gloves

> Fast rule: keep base + mid mostly universal; encode region identity primarily in **outer layers**.

---

## 3) Props Library (Story objects that create uniqueness fast)

### 3.1 Carry Systems
- **Satchel** (strap)
- **Pouch set** (belt-mounted)
- **Backpack / frame pack**
- **Key ring**
- **Seal chain / badge chain**
- **Small ledger/book bundle**
- **Rope coil**
- **Hook**
- **Tool roll**

### 3.2 Everyday Tools
- **Lantern** (2 variants)
- **Torch bundle**
- **Tinder kit**
- **Hammer**
- **Chisel**
- **Tongs**
- **Sickle**
- **Small pick**
- **Shovel head**
- **Waterskin**
- **Ration bag**
- **Cup/flask**

### 3.3 Authority / Identity Props (Functional, not spectacle)
- **Staff / pole** with a **modular head socket**
- **Badge / medallion plates** (swap motifs via decals)
- **Ceremonial-but-practical variants** (e.g., caged ember-lantern top, wax seal stamp)

---

## 4) Material + Texture Template Set (Consistency across the world)
A small reusable library that makes everything cohesive.

### 4.1 Base Materials
- **Cloth:** coarse wool, linen, “fine cloth” (still restrained)
- **Leather:** raw, oiled, cracked
- **Metal:** dull iron, steel, brass, heat-blued (Emberholt), tarnished
- **Wood:** raw, sealed, charred
- **Stone / ceramic:** beads, stamps, small tokens

### 4.2 Wear / Decals (Reusable overlays)
- **Mud line** (boots/hem height variations)
- **Soot smears**
- **Ash dusting**
- **Water stains**
- **Repair patches / seam reinforcement**

> Even if fidelity upgrades later, this library locks in a unified world “hand feel.”

---

## 5) Region Overlay Kits (Small, high-impact differentiation)
Make **one overlay kit per region**: silhouette + texture, not a full wardrobe replacement.

### 5.1 Lowmark Overlay Kit
- Labor wear accents: apron variants, rolled sleeves, simple hood
- Utilitarian belts, field grime overlays

### 5.2 Thornfell Overlay Kit
- Scout cloak variant, ridge-weather wraps
- Repaired leather/cloth, climbing kit bits

### 5.3 Mire Overlay Kit
- Rain wrap / poncho variants
- Waterproofing layers, rot-stain decals
- Reed/cord bindings and lash points

### 5.4 Emberholt Overlay Kit
- Civic mantle/robe silhouettes, cleaner cuts with ash contrast
- Heat-blued fasteners
- Seal-chain motifs and civic iconography placements

---

## 6) Animation Starter Set (Optional, but high value)
Even for “standing NPCs,” a small set adds life.
- **Idle (subtle)**
- **Look/turn**
- **Gesture x2**
- **Interact (reach/hand-off)**
- **Sit / lean**
- **Walk (slow)**
- **Walk (normal)**

---

## 7) Template Prefabs + Assembly Rules (Non-art, saves massive time)
### 7.1 Standard NPC Prefab Structure
- Rig + body mesh
- Layered clothing slots
- Prop sockets
- Consistent material slot names

### 7.2 Socket Standard (example)
- `Hand_R`, `Hand_L`
- `Back`
- `Belt_L`, `Belt_R`
- `Neck`

### 7.3 Modularity Naming Convention
- Clear names for layers and variants so you don’t drown later:
  - `Body_Average`, `Cloak_Long_A`, `Hood_Drape_B`, `Boot_Patched_A`, etc.

---

## 8) Minimum “Start Tomorrow” List (Smallest viable kit)
1) Shared rig + **1 base body**
2) Base outfit set: **tunic + trousers + belt + boots**
3) **Cloak + hood + satchel**
4) **Lantern + tool roll**
5) Cloth/leather/iron materials + **soot/mud decals**
6) Then start generating NPC-specific turnarounds and assembling variants
