# Combat v0 Design  
### Vertical Slice — Caelmor  
### Role: Gameplay Systems & Combat Designer

---

# 1. Combat Philosophy (VS Scope)

Combat v0 supports Caelmor’s early-game identity:

- **Grounded, readable, and predictable** (Pillars & Tenets)  
- **No reflex-heavy timing analysis** except for bosses/minibosses  
- **Simple 1–2 attack options** for both player and early enemies  
- **Clear silhouettes and slow telegraphs** for the top-down camera  
- **No animation locks that reduce approachability**  
- **Tick-aligned, host-authoritative resolution** (10 Hz)  

The goal is to create a **fair, low-friction combat loop** suitable for Levels 1–10 and matched to the Lowmark VS Whitebox.  

---

# 2. Attack Types (Player)  
v0 includes:  
- **Light Attack (Primary)**  
- **Heavy Attack (Optional/Intro Only)**  
- No combos, no chaining, no stance-swaps.

### 2.1 Light Attack  
- **Wind-up:** 0.32s  
- **Hit window:** 0.10s (centered at 0.32–0.42s)  
- **Recovery:** 0.36s  
- **Total Duration:** ~0.78s  
- **Stamina Cost:** 0 (v0 excludes stamina management)  
- **Purpose:** Default attack; consistent and simple.

Readability:  
- Small forward lean and thrust in animation (non-functional).  
- Sound cue on wind-up for accessibility.

### 2.2 Heavy Attack  
Included to define the pipeline, but does **not appear in the VS quest chain** unless you choose to activate it.

- **Wind-up:** 0.58s  
- **Hit window:** 0.14s (0.58–0.72s)  
- **Recovery:** 0.60s  
- **Total Duration:** ~1.32s  
- **Stamina Cost:** 0  
- **Damage:** ~1.75× light attack  
- **Movement Slow:** 40% during wind-up + recovery  
- **Cancel:** Only backward movement or block (if implemented)

Design intent:  
- Teaches “committed attacks” without animation punishment.  
- Creates early identity for later role-differentiated combat.

---

# 3. Telegraph Timings (Player & Enemy)

Because Caelmor avoids combat that requires animation study for normal encounters, **telegraphs are slow and obvious**.

### 3.1 Player Telegraphs  
- **Light Attack:** 0.20s readable wind-up (0.32s total)  
- **Heavy Attack:** 0.40–0.50s of visible anticipation  

### 3.2 Enemy Telegraphs (Tier 0–2)  
From VS Encounter Design:

- Goblin Poke: **0.40s telegraph**, attack every ~2.8s  
- Hound Lunge: **0.55s wind-up** (audio + crouch), cooldown ~4.0s  
- Footman Heavy Swing: **0.75s arc wind-up**, cooldown 3.5s  
- Lookout Rock Throw: **0.45s raise-arm telegraph**, cooldown 3.0s  

These must remain readable under a top-down camera (Whitebox v1.1).  

---

# 4. Hit Windows & Collision Rules

### 4.1 Raycast / Capsule Model  
v0 uses a simple forward capsule check:
- **Range:** weapon length (1.4–1.6m typical)  
- **Angle:** 60° cone in front of player  
- **Trigger:** opens when the tick index enters the hit window

### 4.2 Hit Window Definition  
A hit is valid if:
1. Server tick time is within the defined hit window  
2. Target is inside forward arc and range  
3. Attack not cancelled by movement reversal or block  

### 4.3 Multi-hit  
No multi-hit frames in v0.  
All basic attacks apply exactly one damage event.

---

# 5. Stamina Interactions (VS Rules)

Per Deep Research Findings and Phase 1 design intent, **stamina should never frustrate core combat**.

Therefore, v0 stamina rules:

### 5.1 Movement  
- **No stamina drain on sprinting** (ensures no friction for traversal).  
- **No stamina drain on dodging (since dodge is not present in v0).**

### 5.2 Attacks  
- Light and heavy attacks cost **0 stamina**.  
- Future phases may assign stamina cost but v0 explicitly avoids it.

### 5.3 Blocking  
Blocking (optional) consumes stamina **only on hit**, never for holding block.

---

# 6. Block / Dodge Rules (VS Scope)

Caelmor v1 does **NOT** use fast-paced action combat.  
Therefore block/dodge remain simple:

## 6.1 Block (Optional for VS, but included in design)
- **Hold to block**  
- **Damage Reduction:** 60%  
- **Stamina Cost:** 0 on hold, 3–4 on hit (if stamina system later desired)  
- **Block Break:** none in v0  
- **Movement:** 70% speed while blocking  
- **Cancel:** instantly on release  

Low complexity, entirely optional to implement in VS.

## 6.2 Dodge  
**Not included in v0.**  
Rationale:
- Increases reflex dependency  
- Adds complexity to animation canceling  
- Harder to synchronize over 10 Hz tick  
- Out of scope for “readable, predictable combat” (Phase 1 Pillars)

Dodge may be introduced in Combat v1+ with clear telegraph vs action tradeoffs.

---

# 7. Tick Alignment Requirements

### 7.1 Tick Rate  
Authoritative tick: **10 Hz (every 100ms)**  
From Technical Foundation.  
:contentReference[oaicite:0]{index=0}

### 7.2 Attack State Machine  
On the **host**, attack states are resolved as:

1. **StartAttack:** local client sends command  
2. **Host validates:**  
   - not mid-attack  
   - target in front (optional early check)  
   - weapon equipped  
3. **Host schedules attack event** for `TickCurrent + windupTicks`  
4. **Hit window opens** for `(startTick + windup) → (startTick + windup + window)`  
5. **Damage resolved** on host only  
6. **Snapshot sent** to clients with animation state + facing  

### 7.3 Network Stability  
Wind-up + hit window timings are chosen to avoid rounding errors:  
- Minimum telegraph length: 0.32s = ~3 ticks  
- Minimum hit windows: 0.10–0.14s = 1–2 ticks  

This makes tick-resolution deterministic and readable.

---

# 8. Combat States (v0)

- **Idle**  
- **Wind-up (light/heavy)**  
- **Attack_Active (hit window)**  
- **Recovery**  
- **Blocking (optional)**  
- **Hitstun (minimal, 0.1s)**  
- No combos, cancels, lock-ons, or weapon swaps in VS.

---

# 9. Damage & TTK Expectations

From encounter design:
- **Expected TTK:** 6–10 seconds vs Tier 1 enemies  
- **Heavy attack:** small tactical benefit without complexity  
- **Block:** defensive option but not required  

Player Level 1–4 tuning example:
- Light Attack: ~4–6 damage  
- Heavy Attack: ~7–10 damage  
- Goblin HP: 20–24  
- Footman HP: 32–38  

This aligns with Phase 1.5 content pacing and Lowmark ecology.

---

# 10. Interrupts & Cancels

To avoid animation frustration:
- **Forward movement does NOT cancel attacks**  
- **Backward movement cancels during wind-up only**  
- **No cancels during hit window or recovery**  
- **Block cancels wind-up**  

---

# 11. Future Extensions (v1 → v2)

v0 establishes the pipeline for:
- Weapon categories (fists, swords, spears)  
- Role-based enemy behaviors  
- More advanced telegraph logic  
- Stamina if desired (NOT recommended per Deep Research Findings)

---

# 12. Summary (Implementation Notes)

- Simple 1–2 attack movesets  
- Clear telegraphs for all actors  
- Predictable damage windows  
- No dodge, optional block  
- No stamina friction  
- Tick-aligned timing → deterministic behavior  
- Suitable for host-authoritative networking  
- Fully compatible with Lowmark VS Whitebox encounter pacing

