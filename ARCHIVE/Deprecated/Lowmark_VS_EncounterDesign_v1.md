# Lowmark VS Zone — Encounter Difficulty, Enemy Placement, and Combat Pacing
### Role: Gameplay Systems & Combat Designer  
### References: Whitebox Plan (VS Zone), Core Vision, Combat Pillars  
### Updated for Simplified Combat + Long-Term Zone Relevance (Lv 1–15)

---

# 1. Encounter Difficulty Tiers (Simplified, Low-Complexity System)

These tiers reflect Caelmor’s grounded, low-cognitive-load combat style.  
Normal enemies use **1–2 predictable attacks**, **fixed cooldowns**, and **no pattern recognition** requirements.

## **Tier 0 — Passive / Low Threat (Training Tier)**
**Examples:** Furrow Boars, Marsh Fen Geese  
- Aggro: only on hit or within 2–3m  
- Attacks: 1 slow basic strike/charge  
- Purpose:  
  - Introduce HP loss, food usage  
  - Train Hunting to ~Lv 10  
  - Provide safe XP / resource loop

---

## **Tier 1 — Basic Hostiles (Everyday Combat)**
**Examples:** Field Goblins, Ash Hounds  
- Attacks:  
  - Goblin: basic poke every ~2.8s  
  - Hound: short-lunge every ~4s (simple audio cue)  
- Behavior: predictable, low threat unless swarmed  
- Purpose:  
  - Core combat loop foundation  
  - Melee/Ranged XP training from Lv 1–12  

---

## **Tier 2 — Moderate Hostiles (Role Introduction)**
**Examples:** Lost Footman, Goblin Lookout  
- Roles:  
  - Footman = slow, tanky melee  
  - Lookout = simple ranged chip damage  
- Attacks:  
  - Footman heavy swing every ~3.5s  
  - Lookout rock toss every ~3.0s  
- Purpose:  
  - Introduce mixed-role encounters  
  - Encourage soft target prioritization  
  - Suitable for Lv 7–15 XP progression  

---

## **Tier 3 — Rare Strong Variant (Early Mid-Game Spike)**
**Examples:** Elite Ash Hound (rare)  
- Same attacks as Tier 1 → slightly stronger stats  
- Spawn rate: 5–10% in deeper zone areas  
- Purpose:  
  - Provide meaningful challenge without mechanics  
  - Create memorable “danger moments” in Lowmark  
  - Remain viable XP for mid-tier players (Lv 10–15)  

---

# 2. Encounter Placement by Whitebox POI

This section directly maps difficulty tiers to the provided VS Whitebox layout.

---

## **A. Overlook Ridge — Safe Start**
**Difficulty Tier:** None  
**Enemies:** None  
**Purpose:**  
- Onboarding, orientation, and tone establishment  
- Prevent early deaths or aggro surprises  

---

## **B. Creek Crossing — Introductory Encounters**
The zone forks here: combat-forward route vs wildlife-forward route.

### **Direct Bridge Path**
- **1× Field Goblin (Tier 1)**  
  - Positioned near broken plank bridge  
  - Intended as optional first combat  
  - Slow poke every ~2.8s

### **Left Creekbank Path**
- **1× Furrow Boar (Tier 0)**  
- **5% chance: 1× Ash Hound (Tier 1)**  
- Role: gentle Hunting introduction, low-pressure engagement  
- Player can completely avoid combat if desired

**Design Intent:** Teach that the world allows routing choices.

---

## **C. Ruined Farmstead — Primary Encounter Pocket**
(Follows Whitebox composition exactly)

### **Enemy Composition**
- **2× Field Goblins (Tier 1)**  
- **1× Ash Hound (Tier 1)** on a simple 12–15m patrol

### **Placement & Behavior**
- Goblins spaced 8–12m apart to avoid accidental double-pulls  
- Hound strolls a predictable oval path, no erratic movement  
- Barn/fence geometry allows LOS breaks and repositioning

### **Difficulty Target**
- For Lv 3–7 players: meaningful but fair  
- For Lv 8–12 players: efficient training spot  
- Clear, readable combat without needing animation analysis

**Purpose:** First “real” fight but not mechanically demanding.

---

## **D. Field Edges — Wildlife Training Loop**
### **Enemy Composition**
- **1–2× Furrow Boars (Tier 0)**  
- **10% chance: 1× Ash Hound (Tier 1)**

### **Design Role**
- A safe mid-zone breathing area  
- XP source for Hunting and early Melee/Ranged  
- Useful for players up to ~Lv 10–12 thanks to low-risk sustain

### **Behavior Notes**
- Boars have very slow commit attacks (2.5–3s intervals)  
- Ideal place for narrative beats involving calm atmosphere

---

## **E. Old Boundary Wall — Secondary Combat Pocket**
(Follows Whitebox: 1 Footman + 1 Lookout)

### **Enemy Composition**
- **1× Lost Footman (Tier 2)**  
  - Slow, tanky, heavy swing every 3.5s  
- **1× Goblin Lookout (Tier 2)**  
  - Simple ranged rock toss every 3.0s  
  - Slight delay before aggro so player can evaluate terrain

### **Placement**
- Footman blocks narrow entrance gap  
- Lookout stands on elevated stone chunk (LOS-dependent)

### **Difficulty Target**
- For Lv 5–8 players: challenging but fair  
- For Lv 9–15 players: sustainable XP with light danger  
- Encourages target prioritization (Lookout → Footman)

**Purpose:**  
The “capstone” encounter of the VS zone, introducing mixed combat roles **without requiring mechanical mastery**.

---

# 3. Combat Pacing Across the Zone

Combat pacing follows the traversal cadence of the whitebox.

## **Phase 1 — Overlook Ridge (0–60m)**
- Combat: none  
- Focus: movement, atmosphere, orientation  

---

## **Phase 2 — Creek Crossing (60–120m)**
- Combat: optional  
- Difficulty: Tier 0–1  
- Teaches: choosing confrontational vs safe routes  
- Encourages: early Hunting/Combat XP trickle  

---

## **Phase 3 — Ruined Farmstead (120–150m)**
- Combat: first structured encounter  
- Difficulty: Tier 1  
- Pacing: deliberate but simple  
- Expected TTK: 6–10 seconds per enemy at early levels  
- Reinforces: single-pull safety, avoid swarming, basic DPS pacing

---

## **Phase 4 — Field Edges (150–200m)**
- Combat: wildlife, low pressure  
- Difficulty: Tier 0–1  
- Pacing: decompression zone  
- Supports: resource gathering, food prep, Hunting XP  
- Good narrative placement for “breathing” story beats  

---

## **Phase 5 — Boundary Wall (200–240m)**
- Combat: moderate, mixed roles  
- Difficulty: Tier 2  
- Pacing: intended final spike  
- Ensures: zone remains relevant for Combat Lv ~10–12  
- Not mechanically complex — just slightly tankier and ranged chip damage  

---

# 4. Zone Longevity and Progression Relevance (Lv 1–15)

To ensure Lowmark Vale does NOT become obsolete at Lv 4:

## **Combat Skills**
- Tier 1/2 enemies provide viable Melee/Ranged XP until ~Lv 12–15  
- Rare Tier 3 variants add mild danger + improved drops

## **Hunting/Leatherworking**
- Boars + Hounds support Hunting progression into mid-game  
- Hide/Meat availability stays relevant for Cooking/Armor crafting

## **Mining/Woodcutting**
- Resources placed at Farmstead & Boundary Wall stay viable  
- Ensures consistent material supply for Smithing/Fletching up to ~Lv 10–15

---

# 5. Summary Table (Handy for Narrative & Quest Integration)

| POI | Enemy Types | Difficulty Tier | Player Level Range | Encounter Purpose |
|-----|-------------|-----------------|--------------------|-------------------|
| Overlook Ridge | None | — | 1–15 | Safe intro, tone-setting |
| Creek Crossing | Goblin / Boar | 0–1 | 1–6 | Optional first combat, routing choice |
| Farmstead | 2 Goblins + Hound | 1 | 3–12 | First structured fight, simple multi-target flow |
| Field Edges | Boars / rare Hound | 0–1 | 1–12 | Wildlife loop, low-pressure pacing |
| Boundary Wall | Footman + Lookout | 2 | 5–15 | Mixed roles, capstone encounter |

---

# 6. Notes for the QUESTLINE & NARRATIVE DESIGNER

This combat layout supports:
- Micro-story beats between pockets  
- Safety zones for exposition + NPC placement  
- Natural escalation without mechanical complexity  
- Predictable enemy behavior (good for telegraphing through environment instead of animations)  
- Long-term relevance of Lowmark for skill progression  
- Optional encounters that support narrative themes (caution, recovery, remnants of war)

Narrative designers can rely on consistent enemy threat levels and clear pacing breaks for dialogue moments, environmental storytelling, and quest triggers.

---

# End of Document
