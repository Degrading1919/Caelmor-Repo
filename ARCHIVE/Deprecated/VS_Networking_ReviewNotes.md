# VS_Networking_ReviewNotes.md
### Caelmor — Vertical Slice Networking Review & Latency Notes  
### Role: Networking, Persistence & Systems Architect  
### Version: VS v1.0 Review

---

## 1. Context & Goals

This document reviews the current Vertical Slice networking design and implementation, focusing on:

- Latency surfaces and their gameplay impact  
- Correction rules for movement and state  
- Concrete improvements to **NetworkManager.cs** and the **VS_Networking_Model** specification  

It assumes:

- **Host-authoritative model** as defined in Phase 1.4 Technical Foundation and VS_Networking_Model.   
- **10 Hz TickManager** driving simulation and snapshots. :contentReference[oaicite:1]{index=1}  
- Current **NetworkManager** implementation as the VS minimum networking facade. :contentReference[oaicite:2]{index=2}  

---

## 2. Latency Surfaces & Risk Points

### 2.1 Input → Tick Latency

**Flow:**

Client input → Transport send → Host receive & buffer → Next TickManager tick → Simulation step

Risk points:

- **Input-to-tick delay**:  
  - Worst-case: input arrives just after a tick; it will be processed on the next tick (up to 100 ms later).  
  - With network RTT, perceived delay can be ~100–150 ms even in LAN-like conditions.

- **Current implementation:**
  - Host buffers `PlayerInput_Move` and `PlayerInput_Attack` into `_bufferedInputs`. :contentReference[oaicite:3]{index=3}  
  - `DrainBufferedInputs()` returns a fresh `InputBatch` each tick and clears the buffer.  
  - This is correct structurally but **lacks timestamp/sequence metadata**, so:
    - No way to detect stale/out-of-order inputs.
    - No room to do time-based reconciliation.

**Recommendation:**

- Extend input DTOs (e.g., `PlayerInput_Move`, `PlayerInput_Attack`) with:
  - `uint Sequence` and/or `long ClientInputTimestamp`.  
- TickManager should:
  - Process inputs **in sequence order per client**.
  - Optionally discard inputs older than N ticks.

---

### 2.2 Tick → Snapshot → Render Latency

**Flow:**

Simulation tick → Snapshot build → Transport send → Client receive → Client apply & render

Risk points:

- **Transform snapshot frequency**:
  - `BroadcastTransformSnapshot` can be called every tick or at a lower rate. :contentReference[oaicite:4]{index=4}  
  - At 10 Hz, plus RTT and render frame timing, remote entities may appear slightly delayed and jittery.

- **Current implementation:**
  - Client receives `Msg_Snapshot_Transforms` and passes snapshot to `ClientWorld.ApplyTransformSnapshot`. :contentReference[oaicite:5]{index=5}  
  - No explicit interpolation/blending logic is defined in this file; it’s assumed to exist in `ClientWorld`.

**Recommendations:**

- Ensure `ClientWorld`:
  - Buffers at least 2–3 snapshots per entity.
  - Interpolates based on **snapshot timestamps or TickIndex** rather than snapping immediately.
- For local player:
  - Use client-side prediction with gentle reconciliation (see §3.1).

---

### 2.3 Join/Resync Latency

**Flow:**

JoinRequest → Load PlayerSave + WorldSnapshot → JoinAccept → Scene load → Receive first snapshots

Risk points:

- **Cold start jitter**:
  - Immediately after join, the client might see a “pop” from default positions to authoritative positions.

- **Current implementation:**
  - `ProcessJoinRequest` loads `PlayerSave` and `WorldSnapshot`, spawns player, then sends `Msg_JoinAccept`. :contentReference[oaicite:6]{index=6}  
  - Client currently just sets `LocalClientId` on `Msg_JoinAccept`; world and player instantiation is left to other systems.

**Recommendations:**

- Ensure **initial snapshot** (player + world) is treated as a full baseline:
  - Client should **not** run prediction until the first authoritative spawn & transform snapshot is applied.
- Add an explicit `Msg_Resync_PlayerState` for debug and manual resync requests (aligning with VS_Networking_Model). :contentReference[oaicite:7]{index=7}  

---

## 3. Correction Rules (Recommended)

### 3.1 Movement Correction

**Current state:**

- Client sends `PlayerInput_Move` unreliably; host simulates, then periodically sends transform snapshots.
- `ClientWorld.ApplyTransformSnapshot` is called directly for each snapshot, but no correction policy is defined here. :contentReference[oaicite:8]{index=8}  

**Recommended rules:**

1. **Local player (predicted):**
   - Maintain both:
     - `PredictedPosition` (client-side integration)  
     - `AuthoritativePosition` (from host snapshot)
   - Compute error vector `E = AuthoritativePosition - PredictedPosition`.

   - If `|E| < smallThreshold` (e.g., 0.15m):
     - Smoothly lerp toward authoritative over the next few frames.
   - If `|E| >= snapThreshold` (e.g., 1.0–1.5m):
     - Hard snap to authoritative to prevent wallhacks / desync.

2. **Remote players & enemies:**
   - Always treat position updates as networked interpolation:
     - Do not predict; only interpolate/extrapolate with a small buffer (1–2 snapshots behind real time).
   - No hard snap unless the entity is extremely far off-screen or teleports.

3. **Authoritative checks:**
   - Host should reject movement inputs that request impossible warps:
     - E.g., large displacement between ticks compared to max speed.

### 3.2 Combat State Correction

**Current state:**

- `BroadcastCombatEvent` sends `Event_CombatResult` to clients.  
- No client-side prediction for damage is implemented. :contentReference[oaicite:9]{index=9}  

**Recommended rules:**

- **Combat = no prediction**:
  - Clients only play animations locally; all HP and death states come exclusively from server.
- If client HP display differs due to stale UI:
  - Always overwrite with authoritative HP from host.
- When a combat result arrives late:
  - Apply as-is; tick index in `Msg_Event_CombatResult` is informational only (can be logged for debugging).

### 3.3 Inventory & Crafting Correction

**Current state:**

- Planned to be event-driven (`SendToHost` for generic messages; future broadcast methods commented as TODO). :contentReference[oaicite:10]{index=10}  

**Recommended rules:**

- Client UI for inventory/crafting must be **fully driven** by authoritative events:
  - No client-side assumption that a move/craft succeeded until a server confirmation event arrives.
- In case of divergence (client thought an item was moved):
  - Rebuild the entire inventory view from server snapshot/events.

---

## 4. Concrete Issues in Current Implementation

### 4.1 `FindObjectOfType<ClientWorld>()` per Packet

**Issue:**

- `HandleClientDataReceived` calls `FindObjectOfType<ClientWorld>()` each time a transform or HP snapshot arrives. :contentReference[oaicite:11]{index=11}  

**Impact:**

- Allocations and repeated hierarchy scans on every incoming packet.
- Latency spikes under moderate packet load; GC pressure in Unity.

**Fix:**

- Cache a reference once:
  - Add `public ClientWorld ClientWorld { get; set; }` on NetworkManager (set via GameManager or bootstrap).
  - Replace `FindObjectOfType<ClientWorld>()` calls with the cached reference, guarding null for menu scenes.

---

### 4.2 Lack of Heartbeat / Timeout Handling

**Issue:**

- `NetworkManager` does not implement explicit heartbeats or timeout logic; relies on transport-level disconnect events. :contentReference[oaicite:12]{index=12}  

**Risk:**

- In some transports, a half-open connection might not trigger `OnServerClientDisconnected` promptly.
- Ghost players may remain in world if the transport does not aggressively detect timeouts.

**Fix:**

- Add lightweight heartbeat:
  - Define `Msg_Heartbeat` ping from client → host at regular intervals.
  - Host tracks `LastHeartbeatTick` per client.
  - If no heartbeat for `N` seconds:
    - Call `HandleClientDisconnected` manually and `KickClient`.

---

### 4.3 Input Batch Growth & Back-Pressure

**Issue:**

- `_bufferedInputs` accumulates `MovementCommands` and `AttackCommands` until drained.  
- No cap or sanity check is applied. :contentReference[oaicite:13]{index=13}  

**Risk:**

- Malicious or buggy client could flood input messages, causing:
  - Huge input batches,
  - Extended tick processing time,
  - Latency spikes / frame drops.

**Fix:**

- Per-client rate limiting:
  - Track number of input messages per tick per client.
  - Discard or clamp movement messages above certain threshold (e.g., 5–10 per tick).
- Global cap:
  - If total buffered input count exceeds a threshold, drop oldest or excessive messages, and log warnings.

---

### 4.4 Join Flow: Unknown Transport Client

**Issue:**

- In `ProcessJoinRequest`, if `FindClientIdByTransport` returns `-1`, the method logs a warning and returns. :contentReference[oaicite:14]{index=14}  

**Risk:**

- A race condition where a client sends `Msg_JoinRequest` just after connecting but before `HandleClientConnected` sets up the mapping could:
  - Leave client in limbo with no response.
- Could also be exploited in edge cases to spam the server with join requests from unknown IDs.

**Fix:**

- If `clientId == -1`:
  - Option A: call `HandleClientConnected(transportClientId)` inline (if safe) or  
  - Option B: Kick the transport client explicitly (`KickClient`) with a clear reason.

---

### 4.5 No AOI / Interest Management (for VS)

**Issue:**

- `Broadcast` sends messages to all clients, with no consideration for area of interest (AOI). :contentReference[oaicite:15]{index=15}  

**Risk (future-facing):**

- Fine for 2–4 player VS; will not scale to larger sessions or more content.
- Increases per-tick bandwidth for each client.

**Suggestion (not required for VS, but easy to seed):**

- Add an optional AOI layer:
  - For now, treat entire VS whitebox as a single AOI (no change).
  - Expose extension points:
    - `ShouldSendMessageToClient(clientId, message)` for future filters.

---

## 5. Recommended Improvements (Prioritized)

### P1 — Mandatory for Smooth VS Feel

1. **ClientWorld caching:**
   - Remove `FindObjectOfType` per packet; cache references.

2. **Movement interpolation & correction:**
   - Implement snapshot buffering and smoothing within `ClientWorld`.
   - Implement thresholds for soft vs hard corrections for local player.

3. **Input metadata:**
   - Add sequence numbers or timestamps to `PlayerInput_Move` / `PlayerInput_Attack`.

4. **Input rate limiting:**
   - Bound per-tick inputs to avoid DoS-like spikes.

5. **Robust join/leave handling:**
   - Clean up unknown-transport join attempts.
   - Ensure disconnect paths always despawn and save.

---

### P2 — Nice-to-Have for VS, Essential for Scaling

1. **Heartbeat & timeouts:**
   - Simple ping mechanism with host-side timeout.

2. **Resync messages:**
   - Add `Msg_Resync_PlayerState` and `Msg_Resync_WorldState` in line with VS_Networking_Model. :contentReference[oaicite:16]{index=16}  

3. **AOI pre-hooks:**
   - Leave a hook in `Broadcast` for future AOI-based filtering.

4. **Debug instrumentation:**
   - Log tick index + snapshot sizes periodically.
   - Measure average & max tick processing time.

---

## 6. Implementation Checklist

**Host / Core:**

- [ ] Extend input DTOs with `Sequence` / `Timestamp`.  
- [ ] Implement per-client input rate limiting.  
- [ ] Cache `ClientWorld` reference in `NetworkManager`.  
- [ ] Add heartbeat messages & timeout handling (optional for VS).  
- [ ] Harden join flow when `clientId == -1`.

**Client:**

- [ ] Implement interpolation/extrapolation in `ClientWorld.ApplyTransformSnapshot`.  
- [ ] Implement local-player prediction and correction thresholds.  
- [ ] Ensure inventory/crafting UIs update only on authoritative events.

**Spec Sync:**

- [ ] Update `VS_Networking_Model.md` to reference:
  - Input sequence/timestamp fields.  
  - Movement correction rules & thresholds.  
  - Heartbeat / timeout mechanism (if implemented).  

Once these items are implemented, the VS networking layer will be resilient to typical LAN/online latencies, preserve Caelmor’s core design goal of **grounded, readable combat**, and provide a solid foundation for scaling to larger sessions without major architectural changes.

---

# End of Document
