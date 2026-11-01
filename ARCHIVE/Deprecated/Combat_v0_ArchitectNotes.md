# Combat_v0_ArchitectNotes.md
### Caelmor — Combat v0 Tick/Network Integration & Prediction Review  
### Role: Networking, Persistence & Systems Architect  
### Version: VS v1.0

---

## 1. Purpose & Inputs

This note validates **Combat v0** against the Vertical Slice technical architecture, focusing on:

- Tick integration and timing
- Network timing and latency tolerance
- Prediction vs rollback needs and boundaries

Primary inputs:

- **Combat v0 Design** (timings, telegraphs, hit windows) :contentReference[oaicite:0]{index=0}  
- **CombatSystem.cs** (host-authoritative implementation) :contentReference[oaicite:1]{index=1}  
- **Phase 1.4 Technical Foundation** (10 Hz tick, server authority) :contentReference[oaicite:2]{index=2}  
- **VS Networking Model + Review Notes** (message types, prediction, corrections)   

---

## 2. Tick Integration Validation

### 2.1 Tick Rate & Timing Conversion

- Authoritative tick interval: **0.1s (10 Hz)**. :contentReference[oaicite:4]{index=4}  
- CombatSystem uses `GameConstants.TICK_INTERVAL_SECONDS` and `SecondsToTicks()` with `Mathf.RoundToInt` + min 1 tick. :contentReference[oaicite:5]{index=5}  

Mapping of design timings → ticks:

| Attack   | Phase         | Seconds (Design) | Approx Ticks (10 Hz) |
|----------|---------------|------------------|----------------------|
| Light    | Wind-up       | 0.32s            | 3 ticks              |
| Light    | Hit Window    | 0.10s            | 1 tick               |
| Light    | Recovery      | 0.36s            | 4 ticks              |
| Heavy    | Wind-up       | 0.58s            | 6 ticks              |
| Heavy    | Hit Window    | 0.14s            | 1 tick               |
| Heavy    | Recovery      | 0.60s            | 6 ticks              |

This matches the design intent: **≥3 ticks of visible telegraph** and **single-tick hit windows** for both light and heavy attacks. :contentReference[oaicite:6]{index=6}  

**Conclusion:**  
Tick quantization is acceptable and preserves the combat feel described in the design doc. No sub-tick timing required.

---

### 2.2 Attack State Machine vs Tick Loop

CombatSystem flow (per tick): :contentReference[oaicite:7]{index=7}  

1. `ProcessAttackTimersAndIntents(tickIndex, inputs)` from TickManager:
   - Apply attack inputs (`HandleAttackInput`).
   - Advance state machines (`ProcessAttackStates`).

2. **StartAttack:**
   - Validates attacker/target.
   - Computes `WindupEndTick`, `HitWindowEndTick`, `RecoveryEndTick`.
   - Sets state = `Windup`.

3. **ProcessAttackStates:**
   - `Windup` → `HitWindow` when `tick >= WindupEndTick`.
   - `HitWindow`:
     - Calls `PerformHitIfValid` each tick in window.
   - `Recovery`:
     - Ends sequence and removes entry when `tick >= RecoveryEndTick`.

Because hit windows round to **1 tick** in v0, `PerformHitIfValid` is only called once per attack; no multi-hit bug is exposed. If future designs widen hit windows beyond 1 tick, we should add a `HasHit` flag to `AttackInstance` to enforce single-hit behavior.

**Conclusion:**  
The attack state machine is **tick-aligned and deterministic**, and integrates correctly with a single per-tick call from TickManager.

---

### 2.3 Movement / AI / Combat Ordering

Technical spec for TickManager: **movement → AI → combat → world → snapshot**.   

CombatSystem assumes:

- `WorldManager.GetEntity()` returns **post-movement** positions.
- Range & arc checks (`InAttackRangeAndArc`) use those positions. :contentReference[oaicite:9]{index=9}  

As long as TickManager calls:

1. Movement system
2. AIController
3. `CombatSystem.ProcessAttackTimersAndIntents()`

in that order, the combat pipeline matches the design requirement that **spacing and positioning matter** and that range is evaluated after all movement for the tick is resolved.

**Conclusion:**  
Attack resolution is correctly positioned in the global tick order, provided TickManager respects the documented sequence. No rollback is needed to reconcile movement + combat.

---

## 3. Network Timing & Latency Budget

### 3.1 Client → Host → Tick Latency

Path: Client input → network → host buffer → next tick → simulation → snapshot → client.

With:

- Tick interval: 100 ms
- Typical small-session RTT: 50–150 ms

We expect:

- **Input-to-impact latency** ~150–300 ms worst-case in online conditions.
- **Telegraph durations**:
  - Player light wind-up: 0.32s (~3 ticks)
  - Enemy telegraphs: 0.40–0.75s (4–8 ticks) :contentReference[oaicite:10]{index=10}  

Result: even under moderate RTT, players see:

- Local attacks: they press attack and **immediately see the swing** (client-side animation), but damage/hit result is confirmed from the host after ~200ms.
- Enemy attacks: telegraphs are long enough that **even snapshot + network delay** still leaves multiple visible ticks of warning.

**Conclusion:**  
Telegraph timings are intentionally generous and **tolerate typical VS latencies** without demanding advanced rollback or sub-tick reconciliation.

---

### 3.2 Snapshot Frequency & Jitter

- Host sends transform snapshots at 10–20 Hz (TBD; spec recommends 10 Hz to match tick).   
- Combat results (`Event_CombatResult`) are sent reliably **on the tick where damage is applied**. :contentReference[oaicite:12]{index=12}  

This means:

- Position desyncs are handled via interpolation and correction on the client.
- Combat is **never predicted**; only animations are, so late arrivals are just visual alignment issues, not logic errors.

**Impact:**  
Some enemies may appear a fraction of a second behind their actual server positions under poor network conditions, but:

- Range checks are done **only on host**.
- Client visuals are corrected toward server over time.
- Because Caelmor’s melee is slow and deliberate, small transform jitter does not undermine the core combat fantasy.

---

## 4. Prediction & Rollback Requirements

### 4.1 Movement Prediction

From VS Networking Model & Review Notes: clients are expected to perform **lightweight movement prediction** for the local player, with **soft corrections** and occasional hard snaps when error > threshold.   

Combat v0’s range checks work with this model because:

- Range is checked server-side using authoritative positions.
- Even if the client thinks they are slightly closer or further, **only the server decision matters**.
- Incorrect local expectations (“I thought I was in range”) manifest as occasional misses but not inconsistencies between players.

**Conclusion:**  
Movement prediction is **required** for feel, but remains shallow and does not require rollback.

---

### 4.2 Combat Prediction

Current CombatSystem behavior:

- Hit detection & damage application occur **only on server** via `PerformHitIfValid`. :contentReference[oaicite:14]{index=14}  
- Client simply:
  - Sends `PlayerInput_Attack`.
  - Plays an animation.
  - Listens for `Event_CombatResult` to update HP bars, death states, etc.

**Architect stance:**

- **No combat prediction** for VS.
- **No rollback**:
  - We never need to re-simulate prior ticks on client or host.
  - Telegraphed, slow attacks remove any need for frame-perfect local feedback.
- Only “prediction” is visual:
  - Start swing animation immediately on input.
  - If server rejects the attack (invalid state/target), just don’t show damage.

**Conclusion:**  
Combat v0 is deliberately designed to **avoid the complexity of rollback**. This is aligned with the design philosophy: **readable, grounded, not twitchy**.   

---

### 4.3 Edge Case: High Latency or Packet Loss

Under very poor network conditions:

- Attacks might feel delayed or inconsistent (client sees swing, but damage appears late or never).
- Given VS scope (small co-op, not PvP) and the design goal of **casual, low-stress combat**, this is acceptable.

If later UX tests show too much perceived delay:

- We can optionally:
  - Show a **local “ghost damage” flash** that is overwritten if the server denies the hit.
  - Increase telegraph durations even more for enemies.

---

## 5. Specific Implementation Recommendations

### 5.1 Minor Changes to CombatSystem

1. **Single-hit protection (future-proofing):**
   - Add `bool HasAppliedHit` to `AttackInstance`.
   - In `PerformHitIfValid`, if `HasAppliedHit` is true, return immediately.
   - Set `HasAppliedHit = true` upon successful hit.
   - Keeps behavior correct if we widen hit windows beyond one tick.

2. **Debug Fields (optional for VS):**
   - Include `lastAttackTick` / `lastHitTick` per attacker for debugging logs.
   - Helps correlate perceived latency with tick indices.

### 5.2 TickManager Integration Contract

Ensure TickManager:

- Calls `CombatSystem.ProcessAttackTimersAndIntents(currentTick, attackInputsFromNetwork)` **after** movement & AI each tick.
- Provides `attackInputsFromNetwork` as **all PlayerInput_Attack messages received since last tick**, ordered by arrival time and de-duplicated by sequence number (if implemented).   

### 5.3 Networking Layer

- **Input messages**:
  - Add `uint Sequence` to `PlayerInput_Attack`, used only for anti-spam and debugging.
- **Combat result messages**:
  - Include `TickIndex` (already in `Event_CombatResult`) and surface it in client logs/UI for debugging latency-based issues.

---

## 6. Summary

**Tick Integration**

- Combat v0 is correctly tick-aligned at **10 Hz**.
- Attack timings and telegraphs map cleanly to integer ticks.
- State machine behavior is deterministic and compatible with the global tick pipeline.

**Network Timing**

- Telegraphed, slow attacks are robust against typical RTTs.
- Transform snapshots + event-based combat messages suffice; no special timing hacks needed.

**Prediction & Rollback**

- Movement uses **simple prediction + correction**.
- Combat uses **no prediction**, **no rollback**; server-only damage resolution.
- This matches Caelmor’s high-level philosophy and keeps the VS implementation light and stable.

The current design is therefore **approved for VS scope**, with only small recommended tweaks to improve robustness and future-proofing.

---

# End of Document
