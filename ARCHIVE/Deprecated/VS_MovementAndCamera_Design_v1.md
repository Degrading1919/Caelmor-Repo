# VS Movement & Camera Design  
Vertical Slice — Caelmor  
Role: Gameplay Systems & Combat Designer

---

# 1. Movement Philosophy (Grounded, Readable, Low-Friction)

Movement in Caelmor’s VS follows the principles established in Phase 1.1–1.4:

- **Slow, grounded, deliberate traversal** appropriate for a mythic-medieval world.  
- **No stamina tax on movement** — sprint never punished (Phase 1.3)  
- **No freeform jump; contextual agility triggers instead** (Phase 1.3)  
- **Camera prioritizes readability, silhouette clarity, and player comfort.**

This produces a system that is:
- easy for new players  
- stable for networked play  
- highly predictable for combat positioning  
- performant under a top-down/OTS hybrid camera

---

# 2. Walk / Sprint Cadence

## 2.1 Core Movement Speeds  
**Walk Speed:** 3.4 m/s  
**Sprint Speed:** 4.8 m/s  
These numbers align with the Technical Foundation’s goals of “grounded medieval traversal” and top-down readability.

**Design Rules:**
- Sprint has *no stamina bar* or movement penalty (Phase 1.3).  
- Sprinting is *always allowed*, as long as player input is held.  
- Walk is automatically engaged whenever input magnitude < 60%.  
- No animation locks in VS; animation blend spaces must feel light and responsive.

## 2.2 Cadence & Responsiveness  
- Time to reach full walk speed: **0.18s**  
- Time to reach full sprint speed: **0.28s**  
- Deceleration: **0.14s** to full stop (fast but not snappy).  

Goal: Movement feels weighty enough to fit the grounded theme, while still avoiding the “sluggish” feel that creates early-game churn (Deep Research Findings).

---

# 3. Turn Speed & Facing Model

Caelmor uses a **soft-targeting, direction-based movement model** suitable for OTS/top-down hybrid views.

## 3.1 Turn Speed  
- **Base Turn Rate:** 420°/sec  
- **Sprint Turn Dampening:** 15% slower  
- Camera is unaffected by turn speed; it updates instantaneously with player input.

Rationale:
- High turn rate preserves responsiveness under an elevated camera.  
- Slight sprint dampening prevents zig-zag micro-corrections from feeling jittery.

## 3.2 Facing Behavior  
- Character always faces *movement direction* unless actively attacking.  
- During attack animations, facing is locked for the duration of the hit window, then returns to movement-driven.

This complements deliberate combat pacing (Phase 1.2 Pillar B).

---

# 4. Acceleration & Deceleration Curves

Movement uses **simple, tunable curves** to reduce animation/simulation complexity for the solo developer.

## 4.1 Acceleration Model  
**Acceleration Curve:** SmoothStep(0 → targetSpeed, 0.18–0.28s window)

Rationale:
- Prevents teleport-like snapping on networked clients.  
- Feels grounded without sluggishness.  
- Ensures predictable positioning for tick-based combat.

## 4.2 Deceleration Model  
**Deceleration Curve:** Linear falloff to 0 in 0.14s

Reasoning:
- Immediate but not abrupt; enough momentum to feel real but not enough to break combat readability.

---

# 5. Jump Rules (VS Scope)

Per **Phase 1.3 Technical Foundation**, Caelmor does **not** use a freeform jump button:

> “Vertical traversal does not use a jump button; instead, agility triggers are placed in the environment.”  
:contentReference[oaicite:0]{index=0}

### VS Agility Trigger Types
Each trigger contains:
- animation type  
- start → end position  
- facing correction  
- optional placing offset

### Included in VS:
- **Step-Up (0.2–0.6m)**
- **Vault (low fences & logs)**
- **Creekbank Hop (1–1.4m lateral hop)**
- **Ledge Slide / Drop (≤ 1m)**

### Excluded:
- Climbing  
- Long jumps  
- Multi-trigger parkour chains

**Player Rule:**  
If the player walks into a trigger volume, the contextual animation auto-plays (interruptible by backward movement to prevent lock-in).

This supports:
- clean top-down readability  
- strong environment control  
- minimal animation/network desync risk

---

# 6. Camera System (Top-Down / OTS Hybrid)

The VS camera must support both:
- **Top-down tactical readability** (as specified in Whitebox v1.1)  
- **Slight OTS tilt** for immersion and landmark visibility

## 6.1 Camera Angle & Height  
**Default Height:** 9.5m  
**Default Pitch:** 52°  
**Hard Minimum Height:** 8.0m  
**Soft Maximum Height:** 12.5m

Reasoning:  
These values provide:
- clear silhouette reading of enemies  
- good visibility of POI landmarks (ridge, creek, farmstead, wall)  
- minimal occlusion from trees/structures  

## 6.2 Field of View  
**FOV:** 38°  
Lower FOV preserves top-down readability and prevents spatial distortion during navigation.

## 6.3 Camera Follow Behavior  
- Spring-based smoothing with no overshoot  
- Follow lag: **0.12s**  
- Rotation lag: **0.06s**  
- Zero camera sway (to avoid nausea in top-down hybrid perspective)

## 6.4 Collision Rules  
- Camera pulls closer when colliding with world objects  
- Never passes below 45° pitch  
- Hard-clamps distance to avoid tunnel-like zoom-ins

This follows Phase 1.3 design guidance:  
> “Camera-controlled zoom only. Collision-correcting camera prevents clipping and disorientation.”  
:contentReference[oaicite:1]{index=1}

---

# 7. Combat Readability Requirements (Camera → Movement Interplay)

Camera design must support deliberate, readable combat:
- Enemies must remain fully visible at all times  
- Telegraphed swings (2.8–3.5s) must be readable under zoom  
- Clusters limited to 1–2 hostiles at once (per VS Whitebox)

Movement integrates by:
- ensuring sprinting does NOT break silhouette readability  
- keeping facing predictable during attack sequences  
- preventing jump arcs that would break camera framing  
- mild turn dampening during sprint to reduce chaotic motion

---

# 8. Network Considerations (Tick Alignment)

Movement is simulated host-authoritatively on a **10 Hz tick** (Phase 1.4).  
Camera remains strictly client-side and prediction-friendly.

Movement parameters chosen for:
- predictable interpolation  
- low drift between ticks  
- smooth server corrections (0.18–0.28s accel curves prevent jarring snaps)

---

# 9. VS Deliverables Summary

This file defines:

- Walk speed, sprint speed, cadence  
- Acceleration/deceleration curves  
- Turn speed & facing logic  
- Removal of jump in favor of agility triggers  
- Full camera rules (height, pitch, smoothing, collision)  
- Combat readability impacts  
- Network-alignment considerations

This spec is ready for conversion into PlayerController.cs and CameraController.cs by the Engine-Agnostic Coding Assistant.

